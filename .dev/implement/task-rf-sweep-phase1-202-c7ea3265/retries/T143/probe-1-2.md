365a8f3f22a318cd22479a59b0a00907663f1783
family=log-row-order
defect form: a log row that points at a neighbouring row by position ("above"/"below") names the wrong neighbour, because the Execution Log is newest first.
command: grep -n -E 'row above|row below|rows below|rows above|two rows' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md ; grep -c -E 'row above|row below|rows below|rows above' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-8-run-id-decision.md
before-output:
2806: ...in the two rows below.
2807: ...so the row above is withdrawn, not deleted.
(decision record: 0 matches)
coupled sites: none; line 2806 "the two rows below" is correct (the withdrawal row and the withdrawn row sit below it).
after:
2807: ...so the earlier RUN ID RECORDED row directly below is withdrawn, not deleted.
