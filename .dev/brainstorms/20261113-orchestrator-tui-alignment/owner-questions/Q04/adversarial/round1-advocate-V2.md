# Round 1 advocate statement: Variant 2 (proposal B), architect persona

## Position summary

Q4 is a naming question: which existing thing does "TUI Panel" point at. Variant 2 answers only that (`superclaude observe`, the #409 dashboard) and keeps two release-level properties, the host boundary and read-only, out of the answer, because the observer's own roadmap already plans to change one of them (R4, remote fleet) and has not settled the other (R3, Decision Desk). Keeping the name separate from those properties stops Q4 from deciding Q3 and Q18 by side effect.

## Steelman

### Variant 1 (observe; single-host; read-only; TUIBBS a possible later reader)

Strongest version: it is the recommendation already written in both sources, word for word ("TUI Panel = `superclaude observe`; single-host; read-only", ADJ line 307; `merged-requirements.md:531`). Every clause is true today: the observer is merged (PRs #503, #514, ADJ E-01 line 127), reads Orca on one host and is read-only (ADJ glossary lines 77, 92). It gives Q3's close condition (ADJ line 283) an owner sentence to test against, so CO-01 can go out in one pass. It is cheap to undo: ADJ line 307 marks it "Undo: yes" (an edited comment). It describes a program that exists rather than one that might.

### Variant 3 (both, as a planned sequence)

Strongest version: it takes the #409 lineage seriously. The #409 body preferred a Go stack "informed by TUIBBS-scp styling and components" (`.dev/issues/409/issue-body.md:25`), the glossary says the snapshot "is shaped so a read-only Go screen there could read it later" (ADJ line 91), and the owner's 2026-11-08 record says "the observer may become a TUIBBS module" (ADJ line 306). If that is the real destination, starting the four missing pieces (transport, identity envelope, age rule, re-sanitising, ADJ line 306) early is cheaper than starting them when a screen is waiting, and a narrowed Coder#477 gets a named consumer. Its cost is bounded by A-004: the snapshot contract does not change under any reading (ADJ line 306; `merged-requirements.md:562`).

## Strengths claimed

1. **It does not publish a property the roadmap already plans to break.** The observer's planned releases include "R4 is the remote fleet" (ADJ line 92). A public "single-host" line describes R1 and R2 only; it becomes false at R4 by design. Variant 2's line ("TUI Panel = `superclaude observe` (the #409 dashboard); later readers not decided") stays true through R4.
2. **It keeps Q4 decoupled from Q3, which the ADJ itself requires.** ADJ line 283: "Narrowing or closing does not choose what 'TUI Panel' means (INV-043)." The converse should hold too: the meaning of "TUI Panel" should not choose narrow or close. Variant 1 couples them through the word "single-host"; Variant 2 does not.
3. **It matches the strength of the owner's own record.** The 2026-11-08 record says "Background, not deciding" (ADJ line 306). Variant 2 keeps the TUIBBS direction exactly as undecided as that record leaves it (C-006). It also does not lean on that record, which exists only in a sibling worktree and not on master (ADJ E-16, line 142).
4. **It leaves Q18 to its own gate.** Q18's recommended answer is "Not before observer R4 or an owner statement that a TUIBBS screen is planned", and its default is "ADJ recommendation applies" (`merged-requirements.md:545`). Variant 2 makes neither statement, so Q18's default holds and CO-04 is not opened by a side door.
5. **It avoids the A-003 trap.** It does not assert "read-only" as a standing property. R3 (Decision Desk) sits behind the QUESTION-LINK gate (ADJ line 88) and whether it writes is UNVERIFIED (diff-analysis A-003). A public "read-only" line could be falsified by the observer's own next release.
6. **It is still enough for CO-01.** CO-01 condition (2) asks only that "the reply states Q4's answer in one line" (`merged-requirements.md:353`). Variant 2 supplies that line.

## Weaknesses identified in other variants

1. **Variant 1: a present-tense label cannot satisfy a future-tense test.** The ADJ close condition is "if the observer *stays* single-host and TUIBBS is not near" (ADJ line 283). "Single-host" in the Q4 reply says what the observer is now, not that it will stay so; and R4 (ADJ line 92) says it will not. So Variant 1 gives Q3 an apparently testable sentence that does not answer the question Q3 asks, and tilts Q3 toward close on a misreading (Variant 1 concedes this risk in its own "costs" section).
2. **Variant 1: "read-only" is unverified for R3.** See strength 5. Variant 1 states it publicly in another repository (Coder) where a later correction is a second public edit.
3. **Variant 3: it promotes the weakest reading into a commitment.** ADJ Part 2.7 puts the TUIBBS reading at about 15 percent against 70 to 75 percent for `superclaude observe` (ADJ line 306). The only owner words on TUIBBS are "may become" and "Background, not deciding".
4. **Variant 3: the #409 lineage it cites is superseded.** The "Preferred direction is Bubble Tea" text in #409 is one the owner "replaced with Python + Rich on 2026-11-08" (ADJ line 187). The built observer is a `superclaude` CLI command (ADJ E-01). So the Go-stack sentence at `.dev/issues/409/issue-body.md:25` is not evidence of a TUIBBS plan (X-002).
5. **Variant 3: it opens a trust boundary with nothing to stand on.** "No document in TUIBBS mentions Coder or Orca" (ADJ line 306); the snapshot `scope` is only `object` or `"UNKNOWN"` and has no liveness field (ADJ line 306). Declaring a TUIBBS screen "planned" meets Q18's condition (`merged-requirements.md:545`) and starts CO-04, copying worker data off the host, with no task package.

## Concessions

1. Variant 2's reply is less useful to a Coder#477 reader: it does not say whether the feature must serve one host or several.
2. Q3 loses an owner sentence to test its close condition against and rests on the ADJ's reading instead (Variant 2's own "costs").
3. The question will likely come back when R4 or a TUIBBS task is proposed. I argue this is a small cost (Q18 must be decided at that point anyway), but it is a real extra owner touch.
4. The word "provisional" can read as indecision. Once the owner answers, the meaning is the owner's; "today" carries the point without weakening the answer, and I would drop "provisional" from the ledger wording.
5. Variant 1 is what both the spec and the ADJ recommend (`merged-requirements.md:531`; ADJ line 307), and it is reversible. Variant 2 departs from a reviewed recommendation.
6. Variant 2 is silent on "read-only" even for today, where it is a verified fact (ADJ E-01, glossary line 77). A scoped "read-only today" would be true and useful; Variant 2 as written omits it.

## Shared assumption responses

| Id | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | Supported but not proven: the comment's two nouns mirror the titles of #339 and #409, and the glossary equates them (ADJ lines 77, 306). But the phrase appears in no owner-written file (ADJ line 306) and #477 lives in the Coder repo, so a Coder-side panel is not ruled out. The owner's answer should confirm it, not assume it. |
| A-002 | QUALIFY | CO-01 (2) requires one line in the reply (`merged-requirements.md:353`), but that is a plan requirement, not an owner statement. The owner may prefer the meaning recorded in the ledger only. If it is posted publicly, the line should carry only claims that stay true, which favours a minimal line. |
| A-003 | QUALIFY | True today: the built observer is read-only (ADJ line 77; E-01). Not established for later releases: R3 (Decision Desk) is behind QUESTION-LINK (ADJ line 88) and whether it writes is UNVERIFIED. Any public "read-only" should be scoped to "today" or to R1 and R2. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | None (identical) | 95 | Same five sections in the same order by design of the brief. |
| C-001 | V2 | 60 | V1 and V2 name the same program; V2's "today" scoping is more accurate given R3 and R4, but V1's flat form is cleaner. |
| C-002 | V2 | 70 | "Single-host" contradicts the planned R4 (ADJ line 92); a planned second host (V3) is unsupported. Saying nothing is the only claim that stays true. |
| C-003 | V2 | 65 | INV-043 (ADJ line 283) separates Q3 from Q4's meaning; V1's present-tense label does not answer Q3's "stays" test. |
| C-004 | V1 | 55 | V1 states Q18's "not yet" explicitly; V2 reaches the same default only implicitly (`merged-requirements.md:545`); V3 opens CO-04 without support. |
| C-005 | V2 | 60 | V2's line stays true through R3 and R4; V1's is more informative but carries two claims that later releases may falsify. |
| C-006 | V2 | 75 | Matches the owner's own "Background, not deciding" (ADJ line 306). |
| X-001 | V2 | 65 | The host boundary is a release property for Q18 and R4, not part of a naming answer. |
| X-002 | V1 | 75 | The owner replaced the Go direction with Python + Rich on 2026-11-08 (ADJ line 187); the built CLI is the fact. V2 simply does not use the point. |
| X-003 | V2 | 55 | V1 settles the name but with properties that R4 will unsettle; V2's re-ask coincides with the Q18 decision that must happen then anyway. Close call. |
| A-001 | V2 | 55 | All three share it; V2's narrower claim is the easiest to correct if the owner meant something else. |
| A-002 | V2 | 60 | If the meaning goes public, the minimal line exposes the least to later correction in another repository. |
| A-003 | V2 | 70 | V2 alone does not assert read-only; V1 and V3 both do, and R3's write behaviour is UNVERIFIED. |

## Overall

If I were neutral I would recommend Variant 2, at about 60 percent confidence, with Variant 1 a close second. The best owner answer is likely a merge of the two: Variant 2's scoping plus one verified fact from Variant 1, for example "TUI Panel = `superclaude observe` (the #409 dashboard); read-only today; later readers not decided". That keeps the reply true through R3 and R4, gives Q3 no false close test, and leaves Q18 at its own gate. Variant 3 I would not recommend (about 85 percent confidence it is wrong for now): it turns a 15 percent reading into a commitment on a superseded lineage and opens a cross-host trust boundary with no task package.
