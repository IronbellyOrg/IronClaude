# D-0002 — implementation notes

## Decisions made during build

1. **Schema dialect: Draft 2020-12.** Picked the current published draft to
   avoid a near-term re-pin once downstream tooling
   (`yaml-language-server`, IDE plugins) catches up. `jsonschema>=4.18`
   provides a `Draft202012Validator`; we pin `>=4.0.0` in `pyproject.toml`
   and the installed version is 4.26.

2. **Added `jsonschema>=4.0.0` to `[project] dependencies`.** Per design
   spec §5 ("`loader.py` validates with `jsonschema` (already a transitive
   dep)…") and AC3 (T01.17) allow-list `{pexpect, jsonschema}`, this is
   sanctioned by the roadmap. It was not actually transitive in the
   current venv (only `pyyaml` was present), so the dep had to be added
   explicitly. T01.17's snapshot diff will pick this up as an *expected*
   addition.

3. **Top-level `additionalProperties: false`.** The DM-011 acceptance
   wording "forbids unknown required keys" is satisfied by closing the
   top-level object shape: any key outside the 7 DM-011 fields raises a
   validation error. `defaults` keeps `additionalProperties: true` so
   suite authors can add Phase-4 knobs without bumping the schema.

4. **Schema-level FR-SCH2 regex on `evalEntry.id`.** Reusing the same
   regex documented in FR-SCH2 inside the schema means the YAML
   `yaml-language-server` integration flags traversal IDs at edit time,
   not just at runtime. T01.05 keeps the runtime `validate_eval_id`
   guard as the authoritative check (and re-applies it post-parameterize
   expansion), but having the regex here is a defence-in-depth bonus.

5. **`parameterizeRow.propertyNames` constrained to Python-identifier
   shape.** Template placeholders are referenced as `{{key}}` elsewhere
   in the entry; restricting them to `[A-Za-z_][A-Za-z0-9_]*` keeps the
   expansion grammar unambiguous. Values are scalars only — nested
   structures inside parameterize rows would make expansion semantics
   fuzzy and are deferred to a future schema version.

6. **`evalEntry.additionalProperties: false`.** Closes the DM-002 entry
   contract: new fields require a schema-version bump. This is the
   M1-Risk-3 forward-evolution lever called out in the roadmap.

7. **Fixture manifests stored under `tests/cli/eval/fixtures/`.** Keeps
   the test data co-located with the consuming tests rather than under
   `src/`. Three fixtures cover (a) positive baseline, (b) missing
   required top-level field, (c) unknown top-level key.

## Things deliberately NOT in scope of T01.02

- `validate_manifest(path)` — T01.04 (loader function returning
  `list[EvalSpec]` or raising `SchemaError`).
- `EvalSpec.from_dict()` — T01.03 (data-model layer).
- Runtime `validate_eval_id(eval_id)` — T01.05.
- Post-parameterize expansion semantics — T01.07 (SuiteLoader).
- `eval doctor --json` schema-violation rendering — T01.13.

## Risks / follow-ups

- If T01.07 introduces a new manifest field, it must land alongside a
  schema bump (`version: "1.1"`) to remain consistent with this
  document's M1-Risk-3 framing.
- `defaults` is intentionally open. If Phase 4 introduces unsafe knobs
  there, tighten `additionalProperties` in a schema bump rather than
  silently broadening the contract.
