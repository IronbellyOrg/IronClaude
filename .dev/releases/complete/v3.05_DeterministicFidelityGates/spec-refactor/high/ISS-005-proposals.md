# ISS-005: Diff-size granularity mismatch -- Proposals

> **Source**: issues-classified.md ISS-005, CompatibilityReport-Merged.md Section 3
> **Affected Spec**: FR-9 (Edit-Only Remediation with Diff-Size Guard)
> **Severity**: HIGH

## Issue Summary

FR-9 specifies a **per-patch** diff-size guard: "reject individual patch if `changed_lines / total_file_lines > threshold`" (AC bullet 5, line 440). The current code in `remediate_executor.py` implements a **per-file** diff-size guard via `_check_diff_size()` (lines 416-473), which compares the entire `.pre-remediate` snapshot against the entire current file after all agent edits are applied. This means a single large edit can hide behind many small ones in the same file, and fine-grained rejection of individual oversized patches is impossible.

The spec also says "valid patches for the same file are applied sequentially (not batched)" (AC bullet 7, line 442), which implies an individual-patch evaluation model that does not exist in the current code. The current flow is: ClaudeProcess edits the whole file freely, then a post-hoc whole-file diff check runs.

## CRITICAL Dependency Check

**ISS-003** (CRITICAL: remediate_executor.py listed as CREATE but already exists) **MUST be applied first**. ISS-003's recommended Proposal #1 restructures FR-9's description to include a "v3.0 Baseline" section and a "Delta from v3.0" list. That delta list already references ISS-005 as item 6: "MODIFY `_check_diff_size()`: per-file -> per-patch granularity." Any ISS-005 spec change must be consistent with whichever ISS-003 proposal is adopted.

Specifically:
- If ISS-003 Proposal #1 is adopted: ISS-005 changes should refine the delta list item and add detail to the Acceptance Criteria.
- If ISS-003 Proposal #2 (FR-9a/FR-9b split) is adopted: ISS-005 changes go into FR-9b.
- If ISS-003 Proposal #3 (global Section 0) is adopted: ISS-005 changes stay in FR-9 with the one-sentence patch.

**ISS-004** (threshold 50->30%) is a sibling issue that affects the same `_check_diff_size()` function but is independent -- the threshold value and the granularity are orthogonal concerns.

**ISS-006** (rollback scope: all-or-nothing -> per-file) is tightly coupled -- per-patch diff-size checking changes what "rejection" means, which directly affects rollback behavior.

## Codebase Ground Truth

**File**: `src/superclaude/cli/roadmap/remediate_executor.py` (563 lines)

**Current `_check_diff_size()` (lines 416-473)**:
- Takes `target_file: str` and `allow_regeneration: bool`
- Reads the `.pre-remediate` snapshot and the current file
- Computes a line-level diff: `changed_lines / max(original_lines, current_lines) * 100`
- Compares against `_DIFF_SIZE_THRESHOLD_PCT = 50`
- Returns `True` (within threshold) or `False` (exceeds)

**Current call site in `execute_remediation()` (line 535)**:
- Called AFTER `_run_agent_for_file()` succeeds (exit_code == 0)
- Operates on the whole file post-edit, not on individual patches
- On failure: triggers `_handle_failure()` which rolls back ALL files

**Key gap**: There is no `RemediationPatch` dataclass, no `apply_patches()` function, and no mechanism to evaluate individual patches. The entire patch-based flow (generate -> validate per-patch -> apply sequentially) does not exist yet. Per-patch diff-size checking requires the patch infrastructure to exist first.

**No existing per-patch logic anywhere**: `grep -r "per.patch\|per_patch\|individual.*patch" src/superclaude/` returns zero matches in code files.

## Proposal A: Refine Existing AC with Explicit Per-Patch Algorithm

### Approach

Keep the existing FR-9 structure and Acceptance Criteria text. Add a new sub-section (FR-9.2) that specifies the per-patch diff-size algorithm explicitly, making it clear that `_check_diff_size()` must be refactored from whole-file comparison to per-patch evaluation. This is additive -- no existing text is removed.

### Before (Current Spec Text)

FR-9 Acceptance Criteria, bullet 5 (line 440):
```
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
```

FR-9 Acceptance Criteria, bullet 7 (line 442):
```
- [ ] Valid patches for the same file are applied sequentially (not batched)
```

### After (Proposed Spec Text)

FR-9 Acceptance Criteria, bullet 5 (unchanged):
```
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
```

FR-9 Acceptance Criteria, bullet 7 (unchanged):
```
- [ ] Valid patches for the same file are applied sequentially (not batched)
```

New sub-section added after FR-9.1 (insert after line 466):
```
#### FR-9.2: Per-Patch Diff-Size Guard Algorithm

The existing `_check_diff_size()` function (v3.0) operates on whole-file
diffs post-edit. v3.05 replaces this with per-patch evaluation integrated
into the `apply_patches()` flow.

**v3.0 behavior** (to be replaced):
- ClaudeProcess edits the target file freely
- `_check_diff_size()` compares `.pre-remediate` snapshot vs current file
- Threshold applied to total file-level diff percentage

**v3.05 behavior** (target):
- Remediation agent produces `RemediationPatch` objects (one per finding)
- Before applying each patch, compute: `patch_changed_lines / total_file_lines`
- `patch_changed_lines` = number of lines in `update_snippet` that differ
  from corresponding lines in `original_code`
- `total_file_lines` = line count of the target file at time of evaluation
  (after any prior patches in the sequence have been applied)
- If ratio > `_DIFF_SIZE_THRESHOLD_PCT / 100`: reject this patch, mark
  finding FAILED, continue to next patch for this file
- If `--allow-regeneration`: log WARNING, apply patch anyway (per FR-9.1)

**Acceptance Criteria** (FR-9.2):
- [ ] `_check_diff_size()` refactored to accept a `RemediationPatch` and target file path
- [ ] Diff calculation uses patch-local changed lines, not whole-file diff
- [ ] Each patch is evaluated independently; rejection of one does not block others
- [ ] `total_file_lines` is recalculated after each successful patch application
- [ ] Rejected patches are logged with: patch finding_id, actual ratio, threshold
- [ ] Finding status set to FAILED for rejected patches in the deviation registry
```

### Trade-offs

**Pros**:
- Additive change -- no existing AC text modified, only clarified with a new sub-section
- Makes the algorithm explicit enough to implement without ambiguity
- Addresses the "hiding behind many small edits" risk called out in Resolved Question #4
- Compatible with any ISS-003 resolution (works alongside baseline/delta list, FR-9a/b split, or Section 0)

**Cons**:
- Adds a new sub-section (FR-9.2) which increases spec length
- The algorithm specification may be too prescriptive -- it names internal functions (`_check_diff_size`) which may not survive refactoring
- Does not address the fundamental architectural gap: the entire patch-based flow is new, and per-patch checking is a detail within that larger change

## Proposal B: Replace AC Bullet 5 with Implementation-Ready Contract

### Approach

Replace the terse one-line AC bullet with a multi-line contract that captures the full behavioral change: from post-hoc whole-file checking to inline per-patch validation within `apply_patches()`. This makes the AC self-documenting without adding a separate sub-section.

### Before (Current Spec Text)

FR-9 Acceptance Criteria, bullet 5 (line 440):
```
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
```

### After (Proposed Spec Text)

```
- [ ] Per-patch diff-size guard replaces v3.0's per-file guard:
  - Each `RemediationPatch` is evaluated individually before application
  - Guard metric: `len(changed_lines_in_patch) / total_file_lines > threshold` (default 30%)
  - `total_file_lines` = current line count of target file (updated after each applied patch)
  - Rejected patch: log finding_id + actual ratio + threshold; mark finding FAILED in registry; continue to next patch
  - Accepted patch: apply via MorphLLM or fallback applicator, then re-evaluate file line count for next patch
  - `--allow-regeneration` overrides rejection with WARNING (per FR-9.1)
  - v3.0's `_check_diff_size()` (whole-file snapshot comparison) is retired
```

### Trade-offs

**Pros**:
- Self-contained -- all behavioral detail in one AC bullet, no extra sub-section
- Explicitly calls out that the v3.0 `_check_diff_size()` whole-file approach is retired
- Preserves existing AC numbering (no new FR-9.2)
- Clear enough for implementation without being overly prescriptive about internal function names

**Cons**:
- Multi-line AC bullet is unusual for this spec's style (other bullets are single-line)
- Modifying an existing AC bullet (rather than adding) means the original text is lost -- harder to diff against v1.1.0
- Depends on `RemediationPatch` existing, which is a separate new-code item; if that changes, this AC must be updated too

## Proposal C: Defer to Patch Infrastructure -- Guard Becomes Apply-Time Invariant

### Approach

Rather than specifying per-patch diff-size checking as a standalone mechanism, define it as an invariant enforced within `apply_patches()`. The diff-size guard becomes a precondition on patch application, not a separate checking step. This aligns with the spec's existing statement that "valid patches for the same file are applied sequentially" (AC bullet 7) by making the guard part of the sequential application loop.

### Before (Current Spec Text)

FR-9 Acceptance Criteria, bullets 5-7 (lines 440-442):
```
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
```

### After (Proposed Spec Text)

```
- [ ] `apply_patches(file_path, patches, config) -> list[PatchResult]` applies patches sequentially with inline guard:
  - For each patch in order:
    1. Compute `patch_change_ratio = changed_lines_in_patch / current_file_lines`
    2. If `patch_change_ratio > threshold` (default 30%) AND NOT `allow_regeneration`: reject patch, record `PatchResult(status=FAILED, ratio=..., threshold=...)`, mark finding FAILED in registry, continue
    3. If `patch_change_ratio > threshold` AND `allow_regeneration`: log WARNING with finding_id + ratio + threshold, proceed to step 4
    4. Apply patch via MorphLLM (if available) or `fallback_apply()` (deterministic anchor match)
    5. On apply success: record `PatchResult(status=APPLIED)`, update `current_file_lines`
    6. On apply failure: record `PatchResult(status=FAILED)`, restore file from pre-patch state, continue
  - Return all `PatchResult` entries for upstream status aggregation
- [ ] v3.0's post-hoc per-file `_check_diff_size()` is removed; guard is now inline in `apply_patches()`
- [ ] Partial success is valid: some patches for a file may succeed while others are rejected
```

### Trade-offs

**Pros**:
- Most architecturally coherent -- the guard is not a separate post-hoc check but an integral part of the application loop
- Eliminates the awkward v3.0 pattern where edits happen freely and are checked after the fact
- Makes partial success explicit (some patches pass, others fail for the same file)
- Naturally integrates with ISS-006 (per-file rollback) since each patch failure is handled individually
- `PatchResult` provides structured output for upstream consumers (convergence gate, diagnostic reports)

**Cons**:
- Most disruptive to existing AC text -- replaces 3 bullets with a new structure
- Specifies `apply_patches()` function signature, which may be too prescriptive
- Introduces `PatchResult` concept not mentioned elsewhere in the spec (would need a data model addition)
- Tightly couples the guard to the application flow, making it harder to test the guard logic in isolation

## Recommended Proposal

**Proposal B** (Replace AC Bullet 5 with Implementation-Ready Contract).

Rationale:
1. **Right level of detail**: More explicit than the current one-liner but not as prescriptive as Proposal C's full function signature specification. It tells implementers what behavior to produce without dictating internal structure.
2. **Minimal disruption**: Modifies one AC bullet in-place. No new sub-sections (unlike A), no new data types introduced (unlike C).
3. **Explicitly retires v3.0 behavior**: The line "v3.0's `_check_diff_size()` (whole-file snapshot comparison) is retired" prevents any ambiguity about whether the old approach should coexist with the new one.
4. **ISS-003 compatible**: Works with any ISS-003 resolution. If ISS-003 Proposal #1 is adopted, the delta list item 6 ("MODIFY `_check_diff_size()`: per-file -> per-patch granularity") is fully elaborated by this AC change.
5. **ISS-006 alignment**: The "continue to next patch" behavior on rejection naturally supports per-file partial success, which is compatible with the per-file rollback ISS-006 requires.

**Application order**: ISS-003 resolution first (establishes the MODIFY framing), then ISS-005 Proposal B (refines the diff-size guard AC), then ISS-004 (threshold value is already captured in the AC as "default 30%").
