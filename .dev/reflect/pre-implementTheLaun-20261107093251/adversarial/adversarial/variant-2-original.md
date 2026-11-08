# Reflect Reviewer — Deviation Findings (reviewer 2, qa, model class haiku -> claude-gw-tier2)

Paths below are shortened: PLAN = .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md ; DESIGN = docs/designs/sc-issue-launch-level-hook.md

Total deviations: 9 (Drift 5, Regression 4). Adherent tasks: 15 of 22. Tasks needing correction: 1, 16, 17, 18, 19, 20, 21.

| # | Category | Location | What diverged | Evidence | Severity |
|---|---|---|---|---|---|
| 1 | Regression | PLAN:36 | Task 1 lets L1 proceed while B-CTX stays blocked; its acceptance checks the verdict document, not a stop condition; Task 2 supplies synthetic fixtures instead of completing OB-H1. | DESIGN:359-360 requires stopping enforcement implementation when the distinction cannot be established, then OB-H1 before the skeleton. Fix: make enforcement tasks conditional on the evidence, or obtain an explicit scope decision for an L1-only increment. | HIGH |
| 2 | Drift | .dev/reflect/pre-implementTheLaun-20261107093251/artifacts/coverage-matrix.json:16 | INF-001 quote stops after the design reference; the matrix omits three source clauses (merged requirements, addendum, cheatsheet), so union coverage 1.0 is not established. | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1 | MEDIUM |
| 3 | Regression | PLAN:291 | Task 18 defines effective registrations as the exact command present under both events and hooks not globally disabled; a registration whose matcher excludes governed tools, or a prompt registration that cannot bind, would pass. Negative cases test missing, not present-but-ineffective, registrations. | DESIGN:342-352 | HIGH |
| 4 | Drift | PLAN:293 | Launch preflight omits the identity adapter's runtime prerequisites (UV, Linux process interfaces, effective identity-adapter registration). | DESIGN:561-565 | MEDIUM |
| 5 | Regression | PLAN:318 | Task 20 inspects an "owned shared hook file" and "recorded B-CTX contract marker" without defining identity, version, content or proof; no case rejects ineffective hook lookup, a nonexecutable hook, altered owned content or an unproven contract. | DESIGN:355 and DESIGN:510-514 (exact owned version/content; header alone is not proof) | HIGH |
| 6 | Regression | PLAN:305 | Task 19 fixes the printed L2 status as absent; Task 20 (PLAN:320) requires a successful launch when L2 is present and owned, so a successful L2-backed launch could still print "L2 absent". | DESIGN:354 | HIGH |
| 7 | Drift | PLAN:333 | Task 21 drops L2 implementation and tests even when B-CTX is GO, without authorization. | DESIGN:366, DESIGN:373-377 (O-22 yes), DESIGN:530-532 | MEDIUM |
| 8 | Drift | PLAN:266 | Task 16 requires panel F1-F8 regression cases but no resolvable source holds their definitions; the panel review file does not exist. | DESIGN:311; file .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md is absent | MEDIUM |
| 9 | Drift | PLAN:278 | Task 17 assigns only T-MSG-1 to T-MSG-3; T-MSG-4 to T-MSG-6 (competing-class precedence) are not assigned. | DESIGN:298; .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md:1102-1104 | MEDIUM |

Task-by-task acceptance: tasks 2 to 15 and 22 adequate; 1, 16, 17, 18, 19, 20, 21 not adequate (reasons as in the findings above).

T1 card claims not confirmed: coverage_pct_union 1.0 as complete coverage; unmapped_requirements_union []; INF-001 to Task 22 as substantive coverage; INF-002 to Task 1 as a functioning gate (only its first position is confirmed); INF-003 to Task 18 as coverage of all named code areas; S_dev_density 0.0. Confirmed: 22 tasks, empty parsed-id list, parsed-sparse.

Evidence limits: no diff exists; nothing was run; the missing panel review prevents confirming F1-F8.

<!-- calibration: mean_C 0.71, calibrated_confidence 0.65, calibrator opus (degraded diversity) -->
