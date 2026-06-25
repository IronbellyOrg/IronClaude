# Downstream Task-Builder Handoff (NON-BLOCKING) — RFMerger Refresh

**Generated:** 2026-06-18
**Task:** TASK-RF-rfmerger-refresh-20260618-172224

```yaml
status: AUTHORIZED
review_status: SIGNED-OFF
p2_decision: retain-with-full-set-revalidation-and-guards
p5_decision: retain-advisory-only
authorized_on: "2026-06-19"
action_required_before_use: []   # all preconditions satisfied
```

## Purpose

Instruction for the operator authoring the RFMerger implementation MDTM tasklist. As of 2026-06-19 all preconditions are met (human sign-off + both P2/P5 decisions recorded), so this handoff is now **AUTHORIZED** — a `/task-builder` run from the refreshed spec/PRD/TDD may proceed. (This refresh task itself produced documents only and generated no implementation tasklist.)

## Precondition (ALL satisfied ✅)

1. ✅ `artifacts/review-checkpoint.md` `review_status: SIGNED-OFF` (2026-06-19).
2. ✅ `phase-outputs/reviews/p2-human-decision-record.md` `decision: retain-with-full-set-revalidation-and-guards`.
3. ✅ `phase-outputs/reviews/p5-human-decision-record.md` `decision: retain-advisory-only`.

The downstream `/task-builder` run is authorized to proceed.

## Instruction (once the precondition is met)

Run `/task-builder` to author the implementation MDTM tasklist from the refreshed sources:
- `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/.dev/releases/current/v3.8-RigorFlowMerger-tasklist/spec.md`
- `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/.dev/releases/current/v3.8-RigorFlowMerger-tasklist/prd.md`
- `/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/.dev/releases/current/v3.8-RigorFlowMerger-tasklist/tdd.md`
- plus `artifacts/refresh-requirements-ledger.md` and `artifacts/refresh-validation-matrix.md` as control inputs.

### Hard requirements for the future implementation work

- **Ignore old `sc:tasklist`-generated RFMerger tasklists.** The historical package's implementation framing is stale; use ONLY the refreshed spec/PRD/TDD as the source of intent.
- **Honor the recorded P2/P5 decisions.** If P2 = `defer`, do not implement the Bounded Patch Loop. If P2 = `retain-with-full-set-revalidation-and-guards`, implement with full-set re-validation + monotonicity guard + regression detection + **1-extra-pass cap (2 total passes; `adversarial-validation.md:141`)** + no Stage-10.5 overlap. If P5 = `defer`, skip calibration; if `retain-advisory-only`, keep it advisory-only — scored tiers remain roadmap-only (same roadmap → same scored tiers); the advisory may read `feedback-log.md` but must never feed back into or mutate the deterministic scored tiers.
- **Sprint compatibility:** any future implementation tasklist MUST use `phase-N-tasklist.md` filenames and `### T<PP>.<TT>` task headings.
- **MDTM execution:** execute the built tasklist with `/task <absolute-task-path>` — NOT `/sc:task`.
- **Source-of-truth:** make all code changes under `src/superclaude/...` FIRST, then run `make sync-dev` and `make verify-sync`. NEVER stage `.claude/{skills,commands,agents,hooks,templates}` mirrors (only `.claude/settings.json` is tracked).
- **P3 reuse:** reuse the existing `task-builder` `synthetic-dnsp` DM-003 contract (`src/superclaude/skills/task-builder/SKILL.md:873-911`); do not author a new divergent contract. `StageError` for zero-success is a new implementation-time decision (no typed `StageError` exists in current source).
- **Resolve carried open questions first:** fix OQ-1 (stale `tests/reflect/` in BUILD-REQUEST.md/research-07 → `tests/cli/reflect/`) at source, and settle the `--spec` exact-input-contract §22 risk.

## Status note

Because review and P2/P5 decisions are PENDING, `status: BLOCKED_PENDING_HUMAN_REVIEW`. No `/task-builder` invocation was performed by this task.
