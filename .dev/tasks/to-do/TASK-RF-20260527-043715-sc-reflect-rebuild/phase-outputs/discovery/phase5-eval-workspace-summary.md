# Phase 5 Eval Workspace Summary

**Total files:** 34 under `.dev/eval-workspaces/sc-reflect/`
**Total lines:** 3,661

## Top-level workspace files (researcher 01 rows C1-C3, C5, C10)

| File | Lines | Row | Status |
|------|-------|-----|--------|
| `SPEC.md` | 1706 | C1 | PRESENT (Option A: verbatim copy of merged-requirements.md) |
| `grader.py` | 492 | C2 | PRESENT (sc-brainstorm baseline + 10 new assertion-type implementations) |
| `aggregate_iteration.py` | 163 | C3 | PRESENT (verbatim copy of sc-brainstorm; sc-brainstorm → sc-reflect substitution applied) |
| `evals/evals.json` | 414 | C5 | PRESENT (20 entries: 3 pilot + 15 promotion + 2 falsifier) |
| `iterations/.gitkeep` | 0 | C10 | PRESENT (0 bytes) |
| `skill-snapshot/reflect-v1.md` | 111 | (Phase 1) | PRESENT (frozen from Phase 1 Step 1.4; unmodified) |

## Pilot eval case directories (researcher 01 row C4)

| Case dir | Files | Status |
|----------|-------|--------|
| `cases/pre-trivial-coverage-gap/` | input/spec.md, input/tasklist.md, expected.yaml | PRESENT (3 stub files) |
| `cases/post-small-diff-clean/` | input/diff.patch, input/tasklist.md, expected.yaml | PRESENT (3 stub files) |
| `cases/post-large-diff-mixed/` | input/diff.patch, input/tasklist.md, expected.yaml | PRESENT (3 stub files) |

## 15 Promotion fixture YAMLs (researcher 01 row C5-extension; spec §14.5.7 bullets 1-15)

All 15 fixtures land at `.dev/eval-workspaces/sc-reflect/cases/promotion/` and parse as valid YAML:

- promotion-task-strict-pass.yaml (bullet 1, action: moved)
- promotion-blocked-by-drift.yaml (bullet 2, action: rejected)
- promotion-blocked-by-frontmatter-missing.yaml (bullet 3, action: rejected)
- promotion-blocked-by-frontmatter-mismatch.yaml (bullet 4, action: rejected)
- promotion-blocked-by-grounding-gaps-empty-list.yaml (bullet 5, action: rejected)
- promotion-blocked-by-null-convergence.yaml (bullet 6, action: rejected)
- promotion-citation-revalidation-after-remediation.yaml (bullet 7, action: moved)
- promotion-sprint-release-pass.yaml (bullet 8, action: moved)
- promotion-collision-non-identical.yaml (bullet 9, action: rejected)
- promotion-collision-identical.yaml (bullet 10, action: already-promoted)
- promotion-no-promote-flag.yaml (bullet 11, action: skipped)
- promotion-promote-anyway-on-partial.yaml (bullet 12, action: moved)
- promotion-dry-run.yaml (bullet 13, action: dry-run)
- promotion-cross-fs-crash-recovery.yaml (bullet 14, action: resumed)
- promotion-log-pre-write-survives-crash.yaml (bullet 15, action: reconciled-from-log)

## 4 Falsifier-suite files (researcher 01 rows C6-C9; spec §12.5)

| File | Lines | Row | Status |
|------|-------|-----|--------|
| `cases/falsifier-suite/README.md` | 56 | C6 | PRESENT (documents dual-state lifecycle + iteration-3 promotion checklist) |
| `cases/falsifier-suite/T2-converges-on-wrong.yaml` | 25 | C7 | PRESENT (status: skeleton-pending-iteration-3-fixture, byte-exact) |
| `cases/falsifier-suite/T2-judge-class-collision.yaml` | 25 | C8 | PRESENT (status: skeleton-pending-iteration-3-fixture, byte-exact) |
| `cases/falsifier-suite/fixtures/spec-with-deliberate-misclassification.md` | 33 | C9 | PRESENT (placeholder with TODO_ITERATION_3 block) |

## Validity checks

- `evals.json` parses as valid JSON: ✅
- 20 evals entries; IDs unique 1-20: ✅
- Distribution: 3 pilot + 15 promotion + 2 falsifier: ✅
- 18 grading_criteria assertion types listed (8 baseline + 10 new): ✅
- `grader.py` parses as valid Python 3 (`ast.parse`): ✅
- `aggregate_iteration.py` parses as valid Python 3: ✅
- All `cases/**/*.yaml` (15 promotion + 2 falsifier + 3 expected.yaml = 20 files) parse as valid YAML: ✅ (0 failures)
- Falsifier YAMLs have byte-exact `status: skeleton-pending-iteration-3-fixture`: ✅ (both)
- `iterations/.gitkeep` is 0 bytes: ✅
- `skill-snapshot/reflect-v1.md` unchanged from Phase 1 (111 lines, byte-frozen): ✅

## Notes / Deviations

- **Promotion fixture YAML schema cleanup**: Two stubs (`promotion-collision-identical.yaml`, `promotion-no-promote-flag.yaml`) initially failed YAML parse due to unquoted colons inside description strings — fixed in-place by quoting the descriptions.
- **Falsifier YAML schema cleanup**: Both falsifier skeletons initially failed YAML parse due to backticks + colons in unquoted TODO_ITERATION_3 list items — fixed in-place by quoting each list item.
- **grader.py extension count**: 10 new assertion-type implementations added (citation_resolves, regex_present, regex_absent, yaml_list_contains, matrix_covers_items, checkpoint_logged, deviation_class_matches, path_exists, path_does_not_exist, falsifier_skeleton_present) — 2 more than the BUILD_REQUEST's "8 new" framing because grader-extensions.md spec'd 10 distinct types. All 10 are registered in the `check_assertion` dispatcher AND listed in evals.json's `grading_criteria`.
- **Pilot case fixtures shipped as STUBS** per Phase 5 Steps 5.6/5.7/5.8 explicit stub directive. Full content is iteration-1 follow-up.
- **Promotion fixtures shipped as STUBS** per Phase 5 Steps 5.10-5.24 explicit stub directive. Full content is iteration-1 follow-up.
- **Falsifier fixture content (`fixtures/spec-with-deliberate-misclassification.md`)** is a PLACEHOLDER per W-A8 spec-panel fix. Iteration-3 follow-up authors the deliberately-misclassified content and promotes both falsifier YAMLs to `status: active`.
