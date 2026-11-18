# Inventory of past review sources that flagged blocking issues

Status: In progress (sections below are appended; the last line says `Status: Complete` when done)
Date: 2026-11-15
Program: BLOCKER-CLASSIFICATION-PROGRAM-20261115, step 01
Repo: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel` (branch `ironbelly/shadow-runs`)

## 0. How to read this file

- Scope: only sources are listed; no findings are extracted here. Read-only everywhere except this file.
- `@E2` in a path means the file was read from `origin/ironbelly/eval-tasklist-review-panel` with `git show` / `git ls-tree` (not checked out). E2 paths marked `.../` abbreviate `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/`.
- `Path` abbreviations: none other than the E2 one; every local path is repo-relative.
- Excluded on purpose: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/`, `.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/`; the run-1 and run-2 research QA reports are listed only in section 5 (Kind `other`, fallback pool).
- Kind values: `tasklist review` (review of a generated tasklist or plan), `tasklist review (post-execution audit)` (reflect post audit of executed work against its tasklist or spec; owner may choose to treat these as `other`), `spec review` (review of a spec, design, PRD, TDD or roadmap), `other`.
- `Approx. blocking-flagged findings` = a number plus how it was counted. Methods: **stated** (the report states the number), **headings** (count of headings or ids carrying the marker), **section scan** (items under a `Blocking`/`Critical` section), **regex** (counted by script), **grep token** (count of a severity word, upper bound, marked ESTIMATE). **VERIFIED** = I opened the file or section and confirmed the number (more than 15 such checks, see section 7).
- `Read cost`: small under 300 lines, medium 300 to 1500, large over 1500. For group rows the `Lines` are the sum over all member files.
- Important overlap warning for the later step: many rows review the SAME document. S-045..S-056 and the E2 rows share one frozen plan family; S-201..S-284 all review one spec (`orca-worker-contract-spec.md`). Counts are therefore not independent findings.

## 1. Tasklist reviews and post-execution audits (S-001 to S-088)

| ID | Path | Kind | What was reviewed | Date | Blocking marker used | Approx. blocking-flagged findings (method) | Lines | Read cost |
|---|---|---|---|---|---|---|---|---|
| S-001 | `.dev/reflect/pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258/REPORT.md` | tasklist review | P1 static plan (Orca worker contract) vs spec | 2026-11-05 | `### MF-0n (blocking)` headings; "blocking = wrong behaviour or missing deliverable" | 8 (stated "8 blocking findings (MF-01..MF-08)" + 8 headings; VERIFIED by opening) | 154 | small |
| S-002 | `.dev/reflect/pre-TASK-WF-scIssueClaimPipe-20261107-063237-20261107063558/REPORT.md` | tasklist review | sc:issue claim-pipeline plan vs spec | 2026-11-07 | `## Blocking findings` section, ids B-1..B-6 (+ 6 MEDIUM Drift) | 6 (stated "6 blocking findings (B-1 to B-6)"; VERIFIED B-1/B-2 headings) | 472 | medium |
| S-003 | `.dev/reflect/pre-TASK-WF-implementStages0-20261111-202912-20261111203517/REPORT.md` | tasklist review | stages plan vs spec (round 2 review) | 2026-11-11 | `## Blocking findings (Grounded...)` | 8 (stated "6 blocking defects plus 2 from invariant probe"; section scan = 8; VERIFIED) | 57 | small |
| S-004 | `.dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/REPORT.md` | tasklist review | P2 static plan vs spec | 2026-11-07 | `Deviation D-nn ... INV-nnn (blocking)`, `Unaddressed invariants (blocking convergence)`, also P1/P2/P3 priority scale | 4 (D-03, D-05, INV-001, INV-002 flagged blocking; report also lists 5 P1 of 31 findings; VERIFIED) | 596 | medium |
| S-005 | `.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/REPORT.md` | tasklist review | P0 worker-contract plan vs spec | 2026-11-02 | `Deviation D-001 ... (blocking; merged id M-01)`, "open, possibly blocking" INV-002 | 2 (summary lines (D-001 + INV-002); VERIFIED) | 451 | medium |
| S-006 | `.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261103-012232-20261103055307/REPORT.md` | tasklist review | P0 worker-contract plan, 2nd run | 2026-11-03 | `Deviation D-nnn (blocking; merged id M-nn)` | 2 (stated "two blocking defects" (D-001, D-016); VERIFIED) | 541 | medium |
| S-007 | `.dev/reflect/pre-TASK-WF-implementIronbel-20261104-130647-20261104130837/REPORT.md` | tasklist review | issue #357 plan vs spec | 2026-11-04 | `## Blocking findings` with `### B-n` headings | 4 (4 headings (B-1..B-4); VERIFIED) | 90 | small |
| S-008 | `.dev/reflect/pre-TASK-WF-implementIronbel-20261104-130647-shadow09/REPORT.md` | tasklist review | same plan, shadow re-audit | 2026-11-04 | `### Cn - MAJOR, blocking as written` | 3 (C1-C3 flagged; C4 MAJOR non-blocking; VERIFIED) | 92 | small |
| S-009 | `.dev/reflect/pre-TASK-WF-makeTheAliasOnly-20261105-034531-20261105034821/REPORT.md` | tasklist review | alias-only ccsession plan vs spec | 2026-11-05 | "Four blocking defects" list M-1..M-4 (+19 minor) | 4 (stated + 4 bullets; VERIFIED) | 120 | small |
| S-010 | `.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104070955/REPORT.md` | tasklist review | sc:issue command plan, round 1 | 2026-11-04 | `### Finding F-nn (blocking, ...)` | 2 (stated "2 blocking and 16 minor"; headings F-01, F-02) | 169 | small |
| S-011 | `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/REPORT.md` | tasklist review | P0 live-plan vs spec | 2026-11-03 | table column `blocking` / `should-fix` | 2 (table rows D-001, D-002 (+ should-fix D-012)) | 193 | small |
| S-012 | `.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105165021/REPORT.md` | tasklist review | P1 live plan brief | 2026-11-05 | prose "one blocking defect" (stale branch tip) | 1 (stated in summary) | 24 | small |
| S-013 | `.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105172548/REPORT.md` | tasklist review | P1 live plan brief, recheck | 2026-11-05 | "Blocking (fixed, revision 3)" | 1 (1 bullet) | 26 | small |
| S-014 | `.dev/reflect/pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416/REPORT.md` | tasklist review | sc:issue worker plan | 2026-11-04 | `### Deviation D-M13 (blocking)`, "merged verdict FAIL with one blocking finding" | 1 (stated) | 91 | small |
| S-015 | `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/REPORT.md` | tasklist review | brainstorm fix plan | 2026-11-06 | invariant probe HIGH INV-020 "the skill's gate treats that as blocking" | 1 (prose; estimate) | 127 | small |
| S-016 | `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/REPORT.md` | tasklist review | brainstorm fix plan, run 2 | 2026-11-06 | HIGH INV-019 treated as blocking | 1 (prose; estimate) | 160 | small |
| S-017 | `.dev/reflect/pre-closeIronbellyOr-20261104124503/REPORT.md` | tasklist review | close-issues plan | 2026-11-04 | `### Deviation D-nnn: ... (blocking)` | 2 (D-001, D-002 headings) | 134 | small |
| S-018 | `.dev/reflect/pre-design-20261108041729/REPORT.md` | tasklist review | design plan (tests/skills worker contract) | 2026-11-08 | `## Blocking finding` | 1 (section; stated "one blocking gap") | 184 | small |
| S-019 | `.dev/reflect/pre-fixGitHubIssue31-20261105031639/REPORT.md` | tasklist review | issue 31 fix plan | 2026-11-05 | `D-001 (blocking until a criterion exists)` | 1 (1 heading) | 112 | small |
| S-020 | `.dev/reflect/pre-implementGitHubI-20261105171020/REPORT.md` | tasklist review | GitHub-issue implementation plan | 2026-11-05 | `### Finding M-Fn (blocking)` | 3 (stated "3 blocking findings and 7 minor") | 183 | small |
| S-021 | `.dev/reflect/pre-workflowSource-20261102234109/REPORT.md` | tasklist review | workflow-source tasklist | 2026-11-02 | `Deviation D-001 (blocking)` + `Adversarial invariant gate (blocking...)` INV-001/002/008 HIGH | 4 (1 + 3 invariants; VERIFIED) | 151 | small |
| S-022 | `.dev/reflect/pre-uc2-reachability-20260620-044943/REPORT.md` | tasklist review | UC2 reachability tasklist vs spec/TDD | 2026-06-20 | `## Blocking findings` C1..C5; "Status FAILED" | 5 (5 headings; VERIFIED) | 107 | small |
| S-023 | `.dev/reflect/pre-sprint-cli-tasklist-20260603114816/REPORT.md` | tasklist review | sprint CLI tasklist | 2026-06-03 | `## HIGH - must resolve before execution` | 4 (section scan (4 items)) | 84 | small |
| S-024 | `.dev/reflect/pre-prompts-plan-20260610051257/REPORT.md` | tasklist review | two generated prompts (reflect wrapper) | 2026-06-10 | `## CRITICAL findings` C-1, C-2 | 2 (section scan) | 56 | small |
| S-025 | `.dev/reflect/pre-reflect-wrapper-autofix-20260610132543/REPORT.md` | tasklist review | reflect wrapper auto-fix tasklist | 2026-06-10 | `## 1. Critical Findings (must resolve before execution)` F1 (HIGH) | 1 (1 heading) | 155 | small |
| S-026 | `.dev/reflect/pre-tavily-upgrade-20260623003519/REPORT.md` | tasklist review | Tavily upgrade plan | 2026-06-23 | `## BLOCKING - human decision required` (B1) | 1 (1 section) | 65 | small |
| S-027 | `.dev/reflect/pre-roadmap-brittleness-20260603190008/REPORT.md` | tasklist review | roadmap brittleness plan | 2026-06-03 | prose "the single blocking finding" | 1 (stated) | 86 | small |
| S-028 | `.dev/reflect/pre-phase3CodegraphA-20261029205359/REPORT.md` | tasklist review | codegraph phase 3 plan | 2026-10-29 | severity `critical`/`important`; "19 findings (0 critical, 9 important...)" | 9 (stated 9 important (ESTIMATE: important used as blocking-equivalent)) | 266 | small |
| S-029 | `.dev/reflect/pre-phase2CodegraphI-20261029192356/REPORT.md` | tasklist review | codegraph phase 2 plan | 2026-10-29 | `severity: important`; BLOCKED_BY_INVARIANTS | 4 (4 deviations tagged important (token count 7; ESTIMATE)) | 454 | medium |
| S-030 | `.dev/reflect/pre-phase1RemovalSpe-20261029185357/REPORT.md` | tasklist review | codegraph phase 1 removal plan | 2026-10-29 | severity `important` | 5 (grep token count (ESTIMATE, unverified)) | 549 | medium |
| S-031 | `.dev/reflect/pre-multimodelswarm-remediation-20260605/REPORT.md` | tasklist review | multi-model swarm remediation plan | 2026-06-05 | CRITICAL/HIGH deviation taxonomy | 3 (CRITICAL token count (ESTIMATE; 7 HIGH tokens)) | 111 | small |
| S-032 | `.dev/reflect/pre-refactorIronClau-20261102175540/REPORT.md` | tasklist review | refactor plan | 2026-11-02 | yaml comment "1 high, 3 medium, 10 low", verdict revise-before-execution | 1 (stated) | 257 | small |
| S-033 | `.dev/reflect/pre-implementTheLaun-20261107093251/REPORT.md` | tasklist review | launcher plan | 2026-11-07 | "One HIGH item", all Drift | 1 (stated in verdict line) | 105 | small |
| S-034 | `.dev/reflect/pre-TASK-WF-planTheRealBound-20261107-080351-20261107080543/REPORT.md` | tasklist review | real-boundary plan | 2026-11-07 | HIGH/MEDIUM/LOW scale; verdict FAIL-ADVISORY | 4 (4 HIGH (stated in the 2nd run's report)) | 82 | small |
| S-035 | `.dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/artifacts/reflect/pre-20261030154210/REPORT.md` | tasklist review | follow-up codegraph plan | 2026-10-30 | "2 critical and 18 important deviations" | 20 (stated) | 183 | small |
| S-036 | `.dev/reflect/pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow02/reviewer-cards/` | tasklist review | ccsession detach plan, shadow02 (no REPORT.md; cards only) | 2026-11-02 | reviewer-card `blocking: true` | 4 (grep of cards (as filed)) | 106 | small |
| S-037 | `.dev/reflect/post-sprint-recovery-stranded-20260608175221/REPORT.md` | tasklist review (post-execution audit) | post audit of sprint recovery work vs spec | 2026-06-08 | `## Confirmed blocking defects` DEV-1..3 (Regression/Drift) | 3 (stated "3 blocking claims survived"; VERIFIED) | 101 | small |
| S-038 | `.dev/reflect/post-sprint-auto-resume-rerun-20260603115107/REPORT.md` | tasklist review (post-execution audit) | post audit rerun, sprint auto-resume | 2026-06-03 | `## Blocking finding - NEW-R1 (Regression)` | 1 (heading; VERIFIED) | 93 | small |
| S-039 | `.dev/reflect/post-sprint-auto-resume-20260603003009/REPORT.md` | tasklist review (post-execution audit) | post audit, sprint auto-resume | 2026-06-03 | `regression_present: true (F-3)` | 1 (1 confirmed; text also says "4 regressions" before downgrade (ESTIMATE 1-4)) | 127 | small |
| S-040 | `.dev/reflect/post-rv3low-impl-audit-20260602T211900/REPORT.md` | tasklist review (post-execution audit) | post audit rv3-low implementation | 2026-06-02 | frontmatter `deviation_count_by_class: regression: 2` | 2 (frontmatter; VERIFIED) | 74 | small |
| S-041 | `.dev/reflect/post-phase2-recovery-20260602024648/REPORT.md` | tasklist review (post-execution audit) | post audit phase 2 recovery | 2026-06-02 | "2 regression" in findings summary | 2 (stated (grep)) | 157 | small |
| S-042 | `.dev/reflect/r0-closure-uc2-validation/REPORT.md` | tasklist review (post-execution audit) | UC2 validation, R0 closure | 2026-06 | "1 Drift + 1 Regression class", verdict close-with-caveats | 2 (stated) | 126 | small |
| S-043 | `.dev/reflect/r1-3-uc2-validation/REPORT.md` | tasklist review (post-execution audit) | UC2 validation r1-3 | 2026-06 | "ship-blocking finding", verdict PARTIAL | 1 (stated) | 116 | small |
| S-044 | `.dev/reflect/post-reflect-reviewer-guard-20260623185200/REPORT.md` | tasklist review (post-execution audit) | post audit reflect reviewer guard | 2026-06-23 | `D-1 Drift (MEDIUM-HIGH)` (borderline, no blocking word) | 1 (heading (borderline)) | 106 | small |
| S-045 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboA-r1/REPORT.md (+reviewer-cards)` | tasklist review | frozen pr-submit merge-guard plan (issue 375) vs spec, combo A run 1 | 2026-11-07 | `### MFn (MAJOR, blocking, <category>)` | 2 (merged 2 (MF1, MF2); cards as filed 2) | 256 | small |
| S-046 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboA-r2/REPORT.md (+cards)` | tasklist review | same plan, combo A run 2 | 2026-11-07 | `### Blocking (execute-no-further...)`, yaml `blocking: true` | 4 (merged yaml 4; cards 0 (format)) | 196 | small |
| S-047 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboA-r3/REPORT.md (+cards)` | tasklist review | same plan, combo A run 3 | 2026-11-07 | cards `"blocking":true` | 4 (cards as filed 4; merged 0) | 112 | small |
| S-048 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboB-r2/REPORT.md (+cards)` | tasklist review | same plan, combo B run 2 | 2026-11-07 | `### Fn (MAJOR, BLOCKING, <category>)` | 6 (merged 3 (F1-F3; VERIFIED); cards as filed 6) | 393 | medium |
| S-049 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r1/REPORT.md (+cards)` | tasklist review | same plan, combo C run 1 | 2026-11-07 | reviewer `blocking: true` reduced by debate | 7 (as filed 7; merged 0 (all `MAJOR, not blocking`)) | 292 | small |
| S-050 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r2/REPORT.md (+cards)` | tasklist review | same plan, combo C run 2 | 2026-11-07 | `### M-n (MAJOR, blocking, ...)` | 4 (merged 2 (M-1, M-2; VERIFIED); as filed 4) | 340 | medium |
| S-051 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboD-r1/REPORT.md (+cards)` | tasklist review | same plan, combo D run 1 | 2026-11-07 | `### Gap G1 (MAJOR, BLOCKING)` | 3 (merged 1; as filed 3) | 250 | small |
| S-052 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboD-r2/REPORT.md (+cards)` | tasklist review | same plan, combo D run 2 | 2026-11-07 | `(MAJOR, blocking: no)` for all 5 merged | 1 (as filed 1; merged 0 (borderline MAJOR pool)) | 364 | medium |
| S-053 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboD-r3/REPORT.md (+cards)` | tasklist review | same plan, combo D run 3 | 2026-11-07 | cards `blocking: true` | 2 (as filed 2; merged 0) | 412 | medium |
| S-054 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboE-r1/REPORT.md (+cards)` | tasklist review | same plan, combo E run 1 | 2026-11-07 | "Two acceptance-criteria gaps are blocking"; table column Blocking | 8 (as filed 8; merged 2) | 166 | small |
| S-055 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboE-r2/REPORT.md (+cards)` | tasklist review | same plan, combo E run 2 | 2026-11-07 | "5 MAJOR blocking as filed" in reviewer table | 6 (as filed 6; merged 0) | 215 | small |
| S-056 | `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboE-r3/REPORT.md (+cards)` | tasklist review | same plan, combo E run 3 | 2026-11-07 | `Severity / blocking: MAJOR / false` pairs, cards `blocking:true` | 7 (as filed 7; merged 0) | 385 | medium |
| S-057 | `@E2 .dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/ground-truth.json` | tasklist review | E2 ground truth for the same plan (10 defects) | 2026-11-11 | `"blocking_in_implement": true` | 5 (5 of 10 GT items; VERIFIED) | 207 | small |
| S-058 | `@E2 .dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-makeTheAliasOnly-20261105-051649/ground-truth.json` | tasklist review | E2 ground truth, alias plan (4 defects) | 2026-11-11 | `"blocking_in_implement": true` | 3 (3 of 4 GT items; VERIFIED) | 104 | small |
| S-059 | `@E2 .dev/eval-workspaces/tasklist-review-panel/20261111-a1/arms/C/TASK-WF-designSpec-20261107-075614/merged-1.md (+ledger.json)` | tasklist review | E2 pilot arm C merged ledger, designSpec | 2026-11-11 | ledger rows with blocking flag | 1 (PILOT-REPORT table "13 (1)") | 61 | small |
| S-060 | `@E2 .dev/eval-workspaces/tasklist-review-panel/20261111-a1/arms/B/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md` | tasklist review | E2 pilot arm B merged ledger, alias | 2026-11-11 | ledger rows with blocking flag | 1 (PILOT-REPORT "7 (1)") | 57 | small |
| S-061 | `@E2 .dev/eval-workspaces/tasklist-review-panel/20261111-a1/arms/C/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md` | tasklist review | E2 pilot arm C merged ledger, alias | 2026-11-11 | ledger rows with blocking flag | 2 (PILOT-REPORT "6 (2)") | 155 | small |
| S-062 | `@E2 .dev/eval-workspaces/tasklist-review-panel/20261111-a1/arms/A/TASK-WF-design-20261108-041415/merged-1.md` | tasklist review | E2 pilot arm A merged ledger, design | 2026-11-11 | ledger rows with blocking flag | 1 (PILOT-REPORT "1 (1)") | 69 | small |
| S-063 | `@E2 .dev/eval-workspaces/tasklist-review-panel/20261111-a1/arms/B/TASK-WF-design-20261108-041415/merged-1.md` | tasklist review | E2 pilot arm B merged ledger, design | 2026-11-11 | ledger rows with blocking flag | 1 (PILOT-REPORT "2 (1)") | 118 | small |
| S-064 | `@E2 .dev/eval-workspaces/tasklist-review-panel/20261111-a1/arms/C/TASK-WF-design-20261108-041415/merged-1.md` | tasklist review | E2 pilot arm C merged ledger, design | 2026-11-11 | ledger rows with blocking flag | 1 (PILOT-REPORT "2 (1)") | 145 | small |
| S-065 | `@E2 .../TASK-WF-design-20261108-041415/reviews/{base panel,b*,c*,e*,sol/terra-alone}/t*.md` | tasklist review | E2 reviewer reports, design plan, group A (57 reports) | 2026-11-11 | `findings-v1` JSON line `"blocking":true` | 65 (regex count over 57 files (188 false); VERIFIED on one sample file) | 2877 | large |
| S-066 | `@E2 .../TASK-WF-design-20261108-041415/reviews/combos/g*/t*.md` | tasklist review | E2 reviewer reports, design plan, g series (100 reports) | 2026-11-11 | `"blocking":true` | 135 (regex count (296 false)) | 4263 | large |
| S-067 | `@E2 .../TASK-WF-design-20261108-041415/reviews/combos/{h*,i*,j*}/t*.md` | tasklist review | E2 reviewer reports, design plan, h/i/j series (74 reports) | 2026-11-11 | `"blocking":true` | 75 (regex count (242 false)) | 3038 | large |
| S-068 | `@E2 .../TASK-WF-design-20261108-041415/reviews/combos/n*/t*.md` | tasklist review | E2 reviewer reports, design plan, n series (99 reports) | 2026-11-11 | `"blocking":true` | 90 (regex count (385 false)) | 5167 | large |
| S-069 | `@E2 .../TASK-WF-design-20261108-041415/reviews/combos/r*/t*.md` | tasklist review | E2 reviewer reports, design plan, r series (49 reports) | 2026-11-11 | `"blocking":true` | 57 (regex count (233 false)) | 2790 | large |
| S-070 | `@E2 .../TASK-WF-designSpec-20261107-075614/reviews/{base,b*,c*,e*,alone}/t*.md` | tasklist review | E2 reviewer reports, designSpec plan, group A (58 reports) | 2026-11-11 | `"blocking":true` | 27 (regex count (187 false)) | 2302 | large |
| S-071 | `@E2 .../TASK-WF-designSpec-20261107-075614/reviews/combos/g*/t*.md` | tasklist review | E2 reviewer reports, designSpec, g series (100) | 2026-11-11 | `"blocking":true` | 41 (regex count (271 false)) | 3433 | large |
| S-072 | `@E2 .../TASK-WF-designSpec-20261107-075614/reviews/combos/{h*,i*,j*}/t*.md` | tasklist review | E2 reviewer reports, designSpec, h/i/j (71) | 2026-11-11 | `"blocking":true` | 29 (regex count (247 false)) | 3097 | large |
| S-073 | `@E2 .../TASK-WF-designSpec-20261107-075614/reviews/combos/n*/t*.md` | tasklist review | E2 reviewer reports, designSpec, n series (118) | 2026-11-11 | `"blocking":true` | 30 (regex count (445 false)) | 5526 | large |
| S-074 | `@E2 .../TASK-WF-designSpec-20261107-075614/reviews/combos/r*/t*.md` | tasklist review | E2 reviewer reports, designSpec, r series (57) | 2026-11-11 | `"blocking":true` | 32 (regex count (274 false)) | 2990 | large |
| S-075 | `@E2 .../TASK-WF-makeTheAliasOnly-20261105-051649/reviews/{base,b*,c*,e*,alone}/t*.md` | tasklist review | E2 reviewer reports, alias plan, group A (57) | 2026-11-11 | `"blocking":true` | 101 (regex count (140 false)) | 2891 | large |
| S-076 | `@E2 .../TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/g*/t*.md` | tasklist review | E2 reviewer reports, alias, g series (100) | 2026-11-11 | `"blocking":true` | 128 (regex count (258 false)) | 3981 | large |
| S-077 | `@E2 .../TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/{h*,i*,j*}/t*.md` | tasklist review | E2 reviewer reports, alias, h/i/j (74) | 2026-11-11 | `"blocking":true` | 84 (regex count (199 false)) | 3265 | large |
| S-078 | `@E2 .../TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/n*/t*.md` | tasklist review | E2 reviewer reports, alias, n series (109) | 2026-11-11 | `"blocking":true` | 148 (regex count (375 false)) | 5536 | large |
| S-079 | `@E2 .../TASK-WF-makeTheAliasOnly-20261105-051649/reviews/combos/r*/t*.md` | tasklist review | E2 reviewer reports, alias, r series (54) | 2026-11-11 | `"blocking":true` | 86 (regex count (235 false)) | 3020 | large |
| S-080 | `.dev/experiments/346-validation/phase2/S2/baseline-outputs/R1-REPORT.md` | tasklist review | review-severity-rule plan, pre-review 1 (reflect, original incident) | 2026-11-02 | `## Blocking findings` ids B-01..B-11 | 11 (11 distinct ids; VERIFIED) | 62 | small |
| S-081 | `.dev/experiments/346-validation/phase2/S2/baseline-outputs/R2-REPORT.md` | tasklist review | same plan, pre-review 2 | 2026-11-02 | `## Blocking findings` P2-B1..P2-B7 | 7 (7 distinct ids; VERIFIED) | 40 | small |
| S-082 | `.dev/experiments/346-validation/phase2/S2/baseline-outputs/R3-REPORT.md` | tasklist review | same plan, pre-review 3 | 2026-11-02 | `## Blocking findings` B3-nn | 10 (10 distinct ids; VERIFIED) | 56 | small |
| S-083 | `.dev/orca-command-refactor/review/p0-live-plan-recheck.md` | tasklist review | P0 live plan re-check (orca refactor) | 2026-11-05 | "3 blocking (N-01 to N-03), 6 minor" | 3 (stated) | 163 | small |
| S-084 | `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/qa/ (qa-task-validation-*)` | tasklist review | rf-qa validation of an MDTM task file | 2026-06-20 | `Overall Verdict: FAIL`, issue table severity CRITICAL/IMPORTANT | 9 (table-row grep over 4 files (ESTIMATE)) | 806 | medium |
| S-085 | `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/ (qa-task-validation-*)` | tasklist review | rf-qa validation of the issue-watcher task file | 2026-11-07 | "VERDICT: FAIL (0 CRITICAL, 2 IMPORTANT, 11 MINOR)" | 16 (table-row grep over 8 files; stated 2 IMPORTANT in one report (ESTIMATE)) | 1221 | medium |
| S-086 | `.dev/tasks/to-do/TASK-RF-t2-fallback-ladder-20260706-050832/qa/ (qa-task-validation-*)` | tasklist review | rf-qa validation of the t2 fallback ladder task file | 2026-07-06 | `Overall Verdict: FAIL`; CRITICAL/IMPORTANT rows | 4 (table-row grep over 4 files (ESTIMATE)) | 398 | medium |
| S-087 | `.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/qa/ (qa-task-validation-*)` | tasklist review | rf-qa validation of the detection-contract task file | 2026-07-01 | CRITICAL/IMPORTANT issue rows (fixed in place, final PASS) | 13 (table-row grep over 5 files (ESTIMATE)) | 358 | medium |
| S-088 | `.dev/tasks/to-do/TASK-RF-pr-submit-v11-20260612-013419/qa/ (qa-task-validation-*)` | tasklist review | rf-qa validation of the pr-submit v11 task file | 2026-06-12 | "5 documented issues - 1 IMPORTANT, 4 MINOR" | 1 (stated) | 438 | medium |

## 2. Spec reviews, hand-listed (S-089 to S-114)

| ID | Path | Kind | What was reviewed | Date | Blocking marker used | Approx. blocking-flagged findings (method) | Lines | Read cost |
|---|---|---|---|---|---|---|---|---|
| S-089 | `.dev/orca-command-refactor/review/spec-panel.md` | spec review | orca worker-contract spec, spec-panel round 1 (original issue-346 incident) | 2026-11-02 | `**FAIL.** 24 findings: 3 CRITICAL, 15 MAJOR, 6 MINOR` (binary rule: any finding fails) | 18 (stated CRITICAL+MAJOR; VERIFIED) | 200 | small |
| S-090 | `.dev/orca-command-refactor/review/spec-panel-round2.md` | spec review | same spec, round 2 | 2026-11-02 | "13 new findings: 1 CRITICAL, 9 MAJOR, 3 MINOR" | 10 (stated; VERIFIED) | 283 | small |
| S-091 | `.dev/orca-command-refactor/review/spec-panel-round3.md` | spec review | same spec, round 3 | 2026-11-03 | "14 new findings: 0 CRITICAL, 8 MAJOR, 6 MINOR" | 8 (stated; VERIFIED) | 281 | small |
| S-092 | `.dev/orca-command-refactor/review/round4-review.md` | spec review | same spec, PR #343 diff review rounds 4-5 | 2026-11-04 | `### Bn. BLOCKING:` headings, "2 blocking, 11 minor", then "1 blocking, 3 minor" | 3 (3 headings (B1, B2, N1); VERIFIED) | 252 | small |
| S-093 | `.dev/orca-command-refactor/review/final-diff-review.md` | spec review | same spec, final diff review | 2026-11-04 | "0 CRITICAL, 3 MAJOR, 4 MINOR" (D1-D3 MAJOR) | 3 (stated) | 125 | small |
| S-094 | `.dev/orca-command-refactor/review/p0-spec-fix-review.md` | spec review | same spec, P0 fix review | 2026-11-05 | "S1 has two blocking defects" | 2 (stated) | 132 | small |
| S-095 | `.dev/experiments/346-validation/phase2/S3/baseline/reviews/plan-review.md` | spec review | launch-level-hook refactor plan (issue 394, design), review 1 | 2026-11-05 | `**B-n (BLOCKING).**` "Blocking findings: 8" | 8 (stated; VERIFIED) | 194 | small |
| S-096 | `.dev/experiments/346-validation/phase2/S3/baseline/reviews/plan-review-2.md` | spec review | same plan, review 2 | 2026-11-05 | `### F-n (BLOCKING).` "Blocking findings: 8" | 8 (stated; VERIFIED) | 262 | small |
| S-097 | `.dev/experiments/346-validation/phase2/S3/baseline/reviews/plan-review-3.md` | spec review | same plan, review 3 | 2026-11-05 | "Blocking findings: 10 (B-1 to B-10)" | 10 (stated; VERIFIED) | 300 | medium |
| S-098 | `.dev/experiments/346-validation/phase5/final-bundle/confirmations/diffgate-r2/orca-command-refactor/review/spec-panel.md` | spec review | orca spec, spec-panel-diffgate confirmation r2 | 2026-11-08 | "8 blocking findings (R1.1-R1.8)", `diffgate.py` `blocking_ids` | 8 (stated) | 141 | small |
| S-099 | `.dev/experiments/346-validation/phase5/final-bundle/confirmations/diffgate-r3/orca-command-refactor/review/spec-panel.md` | spec review | same, confirmation r3 | 2026-11-08 | "10 blocking findings" | 10 (stated) | 135 | small |
| S-100 | `.dev/experiments/346-validation/phase5/final-bundle/confirmations/ponytail-r2/orca-command-refactor/review/spec-panel.md` | spec review | spec-panel-ponytail confirmation r2 | 2026-11-08 | `(MAJOR, blocking)` headings | 1 (not stated; minimum 1 (ESTIMATE, uncounted)) | 154 | small |
| S-101 | `.dev/experiments/346-validation/phase5/final-bundle/confirmations/ponytail-r3/orca-command-refactor/review/spec-panel.md` | spec review | spec-panel-ponytail confirmation r3 | 2026-11-08 | "12 blocking (2 CRITICAL, 10 MAJOR...)" | 12 (stated) | 187 | small |
| S-102 | `.dev/experiments/346-validation/phase5/final-bundle/measurements/diffgate/reviews/ (spec-panel*.md, 3 rounds)` | spec review | diffgate arm, 3 review rounds | 2026-11-08 | "7 blocking findings" (r2), "2 blocking items" (r3), r1 uncounted | 9 (stated r2+r3; r1 not counted (lower bound)) | 484 | medium |
| S-103 | `.dev/experiments/346-validation/phase5/final-bundle/measurements/ledger/reviews/review/ (spec-panel*.md)` | spec review | ledger arm, rounds 1-3 + sweep | 2026-11-08 | `Blocking finding ids:`; "13 blocking findings", round 3 "22 blocking rows" | 20 (ids parser (13 + 7)) | 869 | medium |
| S-104 | `.dev/experiments/346-validation/phase5/final-bundle/measurements/ponytail/reviews/ (spec-panel*.md)` | spec review | ponytail arm, rounds 1-3 | 2026-11-08 | `Blocking finding ids:`; "8 blocking" | 21 (ids parser (10 + 11)) | 583 | medium |
| S-105 | `.dev/research/346-review-loop-experiments/p17/findings.jsonl` | spec review | PRE-EXTRACTED: 511 blocking findings from first reviews and frozen audits of 13 arms (140 audits), orca spec | 2026-11-10 | JSON rows with `heading` like `### B1 [CRITICAL, blocking] ...` | 511 (511 rows; 275 headings contain "blocking"; per LEDGER-RESULTS.md "all 511 blocking findings") | 511 | medium |
| S-106 | `.dev/research/346-review-loop-experiments/p17/ledger.json` | spec review | clustered defect ledger (58 defects) of the orca spec | 2026-11-10 | `"severity": "blocking"/"medium"/"minor"` | 26 (jq-style grep: 26 blocking, 20 medium, 5 minor, rest other) | 1188 | medium |
| S-107 | `.dev/releases/backlog/prd-artifact-containment/spec-panel-review.md` | spec review | PRD artifact containment spec-panel | 2026-05-15 | severity CRITICAL/HIGH/MAJOR | 4 (CRITICAL token count (ESTIMATE); also 24 HIGH tokens) | 260 | small |
| S-108 | `.dev/releases/backlog/tdd-artifact-containment/spec-panel-review.md` | spec review | TDD artifact containment spec-panel | 2026-05-15 | severity CRITICAL/HIGH | 9 (CRITICAL token count (ESTIMATE); 26 HIGH tokens) | 304 | medium |
| S-109 | `.dev/releases/backlog/v4.xx-SpawnV2/spec-panel-review.md` | spec review | SpawnV2 spec-panel | 2026-03-23 | severity CRITICAL/MAJOR | 8 (CRITICAL token count (ESTIMATE); 20 MAJOR) | 378 | medium |
| S-110 | `.dev/releases/backlog/v5.xx_release-eval-ab-test/spec-synthesis/spec-panel-review.md` | spec review | release-eval A/B spec-panel | 2026-03-19 | CRITICAL/MAJOR | 1 (CRITICAL token count (ESTIMATE); 8 MAJOR) | 202 | small |
| S-111 | `.dev/releases/current/cleanup-debt-reduction/spec-panel-review.md` | spec review | cleanup-debt-reduction spec-panel | 2026-10-20 | CRITICAL/MAJOR | 1 (CRITICAL token count (ESTIMATE); 6 MAJOR) | 374 | medium |
| S-112 | `.dev/reflect/pre-sprint-cli-arch-20260603002500/REPORT.md` | spec review | reflect UC-1 on SYNTHESIS.md (sprint CLI architecture spec) | 2026-06-03 | `### HIGH (must resolve before authoring a tasklist)` | 6 (stated "16 gaps (6 HIGH)") | 136 | small |
| S-113 | `.dev/reflect/pre-forbid-security-lens-20260620045010/REPORT.md` | spec review | reflect UC-1 on forbid-security-lens requirements | 2026-06-20 | "2 gaps block a clean pass"; verdict amend-then-proceed | 2 (stated) | 95 | small |
| S-114 | `.dev/reflect/pre-reflect-t2-fallback-ladder-202607060452/REPORT.md` | spec review | reflect pre on t2 fallback-ladder design.md | 2026-07-06 | `### HIGH - F1..F3` | 3 (3 headings) | 102 | small |

## 3. Spec reviews: #346 review-loop runs (S-201 to S-284, one row per run)

All rows review the same document, `orca-worker-contract-spec.md` (the issue-346 incident spec). Counts = ids on `Blocking finding ids:` lines of review files whose last verdict is FAIL (deduplicated; excludes `.orig.md` and `r1a/b/c` copies). The number in parentheses is the count of those review files; Lines is their total. ID order: p11 a1/a2/a3 = S-201..S-214; p12 ab1 b1 S-215..220, b1h S-221..224; ab2 b2 S-225..230, b2h S-231..234; ab3 b3 S-235..240, b3h S-241..244; baseline-audit2 S-245..250; p13 ab1 (PN1) S-251..256; p13 ab2 (PN2) S-257..262; p14 Haiku baseline S-263..268; p16 d4 S-269..274, d4h S-275..278; base-drift S-279..284.

| ID | Path | Kind | What was reviewed | Date | Blocking marker used | Approx. blocking-flagged findings (method) | Lines | Read cost |
|---|---|---|---|---|---|---|---|---|
| S-201 | `.dev/research/346-review-loop-experiments/p11/runs/a1-r1/` | spec review | stage-2 arm a1, /sc:spec-panel rounds on orca-worker-contract-spec.md (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 19 (4 review files) | 1227 | medium |
| S-202 | `.dev/research/346-review-loop-experiments/p11/runs/a1-r3/` | spec review | stage-2 arm a1, /sc:spec-panel rounds on orca-worker-contract-spec.md (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 9 (2 review files) | 705 | medium |
| S-203 | `.dev/research/346-review-loop-experiments/p11/runs/a2-r1/` | spec review | stage-2 arm a2 round prompts (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (2 review files) | 423 | medium |
| S-204 | `.dev/research/346-review-loop-experiments/p11/runs/a2-r2/` | spec review | stage-2 arm a2 round prompts (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 5 (3 review files) | 708 | medium |
| S-205 | `.dev/research/346-review-loop-experiments/p11/runs/a2-r3/` | spec review | stage-2 arm a2 round prompts (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 3 (1 review files) | 181 | small |
| S-206 | `.dev/research/346-review-loop-experiments/p11/runs/a2-r4/` | spec review | stage-2 arm a2 round prompts (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (2 review files) | 494 | medium |
| S-207 | `.dev/research/346-review-loop-experiments/p11/runs/a2-r5/` | spec review | stage-2 arm a2 round prompts (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 3 (2 review files) | 534 | medium |
| S-208 | `.dev/research/346-review-loop-experiments/p11/runs/a2-r6/` | spec review | stage-2 arm a2 round prompts (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 1 (1 review files) | 222 | small |
| S-209 | `.dev/research/346-review-loop-experiments/p11/runs/a3-r1/` | spec review | stage-2 baseline arm a3 (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (2 review files) | 346 | medium |
| S-210 | `.dev/research/346-review-loop-experiments/p11/runs/a3-r2/` | spec review | stage-2 baseline arm a3 (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (2 review files) | 380 | medium |
| S-211 | `.dev/research/346-review-loop-experiments/p11/runs/a3-r3/` | spec review | stage-2 baseline arm a3 (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 5 (2 review files) | 431 | medium |
| S-212 | `.dev/research/346-review-loop-experiments/p11/runs/a3-r4/` | spec review | stage-2 baseline arm a3 (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 3 (2 review files) | 429 | medium |
| S-213 | `.dev/research/346-review-loop-experiments/p11/runs/a3-r5/` | spec review | stage-2 baseline arm a3 (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 3 (1 review files) | 197 | small |
| S-214 | `.dev/research/346-review-loop-experiments/p11/runs/a3-r6/` | spec review | stage-2 baseline arm a3 (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 5 (3 review files) | 681 | medium |
| S-215 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1-r1/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 13 (7 review files) | 714 | medium |
| S-216 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1-r2/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 13 (6 review files) | 753 | medium |
| S-217 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1-r3/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 13 (5 review files) | 632 | medium |
| S-218 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1-r4/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 14 (6 review files) | 963 | medium |
| S-219 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1-r5/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 14 (6 review files) | 745 | medium |
| S-220 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1-r6/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 16 (5 review files) | 658 | medium |
| S-221 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1h-r1/` | spec review | ab1 k=3 union+verify, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 28 (7 review files) | 950 | medium |
| S-222 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1h-r2/` | spec review | ab1 k=3 union+verify, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 28 (7 review files) | 1375 | medium |
| S-223 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1h-r3/` | spec review | ab1 k=3 union+verify, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 13 (5 review files) | 692 | medium |
| S-224 | `.dev/research/346-review-loop-experiments/p12/ab1/runs/b1h-r4/` | spec review | ab1 k=3 union+verify, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 23 (7 review files) | 1123 | medium |
| S-225 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2-r1/` | spec review | ab2 verify gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 7 (3 review files) | 582 | medium |
| S-226 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2-r2/` | spec review | ab2 verify gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 5 (3 review files) | 431 | medium |
| S-227 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2-r3/` | spec review | ab2 verify gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 5 (3 review files) | 491 | medium |
| S-228 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2-r4/` | spec review | ab2 verify gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (2 review files) | 369 | medium |
| S-229 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2-r5/` | spec review | ab2 verify gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (2 review files) | 364 | medium |
| S-230 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2-r6/` | spec review | ab2 verify gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 6 (3 review files) | 503 | medium |
| S-231 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2h-r1/` | spec review | ab2 verify gate, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 9 (4 review files) | 580 | medium |
| S-232 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2h-r2/` | spec review | ab2 verify gate, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 12 (4 review files) | 553 | medium |
| S-233 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2h-r3/` | spec review | ab2 verify gate, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 10 (4 review files) | 752 | medium |
| S-234 | `.dev/research/346-review-loop-experiments/p12/ab2/runs/b2h-r4/` | spec review | ab2 verify gate, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 13 (4 review files) | 641 | medium |
| S-235 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3-r1/` | spec review | ab3 final whole-document gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 8 (3 review files) | 424 | medium |
| S-236 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3-r2/` | spec review | ab3 final whole-document gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 8 (5 review files) | 772 | medium |
| S-237 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3-r3/` | spec review | ab3 final whole-document gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 6 (5 review files) | 735 | medium |
| S-238 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3-r4/` | spec review | ab3 final whole-document gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 9 (5 review files) | 714 | medium |
| S-239 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3-r5/` | spec review | ab3 final whole-document gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 5 (4 review files) | 635 | medium |
| S-240 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3-r6/` | spec review | ab3 final whole-document gate, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 5 (2 review files) | 399 | medium |
| S-241 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3h-r1/` | spec review | ab3 final whole-document gate, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 19 (5 review files) | 759 | medium |
| S-242 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3h-r2/` | spec review | ab3 final whole-document gate, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 23 (7 review files) | 1139 | medium |
| S-243 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3h-r3/` | spec review | ab3 final whole-document gate, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 17 (7 review files) | 886 | medium |
| S-244 | `.dev/research/346-review-loop-experiments/p12/ab3/runs/b3h-r4/` | spec review | ab3 final whole-document gate, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 17 (5 review files) | 606 | medium |
| S-245 | `.dev/research/346-review-loop-experiments/p12/baseline-audit2/a3-r1/` | spec review | second frozen audit of a baseline final spec (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 2 (1 review files) | 212 | small |
| S-246 | `.dev/research/346-review-loop-experiments/p12/baseline-audit2/a3-r2/` | spec review | second frozen audit of a baseline final spec (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 1 (1 review files) | 257 | small |
| S-247 | `.dev/research/346-review-loop-experiments/p12/baseline-audit2/a3-r3/` | spec review | second frozen audit of a baseline final spec (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 2 (1 review files) | 197 | small |
| S-248 | `.dev/research/346-review-loop-experiments/p12/baseline-audit2/a3-r4/` | spec review | second frozen audit of a baseline final spec (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 1 (1 review files) | 266 | small |
| S-249 | `.dev/research/346-review-loop-experiments/p12/baseline-audit2/a3-r5/` | spec review | second frozen audit of a baseline final spec (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 1 (1 review files) | 196 | small |
| S-250 | `.dev/research/346-review-loop-experiments/p12/baseline-audit2/a3-r6/` | spec review | second frozen audit of a baseline final spec (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 2 (1 review files) | 205 | small |
| S-251 | `.dev/research/346-review-loop-experiments/p13/ab1/runs/b1-r1/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 52 (15 review files) | 2457 | large |
| S-252 | `.dev/research/346-review-loop-experiments/p13/ab1/runs/b1-r2/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 47 (15 review files) | 2768 | large |
| S-253 | `.dev/research/346-review-loop-experiments/p13/ab1/runs/b1-r3/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 32 (8 review files) | 2051 | large |
| S-254 | `.dev/research/346-review-loop-experiments/p13/ab1/runs/b1-r4/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 45 (14 review files) | 2649 | large |
| S-255 | `.dev/research/346-review-loop-experiments/p13/ab1/runs/b1-r5/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 38 (15 review files) | 2591 | large |
| S-256 | `.dev/research/346-review-loop-experiments/p13/ab1/runs/b1-r6/` | spec review | ab1 k=3 union+verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 37 (15 review files) | 3247 | large |
| S-257 | `.dev/research/346-review-loop-experiments/p13/ab2/runs/l2-r1/` | spec review | PN2 mechanical lint (p13) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 3 (2 review files) | 249 | small |
| S-258 | `.dev/research/346-review-loop-experiments/p13/ab2/runs/l2-r2/` | spec review | PN2 mechanical lint (p13) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (2 review files) | 344 | medium |
| S-259 | `.dev/research/346-review-loop-experiments/p13/ab2/runs/l2-r3/` | spec review | PN2 mechanical lint (p13) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (2 review files) | 224 | small |
| S-260 | `.dev/research/346-review-loop-experiments/p13/ab2/runs/l2-r4/` | spec review | PN2 mechanical lint (p13) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 5 (3 review files) | 356 | medium |
| S-261 | `.dev/research/346-review-loop-experiments/p13/ab2/runs/l2-r5/` | spec review | PN2 mechanical lint (p13) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (3 review files) | 487 | medium |
| S-262 | `.dev/research/346-review-loop-experiments/p13/ab2/runs/l2-r6/` | spec review | PN2 mechanical lint (p13) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 6 (3 review files) | 452 | medium |
| S-263 | `.dev/research/346-review-loop-experiments/p14/haiku-baseline/runs/a3-r1/` | spec review | Haiku baseline (p14) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 10 (4 review files) | 648 | medium |
| S-264 | `.dev/research/346-review-loop-experiments/p14/haiku-baseline/runs/a3-r2/` | spec review | Haiku baseline (p14) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 12 (4 review files) | 653 | medium |
| S-265 | `.dev/research/346-review-loop-experiments/p14/haiku-baseline/runs/a3-r3/` | spec review | Haiku baseline (p14) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 6 (3 review files) | 448 | medium |
| S-266 | `.dev/research/346-review-loop-experiments/p14/haiku-baseline/runs/a3-r4/` | spec review | Haiku baseline (p14) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 7 (3 review files) | 704 | medium |
| S-267 | `.dev/research/346-review-loop-experiments/p14/haiku-baseline/runs/a3-r5/` | spec review | Haiku baseline (p14) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 10 (3 review files) | 592 | medium |
| S-268 | `.dev/research/346-review-loop-experiments/p14/haiku-baseline/runs/a3-r6/` | spec review | Haiku baseline (p14) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 8 (4 review files) | 550 | medium |
| S-269 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4-r1/` | spec review | ab4 lint + k=2 + clean verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 15 (5 review files) | 643 | medium |
| S-270 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4-r2/` | spec review | ab4 lint + k=2 + clean verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 17 (4 review files) | 590 | medium |
| S-271 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4-r3/` | spec review | ab4 lint + k=2 + clean verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 13 (4 review files) | 657 | medium |
| S-272 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4-r4/` | spec review | ab4 lint + k=2 + clean verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 16 (5 review files) | 860 | medium |
| S-273 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4-r5/` | spec review | ab4 lint + k=2 + clean verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 16 (5 review files) | 777 | medium |
| S-274 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4-r6/` | spec review | ab4 lint + k=2 + clean verify, Sonnet (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 14 (3 review files) | 438 | medium |
| S-275 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4h-r1/` | spec review | ab4 lint + k=2 + clean verify, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 27 (6 review files) | 936 | medium |
| S-276 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4h-r2/` | spec review | ab4 lint + k=2 + clean verify, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 43 (5 review files) | 984 | medium |
| S-277 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4h-r3/` | spec review | ab4 lint + k=2 + clean verify, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 25 (6 review files) | 1048 | medium |
| S-278 | `.dev/research/346-review-loop-experiments/p16/ab4/runs/d4h-r4/` | spec review | ab4 lint + k=2 + clean verify, Haiku (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 18 (5 review files) | 720 | medium |
| S-279 | `.dev/research/346-review-loop-experiments/p16/base-drift/runs/a3d-r1/` | spec review | fresh baseline (base-drift, p16) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 3 (2 review files) | 342 | medium |
| S-280 | `.dev/research/346-review-loop-experiments/p16/base-drift/runs/a3d-r2/` | spec review | fresh baseline (base-drift, p16) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (2 review files) | 350 | medium |
| S-281 | `.dev/research/346-review-loop-experiments/p16/base-drift/runs/a3d-r3/` | spec review | fresh baseline (base-drift, p16) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (3 review files) | 415 | medium |
| S-282 | `.dev/research/346-review-loop-experiments/p16/base-drift/runs/a3d-r4/` | spec review | fresh baseline (base-drift, p16) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 7 (3 review files) | 574 | medium |
| S-283 | `.dev/research/346-review-loop-experiments/p16/base-drift/runs/a3d-r5/` | spec review | fresh baseline (base-drift, p16) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 6 (3 review files) | 585 | medium |
| S-284 | `.dev/research/346-review-loop-experiments/p16/base-drift/runs/a3d-r6/` | spec review | fresh baseline (base-drift, p16) (all runs review orca-worker-contract-spec.md) | 2026-11-09/10 | `Blocking finding ids:` + `verdict: FAIL` | 4 (3 review files) | 491 | medium |

## 4. Rejected (no blocking-flagged findings, or not a review)

Hand-checked rows first, then every `.dev/reflect/*/REPORT.md` and shadow combo REPORT not accepted above (scan = 0 blocking markers; scan covers section, heading and table patterns, see section 9).

| ID | Path | What | Reason |
|---|---|---|---|
| R-H01 | `@E2 .../TASK-WF-design-20261108-041415/ground-truth.json` | E2 control plan, 2 GT defects | 0 items with `blocking_in_implement: true` (control package) |
| R-H02 | `@E2 .../PILOT-REPORT.md`, `@E2 .../COMBO-REPORT.md` (83 and 506 lines) | E2 aggregate scoring reports | no findings of their own; they tabulate counts of S-057..S-079 |
| R-H03 | `@E2 .../20261113-collab/RESULTS-20261114.md`, `counted-results.md` (38, 30 lines) | E2 collaboration-design results | scores only ("found of 14"); raw reviewer transcripts not committed |
| R-H04 | `@E2 .../arms/{A,B}/TASK-WF-designSpec-...` and `arms/A/TASK-WF-makeTheAliasOnly-...` `merged-1.md` | E2 pilot ledgers | 0 blocking ledger rows per PILOT-REPORT ("4 (0)", "9 (0)", "4 (0)") |
| R-H05 | `.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104081732/REPORT.md` | round-2 recheck of S-010 | "merged verdict PASS with notes and no finding is blocking" (round-1 blockers fixed) |
| R-H06 | `.dev/reflect/pre-TASK-WF-implementTheDesi-20261031-182028-shadow11/REPORT.md` | shadow re-audit | 7 MAJOR findings, all `blocking: false` (borderline pool for severity scoring) |
| R-H07 | `.dev/reflect/pre-TASK-WF-authorizedNarrow-20261106-214325-shadow06/REPORT.md`, `...-shadow05`, `...-shadow07` | shadow re-audits | MAJOR/MINOR but `blocking: false` throughout |
| R-H08 | `.dev/releases/backlog/v3.8-task-sc-task-directional-merge/roadmap/validate/validation-report.md`, `.dev/releases/archive/v3.66-tdd-skill-refactor-v2/validate/validation-report.md` | roadmap validation reports | `blocking_issues_count: 0` / "BLOCKING: 0" |
| R-H09 | `.dev/releases/current/WorkflowV3/SPEC-PANEL.md` | spec panel, 31 lines | 3 MAJOR only, no CRITICAL or blocking flag |
| R-H10 | `.dev/releases/current/v5.0.0/QA-LOOP-FINDINGS.md` | research on QA loops | research findings, not a review of a spec or tasklist; "blocking" appears in prose |
| R-H11 | `docs/designs/spec-panel-review-loop.md` | design doc of the review loop | not a review (19 "blocking" hits are design text) |
| R-H12 | `.dev/orca-command-refactor/review/s4-two-part-plan-review.md` | plan review | "PASS. No blocking defect" |
| R-H13 | `.dev/research/346-review-loop-experiments/p12/ab1/runs_superseded/*-contaminated` (3 runs) | superseded contaminated runs | has blocking ids but flagged contaminated; excluded from distinct counts |
| R-H14 | `.dev/research/346-review-loop-experiments/p13/ab1/offline`, `p16/ab4/tests`, `p18/ab5/tests` | test fixtures | fixture copies of reports, not runs |
| R-H15 | `.dev/experiments/346-validation/phase2/S4/`, `S5/baseline-reference/` | research-report QA / implementation final reviews | Kind `other` (see section 5) |
| R-H16 | `.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md` | status `needs_human_decision` | no explicit blocking marker; decision gate only (borderline) |
| R-H17 | `.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md` | review of a spec (patched FR-RH1) | verdict "proceed only with corrected design"; blocking appears only inside requirement text |
| R-H18 | `.dev/reflect/pre-design-20261104164711/REPORT.md` | design plan | verdict ready-with-fixes, 1 HIGH token (borderline, not counted) |
| R-H19 | `.dev/reviews/pr-*`, `.dev/eval-workspaces/sc-auggie-review`, `sc-troubleshoot` | PR / code reviews and troubleshoot evals | code reviews, not tasklist or spec reviews |
| R-H20 | `.dev/tasks/done/TASK-WF-*/artifacts/retries/T*/review-*.md` (about 90 files) | per-task implementation reviews from `/sc:implement` | reviews of code against a task, not of a tasklist or spec |
| R-001| `.dev/reflect/mms-phase-1-postaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L64) |
| R-002| `.dev/reflect/mms-phase-2-postaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L61) |
| R-003| `.dev/reflect/mms-phase-3-postaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L53) |
| R-004| `.dev/reflect/mms-phase-4-postaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L40) |
| R-005| `.dev/reflect/mms-phase-5-postaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L49) |
| R-006| `.dev/reflect/mms-phase-6-postaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L40) |
| R-007| `.dev/reflect/mms-phase-7-postaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L41) |
| R-008| `.dev/reflect/mms-phase-8-postaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L58) |
| R-009| `.dev/reflect/mms-phase-9-postaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L53) |
| R-010| `.dev/reflect/phase-2-r0.1-uc2-validation/REPORT.md` | reflect report | no blocking marker (scan=0; L86) |
| R-011| `.dev/reflect/phase-3-r0.2-uc2-validation/REPORT.md` | reflect report | no blocking marker (scan=0; L120) |
| R-012| `.dev/reflect/post-TASK-RF-20260603-180207-20260603221149/REPORT.md` | reflect report | no blocking marker (scan=0; L67) |
| R-013| `.dev/reflect/post-TASK-RF-20260604-042055-20260604T120400/REPORT.md` | reflect report | no blocking marker (scan=0; L119) |
| R-014| `.dev/reflect/post-TASK-RF-20260604-102137-20260606T020255Z/REPORT.md` | reflect report | no blocking marker (scan=0; L93) |
| R-015| `.dev/reflect/post-TASK-RF-20260607031127-20260607T205947Z/REPORT.md` | reflect report | no blocking marker (scan=0; L68) |
| R-016| `.dev/reflect/post-ccsession-pr123-20260603210238/REPORT.md` | reflect report | no blocking marker (scan=0; L51) |
| R-017| `.dev/reflect/post-cleanup-audit-scope-defaults-20260530031952/REPORT.md` | reflect report | no blocking marker (scan=0; L182) |
| R-018| `.dev/reflect/post-detachTheCcsessi-20261102044547/REPORT.md` | reflect report | no blocking marker (scan=0; L160) |
| R-019| `.dev/reflect/post-initlite-task-20260603233400/REPORT.md` | reflect report | no blocking marker (scan=0; L111) |
| R-020| `.dev/reflect/post-mastra-beads-reconciled-20260603021115/REPORT.md` | reflect report | no blocking marker (scan=0; L108) |
| R-021| `.dev/reflect/post-perPhaseturnBudget-20260619/REPORT.md` | reflect report | no blocking marker (scan=0; L99) |
| R-022| `.dev/reflect/post-perworker-models-20260609/REPORT.md` | reflect report | no blocking marker (scan=0; L40) |
| R-023| `.dev/reflect/post-phase11-r16-20260602/REPORT.md` | reflect report | no blocking marker (scan=0; L57) |
| R-024| `.dev/reflect/post-pr-review-fixes-20260609193019/REPORT.md` | reflect report | no blocking marker (scan=0; L77) |
| R-025| `.dev/reflect/post-pr-submit-defaults-20260616-final/REPORT.md` | reflect report | no blocking marker (scan=0; L65) |
| R-026| `.dev/reflect/post-pr-submit-defaults-20260616-prbranch/REPORT.md` | reflect report | no blocking marker (scan=0; L82) |
| R-027| `.dev/reflect/post-pr-submit-defaults-20260616-prbranch2/REPORT.md` | reflect report | no blocking marker (scan=0; L64) |
| R-028| `.dev/reflect/post-pr-submit-defaults-20260616-rerun/REPORT.md` | reflect report | no blocking marker (scan=0; L80) |
| R-029| `.dev/reflect/post-pr-submit-dehardcode-20260615/REPORT.md` | reflect report | no blocking marker (scan=0; L60) |
| R-030| `.dev/reflect/post-pr111-surgery-20260602185700/REPORT.md` | reflect report | no blocking marker (scan=0; L60) |
| R-031| `.dev/reflect/post-pr132-med-remediation-20260604040600/REPORT.md` | reflect report | no blocking marker (scan=0; L49) |
| R-032| `.dev/reflect/post-pr197-remediation-20260621132712/REPORT.md` | reflect report | no blocking marker (scan=0; L109) |
| R-033| `.dev/reflect/post-pr197-remediation-20260622020900/REPORT.md` | reflect report | no blocking marker (scan=0; L77) |
| R-034| `.dev/reflect/post-prd-document-capture-hotfix-20260607212717/REPORT.md` | reflect report | no blocking marker (scan=0; L52) |
| R-035| `.dev/reflect/post-prd-halt-hard-failure-20260608121957/REPORT.md` | reflect report | no blocking marker (scan=0; L106) |
| R-036| `.dev/reflect/post-prd-local-file-20260609105644/REPORT.md` | reflect report | no blocking marker (scan=0; L85) |
| R-037| `.dev/reflect/post-reflect-cli-wrapper-20260609172031/REPORT.md` | reflect report | no blocking marker (scan=0; L110) |
| R-038| `.dev/reflect/post-reflect-flag-postgate-20260609202335/REPORT.md` | reflect report | no blocking marker (scan=0; L94) |
| R-039| `.dev/reflect/post-remediate-2reg-2drift-20260608194807/REPORT.md` | reflect report | no blocking marker (scan=0; L79) |
| R-040| `.dev/reflect/post-remediation-20260603230600/REPORT.md` | reflect report | no blocking marker (scan=0; L33) |
| R-041| `.dev/reflect/post-rerun-verify-checkpoints-20260606/REPORT.md` | reflect report | no blocking marker (scan=0; L48) |
| R-042| `.dev/reflect/post-reuse-audit-20260607/REPORT.md` | reflect report | no blocking marker (scan=0; L52) |
| R-043| `.dev/reflect/post-sc-recommend-cache-20260603202340/REPORT.md` | reflect report | no blocking marker (scan=0; L46) |
| R-044| `.dev/reflect/post-sprint-auto-resume-promoted-20260603124124/REPORT.md` | reflect report | no blocking marker (scan=0; L65) |
| R-045| `.dev/reflect/post-task-rf-20260608-144157-20260608154913/REPORT.md` | reflect report | no blocking marker (scan=0; L75) |
| R-046| `.dev/reflect/post-task-rf-pr120-20260604033553/REPORT.md` | reflect report | no blocking marker (scan=0; L86) |
| R-047| `.dev/reflect/post-taskfile-rv3low-20260602/REPORT.md` | reflect report | no blocking marker (scan=0; L89) |
| R-048| `.dev/reflect/post-taskrf-cifix-20260604101648/REPORT.md` | reflect report | no blocking marker (scan=0; L94) |
| R-049| `.dev/reflect/post-tool-write-schema-id-sot-20260602/REPORT.md` | reflect report | no blocking marker (scan=0; L52) |
| R-050| `.dev/reflect/post-troubleshoot-hardening-20260611T182100Z/REPORT.md` | reflect report | no blocking marker (scan=0; L89) |
| R-051| `.dev/reflect/post-troubleshoot-hardening-evals-20260612031044/REPORT.md` | reflect report | no blocking marker (scan=0; L79) |
| R-052| `.dev/reflect/post-troubleshoot-pipeline-hardening-20260611T005717Z/REPORT.md` | reflect report | no blocking marker (scan=0; L46) |
| R-053| `.dev/reflect/pr144-comment-reaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L42) |
| R-054| `.dev/reflect/pr144-restore-reaudit/REPORT.md` | reflect report | no blocking marker (scan=0; L101) |
| R-055| `.dev/reflect/pre-TASK-RF-20260604-042055-20260604/REPORT.md` | reflect report | no blocking marker (scan=0; L116) |
| R-056| `.dev/reflect/pre-TASK-WF-addTheSharedCode-20261111-193909-shadow04/REPORT.md` | reflect report | no blocking marker (scan=0; L131) |
| R-057| `.dev/reflect/pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15/REPORT.md` | reflect report | no blocking marker (scan=0; L57) |
| R-058| `.dev/reflect/pre-TASK-WF-applyTheV1Worker-20261107-211837-20261107212538/REPORT.md` | reflect report | no blocking marker (scan=0; L67) |
| R-059| `.dev/reflect/pre-TASK-WF-authorizedNarrow-20261106-214325-shadow06/REPORT.md` | reflect report | no blocking marker (scan=0; L83) |
| R-060| `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/REPORT.md` | reflect report | no blocking marker (scan=0; L190) |
| R-061| `.dev/reflect/pre-TASK-WF-designOutput-20261111-193642-shadow14/REPORT.md` | reflect report | no blocking marker (scan=0; L95) |
| R-062| `.dev/reflect/pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow01/REPORT.md` | reflect report | no blocking marker (scan=0; L125) |
| R-063| `.dev/reflect/pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow03/REPORT.md` | reflect report | no blocking marker (scan=0; L95) |
| R-064| `.dev/reflect/pre-TASK-WF-devGuideFenceFix-20261104-204854-shadow12/REPORT.md` | reflect report | no blocking marker (scan=0; L57) |
| R-065| `.dev/reflect/pre-TASK-WF-enforceTheOwnerP-20261108-031809-20261108033529/REPORT.md` | reflect report | no blocking marker (scan=0; L243) |
| R-066| `.dev/reflect/pre-TASK-WF-fixIssue412SVeri-20261106-215543-shadow13/REPORT.md` | reflect report | no blocking marker (scan=0; L81) |
| R-067| `.dev/reflect/pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05/REPORT.md` | reflect report | no blocking marker (scan=0; L57) |
| R-068| `.dev/reflect/pre-TASK-WF-implementFrOnb1O-20261023-180618-shadow10/REPORT.md` | reflect report | no blocking marker (scan=0; L83) |
| R-069| `.dev/reflect/pre-TASK-WF-implementStages0-20261111-202912-20261111203500/REPORT.md` | reflect report | no blocking marker (scan=0; L40) |
| R-070| `.dev/reflect/pre-TASK-WF-implementTheDesi-20261031-182028-shadow11/REPORT.md` | reflect report | no blocking marker (scan=0; L107) |
| R-071| `.dev/reflect/pre-TASK-WF-planTheExplicitl-20261110-024937-shadow08/REPORT.md` | reflect report | no blocking marker (scan=0; L58) |
| R-072| `.dev/reflect/pre-TASK-WF-planTheRealBound-20261107-080351-20261108-rerun/REPORT.md` | reflect report | no blocking marker (scan=0; L111) |
| R-073| `.dev/reflect/pre-TASK-WF-renameTheScIssue-20261104-174359-shadow07/REPORT.md` | reflect report | no blocking marker (scan=0; L109) |
| R-074| `.dev/reflect/pre-TASK-WF-rollOutTheIssueW-20261109-000305-20261109000839/REPORT.md` | reflect report | no blocking marker (scan=0; L115) |
| R-075| `.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104081732/REPORT.md` | reflect report | no blocking marker (scan=0; L296) |
| R-076| `.dev/reflect/pre-TASK-WF-spec-20261019-204314-20261019204736/REPORT.md` | reflect report | no blocking marker (scan=0; L179) |
| R-077| `.dev/reflect/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/REPORT.md` | reflect report | no blocking marker (scan=0; L68) |
| R-078| `.dev/reflect/pre-canonical-brainstorm-taskfile-20260604050508/REPORT.md` | reflect report | no blocking marker (scan=0; L89) |
| R-079| `.dev/reflect/pre-cosmos-pr-submit-20261016-204642/REPORT.md` | reflect report | no blocking marker (scan=0; L23) |
| R-080| `.dev/reflect/pre-design-20261104164711/REPORT.md` | reflect report | no blocking marker (scan=0; L534) |
| R-081| `.dev/reflect/pre-detachTheCcsessi-20261102035312/REPORT.md` | reflect report | no blocking marker (scan=0; L129) |
| R-082| `.dev/reflect/pre-fr-rh1-uc2-reachability-20260620-053500/REPORT.md` | reflect report | no blocking marker (scan=0; L48) |
| R-083| `.dev/reflect/pre-init-lite-task-20260603204300/REPORT.md` | reflect report | no blocking marker (scan=0; L79) |
| R-084| `.dev/reflect/pre-pass-recovered-predicates-20260605011031/REPORT.md` | reflect report | no blocking marker (scan=0; L60) |
| R-085| `.dev/reflect/pre-pr-submit-ci-monitor/REPORT.md` | reflect report | no blocking marker (scan=0; L66) |
| R-086| `.dev/reflect/pre-pr112-111-remediation-20260602/REPORT.md` | reflect report | no blocking marker (scan=0; L85) |
| R-087| `.dev/reflect/pre-pr124-tasklist-20260604035221/REPORT.md` | reflect report | no blocking marker (scan=0; L54) |
| R-088| `.dev/reflect/pre-pr128-handoff-20260604035139/REPORT.md` | reflect report | no blocking marker (scan=0; L44) |
| R-089| `.dev/reflect/pre-reflect-cli-wrapper-20260609/REPORT.md` | reflect report | no blocking marker (scan=0; L98) |
| R-090| `.dev/reflect/pre-renameTheScIssue-20261104174640/REPORT.md` | reflect report | no blocking marker (scan=0; L112) |
| R-091| `.dev/reflect/pre-rerun-verify-checkpoints-20260606/REPORT.md` | reflect report | no blocking marker (scan=0; L56) |
| R-092| `.dev/reflect/pre-revisedPlanRefac-20261102214256/REPORT.md` | reflect report | no blocking marker (scan=0; L293) |
| R-093| `.dev/reflect/pre-rv3-med-tasklist-20260602-172834/REPORT.md` | reflect report | no blocking marker (scan=0; L65) |
| R-094| `.dev/reflect/pre-signalb-pass-recovered-20260604120512/REPORT.md` | reflect report | no blocking marker (scan=0; L151) |
| R-095| `.dev/reflect/pre-sprint-429-detector-20260702192141/REPORT.md` | reflect report | no blocking marker (scan=0; L77) |
| R-096| `.dev/reflect/pre-sprint-cli-tasklist-revalidate-20260603181005/REPORT.md` | reflect report | no blocking marker (scan=0; L38) |
| R-097| `.dev/reflect/pre-sprint-cli-tasklist-revalidate2-20260603190521/REPORT.md` | reflect report | no blocking marker (scan=0; L27) |
| R-098| `.dev/reflect/pre-sprint-resume-remediation-20260603005500/REPORT.md` | reflect report | no blocking marker (scan=0; L72) |
| R-099| `.dev/reflect/pre-task-rf-194013-20260609103200/REPORT.md` | reflect report | no blocking marker (scan=0; L127) |
| R-100| `.dev/reflect/pre-tavily-built-tasklist-20260623110824/REPORT.md` | reflect report | no blocking marker (scan=0; L98) |
| R-101| `.dev/reflect/pre-troubleshoot-pipeline-hardening-20260611T022748Z/REPORT.md` | reflect report | no blocking marker (scan=0; L72) |
| R-102| `.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md` | reflect report | no blocking marker (scan=0; L270) |
| R-103| `.dev/reflect/pre-uc2-reachability-tdd-20260620000727/REPORT.md` | reflect report | no blocking marker (scan=0; L132) |
| R-104| `.dev/reflect/r1-1-uc2-validation/REPORT.md` | reflect report | no blocking marker (scan=0; L164) |
| R-105| `.dev/reflect/r1-2-uc1-validation/REPORT.md` | reflect report | no blocking marker (scan=0; L152) |
| R-106| `.dev/reflect/r1-4-9.9-uc2-validation/REPORT.md` | reflect report | no blocking marker (scan=0; L90) |
| R-107| `.dev/reflect/roadmap-rewrite-uc1-validation/REPORT.md` | reflect report | no blocking marker (scan=0; L190) |
| R-108| `.dev/reflect/uc2-tier1-TASK-RF-20260529-171029/REPORT.md` | reflect report | no blocking marker (scan=0; L299) |
| R-109| `.dev/reflect/uc2-tier2-TASK-RF-20260529-171029/REPORT.md` | reflect report | no blocking marker (scan=0; L263) |
| R-110| `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboB-r1/REPORT.md` | shadow combo run, same frozen plan as S-045..S-056 | 0 blocking (merged and reviewer cards) |
| R-111| `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboB-r3/REPORT.md` | shadow combo run, same frozen plan as S-045..S-056 | 0 blocking (merged and reviewer cards) |
| R-112| `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/REPORT.md` | shadow combo run, same frozen plan as S-045..S-056 | 0 blocking (merged and reviewer cards) |

## 5. Other (research-report QA), fallback pool

| ID | Path | Kind | What was reviewed | Date | Blocking marker used | Approx. blocking-flagged findings (method) | Lines | Read cost |
|---|---|---|---|---|---|---|---|---|
| O-001 | `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/` (139 files) | other (research-report QA) | run-2 research report of the unified Review Panel | 2026-11-14 | `Verdict: FAIL (N blocking, M minor)`, `F_0`/`F_1` cycle counts, `grading-override.md` | >=63 (stated numbers in 26 of 139 files; lower bound, many FAIL files give no number) | 26906 | large |
| O-002 | `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/qa/` (92 files) | other (research-report QA) | run-1 research report of the unified Review Panel | 2026-11-13 | `Verdict: FAIL (N IMPORTANT / blocking)`, CRITICAL/IMPORTANT/MINOR | >=111 (stated in 32 of 92 files; lower bound) | 18661 | large |
| O-003 | `.../run2-20261114-075454/qa/analyst-cross-validation-report-2.md` | other | run-2 cross-validation | 2026-11-14 | `FAIL (6 blocking, 7 minor)` | 6 (stated) | 131 | small |
| O-004 | `.../run2-20261114-075454/qa/analyst-cross-validation-report-3.md` | other | run-2 cross-validation | 2026-11-14 | `FAIL (4 blocking, 9 minor)` | 4 (stated) | 195 | small |
| O-005 | `.../run2-20261114-075454/qa/qa-synthesis-qualitative-report-2.md` | other | run-2 synthesis QA | 2026-11-14 | `FAIL (5 blocking findings)` | 5 (stated) | 57 | small |
| O-006 | `.../run2-20261114-075454/qa/qa-task-validation-structure-report.md` | other | run-2 task-file validation | 2026-11-14 | `FAIL (4 blocking IMPORTANT issues, 0 CRITICAL; 6 MINOR)` | 4 (stated) | 74 | small |
| O-007 | `.../run2-20261114-075454/qa/analyst-completeness-report-2.md`, `analyst-synthesis-accuracy-2.md`, `analyst-synthesis-tracing-2.md`, `qa-synthesis-content-report-2.md`, `qa-research-qualitative-report-3.md` | other | run-2 analyst and QA reports | 2026-11-14 | `FAIL (N blocking)` | 2 + 3 + 3 + 3 + 3 = 14 (stated) | 140 + 166 + 73 + 118 + 75 = 572 | medium |
| O-008 | `.../run2-20261114-075454/qa/qa-anti-omission-enumeration-3.md` | other | run-2 anti-omission enumeration | 2026-11-14 | `verdict FAIL with 4 BLOCKING and 10 MINOR` | 4 (stated) | 4175 | large |
| O-009 | `.../unify-20261113-155942/qa/analyst-synthesis-tracing-1.md` | other | run-1 tracing | 2026-11-13 | `FAIL. 5 blocking findings (2 CRITICAL, ...)` | 5 (stated) | 134 | small |
| O-010 | `.../unify-20261113-155942/qa/analyst-synthesis-accuracy-2.md`, `analyst-synthesis-tracing-2.md`, `analyst-completeness-report-2.md` | other | run-1 analyst reports | 2026-11-13 | `FAIL (5 IMPORTANT)`, `4 IMPORTANT blocking`, `2 blocking` | 5 + 4 + 2 = 11 (stated) | 138 + 176 + 150 = 464 | medium |
| O-011 | `.../unify-20261113-155942/qa/qa-lens-recommendation-feasibility-b.md`, `qa-lens-implementation-concreteness-b.md` | other | run-1 lens QA | 2026-11-13 | `FAIL (7 important; blocking)`, `FAIL (6 important)` | 7 + 6 = 13 (stated) | 44 + 35 = 79 | small |
| O-012 | `.../unify-20261113-155942/qa/qa-consolidated-findings-phase3.md`, `-phase5.md`, `-phase6.md`, `qa-qualitative-consolidated.md` | other | run-1 consolidated gates | 2026-11-13 | `N blocking, M minor` | 2 + 2 + 2 + 3 = 9 (stated) | 74 + 111 + 103 + 34 = 322 | medium |
| O-013 | `.dev/tasks/to-do/TASK-TDD-20260619-235400/qa/`, `.dev/tasks/to-do/TASK-TDD-20260621-124414/qa/` (about 60 files) | other (research-report QA) | TDD research and synthesis tasks | 2026-06-19/21 | rf-qa `CRITICAL/IMPORTANT/MINOR`, `Verdict: FAIL` | not counted (grep token only) | ~5000 | large |
| O-014 | `.dev/tasks/to-do/TASK-RF-*/qa/qa-research-*`, `qa-qualitative-*`, `qa-report-*` (many tasks) | other | research-gate and report QA of MDTM tasks | 2026-06 to 2026-11 | same rf-qa scheme | not counted | n/a | large |
| O-015 | `.dev/experiments/346-validation/phase2/S4/evidence/baseline-qa-outputs/` and `phase2/S5/baseline-reference/R1..R4-reviewer-final-report*.txt` | other | BMAD research-report QA (S4); four final reviews of a P0 live-check package (S5) | 2026-11-04/07 | `CRITICAL/IMPORTANT`; S5 "1, 2, 1, 0 blocking" by round | S5: 4 blocking in 4 reviews (stated in ANALYSIS.md) | ~900 | medium |
| O-016 | `.dev/tasks/done/TASK-RESEARCH-review-loops-20261023-032537/` (277 QA/review files) | other | research on review loops | 2026-10-23 | rf-qa scheme | not counted | n/a | large |

## 6. Totals and answers

### 6.1 Totals by Kind

| Kind | Sources (rows) | Sum of blocking-flagged findings | Notes |
|---|---|---|---|
| tasklist review | 80 rows (S-001..S-036, S-045..S-088) | 1,397 | of which 15 E2 reviewer-report pools hold 1,128 (S-065..S-079) and ground-truth/pilot rows hold 15; **excluding those: 57 sources, 254 findings** |
| tasklist review (post-execution audit) | 8 rows (S-037..S-044) | 13 | owner may reclassify as `other` |
| spec review | 110 sources (26 rows S-089..S-114 plus 84 runs S-201..S-284) | 1,732 | S-105/S-106 (537) are a pre-extraction of the same runs; **excluding them: 108 sources, 1,195 findings** (185 in the 24 hand rows, 1,010 ids in the 84 runs) |
| other (research-report QA, section 5) | 16 rows covering about 231 QA files in two main folders | >=174 for the two main folders (lower bound), +4 (S5) | fallback pool |

Counts are estimates unless marked stated or VERIFIED. Different markers are not commensurable (a `blocking: true` flag, an `IMPORTANT` severity and a `HIGH` token all count as 1).

### 6.2 Are there at least 30 distinct runs or reports with at least 1 blocking finding among tasklist plus spec reviews?

**Yes.** Exact count of rows with at least 1 blocking-flagged finding: **165** (57 tasklist + 24 hand-listed spec + 84 spec-loop runs), or **173** when the 8 post-execution audits are included. Excluded from that number: the E2 reviewer-report pools, the E2 ground-truth and pilot rows, and the pre-extracted p17 files, which would only add overlap.

Honest caveat on "distinct": the 165 are distinct runs or reports, but not distinct documents. Roughly 34 different tasklists or plans stand behind S-001..S-044, 1 plan behind S-045..S-056 (and E2 uses 3 plans), 5 MDTM task files behind S-084..S-088, and the 84 spec-loop runs all review one spec. If "distinct" means distinct reviewed document, the count is roughly 45 tasklist/plan documents (estimate) and 10 spec or design documents (orca spec, launch-hook plan, 5 release specs, 3 reflect-reviewed specs). The `other` pool is not needed to reach 30 (it would add 16 rows and at least 178 stated findings).

### 6.3 Proposed split into 10 batches

Rules: each batch reads at most 2,500 lines. Where a source is larger than its budget, the analyst reads only the budget (start with the blocking-marked sections; for the E2 pools read the first 5 reviewer files containing `"blocking":true`; for S-105 read the first 40 jsonl rows; for S-102..S-104 read the files holding `Blocking finding ids:`). Every batch has tasklist (T) and spec (S) sources. Loads are in budgeted lines.

| Batch | Load | Tasklist sources | Spec sources |
|---|---|---|---|
| B01 | 2412 | S-002 (450), S-066 (200), S-071 (200), S-035, S-042, S-058, S-003, S-081 | S-238 (450), S-279 (342), S-107 (260) |
| B02 | 2394 | S-004 (450), S-045, S-018, S-041, S-017, S-008, S-023 | S-241 (450), S-108 (304), S-090 (283) |
| B03 | 2378 | S-005 (450), S-048 (300), S-020, S-001, S-026 | S-251 (450), S-102 (300), S-257, S-093, S-114 |
| B04 | 2393 | S-006 (450), S-050 (300), S-055, S-016, S-021, S-014, S-034 | S-263 (450), S-103 (300), S-095 |
| B05 | 2397 | S-056 (300), S-046, S-083, S-007 | S-201 (450), S-269 (450), S-104 (300), S-245, S-098, S-113 |
| B06 | 2398 | S-088 (300), S-057, S-054, S-022, S-024, S-013 | S-215 (450), S-275 (450), S-105 (300), S-089, S-112 |
| B07 | 2400 | S-049, S-051, S-011, S-009, S-033, S-080, S-012 | S-221 (450), S-282 (450), S-097 (300), S-100 |
| B08 | 2395 | S-076 (200), S-038, S-027 | S-225 (450), S-235 (424), S-209 (346), S-091, S-110, S-205, S-094 |
| B09 | 2376 | S-069 (200), S-079 (200), S-032, S-010, S-019, S-082 | S-227 (450), S-203 (423), S-111 (374), S-099 |
| B10 | 2386 | S-025, S-015, S-037, S-040 | S-231 (450), S-106 (400), S-109 (378), S-096, S-092, S-101 |

Total budgeted: 23,929 lines over 103 sources (57 tasklist + 46 spec).

Reserve for a second wave (not in the 10 batches): S-028..S-031, S-036, S-039, S-043, S-044, S-047, S-052, S-053, S-059..S-065, S-067, S-068, S-070, S-072..S-075, S-077, S-078, S-084..S-087, and the 64 spec-loop runs not named above (S-202, S-204, S-206..S-208, S-210..S-214, S-216..S-220, S-222..S-224, S-226, S-228..S-230, S-232..S-234, S-236, S-237, S-239, S-240, S-242..S-244, S-246..S-250, S-252..S-256, S-258..S-262, S-264..S-268, S-270..S-274, S-276..S-278, S-280, S-281, S-283, S-284). If more diversity of spec documents is wanted, prefer S-107..S-114 and the orca originals over more loop runs.

## 7. Verification log (counts confirmed by opening the file)

Confirmed by reading the report section, heading list or id lines: S-001 (8 MF headings), S-003 (8 in section), S-004 (D-03, D-05, INV-001/002), S-005 (D-001 plus INV-002), S-006 (D-001, D-016), S-007 (B-1..B-4), S-008 (C1..C3), S-009 (M-1..M-4), S-020 (M-F1..M-F3), S-021 (D-001 plus 3 HIGH invariants), S-022 (C1..C5), S-037 (DEV-1..3), S-038 (NEW-R1), S-040 (frontmatter regression: 2), S-048 (F1..F3), S-050 (M-1, M-2), S-045 (MF1, MF2), S-057/S-058 (GT 5 of 10 and 3 of 4; design control 0 of 2), S-080..S-082 (11, 7, 10 distinct ids), S-089..S-093 and S-095..S-097 (stated verdict lines), S-201 (19 ids across 4 files: 1 + 6 + 4 + 8), plus the E2 `findings-v1` format on one sample reviewer file. That is 30 confirmations. Estimates (not opened in full): S-015, S-016, S-028..S-031, S-039, S-041, S-084..S-087, S-100, S-102, S-107..S-111 and every `>=` figure.

## 8. Blocking-marker conventions found

| # | Convention | Where used | Example path |
|---|---|---|---|
| 1 | `findings-v1` record with `"severity":"MAJOR"` and `"blocking":true|false` (JSON line or YAML `blocking: true`) | E2 reviewer files, shadow-combo reviewer cards, merged verdict yaml | `@E2 .../TASK-WF-design-20261108-041415/reviews/combos/b4-muse-luna2/t3-1.md`; `.dev/reflect/pre-TASK-WF-implementFrOnb1O-20261023-180618-shadow10/adversarial/merged-verdict.yaml` |
| 2 | Heading with `(blocking)`, `BLOCKING` or `(MAJOR, blocking)`; finding ids `MF-01`, `B-1`, `D-001`, `M-F1`, `Cn` | reflect pre reports | S-001, S-009, S-020 |
| 3 | A `## Blocking findings` or `## CRITICAL findings` or `## HIGH - must resolve before execution` section | reflect pre reports | S-007, S-023, S-024 |
| 4 | Table column `blocking` / `should-fix` / `minor` | reflect pre reports | S-011 |
| 5 | Reviser brief line `Blocking finding ids: B-01, ...` and last line `verdict: FAIL` | spec-panel loop reports of the #346 experiments | S-201 (`.dev/research/346-review-loop-experiments/p11/runs/a1-r1/aud/ws/.dev/orca-command-refactor/review/audit.md`) |
| 6 | Binary severity rule of the original spec-panel: CRITICAL / MAJOR / MINOR, any finding fails (`**FAIL.** 24 findings: 3 CRITICAL, 15 MAJOR, 6 MINOR`) | original orca spec review | S-089 |
| 7 | PR #343 style `BLOCKING:` / `minor` gradings (`### B1. BLOCKING: ...`, "2 blocking, 11 minor") | review loop rounds 4-5 | S-092 |
| 8 | Invariant probe `INV-nnn (HIGH)` treated as blocking by the skill gate; "BLOCKED_BY_INVARIANTS" | adversarial merge in reflect | S-021, S-015 |
| 9 | Reflect deviation taxonomy (Drift / Regression / Necessary / Authorized) with severity HIGH / MEDIUM / LOW; `regression_present: true`; `deviation_count_by_class` | reflect post audits | S-037, S-040 |
| 10 | Old reflect severity `critical` / `important` / `minor` | Oct 2026 reflect reports | S-028 |
| 11 | rf-qa `CRITICAL` / `IMPORTANT` / `MINOR` issue tables with `Overall Verdict: FAIL` | MDTM task-file QA | S-084 (`.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/qa/`) |
| 12 | Priority scale `P1` / `P2` / `P3` (P1 = must fix) | P2 static plan report | S-004 |
| 13 | Ground-truth flag `"blocking_in_implement": true` (real defect that would block implementation) | E2 ground truth | S-057 |
| 14 | `verdict FAIL (N blocking, M minor)` plus `F_0`, `F_1` cycle counts and a `grading-override.md` | research-report QA | O-001, O-003 |
| 15 | Spec-panel `CRITICAL` / `HIGH` / `MAJOR` finding tables (no blocking word) | older release spec-panel reviews | S-107 |
| 16 | `defects[].severity: blocking|medium|minor` (clustered ledger) | p17 ledger | S-106 |

Analyst warnings: (a) a finding can be flagged blocking "as filed" by a reviewer and downgraded by the adversarial debate (S-049, S-055, S-056); record both. (b) Headings such as `(MAJOR, blocking: no)` carry the word blocking but are NOT blocking. (c) Words like `non-blocking`, `0 blocking`, `pipeline-blocking` appear in many non-blocking contexts.

## 9. Limits and honesty notes

- Counts for S-015, S-016, S-028..S-031, S-039, S-084..S-087, S-100, S-102, S-107..S-111 are token or table-row estimates and may be off by a factor of two. The 84 spec-loop run counts come from a parser (`ids_from` of `central/score_themes.py`) over deduplicated review files; they include the same finding raised in several rounds and audits, so they overstate distinct defects. p17 shows 511 blocking findings clustering into 58 defects (26 blocking).
- The scan of `.dev/reflect/*/REPORT.md` for the Rejected table used section, heading and table patterns only; a report with an unconventional marker could be missing from section 1 (borderline cases are noted in R-H16..R-H18).
- Not inspected in depth: `~/.claude/projects/**/subagents` (not needed), `.dev/brainstorms/*` debate files (no blocking-flagged review reports found), `.dev/troubleshoot/*` (code and bug reports), the E2 `scoring/combos` judge files (1,240 files of scores, not reviews).
- Nothing was checked out, fetched, pulled, stashed, committed or pushed. Temporary helper files were written only under `/tmp`.

Status: Complete
