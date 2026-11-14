<!-- Provenance: sc:adversarial Step 5 merge for owner question Q22 -->
<!-- Base: Variant 1 (proposal-A), adversarial/variant-1-original.md -->
<!-- Plan: adversarial/refactor-plan.md (4 planned changes, all applied) -->
<!-- Incorporated: Variant 3 (Changes 1 and 2), Variant 2 (Changes 2 and 4), all three advocates (Change 3) -->
<!-- Merge date: 2026-11-14; executor: merge-executor -->

<!-- Source: Variant 1 title, reworded for Change 1 (Variant 3 via round1-advocate-V3.md C-002, X-003; round1-advocate-V1.md Concessions) -->
# Proposal A, merged: a rule, not a number: stale means older than three producer intervals or the producer's longest normal write gap, whichever is larger

<!-- Source: Variant 1 "Answer", replaced by Change 1 (Variant 3, round1-advocate-V3.md Strengths, C-002, X-003; round1-advocate-V1.md Concessions, proposed merge) -->
## Answer

A file is stale when the age of its `generatedAt` exceeds the larger of two values: (a) three times its producer's nominal writing interval, the multiplier the observer already uses for its own feed (three missed 15-second polls = 45 seconds), and (b) that producer's documented longest normal gap between writes, backoff included. For the observer snapshot, (a) is 45 seconds and (b) is about 75 seconds (an inference from the code, not a measurement), so the threshold is about 75 seconds. For a Coder workspace record both values are fixed in writing when that producer is designed.

## What happens next if the owner picks it

<!-- Source: Variant 1 step 1, replaced by Change 1 (Variant 3; Variant 1 advocate), with Change 3 inserted (all three advocates, A-001 responses) and Change 4 appended (round1-advocate-V2.md Concession 1) -->
1. The contract note draft (XC-05) states the rule once: "stale file = `generatedAt` age greater than the larger of 3 x the producer's nominal interval and the producer's documented longest normal gap between writes, backoff included; readers always print the age". Its registry lists each producer's values:
   - Observer snapshot: interval 15 s, so (a) = 45 s (`collector.py:28`, `view.py:32-34`). The observer rewrites the file once per cycle even after failures (`commands.py:294-297`) and waits up to 60 s after errors plus a cycle of up to 15 s (`collector.py:28-30`), so (b) is about 75 s. That figure is an inference from the code, not a measurement. The threshold is therefore about 75 s. If a measurement shows a longer gap, the note uses the measured value.
   - Clock rule: the age rule assumes the reader and the producer share a host clock (`generatedAt` is wall-clock UTC, `view.py:555`). A reader that computes a negative or implausible age prints "age unknown", never "current". CO-04 states a clock-skew allowance alongside its copy delay.
   - The note replaces ADJ's interim "older than one producer cycle" rule (ADJ line 792), which would flicker on ordinary timing.

<!-- Source: Variant 1 step 2, updated for consistency with Change 1 -->
2. The Coder#477 text (CO-02) replaces `[N minutes: owner decides]` with "the larger of three times the record's stated write interval and its stated longest normal write gap", and the CO-03 design (DEFERRED) must state both values.

<!-- Source: Variant 1 step 3, unchanged -->
3. The CO-04 copy channel (DEFERRED) adds its copy delay to the producer's interval when it is designed, so a copied file is not judged stale by transport delay alone.

<!-- Source: Variant 1 step 4, updated for consistency with Change 1 -->
4. No new key is added to the snapshot: the interval and the longest write gap live in the note, not in the file, so "publishes nothing new in version 1" (ADJ line 222) still holds.

## What it unlocks

<!-- Source: Variant 1 bullet 1, replaced by Change 2 (round1-advocate-V3.md X-001; round1-advocate-V2.md Strength 2) -->
- Two ages, never one. File age (`generatedAt`) answers "is the writer still alive". Data age is carried by the snapshot's `source.status` and `source.observedAt`, which already hold the observer's own 45 s feed verdict (`view.py:543-553`). Readers show both; "stale file" and "stale data" are separate words, in line with the mapping-table rule "never show one as the other" (ADJ line 250).

<!-- Source: Variant 1 bullet 2, unchanged -->
- A rule that fits a producer that does not exist yet (the Coder record), without guessing a number for it today.

<!-- Source: Variant 1 bullet 3, updated for consistency with Change 1 -->
- Tolerance for normal timing: a producer that is a few seconds late, or backing off after errors (up to 60 s, `collector.py:30`), is not shown as a stale file while it is still writing, because the threshold covers its longest normal write gap, not one cycle.

## What it costs or risks

<!-- Source: Variant 1 cost bullet 1, updated for consistency with Change 1 -->
- It is not one plain number; a person reading the Coder issue sees a formula with two terms, and the actual minutes are known only when CO-03 is designed.

<!-- Source: Variant 1 cost bullet 2 (backoff), replaced for consistency with Changes 1 and 2; wording from round1-advocate-V3.md Concession 3 and refactor-plan.md Change 1 -->
- A stopped observer is flagged as a stale file only after about 75 s, not after 45 s. During error backoff the file does not read stale while the observer is still writing; the missing fresh data shows instead in `source.status` (see "Two ages, never one" under What it unlocks). The 75 s figure is inferred from the code, not measured, and moves if a measurement shows a longer gap.

<!-- Source: Variant 1 cost bullet 3, updated for consistency with Change 1 -->
- A `--once` snapshot has no interval; under this rule it reads stale after the observer's threshold of about 75 s, which is correct (a one-off file is not a heartbeat) but must be said in the note.

<!-- Source: Variant 1 cost bullet 4, unchanged -->
- The multiplier 3 is borrowed from the observer's own choice, not from any measured reader need.

## What stays unresolved

<!-- Source: Variant 1 bullet 1, updated for consistency with Change 1 -->
- The Coder workspace record's interval and longest write gap, until CO-03 is designed.

<!-- Source: Variant 1 bullet 2, unchanged -->
- The copy delay of the TUIBBS channel, until CO-04 is designed.

<!-- Source: Change 3 (all three advocates, A-001 responses) -->
- The clock-skew allowance for a reader on another host, until CO-04 is designed.
