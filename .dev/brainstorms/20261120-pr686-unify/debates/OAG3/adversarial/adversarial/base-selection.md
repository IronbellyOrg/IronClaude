# Base Selection Report

Variants: Variant 1 = OURS (`variant-1-original.md`), Variant 2 = CLAY (`variant-2-original.md`). Scoring was done by the orchestrator (one model, no separate scorer agent). Both position-bias passes were therefore run by the same reader in opposite order; this is a limit on their independence and is stated here, not hidden. The "source requirements" for requirement coverage are the 6 sections the debate brief requires of a position paper plus the two sub-questions OA-28a and OA-28b (8 items); the source has no formal requirement IDs, so section-level matching applies (edge case in the protocol).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 1.00 (8/8: claim, mechanism, 5-10 facts, costs, risks, gets-right, OA-28a, OA-28b) | 1.00 (8/8, same items) |
| internal_consistency | 0.25 | 0.95 (1 contradiction, X-002, in about 21 claims) | 1.00 (0 internal contradictions in about 19 claims; X-003 and X-004 are errors against sources, scored under Correctness) |
| specificity_ratio | 0.15 | 0.94 (estimate by sampling: nearly every claim carries a file:line, number or named constant) | 0.92 (estimate by sampling, same method) |
| dependency_completeness | 0.15 | 1.00 (no broken internal references; external references excluded) | 1.00 |
| section_coverage | 0.15 | 1.00 (6 of 6 H2 sections, the maximum) | 1.00 (6 of 6) |
| **quant_score** | | **0.979** | **0.988** |

Computation: V1 = 0.30 + 0.25(0.952) + 0.15(0.94) + 0.15 + 0.15 = 0.979. V2 = 0.30 + 0.25(1.00) + 0.15(0.92) + 0.15 + 0.15 = 0.988. The specificity figures are estimates, not an exhaustive grep (UNVERIFIED to the second decimal); they move the margin by under 0.005.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Format: verdict (MET = 1, NOT MET = 0) with the evidence used (Claim-Evidence-Verdict). A MET without citable evidence defaults to NOT MET.

### Completeness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| Covers all explicit requirements | MET | Claim answers OA-28a and OA-28b separately | MET | Claim answers both separately |
| Addresses edge cases/failures | MET | Facts 3-4: generation skips, failed check keeps `enabled: false`; Risks: 516 missing gives `worktree_invalid` | MET | Facts 6-8: INV-025, unrun X-001, 516 not landed |
| Includes dependencies/prerequisites | MET | R33 before R18, S17, Coder 516 | MET | S17, X-001, 516, "no config before S17" |
| Defines success/completion criteria | NOT MET | No definition of "passed" for the S17 run (A-001) | NOT MET | Same gap (A-001) |
| Specifies out-of-scope items | NOT MET | No out-of-scope list searched in all six sections | NOT MET | None found |
| **Subtotal** | **3/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| No factual errors or hallucinated claims | MET | Spot-checked by the orchestrator: `defaults.py:30`, `repos.py:141`, `launch.py:48`, `repo_init.py:93-116`, `first_run.py:193`, `dispatch.py:411,417` all match the code read this session | NOT MET | Fact 3 (tests "encode" the flat NG-2) is wrong: they scan the cycle, and the planb test at `test_security_invariants.py:1059-1079` permits `repo_init.py` as a writer (X-003); fact 4 misapplies D:1125 (X-004). Both conceded by Advocate 2 |
| Technical approach feasible within stated constraints | MET | Idempotent label create behind a read; one defaults key needed | MET | Same key; per-repo go is a chat action |
| Terminology consistent and accurate | MET | "poll cycle", "init", "first run" used consistently | MET | "setup", "poll", "init" used consistently |
| No internal contradictions | NOT MET | X-002: Claim says "behind the owner's chat OK"; Costs says "without a fresh chat go" | MET | None found |
| Claims supported by evidence within the document | MET | Nine cited facts each carry a source | NOT MET | Facts 3 and 4 do not support the use made of them (X-003, X-004) |
| **Subtotal** | **4/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| Logical section ordering | MET | Claim, Mechanism, Facts, Costs, Risks, Gets right | MET | Same order |
| Consistent hierarchy depth | MET | One level of H2 under one H1 | MET | Same |
| Clear separation of concerns | MET | Costs and Risks separate | MET | Same |
| Navigation aids | MET | "Paths:" legend defines planb, MR, REQ | MET | "Paths:" legend defines planb, MR, D:nnn |
| Follows artifact-type conventions | MET | Matches the brief's required headings (claim, mechanism, facts, costs, risks, gets right) | MET | Same |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| Unambiguous language | NOT MET | The owner-OK wording for the label write is ambiguous between its Claim and Costs (X-002) and the ambiguity changes the OA-28b answer | MET | Each position is stated in one sentence with no hedge words in the claim |
| Concrete rather than abstract | MET | Named files, lines, constants | MET | Same |
| Each section has a clear purpose | MET | Each H2 is one purpose | MET | Same |
| Acronyms and terms defined on first use | NOT MET | S17, INV-025, R33, X-001 not defined in the paper | NOT MET | S17, INV-025, K24, X-001, MC-12 not defined |
| Actionable next steps or decision points | MET | "The proof is the owner's go at S17" | MET | "The owner names the repo in chat" |
| **Subtotal** | **3/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| At least 3 risks with probability and impact | NOT MET | Costs and Risks list 5 items but give no probability | NOT MET | Same: no probability given |
| Mitigation for each identified risk | MET | Wrongly-enabled repo bounded by owner filter, generation, gate, approval; 516 gap keeps repos off | NOT MET | The two Risks (zero-setup not zero; label creation may return in code) carry no mitigation |
| Failure modes and recovery | MET | Failed check leaves `enabled: false`; label is deletable | NOT MET | No recovery path stated for a self-created label or a wrongly named repo |
| External dependencies and failure scenarios | MET | Orca listing, Coder 516 | MET | 516, X-001, Orca listing |
| Monitoring or validation mechanism | MET | `first-run.txt` report written either way | MET | `run-all --dry-run` reports `would_generate` |
| **Subtotal** | **4/5** | | **2/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| Collection boundaries (empty, single, maximum) | MET | Generation: no Project, several unmapped Projects, no approvers each skip (`generate.py:218-246`) | NOT MET | No collection boundary discussed |
| State variable interactions across component boundaries | MET | `enabled` flag, state dir, store and lock tests (`first_run.py:1-22`) | MET | Mechanism 2: generate and check without rewriting `enabled` while the key is false |
| Guard condition gaps | MET | Ship gate, INV-025 named | MET | INV-025, one-constant gate |
| Count divergence (off-by-one, ranges) | NOT MET | Not addressed in any section | NOT MET | Not addressed |
| Interaction effects when features combine | MET | `run-all` + `first_run` + ship gate + approval | MET | `run-all` + cron + label write + switch-on (K24) |
| **Subtotal** | **4/5** | | **3/5** | |

Edge Case Floor Check: both variants score at least 1/5 (V1 4/5, V2 3/5). Both eligible as base.

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 3/5 | 3/5 |
| Correctness | 4/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 3/5 | 4/5 |
| Risk Coverage | 4/5 | 2/5 |
| Invariant & Edge Case | 4/5 | 3/5 |
| **qual_score** | **23/30 = 0.767** | **20/30 = 0.667** |

## Position-Bias Mitigation

Pass 1 evaluated V1 then V2; Pass 2 evaluated V2 then V1, both by the orchestrator.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness: edge cases/failures | V2 | MET | NOT MET | DISAGREE | MET (facts 6-8 name failure scenarios) |
| Correctness: claims supported by evidence | V2 | MET | NOT MET | DISAGREE | NOT MET (facts 3 and 4 do not support their use) |
| Clarity: unambiguous language | V1 | MET | NOT MET | DISAGREE | NOT MET (the owner-OK ambiguity changes the OA-28b answer) |
| Invariant: state variable interactions | V2 | NOT MET | MET | DISAGREE | MET (Mechanism 2 describes the state boundary) |

Disagreements re-evaluated: 4
Final verdicts changed from Pass 1: 3 (Correctness V2, Clarity V1, Invariant V2)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| 1 (OURS) | 0.490 | 0.383 | **0.873** | 4 points won of 6 decided non-hybrid points (67%) |
| 2 (CLAY) | 0.494 | 0.333 | **0.827** | 2 points won (33%) |

**Margin**: 4.6% (below the 5% threshold)
**Tiebreaker applied**: Yes (level 1, debate performance)

Debate performance count from the scoring matrix: V1 won C-002, C-007, X-003, X-004; V2 won C-006, X-002; HYBRID won S-001, S-002, C-001, A-001, A-002, A-004, A-005; six points are unresolved (S-003, C-003, C-004, C-005, X-001, A-003) and are not counted. 67% against 33% is far outside the 5% band, so level 2 and level 3 are not reached.

## Selected Base: Variant 1 (OURS)

### Selection Rationale
Variant 1 leads on combined score by 4.6 percent and wins the level-1 tiebreaker 4 points to 2. Its lead comes from Correctness (the debate found two source errors in Variant 2, X-003 and X-004, and one in Variant 1, X-002) and from Risk Coverage (mitigations and recovery). Variant 2 scores higher on Clarity and marginally higher on the quantitative layer. The debate itself landed on a HYBRID for the central point C-001 (key ships false until S17, one owner flip after it, no per-repo go), which is Variant 1's end state with Variant 2's staging control.

### Strengths to Preserve from Base
1. NG-2 scoped to the poll cycle, backed by the planb test `test_only_complete_and_repo_init_may_write_to_github` (`test_security_invariants.py:1059-1079`) and the read/write split in `repo_init.py:93-117` (C-002, 82%).
2. The layered reach limits: `allowed_owners`, generation filters, six checks with fail-safe `enabled: false`, closed ship gate, per-issue approval (U-001, U-002; C-003 leans V1).
3. The owner's recorded zero-setup line (R17, R18) and the point that a per-repo go breaks "nothing manual" after repo 1 (C-007, 68%).
4. The observation that Clay's own design has the poll write `hold:plan`, so strict setup is narrower than Clay's design (U-004).

### Strengths to Incorporate from Non-Base Variants
1. From Variant 2 (C-001, A-001, U-008, U-009): the `auto_enable` key ships false; no config is switched on before S17; the owner flips the default once, after S17, with written pass criteria. Two tests: `test_first_run_keeps_config_off_while_auto_enable_false`, `test_dry_run_generates_nothing`.
2. From Variant 2 (C-006): while the key is false the label step is read-only (`trigger_label_state`); it must report `would_create` without failing the whole check, otherwise the check cannot pass without a hand-made label.
3. From Variant 2 (X-002 outcome, U-007): the label write needs the owner's chat OK as a class-level go recorded at the S17 flip; the X-001 live check is a stated precondition.
4. From Variant 2 and both advocates (A-004): an owner-visible report of self-enabled repos.
5. From Variant 2 (C-004): `hold:backlog` creation is not built; do not add it until the owner asks (a small addition, not part of OA-28's go).
6. From both advocates (A-005): cite symbols, not line numbers, because planb is rebased onto post-revert master.
