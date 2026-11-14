# Round 1 advocate: Variant 1 (historical), frontend persona

All code citations were read on 2026-11-14 in this worktree (`src/superclaude/cli/observe/view.py`, `src/superclaude/cli/sweep/classify.py`), plus INV-023 (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/invariant-probe.md` line 30) and the ADJ mapping row (`alignment-findings-adjudicated.md` line 258).

## Position summary

From the screen's point of view, Variant 1 gives the only default view that answers "what is working right now?": at the probe it would show an empty list with "100 historical hidden (h)" under a header that still reads "active 0 / reclaimable 27 / retained 32 / released 41". Today's view (kept by V2 and V3) shows 27 finished workers mixed in with whatever is running. The case for V1 is strong on the screen. Its weak spot is that it settles a meaning nobody has confirmed (A-001). Because of that I judge V3 the better owner answer today, with V1 as the follow-up once one Orca read confirms the meaning.

## Steelman

**Variant 2 (live side, as built).** At its strongest, V2 says the observer is a cleanup tool as much as a monitor. Orca's own next action for a reclaimable worker is `release`, and the observer prints that action verbatim in the next-action column (`view.py:420-424`, `view.py:454`). Keeping those rows in the default view puts unfinished cleanup in front of the person who has to do it. It costs nothing: no code, no test, no PR. It ratifies what PRs #503 and #514 already shipped, and the sweep already agrees that the state needs attention ("could not determine", "result read not observable", `classify.py:479-481`). That reasoning holds up. A to-do the screen keeps showing is harder to forget than one behind a key.

**Variant 3 (its own state until known).** At its strongest, V3 is the epistemically honest answer. No file read defines `reclaimable` (question.md fact row 34), so any side chosen now is a guess written into a contract note that two programs will cite. V3 unblocks OB-06 and XC-05 today, adds no code, and adds no wording that could be wrong. The observer already shows Orca's word verbatim (`view.py:452`) and never calls a row "live" (a grep of `view.py` for `live` as a word found no label using it). It also names a cheap, concrete way to settle the meaning: one help-text or detail read of a reclaimable worker added to the XC-03 capture (diff U-002). It matches the spec's recommended default (merged-requirements.md line 550) and the ADJ draft row word for word (ADJ line 258).

## Strengths claimed

1. **The default view would show what is working, which is what a person scans for.** INV-023 records the probe counts: reclaimable 27, released 41, retained 32, active 0. With `HISTORICAL_STATES = ("released", "retained")` (`view.py:35`), the default view keeps the 27 reclaimable rows. The sort is by liveness and evidence timestamp, not by state (`_sort_key`, `view.py:373-378`), so finished rows are interleaved with any running ones instead of collecting at the bottom. V1 is the only variant that removes them from the default list.
2. **Hiding does not remove the cue. The screen still says how many there are and how to see them.** The header always prints `source counts: active N / reclaimable N / retained N / released N` (`_source_counts_text`, `view.py:578-586`, added at `view.py:810`), whatever the historical setting. When rows are hidden, the screen adds "`{n} historical hidden (h)`" (`view.py:902-903`). If every row is hidden, the list says "no rows match the filter or the historical setting" (`NO_MATCH_TEXT`, `view.py:94`). V2's main argument, the cleanup cue, is therefore still on screen under V1: "reclaimable 27" in the header, one key away.
3. **The change is the smallest possible one, and it uses an existing mechanism.** One tuple entry at `view.py:35`. `is_historical` (`view.py:363-366`) and the hide/show path (`view.py:844-848`) need no change, and `h` toggles them (`view.py:1038`). Proposal A step 2 limits the test to "hidden by default, shown with `h`".
4. **It matches what the invariant expected.** INV-023's invariant is "A Run whose workers have all exited shows as historical in both programs" (invariant-probe.md line 30). V1 is the only variant that makes that invariant hold in the observer.
5. **It is honest about the remaining cross-program gap.** V1 alone notes that the sweep's "historical" (6 h window) and "settled" (`outcome`, `classify.py:98,114-115`) still differ from the observer's terminal-state meaning, so the note must say so whatever Q23 answers (diff U-001). That is true under all three variants, and V2 and V3 leave it unsaid.
6. **The sweep needs no change.** `_settled` reads `outcome` only (`classify.py:114-115`) and `_lifecycle` follows it (`classify.py:781-786`). The reclaimable branch stays "could not determine" (`classify.py:479-481`).

## Weaknesses identified in other variants

1. **V2: the cleanup cue it defends is already on screen without the rows.** The header count (`view.py:578-586`) and the next-action column both carry it. Keeping 27 full rows in the default list repeats a signal the header already gives, and it crowds out the rows a person opened the observer to see. V2's own risk section concedes this: "A person scanning for working agents sees a list of finished ones."
2. **V2 adds a word the screen never shows.** Its mapping row says "awaiting release", but the observer prints only Orca's `terminal_state` and `next_action_kind` verbatim (`view.py:452`, `view.py:420-424`). The note would describe a label that does not exist on screen. That is harmless, but it is not a UX gain.
3. **V2 decides on the same unconfirmed meaning V1 does.** Both reason from the name and the `release` action (diff X-002). V2 is no more grounded than V1. It only fails in the safer direction: noise rather than a hidden row.
4. **V3 changes nothing a person sees.** Its own risk section says so: "'its own state' names the problem without fixing it." The screen under V3 is identical to V2's: 27 finished rows in the default view at the probe.
5. **V3's provisional row has no owner or trigger.** Its reopen step says "for example" via XC-03, but question.md fact row 35 says XC-03 "does not list `reclaimable` among its recordings" and has not run. Without a required line in XC-03, the provisional row can stay provisional, which V3 itself admits ("without a trigger it can stay provisional indefinitely").

## Concessions

1. **A-001 is V1's real exposure.** If a reclaimable worker can still be running, V1 hides a live worker from the default view of a program whose job is watching workers. The hide rule is `terminal_state in HISTORICAL_STATES` only (`view.py:363-366`). It ignores the row's liveness verdict, so a row whose liveness column says it is alive would still be hidden. V2 and V3 cannot fail this way.
2. **V1 writes a final meaning into a contract note on inferred evidence.** Orca's definition is UNVERIFIED (question.md row 34). V3's point that one Orca read settles it cheaply (U-002) is correct and costs less than reverting a merged change.
3. **The "historical hidden" note lumps reclaimable workers in with released ones.** "100 historical hidden (h)" does not tell a person that 27 of them still await `release`. The header counts recover that only if the person reads both lines.
4. **`release_pending` and `release_unknown` are left open.** V1 leaves the same question open for both (Proposal A, "What stays unresolved"), so it settles one row of a larger family.
5. **V1 is not the default.** The spec's recommended and default answer is V3 (merged-requirements.md line 550). Choosing V1 costs a code change, a test and a PR slot (in OB-06 or its own PR) for the W1 wave. V3 costs none of that.

## Shared assumption responses (A-001)

**QUALIFY.** The evidence supports "a reclaimable worker has finished its task" only through the state name and Orca's next action `release` (`classify.py:479-481` treats it as releasable-but-unconfirmed). No file read shows that the worker's session has exited, so the assumption is UNVERIFIED. That is decisive for V1, which is the only variant that hides rows on the strength of it. It does not affect V2 or V3, which leave the rows visible. V1 is safe to adopt only after one Orca read (help text or a detail read of one reclaimable worker, as V3's U-002 proposes) confirms the session has exited. Short of that, the hide rule would need to exclude rows whose liveness verdict says alive, which none of the three variants proposes.

## Per-point verdicts

| Point | Superior | Reason |
|---|---|---|
| S-001 | tie | All three use the same five-section layout. |
| C-001 | V3 | Recording "historical" (V1) or "not historical" (V2) writes an unconfirmed meaning into the contract; V3 records only what is known. |
| C-002 | V1 | A person needs the screen to change, and one tuple entry at `view.py:35` using the existing `h` mechanism is the smallest change that does it; V2 and V3 change nothing visible. |
| C-003 | V1 | Only V1's default view shows working workers, and the header counts plus "N historical hidden (h)" keep the reclaimable cue on screen (`view.py:578-586`, `902-903`). |
| C-004 | V3 | A provisional row with a named way to settle it is better than a final row resting on A-001; V3 needs XC-03 to actually include the read. |
| X-001 | V1 | Yes they should be hidden, if they are finished: the count stays in the header, so the list can serve active workers. This depends on A-001. |
| X-002 | V3 | No meaning should be decided before Orca confirms it, because V1's failure mode (hiding a running worker) is the costly one. |
| X-003 | V3 | The code change is justified only after the meaning is confirmed. Not yet. |
| A-001 | V3 | Unconfirmed, and only V1 depends on it; V3 is the only variant that also plans to confirm it. |

Overall: V3
