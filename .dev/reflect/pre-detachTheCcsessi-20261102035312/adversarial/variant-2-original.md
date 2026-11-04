# Reviewer 2 card — qa (haiku slot -> glm-5.3), reflect-reviewer agent; persisted by the parent on receipt

Scope: QA slice INF-017..037, INF-043, INF-044 (23 spec units). Total deviations: 6 (0 Regression, 2 Drift, 4 Refinement). Self-reported confidence: 0.82.

| # | Category | Location | What diverged | Evidence (file:line) | Severity |
|---|---|---|---|---|---|
| 1 | Drift | tasklist:69 (INF-032) | Task 4 AC says orca_close_repro.py "writes its output to .../live-check/after.txt", but the script only prints to stdout (writes only the shim copy and fake claude inside SCRATCH); after.txt appears only with an unstated redirect | tasklist:69; remediation-source.md:23; live-check/orca_close_repro.py:75-165 | MEDIUM |
| 2 | Drift | tasklist:17-23 (INF-044) | HC5 off-path review ("PR reviewers and /sc:reflect --mode post") absent from tasks and Constraints | remediation-source.md:35; tasklist:17-23 | LOW |
| 3 | Refinement | tasklist:32 (INF-022) | "ends with message_stop" weakened to "contains"; follows existing test convention | tasklist:32; remediation-source.md:14; tests/unit/test_ccsession_tiers.py:1405 | LOW |
| 4 | Refinement | tasklist:82 (INF-029) | Task 5 grep drops the `SKILL_DIR / "ccsession"` alternative; equivalent today (both files also match `ccsession-tag`) but contingent | tasklist:82; remediation-source.md:22; tests/unit/test_ccsession_tiers.py:30; tests/unit/test_ccsession_tag.py:28 | LOW |
| 5 | Refinement | tasklist:20 (INF-035, INF-037) | AC5 "nothing under ~/.claude edited" and "install/update not run" enforced only by a Constraints bullet, no task-level evidence | tasklist:20; remediation-source.md:25 | LOW |
| 6 | Refinement | tasklist:70 (INF-036) | Task 4 adds a live pid-stability check on 4013/4114 (in-scope strengthening of AC5); health reports pid | tasklist:70; remediation-source.md:25; local-gateway-alias-proxy.py:536 | LOW |

Adherence (QA slice): 16 Aligned, 5 Refinement, 2 Drift, 0 Regression.

Answers to the brief: T1 "covered" judgments hold for INF-022, INF-026/028, INF-043; INF-044 gap confirmed. Every AC is enforced by task ACs except AC5's two config clauses (Constraints-only) and AC3's after.txt wording (untestable as written). Phase ordering verified: after Task 3 alone the shim stays a pid-tree child, so Test A keeps failing until Task 4; fixture terminate() still works (tests:611-613). No `$!`/`jobs`/`wait` in ccsession disturbed by the subshell; traps at ccsession:1182, 1225 are INT handling outside setup_shim. Matrix completeness: every requirement-bearing span of remediation-source.md is in the matrix; only INF-044 is unmapped. Residual: test_ccsession_tag.py not fully read (process-group dependence not excluded; Task 3 full-file AC would catch it).
