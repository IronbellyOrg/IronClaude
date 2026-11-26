#!/usr/bin/env bash
# Owner order 2026-11-14 ("build the 2 process redesigns and rerun 3 tests each"; answer "build in parallel now" for Redesign 2).
# Redesign 2, Recipe Ledger, of the process-redesign brainstorm: design -> checked plan -> implement, three sonnet sessions in a row.
# Redesign 1 (Sweep Sheet) is built by another session in ../20261114-sweep-sheet; this folder never edits it and only reads it.
# Resumable: each stage skips when its output exists; stage C resumes via /sc:implement's own ledger. Sonnet only (Opus is for scoring).
set -u -o pipefail
REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
W=$REPO/.dev/eval-workspaces/tasklist-review-panel
D=$W/20261114-recipe-ledger
SW=$W/20261114-sweep-sheet
MR=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md
EVAL=$W/20261111-a1
MODEL=claude-sonnet-5-5
mkdir -p "$D/design-report" "$D/workflow-report" "$D/implement-report"
CONSTR="Constraints: create or edit files only under $D (plus scratch under /tmp, and for stage B the new plan package that /sc:workflow creates). Do not edit src/, tests/, .claude/, any existing folder under .dev/tasks/, the sweep-sheet folder $SW (read it only), the 20261111-a1 or 20261113-collab folders, or any other folder. Do not stage, commit or push. Do not open any ground-truth*.json: the work must not use the answers of the study packages. Use uv for all Python. Models: do not start any reviewer or judge session unless the stage says so; if a model is needed use claude-sonnet-5-5 or claude-haiku-5-5 (Opus only as the blind judge). Never Qwen or glm."
now() { date -u +%T; }

# ---- A: design
if [ ! -s "$D/DESIGN.md" ] || [ ! -s "$D/TESTING.md" ] || [ ! -s "$D/IMPLEMENTATION.md" ]; then
PROMPT="/sc:design \"Implementation and test design for Redesign 2: Recipe Ledger of the tasklist review panel (written class recipes and a forced enumerate-then-judge ledger, no pre-pass script; the reviewing model runs the recipe). Source of truth: $MR. Read its sections 1 (theories), 2 (defect classes and generality), 3.0 (shared scaffolding), 3.2 (Redesign 2: Recipe Ledger), 4 (comparison), 5 (validation experiment, all subsections) and 6.1, 6.2, 6.4, 6.5, 6.6, 6.7, 6.8 (numbered requirements), plus its 'Not checked and unverified' list. Also read the harness it extends: $EVAL/tools/run-reviewer.sh, $EVAL/tools/tmp-scripts/judge-one.sh, $EVAL/combos/SPEC.md, $EVAL/COMBO-REPORT.md, and the superclaude review merge code under src/superclaude/cli/ (findings-v1 format). A sibling session is building Redesign 1 (Sweep Sheet) in $SW; the shared scaffolding of 3.0 (class cards, ledger-v1, briefs CB-1 to CB-5, harness fixes H1-H4, the Z0 control arm) is common to both. Read $SW/DESIGN.md, $SW/cards/, $SW/briefs/ and $SW/bin/ read-only and REUSE their shared pieces by copying them into $D at build time (record the sha256 of what you copied) instead of inventing a second version; design only the parts that are specific to Recipe Ledger (recipes per class, lens table in the launcher, the ledger enforcement, its checks and fallback, the time budget). Deliver, inside $D only: DESIGN.md (architecture, recipe format and the recipes per class C1-C8, the lens table, the ledger format and the checks that parse it, the brief change, failure and fallback behaviour, the time budget against the +35% rule with numbers, how it generalises beyond the three study packages), TESTING.md (every REQ in 6.1, 6.2, 6.4 to 6.8 mapped to a runnable test or a labelled manual check, fixtures, and the commands to run one panel of ember + 2x luna on one package for the RL arm and for the Z0 control arm), and IMPLEMENTATION.md (ordered steps with files, test commands using uv, what to run first). Design only: write no production code and run no reviewer or judge session. $CONSTR\""
S=$(date +%s); echo "START A $(now)"
( cd "$REPO" && timeout 5400 claude -p --model $MODEL --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$D/design-report/session.json" 2>"$D/design-report/session.err"
echo "END A rc=$? wall=$(( $(date +%s)-S ))s DESIGN=$(wc -l <"$D/DESIGN.md" 2>/dev/null || echo 0) TESTING=$(wc -l <"$D/TESTING.md" 2>/dev/null || echo 0) IMPL=$(wc -l <"$D/IMPLEMENTATION.md" 2>/dev/null || echo 0) $(now)"
fi
[ -s "$D/DESIGN.md" ] && [ -s "$D/TESTING.md" ] && [ -s "$D/IMPLEMENTATION.md" ] || { echo "STOP: design files missing"; exit 1; }

# ---- B: checked plan (/sc:workflow writes a new package under .dev/tasks/to-do/)
PLANF=$D/workflow-report/plan-path.txt
if [ ! -s "$PLANF" ]; then
PROMPT="/sc:workflow \"Implement Redesign 2: Recipe Ledger of the tasklist review panel exactly as specified by $D/DESIGN.md, $D/TESTING.md and $D/IMPLEMENTATION.md (requirements source: $MR sections 3.0, 3.2, 5 and 6). All code, fixtures and tests go under $D only. Tests use uv (uv run pytest) and a fake claude so no model runs are needed; the plan must include a step that runs every test and a final step that writes $D/IMPLEMENTATION-REPORT.md stating what was built, the exact commands to run one panel of ember + 2x luna on each of the three study packages for the RL arm and for the Z0 control arm, test counts, and every requirement not met with the reason.\" --depth standard --handoff none

$CONSTR Print the path of the plan you create as its own line and also write that single path to $PLANF."
S=$(date +%s); echo "START B $(now)"
( cd "$REPO" && timeout 3600 claude -p --model $MODEL --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$D/workflow-report/session.json" 2>"$D/workflow-report/session.err"
echo "END B rc=$? wall=$(( $(date +%s)-S ))s plan=$(cat "$PLANF" 2>/dev/null) $(now)"
fi
PLAN=$(head -1 "$PLANF" 2>/dev/null)
[ -s "$PLAN" ] || { echo "STOP: plan missing ($PLAN)"; exit 1; }

# ---- C: implement
PROMPT="/sc:implement $PLAN

Owner constraints for this run: $CONSTR Start no reviewer or judge model (tests use the fake claude). If a QA step needs a model, use claude-sonnet-5-5 or claude-haiku-5-5 only. The orchestrator runs the three package tests afterwards; do not run any full panel."
S=$(date +%s); echo "START C $(now)"
( cd "$REPO" && timeout 14400 claude -p --model $MODEL --output-format json --no-session-persistence --permission-mode bypassPermissions <<<"$PROMPT" ) >"$D/implement-report/session.json" 2>"$D/implement-report/session.err"
echo "END C rc=$? wall=$(( $(date +%s)-S ))s report=$( [ -s "$D/IMPLEMENTATION-REPORT.md" ] && echo yes || echo no ) $(now)"
echo ALLDONE
