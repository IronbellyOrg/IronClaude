# T2: require-orca-worktree-agent.sh next to launch-job-identity.sh

Both are PreToolUse hooks with matcher `Bash`, registered as separate entries in
`src/superclaude/hooks/hooks.json` (and the `plugins/` copy).

## The risk

`src/superclaude/hooks/scripts/launch-job-identity.sh` (header lines 14-15) replaces
the WHOLE tool input through `updatedInput` for a launch-level governed session and
wraps the original command as one quoted argument of `execute`. Its header also says
the rewrite order of other hooks is unspecified. If the Orca gate were to see the
rewritten command, `orca worktree create` would sit inside one quoted argument and the
scanner would not see an `orca` command word, so the gate would allow it.

## The pinned test

`tests/hooks/test_require_orca_worktree_agent_governed.py::test_blocks_bare_create_in_a_governed_session`
feeds the gate the PreToolUse event a governed session produces for a bare
`orca worktree create --name x` (the original command, `session_id` `old`, a
`tool_use_id`, and `$HOME/.claude/state/launch-level/sessions/old` present) and expects
exit 2 with the block message and empty stdout.

## Unverified

The live order of the two hooks is unverified. This repository's tests run each hook
script on its own, and they do not run Claude Code, so no test shows which hook runs first,
whether they run in parallel on the original input, or whether the second one sees the
first one's `updatedInput`. The test above covers only the case where the Orca gate sees the original
command. The case where it sees the rewritten command is a known ceiling, the same
quoted-execution family the script header lists. The live check ("a bare create in a
governed `/sc:issue` agent session is blocked") is listed in `t8-delivery.md`.
