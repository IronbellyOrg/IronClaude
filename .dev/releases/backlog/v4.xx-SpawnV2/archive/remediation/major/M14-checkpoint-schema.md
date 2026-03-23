# M14 — Spawn Checkpoint Schema Proposal

## Problem

The current Spawn V2 spec requires `Checkpoint → Serena memory` at every wave boundary, but it does not define:

- what data is persisted
- how checkpoint keys are named
- how concurrent sessions avoid collisions
- how `--resume` determines whether a checkpoint is still valid

This makes resume semantics underspecified and unsafe.

---

## Proposal Summary

Define Spawn checkpoints as **versioned, session-scoped JSON documents** written to Serena memory at every wave boundary.

Design goals:

1. **Deterministic lookup** — every checkpoint has a predictable key.
2. **Session isolation** — concurrent runs never share a memory key.
3. **Resume safety** — `--resume` only accepts checkpoints that match the current run context.
4. **Wave-specific detail** — each wave persists the data needed by the next wave, not just a generic summary.
5. **Staleness detection** — changed inputs, flags, graph shape, or workspace identity invalidate resume.

---

## 1. Key Naming Convention

### Canonical key format

```text
spawn/{workspace_fingerprint}/{pipeline_id}/{session_id}/wave/{wave_index}
```

### Companion alias keys

These are optional convenience pointers for lookup:

```text
spawn/{workspace_fingerprint}/{pipeline_id}/latest
spawn/{workspace_fingerprint}/{pipeline_id}/{session_id}/latest
```

The alias values are small pointer records containing the canonical wave key and metadata, not full checkpoint payloads.

### Field definitions

- `spawn` — fixed namespace prefix
- `workspace_fingerprint` — stable identifier for the repo/worktree
- `pipeline_id` — the manifest-level pipeline identifier, e.g. `spawn-2026-03-23T03-14-55Z`
- `session_id` — unique execution session identifier for this exact invocation
- `wave_index` — zero-based or one-based integer wave number; use one-based for readability

### Required generation rules

#### `workspace_fingerprint`

Use a deterministic, collision-resistant value derived from:

```text
SHA256(realpath(output_root) + "|" + realpath(repo_root) + "|" + git_head_or_detached_state)
```

Truncate to 12-16 hex chars for key readability.

Purpose:
- isolates separate worktrees on the same branch
- distinguishes runs against different repos or detached HEAD states
- prevents collision across parallel Claude sessions sharing Serena memory

#### `pipeline_id`

Reuse the manifest pipeline ID already defined in the spec:

```json
"pipeline_id": "spawn-<timestamp>"
```

Strengthen it to include enough entropy to avoid same-second collisions:

```text
spawn-<UTC timestamp>-<6 char random suffix>
```

Example:

```text
spawn-2026-03-23T03-14-55Z-a91f3c
```

#### `session_id`

Generate a unique per-invocation ID:

```text
sess-<UTC timestamp>-<8 char random suffix>
```

Example:

```text
sess-2026-03-23T03-14-55Z-81c4d2e1
```

This is distinct from `pipeline_id` so retries or manual `--resume` attempts can be traced separately.

### Example keys

```text
spawn/4f2ab9130cd1/spawn-2026-03-23T03-14-55Z-a91f3c/sess-2026-03-23T03-14-55Z-81c4d2e1/wave/1
spawn/4f2ab9130cd1/spawn-2026-03-23T03-14-55Z-a91f3c/sess-2026-03-23T03-14-55Z-81c4d2e1/wave/2
spawn/4f2ab9130cd1/spawn-2026-03-23T03-14-55Z-a91f3c/latest
```

---

## 2. Checkpoint Envelope Schema

Every wave checkpoint MUST use the same top-level envelope.

```json
{
  "schema_version": "1.0",
  "checkpoint_type": "spawn_wave_boundary",
  "pipeline_id": "spawn-2026-03-23T03-14-55Z-a91f3c",
  "session_id": "sess-2026-03-23T03-14-55Z-81c4d2e1",
  "workspace_fingerprint": "4f2ab9130cd1",
  "wave_index": 2,
  "wave_name": "dispatch",
  "created_at": "2026-03-23T03:21:18Z",
  "updated_at": "2026-03-23T03:21:18Z",
  "status": "completed",
  "resume_eligible": true,
  "resume_from": "wave_3",
  "run_context": {},
  "graph_snapshot": {},
  "manifest_snapshot": {},
  "wave_state": {},
  "artifacts": {},
  "validation": {},
  "provenance": {},
  "summary": {}
}
```

### Top-level fields

| Field | Type | Required | Purpose |
|---|---|---:|---|
| `schema_version` | string | yes | Versioned contract for future migrations |
| `checkpoint_type` | string | yes | Fixed discriminator: `spawn_wave_boundary` |
| `pipeline_id` | string | yes | Links checkpoint to manifest/run |
| `session_id` | string | yes | Isolates concurrent sessions |
| `workspace_fingerprint` | string | yes | Isolates repo/worktree identity |
| `wave_index` | int | yes | Boundary number |
| `wave_name` | string | yes | Human-readable wave label |
| `created_at` | ISO-8601 | yes | First write time |
| `updated_at` | ISO-8601 | yes | Last write time |
| `status` | enum | yes | `completed | failed | invalidated` |
| `resume_eligible` | bool | yes | Whether this boundary can be resumed from |
| `resume_from` | string/null | yes | Next wave label or phase entrypoint |
| `run_context` | object | yes | Immutable inputs needed for staleness checks |
| `graph_snapshot` | object | yes | Frozen DAG/parallel-group shape |
| `manifest_snapshot` | object | yes | Manifest status at checkpoint time |
| `wave_state` | object | yes | Wave-specific persisted state |
| `artifacts` | object | yes | Output paths and hashes required by resume |
| `validation` | object | yes | Resume safety checks |
| `provenance` | object | yes | Source, host, branch, commit metadata |
| `summary` | object | yes | Short operator-facing explanation |

---

## 3. Required `run_context` Fields

`run_context` is the immutable identity of the run. `--resume` MUST compare the current invocation against this block.

```json
{
  "task_description": "user prompt or pipeline task",
  "pipeline_mode": true,
  "cli_command": "/sc:spawn --pipeline ...",
  "flags": {
    "depth": "deep",
    "pipeline_seq": false,
    "max_concurrent": 6,
    "agents": ["architect", "backend", "security"],
    "output_dir": "/abs/path",
    "prompt_hash": "sha256:...",
    "config_hash": "sha256:..."
  },
  "repo_root": "/config/workspace/IronClaude",
  "output_root": "/config/workspace/IronClaude/.dev/.../output",
  "git": {
    "branch": "v3.0-v3.2-Fidelity",
    "head": "08fa0d8...",
    "is_dirty": true
  },
  "spec_inputs": {
    "pipeline_definition_hash": "sha256:...",
    "resolved_phase_config_hash": "sha256:..."
  }
}
```

### Notes

- `flags` MUST contain all resume-relevant CLI settings after inheritance/resolution, not just raw user input.
- `prompt_hash` hashes the effective prompt after `${prompt}` substitution.
- `resolved_phase_config_hash` hashes the fully expanded pipeline definition after wildcard expansion, inheritance, and dependency resolution.
- These hashes are the primary defense against stale resumes when the spec or execution plan changes.

---

## 4. Required `graph_snapshot` Fields

`graph_snapshot` captures the execution structure at the wave boundary.

```json
{
  "phase_ids": ["analyze_api", "design_patch", "test_regression"],
  "phase_count": 3,
  "dependency_edges": [
    ["analyze_api", "design_patch"],
    ["design_patch", "test_regression"]
  ],
  "parallel_groups": [
    ["analyze_api"],
    ["design_patch"],
    ["test_regression"]
  ],
  "graph_hash": "sha256:...",
  "dag_version": 1
}
```

### Resume rule

If `graph_hash` differs from the current resolved DAG, `--resume` MUST reject the checkpoint as stale.

---

## 5. Required `manifest_snapshot` Fields

This mirrors the on-disk manifest enough to support a reliable resume decision.

```json
{
  "manifest_path": "/abs/path/spawn-manifest.json",
  "manifest_hash": "sha256:...",
  "phase_statuses": {
    "analyze_api": "completed",
    "design_patch": "completed",
    "test_regression": "pending"
  },
  "completed_phase_ids": ["analyze_api", "design_patch"],
  "failed_phase_ids": [],
  "skipped_phase_ids": [],
  "last_completed_phase": "design_patch"
}
```

### Resume rule

The Serena checkpoint is an accelerator, not the sole source of truth. `--resume` SHOULD cross-check Serena checkpoint data against the manifest on disk. If they disagree, disk manifest wins and the checkpoint is marked suspect.

---

## 6. Wave-Specific `wave_state` Schema

Each wave persists a common block plus wave-specific fields.

### Common fields for every wave

```json
{
  "started_at": "ISO-8601",
  "completed_at": "ISO-8601",
  "duration_ms": 1234,
  "inputs_ready": true,
  "outputs_written": true,
  "errors": [],
  "warnings": [],
  "operator_notes": "short summary"
}
```

### Wave 1 — Intake / Resolution

Purpose: capture normalized inputs before DAG construction.

```json
{
  "task_description": "...",
  "raw_flags": {},
  "resolved_flags": {},
  "resolved_agents": ["architect", "backend"],
  "resolved_prompt": "effective prompt text or omitted if too large",
  "resolved_prompt_hash": "sha256:...",
  "pipeline_definition_source": "/abs/path/or inline",
  "expanded_phases": [
    {
      "id": "analyze_api",
      "type": "analyze",
      "depends_on": [],
      "output_dir": "/abs/path/analyze_api"
    }
  ]
}
```

### Wave 2 — DAG Construction

Purpose: capture the frozen execution plan.

```json
{
  "domain_map": {
    "api": ["analyze_api"],
    "tests": ["test_regression"]
  },
  "dependency_graph": {
    "analyze_api": [],
    "design_patch": ["analyze_api"],
    "test_regression": ["design_patch"]
  },
  "parallel_groups": [
    ["analyze_api"],
    ["design_patch"],
    ["test_regression"]
  ],
  "concurrency_cap": 10,
  "sequential_override": false,
  "delegation_plan": {
    "analyze_api": "/sc:analyze",
    "design_patch": "/sc:design",
    "test_regression": "/sc:test"
  }
}
```

### Wave 3 — Dispatch / Execution

Purpose: capture actual runtime outcomes at the phase-group boundary.

```json
{
  "group_index": 1,
  "dispatched_phase_ids": ["design_patch"],
  "completed_phase_ids": ["design_patch"],
  "failed_phase_ids": [],
  "manual_phase_ids": [],
  "skipped_phase_ids": [],
  "phase_results": {
    "design_patch": {
      "status": "completed",
      "attempts": 1,
      "agent": "architect",
      "command": "/sc:design",
      "started_at": "ISO-8601",
      "completed_at": "ISO-8601",
      "output_dir": "/abs/path/design_patch",
      "output_hash": "sha256:...",
      "error": null
    }
  }
}
```

### Wave 4 — Artifact Routing / Dependency Verification

Purpose: record the handoff state required by downstream consumers.

```json
{
  "routing_map": {
    "design_patch": ["test_regression"]
  },
  "verified_dependency_outputs": {
    "design_patch": {
      "exists": true,
      "path": "/abs/path/design_patch",
      "hash": "sha256:..."
    }
  },
  "consumer_ready": ["test_regression"],
  "consumer_blocked": []
}
```

### Wave 5 — Completion / Resume Handoff

Purpose: persist the minimum complete state for a future `--resume`.

```json
{
  "completion_summary": {
    "total": 3,
    "completed": 2,
    "failed": 0,
    "skipped": 0,
    "pending": 1,
    "manual": 0
  },
  "next_runnable_phase_ids": ["test_regression"],
  "resume_entrypoint": "test_regression",
  "preserved_context_paths": [
    "/abs/path/analyze_api",
    "/abs/path/design_patch"
  ],
  "human_handoff_notes": "Resume at test_regression after verifying unchanged DAG"
}
```

---

## 7. `artifacts` Block

Artifacts required for resume MUST be explicit and hashed.

```json
{
  "required": [
    {
      "phase_id": "design_patch",
      "path": "/abs/path/design_patch/result.md",
      "exists": true,
      "size_bytes": 10240,
      "sha256": "abc123..."
    }
  ],
  "optional": [
    {
      "phase_id": "analyze_api",
      "path": "/abs/path/analyze_api/notes.md",
      "exists": true,
      "size_bytes": 2048,
      "sha256": "def456..."
    }
  ]
}
```

### Resume rule

If any required artifact is missing or hash-mismatched, the checkpoint is not resumable from that boundary.

---

## 8. `validation` Block

This block is computed when the checkpoint is written and re-evaluated on `--resume`.

```json
{
  "staleness_basis": {
    "git_head": "08fa0d8...",
    "resolved_phase_config_hash": "sha256:...",
    "graph_hash": "sha256:...",
    "manifest_hash": "sha256:...",
    "required_artifact_hashes": {
      "design_patch": "sha256:..."
    }
  },
  "resume_checks": {
    "workspace_match": true,
    "pipeline_match": true,
    "flags_match": true,
    "git_head_match": true,
    "graph_match": true,
    "manifest_match": true,
    "artifacts_intact": true
  },
  "invalid_reason": null
}
```

---

## 9. Session Isolation Strategy

### Rule 1 — Never use shared generic keys

Forbidden:

```text
checkpoint
spawn-checkpoint
spawn/wave/1
```

These collide across users, worktrees, and concurrent sessions.

### Rule 2 — Session-scoped canonical keys are mandatory

Every write goes to the canonical key that includes both `pipeline_id` and `session_id`.

### Rule 3 — Aliases must be pointer-only

`latest` keys may exist, but they must only store:

```json
{
  "canonical_key": "spawn/.../wave/3",
  "pipeline_id": "spawn-...",
  "session_id": "sess-...",
  "wave_index": 3,
  "updated_at": "ISO-8601"
}
```

This avoids accidental overwrite of full checkpoint payloads.

### Rule 4 — Worktree-aware workspace identity

Two sessions on the same branch but in different worktrees MUST produce different `workspace_fingerprint` values because `realpath(repo_root)` is included.

### Rule 5 — Resume defaults to current session lineage only

When `--resume` is invoked without an explicit checkpoint key:

1. load `spawn/{workspace_fingerprint}/{pipeline_id}/latest`
2. verify its `workspace_fingerprint` matches current repo/worktree
3. follow `canonical_key`
4. reject if the session belongs to another incompatible run context

This permits recovery from the most recent session while still preventing accidental cross-run adoption.

---

## 10. Staleness Detection for `--resume`

`--resume` MUST reject a checkpoint if any of the following conditions hold.

### Hard invalidation checks

1. **Schema mismatch**
   - `schema_version` unsupported

2. **Workspace mismatch**
   - `workspace_fingerprint` differs from current run

3. **Pipeline mismatch**
   - requested `pipeline_id` differs from checkpoint `pipeline_id`

4. **Resolved config mismatch**
   - `resolved_phase_config_hash` differs

5. **DAG mismatch**
   - `graph_hash` differs

6. **Required artifact missing or hash changed**
   - any required output missing or mutated

7. **Manifest contradiction**
   - manifest marks a phase incomplete that checkpoint claims completed, or vice versa

8. **Checkpoint marked failed or invalidated**
   - `status != completed`

### Soft warning checks

These should warn, not always block:

1. **Git branch changed but HEAD unchanged**
2. **Working tree dirty state changed**
3. **Optional artifact hash changed**
4. **Checkpoint age exceeds freshness threshold**

### Freshness threshold

Add:

```json
"validation": {
  "max_resume_age_hours": 24
}
```

If older than threshold, warn and require explicit confirmation or `--force-resume`.

### Resume decision table

| Condition | Behavior |
|---|---|
| All hard checks pass | Resume allowed |
| Only soft warnings present | Resume allowed with warning |
| Any hard invalidation fails | Resume denied; re-plan from Wave 1 or earliest safe boundary |

---

## 11. Write/Read Semantics

### When to write

Write a checkpoint only at **wave-group boundaries**, after:

1. all phases in the current wave/group have reached terminal status for that boundary
2. manifest has been flushed to disk
3. required artifacts for downstream resume have been verified

### Write ordering

To keep disk and Serena consistent:

1. update `spawn-manifest.json`
2. fsync/atomic replace manifest
3. compute checkpoint payload and hashes
4. write canonical Serena checkpoint
5. update `latest` pointer key

### Read ordering on `--resume`

1. load manifest from disk
2. discover candidate Serena checkpoint
3. validate schema/version
4. compare `run_context`, `graph_snapshot`, and `manifest_snapshot`
5. verify required artifacts on disk
6. resume from `resume_from` only if all hard checks pass

---

## 12. Minimal JSON Example

```json
{
  "schema_version": "1.0",
  "checkpoint_type": "spawn_wave_boundary",
  "pipeline_id": "spawn-2026-03-23T03-14-55Z-a91f3c",
  "session_id": "sess-2026-03-23T03-14-55Z-81c4d2e1",
  "workspace_fingerprint": "4f2ab9130cd1",
  "wave_index": 2,
  "wave_name": "dag-construction",
  "created_at": "2026-03-23T03:21:18Z",
  "updated_at": "2026-03-23T03:21:18Z",
  "status": "completed",
  "resume_eligible": true,
  "resume_from": "wave_3",
  "run_context": {
    "task_description": "Implement Spawn V2 remediation plan",
    "pipeline_mode": true,
    "flags": {
      "depth": "deep",
      "pipeline_seq": false,
      "max_concurrent": 4,
      "output_dir": "/config/workspace/IronClaude/.dev/tmp/spawn-run",
      "prompt_hash": "sha256:111",
      "config_hash": "sha256:222"
    },
    "repo_root": "/config/workspace/IronClaude",
    "output_root": "/config/workspace/IronClaude/.dev/tmp/spawn-run",
    "git": {
      "branch": "v3.0-v3.2-Fidelity",
      "head": "08fa0d8",
      "is_dirty": true
    },
    "spec_inputs": {
      "pipeline_definition_hash": "sha256:333",
      "resolved_phase_config_hash": "sha256:444"
    }
  },
  "graph_snapshot": {
    "phase_ids": ["analyze", "design", "test"],
    "phase_count": 3,
    "dependency_edges": [["analyze", "design"], ["design", "test"]],
    "parallel_groups": [["analyze"], ["design"], ["test"]],
    "graph_hash": "sha256:555",
    "dag_version": 1
  },
  "manifest_snapshot": {
    "manifest_path": "/config/workspace/IronClaude/.dev/tmp/spawn-run/spawn-manifest.json",
    "manifest_hash": "sha256:666",
    "phase_statuses": {
      "analyze": "completed",
      "design": "pending",
      "test": "pending"
    },
    "completed_phase_ids": ["analyze"],
    "failed_phase_ids": [],
    "skipped_phase_ids": [],
    "last_completed_phase": "analyze"
  },
  "wave_state": {
    "started_at": "2026-03-23T03:20:00Z",
    "completed_at": "2026-03-23T03:21:18Z",
    "duration_ms": 78000,
    "inputs_ready": true,
    "outputs_written": true,
    "errors": [],
    "warnings": [],
    "operator_notes": "DAG resolved and frozen",
    "domain_map": {
      "backend": ["analyze", "design"],
      "qa": ["test"]
    },
    "dependency_graph": {
      "analyze": [],
      "design": ["analyze"],
      "test": ["design"]
    },
    "parallel_groups": [["analyze"], ["design"], ["test"]],
    "concurrency_cap": 4,
    "sequential_override": false,
    "delegation_plan": {
      "analyze": "/sc:analyze",
      "design": "/sc:design",
      "test": "/sc:test"
    }
  },
  "artifacts": {
    "required": [],
    "optional": []
  },
  "validation": {
    "staleness_basis": {
      "git_head": "08fa0d8",
      "resolved_phase_config_hash": "sha256:444",
      "graph_hash": "sha256:555",
      "manifest_hash": "sha256:666",
      "required_artifact_hashes": {}
    },
    "resume_checks": {
      "workspace_match": true,
      "pipeline_match": true,
      "flags_match": true,
      "git_head_match": true,
      "graph_match": true,
      "manifest_match": true,
      "artifacts_intact": true
    },
    "invalid_reason": null,
    "max_resume_age_hours": 24
  },
  "provenance": {
    "writer": "superclaude spawn",
    "host": "claude-code",
    "source": "serena-memory",
    "branch": "v3.0-v3.2-Fidelity"
  },
  "summary": {
    "headline": "Wave 2 completed successfully",
    "next_action": "Resume at wave_3 dispatch",
    "completed_count": 1,
    "pending_count": 2
  }
}
```

---

## 13. Normative Rules to Add to the Spec

Add the following requirements to the Spawn V2 spec:

1. **Checkpoint format**: All Serena checkpoints MUST conform to `spawn_wave_boundary` schema version `1.0`.
2. **Keying**: Checkpoints MUST use canonical key format `spawn/{workspace_fingerprint}/{pipeline_id}/{session_id}/wave/{wave_index}`.
3. **Session isolation**: Checkpoints MUST include both `pipeline_id` and `session_id`; generic shared keys are prohibited.
4. **Resume validation**: `--pipeline-resume` MUST validate `workspace_fingerprint`, `resolved_phase_config_hash`, `graph_hash`, manifest consistency, and required artifacts before resuming.
5. **Manifest precedence**: On conflict, on-disk manifest state is authoritative; Serena checkpoint is advisory acceleration data.
6. **Boundary-only writes**: Checkpoints MUST be written only after a wave/group reaches a stable boundary and manifest/artifacts are flushed.
7. **Staleness handling**: Any hard invalidation condition MUST block resume and require re-entry from the earliest safe wave.
8. **Compatibility**: Unsupported `schema_version` MUST be treated as non-resumable.

---

## 14. Recommended Implementation Sequence

1. Extend manifest generation so `pipeline_id` is unique and high-entropy.
2. Define a `SpawnCheckpointState` dataclass/model with the envelope above.
3. Add canonical key builder and `latest` pointer builder helpers.
4. Hash resolved config, DAG, manifest, and required artifacts at each wave boundary.
5. Write manifest first, then Serena checkpoint.
6. Implement `--resume` validator using hard/soft invalidation rules.
7. Add tests for:
   - concurrent sessions in same repo
   - concurrent sessions in different worktrees
   - changed flags
   - changed DAG
   - missing artifacts
   - stale checkpoint age
   - manifest/checkpoint disagreement

---

## Recommendation

Adopt this schema exactly or with only additive changes. The critical point is not the specific field names; it is that Spawn V2 needs a **versioned, session-scoped, hash-validated checkpoint contract**. Without that, `Checkpoint → Serena memory` remains too ambiguous to support safe `--resume` behavior.
