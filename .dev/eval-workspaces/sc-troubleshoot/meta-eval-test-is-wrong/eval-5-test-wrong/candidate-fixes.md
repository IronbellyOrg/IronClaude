# Candidate Fixes — Tier 2

| # | Proposed fix | Supporting agents | Verdict |
|---|--------------|-------------------|---------|
| 1 | Delete `test_doctor_rejects_workspace_default` from `tests/cli/eval/test_scratch_root_policy.py`. Do not modify any production code. | root-cause-analyst, quality-engineer, security-engineer | **consensus** |

**Anti-fixes explicitly considered and rejected by all three agents** (recorded so a downstream remediation chain cannot resurrect them):

- A1. Add a denylist for `.dev/eval-workspaces/` in `config.py` — REJECTED (breaks allowlist-only architecture).
- A2. Remove `.dev/eval-runs/` from `_default_allowed_scratch_roots()` — REJECTED (catastrophic policy break).
- A3. Add a name-based reject path in `resolve_scratch_root` — REJECTED (bypasses unified ingress, breaks cross-module consistency).
- A4. Add `.dev/eval-workspaces/` to the allowlist so the test fails for the "right" reason — REJECTED (silently expands trusted scratch surface).

**Wave 4 (adversarial fix debate) SKIPPED**: per the SKILL.md rule "All agents converge with high confidence → skip Wave 4." Adversarial debate exists to choose among competing strong fixes; with consensus on a single fix it would waste tokens.

**Tier 2 calibration summary** (per-card calibrated scores from confidence-calibrator):

- root-cause-analyst: 0.92 (self 0.95 → calibrated 0.92, multi-domain dimension scored 0.5)
- quality-engineer: 0.90 (self 0.93)
- security-engineer: 0.92 (self 0.94)

All three converge on the same fix. Mean calibrated confidence across cards: 0.91. Combined with the consensus signal, final report confidence: **0.94** (consensus boost above any single card per the standard "independent convergence increases joint confidence" reasoning).
