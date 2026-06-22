# Count-Invariant Grader Mechanism

Status: Complete
Date: 2026-06-20

## Decision

Use a new grader assertion type: `yaml_list_len_eq`.

The invariant `len(unreached_surfaces) == runtime_surface_unreached` is computed by the grader from the two already-emitted contract fields:

- `unreached_surfaces` — a top-level YAML list in the emitted contract.
- `runtime_surface_unreached` — a top-level YAML scalar in the emitted contract.

No producer-emitted helper scalar is introduced. In particular, the skill MUST NOT emit `unreached_surfaces_len` or any other seventh runtime-surface contract-like field.

## Artifact Target

The assertion target is the run-time emitted contract artifact:

```text
with_skill/outputs/contract.yaml
```

Scalar assertions such as `yaml_field` and `yaml_field_min` continue to require flat, top-level, non-indented keys because they use `parse_yaml_simple`. Therefore `runtime_surface_unreached` and `runtime_surface_degraded` must remain top-level scalar keys in `contract.yaml`.

## Implementation

Implemented `check_yaml_list_len_eq(assertion, base_dir) -> tuple[bool, str]` in:

```text
.dev/eval-workspaces/sc-reflect/grader.py
```

Assertion keys:

```yaml
type: yaml_list_len_eq
target: with_skill/outputs/contract.yaml
list_field: unreached_surfaces
count_field: runtime_surface_unreached
```

The checker uses `yaml.safe_load`, verifies `list_field` resolves to a list, coerces `count_field` to `int`, and passes only when the list length equals the scalar count.

Documented the checker in:

```text
src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md
```

## Rationale

`parse_yaml_simple` skips indented YAML and cannot compute list length, so `yaml_field` / `yaml_field_min` cannot express this invariant. A full-YAML checker avoids self-attested producer values and directly verifies the contract fields that FR-RSR already emits.
