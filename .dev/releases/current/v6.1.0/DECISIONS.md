# Release decisions (6.1.0)

Source: issue 647 (the map and plan) and the messages of GeneralIronFlow relaying Clay. Times are UTC.

| # | Decision | Answer | Decided by | Date |
|---|---|---|---|---|
| 6.1.0-1 | What 6.1.0 contains | The task and documentation bundle (Part B of issue 571, issue 647): 9 skills (`prd`, `tdd`, `tech-research`, `tech-reference`, `operational-guide`, `readme`, `task`, `task-builder`, `roadmap`), 1 command (`/sc:tdd`) and 1 eval suite (`workflow_vs_task_builder`) are removed; every route that offered the task-file (MDTM) route points at `/sc:workflow` then `/sc:implement`; an upgrade of an installed 6.0.0 removes the shipped files (retire step) | Clay | 2026-11-18 (decision 6.3 of 6.0.0, corrected in issue 647) |
| 6.1.0-2 | Kept (not removed) | `/sc:task` and `sc-task-protocol`, `/sc:validate-tests` and `sc-validate-tests-protocol`, the eval suite `task_classification_contract`, and all eight `rf-*` agents (`rf-analyst`, `rf-assembler`, `rf-task-builder`, `rf-task-executor`, `rf-task-researcher`, `rf-team-lead`, `rf-qa`, `rf-qa-qualitative`). PR 2 withdrawn, #652 closed. The future of the `rf-*` agents is issue 572's research | Clay | 2026-11-18 |
| 6.1.0-3 | How the pull requests are merged | Into `integration`, squash, in this order: #650, #653, #656, #657. Same rule as 6.0.0 (every check green on the final head, Augment and Codex finished on that head, no thread open, verified on GitHub by the orchestrator). The bundle agent rebases and retargets each after the previous merge | Clay (via GeneralIronFlow) | 2026-11-18 20:57 |
| 6.1.0-4 | How the release is run | "The same way" as 6.0.0: records, `master` merged into `integration` if needed, release PR `integration` to `master`, the gate, **stop for Clay's final yes**, then merge with a merge commit, tag `v6.1.0`, GitHub release, post-release | Clay (via GeneralIronFlow) | 2026-11-18 20:57 |
| 6.1.0-5 | Scope of `/sc:post-release v6.1.0` | Not stated. Assumed the same as 6.0.0 (decision 6.6: documentation sync and the install and upgrade runs, no new hand-test guides) because Clay said "the same way". Ask if Clay wants otherwise | Assumed; Clay to confirm | OPEN (assumption) |
| 6.1.0-6 | Open pull request #641 (ccsession feature into `master`) | Not in this release unless Clay says otherwise (it was "meant for a later release" at 6.0.0). Gate G9 needs an answer | Clay | OPEN |
| 6.1.0-7 | Part C (issue 572, agents) | Not in this release | Clay | 2026-11-18 (per issue 647 "Out of scope") |
