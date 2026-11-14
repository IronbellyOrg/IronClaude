# Round 1 advocate: Variant 3 (fixed 2 minutes)

Persona: analyzer (evidence quality, logical consistency). All code paths are under `src/superclaude/cli/observe/` unless stated; all were read on 2026-11-14 in the issue-339 worktree.

## Position summary

For the observer snapshot, the file-age threshold must sit above the longest gap a live observer can leave between two writes, and the code puts that gap at up to about 75 s; 2 minutes is the only proposed number that clears it, while 45 s (V1) and one cycle (V2) mark a live observer's file stale. The snapshot already carries the observer's own 45 s data-freshness verdict in `source.status`, so `generatedAt` age answers a different question ("is the writer still alive?") and does not need to match 45 s. V3 is weaker than V1 on the Coder record and the TUIBBS copy channel, where its fixed number is a guess.

## Steelman

**V1 (rule of three intervals).** Strongest form: "stale" should mean one thing wherever a person sees it. The observer already decided that three missed polls (45 s, `view.py:32-34`) is stale, so a file reader using the same 45 s can never contradict the screen. A rule tied to the producer's own interval also extends to producers that do not exist yet (the Coder record) without guessing a number. It keeps the interval in the note and out of the file, so "publishes nothing new in version 1" (ADJ line 222) holds. V1 also admits its own backoff weakness (variant-1 "What it costs", bullet 2). These points are sound, especially the per-producer framing for unbuilt producers. The critique is below (W-1, W-2): the code shows the 45 s rule measures something other than `generatedAt` age, so the same number does not give the same meaning.

**V2 (no number now).** Strongest form: no program reads these files today (CO-03 and CO-04 are DEFERRED, merged-requirements.md lines 355-356), CO-02 explicitly allows keeping the placeholder with "owner decides" (line 354), and any number chosen now is chosen without a real reader, write cadence or transport delay. The interim default errs toward calling a file stale, and the age is always printed, so no person is told an old file is current (line 279: "An old snapshot is not a current process heartbeat"). V2's own flicker finding (U-002 in diff-analysis.md) is the most useful single observation in the three proposals. The critique (W-3, W-4) is that the code makes the interim rule much worse than "jitter", and that Q22 is a W1 decision (line 861) for a producer that does exist: the observer.

## Strengths claimed

1. **2 minutes is the only proposed threshold above a live observer's worst write gap.** The collector loop runs a cycle, then waits `next_interval` (`collector.py:354-360`), and `next_interval` is `self._wait` (`collector.py:195-198`), which doubles after failures up to `MAX_BACKOFF = 60.0` (`collector.py:30,315`). A cycle can take up to `CYCLE_BUDGET = 15.0` (`collector.py:29`). The snapshot is written "exactly one write per cycle, after failures too" (`commands.py:296-297`). So the gap between two writes is cycle duration plus wait: up to about 30 s in normal running (15 + 15) and up to about 75 s in sustained failure (15 + 60). V3's 120 s is above 75 s with 45 s of margin. V3's own text gives the reason as "twice the 60 s backoff" (variant-3 line 5); the real worst gap is 75 s, not 60 s, so V3 understated it, but the number still holds. (The UI thread's own read delay between the cycle finishing and the write is not measured here: UNVERIFIED, assumed small.)
2. **The snapshot already carries data freshness, so file age only needs to detect a dead writer.** The exported `source.status` is `OK`/`STALE`/`ERROR` (`export.py:187-191`, `view.py:170,547`), computed by `source_state()` with the 45 s rule (`view.py:353-360`, called at `view.py:768` and passed to `_meta` at `view.py:884`). `source.observedAt` is the time of the last successful poll (`view.py:548-551`). `generatedAt` is the wall clock at write time (`view.py:555`). Therefore a reader of a file written by a live observer already sees "feed stale" from the file itself after 45 s; the only case the Q22 threshold adds is the writer having stopped. A threshold above the live writer's worst gap separates those two cases cleanly; a lower one blurs them.
3. **This also removes V3's own conceded risk.** Variant-3 "What it costs", bullet 2, says the same data can be "stale" on screen and "current" in a file for up to 75 s. Strength 2 shows that is not so while the writer is alive: the file says `source.status: "STALE"` at the same 45 s. A gap remains only after the writer dies, which is exactly the window the threshold is meant to bound. The mapping table already separates the two meanings: "Observer feed 45 seconds; stored snapshot uses the age policy" (merged-requirements.md line 486), and line 279 requires readers to "Distinguish feed age, stored-file age".
4. **One plain number answers the question as asked.** The question is "What age makes ... stale?" (question.md line 5) and the Coder#477 slot is literally `[N minutes: owner decides]` (ADJ line 634). V3 fills both with no lookup table (variant-3 "What it unlocks").
5. **Most tolerant of clock error.** All three measure from `generatedAt`, a wall-clock value (`view.py:555`). A cross-host reader with skew misjudges a small threshold proportionally more; 120 s absorbs tens of seconds of skew that would break 15 s or 45 s (see A-001).

## Weaknesses identified in other variants

1. **V1: same number, different measurement.** The 45 s rule counts time since the last *successful poll* on the monotonic clock (`view.py:32-34,358`). A file reader using 45 s counts time since the last *write*, on the wall clock. The observer writes after failed cycles too (`commands.py:296-297`), so these diverge in both directions: during an outage the file is fresh by `generatedAt` while the feed is stale (already reported in `source.status`), and during backoff the file can be older than 45 s while the writer is alive. V1's claim "one meaning of stale across the observer's screen and any reader of its file" (variant-1 "What it unlocks", bullet 1) does not hold as stated.
2. **V1: 45 s is below a live observer's backoff write gap.** With waits up to 60 s plus a cycle of up to 15 s (strength 1), a live, backing-off observer's file crosses 45 s on every long-backoff cycle. V1 calls this "arguably correct (no fresh data)" (variant-1 cost bullet 2), but "no fresh data" is already reported by `source.status`; the file-age verdict then adds a false "writer gone" signal. V1's multiplier is applied to the nominal interval (15 s), not to the worst write gap, which is the quantity that matters for file age.
3. **V2: the interim rule is wrong in normal running, not only under jitter.** The normal write gap is cycle duration plus a 15 s wait (strength 1), so any non-zero cycle duration puts the file past one cycle (15 s) before the next write. A reader on the interim rule would show a healthy observer's file as stale for part of every cycle, and always during backoff. V2 calls this flicker "from ordinary timing jitter" (variant-2 cost bullet 1); the code shows it is structural.
4. **V2: defers a decision that has a real producer now.** The observer exists and writes `snapshot.json` today (`export.py`, `commands.py:296-299`); Q22 is listed among W1 owner answers (merged-requirements.md line 861) and XC-05 must list "the Q22 age policy" (line 476). Keeping a default that V2 itself shows to be defective, instead of fixing the number for the one producer that exists, leaves XC-05 documenting a rule its authors know flickers.
5. **V1 and V2: neither gives the reader a margin for clock skew** (A-001), and both use the smallest thresholds.

## Concessions

1. **The Coder record number is a guess.** No Coder producer exists (merged-requirements.md line 355). V3's step 3, "its producer must write at least every 2 minutes" (variant-3 line 11), imposes a requirement on a DEFERRED design without evidence. V1's "three times the record's stated write interval", set when CO-03 is designed (variant-1 step 2), is more honest here, and V2's deferral is defensible.
2. **The TUIBBS copy budget is tight.** If a live observer can leave a 75 s gap, V3's "deliver a copy within 2 minutes of `generatedAt`" (variant-3 step 4) leaves about 45 s for transport. V1's "add the copy delay to the producer's interval" (variant-1 step 3) is the better design rule for CO-04.
3. **Dead-writer detection is slower.** A stopped observer is flagged after 120 s under V3, against 45 s under V1. If the owner values fast "observer died" detection over false alarms during backoff, V1's number is better for that.
4. **V3's stated rationale was imprecise** (60 s, not the real 75 s worst gap), and its "75 seconds" mismatch cost was overstated (strength 3). Both errors were in V3's own text.
5. **`--once` snapshots.** V3 does not say how a one-off file is judged; V1 does (variant-1 cost bullet 3). Under V3 a `--once` file reads current for 2 minutes, which the note must state.
6. The best answer is probably a hybrid: V3's number for the observer snapshot, framed by V1's per-producer rule keyed to the producer's worst-case write gap, with the Coder and TUIBBS numbers set when CO-03 and CO-04 are designed.

## Shared assumption responses (A-001)

**A-001: QUALIFY.** The assumption holds for a reader on the observer's own host (same wall clock), which is the only reader the observer has today; it does not hold for the cross-host readers in CO-03 and CO-04, where nothing bounds skew. `generatedAt` is wall clock (`view.py:555`), unlike the screen's monotonic 45 s rule (`view.py:32-34`). The XC-05 note should state that the age rule assumes the same host, and CO-04's design should either measure age from its own receipt time plus the producer's stated age or state a skew allowance. A larger threshold (V3) tolerates skew best but does not remove the need to state it.

## Per-point verdicts

| Point | Superior | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| C-001 | V3 (narrow) | A single number fits the question and the `[N minutes]` slot; V1's formula is keyed to the nominal interval, not the worst write gap, so as written it misjudges the one real producer. |
| C-002 | V3 | 120 s is above a live observer's worst write gap of about 75 s (`collector.py:29,30,354-360`; `commands.py:296-297`); 45 s and 15 s are not. |
| C-003 | V1 | No Coder producer exists; deferring its number to CO-03 under a stated rule beats V3's guessed hard requirement. |
| C-004 | V1 | The Coder#477 line concerns the unbuilt Coder record, so a rule tied to its stated interval is more honest than a guessed "2 minutes". |
| C-005 | V1 | Adding copy delay to the threshold is a sound design rule; V3's 2-minute delivery budget leaves about 45 s after a 75 s live gap. |
| X-001 | V3 | The file already carries the 45 s verdict in `source.status` (`view.py:358,547,768,884`); `generatedAt` age measures writer liveness, a different meaning, so it should not reuse 45 s. |
| X-002 | V1 | Setting the rule now and per-producer numbers when each producer is designed balances W1's need against the absence of a Coder reader. |
| X-003 | V3 | A live writer in backoff should not read "writer gone"; the data-staleness signal is already in the file. |
| A-001 | V3 | None of the three addresses skew; the largest threshold is the most tolerant of it. |

Overall: V3
