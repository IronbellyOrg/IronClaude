# Diff Analysis: Reviewer-card comparison (UC-1 plan-vs-spec audit)

Short paths used below. PLAN = `.dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md`. SPEC = `.dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/source.md`. V1 = variant-1-original.md (reviewer-1-card, haiku-class analyzer). V2 = variant-2-original.md (reviewer-2-card, opus-class qa). Row numbers `V1#n` / `V2#n` are the numbers in each card's own Deviations table.

## Metadata
- Generated: 2026-11-26
- Variants compared: 2
- Total differences found: 31 (diff points)
- Categories: structural (5), content (18), contradictions (4), unique (6), shared assumptions (4)
- Grading rule for the merged result is supplied by the caller (Blocking = Decision / Missing / Safety; Medium; Note) and overrides each card's own labels.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Size and breadth | 3 rows; spec units audited 20 | 18 rows; spec units audited 19 | Low |
| S-002 | Grade vocabulary | Writes "Blocking (Missing)" inside the prose and a separate HIGH/MEDIUM severity column; a row can read "Blocking" with severity MEDIUM | Writes "Blocking (Decision/Missing/Safety)", "Medium", "Note" inside the prose and a HIGH/MEDIUM/LOW column | Medium |
| S-003 | Category labels | Regression (1 row), Drift (2 rows) | Drift (16), Authorized expansion (1), Necessary deviation (1) | Low |
| S-004 | Adherence accounting | 17 of 20 units "fully adherent at plan level" | 10 of 19 units fully adherent | Medium |
| S-005 | Supporting sections | Notes only (evidence pathology, no commands run) | Notes plus a coverage-matrix audit, a "can each acceptance check pass or fail" pass, and a list of checked-and-correct citations | Low |

## Content Differences

Taxonomy tag in brackets (L1 surface, L2 structural, L3 state-mechanics).

| # | Topic | Variant 1 | Variant 2 | Severity |
|---|-------|-----------|-----------|----------|
| C-001 [L3] | The counting rule used by Phase 1 tests is a test-local copy (`questions_for`, `read_notes`); scenarios for empty, mixed, multiple-contradiction and three of four categories are not exercised against the shipped protocol by Phase 3 | V1#1 Regression, "Blocking (Missing)", HIGH; PLAN:47-62, 68-81, 121-123, 138-141, 154; SPEC:23, 35, 43 | V2#4 Drift, "Blocking (Decision)", HIGH; PLAN:47, 61, 81, 122-123, 139-141, 154, 175; SPEC:23, 35 | High |
| C-002 [L3] | No "revisit the estimate / stop and report to the lead" step when the isolated runner cannot intercept questions or GitHub posts | V1#2 Drift, "Blocking (Missing)", MEDIUM; PLAN:95-104; SPEC:35 | V2#5 Drift, "Blocking (Missing)", HIGH; PLAN:90, 98, 171; SPEC:35 | High |
| C-003 [L2] | Issue-state re-check (SPEC says the orchestrator must re-check that issue 834 is closed) is not a task | V1#3 Drift, "Blocking (Missing)", MEDIUM; PLAN:24, 176, 195; SPEC:11 | V2#8 Drift, Medium; PLAN:24, 176, 195; SPEC:11 | Medium |
| C-004 [L2] | PLAN:171 says the six acceptance criteria are "quoted in `./source.md`"; SPEC only paraphrases them; the quoted text is in `.dev/issues/834/accuracy-check.md:16-21` and the SPEC:33 link does not resolve inside the package; Task 9's AC4 citation list leaves out the claim files | Only noted as "evidence pathology" (links do not resolve), no finding | V2#1 Drift, "Blocking (Decision)", HIGH | High |
| C-005 [L3] | Runs have an expected question count but no expected `issue create` count; a plain-text question that never posts would show 0 questions | Not raised | V2#2 "Blocking (Decision)", HIGH; PLAN:122-123, 128-131, 148, 90, 108; SPEC:11 | High |
| C-006 [L3] | The plan never names which answer a contradiction run supplies nor what observable proves it was applied | Not raised | V2#3 "Blocking (Decision)", HIGH; PLAN:131, 90, 143 | High |
| C-007 [L3] | SAFETY: "No GitHub writes of any kind" (PLAN:22) is enforced only for the `gh` binary; other write channels (git push through a credential helper, GitHub-capable MCP server) are not blocked or checked; raw event logs are staged with no secret scan | Not raised | V2#6 "Blocking (Safety)", unverified, HIGH; PLAN:22, 91, 108, 132, 159; CLAUDE.md:37; .gitignore:85 | High |
| C-008 [L2] | No task checks that claim direct posting, staged recommendation and the worktree-only plan-approval boundary are preserved (AC4); Task 9 citation list omits those files | Not raised | V2#7 Medium; PLAN:171, 175, 21; SPEC:26 | Medium |
| C-009 [L3] | Preserved-flag run description starts "Feature:" while the flag is `--mode bug`; the user's own words contradict the user's own flag, so a "reversed choice" question is possible and would be misrecorded | Not raised | V2#9 Medium; PLAN:141, 154, 148 | Medium |
| C-010 [L2] | Task 9 must give an AC6 verdict ("the gates plus the monitored pull request") before Task 10 runs the gates and before any pull request exists | Not raised | V2#10 Medium; PLAN:165, 171, 182, 195 | Medium |
| C-011 [L2] | The stop rule for an unknown `gh` call or uninterceptable write sits only in Task 8's acceptance criteria; Tasks 6, 7, 8 each depend only on Task 5 | Not raised | V2#11 Medium; PLAN:119, 136, 152-159, 132 | Medium |
| C-012 [L2] | Generator-Constraint check uses `git diff --name-only origin/integration`, which misses untracked new files and lists upstream drift | Not raised | V2#12 Medium; PLAN:200 | Medium |
| C-013 [L1] | PLAN:92 says the synthetic false fact of "Task 7" depends on the scripts listing; it is first used in Task 6 | Not raised | V2#13 Note; PLAN:92, 123 | Low |
| C-014 [L1] | PLAN:23 says the installed copy is "the pre-852 version" and lists `refs/claim.md` among the differences | Not raised | V2#14 Note; PLAN:23 | Low |
| C-015 [L2] | The notes reader is not told to ignore the HTML comment block in each section | Not raised | V2#15 Note; PLAN:33 | Low |
| C-016 [L2] | The Wave 2 sentence the preserved-flag test looks for appears twice in `refs/create.md` (lines 38 and 86); a whole-file check passes even if the Wave 2 copy is removed | Not raised | V2#16 Note; PLAN:73, 78 | Low |
| C-017 [L2] | Harness, drift guards, incomplete-line cases, secret-material scenario go beyond the lead's scenario list | Notes: not judged unauthorized expansion | V2#17 Authorized expansion, Note; PLAN:35, 72, 74 | Low |
| C-018 [L2] | The secret-material exception has no controlled run | Not raised | V2#18 Necessary deviation, Note; PLAN:169 | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Category of the self-testing counting rule | Regression | Drift | Low |
| X-002 | Grade of the missing issue-state re-check | "Blocking (Missing)" (V1#3) | Medium (V2#8) | Medium |
| X-003 | Severity of the missing estimate revisit | Row says Blocking but severity column MEDIUM (V1#2); V1 summary counts it as Drift | HIGH (V2#5) | Low |
| X-004 | How much of the plan adheres | 17 of 20 units adherent (3 gaps) | 10 of 19 units adherent (9 gaps) | Medium |

Evidence: X-001 V1:19 vs V2:23. X-002 V1:21 vs V2:27. X-003 V1:20 vs V2:24. X-004 V1:26 vs V2:41-42.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V2 | Safety finding on non-gh write channels and unscanned staged logs (C-007) | High |
| U-002 | V2 | Post-count and answer-applied observability gaps (C-005, C-006) | High |
| U-003 | V2 | Criterion-text pointer error and link break (C-004) | Medium |
| U-004 | V2 | Ordering defect AC6-before-gates (C-010) and CI-rule method (C-012) | Medium |
| U-005 | V2 | Coverage-matrix audit: which INF rows the plan really covers, and testability of each task | Medium |
| U-006 | V1 | Concise statement that the plan's own admission (PLAN:81 docstring) does not supply the missing executable coverage | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|-----------|----------------|----------|
| A-001 | C-003 (both flag the missing re-check) | "The orchestrator" in SPEC:11 who "must re-check that state" is the executor of this plan, not the upstream claim orchestrator that wrote the summary | UNSTATED | Yes |
| A-002 | C-001 (both flag self-testing) | SPEC:43 item (1), the regression tests, must itself exercise the shipped protocol; the plan's split into Phase 1 contract tests plus Phase 3 runs does not satisfy it | UNSTATED | Yes |
| A-003 | all rows | The plan and spec line numbers quoted in both cards match the live files and the quoted plan text is accurate | UNSTATED | Yes |
| A-004 | C-001, C-004 (both cite the linked analysis files) | The files linked at SPEC:32-33 (`analysis/analyze-sc-issue-protocol.md`, `accuracy-check.md`) carry requirement force for the plan (V2 cites them as requirements; V1 anchors only to SPEC and PLAN) | UNSTATED | Yes |

### Promoted [SHARED-ASSUMPTION] diff points

| # | Assumption | Impact | Status |
|---|-----------|--------|--------|
| A-001 | SPEC:11 re-check is the plan executor's job | Decides whether C-003 is Blocking or Medium | Open |
| A-002 | Phase 1 must exercise the shipped protocol | Decides C-001 grade | Open |
| A-003 | Line numbers and quotes in the cards are accurate | Every grade | Open |
| A-004 | Linked analysis files bind the plan | Decides C-001, C-004, C-005 evidence weight | Open |

## Summary
- Total structural differences: 5
- Total content differences: 18
- Total contradictions: 4
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 4, STATED: 0, CONTRADICTED: 0)
- total_diff_points (S + C + X + A) = 31
- Highest-severity items: C-001, C-002, C-004, C-005, C-006, C-007
