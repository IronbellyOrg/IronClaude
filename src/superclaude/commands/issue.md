---
name: issue
version: "1.1.0"
description: "Claim a GitHub issue on the origin repo (assign it, check its accuracy, write a summary and a next-step prompt, then create an Orca worktree and launch an agent in it) or create a templated issue with labels from a fixed set"
category: workflow
complexity: advanced
mcp-servers: [auggie, codegraph]
personas: [analyzer]
argument-hint: "--claim <number|url> [--pipeline worktree|full|none] [--submit] | --create \"<description>\" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]"
---

# /sc:issue: GitHub Issue Claim and Create

Two modes on the repository that `origin` points at:

- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` (the default) stops at a plan a human approves, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` creates the worktree and launches no agent. Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); when the worktree has no L2 pre-push layer it warns with `W-L2-ABSENT` and the launch continues (the L2 layer is not built yet). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. In `sc-issue-launch-level-hook.md`, section 7 (U1) requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 come from its sections 11 and 14.
- `--create` turns a description into a GitHub issue built from one of four templates, with labels from a fixed set. GitHub only: no ClickUp task.

Both modes post directly to GitHub; nothing is shown for approval first.

For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`.

## Triggers

Explicit only: the user types `/sc:issue --claim ...` or `/sc:issue --create ...`.

## Usage

```text
/sc:issue --claim <number|url> [--pipeline worktree|full|none] [--submit]
/sc:issue --create "<description>" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]
```

## Options

| Flag | Mode | Default | Values | Meaning |
|---|---|---|---|---|
| `--claim` | claim | - | issue number (`302`, `#302`) or issue URL on the origin repo | Claim this issue |
| `--create` | create | - | free text, or `@path` to a file holding the description | Description of the feature or bug |
| `--depth` | create | `quick` | `quick`, `standard`, `deep` | How hard the command checks the flags and fills the body |
| `--mode` | create | chosen by a worker when omitted | `feature`, `bug` | Picks the feature or bug template and the `enhancement` / `bug` label |
| `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; maps to a `type: <value>` label |
| `--pipeline` | claim | `worktree` | `worktree`, `full`, `none` | How far the launched agent goes. Every value creates the worktree; `none` launches no agent |
| `--submit` | claim | off | no value | Only with `--pipeline full`: the agent also commits, pushes a feature branch to `origin` and runs `/sc:pr-submit --monitor 3`. Never merges |

There is no repository option (the repo is always `origin`), no dry-run option and no preview option.

## STOP rules (checked before Activation)

- Exactly one of `--claim` / `--create` is required. Both or neither: STOP and print the Usage block.
- `--depth`, `--mode` or `--type` together with `--claim`: STOP `E-CREATE-ONLY-FLAG` ("--depth, --mode and --type apply to --create only").
- An unknown value for `--depth`, `--mode` or `--type`: STOP and list the allowed values from the Options table.
- An empty `--create` description (or an `@path` file that is empty or missing): STOP ("--create needs a description").
- An empty `--claim` argument: STOP and print the Usage block.
- `--pipeline` or `--submit` together with `--create`: STOP `E-CLAIM-ONLY-FLAG` ("--pipeline and --submit apply to --claim only").
- A `--pipeline` value that is not `worktree`, `full` or `none`, or `--pipeline` with no value: STOP and list those three values.
- `--submit` with a value, or without `--pipeline full`: STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full").

## Examples

```text
/sc:issue --claim 302
/sc:issue --claim https://github.com/<owner>/<repo>/issues/302
/sc:issue --claim 302 --pipeline none
/sc:issue --claim 302 --pipeline full
/sc:issue --claim 302 --pipeline full --submit
/sc:issue --create "The sync check misses deleted skill files" --mode bug --type cli --depth standard
/sc:issue --create @notes/new-command.md --depth deep
```

## Outputs

Every file starts from a template of the skill and stays under `.dev/issues/`:

| Mode | Directory | Files |
|---|---|---|
| claim | `.dev/issues/<N>/` | `scout.md`, `clickup.json`, `accuracy-check.md` (posted), `issue-summary.md` (effort in hours), `analysis/analyze-<scope>.md` (only when the issue is out of date), `recommend.md`, `next-steps.md`, `launch-prompt.md` (the launched agent's instructions; not written for `--pipeline none`), `claim-comment.md` (posted), `worktree.json` (the worktree path and launch record; never copied into the worktree) |
| create | `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/`, renamed to `.dev/issues/<N>/` once the issue exists | `description.md`, `scout.md`, `flags.md`, `issue-body.md` (posted), `draft-notes.md`, and `create-review.md` (posted only when a standard or deep check disagrees with your flags) |

After a claim, the launched agent works from `.dev/issues/<N>/launch-prompt.md` and `next-steps.md` in the worktree, in order, after the `/model` line `next-steps.md` starts with. With `--pipeline none` no agent is launched: open `.dev/issues/<N>/next-steps.md` and run its commands in your own session.

## Boundaries

**Will:**
- Resolve the repository from the `origin` remote only.
- Spawn tier-pinned worker agents for every lookup, accuracy check and draft.
- Write every artifact under `.dev/issues/` from a template.
- On claim: assign the issue, assign the ClickUp task when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set, post or update the accuracy-check and claim comments, create or reuse the Orca worktree `issue-<N>`, and (unless `--pipeline none`) launch one agent in it at the chosen level. Nothing is ever merged.
- On create: apply only the labels of the fixed set that already exist in the repo, and list the rest as not applied.

**Will Not:**
- Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself (the launched agent may, at the level the user chose).
- Create labels, ClickUp tasks, or interact with any repository other than `origin`.
- Stage or commit `.dev/issues/`.
- Pass an Orca link flag.
- Merge anything.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:issue-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in `~/.claude/skills/sc-issue-protocol/SKILL.md`.

## Related Commands

| Command | Difference |
|---|---|
| `/sc:recommend` | Picks the next-step chain that a claim writes into `next-steps.md` |
| `/sc:brainstorm`, `/sc:design`, `/sc:workflow`, `/sc:implement`, `/sc:troubleshoot` | The next-step commands a claim recommends; the launched agent runs them at the chosen level, or you run them after `--pipeline none` |
