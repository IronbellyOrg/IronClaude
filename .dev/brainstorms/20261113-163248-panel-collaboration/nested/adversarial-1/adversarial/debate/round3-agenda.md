# Round 3 agenda (orchestrator; neutral)

Status after Round 2: diff-point agreement 43/43 (1.000, `round2-tally.md`), taxonomy levels L1/L2/L3 all covered, but **CONVERGENCE BLOCKED_BY_INVARIANTS**: the Round 2.5 fault-finder (`../invariant-probe.md`) found 8 HIGH-severity UNADDRESSED items: INV-001, INV-002, INV-003, INV-004, INV-005, INV-006, INV-007, INV-008. 13 MEDIUM items are warnings (do not block) but the merge should close the cheap ones.

Each HIGH item must be closed in this round: either ACCEPT the probe's required resolution (section "Required resolution" in `../invariant-probe.md`), MODIFY it (give the exact replacement rule and why), or REJECT it with evidence that the consensus already handles it. Only these outcomes close an item: a 4-of-5 majority on ACCEPT or on one specific MODIFY text, or a 4-of-5 majority on REJECT.

## Orchestrator-measured fact for INV-008 (per-package isolated elapsed, slowest reviewer per package)

Computed from `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<package>/reviews/combos/<run>/t*.meta.json` (`wall_s`, max per package-run; non-attempt meta files only). Format: package: (runs, median s, min s, max s).

| Panel | designSpec (DS) | makeTheAliasOnly (AL) | design (DE, control) |
|---|---|---|---|
| ember + 2x luna (g1-*, e2-ember-luna2-rep) | 5, 100, 92, 123 | 5, 120, 98, 171 | 5, 122, 86, 155 |
| ember + luna (g9-*) | 4, 79, 61, 121 | 4, 114, 103, 130 | 4, 100, 85, 115 |
| haiku + 2x luna (g7-*) | 4, 220, 159, 305 | 4, 238, 230, 285 | 4, 226, 163, 297 |
| sonnet + 2x luna (j1-*, b4-sonnet-luna2) | 6, 259, 196, 283 | 6, 302, 208, 416 | 6, 269, 184, 440 |

Reading: the 116 s EL2 planning value is a 3-package mean; the designSpec median (100 s) and single runs (86-98 s) sit near or below the 97.1 s floor the probe computed for F3/F4/F7. Run-to-run spread inside one package (e.g. AL 98-171 s) is larger than any design's added time, so a per-run cap check against the historical number cannot be the test; per-package medians over an arm can.

## Questions beyond the 8 HIGH items

- INV-006 may change the slate. If F6 cannot be stated as a distinct mechanism from F3, the probe names F2 (mid-run method relay, V5-D2 / V2-D3, the only I6 trigger) as the replacement. Decide: keep F6 under the probe's distinctness definition, or replace it.
- INV-005: accept the within-arm challenge-form vs finding-form contrast in F7, or say SEED:47 is answered descriptively only.
- State your final slate and the remaining disagreements.
</content>
</invoke>
