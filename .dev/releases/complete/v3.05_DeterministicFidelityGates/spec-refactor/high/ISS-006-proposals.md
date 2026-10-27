# ISS-006: Rollback scope mismatch -- Proposals

> **Severity**: HIGH
> **Affected Spec**: FR-9 (Edit-Only Remediation with Diff-Size Guard)
> **Source**: CompatibilityReport-Merged.md Section 3 (Modifications Needed on Existing Code)

## Issue Summary

FR-9 specifies "Rollback is per-file (not all-or-nothing)" (acceptance criteria line 444) and "Existing snapshot/restore mechanism retained for per-file rollback" (line 445). However, the actual implementation in `remediate_executor.py` performs all-or-nothing rollback: when any single agent fails, `_handle_failure()` calls `restore_from_snapshots(all_target_files)` to roll back ALL files, shuts down the entire executor, and returns `("FAIL", failed_findings)`. There is no code path for partial success where some files are rolled back while others retain their remediation.

## CRITICAL Dependency Check

**ISS-003 (remediate_executor.py CREATE->MODIFY) MUST be applied first.**

ISS-003's recommended Proposal #1 already lists ISS-006 as delta item #7:
> `7. MODIFY _handle_failure(): all-or-nothing -> per-file rollback (ISS-006)`

ISS-003 reframes FR-9 from "create new module" to "extend existing module" and adds a baseline/delta structure to the spec. Any ISS-006 resolution must be written to fit within that delta structure, not conflict with it. If ISS-003 is applied as Proposal #1 (recommended), then ISS-006's spec changes are a refinement of delta item #7 -- adding the specific behavioral contract for per-file rollback.

**ISS-004 (threshold 50->30%) and ISS-005 (per-file->per-patch granularity) are siblings.** ISS-006 interacts with ISS-005 specifically: per-patch diff-size checking (ISS-005) determines which patches fail, and per-file rollback (ISS-006) determines the blast radius of that failure. Both must be designed together.

## Codebase Ground Truth

**File**: `src/superclaude/cli/roadmap/remediate_executor.py` (563 lines)

### Current rollback architecture

1. **Snapshot creation** (lines 53-78): `create_snapshots()` creates `.pre-remediate` copies for ALL target files before any agent runs. This is per-file granular -- each file gets its own snapshot. This mechanism is sound for per-file rollback.

2. **Snapshot restoration** (lines 81-92): `restore_from_snapshots()` iterates over a file list and restores each independently. Also per-file capable. No coupling between files.

3. **Failure handler** (lines 259-294): `_handle_failure()` is where the all-or-nothing behavior lives:
   - Takes `all_target_files` as input (not just the failed file)
   - Calls `executor.shutdown(wait=False, cancel_futures=True)` -- kills ALL pending agents
   - Calls `restore_from_snapshots(all_target_files)` -- restores ALL files, not just the failed one
   - Marks findings as FAILED for the failed file AND cross-file findings

4. **Main orchestrator** (lines 476-563): `execute_remediation()` processes agents via `as_completed()`. On first failure or diff-size violation, it calls `_handle_failure()` and immediately returns `("FAIL", ...)`. No partial success path exists.

5. **Success handler** (lines 302-328): `_handle_success()` only runs when ALL agents succeed. Cleans up ALL snapshots and marks everything FIXED. No partial success variant.

### Key insight

The snapshot primitives (`create_snapshots`, `restore_from_snapshots`, `cleanup_snapshots`) already operate per-file. The all-or-nothing behavior is entirely in the orchestration layer (`_handle_failure`, `execute_remediation`). Refactoring rollback scope requires changing the orchestrator, not the snapshot primitives.

## Proposal A: Per-File Rollback with Partial Success Orchestration

### Approach

Rewrite the `execute_remediation()` orchestrator to continue processing after individual file failures. Each file is independently evaluated: files whose agents succeed and pass the diff-size guard are kept; files whose agents fail are individually rolled back. The function returns a mixed result with per-file status.

This requires changing `_handle_failure()` to accept a single file (not all files), adding a new `_handle_partial_result()` function, and changing the return contract to support partial success.

### Before (Current Spec Text)

From FR-9 acceptance criteria (lines 435-445):
```
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file (not all-or-nothing)
- [ ] Existing snapshot/restore mechanism retained for per-file rollback
```

### After (Proposed Spec Text)

```
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file: when remediation fails for a specific file (agent failure, diff-size violation, or patch application error), only that file is restored from its snapshot; other files' remediations are preserved
- [ ] Partial success is a valid outcome: `execute_remediation()` returns per-file status (FIXED/FAILED) rather than a single binary PASS/FAIL
- [ ] Per-file failure does NOT halt the executor; remaining agents continue to completion
- [ ] Cross-file findings (findings whose `files_affected` spans multiple files) are marked FAILED only if ALL their affected files failed
- [ ] Existing snapshot/restore mechanism (`create_snapshots`, `restore_from_snapshots`, `cleanup_snapshots`) retained and used per-file; no changes to snapshot primitives
- [ ] After all agents complete: successful files have snapshots cleaned up; failed files have snapshots restored; mixed outcomes are logged with per-file summary
```

### Trade-offs

**Pros**:
- Maximizes remediation progress per convergence run -- partial fixes reduce HIGH count even when some files fail
- Aligns with the convergence model (FR-7): partial progress is better than zero progress when you have a 3-run budget
- Snapshot primitives already support per-file operation; minimal code change to the primitives
- Explicit partial-success return contract prevents ambiguity for callers

**Cons**:
- Changes the return contract of `execute_remediation()` from `("PASS"|"FAIL", findings)` to a more complex per-file result structure. All callers must be updated.
- Cross-file finding status is more complex -- need rules for when a finding spans files that have mixed outcomes
- Concurrent agent execution becomes more complex: currently, one failure halts everything; now each agent must complete independently
- Risk of inconsistent state if File A's remediation depends on File B's changes (cross-file coherence)

---

## Proposal B: Per-File Rollback with Fail-Fast on Cross-File Findings

### Approach

A conservative variant that adds per-file rollback for independent files but preserves fail-fast (all-or-nothing) behavior when files share cross-file findings. This limits the blast radius of per-file rollback to cases where it is provably safe.

The spec adds a "file independence check" step: before parallel execution, findings are analyzed for cross-file dependencies. Independent file groups get per-file rollback; dependent file groups get all-or-nothing rollback within their group.

### Before (Current Spec Text)

Same as Proposal A -- FR-9 acceptance criteria lines 435-445.

### After (Proposed Spec Text)

```
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file for independent files: when remediation fails for a file that shares no findings with other target files, only that file is restored from its snapshot
- [ ] Rollback is per-group for dependent files: files linked by cross-file findings form a rollback group; if any file in the group fails, all files in the group are rolled back
- [ ] File independence determined pre-execution by analyzing `finding.files_affected` across all findings: files sharing any finding are in the same rollback group
- [ ] Existing snapshot/restore mechanism retained for per-file and per-group rollback
- [ ] Overall result: PASS if all files succeed, PARTIAL if at least one independent file succeeds and at least one fails, FAIL if all files fail or any rollback group fails entirely
```

### Trade-offs

**Pros**:
- Safer than Proposal A: cross-file coherence is preserved by grouping dependent files
- Still provides per-file rollback benefit for the common case (most findings target a single file)
- Return contract extends cleanly: PASS/PARTIAL/FAIL is a superset of PASS/FAIL
- File grouping analysis is cheap (set intersection on `files_affected`)

**Cons**:
- More complex spec and implementation than Proposal A -- introduces rollback groups as a new concept
- In practice, if many findings are cross-file, the groups may collapse to a single large group and the behavior degenerates to all-or-nothing
- The PARTIAL return status requires callers to decide how to handle it (retry? continue? halt?)
- Adds pre-execution analysis step that slows the hot path

---

## Proposal C: Per-File Rollback with Sequential Execution Fallback

### Approach

Change the default behavior to per-file rollback with parallel execution, but add a sequential fallback mode for when the first parallel run produces mixed results. In sequential mode, files are processed one at a time; each file is committed (snapshot cleaned) or rolled back before the next begins. This eliminates cross-file coherence risks entirely.

The spec preserves the existing parallel-first architecture but changes the failure contract.

### Before (Current Spec Text)

Same as Proposal A -- FR-9 acceptance criteria lines 435-445.

### After (Proposed Spec Text)

```
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file (not all-or-nothing): when remediation fails for a specific file, only that file is restored from its snapshot; successfully remediated files are retained
- [ ] Parallel execution (default): all file agents run concurrently; after all complete, each file is independently evaluated -- successful files have snapshots cleaned up, failed files have snapshots restored
- [ ] Agent failure for one file does NOT cancel other running agents
- [ ] After parallel completion, cross-file coherence is checked: if any cross-file finding has mixed outcomes (some files FIXED, some FAILED), the FIXED files in that finding are also rolled back and the finding is marked FAILED
- [ ] Existing snapshot/restore mechanism retained; snapshot cleanup and restoration happen after ALL agents complete (not during execution)
- [ ] Return value includes per-file outcome map: `{file: "FIXED"|"FAILED"}` alongside aggregate status
```

### Trade-offs

**Pros**:
- Clean separation of concerns: parallel execution handles speed, post-execution coherence check handles correctness
- No pre-execution analysis needed (unlike Proposal B) -- cross-file coherence is checked after the fact
- Snapshot operations are deferred to after all agents complete, simplifying concurrency (no mid-execution snapshot restoration)
- Return contract is rich (per-file map) but aggregate status is still available for simple callers

**Cons**:
- Cross-file coherence check can retroactively roll back files that successfully remediated, which may surprise users
- "Successfully applied then rolled back" wastes the agent's work for that file
- All agents must complete before any rollback happens -- no early termination optimization
- Slightly more complex than Proposal A but simpler than Proposal B

---

## Recommended Proposal

**Proposal C: Per-File Rollback with Post-Execution Coherence Check.**

Rationale:

1. **Fits the convergence model**: FR-7 gives 3 runs to converge. Per-file rollback maximizes partial progress per run, reducing the number of active HIGHs and improving convergence odds. Proposal C achieves this while handling the cross-file case correctly via post-execution coherence.

2. **Minimal change to execution flow**: The parallel agent execution in `execute_remediation()` continues as-is. The change is in what happens AFTER agents complete: instead of all-or-nothing, each file is evaluated independently, then a coherence pass handles cross-file findings. This is less invasive than Proposal B's pre-execution grouping.

3. **CRITICAL dependency alignment**: ISS-003 Proposal #1 (recommended) lists delta item #7 as `MODIFY _handle_failure(): all-or-nothing -> per-file rollback`. Proposal C's implementation maps directly to this: replace `_handle_failure()` with a per-file evaluation pass plus coherence check, keeping the function signature compatible.

4. **Cross-file safety without complexity**: Proposal A ignores cross-file coherence. Proposal B adds pre-execution grouping complexity. Proposal C handles it with a simple post-execution pass that checks whether cross-file findings have mixed outcomes -- if so, roll back the successful files in that finding. This is correct, simple, and handles the edge case without over-engineering.

5. **ISS-005 compatibility**: Per-patch diff-size checking (ISS-005) produces per-patch pass/fail verdicts. If any patch for a file fails, that file is marked FAILED. This feeds naturally into Proposal C's per-file evaluation: the diff-size guard determines per-file outcome, and the coherence check handles cross-file implications.
