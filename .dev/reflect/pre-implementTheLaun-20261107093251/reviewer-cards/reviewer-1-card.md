# Reflect Reviewer — Deviation Findings (reviewer 1, analyzer, model class sonnet -> claude-gw-tier1b)

Paths: PLAN = .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md ; DESIGN = docs/designs/sc-issue-launch-level-hook.md ; OW = src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py

Total deviations: 16 (Regression 0, Drift 14, Necessary 1, Authorized 1). No finding is HIGH. Finding 4 becomes Regression-class if Task 20 is built as a header-only check.

| # | Category | Location | What diverged | Evidence | Severity | Fix |
|---|---|---|---|---|---|---|
| 1 | Drift | Task 1 (PLAN:32-45) | Gate only records a verdict ("L1: PROCEED"/"L1: STOP", PLAN:36); no later task depends on or is conditioned on it, so a STOP would not stop Tasks 2-22. | PLAN:36; DESIGN:359; source.md:1 | MEDIUM | Make enforcement tasks depend on a PROCEED verdict and say what STOP triggers. |
| 2 | Drift | Task 12 (PLAN:209-220) | Lists only Task 10 as dependency (PLAN:211); design orders registration after classifier work. | PLAN:211; DESIGN:364-365 | LOW-MEDIUM | Add Task 11 as dependency. |
| 3 | Necessary | Task 12 | Guard entry inserted before the identity hook in PreToolUse; justified, does not contradict the pinned test while identity stays last. | DESIGN:339; tests/cli/test_install_hooks.py:844; src/superclaude/hooks/hooks.json:75-106 | LOW | None; keep test at line 844 as acceptance check. |
| 4 | Drift (Regression if header-only) | Task 20 (PLAN:318) | "Owned hook plus recorded marker" undefined; design requires expected version and both registrations effective (IR-4); a header-only or presence-only check would contradict it. | PLAN:318; DESIGN:510-514,355; OW:704-725 | MEDIUM | Define the marker (version string plus registration check) and a test showing a stub fails it. |
| 5 | Drift | Tasks 19, 20 (PLAN:287-325) | Task 19 adds an L2-absent status line; Task 20 refuses the launch when L2 is absent, so the line is dead output. | PLAN:287-325; DESIGN:510-514,355 | MEDIUM | State one behaviour per case; drop or gate the line. |
| 6 | Drift | test fallout | launch_scene writes a stub "#!/bin/sh" hook with 31 uses; tests at 1296-1305, 1308-1314, 1317-1324 encode warning-only behaviour; the enforcement_hook result field (docs/designs/sc-issue-claim-pipeline-flag.md:132) has no task; lead: installer script-list tests at tests/cli/test_install_hooks.py:102 and tests/unit/test_cli_install.py:139 may need the new script. | tests/skills/test_issue_orca_worktree.py:994-1013,1296-1324; pipeline-flag.md:132 | MEDIUM | Add a task updating launch_scene, the three warning tests and the two installer list tests. |
| 7 | Drift | Task 18/19 ("--pipeline none unaffected") | Not testable at script level: --pipeline defaults to worktree in the command file; script --level only takes worktree|full so none never reaches cmd_launch. | src/superclaude/commands/issue.md:43; refs/claim.md:115,136; OW:1048,1058 | LOW | Test at claim-protocol level or assert cmd_launch is not called. |
| 8 | Drift | Task 22 (PLAN:340-351) | Docs update omits src/superclaude/commands/issue.md (flag text, Wave 8). | issue.md:43; .dev/issues/394/issue-summary.md:22 | LOW | Add issue.md to Task 22. |
| 9 | Authorized | Tasks 18-20 | Refusing a governed launch when guard or L2 is absent exceeds the PR 425 warning; the design requires it. | DESIGN:355,514; OW:986-989 | LOW | Note the behaviour change in the PR description. |
| 10 | Drift | task list | IR-3 (pipeline.json documentation only) has no task. | docs/designs/sc-issue-claim-pipeline-flag.md:55; DESIGN:339-355 | LOW | One line in Task 22. |
| 11 | Drift | Task 9 | Drops the superclaude.* command form the design lists. | DESIGN:102-127 | LOW | Add or record why out. |
| 12 | Drift | Task 19 | Release-instruction text takes session id from the wrong source; design binds via sessions/<sid>. | DESIGN:81,133-175; launch-job-identity.sh:435 | LOW | Point at sessions/<sid> or the nonce. |
| 13 | Drift | Task 12 | T-REG-3 negatives do not match the AC-map module. | merged-requirements.md:971-1108 | LOW | Same module. |
| 14 | Drift | Task 16 | Pins non-git leaks as expected behaviour. | DESIGN:133-175 | LOW | Mark as known-gap/xfail. |
| 15 | Drift | Task 20 | Forward reference to Task 21's L2 disposition. | PLAN:318,329-338 | LOW | Reorder or add dependency. |
| 16 | Drift | task list | No OB-CTX probe built (covered by the no-live-observation constraint). | DESIGN:489-565; PLAN:36 | LOW | State in Task 1 that the gate is evidence-based. |

T1 card claims not confirmed or only partly: F-2 is true but the design mandates the refusal (Authorized, not a plan choice); F-5 confirmed but already covered by pipeline-flag.md:55; F-6 partly confirmed (check order exists in cmd_launch, OW:937,941,986-989; card misses launch_scene and test 1308 fallout); F-7 confirmed (spec-panel review.md and 20261106-l2-prepush-decisions absent; authorizedNarrow artifacts exist); risk statements are judgment calls.

Advisory correctness gaps: (1) Task 5 "jq removed, bound session blocks" defines no mechanism for detecting a bound session without jq (DESIGN:133-175; launch-job-identity.sh:435); (2) T-SPD-3 timing assertion is flake-prone and the baseline moves once any claim creates the store (analyze-hooks.md F2; launch-job-identity.sh:20-24,566).

Evidence limits: installer test-list hits at test_install_hooks.py:102 and test_cli_install.py:139 not read in context; Tasks 2-4, 6-8, 10-11, 13-15, 17 not re-verified beyond cross-checks.

<!-- calibration: mean_C 0.66, calibrated_confidence 0.62, calibrator opus (degraded diversity) -->
