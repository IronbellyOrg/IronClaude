# Round 1 advocate statement: Variant 3 (Proposal C, "keep both, write nothing yet, decide after #539 merges and XC-04")

Persona: analyzer (evidence quality and logical consistency). Depth quick, Round 1 only.

## Position summary

Variant 3 is right that the owner's answer should stay provisional until PR #539 merges and the real-id comparison (XC-04) runs, because the "keep both" verdict is the debate's weakest-supported conclusion (A-012, 66 percent, one review). On the evidence, though, Variant 3 is dominated by Variant 2: Variant 2 already holds the landing of the note behind the same two events and only adds a low-cost draft now. Variant 3's one distinct contribution, an explicit re-ask trigger, should be folded into Variant 2.

## Steelman

### Variant 1 (Proposal A: observer panel reads a captured copy of the sweep JSON, plus a note)

Strongest version: it is the only option that removes the user-facing problem instead of documenting it. The live #409 body (updatedAt 2026-11-13T16:57:51Z, verified read-only today) states the rationale: "If the observer built its own collector, two programs would classify the same session and could disagree. Reading the sweep's output keeps one definition of 'waiting on a person' or 'stalled'". Variant 1 also avoids the strongest objection to persistence: it captures the JSON the coordinator's WC-16 pass already prints, so NFR-001 ("a sweep adds exactly one report file", ADJ E-07, line 133) is untouched; that matches the "alternative kept open: caller-side stdout capture inside the WC-16 pass" in ADJ Part 8 (line 806). It keeps the note, gates the panel on #539 and XC-04, and treats every string as untrusted. It is the most complete long-run answer.

### Variant 2 (Proposal B: keep both separate, one written contract note)

Strongest version: it is the adjudicated verdict, "one short written note, no runtime link in version 1 ... the main product of the debate" (ADJ Part 2.3, line 222), and three planned texts depend on it (Coder#477 status record, v2 field list, #409 mapping table; same line). It changes no program code, adds one comparison test (XC-06) that turns the note's amendment rule into something enforced (ADJ line 225: "today no test reads any design document", INV-042), drafts on a master-based branch so the note cannot join #539 (ADJ line 224, INV-031; `merged-requirements.md:499`), and uses "candidate join basis" until XC-04 (avoiding the "premature join key" risk at `merged-requirements.md:500`). It also states its own limit honestly (identical words, different meanings, `merged-requirements.md:1160`).

## Strengths claimed

1. **It matches the confidence level of the evidence.** "Keep both programs" is A-012 at 66 percent, "provisional; only V5 states it and asks the owner" (ADJ line 364); "keep two readers" is X-017 at 70 percent (ADJ line 360). A recorded provisional answer with a dated re-ask trigger is the answer most proportional to a 66 percent, single-source verdict.
2. **It loses no landing time.** The note with its test cannot land on master before #539 merges (`merged-requirements.md:508`, W4: the test compares against `ALLOWED_ORCA` and report constants "which exist only on PR #539's head"). XC-07 already waits for #539 and XC-04 (question.md, XC-07 row). Variant 3's deferral therefore delays only the draft, not the merged artefact.
3. **It refuses to write a join claim before the one comparison that could establish it.** The join basis is "structural basis verified ... but not compared on real ids (D-3)" (ADJ line 229); `merged-requirements.md:1161` warns that even XC-04 on one Run does not establish the key in general. Waiting for XC-04 is logically consistent with that warning.
4. **It names an explicit trigger** ("after #539 merges and XC-04 is recorded"; diff-analysis U-003), which none of the other variants records as a re-ask condition for Q5 itself.
5. **It makes no claim the evidence does not support.** It adds no file, key, reader or test, so it cannot break NFR-001, the golden key set (`ROW_KEYS`, ADJ Part 2.2 action 5, line 210) or the "add no keys and no files inside #539" rule.

## Weaknesses identified in other variants

1. **Variant 1 reverses three adjudicated verdicts on weaker evidence.** It contradicts X-013 (95 percent, "no runtime link in version 1", ADJ line 325), X-017 (70 percent) and A-001 (78 percent, "Sweep JSON v1 is a candidate carrier only for v2 and for a Coder#477 status record, not for the observer", ADJ line 361), and it pre-answers Q9 and Q17 against their recommended "not now" (`merged-requirements.md:536`, `:544`). Answering three questions through one is scope creep on a question that asks only about Q5.
2. **Variant 1's source is a body the adjudication found stale, and its premise is already partly false.** ADJ Part 2.1 says the #409 body "is wrong in 23 places" (line 187), including "Preferred direction is Bubble Tea", which the live body I read today still contains. The rationale "If the observer built its own collector" is conditional on something that has already happened: the observer is built and reads Orca on its own 15 s poller (ADJ E-03, line 129; X-011, line 330). And the built observer does not classify in the sweep's terms: it "shows none of the ten dimension names; it prints Orca's words" (E-06, line 132). So "two programs would classify the same session and could disagree" overstates the conflict today; the disagreement is mostly between Orca's words and the sweep's classes, which the note's mapping table is designed to cover.
3. **Variant 1's panel has no reliable data source or join.** The captured file exists only when a coordinator runs the sweep (Variant 1's own cost list); the snapshot's row keys "carry no command, objective, branch, changed paths or issue or PR" (ADJ Part 8, line 808); the join key is uncompared (D-3). It also adds a new untrusted-input path (two sanitizers already exist, ADJ line 228).
4. **Variant 2's test does not prove alignment.** It "compares constants, not behaviour" (`merged-requirements.md:1160`); "stale" is 45 s in the observer feed (X-011, line 330) against a much longer threshold on the sweep side, and both can pass the test. The note documents the user-facing disagreement; it does not remove it (Variant 2's own cost list).
5. **Variant 2 drafts against constants on an open PR.** The sweep constants it will cite exist only on #539's head (W4), and #539 had two unresolved threads at adjudication time (E-08, 88 percent; current state UNVERIFIED today). A draft can need rework before landing.

## Concessions

1. **Variant 3 is internally strained (X-002).** Its "What it costs" section admits the draft "could have been written now on a master-based branch at low cost; only its landing waits for #539". That undercuts its own "moving target" reason for writing nothing.
2. **The "moving target" reason is weaker than Variant 3 states.** The note's subject matter is schema keys, shared words, Orca verbs and the join basis (ADJ lines 225-231). ADJ pins those as stable inside #539: "Add no JSON keys and no files inside #539" (action 5, line 210), and the Augment thread is to be resolved "with no new JSON key" (action 2, line 207). The open Q1 ruling changes the sweep's git argv and `ALLOWED_GIT` (line 206), which is not one of the note's listed contents. So the constants the note cites are unlikely to move much; Variant 2's test (XC-06) would catch any that do.
3. **Deferral delays the debate's one agreed outcome** ("the main product of the debate", line 222) and forces three dependent texts to be reworded later (Variant 3's own cost list).
4. **Variant 3's trigger is a conjunction of two uncertain events** (#539 merges; XC-04 runs). If either stalls (A-001, A-003), Variant 3 never writes anything and states no fallback; Variant 2 at least has a draft.
5. **The "saves the cost if the owner prefers a panel or merge" argument fails (X-003).** Even Variant 1, the panel option, keeps the note; merging was rejected by all five reviews (ADJ Part 8, line 807). The note is needed under every surviving option.

## Shared assumption responses

| id | Response | Reason |
|---|---|---|
| A-001 (#539 merges in roughly its current shape) | QUALIFY | ADJ shows #539 is "open, mergeable and not ready" with Q1 UNRESOLVED (line 204, 206), so a stall is real. The shape is protected by the "no keys, no files inside #539" rule (line 210), so if it merges, the note's constants are likely stable. But diff-analysis's claim that "only a note drafted against master constants survives" a stall is only partly true: the sweep constants exist only on #539's head (W4, `merged-requirements.md:508`), so a draft survives a stall but cannot be verified against master. |
| A-002 (the person reads both views) | QUALIFY | Not established by any source I read. The observer is "for a person or a coordinator only" (ADJ line 231, INV-013); the sweep runs in the coordinator's WC-16 pass and Q11 recommends "the sweep summary only until the contract note exists" (ADJ line 781). A person may see the sweep only through the coordinator's chat; how often they read both is UNVERIFIED. If they rarely read both, Variant 1's main gain shrinks. |
| A-003 (XC-04 can run) | QUALIFY | It needs a named runner (Q24, ADJ line 794), the Q1 ruling, and a runnable sweep; `merged-requirements.md:1154` records that the installed CLI printed "No such command 'sweep'" (R25-INV-006). It is plausible but not assured. This hurts Variant 3 most, because Variant 3's whole trigger depends on it; Variant 2's draft with "candidate join basis" does not. |

## Per-point positions

| Point | Superior variant | Confidence | One-line reason |
|---|---|---|---|
| S-001 | none (identical) | 90 | Same five sections in the same order by design of the brief; no difference to judge. |
| C-001 | V2 (V3 equal) | 85 | No runtime link matches X-013 (95%) and ADJ Part 8 line 808; V1's link needs a data source and join that do not exist yet. |
| C-002 | V2 | 75 | Note is the adjudicated main product (line 222); V3's deferral costs three dependent texts; V1's third registered artefact presupposes Q9. |
| C-003 | V2 (V3 equal) | 75 | Both keep Q9 and Q17 at their recommended "not now" (`merged-requirements.md:536`, `:544`); V1 pre-answers two other questions. |
| C-004 | V2 | 70 | Same landing gate as V3 (W4, XC-07) but a cheap draft now; V1's timing is fine but its scope is not. |
| C-005 | V2 | 70 | Setting the #409 proposal aside for v1 is consistent with X-013 and A-001; the #409 body is stale in 23 places (line 187) and its "own collector" premise has already happened. |
| C-006 | V2 | 60 | Neither V2 nor V3 changes program code; V2's one comparison test is the only mechanism that enforces the note (INV-042). |
| X-001 | V2 | 70 | The built observer prints Orca's words, not sweep classes (E-06), so documented differences are acceptable in v1; the residual "stale" risk (`:1160`) is real but V1 does not fix it either without a join. |
| X-002 | V2 | 80 | V3 contradicts itself by admitting the draft is cheap now; the note's contents are pinned stable inside #539 (line 210). |
| X-003 | V2 | 75 | Every surviving option, including V1, keeps the note, so it is not wasted. |
| A-001 | V2 | 65 | A draft exists if #539 stalls; V3 has nothing and no fallback. |
| A-002 | V2 | 55 | Unverified either way; if the person rarely reads both views, V1's gain shrinks and a note suffices. |
| A-003 | V2 | 65 | V2's draft uses "candidate join basis" and does not need XC-04 to exist; V3's trigger depends on it entirely. |

## Overall

Neutral recommendation to the owner: **Variant 2**, confidence **75 percent**, amended with Variant 3's one useful idea: record Q5 as "provisional" in the ledger and re-ask it once, with the XC-04 result in hand, before XC-07 lands. Variant 1 is the better long-run direction only if the owner later answers Q17 "yes"; it is premature for version 1. I would not recommend Variant 3 as written.

Unverified in this statement: the current state of PR #539's review threads (E-08 is as of adjudication); how often the person reads both views (A-002).
