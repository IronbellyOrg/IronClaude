# Reflect deviation patterns — bs346-ledger

## pre-TASK-WF-spec-20261108-181649 (UC-1, ledger variant plan for issue 346, 2026-11-08)
- Recurring pattern: a spec states a fact about the repo ("that test scans all of `src/`") and the plan delegates a required check to that test; the test scans `git ls-files` only, so new untracked files are never checked. Re-verify every spec claim about existing code before treating the plan as covered by it.
- Recurring pattern: a "full copy outside the changed blocks" requirement collides with a repo-wide rule the copied text already breaks (`src/superclaude/commands/spec-panel.md:220` names a `src/superclaude/examples/` path). Grep the source of any copy for the rules the copy must satisfy before planning the copy.
- Recurring pattern: adding a new command file breaks tests that pin the command set (`tests/recommend/test_routing_refresh.py:647-648`). Any plan that adds a command must run that test and name the owner's decision.
- New pattern: verbatim worker briefs ("write ONLY your output file", "do not edit the spec") can forbid the very writes a script-kept mechanism needs; an owner rule that briefs stay verbatim must be checked against every write the new mechanism makes.
- New pattern: a "skip when unchanged" predicate checked at the moment of writing a verdict is always true; say where the predicate is evaluated relative to later edits.
- New pattern: acceptance criteria of an earlier task that need a subcommand built in a later task (Task 2 needing `verify` from Task 3).
- Process note: both reviewers missed the two HIGH items (brief ownership, predicate timing); the Round 2.5 invariant probe found them. Keep the probe at standard depth.
