---
name: ccsession-tag
description: "Retired: name a Claude Code session with the built-in /rename <name>, or start it with ccsession <name>. This folder holds the ccsession command, its hooks and the model shim."
user-invocable: false
disable-model-invocation: true
---

# ccsession (the `/ccsession-tag` command is retired)

This skill folder holds the `ccsession` shell command, `ccsession-orca`, the
session-name hooks and the gateway model shim. `superclaude install` installs a
skill folder only when it has a `SKILL.md`, so this file stays; it is not a
command any more. Nobody can run it, and Claude never loads it on its own.

To name a session, use either way. Both give it one name, shown in ccsession's
list, in Claude Code's prompt box and on the Orca tab:

- From the shell: `ccsession <name>` starts or resumes the session with that
  name (quote a name with spaces: `ccsession "my work"`).
- Inside Claude Code: `/rename <name>` names or renames the open session. It
  is built in, so it costs no tokens; ccsession's hooks copy the name into its
  list at the next message or when the session ends, and `ccsession <name>`
  reopens it.

Each list in `ccsession --list` is headed by its repo's name, and `ccsession
--here` adds the current worktree (`IronFlow  (worktree: coordinator)`).

Claude Code deletes a conversation 30 days after its last change by default,
and a name does not protect it. The installer sets `cleanupPeriodDays` to 365 in
`~/.claude/settings.json` when it is absent or lower; a managed value (for
example `/etc/claude-code/managed-settings.d/`) wins over it, and `ccsession
--list` warns when the value in force is below 365.

See `~/.claude/skills/ccsession-tag/README.md` for install, names, Orca and
tiers.
