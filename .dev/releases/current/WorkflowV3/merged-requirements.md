---
schema: merged-requirements/1.0
topic: sc-workflow-v3-command-skill-ref
base: variant-1-opus-architect
convergence: 0.82
adversarial_status: pass
created: 2026-09-30
---

<!-- Provenance: /sc:adversarial. Base V1; YAGNI from V2; STOP/paths from V3. -->

# Merged Requirements: `/sc:workflow` v3 (command + skill + refs)

## 1. Product

`/sc:workflow` produces a **phased implementation plan** from a PRD, spec, feature brief, or inline prompt.

Default artifact: `.dev/workflow/<slug>/plan.md`
Not: code, MDTM task files, Sprint `tasklist-index.md`, or `roadmap.md`.

```
source → /sc:workflow → plan.md + return-contract.yaml
         --handoff none      → print next steps
         --handoff design    → print `/sc:design @plan.md` (do not invoke)
         --handoff implement → Skill sc:implement-protocol with plan.md
         --handoff tasklist  → text only: tell user to run /sc:tasklist on a roadmap; do NOT invoke on plan.md
```

## 2. Problem (evidence, condensed)

Current `src/superclaude/commands/workflow.md` is a monolith: no Activation, no skill, Behavioral Flow includes **Execute** while CRITICAL BOUNDARIES say plan-only, dead `morphllm`, unused magic/playwright, seven unused personas, depth `shallow|normal`, ghost `--validate`, undefined `--parallel`, output `claudedocs/`. Gold peers: `implement.md` + `sc-implement-protocol`, `brainstorm.md` + `sc-brainstorm-protocol`. Guide: command = flags; skill = waves+refs; agents only for real work.

## 3. Non-goals

- Implement / test / mutate product code (`/sc:implement`).
- Sprint bundles (`/sc:tasklist`) or `superclaude roadmap run`.
- Fork MDTM `00/01/02/99`; those stay Rigorflow.
- New `src/superclaude/agents/*`.
- Python CLI, resume/ikey, ledger, `deps.yaml`.
- MCP entries for servers waves do not call.
- `--overlap` user flag; `--validate`; `--parallel`.

## 4. Component layout

| Piece | Path | Owns |
|-------|------|------|
| Command | `src/superclaude/commands/workflow.md` | 80–150 lines: flags, usage, examples, boundaries, Activation |
| Skill | `src/superclaude/skills/sc-workflow-protocol/SKILL.md` | Waves 0–5, allowlist, execution vocab |
| Refs | `.../refs/` | Loaded per wave (see FR-003) |
| Agents | none | Single-orchestrator skill. No Task fan-out in v3. |
| Templates | **reference** `src/superclaude/templates/workflow/03_project_plan_template.md` headings | Do not copy into skill |

## 5. Functional requirements

### FR-001 Thin command
`workflow.md` 80–150 lines. Sections: frontmatter, Triggers, Required Input, Usage, Options, Behavioral Summary (no wave steps), Examples, Boundaries, Related Commands, Activation. **Fail if** Analyze/Plan/Execute/Validate remains as executable protocol.

### FR-002 Activation
Blocking: `Skill sc:workflow-protocol`. Protocol SoT: `src/superclaude/skills/sc-workflow-protocol/SKILL.md`. **Fail if** a plan can be produced from the command file alone.

### FR-003 Skill + five refs
```
sc-workflow-protocol/SKILL.md
  refs/input-parse.md      # source kinds, STOP table, slug, E-LEGACY
  refs/phase-templates.md  # strategy skeletons + phase/dep fields
  refs/overlap-routing.md  # vs implement/tasklist/roadmap
  refs/quality-gates.md    # Wave 4 checks + plan.md schema
  refs/return-contract.md  # yaml 1.0
```
Frontmatter: `name: sc:workflow-protocol`, `description`, `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill`. Bash only for mkdir/existence of output dir. **Fail if** STOP codes or phase skeletons live in SKILL.md.

### FR-004 STOP on empty/malformed
| Code | When |
|------|------|
| `E-NO-SOURCE` | bare invoke or two file tokens |
| `E-EMPTY-SOURCE` | whitespace-only file/prompt |
| `E-LEGACY` | `--parallel`, `--validate`, `--depth shallow\|normal` |
| `E-OUTPUT-PATH` | `--output` not under `.dev/workflow/` (or the default root) |
| `E-BAD-FLAG` | unknown enum |
| `E-MISSING-DIR` | `--output` parent missing |

No plan file on STOP.

### FR-005 Source kinds
Exactly one: existing file (`@path` ok) **or** inline prompt. No `--spec/--prd` aliases. Inline prompt persisted to `<run>/source.md` **before** `plan.md`. Slug: `{prefix}-{hash8}` (first 24 slug chars + sha256[:8]).

### FR-006 Depth
`quick|standard|deep`, default `standard`. Legacy depth tokens → `E-LEGACY` with remap hint. `--strategy enterprise` and omitted `--depth` → `deep` + INFO.

| Depth | Phases | Wave 4 |
|-------|--------|--------|
| quick | 2–4 | schema-min |
| standard | 4–8 | full gates |
| deep | 6–12 | full + overlap classifier |

No Task fan-out. One skill session writes the plan.

### FR-007 Strategy is a ref table
`systematic|agile|enterprise`, default `systematic`. No `auto`. Skeletons in `phase-templates.md` only. Fourth strategy = one table row, not a SKILL rewrite.

### FR-008 Waves (Synthesize, never Execute)
| Wave | Name | Ref | Exit |
|------|------|-----|------|
| 0 | Parse | input-parse | flags+source+output dir |
| 1 | Structure | phase-templates | requirements + phases + deps (one pass) |
| 2 | Synthesize | quality-gates (schema) | `plan.md` written |
| 3 | Gate | quality-gates | pass or STOP `E-GATE` |
| 4 | Contract | return-contract, overlap-routing | yaml + handoff text/invoke |

Each wave: purpose, refs, entry, exit, STOP.

### FR-009 plan.md schema
Frontmatter: `schema: workflow-plan/1.0`, source, strategy, depth, slug. Body headings aligned with `03_project_plan_template.md`: Goal, Context, Phases (each: Goal, Inputs, Outputs, Checkpoint, deps). No MDTM checklist items.

### FR-010 Output root
Default `.dev/workflow/<slug>/`. `--output` must remain under `.dev/workflow/`. Forbidden: `.claude/skills|agents|commands`, `claudedocs/`. Writes: `plan.md`, `return-contract.yaml`; `source.md` if inline.

### FR-011 Overlap routing (not a flag)
- Looks like a **roadmap already**: INFO + continue plan; do not run roadmap CLI.
- User asked for **tasklist**: Wave 4 prints `/sc:tasklist --source <roadmap>` ; **do not** invoke skill on `plan.md`; **do not** emit `phase-N-tasklist.md`.
- User asked to **build it**: `--handoff implement` only.

### FR-012 Handoff
`--handoff none|design|implement|tasklist`, default `none`. `design`/`tasklist` = text. `implement` = Skill invoke. Missing implement skill + `--handoff implement` → STOP, no silent skip.

### FR-013 Return contract 1.0
Write `<run>/return-contract.yaml`:
```yaml
contract_version: "1.0"
status: success | partial | failed
plan_path: <path>|null
source_path: <path>
domain: architecture|code|...
strategy: systematic|agile|enterprise
depth: quick|standard|deep
handoff_action: none|design|implement|tasklist
handoff_output_path: <path>|null
unresolved: []
```

### FR-014 Personas / MCP
Command `mcp-servers: []`. Personas: none always-on. `security` never auto. No new agent files.

### FR-015 Sync
Edit `src/superclaude/` only; `make sync-dev`; never stage `.claude/` skill mirrors.

### FR-016 Related-commands section
Command SHALL name implement (execute), tasklist (sprint bundle), roadmap (CLI), design (architecture) with one-line differences.

### FR-017 Tests
At least one pytest or fixture asserting: (1) command file contains `## Activation` and `Skill sc:workflow-protocol`; (2) command does not contain the word-sequence `**Execute**` as a behavioral step; (3) skill directory exists with the five refs. No need to execute the LLM protocol in CI.

## 6. NFRs

- NFR-001 Token: SKILL.md ≤ ~500 lines; refs lazy per wave.
- NFR-002 Safety: skill must not Edit/Write outside `--output` / default `.dev/workflow/`.
- NFR-003 Deterministic STOP codes (stable strings).
- NFR-004 Ponytail: no second task format, no speculative MCP, no unused agents.

## 7. Risks

| Risk | Mitigation |
|------|------------|
| Becomes a third planner | FR-011 / FR-012 |
| Command file grows protocol again | FR-001 fail condition |
| Confuse 03_project_plan with MDTM | FR-009 + non-goals |
| User Step 5 expects tasklist now | Wave 5 text: run `/sc:tasklist` on a roadmap; this command emits plan.md |

## 8. Out of scope (v3)

Resume, ledger, deps.yaml, `--overlap` flag, `--validate` flag, Magic/Playwright/Morphllm/Serena-required, new agents, workflow Python CLI.
