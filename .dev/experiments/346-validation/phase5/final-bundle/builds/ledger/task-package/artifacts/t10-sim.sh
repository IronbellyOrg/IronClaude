#!/usr/bin/env bash
# Run the ledger-step command lines (L0-init, L-find-close, L-begin, L-verify-close, L-sweep-prepare/ingest)
# against a scratch repo in a new temp folder. Prints each command's JSON; exits non-zero on the first failure.
set -euo pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/bs346-ledger
RL="uv run --no-project python $REPO/src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py"
W=$(mktemp -d /tmp/bs346-sim.XXXXXX)
trap 'rm -rf "$W"' EXIT
cd "$W"
mkdir -p .dev/orca-command-refactor/specs .dev/orca-command-refactor/review
SPEC=.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
LED=.dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger
cp "$REPO/tests/skills/fixtures/review-ledger/doc-r1.md" "$SPEC"
seq() { $RL status --ledger "$LED" | uv run --no-project python -c 'import json,sys; print(json.load(sys.stdin)["seq"])'; }
echo "## L0-init"; $RL init --doc "$SPEC" --profile spec-panel --ledger "$LED" --op sim-init
R1=.dev/orca-command-refactor/review/spec-panel.md
{ echo "# Review 1"; echo; echo '```ledger-input'; cat "$REPO/tests/skills/fixtures/review-ledger/find-basic.json"; echo '```'; } > "$R1"
echo "## L-find-close"
$RL find --ledger "$LED" --input "$R1" --op sim-r1-find --expect-seq "$(seq)"
$RL close --ledger "$LED" --report "$R1" --op sim-r1-close --expect-seq "$(seq)"
set +e; $RL verdict --ledger "$LED"; echo "verdict exit $?"; set -e
echo "## T06 stand-in: reviser edits R1's paragraph and one unrelated line"
cp "$REPO/tests/skills/fixtures/review-ledger/doc-r2-fix.md" "$SPEC"
sed -i 's/The cache is refreshed every hour./The cache is refreshed every ten minutes./' "$SPEC"
echo "## L-begin"
$RL begin --ledger "$LED" --doc "$SPEC" --revert-unclaimed --op sim-r2-begin --expect-seq "$(seq)"
R2=.dev/orca-command-refactor/review/spec-panel-round2.md
{ echo "# Review 2"; echo; echo '```ledger-input'
  echo '{"answers": [{"row": "R1", "result": "resolved", "evidence": "the caller retries at most twice", "touched_ok": "yes"},'
  echo ' {"row": "R2", "result": "open", "evidence": "The service rejects a widget without an owner.", "touched_ok": "yes", "reason": "not fixed"},'
  echo ' {"row": "R3", "result": "open", "evidence": "The service keeps deleted widgets for 30 days.", "touched_ok": "yes", "reason": "not fixed"}]}'
  echo '```'; } > "$R2"
echo "## L-verify-close"
$RL verify --ledger "$LED" --input "$R2" --dry-run
$RL verify --ledger "$LED" --input "$R2" --op sim-r2-verify --expect-seq "$(seq)"
$RL close --ledger "$LED" --report "$R2" --op sim-r2-close --expect-seq "$(seq)"
set +e; $RL verdict --ledger "$LED"; echo "verdict exit $?"; set -e
echo "## T08 stand-in: no edits; L-begin; T09 stand-in answers; L-verify-close"
$RL begin --ledger "$LED" --doc "$SPEC" --revert-unclaimed --op sim-r3-begin --expect-seq "$(seq)"
R3=.dev/orca-command-refactor/review/spec-panel-round3.md
{ echo "# Review 3"; echo; echo '```ledger-input'
  echo '{"answers": [{"row": "R2", "result": "open", "evidence": "The service rejects a widget without an owner.", "touched_ok": "yes", "reason": "x"},'
  echo ' {"row": "R3", "result": "open", "evidence": "The service keeps deleted widgets for 30 days.", "touched_ok": "yes", "reason": "x"}]}'
  echo '```'; } > "$R3"
$RL verify --ledger "$LED" --input "$R3" --op sim-r3-verify --expect-seq "$(seq)"
$RL close --ledger "$LED" --report "$R3" --op sim-r3-close --expect-seq "$(seq)"
set +e; $RL verdict --ledger "$LED"; echo "verdict exit $?"; set -e
echo "## L-sweep-prepare"
$RL sweep --ledger "$LED" --prepare --op sim-sweep-prepare --expect-seq "$(seq)"
SW=.dev/orca-command-refactor/review/spec-panel-sweep.md
{ echo "# Sweep"; echo; echo '```ledger-input'; echo '{"rows": []}'; echo '```'; } > "$SW"
echo "## L-sweep-ingest"
$RL sweep --ledger "$LED" --input "$SW" --report "$SW" --op sim-sweep --expect-seq "$(seq)"
set +e; $RL verdict --ledger "$LED"; echo "verdict exit $?"; set -e
echo "## tails"; tail -n 1 "$R1" "$R2" "$R3" "$SW"
echo "unclaimed edit still in spec (0 = reverted by begin --revert-unclaimed): $(grep -c "every ten minutes" "$SPEC" || true)"
echo "SIM OK"
