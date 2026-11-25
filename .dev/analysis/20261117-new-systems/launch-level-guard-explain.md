# Explanation: launch-level guard hook (advanced)

Source read from origin/master (read-only git show): `src/superclaude/hooks/scripts/launch-level-guard.sh` (750 lines, identical to its `plugins/superclaude/hooks/scripts/` mirror), `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (1884 lines), `src/superclaude/hooks/hooks.json`. graph:stale (codegraph not used).

## Purpose

`/sc:issue --claim` starts a Claude Code agent in a new Orca worktree. The owner wants that agent to stop at a plan until a person releases it, and never to merge, push to main or message other sessions. The guard is a bash+jq hook that enforces this from outside the model. Only sessions the claim launched are "governed"; every other session is allowed (script header, lines 4-7).

## Mental model

1. Claim writes a one-word record (`worktree`, `full` or `full-submit`) into `~/.claude/state/launch-level/pending/<nonce>` and starts the agent with a prompt starting `[sc-launch:v1:<nonce>]` (orca_worktree.py:1745-1765).
2. On the agent's first UserPromptSubmit the guard sees the marker, renames the pending record (one `mv`, so a nonce is used once) and hard-links it as `sessions/<session_id>` (guard.sh:314-385). That binds the session to its level.
3. On every PreToolUse the guard looks up the session id. No record means allow. A record means classify the call (git, gh, Skill, Bash, Edit, Agent, MCP...) into classes and compare to the level in one table (guard.sh:725-745).
4. Release: at level `worktree` only, a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task` creates `sessions/<sid>.ok` (guard.sh:347-361). The level becomes "worktree (approved)", which allows IMPL and TURN classes only.

## Advanced points

- Fails closed for governed sessions (EXIT trap, lines 142-163), open for ordinary ones; identity loss (no valid session id) is a declared fail-open limit (lines 387-391).
- Text-based classification: quotes and backslashes are stripped, words split on separators, then git/gh subcommand tables decide. Unknown git/gh subcommands are blocked (UNKNOWN), so aliases cannot smuggle commit/push/merge.
- Push is allowed only as the exact form `git push [-u] origin <branch>` and never to master/main (line 658).
- Tamper tokens block edits or commands touching the store, settings, hooks, git config or pre-push hook (lines 700-717).
- Messages follow a Blocked / Why / You can format on stderr, exit 2.
- Companion L2: `launch-level-pre-push.sh` is a git pre-push hook that refuses governed pushes to main/master.

## What changed in the last 72 hours

PR #583 (merged 2026-11-16) deleted the typed `approved` release: the whole-prompt match of `approved`, `approved.`, `approved!` was removed from the guard, the LL-IMPL hint, the launch prompt template and claim output. PR #584 changed one message line (LL-TURN) in the guard. The hook itself dates from PR #432 (2026-11-07).
