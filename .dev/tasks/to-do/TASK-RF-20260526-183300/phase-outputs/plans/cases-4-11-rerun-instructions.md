---
phase: 6
step: 6.1
title: Cases 4-11 Rerun Instructions
status: pending operator execution
created_date: 2026-05-26
task_id: TASK-RF-20260526-183300
---

# Cases 4-11 Rerun Instructions

This plan provides the exact procedure to regenerate live `/sc:brainstorm` artifacts for cases 4-11 against the Phase 2-3 remediation. Cases must rerun to produce fresh post-remediation evidence; this task's executor cannot autonomously invoke `/sc:brainstorm` (each invocation is a separate operator session that writes live artifacts), so acceptance for Phase 6.3 / 6.4 / PG-6 remains BLOCKED until the rerun completes.

Case 12 (`architecture-graphql-public-api`) is EXCLUDED from this rerun. Live invocation is blocked by `Unknown skill: sc:brainstorm-protocol`; bringing it into scope requires a separate registry-compatibility task.

## Prerequisite (one-time, already done)

- Phase 2-3 source edits propagated to `.claude/` mirrors via `make sync-dev` and verified by `make verify-sync` (Phase 5 Steps 5.2-5.3, both PASS).
- Phase 4 eval harness changes (`evals.json` per-case keys + assertions block; `grader.py` new parser + assertion branches; `compare_live_runs.py` gap reporting + sync validation) are in place.

## Rerun Procedure (per case)

For each case in `[4, 5, 6, 7, 8, 9, 10, 11]`:

1. Read the case definition from `.dev/eval-workspaces/sc-brainstorm/evals/evals.json`. The `prompt` field is the exact operator input.
2. In a NEW Claude Code session (fresh context), invoke the brainstorm protocol with the case's prompt verbatim:

```
/sc:brainstorm <case prompt verbatim>
```

3. Ensure the protocol writes all required artifacts under `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-<case-name>/`:
   - `seed-brief.md` (with mandatory `## Intent Summary`, `## Context Anchors`, `## Must Preserve`, `## Out of Scope` sections — per Phase 2 schema)
   - `merged-requirements.md` (with canonical frontmatter `schema_version`, `source_seed_brief_path`, `domain`, `strategy`, `adversarial_status`, `convergence_score`, `fit_to_intent`, `unresolved_conflicts` + 6 mandatory sections including dedicated `## Provenance`)
   - `return-contract.yaml` (with `seed_schema_version`, `merged_requirements_schema_version`, `context_anchors_count`, `fit_to_intent`, `fit_to_intent_issues`, `blind_mode`, `source_of_truth_paths` per Phase 2 schema)
   - `adversarial/debate-transcript.md` and other adversarial outputs (per Phase 3 schema — requirement-level provenance, threshold preservation table, dropped-anchor audit when applicable)
   - `handoff/` output if case `handoff` is `tasklist`, `task`, or `design`
   - Optional `timing.json` if the protocol emits telemetry (currently not enforced; absence is reported as explicit availability gap by `compare_live_runs.py`)

4. After the protocol completes, verify the artifact set exists:

```
ls -la .dev/eval-workspaces/sc-brainstorm/live-runs/eval-<case-name>/
```

## Case-by-Case Prompts

Verbatim from `evals.json` (do not paraphrase):

| Case | Name | Prompt |
|------|------|--------|
| 4 | `code-migrate-pytest-vitest` | Brainstorm migration of a test suite from pytest to vitest. Use --depth quick. Use 2 proposals. |
| 5 | `architecture-worker-pool-errors` | Brainstorm redesigning error handling across the worker pool. Use --depth deep. Use 5 proposals. Strategy enterprise. |
| 6 | `process-contributor-onboarding` | Brainstorm improving onboarding workflow for new contributors. Use --depth standard. Strategy agile. |
| 7 | `research-bun-vs-node` | Brainstorm evaluating Bun vs Node for backend services. Use --depth standard. Research deep. No codebase enrichment. |
| 8 | `code-api-caching-tasklist` | Brainstorm adding caching to the API layer. Use --depth standard. Handoff tasklist. |
| 9 | `code-feature-flag-task` | Brainstorm implementing a feature flag system. Use --depth standard. Handoff task. |
| 10 | `incident-payment-webhook-q1` | Brainstorm Q1 incident response for payment webhook delivery failures. Use --depth deep. Strategy enterprise. Simulate interactive dialogue. |
| 11 | `code-duplicate-auth-blind` | Brainstorm consolidating three duplicate auth modules. Use --depth deep. Use blind mode. |

## After All 8 Cases Rerun

Run the regeneration step:

```
uv run python .dev/eval-workspaces/sc-brainstorm/compare_live_runs.py
```

This regenerates `.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.{json,md}` against the fresh post-remediation artifacts.

Then return to this task's executor and proceed to Phase 6 Step 6.2 (post-rerun comparison) and Step 6.3 (acceptance matrix). The blocked steps will then have evidence to evaluate against.

## Expected Improvements (Acceptance Targets)

Per remediation plan lines 419-427 (cases 4-11 acceptance scope):

- Structural pass rate ≥95% (target 100%)
- Qualitative baseline wins ≤2 of 8
- Live qualitative average ≥52/60
- Provenance average ≥8.50
- Concreteness average ≥8.50
- Zero missing dedicated `## Provenance` sections
- Zero critical seed anchors dropped without rationale

## Blocker Status

This step is COMPLETE in the sense that the rerun procedure is fully documented. Steps 6.2, 6.3, 6.4, and PG-6 are BLOCKED pending operator-driven execution of the rerun above; that blocker is intrinsic to the task (the F1 executor cannot autonomously invoke `/sc:brainstorm` for 8 cases in separate fresh sessions). The blocker is reflected in subsequent Phase 6 steps and does not require setting the task's overall status to Blocked at this step — Step 6.4 / PG-6 will surface the BLOCKED acceptance verdict using the templated format.

## Scope Discipline

- Case 12 remains intentionally excluded. Do NOT rerun case 12 unless registry compatibility is brought into scope as a separate task.
- Rerun must use the exact prompts above. Paraphrasing or adding hint text invalidates the comparison.
- Each rerun must occur in a FRESH Claude Code session — running multiple cases in one session would contaminate context and falsely improve outputs.
- Live artifacts must be written under `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-<case-name>/`, NOT into `.claude/` mirrors and NOT into `iterations/iteration-2/` (which is the frozen baseline).
- Do NOT commit `.claude/` paths during the rerun. Generated mirrors remain forbidden to stage.
