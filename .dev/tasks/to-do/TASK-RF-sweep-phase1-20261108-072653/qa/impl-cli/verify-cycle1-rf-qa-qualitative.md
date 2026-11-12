# QA Report - Cycle 1 Verification (rf-qa-qualitative)

**Topic:** impl-cli cycle-1 re-verification of CLI-F1 and CLI-F2
**Date:** 2026-11-12
**Phase:** fix-cycle
**Fix cycle:** 1
**fix_authorization:** false

Method: read the consolidated findings, the fix log, the cycle ledger, the eight cycle-0 QA reports (for the check descriptions), the six `sweep/*.py` files (the changed passages in full, `_ledger` and the `_orca_reads` loop around them), the `main.py` diff, the help record, `phase9-validation.md`, the five live-check artifacts, DESIGN 3, 5, 7.1 and 7.4, SPEC section 8 (lines 287 and 436-441) and the OQ-2/OQ-5 records. Then ran, in private `/tmp` folders (deleted afterwards, `cleanup ok` printed each time): 23 scratch runs of the real `superclaude sweep run` against a fake Orca script chosen through `ORCA_CLI_COMMAND` (7 modes: 1 well-formed, 6 wrong-shape; then 13 scenarios replaying the repository's own captured fixtures `tests/sweep/fixtures/captured-*.json`; then 3 two-Run and exit-1 scenarios), an allowlist probe, `uv run pytest tests/sweep -q`, `uv run ruff check src/superclaude/cli tests/sweep` and `uv run ruff format --check` on the three paths. No live Orca command was run; `superclaude sweep run` never touched the real Orca; `tests/unit` was not run.

Edit footprint check: file times show `classify.py` (03:36:57) and `probes.py` (03:37:25) are the only sweep files newer than the cycle-0 QA reports (03:23 to 03:30). `commands.py` (03:09:43), `report.py` (02:42), `models.py` (02:41), `__init__.py` (01:14), the tests (latest 02:20), DESIGN, SPEC, the OQ records and the first live-check artifacts (03:11 to 03:13) are older. The `main.py` diff is still the same 4 inserted lines.

## Overall Verdict: PASS

Both F_0 findings are RESOLVED, none of the 147 cycle-0 PASS ids now fails, and I found no new BLOCKING or MAJOR finding. Seven MINOR notes are listed below; they never fail the review and are not rechecked later.

## Finding status (F_0)

### CLI-F1 (MAJOR): RESOLVED

- `classify.py:967-977` builds `summary` with `"total_is_lower_bound": True` (comment at `:973-975`). The local `unscanned` is gone and nothing else used it (`ruff check` passes, so no dangling name).
- The report side is unchanged and unconditional: `report.py:178` (`(lower bound: remote hosts not scanned)` in the Scope line) and `report.py:510` (`Remote hosts were not scanned; the session count is a lower bound` in `## What I could not determine`). `report.py:670` copies the flag to the JSON. JSON and report now say the same thing in every run.
- Observed: every scratch run that produced JSON printed `total_is_lower_bound True`, including the well-formed empty read (the case that used to print `False`). The executor's live re-run JSON `artifacts/sweep-live-check-1.4-rerun-9.14.json` has `summary.total_is_lower_bound` true (182 rows); the first record `sweep-live-check-1.4.json` still has false (180 rows), which is the pre-fix evidence kept for the verifiers.
- Not touched by the fix and still pending: DESIGN 7.4 (`docs/designs/orchestrator-mode.md:346`) still defines the flag as "true when any list is truncated ... or unscanned" (see N1).

### CLI-F2 (MAJOR): RESOLVED

- `probes.py:316-321` adds `_LIST_KEY` (`worker-list` to `workers`, `task-list` to `tasks`, `worktree ps` to `worktrees`); `probes.py:332-339` in `_call` replaces an `ok` result whose list key is not a list with `OrcaResult("call_failed", None, "orca call failed (invalid response)")`, before the existing budget-cut and first-call (`:346-348`) rules. That is the reason text and class SPEC section 8 requires (SPEC `merged-requirements.md:287` and failure table line 439).
- Observed with the fake Orca, `--run run_aaaaaaaaaaaa`:
  - `{"ok":true,"result":{}}` for every verb: exit 0, stderr empty, `orca_available False`, `worker-list` `unscanned: orca call failed (invalid response)`, the other three `unscanned: orca unavailable` (first-call rule).
  - `workers` a string, or null: same as above.
  - `tasks` missing or a dict: exit 0, `orca_available True`, both `task-list` rows `unscanned: orca call failed (invalid response)`, `worker-list` and `worktree ps` `read`.
  - `worktrees` missing: `orca worktree ps` `unscanned: orca call failed (invalid response)`, the rest `read`.
  - Two Runs, first good and empty, second wrong-shape (B2): the second Run's three rows are `unscanned: orca call failed (invalid response)`, the first Run and `worktree ps` are `read`, `orca_available True`, exit 0. Later wrong-shape replies do not flip availability.
- No regression on well-formed replies: the repository's own captured fixtures (`captured-worker-list.json`, `-task-list-ready.json` with `tasks: []`, `-task-list.json`, `-worktree-ps.json`, `-worker-list-unknown-run.json` with `workers: []`) all pass the new check. The fixture run with `--run run_a4723d345399` gave 9 Orca source rows, all `read`, and 5 rows; the unknown-Run shape (A2, B1) still gives `worker-list` `read` and both `task-list` rows `unscanned: orca call failed (exit 1)`, exit 0, and the second Run in B1 is still read.
- The executor's live re-run (`sweep-live-check-1.4-rerun-9.14.json`): `orca_available` true, 71 source rows, 0 with coverage `unscanned` or an `unscanned` reason, the same five `orca:ctx_...` rows, so the real Orca replies pass the new check.

## New findings

No new BLOCKING or MAJOR finding. Cycle-1 `Blocking count` is 0.

## Passage read-through (as the intended reader)

- `classify.py:973-976` comment, read as a maintainer: it says the flag is always true in Phase 1, names the two report places that print the same fact (by section name, so it survives line moves), and says when to make it conditional (when remote hosts are scanned). It does not mislead. Read as an operator of the JSON: the flag is a bare boolean, so the reason is only in the comment, the report header and the fix log; the report header explains it. Not misleading; see N1 and N2 for the two things the passage cannot fix.
- `probes.py:316` comment and `:338` comment, read as a maintainer: they say which key must hold a list and that the rule is SPEC section 8. "steps 1.0a and 1.4" are plan step names, as elsewhere in the module (`probes.py:43`, `:73`). The meaning of an invalid response is clear from the SPEC cite and the reason string. Gap: the `_call` docstring (`:325`) still describes only the budget-cut rule (N3).
- Operator reading the new reason: a first-call wrong-shape reply prints `orca call failed (invalid response)` on `worker-list` and `orca unavailable` on the other rows, plus "Orca was unavailable; Orca sources were not read" (`report.py:504-505`). The first row carries the true cause, so the operator can tell a bad reply from an Orca outage. This is the SPEC-pinned first-call rule, not a defect.
- Fix log `## Live re-run by the executor` section: it is labelled as written by the executor, not the fix agent, and its numbers match the saved JSON (182 rows, all `could not determine`, 0 unscanned, flag true, `orca_available` true). The exit code, empty stderr, 5.0 s and the "74 files" hash check are prose only; I cannot re-derive them (N6). It does not mislead.

## Minor notes (not blocking; not rechecked in later rounds)

| # | Severity | Location | Note | Suggested fix |
|---|---|---|---|---|
| N1 | MINOR | `docs/designs/orchestrator-mode.md:346` (DESIGN 7.4 / section 6 table) | The row still says the flag "is true when any list is truncated (a full 100-row page) or unscanned". True as a sufficient condition, but a reader infers it can be false, and in Phase 1 it never is. The fix log already hands this to the coordinator (fix log line 15). | One design pass: "true in every Phase 1 run (remote hosts are never scanned); also true when a list is truncated or unscanned". |
| N2 | MINOR | `classify.py:976`, `report.py:664-671` | The JSON no longer carries any "a worker list filled its page" or "a source was unscanned" signal through this flag; those are only in the report text (`report.py:506-509`, Source coverage) and in `sources[].unscanned`. A consumer that read only the flag lost nothing it could rely on (the flag was false in the live run), but it now cannot tell the standing remote-host bound from a truncated list. | None for Phase 1; keep `sources` and `bound_reached` as the discriminators and say so in DESIGN 7.4. |
| N3 | MINOR | `probes.py:324-325` (`_call` docstring), `:244` (`_orca` docstring "classify the result once") | The list-shape rule lives in `_call`, not `_orca`, and neither docstring says so. A Phase 10 test that calls `_orca` directly with `{"ok":true,"result":{}}` still gets `ok`. Behaviour through `collect` is correct. | Add one clause to the `_call` docstring; write the per-verb tests through `_call` or `collect`. |
| N4 | MINOR | `fix-log-cycle1.md:20` | Cites `artifacts/readonly-probe-raw/a-tl-all.json` for `result.tasks: []`. `a-tl-all.json` holds 5 tasks; the empty list is in `a-tl-ready.json`. The key name is right. | Change the file name in the log. |
| N5 | MINOR | cycle-0 reports citing `probes.py` lines after 316 | The edit added 16 lines, so those citations moved by +16 (for example `open(path, "rb")` 559/810/874 now 575/826/890; the `_ledger` missing-file branch 578-582 now 594-599). Every claim stays true. | None. |
| N6 | MINOR | `fix-log-cycle1.md:45`, `sweep-live-check-1.4-rerun-9.14.md:5` | Exit 0, empty stderr, 5.0 s and the 74-file hash check have no saved file (same class as CLI-F19). | For the Phase 2 live plan, save stderr and timing next to the JSON. |
| N7 | MINOR | `tests/sweep` (4 tests, files not newer than 02:20) | No test pins either fix yet; the consolidated finding schedules one test per verb for the Phase 10 tests. My 23 scratch runs are the only regression evidence at this gate. | Include the six wrong-shape modes above, the flag always true, and the fixtures-pass case in the Phase 10 command/probe tests. |

## Checks

Basis codes. U: the file the check is about (`commands.py`, `report.py`, `models.py`, `__init__.py`, `main.py` diff, tests, DESIGN, SPEC, OQ records) is older than the cycle-0 reports and the fix touched neither it nor anything on its path (`commands.py` calls only `Budget`, `bind_run`, `collect`, `RUN_ID_RE`, `BindingError`; `run-current` is not in `_LIST_KEY`). R: re-observed now by a scratch run (A1-A13 = fixture replays, B1-B3 = two-Run and exit-1 runs, M-x = wrong-shape mode x). A: the check is about a saved first-record artifact; its file time (03:11 to 03:13) and size are unchanged, and the post-fix re-run record agrees. G: grep or probe re-run now. Checks that rested on cycle-0 scratch runs that cannot be re-run (P1-P14, B1-B23, S1-S3 and similar) are marked U with the reason: the code they exercised is in an unchanged file.

| Check id | Result | Basis |
|---|---|---|
| qa-failure-path-report:C1 | PASS | R: A8, A9, A10, A11 exit 2 with the reason in the message; the exit-2 runs (A7-A11, A13) left no report (`.dev/sweeps/` held 7 files, one per exit-0 run A1-A6 and A12) |
| qa-failure-path-report:C2 | PASS | R: A13 run-current hang, exit 2 `Orca unavailable (timeout after 10 s)` |
| qa-failure-path-report:C3 | PASS | R: A7 exit 2 `no Run bound: pass --run <id>` |
| qa-failure-path-report:C4 | PASS | R: A4, A5, A12 `--run` with failing or non-JSON first reply: exit 0, reason in Source coverage, stderr empty, `orca_available False` |
| qa-failure-path-report:C5 | PASS | R: A3, B1, M-tasks_missing: later failure is `call_failed`, `orca_available True`, exit 0 |
| qa-failure-path-report:C6 | PASS | R: M-good, `workers: []` read, total 0, exit 0 (an empty list is still accepted by the new check) |
| qa-failure-path-report:C8 | PASS | U: `commands.py` `_find_root`/`_check_root` unchanged |
| qa-failure-path-report:C9 | PASS | R: A7-A11 and A13 exit 2, no file written; U for the option-error cases |
| qa-failure-path-report:C10 | PASS | R: B3 (`.dev/sweeps` is a regular file) exit 1, stdout 0 bytes, `[sweep publish] [Errno 17] File exists: ...`; U for the rest |
| qa-failure-path-report:C11 | PASS | U: `_publish`/`_write_all` in unchanged `commands.py` (P4-P7b not re-runnable) |
| qa-failure-path-report:C12 | PASS | U: name-space exhaustion path in unchanged `commands.py` |
| qa-failure-path-report:C13 | PASS | U: temp-exists branch (`commands.py:171-172`) unchanged |
| qa-failure-path-report:C14 | PASS | U: post-commit unlink branch (`commands.py:202-207`) unchanged |
| qa-failure-path-report:C15 | PASS | U: escape check after `makedirs` (`commands.py:158-164`) unchanged |
| qa-failure-path-report:C16 | PASS | U: `[sweep output]` handler (`commands.py:286-288`) unchanged |
| qa-failure-path-report:C17 | PASS | U: exit-1-before-link behaviour is `commands.py`; R: B3 left no report name |
| qa-failure-path-report:C18 | PASS | U: `commands.py:175-196` unchanged |
| qa-failure-path-report:C20 | PASS | U: `commands.py:153-208`, `279-288` unchanged; G: `sys.exit` only at `commands.py:281`, `285`, `288` |
| qa-failure-path-report:C21 | PASS | G: `git diff -- src/superclaude/cli/main.py` is the same 4 inserted lines, same pattern as `issue-watch` |
| qa-failure-path-report:C22 | PASS | R: help blocks diff clean against `step-1.7-help.txt`; ruff check and format clean; `pytest tests/sweep` 4 passed; A: first-record JSON unchanged (180 rows, 71 sources, 0 unscanned, 5 workers, 9 Orca source rows); `tests/unit` not re-run (fix log reports 726 passed after the fix) |
| qa-failure-path-report:C23 | PASS | U: `commands.py:27`, `:99-107`, `:155`; G: `git check-ignore -v .dev/sweeps/x.md` gives `.gitignore:256:.dev/sweeps/` |
| qa-input-edge-report:C1 | PASS | U: `_check_run_ids` unchanged |
| qa-input-edge-report:C2 | PASS | U: same |
| qa-input-edge-report:C3 | PASS | U: same (first-seen order) |
| qa-input-edge-report:C4 | PASS | U: `RUN_ID_RE` at `probes.py:44` is above the edit and unchanged |
| qa-input-edge-report:C5 | PASS | U: order of calls in `run` unchanged |
| qa-input-edge-report:C6 | PASS | R: A2 and B1 unknown-Run shape: `worker-list` read, both `task-list` rows `unscanned: orca call failed (exit 1)`, exit 0, later good Run still read |
| qa-input-edge-report:C8 | PASS | R: A6, A7, A8, A9, A10, A11 match FR-002 tests 1 and 4 with the D3 wording |
| qa-input-edge-report:C9 | PASS | R: A4, A5, A12 explicit `--run` with first-call failure publishes and exits 0 |
| qa-input-edge-report:C10 | PASS | U: `_parse_window`; R: help shows `[default: 6h]` |
| qa-input-edge-report:C11 | PASS | U: `_find_root` unchanged, no `_git` call on the walk |
| qa-input-edge-report:C13 | PASS | U: `_check_root` unchanged |
| qa-input-edge-report:C15 | PASS | U: `_check_output` unchanged |
| qa-input-edge-report:C16 | PASS | U: same |
| qa-input-edge-report:C17 | PASS | U: overlap guard unchanged |
| qa-input-edge-report:C18 | PASS | U: `_publish` escape path unchanged |
| qa-input-edge-report:C20 | PASS | R: exit-2 runs A7-A11, A13 created no file or folder; U for option errors |
| qa-input-edge-report:C21 | PASS | U: stem format and `-2` suffix code unchanged (`commands.py:155`, `:182-196`) |
| qa-input-edge-report:C22 | PASS | G: `main.py` diff unchanged; R: both help outputs diff clean against `step-1.7-help.txt` |
| qa-input-edge-report:C23 | PASS | A: first-record JSON `window` 6h, `report_path` under `.dev/sweeps/`, run id from OQ-8; unchanged |
| qa-interface-exit-report:C1 | PASS | U: `commands.py` signatures unchanged (file time 03:09) |
| qa-interface-exit-report:C2 | PASS | R: import probe printed group `sweep`, commands `['run']` |
| qa-interface-exit-report:C3 | PASS | R: `sweep run --help` lists `--run`, `--window`, `--root`, `--output` |
| qa-interface-exit-report:C4 | PASS | R: help `[default: 6h]`, `--root`/`--output` defaults documented |
| qa-interface-exit-report:C5 | PASS | G: `DEFAULT_WINDOW = "6h"` at `commands.py:27` is the only window default in the package (grep for `6h`, `hours=6`, `DEFAULT_WINDOW`); none in `classify.py` or `probes.py` |
| qa-interface-exit-report:C6 | PASS | G: `.gitignore:256` still ignores `.dev/sweeps/`; U: stem code |
| qa-interface-exit-report:C7 | PASS | U: `_parse_window` unchanged |
| qa-interface-exit-report:C8 | PASS | U: `_check_root`, `_check_output` unchanged |
| qa-interface-exit-report:C9 | PASS | U: `_check_run_ids` unchanged |
| qa-interface-exit-report:C10 | PASS | U: usage-error path unchanged; R: A7-A11 stdout empty |
| qa-interface-exit-report:C11 | PASS | R: A7 `no Run bound: pass --run <id>`, A8-A11 `Orca unavailable (<reason>); no Run binding could be established: pass --run <id>`, stdout empty |
| qa-interface-exit-report:C12 | PASS | U: exit-1 stage handlers in unchanged `commands.py` |
| qa-interface-exit-report:C13 | PASS | U: same |
| qa-interface-exit-report:C14 | PASS | U: `_publish` failure messages unchanged |
| qa-interface-exit-report:C15 | PASS | G: `sys.exit` only at `commands.py:281`, `285`, `288` (grep over the package) |
| qa-interface-exit-report:C16 | PASS | R: A1, A6 exit 0, stdout one JSON object (12 keys), stderr empty; U: `-2` suffix code |
| qa-interface-exit-report:C17 | PASS | R: exit-2 runs wrote nothing; B3 exit 1 left no report name |
| qa-interface-exit-report:C18 | PASS | U: post-commit rule unchanged |
| qa-interface-exit-report:C19 | PASS | G: `main.py` diff 4 insertions, 0 deletions; R: registered commands 19, last two `issue-watch`, `sweep` |
| qa-interface-exit-report:C20 | PASS | R: group help and run help diff clean against `step-1.7-help.txt`; ruff check "All checks passed!", format "11 files already formatted" |
| qa-interface-exit-report:C21 | PASS | R: `pytest tests/sweep` 4 passed; `tests/unit` not re-run (out of scope, fix log reports 726 passed) |
| qa-interface-exit-report:C22 | PASS | A: first-record JSON has 12 top-level keys, `window` 6h, 71 sources, 0 unscanned, 180 rows; workers file unchanged; `probes.py:49` still holds the `worker-list` template |
| qa-live-check-report:C1 | PASS | A: first-record JSON and report (`.dev/sweeps/20261112-031239-sweep.md`) still present; re-run record adds exit 0 |
| qa-live-check-report:C2 | PASS | A: 71 sources, 0 unscanned, `bound_reached` 0, 9 Orca source rows (re-derived from the JSON now) |
| qa-live-check-report:C3 | PASS | A: 180 rows, all class `could not determine`; re-run JSON 182 rows all carry a class |
| qa-live-check-report:C4 | PASS | A: the five `orca:ctx_...` rows are `could not determine`, rule `fallback`, in both JSONs |
| qa-live-check-report:C5 | PASS | A: 0 unscanned in both JSONs (computed from `coverage` and `unscanned` fields) |
| qa-live-check-report:C6 | PASS | G: `probes.py:49` still holds the template; the new `("orchestration", "worker-list")` at `probes.py:318` is a dict key, not an argv, and `check_orca_argv` is unchanged |
| qa-live-check-report:C7 | PASS | A: `sweep-live-check-1.4-workers.json` unchanged (03:11:44), 5 workers |
| qa-live-check-report:C8 | PASS | A: the check rested on `stat` of live transcripts at cycle 0 and the saved `tail_complete` notes; the fix did not touch transcript code |
| qa-live-check-report:C9 | PASS | A: both JSONs carry the same evidence strings for the five rows |
| qa-live-check-report:C10 | PASS | A: premise rests on unchanged `a-tl-all.json` and `_contract_candidates`; no `contract` source row in either JSON |
| qa-live-check-report:C11 | PASS | A: report files 031151, 031209, 031239 still exist; `.dev/sweeps/` now holds a fourth file, `20261112-034511-sweep.md`, from the sanctioned executor re-run |
| qa-live-check-report:C12 | PASS | G: `.gitignore:256` matched by `git check-ignore -v` |
| qa-live-check-report:C13 | PASS | U: `commands.py:27`; R: help `[default: 6h]` |
| qa-live-check-report:C14 | PASS | U: `commands.py` unchanged against DESIGN 3.2, 5, 7.1 |
| qa-live-check-report:C15 | PASS | G: `main.py` diff unchanged; R: both help outputs run with exit 0 and diff clean |
| qa-live-check-report:C16 | PASS | R: ruff check, ruff format --check, `pytest tests/sweep` re-run clean; `tests/unit` part not re-run (fix log reports it passing after the fix) |
| qa-live-check-report:C17 | PASS | A: both JSONs list only allowlisted Orca names plus `git status` rows; G: allowlist probe rejected 7 of 7 hostile Orca argvs and 3 of 3 hostile git argvs; 10 templates, 7 verbs |
| qa-live-check-report:C18 | PASS | G: `_ledger` still returns `False, None` on `FileNotFoundError` (`probes.py:594-599`, line shifted +16); the two re-runs show 0 unscanned |
| qa-live-check-report:C19 | PASS | A: `sweep-live-check-1.4.json` is 319,791 bytes (`ls`), unchanged |
| qa-live-check-report:C20 | PASS | A: worktree `issue-504` in both JSONs: `uncommitted` true, `removable` no |
| qa-operator-output-report:C1 | PASS | R: A1, A6 and every exit-0 run: stdout one JSON object that `json.loads` accepts, stderr empty |
| qa-operator-output-report:C2 | PASS | A: saved live stdout is 319,791 bytes, 12 keys, `schema_version` 1 |
| qa-operator-output-report:C3 | PASS | R: A7-A11 and A13 exit 2, stdout `''` |
| qa-operator-output-report:C4 | PASS | R: B3 exit 1, stdout 0 bytes; U: `click.echo(payload)` is the last step of the `try` |
| qa-operator-output-report:C5 | PASS | R: B3 stderr `[sweep publish] [Errno 17] ...`; U: other exit-1 lines in unchanged `commands.py` |
| qa-operator-output-report:C8 | PASS | R: `sweep run --help` names `--run`, `--window` (`[default: 6h]`), `--root`, `--output`, `--help` |
| qa-operator-output-report:C9 | PASS | R: both help outputs diff clean against `step-1.7-help.txt` |
| qa-operator-output-report:C12 | PASS | U: `report.py` unchanged; the new text `orca call failed (invalid response)` states a fact and gives no advice |
| qa-operator-output-report:C15 | PASS | A: first-record claims re-derived from the JSON (180 rows `could not determine`, 0 unscanned, `bound_reached` 0) |
| qa-operator-output-report:C16 | PASS | G: `.gitignore:256`; U: `commands.py:99-107`, `:155` |
| qa-operator-output-report:C17 | PASS | R: help `[default: 6h]`; first and re-run JSON `window` 6h |
| qa-operator-output-report:C18 | PASS | G: `main.py` diff unchanged (+4 lines) |
| qa-operator-output-report:C19 | PASS | U: DESIGN 3.2 strings live in unchanged `commands.py`; R: B3 shows the `[sweep publish]` form |
| qa-operator-output-report:C20 | PASS | R: ruff check and `pytest tests/sweep` (4 passed) re-run clean |
| qa-publication-report:C1 | PASS | U: `commands.py:155` |
| qa-publication-report:C2 | PASS | U: `commands.py:156-164` |
| qa-publication-report:C3 | PASS | U: `commands.py:168-170` |
| qa-publication-report:C4 | PASS | U: `commands.py:146-150`, `:175-181` |
| qa-publication-report:C5 | PASS | U: `commands.py:182-196` |
| qa-publication-report:C6 | PASS | U: `commands.py:197-201` |
| qa-publication-report:C7 | PASS | U: `commands.py:202-207` |
| qa-publication-report:C8 | PASS | U: whole DESIGN 3.2 error table lives in unchanged `commands.py`; R: B3 row 1 |
| qa-publication-report:C9 | PASS | U: message strings unchanged |
| qa-publication-report:C10 | PASS | U: call order in `run` unchanged; G: `sys.exit` only in `run` |
| qa-publication-report:C11 | PASS | U: no overwrite path added; G: write-verb grep shows only the same `commands.py` lines 140, 149, 158, 170, 186, 203 |
| qa-publication-report:C12 | PASS | G: no `os.rename`, `os.replace`, `shutil`, `tempfile`, `O_TRUNC`, `write_text`, `write_bytes` in the package |
| qa-publication-report:C13 | PASS | U: `O_EXCL` and `os.link` logic unchanged (the 12-process probe cannot be re-run) |
| qa-publication-report:C14 | PASS | R: B3 exit 1, nothing at a report name; exit-0 runs left one report each |
| qa-publication-report:C15 | PASS | G: `main.py` diff is registration only |
| qa-publication-report:C16 | PASS | R: help matches OQ-2 and OQ-5 text |
| qa-publication-report:C17 | PASS | A: reports 031151, 031209, 031239 still present, stem equals `observed_at`; a fourth file (034511) exists from the executor re-run, no `.tmp` |
| qa-publication-report:C18 | PASS | R: ruff check, format check, `pytest tests/sweep` clean |
| qa-publication-report:C19 | PASS | U: unsanitized path text unchanged (still note CLI-F3) |
| qa-publication-report:C20 | PASS | U: no test file changed (still note CLI-F11) |
| qa-readonly-safety-report:C1 | PASS | G: write-verb grep over `sweep/` hits only `commands.py:140,149,158,170,186,203` and three `open(path, "rb")` reads in `probes.py` (575, 826, 890) |
| qa-readonly-safety-report:C2 | PASS | U: `_check_output` and `_publish` unchanged |
| qa-readonly-safety-report:C3 | PASS | U: same |
| qa-readonly-safety-report:C4 | PASS | R: exit-2 runs A7-A11, A13 wrote nothing |
| qa-readonly-safety-report:C5 | PASS | R: exit-0 runs wrote one report each (7 files for 7 runs; my listing did not show dot-files, so temp removal rests on the unchanged `commands.py:202-207`); the two edited files have no filesystem write |
| qa-readonly-safety-report:C6 | PASS | U: `-2` suffix path unchanged |
| qa-readonly-safety-report:C7 | PASS | G: `import subprocess` only at `probes.py:15`; `subprocess.run` at `probes.py:248` and `:299`; no `shell=` |
| qa-readonly-safety-report:C8 | PASS | U: `commands.py` calls only the five `probes` names; the new `_LIST_KEY`/check sits inside `_call`, behind `_orca` |
| qa-readonly-safety-report:C9 | PASS | G: probe: 7 of 7 hostile Orca argvs raise `ValueError`; 10 templates, 7 verbs |
| qa-readonly-safety-report:C10 | PASS | G: 3 of 3 hostile git argvs raise; `probes.py:296-297` still `--no-optional-locks` and `GIT_OPTIONAL_LOCKS=0` |
| qa-readonly-safety-report:C11 | PASS | G: no `run-list`, `run_list` or `runlist` in `sweep/`; A7 issued only `run-current` before exit 2 |
| qa-readonly-safety-report:C12 | PASS | G: only `open(..., "rb")` reads in `probes.py`; `_ledger` still checks `_check_inside` |
| qa-readonly-safety-report:C13 | PASS | A: the first-record JSON shows only allowlisted names; the executor re-run shows the same names |
| qa-readonly-safety-report:C14 | PASS | G: `main.py` diff 4 insertions, no deletions |
| qa-readonly-safety-report:C15 | PASS | R: both help outputs diff clean against `step-1.7-help.txt` |
| qa-readonly-safety-report:C16 | PASS | G: `DEFAULT_WINDOW = "6h"`, `.gitignore:256`, stem format unchanged |
| qa-readonly-safety-report:C17 | PASS | R: ruff clean, 4 passed; G: `git status` shows only the sweep package, `tests/sweep`, `main.py`, `.gitignore`, `pragmatic.md` (older change) and task files as changed |
| qa-registration-report:C1 | PASS | G: `main.py` diff context shows the `issue-watch` pair then the sweep pair, nothing between |
| qa-registration-report:C2 | PASS | G: the diff's added import line carries the same `noqa` comment as the `issue-watch` line above it |
| qa-registration-report:C3 | PASS | G: diff line `from superclaude.cli.sweep import sweep_group` (package, not `.commands`) |
| qa-registration-report:C4 | PASS | G: diff line `main.add_command(sweep_group, name="sweep")`; R: group name `sweep` |
| qa-registration-report:C5 | PASS | G: diff is one hunk, 4 insertions, 0 deletions |
| qa-registration-report:C6 | PASS | R: 19 registered names, last two `issue-watch`, `sweep` |
| qa-registration-report:C7 | PASS | G: `sweep/__init__.py` read: lazy `__getattr__`, `AttributeError` otherwise, `__all__ = ["sweep_group"]`, unchanged since 01:14 |
| qa-registration-report:C8 | PASS | U: `__init__.py` has no module-level import and is unchanged; the edited modules add no import |
| qa-registration-report:C9 | PASS | U: same file, same `__getattr__` and `__all__` |
| qa-registration-report:C10 | PASS | G: no `from/import superclaude.cli...` line in any `sweep/*.py`; R: first import of `superclaude.cli.sweep.commands` works |
| qa-registration-report:C11 | PASS | R: ruff check "All checks passed!", format "11 files already formatted" |
| qa-registration-report:C12 | PASS | R: both help outputs exit 0, diff clean against `step-1.7-help.txt` |
| qa-registration-report:C13 | PASS | U: DESIGN file time 2026-11-09, unchanged |
| qa-registration-report:C14 | PASS | U: `commands.py` top level unchanged; the edited modules add no top-level call, only a constant and a function body |

Row count: 21 + 19 + 22 + 20 + 14 + 20 + 17 + 14 = 147 rows, all PASS.

Cycle-0 checks outside the 147: `qa-failure-path-report:C7` (wrong-shape reply treated as invalid) and `qa-operator-output-report:C14` (JSON and report agree) failed at cycle 0 only because of CLI-F1 and CLI-F2 and now pass (see the Finding status section). The MINOR-only FAILs of cycle 0 (for example `qa-failure-path-report:C19`, `qa-input-edge-report:C7`) are notes and were not rechecked.

## Summary

- Checks passed: 147 / 147 (the cycle-0 PASS set); checks failed: 0.
- F_0: 2 of 2 RESOLVED (CLI-F1, CLI-F2). New BLOCKING or MAJOR findings: 0.
- Minor notes: 7 (N1 to N7). Issues fixed in place: 0 (`fix_authorization: false`; no file written except this report).
- Files written: this report only. Scratch folders under `/tmp` were removed (`cleanup ok` printed after each run).

## Self-Audit

**(a) Reliance list:** the prompt carried no `## Inherited Structural Verdict`, so no rf-qa PASS was relied on for a structural skip. I relied on the cycle-0 reports only for what each check id asks, never for a result.

**(b) Independent semantic checks (INV-019):**
- CLI-F2 behaviour, not code reading: ran the real command against 7 fake-Orca modes (6 wrong-shape) and compared each source row with SPEC section 8 (`merged-requirements.md:287`, `:439`); all matched.
- Regression risk of the new shape check on real replies: replayed the repository's own captured fixtures (`tests/sweep/fixtures/captured-*.json`, including `tasks: []` and the unknown-Run `workers: []`) through the real command; all pass, so the check does not reject captured shapes.
- Later-call behaviour: B2 (second Run wrong-shape) and B1 (unknown Run then a good Run) show availability is not flipped and later Runs are still read.
- CLI-F1: compared the JSON flag with the two report strings at `report.py:178` and `:510` and with the executor's saved re-run JSON, parsed with `uv run python -I` (flag true, 182 rows, 0 unscanned).
- Fix-log claims: checked the cited key locations (`readonly-probe.md:791` right; `a-tl-all.json` wrong, see N4) and the file times that back "only two files edited".
- Allowlist and write-verb greps were re-run rather than trusted (7 of 7 hostile Orca argvs and 3 of 3 hostile git argvs rejected).

Claims independently verified with tool output: about 75 (23 scratch runs, 6 file-time and size checks, 8 greps, the allowlist probe, 4 JSON re-derivations, SPEC and DESIGN line reads). Files read: `classify.py` (930-996), `probes.py` (40-160, 160-350, 393-402, 586-602, 1040-1285), `report.py` (165-185, 480-520, 640-673), `models.py` (225-256), `__init__.py`, the three `docs/designs/orchestrator-mode.md` ranges (1-36, 280-291, 330-452), SPEC lines 287 and 436-441, `fix-log-cycle1.md`, `consolidated-findings-cycle0.md`, `cycle-ledger.md`, the eight cycle-0 reports, the two live-check records, `step-1.7-help.txt`, `phase9-validation.md` (1-80), `tests/sweep/fixtures/SOURCES.md` (20-45), `readonly-probe.md` (785-795). If I had reported 0 notes this would be suspect; the notes are real but none is a defect in behaviour. No web research was done (Tavily not needed).

**Confidence:** Verified: 147/147 | Unverifiable: 0 whole checks | Unchecked: 0 | Confidence: 100.0%. Sub-parts I could not re-run and say so: `tests/unit` (forbidden, 285 s; the fix log reports 726 passed after the fix), the real Orca (forbidden), the cycle-0 scratch cases P1-P14, B1-B23, S1-S3 (covered by "the code they exercised is in an unchanged file"), the exit code and timing of the executor's live re-run, and the 74-file hash check (prose only).
**Tool engagement:** Read: 27 | Grep: 9 | Glob: 2 | Bash: 13 (3 fake-Orca batches, 1 allowlist probe, help diffs, file-time listings, ruff, pytest). Flag under the tool-engagement minimum: Read + Grep + Glob is 38, below the 147 check ids. Many ids are covered by one tool result (23 scratch runs each cover several ids; one file-time listing covers every U row), and the U rows rest on that file-time evidence plus the unchanged-path argument stated per row, not on a separate call each. Read the U rows with that limit in mind.

Verdict: PASS
Blocking count: 0

## QA Complete

