Implementer claims (A3 + its repair, not verified):
- A3 rewrote the note from brief 3 (advice-3-a): same sections as A2; "What it is" now says one atomic write; the Safe apply first bullet says the brief allows only audit.md and K1 fails on a changed spec; the blanket "every failure path" bullet became a per-step failure list (check, apply re-check, exact-once/overlap stop, write failure with copy-back, the uncovered log-write gap).
- Repair 3-1 widened the K1 parenthetical to the baseline sha256 as well.
- The exact-once/overlap bullet was taken from the brief and source.md 2.3 item 4 without checking which code path (check K7/K8/K9 or apply's own guard) prints the message.
- Believed T9.AC1 and T9.AC2 met (literals log, tests/docs 11 passed).
