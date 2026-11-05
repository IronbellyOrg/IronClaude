# Base Selection

Evaluator: the orchestrator (debate-orchestrator role). Position-bias note: one evaluator scored the variants in input order (1, 2) and then reverse order (2, 1); both passes gave the same verdict on every criterion, so no re-evaluation was needed. This is a single-context evaluation, not two independent judges.

## Quantitative Scoring (50% weight)

Requirements source: the seed brief's 4 Success Criteria and 4 Open Questions (8 items; no formal IDs, so section-level topic matching).

| Metric | Weight | Variant 1 | Variant 2 | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | Both answer all 4 open questions and specify a test per success criterion |
| Internal consistency (IC) | 0.25 | 0.95 | 0.975 | V1: 2 false claims of about 40 (the `install_mcp.py:739` tuple is `(OSError, ValueError, RuntimeError)`, not `(OSError, RuntimeError)`; "not a regression of anything that worked", conceded). V2: 1 (Out of scope says "Docs changes; none", contradicted by docs/getting-started/installation.md:494-498, conceded) |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.90 | Both cite file:line throughout; each carries a few UNVERIFIED rows |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | Every internal reference (edit numbers, test names) resolves |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | Both have the 8 requested H2 sections |
| **quant_score** | | **0.9725** | **0.9788** | |

## Qualitative Scoring (50% weight)

Only criteria where the variants differ are listed with Claim-Evidence-Verdict; every other criterion is MET by both, with evidence in the named sections.

| Dimension | Variant 1 | Variant 2 | Differing criterion (CEV) |
|---|---|---|---|
| Completeness (5) | 4 | 5 | C2 edge cases: V1 omits the NUL path (diff U-001) NOT MET; V2 "Finding 1" covers it MET |
| Correctness (5) | 4 | 4 | C1 no factual errors: V1 misquotes install_mcp.py:739 NOT MET; V2 "Docs changes; none" NOT MET |
| Structure (5) | 5 | 5 | none |
| Clarity (5) | 5 | 4 | C3 one-sentence purpose: V2's 12-row risk table mixes decisions with UNVERIFIED notes (conceded by Advocate 2) NOT MET |
| Risk coverage (5) | 5 | 5 | none |
| Invariant and edge case (5) | 3 | 5 | C3 guard gaps: V1 misses the `ValueError` guard NOT MET; C1 collection boundaries: V1 does not cover an empty record list as a distinct case, V2 does ("Empty record list for a plugin") NOT MET for V1 |
| **Total** | **26/30 (0.867)** | **28/30 (0.933)** | |

Edge case floor (at least 1/5): both eligible.

## Combined Scoring

| Variant | Quant x 0.5 | Qual x 0.5 | Score |
|---|---|---|---|
| Variant 1 (opus:architect) | 0.4863 | 0.4333 | 0.9196 |
| Variant 2 (sonnet:refactorer) | 0.4894 | 0.4667 | 0.9561 |

Margin: 3.7%, under 5%, so the tiebreaker applies. Level 1, debate points won outright: Variant 2 wins C-001, C-002, C-005 (3); Variant 1 wins none outright (C-004 is a merge). Winner: Variant 2.

## Selected Base: Variant 2 (sonnet:refactorer)

Selection rationale: it closes finding 1 on every reachable input (`ValueError` included), its regression tests use real inputs, and its risk accounting names the user-visible cost of option C.

Strengths to preserve from the base: the `(OSError, RuntimeError, ValueError)` tuple; the NUL and loop test inputs; the user-scope filter with the non-dict guard; the env block; the `SENTINEL` and `""` checks; the existing-test impact table.

Strengths to incorporate from Variant 1: the finding-3 test scenario (a foreign `ironclaude` in the `CLAUDE_CONFIG_DIR` profile, seed success criterion 3); the root-of-truth and long-term rationale for option C; the narrow-catch security rationale.

Unresolved C-003 / X-001 (record without `scope`): resolved toward Variant 2's default-to-user. Rationale: the real CLI writes `scope` on every record (seed brief, proven), so the finding-2 scenario is fully covered either way; the default keeps today's behaviour for any older record shape and cannot cause a repeated install each run. Variant 1's strict rule is recorded under Changes Not Being Made.
