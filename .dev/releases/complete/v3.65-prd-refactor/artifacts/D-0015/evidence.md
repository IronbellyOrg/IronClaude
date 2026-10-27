# D-0015: Update Internal Cross-References to Use refs/ Paths

## Task: T03.03
## Date: 2026-04-03

---

## Replacement Inventory

| Line (pre-edit) | Old Reference | New Reference |
|---|---|---|
| 421 | `Read the "Agent Prompt Templates" section ... "Synthesis Mapping Table" section ... "Synthesis Quality Review Checklist" section ... "Assembly Process" section ... "Validation Checklist" section ... "Content Rules" section` | Rewritten to reference `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` with specific content descriptions |
| 461 | `codebase research agent prompt from SKILL.md` | `from refs/agent-prompts.md` |
| 463 | `agent prompt ... from SKILL.md` | `from refs/agent-prompts.md` |
| 478 | `web research agent prompt from SKILL.md` | `from refs/agent-prompts.md` |
| 484 | `from Synthesis Mapping Table in SKILL.md` | `from refs/synthesis-mapping.md` |
| 485 | `synthesis agent prompt from SKILL.md` | `from refs/agent-prompts.md` |
| 492 | `Assembly Process steps from SKILL.md ... Content Rules from SKILL.md` | `from refs/validation-checklists.md` (both) |
| 493 | `Validation Checklist from SKILL.md` | `from refs/validation-checklists.md` |
| 509 | `Read the SKILL.md file specified above for agent prompts, PRD template structure, validation checklist, and content rules` | `Read the refs/ files specified above: refs/agent-prompts.md, refs/synthesis-mapping.md, refs/validation-checklists.md` |
| 532 | `references the validation checklist from SKILL.md` | `from refs/validation-checklists.md` |

**Total replacements:** 10 stale references updated across 10 locations.

## Intentionally Preserved References

| Line | Reference | Reason |
|---|---|---|
| 504 | `Step 11 from SKILL.md` | Step 11 (Clean Up Consolidation Sources) remains in SKILL.md at line ~1197. Not extracted content. |
| 552-559 | B13 "What the Task File Must Contain" block | Informational — describes what was baked into the task file during Stage A. Per spec Section 12.2, this is not a stale section reference. |

## Acceptance Criteria Verification

```
grep -c 'Agent Prompt Templates section' src/superclaude/skills/prd/SKILL.md → 0 (PASS)
grep -c 'Synthesis Mapping.*section' src/superclaude/skills/prd/SKILL.md → 0 (PASS, no stale matches)
grep -c 'from SKILL.md' src/superclaude/skills/prd/SKILL.md → 1 (Step 11 only — not stale)
grep -c 'in SKILL.md' src/superclaude/skills/prd/SKILL.md → 0 (PASS)
```

## Result: PASS
All former prose section references to extracted content have been replaced with correct refs/ file paths.
