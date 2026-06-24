# QA Report — Structural Aggregation (catch-rate roll-up)

**Topic:** catch_rate aggregation (E1-E5 -> CatchRateReport -> backtest_status)
**Date:** 2026-06-12
**Phase:** report-validation (structural verification, adversarial)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: PASS (with documented coverage limitations)

The five required behaviors (VERIFY 1-5) are all correctly implemented in the
**source model** (`catch_rate.py`) and **wired** in the test
(`test_catch_rate_aggregation.py`). I independently exercised the
`complete` / `partial` / anti-vacuity branches that today's `not_run` repo state
does NOT execute, and the model derives correctly in every case. No correctness
defect found that would flip a verdict.

However, the adversarial mandate ("assume >=5 errors") did surface real
**coverage/robustness weaknesses** in the *test* (not the model). None rise to a
correctness FAIL, but they are logged below as IMPORTANT/MINOR because they mean
the green test is weaker evidence than it appears. I am calling the structural
contract PASS and the test-coverage posture DEGRADED.

---

## VERIFY Checklist (1-5)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | parametrize covers exactly E1-E5, ids E1..E5, sourced from REPLAY_ESCAPES | PASS | `test_catch_rate_aggregation.py:93-95` parametrizes `REPLAY_ESCAPES` with `ids=[e.escape_id for e in REPLAY_ESCAPES]`; `git_replay.py:48-56` defines exactly E1,E2,E3,E4,E5. Pytest collected exactly `[E1][E2][E3][E4][E5]`. |
| 2 | 5 EscapeResults feed a single CatchRateReport | PASS | `test:112-119` `results = tuple(_collect_escape_results())` -> single `build_catch_rate_report(... escapes=results ...)`. `_collect_escape_results` (`test:66-90`) loops all of `REPLAY_ESCAPES`, appending one record each. |
| 3 | report written to tmp_path, NEVER docs/ | PASS (guard is weak — see I-1) | `test:120` `write_catch_rate_report(report, tmp_path)`; `test:121-123` asserts `"docs" not in str(...parent)`. Writer (`catch_rate_report.py:133-169`) writes under `output_dir` only. tmp root is `/tmp` (no "docs"). |
| 4 | backtest_status: complete only when all-5 CATCH+witness+card / partial / not_run; not_run not a failure | PASS | Model `_derive_backtest_status` (`catch_rate.py:119-130`): empty->`not_run`, `all(is_fully_caught)`->`complete`, else `partial`. `is_fully_caught` (`catch_rate.py:107-113`) = CATCH AND witness AND card_path!=None. not_run asserted non-failing at `test:126-130` (`total_escapes==0`, `caught==0`). Live run: 1 passed, 5 skipped — not_run is green, not red. |
| 5 | denominator == five E1-E5 (waiver excluded; ==5 non-empty, ==0 not_run); no vacuous `complete` over a subset | PASS | `_collect_escape_results` (`test:60-90`): builds `present` over ALL `REPLAY_ESCAPES`; `if not any(present.values()): return []`; otherwise loops ALL 5 (present->CATCH+card, absent->MISS+None). So a partial landing yields 5 records with >=1 MISS -> `_derive_backtest_status` returns `partial`, never `complete`. Independently probed (Probe A): 3-CATCH/2-MISS -> `partial`, total=5, caught=3, missing=(E4,E5). Waiver scenario is in a separate file and never imported here (`test:16-17` docstring + no `test_waiver` import). |

**Anti-vacuity independent probes (branches NOT run by today's repo state):**

- Probe A (3 CATCH + 2 MISS): -> `partial`, `total_escapes=5`, `caught=3`, `missing=(E4,E5)`. Correct.
- Probe B (all 5 CATCH+witness+card): -> `complete`, `caught=5`. Correct.
- Probe C (all 5 CATCH+witness but `card_path=None`): -> `partial`, `caught=5`, `missing=(E1..E5)`. **This is the key anti-vacuity case** — a full CATCH *count* with null cards does NOT earn `complete`. Correct (`catch_rate.py:128` + `__post_init__:189-201` would also reject a mis-claimed `complete`).

---

## Summary

- VERIFY checks passed: 5 / 5
- Correctness FAILs: 0
- Issues found (test coverage/robustness, non-blocking): 5 (IMPORTANT: 2, MINOR: 3)
- Issues fixed in-place: 0 (report-only)

---

## Issues Found (adversarial — none flip a VERIFY verdict, all are test-side)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| I-1 | IMPORTANT | `test_catch_rate_aggregation.py:121-123` | The docs-guard is a **substring** check `"docs" not in str(parent)`. It is satisfied vacuously by `tmp_path` (always `/tmp/...`), so it never actually exercises a docs-rejection path. It would also *miss* a legitimately bad dir like `/tmp/redocs/` only by accident, and gives false confidence that "report can't land in docs/" is enforced *here*. The real docs-write protection is the root `_pollution_snapshot` autouse guard (per `catch_rate_report.py:144-146` comment), not this assertion. | Either assert `written["catch-rate.json"].parent == tmp_path` (exact, positive) or drop the misleading substring check and rely on the documented autouse pollution guard. Substring `"docs"` matching is brittle. |
| I-2 | IMPORTANT | `test_catch_rate_aggregation.py:131-153` (else branch) | The entire non-empty branch (`complete`/`partial` assertions, `total_escapes==5`, missing-id surfacing) is **dead today** and will stay dead until impl refs land. All 4 escape refs are absent on disk (verified: `runtime-entrypoint-verification.md`, `unmask-and-sweep.md`, `contract-enumeration.md`, `effective-input-proof.md` all ABSENT). So the green run only ever proves the `not_run` arm. The `complete`/`partial` arithmetic is unproven by THIS test (I proved it out-of-band via Probes A/B/C, but the committed suite does not). | Add a hermetic test that injects synthetic `EscapeResult`s (not dependent on on-disk refs) to assert the `complete` and `partial` arms — exactly the Probe A/B/C cases — so the load-bearing arms are covered regardless of ref landing. |
| I-3 | MINOR | `test_catch_rate_aggregation.py:131-141` | The non-empty (`else`) branch asserts `total_escapes==5` and `backtest_status` but **never asserts `caught`/`missed`/`catch_rate`**. The `not_run` branch asserts `caught==0` (`:130`) but no branch asserts `catch_rate` at all (grep: `catch_rate` appears only in imports/docstring, never in an assert). A desync between `caught` and the CATCH count would pass this test (it is only caught by the model's own `__post_init__:168` balance guard, which the test does not independently re-verify on payload). | Assert `payload["caught"]`, `payload["missed"]`, and `payload["catch_rate"]` in the non-empty branch against the expected CATCH count. |
| I-4 | MINOR | `test_catch_rate_aggregation.py:120` | The writer emits BOTH `catch-rate.json` AND `catch-rate.md` (default `emit_md=True`, `catch_rate_report.py:164-167`), but the test only reads/asserts the JSON. The markdown renderer (`render_catch_rate_markdown`) — including its partial-missing-id line and proxy-limitation note — is never asserted. A regression in the MD wire text (e.g. dropping the proxy caveat) would not be caught here. | Assert the returned mapping contains `catch-rate.md` and spot-check the proxy-limitation line and (in partial) the missing-id line. |
| I-5 | MINOR | `test_catch_rate_aggregation.py` (whole file) | The real on-disk existence gate `unresolved_card_paths` (`catch_rate.py:262-284`) — the function that distinguishes a producer-asserted non-null `card_path` from an actually-landed ref — is **never invoked** in this aggregation test. So "card_path is non-null" is tested, but "card_path resolves to a real file" is not exercised at the aggregation layer. This is by-design per the docstring (existence enforced upstream), but it means the aggregation test cannot detect a `complete` backed by phantom (non-existent) card paths. | Optionally add an assertion in the non-empty branch that `unresolved_card_paths(report, base_dir=...) == ()` to close the producer-asserted-vs-landed gap at this layer. |

---

## Items Re-verified (false-positive sweep — claimed errors that are NOT errors)

To honor the adversarial mandate without manufacturing findings, I explicitly cleared these candidate "errors":

- **Subset-derives-complete (the CRITICAL check in VERIFY-5):** NOT an error. `_collect_escape_results` collects ALL 5 whenever `any(present)` is true; a partial landing therefore carries MISS records and derives `partial`. Confirmed by Probe A.
- **CATCH-count earns complete:** NOT an error. Probe C shows 5×CATCH with null cards -> `partial`. Anti-vacuity holds in both the derivation (`catch_rate.py:128`) and the `__post_init__` guard (`:189-201`).
- **Waiver scenario contaminating the denominator:** NOT an error. Waiver lives in `test_waiver_regreen.py`, is never imported, and `total_escapes` is `len(escapes)` over E1-E5 only.
- **wave mismatch:** NOT an error. `test:107` asserts `rec.wave == escape.wave`; waves pinned in `git_replay.py:49-55` (E1=H1, E2=H3, E3=H3, E4=H2, E5=H4).
- **not_run treated as failure:** NOT an error. Live run shows `1 passed, 5 skipped` — the parametrized arm `pytest.skip`s (`test:100-103`) and the report arm asserts `not_run` is the *expected* status, not a failure.

---

## Confidence Gate

- **Confidence:** Verified: 5/5 VERIFY items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (for the 5 VERIFY contract checks; coverage-completeness of the test is separately rated DEGRADED via I-2)
- **Tool engagement:** Read: 5 | Grep: 6 | Glob: 0 | Bash: 6
- Tool calls (17) >= checklist items — not suspect on the engagement-minimum heuristic.
- Note: VERIFY items 4 & 5's `complete`/`partial` arms are NOT exercised by the committed test (impl refs absent); I marked them VERIFIED on the basis of independent out-of-band Probes A/B/C against the live model, NOT on the basis of the test asserting them. This reliance is documented as I-2.

## Actions Taken

None (report-only, fix_authorization: false).

## Recommendations

1. Resolve I-1 and I-2 before relying on this suite as the catch-rate regression gate — today it only proves the `not_run` arm.
2. I-3/I-4/I-5 are quality hardening; address opportunistically.
3. No source-model change required — `catch_rate.py` / `catch_rate_report.py` are correct as written.

## QA Complete
