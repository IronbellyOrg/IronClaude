# Calibration Report: reviewer-2-card.md (Tier 2)

<!-- Returned by confidence-calibrator (opus, read-only), persisted by orchestrator on receipt 2026-11-08T03:50Z. -->

**Calibrated C = 0.89** (self-reported 0.91, delta -0.02). Citations: 22 held, 0 failed, ~11 unchecked. No C-driven escalation (C >= 0.85); card already Tier 2.

## Per-dimension scores

| Dimension | Score | Evidence |
|---|---|---|
| 1. Citation grounding | 0.92 | All 22 spot-checks held. R2-5's claim that Task 3's happy path is the opaque `created_scene()` fixture is inferred; plan :57 says only "a created-worktree run against the fake Orca". |
| 2. Coverage completeness | 0.88 | All 8 tasks, scope items (1)-(3) mapped; T1 F1, F2, F3, F5, F8, F9, F11 addressed; F4, F6, F7, F10 not mentioned. |
| 3. Deviation-classification clarity | 0.85 | One category per deviation with rationale; labels not the rubric set. |
| 4. Risk surface coverage | 0.90 | R2-5, R2-6, R2-3, R2-9, R2-8, named test breakage. Missed: the plan's guard (close only when exactly one agentless terminal is listed, plan :53) not weighed against R2-5. |
| 5. Recommendation actionability | 0.90 | Concrete changes and tests; ordered action. Success criteria mostly implied. |

Mean (0.92+0.88+0.85+0.90+0.90)/5 = 0.89.

## Spot-checks (all held)

orca_worktree.py:611-614, :618-645, :504-513; test_issue_orca_worktree.py:365-387 (`created_scene` returns `"opaque, not json"` at :376), :552-561 (FO-11 asserts `warning is None` at :559), :607-618; plan :53-57, :53, :42-47, :88-103, :20, :75; launch-job-identity.sh:475-481 (`shlex.join` wraps the original command; "concurrent hook rewrite ordering … unverified"); docs/user-guide/commands.md:367, :379, :394; HOW-WE-WORK.md:329; source.md:1; block-bare-python.sh:97-106, :130-134; SKILL.md:90-92, :124-136, :170, 105-134; refs/claim.md:131-136; test_orca_session_launch_guidance.py:17-31; sc-issue-claim-pipeline-flag.md:39.

Unchecked: test_block_bare_python.py:224-247; test_install_hooks.py:763-819; test_cli_install.py:891-901; test_freshness_subagent_start_policy.py:105-114; test_issue_orca_worktree.py:794-820; test_issue_protocol.py:431-447, :487-515, :503-514; test_issue_command.py:169-179; test_verify_sync_hooks.py:101-111; install_core.py:70-75; main.py:365.

## Severity caveats for Wave 4

- R2-5 HIGH is the upper bound: the plan already closes only when exactly one agentless terminal is listed; residual risk depends on unverified Orca setup-tab layout. MEDIUM-HIGH defensible.
- R2-6 HIGH is the upper bound: the new-row filter (new row id, `issue-<N>` name, directory on disk) makes a foreign-repo row unlikely; the ordering gap is real.
