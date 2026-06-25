# Phase 3 Inventory (L6)

ReplayExecutor seam + catch-rate report model + writer + JSON Schema + fidelity/separation tests +
fixtures. All under `tests/troubleshoot/backtest/`. No file exceeds 500 lines → no I21 per-file gate.

| File | Lines | Public symbols | >500? |
|------|-------|----------------|-------|
| `replay_executor.py` | 190 | `ReplayResult`, `ResolvedCallable`, `ReplayExecutor` (Protocol, runtime_checkable), `read_source_from_worktree`, `load_module_from_worktree`, `resolve_callable`, `InProcessReplayExecutor`, `VERDICT_{MISS,CATCH,ERROR}` | No |
| `catch_rate.py` | 235 | `EscapeResult` (frozen + `_ESCAPE_RESULT_FIELDS` + `to_dict`), `CatchRateReport` (frozen + `_CATCH_RATE_FIELDS` + `__post_init__` + `to_dict` + `missing_escape_ids` + `production_signoff`), `_derive_backtest_status`, `build_catch_rate_report`, `BACKTEST_STATUS_VALUES`, `STATUS_*`, `VERDICT_*` | No |
| `catch_rate_report.py` | 126 | `CatchRateContractViolation`, `CATCH_RATE_CONTRACT_VIOLATION_EXIT_CODE` (=2), `_check`, `render_catch_rate_json`, `render_catch_rate_markdown`, `write_catch_rate_report` | No |
| `schemas/catch_rate.schema.json` | 124 | draft-2020-12 schema; required[10]; `$defs.backtestStatus` enum, `$defs.escapeId` (own `^E[0-9]+$`), `$defs.escapeResult` (verdict enum CATCH/MISS) | No |
| `schemas/__init__.py` | 33 | `CATCH_RATE_SCHEMA_FILENAME`, `load_catch_rate_schema` (importlib.resources) | No |
| `test_catch_rate_schema.py` | 294 | 14 tests: schema well-formed, real-producer round-trip validate, required/enum/escapeId pins, post_init + contract-violation, derivation, anti-vacuity (missing witness / missing card / complete+null-card raises), proxy serialized, valid/invalid fixtures, tmp_path-only writer | No |
| `test_backtest_status_separation.py` | 70 | 3 tests: not_run→advisory, partial→missing ids+advisory, complete→may mirror verdict (via `production_signoff`) | No |

Fixtures (`fixtures/catch_rate/`): `valid_minimal.json`, `valid_full.json`, `invalid_bad_status.json`, `invalid_bad_verdict.json`, `all_catch_missing_witness.json`.

## Key invariants embedded

- **ReplayExecutor** is a `typing.Protocol` (runtime_checkable) `replay(escape, worktree) -> ReplayResult`, mirroring `LifecycleExecutor` (runner.py:136-156); no PTY/pexpect; signature-adaptive (`resolve_callable` reads the real signature — no hardcoded shape).
- **backtest_status** derivation ANTI-VACUITY-TIGHTENED: complete ⟺ all 5 escapes CATCH AND negative_witness AND non-null card_path; else partial (+missing ids); empty → not_run. `__post_init__` raises on mismatch + on complete-claim with null card_path.
- **Writer triad**: `_check` invariant before any serialization; `to_dict()` single SoT; `CatchRateContractViolation` → exit 2.
- **Schema**: own `escapeId` `^E[0-9]+$` (NOT reused from summary.schema.json which has none); required = 10 fields incl `proxy_limitation`; enums backtestStatus={not_run,partial,complete}, verdict={CATCH,MISS}.
- **Separation**: `production_signoff(run_verdict)` returns advisory unless status==complete.

## Local run evidence (pre-QA)

- `uv run pytest tests/troubleshoot/backtest/` → 23 passed.
- `ruff check` clean; `ruff format --check` clean (10 files already formatted).
