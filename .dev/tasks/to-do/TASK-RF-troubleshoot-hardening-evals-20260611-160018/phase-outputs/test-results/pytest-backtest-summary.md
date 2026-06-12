# pytest Backtest Suite Summary (L3)

**Command:** `uv run pytest tests/troubleshoot/backtest/ -v`
**Result: GREEN** — 0 failed AND 0 errored (skips are EXPECTED and acceptable). Exit code 0.

> **Phase 5 update:** the no-leak test (`test_backtest_replay_leaves_no_leaked_worktree`) is now
> **concurrency-robust** — it passes a known `scratch_root` (`tmp_path`) to `checkout_worktree` and
> asserts ONLY about worktrees under that root (scoped assertion), replacing the fragile global
> `after == baseline` porcelain byte-compare that another process's in-flight `git worktree add`
> could false-trip. Verified deterministic: 8/8 serial reruns of the integration module green. The
> integration tests SKIP on CI (`actions/checkout@v4` shallow `fetch-depth: 1` — the pre-fix parents
> are absent). Counts rose +6 vs the prior run: the no-leak test was rewritten in place (still 1
> test) and a new `test_replay_executor.py` added 6 unit tests exercising the previously-orphaned
> `ReplayExecutor` seam.

## Counts

| Outcome | Count |
|---------|-------|
| passed  | 38 |
| skipped | 11 |
| failed  | 0 |
| errored | 0 |

## Failed/errored tests

None.

## Skip attribution (all 11 skips are designed, NOT broken collection)

| Skipped test(s) | Count | Reason |
|-----------------|-------|--------|
| `test_backtest_e{1..5}_new_gate_catches_via_*` (NEW=CATCH proxies) | 5 | `requires_impl_ref(<ref>)` — the hardening impl refs have not landed yet (impl branch `feat/troubleshoot-pipeline-hardening`). Un-skip automatically once the refs exist. |
| `test_waiver_latch_one_way_blocks_downstream_regreen` | 1 | `requires_impl_ref("hardening-output-contract.md")` — single guarded test, no OLD=MISS half by design; excluded from catch_rate (backs NFR-4). |
| `test_backtest_escape_collected_into_catch_rate[E1..E5]` (aggregation parametrize) | 5 | No NEW=CATCH impl refs present → catch-rate is `not_run`; the parametrize skips and the OLD=MISS witnesses are asserted in `test_backtest_e1..e5.py`. |

The OLD=MISS unit-level/real-git replays (E1-E5) RAN and PASSED on this full-history local clone; the
`test_git_replay_integration.py` real-git tests RAN and PASSED; the report model/schema/aggregation
hermetic tests RAN and PASSED; the new `test_replay_executor.py` (6 fast stub/inspection unit tests
exercising the `ReplayExecutor` seam) RAN and PASSED. NONE of the skips are due to a collection error
or an accidentally skipped OLD=MISS assertion.

## CI note

On CI (`actions/checkout@v4` default shallow `fetch-depth: 1`), the OLD=MISS real-git replays + the
integration tests additionally SKIP (the 5 pre-fix parent commits are absent), via the module-level
`pytest.mark.skipif` on `missing_replay_commits([...])`. The report-model/schema/aggregation (synthetic)
+ git_replay unit (subprocess-mocked) tests run green unconditionally on CI.

## backtest_status emitted today

`not_run` (expected) — the NEW impl refs are not yet landed, so no NEW=CATCH proxy contributes a catch
proof and the catch-rate aggregation derives `not_run`.
