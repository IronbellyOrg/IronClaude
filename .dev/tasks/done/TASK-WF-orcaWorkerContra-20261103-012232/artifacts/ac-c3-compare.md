# AC-C3: skills suite compared with the Task 1 baseline

Command (`./source.md` section 7.1, AC-C3), run before any edit (Task 1) and again after Task 6 added the AC-0.9 audit:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/ -q -rf -p no:cacheprovider
```

| Run | File | Summary line |
|---|---|---|
| Baseline (Task 1) | `./artifacts/ac-c3-baseline.txt` | `608 passed in 12.65s`, `rc=0` |
| After Task 6 | `./artifacts/ac-c3-after.txt` | `804 passed in 12.23s`, `rc=0` |

## Per-test comparison

- Neither run has a `FAILED` line (`grep -c '^FAILED'` prints 0 for both files), and both exit 0. No test that passed in the baseline fails now.
- The run after Task 6 has 196 more passing tests (804 - 608). That is exactly the number of tests in the new file `tests/skills/test_worker_contract.py` (`uv run pytest tests/skills/test_worker_contract.py -q` reports `196 passed`, `./artifacts/t6-negative-check.txt`), so the 608 baseline tests all still pass and every new test passes.

Result: AC-C3 passes.

## Tracked files

`git status --short` was captured before and after the run; the two outputs are identical, so the run changed no tracked file.

## Task 8 re-run

After Task 6, only Task 7 changed files, and only under `./artifacts/`. Task 8 re-ran the same command anyway on 2026-11-03: `804 passed in 12.46s`, `rc=0`, no `FAILED` line, and `git status --short` unchanged by the run. The result above still holds: AC-C3 passes.
