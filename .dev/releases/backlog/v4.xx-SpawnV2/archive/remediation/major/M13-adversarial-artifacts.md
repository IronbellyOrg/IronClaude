# M13 Remediation Proposal — Surface Adversarial Artifact Directory in Spawn Return Contract

## Issue

In `/sc:spawn` Pipeline Mode, the `compare-merge` phase delegates to `/sc:adversarial --compare`.

That downstream command produces a multi-artifact output set:
- `diff-analysis.md`
- `debate-transcript.md`
- `base-selection.md`
- `refactor-plan.md`
- `merge-log.md`
- `merged-output.md`

But the current `/sc:spawn` return contract only exposes:
- high-level orchestration fields, and
- `pipeline_manifest` for Pipeline Mode

This creates a visibility gap:
- consumers can reliably find the manifest,
- but they cannot reliably discover the full adversarial output bundle from the return contract itself,
- unless they already know the internal phase output layout and then traverse from `pipeline_manifest` to the relevant `compare-merge` phase `output_dir`.

That is the exact divergence called out in the panel review: one fan-in phase produces one primary output plus five supplementary artifacts, but spawn only advertises a single manifest path.

---

## Why This Is a Real Contract Problem

The current spec already treats Pipeline Mode as artifact-driven:
- each phase writes to `<output_dir>/<phase_id>/`
- the manifest records per-phase `output_dir`
- `compare-merge` is explicitly defined as a wrapper around `/sc:adversarial`

So the data exists.

The problem is discoverability and contract ergonomics.

A caller that wants to:
- inspect the debate transcript,
- review the merge rationale,
- archive all comparison evidence,
- or pass the full adversarial bundle to another command,

currently has to do all of the following:
1. read `pipeline_manifest`
2. parse manifest JSON
3. locate the `compare-merge` phase entry
4. extract `output_dir`
5. know that this directory contains the adversarial artifact set

That is too much hidden coupling for something the spec already knows is a first-class phase type.

---

## Proposed Resolution

Add an `artifacts_dir` field to `/sc:spawn`'s return contract and define it as the canonical entry point to the full adversarial artifact bundle when Pipeline Mode includes a `compare-merge` phase.

### Core rule

- `artifacts_dir` points to the directory containing the full artifact set produced by the most relevant pipeline output bundle.
- For M13 specifically, when the pipeline includes a terminal or consumer-relevant `compare-merge` phase, `artifacts_dir` MUST point to that phase's output directory.
- That directory is where consumers can access:
  - `merged-output.md`
  - `diff-analysis.md`
  - `debate-transcript.md`
  - `base-selection.md`
  - `refactor-plan.md`
  - `merge-log.md`

This preserves `pipeline_manifest` for full pipeline introspection while also giving consumers a direct, zero-guess path to the adversarial bundle.

---

## Why `artifacts_dir` Is Better Than Relying on `pipeline_manifest` Alone

### Option A — Keep current contract, document manifest traversal only
Rejected as the primary fix.

Why:
- It preserves unnecessary indirection.
- It forces every consumer to understand manifest internals.
- It leaks pipeline topology concerns into simple output consumption.
- It makes a common use case harder: “give me the compare-merge evidence bundle.”

This is acceptable as a fallback explanation, but not as the main contract.

### Option B — Add `artifacts_dir` and keep `pipeline_manifest`
Recommended.

Why:
- `pipeline_manifest` remains the full-fidelity orchestration record.
- `artifacts_dir` becomes the ergonomic consumption handle.
- The fix is additive and backward-compatible.
- It matches `/sc:adversarial`'s own return contract, which already exposes `artifacts_dir` directly.

### Option C — Replace `pipeline_manifest` with multiple artifact paths
Rejected.

Why:
- It overfits the contract to one phase type.
- It would bloat the spawn return contract with compare-merge-specific fields.
- A single directory handle is simpler and more extensible.

---

## Normative Behavior

### 1. Return contract addition

Add this field to the `/sc:spawn` return contract:

| Field | Type | Description |
|---|---|---|
| `artifacts_dir` | `string|null` | Canonical directory for the primary output artifact bundle. In Pipeline Mode with `compare-merge`, this is the compare-merge phase output directory containing merged output and supplementary adversarial artifacts. `null` when no such bundle exists. |

### 2. Population rule

#### Standard Mode
- `artifacts_dir = null`
- Reason: Standard Mode produces a task hierarchy and orchestration metadata, not a pipeline artifact bundle.

#### Pipeline Mode without `compare-merge`
- `artifacts_dir = null` by default
- `pipeline_manifest` remains the authoritative source for per-phase outputs.

This keeps the field semantically tight for the M13 problem instead of inventing a vague “some directory” meaning.

#### Pipeline Mode with `compare-merge`
- `artifacts_dir` MUST be set to the resolved output directory of the relevant `compare-merge` phase.
- That directory MUST contain the adversarial bundle.
- Consumers MUST be told to treat this directory as the public access point for the phase’s full output set.

### 3. Relevant phase selection rule

If more than one `compare-merge` phase exists, `/sc:spawn` MUST choose one deterministically.

Recommended rule:
- Use the last successfully completed `compare-merge` phase in topological execution order.

Rationale:
- It is deterministic.
- It usually corresponds to the pipeline’s most downstream merged result.
- It avoids returning a list when the contract only needs one canonical consumer entry point.

If no `compare-merge` phase completed successfully but one produced partial artifacts:
- set `artifacts_dir` to the last `compare-merge` phase that produced an output directory,
- and rely on `status` plus manifest phase status for success/failure interpretation.

This aligns with the adversarial protocol’s own “preserve artifacts on partial/failed runs” pattern.

---

## Consumer Access Model

The spec should explicitly document two supported access patterns.

### Fast path: direct bundle access

Use `artifacts_dir` when the caller wants the final compare-merge output bundle.

Example consumer logic:
1. Read spawn return contract.
2. If `artifacts_dir` is non-null, inspect files in that directory.
3. Use:
   - `merged-output.md` for the final merged deliverable
   - `debate-transcript.md` for adversarial reasoning
   - `merge-log.md` for execution provenance
   - `refactor-plan.md` for manual follow-up or audit

### Full-fidelity path: manifest traversal

Use `pipeline_manifest` when the caller needs:
- all phase outputs,
- non-compare-merge phase directories,
- status of failed/skipped phases,
- or complete pipeline reconstruction.

This cleanly separates:
- `artifacts_dir` = consumer-friendly primary bundle handle
- `pipeline_manifest` = orchestration internals and full graph state

---

## Spec Amendment Text

### A. Update the Return Contract section

In `.dev/releases/backlog/v4.xx-SpawnV2/spec.md`, update `## Return Contract` from:

```md
| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` \| `partial` \| `failed` |
| `task_hierarchy_path` | string | Path to written hierarchy document |
| `tasks_created` | int | Number of TaskCreate entries |
| `delegation_map` | object | Task ID → delegated `/sc:*` command |
| `parallel_groups` | list | Groups of tasks safe to run concurrently |
| `completion_summary` | object | Per-task status (completed/failed/manual) |
| `pipeline_manifest` | string\|null | Path to manifest (Pipeline Mode only) |
```

to:

```md
| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` \| `partial` \| `failed` |
| `task_hierarchy_path` | string | Path to written hierarchy document |
| `tasks_created` | int | Number of TaskCreate entries |
| `delegation_map` | object | Task ID → delegated `/sc:*` command |
| `parallel_groups` | list | Groups of tasks safe to run concurrently |
| `completion_summary` | object | Per-task status (completed/failed/manual) |
| `pipeline_manifest` | string\|null | Path to manifest (Pipeline Mode only) |
| `artifacts_dir` | string\|null | Canonical directory for the primary artifact bundle. In Pipeline Mode with `compare-merge`, this points to the compare-merge output directory containing `merged-output.md` plus supplementary adversarial artifacts. Otherwise null. |
```

### B. Add a consumer guidance note immediately after the table

```md
**Consumer access rule**:
- Use `artifacts_dir` when you want the final compare-merge artifact bundle directly.
- Use `pipeline_manifest` when you need full pipeline execution detail or need to inspect all phase output directories.

For `compare-merge`, `artifacts_dir` contains:
- `merged-output.md`
- `diff-analysis.md`
- `debate-transcript.md`
- `base-selection.md`
- `refactor-plan.md`
- `merge-log.md`
```

### C. Clarify compare-merge output semantics in Pipeline Execution / Artifact Routing

Add a note near the existing artifact routing rules:

```md
**compare-merge output convention**:
A `compare-merge` phase writes the full adversarial output bundle into its phase output directory. This directory contains:
- `merged-output.md` (primary output)
- `diff-analysis.md`
- `debate-transcript.md`
- `base-selection.md`
- `refactor-plan.md`
- `merge-log.md`

When a Pipeline Mode invocation includes a `compare-merge` phase, `/sc:spawn` SHOULD expose that phase directory as `artifacts_dir` in the return contract.
```

### D. Clarify the manifest relationship

Add one sentence to the manifest schema section or immediately after it:

```md
For phases of type `compare-merge`, the phase `output_dir` recorded in the manifest is the same directory surfaced as `artifacts_dir` in the return contract when that phase is selected as the pipeline's canonical output bundle.
```

---

## Recommended Return Contract Example

Add an example contract to the spec:

```yaml
return_contract:
  status: "success"
  task_hierarchy_path: null
  tasks_created: 0
  delegation_map: {}
  parallel_groups: []
  completion_summary: {}
  pipeline_manifest: ".dev/spawn-output/2026-03-23/spawn-manifest.json"
  artifacts_dir: ".dev/spawn-output/2026-03-23/phases/merge/"
```

And document that consumers can then read:

```text
.dev/spawn-output/2026-03-23/phases/merge/merged-output.md
.dev/spawn-output/2026-03-23/phases/merge/diff-analysis.md
.dev/spawn-output/2026-03-23/phases/merge/debate-transcript.md
.dev/spawn-output/2026-03-23/phases/merge/base-selection.md
.dev/spawn-output/2026-03-23/phases/merge/refactor-plan.md
.dev/spawn-output/2026-03-23/phases/merge/merge-log.md
```

---

## Interaction With Existing Adversarial Contract

This change is especially clean because `/sc:adversarial` already defines an `artifacts_dir` field in its own return contract.

That means `/sc:spawn` is not inventing a new concept. It is propagating an existing downstream contract upward.

Recommended implementation policy:
- when `compare-merge` invokes `/sc:adversarial`, capture its returned `artifacts_dir`
- set the phase `output_dir` to that same directory, or validate they match
- surface that directory as spawn-level `artifacts_dir` if this phase is the selected canonical bundle

This avoids duplicating path derivation logic and reduces drift between the two command contracts.

---

## Edge Cases

### 1. Pipeline has no compare-merge phase
- `artifacts_dir = null`
- consumer uses `pipeline_manifest`

### 2. Pipeline has multiple compare-merge phases
- `artifacts_dir` points to the last successfully completed compare-merge phase in topological order
- manifest remains the source of truth for the others

### 3. Compare-merge fails after creating artifacts
- if the phase output directory exists, still surface it as `artifacts_dir`
- `status` and manifest phase status communicate whether the result is partial/failed
- this preserves debuggability and manual recovery value

### 4. Compare-merge is skipped because dependencies failed
- `artifacts_dir = null` unless a previous relevant compare-merge phase produced the canonical bundle

---

## Acceptance Criteria

1. The `/sc:spawn` return contract includes `artifacts_dir`.
2. In Standard Mode, `artifacts_dir` is `null`.
3. In Pipeline Mode without `compare-merge`, `artifacts_dir` is `null`.
4. In Pipeline Mode with one successful `compare-merge` phase, `artifacts_dir` equals that phase’s output directory.
5. That directory is documented as containing:
   - `merged-output.md`
   - `diff-analysis.md`
   - `debate-transcript.md`
   - `base-selection.md`
   - `refactor-plan.md`
   - `merge-log.md`
6. The spec explicitly tells consumers when to use `artifacts_dir` versus `pipeline_manifest`.
7. If multiple `compare-merge` phases exist, the spec defines a deterministic selection rule for `artifacts_dir`.
8. If a compare-merge phase fails after producing artifacts, the directory may still be surfaced via `artifacts_dir` for recovery and inspection.
9. The documented relationship between spawn `artifacts_dir` and adversarial `artifacts_dir` is explicit, so the two contracts do not drift.

---

## Final Recommendation

Adopt the additive contract change:
- keep `pipeline_manifest` for full pipeline introspection,
- add `artifacts_dir` for direct access to the final adversarial artifact bundle,
- and document that consumers should use `artifacts_dir` as the primary entry point to all `compare-merge` outputs.

This is the smallest, clearest, and most backward-compatible fix for M13.

It solves the real problem: making adversarial’s full output visible to consumers without forcing them to reverse-engineer pipeline internals from the manifest.