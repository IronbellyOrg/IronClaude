#!/usr/bin/env bash
# Confirming test of the wonsol panel, step 1 (owner order 2026-11-17): a FRESH Sonnet session writes ground truth for NEW plans
# (none of HO-2, HO-3, HX-1, HX-3, the three study packages, nor any plan about the blocker/severity work). Opus is not used.
# The session sees only the plan folders, their earlier review reports and git history; it writes only under $OUT.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
W=$REPO/.dev/eval-workspaces/tasklist-review-panel
OUT=$W/20261117-confirm/author-out
SLOT=$W/20261114-collab-process/with-slot.sh
mkdir -p "$OUT" /tmp/cf-author2
D=$REPO/.dev/tasks/done
R=$REPO/.dev/reflect
PROMPT="You are the independent ground-truth author for a review-panel evaluation. You have never seen any review recipe, checklist or earlier result, and you must not look for any. Your job: from the ten CANDIDATE plans below pick the FOUR best ones and, for each, write a ground-truth file listing the real plan defects that are already documented by earlier independent reviews, and a package record telling the harness how to rebuild the repository as it was before the plan was implemented.

CANDIDATES (plan folder under $D : earlier review report folder under $R)
C1 : TASK-WF-detachTheCcsessi-20261102-034618 : pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow01
C2 : TASK-WF-addTheSharedCode-20261111-193909 : pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04
C3 : TASK-WF-authorizedNarrow-20261106-214325 : pre-TASK-WF-authorizedNarrow-20261106-214325-shadow06
C4 : TASK-WF-implementFrOnb1O-20261023-180618 : pre-TASK-WF-implementFrOnb1O-20261023-180618-shadow10
C5 : TASK-WF-devGuideFenceFix-20261104-204854 : pre-TASK-WF-devGuideFenceFix-20261104-204854-shadow12
C6 : TASK-WF-fixIssue412SVeri-20261106-215543 : pre-TASK-WF-fixIssue412SVeri-20261106-215543-shadow13
C7 : TASK-WF-designOutput-20261111-193642 : pre-TASK-WF-designOutput-20261111-193642-shadow14
C8 : TASK-WF-analyzeCodegraph-20261111-193557 : pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15
C9 : TASK-WF-planTheExplicitl-20261110-024937 : pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08
C10 : TASK-WF-brainstormFixBri-20261106-113538 : pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956 (its folder names contain the word brainstorm; that word is allowed ONLY inside these two paths)
Each plan folder holds the plan (<folder name>.md), source.md (what the plan must implement), progress.md and artifacts/ (implementation-time review records, e.g. artifacts/retries/*/review-*.md with severity markers). Each report folder holds REPORT.md and related files.

SELECTION RULE. A candidate is usable only if the plan file in its folder is the SAME text the earlier report reviewed (the report cites plan lines, quotes or a plan hash; check that cited lines exist and say what the report says). Earlier attempts of this kind lost two of four documents because the repository's plan was a later, already-fixed version of the reviewed text: reject those. A report folder named \"shadow\" reviewed the plan as it stands in the done folder, so those are the likeliest to match. Among usable candidates prefer the ones with 5 to 12 verified plan defects, and at least two with one or more blocking defects. Stop when you have four usable documents (more than four is not wanted); if fewer than four are usable, deliver what you have and say so. Name them NP-2, NP-3, NP-4, NP-5 in the order you finish them (NP-1 already exists).

ALLOWED to read: the ten plan folders, their review report folders (and files next to them), and git history of this repository (git log, git show, git cat-file, git rev-list) from $REPO. FORBIDDEN, no exceptions: any path containing recipe, recipes, cards, brief, sweep, ledger, derivation, collab, severity, brainstorm, 20261111-a1, 20261113, 20261114, 20261116, 20261117 (except your own output folder), ground-truth, holdout-gt, or stronger; any file under .dev/eval-workspaces other than your output folder; do not run the repository's tests or any model. You write ONLY under $OUT.

OUTPUT per chosen document NP-n, in $OUT/NP-n/:
1. candidate.md : an exact byte copy of the plan file (cp).
2. source.md : an exact copy of that plan's source.md (cp).
3. ground-truth.json : {\"doc_id\":\"NP-n\",\"plan\":\"<plan folder name>\",\"items\":[ ... ]}. One item per real plan defect, at most 12 per document, each item: {\"id\":\"GT1\" (GT1, GT2, ... in order),\"class\":\"unassigned\",\"blocking_in_implement\":true|false,\"description\":\"2 to 4 sentences: what an implementer who follows the plan as written would build wrongly, and the correct outcome\",\"plan_quote\":\"a contiguous quote of 40 to 200 characters copied EXACTLY from candidate.md that anchors the defect\",\"evidence\":\"the report finding id and file:line you derived it from\"}. blocking_in_implement is true only when the earlier review report marks the finding blocking, or an implementation-time review record under artifacts/ shows it was graded blocking while the plan was implemented; otherwise false. Include only defects of the PLAN text (what the plan says or omits relative to source.md and the repository at the time). Exclude: defects of code written during implementation, style or wording nits, findings the report itself marks as unfounded or not reproduced, and anything whose quote you cannot find verbatim in candidate.md.
4. package.json : {\"base\":\"<40-hex commit>\",\"candidate\":\"<repo-relative path of the plan file under .dev/tasks/done/...>\",\"source\":\"<repo-relative path of its source.md>\",\"kind\":\"plan\",\"set\":\"confirm\",\"masked_paths\":[...]} . base = the commit of the repository just BEFORE this plan was implemented: take it from the first 'start sha=' line of progress.md, and verify with git cat-file -t that it is a commit that contains the repository state the plan was written against; masked_paths = repository files that the implementation CREATED (they must not exist in the sandbox) and that already exist at base, normally none (use [] when none; list only paths you verified with git ls-tree at base). If the base commit lacks files the plan edits, that candidate is unusable.
5. notes.md : findings you dropped and why, and anything that could not be verified.
Also write $OUT/SUMMARY.md: a table candidate | NP id | usable yes/no and why | items | blocking items | dropped findings. Then reply with only that table. Be strict: a smaller verified set is better than a larger doubtful one; never invent a defect, and never copy a quote from memory."
S=$(date +%s)
( cd /tmp/cf-author2 && bash "$SLOT" cf-author2 timeout 7200 claude -p --model claude-sonnet-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$OUT/session.json" 2>"$OUT/session.err"
echo "END author rc=$? wall=$(( $(date +%s)-S ))s summary=$( [ -s $OUT/SUMMARY.md ] && echo yes || echo no )"
