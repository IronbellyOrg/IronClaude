# Round 1 statement: V5 advocate (sonnet, performance lens)

## Position summary

V5's lasting contribution is not a single design. It is the accounting: each gain is split into harness, prompting and collaboration shares; the static-kit control shows communication must beat a free checklist; and every time budget treats the critical path as the slowest reviewer, where any wait breaks the cap. On mechanisms, V4 has the best cores in three families and should be the base document. V5 supplies one core (F5) and the grafts on time, cost and evidence.

## Steelman and critique of each other variant

### V1 (architect)

**Steelman.** V1 has the best theory and enforcement. Its T1 refinement says the two halves of the missing move sit in different models: haiku and ember search, luna reads (V1:25-45). That is the only theory that predicts a gain a static checklist cannot copy, and it licenses the whole F4 family. Its panel deadline `PANEL_FINISH_AT = T0 + 1.20 x B` (V1:138, U-001) is the only panel-level mechanism that makes +35% enforceable for mid-run designs. It also holds the grading rubric constant in every arm (V1:111). Its harness fix H2 truncates, validates and re-asks once (REQ-H2, H3), so the merge parser is untouched and nothing is dropped. V1-R2's evidence trail needs no model action at either end (U-002).

**Critique.**
- V1-R3's hard cap is `1.35 x T1` of the same run (V1:323), not 1.35 x the named 116 s baseline. Phase 1 runs with the longer A2 brief, so T1 can grow, and the "+35%" guarantee floats with it.
- Arithmetic. V1-R2 claims an I7 high of 0.35, but its own chain gives 0.45 x 0.7 x 0.85 = 0.27, and the hash split means only one luna gets the file (V1:279). V1-R4's rows sum to 0.12-0.60, minus up to 0.10 for displacement, which gives 0.02-0.60, not the stated 0.05-0.45 (V1:426-432). I recomputed both.
- Performance. R3 resumes the whole session history as input tokens (V1:376), and V1 does not count that cost. R5 rests on cross-session `SendMessage` from gateway models, which is unverified at both ends (V1:469-473).
- V1's experiment makes found /14 the primary endpoint at n = 6, where V1 itself says only about +1.0 per run is detectable (V1:599). That is larger than any design's central estimate.

### V2 (analyzer)

**Steelman.** V2 is the most careful about contamination and statistics. Decoys (1 of 3 challenges at a place no peer flagged, V2:240) are the only defence against the location-as-signal leak (A-006). Every other F1 design, mine included, sends real peer anchors bare. V2's schema forbids free text and requires `target.quote` to be a located verbatim substring (V2:116-131). Its decision rule is statistically correct: 4/6 vs 0/6 gives p = 0.030, and I confirmed it. The rule also requires beating A2 by 2 runs (V2:526) and confirming on two new packages (V2:531). Judging the sealed reports under separate labels (R-25, R-28) measures collaboration within the same run, at the cost of judge calls only.

**Critique.**
- V2-D1's prose says a luna that stops at 135 s gets no locators. Its own formula gives 0 from t = 128 s (V2:182). R-20's unit test (100/125/140 s) is consistent, so this is a prose error. More serious: the I7 high of 0.60 exceeds the single-luna chain 0.9 x 0.8 x 0.6 = 0.43, and the lunas receive disjoint locators (V2:159).
- D3 has no harness time box (V2:317), so the cap is measured, not enforced. That is unacceptable on the performance lens.
- D4 and D5 sit on sonnet panels (274 s, 225 s). D5's S14 baseline is not in the seed list.
- D2 waits for a report "from a reviewer of a different model", so ember idles until about 102 s.

### V3 (backend)

**Steelman.** V3 is the leanest and the easiest to build: R2 is about 90 lines and R5 adds +4% elapsed (V3:120). It contributes three cheap audits the merge should keep:
- the 12-character anchor-substring leak check (V3:88, U-009);
- an extension rule from 10 to 20 runs (V3:160);
- a fourth unseen package before any product change (req 21).

It is also the only variant that names `--disallowedTools` as the read-only mechanism (req 1).

**Critique.** V3's designs cannot be merged as written:
- **Collaboration findings are never scored.** Req 6 puts collaboration output outside the fenced block (V3:176), so the merge never sees it and every gain would score zero (X-006).
- **I7 is counted on the /14 scale** in R1, R3 and R5 (V3:78, :100, :122), against SEED:22.
- **The harness share of 0.8-2.1** (V3:126) has a low end above every other variant's high end. Its +0.3-0.8 for naming source.md contradicts the evidence that cheap readers of source.md still missed B5 and I1 (V2:144).
- **The 14 s "harness overhead"** (V3:69) misreads the slowest-of-two luna draw (X-005).
- **The absolute 0.5 Jaccard alarm** (V3:77) sits next to the haiku pair reference (0.47), so it fires on noise in haiku panels and never fires in luna+ember panels (0.25).
- **No static-catalogue arm**, so V3 cannot tell content from exchange (X-010).
- **Four of five gain tables do not follow from their inputs.** For example, R1's 5 x 0.6-0.9 x 0.15-0.4 = 0.45-1.8, not 0.4-1.2.

### V4 (devops)

**Steelman.** V4 is the most complete and most operable specification:
- **Move Radar (V4-1)** infers moves from tool-call telemetry. No model writes anything, which removes the gateway-compliance risk that sinks most F3 designs.
- **Axis-Flip Challenge (V4-3)** seals phase 1 by process exit, filters surface findings, routes the move by anchor content, and has correct arithmetic: 116 + 32 = 148 s (+27.6%).
- **Coverage Deflection (V4-5)** is fully harness-authored and lands in a Claude receiver.
- **Operations.** V4 adds a kill switch with a byte-identical launch command (R-05), per-package `collab.json` telemetry, an SLO error budget (R-23, R-24), the board path baked into hook commands (U-013), and failure runbooks per design.
- **Alarm.** Its convergence alarm, ledger rows falling 20% (R-25), needs no ground truth, so it also works in the product.

**Critique.**
- **V4-2 breaks the cap.** The worst case is 116 + 6 + 38 = 160 s = +37.9%. The 125 s delivery deadline cannot bind, because it limits when facts arrive, not how long luna works on them. The 15 s Stop hold (V4:287) adds more. My performance rule fixes this: luna acts on at most 2 facts and never waits (V5:297), so the worst case is 148 s.
- **V4-3's phase-2 timeout disagrees with itself.** The schedule says 45 s (V4:375), section (d) says 35 s for luna (V4:396), and R-15 reconciles the two only afterwards.
- **n = 4 per arm is a screen, not a test** (V4:667). The decision would rest on two or more reach runs out of four.
- **R-24 applies a per-package cap to a mean of three packages** (A-005).

## Strengths claimed

1. **Clean arithmetic.** The grid marks Time = Y for all five V5 designs, and every gain total is correct (D1 0.21, D2 0.178, D3 0.2285, D4 0.16, D5 0.275); I re-added D1-D3 row by row. Only V4 matches this on gains, and V4-2's worst case is over the cap.
2. **A static-kit control and a three-way gain split.** Gains split into harness (A1-A0), prompting (A2-A1) and collaboration (arm-A2) (V5:141, E-5; C-009). The table adds a net-collaboration column, a static-kit row and a sonnet reference row (V5:404-413; S-004). This puts a number on X-010: the kit's gross 0.33 beats every exchange design, so communication must beat A2 (V5:418-419).
3. **Cost per issue and scaling.** c (sum 1.04) is capped against sonnet + 2x luna's measured hard reach of about 1.0 per run (V5:94, U-015). "Output tokens per added issue" is the only cost-to-serve figure in any variant: the sonnet reference costs about 150k, the cheap designs 47-100k. Every schedule states its scaling with n, because a fact computed once costs O(1) and redone by every reviewer costs O(n) (V5:58).
4. **No waiting on the critical path.** "Luna must never wait for a result. A 15 s wait would add 15 s and break the cap" (V5:297). This rule catches V4-2's 15 s hold.
5. **Shadow scheduling.** V5-D5 runs phase 2 while a slow member is still working: +0% on haiku + 2x luna, worst case +6%, with a 15 s kill rule and haiku as an isolated canary (V5:385; U-016). It is the only F1 schedule with no elapsed cost.
6. **First-hand evidence.** A peer fact may be cited only if the receiver re-ran the command, and a re-run mismatch above 10% stops the arm (V5:299, C-3; U-017). This is the only guard against a peer's faulty sweep spreading as evidence.
7. **Checked facts and cheap spikes.** `--max-turns` is absent from `claude --help`, so turn caps need a hook counter and `timeout` (V5:106). Spike 5 re-scores the 30 cheap runs with the normalizer for judge calls only (U-018).
8. **Experiment size.** A1 and A2 get 12 runs each; exchange arms get 6, extended to 12 after an interim look; run order is block-randomized (V5:437-454). That is the largest control sample of the five variants.

## Concessions (own weaknesses)

1. **The Fisher clause in my decision rule is wrong (X-013), and I confirmed it.** For 4 of 6 runs against 1 of 6: P = (C(6,4)C(6,1) + C(6,5)) / C(12,5) = 96/792 = 0.121. At n = 12 the same comparison gives 6,732/42,504 = 0.158. Both are above my threshold of 0.10. My power note is right: 4 of 12 against 0 of 12 gives 495/10,626 = 0.047. **Fix:** replace the clause with V2's rule (V2:526).
2. **The free-text `note` field (X-007).** A 120-character note filtered only for verdict words can still carry a conclusion. **Fix:** drop the field and adopt V2's closed schema.
3. **H-4 and H-6 change the judging (X-008).** H-4 asks reviewers to write MINOR notes, which is a rubric change hidden inside "harness". H-6 also contradicts my own E-3, which says the judge's inputs contain only the merged report. **Fix:** move H-4 out of the bundle. Keep H-6 only as a secondary score, as V2 does with sealed-report judging.
4. **A call-6 gate leaves no record of the first pass (C-006).** **Fix:** use V4's seals: the exited phase-1 process for phase designs, and `panel-seal` with its `seal_missing` runbook for mid-run designs.
5. **Internal mismatches (grid).**
   - D2 caps each reviewer at 2 injections in, but the time block counts 5 ember flips (V5:224, :236). The real ember maximum is 4. ember is off the critical path, so elapsed time does not change.
   - D4 says ember waits at most 70 s (V5:318), but its time row uses "up to about 102 s" (V5:338). With the 70 s wait, ember ends at 41 + 70 + 9.6 = 120.6 s.
   - D2 credits B1 using a 0.61 anchor rate at the Task level (V5:250). That contradicts my own T2b claim that zero findings anchor AC3 (V5:40). V1's 0.00-0.10 is the honest figure (X-011).
6. **I contradict myself on idle time (A-002).** D1 and D4 need the move codes in the brief, which is the kit, yet their budgets start from 116 s. My own estimate puts the kit alone at +29% (V5:411). A kit-plus-exchange arm could therefore exceed +35% against A1. **Fix:** re-derive every budget from A1's and A2's measured times (spike 4) before the arms run.
7. **The 0.25x to 2x band (C-008) is a fixed multiplier, not a per-issue range.** V4's per-issue chains are better. Only my D2 has per-issue rows.
8. **My experiment cannot detect my own central estimates.** Net collaboration shares are 0.05-0.14, but only about +0.3 per run is detectable (V5:463). The likely result, "not distinguishable from A2", still decides kit against transport.
9. **Sweep Desk depends on lunas posting requests**, and lunas search `tests/` in only 4% of runs (V5:309). V4-2's push model is the better F4 core.

## Shared assumptions

A-001: QUALIFY. Delivery is tested by spike; the act rate (0.5-0.85) is not. Use V1's REQ-S3, which checks that the next tool call follows the injected text, measure the act rate for ember and luna, and put the measured value into every gain chain.
A-002: REJECT as stated. Idle windows measured before the fixes do not hold once H1 and the catalogue lengthen runs. Re-derive every budget from measured A1 and A2 times, and cap against A1 (V5:459).
A-003: QUALIFY. Keep the judge unchanged. Add V2's sealed-report judging and report findings per report as a covariate, so that "more findings, more chance credits" can be seen.
A-004: REJECT. The shares interact (M4 and M6 pay off only after H1 and H3, V4:184). Report measured arm differences (A1-A0, A2-A1, X-A2), never a sum of separate estimates.
A-005: QUALIFY. Dividing the three-package total by 3 is a placeholder. Check it against per-run `wall_s`, and apply the cap to per-package medians, not to a mean (V5:23, :539).
A-006: REJECT. A real peer anchor tells the receiver that a peer found something there. Every F1 design needs V2's decoys and V1's gap card.
A-007: QUALIFY. `--resume` appears in `--help`, but gateway ids are untested. Gate on spike S2 and use V4's fresh-session fallback, logged as `resume_fallback`.
A-008: QUALIFY. Read-only is policy, because Bash is unrestricted. Keep `--disallowedTools` (V3 req 1), have helpers write only under `$BOARD`, and check that the sandbox `git status` is clean after every run (V4 R-09, V2 R-5).
A-009: QUALIFY. Any gain is in-sample. Confirm it on unseen packages before adoption (V2:531; V3 req 21).
A-010: ACCEPT. ember + 2x luna is the replicated, cheapest default. Second stages use haiku + 2x luna or sonnet + 2x luna.
A-011: QUALIFY. The rates are judgment, with V5's c capped against SL2's measured reach as an upper bound. Replace them with rates measured in the first experiment.

## Proposed final slate of five redesigns

Every slot also takes the shared grafts:
- V1's panel deadline (U-001), measured against the **named** baseline B;
- V4's board path baked into hook commands (U-013), kill switch and `collab.json`;
- V5's first-hand evidence rule (U-017) and the "no wait on the critical path" rule;
- V2's closed schema (no free text);
- one relative alarm: Jaccard above the isolated arm + 0.15, OR ledger rows down 20%, OR echo above 30%.

| Slot | Family | Core | Grafted parts | One-line reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 | V2-D2 decoys (1 of 3); V1-R3 gap card for a region nobody anchored (the T2b route to B1/B2); V5-D5 shadow schedule and isolated haiku canary as the haiku + 2x luna variant (+0%, worst +6%); luna phase-2 timeout fixed at 35 s | Most reliable design: sealed by process exit, no hooks, 148 s = +27.6% on ember + 2x luna; decoys close A-006, and the shadow variant costs no elapsed time |
| 2 | F3 Content-free coverage steering | V4-1 | V5-D4 end-of-run Stop block assigning one unapplied move by cost class with a rotating permutation (replaces the second checkpoint, so the cap stays at 2 moves); V1-R1 per-receiver hash ordering of gaps; V4-5 surface filter | Zero model authoring (telemetry), +24% with worst = expected; the rotation stops all three reviewers taking the same gap |
| 3 | F4 Searcher-to-reader fact relay | V4-2 | V1-R2 automatic harvest of seen-but-unopened paths as a second fact source; V2-D1 disjoint hash split between the two lunas; V5-D3 command string on every fact plus the re-run mismatch alarm (>10%); **the 15 s Stop hold is dropped and each luna acts on at most 2 facts** | Fixes V4-2's over-cap worst case: 116 + 6 + 26 = 148 s = +27.6%; the only strong T1/I7 path for the cheap panel, and it uses ember's idle time |
| 4 | F5 Structural index | V5-D1 | V1-R4 disjoint luna lenses (lowers Jaccard by construction); V2-D5 source-rule entries (source.md normative lines with no plan counterpart) as an added index kind | Computed once and delivered to n-1 reviewers; 143 s = +23.3%; the source-rule kind is the only route to the B5/I1/B2 defects hidden by the post-implementation checkout |
| 5 | F6 Steering a running strong model | V4-5, moved to the seed baseline sonnet + 2x luna (274 s, cap 369.5 s) with the two lunas as scouts | V2-D4 (Task x move) uncovered-cell grain in the card; V1-R5 brief line "a region a peer covered is not cleared" | Harness-authored, Claude receiver (lowest hook risk); 274 + 28 = 302 s = +10.2% typical, 330 s = +20.4% worst; uses a seed baseline instead of the non-seed S14 |

F2 (V5-D2) is left out because it is a mid-run copy of slot 1's mechanism. F7 (V4-4) is left out because two-way gateway compliance plus a Stop hold costs more risk than F6.

`Proposed base document: V4`. It has the most complete shared substrate (catalogue with best-style routing, baked board path, kill switch, SLO, runbooks), clean arithmetic in three of the five slot cores, and requirement tables with a verification column. Its theories and requirements carry over as they stand. Its experiment section must take V5's arm sizes (A1 and A2 at 12 runs, exchange arms 6 extended to 12) and three-share report, plus V2's decision rule and within-run sealed judging.

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | Each element is a table, plus a failure runbook (detection, action) per design |
| S-002 | V4 | Most complete scaffold: catalogue with style routing, baked board path, kill switch, timing and baseline tables |
| S-003 | V1 | Issue-to-theory map with a "generic move" column ties each miss straight to a design |
| S-004 | V5 | Only table with a net collaboration share, tokens per added issue, a static-kit row and a sonnet reference row |
| S-005 | V4 | R-01..R-30 tables with a verification column per requirement, tied to the chosen designs |
| S-006 | V5 | Itemises every numeric assumption the numbers rest on (turn time, hook cost, act rate, resume start, base commit) |
| C-001 | V1 | "Two halves in different models" is the only T1 refinement that predicts a gain a checklist cannot copy |
| C-002 | V5 | The T2a/T2b split separates anchored near misses (B5, I1, I5) from unvisited regions (B1, B2, I4), which need different cures |
| C-003 | V1 | Four named fixes only, grading held constant, H2 = truncate + validate + re-ask without editing the parser |
| C-004 | V4 | M1-M10 with a best-style column enables routing by style; adopt it as the canonical numbering |
| C-005 | V2 | 400-byte lines, verbatim located quote of at most 120 characters, explicit forbidden keys: the tightest schema |
| C-006 | V4 | Phase designs are sealed by process exit; mid-run designs by `panel-seal` with a `seal_missing` fallback; both auditable |
| C-007 | V4 | Relative Jaccard + 0.15 OR ledger rows down 20% needs no ground truth and works in the product |
| C-008 | V4 | Per-issue chains stated for each design and arithmetically consistent |
| C-009 | V5 | The harness / prompting / collaboration split is the only way to report the required collaboration-vs-harness shares |
| C-010 | V5 | Static-kit arm plus A1/A2 at 12 runs, an interim look and block randomisation |
| C-011 | V2 | Reach with a correct Fisher threshold, plus a margin over A2 and confirmation on new packages |
| C-012 | V5 | Every design sits on a seed baseline (EL2, HL2, SL2), with per-package caps tabulated |
| C-013 | V1 | The panel-level finish signal at T0 + 1.20 x B is the only enforcement for mid-run designs |
| X-001 | V2 | +0.1 to +0.5 with a per-fix basis and explicit evidence that naming source.md alone does little |
| X-002 | V2 | States both scales correctly: 0 on /14, 0 to -0.33 on control for sonnet panels |
| X-003 | V1 | Cites GT6 = I1 for `merge_guard.py:256`, matching SEED:71 |
| X-004 | V5 | Uses haiku legally against its own HL2 baseline and turns its slowness into free phase-2 time |
| X-005 | V1 | The slowest-of-two luna at 116 s is the correct reading of SEED:98 |
| X-006 | V4 | One findings-v1 block, P2-F ids, `origin` stripped before judging |
| X-007 | V2 | No free text at all; V5's `note` field is conceded |
| X-008 | V1 | Grading held constant in every arm; the rubric change is deferred and named |
| X-009 | V1 | Truncate, then validate, then re-ask once: no parser edit and no residual drops |
| X-010 | V5 | Puts a number on why communication must beat the static kit (gross 0.33 against net 0.05-0.14) and makes A2 the comparator |
| X-011 | V1 | Zero AC-level anchors, so B1/B2 need a gap-card route; 0.00-0.10 is the honest range |
| X-012 | V1 | I7 kept on control /2 throughout, stated up front |
| X-013 | V2 | Its Fisher claim (0.030) recomputes correctly; V5's clause fails at 0.121 and 0.158 |
| A-001 | V1 | REQ-S3 tests that the next tool call follows the injection: the act rate, not just delivery |
| A-002 | V5 | The only variant that estimates the kit's own time cost and plans spike 4 to remeasure |
| A-003 | V2 | Sealed-report judging under random labels gives a within-run control for judge comparability |
| A-004 | V4 | States the interaction (M4/M6 need H1/H3) and applies H in both arms |
| A-005 | V5 | Marks the divide-by-3 as unverified and requires a check against per-run `wall_s` |
| A-006 | V2 | Decoys are the only defence against the location-as-signal leak |
| A-007 | V4 | Spike S2 plus a logged fresh-session fallback |
| A-008 | V4 | Helpers write only under `$BOARD`; sandbox `git status` is verified clean |
| A-009 | V2 | Requires confirmation on two new packages with ground truth from implement history |
| A-010 | V1 | States why: the replicated default, the cheapest, and where cheap-model collaboration matters most |
| A-011 | V5 | c is capped against SL2's measured hard reach, an explicit external upper bound |
