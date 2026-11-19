# Phase 4 gate (plan Phase 4, spec Phase 3), iteration 2: reviewer scorecards

Three fresh reviewers, one per width, text and ANSI tier (the PNG route is unavailable). The NO_COLOR and ASCII passes were present and read (ASCII: `+ - |` borders, no `?` on a border). Script rows come from `../checks.json`: every row passes except RB-22 (Low, deferred).

In scope: RB-01, RB-02 (questions and desk), RB-05 to RB-13, RB-15, RB-17 (census), RB-20 to RB-29. All other rows N/A (scheduled later; RB-19 replaced by RB-27).

| Row | 160 | 116 | 80 | Evidence (one line each, from the scorecards) |
|---|---|---|---|---|
| RB-01 colour roles | PASS | PASS | PASS | title bold cyan, ages bold amber, question text bold amber, subjects bold base, header2 and footer muted, rules slate |
| RB-02 titled frames | PASS | PASS | PASS | questions.txt:4 heavy amber `COORDINATOR QUESTIONS`; desk.txt:4 round slate list frame and desk.txt:14-16 heavy amber `DECISION DESK`, titles inset |
| RB-05 literals | PASS | PASS | PASS | disclosure, retention line, desk title whole |
| RB-06 NO_COLOR | PASS | PASS | PASS | 0 ESC bytes in every nocolor file; text equals the SGR-stripped stream |
| RB-07 ASCII | PASS | PASS | PASS | `+- COORDINATOR QUESTIONS ---+` and `\| ... \|`; only `?` is question text |
| RB-08 fit | PASS | PASS | PASS | widest cell equals the width; footer keys last; no blink or mouse sequences |
| RB-09 16 colour | PASS | PASS | PASS | distinct indexes per role |
| RB-10 state roles | PASS | PASS | PASS | `ACTIVE` and `yes (terminal)` green, `idle` and `wait` base |
| RB-11 absent muted | PASS | PASS | PASS | `worktree unknown`, `unavailable`, `reasons: none in source` muted |
| RB-12 heading | PASS | PASS | PASS | heading above the rows; no rule row under it (RB-28 forbids one; the 116 reviewer notes a literal reading of RB-12 would fail; logged in scores/p2/notes.md) |
| RB-13 key list | PASS | PASS | PASS | key groups whole; `n/p question` intact |
| RB-15 badge | PASS | PASS | PASS | `READ ONLY` right-aligned on line 1 |
| RB-17 census | PASS | PASS | PASS | run line, caveat and retention each once; no RETAIN CONTEXT frame yet (later phase) |
| RB-20, RB-21 | PASS | PASS | PASS | rule above the footer; counts line whole |
| RB-22 blank band | FAIL | FAIL | FAIL | Low, deferred: blank run 44 at 116, 25 at 80 (N = 18) |
| RB-23 selected row | PASS | PASS | PASS | whole selected row bold amber |
| RB-24 to RB-28 | PASS | PASS | PASS | script rows pass (census, reasons, status badge, no hash, ledger diet) |
| RB-29 order and labels | PASS | PASS | PASS | question rows lead the list pane; desk labels plain with one value column; no `msg_` id |

failing_high_medium: [] at every width.

Iteration 1 (same folder layout in `../../iter-1/`): the 160 reviewer failed RB-29 (the run, state and count lines came before the first question row); the 116 and 80 reviewers passed every High and Medium row. Fix before iteration 2: the question rows now lead the list pane, the Run id moved into the frame title, and the state, count and reasons note moved under the rows.
