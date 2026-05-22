# D-0018 — `superclaude eval list` subcommand spec

**Task:** T01.21 (Phase 1, Roadmap FR-CLI2 / R-018)
**Module:** `src/superclaude/cli/eval/commands.py`
**CLI surface:** `superclaude eval list [--json] [--suites-dir PATH]`
**Status:** Implemented 2026-05-20

## Command surface

| Flag | Type | Effect |
|---|---|---|
| `--json` | bool flag | Emit a JSON array of `{name, version, eval_count}` entries instead of the human-readable text. |
| `--suites-dir` | path | Override the default manifest directory. Defaults to `src/superclaude/cli/eval/suites/` (the package suites directory). |

Exit codes:

* `0` — every discovered manifest loaded green, or no manifests were
  found. The empty-directory case is explicitly part of the contract
  (FR-CLI2 AC).
* `2` (`SUITE_LOADER_ERROR_EXIT_CODE`) — at least one manifest failed
  schema validation, eval-id regex, or capability resolution. The
  stderr line names the offending manifest and the typed error class
  (`SchemaError`, `InvalidEvalId`, `UnresolvedCapability`) so operators
  can locate the failure without digging through stack traces.

## Output schema

### Human (default)

Rendered by `render_list_text(summaries)`:

```
superclaude eval list:
  - <name> (version <version>, <count> eval[s])
  - <name> (version <version>, <count> eval[s])
```

The empty case prints `  (no suites found)`. Pluralisation toggles
between `eval` (1) and `evals` (0 or >=2) so the output reads
naturally without losing parseability for downstream awk-style
consumers.

### JSON (`--json`)

```json
[
  { "name": "<string>", "version": "<string>", "eval_count": <int> },
  …
]
```

`json.dumps(payload, indent=2, sort_keys=True)` guarantees byte-level
determinism across invocations on a stable host (verified by
`test_cli_list_json_is_deterministic_across_invocations`).

## Eval count semantics

`eval_count` is the **post-parameterize-expansion** count
(`len(ParsedSuite.evals)`), not the raw `evals[]` length. This reflects
the operator-facing question "how many evals would run if I executed
this suite?" rather than the manifest's row count. A manifest with one
static row plus one parameterized row of three values reports
`eval_count: 4`, not `eval_count: 2`.

## Discovery rules

`discover_suite_manifests(suites_dir)` returns the glob
`suites_dir/*.yaml` sorted by filename:

* Missing or non-directory `suites_dir` → empty list (no error). A
  fresh checkout that has not yet populated built-in suites must not
  break `eval list`.
* Non-YAML files (`README.md`, `suite.schema.json`) are filtered out by
  the `*.yaml` glob.
* The sort is alphabetical by filename, providing deterministic output
  regardless of filesystem iteration order.

## Loader integration

`summarize_suites(suites_dir, *, loader=None)` funnels every discovered
manifest through `SuiteLoader.load()` so the same five-stage gate chain
(schema → static id regex → capability resolution → parameterize
expansion → expanded-id regex re-check) that protects `eval run`
gates `eval list` too. There is no separate fast-path that bypasses
FR-SCH2 — listing an unsafe manifest fails closed with exit 2.

The `loader` parameter is injectable for tests that want to stub schema
or capability gates without touching the file system.

## Test injection seams

| Seam | How tests use it |
|---|---|
| `--suites-dir` | Fixture suites are copied into a tmp dir per test; the override avoids polluting the package suites directory. |
| `summarize_suites(loader=...)` | Inject a stubbed `SuiteLoader` for tests that need full control over schema / regex / capability gates. |
| `discover_suite_manifests` | Pure function over `Path`; tests call it directly on tmp dirs to verify the sort + filter contracts. |

## Wiring

* `eval_list` is registered on the existing `eval_group` (`@eval_group.command("list")`).
* `eval_group` is already wired into `superclaude.cli.main` via
  `main.add_command(eval_group, name="eval")` from T01.13 — no new
  top-level wiring required.

## Acceptance criteria → implementation map

| AC bullet (T01.21) | Implementation site |
|---|---|
| `superclaude eval list` exits 0 with at least one suite present and zero suites present (empty-directory case). | `eval_list` Click handler + `render_list_text` empty branch; covered by `test_cli_list_exits_zero_on_empty_directory`, `test_cli_list_exits_zero_with_default_suites_dir`, `test_cli_list_prints_name_version_eval_count`. |
| `--json` emits a JSON array with `{name, version, eval_count}` entries. | `list_payload` + `json.dumps(..., sort_keys=True)`; covered by `test_cli_list_json_emits_array_of_summaries`, `test_cli_list_json_empty_directory_returns_empty_array`. |
| Output is deterministic for a given suite directory (sorted by filename). | `discover_suite_manifests` returns `sorted(...)`; covered by `test_cli_list_json_is_deterministic_across_invocations`, `test_cli_list_output_is_sorted_by_filename`. |
| `artifacts/D-0018/spec.md` records the output schema. | This file. |

## Out of scope for T01.21

- Recursive manifest discovery — only the top-level `*.yaml` glob is
  searched. Nested manifests would require a roadmap extension.
- Filtering by category / capability — FR-CLI2 is enumeration-only;
  filtering belongs to a future `eval list --filter …` enhancement.
- Hot-reloading of the suite directory — `summarize_suites` re-reads on
  every invocation; there is no cache.
