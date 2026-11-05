# Candidate fixes (Wave 3 step 4)

| # | Fix | Supporting cards (calibrated) | Verdict |
|---|---|---|---|
| F-A2 | bounded(): when `timeout` is absent, run the command as a background job, poll with `kill -0` and `sleep 0.2`, at the deadline TERM, 1 s grace, KILL, `wait`, `fail timeout`; plus compute `remaining` once and fail `timeout` when it is not positive (no `timeout 0`) | tier2-root-cause-analyst (0.92, STOP); tier2-quality-engineer (0.50, amendment only); tier1 card | consensus (the amendment is additive, same mechanism) |
| F-C1 | per-attempt directory: `attempt := conflict_attempt(<run-log events>, cycle_id)` (new pure core function) and `cycle_dir := <output-dir>/sync/<cycle_id>/a<attempt>/` at step 3; evidence, resolution.md, message and manifest under `<cycle_dir>`; validator `output_dir` is `<cycle_dir>`; every attempt's files kept | tier2-system-architect (0.83); tier1 card | consensus (single proposal; the architect card refines the tier1 draft by moving the count into the core) |

- No competing fixes and no split-pending cluster: both diagnosed variables were observed in this run (probe-evidence.out:4-8 and the post-fix section; P-1 and the restart tests).
- Wave 4 (adversarial debate) skipped: one viable fix per finding (skip condition "only one viable fix proposal"); all-converge row of the Wave 3 failure table applies, converged variable observed.
