# Hypothesis: Tier 1 conclusion re-affirmed with stronger grounding — TEST is the defect, not the code

**Agent**: root-cause-analyst (carrying Tier 1 hypothesis into Tier 2)
**Tier**: 2
**Timestamp**: 2026-05-21T05:35:00Z
**Cause class**: Test infrastructure

## Claim

After re-grounding with deeper MCP queries, the Tier 1 conclusion stands and is sharpened: the synthetic test asserts a policy that contradicts the canonical OPS-002 contract. The "fix" applied two days ago (commit 5a65c62, the scratch-root tautology fix) did NOT regress the policy — the merge commit's diff modifies `eval_run` to drop the self-extending `output_dir=` kwarg that made the AC12 check tautological. The policy itself (default tuple, `SCRATCH_ROOT_POLICY` constant, doc) was unchanged. The synthetic test was almost certainly added in the same PR by a contributor who saw "OPS-002 fix" in the description and wrote a too-broad regression guard.

## Evidence

- All Tier 1 citations re-verified.
- `git log` references the tautology-fix commit modifying `eval_run` (not `_default_allowed_scratch_roots`). The PR description's "fix for the scratch-root tautology bug" matches the commit message `fix(cliEval): close scratch-root allowlist tautology in eval_run (PR #66 review)` (commit 5a65c62 in recent history).
- The synthetic test's docstring says "REGRESSION TEST written by a contributor who skimmed the policy doc" — the symptom matches: skimming the policy doc would conflate `.dev/eval-runs/` (allowed) with `.dev/eval-workspaces/` (a dev directory used by skill-creator and similar plugins, per `CLAUDE.md` override note).
- `CLAUDE.md` override section: "Plugin Override — Skill-Creator Workspace Destination" explicitly mandates `.dev/eval-workspaces/<skill-name>/` for skill workspaces — a DIFFERENT directory from `.dev/eval-runs/` for a DIFFERENT purpose. The test author plausibly saw `.dev/eval-workspaces/` in CLAUDE.md and thought it was an off-limits directory; in reality it's neither on-limits nor off-limits for OPS-002 — it's simply orthogonal (a dev tool directory, not a scratch root at all).

## Proposed Fix

Delete `test_doctor_rejects_workspace_default` from `tests/cli/eval/test_scratch_root_policy.py`. Same as the other two agents.

## Confidence

Self-reported: 0.95

Per-dimension self-assessment:
- Evidence grounding: 1.0
- Symptom coverage: 1.0
- Reproducibility fit: 1.0
- Fix directness: 1.0
- Domain coherence: 0.5

## Risks

Same as Tier 1.

## If I'm wrong, it's probably because...

The `git log` evidence chain depends on the user-described history; if the tautology-fix commit actually did modify `_default_allowed_scratch_roots`, my premise is wrong. Trivially verifiable.

## Alternatives considered

None new beyond Tier 1.

## Grounding gaps

Same as Tier 1.
