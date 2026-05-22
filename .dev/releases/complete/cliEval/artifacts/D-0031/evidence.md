# D-0031 — Evidence

**Task**: T02.10
**Deliverable**: `tests/cli/eval/test_hard_guard_real_home.py` — NFR-SEC3 hard guard against real `~/.claude/`.

## Pytest run

Full log: [`../../evidence/T02.10/pytest-T02.10.log`](../../evidence/T02.10/pytest-T02.10.log)

```
$ uv run pytest tests/cli/eval/test_hard_guard_real_home.py -v
============================= test session starts ==============================
collected 6 items

tests/cli/eval/test_hard_guard_real_home.py::TestRealHomeAsScratchRoot::test_setup_refuses_real_dot_claude_as_home_root PASSED [ 16%]
tests/cli/eval/test_hard_guard_real_home.py::TestRealHomeAsScratchRoot::test_per_eval_home_is_empty_when_setup_refuses PASSED [ 33%]
tests/cli/eval/test_hard_guard_real_home.py::TestRealHomeAsScratchRoot::test_setup_refuses_real_dot_claude_with_permissive_config_does_not_help PASSED [ 50%]
tests/cli/eval/test_hard_guard_real_home.py::TestScratchRootContainsRealHomeViaSymlink::test_setup_refuses_when_per_eval_home_symlinks_into_real_dot_claude PASSED [ 66%]
tests/cli/eval/test_hard_guard_real_home.py::TestScratchRootContainsRealHomeViaSymlink::test_setup_refuses_when_scratch_root_symlinks_into_real_dot_claude PASSED [ 83%]
tests/cli/eval/test_hard_guard_real_home.py::test_hard_guard_contract_pin PASSED [100%]

============================== 6 passed in 0.15s ===============================
```

Host: `~/.claude/` materialized at `/config/.claude/` (verified via `Path.home() / ".claude"` resolution inside `real_claude_dir` fixture). All 6 tests ran (none skipped) — proving the hard guard fires on a host where the catastrophic case is reachable.

## Regression check on sibling isolation tests

```
$ uv run pytest tests/cli/eval/test_path_containment.py tests/cli/eval/test_defense_in_depth.py tests/cli/eval/test_home_isolation_extend.py tests/cli/eval/test_isolation_dataclass.py -q
collected 136 items
............................................................................
.................................................                            (truncated)
============================= 136 passed in 0.29s ==============================
```

D-0028 (T02.07), D-0029 (T02.08), and D-0030 (T02.09) sibling tests remain green; nothing under `src/superclaude/cli/eval/isolation.py` was modified by D-0031.

## Acceptance-criteria walk-through

| Criterion | Evidence |
|---|---|
| File `tests/cli/eval/test_hard_guard_real_home.py` exists | Created in this task. |
| At least 2 tests proving `HomeIsolation.setup()` refuses real `~/.claude/` | Six tests across two attack-vector classes plus the coverage pin: `TestRealHomeAsScratchRoot` (3 tests, vector 1 step 3) + `TestScratchRootContainsRealHomeViaSymlink` (2 tests, step 4) + `test_hard_guard_contract_pin`. |
| Tests pass on a host where `~/.claude/` exists | Pytest log above — 6 passed in 0.15s; host has `/config/.claude/` materialized. |
| Tests skipped (with explicit reason) on hosts where `~/.claude/` does not exist | `real_claude_dir` fixture: `pytest.skip(f"NFR-SEC3 hard-guard test requires the host's real ~/.claude/ directory to exist at {path}; skipping on hosts where it is absent.")`. |
| Refusal occurs before any FS write under the rejected HOME | `_DirSnapshot.capture()` runs pre-test via `dot_claude_snapshot` fixture (SHA-256 + mtime_ns + `Path.lstat()` per direct child); post-refusal assertion iterates every pre-existing entry, asserting `after_entry == before_entry`. Plus `test_per_eval_home_is_empty_when_setup_refuses` asserts the leaked per-eval HOME (intentionally created by mkdtemp before the guard runs, per NFR-ISO2 / T02.13) is empty. |
| `TASKLIST_ROOT/artifacts/D-0031/spec.md` records the hard-guard contract | `spec.md` "Hard-guard contract (NFR-SEC3)" section pins the four-item contract. |

## Containment bucketing verified

| Vector | Test | Asserted `check` value |
|---|---|---|
| Real `~/.claude/` as `home_root` (default config) | `test_setup_refuses_real_dot_claude_as_home_root` | `scratch_root_allowlist` |
| Real `~/.claude/` as `home_root` (empty allowlist) | `test_setup_refuses_real_dot_claude_with_permissive_config_does_not_help` | `scratch_root_allowlist` |
| Per-eval HOME symlinks into `~/.claude/` | `test_setup_refuses_when_per_eval_home_symlinks_into_real_dot_claude` | `home_path_escape` |
| Scratch root *itself* symlinks into `~/.claude/` | `test_setup_refuses_when_scratch_root_symlinks_into_real_dot_claude` | `scratch_root_allowlist` |

Every vector pins both the exception type (`HomeContainmentViolation`) and the `check` field via `pytest.raises(...) as exc_info` + `assert exc_info.value.check == "..."`.

## Forensic invariants verified

| Invariant | Mechanism | Tests that pin it |
|---|---|---|
| Pre-existing entries under `~/.claude/` are byte-identical after refused setup | Per-entry `_EntrySnapshot` equality (mtime_ns + SHA-256 + size + type flags) | 1, 1b, 2, 3 (all snapshot-bearing tests) |
| Leaked per-eval HOME (mkdtemp partial preservation) is empty | `list(leaked_home.iterdir()) == []` | 1a (`test_per_eval_home_is_empty_when_setup_refuses`), 3 (per-leak check inside `test_setup_refuses_when_scratch_root_symlinks_into_real_dot_claude`) |
| Only test-scoped leak names appear under `~/.claude/` | `name.startswith("HardguardevalT0210-")` | 1, 3 |
| Verbatim forensic payload on refusal | `exc_info.value.scratch_root == <attempted path>` | 1, 3 |

## Cleanup verification

The `cleanup_leaked_eval_homes` fixture removed every per-eval HOME leak this test module created under `/config/.claude/`. Post-run state:

```
$ ls /config/.claude/HardguardevalT0210-* 2>&1
ls: cannot access '/config/.claude/HardguardevalT0210-*': No such file or directory
```

(Empty pattern match — no leaks remain.)

## Artifacts produced

- `tests/cli/eval/test_hard_guard_real_home.py` (new module, ~600 lines including docstrings and fixtures).
- `.dev/releases/current/cliEval/artifacts/D-0031/spec.md`
- `.dev/releases/current/cliEval/artifacts/D-0031/notes.md`
- `.dev/releases/current/cliEval/artifacts/D-0031/evidence.md` (this file)
- `.dev/releases/current/cliEval/evidence/T02.10/pytest-T02.10.log`
