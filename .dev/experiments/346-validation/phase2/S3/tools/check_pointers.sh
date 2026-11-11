#!/usr/bin/env bash
# Re-check the file:line pointers quoted in ANALYSIS.md and REPLAY.md.
# Usage (from the S3 package root): bash tools/check_pointers.sh
# Each check: the given line of the given file must contain the given text.
set -u -o pipefail
fail=0; n=0
chk() { # file line text
  n=$((n+1))
  if sed -n "${2}p" "$1" 2>/dev/null | grep -qF -- "$3"; then :; else echo "FAIL $1:$2 does not contain: $3"; fail=$((fail+1)); fi
}
R=baseline/reviews; P=baseline/plans; B=briefs
chk $R/plan-review.md 5 "Verdict: FAIL";  chk $R/plan-review.md 7 "Blocking findings: 8"; chk $R/plan-review.md 8 "Minor findings: 14"; chk $R/plan-review.md 73 "B-1 (BLOCKING)"
chk $R/plan-review-2.md 5 "Verdict: FAIL"; chk $R/plan-review-2.md 7 "Blocking findings: 8"; chk $R/plan-review-2.md 8 "Minor findings: 12"
for p in "46 F-1" "70 F-2" "87 F-3" "101 F-4" "121 F-5" "131 F-6" "144 F-7" "155 F-8"; do set -- $p; chk $R/plan-review-2.md $1 "### $2 (BLOCKING)"; done
chk $R/plan-review-3.md 5 "Verdict: FAIL"; chk $R/plan-review-3.md 7 "Blocking findings: 10"; chk $R/plan-review-3.md 8 "Minor findings: 11"
for p in "186 B-1" "202 B-2" "214 B-3" "230 B-4" "236 B-5" "246 B-6" "252 B-7" "258 B-8" "264 B-9" "270 B-10"; do set -- $p; chk $R/plan-review-3.md $1 "### $2."; done
chk $R/plan-review-3.md 131 "4.2 Is"; chk $R/plan-review-3.md 133 "Usable, with friction"
chk $P/refactor-plan.v0.md 192 "**N2.**"; chk $P/refactor-plan.v0.md 194 "**N4.**"; chk $P/refactor-plan.v0.md 210 "**G2.**"; chk $P/refactor-plan.v0.md 218 "**G4.**"; chk $P/refactor-plan.v1.md 234 "PR titles"; chk $P/refactor-plan.v0.md 421 'Pinned gaps'
chk $P/refactor-plan.v1.md 197 "NM2:"; chk $P/refactor-plan.v2.md 209 "Segments and words"
chk $B/R1-reviewer-L919.md 14 "GRADE each finding BLOCKING"; chk $B/R2-reviewer-L975.md 12 "Grade each finding BLOCKING"; chk $B/R3-reviewer-L1032.md 14 "Grade each finding BLOCKING"
chk $B/R3-reviewer-L1032.md 8 "at least 25 NEW attacks"; chk $B/R2-reviewer-L975.md 6 "For each of B-1..B-8"; chk $B/R3-reviewer-L1032.md 1 "THIRD and FINAL"
chk $B/R1-reviser-fix-cycle-1-L947.md 1 "fix cycle 1 of 2"; chk $B/R1-reviser-fix-cycle-1-L947.md 5 "STEERING"; chk $B/R1-reviser-fix-cycle-1-L947.md 12 "Minor findings"
chk $B/R2-reviser-fix-cycle-2-L1000.md 1 "the last allowed"; chk $B/R2-reviser-fix-cycle-2-L1000.md 5 "STEERING"; chk $B/R2-reviser-fix-cycle-2-L1000.md 11 "m-1..m-12"; chk $B/R2-reviser-fix-cycle-2-L1000.md 12 "PROTOTYPE AND REGRESSION CORPUS"
chk /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase1/REPORT.md 10 "I2 | Review-severity-rule plan"
chk /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase1/REPORT.md 11 "I3 | Launch-level hook plan"
chk /home/coder/workspaces/worktrees/IronClaude/exp346-p1-tasklists/.dev/experiments/346-validation/phase1/REPORT.md 101 "## I3: Orca"
chk /home/coder/workspaces/worktrees/IronClaude/exp346-p1-tasklists/.dev/experiments/346-validation/phase1/REPORT.md 247 "Biggest obstacle"
chk /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md 12 "S3 review-severity-rule plan"
echo "checked $n pointers, $fail failed"
[ "$fail" -eq 0 ]
