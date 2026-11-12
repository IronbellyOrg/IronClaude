# Tier 1 observation (captured 2026-11-07T23:55Z to 2026-11-08T00:00Z, parent session, same-shell read-only)

## Behaviour definitions
Row 1 (behaviour-definitions.md): Orca seeds a plain terminal on a create with no agent. Verbatim from /home/coder/workspaces/IronOrca (local checkout HEAD dc57b3d6e8, not proven equal to the installed 1.4.245-aidev02):

src/main/runtime/runtime-local-worktree-terminal-startup.ts:202-214
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
src/main/runtime/runtime-local-worktree-terminal-startup.ts:259-269
```
function callerProvidesInitialSurface(args): boolean {
  // Background agent creates already leave their initial surface to the caller.
  return (
    args.promisedAgentChat === true ||
    (args.createdWithAgent !== undefined &&
      args.request.activate !== true &&
      args.request.runHooks !== true)
  )
}
```
src/shared/worktree-first-surface.ts:2-14
```
export function shouldSeedWorktreePrimaryTerminal(args: {hasPrimarySurface: boolean; callerProvidesSurface: boolean; startupNeedsTerminal?: boolean; issueCommandNeedsTerminal?: boolean}): boolean {
  return (
    !args.hasPrimarySurface &&
    (!args.callerProvidesSurface ||
      args.startupNeedsTerminal === true ||
      args.issueCommandNeedsTerminal === true)
  )
}
```
Reading: with no startup pane held (`hasPrimarySurface` false) and no agent on the create (`callerProvidesSurface` false), the function returns true and `createTerminal` runs with no startup agent: a plain shell.

## O1. Orca CLI help (orca 1.4.245-aidev02.780594c521aa)
- `orca terminal create --help`: "This creates a terminal and runs --command in it. To start an agent, use `orca agent launch` (or `orca worktree create --agent` for a new checkout), which follows your Chat UI setting."
- `orca orchestration worker-start --help`: "--agent <id> Launch a known TUI agent in the first terminal ... a fresh agent terminal is created unless --terminal is explicit ... How the worker runs follows the user's own setting for new agent tabs; there is no flag for it."
- Orca UI shortcuts (IronOrca src/shared/keybindings/definitions-core-2.ts:69-81): `tab.newTerminal` = Mod+T "New terminal tab"; `tab.newAgent` = "New agent tab (default agent)".

## O2. Daemon log, ~/.config/orca/logs/daemon.log (jq over `startup-command-delivery`)
- Tabs started with no command (plain shells), per day: 10-27: 22, 10-28: 48, 11-02: 27, 11-04: 15, 11-05: 41, 11-06: 25, 11-07: 22. Tabs with a startup command are present every day.
- 2026-11-07T23:52:18Z: a `serve-` session with hasCommand=false; 2026-11-07T23:52:23Z: a `serve-` session with hasCommand=true (length 70). Five seconds apart, same worktree as this session. The log does not say who requested either.
- The log has no field naming the caller, so "empty tab" cannot be tied to an orchestrator from it.
- Verbatim capture (jq over daemon.log, `select((.sessionId // "")|test("install-core-stale-warning"))`, `[.ts,.event,(.hasCommand|tostring),(.commandLength|tostring)] | @tsv`, run 2026-11-08T00:02Z, tab-separated):
  `2026-11-07T05:36:16.234Z	startup-command-delivery	false	0`
  `2026-11-07T05:36:16.234Z	session-created	null	null`
  No other row for that worktree path. (Same-turn probe output, the source of Evidence item 9.)

## O3. Live tabs, `orca terminal list --json` at 2026-11-08T00:00Z
- Tabs with no "· Claude Code" title: install-core-stale-warning (term_19ed8a7e), Ironeye (term_6c4f59e4), fix-flaky-parallel-thread-test (term_9fe9e46e, term_ee0007a6).
- Every supervised worker tab in `orca orchestration worker-list --run run_93bfa00cae2b` has a "· Claude Code" title; 4 are `live`, 3 `exited`, 4 `unverifiable/stale_status`.
- Named reference-arm capture (same-turn output of the two read-only commands above, recorded verbatim by the parent after validation drop D1):
  `orca terminal list --json` row: `term_8c37967b-4b54-4b2a-89c5-3ea98c9f4277	liveness-v1-contract-1107-211733-7356 · Claude Code	ces/worktrees/IronClaude/liveness-v1-contract`
  `orca orchestration worker-list --run run_93bfa00cae2b --json` row: `ctx_3a6e5a8b9548		{"verdict":"live","observedAt":1794095910431,"source":"agent_status"}	term_8c37967b-4b54-4b2a-89c5-3ea98c9f4277`
  This is the observed reference value `true` for tasklist row M-QE (a worktree with a started worker has a "· Claude Code" tab).

## O4. Orchestrator commands, Claude transcript ~/.claude/projects/-home-coder-workspaces-IronClaude/1779a921-dc86-44c8-867c-d5e117eb8e31.jsonl (Bash tool_use inputs)
- Zero real `orca terminal create` calls in any transcript under ~/.claude/projects (the 6 and 1 counts were my own `--help` runs and a prompt that quotes issue #412).
- Every supervised spawn from 2026-11-07T06:15 onward is `orca orchestration worker-start ... --agent claude` (06:15, 06:16, 06:25, 06:41, 07:16, 07:23, 09:16, 11:44).
- One `orca worktree create --name install-core-stale-warning --no-parent --base-branch origin/master` with no `--agent` at 2026-11-07T06:15:04Z; that worktree has only an empty plain terminal (O3). Calls to `orca worktree create` since 11-05 with no `--agent`: 9; with `--agent`: 3 (transcript counts).

## O5. Instruction delivery
- Fix #415 (a368db4c, 2026-11-06T22:19:55-05:00, ancestor of origin/master) added the "Orca session launches" rule at src/superclaude/core/CLAUDE.md:45-53 and src/superclaude/skills/ccsession-tag/README.md:228-237.
- Installed copies do NOT have it: ~/.claude/CLAUDE.md (modified 2026-11-06T11:13:49) has 0 matches for "Orca session launches"; ~/.claude/skills/ccsession-tag/README.md has 0 matches; the pipx package (~/.local/share/pipx/venvs/superclaude/.../core/CLAUDE.md, built 2026-11-05 13:13:32) has 0 matches.
- Project CLAUDE.md (this repo) lines 308 and 320 tell agents to create worktrees with `orca worktree create --name <name>` and show `orca worktree create --name pm-agent --base-branch origin/master`, with no `--agent` and no mention of starting a Claude session.
- The Orca-bundled `orca-cli` guide (`orca skills get orca-cli`) already says to use `agent launch` / `worktree create --agent` to start an agent (lines 49-63, 144, 240) and lists `terminal create` for shells (line 207).
- Clarification to O4: the transcript 7fd4f558 ran the bare create for install-core-stale-warning at 2026-11-07T05:36:13Z (daemon session 05:36:16Z, hasCommand=false, no other session for that path); the coordinator's 06:15:04Z command used the same name and left no second daemon session.

## Behaviour definitions, rows 2-6 (verbatim; IronOrca checkout HEAD dc57b3d6e8, not proven equal to installed 1.4.245-aidev02)
Row 2, /home/coder/workspaces/IronOrca/src/main/runtime/rpc/methods/orchestration/worker/worker-topology.ts:67-76
```
  const terminal = await args.runtime.createTerminal(`id:${args.worktreeId}`, {
    startupAgent: args.agent,
    launchSource: 'orchestration',
    suppressStartupUpdatePrompt: true,
    ...(args.launchPreferences ? { launchPreferences: args.launchPreferences } : {}),
    title: `worker-${args.taskId}`,
    surfaceOwner: false
  })
```
Row 3, .../worker/explicit-worker-terminal-validation.ts:49-54
```
  if (!(await runtime.isTerminalRunningAgent(terminal))) {
    throw new OrchestrationError('agent_unconfigured', `Terminal ${terminal} is not running a recognized agent.`)
  }
```
Row 4, .../worker/worker-start-receipt.ts:86-112 (excerpt)
```
    state: worker.state === 'start_unknown' ? 'outcome_unknown' : worker.state,
    failedStage: args.failedStage,
    lastError: reason,
    effects: JSON.parse(worker.effects) as unknown[],
    residualResources: JSON.parse(worker.residual_resources) as unknown[],
    ...(releasable ? { recovery: `This start created a terminal that never ran the Task. Close it with: orca orchestration worker-release --dispatch ${args.dispatchId}` } : {}),
    ...(unknown ? { nextCommands: [`orca orchestration worker-show --dispatch ...`, `orca orchestration worker-abandon --dispatch ...`] } : {})
```
Row 5, /home/coder/workspaces/IronOrca/src/main/providers/local-pty-shell-ready-startup-command.ts:45-50
```
    // Keep the interactive shell alive after agent exit; write once past readiness to avoid incremental-paste drops.
    proc.write(buildStartupCommandSubmission(startupCommand, {bracketedPasteSafe: options.bracketedPasteSafe === true}))
```
Row 6, src/superclaude/cli/install_core.py:70-72
```
        if dest_file.exists() and not force:
            skipped.append(src_file.name)
            continue
```
and :94-105: kept files that differ print "NOT updated (run with --force or `superclaude update` to refresh)".
Reading: a failed start returns a receipt that names a terminal "that never ran the Task" (an empty tab) and tells the orchestrator to release it; a start into an existing worktree creates a new `worker-<taskId>` terminal rather than reusing a seeded one; a plain install keeps an existing ~/.claude/CLAUDE.md.
