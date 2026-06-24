# Research Notes: faulthandler wiring + Rich Live redirect-disable prototype

**Date:** 2026-06-17
**Scenario:** A (explicit — file:line targets verified)
**Depth Tier:** Quick (<5 files, single concern, no discovery needed)
**Track Count:** 1
**Provenance:** Verified across troubleshoot turns 1–4; see `.dev/troubleshoot/bug-rich-render-none-20260616205900/` (REPORT.md revised, repro-result.md, tier2-quality-engineer-REDISPATCH.md). NOT re-discovered by spawned researchers — the orchestrator right-sized to Quick given the 2-line additive scope and a prior 429.

---

## EXISTING_FILES
- `src/superclaude/cli/pipeline/process.py` — `ClaudeProcess`; `run()`-adjacent fork at `:189-190` (`preexec_fn=os.setpgrp`); kill path `terminate()` `:284-304`. NOTE: modified by in-flight runlock work; NOT touched by this task.
- `src/superclaude/cli/sprint/commands.py` — `run()` Click command at line 243 (the `superclaude sprint run` entrypoint); calls `execute_sprint(config)` at line 412. **Modified by in-flight runlock work** (has `--ignore-run-lock`). Faulthandler edit MUST be additive.
- `src/superclaude/cli/sprint/tui.py` — `start()` builds `self._live = Live(self._render(), console=self.console, refresh_per_second=2, screen=False)` at lines 101-106. **Clean / unmodified.** Redirect kwargs go here.
- `repro/boundary_fork_repro.py` — MODE=unsafe / MODE=fixed harness. Both currently SURVIVE (exit 0).
- `tests/sprint/test_tui_monitor.py` — patches `process.os.setpgrp`; exercises TUI. Run after changes.

## PATTERNS_AND_CONVENTIONS
- No `faulthandler` anywhere in `src/superclaude/cli/` (verified grep). The repro uses `faulthandler.enable(all_threads=True)` + `dump_traceback_later` — mirror `all_threads=True`.
- Watchdog/TUI errors are emitted via `print(..., file=sys.stderr)` (executor.py:1876/1889/1915/1927/1944) and `_stall_logger.warning` (executor.py:1458). With Rich Live default `redirect_stderr=True`, these route into the shared Console.
- UV only (`uv run …`). Tests in `tests/` via pytest.

## GAPS_AND_QUESTIONS
- None blocking. Whether to gate faulthandler behind an env var: decision — always-enable `all_threads=True` (harmless; the whole point is to catch the next real crash). Keep it cheap and unconditional.

## RECOMMENDED_OUTPUTS
- Edit 1: `commands.py` `run()` — add `import faulthandler; faulthandler.enable(all_threads=True)` as the first statement in the function body (additive; does not touch runlock changes).
- Edit 2: `tui.py:101-106` — add `redirect_stdout=False, redirect_stderr=False` to the `Live(...)` constructor.

## SUGGESTED_PHASES
1. faulthandler wiring (commands.py)
2. redirect disable (tui.py)
3. Validation (repro ×2 + pytest + diff-scope check)
4. Completion

## TEMPLATE_NOTES
Template 01 (generic) — additive, ≤2 files, known inputs/outputs, no discovery. Diagnostic prototype, NOT a declared fix.

## AMBIGUITIES_FOR_USER
None — intent and locations are clear and verified.
