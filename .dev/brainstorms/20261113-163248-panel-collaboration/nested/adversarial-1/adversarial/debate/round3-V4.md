# Round 3 final arguments: V4 (opus, devops lens)

Citations: `V4:<line>` = `variant-4-original.md`; `R2-V4:<line>` = `round2-V4.md`; `R3-V<n>:<line>` = `round3-V<n>.md`; `INV-0nn` = `../invariant-probe.md`; `AG:<line>` = `round3-agenda.md`; `RR:<line>` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`. I read R3-V1, R3-V2 and R3-V3 before writing. Every number below was recomputed.

## Final position

V4 stays the base, and the slate stays F1, F4, F3, F6, F7. The probe is right on all eight HIGH items. I add no new MODIFY text:

- INV-001 and INV-003: MODIFY = R3-V1.
- INV-005: MODIFY = R3-V2.
- The other five: ACCEPT.

I support **k = 1 as the central row** and **move-only F3 injections**.

As base author, I checked each adopted rule against V4's runbook: the spikes in R-27, the fields in R-23, the kill switch in R-05 and V4:139, and the SLO rule in R-24. All of them can be operated, but only with the corrections listed under MEDIUM below. Two of those corrections come from RR, and no statement in the debate has raised them yet:

- the retry loop (RR:61-64) re-runs a whole review, and no time bound counts that second attempt;
- A1 keeps `timeout 3000` (RR:48), while the design arms get a 1.5 B hang guard. That kills slow runs in the design arms only, so the comparison with A1 is not fair.

## HIGH invariant resolutions

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

## MEDIUM invariants worth closing

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

## Remaining disagreements

None.

## Final concessions

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

## Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | V2-D2 `contradiction` -> M7; gap card p = 1/3 booked to the prompting share; balanced anchor deal; per-attempt n with stream-json salvage; one phase-2 deadline including re-ask; sealed judging on the post-re-ask `p1.md`; V5-D5 HL2 shadow | The only bound enforced by a kill: phase-2 end <= 150.8 s (+30.0%). luna B 147.6 s at n = 2, or 134.8 s at n = 1. C 0.06-0.63 |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | V2-D1 locators by balanced deal; V1-R2 harvest; V2-D5 witness kind; V5-D3 first-hand rule; k per INV-008; fail-closed snapshot; sweeper timeout as a formula; common hang guard | The only cheap I7/T1 path, run in ember's idle time. Planned 130.8 s (+12.8%, k = 1) or 143.6 s (+23.8%, k = 2); signal bound 156.6 s; 174 s = breach |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | Observable signatures only; move-only payload; luna kit booked to A2; V1-R1 hash order; V5-D4 skip rule; V3 leak check; k | Tests telemetry timing vs the static kit. C comes from ember rows only and may be near 0 |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Trigger on scout exit; (Task, category) from findings; requests for uncovered Tasks; no counts, telemetry or SendMessage; surface filter; sonnet k | Claude receiver. Planned 303.7 s (+11.0%) or 331.7 s (+21.2%); bound 369.5 s; ceiling 410.6 s. Runs only if k >= 1; gain re-derived |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | Enum-only forms with R3-V2's online deal; validator exception scoped to cards; cap 2k with `over_cap`; snapshot; V5 C-3; the overlap alarm stops the arm | The only slot that answers SEED:47, within one arm. Timing as F4 |

Proposed base document: V4

## Per-point positions

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
