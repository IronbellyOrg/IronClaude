# BUILD_REQUEST — faulthandler + Rich redirect-disable diagnostics for the sprint-runner crash

## GOAL
Implement two small, additive changes that turn the leading (unproven) H-C hypothesis into a settleable one, then validate by re-running the repro:

1. **Wire `faulthandler` into the sprint entrypoint** so the *next real crash* in the Rich `Live` refresh thread (Thread-1) prints a definitive all-threads stack — distinguishing a clean Python `TypeError` (H-C: Rich concurrency) from a C-level segfault (H-A: fork/heap corruption).
2. **Prototype the Rich Live redirect disable** — construct the TUI `Live(...)` with `redirect_stdout=False, redirect_stderr=False`. This is the cheap H-C probe + candidate fix: it removes the cross-thread writes into the shared `Console._buffer`.

Then re-run the repro to confirm no regression, and (stretch) attempt a more realistic reproduction.

## WHY
Per `.dev/troubleshoot/bug-rich-render-none-20260616205900/REPORT.md` (revised 2026-06-17): the original unsafe-fork diagnosis (H-A) was empirically disconfirmed — the repro `MODE=unsafe` SURVIVED, and independent calibration dropped H-A to 0.25, subordinate to **H-C (Rich `redirect_stdout/stderr=True` shared-Console concurrency)**. The crash is a clean Python `TypeError`, which argues for concurrency over corruption. These two changes are the report's decisive next steps. Neither hypothesis is proven; this work is to *settle* it, not to declare a fix.

## WHERE (verified locations)
- **Change 1 (faulthandler):** `src/superclaude/cli/sprint/commands.py` — function `run()` at line 243 (the `superclaude sprint run` entrypoint; calls `execute_sprint(config)` at line 412). Add `import faulthandler; faulthandler.enable(all_threads=True)` as early as possible in the process. Gate on an env var (e.g. honor `PYTHONFAULTHANDLER` already-on, and additionally force-enable) so it is always active for the runner. No faulthandler exists anywhere in `src/superclaude/cli/` today (verified).
- **Change 2 (redirect):** `src/superclaude/cli/sprint/tui.py` lines 101-106 — the `self._live = Live(self._render(), console=self.console, refresh_per_second=2, screen=False)` constructor. Add `redirect_stdout=False, redirect_stderr=False`. (File is currently clean / unmodified.)
- **Validation:** `repro/boundary_fork_repro.py` — re-run `MODE=unsafe` and `MODE=fixed` (ITERS=20000). Both currently SURVIVE; confirm still true.

## CONSTRAINTS (hard)
- **Work alongside existing uncommitted changes — do NOT stash, revert, commit, or alter them.** The working tree has 9 modified tracked files from an in-flight "sprint-runlock" feature (`commands.py`, `config.py`, `executor.py`, `models.py`, `recovery.py`, `rerun_tasks.py`, `tmux.py`, `tests/sprint/test_recovery.py`, `tests/sprint/test_tmux.py`) plus `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/`. `commands.py` (my faulthandler target) is among them — my edit MUST be additive and must not disturb the runlock changes. `tui.py` is clean.
- **UV only** — no bare `python`/`pip`. Tests via `uv run pytest`.
- **Do NOT stage anything under `.claude/`** (gitignored sync output; only `.claude/settings.json` is tracked).
- This is a **prototype/diagnostic**, not a declared fix. The task must NOT claim the crash is fixed; success = changes applied + repro still green + faulthandler verified active.
- Branch/worktree: `worktree-segfault-repro`. Do not open PRs or push.

## VERIFICATION / DONE CRITERIA
1. `faulthandler.enable(all_threads=True)` active in the sprint `run` path — prove with a tiny check (e.g. `uv run python -c "import superclaude.cli.sprint.commands"` then assert `faulthandler.is_enabled()` after invoking the enable site, OR a unit assertion).
2. `tui.py` Live constructed with `redirect_stdout=False, redirect_stderr=False` — assert via grep + a focused unit test if one fits.
3. `MODE=unsafe ITERS=20000 uv run python repro/boundary_fork_repro.py` and `MODE=fixed …` both still print `SURVIVED` (exit 0).
4. `uv run pytest tests/sprint/test_tui_monitor.py` (and any tui/commands tests) still pass — confirm the redirect change and faulthandler import don't break existing TUI tests.
5. `git diff --name-only` shows ONLY `commands.py` and `tui.py` newly touched by THIS work beyond the pre-existing 9 runlock files (i.e., I didn't disturb others).

## TEMPLATE
Generic (template 01) — small, ≤3 files, additive.
