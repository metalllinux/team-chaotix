#!/usr/bin/env python3
"""Entry point for the Team Chaotix A2A server.

The implementation moved to ``team/a2a/server.py`` (and is tested from
there). This file stays as the service entry point so the existing
``team-chaotix-a2a`` service definition keeps working unchanged.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from team.a2a import server  # noqa: E402

if __name__ == "__main__":
    # Keep the historical behaviour: serve forever on the adapter port.
    server.main()
