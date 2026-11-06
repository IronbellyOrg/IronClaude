# Base Selection Report

## Quantitative Scoring (50% weight)
The source has no formal requirement IDs, so requirement coverage uses section-level topic matching over the five topics that appear in either variant: Strongest case, Safety, Reliability, How a person works day to day, Implementation cost. Specificity counts regex matches (citations, dates, rule IDs, backticked identifiers) against a vague-term list; both lists were produced by a fixed shell command and the vague-term list matched nothing in either variant. Neither variant has internal cross-references (every reference points to an outside file), so dependency completeness is vacuously 1.000 for both.

| Metric | Weight | Variant A (explicit flag) | Variant B (command detects Orca) |
|--------|--------|--------------------------|---------------------------------|
| requirement_coverage | 0.30 | 0.800 (4 of 5 topics; no "Strongest case" section) | 1.000 (5 of 5 topics) |
| internal_consistency | 0.25 | 1.000 (0 contradictions in 11 claims) | 0.909 (1 contradiction, X-002, in 11 claims) |
| specificity_ratio | 0.15 | 1.000 (47 concrete, 0 vague) | 1.000 (39 concrete, 0 vague) |
| dependency_completeness | 0.15 | 1.000 (no internal references) | 1.000 (no internal references) |
| section_coverage | 0.15 | 0.800 (4 of 5 H2 sections) | 1.000 (5 of 5 H2 sections) |
| **quant_score** | | **0.910** | **0.977** |

Claims counted as the 10 bullet lines plus the position line (11 per variant).

## Qualitative Scoring (50% weight) — Additive Binary Rubric
Two independent judges scored all 30 criteria for both variants: `judge-pass-1.md` (evaluated A then B) and `judge-pass-2.md` (evaluated B then A). The full Claim-Evidence-Verdict text for each criterion is in those two files. The table gives the final verdicts after reconciling the four disagreements (see Position-Bias Mitigation). A star marks a reconciled verdict. Line references: A:N and B:N are lines of `variant-1-original.md` and `variant-2-original.md`.

| # | Dimension | Criterion | A | B | Key evidence |
|---|-----------|-----------|---|---|--------------|
| 1 | Completeness | Covers all explicit requirements | MET | MET | All four lenses present (A:7, 12, 17, 21; B:12, 16, 21, 24) |
| 2 | Completeness | Edge cases and failure scenarios | MET | MET | A:8 quoted argument, A:19 forgotten flag; B:13 person's tab, B:19 `--print` signal |
| 3 | Completeness | Dependencies and prerequisites | MET | MET | A:15 phase gating; B:5, B:25 |
| 4 | Completeness | Success or completion criteria | MET | NOT MET | A:13 AC-1.1 and A:8 AC-2.8; B gives none (B:17, B:25 are costs) |
| 5 | Completeness | Explicit out of scope | NOT MET* | NOT MET | A:3 is a design exclusion, not a paper-scope statement; B:18 is an argument |
| 6 | Correctness | No factual errors or hallucinated claims | NOT MET* | NOT MET | A:9 headline "would misfire" overreaches (conceded by A's advocate); B:19, B:14, B:10 overstated |
| 7 | Correctness | Feasible within stated constraints | MET | NOT MET | A:22; B:18 admits non-goal 1 and SA-2 are broken |
| 8 | Correctness | Terminology consistent | MET | MET | Used the same way throughout both |
| 9 | Correctness | No internal contradictions | MET | NOT MET | B:9 versus B:17 and B:14 (X-002) |
| 10 | Correctness | Claims supported by evidence | MET | MET | Nearly every bullet carries a SPEC, CAPS or `[G]` line |
| 11 | Structure | Logical section ordering | MET | MET | Position, key, then the lenses |
| 12 | Structure | Consistent hierarchy depth | MET | MET | One H1, H2 sections only |
| 13 | Structure | Separation of concerns | MET | NOT MET | B:9-10 repeats Reliability and Cost; B:14 and B:17 both carry testability |
| 14 | Structure | Navigation aids | MET | MET | Citation key at A:5 and B:5 |
| 15 | Structure | Follows decision-option conventions | MET | MET | Titled option, position, lens sections |
| 16 | Clarity | Unambiguous language | MET | MET | No hedge words in either |
| 17 | Clarity | Concrete rather than abstract | MET | MET | Example commands and counts in both |
| 18 | Clarity | Each section has one purpose | MET | MET | One lens per section |
| 19 | Clarity | Terms defined at first use | NOT MET | NOT MET | SA-1, WC-9, AC-1.1, AC-C1 and "item 13" undefined in both |
| 20 | Clarity | Actionable next steps or decision points | MET* | NOT MET | A:18 "The coordinator copies the command line from the brief template"; B has none |
| 21 | Risk coverage | At least 3 risks with probability and impact | NOT MET | NOT MET | Risks named, none rated |
| 22 | Risk coverage | Mitigation for each risk | MET | NOT MET | A:8, A:9, A:19; B names no mitigation for model miss or coupling |
| 23 | Risk coverage | Failure modes and recovery | NOT MET | NOT MET | Failure modes named, no recovery steps |
| 24 | Risk coverage | External dependencies and failures | MET | MET | A:19, B:9 (Orca reports waiting worker healthy) |
| 25 | Risk coverage | Monitoring or validation mechanism | MET | NOT MET | A:13 AC-1.1 and live checks; B:17 "no token to grep" |
| 26 | Invariant and edge | Boundaries (zero, one, many; quoted arguments) | MET | MET | A:8 quoted argument; B:18 callers with no Orca |
| 27 | Invariant and edge | State variable interactions | MET | MET | Variable versus `worker-list` handles (A:9, B:13) |
| 28 | Invariant and edge | Guard condition gaps | MET | MET | A:19, A:22; B:14, B:17 |
| 29 | Invariant and edge | Count divergence | NOT MET* | NOT MET | Counts quoted (11, 35) but no divergence scenario in either |
| 30 | Invariant and edge | Interaction effects | MET | MET | A:10 flag with outward defaults; B:13 route with SA-1 |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 3/5 |
| Correctness | 4/5 | 2/5 |
| Structure | 5/5 | 4/5 |
| Clarity | 4/5 | 3/5 |
| Risk Coverage | 3/5 | 1/5 |
| Invariant & Edge Case Coverage | 4/5 | 4/5 |
| **qual_score** | **24/30 = 0.800** | **17/30 = 0.567** |

### Edge Case Floor Check

Threshold: at least 1/5 on Invariant & Edge Case Coverage. Variant A 4/5: eligible. Variant B 4/5: eligible. Floor not suspended.

## Position-Bias Mitigation
Pass 1 totals: A 24/30, B 17/30. Pass 2 totals: A 26/30, B 17/30. The two passes agree on 56 of 60 criterion-variant verdicts, and on every Variant B verdict.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| 5 Out of scope | A | NOT MET | MET | DISAGREE | NOT MET |
| 6 No factual errors | A | MET | NOT MET | DISAGREE | NOT MET |
| 20 Actionable next steps | A | NOT MET | MET | DISAGREE | MET |
| 29 Count divergence | A | NOT MET | MET | DISAGREE | NOT MET |

Re-evaluation (made by the orchestrator in this session with both passes' evidence side by side; this is the single-agent form of the protocol's comparison prompt and is recorded here so it can be audited):
- Criterion 5: Pass 2 cited A:3 and A:23. A:3 is the option's design exclusion and A:23 a deferral; neither says what the paper leaves out of scope. Variant B's equivalent line (B:3) was scored NOT MET by both passes, so MET would be inconsistent. NOT MET.
- Criterion 6: Both advocates verified A's citations, but Variant A's own advocate conceded that the A:9 headline "Detection would misfire" rests on an environment-variable observation only. A conceded unsupported generalization fails "no factual errors". NOT MET.
- Criterion 20: A:18 "The coordinator copies the command line from the brief template" is a specific, actionable instruction; Pass 1 looked only at A:23. MET. Variant B has no equivalent (B:22 says no flag to remember).
- Criterion 29: Pass 2 cited A:15 (phase gating) and A:13 (per-phase check). Those are set-membership checks, not an examined count mismatch such as off-by-one or inclusive/exclusive. NOT MET, as for Variant B.

Disagreements re-evaluated: 4. Final verdict differs from Pass 1 in 2 (criteria 6, 20) and from Pass 2 in 2 (criteria 5, 29).

## Combined Scoring
| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points won |
|---------|---------------|--------------|-----------------|-------------------|
| A (explicit flag, `option-a.md`) | 0.455 | 0.400 | **0.855** | 7 of 14 |
| B (command detects Orca, `option-b.md`) | 0.489 | 0.283 | **0.772** | 2 of 14 (5 unresolved) |

**Margin**: 8.3 points (above the 5% threshold)
**Tiebreaker applied**: No

Sensitivity note: Variant B leads on the quantitative layer (0.977 versus 0.910) only because it has one more heading ("Strongest case"), which lifts requirement coverage and section coverage, and because Variant A has no internal contradiction. Variant A leads the qualitative layer by 7 criteria (24 versus 17).

## Selected Base
### Variant A (original, `.dev/orca-command-refactor/decisions/D1/option-a.md`: explicit `--unattended` flag)

### Selection Rationale
Variant A wins by 8.3 points. It won 7 of the 9 resolved debate points, including testability (C-004) and Orca coupling (C-005), where Variant B's own advocate conceded; it has no internal contradiction while Variant B contradicts itself on the stalled-worker state (X-002); and it scores 24/30 on the rubric against 17/30. The decision it argues for is also the one the current spec records (line 401, checked).

### Strengths to Preserve from Base
1. Invocation-scoped trigger: the flag lives in one command line and cannot leak into a later command (A:3, A:8).
2. Testability: AC-1.1 and AC-2.8 give checks (A:13).
3. Caller-neutrality and phase gating (A:14, A:15).
4. The explicit statement of its own known weakness (A:19), which is kept and strengthened.

### Strengths to Incorporate from Non-Base Variants
1. From Variant B, Safety (B:13-14): separate the preamble route from the environment-variable route, and scope A's "would misfire" claim to the variable (C-002, won by B at 78%).
2. From Variant B, Strongest case (B:8): Orca defines a worker by the live preamble; that signal belongs in the worker session as a refuse-only guard (U-005, A-003).
3. From Variant B, Strongest case (B:9) and Reliability (B:17): the silent stall is the real failure; A's weakness bullet should say it is now covered before the run by the brief guard, with the residual risk named (C-003, won by B at 70%).
4. From Variant B, Reliability (B:19): the reflect `claude --print` precedent and why it gives no signal for an Orca worker, marked UNVERIFIED as the spec marks it (U-006).
5. From the debate (both advocates): A's migration path (A:23) conflicts with non-goal 1, and its `SPEC:N` citations point to the pre-decision spec version.
