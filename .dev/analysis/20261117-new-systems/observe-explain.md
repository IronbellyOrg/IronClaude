# Explanation: the Orca observer (`superclaude observe`), advanced level

Source: origin/master, `src/superclaude/cli/observe/` (read with `git show`; the local checkout is an old branch). Codegraph not used (graph:stale).

## One-sentence model

A read-only terminal screen that polls two Orca CLI reads (`worker-list` and, for one named Run, `check --all --types question`), merges the replies into an immutable per-cycle result, and renders it as a ledger that says "UNKNOWN" instead of guessing.

## Layers (strictly one direction)

1. `sanitize.py` strips every escape form and control/format character from untrusted text (`sanitize.py:15-48`).
2. `adapter.py` is the only module that runs Orca. It holds three argv templates (worker-list, discovery probe, one question read), a forbidden-prefix set, run-id and cursor checks, and a runner that kills the whole process group on timeout or on output over 8 MiB (`adapter.py:29-57`, `:224-312`). `LiveSource.read_pages` pages `worker-list` under a 5-call cap and a time budget; `read_questions` makes one call (`adapter.py:395-512`).
3. `parse.py` is strict on envelopes (raises `ShapeError`) and lenient inside rows. Only 30 verified worker-list keys are read (`parse.py:58-90`); every missing value is the `UNKNOWN` sentinel, never None/0/"" (`parse.py:25-43`). `merge` dedupes within a cycle, picks across cycles, and keeps rows not re-seen with `reobserved=False` (`parse.py:588-678`). `parse_questions` drops rows of the wrong type or wrong Run, never keeps body, payload or recipient (`parse.py:415-541`).
4. `questions.py` is a pure retention store keyed (Run, message id), bounded at 1,000 records; a question that leaves Orca's 100-row window stays, marked "no longer in source window"; eviction makes the total read "unknown (retention exceeded)" (`questions.py:21-137`).
5. `collector.py` runs one single-flight cycle every 15 s with a 15 s budget and doubling backoff to 60 s, and publishes one frozen `CycleResult` by swapping a reference under a lock (`collector.py:28-34`, `:246-330`). The question read is a separate step in the same budget; its failure changes nothing about the worker snapshot (`collector.py:288-291`).
6. `view.py` is the pure `build_view(result, session, clock)`; STALE is derived from the monotonic clock at 45 s, never stored (`view.py:32-34`, `:352-359`, `:762`). It owns every status literal.
7. `render.py` + `terminal.py` lay out at 160/116/80 columns, ASCII and NO_COLOR modes. `export.py` makes the text record and a versioned JSON snapshot (schemaVersion 1, atomic 0600 write) from the same View (`export.py:173-264`). `keys.py` is a POSIX cbreak key reader that restores the terminal on exit and signals.
8. `commands.py` is the click group, registered in `main.py:580-582`. `--once` prints a record; interactive mode runs `run_loop` with `Live(screen=True)`.

## The safety design

- No key and no option builds an argv. The forbidden set (`check`, `--ack`, `--wait`, `--peek`, `send`, `reply`, `run-use`, ...) is matched at every verb and flag position (`adapter.py:34-50`, `:135-170`). The one allowed `check` is the exact 8-token question template, whose verb is exempted (`adapter.py:121-132`).
- `--questions` is refused before any Orca call, discovery included, unless `--run` is given, no `--fixture`, a valid run id, and the gate constant `QUESTION_GATE_PASSED` is True (`commands.py:63-67`, `:173-187`).
- Process group kill, reaping, `cancel_active` on quit (`adapter.py:196-221`).
- Fixture mode is labelled "SYNTHETIC FIXTURE ..., not Orca data" (`view.py:777-781`).

## What the question read cannot do (stated limits)

- `--run` is a fence, not a filter: a terminal not bound to the Run gets `consumer_fenced` (mapped to a source code, `adapter.py:66-69`). The observer never runs `run-use`.
- Orca returns at most 100 rows and no total, so a read of exactly 100 is flagged "window full" (`questions.py:22`, `:140-142`).
- Rows carry no read marker: a handled question still shows as open (`questions.py:9-12`).

## Timeline

- PR #503 (2026-11-11): release 1, worker ledger. PR #514 (2026-11-12): release 2 code, questions with the live read switched off. PR #577 (2026-11-16): set `QUESTION_GATE_PASSED = True`, applied 11 debated cuts, recorded the owner's DIRECTION-SELECTED record. PR #586 (2026-11-17): documentation of the live test and a synthetic load test in `release-gates.md`.

## Gotchas

- The flag constant means "the owner's record exists", not "the read is proven for real traffic"; real message rate is unmeasured.
- Both Orca reads are decoded with `json.loads` on up to 8 MiB; deep nesting is rejected via `RecursionError` handling (`adapter.py:437-444`).
- Two spec items remain owner questions after the cuts (S1 snapshot `questions` group, S5 snapshot default), so some behaviour is deliberately left as is.
