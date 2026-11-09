Implementer claims (A1 + A2, not verified):
- Built cmd_verdict: closed ids from closed-minor.txt when the audit applied; DOWNGRADE ids from check.log; held = closed + downgrades; R3 parsed with the T2 parse_report (graded records need a severity label; prior rows need a prior heading or a status cell); unparseable when R3 has no resolution rows or no final verdict line.
- A2 fix pass: held takes every DOWNGRADE id whatever the audit state; added unlabelled_blocking() so an id-cell row outside the resolution table that says "blocking" but has no label counts in new_blocking.
- Owner count: new_cm = R3 graded ids labelled CRITICAL/MAJOR; held_cm = held ids labelled CRITICAL/MAJOR in R2, skipping any id R3 also grades.
- Believed T5.AC1-AC3 met (93 tests pass). Known gaps from review 2: an id row with no grade at all is still dropped; held ids R3 re-lists as MINOR are dropped from the owner count; resolution rows with an unknown status are treated as not open.
