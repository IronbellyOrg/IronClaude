# Release Guide — Authoring Instructions

Instructions for creating consistent, comprehensive release guides for SuperClaude components (CLI tools, skills, commands, agents).

---

## When to Write a Release Guide

Create a release guide when:
- A new CLI subcommand group ships (e.g., `superclaude roadmap`, `superclaude sprint`)
- A new skill ships or an existing skill undergoes major refactoring (e.g., `/prd`, `/tdd`)
- A component's architecture changes significantly enough that existing documentation is misleading

Do NOT create a release guide for:
- Minor bug fixes or incremental improvements
- Internal refactors that don't change the user-facing surface
- Components covered by inline documentation or `--help` output alone

---

## File Naming Convention

```
docs/guides/[component-name]-release-guide.md
```

Examples:
- `roadmap-cli-tools-release-guide.md` — CLI tool group
- `sprint-cli-tools-release-guide.md` — CLI tool group
- `prd-skill-release-guide.md` — Skill
- `tdd-skill-release-guide.md` — Skill

Use the template at `docs/guides/RELEASE-GUIDE-TEMPLATE.md` as the structural starting point.

---

## Mandatory Sections

Every release guide MUST include these 13 sections. The template provides the full structure.

| # | Section | Purpose |
|---|---------|---------|
| 1 | Release Summary | What's included: capability overview, migration notes, architecture, file structure, design decisions |
| 2 | Invocation Reference | How to use: syntax, arguments, options, examples |
| 3 | Pipeline/Architecture | How it works: step/phase breakdown with ASCII diagram |
| 4 | Gates/Validation | Quality assurance: per-gate checklists, enforcement tiers, failure behavior |
| 5 | Output Artifacts | What it produces: directory tree, artifact descriptions |
| 6 | Configuration | Component-specific settings: modes, tiers, content rules, scope classification |
| 7 | Execution Details | Behind the scenes: call path, subprocess/agent management, state, parallelism, errors |
| 8 | End-to-End Workflow | Context: how this component connects to upstream and downstream stages |
| 9 | Performance & Cost | Resource planning: execution time, token consumption, system requirements by configuration |
| 10 | Known Limitations & Gotchas | Non-obvious behaviors: surprising edge cases, traps, workarounds |
| 11 | Troubleshooting | Symptom-based lookup: error -> cause -> fix table |
| 12 | Practical Use Cases | Concrete examples: 8-10 real scenarios with explanations |
| 13 | Quick Reference | Cheat sheet: condensed command/invocation reference |

### Frontmatter (required)

Every release guide MUST begin with YAML frontmatter:

```yaml
---
component: "component-name"
component_version: "4.2.0"
covers_release: "PR #42 or v4.2.0"
last_updated: "2026-04-03"
author: "name or agent"
---
```

This enables staleness detection — when the component version advances past `component_version`, the guide is flagged for review.

---

## Authoring Rules

### Structure
1. **Follow section numbering** — Use the 13-section structure from the template. Subsections within each section are flexible.
2. **Lead with the intro paragraph** — The opening paragraph should list everything the guide covers as a bullet list.
3. **ASCII diagrams for pipelines** — Always include a visual pipeline diagram showing step flow, parallelism, and gates.
4. **Tables over prose** — Use tables for structured data: options, arguments, gates, artifacts, agent types.
5. **Include frontmatter** — Every guide needs the version/date metadata block.

### Content
6. **Source from code, not memory** — Read the actual source files before documenting. Verify file paths exist.
7. **Include every option** — The command reference must document all CLI options or input parameters, not just common ones.
8. **Show full examples** — Include a "production-quality" example combining multiple options for each command.
9. **Document failure modes** — Explain what happens when gates fail, agents error, or sessions are interrupted.
10. **Cross-reference related guides** — If this component feeds into or consumes from another, reference its guide.
11. **Include migration notes** — If this replaces or refactors a prior version, document what changed, what broke, and what to do.
12. **Document gotchas** — Surface non-obvious behaviors prominently in Section 10 rather than burying them in technical sections.
13. **Add troubleshooting entries** — Include at least 6 symptom->cause->fix entries based on known failure modes.
14. **Estimate performance** — Include wall-time and resource expectations so users can plan.

### Style
15. **Imperative descriptions** — "Loads a specification file" not "This command loads a specification file".
16. **Code blocks for all commands** — Every invocation example in a fenced code block with a comment header.
17. **Consistent heading hierarchy** — H1 for title, H2 for numbered sections, H3 for subsections, H4 for sub-subsections.
18. **No orphaned context** — Every acronym, agent type, or configuration option should be defined where first used.

---

## Adapting the Template by Component Type

### CLI Tool Groups (`superclaude <group> <subcommand>`)
- Section 2: One subsection per subcommand with full `| Option | Type | Default | Description |` tables
- Section 3: Focus on step-by-step pipeline with timeout budgets and gate tiers
- Section 7: Include subprocess command construction, input embedding strategy, output sanitization
- Section 9: Include per-step timeout budgets aggregated into total runtime estimates
- Section 10: Focus on flag interactions (e.g., `--no-validate` doesn't skip spec-fidelity)
- Section 13: Cheat sheet organized by subcommand

### Skills (`/skill-name`)
- Section 2: Single invocation method with input requirements table (not CLI options)
- Section 3: Focus on phases with agent types and parallel execution strategy
- Section 4: Focus on QA gates with checklist items and fix cycle limits
- Section 7: Include task file mechanics, agent spawning, resumability
- Section 9: Include agent count and wall-time by tier (Lightweight/Standard/Heavyweight)
- Section 10: Focus on input quality requirements, scope classification edge cases
- Section 13: Key behaviors and quality guarantees as bullet lists

### Commands (`/sc:command-name`)
- Section 2: May have flags/modes passed as arguments
- Section 3: Focus on behavioral flow stages
- Section 7: Simpler — often single-session execution without subprocess management
- Section 9: Typically brief — single-session commands have predictable performance
- Section 10: Focus on argument interpretation edge cases
- Section 13: Brief — often a single invocation pattern

---

## Quality Checklist

Before finalizing a release guide, verify:

**Structure:**
- [ ] YAML frontmatter present with component, version, date, author
- [ ] All 13 sections present and populated
- [ ] Opening paragraph lists all topics covered
- [ ] ASCII pipeline diagram included in Section 3
- [ ] Consistent heading hierarchy (H1 -> H2 -> H3 -> H4)

**Completeness:**
- [ ] Every CLI option or input parameter documented in Section 2
- [ ] Every output artifact listed in Section 5 with source step/phase
- [ ] At least 6 practical use cases in Section 12
- [ ] At least 4 gotchas in Section 10
- [ ] At least 6 troubleshooting entries in Section 11
- [ ] Performance estimates for all tiers/modes in Section 9
- [ ] End-to-end workflow shows upstream and downstream connections

**Accuracy:**
- [ ] All file paths verified against actual repo structure
- [ ] No placeholder text (`[TODO]`, `[TBD]`, `...`)
- [ ] Migration notes included if this replaces a prior version
- [ ] Cross-references to related guides are valid
