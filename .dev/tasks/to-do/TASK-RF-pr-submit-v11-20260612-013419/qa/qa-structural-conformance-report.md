# QA Report — Phase 3 Structural / Template-Conformance + Item-Shape Lens

**Topic:** pr_submit V1.1 — decline classification (FR-9.1 / T-1110/T-1111/T-1112 / EC-23)
**Date:** 2026-06-12
**Phase:** report-validation (Phase 3 delta conformance)
**Fix authorization:** false (report-only)
**Stance:** Adversarial — assumed ≥5 conformance errors and hunted for them.

---

## Overall Verdict: PASS

The Phase 3 deltas conform exactly to the documented V1.1 inventory. The adversarial
hypothesis (≥5 conformance errors) was **not borne out** — every documented claim
was verified against the actual files and cross-validated by execution. Specific
high-risk failure modes (bare mutable default, regex drift between source/ref,
decline-branch ordering, accidental `locked: true` flip) were each probed and
found clean.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `STATE_DECLINED = "declined"` present alongside STATE_* | PASS | classifier.py:21-24 — STATE_POLLING/CLEAN/FINDINGS/DECLINED defined contiguously; line 24 is exactly `STATE_DECLINED = "declined"` |
| 2 | Decline branch runs BEFORE polling/clean/findings (FR-9.1) | PASS | classifier.py:127-129 decline loop returns `STATE_DECLINED`; the `if not augment_reviews → STATE_POLLING` (131-133), findings (138-141), clean (142) branches ALL follow it. No early return precedes the decline loop |
| 3 | Exactly 3 new `DetectionContract` fields w/ correct defaults | PASS | detection.py:78-88 — `decline_phrase_regex` (78), `decline_retrigger_regex` (79-81), `accepted_trigger_phrases` (82-88). Exactly 3, no more. Defaults match canonical strings (verified by execution below) |
| 3a | `accepted_trigger_phrases` uses `field(default_factory=...)` NOT bare mutable | PASS | detection.py:82-88 `field(default_factory=lambda: [...])`. Runtime proof: two fresh instances return **distinct** list objects (`is not` → True) |
| 4 | `from_yaml` reads all 3 new keys via `data.get(...)` | PASS | detection.py:105-115 — `decline_phrase_regex` (105-107), `decline_retrigger_regex` (108-111), `accepted_trigger_phrases` (112-115) all via `data.get(...)` with default fallbacks. `from_yaml({})` reproduces field defaults exactly |
| 5 | Shipped ref `detection-contract.md` still `locked: false` | PASS | detection-contract.md:29 `locked: false`. Parsed YAML confirms `locked == False`. T-210 test (`test_t210_locked_false_halts`) PASSES — default `load()` still HALTs |
| 6 | Regex byte-equality: field == from_yaml == ref YAML | PASS | Execution cross-check: phrase, retrigger, accepted all `True` for field==from_yaml, field==ref, from_yaml==ref. No drift |
| 7 | `import re` present in classifier.py (is_decline uses re.search) | PASS | classifier.py:17 `import re`; used at is_decline lines 89, 91 |
| 8 | `__init__.py` re-exports `is_decline`, `STATE_DECLINED`; STATE_POLLING/CLEAN/FINDINGS NOT re-exported | PASS | __init__.py:21 imports both; __all__ lists `classify`,`is_decline`,`STATE_DECLINED`,`poll_augment_review` (38-44). STATE_POLLING/CLEAN/FINDINGS absent from imports and __all__ — matches inventory line 9 |
| 9 | Test suite green (8 prior + 6 new = 14) | PASS | `uv run pytest test_detection_contract.py` → **14 passed in 0.04s**. New: t1110, t1110b, t1111, t1112, t1112b, ec23 all PASS |
| 10 | `inv` marker registered (no --strict-markers failure) | PASS | pyproject.toml:114/139 `inv:` marker registered; `--strict-markers` (line 111) active; suite collects without marker error |
| 11 | Fixtures exist + schema-valid (decline-comment, decline-initial-poll, stale-decline-pre-watermark) | PASS | All 3 present in fixtures/ (dated Jun 12 12:20). Each has Augment-author comment, both-regex-matching body; stale fixture carries `watermark` + `expected.is_decline_with_watermark:false` |
| 12 | EC-23 watermark semantics: stale ignored, None accepts | PASS | classifier.py:93-96 strict `created > watermark`; `test_ec23_stale_pre_watermark_decline_ignored` PASSES (with-watermark False, no-watermark True) |

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

None. (Adversarial-stance note: each of the five most-likely defect classes was
specifically probed and ruled out — see Adversarial Probes below.)

## Adversarial Probes (defect classes hunted and ruled out)

| Hypothesized defect | Probe | Result |
|---|---|---|
| Bare mutable default on `accepted_trigger_phrases` (classic dataclass bug) | Instantiated two contracts, `is not` identity check | RULED OUT — distinct list instances (default_factory confirmed) |
| Regex drift between detection.py field and ref YAML | Byte-equality compare of field vs parsed ref vs from_yaml | RULED OUT — all three identical |
| Decline branch placed AFTER findings/clean (would miscount decline as findings, FR-9.1 violation) | Read control-flow order in classify() | RULED OUT — decline loop at 127-129 precedes all other returns |
| `from_yaml` silently dropping a new key (so YAML overrides ignored) | Confirmed all 3 keys threaded via data.get | RULED OUT — 3/3 present |
| Accidental `locked: true` flip in shipped ref (would break T-210 gate) | Parsed ref YAML + ran T-210 test | RULED OUT — locked:false, T-210 still HALTs |
| `accepted_trigger_phrases` ordering mismatch vs inventory canonical | Compared list order field vs ref | RULED OUT — `[auggie, augment, augmentcode]` in all sources |
| 4th/extra field smuggled into DetectionContract | Counted new fields in dataclass body 73-88 | RULED OUT — exactly 3 |

## Confidence

**Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

**Tool engagement:** Read: 5 | Grep: 1 | Glob: 0 | Bash: 4

Tool-call-to-check mapping: every check maps to a direct Read of the cited file
plus, for checks 3a/4/6/9/10, a Bash execution that independently re-derived the
claim (regex equality via runtime compare, list-identity for default_factory,
pytest run for test-green, marker registration grep). Verification calls
(10) ≥ checklist items effectively covered; no padding calls.

## Recommendations

- Green light. Phase 3 deltas are conformant to the documented inventory and the
  T-210 lock gate is unaffected.
- No action required before downstream phases consume this change-set.

## QA Complete

VERDICT: PASS
