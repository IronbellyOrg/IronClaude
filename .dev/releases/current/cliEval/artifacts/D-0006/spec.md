# D-0006 — COMP-002 `SuiteLoader` gate-chain orchestrator

**Task:** T01.07 (Phase 1, Roadmap R-006)
**Module:** `src/superclaude/cli/eval/loader.py`
**Public surface:** `SuiteLoader`, `ParsedSuite`, `CapabilityResolver`,
`PermissiveCapabilityResolver`, `UnresolvedCapability`,
`UNRESOLVED_CAPABILITY_EXIT_CODE`, `SUITE_LOADER_ERROR_EXIT_CODE`,
`SuiteLoaderError`
**Status:** Implemented 2026-05-20
**Tier:** STRICT (security-critical, critical-path override)

## Purpose

`SuiteLoader.load(path)` is the single ingress point from a `suites/*.yaml`
manifest on disk to a fully validated, capability-checked, parameterize-
expanded `ParsedSuite`. It composes the FR-SCH1, FR-SCH2, NFR-SEC1, and
COMP-009 gates into one ordered chain so that every downstream consumer
(eval runner, doctor, list, describe) can rely on the same security
invariants without re-implementing them.

The load runs entirely in-memory: no filesystem writes, no scratch
directories, no logging. Every typed failure raises BEFORE any side
effect (NFR-SEC1 invariant).

## Class contract

```python
@dataclass
class SuiteLoader:
    capability_resolver: CapabilityResolver = field(
        default_factory=PermissiveCapabilityResolver
    )

    def load(self, path: Path | str) -> ParsedSuite: ...
```

- **Input:** filesystem path to a `suites/*.yaml` manifest (`str` accepted
  for ergonomics; normalised to `Path`).
- **Output:** a `ParsedSuite` with the post-expansion eval list and
  verbatim suite envelope metadata.
- **Error behaviour:** raises any member of `SuiteLoaderError` =
  `(SchemaError, InvalidEvalId, UnresolvedCapability)`. CLI callers MUST
  map every member to `SUITE_LOADER_ERROR_EXIT_CODE` (= 2).

## Gate ordering (load-bearing)

The chain runs in this fixed order. The order is part of the security
contract — re-arranging gates 2 and 3 would defeat NFR-SEC1.

| # | Gate                                | Implementation                          | Raises                  |
|---|-------------------------------------|-----------------------------------------|-------------------------|
| 1 | YAML read + decode                  | `_read_manifest` (via `_validate_manifest_dict`) | `SchemaError`  |
| 2 | jsonschema (Draft 2020-12) validate | `_validate_manifest_dict`               | `SchemaError`           |
| 3 | Static eval-id regex (FR-SCH2)      | `validate_eval_id` on every `evals[].id` | `InvalidEvalId`        |
| 4 | Capability resolution (COMP-009)    | `self._check_capabilities(entry)` per eval | `UnresolvedCapability` |
| 5 | Parameterize expansion              | `self._expand_entry(entry)` per eval     | (no new errors)        |
| 6 | Expanded-id regex re-check (FR-SCH2)| `validate_eval_id` inside `_expand_entry`| `InvalidEvalId`        |

Stages 1+2 share `_validate_manifest_dict` so every FR-SCH1 rejection
flows through one code path that also powers the backward-compat
`validate_manifest()` API.

### Why gate 3 runs before gate 4 (ordering rationale)

This ordering is the answer to T01.07 AC bullet *"a fixture with an
unsafe id is rejected before any capability resolution call (verified
by mock)"*. The reason it matters in practice:

- `CapabilityGates` (T01.11, COMP-009) is allowed to shell out via
  `shutil.which`, run version probes, and (when MCP is wired) make
  network reachability calls. None of those is a filesystem write to
  the scratch root, but they ARE side effects an attacker would gain
  if they could smuggle a manifest with a traversal-pattern id past
  the regex.
- The regex check is a single compiled-pattern match per id with no
  external dependencies, so running it first costs nothing measurable.
- Putting the cheap, pure check ahead of the expensive, impure check
  is the principle the rest of the harness already follows
  (`_validate_manifest_dict` reads + decodes BEFORE jsonschema, etc.).

`tests/cli/eval/test_suite_loader.py::test_load_rejects_unsafe_id_before_capability_resolver_runs`
asserts the contract by injecting a recording resolver and verifying
`resolver.calls == []` after `InvalidEvalId` raises.

### Why gate 6 (post-expansion re-check) exists

Gate 3 only sees *static* manifest ids; gate 6 sees the
parameterize-expanded forms. The current expansion strategy generates
ids of the form `{base}.{1..N}` which is safe by construction —
digits-only suffix — but the re-check is mandatory because:

- Future expansion strategies (e.g., named row indices) could leak
  unsafe characters.
- A schema-bypassing test or future refactor could substitute the
  base id at expansion time.
- Defence in depth is cheap: one regex match per expanded row.

`tests/cli/eval/test_suite_loader.py::test_load_rejects_post_expansion_unsafe_id`
mocks `_expand_entry` to inject `E2.1.injected` and verifies the
re-check catches it.

## Exit-code map

All three SuiteLoader errors map to the same process exit code. The
constants are kept disjoint so callers can branch on intent without
coupling the classes.

| Trigger                                       | Raised                  | Exit code constant                          | Value |
|-----------------------------------------------|-------------------------|---------------------------------------------|-------|
| Manifest unreadable / YAML decode / schema    | `SchemaError`           | `SCHEMA_ERROR_EXIT_CODE`                    | 2     |
| Static or expanded id failed FR-SCH2          | `InvalidEvalId`         | `INVALID_EVAL_ID_EXIT_CODE`                 | 2     |
| Resolver rejected one or more `requires`      | `UnresolvedCapability`  | `UNRESOLVED_CAPABILITY_EXIT_CODE`           | 2     |
| Aggregate (any of the above)                  | any `SuiteLoaderError`  | `SUITE_LOADER_ERROR_EXIT_CODE`              | 2     |

`SuiteLoaderError` is a `tuple[type[Exception], ...]` rather than a new
base class — see "Design choices" below.

## `CapabilityResolver` Protocol contract

```python
@runtime_checkable
class CapabilityResolver(Protocol):
    def resolve(
        self,
        eval_id: str,
        required: tuple[str, ...],
    ) -> Iterable[str]: ...
```

- **Returns:** the subset of `required` capability names that could not
  be satisfied. An empty iterable means "all required capabilities are
  present"; any non-empty iterable is converted by the loader into
  `UnresolvedCapability(eval_id=..., missing=(...))`.
- **Purity:** implementations MUST NOT perform filesystem writes or
  mutate globals. PATH probes (`shutil.which`) and read-only MCP
  reachability checks are permitted.
- **Idempotency:** the loader assumes `resolve()` returns the same
  answer for the same `(eval_id, required)` pair within one process so
  test stubs and the real `CapabilityGates` (T01.11) can both be wired
  without re-validating.
- **`@runtime_checkable`:** lets tests assert `isinstance(stub,
  CapabilityResolver)` without inheriting; the recording stub used in
  the test suite never imports the Protocol but still satisfies it
  structurally.

`PermissiveCapabilityResolver` is the M1 default: it returns `()` for
every call so M1 callers (the test surface, `eval doctor` dry runs,
and `eval list`) do not need to wire the not-yet-built `CapabilityGates`.
The real implementation lands in T01.11 (COMP-009) and is injected
through `commands.py` (T01.13).

## `ParsedSuite` field shape

```python
@dataclass(frozen=True)
class ParsedSuite:
    name: str
    version: str
    description: str
    defaults: Mapping[str, Any]
    required_binaries: tuple[Mapping[str, Any], ...]
    optional_capabilities: tuple[Mapping[str, Any], ...]
    evals: tuple[EvalSpec, ...]
    source_path: Path
```

- `name`, `version`, `description` and `defaults` are verbatim from the
  manifest envelope.
- `required_binaries` and `optional_capabilities` are tuples so the
  dataclass is hashable and downstream consumers cannot mutate them
  through the container; each entry stays as the original mapping shape
  so it can be replayed by the runner without re-parsing.
- `evals` holds the **post-expansion** eval list: parameterize rows are
  materialised into one `EvalSpec` per row with `.{index}`-suffixed ids.
- `source_path` is the resolved `Path` the manifest was loaded from
  (handy for reporter output and CLI error messages).

## Acceptance criteria → implementation map

| AC bullet (T01.07) | Implementation site |
|---|---|
| Class `SuiteLoader` in `src/superclaude/cli/eval/loader.py` loads `suites/*.yaml`, applies schema validation, eval_id regex, capability resolution, and parameterize expansion in that order. | `SuiteLoader.load` chains `_validate_manifest_dict` → `validate_eval_id` (per id) → `_check_capabilities` (per eval) → `_expand_entry` (per eval). Tests: `test_load_reference_suite_returns_parsed_suite`, `test_load_populates_suite_envelope_fields`, `test_load_expands_parameterize_with_dot_index_suffix`, `test_static_id_evals_pass_through_unmodified`. |
| Each typed error (`SchemaError`, `InvalidEvalId`, `UnresolvedCapability`) maps to process exit code 2 with the error class name in stderr. | Constants `SCHEMA_ERROR_EXIT_CODE`, `INVALID_EVAL_ID_EXIT_CODE`, `UNRESOLVED_CAPABILITY_EXIT_CODE`, and the `SUITE_LOADER_ERROR_EXIT_CODE` aggregate all equal `2`. Tests: `test_schema_error_maps_to_exit_code_two`, `test_invalid_eval_id_maps_to_exit_code_two`, `test_unresolved_capability_exit_code_is_two`, `test_every_loader_exit_constant_is_two`, `test_unresolved_capability_error_class_name_is_visible`. |
| A reference fixture suite loads without error; a fixture with an unsafe id is rejected before any capability resolution call (verified by mock). | `test_load_reference_suite_returns_parsed_suite` + `test_load_rejects_unsafe_id_before_capability_resolver_runs` (injects `_RecordingResolver`, patches `_validate_manifest_dict` to return a dict with `../home` / `1bad` ids, asserts `resolver.calls == []`). |
| `TASKLIST_ROOT/artifacts/D-0006/spec.md` documents the gate ordering and exit-code map. | This document (sections "Gate ordering" and "Exit-code map"). |

## Caller contract (downstream consumers)

- **`eval doctor` (T01.13)** — constructs `SuiteLoader(capability_resolver=
  CapabilityGates(...))` and calls `load()` to validate every
  `suites/*.yaml` it discovers. Maps any `SuiteLoaderError` to exit 2.
- **`eval list` (T01.21) / `eval describe` (T01.22)** — same constructor
  shape; both use `ParsedSuite.name`, `ParsedSuite.version`, and
  `len(ParsedSuite.evals)` for output formatting.
- **`eval run` (M2)** — constructs `SuiteLoader` with the real
  `CapabilityGates` resolver; passes each `EvalSpec` from
  `ParsedSuite.evals` to the runner. The runner relies on the loader
  having already enforced FR-SCH1, FR-SCH2, and capability checks, so
  no re-validation happens at run time.
- **Test code** — injects a stub satisfying the `CapabilityResolver`
  Protocol (no inheritance needed because of `@runtime_checkable`).

## Design choices

### Why a Protocol instead of an ABC

`CapabilityResolver` is `typing.Protocol` rather than an `abc.ABC`
because:

- The M1 ordering tests need a recording stub that does not import
  `CapabilityGates` (which does not exist yet). Structural typing
  removes the import dependency entirely.
- `CapabilityGates` (T01.11) lives in a different module and would
  otherwise have to inherit a base from `loader.py`, creating a
  circular-import hazard.
- `@runtime_checkable` lets the test suite assert `isinstance()`
  without an explicit `register()` step.

### Why `SuiteLoaderError` is a tuple, not a base class

`SuiteLoaderError = (SchemaError, InvalidEvalId, UnresolvedCapability)`
is a plain tuple of exception types so callers can write
`except SuiteLoaderError as exc:` while the three concrete classes
remain disjoint. Introducing a shared base class would:

- Break the existing `SchemaError` and `InvalidEvalId` call sites
  authored in T01.04 and T01.05 (they already inherit from
  `Exception` directly).
- Force downstream consumers to deal with a new ABC for no benefit —
  the three classes are already exhaustively enumerated.

The pattern follows the standard library precedent of
`socket.errno`-style tuples used with `except`.

### Why the M1 default is permissive

`PermissiveCapabilityResolver` returns `()` so M1 commands can be
wired before T01.11 lands. The default is intentionally lenient
rather than strict because:

- Strict-by-default would make every M1 test that loads a manifest
  with `requires:` fail with `UnresolvedCapability` until T01.11
  is implemented, which would hide real defects.
- The real harness path (`eval run`) constructs `SuiteLoader`
  explicitly with `CapabilityGates(...)`, so the permissive default
  never leaks into production behaviour.

### Why `_expand_entry` preserves `parameterize` rows on the EvalSpec

`EvalSpec.from_dict` round-trips the `parameterize` block because the
runner needs the per-row token map to perform `{{key}}` substitution
in commands and expects. The loader's job is to materialise the id
expansion; the runtime substitution itself is the runner's
responsibility (M2 / M4).

## Notes / deferred work

- ExpectDSL wiring (T01.14, COMP-010) is NOT yet attached to the
  loader — the schema already validates the `expects:` block shape,
  and runtime predicate routing is M4 work. When T01.14 lands the
  loader will gain an optional `expect_dsl: ExpectDSL = field(...)`
  field analogous to `capability_resolver`.
- `ParsedSuite.required_binaries` and `.optional_capabilities` are
  kept as tuples of raw mappings rather than typed dataclasses; if
  T01.11 grows a typed `BinaryRequirement` model we will project the
  tuples through it then. The current shape is the smallest change
  that satisfies the schema and lets `eval doctor` enumerate the list.
- The `_RecordingResolver` test stub deliberately does NOT inherit
  from `CapabilityResolver`; the `@runtime_checkable` Protocol picks
  it up structurally. This is the intended pattern for the T01.11
  test surface as well.
- T01.08 (NFR-SEC1 path-traversal test set) cross-links the FR-SCH2
  guard at the integration layer. The loader is wired so that any
  new traversal pattern picked up by T01.08 fixtures is caught by
  the same `validate_eval_id` call sites — no loader changes needed.
