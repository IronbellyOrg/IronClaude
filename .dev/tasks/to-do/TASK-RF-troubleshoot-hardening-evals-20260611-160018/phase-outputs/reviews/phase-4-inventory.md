# Phase 4 Inventory (L6)

Per-escape differential runners (E1-E5) + waiver meta-scenario + skip-guard + path guard +
aggregation. All under `tests/troubleshoot/backtest/`. No file exceeds 500 lines → no I21 gate.

| File | Lines | OLD=MISS test | NEW=CATCH proxy test (+ ref gated on) | escape / wave / parent sha |
|------|-------|---------------|----------------------------------------|-----------------------------|
| `_impl_guard.py` | 57 | — | `requires_hardening_impl` + `requires_impl_ref(ref)`; `REPO_ROOT=parents[3]`; `HARDENING_REFS` | — (skip-guard infra) |
| `test_path_resolution.py` | 19 | `test_backtest_repo_root_resolves_to_pyproject` (parents[3] sanity) | — | — |
| `test_backtest_e1.py` | 90 | `test_backtest_e1_old_protocol_misses_local_path_file` | `test_backtest_e1_new_gate_catches_via_h1_ref` → `runtime-entrypoint-verification.md` | E1 / H1 / `94d5baa0` |
| `test_backtest_e2.py` | 100 | `test_backtest_e2_old_protocol_misses_final_phase_false_positive` | `test_backtest_e2_new_gate_catches_via_unmask_and_sweep_ref` → `unmask-and-sweep.md` | E2 / H3 / `10723863` |
| `test_backtest_e3.py` | 113 | `test_backtest_e3_old_protocol_misses_advisory_severity` | `test_backtest_e3_new_gate_catches_via_unmask_and_sweep_ref` → `unmask-and-sweep.md` | E3 / H3 / `e97aa4fd` |
| `test_backtest_e4.py` | 104 | `test_backtest_e4_old_protocol_misses_second_consumer` | `test_backtest_e4_new_gate_catches_via_contract_enumeration_ref` → `contract-enumeration.md` | E4 / H2 / `1b0264f1` (NOT HEAD) |
| `test_backtest_e5.py` | 77 | `test_backtest_e5_old_protocol_misses_wrong_diff_surface` | `test_backtest_e5_new_gate_catches_via_effective_input_ref` → `effective-input-proof.md` | E5 / H4 / `d878bc6d` |
| `test_waiver_regreen.py` | 50 | **none by design** (forward verdict-state invariant; EXCLUDED from catch_rate) | `test_waiver_latch_one_way_blocks_downstream_regreen` → `hardening-output-contract.md` | FR-12/NFR-4 (not an E1-E5 escape) |
| `test_catch_rate_aggregation.py` | 153 | parametrize over E1-E5 → `test_backtest_escape_collected_into_catch_rate` + `test_backtest_catch_rate_report_drives_status` | — | E1-E5 (denominator 5; waiver excluded) |

## OLD=MISS replay mechanism (uniform across E1-E4)

`replay_executor.run_prefix_replay_snippet(parent_sha, snippet)` checks out the bare parent sha (no caret, G1) into a throwaway worktree and runs the snippet in a FRESH subprocess whose `sys.path[0]` is the worktree's `src/` (a prelude purges inherited `superclaude` modules), so pre-fix code loads from the PARENT tree, not the live editable install. The snippet reads the target's REAL signature via `inspect` and invokes it adaptively (E1/E4 class-bound via SimpleNamespace self / unwrapped staticmethod; E2/E3 module-level). E5 is a SOURCE-TEXT assertion (`read_source_from_worktree`) on the pre-fix SKILL.md. Each OLD=MISS verified green locally; each NEW=CATCH skips (refs absent).

## Skip-guard discipline

- NEW=CATCH: `requires_impl_ref(<specific ref>)` (`pytest.mark.skipif` on ref-file existence). NO `importorskip`, NO `xfail`.
- OLD=MISS: module-level `pytest.mark.skipif` on `(not is_git_worktree()) or missing_replay_commits([parent])` (CI shallow-clone guard, `git cat-file -e <sha>^{commit}`). No impl-ref dependency.
- `REPO_ROOT` = `parents[3]` (pinned by `test_path_resolution.py`).
- Distinct `test_backtest_*` / `test_waiver_*` function names (no nodeid collision with impl `test_hardening_*`).

## Local run evidence (pre-QA)

`uv run pytest tests/troubleshoot/backtest/` → 31 passed, 11 skipped (5 NEW=CATCH proxies + waiver + 5 aggregation parametrize skip; OLD=MISS + integration ran). ruff check + format clean.
