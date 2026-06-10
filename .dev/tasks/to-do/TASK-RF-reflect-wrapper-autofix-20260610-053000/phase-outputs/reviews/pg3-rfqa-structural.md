# QA Report — PG3 Structural Review (reflect-wrapper autofix)

**Topic:** `commands.py` — autofix flags, promote flip, marker self-suppress, tmux base forwarding
**Date:** 2026-06-10
**Phase:** report-validation (structural lens, report-only)
**Fix cycle:** N/A
**Source of truth:** `src/superclaude/cli/reflect/commands.py` (Read in full, 336 lines)
**Stance:** ADVERSARIAL / fail-closed. Verified every claim against source; phase3-summary.md treated as a claim, not evidence.

---

## Overall Verdict: PASS

All six structural criteria verified against `commands.py` with file:line evidence. No CRITICAL markers triggered: the marker guard is at group/eager-callback level (not in-run()-body), truthiness is exactly `== "1"`, `--base` is forwarded under `--tmux`, and there is NO wrapper-side O2 force of `--no-promote`.

---

## Items Reviewed

| # | Criterion | Result | Evidence (file:line) |
|---|-----------|--------|----------------------|
| 1a | `--fix/--no-fix` exists, default False | PASS | `commands.py:127-132` — `@click.option("--fix/--no-fix", "fix", default=False, ...)`. Param in `run()` sig at `:159` (`fix: bool`). |
| 1b | `--max-fix-iterations` int, default 2 | PASS | `commands.py:133-138` — `type=int, default=2`. Param at `:160` (`max_fix_iterations: int`). |
| 1c | `--base` dest `base_override`, default None | PASS | `commands.py:139-147` — `@click.option("--base", "base_override", default=None, ...)`. Param at `:161` (`base_override: str | None`). |
| 1d | All three threaded into `resolve_config` | PASS | `commands.py:188-189` — `fix=fix, max_fix_iterations=max_fix_iterations, base_override=base_override` passed positionally within `resolve_config(...)` call (`:175-190`). Names match dest names exactly. |
| 2a | `--promote/--no-promote` default now `True` | PASS | `commands.py:89-94` — `@click.option("--promote/--no-promote", "promote", default=True, ...)`. Help: "default: --promote". |
| 2b | NO wrapper-side O2 auto-force of `--no-promote` | PASS | `grep "no-promote\|O2\|force"` → only `:93` (help text documenting O2 *caller* convention), `:297-299` (explicit forward keyed on `config.promote`). No code path overrides `promote`/`config.promote` to False. `resolve_config` receives `promote=promote` verbatim (`:181`). |
| 3a | Marker guard exits 0 | PASS | `commands.py:69-73` — `if ...== "1": click.echo(...); sys.exit(0)`. |
| 3b | Guard at GROUP/eager-callback level (pre-empts `exists=True`) | PASS | Guard body is inside `reflect_group()` — the `@click.group("reflect")` callback (`:47-48`), which runs at parse time. It is NOT in `run()`'s body (`run()` opens at `:148`, first body stmt `:169`). Comment `:62-68` states the load-bearing rationale. `exists=True` is on the `tasklist` arg of the `run` subcommand (`:77-80`), validated only after the group callback. **No in-run()-body marker check exists** (grep confirms the only `_WRAPPER_MARKER_ENV` read is `:69`). |
| 3c | Truthiness EXACTLY string `"1"` | PASS | `commands.py:69` — `os.environ.get(_WRAPPER_MARKER_ENV, "").strip() == "1"`. Equality on literal `"1"`, not `bool()`/truthy/`in`. Empty/`"0"`/`"2"`/other → falls through, runs normally. |
| 4 | `_build_inner_command` forwards `--base` under `--tmux` | PASS | `commands.py:306-307` — `if config.base_override: cmd += ["--base", config.base_override]`. `_build_inner_command` (`:279`) is the inner argv builder invoked only by `_launch_tmux` (`:319`). Single-ref pass-through, no `..` range (comment `:304-305`). |
| 5 | Heavy imports stay lazy inside `run()` | PASS | `commands.py:169-170` — `from .config import resolve_config` / `from .runner import ReflectRunner` inside `run()` body. Except-path lazy imports `:202-203` (`models`, `runner.write_sidecar`). Module top (`:15-24`) imports only stdlib + `click`. |
| 6a | NO `cli.sprint`/`cli.roadmap` import | PASS | `grep -E "cli\.sprint\|cli\.roadmap\|import.*sprint\|import.*roadmap"` → no matches. |
| 6b | NO `async`/`await` added | PASS | `grep -E "\basync\b\|\bawait\b"` → no matches. |
| 6c | `subprocess.run` for `--tmux` is allowed (not a defect) | PASS | `commands.py:320,325,327` — `subprocess.run` only in `_launch_tmux` for tmux new-session/attach/kill. Per spec this is permitted. |
| 7 | (Per prompt note) `_build_inner_command` forwards promote explicitly | PASS — CORRECT, not a defect | `commands.py:299` — `cmd.append("--promote" if config.promote else "--no-promote")`. Comment `:296-298` documents this as the fail-closed completion of the promote-default flip: without it, `--tmux --no-promote` would silently promote in the inner reinvocation. Evaluated as intended behavior. |

---

## Summary

- Checks passed: 17 / 17
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found

None.

## CRITICAL-marker probes (all negative)

| Probe | Outcome |
|-------|---------|
| In-run()-body marker guard | NEGATIVE — sole `_WRAPPER_MARKER_ENV` read is at group callback `:69`; `run()` body has none. |
| Too-loose truthiness (`bool()`, truthy, `in`, no `.strip()`) | NEGATIVE — exact `.strip() == "1"` at `:69`. |
| Missing `--base` tmux forward | NEGATIVE — forwarded at `:306-307`. |
| Wrapper-side O2 force of `--no-promote` | NEGATIVE — no override of `promote`/`config.promote`; only explicit forward keyed on caller value. |

## Confidence Gate

- Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Every criterion checked with Read (full file) + targeted Grep; each tool call maps to a specific criterion.

**Tool engagement:** Read: 2 | Grep: 4 (single batched Bash) | Glob: 0 | Bash: 2

No external/web lookup required (all claims are local-source-bound).

## Recommendations

- Green light on the structural lens for `commands.py` PG3 scope. The phase3-summary.md claims are corroborated by source.
- Out of structural scope (not a gate blocker, noted for the orchestrator): phase3-summary reports 1 failing pre-existing test (task-builder marker) and a deferred `_SPEC9_FLAGS` whitelist extension (Step 6.9). Behavioral/runtime correctness of `resolve_config` consuming the three new kwargs was NOT verified here (config.py out of this review's file scope) — confirm in the config/runner review.

## QA Complete
