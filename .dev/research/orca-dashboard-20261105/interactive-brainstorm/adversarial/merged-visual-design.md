<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (sonnet:architect); incorporated: Variant 1 (opus:frontend) -->
<!-- Merge date: 2026-11-05T21:48:40Z -->
# Merged: Orca dashboard visual-design proposal
<!-- Source: Base (original) -->
## 1. Visual Thesis
A calm, instrument-grade console: quiet grey chrome, one warm accent reserved for "a human is needed", and nothing else competing with it.
Structure follows one rule: the attention layer (asks) and the context layer (fleet) are always separate regions with a stable boundary.
Borrowed composition only: gh-dash list/preview whitespace, otel-tui pane proportions, btop tile density; none of their domain logic.
Every screen reads in plain ASCII first; color and rules are enhancement, never the only signal.

<!-- Source: Base (original, modified); Variant 1, Section 2, merged per Changes #1 and #3; Round 1 verdicts A-001/A-002 per Change #2 -->
## 2. Shared Conventions
- Every mockup is a SYNTHETIC SCENE and says so in its frame. Observation only; Orca stays the authority.
- Scene: 24 workers (16 active, 4 waiting, 3 reported done, 1 unavailable), 3 asks (42m, 18m, 7m), 2 blockers, inbox partial.
- Workers, asks and blockers are overlapping views; the footer says "overlap, not a sum". No spend or token numbers anywhere.
- Unknown is "?" (never 0); stale is a "~" prefix on the age plus dim text; partial coverage is "PARTIAL ?" in the frame title; "capped" marks a view limited by the 100-message inspection cap.
- Urgency is double-encoded: glyph ("!!" over 30m, "!" over 15m) plus color, so monochrome and NO_COLOR stay readable.
- Reported-done is shown as "self-reported", not verified.
- Selection is held by identity, not row position: arriving updates never move the highlighted row or steal focus.
- Identity keys are unverified against real Orca output; if a stable identity is missing, the row shows "?" and selection is held by owner plus question text.
- Every request area keeps the oldest asks pinned and ends with a "+N more asks" line when rows run out.
- Pause (p) freezes rendering only; the frame shows "PAUSED, N queued"; resume applies the queue. It never touches Orca.
- Readable names everywhere; exact ids (message, worktree, session) appear only in the selected-detail area.
- A selected ask always shows: question, age, owner, impact, source.
- Reply, acknowledge and resolve are three separate proposed actions. Each later needs an explicit target and a confirmation against current authority. The mockups imply no working integration.

<!-- Source: Base (original, modified); Screens B and E replaced per Changes #5 and #6 -->
## 3. Five Screens
<!-- Source: Base (original, modified); urgency glyphs per Change #1; inline thread from Variant 1, Section 3 Screen A, merged per Change #4 -->
### A. Attention Rail + Fleet (vertical master/detail)
```
+- ASKS, oldest first -------------+- WORKERS 16 active 4 waiting 3 done 1 unavail ------+
| >Schema choice         42m !!    | STATE    TASK                              SINCE    |
|   billing-migrate                | waiting  Billing schema choice               42m    |
|  API target            18m !     | waiting  Webhook API target                  18m    |
|   webhook-retries                | waiting  Login diff review                    7m    |
|  Review                    7m    | waiting  Search build, CI queue              11m    |
|   auth-cleanup                   | unavail  Search indexer                  no sig?    |
+- SELECTED ASK -------------------+ active   Migrate billing tables              12s    |
| Q: Keep orders.status as an enum | active   Rewrite webhook retries             31s    |
|    or a lookup table?            | ...      14 more active, 3 reported done            |
| age 42m   owner billing-migrate  +- BLOCKERS reported (2) -----------------------------+
| impact  1 worker paused          | DB lock wait   .   CI queue backlog                 |
| source  Orca message, 2 msgs     | INBOX partial: newest page read, older unread ?     |
| exact   msg_3f9a / wt bm-12      | [j/k] move  [/] filter  [p] pause  [Enter] thread   |
| -- thread (last 2 of ?, capped) -|                                                     |
| 14:02 Drafted the migration...   |                                                     |
| 14:09 Pausing until you choose.  |                                                     |
+----------------------------------+-----------------------------------------------------+
|  SYNTHETIC SCENE | 24 workers, 3 asks, 2 blockers (overlap, not a sum) | live 4s       |
+----------------------------------------------------------------------------------------+
```
- Color: oldest ask bold amber, other asks plain amber, active green, waiting yellow, done dim, unavailable and "?" magenta; selected row reverse video.
- Wide: rail 34 cols + table fills the rest. Default: as shown. Narrow (<80): rail stacks over the table, detail becomes a toggled overlay.
- Focus: Tab swaps rail/table; j/k move; "/" filters the focused pane by text or state. Rail is the default focus.
- Updates land in the table in place and bump the footer age; new asks insert into the rail by age without moving the selection. The last two thread lines show inline; Enter opens the full thread as a full-width overlay.

<!-- Source: Variant 1, Section 3 Screen D (Focus Column), merged per Change #5; rewritten in base scene wording -->
### B. Focus Column (single centered column of cards, narrow-first)
```
     SYNTHETIC SCENE . inbox PARTIAL ? . live 4s
     ------------------------------------------------------
     NEEDS A HUMAN, oldest first                    3 asks
     +----------------------------------------------------+
     | > Schema choice                        42m !!      |
     |   Keep orders.status as an enum or a lookup table? |
     |   owner billing-migrate . impact 1 worker paused   |
     |   source Orca message . msg_3f9a / wt bm-12        |
     |   proposed: r reply . a acknowledge . x resolve    |
     +----------------------------------------------------+
     |   API target                           18m !       |
     +----------------------------------------------------+
     |   Review                                7m         |
     +----------------------------------------------------+
     (a final "+N more asks" line sits here when rows run out)
     BLOCKERS (2 reported)  DB lock wait . CI queue backlog
     WORKERS observed  16 active . 4 waiting . 3 reported done . 1 unavail
     overlap, not a sum . j/k move  enter expand  / filter  t thread  p pause
```
- Color: the selected card gets a bold amber left border; "!!" red, "!" amber; collapsed cards plain; blocker and worker lines dim.
- Wide: the column stays about 56 cols, centered (whitespace is the design). Default: same centered column. Narrow: same column, full width.
- Focus moves card to card; only the selected card expands, so selection never jumps. "/" filters cards by text or owner.
- Updates: a changed card shows a dim "+N updated" chip on its top edge; new asks insert by age with a flash marker. "t" opens the thread full screen.

<!-- Source: Base (original, modified); urgency glyphs per Change #1 -->
### C. Request Inspector (three-pane thread)
```
+- ASKS 3 -------------+- THREAD: Billing schema choice ----------+- FACTS ----------------+
| >Schema choice 42m !!| billing-migrate                     14:02| Owner   billing-migrate|
|  API target    18m ! |   Drafted the migration. orders.status   | Age     42m, waiting   |
|  Review         7m   |   can stay an enum or become a lookup    | Impact  1 worker paused|
|                      |   table. Needs your call.                | Source  Orca message   |
| / filter: ______     | billing-migrate                     14:09|         thread, 2 msgs |
| all  waiting  mine   |   Pausing until you choose.              | Blocker DB lock wait   |
|                      |   -- no human reply observed --          | Exact identity         |
+- FLEET 24 observed --+   [r]eply  [a]cknowledge  [x]resolve     |   msg_3f9a             |
| 16 active  4 waiting |   Three separate proposed actions;       |   wt bm-12             |
| 3 done  1 unavailable|   each needs target + authority.         |   sess 21c             |
+----------------------+------------------------------------------+------------------------+
|  SYNTHETIC SCENE | 3 asks, 24 workers, 2 blockers (overlap, not a sum) | inbox PARTIAL ? |
+------------------------------------------------------------------------------------------+
```
- Color: message text default, author names cyan, timestamps dim, amber only on the selected ask and the "no human reply" line.
- Wide: three panes as shown. Default (~100): facts collapse into a header strip over the thread. Narrow: one pane at a time, 1/2/3 switches.
- Focus: left pane first; Enter moves into the thread, Esc returns; "/" filters asks. Fleet stays a two-line stub by design.
- Updates: new messages append at the thread bottom with an unread rule; the ask list re-sorts only on Esc. Thread is inline, so no separate open step.

<!-- Source: Base (original, modified); Waiting-column glyphs aligned to the Sec 2 urgency convention (consistency follow-on of Change #1) -->
### D. Board by State (kanban columns)
```
+- ACTIVE 16 ------------------+- WAITING 4 ------------+- REPORTED DONE 3 --+- UNAVAIL 1 --+
| Migrate billing tables   12s | >Schema choice  42m !! | Docs sweep      2h | Search       |
| Rewrite webhook retries  31s |    billing-migrate     | Lint cleanup    3h | indexer      |
| Auth token refactor       8s |  API target     18m !  | Typo fixes      5h | no signal    |
| Index warmup             20s |    webhook-retries     |                    | since ?      |
| Search shards sync       44s |  Review          7m    | (self-reported,    |              |
| ...11 more        [j/k]      |    auth-cleanup        |  not verified)     |              |
|                              |  CI queue, no ask  11m |                    |              |
+------------------------------+------------------------+--------------------+--------------+
|  SELECTED  Q: Keep orders.status as an enum, or move it to a lookup table?                |
|  waiting 42m | owner billing-migrate | impact 1 worker paused | source Orca msg thread    |
|  exact msg_3f9a, wt bm-12 | BLOCKERS (2 reported): DB lock wait . CI queue backlog        |
|  SYNTHETIC SCENE | inbox PARTIAL ? | 24 workers, 3 asks, 2 blockers overlap               |
+-------------------------------------------------------------------------------------------+
```
- Color: column titles colored by state; ask cards in the Waiting column get a bold amber left bar; other columns stay dim.
- Wide: four columns as shown. Default: Active column narrows. Narrow: columns become tabs, Waiting first by default.
- Focus: Tab/Shift-Tab pick a column, j/k a card; "/" filters all columns; Waiting column always sorted by wait age.
- Updates: cards move between columns when state changes, with the selected card pinned (a ghost marker remains if it leaves). Enter opens the thread overlay.

<!-- Source: Variant 1, Section 3 Screen C (Wait Timeline), merged per Change #6; base Screen E COVERAGE facts moved into the header line -->
### E. Wait Timeline (lanes over time, otel-tui proportions)
```
 SYNTHETIC SCENE . inbox PARTIAL ? . live 4s . spend not observed . read-only
+- WAITING ON A HUMAN, last 60m -----------------------------------------------+
|                -60m      -45m      -30m      -15m      now                   |
| Schema choice  ............[==========================]  42m !!              |
| API target     ............................[==========]  18m !               |
| Review         ...................................[===]   7m                 |
| Blockers (2)   DB lock wait . CI queue backlog (reported, times ?)           |
| Workers observed 16 active . 4 waiting . 3 reported done . 1 unavail         |
+-------------------------------------+----------------------------------------+
| SELECTED  Schema choice             | THREAD (last 2 of ?, capped)           |
| Q  Keep orders.status as an enum    | 14:02 billing-migrate: Drafted the     |
|    or a lookup table?               |   migration... Needs your call.        |
| age 42m !!  owner billing-migrate   | 14:09 billing-migrate: Pausing until   |
| impact 1 worker paused              |   you choose.                          |
| source Orca message, 2 msgs         |   -- no human reply observed --        |
| exact msg_3f9a / wt bm-12           | proposed: r reply  a ack  x resolve    |
+-------------------------------------+----------------------------------------+
 up/down lane  left/right scrub  / search  enter thread  p pause | overlap, not a sum
```
- Color: lane bars shift yellow to amber to red as they lengthen; axis dim; "?" magenta; "PAUSED, N queued" inverse yellow at the header's right.
- Wide: lanes for each waiting worker appear under their ask. Default: as shown. Narrow: lanes collapse to age text.
- Focus on lanes; "/" searches question text. An ask older than the window is pinned at the left edge with a ">60m" marker.
- Updates extend bars at the right edge; a new ask adds a lane at the bottom with a flash marker. The thread sits in the lower right pane; Enter moves focus into it.

<!-- Source: Base (original, modified); B and E bullets re-mapped from Variant 1, Section 4 per Change #7 -->
## 4. Recommended Default
Screen A. It puts the asks in a fixed rail that never scrolls away behind routine updates, keeps the fleet as readable context, and maps to three clean components (AskRail, FleetTable, DetailPane) sharing one read model.
It degrades predictably: narrow mode only changes stacking. Provisional, not user approval.
- B suits a narrow split beside the Orca chat, or users who want the least visual noise. C suits working through a backlog of asks, thread-first.
- D suits state-oriented monitoring when "what is stuck where" matters more than the asks. E suits investigating why waits pile up over a session; it is the strongest pause and history view.

<!-- Source: Base (original, modified); B/E sentences re-mapped from Variant 1, Section 5 per Change #7 (X-001 unresolved: fits, not a ranking) -->
## 5. Framework Fit
- Textual: A and C are layout-and-focus problems: nested containers with docked rail, DataTable for the fleet, list widgets for asks, terminal CSS for the amber/dim palette, key bindings for focus, and its testing docs for screen checks. D is columns of lists. Narrow modes need a resize hook (to be confirmed).
- Bubble Tea + Lip Gloss: border, spacing, alignment and composition tools fit B's bespoke card column; color-profile tools help the monochrome fallback. Focus and scrolling are written by hand, which costs more for A and C.
- Ratatui: nested constraint layouts suit D's columns; Chart, Sparkline and Gauge fit E's timeline lanes and bars. A works well too; C needs custom wrapped-text drawing for the thread.
- Both mappings above are documentation-based fits, not a ranking. Provisional pick: Textual for A, with C as its detail mode. This follows documented widgets and the repo's Python/uv context, not any performance comparison. ASCII-only mode must be built and tested in every option.

<!-- Source: Base (original, modified); threshold note from Variant 1, Section 6 per Change #1 -->
## 6. Risks and Unknowns
- Complete non-consuming enumeration of human decisions is unverified; inspection checks cap at 100 messages, so "all asks" may be undercounted. Show "PARTIAL ?", never a total.
- Refresh rate and the live observation interface are untested; the "live 4s" figure is illustrative.
- Durable human state (acknowledged, resolved) has no confirmed home; until validated, those stay proposed actions only.
- Impact ("pauses 1 worker") and blocker-to-worker links may not be derivable from Orca data; if not, show "impact unknown ?".
- Ask-to-worker mapping in the mockups is synthetic and unchecked against real Orca output.
- Urgency thresholds (15m, 30m) are placeholders pending the user's calibration.
