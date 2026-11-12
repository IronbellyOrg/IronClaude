# Calibration Report: reviewer-1-card.md (Tier 2)

<!-- Returned by confidence-calibrator (opus, read-only), persisted by orchestrator on receipt 2026-11-08T03:49Z. -->

**Calibrated C = 0.83** (self-reported 0.70, delta +0.13). Verdict ESCALATE (`low_confidence`, rubric C < 0.85). Citation groups checked: 16 (6 Orca-side): 13 held, 1 partial, 0 failed, 2 unverifiable.

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| 1. Citation grounding | 0.90 | Nearly every finding cites file:line; no checked citation wrong; unproven items listed in section 5. |
| 2. Coverage completeness | 0.90 | Every source item mapped (scope (1)-(3), 3 out-of-scope, 3 respect); all 8 tasks touched. Test line numbers unchecked. |
| 3. Deviation-classification clarity | 0.65 | One label per departure with reasons, but "Necessary deviation"/"Authorized expansion" instead of rubric {Aligned, Refinement, Drift, Regression}; some hedged rows. |
| 4. Risk surface coverage | 0.85 | Timing race, orphaned worktree, scanner holes, hook ordering, uncovered actors, stale fake calls. Missed: during the R1-3 window the close step could close an agentless terminal the user opened. |
| 5. Recommendation actionability | 0.85 | Every finding names a targeted change; R1-10 either/or; R1-13 lacks a pass condition. |

Mean (0.90+0.90+0.65+0.85+0.85)/5 = 0.83.

## Citation spot-checks

Held: block-bare-python.sh:97, :106, :132-134, :48-61, :61; orca_worktree.py:594-613, :611, :628 (no parse of `created.out` in 594-644), :521-524, :934-936, :941, :950, :954-975, :20-30; CLAUDE.md:305, :307-324, :320, :333-337; WORKER-CONTRACT.md:62; launch-job-identity.sh:14-15; install_hooks.py:85; plan :19, :20, :34 (exactly 12 cases), :68, :103; IronOrca src/main/runtime/runtime-local-worktree-terminal-startup.ts:209-210, :187-201, :215-222; IronOrca src/shared/runtime-terminal-contracts.ts:38-39; IronOrca src/cli/help.ts:88-89.

Partial: tier1-observation.md:116, :121 are the seed rows; the "~2.3 s" figure is not on those lines (:117 says "about 2 s").

Unverifiable: explicit-terminal-close-stops.ts:226, :246-249; terminal-close.ts:12-13 (not found at tried paths). The `--tab` claim is still backed by help.ts.

## Notes

- R1-4's "keys sit under `result`" is not shown by the cited startup.ts lines (it rests on the test fixture LAUNCH_OK at test_issue_orca_worktree.py:970).
- Mapping section 4 labels to rubric categories would raise dim 3 to ~0.85 and C to ~0.87.
