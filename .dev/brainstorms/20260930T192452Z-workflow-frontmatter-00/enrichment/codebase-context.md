# Codebase context (Wave 2A, quality_tier: primary — auggie codebase-retrieval ×2 + direct Reads)

## Plan writer (current)
- `src/superclaude/skills/sc-workflow-protocol/SKILL.md:40-44` — Wave 2 writes `<run>/plan.md` with `03_project_plan_template.md` headings (`## Project Goal`, `## Project Context`, `## Phases`); "Do not copy MDTM 00–02".
- `refs/quality-gates.md:3-13` — frontmatter MUST include `schema: workflow-plan/1.0`, `source`, `strategy`, `depth`, `slug`; body headings from 03; each phase Goal/Inputs/Outputs/Checkpoint/deps. Schema-min: keys present, ≥1 phase, no `- [ ]`. Full: + Inputs/Checkpoint per phase, acyclic deps, depth cap, no `.claude/` output paths.
- `refs/phase-templates.md` — strategy skeletons + depth caps only. `refs/input-parse.md` — source/slug/STOP codes. `refs/return-contract.md` — contract 1.0 (no plan-frontmatter echo). `refs/overlap-routing.md` — 10 lines, routing only.
- `src/superclaude/commands/workflow.md` (82 lines) — flags + Activation; says it writes `.dev/workflow/<slug>/plan.md` + `return-contract.yaml`; next step `/sc:implement @plan.md` (line 82).

## Plan consumer
- `sc-implement-protocol/SKILL.md:59-69` — enumerates `- [ ]`, numbered / `R-NNN` / `T-NNN`, `## Task N` / `### T1`; `## Phase N` is a group heading only when it has enumerable children; zero items → T1 = whole document; frontmatter/MDTM fields ignored.
- Consequence: a 03-style plan (`### Phase N` + bold-label bullets) has 0 enumerable items → `/sc:implement` runs it as ONE task (T1 = whole plan).

## Template 00 (edited this session)
- Frontmatter: `version: ""`, `priority: "[High | Medium | Low]"`, `created_date: "YYYY-MM-DD"`.
- Builder comment: 8 new rules (G35/G211 coverage, G81 no fabrication, G40 self-contained, G48 no read-only task, G84 no verify-only task, G36 no bulk, G37 enumerate multi-item, G50 criteria inside tasks).
- Body: `Source:`/`Goal:` lines, `## Constraints`, `## Phase 1`, `## Task N` + `Acceptance criteria:` + `Depends on:`.
- No references to template 00 anywhere in `src/` or `tests/`.

## Mirrors / tests
- Plugin mirror `plugins/superclaude/skills/sc-workflow-protocol/` and `plugins/superclaude/commands/workflow.md` are currently byte-identical to `src/` (manual copy; `scripts/build_superclaude_plugin.py:16` builds from `plugins/superclaude`). No `plugins/superclaude/templates/`.
- `make sync-dev` mirrors skills/commands/templates into `.claude/` (gitignored; never stage). `make verify-sync` is the pre-commit gate.
- `tests/commands/test_workflow_command.py` — 4 guards (Activation, no Execute step, SKILL + 5 refs exist, `mcp-servers: []`).
- Canonical frontmatter parser for CLI gates: `src/superclaude/cli/pipeline/frontmatter.py` (top-level keys only) — not used by `/sc:workflow` (skill-driven, no Python).
