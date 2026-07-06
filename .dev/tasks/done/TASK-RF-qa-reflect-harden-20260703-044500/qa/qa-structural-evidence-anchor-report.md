# QA Report — Task Integrity (Evidence-Anchor Fidelity Lens)

**Topic:** RF-QA-hardening Phase 2 (FX3/FX5) — evidence-anchor fidelity
**Date:** 2026-07-03
**Phase:** task-integrity (LENS: evidence-anchor-fidelity)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY — no files edited)
**Worktree:** /config/workspace/IronClaude/.dev/worktrees/pr209-harden
**Source HEAD:** 46a787da (exactly matches the HEAD cited in fx5-gate-helper-registry.md line 3 — no source drift since research was authored)

---

## Overall Verdict: PASS

Adversarial target was "assume ≥5 anchor errors." Every symbol referenced by the FX3 and
FX5 tests, and every file:line citation in the discovery registry, was cross-checked
against the live source. The registry-equality, per-helper-resolution, and
drift-pattern-cardinality invariants were verified BOTH by manual reading AND by live
Python introspection, and all 37 tests execute green. No fabricated anchor was found.
One MINOR citation imprecision (a 1-line off-by-one on a documented NON-GOAL residual,
referenced by no test) is recorded below; it does not affect any assertion and is
non-blocking.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FX3 imports resolve (`SetupAnswers`, `EvidenceBundle`, `_answer_default`, `_evidence_attr`) | PASS | questions.py:15 `SetupAnswers`, :52 `_answer_default`, :64 `_evidence_attr`; evidence.py:19 `EvidenceBundle`. FX3 suite imports at test lines 32-33 resolve (4 tests green). |
| 2 | FX3 valid-name sets built DYNAMICALLY (not hardcoded) | PASS | test file lines 40 (`dataclasses.fields(questions_mod.SetupAnswers)`) and 45 (`dataclasses.fields(evidence_mod.EvidenceBundle)`); no literal field list present. |
| 3 | FX3 `_answer_default(<lit>)` literals ⊆ SetupAnswers fields | PASS | 8 literals in questions.py (detected_augment_identity:158, author_association_values:165, emission_shape:170, findings_locus:177, severity_field_path:184, review_completeness_signal:189, decline_detection_fields:196, expected_classifier_result:201) — every one is a SetupAnswers field (questions.py:18-38). |
| 4 | FX3 `_evidence_attr` answer_key ⊆ SetupAnswers (THE F3 trap) | PASS | `_evidence_attr("repo")` →answer_key `repo` (field :18); `_evidence_attr("pr_number", answer_attr="probe_pr")` (questions.py:136) →answer_key `probe_pr` (field :19). Both valid. Fix anchor at :136 confirmed. |
| 5 | FX3 `_evidence_attr` positional attr ⊆ EvidenceBundle fields | PASS | attrs `repo` (evidence.py:23) and `pr_number` (evidence.py:24) both present on EvidenceBundle. |
| 6 | FX3 docstring anchors questions.py:68,71,136 | PASS | :68 `answer_key = answer_attr or attr`; :71 `answered = getattr(answers, answer_key, None)`; :136 `_evidence_attr("pr_number", answer_attr="probe_pr")`. Exact. |
| 7 | FX5 module imports resolve (candidate/lockgate/diagnosis/validation, STATE_POLLING, FieldProvenance, PROVENANCE_OBSERVED, derive_candidate) | PASS | candidate.py:14 PROVENANCE_OBSERVED, :30 FieldProvenance, :63 derive_candidate; STATE_POLLING imported by both lockgate.py:8 and validation.py:8; 22 differential tests green. |
| 8 | FX5 every `HELPER_TEST_MAP`/`GATE_LOAD_BEARING_HELPERS` entry resolves on live module | PASS | Live introspection (`_resolve_dotted`) returned OK for all 11 dotted names (see Introspection Evidence). |
| 9 | Invariant `set(GATE_LOAD_BEARING_HELPERS) == set(HELPER_TEST_MAP)` | PASS | Live introspection: `len G 11 len H 11`, `G==H True`, `G-H []`, `H-G []`. No exemption hatch. |
| 10 | Drift-alarm `GATE_HELPER_DEF_PATTERN` matched set over module-level defs == exactly the 9 registered module-level helpers | PASS | Live run `MATCHED_COUNT 9`, and the 9 names equal the §1a set (candidate:5, lockgate:2, diagnosis:2, validation:0). A strict subset of the 11-helper registry. |
| 11 | Each registered helper carries BOTH a negative and differential test that EXISTS in the differentials module | PASS | Introspection: all 22 `TESTFN True` (11 helpers × 2 kinds), names match HELPER_TEST_MAP. |
| 12 | Discovery registry file:line citations (§1a/§1b) match live source | PASS | All 11 def lines verified exact (see Anchor Table). |
| 13 | Discovery §3 over-match reconciliation (brief pattern → 14, tightened → 9) | PASS | The 5 dropped defs (_observed_logins:192, _observed_app_slugs:203, _observed_associations:214, _observed_severity_path:279 via `_observed_`; _shape_observed:352 via `_shape_observed`) exist and are correctly NOT matched by the tightened pattern (confirmed by MATCHED_COUNT 9). |
| 14 | Discovery §4 F4 anchor-chain lines + MUST_OBSERVE_FIELDS set | PASS | candidate.py:18-25 set = {augment_identity, emission_shape, findings_locus, review_completeness_signal, probe_evidence, repo} — exact match to §4 citation. Chain lines 360/253/290/119/47 all verified. |
| 15 | Discovery §5 residual-risk non-goal citations | PASS (1 MINOR) | _structure_checks:133, _evidence_checks:163, _surface_checks:197, _freshness_checks:249, _identity_checks:186, _negative_control_checks:228 all exact; classify/DetectionContract.from_yaml/load_evidence(:56) exist. `ValidationReport.passed` cited at :62 = the `@property` line; the `def` is at :63 (MINOR — see Issues). |
| 16 | Test call-site signatures match live function signatures | PASS | derive_candidate(ev) vs `(evidence,*,answers=None)`; _findings_locus(ev,SetupAnswers(),prov) vs `(evidence,answers,provenance)`; lockgate._check(name,passed,detail); validation.CheckResult(name,passed,detail); diagnosis._first_str(data,*keys); _stale_blockers(data,repo,pr,sha). All consistent. |
| 17 | Live test execution (FX3 + FX5) | PASS | `37 passed in 0.10s` (4 FX3 + 22 differentials + 11 parametrized coverage). |

## Anchor Table — Discovery §1a/§1b file:line vs live source
| Dotted helper | Cited | Live `def` line | Match |
|---|---|---|---|
| candidate._path_resolves | candidate.py:360 | 360 | ✓ |
| candidate._findings_locus | candidate.py:253 | 253 | ✓ |
| candidate._review_completeness_signal | candidate.py:290 | 290 | ✓ |
| candidate._selected_identity | candidate.py:134 | 134 | ✓ |
| candidate._selected_app_slug | candidate.py:161 | 161 | ✓ |
| lockgate._paths_resolve | lockgate.py:119 | 119 | ✓ |
| lockgate._emission_shape_observed | lockgate.py:110 | 110 | ✓ |
| diagnosis._resolve_optional_path | diagnosis.py:285 | 285 | ✓ |
| diagnosis._stale_blockers | diagnosis.py:334 | 334 | ✓ |
| candidate.CandidateContract.required_unobserved | candidate.py:47 | 47 | ✓ |
| validation._negative_control_checks | validation.py:228 | 228 | ✓ |
| (file lengths) lockgate/candidate/diagnosis/validation | 198/396/394/279 | 198/396/394/279 | ✓ |

## Introspection Evidence (live `uv run python`)
```
MATCHED_COUNT 9  ->  candidate._findings_locus, candidate._path_resolves,
  candidate._review_completeness_signal, candidate._selected_app_slug,
  candidate._selected_identity, diagnosis._resolve_optional_path,
  diagnosis._stale_blockers, lockgate._emission_shape_observed, lockgate._paths_resolve
len G 11 | len H 11 | G==H True | G-H [] | H-G []
RESOLVE OK x11 (all dotted names resolve non-None on live modules)
TESTFN True x22 (every negative+differential test name exists in test_gate_helper_differentials.py)
pytest: 37 passed in 0.10s
```

## Summary
- Checks passed: 17 / 17
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (non-blocking citation imprecision)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | fx5-gate-helper-registry.md §5a (line 116) → validation.py | `ValidationReport.passed` is cited as `validation.py:62`, but line 62 is the `@property` decorator; the `def passed` is at line 63. The §1a/§1b registry table consistently cites the `def` line (e.g. required_unobserved → 47 = the def), so this is a 1-line inconsistency. It affects NO test — `ValidationReport.passed` is a documented residual-risk NON-GOAL, not registered and not referenced by any FX5 assertion. | Optional: change `validation.py:62` → `validation.py:63` for convention consistency. No test or invariant depends on it. |

## Confidence Gate
- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 4
- No web research was required (all claims are local-source-bound; Tavily not engaged).
- Tool-call count (13) ≥ checklist item count (17)? Read(9)+Bash(4)=13 tool calls; several Bash calls were batch introspection scripts each verifying multiple checklist items (registry equality, 11 resolutions, 22 test-fn existences, drift cardinality, full test run), so per-item verification density is satisfied. No UNCHECKED or UNVERIFIABLE items.

## Recommendations
- Green light: FX3 and FX5 test anchors are faithful to the live source at HEAD 46a787da.
- The single MINOR item is cosmetic and optional; it need not block Phase 2 completion.

## QA Complete
