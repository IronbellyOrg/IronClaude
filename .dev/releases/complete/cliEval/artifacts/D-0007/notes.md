# D-0007 — implementation notes

**Task:** T01.08 — Author NFR-SEC1 path-traversal prevention test set
**Date:** 2026-05-20

## Design decisions

1. **One test per AC bullet, not bundled `@pytest.mark.parametrize`.**
   The 7 named NFR-SEC1 categories each get a dedicated `def
   test_rejects_*` so the failure name a reviewer sees ("`empty_string`
   regression") maps 1:1 to the AC checklist. Sub-cases inside a
   single category (e.g. multiple leading-digit shapes) are
   parametrize-collapsed because the *category* is the auditable unit.

2. **Integration-level parameterized-unsafe test.** The post-expansion
   guard is the load-bearing FR-SCH2 application. Calling
   `validate_eval_id` on an unsafe expanded string in isolation would
   only test the regex; using `SuiteLoader.load()` with a hostile
   `_expand_entry` patch proves the loader actually invokes the
   re-check after expansion. This is the security guarantee the spec
   relies on.

3. **No regex sanity test here.** That belongs to `test_eval_id_regex.py`
   (T01.05) — `EVAL_ID_REGEX.pattern` is asserted there as a single
   source of truth. Duplicating it here would risk silent drift if a
   future patch updates the regex but the dedicated security checklist
   wasn't re-read.

4. **Defence-in-depth FS-write assertion.** `validate_eval_id` is pure
   and synchronous, but the test
   `test_no_fs_write_when_traversal_id_rejected` snapshots a sandbox
   `tmp_path` before/after a rejection. This pins the **contract** —
   if a future change accidentally adds logging-to-file, telemetry, or
   metric emission, the snapshot diverges and the test fails. The
   security model relies on this; the contract test makes the reliance
   explicit.

5. **Cross-link block at the top of the module docstring.** Avoids
   the "what does TEST-001 mean here?" question for future readers.
   Each cross-link names the task ID and the deliverable in one line.

## Why this file exists separately from `test_eval_id_regex.py`

The two test files have different *audiences*:

- A regression on `test_eval_id_regex.py` says "the function contract
  is broken". That's a developer-surface finding.
- A regression on `test_path_traversal.py` says "the NFR-SEC1
  security model is broken". That's an audit/review-surface finding.

The same regex change *could* trip both, but the security-checklist
naming is what surfaces the right *severity* to a reviewer. The
overlap is intentional defence-in-depth, called out in D-0007/spec.md.

## Sub-agent verification

Tier=STRICT with Risk=High and "security" risk driver. Sub-agent
delegation is *Required* by the task header. Verification path:

- The 7 named AC tests + 2 cross-cutting invariants run green
  (`evidence/T01.08/pytest-targeted.log`).
- The full `tests/cli/eval/` regression remains 139 passed
  (`evidence/T01.08/pytest-regression.log`), so this checklist did
  not break any upstream test.
- The function under test is the same one already exercised by 66
  unit assertions in T01.05; the new file's contribution is the
  *NFR-SEC1 traceability* and the *post-expansion integration*
  assertion, not new coverage of the regex itself.

A sub-agent review pass should confirm:

1. Every NFR-SEC1 rejection case named in the AC has a dedicated test.
2. The parameterize integration test cannot pass without the
   post-expansion `validate_eval_id` call site (proven by the
   `mock_expand.side_effect` invoking `validate_eval_id` directly).
3. No test relies on filesystem state — all writes (if any) happen
   via `tmp_path`.

## Open follow-ups

- T01.23 (TEST-001) will absorb these cases into the CLI-level
  rejection matrix that observes exit codes via `click.testing`. The
  current `test_invalid_eval_id_exit_code_is_two` is a constant-pin
  bridge until then.
- AC12 (T01.19) layers a scratch-root allowlist on top of this guard;
  no change needed here when that lands — the regex rejection runs
  before the allowlist check by design.
