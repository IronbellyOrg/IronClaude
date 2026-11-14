# Proposal C: no channel; record that no TUIBBS screen is planned and drop the item

## Answer

No. Record that no TUIBBS screen is planned, keep the observer single-host as a stated scope, and remove CO-04 (the copy channel) from the program; if TUIBBS ever becomes real, it starts as a new item with its own owner question.

## What happens next if the owner picks it

- The ledger records "Q18: no; no TUIBBS screen planned" with the date.
- CO-04 is closed as "not planned" rather than left deferred (merged-requirements.md line 356).
- The Coder#477 reply (CO-01) says the observer is single-host and no TUIBBS channel is planned. With Q3's recommendation, this is the condition under which closing Coder#477 is preferred ("close if the observer stays single-host and TUIBBS is not near", ADJ line 773).
- The contract note keeps "single owner, single OS user, single host" (line 453) without a pending exception.

## What it unlocks

- One fewer deferred item and one fewer cross-host risk to track.
- A clear basis for the Q3 answer on Coder#477 (close rather than narrow).
- No pressure on Q22 or on an authentication design for a second host.

## What it costs or risks

- The snapshot was deliberately shaped so a TUIBBS screen could read it later (ADJ glossary line 91); dropping the item discards that intent unless the owner no longer holds it.
- The owner's record says "may become a TUIBBS module" (ADJ line 306); a "no" now overrides a "maybe" with a "no" the record does not contain.
- If TUIBBS returns, the design starts from nothing, and Coder#477 may have been closed in the meantime.

## What stays unresolved

- Nothing within this program; any future TUIBBS work is a new decision.
