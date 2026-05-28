---
id: "TASK-STDIN-RECON-REMEDIATION-20260501"
title: "stdin-patch adversarial-recon remediation (18 items)"
description: "Land the 18 remediations from /sc:adversarial recon on fix/claude-process-stdin-large-prompts"
status: "🟡 To Do"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-05-01"
updated_date: "2026-05-01"
assigned_to: "branch-author"
branch: "fix/claude-process-stdin-large-prompts"
base_commit: "2c21279"
source_plan: ".dev/architectural/claude-process-stdin-patch/adversarial-recon/adversarial/refactor-plan.md"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: "1-2 days for branch-author phases (1+2+3+4); spec-keeper handoffs add ~half-day"
task_type: static
related_docs:
  - path: ".dev/architectural/claude-process-stdin-patch/adversarial-recon/merged-output.md"
    description: "Verdict document — coverage scorecard"
  - path: ".dev/architectural/claude-process-stdin-patch/adversarial-recon/adversarial/refactor-plan.md"
    description: "Canonical 18-item remediation plan"
  - path: ".dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md"
    description: "Original spec — source for P-010 amendment + P-014 §3.2 + P-015 §11"
  - path: ".dev/architectural/claude-process-stdin-patch/reconciliation/F-strict-review.md"
    description: "Prior STRICT review (approved-with-nits) — cross-reference for severity calibration"
tags:
  - "subprocess"
  - "stdin-patch"
  - "remediation"
  - "adversarial-recon"
  - "multi-owner"
---

# stdin-patch adversarial-recon remediation (18 items)

## Task Overview

This task lands the 18 remediations produced by the `/sc:adversarial` pipeline on top of branch `fix/claude-process-stdin-large-prompts` at HEAD `2c21279`. The /sc:adversarial pass on the just-shipped stdin-patch delta surfaced 8 NEW findings beyond the prior F-strict-review (1 MEDIUM file-handle leak + 7 LOW), confirmed and re-tiered F's existing findings, and produced a structured remediation plan with named owners.

The work is organized into 6 phases mapping the refactor-plan's MUST/SHOULD/NICE/Tracking/Defer tiers, plus a final verification gate. Items P-006..P-013 + T-012..T-016 + P-014..P-016 are landed in-tree; the 13 D-FOLLOW issues from merged-output §5.3 are filed as GitHub issues in Phase 5 and tracked out-of-band. Multi-owner: 13 items go to `branch-author`, 2 to `spec-keeper` (handled by branch-author in this delta per gap-resolution memo MINOR-7), 1 to `release-engineer` (Makefile target landed by branch-author; executed post-merge by release-engineer).

## Key Objectives

- Address 2 HIGH PRD subclass gaps: P-006 (PrdClaudeProcess.terminate `_stdin_error` surfacing) + P-007 (paired regression test)
- Fix 5 MEDIUM defects: P-009 (env-var helper), P-011 (init `_stdin_error`), P-013 (T-011 mock-injected unconditional), P-012 (`prompt_via=stdin` log token), T-012 (n=0 silent break observability)
- Land 3 NICE polish items: P-008 (parametric subclass test) + P-010 (RECONCILED_DESIGN.md §4 P-004 amendment) + P-012 (overlapping with above)
- Add 4 mutation-kill / coverage-gap tests: T-013 (NUL-byte round-trip), T-014 (finally-close mutation-kill), T-015 (extra_args size invariant), T-016 (tool_write_mode × BrokenPipe cross-product)
- Create 3 tracking artifacts: P-014 (BEAT_2_BACKLOG.md with 15 DEFER + 16 SUPERSEDED), P-015 (TRACEABILITY.md commit→D-NNN map), P-016 (`make ship-coder` target)
- File 13 GH issues for deferred-with-tracking items (D-FOLLOW-001..010 + W-M10/R-5 + T-015/T-016 echoes)
- Restore 1294/1294 baseline + add 6 new pipeline tests; full pytest suite green at Phase 6 gate

## Prerequisites & Dependencies

- Branch `fix/claude-process-stdin-large-prompts` checked out at HEAD `2c21279`
- Pre-existing 1294/1294 pytest baseline is green on master (verified at pre-delta SHA `142ce15`)
- 64 sprint test failures in `tests/sprint/` are pre-existing (out of scope; do NOT fix)
- `verify-sync` drift on rf-* / skill-creator agents in `.claude/` is pre-existing (out of scope; do NOT fix)
- `uv` installed and working (`uv run pytest` succeeds)
- `pipx` installed for wheel reinstall verification
- `gh` CLI authenticated against `IronbellyOrg/IronClaude` for Phase 5 issue creation
- `release-engineer` reachable for D-FOLLOW-001 (post-merge execution; not blocking this PR)
- Working knowledge of `tests/pipeline/test_process_stdin.py` style conventions (see R2 for the canonical patterns: module-level `_stdin_echo_argv()`, inline `tmp_path`, `with patch.object(...)` blocks, no markers)

---

## Phase 1 — MUST (in-PR fixes for real defects)

3 in-PR remediation items + 1 phase-end verification gate. These are the items the refactor-plan classifies as MUST-land before merge: P-006 closes a HIGH PRD subclass contract gap; P-007 pins it with a regression test; P-009 closes the import-time crash on hostile env-var values.

- [ ] **1.1 — P-006 — Surface `_stdin_error` from `PrdClaudeProcess.terminate()`**
  - **Owner**: branch-author
  - **Severity**: HIGH
  - **Refs**: INV-004 (HIGH UNADDRESSED → ADDRESSED-R3) · F MEDIUM-1 · R3-impl §INV-004 · refactor-plan §P-006
  - **Target**: `src/superclaude/cli/prd/process.py` — insert immediately before line 279 (the `_close_handles()` final call site in `terminate()`)
  - **Estimated LOC**: +4 / -0
  - **Context**: PRD's `terminate()` override predates P-004 and silently swallows BrokenPipe under SIGTERM-only paths. The base `pipeline/process.py:288-291` has a 4-line `_stdin_error` log block that PRD must replicate verbatim to honour the contract that `terminate()` surfaces stdin write errors as WARNING-level log lines. **NOTE: refactor-plan cited line 277 — the verified actual `_close_handles()` call is at L279 (R1 drift correction).**
  - **Action**: Read `src/superclaude/cli/prd/process.py` and confirm L274-279 matches:
    ```
    274            except (ProcessLookupError, subprocess.TimeoutExpired):
    275                pass
    276
    277        if self._on_exit is not None:
    278            self._on_exit(self._process.pid, self._process.returncode)
    279        self._close_handles()
    ```
    Then insert the following 4-line block IMMEDIATELY BEFORE line 279 (i.e., between L278 and L279):
    ```python
            if getattr(self, "_stdin_error", None) is not None:
                _log.warning(
                    "stdin_error pid=%s err=%r", self._process.pid, self._stdin_error
                )
    ```
    The block must be byte-identical to the reference at `pipeline/process.py:288-291`.
  - **Output**: Modified `src/superclaude/cli/prd/process.py` with 4 new lines inserted before the `_close_handles()` call. New `_close_handles()` is at L283.
  - **Verification**: Run `grep -n 'stdin_error pid=' src/superclaude/cli/prd/process.py` — must return one match. Run `python -c "import ast; ast.parse(open('src/superclaude/cli/prd/process.py').read())"` — must exit 0 (file parses).
  - **Completion gate**: Block is present and byte-identical to base; file parses; this item marked complete.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **1.2 — P-007 — Pin PRD `terminate` `_stdin_error` surfacing with regression test**
  - **Owner**: branch-author
  - **Severity**: HIGH
  - **Refs**: INV-025 (HIGH UNADDRESSED → ADDRESSED-R3) · R3-impl §INV-025 · refactor-plan §P-007 · paired with P-006
  - **Target**: `tests/pipeline/test_prd_process_stdin.py` (NEW FILE — confirmed not present at HEAD by R2)
  - **Estimated LOC**: +30 / -0
  - **Context**: P-006 inserts a 4-line block in PRD's `terminate()`. P-007 pins that block by writing a regression test that monkeypatches `os.write` to raise `BrokenPipeError`, calls `proc.start(); proc.terminate()`, and asserts `caplog` contains a WARNING containing `"stdin_error"`. Mutation-kill: removing P-006's block must cause this test to fail. The new test file must follow `tests/pipeline/test_process_stdin.py` style (module-level `_stdin_echo_argv()` helper if needed; inline `tmp_path`; `with patch.object(...)` blocks; NO `@pytest.mark.*` decorators).
  - **Action**: Create `tests/pipeline/test_prd_process_stdin.py` with this exact import block (per gap-resolution MINOR-6):
    ```python
    from __future__ import annotations
    import logging
    import os
    import sys
    from unittest.mock import patch
    import pytest
    from superclaude.cli.prd.process import PrdClaudeProcess
    ```
    Then write `test_prd_terminate_surfaces_stdin_error(tmp_path, caplog, monkeypatch)`:
    1. Construct a `PrdClaudeProcess` with prompt and tmp_path-based `output_file`/`error_file`.
    2. Patch `build_command` via `with patch.object(PrdClaudeProcess, "build_command", return_value=<sleep stand-in>):`.
    3. `monkeypatch.setattr(os, "write", <raises BrokenPipeError>)` to inject the failure.
    4. Wrap with `caplog.at_level(logging.WARNING, logger="superclaude.prd.process")`. The PRD module uses an explicit logger string `_log = logging.getLogger("superclaude.prd.process")` at L28 of `prd/process.py` (verified by R1) — pass that exact string. Do NOT substitute `__name__`; the source uses a literal.
    5. Call `proc.start()` then `proc.terminate()`.
    6. Assert `any("stdin_error" in rec.message for rec in caplog.records if rec.levelname == "WARNING")`.
  - **Output**: New file `tests/pipeline/test_prd_process_stdin.py` with one test function that exercises the P-006 block.
  - **Verification**: Run `uv run pytest tests/pipeline/test_prd_process_stdin.py -v` — must pass. Then verify mutation-kill by mentally reverting P-006 (do NOT actually revert) and confirm the test would fail without P-006's WARNING block.
  - **Completion gate**: New test file exists; test passes; mutation-kill is logically guaranteed (test asserts the WARNING that only P-006 emits).
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **1.3 — P-009 — `_resolve_prompt_max_bytes()` helper for env-var hostility**
  - **Owner**: branch-author
  - **Severity**: MEDIUM
  - **Refs**: INV-009 (MEDIUM UNADDRESSED) · INV-011 (NEW vs F, negative cap) · F MEDIUM-2 · R3-impl §9 · refactor-plan §P-009
  - **Target**: `src/superclaude/cli/pipeline/process.py:27-29` (verified exact match by R1)
  - **Estimated LOC**: +12 / -2
  - **Context**: Today the module-level constant `PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024))` crashes at import time on non-numeric inputs (`=16MB`, `=unlimited`, `=-1`). Replace with a helper that catches `ValueError`, logs a WARNING, and falls back to default. Optional clamp on negative values.
  - **Action**: Read `src/superclaude/cli/pipeline/process.py` L24-29 and confirm the current code matches R1's verbatim before-block. Replace L27-29 with:
    ```python
    def _resolve_prompt_max_bytes() -> int:
        raw = os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES")
        default = 16 * 1024 * 1024
        if raw is None:
            return default
        try:
            value = int(raw)
        except ValueError:
            _log.warning("ignoring non-numeric SUPERCLAUDE_PROMPT_MAX_BYTES=%r", raw)
            return default
        if value < 0:
            _log.warning("ignoring negative SUPERCLAUDE_PROMPT_MAX_BYTES=%r", raw)
            return default
        return value

    PROMPT_MAX_BYTES: int = _resolve_prompt_max_bytes()
    ```
    Verify `_log` is already imported / defined at module scope (it is — used elsewhere in the file).
  - **Output**: Modified `src/superclaude/cli/pipeline/process.py` with the helper function and module-level call.
  - **Verification**: Run `SUPERCLAUDE_PROMPT_MAX_BYTES=16MB uv run python -c "from superclaude.cli.pipeline.process import PROMPT_MAX_BYTES; print(PROMPT_MAX_BYTES)"` — must print `16777216` (the default) and emit a WARNING. Same with `=-1` and `=unlimited`. Same with `=2048` must print `2048` (no warning).
  - **Completion gate**: Helper present; module no longer crashes on hostile env values; default fallback verified for at least 3 hostile inputs (`=16MB`, `=unlimited`, `=-1`).
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **1.G — Phase 1 verification gate**
  - **Owner**: branch-author
  - **Severity**: GATE
  - **Refs**: BUILD_REQUEST QA_GATE_REQUIREMENTS=PER_PHASE
  - **Target**: N/A (verification step)
  - **Estimated LOC**: 0
  - **Context**: All 3 Phase 1 remediations must be confirmed in place before advancing to Phase 2. P-007 unit-tests P-006; P-009 is verified by import-time exercise.
  - **Action**: Execute three verifications in sequence:
    1. Run `uv run pytest tests/pipeline/test_prd_process_stdin.py -v` — confirm 1 test passes (P-007).
    2. Run `grep -n 'stdin_error pid=' src/superclaude/cli/prd/process.py` — confirm exactly one match (P-006).
    3. Run `uv run python -c "from superclaude.cli.pipeline.process import PROMPT_MAX_BYTES, _resolve_prompt_max_bytes; print(PROMPT_MAX_BYTES, _resolve_prompt_max_bytes.__name__)"` — confirm helper imports without crashing (P-009).
  - **Output**: Pass/fail outcome for each of the three sub-checks captured in the Phase 1 Findings subsection.
  - **Verification**: All three sub-checks return clean. Any failure halts progression to Phase 2.
  - **Completion gate**: All three verifications PASS. Log results to ### Phase 1 Findings.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

---

## Phase 2 — SHOULD (polish + mutation-kill tests)

7 items: P-011, P-013, T-012, T-013, T-014, T-015, T-016 + 1 phase-end gate. Polish-tier code fixes (init field, log token, mutation-kill conversion) plus 4 new mutation-kill / coverage-gap test additions. Per gap-resolution CRITICAL-1, T-015 and T-016 land in Phase 2 (not Phase 5).

- [ ] **2.1 — P-011 — Initialize `self._stdin_error = None` in `__init__`**
  - **Owner**: branch-author
  - **Severity**: MEDIUM (OVER-CALIBRATED — defensible LOW per /sc:reflect A-FINDING-006)
  - **Refs**: U-007 (R1) · INV-002 (MEDIUM, future-refactor risk) · F LOW-1 · R3-impl §1, §10 · refactor-plan §P-011
  - **Target**: `src/superclaude/cli/pipeline/process.py` `__init__` body — insert after L90 (after `self._stderr_fh = None`)
  - **Estimated LOC**: +1 / -0
  - **Context**: Currently `_stdin_error` is only set inside `start()` (L175). `wait()` (L240) and `terminate()` (L288) both use defensive `getattr(self, "_stdin_error", None)` because the attribute may not exist if `start()` was never called. Adding the init line removes the asymmetry; both call sites can subsequently switch to plain attr access. Calibration note: this MEDIUM is over-calibrated per /sc:reflect; defensible LOW. Lands in this PR regardless.
  - **Action**: Read `src/superclaude/cli/pipeline/process.py` L88-90 and confirm:
    ```
    88        self._process: Optional[subprocess.Popen] = None
    89        self._stdout_fh = None
    90        self._stderr_fh = None
    ```
    Insert one line after L90:
    ```python
            self._stdin_error: Optional[BaseException] = None
    ```
    Then optionally remove the redundant `self._stdin_error: Optional[BaseException] = None` assignment at L175 inside `start()` (the existing one). The `getattr(...)` reads at L240 and L288 may be simplified to plain attribute access, but this is OPTIONAL — keep the `getattr` calls if simpler.
  - **Output**: Modified `__init__` body with one new line; (optional) cleanup of redundant L175 assignment.
  - **Verification**: Run `grep -n '_stdin_error' src/superclaude/cli/pipeline/process.py` — confirm at least one match in the `__init__` region (L88-95). Run `uv run pytest tests/pipeline/test_process_stdin.py -v` — confirm all existing tests still pass.
  - **Completion gate**: Init line present; existing test_process_stdin.py suite still passes.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **2.2 — P-013 — Replace conditional T-011 BrokenPipe assertion with mock-injected unconditional**
  - **Owner**: branch-author
  - **Severity**: MEDIUM
  - **Refs**: X-006 · R3-impl §3 · NIT-1 (F-strict-review) · refactor-plan §P-013
  - **Target**: `tests/pipeline/test_process_stdin.py` — T-011 test at L262-285, specifically the conditional block at L282-285. **NOTE: refactor-plan cited L465-488; the verified actual location is L262-285 (R1 drift correction; ~200-line negative drift).**
  - **Estimated LOC**: +8 / -5
  - **Context**: Currently T-011 (`test_broken_pipe_surfaces_via_stdin_error_log`) uses a race-tolerant `if proc._stdin_error is not None:` guard at L282-285 because the existing approach (early-exit child stand-in) doesn't guarantee BrokenPipe fires on fast machines. Replacement: inject BrokenPipe deterministically via `monkeypatch.setattr(os, "write", _raise_broken_pipe)` so the assertion can be unconditional. Restores mutation-kill: removing P-004's capture block must fail T-011.
  - **Action**: Read `tests/pipeline/test_process_stdin.py` L262-285 (R1 verified body). Replace the test body with:
    ```python
        def test_broken_pipe_surfaces_via_stdin_error_log(self, tmp_path, caplog, monkeypatch):
            """T-011: BrokenPipe injected deterministically via monkeypatch; _stdin_error captured + WARNING log."""
            def _raise_broken_pipe(*args, **kwargs):
                raise BrokenPipeError("injected for T-011 mutation-kill")

            proc = ClaudeProcess(
                prompt="c" * (1024 * 1024),
                output_file=tmp_path / "out.txt",
                error_file=tmp_path / "err.txt",
            )
            monkeypatch.setattr(os, "write", _raise_broken_pipe)
            with caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process"):
                with patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv()):
                    proc.start()
                    rc = proc.wait()
            # Unconditional assertions (no race tolerance):
            assert proc._stdin_error is not None
            assert isinstance(proc._stdin_error, BrokenPipeError)
            warnings = [r for r in caplog.records if "stdin_error" in r.message]
            assert warnings, "BrokenPipe must surface as a WARNING log"
    ```
    Add `import os` to the file's import section if not already present.
  - **Output**: Modified `tests/pipeline/test_process_stdin.py` with deterministic BrokenPipe injection.
  - **Verification**: Run `uv run pytest tests/pipeline/test_process_stdin.py::TestChunkedStdinWrite::test_broken_pipe_surfaces_via_stdin_error_log -v` — must pass. Confirm conditional `if proc._stdin_error is not None:` no longer present via `grep -c 'if proc._stdin_error is not None' tests/pipeline/test_process_stdin.py` returning 0.
  - **Completion gate**: Test passes with unconditional assertion; conditional guard removed; `os` import added.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **2.3 — T-012 — `n == 0` silent break observability**
  - **Owner**: branch-author
  - **Severity**: MEDIUM (OVER-CALIBRATED — defensible LOW per /sc:reflect A-FINDING-007)
  - **Refs**: INV-014 (MEDIUM, elevated from F LOW-2) · R3-impl §11 · refactor-plan §T-012
  - **Target**: `src/superclaude/cli/pipeline/process.py:216-218` (verified exact match by R1)
  - **Estimated LOC**: +2 / -0 (logical change is +2; physical insertion is +3 lines counting f-string body)
  - **Context**: At L216-218 the chunked write loop breaks silently on `n <= 0` with no `_stdin_error` set, leaving silent-truncation invisible to operators. Insert a capture line that sets `self._stdin_error = OSError(...)` with a diagnostic offset before the break. Calibration note: MEDIUM is over-calibrated per /sc:reflect (F LOW-2 is defensible). Lands in this PR regardless.
  - **Action**: Read `src/superclaude/cli/pipeline/process.py` L213-219 and confirm:
    ```
    213                    except InterruptedError:
    214                        # EINTR from signal delivery -- retry the same chunk.
    215                        continue
    216                if n <= 0:
    217                    # Defensive -- os.write should not return 0 on a pipe.
    218                    break
    219                offset += n
    ```
    Replace L216-218 with:
    ```python
                    if n <= 0:
                        # Defensive -- os.write should not return 0 on a pipe.
                        self._stdin_error = OSError(
                            f"unexpected zero-byte write at offset {offset}/{len(view)}"
                        )
                        break
    ```
  - **Output**: Modified `src/superclaude/cli/pipeline/process.py` with `_stdin_error` capture before the silent break.
  - **Verification**: Run `grep -n 'unexpected zero-byte write' src/superclaude/cli/pipeline/process.py` — confirm one match. Run `uv run pytest tests/pipeline/test_process_stdin.py -v` — confirm no regression.
  - **Completion gate**: Capture present; test suite still green.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **2.4 — T-013 — NUL-byte prompt round-trip test**
  - **Owner**: branch-author
  - **Severity**: MEDIUM (severity elevated from LOW for mutation-kill purposes)
  - **Refs**: INV-019 (NEW vs F, LOW elevated for mutation-kill) · R2-impl W-L9 · R3-impl §12 · refactor-plan §T-013
  - **Target**: `tests/pipeline/test_process_stdin.py` — append new test to existing `TestChunkedStdinWrite` class. Reference test: T-002 (line 178-191).
  - **Estimated LOC**: +20 / -0
  - **Context**: Pin binary-safety invariant against future string-conversion regressions. Send `b"\x00" * 1024` through stdin and assert byte-for-byte echo.
  - **Action**: Append a new test to `TestChunkedStdinWrite` class:
    ```python
        def test_nul_byte_prompt_round_trip(self, tmp_path):
            """T-013: NUL-byte payload round-trips byte-identical via stdin (binary-safety pin)."""
            payload = b"\x00" * 1024
            out_file = tmp_path / "out.txt"
            err_file = tmp_path / "err.txt"
            proc = ClaudeProcess(
                prompt=payload.decode("latin-1"),  # round-trip through str→bytes preserves NULs
                output_file=out_file,
                error_file=err_file,
            )
            with patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv()):
                proc.start()
                rc = proc.wait()
            assert rc == 0
            assert out_file.read_bytes() == payload, "NUL-byte payload must round-trip byte-identical"
    ```
  - **Output**: New test in `TestChunkedStdinWrite` class.
  - **Verification**: Run `uv run pytest tests/pipeline/test_process_stdin.py::TestChunkedStdinWrite::test_nul_byte_prompt_round_trip -v` — must pass.
  - **Completion gate**: Test passes; all 1024 NUL bytes preserved through stdin pipeline.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **2.5 — T-014 — `finally`-close mutation-kill test**
  - **Owner**: branch-author
  - **Severity**: MEDIUM
  - **Refs**: F-strict-review §6 mutation-kill gap · R2-impl W-L10 · R3-impl §13 · refactor-plan §T-014
  - **Target**: `tests/pipeline/test_process_stdin.py` — append new test (likely to `TestChunkedStdinWrite`)
  - **Estimated LOC**: +25 / -0
  - **Context**: Pins the `finally: stdin.close()` invariant against future refactors that might move close() out of the finally block. Inject `OSError` mid-write via `monkeypatch.setattr(os, "write", ...)`, then assert `proc._process.stdin.closed` is True post-call. Pairs with P-013 (X-006).
  - **Action**: Append a new test to `TestChunkedStdinWrite`:
    ```python
        def test_stdin_closed_in_finally_on_oserror(self, tmp_path, monkeypatch):
            """T-014: OSError mid-write does not prevent stdin.close() in finally."""
            def _raise_oserror(*args, **kwargs):
                raise OSError("injected mid-write OSError for T-014")

            proc = ClaudeProcess(
                prompt="x" * (1024 * 1024),
                output_file=tmp_path / "out.txt",
                error_file=tmp_path / "err.txt",
            )
            monkeypatch.setattr(os, "write", _raise_oserror)
            with patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv()):
                proc.start()
                # start() must not raise; OSError captured into _stdin_error
                _ = proc.wait()
            assert proc._stdin_error is not None
            assert isinstance(proc._stdin_error, OSError)
            # Critical invariant: stdin handle was closed in finally even though write raised
            assert proc._process.stdin is None or proc._process.stdin.closed, \
                "stdin must be closed via finally even when os.write raises OSError"
    ```
  - **Output**: New test asserting the finally-close invariant.
  - **Verification**: Run `uv run pytest tests/pipeline/test_process_stdin.py::TestChunkedStdinWrite::test_stdin_closed_in_finally_on_oserror -v` — must pass.
  - **Completion gate**: Test passes; mutation-kill confirmed by inspection.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **2.6 — T-015 — Parametric `extra_args` size invariant**
  - **Owner**: branch-author
  - **Severity**: LOW (refactor-plan); landed in-PR per gap-resolution CRITICAL-1
  - **Refs**: INV-015 (NEW vs F, LOW) · refactor-plan §T-015 · gap-resolution CRITICAL-1
  - **Target**: `tests/pipeline/test_process_stdin.py` — append new test (likely to `TestArgvByteSizeInvariant` class at L366-393)
  - **Estimated LOC**: +12 / -0
  - **Context**: Existing `T-001` (`test_argv_total_byte_size_bounded_for_huge_prompt`) checks individual argv element size when constructed from huge prompts, but does NOT exercise the `extra_args` live-caller path. T-015 fills that gap.
  - **Action**: Append a new test to `TestArgvByteSizeInvariant`:
    ```python
        def test_extra_args_size_invariant_caught(self, tmp_path):
            """T-015: extra_args element exceeding 4 KiB is detectable by argv-byte-size invariant."""
            huge_extra_arg = "z" * (5 * 1024)  # 5 KB single arg
            proc = ClaudeProcess(
                prompt="small",
                output_file=tmp_path / "out.txt",
                error_file=tmp_path / "err.txt",
                extra_args=[huge_extra_arg],
            )
            cmd = proc.build_command()
            max_arg_bytes = max(len(arg.encode("utf-8")) for arg in cmd)
            # Invariant assertion: 5 KB extra_arg propagates into argv and is detectable
            # by the same byte-size invariant T-001 protects.
            assert max_arg_bytes >= 5 * 1024, \
                "5 KB extra_arg must show in argv (invariant detects oversized extra_args path)"
    ```
    NOTE: if production code instead RAISES on oversized extra_args, switch to `pytest.raises(...)`. Verify production behaviour by reading `build_command()` before finalising.
  - **Output**: New test in `TestArgvByteSizeInvariant` class.
  - **Verification**: Run `uv run pytest tests/pipeline/test_process_stdin.py::TestArgvByteSizeInvariant::test_extra_args_size_invariant_caught -v` — must pass.
  - **Completion gate**: Test exercises 5 KB extra_args path and asserts the byte-size invariant; new test runs green.
  - If unable to complete due to missing context, file-access errors, or unclear instructions (e.g., production behaviour differs from R3's description), log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **2.7 — T-016 — `tool_write_mode × BrokenPipe` cross-product test**
  - **Owner**: branch-author
  - **Severity**: LOW (mechanically straightforward — INV-023 downgrade); landed in-PR per gap-resolution CRITICAL-1
  - **Refs**: INV-023 (NEW vs F, MEDIUM downgraded to LOW) · refactor-plan §T-016 · gap-resolution CRITICAL-1
  - **Target**: `tests/pipeline/test_process_stdin.py` — append new test to `TestToolWriteMode` class (L293-358)
  - **Estimated LOC**: +20 / -0
  - **Context**: Combines T-007 (`tool_write_mode=True`) and T-011 (BrokenPipe via monkeypatch) to exercise the cross-product. Asserts the sidecar `.log` file handle is properly cleaned up under BrokenPipe injection.
  - **Action**: Append a new test to `TestToolWriteMode`:
    ```python
        def test_tool_write_mode_cleans_sidecar_on_broken_pipe(self, tmp_path, monkeypatch):
            """T-016: tool_write_mode=True + BrokenPipe — sidecar fh still cleaned up via finally."""
            def _raise_broken_pipe(*args, **kwargs):
                raise BrokenPipeError("injected for T-016 cross-product")

            out_file = tmp_path / "out.md"
            proc = ClaudeProcess(
                prompt="y" * (1024 * 1024),
                output_file=out_file,
                error_file=tmp_path / "err.txt",
                tool_write_mode=True,
            )
            monkeypatch.setattr(os, "write", _raise_broken_pipe)
            with patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv()):
                proc.start()
                _ = proc.wait()
            # _stdin_error captured (BrokenPipe surfaced from cross-product path)
            assert proc._stdin_error is not None
            assert isinstance(proc._stdin_error, BrokenPipeError)
            # Sidecar handle invariant: tool_write_mode sidecar fh must not be left open
            assert proc._stdout_fh is None or proc._stdout_fh.closed, \
                "tool_write_mode sidecar fh must be closed even when stdin write raises BrokenPipe"
    ```
  - **Output**: New cross-product test in `TestToolWriteMode` class.
  - **Verification**: Run `uv run pytest tests/pipeline/test_process_stdin.py::TestToolWriteMode::test_tool_write_mode_cleans_sidecar_on_broken_pipe -v` — must pass.
  - **Completion gate**: Cross-product test passes; sidecar fh cleanup confirmed under BrokenPipe.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **2.G — Phase 2 verification gate**
  - **Owner**: branch-author
  - **Severity**: GATE
  - **Refs**: BUILD_REQUEST QA_GATE_REQUIREMENTS=PER_PHASE
  - **Target**: N/A (verification step)
  - **Estimated LOC**: 0
  - **Context**: All 7 Phase 2 items must be confirmed before advancing to Phase 3. Pre-task baseline = 13 tests in test_process_stdin.py; post-Phase-2 expected count = 17 (13 existing + 4 net new from T-013/T-014/T-015/T-016; P-013 is in-place so no count delta).
  - **Action**: Run `uv run pytest tests/pipeline/test_process_stdin.py -v` and capture the test count + outcome. Then run targeted greps:
    1. `grep -n 'self._stdin_error: Optional' src/superclaude/cli/pipeline/process.py` — confirm at least one match in `__init__` (P-011).
    2. `grep -c 'if proc._stdin_error is not None' tests/pipeline/test_process_stdin.py` — confirm 0 (P-013 conditional removed).
    3. `grep -n 'unexpected zero-byte write' src/superclaude/cli/pipeline/process.py` — confirm one match (T-012).
  - **Output**: All checks pass; test count delta logged; full pytest output captured to ### Phase 2 Findings.
  - **Verification**: All tests pass; count >= 17; all 3 grep checks return expected.
  - **Completion gate**: Phase 2 results captured; gate passes; ready to advance.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

---

## Phase 3 — NICE (parametric subclass test + spec amendment)

3 items: P-008 (parametric subclass test), P-010 (spec amendment), P-012 (log token) + 1 phase-end gate. Per gap-resolution MINOR-7, `spec-keeper`-tagged items (P-008, P-010) are handled by the branch author in this delta — there is no separate handoff.

- [ ] **3.1 — P-008 — Parametric subclass-propagation test for `_stdin_error` surfacing**
  - **Owner**: spec-keeper (branch author handles in this delta)
  - **Severity**: HIGH (per refactor-plan; phase-mapped to NICE per BUILD_REQUEST)
  - **Refs**: R3-spec §INV-025 (subclass-test scope) · §6 R3-spec dispute #4 · refactor-plan §P-008
  - **Target**: `tests/pipeline/test_subclass_terminate_invariant.py` (NEW FILE — confirmed not present at HEAD by R2)
  - **Estimated LOC**: +35 / -0
  - **Context**: Closes the contract-level gap that P-006 + P-007 only point-fix. The parametric test walks `ClaudeProcess.__subclasses__()` at collection time and asserts every subclass override of `terminate()` either calls `super().terminate()` or contains the `_stdin_error` log block. Future subclasses are auto-covered. Reference style: T-005 + `TestPortifyProcessInheritance` (cli_portify file line 27).
  - **Action**: Create `tests/pipeline/test_subclass_terminate_invariant.py` with this content:
    ```python
    from __future__ import annotations
    import inspect
    import textwrap
    import pytest
    from superclaude.cli.pipeline.process import ClaudeProcess
    # Ensure subclasses are imported so __subclasses__() is populated
    from superclaude.cli.cli_portify.process import PortifyProcess  # noqa: F401
    from superclaude.cli.prd.process import PrdClaudeProcess  # noqa: F401


    def _terminate_overrides_supercall_or_log(cls):
        """Inspect cls.terminate source: must contain super().terminate() OR _stdin_error log."""
        terminate = cls.__dict__.get("terminate")
        if terminate is None:
            return True  # inherits from base — vacuously satisfies
        try:
            src = textwrap.dedent(inspect.getsource(terminate))
        except (OSError, TypeError):
            return False
        if "super().terminate(" in src:
            return True
        # Allow either explicit getattr-based defensive read or plain attr access
        if "_stdin_error" in src and "_log.warning" in src:
            return True
        return False


    @pytest.mark.parametrize("cls", ClaudeProcess.__subclasses__())
    def test_subclass_terminate_surfaces_stdin_error(cls):
        """P-008: every ClaudeProcess subclass with a terminate() override must surface _stdin_error."""
        assert _terminate_overrides_supercall_or_log(cls), (
            f"{cls.__name__}.terminate() must call super().terminate() or "
            f"replicate the _stdin_error log block; see RECONCILED_DESIGN.md §4 P-004."
        )
    ```
    Note: this is source-inspection rather than runtime exercise — it pins the contract that any subclass terminate() override either delegates or replicates. A runtime per-subclass test would require ctor-args fixtures per subclass, which P-008 deliberately avoids per refactor-plan risk note.
  - **Output**: New file `tests/pipeline/test_subclass_terminate_invariant.py` with parametric test that auto-covers future subclasses.
  - **Verification**: Run `uv run pytest tests/pipeline/test_subclass_terminate_invariant.py -v` — must pass for all known subclasses (PortifyProcess + PrdClaudeProcess after P-006).
  - **Completion gate**: New test file exists; parametric expansion covers ≥2 subclasses (PortifyProcess + PrdClaudeProcess); test passes. If parametric collection breaks (subclass requires unusual ctor args during collection), fall back to explicit subclass list per refactor-plan rollback.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **3.2 — P-010 — Spec amendment: subclass-propagation invariant in §4 P-004**
  - **Owner**: spec-keeper (branch author handles in this delta)
  - **Severity**: MEDIUM
  - **Refs**: R3-spec §INV-004 spec-fault concession · §6 R3-spec dispute #5 · refactor-plan §P-010
  - **Target**: `.dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md` §4 P-004 Acceptance sub-block — append one bullet at end of Acceptance list (after the existing `stdin.close() runs in the finally...` line, before the `---` separator at L416)
  - **Estimated LOC**: +1 (one new bullet in markdown)
  - **Context**: Per R4 §2, the current Acceptance block is at L409-414 with 5 bullets. P-010 appends a 6th bullet recording the subclass-propagation invariant and pinning it to the new test file from P-008. Doc-only edit; no code impact.
  - **Action**: Read `.dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md` L409-414 and confirm:
    ```markdown
    **Acceptance**:
    - A 400 KB ASCII prompt round-trips byte-identical via stdin (extends current 200 KB test).
    - A 200 KB UTF-8 emoji prompt round-trips byte-identical.
    - `BrokenPipeError` (child exits early) populates `self._stdin_error` and emits a `WARNING` log line, but does not raise from `start()`.
    - A SIGTERM delivered to the parent during the write loop does not hang `start()` indefinitely (the chunk loop exits after the current chunk because the child closes its end).
    - `stdin.close()` runs in the `finally`, even if `os.write` raises an unexpected `OSError`.
    ```
    Insert after the last bullet (before the `---` at L416):
    ```markdown
    - Subclasses overriding `terminate()` MUST either call `super().terminate()` or replicate the `_stdin_error` log block verbatim. Pinned by `tests/pipeline/test_subclass_terminate_invariant.py`.
    ```
    Preserve trailing horizontal-rule separator.
  - **Output**: Modified RECONCILED_DESIGN.md with 6th Acceptance bullet.
  - **Verification**: Run `grep -n 'Subclasses overriding' .dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md` — confirm one match. Confirm the `---` separator immediately follows.
  - **Completion gate**: New bullet present; cross-references P-008's pinning test file by exact path.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **3.3 — P-012 — Add `prompt_via=stdin` literal to spawn debug log**
  - **Owner**: branch-author
  - **Severity**: MEDIUM (OVER-CALIBRATED — defensible LOW per /sc:reflect A-FINDING-004)
  - **Refs**: X-004 · R3-impl §2 · refactor-plan §P-012
  - **Target**: `src/superclaude/cli/pipeline/process.py:182` (verified exact match by R1; L181-186 region)
  - **Estimated LOC**: +1 / -1 (single format-string line edit)
  - **Context**: Restores telemetry contract D-099. Operators grepping `prompt_via=stdin` against debug logs currently get zero matches; the literal token must be added to the spawn debug format string. Calibration note: MEDIUM is over-calibrated per /sc:reflect; defensible LOW. Lands in this PR regardless.
  - **Action**: Read `src/superclaude/cli/pipeline/process.py` L181-186 and confirm:
    ```
    181        _log.debug(
    182            "spawn pid=%d cmd=%s prompt_bytes=%d",
    183            self._process.pid,
    184            str(self.build_command()[:3]),
    185            len(self._prompt_bytes),
    186        )
    ```
    Replace L182's format string from `"spawn pid=%d cmd=%s prompt_bytes=%d"` to `"spawn pid=%d cmd=%s prompt_via=stdin prompt_bytes=%d"`. The `%d/%s` arg list at L183-185 stays unchanged (the new `prompt_via=stdin` is a literal — no new args).
  - **Output**: Modified format string at L182 includes literal `prompt_via=stdin`.
  - **Verification**: Run `grep -n 'prompt_via=stdin' src/superclaude/cli/pipeline/process.py` — confirm at least one match. Run `uv run pytest tests/pipeline/test_process_stdin.py -v` — confirm no regression.
  - **Completion gate**: Literal token present; format string still has matching `%d/%s` count vs args (3 substitutions: `%d` for pid, `%s` for cmd, `%d` for prompt_bytes).
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **3.G — Phase 3 verification gate**
  - **Owner**: branch-author
  - **Severity**: GATE
  - **Refs**: BUILD_REQUEST QA_GATE_REQUIREMENTS=PER_PHASE
  - **Target**: N/A (verification step)
  - **Estimated LOC**: 0
  - **Context**: Phase 3 is the final NICE/spec-amendment phase before tracking artifacts and final verification. Confirm all three items landed cleanly.
  - **Action**: Execute three sub-checks:
    1. Run `uv run pytest tests/pipeline/test_subclass_terminate_invariant.py -v` — confirm parametric test passes for known subclasses (P-008).
    2. Run `grep -n 'Subclasses overriding' .dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md` — confirm exactly one match (P-010).
    3. Run `grep -c 'prompt_via=stdin' src/superclaude/cli/pipeline/process.py` — confirm exactly one match (P-012).
  - **Output**: All three checks pass; results captured in ### Phase 3 Findings.
  - **Verification**: All three sub-checks return clean.
  - **Completion gate**: Phase 3 verifications PASS; ready to advance to Phase 4 tracking artifacts.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

---

## Phase 4 — Tracking artifacts (separate ownership)

3 items: P-014 (BEAT_2_BACKLOG.md), P-015 (TRACEABILITY.md), P-016 (Makefile target) + 1 phase-end gate. Each item is a documentation-or-build artefact whose body content is paste-ready from R4.

- [ ] **4.1 — P-014 — Create `BEAT_2_BACKLOG.md` tracking artefact**
  - **Owner**: branch-author
  - **Severity**: MEDIUM
  - **Refs**: U-024 (HIGH) · R3-impl §5 · R3-spec §"Sufficiency of Deferral Plan" · refactor-plan §P-014
  - **Target**: `.dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md` (NEW FILE)
  - **Estimated LOC**: +60 (the markdown body below)
  - **Context**: Per R4 §1, RECONCILED_DESIGN.md §3.2 contains 3 buckets (DROP=15, SUPERSEDED=16 distinct IDs, DEFER-TO-BEAT-2=15). The merged-output banner of "12 SUPERSEDED" undercounts; the actual ID list is 16. P-014 creates a tracking artefact with both DEFER-TO-BEAT-2 (§1) and SUPERSEDED (§2) tables.
  - **Action**: Create the file `.dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md` with this exact body (paste-ready from R4 §"Builder-Usable Content for P-014"):
    ```markdown
    # Beat-2 Backlog — Deferred and Superseded Ledger

    **Source**: `RECONCILED_DESIGN.md §3.2`
    **Beat-1 HEAD at deferral**: `2c21279`
    **Created by**: P-014 (TASK-STDIN-RECON-REMEDIATION-20260501)
    **Status**: Open until Beat-2 sprint planned

    ---

    ## §1. DEFER-TO-BEAT-2 (15 items)

    These items were intentionally deferred from Beat-1 (the stdin-patch delta) to a future Beat-2 sprint. Each will be filed as an individual GH issue when Beat-2 is scheduled.

    ### Sidecar feature (7 items)

    - **D-016, D-022, D-035, D-064, D-065, D-072, D-073** — sidecar feature: `prompt_sidecar` kwarg, `.prompt` file, caller policy, opt-in tests, off-by-default test, disk-bloat note. Sidecar is observability-only and adds disk-bloat surface; commit `4799719` already gives the security improvement of hiding prompts from `ps` for free. Land sidecar in Beat-2 once the cap-and-error-surfacing baseline is stable.

    ### Coder-repo deployment (3 items)

    - **D-077, D-085, D-087** — vendored monkey-patch in consumer repo (`/config/workspace/Coder` deployment). Separate operational deliverable downstream of the IronClaude release.

    ### Beat-2 architectural items (4 items)

    - **D-093, D-095, D-096, D-097** — `pre_prompt_args`, `--input-format=stream-json`, sidecar rotation, `PromptSource` Protocol.

    ### Per-caller override (1 item)

    - **D-098** — `force_prompt_via` per-caller override; superseded under always-stdin but retained here in case the design reverses.

    ---

    ## §2. SUPERSEDED ledger (16 D-NNN items, recorded for audit)

    These items were obsoleted by the always-stdin migration in commit `4799719` (2026-04-20). They are recorded here per merged-output §5.4 ("Optionally appended to `BEAT_2_BACKLOG.md` per P-014 R3 concession").

    - **D-002, D-004** — AC-2/AC-4 byte-identical-argv contract (pre-patch shape obsolete since `4799719`).
    - **D-017, D-018, D-019, D-023, D-024, D-028, D-042, D-109** — threshold + `_use_stdin_for_prompt` + `_prompt_anchor_flag(--output-format)` no longer applicable (always-stdin chosen).
    - **D-050, D-053, D-054, D-055, D-057** — threshold-boundary tests N/A; "empty → argv with `-p ''`" inverted by always-stdin.
    - **D-075** — threshold-tweak rollback mechanism N/A; rollback is now `git revert 4799719`.

    Audit trail also lives in:
    - `git log -- src/superclaude/cli/pipeline/process.py` (history of each line).
    - `RECONCILED_DESIGN.md §3.2` (the named ledger).
    ```
  - **Output**: New file `.dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md`.
  - **Verification**: Run `test -f .dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md` (exit 0). Run `grep -c 'D-' .dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md` — expected count of D-NNN tokens is at least 30 (15 DEFER + 16 SUPERSEDED IDs, some on grouped lines). Run `grep -c '^## §' .dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md` — confirm 2 (the §1 and §2 headers).
  - **Completion gate**: File exists; both DEFER and SUPERSEDED sections present.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **4.2 — P-015 — Create `TRACEABILITY.md` commit→D-NNN map**
  - **Owner**: branch-author
  - **Severity**: MEDIUM
  - **Refs**: S-008 · U-035 · R3-impl §4 · R3-spec Concession #8 · refactor-plan §P-015
  - **Target**: `.dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` (NEW FILE)
  - **Estimated LOC**: +40
  - **Context**: Closes S-008 (loss of D-NNN linkage in commit messages) by providing an out-of-band traceability artefact. Body content is the canonical mapping derived from RECONCILED_DESIGN.md §11 + `git log --oneline 142ce15..HEAD`. R4 §3 captured the full reconciled tables.
  - **Action**: Create the file `.dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` with this exact body (paste-ready from R4 §"Builder-Usable Content for P-015"):
    ```markdown
    # Traceability Matrix — stdin-patch Delta (Beat-1)

    **Branch**: `fix/claude-process-stdin-large-prompts`
    **Pre-delta baseline**: `142ce15`
    **Beat-1 HEAD**: `2c21279`
    **Created by**: P-015 (TASK-STDIN-RECON-REMEDIATION-20260501)
    **Source**: `RECONCILED_DESIGN.md §11` + `git log --oneline 142ce15..HEAD`

    ---

    ## §1. Patch ↔ D-NNN ↔ Provenance ↔ AC/Risk

    | Patch | D-NNN | Adversarial provenance | AC / Risk reference |
    |-------|-------|-------------------------|-----------------------|
    | P-001 | D-012, D-046, D-047, D-048 | C-003 (A 65%), X-002 (A 60%), U-002 (A only, 70%) | DESIGN.md AC-4 (adapted), Risk #2 |
    | P-002 | D-014, D-020, D-021 | U-001 (A only, 95%), U-003 (B only, 90%, Change #1) | DESIGN.md AC-7, Risk #4 |
    | P-003 | D-007, D-036 | U-001 (A) + U-003 (B) — pre-spawn cap | DESIGN.md AC-7, Risk #4 |
    | P-004 | D-013, D-025, D-026, D-032, D-034, D-040, D-107, D-108 | C-007 (B 75%, Change #3), C-004 (A 85%), INV-002 (HIGH ADDRESSED) | DESIGN.md AC-1, AC-5, AC-6, Risk #3 (reframed), Risk #5 (partial) |
    | P-005 | (orthogonal — `tool_write_mode` regression net) | DESIGN-NEW (Surprise from `B-code-state.md` Surprise #4) | DESIGN.md AC-10 |

    ## §2. Test ↔ D-NNN ↔ Provenance ↔ AC/Risk

    | Test | D-NNN | Adversarial provenance | AC / Risk reference |
    |------|-------|-------------------------|-----------------------|
    | T-001 | D-052 | X-001 (A) | DESIGN.md AC-3 |
    | T-002 | D-001, D-056 (extended) | C-007 (B), C-001 (A) | DESIGN.md AC-1 |
    | T-003 | D-006, D-058 | Change #4 (B§8.2) | DESIGN.md AC-6 |
    | T-004 | D-007, D-059 | U-001 (A) + U-003 (B) | DESIGN.md AC-7 |
    | T-005 | D-005, D-060 (reframed) | INV-002 | DESIGN.md AC-5, Risk #3 |
    | T-006 | D-027 (reframed for always-stdin) | X-003 (B 75%, Change #5) | operational documentation |
    | T-007 | (orthogonal — `tool_write_mode` regression net) | DESIGN-NEW | DESIGN.md AC-10 |
    | T-008 | D-049, D-063 | DESIGN-NEW (test contract for U-002) | DESIGN.md AC-4 (adapted) |
    | T-009 | D-062 | C-003, X-002 | DESIGN.md AC-4, Risk #2 |
    | T-010 | new from P-001 | DESIGN-NEW (regression net) | DESIGN.md Risk #2 |
    | T-011 | D-034 | A§3.3 — error surfacing | DESIGN.md Risk #5 (partial) |

    ## §3. Commit ↔ Patch ↔ Files Touched

    | SHA | Subject | Patch ID | Files Touched |
    |---|---|---|---|
    | `526a606` | `fix(cli_portify): anchor --add-dir on --output-format instead of dead -p lookup` | P-001 | `src/superclaude/cli/cli_portify/process.py`, `tests/pipeline/test_process_stdin.py` |
    | `c42139b` | `feat(pipeline): add PROMPT_MAX_BYTES and PromptTooLargeForArgv exception` | P-002 | `src/superclaude/cli/pipeline/process.py` |
    | `be46520` | `feat(pipeline): pre-spawn size guard + capture encoded prompt for reuse` | P-003 | `src/superclaude/cli/pipeline/process.py`, `tests/pipeline/test_process_stdin.py` |
    | `5a8e5e7` | `fix(pipeline): chunked stdin write with EINTR retry, error capture, finally-close` | P-004 | `src/superclaude/cli/pipeline/process.py`, `tests/pipeline/test_process_stdin.py` |
    | `01cf2ef` | `test(pipeline): pin tool_write_mode contract` | P-005 / T-007 | `tests/pipeline/test_process_stdin.py` |
    | `dda68d9` | `test(pipeline): argv byte-size invariant for huge prompts` | T-001 | `tests/pipeline/test_process_stdin.py` |
    | `fde1431` | `docs: mark DESIGN.md as historical; RECONCILED_DESIGN.md is the actionable plan` | (doc-only) | `.dev/architectural/claude-process-stdin-patch/DESIGN.md` |
    | `db8cffe` | `docs: STRICT-tier verification review of stdin-patch delta` | (doc-only) | `.dev/architectural/claude-process-stdin-patch/reconciliation/F-strict-review.md` |
    | `2c21279` | `docs: /sc:adversarial coverage analysis of stdin-patch delta` | (doc-only) | 16 files under `.dev/architectural/claude-process-stdin-patch/adversarial-recon/` |

    ## §4. Beat-2 Remediation Patches

    (Add rows here as remediation P-006 through P-018 are landed by TASK-STDIN-RECON-REMEDIATION-20260501.)
    ```
  - **Output**: New file `.dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` containing 5-patch table + 11-test table + 9-commit map + Beat-2 remediation placeholder.
  - **Verification**: Run `test -f .dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` (exit 0). Run `grep -c '^## §' .dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` — confirm 4 (§1 patches, §2 tests, §3 commits, §4 placeholder). Run `grep -c '| P-' .dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` — confirm at least 5 (one per patch row in §1).
  - **Completion gate**: File exists; all 4 sections present; commit table contains all 9 SHAs.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **4.3 — P-016 — Add `make ship-coder` Makefile target**
  - **Owner**: release-engineer (branch-author lands; release-engineer executes post-merge)
  - **Severity**: LOW
  - **Refs**: U-031 · R3-impl §6 (compromise) · R3-spec §"Sufficiency of Deferral Plan" · refactor-plan §P-016
  - **Target**: `Makefile` (append target at end of file)
  - **Estimated LOC**: +10
  - **Context**: Closes the IronClaude-side half of §9.2 — release-engineer runs `make ship-coder` post-merge to close U-031 (the 338 KB Coder roadmap repro). The target builds the wheel, force-installs via pipx, and prints instructions for re-running the failing roadmap.
  - **Action**: Read `Makefile` at the repo root and identify the last existing target. Append the following at the end:
    ```makefile

    .PHONY: ship-coder
    ship-coder:
    	uv build
    	pipx install --force /config/workspace/IronClaude/dist/superclaude-*.whl
    	@echo ""
    	@echo "ship-coder: wheel rebuilt and pipx-installed."
    	@echo "Re-run failing 338 KB roadmap via:"
    	@echo "  cd /config/workspace/Coder && superclaude roadmap run <338KB-spec.md>"
    	@echo ""
    ```
    Note: use TAB-indentation for recipe lines (not spaces) — Makefile syntax is strict. The `.PHONY:` line preserves the convention used by other targets in the existing Makefile.
  - **Output**: Modified `Makefile` with new `ship-coder:` target at the end.
  - **Verification**: Run `grep -n '^ship-coder:' Makefile` — confirm exactly one match. Run `make -n ship-coder` (dry-run) — confirm it shows the `uv build` and `pipx install` commands without errors. Do NOT run the target itself; release-engineer executes it post-merge.
  - **Completion gate**: Target present; dry-run succeeds; release-engineer informed via PR description that target is ready for post-merge use.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **4.G — Phase 4 verification gate**
  - **Owner**: branch-author
  - **Severity**: GATE
  - **Refs**: BUILD_REQUEST QA_GATE_REQUIREMENTS=PER_PHASE
  - **Target**: N/A (verification step)
  - **Estimated LOC**: 0
  - **Context**: Verify that all 3 tracking artefacts are present and well-formed before advancing to Phase 5 issue-filing.
  - **Action**: Execute three sub-checks:
    1. Confirm `BEAT_2_BACKLOG.md` exists with both DEFER and SUPERSEDED tables: `test -f .dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md && grep -c '^## §' .dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md` — confirm 2.
    2. Confirm `TRACEABILITY.md` exists with full commit map: `test -f .dev/architectural/claude-process-stdin-patch/TRACEABILITY.md && grep -c '^| .526a606. ' .dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` — confirm at least 1 (the §3 commit table contains 526a606).
    3. Confirm Makefile contains `ship-coder:` target: `grep -n '^ship-coder:' Makefile` — confirm one match.
  - **Output**: All three sub-checks pass; results captured in ### Phase 4 Findings.
  - **Verification**: All checks PASS.
  - **Completion gate**: Phase 4 verifications PASS; ready to advance to Phase 5 GH issue filing.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

---

## Phase 5 — Defer-with-tracking issues (file as GH issues)

1 collapsed item that opens 13 GH issues against `IronbellyOrg/IronClaude` via `gh issue create`. **DELIBERATE A3 DEVIATION** — see ## Task Log / Notes "Phase 5 A3 Deviation Note" for justification. Source: R4 §"Phase 5 Canonical D-FOLLOW List (13 items, reconciled)" using merged-output §5.3 verbatim issue titles.

- [ ] **5.1 — Open 13 D-FOLLOW issues against `IronbellyOrg/IronClaude`**
  - **Owner**: branch-author (filer); maintainer / release-engineer / branch-author / beat-2 owner per row
  - **Severity**: TRACKING
  - **Refs**: refactor-plan §"Changes NOT Being Made" · merged-output.md §5.3 · R4 §"Phase 5 Canonical D-FOLLOW List"
  - **Target**: `IronbellyOrg/IronClaude` GitHub issues (13 new)
  - **Estimated LOC**: 0 (no code; 13 GH API calls)
  - **Context**: The /sc:adversarial pipeline's refactor-plan tier categorises 13 deferred items that should be tracked out-of-band rather than landed in this PR. Per R4's reconciliation: 10 items match exactly between refactor-plan D-FOLLOW-001..010 and merged-output §5.3; W-M10 (R-5 telemetry) matches; T-015/T-016 are merged-output-only echoes preserved here for audit (NOT to be filed if Phase 2 already lands them — but file the issue for tracking record). Phase 5 SKIPS refactor-plan D-FOLLOW-011/-012 because P-014 BEAT_2_BACKLOG.md already absorbs those items.
  - **Action**: For each row in the table below, run `gh issue create --repo IronbellyOrg/IronClaude --title "<Issue Title>" --body "<Body>"`, where `<Body>` is the standard template:
    ```
    Tracking issue filed by TASK-STDIN-RECON-REMEDIATION-20260501.

    **Owner**: <Owner from row>
    **Provenance**: <refactor-plan ID>
    **Source**: merged-output.md §5.3 / refactor-plan §"Changes NOT Being Made"

    Deferred from Beat-1 stdin-patch delta. See `.dev/architectural/claude-process-stdin-patch/adversarial-recon/merged-output.md` for full context.
    ```

    | # | Issue Title (verbatim, paste into GH) | Owner | refactor-plan ID |
    |---|---|---|---|
    | 1 | `[deferred] D-086: re-run failing 338 KB roadmap on /config/workspace/Coder` | release-engineer | D-FOLLOW-001 |
    | 2 | `[deferred] D-067: paste CI link confirming test_process_stdin.py runs in CI` | branch author | D-FOLLOW-002 |
    | 3 | `[deferred] U-033/U-034: PR-description amendment with verdict mapping link` | branch author (pre-merge) | D-FOLLOW-003 |
    | 4 | `[deferred] INV-005: wrap _stdout_fh/_stderr_fh in start()-level try/except` | maintainer | D-FOLLOW-004 |
    | 5 | `[deferred] INV-011: clamp negative SUPERCLAUDE_PROMPT_MAX_BYTES to default` | branch author | D-FOLLOW-005 |
    | 6 | `[deferred] INV-024: pin PortifyProcess anchor to first --output-format only` | maintainer | D-FOLLOW-006 |
    | 7 | `[deferred] INV-026: cache build_command() result for debug-log reuse` | maintainer | D-FOLLOW-007 |
    | 8 | `[deferred] INV-027: reorder T-005 to start() before timer schedule` | branch author | D-FOLLOW-008 |
    | 9 | `[deferred] INV-028: capture exception chain depth in _stdin_error` | maintainer | D-FOLLOW-009 |
    | 10 | `[deferred] INV-030: gate T-005 on Linux platform marker` | maintainer | D-FOLLOW-010 |
    | 11 | `[deferred] R-5: add prompt_encode_peak_bytes telemetry hook` | beat-2 owner | W-M10 |
    | 12 | `[deferred] T-016: tool_write_mode × BrokenPipe interaction test` | branch author (or maintainer) | (merged-output only) |
    | 13 | `[deferred] T-015: extra_args byte-size invariant test` | branch author (or maintainer) | (merged-output only) |

    Loop: for each row 1..13, execute the `gh issue create` call. Capture each returned issue URL into the Phase 5 Findings subsection of ## Task Log / Notes for traceability. If `gh` fails for any reason, log the row that failed and continue to subsequent rows; do NOT halt the loop on a single failure.

    NOTE: rows 12 and 13 (T-016, T-015) are filed as tracking issues even though Phase 2 may have already landed the actual tests in this PR — this preserves the audit trail. Mark those issues "closed by Phase 2 of this task" if the tests actually shipped.
  - **Output**: 13 new GH issues in IronbellyOrg/IronClaude; URLs captured in Phase 5 Findings.
  - **Verification**: After all 13 issues are filed, run `gh issue list --repo IronbellyOrg/IronClaude --search '[deferred]' --limit 20 --json number,title` — confirm at least 13 new `[deferred]` issues are present. (Pre-existing `[deferred]` issues unrelated to this delta will inflate the count, which is fine.)
  - **Completion gate**: 13 issues filed (or count of failures recorded with reasons); URLs captured.
  - If unable to complete due to missing context, file-access errors, GitHub auth issues, or unclear instructions, log the specific blocker(s) per row in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

---

## Phase 6 — Verification gate

5 items: full pytest suite, sync gates, pipx rebuild, version check, frontmatter close-out. This phase is the final integration verification + task close-out.

- [ ] **6.1 — Full pipeline + cli_portify pytest suite**
  - **Owner**: branch-author
  - **Severity**: VALIDATION
  - **Refs**: BUILD_REQUEST VALIDATION_REQUIREMENTS · BUILD_REQUEST TESTING_REQUIREMENTS=INTEGRATION
  - **Target**: N/A (verification step)
  - **Estimated LOC**: 0
  - **Context**: After all 4 prior phases land, the full `tests/pipeline tests/cli_portify` slice must pass with no regressions. Pre-task baseline: 13 tests in test_process_stdin.py + 14 in test_process.py + 33 in cli_portify/test_process.py = 60 in the slice (R2 §8). Post-task expected: at least 60 + 6 net new = 66 (P-007 = 1 in test_prd_process_stdin.py; T-013, T-014, T-015, T-016 = 4 in test_process_stdin.py; P-008 parametric = 2+ effective tests in test_subclass_terminate_invariant.py; P-013 is in-place rewrite). The full repo-wide suite (1294 → 1300) is the upstream gate.
  - **Action**: Run `uv run pytest tests/pipeline tests/cli_portify -v` and capture full output. Confirm:
    1. Zero failures.
    2. Test count is at least 66 (60 pre-task baseline + 5 net-new test names + ≥1 from the P-008 parametric expansion across known subclasses; >66 is acceptable if the parametric expands to more).
    3. ALL 6 new test names are visible in output: `test_prd_terminate_surfaces_stdin_error`, `test_nul_byte_prompt_round_trip`, `test_stdin_closed_in_finally_on_oserror`, `test_extra_args_size_invariant_caught`, `test_tool_write_mode_cleans_sidecar_on_broken_pipe`, `test_subclass_terminate_surfaces_stdin_error[...]` (parametric, ≥1 instance). If any of the 6 names are missing, halt — a Phase 1/2/3 item silently failed to land its test.
  - **Output**: pytest summary line captured to ### Phase 6 Findings; confirmation that no regressions vs pre-task baseline.
  - **Verification**: Full slice test run is GREEN. If anything fails: log the failing test name + trace in Phase 6 Findings; halt the rest of Phase 6 and escalate.
  - **Completion gate**: All tests pass; new tests visible.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **6.2 — `make sync-dev && make verify-sync` (sync clean)**
  - **Owner**: branch-author
  - **Severity**: VALIDATION
  - **Refs**: BUILD_REQUEST VALIDATION_REQUIREMENTS · CLAUDE.md "Component Sync"
  - **Target**: N/A (verification step)
  - **Estimated LOC**: 0
  - **Context**: This task did NOT edit any `src/superclaude/skills/` or `src/superclaude/agents/` files, so `make sync-dev` should be a no-op for stdin-patch content. However the sync gates must still verify clean state. Pre-existing rf-* / skill-creator drift in `.claude/` is acceptable per the task's prerequisites (do NOT fix it).
  - **Action**: Run `make sync-dev` and capture output (should be a no-op or report "already in sync" for stdin-patch-relevant paths). Then run `make verify-sync` and confirm:
    1. No NEW drift introduced by this task (i.e., no drift in `pipeline/`, `prd/`, `cli_portify/` directories).
    2. Pre-existing drift in `rf-*` / `skill-creator` agents is reported but is unchanged from the baseline at 2c21279.
  - **Output**: Sync output captured to ### Phase 6 Findings. New drift count delta = 0.
  - **Verification**: `make verify-sync` exits 0 OR reports only pre-existing drift (no new drift from this delta).
  - **Completion gate**: No NEW sync drift introduced; pre-existing drift acceptable.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **6.3 — `pipx install --force` from local wheel**
  - **Owner**: branch-author
  - **Severity**: VALIDATION
  - **Refs**: BUILD_REQUEST VALIDATION_REQUIREMENTS
  - **Target**: N/A (verification step)
  - **Estimated LOC**: 0
  - **Context**: Confirm the task's source edits (P-006, P-009, P-011, P-012, T-012) build a clean wheel and the wheel installs cleanly via pipx. This validates that no syntax error or import-time crash was introduced.
  - **Action**: Run:
    ```
    uv build
    pipx install --force /config/workspace/IronClaude/dist/superclaude-*.whl
    ```
    Capture both commands' output. `uv build` must produce a wheel under `dist/`. `pipx install --force` must report "installed package superclaude X.X.X" without errors.
  - **Output**: Wheel built; pipx install succeeded. Output captured to ### Phase 6 Findings.
  - **Verification**: Both commands exit 0; wheel file exists at `dist/superclaude-*.whl`; pipx reports successful install.
  - **Completion gate**: Wheel build and pipx install both succeed.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **6.4 — `superclaude --version` returns 4.2.0**
  - **Owner**: branch-author
  - **Severity**: VALIDATION
  - **Refs**: BUILD_REQUEST VALIDATION_REQUIREMENTS
  - **Target**: N/A (verification step)
  - **Estimated LOC**: 0
  - **Context**: Final confirmation that the pipx-installed wheel exposes the working CLI. Expected output: `SuperClaude, version 4.2.0`.
  - **Action**: Run `superclaude --version` and capture stdout. Confirm output contains `SuperClaude, version 4.2.0` (exact string match — both the literal `SuperClaude, version` prefix and the `4.2.0` version per project pyproject.toml).
  - **Output**: Version-string output captured to ### Phase 6 Findings.
  - **Verification**: `superclaude --version | grep 'SuperClaude, version 4.2.0'` returns one match.
  - **Completion gate**: Version string matches expected exactly.
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

- [ ] **6.5 — Task close-out: update frontmatter and append final summary**
  - **Owner**: branch-author
  - **Severity**: CLOSE-OUT
  - **Refs**: MDTM Template 02 anti-orphaning rule (R5 cites C3/C4); BUILD_REQUEST item 5
  - **Target**: This task file (`TASK-STDIN-RECON-REMEDIATION-20260501.md`) — frontmatter and ## Task Log / Notes
  - **Estimated LOC**: ~10 (frontmatter edits + summary)
  - **Context**: After all prior verifications pass, mark the task complete by updating the YAML frontmatter and appending a final summary to ## Task Log / Notes. This satisfies MDTM anti-orphaning (no separate post-completion section).
  - **Action**: Edit this task file:
    1. Frontmatter: change `status: "🟡 To Do"` to `status: "🟢 Done"`.
    2. Frontmatter: change `updated_date: "2026-05-01"` to today's actual completion date (use `date +%Y-%m-%d` if uncertain).
    3. Frontmatter: add a new field after `updated_date`: `completion_date: "<YYYY-MM-DD>"` (same date as updated_date).
    4. Append a new subsection to ## Task Log / Notes titled `### Final Summary` containing:
       - Total items completed (out of 22 in this task file: 18 P/T-NNN + 4 phase gates + 5 Phase 6 items, with Phase 5's 1 collapsed item replacing the 13 individual GH-issue rows).
       - Test count delta (expected +6: P-007, T-013, T-014, T-015, T-016, P-008-parametric).
       - Files modified count (expected: 5 source/test files modified + 4 new files created + 1 spec amendment + 1 Makefile edit + 13 GH issues filed).
       - Branch HEAD SHA after all commits (run `git rev-parse HEAD`).
       - Any deviations from the original plan (e.g., calibration notes that had to be re-tiered, gh CLI failures requiring re-run, etc.).
  - **Output**: This task file with status flipped to Done, completion_date populated, and a final summary subsection appended.
  - **Verification**: Run `grep -E '^status:|^completion_date:' .dev/tasks/to-do/TASK-STDIN-RECON-REMEDIATION-20260501/TASK-STDIN-RECON-REMEDIATION-20260501.md` — confirm `status: "🟢 Done"` and `completion_date:` are both present. Run `grep -c '### Final Summary' .dev/tasks/to-do/TASK-STDIN-RECON-REMEDIATION-20260501/TASK-STDIN-RECON-REMEDIATION-20260501.md` — confirm exactly 1.
  - **Completion gate**: Frontmatter updated; final summary appended; task ready for human archival to `.dev/tasks/done/` (manual move; not part of this item).
  - If unable to complete due to missing context, file-access errors, or unclear instructions, log the specific blocker in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file using the templated format, then mark this item complete. Once done, mark this item as complete.

---

## Task Log / Notes

### Execution Log

(Empty — populated by executor as items are completed. Use the format `<YYYY-MM-DD HH:MM> [item-id] <one-line outcome>`.)

### Phase 1 Findings

(Empty — populated by executor as Phase 1 items run. Use blocker-log template:
```
[BLOCKER item=X.Y date=YYYY-MM-DD] <short title>
- What I tried: ...
- What blocked me: ...
- Files involved: ...
- Suggested resolution: ...
```)

### Phase 2 Findings

(Empty — populated by executor as Phase 2 items run.)

### Phase 3 Findings

(Empty — populated by executor as Phase 3 items run.)

### Phase 4 Findings

(Empty — populated by executor as Phase 4 items run.)

### Phase 5 Findings

(Empty — populated by executor; capture URLs for the 13 filed GH issues here, one per row.)

### Phase 6 Findings

(Empty — populated by executor; capture pytest summary, sync output, pipx install output, version string, and the final close-out summary here.)

### Follow-Up Items

(Empty — populated as new follow-up items are discovered during execution. These items are NOT part of this task's scope; they are forward-pointers to be filed as separate tasks or GH issues.)

### Calibration Notes

P-011 (`__init__` `_stdin_error` init), P-012 (`prompt_via=stdin` log token), and T-012 (`n=0` silent break) are MEDIUM-severity in the refactor-plan but were flagged as over-calibrated by /sc:reflect:
- A-FINDING-006 (P-011, asymmetric `_stdin_error`): MEDIUM is over-calibrated; defensible LOW.
- A-FINDING-004 (P-012, log token): MEDIUM is over-calibrated; defensible LOW.
- A-FINDING-007 (T-012, `n=0` silent break): MEDIUM elevated from F LOW-2; defensible LOW.

These three items still land in this PR; the calibration note is purely for reviewer transparency. **If Phase 3 stalls for any reason, the MUST-tier (Phase 1 = P-006/P-007/P-009) plus the SHOULD-tier (Phase 2 = P-011/P-013/T-012/T-013/T-014/T-015/T-016) is defensibly mergeable per /sc:reflect.** Phase 4 tracking artifacts and Phase 5 GH issues can be filed in a follow-up if necessary, but Phases 1+2 alone close all HIGH-severity findings (INV-004 + INV-025 via P-006/P-007).

### Phase 5 A3 Deviation Note

Phase 5 collapses 13 D-FOLLOW issues into one checklist item (5.1). This is a deliberate deviation from MDTM rule A3 (Complete Granular Breakdown). Justification: the 13 issues share identical execution shape (`gh issue create --repo IronbellyOrg/IronClaude --title <title> --body <body>`) and differ only in title and owner per row. Atomicity is sacrificed for execution speed; the user explicitly authorized this collapse in the BUILD_REQUEST under the heading "CRITICAL — GRANULARITY REQUIREMENT" with the text "The single allowed exception is Phase 5 — collapse 13 D-FOLLOW issues into ONE checklist item that opens 13 GH issues sequentially". Per-row outcomes (success URL or failure reason) are still captured individually in the Phase 5 Findings subsection above, preserving audit-grade traceability without requiring 13 separate checklist rows.

### Pre-existing Constraints

64 sprint test failures in `tests/sprint/` are pre-existing (verified at pre-delta SHA `142ce15`). They are out of scope for this delta. **Do NOT fix.** The verify-sync drift on `rf-*` / `skill-creator` agents in `.claude/` is also pre-existing. Out of scope. **Do NOT fix.** Both pre-existing constraints are explicitly enumerated in the task's Prerequisites & Dependencies section above.

### Drift Log (anchor corrections vs refactor-plan)

The /sc:adversarial refactor-plan cites two anchors that drifted vs actual HEAD = 2c21279. Researcher 1 (R1) verified each anchor by reading current source and reported the corrections below. **The B2 item bodies in Phases 1 and 2 use the corrected line numbers, NOT the refactor-plan's stale citations.**

- **P-006 anchor**: refactor-plan cited `prd/process.py:277` — actual `_close_handles()` insertion target is **L279** (off by +2). The cited L277 points at `if self._on_exit is not None:` which is two lines above the actual call site. Insertion point in item 1.1 corrected to "before L279".
- **P-013 anchor**: refactor-plan cited `tests/pipeline/test_process_stdin.py:465-488` — actual T-011 test body is at **L262-285** (off by ~-200). The conditional assertion to be replaced (the `if proc._stdin_error is not None:` block) is specifically at **L282-285**. The test file is much shorter than the refactor-plan assumed. Anchor in item 2.2 corrected to "L262-285 with conditional at L282-285".

Both corrections are sourced from R1 §"Drift Summary" and R1 §"Builder-Usable Anchors", with paste-ready Before/After blocks already lifted into the corresponding item bodies above.

