#!/usr/bin/env bash
# Run the REAL swarm end-to-end suite against the live T2 proxy.
#
# This spends REAL tokens. It drives `superclaude swarm run --transport
# openai_compat` across multiple lenses and real .aienv models.
#
# Contract source: /config/.aienv (the ONLY authorized source of endpoint,
# key, and models — never probe other ports/paths or query the proxy API).
#   * T2ProxyKey   : bearer key            (from .aienv)
#   * T2Model0N    : model pool            (from .aienv)
#   * T2ProxyUrl   : base; .aienv ships :4000/cli. The swarm openai_compat
#                    transport appends /chat/completions, and the working
#                    OpenAI-compatible path is :4000/cli/v1/chat/completions,
#                    so we point the base at :4000/cli/v1 (user-authorized;
#                    still under :4000/cli).
#
# Usage:  ./scripts/run_swarm_real_e2e.sh [pytest args...]
set -euo pipefail

AIENV="/config/.aienv"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

if [[ ! -f "$AIENV" ]]; then
  echo "FATAL: $AIENV not found — it is the only authorized proxy contract source." >&2
  exit 2
fi

# shellcheck disable=SC1090
source "$AIENV"

: "${T2ProxyKey:?T2ProxyKey not set by .aienv}"
: "${T2ProxyUrl:?T2ProxyUrl not set by .aienv}"

# Normalize the bare :4000/cli base to the working OpenAI path :4000/cli/v1.
base="${T2ProxyUrl%/}"
if [[ "$base" == */cli ]]; then
  base="${base}/v1"
fi
export T2ProxyUrl="$base"
export SWARM_REAL_E2E=1

# Collect the model pool actually present for the report.
models=()
for i in 1 2 3 4 5 6 7 8 9; do
  v="$(eval echo "\${T2Model0$i:-}")"
  [[ -n "$v" ]] && models+=("$v")
done

echo "============================================================"
echo " REAL swarm E2E — live proxy (spends tokens)"
echo "   endpoint : ${T2ProxyUrl}/chat/completions"
echo "   key      : ${T2ProxyKey:0:8}…(${#T2ProxyKey} chars)"
echo "   models   : ${models[*]:-<none>}"
echo "============================================================"

# Fast connectivity precheck against the authorized endpoint (model slot 1).
probe_model="${T2Model01:-${models[0]:-}}"
code="$(curl -s -m 20 -o /dev/null -w '%{http_code}' \
  "${T2ProxyUrl}/chat/completions" \
  -H "Authorization: Bearer ${T2ProxyKey}" -H 'Content-Type: application/json' \
  -d "{\"model\":\"${probe_model}\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"max_tokens\":5}" || echo 000)"
if [[ "$code" != "200" ]]; then
  echo "FATAL: proxy precheck failed (HTTP $code) at ${T2ProxyUrl}/chat/completions with model ${probe_model}" >&2
  echo "       Refusing to run — fix the .aienv contract, do not substitute another endpoint." >&2
  exit 1
fi
echo "precheck: HTTP 200 OK (model=${probe_model})"
echo ""

exec uv run pytest tests/swarm/test_e2e_real_proxy.py -v "$@"
