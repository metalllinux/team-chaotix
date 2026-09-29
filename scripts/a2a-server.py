#!/usr/bin/env python3
"""Team Chaotix A2A adapter (AGENTS.md section 15).

Exposes the team's opencode agents as an A2A agent, fronted by agentgateway
(port 4100; this process listens on 127.0.0.1:4210).

Surface
  GET  /.well-known/agent.json   agent card (capability discovery)
  GET  /health                  liveness
  POST /                        JSON-RPC 2.0: message/send, message/stream, tasks/get

Task addressing: the first token of the task text is @<agent> (a roster agent
file name; default @robotnik). The remainder is the task brief. A task runs
`opencode run --standalone --agent <role> <brief>` in the team repo, queued
one at a time (single inference slot). The final task's
status.message.parts[0].text is the agent's output.

State is in-memory; the durable record of a task is the planning doc it
writes.
"""
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
AGENTS_DIR = REPO_DIR / ".opencode" / "agents"
OPENCODE = os.environ.get("OPENCODE_BIN", "/home/howard/.opencode/bin/opencode")
PORT = int(os.environ.get("A2A_PORT", "4210"))
PUBLIC_URL = os.environ.get("A2A_PUBLIC_URL", "http://127.0.0.1:4100/")
# opencode run ignores the agent frontmatter model and falls back to the first
# provider in the global config, so pin the team model explicitly.
TEAM_MODEL = os.environ.get("A2A_MODEL", "evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS")
TASK_TIMEOUT = int(os.environ.get("A2A_TASK_TIMEOUT", "7200"))
MAX_TASKS = 64

# (agent file name, card label)
ROSTER = [
    ("robotnik", "Project management (delegator; default target)"),
    ("amy", "Task planning"),
    ("tails", "Coding and implementation"),
    ("shadow", "Code review"),
    ("omega", "Security review"),
    ("big", "Testing"),
    ("charmy", "License compliance"),
    ("vector", "Documentation"),
    ("sonic", "Triage"),
    ("knuckles", "Release management"),
    ("espio", "Context curation"),
]
ROSTER_NAMES = {name for name, _ in ROSTER}

tasks = {}
tasks_lock = threading.Lock()
work_q = queue.Queue()


def agent_description(name):
    p = AGENTS_DIR / (name + ".md")
    try:
        for line in p.read_text().splitlines():
            if line.startswith("description:"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return ""


def agent_card():
    skills = []
    for name, label in ROSTER:
        skills.append({
            "id": name,
            "name": "%s — %s" % (name, label),
            "description": agent_description(name),
            "tags": [name, "team-chaotix"],
        })
    return {
        "name": "team-chaotix",
        "description": (
            "Team Chaotix: an 11-role autonomous software development team built on "
            "opencode. Each skill is a team role. Address a task with a leading "
            "@<role> token (default @robotnik); the rest of the text is the task "
            "brief. The final task's status.message.parts[0].text is the agent's "
            "output."
        ),
        "url": PUBLIC_URL,
        "version": "1.0.0",
        "capabilities": {"streaming": True, "pushNotifications": False},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": skills,
    }


def new_task(agent, brief):
    tid = str(uuid.uuid4())
    task = {
        "id": tid,
        "agent": agent,
        "brief": brief,
        "status": {"state": "submitted"},
        "done": threading.Event(),
    }
    with tasks_lock:
        if len(tasks) >= MAX_TASKS:
            tasks.pop(next(iter(tasks)), None)
        tasks[tid] = task
    return task


def run_task(task):
    task["status"] = {"state": "working"}
    cmd = [OPENCODE, "run", "--standalone", "--agent", task["agent"],
           "--model", TEAM_MODEL, task["brief"]]
    try:
        proc = subprocess.run(cmd, cwd=str(REPO_DIR), capture_output=True,
                              text=True, timeout=TASK_TIMEOUT)
        out = proc.stdout or ""
        if proc.stderr:
            out += "\n[stderr]\n" + proc.stderr
        if proc.returncode == 0:
            task["status"] = {"state": "completed",
                              "message": {"role": "agent",
                                          "parts": [{"text": out[:200000]}]}}
        else:
            tail = out[-2000:]
            task["status"] = {"state": "failed",
                              "message": {"role": "agent",
                                          "parts": [{"text": "exit %d: %s" % (proc.returncode, tail)}]}}
    except subprocess.TimeoutExpired:
        task["status"] = {"state": "failed",
                          "message": {"role": "agent",
                                      "parts": [{"text": "timeout after %ss" % TASK_TIMEOUT}]}}
    finally:
        task["done"].set()


def worker():
    while True:
        tid = work_q.get()
        with tasks_lock:
            task = tasks.get(tid)
        if task is None:
            continue
        run_task(task)


threading.Thread(target=worker, daemon=True).start()


def parse_brief(message):
    parts = message.get("parts", [])
    text = "\n".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()
    agent = "robotnik"
    m = re.match(r"@([a-z]+)\s*(.*)", text, re.S)
    if m:
        agent = m.group(1)
        text = (m.group(2) or "").strip() or text
    if agent not in ROSTER_NAMES:
        agent = "robotnik"
    return agent, text


def task_view(task):
    return {"id": task["id"], "status": task["status"]}


class Handler(BaseHTTPRequestHandler):
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

        if method == "message/send":
            agent, text = parse_brief(params.get("message", {}))
            if not text:
                return err(-32602, "empty message")
            task = new_task(agent, text)
            work_q.put(task["id"])
            ok({"task": task_view(task)})
        elif method == "tasks/get":
            tid = params.get("id")
            with tasks_lock:
                task = tasks.get(tid)
            if task is None:
                return err(-32602, "unknown task")
            ok({"task": task_view(task)})
        elif method == "message/stream":
            agent, text = parse_brief(params.get("message", {}))
            if not text:
                return err(-32602, "empty message")
            task = new_task(agent, text)
            work_q.put(task["id"])
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
        else:
            err(-32601, "method not found: %s" % method)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
