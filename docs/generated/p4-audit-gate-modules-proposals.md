---
title: "P4: Audit Gate Modules (evidence_gate / manifest_gate) — Two Proposals"
date: 2026-03-25
status: draft
context: cli-unwired-components-audit recommended action
---

# P4: Decide Fate of evidence_gate.py and manifest_gate.py

## Problem Statement

`src/superclaude/cli/audit/evidence_gate.py` and `src/superclaude/cli/audit/manifest_gate.py` are fully implemented modules with clean APIs but zero production callers. They were designed for a V2 per-file classification audit pipeline that was never built. They do NOT fit into `cleanup_audit/` (different data model: `ClassificationResult` vs `CleanupAuditStep`).

### Key Constraints
- `evidence_gate.py` imports from `audit/classification.py` (`ClassificationResult`, `V2Action`, `V2Tier`)
- `manifest_gate.py` is standalone (takes `all_files`, `profiled_files`, `threshold`)
- Both have their own `GateResult` dataclasses — architecturally inconsistent with `pipeline/gates.py`'s `GateCriteria`/`gate_passed()` pattern
- Tests exist: `tests/audit/test_evidence_gate.py`, `tests/audit/test_manifest_gate.py`, `tests/audit/test_ac_validation.py`
- `cleanup_audit/` is a separate, live audit pipeline with its own gate system (`ALL_GATES`, `gate_passed()`)
- No V2 classification pipeline orchestrator exists

---

## Proposal A: Quarantine with Expiry — Preserve But Isolate

### Approach
Move both modules and their tests into a clearly marked `_quarantine/` subdirectory within `audit/`. Add a machine-readable expiry marker. If no V2 classification pipeline is built by the expiry date, a future cleanup audit will flag them for deletion. This preserves the implementation work while making the dead-code status explicit and time-bounded.

### Implementation Sketch

1. **Create `src/superclaude/cli/audit/_quarantine/`** directory with `__init__.py`
2. **Move files**:
   - `audit/evidence_gate.py` -> `audit/_quarantine/evidence_gate.py`
   - `audit/manifest_gate.py` -> `audit/_quarantine/manifest_gate.py`
3. **Move tests**:
   - `tests/audit/test_evidence_gate.py` -> `tests/audit/_quarantine/test_evidence_gate.py`
   - `tests/audit/test_manifest_gate.py` -> `tests/audit/_quarantine/test_manifest_gate.py`
4. **Add `_quarantine/README.md`**:
   ```markdown
   # Quarantined Modules — Expiry: 2026-06-25
   These modules were designed for a V2 classification audit pipeline that does not yet exist.
   If no pipeline integrates them by the expiry date, delete this directory.
   ```
5. **Update imports** in `test_ac_validation.py` if it references these modules.

### Risks Mitigated
- No code loss — implementation preserved for potential V2 pipeline
- Dead code is explicitly marked and time-bounded
- Wiring gate audit will no longer flag these as unwired (they're quarantined, not in the active tree)

### Risks Remaining
- Quarantine directories can become permanent if no one checks expiry
- Adds a new convention (`_quarantine/`) that other teams must understand
- Tests in quarantine still run in CI — wasted cycles on dead code

---

## Proposal B: Delete with Git Resurrection Contract

### Approach
Delete both modules and their tests now. Document the deletion in a lightweight "resurrection contract" file that records what was deleted, why, and the exact git commit hash to recover from. If a V2 classification pipeline is ever built, the contract provides a one-command recovery path.

### Implementation Sketch

1. **Delete source files**:
   - `src/superclaude/cli/audit/evidence_gate.py`
   - `src/superclaude/cli/audit/manifest_gate.py`
2. **Delete test files**:
   - `tests/audit/test_evidence_gate.py`
   - `tests/audit/test_manifest_gate.py`
3. **Update `test_ac_validation.py`** — remove any imports from deleted modules
4. **Create `.dev/resurrection-contracts/audit-v2-gates.md`**:
   ```markdown
   # Resurrection Contract: V2 Audit Gate Modules

   **Deleted**: 2026-03-25
   **Reason**: Zero production callers; designed for unbuilt V2 classification pipeline
   **Recovery commit**: <commit-hash-before-deletion>
   **Files**:
   - src/superclaude/cli/audit/evidence_gate.py
   - src/superclaude/cli/audit/manifest_gate.py
   - tests/audit/test_evidence_gate.py
   - tests/audit/test_manifest_gate.py

   **Recovery**:
   ```bash
   git show <commit>:src/superclaude/cli/audit/evidence_gate.py > src/superclaude/cli/audit/evidence_gate.py
   git show <commit>:src/superclaude/cli/audit/manifest_gate.py > src/superclaude/cli/audit/manifest_gate.py
   ```

   **When to resurrect**: When a V2 per-file classification pipeline with ClassificationResult
   flow is being built. These gates validate DELETE/KEEP evidence quality.
   ```

### Risks Mitigated
- Zero dead code in the active tree
- No CI cycles wasted on dead tests
- Clean audit report (wiring gate finds nothing unwired)
- Recovery is trivial via git

### Risks Remaining
- If git history is squashed or rebased, resurrection path breaks
- Resurrection contracts can be forgotten (same as quarantine expiry)
- Reimplementation may diverge from original if `ClassificationResult` schema changes before resurrection
- Small risk of deleting `test_ac_validation.py` imports incorrectly if tightly coupled
