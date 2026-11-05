# Scout report

- Mode: claim
- Repo: IronbellyOrg/IronClaude
- Written by: issue-worker-t3

## Claim

- Issue: #315 — [Bug]: Agent spawned worktree sessins stuck at CCSession Session Name prompt
- url: https://github.com/IronbellyOrg/IronClaude/issues/315
- is_pull_request: false
- State: OPEN
- Assignees: ironbelly
- Current login: ironbelly
- Earlier claim comment ID: none
- Earlier accuracy-check comment ID: none
- Created at: 2026-10-28T03:58:19Z
- Labels: bug
- Author: ironbelly

### Issue body (full)

### Operating system

Linux

### version

_No response_

### Details

More of an issue than a bug.

I think our CCSession default prompt to get a name might cause issues in the event that another agent creates a worktree and session, as they will not be able to proceed.  They don't know, not even sure if they can, how to enter that session name and get into the session to do the work.  

I'm not exactly sure why the agents created these 2 worktrees tbh, but it will become more and more common so we'll need a way for agent sto be able to get past the prompt asking for the name

<img width="1230" height="1049" alt="Image" src="https://github.com/user-attachments/assets/fcc7204f-5a0b-4fbb-9c40-cd27fe34ec98" />

### Comments

1. clayphi, 2026-10-29, https://github.com/IronbellyOrg/IronClaude/issues/315#issuecomment-6503881798: A terminal's New Terminal hook consumes the agent's first command as the session name. Timer alone does not fix this. Fourteen Orca terminal/Claude launch variants showed no human-versus-agent identity signal apart from per-terminal IDs. Proposed heuristic: accept names containing only letters, digits, dot, underscore, hyphen; otherwise run input as a shell command at New Terminal, or as Claude's first message at ccsession-orca; skip the question on launch with a prompt. Nineteen local scenarios reportedly tested; single-word commands remain ambiguous and human names containing spaces would be mistaken for commands. Alternative: remove terminal auto-start and start ccsession manually. Asked owner to choose.
2. ironbelly, 2026-11-02, https://github.com/IronbellyOrg/IronClaude/issues/315#issuecomment-6582812978: Orchestrators manage most sessions; all Claude Code sessions should use ccsession. Requested assessment of explicit launch paths: human Session/Claude button uses ccsession-orca, requires a name, cancellation cancels; orchestrators explicitly supply name and task noninteractively while preserving Orca readiness/supervision/recovery; ordinary terminals are plain shells. Orca's CLI launchSource is telemetry, not a human/agent identity signal; current names support spaces. Verify deployed version, enforcement across direct launches, resumes, overrides and other entry points; test human, orchestrator and shell paths without input guessing.
3. clayphi, 2026-11-03, https://github.com/IronbellyOrg/IronClaude/issues/315#issuecomment-6610091534: Proposed plan later approved: retire Coder New Terminal autostart hook so terminals are plain shells; route Claude button via ccsession-orca and terminal `claude` via Coder's wrapper to ccsession; show a naming question and session list only when no task, name or resume is provided; auto-name launches without names, including prompt-bearing launches and timeouts; 30-second question timeout starts an auto-named session; Ctrl+C cancels to shell. Resume starts without a question. Prompt-bearing Orca launches start immediately, but worker-start and agent launch without prompt still reach the question, and typed tasks before timeout can be consumed as names. Proposed orchestrators always supply task or name, optionally with typed-line heuristic as a safety net; sought owner's view. Claude Agent Teams bypasses ccsession and routing it was also posed as an open question. Coder owns hook retirement and wrapper handoff; IronClaude owns ccsession and ccsession-orca changes. Proposed local workspace image testing across person, plain-terminal, agent and orchestrator paths before monitored PR.
4. ironbelly, 2026-11-04, https://github.com/IronbellyOrg/IronClaude/issues/315#issuecomment-6624500908: “Love it, lets go!” — approves the proposed plan, without explicitly resolving its two open questions.
5. ironbelly, 2026-11-05, https://github.com/IronbellyOrg/IronClaude/issues/315#issuecomment-6648419957: Owner takeover; assigned to ironbelly instead of clayphi. The November 4 agreed plan stands. This worker claims the issue and builds only the IronClaude part: ccsession and ccsession-orca, one naming-question rule, auto-name, 30-second timer, Ctrl+C cancels. Coder's terminal hook retirement and claude wrapper handoff are separately tracked and not started by this session.

### Merged pull requests since creation

- Result truncated at the 200 limit: no (36 returned; date search includes the entire creation date).
- Full returned PR records and all changed file paths: `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-315-ccsession-name-prompt/d362b83b-3e86-4b05-9ecb-53f9740cb19b/tool-results/b0il0sbyp.txt`. Paths below highlight session-related changes; other PRs have changed files in that complete record.

| PR | Title | Merged at | Changed files |
|---|---|---|---|
| #383 | fix(orca): drop the IronClaude-origin exemption; classify /sc:issue hits so master Tests pass | 2026-11-05 02:35Z | See full record |
| #380 | fix(issue): limit the create-mode slug to a-z, 0-9 and - | 2026-11-05 01:53Z | See full record |
| #378 | feat(pr-submit): merge conflict resolution | 2026-11-05 02:33Z | See full record |
| #377 | docs(testing): v5.0.0 impact validation instructions | 2026-11-04 22:38Z | See full record |
| #374 | docs(ccsession): roles above Member now start on Tier 1b | 2026-11-04 20:41Z | src/superclaude/skills/ccsession-tag/MODEL-TIERS.md |
| #373 | feat(issue): /sc:issue command | 2026-11-04 21:27Z | See full record |
| #369 | fix(install): harden pinned-plugin install | 2026-11-04 20:29Z | See full record |
| #368 | docs(orca): P0 live worker checks pass | 2026-11-04 21:33Z | See full record |
| #367 | docs(dev): merged PR follow-ups | 2026-11-04 19:35Z | See full record |
| #360 | fix(install): pin Ponytail | 2026-11-04 18:37Z | See full record |
| #359 | feat(hooks): block bare python/pip | 2026-11-04 18:37Z | See full record |
| #358 | feat(install): install Ponytail | 2026-11-04 15:18Z | See full record |
| #356 | refactor(worktrees): Orca default paths | 2026-11-04 06:12Z | See full record |
| #355 | fix(ccsession): relaunched Orca tab reopens its own session | 2026-11-03 18:44Z | src/superclaude/skills/ccsession-tag/{README.md,ccsession,ccsession-orca,hooks/session-name.sh}; tests/unit/{test_ccsession_tag.py,test_ccsession_tiers.py} |
| #353 | docs(post-release): v5.0.0 follow-through | 2026-11-03 13:04Z | See full record |
| #351 | chore(release): include #347 in 5.0.0 | 2026-11-02 21:39Z | See full record |
| #350 | fix(ccsession): session list follows worktree | 2026-11-02 21:22Z | docs/user-guide/session-management.md; src/superclaude/skills/ccsession-tag/{README.md,ccsession}; tests/unit/test_ccsession_tag.py |
| #349 | chore(release): 5.0.0 | 2026-11-02 21:21Z | See full record |
| #348 | chore(lint): exclude issue body files | 2026-11-02 21:19Z | See full record |
| #344 | feat(core): GitHub issue body files | 2026-11-02 15:06Z | See full record |
| #343 | fix(qa): minor findings and review loops | 2026-11-02 14:04Z | See full record |
| #342 | fix(ccsession): keep shared shim alive | 2026-11-02 18:16Z | src/superclaude/skills/ccsession-tag/{ccsession,local-gateway-alias-proxy.py}; tests/unit/test_ccsession_tiers.py; additional troubleshooting files in full record |
| #340 | fix(gitignore): keep tests in scope | 2026-11-02 03:21Z | See full record |
| #338 | fix(implement): minor findings and line drift | 2026-10-31 23:42Z | See full record |
| #337 | feat(pr-submit): Codex review threads | 2026-10-31 23:42Z | See full record |
| #336 | feat(codegraph): adopt in primitives | 2026-10-31 18:09Z | See full record |
| #335 | docs(plan): codegraph release monitor | 2026-10-31 18:08Z | See full record |
| #334 | chore(tasks): archive Phase 1 | 2026-10-31 01:29Z | See full record |
| #329 | feat: replace codebase-memory and Serena with codegraph | 2026-10-30 15:23Z | See full record |
| #328 | feat(ccsession): one session name for ccsession, Claude Code and Orca | 2026-10-30 11:09Z | docs/user-guide/session-management.md; src/superclaude/cli/install_ccsession.py; src/superclaude/skills/ccsession-tag/{README.md,SKILL.md,ccsession,ccsession-orca,hooks/session-name.sh,hooks/session-start.sh,install.sh}; tests/unit/{test_ccsession_tag.py,test_install_ccsession.py} |
| #327 | feat(mcp): opt-in litellm gateway | 2026-10-30 01:43Z | See full record |
| #321 | fix(ccsession): model tier slot window | 2026-10-28 19:04Z | src/superclaude/skills/ccsession-tag/{README.md,models.py}; tests/unit/test_ccsession_tiers.py |
| #319 | docs(research): recovered command evaluation | 2026-10-30 15:33Z | See full record |
| #318 | feat(ccsession): tiers by Coder role | 2026-10-28 17:01Z | src/superclaude/skills/ccsession-tag/{MODEL-TIERS.md,README.md,ccsession,ccsession-models.json,local-gateway-alias-proxy.py,models.py}; tests/unit/{test_ccsession_tag.py,test_ccsession_tiers.py} |
| #317 | chore(tasks): archive review-loops research | 2026-10-28 11:04Z | See full record |
| #316 | BrainstormBudget | 2026-10-28 04:29Z | See full record |

### Commits on the default branch since creation

- Fetched origin successfully. Complete `git log --since=2026-10-28T03:58:19Z --name-only origin/master`, including every commit and changed file, is at `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-315-ccsession-name-prompt/d362b83b-3e86-4b05-9ecb-53f9740cb19b/tool-results/bn2s7ba86.txt`. The following are relevant session changes, not an exhaustive list.

| Commit | Changed files |
|---|---|
| 8da537e6 | src/superclaude/skills/ccsession-tag/{README.md,ccsession,ccsession-orca,hooks/session-name.sh}; tests/unit/{test_ccsession_tag.py,test_ccsession_tiers.py} |
| 276c3257 | docs/user-guide/session-management.md; src/superclaude/skills/ccsession-tag/{README.md,ccsession}; tests/unit/test_ccsession_tag.py |
| 77d83d78 | src/superclaude/skills/ccsession-tag/{ccsession,local-gateway-alias-proxy.py}; tests/unit/test_ccsession_tiers.py; troubleshooting artifacts |
| 2e91e22d, ff5ed337, 7ef1c0e2 | src/superclaude/skills/ccsession-tag/ccsession; tests/unit/test_ccsession_tag.py; README.md in latter two |
| 7dac79ab | docs/user-guide/session-management.md; src/superclaude/cli/install_ccsession.py; src/superclaude/skills/ccsession-tag/{README.md,SKILL.md,ccsession,ccsession-orca,hooks/session-name.sh,hooks/session-start.sh,install.sh}; tests/unit/{test_ccsession_tag.py,test_install_ccsession.py} |
| 40e41ab0, e328b23c, fab74603 | ccsession model/tier files and tests; see complete log |

### First guesses

- Complexity: complex: several launch modes, interactive timeout and cancellation, naming, resume, and supervision compatibility require coordinated changes and tests.
- Type: bug: agent launches can be blocked or their command consumed by a naming prompt.
