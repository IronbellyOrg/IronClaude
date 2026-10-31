# Diff Analysis: decision-option comparison (M-major-versions)

## Metadata
- Generated: 2026-10-30T15:30:00Z
- Variants compared: 3 (Variant 1 = option-a.md, Variant 2 = option-b.md, Variant 3 = option-c.md)
- Total differences found: 14 debate points (structural 1, content 7, contradictions 3, shared assumptions 3) plus 6 unique contributions
- Categories: structural (1), content (7), contradictions (3), unique (6), shared assumptions (3)
- Focus: safety of Phase 3 skills that call codegraph tools; reviewer burden; code paths to test; fit with the user's rule that a human merges
- Verified facts used (context.md): proof checks tool list and registration shape, not tool semantics; a human always merges; bot PRs get approval-gated CI; a merged pin flows to every Coder workspace; codegraph is single-maintainer, all 8 recent releases are 1.x; v1.6.2 notes are 76,281 characters.
- Related verified facts (sibling decision M-proof-failure/context.md, still undecided): a draft PR is "the only hard non-mergeable state available"; labels are best-effort; IronClaude has no codegraph label today; issue and PR notifications reach the owner; nobody watches Actions run summaries. One candidate for M-proof-failure uses a draft PR for a failed proof.

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|------|---------------|---------------|---------------|----------|
| S-001 | Document shape | H1 + 5 bullets (behaviour, title, rationale, cost, code) | H1 + 5 bullets (minor path, major path, rationale, cost, code) | H1 + 5 bullets (minor path, major path, rationale, cost, code) | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|-------|---------------|---------------|---------------|----------|
| C-001 | What a newer major produces | Same as minor: ready PR when proof passes | No branch, no PR; one idempotent issue with notes link and manual commands | Same verify + rewrite + proof; PR always opened as draft | High |
| C-002 | Mechanism that stops an accidental merge of a major | None beyond the word "MAJOR" in title/body | Nothing exists to merge until a human runs the bump by hand | Draft state: cannot be merged until a person marks it ready | High |
| C-003 | Evidence handed to the reviewer | Hashes, attestation, proof log, release notes in body | Release notes link plus commands; proof evidence only after a manual run | Full evidence plus a checklist (breaking changes; Phase 3 skills that call codegraph tools) | Medium |
| C-004 | Code paths to build and test | One path; title word only | Second path (issue create/update), a `--allow-major` flag, a within-major release selector | One comparison selects `--draft`; all other steps shared | Medium |
| C-005 | Which release is the candidate when a newer major exists | Unstated (implicitly newest overall) | Newest release within the pinned major keeps bumping; major is reported separately | Unstated (implicitly newest overall) | High |
| C-006 | Protection of Phase 3 skills against semantic tool changes | Relies on reviewer noticing "MAJOR"; acknowledged gap | Human decides adoption; no automated evidence | Checklist names Phase 3 skills explicitly; draft forces a deliberate step | High |
| C-007 | Release notes delivery | Notes in PR body (v1.6.2 notes are 76,281 chars, likely over GitHub's body size limit; limit not verified in context.md) | Link only | Notes part of evidence (inline or link unspecified) | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 (A) Position | Variant 2 (B) Position | Variant 3 (C) Position | Impact |
|---|-------------------|------------------------|------------------------|------------------------|--------|
| X-001 | Is "proof + human merge" a sufficient review for a major? | "the proof plus the human merge is the review" | "a major can break Phase 3 skills in ways the proof cannot see" | Proof is necessary but not sufficient; adds checklist + draft | High |
| X-002 | Should automation prepare the major bump? | Yes, fully | No: "majors need a manual run" | Yes: "without doing the bump by hand" | Medium |
| X-003 | Meaning of draft state | n/a | n/a | Draft reused for "major review" and possibly "failed proof" (sibling decision); label/title disambiguate | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 2 (B) | Idempotent issue keyed by title so repeated scheduled runs do not spam | Medium |
| U-002 | 2 (B) | `--allow-major` flag on the bump script for a deliberate manual run | Medium |
| U-003 | 2 (B) | Within-major selection: 1.x patches keep flowing while 2.0 is pending | High |
| U-004 | 3 (C) | `codegraph-major` label and a review checklist naming Phase 3 skills | Medium (label does not exist yet; labels are best-effort) |
| U-005 | 1 (A) | "MAJOR" marker in PR title/body | Low |
| U-006 | 3 (C) | Draft as the hard non-mergeable state for majors | High |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| - | All variants keep a human merge | A human merges every PR; no auto-merge | STATED (context.md) | No |
| - | All variants verify hashes + attestation for every candidate | Integrity checks run before any branch | STATED | No |
| A-001 | All compare "major number higher than the pin's" | Release tags parse cleanly as vX.Y.Z; prerelease tags (for example v2.0.0-rc.1) and malformed tags have a defined handling | UNSTATED | Yes |
| A-002 | All treat minor/patch as safe for a ready PR | codegraph follows semver discipline: tool argument/output changes that break Phase 3 skills only arrive in majors (single-maintainer project) | UNSTATED | Yes |
| A-003 | All run on a schedule | Each scheduled run is idempotent for the major path: it does not open a duplicate PR/issue or a second branch for the same major on the next run (B states this for issues; A and C do not for PRs) | UNSTATED | Yes |

### Promoted Shared-Assumption Diff Points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Tag parsing and prerelease handling defined | Major-number comparison | Medium | Open |
| A-002 | Breaking changes only in majors | Minor/patch auto path | High | Open |
| A-003 | Major path idempotent across scheduled runs | Scheduled workflow | Medium | Open |

## Taxonomy Tags (for Step 2)
- L1 surface: S-001
- L2 structural: C-001, C-003, C-004, X-002
- L3 state mechanics: C-002, C-005, C-006, C-007, X-001, X-003, A-001, A-002, A-003

## Summary
- Total structural differences: 1
- Total content differences: 7
- Total contradictions: 3
- Total unique contributions: 6
- Total shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-005, C-006, X-001, U-003, U-006
- Similarity check: variants differ materially (well above the 10% threshold); debate proceeds.
