# Diff Analysis: owner-answer proposals for Q8 (direction-selection record or amend #409 acceptance criterion 1)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal A, variant-2 = proposal B, variant-3 = proposal C; Mode A copies)
- Total differences found: 13
- Categories: structural (1), content (5), contradictions (2), unique (3), shared assumptions (2 promoted, 1 stated)
- Prerequisites validated: output path is under `.dev/`, not a forbidden `.claude/` prefix; all three inputs exist.

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| S-001 | Section set | Same five sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| C-001 | Instrument used now | None; the honest status line posts | Rewrite acceptance criterion 1 | A new one-paragraph owner record | High |
| C-002 | What #409 says about criterion 1 after the correction pass (OB-08) | "not met as recorded" (BC-18 as proposed) | The amended criterion text | "met by the owner's record of <date>, path" | High |
| C-003 | Release 3 (OB-09) unblocked on this point | No; the record becomes release 3's first step | Yes | Yes | Medium |
| C-004 | The gate's field list at `release-gates.md:22` (fallback date, post-link choice, stack confirmation, command name, production-integration reading) | A later record can cover release 3's own choices | Gate is satisfied by the cited records or amended in the same change | A three-item paragraph may not satisfy it; the owner must add the fields or say the gate is met without them | Medium |
| C-005 | Owner effort now | None | Supply or approve one criterion text | Write one paragraph and choose its location | Low |

## Contradictions

| # | Point of Conflict | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Impact |
|---|---|---|---|---|---|
| X-001 | Does the owner's 2026-11-08 "Stage it" decision already count as the selection? | Unresolved ("for the owner to say") | Yes: "this answer is the owner saying yes" | Not by itself: a separate dated record is needed, written retroactively | High |
| X-002 | Is changing the acceptance criterion legitimate? | Keep it unchanged and admit "not met" | Amend it to fit the staged model actually followed | Keep it unchanged: "no one can say the bar was moved" | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | A | Posting BC-18 now makes #409 honest at once; differs from the spec default, which omits BC-18 | Medium |
| U-002 | B | No new document: the evidence already exists in the owner's 2026-11-08 and 2026-11-11 records | Medium |
| U-003 | C | Fixes the meaning of "production integration" in the owner's own words for later readers | High |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All three build on the 2026-11-08 and 2026-11-11 decisions | Those decisions still describe the direction the owner wants (staged: worker ledger, then question ledger, then Decision Desk) | UNSTATED | Yes |
| A-002 | All three accept BC-18's premise that the criterion is "not met as recorded" because the command is shipped | Registering `superclaude observe` in the shipped CLI counts as "production integration" (the owner might read the term as something not yet done, for example the questions read switched on, or use by a coordinator) | UNSTATED | Yes |
| A-003 | All three | Agents cite owner records and never write them (`release-gates.md:22`) | STATED | No |

### Promoted shared assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The recorded staged direction is still current | All three | If false, a record or amendment written now records a stale direction | Open (owner's knowledge) |
| A-002 | Shipping the CLI command is "production integration" | All three, through BC-18 | If false, criterion 1 is not violated yet and A's "not met" line is wrong; C's paragraph decides it | Open (owner's reading; the question asks for it) |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 3
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001
- Taxonomy tags: L3 (guard and state): C-003, C-004, X-001, A-002; L2 (structure and dependency): C-001, C-002, C-005, X-002, A-001; L1: S-001.
