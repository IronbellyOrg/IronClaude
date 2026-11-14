# Merge Log: Q4 (what "TUI Panel" means)

## Metadata

- Base: Variant 2 (proposal-B), `adversarial/variant-2-original.md`
- Plan: `adversarial/refactor-plan.md` (5 planned changes, auto-approved 2026-11-14)
- Incorporated sources: `adversarial/variant-1-original.md`, `adversarial/variant-3-original.md`, `adversarial/debate-transcript.md`, `question.md`
- Output: `merged-proposal.md`
- Merge date: 2026-11-14
- Rule carried: no claim that a TUIBBS screen exists or is planned.

## Changes Applied

### Change 1: replace the answer and reply line with the converged line

- Status: APPLIED
- Before: title "name `superclaude observe` as today's meaning only, and make no statement about hosts or later screens"; reply line "TUI Panel = `superclaude observe` (the #409 dashboard); later readers not decided"; no host or read-only facts.
- After: new title naming `superclaude observe` (the #409 dashboard), single-host and read-only today, later readers not decided. Answer states the built and merged program (PRs #503, #514), one host and read-only today (ADJ E-01, line 127; glossary, line 92), the glossary equation (ADJ glossary, line 77), and a TUIBBS screen as a possible later reader, not decided. Reply line replaced verbatim with the plan's converged line. Step 2 carries "that line". Consistency edits in "What it unlocks" bullets 1 and 2 ("minimal" dropped; "today" scopes the properties).
- Provenance tag: `<!-- Source: Variant 2 base, modified by Change 1 ... -->` on the Answer section, and noted in the "What it unlocks" source comment.
- Validation: reply line matches `refactor-plan.md` line 16 and `debate-transcript.md` line 36 character for character. Facts match `question.md` rows citing ADJ E-01, glossary lines 77 and 92. No "planned" wording about a TUIBBS screen.

### Change 2: drop "provisional"

- Status: APPLIED
- Before: Answer "recorded as the owner's provisional meaning"; step 1 "The ledger records the provisional meaning".
- After: Answer "recorded as the owner's meaning, with today's properties"; step 1 "The ledger records the owner's meaning, with today's properties, its date and the words "later readers not decided"".
- Provenance tag: noted in the Answer and "What happens next" source comments (Variant 2 advocate concession 4).
- Validation: the word "provisional" no longer appears in `merged-proposal.md`.

### Change 3: Q18 stays at "not yet"

- Status: APPLIED
- Before: step 3 "Q18 stays open and unanswered".
- After: step 3 quotes Q18's recommended "not before observer release R4 or an owner statement that a TUIBBS screen is planned" (`merged-requirements.md:545`) and says this answer is not such a statement and does not change Q18. "What stays unresolved" now lists "Q18 (at its recommended "not yet")".
- Provenance tag: noted in "What happens next" and "What stays unresolved" source comments (Variant 1, C-004).
- Validation: quotation matches `question.md` line 38 and `variant-1-original.md` step 4.

### Change 4: owner sees the exact line before posting; line names the #409 dashboard

- Status: APPLIED
- Before: step 2 "CO-01 carries that shorter line in the Coder#477 reply"; no Coder-side panel note.
- After: step 2 says the owner sees the exact line before it is posted because the reply is public in another repository, and that naming "the #409 dashboard" makes a wrong guess visible. "What stays unresolved" adds that a Coder-side panel is not ruled out (Coder#477 lists Coder template files; nobody searched the Coder repository for the phrase; UNVERIFIED).
- Provenance tag: noted in "What happens next" and "What stays unresolved" source comments (debate A-001, A-002).
- Validation: wording matches `debate-transcript.md` line 33 and `refactor-plan.md` line 36. UNVERIFIED marker kept.

### Change 5: record the 2026-11-08 Python plus Rich decision

- Status: APPLIED
- Before: "What it unlocks" had no note on #409's Go lineage.
- After: appended bullet: #409's issue body preferred a Go stack "informed by TUIBBS-scp styling and components" (`.dev/issues/409/issue-body.md:25`), but the owner replaced that direction with Python plus Rich on 2026-11-08 (ADJ line 187), and the built observer is a `superclaude` CLI command (ADJ E-01).
- Provenance tag: noted in the "What it unlocks" source comment (debate X-002).
- Validation: citations match `question.md` line 35, `debate-transcript.md` line 50 and `round1-advocate-V2.md` line 31.

### Consistency edits required by the instruction (not separate plan changes)

- "What it costs or risks": all three bullets rewritten to match the new reply line. Bullet 1: the reply states only what is true today. Bullet 2: Q3 still rests on its own merits, because "single-host today" cannot test "the observer stays single-host and TUIBBS is not near" (ADJ line 283; debate C-003). Bullet 3: a re-ask is expected only when observer release R4 or a TUIBBS task package is proposed (base step 4).
- "What stays unresolved": base bullet "Single-host or not, TUIBBS or not, and the transport" split into whether single-host and read-only last beyond today (R4 planned; R3 Decision Desk write behaviour UNVERIFIED, `debate-transcript.md` line 17) and whether a TUIBBS screen ever reads the snapshot plus transport.

## Post-Merge Validation

- Structural integrity: PASS. One H1 title and five H2 sections in the required order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved). Provenance header comments present (Provenance, Base, Merge date). Each section carries a `<!-- Source: ... -->` comment.
- Internal references: PASS. Every cited source (ADJ E-01 line 127, glossary lines 77 and 92, ADJ line 187, ADJ line 283, `merged-requirements.md:545`, `.dev/issues/409/issue-body.md:25`, PRs #503 and #514) appears in `question.md`, a variant, the debate transcript or the plan. No new ids, paths or line numbers introduced.
- New contradictions: NONE FOUND. The reply line says "single-host and read-only today", and the costs and unresolved sections treat those properties as present-tense only, consistent with C-002, X-001 and A-003. Q18 is "not yet" in step 3 and in "What stays unresolved". No sentence states or implies that a TUIBBS screen exists or is planned; the only "planned" wording is inside the quoted Q18 condition and the observer's planned release R4. No em dashes or en dashes.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 5 | 5 | 0 | 0 |
