---
artifact: r1-3-aggregation
phase: 8
release: R1.3
task: TASK-RF-20260531-042405
created_date: 2026-06-02
worktree_head: daa10416 (parent commit prior to R1.3 changes)
---

# R1.3 Aggregation — `GateCriteria.code_assertions` Slot + First `CodeAssertion`

Aggregates all Phase 8 (R1.3) outputs for the PG8.1 rf-qa task-integrity gate.

## Scope delivered (BUILD-REQUEST §R1.3 / §MVR §2 / §Contract #2 / master:§Flaw 1)

R1.3 extends the substrate `GateCriteria` with a `code_assertions` slot
(code-graph predicates), implements the first `CodeAssertion`
(dispatch-reachability), wires it into `CERTIFY_GATE`, and gives
`build_certify_step` a production caller — killing the master:§Flaw 1
condition where the certify step had zero production callers (Contract #2).

## Artifacts produced

| Artifact | Path | Step |
| --- | --- | --- |
| Design doc | `phase-outputs/plans/r1-3-codeassertion-design.md` | 8.1 |
| Validation raw log | `phase-outputs/test-results/r1-3-validation.txt` | 8.4 |
| Validation summary | `phase-outputs/test-results/r1-3-validation-summary.md` | 8.4 |
| This aggregation | `phase-outputs/reports/r1-3-aggregation.md` | PG8.1 |

## Source changes

| File | Change | Lines |
| --- | --- | --- |
| `src/superclaude/cli/pipeline/models.py` | NEW `CodeAssertion` dataclass + `GateCriteria.code_assertions: list[CodeAssertion] \| None = None` slot | +37 |
| `src/superclaude/cli/pipeline/gates.py` | `gate_passed` gains keyword-only `envelope=None, repo_root=None` + code_assertions dispatch branch (after semantic_checks); envelope-None backward-compat shim | +36/-2 |
| `src/superclaude/cli/roadmap/gates.py` | `CERTIFY_GATE` gains `code_assertions=[CodeAssertion("step_reachable", assert_step_reachable, ...)]`; imports `CodeAssertion` + `assert_step_reachable` | +17 |
| `src/superclaude/cli/roadmap/executor.py` | NEW `_run_certify_after_remediate` helper (calls `build_certify_step` + runs certify via `roadmap_run_step`, guarded by remediate-PASS); wired into `execute_roadmap` post-pipeline | +82 |
| `src/superclaude/cli/roadmap/code_assertions.py` | NEW module: `assert_step_reachable`, `assert_envelope_artifacts_present`, `_extract_step_ids_from_build_steps`, `_build_certify_step_has_production_caller` (stdlib `ast` only) | NEW ~230 |
| `tests/roadmap/test_dispatch_reachability.py` | NEW: 8 tests (Contract #2 enforcement) | NEW ~190 |

## Acceptance-criteria mapping

| PG8.1 verdict criterion | Status | Evidence |
| --- | --- | --- |
| (a) `GateCriteria.code_assertions` defaults None → existing gates unchanged | ✅ | `models.py:90-105` default `None`; 184-test regression sweep PASS; smoke `GateCriteria(...).code_assertions is None` |
| (b) AST walker correctly identifies `_build_steps` Step IDs (test with synthetic deletion) | ✅ | `test_unwired_step_caught` (synthetic executor without certify → HIGH Finding); `_extract_step_ids_from_build_steps` verified extracting 12 ids incl `generate-` prefix. NOTE: `test_dispatch_reachability.py` contains **7** tests (not 8 — earlier drafts miscounted); all 7 PASS. |
| (c) `build_certify_step` actually wired (or consolidation rationale documented) | ✅ | `_run_certify_after_remediate` calls it; `execute_roadmap` invokes the helper; `assert_step_reachable` returns None (was CA-DISPATCH-002 before wiring) |
| (d) step count still ≤14 (Acceptance gate #6) | ✅ | `_build_steps`=13 constructions; `ALL_GATES`/`_get_all_step_ids`=14 incl certify; certify constructed dynamically, not added to `_build_steps` |
| (e) Contract #2 dispatch-reachability invariant CI-enforceable | ✅ | `test_dispatch_reachability.py` (7 tests) — `test_certify_step_reachable` + `test_unwired_step_caught` |
| (f) `commands.py` / `structural_checkers.py` / `convergence.py` unchanged | ✅ | None of the 3 PRESERVE files appear in `git diff --stat`; only models/gates(pipeline)/gates(roadmap)/executor touched + 2 new files |
| (g) zero new `return True` stubs | ✅ | New code returns `Finding \| None` / `tuple[bool, str]` / `bool` from genuine AST predicates — no fail-open `return True` stubs introduced |

## Step-count budget detail (Acceptance gate #6)

`_build_steps` continues to return 13 Step constructions (extract, generate-A,
generate-B, diff, debate, score, merge, anti-instinct, test-strategy,
spec-fidelity, wiring-verification, deviation-analysis, remediate). `ALL_GATES`
and `_get_all_step_ids` enumerate 14 (the above 13 + certify). certify is built
+ executed dynamically by `_run_certify_after_remediate` after remediate PASSES.
Live executed step count = 14 ≤ 14. No consolidation needed at R1.3; the
R1.5 verify-implementation addition is the budget-pressure point (consolidated
at R1.6).

## Design deviation surfaced for review

The Step 8.1 design doc §6.2 scoped `assert_step_reachable` to `_build_steps`
only, while §7.3 chose option (a) wiring (certify via `_run_certify_after_remediate`,
OUTSIDE `_build_steps`). These were internally inconsistent. Resolution: the
assertion now PASSES if EITHER (1) `certify` is a `_build_steps` literal OR (2)
`build_certify_step` has any production caller in `executor.py`. This matches
Contract #2's "reachable from a production entry point" language and the
master:§Flaw 1 definition ("zero production callers; only a test invokes it" —
the check parses only `executor.py`, so the tests/ caller never satisfies it).
Logged in Phase 8 Findings + design-doc §8 anticipated this extensibility.

## Verification snapshot

- Targeted suite (`test_dispatch_reachability + test_executor + test_certify_gates
  + test_certify_prompts + test_pipeline_integration`): **140 passed, 0 failed**.
- Broader R1.3 regression (Step 8.3): test_executor + test_certify_gates +
  test_certify_prompts + test_pipeline_integration + test_validate_cli +
  test_validate_resume_failure + test_spec_patch_cycle + test_pipeline_envelope =
  **184 passed, 0 failed**.
- `ruff check` (5 files) clean; `ruff format --check` (5 files) clean.
- Broad sweep `tests/roadmap/ tests/cli/` = 3337 passed, 19 failed (16 skipped);
  the 19 are ALL pre-existing failures, confirmed by stash-and-rerun on parent
  state 90a8fa67. CORRECTED ATTRIBUTION (PG8.1 rf-qa): the 19 split as **16 in
  `tests/cli/`** (`test_install_hooks.py` + `tests/cli/eval/`) and **3 in
  `tests/roadmap/`** (`test_cli_contract.py::test_default_agents_when_not_provided`,
  `test_models.py::test_default_agents`, `test_validate_unit.py::test_default_agents_two`).
  The 3 roadmap failures are a default-agent-model drift (test expects `haiku`,
  config default is `sonnet`) that is INDEPENDENT of R1.3 — they fail identically
  on the stashed parent state and none import an R1.3-modified module. The
  earlier "19 are entirely in tests/cli/" statement was inaccurate; corrected here.

## Known interpretation (for PG8.1 awareness)

- `test_all_strict_gates_have_assertions` scopes the "no empty gate" invariant to
  STRICT-tier gates (Step 8.4 parenthetical: "empty gates are silent PASS"
  applies at STRICT). `diff`/`score` are STANDARD with neither check type — they
  gate on frontmatter + min_lines, not a silent pass. The test also guards that
  they remain non-STRICT.
- Source line numbers cited in the design doc §2 are PRE-EDIT
  HEAD-daa10416 numbers (`build_certify_step` L2060, `GateCriteria` L90,
  `CERTIFY_GATE` L1430, `ALL_GATES` L1532). The task-file preamble's
  BareReview-era L1899/L1977/L91 numbers are stale; PG8.1 should validate
  against design-doc §2. POST-EDIT CORRECTION (PG8.1 rf-qa): after Step 8.2
  inserted the `CodeAssertion` dataclass into `models.py`, `GateCriteria`
  shifted from L90 → **L121**; after Step 8.3 inserted helpers into
  `executor.py`, `_build_steps` shifted from L2108 → **L2182**.
  `build_certify_step` remains L2060, `CERTIFY_GATE` is L1431, `ALL_GATES`
  is L1547, `("certify", CERTIFY_GATE)` is L1561. These are post-edit
  positions and supersede the design-doc §2 pre-edit citations.
