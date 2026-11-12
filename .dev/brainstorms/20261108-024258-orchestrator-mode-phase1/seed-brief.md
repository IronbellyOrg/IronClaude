---
topic: "Orchestrator mode Phase 1 for issue #339: a read-only, coordinator-only /sc:sweep that classifies Orca and ccsession sessions over a 6 h activity window and writes a dated static report, plus a WC-14 coordinator-loop rule in WORKER-CONTRACT.md. Inputs: research report .dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md (recommended option A1, summary at synthesis/phase7-summary.md), gaps log gaps-and-questions.md in the same folder (88 open rows; GQ-101 to GQ-113 must be resolved at /sc:design, safety item GQ-103(1) --no-optional-locks first), and the earlier brainstorm folder .dev/brainstorms/20261107-073115-orchestrator-mode/. Read reports with offset and limit, at most 150 lines per read."
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-11-08T03:05:00Z
---

# Seed Brief: orchestrator-mode-phase1

Abbreviations used below: TASK = `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`; REPORT = `TASK/RESEARCH-REPORT-orchestrator-mode.md`; GAPS = `TASK/gaps-and-questions.md`.

## Problem Statement

A person running IronClaude has many Claude Code sessions open across Orca worktrees and must open each one to learn whether it is working, waiting for them, stuck, finished or safe to close. The worker contract has no rule that the coordinator keeps polling, re-arms an expired wait, or sweeps on a schedule (REPORT line 48; `src/superclaude/core/WORKER-CONTRACT.md:45`). The first PR for issue #339 must give the coordinator one read-only command, `/sc:sweep`, that classifies every Orca worker and ccsession session in one worktree tree over a 6 h window and writes one dated static report, and must add the WC-14 coordinator-loop rule. The deep research is done and recommends option A1 (REPORT line 1098); this brainstorm turns that plan, plus its carried gaps, into requirements the spec panel and `/sc:design` can check.

## Known Context

Deep tier, three batches, answered from REPORT, GAPS, `TASK/synthesis/phase7-summary.md` and the earlier brainstorm (`.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md`). No live session was asked. Codebase context: `enrichment/codebase-context.md`.

**Batch 1, clarify**

- What hurts: no single view of who needs the person; sessions sit on a held message or unread question (issue comment 2, 2026-11-05 incident).
- Scope: one coordinator over one worktree tree (a feature worktree and its Orca child worktrees). Orchestrator of orchestrators is later (REPORT line 1331).
- Constraint order: safety (never disturb a live worker, never act outward) over completeness over convenience.
- Maintainers: IronClaude maintainers; sources under `src/superclaude/`, installed to `~/.claude/`.
- Migration: additive; existing workers and WC-2 to WC-13 keep working; WC-14 is the next free rule ID (REPORT line 70).

**Batch 2, validate**

- Pattern chosen: A1, a Python CLI `superclaude sweep run` (package `src/superclaude/cli/sweep/`: `models.py`, pure `classify.py`, `probes.py` with single `_orca` and `_git` seams and an exact argv allowlist, `report.py` as the only write, Click `commands.py`), a thin `/sc:sweep` command and an `sc-sweep-protocol` skill (REPORT Section 8 steps 1.1 to 1.16).
- Data model: no new store. Inputs are Orca read verbs, `git status` of each worktree, task-package ledgers, ccsession and transcript files. Output is one dated Markdown report.
- Contract impact: WC-14 "Coordinator loop" in `WORKER-CONTRACT.md`, `/sc:sweep` added to the never-as-worker list, contract-test pins, routing registries, `HOW-WE-WORK.md` plus its plugin byte copy (steps 1.17 to 1.24b).
- Operational impact: none at install; the sweep runs only when the coordinator calls it.
- Rollback: delete the new package, command and skill; revert the contract and docs; no data migration (GQ-106 adds `.dev/sweeps/` to the rollback table).

**Batch 3, adversarial probe**

- Scale: unknown `worker-list` row schema, so plan for ceil(N/100) list calls plus N `worker-show` calls, bounded at 50 (REPORT line 1164; GQ-01, GQ-104).
- Conflicts: a sweep's plain `git status` can take a live worker's `index.lock`, and WC-9 makes that worker report `blocked` (GQ-103(1)); committed `.dev/tasks/` folders are shared by every worktree, so a naive "package in two worktrees" check flags all of them (GQ-101).
- Rejected alternatives: A4, extend `sc-crash-recovery` (it allows `git stash` and has scanner bugs, REPORT line 325); a skill-only sweep (not mock-testable, fails K-4).
- Prior art: #409 observer design, unmerged at `495eb96d`; this work picks its header, Attention Ledger and Shift Brief (REPORT line 328); Kubernetes, gRPC health and Nagios treat "unknown" as its own state (REPORT line 1148).
- Failure modes: Orca absent; worktree removed mid-sweep; unreadable transcript; stale list data; slow worker read as dead (WC-10: a late heartbeat is absence, only Orca's stall proof counts).
- Veto: the owner; outward actions stay with the coordinator (WC-9).
- Success metric: the person answers "who needs me and what is safe to close" from one report without opening a child session.
- 2-year reversibility: high; Phase 1 writes only a report file.

## Constraints

- Read-only: the sweep never closes, resumes, kills, removes, stashes or messages anything; the report file is its only write. Every `_git` call runs with `--no-optional-locks` (GQ-103(1), safety item, first).
- Coordinator-only; never run by a worker.
- No new store, no new security model, no standing service, no live Orca, ccsession or Claude launch in tests or in this work.
- Extend the worker contract; no parallel orchestrator protocol. WC-6 (a retry is a new Task) and WC-10 hold.
- "Could not determine" is its own class, never folded into stalled or idle.
- `.dev/tasks/` content is never disposable; the sweep never advises deleting it.
- Installed primitives use `~/.claude/...` paths; `make sync-dev`; never stage `.claude/` except `settings.json`; UV only.
- Every behaviour is testable with mocks at the two seams.

## Success Criteria

- `superclaude sweep run [--run <id>] [--window 6h]` writes one dated report under `<root>/.dev/sweeps/`, lists every session and worktree with class, waiting-on and next action, and puts sessions needing the person first. With no `--run` and no `run-current` binding it exits 2 asking for `--run` (GQ-104).
- Tests prove: each recorded `_orca` argv is in the exact allowlist (minus `gate-list`, `worker-read`, stash per GQ-109); every `_git` argv carries `--no-optional-locks`; a snapshot diff shows the report is the only write; one `git status --porcelain --branch` call per worktree (GQ-110).
- Classifier tests cover precedence rules 1-7 plus idle, the window passed into `classify` (GQ-103(2)), the fields of GQ-103(3), the conflict package state (GQ-102), shared committed folders not flagged (GQ-101), archive-blocked from a `FINAL:` line (GQ-105), person-started sessions (GQ-108) and `|` escaping (GQ-107).
- `.dev/sweeps/` is in `.gitignore` (GQ-106).
- WC-14 and the never-as-worker addition are pinned by contract tests; routing registries and docs updated.
- `make verify-sync`, `make lint` and the affected tests pass.
- Later phases (close, resume, trust layer, orchestrator of orchestrators, management relay) are recorded with blockers, not designed (REPORT lines 1328-1332).

## Open Questions

- GQ-01: the populated `worker-list` row schema has never been captured. Design for list plus `worker-show`, or capture it first (step 1.0a)?
- GQ-02: no non-consuming read of pending questions exists, so "waiting on a person" may be missed. Which signal stands in?
- GQ-04: the exact WC-14 wording for "keep polling until every Task is settled" and re-arm after expiry.
- How the #409 layout enters this branch: copy the chosen sections into the design, or cite `495eb96d`.
- 6 h (issue) versus 72 h (`sc-crash-recovery`) default window; the topic fixes 6 h, and older sessions go to a Historical section (GQ-108).
- Sequencing with PR #422 before the WC-14 edit (step 1.16a).
- Stale REPORT citations GQ-111 to GQ-113: the design cites GAPS line 138 (113 rows, 88 open, 25 resolved) and reads REPORT line 1537 as covering GQ-01 to GQ-100 only.

## Enrichment Context

Sources: codebase (reused, quality tier fallback_1: `enrichment/codebase-context.md`); research skipped (the deep research REPORT is itself the input, so a light or deep research pass would repeat it).

- Contract anchors: WC-9 `index.lock` rule at `src/superclaude/core/WORKER-CONTRACT.md:44` (re-checked 2026-11-08); WC-10 absence rule; WC-6 new Task per retry; 41 contract tests in `tests/skills/test_worker_contract.py`.
- Orca read surface: three liveness verdicts, `projection.attention`, `projection.nextAction`, 100-row pages, `--include-remote`, `runtime_unavailable`.
- Reuse from `sc-crash-recovery`: SAFE/REVIEW labels and the "could not determine" section; not its 72 h window or its `git stash` allowance.
- Report layout: #409 header, Attention Ledger, Shift Brief, omission counts, no action controls (`495eb96d`).
- Code placement: Click group in `src/superclaude/cli/sweep/`, deferred registration in `cli/main.py`, command and skill under `src/superclaude/`, installed-path references only.
