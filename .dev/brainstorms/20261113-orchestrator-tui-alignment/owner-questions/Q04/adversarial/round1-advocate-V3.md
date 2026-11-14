# Round 1 advocate statement: Variant 3 (proposal C, "both, as a planned sequence")

Persona: frontend (what screen the owner will actually look at). Mode A, depth quick, Round 1 only.

## Position summary

Variant 3 is the only answer that names both screens the owner has been shown: the built `superclaude observe` view and the TUIBBS-styled Go screen the #409 design package aimed at, and it treats them as one sequence over one snapshot. Its real weakness is that it states a TUIBBS screen is *planned*, which no source shows the owner has decided; on the evidence I would not recommend it as written.

## Steelman

**Variant 1 (observe; single-host; read-only; TUIBBS a possible later reader).** At its strongest: it names the one panel that exists and is merged (PRs #503, #514; ADJ E-01, line 127), matches the working reading at about 70 to 75 percent (ADJ Part 2.7, line 306), and the word "Panel" already fits the built program, since the observer implements "the Attention Ledger's question panel" (ADJ glossary, line 93). It gives Q3's close condition ("the observer stays single-host and TUIBBS is not near", ADJ line 283) an owner statement to test, and it keeps TUIBBS visible as "a possible later reader" rather than erasing it. It is the spec's recommended answer (`merged-requirements.md:531`). It gets right the most important fact for a reader of Coder#477: the alignment target is a real screen, not a mock-up.

**Variant 2 (observe today, provisional; no statement about hosts or later screens).** At its strongest: it is the only answer whose every word is true today and stays true whichever way R3, R4 or TUIBBS go. It keeps the owner's 2026-11-08 position "Background, not deciding" (ADJ line 306) exactly as the owner left it, and it does not let Q4 quietly decide Q3 or Q18 (diff-analysis U-002, rated High). It also avoids the "read-only" claim, which could become false if Decision Desk (R3, "the screen for answering coordinator questions") lets the owner act from the screen (diff-analysis A-003).

## Strengths claimed

1. **It matches the screen the owner was shown, not only the one that was built.** #409's design direction was "Bubble Tea v2, Lip Gloss v2 and Bubbles v2, informed by TUIBBS-scp styling and components" (`.dev/issues/409/issue-body.md:25`), while the built observer is a `superclaude` CLI command (question.md, fact row 8; ADJ E-01). An owner who pictures "the TUI Panel" may be picturing the TUIBBS-styled design images (ADJ glossary line 93: twenty synthetic designs), and only Variant 3's line names that screen.
2. **The architecture already anticipates the second reader.** The glossary states "the observer snapshot is shaped so a read-only Go screen there could read it later" (ADJ line 91), and the owner's 2026-11-08 record says "the observer may become a TUIBBS module" (ADJ line 306). Variant 3 describes the system the snapshot was shaped for.
3. **The sequence framing keeps one contract.** "A TUIBBS screen would be a second reader of the observer's snapshot, not a second program with its own collector. The answer changes the transport, not the contract" (ADJ line 306; diff-analysis A-004, STATED). Variant 3 commits to no second collector and no second data shape.
4. **It gives a narrowed Coder#477 a named consumer.** Coder#477's body is about a workspace listener and prompt routing (`gh issue view 477 --repo IronbellyOrg/Coder`); if Q3 narrows it to read-only workspace status and identity (ADJ line 283), Variant 3 says which screen reads that status. The other two leave the narrowed feature's reader implicit.
5. **It names the trust boundary early** (diff-analysis U-004): a copy of worker data leaving the host needs a transport, an identity envelope, an age rule and re-sanitising (ADJ line 306). Variant 3 is the only one whose own text puts those four pieces on the table.
6. **It is the only one-step answer for an owner who does intend TUIBBS.** Under Variants 1 and 2 that owner must answer Q4 and then separately make the "owner statement that a TUIBBS screen is planned" Q18 needs (`merged-requirements.md:545`).

## Weaknesses identified in other variants

1. **Variant 1's "single-host" reads on screen as a lasting product limit.** The observer's remote fleet is its planned release R4 (ADJ glossary line 92). A one-line public reply "single-host; read-only" has no "today", so a Coder#477 reader sees a permanent boundary, and Variant 1 itself admits this "tilts Q3 toward closing #477 even if the owner expects remote reading (R4) later" (variant-1, costs).
2. **Variant 1 reduces the design lineage to a footnote.** The owner's TUIBBS note survives only as "a possible later reader", and the reply line does not carry even that; the #409 preferred Go stack (`issue-body.md:25`) disappears from the public statement.
3. **Variant 1's "read-only" may age badly.** R3 is Decision Desk (ADJ line 92); whether it writes is UNVERIFIED (diff-analysis A-003). A screen where the owner answers questions is, from the owner's seat, an action surface.
4. **Variant 2's reply is the least useful screen-level statement.** "later readers not decided" tells a Coder#477 implementer nothing about whether the feature serves one host or several (variant-2, costs), and Q3 then rests on the ADJ's reading, not the owner's.
5. **Variant 2 guarantees a second round.** It expects the question to be "re-asked when observer release R4 or a TUIBBS task package is proposed" (variant-2, step 4): the owner pays for the same question twice.

## Concessions

1. Variant 3 turns the weaker reading (about 15 percent, ADJ line 306) into a commitment. The owner's own record says "Background, not deciding" (ADJ line 306); "planned" contradicts it. This is the decisive weakness.
2. It satisfies Q18's trigger by its own wording: the "owner statement that a TUIBBS screen is planned" (`merged-requirements.md:545`) would be manufactured by the answer template, not by an owner plan. That is circular.
3. It opens cross-host work (CO-04) and a new trust boundary with no task package, and "No document in TUIBBS mentions Coder or Orca" (ADJ line 306; glossary line 91).
4. My Strength 1 over-reads the #409 lineage: the Go stack is a "preferred direction" for a design package that is "synthetic and [has] no live integration", where "User selection precedes production integration" (`issue-body.md:23,25`). It is not a TUIBBS integration commitment (diff-analysis X-002).
5. Variant 1's "Panel" fit is real: the built observer already contains a "question panel" (ADJ line 93), so the word does not need TUIBBS to make sense.
6. Variant 3 also says "read-only", so it carries the same A-003 risk I charged Variant 1 with.

## Shared assumption responses

| # | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | Likely but not proven. The comment's two nouns mirror the titles of #339 and #409 and the ADJ glossary equates the "TUI panel" with the observer (ADJ lines 77, 306). But Coder#477 lives in the Coder repo and its body lists Coder template files (`main.tf`, `orca/runtime.mjs`) as components; a Coder-side panel reading is not ruled out by any source (UNVERIFIED either way). Whatever variant wins, the reply should name "the #409 dashboard" explicitly so a wrong guess is visible to the owner on first read. |
| A-002 | QUALIFY | CO-01 (2) requires the line (question.md, "What it gates"), so it is a plan requirement, not an owner statement. A one-line comment is cheap and reversible (edit), which justifies posting it; but the owner should see the exact line before it is posted, since it is public in another repository. |
| A-003 | QUALIFY | True for R1 and R2 on master (ADJ E-01, E-02: the questions read is off). R3 Decision Desk is "the screen for answering coordinator questions" (ADJ line 92), and whether it writes is UNVERIFIED. Any variant that says "read-only" should say "read-only today" or drop the word; Variant 3's line needs that fix as much as Variant 1's. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (all three) | 95 | Identical section set by design of the brief. |
| C-001 | V1 | 65 | Names the built, merged screen at the 70 to 75 percent reading; V3 adds a plan with no owner evidence. |
| C-002 | V1 | 55 | Single-host is true today (ADJ E-01) and gives Q3 a test, but only if worded "today"; V2 is the safe fallback. |
| C-003 | V2 | 60 | Q3 should rest on its own merits; Q4 tilting Q3 in either direction (V1 to close, V3 to narrow) is a side effect. |
| C-004 | V1 | 70 | Q18's recommended "not yet" holds; V3 unlocks CO-04 by its own wording, which is circular. |
| C-005 | V1 | 60 | The most concrete true line for a #477 reader; it would be best with "today" added to "single-host; read-only". |
| C-006 | V2 | 70 | Keeps "Background, not deciding" as the owner left it; V3 turns it into a plan. |
| X-001 | V2 | 55 | Silence on hosts cannot become false; V1's statement is useful but reads as permanent. |
| X-002 | V1 | 70 | The built CLI is the fact; #409's Go preference was a design direction pending user selection (`issue-body.md:23,25`). |
| X-003 | V1 | 60 | Settling now with a reversible edit beats a guaranteed re-ask (V2) or more decisions sooner (V3). |
| A-001 | Tie (all share it) | 60 | None tests it; naming "the #409 dashboard" in the line is the mitigation for whichever wins. |
| A-002 | V2 | 55 | Its line commits least in public, so a wrong shared assumption costs least. |
| A-003 | V2 | 65 | The only line without "read-only", so it cannot become false when R3 ships. |

## Overall

As a neutral judge I would recommend **Variant 1** to the owner, with confidence 62, amended to read "TUI Panel = `superclaude observe` (the #409 dashboard); single-host and read-only today; a TUIBBS screen reading its snapshot is a possible later reader". That keeps Variant 1's concrete screen, takes Variant 2's protection against permanence, and keeps Variant 3's sequence visible without claiming a plan. Variant 3 as written is the right answer only if the owner confirms that a TUIBBS screen is planned; the sources do not show that.
