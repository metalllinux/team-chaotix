"""Tests for the licence scanner and policy engine (team/licenses).

Fixtures build tiny throwaway repos under tmp_path; nothing here touches
the team repo's own files.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from team.licenses import core

REPO_ROOT = Path(__file__).resolve().parent.parent


def _write(repo: Path, name: str, text: str):
    p = repo / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


MIT = """MIT License

Copyright (c) 2026 Test

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software ...
"""

APACHE = """Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
"""

GPL3 = """GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

This program is free software: you can redistribute it and/or modify it
"""

BUSL = """Business Source License 1.1

The Business Source License, it is a source-available licence ...
"""

SPDX_PY = """# SPDX-License-Identifier: MIT
def main():
    pass
"""


def test_mit_repo_passes(tmp_path):
    _write(tmp_path, "LICENSE", MIT)
    _write(tmp_path, "src/main.py", SPDX_PY)
    _write(tmp_path, "package.json", '{"name": "x", "license": "MIT"}')
    result = core.evaluate(tmp_path)
    assert result.outcome == core.OUTCOME_PASS
    kinds = {f.kind for f in result.findings}
    assert {"repo_license", "header", "package_meta"} <= kinds


def test_apache_root_with_notice_passes(tmp_path):
    _write(tmp_path, "LICENSE", APACHE)
    _write(tmp_path, "NOTICE", "Test Project (Apache-2.0)")
    result = core.evaluate(tmp_path)
    assert result.outcome == core.OUTCOME_PASS
    assert any(f.kind == "attribution" for f in result.findings)


def test_no_licence_is_hard_stop(tmp_path):
    _write(tmp_path, "main.py", "# nothing here\n")
    result = core.evaluate(tmp_path)
    assert result.outcome == core.OUTCOME_HARD_STOP
    assert core.EXIT_CODES[result.outcome] == 8


def test_gpl_root_is_policy_exception(tmp_path):
    _write(tmp_path, "COPYING", GPL3)
    result = core.evaluate(tmp_path)
    assert result.outcome == core.OUTCOME_EXCEPTION
    assert core.EXIT_CODES[result.outcome] == 6


def test_busl_dependency_is_block(tmp_path):
    _write(tmp_path, "LICENSE", MIT)
    _write(tmp_path, "package.json", '{"name": "x", "license": "BUSL-1.1"}')
    result = core.evaluate(tmp_path)
    assert result.outcome == core.OUTCOME_BLOCK
    assert core.EXIT_CODES[result.outcome] == 7


def test_sspl_dependency_is_block(tmp_path):
    _write(tmp_path, "LICENSE", MIT)
    _write(tmp_path, "Cargo.toml", '[package]\nlicense = "SSPL-1.0"\n')
    result = core.evaluate(tmp_path)
    assert result.outcome == core.OUTCOME_BLOCK


def test_copyleft_dep_under_permissive_root_is_exception(tmp_path):
    # A permissive root plus a GPL dependency is a licence change on the
    # combined work: record it, do not silently pass, do not block.
    _write(tmp_path, "LICENSE", MIT)
    _write(tmp_path, "src/dep.c", "/* SPDX-License-Identifier: GPL-3.0-only */\n")
    result = core.evaluate(tmp_path)
    assert result.outcome == core.OUTCOME_EXCEPTION


def test_cli_exit_codes(tmp_path):
    _write(tmp_path, "LICENSE", MIT)
    script = REPO_ROOT / "team" / "licenses" / "core.py"
    r = subprocess.run([sys.executable, str(script), str(tmp_path), "--json"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    import json
    report = json.loads(r.stdout)
    assert report["outcome"] == "PASS"
    assert report["exit"] == 0

    # A bare directory with no licence must exit 8.
    bare = tmp_path / "bare"
    bare.mkdir()
    r = subprocess.run([sys.executable, str(script), str(bare)],
                       capture_output=True, text=True)
    assert r.returncode == 8


def test_no_maxturns_in_scanner_or_policy(tmp_path):
    # The requirement is pinned here too: no turn caps anywhere in the
    # team's tooling text.
    policy = (REPO_ROOT / "team" / "licenses" / "policy.yaml").read_text()
    core_text = (REPO_ROOT / "team" / "licenses" / "core.py").read_text()
    for text in (policy, core_text):
        # Built by concatenation so the gate's own source never carries the key.
        assert "max" "Turns" not in text
        assert "max_" "turns" not in text
