6ea55ee30b6420813af1262f567e2695d7d39020
family=verifier-result-label
defect form: a finding with a part left open by scope is labelled RESOLVED in a verifier report without naming who decided the remainder does not count.
command: grep -n -E 'DEC-F5' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/verify-cycle1-rf-qa.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/verify-cycle1-rf-qa-qualitative.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md
before-output (state reviewed in review 2):
both reports: DEC-F5 RESOLVED with the remainder as a new minor note; fix log: PARTLY FIXED, the rest OPEN; no owner ruling on the remainder.
coupled sites: the 7.32 report (same label), the fix log, the cycle ledger and the item 7.33 gate decision.
after:
fix log last section records the owner's ruling (Accept as a minor note, 2026-11-12T01:04:30.551Z); both reports keep RESOLVED plus the separate minor note.
