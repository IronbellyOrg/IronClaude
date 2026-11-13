# Round 1 statement: V1 (opus, architect lens)

## Position summary

The merged spec should be one shared substrate (board, digest, catalogue, schema, deadline, alarm) plus five policies on top of it, one per mechanism family, so the five designs share code and cannot drift. V1 supplies the parts that make the cap and the harness/collaboration split enforceable: the panel-level deadline (V1:138), the four-fix bundle with grading held constant (V1:102-111), the deny-list (REQ-C2) and the act-not-just-delivery spike (REQ-S3). V4 is the better base document, and four of my five designs lose their slot to stronger members of the same family.

## Steelman and critique of each other variant

### V2

**Steelman.** V2 has the most rigorous experiment. It runs a fresh A0 so the harness share is measured at the same time as the arms, not taken from history (V2:509). It has a catalogue-only arm (V2:511). It judges the sealed phase-1 reports separately under random labels, which measures collaboration inside the same run (V2:517, R-28). Its adoption rule is the only one whose Fisher example is right at p < 0.05 (4/6 vs 0/6 = 0.030, V2:526; I recomputed it). Decoys (V2:240, :266) are the only defence against a peer's anchor acting as a "something is here" signal (A-006). The three-gate funnel (V2:11, :81-94) is the cleanest way to map theories to designs. The pointer-following evidence (luna read source.md 48/48 vs 11/48, V2:27) is the best measured support for any relay design.

**Critique.**
- D1's time guard is wrong as stated. V2:182 says a luna that stops at 135 s or later gets nothing, but min(2, floor((150 − t − 12)/11)) is already 0 at t = 128 s.
- D1's I7 high end of 0.60 (V2:204) is above the single-luna chain 0.9 × 0.8 × 0.6 = 0.43. The two lunas get disjoint locators (V2:159), so having two lunas cannot double it.
- D3 has no harness time box (V2:317), and its first pass is "only partly protected" (V2:327).
- D5 is budgeted against S14 (V2:438), which is not a seed baseline.
- D4 depends on luna logging cells, but luna makes about 1 Bash call per run (V2:414).

### V3

**Steelman.** V3 is the shortest path to running code: R2 is about 90 lines, R4 about 50 and R5 about 110. Several of its safeguards are cheap and worth keeping:
- the 12-character anchor-leak check (V3:88, req 11);
- the 10 → 20 run extension rule (V3:160);
- second-judge double scoring of a sample (V3:167);
- a hold-out fourth package before any product change (req 21).

R5 Coverage Claims is the cheapest coordination design in all 25 (+4%).

**Critique.**
- Req 6 (V3:176) puts collaboration findings outside the findings-v1 block, so every collaboration gain would be scored as zero (X-006).
- The harness share of 0.8-2.1 (V3:126) is above every other variant's high end. It also contradicts the seed: cheap reviewers who read source.md still missed B5 and I1.
- I7 is counted on the /14 scale (V3:78), which inflates the gains (X-012).
- The 14 s "harness overhead" (V3:69) contradicts SEED:98, and it shifts every V3 budget.
- There is no static-catalogue arm (V3:148-154), so V3 cannot separate the exchange from the content of the prompt.
- The absolute Jaccard 0.5 alarm (V3:77) fires on noise in haiku panels and never fires in ember + luna panels.
- None of the five gains follows from its own stated inputs (grid rows V3-R1 to R4).
- V3:44 attributes `merge_guard.py:256` to B5. It repairs I1 (X-003).

### V4

**Steelman.** V4 is the only variant written to be operated, not just tested:
- the kill switch gives a byte-identical launch command (R-05);
- the board path is baked into the hook command strings, which removes the unverified environment-inheritance dependency (R-21, U-013);
- per-package `collab.json` telemetry and an SLO error budget (R-23, R-24);
- a detection/action runbook for every failure mode.

Its phase design (V4-3) seals by process exit, so the seal needs no compliance (V4:379). It filters surface findings (V4:345, :563). Move Radar (V4-1) needs no model to author anything. Four of its five gain tables are arithmetically correct. Its T3 split into "cannot see" and "seen and dropped" is the most useful refinement of T3 (V4:57-70).

**Critique.**
- V4-2's worst case is 116 + 6 + 38 = 160 s, which is +37.9% (V4:301). The 125 s delivery deadline cannot bind, because facts arrive mid-run.
- V4-2 also needs a `panel-seal` compliance turn from luna.
- V4-3's schedule says a 45 s timeout (V4:375) but its budget uses 35 s (V4:396).
- The experiment is n = 4, a screen, and its reach rule has no significance test (V4:658, :666).
- V4-4 and V4-5 use S13 and S14. S14 is not a seed baseline.
- V4-3 sends real peer anchors with no decoy (A-006).
- V4 states that H and C interact (V4:184) but still reports "plus H share" additively.

### V5

**Steelman.** V5 is the most disciplined about cost.
- It checked the CLI and found that `--max-turns` is absent (V5:106), so turn caps must come from hooks and `timeout`.
- It calibrates per-move credit c as a ceiling against sonnet + 2x luna's measured reach (V5:94).
- It adds tokens per added issue and a static-kit row that predicts the kit beats every exchange design on gross gain (V5:411, :418). That is the hypothesis the experiment most needs to refute.
- It splits the gain into three shares: harness, prompting and collaboration (E-5).
- Its first-hand evidence rule stops a bad peer sweep from spreading (C-3).
- Shadow Resume uses real idle time for +0% (V5-D5).
- Spike 5 re-scores existing runs with the normalizer at judge cost only.

**Critique.**
- The "4 vs at most 1" Fisher clause gives p = 0.121 at n = 6 (V5:457; I recomputed 112/924), so it cannot pass at p ≤ 0.10.
- The low/high band is a fixed 0.25× and 2× of the central estimate (V5:139), not tied to individual issues.
- The 120-character `note` field (V5:117) can carry a conclusion that contains no listed verdict word.
- H-4 (MINOR notes) and H-6 (the judge also scores the raw union) change the grading inside the "harness share" (V5:482-484, X-008).
- The independence gate counts tool calls only (V5:120) and leaves no sealed artifact.
- D2's schedule caps injections at 2 (V5:224), but its time block uses 3 and 5 flips (V5:236-237).

## Strengths claimed

1. **Panel-level time enforcement.** At `PANEL_FINISH_AT = T0 + 1.20 × B` the hook injects "finish now", the send helper refuses and Stop never blocks (V1:138, REQ-B5). Only V1 makes the +35% cap hold per package for mid-run designs (U-001, C-013). Every board design in the slate needs it.
2. **Harness/collaboration separation.** The bundle is exactly the four seed fixes. H2 truncates to 200/300 characters, validates with the real parser and re-asks once (REQ-H2, H3), which closes both the gap in V4's re-ask-only fix and the gap in V5's truncate-only fix (X-009). The grading rule is held constant and the judge template is pinned by sha256 (V1:111, REQ-M3), so A1 against S07 does not mix in a rubric change (X-008).
3. **Substrate-plus-policy architecture.** V1 builds one bus and gives each design a policy file (V1:100), with shared lines counted (V1:223). The merge needs this shape to build five designs without five harnesses.
4. **Overfitting guard.** A mechanical deny-list of candidate paths and backticked tokens is applied to the catalogue, the briefs and the cards (V1:128, REQ-C2).
5. **Spike that tests the act, not just delivery.** REQ-S3 (V1:614) checks that the next tool call follows an injected instruction. It is the only spike in the five variants that tests A-001's act rate, which every gain in the slate depends on.
6. **Decision logic.** Adoption is judged against the catalogue arm (A2), not the bare arm (V1:591). If A2 comes within 0.25 of the collaboration arm, the static catalogue ships instead (V1:593). There is a stop-early rule at A1 ≥ 3.0/14 (V1:595). The Fisher example is correct (3/6 vs 0/6 = 0.091).
7. **Every design on a seed baseline** (EL2, HL2, SL2; C-012). The automatic evidence trail needs no model action on either end, hash-splits paths across receivers and has a tunnelling alarm (V1-R2, U-002). It is grafted into slot 2.
8. **Searcher/reader complementarity** (V1:27-45). This is the structural reason an F4 relay is collaboration and not a checklist: no cheap model holds both halves.

## Concessions

I checked each finding of the diff analysis about V1. All of them hold.

1. **V1-R2 I7 high end.** The chain is 0.45 × 0.7 × 0.85 = 0.268, but V1:279 states 0.35. The hash split sends each path to one luna only, so nothing doubles it. The correct range is 0.16-0.27.
2. **V1-R4 total.** The rows sum to 0.12 − 0.10 = 0.02 at the low end and 0.60 − 0 = 0.60 at the high end, not the stated 0.05-0.45 (V1:426-432).
3. **V1-R3 rounding.** The rows sum to 0.16-0.63, against the stated 0.15-0.6.
4. **V1-R3 kill rule.** The hard kill at 1.35 × T1 (V1:323, REQ-X6) is relative to the run's own phase 1, which runs with the catalogue brief, not to the named baseline. Fix: kill at min(1.35 × T1, T0 + 1.35 × B_A1) − 2 s.
5. **V1-R5 arrival time.** Arrival is at about 40% of sonnet's run (110/274), not 45% (V1:455).
6. **Independence gates.** R1, R2 and R4 gate on a tool-call count (V1:185, :251). That leaves no auditable sealed artifact. V4's process-exit and seal-file gates are better (C-006).
7. **Idle-time budgets (A-002).** My budgets start from 116 s, while arm A3 runs with the catalogue in the brief (V1:171, :556). V5's +29% estimate for the static kit makes this unsafe.
8. **Location signal (A-006).** R3 sends peer regions without decoys. V2's decoys are needed.
9. **H + C summed linearly** (V1:198-200), although they interact (A-004).
10. **Compliance.** Three of my designs have weak compliance profiles. R1 and R4 depend on models posting, and I flagged that weakness myself (V1:540). R5 rests on gateway `SendMessage`, which I rated Low reliability (V1:538). Their family rivals (V4-1, V2-D5, V4-5) are better.

## Shared assumptions

- A-001: QUALIFY. Proving delivery is not enough. A REQ-S3-style spike must measure the act rate per gateway model, and every gain must be recomputed from that measured rate.
- A-002: QUALIFY. The idle windows exist, but every budget must be recomputed from measured A1 and A2 end times (V5 spike 4). The +35% is judged against A1, the named harness-fixed isolated baseline.
- A-003: QUALIFY. Strip arm markers (REQ-M2, R-10), add V2's sealed-report judging, and report credits per finding so that "more findings, more chance credits" is visible.
- A-004: REJECT. The shares interact (V4:184). Measure C as arm minus A2 with H applied in both arms, report it as conditional on H, and never add H and C as independent quantities.
- A-005: QUALIFY. Use per-package A1 medians for the cap (V4 R-24), not three-package totals divided by 3.
- A-006: REJECT. A location is a signal. F1 must carry V2's decoys. F3 and F6 send no peer locations, so they are unaffected.
- A-007: ACCEPT, behind spike S2 and the fresh-session fallback (V2:286, V4:384).
- A-008: QUALIFY. Read-only is a policy, because Bash is unrestricted. Enforce it with helpers that write only under `$BOARD` plus a clean `git status` check after each run (V4 R-09, V2 R-5).
- A-009: ACCEPT, with the deny-list (REQ-C2) and confirmation on two new packages before adoption (V2:531).
- A-010: ACCEPT. Slot 1 runs its HL2 variant and slot 4 runs on SL2 only after the EL2 result.
- A-011: QUALIFY. These rates are judgment. For never-found issues (B1, B2, I5, I6) the low end must be about 0, and V5's c ceiling bounds the high end.

## Proposed final slate of five redesigns

| Slot | Family | Core | Grafted parts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 decoy (1 of 3) and flip table; V1-R3 gap card and per-run kill at min(1.35 × T1, T0 + 1.35 × B_A1); V5-D5 HL2 shadow scheduling with an isolated haiku canary | Most reliable design, sealed by process exit; four variants converged on it; 148 s = +27.6% on EL2 with a 35 s luna timeout |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V1-R2 automatic seen-not-opened harvest, hash-split; V2-D1 delivery at the first Stop (natural seal, no `panel-seal` turn) with the guard recomputed; V5-D3 first-hand re-run rule and the 10% mismatch stop | Only strong I7/T1 path on EL2, run in ember's idle time; dropping the seal turn and capping at 2 facts fixes the +37.9% worst case: 116 + 12 + 2 × 12.8 = 153.6 s = +32.4% |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V1-R1 region × move gap grain and per-receiver hash ordering; V5-D4 rule that a covered region is never a reason to skip, plus the rotating move permutation | No model authors anything, so lowest compliance risk; 144 s = +24.1% |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection, re-based to SL2 (274 s, a seed baseline) | V2-D4 cards list uncovered (Task × move) cells only, not covered counts; V1-R5 sonnet brief line "peer coverage is not clearance"; V4 surface filter kept | Harness-generated cards and a Claude receiver; the only design that uses cheap models' finished output to steer the strong one; 274 + 56 = 330 s = +20.4% |
| 5 | F5 Structural index / source-rule witness | V2-D5 Source-Rule Witness, re-based to EL2 | V1-R4 fact-only feature enum and "partial, not exhaustive" label; V5-D1 kind → move pairing, delivered by PostToolUse after call 6 (no Stop reissue) | Only design aimed at the source-only rules (B5, I1, B2) that H1 and H3 expose; ember witness about 61 s; luna 116 + 25.6 + 1.4 = 143 s = +23.3% |

All five sit on the shared substrate: V4 board with baked-in path and kill switch, V1 `PANEL_FINISH_AT`, V2 schema with no free text, V5 first-hand rule, and one relative convergence alarm. Cross-session `SendMessage` stays a spike-gated fallback only. It has no audit file, and no design depends on it.

Proposed base document: V4. It has the most complete scaffold (catalogue with a style column, timing constants, baseline table, R-01..R-30 with verification), it supplies four of the five cores, and four of its five gain tables are correct. Graft in V2's theory funnel and experiment (A0-A4, sealed judging, Fisher p < 0.05), V5's three-share split and static-kit control, and V1's deadline, deny-list and held-constant grading.

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | Full (a)-(h) per design plus a detection/action runbook table |
| S-002 | V4 | Most complete scaffold: kill switch, baked-in board path, timing constants, baseline table |
| S-003 | V2 | Three-gate funnel names the blocked gate per issue, the cleanest theory-to-design map |
| S-004 | V5 | Only table with net collaboration share, tokens per issue and a static-kit control row |
| S-005 | V4 | One ID scheme, each requirement paired with a verification column |
| S-006 | V5 | Itemised unverified-assumption list that ties each number to a spike |
| C-001 | V2 | Pointer-following evidence (48/48 vs 11/48) is the best measured support for relay designs |
| C-002 | V5 | T2a/T2b split correctly shows that B1/B2/I4 need reach, not a flipped question |
| C-003 | V1 | Exactly the four seed fixes, H2 = truncate + validate + re-ask, grading held constant |
| C-004 | V4 | M1-M10 with a best-style column that routing uses; M10 covers B6 |
| C-005 | V2 | ≤400 bytes, verbatim located quote, explicit forbidden keys, "place and method, not a finding" render |
| C-006 | V4 | Process-exit seal for phases and a seal file plus `seal_missing` runbook for mid-run |
| C-007 | V5 | Relative arm alarm plus echo plus easy-issue share, which directly measures the seed's "same easy issues" |
| C-008 | V4 | Per-design, per-issue chains, arithmetically correct in four of five designs |
| C-009 | V5 | Three shares (harness, prompting, collaboration); add V2's within-run sealed judging |
| C-010 | V2 | Fresh A0 + H + catalogue + two designs, so all four shares are measured at the same time |
| C-011 | V2 | Reach vs A1 at p < 0.05 AND +2 runs vs A2; correct Fisher example |
| C-012 | V1 | All five designs on seed baselines (EL2, HL2, SL2) |
| C-013 | V1 | Panel-level `PANEL_FINISH_AT` is the only per-package mechanism for mid-run designs |
| X-001 | V5 | Bottom-up per-fix estimate (0.03-0.34) with a cheap measurement (spike 5); V3's 0.8-2.1 contradicts the seed |
| X-002 | V1 | 0 on /14; control may fall up to 0.33 for sonnet panels, consistent with SEED:71 |
| X-003 | V1 | `merge_guard.py:256` repairs GT6 = I1, matching SEED:71 |
| X-004 | V5 | HL2 used legally against its own baseline, and its idle time used for +0% |
| X-005 | V1 | luna B at 116 s is the slowest reviewer, per SEED:98; no invented overhead |
| X-006 | V4 | Single block, P2-F ids, origin tag stripped before judging, validated by R-02 |
| X-007 | V2 | No free text at all; forbidden keys enumerated and rendered template fixed |
| X-008 | V1 | Grading and judge template held constant, sha256-pinned (REQ-M3) |
| X-009 | V1 | Truncate then validate then re-ask once covers both V4's and V5's gaps |
| X-010 | V5 | Static kit estimated explicitly; net collaboration share is the honest figure |
| X-011 | V5 | 0 AC-level anchors means low B1/B2 gains; task-level anchoring does not reach AC3 |
| X-012 | V1 | I7 kept on control /2 from the header onward (V1:17) |
| X-013 | V2 | Fisher example correct and threshold stricter (p < 0.05) |
| A-001 | V1 | REQ-S3 is the only spike that tests whether the model acts on an injection |
| A-002 | V5 | Only variant that flags the cost of the static kit and remeasures turns (spike 4) |
| A-003 | V2 | Random labels plus separately judged sealed reports give an in-run control |
| A-004 | V4 | States the dependency (M4/M6 pay only after H1/H3) |
| A-005 | V5 | States per-package baselines as unverified and says to check them against per-run wall_s |
| A-006 | V2 | Decoys are the only defence against the location signal |
| A-007 | V4 | Spike S2, fresh-session fallback and a `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD`; clean `git status` check (R-09) |
| A-009 | V2 | 12-run confirmation on two new packages before adoption |
| A-010 | V1 | States why: replicated default, cheapest, where cheap-model collaboration matters most |
| A-011 | V5 | c calibrated as a ceiling against SL2's measured hard reach |
