#!/usr/bin/env bash
# selftest -- the team's local and CI test entry point.
#
# Everything here is deterministic: no model is invoked, nothing is pushed,
# nothing outside the checkout is touched (pytest uses temp dirs). Run it
# locally before pushing; CI runs the same script.
#
# Exit non-zero on the first failure. Prints a check count on success;
# the CI workflow asserts a minimum so a suite that stopped asserting
# cannot read as green.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
CHECKS=0
PASS() { CHECKS=$((CHECKS+1)); }

note() { printf 'selftest: %s\n' "$*"; }
fail() { printf 'selftest FAIL: %s\n' "$*" >&2; exit 1; }

# --- syntax gates (by shebang, not by extension) -------------------------
for f in $(find scripts team tests -type f | sort); do
  first="$(head -1 "$f")"
  case "$first" in
    *"/bin/bash"*)
      bash -n "$f" || fail "bash syntax: $f"
      PASS
      ;;
    *"/usr/bin/env python3"*)
      python3 -m py_compile "$f" || fail "python syntax: $f"
      PASS
      ;;
  esac
done
note "bash + python syntax OK"

# --- shellcheck (warn-only when absent; the runner may not have it) ------
if command -v shellcheck >/dev/null 2>&1; then
  for f in $(find scripts team tests -type f | sort); do
    case "$(head -1 "$f")" in
      *"/bin/bash"*)
        shellcheck -S warning "$f" || fail "shellcheck: $f"
        PASS
        ;;
    esac
  done
  note "shellcheck OK"
else
  note "shellcheck absent, skipped"
fi

# --- YAML parse -----------------------------------------------------------
for f in $(find team .github planning \( -name "*.yml" -o -name "*.yaml" \) -not -path "*/node_modules/*" | sort) team/gateway/agentgateway.yaml.template; do
  python3 -c "import yaml,sys; yaml.safe_load(open('$f'))" || fail "yaml: $f"
  PASS
done
note "yaml OK"

# --- JSON parse -----------------------------------------------------------
for f in $(find team .github -name "*.json" -not -path "*/node_modules/*" | sort); do
  python3 -m json.tool "$f" > /dev/null || fail "json: $f"
  PASS
done
note "json OK"

# --- the no-turn-caps rule ------------------------------------------------
# The operator's standing requirement: the max-turns key does not exist on
# this team. If the string shows up in tracked source, that is a
# regression. The pattern is written [m]axTurns so this file does not
# match itself, and the gate files build the key by concatenation.
if grep -rIl "[m]axTurns\|[m]ax_turns" team scripts tests .github AGENTS.md \
    .opencode/agents planning/templates 2>/dev/null; then
  fail "turn caps found in team source (no-turn-caps rule)"
fi
PASS
note "no turn caps OK"

# --- agent configuration gate ----------------------------------------------
python3 tests/config_gate.py || fail "config gate"
PASS
note "config gate OK"

# --- the test suite --------------------------------------------------------
if command -v pytest >/dev/null 2>&1; then
  PYTEST="pytest"
else
  PYTEST="python3 -m pytest"
fi
note "pytest"
SUITE_OUT="$($PYTEST tests/ -q 2>&1)" || { printf '%s\n' "$SUITE_OUT"; fail "pytest"; }
TESTS=$(printf '%s\n' "$SUITE_OUT" | grep -Eo '[0-9]+ passed' | grep -Eo '^[0-9]+' | head -1 || true)
CHECKS=$((CHECKS + ${TESTS:-0}))
note "pytest OK (${TESTS:-?} tests)"

# --- licence gate on this repo ---------------------------------------------
# The repo itself must pass its own gate (Apache-2.0 root).
scripts/licence-check > /dev/null || fail "licence-check on this repo"
PASS
note "licence-check OK"

# --- gateway selftest (boot the real binary on ephemeral ports) ------------
# The template must not merely parse: the gateway has to boot with it.
# Skipped when the binary is absent (same rule as shellcheck above).
if [ -x "${AGENTGATEWAY_BIN:-/usr/local/bin/agentgateway}" ]; then
  GW_OUT="$(bash team/gateway/gateway.sh selftest 2>&1)" || { printf '%s\n' "$GW_OUT"; fail "gateway selftest"; }
  PASS
  note "gateway selftest OK"
else
  note "agentgateway binary absent, gateway selftest skipped"
fi

printf 'SELFTEST: %s checks passed\n' "${CHECKS}"
