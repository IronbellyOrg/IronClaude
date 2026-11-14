# Round 1 advocate statement: Variant 2 (proposal B, keep both, one written contract note)

Persona: architect (structure, dependencies, long-term impact). Mode A, depth quick, Round 1 only.

## Position summary

Variant 2 is the only option that fixes the drift that exists today (two "v1" files, three vocabularies, two allow-lists that disagree on `check`) without adding a runtime dependency between two programs that were built independently. It is also the base that Variant 1's panel would need anyway. Its draft can start now on a master-based branch; only its landing waits for PR #539.

## Steelman

### Variant 1 (observer panel reads a captured copy of the sweep JSON, plus a note)

Strongest version: the person who will read these screens should see one classification of each session, not two. The live #409 body says so: "If the observer built its own collector, two programs would classify the same session and could disagree. Reading the sweep's output keeps one definition of 'waiting on a person' or 'stalled'" (`gh issue view 409`, read 2026-11-14). Variant 1 gets this without breaking the sweep's one-report-per-run rule: it captures stdout the coordinator's WC-16 pass already prints (U-001), which is the "alternative kept open" in ADJ Part 8 (line 806). It still writes the note, and it waits for XC-04 before joining rows. It honestly lists its own costs, including the three verdicts it reverses. Of the three, it is the only one that would reduce disagreement on screen rather than just record it.

Critique:
1. The #409 premise is already past. "If the observer built its own collector" has happened: the observer is merged (PRs #503, #514) and reads Orca only (ADJ E-03, line 129, 95 percent). A panel does not remove the second classifier; it adds a third view on the same screen, next to the observer's own Orca rows. Variant 1 admits this in "What stays unresolved": "which wins on screen".
2. It creates a dependency that runs the wrong way for version 1. The observer gains a reader of a file whose producer exists only when a coordinator runs the sweep (Variant 1, costs bullet 2). That is a time-based coupling with no liveness signal. The note design already says the snapshot has "no pid, no liveness flag" and needs an age rule (ADJ line 228). Variant 1 would add a second file with the same problem.
3. The data does not join cleanly yet. The snapshot's 15 row keys "carry no command, objective, branch, changed paths or issue or PR" (ADJ line 808), and the join basis has "not [been] compared on real ids" (ADJ line 229). The panel is built on the one fact the debate could not establish (A-003).
4. It forces two later questions early. It needs Q9 = caller-side capture and Q17 = "yes, later". The spec recommends "not now" for both (`merged-requirements.md:536`, `:544`), and ADJ rejected an observer reader of the sweep JSON at 95 percent (X-013, line 808).

### Variant 3 (keep both, write nothing yet, decide after #539 merges and XC-04 runs)

Strongest version: do not write a contract against code that is still moving. PR #539 has two unresolved review threads and an open security ruling (ADJ E-08, line 134; Q1), so the sweep's verbs and constants could change before merge. The one fact that decides the relationship (whether `dispatchId` equals the part of `row_id` after `orca:` on a real Run) is not yet known. Waiting saves a note, a test and a link PR if the owner later prefers a panel or a merge. The explicit re-ask trigger (U-003) is good process.

Critique:
1. It contradicts itself (X-002). Its own costs say the draft "could have been written now on a master-based branch at low cost; only its landing waits for #539". That is Variant 2's timing.
2. It delays the one agreed result. ADJ calls the note "the main product of the debate" and says three other texts depend on it (Part 2.3, line 222). Variant 3 makes those texts use plain descriptions now and be reworded later. That is two writes instead of one.
3. Waiting does not stop drift. The confusion it leaves in place (Variant 3, costs bullet 1) is the confusion ADJ Part 1.1 (line 111) names as the gap: "aligned in intent and not yet in practice ... no written contract between them".
4. A merge is not a live alternative to wait for. All five reviews rejected it (ADJ line 807; diff-analysis A-004). So the "wasted note" risk in X-003 only applies if a panel is chosen later, and Variant 1 itself keeps the note in that case.

## Strengths claimed

1. **No new runtime coupling.** "Neither program reads the other and neither gains a file or key" (Variant 2, Answer). This is the ADJ verdict word for word (line 222). The two programs keep their own design rules (stdlib-only models, owner-signed exact allow-list NFR-014; ADJ line 807).
2. **The base for any later choice.** The note is the registry of contracts, units, versioning rule ("consumers ignore unknown keys"), mapping table and verb lists (ADJ lines 224-231). A later panel (Q17) would need exactly this. Variant 1 writes the note too. So Variant 2 is the shared first step of both "yes" answers, and the panel can still be added later.
3. **A mechanical check for drift (U-002).** XC-06 fails when either program changes a shared word, verb, schema version or join basis without updating the note. ADJ says the amendment rule "needs a test" and "today no test reads any design document (INV-042)" (line 225). Neither other variant adds a guard like this.
4. **Correct timing.** Draft now on a master-based branch (ADJ line 224: this checkout is PR #539's head, so a note committed here would join the PR). Land after #539 and XC-04. This matches weak point W4: "only the draft (XC-05) can run early" (`merged-requirements.md:508`).
5. **No overclaiming.** It keeps the words "candidate join basis", not "join key", until XC-04 (Variant 2 step 1; ADJ line 229; `merged-requirements.md:500` "Premature 'join key'").
6. **Smallest change, easy to undo.** No program code changes, and NFR-001 stays as it is. Both PRs revert cleanly (ADJ line 806 for NFR-001; `merged-requirements.md:503` for reversibility).
7. **Honest about its limits (U-004).** It states that the test compares constants, not behaviour ("stale" 45 s against 6 h), which is `merged-requirements.md:1160`.

## Weaknesses identified in other variants

1. Variant 1: it reverses X-013 (95 percent), X-017 (70 percent) and the recommended answers to Q9 and Q17 (ADJ lines 806, 808; `merged-requirements.md:536,544`), on the authority of an issue body whose premise has been overtaken by the built observer (E-03).
2. Variant 1: it adds a third artefact (the captured JSON) with an owner, path and age rule still open (its "What stays unresolved": "Who runs the capture and where the file lives (Q9)"). It also adds a new untrusted-input path in the observer (Variant 1, costs bullet 4; ADJ line 228 already names two sanitizers).
3. Variant 1: the capture depends on a coordinator running the sweep. On a host with no coordinator the panel is empty (Variant 1, costs bullet 2). An orchestrator that manages work is not built, so the panel depends on a step outside both programs. Where the WC-16 capture change would be made is UNVERIFIED.
4. Variant 3: it is internally strained (X-002, as above). It also leaves no written rule for changes to either program during the gap, while #539 is still under review and the observer may change separately.
5. Variant 3: rewording three texts later (Coder#477 status record, v2 field list, #409 mapping table) costs more than drafting the note once against the current constants.

## Concessions

1. Variant 2 does not remove the disagreement the person may see. It documents it (Variant 2, costs bullet 1). If the owner's priority is one classification on screen, only Variant 1 aims at that.
2. The XC-06 test can pass while meanings differ (`merged-requirements.md:1160`). The mapping table's "Rule" column must carry the meaning. The test only guards the words.
3. The draft is written against a moving target. If the Q1 ruling or the two unresolved #539 threads change sweep constants, the draft has to be revised before landing. Whether Q1's fix touches `ALLOWED_ORCA` or the report constants is UNVERIFIED.
4. Variant 3's explicit re-ask trigger (U-003) is a good idea. Variant 2 should take it: re-ask Q17 once XC-04 is recorded.
5. Variant 2 sets aside the live #409 proposal for version 1. That needs an owner decision, and the #409 body itself says it does.

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 (#539 merges in roughly its current shape) | QUALIFY | All three depend on it. Variant 2 depends on it least: the draft, the observer half of the note and the mapping table do not wait for it. But the XC-06 test compares against `ALLOWED_ORCA` and the report constants, which exist only on #539's head (`merged-requirements.md:508`). If #539 stalls, the sweep half of the note describes unmerged code and cannot land. Variant 1 stalls entirely. Variant 3 waits forever unless the trigger gets a fallback date. |
| A-002 (the person reads both views) | QUALIFY | The note is not only for the person. Agents and three planned texts cite it (ADJ line 222), so the note is worth writing even if the person reads only one view. The panel's gain depends on A-002 holding; Variant 1 is the option that rests on it. Q11 shows the person may read only the sweep summary for now (`merged-requirements.md:538`). |
| A-003 (the real-id comparison XC-04 can run) | QUALIFY | It needs the Q1 ruling, a runnable sweep on this host (Q29), reachable Orca and a named runner (Q24). If it never runs, Variant 2 still lands with "candidate join basis" wording and loses nothing. Variant 1's panel has no reliable join. Variant 3 never re-asks. Variant 2 is the variant least exposed to this risk. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | tie (V1 = V2 = V3) | 50 | The sections are identical by design of the brief, so there is nothing to choose. |
| C-001 | V2 (V3 equal on this point) | 80 | No runtime link in v1 is the ADJ verdict (line 222). The snapshot cannot join the sweep's data yet (line 808). |
| C-002 | V2 | 85 | Draft now, land after #539. W4 allows only the draft early (`merged-requirements.md:508`). Deferring wastes the agreed main product. |
| C-003 | V2 (V3 equal) | 75 | Q9 and Q17 are recommended "not now". Variant 1 forces both early (`:536`, `:544`). |
| C-004 | V2 | 80 | The draft can run early; landing waits for #539 and XC-04. This matches W4 exactly. |
| C-005 | V2 | 65 | The #409 premise ("if the observer built its own collector") is already true (E-03). Setting the proposal aside for v1 and keeping it open as Q17 is the honest treatment. V1 has a real point about one definition on screen. |
| C-006 | V2 | 65 | V3 changes nothing but also guards nothing. V2's one test is the least change that detects drift. V1 changes the observer and a coordinator step. |
| X-001 | V2 | 70 | Two classifiers already exist. A documented difference is achievable now; one definition on screen needs the unverified join and a coordinator capture. |
| X-002 | V2 | 85 | V3's own costs concede the draft is cheap now. |
| X-003 | V2 | 75 | V1 keeps the note in every case, so the note is not wasted. Merge is rejected (A-004). |
| A-001 | V2 | 70 | Least exposed to a #539 stall, but not immune: the test needs #539 constants. |
| A-002 | V2 | 65 | The note has readers besides the person. The panel's value depends on A-002. |
| A-003 | V2 | 75 | "Candidate join basis" wording survives a failed or unrun XC-04. The panel does not. |

## Overall

As a neutral judge, I would recommend Variant 2 to the owner at 75 percent confidence, with two additions taken from the other variants: Variant 3's explicit trigger to re-ask Q17 after XC-04 is recorded, and Variant 1's caller-side capture (U-001) noted in the contract as the approved path if Q17 later becomes "yes". Variant 1 would be the better pick only if the owner says that one classification on screen matters more in version 1 than keeping the programs independent. That is an owner preference the sources cannot settle.
