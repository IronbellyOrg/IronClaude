# Test 2 — Spec Pipeline Summary

**Fixture:** `.dev/test-fixtures/test-spec-user-auth.md`
**Output:** `.dev/test-fixtures/results/test2-spec-modified/`
**Pipeline exit code:** 1 (halted at anti-instinct)

## Pass/Fail Table

| Artifact | Gate | Check | Result | Notes |
|----------|------|-------|--------|-------|
| extraction.md | EXTRACT_GATE | 13 standard frontmatter fields | PASS | All 13 present with valid values |
| extraction.md | — | 6 TDD fields absent | PASS | 0/6 TDD fields found — no content leak |
| extraction.md | — | 8 standard body sections | PASS | 8/8 found at expected line numbers |
| extraction.md | — | 6 TDD body sections absent | PASS | 0/6 TDD sections found — no content leak |
| roadmap.md | MERGE_GATE | >= 150 lines | PASS | 494 lines |
| roadmap.md | MERGE_GATE | spec_source, complexity_score, adversarial | PASS | All 3 present |
| roadmap.md | — | auth content present | PASS | FR-AUTH.1-5, JWT, bcrypt, middleware |
| anti-instinct-audit.md | ANTI_INSTINCT_GATE | fingerprint_coverage >= 0.7 | PASS | 0.72 (13/18) |
| anti-instinct-audit.md | ANTI_INSTINCT_GATE | undischarged_obligations == 0 | PASS | 0 |
| anti-instinct-audit.md | ANTI_INSTINCT_GATE | uncovered_contracts == 0 | FAIL | 3 uncovered (middleware_chain) |
| spec-fidelity.md | SPEC_FIDELITY_GATE | high_severity_count == 0 | SKIPPED | Pipeline halted at anti-instinct |
| spec-fidelity.md | — | TDD dimension cross-contamination | SKIPPED | Pipeline halted at anti-instinct |
| .roadmap-state.json | — | schema_version, agents, depth | PASS | All valid |

**Total: 10 PASS, 1 FAIL, 2 SKIPPED**

## Key Success Criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| No TDD content leaks in extraction | PASS | 0/6 TDD fields, 0/6 TDD sections |
| Standard 8 sections only | PASS | 8 H2 headings, all standard |
| All gates pass | PARTIAL | 8/9 steps pass; anti-instinct fails (pre-existing) |
| Pipeline completes fully | NO | Halted at anti-instinct (EXIT_CODE=1) |
| extraction_mode = standard | PASS | Confirms spec prompt used |

## Critical Findings (from Phase 5 Findings table)

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| 5.1 | Spec pipeline halted at anti-instinct. Semantic check `integration_contracts_covered` failed: uncovered_contracts=3 (middleware_chain refs). 8/11 steps passed. Extraction verified clean. | IMPORTANT | Pre-existing anti-instinct issue — roadmap doesn't generate explicit wiring tasks for all integration contracts. Not caused by TDD changes. |

## Follow-Up Actions

1. **Pre-existing: anti-instinct contract coverage** — The anti-instinct gate's `integration_contracts_covered` check is too strict for generated roadmaps. Both TDD and spec pipelines fail here. Investigate whether the contract detection regex is too broad or whether the merge step should explicitly wire integration contracts.
2. **Spec-fidelity untested** — Because anti-instinct blocks, the spec-fidelity cross-contamination check could not run. This check is important for validating that the generalized fidelity prompt doesn't inject TDD dimensions into spec analysis. Consider a `--skip-gate anti-instinct` flag for test runs.
