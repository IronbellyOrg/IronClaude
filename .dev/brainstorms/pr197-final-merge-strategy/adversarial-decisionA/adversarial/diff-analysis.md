# Diff Analysis: Decision A — anti-self-confirmation model (3 options)

## Metadata
- Generated: 2026-06-28
- Variants: 3 (A=exclusion, B=instance-level, C=hybrid)
- Categories: content (5), contradictions (4), unique (3), shared-assumptions (3)

## Content Differences

| # | Topic | A (exclusion) | B (instance-level) | C (hybrid) | Severity | Tax |
|---|-------|---------------|--------------------|-----------|----------|-----|
| C-001 | Failure mode targeted | weight-level representational bias | context/instance self-confirmation | both | High | L3 |
| C-002 | Class diversity vs executor | hard-forced (exclusion+backfill) | soft preference | hard preference *when class resolves* | High | L3 |
| C-003 | Tier on class collision | may degrade T2→T1 (loud) | never degrades | never degrades (loud warn, stays T2) | High | L3 |
| C-004 | Graded invariant | retained unconditionally | deleted | retained, gated on identity reliability | Medium | L3 |
| C-005 | Build state / merge cost | already merged (smallest) | authored in #197 (low) | not built (highest) | Medium | L2 |

## Contradictions

| # | Conflict | A position | B position | C position | Impact |
|---|----------|-----------|-----------|-----------|--------|
| X-001 | Does instance-freshness defeat §1/Mehta? | No (weights carry bias) | Yes (instance≠instance) | Partial (only context axis) | High |
| X-002 | Is exclusion's T2→T1 degrade a feature or a bug? | feature (loud true signal) | bug (kills the review) | bug to collapse, but keep the signal as warn | High |
| X-003 | Is the deleted telemetry load-bearing? | yes (graded invariant) | no (non-stable, no consumer) | yes but conditionally | Medium |
| X-004 | Is the commit-author heuristic decisive against A? | no (frontmatter exists) | yes (fail-open) | neutralized by gating on reliable source | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | C | `executor_exclusion_unsatisfiable` + source-reliability-gated assertion (degrade without tier-collapse) | High |
| U-002 | A | concrete backfill arithmetic showing exclusion stays full-panel in rich-alias env | High |
| U-003 | B | observation that exclusion *shrinks* the frame and that #197 keeps all three named §1 mechanisms | Medium |

## Shared Assumptions (UNSTATED → promoted)

| # | Assumption | Source agreement | Impact | Status |
|---|-----------|------------------|--------|--------|
| A-001 | The proxy reliably resolves many distinct model classes (rich multi-vendor) at review time | all three lean on it | If FALSE (alias outage / single-vendor window), A degrades loudly, B silently seats same-class, C warns-but-survives | UNSTATED — **decisive on the environment axis** |
| A-002 | Reviewer-isolation (read-only reflect-reviewer + `--isolate-reviewers`) is orthogonal and lands regardless | all three | None of the options strengthen/weaken mutation-safety | UNSTATED |
| A-003 | EV-1…EV-4 (on-disk merge gates) are model-agnostic and land regardless of A/B/C | all three | The merge-cost delta between options is ONLY the §7.1/§11.3/telemetry surface, not the EV gates | UNSTATED |

## Summary
- Core fork is L3 state-mechanics (C-001..C-004): *what* the guarantee protects (weights vs context), *how hard* it is enforced, and *whether it is observable*.
- A-001 is the load-bearing shared assumption: every option's ranking is conditional on alias richness at review time.
- Highest-severity: C-001, C-002, C-003, X-001, X-002.
