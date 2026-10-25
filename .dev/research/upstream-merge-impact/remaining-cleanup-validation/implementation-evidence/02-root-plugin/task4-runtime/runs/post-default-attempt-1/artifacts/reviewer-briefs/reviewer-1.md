<!-- reviewer-1: persona=analyzer; model slot=sonnet; agent type=sc:reflect-reviewer; mode=post (UC-2); lens: root-cause / deviation-classification lens: re-derive the class of every divergence from scratch; challenge the T1 card where wrong. -->

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
grounding_gaps:
  - hunk_ref: "T-103 / R-003: tests/test_greeting.py (whole file)"
    evidence_missing: "Test file is not in changes.patch (changes.patch:1-9 covers only src/greeting.py); it is untracked, the repo has no commits, it is outside --scope src/; no execution record (execution.log:5)."
    why_not_classifiable: "Cannot determine from the supplied diff whether the test file belongs to the audited change set; it is a required deliverable (completed.md:8) that is missing from the diff evidence, and passing behavior is unobserved."
    next_evidence_needed: "Include tests/ in the diff or scope, and run the suite with verification available."
    owner: user
    decision_needed_by_user: true
  - hunk_ref: "tests/test_greeting.py:1 (from src.greeting import greet)"
    evidence_missing: "No src/__init__.py, tests/__init__.py, conftest.py or pytest configuration present."
    why_not_classifiable: "[INFERRED] Resolves as a namespace package only if the project root is on sys.path; cannot be resolved by reading alone."
    next_evidence_needed: "Run the tests from the project root, or add pytest pythonpath config / __init__.py."
    owner: reviewer
    decision_needed_by_user: false
regression_candidates: []
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

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-default-attempt-1/artifacts/reviewer-snapshot/root/execution.log:1-5
```text
Synthetic completed-work log, not an execution claim about product code.
T-101 R-001: created src/greeting.py.
T-102 R-002: empty names raise ValueError.
T-103 R-003: created tests/test_greeting.py with ordinary and empty-name cases.
No test execution is claimed; inspect these files independently.
```

## Coverage slice

| Task / Requirement | Grounding | Status |
|---|---|---|
| T-101 / R-001 | changes.patch:6-9 -> src/greeting.py:4 | mapped |
| T-102 / R-002 | changes.patch:7-8 -> src/greeting.py:2-3 | mapped (DEV-1 classification disputed by T1 calibrator: Drift requires an UNMAPPED change) |

Return ONE fenced YAML reviewer card: {reviewer_id: reviewer-1, persona: analyzer, model_class, findings: [{id, location (snapshot file:line), mapped_task, spec_ref, class: authorized|necessary|drift|regression|none, rationale, evidence}], deviation_count_by_class: {authorized, necessary, drift, regression}, grounding_gaps: [{hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, owner, decision_needed_by_user}], regression_present: bool, verdict_summary, recommendations: [{id, file, change, verifier, priority}], self_reported_confidence, inferred_claims}. You are read-only: run no shell/git, write nothing.
