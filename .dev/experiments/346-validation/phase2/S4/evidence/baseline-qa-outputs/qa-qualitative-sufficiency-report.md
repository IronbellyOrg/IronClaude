# QA Report - task-qualitative, lens qa-gate-sufficiency

**Status:** Complete
**Date:** 2026-11-07
**Task file:** TASK-RESEARCH-bmad-first-use-20261107-075901.md

---

## Counts (verified by grep on the task file)
Gate 1 = 3 agents (lines 217/221/225), Gate 2 = 3 (307/311/315), Gate 3 = 7 (370-386: 3 rf-qa, 3 rf-qa-qualitative, 1 domain), Gate 4 = 3 rf-qa (416-420), Gate 5 = 3 rf-analyst (446-450, covers all 12 inputs, no overlap, line 444). One fix agent per cycle (233,253,323,343,392,404,424,434,454,464). HALT after 2 cycles at 265,355,410,440,470. 91 items. No gate is under the standard minimum.

## Blocking findings
| # | Sev | Where | Finding | Fix |
|---|-----|-------|---------|-----|
| 1 | IMPORTANT | 217-241, 229, 245, 390 | No inline-return fallback for QA agents that cannot write .md files. Only Phase 2 mentions "cannot write" (192-208). Gate items say the report must be "produced by the agent and not by you". This session already needed transcription (qa/qa-fix-verification.md line 3). A missing report means "log blocker, mark complete" with no halt, so BLOCKING_COUNT can be 0 from absent reports and the gate passes. | Add to every gate item: agent returns findings inline, orchestrator persists them verbatim with a "transcribed" header; a missing or empty report means the gate is not PASS (re-spawn once, else HALT). |
| 2 | IMPORTANT | 229, 390, 452 | The orchestrator regrades findings alone. The consolidated table has no reporter-severity column, so downgrades are invisible. BLOCKING_COUNT 0 then skips the fix and verification (237, 241) and decides PASS (245). | Record reporter severity and a reason for every downgrade; one rf-qa must confirm any downgrade of a reporter FAIL to zero blocking. |
| 3 | IMPORTANT | 213, 307, 374, 380, 414 | No gate re-checks web facts against their URLs. Phase 4 has no QA, Gate 1 covers files 01-05 only, Gate 2 traces to research text, Gate 4 excludes web ("single source family"), lenses check only that a URL exists. The "skills created after session start" answer (web-01) decides options B, C and D. | Make the domain-accuracy lens or fidelity agent 3 re-fetch every URL behind a fact used in Sections 6-8 and confirm the quoted sentence. |
| 4 | IMPORTANT | 386, 374, 416 | The reproducibility lens samples 15 findings from Sections 2, 4, 6 and 7 only. Section 8 holds the pinned-assertion lines (for example test-57 lines 448-450) and is excluded. Evidence-quality samples 20, fidelity 8 per agent. A wrong line is MINOR when the claim is true (every lens), so it becomes a note. It would be caught only if sampled. | Reproduce EVERY row of the Section 8 pinned-test and document-change tables (open file:line, quote the assertion text); a wrong line on a row the plan tells the implementer to edit is blocking. |
| 5 | IMPORTANT | whole file | The zero-finding Self-Audit demand is absent. "Self-Audit" appears 0 times. Prompts say only "0 issues requires evidence" (217, 307, 370) and the lens OUTPUT FORMAT has no audit section, so a zero-finding PASS carries no checkable evidence. | Require a Self-Audit section (claims verified, files read, why 0 issues is credible) in every report-only agent and treat a zero-finding report without it as incomplete. |

## Minor notes
- Pinned-test list rests on hand-picked files (line 204). It currently matches the repo (grep -i bmad under .github: test-19, 46, 49, 52, 57, startup-boot, plus upstream-monitor expected.txt and renovate-global.json5, which no gate mentions). Add a repo-wide bmad grep to the crossref lens.
- Feasibility correctness is judged only at Gate 2 (315, item 6). Gate 3 checks consistency only (372, 382). Owner questions are checked at Gate 2 item 7 and Step 6.8 criterion 9 (474), not by any Gate 3 lens.
- SKILL Rule 14 floors (5 agents) conflict with the standard table (3); the task follows the table.

## Self-Audit
(a) Inherited PASS relied on: F7 counts (re-counted 91 items and agent types by grep), F2 (N defined in lenses), F3. (b) Where PASS was insufficient: F1 "inline prompts" passes structurally but does not cover the harness .md-write limit (finding 1); F7 "3 agents at Gates 4 and 5" passes but the Gate 4 partition omits web sources (finding 3). About 14 reads and greps, 25 claims checked. Lens prompts do test what their names claim; the reproducibility lens would catch a wrong file:line only inside its sample, outside Section 8.

VERDICT: FAIL (5 IMPORTANT, 0 CRITICAL, 3 MINOR)
