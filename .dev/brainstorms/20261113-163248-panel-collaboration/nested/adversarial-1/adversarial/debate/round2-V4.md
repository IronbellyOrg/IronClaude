# Round 2 rebuttal: V4 (opus, devops lens)

Citations: `V<n>:<line>` = variant files; `R1-V<n>:<line>` / `R2-V<n>:<line>` = debate statements; `SEED:<line>` = seed brief. I re-read V4:276-445, :455-579 and :640-745, V5:138-156 and :350-392 for this round, and recomputed every number below.

## Responses to criticisms of V4

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

## Agenda items

### 1. Slot 5: F5 versus F7

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

### 2. F1 core, time box and gap card

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

### 3. F4 core and its worst case

**Core V4-2; the converged block** (R2-V1:69-75, R2-V2:82-86, R2-V3:85): sweeper 41 + 6 + 10 x 3.2 = 79 s, inside ember's idle time; luna B 116 + 2 x 2 x 6.4 + 2 = **143.6 s (+23.8%)**; worst **150.0 s (+29.3%)**. This matches my R1 fix (144 s / 150 s, R1-V4:65). Rules: at most 2 facts per luna, no Stop hold, late facts logged `late` and dropped.

Devops rules the other blocks leave implicit:

| Rule | Why |
|---|---|
| **Fail closed on the seal, fail open on the review.** If the snapshot write or hash fails, the hook delivers nothing and logs `snapshot_missing`; the review continues (R-22). | Never deliver to an unsealed reviewer. A hook error must never kill a review. |
| Snapshot under `$BOARD`; harness records sha256 in `collab.json`; V3 timestamp test (R2-V3:99) | Bash is unrestricted (A-008). |
| Sweeper `timeout` at T0 + 85 s; atomic fact writes (R2-V3:100-101) | `--max-turns` does not exist (V5:106). |
| Hang guard: process `timeout` at T0 + 1.5 x B_A1 (174 s at planning B) on every reviewer in mid-run arms. A kill counts as `SLO_BREACH`. | Mid-run designs cannot be cut off without losing the report (R2-V1:147). Their bound is count caps plus the finish signal. A hung gateway session still needs a ceiling. The 1.5x figure is the existing "no package > 1.5x" guard. |

C /14 stays 0.14-0.67 (V4:325 rows re-added). The witness kind takes 1 of the 4 fact places and replaces the 0-0.05 B5/I1 placeholders. I7 is **0.17-0.50** (concession above).

### 4. F3 grafts

I accept the converged set: V2-D4 Task x move cells filled from V4-1 telemetry; V1-R1 per-receiver hash order; V5-D4's skip rule only; V3's leak check on variable fields only (R2-V3:110); the surface filter; V3-R1 resume digest as the fallback if S0 fails (147.6 s). R2-V1:95 rejects the V5-D4 Stop block: 116 + 12.8 + 19.2 + 2 = 150.0 s against 143.6 s, and it rests on the unverified reissue. I recomputed and agree. Deadline: write it as `T0 + 1.35 x B_A1 - 47 s` (110 s at planning B; V4:215 said 110 s, the correct 157 - 45 is 112 s).

### 5. F6 requests versus uncovered cells

**Accept the V1/V2/V3 merge.** The harness renders imperative requests only from V2-D4 uncovered cells, ranked by luna's declared not-checked scope. There are no covered counts, and V4:545's "Tasks that already have a finding ... with the counts" is withdrawn as a clearance signal (V5 C-2). No SendMessage. The surface filter (V4:563) stays. Precision fix: SL2 = 821/3 = 273.7 s, so worst 330 s is **+20.6%** and typical 302 s is +10.4% (the +20.4%/+10.2% figures used 274).

### 6. Experiment section

**Adopt R2-V2's plan** (R2-V2:118-148): A0 fresh (4) plus S07 context; A1 and A2 at 12; A3 F1, A4 F4, A5 F7, A6 F3 at 6 -> 12; stage 2 on SL2 for F6. One reach endpoint. Fisher one-sided p < 0.05 at the final look only: 4/12 vs 0/12 = 495/10,626 = 0.047 passes; 3/12 vs 0/12 = 220/2,024 = 0.109 fails. X must also beat A2 by >= 4 at n = 12. The interim look is futility only (R2-V2:144). Size: 4 + 12 + 12 + 4 x 12 = 76 maximum, 52 minimum, plus 30 in stage 2.

Operational requirements the plan needs from V4:
- A1 runs with `PANEL_COLLAB=0`, and its launch command is checked byte-identical to today's plus H (R-05). Otherwise "A1" is not the panel a design replaces.
- Gate 0: S0 (hooks fire), S2 (resume), S3 (full-chain smoke, 0 dropped lines) and REQ-S3 act rate, recorded before any arm (R-27).
- Conduct: `NOFALLBACK=1`, at most 10 concurrent runs and at most 4 ember, `model_ok` for sweeper and phase-2 sessions (R-28), block-randomised order (V5).
- Guard: SLO error budget, 1 package in 12 over 1.35 x B_A1 per arm, stops the arm (R-24).

### 7. Harness share figure

Carry **H = 0.03-0.34 /14 per run, central 0.14** (V5:147-151; low 0.02 + 0.01 + 0.00, high 0.16 + 0.08 + 0.10, central 0.08 + 0.03 + 0.03, all re-added). H-4 is excluded (X-008); V5's table never counted it, so the range is unchanged. H-6 is a secondary score. Leak removal adds 0 on /14 and is a sonnet-panel I7 measurement correction on control. Spike 5 replaces the normalizer row. Each gain block carries C and H in separate columns and never sums them.

### 8. Idle-time budgets and the baseline rule

**Adopt V1's five-part rule** (R2-V1:139-147), **V2's per-slot slowdown limit** (R2-V2:176-187) and **V3's drift band** (R2-V3:162-168). Rechecked: s <= (0.35B - W)/B gives F4/F7 6.6/116 = 5.7%, F3 13.0/116 = 11.2%, F6 39.9/274 = 14.6%. Drift band lower edge 1.30/1.35 = 0.963.

Two devops refinements:

1. **Measure s on the critical-path reviewer, not the arm.** The cap moves only if the *slowest luna* slows. In F4 the extra brief text goes to the sweeper; in F7 most goes to ember (off the path). F4's 5.7% limit is therefore far easier to meet than it looks, provided luna's brief is unchanged. Spike 4 logs per-role end times; the limit applies to the role that sets B.
2. **Name the baseline once.** V4's "A0" (V4:648, R-24) is the merged A1. The merged spec renames it, so that no requirement measures the cap against the old-harness arm.

## Updated assessment of other variants

- **V1:** R2's repairs are the best in the debate: the B_A1 box, one-way F7, withdrawing first-Stop delivery and the hook snapshot. It carries the mislabelled HL2 figure (R2-V1:61).
- **V2:** Its futility-only interim look and per-slot slowdown limit are needed. Its `flag_finding_overlap` is a cheap, ground-truth-free alarm, and I adopt it. It rejected my witness graft correctly.
- **V3:** This round's most useful auditor. It found the HL2 mislabel, my haiku-variant error, the disjoint-split I7 double count and the drift-band gap. Its F1 gain keeps I4 on the anchor route, which T2b does not allow.
- **V5:** Not yet heard in R2. "Never wait", the 12-run controls, the H table and the shadow schedule are all in the slate. Its F5 core is the only R1 slot no longer supported.

## Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Anchor-text routing plus V2-D2 `contradiction` -> M7; decoy slot = V1-R3 gap card (p = 1/3 per slot, kind withheld); V1 box min(35, T0 + 1.30 B_A1 - start); V4 combiner with `phase2_timeout` fallback; V2 sealed-report judging; HL2 variant = V5-D5 as written (haiku canary) | Sealed by process exit, no hooks. EL2 147.6 s (+27.2%), hard 150.8 s (+30.0%); HL2 +0%, worst +6.3%. C 0.06-0.73 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint ranked locators; V1-R2 harvest incl. sweeper output; V2-D5 witness as a sweep kind; V5-D3 first-hand rule and 10% stop; 2 facts per luna, no hold; hook snapshot seal, fail-closed, sha256 by harness, V3 timestamp test; sweeper timeout T0 + 85 s; hang guard 1.5 x B_A1 | Only cheap I7/T1 path, in ember's idle time. 143.6 s (+23.8%), worst 150.0 s (+29.3%). C 0.14-0.67; I7 0.17-0.50 control |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move cells from telemetry; V1-R1 hash order; V5-D4 skip rule only; V3 leak check on variable fields; surface filter; V3-R1 resume-digest fallback | No model authors anything. 143.6 s (+23.8%), worst = expected; arm A6 tests exchange vs kit |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Harness-rendered requests from uncovered cells only, ranked by luna's not-checked scope; no covered counts; V1-R5 brief line; V3 leak check; surface filter; no SendMessage | Harness author, Claude receiver. Worst 330 s (+20.6% of 273.7 s), typical +10.4% |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Hash-split cards, at most 2 per luna (4 slots = 4 cards); hook snapshot seal; no luna card, no hold; V5 C-3; `PANEL_FINISH_AT`; `flag_finding_overlap` alarm; S13 variant dropped | Distinct mechanism; answers SEED:47 against slot 2 on one panel. 143.6 s (+23.8%), worst 150.0 s (+29.3%). C 0.08-0.77 |

Shared substrate: V4 board with baked path (R-21), kill switch (R-05), hooks exit 0 (R-22), `collab.json` (R-23), SLO budget against B_A1 (R-24), quarantine-in-place (R-26); V1 `PANEL_FINISH_AT = T0 + 1.20 B_A1`; V2 no-free-text rules over V4's 12-200-character anchors; V4 relative alarm (J + 0.15 or ledger rows -20%) plus per-design echo.

Proposed base document: V4

## Per-point positions

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
