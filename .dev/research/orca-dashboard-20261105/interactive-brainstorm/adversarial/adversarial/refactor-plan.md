# Refactoring Plan: Merge into Base (Variant 2)

## Overview
- Base: Variant 2 (sonnet:architect), variant-2-sonnet-architect.md
- Incorporating strengths from: Variant 1 (opus:frontend), variant-1-opus-frontend.md
- Planned changes: 7
- Risk level: Medium (two whole screens are replaced)
- Hard limits for the merged file: at most 180 lines INCLUDING provenance comments; exactly five screens; at most 8 material points is already met. Every mockup must use the BASE scene text (schema choice "Keep orders.status as an enum or a lookup table?", owner billing-migrate, impact "1 worker paused"; API target owner webhook-retries; Review owner auth-cleanup; blockers "DB lock wait" and "CI queue backlog"; "reported done"; unavailable worker "Search indexer"). Do not import V1 scene wording (ledger table, api-client, staging creds, step N).

## Planned Changes

### Change 1: Glyph-plus-color urgency (from Variant 1)
- **Source**: V1 Sec 2, "Urgency is double-encoded: glyph (`!!` over 30m, `!` over 15m) plus color"; V1 Sec 6 "thresholds (15m, 30m) are placeholders"
- **Target**: Base Sec 2 (insert one convention line) and base mockups A and C ask lists (append `!!` / `!` after the ages); add the placeholder note to Sec 6 Risks
- **Rationale**: C-001, Round 1, V2 advocate conceded; 95%
- **Integration point**: after the "Unknown is ?" convention; asks at 42m get `!!`, 18m gets `!`, 7m none
- **Risk**: Low, additive

### Change 2: Request overflow and identity fallback conventions (debate outcome)
- **Source**: Round 1 verdicts on A-001 (both QUALIFY) and A-002 (both REJECT)
- **Target**: Base Sec 2 (insert two convention lines)
- **Rationale**: A-001 90%: identity keys are unverified against real Orca output; if a stable identity is missing, mark the row "?" and hold selection by owner plus question text. A-002 90%: every request area keeps the oldest asks pinned and shows a final "+N more asks" line when rows run out
- **Integration point**: after the selection-by-identity convention
- **Risk**: Low, additive

### Change 3: `capped` marker (from Variant 1)
- **Source**: V1 Sec 2 "`capped` where 100-message inspection limited a view"; V1 A "thread (last 2 of ?, capped)"
- **Target**: Base Sec 2, extend the unknown/stale/partial convention line
- **Rationale**: brief success criterion "Unknown/capped/stale data ... visible but succinct"; base has no capped marker in conventions
- **Integration point**: same line as "?", "~" and "PARTIAL ?"
- **Risk**: Low

### Change 4: Inline thread lines in default Screen A (from Variant 1)
- **Source**: V1 Screen A preview "-- thread (last 2 of ?, capped) --" with two timestamped lines
- **Target**: Base Screen A, SELECTED ASK box (replace the "exact" line area by adding two thread lines; keep exact identity line); update the Updates note so Enter opens the full thread
- **Rationale**: V2 advocate conceded "V1's Screen A preview shows the thread inline ... For deciding speed V1 is better"; S-002 itself stays unresolved, so the base fleet table is kept
- **Integration point**: inside the SELECTED ASK box under "source"; reuse base C thread text ("Drafted the migration..." 14:02, "Pausing until you choose." 14:09)
- **Risk**: Low, box may need 2 more rows; keep mockup at most 19 lines

### Change 5: Replace Screen B Triage Stack with V1 Focus Column (from Variant 1)
- **Source**: V1 Screen D "Focus Column (single centered column of cards, narrow-first)" plus its four notes
- **Target**: Base Sec 3 Screen B (replace whole subsection; heading becomes "B. Focus Column")
- **Rationale**: S-001, Round 1, both advocates agreed on merge-both (90%); V2 advocate conceded "V1's Focus Column (D) is a better narrow-first composition than anything in V2"; V2 B and V1 D are both card compositions, so this keeps five distinct geometries
- **Integration point**: rewrite card text in base scene wording; add a "Default" width note (V1 D lacked one); add "+N more asks" under the cards; keep `!!` / `!`
- **Risk**: Medium, whole-screen swap; must not duplicate C or D geometry

### Change 6: Replace Screen E Instrument Panel with V1 Wait Timeline (from Variant 1)
- **Source**: V1 Screen C "Wait Timeline (lanes over time, otel-tui proportions)" plus its four notes
- **Target**: Base Sec 3 Screen E (replace whole subsection; heading becomes "E. Wait Timeline"); move the base E COVERAGE content ("spend not observed", "read-only") into the timeline's header line so it is not lost
- **Rationale**: S-001 agreed merge (90%); U-001 High value; V2 Sec 4 itself calls E "weakest for deciding"; V1 advocate noted E's letter-code map conflicts with "readable content over IDs"
- **Integration point**: rewrite lanes in base scene wording; fix the V2-advocate weakness by stating that an ask older than the window is pinned at the left edge with a ">60m" marker; selected-ask facts must show "impact 1 worker paused" or "impact unknown ?"
- **Risk**: Medium, whole-screen swap; worker map is dropped (see below)

### Change 7: Re-map Sec 4 alternatives and Sec 5 framework fit to the new B and E
- **Source**: V1 Sec 4 ("D suits a narrow split beside the Orca chat", "C suits investigating why waits pile up ... strongest pause and history view") and V1 Sec 5 ("Ratatui ... charts, sparklines and gauges fit C's lanes"; "Lip Gloss ... fit D's bespoke cards")
- **Target**: Base Sec 4 bullets for B and E; base Sec 5 Textual, Bubble Tea + Lip Gloss and Ratatui bullets
- **Rationale**: needed for internal consistency after Changes 5-6. X-001 is UNRESOLVED (50%): record both mappings as documentation-based fits, Ratatui for the timeline lanes and bars, Lip Gloss for the card column, Textual stays the provisional pick for A and C; no ranking or performance claim
- **Integration point**: replace only the sentences that name old B and E
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| S-002 | V1 A: counts-only rail, full-height request preview, no fleet rows | Unresolved (50%); base selected on score keeps the named fleet table; only the inline thread (Change 4) was conceded |
| C-002 | V1 states impact and blocker links as fact | V1 conceded (95%); base guard stays |
| C-003 | V1 dim "N new below" footer counter for new asks | Leaning V2 (60%); V2 advocate showed a new ask must not be the quietest event; base insert-by-age plus flash marker stays |
| X-001 | V1 single mapping "Ratatui fits bars most directly" as a ranking | Unresolved (50%); both mappings recorded as fits without ranking (Change 7) |
| U-005 | V2 E worker map, one cell per worker | Dropped with Screen E; letter codes conflict with readable-content goal; COVERAGE facts kept (Change 6) |
| U-003/V1 B | V1 Control Tower and V1 State Board | V1 advocate conceded B is weaker; V1 E overlaps base D board |
| (V1 content) | "step 4 of ?" step progress, RECENT ACTIVITY feed | Not among observed Orca data in the brief; routine feed competes with asks |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Urgency glyph missing on one screen | Revert to base Sec 2 and mockups |
| 2 | Low | Additive conventions only | Remove inserted lines |
| 3 | Low | Additive | Remove marker text |
| 4 | Low | Screen A box overflows width | Revert to base Screen A |
| 5 | Medium | Duplicate geometry or V1 scene text leaks in | Revert to base Screen B |
| 6 | Medium | Scene facts contradict other screens; line cap exceeded | Revert to base Screen E |
| 7 | Low | Sec 4/5 still name old B/E | Revert Sec 4/5 sentences |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-05T22:20:00Z
