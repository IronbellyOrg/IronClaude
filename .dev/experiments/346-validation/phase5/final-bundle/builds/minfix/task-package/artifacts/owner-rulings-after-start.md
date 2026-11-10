# Owner rulings received after /sc:implement started (2026-11-08)

The plan was frozen (Task 1 complete, Task 2 in review), so these rulings are applied in the work and each departure from a frozen acceptance criterion is recorded as a scoped `Ruling:` line in `progress.md`.

## msg_d5c44f4fbc85 — Owner correction: variant base is the 472-line Arm B file

Owner correction to the earlier Unattended ruling, for the whole team. The variant command's base is the 472-line Arm B file, byte for byte: /home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/inputs/tool-text/spec-panel-post427-95f2c6e4.md (read-only; first 12 characters of its sha256 are c8d80346a96c). The current src/superclaude/commands/spec-panel.md minus its "## Unattended mode" section is 474 lines, not 472: two more lines (the second Usage line advertising --unattended, and the sentence explaining --target-release) must also be absent. So: start the variant by copying that 472-line file, then apply only this team's change. Wherever your plan, tests or INSTALL.md say "copy of src/superclaude/commands/spec-panel.md", use that file as the base instead, and drift tests compare against it. The existing src/superclaude/commands/spec-panel.md is NOT changed. The base inherits a line that contains "src/superclaude" (the examples path); the no-src/superclaude test must assert that the variant adds no occurrence beyond those in the base. Adding the variant to _POST_REFRESH_ADDITIONS in tests/recommend/test_routing_refresh.py is allowed. If you already copied from src/superclaude/commands/spec-panel.md, redo the base copy from the 472-line file and re-run your drift tests against it. Reply with an ack when applied.

Verified: that file is byte-identical to `git show 95f2c6e4:src/superclaude/commands/spec-panel.md` (472 lines, sha256 prefix c8d80346a96c).

## msg_9e319d331e9b — Owner ruling: read-only script calls are allowed in review sessions

Owner ruling on scripted steps, for the whole team: Option A. Reviewer and reviser sessions may run ONLY read-only script calls, meaning calls that write no file anywhere (for example status, check --dry-run, fixcheck --dry-run or your script's equivalents), to self-validate and to use the spec's one repair turn. Any call that writes a file (begin, a real check that appends to the report, snapshot, enforce, apply, revert, ledger updates) is run by the coordinator as its own inserted step with its own brief template. A reviser writes any fix map or ledger content only INSIDE its own allowed output file (its disposition file, e.g. as a '## <script name> fixmap' block), and the coordinator's inserted step reads it from there. Plan the dry-run flags so they provably write nothing, and test that they write nothing.

## Coordinator answer to the worker's `ask` (approval of option A)

Approved: option A. Keep running the frozen plan and apply both owner rulings in the work itself, exactly as you describe (472-line base for the repo file and the experiment build file; hash and plain check in review sessions, snapshot and check --enforce as coordinator-inserted steps with their own brief templates in Task 8). Conditions: (1) record each departure from a frozen acceptance criterion as a scoped Ruling line in the ledger citing this message as the owner's acceptance; (2) do not weaken or delete any test to make a task pass; the drift and no-new-src/superclaude tests must compare against the 472-line base; (3) list every departure in INSTALL.md and in your worker_done body so the final report can show what differs from the plan.

## Effect on this script

`hash` and plain `check` write nothing (tested in Tasks 1 and 2). `snapshot` and `check --enforce` are unchanged in the script; they are now run by the coordinator as inserted steps, not by review or reviser sessions.

## Coordinator answer after the Task 3 halt (`T3: halt review=5 reason=ladder-end`), 2026-11-08

Approved: option C. Fix F5.1 and F5.2 now, then run one fresh operator review of Task 3. Conditions: (1) F5.1 (silent duplication or exit 1 with an undeclared code fence) must be fixed in the code, not documented away; add a regression test for the failing case; (2) F5.2 may be fixed either by detecting joined table rows and paragraphs or by correcting the docstring to say exactly what is detected, in which case list the undetected join case as a known limit in INSTALL.md; (3) do not weaken or delete any test; (4) if the fresh review fails, Task 3 halts again: stop and report with the halt record (option A) and do not build Tasks 4 to 8. If it passes, record the operator Ruling in the ledger citing this message and continue with Tasks 4 to 8.
