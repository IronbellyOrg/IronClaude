# Saved-prompt recovery 1 (after FINAL: issues of artifacts/retries/FINAL-review-1.md)

Re-reviews (template-exact saved prompts, closed template, fresh subagents), reports kept as review-recovery-<k>-<j>.md in each task's retries folder:
- T1 prompt-1-3: all AC met, no finding. T1 complete line repeated.
- T4 prompt-4-3: all AC met; six findings, all four answers `no` (minor/note), written to T4/notes.md; complete line repeated with notes@ token. The earlier prompts (4-1 and 4-2) carried a wrong start sha and are moved.
- T9 prompt-3-2: all AC met; two minors added to T9/notes.md; complete line repeated with the new notes range.
- T2 prompt-2-3: AC met; confirmed blockers by the severity derivation: F1.1 (setup.sh:41-42 records rc=0 for `gh --version` because of `|| true` before the rc line) and F1.2 (setup.sh:157-158 comment says the push continues if the hook's exec target is missing; verified false: a bash hook whose exec target is missing exits 127 and git aborts the push). F1.3 minor.
- T3 prompt-3-4: AC2 unmet (the marker-refusal self-test case does not assert that orca was not called); F2.1 confirmed (driver.sh:59 and driver-helpers.sh:22,38: with no probe log the event count is empty and the integer test errors; verified by running it); F3.1 and F3.2 constraint breaches (`screen <name> <file>` signature and `<name>-<n>.json` naming differ from the task text: the code takes no file argument and inserts an HHMMSS stamp).
- T5 prompts 2-2 and 3-3: T5.AC3 unmet = the gap the owner accepted (T5 Ruling of 2026-11-19, not a confirmed blocker). F1.2 breach: the claim session command carries `--settings $OB/settings-claim.json` (the hook that refuses ob-442/ and settings.local.json writes), not the literal command the AC quotes; added in this run after the claim session wrote ob-442/T4.txt in the main checkout.
- T6 prompt-1-3: all four AC met; F1.1 breach: the terminal handle is looked up with `orca terminal list` (worktree path plus launch title) when the claim output has no terminal key, where the task text says to record the whole record and stop for the operator; added in this run because the real claim output has no terminal key.

Confirmed blockers remain on T2, T3, T5 (F1.2) and T6 (F1.1). No `blocked` line is written for them (it would send the task into a revert that erases later tasks' files). The next archive attempt stays blocked until the owner accepts them with Rulings or asks for fixes.

The eleven defective saved prompts were moved unchanged to artifacts/superseded-prompts/ with a README.md.
