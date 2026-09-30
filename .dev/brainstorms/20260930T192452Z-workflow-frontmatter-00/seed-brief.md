---
topic: "Changes needed in /sc:workflow command + sc-workflow-protocol SKILL + refs to accommodate new template-00 frontmatter fields (version, priority, created_date) and 8 new builder-comment rules"
domain: code
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: 2026-09-30T19:24:52Z
---

# Seed Brief: workflow-frontmatter-00

## Problem Statement

`src/superclaude/templates/workflow/00_mdtm_template_simple_task.md` (template 00) just gained a YAML frontmatter block (`version: ""`, `priority: "[High | Medium | Low]"`, `created_date: "YYYY-MM-DD"`) and 8 builder rules in its HTML comment (requirement coverage, no fabrication, self-contained tasks, no read-only / verify-only / bulk tasks, enumerate multi-item work, criteria stay inside tasks). But `/sc:workflow` never uses template 00: its Wave 2 writes `plan.md` from `03_project_plan_template.md` headings and says "Do not copy MDTM 00–02", and its gate only knows the frontmatter keys `schema/source/strategy/depth/slug`. So the new fields and rules never reach a generated plan. What is the smallest set of edits so they do?

## Known Context

- Command `src/superclaude/commands/workflow.md` (82 lines) only parses flags and activates `Skill sc:workflow-protocol`; it owns no plan format.
- `SKILL.md:40-44` Wave 2: plan.md body = 03 headings (`## Project Goal`, `## Project Context`, `## Phases`); "Do not copy MDTM 00–02".
- `refs/quality-gates.md:3-13`: required frontmatter `schema: workflow-plan/1.0`, `source`, `strategy`, `depth`, `slug`; body headings from 03; schema-min forbids `- [ ]` task items.
- `refs/return-contract.md`, `refs/input-parse.md`, `refs/phase-templates.md`, `refs/overlap-routing.md`: no frontmatter-field or template-00 content.
- `/sc:implement` (`sc-implement-protocol/SKILL.md:59-69`) enumerates only checkboxes, numbered items / `R-NNN` / `T-NNN`, and `## Task N` / `### T1` headings; ignores MDTM fields; zero enumerable items → T1 = whole document (SKILL.md:67). A 03-style plan (`### Phase N` + `- **Goal**:` bullets) therefore runs as ONE task.
- Template 00 is shaped for `/sc:implement` (`## Task N` headings, `Acceptance criteria:` blocks, `## Constraints`).
- Nothing in `src/` or `tests/` references template 00; `tests/commands/test_workflow_command.py` only checks activation, refs existence, `mcp-servers: []`.
- A plugin mirror exists at `plugins/superclaude/skills/sc-workflow-protocol/` and `plugins/superclaude/commands/workflow.md`; `.claude/` is sync-dev output (never staged).
- Gap review `.dev/workflow-v3-gap-review-2/final.md` ranked the 8 rules; frontmatter fields scored V=1 (not read by /sc:implement).

## Constraints

- Minimal scope: markdown protocol edits only; no Python runtime, no new flags unless unavoidable.
- `src/superclaude/` is source of truth; mirror via `make sync-dev` (+ plugin tree); never stage `.claude/`.
- Must not break `/sc:implement` enumeration (no checkboxes / numbered steps in plan body) or the existing Wave 3 gate / `E-GATE` contract.
- `tests/commands/test_workflow_command.py` must keep passing; add at most a small guard test.
- Keep `return-contract.yaml` 1.0 backward compatible.

## Success Criteria

- A plan written by `/sc:workflow` contains `version`, `priority`, `created_date` in its frontmatter with defined fill rules (who sets each value, from what).
- Wave 3 gate states whether the new keys are required and how they are validated.
- The 8 builder rules reach the writer of plan.md (either via template 00 or restated in the protocol).
- Every edit is a named file + exact change; no orphan references (template path, heading names) left inconsistent between SKILL, refs, plugin mirror and tests.

## Open Questions

1. Keep the 03 body and only extend frontmatter (smallest diff), or switch Wave 2 to render template 00 (Task headings that /sc:implement can enumerate, rules come for free) — and if switching, how to reconcile the 03-heading gate?
2. Fill rules: `created_date` = run date (UTC)? `version` = plan revision (start "1")? `priority` = from source if stated, else `Medium`, or a new `--priority` flag?
3. Are the new keys required at schema-min (quick) or only full (standard/deep)? Does `schema: workflow-plan/1.0` need a bump to 1.1?
4. Should `return-contract.yaml` echo any of the new fields, or stay unchanged?

## Enrichment Context

Source: `enrichment/codebase-context.md` (codebase, quality_tier: primary). Research: skipped (`--no-research`).

- Current plan.md has zero `/sc:implement`-enumerable items (03 body = `### Phase N` + bold bullets), so `/sc:implement @plan.md` runs the whole plan as one task (SKILL.md:67). Template 00's `## Task N` + `Acceptance criteria:` shape is what `/sc:implement` enumerates and QAs per task.
- Plugin mirror `plugins/superclaude/{commands/workflow.md,skills/sc-workflow-protocol/}` is byte-identical to `src/` today and must be kept so; no plugin copy of templates.
- Only guard test: `tests/commands/test_workflow_command.py` (activation, refs exist, `mcp-servers: []`).
