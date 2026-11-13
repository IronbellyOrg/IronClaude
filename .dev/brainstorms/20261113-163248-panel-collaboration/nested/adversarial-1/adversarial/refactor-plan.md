# Refactoring Plan: Merge into Base (Variant 4)

## Overview
- Base: Variant 4 (`variant-4-original.md`, opus:devops). Selection evidence: `base-selection.md`.
- Incorporating strengths from: Variant 1 (opus:architect), Variant 2 (opus:analyzer), Variant 3 (haiku:backend), Variant 5 (sonnet:performance).
- Planned changes: 22 (grouped by target section of the base).
- Risk level: Medium overall (most changes modify existing base text; no section is removed; the five-section structure and V4's redesign numbering are kept).
- Authority for every rule below: the Round 2 consensus (`debate/round2-tally.md`, 43/43 points), the Round 3 closures of INV-001..INV-008 (`debate/round3-tally.md`), and the MEDIUM items closed in `debate/round3-V1.md:36-41`, `debate/round3-V2.md:29-33` and `debate/round3-V4.md:42-49`. Where a change says "text of R3-V1 INV-00n", the merge copies the "Exact rule" cell of that row in `debate/round3-V1.md` (or `round3-V2.md`), adapted to the spec's voice, without changing numbers.
- Citation keys used below: `V<n>:<line>` = `variant-<n>-original.md`; `R2-V<n>:<line>`, `R3-V<n>:<line>` = `debate/round<k>-V<n>.md`; `INV-0nn` = `invariant-probe.md`; `AG` = `debate/round3-agenda.md`.

### Global decisions (orchestrator, recorded with rationale)

1. **Slate.** Exactly five redesigns, one per family, all with V4 cores: Redesign 1 Move Radar = F3; Redesign 2 Idle-Shift Sweeper = F4; Redesign 3 Axis-Flip Challenge = F1; Redesign 4 Flag-and-Adjudicate = F7; Redesign 5 Coverage Deflection = F6 (5/5 in Round 3; F6 kept, F2 rejected under the distinctness criterion, INV-006). V4's numbering is kept so the base's internal references stay valid; each heading gains its family label.
2. **Baseline naming.** V4's "A0" (isolated panel with harness fixes) is renamed A1 everywhere; A0 becomes the fresh current-harness arm (R2-V4:109, C-010). Named isolated baselines: EL2 = ember + 2x luna, 116 s per package at planning (348/3); HL2 = haiku + 2x luna, 238 s (715/3); SL2 = sonnet + 2x luna, 273.7 s (821/3); per-package historical medians from AG:13-16 are shown beside them (A-005). The cap is per package against the measured A1 median, B_A1 (R-24).
3. **Central k.** Gain and time rows for F3, F4 and F7 are given at k = 1 (central) and k = 2 (optimistic), both labelled planning values superseded by Spike 4's per-package k (4/5 in Round 3). Planning rule for the k = 1 gain row: each luna receives one item instead of two, so each per-issue row is scaled by 0.5; the spec labels this a planning assumption replaced by the arm's logged delivered-slot counts (V3's objection to plain halving, R3-V3:20, is recorded as the reason it is labelled, not hidden).
4. **F6 gain re-derivation (INV-021).** The old 0.26-1.06 (V4:584-594) was derived on S14 with covered-count cards. On SL2 the scouts are two lunas (no ember) and the cards carry uncovered-Task requests only. Planning re-derivation: high = the V4 rows (1.06) at k = 2; low = V4 low rows x 0.5 (thinner luna-only coverage, one card per scout exit at most) = 0.13; k = 1 row = 0.07-0.53. Labelled planning; the stage-2 screen (INV-020) decides. H share for SL2 is carried as V4's +0.1 to +0.4 marked UNVERIFIED (no bottom-up SL2 table exists).
5. **F3 collaboration share (INV-007).** C is re-derived from ember's search-move rows only (V4:241-247): I4 0.05-0.20, I5 0.02-0.10, B8 0.03-0.10, B6 0.02-0.08, so gross 0.12-0.48 at k = 2 and 0.06-0.24 at k = 1; net of the static kit the low end is 0. Luna's reading-move rows (B1/B2, B5/I1, I6: 0.08-0.40) are booked to the prompting share (A2). I7 0.10-0.40 control (M1, ember) stays.
6. **F4 and F7 at k = 1.** F4 C 0.14-0.67 (k = 2) -> 0.07-0.34 (k = 1); I7 0.17-0.50 -> 0.09-0.25 control. F7 C 0.08-0.77 (k = 2) -> 0.04-0.39 (k = 1).

## Planned Changes

### Change 1: Front matter, provenance and reading guide (orchestrator)
- **Source**: Global decisions 1-2; V5:21-31 style of named shares.
- **Target**: Base title block and introduction (V4:1-21) (replace).
- **Rationale**: The merged document is the converged requirements specification, not "variant 4"; the arm renaming must be stated once at the top (R2-V4:109).
- **Integration point**: New H1 title without "variant 4"; provenance header comments; a short "How to read" list: slate table (5 rows: slot, family, redesign, panel, baseline), arm names A0-A6, the meaning of B, B_A1, B_f, T0, turn_p90, T_report_p90, k, n, C, H, P (prompting share).
- **Risk**: Low - additive.

### Change 2: Theories: gate funnel plus T2a/T2b plus T1 complementarity (V2, V5, V1)
- **Source**: V2:9-94 (three-gate funnel and per-issue gate table, S-003, U-004); V5:40 (T2a/T2b split, C-002); V1:25-45 and V2:27 (searcher/reader complementarity with luna's 48/48 vs 11/48 source.md evidence, C-001, U-007).
- **Target**: Base §1 (V4:22-87) (insert/restructure).
- **Rationale**: S-003 V2 5/5, C-002 V5 5/5, C-001 V1 5/5 (Round 2 and Round 3 tallies).
- **Integration point**: Keep V4's three refined theory paragraphs. Add to T1 the complementarity refinement and its evidence; split T2 into T2a (right place, one question) and T2b (region never reached: B1, B2, I4, I6); add the gate-funnel table (exposure, question, survival) per missed issue before V4's mapping table, and mark which gate each redesign targets. X-003 (GT6 = I1) and X-002 (leak removal changes 0 on /14, lowers sonnet-panel I7 only) are stated as in V4.
- **Risk**: Medium - modifies theory text that later sections cite.

### Change 3: Harness bundle H1-H4 rewritten (V1, INV-002, INV-009, INV-010, V4 R3)
- **Source**: V1:102-111 (H2 = truncate anchors to 200 and claims to 300, parser-validate, re-ask once via resume; grading and judge held constant, sha256-pinned; C-003, X-008, X-009); INV-002 (text of R3-V1 INV-002); INV-009, INV-010 (R3-V1:36-37); R3-V4:42-47 (retry loop and hang-guard symmetry).
- **Target**: Base §2.0 harness block (V4:160-184) and R-01..R-05 (replace).
- **Rationale**: C-003 / X-009 / X-008 V1 5/5; INV-002 closed 5/5; MEDIUM rules adopted without objection.
- **Integration point**: H1 name source.md in the brief; H2 V1's truncate-validate-re-ask; H3 base-commit sandbox; H4 remove `.dev/reflect` (and the leak dirs); grading constant. Add: one phase-2 deadline T0 + 1.30 B_A1 covering resume, fallback, challenges and re-ask; re-ask skipped without room for one start plus one turn; `reask_s` logged in every arm, included in elapsed; every arm (A1 included) drops `--no-session-persistence`; the phase-1 re-ask finishes before the seal and `p1.md` is the post-re-ask report; elapsed sums all attempts of run-reviewer.sh's retry loop (`attempts`, `retry_s`) and in a collaboration arm attempt 2 runs with `PANEL_COLLAB=0` (`retry_isolated`); one hang guard T0 + 1.5 B_A1 in every arm including A1 (`hang_kill`).
- **Risk**: Medium - touches every arm's launch command; R-05's allowed-difference list must change in step (Change 19).

### Change 4: Shares H, P and C, never summed (V5, V4)
- **Source**: V5:141-153 (three shares, X-001 bottom-up H 0.03-0.34, central 0.14; C-009); V4:184 (H-C interaction, A-004); V5:106, :433 (Spike 5, U-018).
- **Target**: Base §2.0 "H share" text (V4:172-184) (replace).
- **Rationale**: X-001 V5, C-009 V5, A-004 V4, all 5/5.
- **Integration point**: Define H = A1 - A0, P = A2 - A1 (static kit, prompting share), C = arm - A2 (collaboration share), C conditional on H. Carry H = 0.03-0.34 /14 per run (central 0.14) for cheap panels. Every gain block shows C and H in separate columns and never sums them; gap-card findings (F1) and luna's F3 injections are booked to P. Spike 5 re-scores 30 cheap runs with the normalizer to measure part of H.
- **Risk**: Low.

### Change 5: Message rules (V2, V4, INV-005 exception)
- **Source**: V4:108-117 (`panel-msg/1`, anchors 12-200 characters, exact and located); V2:116-131 (located verbatim quote rule, forbidden keys); X-007 V2; INV-005 (R3-V2 text, clause 1).
- **Target**: Base §2.0 schema block and §5.2 (V4:108-117, :698-707) (modify).
- **Rationale**: C-005 V4, X-007 V2, INV-005 closed 4/5.
- **Integration point**: No free-text field in any message kind; forbidden keys enumerated; the only exception is F7 `kind:"card"` lines from ember, which may carry the `category` and `severity` enum values (never `claim`, never `blocking`); the R-06 validator enforces this; cards beyond 2k are rejected and logged `over_cap`.
- **Risk**: Low.

### Change 6: Independence, seals and peer tagging (V4, INV-012, INV-031)
- **Source**: V4:122, :286 (seal); R2-V4:73-74 (fail closed on seal, fail open on review); INV-012 (R3-V1:39).
- **Target**: Base §2.0 seal text (V4:118-130) (modify).
- **Rationale**: C-006 V4 5/5; INV-012 MEDIUM closed in Round 3.
- **Integration point**: Phase designs seal by process exit. Mid-run designs seal by a hook-side transcript snapshot written under `$BOARD` with sha256 recorded by the harness; snapshot or hash failure delivers nothing and logs `snapshot_missing`; a hook error never kills a review. In mid-run arms the harness tags a finding `peer` when its anchor overlaps a delivered anchor by at least 12 characters or a delivered locator is in its refs. Alarms based on "own sealed findings per run" are removed; the timestamp test is an integrity log only.
- **Risk**: Medium - removes alarms the base used in Redesigns 2 and 4.

### Change 7: Convergence alarm on own lines (V4, INV-004, INV-018)
- **Source**: V4 R-25 and V4:234 (relative alarm); INV-004 (R3-V1 text); R2-V2:148 (at most 2 of 12 runs guard); INV-018 (R3-V1:41).
- **Target**: Base §2.0 alarm text and R-25 (modify).
- **Rationale**: C-007 V4 5/5; INV-004 closed 5/5.
- **Integration point**: CONVERGENCE alarm = own-line Task Jaccard (`origin:"own"`, phase-1 or pre-delivery, excluding P2-F and peer-tagged lines) above the A1 mean + 0.15 (baselines ember+luna 0.25, luna+luna 0.33, so 0.40 / 0.48), or ledger rows -20%; per-design ECHO on real-anchor slots only (> 30% F1, > 60% F4); an arm passes the independence guard if the alarm fires in at most 2 of 12 runs. `flag_finding_overlap` > 50% (F7) stops and reports the arm, never changes the treatment mid-arm. R-23 gains `own_line_jaccard`; `pairwise_task_jaccard` stays descriptive.
- **Risk**: Medium.

### Change 8: Panel timing rules (V1, V2, V3, V4, V5, INV-001, INV-008)
- **Source**: INV-001 (text of R3-V1 INV-001); INV-008 (text of R3-V1 INV-008 with R3-V2's thresholds); R2-V1:139-147 (five-part rule); R2-V2:176-187 (per-slot slowdown limit); R2-V3:162-168 (drift band); R2-V4:108 (measure slowdown on the critical-path role); V5:411 and A-002 (static kit priced at about +29%); X-005 V1 (slowest luna sets B); INV-024 (baked settings).
- **Target**: Base §2.0 timing constants and baseline tables (V4:131-158) (replace).
- **Rationale**: C-013 V1, A-002 V5, A-005 V5, X-005 V1 5/5; INV-001 and INV-008 closed 5/5.
- **Integration point**: State once: (1) `PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90` (143.8 s at B = 116, turn and report 6.4 s); (2) `k = max(0, min(2, floor((0.35 B_A1(pkg) - hooks - turn_p90 - T_report_p90) / (2 x turn_p90))))`, hooks = 2 s, with the threshold table (k = 2 needs T_report_p90 <= 6.6 s at B = 116, 8.0 s at 120, 8.7 s at 122, 1.0 s at 100; k >= 1 needs <= 19.4 s at 116, 13.8 s at 100; F6: <= 23.8 s and <= 51.8 s); (3) every mid-run design states three numbers: planned end, finish-signal bound (T0 + 1.35 B_f), enforced ceiling (hang guard 1.5 B_A1 = `SLO_BREACH`); (4) for slots 2-5 the +35% cap is audited by the SLO budget (R-24: 1 package in 12 over 1.35 B_A1 stops the arm), not enforced; only F1's phase-2 end is enforced by a kill; (5) V1's five-part rule, V2's per-slot slowdown limits (F4/F7 5.7%, F3 11.2%, F6 14.6%) measured on the critical-path role, V3's drift band (lower edge 1.30/1.35 = 0.963); (6) Spike 4 writes a per-package values file (B_A1, turn_p90, T_report_p90, PANEL_FINISH_AT, k) committed with its sha256 before the first arm and never recomputed during an arm; (7) log `finish_would_fire` in A1 and A2 as the counterfactual truncation rate; (8) T0, PANEL_FINISH_AT, board path and reviewer id are baked into each reviewer's `--settings` JSON; hooks read nothing from the environment; (9) every "+x%" is labelled valid at its stated B and k. Add the per-package table from AG:11-16 beside the planning baselines.
- **Risk**: High - every redesign's time block depends on it; done before Changes 10-14.

### Change 9: Move catalogue: observable signatures and c-values (V4, INV-007, V5)
- **Source**: V4:95-106 (M1-M10 with best-style column, C-004); INV-007 (R3-V1:31 plus R3-V2:23); V5:83-94 (per-move c as ceiling, U-015, A-011).
- **Target**: Base catalogue table (V4:95-106) (modify: add two columns).
- **Rationale**: C-004 V4, A-011 V5 5/5; INV-007 closed 5/5.
- **Integration point**: Column "observable tool-call signature": M1 grep over tests/ with a plan-edited path; M7 repo-wide search including root files; source.md opened; unnamed test opened; M2 and M4 get a listed signature or "unobservable"; M3, M5, M6, M8, M9, M10 "unobservable" (never described as "not done by any panel member"). Column "c ceiling" from V5 mapped to V4 ids. Gain rows for never-found issues (B1, B2, I5, I6) have low end 0 (A-011).
- **Risk**: Low.

### Change 10: Distinctness criterion and slate table (INV-006, R3-V1, R3-V2)
- **Source**: R3-V1:30 (triple criterion), R3-V2:22 (move-only F3); R2-V4:32 (why F5 is evicted).
- **Target**: Base §2 introduction, before Redesign 1 (insert).
- **Rationale**: INV-006 closed 5/5; move-only F3 4/5.
- **Integration point**: State the criterion (content source, content form, delivery point; distinct when they differ in at least 2 of 3), the five triples, the pairwise check, and why F5 (0 of 3 from F4) and F2 (at most 1 of 3 from F7) are not in the slate.
- **Risk**: Low - additive.

### Change 11: Redesign 3 Axis-Flip Challenge = F1 (V4-3 core plus grafts)
- **Source**: V4:343-460; R2-V4:45-63 (box, gap card, HL2 shadow, gain table); INV-003 (text of R3-V1 INV-003); INV-004 (balanced deal, R3-V2:21(3)); INV-013, INV-014, INV-022 (R3-V1:40, R3-V3:26); V2-D2 `contradiction` -> M7 (I6 route, R2-V2:13); V2 sealed-report judging (V2:517, U-006); V5-D5 (V5:350-392, X-004, U-016).
- **Target**: Base Redesign 3, all subsections (a)-(h) (modify).
- **Rationale**: Slate slot 1 5/5; X-011 V5, A-006 V2, A-003 V2, X-004 V5 5/5; INV-003 closed 5/5.
- **Integration point**: (b) schedule: phase-2 box `box = min(35, T0 + 1.30 B_f - t_launch)` and `n = max(0, min(cap, floor((box - start_cost)/(2 x turn_p90))))`, start_cost 6 s resume / 16 s fresh fallback, recomputed after a failed resume; n = 0 means no launch; anchors dealt to the two lunas by the balanced online deal (recipient (i + r) mod 2); each slot holds the gap card with p = 1/3, seeded per receiver, kind withheld; zero real anchors: the package behaves as isolated for real slots and ECHO is "not applicable"; gap cards only where an eligible never-anchored trigger region exists. (c) transport: process exit plus `claude -p --resume` with `--output-format stream-json --verbose` on phase-2 and re-ask sessions; spike S2 checks streaming on luna. (d) time: luna A 95 + 6 + 25.6 = 126.6 s; luna B n = 2 147.6 s (+27.2%), n = 1 134.8 s (+16.2%) whenever turn_p90 > 7.2 s; fallback detected at 2 s gives n = 1 and 146.8 s; ember 141.2 s; phase-2 end hard-bounded at T0 + 1.30 B_A1 = 150.8 s (+30.0%); panel elapsed = max(T1, deadline); HL2 variant = V5-D5 as written (+0%, worst 253 s = +6.3%, haiku isolated canary). (e) contamination: own-line alarm, ECHO on real slots, decoys, sealed-report judging on the post-re-ask `p1.md` under random labels. (f) gain: C 0.06-0.63 /14 (R2-V4 steps minus the gap route); gap route 0-0.10 in P; I7 0.05-0.20 control; H column separate. (g) effort per V4 plus stream-json parse. (h) runbook rows: `phase2_timeout` keeps every complete parser-valid streamed P2 line (`p2_lines_salvaged`); `resume_fallback`; INV-011 session cleanup only of run-recorded ids. Drop V4's haiku-anchor variant (R2-V4:21) and the 45 s / 35 s timeouts.
- **Risk**: High - largest rewrite; keep the base's (a)-(h) skeleton.

### Change 12: Redesign 2 Idle-Shift Sweeper = F4 (V4-2 core plus grafts)
- **Source**: V4:274-342; R2-V4:65-78; V2-D1 disjoint ranked locators (V2:151-216); V1-R2 harvest including sweeper output (V1-R2, U-002); V2-D5 witness as a sweep kind (R2-V4:19); V5-D3 first-hand rule and 10% re-run mismatch stop (V5:299, U-017); INV-008; INV-015, INV-016 (R3-V4:49, R3-V3:27).
- **Target**: Base Redesign 2, (a)-(h) (modify).
- **Rationale**: Slate slot 2 5/5; INV-008 closed 5/5.
- **Integration point**: Facts per luna = k (planning k = 1 central, 2 optimistic); locators dealt by the balanced online deal; no luna seal turn (hook snapshot instead); no Stop hold; late facts logged `late` and dropped; sweeper timeout = PANEL_FINISH_AT - T0 - 2 x turn_p90 (not 85 s) and its actual start logged; a count fact with n = 0 is never delivered as clearance (rendered only as the command to re-run); facts may be cited only after the receiver's own transcript re-ran the command. Time: planned 116 + 2 + 12.8 = 130.8 s (+12.8%, k = 1) or 143.6 s (+23.8%, k = 2); finish-signal bound 156.6 s (+35.0%); ceiling 174 s (+50%, `SLO_BREACH`); sweeper 79 s off the path. Gain: C 0.07-0.34 (k = 1) / 0.14-0.67 (k = 2); I7 0.09-0.25 / 0.17-0.50 control; H separate. Strike "worst 150.0 s".
- **Risk**: Medium.

### Change 13: Redesign 1 Move Radar = F3 (V4-1 core plus grafts)
- **Source**: V4:188-273; INV-006 (move-only), INV-007; V1-R1 per-receiver hash order (V1:148-231); V5-D4 skip rule only (R2-V4:82); V3 leak check on variable fields (V3:88, U-009); global decision 5.
- **Target**: Base Redesign 1, (a)-(h) (modify).
- **Rationale**: Slate slot 3 5/5; INV-006, INV-007 closed 5/5.
- **Integration point**: Injection names a move id only (plus a Task only when the triggering tool call's path names one; that Task stays in `metrics/<rid>.jsonl`, never in the message). "No panel member has done this yet" is used only for observable moves (ember's M1, M7, and M2/M4 if they get signatures) and for the "source.md never opened" check; luna's reading-move injections are a timed static prompt booked to P. Count per reviewer = k. Deadline expressed as a formula in B. Time: same three-number block as F4 (130.8 / 143.6 s planned, bound 156.6 s, ceiling 174 s). Gain per global decision 5; A6 vs A2 is read as "telemetry-timed kit vs static kit". Strike "worst = expected".
- **Risk**: Medium.

### Change 14: Redesign 5 Coverage Deflection = F6 on SL2 (V4-5 core plus grafts)
- **Source**: V4:539-611; R2-V4:84-86; INV-006 (R3-V1:30, R3-V4:29); INV-008; V1-R5 brief line (V1); U-014 surface filter; global decision 4.
- **Target**: Base Redesign 5, (a)-(h) (modify).
- **Rationale**: Slate slot 4 5/5; C-012 V1 (every design on a seed baseline); INV-006 and INV-021 closed.
- **Integration point**: Panel SL2 (sonnet + 2x luna), baseline 273.7 s per package. Trigger: each luna scout's exit; its findings block yields (Task, category) of non-surface findings; the harness renders requests for Tasks with no peer finding, ranked by the lunas' declared not-checked scope; no counts, no telemetry, no SendMessage; at most k requests per card computed with sonnet's turn_p90 and T_report_p90 (turn 14 s). Time: planned 273.7 + 2 + 28 = 303.7 s (+11.0%, k = 1) or 331.7 s (+21.2%, k = 2); bound T0 + 1.35 x 273.7 = 369.5 s; ceiling 410.6 s; runs only if Spike 4 gives sonnet T_report_p90 <= 51.8 s. Deflection alarm kept (sonnet's anchored Tasks overlapping the covered list > 50%, or union shrink vs A1-SL2). Gain per global decision 4 (k = 1 0.07-0.53, k = 2 0.13-1.06, planning); I7 -0.20 to +0.20 control; H separate (UNVERIFIED +0.1 to +0.4). Replace S14 and 225 s everywhere.
- **Risk**: Medium.

### Change 15: Redesign 4 Flag-and-Adjudicate = F7 (V4-4 core, EL2, one way)
- **Source**: V4:461-538; R2-V4:28-43; INV-005 (text of R3-V2 INV-005); INV-017, INV-018, INV-023; V5 C-3 first-hand rule.
- **Target**: Base Redesign 4, (a)-(h) (modify).
- **Rationale**: Slate slot 5 5/5; INV-005 closed 4/5.
- **Integration point**: Panel EL2, one way: ember flags checkable sentences (AC, quantifier, grep, mapping) as cards from its 3rd tool call, at most 2k cards; lunas adjudicate; no luna card, no Stop hold. Card i (board append index) goes to luna (i + r) mod 2; its form is challenge when (i + floor(i/2) + c) is even, finding otherwise; r, c seeded coins logged. Challenge form = anchor + required finite check; finding form = anchor + ember's category and severity enums. Logged per slot: form, recipient, conversion (receiver's line overlaps the card anchor by >= 12 characters), judge-credited and uncredited conversion, card Task (INV-017 falsifier: cards spent on early Tasks). Pre-registered secondary analysis: conversion by form, two-proportion test, run-paired difference; at most 144 cards. State that A5 vs A4 compares two whole designs (sender session, content source, move type and target issues differ). Time: as F4 (130.8 / 143.6 s planned; ember 41 + 4 x 3.2 = 53.8 s off the path). Gain: C 0.04-0.39 (k = 1) / 0.08-0.77 (k = 2); designSpec rows (B5, I1, I4) depend on k >= 1 there; I7 0-0.10. Drop the S13 variant and the Stop hold. Strike "A5 vs A4 answers SEED:47" and "worst 150.0 s".
- **Risk**: Medium.

### Change 16: Comparison table (V5 columns, V4 I7 column)
- **Source**: V5:400-413 (net collaboration share, tokens per added issue, static-kit row, sonnet reference row; S-004); V4:614-626.
- **Target**: Base §3 (replace table).
- **Rationale**: S-004 V5 5/5.
- **Integration point**: One row per redesign (in slot order F1, F4, F3, F6, F7, keeping V4 redesign numbers in a column) plus a static-kit (A2) row and the isolated baselines; columns: panel and baseline; planned elapsed (k = 1 / k = 2 or n); finish-signal bound; enforced ceiling; C /14 (k = 1 / k = 2); P; H; I7 control /2; output tokens overhead; tokens per added issue; contamination risk; effort; reliability. Remove "+0.2 to +0.6 H" and all "worst" guarantees.
- **Risk**: Medium - numbers must match Changes 11-15.

### Change 17: First experiment (V2 plan, V5 screen, INV-019, INV-020)
- **Source**: R2-V2:118-148 (arms, sizes, endpoint, futility-only interim, familywise bound); R2-V4:90-96; R3-V2:30-32 (decision table against observed A1 reach, stage-2 screen); V2:531 (confirmation on two new packages, A-009); INV-005 (secondary analysis); V5 block randomisation.
- **Target**: Base §4 (V4:630-684) (replace).
- **Rationale**: C-010 V2, C-011 V2, X-013 V2, A-009 V2 5/5; INV-019, INV-020 MEDIUM closed.
- **Integration point**: Gate 0 spikes (S0 hooks fire, S2 resume plus streaming, S3 full-chain smoke with 0 dropped lines and stream-json parse, REQ-S3 act rate incl. "finish now", Spike 4 values file, Spike 5 re-score). Arms on EL2: A0 fresh current harness (4) plus S07 context; A1 isolated + H (12); A2 + static kit (12); A3 F1, A4 F4, A5 F7, A6 F3 (6, extended to 12). Stage 2 on SL2: A1-SL2, A2-SL2, F6 arm with V5's screen (hard credits per run, one-sided permutation p < 0.05, margin over A2-SL2 >= 1/3 of runs). Endpoint: target reach; one-sided Fisher at the final look only, decision table against observed A1 reach (0/12 -> X >= 4/12, p = 0.047; 1/12 -> 6/12, p = 0.034; 2/12 -> 7/12, p = 0.045); X must also beat A2 by >= 4 runs; interim look futility only; familywise bound 0.20, adoption only after 12-run confirmation on two new packages. Size 76 max / 52 min plus 30 in stage 2. Conduct: `NOFALLBACK=1`, at most 10 concurrent runs and 4 ember, `model_ok`, block-randomised order, same blind judge. State that the plan cannot detect the central estimates (INV-019) and why it is still run (screen).
- **Risk**: Medium.

### Change 18: Requirements for all five redesigns (V4 tables extended)
- **Source**: V4:686-746 (R-01..R-30, verification column, S-005); Changes 3-17.
- **Target**: Base §5 (modify and append).
- **Rationale**: S-005 V4 5/5; the merge target requires numbered testable requirements covering the chosen designs; the experiment now runs all five.
- **Integration point**: Retitle §5 to cover the shared substrate and all five redesigns. Update R-01..R-30 in place for every rule above (keep ids). Add §5.x subsections for Redesign 1 (F3), Redesign 4 (F7), Redesign 5 (F6) and new ids from R-31 upward, each with a verification column, including: k values file (R-30), stream-json salvage, balanced deal, card-form contrast, finish signal, hang guard in every arm, retry accounting, own-line alarm, observable-signature list, F6 trigger on scout exit.
- **Risk**: Medium.

### Change 19: Kill switch and `collab.json` schema (V4 R-05, R-23, R3-V4)
- **Source**: V4:139, R-05, R-23; R3-V4:48, :57-63.
- **Target**: Base R-05, R-23 (modify).
- **Rationale**: U-011 V4; MEDIUM rules adopted.
- **Integration point**: R-05's allowed differences become R-01 and R-03, removal of `--no-session-persistence`, stream-json on phase-2 and re-ask sessions, the common hang guard; the kill switch restores the isolated panel with H, not today's panel. R-23 gains `reask_s`, `attempts`, `retry_s`, `phase2_timeout`, `p2_lines_salvaged`, `n_planned`, `n_launched`, `k`, `panel_finish_at`, `finish_signal_t`, `finish_would_fire`, `hang_kill`, `snapshot_missing`, `late`, `over_cap`, `slot_type`, `card_form`, `deal_r`, `deal_c`, `own_line_jaccard`, `retry_isolated`. INV-011: cleanup deletes only session ids recorded in that run's `collab.json`, after every concurrent run on that sandbox ends, never the directory; `git status` is checked after the last such run.
- **Risk**: Low.

### Change 20: Act rate tied to a spike (V1, A-001)
- **Source**: V1:614 (REQ-S3); A-001.
- **Target**: Base gain-model text and each (f) block (modify).
- **Rationale**: A-001 V1 5/5.
- **Integration point**: Every act-rate factor (0.5-0.85) is labelled planning and replaced by REQ-S3's measured act rate, including the act rate on "finish now".
- **Risk**: Low.

### Change 21: Itemised unverified list (V5, S-006)
- **Source**: V5:538-545; V4:750-759; R3-V2 (T_report_p90).
- **Target**: Base closing section after §5 (V4:747-759) (replace/extend).
- **Rationale**: S-006 V5 5/5.
- **Integration point**: One row per unmeasured number used in the spec (T_report_p90, turn_p90 per model, act rates, resume on gateway ids, stream-json before exit, hook env, per-package B_A1 after H, static kit cost +29%, k = 1 gain scaling, F6 SL2 re-derivation, SL2 H share), with the spike that replaces it.
- **Risk**: Low.

### Change 22: Read-only enforcement statement (V4, A-008)
- **Source**: V4 R-09 (helpers write only under `$BOARD`), A-008.
- **Target**: Base §5.5 (modify).
- **Rationale**: A-008 V4 5/5.
- **Integration point**: State that Bash is unrestricted, so read-only is enforced by audit: helpers write only under `$BOARD`, a clean `git status` after the last run on a sandbox, candidate hash checked.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| S-005 | V1 REQ-* ids, V2 R-n bullets, V3 generic list 1-21, V5 grouped H-/B-/S-/C- ids | V4's R-01..R-30 tables with a verification column won 5/5; V3's list is not tied to design behaviour |
| C-005 | V2 400-byte messages with 120-char quotes; V5 `note` <= 120 chars | V4's 12-200-character anchors fit F1's anchor text (V2 conceded, R2-V4:146); V5's note carries conclusions (X-007) |
| C-006 | V1/V5 call-count gate (6th tool call) | A call count produces no auditable artifact; process exit or a fail-closed snapshot does (5/5) |
| C-007 | V3 absolute Jaccard > 0.5; V5 any pair >= 0.70 | Relative, ground-truth-free alarm won 5/5; V3's absolute threshold fires on noise in haiku panels |
| C-008 | V5 fixed 0.25x / 2x band; V3 aggregated factors | Per-issue chains (V4) are tied to B1-B8/I1-I8 as the seed requires |
| X-001 | V3 harness share 0.8-2.1 | Above every other variant's high end; V5's bottom-up 0.03-0.34 won 5/5 |
| X-006 | V3 collaboration findings outside the findings block | They would never be scored; one block with P2-F ids won 5/5 |
| X-008 | V5 H-4 (MINOR notes in the block) and H-6 (judge scores raw union) as harness changes | Grading and judge held constant (V1); H-6 may be reported as a secondary score only |
| X-010 | V3 no static-catalogue arm | Cannot separate catalogue content from exchange; A2 is the comparator (V5) |
| X-012 | V3 I7 counted on /14 | I7 stays on control /2 (V1, all others) |
| Slate slot 5 | F5 structural index / source-rule witness (V1-R1/V2-D5/V5-D1 cores) | Its mechanism is F4's (helper session, facts, mid-run): 0 of 3 triple differences; the witness survives as an F4 sweep kind |
| INV-006 | Replace F6 with F2 mid-run method relay | F2 differs from F7 in at most 1 of 3; I6 keeps a route via F1's `contradiction` -> M7 |
| INV-001 | Probe's `min(1.20 B, ...)` finish signal; V1's original 1.20 B (U-001) | Fires on the planned path at k = 2 (139.2 s < 143.6 s); conceded by V5 (R3-V5) |
| INV-005 | Probe's finding form with ember's free-text claim; V1's dealing clause | Free text violates X-007; V1's clause confounds luna with form |
| R2-V4:21 | V4-3 haiku-anchor variant (lunas wait for haiku, +21.8%) | Loses V5-D5's isolated canary and costs 22 points; V5-D5 as written instead |
| R2-V4:41 | F7 on S13 with one adjudication | Only 1 of 4 cards answered; gain 0.02-0.19, not worth an arm |
| INV-018 | V2's mid-arm decoy on overlap | Pools two treatments in one arm; stop and report instead |
| Ordering | Renumber redesigns to slot order | V4 numbering kept to avoid breaking the base's cross-references; slot order is shown in the slate and comparison tables |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Low | Reader cannot map arm names | Revert to base title block |
| 2 | Medium | Theory-to-design mapping inconsistent | Revert to base §1 and add only T2a/T2b |
| 3 | Medium | Arms' launch commands disagree with R-05 | Revert base H block; keep INV-002 sentence |
| 4 | Low | Shares summed somewhere | Remove the H/P/C definitions |
| 5 | Low | Validator rule inconsistent with F7 | Revert to base schema plus no-free-text line |
| 6 | Medium | Alarms reference removed fields | Restore base seal text, keep fail-closed line |
| 7 | Medium | Alarm thresholds inconsistent | Restore base R-25 |
| 8 | High | Time blocks in all five redesigns inconsistent | Restore base timing block; flag every time figure UNVERIFIED |
| 9 | Low | Catalogue columns misaligned | Remove the two new columns |
| 10 | Low | Additive | Remove the inserted subsection |
| 11 | High | F1 numbers inconsistent with §3/§5 | Restore base Redesign 3 with R2-V4 gain table |
| 12-15 | Medium | Per-design blocks inconsistent | Restore the base block for that design |
| 16 | Medium | Table disagrees with design blocks | Rebuild table from design blocks |
| 17 | Medium | Experiment arms misnamed | Restore base §4 with renamed arms |
| 18-22 | Low-Medium | Requirement ids out of step | Restore base §5 tables |

## Review Status
- [x] Auto-approved (default; `--unattended`, no `--interactive`)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-13T18:56:58Z
