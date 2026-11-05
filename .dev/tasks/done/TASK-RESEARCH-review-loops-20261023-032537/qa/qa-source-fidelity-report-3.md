# Source-Document Fidelity Report: Partition 3

**Report reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md` (1,310 lines). Its sha256 was re-measured as `9ac64f1353fb9a6ea228af727183d3434788807498219150a54275a84ad8e568`, which matches the assignment.
**Partition:** 3 of 4 (CI-plan and Orca-monitor originals), as defined in `phase-outputs/discovery/fidelity-source-map.md:154-199`
**QA phase:** source-fidelity. Fix authorization: false. No file was edited.
**Date:** 2026-10-24
**Source files checked:** 24 primary and research files. The total text read was about 4,400 lines, plus targeted record reads from 2 session logs: 25 records of the CI log and about 60 records of the monitor log.

Verdict: FAIL

## Fidelity Findings

| # | Source File | Report Section | Type | Finding | Severity |
|---|---|---|---|---|---|
| 1 | Final second-review report `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/REPORT.md:21`. The same directory's `adversarial/round2-v1.md:5`. CI session log `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` record 1084 (03:48:11.615Z). `research/04-session-43582de1.md:361`. | §2.2 CI row (Report:167); §2.6 CI row (:272); §4 "Reviewer outputs contain overclaims" row (:347); §4 Key Takeaway CI row (:380) | Distorted (the report misstates how one stage led to the next) | The report calls reviewer 1's "16 fixed, 2 partial" an intermediate assessment. At :347 and :380 it says this judgment was "corrected ... in debate". The primary records show something narrower. In `round2-v1.md:5`, debate conceded only that the boundary-workflow gap is not an M-10 requirement and downgraded it to optional hardening. The completed second review then kept the same tally: "fixes 16 of the 18 cycle-0 findings in full and the other 2 in part" (REPORT.md:21). The final message to the user repeated it at record 1084: "16 of the 18 findings from the first review are now fixed, and the other 2 are partly fixed". Case 04:361 preserved this fact ("The final report repeats ..."), but the report dropped it. A reader would conclude that the 16/2 count was superseded, when it actually survived into the final verdict. That verdict also conflicts with the debate concession. **Required fix:** state that the final review report and record 1084 kept the 16-fixed/2-partial tally, while debate conceded that the boundary-file part of one partial item was not an original requirement. Keep the existing point that the "ready with notes" verdict was changed. | MINOR |
| 2 | Monitor session log `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl`: record 14 (19:29:17.282Z, the `/sc:implement` command); record 40 (19:29:22.409Z, the skill call); record 42 (19:29:22.708Z, the skill text loaded); record 58 (19:29:28.357Z, `qa.md` loaded). `research/05-session-e002bed2.md:83` lists "19:29:17.282 / 19:29:22.409" for "invocation and its skill load". | Option C, Scope row, shared-deployment paragraph (Report:578) | Inaccurate | The report says "the monitor's skill load was at 19:29:17Z". 19:29:17Z is when the user's command arrived. The skill was loaded at 19:29:22Z (records 40 and 42), and the rubric at 19:29:28Z (record 58). The conclusion does not change, because every one of these loads happened before the 20:29:54Z install. The timestamp is still attributed to the wrong event. **Required fix:** change it to "the monitor's skill load was at 19:29:22Z (records 40/42; the command was at 19:29:17Z)". | MINOR |

**Known, user-accepted defect J1 (not a new finding):** the stale status lines at Report:5, :1235 and :1287 were seen while reading the full report. They are recorded here as known, following `fidelity-source-map.md:6`.

## Claims Verified Against Primary Sources (no issue found)

| Report claim (location) | Primary evidence read |
|---|---|
| The original CI review merged 18 concerns, 10 medium and 8 low (§2.2, §2.1 table, Option A Effort) | Record 623 text; original `adversarial/merged-verdict.yaml` has 18 `M-` ids (10 medium, 8 low); original `REPORT.md:21,25` |
| The user authorized "refactor" (627). Review notes were written and the source concatenated (651/653). A new workflow package was generated (663/670) | Records 627, 651, 653, 663, 670 |
| The orchestrator said every note was applied (791). The calibrator then said the 18 earlier findings had not been checked (801) | Record 791: "Every review note is applied". Record 801: "the card never checked whether the 18 earlier findings are fixed" |
| Reviewer 1: 16 fixed, 2 partial, `ready_with_notes`, 4 new medium findings (810/821). Debate changed the verdict | Record 810 card (`overall_verdict: ready_with_notes`; self-audit M-05 and M-10 partial); record 821; `round2-v1.md:16,33` ("V2's 'not_ready' is the correct label") |
| The completed second review is not ready: 5 medium, 11 low, 0 high. Status is partial because 2 citations were dropped. The evidence spans records 1003-1084 | `REPORT.md:5,11,21-25,124-136`; `return-contract.yaml` `overall_verdict: not_ready`, medium 5, low 11; `evidence-validation.yaml:1-6`; second merged verdict: 16 ids, 5 medium and 11 low; records 1003, 1036, 1072, 1084 |
| The tooling exemption covers status but not hashes. Search filters are unchecked while creation arguments are asserted. A phrase blacklist accepts a half-edited advisory header | Regenerated plan lines 37, 94, 117, 128, 129, 183, 184; original plan lines 88, 105, 113, 114, 158; probe result at record 1003 (INV-004 to INV-006) |
| Repointing dependencies introduced a missing-ancestor defect (before/after). Sequential execution still protects runtime order | Original plan: every task depends on the previous one (lines 43-148). Regenerated plan lines 46, 56, 69, 79, 112, 138, 153, 172 and the prose rule at :31. Revised `source.md:82`. Original M-18 repoint advice. `REPORT.md:60` and `round2-v1.md:20` (`SKILL.md:97`, sequential) |
| Boundary-file hardening and the broad allowlist were qualified as optional (Option B Opposition: two of four new medium findings downgraded) | Final `REPORT.md:82-83` (D-011 and D-012 optional); `consensus-summary.md:17`; `round2-v1.md:5,14,30` |
| Observation windows: 1,000 rows ending 03:37:30.672Z; 1,086 rows ending 03:51:14.486Z | Timestamps of records 1000 and 1086 |
| Record 1087 (04:07:09.883Z) is the user's message "I am running that in another session" | Record 1087 |
| Q7: the post-window ledger was created at 04:06:20Z, with FINAL pass at :21 and ARCHIVE start at :22. It is outside the frozen sample. The plan hashes still match | Done `progress.md:1,21,22` (its PLAN sha is `895dcd6b…`, which is the regenerated plan); `sha256sum` of both plans matches `dcb320b5…` and `895dcd6b…` |
| Monitor: one invocation (14/40); the first Write produced a 640-line workflow (585) | Records 14, 40, 42; the record-585 Write content has 640 lines |
| Plan acceptance is structural, with behavior and job-wiring tests deferred to Task 14 | Plan `TASK-WF-designSpec-20261022-132541.md:209-232`; record 697 shows AC1-AC3 met and AC4 deferred |
| Seven verdicts (six noncompliant, one compliant), five reviewer identities, five repairs, four literal `fix` replies | Records 697, 804 and 849 (reviewer `abeae1e32b8eb193b`); 906, 1021, 1143 and 1240 (four other ids); `fix` at 820, 921, 1044 and 1153; halt at 817 |
| Older-pin behavior was first judged nonblocking (697); the equal-tag case was newly shown at 804 | Record 697: "Observations (judged, not blocking...)", line 48. Record 804, lines 67-73 |
| A protocol migration reopened the compliant result. No repair happened between 849 and 906 | Record 869 (`ls` shows installed files dated Oct 22 20:29); records 874 (installed `ledger.md`, Resume row P), 882/884 (installed `SKILL.md`), 885, 893, 902. Tool uses between 849 and 906 include no Edit or Write |
| The first repair introduced the trap regression (759-762), reproduced at 1240. The detect job got a sibling guard; the pin job did not | Record 759 new text `set -Eeuo pipefail`; 761 adds the stdout ERR trap; 760/762 succeeded. 1240 shows `P=::error::…`. 994 adds a `BASHPID` guard to detect. Current workflow lines 413 and 422 still contain the mechanism |
| Argument-size failure reproduced with 89 tags. The roughly 9,000-tag ceiling is theoretical. The field-10 cap is a plan gap | Record 1021 lines 31-32; record 1143 lines 44-51 |
| Edits at 1164-1170 were blocked, not applied | Record 1165 freshness-hook block |
| Prefix endpoint 1247. Acceptance at 1250, completion at 1261 with `misunderstood` unchanged and no eighth review | Records 1243, 1244 (count 4), 1247, 1250 (user, external), 1260, 1261; ledger lines 25-36 |
| Out-of-window adviser activity: 859 is an agent listing; the string occurs at 1620-2049; 1670 and 1997 are Task 14 advisers. No Task 12 retry records in 1-1247 | `grep` occurrence list; record 859 `agent_listing_delta`; records 1670 and 1997; 0 `T12: retry` lines before 1247 |
| Monitor Tasks 10 and 11 each converged after one repair | Records 267 to 319 (Task 10, extra then compliant); 496 to 540 (Task 11, missing then compliant) |
| Session 19 control: nine compliant task reviews | Orca ledger lines 3-20 |
| Deck citations :280, :312, :501-518, :505 and :547-548 support the claims made from them | `research/evidence-deck.md:265-336,497-552` |
| §10 descriptions of P3 inventory items: scope-01, scope-01-recovered (In Progress, four placeholders), screening and handoff captures, dispatch, resume-analysis and `.probe` files | `scope-01.md:13-24,48`; `scope-01-recovered.md:5,138-147`; `screening-recovery-source.txt:111-167`; `deep-handoffs-remaining-source.txt` headers; `ls` of three directories |

## Summary

- Files checked: 24 (2 primary session logs by record, 2 CI plans, CI source line 82, 8 CI review artifacts, the original CI merged verdict, the done CI ledger, the Orca plan, source and ledger, the current monitor workflow, both case files, deck ranges and the screening captures).
- Claims verified: 62 report statements on transitions, counts, timestamps and classifications, checked against primary records.
- Fidelity issues: 2 (CRITICAL 0, IMPORTANT 0, MINOR 2). Known defect J1 is excluded as user-accepted.
- No introduced-defect claim lacked before/after proof. The CI graph defect and the monitor trap regression both have before/after evidence. No review was invented, and no counterexample was ignored: the Task 10/11 controls, the downgraded CI findings and the post-window CI ledger all appear in the report.
- Verdict: FAIL. Any real issue fails, regardless of severity.
- **Confidence:** Verified: 62/62 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 16 | Grep: 0 | Glob: 0 | Bash: 25 (targeted `sed`/`jq`/`grep` record reads and hashes). No web research.

## Partition Limitations

- Cross-file checks covered only the Partition 3 sources plus the assigned cross-reads: Orca `source.md:340,365`, Orca plan 209-232 and ledger 3-20. Partitions 1, 2 and 4 cover the oracle, documentation, Orca planning, credential and current-rule claims, including the 20:29:54Z install provenance and rubric hashes. The shared-deployment claim was checked here only on the monitor side (records 869, 874 and 884).
- No Git-only objects belong to Partition 3, and no Git command was run.
- The CI source file `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/pull-sync-framework.yml:89-108` is unavailable (map:296). The report does not cite it directly. Its use in case 04 was judged against the second review's `REPORT.md:66`.
- `t12-monitor-yaml.log` has been overwritten (now 33 lines). The report makes no line claim from it.
- Historical log line counts the report gives as of 04:37Z (CI 1,153) cannot be re-measured. The CI log now has 1,156 lines and the monitor log 2,058; this is growth, not contradiction.
- Session logs were read by targeted record, not in full. The parent session log and index 03 were not opened.

## Verification Record

Record checks were mechanical (`jq`/`grep`/`sha256sum`). Both findings come from direct comparison of primary text with report wording. No finding was added to meet a quota.

| Status | Result |
|---|---|
| DONE | Compared every Partition 3 report claim with the primary CI and monitor records. Found 2 MINOR fidelity defects, so the verdict is FAIL. |
| NEXT | The fidelity consolidator (Step 6.28) merges these 2 findings for the single fixer (Step 6.29). |