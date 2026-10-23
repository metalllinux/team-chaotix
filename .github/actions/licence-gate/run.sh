#!/usr/bin/env bash
# licence-gate run.sh: run the scanner on the given path, JSON report.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PATH_ARG="${1:-${ROOT}}"

# --json goes through so CI can parse the report; the exit code is what
# the action captures.
exec python3 "${ROOT}/team/licenses/core.py" "${PATH_ARG}" --json
