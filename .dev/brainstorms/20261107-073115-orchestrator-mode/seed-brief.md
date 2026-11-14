---
topic: "Orchestrator mode: run and manage all sessions within a worktree @.dev/issues/339/issue-summary.md"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-11-07T07:33:00Z
---

# Seed Brief: orchestrator-mode

## Problem Statement

The person running IronClaude has many Claude Code sessions open at once across Orca worktrees (5-10 coordinators, 50-100 sessions per issue #409). Today they must open each session to learn whether it is working, waiting for them, stuck, finished, or safe to close. Issue #339 asks for one orchestrator session that every other session reports through, a periodic status report of all agents, sessions and worktrees, a `/sc:sweep` command that finds idle, stuck or timed-out sessions, and a `/sc:close` command that removes a worktree and branch only after strict checks.

Much of the base model already exists as the Orca coordinator/worker contract (`src/superclaude/core/WORKER-CONTRACT.md`, PR #368 and later). What is missing is: a shipped rule that the coordinator keeps polling until every session is finished; a single command that reads the state of every session in a worktree tree and says what needs the person; and a report surface. The owner chose (2026-11-07, via the coordinator) that the first PR delivers only a read-only `/sc:sweep` plus the static orchestrator status report on the #409 layout, with no new state store and no new security model. `/sc:close`, resume actions and signed grants are later phases that the design must record.

## Known Context

Socratic dialogue, deep tier, answered from `.dev/issues/339/` (issue summary, accuracy check, analysis F1-F12) and the owner's scope answer. No live session was asked.

**Batch 1, clarify**

- What hurts: the person cannot see, from one place, which sessions need them; sessions sit waiting on a held message or a question nobody reads (2026-11-05 incident, issue comment 2).
- Scope: one orchestrator over the sessions of one worktree tree (a feature worktree and its Orca child worktrees). Orchestrator of orchestrators is version 2.
- Constraint hierarchy: safety (never lose work, never act outward without the coordinator) beats completeness, which beats convenience.
- Who maintains: the IronClaude maintainers; the commands ship from `src/superclaude/` and install to `~/.claude/`.
- Migration tolerance: additive only; existing Orca workers and the worker contract keep working unchanged.

**Batch 2, validate**

- Existing patterns: Orca `worker-list` gives a per-worker liveness verdict (`live`, `unverifiable`, `exited`), `projection.attention` and `projection.nextAction` (`.dev/orca-command-refactor/inventory/orca-capabilities.md:37,123-127`). `sc-crash-recovery` already sweeps artifacts, session logs and git status read-only with `--all` and `--since` (default 72 hours). `ccsession --list` lists named sessions. Workers report on disk through `return-contract.yaml` (WC-4).
- Data model: no new store (owner choice A). The sweep reads Orca state, git state of each worktree, on-disk reports, and session logs, and writes one dated report file.
- Contract impact: `WORKER-CONTRACT.md` section 4 gains coordinator-loop rules (keep polling, re-arm after expiry, periodic sweep, when to tell the person). `/sc:sweep` joins the never-as-worker list as a coordinator command. `HOW-WE-WORK.md` "Orca coordination" (lines 396-405) and its plugin copy change with it.
- Operational impact: none at install time; the sweep runs only when the coordinator calls it.
- Rollback: delete the command and skill files and revert the contract paragraphs; no data to migrate.

**Batch 3, adversarial probe**

- 10x scale (500+ sessions): a sweep that shells out per session may be slow; the report must stay readable (group by needs-the-person first).
- Conflicts: the issue's "new worktree is always first choice" conflicts with the approved child-worktree trigger rule (CR-01); "logs, artifacts and plans are not valuable" conflicts with the `.dev/tasks/` always-staged rule; "resume on timeout" conflicts with WC-6 (a retry is a new Task) and WC-10 (a late heartbeat is absence, never death).
- Rejected alternative: a separate "orchestrator mode" protocol beside the worker contract (duplicates WC-3, WC-5, WC-6; analysis F1).
- Prior art: #409 observer TUI design (unmerged branch `docs/409-orca-dashboard-designs`, commit 495eb96d); Orca `worker-list`; `sc-crash-recovery`.
- Failure modes: Orca not running or not installed; a worktree removed mid-sweep; a session log unreadable; stale `worker-list` data; the sweep mistaking a slow worker for a dead one.
- Coupling points: the Orca CLI's JSON output shape (versioned by Orca, not this repo); ccsession's session store; git.
- Veto: the owner; outward actions stay with the coordinator (WC-9).
- Metric: the person can answer "who needs me and what is safe to close" from one report without opening any child session.
- 2-year reversibility: high, since the first phase writes only a report file.

## Constraints

- First phase is read-only: `/sc:sweep` reports and recommends; it never closes, resumes, kills, removes or messages a session, worktree or branch. Owner choice A, 2026-11-07.
- No new state store and no new security model in the first phase; state stays in Orca and on-disk reports.
- No standing service, management server, live sweep or live Orca/ccsession launch is built or run in this work; anything that needs one is recorded as a later phase.
- Extend the Orca coordinator/worker contract; do not create a parallel orchestrator protocol.
- `/sc:sweep` is coordinator-only (never-as-worker list); workers never take outward actions (WC-9).
- A late heartbeat is absence, never death (WC-10); only positive stall proof may recommend a stop. A retry of an Orca worker is a new Task (WC-6).
- The report layout reuses #409's design rather than inventing a second one; #409 stays the owner of the live observer TUI.
- `.dev/tasks/` content is never classed as disposable.
- Canonical sources live under `src/superclaude/`; `make sync-dev` mirrors them; installed primitives use `~/.claude/...` paths, never `src/superclaude/...`.
- Every behaviour must be testable with mocks (no live Orca, git remote or Claude session in tests). UV only.

## Success Criteria

- A coordinator can run `/sc:sweep` (default window 6 hours, as the issue asks) and get one dated report that lists every session and worktree in the tree with its state, what it is waiting for, and a recommended next action, with sessions needing the person listed first and kept until answered.
- The report follows the #409 layout and is written as a file on disk; the coordinator reads it as data.
- The sweep's classification is pure, deterministic and covered by mock-based tests (liveness verdicts, attention, git cleanliness, unpushed commits, unfinished ledgers).
- `WORKER-CONTRACT.md` states the coordinator loop rules (keep polling until every Task is settled; re-arm after expiry; periodic sweep) and lists `/sc:sweep` as coordinator-only; contract tests pin them.
- The design records every later phase: `/sc:close`, resume actions, the cross-session trust layer (typed messages, signed narrow grants), and the orchestrator of orchestrators, each with its blockers.
- `make verify-sync`, `make lint` and the affected tests pass.

## Open Questions

- Which session channel does the orchestrator rely on for non-Orca sessions: Orca messages only, or also Claude Code cross-session messages? (Analysis F2, F8, F9.) First-phase answer under choice A: Orca plus on-disk state only; non-Orca sessions appear in the report from ccsession and session logs but cannot be messaged.
- How exactly is the #409 layout available to this branch, given its design package is on an unmerged branch? Copy the layout spec into the design, or cite the branch commit?
- Is the sweep's data gathering a Python CLI subcommand (testable, deterministic) or a skill that runs shell commands (cheaper, harder to test)?
- What does "orchestrator management server" mean (issue body)? Not known; recorded as a later phase pending the owner's definition.
- Default window: the issue says 6 hours; `sc-crash-recovery` uses 72. Which wins for `/sc:sweep`?
- Comment 3's open questions (how a sender marks itself bypassing, whether a hook can check inbound cross-session messages, Macaroons versus Biscuit) belong to the trust-layer phase and its `/tech-research` and adversarial spike, not to phase 1.
