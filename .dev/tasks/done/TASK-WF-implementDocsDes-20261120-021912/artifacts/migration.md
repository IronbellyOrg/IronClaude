# Migration of superseded workflow packages (issue 624, Task 13)

Moved from `.dev/tasks/to-do/` to `.dev/tasks/archive/` with `remediate.py archive` (no `mv`):

1. TASK-WF-designSpec-20261107-072120 (--superseded-by none; contract already said SUPERSEDED, no second item added)
2. TASK-WF-designSpec-20261107-074040 (--superseded-by none; contract already said SUPERSEDED)
3. TASK-WF-p3Requirements-20261107-065757 (--superseded-by TASK-WF-p3Requirements-20261107-070713; `superseded_by` written; that replacement sits in `.dev/tasks/done/`)
4. TASK-WF-removeTheAnyIssu-20261031-235404 (--superseded-by none)
5. TASK-WF-removeTheAnyIssu-20261101-225338 (--superseded-by none)
6. TASK-WF-removeTheAnyIssu-20261101-225635 (--superseded-by none)
7. TASK-WF-removeTheAnyIssu-20261102-042031 (--superseded-by none)

Open owner decisions (NOT moved):

- TASK-WF-blockerStage4-20261116-030206: has no `return-contract.yaml` at all; its replacement TASK-WF-blockerStage4-20261117-170451 says it is superseded. Owner decides whether to archive it.
- TASK-WF-specScRecommendR-20261024-055620: an intake with no plan. Owner decides what to do with it.
