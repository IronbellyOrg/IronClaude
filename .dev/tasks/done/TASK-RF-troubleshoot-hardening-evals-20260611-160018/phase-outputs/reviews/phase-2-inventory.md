# Phase 2 Inventory (L6)

Consolidated inventory of Phase 2 deliverables (git-replay helper + unit + integration tests).
All files live under `tests/troubleshoot/backtest/`. No file exceeds 500 lines → no I21 per-file
source-fidelity gate triggered for any Phase 2 file.

| File | Lines | Public symbols | >500? |
|------|-------|----------------|-------|
| `tests/troubleshoot/backtest/git_replay.py` | 126 | `ReplayEscape` (NamedTuple), `REPLAY_ESCAPES` (5-tuple), `escape_by_id`, `worktree_list_porcelain`, `checkout_worktree` (contextmanager) | No |
| `tests/troubleshoot/backtest/test_git_replay_unit.py` | 81 | `test_backtest_checkout_worktree_issues_detached_add_with_commitish_unchanged`, `test_backtest_checkout_worktree_teardown_fires_even_when_body_raises`, `test_backtest_replay_escapes_has_exactly_five_bare_parent_shas`, `test_backtest_escape_by_id_round_trips_and_rejects_unknown` | No |
| `tests/troubleshoot/backtest/test_git_replay_integration.py` | 106 | module-level `pytestmark` skipif (predicates `_not_a_git_worktree`, `_missing_replay_shas`), `test_backtest_real_worktree_checkout_lands_on_prefix_parent`, `test_backtest_replay_leaves_no_leaked_worktree` | No |

## Key invariants embedded

- **REPLAY_ESCAPES** (bare parent shas, no caret): E1=`94d5baa0`/H1, E2=`10723863`/H3, E3=`e97aa4fd`/H3, E4=`1b0264f1`/H2, E5=`d878bc6d`/H4. fix_sha kept as provenance only.
- **Subprocess seam:** module-top `import subprocess as _subprocess` (patchable at `tests.troubleshoot.backtest.git_replay._subprocess.run`), mirroring `cli/sprint/process.py:17`.
- **Teardown (G3):** `checkout_worktree` finally block = `remove --force` (check=False) + `shutil.rmtree(base, ignore_errors=True)` + `prune` (check=False).
- **G2 skip-guard:** module-level skipif probes `git cat-file -e <sha>^{commit}` per escape + `git rev-parse --is-inside-work-tree` first; self-clearing reason names missing shas + `fetch-depth: 0` un-skip trigger.

## Local run evidence (pre-QA)

- `test_git_replay_unit.py` → 4 passed (0.02s).
- `test_git_replay_integration.py` → 2 passed (2.56s) on the local full-history clone.
