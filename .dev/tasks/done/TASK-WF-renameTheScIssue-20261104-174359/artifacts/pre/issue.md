---
name: issue
description: "Claim a GitHub issue on the origin repo (assign it, check its accuracy, write a summary and a next-step prompt, then stop) or create a templated issue with labels from a fixed set"
category: workflow
complexity: advanced
mcp-servers: [auggie, codegraph]
personas: [analyzer]
argument-hint: "--claim <number|url> | --create \"<description>\" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]"
---

# /sc:issue: GitHub Issue Claim and Create

Two modes on the repository that `origin` points at:

- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then stops. It never runs the next-step commands.
- `--create` turns a description into a GitHub issue built from one of four templates, with labels from a fixed set. GitHub only: no ClickUp task.

Both modes post directly to GitHub; nothing is shown for approval first.

For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`.

## Triggers

Explicit only: the user types `/sc:issue --claim ...` or `/sc:issue --create ...`.

## Usage

```text
/sc:issue --claim <number|url>
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

There is no repository option (the repo is always `origin`), no dry-run option and no preview option.

## STOP rules (checked before Activation)

- Exactly one of `--claim` / `--create` is required. Both or neither: STOP and print the Usage block.
- `--depth`, `--mode` or `--type` together with `--claim`: STOP `E-CREATE-ONLY-FLAG` ("--depth, --mode and --type apply to --create only").
- An unknown value for `--depth`, `--mode` or `--type`: STOP and list the allowed values from the Options table.
- An empty `--create` description (or an `@path` file that is empty or missing): STOP ("--create needs a description").
- An empty `--claim` argument: STOP and print the Usage block.

## Examples

```text
/sc:issue --claim 302
/sc:issue --claim https://github.com/<owner>/<repo>/issues/302
/sc:issue --create "The sync check misses deleted skill files" --mode bug --type cli --depth standard
/sc:issue --create @notes/new-command.md --depth deep
```

## Outputs

Every file starts from a template of the skill and stays under `.dev/issues/`:

| Mode | Directory | Files |
|---|---|---|
| claim | `.dev/issues/<N>/` | `scout.md`, `clickup.json`, `accuracy-check.md` (posted), `summary.md` (effort in hours), `analysis/` (only when the issue is out of date), `recommend.md`, `next-steps.md`, `claim-comment.md` (posted) |
| create | `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/`, renamed to `.dev/issues/<N>/` once the issue exists | `description.md`, `scout.md`, `flags.md`, `issue-body.md` (posted), `draft-notes.md`, and `create-review.md` (posted only when a standard or deep check disagrees with your flags) |

After a claim, open `.dev/issues/<N>/next-steps.md` and run its commands in your own session, in order, after the `/model` line it starts with.

## Boundaries

**Will:**
- Resolve the repository from the `origin` remote only.
- Spawn tier-pinned worker agents for every lookup, accuracy check and draft.
- Write every artifact under `.dev/issues/` from a template.
- On claim: assign the issue, assign the ClickUp task when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set, post or update the accuracy-check and claim comments, and stop after writing `next-steps.md`.
- On create: apply only the labels of the fixed set that already exist in the repo, and list the rest as not applied.

**Will Not:**
- Run any next-step command (brainstorm, design, workflow, implement, troubleshoot).
- Create labels, ClickUp tasks, or interact with any repository other than `origin`.
- Stage or commit `.dev/issues/`.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:issue-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in `~/.claude/skills/sc-issue-protocol/SKILL.md`.

## Related Commands

| Command | Difference |
|---|---|
| `/sc:recommend` | Picks the next-step chain that a claim writes into `next-steps.md` |
| `/sc:brainstorm`, `/sc:design`, `/sc:workflow`, `/sc:implement`, `/sc:troubleshoot` | The next-step commands a claim recommends; the user runs them |
