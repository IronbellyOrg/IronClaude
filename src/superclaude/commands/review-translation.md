---
name: review-translation
description: "Systematic localization review with adversarial validation, real-world evidence search, and comprehensive quality scoring"
category: orchestration
complexity: advanced
mcp-servers: [tavily, context7]
personas: [localization-reviewer, linguistic-validator, cultural-consultant, research-analyst]
---

# /sc:review-translation - Localization Quality Review System

> **Orchestration Command**: Manages a complete translation review workflow with parallel analysis, adversarial validation, and evidence-based scoring.

## Triggers

- Translation file review requests
- Localization quality assessment
- Multi-language content validation
- Software/game localization QA
- Marketing copy translation review

## Usage

```bash
/sc:review-translation [source-file] [translation-files...] [flags]

# Implicit trigger with files present:
"Review" | "Review these" | "Check translations"
```

### Flags

| Flag | Description |
|------|-------------|
| `--strict` | Enable strict validation mode |
| `--depth [level]` | quick, standard (default), deep |
| `--tone-matrix` | Enable quantified tone calibration |
| `--platform [name]` | steam, playstation, mobile, web, enterprise (default: auto) |
| `--export` | Generate team handoff format |
| `--context <file>` | A context summary the caller has already confirmed; with `--unattended` it is used as the Phase 1 confirmation |
| `--unattended` | Worker mode for a coordinator; applies only as a standalone argument token. Behaviour is in `## Unattended mode`; without it nothing changes |
| `--report-dir <dir>` | With `--unattended`: the directory that holds `return-contract.yaml` and `context-summary.md` |

## Behavioral Summary

7-phase localization review protocol: Phase 0 (file detection and technical validation), Phase 1 (context analysis with mandatory user confirmation gate), Phase 2 (review framework with 6-dimension weighted scoring), Phase 3 (parallel sub-agent deployment per language), Phase 4 (adversarial validation with tiered evidence search for Critical/High issues), Phase 5 (individual per-language reports), Phase 6 (project summary with release readiness), Phase 7 (implementation options). Produces scored reports with severity-classified findings and copy-paste JSON fixes.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:review-translation-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.

## Examples

### Basic Review

```bash
# Upload English source and translation files, then:
"Review"

# Or explicitly:
/sc:review-translation english.json de_DE.json fr_FR.json es_ES.json
```

### Deep Analysis with Tone Matrix

```bash
/sc:review-translation source.json translations/*.json --depth deep --tone-matrix
```

### Platform-Specific Review

```bash
/sc:review-translation steam_page.json translations/*.json --platform steam --strict
```

### Team Export

```bash
/sc:review-translation source.json *.json --export
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:review-translation` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only. Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the concrete path of the `reports/localization/PROJECT_SUMMARY_*.md` file this run wrote (the path itself, never the pattern), or `<report-dir>/context-summary.md` when the run is blocked at Phase 1. `artifacts` lists every `reports/localization/[lang]_review_*.md` file written, and the context summary when the run is blocked; paths git ignores are left out (WC-4).
- **Person-mode flags.** None is refused.
- **Gates.** Under `--unattended` Phase 1 (the mandatory context confirmation) uses the summary in `--context <file>` as the confirmed context and does not wait. Phase 1 without `--context` resolves as blocked: the run writes the context summary to `<report-dir>/context-summary.md` and stops with the confirmation question in `blocked_question`; a re-run with `--context` is a fresh run. Phase 7 resolves to SKIP IMPLEMENTATION, so no fix is implemented. There is no other gate.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Perform comprehensive linguistic and cultural quality assessment
- Generate prioritized, actionable reports with evidence
- Implement confirmed fixes upon user request
- Search for real-world usage evidence to validate suggestions
- Apply platform-specific validation rules
- Provide structured adversarial validation with confidence levels

**Will Not:**

- Proceed with review before user confirms context analysis
- Mark subjective preferences as critical errors
- Implement changes without explicit user consent
- Replace professional human translator review for high-stakes content
- Modify protected elements (placeholders, brand terms) without approval

## CRITICAL BOUNDARIES

**MANDATORY CONFIRMATION GATE**: Phase 1 context analysis MUST receive user confirmation before any review work begins.

**Output Artifacts:**

1. Individual language reports (`reports/localization/[lang]_review_*.md`)
2. Project summary (`reports/localization/PROJECT_SUMMARY_*.md`)
3. Implementation task list with copy-paste JSON
4. Team export package (if `--export` flag used)

**Next Step**: After review, user chooses to implement fixes, provide feedback, export for team, or skip.
