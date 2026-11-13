#!/usr/bin/env bash
# Wave 3 variant generation, one headless claude -p session per proposal (owner decision 2026-11-13:
# each proposal in its own session with its own budget). The debate and merge then run as sc:adversarial Mode A.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
B=$REPO/.dev/brainstorms/20261113-163248-panel-collaboration
A=$B/adversarial; mkdir -p "$A" "$B/sessions"
# n model-id alias persona instruction (from refs/agent-spec-builder.md templates, domain=architecture, strategy=systematic)
SPECS=(
"1|claude-opus-5-5|opus|architect|prioritize maintainability and extension scaffolding for architecture domain"
"2|claude-opus-5-5|opus|analyzer|focus on root-cause analysis and evidence-based reasoning for architecture"
"3|claude-haiku-5-5|haiku|backend|focus on API contracts, data integrity, idempotency, and operational concerns"
"4|claude-opus-5-5|opus|devops|focus on deployment, observability, runbooks, and SLO impact for systematic delivery"
"5|claude-sonnet-5-5|sonnet|performance|focus on bottlenecks, scaling behavior, and cost-to-serve"
)
run_one() {
  IFS='|' read -r N MODEL ALIAS PERSONA INSTR <<<"$1"
  OUT="$A/variant-$N-$ALIAS-$PERSONA.md"; J="$B/sessions/variant-$N.json"
  PROMPT="You are generating ONE variant (variant $N of 5) of a requirements specification that will be compared against 4 other independently written variants in an adversarial debate and merge. Persona: $PERSONA. Lens: $INSTR.

Source (read it fully first): $B/seed-brief.md. Then read every enrichment artifact it lists under $B/enrichment/ (investigation-designspec.md, investigation-alias-control.md, investigation-patterns.md, research-light.md). You may read evidence read-only under $REPO/.dev/eval-workspaces/tasklist-review-panel/ (COMBO-REPORT.md final sections, HANDOFF-review-panel-unification-run2.md, 20261111-a1/tools/run-reviewer.sh, analysis/) and the repo source. Do not edit or create any file.

Write a requirements specification that answers the seed brief, with exactly these sections:
1. Theories: state the three theories that best explain why ember + luna + haiku panels never found B1, B2, B5, B6, B8, I1, I4, I5, I6, I7 (accept, refine or replace T1-T3 from the seed brief, with the evidence numbers).
2. Five redesigns of how the panel operates so models communicate and collaborate DURING their runs. For EACH redesign give: (a) name and one-paragraph mechanism with the role of each model (choose from ember, luna, haiku, sonnet, grok; no Qwen or glm; Opus only as the blind judge); (b) communication schedule: the exact trigger points, how often, the maximum messages per reviewer per package, the message size cap, and the message schema; (c) transport and why (from: JSON board with hooks, Claude Code cross-session messaging, between-phase digest; Orca mail and A2A were researched); (d) time budget arithmetic per package against a named isolated baseline panel, showing the added elapsed time is at most +35% (use the slowest-reviewer critical path and the idle time of faster reviewers); (e) contamination safeguards: what is shared and what is withheld, how each model keeps its independent first pass, how a peer's blind spot is prevented from spreading, and a measurable convergence alarm; (f) expected gain: which missed issues it targets and through which theory, an estimate of added issues found out of 14 per run with stated assumptions and a low/high range, separating the share due to collaboration from the share due to harness fixes (named source.md, anchor limit, pre-implementation checkout, removing the .dev/reflect leak); (g) implementation effort against the existing harness (files, rough lines of code); (h) failure modes.
3. A comparison table of the five redesigns (elapsed overhead %, tokens overhead %, expected gain low/high, contamination risk, implementation effort, reliability).
4. The recommended first experiment on the three existing packages, scored with the existing blind Opus judge: arms, runs per arm, decision rule.
5. Numbered, testable requirements for the chosen design(s).
Rules: hints exchanged between reviewers must be generic investigative moves that would apply to any plan, never issue-specific text derived from ground truth (that would overfit the panel to these three packages); reviewers stay read-only and never see ground truth; keep the findings-v1 merge contract. Use plain English, tables for multi-item data, cite evidence paths. Your final reply must be the complete specification in markdown and nothing else (it is saved verbatim as your variant file)."
  local S=$(date +%s)
  ( cd "$REPO" && timeout 3000 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$PROMPT" ) >"$J" 2>"$B/sessions/variant-$N.err"
  local RC=$?
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$J" >"$OUT" 2>/dev/null
  OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$J" 2>/dev/null)
  TOK=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$J" 2>/dev/null)
  echo "END variant-$N rc=$RC model=$MODEL observed=$OBS wall=$(( $(date +%s)-S ))s out_tokens=$TOK lines=$(wc -l <"$OUT")"
}
for s in "${SPECS[@]}"; do run_one "$s" & done
wait; echo ALLDONE
