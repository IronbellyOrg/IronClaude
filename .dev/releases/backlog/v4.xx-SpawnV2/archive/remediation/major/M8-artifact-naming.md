# M8: Artifact Naming Convention Per Phase Type — Complete Proposal

## Problem

The spec defines phase-level directories (`<output_dir>/phases/<phase_id>/`) but does not define a stable contract for what files must exist inside each phase directory. Without a per-phase-type naming convention, downstream phases and external consumers cannot resolve inputs deterministically.

## Proposal Summary

Add a normative artifact naming contract for every concrete phase type. The contract must:

1. Define exactly one primary artifact path for every phase type.
2. Reserve fixed filenames for known supplementary artifacts.
3. Distinguish between files that are guaranteed vs optional.
4. Give consumers a deterministic rule for resolving dependency outputs.
5. Forbid phase implementations from renaming primary artifacts.

## Exact Spec Text to Add

### Artifact Naming Convention

All pipeline phase artifacts MUST be written under:

```text
<output_dir>/phases/<phase_id>/
```

Each phase directory MUST contain exactly one **primary artifact** at a phase-type-specific fixed filename. Consumers resolve dependency outputs by reading the primary artifact for the dependency phase type unless a phase explicitly declares that it needs a named supplementary artifact.

Phase implementations MAY write additional files, but they MUST NOT change or omit the required primary artifact filename for their phase type.

### Primary Artifact Table

| Phase Type | Primary Artifact | Required Supplementary Artifacts | Optional Supplementary Artifacts | Notes |
|---|---|---|---|---|
| `analyze` | `output.md` | None | `notes.md`, `sources.json` | Standard single-document analysis result. |
| `design` | `output.md` | None | `notes.md`, `decision-log.md` | Standard single-document design result. |
| `implement` | `output.md` | None | `changed-files.json`, `notes.md` | `output.md` summarizes implementation work; source code changes occur in-place in the repo and are not copied into the phase directory unless explicitly requested by the phase. |
| `test` | `output.md` | None | `test-results.json`, `notes.md` | `output.md` is the human-readable test summary; structured results may be emitted separately. |
| `review` | `output.md` | None | `findings.json`, `notes.md` | `output.md` is the review report. |
| `deploy` | `output.md` | None | `deployment-log.md`, `deployment-metadata.json` | `output.md` is the deployment summary/report. |
| `generate` | `output.md` | None | `notes.md`, `metadata.json` | `generate` is the concrete expanded form of `generate-parallel`. |
| `compare-merge` | `merged-output.md` | `debate-transcript.md`, `diff-analysis.md`, `base-selection.md`, `merge-log.md` | `refactor-plan.md`, `metadata.json` | `merged-output.md` is the canonical dependency artifact for downstream consumers. |

### Artifact Resolution Rules

1. **Directory rule**: Every concrete phase writes only to `<output_dir>/phases/<phase_id>/` for its owned phase artifacts.
2. **Single primary artifact rule**: Every phase type has exactly one canonical primary artifact filename.
3. **Consumer default rule**: A dependent phase that references another phase without naming a specific artifact MUST consume that phase’s primary artifact.
4. **Filename stability rule**: Primary artifact filenames are fixed by phase type and MUST NOT be customized by user input, prompt text, agent choice, or implementation details.
5. **Existence rule**: A phase is not considered to have produced a consumable output unless its primary artifact exists.
6. **Supplementary artifact rule**: Supplementary artifacts may be used by humans, debugging tools, manifests, or explicitly artifact-aware consumers, but they do not replace the primary artifact.
7. **Unknown extra files rule**: Consumers MUST ignore unrecognized extra files in a phase directory unless explicitly instructed to read them.
8. **Markdown rule**: All required primary and required supplementary artifacts use `.md` filenames unless the spec explicitly defines a structured machine-readable file for that artifact.
9. **Manifest rule**: The pipeline manifest SHOULD record the phase’s `primary_artifact` absolute path and MAY record a list of supplementary artifacts.
10. **Resume rule**: `--pipeline-resume` MUST determine phase output availability using the required primary artifact filename for the phase type.

### Dependency Path Resolution

Consumers resolve dependency paths as follows:

| Dependency Phase Type | Resolved Default Input Path |
|---|---|
| `analyze` | `<output_dir>/phases/<dep_id>/output.md` |
| `design` | `<output_dir>/phases/<dep_id>/output.md` |
| `implement` | `<output_dir>/phases/<dep_id>/output.md` |
| `test` | `<output_dir>/phases/<dep_id>/output.md` |
| `review` | `<output_dir>/phases/<dep_id>/output.md` |
| `deploy` | `<output_dir>/phases/<dep_id>/output.md` |
| `generate` | `<output_dir>/phases/<dep_id>/output.md` |
| `compare-merge` | `<output_dir>/phases/<dep_id>/merged-output.md` |

### Dynamic Phase Rules

#### `generate-parallel`

`generate-parallel` is a YAML expansion directive, not a runtime artifact-producing concrete phase type. After expansion, each generated child phase is of type `generate` and MUST write:

```text
<output_dir>/phases/<generated_phase_id>/output.md
```

If a downstream `compare-merge` phase collects all outputs from a `generate-parallel` expansion, it resolves the set of branch inputs as the `output.md` primary artifact from each expanded `generate` phase.

#### `compare-merge`

A `compare-merge` phase MUST write the following files in its phase directory:

- `merged-output.md` — canonical merged result and primary artifact
- `debate-transcript.md` — adversarial or comparison transcript
- `diff-analysis.md` — structured analysis of branch differences
- `base-selection.md` — rationale for chosen base or synthesis strategy
- `merge-log.md` — merge decisions and notable transformations

A `compare-merge` phase MAY additionally write:

- `refactor-plan.md`
- `metadata.json`

Downstream phases that depend on `compare-merge` without naming a specific artifact MUST consume `merged-output.md`.

### Prohibitions

The spec should state the following explicitly:

- A phase MUST NOT emit its primary content under an arbitrary filename.
- A phase MUST NOT require downstream consumers to inspect directory contents to infer which file is primary.
- A phase MUST NOT use agent-specific or persona-specific primary artifact names.
- A phase MUST NOT overload supplementary artifacts as the only consumable output.

## Why This Convention Is Complete

This convention closes the ambiguity for all concrete phase types currently in scope:

- Static phase types (`analyze`, `design`, `implement`, `test`, `review`, `deploy`) all share the same canonical primary artifact: `output.md`.
- Expanded dynamic generation uses the concrete `generate` type and therefore also resolves to `output.md`.
- Fan-in synthesis uses a distinct primary artifact, `merged-output.md`, because it semantically represents a merged result rather than a simple phase-local report.
- Required compare-merge side artifacts are explicitly named so consumers, manifests, and humans can locate them reliably.

## Recommended Companion Spec Updates

To make the naming convention fully enforceable, also update these sections:

1. **Pipeline Manifest Schema**
   - Extend each phase entry with:
   ```json
   "primary_artifact": "absolute-or-output-dir-relative-path",
   "supplementary_artifacts": ["..."]
   ```

2. **Artifact Routing Section**
   - Replace vague wording like “each phase writes to `<output_dir>/<phase_id>/`” with the exact directory and filename rules above.

3. **Delegation Matrix / Dispatch Rules**
   - State that the dispatcher passes the resolved primary artifact path of each dependency into downstream prompts by default.

4. **Validation / Acceptance Criteria**
   - Add a validation requirement that each completed phase directory contains the correct primary artifact filename for its type.

## Final Recommendation

Adopt the simple invariant:

- **Most phase types write `output.md`.**
- **`compare-merge` writes `merged-output.md` as its primary artifact plus a fixed set of named side artifacts.**

This keeps the contract easy to remember, easy to validate, and deterministic for both routing logic and downstream consumers.
