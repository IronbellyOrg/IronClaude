# Base Selection Report

- Step: 3 (hybrid scoring and base selection) of the /sc:adversarial git-ownership debate, completed after the 2026-11-02 interruption.
- Inputs: `variant-1-original.md` .. `variant-5-original.md` (`V<n>:L`), `scoring-pass-1.md`, `scoring-pass-2.md`, `scoring-reconcile.md`, `debate-transcript.md` (scoring matrix at lines 1286-1317).
- Method note: the qualitative layer is NOT rescored. Verdicts are pass 1 where both passes agreed, and the reconciler's final ruling for each of the 15 disputed pairs (`scoring-reconcile.md:21-37`). The quantitative layer had not been computed before the interruption; it is computed here by a deterministic script (described below), because the protocol defines it as text metrics with no judgement (`refs/scoring-protocol.md:9`).

## Quantitative Scoring (50% weight)

Computed by `/tmp/git-ownership-quant/quant.py` (read-only; run twice with identical output, md5 `a9f966672215db00295e8d9acefb1122`). The fixed rules, decided before the run:
- **Statements:** sentences of every non-blank line that is not a heading, a table separator, or the "Position paper for" / "Citation keys" boilerplate.
- **RC:** 8 requirement items: R1-R7 from `scoring-pass-1.md:9`, with R3 split into "worker crash" and "git-owner crash", the same test the reconciler used (`scoring-reconcile.md:10`). Each item is matched by a fixed regex over the whole variant.
- **IC:** 1 - (intra-variant contradictions / statements). The only intra-variant contradiction found in Step 1 is X-005 in V4 (`diff-analysis.md:48`).
- **SR:** a statement is concrete if it holds a digit, a backtick span or a named entity (Orca, GitHub, git, HEAD, PR, Task, worktree, pr-submit, SPEC, K3, WC-n, D3, D4 and similar); vague if it holds a vague phrase from `refs/scoring-protocol.md:68-70` and is not concrete. No variant has a vague statement.
- **DC:** in-document references ("Self-check below", "above", "this file's table", "weakness N"); resolved when the target exists in the same file. Cross-file references (`option-a.md`, `SPEC:N`) are excluded (`refs/scoring-protocol.md:87`). A variant with no in-document reference scores 1.0 (no unresolved reference).
- **SC:** H2 count / 12 (V3 has the most H2 headings).

| Metric | Weight | V1 (A) | V2 (B) | V3 (C) | V4 (D) | V5 (E) |
|---|---|---|---|---|---|---|
| requirement_coverage | 0.30 | 1.000 (8/8) | 1.000 (8/8; the worker is the git owner, V2:25) | 1.000 (8/8) | 0.875 (7/8; no worker-crash case, V4:26) | 1.000 (8/8) |
| internal_consistency | 0.25 | 1.000 (0/53) | 1.000 (0/44) | 1.000 (0/52) | 0.969 (1/32, X-005) | 1.000 (0/39) |
| specificity_ratio | 0.15 | 1.000 (46 concrete, 0 vague) | 1.000 (39, 0) | 1.000 (50, 0) | 1.000 (28, 0) | 1.000 (32, 0) |
| dependency_completeness | 0.15 | 1.000 (2/2: "Self-check below" V1:5 to V1:45; "above" V1:46 to V1:11) | 1.000 (no refs) | 1.000 (no refs) | 1.000 (no refs) | 1.000 (1/1: "this file's table" V5:41 to V5:8-14) |
| section_coverage | 0.15 | 0.833 (10/12) | 0.750 (9/12) | 1.000 (12/12) | 0.833 (10/12) | 0.750 (9/12) |
| **quant_score** | | **0.975** | **0.963** | **1.000** | **0.930** | **0.963** |

Limits of this layer: SR and DC do not separate the variants (all at 1.0), so the quantitative layer turns mostly on section count and on V4's one gap and one contradiction. It is reported as computed, not adjusted.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdict per criterion and variant. Evidence column: `P1:N` = the CEV row at line N of `scoring-pass-1.md` (both passes agreed); `R#n` = ruling n of `scoring-reconcile.md` (passes disagreed; the reconciler's verdict is final, `SKILL.md:1771-1772`). The full Claim-Evidence-Verdict text is in those rows and is not copied here.

### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | MET | MET | NOT MET | MET | P1:15-17,19; R#1 (V4 has no worker-crash case, V4:26) |
| Addresses edge cases/failures | MET | MET | MET | MET | MET | P1:20-24 |
| Includes dependencies/prerequisites | MET | MET | MET | MET | MET | P1:25-29 |
| Defines success/completion criteria | NOT MET | NOT MET | NOT MET | NOT MET | NOT MET | P1:30; R#2-R#5 (a SHA in a contract is a record, not a done condition) |
| Specifies out-of-scope items | MET | MET | MET | MET | MET | P1:35,37-39; R#6 |
| **Subtotal** | **4/5** | **4/5** | **4/5** | **3/5** | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence |
|---|---|---|---|---|---|---|
| No factual errors | NOT MET | MET | NOT MET | NOT MET | NOT MET | P1:47,48,50,51; R#7 (V3:34 repeats V1's false "no git state" claim) |
| Approach feasible under stated constraints | MET | NOT MET | NOT MET | MET | MET | P1:52-56 |
| Terminology consistent | MET | MET | MET | MET | MET | P1:57-61 |
| No internal contradictions | MET | MET | MET | NOT MET | MET | P1:62-66 (V4: X-005) |
| Claims supported | MET | MET | MET | MET | MET | P1:67-71 |
| **Subtotal** | **4/5** | **4/5** | **3/5** | **3/5** | **4/5** | |

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence |
|---|---|---|---|---|---|---|
| Logical ordering | MET | MET | MET | MET | MET | P1:79-83 |
| Consistent hierarchy | MET | MET | MET | MET | MET | P1:84-88 |
| Separation of concerns | MET | MET | MET | NOT MET | MET | P1:89-93 |
| Navigation aids | MET | MET | MET | MET | MET | P1:94-98 |
| Artifact-type conventions (required topics as sections) | MET | MET | MET | NOT MET | MET | P1:99-103 |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **3/5** | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | MET | MET | MET | MET | MET | P1:111,113-115; R#8 |
| Concrete | MET | MET | MET | MET | MET | P1:116-120 |
| Each section has a clear purpose | MET | MET | MET | MET | MET | P1:121-125 |
| Terms defined on first use | NOT MET | NOT MET | NOT MET | NOT MET | NOT MET | P1:126-130 |
| Actionable next steps | MET | MET | MET | MET | MET | P1:131-135 |
| **Subtotal** | **4/5** | **4/5** | **4/5** | **4/5** | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence |
|---|---|---|---|---|---|---|
| At least 3 risks with probability and impact | NOT MET | NOT MET | NOT MET | NOT MET | NOT MET | P1:143-147 |
| Mitigation for each risk | NOT MET | NOT MET | NOT MET | NOT MET | NOT MET | P1:148-152 |
| Failure modes and recovery | MET | MET | MET | MET | MET | P1:153-157 |
| External dependencies and failure scenarios | MET | MET | MET | MET | MET | P1:160-161; R#9-R#11 |
| Monitoring or validation mechanism | MET | NOT MET | MET | MET | MET | P1:163-167 |
| **Subtotal** | **3/5** | **2/5** | **3/5** | **3/5** | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence |
|---|---|---|---|---|---|---|
| Collection boundaries (empty plus single or maximum) | MET | NOT MET | NOT MET | NOT MET | MET | P1:175,179; R#12-R#14 |
| State interactions across components | MET | MET | MET | MET | MET | P1:180-184 |
| Guard condition gaps | MET | MET | MET | MET | MET | P1:186-189; R#15 |
| Count divergence | MET | MET | MET | NOT MET | MET | P1:190-194 |
| Interaction effects | MET | MET | MET | MET | MET | P1:195-199 |
| **Subtotal** | **5/5** | **4/5** | **4/5** | **3/5** | **5/5** | |

### Qualitative Summary

| Dimension | V1 (A) | V2 (B) | V3 (C) | V4 (D) | V5 (E) |
|---|---|---|---|---|---|
| Completeness | 4/5 | 4/5 | 4/5 | 3/5 | 4/5 |
| Correctness | 4/5 | 4/5 | 3/5 | 3/5 | 4/5 |
| Structure | 5/5 | 5/5 | 5/5 | 3/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 2/5 | 3/5 | 3/5 | 3/5 |
| Invariant & Edge Case | 5/5 | 4/5 | 4/5 | 3/5 | 5/5 |
| **qual_score** | **25/30 = 0.833** | **23/30 = 0.767** | **23/30 = 0.767** | **19/30 = 0.633** | **25/30 = 0.833** |

These totals equal the reconciler's final totals (`scoring-reconcile.md:55-61`), which confirms the per-criterion table above.

### Edge Case Floor Check

| Variant | Invariant & Edge Case | Eligible as base (floor 1/5) |
|---|---|---|
| V1 (A) | 5/5 | Yes |
| V2 (B) | 4/5 | Yes |
| V3 (C) | 4/5 | Yes |
| V4 (D) | 3/5 | Yes |
| V5 (E) | 5/5 | Yes |

## Position-Bias Mitigation

Pass 1 (input order 1-5, `scoring-pass-1.md`) and pass 2 (reverse order 5-1, `scoring-pass-2.md`) disagreed on 15 of 150 criterion-variant pairs. Each was re-evaluated once by an independent reconciler with both passes' evidence (`scoring-reconcile.md`); that verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Completeness 1 | V4 | MET | NOT MET | DISAGREE | NOT MET (R#1) |
| Completeness 4 | V2 | MET | NOT MET | DISAGREE | NOT MET (R#2) |
| Completeness 4 | V3 | MET | NOT MET | DISAGREE | NOT MET (R#3) |
| Completeness 4 | V4 | MET | NOT MET | DISAGREE | NOT MET (R#4) |
| Completeness 4 | V5 | MET | NOT MET | DISAGREE | NOT MET (R#5) |
| Completeness 5 | V2 | MET | NOT MET | DISAGREE | MET (R#6) |
| Correctness 1 | V3 | MET | NOT MET | DISAGREE | NOT MET (R#7) |
| Clarity 1 | V2 | NOT MET | MET | DISAGREE | MET (R#8) |
| Risk 4 | V1 | NOT MET | MET | DISAGREE | MET (R#9) |
| Risk 4 | V2 | NOT MET | MET | DISAGREE | MET (R#10) |
| Risk 4 | V5 | NOT MET | MET | DISAGREE | MET (R#11) |
| Invariant 1 | V2 | MET | NOT MET | DISAGREE | NOT MET (R#12) |
| Invariant 1 | V3 | MET | NOT MET | DISAGREE | NOT MET (R#13) |
| Invariant 1 | V4 | MET | NOT MET | DISAGREE | NOT MET (R#14) |
| Invariant 3 | V1 | NOT MET | MET | DISAGREE | MET (R#15) |

Disagreements re-evaluated: 15. The final verdict sided with pass 2 in 14 and with pass 1 in 1 (R#6). No agreed verdict was changed (`scoring-reconcile.md:49`).

## Combined Scoring

`variant_score = 0.50 × quant + 0.50 × qual` (`refs/scoring-protocol.md:188`).

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate points won (Step 2) |
|---|---|---|---|---|
| V1 (A) coordinator main chat | 0.4875 | 0.4167 | **0.904** | 4 alone + 2 shared |
| V5 (E) hybrid | 0.4813 | 0.4167 | **0.898** | 15 alone + 2 shared |
| V3 (C) dedicated git session | 0.5000 | 0.3833 | **0.883** | 4 alone |
| V2 (B) workers own git | 0.4813 | 0.3833 | **0.865** | 0 |
| V4 (D) coordinator subagent | 0.4648 | 0.3167 | **0.782** | 1 alone + 1 shared |

Debate points from `debate-transcript.md:1317`; one point (C-006) was split and is credited to no variant.

**Margin**: V1 over V5 is 0.006 (0.7% of V1's score), below the 5% threshold (`refs/scoring-protocol.md:197`). V3 is also within 5% of V1 (0.021), so the tiebreaker is applied to all three for transparency, although the protocol only requires the top two.
**Tiebreaker applied**: Yes, level 1 (debate performance, `refs/scoring-protocol.md:199`). V5 won 15 diff points alone against V1's 4 and V3's 4; the gap is far outside 5%, so level 2 is not reached.

## Selected Base: Variant 5 (option E, hybrid)

### Selection Rationale
V5 ties V1 on the qualitative layer (25/30), trails it by 0.006 on the combined score, and wins the level-1 tiebreaker decisively: in Round 2 all five advocates chose V5's per-action owner and condition table as the merge form (S-001, 95%) and V5 won 15 of 25 diff points alone (`debate-transcript.md:1291-1317`). The debate converged on E plus additions (`debate-transcript.md:1185`, "No addition conflicts with E's core split"). V1's lead comes only from section count (10 against 9 H2 headings); its decisive weakness, no per-task or worker-side commits at all (V1:14), lost every L3 state-mechanics point it contested.

The debate did not fully converge: it ended `BLOCKED_BY_INVARIANTS` with five HIGH UNADDRESSED invariants (INV-006, INV-024, INV-025, INV-026, INV-032) and one split point (C-006) (`debate-transcript.md:1319-1327`). Under the no-convergence rule the base is force-selected by score (done here) and the five HIGH items become mandatory changes in `refactor-plan.md`.

### Strengths to Preserve from Base
1. The per-action table: action, owner, condition (V5:8-14, S-001, U-002).
2. Every outward action (push, PR through `/sc:pr-submit --monitor 3`, review replies, issue and status comments) owned by the coordinator in its main chat, only when the user's instruction names it (V5:10, V5:23; C-003, X-003).
3. The worker local-commit lane, bounded by a quoted grant, sole-writer placement and the between-tasks window for `/sc:implement` (V5:13; C-002, X-001).
4. The coordinator's shared-worktree commit only at a quiescent point, explicit paths plus `.dev/tasks` (V5:12; C-001).
5. The branch-removal guard: never remove a branch with unmerged commits or an open PR without the user's instruction (V5:11; C-011, `EVAL:53`).
6. The honest dependency on #326 K3 for in-run implement commits (V5:41).

### Strengths to Incorporate from Non-Base Variants
1. From V1 (A), Round 2 conditions 1-4 (`round2-advocate-a.md:30-33`): the lane is off by default and scoped; sole writer is a recorded placement fact; dormant for implement until K3; the worker invariant restated precisely.
2. From V2 (B), Round 2 rule P1 and B8: own worktree for granted committers, for implement ladders that share with outside writers, and the "found `index.lock` gives `blocked`" recovery rule (`round2-advocate-e.md:23,41-42`).
3. From V3 (C), M1-M3: each pr-submit run in its own PR-head checkout with no other writer; HALT ends `blocked`, resume is a new Task with `--resume`; optional same-terminal reuse (`round2-advocate-e.md:43-45`); and the per-action Orca record (S-002, C-005, X-002).
4. From V4 (D), the optional two-layer git guard, as amended (`round2-advocate-d.md:44-80`; `round2-advocate-e.md:46-47`).
5. From V1 (A), the GITDEMO evidence (U-004) and the quiescence rule (U-008), already present in V5 in shorter form.
6. From Advocate E's own Round 2 (`round2-advocate-e.md:49-57,61-87`): the four conflict fixes (D's block-list against implement's snapshot; A's condition 4 against the per-PR opt-in; A's condition 2 against resume Tasks; `git commit --only -- <paths>` on every commit).
7. From the invariant probe, the smallest rule change for each HIGH finding (`invariant-probe.md:52-58`).
