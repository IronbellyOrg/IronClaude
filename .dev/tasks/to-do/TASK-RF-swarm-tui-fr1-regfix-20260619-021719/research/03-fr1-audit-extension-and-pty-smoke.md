# Research: DRIFT-2 FR-1 audit hardening + real-PTY smoke + FR-5 regression tests

**Topic type:** Test & Verification
**Scope:** `tests/swarm/test_inv012_tui_opt_in.py:640-713`, `tests/swarm/test_run_tui_integration.py`
**Status:** Complete
**Date:** 2026-06-19

---

## DRIFT-2 (FR-1, MED) — the audit checks the wrong invariant

`test_worker_surfaces_have_zero_tui_reachability` (test_inv012_tui_opt_in.py:655-713) + `_TuiSymbolVisitor` (visit_Import/visit_ImportFrom/visit_Attribute, ~600-643) flag only **forbidden TUI/Rich import & name symbols** (`_FORBIDDEN_TUI_NAMES` = TUI/Live/Console/should_enable_tui) on `dispatch.py` + `parallel.py`. It does NOT detect `print(`/`sys.stdout`/`sys.stderr` writes, and it is **per-file** (each module's own symbol table), not the transitive call graph FR-1's acceptance text demands ("any callable they invoke"). That is exactly why REG-1 shipped green.

**Fix — extend the audit (fold DRIFT-2 into REG-1):**
1. Add a stdout-write detector to the AST visitor: flag `print(...)` Call nodes and any `Attribute` access of `sys.stdout` / `sys.stderr` (and `.write`/`.flush` on them) within `dispatch.py` + `parallel.py`. Keep the existing import/name checks.
2. Keep the MANDATORY vacuity guard (≥1 module scanned) and add a **mutation guard** for the new rule: a synthetic `print('x')` and `sys.stdout.write('x')` source MUST be flagged, proving the new detector isn't a no-op.
3. (Transitive coverage) At minimum, document the per-file limitation and assert the two known worker surfaces are clean; a full call-graph walk is optional but the stdout-write rule on the two modules closes the REG-1 gap. Pin `_run_worker` lives in dispatch.py (existing assertion at 690-695) so coverage doesn't silently move.

After the fix, the gated `parallel.py` prints (`if not self.quiet:` guarded — see research/01) are STILL `print(` calls in source, so the audit would flag them. Resolution: the audit's intent is "worker surfaces emit nothing to the Console **when on the dispatch path**". Two viable encodings — the executor picks one and documents it:
- (a) Assert `parallel.py` prints are ALL guarded by a `self.quiet` conditional (the detector flags an UNGUARDED `print(`/stdout-write only); or
- (b) Assert `dispatch.py` flips `executor.quiet = True` AND that `parallel.py` has the `quiet` gate, treating the guard as the structural proof.
Option (a) is the stronger structural invariant (it directly proves "no unconditional stdout write on a worker surface").

## Real-PTY `--tui` smoke (REG-1 acceptance — the test that would have caught it)

The non-TTY `CliRunner` streams used by all existing `--tui` integration tests cannot reproduce the TTY-only cross-thread race (`why_tests_missed_it`). Add a smoke that runs under a **real PTY** so `stream.isatty()` is True and the armed-redirect race is exercised with concurrent worker stdout.

Design:
- Use `pty.openpty()` (POSIX) to get a master/slave fd; run `swarm run --tui` (or drive `run_cmd` with the slave as stdout) so `should_enable_tui` sees a TTY.
- Ensure the worker path actually emits stdout concurrently (the very prints REG-1 is about) — e.g. an unguarded-print baseline would crash; the fixed path must NOT.
- **Assert:** process completes with a non-crash exit (no `Traceback`/render-crash in master-fd output), terminal restored.
- **Portability:** `pty` is POSIX-only → `@pytest.mark.skipif(sys.platform == "win32", reason="pty is POSIX-only")` (or `not hasattr(os, "openpty")`). Mirror the subprocess/pty idiom already present in `test_inv_suite.py` (references `pty`/`pexpect`) and `test_inv012_tui_opt_in.py` (PTY usage exists there per grep).
- Keep it deterministic & bounded (small worker count, the `_TUI_POLL_MAX_ITERATIONS` injection seam, short timeout) so it doesn't hang CI.

## FR-5 regression tests (DRIFT-3 + DRIFT-4)
Add to `test_run_tui_integration.py` (or a new `tests/swarm/test_fr5_masking.py`):
- **DRIFT-3:** monkeypatch `read_state` to raise `ValueError` on a poll iteration while `exc_box` holds a worker exception → assert the WORKER exception reaches the caller (not the ValueError, not a clean exit), terminal restored, `tui.stop()` ran.
- **DRIFT-4:** drive the loop so `interrupted=True` AND `exc_box["e"]` is set → assert the worker exception is surfaced/chained (not a bare `Exit(130)`), preserving the original traceback.
- Keep the existing FR-6 SIGINT-only test green (no concurrent crash → still `Exit(130)`).

## Validation surface
- `uv run pytest tests/swarm/ -v` (full swarm suite incl. frozen-sig + INV-012 audit + new tests).
- `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/` (CI runs format --check separately — green `make lint` ≠ green CI format, per project memory).
