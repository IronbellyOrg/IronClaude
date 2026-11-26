# Base Selection

Variants are anonymized (blind mode). Map to files: see `blind-map.txt`. Inputs to this step: `scoring/quantitative.md`, `scoring/qual-pass1.md`, `scoring/qual-pass2.md`, `scoring/reevaluation.md`, `debate/scoring-matrix.md`, `invariant-probe.md`.

## Quantitative Scoring (50% weight)

Method and raw counts: `scoring/quantitative.md` (counting rules stated there; source requirements are the seed brief's Constraints, Success Criteria and Open Questions items, because the source has no formal requirement IDs).

| Metric | Weight | Variant A | Variant B | Variant C |
|---|---|---|---|---|
| RC requirement coverage | 0.30 | see file | see file (loses the authorization constraint: keeps a `merge` operation, diff-analysis X-002) | see file |
| IC internal consistency | 0.25 | see file | see file | see file |
| SR specificity ratio | 0.15 | see file | see file | 18 of 52 items have no code span, number or quantity |
| DC dependency completeness | 0.15 | 1.0 | 1.0 | 1.0 |
| SC section coverage | 0.15 | see file | see file | see file |
| **quant_score** | | **0.9736** | **0.9666** | **0.9266** |

Sensitivity (from the scoring agent): the A-over-B order depends on one coverage rule (B's `merge` operation counted as breaking the authorization constraint). With plain topic matching B would score 0.9842 and rank first. Two extra internal contradictions found by the scoring agent (A: FR-052/T-15 vs FR-091; B: FR-020 vs FR-023) do not change the ranking A, B, C.

## Qualitative Scoring (50% weight): Additive Binary Rubric (30 criteria)

Two independent evaluations (pass 1 in order A, B, C: `scoring/qual-pass1.md`; pass 2 in order C, B, A: `scoring/qual-pass2.md`), each with Claim-Evidence-Verdict per criterion. Totals before reconciliation: pass 1 A 26, B 22, C 26; pass 2 A 26, B 26, C 27.

### Dimension subtotals after reconciliation (30 criteria: 6 dimensions of 5)

| Dimension | Variant A | Variant B | Variant C |
|---|---|---|---|
| Completeness | 5 | 4 | 5 |
| Correctness | 4 | 2 | 5 |
| Structure | 4 | 4 | 5 |
| Clarity | 4 | 3 | 3 |
| Risk Coverage | 4 | 4 | 4 |
| Invariant & Edge Case Coverage | 5 | 5 | 5 |
| **Total met / 30** | **26** | **22** | **27** |
| **qual_score** | **0.8667** | **0.7333** | **0.9000** |

Where each variant lost points (from the CEV evidence in the pass files):
- Variant A: FR-052 plus test T-15 forbid the string `--commit-tasks` outside three files, but FR-091 puts it in the worker contract (correctness); shared commit rules in section 6 come after sections that depend on them (structure); undefined terms Q0, Q7, WC-4, TAMPER (clarity); risks have no likelihood or impact rating (risk coverage).
- Variant B: keeps a `merge` operation that the seed constraint forbids (correctness.2); the Wave-0 check "after step 6" contradicts its own claim that the run stops before the ledger exists (correctness.4); "may gain" wording and undefined P4, WC-9 (clarity); wrong fixture claim about `--interactive`.
- Variant C: wording such as "when applicable" and "where observable"; key design values (trailer token, request format, stop code, timeouts, test file names) left open; undefined Q0 and Ruling; no risk ratings.

### Edge Case Floor Check

All three variants score 5/5 on Invariant & Edge Case Coverage; the floor (1/5) is met by every variant. No variant is ineligible.

## Position-Bias Mitigation

Dual-pass results: 90 criterion-variant pairs per pass; 85 agreed, 5 disagreed.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final (re-evaluation, `scoring/reevaluation.md`) |
|---|---|---|---|---|---|
| clarity.1 | B | NOT MET | MET | no | NOT MET ("may gain" in FR-009 leaves the required edit unclear) |
| clarity.4 | B | NOT MET | MET | no | NOT MET (P4, WC-9 undefined at first use; WC-4, W/WA/F, TAMPER never defined) |
| correctness.2 | B | NOT MET | MET | no | NOT MET (FR-013 runs `git merge <branch>` against the seed constraint) |
| correctness.4 | B | NOT MET | MET | no | NOT MET (FR-023 check after step 6 contradicts "before the ledger is created") |
| clarity.2 | C | NOT MET | MET | no | MET (specific actions: exact commands, field lists, closed outcome set) |

disagreements_found: 5. verdicts_changed: 5 (the re-evaluation sided with pass 1 four times and with pass 2 once; each re-evaluated pair got one final verdict).

## Combined Scoring

variant_score = 0.50 x quant_score + 0.50 x qual_score (computed by script, not by hand).

| Variant | quant | qual | Combined |
|---|---|---|---|
| A | 0.9736 | 0.8667 | **0.9201** |
| B | 0.9666 | 0.7333 | 0.8500 |
| C | 0.9266 | 0.9000 | 0.9133 |

Ranking by score: A, C, B. Margin between the top two: 0.0068 (0.74%), which is within the 5% tiebreaker band.

### Tiebreaker

- Applied: yes, level 1 (debate performance).
- Level 1: points won in Step 2 (final-round scoring matrix, `debate/scoring-matrix.md`): Variant A 14, Variant B 12, Variant C 3; HYBRID 29 and NONE 3 are not wins for any one variant. A beats C 14 to 3, which decides it; levels 2 and 3 were not needed.
- Evidence: A won 14 of the points that had a single-variant winner; C won 3. (For information only: C has the higher correctness criteria count, 5 against 4, which would have favored C at level 2, but level 1 already decided.)

## Selected Base: Variant A

### Selection rationale

Variant A has the highest combined score (0.9201) and wins the level-1 tiebreaker against Variant C by debate performance (14 points to 3). It also has the best quantitative score (0.9736) and the most complete treatment of structure, extension scaffolding and the Q-loop integration points the debate settled on (S-009, S-012, C-001, C-002, C-007, X-002, X-003, X-009, X-010, X-011, X-012 and others went to A). The margin over C is small, and C leads on the qualitative layer alone, so the merge must bring in C's strengths wherever the debate voted for them.

### Strengths to preserve from the base

- Operation registry and the "adding an operation" checklist; five refs plus a registry table (S-009, U-002).
- `/sc:git` operation set without `merge`, `--interactive` and push/pull; `--message` with `--smart-commit` (C-001, C-002, X-002, X-003).
- Baseline-facts table with line-level citations (U-001); safety constants defined once with a parity test (U-003).
- Test-obligation table with proposed file names (S-005 HYBRID) and acceptance-criteria table mapped to tests.
- The settle-before-advance rule and the `ledger-lines=` run-segment idea (Round 3, A's proposals).

### Strengths to incorporate from the non-base variants

Taken from the debate record (final-round winners and the Round 3 requirement text), to be itemized in `refactor-plan.md`:
- From Variant B: first-`complete` anchor and moved-on refusal (INV-001); pinned whole-worktree snapshot and per-attempt compare instead of `unstaged-outside` (INV-021); resolution-record amendments (full 64-hex key, reply after disclosure, `abandon` always offered) (INV-027); `pre_tree` comparison and hook-rewrite classes; `foreign-change` per path; guard-denies-`git submodule` finding (U-009); size budgets; root-cause section; fixes for INV-002, 003, 024, 025.
- From Variant C: journal-before-attempt and the frozen full-candidate predicate; stable boundary key (SHA-256, full 64 hex); literal path handling and symlink/traversal refusal; worktree-local helper lock note; worktrees `archive` writes without `--apply`; multi-repository partial-execution reporting; submodule update grant that acknowledges the network effect; honest-limits wording.
- From the Round 2.5 and Round 3 invariant work: all 16 ACCEPT-FIX requirements (INV-002, 003, 004, 007, 008, 009, 010, 012, 014, 015, 020, 022, 023, 024, 025, 030) and the three ACCEPT-RISK residuals (INV-011, 018, 029).
