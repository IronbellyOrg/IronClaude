---
name: template-notes
description: Template availability in IronClaude and fallback strategy when .gfdoc/templates/ is absent
type: project
---

## Template Availability

The `.gfdoc/templates/` directory (containing `01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md`) does NOT exist in IronClaude. These templates are from a different project (GFxAI).

**Why:** IronClaude is the SuperClaude framework repo. The MDTM templates belong to the GFxAI project. They will never be present here.

**How to apply:** When a BUILD_REQUEST specifies TEMPLATE: 02 and the template file is not found, proceed directly to build the task file from the BUILD_REQUEST specifications. Do NOT block. The tech-research SKILL.md at `.claude/skills/tech-research/SKILL.md` provides all agent prompt templates needed. Read SKILL.md sections: Agent Prompt Templates (line 556), Report Structure (line 969), Synthesis Mapping Table (line 1147), Content Rules (line 1219).
