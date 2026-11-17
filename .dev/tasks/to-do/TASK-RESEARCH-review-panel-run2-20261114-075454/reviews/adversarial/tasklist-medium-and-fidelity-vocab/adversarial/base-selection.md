# Base Selection: slot X-15 (tasklist-medium-and-fidelity-vocab)

Variants: Variant A = Proposal A (`variant-1-original.md`, Medium is a non-blocking warning; fidelity prompt becomes a tasklist-module vocabulary under the core). Variant B = Proposal B (`variant-2-original.md`, Medium stays blocking; fidelity prompt stays a separate gate outside the core). Both variants are scored as written; the Round 2 hybrids (A+, H+) are not credited to either.

Evidence files: `quant-score.py` and `quant-score-output.json` (deterministic, run with `uv run python`), `score-pass1.md` (order A, B), `score-pass2.md` (order B, A), `score-reeval.md` (the 7 disagreements). Every MET/NOT MET verdict with its Claim-Evidence-Verdict citation is in those three files; this file carries the verdicts and the arithmetic.

## Quantitative Scoring (50% weight)

The source has no formal requirement IDs, so requirement coverage uses topic matching (protocol edge case) over 24 topics taken from the X-15 conflict row and the task brief (listed in `quant-score.py`, `REQ`). Internal consistency uses the intra-variant contradictions found in `diff-analysis.md` (A: X-008; B: X-002; one each).

| Metric | Weight | Variant A | Variant B | Computation |
|--------|--------|-----------|-----------|-------------|
| Requirement coverage (RC) | 0.30 | 1.0000 | 0.9167 | A 24/24 topics. B 22/24; missing R09 (research 05 not cited) and R10 (GQ-060/GQ-160 not cited). |
| Internal consistency (IC) | 0.25 | 0.9773 | 0.9677 | A 1 - 1/44 tagged claims. B 1 - 1/31. |
| Specificity ratio (SR) | 0.15 | 1.0000 | 1.0000 | A 622 concrete / 0 vague. B 366 concrete / 0 vague. |
| Dependency completeness (DC) | 0.15 | 1.0000 | 0.9722 | A 15/15 section refs resolved. B 35/36 (section refs plus E-refs). |
| Section coverage (SC) | 0.15 | 1.0000 | 0.8000 | A 10 H2 sections; B 8 of max 10. |
| **quant_score** | | **0.9943** | **0.9328** | (RC x 0.30) + (IC x 0.25) + (SR x 0.15) + (DC x 0.15) + (SC x 0.15) |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

30 criteria, 6 dimensions, CEV protocol, two position-bias passes (see next section). Final verdicts after re-evaluation of disagreements:

| Dimension | Variant A | Variant B | Criteria not met (final) |
|-----------|-----------|-----------|--------------------------|
| Completeness (CO1-5) | 5/5 | 5/5 | none |
| Correctness (CR1-5) | 3/5 | 4/5 | A: CR1 (the pinned phrase "the unresolved High or Medium HALT resolves as blocked" exists only at `commands/tasklist.md:113`, not in the skill, and A's edit list omits that file), CR4 (fact 13 against section 7 answer 3). B: CR4 (sections 1-2 "the skill's own model" against section 8 "the skill states no model"). |
| Structure (ST1-5) | 5/5 | 4/5 | B: ST1 (the adjudicated outcomes B rests on appear only in section 7, after design and evidence; A puts them first in section 0). |
| Clarity (CL1-5) | 4/5 | 3/5 | A: CL4 (first-use terms such as "follow-up marker", "core pair", "P2 loop", "I7 findings" undefined). B: CL1 (hedge "possibly demote it ... does not pre-judge"), CL4 (S4, C-01..C-03, `F_k`, `synthetic-dnsp` used before they are glossed). |
| Risk Coverage (RK1-5) | 3/5 | 3/5 | Both: RK1 (no probabilities), RK2 (a named cost left without a mitigation). |
| Invariant & Edge Case Coverage (IE1-5) | 5/5 | 5/5 | none |
| **Total** | **25/30** | **24/30** | |

qual_score: A = 25/30 = 0.8333; B = 24/30 = 0.8000.

### Edge Case Floor Check

Invariant & Edge Case Coverage: A 5/5, B 5/5. Both clear the 1/5 floor; both are eligible as base.

## Position-Bias Mitigation

Pass 1 evaluated A then B (independent agent `x15-scorer-pass1`); Pass 2 evaluated B then A (independent agent `x15-scorer-pass2`). Pass totals: Pass 1 A 26, B 26; Pass 2 A 24, B 23. The two passes disagreed on 7 of 60 criterion-variant pairs; each was re-evaluated by a third agent (`x15-scorer-reeval`) with both pieces of evidence, and that verdict is final. Re-evaluation changed the verdict from Pass 1 on 3 pairs (A CL4, B CL4, B ST1) and from Pass 2 on 4 pairs (A CR2, B CL1, B CL2, B CR1).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| CO1 Covers all explicit requirements | A | MET | MET | Agree | MET |
| CO2 Edge cases and failure scenarios | A | MET | MET | Agree | MET |
| CO3 Dependencies and prerequisites | A | MET | MET | Agree | MET |
| CO4 Success/completion criteria | A | MET | MET | Agree | MET |
| CO5 Explicit out of scope | A | MET | MET | Agree | MET |
| CR1 No factual errors | A | NOT MET | NOT MET | Agree | NOT MET |
| CR2 Approaches feasible | A | MET | NOT MET | Disagree | MET (re-evaluated) |
| CR3 Terminology consistent | A | MET | MET | Agree | MET |
| CR4 No internal contradictions | A | NOT MET | NOT MET | Agree | NOT MET |
| CR5 Claims supported | A | MET | MET | Agree | MET |
| ST1 Logical ordering | A | MET | MET | Agree | MET |
| ST2 Consistent hierarchy depth | A | MET | MET | Agree | MET |
| ST3 Separation of concerns | A | MET | MET | Agree | MET |
| ST4 Navigation aids | A | MET | MET | Agree | MET |
| ST5 Follows artifact conventions | A | MET | MET | Agree | MET |
| CL1 Unambiguous language | A | MET | MET | Agree | MET |
| CL2 Concrete, not abstract | A | MET | MET | Agree | MET |
| CL3 Section purpose clear | A | MET | MET | Agree | MET |
| CL4 Terms defined on first use | A | MET | NOT MET | Disagree | NOT MET (re-evaluated) |
| CL5 Actionable next steps/decisions | A | MET | MET | Agree | MET |
| RK1 At least 3 risks with probability and impact | A | NOT MET | NOT MET | Agree | NOT MET |
| RK2 Mitigation for each risk | A | NOT MET | NOT MET | Agree | NOT MET |
| RK3 Failure modes and recovery | A | MET | MET | Agree | MET |
| RK4 External dependencies and failure | A | MET | MET | Agree | MET |
| RK5 Monitoring/validation mechanism | A | MET | MET | Agree | MET |
| IE1 Collection boundaries | A | MET | MET | Agree | MET |
| IE2 State interactions across boundaries | A | MET | MET | Agree | MET |
| IE3 Guard condition gaps | A | MET | MET | Agree | MET |
| IE4 Count divergence | A | MET | MET | Agree | MET |
| IE5 Interaction effects | A | MET | MET | Agree | MET |
| CO1 Covers all explicit requirements | B | MET | MET | Agree | MET |
| CO2 Edge cases and failure scenarios | B | MET | MET | Agree | MET |
| CO3 Dependencies and prerequisites | B | MET | MET | Agree | MET |
| CO4 Success/completion criteria | B | MET | MET | Agree | MET |
| CO5 Explicit out of scope | B | MET | MET | Agree | MET |
| CR1 No factual errors | B | MET | NOT MET | Disagree | MET (re-evaluated) |
| CR2 Approaches feasible | B | MET | MET | Agree | MET |
| CR3 Terminology consistent | B | MET | MET | Agree | MET |
| CR4 No internal contradictions | B | NOT MET | NOT MET | Agree | NOT MET |
| CR5 Claims supported | B | MET | MET | Agree | MET |
| ST1 Logical ordering | B | MET | NOT MET | Disagree | NOT MET (re-evaluated) |
| ST2 Consistent hierarchy depth | B | MET | MET | Agree | MET |
| ST3 Separation of concerns | B | MET | MET | Agree | MET |
| ST4 Navigation aids | B | MET | MET | Agree | MET |
| ST5 Follows artifact conventions | B | MET | MET | Agree | MET |
| CL1 Unambiguous language | B | NOT MET | MET | Disagree | NOT MET (re-evaluated) |
| CL2 Concrete, not abstract | B | MET | NOT MET | Disagree | MET (re-evaluated) |
| CL3 Section purpose clear | B | MET | MET | Agree | MET |
| CL4 Terms defined on first use | B | MET | NOT MET | Disagree | NOT MET (re-evaluated) |
| CL5 Actionable next steps/decisions | B | MET | MET | Agree | MET |
| RK1 At least 3 risks with probability and impact | B | NOT MET | NOT MET | Agree | NOT MET |
| RK2 Mitigation for each risk | B | NOT MET | NOT MET | Agree | NOT MET |
| RK3 Failure modes and recovery | B | MET | MET | Agree | MET |
| RK4 External dependencies and failure | B | MET | MET | Agree | MET |
| RK5 Monitoring/validation mechanism | B | MET | MET | Agree | MET |
| IE1 Collection boundaries | B | MET | MET | Agree | MET |
| IE2 State interactions across boundaries | B | MET | MET | Agree | MET |
| IE3 Guard condition gaps | B | MET | MET | Agree | MET |
| IE4 Count divergence | B | MET | MET | Agree | MET |
| IE5 Interaction effects | B | MET | MET | Agree | MET |

Disagreements found: 7 of 60. Verdicts changed by re-evaluation: 3 relative to Pass 1, 4 relative to Pass 2 (every disputed pair differs from exactly one pass).

## Combined Scoring

| Variant | Quant (x 0.50) | Qual (x 0.50) | Combined |
|---------|----------------|---------------|----------|
| A (Proposal A) | 0.9943 x 0.50 = 0.4972 | 0.8333 x 0.50 = 0.4167 | **0.9138** |
| B (Proposal B) | 0.9328 x 0.50 = 0.4664 | 0.8000 x 0.50 = 0.4000 | **0.8664** |

Margin: 4.74% (|0.9138 - 0.8664| = 0.0474, below the 5% threshold).

Both layers ranked Variant A first. Tiebreaker applied: Yes, level 1 (debate performance): Variant B won 12 diff points in the Step 2 scoring matrix against 4 for Variant A (Hybrid 6, Neither 4, Unresolved 5, shared A-NNN responses 6; see `debate-transcript.md`). Level 1 is decisive because 12 against 4 is not within 5% of each other, so levels 2 and 3 are not reached. For the record, level 2 (correctness criteria MET) would also have favoured B (4 against 3).

## Selected Base: Variant B (Proposal B; default model, default persona)

### Selection Rationale

The combined score favours Variant A by 4.74 points, inside the 5% band, so the protocol's tiebreaker decides. Debate performance is not close: Variant B won 12 points (S-004, S-007, C-003, C-005, C-006, C-009, C-010, X-003, X-005, X-006, X-008, X-009) against 4 for Variant A (S-001, S-002, X-002, X-010). On the points that carry correctness and risk weight, Advocate A conceded in Round 1 or Round 2: the union mitigation does not exist at Stage 7 (X-009), Form 2 is code the adjudicated shape excludes (C-003), the role-table claim is a design intention (X-005), the "one product" wording was loose (X-008), the S5 reading was wider than written (X-006), and the edit list missed `commands/tasklist.md:113` (C-005, C-006). Variant B's losses were the S4 premise (X-002), its line ranges (X-010), and the overstated reading of the archive (C-010, partly). Variant A's quantitative lead comes from topic coverage and section count (research/05 and GQ-060/GQ-160 are cited only by A; A has 10 sections to B's 8). Both layers are reported: the quantitative layer and the qualitative layer both favoured A by small margins; the debate-performance tiebreaker favours B.

Neither variant won as written. After two rounds both advocates converged on a hybrid that sits on Variant B's structure (module-data label map, nothing new in the core, fidelity prompt outside the core, no pinned sentence edited, no loosening before measurement) with Variant A's grading block, consequence boundary, dedup-highest and tie-break-up rules, containment test and measurements. Five points stay unresolved between the advocates (C-001, C-007, C-012, C-013, C-014).

### Strengths to Preserve from Base (Variant B)

- Placement: the fidelity prompt, gate, six frontmatter fields, exit code and layering guard stay in `cli/tasklist/` outside the core; the only seam is a read-only adapter from a finished deviation report (S-004, C-008, C-009).
- The label map is module data and Form 1 only: no `Medium` token, no new core field, no parse-edge hook (C-003); M-X15-4 (no `Medium` token enters `findings.py`, `findings_v2.py`, `ledger.py` or the ledger JSON).
- Zero churn on the 12 pinned sweep rows, `commands/tasklist.md:113` and the two worker-contract pins until measurement says otherwise (C-005, C-006).
- The archived-report data (the only data in either variant) with the corrected reading (2 omissions, 2 dropped acceptance criteria, 1 contradiction, 1 assumption stated as fact) (C-010).
- The pre-registered measurement structure with a stop condition and a default (S-005, S-007, C-011): thresholds registered before any run.
- The separation of what C-S3 decided by evidence from what is design inference (U-015), the `card_convert.py` caution (U-012), the 2N-agent fan-out fact (U-016, X-009).

### Strengths to Incorporate from Non-Base Variants (Variant A)

- A Stage 7 grading block that defines High, Medium and Low (U-001), graded by consequence (PM:225/PM:231, C-002, C-004, C-013), with omission of a roadmap-stated deliverable defined as High (U-002).
- Dedup keeps the highest severity and "when torn between two grades, grade higher" (adopted by both advocates in Round 2; C-007 residue on `F_k` counting remains unresolved).
- A parity/containment test over the skill block and the CLI prompt (C-008), as the tie between the two hand-kept definition texts (A section 5, T2).
- Static tests that need no model call (U-005, S-005); the `reflect_category` hazard note (U-004); the observation that `_tasklist_ready_consistent` reads typed counts only (U-006).
- The measurements M1 (seeded defects, FC/FB counts) and M-X15-5 (flip rate at both boundaries) (C-011).
- Inputs-first dependency table and one-fact-per-row evidence format (S-001, S-002); A's line ranges (X-010); the correction that the pinned HALT sentence lives in `commands/tasklist.md:113` (C-006).
- A-004..A-009 responses as both advocates ended them (A-008 REJECT).
