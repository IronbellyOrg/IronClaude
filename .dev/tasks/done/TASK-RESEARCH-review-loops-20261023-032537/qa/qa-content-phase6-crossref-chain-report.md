# QA Report: Phase 6 Gate, Cross-Reference Chains

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks
**Date:** 2026-10-24
**Phase:** phase-gate (Task Phase 6), report-only, content lens
**Lens:** Cross-reference chain integrity
**Fix cycle:** N/A
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Report identity checked:** `R/RESEARCH-REPORT-review-loops.md`, 1,316 lines, sha256 `41145b5e9660967e6f6498efb90da18bbfcd51eb3a81a0850fbdcde29fca40a0` (matches the dispatch)
**Known defects not counted:** J1, L1, L2 and L3 (user-accepted). The ranks and the non-consensus order V1 > V3 > V2 > V5 > V4 were not challenged.
**Restrictions observed:** no Git command, no session `.jsonl` log opened, no file edited.

---

## Overall Verdict: FAIL

Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Case evidence to hypothesis card | PASS | Read the supporting-incident tables of all five cards (`hypothesis-01.md:48-62`, `-02.md:48-63`, `-03.md:55-60`, `-04.md:51-66`, `-05.md:50-64`). Their case-section pointers (for example 01 §3.1-3.3, 05 §5.2-5.4, 06 §4-5, 03 §2-5) resolve to the matching headings in the six case files. The card anchors match Option A-E Support: records 291, 585/804/906/1021, 544-545/841, 759-762/1240, 332-435, 188-234, 383-668 and 413-527. |
| 2 | Card to debate outcome | PASS | Printed about 50 cited lines of `ADV/debate-transcript.md`. All of these resolve to the stated advocate and content: Round 1 :128, :129, :167, :168, :208, :243; Round 2 :256-258, :264-265, :277, :294-304, :316, :333-344, :356, :378-385, :397, :414-426, :438; convergence and order :449-453, :468-484. "All five nominated C-004/C-003/C-002/C-007/C-005" matches the scoring matrix at :460-465. |
| 3 | Debate outcome to Section 6 Debate record rows and Options Comparison | PASS | The final positions "1/1/1/1/1, 2/2/3/3/3, 3/3/2/2/2, 4/4/4/5/5, 5/5/5/4/4" (Report:654) match the orders at :480-484. Each For/Against citation in Options A-E resolves to the correct advocate. |
| 4 | Section 6 to Section 7 rank and tallies | PASS | Section 7.1 holders and Section 7.2 pair tallies agree with :480-486. These also resolve: `merged-root-cause-analysis.md:21,37,43,64,155-165,170,205`, `return-contract.md:14,16,24,26`, `base-selection.md:5,150-155,170-171`, `invariant-probe.md:18-20,39-44,51-54,72`, `refactor-plan.md:9,32,33`, `plan-review-evidence.md:16` and `diff-analysis.md:33,64,69`. |
| 5 | Section 7 rank to Section 7.6 orders to Section 8 steps | FAIL | The order-to-step mapping and the reach pointer are inexact (C-04, C-05). The rest resolves: Options Comparison Integration-complexity cells to orders 1-2; the replay table "Used by" column; step 2.6 to order 4 and Question 1. |
| 6 | Section 4 gaps to Section 8 checks or Section 9 questions | PASS | Walked all 12 gap rows against the 10.10 table (Report:1270-1283). Each named Section 8 row exists (steps 2.1-2.6, 3.2-3.6) and each cited question number carries matching content. |
| 7 | Gap register to report gap rows to questions | FAIL | Read all 69 lines of `R/gaps-and-questions.md`. The third Orca contradiction is missing and the register's state text is stale (C-01, C-08). |
| 8 | Intra-report references ("Section X.Y", "Question N", "order N", "header Scope line", "Option C Scope row", task log entries) | FAIL | About 90 references resolve. Every cited task log entry exists (03:41Z, 03:45Z, 03:52Z, 05:24Z, 05:35Z, 06:32Z, 07:09Z). One pointer resolves to the wrong content (C-04). |
| 9 | Each citation points to supporting text, not just an ID | FAIL | Printed about 60 evidence-deck lines, scope-rules :28-96, about 90 case-report lines, about 40 QA and gate-record lines, the BUILD-REQUEST quotes at :12 and :34, and task file :68 and :253-259. One citation is attached to the wrong claim (C-06). |
| 10 | No fictitious file links | PASS | Expanded and stat-checked 335 backticked paths. Three do not resolve, and all three are expected: the worktree that Report:617 says no longer exists, the original CI plan (L3, known), and the `variant-1..5` shorthand at :1092. Every `ADV/` name exists. External artifacts exist at the cited lines: `t12-review-1.md:20-35`, `t12-review-2.md:20-28`, the second CI review `REPORT.md:21`, `merged-verdict.yaml:154`, `round2-v1.md:5,16,33`, the Orca `merged-verdict.yaml:39-47,57,75,120-128`, `coverage-matrix.yaml:1749-1757`, and the Q7 ledger `progress.md:1,21,22`. |
| 11 | Synthesis components agree with the report | FAIL | Compared report Sections 1-10.8 line by line with synth-01..06: 30, 7, 9, 46, 31 and 7 report lines are absent from the respective components. synth-04 contradicts report Section 7.6 (C-02). |
| 12 | Evidence trail covers the cited sources | FAIL | 13 cited package files are not in Section 10. The 10.9 hash note is incomplete (C-03, C-07). Measured: `ls qa \| wc -l` = 266; `find . -type f \| wc -l` = 341. |
| 13 | Controls and conditions survive along the chain | PASS | The screened controls in the 7.7 placement table (Report:785-790) appear in the Opposition rows of A, B, E and D as stated. Deck anchors :650-655 match. The confounding (Option C/D) and the timing-only shared-install caveat stay attached in 6, 7.4 and Q4. |

## Summary

- Checks passed: 7 / 13
- Checks failed: 6
- Critical issues: 0
- Important issues: 3 (C-01, C-02, C-03)
- Minor issues: 5 (C-04 to C-08)
- Issues fixed in-place: 0 (report-only)

The main chain holds end to end: case evidence, then card, then debate, then options, then rank, then proposed checks, then open questions. The breaks are at the edges. The gap register (C-01) and synth-04 (C-02) no longer agree with the report. The Section 10 evidence trail stopped tracking the Phase 6 records the report itself cites (C-03).

## Issues Found

| ID | Severity | Location path:line | Issue | Evidence | Required fix |
|---|---|---|---|---|---|
| C-01 | IMPORTANT | `R/gaps-and-questions.md:29-35,59,65-69`; `R/RESEARCH-REPORT-review-loops.md:259,348,408,904,953,969,1292` | The chain from gap register to report to questions breaks for the third Orca source tension: following the annotated tag's upstream `object.url` versus checking upstream values before use. The report treats it as an unresolved contradiction in five places (2.5 marker row, Section 4 row 3, 5.1, Section 8 Constraints, Question 6). Question 6's sources cite `gaps-and-questions.md:29-59`. The register has no marker for this tension and says the opposite. 10.10 (Report:1292) reports "None unresolved" for contradictions between components. | Register :33 and :35 hold the only two Orca `[CONTRADICTION: ...]` markers. Register :59 says "The two searchable source contradictions above remain reported historical tensions". The only fidelity addition (:65-69) is the CI 16/2 contradiction. Report:953 and :1292 say three Orca tensions. The tension's actual sources are `research/01-session-ac2cd1fd.md:259,298` and `research/evidence-deck.md:452`. | Append a `[CONTRADICTION: ...]` entry for the annotated-tag tension at the end of `gaps-and-questions.md`, so existing line citations keep their numbers, citing those sources. Qualify :59 ("two" becomes three, or add a note). Alternatively, state in Question 6 and 10.10 that the register still lists two and the third comes from the case report and the deck. |
| C-02 | IMPORTANT | `R/synthesis/synth-04-options-recommendation.md:225,267,289,291,294`; `R/RESEARCH-REPORT-review-loops.md:696,738,760,762,765,583` | synth-04, a gate deliverable and the Sections 6-7 source component (10.9), contradicts the report on the rank-to-check link, and has no in-file note that the report supersedes it. (1) Order 1 decision rule: synth-04:289 says "If the checks actually used already rejected the counterexamples, V1 loses its lead". Report:760 says "The check alone cannot reorder the ranking". (2) Order 3 scope: synth-04:291 says "Option D and E checks on their two incidents each". Report:762 says "Option D on its one incident and two controls (three contexts in two sessions)". (3) Execution status: synth-04:294 says steps 1-3 "stay read-only". Report:765 says steps 1-2 "require separately approved execution in a disposable copy". (4) synth-04:225 still says the five orders are repeated at `return-contract.md:24`, which repeats only the displayed order (Report:696; `return-contract.md:24` read). (5) synth-04 has no trace of the shared 2026-10-22T20:29:54Z install (grep: 0 hits), which the report uses to qualify V3's reach (Report:583, 738). | Line-by-line comparison: 46 lines of report Sections 6-7 are absent from synth-04. Report 10.10 (:1293) discloses that the other corrections "exist only in this report". That disclosure is in the report, not in synth-04, and the synth-04 header (:1-8) carries no supersession pointer. | Mirror report 7.2's source sentence, the 7.4 shared-clusters row, the 7.6 table and the trade-off paragraph (and the Option C Scope dependency) into synth-04. Alternatively, add a header line in synth-04 stating that report Sections 6-7 supersede it from Task Step 6.18 onward, and naming the differing items. |
| C-03 | IMPORTANT | `R/RESEARCH-REPORT-review-loops.md:1167-1182,1208-1249,1291`; cited at :5, :8, :857, :1262, :1293 | The Section 10 evidence trail does not list Phase 6 records that the report cites as sources. 10.10 still records "Evidence trail lists every package file: Pass ... `qa/` (207)". This is distinct from J1: J1 covers the cycle-2 "pending" status lines at :5, :1241 and the 10.10 assembly-changes row, not this inventory row. | Programmatic diff of cited package paths against the Section 10 listings found 13 cited files absent: `qa/qa-consolidated-findings-phase6.md`, `qa/qa-fix-log.md`, `qa/qa-fix-log-cycle2.md`, `qa/qa-lens-internal-consistency.md`, `qa/qa-lens-crossref-chain.md`, `qa/qa-lens-domain-accuracy.md`, `qa/qa-fix-verification.md`, `qa/qa-fix-verification-qualitative.md`, `qa/qa-lens-implementation-concreteness.md`, `qa/qa-fidelity-fix-log.md`, `qa/qa-fidelity-fix-log-cycle2.md`, `qa/qa-anti-omission-fix-log.md`, `qa/qa-anti-omission-fix-log-cycle2.md`. `phase-outputs/plans/report-gate-decision.md` is cited at :5, :8, :1241 and :1293 but is not a row in 10.7. Counts now: `qa/` = 266, package = 341, against 207 and 277 in 10.9. | Add an inventory subsection (for example 10.12) listing the Phase 6 lens, consolidation, fix, verification, fidelity and anti-omission records and the three later gate decisions, with date and provenance class. Relabel Report:1291 as the 03:51:27Z assembly-time check that later files supersede. |
| C-04 | MINOR | `R/RESEARCH-REPORT-review-loops.md:762` versus `:709` | Order 3 says the D and E checks cannot change the bottom placement "because that dispute is also about reach (Section 7.2)". Section 7.2 does not say this. It says the displayed V5-above-V4 step was adopted "under A-001's second criterion", the direct-continuation evidence. The reach basis is in 7.1 rows 4-5 (:683-684) and in the debate at :265, :384 and :426. | Report:709; Report:683-684; `debate-transcript.md:265,384,426` read. | Repoint to "Section 7.1 rows 4-5 and the Option D/E Debate records". Or state in 7.2 that the bottom dispute weighs comparable narrow reach against direct continuation evidence. |
| C-05 | MINOR | `R/RESEARCH-REPORT-review-loops.md:756` versus `:761,852` | The 7.6 lead-in maps "order 2 uses steps 2.2-2.3". But order 2's credential transitions apply "Option D's proof-state reconstruction", which is the content of step 2.4 (:878). The replay table assigns the credential artifacts to steps 2.3 and 2.4 (:852). | Report:761 and :878 read. | Change to "order 2 uses steps 2.2-2.3, with step 2.4's proof-state reconstruction for the credential transitions". |
| C-06 | MINOR | `R/RESEARCH-REPORT-review-loops.md:554` (Option B Opposition) | The parenthetical after "Two of CI's four 'new medium' findings were later downgraded" cites `research/evidence-deck.md:626,657`. Those deck rows are monitor rows about file-backed JSON output and output limits. They support the earlier monitor sentence, not the CI downgrade. | Deck :626 ("File-backed monitor JSON caused oversized output") and :657 ("Monitor output limits") read. The CI downgrade is supported by `research/04-session-43582de1.md:16`. | Move `:626,657` to follow "the size repair exposed later limits rather than creating them", and keep `04-session ... section 1` on the CI sentence. |
| C-07 | MINOR | `R/RESEARCH-REPORT-review-loops.md:1262` | The 10.9 note naming later changes to the assembly-hashed components lists only synth-01, -04 and -05 (Step 6.18) and synth-01, -02 and -04 (Steps 6.29/6.32). All six component hashes now differ from the 10.9 identities, including synth-03 and synth-06. Those changes are recorded only in 10.10's last row. | `sha256sum`: synth-03 `b0a561a5…` (10.9 lists `ca519125…`), synth-06 `bdf94b0d…` (10.9 lists `bcffe37a…`). Report:1293 names Steps 6.39 and 6.42 changes to synth-01..06. | Add "and the Task Step 6.39 and 6.42 anti-omission corrections changed synth-01 through synth-06 (10.10, last row)", or replace the partial list with a pointer to 10.10. |
| C-08 | MINOR | `R/gaps-and-questions.md:11,63` | The register's state column and summary still say "Final synthesis/ranking QA remains pending" and "synthesis/ranking and final-report gates remain pending". The report it feeds delivers the ranking (Report:668, 676-684), and its header records the later report-gate history. The register is cited as a Section 9 source (Report:969). | Register :11 and :63 read. | Add a dated status note to the register recording the Phase 5 user-authorized advance and the Phase 6 gate outcomes, without rewriting the historical rows. |

## Actions Taken

None. Report-only run (`fix_authorization: false`): no file was edited, no Git command was run, and no session log was opened.

## Confidence Gate

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 12 | Grep: 0 (content searches ran as read-only `grep` and `sed` inside Bash) | Glob: 0 | Bash: 38 (read-only `sed`, `grep`, `wc`, `ls`, `stat`-free `ls -la`, `sha256sum`, `find`, and three `uv run --no-project python` read-only comparison scripts that wrote no file)
- Unchecked items: none.
- Unverifiable items: none. Current-rule `git show` claims were not re-run because of the no-Git rule. They belong to the domain lens and were not used for any chain verdict here.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check.**
- No `## Inherited Structural Verdict` block was supplied. Nothing was relied on. Structure was re-checked only where a chain depended on it (heading existence for every "section N" pointer).

**(b) Independent semantic checks (at least one required, INV-019).**
- Rank to debate merit: matched every Section 6 and 7 debate citation to its advocate's actual Round 1 or Round 2 text (`debate-transcript.md` lines listed in item 2). They support the stated For/Against role.
- Gap register to report: read the full register and compared its contradiction markers with Report 2.5 and Question 6. Found C-01.
- Synthesis to report: line-set comparison of six component ranges, then a diff of synth-04 Section 7 against report Section 7. Found C-02.
- Evidence trail to citations: programmatic extraction of cited package paths against the Section 10 listings. Found C-03.
- Citation semantics: read deck :626 and :657 against the Option B sentence. Found C-06.
- External targets: read `t12-review-1.md:20-35`, `t12-review-2.md:20-28`, CI second-review files and the Q7 ledger. All support their claims.

Why the passing chains should be trusted: every debate line, card table, case heading, deck row and gate-record line behind a PASS was printed and compared. The citation list per item is above.

## Recommendations

- Resolve C-01 to C-08 in one serialized correction pass. Keep J1, L1, L2 and L3 untouched. Change no rank or tally.
- After the fix, rerun this lens on the new report hash, together with a structural verifier.

| Status | Result |
|---|---|
| DONE | Traced case evidence, cards, debate, Sections 6-9 and the gap register for the full report (sha256 `41145b5e…`). Found 8 issues: 3 IMPORTANT, 5 MINOR. |
| NEXT | A single fixer resolves C-01 to C-08. Fresh structural and content verifiers then check the fix. |

## QA Complete