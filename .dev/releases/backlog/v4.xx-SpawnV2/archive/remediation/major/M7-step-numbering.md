# M7 Remediation Proposal — Pipeline Execution Step Numbering

## Issue

The `Pipeline Execution` section in `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md` currently contains duplicate numbering for step `3`:

- `3. DAG Construction`
- `3. Phase Dispatch`

This creates an invalid execution sequence and makes the procedure ambiguous for implementers and reviewers.

## Goal

Restore a single, strictly increasing step sequence for `Pipeline Execution` so the flow reads unambiguously from `1` through `6`.

## Exact Renumbering

The remediation should preserve the existing step names and step content, and only correct the numbering as follows:

1. **Parse**
2. **Expand Dynamic Phases**
3. **DAG Construction**
4. **Phase Dispatch**
5. **Artifact Routing**
6. **Progress & Resume**

## Corrected Pipeline Execution Sequence

### Step 1 — Parse
- Parse inline shorthand or load YAML file
- Validate: no cycles in dependency graph
- Validate: all `depends_on` references exist
- If parse error: STOP with details

### Step 2 — Expand Dynamic Phases
- Before DAG construction
- For each `generate-parallel` phase: expand into N concrete phases from `--agents` list. STOP if `--agents` not provided.
- For each `compare-merge` phase: resolve `depends_on` references to expanded phase IDs (fan-in collection)
- Resolve `inherit` config values from CLI flags (`--depth`, etc.)
- Substitute `${prompt}` from `--prompt` CLI value. STOP if missing.
- Log resolved DAG for debugging (visible in `--dry-run`)

### Step 3 — DAG Construction
- Build execution graph from resolved phases
- Assign auto-IDs to inline phases (`phase_1`, `phase_2`, ...)
- Compute parallel groups from dependency structure
- Apply concurrency cap: `MAX_CONCURRENT = 10` (split oversized groups)
- If `--pipeline-seq`: force all phases into linear chain (one at a time)

### Step 4 — Phase Dispatch
- Execute phases respecting DAG + concurrency cap
- For each phase, construct Task prompt from phase definition
- Use delegation-matrix ref for agent type and model selection
- Dispatch phases in same parallel group concurrently (up to 10)
- Wait for all dependencies before dispatching dependent phases

### Step 5 — Artifact Routing
- Pass outputs between phases
- Each phase writes to `<output_dir>/<phase_id>/`
- Dependent phases receive resolved paths to dependency outputs
- Verify dependency output exists before dispatching consumer

### Step 6 — Progress & Resume
- Write manifest at `<output_dir>/spawn-manifest.json` with phase statuses
- `--pipeline-resume`: Read manifest, skip completed phases, resume from first incomplete phase
- Save checkpoints to Serena memory at phase-group boundaries

## Why This Renumbering Is Correct

- It preserves the existing logical order already implied by the section content.
- `Phase Dispatch` must follow `DAG Construction`, so it must be step `4`, not a second step `3`.
- `Artifact Routing` and `Progress & Resume` are downstream execution concerns and should shift to steps `5` and `6` respectively.
- No semantic redesign is required; this is a numbering correction only.

## Required Spec Change

Update the `Pipeline Execution` block in `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md` so the numbered list reads exactly:

1. **Parse**
2. **Expand Dynamic Phases**
3. **DAG Construction**
4. **Phase Dispatch**
5. **Artifact Routing**
6. **Progress & Resume**

## Acceptance Criteria

- The `Pipeline Execution` section contains exactly six top-level numbered steps.
- Each step number is unique and strictly increasing from `1` to `6`.
- The step names are exactly:
  - `Parse`
  - `Expand Dynamic Phases`
  - `DAG Construction`
  - `Phase Dispatch`
  - `Artifact Routing`
  - `Progress & Resume`
- Only numbering is changed; the existing step body text remains functionally unchanged.
- Reviewers can reference step numbers unambiguously in implementation and remediation work.

## Source References

- Spec section: `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md`
- Review note identifying the defect: `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec-panel-review.md`
