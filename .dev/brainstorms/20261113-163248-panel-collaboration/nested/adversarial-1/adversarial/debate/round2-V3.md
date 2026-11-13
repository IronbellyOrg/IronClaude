# Round 2 rebuttal: V3 (haiku, backend lens)

Citations: `V<n>:<line>` = variant files; `R1-V<n>` / `R2-V<n>` = debate statements (line numbers after the colon). I recomputed every number below this round.

## Responses to criticisms of V3

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

## Agenda items

### 1. Slot 5: F5 versus F7

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

### 2. F1 core, time box and gap card

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

### 3. F4 core and its worst case

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

### 4. F3 grafts

| Graft | Position |
|---|---|
| V2-D4 Task x move grain, filled from V4-1 telemetry | **Concede**, moving from V1-R1's region grain. Telemetry fills the cells with no model authoring. |
| V1-R1 per-receiver hash order | Adopt. It does the job of V5-D4's rotation. |
| V5-D4 Stop block | **Concede: reject the block, keep its skip rule.** 116 + 12.8 + 19.2 + 2 = 150.0 s against 143.6 s, and it depends on the unverified Stop reissue. |
| V3 12-character leak check | Keep, on F3 and F6 only. Refinement: compare only the variable fields, never the fixed template text, so that shared template wording cannot produce false positives. It does not apply to F4, where real paths may appear in anchors, or to F1/F7, which carry anchors on purpose. |
| V3-R1 resume digest as a fallback | Keep, used only if spike S0 shows that hooks fail. The same telemetry gaps are delivered at phase-1 exit through `--resume`: 116 + 6 + 25.6 = 147.6 s (+27.2%), inside F1's box rule. |

### 5. F6 requests versus uncovered cells

**Agree with the V1/V2 merge.** The harness renders imperative requests drawn only from uncovered cells, ranked by luna's declared not-checked scope. There are no covered counts and no SendMessage.

The SL2 baseline is 821/3 = 273.7 s, so the cap is 369.5 s. Worst case 274 + 28 + 28 = **330 s (+20.4%)**; typical 302 s (+10.2%).

### 6. Experiment section

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

### 7. Harness share figure

Carry **H = 0.03-0.34 /14, central 0.14**:
- low: 0.02 + 0.01 + 0.00 = 0.03;
- high: 0.16 + 0.08 + 0.10 = 0.34;
- central: 0.08 + 0.03 + 0.03 = 0.14 (V5:147-151).

H-4 is excluded (X-008). Leak removal counts 0 on /14. Spike 5 replaces the normalizer row with a measured value. My 0.8-2.1 is withdrawn.

### 8. Idle-time budgets and the baseline rule

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

## Updated assessment of other variants

- **V1.** It gave the best repairs: the B_A1 box, one-way F7, and withdrawing its own first-Stop delivery. It mislabels the HL2 variant (agenda 2).
- **V2.** Its analyzer corrections (futility-only interim, slowdown limits) are right, and the futility point also corrects my own extension rule. Its gate table marks B1 and I4 exposure as passed because the Task is anchored (V2:85, :92). T2b shows that is wrong at the acceptance-criterion level. It shares the HL2 mislabel.
- **V4.** Its Round 1 fix of V4-2 (144 s, worst 150 s) is the converged block. Its F7 is the right core, but in the one-way EL2 form, without its witness cards. Its I7 row (V4:319) double-counts once the disjoint split is grafted.
- **V5.** "Never wait" and the 12-run controls entered every slate. Its D5 shadow schedule is better than the other advocates credit: +0%, not +21.8%.

## Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Anchor-text routing plus V2-D2 `contradiction` -> M7; decoy slot filled by the V1-R3 gap card (p = 1/3 per slot, kind withheld); box min(35, T0 + 1.30 B_A1 - start); V4 combiner with `phase2_timeout` fallback; V2 sealed-report judging; V5-D5 shadow variant as written (haiku canary) | Sealed by process exit, no hooks. EL2 147.6 s (+27.2%), hard 150.8 s (+30.0%); HL2 238 s (+0%), worst 253 s (+6.3%); C 0.07-0.81 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint ranked locators; V1-R2 harvest including the sweeper's output; V2-D5 witness as a sweep kind; V5-D3 first-hand rule and 10% stop; 2 facts per luna, no hold; hook snapshot seal under `$BOARD` with harness-recorded sha256 and the V3 timestamp test; sweeper `timeout` at T0 + 85 s; atomic writes | Only cheap I7/T1 path. 143.6 s (+23.8%), worst 150.0 s (+29.3%); I7 0.17-0.50 control |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move grain from telemetry; V1-R1 hash order; V5-D4 skip rule only; V3 leak check on variable fields; V4 surface filter; V3-R1 resume digest as the fallback if S0 fails (147.6 s) | No model authors anything. 143.6 s (+23.8%), worst = expected |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Harness-rendered requests from uncovered cells only, ranked by luna's not-checked scope; V1-R5 brief line; V3 leak check; no SendMessage; V4 surface filter | Harness author, Claude receiver. 330 s worst (+20.4%), typical 302 s (+10.2%) |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Hash-split cards, at most 2 per luna; hook seal plus V3 timestamp test; no luna card, no Stop hold; V5 C-3; `PANEL_FINISH_AT`; `flag_finding_overlap` alarm; S13 variant limited to 1 adjudication | Distinct mechanism; answers SEED:47 against slot 2 on the same panel. 143.6 s (+23.8%), worst 150.0 s (+29.3%); C 0.08-0.77 |

Proposed base document: V4

## Per-point positions

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
