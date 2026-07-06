# QA Report — Report Validation (FINAL M3 gate)

**Topic:** PR-209 QA + Reflect hardening — evidence-anchor fidelity across FX1/FX2/FX3/FX5/FX7
**Date:** 2026-07-03
**Phase:** report-validation
**Lens:** evidence-anchor-fidelity
**Fix authorization:** false (REPORT ONLY)
**Fix cycle:** N/A (re-run after transient API error left a PENDING stub)

---

## Overall Verdict: PASS

Adversarial premise ("assume ≥5 edits cite a wrong or hallucinated anchor") was **not borne out**.
Across a sample spanning all five FX surfaces, every cited symbol resolves at its cited file, every
line-anchor in shipped code comments is correct, both DO-NOT-TOUCH frozensets are byte-unchanged, and
all 90 FX3/FX5/FX7 tests pass green — runtime proof that every anchor resolves, not just static reads.
Zero anchor-fidelity failures found. The premise's "≥5 wrong anchors" is a false-pressure prior; the
evidence overwhelmingly contradicts it.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FX3: `SetupAnswers`/`EvidenceBundle`/`_answer_default`/`_evidence_attr` exist at cited locations | PASS | `SetupAnswers` questions.py:15; `_answer_default` questions.py:52; `_evidence_attr` questions.py:64; `EvidenceBundle` evidence.py:19. All Read directly. |
| 2 | FX3: fix anchor + docstring line citations (68, 71, 136) | PASS | questions.py:68 `answer_key = answer_attr or attr`; :71 `getattr(answers, answer_key, None)`; :136 `_evidence_attr("pr_number", answer_attr="probe_pr")`. Test docstring citations exact. |
| 3 | FX3: `augment_app_slug` cited as real-but-unreferenced field | PASS | questions.py:28 `augment_app_slug: str \| None = None` present; correctly excluded by SUBSET direction. |
| 4 | FX5: `GATE_LOAD_BEARING_HELPERS` (11) ≡ `HELPER_TEST_MAP` keys (11) | PASS | conftest.py:117-131 (11 entries) vs test_gate_helper_differentials `HELPER_TEST_MAP` — set-equal, introspected live. |
| 5 | FX5: each of 11 helpers resolves in candidate/lockgate/diagnosis/validation.py | PASS | `uv run python` hasattr probe: all 11 → OK (incl. `CandidateContract.required_unobserved`, `validation._negative_control_checks`). |
| 6 | FX7: ensemble.py edits match anchors | PASS | `reviewers_requested` kwarg ensemble.py:509; `reviewers_verified` :535-540; `*_verified` keys :577-579; shortfall token :540. |
| 7 | FX7: `verification_skip_reason` still `"tool-unavailable"` | PASS | ensemble.py:572 byte-unchanged; comment at :530 cites `contract.py:31-33` correctly. |
| 8 | FX7: `_VERIFICATION_SKIP_EXEMPTIONS` + `_DEGRADED_COMPONENTS_HALT_SET` unchanged | PASS | contract.py:31-33 HALT_SET = {serena,auggie,env-aliases,evidence-validator,serena:context-excluded}; :36-38 EXEMPTIONS = {read-only-project,tool-unavailable,--no-verify}. Both match pre-edit exactly. |
| 9 | FX7: models.py + contract.py `_make_result` edits match anchors | PASS | models.py:158-160 three defaulted `*_verified` fields after `reviewer_grounding_root` (:152); contract.py:130-132 `c.get(..., False)` population. |
| 10 | FX2: item-5 augmentation cites real siblings | PASS | `diagnose()` diagnosis.py:63; `load_evidence()` evidence.py:56; `_evidence_sha256()` diagnosis.py:294. All exist; file assignments correct (rf-qa-qualitative.md:674). |
| 11 | FX1: reflect-reviewer.md + deviation-taxonomy.md edits anchored | PASS | reflect-reviewer.md:30 advisory note, :56 `no-spec-correctness` persona_lens, :101 `## Correctness gaps`, :5 `tools:` unchanged (read-only preserved); deviation-taxonomy.md:156 `## Correctness-gap` parallel dimension. |
| 12 | Runtime anchor resolution (FX3+FX5+FX7 tests green) | PASS | `uv run pytest` 90 passed in 0.31s — every AST/introspection/hasattr anchor resolves at runtime. |

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Issues Found

None at the evidence-anchor-fidelity level. No wrong or hallucinated anchor was found in the sample.

## Observations (non-gating, out of lens — logged for completeness)

| # | Severity | Location | Observation |
|---|----------|----------|-------------|
| 1 | INFO | `phase-outputs/discovery/fx7-editmap.md:52,61,64,71` | The edit-map plan doc uses PRE-EDIT line anchors (L502, L550-551, L560) that shifted post-edit (:509, :571-572, :588). This is **self-documented** at lines 46-50 as cosmetic plan-doc drift, and it explicitly redirects to the Gate-B reports for authoritative post-edit anchors. The *shipped code* comment anchors (e.g. ensemble.py:530 → `contract.py:31-33`) are correct. NOT a code anchor defect. |
| 2 | INFO | `src/superclaude/agents/reflect-reviewer.md:101` & `:108` | Two `## Correctness gaps` headings appear, but :108 is INSIDE a fenced ```markdown``` block — it is the literal output template the reviewer emits, not a duplicated document section. Intentional (matches the doc's own "Report each as a row" framing at :105). NOT a structural defect. |

## FX2 shape-illustration note (verified, not a defect)

The FX2/FX1 illustration "a `diagnose()` that treats its probe argument as a file while sibling
`load_evidence()` / `_evidence_sha256()` accept a directory" is explicitly **hypothetical** (the F1 /
PR #209 bug *class*), not a claim about current behavior. Verified against source: `load_evidence`
accepts a directory (evidence.py:59 `root.is_dir()`), `_evidence_sha256` normalizes file→parent dir
then calls `load_evidence` (diagnosis.py:296), and `diagnose()` takes `repo/pr_number/cwd` (diagnosis.py:63-68).
All three symbols resolve at their cited files; the illustrative "diagnose treats probe as file" is a
worded example of the class, correctly caveated. No anchor misattribution.

## Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 12 | Grep: 0 | Glob: 0 | Bash: 10 (incl. live `uv run python` symbol introspection + `uv run pytest` 90-test green run; grep performed via Bash)
- Tool-call total (~22) exceeds the 12-item checklist minimum — no padding; each call mapped to a specific FX anchor.
- No web research performed (all claims are local source-truth; no external/URL/standards-bound anchor in scope).
- Every checklist item marked VERIFIED with cited tool output (file:line + introspection + pytest). No UNCHECKED, no UNVERIFIABLE.

**Self-audit:** If I told the user I found 0 anchor defects, would they believe me? Yes — because I can
point to (a) 11/11 live `hasattr` resolutions for FX5, (b) exact line reads for every FX3/FX7 anchor,
(c) byte-comparison of both DO-NOT-TOUCH frozensets against the edit-map's stated pre-edit values, and
(d) a 90-test green run that would have failed on any unresolved AST/import anchor. The adversarial "≥5
wrong anchors" prior was actively hunted (I checked the two frozensets for tampering, the shifted plan-doc
anchors, the double header, and the hypothetical `diagnose()` illustration) and each suspected defect
resolved to correct-and-intentional.

## Recommendations

- Green light on evidence-anchor fidelity. No remediation required for this lens.
- The two INFO observations are cosmetic/documentary; no action needed (both are self-documented as intentional).

## QA Complete
