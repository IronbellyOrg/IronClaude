# Round 1 advocate: Variant 3 (not now; decide with the handoff design)

Persona: qa (edge cases, failure scenarios). Sources read for this round: `Q21/question.md`, the three variants, `diff-analysis.md`, ADJ (`alignment-findings-adjudicated.md`) lines 158-247, `merged-requirements.md` lines 300-311, `src/superclaude/cli/sweep/classify.py:295-319, 740-767, 872-919`, `src/superclaude/cli/sweep/probes.py` (grep), `src/superclaude/cli/sweep/models.py:152` (grep), `src/superclaude/cli/issue_watch/record.py` (grep).

## Position summary

Do not schedule the machine-started label now. Every signal the label could rest on is unmeasured (D-B, D-A), the failure the label fixes errs in the safe direction (a watcher session is never messaged as if it were a worker), and the one consumer that needs the label (WA-07) is deferred and may make it unnecessary by binding the session to a Run. Keep FU-1's item (e) so the evidence exists; write the blind spot down; reopen Q21 when SW-13's design is accepted.

## Steelman

**Variant 1 (watcher's own record).** Its strongest version: a label should rest on a record written on purpose, not on Orca's free-form fields, and a positive-match rule (label only when a watcher record matches) makes a false "machine-started" label nearly impossible. It is also better grounded than its own text says: the watcher's state store already carries a `schema_version` that is checked on read (`issue_watch/record.py:95, 227, 265`), and it stores the `operation_id` per claim (`record.py:76, 580-593`). So the versioning worry it raises about `status --json` (no `schema_version`, merged-requirements line 453) is avoidable if the sweep reads the store file instead. If the owner wants a label at all, V1's input is the more durable one. Critique: it is the most expensive answer to a question whose answer may be "not needed". It widens the owner-signed allow-list or adds a file-read path (NFR-014), creates the first runtime link between two programs that ADJ deliberately keeps unlinked ("no runtime link in version 1: neither program reads the other", ADJ Part 2.3 verdict, line 222), and its join key is unknown until FU-1: the store holds an operation id, but whether that id joins to a transcript or session is D-A, unresolved. Its own fallback, worktree-path matching, labels every session a person opens in the watcher worktree as machine-started, which is the false-positive direction it was designed to avoid.

**Variant 2 (spec's answer: Orca rows after FU-1).** Its strongest version: it changes nothing until evidence exists, uses only a command already on the allow-list (`("worktree", "ps", "--json")`, `probes.py:55`), and carries the best guard of all three: if FU-1 shows no usable signal, SW-10 "records 'no reliable signal' and stops; the label is not guessed". It also keeps the existing dependency table intact (WA-07 blocked-by lists SW-10, merged-requirements line 309). This is the cheapest "yes". Critique: the signal it reads has already failed once in the field: on all 27 live agent rows `prompt` was empty or not a slash command (ADJ line 162). FU-1 records one row from one launch on one Orca build (WA-04 item (e), (g)); a label built from one fixture is a label built on n=1, and A-009 (two builds of Orca 1.4.245) shows the field shape can move under a fixed version string, which the sweep's version check cannot detect (ADJ line 233, INV-020: it compares only the text before the first hyphen). V2's stop rule protects against "no signal"; it does not protect against "signal on one row, absent on the next build".

## Strengths claimed

1. **No code on an unmeasured signal.** D-B ("does the agent row's `prompt` hold the claim?") is open (ADJ line 493 per question.md), and the only field observation is negative: 27 of 27 live rows had `prompt` empty or not a slash command (ADJ line 162). D-A (does `agent launch` create a Run) is also open (merged-requirements line 128 per question.md). V3 is the only variant that does not commit a work item to either signal before either question is answered.
2. **The status-quo error is the safe one, and is often not even an error.** Code: `_person_origin` returns `None` (unknown), not `True`, whenever the transcript has a ccsession tab-map entry, a join problem, or an origin note (`classify.py:760-765`); only with none of those does it return `True` with `NOTE_ORIGIN_NOT_PROVED` (`classify.py:766-767`). `_rule_person_active` fires only when `person_started is True` (`classify.py:305`). So a watcher session launched through ccsession (FU-1 item (h) records its tab-map entry) is likely to land as `could not determine`, which matches ADJ's "today the sweep prints `could not determine`" (ADJ line 242). Where it does land as person-active, it is never messaged (WC-16, cited by V2 and V3). The harm V1 and V2 fix is a misleading label in a report, not a wrong action.
3. **The only consumer is deferred and has an alternative route.** WA-07 item (3) reads "visible to the sweep as a labelled row (SW-10) or bound to a Run" (merged-requirements line 309). If SW-13 chooses Run binding, the session becomes an Orca row and the sweep already builds it with `person_started=False` from the Orca side (`classify.py:878-884`), so the label work would be wasted.
4. **No change to the security-relevant allow-list and no new cross-program link.** Matches ADJ's version-1 rule that neither program reads the other (ADJ line 222) and keeps NFR-014 untouched; V1 cannot say this, and V2 can only because it reuses a verb.
5. **Evidence is still collected.** V3 keeps FU-1 item (e) (step 3), so reopening Q21 starts from a recorded row, not from scratch. Nothing is lost by waiting except the label itself.
6. **Honest documentation of the blind spot now.** It carries ADJ's sentence "Run-less sessions (watcher-launched, person-started) not observable by either program today" (ADJ line 227) plus one sentence that the sweep may show a watcher session as a person's. That addresses the "reader is misled" risk at the cost of one sentence instead of a work item.

## Weaknesses identified in other variants

1. **V2, n=1 fixture.** SW-10's done-when needs "a test with the FU-1 fixture" (question.md, SW-10). One fixture proves the parser reads that row; it says nothing about the 27 rows that had no usable `prompt` (ADJ line 162). Failure scenario: FU-1's row happens to hold `/sc:issue --claim N`, SW-10 ships, a later launch or Orca build empties `prompt`, and the label silently falls back to person-started with no test failing.
2. **V2, build drift is undetectable.** The sweep's version check compares only the text before the first hyphen (ADJ line 233, INV-020), and A-009 records two builds under one version. A label keyed on free-form fields has no tripwire.
3. **V2, `paneKey` may overlap the existing join.** The sweep already joins transcripts by tab map (`classify.py:872-874`; `_person_origin` uses `has_entry`). Whether `paneKey` adds information beyond the tab-map join is not shown in V2. UNVERIFIED either way.
4. **V1, coarse fallback inverts its own safety claim.** V1 states a false "machine-started" label is unlikely because it needs a positive match; but if the operation id cannot be joined (D-A), it falls back to worktree-path matching, under which "any session a person opens in the watcher worktree would be labelled machine-started" (V1, costs). That is the dangerous error direction: a person's session labelled machine-started could later be treated differently by the course-correction design (ADJ line 714, per V2; not read this round).
5. **V1, first runtime link between programs.** It breaks ADJ Part 2.3's "no runtime link in version 1" (ADJ line 222) and needs an owner signature on a security-relevant list (NFR-014), for a label whose consumer is deferred.
6. **V1 and V2, both silent on the case where SW-13 binds to a Run.** Neither says what happens to a built label if the handoff design makes the session an Orca row; the label becomes dead code with a test to maintain.
7. **V1, A-001 unstated.** FU-1 waits on Q2 and Q20 (V2 states this; diff-analysis A-001 notes V1 does not), so V1's timeline is understated.

## Concessions

1. **WA-07's dependency table must change under V3.** WA-07's blocked-by column lists SW-10 explicitly (merged-requirements line 309; row 74 at line 721 per question.md). V3's "WA-07 loses one route" understates this: picking V3 requires editing the dependency table so WA-07 is blocked by "SW-10 or a Run-binding decision", otherwise WA-07 is blocked on an unscheduled item. V3 does not say this.
2. **The question comes back.** The person answering it later may lack this context (V3 states this). V2 resolves it once.
3. **V2's stop rule already gives most of V3's safety.** If FU-1 shows no signal, V2 ends exactly where V3 starts. V3's extra value is only in the case where FU-1 shows a signal on one row that is not durable, plus avoiding work that SW-13 may make unnecessary.
4. **The misleading-report risk is real, not hypothetical.** `_person_origin` can return `True` for a Run-less transcript with no tab-map entry and no join problem (`classify.py:766-767`); a reader can then see a watcher session reported as a person's active session. V3 answers this with a document sentence, which a report reader may never see.
5. **V1's input is more durable than V3 credits.** The watcher store has a checked `schema_version` (`record.py:227`), so V1's versioning risk is smaller if it reads the store, not `status --json`.
6. **The "safe direction" argument depends on WC-16 being enforced.** I did not read WC-16's enforcement in this round; UNVERIFIED beyond the citations in V2 and V3.

## Shared assumption responses (A-001)

**A-001: QUALIFY.** All three variants do depend on FU-1 running and recording items (e) and (f), but the dependency is not symmetric. V1 and V2 cannot start without it (WA-04 blocks SW-10, merged-requirements line 306); V3 only uses it as optional evidence for a later reopen, so if FU-1 never runs V3's outcome is unchanged and the owner loses nothing. Also, "FU-1 records item (e)" is one row from one launch on one build (WA-04 (e), (g)); the assumption should read "FU-1 produces one sample", not "FU-1 settles D-B", because one sample cannot show a field is reliably populated.

## Per-point verdicts

| point | superior | one-line reason |
|---|---|---|
| S-001 | tie | Same five-section layout in all three. |
| C-001 | V3 | No label on a signal that failed on 27 of 27 live rows (ADJ line 162); if a label is wanted later, V1's input beats V2's. |
| C-002 | tie (V2, V3) | Neither touches NFR-014; V2 reuses `worktree ps --json` (`probes.py:55`), V3 adds nothing; V1 must widen the list. |
| C-003 | V2 | V2 has a concrete trigger (FU-1 recorded, #539 merged); V3's "SW-13 accepted" trigger is far off and leaves the question to a later reader. |
| C-004 | V2 | V2 keeps WA-07's dependency table valid (blocked-by SW-10, line 309); V3 requires a table edit it does not state. |
| C-005 | V2 | V2's explicit "no reliable signal, stop" rule is the best failure handling; V1's fallback inverts its safety; V3 has nothing to fail. |
| X-001 | V3 | One FU-1 row cannot establish that a free-form field is trustworthy; V3 is the only variant that does not act on n=1. |
| X-002 | tie (V2, V3) | Adding a cross-program input breaks ADJ's version-1 "neither reads the other" (line 222) for a deferred consumer; V2 and V3 both avoid it, V1 loses. |
| X-003 | V3 | WA-07 item (3) already allows "bound to a Run", and an Orca-bound row is built with `person_started=False` (`classify.py:884`), so the label may be unnecessary. |
| A-001 | V3 | Only V3's outcome survives FU-1 never running; V1 and V2 stall. |
