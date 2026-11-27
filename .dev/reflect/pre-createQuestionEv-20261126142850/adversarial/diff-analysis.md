# Diff Analysis: UC-1 reviewer-card Comparison (plan TASK-WF-createQuestionEv-20261126-142533 vs its spec)

Short paths: PLAN = .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/TASK-WF-createQuestionEv-20261126-142533.md, SPEC = the source.md beside it. Cards: V1 = variant-1-original.md (reviewer 1, haiku-class analyzer, 3 deviations), V2 = variant-2-original.md (reviewer 2, opus-class qa, 22 deviations). "V1-n" and "V2-n" are the finding numbers in each card's own table.

Debate question: which findings are real, which overstated or wrong, and the right grade of each by consequence, under the brief's grading rule (Blocking only for Decision / Missing / Safety; real defect in substance that nothing named rests on is Medium; form-only is Note; a defect in the plan's own choices that makes a stated check fail or become unrunnable is Blocking (Decision) or (Missing)).

## Metadata
- Generated: 2026-11-26 (orchestrator pass; variant copies are variant-1-original.md and variant-2-original.md)
- Variants compared: 2
- Total differences found: 4 structural, 19 content, 4 contradictions, 5 unique, 3 shared assumptions
- Categories: structural (4), content (19), contradictions (4), unique (5), shared assumptions (3)
- Orchestrator pre-verification (read myself, before the debate): origin_repo.py:156-174 and :66-69 (only `https://github.com/` and `git@github.com:` origins parse); refs/create.md:7, 32, 38, 59, 84-86, 98-99; templates/draft-notes.md:3-15; SKILL.md:100; issue-worker-t1/t2/t3.md:33; CLAUDE.md:37; `git rev-list --count HEAD..origin/integration` = 51 and `git log HEAD..origin/integration` over the three AC4 files = empty, `git diff origin/integration -- <3 files>` = empty today.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Card size and scope | 3 findings, all on spec-required deliverables (R-006, R-013, R-019) | 22 findings: 4 Blocking, 12 Medium, 6 Note | Medium |
| S-002 | Category vocabulary | Only Drift and Regression used | Drift, Regression, Necessary deviation, Authorized expansion all used | Low |
| S-003 | Adherence reporting | Requirement-by-requirement table R-001 to R-024 (21 resolved) | Counts 14 of 24 R-units fully adherent; adds the 12 prohibitions one by one, a coverage-matrix audit and a per-task "can the AC pass or fail" audit | Medium |
| S-004 | Label vs severity column | Row text says "Blocking (Missing)" while the severity column says MEDIUM (row 1) and HIGH (row 2) | Row text "Blocking (Safety/Decision)" with severity HIGH; "Medium" with MEDIUM; Notes LOW | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Severity |
|---|-------|-----------|-----------|----------|
| C-001 | R-006 `kept without approval:` lines in the addition-disclosure check | V1-1: Blocking (Missing); PLAN:142-150, 195 do not require the line | Not raised; R-006 listed as fully adherent | Medium |
| C-002 | Secret-scan coverage (R-013) | V1-2: Blocking (Missing), PLAN:191 scans only ./artifacts/runs/, feasibility dry-run excerpt (PLAN:96-109) is outside it, Task 11 uses it as the staging prerequisite | V2-13: Medium, same scope gap, also harness/self-test.txt and planted-token folder | High |
| C-003 | AC6 refresh from the pull request (R-019) | V1-3: Blocking (Missing); Task 11 refreshes only from the gate record | V2-14: Medium, same fact | Medium |
| C-004 | Task 4 dry run before any write block exists | Not raised | V2-1: Blocking (Safety); PLAN:104; fake gh and isolated home are built in Task 5 | High |
| C-005 | AC4 diff basis `git diff origin/integration -- <files>` | Not raised | V2-2: Blocking (Decision); compares the working tree with a moved tip | High |
| C-006 | Preserved-flag scenario vs the counting rule | Not raised (R-001 resolved) | V2-3: Blocking (Decision); PLAN:76 counts "the flag as passed" as the second part, PLAN:81 expects zero for a line "without the user's quoted words" | High |
| C-007 | Placement of the staging hold (R-013) | Not raised | V2-4: Blocking (Decision); hold only at PLAN:191 and 234, not in Constraints or Tasks 4-8; CLAUDE.md:37 says always staged | High |
| C-008 | Draft body before the answer (R-005 comparison) | Not raised (R-005 resolved) | V2-5: Medium; no step captures the pre-answer body; fake gh logs only arguments | Medium |
| C-009 | "not evidenced" vs the four verdict words | Not raised | V2-6: Medium; reconciliation not stated | Low |
| C-010 | Expected `issue comment` count per run (R-004) | Not raised (R-004 resolved) | V2-7: Medium; three runs state no comment expectation | Medium |
| C-011 | Task 7 and 8 depend only on Task 5; parallel runs vs matrix stop (R-014) | Not raised | V2-8: Medium | Medium |
| C-012 | Files a run must load: analyze command and adversarial skill missing from Task 4's list | Not raised | V2-9: Medium | Medium |
| C-013 | Model credential in an isolated home vs "never a real credential" | Not raised | V2-10: Medium | Medium |
| C-014 | Fork-activity attribution when other sessions are active | Not raised | V2-11: Medium | Medium |
| C-015 | read-files.txt source of file paths (R-010) | Not raised (R-010 resolved) | V2-12: Medium; reviewer's own understanding, not verified | Medium |
| C-016 | Classifier tests mostly test their own line format (R-002) | Not raised (R-002 resolved) | V2-15: Medium | Medium |
| C-017 | Run clone's fetch URL vs origin_repo.py (Wave 0) | Not raised | V2-16: Medium | Medium |
| C-018 | Stricter-than-spec choices (quick 0 comment; stop on installed-copy read) | Not raised | V2-17, V2-18: Notes, Authorized expansion | Low |
| C-019 | Wording and line-citation items | Not raised | V2-19, 20, 21, 22: Notes (closed-issue tense, claim.md:80 and SKILL.md:86 omitted, builder signature, install-state-dependent self-test check) | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Is R-006 met at plan level? | Not fully resolved (V1 summary: R-006 deviation 1) | Fully adherent (V2 adherence summary lists R-006) | Medium |
| X-002 | Grade of the secret-scan scope gap | Blocking (Missing), severity HIGH (V1-2) | Medium (V2-13), while the neighbouring staging-hold gap is Blocking (Decision) (V2-4) | High |
| X-003 | Grade of the missing AC6 refresh from the pull request | Blocking (Missing), severity MEDIUM (V1-3) | Medium (V2-14) | Medium |
| X-004 | Which R-units are resolved | V1 marks R-001, R-002, R-004, R-005, R-010, R-012, R-014, R-017 resolved | V2 has findings on every one of them (V2-3, 15, 7, 5, 9, 12, 1, 10, 11, 16, 8, 2) | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|-----------------|
| U-001 | V1 | R-006 line-format check gap (V1-1); the only R-006 finding | Medium |
| U-002 | V2 | Task 4 dry-run safety gap (V2-1); the only Safety item | High |
| U-003 | V2 | AC4 diff basis and preserved-flag counting-rule conflict (V2-2, V2-3) | High |
| U-004 | V2 | Check-by-check runnable audit of Tasks 1-11 and prohibition-by-prohibition result | Medium |
| U-005 | V2 | Run environment gaps (V2-9, 10, 11, 16): loaded set, model credential, fork attribution, origin URL | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | Staging, commit and push of the package happen only after Task 9's scan (so a hold stated in Task 9 and Task 11 is enough); neither card shows where the story agent first stages | Both cards accept Task 9 and 11 as the place the hold lives (V1-2, V2-4, V2-13) | UNSTATED (state of the index between Task 4 and Task 9) | High | Promoted |
| A-002 | A literal executor of the plan text, with no knowledge beyond the plan and the repo, is the standard for "runnable as written" (guard against a competent executor repairing gaps ad hoc) | Both cards grade by literal reading | UNSTATED | Medium | Promoted |
| A-003 | The plan's stop path (Task 4 stop report, matrix-wide stop) is the intended net for environment surprises, so a gap that the stop path would catch is a smaller defect than one it cannot catch | V2 downplays some run-environment items and escalates only those with no stop path (V2-1); V1 does not discuss it | UNSTATED (validation rule for grading) | Medium | Promoted |

## Taxonomy tags (auto-tagged, one level per point)

- L1 surface: S-001, S-002, S-004, C-019
- L2 structural: S-003, C-001, C-008, C-009, C-010, C-011, C-012, C-015, C-016, C-018, X-001, X-004, A-002
- L3 state mechanics: C-002, C-003, C-004, C-005, C-006, C-007, C-013, C-014, C-017, X-002, X-003, A-001, A-003

## Summary
- Total structural differences: 4
- Total content differences: 19
- Total contradictions: 4
- Total unique contributions: 5
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0)
- Total diff points for convergence (S + C + X + A): 30
- Highest-severity items: C-002, C-004, C-005, C-006, C-007, X-002, X-004
- Similarity: variants are far from identical (V1 is a near-subset in topic count); debate proceeds.
