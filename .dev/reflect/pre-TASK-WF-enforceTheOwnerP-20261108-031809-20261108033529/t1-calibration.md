# Calibration Report: Tier 1 card (t1-card.md)

<!-- Returned by confidence-calibrator (opus, read-only), persisted by orchestrator on receipt 2026-11-08T03:44Z. -->

**Calibrated C = 0.72** (self-reported 0.80, delta -0.08). **Recommendation: ESCALATE (low_confidence; rubric C < 0.85).**

## Per-dimension scores (reflection rubric, C = arithmetic mean)

| Dimension | Score | Justification |
|---|---|---|
| 1. Citation grounding | 0.80 | 20 local citations checked held; 2 overstated; 7 unverifiable (6 IronOrca citations given as bare file names, tier1-observation.md:54). F5 and Task 3 feasibility rest on the unverified ones. Hook interaction honestly [INFERRED]. |
| 2. Coverage completeness | 0.80 | Every source requirement mapped to a task or Constraint; all 8 tasks reviewed; scope-item-2 deviation and INF-014/015 false positives caught. No coverage percentage or gap list in the card itself. |
| 3. Deviation-classification clarity | 0.35 | Rubric categories not used ("documented deviation", "undocumented consequence" instead). Suggested reading: scope-item-2 = Refinement (owner-approved, plan :20); F2 = Drift risk; F6 = Drift (undocumented consequence). |
| 4. Risk surface coverage | 0.80 | F1 bypass, F2, F6, F10, launch-identity interaction surfaced. Not checked: other installed primitives/docs that tell agents to run a bare `orca worktree create` (would be blocked by the new hook). |
| 5. Recommendation actionability | 0.85 | All 11 findings name a target and change; F1/F11 give test criteria; F4, F7, F10 lack a verifier. |

Mean: (0.80+0.80+0.35+0.80+0.85)/5 = 0.72. With dim 3 at 0.55, C = 0.76; verdict unchanged.

## Citations checked (20 held, 0 failed, 2 overstated, 7 unverifiable)

| Citation | Result |
|---|---|
| install_hooks.py:42, :85 | held |
| hooks.json:91, :101 | held |
| block-bare-python.sh :130-134, :106, :48-61, :61 | held (F1 sound) |
| launch-job-identity.sh :14-15 | held |
| orca_worktree.py :594-613, :614-646, :611/:628 | held |
| test_issue_orca_worktree.py :794, :800-817, :970 | held |
| test_issue_protocol.py :325-332, :341, :349, :503-514 | held |
| SKILL.md :84/:148, :91, :105-136, :126, :150, :170 | held (F2 real) |
| claim.md :17, :123 | held |
| CLAUDE.md :305, :335-337 | held (F4 real) |
| design doc §8.3 at :175 | held |
| test_verify_sync_hooks.py :95-111 | partly held (mutates `_FRESHNESS_SCRIPTS`; hooks.json mutation not shown in range) |
| F3 "SKILL.md range wrong" | overstated: plan's "around 105-134" matches the contract block; only prose :136 outside |
| F4 "Task 6 edits only :312, :320" | slightly overstated: plan also edits :307-310; contradiction holds |
| IronOrca citations (x6), tier1-observation.md:54 | unverifiable (no directory given) |

## Tier 2 asks

- Verify IronOrca citations under /home/coder/workspaces/IronOrca/ with full paths.
- Search installed primitives and docs for bare `orca worktree create` instructions the new hook would block.
- Classify F2, F6 and the scope-item-2 deviation with the rubric categories.
