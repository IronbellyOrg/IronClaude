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
