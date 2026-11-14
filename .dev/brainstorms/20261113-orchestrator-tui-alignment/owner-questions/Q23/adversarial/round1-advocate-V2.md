# Round 1 advocate: Variant 2 (live side, as built)

Persona: backend (data integrity, fault tolerance). Evidence read on 2026-11-14 in the worktree `issue-339-orchestrator-mode`, read-only.

## Position summary

`reclaimable` belongs on the not-historical side and stays in the observer's default view, labelled "awaiting release" and not "running". The deciding facts are Orca fields the observer already parses: in the redacted live fixture, every reclaimable worker has finished its task, but its resources are still owned and their release has not been requested. Hiding that state would hide resources that are still held. The decision needs no code change. I amend my variant's title: "live side" overstates it, and the row should say "not historical: awaiting release".

## Steelman

**Variant 1 (historical, hide it).** The strongest form: the observer's default view is for "what is working now", and at the probe Orca reported 27 reclaimable workers and 0 active (question.md line 30; INV-023). So today a person opening the observer sees only finished workers. Orca's own data supports V1's inference more strongly than V1 claims. In `src/superclaude/cli/observe/fixtures/golden-success.json` (described in the file as "one redacted live worker-list read"), all 9 reclaimable rows have `workerState: succeeded`, `dispatchStatus: completed` and `projection.outcome: succeeded`. Hiding the rows also does not erase them completely: the COUNTS strip always shows `source counts: active a / reclaimable r / ...` and is "never dropped" (`.dev/issues/409/bmad/ux-orca-observer/EXPERIENCE.md:116`), and the view prints "`N historical hidden (h)`" (`view.py:902-904`). The change is small and testable. V1 also contributes U-001: whatever Q23 answers, the sweep's "historical" (its 6 h window) and "settled" (from `outcome`) still differ from the observer's terminal-state meaning. That is true and the note must say it.

**Variant 3 (its own state, until the meaning is known).** The strongest form: V3 is the spec's default and the row ADJ already drafted (ADJ line 258: "until then show Orca's word `reclaimable` and do not call it live or historical"; line 793). It needs no code change and claims no meaning beyond the evidence. It names a concrete way to settle the question: add one help-text read or one detail read of a reclaimable worker to the shared capture XC-03 (U-002). It also keeps both later choices open at no cost. Its runtime behaviour is identical to mine.

## Strengths claimed

1. **The decision rests on observed fields, not on a guessed definition.** The observer already parses `release_state` from `resource.releaseState` (`parse.py:67`) and the liveness verdict from `projection.liveness.verdict` (`parse.py:84`). In the redacted live fixture, all 9 reclaimable rows read: `nextAction.kind: release`, `resource.releaseState: not_requested`, `resource.ownershipState: owned`, `liveness.verdict: unverifiable`. "Awaiting release" describes exactly those values. Orca's prose definition is still UNVERIFIED. The fact that resources are held and their release was not requested is visible in the data.
2. **Data integrity: hiding held resources hides a possible leak.** By resource lifecycle, `reclaimable` is the one state where Orca still owns a resource (`ownershipState: owned`, not `user_owned`) and no release has started. Every `released` row in the fixture has `releaseState: released`. Moving reclaimable into the hidden set would put "resource still held, release not requested" behind the same `h` key as "resource gone". The `N historical hidden (h)` note would then add reclaimable rows to the 326 released rows in one number (fixture counts: reclaimable 11, retained 91, released 326).
3. **The terminal state describes the resource's lifecycle, not whether the worker is alive.** In the same fixture, 2 `retained` rows have `workerState: ready`, `outcome: in_progress` and `liveness.verdict: live`. Because `HISTORICAL_STATES = ("released", "retained")` (`view.py:35`, `is_historical` at `view.py:363-366`), the observer already hides those live workers by default. That is a separate problem outside Q23 and should be logged. But it shows that "terminal state equals finished" is already wrong once, and V1 would extend that rule.
4. **Zero code change, matching what was merged and tested.** `HISTORICAL_STATES` stays as it is (`view.py:35`). The default view keeps reclaimable rows (`view.py:844-849`). The row already shows Orca's word, because `terminal_state=text_of(row.terminal_state)` (`view.py:452`), and it shows liveness in its own column (`view.py:455`). The screen therefore never says "running" for these rows: the reader sees `reclaimable` together with `unverifiable`.
5. **Consistent with the sweep.** `safe_to_close` gives "could not determine" with reason "result read not observable" for `state == "reclaimable" and action == "release"` (`classify.py:479-481`). That is a "still needs a look" answer, not "done and forgettable". Leaving the state visible in the observer matches the sweep's caution.
6. **A final row for OB-06.** Prerequisite (e) needs a mapping row (question.md lines 19-20). A row with a reason ("awaiting release: release not requested") is final and gives a reader something to act on.

## Weaknesses identified in other variants

1. **V1 hides a state whose resources are still held.** Evidence: strength 2. The count in the COUNTS strip survives, but it does not say which worker holds which worktree (`resource.worktreeId` such as `wt-012` in the fixture row `w-031`). The per-row cleanup cue would sit behind `h`.
2. **V1 extends a rule that is already wrong once.** It adds `reclaimable` to a hide-by-terminal-state set that already hides live `retained` workers (strength 3). V1 also changes merged, tested observer code (C-002) on the basis of the state's name, which its own risk section calls "inferred" (variant-1 line 23).
3. **V1's main metric is a view-layout problem, not a meaning problem.** The probe figure "27 reclaimable, 0 active" argues for a separate group or a different sort order, not for calling held resources historical. V2 leaves that as an open follow-up ("a separate 'awaiting release' group", variant-2 line 29).
4. **V3 overstates what is unknown.** It says the meaning is "UNVERIFIED in every file read" (variant-3 line 16). That is true of Orca's prose definition, but the fields that decide visibility are parsed and present: release state, ownership state, outcome and liveness (strength 1). "Its own state" gives a reader who asks "do I need to do anything?" no answer, and V3 concedes this (variant-3 line 23).
5. **V3's provisional row may never be revisited.** V3 concedes it "can stay provisional indefinitely" without a trigger (variant-3 line 24). XC-03 is planned but has not been run, and it does not yet list `reclaimable` (question.md line 35). The trigger depends on a capture whose scope has not been amended.

## Concessions

- My variant's title and the word "live" are wrong. Every reclaimable row in the fixture has `workerState: succeeded`, and its liveness verdict is `unverifiable`. The row must say "not historical: awaiting release", never "live" or "running".
- V2 does not fix the noise problem. The default view can still be filled with finished workers (27 reclaimable, 0 active, INV-023).
- It is UNVERIFIED whether a person performs `release` or Orca reclaims the resources automatically. If Orca reclaims them on its own, the cleanup cue is not meant for a person, and V1's case gets stronger.
- The fixture evidence comes from one redacted read. I take its provenance from the file's own `description` string; no capture log was read. `ownershipState: owned` meaning "owned by Orca" is my reading of it next to `user_owned`, UNVERIFIED.
- V3's reopen trigger (U-002) is better than anything V2 offers. V2 should adopt it: add one reclaimable detail read and the help text to XC-03.
- V1's U-001 is correct and belongs in the note whatever the answer is.

## Shared assumption responses (A-001)

**QUALIFY.** In the redacted live fixture, the worker's task has finished: all 9 reclaimable rows have `workerState: succeeded`, `dispatchStatus: completed` and `outcome: succeeded`. But the session's exit is not confirmed: `liveness.verdict` is `unverifiable` for every one of them, and the evidence is a single redacted read. Because the session may still exist, the safe course is to keep the rows visible, which V2 and V3 both do. V1 is the only variant that would hide a worker if one turned out to be alive.

## Per-point verdicts

| Point | Superior | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| C-001 | V2 | "Awaiting release" matches the parsed fields (`releaseState: not_requested`, `ownershipState: owned`, `nextAction: release`); "historical" contradicts held resources, and "its own state" says nothing a reader can act on. |
| C-002 | tie | V2 and V3 both need no change to tested, merged code; V1 changes code on an inferred meaning. |
| C-003 | tie | V2 and V3 render the same thing (Orca's word at `view.py:452`, liveness at `view.py:455`); V1 hides rows whose resources are still held. |
| C-004 | V3 | V3's explicit reopen trigger through XC-03 is better than V2's unconditional finality. |
| X-001 | V2 | A per-row cleanup cue for held resources outweighs the noise in the default view; the noise belongs to a layout fix, not to the meaning. |
| X-002 | V2 | The visibility decision can rest on observed fields now; only Orca's prose definition is missing, and V3 treats that gap as larger than it is. |
| X-003 | tie | V2 and V3 both decline a code change. |
| A-001 | tie | V2 and V3 both keep possibly-live rows visible; V1 alone carries the risk. |

Overall: V2 (with V3's XC-03 reopen trigger adopted as an amendment)
