# Settle reference: statuses, line shapes and fixed sentences

This is the one place that holds the status words, the closed sets of `how` and `why` tokens and the fixed sentences of the closeout. `scripts/settle.sh check` reads the escalation table below at run time, so keep the table format exact. It works with the adopted `scripts/branch-landed.sh`. The model never writes a status or an escalation sentence: every status comes from a table in a script, from the verdict word and the read-backs.

## 1. The four final status words

| Word | Meaning | Written by this run? |
|---|---|---|
| `settled` | The item is now in its final state because of this run. | yes |
| `already_final` | The item was already in its final state; nothing was written. | no |
| `none_found` | The surface was reachable and holds no record for this pull request, so there is nothing to settle. | no |
| `escalated` | The item could not be settled. A reason token and one sentence say why and give the one next step. | no |

`none_found` is a stated result, not a skip: it says the place was looked at. A surface that could not be looked at is `escalated`, never `none_found`. An issue that the done-check finds not done is `settled` with `how=left_open`, not `escalated`: it stays open with its one marked note, which is its final state for this run, and the result hands back to the orchestrator.

## 2. Line shapes and the closed sets of tokens

Each script step prints one stdout line: `<ITEM> <status> <key>=<value> ... how=<token>` or `... why=<token>`. No value holds a space. Details go to stderr. Exit 0 for `settled`, `already_final` and `none_found`; exit 1 for `escalated`; bad arguments print `SETTLE_FAIL <reason>` and exit 2.

| Line | Shape |
|---|---|
| `ISSUE` | `ISSUE <status> n=<N> links=<closing, refs or none> how=<token> note=<posted, already_there or none>`; `why=<token>` replaces `how=<token>` when escalated; a `settled` line with `how=left_open` ends with `remaining=<k>`; an `already_final` line may end with `reason=<state reason read as data>` |
| `ENTRY` | `ENTRY <status> key=<key> how=<token>` or `... why=<token>` |
| `TASK` | `TASK <status> id=<id> how=<token>` or `... why=<token>`; with `--dispatch` it carries `dispatch=<state read>` |
| `EVIDENCE` | `EVIDENCE ok prs=<k> comments=<c> events=<e> truncated=<yes or no> dir=<path>` or `EVIDENCE fail why=gh_failed` |
| `CHECK` | `CHECK ok` or `CHECK_FAIL <item>` |

Closed sets of `how` tokens: issue `closed_now`, `already_closed`, `left_open`; entry `moved`, `already_closed`, `issue_open`; task `completed`, `already_completed`, `already_failed`.

Closed sets of `why` tokens: issue `no_issue_named`, `several_issues`, `not_an_issue`, `issue_lookup_failed`, `no_verdict`, `unclear`, `reopened`, `note_failed`, `close_failed`; entry `surface_absent`, `entry_command_failed`; task `no_orca`, `no_orca_run`, `task_lookup_failed`, `write_failed`; for all three `merge_differs`; for any item `not_reached` (the skill sets it when the check fails an item). The evidence step alone also prints `gh_failed`.

The `note=` rule: it describes this run. `posted` means this run posted the note, `already_there` means a note with the marker was already on the issue when this run read it, `none` means no note was written or found. It is on every `ISSUE` line.

`--match differs` is checked first in every step, before any read or write: the step prints `escalated why=merge_differs` and writes nothing, also when a `done` verdict is passed and also when `--issue-open` is passed. `--issue-open` means the issue item did not end closed; the entry step then prints `already_final how=issue_open` and does not run the report command.

The task title uses the issue number `<N>` (the title is `<owner>/<repo>#<N>`); the task result text uses the pull request number `<PR>` (`merged <owner>/<repo>#<PR>`).

## 3. The escalation sentences

Each `why` token has one fixed sentence, so the same words come out whoever calls the scripts. The result lists it as `<item>: <sentence>`. For `unclear` the printing step follows the fixed sentence with the verdict's `unsettled` and `question` lines, so the one question for a person is named; those two lines are written by the model, the sentence is not.

| Item | `why` | Sentence |
|---|---|---|
| issue | `no_issue_named` | The pull request names no issue and none was passed. Run closeout again with `--issue <N>`. |
| issue | `several_issues` | The pull request names more than one issue. Run closeout again with `--issue <N>` for each. |
| issue | `not_an_issue` | The number given is a pull request. Run closeout again with the issue's number. |
| issue | `issue_lookup_failed` | The issue could not be read, so it was not checked and not changed. Run closeout again, or pass `--issue <N>` for a different issue. |
| issue | `no_verdict` | No usable done-check verdict was given, so the issue was not judged and not changed. Run closeout again (the skill writes the verdict). |
| issue | `unclear` | The done-check investigated and still could not tell whether the issue is done; the verdict lists what it checked and what could not be settled. The one question for a person follows. |
| issue | `reopened` | A person reopened the issue after the closeout's note. Closeout did not close it again. A person decides. |
| issue | `note_failed` | Posting the closing note failed, so the issue was not closed. Run closeout again. |
| issue | `close_failed` | The closing note is on the issue but closing the issue failed. Run closeout again (it closes the issue and posts no second note), or close it by hand: `gh issue close <N> --repo <owner>/<repo> --reason completed`. |
| entry | `surface_absent` | This install has no command that updates a work report entry. Check the entry for `<key>` by hand. |
| entry | `entry_command_failed` | The report entry command failed. Run it again by hand with `--key <key> --closed`. |
| task | `no_orca` | Orca is not available here, so the worker's task was not looked at. Settle it from a session that has the Run. |
| task | `no_orca_run` | No Orca Run is bound to this session, so the worker's task was not looked at. Settle it from the coordinator's session. |
| task | `task_lookup_failed` | The task could not be looked up. Run `orca orchestration task-list` in the coordinator's session and set it by hand. |
| task | `write_failed` | Setting the task failed. Set it by hand with `orca orchestration task-update --status completed`. |
| all three | `merge_differs` | The merge changed different files than the pull request held. Check it, then run closeout again. |
| any | `not_reached` | Closeout did not reach this item. Run closeout again. |

### The hand-back sentence

A `not_done` run is not an escalation, so its sentence has no `why` token and is not in the table. When `issue.handback` is `remaining`, `issue.handback_text` holds exactly this sentence, with the issue's number filled in by the printing step and nothing else changed:

The issue is not done and stays open with one note of what remains. The orchestrator takes the rest from here; by hand, run `/sc:issue --plan <N>` and start a worker on what remains.

`settle.sh check` does not read this sentence (it checks the three item lines); a test does.

## 4. The note's one sentence

The closing note carries one sentence, `--what`, written by the model: one plain sentence from the pull request's files, at most 25 words. Without `--what`, or when the sentence fails the title, name or dash checks of section 6, the script writes "`<n>` files changed." in its place.

## 5. Completed and deployed

- Completed means merged. It is the only status word this version writes for the issue and the task.
- Deployed means verified in the place it runs. This version never writes the word: no output of the skill or its scripts contains it. This file defines it so that nobody writes it by habit.
- What will count as a recorded check, for a later change the owner decides: a record that names what was checked (a health check or an installed version), where it runs, the result and the time in UTC, written by whoever ran it, in a file or comment the caller points to. The closeout would copy it and name its source. This version has no input for it.

## 6. The name rule and the matching rule

No output names the agent or the model, and the pull request title is never quoted. People are credited by name: the name on the merger's public profile, else the login; a merger that GitHub does not report is written "someone GitHub does not name".

`scripts/deny-names.txt` holds the names (it is the one accepted place that lists them). The script refuses a verdict file, and replaces a `--what` sentence, whose text holds a listed name, the target pull request's title (any letter case), or an em dash or an en dash. Matching rule for a name: case-insensitive, as a whole word; a name inside a path or file-name token (a run of letters, digits, underscore, dot, slash and hyphen that holds a slash, or a dot followed by a letter or digit, such as `skills/x.md` or `.config/settings.json`) is not a match, so a criterion that cites a repository path passes.

## 7. Known limits

These state what the scripts do today and change no behaviour.

- The issue lookup (`repos/<R>/issues/<N>` and the state read) depends on the REST request budget of the account that runs the closeout; when that budget is used up the item is `escalated why=issue_lookup_failed`.
- A merger's profile name may read like an organisation's name; the note uses it as GitHub gives it.
- The word for "released to production" has no runtime guard beyond the title, name and dash checks; the templates never write it and the model is told not to.
- `note=` describes this run only (section 2).
- A repeated run may add one more note when the account that runs the closeout does not pass the marker tests (its own note is then not read back as the marker); the approved sentence for that case is unchanged.
- The caps of the evidence step cut what they cut: `--limit 10` on the two pull request searches cannot show `truncated=yes` by itself.

## 8. UNVERIFIED items this file relies on

- U1: the first-word contract of `superclaude orchestrator report-entry --key <key> --closed` (`moved`, `already_closed`, `no_entry`, exit 0) is not written anywhere yet. The command does not exist in this repository, so the entry item is `escalated why=surface_absent` until it does. It is not tested against a real command.
- U3: the JSON field names of a task's title and status in `orca orchestration task-list --json` are not read from a real Run. A lookup that does not fit is `escalated why=task_lookup_failed`.
