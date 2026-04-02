---
title: "P4 Unified Proposal: Delete with Resurrection Contract + AC Validation Decoupling"
date: 2026-03-25
status: approved
winning-approach: "Proposal B (Delete with Git Resurrection Contract), augmented with Proposal A's expiry discipline"
---

# P4 Unified Proposal: evidence_gate.py and manifest_gate.py

## Adversarial Evaluation

### Proposal A: Quarantine with Expiry -- Strengths

1. **Zero code loss risk.** The implementation stays in the working tree, discoverable by anyone who browses the directory. No git archaeology required.
2. **Time-bounded discipline.** The expiry date creates a concrete decision point rather than an indefinite "maybe later."
3. **Tests remain runnable.** If someone does begin a V2 pipeline, the quarantined tests validate immediately without recovery steps.

### Proposal A: Quarantine with Expiry -- Weaknesses

1. **Quarantine is a euphemism for keeping dead code.** Moving files to `_quarantine/` does not remove them from the package -- they are still importable, still in `sys.modules` path, still consuming CI cycles. The audit problem is cosmetic, not structural.
2. **Introduces a novel convention.** No other subsystem uses `_quarantine/`. Every future contributor must learn this pattern. Convention proliferation is a maintenance tax.
3. **Expiry enforcement is manual.** There is no automation to flag expired quarantine directories. The README expiry date is aspirational, not enforceable. This is exactly the kind of soft process that decays silently.
4. **Test coupling persists.** `test_ac_validation.py` classes `TestAC4EvidenceDelete` and `TestAC5EvidenceKeep` import directly from `evidence_gate`. Moving to quarantine means updating these imports to `_quarantine.evidence_gate`, which creates a dependency on the quarantine directory existing -- the opposite of isolation.
5. **CI waste.** Quarantined tests still execute on every push. For modules with zero production callers, this is pure overhead.

### Proposal B: Delete with Git Resurrection Contract -- Strengths

1. **Clean slate.** Zero dead code in the active tree. Wiring gate, import analysis, and CI all benefit immediately.
2. **Git is the source of truth, not the filesystem.** The code already exists permanently in git history. A resurrection contract simply documents the recovery path -- it does not create new infrastructure.
3. **No novel conventions.** `.dev/resurrection-contracts/` is a documentation directory, not a code convention. It requires no tooling, no CI integration, no import path awareness.
4. **Forces intentional re-adoption.** If a V2 pipeline is built, the developer must consciously decide to resurrect and adapt these modules rather than accidentally depending on stale quarantined code whose `ClassificationResult` schema may have drifted.

### Proposal B: Delete with Git Resurrection Contract -- Weaknesses

1. **Git history fragility.** If the repository undergoes a squash-merge or history rewrite, the resurrection commit hash becomes invalid. (Mitigated: commit hashes in the contract can be updated, and the file paths are documented for `git log --all -- <path>` recovery.)
2. **Resurrection contracts can be forgotten.** Same decay risk as quarantine expiry dates -- a document that nobody checks. (Mitigated: these are in `.dev/`, which is the active release/operations directory, not a graveyard.)
3. **test_ac_validation.py coupling.** Four test methods in `TestAC4EvidenceDelete` and `TestAC5EvidenceKeep` import from `evidence_gate`. Deletion requires either removing these tests or decoupling them. The proposals document underspecifies this.

---

## Winner Selection

**Proposal B wins.** The core question is: should dead code live in the working tree or in git history? The answer is git history. Every argument for quarantine reduces to "someone might want this later" -- and git already solves that problem without maintaining phantom directories, novel conventions, or wasted CI cycles.

The critical weakness of Proposal B -- the `test_ac_validation.py` coupling -- is addressable and in fact reveals a separate design smell: acceptance-criterion tests should validate the AC semantics, not the specific gate function implementations. The unified proposal below addresses this.

Proposal A's one genuine strength -- the time-bounded expiry discipline -- is incorporated into the resurrection contract as a "review-by" date.

---

## Unified Final Proposal: Delete + Decoupled AC Tests + Review-By Contract

### Rationale

Delete both modules and their dedicated tests. Decouple `test_ac_validation.py` from the gate implementations by inlining the AC validation logic (the tests assert classification semantics, not gate function behavior). Document the deletion with a resurrection contract that includes a review-by date borrowed from Proposal A's expiry concept.

### Implementation Plan

#### Step 1: Decouple test_ac_validation.py (before deletion)

The four test methods in `TestAC4EvidenceDelete` and `TestAC5EvidenceKeep` currently import `check_delete_evidence` and `check_keep_evidence` from `evidence_gate`. These tests validate acceptance criteria AC4 and AC5 -- they should assert the *semantics* (DELETE requires zero-reference evidence, KEEP requires reference evidence) without depending on the gate module.

**Action:** Replace the `evidence_gate` imports in `test_ac_validation.py` with inline assertions against `ClassificationResult` fields directly. The AC tests should verify that:
- AC4: A `ClassificationResult` with `action=DELETE` has evidence containing zero-reference proof
- AC5: A `ClassificationResult` with `action=KEEP` and `tier in (TIER_1, TIER_2)` has reference evidence

This preserves the AC validation coverage while removing the gate dependency. The `ClassificationResult` dataclass (from `audit/classification.py`) remains a live, wired module.

```python
# Before (coupled to evidence_gate):
from superclaude.cli.audit.evidence_gate import check_delete_evidence
gate = check_delete_evidence(result)
assert gate.passed is True

# After (tests AC semantics directly):
assert result.action == V2Action.DELETE
assert any("zero" in e.lower() and "ref" in e.lower() for e in result.evidence), \
    f"AC4 violation: DELETE for {result.file_path} lacks zero-reference evidence"
```

#### Step 2: Delete source and test files

Remove:
- `src/superclaude/cli/audit/evidence_gate.py`
- `src/superclaude/cli/audit/manifest_gate.py`
- `tests/audit/test_evidence_gate.py`
- `tests/audit/test_manifest_gate.py`

#### Step 3: Create resurrection contract

Create `.dev/resurrection-contracts/audit-v2-gates.md`:

```markdown
# Resurrection Contract: V2 Audit Gate Modules

**Deleted**: 2026-03-25
**Review-by**: 2026-06-25 (if no V2 pipeline exists by this date, close this contract)
**Reason**: Zero production callers; designed for unbuilt V2 per-file classification pipeline.
  Architecturally inconsistent with cleanup_audit/gates.py (GateCriteria/gate_passed() pattern).
  Dual GateResult dataclasses created namespace collision risk.
**Recovery commit**: <commit-hash-of-commit-before-deletion>

## Deleted Files
- src/superclaude/cli/audit/evidence_gate.py (86 lines, depends on classification.py)
- src/superclaude/cli/audit/manifest_gate.py (159 lines, standalone)
- tests/audit/test_evidence_gate.py
- tests/audit/test_manifest_gate.py

## Recovery Commands
git show <commit>:src/superclaude/cli/audit/evidence_gate.py > src/superclaude/cli/audit/evidence_gate.py
git show <commit>:src/superclaude/cli/audit/manifest_gate.py > src/superclaude/cli/audit/manifest_gate.py
git show <commit>:tests/audit/test_evidence_gate.py > tests/audit/test_evidence_gate.py
git show <commit>:tests/audit/test_manifest_gate.py > tests/audit/test_manifest_gate.py

## When to Resurrect
When a V2 per-file classification pipeline with ClassificationResult flow is being built
and needs evidence-quality gating for DELETE/KEEP actions. Before resurrecting, verify:
1. ClassificationResult schema in audit/classification.py has not diverged
2. The resurrected GateResult should be reconciled with pipeline/gates.py's GateCriteria
3. manifest_gate's exclusion patterns should be refreshed against current .gitignore

## When to Close
If no V2 classification pipeline is planned by the review-by date, delete this contract.
```

#### Step 4: Verify

- Run `uv run pytest tests/audit/test_ac_validation.py -v` to confirm decoupled AC tests pass
- Run `uv run pytest tests/audit/ -v` to confirm no import errors from deleted modules
- Wiring gate should no longer flag evidence_gate or manifest_gate as unwired

### Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Git history rewrite invalidates commit hash | Low | Contract documents file paths; `git log --all -- <path>` always works |
| ClassificationResult schema drifts before resurrection | Medium | Contract includes verification checklist; drift is actually an argument *for* rewriting rather than resurrecting stale code |
| test_ac_validation decoupling introduces subtle behavior change | Low | The inline assertions replicate the exact same logic from evidence_gate.py; the check functions were simple string matching |
| Resurrection contract forgotten | Low | Review-by date in contract; `.dev/` is actively maintained release directory |

### Files Modified

| File | Action |
|------|--------|
| `src/superclaude/cli/audit/evidence_gate.py` | DELETE |
| `src/superclaude/cli/audit/manifest_gate.py` | DELETE |
| `tests/audit/test_evidence_gate.py` | DELETE |
| `tests/audit/test_manifest_gate.py` | DELETE |
| `tests/audit/test_ac_validation.py` | EDIT (decouple AC4/AC5 tests from evidence_gate imports) |
| `.dev/resurrection-contracts/audit-v2-gates.md` | CREATE |
