# Refactor Plan — Merging Sonnet strengths into Opus base

## Overview

- **Base variant**: Variant 1 (Opus) — score 0.9765
- **Incorporating from**: Variant 2 (Sonnet) — score 0.8475
- **Total planned changes**: 4 incorporations + 2 base-strengthening additions
- **Overall risk**: Low (additive incorporations, none modify Opus's core design)

## Planned Changes

### Change #1 — Adopt Sonnet's explicit DISPATCH_TABLE alternation
- **Source**: Sonnet §Part 1
- **Target location in base**: Opus §2.2, DISPATCH_PATTERNS[0]
- **Integration approach**: replace
- **Rationale**: Sonnet's pattern explicitly lists `DISPATCH_TABLE` as an alternation entry. Opus's pattern relies on `dispatch[_\s]?table` + `re.IGNORECASE` to match the all-caps form — correct but obscure to reviewers (debate Round 1 Sonnet U-004, confidence 100%). Explicit alternation eliminates a class of review confusion at zero behavioral cost.
- **Risk level**: Low (additive — broadens to explicitly include what was already matched via IGNORECASE)

### Change #2 — Add generic stem-based fallback as tertiary coverage check
- **Source**: Sonnet §Part 3
- **Target location in base**: Opus §2.4, after the `dispatch_family` regex block, before the existing same-line/3-line-window verb check finishes its iteration
- **Integration approach**: insert (new code block between Opus's existing additions and the end of the broad-coverage section)
- **Rationale**: Opus's `dispatch_family` is mechanism-specific to dispatch. Sonnet's stem fallback generalizes to ANY compound mechanism term (middleware_chain → "middleware", event_binding → "event", di_container → "container"), filling a gap Opus's solution leaves for non-dispatch mechanisms. Debate Round 1 Sonnet U-006, confidence 100%.
- **Risk level**: Medium (introduces semantic looseness; mitigated by Change #3)

### Change #3 — Identifier-overlap guard for stem-based matches
- **Source**: Sonnet's own §counter-argument mitigation (text after "If this materializes in practice, the fix is to add a secondary check…")
- **Target location in base**: Inside Change #2's new stem-fallback block; require the stem-matching roadmap line's 3-line window to contain at least one identifier from `contract.mechanism_signature` (the persisted set Opus added in §2.1)
- **Integration approach**: insert (defensive guard inside the new stem-fallback block)
- **Rationale**: Sonnet acknowledged stem matching can produce false-positive coverage when unrelated dispatch concerns appear ("Implement priority dispatch for logging" → covers hub-dispatch contract). The mitigation: only accept a stem match if the roadmap-side context overlaps with the contract's identifier set. This directly leverages Opus's persisted `mechanism_signature` (vindicating its YAGNI defense — the field has a use case in the merged solution).
- **Risk level**: Low (additive guard tightens an otherwise loose match)

### Change #4 — Document the merge-step interaction (INV-005)
- **Source**: Round 2.5 invariant probe finding INV-005
- **Target location in base**: New §7 "Known follow-up: merge-step prompt blindness" appended after §6
- **Integration approach**: append (new section)
- **Rationale**: Neither proposal addresses the merge-prompt side of the failure mode. The gate fix lands but the merge step remains blind to what it should generate. This is a META observation, not a defect in either proposal, but the merged Fix B must record it so future maintainers know the work is incomplete. Severity: HIGH per invariant probe.
- **Risk level**: Low (documentation only)

### Change #5 — Frontmatter inheritance
- **Source**: Opus base
- **Target location**: Top of merged output
- **Integration approach**: replace (use Opus's YAML frontmatter, updating `fix_id` to `fix-b-merged`, `confidence` to reflect the merged score, `addresses` to enumerate the same 3 factors)
- **Rationale**: Opus's frontmatter pattern is a known SuperClaude convention for fix proposals; Sonnet's plain-header doesn't add structured metadata. Trivial.
- **Risk level**: Low

### Change #6 — Add test cases that exercise stem-fallback + identifier-overlap guard
- **Source**: Synthesized from Opus §3 + Sonnet §Test Plan + Change #3
- **Target location**: Opus's test plan §3, extend `TestHubDispatchRegression` class
- **Integration approach**: append (new test methods)
- **Rationale**: The merged proposal introduces a new code path (stem-fallback + ident-overlap guard) that neither original proposal's test plan exercises. Add `test_t6_stem_fallback_with_ident_overlap_covers` (positive case) and `test_t7_stem_fallback_without_ident_overlap_uncovers` (negative case — defends against "Implement priority dispatch for logging" false positive).
- **Risk level**: Low (test additions only)

## Changes NOT Being Made

### Rejected: Sonnet's dataclass-stability argument (X-001)
- **Diff point**: X-001 (dataclass contradiction)
- **Sonnet's approach**: Do NOT add `mechanism_signature` to `IntegrationContract` (YAGNI)
- **Rationale for rejection**: Change #3 above (identifier-overlap guard) requires the persisted identifier set to defeat the stem-fallback false-positive class. The persisted field is now load-bearing for the merged solution, not speculative. This vindicates Opus's §2.1 design choice. Debate Round 2 Opus rebuttal: "the persisted signature is the cheapest enabling primitive for the very defense Sonnet says is needed" — confirmed by Change #3's adoption.
- **Mitigation for the API-stability concern**: Opus's design uses a `default=(("", frozenset()))` value, so existing `IntegrationContract(...)` constructions without the new field continue to work. The backward-compat walkthrough in Opus §4 (PASS verdicts on all existing tests) addresses this.

### Rejected: Sonnet's deletion-only DISPATCH_PATTERNS approach (C-002)
- **Diff point**: C-002
- **Sonnet's approach**: Remove bare `DISPATCH` and add nothing else (no compound-noun pattern)
- **Rationale for rejection**: Opus's debate Round 2 evidence — Sonnet's narrower pattern would NOT extract IC-005 from epics.md:200 ("Hub class-priority…dispatch order"). The gate's purpose is to SURFACE integration mechanisms, not silence noise. Dropping prose mentions of the hub dispatch mechanism reduces gate signal even if it greens the TUIBBS-scp case by coincidence. Opus's compound-noun pattern maintains the extraction with dedup absorbing the lexical variation downstream.

### Rejected: Sonnet's removal of architectural rationale section
- **Sonnet has no §2.5 equivalent**. The "WHY this is one coherent fix" framing is preserved from Opus because it documents intent for future maintainers — without it, the merged refactor reads as "three independent patches that happen to be in one PR".

## Risk Summary

| Change | Risk Level | Impact if wrong | Rollback |
|---|---|---|---|
| #1 explicit DISPATCH_TABLE | Low | Cosmetic — pattern broader by an alternation already covered by IGNORECASE | Remove the alternation |
| #2 stem-based tertiary fallback | Medium | False-positive coverage on unrelated compound-mechanism mentions | Remove the stem-fallback block; revert to dispatch-family-only |
| #3 identifier-overlap guard | Low | Tightens an otherwise loose match; could cause false-negative if context window is too small to contain the identifier | Remove the guard (degrades to Sonnet's raw stem-fallback) |
| #4 follow-up section | Low | Documentation only | Remove the section |
| #5 frontmatter | Low | Metadata only | Remove frontmatter |
| #6 new tests | Low | Test additions only | Remove the tests |

Overall merged-output risk: **Low**.

## Review Status

**Auto-approved** — non-interactive mode (no `--interactive` flag). Rationale documented in this plan.

**Approval timestamp**: 2026-05-25T14:42:00Z
