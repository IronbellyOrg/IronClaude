# T8: delivery steps for "every Orca worktree gets an agent"

Package: `TASK-WF-enforceTheOwnerP-20261108-031809`. Test and lint results: `./t8-tests.log`.

## Update (after the change is merged)

1. On each machine, run `superclaude update`. Plain `superclaude install` skips core files that already exist (`src/superclaude/cli/install_core.py:70-72`: `if dest_file.exists() and not force: skipped.append(...)`), so `~/.claude/CLAUDE.md` would keep the old text; `update` forces them.
2. `update` overwrites local edits to `~/.claude/*.md`. Copy any local edit you want to keep first.
3. Sessions that were started before the update keep the old instructions and the old hook list until they are restarted. Restart them.

## Confirm

- `grep -c 'Every Orca worktree gets an agent' ~/.claude/CLAUDE.md` prints `1`.
- `~/.claude/settings.json` lists `~/.claude/hooks/require-orca-worktree-agent.sh` under `hooks.PreToolUse`, in an entry with matcher `Bash` and `"timeout": 3`.
- `ls -l ~/.claude/hooks/require-orca-worktree-agent.sh` shows an executable file.
- Offline smoke check of the installed hook, no Orca call: `printf '%s' '{"tool_name":"Bash","tool_input":{"command":"orca worktree create --name x"}}' | ~/.claude/hooks/require-orca-worktree-agent.sh; echo rc=$?` prints the block message and `rc=2`; with ` --agent claude` added it prints `rc=0`.

## Not covered

The hook only checks the `--agent` flag of a Bash tool call that runs `orca worktree create`. It does not stop:

- a human typing the command in a terminal, and other agent tools that create worktrees themselves;
- `bash -c`, `sh -c`, `eval`, `env -S`, `ssh host '...'`, a heredoc piped into a shell, `xargs`, `find -exec` (quoted-execution forms);
- a quoted value equal to `--agent`, for example `--prompt "--agent"`;
- `claude --bare` sessions, which skip settings hooks;
- scripts that call Orca as a subprocess, such as `orca_worktree.py` (it runs `orca worktree create` itself without `--agent`, on purpose: see the 2026-11-08 notes on D2 and FO-18 in `docs/designs/sc-issue-claim-pipeline-flag.md`);
- hosts without `jq` or `awk` (the hook fails open there);
- the live order of this hook and `launch-job-identity.sh` for a governed session: if the identity hook's rewrite reached the Orca gate first, the original command would sit inside one quoted argument (see `t2-launch-identity-interaction.md`).

"No worktree for your own use", "the creator owns the agent" and "a human-created worktree needs an agent" are instruction text only.

## Pending live checks (unit tests cannot cover these)

Each needs a real Orca runtime and creates a real worktree, so none was run in this change.

1. **Claim leaves no plain tab, and the close runs after the copy.** Run `/sc:issue --claim <test issue>` on a test issue, then `orca terminal list --worktree path:<wt> --json`. Expect one terminal that runs the agent and no empty tab, and no `W-FIRST-TAB-LEFT`. Also check that `<wt>/.dev/issues/<N>/launch-prompt.md` existed before the agent started. Risk to watch: if Orca registers the seeded tab 2-3 seconds after the create returns, `terminal list` shows zero terminals, the claim reports `W-FIRST-TAB-LEFT`, and the tab survives (harmless, but the close step then needs a short retry).
2. **A bare create in a Claude session is blocked.** In an installed, restarted Claude session ask the agent to run `orca worktree create --name hook-check` (do not run it yourself). Expect the `ORCA WORKTREE BLOCK` message and no new worktree in `orca worktree list`.
3. **A bare create in a governed `/sc:issue` agent session is blocked.** Do the same from the agent that a `/sc:issue --claim` launch started (launch-level state present). This is the live check for the unverified hook order in `t2-launch-identity-interaction.md`.
4. **`orca worktree create --agent claude --prompt "<task>"` leaves no plain tab.** Run it for a throwaway worktree and list its terminals: expect only the agent's terminal. Then repeat with `--activate` and with a repository that has setup hooks, to see whether either still seeds a plain first tab. If one does, the block message and the `CLAUDE.md` example must not combine `--agent` with that option.
5. **`--pipeline none` makes no worktree.** `/sc:issue --claim <test issue> --pipeline none` posts both comments, writes `.dev/issues/<N>/next-steps.md`, and `orca worktree list` shows no new `issue-<N>` row.
