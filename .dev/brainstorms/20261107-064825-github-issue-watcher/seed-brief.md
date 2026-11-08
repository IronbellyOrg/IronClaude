---
topic: "GitHub issue watcher and routing service @.dev/issues/331/issue-summary.md"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 5
handoff_target: none
created: 2026-11-07T06:50:00Z
---

# Seed Brief: github-issue-watcher

Dialogue mode: non-interactive (running as a dispatched worker; best available context used, no person to answer). Owner-level decisions were sent to the coordinator (see Open Questions) and the recommended answer is used as the working assumption.

## Problem Statement

Issues in IronbellyOrg/IronClaude are brought into Orca / Claude Code by hand, one at a time, and then a pipeline is started by hand. Issue 331 asks for an automated watcher that checks GitHub every 5 minutes for issues that are tagged, approved by a human, in a GitHub Project and in Backlog status, and then makes the right person's Coder workspace open a new session that runs `/sc:issue --claim <N>`. What hurts is the manual hand-off and the lack of any automatic routing of an approved issue to the workspace of the person who should own it. The command the watcher would start now exists but stops after a claim (assign, accuracy check, summary, `next-steps.md`), and it cannot run as an Orca worker.

## Known Context

- `/sc:issue --claim <N>` exists (PR #373): assigns the issue to the `gh` user of the machine that runs it, refuses an issue assigned to someone else, reads the repo only from the `origin` remote, asks no question, and edits its earlier marked comments on a re-run. It stops at `next-steps.md` and never runs the next steps. (`src/superclaude/commands/issue.md`, `refs/claim.md`.)
- `/sc:issue` is on the never-as-worker list, so the watcher must reach a top-level session, not an Orca worker (`src/superclaude/core/WORKER-CONTRACT.md`).
- A new ccsession-backed Claude session is started with `orca agent launch` (`--surface terminal`) in an existing worktree (`src/superclaude/skills/ccsession-tag/README.md`).
- `/sc:issue --claim --pipeline <level>` is design only (`docs/designs/sc-issue-launch-level-hook.md`); PR #414 added only the Bash job-identity groundwork.
- Nothing in the repo watches GitHub: workflows run on push, pull_request, workflow_dispatch only. No trigger or approval label exists (nine default labels). No code reads GitHub Projects. `/sc:issue` never creates labels.
- Full enrichment: `enrichment/codebase-context.md`, `enrichment/research-deep.md`. Accuracy check and options analysis: `.dev/issues/331/accuracy-check.md`, `.dev/issues/331/analysis/analyze-sc-issue-protocol.md`.

## Constraints

- This repo holds commands, skills and CLI code. A standing network service, a GitHub Action installed on a real project, or anything that listens on a port or calls a real workspace must not be deployed or run live from this task. Build only what is testable with mocks here; record the rest as follow-up.
- PR and issue target is IronbellyOrg/IronClaude only (`origin`), never SuperClaude-Org. Every `gh` call names the repo.
- Security: untrusted issue text must never reach a session prompt; only a validated integer issue number may. Any inbound endpoint that can make a Claude session run commands is a remote-command surface and needs sender authentication and a command allowlist.
- Claim assigns to the `gh` login of the workspace that runs it and stops if the issue is assigned to someone else, so routing must pick the workspace whose login should own the issue.
- Edit canonical sources under `src/superclaude/` (then `make sync-dev`); UV only; no secrets in any file.
- Poll interval of 5 minutes is requested by the issue; GitHub scheduled workflows have a 5-minute minimum and can be delayed (UNVERIFIED here; check in research).

## Success Criteria

- A reviewed requirements spec that records the owner's decision for option A (workspace-side poller), scores B and C as documented alternatives with the conditions for revisiting, and fixes: the definitions of "tagged", "approved by a human", "in a Project" and "Backlog", the routing rule from issue to workspace/owner, the dispatch record that gives at-most-once starts, and the security model.
- Existing solutions were researched first and the decision cites them.
- A repo-side deliverable list that is testable with mocks (no live deployment) and a follow-up list for everything that is not built here.
- Acceptance criteria are observable (for example: given a mocked `gh` response with N matching issues, the poller starts exactly one mocked launch per eligible issue, with the integer number only, and records each dispatch).

## Open Questions

- Q1 (DECIDED BY THE OWNER, 2026-11-07, relayed by the coordinator; supersedes the earlier hold): **option A, the workspace-side poller**: each workspace polls GitHub every 5 minutes with its own `gh` login and starts the claim via `orca agent launch`; no listener, no inbound port, no address registry. B (GitHub Action plus Coder-side listener) and C (central microservice plus listener) stay documented as alternatives and follow-up, to be revisited only if the decision changes. The issue text and sibling issue IronbellyOrg/Coder#477 were written assuming a push design; the spec must record that A makes #477 unnecessary unless B/C is revisited.
- Q2 (ACCEPTED by coordinator): the watcher stops at a posted claim plus `next-steps.md`; the post-claim pipeline stays manual. Only a validated integer issue number ever reaches a session prompt, never issue text (Q3 of the coordinator question, accepted).
- Sibling dependency: IronbellyOrg/Coder#477 (workspace listener, monitor registration, secure prompt routing; Coder repo, open). It owns the listener, registration, transport and audit; #331 owns the watcher, selection, dispatch record and the contract the listener must meet. Interface, registration mechanism, credentials, topology and audit implementation are "not known yet" there.
- Q3: what concretely is "approved by a human": a label, a Project status change, or a reviewer reaction; who may set it?
- Q4: which label name(s) mark "tagged"; setup instructions only, since `/sc:issue` never creates labels?
- Q5: can the available token read the org-level Project and its Backlog status (GraphQL Projects v2), and with what scope?
- Q6: how is "this issue is meant for this workspace's owner" decided: assignee already set, a label per person, or a Project field?
- Q7: how is double-dispatch prevented across polls and across several workspaces (claim marker comment, label flip, local state file)?

## Enrichment Context

Wave 2A, 2026-11-07. Sources: codebase scan (`enrichment/codebase-context.md`, quality tier primary, corrected once: `src/superclaude/pr_submit/ci.py` is NOT a `gh` wrapper) and deep research (`enrichment/research-deep.md`, quality tier primary, produced by `tech-research`; full report `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md` is authoritative). Late report edits F1, F2, B1, B2 were owner-approved and are unverified by a further review.

**Decided by the owner (not open):** D1 option A (workspace-side poller, pull); D2 claim-only; D3 only a validated integer issue number reaches a session prompt. B and C stay scored alternatives with nine revisit conditions. IronbellyOrg/Coder#477 (listener and registration, Coder repo) is unnecessary under A unless B or C is revisited; under A the Coder-side follow-up is a `coder_script` cron entry and, if `$HOME` is not persisted, a persisted path for the dispatch record.

**Verified facts that constrain the spec:**

- The claim reads, checks, then adds `--add-assignee @me` with no mutual exclusion, and leaves the issue in Backlog; the poller needs its own dispatch record written BEFORE the launch (report plan: states pending, launched, unknown, failed, abandoned, claimed; proposed values lease 60 minutes, `max_attempts` 3, `max_launches` 1, `max_candidates` 10, all [PROPOSAL]).
- `orca agent launch --agent claude --worktree path:<abs> --surface terminal --prompt "/sc:issue --claim <int>" --json` needs an existing worktree, has no `--repo` flag and no permission-mode or allowed-tools flag; a lost reply is retried only with `--retry-launch <operationId>`. Whether a leading `/sc:issue` runs as a slash command is UNVERIFIED (needs one owner-run live test).
- No Python module under `src/superclaude` builds a `gh` call; the poller needs its own injectable subprocess runner (argv list, never a shell). The repo mocks `gh` with a stub executable on PATH (`tests/pr_submit/test_conflict_e2e.py`). Nearest subprocess pattern: `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`.
- The repository is PUBLIC and the claim reads title, body and comments live, so the integer-only prompt protects the launch prompt, not the launched session. Nothing registered constrains a launched session (open decision on permission mode).
- Approval has no label today (9 default labels); only a Triage-or-higher account can label (3 accounts today); the `labeled` event `actor` is the available signal. Reading a Project needs `read:project`, which the observed token lacks; `gh project item-list --query "status:Backlog ..."` acceptance is UNVERIFIED; default page 30, so `-L 100`, fail closed on truncation.
- Polling is cheap (12 polls an hour is about 0.24 percent of the 5,000 an hour allowance per call type). A stopped workspace polls nothing; approved issues wait on GitHub.
- Poll cycle shape in the report: five filters (state open, trigger label, approval label by allow-listed actor, not assigned to another login, intended-owner), claim-marker check, record before launch, pre-launch re-read, caps, one audit line; a `considered` map with least-recently-examined-first ordering so unhandled issues cannot monopolize the candidate cap.

**Still open (spec must settle or record as follow-up):** intended-owner routing candidate and the same-login multi-workspace case; approver allow-list location and rule; trigger and approval label names and the Project/Status mapping; policy for the claim's reads of issue text; at-most-once parameters; where the poller runs and keeps state; per-host Coder facts; the permission mode of the launched session; the live launch test.
