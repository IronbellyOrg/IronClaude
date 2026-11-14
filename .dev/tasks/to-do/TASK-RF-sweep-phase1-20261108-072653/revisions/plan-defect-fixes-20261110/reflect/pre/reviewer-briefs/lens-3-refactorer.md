# Lens 3 (persona: refactorer): spec fidelity, routing row (F-02) and downstream gates in Phases 11, 13 and 14

Read first: the common brief (same folder, common.md). Your slice: items 11.1 to 11.20, 13.1 to 13.24, 14.1 to 14.49 and the DESIGN sections they implement.

Focus on F-02 and spec fidelity:
1. Item 13.1 (TL:2263-2268): compare the quoted routing bullet with DESIGN:716 character by character; check the placement claims against src/superclaude/core/HOW-WE-WORK.md lines 396-405; check the `grep -nF` command (backticks and inner double quotes, will a fixed-string search find the line, what does it print today and after the edit); check item 13.2 and the 13.12 routing lens (TL near 2342) for line shifts or wording that still use the old sentence; confirm ticked item 5.2 (TL:774-778) is untouched and that nothing now contradicts it.
2. The F-06 reword and the F-01 wording on the 13.x and 14.x lens items: any change of meaning? 14.19 (TL:2570-2573): does the cross-artifact lens still ask for the right things (WC-16, flags, report location, JSON schema version, owner decisions, the seven table sites)?
3. QA gate sufficiency across Phases 13 and 14: compare the changed items with BASE for any lost agent count, lens, serialized fixer, cycle cap, sha256 guard or halt order. List the fixers that may edit the style file or the design and what guards them.
4. Spec fidelity of the whole edit set: does any new text misstate DESIGN, ADD or the OQ-6 record (R1/../phase-outputs: P/phase-outputs/plans/OQ-6-GQ-63-done-next-decision.md) or add scope beyond them (for example a new rule that is in neither)? Quote both sides.
5. Coverage matrix rows touched by the delta (rows that cite changed items): does the status still hold? Name any row whose covered/partial/missing status would change, with evidence.
