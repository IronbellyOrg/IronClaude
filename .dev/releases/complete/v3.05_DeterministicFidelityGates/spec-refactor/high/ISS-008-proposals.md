# ISS-008: deviation_registry.py listed as new file but class exists inside convergence.py — Proposals

## Issue Summary

The spec's YAML frontmatter (line 19) lists `src/superclaude/cli/roadmap/deviation_registry.py` in the `relates_to` manifest, implying it is a standalone file to be created. FR-6 describes a "Deviation Registry" as a component. However, the `DeviationRegistry` class (with full lifecycle: load/save/merge, stable IDs, run metadata, prior findings summary) already exists as a 176-line class (lines 50-225) inside `convergence.py`. No standalone `deviation_registry.py` file exists anywhere in the codebase.

## CRITICAL Dependency Check

**ISS-001** (convergence.py CREATE-to-MODIFY) directly affects this issue. DeviationRegistry lives inside convergence.py, which ISS-001 already addresses by reclassifying convergence.py from CREATE to MODIFY. The ISS-001 recommended approach (Proposals #1 + #2 + #3) includes a frontmatter `module_disposition` table that lists convergence.py as `action: MODIFY` but does **not** address `deviation_registry.py` as a separate line item in `relates_to`.

**Dependency**: ISS-001 resolution must be applied first (or simultaneously). Whichever ISS-008 proposal is chosen, it must be consistent with ISS-001's final disposition of convergence.py. If ISS-001 Proposal #3 is adopted (frontmatter disposition table), ISS-008's resolution should either add a `deviation_registry.py` entry with `action: REMOVE_FROM_MANIFEST` or handle it within the convergence.py entry.

## Codebase Ground Truth

**File**: `src/superclaude/cli/roadmap/convergence.py` (323 lines total)

`DeviationRegistry` class spans lines 50-225 (176 lines). It includes:

| Method / Property | Lines | Purpose |
|---|---|---|
| `load_or_create()` | 62-82 | Classmethod: load existing registry or create fresh; resets on spec_hash change (FR-6) |
| `begin_run()` | 84-94 | Start a new run, return run_number |
| `merge_findings()` | 96-153 | Merge structural + semantic findings; mark missing as FIXED; update split HIGH counts |
| `get_active_highs()` | 154-159 | Return active HIGH findings |
| `get_active_high_count()` | 161-163 | Gate evaluation: count of active HIGHs |
| `get_structural_high_count()` | 165-170 | Monotonic enforcement: structural HIGHs only |
| `get_semantic_high_count()` | 172-177 | Informational: semantic HIGHs |
| `get_prior_findings_summary()` | 179-192 | FR-10 run-to-run memory for semantic prompt |
| `update_finding_status()` | 194-197 | Set FIXED/FAILED/SKIPPED |
| `record_debate_verdict()` | 199-211 | Record adversarial debate outcome, apply downgrade |
| `save()` | 213-225 | Atomic write via tmp + os.replace() |

Other convergence.py contents that co-locate with DeviationRegistry:
- `compute_stable_id()` (lines 24-32) — used exclusively by DeviationRegistry
- `RunMetadata` dataclass (lines 36-46) — dead code, never instantiated
- `ConvergenceResult` dataclass (lines 228-237) — convergence loop outcome
- `_check_regression()` (lines 240-272) — operates on registry data
- Temp dir isolation functions (lines 275-323) — FR-8 support

The class is tightly coupled with convergence.py's other components: `_check_regression()` takes a `DeviationRegistry` parameter, and the convergence loop (yet to be built) will orchestrate the registry.

**No imports of `deviation_registry` exist anywhere in the codebase** — all code imports from `convergence.py`.

---

## Proposal A: Remove deviation_registry.py from Manifest — Accept Current Location

### Approach
Accept that DeviationRegistry living inside convergence.py is the correct architecture. Remove `deviation_registry.py` from the spec's `relates_to` list. Add a note in FR-6 clarifying that the registry is implemented as a class within convergence.py, not as a standalone module.

### Before (Current Spec Text)

Frontmatter `relates_to` (line 19):
```yaml
  - src/superclaude/cli/roadmap/deviation_registry.py
```

FR-6 description (lines 297-300):
```
**Description**: A persistent, file-backed registry of all findings across
runs within a release. Each run appends new findings, updates status of
existing ones. The gate evaluates registry state, not fresh-scan results.
```

### After (Proposed Spec Text)

Remove from frontmatter `relates_to`:
```yaml
  # deviation_registry.py removed — DeviationRegistry class lives in convergence.py:50-225
```

FR-6 description:
```
**Description**: A persistent, file-backed registry of all findings across
runs within a release, implemented as the `DeviationRegistry` class within
`convergence.py` (v3.0 pre-existing, lines 50-225). Each run appends new
findings, updates status of existing ones. The gate evaluates registry
state, not fresh-scan results.
```

### Trade-offs
**Pros**:
- Zero code changes required — reflects actual codebase architecture
- Smallest edit surface (2 locations: frontmatter + FR-6 description)
- Consistent with ISS-001 which already reclassifies convergence.py as MODIFY
- Co-location keeps `compute_stable_id()`, `_check_regression()`, and `DeviationRegistry` together — they are tightly coupled
- If ISS-001 Proposal #3 is adopted (frontmatter disposition table), `deviation_registry.py` simply disappears from the manifest

**Cons**:
- convergence.py is already 323 lines and will grow when `execute_fidelity_with_convergence()` and `handle_regression()` are added (ISS-001) — could become 500+ lines
- Single Responsibility Principle argument: the file implements both the registry (data layer) and the convergence engine (orchestration layer)

---

## Proposal B: Extract to Standalone File — Align Code with Spec Intent

### Approach
Create `deviation_registry.py` as the spec originally intended, by extracting `DeviationRegistry` and its helper `compute_stable_id()` from convergence.py. Update imports across the codebase. The spec's `relates_to` entry becomes correct as-is, but add a note in FR-6 that this is an extraction, not a greenfield build.

### Before (Current Spec Text)

Frontmatter `relates_to` (line 19):
```yaml
  - src/superclaude/cli/roadmap/deviation_registry.py
```

FR-6 description (lines 297-300):
```
**Description**: A persistent, file-backed registry of all findings across
runs within a release. Each run appends new findings, updates status of
existing ones. The gate evaluates registry state, not fresh-scan results.
```

### After (Proposed Spec Text)

Frontmatter `relates_to` unchanged (line 19 stays):
```yaml
  - src/superclaude/cli/roadmap/deviation_registry.py
```

FR-6 description:
```
**Description**: A persistent, file-backed registry of all findings across
runs within a release. The `DeviationRegistry` class and `compute_stable_id()`
helper are extracted from `convergence.py` (where they were co-located in v3.0)
into a dedicated `deviation_registry.py` module. Each run appends new findings,
updates status of existing ones. The gate evaluates registry state, not
fresh-scan results.

**Implementation Note**: This is a code extraction (EXTRACT, not CREATE).
The class already exists at convergence.py:50-225. The extraction moves
~200 lines (DeviationRegistry + compute_stable_id + RunMetadata) to a new
file; convergence.py then imports from deviation_registry.py.
```

### Trade-offs
**Pros**:
- Follows Single Responsibility Principle — registry (data) separated from convergence engine (orchestration)
- Keeps convergence.py focused on orchestration, which will grow with `execute_fidelity_with_convergence()` and `handle_regression()`
- Spec's original `relates_to` entry becomes literally correct
- Makes DeviationRegistry independently testable and importable

**Cons**:
- Requires actual code changes (file extraction + import updates) that are not part of v3.05's functional requirements — this is refactoring overhead
- Creates a merge risk: if other branches are editing convergence.py simultaneously, the extraction creates conflicts
- Adds a new import dependency: convergence.py must `from .deviation_registry import DeviationRegistry, compute_stable_id`
- ISS-001 resolution must account for this: the frontmatter disposition table would need both `deviation_registry.py: CREATE (extract)` and `convergence.py: MODIFY (reduce + extend)`
- `_check_regression()` in convergence.py takes `DeviationRegistry` as a parameter — the coupling remains even after extraction

---

## Proposal C: Hybrid — Keep Current Location, Add Re-export Module

### Approach
Create `deviation_registry.py` as a thin re-export module that imports from convergence.py and re-exports. This makes the spec's `relates_to` entry technically valid without moving any code. FR-6 documents that the implementation lives in convergence.py with a public API re-exported through deviation_registry.py.

### Before (Current Spec Text)

Frontmatter `relates_to` (line 19):
```yaml
  - src/superclaude/cli/roadmap/deviation_registry.py
```

FR-6 description (lines 297-300):
```
**Description**: A persistent, file-backed registry of all findings across
runs within a release. Each run appends new findings, updates status of
existing ones. The gate evaluates registry state, not fresh-scan results.
```

### After (Proposed Spec Text)

Frontmatter `relates_to` unchanged (line 19 stays):
```yaml
  - src/superclaude/cli/roadmap/deviation_registry.py
```

FR-6 description:
```
**Description**: A persistent, file-backed registry of all findings across
runs within a release. The `DeviationRegistry` class is implemented within
`convergence.py` (v3.0 pre-existing, lines 50-225) and re-exported via
`deviation_registry.py` for public API clarity. Each run appends new findings,
updates status of existing ones. The gate evaluates registry state, not
fresh-scan results.

**Module Structure**: `deviation_registry.py` re-exports `DeviationRegistry`
and `compute_stable_id` from `convergence.py`. Internal callers may import
from either module; external callers should use `deviation_registry.py`.
```

The re-export file would contain:
```python
"""Public API for the deviation registry (FR-6).

Implementation lives in convergence.py for co-location with convergence
engine internals. This module provides the stable import path.
"""
from .convergence import DeviationRegistry, compute_stable_id

__all__ = ["DeviationRegistry", "compute_stable_id"]
```

### Trade-offs
**Pros**:
- Spec's `relates_to` becomes literally valid without moving code
- Provides a stable import path for external consumers
- Zero risk to existing code — no lines are moved or modified
- Future extraction (Proposal B) remains possible without breaking imports

**Cons**:
- Adds indirection — two files for one class, which is confusing
- The re-export module is ~8 lines of boilerplate with no real logic
- Violates "don't create unnecessary files" principle
- Consumers could still import from convergence.py directly, defeating the purpose
- Doesn't actually solve the SRP concern — convergence.py remains large

---

## Recommended Proposal

**Proposal A (Remove from manifest, accept current location)** is recommended for the following reasons:

1. **Zero code changes**: This is a spec-refactoring exercise, not a code-refactoring exercise. The goal is to make the spec accurately describe reality, not to reshape reality to match spec assumptions.

2. **ISS-001 consistency**: ISS-001 already reclassifies convergence.py as MODIFY. Proposal A naturally extends this by removing the phantom `deviation_registry.py` entry. If ISS-001 Proposal #3 (frontmatter disposition table) is adopted, `deviation_registry.py` simply does not appear in the table.

3. **Tight coupling justifies co-location**: `compute_stable_id()`, `_check_regression()`, and `DeviationRegistry` form a cohesive unit. The convergence loop orchestrator (yet to be built) will be the primary consumer of DeviationRegistry. Separating them would create artificial boundaries across tightly coupled code.

4. **File size is manageable**: Even after adding `execute_fidelity_with_convergence()` and `handle_regression()`, convergence.py will likely be ~500 lines — well within acceptable single-module size for Python.

5. **Proposal B can be done later**: If convergence.py grows beyond 600-700 lines during implementation, extraction can be done as a follow-up refactor without any spec changes (since Proposal A documents the class's location, not its module boundary).

**If ISS-001 Proposal #3 is adopted** (frontmatter disposition table), add this to resolve ISS-008 simultaneously:
```yaml
module_disposition:
  # ... (ISS-001 entries) ...
  - file: src/superclaude/cli/roadmap/deviation_registry.py
    action: REMOVE_FROM_MANIFEST
    note: "DeviationRegistry class lives in convergence.py:50-225. No standalone file needed."
```
