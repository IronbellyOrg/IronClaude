# Round 1 statement: V4 (devops lens)

Citations: `V<n>:<line>`, `DA:<line>` for `diff-analysis.md`, `SEED:<line>` for the seed brief. I recomputed all V4 arithmetic below myself.

## Position summary

V4 should supply the merged spec's scaffolding: the kill switch, the board path baked into hook commands, hooks that cannot fail a review, `collab.json` telemetry, the SLO error budget and a runbook per design. It should also supply three family cores that no other variant matches (Move Radar F3, Flag-and-Adjudicate F7, Coverage Deflection F6). V4 does not win everything. V2 should supply the F1 core, the theory gate table and the decision rule. V5 should supply the three-way gain split. V1 should supply the harness fix for long anchors and the panel deadline. V4-2's worst case breaks the +35% cap as written.

## Steelman and critique of each other variant

### V1 (architect)

**Steelman.** V1 is the most disciplined architecture of the five. All designs run as policies on one shared substrate (V1:100), so five designs do not mean five harnesses. Its deadline rule `PANEL_FINISH_AT = T0 + 1.20 x B` (V1:138) is the only panel-level, per-package mechanism that turns +35% from a hope into a guarantee for mid-run designs. In the evidence trail (V1-R2, V1:237) neither sending nor receiving needs the model to act, which removes gateway compliance at both ends. Its H2 truncates long fields, validates them with the real parser and re-asks once (V1:107), so no finding can be silently lost; V4's H2 does not achieve this. It also holds the grading rule constant (V1:111). Spike REQ-S3 (V1:614) is the only spike that checks a gateway model *acts* on injected text, not just that the hook fired. And V1-R3's gap card (V1:303) is the only F1 mechanism that points a reviewer at a region nobody anchored, which matters for B1/B2 (see X-011).

**Critique.** V1-R2's I7 high of 0.35 exceeds its own chain: 0.45 x 0.7 x 0.85 = 0.27 (V1:279; recomputed). V1-R4's stated 0.05-0.45 does not follow from its rows. The rows sum to 0.12-0.60, minus displacement 0.10-0, which gives 0.02-0.60 (V1:426-432). V1-R3's hard kill is 1.35 x T1 of the same run (V1:323), not 1.35 x the named S07 baseline. Phase 1 there also carries the catalogue and H1 (V1:300), so T1 can exceed 116 s and the guarantee drifts. REQ-S2 (V1:613) depends on hooks inheriting environment variables. Baking the board path into the hook command (V4:124) removes that dependency instead of testing it. R1 and R4 depend on gateway models posting cards (V1:540); R5 rests on SendMessage.

### V2 (analyzer)

**Steelman.** V2 has the best theory frame: a three-gate funnel (exposure, question, survival) with a per-issue table naming the blocked gate (V2:83-94). It has the best piece of collaboration evidence: luna read source.md in 48 of 48 control runs, where tasks cite it, against 11 of 48 alias runs (V2:27). That number shows pointers change luna's behaviour. D2's decoys (V2:240, :266) are the only defence against the signal carried by a peer anchor's location ("a peer found something here", A-006). Its time box `min(35, 150 - start - 4)` (V2:251) is anchored to panel start, so it binds against the named baseline. Its decision rule uses a correct Fisher threshold (4/6 vs 0/6, p = 0.030; recomputed). Within-run attribution (V2:517, R-28) judges sealed reports separately, which measures collaboration without a separate arm. R-17 (V2:563) catches a real pitfall: a resumed prompt must not start with a slash command. Its confirmation step uses two new packages (V2:531).

**Critique.** D1's time guard is wrong as stated: `min(2, floor((150 - t - 12)/11))` is already 0 at t = 128 s, not 135 s (V2:182; recomputed). D1's I7 high of 0.60 exceeds the single-luna chain 0.9 x 0.8 x 0.6 = 0.43, and the lunas get disjoint locators (V2:159), so "two lunas" cannot double it. D1 also assumes a Stop block yields a reissued full report (V2:172), which is unverified; if it fails, the fallback discards the gain. D3 has no harness-side time box (V2:317), no send validation and no durable log. D4 depends on luna calling `panel-cover`, but luna makes about 1 Bash call per run (V2:414). D2's flip table routes on the peer's category, while V4-3 routes on anchor text (V4:349-354). Anchor-text routing sends a grep sentence to M4/M7, the moves the 16 I5 near-misses lacked.

### V3 (backend)

**Steelman.** V3 takes the seed's first ranking seriously: "simplicity and speed of implementation rank first" (SEED:31). Its designs are the shortest to build (50-175 lines). It contributes a cheap mechanical leak check: no board line may contain 12 or more characters of another reviewer's anchor (V3:88). It adds an extension rule (10 to 20 runs) for borderline results (V3:160), a double-scored judge sample and a mandatory unseen fourth package before adoption (V3:191). Its first-pass seal (`pass1.md`) is an auditable artifact (V3:56).

**Critique.** Requirement 6 places collaboration findings outside the findings-v1 block (V3:176), so the merge and the judge never see them and every collaboration gain would score zero. It also contradicts R1 (V3:73). I7 is counted inside "/14" (V3:78, :100). The harness share of 0.8-2.1 (V3:126) exceeds every other variant's high end, and the seed's own data contradicts it: cheap readers of source.md still missed B5 and I1 (V2:144). The 14 s "fixed overhead" (V3:69) misreads the baseline. 116 s is the slower of two luna draws, not luna's 102 s median plus overhead. The gains do not follow from their inputs: R1 is 5 x 0.6-0.9 x 0.15-0.4 = 0.45-1.8, but V3 states 0.4-1.2. V3 also says `merge_guard.py:256` repairs B5; it repairs I1 (SEED:71). The absolute Jaccard alarm of 0.5 sits just above the ember+haiku reference of 0.47 (V3:77), so it fires on noise in haiku panels and never fires in luna panels. There is no static-catalogue arm, so V3's experiment cannot separate the move list from the exchange. Finally, `pass1.md` must be written through Bash, which V3's read-only rule (req 1) does not restrict.

### V5 (performance)

**Steelman.** V5 is the most intellectually honest variant on the core question. It estimates that a static move kit in the brief may beat every exchange design on gross gain (V5:411, :418), and it builds the experiment so that communication must beat that kit. Its three-way split (harness A1-A0, prompting A2-A1, collaboration arm-A2; V5 E-5) is the only gain decomposition that answers SEED:102 cleanly. The T2a/T2b split (V5:40) correctly reads the B1/B2 evidence: Task 1 is anchored, AC3 never is. Shadow Resume (V5-D5) gets +0% elapsed with an isolated haiku canary, which uses idle time well and gives a clean within-run reference. The first-hand evidence rule (V5 C-3, :299) stops a bad peer sweep from spreading as evidence. V5 also verified `--help`: `--max-turns` does not exist, so turn caps need a hook counter or `timeout` (V5:106). Its spike 5 re-scores the 30 cheap runs to measure the 200-character drop directly (V5:433).

**Critique.** The pass path "at least 4 runs vs at most 1 for A2 (Fisher p <= 0.10)" (V5:457) cannot be met. One-sided Fisher for 4/6 vs 1/6 is 112/924 = 0.121; I recomputed it. A `note` of up to 120 characters is filtered only for verdict words (V5:117-119), so "grep misses root files" passes and carries a conclusion (X-007). H-4 (MINOR notes) and H-6 (judge scores the raw union) change the rubric and the judge input, yet are counted in the "harness share" (X-008). The independence gate is a call count (C-1), not an artifact. The 0.25x/2x band (V5:139) is fixed, not derived per issue. D2's caps conflict: "2 injections in" (V5:224) against 3-5 flips in its time block (V5:236-237).

## Strengths claimed

1. **Operability scaffold no other variant has.** V4's scaffold has these parts:
   - `PANEL_COLLAB=0` gives a launch command byte-identical to today's (V4:139, R-05), so every arm can be rolled back.
   - The absolute board path and reviewer id are baked into the hook command strings (V4:124, R-21), which resolves SEED:93's UNVERIFIED env-inheritance item by design (U-013; V5 B-2 later adopted the same rule).
   - Hooks exit 0 and log on any error (R-22).
   - Per-package `collab.json` has a fixed field list (R-23).
   - An SLO error budget of 1 package in 12, with `SLO_BREACH` above 1.5x (R-24).
   - Board directories are kept and quarantined in place (R-26).

   The merged spec needs all of these regardless of which designs win.
2. **A failure runbook per design** (detection, then action), for example V4:264-270, :333-339, :529-535 (S-001). Each failure mode has a numeric trigger and an action. For example, `seal_missing` above 50% switches the delivery rule (V4:335), and `cards_sent = 0` in more than 50% of runs stops the arm (V4:531).
3. **The lowest-compliance designs in their families.**
   - V4-1 infers moves from tool-call telemetry, so no model authors anything (V4:204; U-012).
   - V4-5's cards are generated by the harness and received by a Claude model (V4:565).
   - V4-3 needs no hooks (V4:446).

   By contrast, V1-R1, V1-R4, V2-D4, V3-R2, V3-R5 and V5-D2 all need gateway models to author posts, and HO2:195 shows these models break stated format rules.
4. **The surface-finding filter** (V4:345, :563; U-014). It keeps luna's Task 12 artifact objection, present in 91% of luna control runs, from counting as coverage or as a challenge source. Any coverage or flip design needs it.
5. **A convergence alarm that needs no ground truth.** `CONVERGENCE` fires when pairwise Task Jaccard exceeds the isolated mean + 0.15 or when ledger rows fall 20% below the isolated arm. `ECHO` fires on a design-specific threshold (V4:415, R-25). Because it uses only the ledger, the same alarm can run in production. V5's easy-issue share needs judged clusters.
6. **Sound arithmetic in four of five designs.** The gains of V4-1, V4-3, V4-4 and V4-5 match their rows (DA:90-94). I7 is kept on control /2 throughout (V4:10).
7. **An integrity grep against ground truth.** No board message or digest may contain a ground-truth `plan_quote` substring of 12 or more characters (V4:671, R-07). This is the leak check aimed at the actual answer, not only at peers' anchors.
8. **A direct answer to the seed's open question** ("challenge vs shared findings", SEED:48). V4-4 makes the challenge a mandatory finite-check answer and routes it to a different model by rule (V4:468, :501).

## Concessions

1. **V4-2 breaks the cap; the diff analysis is right.** My own recomputation:
   - The worst case is luna 116 + seal 6 + 3 facts x 2 turns x 6.4 s = 160.4 s, which is +38%. V4:301 claims the 125 s delivery deadline caps it. It cannot, because facts arrive at 55-85 s, long before 125 s.
   - The "typical 142 s" omits the 6 s seal. It is 148 s (+27.6%).
   - The 15 s Stop hold (V4:287) can add more on top.
   - Fix: at most 2 facts per luna, a hook-side seal with no model turn, and the hold bounded by V1's finish signal. That gives 116 + 26 + 2 (hooks) = 144 s (+24%), worst 150 s (+29%).
2. **V4-3's B1 estimate of 0.03-0.15** (V4:421) rests on task-level anchoring (52%), while no finding anchors AC3/O3 (V4:50, my own evidence). V5's T2b reading is correct (X-011). With peer anchors alone, B1's low end should be about 0. Reaching it needs V1-R3's gap card.
3. **V4-3 sends real peer anchors with no decoy** (V4:409). A location alone signals "a peer found something here" (A-006). V2's decoy is the fix.
4. **V4-3's timeout is inconsistent.** It is 45 s in the schedule (V4:375) and 35 s for luna in the budget (V4:396); only R-15 reconciles the two.
5. **V4's H2 only re-asks** (R-02), so after one failed re-ask lines can still drop (X-009). V1's truncate-then-re-ask path is strictly better.
6. **The experiment's n = 4 is a screen, not a test** (V4:667). V2's design (6 per arm, concurrent A0, correct Fisher) should replace it.
7. **Every V4 budget assumes the 116 s baseline survives H1** (A-002). Reading source.md adds turns for the 39% of ember runs that skipped it. Budgets must be re-based on the measured A1 median.
8. **The per-package figure (3-package total / 3) is unstated in V4's tables** (V4:152), and V4-5 uses S14, which is not a seed baseline. V4-5 should re-base on SL2. V4-2's `panel-seal` and V4-4's ember posting both depend on model compliance (C-006).
9. **V4-1's deadline is slightly off:** 157 minus 45 (V4:215) is 112 s, not 110 s; harmless, since 110 s is more conservative.

Two findings in the diff analysis I dispute:
- C-012 says S13 is not a seed baseline. It is one: SEED:25 lists "ember + luna ~300 s".
- A-005 says R-24 applies a per-package cap to a mean. R-24 compares each package with the concurrent A0 median for that same package (V4:735).

## Shared assumptions

A-001: QUALIFY — delivery is spike-tested, but the 0.5-0.85 act rates are not; adopt V1 REQ-S3 (next tool call follows the injection) and replace every gain's act rate with the spike's measured rate.
A-002: REJECT — idle windows were measured before H1 and the catalogue; re-base every budget on the measured A1 median per package (V5 spike 4) before arms run.
A-003: QUALIFY — strip arm markers (V1 REQ-M2, V4 R-10), add V2's sealed-report judging under random labels, and report credits per finding so "more findings, more chance credits" is visible.
A-004: REJECT — shares interact (M4/M6 need H1/H3, V4:184); apply H in every arm and report shares as measured differences (V5 E-5), never as summed estimates.
A-005: QUALIFY — the 3-package total / 3 figure is acceptable for planning only; enforce against the concurrent per-package A0 median (V4 R-24, V2 rule 3).
A-006: REJECT — a location is a signal; adopt V2's decoys, implemented as V1-R3 gap cards, and measure the echo rate.
A-007: QUALIFY — spike-gated with a fresh-session fallback (V4:384, V2:286) and V2 R-17's slash-command guard; the fallback costs about 10 s and must be in the budget.
A-008: QUALIFY — read-only is policy, because Bash is unrestricted; enforce it after the run with R-09 (clean sandbox `git status`, unchanged candidate hash) and a transcript audit for writes outside `$BOARD`.
A-009: QUALIFY — accept only with V2's confirmation on two new packages and V4's ground-truth substring check on the catalogue.
A-010: ACCEPT — ember + 2x luna is the replicated, cheapest default (SEED:25); other panels are measured against their own seed baselines.
A-011: QUALIFY — all rates are judgment; cap the sum against measured sonnet reach as V5 does (V5:94) and label B1, B2, I5 and I6 rows as unsupported by any observation.

## Proposed final slate of five redesigns

| Slot | Family | Core redesign | Parts grafted from other redesigns | Reason |
|---|---|---|---|---|
| 1 | F1 between-phase cross-examination | V2-D2 Axis-Flip Cross-Examination | V4-3 (anchor-text routing table, surface filter, immutable phase-1 lines plus a `P2-F` combiner, haiku variant at +22% of 238 s); V1-R3 (gap card toward never-anchored regions, filling D2's decoy slot, so the decoy also reaches T2b issues B1/B2/I4); V5-D5 (isolated haiku canary in the HL2 variant) | Most reliable family (process-exit seal, no hooks); decoys answer A-006; V2's time box binds against the named 116 s baseline (+25%/+29%) |
| 2 | F4 sweep service | V4-2 Idle-Shift Sweeper (fixed) | V1-R2 (automatic seen-not-opened harvest); V2-D1 (ranked disjoint locators per luna, unnamed tests first); V5-D3 (command string in every fact, first-hand re-run rule, mismatch above 10% stops the arm); V1 finish signal bounding the Stop hold; at most 2 facts per luna and a hook-side seal (144 s, +24%; worst 150 s, +29%) | Only cheap-panel path to I7 and I5 (T1); the sweeper is a fresh session that never sees ember's report, and it runs entirely in ember's idle window |
| 3 | F3 content-free coverage steering | V4-1 Move Radar | V2-D4 (harness-built Task x move cell matrix, giving region-level grain); V1-R1 (gap order hashed per receiver, so the two lunas never get the same gap) | Zero model authoring; directly measures panel blind spots; +24% equals its worst case |
| 4 | F7 directed challenge | V4-4 Flag-and-Adjudicate | V2-D5 (source-rule witness lines become harness-generated cards, so B5/I1/B2 reach does not depend on ember posting); V5-D1 (kind-to-move pairing for flagged sentences); V5 C-3 first-hand rule | The only design testing the seed's challenge question with a mandatory finite-check answer from a different model; on seed baseline S13 (100 s), +19%/+32% |
| 5 | F6 steering a running strong model | V4-5 Coverage Deflection | V1-R5 (per-luna move requests, but rendered by the watcher from finished blocks, not sent with SendMessage); re-based on seed baseline SL2 (274 s): 274 + 28 + 28 = 330 s, +20.4% worst; V5 C-2 (cards lead with uncovered Tasks and never mark a region "fine") | Lowest-risk receiver (a Claude model, cards made by the harness); turns cheap reviewers' finished work into steering for the one model that already sweeps |

Proposed base document: V4. The merged spec's bulk is five complete redesigns plus testable requirements. V4 has the most complete per-design template (a-h plus runbook), the operability requirements (R-05, R-21 to R-26), and three of the five slate cores. Two parts should be imported in place of V4's own: from V2, the gate table (section 1) and the experiment design with its decision rule (section 4); from V5, the three-share split.

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | a-h plus a detection/action runbook per design gives the failure-modes element directly |
| S-002 | V4 | Most complete operational scaffold: kill switch, baked board path, timing constants, baseline table |
| S-003 | V2 | Three-gate funnel with a per-issue blocked-gate table maps theories to designs most cleanly |
| S-004 | V5 | Only table with net collaboration share, a static-kit control row and tokens per added issue |
| S-005 | V4 | Table IDs with a verification column per requirement; easiest to audit |
| S-006 | V5 | Itemised unverified list tied to specific numbers |
| C-001 | V2 | 48/48 vs 11/48 source.md reads is the strongest evidence that pointers move luna |
| C-002 | V5 | T2a/T2b split correctly separates "asked the wrong question" from "never reached" |
| C-003 | V1 | Truncate, then parser-validate, then re-ask; grading held constant |
| C-004 | V4 | The best-style column is what routing in F1, F3 and F7 needs; add V5's c column |
| C-005 | V2 | 400 bytes, quotes located and verbatim, forbidden keys listed, source quotes allowed |
| C-006 | V2 | Natural seal at the first Stop is an artifact that needs no model compliance |
| C-007 | V4 | Relative and ground-truth-free (Jaccard +0.15, ledger rows -20%), so it can run in production |
| C-008 | V2 | Trigger x delivered/acted x survives mirrors the funnel and is per issue |
| C-009 | V5 | Harness, prompting and collaboration shares measured as arm differences |
| C-010 | V2 | Concurrent A0, H, catalogue and two design arms at n = 6 isolate each factor |
| C-011 | V2 | Reach endpoint with a correctly computed Fisher threshold, plus a margin over the catalogue arm |
| C-012 | V1 | Uses only seed baselines (EL2, HL2, SL2) |
| C-013 | V1 | Panel-wide finish signal at T0 + 1.20 x B is enforceable per package |
| X-001 | V5 | Itemised, conservative harness share plus spike 5 to measure the drop directly |
| X-002 | V1 | States correctly: 0 on /14, control may fall up to 0.33 in sonnet panels |
| X-003 | V1 | GT6 = I1, matching SEED:71 |
| X-004 | V5 | Haiku panels are legal against HL2, and Shadow Resume shows +0% there |
| X-005 | V1 | 116 s is the slower luna, as SEED:98 implies |
| X-006 | V4 | Exactly one block, phase-1 lines verbatim, P2 ids, parser-validated (R-04, R-16) |
| X-007 | V2 | Free text forbidden and receiver text rendered only from a template |
| X-008 | V1 | Grading and judge held constant in every arm |
| X-009 | V1 | Truncation cannot drop; V4's re-ask alone can |
| X-010 | V5 | Quantifies net collaboration against a static kit and admits the kit may win |
| X-011 | V5 | Zero AC-level anchors means anchor-based B1 gain needs a gap route |
| X-012 | V4 | I7 kept on control /2 throughout, stated in the header |
| X-013 | V2 | Its Fisher claim (p = 0.030) is correct; V5's fails |
| A-001 | V1 | REQ-S3 tests that the model acts, not only that the hook fires |
| A-002 | V5 | Only variant that estimates the static kit's own time cost and plans to remeasure turns |
| A-003 | V2 | Random labels plus sealed-report judging give a within-run comparison |
| A-004 | V4 | States the H-collaboration interaction (M4/M6 need H1/H3) and applies H to all arms |
| A-005 | V5 | States the /3 assumption as unverified and asks for per-run checks |
| A-006 | V2 | Only variant with a defence (decoys) |
| A-007 | V2 | Spike, fresh-session fallback and the slash-command guard (R-17) |
| A-008 | V4 | States the rule (helpers write only under $BOARD) and verifies it (clean sandbox, unchanged candidate hash) |
| A-009 | V2 | Requires confirmation on two new packages |
| A-010 | V1 | States why: replicated n = 6, cheapest, where cheap collaboration matters |
| A-011 | V5 | Calibrates the summed c to sonnet's measured reach as a ceiling |
