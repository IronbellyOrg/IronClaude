# Round 1 advocate: Variant 2 (architect persona)

## Position summary

Answer Q21 "yes, in Phase 2, reading `worktree ps` agent rows only in the shape FU-1 records, with a stop rule if the shape carries no signal". Structurally this is the only option that adds no new input, no new dependency edge and no allow-list change to the sweep, while keeping SW-10 scheduled so the WA-07 gate keeps both of its routes.

## Steelman

**Variant 1 (watcher record).** At its strongest, V1 says: a label should rest on data written on purpose for that purpose, not on Orca's free-form fields. The watcher knows exactly what it launched (claim number, operation id, watcher worktree), so a positive match against that record makes a false "machine-started" label very unlikely (U-001), and it does not break when Orca changes what it puts in `prompt`. That concern is real: on all 27 live agent rows seen, `prompt` was empty or not a slash command (ADJ `alignment-findings-adjudicated.md:162`), and Orca's fields are not a published contract. V1 also correctly makes FU-1 run first and records the join key from a real launch rather than assuming it.

**Variant 3 (not now).** At its strongest, V3 says: do not build on a signal nobody has measured, and do not build a label the handoff design may make unnecessary. WA-07 item (3) already accepts "visible to the sweep as a labelled row (SW-10) or bound to a Run" (merged-requirements.md:309), so if SW-13 binds handed-off sessions to Runs, the sweep sees them as workers and SW-10 is dead code. V3 also keeps FU-1 item (e), so evidence is not lost, keeps W4 smaller, and the residual error (a watcher session shown as a person's) is the safe direction because person-started sessions "are never messaged" (`src/superclaude/core/WORKER-CONTRACT.md:288`, WC-16). It is the cheapest honest answer.

## Strengths claimed

1. **No new dependency edge or input.** `("worktree", "ps", "--json")` is already in the sweep's allowed Orca command list (`src/superclaude/cli/sweep/probes.py:55`) and is already called (`probes.py:1230`). SW-10 done-criterion (4) forbids a new Orca verb without a new owner signature (merged-requirements.md:199). The sweep's coupling graph stays sweep -> Orca, which it already has; no sweep -> watcher edge is created.
2. **Evidence-gated, not guess-gated.** SW-10 criterion (2) reads the rows "only in the shape FU-1 recorded (D-B)" and criterion (3) requires a test with the FU-1 fixture showing a watcher-launched session is not labelled person-started (merged-requirements.md:199). FU-1 item (e) is exactly the observation that settles D-B (merged-requirements.md:306; ADJ:493). The label is never written before the evidence exists.
3. **Explicit stop rule (U-002).** If FU-1 shows no usable signal, SW-10 records "no reliable signal" and stops (variant-2-original.md, next-step 3). That turns the risk V3 fears into a bounded, recorded outcome instead of a reason not to schedule the work, and avoids V1's coarse fallback.
4. **Keeps both WA-07 routes open.** Dependency row 74 gates WA-07 on SW-13, SW-12 and SW-10 (merged-requirements.md:721), and WA-07 item (3) allows a labelled row or a Run binding (merged-requirements.md:309). V2 schedules the label route without precluding the Run route; SW-13 can still pick either.
5. **Matches the already-adjudicated decision.** ADJ:274 records "[Decision: Q21 (yes, Phase 2, after FU-1). Waits for: FU-1. Unblocks: the label in #534. Undo: yes.]", and the spec's recommended answer is the same (merged-requirements.md:548). V2 re-litigates nothing and is reversible ("Undo: yes").
6. **Fits the existing data model with the smallest change.** `SessionRow` already carries `person_started: bool | None` (`src/superclaude/cli/sweep/models.py:152`), and `_person_origin` already returns `None` (unknown) on join problems and `True` only with the note "origin not proved" (`classify.py:748-767`). A machine-started signal from an Orca row is one more input to that same origin decision inside the same module, not a new subsystem.
7. **Error direction is the safe one.** A false negative leaves a watcher session shown as a person's; person-started sessions "are never messaged" (WORKER-CONTRACT.md:288). The design fails toward no action.

## Weaknesses identified in other variants

1. **V1 adds a cross-program contract with no version.** V1 makes the sweep read the watcher's `status --json` or state store, but the contract-note registry lists "watcher `status --json` with no `schema_version`" and governs only the first two contracts (merged-requirements.md:453). V1 trades one unversioned source (Orca fields) for another (watcher output) and adds a new coupling edge sweep -> watcher. V1 concedes this itself ("a watcher change can silently break the label").
2. **V1 widens a security-relevant list.** NFR-014 is an owner-signed allow-list; V1 requires either signing `superclaude issue-watch status --json` or approving a new file read (variant-1-original.md, next-step 3). Today the sweep code has no reference to the watcher at all (a search for `issue.watch|issue_watch` in `src/superclaude/cli/sweep/` returns nothing). That is new surface for a label.
3. **V1's join key may not exist.** The watcher "records only an Orca operation id" (merged-requirements.md:128); whether that id joins to a session is unknown (D-A). V1's fallback is worktree-path matching, which V1 itself calls coarse: any person session in the watcher worktree would be labelled machine-started. That is the unsafe error direction (a person's session mislabelled as machine's), the opposite of V2's.
4. **V1 still depends on FU-1 items (e) and (f).** It does not escape the measurement dependency V2 has; it adds a second program to it.
5. **V3 loses a WA-07 route and leaves a known misleading report.** Under V3, WA-07 item (3) must use the Run route or reopen Q21 (variant-3-original.md, costs). Meanwhile `_rule_person_active` fires on `person_started is True` plus a readable, recent transcript (`classify.py:302-315`), and `_person_origin` returns `True` with "origin not proved" when no join problem is found (`classify.py:766-767`), so the report can call a watcher session "person_active". V3 accepts that until SW-13, which is DEFERRED with no date (merged-requirements.md:128).
6. **V3 reopens a settled decision with context loss.** V3 itself notes "the person answering it then may not have this context". V2 records the decision now with a trigger, which is the cheaper long-term path.
7. **V3's "may be unnecessary" is answerable sooner.** Whether `agent launch` creates a Run is D-A, and FU-1 item (d) settles it in the same test as item (e) (merged-requirements.md:306). V2 already says that if a Run exists the label may be unneeded (variant-2-original.md, unresolved), so V2 gets V3's benefit without waiting for SW-13.

## Concessions

1. V2's signal source is Orca's free-form fields; they are not a published contract and can change between Orca builds (A-009, two builds of Orca 1.4.245 on record, as cited in variant-2-original.md; not re-checked here). V1 is right that a purpose-written record is a stronger long-term contract, if one existed and were versioned.
2. One FU-1 row may not represent every launch. The FU-1 fixture test proves the recorded shape, not all shapes.
3. V2 has a real chance of ending in "no reliable signal": 27 of 27 live rows had empty or non-slash-command `prompt` (ADJ:162). Whether `paneKey` carries anything usable is UNVERIFIED.
4. V2 waits on FU-1, which waits on Q2 and Q20; if those stay open, V2 is in practice the same as V3 (see A-001).
5. V2 adds an item to W4 that V3 does not; if the Run route is chosen later, the label work may be redundant.

## Shared assumption responses

**A-001: QUALIFY.** All three variants rely on FU-1, and FU-1 waits on other owner answers, so if FU-1 never runs V1 and V2 never start and V3 is the de facto outcome. But the dependency is asymmetric: V2 and V3 fall back to the same safe state (no label, today's behaviour), while V1 has also asked the owner to widen NFR-014 before any evidence exists. V2's stop rule also makes "FU-1 ran but found nothing" a recorded outcome rather than a stall. The assumption should be written into the #534 row's trigger ("after FU-1; if FU-1 does not run, SW-10 stays unscheduled").

## Per-point verdicts

| Point | Superior | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| C-001 | V2 | Uses an input the sweep already reads; V1's watcher record is equally unversioned (merged-requirements.md:453) and its join key is unknown (D-A). V1 would win only if FU-1 shows the Orca rows empty and the watcher id joins. |
| C-002 | tie (V2, V3) | Neither touches NFR-014; V1 needs a new owner signature on a security-relevant list. |
| C-003 | V2 | Same timing as V1 and the adjudicated decision (ADJ:274); V3 ties reopening to SW-13, which is DEFERRED with no date. |
| C-004 | tie (V1, V2) | Both keep the labelled-row route of WA-07 item (3) open alongside the Run route; V3 removes it. |
| C-005 | V2 | Records "no reliable signal" and stops; V1 falls back to coarse path matching that errs in the unsafe direction. |
| X-001 | V1 | Honest concession: a purpose-written record is a more trustworthy long-term source than Orca free-form fields, though V2's FU-1 gate and fixture test contain the risk. |
| X-002 | V2 | No new cross-program input keeps the sweep's dependency graph unchanged; V3 is equal on this but builds nothing. |
| X-003 | V2 | FU-1 item (d) settles D-A in the same test as item (e), so V2 learns whether the label is unnecessary without waiting for SW-13. |
| A-001 | V2 | QUALIFY: all depend on FU-1, but V2's stop rule and unchanged allow-list give the cleanest failure mode. |
