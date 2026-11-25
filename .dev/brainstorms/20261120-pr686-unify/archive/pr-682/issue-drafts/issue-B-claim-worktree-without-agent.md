## What was tried
Review of PR 697 (the revert of PR 682) flagged the restored "Worktree, then worker" step in `WORKER-CONTRACT.md` (line 298; Codex P1 and Augment): it creates a worktree with no agent before the worker starts, which conflicts with the repository rule that every Orca worktree gets an agent (the Orca hook blocks `orca worktree create` without `--agent`). The cause is the claim script, not the revert: `orca_worktree.py` (docstring lines 23 to 40) runs `orca worktree create` with no `--agent` on purpose, because the claim must copy the issue folder `.dev/issues/<N>/` into the worktree before any agent starts. Orca then opens a plain first terminal tab, which the script closes (warning `W-FIRST-TAB-LEFT` when it cannot). PR 682 did not touch this script. Fix commit `fd23c01a9` in PR 697 changed only the contract wording: the claim script creates the worktree without an agent of its own, and the worker started right after by `worker-start` is that worktree's agent. The two review threads were left open. Simply adding `--agent` was considered and rejected: it would start a claim agent and then a second agent from `worker-start` in the same worktree (the one-live-agent-per-worktree problem that debate D07 found for the Coordinator worktree), and the copy would race the agent's start. Whether the hook sees an `orca` call made inside a script is UNVERIFIED; it reads commands an agent types.

## Relevant files and links
- `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (docstring lines 23 to 40)
- `src/superclaude/core/WORKER-CONTRACT.md` around line 298 (restored by PR 697, reworded in `fd23c01a9`)
- The repository Orca rule in the global `~/.claude/CLAUDE.md` ("Every Orca worktree gets an agent"), and the project `CLAUDE.md`
- PR 697: https://github.com/IronbellyOrg/IronClaude/pull/697 (threads on line 298); PR 682 (the deletion); PRs 584 and 591
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/VERDICT.md (claim agents launch into the shared Coordinator worktree) and spec/SPEC.md

## Done when
The owner chooses one of two, and it is tested. (1) Keep the script as a documented exception: the rule text names it, and a test pins that the claim worktree has no agent of its own until `worker-start`. (2) Change the claim so the worktree is created with the worker's one agent and the issue folder is read by absolute path (no copy), with a live check on a throwaway issue that exactly one agent exists in the claim worktree afterwards.

## Pick-up note
- Do not add `--agent` to the create call alone; it starts a second agent and races the copy.
- Check first whether the Orca hook can see a script's inner `orca` call. If it cannot, the exception is silent, and option (1) means saying so in the rule.
- Related to debate D07 (one live agent per worktree) and the Coordinator worktree design in the unification spec. Decide the two together.
- The owner's default for now is the documented exception that the contract wording already states.
