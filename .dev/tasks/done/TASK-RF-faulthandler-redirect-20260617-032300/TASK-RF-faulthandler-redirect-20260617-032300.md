---
id: "TASK-RF-faulthandler-redirect-20260617-032300"
title: "Wire faulthandler into sprint entrypoint + prototype Rich Live redirect-disable"
description: "Two additive diagnostic changes to settle the H-C (Rich redirect-IO concurrency) vs H-A (unsafe fork) hypothesis for the sprint-runner Thread-1 TypeError crash, validated by re-running the boundary fork repro."
status: "🟢 Done"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-06-17"
updated_date: "2026-06-17"
start_date: "2026-06-17"
completion_date: "2026-06-17"
assigned_to: "orchestrator"
template_schema_doc: ".claude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: "20-30 min"
task_type: static
related_docs:
- path: ".dev/troubleshoot/bug-rich-render-none-20260616205900/REPORT.md"
  description: "Revised diagnosis — H-C leading (unproven), these two changes are its decisive next steps"
- path: "repro/boundary_fork_repro.py"
  description: "Validation harness (MODE=unsafe / MODE=fixed)"
tags:
- "diagnostics"
- "rich-tui"
- "sprint-runner"
---

# Wire faulthandler into sprint entrypoint + prototype Rich Live redirect-disable

## Task Overview

The sprint runner crashes in the Rich `Live` auto-refresh thread (Thread-1) with `TypeError: sequence item 139: expected str instance, NoneType found`. The revised troubleshoot diagnosis (see related REPORT.md) ruled out the original unsafe-fork theory (H-A, calibrated 0.25) in favor of an unproven Rich redirect-IO concurrency hypothesis (H-C): the TUI builds `Live(...)` with Rich's default `redirect_stdout/stderr=True`, so watchdog `print(..., file=sys.stderr)` and `_stall_logger.warning` calls route into the same `Console._buffer` the refresh thread renders. This task applies the report's two decisive next steps: (1) enable `faulthandler` so the next real crash yields a Python-vs-C stack, and (2) prototype disabling the Live redirect as the H-C probe + candidate fix.

**This is a diagnostic prototype, NOT a declared fix.** Success = changes applied + repro still green + faulthandler verified active. It does NOT claim the crash is fixed.

## Key Objectives

- Enable `faulthandler.enable(all_threads=True)` at the `superclaude sprint run` entrypoint (additive).
- Construct the TUI `Live(...)` with `redirect_stdout=False, redirect_stderr=False`.
- Re-run `repro/boundary_fork_repro.py` both modes; confirm still SURVIVE.
- Confirm existing TUI tests still pass and the working-tree diff is scoped to these two files (plus the 9 pre-existing runlock files, untouched).

## Prerequisites & Dependencies

- The working tree has 9 pre-existing uncommitted "sprint-runlock" changes (`commands.py` among them). **Do NOT stash, revert, commit, or alter them.** Both edits below must be additive.
- UV available (`uv run …`). Do NOT stage anything under `.claude/`.

---

## Phase 1: faulthandler wiring

- [x] **1.1 — Enable faulthandler at the sprint `run` entrypoint**
  - **Context**: `src/superclaude/cli/sprint/commands.py` defines the Click command `def run(ctx, index_path, ...)` at line 243 (the `superclaude sprint run` entrypoint; it calls `execute_sprint(config)` at line 412). No `faulthandler` exists anywhere in `src/superclaude/cli/` (verified). This file is ALSO modified by in-flight runlock work — the edit must be purely additive and must not alter any runlock lines.
  - **Action**: As the FIRST executable statement inside the `run()` function body (after the signature/decorators, before any existing logic), insert:
    ```python
    import faulthandler
    faulthandler.enable(all_threads=True)
    ```
    Place it at the top of the function body so it is active for the entire run. Do not gate it behind a flag — it is a cheap, always-on crash dumper. Match surrounding indentation.
  - **Output**: `commands.py` `run()` enables faulthandler with all-threads dumping; no other lines changed.
  - **Verification**: `grep -n "faulthandler" src/superclaude/cli/sprint/commands.py` shows the two new lines inside `run()`. `git diff src/superclaude/cli/sprint/commands.py` shows ONLY the additive faulthandler lines beyond the pre-existing runlock diff (no runlock hunk modified).
  - **Completion gate**: faulthandler import + `enable(all_threads=True)` present at the top of `run()`; runlock hunks untouched.

---

## Phase 2: Rich Live redirect-disable prototype

- [x] **2.1 — Disable stdout/stderr redirect on the TUI Live**
  - **Context**: `src/superclaude/cli/sprint/tui.py` lines 101-106 build `self._live = Live(self._render(), console=self.console, refresh_per_second=2, screen=False)`. Rich's `Live` defaults `redirect_stdout=True, redirect_stderr=True`, which wraps `sys.stdout`/`sys.stderr` in a `FileProxy` onto the TUI Console — the shared-Console concurrency surface H-C blames. This file is currently clean (not part of the runlock changes).
  - **Action**: Add `redirect_stdout=False, redirect_stderr=False` as keyword arguments to the `Live(...)` constructor at lines 101-106. Preserve the existing args (`console`, `refresh_per_second=2`, `screen=False`). Add a brief comment noting this is the H-C probe per the troubleshoot REPORT.
  - **Output**: TUI `Live` constructed with redirect disabled; watchdog/stall output no longer routes through the Live Console.
  - **Verification**: `grep -n "redirect_stdout=False" src/superclaude/cli/sprint/tui.py` matches the Live constructor. `uv run python -c "import superclaude.cli.sprint.tui"` imports cleanly.
  - **Completion gate**: `redirect_stdout=False, redirect_stderr=False` present in the `Live(...)` call; module imports.

---

## Phase 3: Validation

- [x] **3.1 — Re-run the boundary fork repro (both modes)**
  - **Context**: `repro/boundary_fork_repro.py` exercises the runner's thread topology. Both modes currently SURVIVE (exit 0); these changes must not regress that.
  - **Action**: Run, capturing exit codes:
    ```bash
    MODE=unsafe ITERS=20000 timeout 175 uv run python repro/boundary_fork_repro.py 2>&1 | tail -5
    MODE=fixed  ITERS=20000 timeout 175 uv run python repro/boundary_fork_repro.py 2>&1 | tail -5
    ```
  - **Output**: Both runs print `SURVIVED` and exit 0.
  - **Verification**: Both tails contain `SURVIVED ... — no SIGSEGV/deadlock observed`; both exit codes are 0.
  - **Completion gate**: Both modes SURVIVE; no new crash introduced by the edits.

- [x] **3.2 — Run TUI tests**
  - **Context**: `tests/sprint/test_tui_monitor.py` exercises the TUI and patches `process.os.setpgrp`. The redirect change and faulthandler import must not break it.
  - **Action**: `uv run pytest tests/sprint/test_tui_monitor.py -q`.
  - **Output**: Test run result.
  - **Verification**: All collected tests pass (exit 0). If any fail, inspect whether the redirect kwarg or faulthandler import is the cause; if unrelated to the edits (e.g., a pre-existing runlock failure), record that distinction in the Task Log.
  - **Completion gate**: TUI tests pass, OR any failure is shown to pre-date these edits (runlock-owned).

- [x] **3.3 — Confirm diff scope**
  - **Context**: The edits must touch only `commands.py` (additively) and `tui.py`, leaving the 9 pre-existing runlock files otherwise as they were.
  - **Action**: `git diff --name-only` and confirm the only files changed by THIS task beyond the pre-existing 9 are `commands.py` (additive hunk) and `tui.py`. (`commands.py` appears in both sets — verify its runlock hunks are intact via `git diff src/superclaude/cli/sprint/commands.py`.)
  - **Output**: Diff-scope confirmation.
  - **Verification**: No unexpected files modified; runlock hunks intact; `tui.py` newly modified; no `.claude/` paths staged.
  - **Completion gate**: Diff scope is exactly the two intended edits plus untouched runlock changes.

---

## Phase 4: Completion

- [x] **4.1 — Record outcome in the troubleshoot trail**
  - **Context**: The troubleshoot run at `.dev/troubleshoot/bug-rich-render-none-20260616205900/` is the home for this investigation's evidence.
  - **Action**: Append a short note to `repro-result.md` (or a new `prototype-result.md` in that dir) recording: the two edits applied, the repro re-run result, and that this is a probe awaiting the next real-runner crash (which faulthandler will now capture). Do NOT claim the crash is fixed.
  - **Output**: Evidence trail updated.
  - **Verification**: The note exists and is accurate (matches the actual repro exit codes from 3.1).
  - **Completion gate**: Outcome recorded honestly.

- [x] **4.2 — Update task status to Done**
  - **Context**: All phases complete.
  - **Action**: Update frontmatter: `status: "🟢 Done"`, set `updated_date`.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows `🟢 Done`.
  - **Completion gate**: Task marked complete.

---

## Task Log / Notes

### Execution Log
- (to be filled during execution)

### Phase Findings
- (to be filled during execution)

### Follow-Up Items
- If a real-runner crash is later captured by faulthandler with a clean Python stack → H-C confirmed; promote the redirect-disable from prototype to fix. If it shows a C-level/segfault stack → H-A regains weight; pursue `start_new_session=True`.
