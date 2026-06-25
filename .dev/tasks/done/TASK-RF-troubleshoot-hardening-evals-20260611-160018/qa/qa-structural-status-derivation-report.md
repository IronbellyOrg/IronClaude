# QA Report — Structural: backtest_status enum + derivation

**Topic:** backtest_status enum and its derivation (anti-vacuity) vs RELEASE-SPEC §4.5/§5.4
**Date:** 2026-06-12
**Phase:** task-integrity (structural code-correctness, adversarial)
**Fix cycle:** N/A (report-only, fix_authorization: false)

---

## Overall Verdict: PASS

Adversarial mandate was to assume >=5 errors in the enum and its derivation. I attempted to break each
of the 5 VERIFY items against the actual source and the verbatim spec excerpts in research/04. No defect
was found in any of the 5 items. Every claim below is backed by a file:line citation I personally read.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | backtest_status enum EXACTLY {not_run, partial, complete}, default not_run | PASS | catch_rate.py:30-37 defines `STATUS_NOT_RUN="not_run"`, `STATUS_PARTIAL="partial"`, `STATUS_COMPLETE="complete"`, tuple `BACKTEST_STATUS_VALUES` = those three only. Schema `$defs/backtestStatus` enum (catch_rate.schema.json:70-78) = `["not_run","partial","complete"]` — identical set, no extras. Default `not_run`: `_derive_backtest_status` returns `STATUS_NOT_RUN` on empty (catch_rate.py:110-111); spec §4.5/§5.5 verbatim "Initial=not_run" (research/04:63,74). Matches exactly. |
| 2 | Per-escape verdict enum EXACTLY {CATCH, MISS} | PASS | catch_rate.py:26-27 `VERDICT_CATCH="CATCH"`, `VERDICT_MISS="MISS"`. `EscapeResult.__post_init__` (catch_rate.py:84-89) raises ValueError on any verdict not in `(CATCH, MISS)`. Schema `escapeResult.verdict` enum (catch_rate.schema.json:101-108) = `["CATCH","MISS"]`. Exact, with both a runtime guard and schema guard. |
| 3 | `_derive_backtest_status`: all-5 CATCH+truthy negative_witness+non-null card_path → complete; replay-ran-but-unmet → partial (missing ids surfaced); no escapes → not_run | PASS | `is_fully_caught` (catch_rate.py:91-97) = `verdict==CATCH AND bool(negative_witness) AND card_path is not None` — the exact 3-conjunct anti-vacuity. `_derive_backtest_status` (catch_rate.py:103-114): empty→not_run (110-111); `all(is_fully_caught)`→complete (112-113); else→partial (114). Missing-id surfacing: `_missing_escape_ids` (117-119) + `CatchRateReport.missing_escape_ids()` (179-181) return ids where `not is_fully_caught()`. Partial path always has a non-empty missing set by construction (if it were empty, `all()` would be True → complete). Renderer lists them for partial (catch_rate_report.py:88-92). |
| 4 | `__post_init__` raises ValueError on mismatched status AND explicitly on 'complete'-claim with any card_path=None (card participates; not silent downgrade) | PASS | CatchRateReport.`__post_init__` invariant #3 (catch_rate.py:155-162): re-derives via `_derive_backtest_status(self.escapes)` and raises ValueError if `self.backtest_status != derived`. Invariant #4 (163-177): when `backtest_status==STATUS_COMPLETE`, loops escapes and raises ValueError explicitly on `e.card_path is None` (168-172) BEFORE the broader `not is_fully_caught()` raise (173-177). card_path is named in the raise message and is a hard failure — confirmed not a silent downgrade. |
| 5 | enum/derivation match spec §4.5/§5.4 exactly; a CATCH count alone must NOT earn complete | PASS | Spec §4.5 enum + default (research/04:63), §5.4 derivation table (research/04:84-86), §5.4 anti-vacuity tightening (research/04:90-93, 199 checklist item 3). Code's `complete` requires per-escape `negative_witness` + `card_path` beyond CATCH (catch_rate.py:91-97), so a bare CATCH count cannot reach complete — the `build_catch_rate_report` factory counts `caught` separately (catch_rate.py:221) but derives status via `_derive_backtest_status`, never from the count. Invariant #3 raise message (catch_rate.py:160-162) literally encodes "a CATCH count alone never earns 'complete'". Schema disclaims enforcing anti-vacuity itself and points to `__post_init__` (catch_rate.schema.json:5) — consistent, no contradiction. |

## Summary

- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Adversarial probes attempted (and why each failed to find a defect)

| Probe (hypothesized defect) | Result |
|---|---|
| Enum carries a 4th value / typo'd token | REFUTED — only 3 tokens in `BACKTEST_STATUS_VALUES` (catch_rate.py:33-37) and schema enum (catch_rate.schema.json:72-76); strings match byte-for-byte. |
| `partial` derivable with empty missing-id set (so ids never surfaced) | REFUTED — partial is only reached when `all(is_fully_caught)` is False (catch_rate.py:112-114), which guarantees >=1 non-caught escape, so `_missing_escape_ids` (117-119) is non-empty by construction. |
| `complete` reachable from CATCH count alone (vacuity hole) | REFUTED — status is derived from `is_fully_caught` 3-conjunct (catch_rate.py:91-97), not from `caught` (which is computed independently at factory line 221 and never feeds status). |
| `card_path=None` silently downgrades complete→partial instead of raising | REFUTED — `__post_init__` invariant #4 (catch_rate.py:165-172) raises ValueError naming card_path; it does not coerce. A producer hand-setting `complete` with a null card fails loudly (test_catch_rate_schema.py:233-251 asserts the raise). |
| Default is something other than not_run on the empty path | REFUTED — `_derive_backtest_status([])` returns `STATUS_NOT_RUN` (catch_rate.py:110-111); spec Initial=not_run (research/04:63). |
| `negative_witness` truthiness bypassable (e.g. only checks `is not None`) | REFUTED — `bool(self.negative_witness)` (catch_rate.py:95) enforces truthiness, not mere presence; field is typed `bool` (catch_rate.py:80). |
| Status re-derivation invariant (#3) absent, letting a misreporting producer pass | REFUTED — invariant #3 re-derives and compares (catch_rate.py:156-162); divergence raises. Confirms the load-bearing guard exists. |

## Issues Found

None.

## Actions Taken

None — report-only (fix_authorization: false). No source file modified.

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 2
- Tool-call count (7) >= checklist items (5): not suspect. Every Read/Bash mapped to a specific VERIFY
  item (catch_rate.py for items 1-5; schema for items 1,2,5; research/04 for the spec literals in 1,3,5;
  Bash grep for the no-duplicate-definition check + test-fixture corroboration of derivation behavior).
- Note: the spec (§4.5/§5.4) was consulted via the verbatim excerpts in research/04 (the file provided
  in scope), not the live RELEASE-SPEC. Items 1/3/5 cite research/04 line numbers for the spec literals.
  This is the source-of-truth the spawn prompt designated; flagged for transparency, does not reduce
  confidence on the code-vs-stated-spec match.

## Recommendations

- Green light. The enum and its anti-vacuity derivation match the stated §4.5/§5.4 contract exactly,
  with both a runtime re-derivation guard (invariant #3) and an explicit card_path-participates guard
  (invariant #4). No remediation required for this surface.

## QA Complete
