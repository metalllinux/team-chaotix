"""A2A client for Team Chaotix.

Small stdlib-only client for the A2A surface. This is the agent-to-agent
side of the protocol inside one team instance and to other team instances
across the network: it sends a task to an agent card's endpoint and waits
for the final task status.

Usage (module):

    from team.a2a.client import A2AClient
    c = A2AClient("http://127.0.0.1:4100")
    task = c.send("shadow", "Review TASK-0037 in planning/docs/...")
    final = c.wait(task["id"])

Usage (CLI, via ``scripts/a2a-send``):

    a2a-send @shadow "Review TASK-0037 ..."
    a2a-send robotnik "Intake this issue"            # no leading @
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request


class A2AError(RuntimeError):
    pass


class A2AClient:
    def __init__(self, base_url: str | None = None, timeout: int = 30) -> None:
        # The gateway A2A port is the default address; point the client at
        # the adapter directly with A2A_DIRECT or an explicit base_url.
        self.base_url = (base_url
                         or os.environ.get("A2A_BASE_URL")
                         or os.environ.get("A2A_PUBLIC_URL")
                         or "http://127.0.0.1:4100").rstrip("/")
        self.timeout = timeout
        self._rpc_id = 0

    def _rpc(self, method: str, params: dict) -> dict:
        self._rpc_id += 1
        body = json.dumps({
            "jsonrpc": "2.0",
            "id": self._rpc_id,
            "method": method,
            "params": params,
        }).encode()
        req = urllib.request.Request(
            self.base_url + "/",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            raise A2AError("HTTP %s from %s" % (e.code, self.base_url)) from e
        if "error" in payload:
            raise A2AError("JSON-RPC error: %s" % payload["error"].get("message"))
        return payload.get("result", {})

    def agent_card(self) -> dict:
        req = urllib.request.Request(self.base_url + "/.well-known/agent.json")
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read() or b"{}")

    def health(self) -> bool:
        try:
            req = urllib.request.Request(self.base_url + "/health")
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read() or b"{}").get("ok") is True
        except (urllib.error.URLError, A2AError):
            return False

    def send(self, agent: str, brief: str, context_id: str | None = None) -> dict:
        """Send the task and return the task view (id, contextId, status)."""
        text = ("@%s %s" % (agent, brief)) if agent else brief
        message = {"parts": [{"text": text}]}
        if context_id:
            message["contextId"] = context_id
        return self._rpc("message/send", {"message": message}).get("task", {})

    def get(self, task_id: str) -> dict:
        return self._rpc("tasks/get", {"id": task_id}).get("task", {})

    def cancel(self, task_id: str) -> dict:
        return self._rpc("tasks/cancel", {"id": task_id}).get("task", {})

    def wait(
        self,
        task_id: str,
        poll: float = 2.0,
        deadline: float = 7200.0,
    ) -> dict:
        """Poll ``tasks/get`` until the task reaches a terminal state."""
        start = time.monotonic()
        terminal = {"completed", "failed", "canceled", "cancelled", "rejected"}
        while True:
            task = self.get(task_id)
            state = task.get("status", {}).get("state", "")
            if state in terminal:
                return task
            if time.monotonic() - start > deadline:
                raise A2AError("timed out waiting for task %s" % task_id)
            time.sleep(poll)


def main(argv: list[str] | None = None) -> int:
    import argparse

    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser(
        prog="a2a-send",
        description="Send one task to a Team Chaotix A2A endpoint and wait "
                    "for the final result.",
    )
    ap.add_argument("brief", nargs="*", help="task text; a leading @<agent> "
                  "token addresses a roster agent (default @robotnik)")
    ap.add_argument("--base-url", default=None, help="A2A endpoint base URL")
    ap.add_argument("--context-id", default=None, help="A2A contextId to use")
    ap.add_argument("--no-wait", action="store_true",
                    help="print the task id and exit without waiting")
    ap.add_argument("--deadline", type=float, default=7200.0)
    args = ap.parse_args(argv)

    if not args.brief:
        ap.error("empty brief")
    client = A2AClient(args.base_url)
    brief = " ".join(args.brief)
    if brief.startswith("@"):
        token, _, rest = brief.partition(" ")
        agent = token.lstrip("@")
        brief = rest.strip() or brief
    else:
        agent = "robotnik"
    task = client.send(agent, brief, args.context_id)
    tid = task.get("id", "")
    if args.no_wait:
        print(tid)
        return 0
    final = client.wait(tid, deadline=args.deadline)
    status = final.get("status", {})
    state = status.get("state", "unknown")
    text = ""
    msg = status.get("message")
    if isinstance(msg, dict):
        for part in msg.get("parts", []):
            if isinstance(part, dict) and "text" in part:
                text = part["text"]
                break
    print("state=%s contextId=%s" % (state, final.get("contextId", "")))
    if text:
        print(text)
    return 0 if state == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
