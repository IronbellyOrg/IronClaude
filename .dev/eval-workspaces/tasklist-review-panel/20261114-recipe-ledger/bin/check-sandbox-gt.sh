#!/usr/bin/env bash
# usage: check-sandbox-gt.sh [DIR ...]                                               (REQ-34, DESIGN 11.1 AO-6)
# Reviewers never receive ground truth. This looks for it: a `grep -r` over every sandbox under the sandbox root
# ($SW_SB_ROOT, default /tmp/evalsb-recipe) and over every RUN/briefs folder under the runs root ($RL_RUNS_ROOT, default
# RL/runs; at any depth, so the spike runs runs/spike-timing/<run>/briefs and runs/spike-compliance/<run>/briefs count),
# or over the folders named on the command line instead. It looks for
#   * a file whose name starts with ground-truth, ground_truth or groundtruth, and
#   * a file that holds a ground-truth file name (ground-truth*.json) or one of the ground-truth field names
#     plan_quote and blocking_in_implement.
# The .git folders are not searched (a sandbox repository's history is checked by bin/build-sandbox.sh). The Z0-raw sandbox
# (repo-raw) is the whole repository minus its ground-truth files (DD-15) and holds documents that talk about ground truth,
# so it is searched by file name only.
# It prints the PATH of each hit, once per file, and nothing else: never a matching line, never file content. It prints
# nothing when clean. Exit: 0 clean, 1 at least one hit, 2 a named folder does not exist.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"

case "${1:-}" in -h | --help) sed -n '2,/^set -u/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;; esac
DIRS=()
if [ $# -gt 0 ]; then
  for d in "$@"; do
    [ -d "$d" ] || { echo "E_DIR: $d is not a folder" >&2; exit 2; }
    DIRS+=("$d")
  done
else
  RUNS=${RL_RUNS_ROOT:-$SW/runs}
  [ ! -d "$SB" ] || DIRS+=("$SB")
  # every briefs folder at any depth: runs/<id>/briefs and the spike runs of bin/run-spike.sh, runs/spike-*/<run>/briefs
  if [ -d "$RUNS" ]; then
    while IFS= read -r b; do
      DIRS+=("$b")
    done < <(find "$RUNS" -name .git -prune -o -type d -name briefs -print | sort)
  fi
fi
[ ${#DIRS[@]} -gt 0 ] || exit 0

HITS=$(
  for d in "${DIRS[@]}"; do
    find "$d" -name .git -prune -o -type f \( -iname 'ground-truth*' -o -iname 'ground_truth*' -o -iname 'groundtruth*' \) -print
    grep -rIl --exclude-dir=.git --exclude-dir=repo-raw -E 'ground-truth[A-Za-z0-9_.-]*\.json|plan_quote|blocking_in_implement' -- "$d" 2>/dev/null
  done | sort -u
)
[ -z "$HITS" ] || { printf '%s\n' "$HITS"; exit 1; }
exit 0
