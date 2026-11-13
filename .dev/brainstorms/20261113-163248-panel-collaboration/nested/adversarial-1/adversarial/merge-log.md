# Merge Execution Log

## Metadata
- Base: Variant 4 (opus:devops)
- Executor: merge-executor agent
- Changes applied: 22 of 22
- Status: success
- Timestamp: 2026-11-13T19:02:25Z (start; base copied and this stub written before any change)
- Output: `../merged-spec.md` (copied from `variant-4-original.md` before any change)
- Order of application: 1, 8, 3, 4, 5, 6, 7, 9, 10, 2, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22

## Changes Applied

### Change 1: Front matter, provenance and reading guide
- **Status**: Applied
- **Source**: refactor-plan global decisions 1-2; V5:21-31 (named baselines and shares style)
- **Target**: base title block and introduction (V4:1-21)
- **Before**: H1 "Requirements specification, variant 4 (devops lens) ..."; path list; label sentence; devops framing list ("kill switch ... restores the isolated panel unchanged")
- **After**: provenance header comments; H1 without "variant 4"; `RR` abbreviation added; label sentence states GT6 = I1 (X-003); framing list says the cap is audited for mid-run designs and the kill switch restores the isolated panel with H; "How to read" block with the 5-row slate table, the arm table (A0-A6 plus stage 2) and one symbol table defining B, B_A1, B_f, B_c, T0, turn_p90, T_report_p90, k, n, H, P, C. The reading guide is a bold label, not a heading, so the document keeps exactly five H2 sections.
- **Provenance tag**: `<!-- Source: Base (original, modified) - new title and reading guide per Change #1 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (section 2.0, section 4, R-05 resolve after later changes) | Contradictions ✅

### Change 8: Panel timing rules
- **Status**: Applied
- **Source**: INV-001 and INV-008 "Exact rule" cells of `debate/round3-V1.md:25, :32`; thresholds from `round3-V2.md:24`; five-part rule `round2-V1.md:139-147`; per-slot slowdown limits `round2-V2.md:176-187`; critical-path measurement `round2-V4.md:108`; drift band `round2-V3.md:162-168`; values file and baked settings `round3-V4.md:24, :31` (INV-024); static kit +29% `V5:411`; per-package medians `round3-agenda.md:11-16`
- **Target**: base §2.0 "Timing constants" and "Baseline elapsed time per package" (V4:141-161)
- **Before**: per-turn table; 6 s start; baseline table S07/S13/S14/S24 with caps 157/135/304/322 s
- **After**: per-turn table kept (now labelled medians) plus 16 s fallback and 2 s hooks; named-baseline table EL2 116 s, HL2 238 s, SL2 273.7 s with 1.30/1.35/1.5 x B columns and the AG per-package medians; nine numbered timing rules: PANEL_FINISH_AT formula (143.8 s), k formula with threshold table, three-number block, audited-vs-enforced statement, five-part baseline rule with slowdown limits (5.7/11.2/14.6%) and drift band (0.963), values file, `finish_would_fire`, baked settings, "+x%" labelling. S13 and S14 rows removed (no design uses them; Change 14 says replace S14 everywhere).
- **Executor note**: the k >= 1 thresholds at B = 120 s and 122 s (20.8 s, 21.5 s) were computed mechanically from the same formula; the sources give only the k = 2 values there. V3's drift rule also said "re-freeze B_f from that block's A1 runs"; that clause was not copied because `round3-V4.md:31` (adopted in Change 8 item 6) says the values file is never recomputed during an arm.
- **Provenance tag**: `<!-- Source: Base (original, modified) - timing constants and baseline tables replaced by the panel timing rules per Change #8 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ (R-21, R-24, R-30 exist in §5) | Contradictions ✅ (143.8, 156.6, 174, 369.5, 410.6, 130.8, 143.6 match the INV-001/INV-008 texts)

### Change 3: Harness bundle H1-H4 rewritten
- **Status**: Applied (R-05 deferred to Change 19, as the plan's risk note says R-05 changes in step with Change 19)
- **Source**: V1:102-111 (H2 truncate-validate-re-ask; grading held constant); INV-002 cell of `round3-V1.md:26`; INV-009 and INV-010 at `round3-V1.md:36-37`; retry loop and hang guard at `round3-V4.md:42-47`
- **Target**: base §2.0 harness list (V4:163-168) and R-01..R-04
- **Before**: four one-line fixes; H2 = validate and re-ask only; R-02 re-ask only, no truncation, no time accounting
- **After**: H1-H4 table; grading and judge held constant and sha256-pinned; six rules (one phase-2 deadline T0 + 1.30 B_A1 incl. re-ask, "hard bound" = phase-2 bound, panel elapsed <= max(T1, deadline); `reask_s` in every arm; every arm drops `--no-session-persistence`; phase-1 re-ask before the seal; retry loop sums attempts with `attempts`, `retry_s`, `retry_isolated`; common hang guard 1.5 B_A1 with `hang_kill`). R-01 verification now names A1 (renamed arm); R-02 rewritten with truncation, resume re-ask, deadline and `reask_s`; R-03 labelled H3/H4.
- **Provenance tag**: `<!-- Source: Base (original, modified) - harness bundle rewritten per Change #3 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ (R-03, R-11 exist) | Contradictions ✅ (150.8 s deadline, 1.5 B_A1 guard agree with Change 8)

### Change 4: Shares H, P and C, never summed
- **Status**: Applied
- **Source**: V5:141-153 (three shares, bottom-up H 0.03-0.34, central 0.14); V4:184 (H-C interaction, A-004); V5:106, :433 (Spike 5)
- **Target**: base §2.0 "Estimated H share" table and basis (V4:170-184)
- **Before**: H +0.2 to +0.6 (EL2), +0.2 to +0.5 (S13), +0.1 to +0.4 (sonnet panels), with an AUDIT-CLEAN basis
- **After**: share definitions H = A1 - A0, P = A2 - A1, C = arm - A2 (gap cards and luna F3 injections booked to P); C conditional on H, never summed; V5's bottom-up H table (0.03-0.34, central 0.14); SL2 H +0.1 to +0.4 UNVERIFIED; Spike 5 replaces the normalizer row
- **Provenance tag**: `<!-- Source: Variant 5 (sonnet:performance), V5:141-153 ... - merged per Change #4 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (old "+0.2 to +0.6" removed here; remaining copies in the redesign blocks and §3 are removed by Changes 11-16)

### Change 5: Message rules
- **Status**: Applied
- **Source**: V4:108-117 (`panel-msg/1`, 12-200-character anchors); V2:116-131 (located verbatim quote, existing path, forbidden keys; X-007); INV-005 clause (1) of `round3-V2.md:21`; `over_cap` from `round3-V4.md:28`
- **Target**: base §2.0 schema text (V4:117) and §5.2 R-06, R-08
- **Before**: forbidden `claim`, `severity`, `blocking`, `category` and free text; R-08 anchor rule
- **After**: four validation bullets (no free text, forbidden keys enumerated incl. `verdict` and `note`; located anchors and existing paths; the single F7 enum exception; `over_cap`); R-06 and R-08 updated in place with matching verification
- **Provenance tag**: `<!-- Source: Base (original, modified) - message rules per Change #5 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ ("Redesign 4", "section 4" resolve) | Contradictions ✅
- **Executor note**: a follow-up edit in the same change lets `kind:"coverage"` lines carry candidate Task ids in `items` (Redesign 5 sends Task ids, not paths), so the "existing path" rule does not contradict F6.

### Change 6: Independence, seals and peer tagging
- **Status**: Applied
- **Source**: V4:122, :286 (seal); `round2-V4.md:73-74` (fail closed on the seal, fail open on the review); INV-012 at `round3-V1.md:39`; INV-031
- **Target**: base §2.0 board substrate (V4:119-125) and R-10
- **Before**: `panel-seal` helper and luna seal turn; Stop hook hold up to H seconds; R-10 origin by receipt time
- **After**: one helper `panel-post` (atomic), harness-authored lines named; no Stop hold anywhere, `late` items dropped; new "Independence: seals and peer tagging" block (process-exit seal for F1, fail-closed hook snapshot with sha256 for mid-run designs, `snapshot_missing`, mechanical 12-character peer tag, own-sealed-findings alarms removed, timestamp test = integrity log only); R-10 rewritten in place
- **Provenance tag**: `<!-- Source: Base (original, modified) - writing, reading and seal rules per Change #6 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ (R-22 exists) | Contradictions ✅ (Redesign 2's `panel-seal` and Stop hold and Redesign 4's hold are removed in Changes 12 and 15)

### Change 7: Convergence alarm on own lines
- **Status**: Applied
- **Source**: V4 R-25 and V4:234 (relative alarm); INV-004 cell of `round3-V1.md:28`; guard "at most 2 of 12 runs" (`round2-V2.md:148`); INV-018 at `round3-V1.md:41`
- **Target**: new shared alarm block in §2.0 (the base had the alarm only inside Redesign 1 (e)) and R-25
- **Before**: CONVERGENCE on all-line `pairwise_task_jaccard`; `SEAL` alarm on seal compliance
- **After**: own-line Jaccard rule (`own_line_jaccard`, A1 mean + 0.15, ledger rows -20%), independence guard 2 of 12 runs, ECHO on real-anchor slots only (> 30% F1, > 60% F4), `flag_finding_overlap` > 50% stops and reports the arm; R-25 rewritten in place. `SEAL` replaced by `SNAPSHOT` (> 50% `snapshot_missing`), because the luna seal turn no longer exists (Change 6).
- **Executor note**: the 50% `SNAPSHOT` threshold carries over the base's 50% `SEAL` threshold (V4:335, R-25) to the renamed mechanism; no new number was introduced.
- **Provenance tag**: `<!-- Source: Base (original, modified) - shared convergence alarm per Change #7 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (R-23 gains `own_line_jaccard` in Change 19)

### Change 9: Move catalogue: observable signatures and c-values
- **Status**: Applied
- **Source**: V4:95-106 (catalogue with best-style column); INV-007 (`round3-V1.md:31`, `round3-V2.md:23`); V5:83-94 (c per move as a ceiling; U-015, A-011)
- **Target**: base catalogue table (V4:95-106)
- **Before**: 3 columns (id, move, style)
- **After**: 5 columns: adds "observable tool-call signature" (M1, M2, M4, M7 observable; M3, M5, M6, M8, M9, M10 unobservable) and "c ceiling" mapped from V5's G ids (G7->M1, G6->M2, G1->M3, G5->M4, G3->M5, G4->M6, G8->M7/M8 shared, G2->M9, none for M10); "source.md opened" and "unnamed test opened" listed as observable non-move checks; three rules (unobservable never "not done by any panel member", c is a ceiling, low end 0 for never-found issues)
- **Executor notes**: (1) M2 and M4 were given signatures rather than "unobservable": global decision 5 keeps ember's I4 (M4) and B8/B6 (M2) rows in F3's collaboration share, which is only coherent if the classifier can see those moves. (2) The A-011 rule is worded so that it does not contradict the plan's explicit F4 total (0.14-0.67, whose I5 row has low end 0.06) and F6 re-derivation (global decision 4); the plan states both numbers and the rule, and this wording is the reconciliation.
- **Provenance tag**: `<!-- Source: Base (original, modified) - two columns added per Change #9 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 10: Distinctness criterion and slate table
- **Status**: Applied
- **Source**: `round3-V1.md:30` (triple criterion, INV-006); `round3-V2.md:22` (move-only F3); `round2-V4.md:32` (why F5 is evicted)
- **Target**: inserted as "### 2.1 Slate and distinctness criterion" after §2.0 and before Redesign 1
- **Before**: none (base had no distinctness statement)
- **After**: criterion; five triples; pairwise check incl. the move-only condition for F3/F6; why F5 (0 of 3 from F4) and F2 (at most 1 of 3 from F7) are out; I6 route via F1's `contradiction` routing row
- **Executor note**: the debate texts say "`contradiction` -> M7" using V2's catalogue ids, where V2's M7 is "Propagation" (V2:112). In this document's catalogue (V4 ids) the same move is M8 ("apply the same check ... to every other task"), so the row is written `contradiction` -> M8. Meaning unchanged.
- **Provenance tag**: `<!-- Source: Variant 1 (opus:architect), debate/round3-V1.md:30 ... - merged per Change #10 -->`
- **Validation**: Structural integrity ✅ (H3 under §2, no level gap) | References ✅ (Redesign 1-5 resolve) | Contradictions ✅

### Change 2: Theories: gate funnel plus T2a/T2b plus T1 complementarity
- **Status**: Applied
- **Source**: V2:9-94 (three-gate funnel and per-issue gate table; S-003, U-004); V5:40 (T2a/T2b; C-002); V1:25-45 and V2:27 (searcher/reader complementarity, luna 48/48 vs 11/48 source.md; C-001, U-007)
- **Target**: base §1 (V4:22-87)
- **Before**: intro; T1, T2, T3 each with an evidence table; mapping table with T2 as one theory
- **After**: intro names the funnel and the T2 split; T1 gains the complementarity paragraph and one evidence row; T2 retitled and split into T2a/T2b with a "Part" column (rows unchanged in content); T3 gains the X-002 sentence (leak removal 0 on /14, sonnet-panel I7 only); new "Gate funnel" H3 table (exposure, question, survival, redesigns aimed at the blocked gate) before the mapping table; mapping table's primary/secondary theories relabelled T2a/T2b. Three theories kept; X-003 (GT6 = I1) stated in the front matter (Change 1).
- **Executor note**: V2's gate table cites V2's own move ids; the table here names redesigns instead of moves so it cannot disagree with the V4-id mapping table. B1, B2, I4 and I6 exposure cells were changed from V2's "in plan" to "fails (T2b)" as `round2-V3.md:173` and `round2-V4.md:138` require.
- **Provenance tag**: `<!-- Source: Base (original, modified) - section 1 restructured per Change #2 (...) -->` and `<!-- Source: Variant 2 (opus:analyzer), V2:81-94 ... - merged per Change #2 -->`
- **Validation**: Structural integrity ✅ (new H3 under §1) | References ✅ (F1-F7 defined in front matter and §2.1) | Contradictions ✅

### Change 11: Redesign 3 Axis-Flip Challenge = F1
- **Status**: Applied
- **Source**: V4:343-460; `round2-V4.md:45-63` (box, gap card, HL2 shadow, gain steps); INV-003 cell of `round3-V1.md:27`; balanced deal `round3-V2.md:21(3)`; INV-013, INV-014, INV-022 (`round3-V1.md:40`, `round3-V3.md:26`); `contradiction` row (`round2-V2.md:13`); sealed-report judging (V2:517); V5-D5 (V5:350-392, X-004)
- **Target**: base Redesign 3, (a)-(h)
- **Before**: K challenges, 45 s / 35 s timeouts, 148 s (+28%), haiku-anchor variant 290 s (+22%) with gain 0.40-1.60, C 0.23-0.94 "plus H +0.2 to +0.6", session-directory deletion
- **After**: heading carries slot/family label; (a) routing table plus `contradiction` -> M8 row, gap card p = 1/3 seeded per receiver and booked to P, balanced online deal (`deal_r`), HL2 = V5-D5 as written (+0%, worst 253 s = +6.3%, 173.2 s < 238 s, gain not carried); (b) n/box formulas with start_cost 6/16 s, recomputed per launch, n = 0 no launch, one phase-2 deadline, zero-anchor rule; (c) stream-json on phase-2 and re-ask sessions, salvage, S2 streaming check; (d) 126.6 / 147.6 (+27.2%) / 134.8 (+16.2%) / 146.8 / 141.2 s, enforced phase-2 bound 150.8 s (+30.0%), panel elapsed <= max(T1, deadline), 132.0 s last useful start; (e) decoys, own-line alarm, ECHO on real slots, sealed-report judging on post-re-ask `p1.md`; (f) per-issue C table 0.06-0.63, gap route 0-0.10 in P, H column separate, I7 0.05-0.20, act-rate labelled planning; (g) +20 lines stream-json (total about 165); (h) `phase2_timeout`/`p2_lines_salvaged`, `resume_fallback` with re-computed n, INV-011 cleanup. V4's haiku-anchor variant and the 45 s / 35 s timeouts dropped.
- **Executor notes**: (1) the "+20 lines" for stream-json is the executor's estimate of the plan's "effort per V4 plus stream-json parse"; (2) `contradiction` -> M7 in V2 ids is written M8 in V4 ids (see Change 10).
- **Provenance tag**: `<!-- Source: Base (original, modified) - Redesign 3 (F1, slot 1) rewritten inside its (a)-(h) skeleton per Change #11 (...) -->`
- **Validation**: Structural integrity ✅ ((a)-(h) kept) | References ✅ (section 2.0, REQ-S3 defined in §4 by Change 17) | Contradictions ✅ (147.6, 134.8, 150.8, 0.06-0.63 match Change 8 and the plan)

### Change 12: Redesign 2 Idle-Shift Sweeper = F4
- **Status**: Applied
- **Source**: V4:274-342; `round2-V4.md:65-78`; V2-D1 ranked disjoint locators (V2:151-216); V1-R2 harvest incl. sweeper output; V2-D5 witness as a sweep kind (`round2-V4.md:19`); V5-D3 first-hand rule and 10% stop (V5:299); INV-008; INV-015 (`round3-V4.md:49`), INV-016 (`round3-V3.md:27`)
- **Target**: base Redesign 2, (a)-(h)
- **Before**: luna `panel-seal` turn, 15 s Stop hold, up to 3 facts per luna, 125 s delivery deadline, sweeper last fact by 85 s, typical 142 s / worst 148-160 s (+22% / +28%), I7 0.25-0.60, "plus H +0.2 to +0.6", own-sealed-findings alarm
- **After**: heading with slot/family; (a) witness kind, harvest, ranked locators, balanced deal, k facts per luna, no-clearance rule for n = 0, first-hand rule with 10% stop; (b) snapshot-gated delivery, 2k facts total, sweeper timeout = PANEL_FINISH_AT - T0 - 2 x turn_p90 (131.0 s), no Stop hold, `late`; (d) 130.8 s (+12.8%, k = 1), 143.6 s (+23.8%, k = 2), bound 156.6 s (+35.0%), ceiling 174 s (+50%, `SLO_BREACH`), sweeper 79 s off path, cap audited by R-24; "worst 150.0 s" not used; (e) own-line alarm, ECHO > 60% on real slots; (f) per-issue C at k = 2 and k = 1 (0.14-0.67 / 0.07-0.34), I7 0.17-0.50 / 0.09-0.25 control, H in its own column; (h) `snapshot_missing`, `late`, first-hand audit, INV-015 late-start row, hang guard row
- **Executor notes**: (1) the old 125 s delivery deadline was replaced by "nothing after PANEL_FINISH_AT", the finish-signal rule of Change 8, so no new absolute number was introduced; (2) witness moves M8/M9 in V2 ids are M6/M9 in V4 ids; (3) the I7 chain text was updated to the disjoint-deal chain of `round2-V4.md:20` (0.7 x 0.6 x 0.4 = 0.17 to 0.9 x 0.8 x 0.7 = 0.50).
- **Provenance tag**: `<!-- Source: Base (original, modified) - Redesign 2 (F4, slot 2) rewritten inside its (a)-(h) skeleton per Change #12 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ (section 2.0, R-24, section 4) | Contradictions ✅ (130.8 / 143.6 / 156.6 / 174 match Change 8)

### Change 13: Redesign 1 Move Radar = F3
- **Status**: Applied
- **Source**: V4:188-273; INV-006 move-only rule (`round3-V2.md:22`), INV-007 (`round3-V1.md:31`); V1-R1 per-receiver hash order (V1:231); V5-D4 skip rule only (`round2-V4.md:82`); V3 leak check (V3:88, U-009; `round3-V4.md:36`); global decision 5
- **Target**: base Redesign 1, (a)-(h)
- **Before**: "one move that no panel member has done yet" for all reviewers; 2 injections each; deadline 110 s "cap 157 s minus 45 s"; 144 s (+24%, "worst case equals expected"); C 0.20-0.88 incl. luna rows; "plus H +0.2 to +0.6"
- **After**: heading with slot/family; (a) classifier limited to observable signatures; roles table with share per row (ember observable moves and source.md check -> C; luna reading moves -> timed static prompt, P); move-only payload with Task kept in metrics; per-receiver hash order; skip rule; A6 vs A2 = "telemetry-timed kit vs static kit"; (b) k checkpoints, source.md check counted inside k, deadline T0 + 1.35 B_A1 - 47 s (110 s); (d) ember 47.4/53.8 s off path, luna 130.8 s (+12.8%) / 143.6 s (+23.8%), bound 156.6 s, ceiling 174 s, cap audited by R-24; "worst = expected" struck; (e) leak check as move-id lookup, own-line alarm; (f) ember gross 0.12-0.48 (k = 2) / 0.06-0.24 (k = 1), C net 0-0.48 / 0-0.24, luna rows 0.08-0.40 / 0.04-0.20 in P, I7 0.10-0.40 / 0.05-0.20, H column separate; (h) leak and finish-signal rows added
- **Executor notes**: (1) the base's Stop-time "source.md never opened" check would add turns outside the three-number block, so it is delivered at the first checkpoint and counted inside k; (2) global decision 5 states I7 0.10-0.40 "stays"; the k = 1 value 0.05-0.20 applies global decision 3's 0.5 planning rule to that row, as for F4's I7 row; (3) the never-found I5 row keeps its gross 0.02 low end per global decision 5; its net C low end is 0, which satisfies the A-011 rule.
- **Provenance tag**: `<!-- Source: Base (original, modified) - Redesign 1 (F3, slot 3) rewritten inside its (a)-(h) skeleton per Change #13 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ (section 2.0, section 2.1, R-24) | Contradictions ✅

### Change 14: Redesign 5 Coverage Deflection = F6 on SL2
- **Status**: Applied
- **Source**: V4:539-611; `round2-V4.md:84-86`; INV-006 (`round3-V1.md:30`, `round3-V4.md:29`); INV-008; V1-R5 brief line ("peer coverage is not clearance", `round2-V1.md:104`); U-014 surface filter; global decision 4
- **Target**: base Redesign 5, (a)-(h)
- **Before**: S14 (ember + luna + sonnet), 225 s, cap 304 s, covered list with counts `"T9:contradiction:2"`, expected 253 s / worst 281 s (+12% / +25%), C 0.26-1.06, transcript-timestamp separation
- **After**: heading with slot/family; SL2 (sonnet + 2x luna), 273.7 s; trigger on each luna scout's exit; (Task, category) of non-surface findings parsed, requests only for Tasks with no peer finding ranked by declared not-checked scope; no counts, no categories, no telemetry, no SendMessage; V1-R5 brief line; at most k requests per card and k in total; run condition T_report_p90 <= 51.8 s; (d) 303.7 s (+11.0%, k = 1), 331.7 s (+21.2%, k = 2), bound 369.5 s, ceiling 410.6 s, cap audited by R-24; (e) snapshot seal, mechanical peer tag, own-line alarm plus deflection alarm against A1-SL2; (f) per-issue re-derivation table (k = 2 0.13-1.06, k = 1 0.07-0.53, planning), I7 -0.20 to +0.20, H +0.1 to +0.4 UNVERIFIED in its own column; (h) Spike-4 run-condition and finish-signal rows. S14 and 225 s no longer appear in the section.
- **Executor note**: the plan says "at most k requests per card" while its time arithmetic (303.7 s = 273.7 + 2 + 28) counts one request at k = 1 for the whole package; the spec states both (each card lists at most k; sonnet acts on at most k in total), which is what INV-008's per-receiver k means.
- **Provenance tag**: `<!-- Source: Base (original, modified) - Redesign 5 (F6, slot 4) re-based to SL2 ... per Change #14 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ (section 2.0, section 4, R-24) | Contradictions ✅ (303.7 / 331.7 / 369.5 / 410.6 / 23.8 / 51.8 match Change 8)
- **Follow-up edit**: (e) originally said sonnet's later findings are tagged when they "cite a requested Task's anchor region"; F6 sends no anchors, so it now says the requested Task id is the delivered locator of the INV-012 rule.

### Change 15: Redesign 4 Flag-and-Adjudicate = F7 (EL2, one way)
- **Status**: Applied
- **Source**: V4:461-538; `round2-V4.md:28-43`; INV-005 cell of `round3-V2.md:21`; INV-017, INV-018, INV-023; V5 C-3 first-hand rule
- **Target**: base Redesign 4, (a)-(h)
- **Before**: two-way design on S13 (ember + luna, 100 s, cap 135 s), luna search cards, Stop hold up to 50 s, at most 4 ember cards, typical +19% / worst +32%, C 0.16-0.93 "plus H +0.2 to +0.5", alarm on luna's sealed findings
- **After**: heading with slot/family; EL2, one way; ember flags from its 3rd tool call, at most 2k cards with enum category/severity; dealing card i -> luna (i + r) mod 2, form challenge when (i + floor(i/2) + c) is even; per-slot logging incl. conversion, judge-credited/uncredited conversion and card Task; SEED:47 answered within F7, A5 vs A4 stated to compare two whole designs; (d) ember 47.4/53.8 s off path, luna 130.8 / 143.6 s, bound 156.6 s, ceiling 174 s, cap audited; (e) own-line alarm, adjudication agreement, `flag_finding_overlap` stops and reports; (f) per-issue C at k = 2 0.08-0.77 and k = 1 0.04-0.39, I7 0-0.10 / 0-0.05, designSpec rows depend on k >= 1, INV-017 falsifier, pre-registered secondary analysis (at most 144 cards); (h) Stop-hold rows removed, overlap, early-Task, snapshot and finish-signal rows added. S13 variant and Stop hold dropped; "A5 vs A4 answers SEED:47" and "worst 150.0 s" not used.
- **Executor notes**: (1) the base note "arm A1 bounds it" now says A2, because the static-kit arm is A2 after the renaming (global decision 2); (2) effort was re-totalled from the base's own line items with the 30-line Stop hold removed (210 -> 180); (3) the card-overload row's detection moved from "luna's sealed findings below 1.0" (removed by Change 6) to the ledger-rows part of the CONVERGENCE alarm, and its action no longer changes the cap mid-arm (INV-018).
- **Provenance tag**: `<!-- Source: Base (original, modified) - Redesign 4 (F7, slot 5) re-based to EL2, one way ... per Change #15 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ (R-06, R-24, section 2.0) | Contradictions ✅

### Change 16: Comparison table
- **Status**: Applied
- **Source**: V5:400-413 (net collaboration share, tokens per added issue, static-kit row, sonnet reference row; S-004); V4:614-626 (I7 column)
- **Target**: base §3 table and intro
- **Before**: 5 rows in redesign order, "expected / worst" overhead column, single gain column, "Add the H share (+0.2 to +0.6 ...)"
- **After**: 8 rows (five redesigns in slot order F1, F4, F3, F6, F7 with V4 numbers kept, plus A2 static kit, A1 on EL2, A1-SL2 as the sonnet reference); 15 columns: panel and baseline; planned elapsed k = 1 / k = 2 (n for F1); finish-signal bound; enforced ceiling; C k = 1 / k = 2; P; H; I7; output tokens overhead; tokens per added issue; contamination; effort; reliability. "+0.2 to +0.6 H" and all "worst" columns removed. Notes define the tokens-per-added-issue planning formula.
- **Executor notes**: (1) tokens per added issue for F1, F4, F3 were computed with the stated formula (21.6k/0.345 = 63k; 28.8k/0.405 = 71k; 16.8k/0.24 = 70k); (2) F6 and F7 token overheads in the base were for S14 and the two-way S13 design, so they are marked "not re-derived" instead of being carried; (3) A2 and sonnet-reference values are V5's (V5:411-413), labelled as V5 assumptions or historical measurements.
- **Provenance tag**: `<!-- Source: Base (original, modified) - comparison table rebuilt per Change #16 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ (R-24, section 4) | Contradictions ✅ (every number matches the five (d) and (f) blocks)

### Change 17: First experiment
- **Status**: Applied
- **Source**: `round2-V2.md:118-148` (arms, sizes, endpoint, futility-only interim, familywise bound); `round2-V4.md:90-96`; `round3-V2.md:30-32` (decision table against observed A1 reach, stage-2 screen); V2:517, :531 (sealed-report judging, two-new-package confirmation; A-009); INV-005 secondary analysis; V5 block randomisation (V5:448); V1:614 (REQ-S3); V5:429-433 (spikes 4, 5)
- **Target**: base §4 (V4:630-684)
- **Before**: two arms (Axis-Flip, Sweeper) at 4 replicates; old A0/A1 naming; "2 of 4 and +2 vs A1" reach rule; deferred Redesigns 1, 4, 5
- **After**: all five slots in two stages; Gate 0 (S0, S1 conditional, S2 incl. streaming, S3 incl. stream-json parse, REQ-S3 incl. "finish now", Spike 4 values file, Spike 5); arms A0 (4 + S07 context), A1 12, A2 12, A3-A6 6 -> 12, stage 2 A1-SL2 12, A2-SL2 6, F6-SL2 6 -> 12; size 76 max / 52 min + 30; conduct (`NOFALLBACK=1`, 10 concurrent / 4 ember, `model_ok`, block randomisation, same blind judge, sealed-report judging for A3); reach endpoint; decision table against observed A1 reach (0 -> 4/12 p = 0.047; 1 -> 6/12 p = 0.034; 2 -> 7/12 p = 0.045); +4 over A2; no-loss guards; time and independence guards; futility-only interim; familywise 0.20 with two-package confirmation; stage-2 screen; secondary analyses incl. F7 form contrast; INV-019 statement that the plan cannot detect central estimates, and why it is still run; outcomes table
- **Executor note**: the base cost estimate (about 1.25M tokens for 48 package-runs) applied to the old 4-arm plan and was not carried; no source gives a cost for the merged plan.
- **Provenance tag**: `<!-- Source: Variant 2 (opus:analyzer) experiment plan (...) - merged per Change #17, replacing the base section 4 -->`
- **Validation**: Structural integrity ✅ | References ✅ (R-24, R-30, section 2) | Contradictions ✅ (arm names match the front-matter table; 51.8 s matches Change 8)

### Change 18: Requirements for all five redesigns
- **Status**: Applied
- **Source**: V4:686-746 (R-01..R-30 with verification column; S-005); Changes 3-17
- **Target**: base §5
- **Before**: title "Requirements for the chosen designs (Redesign 3 ..., Redesign 2 ..., and the shared substrate)"; R-11..R-30 for the old two-arm plan (35/45 s timeouts, 4 facts, `panel-seal`, 125 s deadline, 15 s hold, A0-relative cap, 4 replicates, n = 4 caveat)
- **After**: §5 retitled "Requirements for the shared substrate and all five redesigns" with an id note. Updated in place: R-11 (post-re-ask `p1.md`), R-12 (balanced deal, gap card, zero-anchor rule), R-13 (`contradiction` -> M8), R-14 (n recomputed on fallback), R-15 (box/n formulas, one deadline, stream-json salvage), R-17 (witness kind, sweeper timeout formula), R-18 (2k facts, harvest, n = 0 rule), R-19 (snapshot seal), R-20 (balanced deal, k, no hold, first-hand rule), R-21 (T0 and PANEL_FINISH_AT baked), R-24 (B_A1, retries and re-asks in elapsed, audited not enforced), R-26 (snapshots), R-27 (all spikes), R-28 (section 4 arms), R-29 (random labels, sealed-report judging), R-30 (values file and analysis script committed, H/P/C separate). New: §5.7 F3 R-31..R-33 (observable-signature list, move-only injection, static booking), §5.8 F7 R-34..R-37 (cards, deal and form, slot logging, overlap stop), §5.9 F6 R-38..R-40 (trigger on scout exit, k and run condition, deflection alarm), §5.10 shared R-41..R-47 (finish signal, k formula, hang guard in every arm, retry accounting, slowdown and drift, session cleanup, act rate). Every new id has a verification entry.
- **Executor note**: while editing §5.5 the read-only enforcement paragraph of Change 22 was inserted in the same Edit, because both target the head of §5.5; it is logged under Change 22 below.
- **Provenance tag**: `<!-- Source: Base (original, modified) - section 5 retitled and extended ... per Change #18 ... -->` and `<!-- Source: Base (original, modified) - new requirement subsections ... per Change #18 ... -->`
- **Validation**: Structural integrity ✅ (5.1-5.10 consecutive, all H3 under H2 §5) | References ✅ (R-06, R-09, R-24, R-30 resolve) | Contradictions ✅ (R-05 and R-23 left for Change 19)

### Change 19: Kill switch and `collab.json` schema
- **Status**: Applied
- **Source**: V4:139, R-05, R-23; `round3-V4.md:48, :57-63`; INV-011 (`round3-V1.md:38`, already carried in Redesign 3 (h) and R-46)
- **Target**: base kill-switch paragraph in §2.0, R-05, R-23
- **Before**: kill switch "reproduces today's `run-reviewer.sh` exactly"; R-05 allowed only R-01 and R-03; R-23 with `seal_missing` and without timing/accounting fields
- **After**: kill switch restores the isolated panel with H; R-05 allowed differences = R-01, R-03, removal of `--no-session-persistence`, stream-json on phase-2 and re-ask sessions, common hang guard; R-23 gains `reask_s`, `attempts`, `retry_s`, `phase2_timeout`, `p2_lines_salvaged`, `n_planned`, `n_launched`, `k`, `panel_finish_at`, `finish_signal_t`, `finish_would_fire`, `hang_kill`, `snapshot_missing`, `late`, `over_cap`, `slot_type`, `card_form`, `deal_r`, `deal_c`, `own_line_jaccard`, `retry_isolated` (all 21 named by the plan), plus the values-file sha256 needed by R-30; `seal_missing` removed (no seal turn exists); verification now covers A1 and A2 too (they log `reask_s` and `finish_would_fire`)
- **Provenance tag**: `<!-- Source: Base (original, modified) - kill switch per Change #19 (...) -->` (R-05 and R-23 are rows inside the §5 tables, covered by the Change 18 section tag)
- **Validation**: Structural integrity ✅ | References ✅ (R-01, R-03, R-43 resolve) | Contradictions ✅

### Change 20: Act rate tied to a spike
- **Status**: Applied
- **Source**: V1:614 (REQ-S3); A-001
- **Target**: §2.0 gain-model text (shares block) and each (f) block
- **Before**: act rates (0.5-0.8, 0.5-0.6, 0.6-0.8) stated as assumptions with no spike
- **After**: an "Act rates are planning values" paragraph in §2.0 tying every factor to REQ-S3 (including "finish now") and R-47; each of the five (f) blocks already carries a sentence labelling its act-rate factor as planning and naming REQ-S3 (written during Changes 11-15)
- **Provenance tag**: `<!-- Source: Variant 1 (opus:architect), V1:614 (REQ-S3) - act-rate rule merged per Change #20 (A-001) -->`
- **Validation**: Structural integrity ✅ | References ✅ (section 4 defines REQ-S3; R-47 exists) | Contradictions ✅

### Change 21: Itemised unverified list
- **Status**: Applied
- **Source**: V5:538-545; V4:750-759; `round3-V2.md` (T_report_p90)
- **Target**: base closing list after §5 (V4:750-759)
- **Before**: three bullets (hooks/resume, per-turn and 6 s start, gain ranges) and two risks (n = 4 power, regression to the mean)
- **After**: a 16-row table, one row per unmeasured number (T_report_p90, turn_p90, act rates, act rate on "finish now", resume and start costs, stream-json before exit, hooks and hook env, per-package B_A1, static-kit and brief cost, k = 1 scaling, F6 SL2 re-derivation, SL2 H share, H2 part of H, F6/F7 token overheads, c/P/gain ranges, base commits), each with where it is used, the value used, and the spike or arm that replaces it; risks updated (n = 12 cannot detect central estimates; in-sample catalogue). Kept as a bold label, not a heading, so the document still has exactly five H2 sections plus the closing list.
- **Provenance tag**: `<!-- Source: Variant 5 (sonnet:performance), V5:538-545 ... - merged per Change #21 -->`
- **Validation**: Structural integrity ✅ | References ✅ (section 4, R-03) | Contradictions ✅ (values match §2.0 and the (d)/(f) blocks)

### Change 22: Read-only enforcement statement
- **Status**: Applied (text inserted during the Change 18 edit of §5.5, see the note there; content exactly as planned)
- **Source**: V4 R-09 (helpers write only under `$BOARD`); A-008
- **Target**: base §5.5 head
- **Before**: no statement; R-09 alone implied read-only came from `--disallowedTools`
- **After**: paragraph "Read-only is enforced by audit, not by the tool list": Bash is unrestricted, so read-only is enforced by audit (helpers write only under `$BOARD`, clean `git status` after the last run on a sandbox, unchanged candidate sha256)
- **Provenance tag**: `<!-- Source: Base (original, modified) - read-only enforcement statement per Change #22 (V4 R-09; A-008) -->`
- **Validation**: Structural integrity ✅ | References ✅ (R-09) | Contradictions ✅ (agrees with R-09 and R-46)

## Post-Merge Validation

### Structural Integrity
- Exactly five H2 sections: 1 Theories, 2 Five redesigns, 3 Comparison, 4 Recommended first experiment, 5 Requirements. The reading guide (front matter) and the closing unverified list are bold labels, not headings. ✅
- Heading hierarchy: one H1; every H3 sits under an H2; no H4 or deeper; no level gaps. §1 has T1, T2 (T2a/T2b), T3, Gate funnel, Mapping; §2 has 2.0, 2.1 and Redesigns 1-5; §5 has 5.1-5.10 in order. ✅
- Each redesign keeps the (a)-(h) skeleton: (a) mechanism and model roles, (b) communication schedule with triggers, frequency, per-reviewer message counts, size cap, schema, (c) transport and why, (d) time budget against a named baseline (EL2 or SL2) with the three numbers for F3, F4, F6, F7 and the enforced phase-2 bound for F1, (e) safeguards with the own-line Jaccard alarm, (f) gain with C and H (and P) in separate columns at k = 1 and k = 2 (F1 at n = 2), (g) effort, (h) runbook. ✅
- Table check: every markdown table row has the same column count as its header (awk scan, 0 mismatches). ✅
- Provenance: 3 header comments plus 26 `<!-- Source: ... -->` comments, one before every H2 section and every replaced or merged block. During validation a Source tag was added before "## 2." and before the base "Transports rejected" block, and §4's tag was moved above its heading. ✅

### Internal References
- `R-nn`: 93 occurrences, 47 distinct ids, all 47 defined in §5 (R-01..R-30 kept, R-31..R-47 new); 0 broken. Every requirement row has a verification entry. ✅
- `Redesign N`: 49 occurrences, all N in 1-5, all defined in §2; 0 broken. ✅
- Section references in body text: "section 2" (2), "section 2.0" (21), "section 2.1" (1), "section 4" (10), "section 5.5" (1); all resolve. "section 1" and "section 5" occur only inside provenance comments. The two "§2" occurrences cite `investigation-alias-control.md` §2 (an external file) and the three "§3" occurrences in the unverified table refer to this document's §3; all resolve. ✅
- Total checked: 93 + 49 + 40 body section references = 182; resolved 182; broken 0.
- Body text no longer cites debate-internal ids (A-011, X-005, `round2-V1.md`); those were replaced by plain wording during validation and remain only in provenance comments. The word "Change" appears only in provenance comments.

### Contradiction Re-Scan
Each key number was searched in the merged spec (count of occurrences, and every percentage attached to it):
- 116 s (39): always the EL2 planning B. ✅
- 143.6 s (10): always "+23.8%", always the k = 2 planned end. ✅
- 130.8 s (10): always "+12.8%", always the k = 1 planned end. ✅
- 147.6 s (3): always "+27.2%" (F1, n = 2). 134.8 s (3): always "+16.2%" (F1, n = 1). 146.8 s (1, F1 fallback), 141.2 s (1, ember), 126.6 s (1, luna A). ✅
- 150.8 s (5): always the F1 phase-2 deadline, "+30.0%" where a percentage is given. ✅
- 156.6 s (8): always T0 + 1.35 B_f on EL2, "+35.0%". 143.8 s (6): always PANEL_FINISH_AT at planning values. ✅
- 174 s (13): always the EL2 hang guard, "+50%" / `SLO_BREACH`. ✅
- 273.7 s (15): always the SL2 planning B. 303.7 s (3): "+11.0%"; 331.7 s (3): "+21.2%"; 369.5 s (3): "+35.0%"; 410.6 s (6): "+50%". ✅
- 0.03-0.34 (12): always EL2 H, "central 0.14" where a central value is given; SL2 H is always "+0.1 to +0.4 (UNVERIFIED)". ✅
- Removed figures confirmed absent: "157 s", "225 s", "S14", "S13", "+0.2 to +0.6", "+0.2 to +0.5", "0.20-0.88", "125 s", `seal_missing`. "0.23-0.94" appears once, only as the stated starting point of F1's derivation. ✅
- "worst": every remaining occurrence either says no figure is a worst-case guarantee, or is the HL2 shadow variant of F1 (253 s), which is not one of F3, F4, F6, F7. ✅
- Gains cross-checked between §2 (f) blocks and §3: F1 0.06-0.63, P 0-0.10, I7 0.05-0.20; F4 0.07-0.34 / 0.14-0.67, I7 0.09-0.25 / 0.17-0.50; F3 0-0.24 / 0-0.48, P 0.04-0.20 / 0.08-0.40, I7 0.05-0.20 / 0.10-0.40; F6 0.07-0.53 / 0.13-1.06, I7 -0.20 to +0.20; F7 0.04-0.39 / 0.08-0.77, I7 0-0.05 / 0-0.10. All match; the unverified table matches F6. ✅
- New contradictions found and fixed during the merge: (1) F6 Task-id `items` against the "existing path" rule (fixed in Change 5); (2) F6 peer-tag wording referring to anchors F6 never sends (fixed in Change 14); (3) the A-011 low-end rule against the plan's F4 and F6 low ends (reconciled in Change 9 wording); (4) "the two helpers" in §2.0 after `panel-seal` was removed (now "the `panel-post` helper and the hooks"). No open contradiction remains.

## Summary
- Total changes planned: 22
- Successfully applied: 22
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
- Deviations to note (none change a planned number): Change 22's paragraph was inserted in the same edit as Change 18 (logged in order); `contradiction` -> M7 (V2 ids) is written M8 (V4 ids); M2 and M4 were given observable signatures so global decision 5's ember rows stay in C; F3's source.md check is counted inside k instead of being a Stop-time injection; I7 rows at k = 1 for F3 and F7 apply global decision 3's halving; F6 and F7 token overheads are marked "not re-derived"; the k >= 1 thresholds at B = 120 s and 122 s were computed from the stated formula.

## Independent Post-Merge Review (orchestrator addendum)
- Reviewer: a fresh evaluator agent that wrote neither the variants nor the merge; report `merge-review.md`.
- Review 1: FAIL, 2 blocking findings: (1) the c-column sentence claimed no gain row exceeds c, but rows in F3, F4, F6 and F7 do; (2) the F6 slowdown limit used W = 56 s instead of the k = 2 additive cost 58 s (14.6% -> 13.8%). 8 minor notes recorded, not fixed.
- Fix 1 (orchestrator): F6 limit set to 13.8% (W = 58 s) in the timing rules and R-45; c sentence narrowed. Re-review 1: finding 2 closed, finding 1 open (F3's luna rows also exceed c).
- Fix 2 (orchestrator): the c sentence now says c is a reference ceiling that does not bound the gain rows, with examples from F3, F4/F6/F7 and F6's sonnet receiver. Re-review 2 (final): both findings closed, verdict PASS.
- Post-merge validation after fixes: PASS.
