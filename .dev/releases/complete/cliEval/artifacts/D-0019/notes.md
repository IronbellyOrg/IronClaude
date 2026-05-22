# D-0019 — implementation notes

## Design choices

### Three-rule `--suite` resolution

The acceptance criterion `describe --suite <name>` is loose about what
"name" means. We support three resolution rules so operators can use
the most natural reference:

1. **Direct path** — `superclaude eval describe --suite ./my-suite.yaml`.
   Useful when developing a manifest outside `cli/eval/suites/`.
2. **Filename stem** — `--suite reference` resolves to
   `<suites-dir>/reference.yaml`. Cheap (no manifest load) and matches
   the convention built-in suites will follow.
3. **`name:` field** — last resort: scan and match the manifest's
   declared `name`. Required for fixtures like `valid_suite.yaml` whose
   filename diverges from the manifest name (`reference`).

Rule 3 silently skips broken neighbours so a single bad manifest in
`suites_dir` does not block lookups of unrelated suites.

### Two-shape output

`describe` returns one of two shapes depending on `--eval`:

- **Envelope** (no `--eval`) — the full manifest projection. Matches
  the schema's top-level shape (`name`, `version`, `description`,
  `defaults`, `required_binaries`, `optional_capabilities`, `evals`).
- **Single entry** (with `--eval`) — just the `evalEntry` projection.
  No suite envelope. This is the operator-facing answer to "what would
  run if I executed eval X?" and matches the `manifest.evals[i]` shape
  one-to-one.

The renderer functions (`render_describe_yaml`, `render_describe_json`)
don't care which shape they receive — they emit any dict.

### Omitting default optional fields

`_evalspec_to_dict` omits fields that hold their dataclass default:

- `category=""` → omitted
- `requires=()`, `inputs=()`, `expects=()`, `parameterize=()` → omitted
- `timeout_sec=None`, `isolation=None` → omitted

Rationale: T01.22 Notes says "Output mirrors validated manifest
exactly; no editorial transformation." An eval that did not declare
`category:` in YAML should not gain a `category: ""` line in the
description output. Required fields (`id`, `title`) always appear.

### Validation BEFORE rendering

The Click handler runs the full `SuiteLoader.load()` gate chain inside
`describe_suite`, so any schema / id-regex / capability rejection
raises an exception that the `try/except` block maps to exit 2 BEFORE
`click.echo` of the payload is reached. Verified by snapshot test
`test_cli_describe_validation_runs_before_any_stdout`.

### YAML output settings

`yaml.safe_dump(payload, sort_keys=False, default_flow_style=False,
allow_unicode=True)`:

- `sort_keys=False` preserves the field order our projection produces
  (matches `suite.schema.json` declaration order).
- `default_flow_style=False` keeps block style throughout so the YAML
  reads like the source manifest (no inline `{a: 1, b: 2}` collapses).
- `allow_unicode=True` keeps em-dashes and other non-ASCII characters
  in titles intact instead of escaping them to `—` etc.

### JSON output determinism

`json.dumps(payload, indent=2, sort_keys=True)` matches the
`eval list --json` contract. Byte-stable across hosts and Python
versions; verified by the determinism test.

## Test seams

Tests inject a `tmp_path` via `--suites-dir`, copy fixture YAML files
into it, and exercise both the function-level API (`describe_suite`,
`resolve_suite_manifest`, `_evalspec_to_dict`, `_parsed_suite_to_dict`)
and the Click CLI surface via `CliRunner`.

## Cross-cuts

- **FR-SCH1 (T01.04 / R-004)** — schema validation runs via
  `SuiteLoader.load()`, which delegates to `validate_manifest`. Schema
  rejection → exit 2 with `SchemaError` on stderr.
- **FR-SCH2 (T01.05 / R-005)** — eval-id regex runs pre- AND
  post-expansion inside `SuiteLoader`. Unsafe ids never reach `describe`'s
  print path.
- **COMP-002 (T01.07 / R-006)** — `SuiteLoader.load()` is the single
  ingress for the gate chain; `describe` re-uses it verbatim.
- **FR-CLI2 (T01.21 / R-018)** — `eval list` and `eval describe` share
  `discover_suite_manifests` + Click group registration patterns.
