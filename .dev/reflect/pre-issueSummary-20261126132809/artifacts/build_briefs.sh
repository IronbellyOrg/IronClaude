#!/usr/bin/env bash
# Builds the two Tier-2 reviewer briefs (Step 3B.0). Hunks are copied with sed from the real files, never retyped.
set -u -o pipefail
cd /home/coder/workspaces/worktrees/IronClaude/issue-834-rest || exit 1
ID=TASK-WF-issueSummary-20261126-132314
PKG=.dev/tasks/to-do/$ID
PLAN=$PKG/$ID.md
SPEC=$PKG/source.md
S=src/superclaude/skills/sc-issue-protocol
O=.dev/reflect/pre-issueSummary-20261126132809
CARD=$O/t1-card.md
STATE="codegraph run state: index_state=stale checked_at=2026-11-26T13:23:40Z worktree_root=$(pwd) projectPath=$(pwd)"

hunk() { # file start end lang
  printf '### %s:%s-%s\n\n```%s\n' "$1" "$2" "$3" "$4"
  sed -n "$2,$3p" "$1"
  printf '```\n\n'
}
section() { # heading text of a "## " section in the card
  awk -v h="$1" '$0==h{p=1;next} /^## /{p=0} p' "$CARD"
}
slice() { # ids regexp
  jq -r --arg re "$1" '.matrix[] | select(.requirement_id|test($re)) |
    "| \(.requirement_id) (\(.citation)) | Task \(.best_task) (best containment \(.best_ratio)) | \(if .match_method=="none" then "unmapped" else "covered" end) | \(.citation) |"' \
    $O/artifacts/coverage-matrix.json
}

# ---- reviewer 1: analyzer (haiku class) ----
{
  echo "## T1 card excerpt"; echo
  echo "Persona lens: analyzer (root-cause and deviation). This is a PRE-execution audit: the work under audit is the PLAN (plan_path below) and the driving spec is the SPEC (spec_path below). Find where the plan omits, contradicts or goes beyond the spec, and where a task as written cannot be carried out or cannot pass its own acceptance criteria. Ground every finding at file:line."
  echo; echo "spec_path: $(pwd)/$SPEC"; echo "plan_path: $(pwd)/$PLAN"; echo "diff_scope: none (pre-execution)"
  echo; section "## Root-cause / deviation findings"
  echo; echo "## Grounding hunks"; echo; echo "$STATE"; echo
  hunk $S/refs/create.md 84 86 markdown
  hunk $S/refs/create.md 38 38 markdown
  hunk $S/refs/create.md 57 59 markdown
  hunk $S/templates/draft-notes.md 1 15 markdown
  hunk tests/skills/test_issue_protocol.py 1337 1347 python
  hunk tests/skills/test_issue_protocol.py 1365 1381 python
  hunk $PLAN 17 26 markdown
  hunk $PLAN 43 83 markdown
  hunk $PLAN 85 115 markdown
  hunk $PLAN 117 161 markdown
  echo "## Coverage slice"; echo
  echo "| Requirement / Task | Card ID | Status | Grounding |"; echo "|---|---|---|---|"
  slice 'INF-00[2-7]'
} > $O/reviewer-briefs/reviewer-1.md

# ---- reviewer 2: qa (opus class) ----
{
  echo "## T1 card excerpt"; echo
  echo "Persona lens: qa (coverage and acceptance). This is a PRE-execution audit: the work under audit is the PLAN and the driving spec is the SPEC. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check that each task's acceptance criteria can actually be passed or failed as written."
  echo; echo "spec_path: $(pwd)/$SPEC"; echo "plan_path: $(pwd)/$PLAN"; echo "diff_scope: none (pre-execution)"
  echo; section "## Coverage / acceptance findings"
  echo; echo "## Grounding hunks"; echo; echo "$STATE"; echo
  n=$(wc -l < $SPEC); hunk $SPEC 1 "$n" markdown
  n=$(wc -l < $PLAN); hunk $PLAN 1 "$n" markdown
  hunk $S/refs/create.md 84 86 markdown
  echo "## Coverage slice"; echo
  echo "| Requirement / Task | Card ID | Status | Grounding |"; echo "|---|---|---|---|"
  slice 'INF-0'
} > $O/reviewer-briefs/reviewer-2.md

echo "briefs: $(ls $O/reviewer-briefs | wc -l)"; wc -l $O/reviewer-briefs/*.md
grep -c '^## ' $O/reviewer-briefs/reviewer-1.md $O/reviewer-briefs/reviewer-2.md
