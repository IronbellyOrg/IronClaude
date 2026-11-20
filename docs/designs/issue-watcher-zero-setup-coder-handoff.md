# Issue watcher zero setup: handoff to the Coder template maintainers

**Audience:** the maintainers of the Coder template (repository `IronbellyOrg/Coder`). **Source:** the zero-setup requirements of `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (rows R1, R6, R9, R10, R17, R20, R21) and Coder issues 515 (cron) and 516 (the coordinator). IronClaude builds the watcher side; the template must provide the rows below. Every value was read or run on 2026-11-18 or 2026-11-20 unless marked otherwise.

## 1. What the template must provide

| Row | Coder issue | What the template must do, with the value to use |
|---|---|---|
| R1 | none | Save the central defaults file of section 3 as `~/.config/superclaude/issue-watch-defaults.json` so no user writes one by hand. |
| R6 | 515 (https://github.com/IronbellyOrg/Coder/issues/515) | Install `cron`, start the daemon from `startup.sh` at every boot, and make the crontab of section 2 exist exactly once at every boot. |
| R9 | 516 (https://github.com/IronbellyOrg/Coder/issues/516) | For every project: a `Coordinator` branch, a `Coordinator` worktree and a running coordinator session, checked at boot and on every watcher run (section 4). |
| R10 | 516 | The watcher's worktree is the `Coordinator` worktree, path `/home/coder/workspaces/worktrees/<repo>/Coordinator`, created by Orca with an agent; its `origin` must equal the repository it serves. |
| R17 | 516 | Nothing manual. The session is named `COORD-<RepoName>` and starts from the standing prompt of section 5. |
| R20 | none | Open, not verified here: `orca worktree create --branch` suffixes a taken branch name (`Coordinator-2`), so using an existing remote `Coordinator` branch needs a verified method. Reproduction: in a repository that has a remote branch named `Coordinator`, run `orca worktree create --name Coordinator --branch Coordinator --agent claude --prompt "<task>"` and read the branch name with `git -C <path> branch --show-current`; a result other than `Coordinator` reproduces it. IronClaude has no remote `Coordinator` branch (checked with `git ls-remote`), so it takes the create path and is not affected today. |
| R21 | 515 | Cron's environment is only `PATH=/usr/bin:/bin` and no `~/.aienv`, so the entry sets `PATH` and uses full paths (section 2). |

## 2. The crontab

Tool locations checked on 2026-11-18 and found again on 2026-11-20: `/home/coder/.config/orca/linux-orca-cli-shim/orca`, `/home/coder/.local/bin/gh`, `/usr/local/bin/superclaude` (a link to `/opt/uv/tools/superclaude/bin/superclaude`), `/usr/local/bin/uv`, `/usr/bin/flock`. The folder `/home/coder/.aidev/logs` exists.

```cron
PATH=/home/coder/.local/bin:/usr/local/bin:/usr/bin:/bin
*/5 * * * * /usr/bin/flock -n /home/coder/.aidev/issue-watch.lock /usr/local/bin/superclaude issue-watch run-all --orca /home/coder/.config/orca/linux-orca-cli-shim/orca >> /home/coder/.aidev/logs/issue-watch.log 2>&1
```

Notes: `flock -n` makes a second entry exit at once while a sweep runs (the loop has its own lock too and exits 75). `--orca` is explicit because the Orca shim is not on cron's `PATH`; `gh` is found through the `PATH` line. `superclaude issue-watch run-all` exists only in a build that contains the zero-setup work: the `/usr/local/bin/superclaude` on this machine on 2026-11-20 does not list `run-all` yet, so the template must install a build that has it.

**`gh` login under cron's environment.** Run on 2026-11-20: `env -i HOME=$HOME PATH=/usr/bin:/bin /home/coder/.local/bin/gh auth status`. Result: `gh` stayed logged in (`Logged in to github.com account ironbelly`, token scopes `gist`, `project`, `read:org`, `repo`, `workflow`, exit 0). It reads the login from `$HOME/.config/gh/hosts.yml`, so the entry needs `HOME` (cron sets it) and no token variable. Orca listing under the same empty environment worked on 2026-11-18 (6 repositories).

## 3. The central defaults file

Content for the template to save at `~/.config/superclaude/issue-watch-defaults.json` (these equal the built-in values, so a missing file behaves the same; `projects` is optional and only needed for a repository with several Projects):

```json
{
  "approver_logins": ["ironbelly", "clayphi"],
  "trigger_label": "issue-watch:trigger",
  "approval_field": "Approved",
  "approval_option": "Yes",
  "allowed_owners": ["IronbellyOrg"],
  "projects": {}
}
```

## 4. The `Coordinator` branch and worktree rules

- When the repository has a `Coordinator` branch on the remote, switch to it; create it only when it does not exist (R20 above is the open question of how Orca does this).
- The worktree path is `/home/coder/workspaces/worktrees/<repo>/Coordinator`; its `origin` must name the repository (the sweep refuses a repository whose `origin` differs, reason `origin_mismatch`).
- The worktree is created through Orca with an agent. Check all three (branch, worktree, session) at boot and on every watcher run, and restart a stopped session.

## 5. The coordinator session

The session name is `COORD-<RepoName>`. Its standing launch prompt must state, as a standing owner authorization, that the coordinator carries the issue-pipeline duties of `~/.claude/WORKER-CONTRACT.md` section 4 ("Issue pipeline duties"). The duties include: adopt a claimed issue, start a worker for a level `none` claim, and, after a run ends `succeeded`, the coordinator-only completion update `superclaude issue-pipeline complete` that moves the Project Status to `In review` and posts one result comment. The Full Submit push rule: at Full Submit the launched agent pushes its own feature branch; the coordinator never pushes worker commits without the person's go.

## 6. The organization issue field `Approved`

The approval is the organization issue field `Approved` (single select, option `Yes`, visible to the organization members) that every workspace's approvers set. The template does not create it; the owner creates it once for the organization. The loop's per-repository check reports `approved_field_missing` for a repository whose organization lacks it, and the loop skips that repository.

## 7. Credentials

The launch-level guard is text-only, and the launch account is also an approver, so launched agents and workers should hold a token with no issues or projects write, or the watcher should run under a dedicated launch login. Until then the first-run report and `check-config` print `warning: approver_is_launch_account` when the approvers file holds the launch account.

## 8. Hosts must install guard version 2

The launch-level guard version stamp is 2. Each host runs `superclaude install --force` once after receiving the build; until then the hook script on the host is version 1.
