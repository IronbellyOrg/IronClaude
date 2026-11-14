# Base Selection Report

Template: `~/.claude/skills/sc-adversarial-protocol/refs/artifact-templates.md` Section 3; algorithm: `refs/scoring-protocol.md` A.1 to A.5.

Reconciler: Step 3 (hybrid scoring and base selection). Argues for no variant. Read-only except this file. Run 2026-11-13.

- V1 = `variant-1-opus-architect.md` (751 lines), V2 = `variant-2-opus-analyzer.md` (719), V3 = `variant-3-haiku-backend.md` (662). "Vn:L" is a line in that file.
- Inputs: `scoring-pass1.md` (quantitative layer and qualitative pass 1, order V1, V2, V3), `scoring-pass2.md` (qualitative pass 2, order V3, V2, V1, with its machine-readable table), `debate-transcript.md` (Scoring Matrix, lines 973-1024), `convergence.md`, `diff-analysis.md`, `invariant-probe.md`, `round2-rebuttal-V1/V2/V3.md` section 6, `round3-invariants-V1/V2/V3.md`, `../../seed-brief.md`.
- Every disputed criterion below was settled by opening the variant text again in this step; the lines quoted were read in this step.

## Quantitative Scoring (50% weight)

Taken unchanged from `scoring-pass1.md` (the quantitative layer runs once; it is deterministic and is not part of position-bias mitigation). Counting methods and raw counts are in `scoring-pass1.md` sections RC, IC, SR, DC and SC.

| Metric | Weight | V1 (opus-architect) | V2 (opus-analyzer) | V3 (haiku-backend) |
|--------|--------|---------------------|--------------------|--------------------|
| requirement_coverage | 0.30 | 1.0000 (18/18: seed criteria R1-R12, constraints C1-C6) | 1.0000 (18/18) | 1.0000 (18/18) |
| internal_consistency | 0.25 | 0.9946 (1 - 2/368) | 0.9952 (1 - 2/417) | 0.9925 (1 - 2/267) |
| specificity_ratio | 0.15 | 1.0000 (454 / (454 + 0)) | 1.0000 (474 / (474 + 0)) | 0.9917 (360 / (360 + 3)) |
| dependency_completeness | 0.15 | 1.0000 (1169/1169) | 0.9992 (1200/1201) | 1.0000 (768/768) |
| section_coverage | 0.15 | 1.0000 (8/8 H2) | 1.0000 (8/8 H2) | 1.0000 (8/8 H2) |
| **quant_score** | | **0.998641** | **0.998676** | **0.996888** |

Computation notes:
- quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC. V1 0.30 + 0.248641 + 0.15 + 0.15 + 0.15 = 0.998641. V2 0.30 + 0.248801 + 0.15 + 0.149875 + 0.15 = 0.998676. V3 0.30 + 0.248127 + 0.148760 + 0.15 + 0.15 = 0.996888.
- Spread 0.0018. All three variants share one seed and one adjudicated source, so every requirement and almost every internal id resolves in all three. The layer cannot separate them; the qualitative layer and the tiebreaker do.
- The two IC contradictions per variant (IC-V1-1, IC-V1-2, IC-V2-1, IC-V2-2, IC-V3-1, IC-V3-2) are the same findings that make CORR-4 NOT MET for all three in both passes.
- V3's SR loss comes from three vague lines (V3:443 "as needed", V3:444 "Appropriate owner answers", V3:517 "adequate plans"); the same wording drives V3's CLAR-1 NOT MET in both passes.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Reconciled verdicts (30 criteria, 6 dimensions, scoring-protocol A.2). Full CEV rows (claim, evidence, verdict) for all 90 cells are in `scoring-pass1.md` (section "Qualitative Scoring") and `scoring-pass2.md` (sections "Completeness" to "Invariant & Edge Case Coverage"); they are not copied here. For the 84 cells where the passes agree, both passes' CEV rows stand. For the 6 cells where they disagree, the final CEV is in "Position-Bias Mitigation", R-1 to R-4 below.

### Reconciled per-criterion verdicts

1 = MET, 0 = NOT MET. "agree" = both passes gave this verdict; "R-n" = settled by re-evaluation R-n.

| Criterion | V1 | V2 | V3 | Basis |
|---|---|---|---|---|
| COMP-1 Covers all explicit requirements | 1 | 1 | 1 | agree |
| COMP-2 Edge cases and failures | 1 | 1 | 1 | agree |
| COMP-3 Dependencies and prerequisites | 1 | 1 | 1 | agree |
| COMP-4 Success or completion criteria | 1 | 1 | 1 | agree |
| COMP-5 Out of scope stated | 1 | 1 | 1 | agree |
| CORR-1 No factual errors | 0 | 0 | 1 | agree (V1: SC-01 WRONG at V1:57 plus INV-001 at V1:575; V2: INV-001 at V2:563, 610) |
| CORR-2 Feasible with stated constraints | 0 | 0 | 0 | agree for V1, V2; R-1 for V3 |
| CORR-3 Terminology consistent | 1 | 0 | 1 | agree for V2 (X-010), V3; R-2 for V1 |
| CORR-4 No internal contradictions | 0 | 0 | 0 | agree (IC-V1-1/2, IC-V2-1/2, IC-V3-1/2) |
| CORR-5 Claims supported | 1 | 1 | 1 | agree |
| STRU-1 to STRU-5 | 5 | 5 | 5 | agree (all MET) |
| CLAR-1 Unambiguous language | 1 | 0 | 0 | agree for V1, V3; R-3 for V2 |
| CLAR-2 Concrete | 1 | 1 | 1 | agree |
| CLAR-3 Section purpose | 1 | 1 | 1 | agree |
| CLAR-4 Terms defined on first use | 0 | 0 | 0 | agree (QUESTION-LINK undefined in all three: V1:40, V2:31, V3:34) |
| CLAR-5 Next steps and decisions | 1 | 1 | 1 | agree |
| RISK-1 3+ risks with probability and impact | 0 | 0 | 0 | agree (no probability rating in any variant) |
| RISK-2 Mitigation for each risk | 1 | 1 | 1 | R-4 |
| RISK-3 Failure modes and recovery | 1 | 1 | 1 | agree |
| RISK-4 External dependencies and failure | 1 | 1 | 1 | agree (residual INV-009 "Orca app not running" missing in all three, not scored) |
| RISK-5 Monitoring or validation | 1 | 1 | 1 | agree |
| INV-1 to INV-5 | 5 | 5 | 5 | agree (all MET) |

### Qualitative Summary (after reconciliation)

| Dimension | V1 (opus-architect) | V2 (opus-analyzer) | V3 (haiku-backend) |
|-----------|----|----|----|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 2/5 | 1/5 | 3/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 3/5 | 3/5 |
| Risk Coverage | 4/5 | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.833333** | **23/30 = 0.766667** | **25/30 = 0.833333** |

What separates them: Correctness and Clarity only. V3 is the most correct (3/5: no wrong fact, no worker PR tool, consistent terms) but fails feasibility (R-1) and clarity of wording (CLAR-1). V1 is the clearest (only variant with no discretionary qualifier) but carries one checked-wrong fact (SC-01) and the worker PR instruction (INV-001). V2 loses one point more than both: worker PR instruction twice, the unmarked "Phase 2" double meaning (X-010) and "if convenient" (R-3).

### Edge-case floor check

| Variant | Invariant & Edge Case Coverage | Floor (at least 1/5) | Eligible as base |
|---|---|---|---|
| V1 | 5/5 | met | yes |
| V2 | 5/5 | met | yes |
| V3 | 5/5 | met | yes |

Both passes agree on 5/5 for every variant; the floor is not suspended. The residual invariant gaps recorded by both passes (INV-001 worker PR actor, INV-002 coordinator home, INV-003 stall under defaults, INV-004 `filter.<driver>.process`, INV-013 single M-APPROVAL node in V3) are not scored against this dimension, because each variant meets all five criteria through other cited coverage. They are carried into the must-fix list of the selected base below.

## Position-Bias Mitigation

### Mechanical diff of the two passes

Pass 1 has no machine-readable table, so its six dimension tables were converted by script: each criterion row of `scoring-pass1.md` between "## Qualitative Scoring" and "### Qualitative Summary" was read in order (dimension order Completeness, Correctness, Structure, Clarity, Risk, Invariant; criteria 1-5 within each), and its V1, V2 and V3 verdict cells mapped "NOT MET" to 0 and "MET" to 1. Pass 2's "Machine-readable verdict table" was read as is. Both files gave 30 rows; the script's column totals reproduce each pass's own summary (pass 1: V1 23, V2 23, V3 25; pass 2: V1 25, V2 23, V3 25). `diff -u` of the two 30-row tables (columns V1 | V2 | V3):

```diff
@@ -4,8 +4,8 @@
 COMP-4 | 1 | 1 | 1
 COMP-5 | 1 | 1 | 1
 CORR-1 | 0 | 0 | 1
-CORR-2 | 0 | 0 | 1
-CORR-3 | 0 | 0 | 1
+CORR-2 | 0 | 0 | 0
+CORR-3 | 1 | 0 | 1
 CORR-4 | 0 | 0 | 0
 CORR-5 | 1 | 1 | 1
 STRU-1 | 1 | 1 | 1
@@ -13,13 +13,13 @@
 STRU-3 | 1 | 1 | 1
 STRU-4 | 1 | 1 | 1
 STRU-5 | 1 | 1 | 1
-CLAR-1 | 1 | 1 | 0
+CLAR-1 | 1 | 0 | 0
 CLAR-2 | 1 | 1 | 1
 CLAR-3 | 1 | 1 | 1
 CLAR-4 | 0 | 0 | 0
 CLAR-5 | 1 | 1 | 1
 RISK-1 | 0 | 0 | 0
-RISK-2 | 0 | 0 | 0
+RISK-2 | 1 | 1 | 1
 RISK-3 | 1 | 1 | 1
 RISK-4 | 1 | 1 | 1
 RISK-5 | 1 | 1 | 1
```

Result: 4 criteria disagree (CORR-2, CORR-3, CLAR-1, RISK-2), covering 6 variant cells: CORR-2 V3, CORR-3 V1, CLAR-1 V2, RISK-2 V1, RISK-2 V2, RISK-2 V3. The other 26 criteria (84 of 90 cells) agree and keep the agreed verdict. Every disagreement favours pass 2 for V1 (+2: CORR-3, RISK-2) and is mixed for the others (V2 -1 +1; V3 -1 +1), so there is no uniform first-position or last-position direction.

### Re-evaluation of each disagreement (final verdicts)

Each cell was re-evaluated by a direct comparison of both passes' evidence against the variant text, opened again in this step. The re-evaluation verdict is final (scoring-protocol A.5).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| CORR-2 feasible with stated constraints | V3 | MET | NOT MET | DISAGREE | **NOT MET** |
| CORR-3 terminology consistent | V1 | NOT MET | MET | DISAGREE | **MET** |
| CLAR-1 unambiguous language | V2 | MET | NOT MET | DISAGREE | **NOT MET** |
| RISK-2 mitigation for each risk | V1 | NOT MET | MET | DISAGREE | **MET** |
| RISK-2 mitigation for each risk | V2 | NOT MET | MET | DISAGREE | **MET** |
| RISK-2 mitigation for each risk | V3 | NOT MET | MET | DISAGREE | **MET** |

**R-1. CORR-2, V3: NOT MET.**
- Pass 1 evidence: V3 does not give `/sc:pr-submit` to workers; the role contract keeps external writes with the coordinator (V3:507-508). Pass 1 itself recorded "Residual X-011 shared by all three" and, in its IC notes, said X-011 is to be scored in qualitative Correctness, but did not charge it here.
- Pass 2 evidence: (a) the hard issue-edit order stalls under V3's own defaults (invariant-probe INV-003); (b) X-011; (c) one M-APPROVAL node for seven items (INV-013).
- Re-check: V3:485 requires "Explicit authorization for every outward write, merge and live test"; V3:520 mandates "IronClaude PRs use `/sc:pr-submit --monitor 3`", the tool the project rule describes as pushing fixes and resolving threads without asking (diff X-011, rated High; A-002 CONTRADICTED). Two of V3's own stated constraints cannot both hold. Separately, CO-01 requires "Q3 and Q4 explicit" (V3:188), Q3's default is "No #477 rewrite" (V3:296), and OB-04 (the #409 body correction) is blocked by CO-01 (V3:138), so under defaults OB-04, XC-06 and V2-01 never become eligible; V3:454 accepts "Default-blocked lanes stay blocked", which makes the #409, #339 and #423 corrections wait on an unrelated Coder decision. Pass 1 is right that this is a stall rather than a contradiction (so it is not CORR-4), but a plan that cannot reach its target state under its own defaults fails feasibility. The M-APPROVAL point (V3:333) is a modelling gap, not decisive on its own.
- Verdict: NOT MET. The pass 1 basis (no worker PR tool) is true but does not answer X-011 or the stall.

**R-2. CORR-3, V1: MET.**
- Pass 1 evidence: "SEED" means the seed brief (V1:24) and is also the label of the test "Seeded consumption test (SEED)" (V1:178).
- Pass 2 evidence: the two "Phase 2" senses are kept apart by a contradiction marker (V1:103); markers defined once (V1:30-32).
- Re-check: "(SEED)" at V1:178 is a source tag, not a second meaning. V1 tags sources in parentheses in the same way elsewhere ("(ENR)" at V1:123, 161, 305, 311, 560), and the seed brief itself names the "seeded consumption test" (`seed-brief.md:97`, `:102`). So "SEED" means the seed brief at both places. The "Phase 2" collision, which costs V2 this criterion, is fenced off in V1 by the CONTRADICTION MARKER at V1:103 (SW-12 versus SW-13).
- Verdict: MET. Pass 1's collision does not exist.

**R-3. CLAR-1, V2: NOT MET.**
- Pass 1 evidence: its vague-word grep (pattern: appropriate, as needed, properly, adequate, should consider, might, various, etc., best practices, industry standard) found 0 hits in V2.
- Pass 2 evidence: V2:498 Wave 2 lane "OB-05, with OB-08 if convenient"; the two "only if needed" hits (V2:499, 551) are tied to a stated condition and were not counted.
- Re-check: a wider grep in this step (adding as required, if needed, if convenient, where possible) over all three variants: V1 0 hits; V2 V2:498, 499, 551; V3 V3:114, 302, 443, 444, 521. In V2, OB-08 is placed in a wave only at V2:498, and only "if convenient"; no other wave row schedules it (OB-08 also appears at V2:147, 283, 286, 400, 439, 459, 507, 548, none of which fixes its wave; V2:548 lists it in the `409-guard-flip` worktree row). Its schedule is therefore left to discretion. Pass 1's grep pattern did not include the phrase, so its 0 is a coverage gap, not evidence. The same standard already makes V3 NOT MET in both passes.
- Verdict: NOT MET.

**R-4. RISK-2, V1, V2 and V3: MET (all three).**
- Pass 1 evidence: one risk per variant with no mitigation stated beside it: V1:229 "Host-only facts ... other hosts UNVERIFIED (INV-011)"; V2:196 R-WA5 "ClickUp writes made by FU-1 may not be reversible"; V3:122 "Full build divergence remains unresolved even if the release prefix matches."
- Pass 2 evidence: examples of risks paired with controls in each variant (V1:149, 189, 292, 332; V2:192, 252, 292; V3:287 and the Section 7 check table).
- Re-check: the criterion is mitigation for each identified risk in the document, not in the same bullet. Each of pass 1's counterexamples is mitigated elsewhere in its own variant:
  - V1:229 maps to the INV coverage row V1:657 "INV-011 | MED | WA-04 (c) | both permission knobs and real argv recorded", and WA-04 (b) and (c) (V1:218) require the owner's written acceptance of the permission mode and the real argv; other hosts are out of scope (V1:98; seed constraint single host).
  - V2:196 (ClickUp writes) is bounded by WA-05 (b) "the owner's written acceptance of the session's permission mode, test issue only" and (i) "the list of writes and the test issue closed or unlabelled" (V2:185). V2:712 marks INV-032 "Gap" for measurement only; the load risk itself is capped by guardrail V2:574 ("do not start extra observers").
  - V3:122 is answered by SW-01 (V3:108, the owner ruling with regression evidence) and by the edge-case runbook V3:623 "Orca full build differs: stop build-dependent gates; retain old evidence labelled with its build".
  The ClickUp reversibility note also present in V1 (V1:230) is bounded the same way (V1:218 (b) and (i)), and V3:173 bounds it with "owner consent". With the same standard applied to all three, no variant leaves an identified risk without a control somewhere in the document.
- Verdict: MET for V1, V2 and V3. Pass 1's adjacency reading is stricter than the criterion and its three counterexamples fail on re-check.

### Counts

- Disagreements found: 4 criteria, 6 variant cells.
- Disagreements re-evaluated: 6 of 6.
- Final verdicts changed: 6 of 6 relative to pass 1 (the input-order pass); 0 of 6 relative to pass 2. Every final verdict matches pass 2.
- Final qualitative totals after reconciliation: V1 25/30, V2 23/30, V3 25/30 (pass 2's totals; pass 1 had V1 23, V2 23, V3 25).

## Combined Scoring

variant_score = 0.50 x quant_score + 0.50 x qual_score (scoring-protocol A.3).

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate tiebreaker (Round 2 points won outright, of 44) |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (opus-architect) | 0.499321 | 0.416667 | **0.915987** | 9 (20.45%) |
| V3 (haiku-backend) | 0.498444 | 0.416667 | **0.915111** | 4 (9.09%) |
| V2 (opus-analyzer) | 0.499338 | 0.383333 | **0.882671** | 11 (25.00%) |

**Ranking:** 1. V1 0.915987; 2. V3 0.915111; 3. V2 0.882671.

**Margin:** V1 over V3 = 0.000877 (0.096% of V3's score), far **below** the 5 percent threshold (|A - B| < 0.05). The qualitative scores are tied at 25/30; the whole gap comes from the quantitative layer (V1's higher IC and SR), which is too small to decide on. V2 is 0.033316 below V1 and 0.032439 below V3, so **V2 is also inside the 5 percent band** of both the first and the second place.

**Tiebreaker applied: Yes.**

Debate counting rule: points won are the Winner column of `debate-transcript.md` Scoring Matrix (lines 973-1024), tallied by script over all 44 rows: MERGE 17, V2 11, V1 9, V3 4, NEITHER 3. Only rows whose winner is V1, V2 or V3 count as a win for that variant. MERGE (17) and NEITHER (3) count for no variant: a MERGE verdict says the point needs material from several variants, and NEITHER says no variant got it right, so neither is a win for any single variant. Sensitivity: crediting every MERGE to all three variants adds 17 to each and changes no ordering. "Tied within 5%" at level 1 is read on the same scale as the score margin: an absolute difference of less than 0.05 in the share of the 44 points.

**Protocol reading (top two only, A.4 as written): decided at level 1.**
- Level 1, debate performance: V1 9/44 = 0.2045 against V3 4/44 = 0.0909; difference 0.1136, not within 0.05. **V1 wins.** Level 2 (correctness count; V3 3/5 against V1 2/5) and level 3 (input order) are not reached.

**Check with V2 inside the band (three-way reading): same result, decided at level 2.**
- Level 1: V2 11/44 = 0.2500, V1 0.2045, V3 0.0909. V3 is 0.1591 behind the leader and drops out. V2 and V1 differ by 0.0455, within 0.05, so they are tied at level 1.
- Level 2, correctness criteria met: V1 2/5 against V2 1/5. **V1 wins.**
- Under a relative reading of level 1 (11 against 9 wins is an 18% difference), V2 would win at level 1. This report applies the absolute reading used for the score margin, consistently; the protocol text (A.4) names only the top two, and under that text V2 is not considered at all.

Corroborating, not part of the algorithm: two of the three advocates named V1 as their final preferred base after Round 2 (`convergence.md`, "Final preferred base": V1 advocate V1 at 70, V3 advocate V1 at 75 changed from V3 at 90; V2 advocate V2 at 60, "would accept V1 if a fresh reviewer's row count goes against V2").

## Selected Base: Variant V1 (opus-architect)

### Selection Rationale

- **Score:** V1 0.915987, V3 0.915111, V2 0.882671. V1 and V3 tie on the reconciled qualitative layer (25/30 each); V1's lead is 0.000877, from the quantitative layer only.
- **Decided by the tiebreaker, level 1 (debate performance):** V1 won 9 of 44 points outright, V3 won 4 (difference 0.1136 of the 44 points, outside the 0.05 tie band). With V2 also inside the 5 percent band, a three-way tiebreak ties V2 (11) and V1 (9) at level 1 under the absolute reading and V1 wins at level 2 (correctness 2/5 against 1/5). V1 is selected under both readings.
- **What V1 holds that the others do not:** the debate's agreed safety order is already V1's structure. V1 won the hard cross-issue edit order (X-005, 92.3%) and the single #450 edit set (X-006, 91.3%; C-004, 81.0%), both conceded by V2; the live-layout read before the seeded test (C-003, 84.3%); the Phase 2 numbering marker (X-010, 91.3%, V1:103); the `/sc:sweep` install gate (A-001, 94.3%); the owner-decision gate mapping (C-010, 75.0%); and the register shape with the fewest reversals (S-002, 67.5%). V1 is also the only variant with no discretionary wording (CLAR-1).
- **What V1 gets wrong, which the merge must fix:** one checked-wrong fact (V1:57, the two task packages "were not found", SC-01 WRONG; X-001), the worker-run `/sc:pr-submit --monitor 3` (V1:575; INV-001), the JOIN run before the INV-008 fix (V1:322; X-002), the ledger placed in the #539 checkout against V1's own warning (V1:319 against V1:332; X-012), and the Q3-default stall in its hard chain (V1:346 against V1:183, 436; INV-003).
- **Caveat recorded for the merge step:** V3 has the higher Correctness count (3/5 against 2/5) and lost only on the tiebreaker; its contracts and gates are the largest import below.

### Strengths to Preserve from Base (V1)

1. Hard cross-issue publication order #450 -> Coder#477 -> #409 -> #339 -> #423 (X-005) and one ordered edit set per issue, with one `updatedAt` re-read (X-006, C-004; V1 4.2 graph, V1:436).
2. Observer guard flip sequence OB-03 -> OB-04 -> OB-06, live-layout read ordered against the seeded consumption test (C-003).
3. CONTRADICTION MARKER for the two "Phase 2" senses, with SW-12 and SW-13 as separate items (V1:103; X-010).
4. `/sc:sweep` availability caveat (V1 7.3; A-001), to be widened by INV-006 below.
5. Owner-decision gate mapping that keeps Q11 and Q17 off the contract note (C-010) and the "Wave needed by" column in the Q table (V1:342-367).
6. Seed-ordered skeleton (sections 0-7), numbered H3 subsections, "How to read a work item" (V1:60-62), the INV coverage map by severity (V1 7.1) and the extension slots (V1 7.5).
7. Zero discretionary qualifiers; uncertainty carried by UNVERIFIED and PLAN INFERENCE markers (V1:30-32).
8. Stop and escalation rules (V1 6.5, V1:596-613) and the "What may run today" list (V1 5.2, V1:514).
9. X-014 position (no new coordinator clock; WC-16 re-arm duty), **subject to** Round 3 INV-010, where all three advocates rated the probe finding VALID and turned "no extra scheduler" into an owner question (see M-24).

### Strengths to Incorporate from Non-Base Variants

From V2 (opus-analyzer; 11 outright debate wins):
1. Edge kinds with per-edge evidence (FILE, PIN, GATE, DEC, PROC, SOFT), 70 numbered edges (V2 4.2, V2:364-439; S-003 86.3%, U-004 88.0%). V3's advocate asks for an explicit old-to-new id map when the edges are re-keyed onto V1 ids (round2-rebuttal-V3 item 11; S-002 id collisions).
2. INV-008 regression test detail: `core.fsmonitor` hook, `filter.probe.clean`, `* filter=probe`, F2 `unscanned` falsifier (C-001 88.0%), widened by INV-004 below.
3. TB-1 / TB-GIT edge before JOIN: the sweep is not run for the join comparison before the INV-008 fix is in the code being run (X-002 94.3%).
4. "Observe:" verification commands in every acceptance criterion and the OBS-NOW evidence basis (C-011 81.0%; V2:46, 75).
5. Correct package facts: both task packages exist and are listed as inputs (X-001 98.3%).
6. #423 research split: ungated research early, gated brainstorm later (C-006 90.3%, X-008 90.7%).
7. Q14 gate read as the owner's wording plus a conditional SW-13 `working` class (X-009 81.0%; Weak point W5).
8. No hard contract-note predecessor on the guard flip (X-007 86.0%).
9. Weak points W1 to W6, without W7 and W8, which the debate withdrew under X-005 (U-005 80.7%).
10. Verified worktree map (V2 6.2; SC-27) and the "Check" column per invariant (V2:616-646).

From V3 (haiku-backend; 4 outright debate wins):
1. Interface, failure, retry and idempotency contracts per system: sweep, snapshot, issue edit, PR merge (V3:116-118, 142, 283, 285; U-010 85.0%).
2. Two-scope independent gate: a first-release PASS is never relabelled end-to-end PASS (XC-08, V3:246-248; U-011 87.7%).
3. "Decision lifetime" and "Authority not granted by these questions" (V3:321-323; U-012 87.7%).
4. ADJ live facts treated as historical and re-read at W0 and at each gate (A-007 85.0%; V3:466, 656).
5. Wave interruption rule and the "expired wait is not an exit gate" rule (V3:464-468), requested in all three advocates' fix lists.
6. Role contract keeping external writes with the coordinator, not item workers (V3:502-512), the starting point for the INV-001 fix.
7. Read-capture versus seed-test consent split (V3:460, rule 8).

MERGE points (17) and NEITHER points (3: X-011, X-015, A-002) are not variant wins; their agreed content is in the evidence column of the `debate-transcript.md` Scoring Matrix and goes to the refactor plan from there.

### Must-fix list for the V1 base (named here, not decided)

The refactor plan decides each item. Sources: the three advocates' minimum-fix lists (`round2-rebuttal-V1.md`, `-V2.md`, `-V3.md`, section 6; V2's list was written for a V2 base, so only its items that apply to V1 are listed) and the Round 3 invariant rules (`round3-invariants-V1.md`, `-V2.md`, `-V3.md`) for probe findings INV-001 to INV-016. Work-item ids are V1's unless stated.

Round 2 minimum fixes:

| Id | Fix | Named by |
|---|---|---|
| M-01 | X-002: TB-GIT -> XC-04; JOIN only after F1/F2 is in the code run, or Q1 = F3 recorded (timing revised by M-17) | V1 #1, V3 #1 |
| M-02 | X-011 / A-002: per-PR owner go-ahead in the ledger covers pr-submit's push, reply and resolve on that PR only; merges, issue posts and the #539 Codex-thread INV-008 reply stay owner-approved (replaces V1 6.3 and 6.9 wording; shape set by M-25) | V1 #2, V2 #4, V3 #3 |
| M-03 | X-012 / A-005: where the decision ledger and program files live; #539 commits stage named files only (home disputed, see M-14) | V1 #3, V2 #5, V3 #4 |
| M-04 | X-001: both task packages exist; list them in V1 6.1 inputs (fixes V1:57) | V1 #4, V3 #5 |
| M-05 | X-007: drop OB-06's hard XC-05 edge; keep (e) disjunctive | V1 #5, V3 #6 |
| M-06 | X-008: split V2-03 into ungated research and gated brainstorm | V1 #6, V3 #7 |
| M-07 | X-009: V2-02 passes only if every part of Q14's gate is met; add conditional SW-13 | V1 #7, V3 #7 |
| M-08 | A-003 / A-004 / A-007: W0 exit names the #539 author session and confirms the Q24 runner or records the default; ADJ live facts labelled "as of ADJ" and re-read | V1 #8, V2 #12, V3 #5 |
| M-09 | Resume: import V3's wave interruption and evidence-handoff rules into Section 6 | V1 #9, V2 #13, V3 #10 |
| M-10 | X-015: fix V1's register and wave mismatches (IC-V1-1, IC-V1-2) and re-check every wave row against its hard edges | V1 #10, V3 #11 |
| M-11 | C-001: SW-02's regression test takes V2's detail (widened by M-16) | V1 #11, V3 #2 |
| M-12 | X-013: the owner merges #541 or records approval for a named merger | V2 #8, V3 #3 |
| M-13 | X-004 / C-010: log follow-ups early under publication authority, keep source edits post-merge, retain clause-level gates | V3 #8 |
| M-13a | C-005: fold CO-01's Q4 line into the single Coder#477 reply (written for V2; check whether V1's CO items need it) | V2 #10 |

Round 3 invariant rules (probe INV-001 to INV-016; the probe's HIGH and UNADDRESSED set is INV-001 to INV-005):

| Id | Probe finding | Rule proposed | Advocate verdicts (V1 / V2 / V3) |
|---|---|---|---|
| M-15 | INV-001 PR actor | pr-submit runs only in a top-level session (the coordinator or a named person-opened PR session), never in a `worker-start` worker (`WORKER-CONTRACT.md:23`, `:243`). V1 splits each PR item into worker work plus a coordinator-launched PR session; V3 hands back to an owner-designated top-level PR session. Replaces V1:575 | VALID / VALID / VALID |
| M-14 | INV-002 coordinator home and ledger branch | **Disagreement to settle:** V1 and V3 rate it PARTLY (an owner-selected existing checkout, or one a human creates, is allowed; record the branch that stages the ledger); V2 rates it VALID (the main checkout is the only rule-conforming home; two owner decisions) | PARTLY / VALID / PARTLY |
| M-16a | INV-003 hard order versus defaults | Skip rule in XC-02: a link defaulted to "not posted" is recorded as skipped and the next link becomes eligible; V3 adds that a withheld slot does not satisfy content dependencies | VALID / VALID / VALID |
| M-16 | INV-004 regression test scope | Widen SW-02's test and TB-GIT beyond the two keys to `filter.<driver>.process`, and state whether `include.path` and inherited `GIT_*` env are in scope; no code fix named (INV-008 stays with the owner) | VALID / VALID / VALID |
| M-18 | INV-005 pr-submit on #539 | No `/sc:pr-submit` at `--monitor 2` or `3` on #539 until the Q1 ruling is applied (V1 also requires the Codex thread resolved by the #539 author under that ruling; V2 keeps the Codex INV-008 thread excluded from the tool even afterwards and allows `--monitor 1` before) or all security-remediation scope is authorized (V3) | VALID / VALID / VALID |
| M-19 | INV-006 `/sc:sweep` availability | Replace "install or `make sync-dev`" with an exit check that `superclaude sweep --help` works in the coordinator's CLI; until then the WC-16 sweep duty is recorded as not runnable | VALID / VALID / VALID |
| M-17 | INV-007 JOIN runner and place | V1 and V2 move JOIN to after the #539 merge, run from a master-based checkout by the Q24 runner (V1 says this reverses its Round 2 position); V3 also allows the authorized #539 owner to run it pre-merge in that checkout | VALID / VALID / VALID |
| M-20 | INV-008 OB-04 target Run | OB-04 names an owner-approved holder-terminal Run that is not the alignment coordinator's own | VALID / VALID / VALID |
| M-21 | INV-009 Orca not running | Stop trigger "Orca app not reachable": hold live lanes, record it in the ledger, keep bounded supervision, ask the owner | VALID / VALID / VALID |
| M-24 | INV-010 extra scheduler | Owner question whether the 2026-11-05 cron order applies; replaces the categorical "no extra scheduler" (affects preserved strength 9) | VALID / VALID / VALID |
| M-22 | INV-011 F3 caveat coverage | Under F3, caveat every "read-only" claim found by a grep at ruling time, plugin mirror included, not four texts | VALID / VALID / VALID |
| M-23 | INV-012 SW-02 plan package in #539 | All three read A-004 as "no new program, collector, JSON key or sidecar", so a plan package is not barred outright; state where the package lives and record it | PARTLY / PARTLY / PARTLY |
| M-25 | INV-013 approval shape | Replace a single M-APPROVAL boolean with approval rows keyed by PR or issue and action (push-reply-resolve, draft toggle, merge, issue write, live test), each with a lifetime; governs how M-02 adds M-APPROVAL | VALID / VALID / VALID |
| M-26 | INV-014 pr-submit's full write list | The per-PR approval row lists every write the tool makes (create or attach, push, reply and resolve, review re-trigger comments, draft toggle), or the run is held | VALID / VALID / VALID |
| M-27 | INV-015 worker commits | Either quote the owner's per-Task local-commit wording in the brief (WC-9), or workers leave changes uncommitted and the PR session or coordinator commits | VALID / VALID / VALID |
| M-28 | INV-016 TB-GIT as a ledger row | TB-GIT checked before every sweep run; the four existing `.dev/sweeps/` reports marked as not JOIN evidence | VALID / VALID / VALID |

Not covered by Round 3 and left to the refactor plan to triage: probe findings INV-017 to INV-028 (`invariant-probe.md`, Summary), including INV-018 (the INV-008 security ruling), which stays UNRESOLVED-EXTERNAL with the owner in every variant.
