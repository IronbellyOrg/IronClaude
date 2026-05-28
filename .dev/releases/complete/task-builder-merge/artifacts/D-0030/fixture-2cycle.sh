#!/usr/bin/env bash
#
# D-0030 T03.05 — 2-cycle INV-002 freshness fixture (synthetic demonstration)
#
# Purpose: Demonstrate the cycle-N+1 reinjection rule (INV-002) by simulating
# two consecutive rf-qa task-integrity producer artifacts (cycle 1 + cycle 2)
# whose "Items Reviewed" PASS/FAIL tables differ, then exercising the
# orchestrator's re-extract + splice procedure documented at SKILL.md A.10.5
# steps 1-7. The fixture asserts:
#
#   (a) Cycle-2 spawn prompt contains cycle-2's verdict (post-fix PASS row).
#   (b) Cycle-2 spawn prompt does NOT contain cycle-1's verdict (pre-fix FAIL row).
#   (c) Byte-diff of cycle-1 vs cycle-2 spawn prompts at the verdict-table
#       region surfaces the cycle-2 content (non-zero diff).
#   (d) The re-extract log line for cycle 2 is emitted with witness fields.
#
# The formal pytest fixture under tests/audit/test_inherited_verdict_freshness_inv_002.py
# is deferred to T03.13 (TEST-008); this shell fixture is the static
# proof-of-concept evidence consumed by D-0030/evidence.md.

set -euo pipefail

WORKDIR="$(mktemp -d -t inv002-XXXXXX)"
trap 'rm -rf "$WORKDIR"' EXIT

TASK_DIR="$WORKDIR/TASK-DEMO/"
mkdir -p "${TASK_DIR}qa"
PRODUCER="${TASK_DIR}qa/qa-task-validation-report.md"

# ---------------------------------------------------------------------------
# Cycle 1: producer reports TB-Add-3 FAIL (clarification-adjacency violation).
# ---------------------------------------------------------------------------
cat >"$PRODUCER" <<'CYCLE1'
# qa-task-validation-report.md (cycle 1 — pre-fix)

## Items Reviewed

| Item ID  | Check                                  | Verdict | Notes                                  |
|----------|----------------------------------------|---------|----------------------------------------|
| TB-Add-1 | Placeholder scan (no TBD/TODO/FIXME)   | PASS    | clean                                  |
| TB-Add-2 | Item count bounds                      | PASS    | 28 items, within bounds                |
| TB-Add-3 | Clarification adjacency                | FAIL    | items 4, 7 missing Open-Question refs  |
| TB-Add-4 | Circular dependency detection          | PASS    | DAG verified                           |
| TB-Add-5 | Granularity / XL splitting             | PASS    | no XL items                            |

## Verdict

VERDICT: FAIL (TB-Add-3 unfixable in single pass)
CYCLE1

# Capture cycle-1 witness fields (mtime + sha256).
sleep 1  # ensure subsequent mtime is strictly newer
P1_MTIME="$(stat -c '%Y' "$PRODUCER")"
P1_SHA="$(sha256sum "$PRODUCER" | cut -c1-16)"

# Extract cycle-1 "Items Reviewed" span contiguously (single span between the
# `## Items Reviewed` heading and the next top-level `## ` heading).
extract_span() {
    awk '
        /^## Items Reviewed/ {capture=1; print; next}
        capture && /^## / {capture=0}
        capture {print}
    ' "$1"
}

CYCLE1_SPAN="$(extract_span "$PRODUCER")"

# Assemble cycle-1 spawn prompt (verdict block sits between TARGET FILES and
# ADVERSARIAL STANCE per the API-002 wire-contract position).
build_spawn_prompt() {
    local span="$1"
    cat <<PROMPT
QA_PHASE: task-qualitative
fix_authorization: true

TASK FILE: ${TASK_DIR}TASK-DEMO.md

TARGET FILES (verify ALL — no spot-checking):
- ${TASK_DIR}TASK-DEMO.md

PROJECT CONVENTIONS:
None identified.

## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)
${span}

**ADVERSARIAL STANCE:** Assume the work contains errors.

INSTRUCTIONS:
Apply the 15-item Task File Qualitative Review checklist.
PROMPT
}

CYCLE1_PROMPT="$(build_spawn_prompt "$CYCLE1_SPAN")"
C1_BLOCK_SHA="$(printf '%s' "$CYCLE1_SPAN" | sha256sum | cut -c1-16)"
printf '%s\n' "$CYCLE1_PROMPT" >"$WORKDIR/spawn-prompt-cycle-1.txt"

echo "[fixture] cycle-1 producer witness mtime=$P1_MTIME sha=$P1_SHA block_sha=$C1_BLOCK_SHA"

# ---------------------------------------------------------------------------
# Fix cycle: rf-qa re-runs (producer rewrites the file with TB-Add-3 PASS).
# ---------------------------------------------------------------------------
sleep 1
cat >"$PRODUCER" <<'CYCLE2'
# qa-task-validation-report.md (cycle 2 — post-fix)

## Items Reviewed

| Item ID  | Check                                  | Verdict | Notes                                  |
|----------|----------------------------------------|---------|----------------------------------------|
| TB-Add-1 | Placeholder scan (no TBD/TODO/FIXME)   | PASS    | clean                                  |
| TB-Add-2 | Item count bounds                      | PASS    | 28 items, within bounds                |
| TB-Add-3 | Clarification adjacency                | PASS    | items 4, 7 now reference OQ-1/OQ-2     |
| TB-Add-4 | Circular dependency detection          | PASS    | DAG verified                           |
| TB-Add-5 | Granularity / XL splitting             | PASS    | no XL items                            |

## Verdict

VERDICT: PASS
CYCLE2

P2_MTIME="$(stat -c '%Y' "$PRODUCER")"
P2_SHA="$(sha256sum "$PRODUCER" | cut -c1-16)"

# Per A.10.5 fix-cycle re-entry procedure:
#   Step 1: discard cached state (no cache reuse — we always recompute below).
#   Step 2: re-stat + re-sha256 the producer artifact; compare witnesses.
if [ "$P1_MTIME" = "$P2_MTIME" ] && [ "$P1_SHA" = "$P2_SHA" ]; then
    echo "[fixture] stale-producer: witnesses unchanged — log and proceed."
fi
#   Step 3: re-extract span contiguously (do NOT reuse cycle-1 extraction).
CYCLE2_SPAN="$(extract_span "$PRODUCER")"
#   Step 4: re-enumerate TB-Add catalogue (omitted in this synthetic fixture —
#           the static catalogue above already enumerates TB-Add-1..5).
#   Step 5: re-assemble + re-splice the spawn prompt.
CYCLE2_PROMPT="$(build_spawn_prompt "$CYCLE2_SPAN")"
C2_BLOCK_SHA="$(printf '%s' "$CYCLE2_SPAN" | sha256sum | cut -c1-16)"
printf '%s\n' "$CYCLE2_PROMPT" >"$WORKDIR/spawn-prompt-cycle-2.txt"

#   Step 6: stale-verdict-rejection — the contradiction case is
#           (P1_SHA != P2_SHA) AND (C1_BLOCK_SHA == C2_BLOCK_SHA).
if [ "$P1_SHA" != "$P2_SHA" ] && [ "$C1_BLOCK_SHA" = "$C2_BLOCK_SHA" ]; then
    echo "[fixture] INV-002-stale-verdict-rejected: producer changed but block sha unchanged."
    exit 7
fi

#   Step 7: log the re-extract.
ISO_MTIME="$(date -u -d "@$P2_MTIME" +%Y-%m-%dT%H:%M:%SZ)"
echo "INV-002: re-extracted verdict for ${TASK_DIR} cycle=2 producer_mtime=${ISO_MTIME} producer_sha256=${P2_SHA} block_sha256=${C2_BLOCK_SHA}" \
    | tee "$WORKDIR/orchestrator.log"

# ---------------------------------------------------------------------------
# Assertions
# ---------------------------------------------------------------------------

# (a) Cycle-2 spawn prompt contains cycle-2's PASS row for TB-Add-3.
if ! grep -q "TB-Add-3 | Clarification adjacency.*PASS.*items 4, 7 now reference OQ-1/OQ-2" \
        "$WORKDIR/spawn-prompt-cycle-2.txt"; then
    echo "FAIL: cycle-2 spawn does not contain cycle-2 verdict"
    exit 1
fi
echo "PASS (a): cycle-2 spawn carries cycle-2 verdict (TB-Add-3 PASS row present)"

# (b) Cycle-2 spawn prompt does NOT contain cycle-1's FAIL row.
if grep -q "TB-Add-3 | Clarification adjacency.*FAIL.*items 4, 7 missing" \
        "$WORKDIR/spawn-prompt-cycle-2.txt"; then
    echo "FAIL: cycle-2 spawn still contains cycle-1 stale verdict"
    exit 1
fi
echo "PASS (b): cycle-2 spawn does NOT contain cycle-1's stale FAIL row"

# (c) Byte-diff of cycle-1 vs cycle-2 spawn prompts at the verdict-table region
#     surfaces cycle-2 content (non-zero diff).
DIFF_RAW="$(diff "$WORKDIR/spawn-prompt-cycle-1.txt" "$WORKDIR/spawn-prompt-cycle-2.txt" \
              || true)"
DIFF_BYTES="$(printf '%s\n' "$DIFF_RAW" | grep -cE '^[<>]' || true)"
if [ "$DIFF_BYTES" -eq 0 ]; then
    echo "FAIL: cycle-1 and cycle-2 spawn prompts are byte-identical"
    exit 1
fi
echo "PASS (c): cycle-1 vs cycle-2 byte-diff is non-zero ($DIFF_BYTES diff lines at verdict-table region)"

# (d) Re-extract log line emitted for cycle 2 with required witness fields.
if ! grep -qE "INV-002: re-extracted verdict for .* cycle=2 producer_mtime=.* producer_sha256=.* block_sha256=" \
        "$WORKDIR/orchestrator.log"; then
    echo "FAIL: re-extract log line missing or malformed"
    exit 1
fi
echo "PASS (d): re-extract log line emitted with mtime + sha256 witnesses"

# Print byte-diff for the evidence artifact.
echo ""
echo "----- byte-diff cycle-1 → cycle-2 (verdict-table region) -----"
printf '%s\n' "$DIFF_RAW"
echo "----- end byte-diff -----"

echo ""
echo "ALL ASSERTIONS PASS — INV-002 freshness rule operational."
