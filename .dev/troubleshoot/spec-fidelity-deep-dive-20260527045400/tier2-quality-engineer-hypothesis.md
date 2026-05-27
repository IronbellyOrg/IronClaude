# Hypothesis: The phantom_id checker, the convergence pass predicate, and the 30% diff guard all ship with example-based tests that exercise only ONE shape per behaviour — so an ID-form-drift "flatline at N>0" failure mode is structurally invisible to the test suite and recurs every release

**Agent**: quality-engineer
**Tier**: 2
**Timestamp**: 2026-05-27T05:40:00Z
**Cause class**: Coverage gap — example-based tests for invariants that are universally-quantified over input *form* (test asserts "phantom IDs are detected" for one fixture but never "IDs that differ only in surface form are NOT phantoms"); compounded by missing "flatline halt" + "all-findings-structurally-unfixable" scenarios.
**Consistency with docs**: aligned

## Claim

The structural recurrence vector documented across releases (v3.0 → v3.05 → mid-May `roadmap-spec-fidelity-fix` → TUIBBS) is not just a code defect; it is a **test-design defect that allows the code defect to ship undetected each time the surrounding machinery is hardened**. Three concrete coverage gaps make the present TUIBBS failure shape (54 ACTIVE `phantom_id` HIGHs, flatline 58→54→54, halt message blames "TurnLedger" not comparator) unobservable in CI: (1) `test_structural_checkers.py` exercises `phantom_id` with one phantom (`FR-99`) and never with an asymmetric ID-form pair (`D1` in spec vs `D01` in roadmap); (2) `test_convergence.py::decreasing_checkers` (line 930) covers monotone descent and budget exhaustion but **has no test for the FLATLINE shape** (N → N-k → N-k → N-k where N-k > 0) that the present failure exhibits; (3) `test_remediate_executor.py::test_large_change_rejected` (line 708) covers per-patch rejection but **has no integration test that asserts "when EVERY remediation path requires >30% diff, the convergence loop emits a structurally-unfixable verdict rather than a budget verdict"**. The minimum fix is a checker-side canonicalization patch (per Tier 1 hypothesis) **plus** a focused test-suite expansion that closes all three gaps, including one property-based test that would have caught the comparator asymmetry 18 months ago at construction.

## Evidence

- `tests/roadmap/test_structural_checkers.py:152` — fixture text contains `"References FR-99 which is a phantom ID."` and `test_detects_phantom_id` (line 258) asserts only that `"FR-99" in f.description` for at least one finding. **No fixture in this 925-line file feeds the checker an asymmetric ID-form pair** (e.g. spec mentions `D1, D3, D5`; roadmap mentions `D01, D03, D05`). The canonical-form asymmetry that drives the TUIBBS failure is therefore structurally absent from the checker's test surface.
- `tests/roadmap/test_spec_parser.py:191-192` — `TestExtractRequirementIds.test_all_families` covers `D0042` only as a single string, **never asserting** that `extract_requirement_ids` on `"D1"` and on `"D01"` produce the *same* canonical form (it doesn't — and the test doesn't ask). The lenient regex at `spec_parser.py:329` (`\bD-?\d+\b`) is tested for *matching* both forms but never for *equivalence* of both forms, so the asymmetry between extractor and downstream comparator is invisible.
- `tests/roadmap/test_convergence.py:930-950` — `decreasing_checkers` walks the registry through `n=1 → 2 findings`, `n=2 → 1 finding`, `n=3 → 0 findings`, then asserts `result.passed` and `result.final_high_count == 0`. The complementary **flatline-but-non-zero** scenario — `n=1 → 58`, `n=2 → 54`, `n=3 → 54`, assert NOT passed AND assert halt message identifies structurally-unfixable findings rather than just "convergence not reached after 3 runs" — does not exist anywhere in the 1509-line file. The closest neighbour, `test_convergence_loop_budget_exhaustion` (line 952), engineers budget starvation, not finding-count flatline.
- `tests/roadmap/test_remediate_executor.py:686-749` — `test_threshold_is_30_percent`, `test_small_change_passes`, `test_large_change_rejected`, `test_large_change_allowed_with_flag`, `test_empty_original_passes`. **All five tests are per-patch unit tests**. There is no integration-level test that constructs a registry where the only roadmap-side fix for every active finding requires a >30% diff and asserts "the loop's halt verdict tells the operator this is a structurally-unfixable schema problem, not a budget problem." Without that test, the present TUIBBS halt message ("Convergence not reached after 3 runs. TurnLedger: available=31, consumed=46") is the **expected behaviour** the code was tested to produce — it just isn't the behaviour the operator needs.
- `tests/conftest.py` (matched line: `"sprint/test_property_based.py",  # requires 'hypothesis' (not a declared dependency)`) + `pyproject.toml` (line registering the `property_based` marker) + `tests/sprint/test_property_based.py` (lone consumer, `from hypothesis import assume, given, settings`). The `hypothesis` library is **named in pyproject.toml as a marker but explicitly excluded from declared dependencies** and used in exactly ONE test file. The deterministic checker surface in `structural_checkers.py` — five pure functions over `SpecData`/`RoadmapData` (NFR-4) — is exactly the surface property-based testing was designed for, but the practice has been quarantined to one sprint module. Generators like `id_form_pairs()` yielding `(spec_id="D1", roadmap_id="D01")` / `("FR-7", "FR-07")` / `("NFR-3.1", "NFR-3-1")` would have caught the comparator asymmetry on first run, 18+ months before TUIBBS surfaced it.
- `src/superclaude/cli/roadmap/structural_checkers.py:380-391` (Wave 1 ground truth) — the comparator under test. Read in this turn; confirms `phantom_ids = roadmap_ids - spec_ids` is a raw set-difference over the *matched* strings, which is the behaviour the tests above neither prove nor disprove for asymmetric forms.

## Why it recurs (Phase 0 + quality lens)

`historical-context.md` Section 5 records that "every prior failure shape has been distinct" (Pattern 2) and that "no shipped remediation has touched the comparator itself" (Pattern 3). Both patterns are *predicted* by the coverage shape above: when a test suite only exercises example-shaped invariants and surrounds the untested core with monotonically-hardening orchestration (DeviationRegistry, TurnLedger, monotonic-progress invariant, regression detection, `_route_findings`, S5 NFR demotion), each new release ships a new shape because (a) the previous shape's regression test gets added, (b) the comparator itself remains untested for *universal* properties, and (c) the convergence loop's halt-message tests assert on the message *as it is currently emitted*, codifying the misdirection. The team is rationally fixing the shapes the tests CAN catch and missing the structural invariant the tests CAN'T. The right empirical validation for any proposed fix is therefore not just "does this make the TUIBBS halt pass" but "does this fix come paired with tests that would have caught the bug at construction time — golden-artifact fixtures of asymmetric ID pairs across all 5 families, plus a property-based generator, plus an integration test for the flatline halt verdict."

## Proposed Fix

**Two-layer fix: minimal checker-side canonicalization (mirrors Tier 1) PLUS a test-suite expansion that closes the three coverage gaps. The code change is small; the test change is the load-bearing part for preventing the next-shape recurrence.**

Layer A — code (minimal, mirrors Tier 1 hypothesis exactly): add `_canonicalize_requirement_id(pid: str) -> str` near `_make_finding` in `structural_checkers.py` (strips leading zeros within the numeric tail of the regex match, preserves prefix and sub-IDs), apply to both sides before the set difference at lines 380-391, and emit `mismatch_type="id_schema_drift"` with `severity="MEDIUM"` for canonical-match-but-form-differs cases. Under the per-patch 30% guard (single-helper addition + ~6-line edit in one function), zero `convergence.py` changes, zero `spec_parser.py` changes (preserves Restriction 1 module ownership), pure transformation (NFR-4 / Restriction 2).

Layer B — tests (this is the new contribution; without these, the next shape recurs):

1. **Golden-fixture asymmetric-ID tests** in `tests/roadmap/test_structural_checkers.py`:
   - `test_phantom_id_canonicalizes_zero_padded_d_ids` — spec has `D1, D3, D5`; roadmap has `D01, D03, D05`. Assert 0 HIGH `phantom_id` findings and 3 MEDIUM `id_schema_drift` findings.
   - `test_phantom_id_genuine_phantom_still_emits_high` — spec has `D1, D3`; roadmap has `D01, D99`. Assert exactly 1 HIGH (`D99`) and 1 MEDIUM (`D01` ↔ `D1` drift). Regression guard against over-canonicalization.
   - One fixture pair per family (FR/NFR/SC/G/D) covering both `D01↔D1` style and `FR-7.1↔FR-7-1` style. Five tests, ~50 lines.

2. **Property-based comparator test** in NEW `tests/roadmap/test_structural_checkers_properties.py` gated on `pytest.importorskip("hypothesis")` so the existing `# not a declared dependency` posture is respected (matches the `tests/sprint/test_property_based.py` precedent):
   - `@given(id_form_pairs())` strategy yielding `(canonical, surface_variants)` tuples; assert that for every `(c, v)` pair, `check_signatures` on a spec with `c` and a roadmap with `v` produces zero HIGH `phantom_id` findings. This is the test that should have existed since the checker was written and would have caught the bug at construction.

3. **Flatline-halt integration test** in `tests/roadmap/test_convergence.py` (as a sibling to `test_convergence_loop_three_runs` at line 911 and `test_convergence_loop_budget_exhaustion` at line 952):
   - `test_flatline_halt_emits_structural_verdict` — driver `flatline_checkers` returns 58 findings on n=1, 54 on n=2, 54 on n=3 (matching TUIBBS shape exactly). Assert `not result.passed` AND that the halt reason text contains a marker indicating structural-unfixability (e.g. `"id_schema_drift"` or `"no structural progress"`), NOT only `"Convergence not reached"`. Once Layer A demotes the drift findings, this same fixture should *pass* on Run 1 — keep the test as a permanent regression for "fixture shape that used to fail must now resolve."

4. **Cross-cutting "all-findings-unfixable" integration test** in `tests/roadmap/test_remediate_executor.py` (sibling to `test_large_change_rejected` at line 708):
   - `test_loop_reports_structural_when_all_remediations_exceed_diff_guard` — registry where every active finding's only candidate patch exceeds the 30% guard; assert the convergence loop's terminal verdict identifies the structural ceiling, not budget exhaustion. (This test is gentler — it can be satisfied by the existing halt-message even pre-Layer-A as long as the assertion is loose; its long-term value is locking the post-fix behaviour.)

Files that would change:
- `src/superclaude/cli/roadmap/structural_checkers.py` — add canonicalizer helper + modify lines 372-391 (same edit Tier 1 proposes).
- `tests/roadmap/test_structural_checkers.py` — add 5 example-based golden tests.
- `tests/roadmap/test_structural_checkers_properties.py` — NEW file, ~40 lines, `importorskip("hypothesis")` guarded.
- `tests/roadmap/test_convergence.py` — add flatline-halt test, ~30 lines.
- `tests/roadmap/test_remediate_executor.py` — add structural-ceiling integration test, ~25 lines.

Empirical validation (the right kind, per the question in the prompt): golden artifacts pinned to the TUIBBS fixture pair (the existing `D1/D3/D5` vs `D01..D54` reproducer becomes a saved test fixture under `tests/roadmap/fixtures/` and is consumed by an integration test), property generators for the invariant "asymmetric-form IDs must not produce phantoms," and the flatline-shape regression test — together these answer "does this fix HOLD" rather than "does this fix PASS the new failure."

## Compliance with the 7 restrictions (doc-context.md §Restrictions)

1. **Module ownership** — Layer A canonicalization lives inside `structural_checkers.py`, the module that owns FR-1/FR-3 per `architecture-design.md:27-33`. Layer B tests add to `tests/roadmap/` mirroring the source module. No changes to `spec_parser.py` or `convergence.py` source. ✅
2. **Pure-function contract (NFR-4)** — `_canonicalize_requirement_id` is a pure string-in/string-out function; the modified comparator computes two canonical sets and a difference, with no shared mutable state. Property-based tests are themselves pure. ✅
3. **30% per-patch diff guard** — Layer A is ~6 modified lines + 1 ~10-line helper inside one ~400-line file — well under 30%. Layer B test additions touch test files only, exempt from the production-patch guard. ✅
4. **Binary pass predicate `active_highs == 0`** — Layer A demotes drift findings to MEDIUM, which makes `active_highs == 0` naturally true for the TUIBBS fixture without modifying `convergence.py:539`. S6 stays deferred. ✅
5. **Spec is an input the agent cannot modify** — No proposed change touches the spec or the contract that the agent treats spec as read-only. Test fixtures are independent of any project's real spec. ✅
6. **`max_runs=3` hard default** — Untouched in both layers. Flatline-halt test exercises the 3-run loop as-is. ✅
7. **Canonicalization precedent at `integration_contracts.py:445`** — Layer A is structurally identical to that already-merged precedent (per KNOWLEDGE.md 2026-05-25 "Fix B Merged"), strengthening the project pattern rather than introducing a new one. ✅

## Confidence

Self-reported confidence: 0.85

Per-dimension self-assessment:
- Evidence grounding: 1.0 — every cited file:line was Read or `grep`-verified in this turn; quoted snippets match.
- Symptom coverage: 1.0 — explains the deterministic comparator bug, the flatline shape, the misleading halt message, AND the cross-release recurrence pattern. Adds the quality-engineering "why CI never caught it" layer that pure RCA cannot.
- Reproducibility fit: 1.0 — the proposed `flatline_checkers` test driver is a one-paragraph synthesis of the TUIBBS observed shape (58/54/54) and runs deterministically.
- Fix directness: 0.5 — the *code* change is direct (mirrors Tier 1); the *test* expansion is the larger surface and requires consensus on adopting `hypothesis` as an opt-in dev-dep pattern (precedent exists at `tests/sprint/test_property_based.py` but the broader policy is "not a declared dependency"). A purist might say the test-suite expansion is out-of-scope for a fix card. I argue (Domain coherence section below) it is the load-bearing half.
- Domain coherence: 1.0 — directly aligned with the project's stated quality posture in `KNOWLEDGE.md` ("evidence-based development", "never guess") and with the historical-context.md Pattern 2 observation ("every prior failure shape has been distinct"); the test gap *is* why the shapes keep being distinct.

## Risks

- **`hypothesis` dependency posture**: adding `tests/roadmap/test_structural_checkers_properties.py` requires either declaring `hypothesis` as a dev-dep (small policy change) or matching the existing `pytest.importorskip` + `conftest.py` collect_ignore pattern. I propose the latter to avoid any policy decision; the test simply doesn't run in environments without hypothesis, same as `tests/sprint/test_property_based.py` today. Risk: skipped tests provide no protection until hypothesis is installed in CI.
- **Over-canonicalization**: same as Tier 1 — collapsing `D1` and `D01` may hide a legitimately-distinct ID in some future project's convention. The `test_phantom_id_genuine_phantom_still_emits_high` test in Layer B is the explicit guard against this regression.
- **Flatline test fragility**: the integration test in Layer B(3) asserts on the halt-message *shape*. If the halt formatter is later refactored to emit JSON or change wording, the test must be updated. Mitigation: assert on a stable structured field (e.g. `result.halt_reason` enum) rather than free-text substring once that field exists.
- **Five family-specific golden tests grow over time**: as new requirement families are introduced (per `_REQUIREMENT_PATTERNS`), each needs its own asymmetric-form test. Mitigation: the property-based test in Layer B(2) is family-agnostic and provides automatic coverage if its strategy is wired off `_REQUIREMENT_PATTERNS.keys()`.
- **Does NOT address LLM attention drift** (historical-context.md Section 5, Pattern 1). Structural recurrence is foreclosed; semantic-fluctuation failures (`fidelity-remediation-log.md` row "DISPUTED post-remediation") remain possible. A complementary 5-vote-consensus or DISPUTED reclassification automation is still warranted but is a separate hypothesis card.

## If I'm wrong, it's probably because...

The right structural escape is to re-promote backlog item S6 (MANUAL_TRIAGE halt) inside `convergence.py` rather than to demote drift findings in the checker — meaning my Layer A is correct as a comparator fix but my Layer B(3) test target is wrong (the test should assert on a new `MANUAL_TRIAGE` terminal state in `convergence.py`, not on a demoted severity in the checker), and the proper fix is a convergence-loop change that the Restriction 1 reading rules out only on a strict module-ownership interpretation.

## Alternatives considered

- **Tests-only fix (no code change)**: rejected — even comprehensive property-based tests over a known-buggy comparator only *document* the bug; they don't fix it. The TUIBBS halt would continue to fire until Layer A lands. Tests without code are diagnosis, not remediation.
- **Code-only fix (skip the test expansion)**: rejected — this is what every prior release has done (S1, S2, S5 all shipped with example-based tests of their narrow shape). Pattern 2 of historical-context.md is the receipt: shape-specific code patches without invariant-level tests produce the next-shape failure on the next release. The test layer is what breaks the cycle.
- **Move canonicalization into `spec_parser.py:329` and write tests there**: rejected — same reasoning as Tier 1 (Restriction 1 module ownership; breaks downstream consumers of raw-form IDs). The asymmetric-form tests would still need to live in `test_structural_checkers.py` because the comparator is the surface under test, not the extractor.

## Grounding gaps

- Did not run `uv run pytest tests/roadmap/test_structural_checkers.py -v` in this turn to confirm the currently-passing test count or to baseline runtimes — the coverage-gap claim is from reading the file's test inventory, not from a coverage report.
- Did not enumerate downstream consumers of `Finding.severity == "HIGH"` (beyond `convergence.py:539` cited in Tier 1) to confirm the MEDIUM-demotion has no second-order effects on release-readiness scoring or PR-review gates.
- Did not verify whether `tests/roadmap/test_spec_fidelity.py` or `test_convergence_e2e.py` contain end-to-end fixtures that exercise TUIBBS-like ID drift — only the four files I read in depth (`test_structural_checkers.py`, `test_convergence.py`, `test_spec_parser.py`, `test_remediate_executor.py`) were scanned. A wider sweep might reveal partial coverage that this card under-credits.
- Did not measure whether installing `hypothesis` as a declared dev-dep would break any existing CI configuration. The proposal uses `importorskip` to sidestep this, but the broader question is unanswered.
