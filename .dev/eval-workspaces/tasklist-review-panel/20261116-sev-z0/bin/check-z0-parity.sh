#!/usr/bin/env bash
# usage: check-z0-parity.sh DOC [--panel primary|haiku|sonnet]                       (DESIGN 3.5, DR-12)
# Renders the Z0 brief of document DOC with the copied code (scaffold/briefs.py through rl/cli.py briefs) and prints its
# sha256 on one line. A person compares it with `z0_sha256` in the run.json of any Sweep Sheet Z0 run of the same document:
# the Z0 brief of both builds is byte for byte the same text for the same inputs. Nothing is written but a scratch folder
# under /tmp that is removed on exit; no model is started.
# The sandbox of DOC must exist (bin/build-sandbox.sh DOC): the candidate (and the source, if the document has one) are read
# from $SW_SB_ROOT/cand/DOC/ (default /tmp/evalsb-recipe). RL_LENSES names another lens table (it only supplies the panel's
# reviewer list; the brief does not depend on it).
# Exit: 0 printed, 2 usage or no sandbox, 1 the render failed.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"

case "${1:-}" in -h | --help) sed -n '2,/^set -u/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;; esac
usage() { echo "usage: check-z0-parity.sh DOC [--panel primary|haiku|sonnet]" >&2; exit 2; }
DOC=${1:-}
PANEL=primary
[ -n "$DOC" ] || usage
shift
if [ $# -gt 0 ]; then
  [ "$1" = --panel ] && [ $# -eq 2 ] || usage
  PANEL=$2
fi
[[ $DOC =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || usage
CAND=$SB/cand/$DOC/candidate.md
SOURCE=$SB/cand/$DOC/source.md
[ -f "$CAND" ] || { echo "E_SANDBOX: no candidate $CAND (run bin/build-sandbox.sh $DOC first)" >&2; exit 2; }
OUT=$(mktemp -d /tmp/rl-z0parity.XXXXXXXX) || exit 1
trap 'rm -rf -- "$OUT"' EXIT
ARGS=(--arm Z0 --panel "$PANEL" --doc "$DOC" --candidate-sb "$CAND" --out "$OUT")
[ ! -f "$SOURCE" ] || ARGS+=(--source "$SOURCE")
[ -z "${RL_LENSES:-}" ] || ARGS+=(--lenses "$RL_LENSES")
sw_py "$HERE/../rl/cli.py" briefs "${ARGS[@]}" || { echo "E_RENDER: the Z0 brief could not be rendered" >&2; exit 1; }
jq -r '.z0_sha256' "$OUT/run.json"
