---
name: help
description: "List the SuperClaude commands and skills installed here, show the six process levels, and point to the routing guide"
category: utility
complexity: low
allowed-tools: Read, Glob, Grep, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(echo:*), Bash(test:*), Bash(basename:*), Bash(dirname:*), Bash(sed:*), Bash(while:*), Bash(read:*), Bash([:*), Bash(case:*), Bash(continue:*), Bash(git rev-parse:*)
mcp-servers: []
personas: []
---

# /sc:help - What is installed and where to start

## Triggers

- "What commands do I have?", "what can SuperClaude do?", or `/sc:help`
- Choosing where to start before running a command
- Checking whether an install or update worked

## Behavioral Flow

Run only the listing commands below (they read files and change nothing). Run each of the four listings below as its own Bash call. Then do steps 2-4. Do nothing else.

### 1. List what is installed, read live

List only what exists on disk. Show each name with the `description:` line from its frontmatter, in up to four groups. Skip `README.md`. Each listing prints the name Claude Code shows; do not invent a prefix. The mapping:

- Project-local: `.claude/commands/<name>.md` is `/<name>`; `.claude/commands/<dir>/<name>.md` is `/<dir>:<name>`; `.claude/skills/<name>/SKILL.md` is skill `<name>`.
- Plugin: `commands/<name>.md` is `/<plugin name>:<name>` and `skills/<name>/SKILL.md` is skill `<plugin name>:<name>`, where `<plugin name>` is the `name` field of `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`.

**Commands (`/sc:`)** - each `$HOME/.claude/commands/sc/<name>.md` is `/sc:<name>`:

```bash
find -L "$HOME/.claude/commands/sc" -maxdepth 1 -name '*.md' 2>/dev/null | while read -r f; do n=$(basename "$f" .md); [ "$n" = README ] && continue; d=$(grep -m1 '^description:' "$f"); echo "/sc:$n | ${d#description: }"; done
```

**Skills** - each `$HOME/.claude/skills/<name>/SKILL.md`:

```bash
find -L "$HOME/.claude/skills" -mindepth 2 -maxdepth 2 -name SKILL.md 2>/dev/null | while read -r f; do d=$(grep -m1 '^description:' "$f"); echo "$(basename "$(dirname "$f")") | ${d#description: }"; done
```

**Project-local** - commands and skills defined in the current project:

```bash
find -L .claude/commands .claude/skills -maxdepth 2 -name '*.md' \( -path '.claude/commands/*' -o -path '.claude/skills/*/SKILL.md' \) 2>/dev/null | while read -r f; do [ "$(basename "$f")" = README.md ] && continue; case "$f" in .claude/skills/*) n="skill $(basename "$(dirname "$f")")";; .claude/commands/*/*) r=${f#.claude/commands/}; n="/${r%%/*}:$(basename "$f" .md)";; *) n="/$(basename "$f" .md)";; esac; d=$(grep -m1 '^description:' "$f"); echo "$n | ${d#description: }"; done
```

**Plugin install** - only when Claude Code was given SuperClaude as a plugin. If the text below still shows the literal `${CLAUDE_PLUGIN_ROOT}`, or the variable is empty, skip this group (a skipped group prints nothing and counts as empty):

```bash
[ -z "${CLAUDE_PLUGIN_ROOT}" ] || { p=$(grep -m1 '"name"' "${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json" 2>/dev/null | sed 's/.*"name"[^"]*"\([^"]*\)".*/\1/'); find -L "${CLAUDE_PLUGIN_ROOT}/commands" "${CLAUDE_PLUGIN_ROOT}/skills" -maxdepth 2 -name '*.md' \( -path "${CLAUDE_PLUGIN_ROOT}/commands/*.md" ! -path "${CLAUDE_PLUGIN_ROOT}/commands/*/*" -o -path "${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md" \) 2>/dev/null | while read -r f; do [ "$(basename "$f")" = README.md ] && continue; case "$f" in */SKILL.md) n="skill $p:$(basename "$(dirname "$f")")";; *) n="/$p:$(basename "$f" .md)";; esac; d=$(grep -m1 '^description:' "$f"); echo "$n | ${d#description: }"; done; }
```

These listings use `find`, not shell globs, so a missing folder prints nothing in any shell (zsh aborts a whole command on an unmatched glob).

Output rules:

- One line per entry: name, then the description, shortened to one line. A file with no `description:` line is still listed, with `(no description line)`. Sort names alphabetically inside each group.
- Skills whose names end in `-protocol` are loaded by their `/sc:` command; list them last in the Skills group under the label "loaded by commands, not run directly".
- A skipped Plugin group prints nothing and counts as empty.
- For an empty group print `Nothing installed at <path>.`, using `~/.claude/commands/sc/` (Commands), `~/.claude/skills/` (Skills), or `.claude/commands/ and .claude/skills/ in this project` (Project-local).
- If the Commands, Skills, and Project-local groups are all empty (and Plugin is empty or skipped), print only this message instead of the per-group lines:
  `No SuperClaude commands or skills found. If you installed SuperClaude with pipx or pip, run superclaude install. If you installed it as a Claude Code plugin, its commands are in the Claude Code slash-command menu.`

### 2. Show the six process levels

Find the routing guide. Try these in order and use the first that exists. Inside an IronClaude checkout (`src/superclaude/commands/` exists under `git rev-parse --show-toplevel`), try location 3 first, then the others in order, because the installed copy may be older:

1. `$HOME/.claude/HOW-WE-WORK.md` (installed by `superclaude install`)
2. `${CLAUDE_PLUGIN_ROOT}/skills/sc-recommend/refs/HOW-WE-WORK.md` (plugin installs; skip if the variable is unexpanded or empty)
3. `src/superclaude/core/HOW-WE-WORK.md` under the repository root (`git rev-parse --show-toplevel`; inside an IronClaude checkout)

Print, verbatim, the text between the markers `<!-- level-table:v1 -->` and `<!-- /level-table -->`: the six-level table and the hard limit. Do not retype or shorten it.

If the guide is found but either marker is missing, print exactly this line, with `<path>` replaced by the guide's path, and skip the table:

`Routing guide at <path> has no level table (markers missing). pipx/pip install: run superclaude update. Plugin install: update the SuperClaude plugin.`

If no guide is found, print exactly this line and skip the table:

`Routing guide not found. pipx/pip install: run superclaude update. Plugin install: update the SuperClaude plugin. Until then, recommendations do not use the routing guide.`

### 3. Name the built-ins the guide uses

Print: "The guide also uses two Claude Code built-in commands: `/code-review` (bug review of your changes) and `/security-review` (security review). They come with Claude Code and are not files in your install."

### 4. Point to the next step

Print these three lines:

- Full workflows, in order, with required flags: read `<the guide path found in step 2>` (normally `~/.claude/HOW-WE-WORK.md`). If none was found, say how to install it, as in step 2.
- Not sure which tool fits your job: `/sc:recommend "<what you want to do, and why>"`.
- Options for one command: read its file. Installed `/sc:` commands are at `$HOME/.claude/commands/sc/<name>.md`; project-local commands are under `.claude/commands/`; plugin commands are at `${CLAUDE_PLUGIN_ROOT}/commands/<name>.md`; inside an IronClaude checkout (`src/superclaude/commands/` exists under `git rev-parse --show-toplevel`), read `src/superclaude/commands/<name>.md` under that repository root.

## Examples

### Show everything installed

```
/sc:help
```

Prints the installed commands and skills with their descriptions, then the six-level table and the hard limit, then the built-ins and the pointers.

### In a project with its own commands

```
/sc:help
```

Also prints the Project-local group, for example a command defined in `.claude/commands/deploy.md` of the current project.

### Before the guide is installed

```
/sc:help
```

Prints the listings, then the "Routing guide not found" line instead of the table.

## Boundaries

**Will:**

- List the commands and skills that are installed, read from disk each time
- Print the guide's level table and hard limit exactly as the guide has them
- Name the Claude Code built-ins the guide uses
- Point to the guide and to `/sc:recommend`

**Will Not:**

- Write, edit, or delete any file
- Run any command it lists
- Invent entries that are not on disk, or keep a hand-written list of commands
- Recommend a workflow (that is `/sc:recommend`'s job)
