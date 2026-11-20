# Base Selection Report

Variants: V1 = reviewer card 1 (opus advocate, analyzer lens; card by sonnet class), V2 = reviewer card 2 (qa lens; card by haiku class), V3 = reviewer card 3 (refactorer lens; card by opus class). Source input for coverage: the spec `source.md` of `TASK-WF-stage3CRequest-20261119-143901`. Full per-criterion CEV evidence: `scoring/qual-pass-1.md` (input order) and `scoring/qual-pass-2.md` (reverse order), written by two independent evaluator agents.

## Quantitative Scoring (50% weight)

Computed by the orchestrator from the card text with fixed rules (re-running gives the same numbers):
- RC: the spec has no requirement IDs, so section-level topic matching was used: 13 spec topics, each with a fixed case-insensitive regex (branch `origin/master|fresh branch`; owner go; entry condition `PR #605|FINAL: pass|entry condition`; edit anchor `anchor|line 122|:122`; byte copy `sha256|byte`; `needle`; do-not-change list `frontmatter|Boundaries|S1`; `git grep`; Task 1 acceptance `grep -c|greps|acceptance`; Task 2 `sync-dev|verify-sync|Task 2`; exclusions `not to be done|not-to-be-done|exclusion`; `known limits|limits`; constraints `uv run|\.claude/|\.dev/tasks`).
- IC: intra-card contradictions / scorable claims (table rows + summary lines + Notes bullets).
- SR: concrete tokens (file:line citations) / (concrete + vague tokens from the protocol's vague list). No card contains a vague token.
- DC: resolved internal references / internal references (references to other documents excluded).
- SC: H2 count / max H2 count.

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|--------|--------|-----------|-----------|-----------|
| requirement_coverage | 0.30 | 0.923 (12/13; misses the do-not-change list) | 0.615 (8/13; misses anchor, byte copy, do-not-change list, git grep, Task 2 sync) | 1.000 (13/13) |
| internal_consistency | 0.25 | 0.941 (1 of 17: "Spec units audited: 22" while its own list sums to 4+6+3+5+3+1+1 = 23, variant-1:29) | 1.000 (0 of 14; 43+2 = 45 and 40+5 = 45 reconcile) | 1.000 (0 of 19; 2+1+6+5+5+4+3+4 = 30 and 25+5 = 30 reconcile) |
| specificity_ratio | 0.15 | 1.000 (20 concrete / 0 vague) | 1.000 (9 / 0) | 1.000 (49 / 0) |
| dependency_completeness | 0.15 | 0.500 (1 of 2: "the paragraph above" at variant-1:25 points at no paragraph above it; "both blocking rows" resolves) | 1.000 (4 of 4) | 1.000 (5 of 5) |
| section_coverage | 0.15 | 1.000 (3/3) | 1.000 (3/3) | 1.000 (3/3) |
| **quant_score** | | **0.887** | **0.885** | **1.000** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts after position-bias reconciliation (M = MET, N = NOT MET). Short evidence is given for each criterion; the full CEV text with quotes is in the two pass files.

### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 | Evidence (from both passes) |
|-----------|----|----|----|-----------------------------|
| Covers all explicit requirements | N | M | M | V1 lists 22 units but no do-not-change/frontmatter unit and miscounts; V2 45 INF units; V3 30 units incl. do-not-change list (variant-3:24) |
| Edge cases / failure scenarios | M | M | M | V1 "a middle error such as a wrong grade token still passes"; V2 "can satisfy every acceptance check without satisfying this execution condition"; V3 "A copy with a wrong token in the middle ... passes all three greps" |
| Dependencies / prerequisites | M | M | M | All check the entry condition or dependents (V1 test at :214; V2 copy route at plan:20; V3 entry condition, progress.md:7) |
| Success / completion criteria | M | M | N | V1 "Fixes for both blocking rows are added text in the plan"; V2 "Next: resolve findings 1 and 2 before execution"; V3 states which rows block but no done criterion |
| Out of scope | M | M | M | All record the "not to be done" exclusions as checked |
| **Subtotal** | **4/5** | **5/5** | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 | Evidence |
|-----------|----|----|----|----------|
| No factual errors | N | N | N | V1: 22 vs 23 units and "5 not to be done items" vs 4 bullets; V2: "not an additional plan deviation" (conceded wrong, r2-v2); V3: "drops the spec's way of checking byte identity" overstates a provenance sentence (conceded, r2-v3.md:20) |
| Feasible approaches | M | M | M | All recommend small plan-text fixes |
| Terminology consistent and accurate | N | M | M | V1 categorises row 4 "Drift" while saying the wording comes from the spec; V2 keeps category, grade and label distinct as agent:122 allows; V3 consistent |
| No internal contradictions | N | M | M | V1 unit count; V2 and V3 reconcile |
| Claims supported | M | M | M | file:line evidence in every row of all three |
| **Subtotal** | **2/5** | **4/5** | **4/5** | |

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 | Evidence |
|-----------|----|----|----|----------|
| Logical ordering | N | M | M | V1 inserts a stray Note paragraph between table and summary (variant-1:25) |
| Consistent hierarchy | M | M | M | All use the template's three H2 sections |
| Separation of concerns | M | M | M | Deviations / summary / notes kept apart |
| Navigation aids | M | M | M | Row numbers and cross-references to findings |
| Artifact-type conventions | N | M | M | V1 grades a spec-inherited item Medium and leaves a graded Note outside the table; V2 and V3 follow the card template and grade-prefix rule |
| **Subtotal** | **3/5** | **5/5** | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 | Evidence |
|-----------|----|----|----|----------|
| Unambiguous language | N | M | M | V1 "Not found, so no row: the paragraph above is a note on form only" is garbled |
| Concrete | M | M | M | Named files, lines, commands in all |
| Clear section purpose | M | M | M | |
| Terms defined on first use | N | N | N | None defines INF, UC-1, RT1-style terms or "consumer" |
| Actionable next steps | M | M | M | V1 fix line; V2 "Next"; V3 grade summary line |
| **Subtotal** | **3/5** | **4/5** | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | Evidence |
|-----------|----|----|----|----------|
| ≥3 risks with probability and impact | N | N | N | No card rates probability |
| Mitigation per risk | N | N | N | Fixes given only for the Blocking rows |
| Failure modes / recovery | M | M | N | V1 and V2 describe how execution goes wrong and how to fix; V3 does not give a recovery for row 3 |
| External dependencies and their failure | M | N | M | V1 stale codegraph; V3 origin/master line 122 may differ; V2 names the live grounding root but no failure scenario (re-evaluated) |
| Monitoring / validation mechanism | M | M | M | V1 Grep counts; V2 validates the matrix's INF-036 containment match against semantics (re-evaluated); V3 checked-with-no-finding list |
| **Subtotal** | **3/5** | **2/5** | **2/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | Evidence |
|-----------|----|----|----|----------|
| Collection boundaries | M | N | M | V1 and V3: grep-matched YAML fixtures in the test set; V2 none |
| State interactions across components | M | M | M | Branch state vs acceptance checks (all) |
| Guard condition gaps | M | M | M | Acceptance checks that pass while the behaviour is absent (all) |
| Count divergence | N | N | M | V3: git grep names two test files beyond the four; "3 rows covering 5 units"; V2's own 45/40 count was padded (re-evaluated) |
| Interaction effects | M | N | M | V1 needle-tuple vs pytest; V3 sync-dev vs src/plugins check |
| **Subtotal** | **4/5** | **2/5** | **5/5** | |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 | Variant 3 |
|-----------|-----------|-----------|-----------|
| Completeness | 4/5 | 5/5 | 4/5 |
| Correctness | 2/5 | 4/5 | 4/5 |
| Structure | 3/5 | 5/5 | 5/5 |
| Clarity | 3/5 | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 2/5 | 2/5 |
| Invariant & Edge Case | 4/5 | 2/5 | 5/5 |
| **qual_score** | **19/30 = 0.633** | **22/30 = 0.733** | **24/30 = 0.800** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case | Eligible as base (≥1/5) |
|---------|-----------------------|-------------------------|
| V1 | 4/5 | Yes |
| V2 | 2/5 | Yes |
| V3 | 5/5 | Yes |

## Position-Bias Mitigation

Pass 1 (input order V1, V2, V3) totals: V1 20, V2 21, V3 24. Pass 2 (reverse order V3, V2, V1) totals: V1 19, V2 22, V3 25. 83 of 90 criterion-variant pairs agreed.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final (orchestrator re-evaluation with both passes' evidence) |
|-----------|---------|--------|--------|-----------|-------|
| Corr.3 terminology | V1 | MET | NOT MET | DISAGREE | NOT MET: row 4 is categorised Drift while its own cell says the wording comes from the spec |
| Corr.3 terminology | V2 | MET | NOT MET | DISAGREE | MET: Pass 2's objection is the MEDIUM label on Blocking rows, but agent:122 makes the label information and allows it to differ from the grade |
| Str.5 conventions | V2 | MET | NOT MET | DISAGREE | MET: the Notes-placed items (coverage-matrix inventory, the rejected byte-identity point) are not plan deviations, so they do not belong in the Deviations table; labels as above |
| Risk.4 external deps | V2 | NOT MET | MET | DISAGREE | NOT MET: the live grounding root is named, but no failure scenario is given, and CEV needs evidence for MET |
| Risk.5 validation | V2 | NOT MET | MET | DISAGREE | MET: checking the matrix's INF-036 containment match against meaning is a validation mechanism (variant-2:32) |
| Inv.4 count divergence | V2 | NOT MET | MET | DISAGREE | NOT MET: V2 finds no count divergence in the audited plan; reconciling its own padded count is not that |
| Corr.1 factual errors | V3 | NOT MET | MET | DISAGREE | NOT MET: row 3's "drops the spec's way of checking byte identity" overstates source.md:24, a provenance sentence (conceded at r2-v3.md:20) |

Disagreements re-evaluated: 7
Final verdicts changed from Pass 1: 2 (V1 Corr.3, V2 Risk.5); from Pass 2: 5

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (card 1, analyzer) | 0.444 | 0.317 | **0.760** | 4 points won (not needed) |
| V2 (card 2, qa) | 0.442 | 0.367 | **0.809** | 3 points won (not needed) |
| V3 (card 3, refactorer) | 0.500 | 0.400 | **0.900** | 12 points won (not needed) |

**Margin**: 9.1% between V3 and V2 (above the 5% threshold)
**Tiebreaker applied**: No

The debate gave the same answer: V3 won 12 of 15 diff points (shared wins counted), and its four graded rows survived both rounds with only wording corrections.

## Selected Base: Variant 3 (card 3, refactorer lens)

### Selection Rationale
V3 has the highest combined score (0.900) by a 9.1% margin. It is the only card that covers all 13 spec topics, has no internal count error and no broken internal reference, and scores 5/5 on invariant and edge-case coverage. Every grade on its four rows matches the debate's final consensus: branch Blocking (Missing), known limits Blocking (Missing), byte identity Medium, Authorized expansion Note. It also carries the Notes the consensus kept, the backtick rendering and the test-discovery wording. Its weaknesses are wording, and all are fixable in the merge: row 3 overstates the spec, the 83-test Note is too short, it has no verdict line, and it leaves U-005 open, which Round 2 closed.

### Strengths to Preserve from Base
1. Row 1 (branch) and row 2 (known limits), both `Blocking (Missing)`, each with its affected action named (variant-3:17-18).
2. Row 2's explicit statement that plan:21 contradicts the judgment limit (variant-3:18), which supports the Decision limb.
3. Row 4, Authorized expansion `Note:` (plan:61, :37, :60), and the Makefile evidence that `make sync-dev` writes only under `.claude/` (variant-3:20).
4. The "Checked with no finding" list: edit location, test target, whole-tree scans, edit tables, exclusions, entry condition (variant-3:30-36).
5. Notes (a) backtick rendering and (b) test-discovery wording with the six extra files named (variant-3:38).

### Strengths to Incorporate from Non-Base Variants
1. From V2: the explicit verdict line and a "Next" line (variant-2:12, :35), per S-001.
2. From V1: grounding header with the full spec and plan paths given once, then short cites (variant-1:13-14), per S-002.
3. From V2: the Adherence summary counted by coverage-matrix INF ids, corrected to 43 units, 37 fully adherent, with INF-001, INF-008, INF-034, INF-036, INF-037 and INF-038 named as not carried (S-003; matrix:14, :39, :87, :91).
4. From V2: limit 3's exact qualification "digits and apostrophes rather than lowercase letters" and the note that the INF-036 containment match is not semantic coverage (variant-2:19, :32).
5. From V1: "one of them" for the plan:21 overstatement (variant-1:21), confirmed by INV-014 (the other spec B finding was ruled a Blocker, README.md:28).
6. From V1: U-001, the needle-presence gap, folded into row 3's impact (variant-1:22).
7. From V2: the coverage-matrix inventory Note (variant-2:31), kept as a non-gating Note.
8. From the debate and probe: the C-006 rewording, the U-005 closure, PR #605 verified merged (`e3e9d636a`), 5 ahead / 49 behind origin/master, and the probe corrections INV-002, INV-003, INV-005, INV-010, INV-011 and INV-013 to the fix text and placement.
