---
phase: 4
title: "Modifications to Existing Code"
tasks: 5
depends_on: [3]
parallelizable: true
---

# Phase 4: Modifications to Existing Code

All tasks modify existing files. All are independent within this phase and can execute in parallel.

---

### T12: Change diff-size threshold from 50% to 30%

**Tier**: simple
**File**: src/superclaude/cli/roadmap/remediate_executor.py, line 45
**FR**: FR-9
**Decision**: 30% per spec (adversarial-reviewed BF-5 decision — do not re-debate)

**Action**: Change `_DIFF_SIZE_THRESHOLD_PCT = 50` to `_DIFF_SIZE_THRESHOLD_PCT = 30`

**Acceptance criteria**:
- [ ] `_DIFF_SIZE_THRESHOLD_PCT = 30` at remediate_executor.py:45
- [ ] All 3 usage sites (lines 453, 458, 467) still reference the constant
- [ ] Existing tests pass with new threshold

---

### T13: Change diff-size granularity from per-file to per-patch

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/remediate_executor.py
**FR**: FR-9 (Resolved Q#4: per-patch, not per-file)

**Action**: The current diff-size guard evaluates `changed_lines / total_file_lines` at the file level. Change to evaluate each patch individually:

1. Read current guard logic (around lines 450-470)
2. Change from comparing file-level diff to per-patch diff
3. Each `RemediationPatch` (T18) has `original_code` and `update_snippet` — compute `changed_lines` from these
4. Guard formula: `patch_changed_lines / total_file_lines > threshold` per patch

**Acceptance criteria**:
- [ ] Each patch is individually evaluated against threshold
- [ ] A single large patch is rejected even if other patches for the same file are small
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry

---

### T14: Change rollback scope from all-or-nothing to per-file

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/remediate_executor.py
**FR**: FR-9

**Action**: Current rollback restores all files if any remediation fails. Change to per-file rollback:

1. Existing snapshot/restore mechanism (lines 53-101) already creates per-file snapshots
2. Change rollback logic: if a patch for file X fails, restore only file X
3. Patches for other files continue independently

**Acceptance criteria**:
- [ ] Failed patch restores only the affected file
- [ ] Successful patches for other files are preserved
- [ ] Existing snapshot/restore mechanism reused (not replaced)

---

### T15: Fix TRUNCATION_MARKER to include heading name

**Tier**: simple
**File**: src/superclaude/cli/roadmap/semantic_layer.py
**FR**: FR-4.2

**Action**: Find the truncation marker in `_truncate_to_budget()` and update it to include the section heading name:

Current: `[TRUNCATED: N bytes omitted]`
Required: `[TRUNCATED: N bytes omitted from '<heading>']`

**Acceptance criteria**:
- [ ] Truncation marker includes heading name
- [ ] Marker format matches FR-4.2 spec: `[TRUNCATED: N bytes omitted from '<heading>']`

---

### T16: Extend Finding dataclass with new fields

**Tier**: simple
**File**: src/superclaude/cli/roadmap/models.py
**FR**: FR-6

**Action**: Add 4 fields to the Finding dataclass:

```python
@dataclass
class Finding:
    # ... existing fields ...
    rule_id: str = ""           # FR-3 rule identifier
    spec_quote: str = ""        # Verbatim spec text this finding references
    roadmap_quote: str = ""     # Verbatim roadmap text (or "MISSING")
    stable_id: str = ""         # Computed via compute_stable_id()
```

Default empty strings preserve backward compatibility with existing serialized data.

**Acceptance criteria**:
- [ ] All 4 fields added with default values
- [ ] Existing code that creates Finding objects continues to work
- [ ] Pre-v3.05 registries (without these fields) load without error
