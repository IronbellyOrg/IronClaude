# ISS-003 Refactoring Proposals

> **Issue**: `remediate_executor.py` listed as CREATE new module in the spec, but it already exists (v3.0), 563 lines, with snapshot create/restore/cleanup, `_DIFF_SIZE_THRESHOLD_PCT=50`, per-file diff checking, all-or-nothing rollback, ClaudeProcess remediation.

> **Overlapping HIGH issues**: ISS-004 (threshold 50->30), ISS-005 (per-file->per-patch granularity), ISS-006 (all-or-nothing->per-file rollback). All proposals below acknowledge these dependencies.

> **Ranked by**: minimal disruption > correctness > completeness

---

## Proposal #1: Reclassify to MODIFY with Surgical Delta List (RECOMMENDED)

**Strategy**: Keep FR-9 structure intact. Replace the implicit "create from scratch" framing with an explicit delta list that enumerates only what changes against the v3.0 baseline.

### Exact Spec Text Changes

**FR-9 Description block (lines 413-417)**

BEFORE:
```
**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than a configurable
percentage of the target file. Full document regeneration requires explicit
user consent.
```

AFTER:
```
**Description**: Extends the existing `remediate_executor.py` (v3.0, 563 lines)
to produce structured patches as MorphLLM-compatible lazy edit snippets instead
of its current freeform ClaudeProcess file rewrites. The existing per-file
diff-size guard is narrowed to per-patch granularity, the threshold is reduced
from 50% to 30%, and the all-or-nothing rollback is replaced with per-file
rollback. Full document regeneration requires explicit user consent.

**v3.0 Baseline** (already implemented -- DO NOT recreate):
- `create_snapshots()`, `restore_from_snapshots()`, `cleanup_snapshots()` (lines 53-101)
- `enforce_allowlist()` with `EDITABLE_FILES` constant (lines 109-153)
- `_run_agent_for_file()` / `_run_agent_with_retry()` via ClaudeProcess (lines 161-251)
- `_check_diff_size()` with `_DIFF_SIZE_THRESHOLD_PCT = 50` (lines 416-473)
- `execute_remediation()` orchestrator with parallel agents + rollback (lines 476-563)
- `_handle_failure()` -- all-or-nothing rollback (lines 259-294)
- `_handle_success()` -- snapshot cleanup (lines 302-328)
- `update_remediation_tasklist()` -- two-write model (lines 336-408)

**Delta from v3.0** (implementation work for v3.05):
1. Add `RemediationPatch` dataclass (MorphLLM lazy edit snippet format)
2. Add `apply_patches()` -- sequential per-file, per-patch diff guard
3. Add `fallback_apply()` -- deterministic text replacement with anchor matching
4. Add `check_morphllm_available()` -- MCP runtime probe
5. MODIFY `_DIFF_SIZE_THRESHOLD_PCT`: 50 -> 30 (ISS-004)
6. MODIFY `_check_diff_size()`: per-file -> per-patch granularity (ISS-005)
7. MODIFY `_handle_failure()`: all-or-nothing -> per-file rollback (ISS-006)
8. MODIFY `execute_remediation()`: integrate patch-based flow, per-file rollback
```

**Acceptance Criteria -- no change needed**. The existing AC list (lines 436-445) already describes the target state correctly. It says "per-patch diff-size guard" (not "create per-file guard"), "rollback is per-file" (not "create all-or-nothing rollback"), and threshold is 30%. The AC is future-state, not implementation-action.

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` (FR-9 Description block) | Replace description paragraph + add baseline/delta subsections |

### Risk: LOW

- Preserves all existing AC verbatim -- no acceptance criteria rewrite needed.
- Explicit baseline section prevents implementers from recreating existing code.
- Delta list directly maps to code changes, making task decomposition trivial.
- Does not alter FR-9.1 at all (already correctly specified).

### Requires Code Changes: YES (but only what the spec already demands)

- ISS-004: Change `_DIFF_SIZE_THRESHOLD_PCT = 50` to `30` at line 45.
- ISS-005: Refactor `_check_diff_size()` to operate on individual patches, not whole-file diffs.
- ISS-006: Refactor `_handle_failure()` to roll back only the failed file, not all files.
- New functions: `RemediationPatch`, `apply_patches()`, `fallback_apply()`, `check_morphllm_available()`.

These code changes are required regardless of which proposal is chosen -- the spec demands them. This proposal simply makes the spec honest about what already exists vs. what must change.

---

## Proposal #2: Split FR-9 into FR-9a (Baseline Acknowledgment) and FR-9b (New Behavior)

**Strategy**: Decompose FR-9 into two sub-requirements. FR-9a formally documents the v3.0 baseline as accepted/verified. FR-9b specifies only the new behavior delta. This is more disruptive than Proposal #1 but provides cleaner traceability for audit purposes.

### Exact Spec Text Changes

**Replace FR-9 header and description (lines 411-417) with:**

BEFORE:
```
### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than a configurable
percentage of the target file. Full document regeneration requires explicit
user consent.
```

AFTER:
```
### FR-9a: Remediation Executor Baseline (v3.0 -- Verified)

**Description**: The remediation executor (`remediate_executor.py`, 563 lines)
was implemented in v3.0. This sub-requirement formally acknowledges the existing
baseline and marks it as verified, preventing duplicate implementation.

**Verified Capabilities** (no implementation work):
- Snapshot lifecycle: `create_snapshots()`, `restore_from_snapshots()`, `cleanup_snapshots()`
- File allowlist enforcement: `enforce_allowlist()` with `EDITABLE_FILES`
- Parallel ClaudeProcess agent execution with timeout/retry
- Post-hoc per-file diff-size checking at 50% threshold
- All-or-nothing rollback on any agent failure
- Two-write tasklist outcome model

**Acceptance Criteria** (FR-9a):
- [ ] `remediate_executor.py` exists and is importable
- [ ] Snapshot create/restore/cleanup functions are present and tested
- [ ] ClaudeProcess agent execution path is functional

### FR-9b: Edit-Only Remediation with Per-Patch Diff-Size Guard

**Description**: Extends the v3.0 remediation executor to produce structured
patches as MorphLLM-compatible lazy edit snippets. Narrows the diff-size guard
from per-file to per-patch granularity, reduces the threshold from 50% to 30%,
and replaces all-or-nothing rollback with per-file rollback.
```

**Acceptance Criteria block (lines 435-445) -- move under FR-9b, unchanged.** The existing AC already describes the target state. No rewording needed.

**FR-9.1 (lines 447-466) -- becomes FR-9b.1, no content change.** Just renumber.

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` | Split FR-9 into FR-9a + FR-9b; renumber FR-9.1 to FR-9b.1 |
| Any document referencing "FR-9" | Update references to FR-9a/FR-9b as appropriate |

### Risk: MEDIUM

- Renumbering FR-9 to FR-9a/FR-9b may break references in other spec sections, the compatibility report, and any downstream tasklists that cite "FR-9".
- The FR-9 Dependencies line ("FR-6") and any backlinks from FR-6 to FR-9 need updating.
- FR-9a is essentially a no-op requirement (verified baseline), which may confuse reviewers expecting all FRs to represent work items.

### Requires Code Changes: YES (identical to Proposal #1)

Same code changes as Proposal #1. The split is spec-organizational only.

---

## Proposal #3: Add Global "v3.0 Baseline" Preamble Section, Minimally Patch FR-9

**Strategy**: Instead of modifying FR-9 heavily, add a new top-level section to the spec ("Section 0: v3.0 Baseline") that documents ALL pre-existing modules (convergence.py, semantic_layer.py, remediate_executor.py). Then add a single sentence to FR-9's description acknowledging it extends existing code. This addresses ISS-003 alongside ISS-001 and ISS-002 (the other two CREATE-vs-EXISTS conflicts) in one structural change.

### Exact Spec Text Changes

**Add new section before FR-1 (insert after the spec preamble):**

```
## Section 0: v3.0 Baseline -- Pre-Existing Modules

The following modules were implemented in v3.0 and MUST NOT be recreated.
All v3.05 requirements that reference these modules are MODIFY operations,
not CREATE operations.

| Module | Lines | Key Capabilities | v3.05 FRs That Extend It |
|--------|-------|-------------------|--------------------------|
| convergence.py | 323 | DeviationRegistry, convergence loop, temp-dir isolation, run-to-run memory | FR-7, FR-8, FR-10 |
| semantic_layer.py | 336 | Prompt budget, debate scoring, truncation | FR-4, FR-5 |
| remediate_executor.py | 563 | Snapshots, allowlist, parallel ClaudeProcess agents, diff-size guard (50%), all-or-nothing rollback | FR-9 |

Implementation instructions: Read each module before writing code. Use
`grep -n "def \|class "` to inventory existing functions. Only add or modify
functions listed in the relevant FR's delta section.
```

**FR-9 Description (lines 413-417) -- add one sentence:**

BEFORE:
```
**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than a configurable
percentage of the target file. Full document regeneration requires explicit
user consent.
```

AFTER:
```
**Description**: Extends the existing `remediate_executor.py` (see Section 0)
to produce structured patches as MorphLLM-compatible lazy edit snippets instead
of freeform file rewrites. The per-file diff-size guard is narrowed to per-patch
granularity with a reduced threshold (50% -> 30%), and rollback is changed from
all-or-nothing to per-file. Full document regeneration requires explicit user
consent.
```

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` | Add Section 0 preamble; patch FR-9, FR-4, FR-7 descriptions |

### Risk: MEDIUM

- Addresses ISS-001, ISS-002, ISS-003 simultaneously -- larger blast radius means more review surface.
- Section 0 could drift from reality if modules change before implementation begins. Needs a "verified at commit" annotation.
- Minimal change to FR-9 itself means implementers still need to read Section 0 carefully to understand what exists vs. what to build.

### Requires Code Changes: YES (identical to Proposal #1)

Same code changes. This proposal is purely about spec structure.

---

## Proposal #4: Replace FR-9 Description with Tabular Before/After Contract

**Strategy**: Replace the prose description with a structured table showing current state vs. target state for every function in `remediate_executor.py`. Most explicit approach but highest editorial effort.

### Exact Spec Text Changes

**Replace FR-9 Description block (lines 413-417) entirely:**

BEFORE:
```
**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than a configurable
percentage of the target file. Full document regeneration requires explicit
user consent.
```

AFTER:
```
**Description**: Modify `remediate_executor.py` (v3.0) per the following contract:

| Function / Constant | v3.0 State | v3.05 Target | Action |
|---------------------|-----------|--------------|--------|
| `_DIFF_SIZE_THRESHOLD_PCT` | `50` | `30` | MODIFY (ISS-004) |
| `_check_diff_size()` | Per-file comparison | Per-patch comparison against `RemediationPatch` | MODIFY (ISS-005) |
| `_handle_failure()` | All-or-nothing rollback of ALL files | Per-file rollback; only failed file restored | MODIFY (ISS-006) |
| `_handle_success()` | Marks all FIXED | Per-file success; partial success possible | MODIFY |
| `execute_remediation()` | Parallel ClaudeProcess agents, post-hoc diff check | Patch-based flow: generate patches -> validate -> apply | MODIFY |
| `RemediationPatch` | Does not exist | MorphLLM lazy edit snippet dataclass | CREATE |
| `apply_patches()` | Does not exist | Sequential per-file patch application with per-patch guard | CREATE |
| `fallback_apply()` | Does not exist | Deterministic text replacement (5-line/200-char anchor) | CREATE |
| `check_morphllm_available()` | Does not exist | MCP runtime probe for morphllm-fast-apply | CREATE |
| `create_snapshots()` | Exists, functional | No change | RETAIN |
| `restore_from_snapshots()` | Exists, functional | No change | RETAIN |
| `cleanup_snapshots()` | Exists, functional | No change | RETAIN |
| `enforce_allowlist()` | Exists, functional | No change | RETAIN |
| `_run_agent_for_file()` | Exists, ClaudeProcess | Potentially refactored to generate patches instead of direct edits | MODIFY |
| `_run_agent_with_retry()` | Exists, functional | Adapt to patch-based flow | MODIFY |
| `update_remediation_tasklist()` | Exists, functional | No change | RETAIN |

Full document regeneration requires explicit user consent (see FR-9.1).
```

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` (FR-9) | Replace description with before/after table |

### Risk: MEDIUM-HIGH

- Most verbose approach -- the table itself becomes a maintenance burden if the code evolves during implementation.
- Mixes spec-level requirements with implementation-level function names. This violates the spec's current abstraction level (other FRs don't name specific functions).
- Risk of the table becoming stale if refactoring changes function signatures.
- However, it is the most explicit and least ambiguous for implementers.

### Requires Code Changes: YES (identical to Proposal #1)

Same code changes. The table simply makes them maximally visible.

---

## Proposal #5: Minimal Patch -- Single Sentence + Footnote

**Strategy**: Absolute minimum disruption. Add one sentence to FR-9 and a footnote. Relies on the Compatibility Report for full context.

### Exact Spec Text Changes

**FR-9 Description (lines 413-414) -- prepend one sentence:**

BEFORE:
```
**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites.
```

AFTER:
```
**Description**: `remediate_executor.py` already exists (v3.0, 563 lines);
this requirement specifies MODIFICATIONS, not creation [^baseline-1].
Remediation is extended to produce structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites.
```

**Add footnote at end of FR-9 section (after line 467):**

```
[^baseline-1]: See CompatibilityReport-Merged.md Section 1 (Module Existence
Conflicts) and Section 3 (Modifications Needed) for full v3.0 baseline audit.
Key deltas: threshold 50->30% (ISS-004), per-file->per-patch granularity
(ISS-005), all-or-nothing->per-file rollback (ISS-006).
```

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` (FR-9) | Add 1 sentence + 1 footnote |

### Risk: LOW (but incomplete)

- Minimal editorial disruption -- two additions, zero deletions.
- Does NOT make the spec self-contained; requires reading the Compatibility Report alongside the spec.
- An implementer who reads only FR-9 might still miss the baseline inventory.
- Does not resolve ISS-004/005/006 inline -- defers to footnote cross-reference.

### Requires Code Changes: YES (identical to Proposal #1)

Same code changes. This proposal just acknowledges the conflict with minimal spec surgery.

---

## Summary Comparison

| # | Proposal | Disruption | Self-Contained | ISS-004/005/006 | Risk |
|---|----------|-----------|----------------|------------------|------|
| 1 | Reclassify + baseline/delta list | Low | Yes | Inline in description | LOW |
| 2 | Split FR-9a/FR-9b | Medium | Yes | Inline in FR-9b | MEDIUM |
| 3 | Global Section 0 preamble | Medium | Yes | Brief in FR-9 | MEDIUM |
| 4 | Tabular before/after contract | Medium-High | Yes | Per-function table | MEDIUM-HIGH |
| 5 | Single sentence + footnote | Minimal | No | Footnote reference | LOW (incomplete) |

**Recommendation**: Proposal #1. It is self-contained, low-disruption, preserves all existing acceptance criteria verbatim, and makes the ISS-004/005/006 deltas explicit without requiring renumbering or cross-document references. If ISS-001 and ISS-002 are being resolved simultaneously, consider Proposal #3 as a complement (add Section 0 for all three modules, then use Proposal #1's delta format within each FR).
