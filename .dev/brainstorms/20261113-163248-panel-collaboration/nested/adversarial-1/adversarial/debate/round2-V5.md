# Round 2 rebuttal: V5 (sonnet, performance lens)

Citations: `V<n>:<line>` = variant files; `R1-V<n>:<line>` / `R2-V<n>:<line>` = debate statements. Every number below was recomputed this round (Fisher values by exact hypergeometric sum).

## Responses to criticisms of V5

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

## Agenda items

### 1. Slot 5: F5 versus F7

**Concede to F7 (V4-4, EL2, one way).** V4 states correctly that my F5 core is the only R1 slot no longer supported (R2-V4:116).

Steelman of my F5 (V5-D1): it is computed once by ember and delivered to n-1 readers, so it scales O(n). It costs 143 s (+23.3%) and +14% tokens (V5:183-184).

Why it loses:
- Its mechanism is "a searcher posts, a reader acts", which is F4's mechanism (R2-V1:26). Two such slots fail the "five distinct" criterion.
- Its net collaboration share is 0.07 (V5:193), the second lowest of my five.
- It is thin whenever ember skips source.md, which happens in 39% of runs (V5:197). Its B5/I1/B2 target survives as the witness sweep kind inside F4.

**Performance check on F7.** F7 costs exactly what F4 costs: luna B 116 + 2 x 2 x 6.4 + 2 = 143.6 s (+23.8%). ember adds 4 posts x 3.2 s, ending at 53.8 s, off the critical path. So A5 (F7) against A4 (F4) differs in message content only, at equal time and equal receiver turns. That is the cleanest possible test of SEED:47.

I accept C = 0.08-0.77 (R2-V3:44, R2-V4:40) and dropping the S13 variant (R2-V4:41: one adjudication answers 1 of 4 cards, gain about 0.02-0.19).

### 2. F1 core, time box and gap card

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

### 3. F4 core and its worst case

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

### 4. F3 grafts

**Concede on V5-D4.** Its Stop block replaces a 2-turn checkpoint with a 3-turn Stop move: 116 + 12.8 + 19.2 + 2 = 150.0 s against 143.6 s. It also rests on the unverified Stop reissue. I keep only its rule "a covered region is never a reason to skip" (V5:343). V1-R1's per-receiver hash order already does the job of my rotating permutation.

I accept the rest of the converged set:
- V2-D4 Task x move cells filled from telemetry;
- V3's leak check on variable fields only;
- the surface filter;
- the V3-R1 resume-digest fallback (147.6 s).

F3 is bounded by its count caps plus the finish signal, so the T_report condition in agenda 3 applies to it as well.

### 5. F6 requests versus uncovered cells

**Concede to the merge** (R2-V1:102). My R1 objection was to covered counts, which act as a clearance signal (V5:130). The merge removes them. An imperative request drawn from an uncovered cell costs sonnet no more turns than a list, since the cap stays at 4 turns (56 s).

Numbers, with V4's precision fix (R2-V4:86):
- worst 330 / 273.7 = **+20.6%**;
- typical 302 / 273.7 = +10.4%;
- headroom 369.5 - 330 = 39.5 s.

That makes F6 the most time-robust mid-run slot.

### 6. Experiment section

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

### 7. Harness share figure

Carry **H = 0.03-0.34 /14 per run, central 0.14**:
- low 0.02 + 0.01 + 0.00 = 0.03;
- high 0.16 + 0.08 + 0.10 = 0.34;
- central 0.08 + 0.03 + 0.03 = 0.14 (V5:147-151).

H-4 is excluded. H-6 is secondary. Leak removal counts 0 on /14 and is a correction to sonnet-panel I7 on control. C and H go in separate columns, and C is conditional on H (A-004).

Two corrections to my own table:
- V5:143 measures H against historical EL2. Replace that with the fresh A0, keeping S07 as context.
- **H is an estimate, not a test.** A0 at 4 runs against A1 at 12 detects about 2.49 x 0.94 x √(1/4 + 1/12) = 1.35 /14, roughly 10x the central H. Only spike 5 (rescoring with the normalizer, judge calls only) measures a row exactly. The spec should say so.

I switch X-001 to V5. V2's own rows sum to 0.10-0.55 (V2:143-147: 0.05 + 0 + 0.05; 0.15 + 0.1 + 0.3), as V2 itself conceded (R2-V2:157).

### 8. Idle-time budgets and the baseline rule

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

## Updated assessment of other variants

- **V1.** Its repairs are the best in the debate: the B_A1 box, one-way F7 and the hook snapshot. Its "worst 150.0 s" for F4 is a typical-path figure, not the finish-signal bound (agenda 3).
- **V2.** Its futility-only interim look and slowdown limit are needed, and its `flag_finding_overlap` alarm is cheap. Its stage-2 arm inherits a reach endpoint that does not fit sonnet panels (agenda 6).
- **V3.** The best auditor this round. It found the HL2 mislabel, which restores V5-D5's +0%, the I7 double count and the drift gap.
- **V4.** It conceded honestly. Its counter on R-24 is correct, and its hang guard and fail-closed seal are the right operational rules. The hang guard is not cap enforcement.

## Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Anchor-text routing + V2-D2 `contradiction` -> M7; V1-R3 gap card as the decoy slot (p = 1/3, kind withheld); V1 box min(35, T0 + 1.30 B_A1 - start); V4 combiner with `phase2_timeout`; V2 sealed-report judging; resumed input tokens logged; HL2 variant = V5-D5 as written (haiku canary, gain to be re-derived) | Only compliance-free hard bound: 147.6 s (+27.2%), hard 150.8 s (+30.0%); HL2 +0%, worst +6.3% |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint locators; V1-R2 harvest incl. sweeper output; V2-D5 witness kind; V5-D3 first-hand rule + 10% stop; 2 facts per luna, no hold; fail-closed hook snapshot + sha256 + V3 timestamp test; sweeper timeout T0 + 85 s; T_report-based finish time | Only cheap I7/T1 path, in ember's idle window; 143.6 s (+23.8%); bound 145.6 + T_report |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move cells from telemetry; V1-R1 hash order; V5-D4 skip rule only; V3 leak check (variable fields); surface filter; V3-R1 resume fallback | No model authors anything; 143.6 s (+23.8%); arm A6 tests exchange vs kit |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Harness-rendered requests from uncovered cells only, ranked by luna's not-checked scope; V1-R5 brief line; V3 leak check; surface filter; no SendMessage | Claude receiver, harness author; worst 330 s (+20.6%), 39.5 s headroom; stage-2 screen |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Hash-split cards, at most 2 per luna; hook snapshot seal; no luna card, no hold; V5 C-3; `PANEL_FINISH_AT`; `flag_finding_overlap` alarm; S13 variant dropped | Same cost as F4, so A5 vs A4 isolates challenge vs findings (SEED:47); 143.6 s (+23.8%); C 0.08-0.77 |

`Proposed base document: V4`

## Per-point positions

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
