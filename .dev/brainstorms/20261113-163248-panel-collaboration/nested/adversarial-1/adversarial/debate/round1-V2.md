# Round 1 statement: V2 (analyzer lens)

## Position summary

V2 should supply the merge's theory spine (the three-gate funnel), its contamination defence against the "a peer found something here" signal (decoys), and its attribution machinery (a fresh old-harness arm, a static-catalogue arm and within-run sealed-report judging). For the redesigns and the scaffolding, V4 is the better base: its five gain tables are arithmetically clean, and three of my five slate cores come from it. Two of my own gain tables carry errors, which I confirm below.

## Steelman and critique of each other variant

### V1

**Steelman.** V1 is the only variant whose design treats the +35% cap as a panel-level rule. `PANEL_FINISH_AT = T0 + 1.20 x B` (V1:138) makes every mid-run design stop on time by construction. REQ-S3 (V1:614) is the only spike that tests whether a gateway model *acts* on injected text; every other variant tests only that the hook fires. R2 Evidence Trail (V1:235-256) is the only design that needs no model action on either side, which matters because luna makes about one Bash call per run. V1 holds grading constant (V1:111), pins the judge template by sha256 (REQ-M3) and adds a mechanical deny-list against overfitting (REQ-C2). Its H2 (truncate, validate, re-ask once) is the best anchor-drop fix of the five.

**Critique.**
- R3's "hard" cap is `1.35 x T1` of the same run (V1:323), not 1.35 x the named 116 s. If a slow luna ends phase 1 at 150 s, the cap becomes 202 s, which is +74% of S07. The guarantee is per run, not against the baseline the seed names.
- The R4 gain total does not follow from its rows. The rows give 0.02 to 0.60; V1 states 0.05 to 0.45 (V1:426-432; I re-summed them). The R2 I7 high of 0.35 exceeds its own chain, 0.45 x 0.7 x 0.85 = 0.27.
- The decision rule ORs three endpoints, each at p <= 0.10 (V1:591), so the familywise false-pass rate is well above 0.10.
- R1 and R4 depend on models posting cards, which V1 itself calls the weak point (V1:540).
- V1 has no fresh old-harness arm, so the H share is "descriptive only" against historical S07 (V1:594).

### V3

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

### V4

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

### V5

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

## Strengths claimed

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

## Concessions

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

## Shared assumptions

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

## Proposed final slate of five redesigns

| Slot | Family | Core | Grafted from | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 | V2-D2: decoys (1 of 3), unanchored tasks first, flip row `contradiction` -> M7 on all tasks (keeps V2-D3's I6 trigger), absolute time box `min(35, 150 - start - 4)` replacing the 35/45 s split; V1-R3: one gap card; V4 combiner; V2 R-25 sealed-report judging | The family four variants reached independently; deterministic, no hooks; V4-3's gain table is clean (0.23-0.94) |
| 2 | F4 Searcher-to-reader fact relay | V2-D1 | V4-2: the sweeps run in a fresh ember sweeper session that never sees ember's report; V1-R2: automatic, hash-split harvest; V5-D3: command string on every fact plus the first-hand rule C-3; corrected guard (0 locators from t > 127 s) and I7 0.17-0.43 | Theory A pointer-following (48/48); the Stop-gated natural seal needs no luna seal call, unlike V4-2; strongest I7 path |
| 3 | F3 Content-free coverage steering | V4-1 | V2-D4: Task x move cell grain from trigger regexes, so the injected gap carries a location but no peer content; V1-R1: per-receiver hash ordering of gaps; V1 `PANEL_FINISH_AT`; V4 deadline corrected to 112 s | No model authoring, so the lowest compliance risk; measures panel blind spots directly |
| 4 | F5 Structural index / source witness | V2-D5 | V5-D1: kind -> move index entries in the same single ember post; V1-R4: unnamed-referrer item; B5 row corrected (0.06-0.24); EL2 variant with at most 2 witness lines per luna (116 + 20 + 12 = 148 s, +27.6%) alongside the S14 form | The only design aimed at source-only rules masked by the checkout (B5, I1, B2) |
| 5 | F6 Steering a running strong model | V4-5 | V2-D4: the Stop-time assignment of 2 uncovered cells to sonnet; V1-R5: request semantics, delivered by the harness instead of SendMessage; V4 surface filter kept | Harness-generated with a Claude receiver; deflects the one model that already sweeps; gain table clean (0.26-1.06) |

F2 (mid-run method relay) and F7 (directed challenge) are left out because they rely on gateway models authoring sends mid-run, which carries the highest compliance and free-text risk. Their key idea, propagation, survives in slot 1's flip table.

Proposed base document: V4. It has the most complete scaffold (baseline table, kill switch, timing constants, telemetry, runbooks, and R-01..R-30 with a verification column), zero gain-table errors, and three of the five cores. Its theories section takes V2's gate table. Its experiment takes V2's arm design (fresh A0, catalogue arm, within-run C) at at least 6 runs per arm, with V5's 12-run controls, in place of V4's n = 4 screen.

## Per-point positions

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
