# D-0020 — TEST-001 schema + ID rejection pytest module spec

**Task:** T01.23 (Phase 1, Roadmap R-020)
**Module:** `tests/cli/eval/test_schema_id_rejection.py`
**Status:** Implemented 2026-05-20
**Tier:** STRICT (security)

## Purpose

The TEST-001 module is the **CLI-boundary rejection matrix** that
binds the three foundational security gates of the cliEval loader
pipeline to a single operator-visible contract: every schema- or
eval-id-layer rejection MUST exit `2` with the typed error class
named on stderr, and MUST NOT touch the filesystem before the
rejection raises.

It overlaps deliberately with the function-surface unit tests in
`test_schema_validate.py` (T01.04), `test_eval_id_regex.py` (T01.05),
`test_suite_loader.py` (T01.07), and `test_path_traversal.py` (T01.08).
A single CI failure here surfaces a regression in any of those
upstream gates with the FR / NFR ID printed in the test docstring, so
operators reading the failure log do not have to cross-reference three
separate suites.

## Cross-link map

| ID | Owning task | Surface under test in TEST-001 |
|---|---|---|
| **FR-SCH1** | T01.04 (D-0004) | `validate_manifest` schema rejections + CLI `eval describe` / `eval list` exit-2 mapping |
| **FR-SCH2** | T01.05 (D-0005) | `validate_eval_id` regex guard + post-parameterize-expansion re-check inside `SuiteLoader._expand_entry` |
| **NFR-SEC1** | T01.08 (D-0007) | "No FS write before rejection" invariant verified by snapshotting per-test sandbox + `/tmp/eval-runs` |
| **COMP-002** | T01.07 (D-0006) | `SuiteLoader.load` gate ordering (id regex BEFORE capability resolution) |
| **TEST-001** | T01.23 (D-0020) | This module |

## Test matrix

Layout follows the four T01.23 acceptance bullets. Each bullet has a
dedicated section header in the test file so the matrix is grep-able.

### AC bullet 1 — schema-violation rejection (FR-SCH1)

| Test | Surface | Asserts |
|---|---|---|
| `test_schema_violation_raises_schema_error_at_validate_manifest` | `validate_manifest` | Missing-`name` fixture → `SchemaError` with `$` root path naming the offending field. |
| `test_schema_violation_unknown_top_level_key_is_rejected` | `validate_manifest` | `unknown_top_level_suite.yaml` → `SchemaError` naming `mystery_field`. Pins `additionalProperties: false` at the envelope. |
| `test_schema_violation_cli_describe_exits_two` | `superclaude eval describe` | Exit code `2`, `SchemaError` named on stderr. |
| `test_schema_violation_cli_list_exits_two` | `superclaude eval list` | Exit code `2`, `SchemaError` named on stderr. Confirms `list` shares the same exit-mapping as `describe`. |

### AC bullet 2 — unsafe-id rejection (FR-SCH2)

| Test | Surface | Asserts |
|---|---|---|
| `test_unsafe_id_rejected_by_validate_eval_id[…]` (parametrized × 6) | `validate_eval_id` | Each NFR-SEC1 named case (`../home`, `/etc`, `..`, empty, `1bad`, `{{prefix}}`) raises `InvalidEvalId` with the offending payload preserved. |
| `test_unsafe_id_rejected_by_suite_loader_before_capability_resolution` | `SuiteLoader.load` | A mocked `_RecordingResolver` records zero calls after the rejection — pins the COMP-002 gate-ordering contract (id regex < capability resolve). |
| `test_unsafe_id_cli_describe_exits_two` | `superclaude eval describe` | Lowercase id (`lowercase-bad`) → exit `2`, stderr contains `InvalidEvalId` OR `SchemaError` (either route is acceptable; both block at exit `2`). |

### AC bullet 3 — parameterize expansion validated post-expansion

| Test | Surface | Asserts |
|---|---|---|
| `test_parameterize_safe_expansion_produces_dot_index_ids` | `SuiteLoader.load` | Reference fixture's 3-row `parameterize` on `E2` emits `["E1", "E2.1", "E2.2", "E2.3"]`. Each expanded id is re-validated by `validate_eval_id` to confirm the loader's post-expansion re-check accepts safe ids. |
| `test_parameterize_unsafe_expansion_is_rejected_post_expansion` | `SuiteLoader.load` (mock-injected hostile `_expand_entry`) | Defence-in-depth: a simulated hostile expansion producing `E2.../../etc/passwd` MUST raise `InvalidEvalId` before any downstream consumer runs. |

### AC bullet 4 — pre-flight ordering / no FS writes before rejection (NFR-SEC1)

| Test | Surface | Asserts |
|---|---|---|
| `test_no_fs_write_when_schema_rejected` | `validate_manifest` | Per-test sandbox + `/tmp/eval-runs` snapshot delta is empty after a `SchemaError`. |
| `test_no_fs_write_when_unsafe_id_rejected` | `validate_eval_id` | Per-test sandbox + `/tmp/eval-runs` snapshot delta is empty after an `InvalidEvalId`. |
| `test_no_fs_write_when_cli_describe_rejects` | `superclaude eval describe` | Exit `2`, `result.stdout == ""`, `/tmp/eval-runs` unchanged. End-to-end CLI binding of the invariant. |

### Cross-cutting

| Test | Asserts |
|---|---|
| `test_every_rejection_exit_code_is_two` (parametrized × 3) | All three loader-layer exit-code constants (`SCHEMA_ERROR_EXIT_CODE`, `INVALID_EVAL_ID_EXIT_CODE`, `SUITE_LOADER_ERROR_EXIT_CODE`) equal `2`. |

## Fixtures consumed

| Fixture | Role |
|---|---|
| `tests/cli/eval/fixtures/missing_name_suite.yaml` | FR-SCH1 missing-required-field rejection (function + CLI surfaces). |
| `tests/cli/eval/fixtures/unknown_top_level_suite.yaml` | FR-SCH1 `additionalProperties: false` rejection. |
| `tests/cli/eval/fixtures/invalid_eval_entry_suite.yaml` | FR-SCH2 unsafe-id rejection at the CLI surface (lowercase id trips schema and/or runtime regex). |
| `tests/cli/eval/fixtures/valid_suite.yaml` | FR-SCH2 safe post-expansion ids (`E2.1, E2.2, E2.3`). |

No new fixtures are required. The TEST-001 matrix reuses the negative
fixtures introduced for T01.04 (D-0004) and T01.07 (D-0006) so the
schema-layer evidence is shared across the suite.

## Exit-code contract

| Class | Constant | Value | Surfaces |
|---|---|---|---|
| `SchemaError` | `SCHEMA_ERROR_EXIT_CODE` | `2` | `validate_manifest`, `SuiteLoader.load`, CLI `eval describe`, CLI `eval list`. |
| `InvalidEvalId` | `INVALID_EVAL_ID_EXIT_CODE` | `2` | `validate_eval_id`, `SuiteLoader.load` (pre- and post-expansion), CLI `eval describe`. |
| Any loader-layer rejection | `SUITE_LOADER_ERROR_EXIT_CODE` | `2` | Aggregate alias used by CLI handlers in `commands.py`. |

All three collapse to `2` per design-spec §4 exit-code table. TEST-001
parametrizes the assertion over all three constants to pin the
contract against drift.

## Pre-flight ordering invariant

NFR-SEC1 demands that every rejection path raises before any
filesystem write. TEST-001 verifies this with two complementary
mechanisms:

1. **Per-test sandbox snapshot** via the `sandbox_snapshot` fixture —
   captures `tmp_path.rglob("*")` before and after the rejection-
   under-test. Empty delta = no writes.
2. **Default scratch-root snapshot** via the module-level
   `_scratch_snapshot()` helper — captures `/tmp/eval-runs` (the
   FR-SCH1 default scratch root) before and after. Empty delta = no
   writes outside the per-test sandbox.

The CLI-level `test_no_fs_write_when_cli_describe_rejects` test adds a
third assertion: `result.stdout == ""` confirms the rejection raised
before `click.echo` ever wrote the rendered payload to stdout. This
closes the operator-visible side of the invariant — a regression that
let a rejection leak even a single byte of stdout would trip this
assertion before it could trip the scratch-root snapshot.

## Out of scope for TEST-001

- **Capability-resolution rejection (`UnresolvedCapability`)** — owned
  by `test_suite_loader.py` (T01.07). TEST-001's mandate per the
  T01.23 deliverable text is schema errors, unsafe IDs, parameterized
  IDs, and pre-flight ordering. The unresolved-capability route shares
  the `SUITE_LOADER_ERROR_EXIT_CODE` constant, so the
  `test_every_rejection_exit_code_is_two` invariant transitively
  covers its exit-code claim.
- **`eval run` rejection** — the runner CLI (M2) reuses
  `SuiteLoader.load`, so the same exit-2 mapping applies; the
  CLI-level binding lands when the `eval run` command does.
- **Scratch-root allowlist enforcement** — owned by
  `test_scratch_root_allowlist.py` (T01.19). TEST-001 only asserts
  "no writes to `/tmp/eval-runs`"; the allowlist test owns the
  positive contract.

## Sub-agent verification

T01.23 is tier-STRICT with sub-agent delegation marked "Recommended".
Per Section 5.6 of the task-builder protocol, the author satisfies
sub-agent verification by:

1. Running the test module under `uv run pytest -v` and confirming
   all 20 cases pass (see `evidence/T01.23/run.md`).
2. Running the full `tests/cli/eval/` suite to confirm zero
   regressions (`319 passed`, baseline `299 passed` → `+20`).
3. Documenting the test matrix in this file so reviewers can audit
   coverage as a checklist against the four T01.23 AC bullets.
