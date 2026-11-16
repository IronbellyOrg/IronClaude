9498f25ef3e2b3692e123474ef1ea1d352114c54
family=invented-owner-decision
defect form: text stating that the owner already decided something about D9 (the sign-off is pending).
command: grep -n -E -e 'earlier decision' -e 'True becoming None' -e 'True becomes None' docs/designs/orchestrator-mode.md
before-output:
819:| D9 | FR-010 and SP-29 (line 104): a transcript that th ...
857:| SP-29 | Applied with the D9 narrowing: a worker is a t ...
994:| 22 | Whether Orca workers get tab-map entries (launche ...
coupled sites: D9 row, SP-29 row, open item 22, the Fix cycle 3 R3-B2 row and the fix log (.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r3-b2/fix-log-cycle1.md).
after:
819:| D9 | FR-010 and SP-29 (line 104): a transcript that the tab map 
857:| SP-29 | Applied with the D9 narrowing: a worker is a transcript 
994:| 22 | Whether Orca workers get tab-map entries (launched through 
