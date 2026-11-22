# Base Selection Report

Variants: Variant 1 = OURS (`variant-1-original.md`), Variant 2 = CLAY (`variant-2-original.md`). Debate result used as input: `debate-transcript.md` (CONVERGED, 15 of 16 points).

## Quantitative Scoring (50% weight)

Source requirements (no formal requirement IDs exist, so section-level topic matching is used): the brief's six paper elements (claim, mechanism, cited facts, costs, risks, gets right) plus the three answered questions (OD-1, OD-2, OD-13) = 9 items. Specificity counts come from a read-only shell count over each file: file:line or `D:nnn` references + digit tokens outside references + backticked names = concrete; vague words (may, might, implies, "if a gate is wanted", etc.) = vague. These are crude proxies and are stated as such.

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 1.000 (9 of 9) | 1.000 (9 of 9) |
| internal_consistency | 0.25 | 1.000 (0 intra-variant contradictions found in about 20 claims) | 1.000 (0 intra-variant contradictions found; one tension, "place never freed" is both a cost and a strength, is stated openly by V2) |
| specificity_ratio | 0.15 | 0.991 (concrete 108: 11 refs + 53 numbers + 44 names; vague 1) | 0.975 (concrete 117: 26 refs + 44 numbers + 47 names; vague 3) |
| dependency_completeness | 0.15 | 1.000 (vacuous: no internal cross-references to resolve; external references excluded) | 1.000 (vacuous, same) |
| section_coverage | 0.15 | 1.000 (6 H2 of max 6) | 1.000 (6 H2 of max 6) |
| **quant_score** | | **0.9987** | **0.9963** |

Note: the quantitative layer barely separates the two variants (difference 0.0024); the separation comes from the qualitative layer.

## Qualitative Scoring (50% weight): Additive Binary Rubric

Method: two independent evaluator agents ran the 30-criterion rubric, Pass 1 in order (V1, V2) and Pass 2 in reverse order (V2, V1). Where they agreed the verdict stands. Where they disagreed (6 cases) the orchestrator re-evaluated with both pieces of evidence (see Position-Bias Mitigation). Two cited facts were spot-checked by the orchestrator: `predicates.py` in snapshot `pr-a` has 219 lines (the approval-voiding code at lines 249-259 exists only in master, 312 lines); and design D:616 reads "the place is never freed between rounds".

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Covers all explicit requirements | MET | Claim 1-3 answer OD-1, OD-2, OD-13; six sections; 9 facts | MET | Same; 9 facts with D:nnn lines |
| Edge cases and failure scenarios | MET | Risks: weak plan passes `plan_check`, unbounded waiting pile, poll never wakes an acknowledged entry (`cycle.py:993-994`) | MET | Risks: autonomous 4-round loop, `--remaining` fidelity (U60), counted place blocks repo |
| Dependencies and prerequisites | MET | Needs C-INV-2 wake path; depends on D14 and WC-17 (UNVERIFIED fit) | MET | Fact 6: old worker final first; PR P table not on master |
| Success/completion criteria | MET (resolved) | Fact 7 gives a testable condition (three waiting hand-backs must not give `coordinator_full`); rounds capped at 4 | MET (resolved) | Fact 8: loop ends on `cap`, `no_progress`, `no_remaining` |
| Out-of-scope items | MET (resolved) | "does not invent a second mechanism (no `handback_awaiting_go`, no `answer-check` per round)"; "no separate chat go per round" | NOT MET | Searched Claim, Mechanism, Costs, Risks, Gets right: no exclusion stated |
| **Subtotal** | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| No factual errors | NOT MET | Fact 4 cites `pr-a/.../predicates.py:249-259` but that file has 219 lines (content exists in master); fact 2 (D12 item 6) is a create-time tier floor, only loosely related to OD-1 | NOT MET (resolved) | Claim 3 says "there is no waiting step" while D:605 defines step `handback_waiting` (waits for the old worker, not for a person); quotes D:616 as "the place in flight is never freed", actual text "the place is never freed" |
| Feasible with stated constraints | MET | Counting by `route.in_flight` verified at `route.py:379-426` | NOT MET | Round 2 start concedes the re-plan voids the approval with nothing replacing it; `deep` needs a table not on master |
| Consistent terminology | MET | "start gate", "waiting step", `plan_depth` used consistently | MET | `handback`, `plan_tier`, "in flight" consistent |
| No internal contradictions | MET | Claim, Mechanism, Costs agree | MET (weak) | Fact 9 admits a gap in Clay's text but the paper stays consistent |
| Claims supported by evidence | MET | Each claim tied to a fact or code line; OD-1 case thin but traceable to D15 | MET | Each claim backed by D:nnn; weak `deep` claim marked UNVERIFIED |
| **Subtotal** | **4/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Logical section ordering | MET | Claim, Mechanism, Facts, Costs, Risks, Gets right (the brief's order) | MET | Same |
| Consistent hierarchy depth | MET | H1 then six flat H2 | MET | Same |
| Separation of concerns | MET | Cost, risk, strengths separate | MET | Same |
| Navigation aids | MET (resolved) | Cross-references to D15, D01, D12, D14 and source line refs | MET (resolved) | Header defines the `D:nnn` convention; cross-references to D01, D12, D15 |
| Artifact-type conventions | MET | All brief elements present | MET | All brief elements present |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Unambiguous language | MET | "`quick`", "option (a)", "NOT counted" | NOT MET | "implies `deep`" (UNVERIFIED table); "if a gate is wanted ... option (b)" |
| Concrete not abstract | MET | Workers t3/t2/t1, rounds capped at 4, line refs | MET | `HANDBACK_MAX = 3`, marker `<!-- sc:issue:replan round=<n> -->` |
| Clear section purpose | MET | One job per section | MET | Same |
| Terms defined on first use | NOT MET | C-INV-1, C-INV-2, WC-17, D14, R19, `plan_check` not defined | NOT MET | G6, ruling 36, U60, MR-1, "row 9 of 5.6" not defined |
| Actionable next steps | MET | "Needs C-INV-2"; "add an expiry later only if waiting issues pile up" | MET | Option (b) as fallback; three decisions stated |
| **Subtotal** | **4/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| At least 3 risks with probability and impact | NOT MET | Three risks, no probability or impact | NOT MET | Three risks, no probability or impact |
| Mitigation for each risk | NOT MET | Only the waiting pile has one (visible reason, later expiry) | NOT MET | No mitigations in Risks |
| Failure modes and recovery | NOT MET | No recovery or restart procedure | MET | `handback_recorded` resumes at wave 2; stop raised once as row 9; idempotent marker (D:613, D:617, D:620) |
| External dependencies and their failure | MET | D14 revert, WC-17 fit (UNVERIFIED), wake component unspecified | MET | PR P table missing from master; U60 fidelity |
| Monitoring or validation mechanism | MET | "visible waiting reason" | MET | `no_progress` and `cap` detect a runaway loop |
| **Subtotal** | **2/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Collection boundaries | MET | Unbounded waiting pile; three waiting hand-backs | MET | `no_remaining` (empty list), `cap`, three in flight |
| State-variable interactions | MET | State file vs poll entry vs plan request | MET | State file `in_progress` vs poll count |
| Guard-condition gaps | MET | `plan_check` proves presence only; poll never wakes acknowledged entry | MET | Fact 9: wave-1 re-check lacks the approval |
| Count divergence | MET | Rounds capped at 4 as `1 + HANDBACK_MAX` against `HANDBACK_MAX` = 3 | MET | "up to 4 rounds" against `HANDBACK_MAX` = 3 |
| Interaction effects | MET | Re-plan voids approval with the in-flight count and the wake path | MET | Re-plan voids approval while the place is never freed |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 5/5 | 4/5 |
| Correctness | 4/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 3/5 |
| Risk Coverage | 2/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.8333** | **23/30 = 0.7667** |

### Edge Case Floor Check
Both variants score 5/5 on Invariant & Edge Case Coverage (floor is 1/5): both eligible as base.

## Position-Bias Mitigation

Pass totals before resolution: Variant 1 = 23 (Pass 1) and 24 (Pass 2); Variant 2 = 23 (Pass 1) and 22 (Pass 2).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness: success criteria | V1 | MET | NOT MET | DISAGREE | MET (fact 7 gives a testable condition; same standard applied to V2) |
| Completeness: out of scope | V1 | NOT MET | MET | DISAGREE | MET (named exclusions "no `handback_awaiting_go`, no `answer-check` per round") |
| Structure: navigation aids | V1 | NOT MET | MET | DISAGREE | MET (criterion allows cross-references; present) |
| Completeness: success criteria | V2 | MET | NOT MET | DISAGREE | MET (fact 8 stop conditions; same standard) |
| Correctness: no factual errors | V2 | MET | NOT MET | DISAGREE | NOT MET ("no waiting step" contradicts D:605 step name; D:616 quote altered; both verified by the orchestrator) |
| Structure: navigation aids | V2 | NOT MET | MET | DISAGREE | MET (same standard as V1) |

Disagreements re-evaluated: 6 (3 per variant).
Final verdicts that differ from Pass 1: 4 (V1 out-of-scope, V1 navigation, V2 no-errors, V2 navigation). Final verdicts that differ from Pass 2: 2 (V1 and V2 success criteria).
Limitation: the re-evaluation was done by the orchestrator, who also wrote the diff analysis; the two evaluator agents were independent of it.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| 1 (OURS) | 0.4993 | 0.4167 | **0.9160** | 12 points won (C-001, C-002, C-003, C-004, C-007, X-001, X-002, X-003, A-001 to A-004) |
| 2 (CLAY) | 0.4981 | 0.3833 | **0.8815** | 1 point won (C-006); 3 ties (S-001, S-002, C-005) |

**Margin**: 3.45 points (0.0345), below the 5% threshold
**Tiebreaker applied**: Yes, level 1 (debate performance): Variant 1 won 12 diff points against 1; the debate counts are not within 5% of each other, so level 2 and 3 are not needed.

## Selected Base: Variant 1 (OURS)

### Selection Rationale
Variant 1 scores higher on the combined score (0.916 against 0.882) and wins the debate tiebreaker 12 to 1. The lead comes from the qualitative layer (25/30 against 23/30): V2 loses points for a position that concedes the round-2 approval gap (K2), hedged wording (L1), a mis-stated "no waiting step" (K1) and no out-of-scope statement (C5); V1 loses points for a wrong file path and a loosely related source (K1) and has the weaker risk section (R3). Both advocates, one of them Clay's, favored V1 on the contested rules (OD-1, OD-2, OD-13).

### Strengths to Preserve from Base
1. The three answers: `quick` default with a plain `plan_depth` key (C-001, C-002); re-plan then re-approve (C-003); waiting step not counted (C-004), with the wake path and invariants C-INV-1 and C-INV-2 (C-007, U-001).
2. The code-based evidence for what counts as in flight (`route.py:379-426`, `cycle.py:993-994`) and the option of status `escalated` as the carrier of a waiting step (advocate proposal, UNVERIFIED side effects).

### Strengths to Incorporate from Non-Base Variants
1. From Variant 2, Mechanism and Cited facts 6-8 (D:612-614, D:1078-1080): the `handback` bounds (`no_remaining`, `cap`, `no_progress`), the old-worker-final rule, the idempotent re-plan marker and the `--remaining` re-plan (C-006, U-005, U-006). They hold under any start rule.
2. From Variant 2, Claim 1 and Mechanism bullet 1 (D:60, D:722): goal G6 as an option: keep `quick` as the default, allow a per-repo `plan_depth` of `standard` or `deep` (C-005, U-004).
3. From Variant 2, Cited fact 9 (U-007): the wave-1 re-check must repeat the approval (D01 MR-1); and from V2 Costs, the explicit statement of what its rule costs (no human between re-plan and a new worker).
4. Corrections to carry into the merged text: fix the `predicates.py` path (master, not pr-a); drop or re-label V1 fact 2 (D12 item 6 is a create-time floor); state that D:616 says "Nothing is escalated for a hand-back", so using status `escalated` for the waiting step is an extension that needs its own side-effect check.
