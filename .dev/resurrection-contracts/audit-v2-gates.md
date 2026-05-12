# Resurrection Contract: V2 Audit Gate Modules

**Deleted**: 2026-03-25
**Review-by**: 2026-06-25 (if no V2 pipeline exists by this date, close this contract)
**Reason**: Zero production callers; designed for unbuilt V2 per-file classification pipeline.
  Architecturally inconsistent with cleanup_audit/gates.py (GateCriteria/gate_passed() pattern).
  Dual GateResult dataclasses created namespace collision risk.
**Recovery commit**: 2b7c1f7

## Deleted Files
- src/superclaude/cli/audit/evidence_gate.py (86 lines, depends on classification.py)
- src/superclaude/cli/audit/manifest_gate.py (159 lines, standalone)
- tests/audit/test_evidence_gate.py
- tests/audit/test_manifest_gate.py

## Recovery Commands
```bash
git show 2b7c1f7:src/superclaude/cli/audit/evidence_gate.py > src/superclaude/cli/audit/evidence_gate.py
git show 2b7c1f7:src/superclaude/cli/audit/manifest_gate.py > src/superclaude/cli/audit/manifest_gate.py
git show 2b7c1f7:tests/audit/test_evidence_gate.py > tests/audit/test_evidence_gate.py
git show 2b7c1f7:tests/audit/test_manifest_gate.py > tests/audit/test_manifest_gate.py
```

## When to Resurrect
When a V2 per-file classification pipeline with ClassificationResult flow is being built
and needs evidence-quality gating for DELETE/KEEP actions. Before resurrecting, verify:
1. ClassificationResult schema in audit/classification.py has not diverged
2. The resurrected GateResult should be reconciled with pipeline/gates.py's GateCriteria
3. manifest_gate's exclusion patterns should be refreshed against current .gitignore

## When to Close
If no V2 classification pipeline is planned by the review-by date, delete this contract.
