<!-- Reviewer brief 2. Persona: qa. Model slot: haiku. Agent type: sc:reflect-reviewer (read-only). -->
<!-- Grounding: reviewer_grounding_root: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root ; snapshot_kind: native-selected-inputs ; native_reviewer_snapshot: verified ; native_reviewer_snapshot_manifest_path: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/provenance-manifest.json -->
<!-- reviewer_grounding_degraded: ["snapshot-mcp-unindexed"] -- use native Read/Grep/Glob ONLY within the snapshot root; NO MCP lookups; NO live-project paths; NO shell/git/test execution; return findings only. -->
<!-- Mode: UC-2 post-execution audit. Classify every divergence as exactly one of authorized | necessary | drift | regression (precedence Regression > Drift > Necessary > Authorized). Authorized REQUIRES an explicit approving artifact (updated tasklist, spec amendment, user approval in log). Necessary REQUIRES inline documented rationale. Drift = unmapped change with no rationale and no contradiction. Regression = contradicts a spec acceptance criterion / previously-passing test / invariant. Evidence-insufficient items go to grounding_gaps, never a 5th class. Tag uncited claims with the literal prefix [INFERRED]. Cite snapshot paths file:line. -->
# Reviewer 2 — qa persona (coverage / acceptance / verification lens)

Your lens: audit whether each acceptance criterion is actually evidenced, whether the tests statically exercise the required behaviour, and what the absence of test execution means. Audit the coverage slice AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the slice. Challenge the T1 card where it is wrong. Return YAML: {reviewer: 2, persona: qa, per_task: [{task, verdict, evidence}], deviations: [{id, location, mapped_task, spec_section, class, rationale, evidence}], grounding_gaps: [{hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, decision_needed_by_user}], risks: [...], recommendations: [{file, change, verifier}], self_reported_confidence}.

## T1 card excerpt
_(Verbatim T1-card excerpt; its H2 headings demoted to H4 so the brief keeps exactly three H2 sections. Relative paths resolve against the snapshot root.)_
#### Per-task verdicts
| Task | Spec req | Verdict | Evidence |
|---|---|---|---|
| T-101 (`completed.md:6`) | R-001: exact "Hello, Ada!" for Ada (`spec.md:6`) | implemented | `src/greeting.py:4` `return f"Hello, {name}!"`; `changes.patch:9` |
| T-102 (`completed.md:7`) | R-002: empty name raises ValueError (`spec.md:9`) | implemented | `src/greeting.py:2-3` `if not name: raise ValueError("name required")`; `changes.patch:7-8` |
| T-103 (`completed.md:8`) | R-003: tests cover the normal greeting and the empty-name rejection (`spec.md:12`) | implemented (on disk only, not run) | `tests/test_greeting.py:4-5` (Ada case), `tests/test_greeting.py:8-13` (empty case); declared at `execution.log:4`; absent from `changes.patch:1-9` |

The orchestrator map (`runs/post-tier2-attempt-1/artifacts/artifacts/task-to-work-map.yaml:15-32`) matches these verdicts: hunk H1 maps to T-101 and T-102, and there are 0 unmapped hunks.

#### Grounding gaps
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

#### Risks
- **Regression candidate, whitespace input:** `greet("   ")` would pass the check at `src/greeting.py:2` and return `"Hello,    !"`. R-002 only says "empty", so this is not a regression today. If the spec ever comes to mean "blank", it would become one. [INFERRED: "empty" may be read as covering blank strings]
- **Regression candidate, non-string input:** `greet(42)` returns `"Hello, 42!"` because `src/greeting.py:4` has no type check. The spec says nothing on this, so it is noted only.
- **Structural risk, test import:** `tests/test_greeting.py:1` imports `from src.greeting import greet`. The project has no `conftest.py`, `pytest.ini`, `pyproject.toml`, `setup.cfg`, `tox.ini`, `src/__init__.py` or `tests/__init__.py` (I checked with Glob, so there is no line to cite). [INFERRED] In pytest's default "prepend" import mode, a rootdir-less `tests/` without `__init__.py` puts `tests/` on sys.path, not the project root. A plain `pytest` run would then fail with ModuleNotFoundError: src. `python -m pytest` run from the root would probably work, because it adds the current directory to sys.path.
- **Structural risk, tasklist vs evidence:** `completed.md:8` marks T-103 `[x]`, but the only proof is a file outside the diff and outside `--scope src/` (`task-to-work-map.yaml:30-31`).
- **Minor:** `tests/test_greeting.py:8-13` uses a hand-written try/except instead of `pytest.raises`. It is correct when read, but more fragile to change.


## Grounding hunks

Path map (source -> snapshot):
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/spec.md -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/spec.md
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/completed.md -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/completed.md
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/changes.patch -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/changes.patch
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/execution.log -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/execution.log
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/src/greeting.py -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/src/greeting.py
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/tests/test_greeting.py -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/tests/test_greeting.py
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/t1-card.md -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/t1-card.md
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/artifacts/task-to-work-map.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/task-to-work-map.yaml
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/verify-logs/invocations.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/verify-logs/invocations.yaml
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/artifacts/interaction-effects.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/interaction-effects.yaml
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/artifacts/reuse-audit.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/reuse-audit.yaml

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/spec.md:1-12
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

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/completed.md:1-8
```markdown
---
status: done
---
# Synthetic completed tasklist

- [x] T-101 implements R-001 ordinary greeting.
- [x] T-102 implements R-002 empty-name rejection.
- [x] T-103 implements R-003 both ordinary and empty-input tests.
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/tests/test_greeting.py:1-13
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

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/src/greeting.py:1-4
```python
def greet(name):
    if not name:
        raise ValueError("name required")
    return f"Hello, {name}!"
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/changes.patch:1-9
```diff
diff --git a/src/greeting.py b/src/greeting.py
new file mode 100644
--- /dev/null
+++ b/src/greeting.py
@@ -0,0 +1,4 @@
+def greet(name):
+    if not name:
+        raise ValueError("name required")
+    return f"Hello, {name}!"
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/execution.log:1-5
```text
Synthetic completed-work log, not an execution claim about product code.
T-101 R-001: created src/greeting.py.
T-102 R-002: empty names raise ValueError.
T-103 R-003: created tests/test_greeting.py with ordinary and empty-name cases.
No test execution is claimed; inspect these files independently.
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/verify-logs/invocations.yaml:1-5
```yaml
# §6.1 step 5.5 verification triangle: NOT RUN.
verification_ran: false
verification_skip_reason: tool-unavailable   # mcp__serena__execute_shell_command not exposed; orchestrator did not substitute Bash for the sanctioned surface
invocations: []
```

## Coverage slice

| Task | Spec req | Status (orchestrator map) | Grounding |
|---|---|---|---|
| T-101 | R-001 (spec.md:5-6) | implemented | src/greeting.py:4 |
| T-102 | R-002 (spec.md:8-9) | implemented | src/greeting.py:2-3 |
| T-103 | R-003 (spec.md:11-12) | implemented statically; NOT in supplied diff; NOT executed | tests/test_greeting.py:4-5, 8-13; execution.log:4 |
