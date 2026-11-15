#!/usr/bin/env bash
# usage: open-manual-checks.sh                                                       (TESTING sections 3 and 6)
#        open-manual-checks.sh ran-audit [RUN_DIR ...] [--rows N] [--seed S]
# Lists the manual (M) records of TESTING.md and whether each one is still open. A record is closed by a file or a line that
# a person writes; this script only looks. One line per record: "OPEN" or "done", the requirement, what closes it.
#
#   REQ-08  recipes/REVIEWS.md: all eight rows C1 to C8 are DONE with a reviewer and a date
#   REQ-28  results/ran-audit.md exists (the 20-row audit below)
#   REQ-31  a line "REQ-31" in results/attestations.md (the report shows measured next to planned values)
#   REQ-32  config/values.json holds a spike record of at least 5 runs with a c_luna (bin/run-spike.sh timing)
#   REQ-33  a line "REQ-33" in results/attestations.md (the output of bin/check-order.sh freeze)
#   REQ-36  config/attestation.md exists (author, date, hash of the ground-truth files)
#   REQ-38  a line at the foot of recipes/README.md: reader, date, "each row is specific, not a restatement of the heading"
#   REQ-40  a line "REQ-40" in results/attestations.md (the headline adds no two shares)
#   REQ-41  config/prereg.json exists (the real bands, committed before the first hold-out run)
#   REQ-44  a line "REQ-44" in results/attestations.md (the output of bin/check-order.sh prereg)
#   REQ-45  a line "REQ-45" in results/attestations.md (the final report uses the REQ-45 wording)
#   REQ-35  the model-stage ablation: not run; it stays open until the owner decides (DR-13)
#
# `ran-audit` prints 20 rows of the compliance spike (default folder RL/runs/spike-compliance) with their transcripts for the
# REQ-28 audit (bin/ran-audit.py): write results/ran-audit.md after reading them.
# RL_ROOT (default: the folder above bin/) is the root whose records are read. Exit: 0 listed (open records are not an
# error), 2 usage.
set -u -o pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=rl-env.sh
source "$HERE/rl-env.sh"
# shellcheck source=common.sh
source "$HERE/common.sh"
ROOT=${RL_ROOT:-$SW}

case "${1:-}" in
  -h | --help) sed -n '2,/^set -u/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//'; exit 0 ;;
  ran-audit) shift; exec uv run --frozen --project "$REPO" python "$HERE/ran-audit.py" "$@" ;;
  "") ;;
  *) echo "usage: open-manual-checks.sh [ran-audit [RUN_DIR ...] [--rows N] [--seed S]]" >&2; exit 2 ;;
esac

ATT=$ROOT/results/attestations.md
attested() { [ -f "$ATT" ] && grep -q "^$1\b" "$ATT"; }
reviews_done() {
  [ -f "$ROOT/recipes/REVIEWS.md" ] &&
    [ "$(grep -Ec '^\| C[1-8] \| DONE \| [^|[:space:]][^|]*\| [^|[:space:]][^|]*\|' "$ROOT/recipes/REVIEWS.md")" = 8 ]
}
spike_done() {
  [ -f "$ROOT/config/values.json" ] &&
    jq -e '(.spike.runs // 0) >= 5 and ((.spike.c_luna // null) | type) == "number"' "$ROOT/config/values.json" >/dev/null 2>&1
}
readme_signed() {
  [ -f "$ROOT/recipes/README.md" ] &&
    grep -Eq '[0-9]{4}-[0-9]{2}-[0-9]{2}.*each row is specific, not a restatement of the heading' "$ROOT/recipes/README.md"
}

OPEN=0
rec() { # rec REQ "what closes it" <test command...>
  local req=$1 what=$2 state=OPEN
  shift 2
  if "$@"; then state=done; else OPEN=$((OPEN + 1)); fi
  printf '%-4s %s  %s\n' "$state" "$req" "$what"
}
rec REQ-08 "recipe reviews: recipes/REVIEWS.md rows C1 to C8 DONE with reviewer and date" reviews_done
rec REQ-28 "ran audit: results/ran-audit.md (18 of 20 rows agree; bin/open-manual-checks.sh ran-audit)" test -f "$ROOT/results/ran-audit.md"
rec REQ-31 "report read: REQ-31 line in results/attestations.md" attested REQ-31
rec REQ-32 "timing spike: values.json spike record of 5 runs with a c_luna (bin/run-spike.sh timing --go)" spike_done
rec REQ-33 "real freeze order: REQ-33 line in results/attestations.md (bin/check-order.sh freeze)" attested REQ-33
rec REQ-36 "hold-out attestation: config/attestation.md (author, date, ground-truth hashes)" test -f "$ROOT/config/attestation.md"
rec REQ-40 "report headline read: REQ-40 line in results/attestations.md" attested REQ-40
rec REQ-41 "act bands: config/prereg.json committed with the owner's values" test -f "$ROOT/config/prereg.json"
rec REQ-44 "real prereg order: REQ-44 line in results/attestations.md (bin/check-order.sh prereg)" attested REQ-44
rec REQ-45 "claim wording review: REQ-45 line in results/attestations.md" attested REQ-45
rec REQ-38 "README content review: dated reader line at the foot of recipes/README.md" readme_signed
rec REQ-35 "model-stage ablation: not run (96 panel runs); owner decision" false
echo "open: $OPEN of 12"
