<!-- Wave 1C Tier-1 card. Author: sc:sc-root-cause-analyst, requested model slot: sonnet (claude-sonnet-5-5[1m]); agentId a0e1a2636ce725d44. Persisted verbatim by orchestrator. Paths are repo-relative to audit_repo_root = fixtures/project. -->
# Tier-1 Reflection Card (UC-2 post-execution): greeting fixture

Paths are repo-relative to `audit_repo_root`. I read all inputs directly. I did not read `execution.log` or `proposed.md`. Nothing was executed.

## Coverage map

| Task | Spec req | Work, with verified citation | Status |
|---|---|---|---|
| T-101 (completed.md:6) | R-001 (spec.md:5-6) | `src/greeting.py:4` `return f"Hello, {name}!"`. It is diff-backed at changes.patch:9. By static reading it gives "Hello, Ada!" for "Ada". | Covered (static) |
| T-102 (completed.md:7) | R-002 (spec.md:8-9) | `src/greeting.py:2-3` `if not name: raise ValueError("name required")`. Diff-backed at changes.patch:7-8. | Covered (static) |
| T-103 (completed.md:8) | R-003 (spec.md:11-12) | `tests/test_greeting.py:4-5` (ordinary) and `:8-13` (empty-input rejection). The file exists on disk. It is not in changes.patch (the patch has a single file header, changes.patch:1-4) and is outside `--scope src/`. | Presence only; the requirement says tests "exercise", which needs execution. That has not happened. |

- **Frontmatter:** `status: done` at completed.md:2. Claimed completion is 3/3. Presence is independently grounded at 3/3. Execution is grounded at 0/1.
- **Orchestrator map:** I checked `artifacts/artifacts/task-to-diff-map.md`. Its citations match what I read. Note that the map is at `artifacts/artifacts/`, not `artifacts/`.
- **Patch vs. disk:** changes.patch:5-9 is a single hunk, and `src/greeting.py:1-4` is byte-identical to it. Both files are 4 lines.

## Deviation register

Hunks: 1 (H1, changes.patch:5-9, which creates `src/greeting.py`).

**Result: no divergence found.** The registers hold zero Authorized, zero Necessary, zero Drift and zero Regression entries.

- **H1:**
  - It maps to T-101 and T-102, so Drift's "unmapped hunk" signal does not match.
  - It contradicts no acceptance criterion: R-001 and R-002 are both satisfied by static reading.
  - The Regression signals do not match. The test-failure signal needs execution, and none ran.
  - It adds no scope beyond the spec, so there is nothing to classify as Authorized expansion or Necessary deviation.
- **S_dev_density** = 0/1.

The T-103 diff-vs-claim mismatch is not classified as a deviation. The test file is real, but no diff evidence says whether it was written as part of the audited change. It is a Grounding Gap, not a fifth class.

## Grounding gaps

```yaml
- hunk_ref: tests/test_greeting.py:1-13 (no hunk in changes.patch)
  evidence_missing: Test-run result (verification triangle skipped, execute_shell_command unavailable); no task log; no diff hunk or provenance for the test file.
  why_not_classifiable: Cannot tell whether T-103 "exercise" holds, or whether the tests pass, without execution. A pytest exit-1 would be Regression and exit-5 would be Drift/coverage (taxonomy exit-code table).
  next_evidence_needed: pytest exit code run from the project root, plus provenance of tests/test_greeting.py (a diff or task-log entry).
  owner: user
  decision_needed_by_user: true
- hunk_ref: completed.md:6-8 (claim "done")
  evidence_missing: No task log, so there is no self-reported test state to compare against.
  why_not_classifiable: Regression detection degrades to a log claim, and no claim exists.
  next_evidence_needed: Task log or a verification run.
  owner: user
  decision_needed_by_user: false
```

Because the gaps list is non-empty, `status: partial` and `needs_human_decision: true` are forced.

## Risk register

| # | Risk | Tag |
|---|---|---|
| 1 | The tests were never run. The R-003 "exercise" claim is unverified. | Grounded (map "Verification triangle" section; tests/test_greeting.py:1-13 read but not executed) |
| 2 | Diff-vs-claim mismatch. T-103 is marked `[x]` (completed.md:8) but its work is absent from changes.patch and outside scope. | Grounded (changes.patch:1-9) |
| 3 | The import path `from src.greeting import greet` (tests/test_greeting.py:1) depends on how the tests are run. The directory listing shows no `src/__init__.py`, no `tests/__init__.py`, no conftest and no pyproject. `src` would resolve as a namespace package only if the project root is on `sys.path`. | Grounded for the file absence (directory glob); [INFERRED] for the failure mode. Plain `pytest` may fail at collection (exit 2, a Grounding Gap, not a Regression) where `python -m pytest` would pass. |
| 4 | Whitespace-only names such as `"   "` pass the `not name` check (src/greeting.py:2) and return "Hello,    !". Spec R-002 says only "empty", so this is not a contradiction. | Grounded (src/greeting.py:2) for the code, [INFERRED] for the intent |
| 5 | `None` and falsy non-strings such as `0` raise ValueError. A truthy non-string such as `5` returns "Hello, 5!". The spec is silent. | [INFERRED] |
| 6 | The tests do not check the ValueError message, whitespace or non-string inputs. The empty-input test is a try/except pattern (tests/test_greeting.py:8-13) that works but is weaker than `pytest.raises`. | Grounded (tests/test_greeting.py:8-13) |
| 7 | Cross-task interaction: T-101 and T-102 both touch `greet`. This is low risk, since one 4-line function implements both and no conflicting edit is visible. | Grounded (src/greeting.py:1-4) |
| 8 | Regression candidates: none identified. Regression cannot be ruled out until the tests run. | [INFERRED] |

## Recommendations

1. **File:** none (a verifier run only). **Change:** run pytest from the fixture project root, using `python -m pytest tests/test_greeting.py`. **Verifier:** the exit code, read against the taxonomy exit-code table. Exit 0 closes the T-103 gap, 1 is Regression, 2/3 is a Grounding Gap and 5 is Drift/coverage.
2. **File:** `changes.patch` or a task log. **Change:** record the provenance of `tests/test_greeting.py` by including it in the diff or in a task-log entry, and widen `--scope` to `tests/`. **Verifier:** re-run the audit and check that a hunk now maps T-103 to tests/test_greeting.py.
3. **File:** `tests/test_greeting.py`. **Change:** add `tests/__init__.py` or a conftest/`pythonpath` setting if plain `pytest` fails to collect. **Verifier:** plain `pytest` from the root collects 2 tests.
4. **File:** `spec.md` (R-002). **Change:** state whether whitespace-only and non-string names count as "empty". **Verifier:** spec review. If the answer is yes, add a matching test and re-run recommendation 1.

## Self-reported confidence

**0.72**

- Static mapping, citations and the "no divergence" finding are strong. The source is 4 lines, there is one hunk, and the patch matches the file exactly.
- I deduct for three things: no test execution, no task log, and the T-103 provenance gap.
- I deduct a little more for a possible Regression I cannot rule out. The import-path failure mode is also inference only.
