# Round 1 statement: V3 advocate (haiku backend lens; persona: backend, focus on data integrity, scalability, fault tolerance)

## Position summary (1-3 sentences)

V3 is the weakest scaffold of the five and should not be the base. Its gain blocks do not follow from their own inputs, and its harness share is overstated about 3x. What it does contribute is a set of integrity controls: a sealed first-pass artifact, a cross-reviewer anchor-leak check, reject-not-truncate caps, a frozen and hashed enum, and run-scoped settings with a hash check. These belong in the merged spec on top of V4's scaffold. V4 has the most complete substrate and supplies four of my five slate cores.

## Steelman and critique of each other variant (one subsection per variant: steelman first, then critique with evidence)

### V1 (architect lens)

**Steelman.** V1 is the only variant that makes the +35% cap enforceable at panel level. `PANEL_FINISH_AT = T0 + 1.20 x B` injects "finish now", stops Stop-blocking and makes the send helper refuse (V1:138). It also gives the phase design a per-run hard kill at `1.35 x T1 - 2 s` (V1:323). Its H2 combines truncation with a parser check and one re-ask (V1:107), which is strictly safer than V4's re-ask-only path, and it holds the grading rule constant (V1:111). That makes "harness share" a clean quantity. R2 Evidence trail is the most fault-tolerant design in the field: neither end needs model action, and paths are hash-split (V1:237). Its experiment has the static-catalogue arm that separates "the move list helps" from "the exchange helps" (V1:548). Its baselines are all seed baselines (EL2, HL2, SL2).

**Critique.**
- V1-R3's guarantee is relative to the run's own T1, not to the named baseline (V1:323). A slow phase 1 (A2 brief plus H1 makes runs longer, A-002) therefore widens the window. The kill must be `min(1.35 x B_named, 1.35 x T1) - 2 s`.
- V1-R4's total of +0.05 to +0.45 does not match its rows: low 0.12 - 0.10 = 0.02, high 0.60 (V1:426-432).
- In V1-R2, the I7 high of 0.35 exceeds its own chain, 0.45 x 0.7 x 0.85 = 0.27 (V1:279).
- R1 and R4 depend on gateway models posting cards. V1 itself names this as the weak point (V1:540).

### V2 (analyzer lens)

**Steelman.** V2 is the best on measurement integrity.
- Decoys (1 of 3 challenges at a place no peer flagged, V2:241) are the only defence against the location-as-signal leak (A-006).
- Judging the sealed phase-1 reports separately gives within-run attribution of the collaboration share (V2:517, R-28).
- Its decision rule is correct as written: 4/6 vs 0/6 gives one-sided Fisher p = 15/495 = 0.030, which I recomputed. It also requires beating the catalogue arm by 2 runs (V2:526).
- Contemporaneous A0 and A1 arms make H a measured quantity, not a historical comparison (V2:509-510).
- R-9 validates each message mechanically: a quote must be verbatim and located, and a path must exist.

**Critique.**
- V2-D1's time guard is misstated: `min(2, floor((150-t-12)/11)) = 0` from t = 128 s, not 135 s (V2:182).
- The D1 I7 high of 0.60 exceeds the single-luna chain 0.9 x 0.8 x 0.6 = 0.43, and the lunas receive disjoint locators (V2:159), so two lunas cannot double it.
- V2-D3 has no harness time box at all (V2:317), and its first pass is "only partly protected" (V2:327). That is a weaker fault boundary than any other design.
- V2-D5's baseline (S14) is not a seed baseline.

### V4 (devops lens)

**Steelman.** V4 is the most operable spec.
- The kill switch `PANEL_COLLAB=0` gives a byte-identical launch command (R-05).
- Per-package `collab.json` telemetry and an SLO error budget make the panel diagnosable (R-23, R-24).
- The absolute board path and reviewer id are baked into hook commands, which removes the unverified env-inheritance dependency by design (V4:124).
- Every design has a detection-and-action runbook (V4:262-270).
- Move Radar (V4-1) needs zero model authoring, so it is immune to gateway tool-call compliance.
- Axis-Flip (V4-3) seals the first pass by process exit, needs no compliance, and has a surface filter (V4:345).
- Its alarm is ground-truth-free and works in the product (V4 R-25).
- Four of its five arithmetic blocks are correct.

**Critique.**
- V4-2's typical 142 s omits the 6 s seal turn. My recomputation: 116 + 6 + 26 = 148 s typical, and worst 116 + 6 + 38 = 160 s = +37.9%, which is over the cap. The 125 s delivery deadline (V4:301) cannot bind because luna's baseline end is 116 s, and the 15 s Stop hold adds more.
- V4-3's phase-2 timeout is stated as 45 s (V4:375) and then corrected to 35 s (V4:396). This is reconciled only in R-15.
- n = 4 per arm (V4:658) is a screen, not a test. V4 admits this.
- V4-5 uses S14, which is not a seed baseline.

### V5 (performance lens)

**Steelman.** V5 asks the most important question honestly: does any exchange beat a static move kit? Its estimate is that the kit wins on gross gain (0.33) and that net collaboration is 0.05-0.14 (V5:411, :418). It splits gains into three shares: harness, prompting and collaboration (E-5). It also:
- splits T2 into T2a (asked the wrong question) and T2b (never reached the place, V5:40), which correctly predicts that anchor designs barely reach B1 and B2;
- is the only variant to require first-hand evidence: a receiver must re-run a peer's command before citing it, with a >10% mismatch stop (V5:299, C-3);
- uses haiku as an isolated in-run canary while lunas use haiku's shadow for +0% elapsed (V5-D5);
- verified `--resume` and the absence of `--max-turns` against `claude --help` (V5:106);
- has a tokens-per-added-issue column, the only cost-per-issue figure in the field.

**Critique.**
- The adoption clause "4 runs vs at most 1, Fisher p ≤ 0.10" fails its own threshold. I recomputed it at n = 6: (15·6 + 6)/C(12,5) = 96/792 = 0.121 (V5:457).
- The `note` field (≤120 chars, filtered only for verdict words, V5:117) lets conclusions travel ("grep misses root files").
- H-4 (ask for MINOR notes) and H-6 (judge the raw union) change the rubric and the judge input inside the "harness share" (V5:482-484). That mixes a grading change into H (X-008).
- The 0.25x/2x band is fixed, not derived per issue.

## Strengths claimed (numbered, with evidence)

1. **A file-based seal with a timestamp check.** For mid-run designs, a `pass1.md` must exist before any peer content is released, and its timestamp must be earlier than the first peer line received (V3:56, req 10). This turns "independent first pass" into one auditable integrity check per run. A call-count gate (V1:185, V5:120) leaves no artifact. V4's `panel-seal` does the same thing with better fallbacks, so the merge should use V4's mechanism with my timestamp test as its acceptance criterion.
2. **A cross-reviewer anchor-leak check.** A board line that contains a 12-character or longer substring of another reviewer's anchor is a hard failure (V3:88, req 11). This is a mechanical, ground-truth-free test that a content-free channel really is content-free. V4's check (V4:671) compares against ground truth, which a product cannot do. The two are complementary. Mine applies only to designs that promise to carry no anchors (Radar, Deflection), not to F1 designs, which send anchors on purpose.
3. **Caps reject oversized messages instead of truncating them** (V3 req 8). Truncating a message silently changes what a peer receives. Rejecting it keeps the board an exact record. V4 R-06 agrees, but V1 H2 and V5 H-2 truncate *findings* (correctly) and say nothing about *messages*. The merge must state the rule for messages explicitly.
4. **Configuration integrity.** The move enum is hashed before the arm starts, and any change invalidates the arms that used the old hash (req 18). Hooks are run-scoped through `--settings`, and the user's `~/.claude/settings.json` sha256 must be equal before and after the experiment (req 17). No other variant tests that the panel leaves host configuration untouched.
5. **A sequential power plan.** V3 gives an explicit power estimate (about 60% for +1.0 at n = 10, SD 0.94, V3:163), an extension rule that is triggered only by stated conditions (V3:160), and double-scoring of a random sample by a second judge (V3:167). The diff analysis judges the power estimate "approximately right" (X-013). V5's interim look (V5:454) is the same idea with better arm structure.
6. **Honest risk ratings.** R4 is rated High contamination risk (V3:110), not argued away.

## Concessions (own weaknesses)

I re-checked each finding the diff analysis made against V3. All of them hold except where noted.

1. **Gain arithmetic does not follow from its inputs.**
   - R1: 5 targets x 0.6-0.9 x 0.15-0.4 = 0.45-1.8, but V3 states 0.4-1.2 (V3:78).
   - R2: 5 x 0.5-0.8 x 0.1-0.3 = 0.25-1.2, but V3 states 0.2-0.9 (V3:89).
   - R3: 0.5-0.8 x 0.8-1.2 x 0.5-0.8 = 0.20-0.77, but V3 states 0.3-0.9 (V3:100).
   - R4: 4 x 0.1-0.3 = 0.4-1.2, but V3 states 0.1-0.6 (V3:111).
   - R5's figure cannot be derived from anything stated (V3:122).
   - The multiplication model is also too generous: it never multiplies by P(the move lands on the right region). V2's three-gate chain and V4's anchor-rate chain do. Confirmed.
2. **I7 is counted on the /14 scale** in R1, R3 and R5 (V3:78, :100, :122), and R3 is calibrated on sonnet's I7 rate. I7 is a control issue (SEED:22). Confirmed. That inflates every V3 /14 figure.
3. **The harness share of 0.8-2.1 is indefensible** (V3:126). The source.md fix is credited +0.3 to +0.8, but cheap reviewers who did read source.md still missed B5 and I1 (V2:144). The leak removal is counted as a *gain* of +0 to +0.1, when removing it can only lower credited I7 (X-002). Confirmed. V5's itemised 0.03-0.34 and V1/V2's 0.1-0.5 are the defensible range.
4. **Req 6 contradicts R1** (V3:176 vs :73). Putting collaboration findings "outside the fenced block" means they are never merged or judged, so every collaboration gain would score as zero. This is the most serious error in V3. The rule must be V1 REQ-X7 / V4 R-04: one block, with phase-1 lines unchanged.
5. **The "14 s fixed harness overhead" is wrong in attribution** (V3:69, X-005). Panel time is the maximum of the two luna draws, about 116 s. This error happens not to change the totals, because 102 + 14 = 116. Every V3 critical path equals "luna B at 116 s plus added work". So R1's 149 s (+28%) and R2's 136 s (+17%) stand. The reasoning behind them does not.
6. **R4 uses the wrong baseline.** It is an ember+luna panel measured against EL2. Against ember+luna (300/3 = 100 s), its 128 s is +28%, not +10%. Its "luna seal at about 60 s" contradicts luna's 102 s median, and nothing keeps ember alive (V3:107). V4-4 solves all of this with a Stop hold. R3 adds a fourth reviewer but keeps the 3-reviewer baseline, and its 130 s cap truncates most sonnet runs (228 s median).
7. **Mechanism gaps.** R1 never says how the harness knows "which moves each reviewer ran" when the phase-1 brief is unchanged (V3:73). V4-1's telemetry classifier is the missing piece. R3's alarm has no threshold (V3:99). R4 has no measurable alarm (V3:110). R5 "flags" compliance only, not convergence (V3:121).
8. **An absolute Jaccard alarm of 0.5** (V3:77, req 12) fires on noise in haiku panels (isolated reference 0.47) and never fires in ember+luna panels (0.25). It must be relative to the isolated arm (+0.15), as in V1, V2, V4 and V5.
9. **Factual errors.**
   - `merge_guard.py:256` repairs I1 (GT6), not a "B5-related cause" (V3:44 vs SEED:71).
   - Excluding haiku (V3:67) is wrong: the cap is relative to each panel's own isolated baseline (SEED:30).
   - V3 req 15 then allows haiku and grok, which contradicts its own V3:67.
10. **The experiment has no static-catalogue arm** (V3:148-154). V3 therefore cannot separate "the enum in the prompt" from "the exchange" (X-010), and its +1.0 adoption threshold is set against estimates that are 3-20x too high.

## Shared assumptions (one line per A-001..A-011: `A-NNN: ACCEPT|REJECT|QUALIFY — reason`; omitting any is flagged)

- A-001: QUALIFY — Hook delivery is testable, but act rate is the load-bearing number. Adopt V1 REQ-S3 (the next tool call follows the injection), and replace every gain table's act rate with the measured spike rate before the arms run.
- A-002: REJECT — Idle time after H1 plus a catalogue brief is not measured. V5 estimates the static kit at +29% (V5:411). Every budget must be re-based on the A1 (or A2) arm's measured elapsed time, not on 116 s.
- A-003: QUALIFY — Keep the judge unchanged and stripped of arm markers (V1 REQ-M2, V4 R-10). Also report found-per-finding, and judge the sealed reports (V2), so that "more findings, more chance credits" is visible.
- A-004: REJECT — The shares interact: M4 and M6 pay off only after H1 and H3 (V4:184). Report harness, prompting and collaboration as measured arm differences (V5 E-5), never as a sum of estimates. V3's "20% overlap" was a guess.
- A-005: QUALIFY — Dividing by 3 is acceptable for planning only. The cap must be checked per package against the measured per-package A1 median (V4 R-24; V5:23).
- A-006: REJECT — A location is a signal. Every design that sends peer anchors needs V2 decoys. Content-free designs need my 12-character cross-reviewer leak check.
- A-007: QUALIFY — Spike-gate it (V4 S2). The fresh-session fallback must be logged (`resume_fallback`), and the fallback's extra ~10 s must be inside the time arithmetic.
- A-008: QUALIFY — Bash is unrestricted, so "read-only" is policy. Enforce it after the fact: sandbox `git status` clean, candidate sha256 unchanged, board writes only through helpers (V4 R-09), and user settings sha256 unchanged (V3 req 17).
- A-009: QUALIFY — Freeze and hash the catalogue, run the deny-list check (V1 REQ-C2), and confirm on two new packages before any product change (V2:531). V3's single hold-out package is weaker.
- A-010: ACCEPT — EL2 is the replicated default and the cheapest panel. Variants on HL2, SL2 and ember+luna are allowed against their own seed baselines.
- A-011: QUALIFY — For never-found issues (B1, B2, I5, I6), the low end must be ~0 (V2:139). High ends are labelled as ceilings, not forecasts (V5:94).

## Proposed final slate of five redesigns

| Slot | Family | Core redesign | Grafted parts (ids) | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 (1 decoy in 3; flip table); V1-R3 (gap card; kill at min(1.35 x B_named, 1.35 x T1) - 2 s); V2 sealed-report judging (U-006); V5-D5 (HL2 shadow variant with an isolated haiku canary) | Most fault-tolerant: seal by process exit, harness-only delivery, phase-1 fallback. 148 s = +27.6% of EL2 116 s; HL2 variant +0-6%. |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V1-R2 (automatic seen-not-opened harvest, hash-split); V5-D3 (first-hand re-run rule; >10% mismatch stop); V2-D5 (source-rule witness as one sweep kind); V3-R3 (hard `timeout` on the sweeper session); luna limited to 2 acted facts | The only cheap path to I7 (T1). With 2 facts: 116 + 6 + 26 = 148 s = +27.6%, which fixes V4-2's 160 s (+37.9%) worst case. |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V1-R1 (region x move gap grain; per-receiver hash order); V5-D4 (rotating permutation so reviewers do not share a gap); V3-R2/R5 (12-character cross-reviewer leak check, hard failure); V3-R1 (end-of-phase move-gap digest via `--resume` as fallback if hooks fail spike S0) | Zero model authoring, so no gateway compliance risk. 144 s = +24%. Its rival is the static catalogue arm, which the experiment measures. |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection | Moved to SL2 (seed baseline 274 s, cap 369.5 s) per V1-R5; V1-R5 requests rendered by the harness from luna's "not checked" scope (no SendMessage); V2-D4 (Task x move cell grain); V4 surface filter (U-014) | Harness-authored cards and a Claude receiver are the lowest-risk mid-run path. 274 + 56 worst = 330 s = +20%. |
| 5 | F7 Directed challenge / adjudication | V4-4 Flag-and-Adjudicate | V3-R4 (cross-session SendMessage only as a spike-gated fallback); V5 C-3 (first-hand evidence); V1 PANEL_FINISH_AT at 1.20 x 100 s; V2 decoy card | Answers the seed's open question "challenge vs shared findings" with a mandatory finite-check answer. On ember+luna (seed 300/3 = 100 s): typical 119 s (+19%), worst 132 s (+32%). |

F2 (V5-D2, V2-D3) is dropped. It is F1's axis flip done mid-run with model-authored posts, which adds compliance risk and no new mechanism. F5 (V1-R4, V5-D1, V2-D5) is folded into slot 2's fact kinds as the witness and referrer sweeps.

Proposed base document: V4. It has the most complete substrate (catalogue with style routing, schema, baked board path, kill switch, telemetry, SLO, runbooks), and it supplies four of the five cores. Two parts must be replaced. Its experiment and statistics should come from V2: the arm structure, the Fisher-verified decision rule and sealed-report judging, at V5's 12-run size. Its theories should be extended with V5's T2a/T2b split.

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design with tables plus a detection/action runbook; V3's one-bullet designs are too thin |
| S-002 | V4 | Most complete shared block: catalogue with style column, schema, baked board path, kill switch, timing and baseline tables |
| S-003 | V5 | One theory table plus T2a/T2b split and issue map; the split changes which designs can reach B1/B2/I4 |
| S-004 | V5 | Carries harness, net collaboration, a static-kit control row and tokens per added issue |
| S-005 | V4 | One ID scheme (R-01..R-30), design-specific, each with a verification column |
| S-006 | V5 | Itemised unverified list tied to each assumption used in arithmetic |
| C-001 | V1 | Searcher-to-reader split across models explains why F4 relays work (V2's 48/48 pointer evidence supports it) |
| C-002 | V5 | T2b (never reached) is the honest reading of 0 AC3 anchors; T3 split into masks vs drops |
| C-003 | V1 | Truncate + parser-validate + re-ask once, grading held constant; V4 re-ask alone can still drop, V5 bundles a rubric change |
| C-004 | V4 | M1-M10 with a best-style column, which the routing in Radar, Flip and Adjudicate needs |
| C-005 | V4 | Single `panel-msg/1`, forbidden fields dropped, anchor 12-200 located; fits F1 anchors (V2's 120-char quote is too short for real anchors) |
| C-006 | V4 | Process-exit seal for phase designs; `panel-seal` + call-6 gate + `seal_missing` fallback for mid-run |
| C-007 | V4 | Relative J +0.15 or ledger rows -20%, ground-truth-free so usable in product; per-design echo thresholds |
| C-008 | V2 | Explicit P(trigger) x P(delivered and acted) x P(stated and survives) per issue, tied to the gate funnel |
| C-009 | V5 | Three measured shares (harness, prompting, collaboration); add V2's within-run sealed-report C |
| C-010 | V2 | Contemporaneous A0 and A1, a catalogue arm, two design arms, 6 runs each; V3 lacks the catalogue arm, V4 n=4 is a screen |
| C-011 | V2 | Reach endpoint with a Fisher threshold that holds (p=0.030) plus +2 runs over the catalogue arm |
| C-012 | V1 | Uses only seed baselines (EL2, HL2, SL2); V4-5 should move from S14 to SL2 |
| C-013 | V1 | Panel-level PANEL_FINISH_AT is the only enforcement of the cap for mid-run designs |
| X-001 | V5 | Itemised derivation (0.03-0.34) plus spike 5 that measures the anchor-drop share; V3's 0.8-2.1 is contradicted by the data |
| X-002 | V1 | Leak removal adds 0 on /14 and can only lower sonnet-panel I7 credits |
| X-003 | V1 | `merge_guard.py:256` repairs GT6 = I1, matching SEED:71; V3 is wrong |
| X-004 | V5 | Haiku is legal against HL2 and is best used as an isolated canary with phase 2 in its shadow |
| X-005 | V1 | Slowest luna (max of two draws) sets 116 s; V3's 14 s overhead is unsupported |
| X-006 | V4 | One findings-v1 block, phase-1 lines verbatim, new lines tagged `origin` and stripped before judging; V3 req 6 would zero every gain |
| X-007 | V4 | Free text forbidden and dropped by the validator; V5's 120-char `note` can carry conclusions |
| X-008 | V1 | Grading and judge held constant in every arm; V5's H-4/H-6 mix a rubric change into H |
| X-009 | V1 | Truncate then validate then re-ask: no edit to `findings.py`, and nothing can still drop |
| X-010 | V5 | A static kit may beat every exchange on gross gain; exchange must beat the catalogue arm |
| X-011 | V5 | 0% AC-level anchors means anchor designs barely reach B1/B2; task-level 52% is not enough |
| X-012 | V1 | I7 scored on control /2, separate from /14 |
| X-013 | V2 | Its Fisher threshold recomputes correctly (0.030); V5's "4 vs 1" fails (0.121) |
| A-001 | V1 | REQ-S3 spike tests that the next tool call follows an injection, the closest to measuring act rate |
| A-002 | V5 | Only variant to estimate prompt-induced slowdown (+29%) and plan a spike to remeasure turns |
| A-003 | V2 | Random labels plus separate sealed-report judging give a same-run comparison of judge credit |
| A-004 | V4 | States the dependency (M4/M6 pay only after H1/H3) and applies H in both arms |
| A-005 | V5 | States the divide-by-3 as unverified and requires checking per-run wall_s |
| A-006 | V2 | Decoys are the only defence against "a peer found something here" |
| A-007 | V4 | Spike S2, logged fresh-session fallback, and session-storage cleanup in the runbook |
| A-008 | V4 | Helpers write only under `$BOARD`; sandbox `git status` and candidate sha256 verified (R-09) |
| A-009 | V2 | Confirmation on two new packages with implement-history ground truth before adoption |
| A-010 | V1 | States why EL2 (replicated S07 n=6, cheapest, where cheap collaboration matters) and uses ember as the searcher |
| A-011 | V2 | Low end assumes ~0 where no cheap model ever executed the move |
