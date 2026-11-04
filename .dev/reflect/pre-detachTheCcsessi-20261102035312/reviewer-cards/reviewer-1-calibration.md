# Calibration Report — reviewer-1 card (analyzer, sonnet); calibrator opus (calibrator_diversity: full)

Persisted by the parent on receipt.

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.85 | all code citations re-read and match (ccsession:86, 688, 769-795, 832; tests:1354-1361, 574-614, 1416-1418; models.py:772-784; proxy:857-872; remediation-source:14, 22, 35); F8 INF ids not on tasklist line 21; F10 file list not checkable (no grep) |
| Coverage completeness | 0.90 | every task has a finding; AC1-AC6 and HC5 touched; no explicit coverage_pct |
| Deviation-classification clarity | 0.80 | one category each; F3 "Regression (inherent...)" hedged; F7/F8 "Aligned" with gaps |
| Risk surface coverage | 0.85 | F3 blast-radius reasoning; F1/F5 AC5 safety; F7 untested invariant; Task 1 descendant-listing timing only partly covered |
| Recommendation actionability | 0.85 | F1/F4-F8 concrete; F9/F11/F12 advisory |

C = (0.85 + 0.90 + 0.80 + 0.85 + 0.85) / 5 = **0.85** (self-reported 0.72; delta +0.13). Card-level verdict: STOP (C on the 0.85 floor).

Per-finding verdicts: F1 confirmed (tests:1355 sets HOME; ccsession:832 writes $HOME/.claude/cache); F2 confirmed (borderline LOW); F3 confirmed (code_digest at models.py:772-785 makes running shims stale; 6 ports at 769-770; "no free shim port" 793-795); F4 confirmed (`result["r"]` at tests:1404 raises KeyError if the thread failed); F5 confirmed with imprecision (the fixture runs SKILL_DIR's proxy, not a per-test copy; `kill -0 <pid>` works); F6-F9, F11, F12 confirmed; F10 confirmed (not fully checked). 12 confirmed, 0 wrong.

input_absent: assertions_path, now_iso.
