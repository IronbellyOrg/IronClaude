# A.10 / A.10.25 Consolidated Findings (task-integrity gate)

**Task file:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/TASK-TECHREF-issue-pipeline-20261120-040158.md
**Sources:** qa-task-validation-b2-report.md (rf-qa, B2 lens), qa-task-validation-structure-report.md (rf-qa, phase-structure lens), qa-task-research-alignment-report.md (rf-analyst, run in the same wave as the two rf-qa agents because all three were report-only)
**Date:** 2026-11-20

## Items Reviewed

| Check | Lens | Verdict | Note |
|---|---|---|---|
| B2 items 1-2, 4-6 (5 components, restated context, absolute paths, measurable checks, no batch items) | b2-self-containment | PASS | |
| B2 item 3 (full prompts embedded, safety block, incremental protocol, staleness/C8, adversarial stance) | b2-self-containment | PASS | 40 fenced prompts carry the blocks (structure report) |
| B2 item 7 (no item built on contradicted claims) | b2-self-containment | PASS | Medium M3: scout hints stated as required output; each confirmed against snapshot |
| Cycle-2 and Gate-4 prompt reuse by reference (14 items) | b2-self-containment | PASS | Medium (form only): blocks are in the same file |
| Frontmatter and mandatory sections (task_type dynamic allowed) | phase-structure | PASS | |
| Phase ordering and dependencies | phase-structure | PASS | |
| Anti-orphaning (completion items inside Phase 7) | phase-structure | PASS | |
| Task Log present, last section | phase-structure | PASS | |
| QA gates M3/M4/I20 at standard intensity (3 / 3x2 / 7 / 2 agents, one fix agent, verification, halt to team-lead) | phase-structure | PASS | |
| TB-Add-1 placeholders | phase-structure | PASS | `TBD/TODO` appear only as grep patterns (Note) |
| TB-Add-3 blocked items reference Open Question | phase-structure | PASS | |
| TB-Add-4 dependency DAG | phase-structure | PASS | |
| TB-Add-5 granularity | phase-structure | PASS | |
| TB-Add-6 Verify prefix uniformity | phase-structure | PASS | |
| TB-Add-7 Execution Context source areas | phase-structure | PASS | |
| TB-Add-8 per-item code evidence | phase-structure | PASS | Medium: 15 item paragraphs name files without file:line or evidence-absence comment (planning text, not claims about code) |
| Research alignment (every scope finding has an item; no fabrication; no contradicted claim built upon) | task-research-alignment | PASS | 8 Medium gaps, see below |

## Verdicts
- B2: PASS (0 blocking, 3 Medium, 7 Notes)
- Structure: PASS (0 blocking, 3 Medium, 13 Notes)
- Research alignment: PASS (0 blocking, 8 Medium, 14 Notes)
- Overall A.10 + A.10.25: PASS. No blocking finding, so no fix agent is spawned (minor findings stay as notes).

## Follow-up candidates (Medium, non-blocking, recorded only)
1. "17 templates" vs 15 in the snapshot (task lines ~451, 469); "Glob on `_*` patterns" / "underscore-named companion files" wording (lines ~577, 2136) although the four tests/hooks files are real.
2. "grant row = not found in snapshot" rule conflicts with WORKER-CONTRACT.md:57 which contains the phrase.
3. Synth-02 agent (Step 5.2) does not read research file 06.
4. The claim-to-watcher link (`<!-- sc:issue:claim -->` marker) not carried in integration map and hand-off contracts.
5. GitHub writes by the launched agent at `--pipeline full --submit` (push, PR via /sc:pr-submit) not asked for.
6. `agent-work-report` reads `orchestrator_repo` from issue-watch.json but `cycle.py` rejects unknown keys (cycle.py:216-219): possible real contradiction, no item looks for it.
7. No item checks which launch paths each guard layer governs (watcher `--pipeline none` session and coordinator-started workers get no L1/L2).
8. Appendix A would miss tests/skills/test_clickup_claim.py, tests/skills/test_model_alias_policy.py, tests/unit/test_cli_doctor.py.
