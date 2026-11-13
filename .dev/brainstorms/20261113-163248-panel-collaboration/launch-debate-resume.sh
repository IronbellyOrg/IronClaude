#!/usr/bin/env bash
# Resume of Wave 3 after the first debate session hit its 5400 s timeout during Round 3 (rounds 1, 2, 2.5 and round3-V1/V2 complete on disk).
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
B=$REPO/.dev/brainstorms/20261113-163248-panel-collaboration
O=$B/nested/adversarial-1; A=$O/adversarial
FILES=$(ls $B/variants/variant-*.md | sort | paste -sd,)
PROMPT="/sc:adversarial --compare $FILES --depth deep --convergence 0.75 --unattended --output $O

RESUME INSTRUCTION (from the brainstorm orchestrator): a previous session ran this exact command and was killed by a timeout during Round 3. Its work is on disk under $A: variant-1..5-original.md (loaded), diff-analysis.md (Step 1 done), debate/round1-V1..V5.md and round1-tally.md, debate/round2-agenda.md, round2-V1..V5.md and round2-tally.md (43/43 diff points agreed), invariant-probe.md (Round 2.5 done: 8 HIGH unaddressed invariants), debate/round3-agenda.md, and debate/round3-V1.md and round3-V2.md. Do NOT redo any completed step or overwrite those files. Continue the protocol from where it stopped: produce round3-V3.md, round3-V4.md and round3-V5.md following round3-agenda.md, then the Round 3 tally and convergence check, then Step 3 scoring and base selection, Step 4 refactor plan, Step 5 merge, the debate-transcript.md and the remaining standard artifacts, and finally replace both stub return contracts ($O/return-contract.yaml and $A/return-contract.yaml) with the real ones. Work efficiently: keep advocate statements concise.

Merge target (unchanged from the first session): the five files are independent variants of one requirements specification answering the seed brief at $B/seed-brief.md. The merged specification must keep the five-section structure and must end with exactly FIVE finalized, distinct redesigns, each complete with: mechanism and model roles, communication schedule (triggers, frequency, per-reviewer message caps, size caps, schema), transport and why, time-budget arithmetic showing at most +35% elapsed against a named isolated baseline, contamination safeguards with a measurable convergence alarm, expected gain with low/high range split into collaboration vs harness-fix shares, implementation effort, failure modes. Keep the three theories, the comparison table, the first-experiment section and the numbered testable requirements."
S=$(date +%s)
( cd "$REPO" && timeout 7200 claude -p --model claude-opus-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$B/sessions/debate-resume.json" 2>"$B/sessions/debate-resume.err"
RC=$?
jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$B/sessions/debate-resume.json" > "$B/sessions/debate-resume-reply.md" 2>/dev/null
echo "END debate-resume rc=$RC wall=$(( $(date +%s)-S ))s"; ls -la "$A"
