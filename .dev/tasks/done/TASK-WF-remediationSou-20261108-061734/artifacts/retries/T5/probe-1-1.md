677defafdfcfb17d393151ffe8106ab2492db716

## family=false-claim (from review r5-1)

Defect form: an overgeneralized claim sentence in a decision artifact ("every case exceeded even 3.8 s") contradicted by the measured table it summarizes (backslash-lines-64KB max 2991.6 ms).

Search command (read-only): grep -n -e "every case exceeded" -e "2991.6" .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/limit-selection.md .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d2-serial-loaded.md

before-output (touched files + AC-named files):
- .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/limit-selection.md:24: ...Under that load every case exceeded even 3.8 s and the worst exceeded 5.5 s...
- .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d2-serial-loaded.md:16: | T-SPD-5 guard, governed FS, backslash-lines-64KB | 100 | 1694.3 ms | 2566.7 ms | ... | FAIL: max 2991.6 ms; exit [0] |

Coupled sites: none (the same claim appears nowhere else in the artifact set; the T6 test comment must not copy this sentence).

after:
- .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/limit-selection.md:24: ...Under that load three of the four case maxima exceeded 3.8 s (backslash-lines-64KB maxed at 2991.6 ms) and the worst exceeded 5.5 s...
- .dev/tasks/to-do/TASK-WF-remediationSou-20261108-061734/artifacts/d2-serial-loaded.md:16: (unchanged measured row; the sentence now matches it)
