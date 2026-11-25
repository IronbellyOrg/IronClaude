# Base Selection (OAG1)

Method note. The quantitative layer was estimated by hand from the two papers (no script was run). The qualitative layer was scored by two independent evaluator agents, one in input order (pass 1: OURS then CLAY) and one in reverse order (pass 2: CLAY then OURS), then the orchestrator resolved each disagreement by re-reading the cited text. Edge-case floor: both variants score 5/5 on the invariant dimension, so both are eligible.

## Quantitative Scoring (50% weight)

Source requirements used: the five sub-questions OA-13a, OA-13b, OA-13c, OA-25a, OA-25b (the papers carry no formal requirement IDs, so section-level topic matching was used).

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) | Computation |
|--------|--------|------------------|------------------|-------------|
| Requirement coverage (RC) | 0.30 | 1.00 | 0.80 | OURS answers all five (OA-13c in fact 8); CLAY never mentions `changes_requested`, so 4 of 5 |
| Internal consistency (IC) | 0.25 | 0.96 | 0.96 | About 28 falsifiable claims each, one tension each: OURS "no push reminder" beside the quoted K9 "with a reminder"; CLAY says an expiry should stop a waiting item "holding capacity" though K15 puts `waiting_reapproval` outside the cap |
| Specificity ratio (SR) | 0.15 | 0.93 | 0.89 | Both cite lines and numbers; CLAY leaves "N hours" and "N" open |
| Dependency completeness (DC) | 0.15 | 0.95 | 0.97 | Terms defined at the top of OURS; CLAY defers its terms to the OURS file; OURS has one vague pointer ("line 244 region") |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | Six H2 sections each |
| **quant_score** | | **0.972** | **0.909** | RC 0.30 + IC 0.25 x 0.96 + SR + DC + SC |

## Qualitative Scoring (50% weight): additive binary rubric, 30 criteria

Per-criterion results after resolving pass disagreements (a MET needs cited evidence). Pass 1 totals: OURS 25, CLAY 25. Pass 2 totals: OURS 24, CLAY 21.

### Dimension subtotals (final)

| Dimension | Variant 1 (OURS) | Variant 2 (CLAY) | Not met (final) |
|-----------|------------------|------------------|-----------------|
| Completeness | 4/5 | 3/5 | OURS: C4 (no testable completion criteria). CLAY: C1 (OA-13c absent), C4 |
| Correctness | 3/5 | 4/5 | OURS: K1 (see below), K4. CLAY: K4 |
| Structure | 5/5 | 5/5 | none |
| Clarity | 4/5 | 4/5 | OURS: L4 (RK-30, K9, INV-023 undefined). CLAY: L4 (terms deferred to another file) |
| Risk coverage | 3/5 | 3/5 | both: R1 (no probability or impact), R2 (no mitigation for the unsourced-number risk) |
| Invariant and edge-case | 5/5 | 5/5 | none |
| **Total** | **24/30** | **24/30** | |

### Disagreements between the passes and their resolution

| Criterion | Variant | Pass 1 | Pass 2 | Final | Evidence for the final verdict |
|-----------|---------|--------|--------|-------|--------------------------------|
| K4 | OURS | MET | NOT MET | NOT MET | OURS claim 3 says "no new push reminder" while fact 5 quotes K9 "with a reminder"; the OURS advocate conceded the word was never defined (diff point X-002) |
| K3 | CLAY | MET | NOT MET | MET | The CLAY paper separates `waiting_reapproval` (fact 5) from a waiting merge go (risks section); the mixing is in one sentence of claim 3, which is a K4 problem, not a term problem |
| K4 | CLAY | MET | NOT MET | NOT MET | Claim 3 says an expiry stops a waiting item "holding capacity", but K15 (`merged-requirements.md:317`) says `waiting_reapproval` is outside the cap, so an expiry frees nothing |
| L1 | CLAY | MET | NOT MET | MET | Claims 1 to 3 each name their target (a go; a hold; a hand-back) |
| R3 | CLAY | MET | NOT MET | MET | The paper names a re-ask on lapse and escalation after the hold |

### Source errors the evaluators verified (carried to the verdict)

1. OURS says a go ends "in exactly three ways" and credits D06 item 1 and Q01 item 5. Q01 item 5 says that; D06 item 1 (`debates/D06/VERDICT.md:14`) says the go "expires (number is an Owner DECISION, no source gives one)". The two verdicts are not worded alike. OA-13's "No expiry" line (`merged-requirements.md:685`) is one open owner option, not a requirement.
2. OURS quotes D:1177 as "not ruled on; open". The same row (`docs/designs/orchestrator.md:1177`) also says "Settled as recommended (ruling 39)", a cap of 5 notices a day; D11 treats ruling 39 as Clay's, not the repository owner's. The design text is inconsistent with itself; the question column says open.
3. OURS fact 5 credits QG1 OD-13 for a K9 quote (see diff point X-001).

## Position-Bias Mitigation

Two evaluator passes in opposite order. Disagreements found: 5 criterion-variant pairs (table above). Every disagreement was settled in favour of one of the two passes, so each final verdict equals one pass and differs from the other: pass 2 won for OURS K4 and CLAY K4; pass 1 won for CLAY K3, L1 and R3. Total effect: pass-1 sums 25 and 25, pass-2 sums 24 and 21, final 24 and 24.

## Combined Scoring

| Variant | 0.50 x quant | 0.50 x qual | Combined |
|---------|--------------|-------------|----------|
| Variant 1 (OURS) | 0.486 | 0.400 | **0.886** |
| Variant 2 (CLAY) | 0.455 | 0.400 | **0.855** |

Margin 3.1 percent, below 5 percent, so the tiebreaker protocol applies.

Tiebreaker level 1 (debate performance, points won in Round 1 and the forced round): OURS wins C-001, C-002, C-003 and A-004; CLAY wins none outright; C-004 is split by state; the rest are agreed. OURS has more points won. Tiebreaker level 2 (correctness criteria met) was not needed (OURS 3, CLAY 4 would favour CLAY, noted for transparency; level 1 decided). Tiebreaker applied: yes (level 1).

## Selected Base: Variant 1 (OURS)

Selection rationale. OURS covers every sub-question (including `changes_requested`), keeps the owner's recorded rules, invents no number, and loses points only on citation hygiene and one undefined word. CLAY's paper is the more careful on citations but omits one sub-question and misstates one capacity effect.

Strengths to preserve from the base. No clock expiry; the sha-bound, one-shot go; the second gate run; WC:241 (live conversation or confirmation at the moment of action); silence is never a yes; no committed work dropped; no new notice sender in the first build.

Strengths to incorporate from CLAY.
1. A defined meaning of "reminder": display plus the age of the wait, with a push notice reserved (fixes X-002).
2. The K15 expiry for `waiting_reapproval` only, as an owner-set limit with no default number (fixes X-001).
3. A reserved clock check: when merge automation is built, the build must include a go age check and must refuse to start unless the owner recorded a number or an explicit "none".
4. Naming the start of the reviewer-hold clock: 60 minutes from the final head's checks finishing (already in D06 item 4; ADD4 agrees).
5. The daily report as the existing re-listing surface for an unanswered entry (`agent-work-report/SKILL.md:22,30`), with the caveat that it is configured for one named person today.
