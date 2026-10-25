<!-- reviewer-2: sc:reflect-reviewer, persona=qa, model slot=haiku (grok-4.7[1m]). Read-only: return findings, run no shell/git, write nothing. Persona: QA (coverage / acceptance lens). Audit the coverage slice AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix as a finding. Judge whether each acceptance criterion (R-001..R-003) is evidenced by the supplied diff, whether the tests would actually exercise the criteria, and whether the frontmatter 'status: done' is supported. -->
## T1 card excerpt

### Task/spec-to-work map (verbatim from t1-card.md)
| Task | Spec req | Diff hunk | Evidence file:line | Verdict |
|---|---|---|---|---|
| T-101 (`completed.md:6`) | R-001 (`spec.md:5-6`) | H1 (`changes.patch:5-9`) | `src/greeting.py:4` returns `f"Hello, {name}!"`, so `greet("Ada")` gives `Hello, Ada!`. `execution.log:2` agrees. | Satisfied (static only) |
| T-102 (`completed.md:7`) | R-002 (`spec.md:8-9`) | H1 | `src/greeting.py:2-3` raises `ValueError("name required")` for `""`. `execution.log:3` agrees. | Satisfied (static only) for `""`. Broader falsy behavior is unspecified (see G3). |
| T-103 (`completed.md:8`) | R-003 (`spec.md:11-12`) | none | `tests/test_greeting.py:4-5` covers the ordinary case. `tests/test_greeting.py:8-13` covers the empty case. `execution.log:4-5` claims creation and disclaims execution. | Not verifiable from the diff (G1, G2). On-disk content is adequate. |

No hunk is unmapped. The Wave 1B map agrees: `task-diff-map.yaml:29` lists no unmapped hunks, and `task-diff-map.yaml:34` gives 0.667 completion.

### Grounding gaps (verbatim from t1-card.md)
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

### Recommendations (verbatim from t1-card.md)
1. **Regenerate the diff to include tests.** Run `git -C <audit_repo_root> add -N tests && git -C <audit_repo_root> diff` and re-save the result as `changes.patch`. Success criterion: the new patch contains a hunk for `tests/test_greeting.py` with the same 13 lines as `tests/test_greeting.py:1-13`, and G1 can be closed.
2. **Verify importability and execution.** Run `python -m pytest tests -q` from the audit root, and separately plain `pytest tests -q`. Success criterion: both exit 0 with 2 tests collected and passing. If plain `pytest` fails to collect, add an empty `src/__init__.py` or a `conftest.py` or `pytest.ini` setting `pythonpath = .`, then re-run.
3. **Pin down R-002.** Edit `spec.md:9` to state the intended semantics for `None`, non-str input and whitespace-only strings. Then either tighten `src/greeting.py:2` or add tests in `tests/test_greeting.py` for those cases. Success criterion: each stated case has an assertion that passes.
4. **Correct the status.** Change `completed.md:2` to `status: partial` until recommendations 1 and 2 are met. Success criterion: the status is `done` only after the T-103 hunk is in the diff and a test run is recorded.

## Grounding hunks

snapshot_kind: native-selected-inputs
native_reviewer_snapshot: verified
reviewer_grounding_root: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root
native_reviewer_snapshot_manifest_path: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/provenance-manifest.json
reviewer_grounding_degraded: ["snapshot-mcp-unindexed"]  # use native Read/Grep/Glob inside reviewer_grounding_root ONLY; no MCP, no live-project lookups
Source -> snapshot path map (cite SNAPSHOT paths; orchestrator translates back):
- spec_path: <audit_repo_root>/spec.md -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/spec.md
- tasklist_path: <audit_repo_root>/completed.md -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/completed.md
- diff evidence: <audit_repo_root>/changes.patch -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/changes.patch
- task-log: <audit_repo_root>/execution.log -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/execution.log
- scoped source: <audit_repo_root>/src/greeting.py -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/src/greeting.py
- linked evidence (outside --scope, not in diff): <audit_repo_root>/tests/test_greeting.py -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/tests/test_greeting.py
- T1 card: <output>/t1-card.md -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/t1-card.md
- Wave 1B map: <output>/artifacts/task-diff-map.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/task-diff-map.yaml
- reuse audit: <output>/artifacts/reuse-audit.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/reuse-audit.yaml
- git inventory: <output>/artifacts/git-inventory.txt -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/git-inventory.txt  (repo has NO commits; every file incl. src/greeting.py is untracked)
Verification-results hunk: verification triangle did NOT run (execute_shell_command unavailable; verification_skip_reason: tool-unavailable). No test has been executed by anyone; execution.log:5 disclaims execution. No verify-logs artifact exists.
Runtime-surface: not a surface symbol (no ledger). Reachability gate: skipped, no-side-effect-requirements.

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/spec.md:1-12
```markdown
# Synthetic greeting contract

This fixture is synthetic audit input, not shipped product code.

## R-001 Greeting
The greet function MUST return the exact string Hello, Ada! for Ada.

## R-002 Empty input
The greet function MUST reject an empty name with ValueError.

## R-003 Evidence
Tests MUST exercise the ordinary greeting and empty-input rejection.
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/completed.md:1-8
```markdown
---
status: done
---
# Synthetic completed tasklist

- [x] T-101 implements R-001 ordinary greeting.
- [x] T-102 implements R-002 empty-name rejection.
- [x] T-103 implements R-003 both ordinary and empty-input tests.
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/tests/test_greeting.py:1-13
```python
from src.greeting import greet


def test_ordinary():
    assert greet("Ada") == "Hello, Ada!"


def test_empty():
    try:
        greet("")
    except ValueError:
        return
    raise AssertionError("empty name accepted")
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/src/greeting.py:1-4
```python
def greet(name):
    if not name:
        raise ValueError("name required")
    return f"Hello, {name}!"
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/execution.log:1-5
```text
Synthetic completed-work log, not an execution claim about product code.
T-101 R-001: created src/greeting.py.
T-102 R-002: empty names raise ValueError.
T-103 R-003: created tests/test_greeting.py with ordinary and empty-name cases.
No test execution is claimed; inspect these files independently.
```

## Coverage slice

| Task / Requirement | Diff hunk | Status | Grounding |
|---|---|---|---|
| T-101 / R-001 (completed.md:6, spec.md:5-6) | H1 changes.patch:5-9 | verified-static | src/greeting.py:4 |
| T-102 / R-002 (completed.md:7, spec.md:8-9) | H1 changes.patch:5-9 | verified-static | src/greeting.py:2-3 |
| T-103 / R-003 (completed.md:8, spec.md:11-12) | none | unverified-in-diff | tests/test_greeting.py:4-13 (outside diff/scope) |

