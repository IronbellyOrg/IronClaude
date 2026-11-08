# R-1 fix record (cut-off re-check after the pending save) and D-1

Nothing was staged or committed. Original copies of the two changed code files are in `/tmp/r1-orig/` (`cycle.py.orig`, `test_cycle.py.orig`).

## What changed

| File | Change |
|---|---|
| `src/superclaude/cli/issue_watch/cycle.py`, `_Cycle._launch` | Before `record.mark_pending` the whole document is kept in `before_pending`. After `self._save()` (the durable pending write) `self.deadline.launch_allowed()` is checked again. If the 120 s cut-off has passed, `self._set(before_pending)`, `self._save()` and `raise _Skip("budget_exhausted")`. No launcher call happens, no entry stays on disk, and the existing `_candidates` path writes the `budget_exhausted` decision line and does not stamp the issue as considered. +7 lines. |
| `tests/issue_watch/test_cycle.py` | New helper `_SlowPendingSaveStore` (wraps the real store; the save of issue 9 in state `pending` advances the `FakeClock`; records every saved document) and two tests (below). +65 lines. |
| `docs/designs/issue-watcher-setup.md` | D-1, three one-sentence edits (below). |

The restore is the whole document (`StoreDoc` is frozen, so `before_pending` is the exact object that was current before the pending write), never field by field.

## Tests

- `test_a_launch_does_not_start_when_the_pending_save_crosses_120_s__fr011_ac19`: the pending save takes 121 s. Asserts exit 0, `launched_issue is None`, `launcher.calls == []`, the first saved document has the entry `pending` with `launches` 1, the second saved document equals the document loaded before the cycle (`restored == before`) and has no entry for issue 9, one decision line `(9, "budget_exhausted")` with no `state`, the store on disk has `entries == {}`, issue 9 is not in `considered`, and the last saved document has no entry.
- `test_a_launch_still_starts_when_the_pending_save_ends_at_exactly_120_s__fr011_ac19`: the pending save takes exactly 120 s. Asserts exit 0, `launched_issue == 9`, one launcher call with the full 120.0 s timeout, entry `launched`.

No skip, no xfail, no assertion weakened.

## Pre-fix proof (FAIL) and post-fix (PASS)

Pre-fix: a /tmp copy of `src`, `tests` and `pyproject.toml` with the original `cycle.py` (`/tmp/r1-orig/cycle.py.orig`) put in place, run with `PYTHONPATH=/tmp/r1-prefix/src uv run --project <repo> --no-sync pytest ... --rootdir=/tmp/r1-prefix`. The copy was deleted afterwards. Output lines:

```text
rootdir: /tmp/r1-prefix
collected 542 items / 540 deselected / 2 selected
tests/issue_watch/test_cycle.py F.                                       [100%]
FAILED tests/issue_watch/test_cycle.py::test_a_launch_does_not_start_when_the_pending_save_crosses_120_s__fr011_ac19
E   AssertionError: assert 9 is None   (launched_issue=9, 'duration_ms': 121000)
================= 1 failed, 1 passed, 540 deselected in 0.73s ==================
```

The boundary test passes on the old code, as it should: it pins that the fix does not cut off a launch at exactly 120 s.

Post-fix, in the repo:

```text
tests/issue_watch/test_cycle.py ..                                       [100%]
====================== 2 passed, 540 deselected in 0.11s =======================
```

## D-1 edits (`docs/designs/issue-watcher-setup.md`)

Verified against `cli.py` (`_load_config(..., platform=False)` for `status` at line 169, `_config_exit` exits 2; `reset_command` calls `_load_config(config_path)` with the platform check at line 314, `cycle.check_platform()` raises `platform_unsupported`) and `uv run superclaude issue-watch status --help` / `reset --help` (they list no exit codes, so the code is the source).

1. Line 53: `once`, `check-config` and `init-state` exit 2 on any other platform becomes `once`, `check-config`, `init-state` and `reset` exit 2 on any other platform, plus the sentence `(status does not check the platform.)`.
2. Line 432: `status` exits 0 healthy, 1 unhealthy, "and 6 when the store cannot be read" becomes 0, 1, 2 when the configuration file is invalid, 6 when the store cannot be read.
3. Section 10.1 table, exit 2 row (one extra edit for consistency with edit 2, same fact): added `status` uses it for an invalid configuration file.

`docs/designs/issue-watcher.md` and the spec were not touched.

## Final results

| Check | Result |
|---|---|
| `uv run pytest tests/issue_watch/ -q` | 2637 passed in 16.21s |
| `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/ -q` | 2637 passed in 6.51s |
| `make lint` | `uv run ruff check .` All checks passed (architecture policy compliant, 5 warnings, pre-existing) |
| `uvx --offline ruff@0.15.20 check` on `cycle.py`, `test_cycle.py` | All checks passed! |
| `uvx --offline ruff@0.15.20 format --check` on the same files | 2 files already formatted |
| `make verify-sync` | All components in sync. |
| G-2 set (`tests/issue_watch/ tests/skills/test_model_alias_policy.py tests/docs/test_retired_docs_absent.py tests/cli/test_cli_registration.py tests/swarm/test_cli_registration.py tests/recommend/test_cli_registration.py -q`) | 2667 passed, 1 skipped in 19.01s |
| markdownlint 0.38.0 (`~/.cache/pre-commit/reposcxph1ch/node_env-system/bin/markdownlint`, repo `.markdownlint.json`, /tmp copy of the runbook, no `--fix`) | exit 0 |

The one skip in the G-2 set is `tests/swarm/test_cli_registration.py:127` ("got empty parameter set for (subcommand)"); it is outside this change and was not touched.
