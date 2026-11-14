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
