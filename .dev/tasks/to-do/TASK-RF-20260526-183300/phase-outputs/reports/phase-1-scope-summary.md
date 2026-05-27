# Phase 1 Scope Summary

**Captured:** 2026-05-26
**Step:** Phase 1, Step 1.4 (aggregation for PG-1 gate)

**Aggregated inputs:**

- `.dev/tasks/to-do/TASK-RF-20260526-183300/phase-outputs/discovery/pre-existing-worktree-state.md` (Step 1.0 output)
- `.dev/tasks/to-do/TASK-RF-20260526-183300/phase-outputs/discovery/safety-scope-confirmation.md` (Steps 1.2 + 1.3 outputs, including the Scope Note)
- `.dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-plan.md` (decision, rollback recommendation, acceptance metrics)
- `.dev/tasks/to-do/TASK-RF-20260526-183300/research/05-gap-fill-research-gate-remediation.md` (case 12 deferral rationale)

## Phase 1 Decision Table

| Decision | Verdict / Evidence | Required Follow-Up | Blocks Later Phase? |
|----------|--------------------|--------------------|---------------------|
| **Live default status** | Live `/sc:brainstorm` behavior IS default-user-facing. No gating flag found in `src/superclaude/commands/brainstorm.md` or `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` (only Wave 4 handoff is flag-gated, which is downstream of the lossy synthesis behavior). Per `sc-brainstorm-remediation-plan.md` lines 479-489. | A separate rollback/gating task is identified as a follow-up. Suggested: feature flag in `src/superclaude/commands/brainstorm.md` defaulting `/sc:brainstorm` to iteration-2 behavior until cases 4-11 acceptance passes, OR temporary disable of live synthesis. Decision deferred to operator. | **No.** Phase 2 may proceed. Phase 2-4 fix the protocol in-place; if remediation lands quickly, separate gating may not be needed. |
| **Non-rollback stance** | This task is targeted in-place remediation, not a blanket rollback. Phases 2-4 EDIT existing protocol/merge/eval files; they do not delete or revert. Per `sc-brainstorm-remediation-plan.md` lines 5-9 ("Keep iteration-2 baseline as the quality bar, freeze or roll back live as the default, then selectively reintroduce live's useful improvements"). | None. The stance is durable across all phases. | **No.** |
| **Useful live improvements preserved** | Six categories of useful live improvements identified for preservation as augmentation, not removal: (1) governance/safety framing, (2) source-of-truth safeguards, (3) rollback/purge/disablement controls, (4) lifecycle taxonomies, (5) policy-first framing, (6) proof gates. Per `safety-scope-confirmation.md` "Live Improvements to Preserve" section. | Phase 2 protocol edits, Phase 3 adversarial merge edits, and Phase 4 eval assertion edits must each verify these are preserved in their respective output summaries. | **No** (but each later phase carries a preservation obligation). |
| **Cases 4-11 acceptance scope** | Per `sc-brainstorm-remediation-plan.md` lines 419-427: structural pass rate ≥95% (target 100%), qualitative baseline wins ≤2/8, live average ≥52/60, provenance average ≥8.50, concreteness average ≥8.50, no missing dedicated Provenance sections, no critical seed anchors dropped without rationale. Per `compare_live_runs.py:10-14`: `CASE_IDS = set(range(4, 12))` is the canonical compared set. | Phase 4 must update `evals.json`, `grader.py`, and `compare_live_runs.py` assertions to enforce these metrics. Phase 6 must regenerate comparison artifacts and evaluate against this matrix. | **No.** |
| **Case 12 exclusion (intentional)** | Case 12 blocker is the literal error string `Unknown skill: sc:brainstorm-protocol` at `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-architecture-graphql-public-api/live-run-error.md:6-10`. The case failed BEFORE protocol execution — it's a command-dispatch / skill-registry compatibility issue, not a synthesis-quality issue addressable by Phase 2-4 edits. Per `research/05-gap-fill-research-gate-remediation.md` lines 44-55. | If operator decides to bring registry compatibility into scope, a separate task is required (investigates command dispatcher behavior, skill name registration, `sc:` / `sc-` naming convention). | **No** (exclusion is documented; this task does not silently drop case 12 and does not preemptively allocate effort to it). |
| **No generated mirror edits** | Per CLAUDE.md "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents" and per `pre-existing-worktree-state.md`. All edits in Phases 2-4 go to `src/superclaude/`. Mirrors are regenerated via `make sync-dev` in Phase 5. Existing `.claude/` mirror drift (6 paths in scoped set, ~125 paths in broader worktree) is NOT staged, reverted, or hand-edited. | Phase 5 (`make sync-dev` + `make verify-sync`) reconciles mirrors after source edits. Phase 5 Step 5.1 audits for any source-of-truth violations introduced during execution. | **No** (constraint is enforced by hook + Phase 5 audit). |
| **UV-only Python** | Per CLAUDE.md "Python Environment Rules" and tasklist Phase 4/5 statements. All Python validation in Phases 4-6 (`grader.py`, `compare_live_runs.py`, optional pytest) wrapped in `uv run`. | Phase 5 syntax checks and Phase 5/6 comparison runs use `uv run python`. | **No** (constraint is enforced by Phase 5 gate). |

## Source-of-Truth / Sync Discipline Inventory

- Source files to edit (Phases 2-4):
  - `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` (Phase 2.1)
  - `src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md` (Phase 2.2)
  - `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` (Phase 2.3)
  - `src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md` (Phase 2.4, conditional)
  - `src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md` (Phase 3.1)
  - `src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md` (Phase 3.2)
  - `.dev/eval-workspaces/sc-brainstorm/evals/evals.json` (Phase 4.1)
  - `.dev/eval-workspaces/sc-brainstorm/grader.py` (Phase 4.2)
  - `.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py` (Phase 4.3)

- Generated mirrors that will reflect source edits after Phase 5 `make sync-dev`:
  - `.claude/skills/sc-brainstorm-protocol/` (currently in sync per scoped status)
  - `.claude/skills/sc-adversarial-protocol/` (currently has drift — will be reconciled by source edits + sync, not hand-edits)
  - `.claude/commands/sc/brainstorm.md` (currently has drift — same reconciliation path)

## Acceptance-Scope Anti-Drift Reminders

- Phase 3 adversarial merge edits target `sc-adversarial-protocol` which is shared with `/sc:adversarial`, `/sc:release-split`, `/sc:roadmap`, etc. Edits must not break these other consumers. Phase 3 items already note: "These edits preserve concrete eval-specific context while allowing live governance improvements to augment the output." Phase 3 Step 3.1 should be done with explicit awareness that requirement-level provenance rules apply broadly, not only to brainstorm.
- Phase 4 evals.json edits must add to cases 4-11 without inventing new eval cases or modifying case 12's existing entry (which remains in evals.json but excluded from comparison per `research/03`).
- Phase 6 acceptance metric thresholds are FIXED at the plan-specified values; Phase 6 must not relax them to claim passing if measured metrics fall short. Missing rerun artifacts → BLOCKED, not PASS.

## Phase 1 Gate Status

All Phase 1 outputs exist:

- ✅ `phase-outputs/discovery/pre-existing-worktree-state.md` (Step 1.0)
- ✅ `phase-outputs/discovery/safety-scope-confirmation.md` (Steps 1.2 + 1.3, including Scope Note)
- ✅ `phase-outputs/reports/phase-1-scope-summary.md` (Step 1.4, this file)

No fabricated evidence. All claims trace to the remediation plan, research bundle, or scoped git status.

**Ready for PG-1 rf-qa adversarial review.**
