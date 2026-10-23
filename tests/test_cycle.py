"""Tests for the cycle graph (team/graph).

No model is invoked: a fake runner performs the stages. These tests are
what CI runs, so the graph's behaviour is pinned without a single LLM call.
"""

from __future__ import annotations

import os

import pytest

from team.graph import cycle, state as st
from team.graph.cycle import run_cycle


class FakeRunner:
    """Performs stages by returning canned text, optionally failing the
    first N review rounds for one (or all) reviewers."""

    def __init__(self, fail_rounds: int = 0, fail_agents: set | None = None):
        self.fail_rounds = fail_rounds
        self.fail_agents = fail_agents or set()
        self.calls: list[tuple[str, str]] = []
        self.round = 0

    def __call__(self, agent: str, task_id: str, brief: str) -> str:
        self.calls.append((agent, brief))
        out = f"[{agent}] stage done"
        if agent in ("shadow", "omega", "big", "charmy", "flicky"):
            # Reviewers always end with an explicit verdict; a clean round
            # is a PASS, not silence (silence is fail-closed by design).
            if self.round < self.fail_rounds and (
                not self.fail_agents or agent in self.fail_agents
            ):
                out += "\nVERDICT: FAIL planted finding for the test"
            else:
                out += "\nVERDICT: PASS"
        return out


def make_runner(fail_rounds: int = 0, fail_agents: set | None = None):
    """Wrap a FakeRunner so that review rounds are counted. A round ends
    when ``fix`` runs, so the round number is incremented on the fix brief
    (the implement stage shares the ``tails`` agent but not the brief)."""
    base = FakeRunner(fail_rounds, fail_agents)
    original = base.__call__

    def wrapped(agent: str, task_id: str, brief: str) -> str:
        if "stage fix" in brief:
            base.round += 1
        return original(agent, task_id, brief)

    return wrapped, base


def test_cycle_runs_start_to_archive_with_clean_reviews(tmp_path, monkeypatch):
    monkeypatch.setenv("TEAM_RUNS_DIR", str(tmp_path))
    runner, _ = make_runner(fail_rounds=0)
    final = run_cycle(
        "TASK-0037",
        "planning/docs/TASK-0037-team-platform.md",
        runner=runner,
        thread_id="ctx-test-clean",
    )
    assert final["stage"] == "archive"
    assert final["halted"] is False
    assert final["attempts"] == 0
    # The whole cycle, in order, no revisits.
    assert final["stage_history"] == [
        "intake", "plan", "implement",
        "review_shadow", "review_omega", "review_big", "review_charmy",
        "review_flicky", "docs", "release", "archive",
    ]
    # langchain-core messages: the first message is the task brief, and
    # every stage left an AIMessage in the log.
    from langchain_core.messages import AIMessage, HumanMessage

    msgs = final["messages"]
    assert isinstance(msgs[0], HumanMessage)
    assert "TASK-0037" in msgs[0].content
    assert sum(isinstance(m, AIMessage) for m in msgs) == len(final["stage_history"])


def test_cycle_fixes_and_recovers(tmp_path, monkeypatch):
    monkeypatch.setenv("TEAM_RUNS_DIR", str(tmp_path))
    # One reviewer fails in round 1, passes in round 2.
    runner, _ = make_runner(fail_rounds=1, fail_agents={"omega"})
    final = run_cycle("TASK-0038", "planning/docs/TASK-0038-x.md",
                     runner=runner, thread_id="ctx-test-recover")
    assert final["stage"] == "archive"
    assert final["attempts"] == 1
    assert final["stage_history"].count("fix") == 1
    # The review chain ran twice; the work was implemented, then re-reviewed.
    assert final["stage_history"].count("implement") == 1
    assert final["stage_history"].count("review_omega") == 2


def test_cycle_halts_when_reviews_never_pass(tmp_path, monkeypatch):
    monkeypatch.setenv("TEAM_RUNS_DIR", str(tmp_path))
    runner, _ = make_runner(fail_rounds=10, fail_agents={"shadow"})
    final = run_cycle("TASK-0039", "planning/docs/TASK-0039-x.md",
                     runner=runner, thread_id="ctx-test-halt",
                     max_revisions=2)
    assert final["halted"] is True
    assert final["stage"] == "halted"
    assert final["attempts"] == 2
    assert "shadow" in final["result"]
    # And it stopped instead of looping: no stage after the halt.
    assert final["stage_history"][-1] == "halted"


def test_no_turn_cap_anywhere_in_state():
    # The user's requirement, pinned by a test: no max-turns field exists in
    # the cycle state. max_revisions is a loop guard, named as such.
    state = st.initial_state("TASK-X", "doc")
    # Built by concatenation so the gate's own source never carries the key.
    assert "max" "Turns" not in state
    assert "max_" "turns" not in state
    assert "steps" not in state
    assert state["max_revisions"] == 3


def test_verdict_parsing():
    s = st.initial_state("T", "d")
    v = st.record_verdict(s, "review_shadow", "findings...\nVERDICT: PASS")
    assert v["shadow"] == st.VERDICT_PASS
    v = st.record_verdict(s, "review_shadow", "VERDICT: FAIL missing edge case")
    assert v["shadow"] == st.VERDICT_FAIL
    # No verdict line is fail-closed.
    v = st.record_verdict(s, "review_shadow", "I looked at it, seems fine.")
    assert v["shadow"] == st.VERDICT_FAIL


def test_checkpoint_persists_under_thread_id(tmp_path, monkeypatch):
    monkeypatch.setenv("TEAM_RUNS_DIR", str(tmp_path))
    runner, _ = make_runner(fail_rounds=0)
    from team.graph import checkpoint as cp

    graph = cycle.build_cycle_graph(runner,
                                   checkpointer=cp.sqlite_checkpointer(tmp_path / "c.sqlite3"))
    config = {"configurable": {"thread_id": "ctx-persist"}}
    final = graph.invoke(
        st.initial_state("TASK-0040", "planning/docs/TASK-0040-x.md"), config
    )
    assert final["stage"] == "archive"
    # Read the checkpoint back out of the database, as a fresh process would.
    saved = graph.get_state(config)
    assert saved.values["stage"] == "archive"
    assert saved.values["task_id"] == "TASK-0040"
