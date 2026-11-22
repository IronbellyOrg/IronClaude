# Round 1 Advocate Statement: Variant 1 (opus, frontend)

## Position (1-3 sentences)
V1 gives five geometrically distinct full-screen compositions and encodes urgency with glyph plus color on every one, so requests stay loud even in monochrome. It should be the base; V2's missing-data guard (C-002) and its selection-pinning mechanics (C-003) should be merged in.

## Steelman of Variant 2
V2's strongest argument is honesty about what Orca can actually tell us: it warns that "impact and blocker-to-worker links may not be derivable" and falls back to "impact unknown ?", labels completion "self-reported, not verified", and adds a COVERAGE tile ("spend not observed", "read-only"). It also specifies the hardest motion cases precisely: the ask list "re-sorts only on Esc" and a selected card that leaves its column leaves "a ghost marker". Its Request Inspector (C) is the best screen in either variant for actually deciding a request: thread inline, facts beside it, "no human reply observed".

## Strengths Claimed (numbered, with evidence)
1. Distinct compositions (S-001): V1 C is the only screen in either set that maps wait length to space ("-60m ... now" lanes, blocker ticks); V1 D is a deliberate narrow-first column ("whitespace is the design"). In V2, B, D and E all end in the same full-width bottom detail strip ("DETAIL", "SELECTED", "PEEK"), and A and C both open with the same left ask list, so the five screens look more alike.
2. Urgency survives without color (C-001): V1 sec 2 "glyph (`!!` over 30m, `!` over 15m) plus color, so monochrome and NO_COLOR stay readable", and the glyphs appear on A, C, D and E. V2's default A rail shows only "42m" with "oldest ask bold amber", breaking its own "color is enhancement, never the only signal" thesis.
3. The default gives the request the space (S-002): V1 A spends the full-height right pane on the question, age, owner, impact, source and thread. V2 A spends its largest pane on routine rows ("active Migrate billing tables 12s") and wraps the question into a 34-column box.
4. Routine motion is kept away from requests: V1 B "Updates land only in RECENT ACTIVITY"; V1 A uses a dim "2 new below the rail" counter. V2 A's "Updates land in the table in place", in the larger pane, so the moving region is the routine one.
5. Pause is visible where the eye is: V1 C puts "PAUSED +7 queued" in the frame header, inverse yellow.
6. Framework fit is matched to geometry: Ratatui for C's lanes and B's bars "most directly" (charts, sparklines, gauges), Lip Gloss for D's cards and E's banner, Textual for the list-heavy default, with "Revisit if C or D wins the visual vote".

## Weaknesses in Variant 2 (numbered, with evidence)
1. Default A's urgency is color-only in the rail (see Strength 2); a NO_COLOR user cannot see which request is overdue.
2. Instrument Panel (E) makes requests one tile among six equals ("Tab cycles tiles"); V2 itself calls it "weakest for deciding". Its worker map ("A A A A A W") swaps readable names for letter codes, against the brief's "readable content over IDs".
3. B's card band holds "up to 4" requests with no overflow rule, and the 5th request has nowhere to go (see A-002).
4. X-001: V2 calls Bubble Tea "strongest" for E, a bars-and-map grid, while listing Ratatui's built-in "Table, Chart, Sparkline, Gauge"; for bar compositions the built-in widgets are the closer fit.

## Concessions
- C-002: V2 is better. V1 A shows "Impact 2 workers waiting; 1 of 2 reported blockers" as fact, without a guard; V1 should adopt "impact unknown ?" and "self-reported, not verified".
- C-003: V2's Esc-only re-sort and ghost marker are more concrete than V1 E's "cursor follows identity", which can make the cursor jump to another column on screen.
- V2 C (Request Inspector) beats V1 B (Control Tower) as a fifth screen; V1 B overlaps V2 E as a glance view and is weaker for deciding.
- V2 A's fleet table shows readable task names; V1 A reduces workers to counts in the rail.
- V1 shares the A-002 gap: "NEEDS YOU (3)" has no overflow rule.

## Per-Point Verdicts
| Point | Superior (V1 / V2 / Merge-both) | One-line reason |
|-------|------------------|-----------------|
| S-001 | Merge-both | Keep V1's time lanes and narrow column for distinctness; swap V1 B for V2 C Inspector. |
| S-002 | V1 | Full-height request preview puts the question, not routine rows, in the largest pane. |
| C-001 | V1 | Glyph plus color on every screen meets "never color alone"; V2 A breaks it. |
| C-002 | V2 | "impact unknown ?" and "self-reported" prevent overclaiming; V1 shows impact as fact. |
| C-003 | Merge-both | V2 ghost marker and Esc re-sort, plus V1's dim "N new below" counter. |
| X-001 | V1 | Ratatui's built-in chart, sparkline and gauge widgets fit bar/lane screens; both agree Lip Gloss fits cards. |
| A-001 | Merge-both | QUALIFY: selection needs stable ids, but they are unverified against real Orca output; if an id is missing, mark the row "?" and hold the selection instead of tracking position. |
| A-002 | Merge-both | REJECT: neither variant handles more requests than rows; add "oldest pinned, +N more" to every request area. |
