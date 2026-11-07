---
name: release-split
description: "Neutral two-phase release split analysis with adversarial validation and fidelity verification"
category: planning
complexity: advanced
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
mcp-servers: [context7]
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
  --agents opus:architect:"Focus on dependency isolation",sonnet:analyzer:"Prioritize testability"
```

## Options

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<spec-file-path>` | | Yes | - | Path to release artifact to analyze |
| `--output` | `-o` | No | `<spec-dir>/release-split/` | Output directory for all artifacts. **Policy:** `--output` paths under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` are refused before any write — those prefixes are reserved for distributable components. Redirect to `.dev/` (e.g., `.dev/releases/current/<release-name>/` or `.dev/eval-workspaces/<skill-name>/`). See `.dev/README.md`. |
| `--depth` | `-d` | No | `standard` | Analysis depth: quick, standard, deep |
| `--interactive` | `-i` | No | `false` | Pause for user confirmation between phases |
| `--resume-from` | | No | - | Path to pre-validated split proposal; skips Parts 1-2 |
| `--no-split` | | No | `false` | Skip split analysis; produce single-release validation only |
| `--r1-scope` | | No | `fidelity-schema` | Release 1 default scope bias: fidelity-schema, minimal-viable, custom |
| `--smoke-gate` | | No | `r2` | Default smoke gate placement: r1, r2 |
| `--agents` | `-a` | No | `opus:architect,sonnet:analyzer` | Agent specs for variant generation in Part 2. Format: `model[:persona[:"instruction"]]`, comma-separated. Minimum 2 agents. |
| `--unattended` | | No | `false` | Worker mode for a coordinator; applies only as a standalone argument token. Behaviour is in `## Unattended mode`; without it nothing changes. |
| `--report-dir` | | No | - | With `--unattended`: the report directory, instead of `--output`, never both (see `## Unattended mode`). |

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

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:release-split` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** Exactly one of `--output <dir>` (short form `-o`) or `--report-dir <dir>`; both, or neither, is refused before any work and the refusal is printed in chat only. `--report-dir` follows the same path rules as `--output`, and a directory the caller passes is used exactly as passed. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome and holds the skill's return-contract fields beside the worker fields. `report_path` is `<report-dir>/release-split-report.md`, the skill's `<output>/release-split-report.md`. `artifacts` lists the skill's `artifacts` paths and the nested contracts, also when a nested call failed; paths git ignores are left out (WC-4). The status maps `split-approved` and `no-split` to `succeeded`, `split-with-remediation` to `partial`, and `failed` to `failed`.
- **Person-mode flags.** `--interactive` and its short form `-i` are refused before any work (contract `worker_status: failed`, the flag in `reason`).
- **Gates.** Under `--unattended` the tasklist-input warning resolves as blocked, with the question whether the file is a spec in `blocked_question`; `--r1-scope custom` resolves as blocked, with the Release 1 scope question in `blocked_question`. The convergence band that would prompt in interactive mode (0.5 to 0.59) aborts as it does today in non-interactive mode. There is no other gate.
- **Nested invocations.** The Part 1 `sc:brainstorm` call receives `--unattended --output <report-dir>/nested/brainstorm-<n>/` and the Part 2 `sc:adversarial-protocol` call receives `--unattended --output <report-dir>/nested/adversarial-<n>/`, each `<n>` counting from 1 per nested command and never reused (a retry or the Mode A fallback takes the next number). Part 3 writes the specs inline and Part 4 uses inline verification, so neither makes a nested call. A nested contract is read by the nested-result rule of `~/.claude/WORKER-CONTRACT.md`.
- **Outward actions.** It pushes, commits and stages nothing.

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
