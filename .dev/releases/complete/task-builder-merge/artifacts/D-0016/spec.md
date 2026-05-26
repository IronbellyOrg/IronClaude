# D-0016 — Spec (T02.01 FR-CONV.2 Execution Context Header Wrapper)

**Task:** T02.01 — Land FR-CONV.2 Execution Context header
**Roadmap row:** R-032
**Implementation surface:** `src/superclaude/skills/task-builder/SKILL.md`
- Initial file-write checklist mention: `:867–873` (line 873 reads `- ## Execution Context (OPTIONAL — see EXECUTION CONTEXT BLOCK below)`)
- EXECUTION CONTEXT BLOCK narrative: `:878–940`
- MDTM Output Structure template: `:1707–1722` (Execution Context heading at `:1712`, between `## Prerequisites & Dependencies` at `:1707` and `## Phase 1: [Phase Name]` at `:1722`)

## Deliverables
- FR-CONV.2 wrapper inserted in MDTM template at SKILL.md post-frontmatter, pre-checklist.
- 3-labeled-line block specification (References / Source areas / Key constraints) defined for fully-populated BUILD_REQUEST.
- Per-item Context fields unchanged (scope-confinement rule at `:934–940` explicitly preserves TB-Add-8 evidence-bound-item invariant).

## Acceptance Criteria
- AC1: `grep -n "## Execution Context" <generated-mdtm>` returns the block heading line immediately after frontmatter.
- AC2: Block contains References, Source areas, Key constraints labeled lines for the fully-populated fixture.
- AC3: Per-item Context fields outside the header are unchanged (byte-identical diff outside header range).
- AC4: Evidence at `TASKLIST_ROOT/artifacts/D-0016/evidence.md`.

## Dependencies
- Phase 1 (M1 PASS)
- DM-001 contract-freeze ratified (T01.13 / D-0011 § 1)
