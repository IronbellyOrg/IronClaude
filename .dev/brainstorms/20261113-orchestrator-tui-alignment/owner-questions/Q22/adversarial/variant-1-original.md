# Proposal A: a rule, not a number: stale means older than three of the producer's own intervals

## Answer

A record is stale when it is older than three times its producer's normal writing interval, the same rule the observer already uses for its own feed (three missed 15-second polls = 45 seconds). For the observer snapshot that is 45 seconds; for a Coder workspace record it is three times that producer's interval, fixed in writing when that producer is designed.

## What happens next if the owner picks it

1. The contract note draft (XC-05) states the rule once: "stale = older than 3 x the producer's nominal interval, measured from `generatedAt`; readers always print the age". Its registry lists each producer's interval: observer snapshot 15 s, so stale at 45 s (`collector.py:28`, `view.py:32-34`).
2. The Coder#477 text (CO-02) replaces `[N minutes: owner decides]` with "three times the record's stated write interval", and the CO-03 design (DEFERRED) must state that interval.
3. The CO-04 copy channel (DEFERRED) adds its copy delay to the producer's interval when it is designed, so a copied file is not judged stale by transport delay alone.
4. No new key is added to the snapshot: the interval lives in the note, not in the file, so "publishes nothing new in version 1" (ADJ line 222) still holds.

## What it unlocks

- One meaning of "stale" across the observer's screen and any reader of its file: today the observer calls its feed stale at 45 s (`view.py:32-34`); this rule gives a file reader the same 45 s.
- A rule that fits a producer that does not exist yet (the Coder record), without guessing a number for it today.
- Tolerance for normal timing: a producer that is a few seconds late, or backing off after errors (up to 60 s, `collector.py:30`), is shown stale only after three missed writes, not after one.

## What it costs or risks

- It is not one plain number; a person reading the Coder issue sees a formula, and the actual minutes are known only when CO-03 is designed.
- During the observer's error backoff (waits up to 60 s) the snapshot can cross 45 s and show stale while the observer process is still alive. That is arguably correct (no fresh data) but may surprise.
- A `--once` snapshot has no interval; under this rule it reads stale after 45 s, which is correct (a one-off file is not a heartbeat) but must be said in the note.
- The multiplier 3 is borrowed from the observer's own choice, not from any measured reader need.

## What stays unresolved

- The Coder workspace record's interval, until CO-03 is designed.
- The copy delay of the TUIBBS channel, until CO-04 is designed.
