# Prototype applied — faulthandler + Rich Live redirect-disable

**Date:** 2026-06-17
**Task:** `.dev/tasks/to-do/TASK-RF-faulthandler-redirect-20260617-032300/`
**Status:** prototype applied + validated green. NOT a confirmed fix.

## Changes applied (additive, alongside in-flight runlock work)
1. `src/superclaude/cli/sprint/commands.py` — `run()` now calls `faulthandler.enable(all_threads=True)` at the top of its body. The next real Thread-1 crash will print an all-threads stack (Python-vs-C), which definitively separates H-C (clean Python `TypeError`) from H-A (C-level segfault).
2. `src/superclaude/cli/sprint/tui.py:101` — the TUI `Live(...)` is now built with `redirect_stdout=False, redirect_stderr=False`, removing the cross-thread writes (watchdog `print`/`_stall_logger.warning`) into the shared `Console._buffer`. This is the H-C candidate fix.

## Validation
| Check | Result |
|-------|--------|
| `import superclaude.cli.sprint.{tui,commands}` | OK |
| `MODE=unsafe ITERS=20000` repro | SURVIVED, exit 0 (38.4s) |
| `MODE=fixed ITERS=20000` repro | SURVIVED, exit 0 (21.1s) |
| `pytest tests/sprint/test_tui_monitor.py` | 5 passed |
| diff scope | only `tui.py` net-new + additive `commands.py` faulthandler hunk; 9 runlock files untouched; no `.claude/` staged |

## Honest status
- This does **not** prove the fix. The repro never reproduced the original crash (it survived even before these edits), so it cannot confirm the redirect change fixes anything — it only confirms no regression.
- **The real test is the next production crash.** With faulthandler now active, if the sprint runner crashes again: a clean Python `TypeError` stack through `live.py → _render_buffer` confirms H-C (promote the redirect-disable to the fix); a C-level/segfault dump points back to H-A (pursue `start_new_session=True` at `process.py:189-190`).
- The redirect-disable is low-risk to leave in regardless: watchdog/stall output now goes straight to the real stderr instead of through the Live Console.
