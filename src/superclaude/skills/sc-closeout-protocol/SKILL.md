---
name: sc:closeout-protocol
description: "Behavioral protocol for /sc:closeout: after a pull request merged on the origin repo, settle its three items, the issue, the work report entry and the worker's Orca task. A script checks that the pull request really merged, the skill's own session decides whether the issue is done and writes a verdict, and scripts do every write with a read before it. Each item ends with a stated final status or an escalation that says why. Never leave an item silently in progress."
allowed-tools: Read, Write, Edit, Bash
---

<!-- Extended metadata (for documentation, not parsed):
category: workflow
complexity: standard
mcp-servers: []
-->

# /sc:closeout protocol

> Adapted from Jay Wedgeworth's `skills/closeout/SKILL.md` at https://github.com/Simple-With-Us/AI-Fleet-Coordinator (commit ec86182d70d5a77410774392439090f1e36ca367, 2026-11-05), Copyright 2026 Jay Wedgeworth, licensed under the Apache License, Version 2.0.
> Changed by IronClaude: see `PROVENANCE.md`.

The command (`~/.claude/commands/sc/closeout.md`) has already validated the arguments: `<PR>` (a number, `#number` or a URL of the origin repo) and the optional `--issue <N>`, `--dispatch <id>` and `--entry-key <key>`. This skill runs after a merge, from a checkout of the origin repo, and settles three items for that pull request:

1. **The issue.** A model (this session) decides whether the issue is done and writes a verdict file; only a `done` verdict closes the issue. A `not_done` verdict leaves it open with one marked note of what remains and hands the unmet criteria back to the caller in the result. An unclear case is escalated.
2. **The work report entry.** Settled only through `superclaude orchestrator report-entry`, or escalated when that command is absent.
3. **The worker's Orca task.** Set to completed, or escalated when Orca or its Run is not there.

Every status comes from a table in a script, from the verdict word and the read-backs. The words `Fixes`, `Closes` and `Refs` are read as data and decide nothing.

`<skill base>` below is the directory that holds this `SKILL.md` (`~/.claude/skills/sc-closeout-protocol/` when installed; the project `.claude/skills/sc-closeout-protocol/` copy in a dev checkout). Read other skill files from the installed copy first and from the project copy second.

## Files of this skill

| Path (skill-relative) | Loaded or used |
|---|---|
| `LICENSE` | Apache License 2.0 of the two adopted files, kept verbatim |
| `PROVENANCE.md` | the source files, their commits and hashes, and what changed (kept as is, changed or dropped) |
| `refs/settle.md` | wave 2 and wave 3: the status tables, the closed `how` and `why` tokens, the escalation sentences, the hand-back sentence, the note's one sentence, "completed" and "deployed", the names rule |
| `refs/done-check.md` | wave 2 (b) only: how the model reads the evidence and writes the verdict |
| `refs/result.md` | wave 3: the result block, the check, the hand-back copy rules, how the orchestrator calls the scripts |
| `templates/closing-note.md` | rendered by `scripts/settle.sh issue` for a `done` verdict (the note on the issue) |
| `templates/done-verdict.md` | wave 2 (b): the stub the model copies and fills in |
| `templates/not-done-note.md` | rendered by `scripts/settle.sh issue` for a `not_done` verdict |
| `templates/result.md` | wave 3: the fixed shape of the printed result block |
| `scripts/branch-landed.sh` | wave 1: the truth check (adopted from Jay Wedgeworth) |
| `scripts/settle.sh` | wave 2 and wave 3: the issue, evidence, entry, task and check steps |
| `scripts/deny-names.txt` | data read by `scripts/settle.sh`: the names no output may contain |

Every output file starts as a copy of its template (stub first) and is filled in place.

## Repository and GitHub call rules

- `<R>` is the `origin` repo, and nothing else is consulted: not `gh repo set-default`, not the fork-parent default, not a `--repo` flag of the command (there is none). Every `gh` call in the scripts names `--repo <R>`; this skill makes no `gh` call of its own except `gh auth status`.
- Nothing is ever pushed to, fetched from or opened against any repo other than `origin`. The only fetch is the one inside `scripts/branch-landed.sh`.
- This skill's session writes one file and nothing more: `done-verdict.md` in the private temporary directory that `settle.sh evidence` makes (outside the checkout, so `git status` stays unchanged). Every write to GitHub or Orca is made by `scripts/settle.sh` (a note, a close, a task update) after a read.
- Completed means merged. Deployed means verified in the place it runs. This version never writes the word "deployed": no output of this skill or its scripts contains it, and a later change needs a recorded check (`refs/settle.md`).
- People are credited by name (their profile name, else their login). The agent and the model are never named, and the pull request title is never quoted.
- The tools of this skill are `Read, Write, Edit, Bash`. The model's reading is bounded by a script: `settle.sh evidence` writes one file of fixed size (at most 30 comments, 10 pull requests, 100 file names each, 100 timeline events), and "read that file and `refs/done-check.md` and nothing else" is an instruction to this session, not a lock.
- Plain English, no em or en dashes, no secret printed or written.

## Waves

Run the waves in order. `<PR>` is the pull request number (the command gave it as a number, `#number` or a URL of the origin repo; use the number). `<N>` is the issue number.

1. **Wave 0, intake.** Read the arguments the command validated. Resolve `origin` (`git remote get-url origin`; no origin or a remote that is not GitHub is STOP `E-NO-ORIGIN`, and a URL naming another repo is STOP `E-FOREIGN-REPO`). Run `gh auth status` (failure is STOP `E-GH-AUTH`, before any other call). Check that `jq` is on the path (missing is STOP `E-NO-JQ`).
2. **Wave 1, truth check.** Run `<skill base>/scripts/branch-landed.sh <PR>` and keep its one line. Only `MERGED` goes on. Any other verdict (`OPEN`, `CLOSED`, `NONE`, `UNKNOWN`) is STOP `E-NOT-MERGED` with the verdict in the message: nothing is written, and the run ends with the result block, status `stopped`. Keep the `match=` value (`same`, `differs` or `unchecked`), the merger (`by=`), the merge commit and the base branch for the later steps and the block.
3. **Wave 2, settle.** `<M>` below is the `match=` value, passed as `--match <M>` to every step. With `differs` each step prints `escalated why=merge_differs` and writes nothing, so the rule lives in the script. A step that escalates does not stop the next one.
   - **(a) The find pass.** `<skill base>/scripts/settle.sh issue <PR> [--issue <N>] --match <M>` with no `--verdict`. Its line either ends the issue item (closed issue, a marker note, reopened, no issue, `merge_differs`) or says `why=no_verdict` with `n=<N>` for an open issue, which means the done-check is needed.
   - **(b) The done-check, only when (a) said `no_verdict` for an open issue and `<M>` is not `differs`.** Run `<skill base>/scripts/settle.sh evidence <PR> --issue <N>`; its `EVIDENCE` line gives `dir=<path>`, a private temporary directory outside the checkout. Read `<dir>/evidence.md` and `refs/done-check.md` and nothing else, and run no `gh` or `git` command of your own. Copy `templates/done-verdict.md` to `<dir>/done-verdict.md` (stub first), investigate, and fill it in place, listing what you checked in every verdict. Then run `settle.sh issue <PR> --issue <N> --verdict <dir>/done-verdict.md --dir <dir> --match <M> --what "<one plain sentence>"`, where the sentence follows the note rule of `refs/settle.md` (about the pull request's files, 25 words at most, no title, no name, no dash). When `evidence` prints `EVIDENCE fail why=gh_failed` there is no verdict file to write: make the next `issue` call without `--verdict`, which gives `no_verdict`, and do not retry the reads.
   - **(c) Entry and task.** Run `settle.sh entry --key <key> [--issue-open] --match <M>` and `settle.sh task [--dispatch <id>] --match <M>`. `<key>` is `--entry-key` when given, else `<owner>__<repo>__<N>`. Pass `--issue-open` when the issue item did not end closed (`left_open`, `unclear`, `no_verdict`, `reopened` or any escalation); `--match differs` is still checked first. Pass `--dispatch` when it was given to the command. When no issue number exists (`no_issue_named`, `several_issues`, `not_an_issue` or `issue_lookup_failed`), the entry item is not reached unless `--entry-key` was given and the task item is not reached unless `--dispatch` was given: set such an item to `escalated why=not_reached` yourself (sentence in `refs/settle.md`).
4. **Wave 3, check and return.** Load `refs/result.md` and `templates/result.md`. Run `<skill base>/scripts/settle.sh check`, giving it the three item lines (`ISSUE`, `ENTRY`, `TASK`) on standard input. On `CHECK_FAIL <item>` set that item to `escalated why=not_reached` and the result status to `partial`; never print an item with no final status. Print the one result block of `templates/result.md`, filled in. For an issue line `settled ... how=left_open`, copy the hand-back values as `refs/result.md` says (`issue.remaining[]` from the unmet criteria of the verdict file, `issue.remaining_file`, `issue.handback_text`) and leave the temporary directory in place; do not delete it.

## Return contract

Print the result block last, also after a stop. It is printed from wave 0 on: a STOP in wave 0 or wave 1 prints the block with `status: stopped`, the STOP code in `stop`, and `null` in the three item fields (the exact rules are in `refs/result.md`). A usage stop of the command (a bad or missing argument) prints only the usage, before this skill starts, and no block. The block is the only output: there is no second summary. `status: complete` means no item is `escalated`; `partial` means at least one is, and each has its fixed sentence in `escalations`; `stopped` means the verdict is not `MERGED` or a STOP code fired. The block never names the agent or the model.

## Error handling

| Scenario | Behavior |
|---|---|
| Bad or missing arguments | The command STOPs with usage before Activation; no block |
| No `origin`, or `origin` is not GitHub | STOP `E-NO-ORIGIN` |
| A URL naming another repo | STOP `E-FOREIGN-REPO` |
| `gh auth status` fails | STOP `E-GH-AUTH`, before any other call |
| `jq` missing | STOP `E-NO-JQ` |
| Verdict `OPEN`, `CLOSED` (closed without merge), `NONE` or `UNKNOWN` (`gh_failed`, `bad_json`) | STOP `E-NOT-MERGED` with the verdict in the message; no write; status `stopped` |
| No issue qualifies (`ISSUE escalated why=no_issue_named`) | Code `E-NO-ISSUE`, not a stop: nothing is written to any issue; entry and task are not reached unless `--entry-key` or `--dispatch` was given |
| `why=several_issues`, `why=not_an_issue`, `why=issue_lookup_failed` | Not a stop: the issue item is `escalated`, nothing is written to the issue, the sentence is in `refs/settle.md` |
| The done-check gives `not_done` | Not an escalation: `ISSUE settled how=left_open remaining=<k>`, one marked note, the issue is never closed; the block hands back (`issue.handback: remaining`); the task is still settled; the entry gets `--issue-open` |
| `why=unclear` (verdict `unclear_escalate`) or `why=no_verdict` (no usable verdict) | Not a stop: the issue item is `escalated`, nothing is written to the issue; the task is still settled; the entry gets `--issue-open` |
| `why=reopened`, or `why=issue_lookup_failed` from the reopen guard or the permission lookup of a marker's author | Not a stop: the issue item is `escalated`, nothing is written; the entry gets `--issue-open` |
| `match=differs` (`why=merge_differs`) | Not a stop: all three items are `escalated`, nothing is written, status `partial` |
| `why=note_failed` (the note was not posted or its marker was not read back) | Not a stop: the issue is not closed; the other two items still run |
| `why=close_failed` | Not a stop: one note is on the open issue; a rerun closes it and posts no second note |
| Entry: `why=surface_absent` or `why=entry_command_failed` | Not a stop: that item is `escalated` with its sentence |
| Task: `why=no_orca`, `why=no_orca_run`, `why=task_lookup_failed` or `why=write_failed` | Not a stop: that item is `escalated` with its sentence |
| `settle.sh check` prints `CHECK_FAIL <item>` | Set that item to `escalated why=not_reached`, status `partial` (`why=not_reached` is also the value for an item wave 2 did not reach) |
| `settle.sh` prints `SETTLE_FAIL <reason>` (exit 2, bad arguments or a directory that cannot be made) | Treat the item as `escalated why=not_reached` and print the reason in `escalations` |

## Will Do

- Resolve the repo from `origin` only and pass it on every `gh` call.
- Read the pull request state first and act only on `MERGED`.
- Decide whether the issue is done by reading its own criteria against what the pull request and its linked pull requests delivered, writing the verdict into the fixed-shape file.
- Close an open issue once, only after a `done` verdict, with a note that says why and names who merged, crediting people by name.
- Leave an issue that is not done open with one short marked note of what remains, and return the unmet criteria in the result for the orchestrator to continue the work.
- Escalate only a case it still cannot tell after investigating.
- Settle the entry and the task by read-then-write, or escalate with the reason.
- Print the result block last, also after a stop.

## Will Not Do

- Merge, push, commit, stage or delete a branch or a worktree.
- Use commit ancestry or a two-dot diff.
- Decide whether an issue is done by matching the words `Fixes`, `Closes` or `Refs`.
- Write a status or an escalation sentence, or run a `gh` command of its own while judging (it reads the evidence file only).
- Close an issue that is already closed or that a person reopened after its note.
- Write the word "deployed".
- Edit or delete any comment or text on GitHub, or reopen an issue.
- Release, stop, abandon or message a worker or its Dispatch.
- Start the work that a not-done issue still needs (a worker, a plan or a Dispatch) or count rounds of hand-backs.
- Write a report file by hand.
- Name the agent or the model, or quote the pull request title.
- Ask the person a question.
- Start a worker agent.
- Pass an Orca link flag, or call `orca` anywhere but in `settle.sh task`.
- Print or write a secret.
