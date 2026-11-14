# How old can a status file be before readers call it stale?

## Question in one sentence
When a program reads a status file written by another program, at what age should it say "this file is stale" instead of treating it as current?

## Why you are being asked
Two pieces of text are waiting on this: the contract note that describes what the observer and the sweep share (XC-05), and the narrowed text of the Coder issue Coder#477, which has an open blank "[N minutes: owner decides]". The review left the number to you.

## Background you need
- The observer (`superclaude observe`) is the built dashboard of Orca agent workers. While running, it checks every 15 seconds and rewrites a file, `snapshot.json`, each time, even after a failed check. After errors it waits up to 60 seconds.
- On its own screen it calls its data stale after 45 seconds (three missed checks).
- The file has a timestamp, `generatedAt`, and no "still alive" flag. The file also already says, inside it, whether its data was fresh.
- The Coder workspace record and a copy channel to the owner's other platform (TUIBBS) are not built. Nobody reads these files yet.

## Your options

### 1. A rule: stale after three intervals or the longest normal gap, whichever is larger (recommended)
- If you pick this: the observer's file is stale after about 75 seconds (inferred from its code); the Coder record and copy channel get numbers when they are designed. Readers always print the age and keep "stale file" separate from "stale data".
- Upside: matches how the observer actually writes; no guess for things not built yet.
- Downside: the Coder issue shows a formula, not a number; 75 seconds is inferred, not measured.

### 2. One fixed number now (suggested: 2 minutes, or your own)
- If you pick this: both kinds of record are stale after 2 minutes; future producers must write at least that often.
- Upside: one plain number; closes the Coder issue blank now.
- Downside: a guess for a producer that does not exist; little time left for copying the file to another host.

### 3. No number yet
- If you pick this: keep the review's stopgap ("older than one of the producer's cycles is stale") and ask again when a reader is built.
- Upside: decided against a real reader later.
- Downside: the stopgap (about 15 seconds) would make a normal observer file flip between fresh and stale; the Coder issue blank stays open.

## What the debate found
- All three advocates agreed the stopgap in option 3 flickers and should not be kept.
- The code shows a live observer can leave about 75 seconds between writes, so 45 seconds is too tight for the file.
- Option 1 won 6 of 10 points; option 2's number won on the observer threshold only.

## Recommendation and confidence
Option 1, about 70 percent.

## If you do not answer
The stopgap applies: readers call any file older than one producer cycle stale and print its age. The Coder issue keeps "[N minutes: owner decides]".

## What this answer does not authorize
It does not post anything to Coder#477, build any reader, or add any field to the snapshot file.

## How to answer
Type: "Q22: option 1" (or "Q22: option 2, N minutes", or "Q22: option 3").
