# ISS-022: Spec language uses "create" for modules that need "extend"

**Issue**: FR-4, FR-7, FR-8, FR-9 descriptions read as greenfield — no acknowledgment of pre-existing code in `convergence.py`, `semantic_layer.py`, or `remediate_executor.py`.

**Source**: Compatibility Report Section 8, Priority 1

**Note on actual spec text**: Despite the issues-classified summary saying the spec uses "Create new" / "build module," the actual FR descriptions do NOT contain those literal phrases. The problem is subtler: the descriptions use neutral language ("The fidelity gate evaluates...", "Remediation produces...") that implies building from scratch by omitting any reference to existing code. The only literal "build" is in FR-4.1 line 210 ("Build prosecutor prompt"), which is an action step in a protocol, not a module creation instruction.

---

## Status Check

**Superseded by upstream? PARTIALLY.**

| FR Section | Covered By | What ISS-001/002/003 Fix | What Remains for ISS-022 |
|------------|-----------|--------------------------|--------------------------|
| FR-4 | ISS-002 (CRITICAL) | Adds "Existing baseline" paragraph, marks acceptance criteria `[x]`, adds `validate_semantic_high()` / `run_semantic_layer()` acknowledgment | **Nothing** — ISS-002 fully addresses FR-4's create-vs-extend language |
| FR-7 | ISS-001 (CRITICAL) | Adds "extends existing convergence engine" to description, documents v3.0 baseline components | **Nothing** — ISS-001 fully addresses FR-7's create-vs-extend language |
| FR-9 | ISS-003 (CRITICAL) | Adds "Extends the existing `remediate_executor.py`" to description, adds v3.0 Baseline and Delta sections | **Nothing** — ISS-003 fully addresses FR-9's create-vs-extend language |
| **FR-8** | **None** | **Not covered by any CRITICAL issue** | **FR-8 describes temp dir isolation and parallel agents without acknowledging that `convergence.py` already implements temp dir isolation + atexit cleanup (lines 278-323)** |

**Conclusion**: ISS-001/002/003 fully cover FR-4, FR-7, and FR-9. The only remaining gap is **FR-8**, which describes regression detection infrastructure without acknowledging the existing temp dir isolation code in `convergence.py`.

---

## Proposal A: Add "extends existing" acknowledgment to FR-8 only

**Rationale**: Since ISS-001/002/003 already fix FR-4, FR-7, and FR-9, this proposal addresses the sole remaining gap: FR-8's description implies building temp dir isolation and parallel validation from scratch, when `convergence.py` already provides the temp dir isolation mechanism (lines 278-323: temp dir creation, file copying, atexit cleanup registration).

**Instances to fix**:

### FR-8

**Before** (lines 373-378):
> **Description**: When run N+1 has MORE **structural** HIGHs than run N
> (regression detected), the system spawns 3 parallel validation agents in
> isolated temporary directories. Each independently re-runs the fidelity check.
> Their findings are collected, merged by stable ID, deduplicated, sorted by
> severity, and written to a consolidated report. After consolidation, an
> adversarial debate validates the severity of each HIGH.

**After**:
> **Description**: When run N+1 has MORE **structural** HIGHs than run N
> (regression detected), the system extends the existing temp dir isolation
> mechanism in `convergence.py` (lines 278-323) to spawn 3 parallel validation
> agents in isolated temporary directories. Each independently re-runs the
> fidelity check. Their findings are collected, merged by stable ID,
> deduplicated, sorted by severity, and written to a consolidated report. After
> consolidation, an adversarial debate validates the severity of each HIGH.

**Before** (lines 380-384):
> **Isolation mechanism**: Each agent operates in its own temporary directory
> containing independent copies of all input files (spec, roadmap, registry
> snapshot). This replaces git worktrees because the files that need isolation
> (roadmap, registry) are output artifacts not tracked by git. Temp directories
> provide true input isolation at ~1.5MB vs ~150MB per worktree.

**After**:
> **Isolation mechanism**: Each agent operates in its own temporary directory
> containing independent copies of all input files (spec, roadmap, registry
> snapshot), reusing and extending the temp dir + atexit cleanup pattern already
> implemented in `convergence.py`. This replaces git worktrees because the files
> that need isolation (roadmap, registry) are output artifacts not tracked by
> git. Temp directories provide true input isolation at ~1.5MB vs ~150MB per
> worktree.

**Before** (lines 386-390):
> **Cleanup protocol**:
> 1. Primary: `finally` block in the orchestrator guarantees cleanup
> 2. Fallback: `atexit` handler registered after directory creation
> 3. Identification: directories use prefix `fidelity-validation-{session_id}-`
> 4. No git state pollution (no `.git/worktrees/` entries)

**After**:
> **Cleanup protocol** (extends existing `atexit` cleanup in `convergence.py:310-323`):
> 1. Primary: `finally` block in the orchestrator guarantees cleanup
> 2. Fallback: `atexit` handler registered after directory creation (pattern already in convergence.py)
> 3. Identification: directories use prefix `fidelity-validation-{session_id}-`
> 4. No git state pollution (no `.git/worktrees/` entries)

### FR-4, FR-7, FR-9

No changes needed — fully covered by ISS-001 (FR-7), ISS-002 (FR-4), ISS-003 (FR-9).

---

## Proposal B: Mark ISS-022 as fully superseded, close with no spec changes

**Rationale**: ISS-022 was classified before ISS-001/002/003 proposals were written. Now that those CRITICAL proposals exist and comprehensively address the "create vs extend" language for FR-4, FR-7, and FR-9, the question is whether FR-8's temp dir description is truly a "create vs extend" problem or simply a description of new behavior that happens to build on existing infrastructure.

**Argument for closing**: FR-8 describes the *regression detection and parallel validation* flow, which is genuinely new functionality. The temp dir isolation in `convergence.py` is an implementation detail that FR-8 can reasonably reuse without the spec needing to call it out — the spec describes desired behavior, not implementation lineage. The acceptance criteria (lines 392-405) are correct as-is. If ISS-001's Proposal #2 or #5 is adopted (which adds a baseline section listing all existing `convergence.py` capabilities including temp dir isolation), then FR-8 is implicitly covered by that baseline inventory.

**Risk**: If ISS-001 adopts only Proposal #1 (minimal reword) without a baseline section, then FR-8's temp dir description remains disconnected from the existing implementation. An implementer could rebuild the temp dir mechanism from scratch.

---

## Recommendation

**Adopt Proposal A** (FR-8 acknowledgment only), contingent on the outcome of ISS-001:

- If ISS-001 adopts **Proposal #2 or #5** (which include a baseline section listing temp dir isolation as existing code): Proposal B is acceptable — close ISS-022 as fully superseded.
- If ISS-001 adopts **Proposal #1** (minimal reword only): Proposal A is necessary to ensure FR-8 acknowledges the existing temp dir isolation code.

**Either way, ISS-022 is LOW severity and LOW risk.** The worst case (no fix) is that an implementer re-implements temp dir isolation that already exists — a minor duplication that would be caught in code review.
