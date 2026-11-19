# Upgrading to IronClaude 6.1.0

This page is for anyone who already has IronClaude 6.0.0 installed and wants
6.1.0. The same steps apply to an older 5.0.0 install and to a 4.x install
(including the untagged 4.3.5); the parts that only matter there are marked
"from 5.0.0" or "from 4.x". For a first install, see the
[Installation Guide](installation.md).

6.1.0 removes the task-file route and the document skills built on it: nine
skills (`task`, `task-builder`, `roadmap`, `prd`, `tdd`, `tech-research`,
`tech-reference`, `operational-guide`, `readme`) and the `/sc:tdd` command.
Plan work with `/sc:workflow`, then run the plan with `/sc:implement`. It keeps
`/sc:task`, `/sc:validate-tests` and all eight `rf-*` agents. The upgrade
therefore does more than copy new files: the installer removes the installed
copies of the removed command and skills, and it saves a copy of a command,
rule or output-style file before it overwrites one that differs. The full list
of changes is in the [6.1.0 release notes](../releases/v6.1.0.md).

From 5.0.0 you also get the 6.0.0 changes (six `superclaude` command groups,
twelve slash commands and five skills removed; see the
[6.0.0 release notes](../releases/v6.0.0.md)). From 4.x you also get the 5.0.0
changes: codegraph replaces codebase-memory-mcp and Serena, session memory
moves to plain files, and the upgrade installs codegraph and removes the old
MCP registrations IronClaude wrote (see the
[5.0.0 release notes](../releases/v5.0.0.md)). The 6.0.0 to 6.1.0 upgrade was
run for 6.1.0 (see
[the end-to-end record](../testing/v6.1.0/post-release-report.md)). The 5.0.0
to 6.0.0 upgrade was run for 6.0.0 (see
[its record](../testing/v6.0.0/post-release-report.md)), and the 4.x steps were
tested for 5.0.0. Neither was re-run straight to 6.1.0.

## Before you start

You need:

- the Claude Code CLI `claude` on `PATH` (`claude --version` must work);
- network access to GitHub, to install the package and download codegraph;
- Linux or macOS on x64 or arm64 for the automatic codegraph download (on any
  other platform the install exits 1 unless a `codegraph` that prints `1.6.2`
  is already on `PATH` or in `~/.local/bin`);
- `pipx` (or pip: see the Management section of [Installation](installation.md)).

Without `claude` or the network, the codegraph step fails and the command
exits 1. See [If the codegraph step fails](#if-the-codegraph-step-fails).

## Step 1: Back up files you edited

`superclaude install --force` overwrites every file IronClaude ships. Whether
your edited copy is saved first depends on the kind of file:

| In `~/.claude/` | If your copy differs from the shipped one |
|-----------------|-------------------------------------------|
| Commands (`commands/sc/`), rules (`rules/`) and output styles (`output-styles/`) | A copy is saved next to it as `<name>.bak.<UTC time>` (for example `analyze.md.bak.20261118T170151Z`) before the file is overwritten. See [Saved copies](#saved-copies-of-changed-files). |
| Core files (`CLAUDE.md`, `RULES.md` and the other core `.md` files), agents (`agents/`) and skill folders (`skills/`) | Overwritten with no copy. Each shipped skill folder is deleted and copied again, so any file you added inside one is lost. |
| `settings.json` | Backed up as `settings.json.bak.<timestamp>` before the installer merges its entries, on every run. |

Copy anything you changed in the second row first, for example:

```bash
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine
cp ~/.claude/RULES.md ~/.claude/RULES.md.mine
```

Re-apply your changes after the upgrade.

## Step 2: Upgrade the package and the installed files

```bash
pipx install --force git+https://github.com/IronbellyOrg/IronClaude
superclaude install --force
```

To install exactly this release rather than the latest commit, use
`git+https://github.com/IronbellyOrg/IronClaude@v6.1.0` in the first command.

Use `superclaude install --force`, not the other two install commands:

| Command | Refreshes existing files | Installs codegraph | Retires old MCP registrations | Removes the commands, skills and agents 6.1.0 no longer ships |
|---------|--------------------------|--------------------|-------------------------------|------------------|
| `superclaude install` | No, skips files that already exist (it names the kept files that differ) | Yes | Yes | Yes |
| `superclaude update` | Yes | No | No (it only prints a notice when a legacy registration is present) | Yes |
| `superclaude install --force` | Yes | Yes | Yes | Yes |

If you already upgraded with `superclaude update`, run
`superclaude install --force` now: `update` does not install codegraph.

### From a clone

In an IronClaude clone, check out the release first, then run `./update.sh`:

```bash
git fetch origin --tags
git checkout v6.1.0
./update.sh
```

`update.sh` installs whatever is checked out in that folder, not the latest
release: it runs `pipx install --force ./`, then `superclaude install --force`,
`make sync-dev` and `superclaude doctor`. It needs `pipx` and `make` on `PATH`;
without `pipx` it stops at that first command (exit 127). Install pipx with
`uv tool install pipx` or your distribution's `pipx` package.

## What the upgrade does

`superclaude install --force` runs these steps in order:

1. Refreshes the framework files in `~/.claude/`: 12 core files, 34 commands,
   48 agents, 26 skills, hooks, templates, rules and output styles, and merges
   its hook entries into `~/.claude/settings.json`. A command, rule or
   output-style file that differs from the shipped one is saved as
   `<name>.bak.<UTC time>` first.
2. Installs codegraph 1.6.2: downloads the release for your platform, checks its
   SHA-256, extracts it under `~/.codegraph/`, links `~/.local/bin/codegraph`
   and registers it as a user-scope MCP server.
3. Retires old MCP registrations at user scope. It removes the
   `codebase-memory-mcp` and `serena` entries IronClaude can prove it wrote.
   Once codegraph is ready it also removes the `codebase-memory-mcp` entry that
   points at `~/.local/bin/codebase-memory-mcp` and any uncustomised Serena
   launcher (a stdio entry that runs `start-mcp-server` with no `env` or
   `headers`), whatever user-scope name it is registered under, except
   `serena-local`. A `codebase-memory-mcp` or `serena` entry it keeps is
   reported as `<name>: kept: <reason>`; only a legacy Serena entry kept until
   codegraph is ready also prints `claude mcp remove serena --scope user`.
   Other user-scope entries are left alone without a message. The removal
   commands are under [What stays on purpose](#what-stays-on-purpose).
   Each `claude` call has 10 seconds and the
   whole step 15 seconds, and nothing in this step changes the exit code.
4. Retires the commands, skills and agents this release no longer ships:
   removes the installed copies it can prove it installed and keeps (and
   explains) any copy you changed. See
   [Commands, skills and agents a release no longer ships](#commands-skills-and-agents-a-release-no-longer-ships).

The MCP retire step (item 3) never touches:

- a Serena registered under the name `serena-local`;
- local-scope registrations or a project's `.mcp.json`;
- binaries, uv tools, indexes, caches or memories;
- a registration you customised with its own `env` or `headers`.

### Expected output

In the end-to-end upgrade test from 4.3.5, the codegraph and retire steps
printed (temporary paths shortened to `~`):

```text
📦 Installing codegraph (required user-level phase)...
installed codegraph 1.6.2 (SHA-256 verified) at ~/.codegraph/versions/v1.6.2
Registration: exact user stdio entry verified (codegraph 1.6.2 at ~/.codegraph/versions/v1.6.2/bin/codegraph). Restart Claude sessions to load it; no indexing or live MCP handshake was performed.

📦 Retiring stale MCP registrations...
   Retired MCP registrations (user scope only):
   Removed the codebase-memory-mcp user registration (codegraph is ready: kind-B registration (binary and companions stay))
   Removed the serena user registration (Tier R row (c): serena start-mcp-server --context ide-assistant --project '$(pwd)')
   Restart running Claude sessions; a running session can write the entry back. Check with `superclaude install --list`.
```

It then printed the manual cleanup commands listed under
[What stays on purpose](#what-stays-on-purpose). Which lines you see depends on
what was registered before the upgrade.

### If the codegraph step fails

The framework files are already refreshed when the codegraph step runs. If it
fails (no network, `claude` missing, or an unsupported platform), the command
prints the failed stage, still runs the retire step, and exits 1. Fix the cause
and run `superclaude install --force` again; the codegraph step only repairs what
differs. The failure table is in the
[MCP Installation Guide](../user-guide/mcp-installation.md#if-the-codegraph-phase-fails).

## Step 3: Restart Claude sessions

Restart every running Claude Code session. MCP servers and skills load at
session start, and a running session can write a removed registration back.

If you use ccsession, restart its shim too, because a running shim keeps the old
behaviour. Run this only when no ccsession session needs the shim, because it
stops the shim for every running session; the next `ccsession` launch starts a
new one:

```bash
pkill -f local-gateway-alias-proxy.py
```

## Step 4: Check the result

```bash
superclaude --version          # prints: SuperClaude, version 6.1.0
superclaude install --list     # read-only; ends with the codegraph and retired-registration blocks
superclaude doctor --verbose
```

Check that:

- the `codegraph MCP` block of `superclaude install --list` shows a
  `User registration:` line that is not `absent` (after a clean upgrade it reads
  `matches`) and ends with `Ready for Serena retirement: yes`;
- the `Retired MCP registrations (user scope):` block lists
  `codebase-memory-mcp` and `serena` as `absent`, or as kept with a reason;
- `superclaude doctor --verbose` ends with `✅ SuperClaude is healthy` and prints
  no `no codegraph registration` line. Plain `superclaude doctor` passes even
  when codegraph is missing, so use `--verbose`.

Then, in a new Claude Code session, run `/sc:graph status`. It reports the
code-graph index state of that folder and the next action to take.

## What stays on purpose

### codebase-memory-mcp binary and companions

The retire step removes only the registration. The codebase-memory-mcp binary
and the client companions its own installer added stay. After the end-to-end
upgrade from 4.3.5 (run for 5.0.0), `superclaude doctor --verbose` counted 48
agents and 39 skills (including a `codebase-memory` skill), while 5.0.0 ships 45
agents and 38 skills. The extra skill and 3 agents are those companions, and
they are still there after a later upgrade.

To remove a codebase-memory-mcp installed under `~/.local/bin` (by you or by
IronClaude) together with its companions, run its own uninstall. Use the
absolute path, because a bare `codebase-memory-mcp` could resolve to another
copy, such as the one in a Coder workspace image. This keeps its indexes:

```bash
"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"
```

Delete the indexes only if you no longer need them:

```bash
rm -rf ~/.cache/codebase-memory-mcp
```

### Serena

If you still want Serena, register it under the name `serena-local`, which the
installer never removes:

```bash
claude mcp add --scope user serena-local -- uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false
```

If you no longer want Serena at all:

```bash
uv tool uninstall serena-agent   # if you installed it yourself; Coder workspaces reinstall it at start
rm -rf ~/.serena                 # only if you no longer need Serena's user data
```

To remove a `codebase-memory-mcp` or `serena` registration the retire step
kept:

```bash
claude mcp remove codebase-memory-mcp --scope user
claude mcp remove serena --scope user
```

### Files 5.0.0 no longer ships

The installer never deletes core files. Copies of the retired core files
(`ORCHESTRATOR.md`, `COMMANDS.md`, `PERSONAS.md`, `MODES.md`, `FLAGS.md`,
`MCP.md`) stay in `~/.claude/`, and an old `~/.claude/commands/sc/README.md`
keeps showing a `/sc:README` command. Nothing loads the retired core files; delete
them if you like:

```bash
cd ~/.claude && rm -f ORCHESTRATOR.md COMMANDS.md PERSONAS.md MODES.md FLAGS.md MCP.md commands/sc/README.md
```

Commands, skills and agents are different: from 6.0.0 the installer retires the
ones a release stops shipping. See
[Commands, skills and agents a release no longer ships](#commands-skills-and-agents-a-release-no-longer-ships).

### Commands, skills and agents a release no longer ships

An upgraded workspace would otherwise keep dead commands: a `/sc:roadmap` left in
`~/.claude/commands/sc/` calls a `superclaude roadmap run` that no longer exists.
From 6.0.0, `superclaude install` (with or without `--force`) and
`superclaude update` end with a retire step that removes them, but only files
IronClaude can prove it wrote.

- **Proof.** A command or agent file is removed only when its SHA-256 equals the
  file as shipped at an earlier release tag (the list and hashes are generated
  from the `v5.0.0` and `v6.0.0` tags into
  `src/superclaude/cli/install_retired_data.py`). A
  skill is a folder: it is removed only when every file in it is a shipped file
  with a matching hash and nothing else is in it.
- **Removed from 5.0.0.** 12 commands: `build`, `cli-portify`, `improve`,
  `index-repo`, `index`, `load`, `review-translation`, `roadmap`, `save`, `spawn`,
  `tasklist`, `validate-roadmap`. 5 skills: `sc-cli-portify-protocol`,
  `sc-review-translation-protocol`, `sc-roadmap-protocol`, `sc-tasklist-protocol`,
  `sc-validate-roadmap-protocol`. No agent is removed in 6.0.0.
- **Removed from 6.0.0 (in 6.1.0).** 1 command: `tdd`. 9 skills: `operational-guide`,
  `prd`, `readme`, `roadmap`, `task`, `task-builder`, `tdd`, `tech-reference`,
  `tech-research`. No agent is removed in 6.1.0, and `/sc:task`,
  `/sc:validate-tests` and the eight `rf-*` agents are kept. A workspace upgraded
  straight from 5.0.0 to 6.1.0 gets both lists in one run (the retire data holds
  both; that straight path was not run end to end for 6.1.0).
- **Kept and explained.** A file you edited, a skill folder with a file or folder
  you added (including a `__pycache__` a skill script created), a link, or
  anything unreadable is kept. The installer prints one line for each, with the
  reason and the exact command that removes it, for example
  ``Kept /sc:roadmap: its content differs ... Remove it yourself with `rm ~/.claude/commands/sc/roadmap.md` ``.
  `superclaude doctor` fails with `Missing command-required skill(s)` while a kept
  command still asks for a removed skill; removing the kept item clears it.
- **Never touched.** Any name not on the generated list, and anything outside
  `~/.claude/commands/sc/` (or the folder you passed to `--target`),
  `~/.claude/skills/` and `~/.claude/agents/`.
- **Safe to repeat.** A second run changes nothing and prints "No retired
  commands, skills or agents present." (plus the kept lines while you keep
  anything). It works when `~/.claude` does not exist, and nothing in it changes
  the exit code of `install` or `update`.
- **Older than 5.0.0.** Files installed by an earlier release than the tag the
  list was generated from differ in content, so they are kept and reported the
  same way.

In the 6.1.0 end-to-end test (a genuine 6.0.0 install upgraded with
`superclaude install --force`, after an edit to `tdd.md` and a `my-notes.txt`
added to the `task-builder` skill folder) the step printed, with temporary paths
shortened to `~`:

```text
📦 Retiring commands, skills and agents this release no longer ships...
   Kept /sc:tdd: its content differs from every copy IronClaude shipped (you edited it, or it came from another source). This release no longer ships it, so it is dead weight. Remove it yourself with `rm ~/.claude/commands/sc/tdd.md`
   Removed skill operational-guide (this release no longer ships it; unchanged since it was installed)
   ... 4 more "Removed skill ..." lines (prd, readme, roadmap, task) ...
   Kept skill task-builder: 1 path(s) in it were added or changed after IronClaude installed it (my-notes.txt). This release no longer ships it, so it is dead weight. Remove it yourself with `rm -r ~/.claude/skills/task-builder`
   Removed skill tdd (this release no longer ships it; unchanged since it was installed)
   Removed skill tech-reference (this release no longer ships it; unchanged since it was installed)
   Removed skill tech-research (this release no longer ships it; unchanged since it was installed)
   Restart running Claude Code sessions so the removed commands and skills disappear.
```

The counts went from 35 commands, 48 agents and 35 skills (6.0.0) to 35
commands (the 34 shipped plus the kept `tdd`), 48 agents and 27 skills (the 26
shipped plus the kept `task-builder`). `superclaude doctor --verbose` then
exited 1 with `Missing command-required skill(s): tdd` until the two printed
`rm` commands were run, and printed `✅ SuperClaude is healthy` after them
(34 commands, 48 agents, 26 skills). The transcript is
[`docs/testing/v6.1.0/c-e2e-transcript.txt`](../testing/v6.1.0/c-e2e-transcript.txt).

For 6.0.0 (a genuine 5.0.0 install upgraded the same way, after an edit to
`roadmap.md` and a `my-notes.txt` added to `sc-tasklist-protocol`) the step
printed:

```text
📦 Retiring commands, skills and agents this release no longer ships...
   Removed /sc:build (this release no longer ships it; unchanged since it was installed)
   Removed /sc:cli-portify (this release no longer ships it; unchanged since it was installed)
   ... 9 more "Removed /sc:..." lines ...
   Kept /sc:roadmap: its content differs from every copy IronClaude shipped (you edited it, or it came from another source). This release no longer ships it, so it is dead weight. Remove it yourself with `rm ~/.claude/commands/sc/roadmap.md`
   Removed skill sc-cli-portify-protocol (this release no longer ships it; unchanged since it was installed)
   ... 2 more "Removed skill ..." lines ...
   Kept skill sc-tasklist-protocol: 1 path(s) in it were added or changed after IronClaude installed it (my-notes.txt). This release no longer ships it, so it is dead weight. Remove it yourself with `rm -r ~/.claude/skills/sc-tasklist-protocol`
   Removed skill sc-validate-roadmap-protocol (this release no longer ships it; unchanged since it was installed)
   Restart running Claude Code sessions so the removed commands and skills disappear.
```

The counts went from 45 commands, 45 agents and 38 skills (5.0.0) to 36 commands
(the 35 shipped plus the kept `roadmap`), 48 agents and 36 skills (the 35 shipped
plus the kept `sc-tasklist-protocol`).
`superclaude doctor --verbose` then failed with `Missing command-required
skill(s): sc:roadmap-protocol` until the two printed `rm` commands were run, and
printed `✅ SuperClaude is healthy` after them. The transcript is
[`docs/testing/v6.0.0/c-e2e-transcript.txt`](../testing/v6.0.0/c-e2e-transcript.txt).

Restart running Claude Code sessions afterwards so the removed commands and skills
disappear from them.

### Saved copies of changed files

`superclaude install --force` and `superclaude update` save a copy of every
command, rule and output-style file that differs from the shipped one before
they overwrite it. The install output lists the copies, for example
`Saved 7 changed command(s) before overwriting:` (and the same for `rule
file(s)` and `output style(s)`).

- **Why so many.** A file from an older release and a file you edited look the
  same to the installer, so both are saved. An upgrade leaves a copy of every
  command that changed since the release you came from, whether you edited it or
  not: 7 in the 6.0.0 to 6.1.0 test (six commands that 6.1.0 changed and one
  that the test edited), 27 from 5.0.0 to 6.0.0.
- **Not loaded.** The copy is named `<name>.bak.<UTC time>` (for example
  `analyze.md.bak.20261118T170151Z`). It ends in a time stamp, not in `.md`, so
  Claude Code does not load it as a command.
- **Not covered.** Core files, agents and skill folders are overwritten without a
  copy (see Step 1). A plain `superclaude install` overwrites nothing; it names
  each kept file that differs from this version (`N kept command(s) differ from
  this version and were NOT updated`).
- **If a copy cannot be saved,** that one file is left as it is, and
  `superclaude install` prints it as a failure and exits 1.
- **Nothing deletes them.** List the copies, then delete them when you no longer
  need what is in them (look at the ones for files you edited first):

  ```bash
  find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*'
  find ~/.claude/commands/sc ~/.claude/rules ~/.claude/output-styles -name '*.bak.*' -delete
  ```

  The `settings.json.bak.<timestamp>` files in `~/.claude/` are separate: the
  installer writes one on every run.

## Step 5: Move your session memories

`/sc:pm` and the PM agent keep session memory in
`<project>/.superclaude/memory/<key>.md`, where `<project>` is the top folder of
the git checkout (one store per worktree). Nothing reads `.serena/memories/`
any more: 6.0.0 removed the memory save and load commands, and with them the
read-only fallback to the old Serena folder.

To keep your Serena memories, copy them in each project (or worktree). The
second line adds the `.gitignore` that the PM agent creates on its first write, so
the store is not committed:

```bash
mkdir -p .superclaude/memory && cp -Rn .serena/memories/. .superclaude/memory/
[ -e .superclaude/.gitignore ] || printf '*\n' > .superclaude/.gitignore
```

## Step 6: Update your scripts

### From 6.0.0 to 6.1.0

| Old usage | In 6.1.0 |
|-----------|----------|
| `/task`, `/task-builder`, `/roadmap` | Removed. Use `/sc:workflow "<what to build>"`, then `/sc:implement <printed plan path>`. To continue an old task file, copy its unchecked items into a new list and run `/sc:implement <list>`; do not point `/sc:implement` at the old file, because it lists checked items too. |
| `/prd`, `/tdd`, `/tech-research`, `/tech-reference`, `/operational-guide`, `/readme`, `/sc:tdd` | Removed with no replacement. `/sc:research`, `/sc:analyze` and `/sc:brainstorm` cover the research steps; write requirement and design documents by hand or with `/sc:design`. |
| `/sc:brainstorm --handoff task` | Stops with a message that names the replacement. `--handoff` takes `none` or `design`; then run `/sc:workflow @<output>/merged-requirements.md`. |
| `/sc:reflect --remediate --depth deep`, `/sc:troubleshoot --fix --depth deep` | Both take the plan route (`/sc:workflow`, then `/sc:implement`) at every depth; `--depth deep` only sets the review depth. |
| `superclaude reflect run --fix` with a report that has only `remediation_task_path` | The wrapper ignores that field and the run ends as a terminal HALT. Regenerate the report with `/sc:reflect --remediate`. |
| `ccsession --list`, `--here` and the new-tab question | Sessions an agent saved are hidden (`ccsession --agents` shows them). New: `ccsession --mark <name> agent\|human`, `ccsession --classify [--apply]` and `ccsession --prune [--apply] [--days N]`; the last two are dry runs without `--apply`. See the [ccsession README](https://github.com/IronbellyOrg/IronClaude/blob/v6.1.0/src/superclaude/skills/ccsession-tag/README.md). |
| Claude Code retention (`cleanupPeriodDays`) | The installer's target is 90 days, not 365; it never lowers a value you already set. See [Installation](installation.md). |

Kept, nothing to change: `/sc:task`, `/sc:validate-tests`, the eval suite
`task_classification_contract` and all eight `rf-*` agents.

### From 5.0.0 to 6.0.0

| Old usage | In 6.0.0 |
|-----------|----------|
| `superclaude prd`, `cleanup-audit`, `cli-portify`, `roadmap`, `tasklist`, `sprint` (any subcommand) | Removed; `superclaude <group>` answers "No such command". Replacements: the interactive `prd` skill, `/sc:cleanup-audit`, and `/sc:workflow` then `/sc:implement`. The per-group table is in the [6.0.0 release notes](../releases/v6.0.0.md#command-line-groups-and-their-flags). If a script or CI job needs one, stay on `v5.0.0`. |
| `/sc:build`, `/sc:cli-portify`, `/sc:improve`, `/sc:index`, `/sc:index-repo`, `/sc:load`, `/sc:review-translation`, `/sc:roadmap`, `/sc:save`, `/sc:spawn`, `/sc:tasklist`, `/sc:validate-roadmap` | Removed; replacements are in the [release notes](../releases/v6.0.0.md#slash-commands-12). |
| `/sc:workflow --handoff tasklist`, `/sc:brainstorm --handoff tasklist` | `tasklist` is gone. `/sc:workflow --handoff` takes `none`, `design` or `implement`; `/sc:brainstorm --handoff` takes `none`, `design` or `task` (6.1.0 removes `task`; see the table above). |
| A model alias in `~/.aienv` whose name starts with a capital letter (for example `GLM`) | `ic` no longer resolves it and passes the name through as typed. Rename the alias to start with a lowercase letter. |

### From 4.x (the changes of 5.0.0)

| Old usage | In 5.0.0 |
|-----------|----------|
| `/sc:pr-submit --yes` | `--yes` is removed; drop it. With no `--monitor`, `/sc:pr-submit` now runs level 3 and pushes review and CI fixes; pass `--monitor 2` to stop before pushing. |
| `superclaude mcp --uninstall` or `--yes` | Both options are removed; drop them. |
| `superclaude mcp --servers serena` | Serena is no longer a registry server; the command reports an unknown selection. |
| `superclaude reflect run` | Promotes by default; pass `--no-promote` for the old behaviour. |
| `/sc:reflect --onboard` or `--with-hierarchy` | Removed; drop them. |
| `/ccsession-tag` | Removed; use `/rename`. |

## See also

- [6.1.0 release notes](../releases/v6.1.0.md): what is removed, replacements,
  migration steps and known issues
- [6.0.0 release notes](../releases/v6.0.0.md): what is removed, replacements,
  migration steps and known issues
- [5.0.0 release notes](../releases/v5.0.0.md): migration steps, breaking
  changes and known issues for the 4.x upgrade
- [Installation Guide](installation.md): requirements, what is installed, and
  uninstalling
- [MCP Installation Guide](../user-guide/mcp-installation.md): codegraph
  details, failures, indexing and removal
