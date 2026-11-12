# QA Report: impl-cli gate, live-check evidence lens (agent 5 of 8, rf-qa, report-only)

**Topic:** Phase 1 sweep, step 1.4 live check (item 9.3) and the CLI shell (items 9.1, 9.2, 9.4)
**Date:** 2026-11-12
**Phase:** task-integrity / code gate, live-check evidence lens
**Fix cycle:** N/A (first review, `fix_authorization: false`; no file edited except this report)
**Package folder:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/`

Method: every number below was re-derived from the saved files with `uv run python -I` snippets that read the JSON and write nothing (scratch files only under one private `/tmp` folder, removed at the end), plus read-only `grep`, `stat`, `git status` and `ruff` runs. No live Orca command was run and `superclaude sweep run` was not run. The record's own PASS lines were not trusted.

---

## Verdict summary

All five REPORT:1247 pass conditions are supported by the saved artifacts when I re-derive them. I found no BLOCKING or MAJOR defect. I found six MINOR notes: the record misstates the reason split for 29 of 175 transcript rows, conditions 1 and 2 rest on prose for exit code, stderr and wall time, the "no contract" premise is uncited, the live data cannot discriminate between classes, the mid-check `probes._ledger` edit has no regression test yet, and one sentence in Step 3 conflates two rules.

---

## Findings

| id | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| F-1 | MINOR | `artifacts/sweep-live-check-1.4.md:37` says "the 175 transcript rows are could not determine because no tab-map join places them in the scoped Run (`Orca pane session, not in scoped Runs`)". The saved JSON (`artifacts/sweep-live-check-1.4.json`, `rows[].notes`, counted with a read-only script) holds, for the 175 transcript rows: 146 with `Orca pane session, not in scoped Runs`, 24 with `earlier pane session not joinable (tab map keeps only the latest session)`, and 5 with `session start not observable: transcript tail only`. 170 of the 175 also carry `could not join Orca workers to transcripts (tab map empty or stale)`. | The sentence attributes all 175 rows to one reason. It is true for 146. The conclusion (no row is could not determine because of a probe error or timeout) still holds for all 175, because none of the three reasons is an error or timeout, and `sources` has 0 `unscanned` rows. Only the record's explanation is wrong. | Replace the clause with the 146 / 24 / 5 split and name the SP-16 line on 170 rows. |
| F-2 | MINOR | Conditions 1 and 2 (`sweep-live-check-1.4.md:33-34`): "exit 0 (stderr empty)" and "wall time 5.1 s" have no saved artifact. Item 9.3 Action (2) (`TASK-RF-sweep-phase1-20261108-072653.md:1646`) asks for "exit code, stderr and wall time" in the `.md`; they are there as prose only. | The only machine-checkable support is indirect: the JSON exists and parses, and `commands.py:277-278` prints it as the last step of the success path, so a printed payload implies exit 0 (any failure goes to `sys.exit` at `commands.py:281`, `:285`, `:288`). `collected` runs 03:12:39Z to 03:12:44Z (5 s), which supports the 90 s bound. Stderr emptiness cannot be re-derived. | Not needed for this gate. For the Phase 2 live plan, tee stderr and `time` output to a file next to the JSON. |
| F-3 | MINOR | `sweep-live-check-1.4.md:19`: "no contract was read for these Tasks" has no citation. | The premise is the reason condition 4's expected class is could not determine instead of finished (SPEC rule 6 needs a parsed contract, `merged-requirements.md:254`). I confirmed it (checks C4 and C10) from `artifacts/readonly-probe-raw/a-tl-all.json`, but the record does not point there. | Add the two citations: no `contract <dispatch>` row in `sources`, and no `return-contract.yaml` or `--report-dir` text in the five Task specs. |
| F-4 | MINOR | `rows[]` in the saved JSON: 180 of 180 are `could not determine` with rule `fallback`; `person_started` is `null` on all 180; `summary.counts` shows 0 for the other seven classes. All five workers are identical (`succeeded` / `completed` / `released` / `exited`, `workers.json` lines 57-61 for the first worker and the same for the others), all in worktree `issue-504`. | The live check cannot tell a correct classifier from one that returns the fallback for everything. Rules 1 to 8 and the join success path were never exercised on live data (the five worker transcripts are 2.99 to 4.71 MB, so `tail_complete` is False and no join can succeed). Condition 4 holds, but only because the correct answer is the fallback. The record discloses this (`sweep-live-check-1.4.md:39`), and the owner chose a Run with no live worker (`OQ-8-run-id-decision.md`), so this is a coverage limit and not a failure. | Carry it into the Phase 2 live plan: it needs a Run with a live worker and a contract. No change to this gate. |
| F-5 | MINOR | `src/superclaude/cli/sweep/probes.py:572-584` (`_ledger` returns `False, None` on `FileNotFoundError`) was changed during item 9.3 (`Phase 9 Findings`, item 9.3 re-run log) after the impl-core gate passed. `tests/sweep/` holds only `test_readonly.py` (4 tests). | The change matches DESIGN GQ-105 (`orchestrator-mode.md:62`: a `to-do/` package with no `FINAL:` line is `unfinished`). It was logged and 9.3 and 9.4 were re-run, as item 9.3 Verification requires. No test pins the missing-`progress.md` case yet. | Make sure the later `tests/sweep/test_probes_*.py` item includes a missing-ledger case: state `unfinished`, no `package ledger` source row. |
| F-6 | MINOR | `sweep-live-check-1.4.md:19`: "`worker_done_seen` is not observable, so rule 6 (finished) and rule 2 (stalled) decline". | Rule 6 does not read `worker_done_seen` (`classify.py:266-286`); only rule 2 does (`classify.py:197`). Rule 6 declines because `row.contract` is None. The expected class is the same. | Split the sentence: rule 2 declines for `worker_done_seen`, rule 6 declines for no parsed contract. |

No BLOCKING or MAJOR finding.

---

## Re-derivation of the five REPORT:1247 pass conditions

Rule source: `RESEARCH-REPORT-orchestrator-mode.md:1247` (step 1.4 "Acceptance, live check"), quoted in item 9.3 (`TASK-RF-sweep-phase1-20261108-072653.md:1645`). The `--include-remote` timing half is dropped by the design (`research/09-gap-fill.md:105`).

| # | Condition | Re-derived from | Result |
|---|---|---|---|
| 1 | exit 0 | `sweep-live-check-1.4.json` parses and carries `report_path`; `commands.py:274-278` prints it only after `_publish` returns; every failure path ends in `sys.exit(1 or 2)` (`commands.py:279-288`). The report file exists (`.dev/sweeps/20261112-031239-sweep.md`, 605 lines, last line `Report complete`). Stderr emptiness is prose only (F-2). | Supported |
| 2 | probe calls finish inside the 90 s budget | JSON `collected` 03:12:39Z to 03:12:44Z; `summary.bound_reached` 0; 0 `unscanned` rows in `sources` (71 rows); the strings `time budget reached`, `show cap reached`, `budget reached`, `cap reached`, `call failed` occur 0 times in the JSON and the report. 9 Orca reads (1 `worker-list`, 2 `task-list`, 5 `worker-show`, 1 `worktree ps`) match DESIGN section 5 lines 244-249 (5 shows is under the 50 cap). | Supported |
| 3 | every row carries a class | 180 rows; all 180 `class` values are in the eight `CLASSES` names; all 180 have a `rule`; `summary.counts` sums to 180 = `total` = `visible`; `row_id` is unique. The 175 transcript rows equal the sum of the 30 `claude project` source file counts (175), so no transcript was dropped before classification. | Supported |
| 4 | each recorded worker gets the class its state maps to | See the worker table below. | Supported (F-3, F-4, F-6 are notes) |
| 5 | no row is could not determine because of a probe error or timeout | 0 `unscanned` sources; 0 rows whose `notes` or `evidence` mention `unscanned`, `conflict` or `call failed`; the 5 `not readable` hits in the JSON are the rule-2 note `fenced evidence not readable`, a defined note and not an error. All note texts on all 180 rows: SP-16 line (170 rows), `Orca pane session, not in scoped Runs` (146), `earlier pane session not joinable ...` (24), `session start not observable: transcript tail only` (10: 5 Orca rows plus 5 transcript rows), `Orca: exited; fenced evidence not readable` (5). None is a probe error or timeout. | Supported (record's reason split is wrong, F-1) |

### Worker table (condition 4), re-derived

Recorded state is from `artifacts/sweep-live-check-1.4-workers.json` (5 workers; `page.total` 5, `hasMore` false, `counts` `{released: 5}`): every worker has `workerState` succeeded, `dispatchStatus` completed, `terminalState` released, `projection.outcome` succeeded, `liveness.verdict` exited, `parent` null, `nextAction.kind` none.

Step 1.3 rules applied in order (SPEC `merged-requirements.md:247-257`, DESIGN `orchestrator-mode.md:474-486`):

| Rule | Condition on these five | Outcome |
|---|---|---|
| 1 `blocked_contract` | needs a contract with `worker_status: blocked`; no contract | declines |
| 2 `orca_exit_proof` | needs `worker_done_seen is False` and `fenced_evidence == "absent"`; `worker_done_seen` is never set by `probes.py` (default None, `models.py:86`) and fencing is unreadable | declines, attaches note `Orca: exited; fenced evidence not readable` |
| 3 `fenced` | needs `fenced_evidence == "present"` | declines |
| 4 `waiting_signal` | `agent_wait` null; no ready Task for them | declines |
| 5 `working` | needs `liveness_verdict == "live"` | declines |
| 6 `finished` | needs a settled outcome and a parsed contract (`classify.py:273-278`); outcome is settled but `row.contract` is None (no contract path in any Task spec: C10) | declines |
| 7, 8 | need `person_started is True`; these are Orca rows | decline |
| 9 `fallback` | everything else | **could not determine** |
| join (DESIGN line 498) | path B: the tab-map entry exists for each worker terminal, but the worker transcript is over 256 KiB so `tail_complete` is False | adds `session start not observable: transcript tail only`; class stays could not determine |

Expected class is could not determine (rule 9 `fallback`) for all five. The saved JSON reports exactly that for `orca:ctx_4e3237d227c3`, `orca:ctx_6a0e3e3baaee`, `orca:ctx_7c86fffa9716`, `orca:ctx_9a3728b21883` and `orca:ctx_dad78c5c1332` (class, rule `fallback`, the two notes above, evidence `no rule 1 to 8 matched (liveness_verdict exited, outcome succeeded, status completed; person_started None)`). The five Dispatch ids equal the five in the independently saved worker list. Match: 5 of 5.

---

## Checks

| id | Check | Result | Evidence |
|---|---|---|---|
| C1 | Pass condition 1 (exit 0, stderr empty) supported | PASS | `commands.py:274-288`; JSON parses with `report_path`; report file present with `Report complete` last line. Stderr only in prose (F-2, MINOR). |
| C2 | Pass condition 2 (inside 90 s budget, no bound) supported | PASS | `collected` 5 s; `bound_reached` 0; 0 `unscanned`; 0 budget/cap strings; 9 Orca reads match DESIGN section 5. |
| C3 | Pass condition 3 (every row has a class) supported | PASS | 180/180 classes in `CLASSES`; counts sum to total; 175 files = 175 transcript rows. |
| C4 | Pass condition 4 (expected class per worker) supported, each worker checked against step 1.3 | PASS | Worker table above; 5 of 5 match; independent of the record's PASS lines. |
| C5 | Pass condition 5 (no could-not-determine from probe error or timeout) supported | PASS | Every note text on all 180 rows listed above; none is an error or timeout. Record's split is wrong (F-1, MINOR). |
| C6 | Step 1 command argv equals the `ALLOWED_ORCA` entry and DESIGN 7.3 | PASS | `probes.py:49` = `("orchestration", "worker-list", "--run", "<run>", "--json")`; DESIGN 7.3 block (`orchestrator-mode.md:519-531`) has the same tuple; record lines 7-8 give argv `orchestration worker-list --run run_a4723d345399 --json`; `grep -n '"worker-list"'` hits `probes.py:49`; no `--include-remote`. |
| C7 | Saved worker list is self-consistent and is the OQ-8 Run | PASS | `runId` `run_a4723d345399` on all 5, `scope.run` same, `page.total` 5; `OQ-8-run-id-decision.md` names the same Run with 5 rows, none live; the five Dispatch ids equal the sweep's five Orca rows. |
| C8 | Tail-incomplete claim (transcripts over 256 KiB) | PASS | `stat` of the 5 worker transcripts (the 5 transcript rows carrying only the tail-only note): 4,709,478; 4,408,755; 4,180,425; 2,987,139; 3,605,224 bytes, all over 262,144. Tab-map files containing each of the 5 terminal handles exist (5 of 5). |
| C9 | Worker-list state vs sweep-run state (no drift between the two reads) | PASS | Sweep evidence strings say `liveness_verdict exited, outcome succeeded, status completed` for all five, equal to the saved list. |
| C10 | "No contract was read" premise (feeds C4) | PASS | No `contract <dispatch>` row in `sources`; no `return-contract.yaml` or `--report-dir/--output-dir/--output` text in any of the 5 Task specs in `artifacts/readonly-probe-raw/a-tl-all.json` or in `a-ws-ctx_6a0e3e3baaee.json`; `_contract_candidates` (`probes.py:1001-1011`) only reads paths named in `task_spec_text` or `body_text`. Premise uncited in the record (F-3, MINOR). |
| C11 | Published report vs JSON | PASS | `Sessions (180/180)`; `Scope: Runs run_a4723d345399 . worktrees 30 . sessions 180/180 (lower bound: remote hosts not scanned) . window 6h`; Source coverage table with 0 unscanned; report name matches `<YYYYMMDD-HHMMSS>-sweep.md` in UTC (`20261112-031239`, equal to `observed_at` 03:12:39Z); 3 reports in `.dev/sweeps/` (two earlier runs kept, as the record says). |
| C12 | OQ-2: report location and name | PASS | `git check-ignore -v` gives `.gitignore:256:.dev/sweeps/`; `commands.py:99-107` default `<root>/.dev/sweeps`; `commands.py:155` stem format; the OQ-2 record chose exactly this. |
| C13 | OQ-5: `--window` default 6h, activity-only | PASS | `commands.py:27` `DEFAULT_WINDOW = "6h"`; `step-1.7-help.txt:27` `[default: 6h]`; JSON `window` `6h`; `summary.historical` 0 and all 180 rows listed regardless of age (the five workers were released about 7.3 to 7.5 h before the run and are still listed). |
| C14 | `commands.py` matches DESIGN 3.2, 5 and 7.1 (exit map, `_publish` steps, stage prefixes) | PASS | `commands.py:242-288` vs `orchestrator-mode.md:99-129` and `:435-447`: exit 2 for `click.UsageError`/`BindingError`; exit 1 for `_PublishError` and any other exception with `[sweep <stage>]`; `_publish` steps 1-7 in order (`commands.py:153-208`); `sys.exit` only inside `run`. Item 9.1 greps re-run: no `os.rename`/`os.replace`/`run-list`; 3 `sys.exit` lines (281, 285, 288), all inside `run`; the five fixed message parts each found once with `grep -F`. |
| C15 | `main.py` registration | PASS | `git diff -- src/superclaude/cli/main.py`: 4 insertions, 0 deletions, after the `issue-watch` line, same `noqa` comment; `uv run superclaude sweep run --help` exits 0 (re-run from `/tmp`); `step-1.7-help.txt` text matches the code (`commands.py:219-245`: four options, `run` command). |
| C16 | `phase9-validation.md` claims | PASS (3 of 4 parts re-run) | Re-ran `ruff check --no-cache` (All checks passed), `ruff format --check --no-cache` (11 files already formatted), `pytest tests/sweep -p no:cacheprovider` (4 passed). The `tests/unit` part (726 passed, 2 skipped, 285 s) was not re-run; the file is dated 03:20, after the 03:12 third live run, so it post-dates the `probes._ledger` fix. |
| C17 | Live check stayed read-only | PASS | `sources` holds only allowlisted Orca reads, `git status` per worktree (30) and disk reads; no forbidden token; the one write is the report under `.dev/sweeps/` (gitignored). |
| C18 | Mid-check code change handled per item 9.3 re-run rule | PASS | `Phase 9 Findings` logs the `_ledger` change, the 993 unscanned rows in runs 1 and 2, and the re-run; the change matches GQ-105 (`orchestrator-mode.md:62`). No regression test yet (F-5, MINOR). |
| C19 | Other figures in the record | PASS | 320 KB JSON (319,791 bytes); 2 packages in state `conflict` in two worktrees (`/home/coder/workspaces/Coder`, `/home/coder/workspaces/worktrees/Coder/dashboard-bmad`) listed under `## Retained problems`; 30 worktrees, all `status_read` true; 413 tab-map entries. |
| C20 | `safe_to_close` on the five rows is consistent with the real worktree | PASS | JSON worktree `issue-504`: `uncommitted` true, `removable` no; read-only `git status` of that worktree shows 5 `??` paths (`.dev/issues/504/` and four `.dev/reflect/...`). |
| C21 | Live data can discriminate the classifier | FAIL (note only) | F-4: 180/180 could not determine. Not a gate failure; the record discloses it. |

Checks passed: 20 of 21. The one FAIL (C21) is graded MINOR and does not fail the gate.

## Confidence

Verified: 21/21 (C21 verified as a limit) | Unverifiable: 0 whole checks (one sub-part of C16, the `tests/unit` run, was not re-run because it takes 285 s) | Unchecked: 0 | Confidence: 100.0%

Tool engagement: Read: 21 | Grep: 8 | Glob: 0 | Bash: about 24 (read-only: `ls`, `stat`, `grep`, `git status`/`diff`/`check-ignore`, `ruff --no-cache`, `pytest -p no:cacheprovider`, and about 11 `uv run python -I` snippets that read the saved JSON). No web research.

## Summary

- Blocking findings (BLOCKING plus MAJOR): 0
- Minor findings: 6 (F-1 to F-6)
- Files edited besides this report: 0

## Recommendation

Proceed. The five pass conditions hold on the saved evidence. Fix the reason split in the record (F-1) if it is cited again, and plan the Phase 2 live check on a Run with a live worker and a contract so that rules 1 to 8 and the join success path get live evidence (F-4).

Verdict: PASS
Blocking count: 0

## QA Complete
