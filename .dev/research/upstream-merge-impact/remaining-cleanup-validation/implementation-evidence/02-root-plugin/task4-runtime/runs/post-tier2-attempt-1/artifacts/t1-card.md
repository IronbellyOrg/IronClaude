<!-- Tier-1 reflection card. Producer: Task(sc:sc-root-cause-analyst) agentId aaba08de0607b06fe. hypothesis_source: agent. Persisted verbatim by orchestrator before calibration. Relative paths are relative to fixtures/project/. -->
## Summary
All three tasks are present in the files on disk. T-101 and T-102 are implemented in `src/greeting.py:1-4`. T-103's tests exist only as a file on disk (`tests/test_greeting.py`), are not in the supplied diff, and have not been run. I found no Drift or Regression against spec R-001..R-003. The main structural risk is that `from src.greeting import greet` may not import under a plain `pytest` run. This is unverified because no tests could be run in this audit (`execution.log:5`).

## Per-task verdicts
| Task | Spec req | Verdict | Evidence |
|---|---|---|---|
| T-101 (`completed.md:6`) | R-001: exact "Hello, Ada!" for Ada (`spec.md:6`) | implemented | `src/greeting.py:4` `return f"Hello, {name}!"`; `changes.patch:9` |
| T-102 (`completed.md:7`) | R-002: empty name raises ValueError (`spec.md:9`) | implemented | `src/greeting.py:2-3` `if not name: raise ValueError("name required")`; `changes.patch:7-8` |
| T-103 (`completed.md:8`) | R-003: tests cover the normal greeting and the empty-name rejection (`spec.md:12`) | implemented (on disk only, not run) | `tests/test_greeting.py:4-5` (Ada case), `tests/test_greeting.py:8-13` (empty case); declared at `execution.log:4`; absent from `changes.patch:1-9` |

The orchestrator map (`runs/post-tier2-attempt-1/artifacts/artifacts/task-to-work-map.yaml:15-32`) matches these verdicts: hunk H1 maps to T-101 and T-102, and there are 0 unmapped hunks.

## Deviations
- **D-1**
  - Location: `src/greeting.py:2`
  - Mapped task: T-102
  - Spec section: R-002 (`spec.md:8-9`)
  - Class: **authorized**
  - Rationale: the check rejects every falsy value (None, 0, [], False), not just `""`. That goes further than R-002 requires but does not contradict it, because the spec says nothing about non-empty falsy input. The change is mapped to T-102, so it is not Drift.
  - Evidence: `if not name:` at `src/greeting.py:2`, against "MUST reject an empty name with ValueError" at `spec.md:9`.
- Drift: none. The only hunk, H1, is mapped (`task-to-work-map.yaml:8-10`).
- Regression: none. No line of code contradicts R-001 or R-002.

## Grounding gaps
- **G-1: tests not in the supplied diff**
  - hunk_ref: none. `tests/test_greeting.py` is missing from `changes.patch:1-9`.
  - evidence_missing: the file is not in the diff. With git init only and no commits, there is no history showing who created it or when.
  - why_not_classifiable: there is no hunk to classify. The only proof of authorship is the log claim at `execution.log:4`.
  - next_evidence_needed: a diff that includes `tests/`, or a run with the scope widened to `src/,tests/`.
- **G-2: R-003 not proven at runtime**
  - hunk_ref: none.
  - evidence_missing: test execution results. The test tool was unavailable and `execution.log:5` says no tests were run.
  - why_not_classifiable: I cannot confirm the tests actually exercise the code. I make no claim that they pass or fail.
  - next_evidence_needed: a `pytest` run from the project root, with its output saved.

## Risks
- **Regression candidate, whitespace input:** `greet("   ")` would pass the check at `src/greeting.py:2` and return `"Hello,    !"`. R-002 only says "empty", so this is not a regression today. If the spec ever comes to mean "blank", it would become one. [INFERRED: "empty" may be read as covering blank strings]
- **Regression candidate, non-string input:** `greet(42)` returns `"Hello, 42!"` because `src/greeting.py:4` has no type check. The spec says nothing on this, so it is noted only.
- **Structural risk, test import:** `tests/test_greeting.py:1` imports `from src.greeting import greet`. The project has no `conftest.py`, `pytest.ini`, `pyproject.toml`, `setup.cfg`, `tox.ini`, `src/__init__.py` or `tests/__init__.py` (I checked with Glob, so there is no line to cite). [INFERRED] In pytest's default "prepend" import mode, a rootdir-less `tests/` without `__init__.py` puts `tests/` on sys.path, not the project root. A plain `pytest` run would then fail with ModuleNotFoundError: src. `python -m pytest` run from the root would probably work, because it adds the current directory to sys.path.
- **Structural risk, tasklist vs evidence:** `completed.md:8` marks T-103 `[x]`, but the only proof is a file outside the diff and outside `--scope src/` (`task-to-work-map.yaml:30-31`).
- **Minor:** `tests/test_greeting.py:8-13` uses a hand-written try/except instead of `pytest.raises`. It is correct when read, but more fragile to change.

## Recommendations
1. `conftest.py` (empty, at the project root) or `pyproject.toml` with `[tool.pytest.ini_options] pythonpath = ["."]`. **Change:** make `src.greeting` importable under a plain `pytest`. **Verifier:** run `pytest -q` from the project root; 2 tests should be collected and passing.
2. `tests/test_greeting.py:8-13`. **Change:** replace the try/except with `with pytest.raises(ValueError): greet("")`. **Verifier:** the same pytest run.
3. `changes.patch` / audit inputs. **Change:** regenerate the diff to include `tests/test_greeting.py`, or widen the scope to `src/,tests/`. **Verifier:** the task-to-work map shows T-103 mapped to a hunk with `in_supplied_diff: true`.
4. `spec.md:9` (optional). **Change:** say whether whitespace-only names and non-string names must be rejected. If they must, use `if not isinstance(name, str) or not name.strip():` at `src/greeting.py:2`. **Verifier:** add tests for `"   "` and `None`.

## Self-reported confidence
0.82
