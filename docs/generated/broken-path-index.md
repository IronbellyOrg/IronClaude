# Broken Template Path Index

Generated: 2026-04-03

## Summary

Two categories of broken paths found across active skill files (excluding `.dev/`, `docs/generated/`, and historical artifacts):

| Wrong Path | Correct Path | Occurrences |
|-----------|-------------|-------------|
| `docs/docs-product/templates/prd_template.md` | `src/superclaude/examples/prd_template.md` | 22 |
| `docs/docs-product/templates/tdd_template.md` | `src/superclaude/examples/tdd_template.md` | 10 |
| `.gfdoc/templates/02_mdtm_template_complex_task.md` | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 6 |
| `.gfdoc/templates/01_mdtm_template_generic_task.md` | `.claude/templates/workflow/01_mdtm_template_generic_task.md` | 6 |

**Note**: `.claude/templates/documents/` also contains copies of `prd_template.md` and `tdd_template.md`. The `src/superclaude/examples/` copies are the canonical source-of-truth per project conventions.

---

## Category 1: `docs/docs-product/templates/` (does not exist)

### PRD Skill — src/superclaude/skills/prd/SKILL.md (10 occurrences)
| Line | Context |
|------|---------|
| 12 | `docs/docs-product/templates/prd_template.md` — description |
| 127 | Template schema table row |
| 368 | GOAL prompt template |
| 464 | "Read the PRD template at..." |
| 713 | Template reference |
| 848 | Section headers match check |
| 874 | Template path reference |
| 925 | Template reference |
| 993 | Final PRD template reference |
| 1135 | Template section headers validation |

### PRD Skill — src/superclaude/skills/prd/refs/agent-prompts.md (4 occurrences)
| Line | Context |
|------|---------|
| 150 | Template reference |
| 285 | Section headers match check |
| 311 | Template path reference |
| 362 | Template reference |

### PRD Skill — src/superclaude/skills/prd/refs/synthesis-mapping.md (1 occurrence)
| Line | Context |
|------|---------|
| 12 | Final PRD template reference |

### PRD Skill — src/superclaude/skills/prd/refs/validation-checklists.md (1 occurrence)
| Line | Context |
|------|---------|
| 15 | Template section headers match validation |

### PRD Skill — src/superclaude/examples/prd_template.md (1 occurrence)
| Line | Context |
|------|---------|
| 1318 | `template_schema_doc` self-reference |

### TDD Skill — src/superclaude/skills/tdd/SKILL.md (2 occurrences)
| Line | Context |
|------|---------|
| 12 | `docs/docs-product/templates/tdd_template.md` — description |
| 125 | Template schema table row |

### TDD Skill — src/superclaude/skills/tdd/refs/build-request-template.md (2 occurrences)
| Line | Context |
|------|---------|
| 80 | "Read the TDD template at..." |
| 114 | BUILD_REQUEST template reference |

### TDD Skill — src/superclaude/skills/tdd/refs/agent-prompts.md (4 occurrences)
| Line | Context |
|------|---------|
| 150 | Template reference |
| 286 | Section headers match check |
| 312 | Template path reference |
| 361 | Template reference |

### TDD Skill — src/superclaude/skills/tdd/refs/synthesis-mapping.md (1 occurrence)
| Line | Context |
|------|---------|
| 5 | Final TDD template reference |

### TDD Skill — src/superclaude/skills/tdd/refs/validation-checklists.md (1 occurrence)
| Line | Context |
|------|---------|
| 9 | Template section headers match validation |

### TDD Skill — src/superclaude/skills/tdd/refs/operational-guidance.md (1 occurrence)
| Line | Context |
|------|---------|
| 82 | Template schema table row |

### Release Guides (docs/guides/) — informational, non-runtime (2 occurrences)
| File | Line | Context |
|------|------|---------|
| docs/guides/prd-skill-release-guide.md | 73 | Template conformance description |
| docs/guides/tdd-skill-release-guide.md | 81 | Template conformance description |
| docs/guides/tdd-skill-release-guide.md | 687 | Template conformance checking |

---

## Category 2: `.gfdoc/templates/` (does not exist)

### PRD Skill — src/superclaude/skills/prd/SKILL.md (2 occurrences)
| Line | Context |
|------|---------|
| 520 | MDTM complex task template reference |
| 521 | MDTM generic task template reference |

### TDD Skill — src/superclaude/skills/tdd/refs/build-request-template.md (2 occurrences)
| Line | Context |
|------|---------|
| 133 | MDTM complex task template reference |
| 134 | MDTM generic task template reference |

### Tech-Research Skill — .claude/skills/tech-research/SKILL.md (2 occurrences)
| Line | Context |
|------|---------|
| 438 | MDTM complex task template reference |
| 439 | MDTM generic task template reference |

**Note**: tech-research has no `src/superclaude/skills/tech-research/` source copy — only exists in `.claude/skills/`.

---

## Category 3: `.claude/` dev copies (mirrors of src/ — will be fixed by `make sync-dev`)

These are exact mirrors of the src/ files above. They do NOT need separate fixes — `make sync-dev` will propagate src/ changes:

- `.claude/skills/prd/SKILL.md` — mirrors src/superclaude/skills/prd/SKILL.md
- `.claude/skills/prd/refs/agent-prompts.md` — mirrors src refs
- `.claude/skills/prd/refs/synthesis-mapping.md` — mirrors src refs  
- `.claude/skills/prd/refs/validation-checklists.md` — mirrors src refs
- `.claude/skills/tdd/SKILL.md` — mirrors src/superclaude/skills/tdd/SKILL.md
- `.claude/skills/tdd/refs/*` — mirrors src refs

**Exception**: `.claude/skills/tech-research/SKILL.md` has NO src/ mirror and must be edited directly.

---

## Files explicitly EXCLUDED from fix scope

These are historical/artifact files that reference the broken paths but are not runtime-affecting:
- `docs/generated/qa-tdd-skill-refactor.md` — QA report (documents the issue)
- `.dev/releases/**` — release pipeline artifacts
- `.dev/tasks/**` — research notes and task files
- `.claude/agent-memory/**` — agent memory files
- `.dev/releases/backlog/prd-skill-refactor/qa-intra-task-report.md` — QA report

## Correct Path Mapping

| Wrong | Correct |
|-------|---------|
| `docs/docs-product/templates/prd_template.md` | `src/superclaude/examples/prd_template.md` |
| `docs/docs-product/templates/tdd_template.md` | `src/superclaude/examples/tdd_template.md` |
| `.gfdoc/templates/02_mdtm_template_complex_task.md` | `.claude/templates/workflow/02_mdtm_template_complex_task.md` |
| `.gfdoc/templates/01_mdtm_template_generic_task.md` | `.claude/templates/workflow/01_mdtm_template_generic_task.md` |
