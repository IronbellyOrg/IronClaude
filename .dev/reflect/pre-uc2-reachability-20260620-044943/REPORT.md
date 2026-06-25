# sc:reflect UC-1 PRE Gate — FR-RSR tasklist audit

**Mode:** pre (UC-1)  
**Depth:** deep  
**Tier reached:** 2  
**Status:** FAILED — tasklist is not safe to execute as written  
**Spec:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-1-uc2-reachability/spec.md`  
**Tasklist:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md`  
**TDD considered:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-1-uc2-reachability/tdd.md`

## Verdict

```yaml
status: failed
coverage_pct: 0.917          # 16.5 / 18 weighted groups
coverage_undefined: false
unmapped_requirements: []
best_practice_grade: 2
needs_human_decision: true
blocked_by_low_confidence: false
recommended_action: remediate_tasklist_before_execution
```

The tasklist has broad nominal coverage, but Tier 2 review found **critical pre-execution blockers** that can let the work falsely mark itself complete or contaminate staging. The prior pre-report passed on coverage; this rerun applies the deep task-safety lens and rejects the tasklist until the blockers below are fixed.

## Coverage summary

The tasklist covers the implementation spine: source-of-truth ref, gather + contract, gate, classify, surface, falsify, final QA, and release are all present in phase headings or objectives. The spec defines FR-RSR.10 as an active real-fixture eval requirement that must fail pre-change and pass post-change, with companions and count-invariant assertions (`spec.md:517-539`). The TDD release criteria require the same eval outcome, the release checklist, and byte-identical determinism (`tdd.md:977-998`).

Weighted coverage is **16.5/18 = 0.917**:

- Covered: FR-RSR.1–9, NFR-RSR.1/3/4/5/6, blocker ordering.
- Partial: FR-RSR.10, NFR-RSR.2, release checklist.
- Missing: none.

See `artifacts/coverage-matrix.yaml` for the detailed map.

## Blocking findings

### C1 — Verification/release failures can still be marked complete

Multiple verification gates say that if verification fails or a blocker remains, the executor should log the blocker and then mark the checklist item complete. Examples include Phase 4 verification (`tasklist.md:223`) and the release checklist (`tasklist.md:351`). The TDD requires the DoD and release checklist to actually pass, including sync, evals, unchanged-field assertions, counter hygiene, and determinism (`tdd.md:977-998`).

**Impact:** a failed `make verify-sync`, failed acceptance criterion, missing artifact, or failed release checklist line can become a completed checklist item. That defeats the pre-execution task discipline.

**Required correction:** for verification/release gates, replace “log blocker then mark complete” with “log blocker and HALT / leave unchecked.” Only mark an item complete after the stated acceptance criteria pass.

### C2 — FR-RSR.10 and NFR-RSR.2 can be downgraded from executed evidence to structural inspection

FR-RSR.10 requires the headline eval to be active, use real fixtures, fail against the pre-change skill, and pass against the post-change skill (`spec.md:517-539`). The TDD repeats that the headline must fail-pre/pass-post and that determinism is a byte-identical two-run ledger check (`tdd.md:987-998`).

The tasklist’s Step 7.8 allows a “STRUCTURAL COMPLETENESS” path if no runner/producer exists, and Step 7.9 allows determinism to be asserted by inspection rather than by executing a two-run byte-compare (`tasklist.md:289-295`).

**Impact:** the core falsifiability gate can pass without proving the pre-change failure, post-change pass, or deterministic ledger.

**Required correction:** make no-runner/no-producer a BLOCKED release state, or add a task that materializes eval outputs and actually executes both `old_skill/` and `with_skill/` plus the two-run determinism check.

### C3 — POST reflect wrapper stages unrelated work with `git add -A`

The tasklist’s penultimate POST reflect command contains `git -C /config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3 add -A` (`tasklist.md:363`). The current working tree has many unrelated untracked `.dev/` directories. A broad `git add -A` would stage all of them, not just this task’s implementation.

**Impact:** release/post-reflect can contaminate the index with unrelated artifacts and invalidate source-of-truth/staging checks.

**Required correction:** remove `git add -A` from the wrapper command. Use explicit pathspec staging for intended files only, or run the wrapper against `start_commit` without staging.

### C4 — Step 3 insertion order contradicts the verified research anchor

The tasklist instructs inserting new §6.1 steps 4b'/4b after existing step 4a (`tasklist.md:199-203`). The verified research anchor says the new steps belong between step 4 `find_referencing_symbols` and existing step 4a, because the new sweep consumes the already-fetched referrer set (`research/01-skill-gather-gate-anchors.md:74-86`).

**Impact:** the executor receives contradictory instructions on a load-bearing insertion point.

**Required correction:** either insert the runtime-surface tagger/sweep between step 4 and 4a, or explicitly update the research/TDD with the justified alternate ordering before execution.

### C5 — Count-invariant fallback can add an undocumented seventh emitted field

The spec says FR-RSR.7 adds exactly six fields: `runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_ledger_path`, `runtime_surface_unreached`, `runtime_surface_degraded`, and `unreached_surfaces[]` (`spec.md:445-449`). Step 7.1 correctly prefers a full-YAML grader assertion, but its fallback allows the producer to emit `unreached_surfaces_len` (`tasklist.md:263`).

**Impact:** if the fallback is used, the implementation can drift beyond the additive contract without updating spec/TDD.

**Required correction:** make the full-YAML grader assertion mandatory. If a grader change is disallowed, halt and update the design instead of adding a seventh emitted field.

## Non-blocking notes

- The codebase-over-doc reconciliation placing eval cases under `cases/uc2-*/` while the registry lives under `evals/evals.json` is acceptable for this repo convention and is not counted as a gap.
- Core scope and source-of-truth constraints are well represented; the failure is not lack of task volume, but unsafe gate semantics.

## Required next move

Do **not** execute this tasklist yet. Author a corrective tasklist revision that:

1. Converts all verification/release “log blocker then complete” paths into hard halts / unchecked items.
2. Requires executed FR-RSR.10 fail-pre/pass-post and NFR-RSR.2 two-run determinism, or marks the task blocked until a runner exists.
3. Removes `git add -A` from the post-reflect wrapper.
4. Reconciles the §6.1 insertion-order conflict.
5. Removes the undocumented `unreached_surfaces_len` fallback or updates the design explicitly.

## Artifact index

- `return-contract.yaml`
- `audit.log`
- `artifacts/input-snapshot.yaml`
- `artifacts/tier_decision.yaml`
- `artifacts/coverage-matrix.yaml`
- `artifacts/gap-register.yaml`
- `reviewer-cards/requirements-analyst.md`
- `reviewer-cards/qa-qualitative.md`
- `reviewer-cards/evidence-validator.md`
