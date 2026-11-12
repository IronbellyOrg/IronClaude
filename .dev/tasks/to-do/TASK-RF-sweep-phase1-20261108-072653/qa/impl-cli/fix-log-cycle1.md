# Fix log, cycle 1 (item 9.14)

Fix agent for F_0 = {CLI-F1, CLI-F2}. fix_authorization: true. MINOR findings CLI-F3 to CLI-F37 left alone.
Consolidated findings: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/impl-cli/consolidated-findings-cycle0.md`

## Files edited

- `src/superclaude/cli/sweep/classify.py` (CLI-F1)
- `src/superclaude/cli/sweep/probes.py` (CLI-F2)

## CLI-F1 (MAJOR): status FIXED

- Change: in `classify_all`, the summary key `total_is_lower_bound` is now the constant `True`, with a `shortcut:` comment saying why and when to make it conditional again. The unused local `unscanned` (`unscanned = any(s.unscanned is not None for s in inp.sources)`) was deleted with it. The report wording was not touched; `report.py:178` and `report.py:510` still print the lower-bound lines unconditionally, so the JSON and the report now agree in every run.
- After the change: `src/superclaude/cli/sweep/classify.py:976` (`"total_is_lower_bound": True,`; comment at :973-975).
- Note for the coordinator (not a code change): DESIGN 7.4 (`docs/designs/orchestrator-mode.md:346`) still reads "true when any list is truncated or unscanned". The flag is now true in every Phase 1 run, so that row needs a wording change (or a remote-hosts scan) in a later design pass. I did not edit DESIGN.
- Scratch proof: a fake Orca script chosen through `ORCA_CLI_COMMAND`, a throwaway `git init` root and `HOME` pointed at the scratch folder, all under `/tmp/f2-scratch.<random>` (deleted afterwards; `ls` confirmed it is gone). Command: `superclaude sweep run --run run_aaaaaaaaaaaa --root <scratch root>`, exit 0 in all five modes. With well-formed empty lists (the case that used to give `false`) the JSON showed `orca_available True | lower_bound True | total 0`. It showed `lower_bound True` in the four failure modes below as well.

## CLI-F2 (MAJOR): status FIXED

- Change: in `probes.py`, added the module constant `_LIST_KEY`, mapping `("orchestration","worker-list")` to `"workers"`, `("orchestration","task-list")` to `"tasks"` and `("worktree","ps")` to `"worktrees"`. In `_call`, right after `_orca(...)` returns, an `ok` result for one of those three verbs whose `result[key]` is not a list is replaced with `OrcaResult("call_failed", None, "orca call failed (invalid response)")`. The existing first-call rule (a first call that is `call_failed` becomes `unavailable`), `record()` and the origin-unknown logic then apply unchanged. The key names and the empty-list form come from the captured shapes (`artifacts/sweep-live-check-1.4-workers.json`: `result.workers`; `artifacts/readonly-probe-raw/a-tl-all.json`: `result.tasks: []`; `artifacts/readonly-probe.md:791`: `result.worktrees[]`).
- After the change: `src/superclaude/cli/sweep/probes.py:316-321` (`_LIST_KEY`) and `:332-339` (the check in `_call`).
- Scratch proof (same scratch setup as CLI-F1; the fake Orca switched by an environment variable):

| Fake reply | Result |
|---|---|
| good shape, all lists empty | exit 0; `orca_available True`; all four Orca sources `read` (an empty list is still accepted) |
| `{"ok":true,"result":{}}` for every verb (the F1 case) | exit 0; `orca_available False`; `worker-list` `unscanned: orca call failed (invalid response)`; the other three `unscanned: orca unavailable` (first-call rule) |
| `worker-list` with `"workers":"nope"` | same as the row above |
| `task-list` without `tasks` (a later call) | exit 0; `orca_available True`; both `task-list` sources `unscanned: orca call failed (invalid response)`; `worker-list` and `worktree ps` `read` |
| `worktree ps` without `worktrees` (a later call) | exit 0; `orca_available True`; `worktree ps` `unscanned: orca call failed (invalid response)`; the others `read` |

No live Orca command was run and no test file was added; the per-verb tests belong to Phase 10.

## Re-check commands (required order, run after the edits)

| # | Command | Exit | Last lines | Result |
|---|---|---|---|---|
| 1 | `uv run ruff check src/superclaude/cli tests/sweep` | 0 | `All checks passed!` | PASS |
| 2 | `uv run ruff format --check src/superclaude/cli/sweep src/superclaude/cli/main.py tests/sweep` | 0 | `11 files already formatted` (no `ruff format` run was needed) | PASS |
| 3 | `uv run superclaude sweep --help` | 0 | `Commands:` / `run  Collect, classify and publish one read-only report; print one JSON...` | PASS |
| 4 | `uv run pytest tests/sweep tests/unit -v` | 0 | `726 passed, 2 skipped in 282.43s (0:04:42)` | PASS |

## Live re-run by the executor (item 9.14 rule: a fix touched a probe and a rule)

Written by the executor, not the fix agent. The read-only live check was re-run against Run `run_a4723d345399` after the edits: exit 0, stderr empty, 5.0 s, 182 rows all `could not determine`, 0 `unscanned` sources, `total_is_lower_bound` true, `orca_available` true (PASS). Record: `artifacts/sweep-live-check-1.4-rerun-9.14.md` and `.json`. The protected-file hash check (74 files: QA reports, artifacts, tests, DESIGN, SPEC, task file, `.gitignore`) showed no change after the fix agent returned.

## Files not touched

I did not edit `docs/designs/orchestrator-mode.md`, the SPEC (`merged-requirements.md`), the task file, anything under `tests/`, `.gitignore`, `src/superclaude/cli/main.py`, `commands.py`, `report.py`, `models.py`, `__init__.py`, any QA report, the consolidated findings file, the cycle ledger, or anything under `artifacts/` or `phase-outputs/`. Nothing was staged or committed. The MINOR findings CLI-F3 to CLI-F37 were left as notes.
