#!/usr/bin/env bash
# Blind judge for one batch (PLAN.md section 5). Opus is used only as the judge. Usage: judge-batch.sh <batch-NN>
set -u -o pipefail
O=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-severity
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
B=$1; IN=$O/batches/$B.json; OUT=$O/judged/$B.json; mkdir -p "$O/judged" "$O/judged-raw"
[ -s "$OUT" ] && { echo "SKIP $B"; exit 0; }
PROMPT="You are a blind grading judge. Below is a batch of review findings, each claiming that two texts in an implementation plan contradict each other. Decide for each whether the finding is BLOCKING or MEDIUM under the grading rule below.

Files (read them fully, read-only): the plan under review: $(jq -r .candidate "$IN"); its source document: $(jq -r .source "$IN"); the batch: $IN. You may read any file in the repository at $REPO to check what the plan orders built (read-only; edit nothing). Do not open anything under .dev/eval-workspaces, .dev/reflect or .dev/research, and do not look for review reports or ground truth.

THE RULE for a contradiction finding. It is BLOCKING only if the two stated texts contradict each other AND the contradiction would, with high probability, change what ships: it decides the behavior, output, test, interface or reader-facing instruction of a final deliverable. A contradiction confined to text that no deliverable reads or acts on (code comments, rationale or background prose, superseded or historical sections, examples, labels, internal notes) is MEDIUM even when the two texts clearly disagree. To mark a contradiction BLOCKING you must name the deliverable it changes and say in one sentence why a reader or implementer would act on the wrong text. If you cannot name it, grade MEDIUM. When the deliverable is itself documentation that readers act on (a user guide, a reference page, a skill or command instruction), a contradiction in that documentation is BLOCKING. Also grade MEDIUM when the finding is not a real contradiction (the two texts are consistent, the claim misreads the plan, or the text is already corrected elsewhere in the plan), and grade by the plan's text, not by whether the finding is well written.

For each item: locate the anchor text in the plan, check the claim against the plan and, where needed, the repository, then decide. Be strict and consistent: the same situation gets the same grade.

Final reply: ONLY a JSON array, no prose, one object per item in the batch order, with keys: id, verdict (\"BLOCKING\" or \"MEDIUM\"), deliverable (the named deliverable, or null for MEDIUM), real_contradiction (true or false), reason (at most 30 words)."
S=$(date +%s)
( cd "$REPO" && timeout 2400 claude -p --model claude-opus-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$PROMPT" ) > "$O/judged-raw/$B.json" 2>"$O/judged-raw/$B.err"
RC=$?
jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$O/judged-raw/$B.json" | sed -e 's/^```json//' -e 's/^```//' -e 's/```$//' > "$O/judged-raw/$B.txt" 2>/dev/null
if jq -e 'type=="array" and length>0' "$O/judged-raw/$B.txt" >/dev/null 2>&1; then cp "$O/judged-raw/$B.txt" "$OUT"; ST=ok; else ST=BAD; fi
OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$O/judged-raw/$B.json" 2>/dev/null)
echo "END $B rc=$RC $ST observed=$OBS wall=$(( $(date +%s)-S ))s items_in=$(jq '.items|length' "$IN") items_out=$(jq 'length' "$OUT" 2>/dev/null || echo 0)"
