---
topic: "Unified alignment plan, broken down by issue/feature/system, to re-align the roadmaps and start work in lockstep on: Orchestrator mode (#339), the built TUI observer (#409), the issue watcher (#331/#450), the Coder workspace listener (Coder#477), and Orchestrator v2 proactive holistic (#423)"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-11-13T19:20:00Z
---

# Seed Brief: orchestrator-tui-alignment

> Source of truth for every fact below: `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md` (the "adjudicated document", 842 lines, status BLOCKED_BY_INVARIANTS). Evidence behind it: `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/debate-transcript.md` and `invariant-probe.md`. Read those files when a fact here needs its source. Do NOT re-open any finding the adjudicated document lists as withdrawn (its Part 1.3). Ids used below (E-nn, X-nnn, A-nnn, INV-nnn, Q1 to Q24, BC-nn) are defined in its Part 0.3.

## Problem Statement

The owner wants one chain to work end to end: an **issue monitor** (the issue watcher) drives approved issues to an **orchestrator** that manages work across several git worktrees in different stages of development; the orchestrator keeps a **holistic, proactive view** built from the combined knowledge of all that work; and that view **feeds the TUI dashboard** so a human can stay on top of everything, answer questions, make decisions and unblock agents.

Five reviews (of #409, #450, Coder#477, #423, and the built observer) found that the pieces were designed against each other but built independently, and that the chain does not exist as drawn:

- The watcher starts an ordinary `/sc:issue --claim <N>` session. It does not hand work to an orchestrator, and it records only an Orca operation id. Sessions it starts have no Orca Run, so neither the sweep nor the observer can see them (E-10, X-003).
- Orchestrator mode Phase 1 (`superclaude sweep run`, PR #539) is read-only and still open, with two unresolved review threads, one of them a security thread whose suggested fix does not work (INV-008).
- The TUI observer (`superclaude observe`, PRs #503, #514) is already built and merged, but its coordinator-questions read is switched off on master (`QUESTION_GATE_PASSED = False`). Decision Desk (the part where a human decides) is a later, gated release.
- #423 (Orchestrator v2, the knowledge layer) says "v2" in a sense that differs from #339's "version 2"; its gate cannot be applied as written.
- Coder#477 (workspace listener) assumes a watcher-to-listener prompt channel the built watcher does not use, and a listener that accepts prompts would be a remote trigger for sessions that run with permission checks off on this host.
- Issue #409's body is wrong in 23 places (BC-01 to BC-23) and a correction banner is live.

The deliverable is a **unified spec of the alignment plan**, broken down per issue/feature/system, with every dependency identified, so the owner can re-align the roadmaps and start work in lockstep, plus enough detail that an **orchestrator session** can run the work across all relevant worktrees.

## Known Context

(All of it from the adjudicated document; E-nn ids in brackets.)

**What exists.**
- Observer built and merged: release 1 PR #503, release 2 PR #514; registered at `src/superclaude/cli/main.py:572-574`. Reads Orca only; reads no sweep file; neither program mentions the other [E-01, E-03]. Python + Rich stack (owner 2026-11-08). Snapshot v1 JSON (camelCase, `"UNKNOWN"`, 15 row keys, last-writer-wins file in `$XDG_STATE_HOME/superclaude/observe/`). Implements only Signal Bridge's worker ledger and the Attention Ledger's question panel. 15 s poll, up to 5 calls x 100 rows, STALE at 45 s. Already past its row cap on this host (513 rows) [E-14].
- Questions read is dark: `QUESTION_GATE_PASSED = False` (`observe/commands.py:63-67`); the switch-on exists only as two unpushed commits in sibling worktree `issue-409-mvp` (E-02). Owner records it relies on are mostly not on master (E-16).
- Sweep (Orchestrator mode Phase 1): `superclaude sweep run`, `/sc:sweep`, skill `sc-sweep-protocol`, WC-16 (at most once per 5 minutes, a cap), sweep report JSON v1 (stdout only), NFR-001 (one report file per sweep, pinned by two tests), NFR-014 (owner-signed allow-list: 10 Orca templates over 7 verbs; `check` forbidden). PR #539 is open at head `873599d59`; CI red on one test that is also red on master; PR #541 fixes that test and is OPEN and CLEAN (E-08). A CI re-run keeps the old merge ref, so a push or update-branch is needed (INV-037).
- Watcher: `superclaude issue-watch` (#331 closed; PRs #447/#448 merged; rollout #450 open). Launches `/sc:issue --claim <N>` through `orca agent launch` with no `--pipeline`, so the claim runs at the default `worktree` level and starts a governed second agent, contrary to the design's "claim stops at next-steps.md" (E-10, X-001). Launched sessions on this host run with permission checks off (E-11).
- Integration facts: two JSON files both called "v1" (E-05); three vocabularies (E-06); two readers of `worker-list` (E-04); `sweep run` always writes a report (E-07); two Orca builds of one release on record (E-15, A-009 unresolved); whether `check --all --types question` consumes on a live coordinator Run is unproven both ways (X-016, 61%).

**What is settled (adjudicated).** Keep both programs (A-012, 66%, provisional: Q5). One written contract note `docs/designs/observe-sweep-contract.md`, owned by #339, plus one test comparing it with code constants (INV-042); no runtime link in v1; join key `dispatchId` = `row_id` minus `orca:` only after one real-id comparison (JOIN). Do not build an observer reader of the sweep JSON (X-013, X-017). Do not add a watcher panel to the observer, and do not route watcher prompts through a listener, before FU-1 is recorded. Persistence of the sweep JSON is Phase 2 (Q9). "TUI Panel" most likely means `superclaude observe` (70 to 75%).

**What is blocked.** INV-008 (git-config hole in the sweep's `git status`: `core.fsmonitor` and `filter.*.clean` both run in linked worktrees; `-c core.fsmonitor=false` stops only the first; filtering to one repo leaves a shared `.git/config` exposed) is HIGH, UNRESOLVED, owner decision Q1; it blocks the #539 merge and is the first action.

**Merge and implementation order (adjudicated Part 4.2).** 0 owner answers and the INV-008 ruling; 1 PR #541; 2 PR #539 fix push then merge; 3 #409 correction pass (parallel, no code); 4 observer guard-flip PR (needs #541, scope sentence Q6, seeded consumption test, owner records committed, live-layout attempt, build pin, "not passed" grep); 5 routing row (two machine-read tables, INV-029; after #539); 6 contract note and test (after #539 for links; JOIN for the words "join key"); 7 Coder#477 reply (Q3, Q4); 8 #450 edits and FU-1 (Q2); 9 #423 rewrite (after one #339 comment; gate = #539 merged plus #534 live capture). Cross-issue edit order: owner answers, #450, Coder#477, #409, one #339 comment, #423.

**Not-yet-built links of the requested chain (must be stated honestly in the spec, not papered over).**
1. Watcher to orchestrator handoff: does not exist (watcher starts an ordinary session; Run-less; invisible to sweep and observer). Phase 2 sub-orchestrator mode (#444 evaluation open) is the nearest design.
2. Orchestrator across worktrees: Phase 1 sweep is read-only and per-Run; the "manages work" part (dispatch, resume, close) is later phases (`/sc:close`, resume, trust layer, orchestrator of orchestrators).
3. Holistic proactive knowledge layer: #423, advisory only, reads only what named collectors publish; not started; gated.
4. TUI decision loop: observer shows the ledger and (gated) coordinator questions; Decision Desk (the human answers or unblocks) is release 3 behind QUESTION-LINK, not established.

## Constraints

- Read-only discipline: nothing here posts, edits an issue or changes a repository. Issue edits are owner-gated and ordered (A-011: one editor, one ordered edit set, `updatedAt` re-read before each write).
- Project rules: PRs only via `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`, never the SuperClaude upstream; `.claude/` mirrors never staged; `.dev/tasks/` always staged; worktrees only via Orca with `--agent` at Orca's default location; no worker creates worktrees or dispatches workers (WC-13).
- Owner decisions Q1 to Q24 are not the spec's to make: each gets a recommended answer, a default if unanswered, and what it gates.
- Facts stay marked: UNVERIFIED stays UNVERIFIED; PLAN INFERENCE stays marked; no invented file paths, ids or line numbers.
- Single owner, single OS user, single host is the stated scope (A-007).
- No new program, collector, JSON key or sidecar inside PR #539 (A-004).

## Success Criteria

The merged spec must contain, for each of the six systems (Orchestrator mode / #339 and PR #539; observer / #409; watcher / #331 and #450; Coder#477; #423 Orchestrator v2; the cross-cutting contract and trust layer):
1. Scope.
2. Current state (verified, with source).
3. Target state.
4. Work items with stable ids, each with acceptance criteria that can be checked.
5. Dependencies: blocked-by and blocks, by work item id.
6. Owner decisions needed (Q ids) with the recommended answer and the default when unanswered.
7. Risks and reversibility.

Plus:
8. A cross-system dependency graph (all work items, including shared contracts, owner decisions and security or trust boundaries) with no dangling reference.
9. An ordered lockstep schedule of waves: what can run in parallel in which worktree, what must be serial, and the gate that opens each wave.
10. A section "Chain to target": the four unbuilt links above, which work item closes each, and what stays out of scope until later.
11. A closing section listing what an orchestrator session needs to run the work across worktrees (inputs, worktree map, roles, guardrails, stop and escalation rules, polling cadence, decision ledger).
12. Convergence of the three proposals judged by invariant coverage as well as by agreement; INV-008 first.

## Open Questions

Owner questions Q1 to Q24 (adjudicated Part 7). The ones that gate the first waves: Q1 INV-008 fix or accept; Q2 watcher claim level (`--pipeline none`) and written acceptance of permission mode; Q3 Coder#477 narrow, keep or close; Q4 what "TUI Panel" means; Q5 one contract note and keep both programs; Q6 scope of the pass for the questions read and whether to flip before the seeded test; Q7 commit the owner records; Q8 write the selection record (AC-S); Q9 persistence of sweep JSON (Phase 2); Q14 what "#339 complete" means for #423; Q16 one grant vocabulary and audit format; Q24 who runs the shared read-only Orca capture and the join-key comparison.

Unresolved by evidence: A-009 (Orca build divergence), X-016 (consumption on a live Run), D-A (does `agent launch` create a Run or Dispatch), D-B (does the agent row `prompt` hold the claim), D-3 (join key on real ids), D-8 (`projection.attention` values), pass-record authorship, usability of the questions panel in a terminal that holds a Run.

## Socratic Dialogue (non-interactive; answered from the sources, three batches)

**Batch 1: clarify.**
1. *What outcome counts as "aligned"?* A written, ordered plan the owner can start executing without further discovery, where no item depends on something unbuilt without saying so. Not a claim that the chain already works.
2. *Who is the user of the spec?* The owner, and an orchestrator session that dispatches work across worktrees. So it needs ids, gates and stop rules, not prose.
3. *What is in and out of scope?* In: #339/#539, #409/#503/#514, #331/#450, Coder#477, #423, the contract note and trust vocabulary. Out: building the code, editing issues, TUIBBS screen, multi-host.
4. *What does "lockstep" mean here?* Work items advance in dependency waves; items with no shared files run in parallel in separate worktrees; a later wave opens only when its gate (merge, owner answer, live capture) is met.

**Batch 2: validate.**
5. *Is the chain already real?* No: four links are not built (see Known Context). The spec must say which work item closes each and which is deferred.
6. *What is the first blocker?* INV-008 and the owner ruling Q1. Everything that touches #539 waits behind it; work that touches no #539 file (#409 pass, #450 edits, guard-flip prerequisites, Coder#477) does not.
7. *What can run in parallel today?* #541 merge; #409 correction pass (non-owner-dependent rows); owner-record commit; seeded consumption test design; #450 edits after Q2; contract note drafting on a master-based branch. What cannot: routing row, note links, #423 start (all after #539 merges).
8. *Where does a person enter the loop?* Q ids are the human decisions; the observer's questions panel (gated) and Decision Desk (release 3, gated) are where a person answers coordinator questions later; until then the orchestrator session surfaces open decisions in its own decision ledger and stops at owner-gated steps.

**Batch 3: adversarial probe.**
9. *What if the owner never answers Q1?* #539 does not merge; the spec must give the default (the PR stays open, no caveat is added) and say what proceeds without it.
10. *What if the seeded consumption test shows `check --all` consumes?* The guard stays off; the observer's questions panel is not offered; the sweep's caution stands; Q10 stays "observer's alone" or "neither".
11. *What could make the orchestrator session itself unsafe?* A coordinator that dispatches workers that run with permission checks off, reading untrusted issue text (INV-011, INV-012); a worker creating worktrees (WC-13); polling too often (WC-16); posting to the upstream repo (project rule); editing issues out of order (A-011). The prompt must forbid each.
12. *What is the smallest first release of the chain?* Merge #541 and a fixed #539 (sweep, read-only), the contract note and its test, #450 edits with FU-1 (watcher live test at `--pipeline none`), the guard-flip PR with its prerequisites; then #423 start and Decision Desk are separate later waves. The "watcher to orchestrator" handoff and "orchestrator manages work" are explicit later phases with their own gates.

## Enrichment Context

enrichment_used: codebase (primary, Augment search plus adjudicated facts), research (skipped, `--research none`). Full artifact: `enrichment/codebase-context.md`.

- Observer code is on master under `src/superclaude/cli/observe/`; sweep code exists only on PR #539's head; watcher code is on master under `src/superclaude/cli/issue_watch/`.
- Guard, caps and verb limits are constants in `observe/commands.py`, `adapter.py` (`FORBIDDEN_PREFIXES`) and `collector.py` (`MAX_BACKOFF = 60.0`).
- Two task packages for sub-orchestrator mode and the orchestration technical reference are already on disk under `.dev/tasks/to-do/` and `docs/architecture/`; the spec should link to them rather than restate them.
- Host fact: `orca-ide` resolves at `/home/coder/.local/bin/orca-ide`.
