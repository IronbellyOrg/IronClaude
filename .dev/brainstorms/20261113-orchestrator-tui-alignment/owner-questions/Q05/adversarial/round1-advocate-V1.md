# Round 1 advocate statement: Variant 1 (proposal A, observer panel on a captured copy of the sweep JSON, plus a note)

Persona: frontend (what the person sees on screen, and whether it is consistent). Depth quick, Round 1 only.
Sources read: `../question.md`, the three variants, `diff-analysis.md`, ADJ (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`) lines 105-134, 214-229, 320-365, 798-811, `merged-requirements.md` lines 506-510, 530-544, 1158-1162, and the #409 body (`gh issue view 409 --repo IronbellyOrg/IronClaude`, read-only, `updatedAt` 2026-11-13T16:57:51Z).

## Position summary

Variant 1 is the only answer that puts one classification of a session in front of the person, which is what the live #409 body still asks for. It is the right long-term screen, but the evidence says it is premature for version 1: the sweep JSON is stdout-only, the join key is unverified, and the panel would mix data of very different ages on one screen. I argue its strengths honestly and, as a neutral judge, recommend Variant 2 for now, with Variant 1 kept as the named later path behind Q17.

## Steelman

**Variant 2 (one note, no runtime link).** Its strongest form: the debate's single agreed outcome, "one short written note, no runtime link in version 1 ... the main product of the debate" (ADJ line 222), done with zero code change in either program, a test (XC-06) that fails when a shared word, verb or schema version drifts, and a draft that can start now on a master-based branch (ADJ line 224, INV-031). It honestly names its own limit: identical words can mean different things ("stale" 45 s against 6 h, `merged-requirements.md:1160`). It is the base every later choice, including my panel, would need anyway.

**Variant 3 (write nothing yet).** Its strongest form: PR #539 is open with two unresolved review threads and a HIGH invariant (INV-008) not waived (ADJ lines 113, 134), so the sweep's constants, verbs and wording may still change; and the one fact the debate could not establish, whether the observer's `dispatchId` equals the part of the sweep's `row_id` after `orca:` on real ids (ADJ line 229, "not compared on real ids (D-3)"), decides whether any join is possible. Deciding after that evidence avoids writing, testing and linking a document that might be rewritten.

## Strengths claimed

1. **One definition on the person's screen.** The #409 body, line 55: "If the observer built its own collector, two programs would classify the same session and could disagree. Reading the sweep's output keeps one definition of 'waiting on a person' or 'stalled'". Only Variant 1 acts on that; Variants 2 and 3 leave it as "set aside" or "deferred" (diff C-005).
2. **It fills cells the screen already shows as empty.** The built observer marks report status, acceptance, tests, approval, settled and policy-frozen as `unavailable (no source)` (ADJ E-06, line 132, `view.py:96,412`). A panel fed by a classifier is the only proposal that could ever replace some of those cells. Which of those cells the sweep JSON can actually fill is UNVERIFIED; Variant 1's own list ("frozen plans, safe-to-close, contract questions") is not checked against the sweep's row keys in any source I read.
3. **It does not break the sweep's one-report rule.** It reads a copy captured by the caller in the coordinator's WC-16 pass, never runs the sweep (U-001). This is exactly the "alternative kept open: caller-side stdout capture inside the WC-16 pass" in ADJ Part 8 (line 806), and it avoids the rejected "observer starts the sweep" path that would write a report and run `git status` in every worktree each time (line 808).
4. **It keeps the note.** Variant 1 still drafts XC-05, adding the captured file as a third registered artefact (variant-1 step 2), so it does not lose Variant 2's main benefit.
5. **It is sequenced behind the evidence.** The panel waits for #539 to merge and for XC-04 (variant-1 step 3), the same trigger Variant 3 uses.

## Weaknesses identified in other variants

1. **Variant 2 leaves two screens that can disagree.** Its own costs say so: "The person still sees two views that can classify the same session differently; the note documents the difference, it does not remove it" (variant-2 line 22). A note is read by developers, not by the person looking at the screen.
2. **Variant 2's test protects words, not meaning.** `merged-requirements.md:1160`: "the test compares constants, not behaviour ... 'stale' 45 s vs 6 h". Nothing in Variant 2 checks what the person actually sees.
3. **Variant 2 leaves the #409 body contradicting the outcome.** The live body still proposes one shared set of facts (line 55). Choosing Variant 2 needs a matching #409 edit, which Variant 2 does not list. (Variant 1 needs no such reversal of #409; it needs reversals of three debate verdicts instead, see Concessions.)
4. **Variant 3 contradicts itself.** It refuses to write against "a moving target" (variant-3 line 15) yet concedes the draft "could have been written now on a master-based branch at low cost" (line 24); diff X-002 flags this strain.
5. **Variant 3 delays the one agreed product and breaks three dependent texts** (Coder#477 status record, v2 field list, #409 mapping table; ADJ line 222), which must be reworded later (variant-3 line 22).
6. **Variant 3's trigger may never fire.** It waits on #539 and XC-04; XC-04 depends on Q1, Q29, Q24 and live Orca (diff A-003). No fallback date is given.

## Concessions

1. **The panel reverses three debate verdicts for version 1:** X-013 (95 percent, "no runtime link in version 1", ADJ line 325), X-017 (70 percent, line 360) and A-001 (78 percent, "Q17: no observer panel for sweep facts now", line 361). Variant 1 says so itself (variant-1 line 21).
2. **Mixed freshness on one screen.** The observer polls every 15 s and calls a snapshot stale after 45 s (ADJ X-011, line 330); the sweep runs at most once per 5 minutes under WC-16 (E-04, line 130). A panel row would nearly always be older than the observer's own stale threshold, beside rows that are seconds old. That is an on-screen inconsistency my variant creates, not removes.
3. **The panel can contradict the row next to it.** "Whether the observer's own Orca view and the sweep's view disagree for the same worker, and which wins on screen" is unresolved (variant-1 line 29). Today the disagreement is between two programs the person may not view together; the panel would put it side by side.
4. **Empty panel without a coordinator.** The captured file exists only when a coordinator runs the WC-16 pass (variant-1 line 22).
5. **No verified join.** The structural join basis is verified but "not compared on real ids (D-3)" (ADJ line 229); duplicate-flagged and empty rows must be excluded (`NOTE_DUPLICATE_DISPATCH`, INV-028).
6. **More attack surface and tests.** A new file and a new reader of untrusted strings, with two different sanitizers already in play (ADJ line 228).
7. **In version 1 there is no on-screen disagreement to fix.** The built observer prints Orca's words and none of the ten dimension names (E-06). The sweep's classes do not appear on the observer screen at all, so the "two definitions on screen" problem my variant solves is not yet visible to the person. This weakens Strength 1 for version 1 specifically.

## Shared assumption responses

| id | Response | Reason |
|---|---|---|
| A-001 (#539 merges in roughly its current shape) | QUALIFY | Not safe: #539 is open with two unresolved threads and INV-008 (HIGH, not waived) blocks the merge (ADJ lines 113, 134, 344). Variant 1 is the most exposed (panel, capture and join all wait on it); Variant 2 is least exposed because its draft can be written on a master-based branch now, though even its test needs `ALLOWED_ORCA` and report constants that exist only on #539's head (`merged-requirements.md:508`, W4). |
| A-002 (the person reads both views) | QUALIFY | Unmeasured in any source I read (UNVERIFIED). I dispute the diff-analysis inference that the panel's gain shrinks if the person reads only one view: if the person reads only the observer, the panel is the only way the sweep's proof-based classes ever reach them, so the gain grows; what shrinks is the cost of disagreement. Either way the assumption should be checked with the owner, not assumed. |
| A-003 (the real-id comparison XC-04 can run) | QUALIFY | It needs the Q1 ruling applied, a runnable sweep on this host (Q29), reachable Orca and a named runner (Q24) (diff A-003). Variant 1 depends on it hardest (a panel without a join cannot place sweep facts against observer rows); Variant 2 survives a failed or absent comparison by keeping the words "candidate join basis" (variant-2 step 1); Variant 3 waits on it with no fallback. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | none (identical) | 95 | All three use the same five sections by design of the brief. |
| C-001 | V2 | 75 | No runtime link in v1: the sweep JSON is stdout-only, the join is unverified, and the panel would mix 15 s and 5-minute data on one screen (X-013 95%). |
| C-002 | V2 | 80 | Draft now on a master-based branch, land after #539 (INV-031, W4); V1's third-artefact registration can be added later. |
| C-003 | V2 | 70 | Q9 and Q17 "not now" match the debate (ADJ line 806, line 361); V1's caller-side capture stays a valid later option. |
| C-004 | V2 | 75 | Only V2 does useful work before #539 merges without depending on its outcome. |
| C-005 | V2 | 60 | Setting #409's proposal aside for v1 with a recorded reason is honest; but V1 is right that the #409 body must then be corrected, which V2 omits. |
| C-006 | V2 | 75 | No program change in v1; V1 adds a reader, a file and a capture step to two programs. |
| X-001 | V2 | 65 | For v1 the disagreement is not on the person's screen (observer shows no sweep classes, E-06), so documenting it is enough; V1's concern becomes real once Q17 is "yes". |
| X-002 | V2 | 85 | Writing the draft early is cheap and V3 concedes it; V3 is internally strained. |
| X-003 | V2 | 75 | The note is the base for any later panel or merge; V1 agrees it is still needed, V3's "possibly wasted" is not supported. |
| A-001 | V2 | 70 | Its master-based draft is the only step that survives a stalled #539. |
| A-002 | V1 | 55 | Only V1 addresses what reaches the person if they read one screen; weak, because how the person reads is unmeasured. |
| A-003 | V2 | 80 | "Candidate join basis" wording survives a failed or absent comparison; V1 needs the join, V3 waits on it. |

## Overall

If I were neutral I would recommend **Variant 2** to the owner, confidence **75 percent**: keep both programs, draft the note now on a master-based branch, land it with its test after #539 merges and XC-04 runs, and record Variant 1's panel (fed by caller-side capture in the WC-16 pass, never by running the sweep) as the named path if the owner later answers Q17 "yes". Two additions from Variant 1 should ride on Variant 2: correct the #409 body's "one shared set of facts" proposal so it does not contradict the choice, and have the note's mapping table state each program's stale threshold so the person-facing meaning of "stale" is written down.
