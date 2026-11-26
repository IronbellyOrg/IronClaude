#!/usr/bin/env bash
# Wave 3 debate + merge in its own session (owner: each stage with its own budget). sc:adversarial Mode A over the 5 variants.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
B=$REPO/.dev/brainstorms/20261113-163248-panel-collaboration
V=$B/variants; O=$B/nested/adversarial-1; mkdir -p "$B/sessions"
FILES=$(ls $V/variant-*.md | sort | paste -sd,)
PROMPT="/sc:adversarial --compare $FILES --depth deep --convergence 0.75 --unattended --output $O

Context for the merge (from the brainstorm orchestrator): the five files are independent variants of one requirements specification answering the seed brief at $B/seed-brief.md (read it). The merged specification must keep the same five-section structure as the variants and must end with exactly FIVE finalized, distinct redesigns, each complete with: mechanism and model roles, communication schedule (triggers, frequency, per-reviewer message caps, size caps, schema), transport and why, time-budget arithmetic showing at most +35% elapsed against a named isolated baseline, contamination safeguards with a measurable convergence alarm, expected gain with low/high range split into collaboration vs harness-fix shares, implementation effort, failure modes. Select and combine the strongest redesigns across all variants rather than merging everything into one design. Keep the three theories, the comparison table, the first-experiment section and the numbered testable requirements."
S=$(date +%s)
( cd "$REPO" && timeout 5400 claude -p --model claude-opus-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$B/sessions/debate.json" 2>"$B/sessions/debate.err"
RC=$?
jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$B/sessions/debate.json" > "$B/sessions/debate-reply.md" 2>/dev/null
echo "END debate rc=$RC wall=$(( $(date +%s)-S ))s"; ls -la "$O" "$O/adversarial" 2>/dev/null
