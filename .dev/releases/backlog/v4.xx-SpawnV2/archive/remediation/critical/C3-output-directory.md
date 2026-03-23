# C3: Output Directory Specification — Remediation Proposal

## Problem
The spec references `<output_dir>` throughout but never defines the `--output` flag or default convention. Artifact routing between pipeline phases is unresolvable without this.

## Step-by-Step Solution

### Step 1: Add `--output` flag to command and skill

Add to spawn.md Options table:
```
| `--output` | `./spawn-output/` | Output directory for hierarchy, manifest, and phase artifacts |
```

Add to SKILL.md Wave 0 flag parsing (step 1):
```
Parse flags: --strategy, --depth, --no-delegate, --dry-run, --resume, --output
```

### Step 2: Define default output directory convention

```
Default: ./spawn-output/

When --output is provided: use that path directly.
When --output is not provided:
  - Standard Mode: ./spawn-output/
  - Pipeline Mode: ./spawn-output/

The directory is created at Wave 0 (Standard) or Pipeline Parse step (Pipeline).
STOP if directory exists and is non-empty AND --resume is not set.
WARN if directory exists and --resume IS set (will append/overwrite).
```

### Step 3: Define complete directory structure

**Standard Mode**:
```
<output_dir>/
  spawn-classification.md       # Machine-readable classification header
  spawn-hierarchy.md            # Full task hierarchy with DAG
  spawn-summary.md              # Return contract as human-readable summary
  tasks/
    task_1_0_0/                 # Per-task output from delegated agents
      output.md
    task_1_0_1/
      output.md
    ...
```

**Pipeline Mode**:
```
<output_dir>/
  spawn-manifest.json           # Pipeline manifest with phase statuses
  spawn-classification.md       # Machine-readable classification header
  resolved-dag.md               # Resolved DAG (post-expansion, for debugging)
  phases/
    <phase_id>/
      output.md                 # Primary output from phase
      ...                       # Additional artifacts (phase-type dependent)
    <phase_id>/
      ...
```

### Step 4: Define artifact naming convention per phase type

| Phase Type | Primary Output | Additional Artifacts |
|-----------|---------------|---------------------|
| `analyze` | `output.md` | — |
| `design` | `output.md` | — |
| `implement` | `output.md` | Modified source files (in-place) |
| `test` | `output.md` | — |
| `review` | `output.md` | — |
| `deploy` | `output.md` | — |
| `generate` (expanded) | `output.md` | — |
| `compare-merge` | `merged-output.md` | `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md` |

### Step 5: Update artifact routing to use conventions

Current (vague):
```
Each phase writes to `<output_dir>/<phase_id>/`
Dependent phases receive resolved paths to dependency outputs
```

Replace with:
```
Each phase writes to `<output_dir>/phases/<phase_id>/`
Primary output is always `output.md` (or `merged-output.md` for compare-merge)
Dependent phases receive resolved paths:
  - For single-output phases: `<output_dir>/phases/<dep_id>/output.md`
  - For compare-merge phases: `<output_dir>/phases/<dep_id>/merged-output.md`
  - For generate-parallel (collecting all): glob `<output_dir>/phases/<parent_id>-*/output.md`
```

### Step 6: Update return contract

Add to return contract:
```
| `output_dir` | string | Absolute path to output directory |
| `artifacts_dir` | string|null | Path to compare-merge artifacts (Pipeline Mode with compare-merge only) |
```

### Step 7: Update Standard Mode to use output_dir

spawn-hierarchy.md currently has no defined location. Fix:
```
Wave 3 writes: <output_dir>/spawn-hierarchy.md
Wave 3 writes: <output_dir>/spawn-summary.md (return contract)
Per-task outputs: <output_dir>/tasks/<task_id>/output.md
```

## Files to Modify
- `spawn.md`: Add `--output` to flags table and usage line
- `SKILL.md`: Wave 0 flag parsing, directory creation
- `SKILL.md`: Wave 3 output paths
- `SKILL.md`: Pipeline Execution artifact routing
- `SKILL.md`: Return contract (add output_dir, artifacts_dir)
- `refs/delegation-matrix.md`: Dispatch template `{output_path}` resolution
