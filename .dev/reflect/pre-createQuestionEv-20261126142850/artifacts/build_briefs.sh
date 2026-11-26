#!/usr/bin/env bash
# Builds the two Tier-2 reviewer briefs for the second review (Step 3B.0). Hunks are copied with sed, never retyped.
set -u -o pipefail
cd /home/coder/workspaces/worktrees/IronClaude/issue-834-rest || exit 1
ID=TASK-WF-createQuestionEv-20261126-142533
PKG=.dev/tasks/to-do/$ID
PLAN=$PKG/$ID.md
SPEC=$PKG/source.md
S=src/superclaude/skills/sc-issue-protocol
O=$(cat /tmp/reflect2-out.txt)
CARD=$O/t1-card.md
STATE="codegraph run state: index_state=stale checked_at=2026-11-26T13:23:40Z worktree_root=$(pwd) projectPath=$(pwd)"

hunk() { printf '### %s:%s-%s\n\n```%s\n' "$1" "$2" "$3" "$4"; sed -n "$2,$3p" "$1"; printf '```\n\n'; }
section() { awk -v h="$1" '$0==h{p=1;next} /^## /{p=0} p' "$CARD"; }
slice() { jq -r --arg re "$1" '.matrix[] | select(.requirement_id|test($re)) |
    "| \(.requirement_id) (\(.citation)) | \(if .source=="parsed" then (if (.matched_task_ids|length)>0 then "Task " + (.matched_task_ids|map(tostring)|join(", Task ")) else "none" end) else "Task \(.best_task) (best containment \(.best_ratio))" end) | \(if .match_method=="none" then "unmapped" else "covered" end) | \(.citation) |"' \
    $O/artifacts/coverage-matrix.json; }

{
  echo "## T1 card excerpt"; echo
  echo "Persona lens: analyzer (root-cause and deviation). This is a PRE-execution audit: the work under audit is the PLAN (plan_path below) and the driving spec is the SPEC (spec_path below). Find where the plan omits, contradicts or goes beyond the spec, and where a task as written cannot be carried out or cannot pass its own acceptance criteria. The spec's 'Revision 1' section lists findings of an earlier review that the plan must not repeat: check the plan against each of them as well. Ground every finding at file:line."
  echo; echo "spec_path: $(pwd)/$SPEC"; echo "plan_path: $(pwd)/$PLAN"; echo "diff_scope: none (pre-execution)"
  echo; section "## Root-cause / deviation findings"
  echo; echo "## Grounding hunks"; echo; echo "$STATE"; echo
  hunk $S/refs/create.md 84 86 markdown
  hunk $S/refs/create.md 38 38 markdown
  hunk $S/refs/create.md 57 59 markdown
  hunk $S/templates/draft-notes.md 1 15 markdown
  hunk tests/skills/test_issue_protocol.py 1337 1347 python
  hunk tests/skills/test_issue_protocol.py 1365 1381 python
  hunk $PLAN 17 27 markdown
  hunk $PLAN 31 90 markdown
  hunk $PLAN 92 133 markdown
  hunk $PLAN 134 183 markdown
  echo "## Coverage slice"; echo
  echo "| Requirement / Task | Card ID | Status | Grounding |"; echo "|---|---|---|---|"
  slice '^INF-'
} > $O/reviewer-briefs/reviewer-1.md

{
  echo "## T1 card excerpt"; echo
  echo "Persona lens: qa (coverage and acceptance). This is a PRE-execution audit: the work under audit is the PLAN and the driving spec is the SPEC. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check that each task's acceptance criteria can actually be passed or failed as written, and check the plan against each item of the spec's 'Revision 1' section (findings of an earlier review that the plan must not repeat)."
  echo; echo "spec_path: $(pwd)/$SPEC"; echo "plan_path: $(pwd)/$PLAN"; echo "diff_scope: none (pre-execution)"
  echo; section "## Coverage / acceptance findings"
  echo; echo "## Grounding hunks"; echo; echo "$STATE"; echo
  n=$(wc -l < $SPEC); hunk $SPEC 1 "$n" markdown
  n=$(wc -l < $PLAN); hunk $PLAN 1 "$n" markdown
  hunk $S/refs/create.md 84 86 markdown
  echo "## Coverage slice"; echo
  echo "| Requirement / Task | Card ID | Status | Grounding |"; echo "|---|---|---|---|"
  slice '.'
} > $O/reviewer-briefs/reviewer-2.md
wc -l $O/reviewer-briefs/*.md
for f in $O/reviewer-briefs/reviewer-*.md; do echo "$f:"; awk '/^```/{x=!x} !x && /^## /' $f; done
