# /sc:analyze --depth deep: orchestrator mode (#339) against today's coordinator code

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/339
- Checked at: `origin/master` = `e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b` (2026-11-07); open PR #422 also read (file list only).
- Target: `src/superclaude/core/WORKER-CONTRACT.md` (main path), plus `src/superclaude/core/HOW-WE-WORK.md` "Orca coordination", `src/superclaude/skills/sc-crash-recovery/`, `src/superclaude/skills/ccsession-tag/`, `src/superclaude/output-styles/pragmatic.md`, `src/superclaude/hooks/scripts/launch-job-identity.sh`, `.dev/orca-command-refactor/`, and the registries a new command must join.
- Focus: architecture (where an orchestrator mode, `/sc:sweep` and `/sc:close` sit), plus security for the cross-session trust proposal in comment 2.
- Tools: Read, Grep, Glob and Bash (read-only `git` and `gh`). codegraph and auggie were not used: the targets are Markdown contracts and shell scripts, which Grep and Read cover.

## 1. Discover: what exists today

| Component | Path | Role for #339 |
|---|---|---|
| Worker contract (156 non-blank lines) | `src/superclaude/core/WORKER-CONTRACT.md` | Terms (worker run vs ordinary session, line 11), command rules WC-2/4/8/9/10/11, worker duties WC-3/5/7/12/13, coordinator rules (section 4, lines 64-164), brief template (section 5). This is the orchestrator protocol in all but name. |
| Routing guide section | `src/superclaude/core/HOW-WE-WORK.md:396-405` | Says the coordinator is a session the person opened and owns every outward action. Copied byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. |
| Contract tests | `tests/skills/test_worker_contract.py` | Pin rule text, the never-as-worker list (`NEVER_AS_WORKER`, line 245; test at 545), the brief layout and every `## Unattended mode` section. Any contract edit must keep these green. |
| Orca facts inventory | `.dev/orca-command-refactor/inventory/orca-capabilities.md` | Message types (line 75), `ask`/`reply` (56-68), liveness verdicts and `worker-list` attention/nextAction (120-131), identity outside Orca (143-151). |
| Placement change | `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md` | Child worktree only on triggers T1-T4; merge-back and cleanup by the git owner. Carried into WC-11 and section 4 of the contract. |
| Decisions log | `.dev/orca-command-refactor/decisions/APPROVED.md` | P1 PASS (line 82); P1-C5 (whether a worker that only reads a command file satisfies WC-7) was left open for P2 (line 83). |
| Crash recovery | `src/superclaude/skills/sc-crash-recovery/SKILL.md:25-29` | Read-only fleet sweep, `--all`, `--since` (default 72 hours). Nearest existing "sweep". |
| ccsession | `src/superclaude/skills/ccsession-tag/ccsession:135-139`, `README.md:125` | Launch flags (bypass by default, `CCSESSION_PERMISSIONS=default` turns it off); `ccsession --list` per worktree. |
| Output style | `src/superclaude/output-styles/pragmatic.md:22,53` | Mandatory DONE / NEXT table, "No exceptions"; the issue wants it replaced in orchestrator mode. |
| Job identity hook | `src/superclaude/hooks/scripts/launch-job-identity.sh:2-9` | Same-user identity for governed Bash; explicitly "not a sandbox". Not a grant layer. |
| #409 designs | branch `docs/409-orca-dashboard-designs`, commit 495eb96d | Read-only observer TUI design; unmerged. The static report layout should come from here. |
| Local, uncommitted work | `.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md`; `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/research/scope-01..04-*.md` | A deep brainstorm seed (owner scope choice recorded there: first PR = read-only `/sc:sweep` plus a static report, no new store, no new security model) and four complete research scopes. No synthesis, QA, review or final report yet. |

## 2. Scan: findings

Severity: High = blocks a correct design or risks lost work; Medium = will cause rework or a failing test; Low = wording or follow-up.

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | High | The issue's orchestrator is already specified as the Orca coordinator. A second "orchestrator mode" protocol beside the contract would duplicate WC-3 (questions), WC-5 (outcome), WC-6 (retry) and section 4 (cleanup, git ownership). Extend section 4 instead. | `WORKER-CONTRACT.md:52-58,64-129` |
| F2 | High | "All sessions report through the orchestrator" cannot reach sessions Orca did not start: only a session with a live preamble (Task and Dispatch IDs) may send lifecycle messages; an ordinary session has no orchestration identity and is refused. Interactive peers must be observed (session logs, git, ccsession), not messaged. | `WORKER-CONTRACT.md:11`; `orca-capabilities.md:148-151`; owner memory note: "Peer sessions ... do not appear in the Orca message queue at all" |
| F3 | High | "Resume on timeout or ECONNREFUSED" conflicts with WC-10 and WC-6: a late heartbeat is absence, never death; only positive stall proof settles a worker, and a retry is a new Task. A sweep may recommend a stop only on `exited` liveness or a final turn without `worker_done`. | `WORKER-CONTRACT.md:45,70-74`; `orca-capabilities.md:125-126` |
| F4 | High | "Artifacts and plans are not valuable" conflicts with the `.dev/tasks/` always-staged rule. `/sc:close` must treat `.dev/tasks/` as valuable and refuse deletion while it holds untracked or unstaged content. | `CLAUDE.md` ABSOLUTE RULE; `WORKER-CONTRACT.md:117` |
| F5 | High | `/sc:close`'s safety checks largely exist as coordinator refusals (unmerged commits, open PR, uncommitted changes, unfinished ledger, unread report), but as prose, not a check a command runs. "All commits pushed" is missing (a child can be merged locally into the feature branch while the feature branch is unpushed). Removal must use `orca worktree rm`, never raw git. A frozen `/sc:implement` worktree must never be removed. | `WORKER-CONTRACT.md:103,107-108,133-136` |
| F6 | Medium | `/sc:sweep` and `/sc:close` act across sessions and worktrees, so both belong on the never-as-worker list (coordinator-only). That list is pinned by a test named for "all seven commands" and a one-line check, so adding them changes `tests/skills/test_worker_contract.py` (lines 245, 400-403, 545). | `WORKER-CONTRACT.md:23`; test file lines cited |
| F7 | Medium | A new command must join the registries: `tests/recommend/test_routing_refresh.py:33` (`_POST_REFRESH_ADDITIONS`, asserted at 648), the "Other commands" table at `HOW-WE-WORK.md:318-337` and its test set in `tests/core/test_how_we_work_routing_table.py` (per research scope 03), the plugin byte copy of the guide, and `docs/user-guide/commands.md`. | `test_routing_refresh.py:33,648`; `HOW-WE-WORK.md:318,337`; `scope-03-cli-patterns.md:131-150` |
| F8 | Medium | Open PR #422 (P2) edits `WORKER-CONTRACT.md` and 15 command files. Contract edits for #339 made before #422 merges will conflict; sequence #339's contract change after #422, or keep the first PR to new files only. | `gh pr diff 422 --repo IronbellyOrg/IronClaude --name-only` |
| F9 | Medium | The "keep polling indefinitely" owner order is not in any shipped file; it lives only in a private memory note (re-arm `check --wait` after every expiry, periodic sweep, renew idle subscriptions). Shipping it means a new coordinator-loop rule in section 4. | owner memory `coordinator-never-stop-polling.md`; `WORKER-CONTRACT.md:45` |
| F10 | Medium | Replacing the end-of-message table needs an explicit exception in the pragmatic output style, which today says "No exceptions". Otherwise a coordinator under that style must print both. | `pragmatic.md:22,53` |
| F11 | Medium | Sweep defaults disagree: the issue asks for 6 hours, `sc-crash-recovery` uses 72 hours. Pick one default and state it; reuse crash-recovery's signals rather than re-implementing them. | `sc-crash-recovery/SKILL.md:26,29` |
| F12 | Medium | "A new worktree is always the first choice" conflicts with the approved trigger-based placement (CR-01, WC-11). | `WORKER-CONTRACT.md:46,87`; `CR-01-feature-worktree-hierarchy.md:12-21` |
| F13 | Low | `/orchestration` is an Orca discovery stub that defers to the `orca` binary's own guide; it cannot be "incorporated" into a repo skill without copying version-specific syntax, which the contract forbids (line 7). Reference it; do not copy it. | `~/.claude/skills/orchestration/SKILL.md:16-18`; `WORKER-CONTRACT.md:7` |
| F14 | Low | "Orchestrator management server" has no counterpart in the repo. Not known yet whether it means Orca or the #409 observer. | Grep: no hit |

## 3. Security: the cross-session trust proposal (comment 2)

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| S1 | High | Step 1 ("everyone in bypass mode") is undermined by `CCSESSION_PERMISSIONS=default`, which launches without the bypass and recreates the mismatch that held the message. Any orchestrator launch rule must state which mode it uses and refuse mixing. Running everything in bypass also widens the blast radius of a poisoned child (the issue's own section 3). | `ccsession:135-139`; PR #403 |
| S2 | High | Step 2 (fixed message types) already holds for Orca workers: fixed `--type` values, `ask`/`reply`, and reports as on-disk YAML the coordinator reads as data. The gap is only the Claude Code cross-session channel. Prefer routing children through Orca workers over hardening that channel. | `orca-capabilities.md:58-67,75`; `WORKER-CONTRACT.md:31-38` |
| S3 | Medium | Step 3 (macaroon/Biscuit grants) has no design, library choice or code. PR #414's job identity is same-user and "not a sandbox", so it cannot carry grants. This is version-2 work and needs the comment-3 research and debate first. | `launch-job-identity.sh:2-9`; grep: no macaroon/Biscuit in committed files |
| S4 | Medium | Step 4 (gate destructive actions) is partly in place: WC-9 bars workers from every outward action, and section 4 requires the user's named instruction plus a confirmation at the moment of action. `/sc:close` must keep that confirmation, not bypass it. | `WORKER-CONTRACT.md:40-43,112-117` |
| S5 | Low | Open questions 1-2 (how a sender marks itself as bypassing; whether a hook can inspect inbound messages) are not covered by the local research package's four scopes. | `TASK-RESEARCH-orchestrator-supervision-20261107-073942/research/` |

## 4. Recommend

1. Treat #339 as an extension of the Orca coordinator contract, not a new protocol (F1). Phase it:
   - Phase 1 (the owner's first-PR scope recorded in the local seed brief): a read-only, coordinator-only `/sc:sweep` that reads Orca `worker-list`, git state per worktree, on-disk return contracts, crash-recovery signals and `ccsession --list`, and writes one dated report on the #409 layout; plus the "keep polling" coordinator-loop rule in section 4. No close, resume, kill or message actions.
   - Phase 2: `/sc:close`, turning the section 4 refusals into executed checks, adding "all commits pushed" and the `.dev/tasks/` rule (F4, F5), removal through `orca worktree rm` only.
   - Phase 3 (version 2): the trust layer and orchestrator of orchestrators, after the comment-3 research and the macaroon-versus-Biscuit debate (S3, S5).
2. Land contract edits after PR #422 merges (F8).
3. Add each new command to the never-as-worker list and the registries in F6 and F7 in the same PR as the command.
4. Decide the output-style exception (F10) and the sweep default window (F11) in the plan, not during implementation.

## 5. Report: metrics

- Claims checked: 20 (accuracy check): changed 12, still true (not built) 6, not known yet 2.
- Merged PRs relevant: 13 of 46. Open PR in conflict: 1 (#422).
- Findings: architecture 14 (High 5, Medium 7, Low 2); security 5 (High 2, Medium 2, Low 1).
- Subsystems touched: worker contract and its tests; routing guide and its copies; command registries; ccsession launch; output style; Orca CLI (external); a future trust layer.
