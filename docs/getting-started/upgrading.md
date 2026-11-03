# Upgrading to IronClaude 5.0.0

This page is for anyone who already has IronClaude 4.x installed (including the
untagged 4.3.5) and wants 5.0.0. For a first install, see the
[Installation Guide](installation.md).

5.0.0 replaces codebase-memory-mcp and Serena with codegraph and moves session
memory to plain files. The upgrade therefore does more than copy new files: it
installs codegraph and removes the old MCP registrations IronClaude wrote. The
full list of changes is in the [5.0.0 release notes](../releases/v5.0.0.md).

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

The upgrade overwrites every file IronClaude ships, including an edited
`~/.claude/CLAUDE.md` and `~/.claude/RULES.md`, and keeps no backup of them. It
also deletes and re-copies each shipped skill folder in `~/.claude/skills/`, so
any file you added inside one is lost.

Copy anything you changed first, for example:

```bash
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine
cp ~/.claude/RULES.md ~/.claude/RULES.md.mine
```

Re-apply your changes after the upgrade. The installer does back up
`~/.claude/settings.json` before it merges its hook entries (a file named
`settings.json.bak.<timestamp>`).

## Step 2: Upgrade the package and the installed files

```bash
pipx install --force git+https://github.com/IronbellyOrg/IronClaude
superclaude install --force
```

To install exactly this release rather than the latest commit, use
`git+https://github.com/IronbellyOrg/IronClaude@v5.0.0` in the first command.

Use `superclaude install --force`, not the other two install commands:

| Command | Refreshes existing files | Installs codegraph | Retires old MCP registrations |
|---------|--------------------------|--------------------|-------------------------------|
| `superclaude install` | No, skips files that already exist | Yes | Yes |
| `superclaude update` | Yes | No | No (it only prints a notice when a legacy registration is present) |
| `superclaude install --force` | Yes | Yes | Yes |

If you already upgraded with `superclaude update`, run
`superclaude install --force` now.

### From a clone

In an IronClaude clone, check out the release first, then run `./update.sh`:

```bash
git fetch origin --tags
git checkout v5.0.0
./update.sh
```

`update.sh` installs whatever is checked out in that folder, not the latest
release: it runs `pipx install --force ./`, then `superclaude install --force`,
`make sync-dev` and `superclaude doctor`. It needs `pipx` and `make` on `PATH`;
without `pipx` it stops at that first command (exit 127). Install pipx with
`uv tool install pipx` or your distribution's `pipx` package.

## What the upgrade does

`superclaude install --force` runs these steps in order:

1. Refreshes the framework files in `~/.claude/`: 11 core files, 45 commands,
   45 agents, 38 skills, hooks, templates, rules and output styles, and merges
   its hook entries into `~/.claude/settings.json`.
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

The retire step never touches:

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
superclaude --version          # prints: SuperClaude, version 5.0.0
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
upgrade from 4.3.5, `superclaude doctor --verbose` counted 48 agents and 39
skills (including a `codebase-memory` skill), while 5.0.0 ships 45 agents and 38
skills. The extra skill and 3 agents are those companions.

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

The installer never deletes files. Copies of the retired core files
(`ORCHESTRATOR.md`, `COMMANDS.md`, `PERSONAS.md`, `MODES.md`, `FLAGS.md`,
`MCP.md`) stay in `~/.claude/`, and an old `~/.claude/commands/sc/README.md`
keeps showing a `/sc:README` command. Nothing loads the retired core files; delete
them if you like:

```bash
cd ~/.claude && rm -f ORCHESTRATOR.md COMMANDS.md PERSONAS.md MODES.md FLAGS.md MCP.md commands/sc/README.md
```

## Step 5: Move your session memories

`/sc:save`, `/sc:load` and `/sc:pm` now keep session memory in
`<project>/.superclaude/memory/<key>.md`, where `<project>` is the top folder of
the git checkout (one store per worktree). For this release only, `/sc:load`
still reads `.serena/memories/<key>.md` when the new file is absent; it never
writes there.

To keep your Serena memories, copy them in each project (or worktree). The
second line adds the `.gitignore` that `/sc:save` creates on its first write, so
the store is not committed:

```bash
mkdir -p .superclaude/memory && cp -Rn .serena/memories/. .superclaude/memory/
[ -e .superclaude/.gitignore ] || printf '*\n' > .superclaude/.gitignore
```

## Step 6: Update your scripts

| Old usage | In 5.0.0 |
|-----------|----------|
| `/sc:pr-submit --yes` | `--yes` is removed; drop it. With no `--monitor`, `/sc:pr-submit` now runs level 3 and pushes review and CI fixes; pass `--monitor 2` to stop before pushing. |
| `superclaude mcp --uninstall` or `--yes` | Both options are removed; drop them. |
| `superclaude mcp --servers serena` | Serena is no longer a registry server; the command reports an unknown selection. |
| `superclaude sprint run <index>` in CI | With no `--start`/`--end` it auto-resumes and asks for confirmation. Add `--yes` (or set `CI=1`), or pass `--start 1` for the old start-from-phase-1 behaviour. |
| `superclaude reflect run` | Promotes by default; pass `--no-promote` for the old behaviour. |
| `/sc:reflect --onboard` or `--with-hierarchy` | Removed; drop them. |
| `/ccsession-tag` | Removed; use `/rename`. |

## See also

- [5.0.0 release notes](../releases/v5.0.0.md): migration steps, breaking
  changes and known issues
- [Installation Guide](installation.md): requirements, what is installed, and
  uninstalling
- [MCP Installation Guide](../user-guide/mcp-installation.md): codegraph
  details, failures, indexing and removal
