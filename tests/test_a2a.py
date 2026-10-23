"""Tests for the A2A server and client (team/a2a).

The server is driven in-process with an injected runner, so no opencode
session and no model is involved. The agent card is checked against the
real roster files in ``.opencode/agents/``.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.request

import pytest

from team.a2a import client as client_mod
from team.a2a import server as srv


@pytest.fixture()
def live_server(tmp_path, monkeypatch):
    """Start the A2A server on an ephemeral port with a fake runner."""
    monkeypatch.setenv("TEAM_RUNS_DIR", str(tmp_path))

    calls: list[tuple[str, str]] = []

    def fake_runner(agent: str, context_id: str, brief: str) -> str:
        calls.append((agent, brief))
        return f"[{agent}] done with: {brief[:40]}\nVERDICT: PASS"

    port, httpd = srv.start(port=0, runner=fake_runner)
    base = f"http://127.0.0.1:{port}"
    yield base, calls
    httpd.shutdown()
    srv.Handler.runner = None


def _post(base, method, params, rpc_id=1):
    body = json.dumps({"jsonrpc": "2.0", "id": rpc_id,
                       "method": method, "params": params}).encode()
    req = urllib.request.Request(base + "/", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read() or b"{}")


def _get(base, path):
    with urllib.request.urlopen(base + path, timeout=15) as resp:
        return json.loads(resp.read() or b"{}")


def _wait_task(base, tid, deadline=20.0):
    start = time.monotonic()
    while time.monotonic() - start < deadline:
        res = _post(base, "tasks/get", {"id": tid}, rpc_id=99)
        task = res.get("result", {}).get("task", {})
        if task.get("status", {}).get("state") in ("completed", "failed", "canceled"):
            return task
        time.sleep(0.1)
    raise AssertionError(f"task {tid} did not finish in time")


def test_agent_card_matches_roster_files(live_server):
    base, _ = live_server
    card = _get(base, "/.well-known/agent.json")
    assert card["name"] == srv.TEAM_NAME
    skill_ids = {s["id"] for s in card["skills"]}
    # Every roster agent file is advertised, including the new licence
    # agent and the delegator.
    assert "flicky" in skill_ids
    assert "robotnik" in skill_ids
    assert "tails" in skill_ids
    # The card carries the protocol version and the team version.
    assert card["protocolVersion"] == srv.PROTOCOL_VERSION
    assert card["version"] == srv.TEAM_VERSION


def test_health(live_server):
    base, _ = live_server
    assert _get(base, "/health") == {"ok": True}


def test_message_send_and_get_with_context_id(live_server):
    base, calls = live_server
    res = _post(base, "message/send",
                {"message": {"parts": [{"text": "@shadow review the gate"}],
                             "contextId": "ctx-a2a-test-1"}})
    task = res["result"]["task"]
    assert task["contextId"] == "ctx-a2a-test-1"
    final = _wait_task(base, task["id"])
    assert final["status"]["state"] == "completed"
    text = final["status"]["message"]["parts"][0]["text"]
    assert "shadow" in text
    # The fake runner was addressed with the parsed agent, not the raw text.
    assert calls and calls[0][0] == "shadow"


def test_unknown_agent_falls_back_to_robotnik(live_server):
    base, calls = live_server
    res = _post(base, "message/send",
                {"message": {"parts": [{"text": "@nobody here please"}]}})
    task = res["result"]["task"]
    _wait_task(base, task["id"])
    assert calls[0][0] == "robotnik"


def test_missing_context_id_is_minted(live_server):
    base, _ = live_server
    res = _post(base, "message/send",
                {"message": {"parts": [{"text": "@tails do the thing"}]}})
    task = res["result"]["task"]
    assert task["contextId"]  # non-empty
    assert len(task["contextId"]) >= 8


def test_client_roundtrip(live_server):
    base, _ = live_server
    c = client_mod.A2AClient(base)
    assert c.health() is True
    card = c.agent_card()
    assert card["name"] == srv.TEAM_NAME
    task = c.send("charmy", "check the licence")
    final = c.wait(task["id"], poll=0.1, deadline=20)
    assert final["status"]["state"] == "completed"


def test_tasks_cancel_unknown_is_error(live_server):
    base, _ = live_server
    res = _post(base, "tasks/cancel", {"id": "no-such-task"}, rpc_id=7)
    assert "error" in res
    assert res["error"]["code"] == -32602
