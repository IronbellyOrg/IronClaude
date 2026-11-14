# Round 1 advocate: Variant 3 (its own state until Orca's meaning is known)

Persona: analyzer (evidence quality, logical consistency). All file:line citations below were read on 2026-11-14.

## Position summary

`reclaimable` should be recorded as its own state, shown with Orca's word, until Orca's meaning is confirmed. It is the only answer that claims no more than the evidence supports, and it is already the rule the built observer follows for any terminal state other than `released` and `retained`. Its real cost is that it does not fix the crowded default view, and it needs a named trigger to be reopened.

## Steelman

**Variant 1 (historical, hide it).** Strongest version: the default view exists to show workers that are working, and at the probe Orca reported reclaimable 27, released 41, retained 32, active 0 (ADJ line 230), so today the default view can be all finished workers. The name `reclaimable` plus the next action `release` (`classify.py:479`) points strongly at "finished, resources not yet freed". Hiding is cheap and reversible: one tuple entry at `view.py:35`, the `h` key brings rows back (`view.py:79,87`), the COUNTS strip still prints `reclaimable r` from Orca's own counts and never changes when rows are hidden (`rendering-rules.md:20,23`), and historical evidence linked to a shown item is never hidden (`rendering-rules.md:23`). Variant 1 can also point out that the observer already hides `released` and `retained` on a meaning that is itself UNVERIFIED (`unverified-register.md:61`), so "hide on an inferred meaning" is existing practice, not a new risk. It also contributes U-001: the sweep's "historical" (6 h window) and "settled" (`outcome`) differ from the observer's terminal-state meaning whatever Q23 answers (ADJ line 254, 256). That is a genuine, correct contribution.

**Variant 2 (live side, keep as built).** Strongest version: it changes nothing that works, needs no code and no test, and gives a final row now, so OB-06 cites a decided answer rather than a provisional one. Orca's own next action for these rows is `release`, which is a thing a person may need to do; the sweep already treats the pair `reclaimable`/`release` as "could not determine" rather than safe to close (`classify.py:479-481`), which is consistent with "still needs attention". Keeping such rows visible is the safe failure mode for cleanup: a person cannot miss a worker that still holds resources. And Variant 2 is honest that the row must say "awaiting release", not "running".

## Strengths claimed

1. **It is the only variant whose claim matches the evidence.** Orca's definition of `reclaimable` is UNVERIFIED in every file read (question.md fact row line 34; the `worker-list --help` filter list is recorded but "its behaviour was not run, so it is still UNVERIFIED", `unverified-register.md:58`). Variants 1 and 2 each decide a meaning from the word and from `next_action == "release"`; Variant 3 decides only what the screen and the note say, which is fully supported.
2. **It is already the built observer's rule, so "no code change" is literally true.** The observer spec says: "A row whose `terminalState` is absent or any other value is shown with its raw value ..., never hidden and never counted active" (`rendering-rules.md:23`). Code matches: `is_historical` returns true only for `HISTORICAL_STATES` (`view.py:35,363-366`). "Shown raw, not hidden, not counted active" is exactly "its own state". Variant 2 calls the same behaviour "live side", which adds a label the spec deliberately avoids.
3. **It is the default every upstream document already carries.** ADJ mapping row: "until then show Orca's word `reclaimable` and do not call it live or historical" (ADJ line 258). Merged requirements: "Its own Orca state until Q23; not automatically live, historical or settled" (merged-requirements.md line 494); invariant row "`reclaimable` is neither live nor historical until Q23" (line 1140); Q23 default "ADJ: its own state" (line 550). Picking Variant 3 writes no new text into the note: the XC-05 row already exists in draft form.
4. **It satisfies both gates without a meaning decision.** OB-06 prerequisite (e) only requires that "the `reclaimable` mapping row exists in the contract note draft (XC-05) or ... in the observer spec" (question.md line 20, merged-requirements.md line 254); it does not require the row to be final. XC-05 needs "the `reclaimable` row (Q23 default: its own state)" (question.md line 19).
5. **It separates two facts the other variants merge.** Whether a worker is still running is a liveness fact, which the observer shows per row as its own field (`liveness_verdict` is a change-key field, `view.py:40`). Whether its resources are released is the terminal-state fact. Variant 3 keeps the terminal-state word from being read as a liveness claim either way.
6. **It names a concrete way to settle the meaning (U-002 of the diff, rated High).** One help-text or one detail read of a reclaimable worker added to the shared read-only capture XC-03, which today does not list `reclaimable` (question.md line 35, merged-requirements.md line 451). That turns an inferred meaning into a recorded one before anyone hides or labels rows.
7. **Every later choice stays open at no cost.** If the capture shows "finished, safe to forget", Variant 1's one-line change follows; if it shows "still holds resources a person must release", Variant 2's wording follows. Neither is foreclosed, and nothing has to be undone.

## Weaknesses identified in other variants

1. **Variant 1 hides rows on an unconfirmed meaning, and the diff's own shared assumption (A-001) is the failure case.** No file read confirms that a reclaimable worker's session has exited. If it has not, Variant 1 hides a running worker from the default view. The mitigations are real (COUNTS strip, `h` key, `rendering-rules.md:20,23`) but they reduce, not remove, the risk: a person scanning the ledger for working agents would not see it.
2. **Variant 1's "existing practice" argument cuts the other way.** That `released`/`retained` mean historical is itself UNVERIFIED (`unverified-register.md:61`) is a reason to stop widening the hidden set until a capture is recorded, not to widen it further on weaker evidence (`released` at least names a completed release; `reclaimable` does not).
3. **Variant 1 claims "one meaning of historical in both programs", then concedes it does not hold.** Its own risk section says the sweep's "historical" is the 6 h window and "settled" comes from `outcome` (ADJ line 254, 256), so adding `reclaimable` to the observer's set does not align the programs; the note still has to label which program's meaning, as the mapping table's rule already says (ADJ line 254).
4. **Variant 1 adds a code change and a test to the built observer** for a word whose meaning was inferred; if the capture later contradicts the inference, that change and test must be reverted.
5. **Variant 2 records a decided meaning it cannot support.** "Live side" (or "not historical ... because it still awaits release") asserts that a person still has something to do. The only basis is the next-action string `release`; the observer spec records that the value set of `nextAction.kind` and whether any value means a person must act are UNVERIFIED and "never classified" (`unverified-register.md:54`). Variant 2 classifies from it.
6. **Variant 2's "live" label conflicts with the built observer's own rule**, which says other terminal states are "never counted active" (`rendering-rules.md:23`). Recording "live side" in the note invites a later reader or the XC-06 comparison test to treat 27 reclaimable rows as active, contradicting a COUNTS strip that shows `active 0`.
7. **Variant 2 makes the crowded view permanent policy.** Variant 3 leaves the same view in place but as provisional; Variant 2 ratifies it, so fixing it later reopens a "final" decision.
8. **Variant 2's citation that the behaviour was "built and merged (PRs #503, #514)"** was not checked in this round: UNVERIFIED. It does not change the argument, since the code at `view.py:35` is what matters.

## Concessions

1. Variant 3 does not fix the problem INV-023 found: with 27 reclaimable and 0 active at the probe (ADJ line 230), the default view can still be filled with finished workers. On the view's usefulness alone Variant 1 is better.
2. "Its own state" is a non-answer to "is this worker still running?". Variant 3 deflects that to the liveness field (strength 5), but a person still has to read two fields.
3. A provisional row has no owner or date for reopening. The XC-03 line is a suggestion, not a scheduled step; without one, "provisional" can become permanent by default. The answer should name who adds the capture line and in which wave.
4. Variant 3 does not address `release_pending` and `release_unknown` (`unverified-register.md:58`); Variant 1 at least raises them. The same "own state, Orca's word" rule would cover them (and `rendering-rules.md:23` already does in code terms), but Variant 3 does not say so.
5. Variant 1's U-001 is correct and should be carried into the note whichever variant wins.
6. Variant 2's "zero code, final row now" is a real advantage for OB-06 citation clarity over a provisional row.

## Shared assumption responses (A-001)

**A-001: QUALIFY.** Variant 3 does argue from the word and from `classify.py:479-481` like the others, so it shares the assumption in its framing ("the name and the next action `release` suggest a finished worker", question.md line 34). But it is the only variant whose decision does not depend on the assumption being true: it neither hides the row (Variant 1's failure if the worker is running) nor records it as needing attention (Variant 2's failure if it is safe to forget). The assumption is UNVERIFIED and should be tested by the XC-03 capture before any variant that depends on it is adopted.

## Per-point verdicts

| Point | Superior | One-line reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| C-001 | V3 | The only mapping-table meaning supported by the evidence; Orca's definition is UNVERIFIED (`unverified-register.md:58`) and ADJ line 258 already drafts this row. |
| C-002 | tie | V2 and V3 both need no code; V1 adds a change and test on an inferred meaning. |
| C-003 | V1 | On the view's usefulness alone, hiding 27 finished-looking rows when 0 are active is better, and `h` plus the COUNTS strip limit the loss (`rendering-rules.md:20,23`). |
| C-004 | V3 | Provisional is the honest status for an unconfirmed meaning; weakened by having no named reopen owner. |
| X-001 | V3 | Show by default without a meaning claim until confirmed; V1 risks hiding a running worker (A-001), V2 adds an unsupported "awaits release" claim. |
| X-002 | V3 | Deciding a meaning before Orca's definition is recorded classifies from a next-action value the spec says is never classified (`unverified-register.md:54`). |
| X-003 | tie | V2 and V3 reach the same no-change outcome; V3's "not yet" keeps V1's change available after the capture. |
| A-001 | V3 | Only variant whose outcome is correct whether or not a reclaimable worker has exited. |

Overall: V3
