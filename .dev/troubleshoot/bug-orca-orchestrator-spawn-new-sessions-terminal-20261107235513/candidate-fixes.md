# Candidate fixes (Wave 3 index)

| # | Fix proposal | Supporting card(s) | Calibrated | Verdict |
|---|--------------|--------------------|-----------:|---------|
| F1 | Add one sentence next to CLAUDE.md:308 and :320: a bare `orca worktree create` leaves only an empty plain terminal; for a Claude session add `--agent claude` or follow with `agent launch --agent claude`; never `terminal create` for an agent; allow the `/sc:issue --claim` two-step path | Tier 1 root-cause-analyst; Tier 2 quality-engineer (adds `worker-start --worktree new-top-level`) | 0.30 each | `split-pending` (P1 vs P4): both cards propose the same edit, but the variable they share was not observed in the reporter's run, so it is not marked consensus; no debate |
| F2 | Make `superclaude install` insert the Orca session-launch block (marker-delimited) into an existing ~/.claude/CLAUDE.md instead of skipping it | Tier 2 system-architect | 0.30 | outlier (a different layer: delivery, not wording); complementary to F1, not a competitor |
| F3 | None (refutation: a failed `--agent claude` start does not leave an unreported empty tab) | Tier 2 root-cause-analyst | 0.30 | outlier (no fix); keeps P4 narrowed, not excluded |

Wave 4 (adversarial debate): not run. No two strong competing fixes exist (every card calibrated 0.30), F1 and F2 act on different layers, and the P1-vs-P4 disagreement is decided by the probe pair M-QE in diagnosability-tasklist.md (Wave 3 step 4.5), not by a debate.
Escalation reason recorded: `low_confidence` (Wave 2); cluster flag `split-pending` (P1 vs P4).
