# HX-1 notes

Report used: `.dev/reflect/pre-TASK-WF-applyTheV1Worker-20261107-211837-20261107212538/REPORT.md`. Its input-snapshot plan sha256 (2da8dc1d...) equals the plan file, and its source sha256 (310693b3...) equals source.md.

## Kept
- G-1 (GT1) and G-2 (GT2): both are minor drift in the report, so `blocking_in_implement` is false. No implementation-time review graded them blocking. Quotes were checked by script as exact substrings of candidate.md. Both facts were confirmed present in source.md and absent from the plan.

## Dropped
- T1 review-1 F1.1 (blocking): the implementer's WC-10 sentence cut part of the C-1 wording. This is a defect in code written during implementation, not in the plan text.
- T6 review-1 F1.1 (blocking): the implementer wrote the wrong L1 cap. Implementation defect. The plan does not state the caps, but the review blames the delivered text, so it is not a plan defect.
- T7 review-1 F1.1 (blocking): ruff-format.log ended in exit=1 because of an extra repo-wide run. Implementation evidence defect.
- The report's coverage rows INF-003 and INF-004 are the same two gaps as G-1 and G-2, so nothing was counted twice.

## Base commit
- The `start sha=` lines in progress.md are tree objects (`git cat-file -t` prints `tree`), not commits, and no commit in history has that tree.
- Tree 651fb0e3 matches the non-`.dev` content of commit 2b3ae7e7 (and of 0b8a5801) exactly. 2b3ae7e7 has the smallest total difference, so it is used as base.
- Base contains `src/superclaude/core/WORKER-CONTRACT.md` and `tests/skills/test_worker_contract.py`. The implementation only edits those two files, so `masked_paths` is `[]`.
- The design file the plan cites (`.dev/brainstorms/.../merged-requirements.md`) is not in base (it was untracked at the time). It was not read, and the plan quotes only the plan's own text.

## Not verified
- The design wording of section 10.2 was not opened, so whether the plan's task text matches the design line by line is unchecked.
