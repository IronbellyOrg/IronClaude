#!/usr/bin/env bash
# usage: run-reviewer.sh <EVAL abs> <pkg id> <reviewer_id> <model>
# Runs one first-review reviewer in a fresh `claude -p` session on the raw gateway model id.
set -u -o pipefail
EVAL=$1; PKG=$2; RID=$3; MODEL=$4
OUT=$EVAL/$PKG/reviews${5:+/$5}; mkdir -p "$OUT"
CAND_SB=/tmp/evalsb/cand/$PKG/candidate.md
mkdir -p "$(dirname "$CAND_SB")"; cmp -s "$EVAL/$PKG/candidate.md" "$CAND_SB" || cp "$EVAL/$PKG/candidate.md" "$CAND_SB"
# ship source.md next to the candidate when the eval carries it (per-model source input)
SRC_EVAL=$(ls /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md 2>/dev/null || true)
[ -n "$SRC_EVAL" ] && cmp -s "$SRC_EVAL" /tmp/evalsb/cand/$PKG/source.md 2>/dev/null || { [ -n "$SRC_EVAL" ] && cp "$SRC_EVAL" /tmp/evalsb/cand/$PKG/source.md; } || true
SHA=$(sha256sum "$CAND_SB" | cut -d' ' -f1)
BRIEF="/sc:spec-panel @$CAND_SB --mode critique

Review the candidate $CAND_SB (sha256 of the file: $SHA) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered.

First-review rules (from ~/.claude/rules/prompts/document_review_loop_prompts.md, read it first): write 'review: 1 of 3' once as the first line of the report. Grading check, for each finding before you mark it blocking: write the sentence 'An implementer who follows the stated text as written builds X, and X is wrong because Y.' Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass. Grade it Medium when the sentence needs a guess that the implementer picks the worse of two readings the text allows, or when the finding is a requirement the document never states rather than a stated text that does harm. End the report with the '## Findings block' (one fenced code block with info string findings-v1, one JSON object per line: id, severity CRITICAL|MAJOR|MINOR, blocking, category contradiction|unpassable-check|data-loss|safety|missing-requirement|other, anchor = 12 to 200 chars copied exactly from the candidate, optional anchor2, refs, claim) and a final 'verdict: PASS' or 'verdict: FAIL' line. Your final reply must be the complete report text."
attempt=0
# Model fallback ladder (owner order 2026-11-12: every model needs a fallback for
# communication errors / model-level outages). Keyed by requested model; a misrouted
# observed model (model_ok=false after both attempts) or an API-error result escalates
# to the next fallback. Empty observed model with 0 tokens = communication error.
declare -A FALLBACK
# Owner order 2026-11-12 18:10 UTC: fall back to the NEXT MODEL IN THE SAME TIER (02->03->04...),
# then wrap to the FIRST model of the NEXT tier. Tier lists as registered in the gateway picker
# (muse-ember-1.0 being added as Tier 04 Model 02):
#   T3 (01 glm-5.3, 02 Qwen3.8-max) -> next tier T4 (01 luna, 02 ember, 03 haiku, 04 grok)
#   T2 (01 sol, 02 glm, 03 grok, 04 Qwen, 05 muse-wonder, 06 spark) -> T2b (terra, glm, Qwen, muse-wonder)
#   T1b (sonnet, sol, muse-wonder-full) / T1a (opus, sonnet) -> T2
# Within-tier successor then next-tier head (cyclic; never returns to the failed model's tier-mate that already failed):
FALLBACK[glm-5.3]="Qwen3.8-max"                 # T3 01 -> T3 02
FALLBACK[Qwen3.8-max]="gpt-6-luna"              # T3 02 -> T4 01 (next tier head)
FALLBACK[gpt-6-luna]="muse-ember-1.0"           # T4 01 -> T4 02
FALLBACK[muse-ember-1.0]="claude-haiku-5-5"     # T4 02 -> T4 03
FALLBACK[claude-haiku-5-5]="grok-4.7"           # T4 03 -> T4 04
FALLBACK[grok-4.7]="gpt-6.1-sol"                # T4 04 -> T2 01 (next tier head)
FALLBACK[gpt-6.1-sol]="glm-5.3"                 # T2 01 -> T2 02
FALLBACK[muse-wonder-1.0]="muse-spark-1.3"      # T2 05 -> T2 06
FALLBACK[muse-spark-1.3]="gpt-6.1-terra"        # T2 06 -> T2b 01 (next tier head)
FALLBACK[gpt-6.1-terra]="gpt-6-luna"            # T2b head -> T4 01
FALLBACK[claude-sonnet-5-5]="gpt-6.1-sol"       # T1b/T1a -> T2 01
FALLBACK[muse-wonder-full-1.0]="gpt-6.1-sol"    # T1b 03 -> T2 01
FALLBACK[claude-opus-5-5]="gpt-6.1-sol"         # T1a -> T2 01 (never auto-run; guard)
MODEL_LADDER="$MODEL"
run_attempt() { # runs one attempt with $MODEL; returns 0 if model_ok && block_ok
  local attempt=$1
  local S=$(date +%s)
  ( cd /tmp/evalsb/repo && timeout 3000 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$BRIEF" ) >"$OUT/$RID.attempt$attempt.json" 2>"$OUT/$RID.attempt$attempt.err"
  RC=$?; W=$(( $(date +%s)-S ))
  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$OUT/$RID.attempt$attempt.json" > "$OUT/$RID.attempt$attempt.md" 2>/dev/null
  OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$OUT/$RID.attempt$attempt.json" 2>/dev/null)
  TOK=$(jq '[.[]|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$OUT/$RID.attempt$attempt.json" 2>/dev/null)
  TOKALL=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/$RID.attempt$attempt.json" 2>/dev/null)
  APIERR=false; grep -q 'API Error' "$OUT/$RID.attempt$attempt.md" 2>/dev/null && APIERR=true
  LOWOBS=$(echo "$OBS" | tr 'A-Z' 'a-z'); LOWEXP=$(echo "$MODEL" | tr 'A-Z' 'a-z')
  MODEL_OK=false; [ -n "$OBS" ] && [ "$OBS" != "<synthetic>" ] && { [ "$LOWOBS" = "$LOWEXP" ] || [ "$LOWOBS" = "$LOWEXP-build" ]; } && MODEL_OK=true
  BLOCK_OK=false; grep -q '^```findings-v1' "$OUT/$RID.attempt$attempt.md" && BLOCK_OK=true
  jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$OBS" --argjson mok $MODEL_OK --argjson bok $BLOCK_OK --argjson att $attempt --argjson w $W --argjson tok "${TOK:-0}" --argjson tokall "${TOKALL:-0}" --argjson rc $RC '{reviewer_id:$rid,expected_model:$exp,observed_model:$obs,model_ok:$mok,findings_block:$bok,attempt:$att,wall_s:$w,output_tokens_main:$tok,output_tokens_all:$tokall,exit:$rc}' > "$OUT/$RID.attempt$attempt.meta.json"
  $MODEL_OK && $BLOCK_OK && ! $APIERR
}
while [ $attempt -lt 2 ]; do
  attempt=$((attempt+1))
  if run_attempt $attempt; then break; fi
done
# Escalate the ladder when the primary model failed model-identity or errored
if { ! ($MODEL_OK && $BLOCK_OK) || $APIERR; } && [ -z "${NOFALLBACK:-}" ]; then
  # Guards added 2026-11-12 after a batch-9 incident: the ladder is cyclic, so instant failures (claude binary briefly missing,
  # exit 127) spun it round the cycle and finally ran a review on Qwen3.8-max. Now: never revisit a model, never use an excluded model.
  EXCLUDE_MODELS=${EXCLUDE_MODELS:-"glm-5.3 Qwen3.8-max"}
  VISITED=" $MODEL "
  nextmodel() { local n=${FALLBACK[$1]:-}; while [ -n "$n" ]; do case " $EXCLUDE_MODELS " in *" $n "*) n=${FALLBACK[$n]:-};; *) break;; esac; done; case "$VISITED" in *" $n "*) n="";; esac; echo "$n"; }
  NEXT=$(nextmodel "$MODEL")
  while [ -n "$NEXT" ] && ! ($MODEL_OK && $BLOCK_OK); do
    VISITED="$VISITED$NEXT "
    echo "FALLBACK $MODEL -> $NEXT ($(date -u +%T))" >> "$OUT/$RID.fallback.log"
    MODEL="$NEXT"; MODEL_LADDER="$MODEL_LADDER->$NEXT"; attempt=0
    while [ $attempt -lt 2 ]; do
      attempt=$((attempt+1))
      if run_attempt $attempt; then break; fi
    done
    NEXT=$(nextmodel "$MODEL")
  done
fi
# final = last attempt
cp "$OUT/$RID.attempt$attempt.md" "$OUT/$RID.md"; cp "$OUT/$RID.attempt$attempt.meta.json" "$OUT/$RID.meta.json"
# total cost across attempts (both attempts count toward tokens/wall)
jq -s '{attempts:length,total_wall_s:(map(.wall_s)|add),total_output_tokens_all:(map(.output_tokens_all)|add)}' "$OUT/$RID".attempt*.meta.json > "$OUT/$RID.cost.json"
