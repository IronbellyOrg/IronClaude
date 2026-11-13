# Round 1 summary (orchestrator-written digest of the three advocate transcripts; verdict tables copied as returned)

Advocates: adv1 = variant 1 (sonnet class), adv2 = variant 2 (haiku class), adv3 = variant 3 (opus class). Each read the diff analysis, the three cards, the plan and the spec.

## Shared assumptions
- A-001 (prose requirements without an AC do not gate): adv1 QUALIFY, adv2 QUALIFY, adv3 QUALIFY. Common reason: task prose still binds the implementer; a missing check is blocking only when a plausible wrong implementation causes material failure.
- A-002 (spec is correct, only the plan can be at fault): adv1 REJECT, adv2 REJECT, adv3 REJECT. Common reason: the spec itself omits the `--read` JSON mapping (spec 88-90), the request-key builder (spec 184) and the release inputs of resume row 4 (spec 109, 166).

## Per-point verdicts (winner, confidence)
| Point | adv1 | adv2 | adv3 |
|---|---|---|---|
| C-001 cycle-id continuity | V1, 65 | none, 82 | none, 86 |
| C-002 fsync order | V1, 55 | V1, 78 | none, 75 |
| C-003 GuardRead mapping | V1, 55 | V1, 77 | V1, 68 |
| C-004 request key builder | V1, 60 | V1, 73 | V1, 72 |
| C-005 resume release inputs | V1, 70 | V1, 86 | V1, 68 |
| C-010 Task 11 names only | V2, 70 | V2, 90 | V2, 91 |
| C-014 pin start text | V3, 65 | V3, 88 | V3, 94 |
| X-001 severity conflict | none, 60 | none, 85 | none, 84 |
| X-002 cycle-id ownership | none, 70 | none, 90 | V3, 96 |
| X-003 guard None | none, 70 | none, 95 | V2, 89 |

## Points the advocates agreed on in their text
- Concessions by adv1: its F1 claim "no task edits that wiring" is wrong (plan line 124 assigns reuse to Task 8 prose); only the missing AC survives. Its F8 (engage rows with guard None) is a real spec gap but Task 4's row-11 test (plan line 73) would catch a literal build, so it is not blocking. Its F2 (fsync order) rests on an explicit instruction (plan 124, spec 178); the gap is an unverified order.
- adv3 and adv1 both say C-014's "blocking" label overstates the evidence: plan line 21 and the existing pins already protect the sentences.
- adv2 and adv3 call C-010 a weaker check, not a missing behavior.
- adv2 and adv1 both hold C-005 as a real spec/plan interface gap; adv2 and adv3 do not call it a shipped wrong outcome by itself, adv1 does (blocking) if a default `applied_edits=0` releases without proof.
- Not debated in Round 1: C-006, C-007, C-008, C-009, C-011, C-012, C-013, S-001 to S-004, U-001 to U-003.
