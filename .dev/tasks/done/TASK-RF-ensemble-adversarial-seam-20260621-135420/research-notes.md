# Research Notes: FR-RH2 R6 — wire the adversarial seam into build_reflect_contract

**Date:** 2026-06-21
**Scenario:** A (explicit — clear goal, known files, known fix shape)
**Depth Tier:** Standard
**Track Count:** 1
**Spec:** `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` (FR-RH2 acceptance oracle)

---

## EXISTING_FILES

- `src/superclaude/cli/reflect/ensemble.py` (~509 LOC, FR-RH2 driver, introduced in commit 576aadff/4cb604fa)
  - `AdversarialScoreFn = Callable[[list[str], Path], float | None]` (line 72) — the SEAM TYPE. Currently returns only a float convergence score. **This is the type to widen** to return/parse a richer adversarial result object.
  - `run_tier2_ensemble(...)` (line ~120-241) — orchestrates dispatch → normalize → reduce → adversarial seam → `build_reflect_contract` → emit.
  - Seam invocation site: lines 221-239 (`adversarial_score_fn` or `run_adversarial_scorer`), result passed to `build_reflect_contract(..., adversarial_convergence_score=...)` at line 234.
  - `run_adversarial_scorer(final_paths, output_dir, *, config)` (line 244) — default seam impl; launches the Mode-A scorer and **parses only `convergence_score`**.
  - `_parse_convergence_score(contract)` (~line 340-357) — unwraps `return_contract.convergence_score`. Reference pattern for parsing the richer object.
  - `build_reflect_contract(workers, *, swarm_merged_path, adversarial_convergence_score, adversarial_unavailable)` (line 360-407) — **THE TARGET**. Hard-codes `status:"success"` (379), `deviation_count_by_class` all-zero (385-390), `regression_present:False` (401), `unauthorized_deviation_present:False` (402), `needs_human_decision:False` (403), `user_decision_required:False` (404). `report_path` via `_select_report_path` (375) = swarm merged.md only.
  - `_select_report_path(succeeded, swarm_merged_path)` (line ~490) — currently returns `swarm_merged_path` when present (the merged swarm report, NOT the adversarial child report).
  - `ADVERSARIAL_SUBRUN_DIR = "t2-adversarial"` (line 67) — where the adversarial child writes.
- `src/superclaude/cli/reflect/contract.py` — the CONSUMER (constraints, do NOT modify behavior per FR-RH2.7):
  - `_LOAD_BEARING_BOOL_FIELDS` (line 47-57): `{regression_present, unauthorized_deviation_present, needs_human_decision, user_decision_required, adversarial_unavailable, input_drift_detected, verification_ran}`.
  - `_extract_deviations(contract)` (line 90-101): reads `deviation_count_by_class` as 4-key int dict (authorized/necessary/drift/regression).
  - `derive_verdict(...)` (line 130): first-match-wins verdict. Blocks/halts on `regression_present is True` (315), `unauthorized_deviation_present is True` (317), `needs_human_decision is True` (319), and deviation counts (323-326).
  - `parse_contract` (65), `_make_result` (104).
  - **FR-RH2.7 invariant:** `derive_verdict` and the Verdict exit-code map (`pass→0, halted→10, degraded→11, blocked→2`) MUST stay unchanged. The fix is ensemble-side mapping ONLY — feed `derive_verdict` REAL values; do not edit derive_verdict.
- `src/superclaude/cli/reflect/models.py` — `ReflectConfig` (timeout_seconds line 74; relevant if seam needs config).
- `tests/cli/reflect/test_ensemble_stub_integration.py` — existing ensemble integration tests (I1-I6 witnesses per the FR-RH2 QA report); the new regression-asserting test belongs here or a sibling.
- The adversarial child: `/sc:adversarial` Mode-A scorer (invoked by `run_adversarial_scorer`). Its emitted contract/report under `output_dir/t2-adversarial/` is the SOURCE of the deviation/regression/human-decision signal the seam must parse. **What fields it emits is the key discovery item.**

## PATTERNS_AND_CONVENTIONS

- NFR-1 thinness: ensemble.py is ≤~400 LOC of mapping logic; no reflect-domain re-derivation. The fix must stay thin — map existing adversarial-child fields onto contract keys, do not author new deviation-classification logic.
- NFR-7 no-nesting guard: ensemble.py is covered by the no-nesting guard (`tests/cli/reflect/test_no_nesting_guard.py`); the seam must NOT introduce agent-spawn/slash-command tokens.
- OI-1 provenance discipline: the validated OI-1 mapping table classifies each contract field MAPPED/DERIVED/SYNTHESIZED. R6 promotes `deviation_count_by_class`, `regression_present`, `unauthorized_deviation_present`, `needs_human_decision` from SYNTHESIZED-inert-default to MAPPED-from-adversarial-child (the table's own "unless the adversarial/reflect domain supplies counts" clause).
- Test style: pytest, `uv run pytest`, fixtures + stub transports (`--transport stub`). Existing I1-I6 witnesses parse `config.contract_path` then call `derive_verdict`.

## GAPS_AND_QUESTIONS

1. **What does the `/sc:adversarial` Mode-A child actually emit?** The seam can only map fields the adversarial child produces. Researchers MUST find the adversarial child's output contract/report schema — does it expose deviation counts, a regression/blocking flag, a human-decision flag, and a report path? Or only a convergence score? This determines whether R6 is a pure mapping change or needs the child to emit more.
2. **Seam return type design:** widen `AdversarialScoreFn` to return a small result object/dataclass (e.g. `AdversarialResult{convergence_score, deviation_counts, regression_present, unauthorized_deviation_present, needs_human_decision, report_path}`) vs a dict. Must keep backward-compat for existing callers/tests that pass `adversarial_score_fn` returning a float, OR update those call sites/tests.
3. **`adversarial_unavailable` interaction:** when the seam can't run (M<2 / parse failure), the existing degrade path sets `adversarial_unavailable`. The new mapping must not break that path.
4. **report_path:** should map to the adversarial child report (per QA CRITICAL #2 fix) — confirm `_select_report_path` change keeps swarm merged.md as a subrun artifact only.

## RECOMMENDED_OUTPUTS

Research files in `research/`:
- `01-ensemble-seam-inventory.md` — ensemble.py seam, scorer, build_reflect_contract, _select_report_path (File Inventory)
- `02-adversarial-child-output-schema.md` — what the Mode-A adversarial child emits; the parseable signal source (Data Flow / Integration Points) — THE crux
- `03-contract-consumer-constraints.md` — derive_verdict, _extract_deviations, _LOAD_BEARING_BOOL_FIELDS, FR-RH2.7 invariant (mapping target)
- `04-test-patterns.md` — existing ensemble tests + regression-asserting test design (Test & Verification)
- `05-template-and-citations.md` — MDTM template 02 + spec FR-RH2 bullets + OI-1 table + QA CRITICAL #2 (Template & Examples + citation anchors)

## SUGGESTED_PHASES

- Researcher 1 (File Inventory): `src/superclaude/cli/reflect/ensemble.py` — seam type, scorer, build_reflect_contract, _select_report_path, call sites; exact line anchors + signatures. → `research/01-ensemble-seam-inventory.md`
- Researcher 2 (Data Flow / Integration): the `/sc:adversarial` Mode-A child — invocation in run_adversarial_scorer, output dir `t2-adversarial`, the emitted contract/report schema, which deviation/regression/human-decision fields exist. Trace what the seam CAN parse. → `research/02-adversarial-child-output-schema.md`. Other researchers cover ensemble inventory (R1) and contract consumer (R3) — focus on the adversarial child's emission.
- Researcher 3 (Integration Points): `src/superclaude/cli/reflect/contract.py` — derive_verdict, _extract_deviations, _LOAD_BEARING_BOOL_FIELDS, the FR-RH2.7 "derive_verdict unchanged" constraint; the exact contract keys + types the mapping must produce. → `research/03-contract-consumer-constraints.md`
- Researcher 4 (Test & Verification): `tests/cli/reflect/test_ensemble_stub_integration.py` + sibling reflect tests + no-nesting guard test; fixture/stub patterns; how to inject a seam that reports a regression and assert derive_verdict ≠ pass. → `research/04-test-patterns.md`
- Researcher 5 (Template & Examples): MDTM template 02 (`.claude/templates/workflow/02_mdtm_template_complex_task.md`) PART 1; the spec FR-RH2.* bullets at `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md`; the OI-1 table + QA CRITICAL #2 citation anchors (verbatim quotes for the task to cite). → `research/05-template-and-citations.md`

## TEMPLATE_NOTES

- Template **02** (complex): requires discovery (adversarial child schema) → build (widen seam + map fields) → test (regression-asserting) → verify (FR-RH2.7 unchanged, full reflect+swarm suites). Conditional flow on what the adversarial child emits.
- Tier **Standard**: single `reflect/` subsystem, ~5-15 files, moderate complexity, 0-1 web agents (none expected — internal codebase).
- QA_GATE_REQUIREMENTS: PER_PHASE (template 02). Final-document gate min 6 agents; this is a code task so the generated gates target the implementation + tests.
- TESTING_REQUIREMENTS: UNIT (the regression-assert test is the headline acceptance) + run existing reflect/swarm suites for regression.
- VALIDATION_REQUIREMENTS: `make lint`, `uv run ruff format --check src/ tests/`, FR-RH2.7 invariant (derive_verdict byte-unchanged), no-nesting guard passes.

## AMBIGUITIES_FOR_USER

None blocking — intent is explicit and the fix shape is known. The one genuine discovery dependency (does the `/sc:adversarial` Mode-A child already emit deviation/regression fields, or must it be extended?) is a codebase question for Researcher 2, not a user-intent question. If the child emits ONLY a convergence score, the task must include extending the child's emission OR deriving regression from the convergence score against a threshold — Researcher 2's finding decides which, and the builder will branch the task accordingly.
