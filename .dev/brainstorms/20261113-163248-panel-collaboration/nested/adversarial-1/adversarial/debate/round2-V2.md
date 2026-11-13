# Round 2 rebuttal: V2 (opus, analyzer lens)

Citations: `V<n>:<line>`, `R1-V<n>` = `round1-V<n>.md`, `R2-V1` = `round2-V1.md`, `SEED:<line>` = `../../../seed-brief.md`. I recomputed every number below this round.

## Responses to criticisms of V2

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

## Agenda items

### 1. Slot 5: F5 versus F7

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

### 2. F1 core, time box and gap card

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

### 3. F4 core and its worst case

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

### 4. F3 grafts

| Graft | Position | Reason |
|---|---|---|
| V2-D4 Task x move grain | Adopt (V1 now concedes) | About 25 regex-applicable cells per plan (V2:357). Fill them from V4-1 telemetry (V4:190-195), so no model logs anything (my D4 concession). |
| V1-R1 per-receiver hash order | Adopt | Already gives the two lunas different gaps, which is what V5-D4's rotation was for. |
| V5-D4 Stop block | Reject the block, keep its rule | A Stop move costs 3 turns against 2: 116 + 12.8 + 19.2 + 2 = 150.0 s vs 143.6 s, and it rests on the unverified reissue. Keep "a covered region is never a reason to skip" (V5:343). |
| V3 12-character leak check | Adopt for F3 and F6 | Ground-truth-free, so it complements V4 R-07. It does not apply to F1, which sends anchors on purpose. |
| V4-1 deadline | Keep 110 s | V4's own correction gives 112 s; 110 s is more conservative (R1-V4 concession 9). |

### 5. F6 requests versus uncovered cells

**Adopt V1's merge.** The harness renders imperative requests ("apply M5 to Task 12"), drawn only from V2-D4's uncovered cells and ranked first by luna's declared not-checked scope. There are no covered counts and no SendMessage.

My D4 concession is why covered counts must go: they are a clearance signal (V5 C-2). The V1-R5 brief line and the V4 surface filter stay.

Arithmetic on SL2 (seed sonnet + 2x luna, 821/3 = 273.7 s; cap 369.5 s):
- worst 274 + 28 + 28 = 330 s (+20.4%);
- typical 302 s (+10.2%).

### 6. Experiment section

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

### 7. Harness share figure

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

### 8. Idle-time budgets and the baseline rule

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

## Updated assessment of other variants

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

## Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Anchor-text routing plus V2-D2 `contradiction` -> M7 override; decoy slot filled by the V1-R3 gap card (p = 1/3 per slot, rendered identically, kind withheld); box min(35, T0 + 1.30 B_A1 - start), n from remaining time; V4 combiner; V2 sealed-report judging; V5-D5 HL2 shadow variant with haiku canary | Sealed by process exit, no hooks; 147.6 s (+27.2%), hard 150.8 s (+30.0%) for any T1; C 0.23-0.94 before the act-rate spike |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 disjoint ranked locators; V1-R2 harvest, also on the sweeper's output; V2-D5 witness as a sweep kind; V5-D3 first-hand rule and 10% stop; 2 facts per luna; hook snapshot seal plus sha256 and V3 timestamp test; no hold | Only cheap I7/T1 path; keeps the B5/I1/B2 target; 143.6 s (+23.8%), worst 150.0 s (+29.3%) |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move grain from telemetry; V1-R1 hash order; V5-D4 skip rule only; V3 leak check; V4 surface filter | No model authors anything; 143.6 s (+23.8%), worst = expected; arm A6 tests exchange vs kit directly |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Harness-rendered requests from uncovered cells only, ranked by luna's not-checked scope; V1-R5 brief line; V3 leak check; no SendMessage | Harness author, Claude receiver; 330 s (+20.4%) worst |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Hash-split cards, at most 2 per luna; hook seal; no luna card, no hold; V5 C-3; `PANEL_FINISH_AT`; `flag_finding_overlap` alarm (> 50% adds a gap-card decoy); S13 variant | Distinct mechanism, answers SEED:47 against slot 2; 143.6 s (+23.8%), worst 150.0 s (+29.3%); C 0.13-0.77 |

Proposed base document: V4

## Per-point positions

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
