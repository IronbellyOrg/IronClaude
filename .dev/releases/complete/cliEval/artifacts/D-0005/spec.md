# D-0005 — `validate_eval_id()` FR-SCH2 eval-id regex guard

**Task:** T01.05 (Phase 1, Roadmap FR-SCH2 / R-005)
**Module:** `src/superclaude/cli/eval/loader.py`
**Public surface:** `validate_eval_id`, `InvalidEvalId`, `EVAL_ID_REGEX`, `INVALID_EVAL_ID_EXIT_CODE`
**Status:** Implemented 2026-05-20
**Tier:** STRICT (security-critical, critical-path override)

## Function contract

```python
def validate_eval_id(eval_id: str) -> None
```

- **Input:** an eval identifier as it appears either in the manifest
  (pre-expansion) or after parameterize expansion. The function accepts
  any value at runtime so non-string scalars (`int`, `bool`, `None`,
  `bytes`) that may leak through YAML decoding are rejected via the
  type guard rather than slipping past the regex check.
- **Output:** `None` on success (the function is a pure guard).
- **Error behaviour:** raises `InvalidEvalId` carrying the offending
  value on `InvalidEvalId.eval_id`. CLI callers MUST map this to
  `INVALID_EVAL_ID_EXIT_CODE` (= 2).

## The regex

```python
EVAL_ID_REGEX = re.compile(r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$")
```

This is the single source of truth for the runtime guard. The same
regex literal is encoded into `suites/suite.schema.json` (T01.02) as
the `evalIdString` `pattern`, so schema validation rejects unsafe
**static** ids at the schema layer too; `validate_eval_id` is the
authoritative runtime check the security model relies on (especially
for post-parameterize-expanded ids that never touch the schema).

The pattern accepts:

| Shape           | Examples                          |
|-----------------|-----------------------------------|
| Canonical eval  | `E1`, `E2`, `E15`, `D15`          |
| Parameter-ized  | `E2.1`, `E2.2`, `E2.10`, `Foo42.7`|
| Single letter   | `A`, `Z9`                         |
| Mixed-case body | `Test1`, `ABC123`                 |

It rejects everything else; the named negative cases below are the
floor, not the ceiling.

## Negative-case checklist (FR-SCH2 / NFR-SEC1)

| Category                  | Examples                                                 | Why it must fail                                              |
|---------------------------|----------------------------------------------------------|---------------------------------------------------------------|
| Empty string              | `""`                                                     | AC bullet; trivially escapes `home_root / "" / "home"`        |
| Path-traversal prefix     | `../home`, `../../etc`, `..`                             | AC bullet; escapes the scratch root via `Path` join semantics |
| Absolute path             | `/etc`, `/tmp/eval-runs`                                 | AC bullet; `Path("/abs") / "home"` discards `home_root`       |
| Embedded separator        | `foo/bar`, `foo\\bar`, `E1/x`, `./foo`, `.`              | Lets attacker carve sub-directories under `home_root`         |
| Leading-digit id          | `1E`, `9`, `0E`, `1`, `12.3`                             | AC bullet; the schema also bans this — runtime mirrors        |
| Template token leakage    | `{{prefix}}`, `E{{p}}`, `${var}`, `<id>`, `%name%`       | AC bullet; an un-substituted token must NEVER reach the FS    |
| Whitespace / control char | ` E1`, `E1 `, `E 1`, `\tE1`, `E1\n`, `E1\x00`            | Defence in depth — control chars confuse downstream consumers |
| Wrong character class     | `e1`, `eval1`, `E-1`, `E_1`                              | Underscores and lowercase are excluded by the regex anchor    |
| Malformed decimal         | `E1.`, `E.1`, `E1..1`, `E1.1.1`, `E1.1.`                 | Only one `.N` decimal allowed (mirrors parameterize semantics)|
| Non-string scalar         | `None`, `1`, `1.0`, `b"E1"`, `["E1"]`, `("E1",)`, `{...}`| YAML may decode bare scalars; type guard runs before regex    |

> All entries above are exercised by `tests/cli/eval/test_eval_id_regex.py`
> (T01.05 unit surface, 66 assertions). The dedicated path-traversal
> negative-case test set (T01.08 / NFR-SEC1) cross-links the same
> categories at the integration layer.

## Error → exit-code mapping

| Trigger                                      | Raised           | Exit code                  |
|----------------------------------------------|------------------|----------------------------|
| `eval_id` is not `str`                       | `InvalidEvalId`  | `INVALID_EVAL_ID_EXIT_CODE`|
| `eval_id` does not match `EVAL_ID_REGEX`     | `InvalidEvalId`  | `INVALID_EVAL_ID_EXIT_CODE`|

`INVALID_EVAL_ID_EXIT_CODE = 2` is kept as its own constant (even though
the value equals `SCHEMA_ERROR_EXIT_CODE`) so call sites can branch on
the *intent* of the rejection without coupling the two failure classes
together. Both surface to operators as the same "harness rejected the
manifest before any filesystem write" outcome (design-spec §4).

## Application sites (FR-SCH2 ordering)

`validate_eval_id` is invoked in two places by the SuiteLoader
orchestrator (T01.07 / COMP-002):

1. **At loader entry**, against every static `evals[].id` in the parsed
   manifest. This is redundant with the schema layer for well-formed
   manifests but the security model treats the runtime guard as
   authoritative.
2. **After parameterize expansion**, against every generated id
   (`E2.1`, `E2.2`, ...). This is the *load-bearing* call — it closes
   the path-traversal attack surface where a malicious parameterize
   row could otherwise inject `..` or `/` into an id that
   `HomeIsolation` interpolates into `home_root / eval_id / home`.

Both call sites MUST run **before any filesystem write** (NFR-SEC1
invariant). The unit tests in this task simulate the post-expansion
guard call directly; the actual SuiteLoader wiring lands in T01.07 and
its integration test verifies the no-FS-write contract via the same
`/tmp/eval-runs` snapshot pattern that `validate_manifest` already
honours (`test_rejection_does_not_write_to_default_scratch_root`).

## Acceptance criteria → implementation map

| AC bullet (T01.05) | Implementation site |
|---|---|
| `validate_eval_id()` in `src/superclaude/cli/eval/loader.py` raises `InvalidEvalId` for inputs `../home`, `/etc`, `..`, empty string, leading-digit IDs, and template tokens inside id. | `tests/cli/eval/test_eval_id_regex.py::test_validate_eval_id_rejects_traversal_and_separator_patterns`, `test_validate_eval_id_rejects_empty_string`, `test_validate_eval_id_rejects_leading_digit_ids`, `test_validate_eval_id_rejects_template_token_patterns`. |
| Guard is applied at SuiteLoader entry AND after parameterize expansion. | Unit-level surface here (`test_validate_eval_id_rejects_unsafe_expanded_id`, `test_validate_eval_id_accepts_safe_expanded_id`, `test_validate_eval_id_rejects_traversal_after_substitution`); SuiteLoader wiring + integration assertion lands in T01.07. |
| `InvalidEvalId` propagates to process exit code 2 via the loader error mapping. | `INVALID_EVAL_ID_EXIT_CODE = 2` exported from the loader; asserted by `test_invalid_eval_id_exit_code_is_two`. |
| `TASKLIST_ROOT/artifacts/D-0005/spec.md` documents the regex and all negative cases. | This document (see "The regex" + "Negative-case checklist" sections). |

## Caller contract (downstream consumers)

- **COMP-002 `SuiteLoader` (T01.07)** — calls `validate_eval_id` twice
  per eval (entry + post-expansion) as the authoritative runtime guard.
  Maps `InvalidEvalId` to `INVALID_EVAL_ID_EXIT_CODE`.
- **`HomeIsolation` (Phase 2)** — MAY re-apply the guard as a
  belt-and-braces check immediately before `home_root / eval_id /
  "home"` is constructed. This is defensive: the SuiteLoader should
  already have rejected the id, but `HomeIsolation` is the last layer
  before an actual FS write so the cost of the extra check (one
  compiled regex match) is negligible relative to the failure mode.

## Notes / deferred work

- `EVAL_ID_REGEX` is the **runtime** copy of the FR-SCH2 regex. The
  **schema** copy lives in `suites/suite.schema.json`. Keeping them in
  sync is a manual contract for now; design-spec §5 explicitly calls
  out that the runtime guard is authoritative, so a schema-vs-runtime
  drift would be detected by the unit tests in this task.
- The function is intentionally narrow (no logging, no allow-list, no
  length cap). Path-containment for the scratch root is a separate
  concern handled by AC12 (T01.19) and `HomeIsolation` (Phase 2).
- `InvalidEvalId.eval_id` stores the original value (including non-str
  inputs) so reporter output can render the offending payload
  verbatim. `__str__` uses `repr()` so whitespace, empty strings, and
  control characters survive into stderr without being silently
  collapsed.
