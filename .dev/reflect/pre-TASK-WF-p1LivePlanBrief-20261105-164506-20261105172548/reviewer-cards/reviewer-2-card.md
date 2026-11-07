# Reviewer 2 card (qa, haiku class label) - 7 deviations (Regression 0, Drift 2, Necessary 4, Authorized 1)

| # | Class | Location | Finding | Evidence | Sev |
|---|---|---|---|---|---|
| 1 | Necessary | plan:52, :552, :556-566 | grant file replaced by a Constraints bullet; justified by owner decision G1 (APPROVED.md:66-71) | source.md:79 | LOW |
| 2 | Necessary | plan:554 | Task 24 child created first, synced, no --setup; justified by spec 7.2 step 1 and WORKER-CONTRACT.md:174 | source.md:79; p0-live-orca-help.txt:49,69 | LOW |
| 3 | Necessary | plan:19, :58 | tip recorded, ancestor check instead of literal pin; justified | source.md:30 | LOW |
| 4 | Necessary | plan:41, :447-467 (Task 19, lc18) | keeps step 3's pass rule and does not require "step 6 shows nothing written"; the brief's phase header at source.md:70 contradicts lc18's own row (a contract is written) | source.md:70, :72; spec AC-1.6 row | LOW |
| 5 | Drift | plan:405 | extra cites D-P1-5 for "worker did not stage .dev/tasks"; wrong decision cited, requirement correct (WC-9) | .dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md:29 | LOW |
| 6 | Drift | coverage matrix | seven requirement-bearing spans of source.md have no matrix row (lines 16, 23, 30, 36-44, 70, 78, 87); reviewer verified the plan implements each (plan:20, 29, 33-49, 54-58, 541); matrix trace debt, not a plan defect | source.md; coverage-matrix.yaml | LOW |
| 7 | Authorized | plan:44, :48, :58 | extra preflight checks, Remove artifacts, section-check rule, step 2/3 rule, not-invoked check extended to guard cases 1 and 2 | source.md:63, :87 | LOW |

No Regression found (every command line in Tasks 2-24 matches source.md:51-79). Notes: this reviewer did not find the README.md install-line defect or the Task 23 find defect that reviewers 1 and 3 found.

Advisory: lc15 omits `--output <file>` that WORKER-CONTRACT.md:197 lists; lc13 uses --report-dir where the table names --output-dir (WORKER-CONTRACT.md:195); spec 2.1 permits both, so no rule is breached.
