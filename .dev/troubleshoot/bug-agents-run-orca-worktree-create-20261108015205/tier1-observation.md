# Tier 1 observation (captured 2026-11-08T01:51Z to 01:56Z, parent session, same-shell, read-only)

Carried in from the prior run (same host): .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/tier1-observation.md (O1 to O5, behaviour rows 1-6) and UPDATE-1-orchestrator-evidence.md. Not re-captured here except where noted.

## Behaviour definitions
Row 1 (behaviour-definitions.md), read 2026-11-08T01:58Z from the local IronOrca checkout (HEAD dc57b3d6e8; not proven equal to installed 1.4.245-aidev02):

/home/coder/workspaces/IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:202-214
```
  } else if (
    ports.canSpawn &&
    shouldSeedWorktreePrimaryTerminal({
      hasPrimarySurface: startupPaneHeld,
      callerProvidesSurface: callerProvidesInitialSurface(args)
    })
  ) {
    try {
      await ports.createTerminal(`id:${worktree.id}`, { surfaceOwner: false })
    } catch (error) {
      warning = appendFailure(warning, worktree.path, 'initial', error)
    }
  }
```
:259-269
```
function callerProvidesInitialSurface(
  args: Parameters<typeof startRuntimeLocalWorktreeTerminals>[0]
): boolean {
  // Background agent creates already leave their initial surface to the caller.
  return (
    args.promisedAgentChat === true ||
    (args.createdWithAgent !== undefined &&
      args.request.activate !== true &&
      args.request.runHooks !== true)
  )
}
```
/home/coder/workspaces/IronOrca/src/shared/worktree-first-surface.ts:2-14
```
export function shouldSeedWorktreePrimaryTerminal(args: {
  hasPrimarySurface: boolean
  callerProvidesSurface: boolean
  startupNeedsTerminal?: boolean
  issueCommandNeedsTerminal?: boolean
}): boolean {
  return (
    !args.hasPrimarySurface &&
    (!args.callerProvidesSurface ||
      args.startupNeedsTerminal === true ||
      args.issueCommandNeedsTerminal === true)
  )
}
```
Reading: with no agent on the create, `callerProvidesSurface` is false, so the seed runs and `createTerminal` gets no startup command: a plain shell. The `await` means the seed is requested inside the create call (whether the CLI reply waits for it is not shown here).

## N1. Every real `orca worktree create` Bash call in ~/.claude/projects transcripts, with the next two Bash calls of the same session
Command: for each transcript containing `"orca worktree create`, jq over assistant Bash tool_use inputs, awk prints the create line (excluding `--help`) and the next two commands. Run 2026-11-08T01:54Z. Commands truncated to 170 chars.

| session | ts | create flags (abridged) | --agent | next action by the same session |
|---|---|---|---|---|
| af4401a8 | 2026-11-01T14:08:54Z | --name gh-pin-latest --issue 367 ... --json | no | `orca orchestration task-create/run-create` (supervised worker) |
| 1779a921 | 2026-11-06T20:48:50Z | --name fix-claude-cli-session-launch --no-parent --agent claude --prompt ... | yes | `orca terminal read/send` to the agent terminal |
| 955b0bcc | 2026-11-07T20:35:28Z | --name fix-flaky-parallel-thread-test --base-branch origin/master | no | `cd /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test && uv run pytest ...`, then `git add/commit` |
| 347c98b7 | 2026-10-25T14:23:17Z | --name IB-CPlus-01 --parent-worktree active --json | no | read-only discovery commands (no cd to the new path in the next two) |
| 44e7b6ec | 2026-11-02T23:09:40Z | --repo path:IronOrca --name orca-idle-sleep | no | `orca terminal create --worktree path:$W --title ...` then send a prompt |
| 44e7b6ec | 2026-11-04T12:10:27Z | --name specstory-symlink-home-fix ... --setup skip --json | no | git on new path, then a `/sc:workflow` prompt sent to a terminal |
| 44e7b6ec | 2026-11-04T15:50:46Z | --name ci-self-hosted-runners ... | no | prompt sent, `orca terminal rename --terminal term_6d11...` |
| 44e7b6ec | 2026-11-04T19:26:03Z | --name followup-notes-359-360 ... --setup skip | no | prompt sent, `orca terminal rename --terminal term_8235...` |
| 68fc8b81 | 2026-11-06T02:17:58Z | --name ironclaude-install-force --no-parent --json | no | `cd /home/coder/workspaces/worktrees/Coder/ironclaude-install-force && ...` |
| 7fd4f558 | 2026-11-06T21:42:47Z | --name WorkerContractFollowups --no-parent --setup skip --json | no | `cd .../WorkerContractFollowups && git status ...` |
| 7fd4f558 | 2026-11-07T01:11:47Z | --name P1Closeout --no-parent --setup skip --json | no | `cd $C && git log ...`, then `git rm ...` |
| 7fd4f558 | 2026-11-07T01:13:32Z | --name OrcaCLICommandRefactor-P2 --no-parent --setup skip --json | no | `cd .../OrcaCLICommandRefactor-P2 && sed ...` |
| 7fd4f558 | 2026-11-07T05:36:13Z | --name install-core-stale-warning --no-parent | no | `cd .../install-core-stale-warning && git apply ...` |
| d9133120 | 2026-10-26T17:26:04Z | --name Test --no-parent --json | no | `cd /home/coder/workspaces/worktrees/IronClaude/Test && git log ...` |
| 514abb0c | 2026-11-02T18:49:03Z | --name release-v5.0.0 ... | no | `cd .../release-v5.0.0 && git log ...` |
| 514abb0c | 2026-11-05T01:55:00Z | --name pr383-fix --no-parent --json | no | `cd .../pr383-fix && git merge origin/master ...` |
| 0cf7ada3 | 2026-11-04T22:41:31Z | --name docs-sc-issue-usage --base-branch origin/master | no | `W=...; cd $W && grep ...` |
| 0798a6cf | 2026-11-07T05:37:02Z | --name pr369-followup-record --no-parent | no | `cd .../pr369-followup-record && git fetch ...`, then `git add/commit` |

Counts: 18 creates; 1 with `--agent`; 17 without. Of the 17: 11 are followed by the SAME session `cd`-ing into the new checkout and working there itself; 4 (session 44e7b6ec) send work into a terminal of the new worktree (whether that is the seeded terminal or a new one is not settled by the truncated lines; the 23:09 case creates a new terminal); 1 (af4401a8) hands it to a supervised worker; 1 (347c98b7) is unclear from the next two calls.

## N2. `orca worktree create --help` (orca 1.4.245-aidev02), captured 2026-11-08T01:53Z, verbatim lines
- "By default this creates the worktree and its first terminal without switching the active Orca view."
- "Pass --agent to start an agent with the worktree, as a chat or a terminal per your Chat UI setting, exactly as a new agent tab does"
- "This creates a new checkout. For a fresh agent in an existing worktree, use `orca agent launch` instead."
- The usage line lists no option that suppresses the first terminal (flags: --name --repo --project --host --project-host-setup --agent --prompt --model --effort --surface --setup --base-branch --branch --reference --reference-site --issue --pr --linear-issue --gitlab-issue --gitlab-mr --comment --parent-worktree --no-parent --run-hooks --activate --retry-launch --json).

## N3. `orca terminal close --help` and `orca terminal list --help`, captured 2026-11-08T01:53Z, verbatim lines
- Usage: `orca terminal close ([--terminal <handle>] [--tab] | --worktree <selector> --all) [--json]`
- "With --worktree <selector> --all, stops every terminal process owned by that workspace and durably removes its terminal tabs, layouts, and resume records."
- Usage: `orca terminal list [--worktree <selector>] [--limit <n>] [--include-visual-layouts] [--json]`

## N4. `orca agent launch --help`, captured 2026-11-08T01:54Z, verbatim lines
- "Start an agent in an existing workspace, as a chat or a terminal"
- "The tab opens without switching focus; pass --focus to switch to it." (a new tab; no option to reuse an existing terminal)

## N5. Bare-create `--json` result (7fd4f558, WorkerContractFollowups, tool_result tail)
The tail shows `worktree`, `lineage`, `warnings`, `localBaseRefUpdateSuggestion`, `catalogVersion`; no terminal handle is visible in the captured tail (head of the result not captured, so absence of a handle field is UNVERIFIED). An `--agent` create result (44e7b6ec transcript) does carry `"agentTerminalHandle"` and `"terminalHandle"`.

## N6. Daemon instances (from UPDATE-1, verified there)
- 955b0bcc create 20:35:28.903Z -> daemon `session-created` 20:35:31.197Z with `startup-command-delivery hasCommand=false`, one session only.
- 7fd4f558 create 05:36:13Z -> daemon session 05:36:16.234Z hasCommand=false, one session only.

## N7. Live tabs per worktree, `orca terminal list --json` (jq: worktreePath basename, handle, title), captured 2026-11-08T01:54Z
Tabs with an empty title (plain shells): Ironeye term_6c4f59e4; fix-flaky-parallel-thread-test term_9fe9e46e and term_ee0007a6; install-core-stale-warning term_19ed8a7e.
Worktrees issue-331-github-issue-watcher, issue-339-orchestrator-mode, issue-346-review-loop-convergence, issue-361-late-conflict-resync, issue-473-claim and sc-issue-claim-pipeline-flag each show exactly one tab, titled "... · Claude Code", and no empty tab. How they were created is not in N1 (no hand-typed create); see N8 for their daemon rows.
Worktrees from N1 own-use creates still live with an empty tab: fix-flaky-parallel-thread-test (955b0bcc), install-core-stale-warning (7fd4f558). Other N1 own-use worktrees (WorkerContractFollowups, P1Closeout, pr369-followup-record, ...) have no live terminals in the list.

## N8. Daemon tab starts per worktree (jq over ~/.config/orca/logs/daemon.log, `select((.sessionId // "")|test($w))`, event `startup-command-delivery`, fields ts, hasCommand, commandLength), captured 2026-11-08T01:56Z, verbatim tab-separated rows

Bare create, then work handed to another session in a NEW terminal (N1 rows af4401a8 and 44e7b6ec):
- gh-pin-latest: `2026-11-01T14:08:55.817Z	false	0` then `2026-11-01T14:09:27.326Z	true	70` (and later true rows)
- orca-idle-sleep: `2026-11-02T23:09:50.410Z	false	0` then `2026-11-02T23:09:56.028Z	true	28`
- ci-self-hosted-runners: `2026-11-04T15:50:48.974Z	false	0` then `2026-11-04T15:50:58.432Z	true	70`
- followup-notes-359-360: `2026-11-04T19:26:05.605Z	false	0` then `2026-11-04T19:26:16.164Z	true	70`
- specstory-symlink-home-fix: `2026-11-04T12:10:29.242Z	false	0` then `2026-11-04T12:10:45.190Z	true	70`
Reading: in all 5, the seeded plain tab (hasCommand=false, about 2 s after the create) is followed by a SEPARATE tab start that carries the agent command. The later launch does not reuse the seeded tab.

Bare create, own use (N1):
- install-core-stale-warning: `2026-11-07T05:36:16.234Z	false	0` only.
- fix-flaky-parallel-thread-test: `2026-11-07T20:35:31.197Z	false	0` only (rows with a sessionId containing the worktree name; later UI tabs use other ids).

Control (worktrees whose first tab carried a command; creation path not in N1):
- issue-473-claim: `2026-11-07T06:08:04.272Z	true	70`, `2026-11-07T06:20:37.667Z	true	70`
- issue-331-github-issue-watcher: `2026-11-07T06:41:35.707Z	true	70`
- sc-issue-claim-pipeline-flag: `2026-11-07T06:26:02.108Z	true	70`
Reading: no hasCommand=false row; consistent with a create where the caller provides the first surface (agent on create, IronOrca runtime-local-worktree-terminal-startup.ts:259-269). Which command created them is not captured here.

## N9. Bundled `orca skills get orca-cli` guide, grep -n -i for "worktree create|first terminal|terminal close|seed", captured 2026-11-08T02:00Z
Matches at lines 36, 44, 63, 71, 87-91, 98, 113, 115, 123, 131-134, 144, 154, 159. Line 63: "`worktree create --agent` (new checkout) and `agent launch` (existing worktree) are how to start an agent." Bare examples at 87-89, 91, 133-134 (e.g. `ORCA worktree create --name independent-task --no-parent --json`). No match for "first terminal" or "terminal close"; the only "seed" match is line 159 ("to seed links"), unrelated. The guide never says a bare create leaves a plain first terminal or how to close it.

## N10. How the control worktree issue-473-claim was created (transcript ~/.claude/projects/-home-coder-workspaces-Coder/7c1fa634-2b82-4c8d-8478-db376a53a5af.jsonl, Bash tool_use at 2026-11-07T06:08:02.558Z), captured 2026-11-08T02:01Z, `orca` portion verbatim (the long --spec text removed by the parent's sed):
`orca orchestration worker-start --run run_f0e2c5772f56 --task-title "Claim issue 473 (agent depth default 2)" --worktree new-top-level --name issue-473-claim --repo path:/home/coder/workspaces/Coder --base-branch origin/main --agent claude --json`
Reading: the control worktree was created by `worker-start --worktree new-top-level --agent claude`, so an agent was the first surface; its daemon row (06:08:04.272Z, hasCommand=true) is that agent. It was NOT created by orca_worktree.py's bare create, so M-CTRL does not conflict with P1. The /sc:issue in-script bare create (orca_worktree.py:594-610) remains unobserved in this run.

## N11. Has `/sc:issue --claim` (orca_worktree.py, worktree name `issue-<N>`) ever run on this host? Captured 2026-11-08T02:04Z
- `ls -d /home/coder/workspaces/worktrees/*/issue-[0-9]*` lists only issue-473-claim, issue-331-github-issue-watcher, issue-339-orchestrator-mode, issue-346-review-loop-convergence, issue-361-late-conflict-resync, issue-394-launch-level-hook: none is the bare `issue-<N>` name orca_worktree.py:602 uses.
- daemon.log sessionIds (format `<repo-id>::<worktree path>@@<suffix>` or `serve-<uuid>`) with `issue-<digits>` not followed by `-`: only ic-issue-389 and ic-issue-390 (an `ic-` prefix; not the script's name).
Reading: the script's bare create + `agent launch` path has not produced any captured tab on this host; whether it leaves a plain tab is predicted by P1 but unobserved.

## N12. Repo of each N1 bare create (from the worktree path in the same session's next commands, N1 table; and the `--repo`/base-branch in the create), derived 2026-11-08T02:07Z
- Own-use (11): IronClaude 10 (955b0bcc, 7fd4f558 x4, d9133120, 514abb0c x2, 0cf7ada3, 0798a6cf); Coder 1 (68fc8b81, path /home/coder/workspaces/worktrees/Coder/ironclaude-install-force).
- Hand-off (5): IronOrca 1 (44e7b6ec orca-idle-sleep, `--repo path:/home/coder/workspaces/IronOrca`); Coder 2 (44e7b6ec specstory-symlink-home-fix and ci-self-hosted-runners, `--repo path:/home/coder/workspaces/Coder` / `--repo path:$R` with R=/home/coder/workspaces/Coder); IronClaude 1 (44e7b6ec followup-notes-359-360, R=/home/coder/workspaces/IronClaude); Coder 1 (af4401a8 gh-pin-latest, base origin/main; repo inferred from the Coder project dir of that transcript, -home-coder-workspaces-Coder).
- Unclear (1): 347c98b7 IB-CPlus-01 (transcript dir -home-coder-workspaces-worktrees-Coder-IB-CPlus-01).
- Installed instruction check, 2026-11-08T02:06Z: `grep -c 'Orca session launches' ~/.claude/CLAUDE.md` → 0 (mtime 2026-11-05T13:13:32Z); same grep on src/superclaude/core/CLAUDE.md → 1.
Note: sessions in Coder or IronOrca load that repo's CLAUDE.md, not IronClaude's; whether those repos have a similar Orca-only rule was not checked.

## N13. Parent resolution of Tier 2 calibration gaps, captured 2026-11-08T02:10Z
- Path resolved: /home/coder/workspaces/IronOrca/src/main/runtime/workspaces/workspace-creation.ts exists. Read :200-271: `} = await startRuntimeLocalWorktreeTerminals({ ... createdWithAgent: effectiveCreatedWithAgent, promisedAgentChat: args.promisedAgentChat, ... })` at :209-231, then `return { worktree: {...}, ...(returnedSetup ...), ...(args.awaitTerminalProvisioning ? { setupReceipt: { ... ...(setupTerminalHandle ? { terminalHandle: setupTerminalHandle } : {}) } } : {}), ...(defaultTabs ? { defaultTabs } : {}), ...(warning ...) }` at :239-271. Reading (checkout source, not installed binary): the create awaits the terminal startup step, and the reply carries no seeded-terminal handle; only a setup terminal handle, and only with awaitTerminalProvisioning.
- `grep -rln awaitTerminalProvisioning src --include=*.ts` (non-test): rpc/methods/agent-launch-worktree-creation.ts, rpc/methods/orchestration/federation/federated-worker-agent-launch.ts, rpc/methods/orchestration/worker/worker-worktree-creation.ts, runtime-managed-worktree-create-types.ts, runtime-local-worktree-terminal-startup.ts, workspaces/workspace-creation.ts.
- When the "Orca session launches" rule entered the source: `git log -S 'Orca session launches' -- src/superclaude/core/CLAUDE.md` → `a368db4c 2026-11-06T22:19:55-05:00 fix(orca): launch Claude CLI sessions and refresh stale guides (#415)`. Reading: the 5 hand-off creates (2026-11-01 to 11-04, N8) predate the rule; a stale install cannot explain them. They ran with no rule at all about the first tab or about `--agent` on create.

## N14. Follow-up checks for the user's design questions, captured 2026-11-08T03:01Z
- The one hand-typed create WITH `--agent` (1779a921, 2026-11-06T20:48:50.892Z, `orca worktree create --name fix-claude-cli-session-launch --no-parent --agent claude --prompt ...`): daemon rows `2026-11-06T20:48:53.194Z	true	70` and `2026-11-06T21:57:34.511Z	true	70`; no `false` row. Reading: a create with `--agent` produces no plain first tab (second agent-backed case after N10).
- Existing deterministic precedent: `~/.claude/settings.json` PreToolUse matcher `Bash -> ~/.claude/hooks/block-bare-python.sh` and `Bash -> ~/.claude/hooks/launch-job-identity.sh`; sources at src/superclaude/hooks/scripts/block-bare-python.sh (header: "PreToolUse(Bash) UV-only gate (IronbellyOrg/IronClaude issue #357). Blocks a Bash tool call whose command runs bare `python` ... and tells the agent to use `uv run python`"), registered in src/superclaude/hooks/hooks.json:91, :101.
- No non-inference (hook, wrapper or Orca setting) option was evaluated by any Wave 3 card or the Wave 4 debate; the system-architect card rejected an Orca flag as sole fix because "agents would still need an instruction" (tier2-system-architect-hypothesis.md).

## Reproduction
No live repro: creating a worktree is a mutation and `re-run permitted` is unknown. The transcripts and daemon log are the captured evidence.
