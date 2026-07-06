# QA Report — task-qualitative (operational-correctness lens)

**Topic:** TASK-RF-qa-reflect-harden-20260703-044500 (FX1/FX2/FX3/FX5/FX7 additive hardening)
**Date:** 2026-07-03
**Phase:** task-qualitative
**Fix cycle:** N/A
**fix_authorization:** false (report-only)
**Lens:** operational-correctness (will each item actually work against CURRENT source?)

---

## Overall Verdict: PENDING (appended below)

Adversarial stance active. Assume execution failure; verify every anchor against live source.

## Verification Log (appended incrementally)

Verified against live source at HEAD `46a787dac39c75753a6da4ca483dc6b5d2581bb0` (confirmed via `git rev-parse HEAD`). BUILD_REQUEST.GOAL captured verbatim from spawn prompt + task R-001 ("Additively harden RF QA + /sc:reflect vs the PR #209 F1-F4 spec-conformant correctness-bug class ... regression-guards ... ADDITIVE-ONLY, weaken NO existing gate") → **AX-1 Drift axis ACTIVE** for this review.

**FX7 (ensemble.py) — anchors confirmed:** `build_reflect_contract` def L492; `reviewer_count = len(succeeded)` L517; `"verification_ran": False` L550; `"verification_skip_reason": "tool-unavailable"` L551; `"degraded_components": []` L560; call site `run_tier2_ensemble` def L168, `reviewers = int(config.reviewers)` L191, builder call L302-327. Only ONE src caller (L302). Trigger-12 mechanism at contract.py:288-291 confirmed (verification_ran is False AND skip_reason NOT in `_VERIFICATION_SKIP_EXEMPTIONS` {read-only-project, tool-unavailable, --no-verify} L36-38 → "verification-skipped" degrade). **Mechanism is sound BUT unconditionally applied — see CRITICAL-1.**

**FX3 (questions.py/evidence.py) — GREEN:** `SetupAnswers` = 17 fields incl. intentionally-unreferenced `augment_app_slug` (subset direction justified). `_answer_default` L52, `_evidence_attr(attr, answer_attr)` L64 with `answer_key = answer_attr or attr` L68. All `_evidence_attr` call sites clean: `_evidence_attr("repo")` (answer_key repo ∈ SetupAnswers, evid repo ∈ EvidenceBundle), `_evidence_attr("pr_number", answer_attr="probe_pr")` (answer_key probe_pr ∈ SetupAnswers, evid pr_number ∈ EvidenceBundle). EvidenceBundle is a frozen dataclass with `repo` + `pr_number` present → `dataclasses.fields()` works. FX3 test will pass green; AST design (collect only `_answer_default`/`_evidence_attr` Name-calls) correctly ignores the 7 other derivers. No false-fail/false-pass found.

**FX5 (4 modules) — anchors GREEN:** candidate `_path_resolves`:360, `_findings_locus`:253, `_review_completeness_signal`:290, `_selected_identity`:134, `_selected_app_slug`:161, `CandidateContract.required_unobserved`:47, `MUST_OBSERVE_FIELDS`:18; lockgate `_paths_resolve`:119, `_emission_shape_observed`:110; diagnosis `_resolve_optional_path`:285, `_stale_blockers`:334; validation `_negative_control_checks`:228. Registry ≡ HELPER_TEST_MAP.keys() ⊇ drift-alarm-matched (9 module-level gate-shaped defs) is coherent as written; hand-registered dataclass-method/`_*_checks` pair (required_unobserved, _negative_control_checks) are documented non-auto-enumerable. Step 2.8 green-able. (Drift-alarm regex must exclude `_*_checks`/`ValidationReport.passed`/`required_unobserved` while matching the 9 defs — specified adequately; executor-dependent, not a defect.)

**FX2 (rf-qa-qualitative.md) — anchors GREEN:** `#### Checklist (15 items)` at :660; closed axis vocab `{AX-1..AX-5,none}` at :639; `##### Code Compatibility` at :670. Audit guard `test_five_axes_overlay.py:28 CHECKLIST_HEADER = "#### Checklist (15 items)"` — Branch A (keep 15, augment in place, AX-2) keeps it green. Step 4.4 runs `make sync-dev && make verify-sync` BEFORE the 5 audit tests (correct ordering).

**FX1 (reflect-reviewer.md / deviation-taxonomy.md) — anchors GREEN:** `tools:` frontmatter at :5 (guarded by test_reviewer_readonly_tools; FX1 body-only edits avoid it); `persona_lens` free-form "e.g." field at :54 (task correctly treats as non-enum). Advisory-only framing consistent.

**Reflect wrapper (PC.11) — GREEN:** `superclaude reflect run` = commands.py:216/320; options `--promote/--no-promote`, `--depth`, `--fix/--no-fix`, `--base` all real. Wrapper uses `--depth deep --fix --promote`, no `--base` (base from start_commit) → valid.

**PER_PHASE gates (Q7) — GREEN:** Phase 2→Gate A, Phase 3→Gate B, Phase 4→Gate C (each 5-agent, serialized fix); Phase 5 = VALIDATION (full pytest + scoped ruff + verify-sync); final M3 gate (≥6 agents) + M4 fidelity gate. UNIT testing present (FX3/FX5/FX7 unit tests). No implementation phase lacks a gate.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-2 | FAIL | FX7 Step 3.5 `uv run pytest tests/cli/reflect/` will NOT be green: Step 3.2(c)'s unconditional skip-reason change flips existing clean-PASS builder tests to DEGRADED. `reflect run`/make targets/ruff otherwise valid. |
| 2 | Project convention (SoT/sync) compliance | none | PASS | FX2/FX1 edit only src/; Step 4.4/4.5/5.1 run make sync-dev before audit tests; cli/reflect + tests/ correctly noted as non-sync surfaces. |
| 3 | Intra-phase execution-order simulation | none | PASS | Discovery→build→test→gate ordering sound in every phase; fixtures (3.4a) precede tests (3.4b-d); conftest registry (2.7a) precedes coverage module (2.7b). |
| 4 | Function-signature / value verification | AX-2 | FAIL | FX7 additive `reviewers_requested` kwarg + None-guard is signature-safe, BUT the L551 value change breaks existing consumers' pinned assertion (test_ensemble_unit.py:360). FX3/FX5 signatures all resolve. |
| 5 | Module-context analysis | none | PASS | ensemble/contract/models/runner module constants (`_VERIFICATION_SKIP_EXEMPTIONS`, `_LOAD_BEARING_BOOL_FIELDS`, `_DEVIATION_KEYS`) correctly identified; FX7 respects int-coercion + bool-sibling constraints. |
| 6 | Downstream-consumer analysis | AX-3 | FAIL | FX7 changes builder output consumed by derive_verdict → the clean-PASS path (test_i1_positive_witness_real_fanout, test_ensemble_stub_integration.py:168-169) is NOT updated; consumer regression unaddressed. |
| 7 | Test validity (real, not stub) | none | PASS | FX3 AST test + FX5 differential (monkeypatch-mutation-must-flip) tests are substantive; precedents (test_no_scoring_engine, existing F4 pair) are real. |
| 8 | Test coverage of primary use case | none | PASS | FX3 covers full deriver set; FX5 per-helper negative+differential; FX7 unit + verdict-mapping + writeback. |
| 9 | Error-path coverage | none | PASS | FX7 None-guard on `reviewers_requested` (avoids `>= None` TypeError); needs_human_decision HALT clause for exemption-set edit. |
| 10 | Runtime failure-path trace | AX-2 | FAIL | Data flow: build_reflect_contract (L551 non-exempt) → derive_verdict → Trigger-12 fires for EVERY ensemble run → existing PASS-expecting tests break; Step 3.5 revert clause then unwinds FX7. Task cannot reach green + additive simultaneously. |
| 11 | Completion-scope honesty | AX-2 | FAIL | Task claims FX7 is "STRICTLY ADDITIVE ... no behavior change to existing consumers" (Phase 3 preamble, Key Constraints) — false: the mechanism inherently changes an existing emitted value multiple existing tests pin. |
| 12 | Ambient-dependency completeness | none | PASS | FX7 threads through ReflectResult (3.3a) → _make_result (3.3b) → reflect_post + sidecar (3.3c); FX5 conftest registry + coverage module wired. |
| 13 | Kwarg-sequencing red flags | none | PASS | `reviewers_requested` param added in same item (3.2) that threads it; ReflectResult fields (3.3a) precede _make_result population (3.3b). |
| 14 | Function-existence claims grep-verified | none | PASS | All FX3/FX5/FX7 "exists at L…" claims grep-confirmed against live source (see Verification Log). No hallucinated symbol. |
| 15 | Template/cross-reference accuracy | none | PASS | rf-qa-qualitative.md :639/:660/:670, reflect-reviewer.md :5/:54, deviation-taxonomy anchors, audit CHECKLIST_HEADER all confirmed. |

<!-- AX-1 Drift axis ACTIVE (GOAL captured). It did not fire as the most-specific axis on any row; the FX7 defect is most-specifically a contradiction (AX-2) between the mechanism and existing pinned tests / the R2-F2 design, plus an omission (AX-3) of the required test-update items. Drift from the ADDITIVE-ONLY GOAL is a downstream symptom of the same AX-2 root, so AX-2 is recorded. -->

## Summary
- Checks passed: 9 / 15
- Checks failed: 6 (all trace to the single FX7 root defect)
- Critical issues: 1 (FX7 non-additive skip-reason change — multi-test regression + self-contradicting revert clause + reverses prior R2-F2 design)
- Important issues: 0 standalone (the 6 failing rows are facets of CRITICAL-1)
- Minor issues: 1 observation (FX5 drift-alarm regex is executor-dependent — specified, not a defect)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)
- Axis lens status: AX-1 Drift ACTIVE (GOAL baseline captured; not emitting `drift-axis-inactive`).

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Task Step 3.2(c) + 3.4b(b) + 3.5 vs `tests/cli/reflect/test_ensemble_unit.py:360`, `tests/cli/reflect/test_ensemble_stub_integration.py:168-169` | FX7 Step 3.2(c) changes `ensemble.py:551` `verification_skip_reason` from the EXEMPT `"tool-unavailable"` to a NON-exempt token **unconditionally** (the builder always emits `verification_ran: False`). This makes EVERY ensemble contract fire Trigger-12 → DEGRADED/exit-11. Pre-existing tests that pin the exempt value / expect a clean PASS from the builder REGRESS: (a) `test_r2f2_build_reflect_contract_emits_honest_verification_fields`:360 asserts `== "tool-unavailable"`; (b) `test_i1_positive_witness_real_fanout`:168-169 asserts `Verdict.PASS` / `exit_code == 0` on a clean 3-reviewer run (likely more clean-PASS stub tests too). The task provides NO item to update these tests. Worse, Step 3.5's clause "if a failure is in an EXISTING test … REVERT the offending FX7 change" would unwind the FX7 mechanism, and Step 3.4b(b)'s NEW test asserting a non-exempt reason directly CONTRADICTS test_r2f2. The task's own "STRICTLY ADDITIVE / no behavior change to existing consumers" constraint is violated by FX7's core mechanism. It also silently REVERSES the deliberate prior fix R2-F2 (documented at test_ensemble_unit.py:342-351: the ensemble was *made* to emit the exempt reason precisely so clean Tier-2 runs don't spuriously degrade) with no reconciliation. Result: Phase 3 will thrash at Step 3.5 / Gate B and cannot satisfy green-AND-additive. | Add explicit Phase-3 items that (1) UPDATE `test_r2f2` (assertion L360 + its docstring) and every clean-PASS ensemble/stub test to the new honest-degrade expectation, framed as a deliberate supersession of R2-F2; (2) carve `test_r2f2`/`test_i1` OUT of Step 3.5's "revert on existing-test failure" clause (those failures are EXPECTED, not regressions); and (3) reconcile the FX7 goal vs R2-F2 in the task preamble. ALTERNATIVELY, if FX7 must remain truly additive, gate the skip-reason flip on reviewer-shortfall only — but then the task must drop the "verification never ran → always degrade / no vacuous PASS" framing in 3.2(c)/3.4b(b), because a clean full-reviewer unverified run would still route a vacuous PASS (the very F-class FX7 claims to close). The task must pick one coherent design and encode its test-update consequences. |
| 2 | MINOR | Task Step 2.7a (FX5 drift-alarm) | The single "gate-shaped module-level def" regex governing registry + alarm + pairs is described but not literally specified; green-ness of Step 2.8 depends on the executor authoring a pattern that matches exactly the 9 resolution/lockability/provenance defs while excluding the `_*_checks` family, `ValidationReport.passed`, and the `required_unobserved` dataclass method. Achievable and adequately constrained, but a mis-scoped pattern would false-trip the drift alarm. | No task change required; noted so the executor treats the pattern definition as load-bearing and validates it against the 9 known defs before Step 2.8. |

## Actions Taken
None — `fix_authorization: false` (report-only). All findings documented above.

## Self-Audit (INV-019)

**(a) Reliance list — rf-qa A.10 (Inherited Structural Verdict) PASS items I relied on (skipped structural re-check):**
- Relied on A.10 PASS for B2 self-containment / 5-field item structure (did not re-audit each item's ensuring/blocker/completion clauses).
- Relied on A.10 PASS for phase-structure + TB-Add-1..8 (item numbering, frontmatter schema, POST wrapper PC.11 penultimate / status→Done PC.12 last, Execution Context citation-free).
- Relied on A.10.25 research-alignment PASS (FX5 enforced-registry ≡ authored-pairs, no exemption hatch — accepted the *documentary* claim structurally).

**(b) Independent semantic checks where structural PASS was insufficient and my own tool work was required (≥1, INV-019):**
- **FX7 operational simulation (the decisive one):** A.10 verified item structure but NOT that the item's action works against live code. I Read `ensemble.py:492-568`, `contract.py:36-38/249-304`, and grepped every `build_reflect_contract`/`verification_skip_reason` test → discovered the unconditional L551 change regresses `test_ensemble_unit.py:360` + `test_ensemble_stub_integration.py:168-169` and reverses R2-F2. Structural PASS could never surface this — it required tracing the emit→derive_verdict→existing-test data flow.
- **FX3 green-ability:** Read `questions.py` deriver call sites + `evidence.py` EvidenceBundle fields to confirm every `_evidence_attr` answer_key ∈ SetupAnswers and evidence_attr ∈ EvidenceBundle (so the AST test passes green, not just that the item is well-formed).
- **FX2 audit-guard interlock:** Read `test_five_axes_overlay.py:28` to confirm the CHECKLIST_HEADER literal matches the :660 header Branch A preserves — verifying the tripwire stays green, which structure validation does not check.

## Confidence Gate
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 5 (via Bash) | Glob: 0 | Bash: 5
  - Tool-call count (≈14 targeted Read/Bash-grep) ≈ 15 checklist items → engagement floor met; each call mapped to a specific FX anchor/test, no padding.
  - No web research performed (all verification is local-file-bound) → no Tavily/fallback to report.

## Recommendations
1. **BLOCKER — do not execute Phase 3 as written.** Resolve CRITICAL-1 before the task runs: add the test-update items, carve the expected failures out of the Step 3.5 revert clause, and reconcile FX7 vs the R2-F2 design (or switch FX7 to a shortfall-gated flip and drop the "always degrade" framing). Until then Phase 3 / Gate B will loop and the additive-only invariant is unsatisfiable.
2. Have the FX7 research (research/03) explicitly note the R2-F2 precedent (test_ensemble_unit.py:342-363) and state the supersession decision, so the M4 fidelity gate has the reconciliation on record rather than re-discovering the conflict.
3. FX3, FX5, FX2, FX1, the PER_PHASE gate structure, and the PC.11 reflect wrapper are operationally sound as written — no changes needed there.

## Overall Verdict: FAIL

One CRITICAL operational defect (FX7 non-additive, multi-test-regressing, self-contradicting, R2-F2-reversing skip-reason change with no remediation items) + one MINOR observation. Per task-qualitative rules, ANY issue ⇒ FAIL. The four other fixes verify green; the failure is isolated to FX7 but is execution-blocking for Phase 3.

## QA Complete
