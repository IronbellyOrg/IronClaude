# Variant 2 — Minimal-Risk Contract Creation UX

Recommended first slice: do the smallest safe change that improves the operator experience without weakening arming.

Key positions:

- Add structured contract diagnosis around the existing loader first.
- Improve `/sc:pr-submit` halt text while preserving the same hard stop.
- Add file-based payload validation before automated GitHub capture.
- Validate by invoking existing `poll_augment_review()` / `classify()` logic, not by duplicating parser behavior in skill markdown.
- Write only `.dev/pr-monitor/detection-contract.locked.md` after explicit confirmation.
- Keep all probe artifacts under `.dev/pr-monitor/probes/` and ensure they are gitignored.
- `/sc:reflect` should initially diagnose and recommend the helper; it should not write the contract in the first implementation unless explicitly chosen later.
- Contract may lock only when evidence proves repo/PR, Augment-authored payload, observed identity, observed emission surface, observed findings/completion signal, classifier dry-run success, provenance, and explicit user confirmation.

Preferred phases:

1. Shared diagnosis with no behavior change.
2. Clearer `/sc:pr-submit` halt message.
3. Probe evidence storage and validation report.
4. Candidate contract writer.
5. `/sc:reflect` read-only readiness reporting.
6. Optional GitHub capture after file-based validation works.
