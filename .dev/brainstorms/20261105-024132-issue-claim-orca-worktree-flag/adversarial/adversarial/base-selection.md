# Base Selection Report

Variants: A = variant-1-opus-architect (opus:architect), B = variant-2-sonnet-refactorer (sonnet:refactorer), C = variant-3-haiku-qa (haiku:qa).
Evidence (single source of truth, not copied here): full Claim-Evidence-Verdict lines are in `scoring-pass1.md` (forward order A,B,C; also holds the quantitative counts) and `scoring-pass2.md` (reverse order C,B,A). Orchestrator-verified facts used by both scorers are in `diff-analysis.md` (X-001..X-004) and `invariant-probe.md`.

## Quantitative Scoring (50% weight)

| Metric | Weight | A | B | C |
|--------|--------|---|---|---|
| requirement_coverage | 0.30 | 1.000 (12/12) | 0.917 (11/12; re-claim path not pinned by a test) | 1.000 (12/12) |
| internal_consistency | 0.25 | 0.905 (2 of 21 claims) | 0.944 (1 of 18; X-003) | 0.722 (5 of 18; X-001, X-002, X-004 plus two found) |
| specificity_ratio | 0.15 | 1.000 (206/206) | 0.985 (201/204) | 0.984 (184/187) |
| dependency_completeness | 0.15 | 1.000 (12/12) | 1.000 (16/16) | 0.923 (36/39; three edge-to-test mappings cannot exercise their case) |
| section_coverage | 0.15 | 1.000 (9 of 9) | 1.000 (9 of 9) | 1.000 (9 of 9) |
| **quant_score** | | **0.976** | **0.959** | **0.917** |

Source of counts: `scoring-pass1.md` Part 1. The scorer counted tokens with grep; the specificity numbers are estimates, and the ranking does not depend on them (the largest swing between variants is 0.015).

## Qualitative Scoring (50% weight): Additive Binary Rubric (30 criteria)

Final verdicts after position-bias reconciliation (MET = 1). Evidence per cell: `scoring-pass1.md` Part 2 and `scoring-pass2.md`.

| Dimension | Criterion | A | B | C |
|---|---|---|---|---|
| Completeness | 1 covers all explicit requirements | MET | NOT MET | MET |
| Completeness | 2 edge cases and failures | MET | MET | MET |
| Completeness | 3 dependencies and prerequisites | MET | MET | MET |
| Completeness | 4 success/completion criteria | MET | MET | MET |
| Completeness | 5 out-of-scope items | MET | MET | MET |
| Correctness | 1 no factual errors | MET | NOT MET | NOT MET |
| Correctness | 2 feasible with constraints | MET | MET | NOT MET |
| Correctness | 3 consistent terminology | MET | MET | MET |
| Correctness | 4 no internal contradictions | NOT MET | MET | NOT MET |
| Correctness | 5 claims supported by evidence | MET | MET | MET |
| Structure | 1 to 5 (order, hierarchy, separation, IDs, nine H2) | 5 MET | 5 MET | 5 MET |
| Clarity | 1 unambiguous language | NOT MET | MET | NOT MET |
| Clarity | 2 concrete | MET | MET | MET |
| Clarity | 3 clear section purpose | MET | MET | MET |
| Clarity | 4 terms defined on first use (`<D>` undefined in all three) | NOT MET | NOT MET | NOT MET |
| Clarity | 5 actionable next steps | MET | MET | MET |
| Risk coverage | 1 three risks with likelihood and impact (none rated) | NOT MET | NOT MET | NOT MET |
| Risk coverage | 2 mitigation for each | MET | MET | MET |
| Risk coverage | 3 failure modes and recovery | MET | MET | MET |
| Risk coverage | 4 external dependency failures | MET | MET | MET |
| Risk coverage | 5 monitoring or validation mechanism | MET | MET | MET |
| Invariant and edge case | 1 collection boundaries | MET | NOT MET | NOT MET |
| Invariant and edge case | 2 state across component boundaries | MET | MET | MET |
| Invariant and edge case | 3 guard-condition gaps | MET | MET | MET |
| Invariant and edge case | 4 count and off-by-one | MET | MET | NOT MET |
| Invariant and edge case | 5 interaction effects | MET | MET | MET |

### Qualitative Summary

| Dimension | A | B | C |
|-----------|---|---|---|
| Completeness | 5/5 | 4/5 | 5/5 |
| Correctness | 4/5 | 4/5 | 2/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 3/5 | 4/5 | 3/5 |
| Risk coverage | 4/5 | 4/5 | 4/5 |
| Invariant and edge case | 5/5 | 4/5 | 3/5 |
| **qual_score** | **26/30 = 0.867** | **25/30 = 0.833** | **22/30 = 0.733** |

### Edge Case Floor Check

Floor: below 1/5 on Invariant and edge case coverage makes a variant ineligible as base. A 5/5, B 4/5, C 3/5. All three eligible.

## Position-Bias Mitigation

Pass 1 scored A,B,C; pass 2 scored C,B,A without seeing pass 1. Pass 2 wrote `0` where pass 1 wrote `NOT MET` (same meaning). Pass 1: A 26, B 26, C 22. Pass 2: A 27, B 26, C 21. Agreement on 84 of 90 verdicts (93%).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final (re-evaluation) |
|-----------|---------|--------|--------|-----------|-----------------------|
| Completeness 5 out of scope | A | MET | NOT MET | DISAGREE | MET: FR-12 is an explicit "MUST NOT stage, commit, push, run git worktree add, use EnterWorktree, or run orca worktree rm", and 2.1 rejects agent launch |
| Completeness 5 out of scope | C | MET | NOT MET | DISAGREE | MET: FR-10 "MUST NOT run, prompt or schedule any next-step command"; same standard as A |
| Correctness 4 no contradictions | A | NOT MET | MET | DISAGREE | NOT MET: FR-8 says the two files "MUST exist" after create or reuse, while section 6 allows "Copy fails" to leave the worktree without them |
| Clarity 1 unambiguous | A | NOT MET | MET | DISAGREE | NOT MET: "reuse first marker match" has no defined order, and FR-4 "after Wave 6 step 3 succeeded" names a failure rule as a success step |
| Completeness 1 covers requirements | B | NOT MET | MET | DISAGREE | NOT MET: success criterion 5 says tests pin the idempotent re-claim path; B's re-claim check is a manual run only (section 7 observed run), not a pinned test |
| Invariant 1 collection boundaries | B | MET | NOT MET | DISAGREE | NOT MET: B's list call has no row cap and no truncation rule (maximum size is one of the three named boundaries); A sets `--limit 500` and scores MET, although neither checks truncation (INV-001) |

Disagreements re-evaluated: 6. Final verdicts that differ from pass 1: 1 (B Invariant 1). Final verdicts that differ from pass 2: 5.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (opus:architect) | 0.4880 | 0.4335 | **0.9215** | 13 points won |
| B (sonnet:refactorer) | 0.4795 | 0.4165 | **0.8960** | 13 points won |
| C (haiku:qa) | 0.4585 | 0.3665 | **0.8250** | 1 point won |

Debate points won (Round 1 verdict tables of the three advocates, majority winner per point; a stated tie credits both): A alone: S-001, C-001, C-002, C-004, C-006, C-012, C-013, C-015, X-003 (9). B alone: S-003, C-005, C-007, C-008, C-009, C-010, C-011, C-016, X-004 (9). C alone: S-004 (1). Ties credited to A and B: S-002, C-003, X-001, X-002 (4 each). C-014 tied across all three, no credit.

**Margin**: A over B is 0.0255 (2.6 points on a 0 to 1 scale), below the 5% threshold. A over C is 0.0965.
**Tiebreaker applied**: Yes. Level 1 (debate points won): A 13, B 13, tie. Level 2 (Correctness criteria MET): A 4, B 4, tie. Level 3 (input order): A.

Honest reading: A and B are statistically level; the rule picks A only by input order. The choice matters little because the merged design (refactor-plan.md) takes B's file-surface and copy rules and C's test mapping.

## Selected Base: Variant A (opus:architect)

### Selection Rationale

A leads on quant (0.976) and on correctness evidence that no orchestrator-verified fact contradicts: its census of eight versioned commands is right (X-002), its Wave 6 handling is right (X-001), and its `--git-common-dir` repo resolution works from a linked worktree (verified). It is the only variant with Orca-call timeouts, a testable seam (fake `orca` on PATH, the existing `clickup_claim.py` pattern), and a `--comment` marker lookup. It ties B on edge cases and beats C by 0.0965. All three advocates, including B's and C's, proposed A's script and A's repo resolution in their merged designs. The tiebreaker decided A over B by input order only.

### Strengths to Preserve from Base

1. Single script seam `scripts/orca_worktree.py` with exit 0 for runtime outcomes and 2 for bad arguments, one JSON line, 120 s timeout per call (A FR-5, FR-9, section 5).
2. `<main>` from `git --git-common-dir`, passed as `--repo path:<main>` (A section 4).
3. `--name issue-<N>` lookup order beginning with the `--comment "sc:issue <R>#<N>"` marker, then a path-basename fallback `^issue-<N>(-|$)` (A 2.5).
4. B16 design-doc decision, `version: "1.1.0"` in `commands/issue.md` only, no second command (A 2.7).
5. Return-contract fields printed only with the flag (A FR-11).

### Strengths to Incorporate from Non-Base Variants

1. From B (2.4, FR-7, section 8): no new ref file (a new ref breaks `test_all_five_refs_exist`); per-file copy that never nests; "left out on purpose" list.
2. From B (section 5 step 4, O7 of Round 2): path after create from a follow-up list, with set difference of row ids, not from the unverified create JSON; empty-list guard (a registered repo always lists its `isMainWorktree` row).
3. From B (6): ignore archived rows; "several live matches create nothing and list them".
4. From B (9): name the upstream project-id risk and the manual checks.
5. From C (6, 7): edge-case table mapped to tests; forbidden-flag regex; "unflagged output byte-identical" acceptance criterion; remedy line on failure; record file `worktree.json` (path only, guarded) kept out of the copy.
6. From the invariant probe: INV-001 (truncation), INV-002 (branch tail), INV-003 (0 or 2+ new ids), INV-004 (dedupe by id, first key decides), INV-005 (tracked files), INV-009 (own fetch), INV-010 (realpath), INV-011 (re-list after timeout), INV-016 (post-condition check).
7. From Round 2 (A, B, C agree): `W-WORKTREE-STALE` stop for a missing path, `<name>.prev` single backup, self-copy skip.
