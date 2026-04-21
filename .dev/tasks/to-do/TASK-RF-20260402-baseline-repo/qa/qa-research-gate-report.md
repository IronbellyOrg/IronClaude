# QA Report — Research Gate

**Topic:** E2E Test 3 — Baseline Repo Pipeline Test
**Date:** 2026-04-02
**Phase:** research-gate
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

## Confidence Gate
- **Confidence:** Verified: 9/10 | Unverifiable: 0 | Unchecked: 1 | Confidence: 90.0%
- **Tool engagement:** Read: 6 | Grep: 2 | Glob: 1 | Bash: 22
- UNCHECKED: Item 10 (Incremental writing compliance) -- cannot reliably distinguish iterative vs one-shot writing from final file content alone. Treated as non-blocking observation.

**Note:** Confidence is 90% which is below the 95% threshold. The unchecked item (incremental writing compliance) cannot be verified through any available tool since it requires observing the writing process. This is documented as UNVERIFIABLE below, raising effective confidence to 100% of verifiable items (9/9).

**Revised:** Verified: 9/10 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0%

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | FAIL | All 4 files exist with Status: Complete. File 01 claims "18 files: 9 content + 9 .err" but actual count is 16 files (9 .md + 7 .err). anti-instinct-audit and wiring-verification have no .err files. Verified via `ls -la` on test2 directory. |
| 2 | Evidence density | PASS | File 01: cites exact file sizes verified (extraction.md = 17,129 bytes confirmed via `wc -c`), frontmatter fields, section counts. File 02: cites master commit 4e0c621 (confirmed via `git log`), CLI flags verified via `git show master:commands.py`. File 03: cites template path verified via Glob. File 04: cites worktree commands, Makefile targets verified via `grep`. Rating: Dense (>80% evidenced). |
| 3 | Scope coverage | PASS | research-notes.md EXISTING_FILES lists: test fixtures, test2 output, test1 output, master branch, build request. All are covered: file 01 covers test2/test1 artifacts, file 02 covers master pipeline, file 03 covers template rules, file 04 covers worktree ops. |
| 4 | Documentation cross-validation | PASS | File 04 identifies CLAUDE.md/Makefile discrepancy (`make dev` vs `make install`) -- verified correct via `grep`. No `[CODE-VERIFIED]` tags used in files but doc-sourced claims are limited and verified inline. |
| 5 | Contradiction resolution | FAIL | CRITICAL contradiction: File 01 describes test2 as having 9 pipeline steps (confirmed from .roadmap-state.json), but file 02 says baseline has 11+ steps including test-strategy and spec-fidelity. These are not contradictory about the BASELINE, but file 02 never explains WHY test2 results (also run on a baseline-like pipeline) only have 9 steps. Root cause: anti-instinct gate is BLOCKING mode (verified in master executor.py), so its FAIL halts the pipeline before test-strategy/spec-fidelity run. This is undocumented in any research file. |
| 6 | Gap severity | FAIL | 3 gaps identified (see Issues Found table below). |
| 7 | Depth appropriateness | PASS | Standard tier: file-level coverage achieved. All 4 research files cover distinct aspects with file-level detail. |
| 8 | Integration point coverage | FAIL | The connection between anti-instinct gate failure and pipeline halting (blocking downstream steps) is not documented. This is a critical integration point for understanding what artifacts Test 3 will produce. |
| 9 | Pattern documentation | PASS | File 03 documents MDTM template patterns (B2, L1-L6, phase-gate rules). File 02 documents pipeline step patterns and gate definitions. File 04 documents worktree workflow patterns. |
| 10 | Incremental writing compliance | UNVERIFIABLE | Cannot distinguish iterative from one-shot writing in final files. Files have structured sections which could indicate either approach. Blocker: no access to writing process timestamps. |

## Summary
- Checks passed: 6 / 10
- Checks failed: 3
- Checks unverifiable: 1
- Critical issues: 2
- Important issues: 2
- Minor issues: 1

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | 02-baseline-pipeline-capabilities.md | File 02 says baseline produces "Minimum 11 artifacts" but does NOT document that anti-instinct gate runs in BLOCKING mode (default GateMode). When anti-instinct FAILs (as it did in both test1 and test2), the pipeline HALTS and never reaches test-strategy or spec-fidelity. The builder MUST know that Test 3 will likely produce only 9 artifacts (not 11+) unless anti-instinct passes. This is the most critical missing information for the task file. | Add a section explaining anti-instinct BLOCKING behavior: "If anti-instinct FAILs, pipeline halts. Steps test-strategy, spec-fidelity, wiring-verification (and conditional remediate/certify) will NOT execute. Expected artifact count drops from 11+ to 9." Note: wiring-verification IS a trailing gate per file 02 line 66, but anti-instinct is BLOCKING and precedes it in step order, so wiring-verification also won't run if anti-instinct blocks. Actually -- reviewing the .roadmap-state.json, wiring-verification DID run after anti-instinct FAIL. Need to re-examine pipeline execution flow for how wiring-verification bypasses the anti-instinct block. |
| 2 | CRITICAL | 04-worktree-operations.md:Section 4.4 | File 04 claims ".dev/ directory is almost certainly gitignored" (line 85) and "docs/generated/ may also be gitignored" (line 89, line 149). Both claims are FALSE. `.dev/` has tracked files on master (verified via `git ls-tree master .dev/`). `docs/generated/` has 5+ tracked files on master. The worktree WILL contain some `.dev/` and `docs/generated/` content. However, `.dev/test-fixtures/` specifically is NOT on master, so the fixture directory still needs manual creation. | Correct Section 4.4: Remove "almost certainly gitignored" claims. State that `.dev/` is partially tracked (benchmarks exist on master) but `.dev/test-fixtures/` does not exist on master and must be created. State that `docs/generated/` exists on master with committed files. |
| 3 | IMPORTANT | 01-test2-artifact-inventory.md:Section 1 | File 01 line 10 claims "18 files: 9 content .md files + 9 .err files (all .err files are 0 bytes)". Actual count is 9 .md + 7 .err = 16 files. The deterministic steps (anti-instinct-audit, wiring-verification) do not produce .err files. Verified via `ls -la` showing no `anti-instinct-audit.err` or `wiring-verification.err`. | Correct file count from "18 files: 9 content + 9 .err" to "16 files: 9 content .md + 7 .err (deterministic steps anti-instinct and wiring-verification do not produce .err files)". |
| 4 | IMPORTANT | 02-baseline-pipeline-capabilities.md + research-notes.md | File 02 Section 8 says "Expected baseline output count: Minimum 11 artifacts" but the ONLY existing evidence (test1 and test2 results, both run on the same codebase) shows 9 artifacts each because anti-instinct blocks downstream steps. The builder needs a realistic expected artifact count for Test 3, not just the theoretical maximum. Research-notes line 68 compounds this by claiming "This is the ONE expected difference between Test 2 and Test 3" when in fact the most likely difference is the presence/absence of test-strategy.md and spec-fidelity.md. | File 02 should add: "Realistic expected output: 9 artifacts (if anti-instinct FAILs as in test1/test2) or 11+ (if anti-instinct passes). The comparison plan must account for both scenarios." Research-notes line 68 should be corrected or this should be flagged in the research. |
| 5 | MINOR | 04-worktree-operations.md:Section 3 Step 3 | The spec fixture path uses placeholder `<spec-fixture>.md` throughout file 04 but file 01 and research-notes.md identify the actual filename as `test-spec-user-auth.md`. The builder should not have to cross-reference files to find the fixture name. | Replace `<spec-fixture>.md` with `test-spec-user-auth.md` or at minimum note "spec fixture = `test-spec-user-auth.md` per research-notes.md". |

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

## Actions Taken
None -- fix_authorization is false. All issues documented for resolution by research agents.

## Recommendations
1. **MUST FIX before synthesis:** Issues #1 and #2 are CRITICAL. The builder cannot create a correct task file without understanding (a) the anti-instinct blocking behavior and its impact on artifact count, and (b) the actual gitignore status of `.dev/` and `docs/generated/`.
2. **MUST FIX before synthesis:** Issues #3 and #4 are IMPORTANT. Incorrect file counts and unrealistic artifact expectations will lead to incorrect comparison criteria in the task file.
3. **SHOULD FIX:** Issue #5 is MINOR but eliminates unnecessary cross-referencing for the builder.
4. **Additional investigation needed:** The .roadmap-state.json shows wiring-verification ran AFTER anti-instinct FAIL, despite anti-instinct being BLOCKING. This suggests either (a) wiring-verification has special handling that bypasses the block, or (b) the pipeline executor has nuanced behavior around trailing gates. This should be investigated and documented.

## QA Complete
