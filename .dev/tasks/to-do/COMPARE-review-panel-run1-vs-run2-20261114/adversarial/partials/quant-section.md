## Quantitative Scoring (50% weight)

All five metrics were computed by `/tmp/cmp_quant.py` (deterministic regex and counts over `variant-1-original.md` and `variant-2-original.md`; re-running gives identical numbers). Source requirements: the report-shape and decision-relevant items listed under RC (the inputs have no formal FR-/NFR- ids, so the skill's section-level topic-matching edge case applies).

| Metric | Weight | Variant 1 (run 1) | Variant 2 (run 2) |
|---|---|---|---|
| requirement_coverage | 0.30 | 1.000 (24/24; missing: none) | 1.000 (24/24; missing: none) |
| internal_consistency | 0.25 | 0.994 (1 - 5/880 cited-claim lines) | 0.989 (1 - 8/756 cited-claim lines) |
| specificity_ratio | 0.15 | 1.000 (20849 concrete / 0 vague) | 1.000 (19454 concrete / 0 vague) |
| dependency_completeness | 0.15 | 0.795 (696/875 Section refs resolve) | 0.955 (343/359 Section refs resolve) |
| section_coverage | 0.15 | 0.786 (11/14 H2 sections) | 1.000 (14/14 H2 sections) |
| **quant_score** | | **0.936** | **0.991** |

### Internal contradictions counted for IC (established in diff analysis, orchestrator verification and debate)

**V1** (5):
- V1 8.4 states 'ironbelly/shadow-runs 3 commits ahead' (stale: 5 now; r25 re-derivation #2)
- V1 labels 16 of 20 conflicts DECIDED-BY-EVIDENCE although the same report calls 4 debates partial and C-04 depends on availability vs diversity (V2 advocate and X-052; status overclaim)
- V1 Q-54..Q-61 itself flags a verdict-vocabulary contradiction (PENDING/exit 12 vs ESCALATE) in the carried design (U-106)
- V1 count '37 reflect test files' (V1:381) vs 38 (r25 re-derivation #6)
- V1 rf-* '43 call sites' unit unstated and not reproducible (X-022)

**V2** (8):
- V2 SC-04 'declared quorum (decision)' vs delta row G-14 decided quorum (X-004)
- V2 G-85 and 3.5 list the workflow/tasklist entry open while delta row T-4/3.5 says decided (X-005)
- V2 SC-17 'decision, 0.75 or 0.80' vs delta row 'decided by the code: 0.80' (C-017)
- V2 Section 7 C-2 and D9 assert KeyError on the ledger merge path while V2 axis 1 and Appendix B say rejected at findings.py:104 (X-049, X-053; orchestrator VERIFIED-V1)
- V2 2.4 treats installed-variant scripts as read (verified) while 2.9 OQ-01 tags all E3i cells UNVERIFIED (X-034)
- V2 G-06 rated Important although its own rubric (V2:1121) makes a fail-open verdict Critical (CL-15, V2 advocate concession)
- V2 uses arXiv 2606.19544 (withdrawn) at V2:1647-1648, 1655, 2044, 2829 (X-036; r25 #26)
- V2 'pr_submit 50 test files' vs 47 (r25 #6); '(6)' occurrences vs 5 lines/7 (X-017)

Note on IC: the denominator is the number of lines that carry a file:line citation (a proxy for scorable, falsifiable claims); the numerators are the internal inconsistencies actually established, so IC is high for both and differentiates weakly. Note on SR: the concrete-indicator regex is deliberately broad (numbers with units, file names, hashes, line refs), so SR is near 1.0 for both reports and differentiates weakly.
