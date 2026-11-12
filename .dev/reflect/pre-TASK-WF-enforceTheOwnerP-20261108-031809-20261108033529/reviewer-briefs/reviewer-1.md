# Reviewer 1 brief — persona: analyzer (model class: sonnet)

Mode: UC-1 pre-execution. Audit the proposed plan `.dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/TASK-WF-enforceTheOwnerP-20261108-031809.md` against its source `.dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/source.md` (repo root `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test`). Your lens: root cause and deviations — does each task actually achieve the source's intent (every Orca worktree gets an agent; deterministic enforcement), are deviations justified and documented, and would any task as written fail or leave the problem in place? You are read-only; audit the supplied refs with Read/Grep/Glob; run nothing.

## T1 card excerpt

(verbatim from t1-card.md)

- Documented deviations: agent-not-with-create (FO-18, D2 kept) at plan :20; `none` no-worktree at :19.
- INF-014, INF-015 are containment false positives: they match Tasks 3/4 by word overlap but those tasks do something different from source.md:1 scope item 2 (plan :51-64); covered only by the Constraints deviation. Record as "covered by deviation", not "matched".
- Undocumented consequence: a claim whose `agent launch` fails (`W-LAUNCH-FAILED`) leaves a worktree with no agent and no tab, breaking "every worktree gets an agent"; no task or Constraint acknowledges it.

| id | sev | task | claim | evidence | recommended change |
|---|---|---|---|---|---|
| F1 | HIGH | 1 | Scanner reuse understated: block-bare-python.sh records only the command word and exits at first match (:130-134), returns early on `!need[o]` (:106); the new hook needs per-command argument tracking (`worktree`, `create`, `--agent`, `--help`) resetting at separators, which does not exist. | block-bare-python.sh:99-135 | Say the scanner must be extended with per-command word collection; add tests for `env X=1 orca …`, `sudo orca …`, `command orca …`, `orca … ; orca worktree create --agent x`, heredoc into a shell; list ceilings (`bash -c`, `eval`, `xargs`, `--bare`) in the header as the sibling does at :48-61. |
| F4 | MEDIUM | 6 | CLAUDE.md:305 "give each session its own worktree" and Usage :335-337 (sessions open their own worktrees) contradict "no session creates a worktree for its own use"; Task 6 edits only :312, :320. | CLAUDE.md:305, :333-337 | Add both spots to Task 6 and the new test. |
| F5 | MEDIUM | 3 | Close-step timing and missing cases: seed awaited inside create (runtime-local-worktree-terminal-startup.ts:209-210) but CLI-reply waiting not shown; timed-out create (orca_worktree.py:611, 628) has no reply; reply is an envelope `{"ok","result":{…}}` (LAUNCH_OK at test_issue_orca_worktree.py:970), so keys sit under `result`. | as cited | Read `result.setup`/`result.defaultTabs`; timed-out or unparseable reply → `W-FIRST-TAB-LEFT`, no close; tests for both; keep Task 8 live check blocking. |
| F6 | MEDIUM | 3, 5 | Deviation leaves an agentless worktree when launch fails or the user stops after create. | plan :20; claim.md:123 | Constraint line accepting this, pointing at `W-LAUNCH-FAILED` remedy; mention in Task 5 doc note. |
| F10 | LOW | 8 | Humans, Codex/other agents, `claude --bare` not covered by the hook; delivery note silent. | block-bare-python.sh:61 | Add a "not covered" line to t8-delivery.md. |

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T01:51Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test projectPath=/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test

### src/superclaude/hooks/scripts/block-bare-python.sh:1-135
(Read the file: header contract, ceilings :48-61, scanner :99-135.)

### src/superclaude/hooks/scripts/launch-job-identity.sh:1-20
(Header: "updatedInput replaces the WHOLE input; omit permissionDecision so ordinary permission checks still apply. Other hooks' rewrite ordering is unspecified.")

### src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:590-660, :905-1003
(Create call, new-row handling, `cmd_launch` with pending record before `orca agent launch`.)

### /home/coder/workspaces/IronOrca/src/main/runtime/workspaces/workspace-creation.ts:200-290
(Create awaits `startRuntimeLocalWorktreeTerminals`; reply keys `setup`, `defaultTabs`, setup handle only with `awaitTerminalProvisioning`.)

### /home/coder/workspaces/IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:187-269
(Provisioning branch fire-and-forget; seed branch :202-214; `callerProvidesInitialSurface` :259-269.)

### CLAUDE.md:303-340
(Worktree section to be edited.)

### .dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/tier1-observation.md (N1, N8, N10, N13, N14)
(Captured evidence: 17 of 18 creates bare; seeded plain tab in 7 of 7; agent-on-create leaves no plain tab.)

## Coverage slice

| Requirement | Matched task | Status | Note |
|---|---|---|---|
| INF-001..003 policy (every worktree gets an agent; no own-use; creator owns agent) | Task 6, Task 7 | covered | text + hook enforce |
| INF-004 enforcement must be deterministic | Constraints | covered by constraint | |
| INF-005..009 hook behaviour | Task 1 | covered | see F1 |
| INF-014 /sc:issue agent comes with the create | Task 3 | covered by deviation | plan :20 |
| INF-015 keep `agent launch` only for an existing worktree | Task 4 (word overlap) | covered by deviation | false positive |
| INF-016 pending record before agent starts | Task 5 (word overlap) | covered by Task 3 ordering | check |
| INF-026..029 out-of-scope items | Constraints | covered by constraint | |
