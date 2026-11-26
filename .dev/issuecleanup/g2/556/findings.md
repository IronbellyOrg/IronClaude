# Issue 556 review

## Verdict and evidence
still-relevant

Issue 556 (the grouped record of three defects in the reflection command-line wrapper) is open, in the project backlog, and all three defects are still present in the current source. Nothing is in progress: no assignee, no open pull request, and the owner put it at lowest priority on 2026-11-18 with an instruction that nobody works on it until the wrapper is used again.

- Preview mismatch, split out as issue 563. `--print-command` prints the `/sc:reflect` prompt (`src/superclaude/cli/reflect/runner.py:452-481,647-651`), but a real run at the default depth takes the ensemble route (`runner.py:538-543`) and the scorer prompt is the literal `/sc:adversarial` string (`ensemble.py:582-598`, the text at 594). The issue's cited lines `runner.py:538-544,655-658` have shifted: 655-658 is now the dry-run result record, and the prompt print is at 650-651.
- Exit-code mismatch, split out as issue 564. Any exception inside `run()` is written as a `blocked` sidecar with reason `runner-error` and then re-raised (`src/superclaude/cli/reflect/commands.py:442-469`), so the process exits 1. The user guide maps `blocked` to exit 2 (`docs/guides/reflect-cli-tools-guide.md:370`). The cited lines `commands.py:444-470` now start at 442.
- Stub scorer, split out as issue 565. With two or more successful reviewers and no score function, the ensemble starts a real `ClaudeProcess` as the scorer (`src/superclaude/cli/reflect/ensemble.py:424-430,537-553`) even under `--transport stub`. The guide calls stub "credit-free" (`docs/guides/reflect-cli-tools-guide.md:137`). The cited lines `ensemble.py:424-430,537-555` match, with the launch ending at 553.
- The manual testing guide already records all three as observed-as-coded (`docs/testing/v5.0.0/user/D12-reflect.md:15,26-30`), so it and the user guide disagree.
- Last commit touching the three files: `2ca022bf7` (pull request 653). Current branch tip: `a7ae3dd30`.

## Real current state
The wrapper still runs exactly as the 2026-11-16 report describes. The default depth goes through the tier-2 ensemble, the preview prints the tier-1 prompt that production code only launches when the process class is a test double, a missing-credential failure exits 1 with a `blocked` sidecar, and stub mode still starts one headless `claude` session for the scorer. The line numbers in the issue have drifted by a few lines, but the behavior has not changed. The owner's 2026-11-18 comment keeps the project status at Backlog and the issue unassigned.

## Concrete next steps
No fix should start. The owner said on 2026-11-18 that nobody works on this until the wrapper is used again, because it runs headless Claude. When that hold lifts, the smallest safe changes are: make the preview print the ensemble plan and the scorer prompt without launching; map the missing-credential error to exit 2 while still re-raising every other exception; and either score the stub path in-process or correct the guide. If an in-process scorer is chosen, synthetic scores must never certify real-model convergence, and a model-free integration regression must protect that distinction. Close issue 556 only after issues 563, 564 and 565 are each closed or consciously dropped.

## Complexity and size
complex, size L. Three separate defects across the runner, the command, the ensemble and two guides, each with its own regression test, and the issue warns that a broad prompt rewrite or a catch-all exception conversion would be unsafe.

## Priority
P3. The owner set it to lowest priority on 2026-11-18, the wrapper is not used, and nothing else depends on these three defects being fixed. The defects are real, but they block no current work.

## Dependencies
Needs nothing. It blocks nothing. It should not be closed before issues 563, 564 and 565 are resolved, since it is their grouped record.

## Related issues
- 563, 564, 565: the three split-out defects, all open and in backlog.
- 354: the assignment the defects were reproduced under. UNVERIFIED: its current state was not re-read for this review.
- 571: the cleanup plan an earlier review said keeps the reflection command. UNVERIFIED: not re-checked here.

## Related PRs
None open. A search of all pull requests for 556, 563, 564 and 565 returned no pull request for these defects. The only recent change to the three files is the merged pull request 653 (`2ca022bf7`), which re-pointed task-file routes and did not touch these behaviors. Issues 563, 564 and 565 each report no closing pull request.

## Verification limits and negative evidence
Read-only. No `reflect` command was executed, so the exit codes and the scorer dispatch are confirmed from the source as it stands, not from a fresh run. The local captures named in the issue (`.dev/troubleshoot/bug-reflect-three-oddities-20261116025935/`) were not opened. One graph name lookup resolved to the wrong module and was discarded in favour of a direct read of the file. The architecture analysis is at `.dev/issuecleanup/g2/556/analyze/analyze-report.md`.
