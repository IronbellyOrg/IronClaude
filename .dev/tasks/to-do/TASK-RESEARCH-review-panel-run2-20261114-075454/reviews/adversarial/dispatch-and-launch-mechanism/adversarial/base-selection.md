# Base Selection Report

Slot C-07 (dispatch-and-launch-mechanism). Variant 1 = Proposal A (`variant-1-original.md`, per-environment launch adapters). Variant 2 = Proposal B (`variant-2-original.md`, class-word dispatch only). Each variant is scored as written; the gated hybrid that the debate later produced is not credited to either. Scoring files in this folder: `quant-score.py`, `quant-score-output.json` (deterministic layer), `score-pass1.md` (input order), `score-pass2.md` (reverse order), `score-reeval.md` (position-bias re-evaluation, 8 pairs). The full CEV (claim, evidence, verdict) text for every criterion is in those files; the tables below carry the final verdicts and a one-line deciding note.

## Quantitative Scoring (50% weight)

Requirement source: the C-07 conflict row and the position-paper template, 30 topics (no formal requirement IDs exist, so the protocol's topic-matching edge case applies; topic list and regexes are in `quant-score.py`). Contradiction counts come from the diff analysis: intra-variant X-008 and X-009 in Variant 1, none recorded for Variant 2.

| Metric | Weight | Variant 1 (Proposal A) | Variant 2 (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 0.8000 (24 of 30 topics; missing swarm HTTP transport, family-alias "not verified", research 03, 06, 07, GQ-049) | 0.9333 (28 of 30; missing research 03 and 07) |
| internal_consistency | 0.25 | 0.8824 (2 contradictions over 17 tagged claims) | 1.0000 (0 over 28 tagged claims) |
| specificity_ratio | 0.15 | 1.0000 (358 concrete, 0 vague) | 1.0000 (431 concrete, 0 vague) |
| dependency_completeness | 0.15 | 1.0000 (13 of 13 internal references resolve) | 1.0000 (60 of 60) |
| section_coverage | 0.15 | 0.7778 (7 of 9 H2 sections) | 1.0000 (9 of 9) |
| **quant_score** | | **0.8773** | **0.9800** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdict per criterion: where Pass 1 and Pass 2 agreed, the agreed verdict; where they disagreed (8 pairs, marked R), the re-evaluation verdict in `score-reeval.md`. 1 = MET, 0 = NOT MET.

### Completeness (5 criteria)

| Criterion | Variant 1 | Variant 2 | Deciding note |
|-----------|-----------|-----------|---------------|
| C1 Covers all explicit requirements from source input | 0 (R) | 1 | Variant 1 omits three explicit row elements: the family-alias "not verified" clause, GQ-049 and research 03/06/07 (0 grep hits each); Variant 2 has them (s9, header). |
| C2 Addresses edge cases and failure scenarios | 1 | 1 | V1 M-1/M-2 wrong-if rules; V2 E11 dropped-argument run and residuals. |
| C3 Includes dependencies and prerequisites | 1 | 1 | V1 s4 slot dependencies (C-01, C-02, C-03, C-06, C-08); V2 s8, s2 rows for C-08 and C-09. |
| C4 Defines success/completion criteria | 1 | 1 | V1 M-1 to M-3 right/wrong rules; V2 s5 item 1 "B is right if ... wrong if". |
| C5 Specifies what is out of scope | 1 | 1 | V1 "not decided here" (C-08, C-02, C-03); V2 s9 "not decided here". |
| **Subtotal** | **4/5** | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant 1 | Variant 2 | Deciding note |
|-----------|-----------|-----------|---------------|
| K1 No factual errors or hallucinated claims | 0 | 0 | V1: `adapters` key rejected by `validate_tiers` (`panel.py:371-373`), "change D4's trigger" refuted in part (`SKILL.md:320`), "silent swap", "no check at all today", invalid full commit id. V2: "Position A rewrites the same test" is false for A's additive form (diff X-002); "no such test found" is false (diff X-007); the packaged `gateway.launch` fill was withdrawn by B's own advocate. |
| K2 Technical approaches are feasible with stated constraints | 0 | 0 | V1: `adapters` cannot load as written; ceiling check reads no `read_only` (X-009); E2 identity evidence ran under `bypassPermissions` (X-008); `agent-class` has no executor in Python. V2: packaged class-word fill is wrong per seed and changes `tiers_sha256`; dispatch-error rule has no enforcer. |
| K3 Terminology consistent and accurate | 0 | 1 | V1 calls the orchestrator's Agent call a launch adapter the core defines and carries two parallel maps with no precedence; V2 uses "dispatch contract", "launch word", "intended/served" consistently. |
| K4 No internal contradictions | 0 | 1 (R) | V1 has X-008 and X-009 inside the document; for V2 the Pass 2 items were feasibility defects already counted under K2, not statements that conflict (counting them again would score one defect twice). |
| K5 Claims supported by evidence or rationale | 1 | 1 | V1 11 evidence points with file:line and tags; V2 15-row evidence table plus "what the evidence does not show". |
| **Subtotal** | **1/5** | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant 1 | Variant 2 | Deciding note |
|-----------|-----------|-----------|---------------|
| S1 Logical section ordering | 1 | 1 | Both order position, consequence, evidence, invariants, test/consumers, objection. |
| S2 Consistent hierarchy depth | 1 | 1 | V1 flat; V2 H3 only under s3. |
| S3 Clear separation of concerns | 0 (R) | 1 | V1 s4 "Invariants" holds a cross-slot "Dependencies" block and s3 point 6 puts design rules in the evidence list; V2 gives dependencies and open facts their own sections (s8, s9). |
| S4 Navigation aids present | 1 | 1 | Citation legends, labelled tests (V1 M-1..M-4), E-row ids (V2). |
| S5 Follows artifact conventions | 1 | 1 | Both follow the position-paper sections. |
| **Subtotal** | **4/5** | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant 1 | Variant 2 | Deciding note |
|-----------|-----------|-----------|---------------|
| L1 Unambiguous language | 0 (R) | 1 | V1 states the ceiling gate two non-equivalent ways (s1 "mechanically restricted" vs s2 `adapter` is `claude-p`) and no precedence between `launch` and `adapters`; V2's rule is one sentence. |
| L2 Concrete rather than abstract | 1 | 1 | Both name files, lines, keys, ids and runs. |
| L3 Each section has a clear purpose | 1 | 1 | Both. |
| L4 Terms defined on first use | 0 (R) | 0 (R) | One standard for both: a gloss at or before first use, no external pointer. V1 first uses INV-L, the Fable and `classes` rules, D3, tier names undefined; V2's header uses INV-G/L/F and C-S6/CO-10/FX-13 before the s4 glosses and points to "synth-06 6.12.0"; "sidechain" and "shim" undefined. |
| L5 Actionable next steps or decision points | 1 | 1 | V1 M-1..M-4 with consequence; V2 s5 items 1-6 and the owners in s9. |
| **Subtotal** | **3/5** | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant 1 | Variant 2 | Deciding note |
|-----------|-----------|-----------|---------------|
| R1 At least 3 risks with probability and impact | 1 (R) | 1 | V1: class-word drift (five calls), A-r3 collapse, shim swap (two runs), plus four rated endangered items; V2: E11 "1 of 15", E7 "2 runs", INV-G HIGH. |
| R2 Mitigation for each identified risk | 1 | 0 | V1 gives a control for each endangered item (read-only marker plus probe, additive form, module isolation); V2 leaves its two INV-G gaps open ("B does not close") and hands one to C-11. |
| R3 Failure modes and recovery | 1 | 1 (R) | V1 takes the ladder from the resolution and falls back to `agent-class` if M-2 fails; V2 s5 item 6 names a trigger, an action and an owner for the position's own failure. |
| R4 External dependencies and failure scenarios | 1 | 1 | V1 CLI-update and version gate; V2 Agent enum, `resolvedModel`, hooks behaviour unverified. |
| R5 Monitoring or validation mechanism | 1 | 1 | V1 launcher records `model_observed` and tool names, probe re-run at install; V2 collapse replay, read-only pin test, `SubagentStop` spike. |
| **Subtotal** | **5/5** | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant 1 | Variant 2 | Deciding note |
|-----------|-----------|-----------|---------------|
| I1 Collection boundaries (empty, single, maximum) | 1 | 1 | Empty `gateway.launch`, the 3-cap, `live7` seven reviewers. |
| I2 State variable interactions across components | 1 | 1 | Class word to env alias to shim; session persistence for a re-ask. |
| I3 Guard condition gaps | 1 | 1 | Ladder overwrite, Bash open, `_check_reflect_resolution` guards only `launch`. |
| I4 Count divergence | 1 | 1 | A-r3 collapse; `requested` collapse (C-03 INV-007); `live7` seven models for four words. |
| I5 Interaction effects | 1 | 1 | Additive key vs pins and D4; hook-exchange families skip subagents. |
| **Subtotal** | **5/5** | **5/5** | |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 4/5 | 5/5 |
| Correctness | 1/5 | 3/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 3/5 | 4/5 |
| Risk Coverage | 5/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **22/30 = 0.7333** | **26/30 = 0.8667** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Threshold | Status |
|---------|-----------------------------|-----------|--------|
| Variant 1 | 5/5 | >= 1/5 | ELIGIBLE as base |
| Variant 2 | 5/5 | >= 1/5 | ELIGIBLE as base |

Floor not suspended: both variants meet it.

## Position-Bias Mitigation

Pass 1 evaluated Variant 1 then Variant 2; Pass 2 (independent, did not read Pass 1) evaluated Variant 2 then Variant 1. Pass 1 totals: Variant 1 24/30, Variant 2 27/30. Pass 2 totals: Variant 1 23/30, Variant 2 24/30. The two passes disagreed on 8 of 60 criterion-variant pairs; a third agent re-evaluated each (final verdict, no appeal), applying one standard to L4 for both variants.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| C1 | Variant 1 | 0 | 1 | DISAGREE | 0 |
| S3 | Variant 1 | 1 | 0 | DISAGREE | 0 |
| L1 | Variant 1 | 0 | 1 | DISAGREE | 0 |
| L4 | Variant 1 | 1 | 0 | DISAGREE | 0 |
| R1 | Variant 1 | 1 | 0 | DISAGREE | 1 |
| K4 | Variant 2 | 1 | 0 | DISAGREE | 1 |
| L4 | Variant 2 | 1 | 0 | DISAGREE | 0 |
| R3 | Variant 2 | 1 | 0 | DISAGREE | 1 |

Disagreements re-evaluated: 8. Final verdicts changed from Pass 1: 3 (V1 S3, V1 L4, V2 L4). Changed from Pass 2: 5. Both routes give Variant 1 22/30 and Variant 2 26/30. Both layers rank Variant 2 first; the rank does not depend on the re-evaluated pairs (Variant 2 leads under Pass 1 alone, 27 to 24, and under Pass 2 alone, 24 to 23).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| 1 (Proposal A) | 0.4386 | 0.3667 | **0.8053** | not needed (Step 2 points won: 2) |
| 2 (Proposal B) | 0.4900 | 0.4333 | **0.9233** | not needed (Step 2 points won: 9) |

**Margin**: 11.80% (above the 5% threshold)
**Tiebreaker applied**: No (the debate tally, Variant 2 9 points against Variant 1 2, points the same way and is reported for reference)

## Selected Base: Variant 2 (Proposal B; default model, default persona)

### Selection Rationale

Variant 2 leads on both layers: quant 0.9800 against 0.8773 (requirement coverage 0.9333 against 0.8000, internal consistency 1.0 against 0.8824, section coverage 1.0 against 0.7778) and qual 26/30 against 22/30 (Correctness 3/5 against 1/5, Structure 5/5 against 4/5, Clarity 4/5 against 3/5, Completeness 5/5 against 4/5); Variant 1 leads only on Risk Coverage (5/5 against 4/5). The margin is 11.80%, above the 5% tiebreaker threshold, so no tiebreaker was applied.

Where each variant lost Correctness: Variant 1's defects are two intra-variant contradictions (X-008 identity evidence from a flag set the read-only adapter cannot use; X-009 ceiling widened without reading `read_only`), an `adapters` key the tier validator rejects (`panel.py:371-373`), and overstatements the advocate conceded. Variant 2's defects are the packaged `gateway.launch` class-word fill (withdrawn by its own advocate in Round 2: wrong per seed, changes `tiers_sha256`), a misstatement of Variant 1 on the test pin (X-002) and a missed existing static test (X-007).

Scope of this selection: the scores rate the two documents as written. They do not rate the gated hybrid that both advocates converged on in Round 2 (21 of 26 points agreed, convergence BLOCKED_BY_INVARIANTS on INV-017). The merge therefore keeps Variant 2 as the base and changes it where the debate withdrew its packaged fill and where Variant 1's gated probes and design pieces were adopted by both advocates.

### Strengths to Preserve from Base (Variant 2)

1. The dispatch contract: the core launches nothing; a reviewer is launched with its `launch` word as the Agent `model` argument; a missing argument is a dispatch error, not a fallback to the agent default (H-gated S1 and V2-bound S1 both keep it).
2. Read-only by construction on the agent-file path (`reflect-reviewer.md:5-8`, pinned statically by `tests/cli/reflect/test_reviewer_readonly_tools.py`), with the 3-reviewer cap and ceiling unchanged now.
3. The 15-row tagged evidence table, the "what the evidence does not show" list and the open-facts section with owners (C-08, C-09).
4. The measurements: collapse-detector replay with a prediction that can fail, the head-to-head on one ground-truth input, the `SubagentStop` served-model spike, the read-only pin test, and the fall-back trigger for the position itself.
5. The placement rule that raw-id launching stays outside the core's resolution, as a `ClaudeProcess` caller (both advocates accepted `ClaudeProcess` as the substrate).

### Strengths to Incorporate from Non-Base Variant (Variant 1)

1. The read-only probe as a falsifiable gate with a stated fallback (M-2, restated as G2 under the restricted flag set, with the init-event tool list and the grounding MCP tools as pass criteria), and the identity/reach gate (M-1, restated as G1 under restricted flags, because E2's `bypassPermissions` evidence does not transfer: X-008).
2. The outcome row per attempt (`model_requested`, `model_observed`, `identity_source`, fallback taken, tool names seen) judged against the id requested for that attempt, as the one transcript reader of S3 (home is slot C-08).
3. Variant 1's evidence that a class word is a per-session alias, not a model (haiku served three different models across combos), and the reach arithmetic from Round 2 (packaged `reflect-pre` reaches five models for three words, picked per run id), as the reason the packaged `gateway.launch` fill is replaced by a binding stated as data in a workspace or explicit `--tiers` file.
4. The interface constraint from slot C-06 (a persisted session is needed for a bounded re-ask; `ClaudeProcess` always passes `--no-session-persistence`) and the launcher requirement to walk the resolution `fallbacks` once with an exclusion list (N7).
5. The rule that a module needing INV-G refuses an unproven reviewer and that untrusted PR diffs use the agent-class path until the read-only probe passes; the ceiling widening by exactly one value as a reviewed edit after G2.
6. The cost measurement M-4 (informational) and the right-if/wrong-if format for every measurement (S-003).
