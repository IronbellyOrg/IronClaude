# Variant 1 — Architect Proposal: Evidence-Locked Detection Contract UX

Recommended architecture: add a shared evidence-first contract setup workflow under `src/superclaude/pr_submit/`, keep `/sc:pr-submit` as the sole owner of monitor arming, and let `/sc:reflect` diagnose contract readiness without owning PR side effects.

Key positions:

- Preserve `DetectionContract.for_arming()` and the T-210 fail-closed gate.
- Write repo/operator-specific locked data only to `.dev/pr-monitor/detection-contract.locked.md`.
- Store probe evidence under `.dev/pr-monitor/probes/<timestamp-or-pr>/`.
- Add shared helper functions for diagnosis, probe capture/load, candidate derivation, classifier validation, and local lock writing.
- Ask a bounded question sequence: repo, PR, operation, no side effects, evidence surfaces, evidence source, no-evidence behavior, identity, app slug, association, emission shape, findings locus, severity path, completion signal, decline fields, classifier validation, final local write, next command print.
- Treat identity, emission shape, findings locus, completion signal, and probe evidence as observed-required before `locked: true`.
- Allow decline defaults to remain versioned defaults but record whether decline evidence was exercised.
- `/sc:reflect --contract-status` should report readiness and validation status, not arm monitors.
- `/sc:pr-submit` missing-contract halt should show checked paths, state summary, setup command, and “No monitor was armed.”

Recommended design: shared helper with thin integrations in `/sc:reflect` and `/sc:pr-submit`.
