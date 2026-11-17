# Reviewer brief

Run: pre-TASK-WF-blockerStage2-20261116-030156-20261116174316 (UC-1). Plan and spec paths are in the T1 card header. You are read-only: Read, Grep, Glob and codegraph/search tools only. Audit the supplied hunks and the live files they cite; run nothing.

## T1 card excerpt

### F1 [MAJOR, grounded] The /sc:implement sweep has no ledger to read
The plan puts the one sweep call into the final review step of /sc:implement and tells it to read "every `follow-ups.md` under the package folder" (plan:72). Nothing in this stage, or in stages 1, 3, 4, makes /sc:implement write a `follow-ups.md`: its review loops write notes files (qa.md:209-213, "Write the notes file"), and the spec wants a pointer row in a ledger for /sc:implement (merged-requirements.md:484, "keeps `notes.md`; the ledger holds a pointer row") that no task builds. So in every /sc:implement run the call sees zero ledgers. Task 8 states the limit only as "mostly reports skips" for code deliverables (plan:138). The SKILL.md paragraph also prints a fixed line "follow-ups are recorded and not filed, and the owner can ask the session to file them" (plan:72); with no ledger that line is false.
Consequence: the carrier cannot produce any result; the printed line misleads.

### F2 [MAJOR, grounded] GR12 safety row -> `partial` is not carried into the worker contract
Spec 6.4 says a possible safety finding graded non-blocking "makes the run `worker_status: partial`" (merged-requirements.md:438). Task 5 adds the three keys and maps only `follow_up_capture_state: incomplete` to partial, and says "follow-ups alone never change `worker_status` from `succeeded`" with no exception (plan:102); its tests cover only the `incomplete` case (plan:106-107). Task 2's `safety --unattended` "sets the signal that makes the run `partial`" (plan:56), but no contract text or test makes that signal count.
Consequence: an unattended safety row can end `succeeded`.

### F6 [MINOR, grounded] tech-research safety route depends on a "nobody reachable" signal it cannot know
Task 4: "with nobody reachable it records and does not wait" (plan:88), but tech-research has no unattended mode (plan:102), so the skill has no stated way to choose `--unattended`.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T17:48:47Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (index covers py/yaml/js/ts, not Markdown: use Read/Grep for the plan, skills and spec)

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:68-83

````markdown
## Task 3: Give the final review step of `/sc:implement` one read-only sweep call and a printed follow-up list

Depends on: Task 2

Read `src/superclaude/skills/sc-implement-protocol/SKILL.md` (the "Done" section and the "Whole-list review" section) and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (the archive gate, steps 1 to 6, and the sentence that begins "`<skill base>` is the base directory") and `refs/qa.md` (the accepted-minor path with its final-summary sentence, and the closed list of interrupts) before editing, and edit only the first two files. In `SKILL.md` "Done", add one paragraph "Follow-up sweep (record and print only)": at the final review step the executor makes one call of `superclaude review follow-ups sweep` over the follow-up ledgers the run's review loops wrote (every `follow-ups.md` under the package folder for a managed package, or under the ledger directory for a legacy run), with the delivery files named in the ledger `files=` fields as deliverables and `--kind auto`, never `--promote` and never `--write`, and its record file in the package `./artifacts/` (legacy: the ledger directory); the final summary prints the recorded counts, the ledger paths relative to the package so they stay valid after the archive move, the `show_user` rows first, any sweep-flagged rows, and one plain-English line: follow-ups are recorded and not filed, and the owner can ask the session to file them, which shows the issue text first and files nothing until the owner says yes. The paragraph states that this step asks the user nothing ("It asks the user nothing"), makes no offer (the offer is the top-level session's), changes no verdict, no final-review result and no archive outcome, adds no STOP code, and that a missing `superclaude` command or a non-zero exit is printed as one line and the run continues. In `refs/managed-workspace.md`, add one paragraph between the code block that ends step 5 and the line that begins "6. `pass`": on a final review that appended `FINAL: pass`, make the one sweep call described in `SKILL.md` before the helper moves the package. Do not renumber the steps and do not change any existing line. Then run `make sync-dev` and copy the two edited files byte for byte to `plugins/superclaude/skills/sc-implement-protocol/SKILL.md` and `plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` with `cp`.

The existing tests that pin this text and must stay green: `tests/skills/test_implement_severity_static.py` (its halt, stop and ruling site scan flags any new line that holds the words halt, Ruling, `E-HALT-QA` or `E-ARCHIVE-BLOCKED`, and its allow-list pins the step 2, step 3 and step 6 lines of the archive gate), `tests/skills/test_review_severity_rule.py` (the byte-equal twin test, the old cap wording scan and the sweep-phrase patterns), `tests/skills/test_task_workspace_lifecycle.py` (no cross-file line pointers, the location-resolution rows), `tests/skills/test_task_workspace_smoke.py`, `tests/skills/test_workflow_archive.py`, `tests/skills/test_implement_saved_prompt_rule.py` (managed-workspace.md), `tests/skills/test_reflect_input_snapshot.py` (the managed-workspace.md mirror), `tests/skills/test_codegraph_adoption.py` and `tests/commands/test_impact_command.py` (both read `SKILL.md`), `tests/skills/test_worker_contract.py` (the git-word scan of these files), and `tests/unit/test_cli_install.py` (the installed file lists).

Acceptance criteria:
- `sha256sum` of `refs/qa.md` in both trees equals the two lines of `./artifacts/qa-md-sha256-before.txt`, and `git diff --stat HEAD -- src/superclaude/skills/sc-implement-protocol/refs/qa.md plugins/superclaude/skills/sc-implement-protocol/refs/qa.md` prints nothing.
- In `refs/managed-workspace.md` the new paragraph sits after the line that begins "5. Re-run step 3." and before the line that begins "6. `pass` → run the helper in archive mode", and both of those lines and the line "2. `--skip-final-review` → no FINAL and no archive" are unchanged.
- `grep -c "superclaude review follow-ups sweep" src/superclaude/skills/sc-implement-protocol/SKILL.md src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` prints 1 for each file, neither call line holds `--promote` or `--write`, and the sentence "It asks the user nothing" appears in `SKILL.md`.
- `git diff -U0 HEAD -- src/superclaude/skills/sc-implement-protocol | grep '^+' | grep -E "\bhalt(s|ed|ing)?\b|E-HALT-QA|E-ARCHIVE-BLOCKED|\bRuling\b"` prints nothing.
- `uv run pytest tests/skills/test_implement_severity_static.py tests/skills/test_review_severity_rule.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_task_workspace_smoke.py tests/skills/test_workflow_archive.py tests/skills/test_implement_saved_prompt_rule.py tests/skills/test_reflect_input_snapshot.py tests/skills/test_codegraph_adoption.py tests/commands/test_impact_command.py tests/skills/test_worker_contract.py tests/unit/test_cli_install.py -v` passes, and `make verify-sync` reports no difference.
- `cmp` shows the two plugin twin files equal to their sources.

````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:98-107

````markdown
## Task 5: Add the three follow-up keys to the worker contract

Depends on: Task 2

Edit `src/superclaude/core/WORKER-CONTRACT.md`: WC-4 (the bullet that enumerates the top-level keys, `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`) gains `follow_up_ledger` (path), `follow_up_counts` with `follow_up`, `note` and `show_user`, and `follow_up_capture_state` (`complete`, or `incomplete` with a reason); the status mapping maps `incomplete` capture to `worker_status: partial`; the coordinator duties (the bullet that says "the coordinator opens it") name the three keys as things to read; follow-ups alone never change `worker_status` from `succeeded`; the ledger is listed in `artifacts` only when it is a tracked path (WC-4 keeps gitignored paths out). One added sentence names the producer: a command that records follow-ups copies the three keys from the output of `superclaude review follow-ups summary` (Task 2), and a command that records none omits all three. State in the summary of Task 8 the limit that no command emits them live yet: `/sc:implement` has no unattended section until its conversion (its WC-9 rows in `tests/skills/test_worker_contract.py` are marked deferred), and tech-research has no unattended mode and no contract. Update `tests/skills/test_worker_contract.py` and add T10 cases.

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` lists the three new keys in the bullet that enumerates top-level keys and names `superclaude review follow-ups summary` as their producer.
- `uv run pytest tests/skills/test_worker_contract.py -v` passes and a new test fails when a contract with `follow_up_capture_state: incomplete` is not mapped to `partial`.
- A test over the `follow-ups` commands run unattended asserts that recording follow-ups makes no GitHub call (the subprocess call is replaced by one that raises) and asks no question (standard input is closed and the command returns).
````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:52-64

````markdown
## Task 2: Add the follow-ups command group

Depends on: Task 1

Read `src/superclaude/cli/review/__init__.py` (it registers nine subcommand modules today and none for follow-ups, the safety route or the sweep, so a skill can name no working command until this task adds one) and the stage 1 modules `follow_ups.py` and `safety_route.py`, and write `./artifacts/follow-ups-cmd-wiring.md` naming each stage 1 function the commands call. Create `src/superclaude/cli/review/follow_ups_cmd.py` exporting `command` (a click group named `follow-ups`), add `"follow_ups_cmd"` to the tuple in `__init__.py`, and give it four subcommands. `write --ledger <path> --report <reviewer report> (repeatable) --run-id <id> --gate-id <id> [--expected-revision <n>]` imports the non-blocking rows of reviewer report tables through the stage 1 writer (the run owner is the only writer; a reviewer report row carries the fields `rests_on` and `why not blocking`; the tier of a row is the shared outcome that `refs/scale-map.md` gives its native label; Blocking rows are never written; a Medium row without `why not blocking` is refused by the writer and reported; a report that cannot be read sets `capture_state: incomplete` with the reason). `safety --ledger <path> [--judge-answers <file>] [--unattended]` runs the stage 1 safety route over the ledger and prints what it returns: attended text names the person prompt, unattended output sets the signal that makes the run `partial`. `sweep --root <dir> | --ledger <path> (repeatable) --deliverable <path> (repeatable) --kind auto|report|spec|tasklist|code|other [--promote] [--write] [--output <file>]` calls Task 1's sweep, prints the flagged rows (id, deliverable, section) and the skipped count, writes the same text to `--output` when given, exits 0 whenever it ran (flagged rows are information) and non-zero only when it cannot run. `summary --ledger <path>` prints exactly the three worker-contract keys as YAML (`follow_up_ledger`, `follow_up_counts` with `follow_up`, `note` and `show_user`, `follow_up_capture_state`); this is the named producer of those keys for Task 5. No subcommand calls `gh`, a network or a judge. Create `tests/review/test_review_follow_ups_cmd.py`.

Acceptance criteria:
- `uv run superclaude review follow-ups --help` exits 0 and lists `write`, `safety`, `sweep` and `summary`; `uv run superclaude review --help` still lists every earlier subcommand (and `classify` from the stage 1 package) and now lists `follow-ups`.
- `uv run pytest tests/review/test_review_follow_ups_cmd.py tests/review/test_review_cli.py tests/review/test_review_sweep.py -v` passes.
- A test shows `sweep` without `--promote` and `--write` leaves the ledger bytes unchanged and does not promote, and `write` run twice on the same report leaves the ledger as after the first run.
- A test shows `summary` prints exactly the three keys, and `follow_up_capture_state` reads `incomplete` with a reason after an unreadable report.
- `grep -n "subprocess\|requests\|httpx\|\bgh\b" src/superclaude/cli/review/follow_ups_cmd.py` prints nothing.
- `./artifacts/follow-ups-cmd-wiring.md` names each stage 1 function used and states that this package owns `follow_ups_cmd.py`.
````

### src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:46-64

````markdown
## Completion: fresh FINAL, then archive

Dispatch (replaces the legacy "already complete" stop for managed packages): when every task is `complete` and the package is still in `to-do/`, you are **active all-complete** → run the archive gate below. Report `archive-blocked: <reason>` if it cannot finish. Never print `already complete` for an unarchived package.

Archive gate, **every attempt** (N=1, resume, retry; an earlier FINAL never counts):

1. Join every delegated writer / background task. Nothing may still be writing the package or delivery files.
2. `--skip-final-review` → no FINAL and no archive: STOP `E-ARCHIVE-BLOCKED` (`--skip-final-review` prevents archiving a managed package).
3. State: `uv run --no-project python "<skill base>/scripts/archive_workspace.py" --root "<checkout>" --package "<checkout>/.dev/tasks/to-do/<slug>" --print-state` → JSON `{"status": "state", "state": "<sha256>", "files": [...]}` (the plan/source/delivery-file digest; `files` = every repo-relative path named in a ledger `files=` field, so list every delivery file there). Failure → STOP `E-ARCHIVE-BLOCKED` with the helper's code.
4. One independent reviewer (always a Task subagent, even N=1; `refs/qa.md` isolation rules) gets the current full plan, the full ledger, and the current contents of each listed delivery file. Pass absolute paths (include the package root so `./artifacts/` tokens resolve) or inline contents; the reviewer must read the real current files. It verifies every task's AC against the real files and returns `pass` or `issues` with `path:line` evidence. Missing or unverifiable evidence → `issues`, as `refs/qa.md` (Managed FINAL review) defines it. For a user-accepted gap, verify the current outcome still matches the recorded scoped acceptance and cite the unmet AC honestly; any new or changed unaccepted gap → `issues`. Do not mark unmet AC as met or change the non-compliant task verdict. The reviewer applies the FINAL derived test of `refs/qa.md`: a notes entry whose answers are all `no` is never `issues`, and a notes entry with a confirmed `yes` is `issues`.
5. Re-run step 3. If `state` changed during the review, discard the result and repeat from step 1. Otherwise append (after all task lines and the latest `PLAN:` pin):

```
FINAL: <pass|issues> evidence=<ev-list> state=<sha256>
```

6. `pass` → run the helper in archive mode (no extra flag). It appends its own `ARCHIVE: start id=<id> token=<hex>` line after FINAL and moves the package; there is no later "complete" record (location is the archive state). `issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says, except the recovery's own re-review of a saved-prompt task. Before that stop, when every `issues` item of the FINAL concerns a saved prompt (a template difference, a superseded prompt with no later passing saved prompt, or a missing README), the executor runs "Defective saved prompt (recovery)" from `refs/qa.md` in the same invocation and then repeats the archive gate from step 1; the recovery is idempotent (it finishes a half-done move, writes a missing README and runs a missing re-review), and the stop applies only if the recovery cannot finish or the new FINAL still returns `issues`.

`<skill base>` is the base directory the loaded skill announces (the directory holding this skill's `SKILL.md`); never hardcode a repository `src/` path. A FINAL pass is not a commit, PR, merge, release or human approval.
````

### src/superclaude/skills/sc-implement-protocol/refs/qa.md:205-226

````markdown
**Notes keep every minor of the final chain (deliberate SPEC correction of FR-020).** Every review that fails appends its `minor` and `note` findings to the notes file at once, tagged with its review id `r<k>-<j>`, before any later review can overwrite `review-<k>.md`. The passing review's minors and notes, and any capped finding of the final tree, are written at `complete`. The `complete` rewrite keeps, as lines 2 to m, every line of the current tree chain (all reviews since the latest Q0 rebuild, meaning since the task's `start` or its latest revert) whose flagged text is still in the final tree, plus every dispute line of the current `start`; every other line (lines of reverted trees and lines whose text is gone) follows line m, prefixed `superseded `. The `notes@` token cites lines 1 to m.

**Token rule.** A notes file holding any line after line 1 gets a `notes@<path>:1-<m>` token in `evidence=` on the `complete` line; a file holding only `superseded ` lines after line 1 gets the token `notes@<path>:1-1`; no file means no token. A review chain with no minors and no notes writes no notes file. The token is never an AC citation (`refs/ledger.md`).

**Automatic accepted-minor path.** When a review has no `blocking` finding, the orchestrator does three things and asks the user nothing:

1. Write the notes file (above).
2. Run Q6 extras.
3. Append the `complete verdict=compliant … notes@…` line (`refs/ledger.md`).

| | Accepted-minor | Ruling (Halt table above) |
|---|---|---|
| Who decides | Severity derived by the parent from the reviewer's checklist answers and anchors, plus the mechanical origin caps | The user, in the current conversation |
| Covers | `minor` and `note` only | Any explained gap, blockers included |
| Ledger | `compliant` verdict plus a `notes@` token | A `Ruling:` line, then `complete` with the unchanged non-compliant verdict |
| Writes a `Ruling:` line | Never | Always |

The Ruling path is unchanged and remains the only exit from a halt. Conditions on the accepted-minor path:

- A task completes with recorded minors only after a fresh subagent review (see "Subagent prompt").
- When no FINAL that can block will run (legacy N=1, legacy `--skip-final-review`, or any legacy run, whose FINAL is advisory), the run's final summary prints every recorded minor with its checklist answers. The summary is informational and never asks the user anything.
- A batch task whose A2 has only minor or note findings completes on this path instead of halting `batch`. A batch A2 with a confirmed blocker still halts `batch`.
````

### src/superclaude/skills/sc-implement-protocol/refs/qa.md:262-288

````markdown
## Interruption table per attempt

| Attempt | May fail the attempt | May halt | May prompt the user | Minors may be edited |
|---|---|---|---|---|
| A1 | `blocking` only | `blocking` only (in practice never: an A1 failure goes to the A2 fix pass) | `blocking` only (in practice never) | only inside lines already changed for a blocker |
| A2 with its one repair | `blocking` only | `blocking` only | `blocking` only | only inside lines already changed for a blocker |
| A3 | `blocking` only | `blocking` only | `blocking` only | no, recorded only |
| A4 | `blocking` only | `blocking` only | `blocking` only | no, recorded only |
| A5 | `blocking` only | `blocking` only (`ladder-end`) | `blocking` only | no, recorded only |
| legacy FINAL | `blocking` only, advisory (never reopens a task) | never | never (summary only) | no |
| managed FINAL | `blocking` only (`issues`) | `blocking` only (`E-ARCHIVE-BLOCKED`) | `blocking` only | no |

Mapping: high = any confirmed checklist `yes` = `blocking`; medium, IMPORTANT without a `yes`, low-medium, low and cosmetic = `minor` or `note`. Every minor and note is recorded in the notes file and cleared: no halt, no Ruling, no user prompt, at every row. "Cleared" means recorded and closed, not necessarily edited. The FINAL still runs. The only non-finding interrupts are the STOP rows of the STOP table in `SKILL.md` (see "Closed list of interrupts" below).

## Closed list of interrupts

Each line names the path, when it fires and why it stays.

1. `E-HALT-QA` after a ladder halt (`ladder-end`, `advice-rejected`, `no-runner-up`, `brief-invalid`, `budget`, `batch`, `no-snapshot`, `head-moved`, `no-evidence`): reachable only after an attempt failed on a confirmed blocker that a repair could not close. Kept because a real failure must block and the revert guards protect data. The halt message and any Ruling request list blocking findings only.
2. `dispute` halt: only when the adviser disputes a blocking finding or the AC itself. Kept because a disputed AC is a user decision.
3. `E-NO-RULING`: reachable only when someone tries to continue past a non-compliant verdict, which now exists only with a blocker. Kept as the user-acceptance safety gate.
4. `operator-review`: user-initiated after a halt, never started by automation.
5. `E-RESUME-NEEDED` (`reviewer-down` after a second paperwork-only or unparseable review, `ref-failed` including a notes file that cannot be written, incomplete revert, adviser agent missing): infrastructure, never about a finding; it asks the user to re-run, not to fix anything. Kept because continuing would record an unverified completion or risk data loss.
6. Input and integrity STOPs (`E-NO-SOURCE`, `E-SOURCE-MISSING`, `E-NO-TASKS`, `E-NO-AC`, `E-LEGACY`, `E-LEDGER-CORRUPT`, `E-LEDGER-PATH`, `E-MANAGED-INVALID`, `E-MANAGED-CONFLICT`, `E-PLAN-CHANGED`, `E-ARCHIVE-MARKER`): occur before or outside per-task QA. Kept unchanged.
7. `E-ARCHIVE-BLOCKED` (managed): FINAL `issues` naming a blocking defect at the end state (see "FINAL derived test" below), `--skip-final-review` on a managed package, or a helper refusal. Kept because FINAL is never waived.

No other path may stop automation or prompt the user. Every halt message and Ruling request lists blocking findings only. A minors-only replay writes no `halt` and no `Ruling:` line.
````

### src/superclaude/skills/sc-implement-protocol/SKILL.md:184-196

````markdown
### Whole-list review

**Legacy sources.** After the last task is `complete`, when N>1 and not `--skip-final-review`: one reviewer pass vs the full spec + full ledger. The pass also reads every brief named by a `retry … step=revert` record and every file in `<retries>/T<id>/`, and judges WHAT against the spec. Append `FINAL: pass|issues evidence=...`. Advisory. Do not rewrite per-task verdicts. Do not reopen completed tasks unless the operator says so. N=1: skip (the per-task review is that pass). The pass applies the FINAL derived test of `refs/qa.md` and stays advisory.

**Managed packages.** Not advisory and never skipped: every archive attempt runs the fresh FINAL and the helper archive in `refs/managed-workspace.md`, even for N=1 and on resume.

## Done

Every enumerable task has a `complete` ledger line (verdict `compliant`, or non-compliant plus operator Ruling). Print the ledger path. A `compliant` line may carry a `notes@` token (complete with notes, `refs/qa.md`). When no FINAL that can block ran (any legacy run, including N=1 and `--skip-final-review`), the final summary also prints lines 2 to m of each task's notes file with their checklist answers, informational only, asking the user nothing. The final summary also prints every `family-fallback:` header line of an `advice-3-b.md` (`refs/retry.md`, Model ladder). Suggest `/sc:test` and `/sc:git` only as optional next steps, not gates.

Legacy: if all tasks already `complete` on invoke: STOP `already complete: <ledger path>`.

Managed: done means the helper reported `archived` (print its actual `done/` path) or `already-archived`. All tasks complete but not archived is **archive-blocked**, not complete.
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:430-441

````markdown
### 6.4 Unattended runs

<!-- Source: Base (original, modified) - return contract replaced per Change #PC-22 (three keys, visible capture failure; BW-09); tracked-path and nesting rules per RM-1; safety route per Change #PC-10; absence rule per RM-5; final report line and judge-call rule from Variant 3 section 4.6 -->

- The run records only. It writes the ledger and keeps `report_path` as its main report. It lists the ledger in `artifacts` only when the ledger is a tracked path (WC-4 keeps gitignored paths out of `artifacts`, `WORKER-CONTRACT.md:34`) [V]. Follow-ups alone never change `worker_status` from `succeeded`.
- **[REQ-12]** The return contract gains exactly three keys: `follow_up_ledger` (the path), `follow_up_counts` with `follow_up`, `note` and `show_user`, and `follow_up_capture_state` (`complete`, or `incomplete` with a reason). `follow_up_capture_state: incomplete` maps to `worker_status: partial`, added to the WC-4 status mapping. Because WC-4 enumerates the top-level keys (`WORKER-CONTRACT.md:33`) [V], each key is an edit to `core/WORKER-CONTRACT.md`; the old claim that the contract already allows extra keys was wrong. The coordinator duties name the three keys as things to read (the coordinator opens the contract, `WORKER-CONTRACT.md:39`) [V].
- `show_user` counts all three needs-your-decision groups (`consumer-unknown`, `unsettled`, `protected-risk-dispute`).
- Nested runs keep their own ledgers. A parent sees them only through the nested return contracts and never counts them twice.
- A possible safety finding graded non-blocking (GR12) makes the run `worker_status: partial`, is counted in `show_user`, and is named in the final report line. With no person reachable, the row is recorded and the run does not wait.
- A classifier verdict of SHOW_USER means the reviewer's own label stands and the row is tagged `unsettled`.
- Filing is done by the coordinator or the top-level session after the person says yes. Workers have no outward actions, and `/sc:issue` is on the never-as-worker list [V: `WORKER-CONTRACT.md:23`]. Workers also make no paid external judge call; external classifier experiments belong to the coordinator (section 7.8).
- The final report line states the counts, the ledger path, the capture state and "recorded only, no issue created".
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:478-486

````markdown
**[REQ-07]** One rule: `<run-report-dir>/qa/follow-ups.md` when the run has a QA directory, otherwise `<run-report-dir>/follow-ups.md`. The path is fixed before dispatch. Two exceptions:

| Primitive | Ledger | Note |
|---|---|---|
| task skill, tech-research (QA directory exists) | `<run-report-dir>/qa/follow-ups.md`, next to the consolidated findings [V: `R2/qa/` exists] | the task skill's **Follow-Up Items** path for out-of-scope findings (`task/SKILL.md:361` [V]) is absorbed |
| spec-panel, reflect and other runs without a QA directory | `<run-report-dir>/follow-ups.md` | the spec-panel Unattended section (`spec-panel.md:455-465`) gains one line [V that it has none today] |
| `/sc:implement` (exception) | keeps `notes.md`; the ledger holds a pointer row | `qa.md` has a closed list of interrupts and writes no ruling for minors-only replays [E]; no new question is added |
| pr-submit (exception) | keeps its own report-only list | its own tier router stays; `.dev/pr-monitor/` is gitignored (`.gitignore:250`) [V] and gitignored paths stay out of `artifacts` (`WORKER-CONTRACT.md:34`) [V] |

````

### tests/skills/test_review_severity_rule.py:371-385

````python
def test_h_implement_protocol_plugin_twins_byte_equal():
    plugin_root = "plugins/superclaude/skills/sc-implement-protocol/"
    files = sorted(p for p in _tracked_text() if p.startswith(plugin_root))
    assert files, "no plugin sc-implement-protocol files tracked"
    diff = [
        p
        for p in files
        if (_REPO / p).read_bytes()
        != (
            _REPO
            / "src/superclaude/skills/sc-implement-protocol"
            / p[len(plugin_root) :]
        ).read_bytes()
    ]
    assert not diff, f"plugin twins differ from src: {diff}"
````

### tests/skills/test_implement_severity_static.py:290-300

````python
# --- SPEC AC-11 (V1 F-11, V2 F-15): every halt/STOP/Ruling site classified ---
#
# blocking   reachable only while a blocking finding with a confirmed anchor is open
# stop-row   non-finding STOP row of the SKILL.md STOP table, or FR-019 items 5 and 6
# definition grammar, examples, the reason table, or a rule that writes nothing

_SITE = re.compile(r"\bhalt(s|ed|ing)?\b|E-HALT-QA|E-ARCHIVE-BLOCKED|\bRuling\b")

_ALLOW = [
    ("SKILL.md", "Load `refs/qa.md` fo", "definition"),
    ("SKILL.md", "| `E-HALT-QA` | A te", "stop-row"),
````

### tests/skills/test_reflect_input_snapshot.py:61-67

````python
def test_managed_delegate_ref_points_at_reflect_policy_and_mirror_matches():
    src = _REPO / "src/superclaude" / _MANAGED
    t = _read(src)
    assert "fresh dedicated per-run `--output` directory" in t
    assert "REFLECT_OUTPUT_ROOT" in t and "do not restate or reimplement" in t
    mirror = _REPO / "plugins/superclaude" / _MANAGED
    assert _read(mirror) == t
````

## Coverage slice

| Row | Spec line | Quote | Containment match | By hand |
|---|---|---|---|---|
| INF-015 | source.md:28 | The sweep call and the printed list moved from the task skill's "Post-Completion Validation (Final Phase Only)" to the final review step of `/sc:implement` | Task 3 (0.765) | Task 3 |
| INF-016 | source.md:28 | Record and print only: one read-only call, no `--promote`, no `--write`, no question. | Task 3 (0.857) | Task 3 |
| INF-017 | source.md:28 | `refs/qa.md` is not edited | Task 3 (1.0) | Task 3 |
| INF-018 | source.md:29 | tech-research keeps its ledger-writing edit (Task 4); no sweep, no offer | Task 4 (0.625) | Task 4 |
| INF-020 | source.md:30 | copied byte for byte in Task 3 | Task 3 (0.8) | Task 3 |
| INF-023 | source.md:36 | New Task 2 builds `follow_ups_cmd.py` (group `follow-ups`: `write`, `safety`, `sweep`, `summary`) and registers it. | Task 2 (0.769) | Task 2 |
| INF-024 | source.md:37 | Task 5 adds a test that the unattended commands make no GitHub call and ask no question. | Task 3 (0.636) | Task 5 |
| INF-035 | source.md:51 | Task 5 names `follow-ups summary` as the producer and Task 8 states the limit that no command emits the keys live yet. | Task 5 (0.8) | Task 5 |
| INF-036 | source.md:53 | for every finding you grade non-blocking under your current definition | Task 4 (1.0) | Task 4 |
