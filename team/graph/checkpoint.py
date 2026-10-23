"""Checkpointing for the cycle graph.

One thread id, one run. The thread id is the A2A context id, so the A2A task
record, the graph checkpoint, and any external trace that names the context
id all refer to the same run.

Default behaviour:

- ``TEAM_RUNS_DIR`` set (or the repo's ``.runs/`` directory) gives a
  durable SQLite checkpoint database, one row set per thread id. ``.runs/``
  is gitignored: checkpoints are machine-local evidence, never committed.
- Otherwise an in-memory checkpointer, so importing and testing the graph
  never creates a file.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from langgraph.checkpoint.memory import MemorySaver


def runs_dir() -> Path:
    """Where durable run state lives. Machine-local, never committed."""
    env = os.environ.get("TEAM_RUNS_DIR")
    if env:
        return Path(env)
    return Path(os.environ.get("TEAM_DIR", ".")).resolve() / ".runs"


def sqlite_checkpointer(db_path: str | Path | None = None):
    """A SQLite-backed checkpointer (durable across processes)."""
    from langgraph.checkpoint.sqlite import SqliteSaver

    db_path = Path(db_path) if db_path else runs_dir() / "cycle.sqlite3"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    saver = SqliteSaver(conn)
    saver.setup()
    return saver


def default_checkpointer():
    """Durable when a runs dir is available, in-memory otherwise.

    An empty ``.runs/`` is created lazily by the SQLite saver, so the
    default is always durable when run from a checkout; tests that want
    in-memory behaviour pass a ``MemorySaver`` explicitly.
    """
    return sqlite_checkpointer()
