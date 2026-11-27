# Codegraph grounding: TASK-WF-designSpec-20261126-144507

## Run state

- index_state: fresh
- checked_at: 2026-11-26T14:45:48Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611
- access: mcp (lookup tools listed)
- status answer: 4161 files indexed, changes since index 0 added, 0 modified, 0 removed
- graph tokens: none

## Resolved symbols

Rows are leads; each was confirmed by reading the file range before a task names it. All paths are under `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` unless stated.

| Symbol | Where (read) | What the plan uses |
|---|---|---|
| `JevClient` (class) | `client.py:49`; `ask(state, questions, *, case_id, qset_version, data_classes, purpose, run=None, step=None) -> Result` at line 78; `__init__(*, experiment, phase, budget, journal, transport=None, live=False, cache=None, allowed_classes, clock, sleep)` at line 50 | Runner calls `ask` once per attempt with `data_classes=["public"]`; `clock` and `sleep` are injectable for latency tests |
| `Result` (dataclass) | `client.py:30`: `status` (`ok`, `invalid`, `unavailable`, `refused`), `error`, `answers`, `usage`, `model`, `attempts`, `latency_ms`, `logical_call_id`, `request_sha256` | Row builder maps `status` and `error` to the experiment's row status |
| `KeyMissing`, `KeyRejected` | `client.py:21`, `client.py:25` | Raised, not returned; the runner maps them to `RUN_INVALID` |
| `Budget`, `BudgetExhausted` | `budget.py:19`, `budget.py:11`; `Budget(path, *, ceiling_usd, ceiling_input_tokens)`; `reserve_phase`, `draw`, `settle`, `state()` | One cumulative ledger at `ledger/spend.json` with `ceiling_usd=1.0` |
| `Journal` | `journal.py`; `Journal(path).write(record)` | Per-run `journal.jsonl`; headers never written; key redacted |
| `validate_response`, `Invalid` | `validate.py:23`; model must equal `jev-1.14.0`, noul value in 0 to 1, choice probabilities sum within 0.02 | Failure code `model_mismatch` is systemic |
| `build_request`, `noul`, `choice`, `request_sha256`, `canonical_bytes` | `questions.py:53`, `:17`, `:21`, `:108`, `:98`; choice option names must not be positional (`a`, `b`, `option1`) | `questions.py` of the experiment builds one Choice over `bug`, `build`, `performance`, `deployment`, `security`, `test` plus one Noul |
| `privacy_violation(req, data_classes, allowed)` | `manifest.py:27`; refuses email, `/home/`, `/root/`, `/tmp/claude`, `IronbellyOrg`, `SuperClaude-Org`, `github.com/`, private-key header, token shapes, the key | Offline corpus screen at freeze |
| `MockTransport`, `MockStep`, `fake_answer` | `transport.py:50`, `:43`, `:85`; `MockStep(status, body, headers, exc)`; `MockTransport(script, delay, sleep)` records `calls` without the Authorization header; `fake_answer(req, rng_seed, p)` returns a valid body | All runner tests; `p` sets the Noul probability |
| `UrllibTransport`, `TransportTimeout`, `TransportError` | `transport.py:23`, `:15`, `:19` | Runner wraps `UrllibTransport` to time each post; tests wrap `MockTransport` |
| config constants | `config.py`: `MODEL`, `KEY_ENV='JEV_API_KEY'`, `ATTEMPT_TIMEOUT_S=20.0`, `MAX_RETRIES=1`, `PRICE_USD_PER_MTOK_INPUT=0.042`, `ALLOWED_DATA_CLASSES` includes `public` | Runner overrides `MAX_RETRIES=0` and `ATTEMPT_TIMEOUT_S=10.0` in process only |
| `keyscan.py` | `.dev/research/346-review-loop-experiments/p15/jev/keyscan.py`: `keyscan.py [--fake VALUE] [--exclude PATH ...] [paths...]`; prints `KEYSCAN OK files=<n>` or `KEYSCAN FAIL`; its default paths point at a different machine's scratch folder | Tests pass explicit paths and `--fake`; the README gives the coordinator the explicit-path form |

## Dependents

- `JevClient` has 31 callers by import (`codegraph_callers`, 10 shown of 31, `graph:truncated`): experiments `p15/e1`, `p15/e3`, `p15/jev/probe.py` and the `p15/jev/tests/` files, plus later experiment folders found by Grep (`p18`, `p19`, `p21`). All stay unchanged: this plan imports `jevlib` and edits nothing in it.
- The runner changes two module attributes of `jevlib.config` (`MAX_RETRIES`, `ATTEMPT_TIMEOUT_S`) inside its own process. Any test that does so must restore them (monkeypatch) so other tests in the same process keep the library's own values.
- No file under `src/`, `tests/` or `.claude/` is touched.
- A caller row gives the caller's file, not a call site; none is cited as "calls X".

## Pre-check

Run after the Wave 3 gate passed, read-only, no new readiness check (2026-11-26).

- Files named by the tasks exist: the `jevlib` modules, `keyscan.py`, `p15/jev/tests/conftest.py`, `SHARED-CONTRACT.md`, the ops guide, `deviation-patterns-issue-610.md`, `SKILL.md`, `troubleshoot.md`. Result: all found.
- Symbols named by the tasks resolve by Grep and Read: `KeyMissing`, `KeyRejected`, `Budget`, `BudgetExhausted`, `Journal`, `privacy_violation`, `MockTransport`, `fake_answer`, and the config constants (4 of 4 searched names found in `config.py`). `JevClient`, `privacy_violation`, `MockTransport` and `Budget` were also located with `codegraph_search`.
- The experiment folder `.dev/research/jev-vs-keyword-table-611/` does not exist yet; Task 1 creates it.
- Dependents of touched symbols not named by any task: none. No existing symbol is edited. The only shared state touched is two `jevlib.config` attributes inside the runner's own process, which Task 6 restores in tests.
- Count: 0 unresolved names, 0 unnamed dependents.
