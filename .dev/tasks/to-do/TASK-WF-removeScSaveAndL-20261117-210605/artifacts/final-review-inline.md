# Whole-plan review (inline, not independent)

`/sc:implement` asks for a fresh independent reviewer subagent per task and for the archive FINAL. This session launches no subagents (standing user instruction), so each task was checked inline by the implementing session against its own acceptance criteria and the check logs `t1-check.log` to `t8-check.log` in this folder. That is a weaker check than the protocol intends. Consequences:

- The ledger `progress.md` holds `start` and `complete` lines for T1 to T8 and no `FINAL:` line.
- The package is not archived (the helper needs a `FINAL: pass`); it stays under `to-do/`: archive-blocked by design, not by a defect.
- Facts that came up during the work and that the plan did not list: the routing-table test pinned the removed rows' wording (Task 5 covers it); the roadmap skill had six `sc:save` clauses, not five (Task 4); the architecture reference carried the count of seven in two more places (Task 8). All were fixed inside the task that owned the file.
- The independent checks that did run are the full test suite, lint, format, verify-sync, the leftover search and the throwaway-HOME install (see `.dev/issues/v6-save-load/REGRESSION-GATE.md`), plus the Augment and Codex reviews on the pull request.
