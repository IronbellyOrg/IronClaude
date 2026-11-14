# Merge Log: Q3 (Coder#477: keep, narrow or close)

## Metadata

- Producer: /sc:adversarial, Step 5 (merge executor)
- Merge date: 2026-11-14
- Base: Variant 1 (proposal-A, narrow), `adversarial/variant-1-original.md`
- Plan: `adversarial/refactor-plan.md` (5 planned changes, overall risk Low, auto-approved 2026-11-14)
- Sources of incorporated text: `adversarial/variant-2-original.md`, `adversarial/variant-3-original.md`
- Context read: `adversarial/debate-transcript.md`, `question.md`
- Output: `merged-proposal.md`
- Rule carried from the plan: the merge does not claim that an orchestrator that manages work, a watcher-to-orchestrator handoff, or a TUIBBS screen exists.

## Changes Applied

### Change 1: name the condition under which close is right instead

- Status: applied
- Target: "Answer", appended sentence
- Before: the Answer stated "narrow" only, with no condition under which another answer applies.
- After: a second paragraph says close (text C with its two reopen conditions) is right instead if the owner states that single-host is lasting and that no TUIBBS screen or remote reader is planned, citing ADJ line 283 and Q18 at `merged-requirements.md:545`. The primary answer stays "narrow".
- Provenance tag: `<!-- Source: ... Variant 3 Answer and reopen conditions, plan Change 1 (debate X-001, X-003, A-003) -->`
- Validation: the condition matches the debate's shared conclusion (transcript, Convergence Assessment) and question.md's spec recommendation ("close if single-host and TUIBBS not near"). Citations are only those the plan names.

### Change 2: say that narrowing replaces the problem statement

- Status: applied
- Target: "What it costs or risks", appended bullet
- Before: four risk bullets; none said that narrowing changes what the issue is about.
- After: a fifth bullet says narrowing in effect replaces the problem statement, because the issue's written body serves only the watcher, so text A is a new problem under the old issue number (debate A-001).
- Provenance tag: `<!-- Source: ... plan Change 2 (debate A-001; V1 advocate concession) -->`
- Validation: matches the transcript's agreed reading of A-001 and the V1 advocate's concession "'narrow' really replaces the problem statement". Note: the plan calls it "concession 6"; the transcript's summary lists it as the fifth concession named. The full statement file `round1-advocate-V1.md` was not read, so the provenance tag names the concession without a number.

### Change 3: grant rows name each write; fix text C's link placeholder for the fallback

- Status: applied
- Target: "What happens next", step 3, plus a new fallback note after step 4
- Before: step 3 named a single `GRANT(CO-01,issue-write)`; nothing addressed text C's placeholder.
- After: step 3 adds that each write gets its own grant row that names it (XC-02 (4)) and that whether `issue-write` covers a state change is UNVERIFIED. A fallback note says that if close is picked under the Answer's condition, text C still holds "[link to the comment holding option A]" (ADJ line 661), so it must be reworded or text A posted first, and the grant row must name the close as a state change.
- Provenance tag: `<!-- Source: ... plan Change 3 (Variant 3 advocate concession 3 and A-002 response) -->`
- Validation: both facts appear in the transcript's "New facts surfaced in the round" and the A-002 agreed reading; XC-02 (4) and the grant form match question.md's facts table. The UNVERIFIED marker is kept.

### Change 4: reconcile "writes nothing" with the per-read audit line

- Status: applied
- Target: "What happens next", step 2 (CO-02), appended sentence
- Before: step 2 listed three placeholders (age, owner-token route, record name).
- After: step 2 adds that CO-02 also reconciles text A's statement that the read route "writes nothing" with its requirement of an audit line per read, as CO-03 (5) already asks.
- Provenance tag: `<!-- Source: ... plan Change 4 (V3 advocate; spec CO-03 (5)) -->`
- Validation: wording follows the plan's rationale only; no new requirement text or line number was added. The source of the conflict (text A in ADJ Part 6.3) was not re-read, so the clause cites CO-03 (5) as the plan does.

### Change 5: text B's guards stay on record

- Status: applied
- Target: "What stays unresolved", appended bullet
- Before: two unresolved items (reader timing, read-permission model).
- After: a third bullet says that if the owner ever revisits the watcher's design decision D1 (`docs/designs/issue-watcher.md:39`), text B in ADJ Part 6.3, with its guards as Variant 2 lists them, is the guarded routing text to start from; nothing is lost by not keeping routing now.
- Provenance tag: `<!-- Source: ... plan Change 5 (Variant 2, U-002, preserved in ADJ Part 6.3) -->`
- Validation: the guard list is copied from Variant 2's Answer. The plan's phrase "a watcher-design revisit condition" was worded as "if the owner ever revisits ... D1", because the V2 advocate states D1 has no recorded revisit condition (transcript, Round 1); this avoids asserting that such conditions are recorded. Routing is not kept, matching the plan's "Changes NOT Being Made" (C-002, X-002).

## Post-Merge Validation

- Structural integrity: one H1 (base title, unchanged) and five H2 sections in the base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. Each section carries a `<!-- Source: ... -->` comment. Provenance header comments are at the top. The numbered steps 1 to 4 are unchanged in count and order; the fallback note sits after step 4 as unnumbered text.
- Internal references: every cited source appears in the plan, a variant or question.md: ADJ line 283, line 606, line 661, Part 6.3; `merged-requirements.md:545`; `docs/designs/issue-watcher.md:39`; XC-02 (4); CO-03 (5); checklist item 9; debate A-001. No new ids, paths or line numbers were introduced. "Text C" and "text B" are defined in question.md's facts table.
- New contradictions: none found. The Answer stays "narrow"; close appears only as the named conditional alternative, and the fallback note is scoped to that condition. "What it unlocks" (aligned as a read-only source) does not conflict with the close condition, which applies only on an owner statement. The UNVERIFIED status of `issue-write` covering a state change is stated consistently in step 3 and the fallback note. No text claims that an orchestrator managing work, a watcher-to-orchestrator handoff, or a TUIBBS screen exists; TUIBBS appears only as planned or not planned.
- Style: plain English; no em dashes or en dashes.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 5 | 5 | 0 | 0 |

Rejected by the plan and not merged: Variant 2's prompt routing with guards (C-002, X-002) and Variant 3's close as the primary answer (C-001). Rollback: revert to `adversarial/variant-1-original.md`.
