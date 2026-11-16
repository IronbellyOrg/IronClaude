e5b95a9578261602097a95b576b98e08c359914b
family=inherited-stale-suffix-claim
defect form: the claim that the stale build suffix sits in the text of both items 8.12 and 10.5, copied from the fix agent's and the orchestrator's earlier wording; only item 10.5 holds the string.
command: grep -n -E 'items 8\.12 and 10\.5|text of items 8\.12' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/gate-decision.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md ; grep -c '780594c521aa' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
before-output (state reviewed in review 1):
gate-decision.md:10 (in scope, fixed); outside the files of this task and left as written: fix-log-cycle1.md:50 and :203, phase-outputs/discovery/1.0a-facts.md:48 (the same wording; the heading "Follow-up for items 8.12 and 10.5" itself is correct because item 8.12 still needs a pointer to the facts-file rule).
task file: 780594c521aa occurs once (item 10.5).
after:
gate-decision.md:10 names item 10.5 for the string and says item 8.12 only lacks a pointer to the facts-file rule.
