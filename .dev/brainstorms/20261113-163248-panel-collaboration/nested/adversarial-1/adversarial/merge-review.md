# Merge review: merged-spec.md

Document: `.dev/brainstorms/20261113-163248-panel-collaboration/nested/adversarial-1/merged-spec.md` (1,124 lines, read in full)
Brief: `.dev/brainstorms/20261113-163248-panel-collaboration/seed-brief.md`

Verdict: FAIL

Two blocking findings, both in the document's own numbers. Neither touches the structure, the time-budget arithmetic of the five redesigns, or the comparison table.

## R1-R8

| Req | Result | Evidence |
|---|---|---|
| R1 five top-level sections | PASS | `##` headings at L73 (theories), L169 (redesigns), L892 (comparison), L916 (first experiment), L991 (requirements). A reading guide and symbol table sit before section 1 (L6-68), and an "unmeasured items" table and risks list follow section 5 (L1099-1124). Neither is a sixth numbered section. |
| R2 three theories, each redesign maps to one | PASS (minor note M1) | T1, T2 (T2a/T2b) and T3 at L79, L97, L118. Mapping is by the gate funnel (L136-147) and the issue-to-theory table (L153-164). F1 and F7 name T2a/T2b inline (L584, L651, L758-762). F3 and F6 have no inline theory tag. |
| R3 five redesigns, elements (a)-(h) | PASS | See the per-redesign table below. Arithmetic recomputed for all five. |
| R4 comparison table matches sections | PASS | Spot-checked 6+ numbers per redesign, all match: F1 134.8/147.6 s, C 0.06-0.63, P 0-0.10, I7 0.05-0.20, 165 LOC. F4 130.8/143.6 s, C 0.07-0.34/0.14-0.67, I7 0.09-0.25/0.17-0.50, 180 LOC. F3 C 0-0.24/0-0.48, P 0.04-0.20/0.08-0.40, 230 LOC. F6 303.7/331.7 s, C 0.07-0.53/0.13-1.06, 120 LOC. F7 C 0.04-0.39/0.08-0.77, I7 0-0.05/0-0.10, 180 LOC. Token overheads (7.2k/21.2k = 34%, 9.6k = 45%, 5.6k = 26%) and tokens per added issue (62.6k, 71k, 70k) also recompute. |
| R5 first experiment | PASS | L916-986. Runs on the three existing packages (L945: a run is one panel on all three packages), scored by the unchanged sha256-pinned `judge-one.sh` (L947). Fisher thresholds recomputed: 495/10,626 = 0.047; 220/2,024 = 0.109; 11,880/346,104 = 0.034; 10,428/134,596 = 0.077; 58,432/1,307,504 = 0.045. Run counts: 4+12+12+4x12 = 76; 52 at the interim look; stage 2 = 12+6+12 = 30. |
| R6 numbered requirements with verification | PASS | R-01..R-47 (L997-1094), each with a Verification cell. R-35 (card forms) and R-15 (n values) recompute correctly. |
| R7 no internal contradiction in load-bearing number or rule | FAIL | Blocking findings 1 and 2 below. |
| R8 brief constraints | PASS | Read-only: `--disallowedTools` plus audit (L249, L1038, R-09). No ground truth in messages: R-07, R-08 and the guard at L964. findings-v1 merge unchanged: R-04, R-16. No Opus reviewer: "opus" appears only in provenance comments, and the judge is the existing pinned one. Qwen and glm: no mention. Grok is explicitly unused (L887). |

## Per-redesign elements

| Redesign | a mechanism and roles | b schedule (triggers, frequency, per-reviewer caps, size, schema) | c transport and why | d time arithmetic vs named baseline, planned end <= +35% | e contamination and measurable alarm | f gain low/high, C and H separate, issue-tied | g effort | h failure modes |
|---|---|---|---|---|---|---|---|---|
| 1 Move Radar (F3) L376 | Y | Y (L392-401) | Y (L403) | Y: EL2 116 s; 130.8 s (+12.8%) and 143.6 s (+23.8%) | Y (L421-428) | Y: C 0-0.48/0-0.24, P and H separate; I4, I5, B8, B6, B1, B2, B5, I1, I6, I7 | Y: 230 LOC | Y |
| 2 Idle-Shift Sweeper (F4) L477 | Y | Y (L492-504) | Y (L506) | Y: EL2; 130.8 s and 143.6 s; sweeper 41+6+32 = 79 s | Y (L525-532, plus ECHO) | Y: C 0.14-0.67/0.07-0.34; rows sum correctly; I7 0.17-0.50 | Y: 180 LOC | Y |
| 3 Axis-Flip Challenge (F1) L570 | Y | Y (L597-609) | Y (L611-620) | Y: EL2; 147.6 s (+27.2%) or 134.8 s (+16.2%); killed at 150.8 s (+30%) | Y (L638-647, ECHO, sealed-report judging) | Y: C 0.06-0.63, subtotals 0.09/0.63, x2/3 low end; P and H separate | Y: 165 LOC | Y |
| 4 Flag-and-Adjudicate (F7) L699 | Y | Y (L711-722) | Y (L724-726) | Y: EL2; 130.8 s and 143.6 s | Y (L744-752) | Y: C 0.08-0.77/0.04-0.39, rows sum correctly | Y: 180 LOC | Y |
| 5 Coverage Deflection (F6) L797 | Y | Y (L809-821) | Y (L825) | Y: SL2 273.7 s; 303.7 s (+11.0%) and 331.7 s (+21.2%) | Y (L843-849, deflection alarm) | Y: C 0.13-1.06/0.07-0.53, H +0.1 to +0.4 UNVERIFIED | Y: 120 LOC | Y |

Arithmetic recomputed and confirmed:
- Baselines: 348/3 = 116 s, 821/3 = 273.7 s, 715/3 = 238.3 s.
- PANEL_FINISH_AT: 1.35 x 116 - 12.8 = 143.8 s.
- k formula: floor(25.8/12.8) = 2.
- The T_report thresholds in the L281-287 table (6.6, 19.4, 8.0, 20.8, 8.7, 21.5, 1.0, 13.8, 23.8, 51.8).
- The 1.30/1.35/1.50 B deadlines for EL2, HL2 and SL2.
- F1 phase-2 rows (126.6, 147.6, 134.8, 146.8, 141.2 s) and the HL2 shadow (173.2 s, 253 s = +6.3%).
- The 4/9 and 1/9 gap-card probabilities.
- The drift edge 0.963.
- The slowdown limits 5.7% and 11.2%. The F6 limit does not recompute: see finding 2.

## Blocking findings

1. **L194 states "No gain row in this specification exceeds it", but many gain rows exceed the c ceilings, and F6's total exceeds the 1.04 sum.**
   - L194 says c sums to 1.04 and is "a ceiling, not a forecast. No gain row in this specification exceeds it."
   - Total: F6's C high end is 1.06 (L863, L867, L901), above 1.04.
   - Per-row against the catalogue c column (L178-187):
     - F7: B1 0.16 (L758) against M3 0.050; B2 0.08 against M9 0.050; B5 0.15 (L761) against M5 0.125; I1 0.10 against M6 0.075.
     - F6: B1 and B2 0.10 each (L860) against 0.050; I1 0.10 (L861) against 0.075.
     - F4: I5 0.24 (L538) against M7 0.140 (or M1 0.215); B8 0.20 (L539) against M2 0.185.
     - F3: P rows B5 0.15 against 0.125 and I1 0.10 against 0.075 (L441).
   - The sentence is false as written. A reader will take every gain range as bounded by c when it is not. The sentence does not say the ceiling applies only to cheap-model receivers.
   - Exact fix: replace L194's last sentence with "The c column bounds a cheap model that carries out the move unaided. Rows whose route delivers a located fact, a card or a request (F4, F6, F7) and F6's sonnet receiver can exceed it; those rows are planning values and are labelled as such." Alternatively, cap the rows above to their c values and F6's high end to 1.04.

2. **L295: the F6 slowdown limit uses W = 56 s, which is inconsistent with the definition of W used for the other slots.**
   - F3's W = 27.6 s is hooks 2 s + 2k x turn (25.6 s). F4 and F7's W = 34 s is that plus one 6.4 s turn of slip (L281, L410-415).
   - F6's planned end at k = 2 is 273.7 + 58 s (L833), so the same definition gives W = 58 s (hooks 2 s + 4 x 14 s). With slip it would be 72 s.
   - W = 56 s omits the 2 s of hooks.
   - So the F6 limit (0.35 x 274 - W)/274 is 13.8% with W = 58 s, not the stated 14.6% (14.56% with W = 56 s). The 14.6% also appears in R-45 (L1092) and is used there to decide when to drop brief content.
   - Exact fix: at L295 and R-45 change "F6 14.6% (W = 56 s ...)" to "F6 13.8% (W = 58 s = hooks 2 s + 4 x 14 s, computed at B = 274 s)". If slip is intended, state it and recompute for all slots.

## Minor notes

- M1. F3 and F6 have no inline "theory addressed" line. The mapping exists only through the gate funnel (L138-147) and the issue-to-theory table (L153-164). Add one line to each redesign.
- M2. L124 says "4 of the 9 target issues masked", but the brief and L164 count ten missed issues. 9 is presumably the designSpec and alias issues without I7. Say so.
- M3. L291 and L633 say F1's phase-2 end is "the only bound enforced by a kill". The hang guard (L323) and the F4 sweeper timeout (L1030) are also kills, though not +35% bounds. Reword to "the only +35%-related bound".
- M4. The mid-run designs (F3, F4, F6, F7) cap time by audit rather than a kill. Their planned ends are at most +27.2%, but the enforced ceiling is +50% (hang guard). This is disclosed honestly (L291, L419), but the brief's "at most 35%" is met on the planned path only.
- M5. "1 package in 12" (L963, R-24) is ambiguous. Arms are 12 runs x 3 packages = 36 package-runs. State the denominator.
- M6. F3's B6 route uses M2 (L437), while the issue-to-theory table (L158) maps B6 to M10. Make them agree.
- M7. Redesign numbers (1-5) run in a different order from the slot order (3, 2, 1, 5, 4). This is documented at L28.
- M8. For F1, the CONVERGENCE alarm uses only sealed phase-1 own lines, so it cannot detect convergence caused by phase 2. ECHO covers that. The document says this at L234.

## Re-review 1
| Finding | Status (closed/open) | Evidence |
|---|---|---|
| 1. c-ceiling sentence (L194) | open | The false sentence "No gain row in this specification exceeds it" is gone, and the new text is correct for the cases it names (F7 B1 0.16 vs M3 0.050 at L758; F6 total high end 1.06 vs the 1.04 sum). But it says only F4, F6, F7 and F6's sonnet receiver can exceed c, and that is still false. F3's luna rows (L441, route M5/M6 sent to luna, a cheap model acting unaided) have B5 high end 0.15 against M5 c = 0.125 and I1 high end 0.10 against M6 c = 0.075. F3 is not in the exception list and its rows are not labelled planning. So "ceiling ... for a cheap model that carries out the move unaided" is still contradicted by a row. Fix: add F3 to the list (and label its luna rows planning), or cap them at 0.125 and 0.075. |
| 2. F6 slowdown limit (L295, R-45 L1092) | closed | Recomputed: (0.35 x 273.7 - 58) / 273.7 = (95.795 - 58) / 273.7 = 0.1381, i.e. 13.8%. W = 58 s = hooks 2 s + 4 x 14 s, which matches the F6 k = 2 row at L833 (273.7 + 58 = 331.7 s, +21.2%, repeated at L837 and L901). L295 and R-45 both say 13.8%. Grep of the whole document for "14.6", "14.5", "W = 56", "56 s" and "exceeds it" returns nothing. |

Verdict after re-review 1: FAIL

## Re-review 2 (final)
| Finding | Status (closed/open) | Evidence |
|---|---|---|
| 1. c-ceiling sentence (L194) | closed | Every claim in the rewritten sentence checks against the catalogue and the cited rows. c column (L178-187): M5 0.125, M6 0.075, M3 0.050; the eight V5 values sum to 0.215 + 0.185 + 0.050 + 0.200 + 0.125 + 0.075 + 0.140 + 0.050 = 1.04, with M7 and M8 sharing 0.140 once. F3 luna rows (L441): B5 high end 0.15 against M5's 0.125, and I1 high end 0.10 against M6's 0.075. F7 (L758): B1 high end 0.16 against M3's 0.050. F6 (L867): C /14 high end 1.06 against the 1.04 sum. F3 is now named, which closes the Re-review 1 gap. The sentence says "several high ends exceed" and calls every gain row a planning value, so it no longer claims that c bounds the rows. A grep for "ceiling" and "exceed" finds no other sentence claiming c bounds gain rows. The remaining hits are the L173 and L176 labels, the time-related "enforced ceiling" lines (L290, L417, L521, L740, L839, L896) and unrelated alarm or budget thresholds (L233, L295, L963, L966, R-25, R-45). |
| 2. F6 slowdown limit (L295, R-45) | closed | Not re-opened. L295 and R-45 still say 13.8% with W = 58 s. The new edit touched only L194. |

Verdict after re-review 2: PASS
