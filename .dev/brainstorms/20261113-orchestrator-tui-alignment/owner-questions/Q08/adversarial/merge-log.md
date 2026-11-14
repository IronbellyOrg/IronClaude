# Merge Log: Q8 merged answer

## Metadata

- Base: `variant-3-original.md` (proposal C)
- Plan: `refactor-plan.md` (4 planned changes, overall risk Low, auto-approved 2026-11-14)
- Incorporated sources: `variant-1-original.md` (proposal A), `variant-2-original.md` (proposal B), C's advocate concessions 1 and 3 as recorded in the plan
- Output: `../merged-answer.md`
- Merge date: 2026-11-14
- Not applied, as the plan directs ("Changes NOT Being Made"): B's amendment of criterion 1; A's "write the record only at release 3".

## Changes Applied

### Change 1: the record covers every field the gate checks, deferring release-3 fields explicitly

- Status: Applied
- Provenance: `[Source: proposal A + C's advocate concession 1]`
- Title. Before: "Proposal C: write the one-paragraph direction-selection record now". After: "Q8 merged answer: write the owner's direction-selection record now, covering every gate field".
- Answer. Before: "The owner writes one dated paragraph, in their own words, naming the staged direction that was chosen, their reading of "production integration" and the command name (`superclaude observe`); #409's acceptance criterion 1 stays as written and is then met by citing that record." After: the paragraph records every gate field from `acceptance-tests.md:70` on `origin/master` (date, option, who decided, where the owner's statement lives, default before questions are observed, default after, post-link choice or deferral, fallback date, stack confirmation, command name, confirmed production-integration reading); the post-link choice and fallback date may be written "deferred to release 3"; criterion 1 stays as written and is met by citing the record.
- What happens next, first bullet. Before: "The owner writes the paragraph in a file at a location of the owner's choosing ...". After: "The owner writes the paragraph, covering every field listed in the Answer, in a file at a location of the owner's choosing ...".
- What it costs or risks. Before: bullet "The gate rule (`release-gates.md:22`) lists more fields than the three this answer names ...; a three-item paragraph may not satisfy the gate as written ...", and first bullet "Owner writing time (one paragraph), ...". After: gate-field bullet removed; replaced by "The paragraph is longer than a three-item note, because it must cover every field the gate checks; two of those fields (the post-link choice and the fallback date) may be written as deferred to release 3." First bullet shortened to "Owner writing time, and the owner must choose where the file lives." so it does not repeat the length point.

### Change 2: an honest status line for #409

- Status: Applied
- Provenance: `[Source: C's advocate concession 3; proposal A on C-002]`
- Before: "(the status line becomes "met by the owner's record of <date>, path")".
- After: "(the status line becomes "direction selected 2026-11-08 (staged); confirmed in the owner's record of <date>, <path>, written after releases 1 and 2 shipped")".

### Change 3: interim line if the record is not written in time

- Status: Applied
- Provenance: `[Source: proposal A, "What happens next" first bullet]`
- Before: no such bullet.
- After (new bullet after the BC-18 bullet): "If the record does not exist when OB-08 posts, BC-18 posts as proposed, with the status line "not met as recorded", instead of being left out as the spec default would do."

### Change 4: cite the earlier decisions as background, not as the record

- Status: Applied
- Provenance: `[Source: proposal B, "What it unlocks" first bullet]`
- Before: "The paragraph can cite the owner's existing decisions (2026-11-08 "Stage it", 2026-11-11), so it is short to write."
- After: "The paragraph may cite the owner's earlier decisions (2026-11-08 "Stage it", 2026-11-11) as background and say that the staged direction chosen then still stands, so the direction part is short to write. The 2026-11-08 file says it was "Recorded by an Orca worker" (its line 3), so it supports the owner-written record but cannot replace it."
- Note: "short to write" narrowed to "the direction part is short to write" so it does not contradict Change 1's longer paragraph.

## Post-Merge Validation

- Heading structure: Pass. One H1 title, then the five H2 sections in the base order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved). No skipped levels. Three provenance header comments at the top and one `Source` comment before each section.
- Internal references resolve: Pass. "every field listed in the Answer" points at the Answer's field list. OB-02, OB-08, OB-09, BC-18, Q7, ADJ A-003 and the file citations (`acceptance-tests.md:70`, `release-gates.md:22`, `merged-requirements.md:250`) are carried from the base or the plan; none was invented.
- Writing rules: Pass. No em dashes or en dashes; no person's name.
- New contradictions introduced: 0. Checked: (1) the Answer's field list against the costs bullet on paragraph length (consistent); (2) "short to write" against the longer paragraph (resolved by narrowing to the direction part); (3) Change 2's met status against Change 3's interim "not met as recorded" line (they apply to different cases: record present or absent when OB-08 posts); (4) the deferred post-link and fallback-date fields against "What stays unresolved", which still asks whether those later choices need a second dated record (consistent: deferral leaves that question open).

## Summary

- Planned: 4
- Applied: 4
- Failed: 0
- Skipped: 0
