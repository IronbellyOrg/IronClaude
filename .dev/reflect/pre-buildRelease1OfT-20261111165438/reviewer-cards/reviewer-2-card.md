# Reviewer 2 card (haiku class, qa lens), persisted by the orchestrator

Self-reported confidence 0.91. Plan cited as plan:N (`.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/TASK-WF-buildRelease1OfT-20261111-164757.md`); SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. All five rated blocking, MEDIUM severity, class Drift.

- R2-1 (plan:223-238): Task 13 depends only on Task 12 while Task 14 supplies the golden contract tests and can stay blocked; `release-gates.md:5,11,22-26` require those gates or an accepted fallback; plan:23 admits the missing selection record.
- R2-2 (plan:35-40): Task 1 covers SIGINT/SIGTERM and four exit tests, but `stack.md:22` also requires restoration on SIGHUP/SIGTSTP and re-entry on SIGCONT.
- R2-3 (plan:78-84): blank `dispatchId` stays eligible for deduplication; `adapter-contract.md:44` excludes absent and blank IDs and requires `identity unknown`.
- R2-4 (plan:78-86): Task 4 retains every row not returned; `ARCHITECTURE-SPINE.md:112` requires a non-PARTIAL cycle to replace previous anonymous rows (PARTIAL keeps them); no criterion checks this.
- R2-5 (plan:238-241): the golden STALE test ages timestamps but sets no elapsed monotonic time since the successful poll; `ARCHITECTURE-SPINE.md:190` derives STALE from `last_success_mono`; plan:149 says old evidence after a fresh poll must not mark the source STALE.

Notes: no commands or live Orca calls were run. Adherent tasks: 9 of 14 (affected: 1, 4, 12, 13, 14).
