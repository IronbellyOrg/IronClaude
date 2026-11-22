# Round 1 Advocate Statement: Variant 2 (sonnet architect)

## Position
V2 keeps the asks region and the fleet region as separate, stable areas, so routine worker traffic can never push a human request out of view. It also refuses to present guessed links (impact, blocker-to-worker) as fact. Its compositions map cleanly to a few widgets over one read model, which makes the framework choice low-risk.

## Steelman of Variant 1
V1's strongest argument is that urgency must survive monochrome and NO_COLOR. Section 2 double-encodes it ("glyph (`!!` over 30m, `!` over 15m) plus color") on every screen, and flags the thresholds as placeholders (Risks). Its Screen A also shows the full ask detail and the last thread messages beside the rail with no keypress, so a human can decide without opening anything. Its Wait Timeline (C) and centered Focus Column (D) are the two most visually distinct compositions in the debate: a time axis, and a narrow-first single column that fits beside the Orca chat.

## Strengths Claimed
1. Honest unknowns on the facts that drive a decision. V2 Risks: "Impact ... may not be derivable from Orca data; if not, show 'impact unknown ?'". V2 labels done workers "self-reported, not verified" (Sec 2, Screen D column). That serves the brief's "unknown/partial visible but succinct" goal.
2. Attention separated from routine traffic by structure. Screen A: the ASKS rail is a fixed region and the fleet table is a different region; "Rail is the default focus". Screen C keeps the fleet as "a two-line stub by design", so the ask thread gets the space.
3. Fleet stays readable, not just counted. Screen A lists waiting workers by task name ("Billing schema choice", "Search build, CI queue") with a SINCE column and an "unavail ... no sig?" row. This covers workers that wait with no ask, which a counts-only fleet panel cannot show.
4. Update rules cover the state transitions. Screen D: "selected card pinned (a ghost marker remains if it leaves)". Screen C: "ask list re-sorts only on Esc" with an unread rule. Screen B: new asks "flash a title marker".
5. Visually distinct and composable set. Inspector (C: list, thread, facts), kanban (D), and the tile grid with a one-cell-per-worker map and a COVERAGE tile ("spend not observed", "read-only") are all absent from V1.
6. Framework fit through structure. Sec 4: "AskRail, FleetTable, DetailPane sharing one read model", and narrow mode "only changes stacking". That is a concrete Textual docked-container plus DataTable mapping.

## Weaknesses in Variant 1
1. Derived links stated as fact. Screen A: "Impact  2 workers waiting; 1 of 2 reported blockers". Screen B: "Schema undecided -> holds 2 waiting workers". V1's Risks never says these links may be underivable. A wrong impact line misleads the very person deciding.
2. Invented routine content. Screen B "RECENT ACTIVITY": "auth-refactor active, step 4 of ?", and Screen E shows "step 4" per worker. Step progress is never shown to exist in Orca data. It also puts an activity feed on screen, the kind of routine traffic the brief says must not compete with asks.
3. New asks are the quietest event. Screen A: "Updates land as a dim 'N new below' counter" and "2 new below the rail". A newly raised human request is shown as dim text, the lowest-salience element, and the rail overflow case is only implied.
4. Timeline window clips the oldest ask. Screen C is "(last 60m)" with -60m as the left edge. An ask waiting longer than 60m, the one that most needs a human, runs off the axis. The scrub control adds a mode that Screen A and D do not need.
5. Fleet context is thin on the default. Screen A shows only counts ("active 16 waiting 4"), no worker names. Screen D drops the fleet to one summary line, so "which worker is stuck" needs a screen change.

## Concessions
- V1 wins urgency encoding (C-001). V2's Screen A shows the amber ask rail with only an age and no `!`/`!!` glyph, so a monochrome terminal loses the oldest-first cue beyond ordering. V2 should adopt V1's glyph-plus-color scheme with thresholds marked as placeholders.
- V1's Screen A preview shows the thread inline; V2's Screen A needs Enter for the thread overlay. For deciding speed V1 is better.
- V1's Focus Column (D) is a better narrow-first composition than anything in V2.
- A-002 is a real hole in V2: the Screen A rail is five lines and has no "+N more asks" behavior.
- V2's Screen A repeats each waiting ask in both the rail and the table, which costs space.

## Per-Point Verdicts
| Point | Superior | One-line reason |
|-------|----------|-----------------|
| S-001 | Merge-both | V1 adds the Timeline and Focus Column, V2 adds the Inspector, kanban, and worker map; no screen duplicates another. |
| S-002 | V2 | Fleet table gives named worker context next to the asks; concede V1's inline thread. |
| C-001 | V1 | Glyph-plus-color on every screen survives NO_COLOR; V2 only on B and D. |
| C-002 | V2 | "impact unknown ?" fallback beats stating underivable impact as fact. |
| C-003 | V2 | Ghost marker, unread rule, and flash marker beat a dim "N new below" chip for new asks. |
| X-001 | Merge-both | Both mappings are documentation-based and unbenchmarked; each fits different screens, and both pick Textual for the default. |
| A-001 | QUALIFY | Identity stability is unverified; keep identity keys but show "identity unstable ?" and fall back to owner plus question text. |
| A-002 | REJECT | The rail will not stay readable past its rows as drawn; needs a pinned "+N more asks" line and oldest-first scroll. |
