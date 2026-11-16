1e9087e91003554e64917a90032131dceac04b4c
family=style-diff-not-recorded
defect form: a duty to record an actual diff or text is met by hunk-header lines or counts, not by the changed lines.
command: grep -n -E '^@@|^[-+][^-+]' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/decisions-mechanical.md | head ; grep -n 'git diff HEAD' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/decisions-mechanical.md
before-output (state reviewed in review 1):
Run 2 Section B: S2 prints 7 '@@' hunk-header lines only; S4 prints two counts; no diff body anywhere in the file.
coupled sites: the style-diff duty appears once in the item Action ("record the actual canonical style diff"); the result file intro names the style file; no other file records the diff (the step-7.10 result file holds a before/after excerpt and diff of its own, which the item names as a read input, not as this item's output).
after:
(check S11 in Run 3 prints the full git diff HEAD -U0 of the style file, 7 hunks)
