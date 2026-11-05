# Refactoring Plan

## Overview
- Base variant: Variant 3 (Option C, draft PR for majors)
- Incorporated variants: Variant 2 (Option B), Variant 1 (Option A)
- Planned changes: 8
- Rejected changes: 5
- Overall risk: Low to Medium (the changes add rules; none removes C's draft gate)

## Planned Changes

### Change 1: Two candidates per run (within-major and newer-major)
- Source: Variant 2, "later minors of the old major still bump" (U-003, C-005)
- Target: Base bullet "Minor and patch"
- Approach: replace. The ready-PR path picks the newest stable release whose major equals the pin's major. Separately, if a stable release with a higher major exists, the newest such release is the major candidate. A run can produce both.
- Rationale: C-005 won 100% (unanimous, V1 and V3 advocates conceded); keeps 1.x patches flowing while 2.0 waits.
- Risk: Medium (changes candidate selection).

### Change 2: Strict tag parsing
- Source: shared assumption A-001 (all advocates QUALIFY)
- Target: new bullet before the minor/major paths
- Approach: insert. Only tags matching `vMAJOR.MINOR.PATCH` (digits only) are candidates; prerelease and malformed tags are skipped with the reason written to the run log.
- Rationale: A-001 agreed 90%; prevents v2.0.0-rc.1 from triggering the major path early. Advocate split on malformed tags (skip-and-log vs open an issue) is resolved to skip-and-log for scope, and flagged for the user.
- Risk: Low.

### Change 3: Idempotent major branch and PR
- Source: Variant 2, "opens (or updates, idempotently by title)" (U-001, A-003)
- Target: Base bullet "Major"
- Approach: append. One fixed branch per target major (for example `codegraph-major-v2`). Each run rebuilds that branch from current master and updates the existing draft PR; it never opens a second one. The same holds for the within-major branch.
- Rationale: A-003 won 100% (unanimous ACCEPT). Rebuilding from master also clears the conflict that appears after a 1.x patch PR merges (both PRs rewrite the same VERSION and SHA256 lines).
- Risk: Low.

### Change 4: Declined major stays declined
- Source: interaction of A-003 and C-002 (orchestrator, derived from advocates' idempotency rule)
- Target: Base bullet "Major"
- Approach: append. If a person closes the major draft without merging, later runs do not reopen a draft for that same version; a newer release of that major (for example 2.0.1) opens one again.
- Rationale: without it, every scheduled run would reopen a declined draft. Flagged for the user because it is a policy choice no variant stated.
- Risk: Low.

### Change 5: Title prefix carries the meaning; label is optional
- Source: Variant 2 advocate and Variant 3 concession (X-003)
- Target: Base "Cost" bullet
- Approach: replace. Major drafts are titled `codegraph MAJOR vX.Y.Z: manual review`. The title, not the label, is the reliable signal. The `codegraph-major` label is applied only if it exists (labels are best-effort; IronClaude has none today). Whatever M-proof-failure decides, its titles must differ from this prefix.
- Rationale: X-003 won by V2 (75%); all advocates agreed the title must disambiguate.
- Risk: Low.

### Change 6: Release notes as a link
- Source: Variant 2, "the release notes link" (C-007)
- Target: Base bullet "Major" (evidence list)
- Approach: replace "notes" with a link to the release page plus the proof log, hashes and attestation result in the body.
- Rationale: C-007 won 100%; v1.6.2 notes are 76,281 characters.
- Risk: Low.

### Change 7: Single pipeline, no manual-only path
- Source: Variant 1, "one code path" (C-004); rejection of B's `--allow-major` route
- Target: Base "Code" bullet
- Approach: restructure. The same verify, rewrite and proof code runs for both candidates; the only difference is the draft flag and title. No `--allow-major` manual route is added.
- Rationale: C-004 won by V1 (90%), C close second; V3 advocate: a rarely used manual path "is the code most likely to break unnoticed".
- Risk: Low.

### Change 8: Required tests (code paths to test)
- Source: all three advocates' recommended rules
- Target: new bullet after "Code"
- Approach: append the list: major gives a draft PR even on a passing proof; within-major gives a ready PR; second run updates and does not duplicate; prerelease tag skipped; 1.x patch still produces a ready PR while a 2.0 draft is open; closed-unmerged major draft is not reopened for the same version.
- Rationale: the focus "code paths to test"; each item is a branch introduced by Changes 1 to 5.
- Risk: Low.

## Base Weaknesses Addressed
| Issue | Better variant | Fix |
|-------|----------------|-----|
| No candidate rule when a major is pending (C-005) | V2 | Change 1 |
| No idempotency (A-003) | V2 | Changes 3, 4 |
| Draft overload with failed proof (X-003) | V2 | Change 5 |
| Notes delivery unspecified (C-007) | V2 | Change 6 |
| No tag-parsing rule (A-001) | none (shared gap) | Change 2 |

## Changes NOT Being Made
| Diff point | Non-base approach | Rationale |
|------------|-------------------|-----------|
| C-001 | A: ready PR for majors | V1's own advocate conceded the "MAJOR" word is a soft signal; C-001 won by V3 (85%). |
| C-002 | B: no branch or PR for majors | Unresolved (50%). Draft is kept because it is a hard non-mergeable state that keeps the proof evidence attached; B's stronger barrier costs a manual rerun at the riskiest moment (X-002 won by V3, 95%). Flagged for the user. |
| X-002 | B: majors need a manual run | Lost unanimously; V2 advocate conceded. |
| C-004 | B: `--allow-major` flag | Adds a rarely exercised path; Change 7. |
| A-002 | All advocates suggested the minor PR also warn that the proof does not check tool semantics | Outside this decision's question (majors only). Flagged for the user instead of added to the rule. |

## Risk Summary
| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1 | Medium | Two PRs can be open at once | Drop the major candidate; minors unaffected |
| 2 | Low | A future tag scheme could be skipped | Widen the pattern |
| 3 | Low | Force-updating a branch a human edited | Branch is bot-owned by name; document that |
| 4 | Low | A declined version is never re-offered | Reopen the PR by hand |
| 5 | Low | Title collision with M-proof-failure | Coordinate prefixes |
| 6, 7, 8 | Low | None material | n/a |

## Review Status
- Approval: auto-approved (non-interactive)
- Timestamp: 2026-10-30T15:45:00Z
