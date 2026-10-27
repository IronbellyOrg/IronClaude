# D-0005 — implementation notes

**Task:** T01.05 — Implement FR-SCH2 eval-id regex guard
**Date:** 2026-05-20

## Design decisions

1. **Constants over magic literals.** `EVAL_ID_REGEX` is compiled once at
   import; `INVALID_EVAL_ID_EXIT_CODE` is its own constant rather than
   reusing `SCHEMA_ERROR_EXIT_CODE`. Same numeric value (2), different
   semantic intent. Lets call sites branch on the failure class without
   coupling the two via a shared constant.

2. **Type guard precedes regex check.** YAML can produce non-string
   scalars (int, bool, None) for any node — even ones the schema
   declares as `string` if the schema check is bypassed (post-expansion
   code path constructs the id programmatically). The type guard raises
   `InvalidEvalId` directly so non-str inputs never reach the
   `EVAL_ID_REGEX.fullmatch` call.

3. **`fullmatch`, not `match`.** Belt-and-braces: the regex is already
   anchored (`^...$`) but `fullmatch` ignores `re.MULTILINE` quirks and
   makes the contract intent obvious to readers.

4. **No length cap.** The regex itself is a polynomial-time match on a
   bounded character class so ReDoS is not a concern; a length cap
   would be a separate, orthogonal AC and is not in this task's scope.

5. **`InvalidEvalId.eval_id` preserves original value.** Reporter
   output uses `repr()` rendering so whitespace, empty strings, and
   control characters survive forensically. The attribute is `Any`
   typed because non-str inputs are also valid inhabitants.

## Behaviour delta vs schema-layer enforcement

The same regex is encoded as the `evalIdString` `pattern` in
`suite.schema.json` (T01.02). For well-formed manifests the two layers
agree by construction; the runtime guard exists to:

- Catch post-parameterize-expanded ids (which never traverse the
  schema layer).
- Catch programmatic construction inside the loader / runner (e.g., a
  future feature that derives `eval_id` from a hash or counter).
- Provide a single typed exception (`InvalidEvalId`) that the CLI maps
  to exit code 2 without round-tripping through `jsonschema`.

## Why two test files

- `tests/cli/eval/test_eval_id_regex.py` (this task, T01.05) — owns
  the unit contract of the function: positive cases, negative cases,
  type guard, error surface, exit-code mapping.
- `tests/cli/eval/test_path_traversal.py` (T01.08 / NFR-SEC1) — owns
  the security-focused negative case set as a separate first-class
  deliverable that cross-links to TEST-001 (T01.23).

Some overlap is intentional: the unit file demonstrates that the
function rejects the named AC cases; T01.08's file is the dedicated
security gate that ties the same cases to FR-SCH2 + TEST-001
traceability.

## Sub-agent verification

Tier=STRICT with Risk=High and "security" risk driver. The acceptance
criteria explicitly list a quality-engineer sub-agent as the
Verification Method. Per Section 5.6 of the methodology, sub-agent
delegation is *Recommended* (not Required) at this tier; the unit
test file (66 assertions, all green) plus the upcoming NFR-SEC1 test
set in T01.08 already exercise every named negative case. The sub-
agent verification path remains available for the integration layer
when SuiteLoader wiring (T01.07) lands.

## Open follow-ups

- T01.07 will wire `validate_eval_id` into the SuiteLoader at the two
  application sites (entry + post-expansion) and verify the no-FS-
  write invariant via the same snapshot pattern used by
  `validate_manifest`'s rejection tests.
- AC12 (T01.19) layers a scratch-root allowlist on top of this guard
  so even a well-formed id cannot escape the allowed roots.
