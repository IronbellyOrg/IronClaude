# Issue — `src/superclaude/hooks/hooks.json` uses a relative path

**Surfaced:** 2026-05-12
**Surfaced by:** §5.1 freshness-system design work (InfraDocs side); reflection pass identified that the existing pattern is fragile and the freshness `install_hooks.py` work should not propagate it.
**Severity:** Low (single hook today, behavior is "fail silent if cwd is wrong"). High if more hooks are added with the same pattern and the failure becomes invisible.
**Scope:** `src/superclaude/hooks/hooks.json` line 8 + the mirrored copy under `plugins/superclaude/hooks/hooks.json`.

---

## What the file says today

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/session-init.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

The `command` field on line 8 is `./scripts/session-init.sh` — a **relative path**.

## Why this is fragile

Claude Code resolves hook commands using shell-like rules. A relative
path resolves against whatever working directory Claude Code is in when
the hook fires. That working directory depends on:

- Where the user launched `claude` from
- Whether `--cwd` or `--add-dir` were passed
- Whether the session has changed dirs via `cd` in a Bash tool

So `./scripts/session-init.sh` only works if the user happens to launch
Claude Code from a directory where `./scripts/session-init.sh` exists.
For most installs, that's nowhere — Claude Code is launched from the
user's project, not from inside the SuperClaude install tree. The hook
silently fails to fire (or worse, fires a wrong file with the same name
from the user's project).

## What the official guidance says

Per Claude Code docs (referenced in `claudedocs/research_hooks_consolidated.md`
from the freshness-system research):

- Use `${CLAUDE_PROJECT_DIR}` (Claude Code expands this) or an absolute path.
- `$HOME` does NOT expand in hook config JSON (silent failure mode — community
  pattern Top 3 pitfall).
- `~` does expand (per Claude Code's path-expansion rules).

The freshness-system spec (`InfraDocs:phase5.1-context-refresh-design.md` §5)
uses `~/.claude/hooks/freshness-X.sh` as the command path — which is the
right shape because (a) `~` expands, and (b) it's where `install_hooks`
will place the scripts.

## Recommended fix

Two options, both small:

### Option A — Plugin-relative via `${CLAUDE_PLUGIN_ROOT}`

```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/session-init.sh"
```

Per Agent 1's official mechanics research, `${CLAUDE_PLUGIN_ROOT}` and
`${CLAUDE_PLUGIN_DATA}` are documented for plugin contexts. This works
if hooks.json is loaded as part of a plugin. If hooks.json is part of
the standalone install (copied to `~/.claude/...`), this variable is
empty and the path breaks.

### Option B — User-scope absolute path after install

```json
"command": "~/.claude/hooks/session-init.sh"
```

`~` expands per Claude Code's rules. Pre-condition: the install step
copies `session-init.sh` to `~/.claude/hooks/` (which requires an
`install_hooks` step that doesn't currently exist in `src/superclaude/cli/`).

## Recommendation

Adopt **Option B** as part of the freshness-system `install_hooks.py`
work. The same install module deposits scripts at `~/.claude/hooks/`
and writes paths in this shape. Two-bird fix: existing
session-init.sh issue is resolved as a side effect of building the
install pipeline for freshness hooks.

## Action item

Add to the IronClaude tasklist for freshness-system implementation:

> **Pre-cleanup task:** before adding freshness hooks to
> `src/superclaude/hooks/hooks.json`, rewrite the existing
> `./scripts/session-init.sh` command path to
> `~/.claude/hooks/session-init.sh` AND ensure `install_hooks.py`
> deposits `session-init.sh` at that path. Mirror the change to
> `plugins/superclaude/hooks/hooks.json`.

This avoids carrying the fragile pattern forward and gives the freshness
work a clean base to merge into.

## Open questions to verify before fix

- **OQ-1:** Does the current `session-init.sh` even fire today in
  end-user installs? If telemetry/logs suggest it has never fired (because
  the relative path is always wrong), the "fix" is effectively a new
  feature, not a repair. Worth a quick survey.
- **OQ-2:** Is there a managed-settings or plugin-bundle path where
  `${CLAUDE_PLUGIN_ROOT}` *would* work and Option A is preferable? If yes,
  the answer might be plugin-style distribution rather than user-scope
  install. Worth a 5-minute check before committing to Option B.
