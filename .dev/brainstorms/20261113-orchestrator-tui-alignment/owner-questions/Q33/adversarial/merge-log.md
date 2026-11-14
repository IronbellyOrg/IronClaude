# Merge Log: Q33

## Metadata
- Base: Variant 1 (proposal-A), `adversarial/variant-1-original.md`
- Executor: merge-executor agent
- Changes applied: 4 of 4
- Status: success
- Timestamp: 2026-11-14
- Output: `merged-output.md`

## Changes Applied

### Change 1: Written brief for the named author
- **Status**: Applied
- **Source**: Variant 2, U-002 ("What happens next" second bullet and "What it unlocks")
- **Target**: "What happens next if the owner picks it", inserted as the second bullet (after the "owner names the session" bullet)
- **Before**: Three bullets: owner names the session; push sequence; never attaches `/sc:pr-submit`.
- **After**: New second bullet, text taken verbatim from the plan's Integration point: "The coordinator gives the named session a short written brief that quotes the 6.3 '#539 author' row, rule 15 (named-path staging), Q28's limits, the A-004 limit (no new key, file or sidecar) and the fork rule (every push and `gh` call to `IronbellyOrg/IronClaude` only). An independent reviewer checks each push against it."
- **Provenance tag**: `<!-- Source: Variant 2, U-002 (refactor-plan Change 1) -->`
- **Validation**: Bullet list intact; no heading change; no em or en dashes.

### Change 2: Condition on role mixing and a fallback
- **Status**: Applied (two parts)
- **Source**: round1-advocate-1.md Concessions; round1-advocate-2.md Position and Concessions
- **Target**: "Answer" (one sentence appended) and "What it costs or risks" third bullet (replaced)
- **Before (Answer)**: Two sentences ending "...with each push and thread resolve under its own grant row."
- **After (Answer)**: Plan sentence appended verbatim: "If that session also does program or coordinator work in this checkout, that work moves to the coordinator home (Q26) before the first #539 push; if the owner cannot identify the session, a fresh dedicated top-level session is launched instead (that Orca allows a second launch in this worktree is UNVERIFIED)."
- **Before (risk bullet 3)**: "If that session is also the one coordinating this alignment work, it mixes two roles in the checkout the spec says the coordinator never runs in (line 951). The owner would then need to move the coordinator elsewhere (Q26)."
- **After (risk bullet 3)**: "If that session is also the one coordinating this alignment work, it mixes two roles in the checkout the spec says the coordinator never runs in (line 951). The condition in "Answer" moves that work to the coordinator home (Q26) before the first push."
- **Executor wording note**: The plan gave no text for the replacement bullet. The first sentence (the risk) is kept unchanged; only the second sentence is replaced so it points to the new condition in "Answer". It reuses the Answer's own terms ("coordinator home (Q26)", "before the first push") so no new claim is introduced.
- **Provenance tags**: Answer section tag names Change 2; `<!-- Source: refactor-plan Change 2 (replaces base third bullet) -->` before the replaced bullet.
- **Validation**: Answer and risk bullet now agree on where the work goes (Q26) and when (before the first push). Fallback sentence keeps the UNVERIFIED marker on Orca behaviour.

### Change 3: Owner reads each diff before its push grant
- **Status**: Applied
- **Source**: round1-advocate-1.md Key strengths 5; round1-advocate-3.md Overall (Variant 3 middle course)
- **Target**: "What happens next if the owner picks it", inserted immediately after the push sequence bullet
- **Before**: Push sequence bullet followed directly by the `/sc:pr-submit` bullet.
- **After**: New bullet between them, verbatim from the plan: "Before writing each push grant, the owner reads the diff it would publish."
- **Provenance tag**: `<!-- Source: Variant 3 middle course, round1-advocate-1.md Key strengths 5 and round1-advocate-3.md Overall (refactor-plan Change 3) -->`
- **Validation**: Placement follows the plan's order (after the push sequence). Consistent with "The owner merges" and the per-push grant rows.

### Change 4: Record the reading of "tool"
- **Status**: Applied
- **Source**: diff-analysis A-001; all three advocates
- **Target**: "What stays unresolved", new third bullet
- **Before**: Two bullets (same-session question; successor if the session ends).
- **After**: New bullet, verbatim from the plan: "The ledger row naming the author records the owner's reading that '6.3: never lets a tool design or push an INV-008 fix' refers to automated tooling such as `/sc:pr-submit`, not the author writing the change the ruling specifies."
- **Provenance tag**: `<!-- Source: diff-analysis A-001, all three advocates (refactor-plan Change 4) -->`
- **Validation**: Does not describe how the INV-008 fix is written; only records which reading of "tool" the owner confirms.

## Post-Merge Validation

### Structural Integrity
- One H1 (title, unchanged) and the base's five H2 headings in base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. No headings added, removed or renamed. No skipped levels.
- Provenance header (3 comments) at top; a `<!-- Source: ... -->` tag before each section and before each changed block.
- Scan for em dash and en dash characters: none found.
- Status: PASS

### Internal References
- References in the merged text: Q1, Q26, Q28, SW-01, SW-02, SW-03, SW-05, spec 6.2, 6.3, 6.4 rules 12 and 15, line 951, A-001 (recorded as reading only), A-004, U-002 (provenance only), INV-008, the "Answer" section (from risk bullet 3). All are carried from the base or the plan's Integration point text; the one new internal pointer ("Answer") resolves to an existing heading.
- External cross-document references (Q26, Q28, spec lines) were not re-verified against their source files; they are unchanged from the base and plan.
- Status: PASS

### Contradiction Re-Scan
- Answer condition vs risk bullet 3: consistent (both send coordinator work to Q26 before the first push). PASS.
- Change 1 (independent reviewer checks each push) vs Change 3 (owner reads each diff before its grant): complementary, not conflicting. PASS.
- Change 4 vs "never lets a tool design or push an INV-008 fix": a clarification of the same rule, not a contradiction. PASS.
- Tension (flagged, not resolved): the Answer's fallback ("a fresh dedicated top-level session is launched instead") sits against "What it unlocks" bullets 1 and 3 ("a named actor with no new session"; "it adds no agent", spec 6.2). These benefits hold only on the main path, not the fallback. The fallback also depends on UNVERIFIED Orca behaviour that may conflict with spec 6.2's "one worktree never holds two live agents" if the original session is still live. The plan lists no change to "What it unlocks", so the executor did not edit it; the orchestrator may want a follow-up wording change.
- Status: PASS with one flagged tension

## Summary
All 4 planned changes were applied in plan order to a copy of Variant 1. Changes 1, 3 and 4 and the Answer part of Change 2 use the plan's Integration point text verbatim; the replaced risk bullet keeps its original risk sentence and swaps only the follow-on sentence for a pointer to the Answer condition. The base's five headings are preserved, and the document has no em or en dashes. One tension was introduced by the Change 2 fallback (new session vs "no new session" benefits) and is reported for the orchestrator, not fixed.
