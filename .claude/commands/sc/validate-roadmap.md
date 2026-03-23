---
name: validate-roadmap
description: "Validate roadmap fidelity against source specifications with multi-agent coverage analysis, adversarial review, and remediation planning. Use this whenever you need to verify a roadmap covers all spec requirements, check for gaps between specs and roadmaps, or audit roadmap completeness before tasklist generation."
category: analysis
complexity: advanced
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
mcp-servers: [sequential]
personas: [analyzer, architect, qa]
---

# /sc:validate-roadmap - Roadmap-to-Spec Fidelity Validator

Prove — or disprove — that a roadmap covers 100% of the requirements from its source specifications. Adversarial by default: the roadmap is incomplete until proven otherwise.

## Usage

```bash
/sc:validate-roadmap <roadmap-path> --specs <spec1.md,spec2.md,...> [options]
```

## Arguments

- `roadmap-path`: Path to the roadmap under validation (required)

## Flags

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `--specs` | `-s` | Yes | - | Comma-separated spec file paths (1-10) |
| `--output` | `-o` | No | `{roadmap-dir}/validation/` | Output directory for validation artifacts |
| `--exclude` | `-x` | No | - | Comma-separated domains to exclude from validation |
| `--depth` | `-d` | No | `standard` | Analysis depth: quick, standard, deep |
| `--max-agents` | | No | `20` | Maximum parallel validation agents (4-20) |
| `--skip-adversarial` | | No | `false` | Skip Phase 4 adversarial pass |
| `--skip-remediation` | | No | `false` | Skip Phase 5 remediation plan |
| `--report` | `-r` | No | - | Also write summary to specified path |

## Examples

```bash
# Basic: validate roadmap against its release spec
/sc:validate-roadmap .dev/releases/current/v3.0/roadmap.md \
  --specs .dev/releases/current/v3.0/release-spec.md

# Multiple specs with deep analysis
/sc:validate-roadmap .dev/releases/current/v4.0/roadmap.md \
  --specs .dev/releases/current/v4.0/release-spec.md,.dev/releases/current/v4.0/tech-spec.md \
  --depth deep

# Quick check excluding documentation domain
/sc:validate-roadmap roadmap.md --specs spec.md --depth quick --exclude documentation

# Custom output directory
/sc:validate-roadmap roadmap.md --specs spec.md \
  --output .dev/releases/current/v3.0/validation/
```

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc-validate-roadmap-protocol

Pass all user-provided arguments (roadmap path, flags) verbatim to the Skill invocation via the `args` parameter.

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.

## Boundaries

**Will:**
- Extract all requirements from spec files into a structured registry
- Validate every requirement against the roadmap with evidence-based coverage assessment
- Spawn parallel domain agents for independent validation
- Run adversarial review challenging COVERED assessments
- Produce consolidated report with GO/CONDITIONAL_GO/NO_GO verdict
- Generate dependency-ordered remediation plan for gaps
- Preserve all intermediate artifacts as evidence trail

**Will Not:**
- Modify the roadmap or spec files
- Execute remediation — only plans it
- Trigger downstream commands (tasklist generation, implementation)
- Validate code or test execution — only document coverage
- Resolve spec-internal contradictions — flags them for human decision

## See Also

- `/sc:roadmap` - Generate roadmaps from specifications
- `/sc:tasklist` - Generate tasklists from roadmaps
- `/sc:adversarial` - Structured adversarial debate pipeline
- `/sc:analyze` - General code analysis
