# Phase 4 QA — Consolidated Findings

**Consolidated verdict: FAIL** (2 of 6 lenses reported issues; FAIL if ANY agent reports ANY issue).

## Lens verdicts (6 lens agents)

| Lens | Agent | Report | Verdict |
|------|-------|--------|---------|
| Structural — §8.3 per-escape mapping | rf-qa | `qa-structural-escape-mapping-report.md` | PASS (1 advisory D1) |
| Structural — skip-guard correctness | rf-qa | `qa-structural-skip-guard-report.md` | PASS |
| Structural — aggregation + status wiring | rf-qa | `qa-structural-aggregation-report.md` | PASS-with-findings (2 IMPORTANT + 3 MINOR test-robustness) |
| Content — OLD=MISS negative witness | rf-qa-qualitative | `qa-content-negative-witness-report.md` | PASS (1 MINOR) |
| Content — collision boundary + nodeids | rf-qa-qualitative | `qa-content-collision-nodeid-report.md` | **FAIL** (1 MINOR) |
| Domain — E4 HEAD-drift + dual-evaluator | rf-qa-qualitative | `qa-domain-e4-headdrift-report.md` | PASS |

## Deduplicated issues

| # | Severity | File | Issue | Required fix / disposition | Lens |
|---|----------|------|-------|----------------------------|------|
| P4-1 | IMPORTANT | `test_catch_rate_aggregation.py` | The `complete`/`partial` else-branch is DEAD today (all impl refs absent → only the `not_run` arm runs). The aggregation's own derivation+missing-id wiring is never exercised by the suite. | Add a HERMETIC test in `test_catch_rate_aggregation.py` that builds a `CatchRateReport` from SYNTHETIC `EscapeResult`s (an all-CATCH+witness+card set → `complete`; a mixed set with one MISS / one null card → `partial` with the right missing ids), writes via `write_catch_rate_report` to `tmp_path`, and asserts `backtest_status`, `caught`/`missed`/`catch_rate`, the per-escape `catch-rate.md`, and `unresolved_card_paths`. This exercises the today-dead arm without touching impl refs. | aggregation |
| P4-2 | IMPORTANT | `test_catch_rate_aggregation.py` docs-guard | `"docs" not in str(written[...].parent)` is a vacuous substring check (a `/tmp/...` path trivially satisfies it). | Replace with an EXACT-equality assertion that the written parent is the `tmp_path` dir (e.g. `written["catch-rate.json"].parent == tmp_path`), so the guard actually proves the report is tmp_path-rooted. | aggregation |
| P4-3 | MINOR | `test_catch_rate_aggregation.py` non-empty branch | `caught`/`missed`/`catch_rate` are not asserted in the non-empty branch; `catch-rate.md` + `unresolved_card_paths` never exercised. | Covered by the P4-1 hermetic test (assert those there). | aggregation |
| P4-4 | MINOR (acknowledged, NO code change) | `tests/troubleshoot/__init__.py` (parent) | Lens flags the empty parent `__init__.py` as impl-owned per research §D.3. | **By-design / required — keep it.** Task Step 1.5 EXPLICITLY authorizes creating it ONLY-IF-ABSENT (it was absent); §D.1 L280-289 pre-authorizes it as a create-if-absent bootstrap; and it is REQUIRED for the `from tests.troubleshoot.backtest import ...` import chain (deleting it breaks collection — 31 tests currently pass with it present). It is a 0-byte file identical to what the impl's Step 7.1 will idempotently create. Disposition: document the rationale; do NOT delete. | collision-nodeid |
| P4-5 | ADVISORY (optional comment) | E1-E5 runners | §8.3 single-wave numbers (used by the runners) vs §3.1 Traceability Matrix multi-wave closure sets (E1=H1, E4=H1,H2). Runners correctly use §8.3. | Optional one-line clarifying comment that the wave is the §8.3 primary backtest wave; non-blocking, no behavior change. May be skipped. | escape-mapping |

## Fix routing

Substantive fixes are confined to `test_catch_rate_aggregation.py` (P4-1, P4-2, P4-3). P4-4 is a documented by-design disposition (NO code change — deletion would break the import chain and contradicts task Step 1.5). P4-5 is optional. Per I20, ONE serialized rf-qa fix agent applies P4-1/P4-2/P4-3, touching ONLY `tests/troubleshoot/backtest/`, and must keep the suite green-or-correctly-skips + ruff clean.
