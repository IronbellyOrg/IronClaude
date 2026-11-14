# Round 1 advocate: Variant 1 (stale = older than 3 x the producer's interval)

Persona: architect (structure, dependencies, long-term impact). Sources read 2026-11-14: Q22 `question.md`, the three variants, `diff-analysis.md`, `src/superclaude/cli/observe/{collector,view,export,commands}.py`, ADJ (`alignment-findings-adjudicated.md`) lines 220-251 and 630-637, `merged-requirements.md` (grep of the stale, Q22, placeholder and optional-key lines).

## Position summary

Variant 1 answers Q22 with a rule that is already in the code (three missed producer intervals, `view.py:32-34`) instead of a guessed number, so the contract note (XC-05) and the Coder#477 text (CO-02) can be closed now without fixing a number for producers that do not exist yet (CO-03, CO-04 are DEFERRED). It is the best structural answer, but its observer number (45 s) is too tight for a file that the observer rewrites even while failing; I concede that point to Variant 3 and propose the merge below.

## Steelman

**Variant 2 (no number now, keep the interim rule).** Its strongest form: no program reads the snapshot or a Coder workspace record today (merged-requirements lines 355-356), so any number chosen now is a decision without a consumer, and the cheapest correct move is to defer it to the moment a real reader, a real write interval and a real transport delay exist. CO-02 item (1) explicitly allows the placeholder to stay with "owner decides" (merged-requirements line 354), so nothing is blocked. Its interim rule errs toward "stale", which is the safe direction: line 279 says "An old snapshot is not a current process heartbeat". It also found the real defect in the ADJ default (U-002): one cycle is too tight. What it gets right: decisions should be made against a real consumer, and the safe failure direction is "stale".

**Variant 3 (one fixed number, 2 minutes).** Its strongest form: one plain number is the easiest thing for a person reading a Coder issue and for every future reader to apply, with no lookup table. It closes the Coder#477 placeholder (ADJ line 634) so text A becomes paste-ready, and it sets a service level that the DEFERRED producers must design for, which is a legitimate way to constrain a future design early. Its number is grounded: twice the observer's 60 s backoff ceiling (`collector.py:30`), so a healthy but backing-off observer never reads stale. What it gets right, and what I underweighted: the snapshot is rewritten after failed cycles too ("exactly one write per cycle, after failures too", `commands.py:294-297`), so the file's `generatedAt` measures whether the producer is still writing, not whether its data is fresh; a file-age threshold should therefore tolerate backoff, and 2 minutes does.

## Strengths claimed

1. **The rule already exists in the producer.** The observer defines `STALE_SECONDS = 45.0  # three intervals without a successful poll, on the monotonic clock` (`view.py:32-34`) against `INTERVAL = 15.0` (`collector.py:28`). Variant 1 adopts that multiplier as the published rule, so the note states one principle that the code already embodies, instead of a second unrelated constant.
2. **It closes the decision without inventing facts about absent producers.** CO-03 (the Coder record) and CO-04 (the TUIBBS copy) are DEFERRED (merged-requirements lines 355-356). Variant 1 fixes the rule now and lets each producer's interval be stated when that producer is designed (variant-1 step 2). Variant 3 must guess a Coder cadence; Variant 2 must leave the question open.
3. **It keeps version 1 of the note honest.** ADJ line 222: "neither program reads the other, neither gains a file or key"; line 228: the snapshot has "no pid, no liveness flag ... a reader applies its own age rule to `generatedAt`". Variant 1 puts the interval in the note's registry (the note already has a "Registry of contracts", ADJ line 226), not in the snapshot, so nothing new is published (U-001). merged-requirements line 1196 leaves a later optional key possible without breaking this.
4. **It composes with the DEFERRED transport.** Variant 1 step 3 adds the CO-04 copy delay to the producer interval when CO-04 is designed. CO-04's own entry says "an age rule (Q22) ... specified" when opened (merged-requirements line 356); a rule that takes a delay term is the shape that requirement needs. A fixed 2 minutes must either absorb an unknown transport delay or be reopened.
5. **It tolerates ordinary timing.** The collector waits `next_interval` after each cycle finishes (`collector.py:354-360`) and a cycle may take up to `CYCLE_BUDGET = 15.0` (`collector.py:29`), so in normal operation the gap between snapshot writes can reach about 30 s (my inference from the loop, not measured). 45 s covers that; the one-cycle default (Variant 2) does not.
6. **It is testable against code.** ADJ line 225 asks for one test comparing the note with code constants. "3 x interval" lets that test assert `STALE_SECONDS == 3 * INTERVAL` and the note's registry value together, so a change to either constant fails a test (a proposal, not existing code).

## Weaknesses identified in other variants

1. **Variant 2's interim rule is worse than it admits.** It says the one-cycle rule can flicker "from ordinary timing jitter" (variant-2 risks). The code makes it structural, not jitter: the wait starts after the cycle ends (`collector.py:354-360`), so every write gap is 15 s plus the cycle's own duration, which exceeds one cycle on nearly every write. A reader on this rule would show a healthy observer's file as stale most of the time. Variant 2 also concedes the file does not carry the cycle, so the reader needs the note anyway; that is Variant 1's registry with a worse multiplier.
2. **Variant 2 leaves the CO-02 text incomplete.** Text A is paste-ready "except the `[N minutes: owner decides]` placeholder" and two other items (merged-requirements line 343). Keeping the placeholder is allowed (line 354) but means the issue is posted with an open acceptance criterion, and Q22 must be asked again later (variant-2 risks).
3. **Variant 3 couples two unrelated producers to one constant.** The observer (this repo, 15 s cycle) and a Coder workspace record (a separate repository, cadence unknown) get the same threshold. Its own risks section says 2 minutes "may be too short (constant false 'stale') or too long" for CO-03. That is a guess written into posted issue text and turned into a hard requirement on two DEFERRED designs (variant-3 steps 3-4); changing it later means editing posted text.
4. **Variant 3 opens a window where the screen and the file disagree.** Its own risk: the same observer data can be "stale" on screen and "current" in a file reader for up to 75 s. The mapping table rule is "never show one as the other" (ADJ line 250; merged-requirements line 486). Mitigation exists (the file also carries `source.status` and `source.observedAt`, `export.py:187-191`, `view.py:547-552`), but only if every reader reads both, which the note must then require.

## Concessions

- **45 s is too tight for the observer's file.** The file is rewritten once per cycle "after failures too" (`commands.py:294-297`), with `generatedAt` set to the wall time of the write (`view.py:555`). During backoff the wait doubles up to 60 s (`collector.py:30`) plus a cycle of up to 15 s, so a live, still-writing observer can leave a write gap of about 75 s (inference from the loop). Under Variant 1 its file reads stale at 45 s. The data in it is stale too, but that is already reported in the file's `source.status` (`STALE`/`ERROR`, `view.py:547`) and `source.observedAt` (last good read, `view.py:548-552`). So `generatedAt` age is the "is the producer still writing" axis, a different quantity from the screen's feed age (merged-requirements line 279 tells readers to keep them apart), and Variant 1's "same 45 s everywhere" claim partly conflates them. Variant 3 is right on this axis.
- **Proposed merge (my suggestion):** keep Variant 1's form but define the interval as the producer's maximum normal write gap, backoff included: stale = older than max(3 x nominal interval, the documented maximum write gap). For the observer that is about 75 s (UNVERIFIED until the gap is measured), which removes the backoff false alarm while keeping the per-producer rule.
- A formula reads less plainly than a number in the Coder issue, and the Coder minutes stay unknown until CO-03 is designed.
- The multiplier 3 is borrowed from the observer's choice, not from any measured reader need.
- None of the three variants, including mine, says how a reader handles a skewed clock (A-001).

## Shared assumption responses (A-001)

**QUALIFY.** `generatedAt` is wall-clock UTC (`view.py:555`, `format_utc_iso(clock.wall())`), while the observer's own 45 s rule runs on the monotonic clock in one process (`view.py:33`, `view.py:358`). On the same host the comparison is sound. For cross-host readers (CO-03 Coder, CO-04 TUIBBS) it is not, and the error grows as the threshold shrinks. Under Variant 1 the CO-04 design adds its copy delay and should add a stated clock-skew allowance in the same term; the note should say a reader that sees a negative or implausible age prints "age unknown", not "current". Variant 3's larger threshold tolerates skew best; Variant 2's one-cycle threshold tolerates it least.

## Per-point verdicts

| Point | Superior | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| C-001 | V1 | A rule fits the existing producer and future ones without guessing a cadence for producers that do not exist. |
| C-002 | V3 | The file is rewritten during backoff (gap about 75 s), so 120 s avoids marking a live observer's file stale; 45 s does not, 15 s far less. |
| C-003 | V1 | Derives the Coder threshold from its real interval at CO-03 design instead of fixing a guessed requirement now. |
| C-004 | V1 | Closes the placeholder with a rule rather than leaving it open (V2) or posting a guess (V3). |
| C-005 | V1 | Only V1 gives the transport delay a defined place in the rule. |
| X-001 | V1 | Narrowly: same multiplier keeps one principle and avoids a 75 s screen/file disagreement, but the quantities differ (see Concessions). |
| X-002 | V1 | Deciding the rule now and numbers per producer later unblocks XC-05 and CO-02 without a consumerless guess. |
| X-003 | V3 | A healthy producer in backoff should not read stale on the file-age axis; only 120 s covers the about 75 s write gap. |
| A-001 | V3 | No variant addresses skew; the largest threshold is the most tolerant of it. |

Overall: V1
