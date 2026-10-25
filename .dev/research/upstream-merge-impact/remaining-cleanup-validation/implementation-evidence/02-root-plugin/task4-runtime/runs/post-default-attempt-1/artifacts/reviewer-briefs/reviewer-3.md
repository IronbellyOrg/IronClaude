<!-- reviewer-3: persona=refactorer; model slot=opus; agent type=sc:reflect-reviewer; mode=post (UC-2); lens: structural / tech-debt lens: assess code/test structure risks (importability, guard semantics) and whether any is a deviation or only advisory. -->

## T1 card excerpt

Verbatim slice of the Tier-1 card (`/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/tier1-card.yaml`); the T1 card was blind-calibrated at C=0.79 with deviation-classification clarity 0.55 (DEV-1 Drift label conflicts with its mapped_task T-102).

```yaml
deviations:
  - id: DEV-1
    location: "src/greeting.py:2; changes.patch:7"
    mapped_task: T-102
    spec_ref: "spec.md:9"
    class: Drift
    rationale: "`if not name` rejects None/0/False/[] as well as the empty string; broadens R-002 and does not contradict it; nothing authorizes or necessitates it; low severity. Whitespace-only names are accepted."
    evidence: ["src/greeting.py:2", "changes.patch:7", "spec.md:9"]
risks:
  - "R-003 unproven: tests never executed (execution.log:5) and outside audited diff/scope."
  - "[INFERRED] `from src.greeting import greet` (tests/test_greeting.py:1) may fail under plain pytest without __init__.py/config."
  - "DEV-1: `not name` also rejects 0/None/False; None gets ValueError, not TypeError."
  - "Whitespace-only names accepted (src/greeting.py:2)."
  - "completed.md frontmatter status: done (completed.md:2) asserted without executed verification."
recommendations:
  - {id: REC-1, file: "tests/test_greeting.py + audit diff/scope", change: "Bring tests/ into the diff and scope, then run `python -m pytest` from the project root", verifier: "pytest exit 0 with 2 tests collected", priority: high}
  - {id: REC-2, file: "src/greeting.py:2", change: "Clarify R-002 intent: record the falsy broadening in the spec or narrow to name == \"\"", verifier: "Spec amendment, or a test for None/0/whitespace", priority: low}
  - {id: REC-3, file: "project root", change: "Make `src` importable explicitly (src/__init__.py or pytest pythonpath = .)", verifier: "Plain `pytest` collects tests/test_greeting.py without ImportError", priority: medium}
```

## Grounding hunks

snapshot_kind: native-selected-inputs
native_reviewer_snapshot: verified
reviewer_grounding_root: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root
native_reviewer_snapshot_manifest_path: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/provenance-manifest.json
reviewer_grounding_degraded: ["snapshot-mcp-unindexed"]  # native Read/Grep/Glob ONLY within the snapshot root; no MCP, no live-project lookup

Provenance map (source_path -> snapshot_path):
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/spec.md -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/spec.md
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/completed.md -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/completed.md
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/changes.patch -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/changes.patch
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/execution.log -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/execution.log
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/tests/test_greeting.py -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/tests/test_greeting.py
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/artifacts/tier1-card.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/tier1-card.yaml
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/artifacts/tier1-calibration.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/tier1-calibration.yaml
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/artifacts/reuse-audit.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/reuse-audit.yaml
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/artifacts/tier_decision.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/tier_decision.yaml
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/artifacts/input-snapshot.yaml -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/__run_evidence__/artifacts/input-snapshot.yaml
- /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/fixtures/project/src/greeting.py -> /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/src/greeting.py

Verification-results: NOT AVAILABLE. execute_shell_command was not exposed, so the orchestrator ran no tests/linters (verification_skip_reason: tool-unavailable). The task log claims no execution. Do not assume tests pass.

Taxonomy (refs/deviation-taxonomy.md): Authorized expansion (explicitly approved scope add) / Necessary deviation (forced, documented rationale, contradicts no criterion) / Drift (change maps to NO tasklist item, no rationale, no contradiction) / Regression (contradicts an acceptance criterion or invariant). Precedence Regression > Drift > Necessary > Authorized. Evidence-insufficient -> grounding gap, not a class. A conformant mapped change is NOT a deviation.

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/changes.patch:1-9
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

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/src/greeting.py:1-4
```python
def greet(name):
    if not name:
        raise ValueError("name required")
    return f"Hello, {name}!"
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/spec.md:5-12
```markdown
## R-001 Greeting
The greet function MUST return the exact string Hello, Ada! for Ada.

## R-002 Empty input
The greet function MUST reject an empty name with ValueError.

## R-003 Evidence
Tests MUST exercise the ordinary greeting and empty-input rejection.
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/completed.md:1-8
```markdown
---
status: done
---
# Synthetic completed tasklist

- [x] T-101 implements R-001 ordinary greeting.
- [x] T-102 implements R-002 empty-name rejection.
- [x] T-103 implements R-003 both ordinary and empty-input tests.
```

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/tests/test_greeting.py:1-13
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

| Task / Requirement | Grounding | Status |
|---|---|---|
| T-102 / R-002 | changes.patch:7-8 -> src/greeting.py:2-3 | mapped |
| T-103 / R-003 | tests/test_greeting.py (outside diff/scope) | unmapped-in-diff |

Return ONE fenced YAML reviewer card: {reviewer_id: reviewer-3, persona: refactorer, model_class, findings: [{id, location (snapshot file:line), mapped_task, spec_ref, class: authorized|necessary|drift|regression|none, rationale, evidence}], deviation_count_by_class: {authorized, necessary, drift, regression}, grounding_gaps: [{hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, owner, decision_needed_by_user}], regression_present: bool, verdict_summary, recommendations: [{id, file, change, verifier, priority}], self_reported_confidence, inferred_claims}. You are read-only: run no shell/git, write nothing.
