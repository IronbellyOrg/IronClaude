# Base Selection Report

Variants: A = `option-a.md` (variant-1-original), B = `option-b.md` (variant-2-original), C = `option-c.md` (variant-3-original). Mode A, default model, no persona.

## Quantitative Scoring (50% weight)

Source requirements. Mode A has no `--source`, so the requirement set is the 14 items of `context.md` (8 facts, 6 criteria). Each is matched by a fixed keyword regex over the variant text; the batch grep run is the evidence. R01 call site/definition line; R02 `affected`; R03 `init`; R04 `explore`; R05 `return-contract`; R06 `partial` status; R07 implement caller; R08 `test_cli_install`; R09 `## Callers`; R10 token/cost/latency; R11 contract; R12 fail-open/no codegraph/degraded; R13 test files/command files/fixtures/maintenance/machinery; R14 `/sc:test`/explain/index-repo.

| Metric | Weight | Variant A | Variant B | Variant C |
|--------|--------|-----------|-----------|-----------|
| requirement_coverage | 0.30 | 0.714 (10/14; missing R01, R04, R06, R10) | 0.786 (11/14; missing R04, R06, R08) | 0.714 (10/14; missing R04, R08, R10, R14) |
| internal_consistency | 0.25 | 0.923 (1 of 13 claims: X-004, `--tests` vs `/sc:test-scope`) | 0.917 (1 of 12: X-001, skill needed vs "guide plus Read already enforces") | 0.909 (1 of 11: X-002, "no per-run invocation" vs probe via `/sc:graph status`) |
| specificity_ratio | 0.15 | 1.000 (0 vague indicators) | 1.000 (0 vague) | 1.000 (0 vague) |
| dependency_completeness | 0.15 | 1.000 (3/3: `--tests`, `/sc:graph status`, "callers above") | 0.600 (3/5: "test-scope" and "the shared guide doc" undefined in B) | 0.800 (4/5: "the guide's 'not initialized' message" undefined in C) |
| section_coverage | 0.15 | 1.000 (4 H2) | 1.000 (4 H2) | 1.000 (4 H2) |
| **quant_score** | | **0.895** | **0.855** | **0.862** |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Final verdicts after dual-pass reconciliation (Pass 1 order A, B, C; Pass 2 order C, B, A). Each MET cites the variant's own text.

### Completeness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|-----------|---|----------|---|----------|---|----------|
| 1 Covers all explicit requirements | NOT MET | No token cost, no overlap with `/sc:index-repo`/`/sc:test`/`/sc:explain` | NOT MET | No overlap analysis | NOT MET | No overlap, no token cost |
| 2 Edge cases/failures | NOT MET | Only the label "fail-open" (l.11) | MET (re-eval) | l.25 "brittle across releases" plus l.7 degraded vocabulary | MET | l.7 "With no codegraph or no index it returns `status: partial`" |
| 3 Dependencies/prerequisites | MET | l.11 core guide | MET | l.7 consumers run the skill as "Step 0" | MET | l.10, l.21 guide "already planned (spec §4)" |
| 4 Success criteria | NOT MET | none | NOT MET | none | NOT MET | none |
| 5 Out of scope | MET (re-eval) | l.11 "not in a skill" | MET (re-eval) | l.7 "no slash command" | MET | l.10 "No new skill for shared semantics" |
| **Subtotal** | **2/5** | | **3/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|-----------|---|----------|---|----------|---|----------|
| 1 No factual errors | MET | l.29 "affected was never run in EVAL" (true, EVAL §5) | NOT MET | l.25 "parses undocumented CLI text output" vs BRS FR-06 `query --json` (both passes) | MET | spec §4 claim holds (P3-D2) |
| 2 Feasible | MET | | MET | | MET | |
| 3 Terminology consistent | MET | | MET | | MET | |
| 4 No internal contradictions | MET | l.28 is a hedge | MET | | NOT MET | l.8 probe via `/sc:graph status` vs l.21 "No per-run skill invocation" |
| 5 Claims supported | MET | l.29 | MET | EVAL §5.5, OQ-6 | MET | spec §4 |
| **Subtotal** | **5/5** | | **4/5** | | **4/5** | |

### Structure (5 criteria)

All three: MET ×5 (Commands → Callers → Strengths → Weaknesses; flat H1/H2; seam kept separate; cross-references to context/EVAL/spec; decision-option convention). **Subtotals 5/5, 5/5, 5/5.**

### Clarity (5 criteria)

| Criterion | A | B | C |
|-----------|---|---|---|
| 1 Unambiguous | NOT MET: "(or three self-contained commands)" | NOT MET (re-eval): "as in option A plus" leaves B's caller list undefined inside B | NOT MET: "(or simply read the guide's one-call readiness check)" |
| 2 Concrete | MET | MET | MET |
| 3 Section purpose | MET | MET | MET |
| 4 Terms defined | NOT MET (K-2, Q1, VG-1) | NOT MET (K-1, OQ-6) | NOT MET (Q1, VG-1, UC-2) |
| 5 Next steps | NOT MET | NOT MET | NOT MET |
| **Subtotal** | **2/5** | **2/5** | **2/5** |

### Risk Coverage (5 criteria)

| Criterion | A | B | C |
|-----------|---|---|---|
| 1 ≥3 risks with probability/impact | NOT MET | NOT MET | NOT MET |
| 2 Mitigation per risk | NOT MET | NOT MET | NOT MET |
| 3 Failure modes/recovery | NOT MET | NOT MET | MET: Grep-based `partial`, "never stops the caller" |
| 4 External dependency failure | NOT MET | MET: CLI output drift (l.25) | MET: "no codegraph or no index" |
| 5 Monitoring/validation | MET: "each cited row re-Read" | MET: Read-verified lines, fixtures | MET: "confirmed by Grep … and Read" |
| **Subtotal** | **1/5** | **2/5** | **3/5** |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | A | B | C |
|-----------|---|---|---|
| 1 Collection boundaries | NOT MET (re-eval): `--depth 1-3` is a range, not a size cap; `--limit N` unbounded | NOT MET: `[--limit]` unbounded | MET: `--limit N, default 20` |
| 2 State across components | MET: callers probe `/sc:graph status` | MET: per-run probe | MET: index state drives `partial` |
| 3 Guard gaps | MET: init "only when the user typed `init`" | NOT MET (re-eval): "only `init` owner", no user-typed guard | MET: same guard as A |
| 4 Count divergence (shown/total) | NOT MET | NOT MET | NOT MET |
| 5 Interaction effects | MET: `--tests` duplicates test-scope | MET: `--tests` overloads impact | MET (re-eval): "two jobs: dependents and tests" (l.25) |
| **Subtotal** | **3/5** | **2/5** | **4/5** |

### Qualitative Summary

| Dimension | A | B | C |
|-----------|---|---|---|
| Completeness | 2 | 3 | 3 |
| Correctness | 5 | 4 | 4 |
| Structure | 5 | 5 | 5 |
| Clarity | 2 | 2 | 2 |
| Risk Coverage | 1 | 2 | 3 |
| Invariant & Edge Case | 3 | 2 | 4 |
| **qual_score** | **18/30 = 0.600** | **18/30 = 0.600** | **21/30 = 0.700** |

### Edge Case Floor Check

A 3/5 eligible; B 2/5 eligible; C 4/5 eligible. Floor not suspended.

## Position-Bias Mitigation

Pass totals as reported: Pass 1 A 17, B 18, C 21; Pass 2 C 20, A 18, B 17. Pass 2's own subtotals for A's and B's invariant dimension were mis-added: its row verdicts give A 4 and B 3, not 3 and 2. Reconciliation uses the row verdicts, not the subtotals.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness 5 | A | NOT MET | MET | DISAGREE | MET: "not in a skill" is the same kind of exclusion both passes accepted from C ("No new skill") |
| Invariant 1 | A | NOT MET | MET | DISAGREE | NOT MET: a depth range is not a bound on list size |
| Completeness 2 | B | MET | NOT MET | DISAGREE | MET: it names a concrete failure scenario (output drift) and a degraded mechanism, which is more than A's bare label |
| Completeness 5 | B | NOT MET | MET | DISAGREE | MET: "no slash command" is an explicit exclusion |
| Clarity 1 | B | MET | NOT MET | DISAGREE | NOT MET: "as in option A plus" defines B's callers only by reference to another document |
| Invariant 3 | B | NOT MET | MET | DISAGREE | NOT MET: "only `init` owner" lacks the user-typed guard that A and C state |
| Invariant 5 | C | MET | NOT MET | DISAGREE | MET: "two jobs" names the combination effect, of the same type both passes credited to A and B |

Disagreements re-evaluated: 7. Final verdicts followed Pass 1 in 4 cases and Pass 2 in 3. The orchestrator did the re-evaluation in-session, citing both passes' evidence; it was not a separate agent.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (option-a) | 0.448 | 0.300 | **0.748** | 2.5 points won |
| B (option-b) | 0.427 | 0.300 | **0.727** | 7.5 points won |
| C (option-c) | 0.431 | 0.350 | **0.781** | 8.0 points won |

**Margin**: C over A = 0.033 (3.3%), below the 5% threshold.
**Tiebreaker applied**: Yes, level 1 (debate performance). C won 8.0 diff points to A's 2.5, a gap well outside 5%, so C wins. Levels 2-3 were not needed.

## Selected Base: Variant C (`option-c.md`)

### Selection Rationale

C has the highest combined score (0.781). It also wins the level-1 tiebreaker clearly, and the debate agreed unanimously that its unit count (S-002), interface specification (S-004) and fail-open result (C-005) are superior. On the seam it wins 2 of 3 votes, with the third a tie (C-001, X-001). Its two-command shape matches the spec decision P3-D2 (`specs/phase-3-codegraph-adoption-spec.md` §4: one core guide, "would tie generic guidance to one command" rejects a skill seam) and CTX rule 7 (smallest correct change). All three advocates' recommended sets include C's two commands.

### Strengths to Preserve from Base
1. Two units: `/sc:impact` and `/sc:graph`, with shared rules in `~/.claude/CODEGRAPH.md` (S-002, C-001, X-001).
2. Concrete defaults: `--depth 1-3`, default 2; `--limit N`, default 20; several symbols per call (S-004, C-004).
3. Explicit fail-open result: `status: partial` with Grep or files-only results; never stops the caller (C-005).
4. One home for test selection through `--tests` (X-004).
5. `init` only when the user typed it.

### Strengths to Incorporate from Non-Base Variants
1. From B: the closed `graph:*` degraded vocabulary (X-003, BRS FR-02), replacing `degraded: [codegraph]`.
2. From B: provenance and version in readiness (`pin_match`, `worktree_relation`, telemetry; C-006, U-004, BRS FR-03/NFR-09/FR-22), and the `foreign_index` handling behind A-001.
3. From A: the advisory label and a per-test `source` on the `--tests` list (C-002, U-007, BRS FR-13 stage 0, SPEC §2.2 rank 13).
4. From A: a separate depth flag for test mapping (C-009, EVAL §3: `impact --depth` and `affected --depth` are separate verbs).
5. From A, partly: an explicit overlap statement against `/sc:test` (A names `/sc:test` as a caller, U-001). This fills the criterion-6 gap that every variant left open.
6. From B, partly: the budgeted FR-06 resolution rule (5 per symbol, 20 per run; `resolution` field), as a written procedure, not a script (C-003; SPEC §2.2 rank 5 "Guide rule 1 plus the confirmation procedure").
7. From the debate (unanimous on shared assumptions): `index_state` and `checked_at` on every result, advisory until E-1 (A-003); the FR-09 partition (A-006); the `--diff` hunk-mapping rule with `unmapped_files[]` (A-002); `--worktree-local` refusal (A-001); shown/total truncation (FR-08, a gap flagged by both scoring passes).
