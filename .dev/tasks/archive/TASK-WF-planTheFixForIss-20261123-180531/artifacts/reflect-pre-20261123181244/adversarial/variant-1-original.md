# Reflect Reviewer - Deviation Findings
Reviewer persona: analyzer
Requested model: sonnet
Independent calibrated confidence: 0.73 (reviewer-1-calibration.md); calibrator_diversity=degraded. Resume consequence disputed by calibration, do not inherit as fact.
Grounding root: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s (live worktree, reviewer_isolation=disabled)
Diff scope: plan only, no implementation
Verdict: PASS (with notes)
Total deviations: 3 (0 Blocking, 2 Medium, 1 Note)

## Deviations
| # | Category | Location | What diverged | Evidence | Severity |
|---|---|---|---|---|---|
| 1 | Drift (plan gap) | Plan Task3 | Medium: no rule for telling bundled default from caller template. The edit sees inline_job after preflight. A caller template equal to default appears indistinguishable but renders same string, harmless. Suggested explicit lens-name/template-equality/absent-compare_files rule. Risk named, rule not. | commands.py:929; preflight.py:540-543; commands.py:2134-2155 | MEDIUM |
| 2 | Drift (plan gap) | Plan Task4 | Medium: wizard-guide.md:216 still lists /code-review as lens follow-up; no lens will hand off to it after fix. Four known refactor-specific stale occurrences are correct; classify broader list as deliberately out of scope in documentation-check.txt. | docs/swarm/wizard-guide.md:216 | MEDIUM |
| 3 | Note | Plan Task3 | Note: reviewer asserts resume never supplies compare_files, so resumed refactor-find would render literal {compare_files}; pre-existing, explicitly outside plan. | commands.py, compare_files grep only2142 | LOW |

## Adherence summary
Scope INF001, INF002, INF003 plus Task3 count/path guards and Task4 doc count. All three slice items covered in substance. Authorized0, Necessary0, Drift2 minor, Regression0, Note1. Findings1/2 are clarity gaps, not missing obligations.

## Why no blocker
- Changing refactor_find.py:53 to /sc:adversarial --compare keeps nonsuspect rule intact. _validate.py:417-429 forbids suspect_files for suspect=False; proposed template has none. adversarial.md:39 existing-file count matches plan guard.
- Existing succeeded_final_paths at commands.py:2129-2144 supports scoped mapping. Empty template can suppress suggestion (reduce.py:460-461 and test_contract_emission.py:583-597).
- setdefault keeps caller substitutions. Caller compare_files visible in inline_job. Bare-review golden all-success/return-contract.yaml:28 requires existing-review prefix. Sibling protection explicit and tested by plan.
- No existing tests/swarm assertion pins code-review/--apply.
- New availability check should fail today due missing packaged command; argument-list check should fail due prefix.

## Limits
Ran nothing; proposed red failure is source-based inference, not observed test output. Did not glob code-review.md, trusted plan's absence statement. Helpers only seen through grep. Used Read/Grep, not codegraph despite fresh index. No advisory correctness gaps.

## Recommendation (reviewer's, not execution authorization)
Proceed to execution. Optional default-detection sentence not required for PASS. Parent must still complete protocol and obtain separate execution authorization. No files changed.
