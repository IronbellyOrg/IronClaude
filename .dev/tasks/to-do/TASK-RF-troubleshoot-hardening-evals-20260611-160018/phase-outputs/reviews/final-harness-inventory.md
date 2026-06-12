# Final Harness Inventory (Phase 6 — for final QA agents)

Complete file listing of `tests/troubleshoot/backtest/`. **Total: 2869 lines** (= modules + tests 2795
+ the 5 fixtures 74; verified `find … -exec cat {} + | wc -l` = 2869). No single file exceeds
500 lines (max = `test_catch_rate_schema.py` at 337) → no I21 per-file source-fidelity trigger.

## Modules (library)

| File | Lines | Role |
|------|-------|------|
| `__init__.py` | 1 | package marker (docstring) |
| `git_replay.py` | 240 | `ReplayEscape` (NamedTuple), `REPLAY_ESCAPES` (5 bare parent shas, no caret), `checkout_worktree` (try/finally remove+unlock+rmtree+prune), `worktree_list_porcelain`, `escape_by_id`, `is_git_worktree`, `missing_replay_commits`, `_repo_anchor` |
| `replay_executor.py` | 248 | `ReplayExecutor` Protocol + `InProcessReplayExecutor` + `ReplayResult`/`ResolvedCallable` + `resolve_callable`/`load_module_from_worktree`/`read_source_from_worktree` + `run_prefix_replay_snippet` (sys.path→worktree-src subprocess replay) + `PrefixReplayError` |
| `catch_rate.py` | 284 | `EscapeResult` + `CatchRateReport` (frozen, field tuples, anti-vacuity `__post_init__`, `production_signoff`, `missing_escape_ids`), `_derive_backtest_status`, `build_catch_rate_report`, `unresolved_card_paths` |
| `catch_rate_report.py` | 169 | writer triad: `_check` (guard before write), `render_catch_rate_json`/`render_catch_rate_markdown`, `write_catch_rate_report`, `CatchRateContractViolation` (exit 2) |
| `_impl_guard.py` | 57 | `REPO_ROOT=parents[3]`, `HARDENING_REFS`, `requires_hardening_impl`, `requires_impl_ref(ref)` (skipif on ref existence) |
| `conftest.py` | 50 | `replay_scratch_root` + `catch_rate_output_dir` fixtures (tmp-rooted, never docs/) |
| `schemas/catch_rate.schema.json` | 125 | draft-2020-12 schema; required[10]; `backtestStatus` enum, own `escapeId` `^E[0-9]+$`, `escapeResult` (verdict CATCH/MISS), `proxy_limitation` minLength 1 |
| `schemas/__init__.py` | 33 | `load_catch_rate_schema` (importlib.resources) |

## Tests

| File | Lines | Role |
|------|-------|------|
| `test_git_replay_unit.py` | 87 | subprocess-mocked: detached-add argv, teardown-on-raise, 5 bare shas no-caret, escape_by_id |
| `test_git_replay_integration.py` | 140 | real-git: checkout lands on parent; SCOPED no-leak (concurrency-robust); module-level CI skip-guard |
| `test_replay_executor.py` | 125 | seam: InProcessReplayExecutor stub/missing/raising → ReplayResult/ERROR; resolve_callable module+class; Protocol |
| `test_catch_rate_schema.py` | 337 | Draft202012Validator round-trip on REAL producer output; required/enum/escapeId pins; post_init + contract-violation; anti-vacuity (missing witness/card; complete+null-card raises); proxy serialized; valid/invalid fixtures; tmp_path-only writer; unresolved_card_paths |
| `test_backtest_status_separation.py` | 70 | not_run/partial→advisory; complete may mirror (production_signoff) |
| `test_path_resolution.py` | 19 | parents[3] → pyproject sanity |
| `test_backtest_e1.py` | 90 | E1/H1/`94d5baa0`: OLD=MISS local-path `--file`; NEW=CATCH `runtime-entrypoint-verification.md` |
| `test_backtest_e2.py` | 100 | E2/H3/`10723863`: OLD=MISS final-phase false-positive HALT (digit-heading fixture); NEW=CATCH `unmask-and-sweep.md` (word-boundary facet) |
| `test_backtest_e3.py` | 113 | E3/H3/`e97aa4fd`: OLD=MISS hard-HALT (advisory ignored); NEW=CATCH `unmask-and-sweep.md` (sweep facet) |
| `test_backtest_e4.py` | 104 | E4/H2/`1b0264f1` (NOT HEAD): OLD=MISS `_evaluate_gate` halts despite advisory; NEW=CATCH `contract-enumeration.md` |
| `test_backtest_e5.py` | 77 | E5/H4/`d878bc6d`: OLD=MISS `<BASE>..HEAD` wrong-surface; NEW=CATCH `effective-input-proof.md` |
| `test_waiver_regreen.py` | 50 | FR-12/NFR-4 single guarded test (no OLD half; excluded from catch_rate) |
| `test_catch_rate_aggregation.py` | 276 | parametrize E1-E5 → CatchRateReport → backtest_status (not_run today); hermetic complete/partial test |

## Fixtures (`fixtures/catch_rate/`)

`valid_minimal.json` (12), `valid_full.json` (18), `invalid_bad_status.json` (12), `invalid_bad_verdict.json` (14), `all_catch_missing_witness.json` (18).

## Suite state

`uv run pytest tests/troubleshoot/backtest/` → 38 passed, 11 skipped, 0 failed/errored. ruff check + format --check clean. Deterministic (8/8 serial reruns of the integration module).
