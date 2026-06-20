# Research Notes: Corrective fix for swarm `--tui` FR-1 regression (REG-1) + FR-5 edges (DRIFT-3/DRIFT-4) + FR-1 audit hardening (DRIFT-2)

**Date:** 2026-06-19
**Scenario:** A (explicit — corrective task from a reflect-POST deviation register)
**Depth Tier:** Standard
**Track Count:** 1
**Source of truth:** `.dev/tasks/to-do/TASK-RF-swarm-tui-wiring-20260618-165434/reflect/post/ee9acb2266cb/deviation-register.yaml` (reflect UC-2 Tier-2 POST audit) — every claim below was **independently re-verified against live code + the driving spec** during scope discovery (file:line evidence inline).
**Driving spec:** `.dev/brainstorms/swarm-tui-wiring/merged-requirements.md` (FR-1 lines ~49-61, FR-2 ~63-72, FR-5 ~99-105).

---

## EXISTING_FILES

Source surfaces (all changes uncommitted in working tree; `git merge-base HEAD master` = `300c06a6` == register `start_commit`):

| File | Role | Verified state |
|------|------|----------------|
| `src/superclaude/cli/swarm/tui.py` | `TUI` dashboard wrapper around `rich.live.Live` | **`TUI.start()` at `tui.py:218-228` constructs `Live(self.render(...), console=..., refresh_per_second=..., screen=False)` with NO `redirect_stdout=`/`redirect_stderr=` args** → Rich default `redirect_stdout=True/redirect_stderr=True` is armed. [REG-1 root, CODE-VERIFIED] |
| `src/superclaude/execution/parallel.py` | `ParallelExecutor` (plan/execute/_execute_group) | **Unconditional `print()` at lines 110, 111, 164, 165, 176, 177, 183, 191, 196-200, 225, 232** — emit to stdout from the worker thread under the armed redirect. [REG-1 co-cause, CODE-VERIFIED] |
| `src/superclaude/cli/swarm/dispatch.py` | `dispatch_wave1` → constructs `ParallelExecutor` | `dispatch.py:424`: `executor = parallel_executor or ParallelExecutor(max_workers=workers_requested)` — the swarm dispatch call site. [CODE-VERIFIED] |
| `src/superclaude/cli/swarm/commands.py` | `run_cmd` poll loop (the TUI caller) | Eager `from ...tui import TUI, should_enable_tui` at `commands.py:1880` (DRIFT-1, out-of-scope this task). Poll loop `1943-1995`: `read_state` at **1944** + `_tail_events` at **1945** run OUTSIDE the `try/except Exception` that wraps only `tui_obj.update` (1956-1962) → DRIFT-3. Exception precedence `if interrupted: raise Exit(130)` at **1984-1986** runs BEFORE `if "e" in exc_box: raise exc_box["e"]` at **1990-1991** → DRIFT-4. [CODE-VERIFIED] |
| `src/superclaude/cli/swarm/state.py` | `read_state()` | `state.py:~195`: raises `json.JSONDecodeError` on corrupt JSON and `ValueError` on shape-invalid payload (unguarded in poll loop → DRIFT-3). [CODE-VERIFIED] |
| `tests/swarm/test_inv012_tui_opt_in.py` | FR-1 AST audit | `test_worker_surfaces_have_zero_tui_reachability` at **655-713** audits only forbidden **import/name symbols** (rich/Live/Console/TUI) on dispatch.py + parallel.py — NOT `print(`/`sys.stdout`/`sys.stderr` writes, and per-file only (not transitive call graph). [DRIFT-2 root, CODE-VERIFIED] |
| `tests/swarm/test_run_tui_integration.py` | FR-1..FR-7 integration (untracked, 680 lines) | `test_frozen_signatures_unchanged` at **622-672** pins `ParallelExecutor.__init__` params to EXACTLY `["self", "max_workers"]` with `max_workers` default 10. [FROZEN-SIGNATURE CONSTRAINT, CODE-VERIFIED] |
| `tests/swarm/test_tail_events.py` | `_tail_events` unit tests (untracked, 124 lines) | Existing byte-offset tail coverage. |

## PATTERNS_AND_CONVENTIONS

- **UV-only** for all Python ops (`uv run pytest ...`). Never bare `python`/`pip`.
- **Source-of-truth sync:** `src/superclaude/` is canonical; `make sync-dev` copies to `.claude/`. The files here are pure `src/` Python + `tests/` — no `.claude/` involvement.
- **`run_cmd` deferred-import idiom:** `should_enable_tui`/`TUI`/`dispatch_wave1` resolved via function-local imports so tests monkeypatch on the SOURCE module (`superclaude.cli.swarm.tui`). The integration test forces the TTY seam by monkeypatching `should_enable_tui→True` on the source module.
- **FR-1 single-writer topology** is the *whole point* of the feature: workers' only output channel MUST be the filesystem; exactly one thread (main) touches the Console. The active design (Approach A) was chosen specifically to kill the #181/#182/#184 cross-thread `Live` render crash.
- **Render-glitch latch** (`except Exception: pass` around `tui.update`, scoped to `Exception` so `KeyboardInterrupt` still propagates) is the established defensive idiom (AUTH-2) — DRIFT-3 should extend the SAME guard discipline to the readers.
- **Exception/exc_box pattern:** non-daemon worker writes return value to `result_box`/`exc_box`; main thread re-raises after `tui.stop()` + `join()` (FR-5 anti-masking).
- Tests are unmarked (`--strict-markers` on; no `tui` marker registered).

## GAPS_AND_QUESTIONS

- **FROZEN-SIGNATURE CONSTRAINT (load-bearing):** silencing `ParallelExecutor` prints MUST NOT alter `ParallelExecutor.__init__(self, max_workers=10)`. A `quiet=` kwarg on `__init__` WOULD fail `test_frozen_signatures_unchanged` (test_run_tui_integration.py:666-669). Resolution baked into research/01: use a **class-attribute default `quiet: bool = False`** that the swarm dispatch site flips on the instance (`executor.quiet = True`), with each `print()` in plan/execute/_execute_group guarded by `if not self.quiet:`. Signature stays `["self", "max_workers"]`; other callers (execution/__init__.py, sprint convenience fns) keep prints by default. This is the ONLY signature-preserving way to satisfy "gate prints in parallel.py on the swarm dispatch path".
- **Real-PTY smoke:** non-TTY `CliRunner` streams cannot reproduce the TTY-only cross-thread race (`why_tests_missed_it`). The smoke must run under a real PTY (`pty.openpty()` / `os.openpty`) so `stream.isatty()` is True and the armed-redirect race is exercised. Must assert no crash/traceback under concurrent worker stdout. `pty` is POSIX-only — guard with `sys.platform`/skip on Windows.
- **DRIFT-4 chaining semantics:** when SIGINT and a worker crash race, the worker exception in `exc_box` must NOT be silently discarded by `raise Exit(130)`. Decide: surface the worker exception (preferred — it's the FR-5 non-negotiable "exception not masked"), optionally chained with the interrupt. Simplest correct fix: check `exc_box` BEFORE the `interrupted` branch (worker crash dominates a concurrent interrupt) OR chain via `raise exc_box["e"] from KeyboardInterrupt()`-style. The executor must preserve the original traceback.
- **DRIFT-3 fix shape:** wrap `read_state` + `_tail_events` in a guard that catches the expected `ValueError`/`json.JSONDecodeError` and **continues** the loop (a torn/transient read is not a worker crash) so the loop still reaches `dispatch_thread.is_alive()` and the post-loop `exc_box` re-raise. Must NOT broaden to catch `BaseException`/`KeyboardInterrupt`.

## RECOMMENDED_OUTPUTS

Research files (evidence trail):
- `research/01-reg1-redirect-and-print-gating.md` — REG-1 two-part fix + frozen-signature constraint.
- `research/02-drift3-drift4-fr5-poll-loop.md` — DRIFT-3 reader guard + DRIFT-4 exception precedence.
- `research/03-fr1-audit-extension-and-pty-smoke.md` — DRIFT-2 audit hardening (stdout-write detection + transitive coverage) + real-PTY smoke design + FR-5 regression tests for DRIFT-3/4.

## SUGGESTED_PHASES

- **Phase 1 — REG-1 source fix (tui.py + parallel.py + dispatch.py).** (a) tui.py:221 add `redirect_stdout=False, redirect_stderr=False`. (b) parallel.py add class-attr `quiet=False` + guard all prints. (c) dispatch.py:424 set `executor.quiet = True` on the swarm-constructed instance.
- **Phase 2 — FR-5 edge fixes (commands.py poll loop).** DRIFT-3 reader guard; DRIFT-4 exception precedence so a worker crash is never masked by `Exit(130)`.
- **Phase 3 — Test hardening.** DRIFT-2 audit extension (flag `print(`/`sys.stdout`/`sys.stderr` writes + cover invoked callables) in test_inv012_tui_opt_in.py; real-PTY `--tui` smoke; DRIFT-3 + DRIFT-4 regression tests; frozen-signature test still green.
- **Phase 4 — Validation + completion.** `uv run pytest tests/swarm/ -v`, `uv run ruff check`, `uv run ruff format --check src/ tests/`; POST reflect wrapper; status→Done.

## TEMPLATE_NOTES

- **Template 02** (complex): multi-phase (source fix → exception-semantics fix → test hardening → validation), interacting constraints (frozen signature, FR-5 non-masking), and a discovery-sensitive PTY smoke.
- **Tier Standard:** 4 source files + 3 test surfaces; 4 interacting deviations; not Quick because the frozen-signature + FR-5-ordering + PTY-portability constraints need careful per-item encoding.
- VALIDATION_REQUIREMENTS: ruff check + ruff format --check + full `tests/swarm/` suite green.
- TESTING_REQUIREMENTS: UNIT (audit extension, DRIFT-3/4 regressions) + a real-PTY integration smoke.

## AMBIGUITIES_FOR_USER

- **Out of scope (per the user's explicit GOAL):** DRIFT-1 (eager `import TUI` at commands.py:1880) and NEC-1 (documented necessary deviation) are NOT requested. DRIFT-2 is in scope only as folded into the FR-1 audit extension (the user asked to "extend the FR-1 audit"). The task fixes exactly REG-1, DRIFT-3, DRIFT-4, and the DRIFT-2 audit hardening. If the user later wants DRIFT-1 (the eager-import gateway), that is a separate follow-up — noted in the task's Open Questions, not actioned here.
