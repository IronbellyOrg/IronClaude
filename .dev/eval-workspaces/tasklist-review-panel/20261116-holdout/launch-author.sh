#!/usr/bin/env bash
# Frozen hold-out comparison, step 2 (owner order 2026-11-16): a FRESH Sonnet session writes the hold-out documents' ground truth.
# It runs in an empty folder, must not read anything of Recipe Ledger, Sweep Sheet, the collaboration designs or the study packages,
# and writes only under $OUT. RL freeze tag rl-freeze-1553f5dd29b1 exists before this runs (REQ-33). Opus is not used.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
W=$REPO/.dev/eval-workspaces/tasklist-review-panel
OUT=$W/20261116-holdout/author-out
SLOT=$W/20261114-collab-process/with-slot.sh
mkdir -p "$OUT" /tmp/ho-author
D=$REPO/.dev/tasks/done
R=$REPO/.dev/reflect
PROMPT="You are the independent ground-truth author for a review-panel evaluation. You have never seen any review recipe, checklist or earlier result, and you must not look for any. Your job: for each of four implementation plans, write a ground-truth file listing the real plan defects that are already documented by earlier independent reviews, and a package record telling the harness how to rebuild the repository as it was before the plan was implemented.

THE FOUR DOCUMENTS (id : plan folder : earlier review report)
HO-1 : $D/TASK-WF-workerContractFo-20261106-214402 : $R/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/REPORT.md (findings M-1..M-11; docs-only plan)
HO-2 : $D/TASK-WF-implementIronbel-20261104-130647 : $R/pre-TASK-WF-implementIronbel-20261104-130647-20261104130837/REPORT.md (blocking B-1..B-4 plus R1-F3..F8)
HO-3 : $D/TASK-WF-scIssueClaimPipe-20261107-063237 : $R/pre-TASK-WF-scIssueClaimPipe-20261107-063237-20261107063558/REPORT.md (blocking B-1..B-6 and medium M-n; the plan stays as written)
HO-4 : $D/TASK-WF-phase3CodegraphA-20261029-204913 : $R/pre-phase3CodegraphA-20261029205359/adversarial/merged-reviewer-findings.md (19 findings, 9 important, 10 minor)
Each plan folder holds the plan (<folder name>.md), source.md (what the plan must implement), progress.md and artifacts/ (implementation-time review records, e.g. artifacts/retries/*/review-*.md with severity markers).

ALLOWED to read: those four plan folders, those four review reports (and the files next to them in the same report folder), and git history of this repository (git log, git show, git cat-file, git rev-list) from $REPO. FORBIDDEN, no exceptions: any path containing recipe, recipes, cards, brief, sweep, ledger, derivation, collab, severity, brainstorm, 20261111-a1, 20261113, 20261114, 20261116 (except your own output folder), ground-truth, or holdout-gt; any file under .dev/eval-workspaces other than your output folder; do not run the repository's tests or any model. You write ONLY under $OUT.

OUTPUT per document HO-n, in $OUT/HO-n/:
1. candidate.md : an exact byte copy of the plan file (cp).
2. source.md : an exact copy of that plan's source.md (cp).
3. ground-truth.json : {\"doc_id\":\"HO-n\",\"plan\":\"<plan folder name>\",\"items\":[ ... ]}. One item per real plan defect, at most 12 per document, each item: {\"id\":\"GT1\" (GT1, GT2, ... in order),\"class\":\"unassigned\",\"blocking_in_implement\":true|false,\"description\":\"2 to 4 sentences: what an implementer who follows the plan as written would build wrongly, and the correct outcome\",\"plan_quote\":\"a contiguous quote of 40 to 200 characters copied EXACTLY from candidate.md that anchors the defect\",\"evidence\":\"the report finding id and file:line you derived it from\"}. blocking_in_implement is true only when the earlier review report marks the finding blocking, or an implementation-time review record under artifacts/ shows it was graded blocking while the plan was implemented; otherwise false. Include only defects of the PLAN text (what the plan says or omits relative to source.md and the repository at the time). Exclude: defects of code written during implementation, style or wording nits, findings the report itself marks as unfounded or not reproduced, and anything whose quote you cannot find verbatim in candidate.md. If a report finding cites a plan line, check that line really exists and says that in candidate.md; if the plan you copied differs from what the report reviewed, drop the finding and say so in notes.md.
4. package.json : {\"base\":\"<40-hex commit>\",\"candidate\":\"<repo-relative path of the plan file under .dev/tasks/done/...>\",\"source\":\"<repo-relative path of its source.md>\",\"kind\":\"plan\",\"set\":\"holdout\",\"masked_paths\":[...]} . base = the commit of the repository just BEFORE this plan was implemented: take it from the first 'start sha=' line of progress.md, and verify with git cat-file -t that it is a commit that contains the plan's own folder or at least the repository state the plan was written against; masked_paths = repository files that the implementation CREATED (they must not exist in the sandbox) and that already exist at base, normally none (use [] when none; list only paths you verified with git ls-tree at base).
5. notes.md : short list of findings you dropped and why, and anything that could not be verified.
Also write $OUT/SUMMARY.md: a table document | items | blocking items | dropped findings. Then reply with only that table. Be strict: a smaller verified set is better than a larger doubtful one; never invent a defect, and never copy a quote from memory."
S=$(date +%s)
( cd /tmp/ho-author && bash "$SLOT" ho-author timeout 5400 claude -p --model claude-sonnet-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$OUT/session.json" 2>"$OUT/session.err"
echo "END author rc=$? wall=$(( $(date +%s)-S ))s summary=$( [ -s $OUT/SUMMARY.md ] && echo yes || echo no )"
