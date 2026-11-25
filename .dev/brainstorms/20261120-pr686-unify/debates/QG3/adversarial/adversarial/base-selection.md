# Base Selection Report

Method note: a single evaluator (the orchestrating agent) scored both variants; Pass 2 was a reversed-order re-read by the same evaluator, not an independent model. Scores are estimates, not measurements. The two advocates' spot-checks of cited lines all matched (debate-transcript.md).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 1.00 (all four sub-questions OD-6, OD-10, OD-11, OD-12 answered; risks and costs present) | 1.00 (same) |
| internal_consistency | 0.25 | 0.97 (1 intra contradiction, X-003, in about 30 claims) | 0.97 (1 intra contradiction, X-004, in about 30 claims) |
| specificity_ratio | 0.15 | 0.92 (nearly every claim has a file and line; a few unsourced wording lines) | 0.90 (as OURS, with the zero-setup line citing memory the advocate could not read) |
| dependency_completeness | 0.15 | 1.00 (internal references resolve; external D:nnn excluded) | 1.00 |
| section_coverage | 0.15 | 1.00 (6 H2 sections) | 1.00 (6 H2 sections) |
| **quant_score** | | **0.9805** | **0.9775** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| Covers all explicit requirements | MET | Claim block answers OD-6, 10, 11, 12 | MET | Claim block answers the same four |
| Addresses edge cases and failure | MET | Restart between merge and closeout; refusal that looks like a bug | MET | Standing close on a wrong `done` verdict; unreadable file |
| Includes dependencies and prerequisites | MET | Contract line 241; per-PR go record; hook limits | NOT MET | No prerequisite stated for the standing list beyond a chat message to Clay |
| Defines success or completion criteria | NOT MET | No test or acceptance line | NOT MET | No test or acceptance line |
| Specifies what is out of scope | NOT MET | Not stated | NOT MET | Not stated |
| **Subtotal** | **3/5** | | **2/5** | |

### Correctness (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| No factual errors or hallucinated claims | MET | Advocate spot-checks matched (D:688, 694, 696, 763, 799; repos.py; SKILL.md) | MET | Same checks matched |
| Technical approach feasible with stated constraints | NOT MET | Layer 1 "out of reach" is not achievable as the same OS user (A-002; both advocates) | MET | Verb refusal plus test is buildable, limits named (D:688) |
| Terminology consistent | MET | One term per object | MET | One term per object |
| No internal contradictions | NOT MET | X-003 (layer 1 versus hook limit) | NOT MET | X-004 (row 5 versus N6) |
| Claims supported by evidence | MET | 9 cited facts with lines | MET | 8 cited facts with lines |
| **Subtotal** | **3/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| Logical section ordering | MET | Claim, mechanism, facts, cost, risk, merit | MET | Same |
| Consistent hierarchy depth | MET | H2 only | MET | H2 only |
| Separation of concerns | MET | Cost and risk separate | MET | Same |
| Navigation aids | MET | Terms block and per-sub-question claim lines | MET | Same |
| Follows artifact conventions (brief's paper shape, 5 to 10 facts) | MET | 9 facts | MET | 8 facts |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| Unambiguous language | MET | Claim lines state yes or no answers | MET | Same |
| Concrete rather than abstract | MET | Named files, keys, lines | MET | Same |
| Each section has a clear purpose | MET | Headings | MET | Headings |
| Acronyms defined on first use | NOT MET | N6, U57, K22, U42, D04 not glossed | NOT MET | N6, U57, N1, N8, R10 not glossed |
| Actionable decision points | MET | Four claim lines | MET | Four claim lines |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| At least 3 risks with probability and impact | NOT MET | 3 risks, impact only | NOT MET | 3 risks, impact only |
| Mitigation for each risk | MET | "worded narrows", owner-recorded value, refusal must explain | NOT MET | Risks listed without a mitigation |
| Failure modes and recovery | NOT MET | Not given | NOT MET | Not given |
| External dependencies and their failure | MET | Hook cannot see Bash writes; answer-check limits | MET | `answer-check` cannot tell a person from a script |
| Monitoring or validation mechanism | MET | Use log of each grant used | MET | `E-NO-GRANT` logs the grant used (D:696) |
| **Subtotal** | **3/5** | | **2/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| Collection boundaries (empty, single, max) | MET | Empty `grants`; `merge_safety_files: []` | MET | Missing `grants` reads empty; `max_in_flight` 1 to 10 |
| State variable interactions across components | MET | Restart between merge and closeout reads the record | NOT MET | Not discussed |
| Guard condition gaps | MET | Parser accepts weakening values | MET | Shell write the verb never sees (named gap, D:688) |
| Count divergence | NOT MET | None | NOT MET | None |
| Interaction effects | MET | Go ends when head moves vs close; hook vs shell | MET | Standing merge with unprotected master; closeout writes vs `E-NO-GRANT` |
| **Subtotal** | **4/5** | | **3/5** | |

### Qualitative Summary

| Dimension | OURS | CLAY |
|-----------|------|------|
| Completeness | 3/5 | 2/5 |
| Correctness | 3/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 2/5 |
| Invariant & Edge Case | 4/5 | 3/5 |
| **qual_score** | **22/30 = 0.733** | **20/30 = 0.667** |

### Edge Case Floor Check
OURS 4/5, CLAY 3/5: both at or above the 1/5 floor. Both eligible.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 (reverse) | Agreement | Final |
|-----------|---------|--------|------------------|-----------|-------|
| Correctness: feasible with constraints | OURS | NOT MET | MET (layer 2 alone is feasible) | DISAGREE | NOT MET (layer 1 as worded is not achievable; both advocates conceded) |
| Risk: mitigation for each risk | OURS | MET | NOT MET (hook risk has no mitigation beyond wording) | DISAGREE | MET (wording rule and fail-closed values are stated mitigations) |

Disagreements re-evaluated: 2
Final verdicts changed: 0 from Pass 1 (one score moved by the reversed pass and was restored)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| 1 (OURS) | 0.4903 | 0.3667 | **0.8569** | 13 of 17 points won or tied (76%) |
| 2 (CLAY) | 0.4888 | 0.3333 | **0.8221** | 4 of 17 (HYBRID or tie points; 24%) |

**Margin**: 3.5 percentage points (below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance): OURS wins C-001, C-002, C-003, C-005, C-007, C-008, X-001, X-002, X-004, A-001, S-003 outright; CLAY wins none outright; the remaining points are HYBRID or ties.

## Selected Base: Variant 1 (OURS)

### Selection Rationale
Higher combined score (0.857 against 0.822) and the debate tiebreaker favour OURS. Both advocates, including CLAY's, conceded OD-6, OD-10 and OD-11 to OURS. The weighting rule (OURS wins unless CLAY shows a clear evidenced benefit) is met for every sub-question except the separable pieces below.

### Strengths to Preserve from Base
1. Unconditional refusal for release (D:676, U57).
2. One per-PR go that names merge and close; no standing `issue.close` or `pr.merge` (contract line 241).
3. Empty default `grants` with the owner's recorded chat word (`repos.py:295`).
4. Two layers on the config with "narrows" wording and the evidence that the parser accepts weakening values (`repos.py:243`, `:230`, `:262-269`).

### Strengths to Incorporate from Non-Base Variants
1. From Variant 2: the `repos` verb refusal of `reach_daily_max`, `grants` and `merge_safety_files` without an accepted `--answer-ref` (D:688), with tests (D:758, D:765), as the named mechanism of layer 1; layer 1 is then worded "narrows".
2. From Variant 2: the reopen guard (`SKILL.md:114`) and reversibility as the reason the merge go may name the close with "close if closeout's verdict is done".
3. From Variant 2: the enumerated argv list of N6 (`git tag`, `git push --tags`, `git push origin <tag>`, `gh release create`, `edit`, `delete`, `uv publish`, `twine upload`, `npm publish`, D:763) with one refusal test each, as an unconditional refusal with no pass.
4. From Variant 2: the refusal text names the missing grant (visibility benefit of a fail-closed default; answers the zero-setup point).
