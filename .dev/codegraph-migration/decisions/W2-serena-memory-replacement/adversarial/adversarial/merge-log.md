# Merge Log

## Metadata
- Base: Variant 1 (Option A, `variant-1-original.md`), final score 0.6664
- Plan: `refactor-plan.md` (9 planned changes, 6 rejected alternatives)
- Executor: merge-executor
- Output: `../merged-recommendation.md` (90 lines, 14 `Source` tags)
- Changes applied: 9 of 9
- Status: COMPLETE
- Timestamp: 2026-10-30

## Per-Change Log

### Change #1: Split storage into session state and tracked calibration
- Status: APPLIED
- Before: last sentence of paragraph 1 left an open "or" between `.superclaude/memory/reflect/` and `docs/memory/`
- After: section "Storage layout" - session state in ignored `.superclaude/memory/`; reflect calibration in tracked `docs/memory/reflect/` (created on first write); existing `docs/memory/*.md` untouched
- Provenance: `Base (original, modified) - Change #1 resolves the open "or"`
- Validation: matches plan text and E5/E6

### Change #2: Resolve the project root once
- Status: APPLIED
- Before: no root rule
- After: "Rules / Root" - git top-level of the current directory, current directory outside git; one store per worktree by default
- Provenance: `Variant 1 / advocate and Variant 2 / advocate, Change #2`
- Validation: the plan's pointer "see Changes Not Being Made, item 5" was reworded to "see Open decision" because the merged document has no section with that name (the section exists, item 5 of Rejected alternatives also points to it)

### Change #3: Remove, do not rename, the Serena-only calls
- Status: APPLIED
- Before: "so prompts change by tool name only"
- After: claim removed from the Decision text; new section "Removed, not renamed" lists the `think_about_*`, `summarize_changes`, `activate_project`, `onboarding`, `prepare_for_new_conversation` calls and the empty-`list_memories` gate, with the plain-check example
- Provenance: `Variant 1 / advocate, Variant 2 / advocate and Variant 3 / advocate, Change #3` (Decision section tagged "modified" for the removed claim)
- Validation: names match E1, E9, E10

### Change #4: Concurrent-writer convention
- Status: APPLIED
- Before: none (base cons said only "not shared across worktrees")
- After: "Rules / Concurrency" - single-owner keys overwritten whole; shared keys use `<key>-<session-or-timestamp>.md`, never edited in place
- Provenance: `Variant 1 / advocate, Variant 2 / advocate and Variant 3 / advocate, Change #4`
- Validation: placed as a rule subsection instead of a pros/cons bullet, because the merged document has no pros/cons block beyond the Decision bullets

### Change #5: Guard the ignore rule outside this repo
- Status: APPLIED
- Before: "`.superclaude/` is already gitignored"
- After: "Rules / Ignore guard" - ignored only in IronClaude (`.gitignore:114`, E5); first write creates `<project>/.superclaude/.gitignore` with `*` if absent
- Provenance: `Base (original, modified) - Change #5 restricts ...`
- Validation: line 114 taken from the plan and E5

### Change #6: One-release legacy read fallback
- Status: APPLIED
- Before: `/sc:load` sentence had no fallback
- After: "Rules / Legacy fallback" - reads `.serena/memories/<name>.md` when the new file is absent, never writes there, tells the user it is read-only history; "one release" wording kept
- Provenance: `Base (original, modified) - Change #6 appends to the /sc:load sentence`
- Validation: consistent with A-004

### Change #7: Roadmap needs only a default flip
- Status: APPLIED
- Before: roadmap not named in the base
- After: Consumers table row for sc-roadmap-protocol (`SKILL.md` lines 326, 419, 443)
- Provenance: `Base (original, modified) - ... roadmap row from Change #7`; row text names V3 / advocate
- Validation: lines taken from the plan; also in base-selection.md

### Change #8: Edit inventory for the follow-on work
- Status: APPLIED
- Before: base said "mechanical edit across ~15 primitives"
- After: section "Follow-on edit inventory" (14 files, 121 hits; HOW-WE-WORK lines 237, 327, 329 and its copies; tests with line numbers; crash-recovery lines; docs; written-plan requirement). The "~15 primitives" figure was dropped in favour of the E2 count of 14 files
- Provenance: `Variant 3 / advocate, Change #8`
- Validation: every number appears in the plan or diff-analysis.md

### Change #9: Empty or missing store means "no memory"
- Status: APPLIED
- Before: none
- After: "Rules / Empty store" - missing folder or empty Glob is the normal cold-start state; `--onboard` keys off absence of `memory_maintenance.md`
- Provenance: `Variant 1 / advocate, Change #9`
- Validation: matches plan text

## Rejected alternatives and other required blocks
- Six rejected alternatives written into "Rejected alternatives" (items 1-6 from the plan, in plan order)
- "Open decision" and "Debate result" blocks added as required by the task; the debate figures (0.6664, 0.6540, 0.5825, 89.5%, 17 of 19, S-001 and C-003) are from base-selection.md and debate-transcript.md

## Post-Merge Validation

1. Heading hierarchy: PASS. One H1; H2 sections (Decision, Storage layout, Rules, Removed not renamed, Consumers, Follow-on edit inventory, Rejected alternatives, Open decision, Debate result); five H3 under Rules (Root, Concurrency, Ignore guard, Empty store, Legacy fallback). No level skipped. Checked with a heading grep.
2. Cross-references: PASS. "see Root rule and Open decision", "see Removed, not renamed", "see Open decision" all resolve to existing headings. Named files (`diff-analysis.md`, `debate-transcript.md`, `docs/memory/`, `HOW-WE-WORK.md` copies) come from the plan or the evidence list. One reference was reworded (Change #2, see above). The text was also checked for non-ASCII characters: none.
3. Contradiction re-scan: PASS, no new contradictions.
   - X-001 (Option B worktree sharing): the merged text states the sharing advantage as real (E7) and does not repeat B's wrong claim.
   - X-002 (Option C "no gap"): the merged text states the reflect gap is real and fixed by the tracked calibration file.
   - X-003 (HOW-WE-WORK line 237 as a disclaimer): the merged text treats the routing rows as edits, not as proof of obsolescence.
   - X-004 ("tool name only"): the claim is removed and replaced by the "Removed, not renamed" section.
   - One residual tension checked: the Decision cons say one store per worktree while the calibration file is shared via git; this is stated, not contradictory.
4. Change coverage: PASS. Changes #1-#9 all APPLIED, none skipped.

## Summary
- Planned: 9
- Applied: 9
- Failed: 0
- Skipped: 0
- Notes: two small structure adaptations (Change #4 placed as a rule subsection; Change #2 cross-reference reworded) and one base number replaced (~15 primitives -> 14 files, 121 hits)
