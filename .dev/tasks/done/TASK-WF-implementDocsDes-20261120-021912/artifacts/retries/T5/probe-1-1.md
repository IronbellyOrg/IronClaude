3bc8bdc73f23cf7d34b84149481ff37952b092e3
family=mark-once
defect form: text that calls mark more than once per run or loops step 7
command: grep -n -e 'mark' -e 'steps 1 to' src/superclaude/skills/sc-workflow-protocol/refs/remediation.md
before:
51:7. **Mark once.** After the re-review, call `mark` exactly once with the final verdict (section 6).
53:Failed placement undo: when `place` fails, run `REM release --root <root> --new-id <new-id>` and then `REM restore --root <root> --old-id <old-id>`. `restore` moves the archived package back to `to-do/` after removing exactly what `archive` added, so the restored package carries no SUPERSEDED mark and no empty or half-filled new package is left.
55:Order in full: `reserve`, `prepare`, reviser edits, Wave 3 gate on the copy, `archive`, `place`, re-review, then `mark`. `release` runs on a failure before `archive` and after a failed `place` (before `restore`).
57:Fix cycles: a re-review with an open, regressed or new blocker starts the next cycle, which repeats steps 1 to 7 with the placed package as `<old-id>` (counts from the re-reviewer card, section 1). At most 2 fix cycles (3 reviews in all, counting the first review). Do not edit a placed package in place.
82:- Link the new package: `REM mark --package <new package dir> --supersedes <old-id> --route regenerate --finding-counts '<json>'` writes `supersedes`, `remediation_route` and `finding_counts`.
83:- Wave 4 reviews the new package and its counts are routed once more, but a regenerate runs at most once per run: pass `--regenerated-already` to `route`. A second `regenerate` result is `escalate`: stop, report the open blocker ids to the user and mark the package FAIL (section 6). The old plan is never edited.
85:## 6. Cap, verdict and `mark`
87:`mark` is the one writer of `review_verdict: FAIL`, `open_blockers`, `superseded_by`, `fix_cycles` and, for the regenerate route, `supersedes`, `remediation_route` and `finding_counts`. It replaces the line of a key that exists and otherwise appends it once, so no key is written twice. Call it once, with the final verdict.
89:- Clean re-review: `REM mark --package <placed package dir> --fix-cycles <n>`.
90:- Blockers still open after the 2nd fix cycle (or on `escalate`): the last placed package stays in `.dev/tasks/to-do/`; run `REM mark --package <dir> --review-fail --open-blockers <id,id,...> --fix-cycles <n>`. Its contract then carries `review_verdict: FAIL` and `open_blockers`, the run escalates to the user, and `/sc:implement` refuses the package. Under `--unattended` the run ends `partial` with the open blockers in `unresolved`.
91:- `mark` takes `--package` but no `--root`.
coupled sites: lines 51, 55, 57, 82, 83, 87, 89, 90
after:
51:7. **Mark once.** After the re-review, call `mark` exactly once with the final verdict (section 6).
53:Failed placement undo: when `place` fails, run `REM release --root <root> --new-id <new-id>` and then `REM restore --root <root> --old-id <old-id>`. `restore` moves the archived package back to `to-do/` after removing exactly what `archive` added, so the restored package carries no SUPERSEDED mark and no empty or half-filled new package is left.
55:Order in full: `reserve`, `prepare`, reviser edits, Wave 3 gate on the copy, `archive`, `place`, re-review, then `mark`. `release` runs on a failure before `archive` and after a failed `place` (before `restore`).
57:Fix cycles: a re-review with an open, regressed or new blocker starts the next cycle, which repeats steps 1 to 6 with the placed package as `<old-id>` (counts from the re-reviewer card, section 1); step 7 (`mark`) runs once, after the last cycle. At most 2 fix cycles (3 reviews in all, counting the first review). Do not edit a placed package in place.
82:- Link the new package with the one `mark` call of the run (section 6), made at the end of the route: `REM mark --package <new package dir> --supersedes <old-id> --route regenerate --finding-counts '<json>'` writes `supersedes`, `remediation_route` and `finding_counts`; on `escalate` the same single call also carries `--review-fail --open-blockers <id,id,...>`.
83:- Wave 4 reviews the new package and its counts are routed once more, but a regenerate runs at most once per run: pass `--regenerated-already` to `route`. A second `regenerate` result is `escalate`: stop, report the open blocker ids to the user and mark the package FAIL (section 6). The old plan is never edited.
85:## 6. Cap, verdict and `mark`
87:`mark` is the one writer of `review_verdict: FAIL`, `open_blockers`, `superseded_by`, `fix_cycles` and, for the regenerate route, `supersedes`, `remediation_route` and `finding_counts`. It replaces the line of a key that exists and otherwise appends it once, so no key is written twice. Call it once, with the final verdict.
89:- Clean re-review: `REM mark --package <placed package dir> --fix-cycles <n>` (on the regenerate route add `--supersedes <old-id> --route regenerate --finding-counts '<json>'` to this one call).
90:- Blockers still open after the 2nd fix cycle (or on `escalate`): the last placed package stays in `.dev/tasks/to-do/`; run `REM mark --package <dir> --review-fail --open-blockers <id,id,...> --fix-cycles <n>` (on the regenerate route this same call also carries `--supersedes <old-id> --route regenerate --finding-counts '<json>'`). Its contract then carries `review_verdict: FAIL` and `open_blockers`, the run escalates to the user, and `/sc:implement` refuses the package. Under `--unattended` the run ends `partial` with the open blockers in `unresolved`.
91:- `mark` takes `--package` but no `--root`.
