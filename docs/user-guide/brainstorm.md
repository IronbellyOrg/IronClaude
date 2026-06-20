# Brainstorm Guide

`/sc:brainstorm` v2 transforms an ambiguous topic into a unified requirements specification by combining Socratic dialogue, optional codebase/research enrichment, and parallel adversarial proposal generation via `/sc:adversarial`.

## What Changed in v2

| Concern | v1 | v2 |
|---------|----|----|
| Architecture | Monolithic command file | Thin command + `sc-brainstorm-protocol` skill |
| Proposal generation | Single-agent multi-persona dialogue | N parallel proposals across HAIKU/SONNET/OPUS |
| Merge mechanism | None — dialogue produced one doc | Adversarial debate + scoring + provenance-annotated merge |
| Codebase context | Single Auggie shot | Auto-routed `/sc:analyze` or Auggie quick scan, gated by complexity |
| Research | Mentioned, not wired | Auto-invokes `/sc:research` (light) or `tech-research` (deep) |
| Handoff | Text suggestion only | Flag-gated invocation of `/sc:design`, `/sc:tasklist`, or `/sc:task-builder` |
| MCP servers | sequential, context7, magic, playwright, morphllm, serena, auggie-mcp | sequential, serena, auggie-mcp, tavily |
| Personas | 7-persona auto-activation soup | 3 personas auto-selected per detected domain |

v2 does **not** re-implement debate, scoring, or merge logic — those are delegated to `sc-adversarial-protocol`. v2's value is orchestration.

## Required Input

A topic string. File references via `@<path>` are supported. Empty topic STOPs the command.

```bash
/sc:brainstorm "<topic>"
```

## Syntax

```bash
/sc:brainstorm "<topic>" [--proposals N] [--depth quick|standard|deep] \
  [--strategy systematic|agile|enterprise|auto] \
  [--codebase|--no-codebase] [--research light|deep|none|--no-research] \
  [--personas p1,p2,...] [--models opus,sonnet,haiku] \
  [--blind] [--convergence FLOAT] [--interactive] \
  [--handoff none|design|tasklist|task] [--output DIR] \
  [--dry-run] [--resume-from PATH] [--force-stale]
```

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--proposals` | `3` | Number of parallel proposal variants (2-7). Clamped by `--depth`. |
| `--depth` | `standard` | `quick` (3-5 questions, ~500 tok), `standard` (6-10 questions, ~2K tok), `deep` (10-20 questions, ~5K tok). Pass-through to `/sc:adversarial`. |
| `--strategy` | `auto` | `systematic`, `agile`, `enterprise`, or heuristic-detected from topic. |
| `--codebase` / `--no-codebase` | auto | Force or skip codebase enrichment. Auto-detects for `code`/`architecture`/`incident` domains. |
| `--research` | auto | `light` (Tavily), `deep` (`tech-research` skill), `none`. |
| `--personas` | auto | Override domain-aware persona selection with a literal comma list. |
| `--models` | `opus,sonnet,haiku` | Model aliases rotated across proposals (requires `ANTHROPIC_DEFAULT_*_MODEL` env vars). |
| `--blind` | `false` | Strip model identity before scoring (prevents model bias). |
| `--convergence` | `0.75` | Adversarial convergence threshold for PASS routing. |
| `--interactive` | `false` | Pause for user input at Socratic + adversarial decision points. |
| `--handoff` | `none` | Post-merge action: `none`, `design` (text recommend), `tasklist` (invoke), `task` (invoke task-builder). |
| `--output` | auto | Output directory (default `.dev/brainstorms/<ts>-<slug>/`). |
| `--dry-run` | `false` | Run Waves 0-2B (dialogue + enrichment + agent-spec). Skip adversarial. Print preview. |
| `--resume-from` | — | Resume from a saved `seed-brief.md`. |
| `--force-stale` | `false` | Allow `--resume-from` when domain re-classification differs from saved value. |

**Flag interactions** (enforced in Wave 0):

- `--strategy enterprise` implies `--depth deep` unless overridden.
- `--depth quick` caps `--proposals` at 2.
- `--depth deep` allows up to 7 proposals.
- `--handoff task` requires `task-builder` skill; `--handoff tasklist` requires `sc-tasklist-protocol`. Brainstorm STOPs rather than silently downgrading.

## Behavioral Flow (5 Waves)

1. **Wave 0 — Prerequisites**: validate flags, model env vars, sc-adversarial-protocol skill version, handoff prereqs, create output dir.
2. **Wave 1 — Socratic Dialogue**: depth-tiered question batches → `seed-brief.md` with `topic`/`domain`/`strategy`/`depth` frontmatter.
3. **Wave 2A — Enrichment (partial-OK)**: parallel `/sc:analyze` (codebase), `/sc:research` (light), or `tech-research` (deep). Failures degrade quality but do not abort.
4. **Wave 2B — Agent-Spec Composition**: select personas per domain, round-robin assign models, validate via adversarial parser, run token-budget pre-flight.
5. **Wave 3 — Adversarial Delegation**: invoke `Skill sc-adversarial-protocol` with `--generate spec`. Route by convergence score: ≥0.65 PASS, ≥0.50 PARTIAL, <0.50 FAIL.
6. **Wave 4 — Handoff (flag-gated)**: invoke `/sc:tasklist` or `/sc:task-builder`, or print text recommendation for `/sc:design`.

## Output Artifacts

Per invocation, written to `<output>/`:

```text
seed-brief.md                   # Socratic dialogue synthesis with frontmatter
merged-requirements.md          # Adversarial-merged unified spec
enrichment/
  codebase-context.md           # If domain ∈ {code, architecture, incident}
  research-light.md             # If --research light
  research-deep.md              # If --research deep
adversarial/
  debate-transcript.md
  diff-analysis.md
  base-selection.md
  refactor-plan.md
  merge-log.md
  merged-output.md
return-contract.yaml            # Versioned return contract (stable + telemetry)
```

## Examples

### Codebase feature discovery

```bash
/sc:brainstorm "add rate limiting to public API endpoints" --depth standard
```

Auto: codebase enrichment via Auggie; 3 proposals across opus/sonnet/haiku with architect/refactorer/backend personas; adversarial debate + merge.

### Deep incident post-mortem

```bash
/sc:brainstorm "deployment broke staging at 3am" --depth deep --strategy systematic
```

Analyzer/devops personas; 5+ proposals; merge emphasizes observability + rollback strategies.

### Product feature with light research

```bash
/sc:brainstorm "AI-powered changelog summarizer" --strategy agile
```

Tavily research enrichment; architect/frontend/scribe personas; product-style requirements output.

### Cross-domain redesign with full handoff

```bash
/sc:brainstorm "redesign error handling across worker pool" \
  --depth deep --proposals 5 --handoff tasklist
```

Codebase + research enrichment; 5 proposals × 3 models; deep debate; merged requirements feed `sc:tasklist` invocation.

### Blind multi-model comparison

```bash
/sc:brainstorm "consolidate three duplicate auth modules" \
  --depth deep --blind --proposals 4
```

Strips model identity before adversarial scoring to prevent model-bias.

### Dry-run agent-spec preview

```bash
/sc:brainstorm "improve onboarding workflow" --dry-run --strategy enterprise
```

Executes dialogue + enrichment + agent-spec composition; prints the composed `--agents` string and token-budget estimate. Skips adversarial.

### Resume from saved seed brief

```bash
/sc:brainstorm "<topic>" --resume-from .dev/brainstorms/2026-05-25-rate-limit/seed-brief.md
```

Skips Wave 1 dialogue. STOPs if topic re-classifies to a different domain (override with `--force-stale`).

## Convergence Routing

| Score | Routing | Behavior |
|-------|---------|----------|
| ≥ 0.65 | PASS | `merged-requirements.md` copied to output. Proceed to Wave 4. |
| ≥ 0.50 | PARTIAL | Copy with `adversarial_status: partial` frontmatter. Surface caution flag. Proceed to Wave 4. |
| < 0.50 | FAIL | Skip Wave 4. Emit divergence reason. Suggest narrower topic or `--depth deep`. |

## Handoff Targets

| `--handoff` | Action | Skill required |
|-------------|--------|----------------|
| `none` (default) | STOP after `merged-requirements.md` | — |
| `design` | Print recommendation to run `/sc:design` (dialogue-heavy — user invokes manually) | — |
| `tasklist` | Invoke `Skill sc-tasklist-protocol` with `merged-requirements.md` | `sc-tasklist-protocol` |
| `task` | Invoke `Skill task-builder` with domain-detected template | `task-builder` |

Missing handoff skills cause STOP (no silent downgrade) — re-run with a different `--handoff` value.

## Related Commands

| Command | Integration |
|---------|-------------|
| `/sc:adversarial` | Core delegate — Wave 3 invokes via `Skill sc-adversarial-protocol` |
| `/sc:analyze` | Wave 2A enrichment for code-related topics |
| `/sc:research` | Wave 2A light research enrichment |
| `tech-research` (skill) | Wave 2A deep research enrichment |
| `/sc:design` | Wave 4 text-only handoff recommendation |
| `/sc:tasklist` | Wave 4 invoked handoff |
| `/sc:task-builder` | Wave 4 invoked handoff |

## Boundaries

**Will:**

- Transform ambiguous topics into structured seed briefs through Socratic dialogue.
- Orchestrate parallel proposal generation via `/sc:adversarial`.
- Auto-detect and invoke codebase + research enrichment when valuable.
- Compose model × persona agent-specs across 3 active aliases.
- Produce a versioned return contract for composability with downstream commands.

**Will Not:**

- Re-implement adversarial debate, scoring, or merge logic.
- Generate implementation code (use `/sc:implement`).
- Auto-invoke `/sc:design` (text recommendation only — design is dialogue-heavy).
- Silently downgrade on missing handoff skills.
- Modify ANTHROPIC_DEFAULT_*_MODEL environment variables.

## Pipeline Position

```text
topic (user)
   ↓
/sc:brainstorm
   ↓
   ├── enrichment: /sc:analyze | /sc:research | tech-research (optional, parallel)
   ↓
   ├── seed-brief.md (Socratic dialogue output)
   ↓
   ├── /sc:adversarial --source seed-brief.md --generate spec
   ↓
   ├── merged-requirements.md  + 6 adversarial artifacts
   ↓
   └── --handoff:
        ├── none      → STOP (default)
        ├── design    → recommend /sc:design (text only)
        ├── tasklist  → invoke /sc:tasklist
        └── task      → invoke /sc:task-builder
```

## See Also

- [Commands reference](commands.md) — full command catalog
- [Modes guide](modes.md) — Brainstorming mode (`--brainstorm` flag) vs `/sc:brainstorm` command
- Source: `src/superclaude/commands/brainstorm.md` + `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
- Spec: `.dev/eval-workspaces/sc-brainstorm/SPEC.md`
