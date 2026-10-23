"""Team Chaotix A2A server.

Exposes the team's opencode agents as an A2A agent. The gateway
(agentgateway) fronts this process on the A2A port; this process is the
adapter.

Surface (JSON-RPC 2.0 over HTTP, A2A task collaboration):

- ``GET  /.well-known/agent.json``  agent card (capability discovery). The
  card's skills are generated from ``.opencode/agents/`` on every request,
  so the card is always the team's current roster.
- ``GET  /health``                  liveness.
- ``POST /``                        ``message/send``, ``message/stream``,
  ``tasks/get``, ``tasks/cancel``.

Task addressing: the first token of the task text is ``@<agent>`` (a roster
agent file name; default ``@robotnik``). The remainder is the task brief.

One id, several systems: every task carries a ``contextId``. If the caller
supplies one it is used as-is (that is how an upstream agent links a
conversation); otherwise the server mints one. The contextId is also the
langgraph thread id for the cycle graph (``team.graph``), so the A2A task
record and the graph checkpoint of the same run are queryable from one
string.

No model is invoked by this module's own logic; a task runs one
``opencode run --standalone`` session (or an injected runner in tests).
"""

from __future__ import annotations

import json
import os
import queue
import re
import subprocess
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_DIR = Path(os.environ.get("TEAM_DIR", "/home/howard/AI/projects/team-chaotix"))


def agents_dir() -> Path:
    """The roster directory, resolved at call time so tests can point the
    server at a checkout (TEAM_DIR)."""
    return Path(os.environ.get("TEAM_DIR", str(REPO_DIR))) / ".opencode" / "agents"
OPENCODE = os.environ.get("OPENCODE_BIN", "/home/howard/.opencode/bin/opencode")
PORT = int(os.environ.get("A2A_PORT", "4210"))
PUBLIC_URL = os.environ.get("A2A_PUBLIC_URL", "http://127.0.0.1:4100/")
# opencode run ignores the agent frontmatter model and falls back to the
# first provider in the global config, so pin the team model explicitly.
TEAM_MODEL = os.environ.get("A2A_MODEL", "evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS")
TASK_TIMEOUT = int(os.environ.get("A2A_TASK_TIMEOUT", "7200"))
MAX_TASKS = 64

PROTOCOL_VERSION = "0.3.0"
TEAM_NAME = "team-chaotix"
TEAM_VERSION = "2.0.0"


def agent_description(name: str) -> str:
    p = agents_dir() / (name + ".md")
    try:
        for line in p.read_text().splitlines():
            if line.startswith("description:"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return ""


def agent_model(name: str) -> str:
    p = agents_dir() / (name + ".md")
    try:
        for line in p.read_text().splitlines():
            if line.startswith("model:"):
                return line.split(":", 1)[1].strip().strip('"')
    except OSError:
        pass
    return ""


def load_roster() -> dict[str, str]:
    """Roster straight from the agent files, so the card never drifts from
    the team. Keys are file names without the extension."""
    roster: dict[str, str] = {}
    base = agents_dir()
    if base.is_dir():
        for p in sorted(base.glob("*.md")):
            roster[p.stem] = agent_description(p.stem)
    return roster


def agent_card() -> dict:
    roster = load_roster()
    skills = []
    for name in sorted(roster):
        skills.append({
            "id": name,
            "name": "%s" % name,
            "description": roster[name],
            "tags": [name, TEAM_NAME],
        })
    return {
        "name": TEAM_NAME,
        "description": (
            "Team Chaotix: a twelve-role autonomous software development team "
            "built on opencode. Each skill is a team role. Address a task "
            "with a leading @<role> token (default @robotnik); the rest of "
            "the text is the task brief. The final task's "
            "status.message.parts[0].text is the agent's output."
        ),
        "url": PUBLIC_URL,
        "version": TEAM_VERSION,
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {"streaming": True, "pushNotifications": False},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": skills,
    }


tasks: dict[str, dict] = {}
tasks_lock = threading.Lock()
work_q: "queue.Queue[str]" = queue.Queue()


def new_task(agent: str, brief: str, context_id: str | None = None) -> dict:
    tid = str(uuid.uuid4())
    # One id, several systems: the contextId is the A2A context, the graph
    # thread, and any external join key. Minted exactly once, here.
    ctx = context_id or str(uuid.uuid4())
    task = {
        "id": tid,
        "agent": agent,
        "brief": brief,
        "contextId": ctx,
        "status": {"state": "submitted"},
        "done": threading.Event(),
        "proc": None,
        "cancelled": False,
    }
    with tasks_lock:
        if len(tasks) >= MAX_TASKS:
            tasks.pop(next(iter(tasks)), None)
        tasks[tid] = task
    return task


def run_task(task: dict, runner=None):
    task["status"] = {"state": "working"}
    cmd = [OPENCODE, "run", "--standalone", "--agent", task["agent"],
           "--model", TEAM_MODEL, task["brief"]]
    try:
        if runner is not None:
            out = runner(task["agent"], task["contextId"], task["brief"])
        else:
            proc = subprocess.Popen(cmd, cwd=str(REPO_DIR),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            task["proc"] = proc
            out, err = proc.communicate(timeout=TASK_TIMEOUT)
            out = (out or "") + (("\n[stderr]\n" + err) if err else "")
            if proc.returncode != 0:
                out += "\n[exit %d]" % proc.returncode
        if task.get("cancelled"):
            task["status"] = {"state": "canceled",
                              "message": {"role": "agent",
                                          "parts": [{"text": "canceled by request"}]}}
        elif out and out.endswith("]"):
            # An injected runner that appended an exit marker is a failure.
            task["status"] = {"state": "failed",
                              "message": {"role": "agent",
                                          "parts": [{"text": out[-2000:]}]}}
        else:
            task["status"] = {"state": "completed",
                              "message": {"role": "agent",
                                          "parts": [{"text": out[:200000]}]}}
    except subprocess.TimeoutExpired:
        task["status"] = {"state": "failed",
                          "message": {"role": "agent",
                                      "parts": [{"text": "timeout after %ss" % TASK_TIMEOUT}]}}
    finally:
        task["done"].set()


def worker(runner=None, q=None):
    q = q or work_q
    while True:
        tid = q.get()
        with tasks_lock:
            task = tasks.get(tid)
        if task is None:
            continue
        run_task(task, runner)


def parse_brief(message: dict) -> tuple[str, str, str | None]:
    """Return (agent, text, context_id)."""
    parts = message.get("parts", [])
    text = "\n".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()
    agent = "robotnik"
    m = re.match(r"@([a-z]+)\s*(.*)", text, re.S)
    if m:
        agent = m.group(1)
        text = (m.group(2) or "").strip() or text
    roster = load_roster()
    if agent not in roster:
        agent = "robotnik"
    ctx = None
    if isinstance(message.get("contextId"), str) and message["contextId"]:
        ctx = message["contextId"]
    return agent, text, ctx


def task_view(task: dict) -> dict:
    return {
        "id": task["id"],
        "contextId": task["contextId"],
        "status": task["status"],
    }


class Handler(BaseHTTPRequestHandler):
    runner = None  # set by main(); None means the real opencode runner

    def log_message(self, *a):
        pass

    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/.well-known/agent.json":
            self._send(200, agent_card())
        elif self.path == "/health":
            self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path not in ("/", "/a2a"):
            self._send(404, {"error": "not found"})
            return
        n = int(self.headers.get("Content-Length", 0) or 0)
        try:
            req = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            self._send(200, {"jsonrpc": "2.0", "id": None,
                             "error": {"code": -32700, "message": "parse error"}})
            return
        rid = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        def ok(result):
            self._send(200, {"jsonrpc": "2.0", "id": rid, "result": result})

        def err(code, message):
            self._send(200, {"jsonrpc": "2.0", "id": rid,
                             "error": {"code": code, "message": message}})

        def _queue(task):
            # The queue belongs to the server instance, so a test server
            # and the real one never share work items.
            q = getattr(self.server, "queue", None) or work_q
            q.put(task["id"])

        if method == "message/send":
            agent, text, ctx = parse_brief(params.get("message", {}))
            if not text:
                return err(-32602, "empty message")
            task = new_task(agent, text, ctx)
            _queue(task)
            ok({"task": task_view(task)})
        elif method == "message/stream":
            agent, text, ctx = parse_brief(params.get("message", {}))
            if not text:
                return err(-32602, "empty message")
            task = new_task(agent, text, ctx)
            _queue(task)
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()

            def ev(view):
                payload = {"jsonrpc": "2.0", "id": rid, "result": {"task": view}}
                self.wfile.write(("event: message\n"
                                  "data: " + json.dumps(payload) + "\n\n").encode())
                self.wfile.flush()

            ev(task_view(task))
            task["done"].wait(timeout=TASK_TIMEOUT + 60)
            ev(task_view(task))
        elif method == "tasks/get":
            tid = params.get("id")
            with tasks_lock:
                task = tasks.get(tid)
            if task is None:
                return err(-32602, "unknown task")
            ok({"task": task_view(task)})
        elif method == "tasks/cancel":
            tid = params.get("id")
            with tasks_lock:
                task = tasks.get(tid)
            if task is None:
                return err(-32602, "unknown task")
            task["cancelled"] = True
            proc = task.get("proc")
            if proc is not None and proc.poll() is None:
                proc.terminate()
            ok({"task": task_view(task)})
        else:
            err(-32601, "method not found: %s" % method)


def start(host: str = "127.0.0.1", port: int | None = None, runner=None):
    """Start the server in the current process and return ``(port, server)``.

    Used by tests and by ``gateway.sh selftest``. ``main`` serves forever;
    this returns so a test can drive the server in a thread. ``port=None``
    uses the adapter port; ``port=0`` asks the OS for an ephemeral port
    (tests must not touch the real adapter port). The caller shuts the
    server down when done.
    """
    Handler.runner = runner
    server = ThreadingHTTPServer((host, port if port is not None else PORT), Handler)
    server.queue = queue.Queue()
    threading.Thread(target=server.serve_forever, daemon=True).start()
    threading.Thread(target=worker, args=(runner, server.queue), daemon=True).start()
    return server.server_address[1], server


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=worker, daemon=True).start()
    server.serve_forever()


if __name__ == "__main__":
    main()
