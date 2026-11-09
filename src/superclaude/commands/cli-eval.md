---
name: cli-eval
description: "Manage the cliEval pipeline lifecycle — author a new eval suite (propose→critique→debate→author→validate→document) or interactively select and supervise a run of an existing suite."
category: testing
complexity: advanced
mcp-servers: [litellm, context7]
personas: [architect, analyzer, qa, scribe]
---

# /sc:cli-eval - cliEval Suite Lifecycle (create + run)

## Required Input

The first argument selects the pipeline (STOP if neither is given):

- `create` — author a NEW eval suite end-to-end.
- `run` — interactively select and supervise a run of an EXISTING suite.

## Usage

```bash
/sc:cli-eval create [--name <stem>] [--from @<design-or-spec>.md] [--agents <spec>[,...]]
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
| `--agents` | create | `default,default,default` | Three designs using the role-permitted configured child default (native model omitted). An explicit selection/persona/instruction list is forwarded unchanged, in order. |
| `--suite` | run | (menu) | Pre-select a suite by name; otherwise an interactive menu is shown |
| `--eval` | run | (all) | Pre-select a single eval id to drill into / filter |
| `--unattended` | both | off | Worker mode for a coordinator; applies only as a standalone argument token. Behaviour is in `## Unattended mode`; without it nothing changes |
| `--report-dir` | both | — | With `--unattended`: the directory that holds the worker contract and the report |

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

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:cli-eval` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (the `run` pipeline's `--output-dir` names the eval run directory, not the report directory). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, for both pipelines. `report_path` is the path of the run's `summary.md` inside the run directory (run) or of the design spec (create), never a bare file name. `artifacts` lists `summary.json` and the other files the run wrote; paths git ignores are left out (WC-4), and the report names the run directory. The skill's own `status` values `success`, `partial` and `failed` map to `succeeded`, `partial` and `failed`.
- **Person-mode flags.** None is refused.
- **Gates.** Under `--unattended` a missing pipeline (`create` or `run`) resolves as blocked, and so does every W0 "confirm with the user" case. `run` without both `--suite` and `--output-dir` resolves as blocked, with the missing flag named in `blocked_question`, so no suite menu is shown and two workers never share a run directory. The W3 "confirm the exact invocation" step is replaced by the command line as given: each other safety flag takes its command-line value or the CLI default, and the resolved set is the confirmed invocation. The doctor preflight still runs, and an FR-G5 preflight failure resolves as blocked, with the empty-HOME workaround offer in `blocked_question`; the empty-HOME workaround is not applied on the worker's own choice. The eval job is waited on in waits of at most 240 s each (WC-10), so the session can send a heartbeat between them, and the waits repeat until the job ends.
- **Nested invocations.** In the create pipeline `/sc:spec-panel` receives `--unattended --report-dir <report-dir>/nested/spec-panel-<n>/`, `sc:adversarial-protocol` receives `--unattended --output <report-dir>/nested/adversarial-<n>/`, and `/sc:document` receives `--unattended --report-dir <report-dir>/nested/document-<n>/` with an explicit `--output`, each `<n>` counting from 1 per nested command and never reused (a retry takes the next number); each contract is listed in `artifacts`, also when the call failed. `/sc:spec-panel` and `/sc:document` are command-only (no backing skill), so the create pipeline runs them as commands and never through the `Skill` tool; the `technical-writer` agent alternative for the documentation step is skipped under `--unattended` and recorded, because an agent run yields no nested directory. A nested contract is read by the nested-result rule of `~/.claude/WORKER-CONTRACT.md`.
- **Outward actions.** It pushes, commits and stages nothing.

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
