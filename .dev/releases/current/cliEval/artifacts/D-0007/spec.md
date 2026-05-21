# D-0007 — NFR-SEC1 path-traversal prevention test set

**Task:** T01.08 (Phase 1, Roadmap NFR-SEC1 / R-007)
**Module:** `tests/cli/eval/test_path_traversal.py`
**Status:** Implemented 2026-05-20
**Tier:** STRICT (security-critical, critical-path override)

## Purpose

This deliverable is the **dedicated negative-case security gate** for the
FR-SCH2 eval-id regex guard. It exists alongside the function-surface
unit tests in `tests/cli/eval/test_eval_id_regex.py` (T01.05 / D-0005)
so the named NFR-SEC1 rejection categories have their own first-class
auditable checklist, organised by attack class rather than by function
contract.

Each test pins exactly one named NFR-SEC1 / FR-SCH2 acceptance case
and asserts `InvalidEvalId` is raised before any filesystem write.

## Negative-case checklist (AC bullet 1, T01.08)

| # | AC case                  | Test name                                                         | Payload(s)                                |
|---|--------------------------|-------------------------------------------------------------------|-------------------------------------------|
| 1 | `../home`                | `test_rejects_dotdot_home_traversal_prefix`                       | `../home`                                 |
| 2 | `/etc`                   | `test_rejects_absolute_etc_path`                                  | `/etc`                                    |
| 3 | `..`                     | `test_rejects_bare_dotdot`                                        | `..`                                      |
| 4 | empty                    | `test_rejects_empty_string`                                       | `""`                                      |
| 5 | leading-digit            | `test_rejects_leading_digit_ids`                                  | `1bad`, `9E`, `0`, `12.3`                 |
| 6 | template-token           | `test_rejects_template_token_patterns`                            | `{{prefix}}`, `E{{p}}`, `E1{{n}}`, `{prefix}` |
| 7 | parameterized-unsafe     | `test_rejects_parameterized_unsafe_expansion_in_loader`           | `E2.../../etc/passwd` (post-expansion)    |

Plus two cross-cutting invariants:

| Invariant                                   | Test name                                       |
|---------------------------------------------|-------------------------------------------------|
| Exit-code mapping (= 2)                     | `test_invalid_eval_id_exit_code_is_two`         |
| Pure guard — no FS write on rejection path  | `test_no_fs_write_when_traversal_id_rejected`   |

## Cross-links

Per AC bullet 3 (T01.08): the test module's docstring header records the
following cross-links explicitly, so traceability survives independent of
this spec document:

- **FR-SCH2** — eval-id regex guard (T01.05 / D-0005). Runtime
  implementation under test: `superclaude.cli.eval.loader.validate_eval_id`.
- **NFR-SEC1** — path-traversal prevention (this file's owning AC).
- **TEST-001** — schema + ID rejection tests (T01.23). T01.23 will fold
  these cases into the CLI-level rejection matrix; until then, this
  module is the authoritative checklist.
- **COMP-002 SuiteLoader** (T01.07) — applies `validate_eval_id` at
  manifest entry AND after parameterize expansion. The
  parameterized-unsafe test exercises that second site.

## Why a parameterized-unsafe *integration* test

The parameterize re-check at `SuiteLoader._expand_entry` is the
**load-bearing** FR-SCH2 application — it closes the path-traversal
attack surface where a malicious parameterize row (or a future
expansion strategy that interpolates user-controlled values) could
inject `..` or `/` into an id that downstream isolation layers later
interpolate into `home_root / eval_id / "home"`.

Reproducing this at the integration layer (via `SuiteLoader.load()`
with a hostile `_expand_entry` patch) proves the loader's
post-expansion re-check actually fires. A pure unit-level call to
`validate_eval_id("E2.../../etc/passwd")` would only prove the regex
function rejects — not that the loader *invokes* the function at the
expansion site.

## Acceptance criteria → implementation map

| AC bullet (T01.08)                                                                                                       | Implementation site                                                                  |
|--------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| File `tests/cli/eval/test_path_traversal.py` exists and contains tests for the 7 named NFR-SEC1 cases.                   | All 7 named tests above.                                                              |
| `uv run pytest tests/cli/eval/test_path_traversal.py -v` exits 0 with ≥ 7 passing tests.                                  | 15 tests pass (see `evidence/T01.08/pytest-targeted.log`).                            |
| Cross-link to FR-SCH2 (T01.05) and TEST-001 (T01.23) recorded in test docstring header.                                  | Module docstring "Cross-links" section in `test_path_traversal.py`.                  |
| `TASKLIST_ROOT/artifacts/D-0007/spec.md` documents the negative-case checklist.                                          | This document — "Negative-case checklist" table above.                               |

## Relationship to D-0005 (test_eval_id_regex.py)

Intentional overlap with `test_eval_id_regex.py` — the two files serve
different audiences:

- **`test_eval_id_regex.py` (T01.05 / D-0005)** owns the *function
  contract*: positive cases, type guard, error-surface attributes,
  exit-code mapping, regex compilation.
- **`test_path_traversal.py` (T01.08 / D-0007)** owns the *security
  checklist*: one test per NFR-SEC1 attack class, plus the loader
  integration assertion for the post-expansion guard.

If a future change to the regex weakens any single AC bullet, a test in
*this* file will fail first — by design, the security-checklist file is
the one a reviewer reaches for to answer "does the harness still block
the named NFR-SEC1 patterns?".

## Notes / deferred work

- T01.23 (TEST-001) will graft this checklist into the CLI-level
  rejection matrix (exit-code observation through `Click.testing`).
  Until then, this file's `test_invalid_eval_id_exit_code_is_two`
  pins the constant.
- The `home_root` containment guarantee (AC12 / T01.19) is a layered
  defence on top of the regex; the rejection-side FS-write contract
  asserted here (`test_no_fs_write_when_traversal_id_rejected`)
  remains valid regardless of the allowlist outcome.
