---
name: cli-eval
description: "Manage the cliEval pipeline lifecycle — author a new eval suite (propose→critique→debate→author→validate→document) or interactively select and supervise a run of an existing suite."
category: testing
complexity: advanced
mcp-servers: [sequential, context7, serena]
personas: [architect, analyzer, qa, scribe]
---

# /sc:cli-eval - cliEval Suite Lifecycle (create + run)

## Required Input

The first argument selects the pipeline (STOP if neither is given):

- `create` — author a NEW eval suite end-to-end.
- `run` — interactively select and supervise a run of an EXISTING suite.

## Usage

```bash
/sc:cli-eval create [--name <stem>] [--from @<design-or-spec>.md] [--agents opus,sonnet,haiku]
/sc:cli-eval run    [--suite <name>] [--eval <id>]
```

The `run` pipeline is interactive: it enumerates suites via the CLI, presents a menu, confirms the
exact invocation and safety flags with you, then monitors a live run. It adds **no new flags** to the
underlying `superclaude eval` CLI — selection and monitoring are orchestration this command performs.

## Options

| Flag | Pipeline | Default | Description |
|------|----------|---------|-------------|
| `create` / `run` | — | — | Pipeline selector (positional `$1`, required) |
| `--name` | create | derived | Snake_case stem for the new suite (`<stem>.yaml`, must equal `name:`) |
| `--from` | create | — | Seed design/spec file (`@path`) for the critique + variant generation |
| `--agents` | create | `opus,sonnet,haiku` | Advocate specs for adversarial variant generation |
| `--suite` | run | (menu) | Pre-select a suite by name; otherwise an interactive menu is shown |
| `--eval` | run | (all) | Pre-select a single eval id to drill into / filter |

## Behavioral Summary

Both pipelines begin with a **mandatory fresh-context load**: the current eval docs, suite schema,
and CLI flag surface are re-read and cited before any action — the command never reasons from a
hardcoded flag list or schema field.

- **create**: draft a design → critique with `/sc:spec-panel` → generate 2-3 competing suite designs
  and debate/merge with `/sc:adversarial` → author `suites/<stem>.yaml` (schema-first) → **validate**
  with `superclaude eval describe --suite <stem>` (done-ness gate) → update the suites docs.
- **run**: `superclaude eval list --json` → interactive suite menu → optional `eval describe` drill →
  confirm invocation + safety flags (FR-G5 coverage gate, `--no-pty` skip behavior) → monitor a live
  `eval run` → parse `summary.json` → report per-eval status, run-dir, and preserved failed-HOME paths.

## Examples

```bash
# Author a new suite from a seed design, validate it schema-first, document it
/sc:cli-eval create --name eval_cli_doc_parity --from @.dev/eval-workspaces/cli-eval/design/doc-parity.md

# Pick a suite from an interactive menu and supervise the run
/sc:cli-eval run

# Pre-select the smoke suite and drill into one eval before running
/sc:cli-eval run --suite eval_smoke --eval ES1
```

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:cli-eval-protocol

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.

## Boundaries

**Will:**

- Re-read the live eval contract surface and cite it before acting (both pipelines).
- Author suites schema-first and treat `eval describe` exit 0 as the only "done".
- Supervise a real run, surface FAIL/ERRORED/TIMEOUT and non-zero exits, and point at forensic HOMEs.

**Will Not:**

- Add or change any flag on the `superclaude eval` CLI (run selection/monitoring is orchestration).
- Reinvent spec critique, debate/merge, or doc-writing (reuses `/sc:spec-panel`, `/sc:adversarial`,
  `/sc:document`).
- Declare a suite done without schema validation, or present a non-green run as green.

## Related Commands

| Command | Integration | Usage |
|---------|-------------|-------|
| `/sc:spec-panel` | create | Multi-expert critique of the eval-suite design spec |
| `/sc:adversarial` | create | Debate/merge competing suite designs (Mode-A `--compare` / Mode-B `--generate`) |
| `/sc:document` | create | Update the suites-guide inventory + suites/README table |
