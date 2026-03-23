#!/usr/bin/env bash
# run-fidelity-batch.sh — Run spec-fidelity checks across past releases
#
# Executes in 6 batches of 2 parallel jobs with 30s sleep between batches to stay within API rate limits.
# Each job uses fidelity-check-setup.sh --skip-gate-checks --run.
# Uses temporary files to prevent corruption during API errors.
#
# Usage:
#   ./scripts/run-fidelity-batch.sh
#   ./scripts/run-fidelity-batch.sh --dry-run   # setup only, no pipeline execution

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SETUP="$SCRIPT_DIR/fidelity-check-setup.sh"
BASE="/config/workspace/IronClaude/.dev/releases/complete"

MODE="${1:---run}"

echo "=== Fidelity Batch Runner (Rate-Limit Safe) ==="
echo "Mode: $MODE"
echo ""

# --- Delete existing spec-fidelity.md files ---
echo "Removing existing spec-fidelity.md files..."
for dir in \
  "$BASE/cleanup-audit-v2-UNIFIED-SPEC" \
  "$BASE/unified-audit-gating-v1.2.1" \
  "$BASE/unified-audit-gating-v2" \
  "$BASE/v2.24-cli-portify-cli-v4" \
  "$BASE/v2.24.1-cli-portify-cli-v5" \
  "$BASE/v2.24.2-Accept-Spec-Change" \
  "$BASE/v2.24.5-SpecFidelity" \
  "$BASE/v2.25.5-PreFlightExecutor" \
  "$BASE/v2.25.7-Phase8HaltFix" \
  "$BASE/v2.26-roadmap-v5" \
  "$BASE/v3.0_unified-audit-gating"; do
  rm -f "$dir/spec-fidelity.md"
done
echo "Done."

# --- Batch 1/6: 2 parallel ---
echo ""
echo "=== Batch 1/6 (2 parallel) ==="

"$SETUP" "$BASE/cleanup-audit-v2-UNIFIED-SPEC/cleanup-audit-v2-UNIFIED-SPEC.md"          "$BASE/cleanup-audit-v2-UNIFIED-SPEC/"           --skip-gate-checks "$MODE" &
"$SETUP" "$BASE/unified-audit-gating-v1.2.1/unified-spec-v1.0.md"                        "$BASE/unified-audit-gating-v1.2.1/"             --skip-gate-checks "$MODE" &

wait
echo ""
echo "=== Batch 1 complete ==="

# Wait 30 seconds for API cooldown
echo "Waiting 30 seconds for API cooldown..."
sleep 30

# --- Batch 2/6: 2 parallel ---
echo ""
echo "=== Batch 2/6 (2 parallel) ==="

"$SETUP" "$BASE/unified-audit-gating-v2/unified-audit-gating-v2.0-spec.md"               "$BASE/unified-audit-gating-v2/"                 --skip-gate-checks "$MODE" &
"$SETUP" "$BASE/v2.24-cli-portify-cli-v4/portify-release-spec.md"                        "$BASE/v2.24-cli-portify-cli-v4/"                --skip-gate-checks "$MODE" &

wait
echo ""
echo "=== Batch 2 complete ==="

# Wait 30 seconds for API cooldown
echo "Waiting 30 seconds for API cooldown..."
sleep 30

# --- Batch 3/6: 2 parallel ---
echo ""
echo "=== Batch 3/6 (2 parallel) ==="

"$SETUP" "$BASE/v2.24.1-cli-portify-cli-v5/portify-release-spec.md"                      "$BASE/v2.24.1-cli-portify-cli-v5/"              --skip-gate-checks "$MODE" &
"$SETUP" "$BASE/v2.24.2-Accept-Spec-Change/release-spec-accept-spec-change.md"           "$BASE/v2.24.2-Accept-Spec-Change/"              --skip-gate-checks "$MODE" &

wait
echo ""
echo "=== Batch 3 complete ==="

# Wait 30 seconds for API cooldown
echo "Waiting 30 seconds for API cooldown..."
sleep 30

# --- Batch 4/6: 2 parallel ---
echo ""
echo "=== Batch 4/6 (2 parallel) ==="

"$SETUP" "$BASE/v2.24.5-SpecFidelity/v2.25.1-release-spec.md"                            "$BASE/v2.24.5-SpecFidelity/"                    --skip-gate-checks "$MODE" &
"$SETUP" "$BASE/v2.25.5-PreFlightExecutor/sprint-preflight-executor-spec.md"              "$BASE/v2.25.5-PreFlightExecutor/"               --skip-gate-checks "$MODE" &

wait
echo ""
echo "=== Batch 4 complete ==="

# Wait 30 seconds for API cooldown
echo "Waiting 30 seconds for API cooldown..."
sleep 30

# --- Batch 5/6: 2 parallel ---
echo ""
echo "=== Batch 5/6 (2 parallel) ==="

"$SETUP" "$BASE/v2.25.7-Phase8HaltFix/v2.25.7-phase8-sprint-context-resilience-prd.md"   "$BASE/v2.25.7-Phase8HaltFix/"                   --skip-gate-checks "$MODE" &
"$SETUP" "$BASE/v2.26-roadmap-v5/v2.25-spec-merged.md"                                   "$BASE/v2.26-roadmap-v5/"                        --skip-gate-checks "$MODE" &

wait
echo ""
echo "=== Batch 5 complete ==="

# Wait 30 seconds for API cooldown
echo "Waiting 30 seconds for API cooldown..."
sleep 30

# --- Batch 6/6: 1 parallel ---
echo ""
echo "=== Batch 6/6 (1 parallel) ==="

"$SETUP" "$BASE/v3.0_unified-audit-gating/merged-spec.md"                                "$BASE/v3.0_unified-audit-gating/"                              "$MODE" &

wait
echo ""
echo "=== Batch 6 complete ==="

# --- Report ---
echo ""
echo "=== Results ==="
for dir in \
  "$BASE/cleanup-audit-v2-UNIFIED-SPEC" \
  "$BASE/unified-audit-gating-v1.2.1" \
  "$BASE/unified-audit-gating-v2" \
  "$BASE/v2.24-cli-portify-cli-v4" \
  "$BASE/v2.24.1-cli-portify-cli-v5" \
  "$BASE/v2.24.2-Accept-Spec-Change" \
  "$BASE/v2.24.5-SpecFidelity" \
  "$BASE/v2.25.5-PreFlightExecutor" \
  "$BASE/v2.25.7-Phase8HaltFix" \
  "$BASE/v2.26-roadmap-v5" \
  "$BASE/v3.0_unified-audit-gating"; do
  name="$(basename "$dir")"
  if [[ -f "$dir/spec-fidelity.md" ]]; then
    high=$(grep "^[[:space:]]*high_severity_count:" "$dir/spec-fidelity.md" 2>/dev/null | head -1 | sed 's/.*: *//' || echo "?")
    total=$(grep "^[[:space:]]*total_deviations:" "$dir/spec-fidelity.md" 2>/dev/null | head -1 | sed 's/.*: *//' || echo "?")
    ready=$(grep "^[[:space:]]*tasklist_ready:" "$dir/spec-fidelity.md" 2>/dev/null | head -1 | sed 's/.*: *//' || echo "?")
    printf "  %-45s high=%s total=%s ready=%s\n" "$name" "$high" "$total" "$ready"
  else
    printf "  %-45s MISSING (pipeline may have failed)\n" "$name"
  fi
done