# Reviewer 2 brief — persona: qa (coverage / acceptance / verification lens); model slot: haiku (alias resolves to grok-4.7)

Fixed agent type sc:reflect-reviewer, read-only. Audit ONLY the supplied hunks/matrices and files under reviewer_grounding_root. Audit the coverage slice AGAINST the spec body and the test file; check whether each acceptance criterion is actually evidenced. Classify every divergence under exactly one of Authorized expansion / Necessary deviation / Drift / Regression; evidence-insufficient items are Grounding Gaps (never a 5th class). Independently challenge the T1 card — do not simply agree. Return a structured card: findings (id, file:line in snapshot paths, class or gap, signals, Grounded/[INFERRED]), grounding gaps, risks, recommendations (file+change+verifier), self-reported confidence.

## T1 card excerpt

```markdown
## Coverage map

| Task | Spec req | Work, with verified citation | Status |
|---|---|---|---|
| T-101 (completed.md:6) | R-001 (spec.md:5-6) | `src/greeting.py:4` `return f"Hello, {name}!"`. It is diff-backed at changes.patch:9. By static reading it gives "Hello, Ada!" for "Ada". | Covered (static) |
| T-102 (completed.md:7) | R-002 (spec.md:8-9) | `src/greeting.py:2-3` `if not name: raise ValueError("name required")`. Diff-backed at changes.patch:7-8. | Covered (static) |
| T-103 (completed.md:8) | R-003 (spec.md:11-12) | `tests/test_greeting.py:4-5` (ordinary) and `:8-13` (empty-input rejection). The file exists on disk. It is not in changes.patch (the patch has a single file header, changes.patch:1-4) and is outside `--scope src/`. | Presence only; the requirement says tests "exercise", which needs execution. That has not happened. |

- **Frontmatter:** `status: done` at completed.md:2. Claimed completion is 3/3. Presence is independently grounded at 3/3. Execution is grounded at 0/1.
- **Orchestrator map:** I checked `artifacts/artifacts/task-to-diff-map.md`. Its citations match what I read. Note that the map is at `artifacts/artifacts/`, not `artifacts/`.
- **Patch vs. disk:** changes.patch:5-9 is a single hunk, and `src/greeting.py:1-4` is byte-identical to it. Both files are 4 lines.

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

```

## Grounding hunks

- reviewer_grounding_root: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root
- snapshot_kind: native-selected-inputs
- native_reviewer_snapshot: verified
- native_reviewer_snapshot_manifest_path: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/provenance-manifest.json
- reviewer_grounding_degraded: ["snapshot-mcp-unindexed"] — use native Read/Grep/Glob ONLY inside reviewer_grounding_root; no MCP, no live-project lookups.
- audit_repo_root (original, for provenance only — do NOT read it): /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project
- allowed output root (orchestrator writes; you write nothing): /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts
- plugin resource root (read-only; you may Read skills/sc-reflect-protocol/refs/deviation-taxonomy.md): /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/plugin
- Verification triangle: NOT run (execute_shell_command unavailable). No test results exist. No task log supplied.

Provenance map (source_path -> snapshot_path):

| source | snapshot |
|---|---|
| /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project/spec.md | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/spec.md |
| /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project/completed.md | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/completed.md |
| /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project/changes.patch | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/changes.patch |
| /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project/src/greeting.py | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/src/greeting.py |
| /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project/tests/test_greeting.py | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/tests/test_greeting.py |
| /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/t1-card.md | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/t1-card.md |
| /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/artifacts/task-to-diff-map.md | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/task-to-diff-map.md |
| /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/artifacts/reuse-audit.yaml | /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/reuse-audit.yaml |

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/changes.patch:1-9
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

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/src/greeting.py:1-4
```python
def greet(name):
    if not name:
        raise ValueError("name required")
    return f"Hello, {name}!"
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/spec.md:5-12
```markdown
## R-001 Greeting
The greet function MUST return the exact string Hello, Ada! for Ada.

## R-002 Empty input
The greet function MUST reject an empty name with ValueError.

## R-003 Evidence
Tests MUST exercise the ordinary greeting and empty-input rejection.
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/completed.md:1-8
```markdown
---
status: done
---
# Synthetic completed tasklist

- [x] T-101 implements R-001 ordinary greeting.
- [x] T-102 implements R-002 empty-name rejection.
- [x] T-103 implements R-003 both ordinary and empty-input tests.
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/tests/test_greeting.py:1-13
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

## Coverage slice

| Task | Spec req | Work (snapshot path:line) | T1 status |
|---|---|---|---|
| T-101 (completed.md:6) | R-001 (spec.md:5-6) | src/greeting.py:4 | covered (static) |
| T-102 (completed.md:7) | R-002 (spec.md:8-9) | src/greeting.py:2-3 | covered (static) |
| T-103 (completed.md:8) | R-003 (spec.md:11-12) | tests/test_greeting.py:4-5, 8-13 (not in changes.patch; outside --scope) | presence only; unexecuted |
