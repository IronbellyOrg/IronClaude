# D-0019 — `superclaude eval describe` subcommand spec

**Task:** T01.22 (Phase 1, Roadmap FR-CLI3 / R-019)
**Module:** `src/superclaude/cli/eval/commands.py`
**CLI surface:** `superclaude eval describe --suite <token> [--eval <id>] [--json] [--suites-dir PATH]`
**Status:** Implemented 2026-05-20

## Command surface

| Flag | Type | Required | Effect |
|---|---|---|---|
| `--suite` | string | yes | Suite name, filename stem, or direct path. Resolution precedence below. |
| `--eval` | string | no | Filter output to one post-expansion eval id. Missing id → `EvalNotFound` (exit 2). |
| `--json` | bool flag | no | Emit JSON. Default output is YAML (block style, unicode-friendly). |
| `--suites-dir` | path | no | Override the directory used for name / stem lookups. Defaults to `src/superclaude/cli/eval/suites/`. |

### Exit codes

| Code | Trigger |
|---|---|
| `0` | Manifest validated and printed. |
| `2` (`SUITE_LOADER_ERROR_EXIT_CODE`) | Schema / id-regex / capability rejection. Stderr names the typed error class (`SchemaError`, `InvalidEvalId`, `UnresolvedCapability`). |
| `2` (`SUITE_NOT_FOUND_EXIT_CODE`) | `--suite` token did not resolve to any manifest. Stderr names `SuiteNotFound` and the searched directory. |
| `2` (`EVAL_NOT_FOUND_EXIT_CODE`) | `--eval` id did not match any post-expansion id. Stderr names `EvalNotFound`, the suite name, and the known id list. |

All three "rejection" codes are intentionally `2` so operators see a
single "harness rejected the describe request" outcome regardless of
which gate fired. Per-class constants are kept so call sites and tests
can branch on intent.

## `--suite` resolution

`resolve_suite_manifest(suite, suites_dir)` walks three rules in order
(first match wins):

1. `suite` is itself an existing file path → return it verbatim. Lets
   operators describe an out-of-tree manifest by path without copying
   it into `suites_dir`.
2. `suites_dir / f"{suite}.yaml"` exists → return it. Matches the
   filename-stem convention used by built-in suites that will land in
   later milestones.
3. Scan `discover_suite_manifests(suites_dir)` and return the first
   manifest whose schema-validated `name:` field equals `suite`.
   Broken neighbours are skipped silently — only the matching manifest
   needs to validate.

If no rule matches, `SuiteNotFound` is raised and the CLI exits 2 with
the typed class name on stderr.

## Output schema

### Default (YAML)

`render_describe_yaml(payload)` renders block-style YAML with
`sort_keys=False` so the field ordering matches `suite.schema.json`
(envelope: `name`, `version`, `description`, `defaults`,
`required_binaries`, `optional_capabilities`, `evals`). `allow_unicode=True`
preserves em-dashes and other non-ASCII characters that appear in real
manifest titles.

### `--json`

`render_describe_json(payload)` emits `json.dumps(payload, indent=2,
sort_keys=True)` so the JSON output is byte-stable across hosts and
Python versions (verified by `test_render_describe_json_is_deterministic`
and `test_cli_describe_yaml_is_deterministic`).

### Envelope shape (no `--eval`)

`_parsed_suite_to_dict(parsed)` projects a `ParsedSuite` into:

```yaml
name: <string>
version: <string>
description: <string>
defaults: <mapping>
required_binaries: [ <requiredBinary>, ... ]
optional_capabilities: [ <optionalCapability>, ... ]
evals: [ <evalEntry>, ... ]   # post-parameterize-expansion
```

`evals` is the **post-parameterize-expansion** list (`parsed.evals`),
not the raw `evals[]` length. A manifest with one static row plus one
parameterized row of three values prints four `evals[]` entries with
ids `E1, E2.1, E2.2, E2.3`.

### Single-eval projection (`--eval <id>`)

`_evalspec_to_dict(spec)` projects an `EvalSpec` into the
`evalEntry` shape (no suite envelope):

```yaml
id: <string>             # already FR-SCH2-validated post-expansion
title: <string>
category: <string>       # omitted when ""
requires: [<string>, ...]   # omitted when empty
timeout_sec: <int>       # omitted when None
isolation: <mapping>     # omitted when None
inputs: [<mapping>, ...] # omitted when empty
expects: [<mapping>, ...] # omitted when empty
parameterize: [<mapping>, ...]  # preserved on expanded entries
```

Optional fields are omitted when they hold the dataclass default
(`category=""`, empty sequences, `timeout_sec=None`). This honours the
T01.22 Notes contract: "Output mirrors validated manifest exactly; no
editorial transformation" — an eval that did not declare `category:`
in YAML does not gain one in the description.

## Validation order (FR-CLI3 AC)

`describe_suite()` runs the full `SuiteLoader.load()` gate chain
**before any rendering**:

1. Resolve `--suite` to a manifest path (no FS write).
2. `SuiteLoader.load()` — schema (FR-SCH1) → static-id regex
   (FR-SCH2) → capability resolution (COMP-009 surface) →
   parameterize expansion → expanded-id regex re-check (FR-SCH2).
3. Optional `--eval` id lookup against the post-expansion list.
4. Render YAML / JSON.

Validation rejections raise from step 2 — `click.echo` of the payload
in step 4 is never reached. Verified by
`test_cli_describe_validation_runs_before_any_stdout`, which asserts
`result.stdout == ""` on a schema-rejection path.

## Loader integration

`describe_suite(suite, *, suites_dir, eval_id=None, loader=None)` is
the function the CLI handler delegates to. The `loader` parameter is
injectable so tests can stub `SuiteLoader` without touching the file
system. The default loader uses `PermissiveCapabilityResolver` (same
as `eval list`) — capability gating for `describe` is intentionally
permissive because describing a manifest is a read-only operation that
should not require the runtime binary set on the host.

## Acceptance criteria → implementation map

| AC bullet (T01.22) | Implementation site |
|---|---|
| `superclaude eval describe --suite <name>` prints validated post-parameterize manifest content. | `eval_describe` Click handler + `describe_suite` + `render_describe_yaml`; covered by `test_cli_describe_prints_yaml_envelope`, `test_cli_describe_json_emits_valid_json`. |
| `--eval <id>` filters to a single eval; missing id exits 2 with `EvalNotFound`. | `describe_suite(eval_id=...)` + `EvalNotFound`; covered by `test_cli_describe_filters_to_single_eval_yaml`, `test_cli_describe_filters_to_post_expansion_id`, `test_cli_describe_exit2_on_missing_eval`. |
| Validation runs before any print operation; invalid manifest exits 2. | `SuiteLoader.load()` raises pre-render; covered by `test_cli_describe_exit2_on_schema_violation`, `test_cli_describe_exit2_on_invalid_eval_id`, `test_cli_describe_validation_runs_before_any_stdout`. |
| `artifacts/D-0019/spec.md` records flag semantics. | This file. |

## Test injection seams

| Seam | How tests use it |
|---|---|
| `--suites-dir` | Fixture suites copied into `tmp_path` per test; the override avoids polluting the package suites directory. |
| `describe_suite(loader=...)` | Inject a stubbed `SuiteLoader` for tests that need full control over schema / regex / capability gates. |
| `_evalspec_to_dict` / `_parsed_suite_to_dict` | Pure projections; covered directly by unit tests so the renderer contract is verified without spinning up Click. |
| `resolve_suite_manifest` | Pure function over `(token, suites_dir)`; covered by direct tests for each resolution rule plus the broken-neighbour case. |

## Out of scope for T01.22

- Recursive manifest discovery — only the top-level `*.yaml` glob is
  searched. Nested manifests would require a roadmap extension.
- Template substitution of `{{key}}` tokens inside expanded evals —
  substitution happens at the runtime layer (M2/M3 runner work);
  describe preserves the parameterize block verbatim on expanded
  entries so operators can still see the substitution intent.
- Coloured / pretty-printed output beyond YAML / JSON — adding a
  table-style mode belongs to a future `eval describe --format table`
  enhancement.
