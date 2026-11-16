6ea55ee30b6420813af1262f567e2695d7d39020
family=verifier-result-label
defect form: a verifier report gives an F_0 finding a hybrid status instead of the binary RESOLVED or OPEN the item requires.
command: grep -n -E 'RESOLVED for|remainder OPEN' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/verify-cycle1-rf-qa.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/verify-cycle1-rf-qa-qualitative.md
before-output (state reviewed in review 1):
verify-cycle1-rf-qa.md:19: DEC-F5 ... RESOLVED for the rule defect; one stated remainder is not fixed (below)
verify-cycle1-rf-qa-qualitative.md:24: DEC-F5 ... RESOLVED for the fixed part; remainder OPEN, graded MINOR (note N2)
coupled sites: the summary line near the end of each report and the DEC-F5 heading in the qualitative report.
after:
both reports state DEC-F5 as plain RESOLVED, with the remainder as a separate new MINOR note (M-1 in the rf-qa report, N2 in the qualitative report); both keep Verdict PASS and Blocking count 0.
