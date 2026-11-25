# Variant 2 (architect): Orca dashboard visual-design proposal

## 1. Visual Thesis
A calm, instrument-grade console: quiet grey chrome, one warm accent reserved for "a human is needed", and nothing else competing with it.
Structure follows one rule: the attention layer (asks) and the context layer (fleet) are always separate regions with a stable boundary.
Borrowed composition only: gh-dash list/preview whitespace, otel-tui pane proportions, btop tile density; none of their domain logic.
Every screen reads in plain ASCII first; color and rules are enhancement, never the only signal.

## 2. Shared Conventions
- Every mockup is a SYNTHETIC SCENE and says so in its frame. Observation only; Orca stays the authority.
- Scene: 24 workers (16 active, 4 waiting, 3 reported done, 1 unavailable), 3 asks (42m, 18m, 7m), 2 blockers, inbox partial.
- Workers, asks and blockers are overlapping views; the footer says "overlap, not a sum". No spend or token numbers anywhere.
- Unknown is "?" (never 0); stale is a "~" prefix on the age plus dim text; partial coverage is "PARTIAL ?" in the frame title.
- Reported-done is shown as "self-reported", not verified.
- Selection is held by identity, not row position: arriving updates never move the highlighted row or steal focus.
- Pause (p) freezes rendering only; the frame shows "PAUSED, N queued"; resume applies the queue. It never touches Orca.
- Readable names everywhere; exact ids (message, worktree, session) appear only in the selected-detail area.
- A selected ask always shows: question, age, owner, impact, source.
- Reply, acknowledge and resolve are three separate proposed actions. Each later needs an explicit target and a confirmation against current authority. The mockups imply no working integration.

## 3. Five Screens
### A. Attention Rail + Fleet (vertical master/detail)
```
+- ASKS, oldest first -------------+- WORKERS 16 active 4 waiting 3 done 1 unavail ------+
| >Schema choice            42m    | STATE    TASK                              SINCE    |
|   billing-migrate                | waiting  Billing schema choice               42m    |
|  API target               18m    | waiting  Webhook API target                  18m    |
|   webhook-retries                | waiting  Login diff review                    7m    |
|  Review                    7m    | waiting  Search build, CI queue              11m    |
|   auth-cleanup                   | unavail  Search indexer                  no sig?    |
+- SELECTED ASK -------------------+ active   Migrate billing tables              12s    |
| Q: Keep orders.status as an enum | active   Rewrite webhook retries             31s    |
|    or a lookup table?            | ...      14 more active, 3 reported done            |
| age 42m   owner billing-migrate  +- BLOCKERS reported (2) -----------------------------+
| impact  1 worker paused          | DB lock wait   .   CI queue backlog                 |
| source  Orca message, 2 msgs     | INBOX partial: newest page read, older unread ?     |
| exact   msg_3f9a / wt bm-12      | [j/k] move  [/] filter  [p] pause                   |
+----------------------------------+-----------------------------------------------------+
|  SYNTHETIC SCENE | 24 workers, 3 asks, 2 blockers (overlap, not a sum) | live 4s       |
+----------------------------------------------------------------------------------------+
```
- Color: oldest ask bold amber, other asks plain amber, active green, waiting yellow, done dim, unavailable and "?" magenta; selected row reverse video.
- Wide: rail 34 cols + table fills the rest. Default: as shown. Narrow (<80): rail stacks over the table, detail becomes a toggled overlay.
- Focus: Tab swaps rail/table; j/k move; "/" filters the focused pane by text or state. Rail is the default focus.
- Updates land in the table in place and bump the footer age; new asks insert into the rail by age without moving the selection. Enter opens the thread as a full-width overlay.

### B. Triage Stack (horizontal bands)
```
+- SYNTHETIC SCENE ----------+- ORCA WATCH, live 3s ------+- inbox PARTIAL ? ----------+
| >SCHEMA CHOICE       42m !!|  API TARGET           18m !|  REVIEW                  7m|
|  Keep orders.status as an  |  Which endpoint should the |  Login diff ready for your |
|  enum or a lookup table?   |  retries: staging or prod? |  review before it can merge|
|  from billing-migrate      |  from webhook-retries      |  from auth-cleanup         |
|  wait #####################|  wait #########............|  wait ####.................|
+----------------------------+----------------------------+----------------------------+
|  FLEET 24 observed. States are exclusive; asks and blockers are counted separately.  |
|  active 16 [########]  waiting 4 [####]  reported done 3 [###]  unavailable 1 [?]    |
|  BLOCKERS (2 reported): DB lock wait, 2 workers . CI queue backlog, 1 worker         |
+- DETAIL: Schema choice --------------------------------------------------------------+
|  Q    Keep orders.status as an enum, or move it to a lookup table?                   |
|  age 42m | owner billing-migrate | impact 1 worker paused | source Orca msg thread   |
|  exact msg_3f9a, wt bm-12 | proposed, separate: [r]eply  [a]cknowledge  [x]resolve   |
+--------------------------------------------------------------------------------------+
```
- Color: cards carry the only saturated color (amber border, "!!" red past 30m); fleet band is grey with thin green/yellow bars.
- Wide: cards in a row, up to 4. Default: 3 as shown. Narrow: cards stack, one visible at a time with h/l paging, fleet shrinks to one line.
- Focus: cards band first; h/l move between cards, j drops to the fleet band; "/" filters cards by text, owner or age.
- Updates: new asks join the card row at the right and flash a title marker; selected card stays put. Enter expands the detail drawer into a full thread view.

### C. Request Inspector (three-pane thread)
```
+- ASKS 3 -------------+- THREAD: Billing schema choice ----------+- FACTS ----------------+
| >Schema choice    42m| billing-migrate                     14:02| Owner   billing-migrate|
|  API target       18m|   Drafted the migration. orders.status   | Age     42m, waiting   |
|  Review            7m|   can stay an enum or become a lookup    | Impact  1 worker paused|
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

### D. Board by State (kanban columns)
```
+- ACTIVE 16 ------------------+- WAITING 4 ------------+- REPORTED DONE 3 --+- UNAVAIL 1 --+
| Migrate billing tables   12s | >! Schema choice  42m  | Docs sweep      2h | Search       |
| Rewrite webhook retries  31s |    billing-migrate     | Lint cleanup    3h | indexer      |
| Auth token refactor       8s |  ! API target     18m  | Typo fixes      5h | no signal    |
| Index warmup             20s |    webhook-retries     |                    | since ?      |
| Search shards sync       44s |  ! Review          7m  | (self-reported,    |              |
| ...11 more        [j/k]      |    auth-cleanup        |  not verified)     |              |
|                              |  CI queue, no ask  11m |                    |              |
+------------------------------+------------------------+--------------------+--------------+
|  SELECTED  Q: Keep orders.status as an enum, or move it to a lookup table?                |
|  waiting 42m | owner billing-migrate | impact 1 worker paused | source Orca msg thread    |
|  exact msg_3f9a, wt bm-12 | BLOCKERS (2 reported): DB lock wait . CI queue backlog        |
|  SYNTHETIC SCENE | inbox PARTIAL ? | 24 workers, 3 asks, 2 blockers overlap               |
+-------------------------------------------------------------------------------------------+
```
- Color: column titles colored by state; "!" cards in the Waiting column get a bold amber left bar; other columns stay dim.
- Wide: four columns as shown. Default: Active column narrows. Narrow: columns become tabs, Waiting first by default.
- Focus: Tab/Shift-Tab pick a column, j/k a card; "/" filters all columns; Waiting column always sorted by wait age.
- Updates: cards move between columns when state changes, with the selected card pinned (a ghost marker remains if it leaves). Enter opens the thread overlay.

### E. Instrument Panel (tile grid)
```
+- OBSERVED ---------+- HUMAN ASKS, wait age -----------------------+- COVERAGE -----------+
| workers          24| >Schema choice ########################  42m | inbox   PARTIAL ?    |
| active           16|  API target    ##########..............  18m | workers 24 seen      |
| waiting           4|  Review        ####....................   7m | live    4s ago       |
| reported done     3|  bar = wait age; Enter peeks                 | spend   not observed |
| unavailable       1|                                              | read-only            |
+- BLOCKERS 2 -------+- WORKER MAP, 1 cell = 1 worker --------------+- QUEUE --------------+
| DB lock wait  2 wk | billing  A A A A A W    webhooks A A A A W   | updates queued 0     |
| CI queue      1 wk | auth     A A A W D      search   A A A W U   | SYNTHETIC SCENE      |
| (overlap with asks)| docs     D D A    A act W wait D done U off  | [p] pause=freeze     |
+--------------------+----------------------------------------------+----------------------+
|  PEEK  Keep orders.status as an enum, or move it to a lookup table?                      |
|  age 42m | owner billing-migrate | impact 1 worker paused | source Orca thread | msg_3f9a|
+------------------------------------------------------------------------------------------+
```
- Color: wait-age bars shift yellow to amber to red by minutes; worker map cells colored by state letter; tiles use thin dim borders.
- Wide: grid as shown, map can show every worker. Default: map groups collapse to counts. Narrow: tiles stack in one column, ask tile first.
- Focus: Tab cycles tiles; in the asks tile j/k selects; "/" filters the worker map by project or state.
- Updates: tiles refresh in place; map cells change letter, not position. Enter on an ask opens a centered popup of the thread over the grid.

## 4. Recommended Default
Screen A. It puts the asks in a fixed rail that never scrolls away behind routine updates, keeps the fleet as readable context, and maps to three clean components (AskRail, FleetTable, DetailPane) sharing one read model.
It degrades predictably: narrow mode only changes stacking. Provisional, not user approval.
- B suits a glanceable wall display with few asks. C suits working through a backlog of asks, thread-first.
- D suits state-oriented monitoring when "what is stuck where" matters more than the asks. E suits large terminals and ambient watching; thread inspection is a popup, so it is weakest for deciding.

## 5. Framework Fit
- Textual: A and C are layout-and-focus problems: nested containers with docked rail, DataTable for the fleet, list widgets for asks, terminal CSS for the amber/dim palette, key bindings for focus, and its testing docs for screen checks. D is columns of lists; E leans on Sparkline-style widgets. Narrow modes need a resize hook (to be confirmed).
- Bubble Tea + Lip Gloss: strongest for B and E, where bespoke card/tile composition (borders, join horizontal/vertical, color profile) is the point. Focus and scrolling are written by hand, which costs more for A and C.
- Ratatui: nested constraint layouts suit D and E (columns, grid), with Table, Chart, Sparkline, Gauge for the bars. A works well too; C needs custom wrapped-text drawing for the thread.
- Provisional pick: Textual for A, with C as its detail mode. This follows documented widgets and the repo's Python/uv context, not any performance comparison. ASCII-only mode must be built and tested in every option.

## 6. Risks and Unknowns
- Complete non-consuming enumeration of human decisions is unverified; inspection checks cap at 100 messages, so "all asks" may be undercounted. Show "PARTIAL ?", never a total.
- Refresh rate and the live observation interface are untested; the "live 4s" figure is illustrative.
- Durable human state (acknowledged, resolved) has no confirmed home; until validated, those stay proposed actions only.
- Impact ("pauses 1 worker") and blocker-to-worker links may not be derivable from Orca data; if not, show "impact unknown ?".
- Ask-to-worker mapping in the mockups is synthetic and unchecked against real Orca output.
