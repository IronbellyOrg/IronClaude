# Tier 1 reflection card (UC-1, inline orchestrator)

Spec: .dev/tasks/to-do/TASK-WF-spec-20261108-181616/source.md
Tasklist: .dev/tasks/to-do/TASK-WF-spec-20261108-181616/TASK-WF-spec-20261108-181616.md (14 tasks, 6 phases)
Scope of the plan: source.md section 3 and section 4 (plus owner rulings in the plan's Constraints).
Self-reported confidence: 0.80 (to be re-graded blind).

## Analyzer section (root cause, ordering, deviations from the spec)

- A1 [ordering defect]: Task 5 requires `finalize` to write a `label-count critical+major` line "built by the same function as Task 6's `count`" (plan Task 5 body), but Task 6 (Depends on: Task 5) is where `count` is defined. Task 5 cannot meet its own acceptance criterion ("the computed block's label-count line counts a CRITICAL-labelled `late-found` claim") without code Task 6 owns. Fix: define the counting function in Task 5 and have Task 6 only add the `count` subcommand around it.
- A2 [documented deviation, Necessary]: source.md section 3.4 line 129 says `tests/recommend/test_routing_refresh.py` is "Run, do not edit"; plan Task 10 edits `_POST_REFRESH_ADDITIONS`. Justified in the plan by `tests/recommend/test_routing_refresh.py:648` (`assert shipped - _POST_REFRESH_ADDITIONS == active`), which a new command file breaks; source.md itself marked the count effect UNVERIFIED.
- A3 [documented deviation, Authorized by owner]: source.md section 3.1 says the variant is a "Copy of `spec-panel.md`"; plan Task 9 removes `## Unattended mode` per the owner ruling recorded in Constraints. `tests/skills/test_worker_contract.py:831-839` pins the exact command set with that section.
- A4 [scope]: owner decision on deferred/demoted/withdrawn findings is implemented as reporting only (Tasks 3, 5, 6); the verdict function of source.md section 2.4 step 9 is unchanged.

## QA section (coverage and acceptance)

- Q1: Pass 1 found no labelled requirement IDs in source.md (no R-/REQ-/SPEC-/T- tokens), so coverage is Pass-2 inferred only: 34 rows, 31 matched by the deterministic containment rule, coverage_pct_union 0.9118 (artifacts/coverage-matrix.json).
- Q2: The 3 rows the mechanical rule left unmatched are lexical misses that the plan does cover in other words: INF-003 "FR-10 stays" (Task 9 says "FR-10 stays"), INF-009 `--rubric` and `--cap` (Task 3 lists both options), INF-034 `audit-sample` k = 5 (Task 6 `--owner-k 5`). Reviewer should confirm by reading.
- Q3 [gap candidate]: source.md section 4 line 163 says the measurement copy of the command "is built from the exact Arm B base file (472 lines, sha256[:12] `c8d80346a96c`) plus the section 3.1 edits". Plan Task 13 only documents this in INSTALL.md; no task produces that measurement copy file. Whether this is a plan gap or coordinator work is not stated by the spec.
- Q4 [risk]: Task 7 depends on files in a sibling checkout `exp346-ab-ctl-r1` whose exact paths the plan does not pin (it says "Locate the exact files with a read-only listing"); the task has a blocked path if they are absent.
- Q5: Every task has an `Acceptance criteria:` block with runnable checks (pytest commands, grep counts, git diff checks).

## Refactorer section (structure, size, reuse)

- R1: The script grows across Tasks 3 to 6 in one file `scripts/stoprule.py`; each task extends the same test file `tests/skills/test_stoprule_script.py`. Reasonable split for review, but every later task re-runs the whole test file, so a failing earlier case blocks later tasks.
- R2: Test conventions reuse `tests/skills/test_issue_repo_resolution.py` (importlib + subprocess) rather than inventing a harness: reuse, good.
- R3: Agent frontmatter reuses the `confidence-calibrator` pattern (`src/superclaude/agents/confidence-calibrator.md:1-9`).
