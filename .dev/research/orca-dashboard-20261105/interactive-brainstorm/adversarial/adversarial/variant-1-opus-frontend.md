# Variant 1: Orca Observer Dashboard Visual Proposal (frontend lens)

## 1. Visual Thesis
Calm by default, loud only where a human is needed. Routine worker traffic is dim and compact;
the three human requests carry the only saturated color, the only bold weight and the first
focus position. Every screen reads top-left to bottom-right as "what needs me, why, what is it
blocking", and words beat identifiers everywhere except the selected-detail area.

## 2. Shared Conventions
- Every frame carries `SYNTHETIC SCENE` in the header until fed live data; `inbox PARTIAL` sits beside it.
- Markers: `?` unknown (never shown as 0), `~` stale with its age, `capped` where 100-message inspection limited a view.
- Counts say "observed"; worker states, requests and blockers overlap and are never summed into one total.
- Urgency is double-encoded: glyph (`!!` over 30m, `!` over 15m) plus color, so monochrome and NO_COLOR stay readable.
- Selection is keyed to request or worker identity, not row position; arriving updates never move the cursor.
- `p` pauses rendering only (Orca keeps running); header shows `PAUSED +N queued`; resume applies them in one redraw.
- Reply, acknowledge and resolve are three separate proposed actions, greyed in read-only mode. Each later
  requires an explicit target (request plus exact identity) and a fresh confirmation of current Orca authority.
- Orca is the authority; the dashboard only observes. Exact ids appear only in the selected-detail area.

## 3. Five Screens

### Screen A: Triage Rail (list + preview, gh-dash proportions)
```
+- Orca observer -- SYNTHETIC SCENE -- inbox PARTIAL -- updated 4s ago ----------------------+
| NEEDS YOU (3)                  | Schema choice for billing migration                       |
| > Schema choice        42m !!  |   Question  Keep the ledger table, or split it into two?  |
|   API target           18m !   |   Waiting   42m (since 14:06)                             |
|   Review requested      7m     |   Owner     billing-migration worker                      |
|--------------------------------|   Impact    2 workers waiting; 1 of 2 reported blockers   |
| BLOCKERS (2 reported)          |   Source    Orca message, inbox page 1 of ? (partial)     |
|   Schema undecided             |   Identity  task 7f3a / msg 0192 / host build-02          |
|   Staging creds unavailable    |   -- thread (last 2 of ?, capped) ----------------------- |
|--------------------------------|   14:06 worker: two options drafted, need a decision      |
| WORKERS (24 observed)          |   14:09 worker: holding migration step 3                  |
|   active 16     waiting 4      |                                                           |
|   complete 3 (reported)        |   proposed:  r reply   a acknowledge   x resolve          |
|   unavailable 1   stale 0      |   (each needs target + authority confirm; read-only now)  |
+- j/k move  tab pane  / filter  enter thread  p pause  ? help ----- 2 new below the rail ---+
```
Color: requests bold amber/red by age; rail headers cyan; worker counts dim grey; preview labels dim, values default.
Wide: thread grows into a third column. Default: as shown. Narrow (under 80): rail only, enter opens full-screen preview.
Focus starts on the oldest request; `tab` cycles rail/preview; `/` filters rail text, `f` filters by state.
Updates land as a dim "N new below" counter in the footer; the preview refreshes in place. Enter expands the thread.

### Screen B: Control Tower (2x2 quadrants, btop geometry)
```
+- REQUESTS 3 -----------------------------------++- WORKERS 24 observed ------------------------+
| Schema choice  ########################### 42m || active      ################  16             |
| API target     ############                18m || waiting     ####               4             |
| Review         #####                        7m || complete    ###                3 reported    |
|                                                || unavailable #                  1             |
| oldest owner: billing-migration worker         || overlaps requests; rows are not added        |
+------------------------------------------------++----------------------------------------------+
+- BLOCKERS 2 reported --------------------------++- RECENT ACTIVITY (routine) ------------------+
| Schema undecided   -> holds 2 waiting workers  || 14:47 docs-sweep reported complete           |
| Staging creds      -> 1 worker unavailable     || 14:46 auth-refactor active, step 4 of ?      |
|                                                || 14:45 api-client now waiting on API target   |
+------------------------------------------------++----------------------------------------------+
 SYNTHETIC | inbox PARTIAL | 4s ago | 1-4 focus panel  enter detail  / filter  p pause  ? help
```
Color: request bars amber to red by age; worker bars green/yellow/blue/grey; activity panel dim.
Wide: adds a third column with selected detail. Default: 2x2. Narrow: quadrants stack, requests first.
Focus via `1-4`; `/` filters the focused panel. Updates land only in RECENT ACTIVITY (newest on top) and bar lengths.
Enter on a request opens a centered overlay with question, age, owner, impact, source, identity and thread.

### Screen C: Wait Timeline (lanes over time, otel-tui proportions)
```
 SYNTHETIC SCENE   inbox PARTIAL   updated 4s ago                            PAUSED  +7 queued
+- WAITING ON HUMANS (last 60m) ----------------------------------------------------------+
|                  -60m         -45m         -30m         -15m        now                 |
| Schema choice    ...........[=========================================]     42m         |
| API target       ..................................[==================]     18m         |
| Review           ...............................................[=====]     7m          |
| Blockers (2)     ...........x......................x.................                   |
| Workers  active 16  waiting 4  complete 3  unavailable 1   (24 observed, not summed)    |
+-----------------------------------------+-----------------------------------------------+
| SELECTED  API target                    | THREAD (last 3 of ?, capped)                  |
| Question  Use v2 API or v3 sandbox?     | 14:31 api-client: v3 sandbox lacks refunds    |
| Age 18m    Owner api-client worker      | 14:33 api-client: pausing until target chosen |
| Impact    1 worker waiting              | 14:40 orca: request still open                |
| Source    Orca message, inbox partial   |                                               |
| Identity  task 2c19 / msg 0207 / host 1 | proposed only:  r reply  a ack  x resolve     |
+-----------------------------------------+-----------------------------------------------+
 up/down lane   left/right scrub time   / search   enter focus thread   p pause/resume
```
Color: lane bars shift amber to red as they lengthen; blocker ticks magenta; axis dim; PAUSED inverse yellow.
Wide: lanes for each waiting worker appear under their request. Default: as shown. Narrow: lanes collapse to age text.
Focus on lanes; `/` searches question text. Updates extend bars at the right edge; a new request adds a lane at the bottom.
The thread opens in the lower right pane; enter moves focus into it for scrolling.

### Screen D: Focus Column (single centered column of cards, narrow-first)
```
          SYNTHETIC SCENE . inbox partial . updated 4s ago
          ----------------------------------------------------------
          NEEDS A HUMAN                                       3 open
          +------------------------------------------------------+
          | > Schema choice for billing migration       42m  !!  |
          |   Keep the ledger table, or split it into two?       |
          |   Owner billing-migration worker . 2 workers waiting |
          |   Source Orca message . task 7f3a / msg 0192         |
          |   proposed:  r reply . a acknowledge . x resolve     |
          +------------------------------------------------------+
          |   Pick API target (v2 or v3 sandbox)          18m  ! |
          +------------------------------------------------------+
          |   Review payments-ui change                    7m    |
          +------------------------------------------------------+
          BLOCKERS  schema undecided . staging creds unavailable
          WORKERS   16 active . 4 waiting . 3 complete . 1 unavailable
          j/k move   enter expand   / filter   t thread   p pause
```
Color: the selected card gets a bold amber left border; collapsed cards plain; footer summaries dim.
Wide: the column stays about 60 columns, centered (whitespace is the design). Narrow: same column, full width.
Focus moves card to card; only the selected card expands, so selection never jumps. `/` filters cards.
Updates appear as a dim "+N updated" chip on the card's top edge. `t` opens the thread full screen.

### Screen E: State Board (request banner over worker-state columns)
```
+== 3 NEED YOU ==  Schema choice 42m !!  |  API target 18m !  |  Review 7m  ======================+
+- ACTIVE 16 ------------+- WAITING 4 -----------+- COMPLETE 3 reported -+- UNAVAILABLE 1 --------+
| auth-refactor   step 4 | billing-migration !!  | docs-sweep            | staging-deploy  ~22m   |
| api-client-gen  step 2 |   on schema choice    | lint-cleanup          |   staging creds        |
| search-index    step 6 | api-client        !   | changelog             |   unavailable          |
| ... 13 more            |   on API target       |                       |                        |
|                        | payments-ui           |                       |                        |
|                        |   on review           |                       |                        |
|                        | queue-worker      ?   |                       |                        |
|                        |   reason unknown      |                       |                        |
+------------------------+-----------------------+-----------------------+------------------------+
| DETAIL billing-migration worker: waiting 42m on "Keep the ledger table, or split it into two?"  |
| impact 2 workers . source Orca message (inbox partial) . task 7f3a / msg 0192 / host build-02   |
+ SYNTHETIC . 4s ago . h/l column  j/k card  1-3 banner request  / filter  enter thread  p pause -+
```
Color: banner inverse amber; column headers tinted per state; unavailable column grey, `~` and `?` in yellow.
Wide: columns widen and show step text. Default: four columns. Narrow: one column at a time, `h/l` switches.
Focus is per column; `1-3` jumps to a banner request's worker. Updates move cards between columns; the cursor follows identity.
The bottom strip shows the selected card's detail; enter replaces the board with the full thread.

## 4. Recommended Default
Provisional pick: **A, Triage Rail**. It puts the three requests first, shows the full request detail without a
keypress, keeps selection stable (list cursor plus independent preview) and degrades to a clean two-step narrow
flow. This is a design recommendation for discussion, not user approval.
- B suits a second monitor where at-a-glance proportions matter more than reading.
- C suits investigating why waits pile up over a session; it is the strongest pause and history view.
- D suits a narrow split beside the Orca chat, or users who want the least visual noise.
- E suits supervising many workers at once, when "who is stuck where" matters more than request text.

## 5. Framework Fit
Building blocks below are the documented capabilities in REPORT section 6; nothing was benchmarked.
- **Textual (Python):** layouts and terminal CSS cover A's docked rail and B's grid; DataTable fits A's rail and
  E's columns; keyboard events carry the focus model; its testing documentation suits checking each screen.
- **Bubble Tea + Lip Gloss (Go):** border, spacing, alignment and composition tools fit D's bespoke cards and E's
  banner; color-profile tools help the monochrome fallback. Panel layout is composed by hand.
- **Ratatui (Rust):** constraint-based nested layouts, charts, sparklines and gauges fit C's lanes and B's bars most
  directly; A's and D's text-heavy panes need more hand-drawn text layout.
Provisional pick: **Textual**, because the default (A) is list, table and preview heavy, and terminal CSS lets all
five screens be prototyped as style variations over one read model. Revisit if C or D wins the visual vote.
Strict ASCII rendering must be built and tested deliberately in any of the three.

## 6. Risks and Unknowns
- Complete non-consuming enumeration of open decisions is unverified; the request list may be incomplete (hence PARTIAL).
- Message inspection is capped at 100, so thread views must say "capped" and never claim full history.
- Refresh rate and the live observation API are unvalidated; "updated Ns ago" and stale markers depend on them.
- Durable human state (acknowledged, snoozed, last seen) has no chosen store; the mockups assume none yet.
- Urgency thresholds (15m, 30m) are placeholders pending the user's calibration.
