# Research Notes: Apply Spec-Fidelity Convergence Fix (Canonicalizer + Tests)

**Date:** 2026-05-27
**Scenario:** A (highly explicit — BUILD_REQUEST is fully specified)
**Depth Tier:** Standard
**Track Count:** 1

**NOTE: Research phase was conducted UPSTREAM by the sc:troubleshoot --depth deep --fix pipeline at `/config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-20260527045400/`. The 8 research files in `research/` of this task are byte-for-byte copies of those upstream artifacts. Each has already passed the equivalent of rf-analyst completeness + rf-qa research-gate verification (via the troubleshoot pipeline's Wave 1.7 confidence-calibrator + Wave 4 self-review + Wave 5 evidence-validator passes; 18/18 file:line citations re-Read and verified). The task-builder skipping its own A.7 (researcher spawn) and A.8 (quality gate) is appropriate ONLY because the upstream pipeline performed equivalent work.**

---

## EXISTING_FILES

Primary production target:
- `src/superclaude/cli/roadmap/structural_checkers.py` (~700 LOC; helper at ~L260; phantom_id block at L372-391; SEVERITY_RULES at L42-67; FIX_GUIDANCE_TEMPLATES at L155-176)

Test targets (REPO CONVENTION: `tests/roadmap/` NOT `tests/cli/roadmap/` — verified via `ls tests/roadmap/`):
- `tests/roadmap/test_structural_checkers.py` (modify — add 5 golden-fixture tests)
- NEW `tests/roadmap/test_structural_checkers_properties.py` (create — property-based test gated by `pytest.importorskip("hypothesis")`)
- `tests/roadmap/test_convergence.py` (modify — add flatline-halt regression test sibling to `test_convergence_loop_three_runs` at L911)
- `tests/roadmap/test_remediate_executor.py` (modify — add cross-cutting "all-fixes-unfixable" integration test sibling to `test_large_change_rejected` at L708)

Precedent files (read-only references):
- `src/superclaude/cli/roadmap/integration_contracts.py:445` (`_canonicalize_identifiers` — the canonicalization pattern this fix mirrors)
- `src/superclaude/cli/roadmap/structural_checkers.py:309-327` (`_classify_nfr_severity` — the in-module severity-demotion precedent from S5)
- `tests/sprint/test_property_based.py` (the `importorskip("hypothesis")` precedent)

Failing artifact (smoke-test target):
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/.roadmap-state.json` (read-only; the test re-run target)

## PATTERNS_AND_CONVENTIONS

From `research/05-restrictions-doc-context.md` (7 binding restrictions):
1. Module ownership: `structural_checkers.py` owns FR-1/FR-3 (checkers + severity tables). No edits to `spec_parser.py` or `convergence.py`.
2. Pure-function contract (NFR-4): helpers are pure `(str, str) -> str` with no shared state, no I/O.
3. 30% per-patch diff guard: production change must fit. Our scope (~25 LOC in 700-LOC file) is ~4%.
4. Binary pass predicate `active_highs == 0` at `convergence.py:539` must NOT be modified. MEDIUM tier naturally bypasses (per `convergence.py:242` HIGH-only filter).
5. Spec is an input the agent cannot modify. No spec edits.
6. `max_runs=3` at `convergence.py:440` must NOT be modified.
7. Leverage `integration_contracts.py:445` precedent — same pattern, sibling-module placement.

Coding patterns (from existing source):
- Helper functions use `(family, raw) -> str` shape (per fix-3 framing in adversarial debate; preserves option for future upstream relocation).
- `_make_finding` factory at `structural_checkers.py:269-286` produces every Finding.
- `SEVERITY_RULES` dict (line 42-67) keys are `(dimension, mismatch_type)` tuples.
- `FIX_GUIDANCE_TEMPLATES` dict (line 155-176) keys are `rule_id`; templates use `{spec_quote}` and `{roadmap_quote}` placeholders.
- Test file naming: `test_<module>.py` matching the source `<module>.py`.

## GAPS_AND_QUESTIONS

NONE for execution. All 18 file:line citations in `research/01-troubleshoot-report.md` re-verified by `research/08-evidence-validation.md`. Test path convention resolved (`tests/roadmap/`). Self-review (`research/04-self-review-no-blockers.md`) returned APPROVED with no blockers.

## RECOMMENDED_OUTPUTS

4 Changes (verbatim from `research/03-refactor-plan-concrete-changes.md`):

1. **Change 1** — Add `_canonicalize_requirement_id(family, raw) -> str` helper near `_make_finding` at `structural_checkers.py:~260`. ~15 LOC. Docstring per the merged-output.md specification.
2. **Change 2** — Modify phantom_id block at `structural_checkers.py:372-391` + add `("signatures", "id_schema_drift"): "MEDIUM"` to SEVERITY_RULES + add `id_schema_drift` template to FIX_GUIDANCE_TEMPLATES. ~20 LOC.
3. **Change 3** — Add 5 golden-fixture asymmetric-ID tests to `tests/roadmap/test_structural_checkers.py`. ~50 LOC.
4. **Change 4** — Add property-based test (NEW file) + flatline-halt regression test + cross-cutting integration test across 3 test files. ~95 LOC.

## SUGGESTED_PHASES

Per Template 02 (Complex Task), sequence with dependencies:

1. **Phase 1: Preparation** — read research files; verify file:line citations against current HEAD; confirm test path convention.
2. **Phase 2: Implementation — Production Code** — Change 1 (helper) → Change 2 (phantom_id block + SEVERITY_RULES + FIX_GUIDANCE_TEMPLATES). Helper MUST land before the block that uses it.
3. **Phase 3: Implementation — Tests** — Change 3 (5 golden-fixture tests) → Change 4 (property-based + flatline-halt + cross-cutting). Golden-fixture before property-based (catches obvious bugs first; property-based finds edge cases).
4. **Phase 4: Validation** — run `uv run pytest tests/roadmap/ -v`; verify all new tests pass; verify all existing tests still pass; run `make lint` and `make format`.
5. **Phase 5: Smoke Test** — re-run `superclaude roadmap run /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md --resume` and confirm `spec-fidelity` step now passes (Run 1: 0 active HIGHs, 54 MEDIUM `id_schema_drift`).
6. **Phase 6: Restrictions Audit** — verify all 7 restrictions still hold (grep for prohibited edits in `spec_parser.py`, `convergence.py`, `max_runs`, spec file, etc.).
7. **Phase 7: Completion** — update task status to Done.

## TEMPLATE_NOTES

Template 02 (Complex Task) because: 4 logical changes across 4 files, careful sequencing required (helper before consumer; code before tests; golden fixtures before property-based), explicit verification phase, runtime smoke-test phase. Template 01 would not capture the dependencies.

QA_GATE_REQUIREMENTS: FINAL_ONLY — Phase 6 (Restrictions Audit) is the final QA gate verifying the 7 restrictions are honored. Per-phase QA is overkill for a 4-change fix.

VALIDATION_REQUIREMENTS: "make lint, make format, uv run pytest tests/roadmap/ -v all pass; verify all 7 restrictions in research/05-restrictions-doc-context.md hold."

TESTING_REQUIREMENTS: UNIT + INTEGRATION — Change 3 adds unit tests (golden fixtures); Change 4 adds property-based unit test + flatline-halt INTEGRATION test + cross-cutting INTEGRATION test on the convergence loop.

## AMBIGUITIES_FOR_USER

None — intent is clear from the BUILD_REQUEST and richly-grounded research. The 6 known follow-ups (INV-002 collision warning, INV-001 new-family test guard, A-001 spec-side normalization, deferred fixability scaffolding, deferred ADVISORY tier, LLM attention drift) are explicitly out-of-scope for this task and will be surfaced as separate work after this lands.
