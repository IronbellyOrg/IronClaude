<!-- Tier-1 reflection card. Author: sc:sc-root-cause-analyst, requested model slot: sonnet (ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5[1m]; provider model not separately reported by the Agent tool). Persisted verbatim by the orchestrator. Paths are relative to audit_repo_root=/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/fixtures/project unless they name task-diff-map.yaml (under <output>/artifacts/) or deviation-taxonomy.md (under <plugin>/skills/sc-reflect-protocol/refs/). -->
## Summary

The diff has one hunk, a new file `src/greeting.py` (`changes.patch:1-9`). The working-tree file is byte-identical to it (`src/greeting.py:1-4`). I found no deviations in the four classes.

- **T-101 and T-102:** Both are satisfied by static reading only. Nothing was executed.
- **T-103:** This task cannot be verified from the supplied diff. `tests/test_greeting.py` exists on disk and looks adequate (`tests/test_greeting.py:4-13`). It is untracked, outside `--scope src`, and absent from `changes.patch`. `execution.log:5` says no tests were run.
- **Frontmatter:** `completed.md:2` says `status: done`. My independent verdict is **partial**: 2 of 3 tasks are backed by the diff, and none were executed.
- **Taxonomy result:** No Regression, Drift, Necessary or Authorized rows. Three Grounding Gaps are open, so `status: partial` and `needs_human_decision: true` are required by `deviation-taxonomy.md:149-153`.

## Task/spec-to-work map

| Task | Spec req | Diff hunk | Evidence file:line | Verdict |
|---|---|---|---|---|
| T-101 (`completed.md:6`) | R-001 (`spec.md:5-6`) | H1 (`changes.patch:5-9`) | `src/greeting.py:4` returns `f"Hello, {name}!"`, so `greet("Ada")` gives `Hello, Ada!`. `execution.log:2` agrees. | Satisfied (static only) |
| T-102 (`completed.md:7`) | R-002 (`spec.md:8-9`) | H1 | `src/greeting.py:2-3` raises `ValueError("name required")` for `""`. `execution.log:3` agrees. | Satisfied (static only) for `""`. Broader falsy behavior is unspecified (see G3). |
| T-103 (`completed.md:8`) | R-003 (`spec.md:11-12`) | none | `tests/test_greeting.py:4-5` covers the ordinary case. `tests/test_greeting.py:8-13` covers the empty case. `execution.log:4-5` claims creation and disclaims execution. | Not verifiable from the diff (G1, G2). On-disk content is adequate. |

No hunk is unmapped. The Wave 1B map agrees: `task-diff-map.yaml:29` lists no unmapped hunks, and `task-diff-map.yaml:34` gives 0.667 completion.

## Deviation register

none

- **(a) Missing test work:** The untracked test file is not a diff hunk, so there is nothing to classify as Drift. I treat it as a missing-evidence case and route it to G1. The class signals are not met: the work maps to T-103, so it is not unmapped. It also contradicts nothing in the spec.
- **(b) `if not name`:** `src/greeting.py:2` also rejects `None`, `0` and other falsy values with `ValueError`. R-002 only says "reject an empty name" (`spec.md:9`). It does not say what to do with other falsy or non-string input. This is unspecified, not a contradiction, so it is not a Regression. It is also not Drift, because it maps to T-102. I record it as advisory (G3).

## Grounding gaps

```yaml
- hunk_ref: completed.md:8 (T-103) / tests/test_greeting.py:1-13 (no changes.patch hunk)
  evidence_missing: >
    No hunk in changes.patch for the test file. The file is untracked and outside --scope src.
    The only claim of its creation is execution.log:4, a self-report. There is no tracked-state
    evidence that it was part of the delivered change set.
  why_not_classifiable: >
    The diff under audit cannot confirm T-103 either way, and an on-disk file outside the diff
    is not diff evidence. Marking it done or missing would be a guess.
  next_evidence_needed: >
    Either regenerate changes.patch to include tests/, or confirm that the untracked
    tests/test_greeting.py is the delivered T-103 artifact.
  owner: user
  decision_needed_by_user: true

- hunk_ref: tests/test_greeting.py:1 (import) / src/greeting.py (no package marker)
  evidence_missing: >
    No test run. Glob found no src/__init__.py, no tests/__init__.py, and no conftest.py,
    pyproject.toml or pytest config in the audit root. The verification triangle did not run,
    and execution.log:5 disclaims execution.
  why_not_classifiable: >
    `from src.greeting import greet` can resolve as a namespace package if the project root is
    on sys.path, for example under `python -m pytest` run from the root or with PYTHONPATH set.
    Under plain `pytest` with the default prepend import mode and no __init__.py, the tests/
    directory is inserted on sys.path rather than the root, so the import may fail
    (ModuleNotFoundError). Under the exit-code mapping that would be a pytest exit 2/3 collection
    error, which is a Grounding Gap and not a Regression (deviation-taxonomy.md:108).
    This reasoning is [INFERRED] from standard Python and pytest behavior and was not observed.
  next_evidence_needed: >
    The output of `python -m pytest tests` and of plain `pytest tests`, run with the audit root
    as the working directory.
  owner: user
  decision_needed_by_user: true

- hunk_ref: src/greeting.py:2-3 (R-002, spec.md:9)
  evidence_missing: >
    The spec does not define "empty" for None, 0, whitespace-only strings or non-str input.
  why_not_classifiable: >
    There is no spec text to contradict. Over-rejection of None or 0 with ValueError, and
    acceptance of "   ", are neither authorized nor forbidden.
  next_evidence_needed: >
    A spec clarification on whether None should raise TypeError or ValueError, and on whether
    whitespace-only names count as empty.
  owner: user
  decision_needed_by_user: false
```

Regression detection degrades to the task-log claim, as directed. `execution.log:5` explicitly claims no execution, so there is no pass or fail signal either way.

## Risk surface

- **False completion:** `completed.md:2` says `done`, but T-103 is unverified and nothing was run. This is the main risk.
- **Test importability:** Possible collection failure (G2, [INFERRED]). If it fails, R-003 evidence is non-functional even though the file exists.
- **Falsy-input behavior:** `greet(0)` and `greet(None)` raise `ValueError`. A caller expecting `TypeError`, or wanting `0` to be accepted, would be surprised. `greet("  ")` returns `Hello,   !`. Both are unspecified (`src/greeting.py:2-4`).
- **Wider impact:** Small. `greet` is a plain module function with no entrypoint, route or CLI hook (`task-diff-map.yaml:36`), so no runtime-surface or reachability checks apply.

## Recommendations

1. **Regenerate the diff to include tests.** Run `git -C <audit_repo_root> add -N tests && git -C <audit_repo_root> diff` and re-save the result as `changes.patch`. Success criterion: the new patch contains a hunk for `tests/test_greeting.py` with the same 13 lines as `tests/test_greeting.py:1-13`, and G1 can be closed.
2. **Verify importability and execution.** Run `python -m pytest tests -q` from the audit root, and separately plain `pytest tests -q`. Success criterion: both exit 0 with 2 tests collected and passing. If plain `pytest` fails to collect, add an empty `src/__init__.py` or a `conftest.py` or `pytest.ini` setting `pythonpath = .`, then re-run.
3. **Pin down R-002.** Edit `spec.md:9` to state the intended semantics for `None`, non-str input and whitespace-only strings. Then either tighten `src/greeting.py:2` or add tests in `tests/test_greeting.py` for those cases. Success criterion: each stated case has an assertion that passes.
4. **Correct the status.** Change `completed.md:2` to `status: partial` until recommendations 1 and 2 are met. Success criterion: the status is `done` only after the T-103 hunk is in the diff and a test run is recorded.

## Self-reported confidence (0-1, informational only)

0.82. The claims about the diff and file contents were read directly. The importability analysis in G2 is [INFERRED] and unexecuted, and the whole audit rests on static reading.
