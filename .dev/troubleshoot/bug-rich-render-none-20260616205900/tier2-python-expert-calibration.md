<!-- PROVENANCE (harness-stamped):
agent_type: confidence-calibrator
agentId: ae7ec4e928acec562
subagent_tokens: 20028
tool_uses: 9
duration_ms: 38122
outcome: completed
input: tier2-python-expert-hypothesis.md (self-reported 0.88) + post-card disconfirming evidence
persisted: verbatim from the agent's final message (turn 4)
-->

# Calibration Report — H-A (unsafe-fork) card

## Per-dimension scores
| Dimension | Score | Justification |
|---|---:|---|
| Evidence grounding | 0.5 | process.py:189-190 verifies, but doesn't directly exhibit the Rich NoneType symptom; repro contradicted predicted failure. |
| Runtime check | 0.0 | runtime claim; new execution refuted the expected MODE=unsafe failure. |
| Symptom coverage | 0.0 | clean Python TypeError poorly explained by heap corruption. |
| Reproducibility fit | 0.0 | card's own falsification test failed: unsafe mode survived 20000 spawns/67k forks, exit 0. |
| Fix directness | 0.5 | start_new_session=True is a direct mitigation for unsafe preexec_fn, but speculative for the observed crash. |
| Domain coherence | 0.5 | crosses fork-safety, threading, allocator state, Rich rendering. |

## Result
- Self-reported: 0.88 — not used.
- **Calibrated for H-A: 0.25** (Δ −0.63).
- **H-A status: SUBORDINATE to H-C** (H-C directly explains the clean TypeError, temporal coupling, and redirected cross-thread writes into one Console).
- **Verdict: ESCALATE** (rule: confidence < 0.85 → ESCALATE; reason: low_confidence).

## Bottom line
`calibrated_confidence_H_A = 0.25` · `leading_status = subordinate_to_H_C` · `verdict = ESCALATE`
