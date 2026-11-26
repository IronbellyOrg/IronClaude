# Adversarial Debate Transcript

## Metadata
- Depth: deep
- Rounds completed: 3 (plus Round 2.5 invariant probe)
- Convergence achieved: 100% (43/43 diff points)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 5 (V1 opus:architect, V2 opus:analyzer, V3 haiku:backend, V4 opus:devops, V5 sonnet:performance)
- Run note: the first session was stopped by a timeout during Round 3 after round3-V1 and round3-V2; a resumed session wrote round3-V3, -V4 and -V5 sequentially (each saw all earlier Round 3 statements), the Round 3 tally and every later artifact. No completed file was rewritten.
- Source files: `debate/round{1,2,3}-V{1..5}.md`, `debate/round{1,2,3}-tally.md`, `debate/round{2,3}-agenda.md`, `invariant-probe.md`; tallies computed by `debate/convergence.py`.

## Round 1: Advocate Statements

### Variant 1 Advocate (opus:architect)

### Round 1 statement: V1 (opus, architect lens)

#### Position summary

The merged spec should be one shared substrate (board, digest, catalogue, schema, deadline, alarm) plus five policies on top of it, one per mechanism family, so the five designs share code and cannot drift. V1 supplies the parts that make the cap and the harness/collaboration split enforceable: the panel-level deadline (V1:138), the four-fix bundle with grading held constant (V1:102-111), the deny-list (REQ-C2) and the act-not-just-delivery spike (REQ-S3). V4 is the better base document, and four of my five designs lose their slot to stronger members of the same family.

#### Steelman and critique of each other variant

##### V2

**Steelman.** V2 has the most rigorous experiment. It runs a fresh A0 so the harness share is measured at the same time as the arms, not taken from history (V2:509). It has a catalogue-only arm (V2:511). It judges the sealed phase-1 reports separately under random labels, which measures collaboration inside the same run (V2:517, R-28). Its adoption rule is the only one whose Fisher example is right at p < 0.05 (4/6 vs 0/6 = 0.030, V2:526; I recomputed it). Decoys (V2:240, :266) are the only defence against a peer's anchor acting as a "something is here" signal (A-006). The three-gate funnel (V2:11, :81-94) is the cleanest way to map theories to designs. The pointer-following evidence (luna read source.md 48/48 vs 11/48, V2:27) is the best measured support for any relay design.

**Critique.**
- D1's time guard is wrong as stated. V2:182 says a luna that stops at 135 s or later gets nothing, but min(2, floor((150 − t − 12)/11)) is already 0 at t = 128 s.
- D1's I7 high end of 0.60 (V2:204) is above the single-luna chain 0.9 × 0.8 × 0.6 = 0.43. The two lunas get disjoint locators (V2:159), so having two lunas cannot double it.
- D3 has no harness time box (V2:317), and its first pass is "only partly protected" (V2:327).
- D5 is budgeted against S14 (V2:438), which is not a seed baseline.
- D4 depends on luna logging cells, but luna makes about 1 Bash call per run (V2:414).

##### V3

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

##### V4

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

##### V5

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

#### Strengths claimed

1. **Panel-level time enforcement.** At `PANEL_FINISH_AT = T0 + 1.20 × B` the hook injects "finish now", the send helper refuses and Stop never blocks (V1:138, REQ-B5). Only V1 makes the +35% cap hold per package for mid-run designs (U-001, C-013). Every board design in the slate needs it.
2. **Harness/collaboration separation.** The bundle is exactly the four seed fixes. H2 truncates to 200/300 characters, validates with the real parser and re-asks once (REQ-H2, H3), which closes both the gap in V4's re-ask-only fix and the gap in V5's truncate-only fix (X-009). The grading rule is held constant and the judge template is pinned by sha256 (V1:111, REQ-M3), so A1 against S07 does not mix in a rubric change (X-008).
3. **Substrate-plus-policy architecture.** V1 builds one bus and gives each design a policy file (V1:100), with shared lines counted (V1:223). The merge needs this shape to build five designs without five harnesses.
4. **Overfitting guard.** A mechanical deny-list of candidate paths and backticked tokens is applied to the catalogue, the briefs and the cards (V1:128, REQ-C2).
5. **Spike that tests the act, not just delivery.** REQ-S3 (V1:614) checks that the next tool call follows an injected instruction. It is the only spike in the five variants that tests A-001's act rate, which every gain in the slate depends on.
6. **Decision logic.** Adoption is judged against the catalogue arm (A2), not the bare arm (V1:591). If A2 comes within 0.25 of the collaboration arm, the static catalogue ships instead (V1:593). There is a stop-early rule at A1 ≥ 3.0/14 (V1:595). The Fisher example is correct (3/6 vs 0/6 = 0.091).
7. **Every design on a seed baseline** (EL2, HL2, SL2; C-012). The automatic evidence trail needs no model action on either end, hash-splits paths across receivers and has a tunnelling alarm (V1-R2, U-002). It is grafted into slot 2.
8. **Searcher/reader complementarity** (V1:27-45). This is the structural reason an F4 relay is collaboration and not a checklist: no cheap model holds both halves.

#### Concessions

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

#### Shared assumptions

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

#### Proposed final slate of five redesigns

| Slot | Family | Core | Grafted parts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 decoy (1 of 3) and flip table; V1-R3 gap card and per-run kill at min(1.35 × T1, T0 + 1.35 × B_A1); V5-D5 HL2 shadow scheduling with an isolated haiku canary | Most reliable design, sealed by process exit; four variants converged on it; 148 s = +27.6% on EL2 with a 35 s luna timeout |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V1-R2 automatic seen-not-opened harvest, hash-split; V2-D1 delivery at the first Stop (natural seal, no `panel-seal` turn) with the guard recomputed; V5-D3 first-hand re-run rule and the 10% mismatch stop | Only strong I7/T1 path on EL2, run in ember's idle time; dropping the seal turn and capping at 2 facts fixes the +37.9% worst case: 116 + 12 + 2 × 12.8 = 153.6 s = +32.4% |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V1-R1 region × move gap grain and per-receiver hash ordering; V5-D4 rule that a covered region is never a reason to skip, plus the rotating move permutation | No model authors anything, so lowest compliance risk; 144 s = +24.1% |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection, re-based to SL2 (274 s, a seed baseline) | V2-D4 cards list uncovered (Task × move) cells only, not covered counts; V1-R5 sonnet brief line "peer coverage is not clearance"; V4 surface filter kept | Harness-generated cards and a Claude receiver; the only design that uses cheap models' finished output to steer the strong one; 274 + 56 = 330 s = +20.4% |
| 5 | F5 Structural index / source-rule witness | V2-D5 Source-Rule Witness, re-based to EL2 | V1-R4 fact-only feature enum and "partial, not exhaustive" label; V5-D1 kind → move pairing, delivered by PostToolUse after call 6 (no Stop reissue) | Only design aimed at the source-only rules (B5, I1, B2) that H1 and H3 expose; ember witness about 61 s; luna 116 + 25.6 + 1.4 = 143 s = +23.3% |

All five sit on the shared substrate: V4 board with baked-in path and kill switch, V1 `PANEL_FINISH_AT`, V2 schema with no free text, V5 first-hand rule, and one relative convergence alarm. Cross-session `SendMessage` stays a spike-gated fallback only. It has no audit file, and no design depends on it.

Proposed base document: V4. It has the most complete scaffold (catalogue with a style column, timing constants, baseline table, R-01..R-30 with verification), it supplies four of the five cores, and four of its five gain tables are correct. Graft in V2's theory funnel and experiment (A0-A4, sealed judging, Fisher p < 0.05), V5's three-share split and static-kit control, and V1's deadline, deny-list and held-constant grading.

#### Per-point positions

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

### Variant 2 Advocate (opus:analyzer)

### Round 1 statement: V2 (analyzer lens)

#### Position summary

V2 should supply the merge's theory spine (the three-gate funnel), its contamination defence against the "a peer found something here" signal (decoys), and its attribution machinery (a fresh old-harness arm, a static-catalogue arm and within-run sealed-report judging). For the redesigns and the scaffolding, V4 is the better base: its five gain tables are arithmetically clean, and three of my five slate cores come from it. Two of my own gain tables carry errors, which I confirm below.

#### Steelman and critique of each other variant

##### V1

**Steelman.** V1 is the only variant whose design treats the +35% cap as a panel-level rule. `PANEL_FINISH_AT = T0 + 1.20 x B` (V1:138) makes every mid-run design stop on time by construction. REQ-S3 (V1:614) is the only spike that tests whether a gateway model *acts* on injected text; every other variant tests only that the hook fires. R2 Evidence Trail (V1:235-256) is the only design that needs no model action on either side, which matters because luna makes about one Bash call per run. V1 holds grading constant (V1:111), pins the judge template by sha256 (REQ-M3) and adds a mechanical deny-list against overfitting (REQ-C2). Its H2 (truncate, validate, re-ask once) is the best anchor-drop fix of the five.

**Critique.**
- R3's "hard" cap is `1.35 x T1` of the same run (V1:323), not 1.35 x the named 116 s. If a slow luna ends phase 1 at 150 s, the cap becomes 202 s, which is +74% of S07. The guarantee is per run, not against the baseline the seed names.
- The R4 gain total does not follow from its rows. The rows give 0.02 to 0.60; V1 states 0.05 to 0.45 (V1:426-432; I re-summed them). The R2 I7 high of 0.35 exceeds its own chain, 0.45 x 0.7 x 0.85 = 0.27.
- The decision rule ORs three endpoints, each at p <= 0.10 (V1:591), so the familywise false-pass rate is well above 0.10.
- R1 and R4 depend on models posting cards, which V1 itself calls the weak point (V1:540).
- V1 has no fresh old-harness arm, so the H share is "descriptive only" against historical S07 (V1:594).

##### V3

**Steelman.** V3 is the most economical variant. Its designs are small (R2 is 90 lines; R5 adds +4%). It runs 10 runs per arm with a pre-registered 10-to-20-run extension rule (V3:160), which is more statistical power than V2's 6 runs. The 12-character substring leak check (V3:88, requirement 11) is a cheap mechanical audit. It requires a fourth unseen package, a frozen enum hash, a model allowlist and a settings-file sha check (requirements 15-21), all good hygiene. Its R3 (a capped sonnet sweeper) is a distinct idea: buy reach with a time-boxed strong model.

**Critique.**
- The harness share of 0.8 to 2.1 (V3:126) sits above every other variant's high end (X-001). The study contradicts it: cheap reviewers who read source.md still missed B5 and I1 (V2:144).
- Requirement 6 puts collaboration output outside the fenced block (V3:176). The merge never scores text there, so every collaboration gain would score zero (X-006).
- I7, which is scored on the control package, is counted on the /14 scale (V3:78, :100; X-012).
- The 14 s "harness overhead" (V3:69) contradicts SEED:98.
- None of the five gain figures follows from its own inputs. R1's inputs give 0.45-1.8, not 0.4-1.2.
- There is no static-catalogue arm (X-010), so a prompt effect cannot be told apart from an exchange effect.
- The absolute Jaccard threshold of 0.5 fires on noise in haiku panels (reference 0.47) and never fires in luna panels (C-007).
- R4 has no measurable alarm.
- V3 credits `merge_guard.py:256` with a B5 cause; it is I1 (X-003).

##### V4

**Steelman.** V4 is the most operable and the most internally consistent variant. All five of its gain tables are arithmetically correct (diff grid). Its scaffold carries what a merge needs:
- a baseline table with caps (V4:152-159);
- a kill switch that reproduces today's launch command byte for byte (R-05);
- the absolute board path baked into hook strings, which settles the UNVERIFIED environment-inheritance question (V4:124);
- `collab.json` telemetry with an SLO budget (R-23, R-24);
- a failure runbook for every design.

Its Axis-Flip Challenge refines my D2:
- a surface-finding filter (V4:345);
- anchor-content routing by reviewer style;
- "never back to the author";
- a combiner that keeps phase-1 lines verbatim by construction (V4:356, R-16), which is safer than my R-16. Mine relies on the model restating every phase-1 id.

V4 is also the only variant to state that the harness and collaboration shares interact (V4:184).

**Critique.**
- Idle-Shift Sweeper's worst case is 116 + 6 + 38 = 160 s, which is +37.9% and over the cap. The 125 s delivery deadline limits when a fact is delivered, not the work luna does after receiving it (V4:301).
- That design also needs luna to call `panel-seal`. luna makes about one Bash call per run (V2:414; V1:256), so the seal compliance V4's own runbook fears (V4:335) is likely.
- The experiment's n = 4 is a screen. Its reach rule "2 or more of 4 and +2 vs A1" (V4:666) passes at a one-sided Fisher p of 6/28 = 0.214 (my computation).
- The Axis-Flip timeouts disagree: 45 s in the schedule (V4:375), 35 s for luna in the time block (V4:396).
- V4 has no within-run attribution, and H is measured only against historical S07, labelled confounded (V4:656).
- Its anchors carry no decoys, so A-006 stays open.

##### V5

**Steelman.** V5 is the most honest about effect size. It is the only variant that prices designs in tokens per added issue (V5:404). It puts a static-kit row and a sonnet reference row in the comparison (V5:411-412), and it concludes that the static kit may beat every exchange design (V5:418), which is exactly the result the experiment must be able to detect. Its T2a/T2b split (V5:40) explains why anchor-based designs cannot reach B1, B2 or I4. Other strengths:
- the first-hand evidence rule (C-3; re-run mismatch >10% stops the arm) stops a bad sweep from spreading;
- Shadow Resume uses HL2's idle time for +0% elapsed and keeps a haiku canary;
- spike 5 measures part of H with judge calls alone;
- V5 verified the CLI flags against `claude --help`;
- it runs 12 runs per control arm with an interim look, which gives the best power of the five.

**Critique.**
- The adoption clause "4 vs at most 1, Fisher p at most 0.10" (V5:457) gives p = 96/792 = 0.121 at n = 6 (I re-derived it), so a pass path fails its own threshold.
- The `note` field of up to 120 characters (V5:117) can carry a conclusion without a listed verdict word (X-007).
- H-4 and H-6 change the brief's grading and the judge input inside the "harness share" (X-008).
- The 0.25x-2x band is fixed, not derived per issue (C-008).
- The 6th-tool-call gate leaves no auditable sealed artifact (C-006).
- Sweep Desk's Stop-hook wait loop is V5's own "most complex piece" (V5:309).
- Shadow Resume needs HL2, which costs about 3x the tokens of EL2 per package (63.7k vs 21.2k).

#### Strengths claimed

1. **The theory structure maps cleanly to designs.** The three-gate funnel (V2:11) with a per-issue table naming the blocked gate and the peer move that could open it (V2:81-94) is the only theory layout that says which gate collaboration *cannot* open. Gate C, survival, belongs to the harness only (V2:79). That one rule forces the H/C split in every gain block.
2. **Decoys are the only defence against the location signal (A-006).** One challenge in three points at a place no peer flagged, chosen by a trigger regex (V2:240, :266). Every other F1 design (V1-R3, V4-3, V5-D5) sends real peer locations with no defence.
3. **The attribution design separates harness, catalogue and communication.** A fresh A0 on the current harness (V2:509) measures H contemporaneously. V1, V4 and V5 compare against historical runs from other dates and CLI versions. A2 isolates the catalogue, and "communication value = arm - A2" is explicit (V2:512-513). Within-run C, judging the merged sealed reports under separate random labels (V2:517, R-25, R-28), measures collaboration inside the same run with no extra arm. R-28 forbids reporting one combined number.
4. **The time box is tied to the named baseline.** D2's phase 2 is bounded by `min(35, 150 - start - 4)` from panel start (V2:251, R-15). Every phase 2 therefore ends by 150 s, +29% of the named 116 s, whatever T1 is. V1-R3's bound scales with the run's own T1.
5. **The natural seal needs no compliance.** For Stop-delivered designs, the first Stop is the seal (V2:133). luna never has to call a seal helper, which avoids V4-2's luna Bash-compliance risk.
6. **Evidence for pointer-following.** luna read source.md in 48 of 48 control runs vs 11 of 48 alias runs (V2:27). This is the strongest data point that a pointer changes luna's behaviour, and it licenses the F4 slot.
7. **Strict message validation.** No free text and forbidden keys listed (V2:129). Quotes must be verbatim and located, and paths must exist in the sandbox (R-9). Sender claim strings are grepped out of delivered text (R-10).
8. **Verified statistics.** 4/6 vs 0/6 gives p = 15/495 = 0.030 (V2:526; confirmed). Requiring both significance against A1 and +2 runs against A2 credits the catalogue, not communication, when exchange adds nothing.
9. **Reasoning budget rejected with within-model data.** Ember is 0.25 vs 0.22 and luna 0.09 vs 0.09 hard hits between the low- and high-thinking halves (V2:13).
10. **I6 propagation is kept in a reliable transport.** D3 (V2:295) is the only peer-discovered trigger for I6. Its idea survives in D2's flip table without SendMessage: a `contradiction` finding produces "M7 on all tasks" (V2:226).

#### Concessions

1. **D1 time-guard prose is wrong.** I confirm the diff analysis. `min(2, floor((150 - t - 12) / 11))` reaches 0 for t above 127 s, not "135 s or later" (V2:182). R-20's test points (100, 125 and 140 s give 2, 1 and 0) are consistent; only the sentence is wrong. The formula also needs a clamp at 0.
2. **D1's I7 range is too high.** The lunas receive disjoint locators (V2:159), so only one luna gets the test file. The single-luna chain is 0.7 x 0.8 x 0.3 = 0.17 to 0.9 x 0.8 x 0.6 = 0.43. The diff analysis flagged only the high end; my stated low end of 0.25 is also above its chain. The corrected range is 0.17-0.43 /2, in both V2:204 and the section 3 table.
3. **D5's B5 row is off.** 0.2-0.4 x 0.3-0.6 = 0.06-0.24, not 0.04-0.20. The design total becomes 0.10-0.46.
4. **D2's I5 high end needs both lunas to draw ember's I5 anchor.** That reading is legitimate (V2:232), but it should be stated.
5. **D2's B1 figure of 0.05-0.25 is optimistic** (X-011). The route is a sweep of all acceptance criteria triggered by a peer's B3 finding, not an AC3 anchor, so V5's T2b objection applies only partly. Still, no model has ever made the B1 move. The high end should be about 0.10. Decoys also take 1 of 3 slots, and the gain table does not discount for that.
6. **D3 has no enforced time box and only partial independence** (V2:317, :327). It should not enter the slate as specified.
7. **D4 conflicts with my own blind-spot principle.** Its mid-run "cells peers already covered" notes (V2:359) are the clearance signal that V5's C-2 and V1-R1 warn against. With luna at about one Bash call per run, cell logging is also improbable (V2:414).
8. **S14 (D5) is not a seed baseline.** It is measured (CR:320) but not in SEED:25.
9. **Spike S0 tests only that hooks fire, not that models act** (A-001). V1's REQ-S3 is better.
10. **My R-16 relies on the model restating the phase-1 ids.** V4's combiner is the better approach.

#### Shared assumptions

- A-001: QUALIFY. Delivery is testable, but no act rate is grounded. Adopt V1 REQ-S3 (the next tool call follows the injection) and replace every gain's act rate with the spike's measured value.
- A-002: REJECT. Budgets built on 116 s assume that the catalogue and harness fixes do not lengthen runs. V5 estimates +29% for the static kit. Re-base every time block on A1/A2 medians from spike 4. Absolute-from-start time boxes (V2-D2) at least keep the cap whatever phase 1 does.
- A-003: QUALIFY. Random labels and stripped markers are necessary but not sufficient. Add precision (credits per finding) and the sealed-vs-final within-run comparison, so that more findings cannot be read as more discovery.
- A-004: REJECT. Collaboration on B5, I1 and I4 depends on H1 and H3 (V4:184). Measure C only as a difference between arms that both carry H, and never sum shares in the headline.
- A-005: QUALIFY. Dividing by 3 is a mean, and a per-package cap applied to a mean is loose. Confirm against per-run `wall_s` (V5:539).
- A-006: REJECT. A location is a signal. Every design that sends peer anchors needs decoys (V2-D2) and an echo alarm.
- A-007: ACCEPT. Gate it on a spike, keep the fresh-session fallback (V2:286, V4:384), and log `resume_fallback`.
- A-008: QUALIFY. Bash is unrestricted, so read-only is a policy. Require helper writes only under `$BOARD` plus a clean `git status` after every run (V4 R-09, V2 R-5).
- A-009: ACCEPT. Use V1's mechanical deny-list before the runs and V2's confirmation on two new packages before adoption.
- A-010: ACCEPT. It is the replicated, cheapest default; designs that need another panel run as second-stage arms.
- A-011: ACCEPT as judgment. Cap the conversion rates with V5's calibration (the c-values sum to SL2's measured reach) and label B1, B2, I5 and I6 as having no data.

#### Proposed final slate of five redesigns

| Slot | Family | Core | Grafted from | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 | V2-D2: decoys (1 of 3), unanchored tasks first, flip row `contradiction` -> M7 on all tasks (keeps V2-D3's I6 trigger), absolute time box `min(35, 150 - start - 4)` replacing the 35/45 s split; V1-R3: one gap card; V4 combiner; V2 R-25 sealed-report judging | The family four variants reached independently; deterministic, no hooks; V4-3's gain table is clean (0.23-0.94) |
| 2 | F4 Searcher-to-reader fact relay | V2-D1 | V4-2: the sweeps run in a fresh ember sweeper session that never sees ember's report; V1-R2: automatic, hash-split harvest; V5-D3: command string on every fact plus the first-hand rule C-3; corrected guard (0 locators from t > 127 s) and I7 0.17-0.43 | Theory A pointer-following (48/48); the Stop-gated natural seal needs no luna seal call, unlike V4-2; strongest I7 path |
| 3 | F3 Content-free coverage steering | V4-1 | V2-D4: Task x move cell grain from trigger regexes, so the injected gap carries a location but no peer content; V1-R1: per-receiver hash ordering of gaps; V1 `PANEL_FINISH_AT`; V4 deadline corrected to 112 s | No model authoring, so the lowest compliance risk; measures panel blind spots directly |
| 4 | F5 Structural index / source witness | V2-D5 | V5-D1: kind -> move index entries in the same single ember post; V1-R4: unnamed-referrer item; B5 row corrected (0.06-0.24); EL2 variant with at most 2 witness lines per luna (116 + 20 + 12 = 148 s, +27.6%) alongside the S14 form | The only design aimed at source-only rules masked by the checkout (B5, I1, B2) |
| 5 | F6 Steering a running strong model | V4-5 | V2-D4: the Stop-time assignment of 2 uncovered cells to sonnet; V1-R5: request semantics, delivered by the harness instead of SendMessage; V4 surface filter kept | Harness-generated with a Claude receiver; deflects the one model that already sweeps; gain table clean (0.26-1.06) |

F2 (mid-run method relay) and F7 (directed challenge) are left out because they rely on gateway models authoring sends mid-run, which carries the highest compliance and free-text risk. Their key idea, propagation, survives in slot 1's flip table.

Proposed base document: V4. It has the most complete scaffold (baseline table, kill switch, timing constants, telemetry, runbooks, and R-01..R-30 with a verification column), zero gain-table errors, and three of the five cores. Its theories section takes V2's gate table. Its experiment takes V2's arm design (fresh A0, catalogue arm, within-run C) at at least 6 runs per arm, with V5's 12-run controls, in place of V4's n = 4 screen.

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | Full (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Most complete scaffold: baselines, kill switch, rejected transports, timing constants |
| S-003 | V2 | The gate funnel names the blocked gate per issue and fixes the H/C split |
| S-004 | V5 | Only table with net collaboration, a static-kit row, a harness row and tokens per issue |
| S-005 | V4 | Tabled IDs with a verification column, tied to specific designs |
| S-006 | V4 | Not-checked list plus explicit risks |
| C-001 | V2 | "Frontier seeded by citations" covers both unnamed dependents and seen-not-opened, with 48/48 evidence |
| C-002 | V5 | The T2a/T2b split correctly predicts which designs can reach B1, B2 and I4 |
| C-003 | V1 | Truncate, validate and re-ask once, with grading held constant |
| C-004 | V4 | Ten moves with a best-style column the routers need |
| C-005 | V4 | 12-200-character exact anchors match findings-v1, so peer anchors pass intact; add V2's located-quote and path checks |
| C-006 | V2 | The natural seal (first Stop) plus process-exit seals cover four of the five slate designs with no compliance |
| C-007 | V4 | Relative and ground-truth-free (J + 0.15, ledger rows -20%) with per-design echo thresholds |
| C-008 | V4 | Same per-issue chain method as V2, executed without arithmetic errors |
| C-009 | V2 | Four separate rows (H, catalogue, communication, within-run C), never combined |
| C-010 | V2 | The only design with a fresh old-harness arm and a catalogue arm at 6 runs |
| C-011 | V2 | One pre-registered endpoint, verified p, catalogue credited when X does not beat A2 |
| C-012 | V1 | Uses only seed baselines (EL2, HL2, SL2) |
| C-013 | V1 | `PANEL_FINISH_AT` is the only panel-level enforcement for mid-run designs |
| X-001 | V5 | Bottom-up per fix (+0.14, 0.03-0.34), measurable by spike 5; V3's 0.8-2.1 is contradicted |
| X-002 | V1 | Correct: 0 on /14 and up to -0.33 on sonnet control; a removal cannot add finds |
| X-003 | V1 | GT6 = I1, matching SEED:71 |
| X-004 | V5 | Haiku is legal against HL2, and Shadow Resume exploits that idle time |
| X-005 | V1 | The slowest luna, 116 s, is the critical path, per SEED:98 |
| X-006 | V4 | Combiner-built single block with phase-1 lines verbatim and origin stripped before judging |
| X-007 | V2 | Explicit forbidden keys and no free text; V5's note can carry conclusions |
| X-008 | V1 | Grading and judge held constant, judge template pinned by sha256 |
| X-009 | V1 | Truncation plus parser validation plus one re-ask closes both drop paths |
| X-010 | V5 | Quantifies that the static kit may beat exchange and requires the A2 comparison |
| X-011 | V5 | No AC-level anchors exist, so anchor-based B1/B2 gains must stay near zero |
| X-012 | V2 | I7 is kept on control /2 throughout (V2:3) |
| X-013 | V2 | 4/6 vs 0/6 gives p = 0.030, verified |
| A-001 | V1 | REQ-S3 is the only spike that tests acting on an injection |
| A-002 | V5 | The only variant to price the kit's runtime (+29%) and plan to re-measure turns |
| A-003 | V2 | Random labels plus within-run sealed-vs-final judging give the only internal control |
| A-004 | V4 | States the H-C dependency explicitly |
| A-005 | V5 | States it as unverified and requires per-run `wall_s` confirmation |
| A-006 | V2 | Decoys are the only defence against the location signal |
| A-007 | V4 | Spike, fresh fallback, `resume_fallback` metric and session cleanup |
| A-008 | V4 | Helpers write only under `$BOARD`, verified by a clean `git status` (R-09) |
| A-009 | V2 | Confirmation on two new packages; add V1's deny-list |
| A-010 | V1 | States why: the cheapest replicated panel, where cheap-model collaboration matters most |
| A-011 | V5 | The c-values are calibrated so their sum equals SL2's measured hard reach (a ceiling) |

### Variant 3 Advocate (haiku:backend)

### Round 1 statement: V3 advocate (haiku backend lens; persona: backend, focus on data integrity, scalability, fault tolerance)

#### Position summary (1-3 sentences)

V3 is the weakest scaffold of the five and should not be the base. Its gain blocks do not follow from their own inputs, and its harness share is overstated about 3x. What it does contribute is a set of integrity controls: a sealed first-pass artifact, a cross-reviewer anchor-leak check, reject-not-truncate caps, a frozen and hashed enum, and run-scoped settings with a hash check. These belong in the merged spec on top of V4's scaffold. V4 has the most complete substrate and supplies four of my five slate cores.

#### Steelman and critique of each other variant (one subsection per variant: steelman first, then critique with evidence)

##### V1 (architect lens)

**Steelman.** V1 is the only variant that makes the +35% cap enforceable at panel level. `PANEL_FINISH_AT = T0 + 1.20 x B` injects "finish now", stops Stop-blocking and makes the send helper refuse (V1:138). It also gives the phase design a per-run hard kill at `1.35 x T1 - 2 s` (V1:323). Its H2 combines truncation with a parser check and one re-ask (V1:107), which is strictly safer than V4's re-ask-only path, and it holds the grading rule constant (V1:111). That makes "harness share" a clean quantity. R2 Evidence trail is the most fault-tolerant design in the field: neither end needs model action, and paths are hash-split (V1:237). Its experiment has the static-catalogue arm that separates "the move list helps" from "the exchange helps" (V1:548). Its baselines are all seed baselines (EL2, HL2, SL2).

**Critique.**
- V1-R3's guarantee is relative to the run's own T1, not to the named baseline (V1:323). A slow phase 1 (A2 brief plus H1 makes runs longer, A-002) therefore widens the window. The kill must be `min(1.35 x B_named, 1.35 x T1) - 2 s`.
- V1-R4's total of +0.05 to +0.45 does not match its rows: low 0.12 - 0.10 = 0.02, high 0.60 (V1:426-432).
- In V1-R2, the I7 high of 0.35 exceeds its own chain, 0.45 x 0.7 x 0.85 = 0.27 (V1:279).
- R1 and R4 depend on gateway models posting cards. V1 itself names this as the weak point (V1:540).

##### V2 (analyzer lens)

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

##### V4 (devops lens)

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

##### V5 (performance lens)

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

#### Strengths claimed (numbered, with evidence)

1. **A file-based seal with a timestamp check.** For mid-run designs, a `pass1.md` must exist before any peer content is released, and its timestamp must be earlier than the first peer line received (V3:56, req 10). This turns "independent first pass" into one auditable integrity check per run. A call-count gate (V1:185, V5:120) leaves no artifact. V4's `panel-seal` does the same thing with better fallbacks, so the merge should use V4's mechanism with my timestamp test as its acceptance criterion.
2. **A cross-reviewer anchor-leak check.** A board line that contains a 12-character or longer substring of another reviewer's anchor is a hard failure (V3:88, req 11). This is a mechanical, ground-truth-free test that a content-free channel really is content-free. V4's check (V4:671) compares against ground truth, which a product cannot do. The two are complementary. Mine applies only to designs that promise to carry no anchors (Radar, Deflection), not to F1 designs, which send anchors on purpose.
3. **Caps reject oversized messages instead of truncating them** (V3 req 8). Truncating a message silently changes what a peer receives. Rejecting it keeps the board an exact record. V4 R-06 agrees, but V1 H2 and V5 H-2 truncate *findings* (correctly) and say nothing about *messages*. The merge must state the rule for messages explicitly.
4. **Configuration integrity.** The move enum is hashed before the arm starts, and any change invalidates the arms that used the old hash (req 18). Hooks are run-scoped through `--settings`, and the user's `~/.claude/settings.json` sha256 must be equal before and after the experiment (req 17). No other variant tests that the panel leaves host configuration untouched.
5. **A sequential power plan.** V3 gives an explicit power estimate (about 60% for +1.0 at n = 10, SD 0.94, V3:163), an extension rule that is triggered only by stated conditions (V3:160), and double-scoring of a random sample by a second judge (V3:167). The diff analysis judges the power estimate "approximately right" (X-013). V5's interim look (V5:454) is the same idea with better arm structure.
6. **Honest risk ratings.** R4 is rated High contamination risk (V3:110), not argued away.

#### Concessions (own weaknesses)

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

#### Shared assumptions (one line per A-001..A-011: `A-NNN: ACCEPT|REJECT|QUALIFY — reason`; omitting any is flagged)

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

#### Proposed final slate of five redesigns

| Slot | Family | Core redesign | Grafted parts (ids) | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 (1 decoy in 3; flip table); V1-R3 (gap card; kill at min(1.35 x B_named, 1.35 x T1) - 2 s); V2 sealed-report judging (U-006); V5-D5 (HL2 shadow variant with an isolated haiku canary) | Most fault-tolerant: seal by process exit, harness-only delivery, phase-1 fallback. 148 s = +27.6% of EL2 116 s; HL2 variant +0-6%. |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V1-R2 (automatic seen-not-opened harvest, hash-split); V5-D3 (first-hand re-run rule; >10% mismatch stop); V2-D5 (source-rule witness as one sweep kind); V3-R3 (hard `timeout` on the sweeper session); luna limited to 2 acted facts | The only cheap path to I7 (T1). With 2 facts: 116 + 6 + 26 = 148 s = +27.6%, which fixes V4-2's 160 s (+37.9%) worst case. |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V1-R1 (region x move gap grain; per-receiver hash order); V5-D4 (rotating permutation so reviewers do not share a gap); V3-R2/R5 (12-character cross-reviewer leak check, hard failure); V3-R1 (end-of-phase move-gap digest via `--resume` as fallback if hooks fail spike S0) | Zero model authoring, so no gateway compliance risk. 144 s = +24%. Its rival is the static catalogue arm, which the experiment measures. |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection | Moved to SL2 (seed baseline 274 s, cap 369.5 s) per V1-R5; V1-R5 requests rendered by the harness from luna's "not checked" scope (no SendMessage); V2-D4 (Task x move cell grain); V4 surface filter (U-014) | Harness-authored cards and a Claude receiver are the lowest-risk mid-run path. 274 + 56 worst = 330 s = +20%. |
| 5 | F7 Directed challenge / adjudication | V4-4 Flag-and-Adjudicate | V3-R4 (cross-session SendMessage only as a spike-gated fallback); V5 C-3 (first-hand evidence); V1 PANEL_FINISH_AT at 1.20 x 100 s; V2 decoy card | Answers the seed's open question "challenge vs shared findings" with a mandatory finite-check answer. On ember+luna (seed 300/3 = 100 s): typical 119 s (+19%), worst 132 s (+32%). |

F2 (V5-D2, V2-D3) is dropped. It is F1's axis flip done mid-run with model-authored posts, which adds compliance risk and no new mechanism. F5 (V1-R4, V5-D1, V2-D5) is folded into slot 2's fact kinds as the witness and referrer sweeps.

Proposed base document: V4. It has the most complete substrate (catalogue with style routing, schema, baked board path, kill switch, telemetry, SLO, runbooks), and it supplies four of the five cores. Two parts must be replaced. Its experiment and statistics should come from V2: the arm structure, the Fisher-verified decision rule and sealed-report judging, at V5's 12-run size. Its theories should be extended with V5's T2a/T2b split.

#### Per-point positions

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

### Variant 4 Advocate (opus:devops)

### Round 1 statement: V4 (devops lens)

Citations: `V<n>:<line>`, `DA:<line>` for `diff-analysis.md`, `SEED:<line>` for the seed brief. I recomputed all V4 arithmetic below myself.

#### Position summary

V4 should supply the merged spec's scaffolding: the kill switch, the board path baked into hook commands, hooks that cannot fail a review, `collab.json` telemetry, the SLO error budget and a runbook per design. It should also supply three family cores that no other variant matches (Move Radar F3, Flag-and-Adjudicate F7, Coverage Deflection F6). V4 does not win everything. V2 should supply the F1 core, the theory gate table and the decision rule. V5 should supply the three-way gain split. V1 should supply the harness fix for long anchors and the panel deadline. V4-2's worst case breaks the +35% cap as written.

#### Steelman and critique of each other variant

##### V1 (architect)

**Steelman.** V1 is the most disciplined architecture of the five. All designs run as policies on one shared substrate (V1:100), so five designs do not mean five harnesses. Its deadline rule `PANEL_FINISH_AT = T0 + 1.20 x B` (V1:138) is the only panel-level, per-package mechanism that turns +35% from a hope into a guarantee for mid-run designs. In the evidence trail (V1-R2, V1:237) neither sending nor receiving needs the model to act, which removes gateway compliance at both ends. Its H2 truncates long fields, validates them with the real parser and re-asks once (V1:107), so no finding can be silently lost; V4's H2 does not achieve this. It also holds the grading rule constant (V1:111). Spike REQ-S3 (V1:614) is the only spike that checks a gateway model *acts* on injected text, not just that the hook fired. And V1-R3's gap card (V1:303) is the only F1 mechanism that points a reviewer at a region nobody anchored, which matters for B1/B2 (see X-011).

**Critique.** V1-R2's I7 high of 0.35 exceeds its own chain: 0.45 x 0.7 x 0.85 = 0.27 (V1:279; recomputed). V1-R4's stated 0.05-0.45 does not follow from its rows. The rows sum to 0.12-0.60, minus displacement 0.10-0, which gives 0.02-0.60 (V1:426-432). V1-R3's hard kill is 1.35 x T1 of the same run (V1:323), not 1.35 x the named S07 baseline. Phase 1 there also carries the catalogue and H1 (V1:300), so T1 can exceed 116 s and the guarantee drifts. REQ-S2 (V1:613) depends on hooks inheriting environment variables. Baking the board path into the hook command (V4:124) removes that dependency instead of testing it. R1 and R4 depend on gateway models posting cards (V1:540); R5 rests on SendMessage.

##### V2 (analyzer)

**Steelman.** V2 has the best theory frame: a three-gate funnel (exposure, question, survival) with a per-issue table naming the blocked gate (V2:83-94). It has the best piece of collaboration evidence: luna read source.md in 48 of 48 control runs, where tasks cite it, against 11 of 48 alias runs (V2:27). That number shows pointers change luna's behaviour. D2's decoys (V2:240, :266) are the only defence against the signal carried by a peer anchor's location ("a peer found something here", A-006). Its time box `min(35, 150 - start - 4)` (V2:251) is anchored to panel start, so it binds against the named baseline. Its decision rule uses a correct Fisher threshold (4/6 vs 0/6, p = 0.030; recomputed). Within-run attribution (V2:517, R-28) judges sealed reports separately, which measures collaboration without a separate arm. R-17 (V2:563) catches a real pitfall: a resumed prompt must not start with a slash command. Its confirmation step uses two new packages (V2:531).

**Critique.** D1's time guard is wrong as stated: `min(2, floor((150 - t - 12)/11))` is already 0 at t = 128 s, not 135 s (V2:182; recomputed). D1's I7 high of 0.60 exceeds the single-luna chain 0.9 x 0.8 x 0.6 = 0.43, and the lunas get disjoint locators (V2:159), so "two lunas" cannot double it. D1 also assumes a Stop block yields a reissued full report (V2:172), which is unverified; if it fails, the fallback discards the gain. D3 has no harness-side time box (V2:317), no send validation and no durable log. D4 depends on luna calling `panel-cover`, but luna makes about 1 Bash call per run (V2:414). D2's flip table routes on the peer's category, while V4-3 routes on anchor text (V4:349-354). Anchor-text routing sends a grep sentence to M4/M7, the moves the 16 I5 near-misses lacked.

##### V3 (backend)

**Steelman.** V3 takes the seed's first ranking seriously: "simplicity and speed of implementation rank first" (SEED:31). Its designs are the shortest to build (50-175 lines). It contributes a cheap mechanical leak check: no board line may contain 12 or more characters of another reviewer's anchor (V3:88). It adds an extension rule (10 to 20 runs) for borderline results (V3:160), a double-scored judge sample and a mandatory unseen fourth package before adoption (V3:191). Its first-pass seal (`pass1.md`) is an auditable artifact (V3:56).

**Critique.** Requirement 6 places collaboration findings outside the findings-v1 block (V3:176), so the merge and the judge never see them and every collaboration gain would score zero. It also contradicts R1 (V3:73). I7 is counted inside "/14" (V3:78, :100). The harness share of 0.8-2.1 (V3:126) exceeds every other variant's high end, and the seed's own data contradicts it: cheap readers of source.md still missed B5 and I1 (V2:144). The 14 s "fixed overhead" (V3:69) misreads the baseline. 116 s is the slower of two luna draws, not luna's 102 s median plus overhead. The gains do not follow from their inputs: R1 is 5 x 0.6-0.9 x 0.15-0.4 = 0.45-1.8, but V3 states 0.4-1.2. V3 also says `merge_guard.py:256` repairs B5; it repairs I1 (SEED:71). The absolute Jaccard alarm of 0.5 sits just above the ember+haiku reference of 0.47 (V3:77), so it fires on noise in haiku panels and never fires in luna panels. There is no static-catalogue arm, so V3's experiment cannot separate the move list from the exchange. Finally, `pass1.md` must be written through Bash, which V3's read-only rule (req 1) does not restrict.

##### V5 (performance)

**Steelman.** V5 is the most intellectually honest variant on the core question. It estimates that a static move kit in the brief may beat every exchange design on gross gain (V5:411, :418), and it builds the experiment so that communication must beat that kit. Its three-way split (harness A1-A0, prompting A2-A1, collaboration arm-A2; V5 E-5) is the only gain decomposition that answers SEED:102 cleanly. The T2a/T2b split (V5:40) correctly reads the B1/B2 evidence: Task 1 is anchored, AC3 never is. Shadow Resume (V5-D5) gets +0% elapsed with an isolated haiku canary, which uses idle time well and gives a clean within-run reference. The first-hand evidence rule (V5 C-3, :299) stops a bad peer sweep from spreading as evidence. V5 also verified `--help`: `--max-turns` does not exist, so turn caps need a hook counter or `timeout` (V5:106). Its spike 5 re-scores the 30 cheap runs to measure the 200-character drop directly (V5:433).

**Critique.** The pass path "at least 4 runs vs at most 1 for A2 (Fisher p <= 0.10)" (V5:457) cannot be met. One-sided Fisher for 4/6 vs 1/6 is 112/924 = 0.121; I recomputed it. A `note` of up to 120 characters is filtered only for verdict words (V5:117-119), so "grep misses root files" passes and carries a conclusion (X-007). H-4 (MINOR notes) and H-6 (judge scores the raw union) change the rubric and the judge input, yet are counted in the "harness share" (X-008). The independence gate is a call count (C-1), not an artifact. The 0.25x/2x band (V5:139) is fixed, not derived per issue. D2's caps conflict: "2 injections in" (V5:224) against 3-5 flips in its time block (V5:236-237).

#### Strengths claimed

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

#### Concessions

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

#### Shared assumptions

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

#### Proposed final slate of five redesigns

| Slot | Family | Core redesign | Parts grafted from other redesigns | Reason |
|---|---|---|---|---|
| 1 | F1 between-phase cross-examination | V2-D2 Axis-Flip Cross-Examination | V4-3 (anchor-text routing table, surface filter, immutable phase-1 lines plus a `P2-F` combiner, haiku variant at +22% of 238 s); V1-R3 (gap card toward never-anchored regions, filling D2's decoy slot, so the decoy also reaches T2b issues B1/B2/I4); V5-D5 (isolated haiku canary in the HL2 variant) | Most reliable family (process-exit seal, no hooks); decoys answer A-006; V2's time box binds against the named 116 s baseline (+25%/+29%) |
| 2 | F4 sweep service | V4-2 Idle-Shift Sweeper (fixed) | V1-R2 (automatic seen-not-opened harvest); V2-D1 (ranked disjoint locators per luna, unnamed tests first); V5-D3 (command string in every fact, first-hand re-run rule, mismatch above 10% stops the arm); V1 finish signal bounding the Stop hold; at most 2 facts per luna and a hook-side seal (144 s, +24%; worst 150 s, +29%) | Only cheap-panel path to I7 and I5 (T1); the sweeper is a fresh session that never sees ember's report, and it runs entirely in ember's idle window |
| 3 | F3 content-free coverage steering | V4-1 Move Radar | V2-D4 (harness-built Task x move cell matrix, giving region-level grain); V1-R1 (gap order hashed per receiver, so the two lunas never get the same gap) | Zero model authoring; directly measures panel blind spots; +24% equals its worst case |
| 4 | F7 directed challenge | V4-4 Flag-and-Adjudicate | V2-D5 (source-rule witness lines become harness-generated cards, so B5/I1/B2 reach does not depend on ember posting); V5-D1 (kind-to-move pairing for flagged sentences); V5 C-3 first-hand rule | The only design testing the seed's challenge question with a mandatory finite-check answer from a different model; on seed baseline S13 (100 s), +19%/+32% |
| 5 | F6 steering a running strong model | V4-5 Coverage Deflection | V1-R5 (per-luna move requests, but rendered by the watcher from finished blocks, not sent with SendMessage); re-based on seed baseline SL2 (274 s): 274 + 28 + 28 = 330 s, +20.4% worst; V5 C-2 (cards lead with uncovered Tasks and never mark a region "fine") | Lowest-risk receiver (a Claude model, cards made by the harness); turns cheap reviewers' finished work into steering for the one model that already sweeps |

Proposed base document: V4. The merged spec's bulk is five complete redesigns plus testable requirements. V4 has the most complete per-design template (a-h plus runbook), the operability requirements (R-05, R-21 to R-26), and three of the five slate cores. Two parts should be imported in place of V4's own: from V2, the gate table (section 1) and the experiment design with its decision rule (section 4); from V5, the three-share split.

#### Per-point positions

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

### Variant 5 Advocate (sonnet:performance)

### Round 1 statement: V5 advocate (sonnet, performance lens)

#### Position summary

V5's lasting contribution is not a single design. It is the accounting: each gain is split into harness, prompting and collaboration shares; the static-kit control shows communication must beat a free checklist; and every time budget treats the critical path as the slowest reviewer, where any wait breaks the cap. On mechanisms, V4 has the best cores in three families and should be the base document. V5 supplies one core (F5) and the grafts on time, cost and evidence.

#### Steelman and critique of each other variant

##### V1 (architect)

**Steelman.** V1 has the best theory and enforcement. Its T1 refinement says the two halves of the missing move sit in different models: haiku and ember search, luna reads (V1:25-45). That is the only theory that predicts a gain a static checklist cannot copy, and it licenses the whole F4 family. Its panel deadline `PANEL_FINISH_AT = T0 + 1.20 x B` (V1:138, U-001) is the only panel-level mechanism that makes +35% enforceable for mid-run designs. It also holds the grading rubric constant in every arm (V1:111). Its harness fix H2 truncates, validates and re-asks once (REQ-H2, H3), so the merge parser is untouched and nothing is dropped. V1-R2's evidence trail needs no model action at either end (U-002).

**Critique.**
- V1-R3's hard cap is `1.35 x T1` of the same run (V1:323), not 1.35 x the named 116 s baseline. Phase 1 runs with the longer A2 brief, so T1 can grow, and the "+35%" guarantee floats with it.
- Arithmetic. V1-R2 claims an I7 high of 0.35, but its own chain gives 0.45 x 0.7 x 0.85 = 0.27, and the hash split means only one luna gets the file (V1:279). V1-R4's rows sum to 0.12-0.60, minus up to 0.10 for displacement, which gives 0.02-0.60, not the stated 0.05-0.45 (V1:426-432). I recomputed both.
- Performance. R3 resumes the whole session history as input tokens (V1:376), and V1 does not count that cost. R5 rests on cross-session `SendMessage` from gateway models, which is unverified at both ends (V1:469-473).
- V1's experiment makes found /14 the primary endpoint at n = 6, where V1 itself says only about +1.0 per run is detectable (V1:599). That is larger than any design's central estimate.

##### V2 (analyzer)

**Steelman.** V2 is the most careful about contamination and statistics. Decoys (1 of 3 challenges at a place no peer flagged, V2:240) are the only defence against the location-as-signal leak (A-006). Every other F1 design, mine included, sends real peer anchors bare. V2's schema forbids free text and requires `target.quote` to be a located verbatim substring (V2:116-131). Its decision rule is statistically correct: 4/6 vs 0/6 gives p = 0.030, and I confirmed it. The rule also requires beating A2 by 2 runs (V2:526) and confirming on two new packages (V2:531). Judging the sealed reports under separate labels (R-25, R-28) measures collaboration within the same run, at the cost of judge calls only.

**Critique.**
- V2-D1's prose says a luna that stops at 135 s gets no locators. Its own formula gives 0 from t = 128 s (V2:182). R-20's unit test (100/125/140 s) is consistent, so this is a prose error. More serious: the I7 high of 0.60 exceeds the single-luna chain 0.9 x 0.8 x 0.6 = 0.43, and the lunas receive disjoint locators (V2:159).
- D3 has no harness time box (V2:317), so the cap is measured, not enforced. That is unacceptable on the performance lens.
- D4 and D5 sit on sonnet panels (274 s, 225 s). D5's S14 baseline is not in the seed list.
- D2 waits for a report "from a reviewer of a different model", so ember idles until about 102 s.

##### V3 (backend)

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

##### V4 (devops)

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

#### Strengths claimed

1. **Clean arithmetic.** The grid marks Time = Y for all five V5 designs, and every gain total is correct (D1 0.21, D2 0.178, D3 0.2285, D4 0.16, D5 0.275); I re-added D1-D3 row by row. Only V4 matches this on gains, and V4-2's worst case is over the cap.
2. **A static-kit control and a three-way gain split.** Gains split into harness (A1-A0), prompting (A2-A1) and collaboration (arm-A2) (V5:141, E-5; C-009). The table adds a net-collaboration column, a static-kit row and a sonnet reference row (V5:404-413; S-004). This puts a number on X-010: the kit's gross 0.33 beats every exchange design, so communication must beat A2 (V5:418-419).
3. **Cost per issue and scaling.** c (sum 1.04) is capped against sonnet + 2x luna's measured hard reach of about 1.0 per run (V5:94, U-015). "Output tokens per added issue" is the only cost-to-serve figure in any variant: the sonnet reference costs about 150k, the cheap designs 47-100k. Every schedule states its scaling with n, because a fact computed once costs O(1) and redone by every reviewer costs O(n) (V5:58).
4. **No waiting on the critical path.** "Luna must never wait for a result. A 15 s wait would add 15 s and break the cap" (V5:297). This rule catches V4-2's 15 s hold.
5. **Shadow scheduling.** V5-D5 runs phase 2 while a slow member is still working: +0% on haiku + 2x luna, worst case +6%, with a 15 s kill rule and haiku as an isolated canary (V5:385; U-016). It is the only F1 schedule with no elapsed cost.
6. **First-hand evidence.** A peer fact may be cited only if the receiver re-ran the command, and a re-run mismatch above 10% stops the arm (V5:299, C-3; U-017). This is the only guard against a peer's faulty sweep spreading as evidence.
7. **Checked facts and cheap spikes.** `--max-turns` is absent from `claude --help`, so turn caps need a hook counter and `timeout` (V5:106). Spike 5 re-scores the 30 cheap runs with the normalizer for judge calls only (U-018).
8. **Experiment size.** A1 and A2 get 12 runs each; exchange arms get 6, extended to 12 after an interim look; run order is block-randomized (V5:437-454). That is the largest control sample of the five variants.

#### Concessions (own weaknesses)

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

#### Shared assumptions

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

#### Proposed final slate of five redesigns

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

#### Per-point positions

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

### Round 1 tally

### round1: advocates=5 need=4 agreed=37/43 convergence=0.860
| Point | Level | Votes (V1 V2 V3 V4 V5) | Leader | Count | Status |
|---|---|---|---|---|---|
| S-001 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| S-002 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| S-003 | L1 | V2 V2 V5 V2 V1 | V2 | 3/5 | split |
| S-004 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| S-005 | L1 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| S-006 | L1 | V5 V4 V5 V5 V5 | V5 | 4/5 | agreed |
| C-001 | L2 | V2 V2 V1 V2 V1 | V2 | 3/5 | split |
| C-002 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| C-003 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| C-004 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-005 | L2 | V2 V4 V4 V2 V2 | V2 | 3/5 | split |
| C-006 | L3 | V4 V2 V4 V2 V4 | V4 | 3/5 | split |
| C-007 | L3 | V5 V4 V4 V4 V4 | V4 | 4/5 | agreed |
| C-008 | L2 | V4 V4 V2 V2 V4 | V4 | 3/5 | split |
| C-009 | L2 | V5 V2 V5 V5 V5 | V5 | 4/5 | agreed |
| C-010 | L2 | V2 V2 V2 V2 V5 | V2 | 4/5 | agreed |
| C-011 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| C-012 | L2 | V1 V1 V1 V1 V5 | V1 | 4/5 | agreed |
| C-013 | L3 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-001 | L2 | V5 V5 V5 V5 V2 | V5 | 4/5 | agreed |
| X-002 | L2 | V1 V1 V1 V1 V2 | V1 | 4/5 | agreed |
| X-003 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-004 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| X-005 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-006 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| X-007 | L2 | V2 V2 V4 V2 V2 | V2 | 4/5 | agreed |
| X-008 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-009 | L3 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-010 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| X-011 | L2 | V5 V5 V5 V5 V1 | V5 | 4/5 | agreed |
| X-012 | L2 | V1 V2 V1 V4 V1 | V1 | 3/5 | split |
| X-013 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-001 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| A-002 | L3 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| A-003 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-004 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| A-005 | L3 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| A-006 | L3 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-007 | L2 | V4 V4 V4 V2 V4 | V4 | 4/5 | agreed |
| A-008 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| A-009 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-010 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| A-011 | L2 | V5 V5 V2 V5 V5 | V5 | 4/5 | agreed |
coverage L1: 3 points debated
coverage L2: 31 points debated
coverage L3: 9 points debated

## Round 2: Rebuttals

### Round 2 agenda (orchestrator)

### Round 2 agenda (written by the orchestrator from Round 1; neutral, no winner implied)

Round 1 tally: `round1-tally.md` (37 of 43 points agreed at >= 4 of 5; convergence 0.860; threshold 0.75).
Base document: all five advocates proposed V4.

#### Split points (fewer than 4 of 5 on one winner)

| Point | Votes V1 V2 V3 V4 V5 |
|---|---|
| S-003 theory section layout | V2 V2 V5 V2 V1 |
| C-001 refinement of seed T1 | V2 V2 V1 V2 V1 |
| C-005 message schema and size caps | V2 V4 V4 V2 V2 |
| C-006 definition of the independent first pass | V4 V2 V4 V2 V4 |
| C-008 gain model method | V4 V4 V2 V2 V4 |
| X-012 I7 counted on the /14 scale | V1 V2 V1 V4 V1 |

#### Slate disputes

1. **Slot 5 (the only slot not common to all five slates):** F5 structural index / source-rule witness (V1: core V2-D5; V2: core V2-D5; V5: core V5-D1 with V2-D5 entries) versus F7 directed challenge (V3 and V4: core V4-4 Flag-and-Adjudicate, with V2-D5 source-rule lines grafted in as harness-generated cards). Question: which is the more distinct and stronger fifth mechanism, given that F1 (axis flip) already sends "challenge" content between phases, and given the seed's open question "is a mid-run message more valuable as a challenge than as shared findings"?
2. **F1 core:** V4-3 (V1, V2, V3, V5) versus V2-D2 (V4). Grafts proposed by everyone: V2-D2 decoys, V1-R3 gap card, V5-D5 haiku shadow variant with isolated haiku canary. Open sub-questions: the phase-2 time box (V2 `min(35, 150 - start - 4)` vs V1 `min(1.35 x T1, T0 + 1.35 x B)` - 2 s vs V4 35/45 s), and whether the gap card fills the decoy slot (V4) or is extra (V1, V3, V5).
3. **F4 core and its worst-case fix:** V4-2 (V1, V3, V4, V5) versus V2-D1 (V2). The proposed fixes give different worst cases: V1 153.6 s (+32.4%, natural seal at first Stop, no seal turn), V3/V5 148 s (+27.6%, 2 facts, drop 15 s hold), V4 150 s (+29%, hook-side seal). Settle one arithmetic block.
4. **F3 grafts:** Move Radar (V4-1) core is unanimous. Disputed grafts: V2-D4 Task x move cell grain (V2, V4) vs V1-R1 region x move grain (V1, V3); V5-D4 end-of-run Stop block with rotating permutation (V1, V3, V5); V3 12-character leak check (V3).
5. **F6:** V4-5 re-based to sonnet + 2x luna (seed 274 s) is unanimous. Disputed: V1-R5 move requests rendered by the harness (V2, V3, V4) vs only uncovered-cell lists (V1, V5).
6. **Experiment section:** comparator and sizes: V2's arms (fresh A0, catalogue-only arm, sealed-report within-run scoring, Fisher p < 0.05) with V5's 12-run controls and three-share report, versus V4's n = 4 screen. Settle arms, run counts, endpoint, and decision rule in one proposal.
7. **Harness share figure (X-001 agreed on V5):** state the single range the merged spec should carry and whether H-4 (MINOR notes) is excluded (X-008 agreed on V1: grading held constant).
8. **Idle-time budgets vs A-002 (agreed V5: contradicted):** every slot's arithmetic is built on 116 s from pre-fix runs. Propose the one rule the merged spec uses so the +35% cap is measured against the right baseline (A1 harness-fixed isolated arm vs historical S07).
</content>
</invoke>

### Variant 1 Rebuttal (opus:architect)

### Round 2 rebuttal: V1 (opus, architect lens)

Citations: `V<n>:<line>`, `SEED:<line>` = `../../../seed-brief.md`. Every number below was recomputed for this round.

#### Responses to criticisms of V1

| Criticism (raised by) | Response |
|---|---|
| R3 hard kill `1.35 x T1 - 2 s` floats with the run's own T1 (V2, V3, V4, V5) | **Concede.** V1:323 and V1:331 ("0.35 x 150 = 52 s") show the window grows with a slow phase 1. Partial counter: V1's arm-level guard was already against A1 (V1:592, "median elapsed per package at most 1.35 x A1's median"). Only the in-run kill floated. Replaced in agenda 2 by a deadline tied to the named baseline. |
| R2 I7 high 0.35 exceeds its chain (all four) | **Concede.** 0.45 x 0.7 x 0.85 = 0.268. Range 0.16-0.27. |
| R4 total does not follow from its rows (all four) | **Concede.** 0.02-0.60. R4 is not in my slate. |
| R1/R4 need gateway models to post; R5 rests on SendMessage (all four) | **Concede.** None of my R1, R4 or R5 cores is in my slate. |
| Decision rule ORs three endpoints at p <= 0.10 (V2) | **Concede.** If the three tests were independent, the false-pass rate would be 1 - 0.9^3 = 0.271. The merged spec gets one pre-registered endpoint (agenda 6). |
| No fresh A0, so H is only descriptive (V2) | **Concede.** V1:594 says so. Adopt V2's fresh A0. |
| REQ-S2 depends on hooks inheriting env vars (V4) | **Concede.** Baking the board path into the hook command (V4:124) removes the dependency. REQ-S2 is dropped. |
| R3 replays the whole session as input tokens, uncounted (V5) | **Partly concede.** V1:376 names the cost but does not count it. It applies to every resume design, including V4-3 and V2-D2. The merged token metric must count resumed input tokens for slot 1. |
| Primary endpoint found /14 cannot detect the central estimates at n = 6 (V5) | **Concede.** V1:599 says only about 1.0 per run is detectable. Use reach (agenda 6). |
| R3 sends peer regions without decoys (diff analysis, A-006) | **Concede.** Fixed in slot 1 by the gap-card decoy (agenda 2). |

#### Agenda items

##### 1. Slot 5: F5 versus F7

**I switch to F7 (V4-4).** Steelman of my old slot 5: V2-D5 is the only design aimed at the source-only rules (B5, I1, B2) (V2:422-424).

Its mechanism, though, is F4's mechanism: an ember session runs a batched sweep and posts locators that a reader acts on (V2:424, :430-431). Only the fact kind differs. V3 already folds it into F4 as a sweep kind (round1-V3:124). Two "a searcher posts facts" slots in a five-slot slate break the "five distinct redesigns" criterion.

F7 is distinct from F1. In F1 the harness picks peers' anchors from finished reports, between phases. In F7 a model flags sentences mid-run, is told not to judge them, and a different model must answer each one with a finite check (V4:463-468). F7 is also the only slot that answers the seed's open question "a mid-run message as a challenge or as shared findings" (SEED:47). To answer it, the slate needs a mid-run challenge next to F4's mid-run facts.

Where the V2-D5 content goes. I disagree with V4's graft that turns witness lines into harness-generated F7 cards. V4's own note says a deterministic extractor "would be a prompt and harness change, not collaboration" (V4:523). That content belongs in A2's share. I put the witness sweep in slot 2 as a sweeper fact kind, so it stays a model's search delivered to a reader.

**Re-base F7 to EL2, one way.**
- ember flags, and the lunas adjudicate. Cards are split by a hash, so each luna gets disjoint cards and at most 2.
- There is no luna card and no ember Stop hold. Luna makes about 1 Bash call per run (V2:414), and V5's objection is "two-way compliance plus a Stop hold" (round1-V5:119).
- The seal is taken by the hook (see 3).

| F7 arithmetic | Value |
|---|---|
| S13 as written (100 s) | 100 + 25.6 + 2 = 127.6 s (+27.6%); worst 134.0 s (+34.0%), only 1 point under the cap |
| EL2 (116 s) | 116 + 2 x 2 x 6.4 + 2 = 143.6 s (+23.8%); worst 150.0 s (+29.3%) |
| Gain | V4-4's 0.16-0.93 minus the luna search-card rows B8/B6 (0.03-0.16) = **0.13-0.77 /14**; I7 0-0.10 |

On EL2, A5 (F7) against A4 (F4) tests "challenge versus findings" with the same sender, the same receivers and the same panel.

##### 2. F1 core, time box and gap card

**Core: V4-3**, unchanged. Its combiner keeps phase-1 lines verbatim (V4:356, :453), and it routes on anchor text (V4:349-354).

**Time box.** V2's principle is right: the deadline must be tied to the named baseline (V2:251). Its "- 4 s", however, double-counts the 6 s resume start that V4's per-challenge cost already includes (V4:392). For luna B the box is min(35, 150 - 116 - 4) = 30 s, which allows floor((30 - 6)/12.8) = **1** challenge. V4's 35 s fixed box holds only when T1 = 116 s. My own `min(1.35 x T1, T0 + 1.35 x B) - 2` ends at 154.6 s (+33.3%), which leaves too little headroom.

Proposed rule:
- box = min(35, T0 + 1.30 x B_A1 - start);
- challenges n = min(cap, floor((box - 6) / (2 x turn))).

| Reviewer (B = 116, deadline 150.8 s) | Start | Box | n | End |
|---|---|---|---|---|
| luna A | ~95 | 35 | 2 | 126.6 |
| luna B | 116 | 34.8 | 2 | **147.6 (+27.2%)** |
| ember (waits for both lunas, V4:394) | 116 | 34.8 | 3 (3.2 s turns) | 141.2 |

The hard bound is 150.8 s (+30.0%) for any T1. A reviewer that starts after 150.8 - 18.8 = 132.0 s gets n = 0 and keeps its phase-1 report. HL2 shadow variant (V5-D5): 238 + 6 + 2 x 23 = 290 s (+21.8%); its deadline is 309.4 s.

**Gap card fills the decoy slot (concede to V4).** luna can afford only 2 challenges. A pure decoy plus a separate gap card would leave luna 0-1 real challenges. A gap card points at a place no peer flagged, which is exactly what a decoy must be. It is rendered identically to a peer-anchor challenge, using a verbatim candidate quote from a never-anchored region that matches V2's trigger regex. It fills each slot with probability 1/3, seeded per receiver. That keeps V2's 1-in-3 ratio (V2:240), and the slot does real work on the B1/B2 route (X-011). Also keep V2's flip row `contradiction` -> M7 (V2:226).

##### 3. F4 core and its worst case

**Core: V4-2. I withdraw my "delivery at first Stop".** It costs a full report reissue on the critical path: 116 + 12 + 25.6 = 153.6 s (+32.4%). That leaves 2.6 points of headroom, which A-002 can erase. It also depends on the unverified Stop-reissue behaviour (V2:502).

One arithmetic block:

| Item | Value |
|---|---|
| ember sweeper | 41 + 6 + 10 x 3.2 = 79 s (ember's idle window) |
| luna B, 2 facts acted on, hook seal, no hold | 116 + 2 x 2 x 6.4 + 2 (hooks) = **143.6 s (+23.8%)** |
| Worst (one turn of slip at `PANEL_FINISH_AT` = 139.2 s) | 143.6 + 6.4 = **150.0 s (+29.3%)** |

Rules:
- at most 2 facts per luna;
- the 15 s Stop hold is dropped (V5's "never wait", round1-V5:67);
- late facts are logged `late` and dropped.

**The hook-side seal** is a PostToolUse snapshot of the transcript, plus its sha256, at the first delivery. It is gated on call 6. Truthfully, it seals a partial first pass, not a complete report. F4's C is therefore measured only at arm level (A4 - A2), not by sealed-report judging.

Grafts:
- V1-R2 automatic harvest of seen-but-unopened paths;
- the same harvest applied to the sweeper's own Bash output, so the sweeper never has to post;
- V2-D1 disjoint ranked locators;
- V2-D5 witness as a sweep kind inside the 4-fact cap;
- V5-D3 command string plus the first-hand rule and the >10% mismatch stop.

##### 4. F3 grafts

- **Grain: concede to V2-D4 Task x move.** It uses about 25 regex-applicable cells per plan (V2:357). My region x move grid (V1:150) also counts cells where no move applies, and it was fed by model-posted cards. V2-D4's cells can be filled from V4-1's telemetry classifier (V4:190-195), so no model authors anything.
- **Keep V1-R1 per-receiver hash ordering.** It already does what V5-D4's rotating permutation does.
- **V5-D4 Stop block: adopt only its rule** "a covered cell is never a reason to skip" (V5:343). Reject the Stop block itself. A Stop-time move costs 3 turns (V5:339) against 2 for a checkpoint, so it adds 6.4 s: 116 + 12.8 + 19.2 + 2 = 150.0 s against V4-1's 143.6 s. It also depends on the unverified reissue.
- **V3 12-character leak check: adopt** as a hard audit for the content-free slots 3 and 4. It needs no ground truth, so it complements V4 R-07.

##### 5. F6 requests versus uncovered cells

Steelman of the opposing side (V2, V3, V4): a request ("apply M5 to Task 12") is more actionable for sonnet than a list.

My position merges the two. The harness renders requests in imperative form. The cells come only from V2-D4's uncovered matrix, ranked first by the cells luna's block declares not checked (V1:454). There are no covered counts, because they act as a clearance signal (V5 C-2; V2's concession 7). No SendMessage is used.

Keep the V1-R5 brief line "peer coverage is not clearance" and the V4 surface filter (V4:563). Arithmetic: 274 + 28 + 28 = **330 s (+20.4%)**; typical 302 s (+10.2%).

##### 6. Experiment section

| Arm (EL2, H = V1's H1-H4 in A1-A5) | Runs |
|---|---|
| A0 current harness, fresh (V2:509) | 4, plus 6 historical S07 as context |
| A1 isolated + H | 12 (V5:440) |
| A2 A1 + static catalogue | 12 |
| A3 slot 1 F1 | 6, extended to 12 at the interim look |
| A4 slot 2 F4 | 6 -> 12 |
| A5 slot 5 F7 (gated on spikes 1-2 and REQ-S3 act rate) | 6 -> 12 |

- **Primary endpoint:** target reach T. A run counts if it has at least 1 credit on B1, B2, B5, B6, B8, I1, I4, I5 or I6, or on I7 on control (V2:520).
- **Decision (V2:526):** X beats A1 under a one-sided Fisher test at p < 0.05, **and** X beats A2 by at least 2 runs per 6 (that is, +4 at n = 12). Reference p-values:
  - 4/6 vs 0/6: 15/495 = 0.030;
  - 4/12 vs 0/12: 495/10,626 = 0.047;
  - 3/12 vs 0/12: 220/2,024 = 0.109, which fails.
- **Interim look:** V5's (V5:454).
- **Guards:** V2's no-loss guards (V2:527); time per agenda 8.
- **Scoring:** sealed-report judging for A3 only (V2:517).
- **Size:** at most 4 + 12 + 12 + 3 x 12 = 64 panel runs. If every exchange arm stops at 6: 46.

##### 7. Harness share figure

Carry **0.03-0.34 /14 per run (central 0.14)**, V5's bottom-up sum (V5:147-151): low 0.02 + 0.01 + 0.00 = 0.03, high 0.16 + 0.08 + 0.10 = 0.34.

- **Control I7:** 0 for cheap panels. For sonnet panels the leak removal lowers measured I7 by up to about 2 of 9 credits. That is a measurement correction, not a gain.
- **H-4 is excluded** (X-008). V5's table never counted it, so the range does not change.
- **H-6** is a secondary score only.
- Spike 5 replaces the normalizer row with a measured value before any arm runs.
- Per A-004, C is reported conditional on H and is never added to H.

##### 8. Idle-time budgets and the baseline rule

The rule has five parts:

1. **The named baseline is B_A1**, the per-package median of A1 (harness-fixed and isolated), measured in spike 4 and in arm A1. The H fixes ship regardless, so A1 is the isolated panel that a collaboration design actually replaces. V1 (V1:592) and V2 (V2:528) already use this baseline. Historical S07 (116 s) appears only as the planning value in the spec's arithmetic, labelled as such, and every block is re-derived at the spike-4 value.
2. **In-run deadlines use B_A1:**
   - `PANEL_FINISH_AT = T0 + 1.20 B_A1`;
   - the phase-2 deadline is `T0 + 1.30 B_A1`.
3. **The catalogue's own time counts against a design.** If spike 4 shows A2 > 1.10 x A1, design arms do not carry the full kit. Their injected moves are their only catalogue content.
4. **The cap check:** median per package <= 1.35 x B_A1, and no package > 1.5 x (V2:528). V4's SLO budget (R-24) applies across packages.
5. **Mid-run designs (slots 2, 3, 5) cannot be killed** without losing the report. Their bound comes from the count caps plus the finish signal, and the SLO budget audits it.

#### Updated assessment of other variants

- **V2:**
  - Its absolute box is the right principle, but "- 4 s" costs luna B one of its two challenges (agenda 2).
  - Its natural seal gives the best independence for Stop-delivered designs. My slate has no Stop-delivered design, so its cost outweighs its benefit here.
  - Its experiment structure wins.
- **V3:** Its advocate's concessions are complete. Folding F5 into F4 is the better architecture, and I now adopt it. Its leak check enters slots 3-4.
- **V4:**
  - Its own fix for V4-2 (144 s, worst 150 s; round1-V4:65) matches my recomputation.
  - Its dispute of the diff analysis is correct: SEED:25 lists "ember + luna ~300 s", so S13 is a seed baseline. My C-012 vote does not depend on this.
  - F7 is a stronger slot 5 than my F5.
- **V5:**
  - The "never wait" rule and the 12-run controls enter the slate.
  - The Exit Ticket Stop block costs 6.4 s on the critical path and depends on an unverified reissue, so I graft only its skip rule.

#### Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 flip row and decoy ratio, the decoy slot filled by the V1-R3 gap card (p = 1/3, rendered identically); box min(35, T0 + 1.30 B_A1 - start) with n from the remaining time; V2 sealed-report judging; V5-D5 HL2 shadow variant with a haiku canary | Sealed by process exit, no hooks; 147.6 s (+27.2%), hard 150.8 s (+30.0%) for any T1 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V1-R2 automatic harvest, also applied to the sweeper's own output; V2-D1 disjoint locators; V2-D5 source-rule witness as a sweep kind; V5-D3 first-hand rule and 10% stop; 2 facts per luna, hook-side transcript seal, no Stop hold | Only cheap I7/T1 path, uses ember's idle time; 143.6 s (+23.8%), worst 150.0 s (+29.3%) |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move cell grain from telemetry; V1-R1 per-receiver hash order; V5-D4 "covered is never a reason to skip"; V3 12-character leak check; V4 surface filter | No model authors anything; 143.6 s (+23.8%), worst = expected |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 (274 s) | Harness-rendered move requests (V1-R5 semantics, no SendMessage) drawn from V2-D4 uncovered cells, ranked by luna's not-checked scope; no covered counts; V1-R5 brief line; V3 leak check | Harness author, Claude receiver; 330 s (+20.4%) worst |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, re-based to EL2, one way (ember flags, lunas adjudicate) | Hash-split cards, at most 2 per luna; hook-side seal; no luna posting and no Stop hold; V5 C-3 first-hand rule; `PANEL_FINISH_AT`; S13 kept as a variant | Distinct mechanism; answers SEED:47 against slot 2 on the same panel; 143.6 s (+23.8%), worst 150.0 s (+29.3%); C 0.13-0.77 |

Shared substrate: V4 board with the baked-in path, kill switch, `collab.json` and SLO; V1 `PANEL_FINISH_AT` on B_A1; V2's no-free-text rules (forbidden keys, located quote, existing paths) applied over V4's `panel-msg/1` size caps; V4's relative alarm (J + 0.15 or ledger rows -20%) plus a per-design echo threshold.

`Proposed base document: V4`

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Most complete scaffold: kill switch, baked path, timing and baseline tables |
| S-003 | V2 | The gate funnel names the blocked gate per issue and forces the H/C split |
| S-004 | V5 | Net collaboration, static-kit row, tokens per added issue |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Itemised unverified list tied to each number |
| C-001 | V1 | Switched: V5's argument holds. Searcher/reader complementarity is the only refinement predicting a gain a static kit cannot copy (V1:45); graft V2's 48/48 row as its evidence |
| C-002 | V5 | T2a/T2b predicts which designs reach B1/B2/I4 |
| C-003 | V1 | The four seed fixes; truncate + validate + re-ask; grading constant |
| C-004 | V4 | Best-style column needed by routing in slots 1, 3, 5 |
| C-005 | V4 | Switched: anchors of 12-200 characters match findings-v1 after H2, so F1 anchors pass whole; V2's rules graft on |
| C-006 | V4 | Process-exit seal for phases; seal artifact for mid-run (hook-side snapshot) |
| C-007 | V4 | Switched: ground-truth-free, so it can run in the product; V5's easy-issue share stays as an experiment metric |
| C-008 | V4 | Per-issue chains, arithmetically clean |
| C-009 | V5 | Three measured shares; add within-run sealed judging |
| C-010 | V2 | Fresh A0 plus catalogue arm; sizes from V5 |
| C-011 | V2 | Single reach endpoint, correct Fisher, margin over A2 |
| C-012 | V1 | Every design on a seed baseline (EL2, HL2, SL2) |
| C-013 | V1 | Panel-level finish signal, now on B_A1 |
| X-001 | V5 | Bottom-up 0.03-0.34, measurable by spike 5 |
| X-002 | V1 | 0 on /14; control may fall up to 0.33 in sonnet panels |
| X-003 | V1 | GT6 = I1 per SEED:71 |
| X-004 | V5 | HL2 legal against its own baseline; shadow schedule at +0% |
| X-005 | V1 | The slowest luna sets 116 s (SEED:98) |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text; forbidden keys enumerated |
| X-008 | V1 | Grading and judge held constant, sha256-pinned |
| X-009 | V1 | Truncate, validate, re-ask: no residual drop |
| X-010 | V5 | Quantifies that the kit may win; A2 is the comparator |
| X-011 | V5 | No AC-level anchors, so anchor routes need the gap card |
| X-012 | V1 | Tie with V2/V4/V5; V1:17 defines both scales and the label mapping most precisely |
| X-013 | V2 | 4/6 vs 0/6 = 0.030, verified |
| A-001 | V1 | REQ-S3 tests the act, not only delivery |
| A-002 | V5 | Only variant to price the kit's time and plan to re-measure turns |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | Flags /3 as unverified; per-run `wall_s` check |
| A-006 | V2 | Decoys, now carried by the gap card |
| A-007 | V4 | Spike, fallback, `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD`; clean `git status` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | c capped against SL2's measured reach |

### Variant 2 Rebuttal (opus:analyzer)

### Round 2 rebuttal: V2 (opus, analyzer lens)

Citations: `V<n>:<line>`, `R1-V<n>` = `round1-V<n>.md`, `R2-V1` = `round2-V1.md`, `SEED:<line>` = `../../../seed-brief.md`. I recomputed every number below this round.

#### Responses to criticisms of V2

| Criticism (raised by) | Response |
|---|---|
| D1 guard prose: `min(2, floor((150 - t - 12)/11))` is 0 from t = 128 s, not 135 s (V1, V3, V4, V5) | **Concede** (as in R1). (150 - 128 - 12)/11 = 0.91, so floor = 0. The formula also needs a clamp at 0. D1 is no longer a core (agenda 3). |
| D1 I7 high 0.60 exceeds the single-luna chain (all) | **Concede.** The lunas get disjoint locators (V2:159). Chain: 0.7 x 0.8 x 0.3 = 0.17 to 0.9 x 0.8 x 0.6 = 0.43. |
| D1 assumes a Stop block yields a reissued full report, which is unverified (R1-V4) | **Concede.** My own spike list puts this behaviour in doubt (V2:502). It is one reason I move the F4 core to V4-2. |
| D2's `- 4 s` costs luna B one of its two challenges (R2-V1) | **Concede.** V2:255 reserves 4 s for resume start. A wall-clock `timeout` around the resumed process already includes the 6 s start that V4 costs per phase 2 (V4:392). Box = min(35, 150 - 116 - 4) = 30 s, which leaves 24 s of work and floor(24/12.8) = 1 complete challenge. V1's re-based box keeps my principle (an absolute deadline tied to the named baseline) without the double count (agenda 2). |
| D2 routes on the peer's category; V4-3 routes on anchor text (R1-V4) | **Concede, with one row kept.** Anchor-text routing sends grep sentences to M4/M7, the moves the 16 I5 near-misses lacked (V4:349-354). I keep one category override: `contradiction` -> M7 on all tasks (V2:226). It is the only I6 propagation trigger left in the slate. |
| D2 leaves ember idle until about 102 s (R1-V5) | **Counter.** Idle time is not elapsed time. V4-3 has ember wait for both lunas too (V4:370), and ember still ends at 141.2 s, below luna B's 147.6 s. V5 is right that the window has value, and F4 uses it. |
| D3 has no time box, no send validation and no durable log (all) | **Concede.** It is out of every slate. |
| D4 needs luna to log cells; luna makes about 1 Bash call per run (V1, V4) | **Concede.** Only D4's Task x move grain survives, filled from V4-1 telemetry (agenda 4). |
| D5 is budgeted on S14, which is not a seed baseline (V1, V3, V5) | **Concede.** SEED:25 lists ember + 2x luna, ember + luna, haiku + 2x luna and sonnet + 2x luna. It does not list ember + luna + sonnet. |
| `target.quote` at most 120 characters is too short for real anchors (R1-V3) | **Concede.** After H2, anchors run up to 200 characters, and F1 sends them verbatim. Use V4's 12-200 bound and keep my located-verbatim, existing-path and forbidden-key rules. |
| The natural seal's cost outweighs its benefit in this slate (R2-V1) | **Concede.** No slate design delivers at Stop. F1 is sealed by process exit; F3, F4 and F7 use the hook-side snapshot (agenda 3). |

#### Agenda items

##### 1. Slot 5: F5 versus F7

**I switch to F7 (V4-4), re-based to EL2 and run one way as in R2-V1.**

Steelman of F5, my R1 choice: V2-D5 is the only design aimed at the source-only rules B5, I1 and B2 (V2:424). Those rules are masked by the post-implementation checkout.

Its mechanism is still F4's. ember runs a batched sweep and posts locators, and a reader acts on them (V2:424-431). Only the fact kind differs. A five-slot slate with two "searcher posts facts" slots fails the distinctness test. The B5/I1/B2 target survives as a sweep kind inside slot 2 (V1, V3 and V5 graft it there too).

F7 adds what nothing else in the slate tests:
- In F1, the harness picks peers' anchors from finished reports.
- In F7, a model marks sentences mid-run without judging them, and a different model must answer each with a finite check (V4:463-468).
- F7 is the only slot that answers SEED:47 ("challenge versus shared findings") on the same panel as F4.

**V4's witness-card graft, rejected.** V4 proposes turning V2-D5 witness lines into harness-generated F7 cards. V4's own note says a deterministic extractor is "a prompt and harness change, not collaboration" (V4:523), and its share would belong to A2.

**Analyzer addition: the flag signal.** A flag is not a finding, so F7 carries a weaker location signal than F1. But ember picks what it flags, so its flags may track its own findings. Log `flag_finding_overlap`: the share of ember's cards whose anchor equals an anchor in ember's own final findings. If it exceeds 50% in an arm, flags behave like findings and A-006 applies: add a 1-in-3 gap-card decoy.

| F7 check | Recomputed |
|---|---|
| V4-4 rows | low 0.03+0.01+0.03+0.03+0.02+0.02+0.01+0.01+0 = 0.16; high 0.16+0.08+0.15+0.15+0.10+0.10+0.06+0.08+0.05 = 0.93 (V4:508-518) |
| Drop luna search cards B8/B6 | 0.16 - 0.03 = **0.13**; 0.93 - 0.16 = **0.77** /14 |
| EL2 luna B | 116 + 2 x 2 x 6.4 + 2 = 143.6 s (+23.8%); worst +6.4 = 150.0 s (+29.3%) |

**Residual risk.** F7 still needs ember to post cards. Gate A5 on V1's REQ-S3 act rate and on `cards_sent > 0` in the spike. V4's runbook stops the arm if `cards_sent = 0` in more than 50% of runs (V4:531).

##### 2. F1 core, time box and gap card

**Core: V4-3**, as in R1. Its combiner keeps phase-1 lines verbatim by construction (V4:356), which is safer than my R-16.

**Time box: adopt V1's rule.**
- box = min(35, T0 + 1.30 x B_A1 - start)
- n = min(cap, floor((box - 6) / (2 x turn)))

| Reviewer (B_A1 = 116 planning value; deadline 150.8 s) | Start | Box | n | End |
|---|---|---|---|---|
| luna A | 95 | min(35, 55.8) = 35 | floor(29/12.8) = 2 | 95 + 6 + 25.6 = 126.6 |
| luna B | 116 | 34.8 | floor(28.8/12.8) = 2 | 116 + 6 + 25.6 = **147.6 (+27.2%)** |
| ember | 116 | 34.8 | min(3, floor(28.8/6.4)) = 3 | 116 + 6 + 19.2 = 141.2 |
| any T1 | - | - | 0 if start > 150.8 - 18.8 = 132.0 | hard bound **150.8 (+30.0%)** |

The rule also settles V4's 45 s vs 35 s inconsistency (V4:375 vs :396).

**HL2 shadow variant (V5-D5):** 238 + 6 + 2 x 23 = 290 s (+21.8%), against a deadline of 1.30 x 238 = 309.4 s.

**Gap card fills the decoy slot (concede to V4 and V1).** My decoy was already built as a gap card: a trigger-regex location that no peer flagged (V2:240). Merging the two costs nothing, provided three conditions hold:
1. It is rendered identically to a peer-anchor challenge.
2. The digest never says which kind a slot is (V2's withheld table).
3. It fills each slot with probability 1/3, seeded per receiver. With luna's cap of 2, P(no decoy) = (2/3)^2 = 4/9 and P(both slots decoys) = 1/9.

**Measurable alarm for this slot.** Log each X-finding's slot type. Report `echo` (V4: claim-token Jaccard above 0.6 with the peer's claim, alarm above 30%) on real-anchor slots only, since decoys have no peer claim.

##### 3. F4 core and its worst case

**Concede the core to V4-2.** My D1 has two problems:
- Delivery at the first Stop costs a full report reissue on the critical path: 116 + 12 + 25.6 = 153.6 s (+32.4%). That leaves 2.6 points of headroom.
- It depends on the unverified Stop reissue.

One arithmetic block (matches R2-V1 and R1-V4's fix):

| Item | Value |
|---|---|
| ember sweeper (fresh session, never sees ember's report) | 41 + 6 + 10 x 3.2 = 79 s, inside ember's idle window |
| luna B, 2 facts, hook seal, no hold | 116 + 2 x 2 x 6.4 + 2 = **143.6 s (+23.8%)** |
| Worst, one turn of slip at `PANEL_FINISH_AT` = 1.20 x 116 = 139.2 s | 143.6 + 6.4 = **150.0 s (+29.3%)** |

**The seal is the one thing I insist on.** A call-6 count leaves no artifact (my C-006 criticism of V1 and V5). The hook-side seal must therefore be:
- a PostToolUse transcript snapshot plus its sha256, taken at the first delivery;
- checked by V3's acceptance test: the snapshot's timestamp precedes the first peer line received (V3:56, req 10).

It seals a partial first pass, as V1 says. F4's C is therefore measured only at arm level (A4 - A2), never by sealed-report judging.

Grafts: V2-D1 disjoint ranked locators (unnamed tests first); V1-R2 harvest, also run on the sweeper's own output; V2-D5 witness as a sweep kind inside the cap; V5-D3 first-hand rule with the >10% mismatch stop.

##### 4. F3 grafts

| Graft | Position | Reason |
|---|---|---|
| V2-D4 Task x move grain | Adopt (V1 now concedes) | About 25 regex-applicable cells per plan (V2:357). Fill them from V4-1 telemetry (V4:190-195), so no model logs anything (my D4 concession). |
| V1-R1 per-receiver hash order | Adopt | Already gives the two lunas different gaps, which is what V5-D4's rotation was for. |
| V5-D4 Stop block | Reject the block, keep its rule | A Stop move costs 3 turns against 2: 116 + 12.8 + 19.2 + 2 = 150.0 s vs 143.6 s, and it rests on the unverified reissue. Keep "a covered region is never a reason to skip" (V5:343). |
| V3 12-character leak check | Adopt for F3 and F6 | Ground-truth-free, so it complements V4 R-07. It does not apply to F1, which sends anchors on purpose. |
| V4-1 deadline | Keep 110 s | V4's own correction gives 112 s; 110 s is more conservative (R1-V4 concession 9). |

##### 5. F6 requests versus uncovered cells

**Adopt V1's merge.** The harness renders imperative requests ("apply M5 to Task 12"), drawn only from V2-D4's uncovered cells and ranked first by luna's declared not-checked scope. There are no covered counts and no SendMessage.

My D4 concession is why covered counts must go: they are a clearance signal (V5 C-2). The V1-R5 brief line and the V4 surface filter stay.

Arithmetic on SL2 (seed sonnet + 2x luna, 821/3 = 273.7 s; cap 369.5 s):
- worst 274 + 28 + 28 = 330 s (+20.4%);
- typical 302 s (+10.2%).

##### 6. Experiment section

| Arm (EL2; A1-A6 all carry H) | Runs | Measures |
|---|---|---|
| A0 current harness, fresh (V2:509) | 4, plus 6 historical S07 as context | H = A1 - A0 at the same time; gateway drift |
| A1 isolated + H | 12 (V5) | named baseline B_A1; comparator |
| A2 A1 + static catalogue | 12 | prompting share |
| A3 F1 | 6 -> 12 | C, plus sealed-report judging (V2:517) |
| A4 F4 | 6 -> 12 | C at arm level |
| A5 F7 (gated: REQ-S3 act rate, `cards_sent > 0`) | 6 -> 12 | C; A5 vs A4 answers SEED:47 |
| A6 F3 | 6 -> 12 | C; the cleanest test of exchange vs kit, since no model authors anything |
| Stage 2 on SL2: A1-SL2, A2-SL2, F6 | 12, 6, 6 -> 12 | F6 against its own panel |

I add A6 to V1's plan. F3 runs on EL2, shares A1 and A2, needs no compliance gate, and directly tests V5's claim that the kit may beat exchange (V5:418).

Size:
- Stage 1: at most 4 + 12 + 12 + 4 x 12 = 76 panel runs; 52 if every exchange arm stops at 6.
- Stage 2: at most 30.

**Endpoint:** reach T, a run with at least 1 credit on B1, B2, B5, B6, B8, I1, I4, I5 or I6, or on I7 on control (V2:520).

**Decision, at the final look only:** X beats A1 under a one-sided Fisher exact test at p < 0.05, **and** X beats A2 by at least 4 reach runs at n = 12.

| Comparison | Fisher one-sided |
|---|---|
| 4/12 vs 0/12 | C(12,4)/C(24,4) = 495/10,626 = 0.047, passes |
| 3/12 vs 0/12 | 220/2,024 = 0.109, fails |

**Analyzer correction to R2-V1.** V1 cites 4/6 vs 0/6 (0.030) alongside an interim look, which would allow a pass at 6 runs as well as at 12. Two efficacy looks at 0.05 inflate the false-pass rate. The interim look at 6 must be **futility only**, using V5's three stop conditions (V5:454). An arm stopped there is reported as not adopted.

**Multiplicity.** Four arms each tested at 0.05 give a familywise false-pass rate of at most 4 x 0.05 = 0.20 (Bonferroni bound). That is acceptable only because adoption also requires the 12-run confirmation on two new packages (V2:531). The spec must say so.

Guards: V2's no-loss rules (V2:527), independence (alarm in at most 2 of 12 runs, zero audit violations) and time (agenda 8).

##### 7. Harness share figure

Carry **H = 0.03-0.34 /14 per run, central 0.14**, from V5's bottom-up table (V5:147-151):
- low: 0.02 + 0.01 + 0.00 + 0 = 0.03;
- high: 0.16 + 0.08 + 0.10 + 0 = 0.34;
- central: 0.08 + 0.03 + 0.03 = 0.14.

My own figure is superseded. V2:147 states +0.1 to +0.5, but its rows sum to 0.05 + 0 + 0.05 = 0.10 low and 0.15 + 0.1 + 0.3 = 0.55 high, so "rounded" understated the high end.

Further rules:
- **H-4 is excluded** (X-008). V5's table never counted it, so the range is unchanged.
- **H-6** is a secondary score only.
- **Leak removal** is 0 on /14 for cheap panels. For sonnet panels it removes up to 2 of 9 I7 credits; that is a measurement correction, reported on control /2.
- Spike 5 replaces the normalizer row with a measured value.
- Every gain block shows C low-high and H 0.03-0.34 in separate columns, with C conditional on H and never summed with it (A-004).

##### 8. Idle-time budgets and the baseline rule

I adopt V1's five-part rule:
- B_A1 = the per-package A1 median;
- in-run deadlines at 1.20 and 1.30 x B_A1;
- cap: median per package at most 1.35 x B_A1, and no package above 1.5x (V2:528);
- per-package medians, not /3 (A-005).

Two analyzer corrections follow.

**(a) The danger is not a slower A1.** For an additive worst case W, the cap holds when W <= 0.35 x B. A larger B_A1 makes this easier: the F4/F7 worst case of B + 34 fits for any B >= 34/0.35 = 97.1 s. The real danger is a design arm whose phase 1 runs slower than A1's because its brief carries catalogue content (V5 estimates +29% for the full kit, V5:411).

V1's threshold "drop the kit if A2 > 1.10 x A1" is too loose. The allowed brief slowdown s depends on each slot's additive worst case: s <= (0.35 x B - W) / B.

| Slot | W (planning B) | Max s |
|---|---|---|
| F4, F7 (B = 116) | 34 s | 6.6/116 = **5.7%** |
| F3 (B = 116) | 27.6 s | 13.0/116 = **11.2%** |
| F6 (B = 274) | 56 s | 39.9/274 = **14.6%** |
| F1 | absolute deadline | always within the cap. At s >= 13.8% (luna B starts at or after 132.0 s), luna B gets n = 0 and the gain disappears |

Rule: each design's ex-ante budget is B_A1 x (1 + s) + W, where s is the spike-4 slowdown of that design's brief over A1. If the budget exceeds 1.35 x B_A1, the design drops brief content until it fits.

**(b) Two measurements, labelled.**
- The in-run deadlines use the spike-4 B_A1, frozen and pre-registered.
- The ex-post cap test uses the concurrent A1 median.
- Report B_A1 / 116. If it exceeds 1.15 (133.4 s), report it as the harness fixes' own time cost, part of H, not of any design.
- The spec's 116 s blocks stay as labelled planning values, written as formulas in B so they rescale.

#### Updated assessment of other variants

- **V1:** Its Round 2 fixes are the best repairs in the debate:
  - the B_A1 phase-2 box removes both its own floating kill and my double count;
  - the one-way F7 removes V4-4's luna card and its Stop hold;
  - it withdraws "delivery at first Stop", my own D1 idea, for the right reason.

  It still needs the futility-only interim look and the per-slot slowdown limit (agenda 6 and 8).
- **V3:** Its integrity controls belong in the spec as acceptance tests:
  - the seal-timestamp test (now on F4/F7);
  - the 12-character leak check (F3/F6);
  - the hashed enum;
  - the settings sha256.

  Its gain arithmetic is not used.
- **V4:** Its own fixes for V4-2 (144 s, worst 150 s) match my recomputation, and it was right that S13 is a seed baseline (SEED:25). Its witness-card graft fails its own V4:523 test.
- **V5:**
  - The H table, the 12-run controls and the futility look all enter the slate.
  - Its "never wait" rule removed the 15 s hold from F4.
  - Its +29% kit estimate is what makes agenda 8(a) binding.
  - It conceded its Fisher clause (96/792 = 0.121).

#### Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Anchor-text routing plus V2-D2 `contradiction` -> M7 override; decoy slot filled by the V1-R3 gap card (p = 1/3 per slot, rendered identically, kind withheld); box min(35, T0 + 1.30 B_A1 - start), n from remaining time; V4 combiner; V2 sealed-report judging; V5-D5 HL2 shadow variant with haiku canary | Sealed by process exit, no hooks; 147.6 s (+27.2%), hard 150.8 s (+30.0%) for any T1; C 0.23-0.94 before the act-rate spike |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint ranked locators; V1-R2 harvest, also on the sweeper's output; V2-D5 witness as a sweep kind; V5-D3 first-hand rule and 10% stop; 2 facts per luna; hook snapshot seal plus sha256 and V3 timestamp test; no hold | Only cheap I7/T1 path; keeps the B5/I1/B2 target; 143.6 s (+23.8%), worst 150.0 s (+29.3%) |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move grain from telemetry; V1-R1 hash order; V5-D4 skip rule only; V3 leak check; V4 surface filter | No model authors anything; 143.6 s (+23.8%), worst = expected; arm A6 tests exchange vs kit directly |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Harness-rendered requests from uncovered cells only, ranked by luna's not-checked scope; V1-R5 brief line; V3 leak check; no SendMessage | Harness author, Claude receiver; 330 s (+20.4%) worst |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Hash-split cards, at most 2 per luna; hook seal; no luna card, no hold; V5 C-3; `PANEL_FINISH_AT`; `flag_finding_overlap` alarm (> 50% adds a gap-card decoy); S13 variant | Distinct mechanism, answers SEED:47 against slot 2; 143.6 s (+23.8%), worst 150.0 s (+29.3%); C 0.13-0.77 |

Proposed base document: V4

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Kill switch, baked path, timing and baseline tables |
| S-003 | V2 | The gate funnel subsumes V5's T2a (gate B) and T2b (gate A) and names the blocked gate per issue |
| S-004 | V5 | Net collaboration, static-kit row, tokens per added issue |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Switched: itemised unverified list tied to each number |
| C-001 | V1 | Switched: the slate's F4 is searcher/reader complementarity; V2's 48/48 is its evidence, not a rival theory |
| C-002 | V5 | T2a/T2b predicts which designs reach B1/B2/I4 |
| C-003 | V1 | Truncate, validate, re-ask; grading constant |
| C-004 | V4 | Best-style column used by routing in slots 1, 3, 5 |
| C-005 | V4 | 12-200-character anchors fit F1; my 120-character quote was too short; V2 rules graft on |
| C-006 | V4 | Switched: process exit for phases, hook snapshot for mid-run; no slate design is Stop-delivered |
| C-007 | V4 | Relative and ground-truth-free; per-design echo |
| C-008 | V4 | Same per-issue chain method as V2, executed without errors |
| C-009 | V5 | Switched: three measured shares; A0 must be fresh (C-010) |
| C-010 | V2 | Fresh A0 plus catalogue arm; V5's sizes |
| C-011 | V2 | Single reach endpoint, correct Fisher, margin over A2; futility-only interim |
| C-012 | V1 | Every design on a seed baseline |
| C-013 | V1 | Panel-level finish signal, now on B_A1 |
| X-001 | V5 | Bottom-up 0.03-0.34; V2's 0.1-0.5 rounded its own high end down |
| X-002 | V1 | 0 on /14; control falls up to 0.33 for sonnet panels |
| X-003 | V1 | GT6 = I1 per SEED:71 |
| X-004 | V5 | HL2 legal; shadow schedule |
| X-005 | V1 | The slowest luna sets 116 s |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text; forbidden keys enumerated |
| X-008 | V1 | Grading and judge held constant, sha256-pinned |
| X-009 | V1 | Truncate, validate, re-ask: no residual drop |
| X-010 | V5 | Quantifies that the kit may win; A2 is the comparator |
| X-011 | V5 | No AC-level anchors, so anchor routes need the gap card |
| X-012 | V1 | Switched: V1, V2, V4 and V5 are equivalent; V1:17 states both scales and the label mapping |
| X-013 | V2 | 4/6 vs 0/6 = 15/495 = 0.030, verified |
| A-001 | V1 | REQ-S3 tests the act, not only delivery |
| A-002 | V5 | Prices the kit's time; that drives the per-slot slowdown limit |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | /3 flagged; per-run `wall_s` check |
| A-006 | V2 | Decoys, now carried by the gap card |
| A-007 | V4 | Spike, fallback, `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD`; clean `git status` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | c capped against SL2's measured reach |

### Variant 3 Rebuttal (haiku:backend)

### Round 2 rebuttal: V3 (haiku, backend lens)

Citations: `V<n>:<line>` = variant files; `R1-V<n>` / `R2-V<n>` = debate statements (line numbers after the colon). I recomputed every number below this round.

#### Responses to criticisms of V3

V3's design content is not a contender. Every criticism below except the last two was conceded in Round 1 (R1-V3:80-98), and I hold those concessions. What remains in dispute is which V3 integrity controls survive, and in what form.

| Criticism (raised by) | Response |
|---|---|
| Req 6 puts collaboration output outside the findings block, so every gain scores 0 (all) | **Concede.** V3:176 contradicts V3:73. Use V4's combiner: one block, phase-1 lines verbatim (V4:356, :453). |
| Harness share 0.8-2.1 (all) | **Concede.** Withdrawn. See agenda 7. |
| I7 counted on /14 (all) | **Concede.** |
| 14 s "harness overhead" (all) | **Concede** on attribution. The totals still hold, because 102 + 14 = 116. |
| Gains do not follow from their inputs; no per-issue rows (all) | **Concede.** V3's gain arithmetic is not used anywhere in my slate. |
| No static-catalogue arm (all) | **Concede.** |
| Absolute Jaccard 0.5 (all) | **Concede.** Use the relative alarm (V4 R-25). |
| `merge_guard.py:256` credited to B5 (all) | **Concede.** It repairs I1 (GT6). |
| R4 has no measurable alarm (V2) | **Concede.** R4 is out. |
| `pass1.md` must be written through Bash, which the read-only rule does not restrict, and luna makes about 1 Bash call per run (R1-V4:27) | **Concede the artifact, keep the test.** A seal that depends on luna running a command is compliance-dependent. The hook-side PostToolUse snapshot (R2-V1:82) needs no model action. My timestamp check (V3:180, req 10) becomes its acceptance test, as R2-V2:90 already proposes. |
| The 10-to-20 extension rule (praised by V1, V2, V5) | **Self-correction.** R2-V2:144's multiplicity point applies to my rule too. V3:159-160 can adopt at 10 runs **or** at 20, which is two efficacy looks. The interim look must be futility-only. |
| SendMessage fallback for F7 (my own R1 graft) | **Withdraw.** A one-way F7 needs no reply address, and SendMessage leaves no audit file (V4:485). |

#### Agenda items

##### 1. Slot 5: F5 versus F7

**F7, re-based to EL2 and run one way.** This was my Round 1 position, and V1 and V2 now share it.

Steelman of F5: V2-D5 is the only design aimed at the rules hidden by the post-implementation checkout (B5, I1, B2). Its mechanism, however, is F4's: a searcher posts facts and a reader acts on them (V2:424-431). In a slate of five distinct designs, that target belongs as a sweep kind inside slot 2.

Two changes from my Round 1 position:
- I drop V3-R4's SendMessage fallback.
- The one-way EL2 form also removes V4-4's untested Stop-hold dependency (V4:532), which my lens weights most.

V4's witness-card graft fails V4's own test, "a prompt and harness change, not collaboration" (V4:523).

**Gain correction.** No other advocate applied A-011 to F7. B1, B2 and I5 were never found by any cheap model, so their low ends go to 0:

| F7 block | Low | High |
|---|---|---|
| V4-4 rows (V4:508-518) | 0.16 | 0.93 |
| Drop the luna search-card rows B8/B6 (one way) | 0.13 | 0.77 |
| B1 0.03, B2 0.01 and I5 0.01 low ends set to 0 | **0.08** | **0.77** |

**Time on EL2:** 116 + 2 x 2 x 6.4 + 2 = 143.6 s (+23.8%); worst 150.0 s (+29.3%).

**S13 variant.** I would not keep the S13 variant as written. At 2 adjudications its worst case is 134.0 s (+34.0%), only 1 point under the cap. With 1 adjudication: 100 + 12.8 + 2 = 114.8 s (+14.8%); worst 121.2 s (+21.2%).

**Alarm.** Adopt V2's `flag_finding_overlap` alarm: if more than 50% of flags match ember's own final anchors, add a gap-card decoy (R2-V2:38).

##### 2. F1 core, time box and gap card

**Core V4-3.** Adopt V1's box rule: `box = min(35, T0 + 1.30 x B_A1 - start)` and `n = min(cap, floor((box - 6) / (2 x turn)))`.

| Check (planning B = 116 s) | Value |
|---|---|
| Deadline | 1.30 x 116 = 150.8 s |
| luna B | box 34.8 s; n = floor(28.8 / 12.8) = 2; end 116 + 6 + 25.6 = **147.6 s (+27.2%)** |
| Last start that still gets n >= 1 | 150.8 - 6 - 12.8 = 132.0 s |
| Hard bound for any T1 | **150.8 s (+30.0%)** |

**Gap card fills the decoy slot: concede.** I argued in Round 1 that the gap card should be an extra slot. That is unaffordable. A third luna slot ends at 116 + 6 + 3 x 12.8 = 160.4 s, which is past the 150.8 s deadline. Adopt R2-V2:67-70: p = 1/3 per slot, rendered identically, kind withheld.

**Correction to R2-V1 and R2-V2: the HL2 variant is mislabelled.** Both cite "V5-D5 HL2 shadow variant: 238 + 6 + 2 x 23 = 290 s (+21.8%)" (R2-V1:61, R2-V2:65). That figure is V4's haiku variant, in which haiku runs a challenge at 238 s (V4:403). V5-D5 keeps haiku as an isolated canary that receives nothing (V5:357). Under V5-D5 the lunas exchange anchors with each other inside haiku's window, so:
- the panel ends at 238 s (**+0%**);
- the worst case is the 15 s kill, 253 s (**+6.3%**, V5:385).

V4's haiku-variant gain of 0.40-1.60 (V4:430) is unreachable under either schedule. It rests on haiku's high anchor rate, but haiku's anchors exist only at 238 s, after the lunas' phase 2 has ended at about 148 s (V4:402). The merged spec takes V5-D5 as written, with its gain re-derived from luna-to-luna anchors.

**F1 gain, with the corrections everyone conceded:**

| Step | Low | High |
|---|---|---|
| V4-3 rows (V4:421-429) | 0.23 | 0.94 |
| Anchor-route B1 and B2 set to 0, since no AC-level anchors exist (X-011) | 0.18 | 0.71 |
| I5 and I6 low ends set to 0 (A-011) | 0.11 | 0.71 |
| Decoy displacement: real slots fall to x2/3 at worst (low end), and cost nothing when few anchors qualify (high end) | 0.07 | 0.71 |
| Gap-card route to B1/B2, 0-0.10 (V1's range; X-011) | **0.07** | **0.81** |

**Fault-tolerance rule.** On a phase-2 timeout, the combiner emits the phase-1 block unchanged and logs `phase2_timeout` (V4:375, :453).

##### 3. F4 core and its worst case

**Concede to the converged block.** My Round 1 figure of 148 s kept luna's 6 s `panel-seal` turn. The hook-side seal replaces that turn with about 2 s of hook time, which gives 116 + 25.6 + 2 = **143.6 s (+23.8%)**, worst **150.0 s (+29.3%)**.

**Gain correction nobody applied.** Every slate grafts V2-D1's disjoint locators onto V4-2, so the test file goes to one luna only. V4-2's I7 row, however, still counts "two lunas" (V4:319). The single-luna chain is:
- low: 0.7 x 0.6 x 0.4 = 0.168;
- high: 0.9 x 0.8 x 0.7 = 0.504.

So merged F4 I7 is **0.17-0.50 (control /2)**, not 0.25-0.60.

The cap of 2 acted facts per luna costs no gain. The sweeper sends at most 4 facts (V4:288), and the disjoint split gives each luna 2 different ones. The witness kind takes one of those four places.

**Backend additions:**

| Addition | Why |
|---|---|
| Write the seal snapshot under `$BOARD`, outside the sandbox (V4 R-09). The harness records its sha256 in `collab.json` at write time. The timestamp test (V3 req 10) checks it. | Bash is unrestricted (A-008), so the hash must be recorded by the harness, not stored next to the file. |
| Hard `timeout` on the sweeper at T0 + 85 s | `--max-turns` does not exist (V5:106). V4:285 sets the last fact at 85 s, so later work is waste. |
| Write facts and digests atomically (temp file, then `mv`) | A torn line must never reach a hook. V4 does this already for F1's digest (V4:377). |

##### 4. F3 grafts

| Graft | Position |
|---|---|
| V2-D4 Task x move grain, filled from V4-1 telemetry | **Concede**, moving from V1-R1's region grain. Telemetry fills the cells with no model authoring. |
| V1-R1 per-receiver hash order | Adopt. It does the job of V5-D4's rotation. |
| V5-D4 Stop block | **Concede: reject the block, keep its skip rule.** 116 + 12.8 + 19.2 + 2 = 150.0 s against 143.6 s, and it depends on the unverified Stop reissue. |
| V3 12-character leak check | Keep, on F3 and F6 only. Refinement: compare only the variable fields, never the fixed template text, so that shared template wording cannot produce false positives. It does not apply to F4, where real paths may appear in anchors, or to F1/F7, which carry anchors on purpose. |
| V3-R1 resume digest as a fallback | Keep, used only if spike S0 shows that hooks fail. The same telemetry gaps are delivered at phase-1 exit through `--resume`: 116 + 6 + 25.6 = 147.6 s (+27.2%), inside F1's box rule. |

##### 5. F6 requests versus uncovered cells

**Agree with the V1/V2 merge.** The harness renders imperative requests drawn only from uncovered cells, ranked by luna's declared not-checked scope. There are no covered counts and no SendMessage.

The SL2 baseline is 821/3 = 273.7 s, so the cap is 369.5 s. Worst case 274 + 28 + 28 = **330 s (+20.4%)**; typical 302 s (+10.2%).

##### 6. Experiment section

Adopt R2-V2's plan (R2-V2:118-148):
- arms A0-A6, with F3 as arm A6;
- 12-run controls;
- one reach endpoint;
- a Fisher test at the final look only, plus +4 over A2;
- a futility-only interim look.

Fisher checks:
- 4/12 vs 0/12: C(12,4)/C(24,4) = 495/10,626 = 0.047, which passes;
- 3/12 vs 0/12: 220/2,024 = 0.109, which fails.

Size: at most 4 + 12 + 12 + 48 = 76 runs; 52 if every exchange arm stops at 6.

Integrity tests to add (backend):

| Test | Source |
|---|---|
| Catalogue and enum sha256 recorded before A2; a mismatch invalidates the arm | V3 req 18 with V4 R-07 |
| User `~/.claude/settings.json` sha256 identical before and after the experiment | V3 req 17 |
| Second-judge double scoring of a random 12-row sample | V3:167 |
| Block-randomised run order | V5:437-454; needed for the drift rule in agenda 8 |

##### 7. Harness share figure

Carry **H = 0.03-0.34 /14, central 0.14**:
- low: 0.02 + 0.01 + 0.00 = 0.03;
- high: 0.16 + 0.08 + 0.10 = 0.34;
- central: 0.08 + 0.03 + 0.03 = 0.14 (V5:147-151).

H-4 is excluded (X-008). Leak removal counts 0 on /14. Spike 5 replaces the normalizer row with a measured value. My 0.8-2.1 is withdrawn.

##### 8. Idle-time budgets and the baseline rule

**Adopt V1's five-part rule with V2's per-slot slowdown limits.** I checked V2's limits:

| Slot | W (planning) | Slowdown limit s |
|---|---|---|
| F4 / F7 | 34 s | (40.6 - 34) / 116 = 5.7% |
| F3 | 27.6 s | (40.6 - 27.6) / 116 = 11.2% |
| F6 | 56 s | (95.9 - 56) / 274 = 14.6% |

**One consistency gap remains.** R2-V2:190-191 uses two baselines:
- in-run deadlines run on the frozen spike-4 value, B_f;
- the cap test runs on the concurrent A1 median, B_c.

F1's "hard bound" 1.30 x B_f stays under 1.35 x B_c only while B_c >= (1.30 / 1.35) x B_f = 0.963 x B_f. A gateway that is 3.7% faster on the test day turns a guaranteed design into a cap failure.

Rule: log `baseline_drift = B_c / B_f` per randomised block. Outside [0.963, 1.10], re-freeze B_f from that block's A1 runs before the next block. Package results under drift are reported but not used for the time verdict.

#### Updated assessment of other variants

- **V1.** It gave the best repairs: the B_A1 box, one-way F7, and withdrawing its own first-Stop delivery. It mislabels the HL2 variant (agenda 2).
- **V2.** Its analyzer corrections (futility-only interim, slowdown limits) are right, and the futility point also corrects my own extension rule. Its gate table marks B1 and I4 exposure as passed because the Task is anchored (V2:85, :92). T2b shows that is wrong at the acceptance-criterion level. It shares the HL2 mislabel.
- **V4.** Its Round 1 fix of V4-2 (144 s, worst 150 s) is the converged block. Its F7 is the right core, but in the one-way EL2 form, without its witness cards. Its I7 row (V4:319) double-counts once the disjoint split is grafted.
- **V5.** "Never wait" and the 12-run controls entered every slate. Its D5 shadow schedule is better than the other advocates credit: +0%, not +21.8%.

#### Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Anchor-text routing plus V2-D2 `contradiction` -> M7; decoy slot filled by the V1-R3 gap card (p = 1/3 per slot, kind withheld); box min(35, T0 + 1.30 B_A1 - start); V4 combiner with `phase2_timeout` fallback; V2 sealed-report judging; V5-D5 shadow variant as written (haiku canary) | Sealed by process exit, no hooks. EL2 147.6 s (+27.2%), hard 150.8 s (+30.0%); HL2 238 s (+0%), worst 253 s (+6.3%); C 0.07-0.81 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint ranked locators; V1-R2 harvest including the sweeper's output; V2-D5 witness as a sweep kind; V5-D3 first-hand rule and 10% stop; 2 facts per luna, no hold; hook snapshot seal under `$BOARD` with harness-recorded sha256 and the V3 timestamp test; sweeper `timeout` at T0 + 85 s; atomic writes | Only cheap I7/T1 path. 143.6 s (+23.8%), worst 150.0 s (+29.3%); I7 0.17-0.50 control |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move grain from telemetry; V1-R1 hash order; V5-D4 skip rule only; V3 leak check on variable fields; V4 surface filter; V3-R1 resume digest as the fallback if S0 fails (147.6 s) | No model authors anything. 143.6 s (+23.8%), worst = expected |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Harness-rendered requests from uncovered cells only, ranked by luna's not-checked scope; V1-R5 brief line; V3 leak check; no SendMessage; V4 surface filter | Harness author, Claude receiver. 330 s worst (+20.4%), typical 302 s (+10.2%) |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Hash-split cards, at most 2 per luna; hook seal plus V3 timestamp test; no luna card, no Stop hold; V5 C-3; `PANEL_FINISH_AT`; `flag_finding_overlap` alarm; S13 variant limited to 1 adjudication | Distinct mechanism; answers SEED:47 against slot 2 on the same panel. 143.6 s (+23.8%), worst 150.0 s (+29.3%); C 0.08-0.77 |

Proposed base document: V4

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Kill switch, baked board path, timing and baseline tables |
| S-003 | V2 | Switched: the gate funnel's survival gate makes the H/C split structural. Its B1/I4 exposure cells must take V5's T2b correction |
| S-004 | V5 | Net collaboration, static-kit row, tokens per added issue |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Itemised unverified list tied to each number |
| C-001 | V1 | Searcher/reader complementarity predicts a gain a static kit cannot copy; V2's 48/48 is its evidence |
| C-002 | V5 | T2a/T2b predicts which designs reach B1, B2 and I4 |
| C-003 | V1 | Truncate, validate, re-ask; grading constant |
| C-004 | V4 | Best-style column used by routing in slots 1, 3 and 5 |
| C-005 | V4 | 12-200-character anchors fit F1 (V2 conceded); V2's located-quote rules graft on |
| C-006 | V4 | Process exit for phases; hook snapshot for mid-run, with my timestamp test as the acceptance check |
| C-007 | V4 | Relative and ground-truth-free; per-design echo |
| C-008 | V4 | Switched: same per-issue chain method as V2, executed without V2's D1/D5 errors |
| C-009 | V5 | Three measured shares |
| C-010 | V2 | Fresh A0 plus catalogue arm; V5's sizes; A6 for F3 |
| C-011 | V2 | One reach endpoint, correct Fisher, final-look efficacy only |
| C-012 | V1 | Every design on a seed baseline |
| C-013 | V1 | Panel-level finish signal, on B_A1 |
| X-001 | V5 | Bottom-up 0.03-0.34; my 0.8-2.1 withdrawn |
| X-002 | V1 | 0 on /14; control may fall in sonnet panels |
| X-003 | V1 | GT6 = I1 per SEED:71 |
| X-004 | V5 | HL2 legal; the shadow schedule gives +0% when haiku stays a canary |
| X-005 | V1 | The slowest luna sets 116 s |
| X-006 | V4 | One block, P2-F ids, origin stripped; V3 req 6 conceded |
| X-007 | V2 | Switched: V2's located-verbatim quote check closes the one free-text path V4 R-06 leaves (the anchor field) |
| X-008 | V1 | Grading and judge held constant, sha256-pinned |
| X-009 | V1 | Truncate, validate, re-ask: no residual drop |
| X-010 | V5 | The kit may win; A2 is the comparator |
| X-011 | V5 | No AC-level anchors; applied above to F1 and F7 |
| X-012 | V1 | I7 on control /2, both scales defined (V1:17) |
| X-013 | V2 | 4/6 vs 0/6 = 0.030, verified |
| A-001 | V1 | REQ-S3 tests the act, not only delivery |
| A-002 | V5 | Prices the kit's time; drives the slowdown limits |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | /3 flagged; per-run `wall_s` check |
| A-006 | V2 | Decoys, now carried by the gap card |
| A-007 | V4 | Spike, fallback, `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD`; clean `git status` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V2 | Low end about 0 for never-found issues; applied above to F1 and F7 |

### Variant 4 Rebuttal (opus:devops)

### Round 2 rebuttal: V4 (opus, devops lens)

Citations: `V<n>:<line>` = variant files; `R1-V<n>:<line>` / `R2-V<n>:<line>` = debate statements; `SEED:<line>` = seed brief. I re-read V4:276-445, :455-579 and :640-745, V5:138-156 and :350-392 for this round, and recomputed every number below.

#### Responses to criticisms of V4

| Criticism (raised by) | Response |
|---|---|
| V4-2 worst case 116 + 6 + 38 = 160 s (+37.9%); the 125 s delivery deadline cannot bind (all) | **Concede** (as in R1-V4:61-65). The converged block (agenda 3) is 143.6 s, worst 150.0 s. |
| V4-2 needs a `panel-seal` turn from luna, who makes about 1 Bash call per run (V1, V2, V3) | **Concede.** Replaced by the hook-side transcript snapshot (R2-V1:82). My `seal_missing` runbook row (V4:335) becomes a fail-closed rule (agenda 3). |
| V4-2's 15 s Stop hold (V3, V5) | **Concede.** V5's "never wait" (V5:297) is right; dropped. |
| V4-3 timeout 45 s (V4:375) vs 35 s (V4:396) (all) | **Concede.** Superseded by V1's box rule (agenda 2). |
| n = 4 screen; "2 of 4 and +2 vs A1" passes at Fisher p = 6/28 = 0.214 (V2) | **Concede.** C(4,2)/C(8,2) = 6/28 = 0.214, recomputed. V2's plan replaces mine (agenda 6). |
| V4-4/V4-5 sit on non-seed baselines (V1, V2, V3) | **Split.** S13 is a seed baseline (SEED:25 "ember + luna ~300 s"; accepted at R2-V1:158, R2-V2:210). S14 is not: **concede**, V4-5 moves to SL2. |
| V4-3 sends real anchors with no decoy (V1, V2, A-006) | **Concede.** Gap-card decoy (agenda 2). |
| "Plus H share" reported additively although V4:184 says H and C interact (V1) | **Concede.** Every block shows C and H in separate columns, C conditional on H (agenda 7). My "+0.2 to +0.6" (V4:327, :433) is withdrawn for 0.03-0.34. |
| R-24 applies a per-package cap to a three-package mean (V5) | **Counter.** R-24 is "per package, `elapsed_s <= 1.35 x median A0 elapsed for that package`" (V4:735). V4's A0 already carries H1-H4 ("All arms use harness fixes", V4:648). So V4's A0 *is* the merged spec's A1; agenda 8 adopts it. Only the planning arithmetic used /3, and I conceded that (R1-V4:72). |
| No within-run attribution; H only against historical S07 (V2) | **Concede.** Fresh A0 plus sealed-report judging for F1 (agenda 6). |
| My R1 graft of V2-D5 witness lines as harness-generated F7 cards fails V4:523 (R2-V1, R2-V2, R2-V3) | **Concede.** V4:523 says a deterministic extractor "would be a prompt and harness change, not collaboration". My own test rejects my graft. The witness moves to F4 as a sweep kind. |
| V4-2's I7 row "two lunas" double-counts once V2-D1 disjoint locators are grafted (R2-V3:87-91) | **Concede for the merged design, counter for V4 as written.** In V4-2 both lunas get every fact (V4:288), and the union 1 - (1 - p)^2 gives 0.31-0.75, so 0.25-0.60 was conservative. After the disjoint graft, one luna gets the test file: 0.7 x 0.6 x 0.4 = 0.17 to 0.9 x 0.8 x 0.7 = 0.50. Merged F4 I7 = **0.17-0.50 control /2**. |
| V4-3 haiku variant gain 0.40-1.60 is unreachable: lunas end at 148 s, haiku's anchors exist only at 238 s (R2-V3:65-69) | **Concede.** V4:402 runs the lunas' phase 2 "inside haiku's phase-1 window", but V4:430 credits haiku's anchor rate. The only repair is to make the lunas wait for haiku: 238 + 6 + 25.6 = 269.6 s, haiku 290 s (+21.8%). That costs 22 points of time and loses V5-D5's isolated canary. The slate takes V5-D5 as written (+0%, worst +6.3%). |
| V4-3 B1 0.03-0.15 rests on Task-level anchors (X-011) | **Concede** (R1-V4:66). Applied below; I also move I4 (agenda 2). |
| V4-4 two-way compliance plus a Stop hold (V5) | **Concede for the two-way form.** The one-way EL2 form (agenda 1) removes luna posting and the hold. |
| V4 H2 only re-asks (X-009) | **Concede** (R1-V4:69). V1's truncate, validate and re-ask. |

#### Agenda items

##### 1. Slot 5: F5 versus F7

**F7, V4-4, re-based to EL2 and run one way (ember flags, lunas adjudicate).** This was my R1 core. V1, V2 and V3 now hold it (R2-V1:24, R2-V2:25, R2-V3:28).

Steelman of F5 (V5's R1 core): it is the only family aimed at the source-only rules B5, I1 and B2, which the checkout masks (V2:424). But its mechanism is F4's: a searcher posts facts and a reader acts on them (V2:424-431). Two such slots fail the "five distinct" test. The B5/I1/B2 target survives as a sweep kind in F4. F7 is the only slot where a model marks a place without judging it and a *different* model must answer with a finite check (V4:463-468). A5 (F7) against A4 (F4) on the same panel answers SEED:47.

**Arithmetic and a correction nobody raised.** V4-4's chain (V4:506) has no factor for "the card is actually adjudicated". On S13 ember posts up to 4 cards, but luna adjudicates at most 2 (V4:478). Up to half the cards are never answered, so my S13 gain was overstated by up to 2x. The one-way EL2 form fixes this: two lunas x 2 hash-split cards = 4 slots, one per ember card.

| F7 (EL2, one way) | Value |
|---|---|
| luna B | 116 + 2 x 2 x 6.4 + 2 (hooks) = **143.6 s (+23.8%)**; worst +6.4 = **150.0 s (+29.3%)** |
| ember | 41 + 4 posts x 3.2 = 53.8 s, off the critical path |
| C /14 | V4 rows 0.16-0.93, minus luna search-card rows B8/B6 (0.03/0.16) = 0.13-0.77, minus B1/B2/I5 low ends (A-011) = **0.08-0.77** (R2-V3:44, accepted); I7 0-0.10 |
| S13 variant at 1 adjudication (R2-V3:48) | 114.8 s, worst 121.2 s, but only 1 of 4 cards answered: gain falls to about 0.02-0.19. **Drop it** from the slate; it is not worth an arm. |

Operational gates: `cards_sent > 0` in spike, stop the arm above 50% zero-card runs (V4:531), REQ-S3 act rate, V2's `flag_finding_overlap` > 50% adds a gap-card decoy (R2-V2:38).

##### 2. F1 core, time box and gap card

**Concede the core to V4-3.** In R1 I alone chose V2-D2 as core. With V2's grafts (decoy ratio, `contradiction` -> M7) on V4-3's anchor-text routing and combiner, the result is the same design. V2 itself prefers V4-3's combiner (R1-V2:102).

**Box rule: adopt V1's** `box = min(35, T0 + 1.30 x B_A1 - start)`, `n = min(cap, floor((box - 6) / (2 x turn)))` (R2-V1:51-53). Recomputed: luna A 95 + 6 + 25.6 = 126.6 s; luna B box 34.8, n = floor(28.8/12.8) = 2, end **147.6 s (+27.2%)**; ember n = 3, end 141.2 s; hard bound 150.8 s (+30.0%); last useful start 150.8 - 18.8 = 132.0 s. Devops addition: on timeout the combiner emits the phase-1 block unchanged and logs `phase2_timeout` (V4:375, R2-V3:81).

**Gap card fills the decoy slot.** This was my R1 position, now shared by V1, V2 and V3. Each slot holds the gap card with p = 1/3, seeded per receiver, rendered identically and with its kind withheld. With 2 slots, P(no decoy) = 4/9 and P(both) = 1/9. ECHO (V4 R-25, > 30%) is computed on real-anchor slots only (R2-V2:72).

**HL2 variant: V5-D5 as written** (concession above). The lunas exchange luna anchors in haiku's shadow, and haiku stays an isolated canary: +0%, worst 253 s (+6.3%; 253/238 = 1.063). Because phase 2 is free there, the luna cap can stay at V5's 8 turns: 116 + 6 + 4 x 12.8 = 173.2 s < 238 s.

**F1 gain with all conceded corrections.** R2-V3:73-79 zeroes B1 and B2 but keeps I4. T2b covers B1, B2 *and* I4 (C-002; R1-V2:62). So I4 also moves to the gap route:

| Step | Low | High |
|---|---|---|
| V4-3 rows (V4:421-429) | 0.23 | 0.94 |
| Remove anchor-route B1, B2, I4 (0.07 / 0.31) | 0.16 | 0.63 |
| I5, I6 low ends to 0 (A-011) | 0.09 | 0.63 |
| Decoy displacement x 2/3 at the low end | 0.06 | 0.63 |
| Gap-card route to B1/B2/I4, 0-0.10 | **0.06** | **0.73** |

##### 3. F4 core and its worst case

**Core V4-2; the converged block** (R2-V1:69-75, R2-V2:82-86, R2-V3:85): sweeper 41 + 6 + 10 x 3.2 = 79 s, inside ember's idle time; luna B 116 + 2 x 2 x 6.4 + 2 = **143.6 s (+23.8%)**; worst **150.0 s (+29.3%)**. This matches my R1 fix (144 s / 150 s, R1-V4:65). Rules: at most 2 facts per luna, no Stop hold, late facts logged `late` and dropped.

Devops rules the other blocks leave implicit:

| Rule | Why |
|---|---|
| **Fail closed on the seal, fail open on the review.** If the snapshot write or hash fails, the hook delivers nothing and logs `snapshot_missing`; the review continues (R-22). | Never deliver to an unsealed reviewer. A hook error must never kill a review. |
| Snapshot under `$BOARD`; harness records sha256 in `collab.json`; V3 timestamp test (R2-V3:99) | Bash is unrestricted (A-008). |
| Sweeper `timeout` at T0 + 85 s; atomic fact writes (R2-V3:100-101) | `--max-turns` does not exist (V5:106). |
| Hang guard: process `timeout` at T0 + 1.5 x B_A1 (174 s at planning B) on every reviewer in mid-run arms. A kill counts as `SLO_BREACH`. | Mid-run designs cannot be cut off without losing the report (R2-V1:147). Their bound is count caps plus the finish signal. A hung gateway session still needs a ceiling. The 1.5x figure is the existing "no package > 1.5x" guard. |

C /14 stays 0.14-0.67 (V4:325 rows re-added). The witness kind takes 1 of the 4 fact places and replaces the 0-0.05 B5/I1 placeholders. I7 is **0.17-0.50** (concession above).

##### 4. F3 grafts

I accept the converged set: V2-D4 Task x move cells filled from V4-1 telemetry; V1-R1 per-receiver hash order; V5-D4's skip rule only; V3's leak check on variable fields only (R2-V3:110); the surface filter; V3-R1 resume digest as the fallback if S0 fails (147.6 s). R2-V1:95 rejects the V5-D4 Stop block: 116 + 12.8 + 19.2 + 2 = 150.0 s against 143.6 s, and it rests on the unverified reissue. I recomputed and agree. Deadline: write it as `T0 + 1.35 x B_A1 - 47 s` (110 s at planning B; V4:215 said 110 s, the correct 157 - 45 is 112 s).

##### 5. F6 requests versus uncovered cells

**Accept the V1/V2/V3 merge.** The harness renders imperative requests only from V2-D4 uncovered cells, ranked by luna's declared not-checked scope. There are no covered counts, and V4:545's "Tasks that already have a finding ... with the counts" is withdrawn as a clearance signal (V5 C-2). No SendMessage. The surface filter (V4:563) stays. Precision fix: SL2 = 821/3 = 273.7 s, so worst 330 s is **+20.6%** and typical 302 s is +10.4% (the +20.4%/+10.2% figures used 274).

##### 6. Experiment section

**Adopt R2-V2's plan** (R2-V2:118-148): A0 fresh (4) plus S07 context; A1 and A2 at 12; A3 F1, A4 F4, A5 F7, A6 F3 at 6 -> 12; stage 2 on SL2 for F6. One reach endpoint. Fisher one-sided p < 0.05 at the final look only: 4/12 vs 0/12 = 495/10,626 = 0.047 passes; 3/12 vs 0/12 = 220/2,024 = 0.109 fails. X must also beat A2 by >= 4 at n = 12. The interim look is futility only (R2-V2:144). Size: 4 + 12 + 12 + 4 x 12 = 76 maximum, 52 minimum, plus 30 in stage 2.

Operational requirements the plan needs from V4:
- A1 runs with `PANEL_COLLAB=0`, and its launch command is checked byte-identical to today's plus H (R-05). Otherwise "A1" is not the panel a design replaces.
- Gate 0: S0 (hooks fire), S2 (resume), S3 (full-chain smoke, 0 dropped lines) and REQ-S3 act rate, recorded before any arm (R-27).
- Conduct: `NOFALLBACK=1`, at most 10 concurrent runs and at most 4 ember, `model_ok` for sweeper and phase-2 sessions (R-28), block-randomised order (V5).
- Guard: SLO error budget, 1 package in 12 over 1.35 x B_A1 per arm, stops the arm (R-24).

##### 7. Harness share figure

Carry **H = 0.03-0.34 /14 per run, central 0.14** (V5:147-151; low 0.02 + 0.01 + 0.00, high 0.16 + 0.08 + 0.10, central 0.08 + 0.03 + 0.03, all re-added). H-4 is excluded (X-008); V5's table never counted it, so the range is unchanged. H-6 is a secondary score. Leak removal adds 0 on /14 and is a sonnet-panel I7 measurement correction on control. Spike 5 replaces the normalizer row. Each gain block carries C and H in separate columns and never sums them.

##### 8. Idle-time budgets and the baseline rule

**Adopt V1's five-part rule** (R2-V1:139-147), **V2's per-slot slowdown limit** (R2-V2:176-187) and **V3's drift band** (R2-V3:162-168). Rechecked: s <= (0.35B - W)/B gives F4/F7 6.6/116 = 5.7%, F3 13.0/116 = 11.2%, F6 39.9/274 = 14.6%. Drift band lower edge 1.30/1.35 = 0.963.

Two devops refinements:

1. **Measure s on the critical-path reviewer, not the arm.** The cap moves only if the *slowest luna* slows. In F4 the extra brief text goes to the sweeper; in F7 most goes to ember (off the path). F4's 5.7% limit is therefore far easier to meet than it looks, provided luna's brief is unchanged. Spike 4 logs per-role end times; the limit applies to the role that sets B.
2. **Name the baseline once.** V4's "A0" (V4:648, R-24) is the merged A1. The merged spec renames it, so that no requirement measures the cap against the old-harness arm.

#### Updated assessment of other variants

- **V1:** R2's repairs are the best in the debate: the B_A1 box, one-way F7, withdrawing first-Stop delivery and the hook snapshot. It carries the mislabelled HL2 figure (R2-V1:61).
- **V2:** Its futility-only interim look and per-slot slowdown limit are needed. Its `flag_finding_overlap` is a cheap, ground-truth-free alarm, and I adopt it. It rejected my witness graft correctly.
- **V3:** This round's most useful auditor. It found the HL2 mislabel, my haiku-variant error, the disjoint-split I7 double count and the drift-band gap. Its F1 gain keeps I4 on the anchor route, which T2b does not allow.
- **V5:** Not yet heard in R2. "Never wait", the 12-run controls, the H table and the shadow schedule are all in the slate. Its F5 core is the only R1 slot no longer supported.

#### Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Anchor-text routing plus V2-D2 `contradiction` -> M7; decoy slot = V1-R3 gap card (p = 1/3 per slot, kind withheld); V1 box min(35, T0 + 1.30 B_A1 - start); V4 combiner with `phase2_timeout` fallback; V2 sealed-report judging; HL2 variant = V5-D5 as written (haiku canary) | Sealed by process exit, no hooks. EL2 147.6 s (+27.2%), hard 150.8 s (+30.0%); HL2 +0%, worst +6.3%. C 0.06-0.73 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint ranked locators; V1-R2 harvest incl. sweeper output; V2-D5 witness as a sweep kind; V5-D3 first-hand rule and 10% stop; 2 facts per luna, no hold; hook snapshot seal, fail-closed, sha256 by harness, V3 timestamp test; sweeper timeout T0 + 85 s; hang guard 1.5 x B_A1 | Only cheap I7/T1 path, in ember's idle time. 143.6 s (+23.8%), worst 150.0 s (+29.3%). C 0.14-0.67; I7 0.17-0.50 control |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move cells from telemetry; V1-R1 hash order; V5-D4 skip rule only; V3 leak check on variable fields; surface filter; V3-R1 resume-digest fallback | No model authors anything. 143.6 s (+23.8%), worst = expected; arm A6 tests exchange vs kit |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Harness-rendered requests from uncovered cells only, ranked by luna's not-checked scope; no covered counts; V1-R5 brief line; V3 leak check; surface filter; no SendMessage | Harness author, Claude receiver. Worst 330 s (+20.6% of 273.7 s), typical +10.4% |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Hash-split cards, at most 2 per luna (4 slots = 4 cards); hook snapshot seal; no luna card, no hold; V5 C-3; `PANEL_FINISH_AT`; `flag_finding_overlap` alarm; S13 variant dropped | Distinct mechanism; answers SEED:47 against slot 2 on one panel. 143.6 s (+23.8%), worst 150.0 s (+29.3%). C 0.08-0.77 |

Shared substrate: V4 board with baked path (R-21), kill switch (R-05), hooks exit 0 (R-22), `collab.json` (R-23), SLO budget against B_A1 (R-24), quarantine-in-place (R-26); V1 `PANEL_FINISH_AT = T0 + 1.20 B_A1`; V2 no-free-text rules over V4's 12-200-character anchors; V4 relative alarm (J + 0.15 or ledger rows -20%) plus per-design echo.

Proposed base document: V4

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Kill switch, baked path, timing and baseline tables |
| S-003 | V2 | Gate funnel names the blocked gate; B1/B2/I4 exposure cells take V5's T2b correction |
| S-004 | V5 | Net collaboration, static-kit row, tokens per added issue |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Itemised unverified list tied to each number |
| C-001 | V1 | Switched: searcher/reader complementarity is what slot 2 tests; V2's 48/48 is its evidence |
| C-002 | V5 | T2a/T2b decides which routes reach B1/B2/I4 (applied to F1 above) |
| C-003 | V1 | Truncate, validate, re-ask; grading constant |
| C-004 | V4 | Best-style column used by routing in slots 1, 3, 5 |
| C-005 | V4 | Switched: 12-200-character anchors fit F1 (V2 conceded); V2's located-quote and forbidden-key rules graft on |
| C-006 | V4 | Switched: process exit for phases, sealed artifact for mid-run, now a fail-closed hook snapshot |
| C-007 | V4 | Relative and ground-truth-free, runs in the product; per-design echo |
| C-008 | V4 | Per-issue chains; the I7 doubling was valid as written (union), the haiku-variant row is conceded |
| C-009 | V5 | Three measured shares, C and H never summed |
| C-010 | V2 | Fresh A0, catalogue arm, A6 for F3; V5's sizes |
| C-011 | V2 | One reach endpoint, correct Fisher, futility-only interim, +4 over A2 |
| C-012 | V1 | Every design on a seed baseline |
| C-013 | V1 | Panel finish signal, on B_A1 |
| X-001 | V5 | Bottom-up 0.03-0.34, measurable by spike 5 |
| X-002 | V1 | 0 on /14; control may fall in sonnet panels |
| X-003 | V1 | GT6 = I1 per SEED:71 |
| X-004 | V5 | HL2 legal; shadow schedule +0% with haiku canary |
| X-005 | V1 | The slowest luna sets 116 s |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text; forbidden keys enumerated |
| X-008 | V1 | Grading and judge held constant, sha256-pinned |
| X-009 | V1 | Truncate, validate, re-ask: no residual drop |
| X-010 | V5 | The kit may win; A2 is the comparator |
| X-011 | V5 | No AC-level anchors; anchor routes to B1/B2/I4 go to the gap card |
| X-012 | V1 | Switched: V1, V2, V4, V5 equivalent; V1:17 defines both scales most precisely |
| X-013 | V2 | 4/6 vs 0/6 = 0.030, verified |
| A-001 | V1 | REQ-S3 tests the act, not only delivery |
| A-002 | V5 | Prices the kit's time; drives the slowdown limits |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction and applies H in all arms |
| A-005 | V5 | /3 flagged; per-run `wall_s` check |
| A-006 | V2 | Decoys, now carried by the gap card |
| A-007 | V2 | Spike, fresh fallback and R-17's slash-command guard, which V4 lacks |
| A-008 | V4 | Helpers write only under `$BOARD`; clean `git status`; candidate hash |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | c capped against SL2's measured reach |

### Variant 5 Rebuttal (sonnet:performance)

### Round 2 rebuttal: V5 (sonnet, performance lens)

Citations: `V<n>:<line>` = variant files; `R1-V<n>:<line>` / `R2-V<n>:<line>` = debate statements. Every number below was recomputed this round (Fisher values by exact hypergeometric sum).

#### Responses to criticisms of V5

| Criticism (raised by) | Response |
|---|---|
| Fisher clause "4 vs at most 1, p <= 0.10" fails (all) | **Concede** (R1-V5:75). 4/6 vs 1/6 = 0.121. V2's rule replaces it. |
| 120-character `note` field can carry a conclusion (all) | **Concede.** Dropped; V2's no-free-text rules over V4's 12-200-character anchors. |
| H-4 and H-6 change grading inside "harness share" (all) | **Concede.** H-4 is out. H-6 is a secondary score only. My H table (V5:147-151) never counted H-4, so the range is unchanged (agenda 7). |
| 0.25x-2x band is fixed, not per issue (all) | **Concede.** The merged slots use per-issue chains. My band survives only as a labelled placeholder for the HL2 variant (agenda 2). |
| Call-6 gate leaves no sealed artifact (V1, V2, V4) | **Concede.** Hook-side transcript snapshot under `$BOARD`, sha256 recorded by the harness, V3 timestamp test (R2-V3:99, R2-V4:73). |
| D2 caps disagree (2 injections vs 3-5 flips) (V1, V4) | **Concede.** D2 is in no slate. |
| Sweep Desk depends on luna requests and a Stop wait loop (V2) | **Concede** (R1-V5:86). V4-2's push model is the F4 core. |
| Shadow Resume needs HL2, about 3x EL2's tokens (V2) | **Partial counter.** The 3x is the panel's cost, not the design's: the design adds +3.6k on 63.7k = +5.7% (V5:386). The variant fits only a panel that already has a slow member (V5:396). It is not a reason to choose HL2, and it gets no arm in stage 1 or 2. |
| My R1 claim that V2-D2 leaves ember idle until about 102 s (V2 counter, R2-V2:14) | **Concede.** My own rule says time inside the slowest reviewer's window is free (V5:77). Idle is not elapsed. |
| My R1 claim that V4 R-24 caps a three-package mean (V4 counter, R2-V4:17) | **Concede.** V4:648 puts H1-H4 in every arm, so V4's A0 is the merged A1, and R-24 is per package. |
| Resume replays the session as input tokens (my own R1 critique of V1) | **Self-concession.** My S-004 column "output tokens per added issue" (V5:404) ignores input tokens. F1 replays the whole phase-1 context. The merged table needs an input-token column for resume designs. |
| My experiment cannot detect my own central estimates (R1-V5:85) | **Stands, and it applies to the merged plan too** (agenda 6). |

#### Agenda items

##### 1. Slot 5: F5 versus F7

**Concede to F7 (V4-4, EL2, one way).** V4 states correctly that my F5 core is the only R1 slot no longer supported (R2-V4:116).

Steelman of my F5 (V5-D1): it is computed once by ember and delivered to n-1 readers, so it scales O(n). It costs 143 s (+23.3%) and +14% tokens (V5:183-184).

Why it loses:
- Its mechanism is "a searcher posts, a reader acts", which is F4's mechanism (R2-V1:26). Two such slots fail the "five distinct" criterion.
- Its net collaboration share is 0.07 (V5:193), the second lowest of my five.
- It is thin whenever ember skips source.md, which happens in 39% of runs (V5:197). Its B5/I1/B2 target survives as the witness sweep kind inside F4.

**Performance check on F7.** F7 costs exactly what F4 costs: luna B 116 + 2 x 2 x 6.4 + 2 = 143.6 s (+23.8%). ember adds 4 posts x 3.2 s, ending at 53.8 s, off the critical path. So A5 (F7) against A4 (F4) differs in message content only, at equal time and equal receiver turns. That is the cleanest possible test of SEED:47.

I accept C = 0.08-0.77 (R2-V3:44, R2-V4:40) and dropping the S13 variant (R2-V4:41: one adjudication answers 1 of 4 cards, gain about 0.02-0.19).

##### 2. F1 core, time box and gap card

I accept the V4-3 core, V1's box rule and the gap card filling the decoy slot at p = 1/3 (R2-V1:51-63).

| Check (planning B = 116) | Value |
|---|---|
| Box | min(35, T0 + 1.30 x 116 - start); deadline 150.8 s |
| luna B | box 34.8 s, n = floor(28.8 / 12.8) = 2, end 116 + 6 + 25.6 = **147.6 s (+27.2%)** |
| Last start with n >= 1 | 150.8 - 18.8 = 132.0 s, which is a brief slowdown of s = 132.0/116 - 1 = 13.8% |
| Hard bound | **150.8 s (+30.0%)** |

**Performance additions.**
- **F1 is the only slot with a compliance-free hard bound.** The phase-2 process is killed by `timeout` at the deadline, and the combiner emits phase 1 (`phase2_timeout`, R2-V3:81). Slots 2, 3 and 5 depend on luna obeying "finish now" (agenda 3).
- **Input tokens.** Each resume replays about 16 turns of context. Log resumed input tokens per arm. Cost per added issue for F1 must include them.

**HL2 variant: V5-D5 as written.** V3 is right that R2-V1:61 and R2-V2:65 cite V4's haiku schedule, not mine (R2-V3:65-69). The lunas exchange luna anchors inside haiku's window, and haiku stays an isolated canary:
- 4 challenges at most: 116 + 6 + 4 x 12.8 = 173.2 s < 238 s, so **+0%**;
- the 15 s rule gives a worst case of 253 s = **+6.3%** (253/238 = 1.063).

Its gain cannot be carried as stated. The 0.06-0.46 /14 (V5:392) is my conceded fixed band, and V4's 0.40-1.60 credits haiku anchors that arrive too late (R2-V4:21). The merged spec labels the HL2 gain "to be re-derived per issue from luna-to-luna anchor rates" and runs no HL2 arm. My EL2 variant (ember-only resume, 146 s, +25.5%, V5:388) is superseded by V4-3's EL2 schedule.

##### 3. F4 core and its worst case

I accept the converged core: V4-2 with 2 facts per luna, no Stop hold, a hook seal and late facts dropped. That gives 143.6 s (+23.8%). I7 = 0.17-0.50 on control (R2-V3:87-91; R2-V4:20). The sweeper starts at ember's exit (V4:284), not at T0. A start at T0 would put two ember processes in every package against the cap of 4 concurrent ember (V4:661), which halves package parallelism for no elapsed gain.

**The 150.0 s worst case is the wrong bound.** R2-V1:75 computes it as "planned path + one turn of slip". The bound that holds for any natural end is set by the finish signal:
- "finish now" is injected at the first PostToolUse after 139.2 s, so up to one turn later, at 145.6 s;
- luna then writes its report, which takes T_report.

| T_report | Bound | vs 116 s |
|---|---|---|
| 6.4 s (mean turn) | 145.6 + 6.4 = 152.0 s | +31.0% |
| 11.0 s | 156.6 s | **+35.0% (cap)** |

So the cap holds for slots 2, 3 and 5 only if luna's final report turn takes at most 11.0 s. That turn emits the whole `findings-v1` block, so it is output-heavy and probably longer than the 6.4 s mean, and nobody has measured it. If luna ignores the signal, the only bound is V4's hang guard at 1.5 x 116 = 174 s (+50%, R2-V4:76). That guard is a backstop, not cap enforcement.

**Rules:**
- Spike 4 logs every luna's last-turn duration.
- `PANEL_FINISH_AT = T0 + min(1.20 x B_A1, 1.35 x B_A1 - turn_p90 - T_report_p90)`. At planning values both terms give 139.2 s.
- REQ-S3 also measures the act rate on "finish now".

##### 4. F3 grafts

**Concede on V5-D4.** Its Stop block replaces a 2-turn checkpoint with a 3-turn Stop move: 116 + 12.8 + 19.2 + 2 = 150.0 s against 143.6 s. It also rests on the unverified Stop reissue. I keep only its rule "a covered region is never a reason to skip" (V5:343). V1-R1's per-receiver hash order already does the job of my rotating permutation.

I accept the rest of the converged set:
- V2-D4 Task x move cells filled from telemetry;
- V3's leak check on variable fields only;
- the surface filter;
- the V3-R1 resume-digest fallback (147.6 s).

F3 is bounded by its count caps plus the finish signal, so the T_report condition in agenda 3 applies to it as well.

##### 5. F6 requests versus uncovered cells

**Concede to the merge** (R2-V1:102). My R1 objection was to covered counts, which act as a clearance signal (V5:130). The merge removes them. An imperative request drawn from an uncovered cell costs sonnet no more turns than a list, since the cap stays at 4 turns (56 s).

Numbers, with V4's precision fix (R2-V4:86):
- worst 330 / 273.7 = **+20.6%**;
- typical 302 / 273.7 = +10.4%;
- headroom 369.5 - 330 = 39.5 s.

That makes F6 the most time-robust mid-run slot.

##### 6. Experiment section

**Adopt R2-V2's plan** (R2-V2:118-148): A0 fresh at 4 runs, A1 and A2 at 12, A3-A6 at 6 -> 12, a futility-only interim look, Fisher p < 0.05 at the final look, and +4 over A2. V2's futility correction (R2-V2:144) also fixes my own interim look (V5:454), whose three stop conditions it reuses. Checks: 4/12 vs 0/12 = 0.047 passes; 3/12 vs 0/12 = 0.109 fails.

**Cost, from my per-run figures (V5:448: A1 63.6k, A2 83k, exchange 70-83k output tokens).**

| Stage | Runs | Output tokens |
|---|---|---|
| 1, all exchange arms reach 12 | 76 | 4 x 63.6k + 12 x 63.6k + 12 x 83k + 48 x 70-83k = **5.4-6.0M** |
| 1, all stop at 6 | 52 | 3.7-4.0M |
| 2 on SL2 (139k per run, V5:412) | 24-30 | **3.3-4.2M**. Each run takes 821/348 = 2.36x an EL2 run's wall time |

Stage 2 costs about as much as all of stage 1, for one design.

**Stage 2's endpoint does not transfer.** The Fisher references assume 0 reach in the control. Sonnet + 2x luna already reached I7 in 3 of 6 runs (V5:94).

| A1-SL2 reach | X needed | Fisher one-sided |
|---|---|---|
| 6/12 | 11/12 | 0.034, passes |
| 6/12 | 10/12 | 0.097, fails |

On hard credits per run (SD 0.94, V3:163), 12 vs 12 detects about 2.49 x 0.94 x √(2/12) = **0.96 /14**. That is near the top of F6's 0.26-1.06 (R1-V2:126).

Rules:
- Pre-register stage 2 as a **screen**, with hard credits per run (one-sided permutation p < 0.05) as its primary endpoint.
- A2-SL2 has only 6 runs (R2-V2:127), so state its margin as a rate: X beats A2-SL2 by at least 1/3 of runs.
- Gate stage 2 on stage 1's completion and budget.

##### 7. Harness share figure

Carry **H = 0.03-0.34 /14 per run, central 0.14**:
- low 0.02 + 0.01 + 0.00 = 0.03;
- high 0.16 + 0.08 + 0.10 = 0.34;
- central 0.08 + 0.03 + 0.03 = 0.14 (V5:147-151).

H-4 is excluded. H-6 is secondary. Leak removal counts 0 on /14 and is a correction to sonnet-panel I7 on control. C and H go in separate columns, and C is conditional on H (A-004).

Two corrections to my own table:
- V5:143 measures H against historical EL2. Replace that with the fresh A0, keeping S07 as context.
- **H is an estimate, not a test.** A0 at 4 runs against A1 at 12 detects about 2.49 x 0.94 x √(1/4 + 1/12) = 1.35 /14, roughly 10x the central H. Only spike 5 (rescoring with the normalizer, judge calls only) measures a row exactly. The spec should say so.

I switch X-001 to V5. V2's own rows sum to 0.10-0.55 (V2:143-147: 0.05 + 0 + 0.05; 0.15 + 0.1 + 0.3), as V2 itself conceded (R2-V2:157).

##### 8. Idle-time budgets and the baseline rule

**One rule.** It merges V1's five parts (R2-V1:139-147), V2's slowdown limit (R2-V2:176-187), V3's drift band (R2-V3:166-168), V4's critical-role refinement (R2-V4:108) and my finish-time term.

1. **Baseline B_A1** is the per-package A1 median: isolated, H applied, `PANEL_COLLAB=0`, and a launch command byte-identical to today's plus H. V4's "A0" is renamed A1. The 116 s figure is a labelled planning value only, and every block is written as a formula in B.
2. **Two measurements.**
   - Frozen B_f (spike 4) sets the in-run deadlines.
   - Concurrent B_c sets the cap test.
   - Log B_c/B_f per randomized block. Outside [0.963, 1.10], re-freeze B_f; 0.963 = 1.30/1.35.
3. **Slowdown limit, measured on the critical-path role.** Each design's brief may slow the slowest luna by at most s = (0.35B - W)/B.

   | Slot | Limit |
   |---|---|
   | F4, F7 | 5.7% |
   | F3 | 11.2% |
   | F6 | 0.35 x 273.7 = 95.8; (95.8 - 56)/273.7 = **14.5%** (V2's 14.6% used 274) |
   | F1 | n = 0 beyond 13.8% |

   My kit estimate of +29% (V5:411) is why this binds. A slot over its limit carries only its injected moves, not the kit. A2 versus X is then "kit or exchange", which is the deployment choice.
4. **Finish time:** `PANEL_FINISH_AT = T0 + min(1.20 B_f, 1.35 B_f - turn_p90 - T_report_p90)` (agenda 3).
5. **Cap test:**
   - median per package <= 1.35 B_c;
   - no package above 1.5x;
   - SLO budget of 1 package in 12 (R-24);
   - a hang-guard kill counts as a breach.

#### Updated assessment of other variants

- **V1.** Its repairs are the best in the debate: the B_A1 box, one-way F7 and the hook snapshot. Its "worst 150.0 s" for F4 is a typical-path figure, not the finish-signal bound (agenda 3).
- **V2.** Its futility-only interim look and slowdown limit are needed, and its `flag_finding_overlap` alarm is cheap. Its stage-2 arm inherits a reach endpoint that does not fit sonnet panels (agenda 6).
- **V3.** The best auditor this round. It found the HL2 mislabel, which restores V5-D5's +0%, the I7 double count and the drift gap.
- **V4.** It conceded honestly. Its counter on R-24 is correct, and its hang guard and fail-closed seal are the right operational rules. The hang guard is not cap enforcement.

#### Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Anchor-text routing + V2-D2 `contradiction` -> M7; V1-R3 gap card as the decoy slot (p = 1/3, kind withheld); V1 box min(35, T0 + 1.30 B_A1 - start); V4 combiner with `phase2_timeout`; V2 sealed-report judging; resumed input tokens logged; HL2 variant = V5-D5 as written (haiku canary, gain to be re-derived) | Only compliance-free hard bound: 147.6 s (+27.2%), hard 150.8 s (+30.0%); HL2 +0%, worst +6.3% |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint locators; V1-R2 harvest incl. sweeper output; V2-D5 witness kind; V5-D3 first-hand rule + 10% stop; 2 facts per luna, no hold; fail-closed hook snapshot + sha256 + V3 timestamp test; sweeper timeout T0 + 85 s; T_report-based finish time | Only cheap I7/T1 path, in ember's idle window; 143.6 s (+23.8%); bound 145.6 + T_report |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move cells from telemetry; V1-R1 hash order; V5-D4 skip rule only; V3 leak check (variable fields); surface filter; V3-R1 resume fallback | No model authors anything; 143.6 s (+23.8%); arm A6 tests exchange vs kit |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Harness-rendered requests from uncovered cells only, ranked by luna's not-checked scope; V1-R5 brief line; V3 leak check; surface filter; no SendMessage | Claude receiver, harness author; worst 330 s (+20.6%), 39.5 s headroom; stage-2 screen |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Hash-split cards, at most 2 per luna; hook snapshot seal; no luna card, no hold; V5 C-3; `PANEL_FINISH_AT`; `flag_finding_overlap` alarm; S13 variant dropped | Same cost as F4, so A5 vs A4 isolates challenge vs findings (SEED:47); 143.6 s (+23.8%); C 0.08-0.77 |

`Proposed base document: V4`

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Kill switch, baked path, timing and baseline tables |
| S-003 | V2 | Switched: the gate funnel makes the H/C split structural; B1/B2/I4 exposure cells take the T2b correction |
| S-004 | V5 | Net collaboration, static-kit row, tokens per added issue; add input tokens for resume designs |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Itemised unverified list tied to each number |
| C-001 | V1 | Searcher/reader complementarity is what slot 2 tests; V2's 48/48 is its evidence |
| C-002 | V5 | T2a/T2b decides which routes reach B1/B2/I4 |
| C-003 | V1 | Truncate, validate, re-ask; grading constant |
| C-004 | V4 | Best-style column used by routing in slots 1, 3, 5 |
| C-005 | V4 | Switched: 12-200-character anchors fit F1 (V2 conceded); V2's located-quote and forbidden-key rules graft on |
| C-006 | V4 | Process exit for phases; fail-closed hook snapshot for mid-run |
| C-007 | V4 | Relative and ground-truth-free; runs in the product; per-design echo |
| C-008 | V4 | Per-issue chains, arithmetically clean |
| C-009 | V5 | Three measured shares, C and H never summed |
| C-010 | V2 | Switched: fresh A0 beats my historical A0; my 12-run controls graft on |
| C-011 | V2 | One reach endpoint, correct Fisher, futility-only interim, +4 over A2 |
| C-012 | V1 | Switched (tie with V5): every design on a seed baseline |
| C-013 | V1 | Panel finish signal; its time term should come from measured T_report |
| X-001 | V5 | Switched: bottom-up 0.03-0.34; V2's rows sum to 0.10-0.55 |
| X-002 | V1 | Switched (tie with V2): 0 on /14; control may fall in sonnet panels |
| X-003 | V1 | GT6 = I1 per SEED:71 |
| X-004 | V5 | HL2 legal; shadow schedule +0% with a haiku canary |
| X-005 | V1 | The slowest luna sets 116 s |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text; forbidden keys enumerated |
| X-008 | V1 | Grading and judge held constant, sha256-pinned |
| X-009 | V1 | Truncate, validate, re-ask: no residual drop |
| X-010 | V5 | Kit may win; A2 is the comparator |
| X-011 | V1 | States 0 AC3 anchors and applies 0.00-0.10 consistently; my D2 contradicted it |
| X-012 | V1 | I7 on control /2; both scales defined (V1:17) |
| X-013 | V2 | 4/6 vs 0/6 = 0.030, verified |
| A-001 | V1 | REQ-S3 tests the act; extend it to "finish now" |
| A-002 | V5 | Prices the kit's time; drives the slowdown limits |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction; H in all arms |
| A-005 | V5 | /3 flagged; per-run `wall_s` check |
| A-006 | V2 | Decoys, carried by the gap card |
| A-007 | V4 | Spike, fallback, `resume_fallback` metric; graft V2 R-17 |
| A-008 | V4 | Helpers write only under `$BOARD`; clean `git status` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | c capped against SL2's measured reach |

### Round 2 tally

### round2: advocates=5 need=4 agreed=43/43 convergence=1.000
| Point | Level | Votes (V1 V2 V3 V4 V5) | Leader | Count | Status |
|---|---|---|---|---|---|
| S-001 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| S-002 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| S-003 | L1 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| S-004 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| S-005 | L1 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| S-006 | L1 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| C-001 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| C-002 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| C-003 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| C-004 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-005 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-006 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-007 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-008 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-009 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| C-010 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| C-011 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| C-012 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| C-013 | L3 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-001 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| X-002 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-003 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-004 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| X-005 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-006 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| X-007 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| X-008 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-009 | L3 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-010 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| X-011 | L2 | V5 V5 V5 V5 V1 | V5 | 4/5 | agreed |
| X-012 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-013 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-001 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| A-002 | L3 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| A-003 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-004 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| A-005 | L3 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| A-006 | L3 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-007 | L2 | V4 V4 V4 V2 V4 | V4 | 4/5 | agreed |
| A-008 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| A-009 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-010 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| A-011 | L2 | V5 V5 V2 V5 V5 | V5 | 4/5 | agreed |
coverage L1: 3 points debated
coverage L2: 31 points debated
coverage L3: 9 points debated

## Round 2.5: Invariant Probe

Full table and required resolutions: `invariant-probe.md`. Result: 33 findings; 8 HIGH UNADDRESSED (INV-001..INV-008) blocked convergence after Round 2 (diff-point agreement 43/43). 13 MEDIUM and 2 LOW UNADDRESSED items were warnings.

## Round 3: Final Arguments

### Round 3 agenda (orchestrator)

### Round 3 agenda (orchestrator; neutral)

Status after Round 2: diff-point agreement 43/43 (1.000, `round2-tally.md`), taxonomy levels L1/L2/L3 all covered, but **CONVERGENCE BLOCKED_BY_INVARIANTS**: the Round 2.5 fault-finder (`../invariant-probe.md`) found 8 HIGH-severity UNADDRESSED items: INV-001, INV-002, INV-003, INV-004, INV-005, INV-006, INV-007, INV-008. 13 MEDIUM items are warnings (do not block) but the merge should close the cheap ones.

Each HIGH item must be closed in this round: either ACCEPT the probe's required resolution (section "Required resolution" in `../invariant-probe.md`), MODIFY it (give the exact replacement rule and why), or REJECT it with evidence that the consensus already handles it. Only these outcomes close an item: a 4-of-5 majority on ACCEPT or on one specific MODIFY text, or a 4-of-5 majority on REJECT.

#### Orchestrator-measured fact for INV-008 (per-package isolated elapsed, slowest reviewer per package)

Computed from `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<package>/reviews/combos/<run>/t*.meta.json` (`wall_s`, max per package-run; non-attempt meta files only). Format: package: (runs, median s, min s, max s).

| Panel | designSpec (DS) | makeTheAliasOnly (AL) | design (DE, control) |
|---|---|---|---|
| ember + 2x luna (g1-*, e2-ember-luna2-rep) | 5, 100, 92, 123 | 5, 120, 98, 171 | 5, 122, 86, 155 |
| ember + luna (g9-*) | 4, 79, 61, 121 | 4, 114, 103, 130 | 4, 100, 85, 115 |
| haiku + 2x luna (g7-*) | 4, 220, 159, 305 | 4, 238, 230, 285 | 4, 226, 163, 297 |
| sonnet + 2x luna (j1-*, b4-sonnet-luna2) | 6, 259, 196, 283 | 6, 302, 208, 416 | 6, 269, 184, 440 |

Reading: the 116 s EL2 planning value is a 3-package mean; the designSpec median (100 s) and single runs (86-98 s) sit near or below the 97.1 s floor the probe computed for F3/F4/F7. Run-to-run spread inside one package (e.g. AL 98-171 s) is larger than any design's added time, so a per-run cap check against the historical number cannot be the test; per-package medians over an arm can.

#### Questions beyond the 8 HIGH items

- INV-006 may change the slate. If F6 cannot be stated as a distinct mechanism from F3, the probe names F2 (mid-run method relay, V5-D2 / V2-D3, the only I6 trigger) as the replacement. Decide: keep F6 under the probe's distinctness definition, or replace it.
- INV-005: accept the within-arm challenge-form vs finding-form contrast in F7, or say SEED:47 is answered descriptively only.
- State your final slate and the remaining disagreements.
</content>
</invoke>

### Variant 1 Final Position (opus:architect)

### Round 3 final arguments: V1 (opus, architect lens)

Citations: `V<n>:<line>` = `variant-<n>-original.md`; `R2-V<n>:<line>` = `round2-V<n>.md`; `INV-0nn` = `../invariant-probe.md`; `RR:48` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh:48`. No Round 3 statement existed when I wrote this one. Every number below was recomputed.

#### Final position

V4 stays the base. The five-family slate also stands: F1, F4, F3, F6, F7. The probe is right on all eight HIGH items, and three of my Round 2 claims fail under it:

- "worst 150.0 s" was a planned-path figure;
- "A5 vs A4 isolates challenge vs findings" was false;
- F1's n used the mean turn.

I accept five resolutions as written. I modify three where the probe's own text cannot work:

- **INV-001.** Its `PANEL_FINISH_AT` keeps a 1.20 B term. At the k = 2 that INV-008 computes, that term makes the signal fire on the planned path.
- **INV-003.** Partial salvage is impossible under today's `--output-format json`.
- **INV-005.** The finding form as written breaks the agreed no-free-text rule (X-007).

F6 stays. It is distinct from F3 under a stated criterion, and under that criterion the replacement F2 would fail against F7. Only F1's bound is enforced by a process kill. Slots 2-5 stay within 1.35 B at p90 by construction, and the SLO budget audits them.

#### HIGH invariant resolutions

| INV | Verdict | Exact rule for the merged spec |
|---|---|---|
| INV-001 | MODIFY | For each mid-run design (F3, F4, F6, F7) the spec states three numbers: (1) the planned end, B_f + hooks + 2k x turn; (2) the finish-signal bound, PANEL_FINISH_AT + turn_p90 + T_report_p90 = T0 + 1.35 B_f; (3) the enforced ceiling, a hang guard at T0 + 1.5 B_A1 whose firing counts as `SLO_BREACH`. **`PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90`.** The 1.20 B term is dropped. Spike 4 measures turn_p90 and T_report_p90 (the duration of the last turn) per model: luna for EL2, sonnet for SL2. The k of INV-008 guarantees planned end <= PANEL_FINISH_AT, so the signal never fires on the planned path. REQ-S3 measures the act rate on "finish now". The spec says plainly that for slots 2-5 the +35% cap is audited by the SLO budget (R-24), not enforced. "Worst 150.0 s" and "worst 330 s" are struck as cap guarantees. **Why modify:** with the probe's min(1.20 B, ...), INV-008's k = 2 at B = 116 gives a planned end of 116 + 2 + 25.6 = 143.6 s, past 1.20 x 116 = 139.2 s. The probe's two required rules contradict each other at its own planning values. Planning values for the new rule: PANEL_FINISH_AT = 156.6 - 12.8 = 143.8 s; bound 156.6 s (+35.0%); hang guard 174 s (+50%); for SL2, 1.5 x 273.7 = 410.6 s. |
| INV-002 | ACCEPT | One wall-clock deadline, T0 + 1.30 B_A1, covers every process that can write phase-2 lines: the resume or fresh fallback, the challenges and any H2 re-ask. A re-ask that cannot start with one start plus one turn left before the deadline is skipped; invalid phase-2 lines are dropped and phase 1 stands. In A1 and in every mid-run arm the H2 re-ask is logged as `reask_s`, and the cap check uses measured elapsed time that includes it. The words "compliance-free hard bound" appear only with this rule, worded as a **phase-2** bound (panel elapsed = max(T1, deadline), INV-022). |
| INV-003 | MODIFY | Before each launch attempt the harness computes `box = min(35, T0 + 1.30 B_f - t_launch)` and `n = max(0, min(cap, floor((box - start_cost) / (2 x turn_p90))))`. start_cost is 6 s for a resume and 16 s for the fresh fallback. A failed resume therefore re-renders the digest with a new n. If n = 0, no launch happens and phase 1 stands. Phase-2 and re-ask sessions run with `--output-format stream-json --verbose`, written to file as they stream. The brief asks for one complete findings line after each challenge. On timeout the combiner keeps every complete, parser-valid P2 line already streamed and drops the rest (`phase2_timeout`, `p2_lines_salvaged`). Spike S2 checks on luna that text streams before exit. The spec states two consequences: at planning B, luna B gets n = 1 whenever turn_p90 > 7.2 s (28.8/14.4 = 2.0); and the fallback for luna B gets n = floor((34.8 - 2 - 16)/12.8) = 1, not 0, if the resume failure is detected within 2 s. **Why modify:** today's command uses `--output-format json` (RR:48), which writes one result object at exit, so a killed process leaves no line to salvage. The probe also left "margin" undefined; per-line salvage makes margin = 0 safe. |
| INV-004 | ACCEPT | The CONVERGENCE Jaccard is computed on `origin:"own"` lines only: phase-1 or pre-delivery findings, excluding P2-F and peer-tagged lines. In mid-run arms the peer tag is applied mechanically, as in the INV-012 line below. Phase-2 independence is judged by ECHO on real-anchor slots. Ember's qualifying F1 anchors are hash-split disjointly between the two lunas. V2's "alarm in at most 2 of 12 runs" guard applies to this own-line Jaccard. |
| INV-005 | MODIFY | Strike the claim that A5 vs A4 isolates "challenge vs shared findings". A5 vs A4 compares two whole designs that differ in sender session, content source, move type and target issues. SEED:47 is answered **within F7**: <br>(1) For every card it posts, ember also records the `category` and `severity` enum values it would give. This is a scoped R-06 exception for F7 cards; `claim` and every other free-text field stay forbidden. <br>(2) The harness renders each card in one of two forms. **Challenge form:** anchor plus a required finite check. **Finding form:** anchor plus ember's category and severity. <br>(3) Card-to-luna assignment is round-robin over a seeded order, and forms alternate in that order. Each luna gets at most 2 cards and at most one of each form, so each luna serves as its own control (this also closes INV-023 for F7). <br>(4) Logged per slot: form, conversion (the receiver's line overlaps the card anchor by at least 12 characters), judge-credited conversion and uncredited conversion. <br>(5) The secondary analysis is pre-registered: conversion by form, two-proportion test. At 12 runs x 3 packages x 4 cards there are at most 144 cards, about 72 per form. <br>**Why modify:** "anchor plus ember's own claim" puts free text in a message, which X-007 (agreed 5/5) and R-06 (V4:702) forbid. It would also make ECHO the dominant failure mode in half the cards. |
| INV-006 | ACCEPT | **Distinctness criterion, stated once:** each slot is a triple (content source, content form, delivery point). Two slots are distinct when they differ in at least 2 of the 3. Sources are harness-from-telemetry, harness-from-finished-findings, dedicated helper session, and reviewing peer. <br>F1 = (finished findings, peer anchor + move, between phases). <br>F3 = (telemetry, move name only, mid-run). <br>F4 = (helper session, repo facts, mid-run). <br>F6 = (finished findings, uncovered-Task requests, mid-run). <br>F7 = (reviewing peer, flagged sentence + finite check, mid-run). <br>Every pair differs in at least 2: F1/F6 in form and delivery; F3/F6 in source and form; F4/F7 in source and form. The evicted F5 (helper session, facts, mid-run) differs from F4 in 0, and F2 (reviewing peer, anchor/ref + move, mid-run) differs from F7 in 1. So F2 is not a valid replacement. **F6 is kept**, with its coverage source restored to V4-5's watcher (V4:543): (Task, category) from the findings blocks of peers that have finished, rendered as requests for uncovered Tasks, never from telemetry. I6 keeps its route through F1's `contradiction` -> M7 row (R2-V2:13). |
| INV-007 | ACCEPT | The classifier section lists the observable tool-call signature of each catalogue move. M3, M5, M6, M8, M9 and M10 have none, are marked unobservable, and are never described as "not done by any panel member". Luna's F3 injections are labelled a timed static prompt and booked to the prompting share (A2 comparator). F3's collaboration content is restated as ember's search-move gaps plus the "source.md never opened" check, and F3's C is re-derived from ember rows only. F6 draws reading-move requests only from findings-derived coverage (INV-006). |
| INV-008 | ACCEPT | F3, F4 and F7 get a per-package count of facts, cards or injections per luna: `k = max(0, min(2, floor((0.35 B_A1(pkg) - hooks - turn_p90 - T_report_p90) / (2 x turn_p90))))`, with hooks = 2 s. F6 uses the same rule with SL2's B and sonnet's turns. With the INV-001 rule this equals floor((PANEL_FINISH_AT - T0 - B - hooks)/(2 x turn_p90)), so planned end <= PANEL_FINISH_AT holds by construction. Worked values: B = 116 with 6.4/6.4 gives k = floor(25.8/12.8) = 2 (end 143.6 s <= 143.8 s); with T_report_p90 = 11.0, k = floor(21.2/12.8) = 1 (end 130.8 s); B = 90 gives k = floor(16.7/12.8) = 1. Spike 4 publishes per-package B_A1, turn_p90, T_report_p90, PANEL_FINISH_AT and k before any arm runs. Every "+x%" and every gain row is labelled valid only at B = 116 and k = 2. |

#### MEDIUM invariants worth closing

- **INV-009:** R-05's allowed differences become R-01, R-03 and the removal of `--no-session-persistence` (RR:48), because every arm, A1 included, re-asks through `--resume`.
- **INV-010:** the phase-1 H2 re-ask finishes before the seal. `<rid>.p1.md` is the post-re-ask phase-1 report; it is hashed at that point and used for sealed-report judging.
- **INV-011:** cleanup deletes only the session ids recorded in that run's `collab.json`, after every concurrent run on that sandbox ends, and never the directory. `git status` is checked after the last such run.
- **INV-012:** in mid-run arms the harness tags a line `peer` if its anchor overlaps a delivered anchor by at least 12 characters, or if a delivered locator is in its refs, whatever the model wrote. Alarms built on "own sealed findings" are dropped, and the timestamp test is kept as an integrity log only.
- **INV-014:** findings from gap-card slots are booked to the prompting share. F1 C = 0.06-0.63 /14, and the gap route (0-0.10) is reported in that share's column.
- **INV-018:** a `flag_finding_overlap` alarm stops and reports the arm; it never changes the treatment partway through an arm.

#### Remaining disagreements

1. **INV-001, the 1.20 B term.** V5's formula (R2-V5:77) and the probe keep min(1.20 B, ...). I would drop it. That term was my own unmeasured margin (V1:138). With it, either k = 1 at planning B, which halves F3/F4/F7's delivered content, or the signal truncates luna's own isolated work on the planned path (INV-008's "typical path" failure). The measured term already lands the p90 run at exactly 1.35 B, and R-24 absorbs the tail (1 package in 12). I can converge on the probe text only if INV-008's k is computed against the same PANEL_FINISH_AT, which gives k = 1 at planning B.
2. **INV-003, output format.** Without stream-json the salvage clause is unimplementable (RR:48). This is a fact, not a preference.
3. **INV-005, the finding form.** "Ember's own claim" conflicts with X-007. Enum-only verdicts keep the contrast without free text. If the panel rejects the R-06 exception, the fallback is the probe's alternative: SEED:47 is answered descriptively only.

#### Final concessions

- R2-V1:43 ("same sender, same receivers") was false. The F4 sender is a fresh sweeper session posting search facts; the F7 sender is the reviewing ember flagging sentences (INV-005).
- R2-V1:75's "worst 150.0 s" and R2-V1:170's "worst = expected" for F3 are planned-path figures. V5's finish-signal bound (R2-V5:64-73) is the right structure.
- R2-V1:61's "hard bound 150.8 s for any T1" holds only for the phase-2 end, and only once the re-ask sits inside the deadline (INV-002, INV-022).
- R2-V1:52's n used the mean turn and silently zeroed the fallback (INV-003).
- R2-V1:102's "uncovered cells from V2-D4" pointed F6 at telemetry. The findings-derived source is correct (INV-006, INV-007).
- The F1 gap-card route is harness extraction by V4:523's own test; F1 C drops to 0.06-0.63 (INV-014).
- F3 after INV-007: lunas leave almost no search signatures, so ember's "no panel member has done this" mostly reflects ember's own history. F3's collaboration share may be near 0, and its A6 vs A2 result should be read as "telemetry-timed kit vs static kit".

#### Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 `contradiction` -> M7 (I6 route); gap-card decoy p = 1/3, kind withheld, findings booked to the prompting share; ember anchors hash-split between lunas; INV-003 n per launch attempt with stream-json salvage; one phase-2 deadline T0 + 1.30 B_A1 incl. re-ask; V4 combiner; V2 sealed-report judging on the post-re-ask `p1.md`; V5-D5 HL2 shadow variant | Only bound enforced by a kill (phase-2 end <= 150.8 s, +30.0%); planned luna B 147.6 s (+27.2%); C 0.06-0.63 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint locators (round-robin); V1-R2 harvest incl. sweeper output; V2-D5 witness kind; V5-D3 first-hand rule + 10% stop; k per INV-008; fail-closed hook snapshot; mechanical peer tag; sweeper timeout; hang guard 1.5 B_A1 | Only cheap I7/T1 path, in ember's idle time; planned 143.6 s at k = 2, bound 1.35 B at p90, ceiling 174 s = breach |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move cells limited to observable signatures; luna injections labelled static (A2 share); V1-R1 hash order; V5-D4 skip rule; V3 leak check; k per INV-008 | No model authors anything; tests whether telemetry timing beats the static kit; same three-number time block |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Coverage from finished peers' findings (Task, category), rendered as uncovered-Task requests; no counts, no telemetry, no SendMessage; surface filter; V1-R5 brief line; k with sonnet's turns | Claude receiver, harness author; planned 331.7 s at k = 2 (273.7 + 2 + 56; +21.2%); bound 369.5 s at p90; ceiling 410.6 s |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Enum-tagged cards rendered in challenge or finding form, alternating; round-robin split, at most 2 per luna; hook snapshot; V5 C-3; k per INV-008; `flag_finding_overlap` stops the arm | Only slot that answers SEED:47, within one arm; planned 143.6 s at k = 2; C 0.08-0.77 |

Proposed base document: V4

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Kill switch, baked board path, timing and baseline tables |
| S-003 | V2 | The gate funnel makes the H/C split structural |
| S-004 | V5 | Net collaboration, static-kit row, tokens per added issue (plus input tokens for resume) |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Itemised unverified list tied to each number |
| C-001 | V1 | Searcher/reader complementarity predicts a gain the kit cannot copy |
| C-002 | V5 | T2a/T2b decides which routes reach B1/B2/I4 |
| C-003 | V1 | Truncate, validate, re-ask; grading constant |
| C-004 | V4 | Best-style column used by routing |
| C-005 | V4 | 12-200-character anchors plus V2's rules |
| C-006 | V4 | Process exit for phases; fail-closed snapshot for mid-run |
| C-007 | V4 | Relative, ground-truth-free alarm, now on own lines (INV-004) |
| C-008 | V4 | Per-issue chains |
| C-009 | V5 | Three shares, C and H never summed |
| C-010 | V2 | Fresh A0, catalogue arm, A6 |
| C-011 | V2 | One reach endpoint, final-look Fisher, +4 over A2 |
| C-012 | V1 | Every design on a seed baseline |
| C-013 | V1 | Panel finish signal, now measured-reservation form plus R-24 audit |
| X-001 | V5 | Bottom-up H 0.03-0.34 |
| X-002 | V1 | 0 on /14; control correction only |
| X-003 | V1 | GT6 = I1 |
| X-004 | V5 | HL2 shadow schedule +0% |
| X-005 | V1 | The slowest luna sets B |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text, which is why INV-005 uses enums |
| X-008 | V1 | Grading and judge held constant |
| X-009 | V1 | Truncate, validate, re-ask |
| X-010 | V5 | The kit may win; A2 is the comparator |
| X-011 | V5 | Anchor routes to B1/B2/I4 need the gap card |
| X-012 | V1 | Both scales and the label mapping defined most precisely |
| X-013 | V2 | 4/6 vs 0/6 = 0.030 |
| A-001 | V1 | REQ-S3 tests the act, now also on "finish now" |
| A-002 | V5 | Prices the kit's time |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | Per-package values, not /3 |
| A-006 | V2 | Decoys via the gap card |
| A-007 | V4 | Spike, fallback, `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | c capped against measured reach |

### Variant 2 Final Position (opus:analyzer)

### Round 3 final arguments: V2 (opus, analyzer lens)

Citations: `V<n>:<line>` = `variant-<n>-original.md`; `R2-V<n>:<line>` = `round2-V<n>.md`; `R3-V1` = `round3-V1.md`; `INV-0nn` = `../invariant-probe.md`; `AG` = `round3-agenda.md` (orchestrator's per-package table); `RR:<line>` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`. I read R3-V1 before writing. Every number below was recomputed this round.

#### Final position

V4 stays the base, and the slate stays F1, F4, F3, F6, F7. The probe is right on all eight HIGH items. My own Round 2 figures "worst 150.0 s", "worst = expected" and "A5 vs A4 answers SEED:47" do not survive it. I adopt R3-V1's MODIFY texts for INV-001 and INV-003 unchanged, because both rest on checkable facts: the probe's two rules conflict at its own planning values, and RR:48 shows `--output-format json`. I accept INV-002, -004, -006, -007 and -008.

I cannot adopt R3-V1's INV-005 text. Its card-assignment clause contradicts itself. As written, each luna receives two cards of the same form, so luna and form are fully confounded. My replacement keeps V1's enum-only finding form and fixes only the dealing rule.

One analyzer finding changes what the spec should call "expected". k = 2 needs luna's final-report turn at p90 to be no longer than 6.6 s. The gain rows should therefore be reported at k = 1 as the central case.

#### HIGH invariant resolutions

| INV | Verdict | Exact rule for the merged spec |
|---|---|---|
| INV-001 | MODIFY | **MODIFY = R3-V1.** Evidence, recomputed: the probe's `min(1.20 B, 1.35 B - turn_p90 - T_report_p90)` at B = 116 with 6.4/6.4 gives min(139.2, 143.8) = 139.2 s. Its own INV-008 k = 2 plans an end of 116 + 2 + 25.6 = 143.6 s > 139.2, so the probe's "B + W <= PANEL_FINISH_AT" fails under its own rules. The 1.20 B term binds only when T_report_p90 < 0.15 B - turn_p90 = 17.4 - 6.4 = 11.0 s. Dropping it therefore changes nothing in the regime the probe itself calls likely ("output-heavy"). |
| INV-002 | ACCEPT | Probe text, worded as in R3-V1: one wall-clock deadline T0 + 1.30 B_A1 covers resume or fresh fallback, challenges and any H2 re-ask. A re-ask that cannot fit one start plus one turn is skipped, and phase 1 stands. `reask_s` is logged in A1 and every mid-run arm, and the cap check uses measured elapsed time including it. "Compliance-free hard bound" is used only for the **phase-2 end**; panel elapsed = max(T1, deadline) (INV-022). |
| INV-003 | MODIFY | **MODIFY = R3-V1.** Evidence: RR:48 launches with `--output-format json --no-session-persistence`, and RR:50 extracts the single `type=="result"` object, which exists only at process exit. A killed phase 2 therefore leaves nothing to salvage unless it streams. Feasibility: the same `select(.type=="result")` filter works on stream-json read with `jq -s`. Recomputed: luna B n = floor(28.8 / (2 x 7.2)) = 2.0, so n = 1 for any turn_p90 > 7.2 s. Fallback detected at 2 s: box = 150.8 - 118 = 32.8, n = floor(16.8/12.8) = 1, end 118 + 16 + 12.8 = 146.8 s <= 150.8 s. |
| INV-004 | ACCEPT | Probe text plus R3-V1's mechanical peer tag. The CONVERGENCE Jaccard uses only `origin:"own"` lines (phase-1 or pre-delivery, excluding P2-F and peer-tagged lines). Phase-2 independence is judged by ECHO on real-anchor slots. Ember's qualifying F1 anchors go to the two lunas disjointly, using the balanced deal in INV-023 below rather than a raw hash. V2's "alarm in at most 2 of 12 runs" guard applies to own lines only. In F1, own lines are sealed by process exit, so this alarm should fire at A1's rate; a higher rate is an integrity failure, not a design effect. |
| INV-005 | MODIFY | Strike "A5 vs A4 isolates challenge vs shared findings". A5 vs A4 compares two whole designs that differ in sender session, content source, move type and target issues. SEED:47 is answered **within F7**: <br>(1) For every card it posts, ember records the `category` and `severity` enum values it would give. This is a scoped R-06 exception for F7 cards; `claim` and all other free-text fields stay forbidden. <br>(2) Each card is rendered in one of two forms. **Challenge form:** anchor plus a required finite check. **Finding form:** anchor plus ember's category and severity. <br>(3) **Dealing, online in posting order.** Card i is the i-th card ember posts (i = 0, 1, ...), and ember posts at most 2k cards (INV-008). Card i goes to luna (i + r) mod 2. Its form is challenge when (i + floor(i/2) + c) is even and finding otherwise. r and c are seeded 0/1 coins per run, logged. Result: at k = 2 each luna gets exactly one card of each form, and at k = 1 the two lunas get opposite forms. <br>(4) Logged per slot: form, conversion (the receiver's line overlaps the card anchor by at least 12 characters), judge-credited conversion and uncredited conversion. <br>(5) Pre-registered secondary analysis: conversion by form, two-proportion test, with the run-paired difference also reported. At most 12 x 3 x 4 = 144 cards (about 72 per form); fewer where k = 1. <br>**Why not R3-V1's text:** "round-robin over a seeded order, and forms alternate in that order" deals A, B, A, B and forms C, F, C, F, so luna A gets C, C and luna B gets F, F. That contradicts V1's own "at most one of each form", and luna becomes confounded with form. A pre-sorted order also cannot exist, because cards arrive one at a time mid-run. |
| INV-006 | ACCEPT | R3-V1's criterion, unchanged. Each slot is a triple (content source, content form, delivery point), and two slots are distinct when they differ in at least 2 of the 3. F6's source is the findings blocks of peers that have finished: (Task, category) at exit, rendered as requests for Tasks with no peer finding, ranked by the lunas' declared not-checked scope. Telemetry is never used. **Applying the criterion requires one statement R3-V1 leaves implicit.** F3 still carries "V2-D4 Task x move cells" (R3-V1 slate). If its injections name a Task, F3 and F6 share the form "move + Task" and differ only in source, which is 1 of 3 and fails. So F3's injection names a move only, plus a Task only when the triggering tool call's path names one. After INV-007, telemetry cannot attribute most moves to a Task anyway. F2 differs from F7 in at most 1 (both are a reviewing peer sending anchor + move mid-run, V4:466), so it is no replacement. |
| INV-007 | ACCEPT | = R3-V1. Note that ember's F3 set is M1, M2, M7, M4 (V4:201). The probe lists signatures for M1 and M7 only, so M2 and M4 must each get a listed signature or be marked unobservable. |
| INV-008 | ACCEPT | = R3-V1 (k clamped at 0; F6 uses SL2's B and sonnet's turns; Spike 4 publishes B_A1, turn_p90, T_report_p90, PANEL_FINISH_AT and k per package before any arm). **Required statement of the k thresholds**, from the same formula with hooks = 2 and turn = 6.4: <br>k = 2 needs T_report_p90 <= 0.35 B - 2 - 5 x 6.4. That is 6.6 s at B = 116, 8.0 s at AL's 120 and 8.7 s at DE's 122. At DS's 100 the bound is 1.0 s, so k = 2 is impossible there. <br>k >= 1 needs T_report_p90 <= 0.35 B - 2 - 3 x 6.4. That is 19.4 s at 116 and 13.8 s at DS's 100. <br>For F6 (B = 273.7, turn 14): k = 2 needs <= 23.8 s and k >= 1 needs <= 51.8 s. <br>The package medians are from AG (historical, no H); A1 carries H and may be slower, which raises k. Gain and time rows are reported at k = 1 (central) and k = 2 (optimistic). A package with k = 0 counts as isolated for that design, and that dilution is reported. |

#### MEDIUM invariants worth closing

- INV-009, -010, -011, -012, -014, -018: adopt R3-V1's six lines. On INV-018 I withdraw my own mid-arm decoy (R2-V2:38).
- INV-023: every disjoint split (F1 anchors, F4 locators, F7 cards) uses the online balanced deal of INV-005 (3). Recipient = (i + r) mod 2; no hash.
- INV-019: the decision table is stated against the observed A1 reach. A1 0/12 needs X >= 4/12 (p = 0.047); A1 1/12 needs 6/12 (p = 11,880/346,104 = 0.034, while 5/12 gives 10,428/134,596 = 0.077); A1 2/12 needs 7/12 (p = 58,432/1,307,504 = 0.045).
- INV-020: adopt V5's stage-2 screen (R2-V5:126-129): hard credits per run, a one-sided permutation test at p < 0.05, and a margin over A2-SL2 of at least 1/3 of runs.
- INV-021: F6's 0.26-1.06 is withdrawn as a carried figure and re-derived on SL2. F6 runs only if Spike 4 gives sonnet a T_report_p90 of at most 51.8 s (k >= 1).
- New counterfactual, needed by INV-001 and -008: log `finish_would_fire` in A1 and A2 (luna still running at PANEL_FINISH_AT). Spread inside a package (AL 98-171 s, AG) means slow runs get the signal in design arms but not in A1. The truncation rate must be compared, not assumed equal.

#### Remaining disagreements

1. **INV-005 dealing rule.** This is a fact about R3-V1's text, not a preference. Dealing A, B, A, B against forms C, F, C, F yields C, C and F, F per luna. My (3) is the minimal fix, and every other clause is R3-V1's. If the panel prefers V1's wording, it must at least replace "forms alternate in that order" with an alternation per luna.
2. **What "expected" means for F3, F4 and F7.** R3-V1 labels every row "valid only at B = 116 and k = 2". By the INV-008 thresholds, k = 2 requires luna's output-heavy final turn at p90 to be no longer than the 6.6 s mean-turn neighbourhood, and it is impossible on designSpec. That package holds F7's B5/I1/I4 targets (INV-017). Calling k = 2 "planning" overstates every mid-run gain. I ask that k = 1 be the central row. Planned luna B is then 116 + 2 + 12.8 = 130.8 s (+12.8%).
3. **F3's form** (INV-006 row). Without the move-only rule, F3 and F6 fail V1's own criterion.

#### Final concessions

- R2-V2:44 and :86 ("worst 150.0 s, +29.3%") and R2-V2:223 ("worst = expected" for F3) are planned-path figures. V5's finish-signal structure is right (INV-001).
- R2-V2:125 ("A5 vs A4 answers SEED:47") was false: sender, content, move type and targets all differ (INV-005).
- R2-V2:58-61 used the mean turn for n, and my adoption of V1's box missed that the fallback is always killed (INV-003).
- R2-V2:108 ("drawn only from V2-D4's uncovered cells") pointed F6 at telemetry. The findings-derived source is correct (INV-006, -007).
- R2-V2:38: adding a decoy partway through an arm pools two treatments (INV-018). Stop and report instead.
- R2-V2:148: applied to all lines, my independence guard would fail F1 by construction (INV-004).
- R2-V2:176 found the 97.1 s threshold but did not turn it into a count rule. INV-008 does.
- R2-V2:221's F1 C 0.23-0.94 is superseded by 0.06-0.63, with the gap-card route booked to the prompting share (INV-014).
- R3-V1 is right on the 1.20 B term and on stream-json. I had no counter to either.

#### Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 `contradiction` -> M7 (I6 route); gap-card decoy p = 1/3, kind withheld, booked to the prompting share; balanced disjoint anchor deal; INV-003 n per launch attempt with stream-json salvage; one phase-2 deadline T0 + 1.30 B_A1 incl. re-ask; V4 combiner; sealed-report judging on the post-re-ask `p1.md`; V5-D5 HL2 shadow variant | Only bound enforced by a kill: phase-2 end <= 150.8 s (+30.0%). Planned luna B 147.6 s (+27.2%), or n = 1 if turn_p90 > 7.2 s. C 0.06-0.63 /14 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 locators (balanced deal); V1-R2 harvest incl. sweeper output; V2-D5 witness kind; V5-D3 first-hand rule + 10% stop; k per INV-008; fail-closed snapshot; mechanical peer tag; sweeper timeout; hang guard 1.5 B_A1 | Only cheap I7/T1 path, in ember's idle time. Planned 130.8 s (k = 1) / 143.6 s (k = 2). Signal bound T0 + 1.35 B_f = 156.6 s; 174 s = breach |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | Observable signatures only (INV-007); move-only injections (INV-006); luna injections booked as static (A2 share); V1-R1 hash order; V5-D4 skip rule; V3 leak check; k per INV-008 | No model authors anything. A6 vs A2 = telemetry-timed vs static kit; C re-derived from ember rows, may be near 0. Same three-number time block as F4 |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Finished peers' (Task, category), requests for Tasks with no peer finding, ranked by declared not-checked scope; no counts, telemetry or SendMessage; surface filter; V1-R5 line; k with sonnet's turns | Claude receiver, harness author. Planned 303.7 s (+11.0%, k = 1) / 331.7 s (+21.2%, k = 2); bound 369.5 s; ceiling 410.6 s. Runs only if sonnet's T_report_p90 <= 51.8 s; gain re-derived (INV-021) |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Enum-tagged cards in challenge or finding form, dealt online and balanced (INV-005 (3)); ember cap 2k; hook snapshot; V5 C-3; `flag_finding_overlap` stops the arm | Only slot that answers SEED:47, within one arm. Planned 130.8 / 143.6 s; C 0.08-0.77 at k = 2, lower at k = 1, and designSpec rows depend on k >= 1 |

Proposed base document: V4

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Kill switch, baked board path, timing and baseline tables |
| S-003 | V2 | The gate funnel makes the H/C split structural |
| S-004 | V5 | Net collaboration, static-kit row, tokens per added issue incl. resumed input tokens |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Itemised unverified list tied to each number (now incl. T_report_p90) |
| C-001 | V1 | Searcher/reader complementarity predicts a gain the kit cannot copy |
| C-002 | V5 | T2a/T2b decides which routes reach B1/B2/I4 |
| C-003 | V1 | Truncate, validate, re-ask; grading constant |
| C-004 | V4 | Best-style column used by routing |
| C-005 | V4 | 12-200-character anchors plus V2's rules |
| C-006 | V4 | Process exit for phases; fail-closed snapshot for mid-run |
| C-007 | V4 | Relative, ground-truth-free alarm, on own lines (INV-004) |
| C-008 | V4 | Per-issue chains |
| C-009 | V5 | Three shares, C and H never summed |
| C-010 | V2 | Fresh A0, catalogue arm, A6 |
| C-011 | V2 | One reach endpoint, final-look Fisher, +4 over A2, conditional on A1 reach (INV-019) |
| C-012 | V1 | Every design on a seed baseline |
| C-013 | V1 | Panel finish signal, measured-reservation form plus R-24 audit |
| X-001 | V5 | Bottom-up H 0.03-0.34 |
| X-002 | V1 | 0 on /14; control correction only |
| X-003 | V1 | GT6 = I1 |
| X-004 | V5 | HL2 shadow schedule +0% |
| X-005 | V1 | The slowest luna sets B |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text, hence enum-only finding form |
| X-008 | V1 | Grading and judge held constant |
| X-009 | V1 | Truncate, validate, re-ask |
| X-010 | V5 | The kit may win; A2 is the comparator |
| X-011 | V5 | Anchor routes to B1/B2/I4 need the gap card |
| X-012 | V1 | Both scales and the label mapping defined most precisely |
| X-013 | V2 | 4/6 vs 0/6 = 15/495 = 0.030 |
| A-001 | V1 | REQ-S3 tests the act, also on "finish now" |
| A-002 | V5 | Prices the kit's time |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | Per-package values, not /3; AG confirms package spread |
| A-006 | V2 | Decoys via the gap card |
| A-007 | V4 | Spike, fallback, `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | c capped against measured reach |

### Variant 3 Final Position (haiku:backend)

### Round 3 final arguments: V3 (haiku, backend lens)

Citations: `R3-V1:<line>` / `R3-V2:<line>` = those Round 3 files; `R2-V3:<line>` = `round2-V3.md`; `IP:<line>` = `../invariant-probe.md`; `AG:<line>` = `round3-agenda.md`; `T:<line>` = `round2-tally.md`. Arithmetic below is recomputed; timing inputs remain illustrative until measured.

#### Final position

Keep V4 and F1, F4, F3, F6, F7. V1 best separates planned time from cooperative and enforced limits; V2 best repairs the receiver/form confounding. Adopt V1's MODIFY texts for INV-001/-003 and V2's for INV-005; ACCEPT the rest. No new MODIFY text. Support k = 1 as conservative central planning, not measured expectation, and move-only F3 messages. My original gains remain withdrawn. A failed second phase must not destroy a valid first phase.

#### HIGH invariant resolutions

| INV | Verdict | Exact rule for the merged spec |
|---|---|---|
| INV-001 | MODIFY | **MODIFY = R3-V1.** Adopt its full rule (R3-V1:25): planned end; cooperative finish bound; enforced hang ceiling, whose firing is `SLO_BREACH`. `PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90`. At B = 116 and turn/report = 6.4, the probe signals at 139.2 s although k = 2 plans 143.6 s; V1 instead gives 156.6 - 12.8 = 143.8 s. This removes the contradiction. The 174 s hang ceiling is not a +35% guarantee; the finish bound remains compliance-dependent. |
| INV-002 | ACCEPT | Adopt IP:55, R3-V1:26. One phase-2 deadline covers resume, failed starts, fallback, challenges and repair. Skip a re-ask without room for startup plus one turn; drop invalid lines and preserve phase 1. Log `reask_s` in A1 and mid-run arms and include it in elapsed. Only phase-2 end is hard-bounded; killing phase 2 cannot repair an already-late phase 1. |
| INV-003 | MODIFY | **MODIFY = R3-V1.** Adopt its complete per-attempt clamped n, streaming, parser-valid partial salvage and S2 check (R3-V1:27). At B = 116, deadline = 150.8 and launch at 116 leaves 34.8 s: resume fits floor((34.8 - 6)/12.8) = 2; an 8 s turn fits floor(28.8/16) = 1. Failure detected after 2 s leaves 32.8 s; fallback fits floor((32.8 - 16)/12.8) = 1. Preserve P1 verbatim; truncated stream records are not findings. These inputs are feasibility assumptions, not measured startup guarantees. |
| INV-004 | ACCEPT | Adopt IP:59 with R3-V2:20, :29's balanced disjoint deal. Jaccard uses own P1/pre-delivery lines only, excluding P2-F and mechanical peer tags. ECHO judges real-anchor slots separately. Recipient `(i + r) mod 2` prevents an unbalanced hash split. Apply the alarm-frequency guard only to own-line Jaccard. A transcript timestamp proves ordering, not independent findings. |
| INV-005 | MODIFY | **MODIFY = R3-V2.** Adopt its entire within-F7 contrast, enum-only finding form, online deal, logs and secondary analysis (R3-V2:21). Steelman: V1 correctly protects the no-free-text boundary. Defect: its alternating recipients/forms give A challenge/challenge and B finding/finding. Recompute V2 at r = c = 0: i = 0,1,2,3 gives A,B,A,B and challenge,finding,finding,challenge. Each receiver gets both forms when all cards arrive; a two-card prefix gives opposite forms. Seeded coins preserve this balance. Log late/missing slots separately. A5/A4 remains a whole-design comparison, not this contrast. |
| INV-006 | ACCEPT | Adopt IP:68 and R3-V1:30's source/form/delivery criterion. F6 uses finished peers' (Task, category) findings, requests Tasks without peer findings, and ranks by declared not-checked scope; no telemetry or covered counts. Support V2's move-only F3 direction (R3-V2:22, :39): ordinary messages name a move, not an uncovered-Task request. Path-attributed Task metadata stays audit metadata; the fixed source-open check is the INV-007 exception. F3/F6 differ in source and form; F1/F6 in form and delivery. Keep F6, not F2. |
| INV-007 | ACCEPT | Adopt IP:70, R3-V2:23. Publish signatures for every move. M3/M5/M6/M8/M9/M10 are unobservable; M2/M4 need demonstrated signatures or that label too. Missing telemetry never proves a reading move omitted. Luna's timed reading kit belongs to prompting/A2. Re-derive F3 C from observable ember search gaps and the explicit source-open check only. F6 uses findings-derived coverage, never the telemetry matrix. |
| INV-008 | ACCEPT | Adopt IP:72 with R3-V1:32's clamp: `k = max(0, min(2, floor((0.35 B - 2 - turn_p90 - T_report_p90)/(2 x turn_p90))))`. Freeze measured inputs per package; F6 uses sonnet's. With turn = 6.4, k = 2 requires report <= 0.35 B - 2 - 32: 6.6 s at B = 116, 1.0 s at historical DS B = 100 (AG:13). k >= 1 allows 19.4 s and 13.8 s respectively. Support k = 1 central, k = 2 optimistic, pending Spike 4; historical DS is not proof of impossibility after H. k = 0 means no treatment and reported dilution. Re-derive gains at actual k rather than simply halving them. |

#### MEDIUM invariants worth closing

- **INV-009/-010/-011:** adopt R3-V1:36-38. Persistence changes apply uniformly, including A1. Repair P1 before its immutable seal. Delete only run-owned sessions after concurrent users finish, never the shared directory.
- **INV-012:** adopt R3-V1:39. Mechanical peer tags replace model self-report. Drop alarms needing nonexistent mid-run sealed findings. My timestamp check is only an ordering log.
- **INV-013/-014:** empty real-anchor exposure makes ECHO not applicable, not zero. Gap cards need eligible unanchored regions and count as prompting. Re-derive F1 with I4 on the gap route (IP:23-24, :42).
- **INV-015/-016/-017:** log actual sweeper start, delivered slots, late drops and Task coverage. Zero counts are not clearance; credited count evidence requires first-hand checking. An early card cap does not establish exposure of later Tasks (IP:25-27).
- **INV-018:** stop/report the arm on the overlap alarm; never change treatment mid-arm (IP:28).
- **INV-019/-020/-021:** use observed A1 reach; adopt V2's stage-2 hard-credit screen and re-derive SL2 gains (R3-V2:30-32). Repairing measurement does not establish power.
- **INV-022/-023:** clamp n; skip zero-capacity launches; balance recipient dealing. Keep atomic writes and harness-recorded hashes (R2-V3:99-101); torn transport lines must never become delivered messages.

#### Remaining disagreements

1. **V1's INV-005 dealing clause:** support V2 exactly. The recomputed deal demonstrates receiver/form confounding, not a preference about wording.
2. **k = 2 as central:** support V2's k = 1 planning row. Neither is empirical expected performance; package-specific measurements supersede both.
3. **F3/F6 boundary:** support move-only F3, not Task-targeted telemetry requests. Finished findings justify keeping F6. Internal coverage bookkeeping alone is not a different mechanism.

#### Final concessions

- R2-V3:46, :85, :183 confused planned-path times with worst cases. Withdraw those guarantees.
- R2-V3:54-61 used mean-turn n and overstated the panel-wide bound; :81 discarded all P2 on timeout. Adopt the shared deadline and validated streaming salvage.
- Withdraw my mid-arm decoy (:50), A5/A4 form-comparison claim (:185), and unsupported Task-by-reading-move telemetry (:107, :115).
- My timestamp test proves no independence. Original gains and out-of-block collaboration remain withdrawn (R2-V3:7-20); F6's old timing/gains need re-derivation.
- No Round 2 consensus winner changes. My minority A-011 vote changes from V2 to V5, matching T:46: cap never-found issue gains against measured reach.

#### Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Balanced anchors; contradiction-to-M7; gaps booked to prompting; per-attempt n; shared deadline; streamed salvage; immutable repaired P1 | Exit-sealed first pass survives P2 failure. At B = 116, phase-2 deadline = 150.8 s, not a bound on late P1. |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | Disjoint locators; witness sweep kind; first-hand rule; atomic delivery; snapshot; k and late-drop logs | Search-to-reader mechanism. B = 116, turn = 6.4 gives plans 130.8 s at k = 1 and 143.6 s at k = 2. |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | Observable signatures; move-only payload; reading kit booked to A2; variable-field leak check; skip rule; k | Tests telemetry timing versus static kit; collaboration may be negligible. |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Finished findings only; uncovered-Task requests; no counts/telemetry/SendMessage; surface filter; sonnet k | Distinct source and form. B = 273.7, turn = 14 gives plans 303.7/331.7 s at k = 1/2, not enforced ceilings. |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | V2 enum-only forms and online deal; cap 2k; slot logs; snapshot; overlap stops arm | Within-F7 comparison without receiver confounding. Missing/late slots remain visible; timing as F4. |

Proposed base document: V4

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | Requirements plus operational checks |
| S-002 | V4 | Baked settings, kill switch, baselines |
| S-003 | V2 | Gate funnel separates exposure and survival |
| S-004 | V5 | Net gain against kit; resume input cost |
| S-005 | V4 | Unified IDs with verification status |
| S-006 | V5 | Explicit unverified assumptions |
| C-001 | V1 | Searcher/reader complementarity |
| C-002 | V5 | Criterion-level T2a/T2b exposure |
| C-003 | V1 | Validate and repair inside deadline |
| C-004 | V4 | Best-style routing |
| C-005 | V4 | Bounded located verbatim anchors |
| C-006 | V4 | Exit seal or fail-closed snapshot |
| C-007 | V4 | Relative alarm on own findings |
| C-008 | V4 | Per-issue chains |
| C-009 | V5 | Separate shares; C conditional on H |
| C-010 | V2 | Fresh controls and catalogue comparator |
| C-011 | V2 | Final-look decision against observed baseline |
| C-012 | V1 | Seed baseline per design |
| C-013 | V1 | Measured finish reservation, audited cap |
| X-001 | V5 | Bottom-up harness attribution |
| X-002 | V1 | Leak removal is control correction |
| X-003 | V1 | GT6 maps to I1 |
| X-004 | V5 | Shadow leaves haiku isolated |
| X-005 | V1 | Slowest reviewer sets elapsed |
| X-006 | V4 | One block; preserve P1, validate P2 |
| X-007 | V2 | No free-text claim; enum-only F7 |
| X-008 | V1 | Grader and judge held constant |
| X-009 | V1 | Truncate, validate, budget repair |
| X-010 | V5 | Static kit may win |
| X-011 | V5 | Missing criterion anchors block anchor route |
| X-012 | V1 | Separate target/control denominators |
| X-013 | V2 | Corrected Fisher comparison |
| A-001 | V1 | Verify action, not mere delivery |
| A-002 | V5 | Include kit time |
| A-003 | V2 | Random labels, sealed-report judging |
| A-004 | V4 | Harness/collaboration interaction |
| A-005 | V5 | Per-package medians |
| A-006 | V2 | Gap decoys with exposure accounting |
| A-007 | V4 | Spike, bounded fallback, failure logs |
| A-008 | V4 | Board-only helper writes |
| A-009 | V2 | Confirmation on new packages |
| A-010 | V1 | Explicit EL2 rationale |
| A-011 | V5 | Cap gains against measured reach |

### Variant 4 Final Position (opus:devops)

### Round 3 final arguments: V4 (opus, devops lens)

Citations: `V4:<line>` = `variant-4-original.md`; `R2-V4:<line>` = `round2-V4.md`; `R3-V<n>:<line>` = `round3-V<n>.md`; `INV-0nn` = `../invariant-probe.md`; `AG:<line>` = `round3-agenda.md`; `RR:<line>` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`. I read R3-V1, R3-V2 and R3-V3 before writing. Every number below was recomputed.

#### Final position

V4 stays the base, and the slate stays F1, F4, F3, F6, F7. The probe is right on all eight HIGH items. I add no new MODIFY text:

- INV-001 and INV-003: MODIFY = R3-V1.
- INV-005: MODIFY = R3-V2.
- The other five: ACCEPT.

I support **k = 1 as the central row** and **move-only F3 injections**.

As base author, I checked each adopted rule against V4's runbook: the spikes in R-27, the fields in R-23, the kill switch in R-05 and V4:139, and the SLO rule in R-24. All of them can be operated, but only with the corrections listed under MEDIUM below. Two of those corrections come from RR, and no statement in the debate has raised them yet:

- the retry loop (RR:61-64) re-runs a whole review, and no time bound counts that second attempt;
- A1 keeps `timeout 3000` (RR:48), while the design arms get a 1.5 B hang guard. That kills slow runs in the design arms only, so the comparison with A1 is not fair.

#### HIGH invariant resolutions

| INV | Verdict | Exact rule for the merged spec |
|---|---|---|
| INV-001 | MODIFY | **MODIFY = R3-V1.** Recomputed: the probe's min(1.20 B, ...) at B = 116 gives 139.2 s, which is below k = 2's planned end of 116 + 2 + 25.6 = 143.6 s. V1's `PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90` gives 143.8 s. Operability: B_f is the Spike-4 B_A1 for that package, frozen and baked into each reviewer's `--settings` together with T0 (R-21, INV-024). Its log field is `finish_signal_t`. |
| INV-002 | ACCEPT | Probe text, worded as in R3-V1:26. One phase-2 deadline T0 + 1.30 B_A1 covers resume, fallback, challenges and any H2 re-ask. A re-ask with less than one start plus one turn left before the deadline is skipped. `reask_s` is logged in A1 and every arm, and the cap uses measured elapsed time. "Hard bound" means the phase-2 end only. |
| INV-003 | MODIFY | **MODIFY = R3-V1.** RR:48 writes `--output-format json`, and RR:50 extracts the single `type=="result"` object, which exists only at exit. Salvage therefore needs stream-json. Recomputed: luna B n = floor((34.8 - 6)/(2 x 6.4)) = 2; with turn_p90 > 7.2 s, n = 1; the fallback detected at 2 s gives n = floor((32.8 - 16)/12.8) = 1. Operability: the spike S2 record must show luna streaming text before exit, and S3 must parse stream-json with `jq -s` through the same RR:50-52 filters (`model_ok`, tokens). |
| INV-004 | ACCEPT | The CONVERGENCE Jaccard uses only `origin:"own"` lines (phase-1 or pre-delivery, excluding P2-F lines and lines that carry a mechanical peer tag). ECHO is computed on real-anchor slots. F1 anchors go to the two lunas by the balanced online deal of R3-V2:21(3), not by hash (INV-023). V2's guard ("alarm in at most 2 of 12 runs") applies to own lines. R-23 gains `own_line_jaccard`, and `pairwise_task_jaccard` is kept only as a descriptive figure. |
| INV-005 | MODIFY | **MODIFY = R3-V2.** Steelman of V1: its enum-only finding form keeps X-007. Defect, recomputed: dealing A, B, A, B against forms C, F, C, F gives luna A C, C and luna B F, F. With V2's rule at r = c = 0, i = 0..3 gives recipients A, B, A, B and forms C, F, F, C, so each luna gets one card of each form. With c = 1 the forms are F, C, C, F, which is also balanced. Operability: the R-06 validator accepts `category` and `severity` only on `kind:"card"` lines from ember in F7, and still rejects `claim` and `blocking`. Card i is the board's append index under atomic writes. A card past 2k is rejected and logged `over_cap`. r, c, form and recipient are logged per slot. |
| INV-006 | ACCEPT | R3-V1:30's criterion, a triple (source, form, delivery point) in which two slots are distinct when they differ in at least 2 of the 3, plus R3-V2:22's move-only F3. F3 vs F6 then differs in source and form. F6's trigger is the exit of a luna scout: its findings block exists at that point, so the content is sealed by process exit on the sender side and no telemetry is read. F2 differs from F7 in at most 1 of the 3, so it is no replacement. |
| INV-007 | ACCEPT | = R3-V1:31, plus R3-V2:23. M2 and M4 each get a listed signature or the label "unobservable". F3's C is re-derived from ember rows only, and luna's injections are booked to the A2 share. |
| INV-008 | ACCEPT | = R3-V1:32, with k clamped at 0 and hooks = 2 s; F6 uses sonnet's turns. V2's thresholds, recomputed: at B = 116, k = 2 needs T_report_p90 <= 40.6 - 2 - 32 = 6.6 s, and k >= 1 needs <= 19.4 s. At designSpec's B = 100, k = 2 needs <= 1.0 s, and k >= 1 needs <= 13.8 s. **Operability:** Spike 4 writes a values file per package (B_A1, turn_p90, T_report_p90, PANEL_FINISH_AT, k). The file is committed with its sha256 before the first arm (R-30) and is never recomputed during an arm. Drift is handled by V3's band, not by changing k. |

**Open points.**

- **k = 1 central.** I take the V2/V3 side. k = 2 needs luna's output-heavy final turn at p90 to be no longer than 6.6 s, which is about the mean turn of 6.4 s. On designSpec it cannot happen. R3-V1's label "valid at k = 2" would make every mid-run gain optimistic by default. The k = 1 central row and the k = 2 optimistic row are both planning values. Spike 4's per-package k replaces both.
- **F3 names a move only.** I support it. It also simplifies operations: the only variable field is the move id, so V3's leak check reduces to a lookup against M1-M10. A Task inferred from a path stays in `metrics/<rid>.jsonl` and never appears in the message.

#### MEDIUM invariants worth closing

- **INV-009, -010, -011, -012, -014, -018:** adopt R3-V1:36-41. This withdraws my V4:457 runbook row ("delete `~/.claude/projects/<sandbox>` after the row is judged"). Only the session ids that a run recorded may be deleted.
- **INV-019, -020, -021, -023:** adopt R3-V2:29-32.
- **New, retry loop (INV-002 corollary).** RR:61-64 re-runs a whole review on attempt 2 when the block or the model check fails. `NOFALLBACK=1` (R-28) disables only the fallback ladder (RR:66), not this loop. `wall_s` is per attempt (RR:49, :58).
  - Rule: `elapsed_s` sums all attempts, and `attempts` and `retry_s` are logged.
  - In a collaboration arm, attempt 2 runs with `PANEL_COLLAB=0` for that reviewer, and the package counts as isolated for it (`retry_isolated`). Otherwise the hooks would deliver twice.
- **New, hang-guard symmetry (INV-001 corollary).** A1 keeps `timeout 3000` (RR:48), while the arms are killed at T0 + 1.5 B_A1. A tail run would then lose its report only in the design arms.
  - Rule: every arm, A1 included, uses the same guard and logs `hang_kill`.
  - AG:13-14 shows a maximum of 171 s against 1.5 x 120 = 180 s, so the guard rarely binds on A1.
- **Collab.json schema (R-23).** Add `reask_s`, `attempts`, `retry_s`, `phase2_timeout`, `p2_lines_salvaged`, `n_planned`, `n_launched`, `k`, `panel_finish_at`, `finish_signal_t`, `finish_would_fire` (R3-V2:33), `hang_kill`, `snapshot_missing`, `late`, `over_cap`, `slot_type`, `card_form`, `deal_r`, `deal_c`, and `own_line_jaccard`.
- **INV-015:** the sweeper timeout becomes a formula, PANEL_FINISH_AT - T0 - 2 x turn_p90, instead of the absolute 85 s. The sweeper's actual start is logged.

#### Remaining disagreements

None.

#### Final concessions

- **V4:139.** "Reproduces today's `run-reviewer.sh` exactly" is no longer true. R-05's list of allowed differences becomes:
  - R-01 and R-03;
  - removal of `--no-session-persistence` (INV-009);
  - stream-json on re-ask sessions;
  - the common hang guard.
  
  The kill switch now restores "the isolated panel with H", not today's panel.
- **"Worst" figures.** R2-V4:38 and :67 ("worst 150.0 s") and R2-V4:124 ("worst = expected" for F3) were planned-path figures. R2-V4:128's `PANEL_FINISH_AT = T0 + 1.20 B_A1` is dropped.
- **SEED:47.** R2-V4:32 ("A5 against A4 answers SEED:47") was false (INV-005).
- **Mid-arm decoy.** At R2-V4:43 I adopted the mid-arm decoy, which pools two treatments in one arm. Withdrawn (INV-018).
- **n and the combiner.** R2-V4:49 used the mean turn for n, and my combiner rule threw away every complete phase-2 line on a timeout (INV-003).
- **F6 source.** R2-V4:86 pointed F6 at telemetry cells (INV-006).
- **F1 gain.** R2-V4:63 put the gap route inside F1's C. F1's C is now 0.06-0.63, and the gap route moves to the prompting share (INV-014).
- **Sweeper timeout.** R2-V4:75's sweeper timeout was absolute, not a formula in B (INV-015).
- **Runbook coverage.** Neither V4 nor my Round 2 statement noticed the RR:61-64 retry path. This is a gap in the devops lens that the base inherited.

#### Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 `contradiction` -> M7; gap card p = 1/3 booked to the prompting share; balanced anchor deal; per-attempt n with stream-json salvage; one phase-2 deadline including re-ask; sealed judging on the post-re-ask `p1.md`; V5-D5 HL2 shadow | The only bound enforced by a kill: phase-2 end <= 150.8 s (+30.0%). luna B 147.6 s at n = 2, or 134.8 s at n = 1. C 0.06-0.63 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 locators by balanced deal; V1-R2 harvest; V2-D5 witness kind; V5-D3 first-hand rule; k per INV-008; fail-closed snapshot; sweeper timeout as a formula; common hang guard | The only cheap I7/T1 path, run in ember's idle time. Planned 130.8 s (+12.8%, k = 1) or 143.6 s (+23.8%, k = 2); signal bound 156.6 s; 174 s = breach |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | Observable signatures only; move-only payload; luna kit booked to A2; V1-R1 hash order; V5-D4 skip rule; V3 leak check; k | Tests telemetry timing vs the static kit. C comes from ember rows only and may be near 0 |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Trigger on scout exit; (Task, category) from findings; requests for uncovered Tasks; no counts, telemetry or SendMessage; surface filter; sonnet k | Claude receiver. Planned 303.7 s (+11.0%) or 331.7 s (+21.2%); bound 369.5 s; ceiling 410.6 s. Runs only if k >= 1; gain re-derived |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Enum-only forms with R3-V2's online deal; validator exception scoped to cards; cap 2k with `over_cap`; snapshot; V5 C-3; the overlap alarm stops the arm | The only slot that answers SEED:47, within one arm. Timing as F4 |

Proposed base document: V4

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | (a)-(h) per design plus a detection/action runbook |
| S-002 | V4 | Kill switch, baked settings, timing and baseline tables |
| S-003 | V2 | Gate funnel makes the H/C split structural |
| S-004 | V5 | Net collaboration, static-kit row, tokens incl. resumed input |
| S-005 | V4 | One ID scheme with a verification column |
| S-006 | V5 | Itemised unverified list, now incl. T_report_p90 |
| C-001 | V1 | Searcher/reader complementarity |
| C-002 | V5 | T2a/T2b decides routes to B1/B2/I4 |
| C-003 | V1 | Truncate, validate, re-ask inside the deadline |
| C-004 | V4 | Best-style column used by routing |
| C-005 | V4 | 12-200-character anchors plus V2's rules |
| C-006 | V4 | Process exit for phases; fail-closed snapshot mid-run |
| C-007 | V4 | Relative alarm, on own lines (INV-004) |
| C-008 | V4 | Per-issue chains |
| C-009 | V5 | Three shares, C and H never summed |
| C-010 | V2 | Fresh A0, catalogue arm, A6 |
| C-011 | V2 | One reach endpoint, final-look Fisher, against observed A1 |
| C-012 | V1 | Every design on a seed baseline |
| C-013 | V1 | Measured-reservation finish signal, R-24 audit |
| X-001 | V5 | Bottom-up H 0.03-0.34 |
| X-002 | V1 | 0 on /14; control correction only |
| X-003 | V1 | GT6 = I1 |
| X-004 | V5 | HL2 shadow schedule +0% |
| X-005 | V1 | The slowest luna sets B |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text; enum-only F7 cards |
| X-008 | V1 | Grading and judge held constant |
| X-009 | V1 | Truncate, validate, re-ask |
| X-010 | V5 | The kit may win; A2 is the comparator |
| X-011 | V5 | Anchor routes to B1/B2/I4 need the gap card |
| X-012 | V1 | Both scales defined most precisely |
| X-013 | V2 | 4/6 vs 0/6 = 15/495 = 0.030 |
| A-001 | V1 | REQ-S3 tests the act, incl. "finish now" |
| A-002 | V5 | Prices the kit's time |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | Per-package values, not /3 |
| A-006 | V2 | Decoys via the gap card |
| A-007 | V4 | Switched from V2: the merged fallback (per-attempt n, `resume_fallback`) is built on V4:452 and R-14; V2's slash-command guard grafts on |
| A-008 | V4 | Helpers write only under `$BOARD` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | c capped against measured reach |

### Variant 5 Final Position (sonnet:performance)

### Round 3 final arguments: V5 (sonnet, performance lens)

Citations: `V<n>:<line>` = `variant-<n>-original.md`; `R2-V5:<line>` = `round2-V5.md`; `R3-V<n>` = `round3-V<n>.md`; `INV-0nn` = `../invariant-probe.md`; `AG:<line>` = `round3-agenda.md`; `RR:<line>` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`. I read R3-V1 to R3-V4 before writing. Every number below was recomputed.

#### Final position

V4 stays the base and the slate stays F1, F4, F3, F6, F7. I take the same texts as the other four advocates: INV-001 and INV-003 = R3-V1, INV-005 = R3-V2, the other five ACCEPT. I add no new MODIFY text. The one defect in the shared text is a performance defect in my own Round 2 formula, and I concede it below. My lens adds three measured facts: k = 2 is the optimistic row, the common hang guard will bind in one sonnet cell, and the retry loop can double elapsed time in any arm.

#### HIGH invariant resolutions

| INV | Verdict | Exact rule for the merged spec |
|---|---|---|
| INV-001 | MODIFY | **MODIFY = R3-V1.** I concede the 1.20 B term (R2-V5:77). Recomputed at B = 116 with turn and report 6.4 s: my min(1.20 B, 1.35 B - 12.8) = min(139.2, 143.8) = 139.2 s. INV-008's k = 2 plans an end of 116 + 2 + 2 x 2 x 6.4 = 143.6 s, so my signal would fire on the planned path and truncate luna's own isolated work in every typical run. The 1.20 B term binds only when T_report_p90 < 0.15 x 116 - 6.4 = 11.0 s, which is the regime I called likely. R3-V1's `PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90` gives 143.8 s, and the bound (143.8 + 12.8) is 156.6 s (+35.0%). Performance addendum: log `finish_would_fire` in A1 and A2 (R3-V2:33), because a signal that fires only in design arms is a hidden treatment. |
| INV-002 | ACCEPT | R3-V1:26 wording. One deadline T0 + 1.30 B_A1 covers resume or fallback, challenges and any H2 re-ask. A re-ask without one start plus one turn left is skipped. `reask_s` is logged in A1 and every arm. "Hard bound" means the phase-2 end only. |
| INV-003 | MODIFY | **MODIFY = R3-V1.** Recomputed: deadline 1.30 x 116 = 150.8 s; a launch at 116 leaves 34.8 s; n = floor(28.8/12.8) = 2 (end 116 + 6 + 25.6 = 147.6 s); for turn_p90 > 7.2 s, floor(28.8/14.4) = 2 only at exactly 7.2 and n = 1 above it. A fallback detected at 2 s: floor((32.8 - 16)/12.8) = 1 (end 118 + 16 + 12.8 = 146.8 s). Stream-json salvage is required because RR:48 writes `--output-format json` and RR:50 reads the one `result` object that exists only at exit. Cost note: stream-json with `--verbose` writes more output per run, but it is a local file write, not a model cost. |
| INV-004 | ACCEPT | Own-line Jaccard, ECHO on real-anchor slots, balanced online deal (R3-V2:20), alarm guard on own lines only. |
| INV-005 | MODIFY | **MODIFY = R3-V2.** Recomputed at r = c = 0: recipients (i + r) mod 2 = A, B, A, B; forms by (i + floor(i/2) + c) even = C, F, F, C. Luna A gets C, F and luna B gets F, C, so each luna sees both forms; R3-V1's alternation gives A: C, C and B: F, F, which confounds luna with form. Performance and power note: ember posts at most 2k cards at 3.2 s each, off the critical path. At k = 2 there are at most 12 x 3 x 4 = 144 cards (72 per form). At k = 1 there are 12 x 3 x 2 = 72 cards (36 per form) and each luna gets one card, so the contrast is across lunas, balanced by the seeded r and c. At k = 1 the form contrast is descriptive, and the spec must say so. |
| INV-006 | ACCEPT | R3-V1's (source, form, delivery point) criterion, with F3 injections naming a move only (R3-V2:22). F6 uses findings from finished peers, never telemetry. F2 differs from F7 in at most 1 of 3 and is not a replacement. |
| INV-007 | ACCEPT | = R3-V1:31 plus R3-V2:23. M2 and M4 get a listed signature or "unobservable". Luna injections are booked to the A2 static-kit share. F3's C is re-derived from ember rows only. |
| INV-008 | ACCEPT | = R3-V1:32 with k clamped at 0 (R3-V2:24 thresholds). Recomputed with hooks = 2 and turn 6.4: k = 2 needs T_report_p90 <= 0.35 B - 34. That is 6.6 s at B = 116, 1.0 s at designSpec's 100 (AG:13), 8.0 s at 120 and 8.7 s at 122. k >= 1 needs <= 0.35 B - 21.2: 19.4 s, 13.8 s, 20.8 s, 21.5 s. k >= 1 at all needs 0.35 B - 2 - 12.8 >= 12.8, so B >= 78.9 s (the probe's typical floor). For F6 (B = 273.7, turn 14): k = 2 needs <= 23.8 s, k >= 1 needs <= 51.8 s. Package medians are from runs without H; A1 carries H, so measured k can only rise. |

**Open points.**

- **k = 1 as the central row (V2, V3, V4) versus k = 2 (V1): I take k = 1.** k = 2 needs luna's output-heavy last turn at p90 to fit 6.6 s, about the mean turn of 6.4 s, and it is impossible on designSpec at the 100 s median. Both rows are planning values until Spike 4 publishes the per-package k. Planned ends at B = 116: k = 1 gives 116 + 2 + 12.8 = 130.8 s (+12.8%); k = 2 gives 143.6 s (+23.8%). F6: 303.7 s (+11.0%) and 331.7 s (+21.2%).
- **F3 injections name a move only: I agree.** Without it F3 and F6 share the form "move + Task" and differ in source only (1 of 3).
- **V4's two rules from RR: ACCEPT both, with one measured caveat.**
  - Retry loop (RR:61-64): attempt 2 re-runs the whole review, and `wall_s` is per attempt (RR:49). A failure at about B followed by a full retry gives about 2 B elapsed (100 + 116 = 216 s, +86%), regardless of design. `elapsed_s` sums attempts, `retry_s` is logged, and attempt 2 runs isolated (`retry_isolated`). Rows with a retry are reported in a separate column so that they do not hide a design effect.
  - Common hang guard, logged `hang_kill`, in A1 too: required for a fair elapsed comparison. Measured fit against AG:9-16 (max wall vs 1.5 x median): ember panels 123 vs 150, 171 vs 180, 155 vs 183 (never binds); haiku 305 vs 330, 285 vs 357, 297 vs 339 (never binds); sonnet DS 283 vs 388.5, AL 416 vs 453, **DE 440 vs 403.5, binds in 1 of 6 runs**. So the guard is symmetric but not free on the sonnet panel, and F6's SL2 arms must report `hang_kill` counts in both arms.

#### MEDIUM invariants worth closing

- INV-009 to INV-012, INV-014, INV-018: adopt R3-V1:36-41.
- INV-015: sweeper timeout as a formula, PANEL_FINISH_AT - T0 - 2 x turn_p90 (R3-V4:49). Recomputed at planning values: 143.8 - 12.8 = 131.0 s after T0, instead of the absolute 85 s.
- INV-019 to INV-021: V2's decision table (R3-V2:30-32). Recomputed: with A1 at 1/12, 5/12 gives p = 0.077 and 6/12 gives 0.034 (agrees with R3-V2). The spec says plainly that the plan cannot detect the central H estimate 0.14/14 (R2-V5:20). Repairing the measurement does not create power.
- INV-013: an empty digest makes ECHO not applicable, not 0.

#### Remaining disagreements

None. The k = 1 versus k = 2 label is a naming question that Spike 4's per-package k replaces.

#### Final concessions

- R2-V5:77: the 1.20 B term. Dropped for R3-V1's 1.35 B form.
- R2-V5:35: "A5 vs A4 differs in message content only ... the cleanest possible test of SEED:47" was false (INV-005): sender session, content source, move type and targets all differ.
- R2-V5:51: "F1 is the only slot with a compliance-free hard bound" holds for the phase-2 end only, and only with the re-ask inside the deadline (INV-002, INV-022).
- R2-V5:46: n used the mean turn (INV-003); the p90 rule I applied to the finish time must apply to n as well.
- R2-V5:19: F1's input-token cost is a column in the S-004 table (resume replays about 16 turns of context).
- No Round 2 consensus winner changes.

#### Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | `contradiction` -> M7; gap card p = 1/3 booked to prompting; balanced anchor deal; per-attempt n with stream-json salvage; one phase-2 deadline incl. re-ask; V5-D5 HL2 shadow (+0%, worst +6.3%, no arm) | Only kill-enforced bound: phase-2 end <= 150.8 s (+30.0%). Luna B 147.6 s at n = 2 or 134.8 s at n = 1. C 0.06-0.63 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | Locators by balanced deal; harvest; witness kind; first-hand rule; k per INV-008; sweeper timeout formula; common hang guard | Cheap I7 path in ember's idle time. 130.8 s (k = 1) / 143.6 s (k = 2); signal bound 156.6 s; 174 s = breach |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | Observable signatures; move-only payload; luna kit booked to A2; skip rule; leak check; k | Telemetry timing versus static kit; C from ember rows only, may be near 0 |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Finished peers' (Task, category); uncovered-Task requests; no counts, telemetry or SendMessage; sonnet k | Runs only if sonnet T_report_p90 <= 51.8 s. 303.7 / 331.7 s; bound 369.5 s; ceiling 410.6 s |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Enum-only forms with R3-V2 online deal; cap 2k; snapshot; first-hand rule; overlap alarm stops the arm | Only slot that answers SEED:47, within one arm; timing as F4 |

Proposed base document: V4

#### Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V4 | Per-design requirements plus a runbook |
| S-002 | V4 | Kill switch, baked settings, timing tables |
| S-003 | V2 | Gate funnel makes the H/C split structural |
| S-004 | V5 | Net collaboration, static-kit row, input tokens for resume |
| S-005 | V4 | One ID scheme with verification column |
| S-006 | V5 | Itemised unverified list, now incl. T_report_p90 |
| C-001 | V1 | Searcher/reader complementarity |
| C-002 | V5 | T2a/T2b decides routes to B1/B2/I4 |
| C-003 | V1 | Truncate, validate, re-ask inside the deadline |
| C-004 | V4 | Best-style column used by routing |
| C-005 | V4 | 12-200-character anchors plus V2's rules |
| C-006 | V4 | Process exit for phases; fail-closed snapshot mid-run |
| C-007 | V4 | Relative alarm on own lines |
| C-008 | V4 | Per-issue chains |
| C-009 | V5 | Three shares; C and H never summed |
| C-010 | V2 | Fresh A0, catalogue arm, A6 |
| C-011 | V2 | One reach endpoint, final-look Fisher, vs observed A1 |
| C-012 | V1 | Seed baseline per design |
| C-013 | V1 | Measured-reservation finish signal plus R-24 audit |
| X-001 | V5 | Bottom-up H 0.03-0.34 |
| X-002 | V1 | 0 on /14; control correction only |
| X-003 | V1 | GT6 = I1 |
| X-004 | V5 | HL2 shadow schedule +0% |
| X-005 | V1 | The slowest luna sets B |
| X-006 | V4 | One block, P2-F ids, origin stripped |
| X-007 | V2 | No free text; enum-only F7 cards |
| X-008 | V1 | Grading and judge held constant |
| X-009 | V1 | Truncate, validate, re-ask |
| X-010 | V5 | The kit may win; A2 is the comparator |
| X-011 | V5 | Anchor routes to B1/B2/I4 need the gap card |
| X-012 | V1 | Both scales defined most precisely |
| X-013 | V2 | 4/6 vs 0/6 = 15/495 = 0.030 |
| A-001 | V1 | REQ-S3 tests the act, incl. "finish now" |
| A-002 | V5 | Prices the kit's time |
| A-003 | V2 | Random labels plus sealed-report judging |
| A-004 | V4 | States the H-C interaction |
| A-005 | V5 | Per-package medians, not /3 |
| A-006 | V2 | Decoys via the gap card |
| A-007 | V4 | Spike, bounded fallback, `resume_fallback` metric |
| A-008 | V4 | Helpers write only under `$BOARD` |
| A-009 | V2 | Confirmation on two new packages |
| A-010 | V1 | States why EL2 is the base |
| A-011 | V5 | Cap gains against measured reach |

### Round 3 tally and HIGH-invariant closure

### round3: advocates=5 need=4 agreed=43/43 convergence=1.000
| Point | Level | Votes (V1 V2 V3 V4 V5) | Leader | Count | Status |
|---|---|---|---|---|---|
| S-001 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| S-002 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| S-003 | L1 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| S-004 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| S-005 | L1 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| S-006 | L1 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| C-001 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| C-002 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| C-003 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| C-004 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-005 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-006 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-007 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-008 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| C-009 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| C-010 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| C-011 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| C-012 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| C-013 | L3 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-001 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| X-002 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-003 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-004 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| X-005 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-006 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| X-007 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| X-008 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-009 | L3 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-010 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| X-011 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| X-012 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| X-013 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-001 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| A-002 | L3 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| A-003 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-004 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| A-005 | L3 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
| A-006 | L3 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-007 | L2 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| A-008 | L3 | V4 V4 V4 V4 V4 | V4 | 5/5 | agreed |
| A-009 | L2 | V2 V2 V2 V2 V2 | V2 | 5/5 | agreed |
| A-010 | L2 | V1 V1 V1 V1 V1 | V1 | 5/5 | agreed |
| A-011 | L2 | V5 V5 V5 V5 V5 | V5 | 5/5 | agreed |
coverage L1: 3 points debated
coverage L2: 31 points debated
coverage L3: 9 points debated

#### HIGH invariant closure (Round 3; rule: 4 of 5 on ACCEPT, on one MODIFY text, or on REJECT)

| INV | V1 | V2 | V3 | V4 | V5 | Closing outcome | Count | Status |
|---|---|---|---|---|---|---|---|---|
| INV-001 | MODIFY (own text) | MODIFY = R3-V1 | MODIFY = R3-V1 | MODIFY = R3-V1 | MODIFY = R3-V1 | MODIFY = R3-V1 (PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90; three-number time block; cap audited, not enforced, for slots 2-5) | 5/5 | closed |
| INV-002 | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT (one phase-2 deadline T0 + 1.30 B_A1 incl. re-ask; `reask_s`) | 5/5 | closed |
| INV-003 | MODIFY (own text) | MODIFY = R3-V1 | MODIFY = R3-V1 | MODIFY = R3-V1 | MODIFY = R3-V1 | MODIFY = R3-V1 (n per launch attempt with turn_p90; stream-json salvage) | 5/5 | closed |
| INV-004 | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT (own-line Jaccard; ECHO on real anchors; disjoint anchor deal) | 5/5 | closed |
| INV-005 | MODIFY (own text) | MODIFY (own text) | MODIFY = R3-V2 | MODIFY = R3-V2 | MODIFY = R3-V2 | MODIFY = R3-V2 (within-F7 enum-only form contrast; online balanced deal) | 4/5 | closed |
| INV-006 | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT with R3-V1 distinctness triple; F6 kept on finished-findings coverage | 5/5 | closed |
| INV-007 | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT (observable signatures only; luna injections = static prompt share) | 5/5 | closed |
| INV-008 | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT | ACCEPT with R3-V1 clamp (k per package, Spike 4 publishes) | 5/5 | closed |

INV-005: V2's text is V1's text with only the dealing clause replaced; V1's own clause was shown by V2, V3, V4 and V5 to give each luna two cards of one form. 4 of 5 on R3-V2 closes it.

#### Open points beyond the HIGH items

| Point | V1 | V2 | V3 | V4 | V5 | Outcome |
|---|---|---|---|---|---|---|
| Central k for F3/F4/F7 rows | k = 2 | k = 1 | k = 1 | k = 1 | k = 1 (label superseded by Spike 4) | k = 1 central, k = 2 optimistic (4/5) |
| F3 injections name a move only (INV-006 boundary with F6) | not stated | yes | yes | yes | yes | adopted (4/5; V1 did not object) |
| INV-006 slate question: keep F6 or replace with F2 | keep F6 | keep F6 | keep F6 | keep F6 | keep F6 | F6 kept (5/5) |
| V4's run-reviewer.sh rules: elapsed sums all attempts, attempt 2 isolated (`retry_isolated`); same hang guard in every arm incl. A1 (`hang_kill`) | raised after V1 wrote | raised after V2 wrote | raised after V3 wrote | proposed | accepted | adopted as MEDIUM rules (2 of 2 advocates who saw them; no objection) |

#### Convergence check after Round 3

- Diff-point agreement: 43/43 = 1.000 (threshold 0.75).
- Taxonomy coverage: L1 3, L2 31, L3 9 points; all levels covered.
- Invariant gate: 0 HIGH-severity items remain unaddressed (INV-001..INV-008 closed above). MEDIUM items are warnings and are carried into the refactor plan.
- Status: CONVERGED.

## Scoring Matrix

Confidence rule: 5/5 in Round 3 and agreed (>= 4/5) in every earlier round -> 95%; 5/5 in Round 3 after a Round 1 split -> 90%; 4/5 at the end -> 80%. No point is 100% (not every losing advocate explicitly conceded each point).

| Diff Point | Level | Winner | Confidence | R1 / R2 / R3 support | Evidence Summary (R3-V1 reason) |
|---|---|---|---|---|---|
| S-001 | L2 | V4 (variant-4) | 95% | 5/5 V4 / 5/5 V4 / 5/5 | (a)-(h) per design plus a detection/action runbook |
| S-002 | L2 | V4 (variant-4) | 95% | 5/5 V4 / 5/5 V4 / 5/5 | Kill switch, baked board path, timing and baseline tables |
| S-003 | L1 | V2 (variant-2) | 90% | 3/5 V2 / 5/5 V2 / 5/5 | The gate funnel makes the H/C split structural |
| S-004 | L2 | V5 (variant-5) | 95% | 5/5 V5 / 5/5 V5 / 5/5 | Net collaboration, static-kit row, tokens per added issue (plus input tokens for resume) |
| S-005 | L1 | V4 (variant-4) | 95% | 5/5 V4 / 5/5 V4 / 5/5 | One ID scheme with a verification column |
| S-006 | L1 | V5 (variant-5) | 95% | 4/5 V5 / 5/5 V5 / 5/5 | Itemised unverified list tied to each number |
| C-001 | L2 | V1 (variant-1) | 90% | 3/5 V2 / 5/5 V1 / 5/5 | Searcher/reader complementarity predicts a gain the kit cannot copy |
| C-002 | L2 | V5 (variant-5) | 95% | 5/5 V5 / 5/5 V5 / 5/5 | T2a/T2b decides which routes reach B1/B2/I4 |
| C-003 | L2 | V1 (variant-1) | 95% | 5/5 V1 / 5/5 V1 / 5/5 | Truncate, validate, re-ask; grading constant |
| C-004 | L2 | V4 (variant-4) | 95% | 5/5 V4 / 5/5 V4 / 5/5 | Best-style column used by routing |
| C-005 | L2 | V4 (variant-4) | 90% | 3/5 V2 / 5/5 V4 / 5/5 | 12-200-character anchors plus V2's rules |
| C-006 | L3 | V4 (variant-4) | 90% | 3/5 V4 / 5/5 V4 / 5/5 | Process exit for phases; fail-closed snapshot for mid-run |
| C-007 | L3 | V4 (variant-4) | 95% | 4/5 V4 / 5/5 V4 / 5/5 | Relative, ground-truth-free alarm, now on own lines (INV-004) |
| C-008 | L2 | V4 (variant-4) | 90% | 3/5 V4 / 5/5 V4 / 5/5 | Per-issue chains |
| C-009 | L2 | V5 (variant-5) | 95% | 4/5 V5 / 5/5 V5 / 5/5 | Three shares, C and H never summed |
| C-010 | L2 | V2 (variant-2) | 95% | 4/5 V2 / 5/5 V2 / 5/5 | Fresh A0, catalogue arm, A6 |
| C-011 | L2 | V2 (variant-2) | 95% | 5/5 V2 / 5/5 V2 / 5/5 | One reach endpoint, final-look Fisher, +4 over A2 |
| C-012 | L2 | V1 (variant-1) | 95% | 4/5 V1 / 5/5 V1 / 5/5 | Every design on a seed baseline |
| C-013 | L3 | V1 (variant-1) | 95% | 5/5 V1 / 5/5 V1 / 5/5 | Panel finish signal, now measured-reservation form plus R-24 audit |
| X-001 | L2 | V5 (variant-5) | 95% | 4/5 V5 / 5/5 V5 / 5/5 | Bottom-up H 0.03-0.34 |
| X-002 | L2 | V1 (variant-1) | 95% | 4/5 V1 / 5/5 V1 / 5/5 | 0 on /14; control correction only |
| X-003 | L2 | V1 (variant-1) | 95% | 5/5 V1 / 5/5 V1 / 5/5 | GT6 = I1 |
| X-004 | L2 | V5 (variant-5) | 95% | 5/5 V5 / 5/5 V5 / 5/5 | HL2 shadow schedule +0% |
| X-005 | L2 | V1 (variant-1) | 95% | 5/5 V1 / 5/5 V1 / 5/5 | The slowest luna sets B |
| X-006 | L3 | V4 (variant-4) | 95% | 5/5 V4 / 5/5 V4 / 5/5 | One block, P2-F ids, origin stripped |
| X-007 | L2 | V2 (variant-2) | 95% | 4/5 V2 / 5/5 V2 / 5/5 | No free text, which is why INV-005 uses enums |
| X-008 | L2 | V1 (variant-1) | 95% | 5/5 V1 / 5/5 V1 / 5/5 | Grading and judge held constant |
| X-009 | L3 | V1 (variant-1) | 95% | 5/5 V1 / 5/5 V1 / 5/5 | Truncate, validate, re-ask |
| X-010 | L2 | V5 (variant-5) | 95% | 5/5 V5 / 5/5 V5 / 5/5 | The kit may win; A2 is the comparator |
| X-011 | L2 | V5 (variant-5) | 95% | 4/5 V5 / 4/5 V5 / 5/5 | Anchor routes to B1/B2/I4 need the gap card |
| X-012 | L2 | V1 (variant-1) | 90% | 3/5 V1 / 5/5 V1 / 5/5 | Both scales and the label mapping defined most precisely |
| X-013 | L2 | V2 (variant-2) | 95% | 5/5 V2 / 5/5 V2 / 5/5 | 4/6 vs 0/6 = 0.030 |
| A-001 | L2 | V1 (variant-1) | 95% | 5/5 V1 / 5/5 V1 / 5/5 | REQ-S3 tests the act, now also on "finish now" |
| A-002 | L3 | V5 (variant-5) | 95% | 5/5 V5 / 5/5 V5 / 5/5 | Prices the kit's time |
| A-003 | L2 | V2 (variant-2) | 95% | 5/5 V2 / 5/5 V2 / 5/5 | Random labels plus sealed-report judging |
| A-004 | L2 | V4 (variant-4) | 95% | 5/5 V4 / 5/5 V4 / 5/5 | States the H-C interaction |
| A-005 | L3 | V5 (variant-5) | 95% | 5/5 V5 / 5/5 V5 / 5/5 | Per-package values, not /3 |
| A-006 | L3 | V2 (variant-2) | 95% | 5/5 V2 / 5/5 V2 / 5/5 | Decoys via the gap card |
| A-007 | L2 | V4 (variant-4) | 95% | 4/5 V4 / 4/5 V4 / 5/5 | Spike, fallback, `resume_fallback` metric |
| A-008 | L3 | V4 (variant-4) | 95% | 5/5 V4 / 5/5 V4 / 5/5 | Helpers write only under `$BOARD` |
| A-009 | L2 | V2 (variant-2) | 95% | 5/5 V2 / 5/5 V2 / 5/5 | Confirmation on two new packages |
| A-010 | L2 | V1 (variant-1) | 95% | 5/5 V1 / 5/5 V1 / 5/5 | States why EL2 is the base |
| A-011 | L2 | V5 (variant-5) | 95% | 4/5 V5 / 4/5 V5 / 5/5 | c capped against measured reach |

Points won: V1 12, V2 8, V3 0, V4 12, V5 11.

## Convergence Assessment
- Points resolved: 43 of 43
- Alignment: 100%
- Threshold: 75%
- Taxonomy coverage: L1 3, L2 31, L3 9 (all levels covered)
- Invariant gate: 8 HIGH items closed in Round 3 (INV-001, -003 MODIFY = R3-V1 5/5; INV-005 MODIFY = R3-V2 4/5; INV-002, -004, -006, -007, -008 ACCEPT 5/5); 0 HIGH unaddressed
- Status: CONVERGED
- Unresolved points: none
- Round history: Round 1 37/43 (0.860); Round 2 43/43 (1.000) but BLOCKED_BY_INVARIANTS; Round 3 43/43 (1.000), CONVERGED
- Base proposed by every advocate in every round: V4
