# Diff Analysis: decision-option comparison (M-b minimum release age)

## Metadata

- Generated: 2026-10-30T15:20:00Z
- Variants compared: 3 (variant-1 = Option A, variant-2 = Option B, variant-3 = Option C)
- Total differences found: 18
- Categories: structural (1), content (5), contradictions (2), unique (4), shared assumptions (6)
- Focus areas: fit with the user's two-week rule; exposure to pulled or quickly patched releases; lag on security fixes; testability offline
- Current pin: `VERSION = "1.6.2"` in `src/superclaude/cli/install_codegraph.py` (read 2026-10-30)

## Verified facts given to every advocate (from context.md)

- Releases: v1.3.0 07-07, v1.3.1 07-09, v1.4.0 07-10, v1.4.1 07-10, v1.5.0 07-21, v1.6.0 08-26, v1.6.1 09-29, v1.6.2 10-03 (all 2026).
- Quick follow-up patches happen (1.6.1 to 1.6.2 in 4 days; 1.4.0 to 1.4.1 same day). Upstream may delete or re-tag a bad release.
- The user's rule is about two weeks minimum age for new dependency versions (coordinator-stated; closest rule found on disk is the harness rule that script versions must be at least two weeks old).
- Every bump goes through hash checks, attestation verify, an isolated proof, and a PR that a human merges. A merged pin reaches every Coder workspace.

## Derived replay (orchestrator arithmetic from the verified dates, daily scheduled run assumed)

Gaps between releases: 2, 1, 0, 11, 36, 34, 4 days.

| Option | Bumps it would have opened (date: version) | Bumped to a release that already had a newer same-line patch? |
|---|---|---|
| A (no age) | 07-07: 1.3.0, 07-09: 1.3.1, 07-10: 1.4.1 (1.4.0 too if a run fell between them), 07-21: 1.5.0, 08-26: 1.6.0, 09-29: 1.6.1, 10-03: 1.6.2 | 1.3.0, 1.6.1 (and possibly 1.4.0) were bumped before their patch existed; each PR was superseded within 0 to 4 days |
| B (14 days, newest eligible) | 07-21: 1.3.0, 07-23: 1.3.1, 07-24: 1.4.1, 08-04: 1.5.0, 09-09: 1.6.0, 10-13: 1.6.1, 10-17: 1.6.2 | Yes, twice: 1.3.0 on 07-21 (1.3.1 existed since 07-09) and 1.6.1 on 10-13 (1.6.2 existed since 10-03) |
| C (7 days, latest only) | 07-17: 1.4.1, 07-28: 1.5.0, 09-02: 1.6.0, 10-10: 1.6.2 | No. 1.3.0, 1.3.1, 1.4.0 and 1.6.1 were never latest for 7 days |

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| S-001 | Bullet structure | 3 bullets (rule, rationale, cost) | 4 bullets (rule, fallback plus summary, override, rationale, cost) | 3 bullets (rule, rationale, cost) | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| C-001 | Minimum age threshold | 0 days | 14 days, one constant `MIN_AGE_DAYS = 14` | 7 days | High |
| C-002 | Pick when the newest release is too young | Never too young; always newest | Bump to the newest older release that is eligible | Do nothing this run | High |
| C-003 | Manual override for urgent fixes | None (not needed) | `workflow_dispatch` input `min_age_days` | None | Medium |
| C-004 | Release source | `releases/latest` | Full release list filtered to non-draft, non-prerelease, newer than pin | `releases/latest` only | Medium |
| C-005 | Reporting of a waiting release | None | Run summary names the waiting newer release and when it becomes eligible | None | Low |

## Contradictions

| # | Point of Conflict | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Impact |
|---|---|---|---|---|---|
| X-001 | Is an age gate needed at all? | "the proof and the human merge are the safety net" | Age gate needed: "the eligible release is the settled one" | Age gate needed: "still skipping same-day re-releases" | High |
| X-002 | Intra-variant (B): is the eligible release settled? | n/a | Rationale says "the eligible release is the settled one", but B's own example bumps to 1.7.0 while its patch 1.7.1 is already published (3 days old); the replay shows B bumping to 1.3.0 and 1.6.1 after their patches existed | n/a | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | B | `workflow_dispatch` input `min_age_days` overrides the age for a manual run (security fix path) | High |
| U-002 | B | Run summary names the waiting release and its eligibility date | Medium |
| U-003 | C | Do nothing when the newest release is young (no fallback); in the replay this avoided every already-patched release | High |
| U-004 | A | Names PR churn (one PR per quick patch) as an explicit cost | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Release age is measured from a trustworthy timestamp (`published_at`), and a deleted and re-created release restarts the clock. GitHub also exposes `created_at`, which may differ from the publish time. No variant names the field. | All variants compare release time to "now" | High: wrong field can make a fresh release look old | UNSTATED, promoted |
| A-002 | "Newer than the pin" and "newest" are ordered by semantic version, not by date. A later-published backport (for example 1.5.3 after 1.6.0) breaks date ordering. | All variants say "newer than the pin" | Medium | UNSTATED, promoted |
| A-003 | `releases/latest` equals the newest semver release. Maintainers can mark a different release as latest. | A and C rely on it; B avoids it by listing | Medium | UNSTATED, promoted |
| A-004 | Age boundary: "at least N days" is inclusive and measured in whole UTC days or exact seconds; neither is specified. | B and C state a minimum | Medium (off-by-one in tests) | UNSTATED, promoted |
| A-005 | The age rule composes with the M-a major-version rule (a candidate chosen by age may be a new major). | All variants ignore majors | Medium | UNSTATED, promoted |
| A-006 | The age logic can be tested offline as a pure function of (release list JSON, now, pin, min age). | B mentions "one more date comparison to test"; A and C are silent | Medium | UNSTATED, promoted |

## Taxonomy tags (for the coverage gate)

- L1 surface: S-001, C-005, U-004
- L2 structural: C-003, C-004, X-001, U-001, U-002, A-003, A-005, A-006
- L3 state mechanics: C-001 (guard threshold), C-002 (transition when young), X-002 (state of "settled"), U-003, A-001, A-002, A-004

## Summary

- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 4
- Total shared assumptions surfaced: 6 (UNSTATED: 6, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001, X-002, A-001
- Convergence denominator (S + C + X + A): 1 + 5 + 2 + 6 = 14
- Similarity check: variants differ substantially; debate proceeds.
