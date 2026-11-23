# Screen-space value audit (questions screen, Decision Desk, worker ledger)

Method: read the current 160 and 80 column screens (inputs/current/*/questions|desk|ledger.txt), rendering-rules.md (RR) and REDESIGN-SPEC.md (RS). I did not open the PNGs; every number below comes from the text files. 116 columns behaves like 160 for the cut list. Frequency = how often a human acts on it. "Spec" = needs a spec edit (FREE = no spec line requires it).

## 1. Questions screen: what each element spends

| Element (today's text) | Tells the human | Freq | Verdict | Spec |
|---|---|---|---|---|
| Line 1 `ORCA OBSERVER mode=live scope=all as of 12:00:00` | which data, when | every glance | SHORTEN: `ORCA OBSERVER  live  scope=all  12:00:00` | RR L17 requires `mode=`, `as of`; edit |
| Line 2 `worker-list OK 0s  coordinator questions OK 0s (one Run run_14cfcbd8edf2)` | is the data trustworthy | every glance | KEEP the two ages; SHORTEN run id to `run_14cf..edf2` or drop it here (it repeats on line 6) | RR L54 wants the Run in the cell; edit |
| Line 3 `collected 6 / reported 6 scope=all ...` | is the list complete (PARTIAL) | every glance | KEEP `collected n / reported T`; drop the second `scope=all` (repeat of line 1) | RR L20 says never truncated; repeat is edit |
| `source counts: unknown  runs seen: 2` | terminal accounting | almost never | MOVE TO INSPECTOR (show only when a count exists) | RR L20; edit |
| `SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable` (cut off by `>` at 80) | three things we cannot know | almost never | MERGE: one token `no source: settled, frozen, cost` (says the same, 34 cells instead of ~85) | RR L20, L81, L82; safety wording kept, edit |
| `COORDINATOR QUESTIONS` | what the panel is | every glance | KEEP | |
| `one Run only: run_14cfcbd8edf2` | the list covers one Run, not all | sometimes | MERGE into the title row, shorten id | RR L44 verbatim-ish; edit |
| `question read: OK 0s` | is the question list fresh | every glance when not OK | MERGE with the header cell (same fact twice) | RR L45 and L54 both require; edit |
| Disclosure `bounded best effort; coverage unknown; at most 100 rows per read...` (1 row at 160, 2 at 80) | the list may be incomplete | once, then never | KEEP verbatim at 160 (one row). At 80 it is 2 rows: cut to `best effort; coverage unknown; max 100 rows per read; bursts may be lost` (1 row) and put the long form in the inspector | RR L49 says VERBATIM: needs edit; safety kept |
| `seen, not resolved: 3 \| closed by evidence: unavailable (no source)` | how many are waiting on me | every glance | KEEP; drop `(no source)` (the word unavailable already says it) | RR L47 verbatim; edit for 12 cells |
| `no read marker in source: answered questions stay listed` | a listed question may already be answered | sometimes | MERGE with retention line: `answered stay listed (no read marker); observed since 12:00 only` | RR L48, L53; edit |
| `retention reset at 12:00; questions observed before this start are not retained` | older questions are invisible | almost never | MERGE (above) | RR L53; edit |
| Question line `1h  Choose ...  reason unknown` | the actual ask and its age | every glance | KEEP age + text. `reason unknown` on every line = 14 cells x N rows of the same word | RR L50 says never cut; safety is "unknown is not none". Say it once in the title: `reasons: none given`. Needs edit; the cheapest big win |
| `worker-reported, not questions` | stops `wait` being read as a question | sometimes | KEEP (one row) | RR L39 |
| `▸` selected glyph | which row n/p selected | when used | KEEP | RR L50 |
| Footer keys `Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  m mark rows  e export all  q quit  n/p question` (3 rows at 80) | what I can press | first week only | SHORTEN: `j/k move  Enter detail  / filter  n/p question  h history  e export  q quit` (drop Up/Down, Esc, `m`: still work, `m` marks workers only) | FREE (RR L22 only fixes the `shown` part) |
| Footer `shown 6/6 \| collected 6 / reported 6` | overflow | sometimes | SHORTEN: `shown 6/6` (collected is already in line 3) | RR L22; tiny edit |

## 2. Decision Desk (9 field lines + id + note today)

| Element | Tells the human | Freq | Verdict | Spec |
|---|---|---|---|---|
| `msg_000000000000  age 1h` | the question's internal id, its age | age sometimes, id never | SHORTEN to `1h` on the title row; id to inspector | RR L57 requires id; edit |
| Question text (up to 4 lines) | the full ask, if the list line was clipped | every glance on a long ask | KEEP, but skip it when the list line already shows it whole (fixtures repeat the subject) | RR L57; edit |
| `dispatchId: w-001` | which session | every glance | KEEP (one short cell) | |
| `workerState: running` | alive and busy, or idle | every glance | KEEP | |
| `nextAction.kind: wait` | what the worker says it does next | sometimes | KEEP as `next: wait` | |
| `liveness: alive (terminal)` | is it alive | every glance | KEEP | |
| `evidence age: 3s` | how old that reading is | sometimes | KEEP as `3s` | |
| `dispatchStatus: active`, `terminalState: active`, `outcome: none` (3 rows) | separate raw facts | almost never when all are the default | MERGE into one row `dispatch active \| terminal active \| outcome none`; show only values that are not (active, active, none), absent value stays `unknown` so unknown is not none | RR L57 lists them; L71 wants them separate: edit |
| `resource.worktreeId: wt-1` + note `worktree is evidence for this one session; other sessions in it are not inferred affected` (2 rows at 80) | where it runs; do not assume siblings are hit | almost never | MERGE: `wt-1 (this session only)`; full sentence in inspector. The safety is AC-7, kept in 6 cells | RR L57 note verbatim; edit |
| Repeated retention + `worker-reported` lines under the desk | same as the list screen | never twice | already one copy: DROP the duplicate under the desk | FREE |

## 3. Worker ledger

| Element | Tells the human | Freq | Verdict | Spec |
|---|---|---|---|---|
| `dispatchId` (22 wide) | which session | every glance | KEEP, width 10 | |
| `run` | which Run | sometimes | KEEP, width 7 | |
| `workerState` | busy / idle / blocked | every glance | KEEP | |
| `dispatchStatus` + `terminalState` + `outcome` (3 columns, 38 cells, nearly all `active active none`) | raw separate facts | almost never | MERGE to one `status` column showing only the non-default | RR L30; edit |
| `nextAction.kind` | worker's own next step | sometimes | KEEP, verbatim (RR L31) | |
| `liveness` `alive (terminal)` | alive or not | every glance | SHORTEN to the verdict word at 116/160 (source in inspector) | RR L30; edit |
| evidence age | how stale the reading is | every glance | KEEP | |
| `flags` column (empty in every fixture row) | changed `*` marker | rare | DROP the column; show `*` in the first cell | FREE |
| `── ──────` rule row | none | never | DROP | FREE |
| `39/54 shown  +15 more` row above a footer that already says `shown 39/54` | overflow | sometimes | DROP the duplicate | RR L76; edit |
| Gap notice `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` | no question data | every glance in fixture | KEEP verbatim (RR L32) | |
| `26 historical hidden (h)` | rows hidden | sometimes | KEEP; share a row with the gap notice | RR L23 |
| 80-column ledger shows only kind, id, age (no state, no liveness) | | | NOTE: at 80 the human cannot see alive/blocked. Swap `kind` for state. Not applied in the mocks. | RR L33; edit |

## 4. The 64-hex hash and long paths (worked example)

- Today: a plan-ask carries a 64-hex hash and file paths. The desk wraps to at most 4 lines and cuts the rest with `...` (RS D-6, L141); the 80-column desk must keep an in-window hash whole (RB-19, RS L267). Two canary tests pin it (RS L14); question text is on screen only (owner decision).
- What a human needs: the ask in words, and enough of the hash to recognise it: first 4 and last 4 characters, `0123..cdef`. A path needs its last two parts, `.../spec/plan.md`. Nobody types or compares 64 characters on a dashboard.
- Rule I would use: on the list line, first line of the text only. In the desk, collapse any hex run of 32 or more into `xxxx..xxxx` and any path of more than 3 parts into `.../a/b`. The inspector (Enter) and the export keep the full, untruncated text, so nothing is lost and the owner's "on screen only" rule still holds.
- Interaction with the code: this changes D-6, RB-19 and the hash canaries. Not free: it needs the owner to reverse D-6 and rewrite RB-19. Until then the full hash stays and the first-line rule for list lines is the only free part. Safety: a collapsed hash must keep a visible `..` and be selectable in the inspector in full.

## 5. Stripped-down mocks (real fixture wording; rows saved vs today)

Questions, 160 columns: 18 rows vs 24 (saves 6)
```
ORCA OBSERVER  live  scope=all  12:00:00   worker-list OK 0s | coordinator questions OK 0s
collected 6 / reported 6   no source: settled, frozen, cost, source counts
COORDINATOR QUESTIONS  one Run only: run_14cf..edf2   reasons: unknown for all
seen, not resolved: 3 | closed by evidence: unavailable
answered questions stay listed (no read marker in source); observed since 12:00 only
bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between reads may be lost
▸ 1h  Choose schema compatibility policy
  59m  Confirm deployment window
  59m  Name the release reviewer
worker-reported, not questions
   dispatchId  run    state    status  next  liveness          age
   w-001       run-0  running  active  wait  alive (terminal)  3s
   w-002       run-1  idle     active  wait  alive (terminal)  6s
   w-003       run-0  running  active  none  alive (terminal)  9s
   w-004       run-1  idle     active  wait  alive (terminal)  12s
   w-005       run-0  running  active  wait  alive (terminal)  15s
   w-006       run-1  idle     active  none  alive (terminal)  18s
j/k move  Enter detail  / filter  n/p question  h history  e export  q quit        shown 6/6
```
(`reason unknown` moved to the title only as `reasons: unknown for all`; needs RR L50 edit. If the edit is refused, keep the word on each line and the saving is cells, not rows.)

Decision Desk, 160 columns: 22 rows vs 37 (saves 15). Same top 9 rows, then:
```
DECISION DESK  1h
Choose schema compatibility policy
w-001  running  next: wait  alive (terminal)  3s  wt-1 (this session only)
dispatch active | terminal active | outcome none
```
followed by the 8 ledger rows above and the footer.

Questions, 80 columns: 21 rows vs 25 (saves 4)
```
ORCA OBSERVER  live  scope=all  12:00:00
worker-list OK 0s | coordinator questions OK 0s | collected 6 / reported 6
no source: settled, frozen, cost, source counts
COORDINATOR QUESTIONS  one Run only: run_14cf..edf2
seen, not resolved: 3 | closed by evidence: unavailable
answered stay listed (no read marker); observed since 12:00 only
bounded best effort; coverage unknown; at most 100 rows per read, not 100
questions; bursts over 100 rows between reads may be lost
▸ 1h  Choose schema compatibility policy  reason unknown
  59m  Confirm deployment window  reason unknown
  59m  Name the release reviewer  reason unknown
worker-reported, not questions
  wait  w-001   3s        (6 worker rows, as today)
j/k move  Enter detail  / filter  n/p question  q quit
shown 6/6
```
This 80-column mock keeps the long disclosure and per-line `reason unknown` so it needs only the three small edits (header repeat, source-counts line, footer). With the shortened disclosure and `reasons` once it falls to 19 rows.

Decision Desk, 80 columns: 25 rows vs 39 (saves 14): the questions mock's first 11 rows, then
```
DECISION DESK  1h
Choose schema compatibility policy
w-001  running  next: wait  alive (terminal)  3s
wt-1 (this session only) | dispatch active | terminal active | outcome none
```
then the 8 ledger rows and 2 footer rows.

Worker ledger, 160 columns: saves 5 rows of overhead (rule row, `+N more` row, repeated scope and `worker-reported` lines, gap notice and `historical hidden` share a row), and about 75 columns, so the table fits 116 as well:
```
   dispatchId  run    state    status           next    liveness          age
   w-001       run-b  idle     active           none    alive (terminal)  10s
   w-002       run-c  blocked  blocked          review  alive (terminal)  13s
```

## 6. Ten biggest wins (ranked by rows or cells saved; risk)

1. Desk: 3 status fields + worktree + note to 2 rows: 9 rows at 160, 10 at 80. Risk low (AC-7 kept in 6 cells; defaults elided, unknown still shown).
2. Ledger: merge the 3 status columns and drop `flags`: about 55 cells per row. Risk low.
3. One `no source: settled, frozen, cost` token: about 50 cells, and the 80-column cut-off with `>` disappears. Risk low (still says unavailable).
4. `reason unknown` once instead of per line: 14 cells per question (about 100 cells at 7 questions). Risk medium (spec says never cut; "unknown is not none" kept in the title).
5. Footer keys: 3 rows to 1 at 80, 150 to 75 cells at 160. Risk none.
6. Merge caveat plus retention into one row, drop duplicate state line: 2 rows. Risk low.
7. Drop the repeated `scope=all`, collected count in footer, run id twice: about 60 cells, 0 rows. Risk none.
8. Drop rule row and `+N more` row on the ledger: 2 rows. Risk none.
9. Hash and path collapse in desk: up to 3 rows for a plan-ask, longer for a real hash and paths. Risk medium (touches D-6, RB-19, canaries; full text kept in inspector).
10. Shorten disclosure at 80 to one row: 1 row. Risk medium (spec says verbatim; long form stays in the inspector).

## 7. Three cuts I would not make

1. `collected n / reported T` and PARTIAL: they are the only proof the list is complete; RR L20 forbids cutting them.
2. `seen, not resolved: n | closed by evidence: unavailable`: it is the headline number for "is anything waiting on me"; the owner decided its wording and a bare number would read as "resolved".
3. `worker-reported, not questions` plus verbatim `nextAction.kind`: without that one row a worker's `wait` is read as a question, the exact confusion the observer was built to prevent. Also keep the question age and `[no longer in source window]`: the "how old, is it still there" signal.

Skipped: PNGs not viewed; 116-column text not diffed; no code or tests run. Risk: item 4 and 10 may be refused by the spec owner, in which case the stripped mocks gain only the free cuts.
