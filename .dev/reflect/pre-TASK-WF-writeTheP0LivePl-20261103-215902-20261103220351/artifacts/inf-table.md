| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | /sc:troubleshoot "<real symptom>" --output-dir <dir> with no --fix and no --depth deep | source.md:1 | unmapped |
| INF-002 | /sc:workflow "<small change>" --handoff none | source.md:1 | T3 |
| INF-003 | /sc:adversarial --compare <two files> --depth quick --output <dir> | source.md:1 | T4 |
| INF-004 | each run directly by the worker with the AC-0.4 report-file and outcome rule in its brief | source.md:1 | C10 |
| INF-005 | AC-0.5 (timed worker-start under 45 s with the normal launch setup) | source.md:1 | C9 |
| INF-006 | AC-0.6 (whether worker-read --source transcript names tool calls, with a quoted excerpt) | source.md:1 | C10 |
| INF-007 | all seven section 7.2 steps per live check | source.md:1 | C2 |
| INF-008 | fresh disposable worktree created by Orca at its default path from branch ironbelly/OrcaCLICommandRefactor-Specs at 8db29f11, never under .dev/worktrees/ | source.md:1 | unmapped |
| INF-009 | make sync-dev inside it before dispatch unless --setup run is confirmed to do it | source.md:1 | C10 |
| INF-010 | orca worktree rm after step 7 | source.md:1 | C10 |
| INF-011 | a P0 phase report in the package artifacts that combines the static report (.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md, cited not copied) with the live results and states the phase verdict | source.md:1 | unmapped |
| INF-012 | for troubleshoot use a real current symptom from the static run's accepted pre-existing failures (.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-accepted-failures.md) | source.md:1 | unmapped |
| INF-013 | for workflow a small harmless change prompt | source.md:1 | unmapped |
| INF-014 | for adversarial two existing committed files under .dev/orca-command-refactor/ | source.md:1 | T4 |
| INF-015 | no edit to any source, command, skill, agent or test file | source.md:1 | C3 |
| INF-016 | no git commit, push, PR, gh write or superclaude install | source.md:1 | C4 |
| INF-017 | no interaction with the SuperClaude-Org upstream | source.md:1 | C4 |
| INF-018 | UV only | source.md:1 | T1 |
| INF-019 | never stage .claude/ | source.md:1 | C6 |
| INF-020 | leave the superseded package .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/ unstaged and untouched | source.md:1 | C6 |
| INF-021 | stage .dev/tasks at the end | source.md:1 | T5 |
| INF-022 | the live plan is executed by /sc:implement in a top-level session the person opens (depth 0, the coordinator), never inside an Orca worker, since its own live checks start Orca workers | source.md:1 | C1 |
| INF-023 | A failed live check is recorded in the phase report, not retried silently; per spec AC-0.4 a failure reopens section 1. | source.md:1 | C7 |
| INF-024 | The plan must fix concrete inputs in advance, not leave them to the executor | source.md:1 | unmapped |
