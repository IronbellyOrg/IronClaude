# D-0013: Evidence — Remove Extracted Content Blocks from SKILL.md

**Task:** T03.01
**Date:** 2026-04-03
**Status:** PASS

---

## Removal Inventory

| Block(s) | Original Lines | Content Removed | Corresponding refs/ File |
|-----------|---------------|-----------------|--------------------------|
| B11 | 344-508 (165 lines) | BUILD_REQUEST format, A.7 section header + full template | `refs/build-request-template.md` |
| B14-B21 | 553-967 (415 lines) | Agent Prompt Templates (codebase research, web research, synthesis, assembly, consolidation) | `refs/agent-prompts.md` |
| B22-B23 | 969-1106 (138 lines) | Output Structure + Synthesis Mapping Table | `refs/synthesis-mapping.md` |
| B24-B27 | 1108-1254 (147 lines) | Synthesis Quality Review Checklist + Assembly Process + Validation Checklist + Content Rules table | `refs/validation-checklists.md` |
| **Total** | | **~865 lines removed** | |

## Line Count

- **Before:** 1,373 lines
- **After:** 505 lines
- **Reduction:** 868 lines (63% reduction)
- **Target (before T03.02-T03.04):** ~530 (on track; T03.02 adds loading declarations, T03.04 merges B05/B30 reducing further)

## Retained Behavioral Blocks

All behavioral blocks confirmed intact via section header grep:

| Block | Section | Status |
|-------|---------|--------|
| B01 | Frontmatter + PRD Creator header | INTACT |
| B02 | Why This Process Works | INTACT |
| B03 | Input (4 pieces + examples + incomplete handling) | INTACT |
| B04 | Tier Selection | INTACT |
| B05 | Output Locations | INTACT |
| B06 | Execution Overview | INTACT |
| B07 | Stage A header + A.1 | INTACT |
| B08 | A.2: Parse & Triage | INTACT |
| B09 | A.3-A.6 (Scope Discovery, Research Notes, Sufficiency Gate, Template Triage) | INTACT |
| B10 | Template triage closing statement | INTACT |
| B12 | Spawning the builder instruction | INTACT |
| B13 | A.8 + Stage B + Delegation Protocol + Task File Requirements | INTACT |
| B28 | Critical Rules (Non-Negotiable) — 16 rules | INTACT |
| B29 | Research Quality Signals | INTACT |
| B30 | Artifact Locations | INTACT |
| B31 | Session Management | INTACT |
| B32 | Updating an Existing PRD | INTACT |

## Acceptance Criteria Verification

| Criterion | Result |
|-----------|--------|
| `grep -c 'Assembly Process' SKILL.md` returns 0 | **PASS** (0 matches) |
| `grep -c 'Content Rules' SKILL.md` returns 0 | **PASS** (0 matches) |
| `grep -c 'Agent Prompt Templates' SKILL.md` returns 0 | **PASS** (0 matches) |
| `grep -c 'Output Structure' SKILL.md` returns 0 | **PASS** (0 matches) |
| `grep -c 'Validation Checklist' SKILL.md` returns 0 | **PASS** (0 matches) |
| `grep -c 'Synthesis Mapping' SKILL.md` returns 0 | **PASS** (0 matches) |
| All behavioral blocks present and unmodified | **PASS** |
| Line count significantly reduced from 1,373 | **PASS** (505 lines, 63% reduction) |

## Notes

- BUILD_REQUEST is mentioned 3 times in retained behavioral blocks (lines 194, 259, 347) as informational references — these are correct and expected (they describe what the builder reads, not the template itself)
- Double `---` separator at B13/B28 boundary was cleaned up post-removal
- `refs/build-request-template.md` does not yet exist in `.claude/skills/prd/refs/` — expected to be created by a prior or parallel task (T02.01)
