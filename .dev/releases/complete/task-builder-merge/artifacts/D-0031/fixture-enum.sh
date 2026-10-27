#!/usr/bin/env bash
# D-0031 — T03.07 fixture: INV-010 dynamic TB-Add enumeration
#
# Demonstrates that the orchestrator's catalogue lookup (SKILL.md A.10.5
# step 1-8 "TB-Add catalogue enumeration (INV-010 dynamic catalogue
# lookup)") auto-richens when a synthetic TB-Add stub is appended to
# rf-qa.md's bounded "Structural Gate Additions" region.
#
# Cycle 1 baseline: enumerate live rf-qa.md → LIVE_TB_ADD = [TB-Add-1..K].
# Cycle 2 grown:    append synthetic TB-Add-(K+1) to a working copy →
#                   LIVE_TB_ADD' = [TB-Add-1..K, TB-Add-(K+1)].
# Assertions:
#   (a) LIVE_TB_ADD' has exactly one more entry than LIVE_TB_ADD.
#   (b) The new entry is the appended TB-Add-(K+1).
#   (c) byte-diff between cycle-1 and cycle-2 spawn-prompt verdict blocks
#       surfaces the new TB-Add-(K+1) row, no other changes.
#   (d) The INV-010 structured log line is emitted on each enumeration
#       with the live size K.
#   (e) The canonical rf-qa.md on disk is untouched (synthetic stub
#       lives only in the temp working copy).
#
# This script is the proof-of-concept demonstration evidence. The formal
# pytest fixture (tests/audit/test_dynamic_enumeration_inv_010.py) is the
# T03.15 / TEST-010 deliverable.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../../.." && pwd)"
RF_QA="$REPO_ROOT/src/superclaude/agents/rf-qa.md"

if [ ! -f "$RF_QA" ]; then
  echo "ERROR: cannot locate rf-qa.md at $RF_QA" >&2
  exit 1
fi

# ----- helpers -----
extract_catalogue() {
  # Reproduces SKILL.md A.10.5 steps 2-4: bound the "Structural Gate
  # Additions" region, then regex-extract TB-Add IDs from that span.
  local src="$1"
  awk '
    /^#### Structural Gate Additions/ { inblock = 1; next }
    inblock && /^(####|###|## )/      { exit }
    inblock                            { print }
  ' "$src" \
    | grep -oE '^[0-9]+\. \*\*TB-Add-[0-9]+:' \
    | grep -oE 'TB-Add-[0-9]+' \
    | sort -t- -k3 -n -u
}

emit_log() {
  # Reproduces SKILL.md A.10.5 step 7: structured INV-010 log line.
  local size="$1"
  local ids_csv="$2"
  local sha="$3"
  printf 'INV-010: enumerated TB-Add-* catalogue size=%s ids=[%s] source=rf-qa.md source_sha256=%s\n' \
    "$size" "$ids_csv" "$sha"
}

render_block() {
  # Reproduces the spawn-prompt verdict-block enumeration target. In
  # the real orchestrator, this block carries the producer's "Items
  # Reviewed" table; here we render a normalised row-per-TB-Add view
  # that is sufficient to observe enrichment via byte-diff.
  local catalogue_file="$1"
  echo "## Inherited Structural Verdict (enumeration view)"
  while read -r id; do
    printf '| %s | (status carried verbatim from producer) |\n' "$id"
  done < "$catalogue_file"
}

# ----- workdir -----
WORKDIR="$(mktemp -d -t inv010-XXXXXX)"
trap 'rm -rf "$WORKDIR"' EXIT

PRE_HASH="$(sha256sum "$RF_QA" | cut -c1-16)"

# ===== Cycle 1: baseline =====
cp "$RF_QA" "$WORKDIR/rf-qa.cycle1.md"
extract_catalogue "$WORKDIR/rf-qa.cycle1.md" > "$WORKDIR/cat1.txt"
K1="$(wc -l < "$WORKDIR/cat1.txt" | tr -d ' ')"
IDS1="$(paste -sd, "$WORKDIR/cat1.txt")"
SHA1="$(sha256sum "$WORKDIR/rf-qa.cycle1.md" | cut -c1-16)"
LOG1="$(emit_log "$K1" "$IDS1" "$SHA1")"
render_block "$WORKDIR/cat1.txt" > "$WORKDIR/block.cycle1.md"

# ===== Cycle 2: grow catalogue with synthetic TB-Add-(K+1) =====
cp "$RF_QA" "$WORKDIR/rf-qa.cycle2.md"
SYNTH_N="$((K1 + 1))"
SYNTH_NUM="$((K1 + 27))"   # next sequential numbered item in the catalogue
SYNTH_LINE="$SYNTH_NUM. **TB-Add-$SYNTH_N: Synthetic enrichment stub (fixture-only).** This entry is appended only inside the fixture's temp copy of rf-qa.md to demonstrate INV-010 auto-richening. The canonical rf-qa.md on disk is NOT modified."

# Append the synthetic line at the end of the bounded region (just
# before the next top-level heading following Structural Gate Additions).
awk -v synth="$SYNTH_LINE" '
  /^#### Structural Gate Additions/ { in_block = 1; print; next }
  in_block && /^(####|###|## )/     { print synth; print ""; in_block = 0; print; next }
  { print }
  END {
    if (in_block) { print synth; print "" }
  }
' "$WORKDIR/rf-qa.cycle1.md" > "$WORKDIR/rf-qa.cycle2.md"

extract_catalogue "$WORKDIR/rf-qa.cycle2.md" > "$WORKDIR/cat2.txt"
K2="$(wc -l < "$WORKDIR/cat2.txt" | tr -d ' ')"
IDS2="$(paste -sd, "$WORKDIR/cat2.txt")"
SHA2="$(sha256sum "$WORKDIR/rf-qa.cycle2.md" | cut -c1-16)"
LOG2="$(emit_log "$K2" "$IDS2" "$SHA2")"
render_block "$WORKDIR/cat2.txt" > "$WORKDIR/block.cycle2.md"

# ----- emit cycle headers + structured logs (operator-visible) -----
echo "[fixture] canonical rf-qa.md sha (first 16) = $PRE_HASH"
echo "[fixture] cycle-1 K=$K1 ids=$IDS1"
echo "[fixture] cycle-2 K=$K2 ids=$IDS2 (with synthetic TB-Add-$SYNTH_N appended to working copy)"
echo "$LOG1"
echo "$LOG2"

# ===== Assertions =====
fail=0

# (a) LIVE_TB_ADD' has exactly one more entry than LIVE_TB_ADD
if [ "$K2" -eq "$((K1 + 1))" ]; then
  echo "PASS (a): catalogue grew by exactly 1 (K=$K1 → K'=$K2)"
else
  echo "FAIL (a): expected K2 = K1+1 = $((K1 + 1)), got K2=$K2" >&2
  fail=1
fi

# (b) The new entry is the appended TB-Add-(K1+1)
if grep -qxF "TB-Add-$SYNTH_N" "$WORKDIR/cat2.txt" && ! grep -qxF "TB-Add-$SYNTH_N" "$WORKDIR/cat1.txt"; then
  echo "PASS (b): cycle-2 enumeration includes the new TB-Add-$SYNTH_N (absent in cycle-1)"
else
  echo "FAIL (b): cycle-2 does not exclusively introduce TB-Add-$SYNTH_N" >&2
  fail=1
fi

# (c) byte-diff between cycle-1 and cycle-2 spawn-prompt verdict blocks
DIFF_OUT="$(diff "$WORKDIR/block.cycle1.md" "$WORKDIR/block.cycle2.md" || true)"
ADDED_ROWS="$(echo "$DIFF_OUT" | grep -E "^> \| TB-Add-$SYNTH_N \|" | wc -l | tr -d ' ')"
TOTAL_ADDED="$(echo "$DIFF_OUT" | grep -cE '^> ' || true)"
if [ "$ADDED_ROWS" = "1" ] && [ "$TOTAL_ADDED" = "1" ]; then
  echo "PASS (c): structural diff surfaces exactly the new TB-Add-$SYNTH_N row (1 added line, 0 deletions)"
else
  echo "FAIL (c): expected exactly one added line (TB-Add-$SYNTH_N), got added=$TOTAL_ADDED of which TB-Add-$SYNTH_N=$ADDED_ROWS" >&2
  fail=1
fi

# (d) INV-010 log emitted on each enumeration with correct size
if echo "$LOG1" | grep -qE "^INV-010: enumerated TB-Add-\* catalogue size=$K1 ids=\[.*\] source=rf-qa.md source_sha256=[0-9a-f]{16}\$" \
&& echo "$LOG2" | grep -qE "^INV-010: enumerated TB-Add-\* catalogue size=$K2 ids=\[.*\] source=rf-qa.md source_sha256=[0-9a-f]{16}\$"; then
  echo "PASS (d): INV-010 structured log emitted for both cycles with correct sizes"
else
  echo "FAIL (d): INV-010 log shape mismatch" >&2
  fail=1
fi

# (e) Canonical rf-qa.md on disk is untouched
POST_HASH="$(sha256sum "$RF_QA" | cut -c1-16)"
if [ "$POST_HASH" = "$PRE_HASH" ]; then
  echo "PASS (e): canonical rf-qa.md byte-identical pre/post fixture (sha first 16 = $POST_HASH)"
else
  echo "FAIL (e): canonical rf-qa.md changed during fixture run (pre=$PRE_HASH post=$POST_HASH)" >&2
  fail=1
fi

echo
echo "----- structural diff cycle-1 → cycle-2 (verdict-block enumeration view) -----"
echo "$DIFF_OUT"
echo "----- end structural diff -----"
echo

if [ "$fail" -eq 0 ]; then
  echo "ALL ASSERTIONS PASS — INV-010 dynamic enumeration auto-richens on catalogue growth."
  exit 0
else
  echo "FIXTURE FAILED" >&2
  exit 2
fi
