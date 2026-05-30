---
name: sc:roadmap
description: Generate roadmap pipeline artifacts from 1-3 specification, TDD, and PRD markdown inputs. Mirrors the CLI `superclaude roadmap run` surface, including resume, dry-run, convergence, source-enrichment, compression, and cosmetic-remediation flags.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
---

# /sc:roadmap — Roadmap Generator

## Trigger

When the user requests roadmap generation from one to three markdown inputs: spec, TDD, and/or PRD. Input content type is auto-detected by default; `--input-type` may override single-file detection.

## Usage

```bash
/sc:roadmap [OPTIONS] INPUT_FILES...
```

`INPUT_FILES` accepts 1-3 markdown files in any order. Provide at most one spec, one TDD, and one PRD. By default, outputs are written to the parent directory of the first input file unless `--output` is provided.

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `INPUT_FILES...` | Yes | - | 1-3 markdown files: spec, TDD, and/or PRD in any order. Content type is auto-detected. |
| `--agents TEXT` | No | `opus:architect,sonnet:architect` | Comma-separated agent specs: `model[:persona]`. |
| `--output PATH` | No | Parent dir of spec-file | Output directory for all artifacts. |
| `--depth quick\|standard\|deep` | No | `standard` | Debate round depth: `quick=1`, `standard=2`, `deep=3`. |
| `--resume` | No | `false` | Skip steps whose outputs already pass their gates. Re-run from the first failing step. |
| `--dry-run` | No | `false` | Print step plan and gate criteria, then exit without launching subprocesses. |
| `--model TEXT` | No | Per-agent model for generate steps | Override model for all steps. |
| `--max-turns INTEGER` | No | `100` | Max agent turns per Claude subprocess. |
| `--debug` | No | `false` | Enable debug logging to `output_dir/roadmap-debug.log`. |
| `--no-validate` | No | `false` | Skip post-pipeline validation step. |
| `--allow-regeneration` | No | `false` | Allow patches that exceed the diff-size threshold (FR-9). Use with caution. |
| `--no-convergence` | No | `false` | Disable the spec-fidelity convergence engine and use the single-shot LLM check instead. |
| `--retrospective PATH` | No | - | Path to a retrospective file from a prior release cycle. Missing file is not an error; extraction proceeds normally. |
| `--input-type auto\|tdd\|spec` | No | `auto` | Input file type. `auto` detects PRD, TDD, or spec from content; `tdd`/`spec` force type for a single file. PRD files are auto-detected when positional. |
| `--tdd-file PATH` | No | - | Supplementary TDD context when the primary input is a spec. Provides data models, API endpoints, component inventory, and test strategy detail. Ignored when the primary input is itself a TDD unless `--input-type spec` forces spec mode. |
| `--prd-file PATH` | No | - | Supplementary PRD context. Provides personas, success metrics, compliance requirements, and scope boundaries. Works with spec or TDD primary inputs and is auto-wired from `.roadmap-state.json` on `--resume` when omitted. |
| `--no-compress` | No | `false` | Disable lossless markdown compression of LLM-consumed inputs while deterministic steps continue reading originals. |
| `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` | No | enabled | Auto-fix pure-cosmetic gate failures before halting. Semantic failures always halt. |
| `--strict-no-remediation` | No | `false` | Disable cosmetic-failure auto-remediation entirely. Equivalent to `--no-allow-cosmetic-remediation`; explicit alias for high-stakes runs. |
| `--help` | No | - | Show CLI help and exit. |

## Deprecated / unsupported inference-only flags

The current CLI surface does not support the older inference-only command flags `--specs`, `--template` / `-t`, `--multi-roadmap`, `--interactive` / `-i`, `--compliance` / `-c`, or `--persona` / `-p`. Use positional `INPUT_FILES...`, `--agents`, `--depth`, and the CLI validation/convergence flags above instead.

## Examples

```bash
# Basic: one specification file
/sc:roadmap spec.md

# TDD-enriched roadmap generation
/sc:roadmap spec.md tdd.md

# Spec, TDD, and PRD inputs in one run
/sc:roadmap spec.md tdd.md prd.md

# Custom output directory
/sc:roadmap spec.md --output .dev/releases/current/example-release/

# Resume from the first failing or missing step
/sc:roadmap spec.md --output .dev/releases/current/example-release/ --resume

# Preview step plan and gate criteria without launching subprocesses
/sc:roadmap spec.md --dry-run

# Deep debate with explicit agents
/sc:roadmap spec.md --agents opus:architect,sonnet:qa --depth deep

# High-stakes run with cosmetic auto-remediation disabled
/sc:roadmap spec.md --strict-no-remediation
```

## Output Layout

The CLI writes all generated artifacts to `--output` when provided; otherwise it writes to the parent directory of the first input file. Pipeline artifacts include roadmap outputs, extraction/test-strategy artifacts, debug logs when `--debug` is set, and validation artifacts unless `--no-validate` is set.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:roadmap-protocol

Pass all user-provided arguments (input files and flags) verbatim to the Skill invocation via the `args` parameter.

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.

**Relationship to the CLI:** The CLI `superclaude roadmap run [OPTIONS] INPUT_FILES...` is the deterministic counterpart of this slash command. This command mirrors the CLI run surface; the backing protocol skill supplies the inference workflow and must preserve CLI-faithful behavior where the release decision selected CLI convergence.

## Boundaries

**Will do**: Generate roadmap pipeline artifacts from 1-3 markdown inputs; route spec/TDD/PRD content through CLI-faithful input detection and source-enrichment behavior; support resume, dry-run, convergence, compression, validation, and cosmetic-remediation controls; write outputs only to the CLI output directory.

**Will not do**: Accept comma-separated `--specs`; select templates via `--template`; use `--multi-roadmap`, `--interactive`, `--compliance`, or `--persona`; generate tasklists; execute implementation; trigger downstream commands automatically; modify source specification, TDD, or PRD files.

## See Also

- `/sc:validate-roadmap` — Validate roadmap pipeline outputs
- `/sc:tasklist` — Generate Sprint-compatible tasklists from validated roadmap artifacts
- `superclaude roadmap run --help` — CLI counterpart and canonical flag surface
