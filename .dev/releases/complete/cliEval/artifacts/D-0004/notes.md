# D-0004 — implementation notes

## Decisions made during build

1. **`SchemaError` collects every violation, not just the first.**
   `jsonschema` returns one error per failure via `iter_errors`; the
   default behaviour of `validate(...)` raises only the first. We
   collect all errors so a single CLI run surfaces every shape problem
   to the manifest author instead of forcing a fix → re-run → next-error
   loop. Sorting on `(absolute_path, message)` keeps the list stable.

2. **JSON-path rendering uses `$`-rooted dot/bracket notation.** This
   matches the convention used by `jq -e`, `jsonpath`, and the
   `mcp-eval` reference port. `$` is reserved for top-level missing
   required fields where jsonschema leaves `absolute_path` empty —
   without `$`, those errors would render as the empty string and
   become unidentifiable in stderr.

3. **`SCHEMA_ERROR_EXIT_CODE = 2` is a module-level constant.** The CLI
   boundary (T01.13 `eval doctor`, M2 `eval run`) imports the symbol
   instead of duplicating the literal. This keeps the design-spec §4
   exit-code table and the implementation in lockstep.

4. **YAML decode + missing-file + non-mapping all map to `SchemaError`.**
   CLI callers only need to catch one typed error to honour FR-SCH1
   ("exits 2 before any FS write"). `FileNotFoundError`, `OSError`, and
   `yaml.YAMLError` would otherwise leak out as generic exceptions and
   force every caller to maintain its own translation layer.

5. **Schema is loaded via `yaml.safe_load`.** The schema file is
   JSON-formatted but `yaml.safe_load` accepts JSON as a strict subset
   of YAML and avoids pulling in an additional import path. The
   alternative (`json.loads`) would force a second decoder for no
   benefit.

6. **`Path.read_text` chosen over `open(...)` context managers.**
   Makes the FR-SCH1 invariant ("no filesystem writes before
   validation succeeds") trivially auditable — every IO line in
   `loader.py` reads from a `Path`; the absence of `Path.write_text`,
   `os.mkdir`, etc. is verifiable by grep.

7. **`EvalSpec` projection happens AFTER validation passes.** This
   keeps the function's pre-condition trivially provable: by the time
   we hit `EvalSpec.from_dict`, the manifest is schema-valid, so the
   factory's `id`/`title` requirement cannot fail. Any `ValueError`
   from the factory would indicate a contract bug rather than user
   error.

8. **Test fixture `invalid_eval_entry_suite.yaml` added.** The
   T01.02 fixtures only cover top-level violations; we needed a
   manifest with a violation *nested inside* `evals[]` to verify the
   `$.evals[0].id` JSON-path rendering. The fixture deliberately
   violates two rules at once (missing `title`, lower-case id) so the
   determinism test has a non-trivial multi-violation case to compare.

## Things deliberately NOT in scope of T01.04

- Runtime `validate_eval_id(eval_id)` — T01.05 (FR-SCH2). The schema
  enforces the regex on *static* ids; post-parameterize-expanded ids
  still need the runtime guard, which T01.07 wires.
- CLI wiring (`eval doctor`, `eval run`) — T01.13 / M2.
- Capability resolution / parameterize expansion — T01.07 (SuiteLoader).
- Scratch-root allowlist enforcement — T01.19 (AC12).

## Risks / follow-ups

- The `_format_json_path` helper hand-rolls a JSON-pointer-ish notation;
  if downstream tooling later expects RFC 6901 JSON Pointers we will
  need to translate. Keeping the helper isolated makes that swap a
  one-function change.
- `SchemaError.violations` is currently a tuple of plain `(path, msg)`
  pairs. If the reporter needs richer rendering (severity, schema
  pointer, etc.) we can promote it to a frozen dataclass without
  changing the error-raising sites — `_Violation` already exists for
  internal use.
- `jsonschema>=4.0.0` is now a runtime dep (already added in T01.02).
  T01.17's `make verify-deps` snapshot diff will continue to allow it
  per the AC3 allow-list.
