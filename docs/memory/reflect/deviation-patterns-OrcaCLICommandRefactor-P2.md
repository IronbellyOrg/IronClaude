# Deviation patterns: OrcaCLICommandRefactor-P2

Recurring deviation signals from sc:reflect runs on this worktree (90-day expiry, last 20 entries).

## pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500 (2026-11-07, UC-1)

- **Missed nested calls.** A plan that converts commands for `--unattended` listed the nested calls named in each spec row but missed others the command's skill makes (tasklist Stage 9 `sc:task`, release-split Part 4 `sc:analyze`, reflect Wave 1B `tech-research`, troubleshoot `--diagnosability-handoff` to `sc:workflow-protocol`). Check: grep every converted skill for `Skill sc:`, `/sc:` and `Invoke` before writing the nesting table.
- **Nested status propagation.** Passing `--unattended` to a callee makes `blocked` a new possible result; callers had no rule mapping a nested blocked or failed result to their own status.
- **Spec row narrowed silently.** A spec row's "X and Y, else blocked" became "X, else blocked" (cli-eval safety flags). Check each row's full condition list against the task text.
- **Labels pinned instead of resolutions.** Test phrases pinned gate labels ("Approval Required", "blocked_question") rather than condition-to-outcome text, so a reversed rule would pass.
- **One-line exemption budget.** A plan-chosen cap of one deleted line per command file left other stale lines that the same change made wrong (workflow.md:72).
- **Owner-wording rule applied to some tasks only.** "left out (WC-4)" was pinned for 2 of 15 commands.
- **Citation drift in merged cards.** Wrong-file and moved-line citations (troubleshoot.md vs the skill; plan:46 vs :53) survived to the merged verdict and were caught only by the evidence gate.
