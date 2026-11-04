# Wave 3C blind calibration of reviewer-2-card.yaml

Calibrator: confidence-calibrator, model class fable (disjoint from reviewer classes). All 19 cited lines Read; every quote matches. Card self_confidence (0.78) ignored.

| Dimension | Score | Reason |
|---|---|---|
| Citation grounding | 0.95 | Every claim verified on Read; the "brief git-status hunk" cite is transient but matches the session git status. |
| Coverage completeness | 0.85 | All 5 tasks and the shared procedure; spec 7.2 step 4 accepted on the AC-0.4 adaptation clause without reading spec:286-290. |
| Deviation-classification clarity | 0.75 | One stance and severity per finding; the two blocking upgrades rest on a strict-literal reading of qa.md:310 that ignores lc<N>-remove.json as proxy evidence. |
| Risk surface coverage | 0.85 | AC literalism, unrecorded live state, tool timeout, grep exit code; misses that Task 5's `git add .dev/tasks` also stages the untracked reflect folder, compounding R2-01. |
| Recommendation actionability | 0.90 | Every fix names a file, command or wording; R2-07's fix is partly directional. |

Calibrated confidence: 0.86.

Per finding: R2-01 sound; R2-02 sound (blocking defensible but the strongest reading); R2-03 sound; R2-04 sound; R2-05 sound; R2-06 sound; R2-07 sound; R2-08 weak (spec:301 carries the same ambiguity; suffix match is the obvious reading; minor is right); R2-09 sound.
