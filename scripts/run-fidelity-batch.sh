#!/usr/bin/env bash
# run-fidelity-batch.sh — Run spec-fidelity checks across past releases
#
# Executes in batches of 2 parallel jobs with 60s cooldown between batches
# to stay within API rate limits. Each job uses fidelity-check-setup.sh.
#
# Excluded:
#   unified-audit-gating-v1.2.1 — duplicate H3 headings fail MERGE_GATE
#     semantic check; cannot be bypassed without modifying content or pipeline code.
#
# Usage:
#   ./scripts/run-fidelity-batch.sh
#   ./scripts/run-fidelity-batch.sh --dry-run   # setup only, no pipeline execution

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SETUP="$SCRIPT_DIR/fidelity-check-setup.sh"
BASE="/config/workspace/IronClaude/.dev/releases/complete"

MODE="${1:---run}"
BATCH_SIZE=2
COOLDOWN=60

echo "=== Fidelity Batch Runner ==="
echo "Mode: $MODE | Parallel: $BATCH_SIZE | Cooldown: ${COOLDOWN}s"
echo ""

# --- All releases to process (10 total, 5 batches of 2) ---
RELEASES=(
  "cleanup-audit-v2-UNIFIED-SPEC|cleanup-audit-v2-UNIFIED-SPEC.md|--skip-gate-checks"
  "unified-audit-gating-v2|unified-audit-gating-v2.0-spec.md|--skip-gate-checks"
  "v2.24-cli-portify-cli-v4|portify-release-spec.md|--skip-gate-checks"
  "v2.24.1-cli-portify-cli-v5|portify-release-spec.md|--skip-gate-checks"
  "v2.24.2-Accept-Spec-Change|release-spec-accept-spec-change.md|--skip-gate-checks"
  "v2.24.5-SpecFidelity|v2.25.1-release-spec.md|--skip-gate-checks"
  "v2.25.5-PreFlightExecutor|sprint-preflight-executor-spec.md|--skip-gate-checks"
  "v2.25.7-Phase8HaltFix|v2.25.7-phase8-sprint-context-resilience-prd.md|--skip-gate-checks"
  "v2.26-roadmap-v5|v2.25-spec-merged.md|--skip-gate-checks"
  "v3.0_unified-audit-gating|merged-spec.md|"
)

echo "Excluded: unified-audit-gating-v1.2.1 (duplicate H3 headings fail MERGE_GATE)"
echo ""

# --- Delete existing spec-fidelity.md files ---
echo "Removing existing spec-fidelity.md files..."
for entry in "${RELEASES[@]}"; do
  dir="${entry%%|*}"
  rm -f "$BASE/$dir/spec-fidelity.md"
done
echo "Done."

# --- Run in batches ---
total=${#RELEASES[@]}
batch_num=0

for ((i=0; i<total; i+=BATCH_SIZE)); do
  batch_num=$((batch_num + 1))
  end=$((i + BATCH_SIZE))
  if [[ $end -gt $total ]]; then end=$total; fi
  count=$((end - i))

  echo ""
  echo "=== Batch $batch_num ($count parallel) ==="

  pids=()
  for ((j=i; j<end; j++)); do
    entry="${RELEASES[$j]}"
    IFS='|' read -r dir spec flags <<< "$entry"

    echo "  Starting: $dir"
    if [[ -n "$flags" ]]; then
      "$SETUP" "$BASE/$dir/$spec" "$BASE/$dir/" $flags "$MODE" &
    else
      "$SETUP" "$BASE/$dir/$spec" "$BASE/$dir/" "$MODE" &
    fi
    pids+=($!)
  done

  # Wait for all jobs in this batch
  batch_failed=false
  for pid in "${pids[@]}"; do
    if ! wait "$pid"; then
      batch_failed=true
    fi
  done

  echo "=== Batch $batch_num complete$([ "$batch_failed" = true ] && echo " (some jobs failed)") ==="

  # Cooldown between batches (skip after last batch)
  if [[ $end -lt $total ]]; then
    echo "Cooling down ${COOLDOWN}s..."
    sleep "$COOLDOWN"
  fi
done

# --- Report ---
echo ""
echo "=== Results ==="
for entry in "${RELEASES[@]}"; do
  dir="${entry%%|*}"
  if [[ -f "$BASE/$dir/spec-fidelity.md" ]]; then
    high=$(grep "^[[:space:]]*high_severity_count:" "$BASE/$dir/spec-fidelity.md" 2>/dev/null | head -1 | sed 's/.*: *//' || echo "?")
    total_dev=$(grep "^[[:space:]]*total_deviations:" "$BASE/$dir/spec-fidelity.md" 2>/dev/null | head -1 | sed 's/.*: *//' || echo "?")
    ready=$(grep "^[[:space:]]*tasklist_ready:" "$BASE/$dir/spec-fidelity.md" 2>/dev/null | head -1 | sed 's/.*: *//' || echo "?")
    printf "  %-45s high=%-3s total=%-3s ready=%s\n" "$dir" "$high" "$total_dev" "$ready"
  else
    printf "  %-45s MISSING\n" "$dir"
  fi
done

# Also note the excluded release
echo ""
echo "  (excluded: unified-audit-gating-v1.2.1 — duplicate H3 headings)"
