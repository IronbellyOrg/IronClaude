# Merge Log

Base: variant-2-original.md (V2). Merged output: merged-output.md. All 12 planned changes applied, in order.

| # | Status | Provenance tag used | Where it landed |
|---|---|---|---|
| 1 | Applied | `Source: Variant 1, merged per Change #1` | Decision; Design "What runs"; Rejected (outer wrapper) |
| 2 | Applied | `Source: Variant 1, merged per Change #2` | Design "Rate wait"; Risks INV-002 |
| 3 | Applied | `Source: Variant 1, merged per Change #3` | Design "Launch brake"; Risks INV-005 |
| 4 | Applied | `Source: Variant 1, merged per Change #4` | Design "Loop cap"; Risks INV-006 |
| 5 | Applied | `Source: Variant 1, merged per Change #5` | Design "Where state lives"; Risks INV-001 |
| 6 | Applied | `Source: Variant 1, merged per Change #6` | Code that must change (github.py:37, 187, 208, 259; launch.py:50, 249); Risks INV-003, INV-009 |
| 7 | Applied | `Source: Variant 1, merged per Change #7` | Requirements (R10); Risks INV-003, INV-004 |
| 8 | Applied | `Source: Variant 1, merged per Change #8` | Requirements (R11); Risks INV-010 |
| 9 | Applied | `Source: Variant 1, merged per Change #9` | Design "The loop"; Risks INV-007 |
| 10 | Applied | `Source: Variant 1, merged per Change #10` | Design "The loop"; Risks INV-007, INV-008 |
| 11 | Applied | `Source: Variant 1, merged per Change #11` | Design "Config generator"; Risks INV-011 |
| 12 | Applied | `Source: Variant 1, merged per Change #12` | Requirements (R6, R9, R10, R11); Risks INV-012 |

Sections carried from the base keep `Source: Base (V2)`. Changes 5 to 12 come from the invariant probe, not Variant 1; the tag form follows the instruction's two allowed forms, and the plan's Source column names the real origin.

## Notes
- Base V2 said "no change to github.py"; Change #6 overrides it, and the output says the claim was false.
- V2 gave the old default state path as cycle.py:187-192; the probe gives cycle.py:259-266 for the fallback. The output uses only 259-266 and omits 187-192 to avoid two conflicting citations.
- The "Changes NOT Being Made" list went into "What was rejected and why". The in-process loop item rests on base-selection.md (V2 strength: one child per repo with a kill timer).
- Word count of merged-output.md outside the comment tags: 697 (limit 700). No em dashes.

## Post-merge validation
1. Headings consistent: six required sections in the required order under one title; each has provenance tags at the top.
2. References resolve: every file:line in the output appears in the inputs (github.py:37, 187, 208, 259, 418-431; launch.py:50, 249; cycle.py:35, 36, 41, 195, 259-266, 373-375, 685-686, 872-876, 1091-1099; record.py:283, 381-403, 422; predicates.py:224-225); INV-001 to INV-012 each appear once in Risks.
3. No new contradiction: the base's "no change to github.py" and the conflicting state path citation were removed or corrected; the "cycle logic unchanged" claim was dropped in favour of the code-change list.
