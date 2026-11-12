# `cluster_v2` known weaknesses (not fixed)

Found while labelling the 50-pair sheet (`pair-labels/README.md`, `pair-labels/debate-split-pairs.md`). None is fixed in this work; each is a reason to read cluster output as telemetry, which is how the shadow mode already treats it (`cluster_agreement` never routes anything).

| # | Weakness | Evidence | Effect |
|---|---|---|---|
| W-1 | A bundled finding (one finding that states several defects) lands in one cluster with other findings that match only one of its parts. | The run `pre-TASK-WF-brainstormFixBri-...` (pair P09): one finding carries two different defects (S-3 and S-6) and clusters as one. The pair sampler skips same-reviewer pairs, so the 50-pair sheet cannot measure this. | The cluster count and agreement can read higher than the number of distinct defects. |
| W-2 | `refs_norm` can take an id such as `P1` out of text like "D-P1". | Pair P12 was merged wrongly because of it (`src/superclaude/cli/review/findings.py:29`, as found by the split-pair judge; re-read before relying on the line). | A false merge of two findings that share only a prefix-like token. |
| W-3 | A `spec:N` line reference is resolved against the short `source.md` brief, not the spec. | Found by the split-pair judge. | A spec line number can point at the wrong text, so a path-aware match on it is unreliable. |
| W-4 | The sheet's precision (0.84, 21 of 25) and recall (0.95, 21 of 22) are sample figures from AI labels. | `pair-labels/README.md`, "Result" and "Caveats". | They are not rates and not human-checked. |

Recorded numeric calibration is also thin: 0 of 689 recorded findings carry a numeric `finding_confidence` (`stage0a-report.md`), which is why the shadow calibrator brief now asks for one (SKILL.md section 4.3a, step 5).
