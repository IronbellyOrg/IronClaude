# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis

Fault-finder: general-purpose agent, opus class, independent of the advocates; read-only (reads, greps, git status; no test run). Returned 13 findings; evidence shortened by the orchestrator, ids and fields unchanged.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | Adding `--include='*.py'` makes PLAN:125 true as literally written ("lists only `follow_ups.py`") | UNADDRESSED | MEDIUM | `follow_ups.py` need not contain the underscore word `follow_ups` (the module is about `follow-ups.md`); the fixed grep can print nothing, and nothing does not match "lists only"; safer: "lists no file other than `follow_ups.py`"; both sentences of PLAN:125 need the fix |
| INV-002 | guard_conditions | No other grep acceptance line can be broken by bytecode | ADDRESSED | LOW | PLAN:42, 56, 74, 75, 150, 165 grep one named file; PLAN:52 and 97 search the skill folder but no task puts a `.py` there; PLAN:237 is `git diff`; A3 re-read these in round 2 |
| INV-003 | interaction_effects | Task 5's folder-wide grep clashes only with SPEC:485 | ADDRESSED | LOW | spec grep for `.dev/` or `artifacts/` hits lines 72, 73, 485, 952, 1139; only 485 in copied sections; its `artifacts` has no slash |
| INV-004 | collection_boundaries | Every installed reference file has a check that it names no `src/superclaude` path | UNADDRESSED | MEDIUM | Tasks 1-3 have it (PLAN:42, 56, 74); Tasks 4 and 5 do not (PLAN:97 checks only `.dev/` and `artifacts/`); spec sections copied by Task 4 contain `src/superclaude/cli/review/ledger.py` (SPEC:404) and `src/superclaude/commands/issue.md` (SPEC:447); T3 checks only digest and canonical rows (PLAN:223); only PLAN:28 forbids it; a missing check, not a wrong-result blocker |
| INV-005 | count_divergence | Counts 19 = 11+1+2+5, 6,400, 14, 12, "13 lines in 10 files" match the live files | ADDRESSED | LOW | 11 definition-sentence files equal the 11 digest rows; all digest and pointer-only paths exist; 6,400 = 4^4 x 5^2; 14 worked cases (SPEC:283-311); 12 family rows (SPEC:729-751); 13 lines in 10 files (SPEC:828-842) |
| INV-006 | count_divergence | Tasklist Medium is blocking on "7 lines" (PLAN:71, SPEC:742) | UNADDRESSED | LOW | `sc-tasklist-protocol/SKILL.md` has 9 lines with "High or Medium", "Medium (blocking)" or "High and Medium" (1439, 1450, 1531, 1537, 1567, 1571, 1608, 1610, 1614); no acceptance line checks the number |
| INV-007 | state_variables | The plan can run now once C-001 is fixed; the reviewed text is current | UNADDRESSED | LOW | Task 1 halts today by design (README.md:18 empty go cell; stage 0 `stage0-summary-for-owner.md` absent; stage 0 not re-reviewed); plan last changed 17:37, before the cards; a later revision makes PLAN:n citations stale |
| INV-008 | state_variables | Task 16's `git diff --stat HEAD` proves no carrier was edited | UNADDRESSED | LOW | HEAD stays fixed if nothing commits; would show another session's uncommitted carrier edit in the same checkout; cannot fail by itself |
| INV-009 | interaction_effects | Task 2's digest markers and Task 15's T1/T2 match the same marker text without false hits | UNADDRESSED | LOW | the spec names the opening marker in prose (SPEC:193, 722); if `rule.md` or `SKILL.md` quotes it in prose, "exactly one fenced digest" and T2 count only the HTML-comment form; "strict off" undefined |
| INV-010 | interaction_effects | PLAN:125's closed importer list stays true | UNADDRESSED | LOW | stage 2 adds `follow_ups_cmd.py` and `sweep.py` (stage 2 plan lines 27, 44-49); no end point beyond Task 10-13; harmless within stage 1 |
| INV-011 | sufficiency_challenge | The plan's own tests show the new files break no existing check | UNADDRESSED | LOW | `tests/skills/test_review_severity_rule.py:36-51` scans tracked files under `src` and `plugins` for banned wording; Task 16 runs no full suite; risk low (banned phrases only at SPEC:122, 452, 849, 1154, outside copied sections) |
| INV-012 | sufficiency_challenge | After the C-001 fix nothing else between it and Task 16 fails | ADDRESSED | LOW | `make sync-dev`/`verify-sync` (Makefile:115-117, 178); `lint-architecture` checks apply only to `sc-*-protocol` folders; pyyaml is a runtime dependency; `test_review_cli.py:44-48` checks four names; `test_cli_install.py:502`; paths exist; edge cases (`labels none`, installed-only, kind with no list) written into the plan |
| INV-013 | guard_conditions | Only Task 7's module is linted; later modules cannot trip the architecture lint | UNADDRESSED | LOW | lint check 11 (Makefile:466-470, `arch_lint.py:9-16`) flags a reassigned contract name such as `THRESHOLDS` under `src/superclaude/cli/`; Task 9 "Thresholds live only in the JSON file" invites a constant; `make lint` is an acceptance line only in Task 7 |

## Summary

- **Total findings**: 13
- **ADDRESSED**: 4 (INV-002, INV-003, INV-005, INV-012)
- **UNADDRESSED**: 9
  - HIGH: 0
  - MEDIUM: 2 (INV-001, INV-004)
  - LOW: 7
- Gate result: no HIGH UNADDRESSED item, so the invariant probe gate does not block convergence; the two MEDIUM items are warnings carried into the merged card (INV-001 sharpens the C-001 fix wording; INV-004 is a missing check, non-blocking).
