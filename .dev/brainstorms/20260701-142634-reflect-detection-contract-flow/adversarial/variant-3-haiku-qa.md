# Variant 3 — QA Proposal: Evidence-Validated Locked Contract UX

Recommended QA posture: defaults may be suggested, but no evidence-required field can become locked without captured Augment-authored GitHub payload evidence and classifier validation.

Key positions:

- Preserve fail-closed arming.
- Introduce a shared diagnosis/validation helper used by `/sc:reflect` and `/sc:pr-submit`.
- Store local locked contract and evidence under `.dev/pr-monitor/`.
- Support PR review bodies, issue comments, and check-run output as possible surfaces.
- Reject guessed, stale, wrong-repo, wrong-PR, ambiguous, and insufficient evidence.
- Require validation report metadata and provenance before lock.
- Distinguish no evidence, in-progress, findings, no findings, declined, and invalid/unusable contract states.
- `/sc:reflect` should summarize status and paths without dumping full payload bodies.

Acceptance emphasis:

- Missing contract diagnosis is actionable.
- Shipped contract remains unlocked.
- Defaults cannot lock without evidence.
- Wrong repo evidence rejects.
- Cross-PR evidence is never silent.
- Multiple surfaces validate independently.
- Non-Augment-authored copied text is ignored.
- Decline differs from no findings and no evidence.
- Existing arming gate remains fail-closed.
