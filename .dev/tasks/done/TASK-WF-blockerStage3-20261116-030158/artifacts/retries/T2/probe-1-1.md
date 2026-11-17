de14ad4be2913322a46c09c66d9a97e4cdaa5392
family entry-check-order (failing review r1-1)
- defect form: a task whose first step is a re-read of the entry conditions records that re-read after its first edit instead of before it
- search command: grep -n -F -e "re-read" -e "before the" -- .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/pre-edit-check.md
- before-output: pre-edit-check.md:16 says the re-read was run right after the edit, not before it
- coupled sites: pre-edit-check.md Task 2 section (the dated entry and the mapping section below it); Tasks 3 to 6 each start with "First read that pragmatic.md holds the new position 1 wording" and must read before editing; Task 1's entry lines at pre-edit-check.md:7-12
after: 00:56:01Z fix applied
14:## Task 2 re-read of the entry conditions (2026-11-17)
16:Order of events, stated plainly: the four conditions were read at Task 1 a few minutes before the pragmatic
31:## Task 2 re-read of the entry conditions, repeated before the edit is applied again (2026-11-17, fix pass 
33:The first review found that the re-read above ran after the edit. The fix: `pragmatic.md` was set back to i
