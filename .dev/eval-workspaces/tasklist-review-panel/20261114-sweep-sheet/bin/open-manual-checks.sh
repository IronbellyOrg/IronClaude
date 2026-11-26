#!/usr/bin/env bash
# open-manual-checks.sh [--sw DIR]   (TESTING section 3 rows of kind M, section 6 item 4; read-only)
# Prints the manual (M) records that are still open, one line each: `OPEN <id>: <what is missing>`, then `open: <n>`.
# A record is closed by the file or the entry that its row names; this script only looks for them and decides nothing.
#   swap:C1 .. swap:C8       cards/C<n>.json `swap_test` has a reviewer and a date (REQ-08)
#   recall-authors           fixtures/recall/AUTHORS.md exists and is not empty (REQ-21)
#   readme-second-reader     cards/README.md has no line "Second reader ... Status: OPEN" (REQ-38)
#   owner-values             config/prereg.json exists and says owner_confirmed true (REQ-41)
#   spike                    config/values.json: spike.runs is 5 or more (REQ-32)
#   gt-attestation           config/attestation.md exists (REQ-36)
#   attest:<id>              results/attestations.md has a line `ATTEST <id>: <person>, <date>, <statement>` for each of:
#                            freeze-order (REQ-33), prereg-order (REQ-44), report-measured-values (REQ-31),
#                            report-headline (REQ-40), report-claims (REQ-45)
#   model-stage-ablation     not run (DD-13): an owner decision, listed so that it is not forgotten
# Exit: always 0 (it reports; it does not gate). --sw DIR reads another tree (a test hook, under /tmp only).
set -u -o pipefail
source "$(dirname "$0")/common.sh"

TREE=$SW
if [ $# -ge 1 ]; then
  [ "$1" = --sw ] && [ $# -eq 2 ] || { sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 2; }
  case "$(realpath -m -- "$2")/" in /tmp/?*) TREE=$2 ;; *) echo "E_OVERRIDE: --sw $2 is outside /tmp/" >&2; exit 2 ;; esac
fi
OPEN=0
open() { echo "OPEN $1: $2"; OPEN=$((OPEN + 1)); }

for n in 1 2 3 4 5 6 7 8; do
  f=$TREE/cards/C$n.json
  if [ ! -f "$f" ]; then
    open "swap:C$n" "cards/C$n.json does not exist"
  elif [ -z "$(jq -r '.swap_test.reviewer // ""' "$f")" ] || [ -z "$(jq -r '.swap_test.date // ""' "$f")" ]; then
    open "swap:C$n" "swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign"
  fi
done

[ -s "$TREE/fixtures/recall/AUTHORS.md" ] || open recall-authors "fixtures/recall/AUTHORS.md is missing: who seeded the recall plans, and that they had not read the extractors"
if [ ! -f "$TREE/cards/README.md" ] || grep -Eq 'Second reader.*Status: OPEN' "$TREE/cards/README.md"; then
  open readme-second-reader "cards/README.md still says the second reader's record is OPEN"
fi
if [ "$(jq -r '.owner_confirmed // false' "$TREE/config/prereg.json" 2>/dev/null)" != true ]; then
  open owner-values "config/prereg.json is missing or not confirmed by the owner (analysis/analyze.py prereg --write --owner-values FILE)"
fi
runs=$(jq -r '.spike.runs // 0' "$TREE/config/values.json" 2>/dev/null || echo 0)
[ "${runs:-0}" -ge 5 ] 2>/dev/null || open spike "config/values.json has no spike record of 5 runs (bin/run-spike.sh timing; needs the owner's go-ahead)"
[ -f "$TREE/config/attestation.md" ] || open gt-attestation "config/attestation.md is missing: the ground-truth author, the date, 'has not seen the recipes, cards or extractors', the hashes"
for id in freeze-order prereg-order report-measured-values report-headline report-claims; do
  grep -Eq "^ATTEST $id: .+, .+, .+" "$TREE/results/attestations.md" 2>/dev/null || open "attest:$id" "results/attestations.md has no ATTEST $id line"
done
open model-stage-ablation "not run: 8 extra arms and 96 panel runs outside the run budget; an owner decision (DD-13)"
echo "open: $OPEN"
exit 0
