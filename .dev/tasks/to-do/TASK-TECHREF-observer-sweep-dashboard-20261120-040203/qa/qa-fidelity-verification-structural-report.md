# QA Report: Fidelity Verification (structural), Gate 4 fixes

**Status:** Complete
**Phase:** fix-cycle (fidelity verification, structural, report-only, fix_authorization false)
**Date:** 2026-11-20
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md
**Previous findings:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/qa/qa-fidelity-consolidated-findings.md (`|F_1|` = 8)

## Baseline
- `wc -l` of the document at start of verification: 1399 (limit 1,400).

## Per-finding verification (regression check first: none of the 8 findings regressed; all re-read against the document and the source myself)

| ID | Result | Evidence (document line / source) |
|---|---|---|
| GF4-1 | RESOLVED | Document 446 and 1246 now say rows with an identity are never deleted for absence; identity-unknown rows are dropped on a complete cycle, kept only across a PARTIAL cycle. Source `observe/parse.py:723-728` (`if row.identity_unknown and not coverage.partial: continue`). The "only grows" claim is narrowed to identified rows in 446, 1246. |
| GF4-2 | RESOLVED | Document 455 lists the six dropped counters and the four exported `collection` keys `state`, `collected`, `changedDuringRead`, `duplicatesIgnored`. Source `observe/export.py:209-215`; mapping `view.py:687-692` (`changedDuringRead` = `coverage.total_changed`, `duplicatesIgnored` = `coverage.duplicates`); `Coverage` fields at `parse.py:180-193`. |
| GF4-3 | RESOLVED | Document 692 gives the 12 top-level keys (counted: schema_version, observed_at, collected, scope, window, orca_available, sources, rows, worktrees, waiting, summary, report_path) and the shapes of `collected`, `scope`, `sources[]`, `rows[]` with `safe_to_close`, `worktrees[]` with `packages[]`, `waiting`. Every key matches `sweep/report.py:613-695`. |
| GF4-4 | RESOLVED | Document 686 and the 14.1 row at 1229. Source: `sweep/probes.py:89` (`WORKER_LIST_PAGE = 100`), `:1150` (one call per Run), `:1157-1161` (`raw_count >= WORKER_LIST_PAGE or more` sets `truncated`); `report.py:32, 209-210` (`PAGE_LINE`), `:528-531` (bullet); `classify.py:72, 701-702` (note `origin unknown: worker list truncated`), `:764-777` (`g.origin` returns `None`, so `person_started` stays unknown instead of True). Wording is precise and does not copy the finding's word "blocked". |
| GF4-5 | RESOLVED | Document 1071 now gives both messages, `cannot link report: <exc>` (`sweep/commands.py:191-194`) and `report name space exhausted: <dir>` (`:197-201`; `tests/sweep/test_cli_contract.py:1414`). |
| GF4-6 | RESOLVED (relabel supported, see below) | D-1 / C8-9 is KNOWN LIMIT (cited) in every place; C8-8 (Needs-you) stays DEFECT-CANDIDATE with full wording. |
| GF4-7 | RESOLVED | Document 553 and 873: "refs #606 ... #606 was closed separately on 2026-11-20T00:20:54Z". `gh pr view 673` body reads "refs #606"; `gh issue view 606` gives closedAt 2026-11-20T00:20:54Z. |
| GF4-8 | RESOLVED | Document 875-879 adds one-line rule texts for S1-S11 and R1-R11, with source file:line. I read PKG README.md:31, 37, 39, 40; DESIGN-CONTRACT.md:11; data-dictionary.md:27, 28, 34, 39, 40, 46, 50; PLAN.md:38, 57, 66, 67; integration-gaps.md:24; fixtures.py:47; MR lines 74, 75, 77, 84, 86, 88-93, 98-101, 105-107, 1104-1119; MV 16-24. The texts match. The statement that S1-S11 are not numbers in any source file holds (grep for S1/S11/R11 in the package .md files: 0 hits). |

## GF4-6 / D-1 relabel: consistency and support (extra check requested by the executor)

- **Support in the record.** `git show origin/master:.dev/issues/409/ponytail-review-20261116/cuts-debate/final-cut-list.md` line 24 is row R1: CUT-SMALLER, EXECUTE-NOW, confidence 80; scope includes "collector.py `question_fixture` argument, state and replay (:97, :102-104, :134-140); keep `read_questions` as a 2-line stub returning FAILED `no-question-fixture`"; surviving guard "`--fixture` with `--questions` refused: commands.py:177-178". Line 62 is row D13 (mark T7 "not built / no automated test"). Line 16 confirms EXECUTE-NOW = 11. `execute-now-brief.md` Step 1 repeats the R1 text. `runtime-code.md:51` says "production can never reach it". `acceptance-tests.md:25` on origin/master carries the D13 wording. PR #577 (MERGED 2026-11-17T00:40:16Z) body: "applies the 11 debated cuts"; the issue 409 comment of 2026-11-17T07:09:29Z says "applied the 11 agreed cuts". Code: `observe/collector.py:125-129` is the stub; `commands.py:77-78, 183-188` refuse the combination and `:414` calls `_question_refusal`; `tests/observe/test_collector.py:675` is the only test hit. Every citation in 556 and 1329 checked out.
- **Qualifies under R-C8 step 1 (judgment, not a defect).** The record is a design-package decision text for this specific capability that says the build will not deliver it, and a merged PR applied it. The document states the residual honestly (a review-panel debate output, not a dated owner ruling; no "until" owner) and keeps the owner question and the "Remediation task not created ... flagged for the owner" sentence. C8-1 uses the same kind of record ("review inputs, not a dated owner ruling") and is also KNOWN LIMIT, so the treatment is consistent.
- **Consistency.** grep over the document for `D-1|C8-9|DC-0[12]|DEFECT-CANDIDATE`: no `DC-01` or `DC-02` remains. D-1 / C8-9 appear at 246, 346, 375, 549, 556, 1232, 1329, 1387, 1397 and each is KNOWN LIMIT (cited) or label-neutral. DEFECT-CANDIDATE appears at 260 (generic), 555, 918, 1235 (C8-8), 1308/1310/1313/1315 (rule), 1328 (C8-8), 1329 (relabel note and residual), 1345, 1373 (glossary) and 1397: all consistent. The only count is at 1345: "2 DEFECT-CANDIDATE as registered (Gate 4 relabelled D-1 / C8-9 ... so one DEFECT-CANDIDATE, C8-8, stands)"; 40+5+35+2+52 = 134 matches the register total. No "two DEFECT-CANDIDATE" text remains elsewhere.
- **Length.** `wc -l` = 1399, at most 1,400.

## New defects introduced by the fixes (adversarial pass)

No blocking defect found. Protected parts are present (2.5 at 242, 8.1 at 945, 13.1 at 1166, 14.4 at 1264; C8-8 row with full wording at 1235 and 1328). No unification recommendation was added (lines 53, 56, 1381 say none is made). The Table of Contents (136-155) lists the 16 sections plus Appendix A and Document History, and the `##` headings at 161-1393 match it. Section 15.1 and the Document History row were extended consistently.

## Minor findings (notes only, not blocking, not to be rechecked)

1. Document 877 cites `README.md:32` for S6 and S10 (filter scope; hold/pause). Line 32 of the package README is blank; the text is on line 33 (`grep -n`: "Open `gallery" and "Changing a fixture" at 33). A moved line number on a true claim.
2. The register `gaps-and-questions.md` still labels the item DC-02 as DEFECT-CANDIDATE (4 hits for DC-01/DC-02). The document says "as registered" at 1345 and explains the relabel, so the difference is disclosed.
3. D-1's KNOWN LIMIT status rests on a judgment that a debated cut list applied by a merged PR is a scope decision; the document names the alternative reading in the row. No fact depends on it.

## Result

- Open blocking findings: `|F_2|` = 0 versus `|F_1|` = 8. No regression (nothing that was fine at review 1 now fails).
- Structural integrity: 16 sections, ToC accurate, 1399 lines (Standard budget 800-1,200 is exceeded by design, with the 1,400 Gate 3 threshold respected).

**Confidence:** Verified: 8/8 findings plus 4 extra checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 14 | Grep: 11 | Glob: 0 | Bash: 6 (all read-only; `gh` calls use `--repo IronbellyOrg/IronClaude`). No web research performed.

## Verdict: PASS (with 3 minor notes)
