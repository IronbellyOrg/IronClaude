# The result block, the check, and how the orchestrator calls the scripts

Loaded in wave 3 of `SKILL.md`. The fixed shape is `templates/result.md`; this file says what each field holds. The status tables, the closed `how` and `why` tokens and the fixed sentences are in `refs/settle.md`.

## The block

Print one YAML block last, also after a stop. It is the only output; there is no second summary. The block never names the agent or the model.

| Field | Value |
|---|---|
| `closeout.pr` | the pull request number, or `null` when no number was read |
| `closeout.status` | `complete`, `partial` or `stopped` (below) |
| `closeout.verdict` | `MERGED`, `OPEN`, `CLOSED`, `NONE` or `UNKNOWN`: the token of `scripts/branch-landed.sh` |
| `closeout.merged_by` | the merger's profile name, else the login, else `null` |
| `closeout.merge_commit` | the first 7 characters of the merge commit, or `null` |
| `closeout.match` | `same`, `differs` or `unchecked` from the `MERGED` line, else `null` |
| `closeout.pr_links_issue` | the `links=` value of the `ISSUE` line: `closing`, `refs` or `none`; `null` when there is no `ISSUE` line |
| `closeout.issue` | `number`, `status`, `detail`, `note`, `handback`, `remaining_file`, `remaining`, `handback_text` (below) |
| `closeout.entry` | `key`, `status`, `detail` |
| `closeout.task` | `id`, `status`, `detail`, `dispatch` |
| `closeout.escalations` | one string per escalated item: `"<item>: <the fixed sentence>"` |
| `closeout.stop` | the STOP code, or `null` |

`status` of an item is one of the four words `settled`, `already_final`, `none_found`, `escalated` (`refs/settle.md`). `detail` is the `how` or `why` token of its line. `issue.note` is the `note=` value of the `ISSUE` line: `posted` (this run posted the note, the done note or the not-done note), `already_there` (a note with the marker was already on the issue), `none` (no note was written or found) or `null` (the run stopped before the issue item). `task.dispatch` is the `dispatch=` value of the `TASK` line, or `null`.

An `escalations` entry is the fixed sentence from `refs/settle.md` for its `why` token. For `why=unclear` the sentence is followed by the verdict's `unsettled:` and `question:` lines, copied as they are; they are the only text in the block that the model wrote.

## complete, partial, stopped

- `complete`: no item is `escalated`.
- `partial`: at least one item is `escalated`, and each has its sentence in `escalations`.
- `stopped`: the verdict is not `MERGED`, or a STOP code fired. No item was written, the `status`, `detail` and other fields of the three items print `null` (the `remaining` list prints `[]`), and `stop` says why. The block is printed from wave 0 on: a STOP in wave 0 or wave 1 prints it. A STOP in wave 0 happens before any verdict exists, so `verdict` is `UNKNOWN` there. A usage stop of the command prints only the usage, before this skill starts, and no block.

## The check

Before printing, run `settle.sh check` with the three item lines (`ISSUE`, `ENTRY`, `TASK`) on standard input. It prints `CHECK ok` when each item has a status word and every `escalated` line has a `why` token that has a sentence in `refs/settle.md`. Otherwise it prints `CHECK_FAIL <item>` and exits 2: set that item to `escalated` with `why=not_reached`, put its sentence in `escalations`, set `status` to `partial`, and write `note: none` for the issue item (a `not_reached` item has no note; the same holds for an item you set to `not_reached` yourself in wave 2). An item is never silent.

Two rules apply to every item step. `--match differs` is checked first, before any read or write, so it also wins over a `done` verdict and over `--issue-open`. `--issue-open` means the issue item did not end closed, and then the entry item is `already_final` with `how=issue_open` and the report command is not run.

## The hand-back (when the issue item is `settled` with `how=left_open`)

Copy these values with no judgment from the `ISSUE` line and from the verdict file the script already checked:

- `issue.handback: remaining`. Every other issue line, a `done` and its close, an issue that was already closed, a rerun after a failed close and an escalation of any kind (`unclear` included), prints `none`; a run that stopped before the issue item prints `null`.
- `issue.remaining_file` is the path of `done-verdict.md` in the private temporary directory (the `dir=` of the `EVIDENCE` line). It is `null` when `handback` is not `remaining`.
- `issue.remaining` has one line for each criterion whose delivered word in the verdict file is `partly` or `not_delivered`, in the order of the file, with no cap (the comment lists at most 10; the block lists all). A line is `<criterion> (delivered in part by PR #<n>)` or `<criterion> (no pull request yet)`. The number of lines equals the `remaining=<k>` value of the line. It is `[]` when `handback` is not `remaining`.
- `issue.handback_text` is the hand-back sentence of `refs/settle.md` with the issue number filled in and nothing else changed. It is `null` when `handback` is not `remaining`.

The skill does not delete the temporary directory (the operating system's temporary space does). A caller that needs the criteria later copies them into its own state at once. The skill starts no worker, writes no plan and counts no rounds: a rerun that finds the issue still not done returns the same unmet criteria again.

## How the orchestrator calls the scripts directly

The orchestrator may call the skill (`Skill sc:closeout-protocol`), which is the normal way. If a skill inside a skill does not work, it may run the scripts itself in this order, from a checkout of the origin repo. Each line prints one stdout line; `<S>` is the directory `~/.claude/skills/sc-closeout-protocol/scripts/` (the project `.claude/skills/sc-closeout-protocol/scripts/` copy in a dev checkout).

```text
<S>branch-landed.sh <PR>                                                        one line, exit 0 only for MERGED
<S>settle.sh issue <PR> [--issue N] [--match M]                                 the find pass: no --verdict, one line
<S>settle.sh evidence <PR> --issue N                                            one line with dir=D; writes the evidence file (read only)
<S>settle.sh issue <PR> --issue N --verdict F --dir D [--what TEXT] [--match M] one line
<S>settle.sh entry --key <key> [--issue-open] [--match M]                       one line
<S>settle.sh task <PR> [--issue N] [--issue-done] [--dispatch ID | --title T] [--match M]  one line
<S>settle.sh check                                                              reads the three lines on standard input
```

Between `evidence` and the second `issue` call the caller must itself do what the skill does: read the evidence file following `refs/done-check.md`, write the verdict file from `templates/done-verdict.md` in the directory `D` that `evidence` named, and pass `--verdict` and `--dir`. Without a verdict file the issue item is `escalated why=no_verdict` and nothing is written; a verdict is never invented. `--match` carries the `match=` value of the `MERGED` line. `task` takes the pull request number (its result text is `merged <owner>/<repo>#<PR>`) and finds the worker's task by `--dispatch` (completed whatever the verdict), else by `--title`, else by the title `<owner>/<repo>#<N>` built from `--issue`; with none of the three it prints `SETTLE_FAIL usage`. A title lookup runs only with `--issue-done`, which the caller passes when the `ISSUE` line is `settled how=closed_now` or `already_final how=already_closed` with `note=posted` or `note=already_there`; otherwise it prints `TASK escalated why=not_reached` and chooses no task. The title must match exactly one task that is not yet final: none is `none_found`, several are `escalated why=task_lookup_failed`.
