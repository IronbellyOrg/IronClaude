1e9087e91003554e64917a90032131dceac04b4c
family=oq6-b-not-evidenced
defect form: a named evidence duty ("actual (b) ... evidenced") has no check line of its own; the only related check counts RESOLVED files.
command: grep -n -E 'OQ-6|option \(b\)|design-addendum|BUILD-REQUEST' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/decisions-mechanical.md
before-output (state reviewed in review 1):
Only the intro prose names the revision BUILD-REQUEST.md and design-addendum.md and the OQ-6 (b) decision; no command, output or PASS line reads them.
coupled sites: the same duty names three evidence items: (b) itself, the fresh revision checks/PRE and the separate execution authorization; the last two are covered by S5, S6 and S7. No other check is missing a duty.
after:
(checks S9 and S10 in Run 3 read the OQ-6 record and the revision files and carry PASS lines)
