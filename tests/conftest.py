"""Test setup: put the repo root on sys.path so ``team`` imports work.

``TEAM_DIR`` is set before the ``team`` package is imported so that the
A2A server resolves the roster from *this* checkout (the worktree under
test), not from whatever checkout happens to be the default.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("TEAM_DIR", str(ROOT))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
