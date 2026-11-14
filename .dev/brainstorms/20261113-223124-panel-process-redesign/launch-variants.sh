#!/usr/bin/env bash
# Wave 3 variant generation: one headless claude -p session per proposal, each with its own budget (owner decision 2026-11-13),
# at most 2 sessions at once (owner order 2026-11-13). Models: sonnet and haiku only (standing rule: Opus is for scoring).
# Each variant proposes TWO redesigns; the adversarial merge keeps exactly two.
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
B=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign
EV=$REPO/.dev/eval-workspaces/tasklist-review-panel
export REPO B EV
SPECS=(
"1|claude-sonnet-5-5|sonnet|architect|prioritize maintainability and extension scaffolding for architecture domain"
"2|claude-sonnet-5-5|sonnet|analyzer|focus on root-cause analysis and evidence-based reasoning for architecture"
"3|claude-haiku-5-5|haiku|backend|focus on API contracts, data integrity, idempotency, and operational concerns"
)
run_one() {
  IFS='|' read -r N MODEL ALIAS PERSONA INSTR <<<"$1"
  local OUT="$B/variants/variant-$N-$ALIAS-$PERSONA.md" J="$B/sessions/variant-$N.json"
  local PROMPT="You are generating ONE variant (variant $N of 3) of a requirements specification that will be compared against 2 other independently written variants in an adversarial debate and merge. Persona: $PERSONA. Lens: $INSTR.

Source (read it fully first): $B/seed-brief.md. Then read every enrichment artifact: $B/enrichment/reused/*.md and $B/enrichment/investigation-generality.md and $B/enrichment/research-external.md. You may read evidence read-only under $EV/ (HANDOFF-review-panel-unification-run2.md, 20261111-a1/COMBO-REPORT.md final sections, 20261111-a1/tools/run-reviewer.sh, 20261111-a1/analysis/) and the repo. The first brainstorm's merged requirements (.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md) and its five redesigns are background only: this brainstorm asks for two NEW redesigns judged on consistently finding the missed issues and on broad applicability; you may reuse a building block from it only if you justify it. Do not edit or create any file.

Write a requirements specification with exactly these sections:
1. Theories: the three theories that best explain why ember + luna + haiku panels never found the ten issues (accept, refine or replace T1-T3 from the seed brief), with evidence numbers and what instruction or process change each theory implies.
2. Defect classes and generality: abstract the ten missed issues into defect classes stated with no package, task number, file name or ground-truth wording; for each class give the evidence that it recurs in other material (from investigation-generality.md and research-external.md; cite them) and the review targets it applies to.
3. Exactly TWO redesigns of how the panel operates (agent instructions, process, or both; a deterministic non-model pre-pass or helper is allowed; reviewer-to-reviewer messaging is allowed but not required). For EACH give: (a) name and mechanism, with the quoted draft wording of every instruction or brief change and the exact order of steps; (b) model roles on the primary baseline panel ember + 2x luna, and how it adapts to haiku + 2x luna and sonnet + 2x luna; (c) step-by-step time budget in seconds per package against the named isolated baseline (use the measured per-package medians in the seed brief), identifying the critical path and showing elapsed increase of at most +35% (say what is enforced by a kill or timer and what is only expected); (d) a defect-class coverage matrix: for each of the ten missed issues, the class-level mechanism that would trigger it, why a cheap model would then reach it, and a probability of reaching it per run (low and high) so 'consistently' is quantified; (e) broad applicability: how the same mechanism ports to other plans, to specifications and to documentation reviews, what must be re-derived for each new target, and anti-overfitting rules (no ground-truth text or issue-specific hint in any instruction); (f) expected gain in issues found out of 14 per run with low and high range, split into the share from the four harness fixes of the seed brief and the share from the redesign; (g) token and elapsed overhead; (h) implementation effort against the existing harness (files, rough lines); (i) failure modes, including false-positive growth and wrong blockers.
4. Comparison table of the two redesigns.
5. Validation experiment that does not reuse the data the design was derived from: hold-out packages or documents (use the candidates from investigation-generality.md), arms including the isolated panel with the harness fixes, runs per arm, how consistency is measured, and a pre-registered decision rule.
6. Numbered, testable requirements.
Rules: instructions given to reviewers must be generic investigative moves or class-keyed checks that would apply to any plan, never issue-specific text derived from ground truth; reviewers stay read-only and never see ground truth; keep the findings-v1 merge contract; plain English; tables for multi-item data; cite evidence paths. Your final reply must be the complete specification in markdown and nothing else (it is saved verbatim as your variant file)."
  local S=$(date +%s)
  ( cd "$REPO" && timeout 3000 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$PROMPT" ) >"$J" 2>"$B/sessions/variant-$N.err"
  local RC=$?
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$J" >"$OUT" 2>/dev/null
  local OBS TOK
  OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$J" 2>/dev/null)
  TOK=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$J" 2>/dev/null)
  echo "END variant-$N rc=$RC model=$MODEL observed=$OBS wall=$(( $(date +%s)-S ))s out_tokens=$TOK lines=$(wc -l <"$OUT")"
}
export -f run_one
echo "START $(date -u +%T) max_parallel=2"
printf '%s\n' "${SPECS[@]}" | xargs -P 2 -I{} bash -c 'run_one "{}"'
echo ALLDONE
