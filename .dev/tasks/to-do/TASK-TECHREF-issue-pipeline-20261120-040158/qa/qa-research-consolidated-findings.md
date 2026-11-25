# Gate 1 consolidated findings (cycle 1, review 1)

**Date:** 2026-11-20
**Valid review-1 reports:** 3 of 3 (analyst-completeness-report.md PASS, qa-research-evidence-report.md FAIL, qa-research-depth-report.md FAIL; all `Status: Complete` with a `## Verdict:` line).
**Consolidated verdict:** FAIL
**F_1 (BLOCKING findings) = 5** (0 synthetic)

## BLOCKING findings

| ID | Origin lens | Research file and location | Finding (copied from the originating report) | Evidence | Required fix |
|---|---|---|---|---|---|
| B-1 | evidence-quality | research/01-watcher-decision-engine.md, section 1 Key Takeaways (line ~34) | Claim "13 constants at lines 34-47; 12 are read, MAX_LAUNCHES_PER_CYCLE is dead" is wrong. | cycle.py:34-47 is 14 assignments; the file's own section 1 table has 14 rows; 13 are read (HEALTH_AGE_S at cycle.py:1327 and STALE_AGE_S at 1259 only by the status report) and 1 is dead | State: 14 constants at lines 34-47; 13 are read (two of them, HEALTH_AGE_S and STALE_AGE_S, only by the status report); MAX_LAUNCHES_PER_CYCLE is dead (cycle.py:35 only) |
| B-2 | evidence-quality | research/04-claim-flow-and-orca-worktree.md, section 3 table, Lines column, rows issue-worker-t1.md, -t2.md, -t3.md | Each file is claimed to have 36 lines. | `wc -l` of src/superclaude/agents/issue-worker-t1.md, -t2.md, -t3.md = 35 each | Correct all three to 35 |
| B-3 | evidence-quality | research/05-guard-stack-and-ccsession.md, section 11 Key Takeaways (line ~355) | "16 test files plus claim-side pins cover the area" is wrong. | Section 11.1 has 14 rows (one per assigned test file); claim-side pins listed under the table are 3 more files (test_issue_l2_install.py, test_issue_orca_worktree.py, test_require_orca_worktree_agent_governed.py) | State: 14 test files in the table plus 3 claim-side pin files |
| F-1 | research-depth | research/03-watcher-operator-surface-and-setup.md (four places) | One tag is false: the design-doc row for the clock-skew value (issue-watcher.md line 827) is not tagged [CODE-VERIFIED] consistently with file 01 and the code (SKEW_WARN_S = 60; issue-watcher.md:827 says 300 s) | predicates.py:17, 289-295; cycle.py:44, 774; issue-watcher.md:494, 509-510, 827; issue-watcher-setup.md:651. See qa-research-depth-report.md F-1 for the four locations | Correct the tag/wording of the DES:827 row in the four places so file 03 matches file 01 and the code |
| F-2 | research-depth | research/04-claim-flow-and-orca-worktree.md test-pin table | Missing test-pin rows for tests/skills/test_clickup_claim.py and tests/skills/test_model_alias_policy.py (pinning files that exist and pin pipeline behaviour) | See qa-research-depth-report.md F-2 | Add test-pin rows (path, lines, test count, what it pins) for both files |

## MINOR findings (notes; no gap-fill item; carried to synthesis as notes)
- Evidence report M-3: research 04 section 8.7: the import of SCRIPT at line 281 is in tests/hooks/test_launch_level_guard_worker.py, not tests/skills/test_issue_orca_worktree.py.
- Evidence report M-4: research-notes.md figures: modules sum to 4,795 lines (not 4,389); REASON_TABLE is audit.py:26-102; templates are 15 files (not 17). Synthesis agents take figures from the research files, not the notes.
- Evidence report M-5: do not carry rows that rest only on docs/designs/orchestrator.md (the out-of-scope rewrite design) into synthesis; any "recorded decision" column citing only that file is reworded to "no decision found in the files this reference cites".
- Depth report M-1..M-6 (removal-commit numbers and UTC date "2026-11-19 18:02 -0600 (2026-11-20 UTC), PR #682"; use 4,795 or no total; add require-orca-worktree-agent.sh row; cite the hand count for 59).
- Analyst report F-01..F-12 (12 MINOR): removal date wording; negative-search wording ("not found in snapshot" only for COORD-, dispatcher, zero-setup watcher); several sections end without Key Takeaways; R05 "16 test files" (duplicate of B-3); setup-doc "at most 37" sentence should be tagged [CODE-VERIFIED] per R01/R02.

## Gap-fill items registered
5 items (3.5.1 to 3.5.5), one per BLOCKING finding.
