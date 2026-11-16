# Severity-rule test: pre-registration addendum 1 (2026-11-16 22:55 UTC; no run of this test has been scored)

**Context for a reader with no history.** `PREREG.md` in this folder registers a test of a narrowed "contradiction" blocking clause (arm S) against the plain control (arm Z0) on four plans. A second session is running a different test on the same four plans and the same ground truth: a stronger reviewer panel (`../20261116-stronger-panel/PREREG.md`, addenda 1 and 2). The owner ruled that the two efforts overlap and must converge on one deliverable. This addendum fixes how, before any score from either test is read. It changes none of the gates of `PREREG.md` or of the other test's `PREREG.md`.

## Convergence plan (proposed to the other session on 2026-11-16 22:50 UTC; points marked [open] wait for its reply)

1. **One joint report** (`../20261116-levers-report/REPORT.md`), written after both tests end, with one table for every arm of both tests: found fraction, wrong blockers per run, blocking precision, blocking defects found, median seconds, tokens, each against its same-day ember Z0 control. Each test's own pre-registered gate decides its own arms; no gate is added or relaxed afterwards. [open: other session's reply]
2. **Controls:** both tests run an identical ember Z0 on the same plans. They are reported side by side. They are pooled only if the bootstrap interval (documents, then runs) of the difference between the two controls contains 0 on both found fraction and wrong blockers; otherwise each lever is judged against its own interleaved control, as registered. Neither control is dropped.
3. **Conditional combined arm** (sonnet panel + rule S, 20 runs): started only if the sonnet panel meets its found-fraction lever rule AND arm S passes G1 to G4. It will be pre-registered separately, before running, after consulting the other session. If only one lever passes, none is run.
4. **Ownership:** each session owns its arms and gates; this session owns arm S and the joint report; neither edits the other's folder; results of one test are read by the other session only after that test ends.
5. **Shared resources:** this test uses slot 2 and `/tmp/evalsb-sev` and `/tmp/sev-runs`; the other uses slot 1 and `/tmp/evalsb-recipe`.

## Facts recorded now

- Arm S differs from Z0 in one file (`briefs/base.txt` of `../20261116-sev-s/` against `../20261116-sev-z0/`).
- Runs are written under `/tmp/sev-runs` (the harness refuses run folders outside `/tmp` or its own folder); scores and run summaries are copied into this folder after the end.
- The worktree was moved to the branch `ironbelly/eval-severity-rule-test` on 2026-11-16 22:35 UTC with the owner's approval; the other session agreed to work on it too (its message of 22:48 UTC).
