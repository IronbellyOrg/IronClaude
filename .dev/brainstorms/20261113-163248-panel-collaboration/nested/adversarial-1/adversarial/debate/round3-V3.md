# Round 3 final arguments: V3 (haiku, backend lens)

Citations: `R3-V1:<line>` / `R3-V2:<line>` = those Round 3 files; `R2-V3:<line>` = `round2-V3.md`; `IP:<line>` = `../invariant-probe.md`; `AG:<line>` = `round3-agenda.md`; `T:<line>` = `round2-tally.md`. Arithmetic below is recomputed; timing inputs remain illustrative until measured.

## Final position

Keep V4 and F1, F4, F3, F6, F7. V1 best separates planned time from cooperative and enforced limits; V2 best repairs the receiver/form confounding. Adopt V1's MODIFY texts for INV-001/-003 and V2's for INV-005; ACCEPT the rest. No new MODIFY text. Support k = 1 as conservative central planning, not measured expectation, and move-only F3 messages. My original gains remain withdrawn. A failed second phase must not destroy a valid first phase.

## HIGH invariant resolutions

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

## MEDIUM invariants worth closing

- **INV-009/-010/-011:** adopt R3-V1:36-38. Persistence changes apply uniformly, including A1. Repair P1 before its immutable seal. Delete only run-owned sessions after concurrent users finish, never the shared directory.
- **INV-012:** adopt R3-V1:39. Mechanical peer tags replace model self-report. Drop alarms needing nonexistent mid-run sealed findings. My timestamp check is only an ordering log.
- **INV-013/-014:** empty real-anchor exposure makes ECHO not applicable, not zero. Gap cards need eligible unanchored regions and count as prompting. Re-derive F1 with I4 on the gap route (IP:23-24, :42).
- **INV-015/-016/-017:** log actual sweeper start, delivered slots, late drops and Task coverage. Zero counts are not clearance; credited count evidence requires first-hand checking. An early card cap does not establish exposure of later Tasks (IP:25-27).
- **INV-018:** stop/report the arm on the overlap alarm; never change treatment mid-arm (IP:28).
- **INV-019/-020/-021:** use observed A1 reach; adopt V2's stage-2 hard-credit screen and re-derive SL2 gains (R3-V2:30-32). Repairing measurement does not establish power.
- **INV-022/-023:** clamp n; skip zero-capacity launches; balance recipient dealing. Keep atomic writes and harness-recorded hashes (R2-V3:99-101); torn transport lines must never become delivered messages.

## Remaining disagreements

1. **V1's INV-005 dealing clause:** support V2 exactly. The recomputed deal demonstrates receiver/form confounding, not a preference about wording.
2. **k = 2 as central:** support V2's k = 1 planning row. Neither is empirical expected performance; package-specific measurements supersede both.
3. **F3/F6 boundary:** support move-only F3, not Task-targeted telemetry requests. Finished findings justify keeping F6. Internal coverage bookkeeping alone is not a different mechanism.

## Final concessions

- R2-V3:46, :85, :183 confused planned-path times with worst cases. Withdraw those guarantees.
- R2-V3:54-61 used mean-turn n and overstated the panel-wide bound; :81 discarded all P2 on timeout. Adopt the shared deadline and validated streaming salvage.
- Withdraw my mid-arm decoy (:50), A5/A4 form-comparison claim (:185), and unsupported Task-by-reading-move telemetry (:107, :115).
- My timestamp test proves no independence. Original gains and out-of-block collaboration remain withdrawn (R2-V3:7-20); F6's old timing/gains need re-derivation.
- No Round 2 consensus winner changes. My minority A-011 vote changes from V2 to V5, matching T:46: cap never-found issue gains against measured reach.

## Final slate

| Slot | Family | Core | Grafts | Reason |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | V4-3 Axis-Flip Challenge | Balanced anchors; contradiction-to-M7; gaps booked to prompting; per-attempt n; shared deadline; streamed salvage; immutable repaired P1 | Exit-sealed first pass survives P2 failure. At B = 116, phase-2 deadline = 150.8 s, not a bound on late P1. |
| 2 | F4 Searcher-to-reader fact relay | V4-2 Idle-Shift Sweeper | Disjoint locators; witness sweep kind; first-hand rule; atomic delivery; snapshot; k and late-drop logs | Search-to-reader mechanism. B = 116, turn = 6.4 gives plans 130.8 s at k = 1 and 143.6 s at k = 2. |
| 3 | F3 Content-free coverage steering | V4-1 Move Radar | Observable signatures; move-only payload; reading kit booked to A2; variable-field leak check; skip rule; k | Tests telemetry timing versus static kit; collaboration may be negligible. |
| 4 | F6 Steering a running strong model | V4-5 Coverage Deflection on SL2 | Finished findings only; uncovered-Task requests; no counts/telemetry/SendMessage; surface filter; sonnet k | Distinct source and form. B = 273.7, turn = 14 gives plans 303.7/331.7 s at k = 1/2, not enforced ceilings. |
| 5 | F7 Directed challenge | V4-4 Flag-and-Adjudicate, EL2, one way | V2 enum-only forms and online deal; cap 2k; slot logs; snapshot; overlap stops arm | Within-F7 comparison without receiver confounding. Missing/late slots remain visible; timing as F4. |

Proposed base document: V4

## Per-point positions

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
