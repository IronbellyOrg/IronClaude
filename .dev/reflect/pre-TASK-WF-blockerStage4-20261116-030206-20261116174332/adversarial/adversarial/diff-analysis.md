# Diff Analysis: reviewer-card comparison (stage 4 plan, second review)

Variants: V1 = reviewer 1 (analyzer, sonnet class), V2 = reviewer 2 (qa, haiku class), V3 = reviewer 3 (refactorer, opus class). Files: `variant-N-original.md` in this folder. Keys used below: P4 = `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md`; SRC4 = `.../source.md` in the same folder; S1, S3 = the stage 1 and stage 3 plans; SPEC = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`.

## Metadata
- Generated: 2026-11-16T18:26:00Z
- Variants compared: 3
- Total differences found: 20 (structural 1, content 11, contradictions 5, unique 6, shared assumptions 3; unique contributions are not diff points)
- Categories: structural (1), content (11), contradictions (5), unique (6), shared assumptions (3)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Findings count and depth of the Checked section | 6 findings; Checked has G1 to G8 status plus a test simulation | 4 findings; Checked has G1, G2, G9 to G14 and task order | 8 findings; Checked has retired carriers, plugin decision, cross-stage facts, paths | Low |

## Content Differences

| # | Topic | V1 approach | V2 approach | V3 approach | Severity |
|---|-------|-------------|-------------|-------------|----------|
| C-001 | Task 5 acceptance cannot show that strict T2 is on (P4:112; S1:223 "strict mode is a switch, off in this phase") | F1 minor, unpassable-check | F2 minor, other | F1 MAJOR blocking, missing-requirement | High (grade split) |
| C-002 | SPEC:867 asks the roadmap and tech-research cap lines to "point at the shared rule"; no stage 4 task does it and the plan records no exclusion | F6 minor | F1 MAJOR blocking (roadmap only) | F8 minor | High (grade split) |
| C-003 | Task 1 stage 3 completion check P4:41 passes an all-complete archive-blocked package in one clause and fails it in the other | F2 minor | F3 minor | F2 minor | Low |
| C-004 | The Rule 6 grep at P4:37 returns about ten lines; only line 990 of `rf-qa-qualitative.md` is Critical Rule 6 | F3 minor | not raised | F3 minor | Low |
| C-005 | Task 4 keeps "CRITICAL is blocking" unconditional although SPEC:739 says to narrow it | F4 minor | not raised | not raised | Medium |
| C-006 | The "digest ends with the sentence" greps (P4:43, P4:60) already print 1 today | F5 minor | not raised | not raised | Low |
| C-007 | The plugin FR-8 parenthesis is edited "because the mapping test pins them" but MAP:102 pins only "otherwise it is Medium"; plugin twin ends half-narrowed | not raised | not raised | F4 minor, contradiction | Low |
| C-008 | S3:214 still says stage 4 adds a plugin mirror | not raised | not raised | F5 minor | Low |
| C-009 | Task 5 final run omits the doctor tests although Task 5 may reword `src/superclaude/cli/doctor.py` | not raised | not raised | F6 minor | Low |
| C-010 | Task 5 acceptance P4:116 cites the Task 6 summary, written later | not raised | not raised | F7 minor | Low |
| C-011 | Coverage matrix omits clauses of Revision 2 (G6 order, no re-pin of the retired test, final row counts) | not raised | F4 minor | not raised | Low |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | Grade of the strict-T2 gap (C-001) | minor: Task 5 also states "T2 ... is in strict mode", the switch is the requirement | minor: promised evidence "does not distinguish the two modes", not an inevitable wrong result | blocking: a no-op switch passes every check and nothing later catches it | High |
| X-002 | Grade of the SPEC:867 gap (C-002) | minor: lines are [E], plan records no exclusion | blocking: every task can pass while the spec requirement is unmet | minor: lines are [E], consequence small | High |
| X-003 | Overall verdict | "no blocking defect in Tasks 1 to 6" | NEEDS-REVISION (one blocking) | NEEDS-REVISION (one blocking) | Medium |
| X-004 | V1 Checked cites "G4 is removed by the plugin decision at plan line 87"; P4:87 is the FR-8 bullet (plugin decision is at P4:23 and P4:91) | wrong line | n/a | n/a | Low |
| X-005 | V3 F8 says SPEC:867 asks the "roadmap and tech-research cap lines"; the cell names roadmap, readme, tech-reference and operational-guide cap lines and gives tech-research line numbers | n/a | V2 names roadmap only | paraphrase differs from the cell | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | Test simulation of Tasks 2 and 4 text against the mapping, spec-panel, loop-extension, brief-placement, rules-text and worker-contract tests (the new Unattended line must not put `artifacts` in backticks before the Contract bullet; briefs stay one line) | High |
| U-002 | V1 | Re-count of the cap counts (5, 6, 1, 2) and fixture-row check | Medium |
| U-003 | V2 | Phase structure, numbering and `Depends on:` check; G9, G10, G13 verified | Medium |
| U-004 | V3 | Retired-carrier and MDTM-template consistency check; plugin decision check; cross-stage registry counts and allow-list | High |
| U-005 | V3 | S3:214 stale plugin-mirror text; doctor tests; Task 5 forward reference | Low |
| U-006 | V2 | Coverage-matrix completeness note (G9 to G14 fixed) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Stage 1 builds T2 non-strict and its non-strict scan already fails an unregistered file that holds the old sentence (S1:223) | all three reason from it | High | STATED (S1:223) |
| A-002 | Stages 1 to 3 will be executed as their plans say, so the registry, scale-map section, summary names and test files exist when stage 4 runs | all three read cross-stage facts from plan text only | Medium | UNSTATED (no card says nothing was executed except V2 in Checked) |
| A-003 | The 12-test final run (P4:113) is green once every row is `v2`; no card ran any test (stages 1 to 3 have not run) | all three treat the run list as sufficient or insufficient on reading alone | Medium | UNSTATED |

## Summary
- Total structural differences: 1
- Total content differences: 11
- Total contradictions: 5
- Total unique contributions: 6
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001, X-002
