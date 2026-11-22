# Base Selection (D08)

Method note: scores below are the judge's own estimates from reading both variants and the verification log. They were not produced by a script, and the dual-pass position-bias check was not run as two independent evaluators (single judge, variants read in both orders when the table was filled). Treat the numbers as indicative; the base choice does not rest on them (see the tiebreaker).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) | Note |
|---|---|---|---|---|
| Requirement coverage (role name, command name, nesting of 339/423/444 and Clay's design) | 0.30 | 0.75 | 0.85 | V1 points to a nesting table it does not contain |
| Internal consistency | 0.25 | 0.90 | 0.88 | V1: IronOrchestrator as an identifier, 13 vs 15 count. V2: "Decided" overreach, R10 inference |
| Specificity | 0.15 | 0.90 | 0.90 | Both cite lines and counts |
| Dependency completeness | 0.15 | 0.85 | 0.95 | V1 dangling reference |
| Section coverage | 0.15 | 1.00 | 1.00 | Same six headings |
| **quant_score** | | **0.863** | **0.903** | |

## Qualitative Scoring (50% weight)

Dimension subtotals (of 5 each), judge estimates with the CEV evidence in diff-analysis.md:

| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 3 | 4 |
| Correctness | 3 | 3 |
| Structure | 4 | 4 |
| Clarity | 4 | 4 |
| Risk coverage | 3 | 4 |
| Invariant and edge-case coverage | 2 | 2 |
| **Total / 30** | **19** | **21** |
| qual_score | 0.633 | 0.700 |

Edge-case floor (1 of 5): both pass (2 of 5).

## Combined Scoring

variant_score = 0.5 x quant + 0.5 x qual: V1 = 0.748, V2 = 0.802. Margin 5.4 points, just above the 5 percent tiebreaker trigger, so by score alone the protocol would pick Variant 2. **Documented override:** the scores grade the two papers as first written (V2 won on completeness and on the nesting answer, V1 lost points for a dangling reference and two wrong counts). After Rounds 1 and 2 both advocates agree those paper-level gaps are fixed: Advocate 2 withdrew the role noun and the command word, Advocate 1 withdrew its own errors. The debate outcome and the owner-ordered weighting rule (OURS wins unless CLAY shows a clear evidenced benefit) therefore decide the base, not the paper scores. The override is recorded here and in the return contract (`fallback_mode: true`).

## Tiebreaker and base decision

- Level 1, debate performance: Variant 1 won the contested substance (C-001, C-002, C-007, C-009, C-010, C-012, C-014, X-001, X-003, X-006 to X-011). Variant 2 won C-004, C-008 (timing) and part of C-006. Variant 1 wins on points.
- Weighting rule (owner order): OURS wins unless CLAY shows a clear evidenced benefit. Advocate 2 stated in Round 2 that it sees none that OURS-with-hybrid lacks.

## Selected Base: Variant 1 (OURS, one noun "coordinator")

Strengths to preserve: one role noun; owner rows R9, R10, R17; `/sc:coordinator`; `COORD-<RepoName>`; titles of 339, 423, 444 unchanged with a glossary.

Strengths to incorporate from Variant 2 (HYBRID items, each separable from the contested word):
1. The full flag set `--wake`, `--hourly`, `--resume`, `--take` (D:133) and `--sub` kept unchanged.
2. The species term "standing-grant coordinator" (D:799) and a contract section for the orchestrated issue flow (ADD1).
3. The deployed report-session names unchanged (tag `coordinator`, prefix `coordinator-`, `.dev/coordinator/`), called "report coordinator".
4. The process name "orchestrated issue flow" and the existing folder `.dev/coordinator/orchestrated/`.
5. A nesting table for 339, 423, 444, Clay's design and the report session.
6. The deadline: settle every persisted name before PR 686 merges.

## Invariant gate resolution (INV-001, HIGH)

Judge's rule added to the base: authority comes only from a recorded owner authorization (the per-issue grant row, or the authorization the launch prompt cites, D06 items 6 and 7). Not from the command, a flag, the session name or the word. A flag-less `/sc:coordinator` creates no grant and starts no merge, with a test. The owner's R17 launch-prompt route is a `--wake` or `--take` call, so the standing authorization has one door.
