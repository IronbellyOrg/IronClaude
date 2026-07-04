# QA Report — M4 Source-Document Fidelity Gate (fidelity-agent-1)

**Topic:** PR #209 QA/Reflect blindspot hardening — FX3 / FX5 / FX7 source-fidelity
**Date:** 2026-07-03
**Phase:** report-validation (source-document fidelity)
**Fix authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — assumed ≥3 of the five plan §2 fixes were only partially implemented; scoped to FX3/FX5/FX7.
**Change set root:** `/config/workspace/IronClaude/.dev/worktrees/pr209-harden`

---

## Overall Verdict: PASS

All three in-scope fixes (FX3, FX5, FX7) have implemented artifacts that faithfully address their intent under the DOCUMENTATION-STALENESS OVERRIDE. No phantom coverage. No partial coverage. The two deferred FX7 verdict-DEGRADE routings are HALTED as `needs_human_decision` PENDINGs (not applied), which is the FAITHFUL realization of the honest-accounting intent given the code conflict — not a coverage gap.

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 15 | Grep: 2 (via Bash) | Glob: 0 | Bash: 3

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FX3 artifact exists + AST introspection of derivers | PASS | `tests/pr_submit/test_setup_questions_resolution.py` parses `questions.py` via `ast`, walks `_answer_default`/`_evidence_attr` calls (`_deriver_calls` L54-62) |
| 2 | FX3 subset direction (referenced ⊆ valid) | PASS | Valid sets built dynamically from `dataclasses.fields(SetupAnswers/EvidenceBundle)` (L38-45); assertions use `name in valid` (L128, L162, L186); docstring L19-21 explicitly names SUBSET to avoid false-positive on real-but-unreferenced `augment_app_slug` |
| 3 | FX3 Constant-arg guard | PASS | `test_every_collected_deriver_arg_is_a_string_constant` (L193-219) FAILs loudly on any non-`ast.Constant`-str deriver arg or `answer_attr` kwarg, so dynamic args cannot silently bypass the resolution checks |
| 4 | FX5 enforced registry ≡ HELPER_TEST_MAP | PASS | `GATE_LOAD_BEARING_HELPERS` (conftest L117-131, 11 helpers); collector asserts `set(GATE_LOAD_BEARING_HELPERS) == set(helper_map)` (L200-204) |
| 5 | FX5 two hand-registered dataclass/checks helpers | PASS | `candidate.CandidateContract.required_unobserved` + `validation._negative_control_checks` registered (conftest L129-130) and paired in `HELPER_TEST_MAP` (differentials L81-93); documented as outside the module-level drift-alarm set by design (conftest L104-114) |
| 6 | FX5 differential-must-fail (mutation detected, not merely "negative test exists") | PASS | Each of 11 helpers has a differential that `monkeypatch`-installs a naive/pre-fix mutant and asserts the buggy value FLIPS back (e.g. L244-259 all-None list → `observed is True`; L367-379 presence-only mutant → gate wrongly passes; L558-571 constant-True control mutant). Anti-gaming §3.5 satisfied |
| 7 | FX7 `*_verified` fields on `ReflectResult` | PASS | `verification_verified` / `reviewers_verified` / `regression_verified` defaulted False on the dataclass (models.py L158-160) |
| 8 | FX7 `*_verified` populated in `_make_result` | PASS | contract.py L130-132 via `c.get(...,False)`; git diff vs base `46a787da` shows this is the ONLY contract.py change |
| 9 | FX7 `*_verified` emitted by the ensemble builder | PASS | ensemble.py L577-579 in `build_reflect_contract` return dict |
| 10 | FX7 `*_verified` surfaced append-only in runner | PASS | runner.py L120-122 (`_build_reflect_post_value`, end of dict) + L239-241 (sidecar, end of dict); both comment-tagged append-only |
| 11 | FX7 reviewer-shortfall VISIBLE token | PASS | ensemble.py L538-540 appends `"reviewer-shortfall"` to `degraded_components` iff `reviewers_requested is not None and reviewer_count < reviewers_requested`; `reviewers_verified` computed at L535-537 |
| 12 | FX7 shortfall token is BENIGN (does not flip verdict) | PASS | `reviewer-shortfall` ∉ `_DEGRADED_COMPONENTS_HALT_SET` (contract.py L31-33); `_degraded_reason` Trigger 1-5 only degrades on HALT_SET membership (L265) — CONFIRMS the override premise |
| 13 | FX7 clean-run `verification_skip_reason` UNCHANGED (R2-F2 preserved) | PASS | ensemble.py L571-572 still emits `verification_ran: False` + `verification_skip_reason: "tool-unavailable"`; `tool-unavailable` still ∈ `_VERIFICATION_SKIP_EXEMPTIONS` (contract.py L36-38) → exempt, no spurious degrade |
| 14 | FX7 both frozensets byte-unchanged | PASS | `git diff 46a787da -- contract.py` = single 6-line additive `_make_result` hunk; `_DEGRADED_COMPONENTS_HALT_SET` and `_VERIFICATION_SKIP_EXEMPTIONS` untouched |
| 15 | FX7 two aggressive degrade routings HALTED as PENDINGs | PASS | `fx7-degrade-on-unverified-DECISION.md` (Option B reverses R2-F2 / test_r2f2 / test_i1) + `fx7-degrade-on-reviewer-shortfall-DECISION.md` (Option B reverses FR-RH2.9 / test_i3); both state Option A shipped, Option B NOT applied, frozensets byte-unchanged |
| 16 | Deferral faithful to research override (not a coverage gap) | PASS | See "Faithfulness Analysis" below |

## Summary
- Checks passed: 16 / 16
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT ONLY — fix_authorization: false)

---

## Per-Fix Semantic Coverage + Detail Preservation

### FX3 — AST field-resolution backstop — COVERED, DETAIL PRESERVED
**Intent (plan §2/§5):** AST-introspect every `SETUP_QUESTIONS` deriver + `getattr`/`_evidence_attr` string literal; assert each resolves to a real, flow-through `SetupAnswers` field.
**Artifact:** `tests/pr_submit/test_setup_questions_resolution.py` (4 test functions).
- **Subset direction (required detail):** PRESERVED. The valid-name sets are built dynamically from the live dataclasses (`_setup_answers_fields`, `_evidence_bundle_fields`, L38-45), and every assertion tests `referenced ⊆ valid` (`name in valid`). The docstring (L19-21) explicitly justifies the SUBSET direction so a real-but-unreferenced field (`augment_app_slug`, set via the `detected_augment_identity` flow, referenced by no deriver) does not false-positive. This is the exact anti-false-positive nuance the intent requires.
- **Constant-arg guard (required detail):** PRESERVED. `test_every_collected_deriver_arg_is_a_string_constant` (L193-219) asserts every positional deriver arg AND every `answer_attr` kwarg is an `ast.Constant` str, failing loudly rather than silently skipping — closing the "computed arg bypasses the static scan" hole (plan §3 residual-risk #2).
- The direct F3 trap is the dedicated `test_every_evidence_attr_answer_key_resolves...` (L135-167), which reproduces the buggy `_evidence_attr("pr_number")` → `answer_key="pr_number"` (not a `SetupAnswers` field) FAIL.

### FX5 — negative + differential gate-helper mandate — COVERED, DETAIL PRESERVED
**Intent (plan §2/§5):** a collector enumerating lockability/resolution/provenance helpers; FAIL if any lacks a negative test AND a differential check (mutating the helper output must make a test fail).
**Artifacts:** `tests/pr_submit/conftest.py` (collector), `tests/pr_submit/test_gate_helper_differentials.py` (22 tests + `HELPER_TEST_MAP`), `tests/pr_submit/test_gate_helper_coverage.py` (parametrized reported face).
- **Registry (required detail):** PRESERVED. `GATE_LOAD_BEARING_HELPERS` is the enforced 11-helper registry (conftest L117-131), asserted identical to `HELPER_TEST_MAP` keys (L200-204) so registry and authored-pairs can never silently diverge. A drift alarm (L225-234) FAILs when a NEW gate-shaped module-level helper appears unregistered.
- **The two hand-registered dataclass/checks helpers (required detail):** PRESERVED. `candidate.CandidateContract.required_unobserved` (a dataclass method) and `validation._negative_control_checks` (a checks-builder) are explicitly hand-registered (conftest L129-130) because the module-level AST drift-alarm cannot auto-enumerate them; both carry full negative+differential pairs (differentials L81-93, tests L432-453 and L541-571).
- **Differential-must-fail (required detail / anti-gaming §3.5):** PRESERVED. Every differential `monkeypatch`-installs a naive/pre-fix mutant of the helper (or its dependency) and asserts a downstream observation FLIPS to the buggy value — proving the mutation is DETECTED, not merely that a passing negative test exists. Examples: `_naive_path_resolves` restores the all-None-list-truthy bug and `findings_locus.observed` flips True (L244-259); `_naive_paths_resolve_presence_only` drops the `.observed` check and the gate wrongly passes (L367-379); `_naive_negative_control_checks` returns constant-True and the mis-classification is masked (L558-571).

### FX7 — additive honest-accounting — COVERED, DETAIL PRESERVED, DEFERRAL FAITHFUL
**Intent (plan §2 row, reconciled by research override):** add `*_verified` visibility flags; make misses VISIBLE without repurposing existing routing (driving-plan §3.4).
**Artifacts:** `models.py` (+3 fields), `contract.py` (`_make_result` populate), `ensemble.py` (emit + shortfall token + `reviewers_requested` kwarg), `runner.py` (append-only surfacing).
- **Additive `*_verified` fields (required detail):** PRESERVED end-to-end. Declared on `ReflectResult` (models.py L158-160, defaulted False / fail-closed), populated defensively via `c.get(...,False)` (contract.py L130-132), emitted by the ensemble builder (ensemble.py L577-579), and surfaced append-only in both the reflect_post value (runner.py L120-122) and the sidecar (L239-241). `reviewers_verified` is dynamically computed (ensemble L535-537); `verification_verified`/`regression_verified` are honestly always-False in the headless seam (documented, ensemble L573-576) — a faithful "this run did not verify" signal, not a phantom.
- **Reviewer-shortfall VISIBLE token (required detail):** PRESERVED. `reviewer-shortfall` is appended to `degraded_components` only on a genuine shortfall (ensemble L538-540) and is intentionally BENIGN — not a `_DEGRADED_COMPONENTS_HALT_SET` member — so a 2-of-3 outcome stays PASS-eligible (FR-RH2.9).
- **Clean-run `verification_skip_reason` UNCHANGED (required detail):** PRESERVED. Still `verification_ran: False` + `verification_skip_reason: "tool-unavailable"` (ensemble L571-572), which remains in `_VERIFICATION_SKIP_EXEMPTIONS` (contract.py L36-38) → exempt, R2-F2 preserved, no clean-run skip-reason flip.
- **Aggressive degrade routings HALTED (required detail):** PRESERVED. Neither `_VERIFICATION_SKIP_EXEMPTIONS` nor `_DEGRADED_COMPONENTS_HALT_SET` was edited (git diff confirms). The two verdict-DEGRADE routings are recorded as `needs_human_decision` PENDING markers (`fx7-degrade-on-unverified-DECISION.md`, `fx7-degrade-on-reviewer-shortfall-DECISION.md`), each documenting Option A (shipped, additive) vs Option B (deferred, non-additive, requires human authorization). This satisfies the project rule "human-decision items must HALT, not auto-apply."

---

## Faithfulness Analysis (Deferral is NOT a Coverage Gap)

The spawn brief's DOCUMENTATION-STALENESS OVERRIDE requires that where the plan/research and the CODE-VERIFIED reality (research/07, research/08 + actual code) conflict, the code wins. I independently verified the pivotal contradiction:

- Research 08 §G6 concluded FX7 is "NOT a human-decision item" and that "a populated `degraded_components` degrades WITHOUT any consumer edit (`contract.py:259-260`)." **This premise is itself CODE-CONTRADICTED.** I read `contract.py`: `_degraded_reason` Trigger 1-5 (L265) degrades ONLY when a token is a member of `_DEGRADED_COMPONENTS_HALT_SET` (L31-33 = `{serena, auggie, env-aliases, evidence-validator, serena:context-excluded}`). A bare `reviewer-shortfall` token is benign. So populating `degraded_components` does NOT degrade without adding the token to the HALT_SET (a consumer edit).
- Both PENDING markers correctly diagnose this and further show that Option B would REVERSE deliberate, tested designs: degrade-on-unverified reverses R2-F2 (`test_r2f2`/`test_i1`), and degrade-on-reviewer-shortfall reverses FR-RH2.9 (`test_i3`, where 2-of-3 is PASS-eligible).

**Conclusion:** the plan §2 literal text ("downgrade status→degraded when verification_ran:false") is the stale premise. The shipped implementation correctly followed the CODE-VERIFIED reality: it landed only the additive VISIBLE accounting (the `*_verified` fields + the benign `reviewer-shortfall` token) and HALTED the two aggressive routings as `needs_human_decision` PENDINGs. The shipped visible-accounting + the two PENDING markers together ARE the faithful realization of the "honest-accounting" intent under the code conflict, per driving-plan §3.4. This is fidelity, not a gap.

---

## Adversarial Probes (assumed-partial hunt — all cleared)

Per the adversarial stance I actively hunted for partial/phantom coverage in the three in-scope fixes:

1. **"Phase-2 gate prerequisite" (FX3) / "Phase-4 FAIL rule" (FX5) wiring absent?** NOT a gap. Research 08 §G4 (CODE-VERIFIED) established the numeric "Phase 2/4" tokens are task-builder SKILL.md's OWN internal gate numbers, NOT a pytest attach point, and that FX3/FX5 are standalone CI + built-task L3 pytests with NO runtime gate wiring / NO SKILL.md §A.8/§A.10 edit. The absence of wiring is the faithful realization of the override, not phantom coverage.
2. **`verification_verified`/`regression_verified` always False → phantom field?** NOT a gap. They are honest fail-closed defaults for the headless seam (which runs no verification triangle); the plumbing reads them generically so a future verification-running path flows True. `reviewers_verified` IS dynamically computed. This is the additive visibility surface the intent asked for.
3. **FX5 scope-boundary helpers uncovered (classify / DetectionContract.from_yaml / load_evidence)?** NOT a gap. Documented as explicit NON-GOALS (conftest L110-114 / research 02 §4.3) handed to their own suites; FX5's charter is the 4 `contract_setup` modules.
4. **Did any excluded surface get silently touched?** NO. `git diff` vs base `46a787da` confirms contract.py's only change is the additive `_make_result` block; the two frozensets are byte-unchanged.

---

## Actions Taken
None — REPORT ONLY (`fix_authorization: false`). No files modified.

## Recommendations
- Green light for FX3/FX5/FX7 from a source-document-fidelity standpoint.
- The two FX7 `needs_human_decision` PENDINGs are correctly HALTED and remain open items for a human to accept/reject Option B; they must not be auto-resolved by any downstream gate.
- Out of this agent's scope (documented, not verified here): FX2 (`rf-qa-qualitative.md` item-5 augmentation) and FX1 (`reflect-reviewer.md` + `deviation-taxonomy.md`). A sibling fidelity agent should cover those.

## QA Complete
