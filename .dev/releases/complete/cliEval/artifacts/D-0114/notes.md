# D-0114 — implementation notes

## Command selection rationale

The four-command sequence is chosen to walk the harness **inside-out**:
read-only unit code → on-disk surface sync → operator-environment
capability → end-to-end subprocess invocation. A failure on any step
localises the regression band without ambiguity. The OPS-004 contract
(as expressed by R-113 / the task's "enumerate" step) is therefore
shape-fixed at four commands; T06.11 does not get to add a fifth on
intuition. If a future regression band needs additional coverage, it
must be added by a deliberate R-113-amendment task and reflected in
both the document and `test_validation_commands.py` in the same commit.

### Why this pytest selection (not the whole eval test directory)

The task description enumerates "targeted pytest" without naming a
specific file set. Two candidate selections were considered:

1. `tests/cli/eval/` (all 76 files) — comprehensive but slow and
   currently surfaces an unrelated Click 8.2 API drift in
   `test_eval_group.py::test_run_skeleton_emits_deferral_notice_on_stderr`
   (`CliRunner(mix_stderr=...)` was removed upstream). That failure is
   not OPS-004 scope and would noise the gate.
2. `test_describe.py` + `test_doctor.py` (73 tests) — exercises the
   two read-only eval-CLI surfaces, runs in <1s, is currently green,
   and is large enough that a real regression in describe-rendering or
   doctor-payload composition would surface. **Chosen.**

The selection is documented in `validation-commands.md` §2.1 and the
audit test pins it verbatim so the choice cannot drift without a
deliberate doc + test update.

### Why command 4 stays in the contract despite the blocker

The OPS-004 contract is the **release-readiness specification**, not a
snapshot of "what passes today." Removing command 4 because B1/B2 are
unclosed would weaken the gate permanently and let the next operator
ship a release without ever running an end-to-end eval. The honest
treatment is:

- Keep command 4 in the contract.
- Capture the failing evidence with full traceback.
- Document B1 + B2 explicitly in §5 with named follow-up tasks.
- Mark the AC §4 row "All 4 commands exit 0" as partial.
- Make the audit test assert that B1 + B2 remain enumerated until they
  close (`test_doc_records_known_blockers_section`).

## B1 — `_new_run_id` / `_default_output_dir` gap

`src/superclaude/cli/eval/commands.py:1467` reads:

```python
run_id = _new_run_id()
requested_output = (
    output_dir if output_dir is not None else _default_output_dir(run_id)
)
```

Neither helper is defined in `commands.py` or imported from a sibling
module. `secrets` and `datetime` are already imported at the top of
the file (`commands.py:34, 39`), and `compose_run_id(started_at,
suite_name)` exists at `src/superclaude/cli/eval/artifact_layout.py:139`.
The minimal closure for B1 is:

```python
def _new_run_id(suite_name: str = "") -> str:
    started_at = datetime.now(timezone.utc).isoformat()
    return compose_run_id(started_at, suite_name=suite_name)


def _default_output_dir(run_id: str) -> Path:
    return Path(".dev") / "eval-runs" / run_id
```

T06.11 does **not** land this fix inline. Rationale:

1. The fix sits inside the T04.10 `eval_run` body, which is its own
   tracked deliverable. Closing it here would muddle ownership.
2. Even with B1 closed, B2 (ptytest vendoring) still blocks a real
   PASS on E1. Landing only B1 would produce a misleading "exit 0
   with SKIPPED outcome" that satisfies the AC's letter but not its
   intent.
3. T06.10 closed a 4-line Makefile target gap inline because the
   scope was self-contained and the AC ("`make verify-deps` exits 0")
   could not be honestly satisfied otherwise. T06.11's gap is larger
   and the AC permits `Fallback Allowed: Yes`.

The closure path is documented in `validation-commands.md` §5 and in
`artifacts/D-0114/spec.md` §"Regeneration / future updates".

## B2 — ptytest vendoring still SOFT-SKIP

The vendored fork lives entirely under `src/superclaude/cli/eval/pty/`
per D-1 (R5 ADR). The directory exists but `__init__.py` is missing,
so the doctor capability check at `commands.py:_check_ptytest_vendored`
returns SOFT-SKIP. Every E1–E15 row in `suites/real.yaml` carries
`no_pty: skip`, which means without the vendor:

- `eval run --no-pty` → entire suite SKIPPED (already documented in
  the real.yaml header comment, lines 1–14).
- `eval run` (default) → would attempt to drive a real Claude Code
  subprocess through a non-existent PTY driver and fail at import.

B2 closure is the M2 ptytest vendoring task, owner per the original
M2 plan.

## On dependency T06.14 (MIG-001)

The T06.11 phase metadata lists T06.14 as a dependency. T06.14 has
not landed on this branch (no `artifacts/D-0116/` exists). The task
metadata also sets `Fallback Allowed: Yes`, which authorises
proceeding without a satisfied dependency. T06.11 honours the
fallback because:

- Command 2 (`make verify-sync`) is the operator-equivalent of the
  AC11 pre-commit gate that T06.14 attests. Today the gate passes
  (`✅ All components in sync.`) even though T06.14's formal
  attestation is not yet recorded, because the four sync scopes
  (`skills | agents | commands | hooks`) are already aligned. The
  underlying invariant — "no direct `.claude/` edits" — is observed
  on this branch.
- Deferring T06.11 until T06.14 lands would leave the entire OPS-004
  contract undefined during the M6 close. That is the higher cost.

## On the audit test design

The test file `tests/cli/eval/test_validation_commands.py` deliberately
does **not** execute the four commands. Three reasons:

1. **Speed.** A four-command smoke (especially command 4 once
   unblocked) would push the test runtime past the second-mark and
   produce flaky CI evidence.
2. **Locality.** The OPS-004 attestation is the four `*.log` files
   under `evidence/T06.11/`, not pytest output. Having the test run
   the commands would produce a second source of truth that could
   drift from the captured evidence.
3. **Operator-driven by design.** The OPS-004 contract is what an
   operator (or CI cron) runs on release day. The test guards the
   document so the operator-facing recipe stays accurate.

What the test **does** guard:
- The document exists at the canonical path.
- All four commands are present verbatim and in canonical order.
- Each command's evidence log is named correctly.
- All required structural sections are present.
- Evidence logs exist on disk and carry the trailing exit-code marker.
- B1 + B2 remain enumerated until closed.

This is the right granularity for a doc-shape gate: it prevents
silent drift between the document, the evidence captures, and the
known-blocker tracking, without overlapping with the runtime
attestation that the evidence logs themselves provide.

## On the "exit code marker" convention

Each evidence log uses the pattern:

```bash
( <command> 2>&1; echo "EXIT_CODE=$?" ) > <log>
```

The trailing `EXIT_CODE=<n>` line is essential because a stream
redirect strips the shell exit code. Without it, a reader of the log
file cannot distinguish "command ran cleanly and finished" from
"command segfaulted halfway." Pinning the convention in the audit
test (`test_evidence_log_present_with_exit_code`) makes the marker
mandatory.
