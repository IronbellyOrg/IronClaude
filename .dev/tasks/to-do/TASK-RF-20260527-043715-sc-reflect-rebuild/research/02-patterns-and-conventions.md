# Research: Patterns & Conventions
**Topic type:** Patterns & Conventions
**Scope:** sc-troubleshoot-protocol + sc-brainstorm-protocol skill conventions
**Status:** Complete
**Date:** 2026-05-27

---

## Summary

The two existing protocol skills (`sc-troubleshoot-protocol`, `sc-brainstorm-protocol`) form a **band, not a single template**. They share core conventions (parsed frontmatter, on-demand refs, Will/Will Not, Activation gate, command<->skill bidirectional link) but diverge sharply on body shape: troubleshoot is **prose-dense, wave-numbered, table-driven**; brainstorm is **section-numbered (§1-§7), more terse, "Execution Vocabulary"-typed**. Reflect's spec §13.2 explicitly says "keep within the band" — so reflect can pick from either side per section, but should declare which convention it inherits for each major axis.

The two skills also disagree on **how `version:` lives in frontmatter** (brainstorm has it inside HTML comment; troubleshoot omits it entirely). Reflect needs to pick deliberately — Researcher 06 should pin which to mirror.

Below: every convention with `file:line` citations, plus EXACT phrasing to mirror.

---

## 1. SKILL.md Frontmatter Shape

### 1.1 sc-troubleshoot-protocol (`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:1-5`)

```yaml
---
name: sc:troubleshoot-protocol
description: "Tiered debugging protocol — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate in Tier 2, and an opt-in task-builder remediation chain in Tier 3. Use this skill whenever the user reports a broken build, runtime error, performance regression, deployment problem, or failing test, even when they don't explicitly say 'troubleshoot' — phrases like 'why is X broken', 'this used to work', 'something's off with...', a pasted stack trace, or a failing-command transcript should all activate it."
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
---
```

Followed (line 7-12) by HTML-comment **extended metadata** block:

```html
<!-- Extended metadata (for documentation, not parsed):
category: utility
complexity: advanced
mcp-servers: [auggie, serena, context7, tavily, sequential]
personas: [analyzer, performance, security, qa, refactorer, devops]
-->
```

**Fields in parsed frontmatter (order):**
1. `name` — `sc:<command-name>-protocol` form (colon-namespaced)
2. `description` — One sentence then "Use this skill whenever..." trigger guidance, ALL on one line
3. `allowed-tools` — Comma-separated list, includes `Skill` for cross-skill calls

**Notably absent from troubleshoot's parsed frontmatter:**
- No `version:`
- No `argument-hint:`

### 1.2 sc-brainstorm-protocol (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:1-6`)

```yaml
---
name: sc:brainstorm-protocol
description: "Full behavioral protocol for sc:brainstorm — Socratic dialogue + parallel proposals + adversarial merge"
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
argument-hint: "<topic> [--proposals N] [--depth quick|standard|deep] [--strategy ...] [--handoff ...] [--output dir]"
---
```

Followed (line 12-19) by HTML-comment block that DOES include `version:` and `spec:`:

```html
<!-- Extended metadata (for documentation, not parsed):
category: orchestration
complexity: advanced
mcp-servers: [sequential, serena, auggie-mcp, tavily]
personas: [architect, analyzer, scribe]
version: 2.0.0
spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
-->
```

**Fields in parsed frontmatter (order):**
1. `name` — same colon-namespace
2. `description` — terse one-liner (no trigger-guidance prose); trigger guidance moved to `## Triggers` section in body
3. `allowed-tools`
4. `argument-hint` — shell-style usage

### 1.3 Convergence vs divergence (reflect implication)

| Convention | troubleshoot | brainstorm | reflect should... |
|---|---|---|---|
| `name:` namespace | `sc:troubleshoot-protocol` | `sc:brainstorm-protocol` | Use `sc:reflect-protocol` |
| `description` length | long, trigger-rich, single line | terse one-liner | Spec §3.1 says LSC-style hyphen-joined; mirror **whichever spec §3.1 chose**. Spec is likely terse; mirror brainstorm. |
| `argument-hint` | absent | present | INCLUDE (matches reflect spec's CLI surface) |
| `version:` in parsed | absent | absent | absent (use HTML comment) |
| `version:` in HTML comment | absent | `version: 2.0.0` | INCLUDE (`version: 1.0.0`) |
| `spec:` in HTML comment | absent | `spec: .dev/...` | INCLUDE pointing to merged-requirements.md |
| `allowed-tools` ordering | "core tools first, then MCPs" | "core tools only (no MCPs)" | Mirror troubleshoot — reflect uses MCPs heavily |

**EXACT order convention (both):** `Read, ..., Bash, TodoWrite, Task, Write, Edit, Skill` then MCP tools. Brainstorm omits the trailing MCP block in parsed frontmatter because it delegates to other skills that own those tools.

---

## 2. Command-Side Frontmatter Shape

### 2.1 troubleshoot (`src/superclaude/commands/troubleshoot.md:1-9`)

```yaml
---
name: troubleshoot
description: "Tiered debugging — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate, and an opt-in task-builder remediation chain"
category: analysis
complexity: advanced
mcp-servers: [auggie, serena, context7, tavily, sequential]
personas: [analyzer, performance, security, qa, refactorer, devops]
argument-hint: "[<issue description>] [--type ...] [--depth ...] [--scope ...] [--no-escalate] [--fix] ..."
---
```

### 2.2 brainstorm (`src/superclaude/commands/brainstorm.md:1-10`)

```yaml
---
name: brainstorm
description: "Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge"
category: orchestration
complexity: advanced
mcp-servers: [sequential, serena, auggie-mcp, tavily]
personas: [architect, analyzer, scribe]
version: 2.0.0
spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
---
```

### 2.3 Command frontmatter convention

**Fields, in conventional order:**
1. `name:` — bare command name (NO `sc:` prefix, NO `-protocol` suffix) — e.g., `troubleshoot` not `sc:troubleshoot-protocol`
2. `description:` — one-line summary
3. `category:` — e.g., `analysis`, `orchestration`, `utility`
4. `complexity:` — `advanced` for both
5. `mcp-servers:` — YAML list inline `[a, b, c]`
6. `personas:` — YAML list inline
7. `version:` — present in brainstorm (1.0+); absent in troubleshoot
8. `spec:` — pointer to source-of-truth spec (brainstorm only)
9. `argument-hint:` — shell-style usage (troubleshoot only; brainstorm puts it in body)

**Reflect implication:** Use brainstorm's pattern (include `version`, include `spec` pointing to merged-requirements.md) since reflect is being rebuilt with a versioned spec.

---

## 3. Skill Body Section Ordering

### 3.1 sc-troubleshoot SKILL.md spine (NOT numbered §1-§N)

Top-level `##` headings in order (extracted from `SKILL.md:14-456`):

1. `## Purpose` (line 16)
2. `## Required Input (STOP if missing)` (line 26)
3. `## Output Contract` (line 37) — table with type-formatted columns
4. `## Wave Structure` (line 73) — code block listing waves
5. `### Wave 0:` ... `### Wave 6:` (lines 91, 129, 152, 190, 210, 230, 283, 312, 359) — per-wave sub-sections, NOT top-level §
6. `## Tool Coordination Summary` (line 377)
7. `## Will Do` (line 392)
8. `## Will Not Do` (line 404)
9. `## Error Handling` (line 416) — table
10. `## Token Cost Profile` (line 434)
11. `## Refs` (line 445) — table mapping refs files -> "when loaded"

### 3.2 sc-brainstorm SKILL.md spine (numbered §1-§7)

`##` headings (extracted from `SKILL.md:21-421`):

1. `## Triggers` (line 21)
2. `## 1. Purpose & Identity` (line 32)
3. `## 2. Required Input` (line 62)
4. `## 3. Wave Architecture` (line 72) — with `### Execution Vocabulary` table
5. `### Wave 0 — Prerequisites` ... `### Wave 4 — Handoff (Flag-Gated)` (lines 89, 114, 171, 202, 255, 298)
6. `## 4. Return Contract` (line 331) — with stable + telemetry sub-blocks
7. `## 5. Error Handling Matrix` (line 377) — table
8. `## 6. Will Do / Will Not Do` (line 399) — merged into ONE section, not two
9. `## 7. Spec Reference` (line 419)

### 3.3 Convergence/divergence (reflect implication)

**Brainstorm uses numbered §1-§7**, matching reflect spec §16's anticipated layout. **Troubleshoot does NOT** — its body uses descriptive headings only. Per spec §13.2 "within the band" — reflect's numbered §1-§19 spine is **closer to brainstorm's convention** but goes deeper (more sections).

**Reflect-spec deviation flag:** Spec §16 asks for ~19 numbered sections. That's significantly deeper than brainstorm's §1-§7 — closer to a hybrid (numbered top-level + descriptive sub-sections). This is a DELIBERATE spec deviation, not a violation. Document it as: "reflect inherits brainstorm's numbered-section convention but extends to deeper enumeration."

**Common conventions both share:**
- `## Required Input` (sometimes with `(STOP if missing)` annotation)
- Wave-based pipeline (`### Wave N — Name`)
- `## Will Do` / `## Will Not Do` (separated in troubleshoot, merged in brainstorm)
- Error-handling table near the end
- Refs/spec pointer last

---

## 4. Refs File Naming Convention

### 4.1 sc-troubleshoot-protocol/refs/ inventory

From `ls`:
- `doc-discovery.md` (7848 bytes)
- `escalation-rubric.md` (3703 bytes)
- `hypothesis-card-template.md` (4638 bytes)
- `remediation-handoff.md` (5434 bytes)
- `report-template.md` (13046 bytes)
- `triage-checklist.md` (3582 bytes)

### 4.2 sc-brainstorm-protocol/refs/ inventory

- `agent-spec-builder.md` (8926 bytes)
- `handoff-routing.md` (9419 bytes)
- `socratic-templates.md` (11598 bytes)

### 4.3 Pattern (with citations)

**Convention:** `<topic-noun>[-<modifier-noun>].md`, all-lowercase, hyphen-separated, NO numbering, NO frontmatter.

Examples of the pattern:
- Subject + structural type: `hypothesis-card-template.md`, `report-template.md`, `triage-checklist.md`
- Wave-scoped function: `doc-discovery.md`, `socratic-templates.md`
- Handoff/integration: `remediation-handoff.md`, `handoff-routing.md`
- Decision artifact: `escalation-rubric.md`, `agent-spec-builder.md`

**No `wave-1-` or `wave-N-` prefix.** Refs are named by **what they contain**, not by which wave loads them. The SKILL.md `Refs` table (troubleshoot:445-455) is the only place wave<->ref mapping lives.

### 4.4 Refs file frontmatter

**Verified: NONE of the 9 refs files have YAML frontmatter.**

Each ref starts directly with `# <Title>` (H1), e.g.:
- `escalation-rubric.md:1` -> `# Escalation Rubric`
- `socratic-templates.md` (verified via Read) starts `<!-- markdownlint-disable MD013 MD040 -->\n\n# Socratic Templates — ...`
- `agent-spec-builder.md` same pattern
- `handoff-routing.md` same pattern

Three brainstorm refs (`agent-spec-builder.md:1`, `handoff-routing.md:1`, `socratic-templates.md:1`) prepend a `<!-- markdownlint-disable MD013 MD040 -->` HTML comment. Troubleshoot refs do NOT use this comment. **Reflect-spec implication:** match whichever style your refs require for lint; the markdownlint-disable comment is harmless and recommended for tables.

---

## 5. Cross-Skill Invocation Syntax

The literal call patterns differ slightly:

### 5.1 Troubleshoot calls (4 distinct invocations found)

- **Skill call (Wave 4)**, `SKILL.md:292-299`:

```
Skill sc:adversarial-protocol with --compare fix-1.md,fix-2.md[,fix-3.md] \
    --depth quick (when source signals are strong) | standard (default) \
    --focus correctness,risk,test-coverage \
    --output <output-dir>/adversarial/
```

- **Skill call (Wave 6 Phase B)**, `refs/remediation-handoff.md:70`:
  > "Invoke `/sc:reflect --type task --analyze <task-file>` via `Skill` (if `sc:reflect` is available — otherwise fall back to spawning the `self-review` agent on the task file)."

- **Skill call (Wave 6 Phase A)**, `refs/remediation-handoff.md:40`:
  > "Invoke the `task-builder` skill via `Skill`. The `BUILD_REQUEST` is constructed from the report: ..."

- **In Tool Coordination table**, `SKILL.md:387`:
  > Skill in column header; Tier 2 cell reads `(`sc:adversarial-protocol`)`, Tier 3 cell reads `(`task-builder`, `/sc:reflect`)`

### 5.2 Brainstorm calls (3 distinct invocations)

- **Skill call (Wave 3)**, `SKILL.md:278`:
  > "**Invoke**: `Skill sc-adversarial-protocol` with above arguments. Direct skill invocation, not command — per sc:roadmap pattern."

- **Skill call (Wave 4)**, `SKILL.md:314`:
  > "Invoke `Skill sc-tasklist-protocol` with `--source <output>/merged-requirements.md`"

- **Skill call (Wave 4)**, `SKILL.md:326`:
  > "Invoke `Skill task-builder` with `--source <output>/merged-requirements.md --template <detected>`"

### 5.3 The literal syntax convention

Format: `Skill <skill-name> with <args>` OR `Skill <skill-name>` (verb followed by skill name, optionally followed by argument string).

**Skill-name forms in use (BOTH accepted):**
- Colon-namespaced: `sc:adversarial-protocol`, `sc:troubleshoot-protocol`, `sc:reflect`
- Hyphen-only (no `sc:`): `sc-adversarial-protocol`, `sc-tasklist-protocol`, `task-builder`

**Spec deviation flag:** Brainstorm consistently uses `sc-` (hyphen, no colon) in `Skill ...` calls (`SKILL.md:278, 314, 326`), while troubleshoot uses `sc:adversarial-protocol` (colon) in its Wave 4 invocation (`SKILL.md:292`). This is INCONSISTENT across the band. Reflect should pick one and document it in its own SKILL.md. **Recommendation:** mirror brainstorm's hyphen form since brainstorm is newer (v2.0.0) and explicitly references the "sc:roadmap pattern" as its model.

---

## 6. Task Agent Delegation Pattern

Both skills delegate to specialized agents via the `Task` tool. The conventional shape:

### 6.1 Task call structure (troubleshoot Wave 1.7 example, `SKILL.md:198-200`)

> "1. **Form one hypothesis** — spawn the `root-cause-analyst` agent via `Task` with a focused brief: the symptom, the grounding from Wave 1 step 1, the observation from Wave 1 step 2, the Documentation Context Card path (`<output-dir>/doc-context.md`, or `null` when Wave 1.5 was skipped via `--no-doc-discovery`), and `--scope` if any. The agent's job is to produce one hypothesis card (template in `refs/hypothesis-card-template.md`) — not three, not the full tree."

### 6.2 Task call structure (troubleshoot Wave 1.7 calibrator, `SKILL.md:199-200`)

> "2. **Calibrate confidence (independently)** — spawn the `confidence-calibrator` agent via `Task` with `card_path=<output-dir>/tier1-hypothesis.md`, `rubric_path=<skill-dir>/refs/escalation-rubric.md`, `card_tier=1`, `flags_context=<wave 0 parsed flags>`, `output_path=<output-dir>/tier1-calibration.md`."

### 6.3 The Task-delegation convention

**Convention:** spawn AGENT via `Task` with KEY=VALUE briefing parameters. Agent inputs are documented inline in the wave step; expected outputs go to a deterministic `<output-dir>/<artifact>.md` path. **Fallback is ALWAYS documented as a separate sub-bullet immediately under the spawn instruction.**

EXACT fallback phrasing convention (`SKILL.md:200-201, 204`):
> "**Fallback**: if `confidence-calibrator` fails (subprocess crash, malformed output, agent unavailable), fall back to inline orchestrator calibration against the rubric and mark `calibration: inline-fallback` in the audit log."

And:
> "**Failure handling**: If the `root-cause-analyst` agent fails entirely (subprocess crash, no output card produced), fall back to inline orchestrator hypothesis formation against `refs/hypothesis-card-template.md` and mark `hypothesis_source: inline-fallback` in audit. Wave 2 confidence gate proceeds normally with whatever was produced."

**Reflect implication:** Every `Task` spawn in reflect's SKILL.md MUST be paired with an inline-orchestrator fallback that writes a `<key>: inline-fallback` marker into the audit log.

---

## 7. Per-Step Audit Log Convention

### 7.1 Audit log format in sc-troubleshoot

**Two formats are used:**

1. **Wave 0 header** (`SKILL.md:108-121`) — HTML comment with `SC:TROUBLESHOOT:TARGET` marker:

```
<!-- SC:TROUBLESHOOT:TARGET
issue: <first 80 chars>
type: <type|auto>
depth: <quick|standard|deep|auto>
scope: <path|symbol|none>
fix_authorized: <bool>
no_escalate: <bool>
mcps_available: <auggie|serena|context7|tavily|sequential|none>
output_dir: <abs-path>
-->
```

2. **Wave 5 footer** (`SKILL.md:333-346`) — HTML comment with `SC:TROUBLESHOOT:SUMMARY` marker:

```
<!-- SC:TROUBLESHOOT:SUMMARY
status: <success|partial>
tier_reached: <1|2|3>
confidence: <float>
escalation_reason: <none|low_confidence|...>
hypothesis_count: <N>
adversarial_invoked: <bool>
fix_authorized: <bool>
duration_sec: <N>
-->
```

**Audit-log row format throughout the body:** the SKILL.md does NOT specify a `{wave, step, timestamp, outcome, evidence_ref}` shape. Instead, it uses inline statements like "mark `calibration: inline-fallback` in the audit log" and "Emit 'Wave X complete: ...'".

**Spec deviation flag:** Reflect's spec presumably proposes a structured `{wave, step, timestamp, outcome, evidence_ref}` row shape. **This is a SPEC EXTENSION** — no precedent in either troubleshoot or brainstorm. Researcher 06 should confirm reflect's spec §X actually proposes that shape; if so, it's a deliberate enhancement, not a copy of an existing convention.

### 7.2 Brainstorm audit log

Brainstorm does NOT use the HTML-comment audit format. Instead, it uses a single `return-contract.yaml` (`SKILL.md:331-375`) with stable + telemetry blocks. See §8 below.

---

## 8. Return Contract Two-Block Shape

### 8.1 Brainstorm's split (`SKILL.md:333-375`) — THE canonical pattern

**Stable Contract block (line 338-352):**

```yaml
contract_version: "1.0"
status: success | partial | failed | dry-run
seed_brief_path: <path>
merged_output_path: <path> | null
convergence_score: <float 0.0-1.0> | null
adversarial_artifacts_dir: <path> | null
domain: code | architecture | product | process | incident | research
proposal_count: <int>
enrichment_used:
  - source: codebase | research-light | research-deep
    quality_tier: primary | fallback_1 | fallback_2 | skipped
handoff_action: none | design | tasklist | task
handoff_output_path: <path> | null
unresolved_conflicts: [<list of strings>]
```

**Telemetry Block (line 357-375):**

```yaml
wave_durations_ms:
  wave_0: <ms>
  wave_1: <ms>
  ...
token_usage:
  wave_0: <est>
  ...
agent_spec: "<the composed agent-spec string>"
enrichment_artifact_sizes:
  codebase-context.md: <bytes>
  ...
```

### 8.2 Troubleshoot's single-block contract (`SKILL.md:37-72`)

Troubleshoot uses ONE markdown TABLE as the output contract (no YAML split). 17 fields with type + description. Telemetry like `duration_sec` is in the audit-log HTML footer instead.

### 8.3 Convention summary

| Feature | troubleshoot | brainstorm | reflect should... |
|---|---|---|---|
| Contract location | inline table in SKILL.md | `return-contract.yaml` file | YAML file (matches reflect spec) |
| Stable + telemetry split | NO (single table) | YES (two yaml blocks) | YES — mirror brainstorm |
| `contract_version:` field | absent | present (`"1.0"`) | INCLUDE |
| `status:` enum | success/partial/failed | success/partial/failed/dry-run | mirror reflect's spec values |

**Reflect's §9.1/§9.2 split IS mirrored — by brainstorm only.** Troubleshoot is the outlier. This is a CONVENTION DELTA reflect must inherit from brainstorm specifically.

---

## 9. Fallback Path Naming (F1/F2/F3)

### 9.1 Origin

**F1/F2/F3 is from brainstorm, NOT troubleshoot.**

Brainstorm `SKILL.md:291-294` and `refs/handoff-routing.md:136-142`:

> **Fallback protocol** (F1-F3 per sc:roadmap pattern):
> - **F1** — Skill tool error -> retry once with `--depth quick` and reduced proposal count. If retry succeeds, route to step 3.
> - **F2** — Retry fails -> abort Wave 3. Emit error with adversarial logs path. Set `status: failed`. Skip Wave 4.
> - **F3** — All variants fail mid-generation -> write `<output>/brainstorm-failed.md` with partial state for forensic review. Exit.

Note the cite: "per sc:roadmap pattern" — F1/F2/F3 is a project-wide convention that originated in sc:roadmap and was adopted by brainstorm.

### 9.2 Troubleshoot does NOT use F1/F2/F3

Troubleshoot uses **"Failure handling" tables per wave** (e.g., `SKILL.md:273-280, 416-432`) with scenario->behavior->fallback columns. Different style, similar substance.

**Reflect implication:** F1/F2/F3 IS an established convention. Reflect can use it; expect the spec to mention it explicitly.

---

## 10. Fail-Open MCP Policy Phrasing

### 10.1 troubleshoot pattern

EXACT phrasing for MCP fail-open (from `SKILL.md:417-432`, table form):

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| All MCPs unavailable | Run in `--no-mcp` mode; warn user that triage quality is degraded; native tools only | None |
| auggie unavailable (others OK) | Fall back to `Grep` + `Glob` for grounding; mark in audit | None |

Inline reference (`SKILL.md:140`):
> "If `--no-mcp` or both MCPs are unavailable: fall back to `Glob` + `Grep` on the issue keywords; note the fallback in the audit log."

### 10.2 brainstorm pattern

EXACT phrasing (`SKILL.md:381-385`, error matrix):

| Codebase enrichment fails (Auggie down) | WARN, fall back to Serena `get_symbols_overview` (quality_tier=fallback_1) | Native Glob/Grep (quality_tier=fallback_2) |
| Research enrichment fails (Tavily down) | WARN, fall back to WebSearch (quality_tier=fallback_1) | Skip (quality_tier=skipped) |

### 10.3 Convention summary

Both share the **"fall back to native tools and mark in audit"** policy. Brainstorm additionally adds a `quality_tier: primary | fallback_1 | fallback_2 | skipped` enum tracking the degraded path. **Reflect implication:** mirror brainstorm's `quality_tier` enum since it's machine-readable.

EXACT boilerplate to mirror (troubleshoot `SKILL.md:140`):
> "If `--no-mcp` or [MCP-X] unavailable: fall back to [native-tool-Y]; note the fallback in the audit log."

---

## 11. Output Directory Convention

### 11.1 troubleshoot (`SKILL.md:107`)

> "Compute output slug: `<type-or-untyped>-<first-5-words-of-issue-or-scope>-<YYYYMMDDHHMMSS>` and create `<output-dir>/`."

Default: `.dev/troubleshoot/<slug>-<timestamp>/` (from `commands/troubleshoot.md:56`).

### 11.2 brainstorm (`SKILL.md:108`)

> "Create output directory (default `.dev/brainstorms/<ts>-<slug>/`). If exists and non-empty, append `-N` suffix. Cap N at 99 (STOP on N=100); WARN at N>=10."

Note brainstorm puts timestamp **before** slug; troubleshoot puts timestamp **after**.

### 11.3 Convention summary

**`.dev/<skill-slug>/<run-slug>/` is the universal root.** Subdirectory is one of:
- `<noun-form>` (e.g., `troubleshoot`, `brainstorms`) — NOT the full skill name
- Run-slug components: `<type|domain>-<keywords>-<timestamp>`

**Reflect implication:** Match `.dev/reflect/<run-slug>/` per spec §16. Use brainstorm's append-suffix-on-collision convention with `Cap N at 99` STOP.

---

## 12. Kill List / Will / Will Not / Boundaries Structure

### 12.1 troubleshoot (`SKILL.md:392-413`)

Three top-level sections:

```markdown
## Will Do
- Always run Tier 1 first; respect the "quick first option" contract
- Auto-escalate only when the rubric in `refs/escalation-rubric.md` says so
- ... [8 bullets total]

## Will Not Do
- Apply code changes without `--fix` and explicit user confirmation
- ... [9 bullets total]
```

### 12.2 brainstorm (`SKILL.md:399-417`)

ONE merged section with sub-headings:

```markdown
## 6. Will Do / Will Not Do

**Will:**
- Orchestrate Socratic dialogue + enrichment + adversarial delegation + handoff
- ... [6 bullets]

**Will Not:**
- Re-implement adversarial debate, scoring, or merge logic
- ... [6 bullets]
```

### 12.3 Command-side mirror

The COMMAND files also have `## Boundaries` sections with the same Will:/Will Not: split, e.g., `commands/troubleshoot.md:158-181` and `commands/brainstorm.md:147-164`. Both bullet-listed.

### 12.4 "Kill List" — NOT a standard convention

Neither file uses a section called "Kill List". The spec's "Kill List" terminology is new to reflect.

**Spec deviation flag:** if reflect's spec §X uses "Kill List", that's a NEW name for what existing skills call "Will Not Do" / "Will Not:" / `## Boundaries`. Decide whether to keep the new name (deliberate) or rename to match (consistent).

---

## 13. Bidirectional Command <-> Skill Link Convention

### 13.1 Command -> Skill (the Activation gate)

EXACT phrasing from `commands/troubleshoot.md:78-82`:

```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:troubleshoot-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — wave structure, escalation rubric, agent selection, file:line validation, hallucination contract, remediation chain — is in the protocol skill.
```

EXACT phrasing from `commands/brainstorm.md:138-143`:

```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:brainstorm-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification is in the protocol skill at `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`.
```

**Convention:**
1. Heading: `## Activation`
2. Bold `**MANDATORY**:` with the verb-form instruction
3. Blockquote (`> Skill <skill-name>`) — note one uses colon, one uses hyphen — see §5.3 deviation
4. Trailing paragraph re-explaining WHY the command can't be self-contained

### 13.2 Skill -> Command (the Triggers section)

Brainstorm `SKILL.md:21-30` includes an explicit upward link:

```markdown
## Triggers

sc:brainstorm-protocol is invoked ONLY by the `sc:brainstorm` command via `Skill sc:brainstorm-protocol` in its `## Activation` section. Never invoked directly by users.

Activation conditions:
- User runs `/sc:brainstorm <topic> [flags...]` in Claude Code
- All flag arguments are passed through from the command

Do NOT invoke this skill directly. Use the `/sc:brainstorm` command.
```

Troubleshoot does NOT include this upward link in its SKILL.md.

**Reflect implication:** Include the brainstorm-style upward `## Triggers` block — it's the newer, cleaner pattern.

---

## 14. "ESCALATION — CRITICAL OVERRIDE" Phrasing

The literal phrase "ESCALATION — CRITICAL OVERRIDE" appears in NEITHER file. Searching for related boilerplate:

### 14.1 troubleshoot "CRITICAL BOUNDARIES" header (`commands/troubleshoot.md:182-192`)

```markdown
## CRITICAL BOUNDARIES

**DIAGNOSE FIRST — FIXES REQUIRE `--fix` FLAG AND EXPLICIT USER CONFIRMATION**

This command is diagnosis-first by default.

- **Default behavior (no `--fix` flag)**: Run Tiers 1-2, produce REPORT.md, STOP. The user reviews and either re-runs with `--fix` or applies the fix manually.
- **With `--fix` flag**: After REPORT.md, offer the Tier 3 remediation chain. Build the task file. **Stop and surface the literal `/task <path>` command — the user runs it, never the skill.**
- **After `/task` completes**: The user runs `/sc:reflect --type task --validate` as the pre-commit gate.

No silent code changes. No auto-execution. No auto-commit.
```

### 14.2 brainstorm "Stop after merged requirements" (`commands/brainstorm.md:177-202`)

```markdown
## CRITICAL BOUNDARIES

### Stop after merged requirements

This command produces a REQUIREMENTS SPECIFICATION (spec-style format) plus optional downstream artifacts via `--handoff`.

**Explicitly Will NOT**:
- Generate implementation code (use `/sc:implement`)
...
```

### 14.3 Convention

The convention is **`## CRITICAL BOUNDARIES`** (all-caps, no override phrasing). Both files use this exact heading. Reflect should use the same.

**Reflect-spec deviation flag:** If the spec uses "ESCALATION — CRITICAL OVERRIDE" verbatim, that's a NEW phrase. Either:
- Use the spec's new phrase (deliberate)
- Rename to `## CRITICAL BOUNDARIES` (consistent)

Researcher 06 should confirm which the spec specifies.

---

## 15. `make sync-dev` Workflow Paragraph

**Not present in SKILL.md bodies or command bodies.** The `make sync-dev` discipline lives in CLAUDE.md (project root) and is enforced by the pre-commit `verify-sync` hook. Neither protocol skill mentions it in its body.

**Reflect implication:** Do NOT include a `make sync-dev` paragraph in reflect's SKILL.md or command file. It's a project-level concern, not a per-skill concern.

---

## 16. Hook-Redirect Message Body

**Not present in skill/command bodies.** Hooks are configured in `.claude/settings.json` and emit their own redirect messages at hook-time (e.g., the "skill workspace must be in `.dev/eval-workspaces/`" override). Reflect's SKILL.md/command should NOT include hook-redirect text.

---

## 17. Tool Coordination Table

### 17.1 troubleshoot `SKILL.md:377-390`

```markdown
## Tool Coordination Summary

| Tool | Tier 1 | Tier 2 | Tier 3 |
|------|--------|--------|--------|
| `mcp__auggie__codebase-retrieval` | (check) (one focused query + Wave 1.5 doc-grounding fan-out: 3 parallel branch queries) | (check) (per-hypothesis queries) | — |
...
```

### 17.2 brainstorm

Brainstorm does NOT have a "Tool Coordination Summary" — it has `### Execution Vocabulary` at `SKILL.md:78-87` which serves the same purpose but is more compact:

```markdown
### Execution Vocabulary

| Verb | Tool | Scope |
|------|------|-------|
| Invoke Skill | `Skill` | Cross-skill invocation (e.g., `Skill sc:adversarial-protocol`) |
| Dispatch Task agent | `Task` | Parallelized sub-agent work (enrichment) |
...
```

**Reflect implication:** Either is acceptable. brainstorm's `### Execution Vocabulary` is more concise; troubleshoot's per-tier table is more expressive. Pick based on whether reflect has tier-like phases (then mirror troubleshoot) or vocabulary-driven flow (then mirror brainstorm).

---

## 18. Refs Table (Lazy-Load Discipline)

### 18.1 troubleshoot pattern (`SKILL.md:445-456`)

```markdown
## Refs

| File | When loaded |
|------|-------------|
| `refs/escalation-rubric.md` | Wave 2 (confidence gate) and Wave 1.7 (calibration) |
| `refs/triage-checklist.md` | Wave 1 (real-code grounding load) AND Wave 1.7 (passed to root-cause-analyst as part of the brief) |
...

Each ref is loaded only by the wave that needs it. Do not pre-load.
```

### 18.2 brainstorm pattern

Brainstorm does NOT have a final `## Refs` table. Refs are mentioned inline in each Wave under `**Refs Loaded**:` annotations (e.g., `SKILL.md:118, 175, 207, 261, 303`).

EXACT phrasing: `**Refs Loaded**: Read `refs/socratic-templates.md` (depth-tiered question banks + domain taxonomy).` (`SKILL.md:118`)

### 18.3 Convention

**Both share the "lazy-load, never pre-load" discipline** but document it differently:
- troubleshoot: `## Refs` table at the END with `When loaded` column
- brainstorm: `**Refs Loaded**:` annotation per wave

**Reflect implication:** Choose ONE. Brainstorm's inline pattern is more discoverable when reading the wave; troubleshoot's table is better for cross-wave audit. **Recommendation:** include BOTH — inline `**Refs Loaded**` annotations per wave AND a closing `## Refs` table — since reflect's spec proposes deep enumeration.

---

## 19. Exit Criteria + Emit Phrasing

Both skills end every wave with the same shape:

### 19.1 EXACT format (troubleshoot `SKILL.md:123, 146, 174, 202, 226, 281, 306, 355, 373`)

> **Exit criteria**: input validated, output dir created, audit log opened. Emit "Wave 0 complete: type=<type> depth=<depth>".

### 19.2 EXACT format (brainstorm `SKILL.md:112, 169, 200, 253, 296, 329`)

> **Exit Criteria**: All prerequisites validated. Output dir ready. Emit: `"Wave 0 complete: prereqs validated. Models: <list>. Proposals: <N>. Depth: <D>. Output: <path>."`

### 19.3 Convention

- **Header:** `**Exit criteria**:` (troubleshoot lowercase 'c') OR `**Exit Criteria**:` (brainstorm capital 'C') — INCONSISTENT within band; pick one.
- **Body:** 1-2 sentence summary of what's now true.
- **Emit:** `Emit "Wave N complete: <key=value pairs>"` — literal `Emit` keyword, double-quoted message containing wave number, "complete:" suffix, then key=value pairs of materialized facts.

**Reflect implication:** Use this exact emit shape for every wave.

---

## 20. STOP Phrasing Convention

### 20.1 Troubleshoot

`SKILL.md:33`:
> "**STOP** if neither is present — without a symptom and a scope the skill has nothing to triage."

`SKILL.md:35`:
> "**STOP** if `--depth deep` is requested but the issue description is under 10 words and no scope was given — too vague for a deep pass to add value; ask the user to add detail first."

### 20.2 Brainstorm

`SKILL.md:70`:
> "**STOP** on empty topic with: `\"Brainstorm requires a topic. Usage: /sc:brainstorm \\\"<topic>\\\"\"`"

`SKILL.md:95`:
> "Parse `$ARGUMENTS` into topic + flags. Reject empty topic. STOP if empty: `\"Brainstorm requires a topic. Usage: /sc:brainstorm \\\"<topic>\\\"\""`

### 20.3 Convention

- Bold **STOP** keyword
- Followed by `if <condition>` clause
- Followed by `— <reason>` (em-dash + reason) OR `: <literal-message-to-print>` (colon + quoted message)

Brainstorm's pattern is stricter: it specifies the EXACT user-facing message to print. Reflect should mirror brainstorm's literal-message pattern for machine-checkable behavior.

---

## 21. Quality Tier Tracking (brainstorm-only convention)

`SKILL.md:189-194`:

```markdown
2. **Quality-tier tracking** (mandatory per enrichment source):
   - `primary` — first-choice source ran cleanly
   - `fallback_1` — primary failed, used Serena (codebase) or WebSearch (research)
   - `fallback_2` — both primary and fallback_1 failed, used native Glob/Grep
   - `skipped` — enrichment not invoked
   - Record as `enrichment_used: [{source, quality_tier}, ...]` in state.
```

**Reflect implication:** This enum is machine-readable telemetry. If reflect spec has anything like "MCP grounding success/degradation tracking", mirror this EXACT enum.

---

## 22. Token Budget Convention

### 22.1 Troubleshoot per-wave

`SKILL.md:148`:
> "**Token budget for Wave 1**: target <= ~3k Claude tokens (MCP retrieval offloads the bulk of the work)."

`SKILL.md:186`:
> "**Token budget**: Wave 1.5 should consume <= 2k Claude tokens (the auggie calls offload heavy retrieval). If it goes over 3k Claude tokens, audit-log the overrun — the wave is meant to be retrieval-offload, not Claude reasoning."

### 22.2 Troubleshoot per-tier (`SKILL.md:434-443`)

```markdown
## Token Cost Profile

| Tier reached | Auggie tokens (offloaded) | Claude tokens (orchestration + agents) | Wall clock |
|--------------|---------------------------|----------------------------------------|------------|
| Tier 1 only | ~2-5k | ~3-6k | 1-3 min |
...
```

### 22.3 Brainstorm

`SKILL.md:232-238` (token-budget pre-flight in Wave 2B):
> "Estimate Wave 3 cost: `estimate = proposals * depth_multiplier * persona_weight`
> - depth_multiplier: quick=8K, standard=15K, deep=35K per proposal
> - persona_weight: 1.0 default, 1.3 for architect/analyzer"

**Reflect implication:** Both styles are valid. Troubleshoot uses per-wave inline + per-tier table; brainstorm uses estimated formula. Mirror whichever reflect's spec §X specifies.

---

## 23. "Refuse the path" Refusal Convention (troubleshoot-only)

`refs/triage-checklist.md:56-66`:

```markdown
## When to refuse Tier 1

Refuse and recommend `--depth deep` immediately if:

- The symptom is "intermittent" with no reproducer
- The reported scope spans more than 3 modules ...
- ...

Refusal is not failure — it's correctly judging that a one-shot pass is the wrong tool.
```

**Reflect implication:** If reflect has a similar "refuse-and-recommend-different-tier" path, mirror this exact framing: "Refusal is not failure — it's correctly judging that <X> is the wrong tool."

---

## Key Findings — Conventions Reflect MUST Mirror

1. **SKILL.md frontmatter** = brainstorm's terse style + HTML-comment extended metadata block (include `version`, `spec`, `argument-hint`)
2. **Command frontmatter** = brainstorm's pattern including `version` and `spec`
3. **Body structure** = brainstorm's numbered `## N. Section` pattern (reflect deepens to §1-§19)
4. **Refs filenames** = lowercase-kebab-case, NO frontmatter, NO numbering, start with `# Title` H1
5. **Cross-skill calls** = `Skill <skill-name> with <args>` form; reflect should use hyphen-form `sc-X-protocol` to match brainstorm/roadmap pattern (NOT colon-form)
6. **Task agent delegation** = "spawn `<agent>` via `Task` with `key=value` brief; on failure fall back to inline orchestrator and mark `<key>: inline-fallback` in audit log"
7. **Audit log** = HTML-comment header + footer markers (troubleshoot) OR `return-contract.yaml` (brainstorm). Reflect's structured per-step row is a SPEC EXTENSION beyond both.
8. **Return contract two-block** = brainstorm's `contract_version: "1.0"` stable + telemetry split (mandatory mirror)
9. **F1/F2/F3 fallback** = brainstorm's pattern; established convention from sc:roadmap
10. **MCP fail-open** = "If [MCP-X] unavailable: fall back to [native-tool-Y]; note in audit log"
11. **Output dir** = `.dev/<noun-form>/<slug>-<timestamp>/` with brainstorm's collision-suffix rule
12. **Will/Will Not** = either two separate sections (troubleshoot) or one merged (brainstorm); reflect chooses
13. **Activation gate** = exact MANDATORY block + blockquote `> Skill <name>` + trailing why-paragraph
14. **Triggers section** = include brainstorm's upward link (skill->command relationship)
15. **CRITICAL BOUNDARIES** = exact heading; both files use it
16. **Per-wave Refs Loaded** = brainstorm's inline annotation per wave + troubleshoot's final `## Refs` table (best of both)
17. **Exit criteria/Emit** = `**Exit criteria**: <prose>. Emit "Wave N complete: <kv pairs>"`
18. **STOP phrasing** = bold **STOP** + condition + literal message-to-print (brainstorm style preferred for machine-checkable)
19. **Quality tier enum** = `primary | fallback_1 | fallback_2 | skipped`
20. **Token budgets** = either per-wave inline OR formula; both acceptable

## Spec Deviations to Flag for the Builder

1. **`{wave, step, timestamp, outcome, evidence_ref}` audit row** — reflect-spec proposal, NO precedent in either skill. Deliberate enhancement.
2. **§1-§19 deep numbered spine** — extends brainstorm's §1-§7 convention. Deliberate.
3. **"Kill List" terminology** — if used in spec, NEW name for existing "Will Not"/`## Boundaries`. Decide deliberately.
4. **"ESCALATION — CRITICAL OVERRIDE"** — if used in spec, NEW phrasing for `## CRITICAL BOUNDARIES`. Decide deliberately.
5. **§9.1/§9.2 split** — reflect's two-block contract DOES match brainstorm; this is NOT a deviation, it's mirroring brainstorm specifically.

## File Citations Index

| Convention | Primary citation |
|---|---|
| Frontmatter shape (terse) | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:1-6` |
| Frontmatter shape (trigger-rich) | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:1-5` |
| HTML-comment metadata block | `sc-troubleshoot-protocol/SKILL.md:7-12`, `sc-brainstorm-protocol/SKILL.md:12-19` |
| Command frontmatter | `src/superclaude/commands/brainstorm.md:1-10`, `src/superclaude/commands/troubleshoot.md:1-9` |
| Body numbering §1-§N | `sc-brainstorm-protocol/SKILL.md:32-419` |
| Wave-style sub-sections | `sc-troubleshoot-protocol/SKILL.md:91-373` |
| Refs filename pattern | `src/superclaude/skills/sc-troubleshoot-protocol/refs/` (6 files), `src/superclaude/skills/sc-brainstorm-protocol/refs/` (3 files) |
| Refs no-frontmatter | all 9 refs files (verified via Read) |
| `Skill <name>` invocation | `sc-troubleshoot-protocol/SKILL.md:292-299`, `sc-brainstorm-protocol/SKILL.md:278, 314, 326` |
| Task fallback pattern | `sc-troubleshoot-protocol/SKILL.md:200-201, 204, 332` |
| Audit log HTML markers | `sc-troubleshoot-protocol/SKILL.md:108-121, 333-346` |
| Return contract YAML | `sc-brainstorm-protocol/SKILL.md:331-375` |
| F1/F2/F3 fallback | `sc-brainstorm-protocol/SKILL.md:291-294`, `refs/handoff-routing.md:136-142` |
| MCP fail-open phrasing | `sc-troubleshoot-protocol/SKILL.md:140, 417-432` |
| Output dir convention | `sc-troubleshoot-protocol/SKILL.md:107`, `sc-brainstorm-protocol/SKILL.md:108` |
| Will/Will Not (separated) | `sc-troubleshoot-protocol/SKILL.md:392-413` |
| Will Do / Will Not Do (merged) | `sc-brainstorm-protocol/SKILL.md:399-417` |
| `## Activation` block (command) | `commands/troubleshoot.md:78-82`, `commands/brainstorm.md:138-143` |
| `## Triggers` (skill upward link) | `sc-brainstorm-protocol/SKILL.md:21-30` |
| `## CRITICAL BOUNDARIES` | `commands/troubleshoot.md:182-192`, `commands/brainstorm.md:177-202` |
| `## Refs` table | `sc-troubleshoot-protocol/SKILL.md:445-456` |
| `**Refs Loaded**:` inline | `sc-brainstorm-protocol/SKILL.md:118, 175, 207, 261, 303` |
| Exit criteria / Emit | `sc-troubleshoot-protocol/SKILL.md:123, 146, 174, 202, 226, 281, 306, 355, 373`, `sc-brainstorm-protocol/SKILL.md:112, 169, 200, 253, 296, 329` |
| STOP phrasing | `sc-troubleshoot-protocol/SKILL.md:33, 35`, `sc-brainstorm-protocol/SKILL.md:70, 95` |
| Quality tier enum | `sc-brainstorm-protocol/SKILL.md:189-194` |
| Token budget per-wave | `sc-troubleshoot-protocol/SKILL.md:148, 186`, `sc-brainstorm-protocol/SKILL.md:232-238` |
| Refusal-not-failure phrasing | `sc-troubleshoot-protocol/refs/triage-checklist.md:56-66` |

---

**Research complete.** All conventions cited with `file:line` evidence. Spec deviations flagged for builder.
