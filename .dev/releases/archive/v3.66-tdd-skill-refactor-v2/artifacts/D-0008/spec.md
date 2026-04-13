# D-0008: Prompt Examples Migration Evidence

**Task:** T03.01 -- Migrate Prompt Examples from SKILL.md to Command File
**Date:** 2026-04-05
**Source:** `src/superclaude/skills/tdd/SKILL.md` lines 48-63 (D-0004 baseline)
**Target:** `src/superclaude/commands/tdd.md` Examples section

---

## Migration Summary

16 lines of Effective Prompt Examples (3 strong + 2 weak) migrated from SKILL.md to the command file's Examples section under a new "Prompt Quality Guide" subsection. All examples adapted to `/sc:tdd` invocation syntax with appropriate flags.

## Adaptation Details

| # | Type | Original (natural language) | Adapted (command syntax) |
|---|------|---------------------------|-------------------------|
| 1 | Strong | "Create a TDD for the agent orchestration system..." | `/sc:tdd "agent orchestration system" --from-prd ... --focus ... --output ...` |
| 2 | Strong | "Turn the canvas roadmap PRD into a TDD..." | `/sc:tdd "canvas roadmap" --from-prd ... --tier standard --focus ...` |
| 3 | Strong | "Design the technical architecture for a shared GPU pool..." | `/sc:tdd "shared GPU pool" --tier heavyweight --focus ...` |
| 4 | Weak | "Create a TDD for the wizard." | `/sc:tdd "wizard"` |
| 5 | Weak | "Write a technical design document." | `/sc:tdd` |

## Verification: Distinctive String Grep Results

| Example | Distinctive String | Grep Match (line) | Status |
|---------|-------------------|-------------------|--------|
| Strong 1 | `agent orchestration system` | Line 97 | FOUND |
| Strong 2 | `canvas roadmap` + PRD path | Line 105 | FOUND |
| Strong 3 | `shared GPU pool` | Line 112 | FOUND |
| Weak 1 | `topic only (will work but produces broader, less focused results)` | Line 116 | FOUND |
| Weak 2 | `no context (agents won't know what to focus on)` | Line 121 | FOUND |

## Acceptance Criteria Checklist

- [x] All 3 strong example distinctive strings found in `src/superclaude/commands/tdd.md` Examples section
- [x] All 2 weak example distinctive strings found in `src/superclaude/commands/tdd.md` Examples section
- [x] Examples adapted to use `/sc:tdd` command invocation syntax
- [x] Content derived from SKILL.md lines 48-63 baseline snapshot (D-0004)
