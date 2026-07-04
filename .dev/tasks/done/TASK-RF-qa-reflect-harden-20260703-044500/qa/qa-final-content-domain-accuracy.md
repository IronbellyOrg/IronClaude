# QA Report — Task Qualitative (FINAL M3 gate, domain-accuracy lens)

**Topic:** Additively harden RF QA + /sc:reflect vs the PR #209 correctness-bug class (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Phase:** task-qualitative (domain-accuracy sampling lens)
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)
**Adversarial premise tested:** "≥5 claims contradict the actual codebase." Result: premise NOT confirmed — 0 contradictions found across the sampled claims after independent code verification.

---

## Overall Verdict: PASS

## Items Reviewed (sampled claims, one per verified fact)
| # | Check (claim under review) | axis | Result | Evidence |
|---|----------------------------|------|--------|----------|
| 1 | FX3: `SetupAnswers` has 17 fields (R-002) | none | PASS | questions.py:18-38 — counted exactly 17 fields (repo…next_step) |
| 2 | FX3: `EvidenceBundle` has 13 attrs (R-002) | none | PASS | evidence.py:22-36 — counted exactly 13 fields (probe_dir…cross_pr_shape_only) |
| 3 | FX3: fixed call is `_evidence_attr("pr_number", answer_attr="probe_pr")` at questions.py:136 | none | PASS | questions.py:136 — literal match |
| 4 | FX3: silent-getattr locus at questions.py:68,71 | none | PASS | questions.py:68 `answer_key = answer_attr or attr`; :71 `getattr(answers, answer_key, None)` |
| 5 | FX3: evidence-side attrs `repo`/`pr_number` exist on EvidenceBundle | none | PASS | evidence.py:23-24 both present; test green |
| 6 | FX5: all 11 registered gate helpers resolve on live modules | none | PASS | ran `conftest._resolve_dotted` on each — all resolve to `function` |
| 7 | FX5: drift-alarm pattern matches EXACTLY the 9 module-level helpers ("never a superset") | none | PASS | ran `conftest._module_level_gate_shaped_defs()` → 9, set-equal to the 9 registered |
| 8 | FX5: differential tests reference real behavior (`_path_resolves`, `_findings_locus`, `required_unobserved`, `MUST_OBSERVE_FIELDS`, `classify`, `STATE_POLLING`) | none | PASS | test_gate_helper_differentials.py green (all imports resolve; mutation tests flip real provenance) |
| 9 | FX7: `build_reflect_contract` emits `verification_verified`/`reviewers_verified`/`regression_verified` | none | PASS | ensemble.py:577-579 |
| 10 | FX7: `reviewer-shortfall` token appended on genuine shortfall (`reviewers_requested not None and reviewer_count < reviewers_requested`) | none | PASS | ensemble.py:538-540 |
| 11 | FX7: fields surface through `_make_result` → `ReflectResult` → reflect_post/sidecar | none | PASS | contract.py:130-132 (_make_result assigns); models.py:158-160 (ReflectResult fields); runner.py:120-122,239-241 (2 surfacing sites) |
| 12 | FX7 additive-safety: `reviewer-shortfall` NOT in `_DEGRADED_COMPONENTS_HALT_SET` (verdict-benign) | none | PASS | contract.py:31-33 set = {serena,auggie,env-aliases,evidence-validator,serena:context-excluded}; token absent; membership check at :265 |
| 13 | FX7: exemption set at contract.py:36-38 contains `tool-unavailable` (clean-run stays exempt) | none | PASS | contract.py:36-38 |
| 14 | FX2: cross-symbol input-shape invariant annotated `axis: AX-2` in Code Compatibility item 5 | none | PASS | rf-qa-qualitative.md:674 (Module context analysis, item 5) |
| 15 | FX2: AX-2 = Contradictions | none | PASS | rf-qa-qualitative.md:597 `**AX-2 Contradictions**` |
| 16 | FX2: count header still `Checklist (15 items)`, no AX-6 introduced | none | PASS | rf-qa-qualitative.md:660; `grep -c AX-6` = 0 |
| 17 | FX2/FX1: F1 example symbols (`diagnose()`, `load_evidence()`, `_evidence_sha256()`) are REAL and behave as described | none | PASS | diagnose diagnosis.py:63; load_evidence evidence.py:56 (dir); _evidence_sha256 diagnosis.py:294; file/dir handling diagnosis.py:296 |
| 18 | FX1: deviation taxonomy is exactly 4 classes (Authorized/Necessary/Drift/Regression) | none | PASS | deviation-taxonomy.md:26,40,56,73 |
| 19 | FX1: Regression is spec-relative (documented invariant / spec behavior) as cited by the coverage-gap justification | none | PASS | deviation-taxonomy.md:81 + :160 justification |
| 20 | FX1: Correctness-gap is advisory-only (no 5th class; never sets regression_present / status:partial) | none | PASS | deviation-taxonomy.md:156-181; reflect-reviewer.md:30,101-115 |
| 21 | FX1: reflect-reviewer `persona_lens` includes free-form `no-spec-correctness` | none | PASS | reflect-reviewer.md:56 |

<!-- All rows PASS → axis = `none` (five-axis lens applied, surfaced nothing).
     AX-1 Drift was ACTIVE (BUILD_REQUEST.GOAL verbatim available at task R-001, line 118);
     citation freshness was actively checked (line numbers 136 / 68 / 71 / 31-33 / 36-38 all
     matched current source) and AX-1 did not fire. AX-5 Invented-content was the primary
     adversarial target for the F1 example and FX5 registry — cross-checked every named symbol
     against the filesystem; none invented. -->

## Summary
- Checks passed: 21 / 21
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)
- Test corroboration: `tests/pr_submit/{test_setup_questions_resolution,test_gate_helper_differentials,test_gate_helper_coverage}.py` + `tests/cli/reflect/` → 210 passed, 1 xpassed. FX2 guards `tests/audit/` (5 files) → 61 passed.

## Issues Found
None. No CRITICAL, IMPORTANT, or MINOR domain-accuracy discrepancies surfaced across any of the five FX.

## Actions Taken
None (report-only). All findings are verifications, not mutations.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was present in the spawn prompt → fell back to STANDALONE behavior (Critical Rule #11 / release-spec §19.4). No structural PASS items were relied upon; every claim below was independently tool-verified.

**(b) Independent semantic checks (≥1 required, INV-019):**
- FX3 field-count claims: independently counted dataclass fields by Reading questions.py:18-38 (17) and evidence.py:22-36 (13) rather than trusting the research note R-002.
- FX5 "never a superset" equality claim: executed `conftest._module_level_gate_shaped_defs()` in a live `uv run python` process and set-compared to the registry — a computation the structural gate cannot perform (it only checks the subset direction).
- FX7 surfacing chain: traced the field from emission (ensemble.py:577-579) through `_make_result` assignment (contract.py:130-132), the `ReflectResult` dataclass (models.py:158-160), to both runner surfacing sites (runner.py:120-122, 239-241) — verified end-to-end wiring, not mere field presence.
- FX7 additive-safety: Read `_DEGRADED_COMPONENTS_HALT_SET` (contract.py:31-33) to confirm `reviewer-shortfall` is genuinely absent, proving the new token cannot flip the verdict.
- F1 example groundedness: grepped `_evidence_sha256` across src/ + tests/ and confirmed the symbol exists at diagnosis.py:294 (the AX-5 invented-content adversarial probe) rather than assuming the brief's example was illustrative-only.

## Self-Audit answers (mandatory)
1. **Independently verified factual claims:** 21 sampled claims (see table), each against source code or live execution — no claim accepted from the research notes without independent confirmation.
2. **Files read to verify:** questions.py, evidence.py, diagnosis.py, tests/pr_submit/{conftest.py, test_setup_questions_resolution.py, test_gate_helper_differentials.py}, cli/reflect/{ensemble.py, contract.py, models.py} (+ runner.py via grep), agents/{rf-qa-qualitative.md, reflect-reviewer.md}, skills/sc-reflect-protocol/refs/deviation-taxonomy.md, and the task file.
3. **Why trust a 0-issue verdict:** every row cites a concrete file:line or a reproducible command (`_module_level_gate_shaped_defs()`, `_resolve_dotted`, `grep -c AX-6`). The two most error-prone areas were actively adversarially probed: the FX5 "never a superset" claim was recomputed live (found exactly 9, not "≤9"), and the F1 example's least-obvious symbol `_evidence_sha256()` was grep-confirmed to exist rather than assumed. 210 + 61 tests independently corroborate the green state.
4. **Web research:** none performed — every claim was local-file / local-execution bound. No Tavily/WebFetch fallback was needed or invoked.

## Confidence
- **Confidence:** "Verified: 21/21 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 11 | Grep: 6 | Glob: 0 | Bash: 4 (incl. 2 live `uv run python`/`pytest` executions)"
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations
- None blocking. The domain-accuracy lens is clean: every sampled test assertion, contract field name, and brief anchor across FX1/FX2/FX3/FX5/FX7 matches the actual code and behavior in the current tree (HEAD of worktree pr209-harden).
- Green light to proceed on this lens.

## QA Complete
