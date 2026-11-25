# Proposal A: minimal delta

One `## Unattended mode` section in `implement.md` shaped like analyze, task, troubleshoot and workflow (Switch, Report directory, Contract, Person-mode flags, Gates, Nested invocations, Outward actions); short `--unattended` clauses in the skill and refs. Zero new STOP codes, zero new ledger records, two NEW flags already used by other commands.

## 1. Switch and grammar

- NEW `--unattended`, NEW `--report-dir <dir>`, added to Wave 0 known options.
- They count in the option prefix, or after a single existing file path (as `--resume` does). After an inline prompt starts they are prompt text, the same rule Wave 0 step 1 applies to banned tokens. Brief form: `Command: /sc:implement --unattended --report-dir <dir> <absolute plan path>`.
- Person-mode flags: none. `--force` keeps `E-NO-RULING`.

## 2. Report directory

`--report-dir` only (`--ledger` is file-valued). Missing: WC-4 chat refusal. Same invalid list as workflow, plus any directory inside `.dev/tasks/` or the ledger directory (the archive helper moves packages; the ledger directory belongs to the run).

## 3. Contract

WC-4 fields only. `report_path` = the ledger (after archive, its `done/` path). `artifacts` = files named in this run's ledger `files=` fields, files written in the ledger directory, `<report-dir>/follow-ups.md`, nested contracts, minus git-ignored paths. `reason` = STOP code, halt reason, task id. `blocked_question` = the halt text printed today (task, verdict, blocking findings, `Next: fix | ruling | resume`).

| Outcome | worker_status |
|---|---|
| all tasks complete, legacy FINAL pass or skipped, `already complete`; managed `archived` or `already-archived` | succeeded |
| legacy `FINAL: issues`, or a safety-scan hit | partial |
| `E-HALT-QA` (every halt reason), `E-NO-RULING`, `E-ARCHIVE-BLOCKED` after `FINAL: issues`, `index.lock` found (WC-9) | blocked |
| `E-ARCHIVE-BLOCKED` from `--skip-final-review` or helper refusal, `E-RESUME-NEEDED`, every input and integrity STOP | failed |

A task completed by a Ruling already in the ledger counts as complete. Both blocked and failed (except `E-RESUME-NEEDED`) freeze the plan under D2, unchanged.

## 4. Points that ask a person

- **Ruling halt, `E-HALT-QA`:** halt and blocked lines written as today; no question, no Ruling (WC-3); blocked.
- **`E-NO-RULING`:** blocked. No chat confirmation exists, so only an eligible Ruling already in the ledger counts; Resume row R stays automatic.
- **Rows P and H:** operator review is user-initiated (qa.md, Closed list item 4). Under `--unattended` both rows run no review and append nothing; blocked, `reason` `E-HALT-QA operator review not run`.
- **`E-ARCHIVE-BLOCKED`:** per table; package stays in `to-do/`.
- **`E-RESUME-NEEDED`:** failed; the coordinator may re-run it as a new Task (D2, WC-6).
- **Review cap:** reviewer-down is `E-RESUME-NEEDED`; `RETRY_BUDGET` gives the `budget` halt. No change.
- **FINAL issues:** per table.
- **Follow-up offer:** none (the protocol already makes none). The follow-up print and scan output also go to NEW `<report-dir>/follow-ups.md`.
- **Parallel batches:** unchanged. A batch task already halts `batch` (blocked). Commits are off, so WC-9's batch clause never fires. Forcing sequential is one line but changes behaviour; rejected.
- **Extras timeouts:** each extras Bash call gets a 4 minute timeout (WC-10); on timeout record `<extra>=skip` and one line in `follow-ups.md`. Extras never change the verdict.
- N>=20 notice and auggie unavailability: not gates, unchanged.

## 5. Forbidden and allowed

Forbidden: commit, push, merge, PR, any `git add` (the three staging sentences in SKILL.md Q2, `refs/ledger.md`, `refs/managed-workspace.md` gain "not under `--unattended`; the coordinator stages, WC-9"), writing a Ruling, Orca calls. Allowed (WC-9): private-index snapshots, `refs/superclaude/implement/` refs, `sc_retry_revert`, the archive helper move; the contract lists the `done/` path so the coordinator stages it.

## 6. Nested invocations

Q1 and Q6 `sc:impact-protocol` calls get `--unattended --output-dir <report-dir>/nested/impact-<n>/` in place of `<ledger dir>/impact/<task-id>` (impact's own flag is its report directory; both would be refused). A failed or missing nested contract keeps today's `graph:absent` path. Reviewer and adviser subagents are unchanged.

## 7. Plan approval (O3 unanswered)

The command is identical under both answers; only the coordinator differs.

- **O3 yes:** the coordinator creates the implement Task only after the approval record for the plan hash exists (`superclaude issue-pipeline plan-hash` and `check-approval`, WC-17). Managed plans pin the hash at first `start`; `E-PLAN-CHANGED` (failed) catches later edits.
- **O3 no:** the Task is created when the workflow Task settles succeeded.
- `/sc:workflow --handoff implement` stays skipped; implement is always its own Task (plan path known only after workflow settles).
- Gap: an edit between the coordinator's check and the first `start`. Follow-up if wanted: NEW brief line `Plan hash:` checked by the worker guard.

## 8. Idempotence and resume

Ledger resume stays implicit: a re-run resumes at the first non-complete task and reuses `start` shas. Each retry is a new Task with a new report directory (WC-6); a re-invocation into the same directory replaces the contract whole. The contract is written last, after the ledger flush, and on every STOP. A finished plan re-run gives succeeded with no product writes.

## 9. Not changed

LL-IMPL guard, `GOVERNED_LEVELS_ALLOWED`, issue-pipeline brief rows, `WORKER-CONTRACT.md`. UNVERIFIED: whether `worker-start` sessions hit LL-IMPL; whether `.dev/implement/` is git-ignored; the classification values `WRITE_VERB_CLASSIFICATION` uses besides `deferred:P4`. O5 as authority: recommend a live check before the default set, as for P2.

## 10. Tests

- `tests/skills/test_worker_contract.py`: move implement from NOT_CONVERTED to a new P4 set (exact counts), add its UNATTENDED_EXPECT entry, reclassify the three `deferred:P4` lines. The existing section checks then apply; `nested/` is allowed because the nested list is non-empty.
- NEW `tests/skills/test_implement_unattended.py`: every STOP-table code appears once in the mapping; Wave 0 lists both flags; rows P and H and the Halt table carry the clause; each `git add .dev/tasks` sentence carries the deferral; source and `plugins/superclaude/` mirror match; the section has no `AskUserQuestion` or `STOP AND WAIT`.
