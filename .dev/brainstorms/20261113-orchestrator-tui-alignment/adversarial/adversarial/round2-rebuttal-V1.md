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
