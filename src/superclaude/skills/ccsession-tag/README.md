# ccsession

Claude Code session manager with named labels. Lets you resume specific
conversations by name from a shell, instead of hunting through `claude --resume`'s
UUID picker.

## What you get

- **`ccsession <topic>`** — shell command. Resume or start a Claude session
  labeled `<topic>`. Always launches with `--dangerously-skip-permissions`
  (override via `CC_CLAUDE_FLAGS`).
- **`ccsession --list`** — list all labeled sessions across workspaces, with
  the last activity time and short UUID.
- **`ccsession --here`** — list labels in just the current workspace.
- **`ccsession --rm <topic>`** — drop a label (does NOT touch the transcript).
- **`/ccsession-tag <topic>`** — slash command inside Claude. Tag the current
  conversation with a label so you can resume it by name later.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The `/ccsession-tag` slash command behavior |
| `ccsession` | The shell wrapper script (symlinked to PATH by install.sh) |
| `ccsession.env.example` | Template for proxy URL / auth env vars |
| `hooks/session-start.sh` | SessionStart hook (auto-registered by install.sh) |
| `install.sh` | One-shot installer |
| `README.md` | This file |

## Install

```bash
cd ~/.claude/skills/ccsession-tag   # or wherever you put this skill
./install.sh
```

That will:

1. Copy the skill into `~/.claude/skills/ccsession-tag/` (so the
   `/ccsession-tag` slash command is available in every workspace and the
   install survives the source folder being deleted).
2. Symlink `~/.local/bin/ccsession` → the user-level `ccsession`.
3. Create `~/.claude/ccsession.env` from the template (chmod 600) if it
   doesn't already exist.
4. Register the `SessionStart` hook in `~/.claude/settings.json` — an
   idempotent merge that preserves any existing hooks/settings, backs the
   file up first (`settings.json.bak`), and refuses to touch the file if it
   isn't valid JSON (printing the snippet to add by hand instead).

Make sure `~/.local/bin` is in your `PATH`. Then verify:

```bash
which ccsession    # -> /Users/<you>/.local/bin/ccsession (symlink)
ccsession --help
```

## Configure proxy / auth (optional)

If you route Claude through a proxy (LiteLLM etc.) or want to bake in a
specific API key, edit `~/.claude/ccsession.env`:

```bash
# Route through a proxy:
export ANTHROPIC_BASE_URL=http://your-proxy:4000/cli
export ANTHROPIC_AUTH_TOKEN=sk-...

# Or direct API:
export ANTHROPIC_API_KEY=sk-ant-...
```

The wrapper sources this file (if present) before launching claude, so every
`ccsession <topic>` inherits those vars. Leave it empty to rely on
`claude login` or your existing shell env.

## Daily usage

Start a labeled session:

```bash
ccsession brownfield
```

If the label doesn't exist yet, a new Claude session starts. Once it's
running and the conversation has gotten useful, retroactively label it:

```
/ccsession-tag brownfield
```

After a VS Code crash or restart, restore the right conversation in the right
terminal:

```bash
cd /path/to/your/workspace
ccsession brownfield
```

See all your labeled sessions:

```bash
ccsession --list
```

## Storage layout

- Label pointers live at
  `~/.claude/projects/<workspace-slug>/topics/<label>.txt`.
  Each file contains a single line — the session UUID.
- A `.cwd` file in the same dir caches the real workspace path so listings
  show the human-readable name even when the dir contains dashes.
- The conversation transcripts themselves are owned by Claude Code (the
  `<uuid>.jsonl` files alongside `topics/`). This skill never reads or
  modifies them.

## Uninstall

```bash
rm ~/.local/bin/ccsession
rm -rf ~/.claude/skills/ccsession
# Optional: rm ~/.claude/ccsession.env  (your secrets)
# Optional: remove the SessionStart hook block from ~/.claude/settings.json
```

Labels under `~/.claude/projects/*/topics/` are independent of the install —
they survive uninstall and reinstall.
