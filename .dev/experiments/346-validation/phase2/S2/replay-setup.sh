#!/usr/bin/env bash
# Place the recorded S2 inputs for one review round into a replay worktree and print the review command.
# usage: replay-setup.sh <replay-worktree-root> <round 1|2|3>
# It only copies files into <root>/.dev/ (and /tmp for the two spec files, never overwriting). It does not run any review.
set -u -o pipefail
ROOT=${1:?replay worktree root}; R=${2:?round 1|2|3}
HERE=$(cd "$(dirname "$0")" && pwd); IN=$HERE/inputs
case $R in
  1) ID=20261101-225635 ;;
  2) ID=20261102-042031 ;;
  3) ID=20261102-053741 ;;
  *) echo "round must be 1, 2 or 3" >&2; exit 2 ;;
esac
PKG_REL=.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-$ID
PLAN=TASK-WF-removeTheAnyIssu-$ID.md
mkdir -p "$ROOT/$PKG_REL" "$ROOT/.dev/review-severity-rule" "$ROOT/.dev/qa-loop-investigation" /tmp
cp -n "$IN/common/t11-severity-rule-spec.md" /tmp/t11-severity-rule-spec.md
cp -n "$IN/common/t11b-severity-rule-restart-spec.md" /tmp/t11b-severity-rule-restart-spec.md
cp "$IN/common/FINDINGS-qa-loop-investigation.md" "$ROOT/.dev/qa-loop-investigation/FINDINGS.md"
cp "$IN/round$R/$PLAN" "$ROOT/$PKG_REL/$PLAN"
cp "$IN/round$R/source.md" "$ROOT/$PKG_REL/source.md"
cp "$IN/round$R/inventory.md" "$ROOT/.dev/review-severity-rule/inventory.md"
[ -f "$IN/round$R/cap-sites.md" ] && cp "$IN/round$R/cap-sites.md" "$ROOT/.dev/review-severity-rule/cap-sites.md"
[ -f "$IN/round$R/cap-edits.yaml" ] && cp "$IN/round$R/cap-edits.yaml" "$ROOT/.dev/review-severity-rule/cap-edits.yaml"
# Path-only rewrite of the PLACED copies (inputs/ stays byte-exact): the original worktree no longer exists.
OLD_WT=/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule
OLD_QA=/home/coder/workspaces/IronClaude/.dev/worktrees/qa-loop-investigation/.dev/qa-loop-investigation
for f in "$ROOT/$PKG_REL/$PLAN" "$ROOT/$PKG_REL/source.md" "$ROOT/.dev/review-severity-rule/inventory.md"; do
  sed -i -e "s#$OLD_WT#$ROOT#g" -e "s#$OLD_QA#$ROOT/.dev/qa-loop-investigation#g" "$f"
done
echo "placed round $R inputs under $ROOT (absolute paths rewritten from $OLD_WT)"
echo "review command (run it yourself in a session whose cwd is $ROOT):"
echo "  /sc:reflect --mode pre --spec $ROOT/$PKG_REL/source.md --tasklist $ROOT/$PKG_REL/$PLAN"
