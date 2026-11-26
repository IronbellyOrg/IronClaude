# Round 2 rebuttal: V1 (opus, architect lens)

Citations: `V<n>:<line>`, `SEED:<line>` = `../../../seed-brief.md`. Every number below was recomputed for this round.

## Responses to criticisms of V1

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

## Agenda items

### 1. Slot 5: F5 versus F7

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

### 2. F1 core, time box and gap card

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

### 3. F4 core and its worst case

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

### 4. F3 grafts

- **Grain: concede to V2-D4 Task x move.** It uses about 25 regex-applicable cells per plan (V2:357). My region x move grid (V1:150) also counts cells where no move applies, and it was fed by model-posted cards. V2-D4's cells can be filled from V4-1's telemetry classifier (V4:190-195), so no model authors anything.
- **Keep V1-R1 per-receiver hash ordering.** It already does what V5-D4's rotating permutation does.
- **V5-D4 Stop block: adopt only its rule** "a covered cell is never a reason to skip" (V5:343). Reject the Stop block itself. A Stop-time move costs 3 turns (V5:339) against 2 for a checkpoint, so it adds 6.4 s: 116 + 12.8 + 19.2 + 2 = 150.0 s against V4-1's 143.6 s. It also depends on the unverified reissue.
- **V3 12-character leak check: adopt** as a hard audit for the content-free slots 3 and 4. It needs no ground truth, so it complements V4 R-07.

### 5. F6 requests versus uncovered cells

Steelman of the opposing side (V2, V3, V4): a request ("apply M5 to Task 12") is more actionable for sonnet than a list.

My position merges the two. The harness renders requests in imperative form. The cells come only from V2-D4's uncovered matrix, ranked first by the cells luna's block declares not checked (V1:454). There are no covered counts, because they act as a clearance signal (V5 C-2; V2's concession 7). No SendMessage is used.

Keep the V1-R5 brief line "peer coverage is not clearance" and the V4 surface filter (V4:563). Arithmetic: 274 + 28 + 28 = **330 s (+20.4%)**; typical 302 s (+10.2%).

### 6. Experiment section

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

### 7. Harness share figure

Carry **0.03-0.34 /14 per run (central 0.14)**, V5's bottom-up sum (V5:147-151): low 0.02 + 0.01 + 0.00 = 0.03, high 0.16 + 0.08 + 0.10 = 0.34.

- **Control I7:** 0 for cheap panels. For sonnet panels the leak removal lowers measured I7 by up to about 2 of 9 credits. That is a measurement correction, not a gain.
- **H-4 is excluded** (X-008). V5's table never counted it, so the range does not change.
- **H-6** is a secondary score only.
- Spike 5 replaces the normalizer row with a measured value before any arm runs.
- Per A-004, C is reported conditional on H and is never added to H.

### 8. Idle-time budgets and the baseline rule

The rule has five parts:

1. **The named baseline is B_A1**, the per-package median of A1 (harness-fixed and isolated), measured in spike 4 and in arm A1. The H fixes ship regardless, so A1 is the isolated panel that a collaboration design actually replaces. V1 (V1:592) and V2 (V2:528) already use this baseline. Historical S07 (116 s) appears only as the planning value in the spec's arithmetic, labelled as such, and every block is re-derived at the spike-4 value.
2. **In-run deadlines use B_A1:**
   - `PANEL_FINISH_AT = T0 + 1.20 B_A1`;
   - the phase-2 deadline is `T0 + 1.30 B_A1`.
3. **The catalogue's own time counts against a design.** If spike 4 shows A2 > 1.10 x A1, design arms do not carry the full kit. Their injected moves are their only catalogue content.
4. **The cap check:** median per package <= 1.35 x B_A1, and no package > 1.5 x (V2:528). V4's SLO budget (R-24) applies across packages.
5. **Mid-run designs (slots 2, 3, 5) cannot be killed** without losing the report. Their bound comes from the count caps plus the finish signal, and the SLO budget audits it.

## Updated assessment of other variants

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

## Revised final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 flip row and decoy ratio, the decoy slot filled by the V1-R3 gap card (p = 1/3, rendered identically); box min(35, T0 + 1.30 B_A1 - start) with n from the remaining time; V2 sealed-report judging; V5-D5 HL2 shadow variant with a haiku canary | Sealed by process exit, no hooks; 147.6 s (+27.2%), hard 150.8 s (+30.0%) for any T1 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V1-R2 automatic harvest, also applied to the sweeper's own output; V2-D1 disjoint locators; V2-D5 source-rule witness as a sweep kind; V5-D3 first-hand rule and 10% stop; 2 facts per luna, hook-side transcript seal, no Stop hold | Only cheap I7/T1 path, uses ember's idle time; 143.6 s (+23.8%), worst 150.0 s (+29.3%) |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | V2-D4 Task x move cell grain from telemetry; V1-R1 per-receiver hash order; V5-D4 "covered is never a reason to skip"; V3 12-character leak check; V4 surface filter | No model authors anything; 143.6 s (+23.8%), worst = expected |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 (274 s) | Harness-rendered move requests (V1-R5 semantics, no SendMessage) drawn from V2-D4 uncovered cells, ranked by luna's not-checked scope; no covered counts; V1-R5 brief line; V3 leak check | Harness author, Claude receiver; 330 s (+20.4%) worst |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, re-based to EL2, one way (ember flags, lunas adjudicate) | Hash-split cards, at most 2 per luna; hook-side seal; no luna posting and no Stop hold; V5 C-3 first-hand rule; `PANEL_FINISH_AT`; S13 kept as a variant | Distinct mechanism; answers SEED:47 against slot 2 on the same panel; 143.6 s (+23.8%), worst 150.0 s (+29.3%); C 0.13-0.77 |

Shared substrate: V4 board with the baked-in path, kill switch, `collab.json` and SLO; V1 `PANEL_FINISH_AT` on B_A1; V2's no-free-text rules (forbidden keys, located quote, existing paths) applied over V4's `panel-msg/1` size caps; V4's relative alarm (J + 0.15 or ledger rows -20%) plus a per-design echo threshold.

`Proposed base document: V4`

## Per-point positions

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
