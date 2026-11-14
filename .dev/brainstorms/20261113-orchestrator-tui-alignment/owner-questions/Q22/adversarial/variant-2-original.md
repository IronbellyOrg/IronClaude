# Proposal B: no number now; keep the interim rule until a real reader exists

## Answer

Do not set a number yet. Keep the interim rule already written in the review: a reader shows any file older than its producer's own cycle as stale and always prints its age. Set a number only when a program that actually reads these files (the Coder workspace status feature or a TUIBBS screen) is designed.

## What happens next if the owner picks it

1. The contract note draft (XC-05) records the interim rule as "the owner's number is not set (Q22 answered: not yet); until then, older than the producer's own cycle is stale; the age is always printed" (ADJ line 792).
2. The Coder#477 text (CO-02) keeps `[N minutes: owner decides]` and the reply says the owner deferred it, which CO-02's item (1) already allows (merged-requirements.md line 354).
3. When CO-03 (the Coder-repo implementation) or CO-04 (the TUIBBS copy channel) is opened, Q22 is asked again with that reader's real interval and needs in hand.
4. Nothing else changes; no program reads these files today (CO-03 and CO-04 are DEFERRED, merged-requirements.md lines 355, 356).

## What it unlocks

- XC-05 and CO-02 can proceed now without a decision that has no consumer yet.
- The number, when chosen, is chosen against a real reader, a real write interval and a real transport delay instead of a guess.
- The rule is safe in the direction that matters: it errs toward calling a file stale, and the age is always printed, so a person is never told an old file is current (merged-requirements.md line 279: "An old snapshot is not a current process heartbeat").

## What it costs or risks

- The interim rule is strict: the observer writes about every 15 s (`collector.py:28`), so a snapshot can be judged stale after just over 15 s from ordinary timing jitter, and during error backoff (up to 60 s, `collector.py:30`) it will read stale. A reader built on this rule would flicker between fresh and stale.
- "Older than the producer's own cycle" needs the reader to know the cycle; the snapshot does not carry it, so the reader must take it from the note.
- The question comes back later, and the open placeholder stays visible in the Coder issue text.

## What stays unresolved

- The number itself.
- The cycle of a Coder workspace record producer, which does not exist yet.
