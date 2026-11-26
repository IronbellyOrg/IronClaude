# Adversarial Debate Transcript (index; the full rounds are the files named below)

## Metadata
- Depth: standard (Round 1 parallel, Round 2 sequential, Round 2.5 invariant probe; no Round 3)
- Rounds completed: 2 plus Round 2.5
- Advocates (3): V1 `haiku:analyzer` (defend the default), V2 `sonnet:analyzer` (attack), V3 `sonnet:architect` (best alternative). The Round 2.5 fault-finder was a separate `sonnet` agent. No Opus agent was used anywhere.
- Orchestrator and merge executor: the main session (`claude-sonnet-5-5`), not the `debate-orchestrator` and `merge-executor` agents (their model could not be pinned away from Opus)
- Convergence threshold: 0.80. Focus areas: all
- Files: variants `variant-1-haiku-defender.md`, `variant-2-sonnet-prosecutor.md`, `variant-3-sonnet-architect.md`; Round 1 `debate/round1-V1.md`, `round1-V2.md`, `round1-V3.md`; Round 2 `debate/round2-V1.md`, `round2-V2.md`, `round2-V3.md`; probe `debate/invariant-probe.md`; evidence `work/evidence-pack.md`, `work/band_sim.out`, `work/v3_rule_sim.out`

## How the positions moved
- Variants: V1 PASS; V2 FAIL (B-1 to B-4); V3 FAIL "narrowly".
- Round 1: V2 dropped B-2 (alone), B-3 and B-4 as blockers, keeping B-1; V3 dropped "impossible by construction", the 3-distinct-items floor and the claim that the mismatch breaks an interval rule; V1 dropped "preserve original definitions" and "non-gating means inert", but kept PASS.
- Round 2: V1 changed to FAIL (narrowly, on the unnamed measure). V2 and V3 agreed the denominator is act-and-survive among selected item-runs, 95% Wilson, minimum 10 item-runs, caveat not deletion, below-only consequence, no pooled band.
- Round 2.5: 23 probe rows, 1 HIGH unaddressed (INV-013, panel scope). Fixed in the merge text, not re-debated (depth standard has no Round 3).

## Scoring Matrix

| Diff point | Winner | Confidence | Evidence summary |
|---|---|---|---|
| S-001 shape of the text | V3 | 60% | a labelled measure/rule/consequence list; V1 accepted an exact sentence |
| S-002 where the consequence lives | V3 | 60% | in the registered text, not in prose elsewhere |
| C-001 verdict | V2 | 85% | all three FAIL after Round 2 (V1 flipped) |
| C-002 denominator | V2 | 80% | act-and-survive among selected, same quantity as the band (MR 539); V1 and V3 moved to it |
| C-003 interval | V3 | 80% | 95% Wilson, repo constant `WILSON_Z` 1.96; false flag at most 0.9% |
| C-004 minimum data | V2 | 75% | 10 item-runs; V3 dropped its 3-distinct-items floor |
| C-005 consequence | V3 (amended) | 80% | below-only caveat beside the pinned REQ-45 sentence, never deletion (V1, V2) |
| C-006 scope | V3 | 85% | SS only, Stage 1 and 2 apart; the probe added primary panel only and sets apart |
| C-007 pooled or Z0 band | V3 | 80% | rejected: class-mix dependent; Z0 act is a different quantity |
| X-001 mismatch blocking? | V2 | 85% | all three agree it is the blocker |
| X-002 consequence needed? | V2 | 70% | needed in one narrow place (the C4 and C8 REQ-45 claim) |
| A-001 to A-004 | no winner | n/a | all QUALIFY (V1 REJECT on A-003); each became a text clause or a Not-checked line |

## Convergence Assessment
- Points resolved: 15 of 15 (S 2, C 7, X 2, A 4). Alignment: 100% (unanimous on C-001 to C-005, C-007, X-001; majority on S-001, S-002, X-002; A-NNN resolved by qualification).
- Threshold: 80%. Taxonomy coverage: L1 (S-001), L2 (C-006, C-007), L3 (C-002, C-004, A-001 to A-003) all covered.
- Invariant gate: BLOCKED_BY_INVARIANTS before the merge (INV-013, HIGH, unaddressed). Resolved by amendment in the refactor (Measure line: primary panel only, sets apart); the amendment was not debated.
- Status: CONVERGED on diff points, invariant gate resolved by amendment. Unresolved diff points: none. Medium-severity items logged as warnings: INV-004, 005, 008, 009, 015, 017, 020, 021 (all folded into the text or the Not-checked list except INV-021's wording risk, which the INV-004 and INV-013 fixes reduce).
