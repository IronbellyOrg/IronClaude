# Owner rulings received during the /sc:implement run

The plan is pinned (its hash is fixed once the first task starts), so these rulings arrive as instructions from the coordinator, not as plan edits. Each one is copied verbatim from the coordinator message.

## 1. Arm B base file (received before Task 1; already written into the plan's Constraints before the pin)

See the plan's `## Constraints`, owner ruling on the 472-line Arm B base file.

## 2. Read-only script calls in review sessions (received 2026-11-08, during Task 3's review; delivery_9052d9c4051c)

> Owner ruling on scripted steps, for the whole team: Option A. Reviewer and reviser sessions may run ONLY read-only script calls, meaning calls that write no file anywhere (for example status, check --dry-run, fixcheck --dry-run or your script's equivalents), to self-validate and to use the spec's one repair turn. Any call that writes a file (begin, a real check that appends to the report, snapshot, enforce, apply, revert, ledger updates) is run by the coordinator as its own inserted step with its own brief template. A reviser writes any fix map or ledger content only INSIDE its own allowed output file (its disposition file, e.g. as a '## <script name> fixmap' block), and the coordinator's inserted step reads it from there. Plan the dry-run flags so they provably write nothing, and test that they write nothing.

How this run applies it:

- `stoprule.py` has one write path (`write_report`); every subcommand accepts `--dry-run`, which prints what it would write and writes nothing. Tests compare every file in the fixture folder before and after each `--dry-run` call.
- Writing subcommands (`begin`, `seal`, `apply-grades`, `apply-audit`, `finalize`) are coordinator steps; the reviewer session runs only read-only calls (`seal --dry-run`, `grade-prep`, `audit-prep`, `status`, `verdict`, `check`) and writes only its report's prose and its own ledger lines (claim, prior, checked). SKILL.md (Task 8) and the brief templates (Task 14) assign each step to its session.
- Usage errors exit 5 (stop on bad input) instead of argparse's 2, so the documented exit codes stay 0, 3, 4, 5, 6.
