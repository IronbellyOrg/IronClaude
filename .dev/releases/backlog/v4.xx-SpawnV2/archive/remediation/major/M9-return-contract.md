# Major Issue M9 — Mode-Discriminated Return Contract

## Problem

The current return contract uses the same top-level schema for both Standard mode and Pipeline mode, but different subsets of fields are meaningful in each mode. The spec currently tells producers to emit `null` for fields that were not reached or cannot be determined, but it does not distinguish between:

1. `null` because the invocation failed before the field could be populated, and
2. `null` because that field is not applicable in the selected execution mode.

This creates an ambiguous consumer contract. Callers cannot safely determine which fields are expected to be populated without separately inferring or re-deriving the invocation mode.

## Why this is a major issue

This ambiguity weakens the core value of a return contract: predictable machine consumption.

Current downstream consumers appear to route primarily on generic fields such as `status`, `convergence_score`, and `merged_output_path` (for example in `/config/workspace/IronClaude/tests/sc-roadmap/integration/test_return_contract_routing.py`), but as Pipeline support expands, consumers will increasingly need to know whether pipeline-only metadata is expected.

Without an explicit discriminator:
- consumers must branch on external knowledge instead of the contract itself,
- validation cannot reliably distinguish malformed output from intentionally inapplicable fields,
- documentation remains underspecified,
- future additions risk deepening the ambiguity.

## Proposed solution

Add an explicit required `mode` field to the return contract and document field population guarantees per mode.

### Required `mode` field

Introduce:

```yaml
mode: "standard" | "pipeline"
```

This field must always be populated, including failure cases.

It is a discriminator, not optional metadata. Consumers should use it as the first branch point when interpreting the contract.

## Revised contract shape

Keep one shared contract family, but make it explicitly mode-discriminated.

### Shared fields

These fields remain available in all modes:

```yaml
return_contract:
  mode: "standard" | "pipeline"
  status: "success" | "partial" | "failed"
  merged_output_path: "<path|null>"
  convergence_score: 0.75
  artifacts_dir: "<path>"
  unresolved_conflicts: 2
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []
```

### Standard mode fields

Standard mode retains the existing direct-invocation semantics:

```yaml
return_contract:
  mode: "standard"
  status: "success"
  merged_output_path: "<path to merged file>"
  convergence_score: 0.75
  artifacts_dir: "<path to adversarial/ directory>"
  base_variant: "opus:architect"
  unresolved_conflicts: 2
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []
```

### Pipeline mode fields

Pipeline mode adds explicit pipeline metadata and relaxes expectations for standard-only fields where appropriate:

```yaml
return_contract:
  mode: "pipeline"
  status: "success"
  merged_output_path: "<path to final pipeline output>"
  convergence_score: 0.82
  artifacts_dir: "<path to final phase artifacts or pipeline artifacts root>"
  unresolved_conflicts: 1
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants: []

  pipeline:
    manifest_path: "<path to manifest.json>"
    phase_count: 3
    phases_succeeded: 3
    phases_failed: 0
    total_agents_spawned: 9
    execution_time_seconds: 142
```

## Population matrix

The documentation should explicitly define which fields are:
- always populated,
- conditionally populated based on execution progress,
- not applicable in a given mode.

Suggested matrix:

| Field | Standard mode | Pipeline mode | Notes |
|---|---|---|---|
| `mode` | always | always | Required discriminator |
| `status` | always | always | Shared status model |
| `merged_output_path` | progress-dependent | progress-dependent | Null only if output not reached |
| `convergence_score` | progress-dependent | progress-dependent | Null only if convergence step not reached |
| `artifacts_dir` | always | always | Should exist from start of execution |
| `unresolved_conflicts` | always | always | Shared consumer-facing signal |
| `fallback_mode` | always | always | Shared execution metadata |
| `failure_stage` | failed only | failed only | Null on non-failure |
| `invocation_method` | always | always | Shared provenance metadata |
| `unaddressed_invariants` | always | always | Empty list if none / skipped |
| `base_variant` | applicable; progress-dependent | not applicable unless explicitly redefined | Do not overload meaning across modes |
| `pipeline.manifest_path` | not applicable | always | Required for pipeline mode |
| `pipeline.phase_count` | not applicable | always | Required for pipeline mode |
| `pipeline.phases_succeeded` | not applicable | always | Required for pipeline mode |
| `pipeline.phases_failed` | not applicable | always | Required for pipeline mode |
| `pipeline.total_agents_spawned` | not applicable | always | Required for pipeline mode |
| `pipeline.execution_time_seconds` | not applicable | always | Required for pipeline mode |

## Critical semantic rule

The contract must define a strict distinction between two concepts:

- `not applicable for this mode`
- `applicable, but unavailable because execution did not reach that stage`

That distinction is what `mode` unlocks.

### Recommended rule set

1. `mode` determines applicability.
2. `null` only means "applicable but not produced yet / not reached / failed before determination".
3. Mode-inapplicable fields should either:
   - live inside a mode-specific nested object, or
   - be explicitly documented as not applicable for that mode.

The cleanest version is to place pipeline-only data under a nested `pipeline` object and avoid flattening pipeline-only fields into the shared top level.

## Recommended structure choice

Use a discriminated-union design in documentation and implementation.

### Option A — Minimal change

Keep the current mostly-flat contract, add `mode`, and document applicability.

Pros:
- lowest implementation churn,
- easiest migration,
- minimal consumer breakage.

Cons:
- top-level namespace stays semantically mixed,
- ambiguous field ownership persists unless docs are extremely precise.

### Option B — Preferred

Add `mode` and group mode-specific fields into nested objects.

Recommended shape:

```yaml
return_contract:
  mode: "standard" | "pipeline"

  common:
    status: "success" | "partial" | "failed"
    merged_output_path: "<path|null>"
    convergence_score: 0.75
    artifacts_dir: "<path>"
    unresolved_conflicts: 2
    fallback_mode: false
    failure_stage: null
    invocation_method: "skill-direct"
    unaddressed_invariants: []

  standard:
    base_variant: "opus:architect"

  pipeline:
    manifest_path: "<path to manifest.json>"
    phase_count: 3
    phases_succeeded: 3
    phases_failed: 0
    total_agents_spawned: 9
    execution_time_seconds: 142
```

Pros:
- applicability becomes structurally obvious,
- schema validation becomes straightforward,
- future mode expansion is cleaner,
- consumers no longer guess from null patterns.

Cons:
- larger breaking change,
- requires consumer migration.

## Recommendation

Implement Option A immediately as the remediation minimum, but document the contract as a discriminated union and reserve Option B as the follow-up hardening path.

That means:
1. add required `mode`,
2. add a field population matrix,
3. explicitly define null semantics,
4. place any new pipeline-only fields under `pipeline`,
5. avoid introducing additional mode-specific top-level fields.

This satisfies the issue with low implementation risk while moving the contract toward a cleaner long-term design.

## Documentation changes required

Update the return-contract spec to include:

### 1. Discriminator requirement

Add a normative statement:

> `mode` is required on every return contract and is the authoritative discriminator for consumer parsing.

### 2. Field applicability table

Document, for every field:
- type,
- whether it is common, standard-only, or pipeline-only,
- whether it is always present, progress-dependent, or failure-dependent,
- what `null` means if allowed.

### 3. Consumer guidance

Document a required parsing order:

1. Read `mode`
2. Validate common fields
3. Validate mode-specific fields for that mode
4. Interpret any `null` values only within that mode's applicability rules

### 4. Producer guidance

Document that producers must never rely on consumers inferring mode from field presence or null patterns.

## Consumer behavior after change

After this remediation, consumers should be able to do:

```text
if contract.mode == "standard":
    parse standard fields
elif contract.mode == "pipeline":
    parse pipeline fields
else:
    treat contract as invalid
```

This is materially better than the current implicit pattern:

```text
if pipeline-looking fields are present or standard-only fields are null in a certain combination:
    guess pipeline
```

## Backward compatibility and migration

### Producer migration

All return-contract producers should start emitting `mode` immediately.

### Consumer migration

Consumers should:
1. prefer `mode` when present,
2. temporarily retain legacy fallback parsing for contracts that predate this change,
3. log or flag legacy contracts that omit `mode`.

### Validation policy

After migration, contract validation should fail if `mode` is missing.

## Test coverage to add

Add contract tests covering:

1. Standard mode success includes `mode: standard`
2. Standard mode failure still includes `mode: standard`
3. Pipeline mode success includes `mode: pipeline`
4. Pipeline mode failure still includes `mode: pipeline`
5. Pipeline-only fields are validated only in pipeline mode
6. Standard-only fields are not required in pipeline mode
7. `null` is accepted only for progress-dependent applicable fields
8. Missing `mode` is rejected by strict validators
9. Legacy contract without `mode` follows temporary compatibility path if needed

## Acceptance criteria

This issue is resolved when:

- the return contract includes a required `mode` discriminator,
- the spec clearly states which fields are populated in Standard vs Pipeline mode,
- `null` semantics are explicitly defined as "applicable but unavailable," not "mode-inapplicable",
- pipeline-only fields are documented as pipeline-only,
- consumers can parse the contract without out-of-band knowledge of invocation mode.

## Final recommendation

Approve a mode-discriminated return contract with a required `mode` field and explicit per-mode population documentation.

This is the smallest change that restores contract clarity, improves machine consumption, and prevents mode inference from leaking into every downstream consumer.