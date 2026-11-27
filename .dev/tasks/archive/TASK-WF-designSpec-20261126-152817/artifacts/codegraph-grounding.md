# Codegraph grounding: TASK-WF-designSpec-20261126-152817

This package is the rebuild (route `regenerate`) of the package `TASK-WF-designSpec-20261126-144507`, in the same run. The readiness check ran once for the run and is not repeated; the record below is carried over from the first package's `## Run state`, and the symbol facts were re-read this time directly from the files.

## Run state

- index_state: fresh
- checked_at: 2026-11-26T14:45:48Z (same run, carried over)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611
- access: mcp (lookup tools listed)
- graph tokens: none

## Resolved symbols

Each row was confirmed by reading the file range. All paths are under `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` unless stated.

| Symbol | Where (read) | What the plan uses |
|---|---|---|
| `JevClient.ask` | `client.py:78`; returns a `Result` and never raises for budget or model problems: `refused`/`budget_exhausted` at lines 114 to 117, `refused`/`dry_run` at lines 127 to 131 | Runner stops on those results instead of catching exceptions (review findings M-3, M-4) |
| `KeyMissing`, `KeyRejected` | `client.py:21`, `:25`; raised at lines 135 and 190 | The only stop signals that are exceptions |
| `Result` | `client.py:30`; `model` is `None` for every non-`ok` result (`client.py:86`, `:174`) | The model-pin check applies to `ok` results only |
| `Budget.reserve_phase`, `release_phase`, `draw`, `settle`, `state` | `budget.py:63`, `:98`, `:72`, `:85`, `:102`; `draw` consumes the reservation of its own phase; `_committed` counts undrawn reservations (`budget.py:52` to `55`) | Whole-run reservation under phase `issue611-<run-id>`, released in a `finally` |
| `Budget` price use | `budget.py:8` copies `PRICE_USD_PER_MTOK_INPUT` at import; `_fits` checks both the token and the dollar ceiling (`budget.py:57` to `60`) | A confirmed price is fed in through `ceiling_input_tokens` |
| config constants | `config.py:9` `KEY_ENV`, `:10` price, `:14` `RESERVE_BYTES_PER_TOKEN`, `:15` `ATTEMPT_TIMEOUT_S`, `:17` `MAX_RETRIES`, `:34` `api_url` | `spend.py` and the runner read these; the runner overrides two in process only |
| `validate_response` | `validate.py:23`; `model_mismatch` at lines 32 and 33; the choice must be the argmax (`validate.py:80`); output answers `{"type": "noul", "p"}` and `{"type": "choice", "choice", "probs", "confidence"}` (`validate.py:98` to `102`) | `jev_answer` input shape |
| `privacy_violation` | `manifest.py:27`; reads `os.environ` for `JEV_API_KEY` directly at line 35 | Gates never call the corpus loader; the env-read test uses a recorder |
| `build_request`, `noul`, `choice`, `canonical_bytes`, `request_sha256` | `questions.py:53`, `:17`, `:21`, `:98`, `:108` | `questions.py` of the experiment and `spend.py` |
| `MockTransport`, `MockStep`, `fake_answer`, `UrllibTransport`, `TransportTimeout`, `TransportError` | `transport.py:50`, `:43`, `:85`, `:23`, `:15`, `:19` | Runner tests and the timing wrapper |
| `Journal` | `journal.py:12` | Per-run journal |
| `keyscan.py` | `.dev/research/346-review-loop-experiments/p15/jev/keyscan.py`: `keyscan.py [--fake VALUE] [--exclude PATH ...] [paths...]` | Tests and README use explicit paths |
| Wave 0 table | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:153` to `158` (cue rows), `:159` (ambiguity rule) | Task 7 quotes these lines |

## Dependents

- `Budget.reserve_phase` and `release_phase` already have callers outside `budget.py`: `p15/jev/probe.py`, `p15/e1`, `p15/e3`, `p18/seams`, `p19/ab6` and the tests `p15/jev/tests/test_budget.py`. The plan adds new callers only and edits none of them.
- `JevClient` has 31 importers by import (earlier `codegraph_callers`, 10 shown of 31, `graph:truncated`); all stay unchanged because the plan imports `jevlib` and edits nothing in it.
- The runner changes two module attributes of `jevlib.config` (`MAX_RETRIES`, `ATTEMPT_TIMEOUT_S`) in its own process through `limits(rule)`, which restores them in a `finally`; Task 6 tests that.
- No file under `src/`, `tests/` or `.claude/` is touched. A caller row gives a file, not a call site; none is cited as "calls X".

## Pre-check

Run after the Wave 3 gate passed, read-only, no new readiness check (2026-11-26).

- Files named by the tasks exist: the eight `jevlib` modules read, `keyscan.py`, `p15/jev/tests/conftest.py`, `SHARED-CONTRACT.md`, the ops guide, `deviation-patterns-issue-610.md` and `SKILL.md`. Result: 14 of 14 found (shell check).
- Symbols named by the tasks resolve by Read: `JevClient`, `KeyMissing`, `KeyRejected`, `Budget`, `BudgetExhausted`, `reserve_phase`, `release_phase`, `RESERVE_BYTES_PER_TOKEN`, `canonical_bytes`, `privacy_violation`, `MockTransport`, `MockStep`, `fake_answer`, `Journal`, `UrllibTransport`, `TransportTimeout`, `TransportError` (all found).
- The experiment folder `.dev/research/jev-vs-keyword-table-611/` does not exist yet; Task 1 creates it. The new modules `spend.py`, `events.py`, `gate.py`, `scorer.py` and `runner.py` are created by the tasks, so they are not looked up.
- Dependents of touched symbols not named by any task: none. No existing symbol is edited.
- Count: 0 unresolved names, 0 unnamed dependents.
