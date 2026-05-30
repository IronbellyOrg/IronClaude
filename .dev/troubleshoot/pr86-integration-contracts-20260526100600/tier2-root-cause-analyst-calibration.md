# Calibration Report — root-cause-analyst (Tier 2)

**Card under calibration**: `/config/workspace/IronClaude/.dev/troubleshoot/pr86-integration-contracts-20260526100600/tier2-root-cause-analyst-hypothesis.md`
**Rubric**: `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`
**Card tier**: 2
**Timestamp**: 2026-05-26T10:20:00Z
**Captured from**: confidence-calibrator agent output (agent could not write to disk — safety constraint).

## Per-dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 0.5 | `_extract_identifiers` block verified at HEAD lines 347-356 (matches PR sha off by ~65 lines). F2/F4/F5 secondary citations reference `contract_idents`, `_signature_subsumed`, fixture comment — none present in current HEAD's 357-line file. Card is pinned to sha `67ab0af5`; calibrator lacked Bash to `git show` and verify. |
| Symptom coverage | 1.0 | All 5 findings addressed with causal chains. F1 root cause; F3, F5 traced to same gap; F2, F4 declared independent with reasoning. |
| Reproducibility fit | 1.0 | Card provides `re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", "FR-S10-02") == ['S10']` — deterministic Python expression. |
| Fix directness | 1.0 | Touches exactly `_extract_identifiers` + one downstream comparison. F2/F4 explicitly split off — no scope creep. |
| Domain coherence | 1.0 | Single domain: identifier extraction + string matching, one module. |

## Confidence

- **Self-reported**: 0.88
- **Calibrated**: 0.90
- **Delta**: +0.02 — card's self-report was pulled down by F2-independence uncertainty; calibrator rewards mechanical strength of the F1+F3+F5 chain and the discipline of splitting off F2/F4.

## Verdict

- **STOP** (Tier 2 already; no further tier in this protocol for hypothesis cards).
- Calibrated 0.90 ≥ 0.85, domain=1.0, reproducibility=1.0 → would NOT have escalated if this were a Tier 1 card.
- **Strong fix proposal — ready for implementation as a focused PR.** F2/F4 deferred to separate PRs as the card recommends.

## Notes

- F5 test fixture citation is factually absent at current HEAD (lines 130-134 are `class TestDispatchPatternDetection:`). If sha `67ab0af5` contained the cited content, it was removed before current HEAD — or it exists in the PR branch. Orchestrator's grep confirmed `git show 67ab0af5:tests/roadmap/test_integration_contracts.py` DOES contain the `TUIBBS-scp-inspired` comment.
- Card honestly surfaces canonicalization-as-contract-change risk and the `S10` + `FR-S10-02` overlap concern.
