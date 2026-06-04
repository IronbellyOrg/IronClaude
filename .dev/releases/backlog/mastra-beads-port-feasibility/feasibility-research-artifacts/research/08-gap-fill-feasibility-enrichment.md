# Research: 08 - Gap Fill - Feasibility Enrichment
**Investigation Type:** Targeted Doc Analyst / Code Tracer
**Scope:** `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/research-notes.md`; `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md`; `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/codebase-context.md`; `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/research-deep.md`; `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/06-docs-and-existing-feasibility-artifacts.md`; source files needed to cross-check enrichment codebase claims.
**Status:** Complete
**Date:** 2026-06-02
---

## Assigned Gap

Research gate RG-C1 asks whether the existing feasibility enrichment artifacts named in `research-notes.md` are real current-repo files and whether `06-docs-and-existing-feasibility-artifacts.md` incorrectly reported only `seed-brief.md` under `.dev/releases/backlog/mastra-beads-port-feasibility/`.

## Files Investigated

### Feasibility directory existence check

Current directory traversal at max depth 3 found these feasibility artifacts:

- `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/codebase-context.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/research-deep.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/merged-requirements.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/return-contract.yaml`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/base-selection.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/debate-transcript.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/diff-analysis.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/merged-output.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/merge-log.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/proposal-a.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/proposal-b.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/proposal-c.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/proposal-d.md`
- `.dev/releases/backlog/mastra-beads-port-feasibility/adversarial/refactor-plan.md`

Finding: the two enrichment files exist in current repo state. The prior inventory line saying only `seed-brief.md` existed under the feasibility directory is stale or was produced from an incomplete traversal/state snapshot.

### Initial source cross-check: shared pipeline surface

- `src/superclaude/cli/main.py:400-426` [CODE-VERIFIED] registers root commands `sprint`, `roadmap`, `cleanup-audit`, `tasklist`, `cli-portify`, `prd`, and `eval`. This supports the existing research-note warning that `pipeline/` is a package rather than a root command.
- `src/superclaude/cli/pipeline/process.py:73-95` [CODE-VERIFIED] builds the `claude --print --verbose ... --max-turns ... --output-format ...` command with optional `--model` and caller-provided extra args.
- `src/superclaude/cli/pipeline/process.py:114-147` [CODE-VERIFIED] launches the process with `subprocess.Popen`, writes the prompt to stdin, and removes prompt-as-argv behavior from the runtime path.
- `src/superclaude/cli/pipeline/models.py:40-120` [CODE-VERIFIED] defines `StepStatus`, `GateMode`, `SemanticCheck`, `GateCriteria`, and `Step`.
- `src/superclaude/cli/pipeline/models.py:126-234` [CODE-VERIFIED] defines `StepResult`, `Deliverable`, and `PipelineConfig`; current `PipelineConfig` includes cosmetic-remediation fields.
- `src/superclaude/cli/pipeline/gates.py:20-76` [CODE-VERIFIED] implements pure Python tiered gate validation from EXEMPT through STRICT.
- `src/superclaude/cli/pipeline/trailing_gate.py:93-228` [CODE-VERIFIED] implements daemon-thread trailing gate evaluation; `src/superclaude/cli/pipeline/trailing_gate.py:508-591` [CODE-VERIFIED] implements persistent deferred remediation logging.

Reconciliation: the codebase-context enrichment is directionally accurate for the core seam and portable gate/model claims, but some of its cited line numbers and LOC counts differ from current reads. Use the current source citations above rather than copying enrichment line numbers uncritically.

### Source cross-check: sprint, roadmap, tasklist surfaces

- `src/superclaude/cli/sprint/commands.py:71-118` [CODE-VERIFIED] exposes `sprint run` with index path, model/max-turns, dry-run, tmux toggle, and Claude Code permission flag choices.
- `src/superclaude/cli/sprint/commands.py:208-290` [CODE-VERIFIED] loads sprint config, performs fidelity preflight, dry-runs if requested, then launches tmux or foreground `execute_sprint`.
- `src/superclaude/cli/sprint/config.py:52-140` [CODE-VERIFIED] discovers phase files from `tasklist-index.md` references or directory scan and parses optional `Execution Mode` values.
- `src/superclaude/cli/sprint/process.py:88-121` [CODE-VERIFIED] wraps the shared `ClaudeProcess` with sprint-specific `stream-json` output and lifecycle hooks.
- `src/superclaude/cli/sprint/process.py:169-216` [CODE-VERIFIED] builds the current `/sc:task Execute all tasks in @<phase-file> --compliance strict --strategy systematic` prompt. Any generated docs/enrichment text saying `/sc:task-unified` is stale for current code.
- `src/superclaude/cli/sprint/executor.py:927-1073` [CODE-VERIFIED] implements ordered per-task execution with one subprocess per parsed task and post-task gates/hooks.
- `src/superclaude/cli/sprint/executor.py:1076-1115` [CODE-VERIFIED] implements the per-task subprocess path using base `ClaudeProcess` with `output_format="stream-json"`.
- `src/superclaude/cli/sprint/executor.py:1135-1151` [CODE-VERIFIED] preflights for the `claude` binary before sprint execution.
- `src/superclaude/cli/sprint/executor.py:1303-1478` [CODE-VERIFIED] implements phase isolation, `CLAUDE_WORK_DIR`, process polling, monotonic timeout, startup-stall and mid-stall watchdogs, and TUI updates.
- `src/superclaude/cli/sprint/monitor.py:253-429` [CODE-VERIFIED] parses incremental `stream-json`/NDJSON output in a background monitor and extracts assistant/user/tool signals.
- `src/superclaude/cli/sprint/tmux.py:81-169` [CODE-VERIFIED] launches the sprint in a tmux session, creates panes, attaches, and reads an exit-code sentinel.
- `src/superclaude/cli/roadmap/commands.py:32-209` [CODE-VERIFIED] accepts 1-3 positional input files and has options for resume, dry-run, validation, convergence, retrospective, TDD/PRD enrichment, compression, and cosmetic remediation.
- `src/superclaude/cli/roadmap/executor.py:0-9` [CODE-VERIFIED] describes the current roadmap executor as a 9-step pipeline delegating to shared `execute_pipeline()`.
- `src/superclaude/cli/roadmap/executor.py:23-69` [CODE-VERIFIED] imports shared pipeline executor/models/process plus roadmap extraction/generation/diff/debate/score/merge/spec-fidelity/wiring/remediation/certification gates and prompts.
- `src/superclaude/cli/roadmap/executor.py:1107-1118` [CODE-VERIFIED] invokes `ClaudeProcess` for roadmap steps with `output_format="text"` and optional tool-write mode.
- `src/superclaude/cli/roadmap/executor.py:1253-1287` [CODE-VERIFIED] defines `_ClaudeRunner` as a `run(prompt) -> str` adapter over `ClaudeProcess`.
- `src/superclaude/cli/tasklist/commands.py:15-82` [CODE-VERIFIED] exposes `tasklist validate` only, with roadmap/tasklist/TDD/PRD validation inputs.
- `src/superclaude/cli/tasklist/executor.py:191-218` and `src/superclaude/cli/tasklist/executor.py:251-263` [CODE-VERIFIED] build a single `tasklist-fidelity` step and execute it through the shared pipeline.
- `src/superclaude/cli/pipeline/__init__.py:23-89` [CODE-VERIFIED] exports pipeline analysis/gate/process/trailing-gate APIs; this confirms the shared `pipeline/` package surface even though no root `superclaude pipeline` command is registered.

Reconciliation: the enrichment’s major codebase framing is confirmed: current orchestration is Python-controlled, artifact/gate-centric, and tightly coupled to Claude Code at the subprocess/output-stream seam. The most important nuance for downstream feasibility writing is that sprint has both a per-phase freeform prompt path and a parsed per-task subprocess path; roadmap/tasklist use text-mode `ClaudeProcess` through the shared pipeline.

## Findings

### `research-notes.md`

- `research-notes.md` correctly lists all three seed/enrichment artifacts in the feasibility directory: `seed-brief.md`, `enrichment/codebase-context.md`, and `enrichment/research-deep.md`.
- The notes already distinguish `research-deep.md` as external-fact seed material requiring refresh. That status is appropriate because external claims about Mastra, Backlog.md, and Beads cannot be code-verified from this repository.
- The notes’ warning that generated docs and release docs are stale unless cross-validated is supported by this gap-fill pass.

### `seed-brief.md`

- The seed brief’s local codebase architecture claim that `ClaudeProcess` is the central runtime seam is [CODE-VERIFIED]. Current `pipeline/process.py` constructs and launches the `claude` subprocess, passes prompt via stdin, and supports `stream-json` or `text` output.
- The seed brief’s claim that `pipeline` is a flagship surface is [CODE-CONTRADICTED] if interpreted as `superclaude pipeline`; current root command registration does not include a `pipeline` command. It is [CODE-VERIFIED] only as a shared Python package surface exported by `src/superclaude/cli/pipeline/__init__.py`.
- The seed brief’s Stack D facts about Mastra/Backlog.md/Beads remain [UNVERIFIED] in this targeted code-tracing pass. Those belong to web research outputs and should not be treated as repository evidence.

### `enrichment/codebase-context.md`

- The file exists and is highly relevant to the feasibility report. It should have been included in `06-docs-and-existing-feasibility-artifacts.md` inventory and cross-validation.
- Its core architectural claim is [CODE-VERIFIED]: current SuperClaude has a narrow Claude Code runtime seam (`ClaudeProcess`) and a broader set of portable Python/Markdown assets around gates, models, pipeline analysis, sprint parsing, tasklists, roadmap gates/prompts, skills, and agents.
- Several line-number/LOC statements in the enrichment are stale or approximate. Examples: `trailing_gate.py` is currently 648 lines in the read output, not the enrichment’s `~650` exact-enough but still approximate; `pipeline/process.py` current read is 245 lines and line references match conceptually but should be refreshed before final citations; roadmap executor current docstring says 9-step, not an 8-step-only framing.
- Its “THE SINGLE RUNTIME SEAM” wording is useful but should be softened in synthesis: sprint has additional Claude-Code-specific surfaces (`stream-json` monitor, `/sc:task` prompt construction, tmux/session handling, hooks/permission modes), so replacing `ClaudeProcess` is central but not sufficient for parity.

### `enrichment/research-deep.md`

- The file exists and should be included in the existing feasibility artifact inventory.
- It is external research, not codebase verification. All Mastra/Backlog.md/Beads version, licensing, multi-tenancy, ACP, MCP, and storage claims are [UNVERIFIED] in this code-tracing pass unless separately validated by web research artifacts.
- Its local-fit assertions are useful hypotheses for final synthesis but must be separated from code-verified repository facts. In particular, claims that Mastra `AcpAgent` is an “exact structural replacement” for `ClaudeProcess` are [UNVERIFIED] in this code pass because Mastra source/docs were not read here.

### `06-docs-and-existing-feasibility-artifacts.md`

- The inventory statement at lines 10-23 is stale/incomplete. It says only `seed-brief.md` was found under the feasibility directory at max depth 4. Current traversal found both enrichment files, release-level files, and adversarial files.
- The rest of `06` contains useful code cross-validation, including many findings that overlap with and confirm this remediation pass. However, it is missing direct analysis of `enrichment/codebase-context.md` and `enrichment/research-deep.md`; therefore it underreports useful prior feasibility artifacts.

## Evidence Table

| Claim / artifact | Status | Evidence |
|---|---|---|
| `enrichment/codebase-context.md` exists in current repo state. | [CODE-VERIFIED] | Current directory traversal found `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/codebase-context.md`; file was read successfully. |
| `enrichment/research-deep.md` exists in current repo state. | [CODE-VERIFIED] | Current directory traversal found `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/research-deep.md`; file was read successfully. |
| `06-docs-and-existing-feasibility-artifacts.md` inventory that only `seed-brief.md` exists under the feasibility directory is current. | [CODE-CONTRADICTED] | Current traversal found `seed-brief.md`, `enrichment/*`, `adversarial/*`, `merged-requirements.md`, and `return-contract.yaml`. |
| `research-notes.md` accurately identified the enrichment files. | [CODE-VERIFIED] | `research-notes.md` lists both enrichment files in the `EXISTING_FILES` table. |
| Current CLI root registers `pipeline` as a root command. | [CODE-CONTRADICTED] | `src/superclaude/cli/main.py:400-426` registers `sprint`, `roadmap`, `cleanup-audit`, `tasklist`, `cli-portify`, `prd`, and `eval`; no `pipeline` root command. |
| Current code has a shared pipeline package with models/gates/process/analysis exports. | [CODE-VERIFIED] | `src/superclaude/cli/pipeline/__init__.py:23-89` exports shared pipeline APIs; `models.py`, `gates.py`, `process.py`, and `trailing_gate.py` were read. |
| `ClaudeProcess` is a central Claude Code subprocess seam. | [CODE-VERIFIED] | `src/superclaude/cli/pipeline/process.py:73-95` builds the Claude command; `src/superclaude/cli/pipeline/process.py:114-147` launches it and sends prompt over stdin. |
| Sprint uses `stream-json` Claude Code output. | [CODE-VERIFIED] | `src/superclaude/cli/sprint/process.py:108-121` passes `output_format="stream-json"`; `src/superclaude/cli/sprint/monitor.py:253-429` parses incremental NDJSON. |
| Sprint currently prompts `/sc:task-unified`. | [CODE-CONTRADICTED] | `src/superclaude/cli/sprint/process.py:169-216` builds a `/sc:task Execute all tasks...` prompt. |
| Roadmap uses shared `execute_pipeline()` and current executor describes a 9-step pipeline. | [CODE-VERIFIED] | `src/superclaude/cli/roadmap/executor.py:0-9` states 9-step pipeline and delegates to `execute_pipeline()`; imports at `src/superclaude/cli/roadmap/executor.py:23-69`. |
| `tasklist` currently includes generation as a root CLI behavior. | [CODE-CONTRADICTED] | `src/superclaude/cli/tasklist/commands.py:15-82` exposes validation command surface; `src/superclaude/cli/tasklist/executor.py:191-218` builds only `tasklist-fidelity`. |
| Mastra/Backlog.md/Beads external claims in `research-deep.md` are code-verified by this pass. | [UNVERIFIED] | External docs/repos were not fetched in RG-C1. Treat `research-deep.md` as external-seed material to reconcile against web research outputs. |

## Required Corrections to Prior Research

1. Correct `06-docs-and-existing-feasibility-artifacts.md` inventory line that says only `seed-brief.md` exists under `.dev/releases/backlog/mastra-beads-port-feasibility/`.
2. Add `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/codebase-context.md` to `06` as an investigated artifact with a cross-validation table.
3. Add `.dev/releases/backlog/mastra-beads-port-feasibility/enrichment/research-deep.md` to `06` as an investigated artifact, but mark its claims as external research seeds unless separately web-verified.
4. Update any synthesis inputs that relied on `06`’s negative result. The correct state is: feasibility directory contains seed brief, two enrichment files, adversarial artifacts, merged requirements, and return contract.
5. Preserve `06`’s existing code-verification findings, but distinguish them from the newly reconciled enrichment files.
6. In final feasibility synthesis, cite current source reads for line-level code claims rather than relying on enrichment line numbers.

## Gaps and Questions

- [UNVERIFIED] Exact current external facts in `research-deep.md` still need to be reconciled against web research outputs before final report claims: Mastra latest version/license/RBAC/ACP, Backlog.md MCP/task schema, and Beads storage/MCP/multi-writer claims.
- [UNVERIFIED] Hook-specific claims in `codebase-context.md` were not fully traced in RG-C1. This pass focused on the feasibility enrichment reconciliation and core runtime seam.
- [CODE-CONTRADICTED] Any statement that current code exposes `superclaude pipeline` as a root CLI command should be corrected to “shared `pipeline/` package/API.”
- [CODE-CONTRADICTED] Any statement that current sprint prompt uses `/sc:task-unified` should be corrected to `/sc:task`.
- [CODE-CONTRADICTED] Any statement that `06` found all feasibility directory artifacts should be corrected; it missed the enrichment and adversarial/release-level files present now.

## Stale Documentation Found

| Document | Stale / incomplete statement | Correction |
|---|---|---|
| `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/06-docs-and-existing-feasibility-artifacts.md` | “No additional files beyond `seed-brief.md` were found under `.dev/releases/backlog/mastra-beads-port-feasibility/`.” | Current repo includes `enrichment/codebase-context.md`, `enrichment/research-deep.md`, adversarial artifacts, `merged-requirements.md`, and `return-contract.yaml`. |
| `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md` | Wording can imply `superclaude pipeline` is a root CLI command. | Treat `pipeline/` as a shared package/API, not a registered root Click command. |
| Generated/derived sprint references cited by prior research | `/sc:task-unified` prompt naming. | Current sprint prompt uses `/sc:task Execute all tasks...`. |
| `enrichment/codebase-context.md` | Some line refs/LOC and “single seam” wording are approximate. | Use refreshed source citations; treat `ClaudeProcess` as central but not the only parity concern. |

## Summary

RG-C1 is a real prior-research inventory gap, not an absence of files. The enrichment files exist in current repository state and should be included in the feasibility artifact analysis. `research-notes.md` was correct to list them; `06-docs-and-existing-feasibility-artifacts.md` needs correction because its inventory reported only `seed-brief.md` under the feasibility directory.

The codebase-context enrichment is broadly useful and its main local architecture claims are confirmed: SuperClaude’s current orchestration is Python-controlled, gate/artifact-centric, and coupled to Claude Code through the `ClaudeProcess` subprocess seam plus sprint-specific stream parsing, prompt dispatch, tmux/session, and permission/hook surfaces. The research-deep enrichment should be treated as external seed material, not local code verification, and reconciled with web research before final feasibility recommendations.

Exact remediation: amend the prior `06` artifact inventory and downstream synthesis inputs to include both enrichment files, mark `research-deep.md` external claims as [UNVERIFIED] unless web-verified elsewhere, and use refreshed source citations for any final codebase claims.
