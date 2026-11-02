# Calibration Report (Tier 1 card)

**Card**: t1-card.md  **Rubric**: refs/reflection-rubric.md  **calibrator_model_class**: opus (reviewers sonnet, haiku) -> calibrator_diversity: full
**Source**: confidence-calibrator agent, persisted by the parent on receipt.

| Dimension | Score | Justification (condensed) |
|---|---|---|
| Citation grounding | 0.88 | tasklist lines 19-22, 32, 55-56, 67-70, 82 and test_ccsession_tiers.py:1360 verified; two supporting claims uncited ("template forbids verification-only tasks"; "parent pid is unchanged", correct but uncited) |
| Coverage completeness | 0.88 | matcher 31/44 = 0.7045 confirmed; manual check agrees effective coverage 43/44 with INF-044 named; matched rows not checked for narrowing (INF-022 "ends with message_stop" vs Task 1 "contains") |
| Deviation-classification clarity | 0.80 | 4 rows clean; HC5 gap not categorized; missing small deviations: Task 5 grep pattern drops the `SKILL_DIR / "ccsession"` alternative of R:22; "kill the root group" became "kill any remaining root process"; added checks (`bash -n`, pgrep leak check, "no temp files") |
| Risk surface coverage | 0.72 | main execution risks covered; missing: after `os.setsid()` a Ctrl-C to a non-interactive run no longer reaches a directly started shim (fixture leak on hard interrupt); no check that code after ccsession:804 depends on the background job (it does not use `$!`); Task 1 timing (1 s vs 4 s pause); subreaper/macOS reparenting |
| Recommendation actionability | 0.80 | Rec 1 actionable with placeholders; Rec 2 restates Task 3 AC; Risks 2-3 have no recommendation |

C = (0.88 + 0.88 + 0.80 + 0.72 + 0.80) / 5 = **0.82** -> ESCALATE (low_confidence; C < 0.85). Rule 4 (S_domains = 3) also forces ESCALATE (observed by the calibrator, decided in tier_decision.yaml).
