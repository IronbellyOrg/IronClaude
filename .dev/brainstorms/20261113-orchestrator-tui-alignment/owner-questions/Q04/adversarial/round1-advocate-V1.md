# Round 1 advocate statement: Variant 1 (Proposal A)

Persona: analyzer (evidence quality and logical consistency). Mode A, depth quick, Round 1.

## Position summary

"TUI Panel" should be answered as `superclaude observe`, the built and merged #409 dashboard, because that is the only reading with a built referent and the strongest source support (ADJ Part 2.7: about 70 to 75 percent). Variant 1 states that reading in the exact line the spec already carries, and keeps Q18 at its recommended "not yet". Its weak point is that "single-host" and "read-only" describe today's build and can be read as permanent; on that point Variant 2's temporal scoping is better, and I concede it.

## Steelman

### Variant 2 (Proposal B: `superclaude observe` today, provisional; no host or later-screen statement)

Strongest version: Q4 asks what a word *meant*, not what the observer *will be*. Variant 2 answers only the question asked. It records the meaning without adding owner commitments the sources do not contain. "Single-host" and "read-only" are properties of a program, not meanings of a phrase. It keeps the owner's own 2026-11-08 position ("the observer may become a TUIBBS module", "Background, not deciding"; ADJ line 306) exactly as undecided as the owner left it. It also respects the ADJ's decoupling principle (INV-043, ADJ line 283: "Narrowing or closing does not choose what 'TUI Panel' means"). The diff analysis rates this separation the highest-value unique contribution (U-002, High). Variant 2 also avoids the A-003 trap: it never claims "read-only" for future releases, so release R3 (Decision Desk) cannot make it false.

Critique: it leaves out information that is true and checkable today. The observer reads Orca on one host only and is read-only (ADJ E-01, line 127; glossary line 92). A reader of Coder#477 is designing a workspace-side feature (the #477 body asks for "a listener in every Coder workspace", "secure prompt routing"). That reader needs to know whether the thing to align with spans hosts today. "Later readers not decided" answers that only by implication. It also accepts a likely second round of the same question (Variant 2's own "What it costs": "A second round of the question is likely when R4 is proposed").

### Variant 3 (Proposal C: both, as a planned sequence)

Strongest version: the #409 lineage does point at TUIBBS. The issue body states the preferred direction was "Bubble Tea v2, Lip Gloss v2 and Bubbles v2, informed by TUIBBS-scp styling and components" (`.dev/issues/409/issue-body.md:25`). The owner wrote that "the observer may become a TUIBBS module" (ADJ line 306). The glossary already says the snapshot "is shaped so a read-only Go screen there could read it later" (ADJ line 91). If the owner does mean that sequence, Variant 3 gives the narrowed Coder#477 a real consumer. Without one, the narrowed feature risks being designed for nobody. Variant 3 also starts the four missing pieces (transport, identity envelope, age rule, re-sanitising; ADJ line 306) before a screen is waiting on them. It is the only variant that names the new trust boundary of worker data leaving the host (U-004). It is also internally consistent: the ADJ itself says both readings "are a sequence, not a conflict" (ADJ line 306).

Critique: the sources show no owner commitment to a TUIBBS screen. The owner's record says "Background, not deciding" (ADJ line 306). The ADJ weights the TUIBBS reading at about 15 percent. "No document in TUIBBS mentions Coder or Orca" (ADJ line 306, citing sibling `tuibbs-review/notes-3.md:78-84`, which I have not read: UNVERIFIED by me). Variant 3's step 3 claims that "Q18's recommended condition ... is met by this statement". That is circular. The condition is met only because Variant 3 asks the owner to make the very statement the evidence does not show. Variant 3 concedes this itself ("turns a 15 percent reading ... into a commitment the sources do not show the owner has made"). The #409 Go-stack preference is weaker evidence than it looks. What was built is a `superclaude` Python CLI command (ADJ E-01: "registered in the shipped CLI", `src/superclaude/cli/main.py:572-574`), not a Go program. So the preference was not followed even within #409.

## Strengths claimed

1. **It names the only built referent.** The observer is built and merged in PRs #503 and #514 (ADJ E-01, line 127). No TUIBBS screen exists, and no TUIBBS document mentions Coder or Orca (ADJ line 306). An answer pointing at shipped code can be checked. An answer pointing at an unbuilt screen cannot.
2. **It matches the strongest-weighted reading.** ADJ Part 2.7 (line 306) puts `superclaude observe` at 70 to 75 percent and TUIBBS at about 15 percent. The ADJ glossary already equates the observer with "the 'TUI panel' in the owner's wording" (line 77). The reasoning is that the comment's two nouns mirror the titles of #339 and #409 (ADJ line 306; I did not re-read those titles myself: UNVERIFIED by me).
3. **It needs no new document and no new wording.** Its reply line is exactly the spec's recommended line (`merged-requirements.md:531`; CO-01 row (2): "TUI Panel = `superclaude observe`; single-host; read-only" if recommended). It also matches ADJ Part 2.7's recommendation (line 307). So CO-01 can be posted as soon as Q3 is answered.
4. **Its Q18 position is the ADJ's own recommendation.** Q18 stays at "Not before observer R4 or an owner statement that a TUIBBS screen is planned" (`merged-requirements.md:545`). CO-04 stays DEFERRED (`merged-requirements.md:356`). Variant 1 opens no new trust boundary.
5. **It is cheap to reverse.** If the owner meant TUIBBS, the fix is an edited comment (Variant 1, "What it costs"). The contract survives: "the answer changes the transport, not the contract" (ADJ line 306; `merged-requirements.md:1177`, item 10).
6. **It states present facts that the #477 reader needs.** Coder#477 is a cross-workspace feature (its body asks to "register each workspace and listener with the monitor"). Telling that reader that the alignment target is single-host today is decision-relevant. Today's observer reads one host only (glossary line 92: R4 "is the remote fleet").

## Weaknesses identified in other variants

1. **Variant 2 removes true, decision-relevant facts.** The single-host and read-only properties of the merged observer are established (ADJ E-01, glossary lines 77, 92). Leaving them out of a reply to a cross-host feature request makes the reply less useful (Variant 2 concedes this: "does not say whether the feature must serve one host or several").
2. **Variant 2 builds in a re-ask.** Its step 4 schedules the question again when R4 or a TUIBBS package is proposed. That spends a second owner decision on a question whose present answer is already agreed by all three variants (C-001: all three say `superclaude observe` today).
3. **Variant 3's evidence does not reach its conclusion.** The strongest owner evidence for TUIBBS is a "may become" statement paired with "Background, not deciding" (ADJ line 306). That supports "possible", not "planned". Variant 3's reply line asserts "a TUIBBS screen reading its snapshot is planned" in a public comment in another repository.
4. **Variant 3 opens cross-host work with no package.** CO-04 is gated on R4 or an owner TUIBBS statement (`merged-requirements.md:356`). Variant 3 makes that statement to unlock CO-04, which requires a transport, an identity envelope (the snapshot `scope` is only `object` or `"UNKNOWN"`), an age rule (Q22) and re-sanitising (ADJ line 306). None of these is specified, and no TUIBBS document references Coder or Orca.
5. **Variant 3 misreads the #409 lineage.** "Informed by TUIBBS-scp styling and components" (`.dev/issues/409/issue-body.md:25`) is a styling source for a Go stack. The built observer is a Python `superclaude` command (ADJ E-01). It is not evidence of a TUIBBS host target.

## Concessions

1. **Variant 1 overstates its Q3 unlock.** The ADJ's close condition is "if the observer *stays* single-host and TUIBBS is not near" (ADJ line 283). That condition is about the future. Variant 1's "single-host" is a present-tense property, so it cannot test "stays". U-001 is weaker than Variant 1 claims. At most it records today's state, which the ADJ already knows from E-01.
2. **"Single-host" and "read-only" are properties, not meanings.** Putting them in a statement of what a word meant invites the reading that they are lasting limits. Variant 1 flags this risk itself ("may be read as a lasting limit, which tilts Q3 toward closing #477"). Variant 2's "today / later readers not decided" scoping is the better form on this point.
3. **"Read-only" may not survive R3.** The glossary lists R3 as Decision Desk (line 92) and QUESTION-LINK as its gate (line 88). Whether Decision Desk writes is UNVERIFIED (diff-analysis A-003). An unqualified "read-only" in a public reply could become false.
4. **Variant 1 gives the owner's 2026-11-08 note less weight than Variant 2 does.** "A possible later reader" is close to, but slightly firmer than, the owner's "Background, not deciding".

## Shared assumption responses

| # | Response | Reason |
|---|---|---|
| A-001 ("TUI Panel" names a reader of Orca worker state) | QUALIFY | The supporting evidence is indirect. The ADJ says the phrase "appears in no owner-written file" (line 306), and the nouns-mirror-titles argument is inference. Coder#477 lives in the Coder repo and lists Coder template files (its "Components Affected" section names `templates/VSCode-AIDev02/...`), so a Coder-side panel is not ruled out. I did not search the Coder repository for "TUI Panel": UNVERIFIED. Pairing "TUI Panel" with "Orchestrator" (the #339 noun) makes the worker-state reading the most likely one, not a certain one. |
| A-002 (the meaning belongs in the public Coder#477 reply) | QUALIFY | CO-01 row (2) requires the one line (`merged-requirements.md:562`), but that is the plan's requirement, not an owner statement. The owner's comment ("Ensure this aligns with ...") reasonably invites an answer on the issue. The owner could still choose to record the meaning in the ledger only (XC-01) and keep the reply silent. |
| A-003 (the observer stays read-only in every later release) | QUALIFY | True for the merged releases R1 and R2 (ADJ E-01; glossary line 77: "The read-only terminal dashboard"). It is not established for R3 Decision Desk (glossary lines 88, 92; whether it writes is UNVERIFIED). Any reply that says "read-only" should scope it to today ("read-only today"), which corrects Variants 1 and 3. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | none (tie) | 95 | Identical section sets by design of the brief. |
| C-001 | V1 | 60 | Same core meaning as V2, stated firmly in line with the ADJ's 70 to 75 percent reading; V3 adds an unsupported commitment. |
| C-002 | V2 | 55 | "Single-host" is a present property that reads as a lasting limit; V3's planned second host lacks owner evidence; silence or "today"-scoping is safer. |
| C-003 | V2 | 60 | V1's present-tense "single-host" cannot test the ADJ's future "stays single-host" condition; deciding Q3 on its own merits fits INV-043's decoupling. |
| C-004 | V1 | 65 | "Not yet" is the ADJ's and the spec's recommendation (`merged-requirements.md:545`); V3 meets the condition only by making the unsupported statement itself. |
| C-005 | V1 | 55 | It is the spec's verbatim recommended line (CO-01 (2)) and the most informative of the three; it would be better with "today" added. |
| C-006 | V2 | 65 | It keeps the owner's "Background, not deciding" exactly; V1 is close; V3 upgrades "may" to "planned". |
| X-001 | V2 | 55 | No host statement is the least likely to be read as a commitment either way; V1's present fact is true but easy to misread. |
| X-002 | V1 | 75 | The built Python CLI (ADJ E-01) is the fact; #409's Go-stack styling preference was not even what #409 built. |
| X-003 | V1 | 60 | Settling now lets CO-01 post after Q3 with no planned re-ask; the present meaning is uncontested across all three variants. |
| A-001 | V2 | 55 | All three variants share the assumption; V2's "provisional" wording is the cheapest to correct if it is wrong. |
| A-002 | V1 | 55 | All three variants post a line; V1's is the shortest, and it is the one the spec already requires. |
| A-003 | V2 | 70 | The only variant that does not assert "read-only" without a time scope. |

## Overall

As a neutral judge I would recommend **Variant 1, amended with Variant 2's temporal scoping**. Reply line: "TUI Panel = `superclaude observe` (the #409 dashboard); today single-host and read-only; later readers, including a TUIBBS screen, not decided". Q18 stays at "not yet". Confidence: 70.

If the owner must pick one of the three unmodified: **Variant 1**, confidence 55, with Variant 2 a close second. Variant 1 states verifiable present facts about a built program in the spec's own words. Variant 2 is more careful about the future but less useful to the #477 reader. Variant 3 asserts a plan the sources do not show.
