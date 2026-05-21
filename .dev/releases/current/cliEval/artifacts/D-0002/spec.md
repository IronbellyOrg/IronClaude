# D-0002 — suite.schema.json (v1 suite manifest schema)

**Task:** T01.02 (Phase 1, Roadmap DM-011 / R-002)
**Schema file:** `src/superclaude/cli/eval/suites/suite.schema.json`
**Schema dialect:** **JSON Schema Draft 2020-12** (`$schema: https://json-schema.org/draft/2020-12/schema`).
**Status:** Implemented 2026-05-20

## Why this dialect

Draft 2020-12 is the current published draft of JSON Schema and is fully
supported by `jsonschema>=4.18` (we pin `>=4.0.0`; the installed version is
4.26). It gives us `$defs` (vs. legacy `definitions`), `propertyNames`,
`minProperties`, and `prefixItems` should we need them later. Choosing the
current dialect avoids a re-pin when downstream consumers (e.g. IDE
`yaml-language-server`) update.

## Top-level shape (DM-011)

```
type: object
additionalProperties: false   # AC: "forbids unknown required keys"
required: [name, version, description, defaults,
           required_binaries, optional_capabilities, evals]
```

| Field | Type | Notes |
|---|---|---|
| `name` | string (minLength 1) | Suite name; matches CLI `--suite`. |
| `version` | string (pattern `^[0-9]+\.[0-9]+(\.[0-9]+)?$`) | Schema-version field per M1 Risk-3 forward-evolution. |
| `description` | string | Human-readable summary. |
| `defaults` | object (additionalProperties true) | Per-eval default knobs. Named keys: `per_eval_timeout_sec` (int≥1), `per_eval_memory_mb` (int≥1), `capture_tty` (bool), `keep_home_on_success` (bool). |
| `required_binaries` | array of `requiredBinary` | HARD capability gates. |
| `optional_capabilities` | array of `optionalCapability` | SOFT capability gates. |
| `evals` | array of `evalEntry` | Eval entries (DM-002 shape). |

## `$defs` block

| `$def` | Purpose |
|---|---|
| `failureMode` | enum `[hard, skip, xfail]` (DM-007). |
| `evalIdString` | string with FR-SCH2 regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. |
| `requiredBinary` | `{name, min_version?, failure_mode}` — `additionalProperties: false`. |
| `optionalCapability` | `{name, gate_flag?, failure_mode}` — `additionalProperties: false`. |
| `isolationBlock` | `{home_strategy in [ephemeral, seeded, shared], seed_state[]}`. |
| `parameterizeRow` | object with `minProperties: 1`, `propertyNames pattern ^[A-Za-z_][A-Za-z0-9_]*$`, values constrained to `string|number|boolean`. |
| `evalEntry` | DM-002 entry. `additionalProperties: false`. Required keys: `id, title`. |

## `evals[]` entry shape (DM-002)

`evalEntry` declares all 9 DM-002 fields:

| Field | Type |
|---|---|
| `id` | `evalIdString` (FR-SCH2 regex) |
| `title` | string (minLength 1) |
| `category` | string |
| `requires` | array of strings |
| `timeout_sec` | integer (≥1) |
| `isolation` | `isolationBlock` |
| `inputs` | array of objects |
| `expects` | array of objects |
| `parameterize` | array of `parameterizeRow` (minItems 1) |

Only `id` and `title` are schema-required; remaining fields are optional so
authors can compose minimal entries.

## `parameterize` shape

`parameterize` is an **array of substitution rows**. Each row is an object
of `placeholder -> value` pairs where:

* Placeholder names match `^[A-Za-z_][A-Za-z0-9_]*$` (Python-identifier
  style, so `{{prefix}}` and `{{tool}}` substitutions are unambiguous).
* Values are scalars (`string|number|boolean`) — complex structures are
  rejected to keep template expansion deterministic.
* The row must declare at least one key (`minProperties: 1`).
* The schema validates row shape only; **semantic** expansion (E2 →
  `E2.1, E2.2, ...`) and post-expansion id re-validation against FR-SCH2
  happen in COMP-002 (T01.07).

Template tokens inside `id:` are blocked at this layer because the
`evalIdString` regex disallows `{` and `}`; T01.05 re-applies the same
regex programmatically post-expansion.

## Acceptance criteria → implementation map

| AC bullet (T01.02) | Implementation site |
|---|---|
| File `src/superclaude/cli/eval/suites/suite.schema.json` exists and is jsonschema-valid against a documented dialect. | `suite.schema.json` declares `$schema = draft/2020-12`; `Draft202012Validator.check_schema()` passes. |
| Schema declares required `name,version,description,defaults,required_binaries,optional_capabilities,evals` and forbids unknown required keys. | Top-level `required: [...]` + `additionalProperties: false`. |
| Reference fixture validates green. | `tests/cli/eval/fixtures/valid_suite.yaml` + `test_reference_manifest_validates_green`. |
| Fixture missing a required field is rejected. | `tests/cli/eval/fixtures/missing_name_suite.yaml` + `test_missing_required_field_is_rejected`. |
| spec.md documents schema field rules and `parameterize` shape. | This document. |

## Caller contract (downstream consumers)

- **COMP-002 SuiteLoader (T01.07)** — loads YAML manifests and validates
  them against this schema before any `validate_eval_id` invocation.
- **FR-SCH1 `validate_manifest` (T01.04)** — exposes the schema check as
  a typed function returning `list[EvalSpec]` or raising `SchemaError`.
- **FR-CLI4 `eval doctor` (T01.13)** — surfaces schema violations as
  exit-2 with the offending JSON path.

## Notes / deferred work

- Allow-list `additionalProperties: false` at the top level. Inside
  `defaults` we keep `additionalProperties: true` because suite authors
  may extend the per-eval defaults shape per Phase 4 needs without
  schema churn; the named DM-011 keys are still type-checked.
- `evalEntry.additionalProperties` is `false` to keep the DM-002 contract
  closed; adding new fields requires bumping the schema `version` per
  M1 Risk-3.
- The schema is intentionally light on **semantic** validation
  (parameterize-expansion safety, capability-name resolution); those
  remain runtime checks in COMP-002 (T01.07) and CapabilityGates (T01.11).
