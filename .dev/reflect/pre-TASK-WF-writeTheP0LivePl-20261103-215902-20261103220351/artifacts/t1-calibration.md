# Wave 1D blind calibration of t1-card.md

Calibrator: confidence-calibrator agent, model class fable (disjoint from reviewer classes sonnet, haiku, opus). The card's self-report (0.85) was ignored; 27 file:line citations were spot-checked by Read.

| Dimension | Score | Reason |
|---|---|---|
| Citation grounding | 0.92 | Every plan, qa, managed-workspace, ledger, SKILL, WORKER-CONTRACT, orca-capabilities and CR-01 citation read matches its quote; runtime claims (F-001, F-009) agree with the session git snapshot; inferred items (F-006, F-012, F-013) are tagged. Defect: the header labels `Spec:` as `source.md`, but `spec:293` resolves only against `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:293`. |
| Coverage completeness | 0.75 | coverage-matrix.yaml records parsed 0, inferred 24, union 0.75 with per-row match_basis gap notes; rubric band 0.60-0.84. |
| Deviation-classification clarity | 0.65 | Each finding has one severity tied to a named executor rule, but none uses the rubric's Aligned/Refinement/Drift/Regression vocabulary; F-005 carries a split tag. |
| Risk surface coverage | 0.88 | Halt paths, archive blocking, false FAILs, infinite wait, cross-run contamination, resume double-start and Constraints blast radius are covered; no risk row for make sync-dev or setup failing in the disposable worktree beyond "skip to Remove". |
| Recommendation actionability | 0.90 | Every fix names the plan line, Constraints bullet, artifact or command to change; F-005's fix depends on --help output; F-015 and F-016 give no success check. |

Calibrated confidence (arithmetic mean): 0.82. Delta vs self-report: -0.03.

Escalation recommendation: ESCALATE to Tier 2 (C < 0.85; coverage 0.75 with six unmapped rows).
