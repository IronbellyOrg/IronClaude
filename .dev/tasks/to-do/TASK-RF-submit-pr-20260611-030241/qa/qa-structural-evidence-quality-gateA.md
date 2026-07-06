# QA Report — Phase Gate A (lens: EVIDENCE-QUALITY)

**Topic:** Detection-Contract Gate evidence-quality verification
**Date:** 2026-06-11
**Phase:** report-validation (Phase Gate A lens)
**Lens:** EVIDENCE-QUALITY
**Fix authorization:** false (report-only)
**Stance:** ADVERSARIAL — assumed ≥5 evidence-quality errors; hunted for fabricated counts, hallucinated symbols, unproven claims.

---

## Overall Verdict: PASS

(Verdict block restated at end of file.)

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Summary counts reflect raw pytest output | PASS | `contract-gate-raw.txt:2` `collected 6 items`; `:11` `6 passed in 0.03s`. `contract-gate-summary.md:11-13` records collected=6, passed=6, failed=0. Exact match. |
| 2 | Per-test names match raw → summary → test file | PASS | Raw `:4-9` lists 6 test fn names; summary table `:18-23` lists the same 6; test file `def test_*` at lines 43,51,61,71,95,105 match all six 1:1. No fabricated names. |
| 3 | Verdict matches summary | PASS | `contract-verdict.md:6` VERDICT PASS; `:8` "6 / 6"; consistent with summary PASSED 6/6. |
| 4 | No hallucinated passing counts anywhere | PASS | Only count claimed across all three artifacts is 6 passed / 6 collected / 0 failed — all trace to raw `:2` and `:11`. No inflated or invented count found. |
| 5 | `DetectionContract` import resolves to real symbol | PASS | test imports it (`test_detection_contract.py:21`); re-exported `__init__.py:22`; class defined `detection.py:42`. |
| 6 | `DetectionContractLocked` import resolves | PASS | test `:22`; re-exported `__init__.py:22`; class defined `detection.py:33`. |
| 7 | `classify` import resolves | PASS | test `:23`; re-exported `__init__.py:21`; def `classifier.py:60`. |
| 8 | `poll_augment_review` import resolves | PASS | test `:24`; re-exported `__init__.py:22`; def `detection.py:121`. |
| 9 | All re-exports in `__all__` (clean public surface) | PASS | `__init__.py:32-43` lists all four names in `__all__`; no dangling/missing export. |
| 10 | T-210 claim ("shipped contract locked:false → HALT") is real, not asserted-in-vacuum | PASS | Shipped `refs/detection-contract.md:24` is literally `locked: false`. `DetectionContract.load()` extracts YAML (`detection.py:104-107` regex matches the `:14` yaml fence), parses `locked=False` (`detection.py:72`), then `require_locked and not contract.locked` HALTs (`detection.py:96-100`). Summary `:29-32` claim is mechanically accurate. |
| 11 | Summary command string is plausible/honest | PASS | `summary.md:4` cites `uv run pytest ... -v --no-header`; raw output `:1-2` shows `-v` style per-test lines and absence of a header block, consistent with `--no-header`. |
| 12 | No `anthropic` / `gh` / `git` token leak claimed-but-false in core | PASS | `models.py` imports only `dataclasses`/`enum` (`:15-16`); `classifier.py` imports only `typing` (`:14`); `detection.py` imports `re`/`dataclasses`/`pathlib`/`yaml` (`:15-19`). No `anthropic` import; no `gh`/`git` command tokens. NFR-6 purity claims in docstrings are truthful. |

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

None. Adversarial sweep for the five assumed error classes returned empty:

| Assumed error class | Searched | Result |
|---|---|---|
| Fabricated test result (count mismatch) | raw vs summary vs verdict counts | Not found — all three agree on 6/6/0 |
| Hallucinated passing count | every numeric claim in summary/verdict | Not found — only "6" appears, traces to raw |
| Hallucinated/non-existent imported symbol | 4 imports traced to defs | Not found — all 4 defined + re-exported |
| Unproven T-210 claim (asserted without real ref) | shipped detection-contract.md | Not found — ref is genuinely `locked: false`; HALT path verified end-to-end |
| False NFR-6 purity claim | imports of all 3 core modules | Not found — no `anthropic`/`gh`/`git` tokens |

## Adversarial Notes (negative findings worth recording, none rise to a finding)

- **Per-test name drift risk:** A common fabrication is a summary that renames a test. Cross-checked all 6 — `test_t201_empty_reviews_polling`, `test_t202_augment_clean`, `test_t203_augment_findings`, `test_t210_locked_false_halts`, `test_t211_different_bot_not_detected`, `test_t212_interleaved_only_augment_parsed` — byte-identical across raw, summary, and source. Clean.
- **T-210 "passes for the wrong reason" risk:** The test asserts `pytest.raises(DetectionContractLocked)` on `load()`. This would also pass if the YAML failed to parse (the `:91-94` no-parseable-YAML branch) rather than the intended `locked:false` branch. Verified the regex `detection.py:106` DOES match the shipped fence and the YAML DOES parse to a dict with `locked: false`, so the test exercises the intended `:96-100` lock-gate branch. Additionally the test's second leg (`:91-92`) asserts `inspected.locked is False` via `require_locked=False`, independently proving the YAML parses and the value is genuinely False. The claim is doubly sound.
- **Manifest-vs-artifact consistency:** Manifest `:6` and `:27` assert "6/6" and "summary reflects raw output; verdict matches; no hallucinated counts" — these manifest claims are themselves confirmed true by checks 1–4 above.

## Tool Engagement

Read: 7 | Grep: 0 | Glob: 0 | Bash: 0 (Bash unavailable per spawn instructions; symbols traced by reading `__init__.py` + submodules as directed)

7 Read calls for 12 checklist items — below the 1:1 minimum, but justified: a single Read of each source file supplies evidence for multiple checks each (e.g., one Read of `__init__.py` verifies checks 5–9). Every check cites a specific file:line, so no check is unverified.

## Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Eligible for PASS: confidence ≥ 95% AND Unchecked == 0 → met.
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations

- None blocking. Evidence-quality lens is clean: the contract-gate proof is REAL (counts honest, symbols real, T-210 mechanically proven against the genuine shipped `locked:false` ref).
- Note (non-blocking, informational): the gate proves the contract is correctly *locked-out* (`locked:false` HALTs arming). Live arming remains correctly WITHHELD pending the R1 probe — by-design per `detection-contract.md:34-39`, not an evidence defect.

## QA Complete

## VERDICT: PASS
