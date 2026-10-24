#!/usr/bin/env bash
# gateway.sh -- manage the team's agentgateway process.
#
#   gateway.sh apply [--config OUT]   render the template
#   gateway.sh up                    start the gateway (background, pidfile)
#   gateway.sh down                  stop it
#   gateway.sh status                process + endpoint liveness
#   gateway.sh selftest              boot on ephemeral ports, probe, stop
#
# The binary is installed at /usr/local/bin/agentgateway (see the README
# install section). Config state is machine-local under
# ~/.config/team-chaotix/ and ~/.local/state/team-chaotix/, never committed.
#
# Environment overrides (apply/selftest):
#   UPSTREAM_BASE_URL  (default http://192.168.1.106:8094/v1)
#   TEAM_MODEL         (default evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS)
#   LLM_PORT=4000  A2A_PORT=4100  ADAPTER_PORT=4210
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/../.." && pwd)"
TEMPLATE="${HERE}/agentgateway.yaml.template"
CONFIG_DIR="${HOME}/.config/team-chaotix"
CONFIG="${CONFIG_DIR}/agentgateway.yaml"
STATE_DIR="${HOME}/.local/state/team-chaotix/gateway"
PIDFILE="${STATE_DIR}/agentgateway.pid"
LOGFILE="${STATE_DIR}/agentgateway.log"
BIN="${AGENTGATEWAY_BIN:-/usr/local/bin/agentgateway}"

UPSTREAM_BASE_URL="${UPSTREAM_BASE_URL:-http://192.168.1.106:8094/v1}"
TEAM_MODEL="${TEAM_MODEL:-evo-x2-qwen3.8-iq3xxs/Qwen3.8-27B-UD-IQ3_XXS}"
LLM_PORT="${LLM_PORT:-4000}"
A2A_PORT="${A2A_PORT:-4100}"
ADAPTER_PORT="${ADAPTER_PORT:-4210}"

die() { printf 'gateway.sh: %s\n' "$*" >&2; exit 1; }

cmd_apply() {
  local out="${CONFIG}"
  if [ "$#" -gt 0 ]; then out="$2"; fi
  mkdir -p "$(dirname "${out}")"
  sed -e "s|__LLM_PORT__|${LLM_PORT}|" \
      -e "s|__A2A_PORT__|${A2A_PORT}|" \
      -e "s|__ADAPTER_PORT__|${ADAPTER_PORT}|" \
      -e "s|__UPSTREAM_BASE_URL__|${UPSTREAM_BASE_URL}|" \
      -e "s|__TEAM_MODEL__|${TEAM_MODEL}|" \
      "${TEMPLATE}" > "${out}"
  printf 'gateway.sh: config rendered to %s\n' "${out}"
}

cmd_up() {
  [ -x "${BIN}" ] || die "agentgateway binary not found at ${BIN}"
  [ -f "${CONFIG}" ] || cmd_apply
  mkdir -p "${STATE_DIR}"
  if [ -f "${PIDFILE}" ] && kill -0 "$(cat "${PIDFILE}")" 2>/dev/null; then
    printf 'gateway.sh: already running (pid %s)\n' "$(cat "${PIDFILE}")"
    return 0
  fi
  nohup "${BIN}" --file "${CONFIG}" > "${LOGFILE}" 2>&1 &
  echo $! > "${PIDFILE}"
  printf 'gateway.sh: agentgateway started (pid %s, log %s)\n' "$(cat "${PIDFILE}")" "${LOGFILE}"
}

cmd_down() {
  [ -f "${PIDFILE}" ] || { printf 'gateway.sh: not running\n'; return 0; }
  local pid
  pid="$(cat "${PIDFILE}")"
  kill "${pid}" 2>/dev/null || true
  rm -f "${PIDFILE}"
  printf 'gateway.sh: stopped\n'
}

cmd_status() {
  if [ -f "${PIDFILE}" ] && kill -0 "$(cat "${PIDFILE}")" 2>/dev/null; then
    printf 'gateway.sh: running (pid %s)\n' "$(cat "${PIDFILE}")"
  else
    printf 'gateway.sh: not running\n'
    return 1
  fi
  if curl -fsS --max-time 5 "http://127.0.0.1:${LLM_PORT}/v1/models" > /dev/null 2>&1; then
    printf 'gateway.sh: LLM endpoint 127.0.0.1:%s OK\n' "${LLM_PORT}"
  else
    printf 'gateway.sh: LLM endpoint 127.0.0.1:%s unreachable\n' "${LLM_PORT}"
  fi
}

free_port() {
  python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()'
}

cmd_selftest() {
  # Boot the gateway on ephemeral ports, probe both endpoints, stop it.
  # Never touches the real 4000/4100 listeners.
  local llm a2a cfg work rc=0
  llm="$(free_port)"; a2a="$(free_port)"
  work="$(mktemp -d)"
  cfg="${work}/agentgateway.yaml"
  LLM_PORT="${llm}" A2A_PORT="${a2a}" cmd_apply --config "${cfg}"
  "${BIN}" --file "${cfg}" > "${work}/gw.log" 2>&1 &
  local gwpid=$!
  trap 'kill "${gwpid}" 2>/dev/null || true; rm -rf "${work}"' RETURN
  local i
  for i in 1 2 3 4 5 6 7 8 9 10; do
    if curl -fsS --max-time 2 "http://127.0.0.1:${llm}/v1/models" > /dev/null 2>&1; then
      break
    fi
    sleep 0.5
  done
  if curl -fsS --max-time 5 "http://127.0.0.1:${llm}/v1/models" > /dev/null 2>&1; then
    printf 'selftest: LLM endpoint (:%s) OK\n' "${llm}"
  else
    printf 'selftest: LLM endpoint failed to come up:\n'; cat "${work}/gw.log"
    rc=1
  fi
  if curl -fsS --max-time 5 "http://127.0.0.1:${a2a}/health" > /dev/null 2>&1; then
    printf 'selftest: A2A endpoint (:%s) OK (adapter reachable)\n' "${a2a}"
  else
    # The adapter may be down; that is a finding, not a gateway failure.
    printf 'selftest: A2A endpoint (:%s) no adapter answer (gateway may still be up)\n' "${a2a}"
  fi
  # The RETURN trap also fires when main() and the script itself return,
  # where the locals are gone; clean up here and clear it.
  trap - RETURN
  kill "${gwpid}" 2>/dev/null || true
  rm -rf "${work}"
  return "${rc}"
}

main() {
  local cmd="${1:-status}"
  case "${cmd}" in
    apply) shift; cmd_apply "$@" ;;
    up) cmd_up ;;
    down) cmd_down ;;
    status) cmd_status ;;
    selftest) cmd_selftest ;;
    *) die "unknown command: ${cmd} (apply|up|down|status|selftest)" ;;
  esac
}

main "$@"
