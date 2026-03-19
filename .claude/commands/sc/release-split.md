---
name: release-split
description: "Neutral two-phase release split analysis with adversarial validation and fidelity verification"
category: planning
complexity: advanced
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
mcp-servers: [sequential, context7, serena]
personas: [architect, analyzer, scribe]
---

# /sc:release-split - Release Split Analysis & Execution

## Required Input

- A release artifact (spec, roadmap, tasklist, or refactor plan) provided as a file path
- The artifact must contain identifiable requirements, deliverables, or scope items

```bash
/sc:release-split <spec-file-path> [options]
```

## Usage

```bash
# Basic: Analyze whether a release should be split
/sc:release-split path/to/release-spec.md

# With explicit output directory
/sc:release-split path/to/release-spec.md --output .dev/releases/current/v3.1/

# Deep analysis with interactive checkpoints
/sc:release-split path/to/release-spec.md --depth deep --interactive

# Skip directly to execution if you already have a validated proposal
/sc:release-split path/to/release-spec.md --resume-from path/to/split-proposal-final.md

# Force no-split — run fidelity verification on an intact release
/sc:release-split path/to/release-spec.md --no-split

# Custom agents for adversarial variant generation
/sc:release-split path/to/release-spec.md --agents opus:architect,sonnet:security

# With custom instructions per agent
/sc:release-split path/to/release-spec.md \
  --agents opus:architect:"Focus on dependency isolation",haiku:analyzer:"Prioritize testability"
```

## Options

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<spec-file-path>` | | Yes | - | Path to release artifact to analyze |
| `--output` | `-o` | No | `<spec-dir>/release-split/` | Output directory for all artifacts |
| `--depth` | `-d` | No | `standard` | Analysis depth: quick, standard, deep |
| `--interactive` | `-i` | No | `false` | Pause for user confirmation between phases |
| `--resume-from` | | No | - | Path to pre-validated split proposal; skips Parts 1-2 |
| `--no-split` | | No | `false` | Skip split analysis; produce single-release validation only |
| `--r1-scope` | | No | `fidelity-schema` | Release 1 default scope bias: fidelity-schema, minimal-viable, custom |
| `--smoke-gate` | | No | `r2` | Default smoke gate placement: r1, r2 |
| `--agents` | `-a` | No | `opus:architect,haiku:analyzer` | Agent specs for variant generation in Part 2. Format: `model[:persona[:"instruction"]]`, comma-separated. Minimum 2 agents. |

## Behavioral Summary

4-part sequential protocol: Part 1 (Socratic discovery via `/sc:brainstorm` — find the natural split point or confirm none exists), Part 2 (adversarial variant generation and validation via `/sc:adversarial` Mode B — independent agents generate competing split proposals, then debate and merge), Part 3 (execution via the most appropriate command — produce release specs or tasklists), Part 4 (deep fidelity verification via `/sc:analyze` — auditable 100% coverage check). Produces 4-6 artifacts depending on split/no-split outcome. Explicitly neutral — "do not split" is a valid and potentially preferred outcome at every phase.

## Examples

### Analyze a Release Spec
```bash
/sc:release-split .dev/releases/backlog/v3.1/unified-audit-gating-v1.2.1-release-spec.md
```

### Deep Analysis with User Checkpoints
```bash
/sc:release-split .dev/releases/current/v4.0/spec.md --depth deep --interactive
```

### Resume from Prior Proposal
```bash
/sc:release-split .dev/releases/current/v3.1/spec.md \
  --resume-from .dev/releases/current/v3.1/release-split/split-proposal-final.md
```

### Validate an Intact Release (No Split)
```bash
/sc:release-split .dev/releases/current/v3.1/spec.md --no-split
```

### Multi-Agent Split Analysis
```bash
/sc:release-split .dev/releases/current/v4.0/spec.md \
  --agents opus:architect,sonnet:security --depth deep
```

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:release-split-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.

## Boundaries

**Will:**
- Analyze release artifacts for natural split points
- Produce neutral, evidence-based split/no-split recommendations
- Execute split decisions into concrete release specs or tasklists
- Verify 100% fidelity between original scope and split outputs
- Enforce real-world-only validation (no mocks, no synthetic tests)
- Gate Release 2 planning on Release 1 real-world validation

**Will Not:**
- Assume splitting is correct — "do not split" is always valid
- Produce tasklists or roadmaps directly (delegates to appropriate commands)
- Execute the resulting release plans
- Manage git operations or version control
- Treat mocked or simulated tests as valid evidence
- Allow Release 2 planning before Release 1 passes real-world validation

## Related Commands

| Command | Integration | Usage |
|---------|-------------|-------|
| `/sc:brainstorm` | Part 1 discovery | Socratic exploration of split points |
| `/sc:adversarial` | Part 2 validation | Generate competing split variants and merge via adversarial debate |
| `/sc:design` | Part 3 execution (specs) | Produce release specs if split approved |
| `/sc:workflow` | Part 3 execution (workflow) | Produce execution workflow if appropriate |
| `/sc:tasklist` | Part 3 execution (tasklists) | Produce tasklist bundles if appropriate |
| `/sc:analyze` | Part 4 verification | Deep fidelity and coverage analysis |
