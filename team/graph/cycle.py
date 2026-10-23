"""The Team Chaotix task cycle as a langgraph StateGraph.

This is the dispatch backbone for the team: one compiled graph models the
cycle in AGENTS.md,

    intake -> plan -> implement -> review chain (Shadow, Omega, Big,
    Charmy, Flicky) -> (fix loop) -> docs -> release -> archive

with the review chain running as a fixed sequential chain, exactly the way
the single inference slot requires.

The graph never talks to a model itself. A stage's ``runner`` callable
performs the work and returns the agent's output text. The default runner
is :class:`OpencodeRunner`, which invokes one ``opencode run --standalone``
session per stage; tests inject a fake runner, so the graph is fully
testable without a model (and so is CI).

There are deliberately no turn caps anywhere in this module.
``max_revisions`` limits how many times the review chain may bounce the work
back to ``fix``; hitting it halts the run with a recorded result instead of
looping forever. It bounds a cycle, not turns.
"""

from __future__ import annotations

import os
import subprocess
import uuid
from typing import Callable, Protocol

from langgraph.graph import END, START, StateGraph

from . import checkpoint as cp
from . import state as st
from .state import (
    CycleState,
    STAGE_AGENT,
    REVIEW_STAGES,
    initial_state,
)

CycleRunner = Callable[[str, str, str], str]


class AgentRunner(Protocol):
    """Performs one stage for one agent and returns the agent's output."""

    def __call__(self, agent: str, task_id: str, brief: str) -> str: ...


class OpencodeRunner:
    """Default runner: one ``opencode run --standalone`` session per stage.

    The repo directory is the working directory, because opencode resolves
    the team's agent configuration from it (AGENTS.md section 1). The team
    model is pinned explicitly for the same reason the A2A adapter pins it:
    a standalone run must not fall back to the first provider in the global
    config.
    """

    def __init__(
        self,
        repo_dir: str | None = None,
        opencode_bin: str | None = None,
        model: str | None = None,
        timeout: int = 7200,
    ) -> None:
        self.repo_dir = repo_dir or os.environ.get("TEAM_DIR", ".")
        self.opencode_bin = opencode_bin or os.environ.get("OPENCODE_BIN", "opencode")
        self.model = model or os.environ.get("A2A_MODEL", "")
        self.timeout = timeout

    def __call__(self, agent: str, task_id: str, brief: str) -> str:
        cmd = [self.opencode_bin, "run", "--standalone", "--agent", agent]
        if self.model:
            cmd += ["--model", self.model]
        cmd.append(brief)
        proc = subprocess.run(
            cmd,
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
        out = proc.stdout or ""
        if proc.stderr:
            out += "\n[stderr]\n" + proc.stderr
        if proc.returncode != 0:
            out += f"\n[exit {proc.returncode}]"
        return out


def _brief(state: CycleState, stage: str) -> str:
    """Keep briefs short and point at the planning doc; the doc carries the
    detail. This mirrors the PM's own dispatch discipline."""
    agent = STAGE_AGENT[stage]
    base = (
        f"Task {state.get('task_id', '?')}: stage {stage}. "
        f"Planning doc: {state.get('doc_path', 'planning/docs/')}. "
    )
    if stage in REVIEW_STAGES:
        base += (
            "Review the change from your angle only, write your section, "
            "and end with a line 'VERDICT: PASS' or 'VERDICT: FAIL <reason>'."
        )
    elif stage == "fix":
        base += (
            "Fix what the review chain wrote back. Re-read each reviewer's "
            "section before touching the work."
        )
    return base


def _node_factory(runner: CycleRunner):
    def make(stage: str):
        def node(state: CycleState) -> dict:
            agent = STAGE_AGENT[stage]
            brief = _brief(state, stage)
            output = runner(agent, state.get("task_id", "?"), brief)
            update: dict = {
                "stage": stage,
                "stage_history": state.get("stage_history", []) + [stage],
                "messages": [st.ai_note(agent, stage, output)],
            }
            if stage in REVIEW_STAGES:
                update["verdicts"] = st.record_verdict(state, stage, output)
            return update

        node.__name__ = stage
        return node

    return make


def _route_after_reviews(state: CycleState) -> str:
    """The only conditional edge in the graph.

    Any ``fail`` verdict in the current round sends the work through ``fix``
    and back to the head of the review chain. ``max_revisions`` is a loop
    guard, not a turn cap: when it is exhausted the run halts with a
    recorded result so a review that can never be satisfied is visible
    instead of silent.
    """
    verdicts = state.get("verdicts", {})
    failed = sorted(k for k, v in verdicts.items() if v == st.VERDICT_FAIL)
    if failed and state.get("attempts", 0) < state.get("max_revisions", 3):
        return "fix"
    if failed:
        return "halted"
    return "docs"


def _wire(runner: CycleRunner) -> "StateGraph":
    """Build the uncompiled graph. Single source of truth for the wiring."""
    make = _node_factory(runner)
    g: StateGraph = StateGraph(CycleState)

    linear = (
        "intake",
        "plan",
        "implement",
        *REVIEW_STAGES,
        "docs",
        "release",
        "archive",
    )
    for stage in linear:
        g.add_node(stage, make(stage))

    def fix_node(state: CycleState) -> dict:
        """Send the work back: bump the round counter, clear the round's
        verdicts (so the router after the re-review reads this round only),
        and run the implementer."""
        agent = STAGE_AGENT["fix"]
        brief = _brief(state, "fix")
        output = runner(agent, state.get("task_id", "?"), brief)
        return {
            "stage": "fix",
            "stage_history": state.get("stage_history", []) + ["fix"],
            "attempts": state.get("attempts", 0) + 1,
            "verdicts": {},
            "messages": [st.ai_note(agent, "fix", output)],
        }

    def halt_node(state: CycleState) -> dict:
        verdicts = state.get("verdicts", {})
        failed = sorted(k for k, v in verdicts.items() if v == st.VERDICT_FAIL)
        return {
            "halted": True,
            "stage": "halted",
            "stage_history": state.get("stage_history", []) + ["halted"],
            "result": (
                f"halted: review chain still failing after "
                f"{state.get('attempts', 0)} revisions "
                f"(failures: {', '.join(failed)}). "
                "Escalate in the planning doc's ## Status."
            ),
        }

    g.add_node("fix", fix_node)
    g.add_node("halted", halt_node)

    g.add_edge(START, "intake")
    for a, b in zip(linear, linear[1:]):
        if a == REVIEW_STAGES[-1]:
            continue  # the router owns the edge after the last review stage
        g.add_edge(a, b)

    # fix loops back to the head of the review chain.
    g.add_edge("fix", REVIEW_STAGES[0])

    g.add_conditional_edges(REVIEW_STAGES[-1], _route_after_reviews, {
        "fix": "fix",
        "halted": "halted",
        "docs": "docs",
    })
    g.add_edge("docs", "release")
    g.add_edge("release", "archive")
    g.add_edge("archive", END)
    g.add_edge("halted", END)
    return g


def build_cycle_graph(
    runner: CycleRunner | None = None,
    checkpointer=None,
):
    """Compile the cycle graph.

    ``runner`` defaults to :class:`OpencodeRunner`. Pass a checkpointer (see
    :mod:`team.graph.checkpoint`) to make runs durable; the thread id is the
    A2A context id, which is why the id is minted in exactly one place.
    """
    runner = runner or OpencodeRunner()
    return _wire(runner).compile(checkpointer=checkpointer)


def run_cycle(
    task_id: str,
    doc_path: str,
    runner: CycleRunner | None = None,
    thread_id: str | None = None,
    checkpointer=None,
    max_revisions: int = 3,
) -> CycleState:
    """Run one cycle to completion and return the final state.

    ``thread_id`` is the A2A context id; pass ``None`` to mint one. With a
    checkpointer, intermediate checkpoints are stored under that thread id,
    so a run can be inspected or resumed after the process that ran it is
    gone.
    """
    thread_id = thread_id or str(uuid.uuid4())
    if checkpointer is None:
        checkpointer = cp.default_checkpointer()
    graph = build_cycle_graph(runner, checkpointer=checkpointer)
    config = {"configurable": {"thread_id": thread_id}}
    state = initial_state(task_id, doc_path, max_revisions=max_revisions)
    return graph.invoke(state, config)
