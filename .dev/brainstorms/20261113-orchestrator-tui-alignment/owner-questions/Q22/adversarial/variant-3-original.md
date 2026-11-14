# Proposal C: the owner sets one fixed number now: 2 minutes for both kinds of record

## Answer

The owner sets one plain number now, the same for the observer snapshot and any Coder workspace record: a record older than 2 minutes is stale. (2 minutes is this proposal's candidate; the owner may substitute any number. It is twice the observer's longest error-backoff wait of 60 s.)

## What happens next if the owner picks it

1. The contract note draft (XC-05) states: "A snapshot or workspace record whose `generatedAt` is more than 2 minutes old is stale; readers print the age in every case."
2. The Coder#477 text (CO-02) replaces `[N minutes: owner decides]` with "2 minutes" (merged-requirements.md line 354, item (1)).
3. CO-03 (the Coder-repo implementation, DEFERRED) inherits a hard requirement: its producer must write at least every 2 minutes, or its records will always read stale.
4. CO-04 (the TUIBBS copy channel, DEFERRED) must deliver a copy within 2 minutes of `generatedAt`.

## What it unlocks

- The placeholder in the Coder issue is closed now and the issue text reads complete.
- One number every reader can apply without looking anything up: no formula, no per-producer table.
- A healthy observer never looks stale: it writes about every 15 s and waits at most 60 s after errors (`collector.py:28,30`), well inside 2 minutes.
- It sets a clear service level for the producers that do not exist yet, which constrains their design early.

## What it costs or risks

- The number is a guess for the Coder record: no producer exists, so 2 minutes may be too short (constant false "stale") or too long for whatever cadence CO-03 chooses.
- 2 minutes is looser than the observer's own feed rule (45 s, `view.py:32-34`), so the same observer data can be "stale" on its own screen and "current" in a file reader for up to 75 seconds; the mapping table must explain the difference ("feed stale" against "file stale", ADJ line 250).
- Choosing a number now fixes a requirement on two DEFERRED designs before they are opened; changing it later means editing posted issue text.

## What stays unresolved

- Whether 2 minutes suits the Coder record producer and the TUIBBS copy channel, until each is designed.
