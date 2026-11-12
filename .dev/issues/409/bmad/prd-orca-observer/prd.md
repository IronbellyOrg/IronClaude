---
title: Orca Read-Only Terminal Observer
slug: orca-observer
status: final
created: 2026-11-08
updated: 2026-11-08
issue: IronbellyOrg/IronClaude#409
source_spec: _bmad-output/specs/spec-orca-observer/SPEC.md
---

# PRD: Orca Read-Only Terminal Observer (orca-observer)

## 0. Document Purpose

This PRD states what the Orca read-only terminal observer must do for its user, release by release, and how each release is judged done. It is step 2 of the BMAD chain for IronbellyOrg/IronClaude issue 409. The canonical build contract is the spec folder `_bmad-output/specs/spec-orca-observer/` (SPEC.md plus nine companions); every functional requirement here traces to a spec capability id (CAP-n). Technical detail (adapter argv, snapshot fields, geometry, key map) lives in `addendum.md` and the spec companions, not here.

Rules this document keeps:
- Evidence labels from the inputs are kept as written (VERIFIED, UNVERIFIED, PROPOSED, CONTRADICTION). Anything not checked is UNVERIFIED. No Orca API field is invented; the source-to-dashboard schema is PROPOSED, not an Orca contract.
- Orca and coordinator policies keep authority over everything the observer shows.
- Open owner decisions are carried, never decided (section 12).
- Items tagged `[ASSUMPTION]` were inferred during this headless run; they are indexed in section 13.

Readers: the owner (decides gates and open questions), the UX and architecture steps of this chain (steps 3 and 4), and the reviewers of step 5.

**Current status:** DIRECTION-SELECTED is NOT passed and R1 is gated (section 4), so today only offline R0 work is allowed (section 8).

## 1. Vision

One human supervising 5-10 Orca orchestrators and 50-100 sessions/worktrees loses human questions in recency-ordered chat, and "read" gets treated as "handled" (issue 409 Problem Statement; merged requirements: "Root cause of #409: a human question gets lost because chat is ordered by recency and because reading a message is treated as handling it").

The observer is a read-only terminal companion for Stably.ai Orca in the existing IronClaude environment. It separates verified outcomes from activity and says plainly what it cannot see: unknown, stale, unavailable and partial data are disclosed, never implied complete. It is not github.com/orca-cli/orca, not a scheduler and not a session manager (issue 409 Feature Summary). It never acts on Orca.

It ships in gated stages. Release 1 (R1) is a worker ledger on the one verified source (`worker-list`) that states up front that human questions are not yet observed. The question ledger and the decision view come only after data gates prove their sources.

## 2. Target User

### 2.1 Primary user and jobs

**The supervisor**: one human supervising 5-10 orchestrators and 50-100 sessions/worktrees (issue 409, I:11). Sessions do not map one-to-one to worktrees: a worktree can be shared by sessions, and some sessions are unmapped.

| Job (when / I want / so that) | Release that serves it |
|---|---|
| JTBD-1. When I glance at the terminal, I want to know whether the fleet is alive and how complete and fresh my view is, so that I do not mistake a partial or stale picture for the whole fleet. | R1 |
| JTBD-2. When I come back after a while, I want to see what changed since I last looked, so that I find meaningful updates without rereading chat. | R1 |
| JTBD-3. When one worker row matters, I want to inspect its full evidence with full identifiers, so that I judge it on facts, not on activity. | R1 |
| JTBD-4. When I need to share or archive what I saw, I want a plain-text export of exactly the view on screen. | R1 |
| JTBD-5. When agents ask humans questions, I want every observed open question kept until explicit closure evidence, so that reading is never treated as handling. | R2 (gated) |
| JTBD-6. When I decide one question, I want to see who is affected and the evidence, so that I answer with the right scope. | R3 (gated) |

Issue user story (I:15): "As a human supervising orchestrators, I want a read-only view of attention, affected work, changes, and evidence, so that I can find decisions and inspect their supporting facts without confusing activity with outcomes."

### 2.2 Secondary users

- **Reviewer (R0)**: reviews synthetic fixture renders of the three directions at 160/116/80 columns before any live call, as input to the owner's selection (CAP-1, T50).
- **Owner**: records the dated selection record and the other open decisions (section 12). The owner is the only decider for gates; no agent writes a selection record.
- **Snapshot consumer (machine, later)**: a read-only Go screen inside TUIBBS may read the JSON snapshot later, subject to the licence opinion (OQ-9). Not built here.

### 2.3 Non-users

- The agents and workers themselves: the observer never instructs, approves or replies to them.
- Staff teams on a shared bulletin board system (BBS) platform: background only. The TUIBBS review refutes "TUIBBS as a team platform (no teams; group resolver empty)" (summary.md, Refuted). Whether TUIBBS becomes the staff platform is OQ-10.

### 2.4 User journeys

- **UJ-1 Fleet glance (R1).** The supervisor starts the observer. The header shows scope, collected versus reported counts, freshness, and the notice that human questions are not observed. The COUNTS strip shows source state counts unsummed. If data is partial or stale the header says so in words.
- **UJ-2 What changed (R1).** The supervisor presses `m` to mark a look. On the next cycle, rows whose stage, `nextAction.kind` or `liveness.verdict` changed are starred and counted; rows no longer read show `not reobserved`.
- **UJ-3 Inspect (R1).** The supervisor selects a row; selection follows the row's identity across reorders. Enter opens the inspector with every identifier in full or `unknown (absent in source)`.
- **UJ-4 Export (R1, any platform).** The supervisor presses `e` or runs with `--once` and gets a plain-text record of the same view: no escape bytes, full IDs.
- **UJ-5 Find the oldest question (R2/R3, gated).** "find the oldest question and inspect its evidence" (merged requirements, C's walkthrough task).

## 3. Glossary

| Term | Meaning in this PRD |
|---|---|
| Orca | Stably.ai Orca, the agent orchestration tool the observer reads. Not github.com/orca-cli/orca. |
| Orchestrator / Run | An Orca coordinator session and its Run (`runId`). |
| Dispatch / worker row | One worker dispatch reported by `orca orchestration worker-list --json`; identity is source namespace + `dispatchId`. |
| `worker-list` | The one verified live data source for R0/R1 (`orca orchestration worker-list --json --limit 100`). |
| Discovery probe | The one-time `skills list --json` check, via `_find_orca()`, that validates the Orca binary before the first cycle. |
| Signal Bridge (A) | The worker-ledger direction; R1 is its worker ledger. |
| Attention Ledger (B) | The question-ledger direction; R2, after QUESTION-OBSERVATION. In R1 only its "question source UNVERIFIED" notice ships. |
| Decision Desk (C) | The per-question affected-scope view; R3, after QUESTION-LINK. |
| Data gate | A release precondition that passes only on recorded, redacted samples of four kinds (success, missing, stale, contradictory), each pinned in a contract test. |
| DIRECTION-SELECTED | The owner's dated, owner-written selection record. Status: NOT passed. |
| Fixture / R0 | Synthetic recorded data replayed offline; always labelled "synthetic fixture, not live evidence". |
| Snapshot | The versioned, additive-only JSON file written by `export(view)` each R1 cycle (schema PROPOSED). |
| `UNKNOWN` / `unknown` | A value the source did not give. Never shown or exported as 0, false, `-`, blank, empty string or `null`. |
| PARTIAL / STALE / FAILED | Collection states: paging stopped at the per-cycle call cap while `page.hasMore` was still true, or an empty page arrived while reported T was above 0 (`PARTIAL (empty page k)`); no successful read for 45 s on a monotonic clock; a call failed. Stale is not failed (rendering-rules.md, adapter-contract.md). |
| Mismatch | Traversal finished, but collected n is not reported T: `collected n / reported T (mismatch)`. Not PARTIAL; `page.total` may include historical dispatches (K3). |
| UNVERIFIED / PROPOSED / CONTRADICTION | Evidence labels carried from the inputs: UNVERIFIED, not checked; PROPOSED, designed here, not an Orca contract; CONTRADICTION, sources disagree, left open. |
| Write-back | Sending confirmations or corrections from the BBS to agents. A future stage; never R1. |
| TUIBBS | A private Go BBS (AGPL-3.0). Background only: no dependency, no copied code. |
| FR-X-13 | TUIBBS rule "no write-back" (`internal/serve/menu.go:637-640`). |

## 4. Staged Releases and Gates

The owner chose a staged direction (binding): R1 = Signal Bridge's worker ledger on the verified `worker-list` source, carrying Attention Ledger's "question source UNVERIFIED" notice; Attention Ledger after QUESTION-OBSERVATION; Decision Desk behind QUESTION-LINK. The brief's "R1 / B / C" maps to the spec's R1 / R2 / R3. The spec adds an offline R0 before R1 and later stages after R3.

**Data-gate rule** (release-gates.md): "A data gate passes only on recorded, redacted samples of four kinds, success, missing, stale and contradictory, each pinned in a contract test. Without all four the gate stays closed. A failed gate keeps the screen on the previous release's view."

| Stage | What it adds | Gate before it | Gate status |
|---|---|---|---|
| R0 Fixture replay | Ledger screen, inspector, text export at 160/116/80, sanitizer, cell-width truncation, NO_COLOR, ID-anchored selection, every fixture variant, the synthetic `base` variant in place of a recorded sample, which R1 records at the first permitted live read (release-gates.md:9); renders of A, B and C for review. Key-reader spike first. | None from Orca; offline only. Fixtures labelled SYNTHETIC; the PROPOSED schema is used only in fixture mode. | Open to start |
| DIRECTION-SELECTED (gate only) | Nothing ships. | The owner's dated, owner-written selection record (date, option, decider, where the statement lives). Holds the defaults, post-link choice or explicit deferral, fallback date, stack confirmation, command name and confirmed production-integration reading. The owner has already confirmed the stack (owner-decisions-20261108.md item 5, 2026-11-08); whether that confirmation counts toward the selection record is OQ-1. | **NOT passed** |
| R1 Live worker-list | COUNTS strip, freshness strip, worker ledger with verbatim `nextAction.kind`, `result.counts`, capped paging, stale handling, changes since last look, the selected view, the question-source notice, the JSON snapshot export. | DIRECTION-SELECTED passed, production integration permitted under the reading the owner confirms, a redacted golden sample of each of the four kinds, contract test T32. | Closed |
| R2 Attention Ledger (B) | `COORDINATOR QUESTIONS` for one named Run (messages of type `question` only), with observer-side retention, the 100-row disclosure, "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost". One Run only, no rotation. | QUESTION-OBSERVATION: **NOT passed**. Candidate verb, never an available source until the open items are recorded: `orca orchestration check --all --types question --run <runId> --json` for one named Run, never `run-use`, one message call per cycle inside the 5-call cap. Open items (`release-gates.md`): Q-1 (an observer terminal with a handle but no Run, UNVERIFIED), the message rate and identity on the Run the owner names (the owner has not named it), and the owner's written pass record. Seen on probe Runs only: the read returns only the bound Run's mailbox (`consumer_fenced` for another Run), and non-consumption as the Run's owner for the visible effects tested (INV-022, T51). Question identity is `message.id`, a worker `dispatchId` is never a question's identity. Owner decisions 8 and 6 decided 2026-11-11 (coordinator questions only; one named Run, `--types question`, never `run-use`). | Closed |
| R3 Decision Desk (C) | For the selected question, affected sessions with worker-list evidence. | QUESTION-LINK: authoritative mapping from IDs in a message to `dispatchId`/`worktreeId`, verified on this host first; optional owner re-confirm of the post-link default (B or C). No named decider beyond that. | Closed |
| R4 Remote fleet | `--include-remote` rows grouped by `projection.host.id`. | Cross-host ownership joins. Not established. | Closed |
| Later | Closure evidence (`closed by evidence`), history beyond the 100-row window, admission and verification, cost, deep links. | Each needs its own feed; none established. | Closed |
| Future: write-back | Section 11. | Boundary change on issue 409 plus TUIBBS FR-X-13 amendment. Never R1. | Closed |

**Production-integration boundary.** Two readings exist, both UNVERIFIED as the issue's intent: reading 1, the first change that registers `superclaude observe` in the shipped CLI or lets the adapter run a live Orca subprocess outside the fake runner; reading 2, the first change that wires or enables the observer in the shipped product. Until the owner confirms one in the selection record, the stricter reading applies: **offline R0 work only**. Issue 409: "This issue request does not authorize production code changes or deployment" (I:91).

**Fallback rule** (release-gates.md): if QUESTION-OBSERVATION is not verified by the owner's fallback date, the owner re-confirms the direction; expiry never grants permission to switch direction. If A is picked, A stays the default on the same adapter and renderer and B's retention model stays in the code for when the contract arrives. A selection whose data gate has not passed ships only an owner-accepted gated fallback with the reason on screen, or stays blocked. A selection never clears a gate, and a gate is never bypassed to honour a selection.

**Settled by engineering, not by owner vote** (owner-decisions-and-risks.md): fixture replay before the live adapter; 100-row window for the question panel; `--include-remote` off until R4; no persisted "last look" (session memory only); 15 s cycle, at most 5 subprocesses per cycle, STALE after 45 s monotonic, per-call timeout measured at the first permitted live read (R0 makes no Orca calls; UNVERIFIED until then; T5 injects a configured value), message calls per cycle by measurement; POSIX interactive mode plus `--once` text export on every platform.

## 5. Features

FRs are numbered globally. Each traces to a spec capability (CAP-n) and names the acceptance tests (T-n, `acceptance-tests.md`) that pin it. "No spec test" means the spec has no test for that consequence; a test ID is not assigned. CAP-8 (rendering safety and legibility) is carried as NFRs in section 6.

### 5.1 F-R0 Fixture replay (CAP-1, R0)

**FR-1.** A reviewer can replay synthetic fixtures offline and see the Signal Bridge, Attention Ledger and Decision Desk directions at 160, 116 and 80 columns, each with a degraded version beside it, before any live Orca call.
Consequences (testable):
- Every R0 render carries "synthetic fixture, not live evidence" (T50).
- The scale matrix {5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} renders all 27 cases (T16); the 8-orchestrator/80-session `base` is the reference fixture.
- The same input renders byte-identical text twice (T6).
- In fixture mode, B lists every fixture question oldest first with requester/owner and affected IDs (T7). Fixture questions are synthetic and never presented as Orca API fields.
- Fixture fields follow the PROPOSED schema only in fixture mode.

**FR-2.** The development team can record the key-reader spike result before other R0 work, and the stack follows it: Rich stays if the spike passes; Textual replaces Rich only if it fails; never both. The stack is CONFIRMED by the owner (2026-11-08): Python + Rich as a `superclaude observe`-style subcommand with the JSON snapshot export, superseding issue 409's stated Go/Bubble Tea v2 preference (stack.md "recorded owner decision 2"; owner-decisions-20261108.md item 5; numbering differs, see OI-11).
Consequences (testable):
- The spike result is recorded before any other R0 work starts (CAP-1 success). No spec test; reviewer-checked.

### 5.2 F-Ledger Worker ledger (CAP-2, R1)

**FR-3.** A supervisor can see one ledger row per worker dispatch from `worker-list`, with lifecycle fields, outcome, `nextAction.kind`, liveness and evidence age shown raw.
Consequences (testable):
- Every field renders verbatim from the source or as `unknown`; `missing-fields` renders `unknown` for every absent field (T13).
- Contract test T32 parses the redacted golden `worker-list --json` sample and fails on any missing required field.
- The ledger is titled `worker-reported, not questions` (rendering-rules.md; owner-decisions-and-risks.md risk table).

**FR-4.** A supervisor can trust that each ledger row is one distinct dispatch, without one-to-one session/worktree mapping being assumed.
Consequences (testable):
- Row identity is source namespace + `dispatchId`; the same `dispatchId` from different namespaces stays two rows (T39).
- Duplicate and out-of-order rows show `k duplicate rows ignored` (T22).
- Two sessions sharing one `worktreeId` show as two rows; the inspector of each shows the same `resource.worktreeId`, and the inspector of a session with no worktree shows `unknown (absent in source)`; no count divides sessions by worktrees and no `conflict` label appears (T20, acceptance-tests.md:29). The spec ledger has no worktree column; whether the ledger row names the worktree at all is open (UX-OQ-8).
- Uneven per-owner counts sum to the global count (T17).

**FR-5.** A supervisor can hide and show historical (released or retained) rows.
Consequences (testable):
- Historical rows are hidden by default with a visible `k historical hidden (h)`; `h` toggles them (T21).

**FR-6.** A supervisor gets one stable view for the whole session.
Consequences (testable):
- The default view is chosen once at start-up from the runtime state of the question source and never switches mid-session (T45).
- The header shows `read k of N Runs since start` (T45). Where this line belongs is a CONTRADICTION in the source (OQ-13); not resolved here.

### 5.3 F-Notice Question-source notice (CAP-3, R1)

**FR-7.** A supervisor is told above the ledger that human questions are not observed in R1, so an empty screen is never read as "no questions".
Consequences (testable):
- In every live R1 state the notice reads `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` (T9, T47).
- No question count is derived from any message source, including `result.count` (T47).
- The freshness strip carries a second cell `messages UNVERIFIED (not read)` until QUESTION-OBSERVATION passes (rendering-rules.md).
- Empty states never read `no questions` (T33): live, an empty worker read shows `worker-list returned 0 workers in scope=bound`, naming the scope; the fixture `empty` renders `no observed items in this source window; not proof none exist` (rendering-rules.md).

### 5.4 F-Coverage Completeness and freshness (CAP-4, R1)

**FR-8.** A supervisor can tell how much of the fleet was collected versus reported, and in what scope.
Consequences (testable):
- `page.total=287` with 100 rows collected shows `collected 100 / reported 287`, never `287 workers` (T18).
- PARTIAL, STALE, FAILED and `n+? (k unknown)` forms render exactly as pinned (CAP-4 success). A missing `page.total` shows `reported unknown` (T18, T32). A finished traversal where collected n differs from reported T renders `collected n / reported T (mismatch)` (rendering-rules.md:55). No spec test: CAP-4 (SPEC.md:42) names no test for this ledger form; T47 pins only the question-area notes (OI-6). After QUESTION-OBSERVATION the question area also shows `collected n unique / reported T`, `changed during read` and mismatch notes, a per-scope `revisit ~Ns` rotation token; an empty rotation set reads `message source not read: no eligible scope; coverage unknown` (T47; rendering-rules.md).
- A local `/` filter always shows `filter <expr>: k of n collected` beside the unfiltered `source counts: ...`, never summed into workers; the footer reads `shown x/y | collected n / reported T` (rendering-rules.md:56, :21). No spec test (P2).
- At the 5-call cap the screen shows `PARTIAL: collected 500 of reported T` (T4).
- The header shows `scope=<result.scope.source>` or `scope unknown` (rendering-rules.md).

**FR-9.** A supervisor can tell how fresh each fact is, and tell stale from failed.
Consequences (testable):
- The source turns STALE after 45 s without a successful read on a monotonic clock, unaffected by wall-clock jumps; back-off caps at 60 s (T40).
- A timed-out call shows `FAILED (timeout)` and the cycle still ends within the 15 s budget (T5).
- Poll age and evidence age show separately; old evidence alone does not mark the source STALE (T42).
- Each fact is in one of four states: `known`, `unknown`, `unavailable`, `stale` (rendering-rules.md).

**FR-10.** A supervisor sees counts that never overstate what is known.
Consequences (testable):
- An aggregate with k unknown members renders `n+? (k unknown)`, never a clean `n` (T38).
- The COUNTS strip shows numbers and denominators only, no bars, no health name, at 80, 116 and 160 columns; its priority tokens are never truncated (T35). Source state counts are never summed (CAP-4).

### 5.5 F-Facts Separate facts, no inference (CAP-5, R1)

**FR-11.** A supervisor sees lifecycle, outcome, report status, acceptance, current tests and human approval as separate facts.
Consequences (testable):
- Report, acceptance, tests and approval each render `unavailable (no source)` in live mode (T15).
- SETTLED and POLICY FROZEN render `unavailable (no source)` in live mode, never blank or zero (T34).
- A row with `terminalState=released` and no `outcome` never renders `done`, `complete` or `settled` (T14).

**FR-12.** A supervisor is never shown a conclusion the evidence does not support.
Consequences (testable):
- Cost renders `cost unavailable`, never `$0`; no progress is derived from tokens or activity (T31).
- Elapsed time is never shown as completion percentage (issue AC 8). No spec test.
- A partial cost subtotal is never labelled total spend (issue AC 8). No spec test; in R1 cost is unavailable, so this binds whichever later stage adds cost.
- Policy-frozen work stays visible for explicit human handling and is never auto-cleared (issue AC 8). Partly covered by T34 (rendering only); no spec test for the handling.
- A dirty worktree is not shown as dangerous, stale is not shown as failed, shared paths are not shown as a conflict, and inspectable evidence is not shown as admission (issue I:19, AC 4). No spec test.
- `[ASSUMPTION]` These issue-sourced consequences are placed in FR-12 by this PRD; the spec covers them only in part (step-1 coverage gaps G1-G3, G5-G7).

### 5.6 F-Inspector Selection and inspector (CAP-6, R1)

**FR-13.** A supervisor can select a row and inspect its full evidence, with selection anchored to identity, not position.
Consequences (testable):
- The inspector shows every identifier untruncated, or `unknown (absent in source)`; list cells truncate with `>` (T24).
- A reorder between cycles keeps the selection on the same row ID (T25).
- With the selected row visible and others hidden, `+N more` excludes the selected row (T43).
- A selected row that leaves the source window reports `selected <id> no longer in source window`. No spec test pins this (step-1 minor 3).
- `projection.stage.*` renders only in the inspector, sanitized and labelled `worker-reported` (rendering-rules.md).

### 5.7 F-Changes Changes since last look (CAP-7, R1)

**FR-14.** A supervisor can see what changed since they last looked within a session.
Consequences (testable):
- The first observation is the baseline with no change flags; a row that drops out shows `not reobserved` (T41).
- After `m`, a change in one row's `nextAction.kind` stars exactly that row and shows `changed since HH:MM (1)` (T8). Stage and `liveness.verdict` changes also star a row (CAP-7); which `stage` subfield drives this is OQ-15.
- No mark lowers any open count (T10).
- "Last look" lives in session memory only; nothing is persisted across runs.

### 5.8 F-Export Text export (CAP-9, R1)

**FR-15.** A user on any platform can get a readable plain-text record of the view the screen shows.
Consequences (testable):
- `e` (interactive) or `--once` writes the record export: no ESC byte, full IDs, no truncation; an ID the screen truncates with `>` appears in full (T27).
- The screen renderer and the record export read the same view model (T48).

### 5.9 F-Snapshot JSON snapshot (CAP-10, R1)

**FR-16.** A later read-only consumer can read a versioned, additive-only JSON snapshot that `export(view)` writes each R1 cycle, without depending on the Python code.
Consequences (testable):
- A schema test validates every R1 snapshot against `snapshot-export-schema.md`, rejects an unknown `schemaVersion` major, asserts missing values are the string `UNKNOWN`, and finds no message bodies, prompts, file contents or credentials. Test ID not yet assigned (step-1 minor 4).
- `schemaVersion` is `1` for R1. Fields are only added; none is removed, renamed or retyped without a new major version.
- The snapshot carries no write-back path. Terminal handles, worktree and endpoint ids, ownership and release state are deliberately left out of R1. `stage.detail` and `stage.activity` are withheld pending OQ-15.
- The schema is PROPOSED: source key names were checked read-only against live `worker-list --json` on Orca 1.4.245 (2026-11-08), as reported in the source. How a consumer receives the file is UNVERIFIED. Row order is OQ-12. A licence opinion is required before any Go (AGPL) screen reads it (OQ-9).

### 5.10 F-Attention Attention Ledger (CAP-11, R2; gated by QUESTION-OBSERVATION)

**FR-17.** After QUESTION-OBSERVATION passes, a supervisor can see every observed open coordinator question (message type `question`) of the one named Run, retained until explicit closure evidence; seen is not resolved. Questions are listed, not individually selectable, in R2; `m` leaves the question count unchanged (it marks worker rows only).
Consequences (testable):
- `m` on every item leaves the open count unchanged (T10).
- `source-loss` keeps the open count and every retained item (T11); an item missing next cycle stays, marked `no longer in source window` (T12).
- At 1,001 retained questions, eviction does not lower the open total (T46).
- The panel is labelled "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost" and discloses the 100-row source window; the label stays after the gate passes, because a measured rate does not prove completeness (CAP-11; release-gates.md).
- Each item states why it matters (issue 409 AC 2, "explains why they matter", I:78, I:19). `[ASSUMPTION]` (A7) The reason is a sourced field shown verbatim, or `reason unknown` when the source carries none; the observer never writes a reason of its own. No verified message field carries a reason, so R2 shows `reason unknown` (PROPOSED); what identifies a question is decided (OQ-7, 2026-11-11: type `question`); message row keys were seen on probe Runs only and stay UNVERIFIED for other Runs (U1). The spec carries reasons only as a field of attention items (acceptance-tests.md AC-3); no spec test pins it; test ID not assigned.
- The live question read stays refused until the gate passes. T19 and T51 are defined in `acceptance-tests.md`; T51 is the quiet-scope non-consumption test (INV-022), and a pass covers only the visible effects tested, as the Run's owner on a probe Run.
- Nothing in this FR ships in R1. Message rows are not parsed before the gate.

### 5.11 F-Desk Decision Desk (CAP-12, R3; gated by QUESTION-LINK)

**FR-18.** After QUESTION-LINK passes, a supervisor can see, for one selected question, the affected sessions with their worker-list evidence.
Consequences (testable):
- Affected rows come only from an authoritative message-to-`dispatchId`/`worktreeId` mapping verified on this host; otherwise the desk reads "affected scope unknown".
- The desk may show the exact `orca orchestration reply` command as text for the human to run; the observer never sends it (write-back-future-stage.md).
- The selected question shows why it matters (issue 409 AC 2, I:78), under the same rule as FR-17: a sourced reason shown verbatim, or `reason unknown`. `[ASSUMPTION]` (A8) No spec test; test ID not assigned.
- No spec test exists for CAP-12 (step-1 minor 5).

## 6. Cross-Cutting Non-Functional Requirements

These apply to every release. NFR-1 to NFR-6 carry CAP-8; the rest carry the spec's Constraints (SPEC.md).

| ID | Requirement | Verified by |
|---|---|---|
| NFR-1 Widths | The view stays legible at 160, 116 and 80 columns: every screen line has `cell_len <= W`. Under 80 columns every view shows `terminal too narrow (min 80)` above the COUNTS strip, whose denominators still print. When height cannot hold coverage, scope and PARTIAL ahead of optional panels, a too-small diagnostic shows. The threshold is a content rule: the rows those three items need in the R1 view, measured on the rendered output. No numeric minimum height is defined: the spec ties height to C's 44-row contract, whose minimum rows are undefined (OQ-14). Until OQ-14 is answered, T49 tests the content rule only, not a row count. | T23, T35, T49 (content rule only; row count blocked on OQ-14) |
| NFR-2 NO_COLOR | `NO_COLOR=1` and `NO_COLOR=yes` both emit no SGR colour; muted text becomes plain. Meaning never depends on colour alone. | T26 |
| NFR-3 ASCII | Non-UTF-8 terminals use `--ascii`, which replaces box drawing with `+-|`. Text exports are plain readable text. | `[ASSUMPTION]` no dedicated spec test for `--ascii`; T27 covers the export |
| NFR-4 No motion | Nothing blinks (SGR 5/6 never appears); no compulsory motion or animation. | T28 |
| NFR-5 Keyboard | Up/Down or `j`/`k` move, `Enter` opens detail, `Esc` returns, `/` local text filter, `h` historical rows, `m` mark a look, `e` export, `q` quit. No `r` key: refresh runs on the fixed 15 s cycle. No key maps to an Orca call. Selection is anchored to identity. No mouse. | T3, T25 |
| NFR-6 Sanitizing | Every source string is sanitized before it reaches the view model: CSI/OSC sequences (terminated and unterminated), 8-bit C1 controls, bare C0 controls (except newline in the inspector) and Unicode Cf format characters are removed. Strings render as literal text, never Rich markup. Truncation uses display-cell width (`rich.cells.cell_len`), never `len()`, and never splits a double-width character. | T29, T30, T44, manual CJK check (reported as manual, not a test pass) |
| NFR-7 Bounded polling | Fixed 15 s cycle; cycle budget equals the interval; cycles never overlap. At most 5 subprocesses per cycle; each call's output capped at 8 MiB. After failures the interval backs off, up to 60 s. Per-call timeout is measured at the first permitted live read (R0 makes no Orca calls), not guessed; UNVERIFIED until then; T5 injects a configured value. Stderr is sanitized and kept to 2 KiB for the inspector. An overrunning call is killed and reaped; the strip shows `cycle overran (Ns)` (adapter-contract.md). | T4, T5, T40 |
| NFR-8 No LLM loop | Collection is deterministic: no LLM in the loop, no default LLM polling. The same input renders byte-identical text. | T6 |
| NFR-9 Read-only | No write path into Orca. R1 runs exactly one data argv template (`orca orchestration worker-list --json --limit 100`, optional `--run <runId>`, optional `--cursor <c>`) plus the one-time discovery probe (`skills list --json` via `_find_orca()`). Calls use a list, no shell. The forbidden set (plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, any other verb) never shrinks. A value starting with `-`, a malformed `runId` and every forbidden prefix are rejected; the `runId` format check's bounds and regexes are PROPOSED, not verified Orca formats (adapter-contract.md). | T1, T2, T36, T37 |
| NFR-10 No content leakage | Screen, text export and snapshot contain no message bodies, prompts, file contents or credentials. Raw source output never goes into logs, fixtures or exports. | Snapshot schema test (no ID); T29 |
| NFR-11 Honest unknowns | Unknown is never rendered or exported as 0, false, `-`, blank, empty string or `null`. Source loss never closes a question, lowers an open count or turns a value into `failed`. When `_find_orca()` validates no Orca CLI (none found, or every candidate fails the probe), the freshness cell reads `worker-list NOT AVAILABLE (no Orca CLI validated)`, never an empty fleet (adapter-contract.md:10). | T11, T13, T38, snapshot schema test |
| NFR-12 Terminal safety | The key reader restores the terminal in `finally` and on SIGINT/SIGTERM. | `[ASSUMPTION]` no spec test ID; the spike (FR-2) carries its own tests (stack.md) |
| NFR-13 Platform | Interactive mode is POSIX only; `--once` text export works on every platform, including Windows. | T27 covers the export content only (no ESC byte, full IDs, no truncation), on the one headless harness. No spec test runs on Windows: Windows behaviour is UNVERIFIED until T27 also runs on a Windows runner. |
| NFR-14 Independence and authority | No dependency on TUIBBS, no AGPL code copied, and the design prototype (`canvas.py`) is never imported. Orca and coordinator policies keep authority over everything the observer shows. | No spec test; reviewer-checked `[ASSUMPTION]` |

## 7. Non-Goals (Explicit)

From the spec (SPEC.md Non-goals) and issue 409 (I:91):
- Any operational control or write-back in R1, including confirmations or corrections sent to agents: approving, retrying, terminating, spawning, merging, rebasing, deleting worktrees, instructing workers or replying. Write-back is a future stage needing a boundary change (section 11).
- A scheduler, session manager, or fork of another agent manager.
- Remote fleet rows (`--include-remote`) before R4; closure evidence, history beyond the 100-row window, admission, cost, durable replay and deep links before their own feeds exist.
- Parsing message rows (`check --peek/--all`, `inbox --json`) before QUESTION-OBSERVATION; the Decision Desk before QUESTION-LINK.
- Fleet SIGNALS bars, an `r` refresh key, persisted "last look" across runs, mouse, themes, animation, blinking, and Windows interactive keyboard input.
- The TUIBBS Go screen itself.
- Production code changes or deployment under issue 409 (I:91; see the production-integration boundary in section 4).
- Epics, stories, sprint plans and task breakdowns are out of scope for this document.

## 8. Release 1 Scope

R1 is gated (section 4): it needs DIRECTION-SELECTED, a confirmed production-integration reading, the four golden `worker-list` samples and T32. Today only R0 work is allowed.

**In R1:**
- R0 prerequisites delivered first: key-reader spike (FR-2), fixture replay (FR-1), sanitizer and rendering rules (NFR-1 to NFR-6).
- Live `worker-list` adapter under NFR-7 and NFR-9.
- Header, freshness strip, COUNTS strip (FR-8 to FR-10).
- Worker ledger titled `worker-reported, not questions` (FR-3 to FR-6).
- Question-source notice (FR-7).
- Separate facts and no-inference rules (FR-11, FR-12).
- Inspector and identity-anchored selection (FR-13).
- Changes since last look, session memory only (FR-14).
- Text export `e`/`--once` (FR-15).
- Versioned JSON snapshot with its schema test (FR-16).

**Not in R1:**
- Attention Ledger question panel (FR-17, R2) and Decision Desk (FR-18, R3).
- Any message source read; any write-back; `--include-remote`.
- Everything in section 7.

## 9. Success Criteria

### 9.1 Issue 409 acceptance criteria to tests

The issue lists 11 acceptance criteria (I:77-87). The spec maps its tests to AC-1..AC-10 taken from the seed brief, and that mapping is UNVERIFIED against the issue (SPEC.md Assumptions). The table below maps the issue's 11 criteria directly to the spec's tests. `[ASSUMPTION]` This mapping was made by this PRD from the content of each criterion and test; it is not a source mapping.

| # | Issue acceptance criterion (shortened; verbatim in `extract-originals.md`) | Tests / checks | FRs / NFRs | Release where fully met |
|---|---|---|---|---|
| 1 | A human selects the visual direction before production integration. | AC-S reviewer check (owner's dated selection record exists; no agent writes it); T50 renders as input | Section 4 gate | Gate before R1 |
| 2 | Identifies human attention items and why they matter, affected scope, changes since last look, inspection of evidence. | T8, T41 (changes); T24, T25, T43 (inspection); T9, T47 (R1 notice); T7, T10-T12, T46 (questions, R2); CAP-12 has no test (scope, R3) | FR-7, FR-13, FR-14, FR-17, FR-18 | R3 (R1 covers changes and inspection; questions R2; affected scope R3) |
| 3 | Distinguishes verified outcomes from activity; shows freshness and completeness; missing, stale and partial explicit. | T4, T5, T13, T18, T31, T38, T40, T42 | FR-3, FR-8 to FR-10, FR-12 | R1 |
| 4 | Lifecycle, report status, acceptance, tests and approval separate; no inferred conflict, failure or admission. | T14, T15, T34; no spec test for "no inferred conflict/admission" | FR-11, FR-12 | R1 |
| 5 | 160/116/80 columns, stable keyboard selection, NO_COLOR, readable ASCII/text exports, full IDs in detail; no blinking or compulsory motion. | T23, T24, T25, T26, T27, T28, T35; no test for `--ascii` | FR-13, FR-15, NFR-1 to NFR-5 | R1 |
| 6 | 8/80 base and 5/8/10 x 50/80/100 scenarios, uneven ownership, shared/unmapped worktrees, historical, duplicates/out-of-order, stale, missing fields; no one-to-one mapping. | T16, T17, T20, T21, T22, T39, T40, T13; T19 (R2 placeholder) | FR-1, FR-4, FR-5, FR-9 | R1 (R0 in fixtures) |
| 7 | Sanitize untrusted ANSI/OSC/control sequences; display-cell truncation; filtered versus global counts explicit. | T29, T30, T44, manual CJK check; footer `shown x/y \| collected n / reported T` (rendering-rules.md) has no dedicated test | NFR-6, FR-8 | R1 |
| 8 | Tokens not progress; elapsed time not completion %; missing cost not zero; partial subtotal not total; policy-frozen work kept for explicit human handling. | T31, T34; no spec test for elapsed time, partial subtotal or frozen-work handling | FR-12 | R1 (cost items bind the later cost stage) |
| 9 | Deterministic, bounded collection; no default LLM polling loop; no operational controls. | T1-T6, T36, T37, T40 | NFR-7 to NFR-9 | R1 |
| 10 | Confirmed source contracts; unsupported or incomplete coverage identified; no synthetic fixture fields as Orca API fields. | T32, T50, T9, T47, T15 | FR-1, FR-3, FR-7, FR-11 | R1 |
| 11 | Twenty primary design images and the complete package provided with the issue. | None: no test and no reviewer check (step-1 coverage gap G4) | None (delivery item, not product behaviour) | Open (section 12) |

### 9.2 Success metrics

- **SM-1 R0 done.** Every fixture variant renders at 160, 116 and 80 columns with the synthetic label; the 27-render matrix passes; the key-reader spike result is recorded (CAP-1; T6, T16, T50).
- **SM-2 R1 success signal** (SPEC.md): "In R1, replaying the redacted golden `worker-list` samples through the fake runner (and live once the owner clears the integration boundary), a supervisor sees on one screen collected/reported, freshness, scope, the worker ledger and the explicit "questions not observed" notice, the JSON snapshot passes its schema test, and the argv log shows only the allow-listed `worker-list` calls and the one discovery probe."
- **SM-3 Gate evidence.** Each gate passes only on recorded, redacted samples of all four kinds (success, missing, stale, contradictory), each pinned in a contract test (section 4).

### 9.3 Counter-metrics (must stay at zero)

- **SM-C1** Renders in which an empty question area reads as "no questions" (T9, T33, T47).
- **SM-C2** Argv log entries outside the allow-list (T1, T36).
- **SM-C3** Unknown values rendered or exported as 0, false, `-`, blank or `null` (T13, T38, snapshot schema test).
- **SM-C4** Any mark, read or source loss that lowers an open count (T10, T11, T46).

Checks that are not test passes: AC-S is a reviewer check; the CJK check is manual and is reported as manual.

## 10. Risks

### 10.1 Spec risks

From owner-decisions-and-risks.md (verbatim). The source table has no risk ids and no owner column; K1-K12 are extractor row numbers, not source ids. INV ids are the source's own.

| # | Risk | Effect | Mitigation |
|---|---|---|---|
| K1 | Message row contract never verifies | B's panel stays empty; product becomes relabelled A | Decisions 6 and 5; shared adapter and renderer, so a switch costs one layout |
| K2 | Worker ledger read as "questions" | False sense that human attention is covered | Ledger titled `worker-reported, not questions`, gap notice above it (T9) |
| K3 | `page.total` includes historical dispatches | Inflated denominators | `reported T`; `result.counts` shown separately (T18) |
| K4 | Bound scope shows one Run as the fleet | Missed orchestrators | `scope.source` in the header, `one Run only`, `read k of N Runs since start` |
| K5 | Hand-written key reader misbehaves | Terminal left in raw mode | Restore in `finally` and on SIGINT/SIGTERM; `--once` needs no raw mode; R0 spike decides, Textual fallback |
| K6 | Sanitizer gaps | Escape-sequence injection from worker text | Own allow-printable sanitizer, literal rendering, `injection` fixture (T29, T44) |
| K7 | Retention grows in a long session | Memory, clutter | 1,000-record bound; `unknown (retention exceeded)`; eviction never lowers the open total (T46) |
| K8 | Fixture schema mistaken for an Orca API | Coupling to PROPOSED fields | Separate fixture loader; live model built only from verified fields (`unverified-register.md`) |
| K9 | `_find_orca()` lives in `install_user_setup.py` | Observer import pulls installer code | Import as is; moving it is a separate owner-approved refactor |
| K10 | Oldest rows not read at the paging cap (INV-007, accepted) | Long-running active workers missed | Strip disclosure; earlier rows kept as `not reobserved`; state filter UNVERIFIED |
| K11 | Message bodies acquired without permission (INV-017) | Sensitive content in the stdout buffer | Permission checked before the call; call skipped if a narrow read cannot honour it; raw output never logged, fixtured or exported |
| K12 | "Non-consuming" read consumes (INV-022) | Deliveries lost to real recipients | Quiet-scope before/after test in QUESTION-OBSERVATION (T51) |

Recorded dissents (owner-decisions-and-risks.md): `page.total` required (V1) versus optional (merge keeps optional); post-link default (V3 recommends C); A-008 label (QUALIFY applied); message calls per cycle (open, set by measurement, V3 default at most 1); production-integration boundary (both readings UNVERIFIED, stricter applies).

### 10.2 PRD-level risks `[ASSUMPTION]` (raised by this PRD)

| # | Risk | Effect | Mitigation |
|---|---|---|---|
| P1 | DIRECTION-SELECTED and the integration reading stay unrecorded | R1 cannot start; only R0 proceeds | Carried as OQ-1 and OQ-2; R0 work is not blocked |
| P2 | Issue criteria with no spec test (AC 4 inference items, AC 7 filtered counts, AC 8 elapsed/subtotal/frozen, `--ascii`, CAP-12) | Criteria marked met without evidence | Listed "no spec test" in FR-8, FR-12, NFR-3 and section 9.1; test IDs to be assigned downstream |
| P3 | Source contradictions on the post-link default and the origin of recorded owner decision 5 (section 12.2) | Downstream steps act on a disputed record | Both versions carried; not resolved here |
| P4 | Who Orca accepts a `reply` from is UNVERIFIED (write-back-future-stage.md) | A later write-back could be forged | Write-back stays future; relay through the coordinator is required until answered |

## 11. Future Stage: Write-Back (not R1)

> **Separated stage. Nothing in this section is in R0, R1, R2 or R3, and nothing here is approved.** Source: `write-back-future-stage.md`.

**What it is.** Write-back means sending confirmations or corrections from the BBS to agents. The owner wants it later (owner decision 3, binding): it is a FUTURE stage, never R1.

**Boundary change needed in two places before any build.** Issue 409 keeps reply out of scope, and TUIBBS rule FR-X-13 "no write-back" (`internal/serve/menu.go:637-640`) forbids it. Neither moves without an owner decision (OQ-11).

**Python observer stance.** R1, the Attention Ledger and the Decision Desk stay read-only. The Decision Desk may show a pending question and the exact `orca orchestration reply` command for the human to run themselves; the observer never sends anything. The snapshot stays one-way.

**Smallest safe first stage, if approved:** "Answer my own agent's pending question".
- Shows only pending `ask` questions or decision gates from Runs mapped to the logged-in user.
- Allows one of the question's own options, or a fixed Confirm / Decline. No free text, send, spawn, stop, retry, merge or gate-resolve.
- Relayed to the owning coordinator, which issues `reply --id` itself; the coordinator stays the authority.
- Lives inside the later Go TUIBBS screen, where access control, identity and audit exist. Not in the Python observer, not in the snapshot.
- Deferred further: free-text corrections, team-wide answering, any lifecycle control, any Message Base route.

**Gates, all go/no-go before that stage ships:**
0. Boundary: owner records the issue 409 boundary change; TUIBBS owner amends FR-X-13 for this one capability.
1. Identity: operator-maintained UserID-to-Run mapping, read-only to users, every change audited.
2. Authorization: a new per-user capability plus the owner check; default deny.
3. Input: one of the question's options or Confirm / Decline; anything else refused; fixed provenance label.
4. Replay and rate: one accepted answer per question id; nonce as `--retry-request`; per-user rate rule.
5. Audit: `orca.answer.submit` before the send and `orca.answer.result` after (question id, run id, option, nonce, result); hub audit wired into the production broker; HMAC key moved off the audit volume or chain head anchored.
6. Delivery state: pending until confirmed; absent shown as "unknown, do not resend".
7. Credential: narrowest Orca credential; if a pairing code cannot be scoped, the stage waits on Orca.
8. Orca sender: confirm with the Orca owner how `reply` authenticates its sender (UNVERIFIED); relaying through the coordinator is required until answered.

**Threats the stage must control:** wrong person answers; answering someone else's agent; denial after the fact; BBS text steering the agent (prompt injection); flooding; replay and double send; false success shown; spoofed author via Message Base (spoofing itself UNVERIFIED); stolen BBS host; forged audit trail. Controls per threat are in `write-back-future-stage.md`.

## 12. Open Questions

### 12.1 Spec open questions (carried verbatim from SPEC.md; not resolved here)

- **OQ-1.** Does the owner's staged choice satisfy DIRECTION-SELECTED, and where is the dated owner-written selection record?
- **OQ-2.** Which production-integration reading applies (1: registering the command or any live subprocess outside the fake runner; 2: wiring into the shipped product)?
- **OQ-3.** Final command name (recommended `superclaude observe`)?
- **OQ-4.** Fallback date for QUESTION-OBSERVATION?
- **OQ-5.** Sample capture and acquisition permission for live reads (open owner decision 6)?
- **OQ-6.** Message-content exposure (open owner decision 7)?
- **OQ-7.** Decided 2026-11-11 (OWNER, `owner-decisions-20261111.md`): coordinator questions only (message type `question`); the list is not labelled "human".
- **OQ-8.** Multi-observer restriction (open owner decision 9)?
- **OQ-9.** Licence opinion before any Go screen reads the snapshot?
- **OQ-10.** Does TUIBBS become the staff platform?
- **OQ-11.** Is the write-back boundary change (issue 409 plus TUIBBS FR-X-13 amendment) approved?
- **OQ-12.** Which row order is authoritative for snapshot consumers: the snapshot's timestamp order or the ledger's source "newest first" order?
- **OQ-13.** Does `read k of N Runs since start` belong in the B view header only (merged-requirements rendering rule) or in every header (its adapter scope-honesty rule, T45 and the risks table)? CONTRADICTION in the source; see `rendering-rules.md`.
- **OQ-14.** What are the contents of A's width matrix, B's x/width coordinates beyond those copied, and C's 44-row height contract (drop order, minimum rows)? The sources name them but do not define them.
- **OQ-15.** Which `projection.stage.*` subfield drives change detection, and may `stage.detail`/`stage.activity` enter the snapshot (architecture-options.md lists them; merged requirements keep them inspector-only)?

### 12.2 Other open items found while writing this PRD

Parameters and dissents left open by the spec:
- **OI-1.** Per-call timeout: measured at the first permitted live read (R0 makes no Orca calls), UNVERIFIED until then; T5 injects a configured value (adapter-contract.md:28).
- **OI-2.** Message calls per cycle: set by measurement; V3 default at most 1.
- **OI-3.** `page.total`: V1 dissents that it should be required; the merge keeps it optional.
- **OI-4.** Post-link composition: V3 says C; two of three advocates recommend B. The optional owner re-confirm at QUESTION-LINK exists for this choice.
- **OI-5.** `--opt=value` form only after Orca's parser support is recorded.
- **OI-6.** Snapshot schema test ID not yet assigned. No test pins `selected <id> no longer in source window`. No test pins the worker-list mismatch form `collected n / reported T (mismatch)` (FR-8). CAP-12 has no test. (Step-1 minors 3, 4 and 5.)

Coverage gaps (issue text with no spec requirement or test):
- **OI-7.** Issue AC 11, "The twenty primary design images and complete package are provided with the issue": no requirement, test or reviewer check in the spec (gap G4).
- **OI-8.** The reason `--peek` cannot back the question panel ("`--peek` returns only unread messages, so a panel built on it would resolve questions when they are read", merged requirements) is kept as a rule but not stated in the spec (gap G10).

Source contradictions (CONTRADICTION; both versions kept, not resolved):
- **OI-9. Post-link default.** owner-decisions-and-risks.md:57 says "Post-link default (C-001): V3 recommends C. Recorded owner decision 1." The same file at :17 lists the post-link choice as open, and merged requirements (M:463, M:224) say the owner decides, with an optional re-confirm (B or C). The owner's decision file says only "Decision Desk comes behind the QUESTION-LINK gate."
- **OI-10. Recorded owner decision 5.** owner-decisions-and-risks.md:13 records "every fact keeps its evidence label; no invented Orca field; schema PROPOSED; Orca and coordinator policies keep authority" as recorded owner decision 5, but owner-decisions-20261108.md has no matching item (the closest original is issue 409 I:21; the dispatch brief also states it).
- **OI-11. Decision numbering.** The spec calls the stack "owner decision 2"; in owner-decisions-20261108.md the stack is confirmed in item 5 (item 2 called Python + Rich only a recommendation). Meaning is the same; the number is ambiguous.
- **OI-12. Field path.** The TUIBBS review gives `projection.evidence.lastObservedAt`; parts of the spec use the bare `evidence.lastObservedAt`.
- **OI-13. Row order** and **`read k of N` placement** and **`stage.detail`/`.activity` in the snapshot** are already carried as OQ-12, OQ-13 and OQ-15.

Note: step-1 review minor 7 ("Issue 409 does not authorize production code changes or deployment" is phrased more strongly than the sources) is wrong; issue 409 I:91 says exactly that. It is recorded, not acted on.

Owner positions still open (owner-decisions-20261108.md decisions 4 and 5): the licence opinion (OQ-9) and TUIBBS as the staff platform (OQ-10).

### 12.3 Open owner decisions with the spec's recommendations (owner-decisions-and-risks.md; not decided here)

The recommendations are the spec's, recorded for the owner. None is a decision.

1. **Visual direction (DIRECTION-SELECTED).** Dated, owner-written selection record (never an agent): (a) default while no question rows exist, (b) default after QUESTION-OBSERVATION, (c) post-link choice or explicit deferral; reviewed against synthetic R0 renders of A, B, C at 160/116/80, each beside its degraded state, with the task "find the oldest question and inspect its evidence". Recommendation: A plus the COUNTS strip for R1; B after QUESTION-OBSERVATION with A one key away; C behind QUESTION-LINK. V3 dissents (C post-link). NOT passed. (OQ-1)
2. **Stack.** Settled by recorded owner decision 2 (the source listed it as open; it departed from the issue's Go Bubble Tea v2 preference).
3. **Command name and placement.** Recommend `superclaude observe`, registered in `cli/main.py` (deferred import, then `add_command`). The name is the owner's. (OQ-3)
4. **Production-integration boundary.** Reading 1 (V1) or reading 2 (V3), both UNVERIFIED; the stricter applies until confirmed. (OQ-2)
5. **Fallback deadline.** Date by which QUESTION-OBSERVATION must pass; expiry triggers re-confirmation, never a switch. Recommend A on the same adapter as the re-confirm option. (OQ-4)
6. **Sample capture and acquisition permission.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, with the owner setting redaction rules. Unblocks B's headline panel. (OQ-5)
7. **Message-content exposure.** What may be displayed and what exported, kept as separate permissions; no recommendation beyond that. (OQ-6)
8. **Question-type choices.** Decided 2026-11-11: coordinator questions only, messages of type `question`, never inferred from text (OWNER, `owner-decisions-20261111.md`). (OQ-7)
9. **Multi-observer restriction.** Caps are per process, no singleton. Recommend disclosure only. (OQ-8)
10. **Still open from owner-decisions-20261108.md:** write-back stage (summary decision 3), TUIBBS licence opinion (decision 4), TUIBBS as staff platform (decision 5). (OQ-11, OQ-9, OQ-10)

## 13. Assumptions and UNVERIFIED Index

### 13.1 Spec assumptions (SPEC.md)

- The AC-1..AC-10 to test mapping comes from the seed brief via the merged requirements, not a fresh read of the issue's acceptance list.
- Orca timestamps (`liveness.observedAt`, `evidence.lastObservedAt`) are ISO-8601 on one clock; UNVERIFIED.
- Stack-table facts in `stack.md` were researched from primary sources but not run (UNVERIFIED).

### 13.2 Unverified register (unverified-register.md)

The source table has no ids; U1-U19 are extractor row numbers.

| # | Item | How the observer treats it |
|---|---|---|
| U1 | Message row fields and the inbox JSON shape; only an empty peek `result.{count,dispatchId,runId}` has been seen | Not parsed before QUESTION-OBSERVATION |
| U2 | Meaning of `result.count` | No count is ever derived from it |
| U3 | QUESTION-OBSERVATION open items: Q-1, message rate and identity on the named Run, the owner's written pass record (proof (a) as first worded is withdrawn, `release-gates.md`) | Gate stays closed (NOT passed) |
| U4 | Whether the coordinator agent or a person answers a `question` row (Orca has no human recipient field) | Decided 2026-11-11 (OQ-7): the list reads "coordinator questions" |
| U5 | Message IDs, inbox lease fields, terminal-attribution fields | Required before T51 |
| U6 | Value set of `projection.nextAction.kind`, and whether any value means "a human must answer" | Raw string, never classified |
| U7 | Whether `projection.stage.activity` or `.detail` carries question text; value sets of `stage.*` | Inspector only, sanitized, labelled `worker-reported`; withheld from the R1 snapshot |
| U8 | Meaning of `projection.evidence.durable` beyond presence | Shown raw |
| U9 | Whether `page.total` counts historical dispatches; semantics of `result.counts` | Labelled `reported T`, never "workers"; counts never summed |
| U10 | Whether `worker-list` offers a state filter for active workers | INV-007 accepted risk, `not reobserved` |
| U11 | Clock and format of `liveness.observedAt` / `evidence.lastObservedAt` | No per-row STALE; plain age only |
| U12 | Per-call timeout value | Measured at the first permitted live read (R0 makes no Orca calls) |
| U13 | Orca parser support for `--opt=value` | Separate arguments only |
| U14 | Which production-integration reading the issue intends | Stricter reading applies until the owner confirms (OQ-2) |
| U15 | Stack table facts (nothing run) | `stack.md` |
| U16 | AC-1..AC-10 mapping to the issue's acceptance list | `acceptance-tests.md`; this PRD maps the issue's 11 criteria directly (section 9.1) |
| U17 | Snapshot key names checked read-only against Orca 1.4.245 on 2026-11-08; the schema itself is PROPOSED | `snapshot-export-schema.md` |
| U18 | Orca reply sender rule and pairing-code scoping (future stage) | `write-back-future-stage.md` |
| U19 | Whether recorded owner decision 1 counts as the DIRECTION-SELECTED selection record | UNVERIFIED (OQ-1) |

Verified (unverified-register.md): R0 and R1 need exactly one live source, `orca orchestration worker-list --json --limit 100`, plus `_find_orca()` validated through `skills list --json`. Plain `check` consumes deliveries; the observer never calls it.

Not established: complete message history beyond the 100-row window, cross-host ownership joins, admission and revision-pinned evidence feeds, cost/usage accounting, durable event replay, native deep links.

### 13.3 Assumptions made by this PRD (`[ASSUMPTION]`)

- A1. The brief's "R1 / B / C" maps to the spec's R1 / R2 / R3 (section 4).
- A2. Success criteria map the issue's 11 acceptance criteria directly to spec tests, by content (section 9.1).
- A3. Issue-sourced no-inference rules (elapsed time, partial subtotal, policy-frozen handling, dirty worktree, shared paths, admission) are placed as FR-12 consequences with no spec test (section 5.5).
- A4. `--ascii`, terminal restoration and independence from TUIBBS have no spec test ID; they are reviewer-checked or covered by the spike's own tests (NFR-3, NFR-12, NFR-14).
- A5. PRD-level risks P1-P4 are raised by this PRD, not by a source (section 10.2).
- A6. AC 11 (design images) is treated as a delivery item, not product behaviour, and carried open (OI-7).
- A7. Issue AC 2's "why it matters" is an Attention Ledger item field: sourced and verbatim, or `reason unknown` (FR-17).
- A8. The same reason rule applies to the Decision Desk's selected question (FR-18).
