---
name: sc:validate-roadmap
description: "Validate roadmap pipeline outputs (roadmap.md, test-strategy.md, extraction.md) produced by `superclaude roadmap run`. Mirrors the CLI `roadmap validate` surface: single-agent reflection by default, adversarial merge when N≥2 agents; always exits 0 per NFR-006 with findings surfaced as console output."
category: analysis
complexity: advanced
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__search_for_pattern, mcp__serena__activate_project
mcp-servers: [sequential, auggie, serena]
personas: [analyzer, architect, qa]
---

# /sc:validate-roadmap — Roadmap Pipeline Output Validator

Validate the artifacts produced by a prior `superclaude roadmap run`. The CLI surface routes by agent count: a single agent runs reflection against the validation dimensions; N≥2 agents fan out parallel reflections and then run an adversarial merge into a single `validation-report.md`. The validation subcommand always exits 0 per NFR-006 — blocking findings are surfaced via console output, not exit codes.

## Usage

```bash
/sc:validate-roadmap <OUTPUT_DIR> [options]
```

`<OUTPUT_DIR>` must contain `roadmap.md`, `test-strategy.md`, and `extraction.md` from a prior `superclaude roadmap run`. Validation writes to `<OUTPUT_DIR>/validate/`.

## Arguments

- `OUTPUT_DIR`: Path to the roadmap pipeline output directory (required). Must contain `roadmap.md`, `test-strategy.md`, and `extraction.md`.

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--agents` | No | `opus:architect` | Comma-separated agent specs: `model[:persona]`. Single-agent is the default for cost efficiency; pass two or more (e.g. `opus:architect,haiku:qa`) to enable adversarial merge. |
| `--model` | No | `""` (per-agent) | Override model for all validation steps. Empty string keeps each agent's spec model. |
| `--max-turns` | No | `100` | Max agent turns per claude subprocess. |
| `--debug` | No | `false` | Enable debug logging. |

**Routing behavior:**

- **N = 1 agent:** single-agent reflection → writes `validation-report.md` directly.
- **N ≥ 2 agents:** N parallel reflections → adversarial merge → consolidated `validation-report.md`.

**Validation dimensions:** baseline 7 dimensions (Schema, Structure, Traceability, Cross-file consistency, Parseability, Interleave, Decomposition); expands to 9 input-aware dimensions when the original source inputs (spec / TDD / PRD) resolve from `.roadmap-state.json`.

**Exit code:** Always 0 (NFR-006). Inspect `<OUTPUT_DIR>/validate/validation-report.md` and the console summary for blocking/warning/info counts.

## Examples

```bash
# Default single-agent validation
/sc:validate-roadmap ./output

# Multi-agent with adversarial merge
/sc:validate-roadmap ./output --agents opus:architect,haiku:qa

# Three-agent merge with a global model override and verbose logging
/sc:validate-roadmap .dev/releases/current/v3.0/output \
  --agents opus:architect,sonnet:qa,haiku:analyzer \
  --model opus \
  --max-turns 150 \
  --debug
```

## Output Layout

```text
<OUTPUT_DIR>/
└── validate/
    ├── reflect-<agent-id>.md     # one per agent when N≥2
    └── validation-report.md      # consolidated report
```

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc-validate-roadmap-protocol

Pass all user-provided arguments (output directory path, flags) verbatim to the Skill invocation via the `args` parameter.

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.

**Relationship to the CLI:** The CLI `superclaude roadmap validate <OUTPUT_DIR>` is the deterministic counterpart of this slash command. The inference protocol skill (`sc-validate-roadmap-protocol`) may offer additional investigative depth beyond the CLI's baseline 7 / input-aware 9 dimensions; see the skill's "Relationship to CLI" header for the crosswalk.

## Boundaries

**Will:**

- Validate that `<OUTPUT_DIR>` contains the three required pipeline artifacts (`roadmap.md`, `test-strategy.md`, `extraction.md`)
- Run single-agent reflection (N=1) or parallel reflections + adversarial merge (N≥2)
- Apply the 7 baseline validation dimensions, expanding to 9 when source inputs resolve
- Write all intermediate and final artifacts to `<OUTPUT_DIR>/validate/`
- Surface blocking / warning / info findings via console output

**Will Not:**

- Modify `roadmap.md`, `test-strategy.md`, `extraction.md`, or any source spec/TDD/PRD file
- Return a non-zero exit code on validation findings (NFR-006: always exits 0; findings are reported via stdout and the validation report)
- Trigger downstream commands (tasklist generation, implementation, remediation execution)
- Spawn additional sub-agents beyond the `--agents` list passed on the CLI

## See Also

- `/sc:roadmap` — Generate roadmaps from specifications (produces the artifacts this command validates)
- `/sc:tasklist` — Generate tasklists from validated roadmaps
- `/sc:adversarial` — Standalone adversarial debate pipeline
- `superclaude roadmap validate --help` — CLI counterpart (canonical flag surface)
