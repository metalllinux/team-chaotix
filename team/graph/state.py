"""State types for the Team Chaotix cycle graph.

The state is the shared record one run moves through. ``messages`` uses
langchain-core message types so the inter-agent log has a durable, typed
shape; the rest is plain JSON so checkpoints can be stored and read back
without a live model.

The team deliberately has no turn caps: nothing in this state is a max-turns
counter. ``max_revisions`` bounds how many times the review chain may send the
work back to ``fix``; it is a loop guard against a review that can never be
satisfied, not a budget on agent turns.
"""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph.message import add_messages

#: Stages in dispatch order. The review stages run as a fixed chain; the
#: router after the last review stage either sends the work back through
#: ``fix`` or lets it continue to ``docs``.
STAGES: tuple[str, ...] = (
    "intake",
    "plan",
    "implement",
    "review_shadow",
    "review_omega",
    "review_big",
    "review_charmy",
    "review_flicky",
    "docs",
    "release",
    "archive",
)

#: Review stages, in chain order. Each maps to exactly one reviewer agent.
REVIEW_STAGES: tuple[str, ...] = (
    "review_shadow",
    "review_omega",
    "review_big",
    "review_charmy",
    "review_flicky",
)

#: The agent that owns each stage. ``fix`` is owned by the implementer.
STAGE_AGENT: dict[str, str] = {
    "intake": "sonic",
    "plan": "amy",
    "implement": "tails",
    "review_shadow": "shadow",
    "review_omega": "omega",
    "review_big": "big",
    "review_charmy": "charmy",
    "review_flicky": "flicky",
    "fix": "tails",
    "docs": "vector",
    "release": "knuckles",
    "archive": "espio",
}

#: Verdict a review stage may record. ``fail`` is also the default when a
#: review output carries no readable verdict line: a review that cannot be
#: read cannot be trusted (fail-closed).
VERDICT_PASS = "pass"
VERDICT_FAIL = "fail"


class CycleState(TypedDict, total=False):
    """One run of the team cycle, keyed by its A2A context id (thread id)."""

    task_id: str
    doc_path: str
    stage: str
    stage_history: list[str]
    attempts: int
    max_revisions: int
    verdicts: dict[str, str]
    # The reducer lives in the schema (langgraph reads it from the
    # annotation): every stage's message is appended to the log, never
    # replaced.
    messages: Annotated[list[BaseMessage], add_messages]
    result: str
    halted: bool


def initial_state(
    task_id: str,
    doc_path: str,
    max_revisions: int = 3,
) -> CycleState:
    """A fresh run. The task brief is the first message, so the graph state
    always starts with something an audit can read."""
    return {
        "task_id": task_id,
        "doc_path": doc_path,
        "stage": "",
        "stage_history": [],
        "attempts": 0,
        "max_revisions": max_revisions,
        "verdicts": {},
        "messages": [
            HumanMessage(
                content=(
                    f"Task {task_id}: work the planning doc at {doc_path}. "
                    "The doc is the bus; write findings into your own section."
                )
            )
        ],
        "result": "",
        "halted": False,
    }


def record_verdict(state: CycleState, stage: str, output: str) -> str:
    """Extract the machine-readable verdict from a review stage's output.

    Contract: a review agent ends its section with a line
    ``VERDICT: PASS`` or ``VERDICT: FAIL <reason>``. Anything else is
    fail-closed, because an unreadable review is a review that did not happen.
    """
    text = (output or "").strip()
    verdict = VERDICT_FAIL
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.upper().startswith("VERDICT:"):
            verdict = (
                VERDICT_PASS
                if line.split(":", 1)[1].strip().upper().startswith("PASS")
                else VERDICT_FAIL
            )
            break
    verdicts = dict(state.get("verdicts", {}))
    verdicts[STAGE_AGENT[stage]] = verdict
    return verdicts


def ai_note(agent: str, stage: str, output: str) -> AIMessage:
    """Wrap an agent's output in an AIMessage so the inter-agent log is
    inspectable with langchain-core message tooling."""
    return AIMessage(content=f"[{agent} @ {stage}] {output}")
