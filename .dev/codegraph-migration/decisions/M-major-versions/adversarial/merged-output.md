<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (Option C, original) -->
<!-- Merge date: 2026-10-30 -->

# Merged rule: codegraph major versions get the full proof and always a draft PR

## Candidate selection
<!-- Source: Base (original, modified): "Minor and patch" bullet replaced per Change #1 (Variant 2, two candidates per run); tag rule inserted per Change #2 (shared assumption A-001) -->
- Tag parsing: only tags matching `vMAJOR.MINOR.PATCH` (digits only) are candidates. Prerelease and malformed tags are skipped, and the reason is written to the run log. (Skip-and-log for malformed tags is flagged for the user.)
- Within-major candidate: the newest stable release whose major equals the pin's major. It takes the minor and patch path: a ready PR on a passed proof.
- Major candidate: if a stable release with a higher major exists, the newest such release.
- One run can produce both candidates, so 1.x patches keep flowing while a 2.0 draft waits.

## Major path
<!-- Source: Base (original, modified): "notes" replaced by a release link per Change #6 (Variant 2); "Code" bullet restructured per Change #7 (Variant 1, one code path) -->
- The same verify + rewrite + proof as the within-major candidate. The PR is always opened as a draft, even when the proof passes.
- The PR body carries a link to the release page plus the proof log, the hashes and the attestation result.
- Single pipeline: the same verify, rewrite and proof code runs for both candidates. The only differences are the draft flag and the title. No `--allow-major` manual route is added.
- Rationale: the reviewer gets the full evidence without doing the bump by hand, and a draft cannot be merged until a person marks it ready.

## Idempotency
<!-- Source: Variant 2, merged per Change #3 (idempotent branch and PR); orchestrator-derived rule merged per Change #4 (declined major stays declined) -->
- One fixed branch per target major (for example `codegraph-major-v2`). Each run rebuilds that branch from current master and updates the existing open draft PR; it never opens a second one. The same holds for the within-major branch.
- Rebuilding from master also clears the conflict that appears after a 1.x patch PR merges (both PRs rewrite the same VERSION and SHA256 lines).
- Declined major stays declined: if a person closes the major draft without merging, later runs do not reopen a draft for that same version. A newer release of that major (for example 2.0.1) opens one again. (Policy choice flagged for the user.)

## Title and label
<!-- Source: Base (original, modified): "Cost" bullet replaced per Change #5 (Variant 2 advocate and Variant 3 concession, X-003) -->
- Major drafts are titled `codegraph MAJOR vX.Y.Z: manual review`. The title, not the label, is the reliable signal.
- The `codegraph-major` label is applied only if it exists. Labels are best-effort; IronClaude has none today.
- Draft state can mean two things (major review or failed proof). A failed proof on either path follows the separate M-proof-failure decision, and whatever that decision picks, its titles must differ from the `codegraph MAJOR` prefix.

## What the human does
<!-- Source: Base (original) -->
- Works through the checklist in the draft body: read the breaking changes; check Phase 3 skills that call codegraph tools.
- There is no auto-merge. A person marks the draft ready and merges it, or closes it without merging to decline that version.

## Required tests
<!-- Source: all three variants' recommended rules, merged per Change #8 -->
1. A major candidate gives a draft PR even on a passing proof.
2. A within-major candidate gives a ready PR.
3. A second run updates the existing PR and does not open a duplicate.
4. A prerelease tag is skipped.
5. A 1.x patch still produces a ready PR while a 2.0 draft is open.
6. A major draft closed without merging is not reopened for the same version.
