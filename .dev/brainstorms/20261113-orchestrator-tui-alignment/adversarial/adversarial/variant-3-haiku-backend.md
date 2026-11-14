# Unified alignment specification: contracts and operations

Source authority: the adjudicated alignment document, the seed brief, and its codebase enrichment. This is a proposal, not authorization to execute.

## 0. Status, how to read, and honest limits
**BLOCKED_BY_INVARIANTS. First action: the owner rules on the unresolved sweep security finding (INV-008).** Nothing in this specification resolves it, specifies its code fix, or authorizes a risk acceptance. PR #539 must remain open until the owner and author satisfy the ruling. Agreement among proposals does not override an invariant failure. [Adjudicated Part 0.1, Part 2.2 action 1; seed Success Criterion 12.]

### Authority and labels

- `Adjudicated` means `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md` in the supplied ROOT.
- `Seed` means `.dev/brainstorms/20261113-orchestrator-tui-alignment/seed-brief.md`.
- `Enrichment` means that brainstorm folder's `enrichment/codebase-context.md`.
- E, X, A, INV, BC and Q citations refer to the adjudicated document's own identifiers and sections, not new evidence collected here.
- PLAN INFERENCE marks proposed decomposition, operational controls, acceptance checks and future contracts not established as implemented facts.
- UNVERIFIED means no established evidence; absence of evidence never becomes a positive capability claim.
- All work-item identifiers below are proposed planning identifiers, not existing issue or task identifiers.
- This is a written specification only. No code, issue, Run, message, worktree or permission was changed while preparing it.
- The source's live measurements are historical evidence from its review, not fresh runtime measurements by this author.
- Facts reported about the separate Coder repository remain **per V3**, as the adjudicated source marks them.
- Withdrawn findings in Adjudicated Part 1.3 stay withdrawn. The specification does not reopen them.

### Built, dark, pending and absent

| State | Established fact | Source |
|---|---|---|
| Built and merged | Observer releases 1 and 2, PRs #503 and #514; Python + Rich; reads Orca directly | E-01, E-03; Part 2.1 |
| Built but dark | Observer coordinator-question read is guarded off on master; switch-on commits are local and unpushed | E-02 |
| Built and merged | Issue watcher #331; PRs #447/#448; rollout #450 remains open | Seed Known Context; Part 2.4 |
| Pending merge | Sweep Phase 1, PR #539, read-only toward Orca, two unresolved threads; one unresolved security finding | E-08, E-09; INV-008 |
| Pending prerequisite | PR #541 fixes the red test also failing on master; no overlap with #539's files | E-08; INV-036 to INV-038 |
| Absent | Watcher-to-orchestrator handoff; current launch is an ordinary claim session | E-10; Seed four unbuilt links |
| Absent | Phase 1 management actions across worktrees; sweep reports, it does not dispatch, resume or close | Seed four unbuilt links |
| Absent | #423 proactive knowledge catalogue and advisory review layer | Part 2.6 |
| Absent | Observer Decision Desk, release 3; QUESTION-LINK is not established | Part 2.1; Seed four unbuilt links |
| Proposed only | Narrow Coder#477 status/identity channel, with no prompt routing | Part 2.5, Part 6.3 |

### Security ruling boundary

The source measured both `core.fsmonitor` and `filter.*.clean` executing through shared Git configuration in linked worktrees. Disabling only the former and restricting status reads to one repository does not establish safety. [INV-008; Part 2.2 action 1.]

The owner's options remain exactly these requirements, not a chosen implementation.

1. Neutralize both executable-config paths, with the relevant allow-list and regression-test changes.
2. Refuse affected worktrees and represent them with an existing `unscanned` source row, without a new JSON key.
3. Accept the risk explicitly, identify the security premise, and caveat the four read-only statements in the same PR.

Recommended: option 1 or 2. Default without a ruling: no merge and no acceptance caveat added on the owner's behalf. A fix design belongs to the owner and PR author. [Q1; INV-009, INV-010, INV-039.]

### Reading the plan

Section 1 separates immediate alignment from later delivery of the four missing links. Section 2 is the work register; Section 3 owns decision defaults; Sections 4 and 5 are the dependency and execution views of that same register. Section 6 is the operator contract. Section 7 tests whether each claimed outcome actually follows.

All planned worktree labels are **logical roles**, not claims that those worktrees or branches exist. Only the current sweep branch and the sibling observer worktree are named by the evidence. Later workers receive real paths only after coordinator verification. [PLAN INFERENCE; E-02; INV-031.]

This specification has one-host, one-owner, one-OS-user scope. A status reader, advisory summarizer or signed grant does not gain authority to execute instructions contained in issue text, worker text, records or reports. [A-007; X-005; Part 2.6.]

## 1. Chain to target
The target is a chain, not a renamed dashboard. The first release aligns existing surfaces and evidence; it does not claim all four missing links have been built. [Seed Problem Statement and four unbuilt links.]

| Missing link | Work that defines its contract | Work that can close it later | Delivery gate and honest limit |
|---|---|---|---|
| Approved issue to a governed orchestrator | SW-06 defines handoff ownership using WA-04's real launch evidence | WA-05 implements the approved handoff | Q2, Q20, Q21, WA-04, SW-06, XC-05; separate later phase; #444 evaluation remains relevant; no handoff exists now |
| Orchestrator manages work across stages and worktrees | SW-07 defines and validates the management phase against the existing phase material | SW-07's separately planned delivery | SW-03 plus owner-approved management/trust design; Phase 1 remains report-only; no dispatch/resume/close added to #539 |
| Combined work becomes a proactive holistic view | V2-02 investigates; V2-03 names fields, sources, store and inference boundary | V2-04 delivers the separately approved advisory layer | Q14-Q16, SW-03, SW-05; no implementation until brainstorm and research finish; no new v2 scanner |
| Human answers and unblocks from the TUI | OB-02/OB-03 establish the question-read prerequisite; OB-06 designs and delivers Decision Desk | OB-06's separately planned release 3 delivery | QUESTION-LINK, selection record, usable layout, permission and interaction contract; question visibility is not answering |

SW-06, SW-07, WA-05, CO-02, CO-03, V2-02 to V2-04 and OB-06 are later-phase work. They must receive checked implementation plans before code execution; this document does not substitute for those designs or approve their new APIs. [PLAN INFERENCE; Seed Constraints and Success Criteria; Adjudicated Parts 2.4-2.6.]

### Smallest aligned first release

- SW-02 then SW-03 make the sweep mergeable only after SW-01's security ruling is met.
- XC-03 and XC-04 establish one written, checked contract without a runtime connection.
- WA-01 to WA-04 correct the launch expectation and produce a permission-accepted, recorded live test before any cron enable.
- OB-01 to OB-03 establish the prerequisites for a question-read switch-on; absence or failure leaves the switch off.
- OB-04, CO-01, XC-06 and V2-01 make the issue roadmaps accurate through the serialized issue-edit process.
- OB-05 makes the existing observer discoverable after the shared-file merge gate.
- SW-04, SW-05 and XC-07 retain follow-ups with named owners or explicit `unowned` status.
- XC-08 checks invariant coverage independently of whether the variants agree.

This release's acceptance statement is **aligned contracts, accurate roadmaps, and gated reads**, not **autonomous end-to-end orchestration**. [PLAN INFERENCE from Seed dialogue answer 12.]

### Deferred boundaries

No persisted sweep JSON sidecar, observer sweep reader, shared collector, new JSON key, new collector, listener for the watcher, TUIBBS screen, cross-host fleet, or multi-user permission model enters PR #539. Persistence is Phase 2 under Q9; any future observer sweep-facts panel is Q17, not a consequence of adopting the note. [A-004; X-013; X-017; Parts 2.3, 8.]

An ordinary watcher session is operationally outside the current orchestrated worker ledgers. The source describes the blind spot while explicitly leaving the exact existence of Run/Dispatch records from `agent launch` UNVERIFIED; WA-04 must settle that with before/after evidence before WA-05 assumes an identity. [E-10; A-008; D-A; Part 5.3.]

### Contract completion rule

For each later link, the implementation plan must name the producer, consumer, unit of identity, version, authority boundary, retry behavior, interruption behavior, evidence of successful receipt and rollback. A successful process launch alone cannot prove a governed handoff or an observer-visible Dispatch. [PLAN INFERENCE; D-A, D-B; INV-012.]

No item may be accepted merely because an upstream item completed. For example, a fixed sweep does not produce catalogue fields it never collected, a non-consuming read does not make a terminal usable, and a displayed question does not create an answer channel. [INV-041; Part 6.4 acceptance criteria.]

## 2. Per-system sections
All work items and their acceptance criteria are PLAN INFERENCE decompositions of the cited adjudicated actions. `Blocked-by` lists hard predecessors; Q references are owner gates, not implied answers. `Blocks` lists direct successors, not every transitive consumer. `None` means no direct successor. Reversibility never means an external notification can be unsent.

Worktree roles: **S** existing sweep author checkout; **O** fresh master-based observer branch; **W** separate watcher change branch; **C** coordinator's serialized issue-edit lane; **K** master-based contract branch; **F** follow-up branch after #539; **L** separately approved later-phase worktree; **R** independent read-only review context. Exact future paths/branches are UNASSIGNED, not executable placeholders. [PLAN INFERENCE; E-02; INV-031; Part 4.2.]

### Orchestrator mode and sweep (SW)
**Scope.** Finish the contested Phase 1 merge safely, retain the report-only boundary, and identify separate later management/handoff work. No alignment expansion inside #539. [A-004; Part 2.2.]

**Current state.** E-08 records #539 open at `873599d59`, two unresolved threads, and a failing test also red on master. PR #541 changes only that test's file. Sweep uses an owner-signed allow-list, 10 exact Orca templates over 7 verbs; `check` is forbidden. Rows are per bound Run, but worktree and transcript collection are host-global. A run always writes one dated report, then emits sweep report JSON v1 on stdout. [E-07 to E-09; X-010; NFR-001; NFR-014.]

**Target state.** A security-ruled, reviewed Phase 1 with no extra keys/files, fresh merge-ref CI and truthful read-only wording. A later management design, not Phase 1, owns dispatch/resume/close. [Part 2.2; Seed link 2.]

| Id | Title | Checkable acceptance criteria | Blocked-by | Blocks | Worktree/branch | Owner decisions | Reversibility |
|---|---|---|---|---|---|---|---|
| SW-01 | Rule on executable Git configuration | Owner records option 1, 2 or 3 from Section 0; author names allow-list and golden-test impacts; unsafe one-flag remedy is not accepted as proof; status stays unresolved until evidence satisfies ruling | XC-01; security boundary B-GIT | SW-03 | S, current sweep branch | Q1 | Fix can revert; acceptance only reversible before merge |
| SW-02 | Merge CI prerequisite #541 | Fresh read confirms correct fork, still open, expected one-file scope and passing checks; authorized merge recorded; no claim that a rebase is required | Merge authority | SW-03, OB-03 | C, existing PR | None | Revert PR |
| SW-03 | Resolve threads and merge #539 | Both threads resolved with checked evidence; SW-01 ruling met; #541 merged; push/update creates fresh merge ref; CI runs on it; no new schema key/sidecar/alignment file; expected fork URL and merged SHA recorded | SW-01, SW-02 | SW-04, SW-05, SW-06, SW-07, OB-05, XC-03, XC-07, V2-02 | S, `ironbelly/issue-339-orchestrator-mode` | Q1 | Revert PR; notifications persist |
| SW-04 | Deliver bounded Phase 1 follow-ups | #534 table allocates wording corrections, first-50-in-list-order wording, version-limit disclosure, worker-written-field regression test; exact changed sources/tests reviewed; no new collector or JSON key silently added | SW-03, XC-07 | XC-08 | F, fresh post-merge branch | Q9-Q11 | Revert own PR |
| SW-05 | Shared capture and identity comparison | Q24 owner identified; one sitting records full Orca build, allowed help/read outputs, attention values for live/blocked worker, Run-less agent-row evidence or explicit missing observation, and real observer/sweep id comparison; #534 evidence establishes the working class before knowledge-layer gate opens | SW-03, XC-01; boundary B-READ | XC-03, V2-02, OB-06 | O/live-capture context; no code branch needed for reads | Q24 | Evidence retained; reads do not undo prior state |
| SW-06 | Define later watcher handoff contract | Separate checked design names owning coordinator, Run/Dispatch association, launch receipt, deduplication/recovery, allowed launch authority and visibility check; uses WA-04 evidence; #444 evaluation linked; explicitly not implemented by #539 | SW-03, WA-04, XC-05 | WA-05 | L, later phase; UNASSIGNED | Q2, Q20, Q21 | Withdraw design before delivery |
| SW-07 | Plan and deliver management phase separately | Existing phase research/task material read first; approved plan covers dispatch/resume/close, trust and authority as required; tests distinguish a report from a mutation; lifecycle evidence demonstrates work moves between stages; no claim of delivery until this exists | SW-03, XC-05; boundary B-WRITE | XC-08 | L, later phase; UNASSIGNED | New phase authority required, not supplied by Q1 | Stop new actions; revert code, manually reconcile active work |

**Sweep interface contract.** Producer: sweep CLI. Consumer today: coordinator/person; no observer consumer. Format: sweep report JSON v1, snake_case, `schema_version`, `null`, `row_id` structurally prefixed `orca:`; one dated report is the sole per-run file addition. Consumers never invoke another sweep merely to fetch status. Optional caller capture is a Phase 2 choice, not a producer sidecar. [E-05; E-07; Q9.]

**Failure and retry.** A refused or unreadable source is incomplete evidence, not a clean worktree. Repeating a sweep produces another dated report, so a sweep is not a file-idempotent status query. On interruption the coordinator records whether the report exists before considering a retry, and respects WC-16's at-most-once-per-5-minute cap. Existing partial-file behavior on interruption is UNVERIFIED; future runbook acceptance must inspect it rather than assert atomicity. [PLAN INFERENCE; E-07; WC-16.]

**Operational check.** Before an authorized merge, re-read open state, head, changed files, thread states, CI merge ref and fork. Do not call an old CI re-run a refresh. After merge verify the merged revision and that the expected CLI/allow-list tests describe it. PRs are submitted only through `/sc:pr-submit --monitor 3` to IronbellyOrg/IronClaude. [INV-037; Project rules in Seed.]

**Risks.** Shared Git configuration crosses linked-worktree boundaries; changing the shared path set also changes contract/transcript visibility. Only the author/owner designs the fix; SW-01 requires regression evidence of the measured experiment. Full build divergence remains unresolved even if the release prefix matches. [INV-008, INV-039; A-009.]

**Later management recovery.** SW-07 must make each external mutation resumable using the existing authoritative Orca identity, not a repeated natural-language launch. Exact Orca mutation reply shapes and lifecycle retry guarantees are UNVERIFIED here and must be established in its design. A worker may never create or dispatch another worker. [PLAN INFERENCE; WC-13.]

### Observer and issue #409 (OB)
**Scope.** Correct the observer roadmap, preserve the shipped ledger, satisfy every question-read prerequisite, add discoverability, and keep Decision Desk a separate release. [Part 2.1.]

**Current state.** Observer is on master and reads Orca, not sweep files. Guard is false. Poll is 15 seconds; five worker-list calls of 100 rows, up to six calls including questions; feed stale at 45 seconds and backoff up to 60 seconds. The source's host had 513 rows against a 500-row cap, so PARTIAL was steady state. Snapshot has 15 required row keys; command, objective, branch, changed paths, issue and PR are not supplied. [E-01 to E-06; E-14; Enrichment Observer.]

**Target state.** An honest partial ledger with a usable, owner-authorized, build-pinned question read only after diagnostic evidence, plus an accurate issue and routing entry. Decision Desk remains gated on QUESTION-LINK, not inferred from the read switch. [Part 2.1 actions 1-5.]

| Id | Title | Checkable acceptance criteria | Blocked-by | Blocks | Worktree/branch | Owner decisions | Reversibility |
|---|---|---|---|---|---|---|---|
| OB-01 | Preserve owner-authored evidence | Owner supplies pass authorship and dated selection record or explicit AC change; sibling-only decisions, guide and TUIBBS review evidence committed/archived before cleanup; exact record provenance retained; no agent writes an owner answer | XC-01 | OB-03, OB-04, OB-06 | O preparation; sibling `issue-409-mvp` retained as source only | Q7, Q8 | Amend/archive; never fabricate provenance |
| OB-02 | Run diagnostic question-read gate | Plain terminal holds no Run; record run-current before/after; create probe Run without run-use; seed question, worker_done and heartbeat; execute exact observer read twice then consuming check; compare all seeded messages; cite help, full build and limits; record one real coordinator-layout attempt separately | XC-01; B-READ | OB-03, OB-06 | O/live gate context, owner or 409 session | Q6, Q24 | Probe writes retained as test evidence; never bind live Run |
| OB-03 | Ship guarded question read | #541 merged; Q6 scope sentence matches actual guard/code behavior; OB-02 diagnostic result and live-layout attempt recorded; full build pin/check; owner-written pass committed; reclaimable mapping included; every not-passed hit in issue evidence reconciled; fresh master-based PR; otherwise guard remains off | SW-02, OB-01, OB-02; B-QUESTION | OB-06, XC-08 | O, fresh branch; not deleted `409-Phase2` | Q6, Q7, Q23 | Flip off; revert PR |
| OB-04 | Correct #409 body once | Serialized editor re-pins BC-01 to BC-23, applies disposition overrides for BC-12/15/16/17, V1/V2 additions and chosen Q16 text; questions not human-attention shorthand; no provisional id join claimed proven; banner last; owner-dependent wording waits | OB-01, CO-01, XC-02 | XC-06, XC-08 | C, ordered issue-edit lane | Q8, Q16, Q21 | Restore before-body, notifications remain |
| OB-05 | Route people to existing observer | After #539, choose valid routing-table block; both machine-read table contracts and resolvable slash-token checks pass; guide mirror byte-identical; sc-recommend expectation updated; person/coordinator only sentence present | SW-03, XC-01 | XC-08 | F, own small post-merge branch | Q12 | Revert own PR |
| OB-06 | Plan and deliver Decision Desk later | Contract note and capture precede priority choice; Q19 names first release scope; QUESTION-LINK evidence, owner selection, permitted answer mechanism, non-consumption/read limits and live layout all checked; test answer/correction/ack lifecycle with no unauthorized mutation | OB-01, OB-02, OB-03, SW-05, XC-04, XC-05 | XC-08 | L, release 3 plan; UNASSIGNED | Q6, Q8, Q19 | Disable write-back; reconcile already-sent answers |

**Snapshot interface contract.** Producer: observer live process; consumers: local reader today and proposed later status readers. Name: observe snapshot v1; camelCase `schemaVersion`, `UNKNOWN`, `dispatchId`; producer schema rejects extra properties. Files live in the user state directory, mode 0600; absolute-only XDG override rule differs from the sweep. Last writer wins, no pid/liveness flag, file survives process exit. [E-05; Part 2.3; Enrichment Observer.]

**Consumer behavior.** Distinguish feed age, stored-file age, PARTIAL coverage and per-row evidence age. Use `generatedAt`, print age, apply Q22 fallback, ignore unknown future keys and re-sanitize strings. An old snapshot is not a current process heartbeat. Multiple producers can replace one another's snapshot; producer arbitration is not specified and must not be invented as implemented. [INV-004, INV-006, INV-017, INV-035; PLAN INFERENCE on UI separation.]

**Question interface contract.** Producer: Orca mailbox; observer is a guarded reader for one named Run. Format: existing Orca question records; up to 100 after filtering, no read marker; only holder-terminal access established by gate material. Exact live coordinator consumption and replay/ack interactions remain UNRESOLVED. The sweep still forbids `check`. [X-016; E-18; INV-041.]

**Idempotency and operation.** An operator may repeat `observe --once` for text without file writes unless snapshot is requested. Repeated live cycles overwrite snapshot rather than append history. Do not assume repeated question reads are harmless until OB-02 proves the diagnostic case; even then require build and real-layout evidence. On failed gate, leave guard off and retain evidence, not a forged pass. [E-17; Part 2.1 action 4.]

**Risks and undo.** Global boolean scope can exceed a one-Run pass. A seeded pass lacks real listeners and does not prove usability. Reclaimable is not implicitly historical, settled or live. Reversion of code cannot unsend Decision Desk answers, so future write-back must use a separate authority gate. [INV-003, INV-023, INV-024, INV-041; PLAN INFERENCE for future write-back rollback.]

### Issue watcher and rollout #450 (WA)
**Scope.** Align the actual launch chain with the owner-selected claim level, make first rollout diagnostic and explicitly write-authorized, and defer orchestrator integration. [Part 2.4.]

**Current state.** Watcher launches fixed `/sc:issue --claim <N>` through `agent launch`, with no pipeline flag. Default claim level creates/reuses a worktree and a second governed agent despite a claim-only design. Store retains an operation id, not a verified coordinator identity. Real operation-id reply shape is assumed in fixtures. On this host the first session runs permission-free; two environment knobs can affect that. [E-10, E-11; INV-011; D-A/D-B; Part 2.4.]

**Target state.** Q2 explicitly chooses claim-only or the full chain. FU-1 records launch truth, effects and authority before cron enable. Machine-started classification and handoff are later evidence-driven work, never a label inferred from an unverified prompt field. [X-001, X-003; Part 2.4 actions 1-5.]

| Id | Title | Checkable acceptance criteria | Blocked-by | Blocks | Worktree/branch | Owner decisions | Reversibility |
|---|---|---|---|---|---|---|---|
| WA-01 | Align fixed claim prompt and pins | Q2 recorded; if claim-only, prompt, builder, 12-element argv pin, retry argv, property test and runbook strings agree; if default retained, deliberate second-agent chain and OB-H1 item 1, OB-H2, OB-H3 gates recorded; no configurable free-text route | XC-01; B-LAUNCH | WA-02, WA-04 | W, small separate PR | Q2 | Revert PR; existing sessions remain |
| WA-02 | Correct #450 rollout issue | Fresh body/version pin; claim choice and permission acceptance included; FU-1 checklist includes all Part 2.4 evidence; item 4 marked done in #485 with corrected counts; no watcher panel/listener before FU-1; post before later issue edits | WA-01, WA-03, XC-02 | WA-04, CO-01 | C, first issue in ordered pass | Q2, Q20 | Restore before-body |
| WA-03 | Make ownership and unknown-reset safe | Named person owns watcher worktree agent; person/coordinator creates any required worktree through Orca with agent; unknown reset requires live-session check first; interruption runbook never automatically forfeits at-most-once protection | XC-01 | WA-02, WA-04 | W for runbook; C for ownership record | Q20 | Revert text; no silent reset |
| WA-04 | Execute recorded FU-1 | Test issue and first-session permission mode accepted in writing; env knobs and real argv captured; before/after Run/worker lists, agent row, prompt/pane relation, reply operation-id path, tab map/session-name behavior and full build captured; private raw evidence, sanitized fixture; writes enumerated; close/unlabel avoids re-claim; cron remains off until pass | WA-01, WA-02, WA-03; B-LAUNCH | SW-06, WA-05, XC-07 | W live test, named operator | Q2, Q20, Q24 | Manual cleanup except ClickUp effects UNVERIFIED |
| WA-05 | Deliver later governed handoff | Approved SW-06 design and checked implementation plan; duplicate launch/interruption tests; one issue maps to correct ownership/Run/Dispatch or a refused state; retry never starts a second chain from unknown; sweep and observer visibility demonstrated before claiming end-to-end handoff | SW-06, WA-04, XC-05; B-WRITE | XC-08 | L, later phase; UNASSIGNED | Q2, Q20, Q21 | Disable handoff, reconcile existing launches |

**Launch interface contract.** Producer: watcher, one workspace; consumer: local Orca agent launch; payload: fixed typed integer issue claim, not arbitrary remote prompt. Reply parsing currently uses assumed operation-id paths; WA-04 replaces assumption with captured reality. The session's subsequent issue assignment/comments are writes even with claim-only pipeline. [Part 2.4; Part 6.2; E-10/E-11.]

**Store interfaces.** Watcher `status --json` has no schema_version; `dispatch.json` v1 is a distinct named contract. They are registered in the cross-contract note but not governed as observer/sweep schemas. The existing at-most-once guarantee must survive retry handling; `unknown` is uncertainty about a launch, not permission to launch again. Exact store transition/locking implementation is UNVERIFIED by this variant and must be read in WA-01/WA-04 execution. [Part 2.3 registry; INV-007; Part 2.4 action 3.]

**Interruption runbook.** Before a reset with forfeiture, inspect Orca for a live session in the configured worktree, compare stored operation evidence and preserve unknown if identity cannot be settled. A failed reply parse must not become a blind launch retry. Record the decision and operator. [INV-007; PLAN INFERENCE for reconciliation record.]

**Live-test effect inventory.** Assignment, two marked comments, optional ClickUp script when enabled by environment, and local issue files are expected writes. Label/claim order can cause an enabled watcher to claim again. First rollout therefore remains a bounded test with owner consent, not a read-only probe. [Part 2.4 action 2(i); INV-012.]

**Operational acceptance.** Verify real argv rather than assuming `CCSESSION_PERMISSIONS` overrides `CC_CLAUDE_FLAGS`. Confirm there is no Session Name stall and that the tab-map entry refers to the launched session. Only after recorded FU-1 may a separately authorized operator consider FU-2 cron enable; FU-2 is not silently included in WA-04. [INV-011; Part 2.4; Part 6.2.]

**Risks.** Untrusted issue text reaches a permission-free session on the measured host. Claim-only removes a second agent, not this first exposure. Run-less/invisible sessions, assumed reply shapes and forfeited state can together create duplicated, unowned work. No listener or observer watcher panel is introduced to hide that gap. [INV-012; A-008; D-A/D-B.]

### Coder workspace listener #477 (CO)
**Scope.** Resolve the stale listener premise. Recommend narrow read-only identity/status, or close if remote reading is not near. Do not route watcher prompts, choose a transport by implication, or implement a Coder service in this alignment pass. [Part 2.5; Part 6.3.]

**Current state.** Built watcher deliberately has no listener, inbound port or registry. Coder#477 assumes one. Per V3, Coder control-plane workspace identity/running state is authoritative, the existing heartbeat collector is anonymous, and a workspace listener cannot start a stopped workspace. The owner-token route to an owner-shared app is UNVERIFIED. [E-12; Part 2.5; Part 5.3.]

**Target state.** One owner-selected issue disposition that is safe under either `superclaude observe` or a later TUIBBS reader. If narrowed, no send route; remote status design waits for a real remote-reader need, authenticated route verification, identity envelope and age rule. [Q3/Q4/Q18/Q22; Part 2.7.]

| Id | Title | Checkable acceptance criteria | Blocked-by | Blocks | Worktree/branch | Owner decisions | Reversibility |
|---|---|---|---|---|---|---|---|
| CO-01 | Post owner-selected #477 disposition | Q3 and Q4 explicit; one editor uses narrow/keep/close source text with dependencies resolved; Q2 claim statement correct; no unverified auth route claimed working; Q22 unresolved threshold marked as a gate, not pasted as a placeholder; closing retains both reopen conditions | WA-02, XC-02, XC-01 | OB-04, CO-02 | C, second issue in ordered pass | Q2-Q4, Q16, Q18, Q22 | Edit/reopen, notifications persist |
| CO-02 | Design remote read-only status only when needed | Remote-reader task/R4 or explicit owner need recorded; Coder-derived id/owner/name/running state; fixed versioned allowed-field record, age, protected owner-read route, audit, rejection tests and all nine source checklist cases; no address/credential registry, prompt or session-start route; route verified rather than assumed | CO-01, XC-04, XC-05; B-IDENTITY | CO-03 | L in Coder repo, path/branch UNASSIGNED | Q3, Q4, Q18, Q22 | Withdraw design; route remains absent |
| CO-03 | Deliver gated status channel later | Checked separate implementation plan; non-read requests rejected; other-owner/unauthenticated requests rejected/logged; workspace-id spoof rejected; stopped/deleted/name-reused states correct; stale never current; no sweep invocation or Orca consumption; schema/version/audit and least-authority tests observed | CO-02; B-IDENTITY | XC-08 | L in Coder repo, UNASSIGNED | Q3, Q18, Q22 | Disable route/revoke read credential; preserve audit |

If Q3 selects close, CO-02 and CO-03 are explicitly **deferred/not selected**, not complete. If keep is selected, the status-only design is not executed: the issue first needs the grant format, sender/expiry/workspace checks, nonce/replay rejection, separate read/send credentials and written permission-mode acceptance in source text B. That alternative is a new approved scope, not an automatic branch of this specification. [Part 6.3 texts B/C; PLAN INFERENCE for status marking.]

**Read interface contract.** Proposed writer: workspace status publisher; identity authority: Coder control plane; reader: owner-authorized external status client. Fixed permitted fields come from the narrowed text: profile slugs, Orca/Claude Code versions, image hash, last-written time, observe snapshot v1 and watcher status counts. The outer record must be named/versioned in CO-02; no invented current JSON key or record path is asserted here. [Part 6.3 text A.]

**Failure contract.** Workspace id, not reusable name, is the key. Stopped, deleted and never-registered are different timed states. Minimal-profile means no orchestrator, not missing. Unknown/failed read is not current. No route is permitted to wake a stopped workspace. Reader credentials cannot start sessions; no standing secrets appear in metadata, logs or records. [Part 6.3 nine-item checklist.]

**Idempotency and operation.** A repeated status read may append a read audit event but cannot start a process, consume a mailbox or run a sweep. CO-02 must reconcile the source's no-write status criterion with its read-audit requirement: no mutation of observed orchestration state, while the audit sink intentionally records access. Exact sink, retention and consistency contract remain design outputs, not a claimed existing implementation. [PLAN INFERENCE resolving text A's audit/no-write wording.]

**Runbook.** Operator compares control-plane identity to record identity, verifies full versions and age, tests denial with a read-only credential at a non-read route, and verifies audit visibility. Undo disables the route/revokes its credential, not deletes evidence. No transport is selected until Q4/Q18 and actual auth behavior are settled. [PLAN INFERENCE based on Part 6.3.]

**Risks.** Snapshot copying across hosts requires transport, identity envelope, age policy and re-sanitization; none exists merely because a local snapshot does. Signed records do not make embedded strings safe instructions. Narrowing/closing does not decide what the owner meant by TUI Panel. [INV-043; X-005; Part 2.7.]

### Orchestrator v2 knowledge layer #423 (V2)
**Scope.** Align #423's gate and knowledge requirements, then require its own brainstorm, research and checked design before implementation. This is advisory knowledge, not the sweep classifier, management-server relay or a worker-to-worker instruction channel. [Part 2.6; Part 6.4.]

**Current state.** #423 knowledge layer is not started. Its use of v2 differs from #339's trust/orchestrator-of-orchestrators version 2 and research phases. Neither existing collector supplies all desired catalogue fields. There are already at least seven stores before a new catalogue. [E-13; Part 2.6.]

**Target state.** First release is one host, several Runs, facts from named existing collectors and explicitly separate inferred knowledge. It reports to person/coordinator only; unavailable session classes are listed as not observable. Cross-workspace reads require a written read-permission model, not a shared OS account assumption. [Part 6.4 acceptance criteria.]

| Id | Title | Checkable acceptance criteria | Blocked-by | Blocks | Worktree/branch | Owner decisions | Reversibility |
|---|---|---|---|---|---|---|---|
| V2-01 | Rewrite #423 with applicable gate | After one #339 comment, one editor updates title and specified sections; Problem Statement/User Story retained; Q2/Q3-dependent clauses corrected; gate says #539 merged plus #534 live working-class capture; advisory recipient stated; source fields never claimed present | XC-06, XC-02, XC-01 | V2-02, XC-08 | C, last issue in ordered pass | Q2, Q3, Q14-Q16 | Restore before-body |
| V2-02 | Complete separate brainstorm and research | #539 merged and live capture gate met before feature work; dedicated multi-agent memory/context research and design handoff linked; existing sub-orchestrator and technical-reference packages read, not duplicated; no implementation before both outputs | V2-01, SW-03, SW-05 | V2-03 | L, knowledge design context; UNASSIGNED | Q14, Q15 | Retain research; decline implementation |
| V2-03 | Specify catalogue data/operating contract | Every field names source and missing-schema owner; named store/owner/readers/retention/mode and reconciliation with local-only sweep rule; typed field pin, one inert detail field, inference separation; class-specific checkpoint/correction route; scheduler and GitHub-read authority explicit | V2-02, XC-04, XC-05; B-DATA | V2-04 | L, knowledge design branch; UNASSIGNED | Q9, Q14-Q16, Q21 | Amend design before release |
| V2-04 | Deliver advisory knowledge release later | Separate checked implementation plan; source-derived vs inferred entries distinguishable; no new scanner or sweep-class mutation; no transcript/log content catalogue; overlap only possible overlap, not conflict; unsupported classes remain visible as not observable; separate release and never-as-worker decision recorded | V2-03; B-DATA | XC-08 | L, implementation branch; UNASSIGNED | Q14-Q16 | Disable advisory loop; retain authorized facts/evidence |

**Collector-to-catalogue contract.** Producer roles remain sweep per-Run/disk facts and observer Orca ledger rows. V2-03 names the harness-neutral fact schema; it does not retrofit either producer from a v2-only change. Missing command, objective, branch, changed paths, issue and PR need source-owner decisions before use. No direct rescan of Orca/Git/transcripts hides absent data. [Part 6.4 data sources and acceptance criteria.]

**Version and data integrity.** Original schema names/versions and source ages remain attributable in the proposed catalogue; the precise implementation representation is a V2-03 output, not new keys mandated in PR #539. Missing facts are not negative facts. Inferred entries must never overwrite or change a sweep class. [PLAN INFERENCE for provenance representation; Part 2.6.]

**Idempotency.** V2-03 must define stable fact identity, refresh/replacement and inferred-entry reconciliation so repeating a coordinator pass does not multiply facts or re-send advice indefinitely. Store type, uniqueness mechanism and crash recovery are UNVERIFIED until designed; this specification selects no database or extra cache. [PLAN INFERENCE required by the source's named-store requirement.]

**Operational contract.** Refresh uses the existing WC-16 coordinator pass unless owner explicitly authorizes a further scheduler. Existing clocks include observer 15 seconds, watcher cron 5 minutes and PM checkpoints 30 minutes; WC-16 is a cap, not a demand to sweep every 5 minutes. An operator checks the source age/coverage and full capture build before treating advice as informed. [Part 6.4 acceptance criteria; WC-16.]

**Communication contract.** Worker correction passes through coordinator WC-12 and the worker acknowledgement; non-worker/person-started sessions receive no automated prompts. Summarizers have read-only tools. Free text in detail is data even if signed. If Q15 instead requests delivery to agents, trust and delivery phases become additional gates and the advisory plan stops for redesign. [Part 2.6; Part 6.4.]

**Risks.** A catalogue is another store with retention/read authority, not free aggregation. The snapshot does not expose every workspace or issue. Incomplete worker coverage, missing working-class values and inferred overlap can look deceptively holistic. Tests must retain those unknowns and prevent the display from turning a suggestion into authority. [A-005; INV-017; Part 6.4.]

### Cross-cutting contracts, trust and process (XC)
**Scope.** One contract note, one checked amendment rule, one ordered issue-edit pass, explicit human decisions, trust vocabulary rather than a universal trust design, and an invariant-based final gate. [Parts 2.3, 3.6, 4.2, 5.]

**Current state.** Two independent programs, two distinct v1 schemas, three vocabularies and differing `check` permissions have no written shared contract. Issue edits have no server-enforced etag in the cited command. Owner decisions/evidence are scattered. Agreement reached 36/36 points, but the invariant gate failed. [E-03 to E-06; A-010/A-011; INV-030, INV-042; Part 0.1.]

**Target state.** A documented and tested boundary with no runtime v1 link, no hidden writes, no misleading completeness, and roadmaps that preserve genuine prerequisites. Every owner gate is answered or explicitly blocked. [Part 2.3; Seed Success Criteria.]

| Id | Title | Checkable acceptance criteria | Blocked-by | Blocks | Worktree/branch | Owner decisions | Reversibility |
|---|---|---|---|---|---|---|---|
| XC-01 | Maintain owner decision ledger | Q1-Q24 each has recommendation, safe unanswered default, gated items, source and owner answer status; no recommendation recorded as approval; Q1 remains unresolved first action | Owner input only | SW-01, SW-05, OB-01, OB-02, OB-05, WA-01, WA-03, CO-01, V2-01, XC-02, XC-03, XC-05 | C, coordinator decision lane | Q1-Q24 | Owner can supersede decision with trace |
| XC-02 | Serialize version-pinned issue edits | One editor keeps before-bodies and quoted-sentence locators; re-reads updatedAt immediately before each write; aborts on drift; after-write body verified; resumed pass checks already-applied text and never duplicates comment; sequence #450, Coder#477, #409, #339 comment, #423 | XC-01; B-EDIT | WA-02, CO-01, OB-04, XC-06, V2-01 | C only | Applicable question per edit | Restore history; notifications remain |
| XC-03 | Publish shared contract note | After #539 for links, publish `docs/designs/observe-sweep-contract.md`, owned by #339; link source specs rather than duplicate tables; include all registry/unit/schema/verb/word/age/path/build rules below; real-id comparison precedes proven join-key words | SW-03, SW-05, XC-01 | XC-04 | K, master-based branch, not S | Q5, Q9-Q11, Q13, Q17, Q22-Q24 | Revert note and links |
| XC-04 | Pin note to code constants | One comparison test reads note's schema versions, verb lists, join rule and shared words against both producers' constants/templates; deliberate mutation demonstrates failing check; additive schema change requires deliberate producer-test change; no duplicated frozen consumer schema | XC-03 | OB-06, CO-02, V2-03, XC-08 | K, same contract PR | Q5 | Revert own test/note |
| XC-05 | Establish vocabulary and trust boundaries | Owner selects one grant vocabulary/audit format, not one universal design; reader/writer/relay boundaries and poisoned-content rule written; later agent relay needs separate trust design; no signing feature falsely claimed delivered | XC-01; B-DATA | SW-06, SW-07, WA-05, CO-02, V2-03, OB-06 | K for vocabulary, L for later design | Q16 | Amend vocabulary; no execution authority created |
| XC-06 | Add one terminology comment to #339 | No body edit; read version, check duplicate prior comment; cover research phases, #339 version 2, #423 knowledge v2, observer releases, watcher FU steps and undefined management server; links accurate | OB-04, XC-02 | V2-01 | C, fourth issue in edit sequence | Q14-Q16 | Edit comment; notification cannot undo |
| XC-07 | Own #534 follow-up table | After merge, single table gives item/owner/trigger; unknown owner explicitly unowned; persistence, label after FU-1, guard flip, note/routing, R3/R4, identity/status route and word fixes tracked; label row waits for real FU-1 evidence | SW-03; WA-04 for machine-label row only | SW-04, XC-08 | C for table, F for code follow-ups | Q9-Q11, Q17, Q19, Q21 | Edit table; preserve history |
| XC-08 | Independent invariant/coverage gate | Fresh reader checks all 12 seed criteria, all item/decision edges, safe defaults, evidence and honest built/unbuilt status; INV-008 unresolved means FAIL, never voted away; later items explicitly deferred not complete; record PASS/FAIL and exact open blockers | SW-04, SW-07, OB-03, OB-04, OB-05, OB-06, WA-05, CO-03, V2-01, V2-04, XC-04, XC-07, plus declared release scope | None | R, independent context | Unanswered gating questions remain blockers | Revise specification; never waive invariant |

XC-08's listed later predecessors apply only to an **end-to-end target** claim. For first-release alignment it checks those items are explicitly deferred with gates and owners, not delivered. A narrow first-release PASS must not be relabelled end-to-end PASS. CO-03 not-selected under Q3=close is recorded as such. [PLAN INFERENCE; Seed first-release distinction.]

**Contract-note content, normative target derived from Part 2.3.**

- Govern observe snapshot v1 and sweep report JSON v1 only; register watcher status JSON without a version field, dispatch.json v1 and any future Coder/catalogue records separately.
- State one-owner/user/host scope and each collection unit; no Run-less visibility implied.
- State no v1 runtime exchange; neither program reads the other's output.
- Name each producer's writes, including observer persistent snapshots and sweep's always-written report.
- Name schema differences: casing, null/UNKNOWN, row identity and producer unknown-key rules.
- Amend note in the same PR as shared-word, join, schema-version or allowed-verb changes; XC-04 is the mechanical check.
- Optional producer key addition can remain v1 only with deliberate producer-test change; rename/remove/meaning change requires v2.
- Consumers ignore unknown keys and do not enforce a stale copied producer schema.
- Keep prospective join provisional until SW-05 compares real ids; then use Run plus Dispatch and exclude empty/duplicate-flagged rows.
- List observer three argv shapes, including guarded question read; sweep ten exact templates over seven verbs, no check; watcher skills read plus agent-launch write.
- Observer/person/coordinator only; no worker bypass through a plain CLI instead of a slash command.
- Explain binary resolution differences and full-build evidence; release-prefix comparison cannot establish build equivalence.
- List both XDG resolution rules, mode/last-writer/file-survival semantics and Q22 age policy.
- Explain caps: observer 500 rows and six calls with questions; sweep first 50 worker-show in list order and 90-second budget; multiple observers multiply load.
- Record projection.attention as unread by both until values captured; showing verbatim is not permission to classify from it.
- State all strings untrusted and every reader re-sanitizes, including coordinator consumption.

**Required word mapping.** [Part 2.3 mapping table; INV-023.]

| Word | Required distinction |
|---|---|
| stale | Observer feed 45 seconds; stored snapshot uses age policy; sweep transcript-only session uses six-hour window; never substitute one |
| unknown | Observer UNKNOWN versus sweep null/text unknown; never a negative finding |
| unavailable | Observer no source versus sweep attempted read unavailable; not false |
| could not determine | Sweep proof missing; observer does not classify |
| historical | Observer released/retained versus sweep complete-list/window meaning |
| frozen | Observer has no source; sweep requires blocked/failed worker-contract proof |
| settled | Observer Orca outcome verbatim; sweep derives from its outcome set |
| coordinator questions | Mailbox questions seen, not resolved; not equivalent to waiting on a person from a contract |
| reclaimable | Own Orca state until Q23; not automatically live, historical or settled |

**Issue-edit contract and idempotency.** Writer: sole authorized editor. Reader/authority: live issue at its explicitly named fork repository. Input: retained before-body plus reviewed replacement and owner decisions. Version precondition: unchanged updatedAt and quoted target sentence. Failure: drift aborts; fetch/reconcile rather than overwrite. Postcondition: expected body/comment re-read. Retry: compare existing content first; do not duplicate comments or apply an outdated before-body. The time-of-check/write race is still possible because the cited edit route has no etag; serialization reduces, not proves elimination of, lost updates. [A-010, A-011; INV-030; PLAN INFERENCE for retry/readback.]

**PR-merge contract and idempotency.** Writer: authorized maintainer/coordinator using required PR workflow. Consumer: downstream branches based on merged revision. Required record: correct fork, open state, expected head, required review/CI, fresh merge ref and merged revision. Retry begins by checking if already merged; never repeat a push against a merged/changed target by assumption. Undo is a revert PR, not deletion of history. [Project rules; INV-037; PLAN INFERENCE for resume behavior.]

**Risks.** A prose contract without XC-04 drifts. A passing constant check cannot prove live non-consumption, complete collection, authentication, or permission safety. One vocabulary does not erase three threat models. One editor cannot prevent external owner edits, so every issue remains version-checked. [INV-030, INV-042; X-005.]

## 3. Owner decisions
The following preserves Adjudicated Part 7 Q1-Q24. Recommendations are not owner answers. Unanswered defaults are PLAN INFERENCE safety states except where the source gives one explicitly. A default that leaves code unchanged never authorizes a risky live action using that code.

| Decision | Owner choice and recommended answer | Default if unanswered | Gates work items |
|---|---|---|---|
| Q1 | Fix executable Git-config hole by neutralizing both paths or refusing affected worktrees; explicit risk acceptance is the alternative, not the recommendation | INV-008 UNRESOLVED; #539 open; no risk-acceptance caveat authored as owner consent | SW-01, SW-03 |
| Q2 | Claim-only `--pipeline none`; separately accept first-session permission mode in writing for FU-1 test issue only | No prompt behavior change selected, no FU-1 or cron enable; current default remains a documented contradiction | WA-01, WA-02, WA-04, SW-06, WA-05, CO-01, V2-01 |
| Q3 | Narrow Coder#477 to status/identity without prompt routing; close if single-host/no near TUIBBS need; keep only on explicit listener revisit | No #477 rewrite or listener/status implementation; alternatives remain proposals | CO-01, CO-02, CO-03, V2-01 |
| Q4 | TUI Panel means superclaude observe; TUIBBS possible later reader; single-host/read-only | Working reading remains labelled inference; no cross-host transport selected or #477 post | CO-01, CO-02 |
| Q5 | Keep both programs and one contract note; no reader panel/collector merge now | Draft may remain provisional; no note/architecture decision merged as owner-approved | XC-03, XC-04 |
| Q6 | Do not flip before seeded test; owner supplies scope sentence for one Run or any held Run | Guard remains off; no scope widening by agent | OB-02, OB-03, OB-06 |
| Q7 | Owner supplies pass authorship and commits/archives sibling-only records before cleanup | Do not clean sibling, cite missing evidence as missing, no flip | OB-01, OB-03 |
| Q8 | Owner writes dated staged direction/production-integration/command record rather than agents inventing it | AC-S missing; acceptance remains not met as recorded; owner-dependent #409 post/release 3 blocked | OB-01, OB-04, OB-06 |
| Q9 | No producer persistence now; Phase 2 caller stdout capture first, relax one-file rule only if needed | Stdout only; one dated report; no sidecar | SW-04, XC-03, XC-07, V2-03 |
| Q10 | Question reads belong to observer alone for now; sweep wording corrected to uncertainty | Sweep check prohibition retained; no new message-read template | SW-04, XC-03, XC-07 |
| Q11 | Static chat report is sweep summary until contract exists | No extra observe/sweep invocation added to loop | SW-04, XC-03, XC-07 |
| Q12 | Add observer routing entry in own PR after #539, with table-test changes | No routing change merged on assumed approval | OB-05 |
| Q13 | Bare orca acceptable for observer because skills discovery validates it; watcher same; sweep differs | Preserve existing per-caller resolution, document unresolved owner choice | XC-03 |
| Q14 | #423 starts after #539 merged plus #534 capture restoring working class; later management not prerequisite unless agent relay chosen | No #423 implementation/start gate assumed open; draft retains ambiguity as blocked | V2-01, V2-02, V2-03, XC-06 |
| Q15 | Knowledge reports to person/coordinator only, not non-worker sessions | Advisory-only planning ceiling; no automated delivery; a contrary answer requires redesigned gates | V2-01, V2-02, V2-03, V2-04 |
| Q16 | One grant vocabulary and one audit format, not one universal trust design | No unified trust claim; conditional issue text remains unposted; no relay authority | XC-05, OB-04, CO-01, V2-01, V2-03 |
| Q17 | No observer sweep-facts panel now; later yes requires Q9 persistence decision | No runtime observer/sweep link | XC-03, XC-07 |
| Q18 | No snapshot-copy channel before observer R4 or explicit owner TUIBBS plan | No transport/copy service built or promised | CO-01, CO-02, CO-03 |
| Q19 | Choose Fleet Quilt or Decision Desk first in observer after contract and capture; source gives two priorities, owner selects one | Neither priority selected; no new release-3 scope assumed | OB-06, XC-07 |
| Q20 | Named person owns watcher worktree agent and reviews top-level sessions, with allowed volume stated | No watcher-worktree creation/live rollout on assumed ownership | WA-03, WA-02, WA-04, SW-06, WA-05 |
| Q21 | Permit machine-started label in Phase 2 only after FU-1 proves agent-row fields | Existing labels unchanged; no prompt-based origin inference | SW-06, WA-05, OB-04, XC-07, V2-03 |
| Q22 | Owner supplies snapshot/workspace stale age; source offers no preferred number | Readers mark file older than producer cycle stale and print age; no invented workspace threshold; CO-02 must define unknown-cycle behavior before implementation | XC-03, CO-01, CO-02, CO-03 |
| Q23 | Reclaimable stays its own Orca state until owner decides | Print reclaimable; do not call it live/historical | OB-03, XC-03 |
| Q24 | 409 session with live Orca performs shared read-only capture and real-id comparison in one sitting | No capture/join proof; no proven join-key label or knowledge-layer gate | SW-05, OB-02, XC-03, V2-02 |

**Decision runbook.** Present the first needed owner question in plain language, record the exact response and its scope, then unblock only affected work items. Q1 is first. Do not send all 24 as an interactive demand or disguise a recommendation as assent. Section 3 is the complete reference ledger, not a request to answer every row at once. [PLAN INFERENCE; Seed owner-gated process.]

**Decision lifetime.** A changed answer invalidates downstream unsent drafts and unmerged plans that depend on it. Already merged or externally applied effects need a separately authorized revert/reconciliation, not retroactive editing of the decision record. [PLAN INFERENCE; Part 0.4 reversibility.]

**Authority not granted by these questions.** Q1 risk choice does not authorize arbitrary Git allow-list edits; Q2 test permission consent does not authorize all future issues; Q6 pass does not authorize run-use or mailbox writes in normal observer operation; Q16 vocabulary does not authorize relay; Q24 read capture does not authorize seeded message writes. [PLAN INFERENCE preserving NFR-014, INV-012, INV-041 and Part 2.6.]

## 4. Cross-system dependency graph
This is a PLAN INFERENCE graph of the register, not a discovered implementation graph. `A + B -> C` means both predecessors. A question node opens only on its recorded owner answer. A boundary node is a reviewed constraint, never an executable service. Procedural issue-order arrows do not make Coder a functional prerequisite of the observer.

### External and shared-contract nodes

| Node | Meaning and verification |
|---|---|
| Q1-Q24 | Exactly the owner questions in Section 3; no other Q node exists |
| M-APPROVAL | Authorized maintainer merge/launch/issue-write authority; this specification itself does not grant it |
| B-GIT | Executable shared Git-config boundary, INV-008; reviewed at SW-01 and enforced by its chosen ruling |
| B-READ | Orca read-only capture allow-list, full-build evidence, no consumption or run-use claimed safe without its own gate |
| B-QUESTION | Question read scope, diagnostic consumption, build and real-layout boundary; satisfied by OB-01/OB-02 plus Q6, not help text alone |
| B-LAUNCH | Untrusted issue text to permission-free first session; explicit test consent and actual argv evidence required |
| B-EDIT | Serialized issue mutation with version re-read; external concurrent edits remain possible |
| B-IDENTITY | Coder authoritative workspace-id and protected read-only route boundary, no secret registry |
| B-DATA | Untrusted strings and inferred facts stay data; vocabulary/signing never executable authority |
| B-WRITE | Management/answer/handoff writes require their own approved design and coordinator authority; WC-13 holds |
| C-SNAPSHOT | Existing observe snapshot v1 contract, producer observer; defined in OB and XC-03 |
| C-SWEEP | Existing sweep report JSON v1 and one-report-file contract, producer sweep; SW and XC-03 |
| C-WATCH | Existing watcher unversioned status JSON plus dispatch.json v1 and fixed launch contract; WA and XC-03 |
| C-REMOTE | Proposed versioned Coder status record, not implemented; CO-02 defines it |
| C-FACT | Proposed named fact schema and catalogue operating contract, not implemented; V2-03 defines it |

### Work graph: every work item

```text
Owner input -> XC-01
M-APPROVAL -> SW-02
XC-01 + Q1 + B-GIT -> SW-01
SW-01 + SW-02 + M-APPROVAL -> SW-03
SW-03 + XC-07 -> SW-04
SW-03 + XC-01 + Q24 + B-READ -> SW-05
SW-03 + WA-04 + XC-05 + B-LAUNCH -> SW-06
SW-03 + XC-05 + B-WRITE -> SW-07

XC-01 + Q7 + Q8 -> OB-01
XC-01 + Q6 + B-READ + separately authorized seed writes -> OB-02
SW-02 + OB-01 + OB-02 + Q6 + Q7 + Q23 + B-QUESTION -> OB-03
OB-01 + CO-01 + XC-02 + Q8 + Q16 -> OB-04
SW-03 + XC-01 + Q12 -> OB-05
OB-01 + OB-02 + OB-03 + SW-05 + XC-04 + XC-05 + Q19 + B-WRITE -> OB-06

XC-01 + Q2 + B-LAUNCH -> WA-01
XC-01 + Q20 -> WA-03
WA-01 + WA-03 + XC-02 + M-APPROVAL -> WA-02
WA-01 + WA-02 + WA-03 + Q2 + B-LAUNCH + M-APPROVAL -> WA-04
SW-06 + WA-04 + XC-05 + B-WRITE -> WA-05

WA-02 + XC-01 + XC-02 + Q3 + Q4 + M-APPROVAL -> CO-01
CO-01 + XC-04 + XC-05 + B-IDENTITY + explicit remote-reader need -> CO-02
CO-02 + B-IDENTITY + C-REMOTE -> CO-03

XC-06 + XC-01 + XC-02 + Q14 + Q15 + Q16 + M-APPROVAL -> V2-01
V2-01 + SW-03 + SW-05 -> V2-02
V2-02 + XC-04 + XC-05 + B-DATA -> V2-03
V2-03 + C-FACT + B-DATA -> V2-04

XC-01 + B-EDIT -> XC-02
SW-03 + SW-05 + XC-01 + Q5 -> XC-03
XC-03 + C-SNAPSHOT + C-SWEEP -> XC-04
XC-01 + Q16 + B-DATA -> XC-05
OB-04 + XC-02 + M-APPROVAL -> XC-06
SW-03 -> XC-07(base table)
WA-04 + Q21 -> XC-07(machine-label row only)
SW-04 + OB-03 + OB-04 + OB-05 + V2-01 + XC-04 + XC-07 -> XC-08(first-release scope)
SW-07 + OB-06 + WA-05 + CO-03(if selected) + V2-04 -> XC-08(additional end-to-end scope)
```

`Owner input`, `separately authorized seed writes` and `explicit remote-reader need` are external gate descriptions, not work-item ids. First-release and end-to-end are two scope evaluations of XC-08, not two duplicated tasks.

### Decision edges not expanded above

```text
Q2 -> CO-01, V2-01, SW-06, WA-05
Q3 -> CO-02, CO-03, V2-01
Q4 -> CO-02
Q5 -> XC-04
Q6 -> OB-06
Q9 -> SW-04, XC-03, XC-07, V2-03
Q10 -> SW-04, XC-03, XC-07
Q11 -> SW-04, XC-03, XC-07
Q13 -> XC-03
Q14 -> V2-02, V2-03, XC-06
Q15 -> V2-02, V2-03, V2-04
Q16 -> OB-04, CO-01, V2-03, XC-06
Q17 -> XC-03, XC-07
Q18 -> CO-01, CO-02, CO-03
Q19 -> XC-07
Q20 -> WA-02, WA-04, SW-06, WA-05
Q21 -> SW-06, WA-05, OB-04, V2-03
Q22 -> XC-03, CO-01, CO-02, CO-03
Q23 -> XC-03
Q24 -> OB-02, V2-02
```

Q24 appoints the read capture operator; it does not authorize OB-02 writes. The mandatory Q6 scope/seed decision and separate test-write approval still apply.

### Contract production and reading edges

```text
Observer -> C-SNAPSHOT -> XC-03, XC-04, CO-02, V2-03
Sweep -> C-SWEEP -> XC-03, XC-04, SW-05, V2-03
Watcher -> C-WATCH -> XC-03, WA-04, SW-06, CO-02
CO-02 -> C-REMOTE -> CO-03
V2-03 -> C-FACT -> V2-04
```

Observer, Sweep and Watcher here name the existing producers described in Section 2, not additional planned work. These are data/design-reference edges, not runtime connections between observer and sweep. C-REMOTE and C-FACT require design before implementation, so the diagram does not manufacture either interface.

**Shared-file exclusion.** SW-03 completes before OB-05, XC-03 links, or SW-04 source edits. #541 is independently mergeable because its file does not overlap #539. Observer guard work does not overlap sweep source. Each later PR reconciles its own CHANGELOG hunk. [Adjudicated Part 4.1/4.2; INV-029, INV-031, INV-036.]

**Graph integrity check.** Acceptance requires each register id to occur in this graph, every named work-item reference to resolve to the register, all Q1-Q24 to have a decision edge, and every implementation path to cross its authority/trust boundary. Conditional rows remain labelled conditional; they are not omitted to manufacture a cycle-free success claim. [PLAN INFERENCE; Seed Success Criterion 8.]

## 5. Ordered lockstep schedule of waves
This is a PLAN INFERENCE schedule implementing Adjudicated Part 4.2. A wave opens per lane when its own gate is met; Q1 does not freeze unrelated evidence preservation or non-overlapping drafts. No wave authorizes an outward write without owner/maintainer permission.

| Wave | Opening gate | Parallel work and worktree role | Serial work | Exit check |
|---|---|---|---|---|
| W0, owner and safety intake | Sources loaded; no execution assumed | XC-01 ledger in C; preserve sibling evidence for OB-01 without cleaning it; XC-02 prepares before-body process | First surface Q1 and begin SW-01; ask subsequent owner decisions only as needed | INV-008 visibly unresolved or explicit ruling retained; real ownership/worktree map and permissions known |
| W1, independent prerequisites | Appropriate owner answers and separate write consent per lane | SW-02 on existing PR; WA-01/WA-03 in W after Q2/Q20; OB-01 evidence in O after Q7/Q8; OB-02 procedure/design in O after Q6; XC-03 draft in K, no links/commit into S | #541 authorized merge; no test writes until their consent | #541 merged revision read back; prompt/runbook/evidence drafts have checked scope; no #539 alignment expansion |
| W2, sweep fix and rollout edits | SW-01 ruling, SW-02 complete; Q2/Q20 for watcher lane | SW-03 author fixes in S; O may execute authorized OB-02 gate; C prepares reviewed issue drafts; K contract draft remains independent | XC-02 editor posts WA-02 first, then CO-01 after Q3/Q4; no parallel issue writers | #539 fresh merge-ref CI and both threads checked before merge; issue bodies re-read; failed OB-02 keeps guard off |
| W3, independent read release and roadmap pass | SW-03 merged for sweep-following lanes; OB-03 needs only SW-02 plus its own full prerequisites | OB-03 in O (practically here, no hard dependency on #539); SW-05 capture in O/live context after Q24; WA-04 test in W after WA-02 and consent; OB-05 routing in F; XC-07 base table in C | Editor continues OB-04, XC-06 then V2-01; no #409 banner removal before its full pass | Guard either correctly off or reviewed/build-pinned; capture includes full version and real ids; live-test effects and fixture documented |
| W4, contract and bounded follow-ups | SW-03 and SW-05 for final note; Q5; XC-07 base table | XC-03 then XC-04 in K; SW-04 in F if no shared-file edits with K; XC-05 vocabulary after Q16; add XC-07 machine-label row only after WA-04 | Merge each shared-file/changelog change one at a time with refreshed diff; contract test runs after note assembled | Contract test actually reads note; word/verb/schema/join rules complete; first-release gate XC-08 can run independently |
| W5, separately approved designs | First-release boundaries clear; each later item's gate independently met | SW-06 after WA-04; SW-07 management planning; V2-02 brainstorm/research after capture and merge; CO-02 only if remote need chosen; OB-06 planning after note/capture and Q19 | V2-03 after V2-02; new implementation plans approved before delivery; role L paths allocated by coordinator | Plans name contracts/retries/authority and falsifiers; unselected CO route marked deferred; no later code called shipped |
| W6, separate target releases | Checked individual implementation plans and required trust/interaction gates | WA-05 after SW-06; CO-03 after CO-02; V2-04 after V2-03; SW-07 management delivery; OB-06 release 3 only after QUESTION-LINK | Independent reviews and external mutations serialized where ownership overlaps | XC-08 evaluates end-to-end scope only after real behavior evidence; unresolved security/identity/interaction gates fail it |

### Lockstep and concurrency rules

1. Parallel lanes must have distinct worktrees and no shared output file. Identically named logical roles do not authorize two editors in one worktree. [PLAN INFERENCE; Seed lockstep definition.]
2. W0 is first action order, not a claim that all 24 answers are needed before SW-02. Default-blocked lanes stay blocked while independent lanes continue.
3. Code preparation and issue publication have different dependencies. CO-01 is before OB-04 for ordered issue edits only; no observer code waits on Coder implementation.
4. Contract draft may proceed while #539 is open, but its final source links and comparison test wait for merged source. It is never committed onto S. [INV-031.]
5. OB-03 is not forced to wait for #539 by a nonexistent file conflict. It waits for #541 and every question gate; the practical schedule reflects shared owner/live-Orca availability. [Part 4.1.]
6. WA-04 cannot run merely because a document draft says permission-free launch is understood. Written test-specific consent and actual session argv are mandatory. [INV-012.]
7. FU-2 cron enable, later watcher panels and listener reconsideration are follow-on decisions, not implicit W3 actions. [Part 2.4.]
8. Shared capture and seeded consumption test are not interchangeable: one is read-only; the other creates a Run/messages and finally consumes the seeded mailbox. Schedule separate consent and evidence. [INV-005, INV-041.]
9. Every actual PR uses the required monitored fork workflow. The spec author runs none of those writes. [Seed Constraints.]
10. Before starting a later phase, read the existing sub-orchestrator/technical-reference packages identified in Enrichment, and use their current content rather than making duplicate plans by guess.

### Wave interruption rule

At resume, read authoritative state before emitting any write. Re-check PR open/merged/head/ref status, issue updatedAt/body/comment markers, watcher unknown/live-session state, owner answer scope, full Orca build and active Run holder. A completed predecessor is reusable only while its evidence still applies. [PLAN INFERENCE; A-010; INV-007; A-009.]

An expired polling wait is not an exit gate. Re-arm the coordinator's approved wait and keep the decision ledger current; lack of events never means success. Work that requires an unavailable owner decision remains visibly blocked rather than silently passing to the next wave. [PLAN INFERENCE consistent with Seed orchestrator guardrails.]

## 6. What an orchestrator session needs
The orchestrator session is a person-opened coordinator, not a worker. This section is its proposed operating contract, not an instruction for this specification-writing worker to dispatch anything. [Adjudicated glossary; WC-13.]

### Required inputs before execution

- This specification and all three authority documents named in Section 0.
- Current owner answers with provenance, scope and supersession status, especially Q1-Q8 and Q14-Q16.
- Fresh correct-fork PR evidence for #541/#539, not only the source's historical head/check state.
- Exact before-bodies and updatedAt pins for #450, Coder#477, #409, #339 and #423.
- The existing observer owner records and pass provenance, not an agent-authored replacement.
- Exact installed, version-matched Orca orchestration and CLI guides before selecting runtime commands.
- Enrichment's existing sub-orchestrator research package `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115`.
- Enrichment's existing technical-reference package `.dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239` and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`; listed here as supplied pointers, contents not independently read for this variant.
- Actual binary resolution, full Orca build string, Run binding/holder and role for each session.
- Authoritative dispatch/task state and permitted tools for each worker; a plain launch receipt is insufficient ownership evidence.
- Explicit authorization for every outward write, merge and live test, with its cleanup effects stated in advance.

### Worktree and branch map

| Role | Established location/branch | Assignment rule |
|---|---|---|
| S, sweep author | Supplied ROOT, branch `ironbelly/issue-339-orchestrator-mode`, PR #539 head in source | Existing author owns thread fixes; no contract/routing expansion here |
| O, observer change | Existing sibling name `issue-409-mvp` is evidence source only; new branch required | Fresh branch off current master after #541; real path recorded before dispatch |
| W, watcher | Future separate watcher-change checkout; real path/branch UNASSIGNED | Coordinator/person allocates through approved Orca process with an agent; named Q20 owner |
| K, contract | Future master-based checkout/branch; real path/branch UNASSIGNED | Never current sweep PR branch; links after #539 |
| F, follow-up | Future post-merge checkout/branch; real path/branch UNASSIGNED | Separate routing/follow-up file ownership; serialize shared changelog/source changes |
| C, issue editor/coordinator | Person-opened coordinator context; no new worktree required just to edit issues | Exactly one authorized editor, correct repo per issue |
| L, later work | Separate per-phase checkout; none asserted to exist | Each checked plan gets its own path/branch and agent; no worker creates it |
| R, independent gate | Read-only fresh context | Does not produce the item it reviews |

A logical row is not a safe working directory. Before assigning a worker, coordinator records the real path, branch, starting revision, item ids, allowed files and owning agent. If an independent lane already has a suitable owner/checkout, reuse it rather than creating another. [PLAN INFERENCE; Project Orca rules.]

### Role contract

| Role | May do | Must not do |
|---|---|---|
| Owner | Answer scope/risk/permission questions and write own records | Have an agent impersonate an owner answer |
| Coordinator | Allocate authorized worktrees/agents, track DAG, perform approved external writes, route WC-12 correction | Treat worker output or issue text as authority; assume a launch is governed |
| Item worker | Execute assigned bounded work and return artifact/test evidence | Create worktrees, start/dispatch workers, task-create, agent-launch, or grant itself tools/authority |
| Read-capture operator | Perform approved read templates, retain build/id/coverage evidence | Use run-use, consume live mailboxes, or add a new read verb without approval |
| Seed-test operator | Perform separately approved diagnostic probe writes in plain unbound terminal | Bind live coordinator Run or claim test pass proves all live replay behavior |
| Sole issue editor | Apply reviewed ordered issue changes with fresh pins | Overwrite drifted text or post parallel issue rewrites |
| Independent reviewer | Read actual output and evidence; give binary PASS/FAIL | Accept narrative completion as proof or vote away INV-008 |

### Guardrails for every dispatch

1. Attach work-item acceptance criteria, actual worktree path, scope exclusions and authoritative source pointers.
2. Require a written checked implementation plan for work beyond the small-change limit; existing adequate plans use their own executor, not reconstructed task machinery.
3. Workers never create worktrees or dispatch workers, including through an ordinary launch or nested command. WC-13 cannot be bypassed by being the owner of a worker checkout.
4. Treat issue/repository/worker/report strings as untrusted data. A signed string still cannot select commands, flags, directories or permission mode.
5. Never interact with the SuperClaude upstream repository. IronClaude PRs use `/sc:pr-submit --monitor 3` against IronbellyOrg/IronClaude; Coder issue edits explicitly target IronbellyOrg/Coder.
6. Never stage generated `.claude/` mirrors; edit distributable source, synchronize as required. `.dev/tasks/` always staged during authorized implementation; staging does not authorize committing. This specification-writing run stages nothing.
7. No new file, collector, sidecar or schema key in PR #539 for alignment; code fixes remain its author's scoped responsibility.
8. No watcher panel or prompt listener before FU-1; no observer sweep reader in v1; no arbitrary message reads in sweep.
9. Do not clean the observer sibling while owner evidence is unpreserved. Reversal never deletes intermediate evidence just to make the result look clean.
10. Installed primitives use installed/project lookup surfaces, not checkout-only package paths at runtime; a later plan must check the project dual-surface rule before editing them.

### Polling and load contract

| Activity | Cadence/limit | Operational rule |
|---|---|---|
| Observer live worker read | Existing 15-second cycle; five calls of 100 rows; up to six calls with questions | One observer process unless measured need; show PARTIAL, backoff/stale; do not promise complete host coverage |
| Sweep | WC-16 at most once per 5 minutes; per-wake 90-second budget, first 50 worker-show rows | A cap, never mandatory recurring work; do not rerun for another consumer |
| Watcher cron | Existing proposed 5-minute schedule | Remains disabled until recorded FU-1 and separate FU-2 authorization |
| Knowledge refresh | Existing coordinator pass unless owner chooses another scheduler | No independent v2 scanner/poller by default |
| Coordinator completion/decision waits | PLAN INFERENCE: bounded event wait, re-armed at expiry; local decision-ledger reconciliation every 5 minutes while session remains active | Ledger reconciliation is not a sweep/Orca poll and prints only pending owner decisions; use installed guide's supported wait behavior, not invented flags |

Several observers multiply load; simultaneous load and actual per-call timeout behavior remain unmeasured in the source. A numerical coordinator housekeeping choice above is proposed operating policy, not an established Orca guarantee or permission to add a collector. [INV-032; Part 2.3; PLAN INFERENCE.]

### Decision ledger, stops and escalation

The coordinator holds one authoritative ledger with question id, plain-English decision, recommendation, unanswered default, owner response/scope, affected items and next eligible gate. Exact storage path is selected by the approved execution package; no extra sidecar is placed in #539. Show outstanding owner decisions, not heartbeat chatter or fabricated completion tables. [PLAN INFERENCE; Seed requirement for decision ledger.]

Stop only the affected lane for missing owner authority, failed gate, stale issue pin, unexpected PR state, build change invalidating capture, unknown launch identity, changed Run holder, unauthorized read/write verb or missing required input. Continue independent approved lanes. Stop all mutation lanes for evidence of wrong-fork target or a coordinator accidentally running as a worker. [PLAN INFERENCE from project guardrails.]

Escalate a plain-English question with source/evidence, affected items and safe default; never silently expand scope. INV-008 remains first unresolved security question. If the question-read test consumes, keeps guard off. If live layout fails, records that result and does not call the panel usable. If a launch is unknown, preserves at-most-once protection pending live-session reconciliation. [INV-008; INV-007; INV-024/041.]

### Evidence handoff and resume

A worker return includes real artifact paths, changed files, tests actually run and observed results, unresolved facts, and rollback limits. Coordinator reads artifacts and authoritative state, then an independent context checks the unit. A status message, successful launch or self-reported done is not acceptance evidence. [PLAN INFERENCE consistent with Seed Success Criteria.]

On restart, re-read ledger and artifacts, reconcile real PR/issue/Orca state, and resume the first unmet acceptance criterion. Do not regenerate already-posted comments, recreate a Run from a receipt, retry an unknown launch, assume historical build evidence applies, or clean evidence before reconciliation.

## 7. Invariants and edge cases
The assertions below are acceptance tests for the plan, not statements that code has passed. Each sufficiency claim includes the downstream condition that would falsify it. [PLAN INFERENCE applying Seed Success Criterion 12 and Adjudicated Part 5.]

### State, guard, count, collection, interaction and sufficiency

| Kind | Claimed outcome | Invariant/check | Downstream condition that falsifies this fix alone | Item |
|---|---|---|---|---|
| State | Security ruling makes #539 ready | Owner ruling met with regression evidence; both unresolved threads and fresh CI checked | A shared config path still executes, contract scope regresses, other thread remains open, or CI uses old merge ref | SW-01, SW-03 |
| Guard | A false guard prevents question reads | Observe exact code/runtime template gate; tests keep it off absent prerequisites | Another path reads the question mailbox or a global flip exceeds owner scope | OB-03 |
| Guard | Seeded pass permits flipping | Known seeded types survive twice-read then consuming-check comparison; correct build, owner pass and live attempt | Real waiter/ack/replay behavior differs, full build changes, owner scope differs, or layout remains unusable | OB-02, OB-03 |
| Count | Observer represents the host ledger | PARTIAL beyond five 100-row pages; newest-first not contractual | A hidden row contains a blocker, count inferred complete despite cap, or six-call cycle is described as five total | OB-03, XC-03 |
| Collection | Sweep's depth represents its bound Run | Row scope per Run distinguished from host-global worktrees/transcripts and first-50 cap | Unshown worker or out-of-repo contract is treated as absent; host-global files mistaken for owned Run work | SW-01, SW-04, XC-03 |
| State | Snapshot is current | generatedAt age shown; last-writer/no-liveness semantics honored | Process exited, another observer overwrote file, clock/age cannot be established, or remote copy is old | XC-03, CO-02 |
| State | Reclaimable means safe historical work | Q23 explicitly resolved or word shown unchanged | Consumer equates reclaimable with settled, safe-to-close or live without proof | OB-03, XC-03 |
| Interaction | Claim-only is a safe first launch | Q2 written test consent; actual env and argv captured | First session still reads hostile issue text permission-free, custom flags replace mode, or Session Name prompt stalls | WA-01, WA-04 |
| Interaction | Launch receipt means governed handoff | Real Run/Dispatch/owner identity and downstream ledger visibility shown | Only operation id exists, no coordinator owns it, or observer/sweep cannot see it | WA-04, SW-06, WA-05 |
| State | At-most-once prevents duplicate work | Unknown state never reset blindly; live-session reconciliation first | Correct launch parsed as unknown and then relaunched, or test issue re-labelled while watcher enabled | WA-03, WA-04, WA-05 |
| Interaction | One editor prevents lost issue edits | Before-body retained; immediate version re-read and after-write verification | External owner writes between read and edit, or resumed editor uses stale body/comment assumptions | XC-02 |
| Sufficiency | Contract note aligns programs | Comparison test reads actual note/constants and full tables | Runtime build semantics differ, consumers misread unknowns, or note test ignores a changed word/verb/schema | XC-03, XC-04 |
| Sufficiency | Real-id match makes every row joinable | Join uses Run plus Dispatch and excludes empty/duplicate-flagged ids | Dispatch reused across Runs, duplicate flag ignored, ids empty, or Run-less session has no Dispatch | SW-05, XC-03 |
| Guard | Read-only remote route is safe | Coder authoritative identity, protected read-only credential, type rejection and audit tests | Anonymous/spoofed caller, name reuse, read credential starts session, or no verified authenticated route | CO-02, CO-03 |
| Collection | Catalogue creates holistic knowledge | Every field/source/coverage/age named; unobservable classes explicit | Missing objective/PR/path data invented, catalogue rescans directly, hidden capped rows matter, or missing class called complete | V2-03, V2-04 |
| Guard | Advisory output cannot direct agents | Typed fields, inert detail, inferred separation and coordinator-only relay | A string becomes an instruction, inference changes sweep class, or summarizer gains write tools | XC-05, V2-04 |
| Interaction | Question visibility closes human loop | QUESTION-LINK and approved answer/correction/ack mechanism tested | Question displayed but no usable answer channel, answer not acknowledged, or wrong Run receives it | OB-06 |
| Sufficiency | Management plan means work managed | Approved later lifecycle tests and real stage transitions | Only a sweep report exists, resume duplicates work, close has no proof, or worker dispatches worker | SW-07 |
| Sufficiency | All proposals agree, so target is aligned | XC-08 checks required invariants independently of agreement | INV-008 remains unresolved, a required work item omitted, or an unbuilt link described as built | XC-08 |

### Invariant coverage register

The source's addressed/withdrawn findings are not re-opened. This map retains actions or residuals already specified by the adjudicated document.

| Source invariant(s) | Planned evidence/handling |
|---|---|
| INV-001, INV-002, INV-014 | OB-01/OB-03 preserve records, owner authorship and committed pass; no sibling cleanup before preservation |
| INV-003 | Q6 and OB-03 make scope match global guard or leave off |
| INV-004 | Q22, XC-03 and CO-02 define age semantics without a liveness fiction |
| INV-005 | OB-02 unbound-terminal, run-create-only procedure; run-current before/after; no run-use |
| INV-006 | XC-03 lists both XDG rules and paths; no unrequested code normalization |
| INV-007 | WA-03/WA-04 unknown reset requires live-session check |
| INV-008 | SW-01 first; unresolved blocker is never considered fixed by consensus |
| INV-009, INV-010 | SW-01 names allow-list/tests and owner-risk caveats when applicable |
| INV-011, INV-012 | WA-04 records both knobs and actual argv, test-specific written consent and all live writes |
| INV-013 | OB-05 and XC-03 person/coordinator-only line prevents plain-CLI worker bypass |
| INV-015 | SW-04 regression pin restricts worker-written report fields; reader strings remain untrusted |
| INV-016 | XC-03 documents binary resolution distinction; no new speculative risk/fix |
| INV-017, INV-018, INV-019 | XC-03 caps/partial/six-call note and SW-04 first-50-in-list-order wording |
| INV-020 | SW-05 full build evidence, OB-03 build check; A-009 remains unresolved rather than prefix-match proof |
| INV-021 | XC-06 comment covers five numbering namespaces |
| INV-022 | SW-03 re-reads actual threads instead of stale counts |
| INV-023 | Q23/OB-03/XC-03 reclaimable mapping |
| INV-024 | OB-02 real coordinator-layout attempt, separate from synthetic pass |
| INV-025, INV-026, INV-027 | Source marks addressed/no new action; preserve source disposition, no invented remediation |
| INV-028 | SW-05/XC-03 composite join and empty/duplicate exclusions |
| INV-029 | OB-05 tests both machine-read table surfaces and resolvable command syntax |
| INV-030 | XC-02 immediately re-reads updatedAt and aborts drift |
| INV-031 | K master-based contract draft, not sweep PR branch |
| INV-032 | Section 6 states multiplied load and unmeasured simultaneous behavior; no asserted new capacity |
| INV-033 | SW-02 notes #541's brittle wording pin; later CLAUDE changes re-run related test |
| INV-034, INV-035 | Source addressed; watcher gate retained and consumers ignore unknown fields, no frozen copied schema |
| INV-036, INV-037, INV-038 | SW-02/SW-03 non-overlap, current checks, fresh merge ref, no invented rebase requirement |
| INV-039 | SW-01 preserves distinction between git-status scope and contract/transcript allow-list scope |
| INV-040 | SW-03 resolves filtered-count thread with existing paging fields, no new key |
| INV-041 | OB-02/OB-03 help + diagnostic test + build + live layout, not synthetic sufficiency |
| INV-042 | XC-04 comparison test, not prose amendment rule alone |
| INV-043 | CO-01 requires separate TUI meaning decision even if narrowing/closing |
| INV-044 | OB-03 reconciles every not-passed evidence hit in the guard-flip PR |

### Edge-case runbook

- **Owner silent:** preserve safe defaults and blocked lanes; no risk acceptance, scope widening, live test, listener, cron enable or target-complete claim.
- **Orca full build differs:** stop build-dependent gates; retain old evidence labelled with its build; repeat only specifically authorized diagnostic work, not a live consuming read by guess.
- **Worker list truncated:** mark PARTIAL and keep invisible work unknown; do not increase caps inside #539 as alignment work.
- **Missing Run holder:** show access/usability limitation; never solve by binding a live coordinator Run from the observer.
- **Unexpected worker text:** sanitize at every reader, never forward it as executable instructions or a new free-form prompt route.
- **Duplicate/empty row identity:** exclude from joins, retain incompleteness; never join by reusable workspace name or prompt alone.
- **Interrupted live launch:** preserve unknown state and evidence, check live session first; do not forfeit guarantee just to clear the dashboard.
- **Interrupted merge/edit:** inspect current external state; no duplicated comment, outdated body overwrite or push to a now-merged PR.
- **Stopped/deleted remote workspace:** control plane reports state/time; local listener cannot wake it and remote status never appears current from an old snapshot.
- **CO close chosen:** retain CO-02/CO-03 as gated reopening work, not required first-release implementation or falsely complete rows.
- **New request to relay to agents:** stop advisory-only plan; explicit trust/delivery design and authority precede any execution.
- **Multiple concurrent sessions:** real worktree ownership and file locks by process agreement, not shared stash assumptions; each independent worker has assigned files and no nested dispatch.

All runbook behaviors above are PLAN INFERENCE controls derived from the corresponding source findings, not assertions that existing binaries enforce them.

### Coverage of the twelve required outcomes

| Seed criterion | Where this variant satisfies it |
|---|---|
| 1 Scope | Six Section 2 system scopes |
| 2 Verified current state | Section 0 state table and each Section 2 current state with source ids |
| 3 Target state | Each Section 2 target plus honest chain boundary |
| 4 Stable checkable work items | 33 unique register rows; acceptance is evidence, not narrative |
| 5 Dependencies | Register predecessor/successor columns and Section 4 graph |
| 6 Owner decisions | Section 3 Q1-Q24, recommended answer, unanswered default and affected ids |
| 7 Risk/reversibility | Per-system risks, item rollback columns and interface failure/retry contracts |
| 8 Complete dependency graph | Section 4 all work items plus decisions, shared contracts and trust nodes |
| 9 Lockstep waves | Section 5 W0-W6, lanes/worktrees, serial writes, entry/exit gates |
| 10 Four unbuilt links | Section 1 closure owners and later-phase gates; none claimed built |
| 11 Coordinator needs | Section 6 inputs/map/roles/guardrails/cadence/ledger/stops/resume |
| 12 Invariant-based convergence | XC-08 and Section 7; disagreement/agreement never waives INV-008 |

### Honest unresolved facts and limits

INV-008 is UNRESOLVED; no owner ruling or fix has been observed here. A-009 full-build divergence and X-016 live coordinator consumption remain UNRESOLVED. This variant ran no live Orca, GitHub or code tests.

Still UNVERIFIED from the authority sources: exact agent-launch Run/Dispatch creation (D-A), actual launch-reply operation-id shape, claim prompt/pane identity evidence (D-B), real-id join (D-3), live/blocked attention values (D-8), pass-record authorship, actual human usability of the questions panel in the coordinator layout, worker-row pruning, second-host Orca shape, message rate, simultaneous load/per-call behavior, and owner-token access to the owner-shared Coder app. Scheduled work establishes or explicitly retains these unknowns; this document supplies none by assumption. [Adjudicated E-15/E-18, Part 1.2 unresolved facts, Part 5.3; INV-032.]

Future Coder status schema, catalogue schema/store/retention, management mutation retry contracts, real new-worktree paths/branches and QUESTION-LINK delivery mechanism are design outputs, not existing facts. Their work items require evidence before any end-to-end claim.

**Final status of this variant: a proposed alignment specification, not a passed implementation or a resolved invariant gate.** Independent debate/review may compare it with the other variants, but no convergence score or independent PASS is invented here.
