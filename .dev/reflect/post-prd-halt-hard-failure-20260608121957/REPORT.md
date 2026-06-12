# /sc:reflect REPORT — UC-2 post, Tier 2 (deep)

**Mode:** post · **Tier reached:** 2 (forced by `--depth deep`) · **Status:** `partial` (1 Drift finding)
**Calibrated confidence:** 0.86 · **Promotion:** skipped (gate-failed cond-4 + uncommitted)
**Date:** 2026-06-08 · **Output:** `.dev/reflect/post-prd-halt-hard-failure-20260608121957/`

**Subject:** the just-completed two-atom PRD-pipeline halt/missing-artifact fix (5 files, 307 insertions, uncommitted).
**Spec authority:** `research/00-troubleshoot-report.md` "Proposed Fix".

## Ensemble

3 heterogeneous-model reviewers ran in parallel with adversarial stance + distinct lenses:

| Reviewer | Model | Lens | Verdict | Self-conf |
|----------|-------|------|---------|-----------|
| R1 | sonnet | analyzer (control-flow) | minor-issues | 0.90 |
| R2 | haiku | qa (test integrity) | minor-issues | 0.88 |
| R3 | opus | refactorer (design) | minor-issues | 0.86 |

Cross-class convergence on the headline finding = **3/3** (computed convergence 0.83). Per §11.4, agreement across model classes is itself evidence the finding survives a representational frame change. **Caveat (§7.1):** reviewer R3 shares the executor's model class (opus) — `executor_exclusion_degraded: true`; its independence is structurally weaker, flagged in telemetry. The two non-opus reviewers (sonnet, haiku) independently reached the same finding, so the convergence does not rest on the same-class reviewer.

## Headline finding (GROUNDED, evidence-validator-confirmed)

### F1 [IMPORTANT / Drift] — Atom 2's artifact-specific `halt_reason` never reaches the pipeline level; the field is set-but-never-read in production

**All three reviewers, independently.** Evidence re-verified at gate time:

- `executor.py:578-584` — when a HALT step result returns to the Stage-A loop, the loop **unconditionally** rebuilds `result.halt_reason` from a template → `f"hard failure: {status.value}"` = literally `"hard failure: halt"`.
- `models.py:248` — Atom 2 added `PrdStepResult.halt_reason`; `_run_subprocess_step` (executor.py:696-699) sets it to the rich `"missing required artifact scope-discovery-raw.md (producer: scope-discovery)"`.
- **`grep` confirms zero production readers** of that step-level field — it is consumed only by the direct-call unit test `test_missing_required_artifact_yields_graceful_halt` (test_e2e.py:837-839), which bypasses the loop.

**Why it matters.** The spec's stated intent for Atom 2 is that a missing artifact "surfaces as a graceful pipeline halt" with "a clear `halt_reason`" (report:86, 112). The named backstop scenario is `--resume-from research-notes` against a missing `scope-discovery-raw.md` — there scope-discovery is *skipped*, so no ERROR is generated; research-notes reaches `_build_prompt` → `MissingArtifactError` → HALT carrying the rich reason — and then the loop discards it. The operator sees `"hard failure: halt"` and `resume_command()` gives no clue which artifact was missing. The crash is fixed, but the field Atom 2 introduced is dead in production.

**Classification:** Drift (a quality gap vs spec *intent*; no hard acceptance criterion contradicted and all 157 tests pass → not Regression). This refines the Tier-1 verdict, which noted the tradeoff but left the loop untouched to avoid re-editing the PG-1-verified block. The ensemble's point stands: that decision orphaned the new field.

**Recommended fix (4 lines, low-risk).** Make the loop prefer the step's own reason:
```python
result.halt_reason = step_result.halt_reason or (
    f"hard failure: {step_result.status.value}"
    if step_result.status.is_hard_failure
    else f"STRICT gate failure: {step_result.status.value}"
)
```
Atom-1 tests still pass (ERROR results carry `halt_reason=None` → fall back to the template → `test_e2e_standard_tier_error_halts_pipeline` still finds `"hard failure"`). Add one run-level test driving `resume_from="research-notes"` with no scope artifact, asserting the artifact name survives to `result.halt_reason`.

## Secondary findings (recommendations, non-gating)

### F2 [IMPORTANT / out-of-spec-scope] — malformed-but-present JSON crashes the CLI (R1, R2)
`_load_json_required` (prompts.py:74-78) guards only file *absence*. A present-but-corrupt `parsed-request.json` makes `_load_json` raise `json.JSONDecodeError` (a `ValueError`, not `OSError`) — uncaught by `except MissingArtifactError`, so it escapes `run()` exactly like the original bug, for a different input. The spec scoped Atom 2 to *missing* artifacts, so this is **not a deviation** — it's a latent robustness follow-up. Fix: catch `json.JSONDecodeError` in `_load_json_required` and re-raise a typed error the call site already handles.

### F3 [MINOR / test hygiene] — `test_e2e_scope_discovery_error_halts_before_research_notes` mislabeled (R1, R2, R3)
Docstring says "[Atom 2 e2e]" but the test stubs `_build_prompt` (test_e2e.py:875-878), so it exercises **Atom 1** (ERROR halts at scope-discovery), never the `MissingArtifactError` path. Atom 2 is genuinely covered by `test_missing_required_artifact_yields_graceful_halt`. Fix: relabel as Atom 1, or add a no-stub run-level Atom-2 reproduction (folds into F1's test).

### F4 [MINOR / latent coupling] — hardcoded producer strings duplicate `_STEP_ARTIFACT_FILES` (R3)
The producer literals (`"parse-request"`, `"scope-discovery"`, `"research-notes"`) at prompts.py:190/291/294/378/479 re-encode the inverse of the canonical step→artifact map (`executor.py:252-263`) by hand, in a different module, unpinned by any test. **Correct today** (all 5 verified against the real step IDs) — flagged as drift-prone on the next step rename.

### F5 [MINOR / weak assertion] — `test_e2e_standard_tier_validation_fail_does_not_halt` (R2)
Asserts only that the halt wasn't at scope-discovery and that research-notes ran; does not assert `scope-discovery` status == `VALIDATION_FAIL`. Could pass for the wrong reason. Fix: assert the recorded scope-discovery step status is `VALIDATION_FAIL`.

## What the ensemble VERIFIED sound (no issue)
- Stage-A boolean logic traced for every status; `is_hard_failure ⊆ is_failure` confirmed → outer guard never shadows a hard failure; VALIDATION_FAIL non-fatal path preserved.
- `except MissingArtifactError` at the real call site (not inside `_build_prompt`); no collision with the later `except OSError` (separate try block); plain `FileNotFoundError` from unconverted reads correctly NOT swallowed.
- Exactly 5 required reads converted with type-correct helper; 4 Stage-B `.is_file()` reads + skill_refs reads untouched; no over-conversion.
- Tuple-vs-set idiom: behavior-identical, matches sibling predicates — a consistency improvement over the spec sketch, not a defect.
- Local `from .prompts import MissingArtifactError` matches house style (mirrors `_build_prompt`'s local import); no circular-import risk.
- Independent `uv run pytest tests/cli/prd/` → **157 passed**.

## Deviation register (4-category)

| Class | Count | Items |
|-------|-------|-------|
| Authorized | 0 | — |
| Necessary | 2 | N1 `halt_reason` field added to PrdStepResult (spec assumed it existed); N2 tuple membership idiom |
| **Drift** | **1** | **F1 — step-level `halt_reason` orphaned; spec's "clear halt_reason at pipeline level" intent unmet** |
| Regression | 0 | — (all 157 tests pass; no criterion contradicted) |

## Promotion gate (9-condition) — RESULT: BLOCKED

| Cond | Check | Result |
|------|-------|--------|
| 1 mode==post | ✓ | pass |
| 2 status==success | status=partial | **fail** |
| 3 completion==1.0 | ✓ | pass |
| 4 drift==0 ∧ regression==0 | drift=1 | **fail** |
| 5a/5b frontmatter present + done | ✓ (🟢 Done) | pass |
| 6a/6b citations_dropped==0 + no gaps | ✓ | pass |
| 7 no input_drift | ✓ | pass |
| 8 no user-decision pending | needs_human_decision | **fail** |
| 9 convergence non-null @T2 | 0.83 | pass |

**Promotion: SKIPPED** (cond 2/4/8 fail). Independent of the gate, the work is **uncommitted** and the user directed no auto-mutation. No filesystem move performed. Had it passed, the move would have been:
`mv .dev/tasks/to-do/TASK-RF-20260608-021500 .dev/tasks/done/TASK-RF-20260608-021500`

## Post-report remediation applied (operator-approved)

After this report, the operator approved "Apply F1 + run-level test". Applied:
- **F1 fix** — `executor.py:577-589`: the Stage-A halt now sets `result.halt_reason = step_result.halt_reason or <template>`, so Atom 2's artifact-specific reason surfaces at the pipeline level. Atom-1 ERROR/TIMEOUT results carry `halt_reason=None` and still fall back to the template.
- **F3 fix** — corrected the misleading "[Atom 2 e2e]" docstring on `test_e2e_scope_discovery_error_halts_before_research_notes` (it exercises Atom 1).
- **New run-level test** — `test_e2e_resume_missing_artifact_surfaces_reason_at_pipeline_level`: resumes from `research-notes` with `scope-discovery-raw.md` absent, runs the REAL `_build_prompt`, asserts `result.halt_reason` carries the missing artifact + producer at the pipeline level (the regression guard F1 lacked).
- **Verification** — `uv run pytest tests/cli/prd/` → **158 passed**; ruff clean on edited files.

With F1 resolved, the Drift finding is closed and `PrdStepResult.halt_reason` is now read in production. F2 (malformed-JSON), F4 (producer-string coupling), F5 (weak assertion) remain optional follow-ups.

## Bottom line

The fix is **functionally correct and fully tested** — it genuinely closes the reported crash. The deep Tier-2 ensemble surfaced one real, grounded quality gap the fast pass under-weighted: **Atom 2's artifact-specific halt reason is produced but thrown away before the operator can see it, leaving the new `PrdStepResult.halt_reason` field dead in production.** It is a 4-line fix. Recommend applying F1 (and folding in F3's run-level test) before committing/archiving; F2/F4/F5 are optional hardening.
