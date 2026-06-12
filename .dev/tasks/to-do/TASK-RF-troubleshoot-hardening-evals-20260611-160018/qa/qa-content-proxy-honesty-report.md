# QA Report — Content / Proxy-Honesty Review (NEW=CATCH proxy)

**Topic:** sc:troubleshoot pipeline-hardening backtest — catch-rate report proxy honesty
**Date:** 2026-06-12
**Phase:** doc-qualitative (adversarial content audit, report-only)
**Fix cycle:** N/A
**Fix authorization:** false (modified NO source file)

---

## Overall Verdict: FAIL

Three oversells of the NEW=CATCH proxy were found (the adversarial floor of 3 is met).
VERIFY items 1 and 2 pass; items 3 and 4 are **oversold** by the harness framing and by
shipped wire text that the code does not back. Per the rubric (any issue = FAIL) → FAIL.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Proxy note explicitly records documentation-presence PROXY (not executed gate) | PASS | `catch_rate_report.py:25-28` `_PROXY_NOTE`; `catch_rate.py:1-7` + `:127-128`; markdown emit `catch_rate_report.py:95` |
| 2 | `proxy_limitation` SERIALIZED + REQUIRED in schema (can't be dropped) | PASS (key-presence only) | field in `_CATCH_RATE_FIELDS` `catch_rate.py:58`; `to_dict` walk `:198-203`; schema `required` `catch_rate.schema.json:17`; pin `test_catch_rate_schema.py:109` |
| 3 | `complete` only reachable once impl refs land (card_path conjunct enforces) | FAIL | conjunct checks `card_path is not None` only — NO `.exists()` `catch_rate.py:91-97`; `valid_full.json:11-15` reaches `complete` on relative strings never resolved |
| 4 | Report does not claim measured catch-coverage while proxy is the only evidence | FAIL | `catch_rate`/`caught` serialized as bare numerics `catch_rate.py:48-59,195-204`; headline `catch_rate_report.py:78`; `valid_full.json:8` ships `catch_rate:1.0` |

## Summary
- Checks passed: 2 / 4 (item 2 passes only at key-presence granularity)
- Checks failed: 2 (items 3, 4)
- Oversells found: 3 primary + 1 supporting (adversarial floor of 3 met)
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| OVERSELL-1 | CRITICAL | `catch_rate.py:91-97`, `:163-177`; `catch_rate_report.py:28` | `card_path` conjunct enforces **non-null**, NOT **impl-ref-landed**. `is_fully_caught()` accepts any non-null string; there is NO `Path(card_path).exists()` check. `valid_full.json:11-15` reaches `complete` with relative ref strings that are never resolved/stat-ed. The research file's own xfail design keys collection on `(HARDENING_REFS/"pipeline-hardening-closure.md").exists()` (`06-impl-tasklist-crossref.md:175-196`) — that `skipif` is **absent from catch_rate.py/catch_rate_report.py**. The shipped wire text `catch_rate_report.py:28` ("`complete` is only legitimately reachable once the hardening impl refs land") overclaims what the code enforces. | Add an existence/resolution check so a `complete`-bound escape's `card_path` must resolve to a real impl ref on disk (gate `is_fully_caught()` on `(REPO_ROOT/card_path).exists()` or carry the `skipif`-style `_IMPL_LANDED` guard from research §C into the model), OR weaken the docstring/`_PROXY_NOTE` to say "non-null card asserted by the producer" rather than "impl refs land". |
| OVERSELL-2 | IMPORTANT | `catch_rate.py:140`; `catch_rate.schema.json:64-67`; `catch_rate_report.py:95` | `proxy_limitation` is REQUIRED-present but NOT required-honest. Default `""` (`catch_rate.py:140`); schema has **no `minLength`** (`:64-67`) — unlike `run_id`/`contract_version` which carry `minLength:1` (`:23,:33`). A producer can ship a `complete` report whose JSON `proxy_limitation` is empty. The "cannot be dropped / oversold" guarantee (`catch_rate.py:128`, schema `:66`) holds for the KEY only; the Markdown `or _PROXY_NOTE` fallback (`catch_rate_report.py:95`) does NOT apply to the JSON SoT that consumers read. | Add `"minLength": 1` to `proxy_limitation` in the schema AND a `__post_init__` guard rejecting an empty `proxy_limitation` (or default it to `_PROXY_NOTE` in `build_catch_rate_report`), so the JSON artifact cannot ship an empty caveat. |
| OVERSELL-3 | IMPORTANT | `catch_rate.py:48-59,195-204`; `catch_rate.schema.json:57`; `catch_rate_report.py:78`; `valid_full.json:8` | Measured-coverage numerics ARE emitted alongside the proxy with no proxy-qualification in the JSON. `to_dict()` always serializes `caught`/`missed`/`catch_rate`; `catch_rate` is documented as "caught/total_escapes" (a quantitative coverage ratio, schema `:57`). `valid_full.json:8` ships `catch_rate:1.0`. Nothing in schema/model BINDS `catch_rate`'s interpretation to `proxy_limitation`; a consumer reading `catch_rate:1.0` without parsing the prose reads it as measured coverage. The Markdown headline `## Catch rate: {caught}/{total} ({status})` (`:78`) foregrounds the number; the caveat is a trailing blockquote (`:95`) a skimmer misses. Contradicts item 4's "does not claim measured catch-coverage while proxy is the only evidence". | Either rename/qualify the field in the artifact (e.g. `proxy_catch_rate` or co-locate a `coverage_basis: "documentation-presence-proxy"` field), or have the Markdown header carry the proxy qualifier inline rather than only in the trailing blockquote, so the headline number is not read as executed-gate coverage. |
| OVERSELL-4 | MINOR (supporting) | `catch_rate.py:84-89,91-97` | The `verdict==CATCH` conjunct is also caller-supplied, validated only against the `{CATCH,MISS}` enum — nothing derives CATCH from an executed gate. Combined with OVERSELL-1, all three `is_fully_caught()` conjuncts (CATCH, witness, card) are caller-asserted. The model is an honest bookkeeping contract; the harness framing that it gates `complete` on real impl *evidence* is the oversell. | Document explicitly that all three conjuncts are producer-asserted claims, not executed-gate observations, so the contract is not read as measured evidence. |

## What genuinely holds (not oversold)
- The anti-vacuity *bookkeeping* is real and well-guarded: a CATCH count alone never earns `complete`
  (`catch_rate.py:103-114`); `__post_init__` re-derives `backtest_status` and raises on mismatch
  (`:155-162`); a `complete`-claimed escape with null `card_path` raises rather than silently
  downgrading (`:163-177`); the separation invariant keeps signoff `advisory` until `complete`
  (`:183-193`, asserted in `test_backtest_status_separation.py:27-71`). These back items 1 and the
  key-presence half of item 2 cleanly.
- The defects are about the proxy being **oversold as impl-landed / measured evidence**, NOT about
  the count/status accounting being wrong.

## Self-Audit
1. **Factual claims independently verified against source:** 11 — proxy note text (`catch_rate_report.py:25-28`); field tuple membership (`catch_rate.py:58`); `to_dict` walk (`:198-203`); schema `required` array (`catch_rate.schema.json:7-18`); schema pin test (`test_catch_rate_schema.py:99-110`); `is_fully_caught` conjuncts (`catch_rate.py:91-97`); absence of `.exists()` in model/writer (full read of both files); `proxy_limitation` default `""` (`:140`); schema lack of `minLength` on `proxy_limitation` vs presence on `run_id`/`contract_version` (`:23,:33,:64-67`); `valid_full.json` complete-with-relative-paths (`:8,:11-17`); Markdown header vs blockquote placement (`catch_rate_report.py:78,95`).
2. **Files read in full:** `catch_rate.py`, `catch_rate_report.py`, `catch_rate.schema.json`, `test_catch_rate_schema.py`, `test_backtest_status_separation.py`, `fixtures/catch_rate/valid_full.json`, research `06-impl-tasklist-crossref.md`; directory listing of `tests/troubleshoot/backtest/`.
3. **Why trust this found real issues:** I did not stop at the passing surface (items 1/2 pass). I traced the *enforcement chain* of `complete` to its primitives and found two conjuncts (`card_path is not None`, `verdict==CATCH`) are caller-supplied strings with no disk/gate backing, and cross-checked against the research file's own `.exists()`-keyed guard design (`06-impl-tasklist-crossref.md:188`) which the model omits. I compared `proxy_limitation`'s schema constraints against sibling required string fields and found the missing `minLength`. These are grep/read-verified, not impressions.
4. **Web research:** none performed; all verification was local-file-bound. Tavily-first N/A.

## Confidence
Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 6 | Grep: 1 | Glob: 0 | Bash: 1

## Recommendations
- Treat OVERSELL-1 as the load-bearing fix: either enforce `card_path` resolution on disk for
  `complete`, or strip the "impl refs land" claim from `_PROXY_NOTE`/docstrings so wire text matches
  code.
- Add `minLength:1` + a `__post_init__` non-empty guard on `proxy_limitation` (OVERSELL-2).
- Qualify or rename the `catch_rate`/`caught` numerics in the artifact, or inline the proxy caveat in
  the Markdown headline (OVERSELL-3).

## QA Complete
