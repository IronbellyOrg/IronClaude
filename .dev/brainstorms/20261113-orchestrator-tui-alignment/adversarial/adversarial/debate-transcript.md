# Adversarial Debate Transcript

## Metadata
- Depth: deep
- Rounds completed: Round 1, Round 2, Round 2.5 invariant probe (separate file `invariant-probe.md`)
- Convergence achieved: 100.0% after Round 2 (44 of 44 points agreed by at least 2 of 3 advocates); Round 1 was 93.2% (41 of 44). Invariant gate not applied here.
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3 (V1 = `variant-1-opus-architect.md`, V2 = `variant-2-opus-analyzer.md`, V3 = `variant-3-haiku-backend.md`)
- Debate points: 44 (S 6, C 11, X 15, A 7, U 5 promoted), from `diff-analysis.md`
- Note: advocate V3 could not write files; its Round 1 and Round 2 text was saved by the orchestrating session in parts (parts are marked in the bodies below).
- Note: advocate V3 changed its preferred base from V3 (confidence 90) in Round 1 to V1 (confidence 75) in Round 2.
- Note: the bodies below are the advocates' saved files appended verbatim; their own headings are kept as written.

## Round 1: Advocate Statements

### Variant 1 Advocate (opus:architect), source `round1-advocate-V1.md`

---
round: 1
role: advocate
variant: V1 (opus:architect, variant-1-opus-architect.md)
inputs: variant-1-opus-architect.md, variant-2-opus-analyzer.md, variant-3-haiku-backend.md, diff-analysis.md, ADJ, seed-brief.md
created: 2026-11-13
---

# Round 1 advocate: Variant 1 (architect)

## Position summary

V1 should be the base of the merged spec: it is the only variant that keeps ADJ's adjudicated edges where ADJ was explicit (cross-issue edit order X-005, one #450 edit set X-006, CAP not waiting for #539 X-003), states the A-001 install gap, flags the "Phase 2" numbering clash, and gives the coordinator the most complete operating contract (6.4 twelve guardrails, 6.5 eleven stop triggers, 6.8 ledger format, 6.9 never-do list) plus a severity-ranked INV coverage map (7.1). It must not be merged as is: it carries one factual error (X-001), one safety-ordering defect (X-002: the join comparison may run the unfixed sweep), a ledger path inside the #539 checkout (X-012), and the same `/sc:pr-submit --monitor 3` authority conflict as the others (X-011); V2's edge evidence and test detail and V3's authority and interface contracts should be grafted onto it.

Evidence basis for this file: I read all three variants in full, `diff-analysis.md` in full, ADJ lines 330-454 and 700-719, the seed brief in full, and re-ran two checks myself (both task packages exist under `.dev/tasks/to-do/`; `git check-ignore` on the debate folder exits 1, i.e. not ignored). Project CLAUDE.md text on `/sc:pr-submit --monitor 3` is quoted from the loaded project instructions. Two owner-feedback memory files were read (`coordinator-never-stop-polling.md`, `orchestration-decision-ledger-only.md`); memory is the lowest source tier and is cited only where marked.

## Steelman of Variant 2

The strongest form of V2's case: a plan that an orchestrator session will execute must make every dependency auditable, and V2 is the only variant where it is. Every one of its 70 edges carries a kind (FILE, PIN, GATE, DEC, PROC, SOFT) and the evidence that makes it real (V2 4.2), so a coordinator can tell a hard file conflict from a habit and does not stall a wave on a preference. It is also the only variant that checks the source of truth instead of transcribing it: Weak points W1 to W8 (V2 2.1-2.5) name each place ADJ is internally inconsistent or thin, with the evidence that would settle it, and 4.4 lists every change against ADJ's graph. Its OBS-NOW checks (`git worktree list`, `git grep ALLOWED_ORCA`, Glob) are named and reproducible, and they were right where V1 was wrong (X-001, SC-01/SC-02). On safety it found the one ordering hole the others missed: running the sweep for the join comparison before INV-008 is ruled "exercises the exact hole on a permission-free host" (V2 R-XC4, edge 61, TB-1 -> XC-05; diff X-002 High). Its SW-02 regression test is the most falsifiable INV-008 requirement of the three (`core.fsmonitor` hook plus `filter.probe.clean` plus `* filter=probe` in `.gitattributes`, fails on run (F1) or on scan instead of `unscanned` (F2); V2 SW-02). Its "Observe:" clause on every acceptance criterion makes each one checkable by command. And its Weak point W4 correctly observes that the note's test cannot land before #539 because the sweep constants exist only on the #539 head (OBS-NOW `git grep`).

What V2 genuinely gets right that V1 lacks: per-edge evidence (U-004), the weak-point discipline (U-005), the TB-1 -> JOIN edge (X-002), research on #423 unblocked per ADJ line 710 (X-008), the Q14 record-versus-code distinction with conditional SW-13 (X-009), an explicit INV-032 gap, a verified worktree map including `issue-394-launch-level-hook` (U-006), and new decisions N1 to N4 no Q covers (U-008).

## Steelman of Variant 3

The strongest form of V3's case: the hardest failures in a multi-session program are not missing edges but missing authority and missing recovery, and V3 is the only variant that specifies them. It separates authority from decisions ("Authority not granted by these questions": Q1 does not authorize arbitrary allow-list edits, Q2 consent does not cover future issues, Q24 read capture does not authorize seeded writes; V3 Section 3), gives every decision a lifetime ("a changed answer invalidates downstream unsent drafts"), and makes merge/launch/write authority an explicit graph node (M-APPROVAL, V3 Section 4), which is the shape the X-011 conflict needs. It writes per-interface contracts with failure, retry and idempotency for the sweep, snapshot, question read, launch, watcher store, issue edit and PR merge (U-010): "a sweep is not a file-idempotent status query", "retry begins by checking if already merged", "`unknown` is uncertainty about a launch, not permission to launch again". It gives the coordinator a wave interruption and resume rule and an evidence-handoff rule ("a status message, successful launch or self-reported done is not acceptance evidence"; V3 Section 6). It separates the read-capture operator from the seed-test operator because one is read-only and the other writes and consumes (concurrency rule 8, U-014). Its XC-08 is an independent invariant gate with two scopes so a first-release PASS cannot be relabelled end-to-end (U-011). It is also the most honest about its own evidence: it ran nothing and labels every live fact historical (C-011; A-007), and its ledger wording ("no extra sidecar is placed in #539") is the only one that does not risk A-004 (X-012).

What V3 genuinely gets right that V1 lacks: M-APPROVAL and B-EDIT/B-WRITE nodes, decision lifetime and non-granted authority (U-012), interruption/resume and evidence handoff (U-013), the two-scope coverage gate (U-011), the contract completion rule for later links (C-002), the read-audit versus "no write" reconciliation for Coder#477 (C-005), the full nine-row word mapping table (U-015), and a periodic ledger reconciliation clock that fits the owner's recorded polling order better than V1's "not on a timer" (X-014, memory `coordinator-never-stop-polling.md`, lowest tier).

## Strengths claimed

1. **Keeps the adjudicated cross-issue edit order hard (X-005, L3).** V1 XC-02 (3) and graph 4.2 `XC-02 -> WA-02 -> CO-01 -> OB-08 -> SW-09 -> V2-01` reproduce ADJ Part 4.2 line 442 exactly: "(2) #450; (3) Coder#477; (4) #409 pass; (5) one #339 comment; (6) #423 rewrite ... accepted by all five advocates". ADJ A-011 (line 391) says "one editor, one ordered edit set per issue; order in Part 4.2". The order is part of a verdict, not a preference; a variant that demotes it (V2 4.4) re-opens an all-advocate verdict. V3 agrees with V1 here (XC-02).
2. **One edit set per issue (X-006, L3).** V1 WA-02 holds all five #450 edits in one item with one `updatedAt` re-read (criterion (6)), matching A-011's "one ordered edit set per issue" (ADJ line 391). Every extra write on one issue opens another INV-030 race window, because `gh issue edit` has no version check (ADJ INV-030).
3. **The seeded test is a hard predecessor of the live-layout attempt (C-003, L3).** V1 OB-03 -> OB-04 is hard (4.2 `OB-03 -> {OB-04, OB-05}`; 5.3 row "OB-03 -> OB-04 -> OB-06"). OB-04 reads coordinator questions "while a Claude coordinator holds the Run" (V1 OB-04 (1)); whether that read consumes on a live coordinator Run is UNRESOLVED (X-016, 61 percent; ADJ line 333). Running OB-04 before OB-03 has shown the template does not consume risks consuming real questions on a live Run. PLAN INFERENCE from X-016 and INV-041; V2 marks this edge SOFT "no causal link" (V2 OB-04, edge 19), V3 folds both into OB-02 with no stated order.
4. **The read-only capture does not wait for #539 (X-003, L2).** V1 XC-03 is blocked only by Q24 and LIVE, run in W1. ADJ 4.1 line 414 draws `CAP -> { O-13, O-14, #534 working class, E423 gate }` with no `P539m` predecessor (SC-35). CAP uses Orca read verbs only and runs no sweep (V1 XC-03 (6)), so it never crosses TB-GIT.
5. **States that `/sc:sweep` is not available on master before the merge, and needs an install (A-001, U-003, L3).** V1 6.6 bullet 2 and 7.3 row 2. Verified by diff SC-06 (`git show origin/master:src/superclaude/core/WORKER-CONTRACT.md | grep -c /sc:sweep` = 0) and SC-05 (WC-16 at `WORKER-CONTRACT.md:288` on the #539 head only). V2 6.7 and V3's polling table cite WC-16's sweep as the coordinator's current cadence.
6. **Keeps the "Phase 2" numbering clash visible (X-010).** V1 1.4 CONTRADICTION MARKER, SW-12 and SW-13 kept separate, SW-09 asked to carry the namespace sentence (INV-021). V2 uses "Phase 2" in both senses without a marker (V2 L1 gate "SW-12 (Phase 2 of #339) started"); V3 is silent.
7. **Contract nodes say which items may change each contract.** V1 4.1 K-node table has a column "Items that may change it", e.g. K-SWJSON "none inside #539 (A-004); SW-11 later" and K-NFR001 "SW-11 only, by owner decision Q9". That is a checkable form of the seed constraint "No new program, collector, JSON key or sidecar inside PR #539 (A-004)". V2's K-1 to K-8 and V3's C-* nodes name owners but not permitted changers.
8. **Checkable A-004 and INV-037 gates at the merge.** V1 SW-05 (1) "a bare CI re-run does not satisfy this item (INV-037)" and (4) "`gh api pulls/539/files` shows no added sweep JSON key or sidecar relative to the reviewed head (A-004)".
9. **Most complete coordinator operating contract (C-008).** V1 6.4 has 12 guardrails, 6.5 eleven stop triggers including two the others lack: "A golden test (`ROW_KEYS`, NFR-001 tests, allow-list tests) fails in a #539 change: stop" and the WC-16 escalation list quoted from `WORKER-CONTRACT.md:288` (confirmed SC-05). 6.8 gives the ledger row format; 6.9 a never-do list; 6.7 shows only outstanding decisions, matching the owner's recorded preference (memory `orchestration-decision-ledger-only.md`, lowest tier).
10. **Graph checks performed, not just required (S-003).** V1 4.3 lists roots, sinks, no-cycle reasoning, the critical path and the four items that share files with #539 (with the reason each waits). V3's "Graph integrity check" states what acceptance requires but does not perform it (V3 Section 4).
11. **Owner decisions mapped to ADJ without over-gating (C-010).** V1 Q11 "none scheduled; recorded in XC-01" matches ADJ Q11, which is about the chat report and changes no file. V3 makes Q11 gate SW-04, XC-03 and XC-07 (the contract note), and Q21 gate OB-04 (the #409 pass), although ADJ 4.2 step 3 gates the #409 pass on "Q8; Q16 for decision 6; REC" only (ADJ line 434).
12. **Severity-ranked INV coverage map including LOW and residual rows (C-009).** V1 7.1 has 33 rows ordered HIGH, MED, MED residual, LOW, then names the ADDRESSED ids it respects without re-opening (INV-016, 022, 025-027, 034-036, 038, 040, 043). This is the form seed criterion 12 ("judged by invariant coverage") needs to detect a dropped row.
13. **Extension slots named before links are built (U-001).** V1 7.5 maps each future capability to the contract it reads, the boundary it crosses and the item holding its slot, so later work extends K-SNAP/K-SWJSON/K-NOTE instead of creating a third "v1" JSON or a fourth vocabulary (E-05, E-06).

## Weaknesses identified in V2 and V3

**Variant 2**

1. **Demotes an adjudicated, all-advocate order to SOFT (X-005, High).** V2 4.4 row "Demoted to SOFT" cites ADJ's "the order is mainly for cross-links". The same ADJ sentence (line 442) opens with "accepted by all five advocates", and A-011 (line 391) says the order is in Part 4.2. Resulting schedule: SW-10 (#339 comment) runs in the Wave 1 editor lane, OB-07 (#409 pass) in Wave 2 (V2 Section 5), i.e. step 5 before step 4; WA-04 (#450 edits 1 and 3) is in Wave 2 after CO-02 in Wave 1, i.e. part of step 2 after step 3.
2. **Splits #450 into three writes (X-006).** WA-02 (edits 2, 5), WA-03 (edit 4), WA-04 (edits 1, 3) across Waves 1 and 2, each needing its own `updatedAt` pin; ADJ A-011 says one ordered edit set per issue; INV-030 says no etag exists.
3. **Live-layout attempt not ordered after the seeded test (C-003).** V2 OB-04 is "OB-03 (SOFT: same sitting)" and edge 19 says "no causal link". The causal link is X-016: the layout attempt reads questions on a live coordinator Run before anything shows that the read does not consume.
4. **Cites the WC-16 sweep as current cadence (A-001).** V2 6.7 "Sweep: at most once per 5 minutes (WC-16)" with no statement that `/sc:sweep` does not exist on master before SW-06 (SC-06).
5. **"Phase 2" in two senses, no marker (X-010).** V2 L1 gate: "SW-12 (Phase 2 of #339) started"; SW-12 is `/sc:close`, resume, trust layer etc., while the same row names the sub-orchestrator package as the nearest design.
6. **Ledger and #539 author unsafely or unsupportedly placed (X-012, A-004, A-005).** XC-01 is "Staged with `.dev/tasks/` per project rule" in "the orchestrator session's checkout", which V2 never names (6.2 marks the main checkout "Not used by this program"); if that checkout is the #539 head, the staged ledger joins PR #539 (A-004). V2 6.3 asserts the #539 author is "The worker in `issue-339-orchestrator-mode`", which no source records and which would make it subject to WC-13 and coordinator dispatch.
7. **Internally inconsistent on merge authority (X-013).** V2 Section 5 lists XC-03 (#541 merge) under "What can run today" because "the merge itself is not owner-gated by any source", while V2 6.3 says the owner "approves every outward action (merges, issue writes)" and 6.6 forbids posting without the owner's go-ahead.
8. **Schedule contradicts its own list (X-015).** "What never waits for #539" includes XC-05, but the wave table schedules XC-05 in Wave 3, whose gate is "SW-06 merged".
9. **Authority conflict with the mandated PR tool (X-011).** V2 6.6 forbids "Post, edit or comment on any issue or PR without the owner's go-ahead" while 6.7 says each PR's review wait "is owned by `/sc:pr-submit --monitor 3` in the worker", which per project CLAUDE.md "pushes the fixes without asking, and replies to and resolves the review comments it fixed". (V1 shares this defect; see Concessions.)

**Variant 3**

1. **Gates the read-only capture on the #539 merge (X-003).** V3 SW-05 (capture plus join) is blocked by SW-03 (#539 merged) and XC-01; ADJ 4.1 (line 414) has no such edge. Because SW-05 also gates V2-02, XC-03 and OB-06, this delays the v2 gate data and the note's attention row for a read that never runs the sweep. Bundling CAP (read verbs only) with JOIN (needs a sweep run) in one item is the root cause: the safe half waits for the half that touches TB-GIT.
2. **Blocks #423 research behind the merge and capture (X-008).** V3 V2-02 (brainstorm and research) is blocked by V2-01, SW-03, SW-05. ADJ line 710: the research pass "may be done ahead of the rest" (SC-34).
3. **Over-gates with questions ADJ does not attach (C-010).** Q11 gates SW-04, XC-03, XC-07; Q21 gates OB-04 (#409 pass) and V2-03; Q9, Q10, Q17 gate the contract note XC-03. ADJ 4.2 gates the #409 pass on Q8, Q16 and REC (line 434) and the note on Q5, #539 links and JOIN wording (line 437). Every extra gate is a default-blocked lane while the owner is silent.
4. **Puts a bookkeeping file on the INV-008 critical path and drops the separate implement item (C-001).** SW-01 is blocked by XC-01 (the ledger); there is no item for implementing the ruling inside #539, only SW-03's "SW-01 ruling met". The regression test is required ("SW-01 requires regression evidence of the measured experiment") but its content is not specified.
5. **Schedule items with no register row (X-015).** W1 schedules "XC-03 draft in K", but register XC-03 is blocked by SW-03 and SW-05 and no draft item exists; Section 1 says "SW-04, SW-05 and XC-07 retain follow-ups" although SW-05 is the capture item.
6. **No per-edge evidence and fewer, coarser items (S-002, S-003).** 33 items; OB-02 merges the seeded test and the live-layout attempt; SW-05 merges CAP and JOIN; edges are `A + B -> C` with no evidence, so a reviewer cannot tell which edges ADJ supports.
7. **Worktree column is letters only (S-006).** Roles S, O, W, K, F, C, L, R with "real path/branch UNASSIGNED"; V3 itself says "A logical row is not a safe working directory". An orchestrator cannot dispatch from it without first producing the map the other two variants already give.
8. **Blanket authorization rule with the same PR-tool conflict, unstated (X-011).** "Explicit authorization for every outward write, merge and live test" while guardrail 5 mandates `/sc:pr-submit --monitor 3`.
9. **#534 table only after merge (X-004).** XC-07 "After merge" follows ADJ A-005 (line 348) literally but ignores A-004 (line 343) "log items in #534" now, without flagging the ADJ inconsistency.

## Concessions (own weaknesses)

1. **Factual error on the task packages (X-001, SC-01).** V1 0.4 item 5 says both packages "were not found in this checkout". I re-ran `ls -d` for this file: both `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115` and `.dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239` exist. The merge must use V2/V3's statement and drop V1's UNVERIFIED label; V1 6.1 should list them as inputs.
2. **The join comparison may run the unfixed sweep (X-002, High, L3).** V1 XC-04 is blocked only by Q24 and LIVE and is scheduled in W1; criterion (4) allows "the sweep from PR #539's head" before the ruling. That runs `git status` in every Orca-listed worktree with the inherited environment on a host where sessions run permission-free (INV-008, INV-011). V2's TB-1 -> XC-05 edge is right; I adopt it: JOIN waits until SW-02 has landed F1/F2 in the run code, or the owner has recorded F3.
3. **The ledger's default path sits inside PR #539's checkout (X-012, A-005).** V1 XC-01 proposes `.dev/brainstorms/20261113-orchestrator-tui-alignment/decision-ledger.md` under ROOT, while V1's own XC risk says "This checkout IS PR #539's head; a note committed here joins #539 and breaks A-004". I verified the debate folder is not git-ignored (`git check-ignore` exit 1). V1 also has no guardrail that SW-02/SW-03 commits stage only their named paths.
4. **Forbids what its mandated PR tool does (X-011, A-002, High).** V1 6.9 "never ... reply on a review thread without the owner's approval" and 6.3 coordinator "never ... posts without owner approval" sit beside 6.4 rule 2 mandating `/sc:pr-submit --monitor 3`, which per project CLAUDE.md "pushes the fixes without asking, and replies to and resolves the review comments it fixed". V1 never states this.
5. **#423 research gating is ambiguous (X-008).** V1 V2-03 is "blocked by V2-02 (implementation-facing parts)" while criterion (2) says research "may be done ahead". V2's split into a separate unblocked research item is cleaner and matches ADJ line 710.
6. **OB-06 hard edge on the contract-note draft is overstated (X-007).** V1 OB-06 (e) is itself disjunctive ("in the contract note draft (XC-05) or ... in the observer spec"), yet the blocked-by cell and graph 4.2 make XC-05 a hard predecessor. The edge should be removed or made soft, with V2's N2 decision on where the `reclaimable` row lives first.
7. **Polling rule conflicts with a recorded owner order (X-014).** V1 6.6 reads GitHub state "at wave gates and before each edit, not on a timer". The owner's order of 2026-11-05 (memory `coordinator-never-stop-polling.md`, lowest source tier, not re-verified) requires re-arming the Orca wait after every expiry and a recurring sweep that re-checks the Run and open PRs. V3's re-armed wait plus periodic ledger reconciliation fits it better.
8. **Weakest live evidence (C-011).** V1 opened one file and ran one Glob that gave a wrong answer. It left the watcher test directory UNVERIFIED (WA-01 (3)) although `tests/issue_watch/` resolves it (SC-24), and it did not verify the worktree map (V2's `git worktree list`, SC-27).
9. **Presents ADJ's PR/issue state as current (A-007).** V1 0.3 and 2.1 state "OPEN and CLEAN", head `873599d59`, `updatedAt` values without "as of ADJ". 6.1's "Live state" input and the per-edit `updatedAt` re-read mitigate but do not label it.
10. **Critical-path actors unnamed (A-003, A-004).** V1 marks "the #539 author's session (UNVERIFIED which session)" and "the 409 session (UNVERIFIED)" but gives no step that resolves either and no fallback.
11. **No per-edge evidence (S-003) and a less falsifiable INV-008 test (C-001).** V1's graph has hard/soft edges but no evidence column; SW-02 (1) asks for a test that "reproduces the probe experiment" without V2's `.gitattributes` line or the F2 "scanned rather than `unscanned`" falsifier.
12. **Q14 gate interpretation less precise (X-009).** V1 V2-02 (3) lets a record say the `working` class "is not yet" restored; it does not separate "capture recorded" from "class shipped" as V2's W5 and conditional SW-13 do.
13. **Took "now" for the #534 table without flagging ADJ's inconsistency (X-004).** The choice is right, but V1 SW-06 does not record that ADJ A-005 says "#539 merged"; V2's W1 does.
14. **Owner load unsized (A-006).** V1 orders Q1 to Q4 first and the rest by wave but does not count how many answers each wave needs or treat owner latency as the schedule.

## Shared assumption responses

| A-id | Response | Reason |
|---|---|---|
| A-001 (coordinator can run `/sc:sweep` under WC-16 from the start) | **REJECT** | The assumption is false before SW-05: `/sc:sweep` has 0 matches in `origin/master:WORKER-CONTRACT.md` (SC-06) and WC-16's sweep duty exists only on the #539 head (SC-05). The merged spec keeps V1 6.6 bullet 2 and 7.3 row 2: before the merge the coordinator uses WC-16 liveness supervision only; after it, `/sc:sweep` needs `superclaude install` or `make sync-dev`, recorded in the ledger. |
| A-002 (mandated `/sc:pr-submit --monitor 3` fits "owner approves every outward write") | **REJECT** | Project CLAUDE.md: the tool "pushes the fixes without asking, and replies to and resolves the review comments it fixed". All three variants, V1 included, must state the rule explicitly. Proposed merged rule (PLAN INFERENCE): the owner's approval to open a given PR (one ledger row per PR) authorizes `/sc:pr-submit --monitor 3`'s own pushes, replies and resolves on that PR's review threads; it does not authorize a merge, any issue post, any reply outside that PR, or any change beyond the work item's scope. If the owner refuses that, the variant must name the owner-approved alternative before any PR item starts; the coordinator does not lower the monitor level on its own. |
| A-003 ("the 409 session" exists and can run live Orca reads from a terminal with no Run) | **QUALIFY** | ADJ recommends it for Q24, and worktree `issue-409-mvp` exists at `f104ca51a` (SC-27), but no source shows a live session there. Keep it as the recommended answer to Q24, and add: at XC-09 start the coordinator records whether that session exists; if not, the default runner is the owner from a plain terminal that holds no Run, and XC-03, XC-04 and OB-03 stay unscheduled until Q24 names someone. |
| A-004 (a #539 author session exists to do SW-02/SW-03 and push) | **QUALIFY** | Correct that it is unstated; V2's "the worker in `issue-339-orchestrator-mode`" has no source. The merged spec should make "name the #539 author session" a W0 exit condition: the owner names the session (person-opened, not a dispatched worker, so it is not routed through `worker-start`), or opens one in this checkout. Until named, SW-02, SW-03 and SW-05 have no actor and the ledger shows that as the blocker. |
| A-005 (program artifacts stay outside PR #539) | **ACCEPT** | It is an unstated and currently unprotected assumption: this debate's folder is untracked and not ignored in the #539 checkout (re-checked: `git check-ignore` exit 1). The merged spec needs a guardrail: no ledger, record or program file is created in the #539 checkout; SW-02, SW-03 and SW-05 commits stage only the paths their acceptance criteria name; SW-05 (4) (`gh api pulls/539/files` shows no added file) is the check. |
| A-006 (owner can absorb ~24 answers plus every merge and post) | **ACCEPT** | No variant sizes it. The merged spec should state that owner latency is the real schedule, list per wave which Qs and approvals it needs (V1 Section 3 "Wave needed by" is the base), and ask one question at a time (seed; memory `orchestration-decision-ledger-only.md`). |
| A-007 (ADJ's PR and issue state is still current) | **ACCEPT** | V1 presents it as current; V2 and V3 label it historical. The merged spec labels every PR head, check state and `updatedAt` "as of ADJ" and requires the coordinator to re-read them at session start and before each gate (V1 6.1 "Live state", V3 "Wave interruption rule"). |

## Per-point positions

Coverage: all 44 debate points (S-001 to S-006, C-001 to C-011, X-001 to X-015, A-001 to A-007, promoted U-004, U-005, U-010, U-011, U-012). Levels from diff-analysis: L3 = 16, L2 = 20, L1 = 3 among S/C/X/A; U points carry no level.

| Point | Level | Preferred | Conf. | One-line evidence |
|---|---|---|---|---|
| S-001 Section skeleton | L1 | MERGE (V1 base) | 65 | V1 seed-ordered 0-7 plus 7.5 scaffolding; add V2 weak-point blocks and V3 interface sub-blocks where they carry content |
| S-002 Register size and id collisions | L2 | V1 | 65 | V1's 46 items keep ruling/implement (SW-01/SW-02) and #541/refresh/merge (SW-04/SW-05) separate; add V2's SW-13 (conditional) and research split; re-key once from V1 ids |
| S-003 Graph notation | L2 | MERGE (V2 edge table) | 75 | V2's 70 edges each carry kind and evidence (U-004); keep V1's hard/soft text graph and performed checks 4.3 |
| S-004 Wave design | L2 | MERGE (V1 base) | 65 | V1 W0-W5 with lanes, exit checks, 5.2 "today" and 5.3 serial table; add V3 interruption rule and V2's "never waits for #539" list once corrected (X-015) |
| S-005 Trust and contract node sets | L3 | MERGE | 70 | Keep V1 TB-UPSTREAM, TB-WC13 and K "items that may change it"; add V3 M-APPROVAL and B-EDIT (needed for X-011, A-002) and V2 TB-3 (remote start route) |
| S-006 Table conventions | L1 | MERGE | 70 | V1 named worktree and "Wave needed by"; V2 "Observe:" per criterion; V3 decision lifetime; reject V3 letter-only worktree column |
| C-001 INV-008 requirement and test | L3 | MERGE | 75 | V1's two items (ruling, implement) and scope criterion (INV-039); V2's `.gitattributes` test and F2 "scanned vs `unscanned`" falsifier; V1 7.3 "other executable keys in scope?" |
| C-002 Chain-to-target closers | L2 | MERGE | 65 | V1 "what near-term waves deliver instead"; V2 root-cause column; V3 contract completion rule |
| C-003 Guard-flip sequence | L3 | V1 | 80 | OB-04 reads questions on a live coordinator Run; consumption UNRESOLVED (X-016), so OB-03 must precede OB-04 hard; V2 SOFT, V3 merged |
| C-004 Watcher decomposition | L2 | V1 | 70 | One #450 edit set (A-011, ADJ line 391); add V3's launch-store and interruption runbook text to WA-03/WA-04 |
| C-005 Coder#477 decomposition | L2 | MERGE (V1 base) | 60 | V1 CO-01..CO-04 keeps Q4 inside one reply; add V3's read-audit vs "no write" reconciliation to CO-03 |
| C-006 #423 decomposition and research timing | L2 | V2 | 75 | ADJ line 710 "may be done ahead of the rest"; V2-04 research unblocked; V1 ambiguous, V3 contradicts |
| C-007 Contract note and test | L2 | V1 | 60 | V1 already gates XC-06 on SW-05 "(sweep constants exist on master only after merge)"; add V3's nine-row mapping table and V2's W4 evidence |
| C-008 Orchestrator session needs | L2 | MERGE (V1 base) | 70 | V1 6.4/6.5/6.8/6.9 most complete; add V2 verified worktree map, V3 role split (read-capture vs seed-test operator), evidence handoff and resume |
| C-009 Invariants and sufficiency | L3 | MERGE | 65 | V1 7.1 severity-ranked coverage plus residuals; V2 per-invariant check command and explicit INV-032 gap; V3 two-scope gate |
| C-010 Owner-decision gate mapping | L2 | V1 | 65 | V1 Q11 gates nothing, Q21 gates only the label; V3 attaches Q11/Q21 to the note and #409 pass, beyond ADJ 4.2 lines 434, 437 |
| C-011 Evidence basis | L1 | V2 | 80 | V2 OBS-NOW checks named and correct; V1's one Glob was wrong (SC-01) |
| X-001 Task packages exist | L2 | V2 (and V3) | 98 | Re-verified with `ls -d`: both directories exist; V1 0.4 item 5 is wrong |
| X-002 Sweep run for JOIN before INV-008 ruling | L3 | V2 | 85 | TB-1 -> XC-05: running the unfixed sweep exercises INV-008 on a permission-free host (INV-011); V1 allowed it, V3 over-delays via the merge |
| X-003 CAP waits for #539? | L2 | V1 (and V2) | 85 | ADJ 4.1 line 414: CAP has no P539m predecessor; read verbs only, no sweep run |
| X-004 #534 table timing | L2 | MERGE (V1 timing + V2 W1 flag) | 70 | Post now (ADJ A-004 line 343 "log items in #534"), and record ADJ A-005 line 348's "#539 merged" as a noted inconsistency |
| X-005 Cross-issue edit order hard or soft | L3 | V1 (and V3) | 80 | ADJ line 442 "accepted by all five advocates"; A-011 line 391 "order in Part 4.2"; V2 posts #339 comment before #409 pass |
| X-006 #450 one edit set or several writes | L3 | V1 (and V3) | 80 | A-011 "one ordered edit set per issue"; INV-030 no etag, so each extra write is another race |
| X-007 Guard flip waits for note draft? | L3 | V2 | 70 | V1 OB-06 (e) is disjunctive, so the hard XC-05 edge is overstated; ADJ step 4 lists no note predecessor; take V2 N2 to decide where the row lives |
| X-008 #423 research before gate | L2 | V2 | 80 | ADJ line 710 (SC-34); V3 contradicts, V1 ambiguous |
| X-009 Meaning of Q14's gate | L3 | V2 | 70 | V2 W5 separates "capture recorded" from "`working` class shipped" and adds conditional SW-13; ADJ A-013 says capture "unblocks" the class (line 335) |
| X-010 "Phase 2" numbering | L2 | V1 | 85 | V1 1.4 CONTRADICTION MARKER; V2 uses both senses unmarked |
| X-011 Outward-write autonomy vs `/sc:pr-submit --monitor 3` | L3 | NEITHER (new rule) | 85 | All three conflict with project CLAUDE.md; merged spec needs the per-PR authorization rule in A-002 above plus V3's M-APPROVAL node |
| X-012 Decision-ledger location | L3 | V3 | 80 | V3 "no extra sidecar is placed in #539"; V1's default path is in the #539 checkout; V2's staged ledger risks the same; add "never in the #539 checkout" explicitly |
| X-013 Who merges #541 | L2 | V1 | 70 | Owner merges is the conservative reading of "no outward writes without the owner"; V2 is internally inconsistent (Section 5 vs 6.3) |
| X-014 Coordinator polling clock | L3 | MERGE (V3 base) | 65 | Owner order 2026-11-05 to re-arm waits and keep a recurring check (memory, lowest tier); V1 "not on a timer" and V2 "no new clock" conflict with it; keep WC-16 5-minute cap on sweeps |
| X-015 Internal scheduling inconsistencies | L2 | NEITHER (fix all) | 75 | V1: X-001, X-012; V2: XC-05 listed as "never waits" but scheduled after SW-06; V3: W1 drafts XC-03 that has no draft item |
| A-001 `/sc:sweep` available from start | L3 | V1 | 90 | SC-06 (0 matches on master); V1 6.6 and 7.3 state it; REJECT the assumption |
| A-002 PR tool vs owner approval | L3 | NEITHER (new rule) | 85 | Same root as X-011; REJECT the assumption; per-PR authorization rule |
| A-003 "The 409 session" exists | L2 | MERGE | 70 | QUALIFY: keep as Q24 recommendation; record existence at start; fallback owner from a terminal with no Run |
| A-004 #539 author session exists | L2 | MERGE | 70 | QUALIFY: naming the author is a W0 exit; V2's "worker" label unsupported |
| A-005 Program files stay out of #539 | L3 | V3 | 75 | ACCEPT; only V3 states it; debate folder not ignored (re-checked); add path-scoped staging guardrail |
| A-006 Owner capacity | L2 | MERGE (V1 base) | 65 | ACCEPT; V1 "Wave needed by" column is the base for per-wave question counts |
| A-007 ADJ state current | L3 | V2 (and V3) | 75 | ACCEPT; V2/V3 label it historical; V1 must add "as of ADJ" and a start-of-session re-read |
| U-004 V2 edge-kind taxonomy | n/a | V2 | 80 | Adopt FILE/PIN/GATE/DEC/PROC/SOFT with evidence per edge; it makes X-005-style disputes checkable against ADJ |
| U-005 V2 weak points W1-W8 | n/a | V2 | 75 | Adopt as a "Where this spec departs from ADJ" section; W2, W4, W5 are sound; W3 is consistent with V1 (no SW-05 -> OB-06 edge); W6 is a PROC edge on a stated basis; W7 and W8 rejected (X-005) |
| U-010 V3 per-interface contracts | n/a | V3 | 70 | Adopt failure/retry/idempotency for sweep, launch, watcher store, issue edit, PR merge; trim restatements already in ADJ |
| U-011 V3 two-scope coverage gate | n/a | V3 | 80 | Adopt XC-08 with first-release vs end-to-end scopes; prevents a narrow PASS being relabelled end-to-end |
| U-012 V3 authority not granted, decision lifetime | n/a | V3 | 80 | Adopt both; they bound what each owner answer authorizes (e.g. Q24 read capture does not authorize OB-03 seeded writes) |

## What an ideal merged spec would take from each variant

**Base: V1** (skeleton, register ids, per-system tables, owner table, waves, Section 6, Section 7.1/7.5), with these corrections and grafts.

From V1 (keep):
- 0.1 INV-008 first, requirement only; SW-01 ruling and SW-02 implement as separate items; SW-02 (2) scope separation (INV-039) and (4) no key or file.
- 1.1 "what the near-term waves deliver instead" column; 1.4 numbering CONTRADICTION MARKER (X-010).
- 2.x SW-05 merge gate with (1) no bare re-run (INV-037) and (4) `gh api pulls/539/files` check (A-004).
- 2.2 OB-03 -> OB-04 -> OB-06 hard chain (C-003); OB-06 criteria (a) to (i) except the hard XC-05 edge (X-007).
- 2.3 WA-02 single #450 edit set (X-006); WA-04 nine FU-1 preconditions.
- 2.6 XC-02 cross-issue order as a hard chain (X-005); XC-03 CAP gated only by Q24 and LIVE (X-003); XC-06 gated on SW-05 because the sweep constants exist only after the merge (C-007).
- 3 owner table with "Wave needed by"; Q11 gates nothing; Q21 gates only the label (C-010).
- 4.1 K-node "Items that may change it" column; TB-UPSTREAM and TB-WC13; 4.3 performed graph checks.
- 5.2 "what may run today", 5.3 serial-constraints table, 5.4 worktree map (with names marked PLAN INFERENCE).
- 6.4 guardrails, 6.5 stop triggers (incl. golden-test stop and WC-16 escalation list), 6.6 bullet 2 and 7.3 row 2 on `/sc:sweep` availability and install (A-001), 6.7 ledger-only status, 6.8 ledger row format, 6.9 never-do list.
- 7.1 severity-ranked INV coverage map; 7.3 sufficiency rows; 7.4 edge cases; 7.5 extension slots.

Corrections to V1 (required before it is a usable base):
- X-001: replace 0.4 item 5 with "both packages exist" and list them in 6.1 inputs.
- X-002: add TB-GIT -> XC-04 (JOIN waits for SW-02 landed with F1/F2, or F3 recorded); XC-04 (4) loses "from PR #539's head" unless that head already contains the fix.
- X-012/A-005: ledger path "chosen by the coordinator, never in the #539 checkout"; guardrail that #539 commits stage only the named paths; no program artifact in that checkout.
- X-011/A-002: replace 6.3/6.9 wording with the per-PR authorization rule (owner approval to open a PR covers `/sc:pr-submit --monitor 3`'s pushes, replies and resolves on that PR only; merges and issue posts stay owner-approved one by one).
- X-007: OB-06 drops the hard XC-05 edge; (e) keeps its disjunction; add N2.
- X-008: split V2-03 into a gated brainstorm item and an unblocked research item.
- X-014: replace "not on a timer" with a re-armed Orca wait and a recurring ledger and PR-state reconciliation, still under WC-16's 5-minute cap for sweeps (owner order in memory, lowest tier; confirm with the owner as one ledger question if in doubt).
- A-003/A-004/A-007: W0 exit names the #539 author session and the Q24 runner (or records the fallback); every ADJ live fact labelled "as of ADJ" and re-read at session start.

From V2 (graft):
- 4.2 edge table with kind and evidence for every edge (U-004), applied to V1's register; 4.4 "where this graph differs from ADJ" kept as a section (U-005), restricted to W1, W2, W4, W5, W6 (W7, W8 rejected under X-005; W3 already matches V1).
- SW-02 regression test detail: `core.fsmonitor` hook, `filter.probe.clean`, `* filter=probe` in `.gitattributes`, F1 fails if either runs, F2 fails if scanned rather than `unscanned`; 7.2 F2 detection-location falsifier (C-001).
- "Observe:" clause on every acceptance criterion (S-006).
- SW-13 conditional `working`-class item and V2-02's conditional edge (X-009); V2-04 research unblocked (X-008).
- OBS-NOW checks and the verified worktree map in 6.2, including `issue-394-launch-level-hook` (do not touch) and the main checkout (do not switch) (C-011, U-006).
- N1 to N4 decisions in Section 3 (U-008); XC-09 build-string rule as one cross-cutting check (U-009); explicit INV-032 gap in coverage (C-009).
- W1 flag on X-004 recorded beside V1's "now" timing.

From V3 (graft):
- M-APPROVAL authority node and B-EDIT, B-WRITE boundaries in 4.1 (S-005), carrying the X-011 rule.
- Section 3 "Authority not granted by these questions" and "Decision lifetime" (U-012); "Decision runbook" (one question at a time).
- Interface failure/retry/idempotency blocks for sweep, launch, watcher store, issue edit and PR merge (U-010), placed as one sub-block per system, not repeated in tables.
- XC-08 independent invariant and coverage gate with first-release and end-to-end scopes (U-011); contract completion rule for each later link (C-002).
- Wave interruption and resume rule; evidence handoff ("a launch receipt or self-reported done is not acceptance") (U-013).
- Role split of read-capture operator and seed-test operator with separate consent (U-014).
- CO-03 reconciliation of read audit versus "no write" (C-005); the nine-row word mapping table inside XC-05's content list (U-015).
- X-012 ledger wording "no extra sidecar is placed in #539"; the A-007 "historical evidence" label.

Not taken: V2's SOFT demotion of the cross-issue order and its three-write #450 split (X-005, X-006); V2's SOFT OB-03 -> OB-04 edge (C-003); V3's #539-merge gate on CAP and on #423 research (X-003, X-008); V3's extra Q11/Q21/Q9/Q10/Q17 gates on the note and the #409 pass (C-010); V3's letter-only worktree column (S-006).

**Overall preferred base: V1, confidence 70**, conditional on the four required corrections above (X-001, X-002, X-012/A-005, X-011/A-002), which are defects, not matters of taste.

### Variant 2 Advocate (opus:analyzer), source `round1-advocate-V2.md`

# Round 1 Advocate: Variant 2 (opus:analyzer)

Advocate for `variant-2-opus-analyzer.md` (V2). Opponents: V1 = `variant-1-opus-architect.md`, V3 = `variant-3-haiku-backend.md`. Diff points from `diff-analysis.md` (DA). ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`.

## Position summary

V2 should be the base of the merged spec, at about 70 percent confidence. It is the only variant in which every dependency edge carries a kind and evidence that a reviewer can re-check (V2 4.2, 70 edges). It is also the only one that both blocks the unfixed sweep from running before the INV-008 ruling (TB-1 -> XC-05, DA X-002) and has no factual error in its stated state (DA SC-01, SC-02, SC-27, SC-28). V2 also has three real defects that the merge must fix by taking V1 or V3's position: it demotes the adjudicated cross-issue edit order to SOFT (X-005), it splits #450 into three writes (X-006), and its guardrail "no write without the owner" conflicts with `/sc:pr-submit --monitor 3` (X-011, A-002).

## Steelman of Variant 1

The strongest case for V1 is that it is the most conservative and complete operating contract. It keeps the adjudicated cross-issue edit order as a hard chain (V1 4.2 "`XC-02 -> WA-02 -> CO-01 -> OB-08 -> SW-09 -> V2-01`", matching ADJ line 442, "accepted by all five advocates"). It keeps #450 as one ordered edit set (V1 WA-02, matching A-011). It is the only variant that states in time that `/sc:sweep` and its WC-16 duty do not exist on master before #539 merges and is installed (V1 6.6; V1 7.3 row 2; confirmed by DA SC-06 and A-001). It flags the "Phase 2" numbering collision with an explicit contradiction marker (V1 1.4, X-010), which V2 missed. Its section 6 is the fullest coordinator brief: 12 guardrails, 11 stop triggers including the WC-16 escalation list quoted from `WORKER-CONTRACT.md:288` (V1 6.5), a ledger row format (V1 6.8), and a status-output rule (V1 6.7). Its invariant coverage map is organised by severity and includes the LOW rows and residuals (V1 7.1), and its 7.5 table names an extension slot for each later link. V1 also correctly keeps #541's merge with the owner (V1 SW-04 "owner merges"), which matches the rule that merges are outward writes. Where V1 is right, it is right on safety and process, which is what an orchestrator session needs most.

## Steelman of Variant 3

The strongest case for V3 is that it is the variant most aware of failure, retry and authority, the parts an unattended coordinator gets wrong. It gives each interface a producer, a consumer, a failure rule, a retry rule and an idempotency rule (V3 "Sweep interface contract", "Snapshot interface contract", "Issue-edit contract and idempotency", "PR-merge contract and idempotency"), for example "Retry: compare existing content first; do not duplicate comments". It adds a wave interruption and resume rule (V3 5 "Wave interruption rule") and an evidence-handoff rule that a launch receipt or self-reported done is not acceptance (V3 6 "Evidence handoff and resume"). It is the only variant that says what each owner answer does *not* authorize (V3 3 "Authority not granted by these questions"), and that a changed answer invalidates unsent drafts (V3 3 "Decision lifetime"). It models approval as a graph node (M-APPROVAL, V3 4), which is the right shape for the X-011 conflict. Its XC-08 makes invariant coverage an independent gate with two scopes, first release and end to end, so a narrow PASS cannot be relabelled as end-to-end (V3 XC-08 and the paragraph after it). It separates the read-only capture operator from the seed-test operator, which need different consent (V3 rule 8; V3 6 "Role contract"). It reads all live state as historical and asks for fresh reads before acting (V3 0 "Authority and labels"; V3 6 "Required inputs"), which is the right stance for A-007. Its waiting for the #539 merge before the capture (X-003) is over-cautious, but it is cautious in the safe direction.

## Strengths claimed

1. **Every dependency edge can be audited.** V2 4.2 gives 70 numbered edges, each with a kind (FILE, PIN, GATE, DEC, PROC, SOFT) and the evidence that makes it real, for example edge 64 "SW-06 -> XC-07 FILE, PIN: the test reads `ALLOWED_ORCA` and report constants that exist only on #539". V1's graph (V1 4.2) and V3's boolean graph (V3 4) give no evidence for each edge (DA S-003, U-004). For a spec meant to drive an orchestrator session, an edge that cites its cause is one the coordinator can drop or keep when the facts change. Gate soundness is the criterion the brief weights most.
2. **It is the only variant that stops the unfixed sweep from running before the INV-008 ruling.** V2 XC-05 is blocked by TB-1, and risk R-XC4 says: "Running the sweep for XC-05 before INV-008 is ruled exercises the exact hole on a permission-free host." V1 XC-04 is blocked only by Q24 and LIVE and runs in W1, "with the sweep from PR #539's head" (V1 XC-04 (4); V1 5.1 W1), which means running the unfixed `git status` across every listed worktree on a host where sessions run permission-free (ADJ 2.2 action 1; INV-011). V3 is safe here, but only because it delays the whole capture until after the merge, which ADJ does not require (DA X-002, X-003, SC-35).
3. **Its stated current state has no factual error, and each live check names its command.** V2 marks each read-only check as OBS-NOW and names the command (`git worktree list`, `git grep ALLOWED_ORCA`, Glob) (V2 0.3; C-011). The spot checks confirm them: SC-02 (both task packages exist), SC-27 (worktree map), SC-28 (`ALLOWED_ORCA` absent from master `src/`), SC-23 (`SCHEMA_VERSION = 1`), SC-24 (`tests/issue_watch/`). V1 says the two task packages "were not found in this checkout" (V1 0.4 item 5), which is wrong (DA X-001, SC-01). V1 also leaves the watcher test directory UNVERIFIED (V1 WA-01 (3)), although it can be found (SC-24).
4. **It argues with the source where the source is thin, and names what would settle each case.** Weak points W1 to W8 (DA U-005) each say where ADJ's own order or claim rests on thin evidence. Three of them find real inconsistencies in ADJ:
   - W1: ADJ 3.2 row A-005 says "#539 merged" while A-004 and 2.2 action 7 say "log items in #534" now (ADJ lines 343, 348, 212; DA SC-36).
   - W2: flip prerequisite (e) points at a mapping table that lives in a note that cannot land before #539 (ADJ 2.1 action 4 (e); ADJ 2.3).
   - W5: Q14 joins a record ("capture recorded") with a code change ("restores the `working` class"). ADJ line 699 says "the #534 live capture that restores the sweep's `working` class is recorded", and ADJ 4.1 line 414 has CAP unblocking the `working` class, so the class itself is later work.
   V1 resolves W1 silently ("logged there now") and V3 follows A-005 without comment (DA X-004). V2 is the only variant that leaves the owner a decision with evidence attached.
5. **Its acceptance criteria are the most checkable.** Each criterion ends with "Observe:" and names the command, file or record a reviewer uses (V2 0.3; DA S-006). For example, SW-05 says "the new CI run's checkout is not `8c689986`", and OB-05 (f) says `git grep -n "not passed" .dev/issues/409/` returns nothing. V2's INV-008 regression test is the most precise of the three. It sets `core.fsmonitor` hook plus `filter.probe.clean` plus `* filter=probe` in `.gitattributes`. It fails if either command runs (F1) or if the worktree is scanned rather than `unscanned` (F2) (V2 SW-02; DA C-001). This matches ADJ 2.2 action 1, "Keep the probe experiment as the regression test", and it specifies the test, not the fix.
6. **Its #423 timing matches the source.** V2-04 (research) has no hard predecessor, because the #423 AC says research "may be done ahead of the rest" (ADJ line 710; DA SC-34, X-008). V3 blocks research behind V2-01, SW-03 and SW-05 (V3 V2-02). V1 gates its combined item on V2-02 while its own criterion says research may run early (V1 V2-03), which is ambiguous.
7. **It keeps the guard flip independent of #539, with stated evidence.** V2 W3 removes ADJ's `P539m --> GF (practically)` edge. It cites INV-036 (the flip touches `observe/` only) and says the "practical" cause is already the OB-03 edge (V2 4.4). It also keeps the flip free of any contract-note predecessor (W2; DA X-007). V1 makes OB-06 wait for XC-05 "(for (e))" (V1 OB-06 blocked-by). That is a cross-cutting coupling ADJ step 4 does not list, and it contradicts V1's own criterion (e), which allows the row in the observer spec instead.
8. **It gives an honest residual for each invariant and names the one gap.** V2 7.1 gives 26 invariants of five kinds, each with a check command. V2 7.4 states openly: "INV-032 ... **Gap:** no item measures simultaneous load; it stays UNVERIFIED" (DA C-009). V2 7.2 gives a falsifier for each sufficiency claim, including F2's "a definition in a config location the detection does not read". DA 7.2 marks that F2 detection-location falsifier as unique to V2 (C-001).
9. **It records decisions no question covers.** N1 to N4 raise four decisions that no Q1 to Q24 covers: where the INV-008 ruling lives, where `reclaimable` lives before the note, what Q14 means, and the handoff after FU-1 (V2 3; DA U-008). Each is raised and none is answered, which respects the brief's rule that owner decisions are not the spec's to make.

## Weaknesses identified in V1 and V3

**V1**

1. **Safety: it allows the join comparison to run the unfixed sweep before the INV-008 ruling** (V1 XC-04 blocked-by "Q24; LIVE"; criterion (4) "run with the sweep from PR #539's head"; scheduled in W1 before SW-05). Running the sweep runs `git status` in every listed worktree with the inherited environment (E-09). On this host the clean filter runs even with `-c core.fsmonitor=false` (ADJ 2.2 action 1). DA rates this X-002, High, L3. The merge must add TB-1 (or TB-GIT) as a predecessor of the JOIN item.
2. **Factual error on input availability.** V1 says the sub-orchestrator and tech-ref packages "were not found in this checkout ... Their location is UNVERIFIED" (V1 0.4 item 5). Both exist (DA SC-01). A coordinator reading V1 would not read the nearest design for link L1, although the seed says to link it (seed "Enrichment Context").
3. **Its default ledger path sits inside the #539 checkout.** V1 XC-01 sets the ledger location to `.dev/brainstorms/20261113-orchestrator-tui-alignment/decision-ledger.md`, which is under ROOT, the #539 head. V1's own XC risk says "a note committed here joins #539 and breaks A-004" (DA X-012). DA SC-42 shows this brainstorm folder is untracked and not ignored in that checkout.
4. **The guard flip waits on the contract-note draft** (V1 OB-06 blocked-by "XC-05 (for (e))"). ADJ 2.1 action 4 lists six prerequisites, and a contract-note draft is not one of them. Criterion (e) in V1 itself allows "or ... in the observer spec" (DA X-007).
5. **Its Q14 gate check accepts a record that the class is "not yet" restored** (V1 V2-02 (3) "or the entry says it is not yet"). That lets the v2 gate be recorded as checked while the condition ADJ line 699 names ("restores the sweep's `working` class") is not met (DA X-009).
6. **Its guardrail conflicts with the mandated PR tool and the conflict is not stated** (V1 6.9 "Merge a PR, post to an issue or reply on a review thread without the owner's approval" versus V1 6.4 rule 2 `/sc:pr-submit --monitor 3`) (DA X-011). V2 shares this defect (see Concessions). It is listed here because V1's never-do list names "reply on a review thread" explicitly, which is exactly what the tool does.
7. **It has no wave interruption or resume rule.** V1 has no equivalent of V3's "Wave interruption rule" or "Evidence handoff and resume" (DA U-013). A coordinator restarted mid-wave could repost a comment or retry an `unknown` launch.

**V3**

1. **It adds an edge the source does not have, which delays read-only evidence.** V3 SW-05 (shared capture plus join) is blocked by SW-03 (#539 merged) and XC-01. ADJ 4.1 line 414 has `CAP -> {...}` with no #539 predecessor (DA X-003, SC-35). The capture runs no sweep (it uses read verbs on Orca only, ADJ Q24), so holding it to the merge delays the v2 gate data and the note's attention row for no cause. V3 also bundles CAP and JOIN into one item, so the safe capture inherits the JOIN's real need for TB-GIT.
2. **It gates #423 research against the source.** V3 V2-02 (brainstorm and research) is blocked by V2-01, SW-03 and SW-05. ADJ line 710 says research "may be done ahead of the rest" (DA X-008, SC-34).
3. **Its owner-decision gate map adds edges with no source.** Examples: Q11 gates SW-04, XC-03 and XC-07. Q21 gates OB-04 and V2-03. Q9 and Q17 gate XC-03, the contract note (V3 3 table; V3 4 "Decision edges"). ADJ Part 7 says Q11 gates only "#339 D2" (ADJ line 781), and Q17 gates "A-001, D-6" (ADJ line 787) (DA C-010). Each extra DEC edge is a place where an unanswered question blocks work for no cause.
4. **Its schedule does not match its own register** (DA X-015). W1 schedules "XC-03 draft in K", but register XC-03 is blocked by SW-03 and SW-05, and no draft item exists. Section 1 says "SW-04, SW-05 and XC-07 retain follow-ups", but SW-05 is the capture item.
5. **It merges items that need separate evidence.** SW-03 is "Resolve threads and merge #539" as one item. OB-02 holds both the seeded test and the live-layout attempt (DA C-003). V3 itself says the live-layout attempt is recorded "separately" and that seed writes and read capture need separate consent (V3 rule 8). With merged items, one acceptance hides two gates. Its register of 33 items is the smallest (DA S-002, SC-41).
6. **It mixes the ruling and the ledger.** V3 SW-01 (owner rules on INV-008) is blocked by XC-01 (the ledger). An owner can rule before any ledger exists, so this puts a process artifact ahead of the first security action (DA C-001).
7. **It never checks anything itself.** V3 "ran nothing and treats the source's live facts as historical" (DA C-011). That is safe, but it leaves facts that a read could settle cheaply as UNVERIFIED. An example is the existence of the worktrees in its role map, where "real path/branch UNASSIGNED" is used even for the existing `issue-409-mvp` (V3 6 map).
8. **It also has the X-011 conflict, unstated.** V3 says "Explicit authorization for every outward write, merge and live test" (V3 6 inputs) and also requires `/sc:pr-submit --monitor 3` (V3 guardrail 5).
9. **It adds a new polling clock** (V3 polling table "local decision-ledger reconciliation every 5 minutes while session remains active", PLAN INFERENCE; DA X-014). It is local and not an Orca poll, but no source asks for it.

## Concessions (own weaknesses)

1. **X-005 (High): V2 is wrong to demote the cross-issue edit order to SOFT.** ADJ line 442 gives the order "(2) #450; (3) Coder#477; (4) #409 pass; (5) one #339 comment; (6) #423 rewrite", "accepted by all five advocates". The seed restates it as a Known Context fact ("Cross-issue edit order: owner answers, #450, Coder#477, #409, one #339 comment, #423"). V2 relied on ADJ's own sentence "the order is mainly for cross-links" (V2 W7, W8, 4.4). But "mainly" is not "only", and a spec should not override an all-advocate verdict on a reading of one word. The resulting schedule posts SW-10 (#339 comment) in Wave 1, before the #409 pass OB-07 in Wave 2. It also posts CO-02 (Coder#477) before WA-04 (part of #450) (V2 5). The merge should keep V1/V3's hard chain, drawn with V2's PROC kind and ADJ line 442 as evidence.
2. **X-006: V2 is wrong to split #450 into three issue writes** (V2 WA-02, WA-03, WA-04). A-011 asks for "one editor, one ordered edit set per issue" (ADJ 3.6). Each extra write opens another `updatedAt` race window (INV-030). V2 split them because edit 1 needs WA-01 and edit 4 needs Q20. V1 handles both as blocked-by on one item (V1 WA-02: "XC-02; Q2; Q20 (edit 4 only); WA-01"). Take V1's single item and keep V2's per-edit criteria inside it.
3. **X-011 and A-002 (High): V2's never-do list conflicts with its own mandated PR tool.** V2 6.6 says never "Post, edit or comment on any issue or PR without the owner's go-ahead". V2 6.7 hands each PR's wait to `/sc:pr-submit --monitor 3`, which, per project CLAUDE.md, "pushes the fixes without asking, and replies to and resolves the review comments it fixed". V2 did not notice the conflict. Proposed fix (PLAN INFERENCE): the owner's go-ahead to open a given PR with `/sc:pr-submit --monitor 3` is recorded in the ledger and covers that tool's bounded actions on that PR only (push to its own branch, reply to and resolve the threads it fixed). Merges, issue writes, replies on PR #539's Codex thread and anything outside that PR stay owner-gated. Model it as V3's M-APPROVAL node.
4. **A-001: V2 assumes the coordinator can run `/sc:sweep` from the start.** V2 6.7 lists "Sweep: at most once per 5 minutes (WC-16)" as a current clock. The WC-16 `/sc:sweep` duty exists only on #539's head (DA SC-05, SC-06), and after merge it still needs `superclaude install` or `make sync-dev` (V1 7.3 row 2). V1 6.6 is right.
5. **The WC-16 re-arm rule is missing.** `WORKER-CONTRACT.md:288` (read for this round): "It never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it." V2 6.7 says "This session adds no new clock" and does not state the re-arm duty. V1 6.6 and V3 ("re-armed at expiry") both state it.
6. **X-010: V2 uses "Phase 2" in two senses without a marker.** The L1 gate is "SW-12 (Phase 2 of #339) started", SW-12 is `/sc:close` and later, and the same row calls the sub-orchestrator package (#444) the nearest design (V2 1, L1). V1 1.4's contradiction marker should be taken.
7. **X-012 and A-005: V2's ledger location is unsafe if the coordinator runs in the #539 checkout.** V2 XC-01 puts the ledger in "the orchestrator session's checkout ... inside its own package under `.dev/tasks/to-do/` (PI)", "Staged with `.dev/tasks/` per project rule". It never names that checkout, and 6.2 marks the main checkout "Not used by this program". If the coordinator runs here, the always-staged rule would carry the ledger into a #539 commit (A-004). The merge must name the checkout, excluding both the #539 checkout and the main checkout.
8. **A-004: V2 asserts "The worker in `issue-339-orchestrator-mode`" as the #539 author** (V2 6.3). No source records which session owns that checkout. Calling it a worker also makes it subject to WC-13 and coordinator dispatch, which may not be true. It should be UNVERIFIED and a W0 intake item.
9. **X-013: V2 says #541's merge "is not owner-gated by any source"** (V2 5 "What can run today"). That is literally true of ADJ 2.2 action 3, but V2 6.3 also says the owner "approves every outward action (merges, ...)". ADJ 0.4 calls a merged squash commit one of the only irreversible parts. V1's "owner merges" is the safer and internally consistent rule.
10. **X-015: V2's schedule does not match its own text.** "What never waits for #539" lists XC-05, but the wave table places XC-05 in Wave 3, gated on "SW-06 merged". The right placement is Wave 2, once TB-1 is satisfied (SW-02 landed with F1 or F2, or F3 recorded), which is what V2's own Wave 3 note ("or earlier from the #539 checkout once SW-02 is pushed") implies.
11. **C-005: V2's separate owner one-line comment CO-01 on #477 before the CO-02 post is an extra outward write.** No source requires it. V1 folds the Q4 line into the reply (V1 CO-01 (2)), giving one write per issue.
12. **V2 has no interruption and resume rule and no "authority not granted" list.** V3 has both (DA U-012, U-013), and the merge should take them.

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | The contradiction is real for V2 (Concession 4). `/sc:sweep` and its WC-16 duty are absent from `origin/master:WORKER-CONTRACT.md` (SC-06) and present only on #539's head (`:288`, read this round). The merged spec should say: before SW-06 plus an install or `make sync-dev`, the coordinator runs only WC-16's "The sweep." under Liveness supervision, never `/sc:sweep`. After that, it runs both, at most once per 5 minutes. Take V1 6.6 and 7.3 row 2. |
| A-002 | ACCEPT | All three variants contradict themselves (Concession 3). Resolution: the owner's recorded go-ahead to open one PR with `/sc:pr-submit --monitor 3` covers that tool's own push, reply and resolve on that PR only. Merges, issue writes, the INV-008 reply on #539 and any action outside that PR stay owner-gated. A PR URL outside `IronbellyOrg/IronClaude/pull/N` stops the session (V2 6.4 item 1). Model the approval as V3's M-APPROVAL node. |
| A-003 | QUALIFY | No source shows a live 409 session (SC-27 shows only that the worktree exists at `f104ca51a`). The spec should not default to it. Q24's answer must name a reachable session or person, and the W0 exit check must confirm it can run read verbs from a terminal that holds no Run. If it cannot, Q24's default applies (V2 3: "XC-05 and XC-06 not run"). V2's role row "409 session: Per Q24" already makes it answer-dependent. The "ADJ recommends" default in V1 and V3 should become "if Q24 names it and it is confirmed live". |
| A-004 | ACCEPT | V2 wrongly asserts "the worker" (Concession 8). The #539 author is UNVERIFIED. Add a W0 intake item: the owner names the session that owns `ironbelly/issue-339-orchestrator-mode`. Until then SW-02, SW-03 and SW-05 have no actor, and the critical path is held at an owner gate, not silently assumed. |
| A-005 | ACCEPT | SC-42 shows this debate's folder is untracked and not ignored in the #539 checkout. The session git status shows nine untracked `.dev/` and `docs/designs/` paths there. Guardrail for the merge: in the #539 checkout, every commit stages only named files, which must be the SW-02 and SW-03 changes. No program artifact (ledger, records, debate files) is created or kept there. The coordinator's ledger lives in a separate checkout (see "New in the merge" in the last section). |
| A-006 | QUALIFY | The load is real and unsized. But V1 and V2 do order it: Q1 to Q4 first, then by the wave that needs each (V2 3 "Wave" column; V1 3 "Wave needed by"). Each question has a non-outward default, so an unanswered question holds only its own lane (V2 6.5 row 1). What is missing is a statement that owner latency is the schedule. The merged spec should put the per-wave question batch into each wave's gate and say plainly that the critical path is "Q1 answer time" (V2 5 "Critical path"). |
| A-007 | ACCEPT | ADJ's PR state, issue state and `updatedAt` values are historical. V2 marks #541 "as of the adjudicated document" (V2 0.2) and says `origin/master` was not re-fetched (V2 0.4 item 6), but its SW current state reads as current. The merged spec should take V3's rule (V3 0 "historical evidence"; V3 6 "Fresh correct-fork PR evidence ... not only the source's historical head/check state"): every W0 and wave gate re-reads `gh pr view` and `gh issue view --json updatedAt` with `--repo IronbellyOrg/IronClaude` (or `IronbellyOrg/Coder`). |

## Per-point positions

Taxonomy from DA. L3 = state mechanics, L2 = structure, L1 = surface. All 44 debate points are covered: S 6, C 11, X 15, A 7, U 5.

| Point | Level | Preferred | Conf. | One-line evidence |
|---|---|---|---|---|
| S-001 | L1 | V2 | 60 | V2's skeleton plus W1 to W8 keeps disagreement with ADJ visible. Add V3's interface sub-blocks per system and V1 0.6 as a short stance note. |
| S-002 | L2 | MERGE | 70 | Use V2's 50-item register as the base, re-keyed. Collapse WA-02/03/04 into one #450 item (X-006, V1 WA-02). Drop CO-01 as a separate write (C-005). Never reuse an id for different work (DA S-002 collisions). |
| S-003 | L2 | V2 | 80 | Only V2 gives a kind and evidence for each edge (V2 4.2, 70 rows). Add V1 4.3 checks (no cycle, roots, sinks) and V3's M-APPROVAL node. |
| S-004 | L2 | MERGE | 70 | V2 waves 0 to 4 with "can run today / waits / never waits" lists, fixed for X-005 and X-015, plus V3's ten concurrency rules and wave interruption rule. |
| S-005 | L3 | MERGE | 70 | V2's TB-1 to TB-7 (adds TB-3 remote start route, TB-6 relay strings), V1's readable names, and V3's B-EDIT, B-WRITE and M-APPROVAL as authority nodes. |
| S-006 | L1 | V2 | 70 | "Observe:" on every criterion makes acceptance checkable (V2 0.3). Add V3's decision-lifetime and "authority not granted" columns or notes to the owner table. |
| C-001 | L3 | V2 | 80 | Two items (ruling, apply). The most exact regression test (`core.fsmonitor` + `filter.probe.clean` + `.gitattributes`, F1/F2 fail conditions). Matches ADJ 2.2 action 1 "keep the probe experiment as the regression test". V3 blocks the ruling on the ledger. |
| C-002 | L2 | MERGE | 70 | V2's root-cause column plus V3's contract completion rule (producer, consumer, identity, version, authority, retry, interruption, receipt, rollback). Fix V2's L1 gate per X-010. |
| C-003 | L3 | MERGE | 70 | V2's split (OB-03, OB-04 SOFT, OB-05) plus V1's criterion (i) "diff touches `observe/` only" (V1 OB-06). V3 bundles seed and live layout in OB-02, against its own rule 8. |
| C-004 | L2 | V1 | 65 | One #450 item (V1 WA-02), with V2's FU-1 nine-field criteria (V2 WA-05 = V1 WA-04). V2's three-way split is conceded (X-006). |
| C-005 | L2 | V1 | 60 | Fold the Q4 line into the single reply (V1 CO-01 (2)). V2's extra owner comment has no source. Keep V3's read-audit versus "no write" reconciliation in the deferred CO item. |
| C-006 | L2 | V2 | 80 | Research V2-04 is ungated (ADJ line 710). The design is gated on V2-02. The conditional SW-13 follows from W5. |
| C-007 | L2 | MERGE | 65 | V1 and V2 agree: the draft runs early on a master branch, and the note plus test lands after #539 because the test reads `ALLOWED_ORCA` (SC-28). Add V3's full content list and 9-row word mapping table as note content. |
| C-008 | L2 | MERGE | 70 | V1 6.4 and 6.5 guardrails and stops (incl. the WC-16 escalation list), V2 6.2 verified worktree map, V3 role contract (separate capture and seed operators) and evidence-handoff and resume rule. |
| C-009 | L3 | MERGE | 65 | V2 7.1 invariants with a check command each and the explicit INV-032 gap. V1 7.1 coverage by severity incl. LOW rows. V3's INV-001 to INV-044 register incl. addressed rows. |
| C-010 | L2 | V2 | 65 | V2 matches ADJ Part 7 "Gates": Q11 gates "#339 D2" only (ADJ line 781), Q2 gates the #423 and Coder#477 text. V3 adds Q11, Q9 and Q17 edges with no source. |
| C-011 | L1 | V2 | 80 | OBS-NOW checks each name a command, and SC-02, 23, 24, 27, 28 confirm them. V1 has one wrong Glob (SC-01). V3 checked nothing. |
| X-001 | L2 | V2 | 98 | `ls -d` shows both packages exist (SC-01, SC-02). V1 is factually wrong. |
| X-002 | L3 | V2 | 90 | JOIN runs the sweep, and the sweep runs `git status` with inherited env in every listed worktree (E-09, ADJ 2.2 action 1). So TB-1 must precede it. V3 is safe but over-gates via the merge. V1 is unsafe. |
| X-003 | L2 | V2 | 80 | ADJ 4.1 line 414: CAP has no #539 predecessor (SC-35). CAP uses Orca read verbs only (ADJ Q24). V1 is equivalent. V3 adds an unsourced edge. |
| X-004 | L2 | V2 | 70 | ADJ is inconsistent (lines 343 vs 348, 212). V2 flags it as W1 and chooses "now" with a reason. V1 chooses silently. V3 follows A-005 only. The owner should settle it (N-row). |
| X-005 | L3 | V1 | 85 | ADJ line 442: the order is "accepted by all five advocates", and the seed restates it. V2's SOFT demotion is conceded. Keep it hard (PROC kind, with V2's evidence column). V3 is equivalent to V1. |
| X-006 | L3 | V1 | 85 | A-011 "one ordered edit set per issue". Each extra write is another INV-030 race window. V2 is conceded. |
| X-007 | L3 | V2 | 75 | ADJ 2.1 action 4 lists no note predecessor. V2 W2 puts the row in observer text or the draft. V1's blocked-by contradicts its own criterion (e). V3 is equivalent to V2. |
| X-008 | L2 | V2 | 85 | ADJ line 710: research "may be done ahead of the rest" (SC-34). V3 contradicts it. V1 is ambiguous. |
| X-009 | L3 | V2 | 75 | ADJ line 699 "capture that restores the sweep's `working` class is recorded" joins a record with a code change. V2 W5 and the conditional SW-13 make the owner pick. V1 lets "not yet" pass the gate check. |
| X-010 | L2 | V1 | 85 | V1 1.4 marks the two "Phase 2"s. V2 conflates them in its L1 gate (conceded). V3 is silent. |
| X-011 | L3 | NEITHER | 80 | All three forbid what `/sc:pr-submit --monitor 3` does (project CLAUDE.md). The merge needs the bounded carve-out in A-002 (PR-scoped go-ahead recorded in the ledger, plus M-APPROVAL). |
| X-012 | L3 | MERGE | 75 | V3's rule "no sidecar in #539", plus V2's `.dev/tasks/` package, plus an explicit named coordinator checkout that is neither the #539 checkout nor the main checkout. V1's default path is inside the #539 checkout (internal contradiction). |
| X-013 | L2 | V1 | 70 | Merges are outward and the squash commit is irreversible (ADJ 0.4). Owner merges or explicitly approves. V2's "not owner-gated" conflicts with its own 6.3 (conceded). |
| X-014 | L3 | MERGE | 70 | Keep V1/V2's "no new Orca clock". Add V1/V3's WC-16 re-arm on wait expiry (`WORKER-CONTRACT.md:288`). V3's 5-minute local ledger tick is optional PLAN INFERENCE, not required. |
| X-015 | L2 | V2 | 55 | Every variant has schedule-register mismatches. V2's (XC-05 in Wave 3) is one row and fixed by moving it to Wave 2 after TB-1. V3's are structural (a missing draft item, a mislabelled SW-05). V1's are a factual and a path error (X-001, X-012). |
| A-001 | L3 | V1 | 85 | SC-06: no `/sc:sweep` on master. V1 6.6 and 7.3 row 2 state the install step. |
| A-002 | L3 | NEITHER | 80 | Same root as X-011. Resolution in the A-002 response above. |
| A-003 | L2 | MERGE | 70 | No source shows a live 409 session (SC-27). Q24's answer names a session confirmed at W0, or the default applies (V2 3 Q24 default). |
| A-004 | L2 | V1 | 65 | V1 marks the #539 author "UNVERIFIED which session" (V1 5.4). V2's "the worker" is conceded. Add an owner intake item. |
| A-005 | L3 | V3 | 70 | V3 alone states "no extra sidecar is placed in #539". Extend it to all program artifacts with a named-files-only staging rule in the #539 checkout (SC-42). |
| A-006 | L2 | MERGE | 60 | V1/V2 wave columns order the questions. Add the explicit statement that owner latency is the critical path (V2 5 "Critical path"). |
| A-007 | L3 | V3 | 75 | V3 treats source live facts as historical and requires fresh correct-fork reads (V3 0, V3 6 inputs). V2 partly does (0.2, 0.4 item 6). V1 presents them as current. |
| U-004 | L2 | V2 | 80 | The edge-kind taxonomy with evidence is what makes gates auditable. Keep it for the merged graph and also apply it to the hard cross-issue order (PROC). |
| U-005 | L2 | V2 | 75 | W1, W2 and W5 expose real ADJ inconsistencies (SC-36; ADJ 2.1 action 4 (e) vs 2.3; ADJ line 699). W3 and W4 are evidence-backed. W7 and W8 were the source of the X-005 error and should be dropped. |
| U-010 | L3 | V3 | 75 | Producer, consumer, failure, retry and idempotency per interface (V3 2). The orchestrator session needs these to resume without duplicate comments or relaunches. Add as a per-system sub-block. |
| U-011 | L3 | V3 | 80 | XC-08 two-scope independent gate (first release versus end to end) and the contract completion rule. They directly serve seed criterion 12 ("INV-008 first; convergence by invariant coverage"). |
| U-012 | L3 | V3 | 80 | "Authority not granted" (for example "Q24 read capture does not authorize seeded message writes") and "decision lifetime" close gaps that V1 and V2 do not address. |

## What an ideal merged spec would take from each variant

**From V2 (base)**

- 0.1 the INV-008 requirement sentence with two branches. SW-01 and SW-02 as two items, with SW-02's regression test (temp repo, `core.fsmonitor` hook, `filter.probe.clean`, `* filter=probe`) and its F1/F2 fail conditions (V2 2.1).
- The edge-kind taxonomy and the evidence-per-edge table (V2 0.3, 4.2), including TB-1 -> XC-05 (JOIN) and no #539 edge into XC-06 (CAP) (V2 edges 61, 62).
- The "Observe:" acceptance convention and the OBS-NOW verified state rows (V2 0.2, 0.3, 2.x).
- The "root cause of the gap" column in Chain to target (V2 1) and the "after the first release the chain is still broken at L1 and L3" sentence.
- Weak points W1 to W6 and the N1 to N4 uncovered decisions (V2 2.x, 3). Drop W7 and W8, because they caused X-005.
- The 4.4 table of differences from ADJ's graph, with W3 (no SW-06 -> OB-05 edge) and W4 (note plus test waits for #539 because of `ALLOWED_ORCA`, SC-28) kept. Remove the "Demoted to SOFT" row.
- V2-04 research ungated (ADJ line 710). The conditional SW-13 (restore the `working` class) tied to the owner's Q14 wording.
- The verified worktree map with "never remove `issue-409-mvp` until OB-01 and OB-05 merge" (V2 6.2; R-OB3).
- 7.1 invariants with check commands, 7.2 sufficiency falsifiers (incl. the F2 detection-location falsifier), and the explicit INV-032 gap (V2 7.4).
- The "can run today / waits for #539 / never waits for #539" lists and the critical path line (V2 5), corrected for X-005 and X-015.

**From V1**

- The hard cross-issue edit chain `#450 -> Coder#477 -> #409 -> #339 comment -> #423` (V1 4.2, 5.3; ADJ line 442), drawn as PROC edges.
- One #450 edit item (V1 WA-02) and one Coder#477 write that carries the Q4 line (V1 CO-01 (2)).
- 1.4 Phase 2 CONTRADICTION MARKER and keeping SW-12 (`/sc:close` and later) separate from the #444 sub-orchestrator design (V1 SW-13).
- 6.6: no `/sc:sweep` before #539 merges and is installed. 7.3 row 2: the install step after merge.
- 6.4 guardrails 1 to 12 and 6.5 stop table, including the WC-16 escalation list from `WORKER-CONTRACT.md:288`, and "Two sources disagree ... record both with a contradiction marker".
- 6.7 status output (outstanding decisions only) and the 6.8 ledger row format, with UNRESOLVED-fact rows (INV-008, A-009, X-016, D-A, D-B, D-3, D-8, INV-024, authorship, row pruning, R2-V3 D-7).
- 7.1 coverage map by severity, incl. LOW and residual rows. 7.5 extension-slot table (optional appendix).
- OB-06 (i): the flip diff touches `observe/` only. SW-04: the owner merges #541 (all merges owner-gated or explicitly approved).
- Remove V1's errors: 0.4 item 5 (packages exist), the XC-01 path inside the #539 checkout, the OB-06 -> XC-05 edge, and the XC-04 W1 sweep run without TB-GIT.

**From V3**

- Interface contracts with failure, retry and idempotency rules per system (sweep, snapshot, question read, launch, watcher stores, remote read, catalogue, issue edit, PR merge) (V3 2, XC).
- XC-08 independent invariant and coverage gate with first-release and end-to-end scopes, and "INV-008 unresolved means FAIL, never voted away" (V3 XC-08).
- The contract completion rule for each later link (V3 1).
- "Authority not granted by these questions" and "Decision lifetime" (V3 3). M-APPROVAL as the authority node in the graph (V3 4), used to resolve X-011 and A-002 with a PR-scoped go-ahead for `/sc:pr-submit --monitor 3`.
- Concurrency rules 1 to 10, especially rule 8 (separate consent for read capture versus seed writes) and rule 4 (draft never committed on the #539 checkout). The wave interruption rule. Evidence handoff and resume (V3 5, 6).
- Role contract with separate read-capture operator and seed-test operator (V3 6).
- Treat ADJ live facts as historical and require fresh correct-fork reads at each gate (V3 0, 6 inputs) (A-007).
- "No extra sidecar is placed in #539", extended to all program artifacts (A-005).
- The full contract-note content list and 9-row word mapping table (V3 XC) as XC-04 draft content.
- Drop V3's extra edges: CAP after the #539 merge (X-003), research after the merge (X-008), and Q9, Q11 and Q17 gating the note (C-010).

**New in the merge (PLAN INFERENCE, needed by all three)**

- W0 intake items: the owner names the #539 author session (A-004), confirms Q24's live reader (A-003), and names the coordinator's checkout. That checkout is a person-created Orca worktree based on `origin/master`, never `issue-339-orchestrator-mode` (PR #539 head) and never the main checkout. The ledger lives there under `.dev/tasks/` (A-005, X-012).
- In the #539 checkout, commits stage named files only, and only the SW-02 and SW-03 changes.

### Variant 3 Advocate (haiku:backend), source `round1-advocate-V3.md`

# Round 1 Advocate: Variant 3 (haiku:backend)

> Provenance: the advocate agent could not write files (its own instructions forbid report files), so it returned the text in messages and the orchestrating session saved it here verbatim in parts. Parts are marked.

## Position summary

**Preferred base: V3, confidence 90/100.** Its interface, failure, retry, interruption and authority contracts provide the strongest operational foundation. Its independent first-release versus end-to-end acceptance gate prevents aligned roadmaps from being mistaken for a working orchestration chain. [V3 Sections 1, 2, 6, 7; C-002; U-010; U-011.]

V3 is not execution-ready unchanged. Import V2's security acceptance detail and evidence-tagged dependencies, V1's numbering and command-availability corrections, and repair V3's unnecessary capture/research blockers. [C-001; S-003; X-003; X-008; X-010; A-001.]

Citation shorthand: V1, V2 and V3 are the assigned proposal files; ADJ is the adjudicated alignment findings document. Debate identifiers belong to the current `diff-analysis.md`.

## Steelman of Variant 1

V1's strongest argument is that maintainability requires contracts, ownership and extension points before runtime connections. Its contract and trust nodes make later capabilities declare what they consume and which boundary they cross, addressing the independently built components described by ADJ without immediately merging their implementations. [V1 Sections 0.6, 4.1, 7.5; ADJ Parts 1.1, 2.3.]

V1 also explicitly distinguishes the conflicting "Phase 2" namespaces and recognizes that merging the sweep does not automatically install its command for a coordinator. These are operationally useful safeguards. [V1 Sections 1.4, 6.6, 7.3; X-010; A-001.]

## Steelman of Variant 2

V2's strongest argument is that every blocking dependency needs evidence. Its edge taxonomy distinguishes file conflicts, test pins, owner decisions, process constraints and preferences; its weak-point sections expose source tensions rather than presenting derived choices as established facts. [V2 Sections 0.3, 4.2, 4.4; U-004; U-005.]

V2 also correctly gates the join comparison on the executable-Git-config boundary, permits dedicated knowledge research ahead of feature work, and distinguishes recording capture evidence from shipping a restored classification. Its security regression acceptance is more directly checkable than V3's compressed ruling-and-merge path. [V2 SW-02, XC-05, V2-04, Weak point W5; C-001; X-002; X-008; X-009.]

## Strengths claimed

1. **Connections have operational contracts.** V3's completion rule requires producer, consumer, identity, version, authority, retry, interruption, receipt evidence and rollback before later links can be accepted. A launch is therefore not automatically a governed handoff. [V3 Section 1; C-002; U-010.]
2. **Unknown launches remain uncertain.** The watcher contract forbids interpreting an unknown launch result as permission to retry and requires live-session reconciliation before forfeiting at-most-once protection. [V3 watcher "Store interfaces" and "Interruption runbook"; ADJ Part 2.4 action 3.]
3. **Publication follows the adjudicated sequence.** V3 preserves the rollout issue, Coder disposition, observer correction, terminology comment and knowledge rewrite order, as a publication process and not as a functional Coder-to-observer dependency. [V3 XC-02 and Section 5; ADJ Part 4.2; X-005.]
4. Read permission does not authorize diagnostic writes. V3 separates capture and seed-test operators; selecting the capture operator does not authorize messages, binding a live coordinator Run or consuming a test mailbox. [V3 Sections 3, 5 concurrency rule 8, 6 role contract; U-012.]
5. Owner decisions have scope and lifetime. Changed answers invalidate dependent unsent drafts; test-specific consent does not cover future issues; vocabulary agreement does not authorize relay. [V3 Section 3; U-012.]
6. Acceptance has two honest scopes. V3's independent gate distinguishes first-release alignment from end-to-end delivery; question display is not an answer channel, and a sweep is not lifecycle management. [V3 XC-08; Sections 1/7; U-011.]
7. Read auditing is reconciled with no observed-state mutation. The proposed remote contract distinguishes access audit writes from orchestration changes and leaves sink/consistency as design outputs. [V3 Coder Idempotency and operation; ADJ Part 6.3 text A; C-005.]
8. Historical evidence remains historical. V3 does not imply it reran source measurements and requires current external state before execution/resume. [V3 Section 0 and wave interruption rule; C-011; A-007.]

## Weaknesses identified in V1 and V2 (part 1)

1. V1's join timing can exercise the unresolved security hole. XC-04 permits a sweep from the open PR head without an explicit security-boundary predecessor. Adopt V2's boundary gate. [V1 XC-04; V2 XC-05; ADJ Part 2.2 action 1; X-002.]
2. V1's package-absence claim is contradicted by the checked record. Both directories were found; retain existing pointers with unread contents, not a missing-input assertion. [V1 Section 0.4 item 5; diff SC-01/SC-02; X-001.]
3. V1 overcouples the guard flip to the note draft. The required state mapping can be recorded in observer-owned text; a cross-cutting draft establishes no additional read-safety property. [V1 OB-06; V2 W2; ADJ Part 2.1 action 4; X-007.]
4. V2 changes an adjudicated publication process. Its edge taxonomy is valuable, but disjoint sentences do not authorize demoting the accepted cross-issue sequence. Keep a hard process edge, not a functional Coder dependency. [V2 Section 4.4/editor lanes; ADJ Part 4.2; X-005.]
5. V2's split rollout publication adds reconciliation work. Each separate write needs another fresh pin, before-body and readback. Prefer one reviewed edit set after required decisions. [V2 WA-02 to WA-04; V3 WA-02; ADJ A-011; X-006.]
6. Both leave monitored-PR authority inconsistent: the mandatory workflow can push/reply/resolve while blanket rules forbid outward actions without owner approval. Explicit bounded authorization for that specific workflow is needed. V3 shares the defect. [V1 Section 6.9; V2 Sections 6.6-6.7; X-011; A-002.]
7. V2's eligibility list and wave placement disagree on whether the join waits for sweep merge. One eligibility rule must govern the schedule. [V2 Section 5; X-015.]

## Concessions (own weaknesses)

1. V3 is shortest: 33 items versus V1's 46 and V2's 50. It is thinner on separately reviewable security implementation, build capture, cron-enable delivery and per-edge evidence. [S-002; C-001/C-004/C-008.]
2. Separate early read capture from sweep-dependent join work. V3's combined item unnecessarily delays safe reads; running the sweep still needs security/execution gates. [V3 SW-05; ADJ Part 4.1; X-002/X-003.]
3. Dedicated knowledge research must be allowed early, as ADJ explicitly permits. Adopt V2's separate item. [V3 V2-02; V2 V2-04; ADJ Part 6.4; X-008.]
4. Security acceptance is too compressed: require measured regression, allow-list impacts, preservation of other read scopes and applicable caveats. Import V2's criteria, not a fix design. [V3 SW-01/SW-03; V2 SW-02; ADJ Part 2.2.]
5. Remove unrelated decision blockers. Static-chat-report choice should not block note/table; machine-origin label choice should not block unrelated handoff/catalogue design. [V3 decision edges; ADJ Q11/Q21; C-010.]
6. Distinguish recorded capture from shipped working classification using the owner's actual gate interpretation. [V3 SW-05; V2 W5; X-009.]
7. Reconcile register/graph/waves: early draft is scheduled despite blocked register item; a follow-up sentence misidentifies capture. [V3 Sections 1/2/5; X-015.]
8. Add V1's explicit pre/post-merge and installed-command availability gate before coordinator sweep use. [V1 Sections 6.6/7.3; A-001.]
9. Prefer ledger reconciliation on existing wakes over V3's extra housekeeping clock unless justified/authorized. [V3 polling table; V2 Section 6.7; X-014.]
10. Identify an actual non-sweep artifact branch before committing; V3's statement alone does not establish isolation. [V3 ledger; X-012; A-005.]

None of these concessions reopens ADJ Part 1.3 withdrawn findings.

## Shared assumption responses

| Assumption | Response | Reason |
|---|---|---|
| A-001 | REJECT | The new sweep command/revised duty cannot be assumed available at program start. Separate pre-merge supervision from post-merge installed-command use. [V1 Sections 6.6/7.3; diff SC-05/SC-06.] |
| A-002 | QUALIFY | Explicit owner authorization may cover documented actions of one specific monitored PR workflow. Without that bounded scope, the blanket restriction conflicts with the required tool. [X-011; project PR-workflow rule.] |
| A-003 | REJECT | Existing observer worktree proves neither a reachable live session nor an unbound test terminal. Verify actor, access and terminal state before live work. [diff SC-27; ADJ Part 2.1 action 4.] |
| A-004 | REJECT | Sweep branch existence does not identify the author session or establish push authority. Record the actual responsible actor before dispatch. [diff A-004; V1 Section 6.3.] |
| A-005 | REJECT | Artifact isolation is not automatic: debate files are in sweep checkout, and staged task files could join a sweep commit. Verify artifact branch and staged scope. [diff SC-42; X-012.] |
| A-006 | QUALIFY | Decisions are genuine gates, but owner capacity is not established. Ask the next eligible question, retain safe defaults, continue independent lanes. [V3 Section 3 decision runbook; ADJ Part 7.] |
| A-007 | REJECT | Review-time PR/issue state is not current execution evidence. Retain historically and freshly check relevant state before action/resume. [V3 Section 0/interruption rule; ADJ Appendix A.] |

## Per-point positions

Confidence concerns the proposed resolution, not readiness of the unchanged specification. Rows 1 to 22 of 44 (part 3).

| Point | Preferred approach | Confidence | One-line evidence |
|---|---|---:|---|
| S-001 | V3 | 92 | Keep required skeleton and operational interface/failure subsections. [V3 Section 2; U-010.] |
| S-002 | MERGE | 94 | Use V3 compact register, selectively splitting combined items where evidence/timing differ. [X-003/X-008/X-015.] |
| S-003 | MERGE | 96 | Add V2 evidence-tagged edge kinds to V3 register and authority nodes. [V2 Section 4.2; V3 Section 4.] |
| S-004 | MERGE | 94 | Keep V3 interruption rules/scope separation with corrected explicit lane eligibility. [V3 Section 5; V2 Section 5.] |
| S-005 | MERGE | 96 | Retain V3 authority/data/write boundaries and explicit graph-wide fork/worker constraints. [V3 Section 4; V1 Section 4.1.] |
| S-006 | MERGE | 91 | Keep V3 logical roles/decision scope; add V2 observation methods. [V3 Sections 2-3; V2 Section 2.] |
| C-001 | MERGE | 98 | Keep V3 first blocker; import V2 measured regression and scope/pin acceptance. [ADJ Part 2.2; V2 SW-02.] |
| C-002 | V3 | 96 | Contract definition, later delivery and receipt/retry/rollback are explicitly separated. [V3 Section 1.] |
| C-003 | MERGE | 95 | Preserve every guard prerequisite without adding a shared-note-draft blocker. [ADJ Part 2.1 action 4; X-007.] |
| C-004 | V3 | 91 | Prefer one rollout edit set plus launch/store/recovery contracts and separately authorized cron enable. [V3 watcher section.] |
| C-005 | V3 | 92 | Separate disposition, later design/delivery; reconcile auditing with no observed-state mutation. [V3 Coder section.] |
| C-006 | V2 | 98 | Research may run early; design and implementation retain their gates. [V2 V2-04; ADJ Part 6.4.] |
| C-007 | MERGE | 96 | Separate early draft from later note/test/link finalization; retain V3 complete content. [V2 W4; V3 contract-note content.] |
| C-008 | V3 | 94 | Separate operators, actual-path assignment, evidence handoff and resume help safe coordination. [V3 Section 6.] |
| C-009 | MERGE | 96 | Keep V3 scope-sensitive independent gate; add observation methods and explicit unmeasured-load gap. [V3 Section 7; V2 Section 7.4.] |
| C-010 | MERGE | 97 | Use narrow clause-level owner gates; remove unrelated blockers. [ADJ Part 7; V3 decision edges.] |
| C-011 | V3 | 94 | Explicit historical evidence beats implied current remote state. [V3 Section 0; ADJ Appendix A.] |
| X-001 | MERGE | 99 | Keep checked V2/V3 package pointers; drop V1 erroneous absence claim. [diff SC-01/SC-02.] |
| X-002 | V2 | 99 | Explicit security-boundary gating prevents unfixed sweep execution for join. [V2 XC-05/R-XC4.] |
| X-003 | V2 | 97 | Read-only capture need not wait for sweep merge. [ADJ Part 4.1; V2 XC-06.] |
| X-004 | MERGE | 85 | Preserve source timing contradiction; recommend early follow-up logging and post-merge source edits. [V2 W1; ADJ Parts 2.2/3.2.] |
| X-005 | MERGE | 99 | Preserve V1/V3 adjudicated issue sequence as hard process constraint. [ADJ Part 4.2.] |

## Per-point positions (continued, rows 23 to 44, part 4)

| Point | Preferred approach | Confidence | One-line evidence |
|---|---|---:|---|
| X-006 | MERGE | 96 | Prefer V1/V3 one reviewed rollout edit set over several publications. [ADJ A-011; V3 WA-02.] |
| X-007 | MERGE | 96 | Observer-local mapping evidence suffices before note lands. [ADJ Part 2.1 action 4; V2 W2.] |
| X-008 | V2 | 99 | Dedicated research may precede feature gate. [ADJ Part 6.4; V2 V2-04.] |
| X-009 | V2 | 97 | Distinguish capture recorded from classification shipped using actual owner interpretation. [V2 W5.] |
| X-010 | V1 | 97 | Carry numbering conflict explicitly and name capabilities unambiguously. [V1 Section 1.4.] |
| X-011 | NEITHER | 99 | All variants need bounded authorization for monitored PR workflow. [A-002; project rule.] |
| X-012 | V3 | 94 | Avoid default ledger in sweep branch; verify actual separate execution-package location. [V3 decision ledger.] |
| X-013 | V3 | 94 | Require authorized maintainer, not assumed owner-only or automatic authority. [V3 M-APPROVAL/SW-02.] |
| X-014 | V2 | 92 | Use existing wakes rather than another housekeeping timer by default. [V2 Section 6.7.] |
| X-015 | NEITHER | 98 | Register, graph and wave eligibility must agree before execution. [V3 Sections 2/5; V2 Section 5.] |
| A-001 | V1 | 99 | Condition sweep use on merge and actual installed-command availability. [V1 Sections 6.6/7.3.] |
| A-002 | NEITHER | 99 | Specify monitored-workflow authorization instead of assuming compatibility. [X-011.] |
| A-003 | MERGE | 96 | Verify live actor and terminal capability; worktree existence proves neither. [diff A-003.] |
| A-004 | MERGE | 97 | Identify actual sweep author/authorized session before assigning fixes. [diff A-004.] |
| A-005 | MERGE | 98 | Verify separate artifact storage and staged scope before sweep commits. [diff SC-42.] |
| A-006 | V3 | 93 | Ask next eligible owner question and continue independent lanes. [V3 decision runbook.] |
| A-007 | V3 | 98 | Treat remote state as historical until freshly checked before action. [V3 interruption rule.] |
| U-004 | MERGE | 97 | Import V2 evidenced edge taxonomy, not publication-order demotion. [V2 Sections 4.2/4.4.] |
| U-005 | MERGE | 95 | Retain source tensions/settling evidence without unilateral process overrides. [V2 W1-W8.] |
| U-010 | V3 | 98 | Retain interface failure, retry, idempotency and operating contracts. [V3 Section 2.] |
| U-011 | V3 | 98 | Retain independent first-release and end-to-end evaluations. [V3 XC-08; Sections 1/7.] |
| U-012 | V3 | 98 | Retain scoped authority and decision lifetime. [V3 Section 3.] |

Coverage across parts 3 and 4: 44 rows (6 S, 11 C, 15 X, 7 A, 5 promoted U).

## What an ideal merged spec would take from each variant (part 5)

- V3: Operational base, contract-completion rule, interface failure/retry semantics, separate read/test-write roles, scoped decisions, interruption recovery and independent first-release/end-to-end gate. Keep compactness only after repairing combined-item gaps. [V3 Sections 1-3, 5-7.]
- V2: Evidence-tagged edges, explicit security regression acceptance, separate early research, conditional classification restoration, observation methods and labelled source tensions. Exclude publication-order demotion and split rollout publication. [V2 SW-02; V2-04; W1-W8; Sections 4.2/7.]
- V1: Explicit numbering conflict, post-merge command availability, fork/worker boundaries and useful extension ownership. Exclude unsafe join timing and erroneous missing-package claim. [V1 Sections 1.4, 4.1, 6.6, 7.3, 7.5.]
- Required across the merge: Bounded authorization for monitored PR workflow, actual responsible sessions and verified artifact isolation from contested sweep branch. [X-011/X-012; A-002/A-004/A-005.]

Overall preferred base: V3, confidence 90/100. This is base selection, not execution readiness. Merge targeted V2 dependency/security detail and V1 availability/numbering corrections, then independently check dependency and authority consistency.

Limits: no live GitHub/Orca state, source behavior or tests were checked by this advocacy. INV-008 remains unresolved; no execution authority is granted.

## Round 2: Rebuttals

### Variant 1 Rebuttal, source `round2-rebuttal-V1.md`

---
round: 2
role: rebuttal
variant: V1 (opus:architect, variant-1-opus-architect.md)
inputs: round1-advocate-V1.md, round1-advocate-V2.md, round1-advocate-V3.md, diff-analysis.md, ADJ, WORKER-CONTRACT.md
created: 2026-11-13
---

# Round 2 rebuttal: Variant 1 (architect)

## 1. Responses to criticisms of V1

Criticisms are taken from `round1-advocate-V2.md` ("Weaknesses ... V1" items 1 to 7 and its per-point table) and `round1-advocate-V3.md` ("Weaknesses ... part 1" items 1, 2, 3, 6 and its per-point table). Where both raised the same point it is answered once.

| # | Criticism (who) | Response | Basis |
|---|---|---|---|
| 1 | V1 XC-04 lets the join comparison run the unfixed sweep before the INV-008 ruling (V2 item 1, V3 item 1; X-002) | **Conceded, as in Round 1.** JOIN needs a sweep run, and a sweep run executes `git status` in every listed worktree with the inherited environment; the clean filter still runs with `-c core.fsmonitor=false` (ADJ line 206). Fix: TB-GIT -> XC-04; JOIN runs only after SW-02 has landed F1/F2 in the code being run, or Q1 = F3 is recorded. | ADJ line 206; diff X-002 |
| 2 | V1 0.4 item 5 says the two task packages are missing (V2 item 2, V3 item 2; X-001) | **Conceded.** Re-run `ls -d` in Round 1: both exist. | diff SC-01, SC-02 |
| 3 | V1's default ledger path is inside the #539 checkout (V2 item 3; X-012) | **Conceded.** V1's own XC risk says a file committed there joins #539. All three advocates now agree the ledger lives in a separate named checkout, neither the #539 checkout nor the main checkout (V2 "New in the merge"; V3 concession 10). | diff X-012, SC-42 |
| 4 | V1 OB-06 waits on the contract-note draft (V2 item 4, V3 item 3; X-007) | **Conceded.** ADJ 2.1 action 4 (e) (line 192) is "the mapping-table row for `reclaimable` (INV-023)" with no note predecessor, and V1's criterion (e) already allows the observer spec. Fix: drop the hard XC-05 edge; keep (e) disjunctive; add V2's N2. | ADJ line 192 |
| 5 | V1 V2-02 (3) lets the v2 gate be recorded as checked while the `working` class is "not yet" restored (V2 item 5; X-009) | **Partly conceded.** V2-02 is a recording item; V1 does not say that a "not yet" entry keeps V2-03 blocked. That is a wording gap a coordinator could misread. Fix: V2-02 passes only when every part of the gate in the owner's Q14 answer is met; adopt V2's conditional SW-13 for the "class shipped" reading. | V1 2.5 V2-02; ADJ line 784 (Q14) |
| 6 | V1 forbids review-thread replies while mandating `/sc:pr-submit --monitor 3` (V2 item 6, V3 item 6; X-011) | **Conceded.** All three advocates now give one fix: an owner go-ahead recorded per PR covers that tool's push, reply and resolve on that PR only; merges, issue posts and the INV-008 reply on #539's Codex thread stay owner-gated; modelled with V3's M-APPROVAL node. | project CLAUDE.md; diff A-002 |
| 7 | V1 has no wave interruption or resume rule (V2 item 7) | **Partly conceded.** V1 has parts: 6.1 "re-read before acting on a cited fact", 6.5 "`updatedAt` changed: abort; re-read; re-map", 6.5 "never re-run only", 7.4 edge cases 3, 5, 8. It has no single restart rule and nothing forbids reposting a comment or retrying an `unknown` launch on resume. Take V3's "Wave interruption rule" and "Evidence handoff and resume" whole. | V1 6.1, 6.5, 7.4; V3 Sections 5, 6 |
| 8 | V1's hard OB-03 -> OB-04 edge over-sequences; V2 holds it SOFT, "no causal link" (V2 per-point C-003) | **Rejected, with new evidence.** The live-layout attempt reads coordinator questions against a real coordinator Run (ADJ line 465, INV-024). Whether that read consumes is UNRESOLVED (X-016, ADJ line 333), and ADJ's observer "Do not" list says not to treat "0 pending after reads" on the coordinator's own Run as proof of non-consumption (ADJ line 195). Doing the layout attempt first runs an unproven read against a live coordinator's real questions before the seeded test has shown the template keeps every seeded message. The causal link is consumption risk, not file sharing. V3 does not dispute it (V3 per-point C-003: "preserve every guard prerequisite"). | ADJ lines 192, 195, 333, 465 |
| 9 | V1 takes "now" for the #534 table silently against ADJ A-005 (V2 per-point X-004) | **Rejected on substance, conceded on labelling.** ADJ 2.2 action 7 (line 212) gives the #534 table "Waits for: nothing", and action 6 (line 211) says the wording items are "logged in #534 now". Only the Part 3.2 summary row A-005 (line 348) says "#539 merged". V1's timing matches the action list; it should carry V2's W1 note so the inconsistency stays visible. | ADJ lines 211, 212, 348 |
| 10 | V1 6.6 "not on a timer" (my own Round 1 concession 7; X-014) | **Revised: V1 is right.** `WORKER-CONTRACT.md:288` (read this round, #539 head) says the coordinator "never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it", and "Phase 1 adds this duty, not a scheduler". V1 6.6 bullet 1 already states the re-arm. V2 and V3 now agree on no extra clock (V2 per-point X-014; V3 concession 9). My Round 1 lean to V3's 5-minute tick rested only on memory, the lowest tier. Final: V1 6.6, plus ledger reconciliation on each existing wake. | `WORKER-CONTRACT.md:288` |
| 11 | V1 "owner merges #541" is too strict; V3 prefers "authorized maintainer" (V3 per-point X-013) | **Partly conceded.** ADJ 2.2 action 3 (line 208) gives #541 "Decision: none. Waits for: nothing", so no source names the owner personally. But outward writes need the owner (seed constraints; V2 concession 9). Final: the owner merges, or records approval for a named merger (M-APPROVAL); the coordinator never merges on its own authority. | ADJ line 208; V2 concession 9 |

## 2. Updated assessment of V2 and V3

**V2.** Its advocate argued well and conceded honestly, and the concessions matter for base choice. V2 now concedes X-005 (hard cross-issue order), X-006 (one #450 edit set), X-010 (Phase 2 marker), X-011, X-012, X-013, X-015, A-001, A-004, C-005 (no separate CO-01 write) and a missing WC-16 re-arm rule (V2 concessions 1 to 12). Six of those concessions adopt V1's position outright. V2's merge plan then has to collapse WA-02/03/04, drop CO-01, re-harden its editor lane and rewrite its 6.7 cadence (V2 "From V1" list). What remains uniquely V2's is real and should be grafted: the per-edge evidence table (U-004), the INV-008 test detail (C-001), the TB-1 -> JOIN edge (X-002), the unblocked research item (X-008), W5 and SW-13 (X-009), OBS-NOW checks (C-011). These are additions to a register; V1's register needs fewer structural reversals to receive them than V2's needs to receive V1's.

**V3.** Its advocate claims base at 90 but concedes ten items (V3 concessions 1 to 10), including the core of its own decomposition: combined items that need splitting (SW-05 CAP plus JOIN; concession 2), a security path "too compressed" (concession 4), unsourced decision gates (concession 5), register/graph/wave mismatches (concession 7), the missing `/sc:sweep` availability gate (concession 8) and unverified ledger isolation (concession 10). A base whose register, gates and schedule all need repair is not a stronger base than one whose fixes are local. V3's operating contracts (U-010, U-011, U-012, U-013, U-014) are the best material of the three and are additive: they slot into any base as sub-blocks of Sections 2, 3, 5 and 6. V3's 90 confidence is not supported by its own concession list. One process note: V3's Round 1 file says it was saved by the orchestrating session from messages (V3 file line 3); I treat its content as V3's.

**Net.** On the six points that decide whether an orchestrator session can run safely (X-002, X-005, X-006, X-011, C-003, A-001), V1 holds four outright, concedes X-002 and shares X-011 with everyone. V2 holds X-002 and concedes X-005, X-006, A-001. V3 holds X-005, X-006 and concedes A-001 and the CAP/JOIN split behind X-002/X-003.

## 3. New evidence not in Round 1

All read this round; line numbers from the files as they are now.

1. **ADJ 2.1 action 4 (line 192)** lists the flip prerequisites (a) scope sentence, (b) seeded test, (c) live-layout attempt, (d) pass record, (e) `reclaimable` row, (f) "not passed" grep. No contract-note draft is among them (supports conceding X-007). **ADJ line 195** ("Do not ... treat the owner's '0 pending after reads' on the coordinator's own Run as proof of non-consumption (X-016)") supports V1's hard OB-03 -> OB-04 edge (C-003).
2. **ADJ 2.2 actions 6 and 7 (lines 211, 212):** wording items "logged in #534 now"; the #534 table "Waits for: nothing". Only the 3.2 row A-005 (line 348) says "#539 merged". Settles X-004's timing in favour of "now".
3. **ADJ 2.2 action 3 (line 208):** #541 merge "Decision: none. Waits for: nothing". No source names the owner as merger (X-013), so V1's rule is a guardrail choice, not a sourced fact.
4. **ADJ line 101 (reading guide):** "Nothing here is irreversible except a posted comment's notification and a merged PR's squash commit (which a revert PR undoes)". V2's Round 1 citation of this as an irreversibility argument for owner-only merges overstates it; the reason for owner approval is the seed's outward-write guardrail, not irreversibility.
5. **ADJ Part 7 (lines 781, 787):** Q11 gates "#339 D2"; Q17 gates "A-001, D-6". Confirms that V3's Q11 and Q17 edges into the contract note have no source (C-010).
6. **`WORKER-CONTRACT.md:288`:** the coordinator "never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it ... The coordinator keeps that pass scheduled while work remains. Phase 1 adds this duty, not a scheduler." Supports V1 6.6 (re-arm, no new clock) on X-014 and reverses my Round 1 lean to V3.

## 4. Remaining disagreements

| Disagreement | Positions | Single fact or test that settles it |
|---|---|---|
| Base variant | V1 (me, 70), V2 (V2 advocate, 70), V3 (V3 advocate, 90) | Re-key each register with the fixes all three advocates accepted and count rows whose blocked-by or scope changes; the base with fewest changed rows wins |
| C-003: OB-03 -> OB-04 hard or soft | V1 hard; V2 soft; V3 merged item | Orca evidence that `check --all --types question` never marks read on a bound Run with `--wait` listeners (settles X-016); absent that, hard |
| X-013: who merges #541 | V1 owner; V3 authorized maintainer; V2 now owner | One owner statement naming who may merge, recorded in the ledger |
| X-004: #534 table timing | V1 now; V3 after merge; V2 now, flagged | Owner statement whether #534 rows may cite an unmerged PR (V2 W1) |
| X-009: meaning of the v2 gate | V2 conditional SW-13; V1 record; V3 folded into capture | The owner's Q14 answer worded as "capture recorded" or "class shipped" |
| X-014: recurring PR check beyond WC-16 | V1/V2 none beyond re-arm; V3 withdrew its tick | Owner confirms whether the 2026-11-05 polling order (memory) applies to this program |
| A-003: is "the 409 session" live | all: UNVERIFIED | At W0, an Orca read (or the owner) confirming that session exists and holds no Run |
| S-001/S-004 skeleton and waves | V1 W0-W5; V2 0-4 plus Later; V3 W0-W6 | Which schedule places every item after all its hard edges with no X-015 mismatch, checked by a fresh reviewer |

## 5. Final per-point table

All 44 points. Evidence column at most 12 words.

| id | winner | conf. | evidence |
|---|---|---|---|
| S-001 | MERGE | 65 | V1 seed-ordered skeleton; add V2 weak points, V3 interface blocks |
| S-002 | V1 | 60 | Fewest reversals: V2 must collapse WA-02/03/04, drop CO-01 |
| S-003 | V2 | 80 | Only V2 gives kind and evidence per edge (U-004) |
| S-004 | MERGE | 65 | V1 waves and serial table; V3 interruption rule; V2 lists |
| S-005 | MERGE | 75 | V1 TB names, V2 TB-3, V3 M-APPROVAL and B-EDIT |
| S-006 | MERGE | 70 | V1 named worktrees; V2 "Observe:"; V3 decision lifetime |
| C-001 | MERGE | 85 | V1/V2 ruling and apply split; V2 `.gitattributes` test, F2 falsifier |
| C-002 | MERGE | 70 | V1 interim deliverables, V2 root cause, V3 completion rule |
| C-003 | V1 | 75 | Layout read on live Run before seeded test risks consumption (X-016) |
| C-004 | V1 | 75 | One #450 edit set (A-011); V2 conceded |
| C-005 | MERGE | 65 | V1 one reply with Q4 line; V3 audit reconciliation |
| C-006 | V2 | 85 | ADJ line 710: research "may be done ahead" |
| C-007 | MERGE | 70 | V1/V2 test after merge; V3 content list and mapping |
| C-008 | MERGE | 75 | V1 guardrails and stops; V2 map; V3 roles, resume |
| C-009 | MERGE | 70 | V1 severity map; V2 check commands, INV-032 gap; V3 gate |
| C-010 | V1 | 70 | ADJ lines 781, 787: Q11, Q17 do not gate note |
| C-011 | V2 | 80 | V2 OBS-NOW checks correct; V1 Glob wrong (SC-01) |
| X-001 | V2 | 98 | Both packages exist; V1 0.4 item 5 wrong |
| X-002 | V2 | 92 | JOIN runs unfixed `git status`; TB-1 must precede it |
| X-003 | V1 | 85 | ADJ line 414: CAP has no #539 predecessor |
| X-004 | MERGE | 75 | ADJ lines 211-212 "now"; keep V2 W1 flag |
| X-005 | V1 | 88 | ADJ line 442 all-advocate order; V2 conceded |
| X-006 | V1 | 88 | A-011 one edit set per issue; INV-030 no etag |
| X-007 | V2 | 80 | ADJ line 192 lists no note predecessor; V1 conceded |
| X-008 | V2 | 85 | ADJ line 710; V1 ambiguous, V3 conceded |
| X-009 | V2 | 72 | W5 separates record from shipped class; owner Q14 decides |
| X-010 | V1 | 88 | V1 1.4 marker; V2 conceded conflation |
| X-011 | NEITHER | 90 | All conflict with tool; per-PR approval rule plus M-APPROVAL |
| X-012 | MERGE | 82 | V3 "no sidecar in #539" plus named separate checkout |
| X-013 | MERGE | 65 | Owner merges or approves named merger; ADJ line 208 silent |
| X-014 | V1 | 72 | WC-16 `:288`: re-arm waits, "not a scheduler"; V1 6.6 |
| X-015 | NEITHER | 80 | Every variant has register/schedule mismatches; fix all |
| A-001 | V1 | 92 | SC-06: no `/sc:sweep` on master; install step needed |
| A-002 | NEITHER | 90 | Same root as X-011; per-PR scoped authorization |
| A-003 | MERGE | 75 | Confirm Q24 runner live at W0, else default applies |
| A-004 | MERGE | 75 | Owner names #539 author session at W0 |
| A-005 | MERGE | 80 | Debate folder not ignored; named-files-only staging in #539 |
| A-006 | MERGE | 65 | V1 "Wave needed by" plus owner latency as critical path |
| A-007 | V3 | 78 | Treat ADJ live facts historical; re-read at each gate |
| U-004 | V2 | 82 | Edge kinds with evidence; apply PROC to cross-issue order |
| U-005 | V2 | 75 | Keep W1, W2, W4, W5, W6; drop W7, W8 |
| U-010 | V3 | 78 | Failure, retry, idempotency per interface; prevents duplicate writes |
| U-011 | V3 | 82 | Two-scope gate stops first-release PASS read as end-to-end |
| U-012 | V3 | 82 | Authority not granted and decision lifetime bound owner answers |

## 6. Final base preference and minimum fixes

**Preferred base: V1, confidence 70.**

Reason in one line: V1 already holds the adjudicated order, the single edit sets, the consumption-safe flip sequence, the CAP timing and the `/sc:sweep` availability gate; its defects are local fixes, while V2 and V3 each need structural reversals their own advocates conceded.

Minimum fixes the V1 base needs (each is a defect, not a graft of taste):

1. **X-002:** add TB-GIT -> XC-04; JOIN only after SW-02 lands F1/F2 in the code run, or Q1 = F3 recorded.
2. **X-011 / A-002:** replace 6.3/6.9 wording with the per-PR rule: owner go-ahead per PR (ledger row) covers `/sc:pr-submit --monitor 3`'s push, reply and resolve on that PR only; merges, issue posts and the #539 Codex-thread INV-008 reply stay owner-approved; add M-APPROVAL.
3. **X-012 / A-005:** ledger in a named checkout that is neither the #539 checkout nor the main checkout; #539 commits stage named files only; no program artifact created in the #539 checkout.
4. **X-001:** both task packages exist; list them in 6.1 inputs.
5. **X-007:** drop OB-06's hard XC-05 edge; keep (e) disjunctive; add N2.
6. **X-008:** split V2-03 into an unblocked research item and a gated brainstorm item.
7. **X-009:** V2-02 passes only if every part of the owner's Q14 gate is met; add conditional SW-13.
8. **A-003 / A-004 / A-007:** W0 exit names the #539 author session and confirms the Q24 runner (or records the default); ADJ live facts labelled "as of ADJ" and re-read at session start and each gate.
9. **Resume:** add V3's wave interruption rule and evidence-handoff rule to Section 6.
10. **X-015:** fix V1's own mismatches above (X-001, X-012) and re-check every wave row against its hard edges.
11. **C-001:** SW-02's regression test takes V2's detail (`core.fsmonitor` hook, `filter.probe.clean`, `* filter=probe` in `.gitattributes`; F1 fails if either runs, F2 fails if scanned rather than `unscanned`), matching ADJ line 206 "Keep the probe experiment as the regression test".

Grafts recommended but not required for safety: V2's per-edge evidence table (U-004), V2 W1/W5 notes, V3's interface contracts, two-scope gate and authority-not-granted list (U-010, U-011, U-012).

### Variant 2 Rebuttal, source `round2-rebuttal-V2.md`

---
round: 2
role: rebuttal
variant: V2 (opus:analyzer, variant-2-opus-analyzer.md)
inputs: round1-advocate-V1.md, round1-advocate-V2.md, round1-advocate-V3.md, round2-rebuttal-V1.md, diff-analysis.md, ADJ, WORKER-CONTRACT.md
created: 2026-11-13
---

# Round 2 rebuttal: Variant 2 (analyzer)

## 1. Responses to criticisms of V2

The criticisms come from four places:
- `round1-advocate-V1.md`, "Weaknesses ... Variant 2", items 1 to 9, and its per-point table.
- `round1-advocate-V3.md`, "Weaknesses ... part 1", items 4 to 7.
- `round2-rebuttal-V1.md`, sections 1 to 3 and 6.

Where two advocates raised the same point, it is answered once.

| # | Criticism (who) | Response | Basis |
|---|---|---|---|
| 1 | V2 demotes the adjudicated cross-issue edit order to SOFT (V1 item 1, V3 item 4; X-005) | **Conceded, as in Round 1 (concession 1).** ADJ line 442 says the order was "accepted by all five advocates". V2's own PROC edge kind is the right way to draw it. Fix: hard PROC edges #450 set -> CO-02 -> OB-07 -> SW-10 -> V2-01, with ADJ line 442 as evidence. Edge rows 47 and 50 change from SOFT to PROC, and the "Demoted to SOFT" row leaves 4.4. Weak points W7 and W8 are withdrawn. | ADJ line 442; DA X-005 |
| 2 | V2 splits #450 into three writes (V1 item 2, V3 item 5; X-006) | **Conceded.** A-011 (ADJ line 391) requires "one editor, one ordered edit set per issue". Fix: one #450 item, blocked by Q2, WA-01 (for edit 1's wording) and Q20 (for edit 4), as V1 WA-02 does. The runbook text in a repo file (V2 WA-03 (1), (2)) stays a separate PR item, because it is a file change, not an issue write. | ADJ line 391; INV-030 |
| 3 | The live-layout attempt OB-04 is only SOFT after the seeded test OB-03, "no causal link" (V1 item 3, V1 rebuttal #8; C-003) | **Conceded (new this round).** Edge 19's "no causal link" was wrong. OB-04 reads coordinator questions against a real coordinator Run (ADJ line 465, INV-024). Whether that read consumes is "unproven both ways" (ADJ line 333, X-016). ADJ line 195 forbids treating "0 pending after reads" on the coordinator's own Run as proof. Orca's help text saying `--all` "does not mark read" (ADJ line 144, E-18) does not settle it either. The causal link is the risk of consuming real questions, not a shared file. Fix: edge 19 becomes GATE with this evidence. | ADJ lines 144, 195, 333, 465 |
| 4 | V2 cites WC-16's `/sc:sweep` as current cadence (V1 item 4; A-001) | **Conceded (Round 1 concession 4).** Fix: V2 6.7 adopts V1 6.6 bullet 2. Before SW-06 plus an install or `make sync-dev`, the coordinator runs only WC-16's "The sweep." under Liveness supervision. | DA SC-05, SC-06 |
| 5 | V2 uses "Phase 2" in two senses with no marker (V1 item 5; X-010) | **Conceded.** Fix: take V1 1.4's contradiction marker. Rewrite the L1 gate as "SW-12 (research-report Phases 2 to 5) started" and keep the #444 sub-orchestrator design as a named design input of WA-09, not as SW-12. | V1 1.4; ADJ Part 6.4 |
| 6 | The ledger checkout is unnamed and the #539 author is asserted as "the worker" (V1 item 6; X-012, A-004, A-005) | **Conceded.** Fix: a W0 intake item. The owner names the #539 author session. The coordinator runs in a named checkout that is neither `issue-339-orchestrator-mode` nor the main checkout, and the ledger lives there under `.dev/tasks/`. In the #539 checkout, commits stage named files only. | DA SC-42, X-012 |
| 7 | V2 is inconsistent on who merges #541 (V1 item 7; X-013) | **Conceded on the rule, and one Round 1 argument is withdrawn.** In Round 1, V2 called a merged squash commit irreversible, citing ADJ 0.4. ADJ line 101 says it is irreversible only "except ... a merged PR's squash commit (which a revert PR undoes)", so the argument overstated the source. V1's rebuttal (section 3 item 4) is right on this. The owner gate rests on the seed's outward-write constraint and V2's own 6.3 role row. Fix: the owner merges, or records approval for a named merger (M-APPROVAL). | ADJ lines 101, 208 |
| 8 | V2's "never waits for #539" list contradicts the wave table on XC-05 (V1 item 8, V3 item 7; X-015) | **Conceded.** Fix: XC-05 (JOIN) moves into Wave 2. It starts when TB-1 is satisfied (SW-02 landed with F1 or F2 in the code the run uses, or Q1 = F3 recorded). It does not wait for SW-06. This is what V2's own Wave 3 note implies. | V2 4.2 edge 61; V2 5 |
| 9 | V2 forbids what `/sc:pr-submit --monitor 3` does (V1 item 9, V3 item 6; X-011, A-002) | **Conceded and shared by all three.** All three advocates now give the same fix. The owner's go-ahead is recorded per PR and covers that tool's push, reply and resolve on that PR only. Merges, issue writes and the INV-008 reply on #539's Codex thread stay owner-gated. It is modelled with V3's M-APPROVAL node. | project CLAUDE.md; DA A-002 |
| 10 | V1's register needs fewer structural reversals than V2's (V1 rebuttal sections 2 and 6; S-002) | **Partly rejected.** On register rows alone, V1 is right: by my count the agreed fixes change about 13 V2 rows and about 8 V1 rows (count in section 3 item 5). But all three advocates also want V2's per-edge evidence table in the merged spec (V1 R2 per-point S-003 "V2 80"; V3 R1 S-003 "MERGE 96, add V2 evidence-tagged edge kinds"). On a V1 base that table must be re-keyed across colliding ids. The same id names different work in the two variants: XC-03 is CAP in V1 and the #541 merge in V2; XC-04 is JOIN in V1 and the note draft in V2; SW-13 is the #444 design in V1 and the `working`-class item in V2; SW-05 is refresh plus merge in V1 and refresh only in V2. DA S-002 rates this "Medium (a merge must re-key ids; same id means different work)". Re-keying 70 cited edges across colliding ids is the merge step most likely to put a wrong edge into a spec that drives an orchestrator. Fixing about 13 rows in place does not carry that risk. | DA S-002; V1 2.6 XC-03, XC-04; V2 2.6 XC-03, XC-04; V1 SW-13; V2 SW-13 |
| 11 | V1 says the #534 table timing should be V1's, flagged (V1 rebuttal #9; X-004) | **Agreed. This supports V2's W1, not V1's silence.** V1's own new evidence (ADJ line 211, "logged in #534 now"; line 212, "Waits for: nothing") is what W1 cited, against the 3.2 row at line 348. Both variants schedule it now. Only V2 records the inconsistency, which V1 now also adopts. | ADJ lines 211, 212, 348 |
| 12 | V2's research item and W5 are fine but should be grafts, not base (V1 rebuttal section 2) | **Rejected as a reason to choose base.** V1's rebuttal (section 6, fixes 6, 7 and 11) itself lists three V2 items as *required* fixes to V1, not optional grafts: research split, the Q14 condition with SW-13, and the INV-008 test detail. Required fixes in one direction count the same as required fixes in the other. | V1 rebuttal section 6 |

**One further self-correction (not raised by others).** V2 edge 29 ("Q2 -> OB-07") makes the whole #409 pass wait for Q2. ADJ 4.2 step 3 gates the #409 pass on "Q8; Q16 for decision 6; REC" only (ADJ line 434). ADJ Part 7 lists the #409 text nowhere among Q2's gates (ADJ line 772). The edge should be narrowed: only the decision 9 and diagram rows wait for Q2, and they are written last before the banner in any case. The same shape is used for Q16 and decision 6 (ADJ line 442).

## 2. Updated assessment of V1 and V3

**V1.** The V1 advocate's concessions are honest and local: X-001, X-002, X-007, X-011, X-012, part of X-009, and resume (V1 rebuttal section 1, rows 1 to 7). I now accept two V1 positions I opposed in Round 1:
- **C-003:** the OB-03 -> OB-04 edge is hard (see section 1 row 3).
- **X-014:** "no new clock plus re-arm" is already in V1 6.6 bullet 1. `WORKER-CONTRACT.md:288`, read again for this round, says "When a wait on Orca expires, the coordinator re-arms it" and "Phase 1 adds this duty, not a scheduler".

That leaves V1 holding the L3 process points X-005, X-006 and C-003, plus A-001 and X-010. V1 still carries the one High safety-ordering defect of Round 1 (X-002). The fix is a single edge, but V1 only gained it by adopting V2's TB-1 reasoning.

V1's base argument rests on counting register rows. It leaves out the cost of the graft everyone wants (section 1 row 10). V1's minimum-fix list includes three items that are V2 content moved into V1 (fixes 6, 7, 11). So on a V1 base, the merged spec's security test, research timing and Q14 gate would be V2's text under V1's ids.

**V3.** The V3 advocate's 90 confidence does not survive its own ten concessions. Those include splitting its combined CAP and JOIN item, an INV-008 path it calls "too compressed", unsourced decision gates, and register, graph and wave mismatches (V3 R1 concessions 2, 4, 5, 7). The V1 rebuttal makes the same point (section 2). V3's per-point table also scores itself above 90 on points where its own text holds the conceded position. For example, C-004 is "V3 91" although V3's capture/handoff decomposition is conceded in its concession 2.

V3's operating material is still the best of the three and is purely additive: U-010, U-011, U-012, the interruption rule and evidence handoff, and the separate read-capture and seed-test operators. It fits as sub-blocks into any base. The V3 advocate also backs V2 on X-014 ("Use existing wakes rather than another housekeeping timer"; V3 R1 X-014 "V2 92"). Its file was saved by the orchestrating session from messages (V3 R1 line 3); I treat its content as V3's.

**Where the three now agree.** On the six safety-deciding points, all three advocates now agree on the substance:
- X-002: TB-1 before JOIN.
- X-005: hard order.
- X-006: one #450 set.
- X-011: per-PR approval plus M-APPROVAL.
- C-003: OB-03 before OB-04.
- A-001: no `/sc:sweep` before merge and install.

The remaining dispute is mostly which document carries that agreed content with the least rework.

## 3. New evidence not in Round 1

Every item below was read this round, with line numbers from the files as they are now.

1. **ADJ line 101:** "Nothing here is irreversible except a posted comment's notification and a merged PR's squash commit (which a revert PR undoes)." This corrects V2's Round 1 irreversibility argument for owner-only merges (section 1 row 7).
2. **ADJ line 465 (INV-024 row):** "record one live attempt in the real coordinator layout before the flip PR". **ADJ line 333 (X-016):** "UNPROVEN BOTH WAYS whether `check --all --types question` consumes on a live coordinator Run". **ADJ line 144 (E-18):** Orca's help says `--all` "does not mark read", and "the owner's measurement on the coordinator's own Run is non-diagnostic". Together these show that the live-layout attempt runs an unproven read against a live Run. That is why the edge from the seeded test is hard (C-003, conceded).
3. **ADJ line 434 (4.2 step 3)** gates the #409 pass on "Q8; Q16 for decision 6; REC". **ADJ line 772 (Q2 "Gates")** says "the #450 edits, FU-1, X-001, INV-011, INV-012, the #423 and Coder#477 text", which does not include #409. Together they narrow V2 edge 29 (section 1, self-correction) and support V1 on C-010.
4. **`WORKER-CONTRACT.md:288`** contains three duties: "never stops watching on its own"; "When a wait on Orca expires, the coordinator re-arms it"; "Phase 1 adds this duty, not a scheduler". These settle X-014 as "no new clock plus re-arm". V1 6.6 has both parts. V2 6.7 has the first part only.
5. **Id collisions, read from the variant tables:**
   - V1 XC-03 = "Shared read-only Orca capture (CAP)"; V2 XC-03 = "Merge PR #541".
   - V1 XC-04 = "One real-id join comparison (JOIN)"; V2 XC-04 = "Draft the contract note".
   - V1 SW-13 = "sub-orchestrator design (#444)"; V2 SW-13 = "Restore the sweep's `working` class".
   - V1 SW-05 = "Refresh #539's merge ref and merge"; V2 SW-05 = "Refresh ..." and SW-06 = "Merge PR #539".
   
   This is the concrete basis of DA S-002's re-key warning and of section 1 row 10.
6. **Row-change counts after the fixes all three advocates accepted** (my count from the variant tables, PLAN INFERENCE; open to a fresh reviewer per section 4):
   - **V2, about 13 rows:** WA-02, WA-03, WA-04 collapse; CO-01 and CO-02 merge; SW-10, OB-07, CO-02 and V2-01 get PROC edges; OB-04's edge changes; XC-03 merge authority; XC-01 location; the L1 gate row; the #539 author role row. Edge-table rows 19, 29, 47 and 50 also change.
   - **V1, about 8 rows:** XC-04 (TB-GIT), OB-06 (drop XC-05), V2-03 split plus one new research row, V2-02 condition, a new conditional `working`-class row (needs a fresh id, because V1 SW-13 is taken), XC-01 location, and the W0 intake rows.
   - **The graft:** on top of those 8 rows, V1 needs 70 evidence-cited edges re-keyed and "Observe:" added to 46 rows.

## 4. Remaining disagreements

| Disagreement | Positions | Single fact or test that settles it |
|---|---|---|
| Base variant | V2 (me, 60); V1 (V1 advocate, 70); V3 (V3 advocate, 90) | A fresh reviewer applies the agreed fixes **and** the agreed grafts (per-edge evidence table, "Observe:" criteria) to each candidate base, then counts changed register rows plus changed graph edges. The fewest total changes wins. |
| X-004: #534 table timing | V1 and V2 now; V3 after merge | An owner statement on whether a #534 row may cite an unmerged PR (V2 W1) |
| X-009: meaning of the v2 gate | V2 conditional SW-13; V1 now adopts it as a fix; V3 conceded | The owner's Q14 answer worded as "capture recorded" or "`working` class shipped" |
| X-013: who merges #541 | V1 and V2: the owner, or a named merger the owner approved; V3: authorized maintainer | One owner statement in the ledger naming who may merge |
| A-003: is "the 409 session" live | All: UNVERIFIED | At W0, the owner or an Orca read confirms the session exists and holds no Run |
| A-004: who is the #539 author | All: UNVERIFIED; V2's "worker" withdrawn | The owner names the session that owns `ironbelly/issue-339-orchestrator-mode` |
| C-003 residual: could OB-04 ever run before OB-03 | All now: no | Orca evidence that `check --all --types question` never marks read on a bound Run with `--wait` listeners (settles X-016) |
| S-004: whose waves | V1 W0 to W5; V2 0 to 4 plus Later; V3 W0 to W6 | A fresh reviewer checks that every item sits after all its hard edges, with no X-015 mismatch, in each corrected schedule |

## 5. Final per-point table

All 44 points are covered: S 6, C 11, X 15, A 7, U 5. Evidence is at most 12 words.

| id | winner | conf. | evidence |
|---|---|---|---|
| S-001 | MERGE | 60 | V2 weak points, V1 seed order and marker, V3 interface blocks |
| S-002 | MERGE | 60 | Keep V2 ids; collapse WA-02/03/04 and CO-01; avoid re-key collisions |
| S-003 | V2 | 85 | Only V2 gives kind and evidence per edge (U-004) |
| S-004 | MERGE | 70 | V2 lists, V1 serial table, V3 interruption rule; fix X-015 |
| S-005 | MERGE | 75 | V2 TB-3, TB-6; V1 names; V3 M-APPROVAL, B-EDIT, B-WRITE |
| S-006 | MERGE | 70 | V2 "Observe:"; V1 named worktrees; V3 decision lifetime |
| C-001 | V2 | 80 | Ruling plus apply; `.gitattributes` test; F2 `unscanned` falsifier |
| C-002 | MERGE | 70 | V2 root cause, V1 interim deliverables, V3 completion rule |
| C-003 | V1 | 82 | Live-layout read on real Run before seeded test (ADJ 333, 465) |
| C-004 | V1 | 78 | One #450 edit set (ADJ line 391); V2 conceded |
| C-005 | MERGE | 65 | V1 one reply carrying Q4 line; V3 audit reconciliation |
| C-006 | V2 | 88 | ADJ line 710: research "may be done ahead of the rest" |
| C-007 | MERGE | 70 | Draft early, test after merge (SC-28); V3 mapping content |
| C-008 | MERGE | 75 | V1 guardrails and stops; V2 verified map; V3 roles, resume |
| C-009 | MERGE | 70 | V2 check commands, INV-032 gap; V1 severity map; V3 gate |
| C-010 | V1 | 65 | ADJ 434, 772, 781: no Q2, Q11 gate on #409/note |
| C-011 | V2 | 82 | OBS-NOW checks confirmed by SC-02, 23, 24, 27, 28 |
| X-001 | V2 | 98 | Both packages exist (SC-01, SC-02); V1 conceded |
| X-002 | V2 | 92 | JOIN runs unfixed `git status`; TB-1 must precede it |
| X-003 | MERGE | 85 | V1 and V2 agree: ADJ line 414, no #539 predecessor |
| X-004 | MERGE | 75 | ADJ lines 211-212 "now"; keep V2 W1 flag on line 348 |
| X-005 | V1 | 90 | ADJ line 442 all-advocate order; V2 conceded |
| X-006 | V1 | 88 | A-011 one edit set per issue; INV-030 no etag |
| X-007 | V2 | 82 | ADJ line 192 lists no note predecessor; V1 conceded |
| X-008 | V2 | 88 | ADJ line 710; V1 and V3 conceded |
| X-009 | V2 | 75 | W5 separates record from shipped class; Q14 wording decides |
| X-010 | V1 | 88 | V1 1.4 marker; V2 conceded conflation |
| X-011 | NEITHER | 90 | All conflict with tool; per-PR approval plus M-APPROVAL |
| X-012 | MERGE | 82 | V3 "no sidecar in #539" plus named separate coordinator checkout |
| X-013 | MERGE | 70 | Owner merges or approves named merger; ADJ 101, 208 |
| X-014 | MERGE | 78 | WC-16 `:288`: no scheduler, re-arm waits; V1 6.6 has both |
| X-015 | NEITHER | 80 | Every variant has schedule-register mismatches; fix each |
| A-001 | V1 | 92 | SC-06: no `/sc:sweep` on master; install step needed |
| A-002 | NEITHER | 90 | Same root as X-011; per-PR scoped authorization |
| A-003 | MERGE | 75 | Confirm Q24 runner live at W0, else Q24 default |
| A-004 | MERGE | 75 | Owner names #539 author session at W0; "worker" withdrawn |
| A-005 | MERGE | 80 | Debate folder not ignored (SC-42); named-files-only staging |
| A-006 | MERGE | 65 | Per-wave question batches; owner latency is the critical path |
| A-007 | V3 | 78 | ADJ live facts historical; re-read at W0 and each gate |
| U-004 | V2 | 85 | Edge kinds with evidence; PROC for the cross-issue order |
| U-005 | V2 | 75 | Keep W1 to W6; withdraw W7, W8 (X-005) |
| U-010 | V3 | 78 | Failure, retry, idempotency per interface; prevents duplicate writes |
| U-011 | V3 | 82 | Two-scope gate stops first-release PASS read as end-to-end |
| U-012 | V3 | 82 | Authority not granted and decision lifetime bound owner answers |

## 6. Final base preference and minimum fixes

**Preferred base: V2, confidence 60.** This is down from 70 in Round 1, because of the C-003 and C-010 concessions and the honest row count in section 3 item 6.

Reason, in one line: every advocate wants V2's 70-edge evidence table, "Observe:" criteria, INV-008 test detail, research split and Q14 condition in the merged spec. Fixing about 13 rows in place in V2 is less error-prone than re-keying all of that onto V1 across colliding ids (DA S-002). If a fresh reviewer's count (section 4, row 1) comes out against V2, V1 is the right base and I would accept it.

Minimum fixes the V2 base needs (each is a defect):

1. **X-005:** hard PROC chain: #450 set -> CO-02 -> OB-07 -> SW-10 -> V2-01 (ADJ line 442). Rewire the editor lane in waves 1 and 2. Withdraw W7 and W8 and the "Demoted to SOFT" row in 4.4.
2. **X-006:** one #450 item (blocked by Q2, WA-01, Q20). The runbook file change stays its own PR item.
3. **C-003:** edge 19 becomes GATE (OB-03 before OB-04), with ADJ lines 144, 195, 333 and 465 as evidence.
4. **X-011 / A-002:** a per-PR owner go-ahead in the ledger covers `/sc:pr-submit --monitor 3`'s push, reply and resolve on that PR only. Merges, issue writes and the #539 Codex-thread ruling reply stay owner-gated. Add the M-APPROVAL node.
5. **X-012 / A-005 / A-004:** a W0 intake item covers three things. The owner names the #539 author session. The coordinator works in a named checkout that is neither the #539 checkout nor the main checkout, and the ledger lives there under `.dev/tasks/`. In the #539 checkout, commits stage named files only.
6. **A-001 and WC-16:** 6.7 says there is no `/sc:sweep` before SW-06 plus an install or `make sync-dev`. Add the re-arm-on-expiry duty from `WORKER-CONTRACT.md:288`. Add no new clock.
7. **X-010:** add V1 1.4's Phase 2 contradiction marker. The L1 gate names the "research-report Phases 2 to 5" (SW-12) and the #444 design separately.
8. **X-013:** the owner merges, or records approval for a named merger. Delete "not owner-gated by any source" from section 5.
9. **X-015:** XC-05 (JOIN) moves to Wave 2, after TB-1 is satisfied.
10. **C-005:** fold CO-01's Q4 line into the single Coder#477 reply.
11. **C-010:** narrow edge 29. Only the #409 decision 9 and diagram rows wait for Q2 (ADJ lines 434, 772).
12. **A-003 / A-007:** the W0 exit confirms the Q24 runner is live, or records the Q24 default. Every ADJ live fact is labelled "as of ADJ" and re-read at W0 and at each gate.
13. **Resume:** add V3's wave interruption rule and evidence-handoff rule to section 6.

Grafts recommended but not required for safety:
- V3's U-010 interface contracts, U-011 two-scope gate, U-012 authority-not-granted list and decision lifetime, and the operator split.
- V1's 6.5 golden-test stop and WC-16 escalation list, its 6.8 ledger row format, its 7.1 severity map and its 7.5 extension slots.

### Variant 3 Rebuttal, source `round2-rebuttal-V3.md`

# Round 2 Rebuttal: Variant 3 advocate (haiku:backend)

> Provenance: the advocate agent cannot write files; it sent three message parts and the orchestrating session saved them here.

## 1. Responses to criticisms of V3

1. CAP/JOIN bundling (X-003): CONCEDE. Split safe read capture from sweep-dependent comparison. CAP can run before merge; JOIN waits for the security ruling to be satisfied in the actual code run or recorded risk acceptance. [V3 SW-05; V1/V2 R2; X-002/X-003.]
2. Research gate (X-008): CONCEDE. Dedicated research runs early; feature brainstorm/design and implementation retain separate gates. [V3 V2-02; ADJ Part 6.4.]
3. Excess decision gates (C-010): CONCEDE. Q11 concerns chat reporting, not note/table delivery; Q21 concerns labelling, not generic handoff/catalogue work. Use clause-level dependencies. [ADJ Part 7 Q2/Q11/Q21; V2 R2.]
4. Ledger before ruling and compressed fix (C-001): CONCEDE. An owner ruling must not await ledger creation. Record it afterward; separate ruling, implementation and merge evidence. Import V2's measured regression and scope/pin acceptance. [V3 SW-01/SW-03; ADJ Part 2.2 action 1.]
5. Register/wave mismatch (X-015): CONCEDE. Draft and finalization need distinct eligible states/items; repair the misnamed follow-up reference and validate all schedule edges. [V3 W1 versus XC-03.]
6. Seed/live-layout ordering (C-003): CONCEDE ambiguity; adopt V1's explicit hard seed-before-live edge. A seeded pass remains necessary, not sufficient: live consumption stays unresolved. [V3 OB-02; ADJ Part 2.1 action 4.]
7. Logical worktree roles (S-006): QUALIFY. V3 identifies the existing observer sibling as evidence-only; UNASSIGNED describes future change checkouts. Still add an intake map so this prerequisite is explicit and checkable. [V3 Section 6.]
8. No independent checks (C-011): CONCEDE the narrower evidence floor. Historical labelling cannot replace cheap current read-only checks before execution. Combine V2's verified map with V3's freshness rule. [V3 Section 0; V2 OBS-NOW; A-007.]
9. PR-tool authority (X-011/A-002): CONCEDE. Record owner authorization for one specific monitored PR workflow and its bounded branch/review-thread actions. That authorizes neither merge nor unrelated issue/security-ruling posts. [Project rule; V1/V2 R2; V3 M-APPROVAL.]
10. New ledger tick (X-014): CONCEDE. Reconcile on existing wakes; re-arm waits. Do not invent another scheduler. [WORKER-CONTRACT WC-16.]
11. Follow-up timing (X-004): CONCEDE. ADJ action list says log now and waits for nothing; prefer early authorized logging, preserving W1's contradictory summary-row note. Source edits remain post-merge. [ADJ Part 2.2 actions 6-7.]
12. Base confidence: CONCEDE 90 was too strong. My FINAL base changes to V1, 75/100, with mandatory V2 and V3 corrections. No variant is executable unchanged.

## 2. Updated assessment of V1 and V2

V1: its hard publication order, one rollout edit set, explicit seed-before-live sequence, sweep availability gate and numbering marker already match the now-agreed operational ordering. Its R2 accepts JOIN safety, early research, narrower note dependency and resume repairs. A defensible mechanical base. Do not treat its proposed changed-row metric as an observed independent comparison. [V1 R2 Sections 1/4/6.]
V2: its evidenced edges, regression criteria, early research and capture-versus-shipped-class distinction remain essential. Its R2 repairs hard order, single publication, seed-before-live, cadence and clause gating. Its cited re-key collisions are real; its approximate edit counts are its own inference, not a measured result. [V2 R2 Sections 1/3/6.]
V3's contracts, scoped authority and two-scope independent gate prevent duplicate actions and false completion after interruption. Carry them as required acceptance controls whichever base wins. [V3 Sections 1/3/5/6; U-010/U-011/U-012.]

## 3. New evidence not in Round 1

WC-16 explicitly requires re-arming expired waits and says Phase 1 adds a duty, not a scheduler. This supports no extra housekeeping clock, not abandonment of supervision. [src/superclaude/core/WORKER-CONTRACT.md, WC-16.]
ADJ Part 2.2 actions 6-7 support early follow-up logging; Part 7 Q11/Q21 narrow the disputed gates. These sharpen earlier positions; they are not new live Orca/GitHub measurements.

## 4. Remaining disagreements (part 2)

| Disagreement | Final position | Single settling fact or test |
|---|---|---|
| Mechanical base and re-key risk | V1 preferred; V2 evidence table mandatory | Fresh reviewer validates corrected register-edge identities and schedule with no dangling/misbound references. Row-count estimates alone do not settle correctness. |
| Q14 knowledge start gate | Explicit conditional restoration item | Owner states whether gate requires capture recorded or working classification shipped. |
| Authority for PR workflow and merges | Bounded PR authorization; merge separately authorized | Owner records scope for that specific PR workflow and names permitted merger. |
| Capture runner and sweep author | Actual actors, not inferred live sessions | Owner/authoritative session evidence identifies each reachable actor and role at intake. |
| Live question-read semantics | Seed-before-live hard; no universal safety claim | Authorized evidence covering bound-Run waiter/ack/replay behavior on the pinned build. |
| Artifact isolation | Named authorized non-sweep storage and path-scoped commits | Independent read of actual artifact location and staged diff proves no alignment-file additions to contested PR. |
| Follow-up table timing | Early authorized logging; source edits later | ADJ action-list evidence supports now; contrary owner instruction would supersede proposed timing. |

No substantive disagreement remains on hard publication order, one rollout issue write-set, JOIN security gating, early dedicated research, or merge/install before the new sweep duty. The unresolved executable-Git-config finding itself remains unresolved, not a debate vote.

## 5. FINAL per-point table (rows 1-22 of 44)

| id | winner | confidence | evidence |
|---|---|---:|---|
| S-001 | MERGE | 80 | V1 seed order; V2 tensions; V3 operational contracts. |
| S-002 | V1 | 75 | Explicit stages avoid V3 bundling; reconcile V2 identity collisions. |
| S-003 | V2 | 94 | Evidence-tagged edges make constraints auditable; retain hard process order. |
| S-004 | MERGE | 88 | V1 sequencing; V2 eligibility; V3 interruption recovery; validate together. |
| S-005 | MERGE | 94 | V1 fork/worker boundaries; V3 authority; V2 remote-start boundary. |
| S-006 | MERGE | 88 | V2 observation methods; actual-path intake; V3 decision lifetime. |
| C-001 | V2 | 96 | Separate ruling/apply; measured regression, scope separation, refusal falsifier. |
| C-002 | MERGE | 92 | V3 completion contract plus V1 interim and V2 gap columns. |
| C-003 | V1 | 96 | Seed precedes live-layout read; diagnostic pass remains insufficient alone. |
| C-004 | V1 | 90 | One rollout set and explicit separate cron-enable item. |
| C-005 | MERGE | 90 | One disposition reply; V3 audit/no-observed-mutation reconciliation. |
| C-006 | V2 | 98 | Dedicated research expressly allowed early; design remains gated. |
| C-007 | MERGE | 94 | Early draft; post-merge constants/test/links; V3 complete mapping content. |
| C-008 | MERGE | 92 | V1 stops; V2 map; V3 roles, evidence, recovery. |
| C-009 | MERGE | 94 | Severity coverage, observation checks, explicit load gap, independent scoped gate. |
| C-010 | V1 | 90 | ADJ Q11/Q21 do not gate generic note or correction pass. |
| C-011 | MERGE | 90 | V2 verified reads plus V3 historical labelling and refresh. |
| X-001 | V2 | 99 | Checked record confirms packages exist; contents remain separately unread. |
| X-002 | V2 | 99 | Actual sweep code must satisfy security ruling before JOIN. |
| X-003 | MERGE | 98 | V1/V2 read-only CAP has no sweep-merge prerequisite. |
| X-004 | MERGE | 94 | ADJ action list says log now; retain summary conflict. |
| X-005 | V1 | 99 | Adjudicated publication sequence stays hard PROC; V3 equivalent. |

## 5. FINAL per-point table (rows 23-44 of 44, part 3)

| id | winner | confidence | evidence |
|---|---|---:|---|
| X-006 | V1 | 98 | One ordered rollout edit set; V3 equivalent; V2 concedes. |
| X-007 | V2 | 96 | Observer mapping can precede shared note; remove draft blocker. |
| X-008 | V2 | 99 | ADJ expressly permits dedicated research ahead of feature work. |
| X-009 | V2 | 96 | Record and shipped classification differ; owner Q14 wording decides. |
| X-010 | V1 | 98 | Explicit phase-numbering contradiction marker prevents ambiguous handoff prerequisites. |
| X-011 | NEITHER | 99 | All need explicit bounded PR-workflow authorization, separate merge authority. |
| X-012 | MERGE | 96 | V3 isolation principle plus actual authorized storage and staged-scope check. |
| X-013 | MERGE | 96 | Owner merges or explicitly authorizes named merger; no autonomous inference. |
| X-014 | V1 | 96 | WC-16 requires re-arming waits, not adding a scheduler. |
| X-015 | NEITHER | 99 | Validate every corrected register, edge and wave together. |
| A-001 | V1 | 99 | Merge and installed-command availability precede new sweep duty. |
| A-002 | NEITHER | 99 | Explicit per-PR scope resolves blanket-write prohibition conflict. |
| A-003 | MERGE | 97 | Confirm Q24 actor, reachability and terminal capability before capture. |
| A-004 | MERGE | 97 | Name actual author session and role; do not invent worker. |
| A-005 | MERGE | 98 | Verify artifact storage and staged diff; preserve existing evidence. |
| A-006 | MERGE | 92 | Per-wave decisions, next-question presentation, blocked defaults and owner latency. |
| A-007 | V3 | 99 | Historical evidence requires fresh state before action and resume. |
| U-004 | V2 | 97 | Evidence-tagged edges mandatory; process constraints remain hard. |
| U-005 | V2 | 92 | Keep supported tensions; withdraw process-order demotions W7/W8. |
| U-010 | V3 | 99 | Interface failure/retry/idempotency prevents duplicate actions during recovery. |
| U-011 | V3 | 99 | Independent first-release versus end-to-end gate prevents false completion. |
| U-012 | V3 | 99 | Scoped decisions and supersession prevent authority expansion. |

Table coverage across parts 2 and 3: all 44 points.

## 6. Final overall preferred base and minimum fixes

FINAL base: V1, confidence 75/100, changed from V3 at 90. Its existing sequencing now matches the substantive safety consensus. This is not a claim that a measured rewrite-count comparison proved it best. V2's cited edges and V3's recovery/authority contracts remain required contributions.

Minimum fixes before execution:
1. JOIN security (X-002): add the explicit security boundary; the actual code run must implement F1/F2, or the owner must have recorded applicable F3 acceptance/caveats. Merge alone is not the safety proof.
2. Security acceptance (C-001): import V2's two-path measured regression, relevant allow-list/golden impacts and separation of Git-status from contract/transcript read scope. Ruling must not await ledger creation.
3. Authority (X-011/A-002/X-013): owner authorizes the bounded monitored workflow per PR; merges, issue publications and security rulings remain separately authorized. Preserve fork-only targets and WC-13.
4. Artifacts (X-012/A-005): select actual permitted non-sweep storage; inspect staged scope before contested-PR commits. Do not delete or move retained evidence merely to satisfy an isolation slogan.
5. Facts/intake (X-001/A-003/A-004/A-007): correct package availability; label review-time state historical; identify actual author/capture actors and real paths/roles before dispatch. Do not assume the author must be a worker or person-opened session without evidence.
6. Observer (X-007/C-003): remove hard note-draft predecessor; mapping may live in observer text. Make seed-before-live explicit while retaining build, scope, owner-pass and usability gates.
7. Knowledge (X-008/X-009): separate ungated dedicated research from gated brainstorm/design; record owner Q14 interpretation and condition any classification-restoration dependency accordingly.
8. Logging/gates (X-004/C-010): log follow-ups early under publication authority, keep source edits post-merge, flag ADJ summary tension and retain clause-level decision gates.
9. Availability/cadence (A-001/X-014): verify new command installed after merge; retain existing supervision and wait re-arming. No extra housekeeping scheduler by default.
10. Recovery/acceptance (U-010/U-011/U-012): add V3's interface retries, unknown-launch protection, decision scope/lifetime, read-versus-seed consent, artifact readback and two-scope independent completion gate.
11. Graph/schedule (S-003/X-015): incorporate V2's evidenced edges with an explicit old-to-new identity map; reconcile register/graph/waves, then independently check missing edges, authority crossings and scope-specific exit criteria.

No live GitHub/Orca calls or behavior tests were performed. INV-008 remains unresolved.

## Scoring Matrix

Source: the Round 2 FINAL per-point table of each advocate (`round2-rebuttal-V1.md`, `-V2.md`, `-V3.md`, section 5). Cells show winner (confidence). Winner = choice named by at least 2 of 3 advocates; confidence = mean of the majority advocates' confidences; UNRESOLVED (confidence 50) when no 2 agree. Level from `diff-analysis.md`; U points carry no level there (shown as U). Evidence Summary quotes the majority advocates' Round 2 evidence cells.

| Diff Point | Level | V1 | V2 | V3 | Winner | Confidence | Agreement | Evidence Summary |
|---|---|---|---|---|---|---|---|---|
| S-001 | L1 | MERGE (65) | MERGE (60) | MERGE (80) | MERGE | 68.3% | UNANIMOUS | V1: V1 seed-ordered skeleton; add V2 weak points, V3 interface blocks. V2: V2 weak points, V1 seed order and marker, V3 interface blocks. |
| S-002 | L2 | V1 (60) | MERGE (60) | V1 (75) | V1 | 67.5% | AGREED 2/3 | V1: Fewest reversals: V2 must collapse WA-02/03/04, drop CO-01. V3: Explicit stages avoid V3 bundling; reconcile V2 identity collisions. |
| S-003 | L2 | V2 (80) | V2 (85) | V2 (94) | V2 | 86.3% | UNANIMOUS | V1: Only V2 gives kind and evidence per edge (U-004). V2: Only V2 gives kind and evidence per edge (U-004). |
| S-004 | L2 | MERGE (65) | MERGE (70) | MERGE (88) | MERGE | 74.3% | UNANIMOUS | V1: V1 waves and serial table; V3 interruption rule; V2 lists. V2: V2 lists, V1 serial table, V3 interruption rule; fix X-015. |
| S-005 | L3 | MERGE (75) | MERGE (75) | MERGE (94) | MERGE | 81.3% | UNANIMOUS | V1: V1 TB names, V2 TB-3, V3 M-APPROVAL and B-EDIT. V2: V2 TB-3, TB-6; V1 names; V3 M-APPROVAL, B-EDIT, B-WRITE. |
| S-006 | L1 | MERGE (70) | MERGE (70) | MERGE (88) | MERGE | 76.0% | UNANIMOUS | V1: V1 named worktrees; V2 "Observe:"; V3 decision lifetime. V2: V2 "Observe:"; V1 named worktrees; V3 decision lifetime. |
| C-001 | L3 | MERGE (85) | V2 (80) | V2 (96) | V2 | 88.0% | AGREED 2/3 | V2: Ruling plus apply; `.gitattributes` test; F2 `unscanned` falsifier. V3: Separate ruling/apply; measured regression, scope separation, refusal falsifier. |
| C-002 | L2 | MERGE (70) | MERGE (70) | MERGE (92) | MERGE | 77.3% | UNANIMOUS | V1: V1 interim deliverables, V2 root cause, V3 completion rule. V2: V2 root cause, V1 interim deliverables, V3 completion rule. |
| C-003 | L3 | V1 (75) | V1 (82) | V1 (96) | V1 | 84.3% | UNANIMOUS | V1: Layout read on live Run before seeded test risks consumption (X-016). V2: Live-layout read on real Run before seeded test (ADJ 333, 465). |
| C-004 | L2 | V1 (75) | V1 (78) | V1 (90) | V1 | 81.0% | UNANIMOUS | V1: One #450 edit set (A-011); V2 conceded. V2: One #450 edit set (ADJ line 391); V2 conceded. |
| C-005 | L2 | MERGE (65) | MERGE (65) | MERGE (90) | MERGE | 73.3% | UNANIMOUS | V1: V1 one reply with Q4 line; V3 audit reconciliation. V2: V1 one reply carrying Q4 line; V3 audit reconciliation. |
| C-006 | L2 | V2 (85) | V2 (88) | V2 (98) | V2 | 90.3% | UNANIMOUS | V1: ADJ line 710: research "may be done ahead". V2: ADJ line 710: research "may be done ahead of the rest". |
| C-007 | L2 | MERGE (70) | MERGE (70) | MERGE (94) | MERGE | 78.0% | UNANIMOUS | V1: V1/V2 test after merge; V3 content list and mapping. V2: Draft early, test after merge (SC-28); V3 mapping content. |
| C-008 | L2 | MERGE (75) | MERGE (75) | MERGE (92) | MERGE | 80.7% | UNANIMOUS | V1: V1 guardrails and stops; V2 map; V3 roles, resume. V2: V1 guardrails and stops; V2 verified map; V3 roles, resume. |
| C-009 | L3 | MERGE (70) | MERGE (70) | MERGE (94) | MERGE | 78.0% | UNANIMOUS | V1: V1 severity map; V2 check commands, INV-032 gap; V3 gate. V2: V2 check commands, INV-032 gap; V1 severity map; V3 gate. |
| C-010 | L2 | V1 (70) | V1 (65) | V1 (90) | V1 | 75.0% | UNANIMOUS | V1: ADJ lines 781, 787: Q11, Q17 do not gate note. V2: ADJ 434, 772, 781: no Q2, Q11 gate on #409/note. |
| C-011 | L1 | V2 (80) | V2 (82) | MERGE (90) | V2 | 81.0% | AGREED 2/3 | V1: V2 OBS-NOW checks correct; V1 Glob wrong (SC-01). V2: OBS-NOW checks confirmed by SC-02, 23, 24, 27, 28. |
| X-001 | L2 | V2 (98) | V2 (98) | V2 (99) | V2 | 98.3% | UNANIMOUS | V1: Both packages exist; V1 0.4 item 5 wrong. V2: Both packages exist (SC-01, SC-02); V1 conceded. |
| X-002 | L3 | V2 (92) | V2 (92) | V2 (99) | V2 | 94.3% | UNANIMOUS | V1: JOIN runs unfixed `git status`; TB-1 must precede it. V2: JOIN runs unfixed `git status`; TB-1 must precede it. |
| X-003 | L2 | V1 (85) | MERGE (85) | MERGE (98) | MERGE | 91.5% | AGREED 2/3 | V2: V1 and V2 agree: ADJ line 414, no #539 predecessor. V3: V1/V2 read-only CAP has no sweep-merge prerequisite. |
| X-004 | L2 | MERGE (75) | MERGE (75) | MERGE (94) | MERGE | 81.3% | UNANIMOUS | V1: ADJ lines 211-212 "now"; keep V2 W1 flag. V2: ADJ lines 211-212 "now"; keep V2 W1 flag on line 348. |
| X-005 | L3 | V1 (88) | V1 (90) | V1 (99) | V1 | 92.3% | UNANIMOUS | V1: ADJ line 442 all-advocate order; V2 conceded. V2: ADJ line 442 all-advocate order; V2 conceded. |
| X-006 | L3 | V1 (88) | V1 (88) | V1 (98) | V1 | 91.3% | UNANIMOUS | V1: A-011 one edit set per issue; INV-030 no etag. V2: A-011 one edit set per issue; INV-030 no etag. |
| X-007 | L3 | V2 (80) | V2 (82) | V2 (96) | V2 | 86.0% | UNANIMOUS | V1: ADJ line 192 lists no note predecessor; V1 conceded. V2: ADJ line 192 lists no note predecessor; V1 conceded. |
| X-008 | L2 | V2 (85) | V2 (88) | V2 (99) | V2 | 90.7% | UNANIMOUS | V1: ADJ line 710; V1 ambiguous, V3 conceded. V2: ADJ line 710; V1 and V3 conceded. |
| X-009 | L3 | V2 (72) | V2 (75) | V2 (96) | V2 | 81.0% | UNANIMOUS | V1: W5 separates record from shipped class; owner Q14 decides. V2: W5 separates record from shipped class; Q14 wording decides. |
| X-010 | L2 | V1 (88) | V1 (88) | V1 (98) | V1 | 91.3% | UNANIMOUS | V1: V1 1.4 marker; V2 conceded conflation. V2: V1 1.4 marker; V2 conceded conflation. |
| X-011 | L3 | NEITHER (90) | NEITHER (90) | NEITHER (99) | NEITHER | 93.0% | UNANIMOUS | V1: All conflict with tool; per-PR approval rule plus M-APPROVAL. V2: All conflict with tool; per-PR approval plus M-APPROVAL. |
| X-012 | L3 | MERGE (82) | MERGE (82) | MERGE (96) | MERGE | 86.7% | UNANIMOUS | V1: V3 "no sidecar in #539" plus named separate checkout. V2: V3 "no sidecar in #539" plus named separate coordinator checkout. |
| X-013 | L2 | MERGE (65) | MERGE (70) | MERGE (96) | MERGE | 77.0% | UNANIMOUS | V1: Owner merges or approves named merger; ADJ line 208 silent. V2: Owner merges or approves named merger; ADJ 101, 208. |
| X-014 | L3 | V1 (72) | MERGE (78) | V1 (96) | V1 | 84.0% | AGREED 2/3 | V1: WC-16 `:288`: re-arm waits, "not a scheduler"; V1 6.6. V3: WC-16 requires re-arming waits, not adding a scheduler. |
| X-015 | L2 | NEITHER (80) | NEITHER (80) | NEITHER (99) | NEITHER | 86.3% | UNANIMOUS | V1: Every variant has register/schedule mismatches; fix all. V2: Every variant has schedule-register mismatches; fix each. |
| A-001 | L3 | V1 (92) | V1 (92) | V1 (99) | V1 | 94.3% | UNANIMOUS | V1: SC-06: no `/sc:sweep` on master; install step needed. V2: SC-06: no `/sc:sweep` on master; install step needed. |
| A-002 | L3 | NEITHER (90) | NEITHER (90) | NEITHER (99) | NEITHER | 93.0% | UNANIMOUS | V1: Same root as X-011; per-PR scoped authorization. V2: Same root as X-011; per-PR scoped authorization. |
| A-003 | L2 | MERGE (75) | MERGE (75) | MERGE (97) | MERGE | 82.3% | UNANIMOUS | V1: Confirm Q24 runner live at W0, else default applies. V2: Confirm Q24 runner live at W0, else Q24 default. |
| A-004 | L2 | MERGE (75) | MERGE (75) | MERGE (97) | MERGE | 82.3% | UNANIMOUS | V1: Owner names #539 author session at W0. V2: Owner names #539 author session at W0; "worker" withdrawn. |
| A-005 | L3 | MERGE (80) | MERGE (80) | MERGE (98) | MERGE | 86.0% | UNANIMOUS | V1: Debate folder not ignored; named-files-only staging in #539. V2: Debate folder not ignored (SC-42); named-files-only staging. |
| A-006 | L2 | MERGE (65) | MERGE (65) | MERGE (92) | MERGE | 74.0% | UNANIMOUS | V1: V1 "Wave needed by" plus owner latency as critical path. V2: Per-wave question batches; owner latency is the critical path. |
| A-007 | L3 | V3 (78) | V3 (78) | V3 (99) | V3 | 85.0% | UNANIMOUS | V1: Treat ADJ live facts historical; re-read at each gate. V2: ADJ live facts historical; re-read at W0 and each gate. |
| U-004 | U | V2 (82) | V2 (85) | V2 (97) | V2 | 88.0% | UNANIMOUS | V1: Edge kinds with evidence; apply PROC to cross-issue order. V2: Edge kinds with evidence; PROC for the cross-issue order. |
| U-005 | U | V2 (75) | V2 (75) | V2 (92) | V2 | 80.7% | UNANIMOUS | V1: Keep W1, W2, W4, W5, W6; drop W7, W8. V2: Keep W1 to W6; withdraw W7, W8 (X-005). |
| U-010 | U | V3 (78) | V3 (78) | V3 (99) | V3 | 85.0% | UNANIMOUS | V1: Failure, retry, idempotency per interface; prevents duplicate writes. V2: Failure, retry, idempotency per interface; prevents duplicate writes. |
| U-011 | U | V3 (82) | V3 (82) | V3 (99) | V3 | 87.7% | UNANIMOUS | V1: Two-scope gate stops first-release PASS read as end-to-end. V2: Two-scope gate stops first-release PASS read as end-to-end. |
| U-012 | U | V3 (82) | V3 (82) | V3 (99) | V3 | 87.7% | UNANIMOUS | V1: Authority not granted and decision lifetime bound owner answers. V2: Authority not granted and decision lifetime bound owner answers. |

Normalization used for both rounds: a position cell is read by its first word, so "MERGE (V1 base)" counts as MERGE and "V2 (and V3)" counts as V2. Round 1 positions come from each advocate's "Per-point positions" table (V3: both parts); Round 2 from each "Final per-point table" (section 5). All six tables hold exactly the 44 point ids, checked by script.

## Convergence Assessment
- Points resolved (Round 2, at least 2 of 3 advocates name the same winner): 44 of 44 (unanimous 39, two-of-three 5: S-002, C-001, C-011, X-003, X-014)
- Alignment: 100.0% (44/44). Round 1 for comparison: 41 of 44 = 93.2% (unanimous 15)
- Threshold: 75%
- Status: CONVERGED (on the agreement count only; the invariant gate is applied separately by the orchestrator after the Round 2.5 probe, and `invariant-probe.md` is still a stub with TODO markers at the time of this tally)
- Unresolved points (Round 2): none. Round 1 unresolved: S-001, C-005, C-010 (all three resolved in Round 2: S-001 MERGE, C-005 MERGE, C-010 V1)
- Taxonomy coverage (Round 2 agreed / points): L1 3/3, L2 20/20, L3 16/16, U (no level in `diff-analysis.md`) 5/5. Every level is covered. Round 1: L1 2/3, L2 18/20, L3 16/16, U 5/5
- Round 2 winners: MERGE 17, V2 11, V1 9, V3 4, NEITHER 3
- Oscillation (an advocate's own winner differs between Round 1 and Round 2): 40 advocate-point flips on 29 of 44 points (V1 7, V2 11, V3 22)
  - V1 (7): S-003 MERGE->V2; C-007 V1->MERGE; X-012 V3->MERGE; X-013 V1->MERGE; X-014 MERGE->V1; A-005 V3->MERGE; A-007 V2->V3
  - V2 (11): S-001 V2->MERGE; S-006 V2->MERGE; C-003 MERGE->V1; C-005 V1->MERGE; C-010 V2->V1; X-003 V2->MERGE; X-004 V2->MERGE; X-013 V1->MERGE; X-015 V2->NEITHER; A-004 V1->MERGE; A-005 V3->MERGE
  - V3 (22): S-001 V3->MERGE; S-002 MERGE->V1; S-003 MERGE->V2; C-001 MERGE->V2; C-002 V3->MERGE; C-003 MERGE->V1; C-004 V3->V1; C-005 V3->MERGE; C-008 V3->MERGE; C-010 MERGE->V1; C-011 V3->MERGE; X-001 MERGE->V2; X-003 V2->MERGE; X-005 MERGE->V1; X-006 MERGE->V1; X-007 MERGE->V2; X-012 V3->MERGE; X-013 V3->MERGE; X-014 V2->V1; A-006 V3->MERGE; U-004 MERGE->V2; U-005 MERGE->V2
  - Majority winner changed between rounds on 12 points: S-001 (UNRESOLVED->MERGE), S-002 (MERGE->V1), S-003 (MERGE->V2), C-001 (MERGE->V2), C-003 (MERGE->V1), C-005 (UNRESOLVED->MERGE), C-010 (UNRESOLVED->V1), X-003 (V2->MERGE), X-012 (V3->MERGE), X-013 (V1->MERGE), X-014 (MERGE->V1), A-005 (V3->MERGE)
