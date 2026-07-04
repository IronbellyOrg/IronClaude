# FX3/FX5 Completeness Verification Report

**Lens:** completeness (adversarial stance — assumed ≥3 missing elements)
**Mode:** REPORT ONLY (fix_authorization: false — no files edited)
**Date:** 2026-07-03
**Worktree:** `/config/workspace/IronClaude/.dev/worktrees/pr209-harden`

## Verdict: **PASS**

Every required FX3 and FX5 element is present with a file:line citation. All 37
tests across the three artifacts execute green (`uv run pytest` — see §Execution).
The adversarial hypothesis ("≥3 elements missing") is **not sustained**: no
required element from the checklist is absent. Two candidate "gaps" were probed
and both resolve to authorized-scoping decisions, documented in §Adversarial
Probes — neither is a checklist miss.

## Execution evidence

`uv run pytest tests/pr_submit/test_setup_questions_resolution.py test_gate_helper_differentials.py test_gate_helper_coverage.py -q`
→ **37 passed in 0.10s** (FX3 = 4; FX5 differentials = 22 = 11 helpers × 2 kinds;
FX5 coverage = 11 parametrized). Confirms "all reachable/green" structurally AND
by execution.

---

## FX3 checklist — `tests/pr_submit/test_setup_questions_resolution.py`

| # | Required element | Status | file:line |
|---|------------------|--------|-----------|
| 1 | Assertion 1: every `_answer_default(<lit>)` literal ⊆ SetupAnswers fields | PRESENT | test_setup_questions_resolution.py:112-132 (subset check `assert name in valid` L128) |
| 2 | Assertion 2 (**the F3 trap**): every `_evidence_attr` `answer_key` (= `answer_attr or attr`) ⊆ SetupAnswers fields | PRESENT | test_setup_questions_resolution.py:135-167 (`answer_key` derivation L154-161; subset check `assert answer_key in valid` L162) |
| 3 | Assertion 3: every `_evidence_attr` positional `attr` (evidence side) ⊆ EvidenceBundle attrs | PRESENT | test_setup_questions_resolution.py:170-190 (`assert attr in valid` L186) |
| 4 | Assertion 4: every deriver factory arg node is an `ast.Constant` str (Constant-arg guard) | PRESENT | test_setup_questions_resolution.py:193-218 (positional `assert _const_str(arg) is not None` L208; `answer_attr` kw guard L213-218) |
| 5 | Subset **direction** (`referenced ⊆ valid`, not `valid ⊆ referenced`) | PRESENT | All three membership checks use `... in valid` (L128, L162, L186); rationale for `augment_app_slug` non-false-positive documented in module docstring L18-21 |
| 6 | Valid field sets built **dynamically** from `dataclasses.fields`, never hardcoded | PRESENT | `_setup_answers_fields` uses `dataclasses.fields(...SetupAnswers)` L38-40; `_evidence_bundle_fields` uses `dataclasses.fields(...EvidenceBundle)` L43-45 |

Supporting mechanics (not separately mandated but verified present):
- Deriver-call collection scans `ast.Call` whose func is a bare `Name` in
  `{_answer_default, _evidence_attr}` — L54-62; factory set L35.
- Parses the **concrete module source** (not the lazy facade) via
  `questions_mod.__file__` — L48-51 (satisfies research/01 §5 item 6).
- Empty-collection guards fail loudly so a broken AST scan cannot become a
  silent no-op — L117-120, L144-147, L177-179, L201-203.

**FX3: 4/4 assertions + subset direction + dynamic dataclass-derived sets — ALL PRESENT.**

---

## FX5 checklist — `tests/pr_submit/conftest.py` + `test_gate_helper_differentials.py` + `test_gate_helper_coverage.py`

| # | Required element | Status | file:line |
|---|------------------|--------|-----------|
| 1 | `GATE_LOAD_BEARING_HELPERS == HELPER_TEST_MAP.keys()` (registry ≡ authored-pair set) | PRESENT | conftest.py:200-204 (`assert set(GATE_LOAD_BEARING_HELPERS) == set(helper_map)`) |
| 2 | Every registered helper carries a **negative + differential** pair | PRESENT | conftest.py:215-223 (loop over `("negative","differential")`, entry+`hasattr` checks); map with both kinds ×11 at test_gate_helper_differentials.py:48-94 |
| 3 | **NO exemption hatch** (no per-helper carve-out) | PRESENT | conftest.py:100-102 ("There is NO per-helper exemption"); drift-alarm msg "never a per-helper carve-out" L231-233; no exemption code path exists |
| 4 | **NO count target** (no `≥21` / `len==N` mandate) | PRESENT (correctly absent) | No count assertion in any of the 3 files; research/02 §6's literal "≥21" is intentionally superseded by the §4.3 scope-boundary treatment (enforced-set == authored-pair-set) — see conftest.py:95-114 |
| 5 | Enforced set covers full **F4 module-level def family** PLUS the two hand-registered §5 differentials | PRESENT | conftest.py:117-131 — 9 module-level (L119-127) + `candidate.CandidateContract.required_unobserved` L129 (§5.3) + `validation._negative_control_checks` L130 (§5.5) |
| 6 | **Existence check** — each registered dotted name resolves on the live module | PRESENT | conftest.py:206-213 (`_resolve_dotted`; `KeyError/AttributeError` → `AssertionError` "silent rename orphaned its FX5 tests") |
| 7 | Per-helper negative+differential coverage, **all reachable/green** | PRESENT + GREEN | Coverage test test_gate_helper_coverage.py:18-26; parametrized one-id-per-helper `pytest_generate_tests` conftest.py:237-248; 11 map entries each resolving to real test fns (verified pairs, see below); executed 37 passed |
| 8 | **Drift alarm** whose matched set is a **subset** of the registry | PRESENT | conftest.py:225-234 (`assert found in registry` per matched def — matched ⊆ registry); pattern conftest.py:148-151; matched set = the 9 module-level defs (⊂ 11) — independently re-verified below |
| 9 | Residual-risk **AUTO-ENUMERATION** non-goals (`ValidationReport.passed` + residual `_*_checks` family) documented | PRESENT | conftest.py:104-111 (names `validation.ValidationReport.passed`, `candidate.CandidateContract.required_unobserved`, `validation._*_checks` builder family); registry doc §5a fx5-gate-helper-registry.md:115-122 |
| 10 | **Scope-boundary** non-goal (`classify`, `from_yaml`, `load_evidence`) explicitly documented | PRESENT | conftest.py:112-114; registry doc §5b fx5-gate-helper-registry.md:124-126 |

### HELPER_TEST_MAP pair verification (11/11 — every named test fn exists)

| Registered helper | negative fn | differential fn |
|---|---|---|
| candidate._path_resolves | :236 | :244 |
| candidate._findings_locus | :265 | :272 |
| candidate._review_completeness_signal | :287 | :294 |
| candidate._selected_identity | :313 | :320 |
| candidate._selected_app_slug | :335 | :342 |
| lockgate._paths_resolve | :360 | :367 |
| lockgate._emission_shape_observed | :385 | :391 |
| diagnosis._resolve_optional_path | :407 | :415 |
| candidate.CandidateContract.required_unobserved | :432 | :439 |
| diagnosis._stale_blockers | :516 | :525 |
| validation._negative_control_checks | :541 | :558 |

(line numbers in `test_gate_helper_differentials.py`; each differential installs a
named naive mutant via `monkeypatch` and asserts the buggy value reappears —
mutation-detected, not merely "negative test exists".)

### Independent drift-pattern re-verification (I re-derived the matched set, did not trust the doc)

Pattern conftest.py:148-151 = `_(path|paths)_resolv | _resolve_ | _findings_ |
_selected_ | _stale_ | _emission_shape_observed | _review_completeness`.
Walked module-level `def`s (research/02 §1.1-1.4 inventory) against it:

- **candidate (5):** `_path_resolves`✓ `_findings_locus`✓ `_review_completeness_signal`✓ `_selected_identity`✓ `_selected_app_slug`✓. NON-matches confirmed: `_observed_logins/_observed_app_slugs/_observed_associations/_observed_severity_path` (bare `_observed_` token dropped), `_emission_shape`/`_shape_observed` (require full `_emission_shape_observed`), `_evidence_path` (`_path` ≠ `_path_resolv`).
- **lockgate (2):** `_paths_resolve`✓ `_emission_shape_observed`✓. `_identity_observed`/`_negative_controls_pass` correctly NOT matched.
- **diagnosis (2):** `_resolve_optional_path`✓ `_stale_blockers`✓. `_override_path_for` (`_path_for` ≠ `_path_resolv`) correctly NOT matched.
- **validation (0):** none matched (correct — the `_*_checks` family carries no gate-shaped token).

**Matched = 9 = §1a module-level set; strict subset of the 11-helper registry.**
Confirms element #8 (matched ⊆ registry) is real, not asserted-on-faith.

**FX5: 10/10 required elements — ALL PRESENT.**

---

## Adversarial Probes (the "≥3 missing" hypothesis — both candidates resolve to authorized scoping, NOT misses)

1. **`candidate._emission_shape` (candidate.py:223) is load-bearing but unregistered.**
   Research/02 §2.3 lists `_emission_shape.observed → lockgate._emission_shape_observed
   (gate #5)`, and research/02 §4.1's *recommended* registry included
   `candidate._emission_shape`. The final enforced registry does NOT include it.
   **Resolution:** The gate is covered at its lockgate **sink**
   (`lockgate._emission_shape_observed`, registered #7 with a pair). The task's
   §4.3 scope-boundary authorization explicitly scopes the enforced registry to
   the cleanly-enumerable pattern-matched module-level set; `_emission_shape`
   carries no gate-shaped token and is not an F4-family member (F4 = the
   findings_locus / paths_resolve chain). Within authorized scoping — **not a
   checklist miss.** (Observation only.)

2. **`candidate._observed_severity_path` (candidate.py:279) dropped from the pattern.**
   Research/02 §4.1 recommended registry listed it; the reconciled pattern drops
   the bare `_observed_` token so it no longer matches.
   **Resolution:** Research/02 §1.2 + §2.3 classify it "severity is nullable, NOT
   gated"; discovery doc §3 documents the deliberate `_observed_` drop with
   rationale (fx5-gate-helper-registry.md:60-79). Authorized demotion — **not a
   miss.**

3. **`ValidationReport.passed` / `_*_checks` family not enforced.** These are the
   AUTO-ENUMERATION residual-risk non-goals the checklist element #9 *requires be
   documented as non-goals* — and they are (conftest.py:104-111). Their absence
   from the enforced set is the specified behavior, not a gap.

No fourth candidate surfaced. The three probes above are the strongest
completeness challenges available against these artifacts, and all three are
answered by explicit, cited scope decisions.

---

## Caveats (honesty on limits of this pass)

- "All reachable/green" is verified both structurally (every map entry resolves
  to a defined test fn) AND by execution (37 passed). I did **not** re-derive
  each differential's mutation-detection logic against the live source of
  `validation.py` / `candidate.py` bodies line-by-line; I relied on green
  execution + the research inventory for those internals.
- This pass covers the FX3/FX5 element checklist only. It does not assess the
  broader task's other fix families (F1/F2/etc.) or non-FX3/FX5 artifacts.

---

## Final tally

- FX3 required elements: **6/6 PRESENT** (4 assertions + subset direction + dynamic dataclass sets).
- FX5 required elements: **10/10 PRESENT**.
- Adversarial "≥3 missing" hypothesis: **NOT sustained** (0 checklist misses; 3 probes all resolve to cited authorized-scoping decisions).
- Test execution: **37 passed**.
- **VERDICT: PASS.**
