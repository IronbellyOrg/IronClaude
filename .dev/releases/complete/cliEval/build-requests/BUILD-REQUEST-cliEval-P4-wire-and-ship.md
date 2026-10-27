# BUILD REQUEST: cliEval-P4 — Wire `eval_group` into `cli/main.py` + Makefile target + `.gitignore`

## What This Is

Phase 4 of the **cliEval release** — the smallest and lowest-risk phase. Wires the `eval_group` Click group from P1-P3 into the top-level `superclaude` CLI, adds a `make eval-real` convenience target, and updates `.gitignore` to keep eval artifacts out of git.

After this phase merges, `uv run superclaude eval --help` works, `make eval-real` works as a shortcut, and `.dev/eval-runs/<ISO>/<run-id>/evals/<eval-id>/home/` directories never accidentally get committed.

## Why It Matters

P1, P2, and P3 build the harness internals. None of that is REACHABLE from the `superclaude` top-level command until this phase wires `eval_group` into `main.py`. This is a 2-line code change but it's also the "ship gate" — once merged, end users can invoke the harness.

This phase exists as its own task (not bundled into P3) because:
1. It's a separate concern (wiring vs. building).
2. P3's smoke test (`test_eval_run_smoke.py`) drives `eval run` directly via Click's testing API or `uv run superclaude eval run`. The end-user `superclaude eval` invocation only works after THIS phase lands.
3. Splitting reduces blast radius — if P3 has a bug, we can fix it in isolation without touching `main.py` or the Makefile.

## Inputs (read before starting)

- **Design spec:** `.dev/releases/current/cliEval/design-spec.md` — read §3 (directory layout), §10 (integration with existing IronClaude code), §17 (Phase 4 details).
- **Phase 1, 2, 3 outputs (DEPENDENCIES, must all be MERGED):** `cli/eval/` directory complete with `eval doctor`, `eval list`, `eval describe`, `eval run`. All Phase 3's tests must be green on master before P4 starts.
- **Existing wiring pattern:** `src/superclaude/cli/main.py:369-391` — the `add_command()` block where sub-package Click groups are registered. P4 adds exactly TWO lines to this block.

## Scope (what THIS task builds)

### Files to MODIFY

1. **`src/superclaude/cli/main.py`** — Add 2 lines: `from .eval import eval_group` (top imports) + `main.add_command(eval_group)` (registration block). Place alphabetically among existing add_commands.
2. **`Makefile`** — Add a new target `eval-real` after the `verify-sync` target:
   ```makefile
   # Run the real-world eval suite locally (15 evals × parallel=8 by default)
   eval-real:
       @echo "🧪 Running real-world eval suite..."
       uv run superclaude eval run --suite real
   ```
   Also add `eval-real` to the `.PHONY:` declaration at line 1.
3. **`.gitignore`** — Add 2 lines:
   ```
   # cliEval eval-run artifacts
   .dev/eval-runs/**/home/
   .dev/eval-runs/**/stdout.log
   .dev/eval-runs/**/stderr.log
   ```
   (Per-eval HOMEs can be GB-scale + contain user-specific paths; never commit. TTY logs may contain ANSI sequences that bloat diffs.)
4. **`src/superclaude/cli/main.py` help-text update** (if applicable) — if `main.py` has a docstring or help epilog enumerating subcommands, add `eval` to it.

### Files to CREATE

5. **`.dev/eval-runs/.gitkeep`** — Empty file so the artifact directory exists in fresh checkouts (won't trigger eval-runs gitignore patterns).
6. **`tests/cli/test_eval/test_wiring.py`** — Click CliRunner-based tests:
   - `superclaude --help` lists `eval` as a subcommand
   - `superclaude eval --help` lists `doctor`, `list`, `describe`, `run`
   - `superclaude eval doctor` exits 0 (or 2 with clear message if claude binary missing)

### Acceptance criteria

- **AC-P4.1:** `uv run superclaude --help` includes `eval` in the subcommand list.
- **AC-P4.2:** `uv run superclaude eval --help` shows all 4 subcommands (`doctor`, `list`, `describe`, `run`).
- **AC-P4.3:** `uv run superclaude eval doctor` runs to completion (exit 0 on a healthy dev machine).
- **AC-P4.4:** `make eval-real` resolves to `uv run superclaude eval run --suite real` and prints the eval banner.
- **AC-P4.5:** `.gitignore` correctly excludes `.dev/eval-runs/**/home/` AND `**/stdout.log` AND `**/stderr.log` — verified by creating a sample artifact and confirming `git status` doesn't show it.
- **AC-P4.6:** `.dev/eval-runs/.gitkeep` is tracked; `.dev/eval-runs/some-run-id/home/whatever` is NOT tracked.
- **AC-P4.7:** `make verify-sync` EXIT=0 (no regression from wiring changes).
- **AC-P4.8:** `uv run pytest tests/ -v` — full suite — produces no NEW failures vs. pre-P4 baseline.
- **AC-P4.9:** `uv run pytest tests/cli/test_eval/test_wiring.py -v` — all PASS.

### Out of scope for THIS task

- Building any harness component (all done in P1-P3)
- CI integration (deferred per maintainer)
- macOS / Windows support
- The 15 real eval bodies (Wave 2 task files)

## Naming convention

- Task file path: `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/TASK-RF-20260518-cliEval-P4-wire-and-ship.md`
- Branch: `feat/cliEval-P4-wire-and-ship`
- PR title: `feat(eval): cliEval P4 — wire eval_group into main.py + Makefile target + .gitignore`

## Open questions for the executor

- Q1: Where exactly in the `cli/main.py:369-391` `add_command` block does `eval_group` belong? Alphabetical (between `design_group` and `git_group`? Or by feature category? Recommendation: alphabetical for diff cleanliness.
- Q2: Should `make eval-real` accept pass-through args? E.g., `make eval-real ARGS="--eval E1"`. Recommendation: yes, simple Makefile pass-through (`$(ARGS)`).
- Q3: Should `.gitignore` use `**/home/` glob or more specific `evals/*/home/`? Both work; the more specific pattern is safer.

## Dependencies

- **Depends on:** P1 AND P2 AND P3 — all must be merged to master before P4 can be built.
- **Blocks:** Wave 2 (E1-E15) — the eval bodies depend on `superclaude eval run --suite real` being end-to-end invocable.

## Estimated LOC: ~50 (the smallest phase)

(Per design-spec §17: main.py 2 lines, Makefile ~5 lines, .gitignore ~3 lines, test_wiring.py ~40 lines.)
