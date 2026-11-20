---
name: closeout
version: "1.0.0"
description: "Settle a merged pull request on the origin repo: check that it really merged, decide whether its issue is done and close it or leave it open with a note of what remains, and settle the work report entry and the worker's Orca task"
category: workflow
complexity: standard
mcp-servers: []
personas: [analyzer]
argument-hint: "<PR> [--issue <N>] [--dispatch <id>] [--entry-key <key>]"
---

# /sc:closeout: Settle a Merged Pull Request

After a pull request merged on the repository that `origin` points at, `/sc:closeout <PR>` settles three items and prints one fixed-shape result:

- **The issue.** A script reads the pull request state first; only a merged pull request goes on. Then the skill decides whether the issue is done by reading its own criteria against what the pull request and its linked pull requests delivered. A done issue is closed once, with a note that says why and who merged. An issue that is not done stays open with one short marked note of what remains, and the result hands the unmet criteria back to the orchestrator. A case it still cannot tell is escalated. The words `Fixes`, `Closes` and `Refs` decide nothing.
- **The work report entry** (through the orchestrator's report command) and **the worker's Orca task** (set to completed): each is settled, or escalated when its command or Run is not there.

Each item ends with a stated final status or an escalation that says why. "Completed" means merged; the word "deployed" is never written. `/sc:closeout` is for a person or the orchestrator, never a worker.

## Triggers

Explicit only: the user types `/sc:closeout <PR>`, or the orchestrator calls it after a merge.

## Usage

```text
/sc:closeout <PR> [--issue <N>] [--dispatch <id>] [--entry-key <key>]
```

## Options

| Argument | Required | Meaning |
|---|---|---|
| `<PR>` | yes | A pull request number (`661` or `#661`) or its URL on the origin repo; a URL for another repo is refused |
| `--issue <N>` | no | The issue to settle, when the pull request names none or more than one |
| `--dispatch <id>` | no | The worker's Dispatch id; used only to find the worker's task |
| `--entry-key <key>` | no | The work report entry key; default `<owner>__<repo>__<issue number>` |

## STOP rules (checked before Activation)

Print the usage block and stop, with no write, for: no `<PR>`; a `<PR>` that is neither a number nor a URL; an unknown flag; a flag with no value; a repeated flag; an `--entry-key` that holds anything but letters, digits, `_`, `.` and `-` (so a bad key never stops the run after the issue was already settled).

## Examples

```text
/sc:closeout 661
/sc:closeout https://github.com/<owner>/<repo>/pull/661
/sc:closeout 661 --dispatch <id> --entry-key <key>
```

## Outputs

One YAML result block, printed last and also after a stop (a stop of the skill, from its first wave on; a usage stop prints only the usage). It holds the verdict of the truth check, who merged, the status of the issue, the entry and the task, the unmet criteria when the issue is not done, and one fixed sentence for each escalation. The skill writes its working files (an evidence file and a verdict file) in a private temporary directory outside the checkout and nothing else on disk.

## Boundaries

**Will:**
- Resolve the repo from `origin` only and pass it on every `gh` call.
- Read the pull request state first and act only on `MERGED`.
- Decide whether the issue is done by reading its own criteria against what the pull request and its linked pull requests delivered, writing the verdict into the fixed-shape file.
- Close an open issue once, only after a `done` verdict, with a note that says why and names who merged, crediting people by name.
- Leave an issue that is not done open with one short marked note of what remains, and return the unmet criteria in the result for the orchestrator to continue the work.
- Escalate only a case it still cannot tell after investigating.
- Settle the entry and the task by read-then-write, or escalate with the reason.
- Print the result block last, also after a stop.

**Will Not:**
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

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:closeout-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in `~/.claude/skills/sc-closeout-protocol/SKILL.md` (the project `.claude/skills/sc-closeout-protocol/SKILL.md` copy in a dev checkout).

## Related Commands

| Command | Difference |
|---|---|
| `/sc:issue` | Claims or files an issue; `/sc:issue --plan <N>` is how the orchestrator updates a plan after a not-done result |
| `/sc:pr-submit` | Opens the pull request and fixes its review findings; `/sc:closeout` starts after the merge |
| `/sc:sweep` | A read-only snapshot of a Run and its worktrees; it changes nothing |
