365a8f3f22a318cd22479a59b0a00907663f1783
family=person-named-run
defect form: the Run id of the OQ-8 record was chosen by the executor and its Source holds no quote of the person's own words giving that Run id (item 7.15 Branch 2 needs the person's words).
command: grep -n -E -e '^(Run id|Dispatch rows|Given by|Source):' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-8-run-id-decision.md
before-output (state reviewed in review 1):
26: Run id: run_a4723d345399 (chosen by the executor)
27: Dispatch rows: 5
28: Given by: ... "The owner did not type a single Run id"
29: Source: ... "pick one, your choice"
coupled sites: the Execution Log rows for item 7.15 and the task frontmatter status and blocker_reason in .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md; both were reverted after review 1 and are set again from the owner's selection.
after:
(the fix is the owner's own selection "Use run_a4723d345399 (Recommended)" in this session; lines 26-29 now read: Run id run_a4723d345399; Dispatch rows 5; Given by the owner; Source quoting that selection and its option text)
