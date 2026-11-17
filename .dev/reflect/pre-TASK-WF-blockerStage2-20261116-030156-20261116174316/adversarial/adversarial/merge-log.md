# Merge Log (Step 5)

## Inputs
- Base: variant-3-original.md (reviewer card 3, refactorer).
- Plan executed: refactor-plan.md (P-1 to P-10, auto-approved).
- Output: ../merged-review-card.md (4 blocking findings, 15 non-blocking findings).

## Planned changes

| # | Change | Status | Provenance tag | Result in the merged card |
|---|---|---|---|---|
| P-1 | Add MB-1 (Task 8 bare confirmation ids vs run-scoped ids) as BLOCKING | applied | `<!-- Source: Variant 2, R2-1, merged per P-1 -->` | MB-1, first in Findings; fix direction `run_id:id` plus a colliding-id test across two runs |
| P-2 | Add MB-2 (Task 7 agents see only the blind table) as BLOCKING, noted CONTESTED | applied | `<!-- Source: Variant 2, R2-2, merged per P-2 -->` | MB-2; A2 blocking 90, A1 minor 65, A3 wording 40 recorded; fix direction: blind table plus the supplier's inputs for that row |
| P-3 | Add MB-3 (GR12 safety row to `partial` missing from Task 5) as BLOCKING | applied | `<!-- Source: Variant 1, R1-2, merged per P-3 -->` | MB-3; A1 70, A2 conceded; fix direction: add the mapping to WC-4 and a test |
| P-4 | Keep and narrow MB-4 (phases 3 and 5 analyst and qualitative reviewers get no `rests_on` fields; two of five edited templates LEGACY) as BLOCKING | applied | `<!-- Source: Variant 3, R3-3, merged per P-4 -->` | MB-4 with the narrowed claim and the round 2 evidence (SKILL.md:479-487, 507-516, 819, 952, 1003, rf-analyst.md:195-202) |
| P-5 | Downgrade R3-1 to non-blocking medium MN-1 and add INV-001 | applied | `<!-- Source: Variant 3, R3-1 reduced, plus INV-001, merged per P-5 and P-9 -->` | MN-1 (medium); "by construction" claim withdrawn; fix: one acceptance line |
| P-6 | Downgrade R3-2 to non-blocking MN-2 | applied | `<!-- Source: Variant 3, R3-2 reduced, merged per P-6 -->` | MN-2 (minor); residue: no family selector, two column layouts |
| P-7 | Add MN-3 (/sc:implement sweep has no ledger; unconditional printed line) | applied | `<!-- Source: Variant 1, R1-1 reduced, with Variant 3 follow-up candidate 1, merged per P-7 -->` | MN-3 (medium) |
| P-8 | Add minor items from V1: call-line (with R3-5), printed-list producer (R1-4), no unattended mode (with R3-7) | applied | `<!-- Source: Variant 1, R1-3, merged with Variant 3, R3-5, merged per P-8 -->`; `<!-- Source: Variant 1, R1-5, merged with Variant 3, R3-7, merged per P-8 -->`; `<!-- Source: Variant 1, R1-4, merged per P-8 -->` | MN-5, MN-6, MN-7 |
| P-9 | Add INV-002, 003, 004, 005, 006, 007, 008, 009, 010 as follow-up or minor items (INV-001 is under P-5) | applied | `<!-- Source: Invariant probe, INV-nnn, merged per P-9 -->` | MN-10 (INV-009), MN-11 (INV-008), MN-12 (INV-003), MN-13 (INV-004, INV-005), MN-14 (INV-002), MN-15 (INV-006, INV-007, INV-010) |
| P-10 | Keep R3-4, R3-6, R3-8 as minor; withdraw R2-3; T1 F5 and F7 as non-defects | applied | `<!-- Source: Variant 3, R3-4, with Variant 2 refutation of F3 (plan:59), merged per P-10 -->`; `<!-- Source: Variant 3, R3-6, merged per P-10 -->`; `<!-- Source: Variant 3, R3-8, merged per P-10 -->`; `<!-- Source: Invariant probe, INV-009, merged per P-9 and P-10 -->` | MN-4 (with the plan:59 correction), MN-8, MN-9; R2-3, F5, F7 listed under "Refuted or withdrawn"; F5 kept only as the wording tension MN-10 |

Skipped changes: none.

"Changes NOT being made" in the plan were honored: R2-3 is not a finding, the R3-1 "by construction" claim is not carried, R1-1 is not in the blocking list.

## Structure
- Base structure kept: header, reviewer-card fields per finding, then Refuted, Checked no defect, Follow-up candidates, verdict.
- Added to the base: provenance and debate outcome fields on every finding, a citation key, and `### Blocking` and `### Non-blocking` subheadings under `## Findings` (blocking first, as ordered).
- Base items dropped as separate entries: R3-5 and R3-7 (merged into MN-5 and MN-6). The base card's own calibration block and "Refuted T1 findings" paragraph are not carried; the refuted items are re-listed from the register.
- Base follow-up candidates: the first (no ledger under /sc:implement) is merged into MN-3; the second (stage 1 names no public functions) and third (LEGACY templates) are not separate register items; the LEGACY point is inside MB-4. The register had no id for the second candidate, so it is not added.

## Validation

| Check | Result |
|---|---|
| Every citation in the merged card appears in a source card or the transcript | PASS. Citations for MB-1 to MB-4, MN-3 to MN-9 are copied from the source cards. Extra citations in MN-1 (stage1 plan:194, 198-202, plan:61), MN-2 (rf-qa.md:448, rf-qa-qualitative.md:883, SKILL.md:900, 1147-1149, spec:744, plan:29), MN-4 (plan:59, 39-44), MB-4 (SKILL.md:400, 404, 864, 911, 483, 511) come from the round 2 transcript or card 2. MN-10 to MN-15 citations come from invariant-probe.md. No citation was invented. |
| Quotes copied verbatim from the source card | PASS. MN-10 to MN-15 quotes are the probe's Evidence and Assumption text, since the probe is the source card for those items. MN-4 keeps the base card's quote. |
| Heading hierarchy | PASS. `#` title; `##` Findings, Refuted or withdrawn, Checked no defect, Follow-up candidates; `###` Blocking and Non-blocking only under Findings. |
| Order | PASS. BLOCKING MB-1 to MB-4 first, then MN-1 to MN-15 in register order. |
| Counts | 4 blocking, 15 non-blocking (MN-1 to MN-15; 6 of them medium: MN-1, 3, 11, 12, 13, 14). The probe's own summary line miscounts MEDIUM as 5 and corrects itself to 6 (INV-001, 002, 003, 004, 005, 008); the merged card uses the corrected figure. |
| Follow-up candidates match the register | PASS. Lists MN-1, 3, 11, 12, 13, 14, one line each. |
| No new contradiction | PASS. MN-4's correction (Task 2 checks `classify`, plan:59) agrees with MN-4 limiting the late failure to the scale-map and registry files; MN-3 says the sweep finds no ledger and MN-7 refers back to it without conflict; MB-3's "latent today" matches plan:138's note that no live emitter exists. MB-2 is marked CONTESTED and its verdicts are not smoothed. |
| Findings outside the register | None added. Fix directions are included only where the source card or the transcript gives one (MB-1, MB-2, MB-3, MN-1, MN-2, MN-3, MN-5, MN-6, MN-9); MB-4, MN-4, MN-7, MN-8 and MN-10 to MN-15 have none. In MN-12 to MN-14 the fix wording appears only in the Follow-up candidates section, taken from the claim itself. |
| Verdict and score | `NEEDS-REVISION (4 blocking)`; `convergence_score: 0.90 (19 of 21 diff points agreed; C-004 and C-005 split)`, as instructed. |

## Notes for the orchestrator
- The one-line follow-up directions for MN-11 to MN-14 in the Follow-up candidates section are derived from each item's own claim; the probe gives no fix text for them. Strike them if only probe-stated fixes are wanted.
- Nothing was run; the merge is a read-only document merge.
