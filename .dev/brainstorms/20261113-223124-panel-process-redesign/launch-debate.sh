#!/usr/bin/env bash
# Wave 3 debate + merge in its own session (sc:adversarial Mode A over the 3 variants). Sonnet only (standing rule: Opus is for scoring).
# Resume-safe: rerun the same script after a timeout; the prompt tells the session to continue from artifacts already on disk.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
B=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign
O=$B/nested/adversarial-1; mkdir -p "$O"
FILES=$(ls $B/variants/variant-*.md | sort | paste -sd,)
RESUME=""; [ -d "$O/adversarial" ] && RESUME="
RESUME INSTRUCTION: an earlier session ran this exact command and stopped (timeout or interruption). Its work is on disk under $O/adversarial. Do NOT redo or overwrite completed steps; continue from where it stopped and finish all standard artifacts and both return contracts."
PROMPT="/sc:adversarial --compare $FILES --depth deep --convergence 0.75 --unattended --output $O
$RESUME
Context for the merge (from the brainstorm orchestrator): the three files are independent variants of one requirements specification answering the seed brief at $B/seed-brief.md (read it). Each variant proposes TWO redesigns. The merged specification must keep the same six-section structure and must end with exactly TWO finalized, distinct redesigns (select and combine the strongest across all variants; do not merge everything into one design and do not output more than two), each complete with: mechanism with quoted draft instruction wording and step order, model roles and adaptation to the three panels, step-by-step time budget showing at most +35% elapsed against a named isolated baseline, defect-class coverage matrix over the ten missed issues with per-run reach probabilities, broad applicability with anti-overfitting rules, expected gain split into harness-fix share and redesign share, overhead, implementation effort, failure modes. Keep the three theories, the defect classes with their generality evidence, the comparison table, the hold-out validation experiment and the numbered testable requirements. Work efficiently: keep advocate statements concise."
S=$(date +%s)
( cd "$REPO" && timeout 7200 claude -p --model claude-sonnet-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$B/sessions/debate.json" 2>"$B/sessions/debate.err"
RC=$?
jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$B/sessions/debate.json" > "$B/sessions/debate-reply.md" 2>/dev/null
echo "END debate rc=$RC wall=$(( $(date +%s)-S ))s"
