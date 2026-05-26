#!/usr/bin/env bash
# D-0032 — T03.08 missing-verdict fixture
#
# Demonstrates the halt-A.10-before-A.10.5 lever:
#   Scenario A: rf-qa report file is absent on disk        → HALT
#   Scenario B: rf-qa report exists but has no VERDICT line → HALT
#   Scenario C: rf-qa report exists with VERDICT: PASS     → A.10.5 proceeds
#
# This is a textual / behavioral simulation, not an executable orchestrator
# call. The orchestrator IS the skill prompt; this fixture exercises the
# pieces a real orchestrator would compute (file-existence + grep) against
# three synthetic producer states, asserting the prompt's halt directive
# would fire in A and B but not C.

set -euo pipefail

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT
SKILL_MD="src/superclaude/skills/task-builder/SKILL.md"

# Sanity: the halt branch must be present in the skill.
if ! grep -q 'No verdict emitted (report file absent OR present but no `VERDICT:` line OR' "$SKILL_MD"; then
  echo "FAIL: halt-branch directive missing from $SKILL_MD"
  exit 1
fi
if ! grep -q 'halt-A.10-before-A.10.5' "$SKILL_MD"; then
  echo "FAIL: halt lever identifier missing from $SKILL_MD"
  exit 1
fi

echo "=== Scenario A: report absent ==="
TASK_A="$WORKDIR/task-A"
mkdir -p "$TASK_A/qa"
# (no qa-task-validation-report.md written)
REPORT_A="$TASK_A/qa/qa-task-validation-report.md"
if [[ -f "$REPORT_A" ]]; then
  echo "FAIL (a-1): scenario expected absent report"
  exit 1
fi
# Halt directive sub-step (a): missing-file check
echo "PASS (a-1) report-absence detected — orchestrator would emit INV-002-no-producer-artifact halt-A.10-before-A.10.5 and STOP before A.10.5"

echo "=== Scenario B: report present, no VERDICT line ==="
TASK_B="$WORKDIR/task-B"
mkdir -p "$TASK_B/qa"
REPORT_B="$TASK_B/qa/qa-task-validation-report.md"
cat > "$REPORT_B" <<'EOF'
# qa-task-validation-report — TASK-FIXTURE-MISSING-VERDICT

## Items Reviewed
| Item | Description | Status | Notes |
|------|-------------|--------|-------|
| 1    | Frontmatter | PASS   | well-formed |
| 2    | Sections    | PASS   | all present |

## Notes
Report truncated mid-write; no verdict reached.
EOF
if [[ ! -f "$REPORT_B" ]]; then
  echo "FAIL (b-1) fixture failed to write report"
  exit 1
fi
echo "PASS (b-1) report-present detected"
if grep -E '^VERDICT: (PASS|FAIL)$' "$REPORT_B" > /dev/null; then
  echo "FAIL (b-2) unexpected VERDICT line in malformed-report fixture"
  exit 1
fi
echo "PASS (b-2) no-VERDICT-line detected — orchestrator would emit INV-002-no-verdict-line halt-A.10-before-A.10.5 and STOP before A.10.5"

echo "=== Scenario C: report present, VERDICT: PASS — control-case ==="
TASK_C="$WORKDIR/task-C"
mkdir -p "$TASK_C/qa"
REPORT_C="$TASK_C/qa/qa-task-validation-report.md"
cat > "$REPORT_C" <<'EOF'
# qa-task-validation-report — TASK-FIXTURE-GOOD-VERDICT

## Items Reviewed
| Item | Description | Status | Notes |
|------|-------------|--------|-------|
| 1    | Frontmatter | PASS   | well-formed |
| 2    | Sections    | PASS   | all present |

VERDICT: PASS
EOF
if ! grep -E '^VERDICT: (PASS|FAIL)$' "$REPORT_C" > /dev/null; then
  echo "FAIL (c-1) control-case fixture missing VERDICT line"
  exit 1
fi
echo "PASS (c-1) well-formed VERDICT line detected — orchestrator would route via 'Handling the verdict' branch 1 (PASS) and proceed to A.10.5"

echo ""
echo "=== ANTI-INFLATION BYTE-STABILITY CHECK ==="
EXPECTED_SHA="0570c6b474686734d8a69e62adcd825d3c0b3e421ef4a12ef114703d1deec59c"
SRC_SHA="$(sed -n '766,775p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum | cut -d' ' -f1)"
CLAUDE_SHA="$(sed -n '766,775p' .claude/agents/rf-qa-qualitative.md | sha256sum | cut -d' ' -f1)"
if [[ "$SRC_SHA" != "$EXPECTED_SHA" ]] || [[ "$CLAUDE_SHA" != "$EXPECTED_SHA" ]]; then
  echo "FAIL: anti-inflation block sha256 mismatch"
  echo "  expected: $EXPECTED_SHA"
  echo "  src:      $SRC_SHA"
  echo "  .claude:  $CLAUDE_SHA"
  exit 1
fi
echo "PASS: rf-qa-qualitative.md:766-775 byte-identical in both src and .claude (sha256 $EXPECTED_SHA)"

echo ""
echo "ALL ASSERTIONS PASS — halt-A.10-before-A.10.5 lever operational, anti-inflation block byte-stable."
