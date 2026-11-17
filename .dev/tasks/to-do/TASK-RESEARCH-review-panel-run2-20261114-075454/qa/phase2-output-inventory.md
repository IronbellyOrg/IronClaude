# Phase 2 output inventory (Step 3.1)

**Date:** 2026-11-14
**Source:** one read-only shell loop over `research/[0-2][0-9]-*.md` (wc -l, Status line from the first 12 lines, grep counts of `## Gaps and Questions` and `## Summary`, grep of the two forbidden path strings inside this task's own `research/` folder; nothing outside the folder was opened).

| File | Lines | Status | Has Gaps section | Has Summary | Forbidden-string hits (line numbers) |
|---|---|---|---|---|---|
| 01-overlap-capability-matrix.md | 277 | Complete | yes | yes | none |
| 02-finding-contract.md | 254 | Complete | yes | yes | none |
| 03-merge-ledger-verdict.md | 284 | Complete | yes | yes | none |
| 04-dispatch-identity-tiers.md | 231 | Complete | yes | yes | none |
| 05-input-delivery-brief.md | 193 | Complete | yes | yes | none (the independence statement in this file names the folder as a rule; the strict string search found no hit) |
| 06-reflect-two-engines.md | 384 | Complete | yes | yes | none |
| 07-e1-evidence-grading.md | 124 | Complete | yes | yes | none |
| 08-e2-evidence-grading.md | 184 | Complete | yes | yes | none |
| 09-collaboration-designs.md | 223 | Complete | yes | yes | none |
| 10-process-redesign.md | 244 | Complete | yes | yes | none |
| 11-consumers-tasklist-workflow.md | 188 | Complete | yes | yes | none |
| 12-consumers-spec-review.md | 230 | Complete | yes | yes | none |
| 13-future-pr-review-and-rfqa.md | 278 | Complete | yes | yes | none |
| 14-e3-variants-and-experiments.md | 277 | Complete | yes | yes | none |
| 15-telemetry-manifest-run-record.md | 250 | Complete | yes | yes | none |
| 16-eval-governance.md | 301 | Complete | yes | yes | none |
| 17-defect-register.md | 560 | Complete | yes | yes | 534 (a statement of the independence rule and of the disclosed slice 03 grep slip; allowed, not a citation) |
| 18-repo-constraints-and-branching.md | 230 | Complete | yes | yes | none |
| 19-value-ledger-handoffs.md | 986 | Complete | yes | yes | none |
| 20-value-ledger-e2-study.md | 935 | Complete | yes | yes | none |
| 21-value-ledger-brainstorms.md | 1797 | Complete | yes | yes | none |
| 22-value-ledger-collab-designs.md | 1046 | Complete | yes | yes | none |
| 23-value-ledger-e1-e3-code.md | 894 | Complete | yes | yes | none |
| 24-value-ledger-evidence-consumers.md | 671 | Complete | yes | yes | none |

**Files found:** 24 (numbered 01-24, no number missing).
**Total lines:** 11041 (`cat [0-2][0-9]-*.md | wc -l`).
**Hit classification:** the one recorded hit (line 534 of file 17) is a statement of the independence rule, not a citation. Other files state the rule in different words (some include the strings in a sentence about the grep slip) and the strict-string search returned no hit; the Gate 1 independence checks re-scan.

**Gate 1 partitions (line counts computed from the table above):** A = files 01-08 = 277+254+284+231+193+384+124+184 = 1,931 lines; B = files 09-16 = 223+244+188+230+278+277+250+301 = 1,991 lines; C = files 17-24 = 560+230+986+935+1797+1046+894+671 = 7,119 lines. A + B + C = 11,041, equal to the total above.
