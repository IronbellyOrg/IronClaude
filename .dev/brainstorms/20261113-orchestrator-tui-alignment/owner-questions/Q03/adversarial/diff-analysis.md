# Diff Analysis: owner-answer proposals for Q3 (Coder#477: keep, narrow or close)

## Metadata
- Generated: 2026-11-14 (Step 1, sc-adversarial-protocol Mode A, depth quick)
- Variants compared: 3 (variant-1 = proposal-A "narrow to read-only status and identity, no prompt routing"; variant-2 = proposal-B "keep the listener and prompt routing, with strict guards"; variant-3 = proposal-C "close as superseded, two reopen conditions")
- Total differences found: 18
- Categories: structural (1), content (6), contradictions (3), unique (5), shared assumptions (3 promoted)
- Context file for all advocates: `../question.md`

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section set and order | five sections, same order | same | same | Low (identical by design of the brief) |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Fate of the issue | rewritten as read-only status and identity | kept as a listener, rewritten with guards | closed as superseded | High |
| C-002 | Any route that can start a session in a workspace | none | a fixed request list (watcher: `claim` plus one integer), behind signed, expiring, one-use grants | none (issue closed) | High |
| C-003 | Readiness of the text to post | text A not paste-ready (age placeholder, UNVERIFIED owner-token route, naming match) | text B not paste-ready until the #339 grant format exists | text C paste-ready | Medium |
| C-004 | Further owner decisions needed | Q4, Q22 (or keep the placeholder) | revisit watcher design D1, the #339 grant format, Q16 trust vocabulary | Q4 one-liner only | Medium |
| C-005 | Reading of the owner's 2026-11-13 comment ("Ensure this aligns with Orchestrator and TUI Panel") | answered: aligned as a read-only source for the observer | keeps the original feature intent | admits closing may not match it | Medium |
| C-006 | What is kept for later | the design stays in the open issue | the full listener stays in the open issue | the narrowed text kept in the ledger or linked from the closing comment | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Is there a present need the issue should carry? | yes: "the observer reads one host's Orca only ... and cannot see another workspace" | yes: a path for one place to ask another workspace to act | no present consumer: "nothing in IronClaude waits on #477"; reopen when R4 or a TUIBBS task needs it | Medium |
| X-002 | Is keeping prompt routing defensible? | no (removes the dangerous part) | yes, with guards; "lines up with a future orchestrator of orchestrators" | no (premise contradicts the built watcher) | High: ADJ calls keep "the least defensible" |
| X-003 | Write a design now for consumers that do not exist yet? | yes, and accepts it "may sit unbuilt" | yes, blocked on the grant format | no; wait for a task package that needs it | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | Completes text A's placeholders (CO-02) and makes the nine-item checklist a test requirement for any later build (CO-03) | Medium |
| U-002 | 2 | Separate read and request credentials, a per-type rate cap, joinable audit | Medium |
| U-003 | 3 | Concrete reopen conditions: a watcher-design revisit condition, or an observer R4 or TUIBBS task package needing another workspace | High |
| U-004 | 3 | Names the risk that closing contradicts the owner's comment of one day earlier | Medium |
| U-005 | 1 | States the residual risk that a later Coder change adds a send route without the checklist | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | C-001, X-001 | The watcher was the main consumer of #477, so the watcher's no-listener design settles most of the issue; the title's other parts ("monitor registration ... for every Coder workspace") have no separate purpose this answer would lose | UNSTATED | Yes |
| A-002 | All next-step sections | This program may post to an issue in another repository (`IronbellyOrg/Coder`) through the single issue editor under a grant row, and the Coder repo's owner and readers accept that | UNSTATED | Yes |
| A-003 | X-001, X-003 | The present setup (observer single-host, no TUIBBS screen planned) holds for the life of this decision | UNSTATED (variant 3 states the present state, not its persistence) | Yes |
| A-004 | All | Coder-repo facts and paths rest on one review (V3) | STATED (variant 1; question.md) | No |

Promoted shared-assumption points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The watcher was #477's main purpose | C-001, X-001 | If monitor registration has its own purpose, closing loses it and narrowing may cut it (L2, dependency) | UNSTATED |
| A-002 | Cross-repository posting is accepted | next-step sections | Every option writes to another repository; affects who must agree (L2, dependency) | UNSTATED |
| A-003 | Single-host, no TUIBBS screen soon, holds | X-001, X-003 | If the boundary moves (a second host, a planned TUIBBS screen), close becomes the wrong default and narrow becomes the needed design (L3, boundary) | UNSTATED |

## Summary
- Total structural differences: 1
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-002
- Taxonomy levels: L1 (S-001, C-006), L2 (C-001, C-003, C-004, C-005, X-001, X-003, A-001, A-002), L3 (C-002, X-002, A-003)
- Similarity check: well above 10 percent difference; debate proceeds.
