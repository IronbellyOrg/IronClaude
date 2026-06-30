# Research 04 — Doc Cross-Validator

Status: Complete

## Scope

Doc cross-validation for Option C against current reflect prose and implementation, focused on:

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md`
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md`

## Option C requirements from merged recommendation

Source: `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md`.

- Option C is explicitly a funded non-blocking fast-follow after near-term Option A, not the near-term merge target; lines 10-12 select A now and C later, and lines 33-35 introduce the separate A→C fast-follow as subtractive/narrowing on existing graded machinery.
- C1, non-collapsing unsatisfiable exclusion: remove destructive tier collapse. If executor-class collision cannot reach disjoint N=2, stay Tier-2, fill best-available distinct classes, and emit `executor_exclusion_unsatisfiable: true` plus `t2_model_class_diversity: degraded` (`merged-decisionA-recommendation.md:35-36`).
- C2, reliable-source trigger only: narrow exclusion to `executor_class_source ∈ {flag, env, frontmatter}` and drop `log-heuristic` from the trigger (`merged-decisionA-recommendation.md:37-37`).
- C3, reflect-side reader: add reflect-side reader for `executor_model_class`, which task-builder frontmatter writes but reflect does not read in the target behavior (`merged-decisionA-recommendation.md:38-38`).
- C4, waived-not-failed invariant: gate the graded invariant `executor_model_class NOT IN reviewer_model_classes` on identity reliability; assert when reliable, waive rather than fail when unreliable (`merged-decisionA-recommendation.md:39-39`).
- C5, eval: prove same-class panel avoidance when identity is reliable, and prove the unsatisfiable branch stays Tier-2 (`merged-decisionA-recommendation.md:40-40`).
- Open-item telemetry priority: resolver hit-rate is unmeasured; emit/check `executor_class_source` and distinguish reliable `flag|env|frontmatter` from unreliable `log-heuristic|unknown` (`merged-decisionA-recommendation.md:42-44`).

## Current implementation facts relevant to Option C

- CODE-VERIFIED: The Python wrapper already reads executor identity from `EXECUTOR_MODEL_CLASS` first and tasklist frontmatter `executor_model_class` second, then stores it in `ReflectConfig.executor_model` (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/cli/reflect/config.py:53-56`, `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/cli/reflect/config.py:338-344`, `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/cli/reflect/models.py:66-72`). It does not record an `executor_class_source` field.
- CODE-VERIFIED: When `ReflectConfig.executor_model` is present, the wrapper forwards it into the generated `/sc:reflect` prompt as `--executor-model <value>` (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/cli/reflect/runner.py:350-377`).
- CODE-VERIFIED: The public `superclaude reflect run` Click surface does not define a `--executor-model` option; executor identity is currently env/frontmatter-only at the wrapper CLI layer (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/cli/reflect/commands.py:76-179`). The doc⇆CLI parity test explicitly calls a documented `--executor-model` a non-existent flag example and treats Click as the source of truth (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_docs_cli_parity.py:1-11`, `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_docs_cli_parity.py:83-92`).
- CODE-VERIFIED: Current Tier-2 contract construction uses succeeded worker count to set `tier_reached = 2` when at least two reviewers succeed, otherwise `tier_reached = 1` and `merge_method = single-reviewer-fallback` (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/cli/reflect/ensemble.py:516-523`). This is a reviewer-survival collapse, not an executor-exclusion collision collapse.
- CODE-VERIFIED: Current `t2_model_class_diversity` is computed from distinct succeeded `worker.model_id` values and returns `full` for at least two distinct model IDs, otherwise `insufficient` (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/cli/reflect/ensemble.py:571-579`). That implementation does not match the prose contract enum `full | degraded` when diversity is not full.
- CODE-VERIFIED: `derive_verdict` degrades any non-`full` `t2_model_class_diversity` value, including `insufficient` (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/src/superclaude/cli/reflect/contract.py:249-269`). Existing tests expect duplicate-model survivors to return non-`full` diversity and produce a degraded exit (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:230-247`).
- CODE-VERIFIED: The current positive Tier-2 witness requires `tier_reached == 2`, `merge_method != single-reviewer-fallback`, `reviewer_count >= 2`, and `t2_model_class_diversity == full` (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:125-138`). One-reviewer and M==1 cases are deliberate degraded/single-reviewer fallback witnesses (`/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:174-197`, `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:251-277`).

## Current scoped prose claims and status tags

### `/src/superclaude/skills/sc-reflect-protocol/SKILL.md`

- CODE-CONTRADICTED against Option C: §3.1 says `--executor-model <class>` is accepted and ignored; no class is removed, no tier degrade occurs, and no `executor_exclusion_degraded` is emitted (`SKILL.md:89-90`). Option C requires reliable-source executor identity to trigger exclusion and requires unsatisfiable telemetry rather than ignoring identity (`merged-decisionA-recommendation.md:35-40`).
- CODE-CONTRADICTED against Option C: §7.1 states the executor model class is never removed from the reviewer pool, `EXECUTOR_MODEL_CLASS` is recorded provenance only, and there is no Wave-0 executor-class-resolution sub-step (`SKILL.md:621-629`). Option C requires reliable-source exclusion and a reader/source classification surface.
- CODE-CONTRADICTED against Option C: §11.3 says no executor-class exclusion is applied and no `executor_class ∉ reviewer_classes` assertion is graded (`SKILL.md:1215-1219`). Option C requires that invariant asserted when reliable and waived when unreliable.
- CODE-CONTRADICTED by current code enum: §4 and §9.1 say `t2_model_class_diversity ∈ {full, degraded}` (`SKILL.md:223-227`, `SKILL.md:805-815`), but `compute_model_class_diversity()` currently returns `insufficient` when fewer than two distinct succeeded model IDs exist (`ensemble.py:571-579`). The implementation task should normalize this while preserving existing degraded verdict behavior.
- UNVERIFIED/stale baseline risk: §9.1 change note says contract 1.5.1 replaced executor-class exclusion with instance-level anti-self-confirmation and removed `executor_class_source` / `executor_class_resolved` / `executor_exclusion_degraded` as non-stable telemetry (`SKILL.md:696-699`). Option C explicitly asks to reintroduce source telemetry and reliable-source gating; the task must not treat this note as a continuing design constraint.
- CODE-VERIFIED: §9.1 stable contract currently includes `t2_model_class_diversity`, `calibrator_diversity`, and `contract_version: "1.7.0"` (`SKILL.md:696-699`, `SKILL.md:805-815`). Any Option C contract additions should be documented as additive to 1.7.0 or bump the contract version deliberately.

### `/src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`

- CODE-CONTRADICTED against Option C: The reviewer spec says the executor's model class is never removed from the reviewer pool, `--executor-model` / `EXECUTOR_MODEL_CLASS` are ignored for composition, no tier is degraded, `executor_exclusion_degraded` is not emitted, and no Wave-0 0.5b executor-class-resolution step exists (`reviewer-spec.md:86-90`). Option C requires reliable-source exclusion, unreliable-source waiver, and unsatisfiable non-collapse telemetry.
- CODE-CONTRADICTED against Option C: The class-diversity preference says reflect never drops a slot, degrades a tier, or excludes a class for diversity, and `degraded` is only a missed diversity bonus (`reviewer-spec.md:90-90`). Option C should preserve “never drop a slot / never collapse Tier-2” but must add “exclude executor class when reliable and satisfiable” and “emit degraded diversity when unsatisfiable.”
- CODE-CONTRADICTED against Option C: Rotation fill logic says no class is removed for matching executor class and T2 floor is reached only when fewer than two slots can be filled at all, never due to executor-class collision (`reviewer-spec.md:100-106`). Option C requires executor collision handling, but with the same non-collapse property when exclusion is unsatisfiable.
- UNVERIFIED/possibly internally contradictory stale prose: The Khan collision section says executor, reviewers, and calibrator/judge form a partition and reflect enforces executor-vs-reviewer disjointness (`reviewer-spec.md:108-112`), while the immediately preceding sections say executor class is never removed (`reviewer-spec.md:86-106`). The implementation task must avoid using this partition paragraph as current fact unless it is rewritten into the Option C rule.

### `/src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md`

- CODE-CONTRADICTED against Option C: The rubric says the executor class is deliberately not separated from reviewer classes and no executor-class exclusion is applied (`reflection-rubric.md:162-168`). Option C requires reliable-source separation when satisfiable.
- CODE-CONTRADICTED against Option C: The grader assertion section says only `calibrator_model_class NOT IN reviewer_model_classes` is asserted and there is no executor-class grader assertion because executor class may legitimately appear in the reviewer pool (`reflection-rubric.md:171-173`). Option C requires a conditional executor invariant: assert when `executor_class_source ∈ {flag, env, frontmatter}`, waive-not-fail otherwise.
- CODE-VERIFIED outside Option C: The calibrator/reviewer disjoint-set itself remains valid: calibrator class is selected outside reviewer classes when possible and emits `calibrator_diversity: full|degraded` (`reflection-rubric.md:134-153`). Option C should not alter calibrator-vs-reviewer separation except to distinguish it from executor-vs-reviewer separation.

## Required prose updates for the implementation task

1. Replace all instance-level-only language with hybrid language:
   - In `SKILL.md` §3.1, §7.1, §9.1 notes, §11.3, §12/eval assertions, and any downstream grader rows.
   - In `refs/reviewer-spec.md` Composition / Instance-level independence / Rotation fill logic / Khan collision section.
   - In `refs/reflection-rubric.md` Calibrator/reviewer disjoint-set and grader assertion sections.
2. Define an executor-class source contract:
   - `executor_class_source: flag | env | frontmatter | log-heuristic | unknown`.
   - Reliable trigger set is exactly `{flag, env, frontmatter}` per Option C.
   - `log-heuristic` and `unknown` must never fail the invariant; they waive it and should emit loud telemetry.
3. Define the reliable-source composition rule:
   - If reliable executor class is known and at least two non-executor reviewer classes are available/succeed, select/fill Tier-2 reviewers from non-executor classes.
   - Assert `executor_model_class NOT IN reviewer_model_classes` only on the reliable/satisfiable path.
4. Define the unsatisfiable composition rule:
   - If reliable executor class is known but disjoint N=2 is impossible, stay Tier-2 with best-available distinct classes.
   - Emit `executor_exclusion_unsatisfiable: true` and `t2_model_class_diversity: degraded`.
   - Do not route to T1, do not set `single-reviewer-fallback` solely because of executor exclusion, and do not fail the run solely for the unavoidable collision.
5. Define unreliable-source waiver rule:
   - If source is `log-heuristic` or `unknown`, do not assert the executor-exclusion invariant.
   - Emit source telemetry and a waived status, not a failure.
6. Normalize `t2_model_class_diversity` docs and code to one enum. Current docs require `full|degraded`; current code returns `insufficient` for non-full diversity. The generated task should require `degraded` unless another explicit contract-version bump is chosen.
7. Update eval/grader assertions:
   - Add positive reliable-source same-class-avoidance witness.
   - Add reliable-source unsatisfiable witness that stays Tier-2 and emits `executor_exclusion_unsatisfiable: true` + degraded diversity.
   - Add unreliable-source/log-heuristic witness that waives the executor invariant rather than failing.
   - Preserve existing M==1/single-reviewer fallback tests for actual reviewer failures; do not conflate them with unsatisfiable executor exclusion.

## Precondition halt language for the generated task

Use this precondition in the MDTM task before implementation steps:

> PRECONDITION — baseline check: Before editing, inspect current `SKILL.md`, `refs/reviewer-spec.md`, `refs/reflection-rubric.md`, and reflect Python code for the expected Option-A executor-class exclusion baseline. If the baseline is present, proceed with the A→C subtractive/narrowing edits. If the baseline is absent or the files instead contain instance-level-only / no-exclusion language, STOP the “subtractive edit” plan and switch to an explicit “restore hybrid from instance-level baseline” implementation plan; do not silently treat no-exclusion prose as Option A. Record the mismatch in the task log and require the final docs to state the hybrid contract, not the old instance-level contract.

Rationale: the merged recommendation frames C as subtractive/narrowing on an existing Option-A baseline (`merged-decisionA-recommendation.md:33-40`), but the current scoped docs are instance-level/no-exclusion in the exact sections listed above.

## Stale or contradictory docs the generated task must not use as facts

- Do not use `SKILL.md:89-90`, `SKILL.md:621-629`, `reviewer-spec.md:86-90`, or `reflection-rubric.md:162-173` as target design facts; they are the current instance-level-only design and conflict with Option C.
- Do not use `SKILL.md:696-699` as a reason to avoid reintroducing executor source telemetry; Option C explicitly needs source reliability telemetry and conditional gating.
- Do not copy the exact `t2_model_class_diversity: full | degraded` prose without fixing the current code path that emits `insufficient` (`ensemble.py:571-579`).
- Do not conflate actual reviewer-survival collapse (`reviewer_count < 2`, `single-reviewer-fallback`) with executor-exclusion unsatisfiable. Option C says unsatisfiable exclusion stays Tier-2.
- Do not document `--executor-model` as a real `superclaude reflect run` CLI option unless the Click command is changed too; the current CLI has no such option and parity tests guard against phantom flags (`commands.py:76-179`, `test_docs_cli_parity.py:83-92`). If “flag” remains part of the source enum, specify whether it is `/sc:reflect`-internal, wrapper-generated, or a newly added wrapper CLI flag.

## Summary

The scoped prose currently documents #197-style instance-level anti-self-confirmation and explicitly rejects executor-class exclusion. Current code partially reads executor identity from env/frontmatter and forwards it to `/sc:reflect`, but it does not record source reliability, does not exclude same-class reviewers, does not assert/waive the executor invariant, and uses `insufficient` where the docs claim `degraded`. The implementation task should first halt on the absent Option-A baseline, then implement/document the hybrid as a net-new restoration from the current no-exclusion baseline: reliable-source exclusion, unreliable-source waiver, and non-collapsing degraded Tier-2 when exclusion is unsatisfiable.
