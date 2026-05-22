# Calibration Report

**Card under calibration**: /config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/iteration-2/fixtures/confidence-calibrator/C1-under-confident-card.md
**Rubric**: /config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-05-21T00:00:00Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 | All three cited file:line refs spot-checked and verified: `commands.py:1476` literally contains `output_dir=output_dir,`; `commands.py:1406` is `def eval_run(`; `scratch-roots.md` lines 1, 61-62 verbatim contain `OPS-002 / AC12` header and `/etc/foo` rejection example. Diagnostic `git show 1ca2595:...` command supplied. Real code path exhibiting the symptom — meets the 1.0 anchor. |
| Symptom coverage | 1.0 | Claim explains the full OPS-002 tautology mechanism: candidate passed as both candidate and allowlist-extending kwarg → any path silently accepted. Policy doc's `/etc/foo` rejection example is the exact symptom the bug defeats. 100% of reported symptom addressed. |
| Reproducibility fit | 0.5 | Symptom is a deterministic logic regression with a clear trigger (any `--output-dir`), but the card's own Confidence note ("I haven't run the test myself") confirms no reproducer was attempted in Tier 1. Matches the 0.5 anchor ("deterministic but no reproducer attempted in Tier 1") rather than 1.0. |
| Fix directness | 1.0 | Proposed fix is removing one kwarg at the exact `commands.py:1476` line that evidence identifies — small, localised, touches the precise code in evidence. Plus a named regression test path. Meets the 1.0 anchor. |
| Domain coherence | 1.0 | Pure logic bug in a single call site within `eval_run`. Single domain. Risk note about defense-in-depth callers is a guardrail, not a second domain. Meets the 1.0 anchor. |

## Confidence

- **Self-reported (in card)**: 0.65
- **Calibrated (this report)**: 0.90
- **Delta**: +0.25. The agent under-graded itself. The card explicitly attributes the low self-report to "haven't run the test myself" (which is already captured in Reproducibility 0.5) and to fear of "a non-obvious second cause" (not a rubric dimension). The other four dimensions are unambiguously 1.0 against the anchors.

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `security_caution`
- **Rubric rule fired**: "`--type security` AND confidence < 0.95 → ESCALATE (`escalation_reason: security_caution`). Security bugs have asymmetric cost-of-being-wrong; raise the bar."

Rule walk in rubric order: (1) Hard stops — `--no-escalate` is false and `--depth` is `standard` (not `quick`) → no match. (2) Forced — `--depth` is not `deep` → no match. (3) Signal-driven — `confidence 0.90 ≥ 0.85` (not low_confidence); Domain coherence 1.0 (not multi_domain); symptom not described as intermittent; Reproducibility 0.5, not 0.0 (not not_reproducible); **`--type: security` AND 0.90 < 0.95 → security_caution fires**. First match wins.

## Notes

- All three card citations verified verbatim on spot-check; no evidence-grounding penalty.
- Reproducibility scored 0.5 (not 1.0) specifically because the card admits no reproducer was run — this is the single drag on the average. The card's blanket 0.65 self-report misallocates that drag across all dimensions; the rubric concentrates it in Reproducibility, leaving the other four dimensions at 1.0.
- No structural pathology: all required sections present.
- Under `--type: security`, even a calibrated 0.90 does not clear the 0.95 bar — this is the rubric's intentional asymmetry, not a defect in the card.
