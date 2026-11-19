70a5431953263e7683b6e3799361d7faab99761b
minor F1.1 (ac2-source-list): the attention pane also carries view.historical_note and the ledger pane the LEDGER_LEGEND line; both come from the old head and the ledger title; the source-scan test already allows historical_note.
minor F1.2 (test-brittleness): the plain-head test reads ln[:1] in "╭┏╰┗│┃"; an empty line would match; it passes today, tighten in Task 27 when the ledger tests are reworked.
note: 14 older ledger tests and the release-1 golden still read the unframed ledger; Task 27 reworks them.
note: the framed ledger uses margin 0 and a border-only table frame (pad 0); the head panes use pad 1; threshold measured and recorded in scores/p6/notes.md.
