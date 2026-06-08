# Research: 06 - Documentation and Existing Feasibility Artifacts
**Investigation type:** Doc Analyst
**Scope:** `.dev/releases/backlog/mastra-beads-port-feasibility/`, `docs/guides/cli-portify-and-pipeline-runner-guide.md`, `docs/generated/cli-portify-release-guide.md`, `docs/generated/sprint-cli/`, `docs/generated/contributor-knowledge-base/`, `docs/analysis/skill-vs-cli-divergence-roadmap.md`, `.dev/releases/complete/v2.*cli-portify*`, `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/artifacts/dependency-map.md`
**Status:** Complete
**Date:** 2026-06-02
---

## Inventory

Requested artifacts found in current repository:

- `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md` (only file under that feasibility directory at max depth 4)
- `docs/guides/cli-portify-and-pipeline-runner-guide.md`
- `docs/generated/cli-portify-release-guide.md`
- `docs/generated/sprint-cli/` (11 top-level generated sprint CLI docs plus debates and v3.7 refactor subdocs)
- `docs/generated/contributor-knowledge-base/` (8 generated contributor docs)
- `docs/analysis/skill-vs-cli-divergence-roadmap.md`
- `.dev/releases/complete/v2.15-cli-portify/`, `v2.18-cli-portify-v2/`, `v2.23-cli-portify-v3/`, `v2.24-cli-portify-cli-v4/`, `v2.24.1-cli-portify-cli-v5/`, `v2.25-cli-portify-cli/` matching `.dev/releases/complete/v2.*cli-portify*`
- `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/artifacts/dependency-map.md`

Negative result:

- No additional files beyond `seed-brief.md` were found under `.dev/releases/backlog/mastra-beads-port-feasibility/` with the requested traversal.

## Current Code Verification Baseline

These source-of-truth code observations anchor the doc cross-validation below.

| Current code fact | Evidence |
|---|---|
| `superclaude` console script routes to `superclaude.cli.main:main`; an additional `ic` script also exists. | `pyproject.toml:65-67` |
| Root Click group is `main`; registered subcommands include `sprint`, `roadmap`, `cleanup-audit`, `tasklist`, `cli-portify`, `prd`, and `eval`. | `src/superclaude/cli/main.py:18-26`, `src/superclaude/cli/main.py:400-426` |
| Shared pipeline models include `StepStatus`, `GateMode`, `SemanticCheck`, `GateCriteria`, `Step`, `StepResult`, `Deliverable`, and `PipelineConfig`; `PipelineConfig` now includes cosmetic-remediation fields beyond older docs. | `src/superclaude/cli/pipeline/models.py:40-120`, `src/superclaude/cli/pipeline/models.py:126-234` |
| Shared pipeline executor accepts sequential steps and parallel step groups, runs gates, retries, and supports trailing gates plus deferred trailing step execution after a halt. | `src/superclaude/cli/pipeline/executor.py:63-98`, `src/superclaude/cli/pipeline/executor.py:104-188`, `src/superclaude/cli/pipeline/executor.py:191-388` |
| Shared `ClaudeProcess` builds `claude --print --verbose <permission> --no-session-persistence --tools default --max-turns N --output-format <format>` and now writes the prompt through stdin, not argv `-p`. | `src/superclaude/cli/pipeline/process.py:73-95`, `src/superclaude/cli/pipeline/process.py:114-147` |
| Gate validation is pure Python by tier: EXEMPT, LIGHT, STANDARD, STRICT; STRICT invokes semantic checks. | `src/superclaude/cli/pipeline/gates.py:20-76` |
| Sprint CLI `run` accepts tasklist index, phase range, model/max-turns, tmux, permission flag, dry-run, stall controls, shadow gates, fidelity overrides, release/state dirs. | `src/superclaude/cli/sprint/commands.py:71-207` |
| Sprint dispatch loads config, optionally dry-runs, then launches tmux or foreground `execute_sprint`. | `src/superclaude/cli/sprint/commands.py:219-290` |
| Sprint config discovers phase files from the index/table or directory scan; parses `Execution Mode` values `claude`, `python`, `skip`; parses task headings/dependencies/commands/classifiers. | `src/superclaude/cli/sprint/config.py:52-140`, `src/superclaude/cli/sprint/config.py:399-423` |
| Sprint-specific `ClaudeProcess` wraps the shared process with output format `stream-json` and builds a `/sc:task Execute all tasks in @<phase-file> --compliance strict --strategy systematic` prompt. | `src/superclaude/cli/sprint/process.py:88-121`, `src/superclaude/cli/sprint/process.py:123-216` |
| Sprint executor has a per-task path (`execute_phase_tasks`) and a freeform phase path; per-task execution iterates input order and spawns one subprocess per task. | `src/superclaude/cli/sprint/executor.py:927-1073`, `src/superclaude/cli/sprint/executor.py:1259-1301`, `src/superclaude/cli/sprint/executor.py:1303-1557` |
| Roadmap CLI accepts 1-3 positional inputs and supports TDD/PRD routing, validation toggle, convergence toggle, compression toggle, cosmetic remediation toggle, and other options. | `src/superclaude/cli/roadmap/commands.py:32-196` |
| Roadmap executor is currently described in code as a 9-step pipeline with parallel generate group and uses inline-embedded inputs; current imports include anti-instinct, spec-fidelity, wiring, deviation/remediation, and certification gates beyond a simple 8/9-step description. | `src/superclaude/cli/roadmap/executor.py:1-10`, `src/superclaude/cli/roadmap/executor.py:24-69` |
| Roadmap input routing supports PRD/TDD/spec auto-detection and 1-3 positional files; it does not implement a `--specs` consolidation flag. | `src/superclaude/cli/roadmap/executor.py:74-214`, `src/superclaude/cli/roadmap/executor.py:214-240` |
| Tasklist CLI currently exposes `tasklist validate`, not tasklist generation; it auto-wires TDD/PRD from `.roadmap-state.json` and executes a single tasklist-fidelity step through the shared pipeline. | `src/superclaude/cli/tasklist/commands.py:15-82`, `src/superclaude/cli/tasklist/commands.py:113-185`, `src/superclaude/cli/tasklist/executor.py:191-218`, `src/superclaude/cli/tasklist/executor.py:251-260` |
| CLI Portify code exposes `superclaude cli-portify run TARGET`; it validates workflow path/SKILL.md, output writability, name derivation/collision, and runs a sequential step registry with return contract emission. | `src/superclaude/cli/cli_portify/commands.py:14-27`, `src/superclaude/cli/cli_portify/commands.py:30-131`, `src/superclaude/cli/cli_portify/config.py:122-175`, `src/superclaude/cli/cli_portify/executor.py:105-183`, `src/superclaude/cli/cli_portify/executor.py:283-360` |
| `/sc:cli-portify` command markdown still requires invoking `sc:cli-portify-protocol`; the protocol skill claims it generates a CLI package, but the current Python CLI Portify runner implements an artifact-producing planning pipeline rather than direct code generation in `run_portify`. | `src/superclaude/commands/cli-portify.md:76-91`, `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:29-50`, `src/superclaude/cli/cli_portify/executor.py:1-15` |
| CLI Portify full-workflow resolution from prior v2.24.1 planning is now partially implemented: `resolution.py` supports 6 input forms and `discover_components.py` includes agent extraction patterns; current source still uses `commands.py`, not the old `cli.py` module named by some release docs. | `src/superclaude/cli/cli_portify/resolution.py:1-22`, `src/superclaude/cli/cli_portify/resolution.py:54-169`, `src/superclaude/cli/cli_portify/steps/discover_components.py:56-180`, `src/superclaude/cli/cli_portify/commands.py:1-27` |

## Doc Claim Cross-Validation Tables

### A. Feasibility Seed Brief: Mastra + Backlog.md + Beads

Source: `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md`.

| Doc claim | Status | Code verification / notes |
|---|---|---|
| Current SuperClaude/IronClaude ships a Python orchestration layer under `src/superclaude/cli/` with flagship `sprint`, `roadmap`, `pipeline`, `tasklist`, `task_builder`/supporting generators. | [CODE-VERIFIED] for `src/superclaude/cli/` orchestration; [CODE-CONTRADICTED] for current root CLI list if interpreted as complete because current `main.py` also registers `cleanup-audit`, `cli-portify`, `prd`, and `eval`, and no root `pipeline` command is registered. | CLI registrations are in `src/superclaude/cli/main.py:400-426`; `pipeline/` is a shared package, not a root Click command, per `src/superclaude/cli/pipeline/__init__.py:1-21`. |
| `superclaude sprint run <tasklist-index.md>` executes MDTM task phases by spawning `claude --print --verbose --output-format stream-json` subprocesses, with checkpoints, tmux, KPI/diagnostics, and recoverability. | [CODE-VERIFIED] with nuance: sprint subprocess path and tmux/diagnostics exist; per-task rerun is not in the lines read, but later project memory says a `rerun-tasks` verb exists and should be independently verified if this report depends on it. | Sprint command and dispatch: `src/superclaude/cli/sprint/commands.py:71-290`; sprint process uses stream-json: `src/superclaude/cli/sprint/process.py:88-121`; executor initializes TUI/logging/TurnLedger/remediation and preflight: `src/superclaude/cli/sprint/executor.py:1135-1234`; checkpoint enforcement exists at `src/superclaude/cli/sprint/executor.py:1512-1524`. |
| `superclaude roadmap run <spec.md>` is the largest subsystem and includes spec parsing, adversarial generation, convergence/gates/remediation/certification. | [CODE-VERIFIED] for the architecture classes of work, not LOC. | Roadmap command surface is in `src/superclaude/cli/roadmap/commands.py:32-196`; executor imports extraction, generate/diff/debate/score/merge, spec-fidelity, anti-instinct, remediation, certification, and wiring gates/prompts in `src/superclaude/cli/roadmap/executor.py:24-69`. |
| `superclaude pipeline` exists as a CLI surface for FMEA, dataflow graphs, invariants, guard analysis, conflict detection. | [CODE-CONTRADICTED] as a root CLI command; [CODE-VERIFIED] as a shared package API. | Root command registration does not add a `pipeline` command in `src/superclaude/cli/main.py:400-426`; shared pipeline exports FMEA/dataflow/guard/invariant/conflict functions in `src/superclaude/cli/pipeline/__init__.py:23-89`. |
| Execution substrate is a subprocess driver over `claude` CLI at the `ClaudeProcess` seam; porting to Mastra must replace that seam. | [CODE-VERIFIED] | `ClaudeProcess.build_command()` composes the `claude` command in `src/superclaude/cli/pipeline/process.py:73-95`; `start()` launches via `subprocess.Popen` and writes prompt to stdin in `src/superclaude/cli/pipeline/process.py:114-147`; sprint/roadmap/tasklist reuse this process wrapper. |
| Intelligence lives in on-disk skills, agents, commands, hooks; orchestration/gates/waves/checkpoints are Python. | [CODE-VERIFIED] for commands/skills/agents and Python orchestration/gates; [UNVERIFIED] for hooks in this investigation because hook code paths were not part of the requested source cross-check. | Command activation: `src/superclaude/commands/cli-portify.md:76-91`; skill protocol content: `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:12-150`; Python gates and executor: `src/superclaude/cli/pipeline/gates.py:20-76`, `src/superclaude/cli/pipeline/executor.py:63-188`. |
| Coupling point includes `['claude','--print','--verbose']`, `stream-json`, `max_turns`, `model`, and permission flags. | [CODE-VERIFIED] with nuance: output format is configurable (`stream-json` for sprint, `text` for roadmap/tasklist/cli-portify). | Base command includes `--print`, `--verbose`, permission flag, `--max-turns`, and configurable `--output-format` in `src/superclaude/cli/pipeline/process.py:73-95`; sprint passes `output_format="stream-json"` in `src/superclaude/cli/sprint/process.py:108-121`; tasklist passes `output_format="text"` in `src/superclaude/cli/tasklist/executor.py:130-140`. |
| Portable IP includes skills/agents/commands, gate logic, MDTM task format, checkpoint/retrospective models. | [CODE-VERIFIED] for skills/agents/commands/gates/checkpoints; [UNVERIFIED] for retrospective model as a reusable class in this pass. | Skills and command paths verified via `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:1-10` and `src/superclaude/commands/cli-portify.md:1-10`; gates via `src/superclaude/cli/pipeline/gates.py:20-76`; checkpoint enforcement via `src/superclaude/cli/sprint/executor.py:1512-1524`. |
| Claude-Code-specific pieces to re-home include CLI subprocess lifecycle, stream-json parsing, tmux, slash-command dispatch, permission flags, and hook events. | [CODE-VERIFIED] for subprocess lifecycle, stream-json, tmux decision, slash-command prompt dispatch, and permission flags; [UNVERIFIED] for hook events. | `src/superclaude/cli/pipeline/process.py:73-147`; `src/superclaude/cli/sprint/process.py:169-216`; tmux dispatch in `src/superclaude/cli/sprint/commands.py:286-290`; permission option in `src/superclaude/cli/sprint/commands.py:109-118`. |
| Stack D facts: Mastra, Backlog.md, and Beads version/license/server-mode facts. | [UNVERIFIED] in this doc-analysis pass. | These are explicitly marked by the seed as “to verify in research” and require external/current-source verification outside the repo; do not treat as current code facts. |

Key takeaways for report sections 1, 2, 4, 9, 10:

- The seed brief is mostly reliable about the local SuperClaude runtime seam: the highest-value feasibility framing is “replace `ClaudeProcess`/Claude Code subprocess semantics with a different workflow runtime.”
- Treat the `superclaude pipeline` wording as stale/loose. Current code has a rich `pipeline/` API package, not a top-level `superclaude pipeline` Click command.
- The Mastra/Backlog.md/Beads claims are not repo-verifiable and must be kept in the external-facts/risk register bucket.

### B. CLI Portify Guides and Generated Release Docs

Sources: `docs/guides/cli-portify-and-pipeline-runner-guide.md`, `docs/generated/cli-portify-release-guide.md`, `.dev/releases/complete/v2.*cli-portify*`.

| Doc claim | Status | Code verification / notes |
|---|---|---|
| CLI Portify is a workflow-to-pipeline compiler where Python controls flow, Claude fills structured artifacts, gates validate, and Claude does not decide next step. | [CODE-VERIFIED] as the architectural intent and current runner shape. | `src/superclaude/cli/cli_portify/executor.py:1-15` describes a sequential executor, gates, return contracts, diagnostics/TUI; `STEP_REGISTRY` controls steps at `src/superclaude/cli/cli_portify/executor.py:105-183`. |
| `docs/guides` says CLI runner layer includes `src/superclaude/cli/cli_portify/`, roadmap, tasklist, sprint, all built on shared `pipeline/`. | [CODE-VERIFIED] with nuance: sprint has its own executor and reuses pipeline process/models; tasklist/roadmap use shared `execute_pipeline`. | Registrations: `src/superclaude/cli/main.py:400-418`; tasklist uses `execute_pipeline` in `src/superclaude/cli/tasklist/executor.py:23-25`, `src/superclaude/cli/tasklist/executor.py:251-260`; sprint wraps base process in `src/superclaude/cli/sprint/process.py:88-121`. |
| Shared `PipelineConfig` fields are work_dir, dry_run, max_turns, model, permission_flag, debug, grace_period. | [CODE-CONTRADICTED] by additive drift: those fields exist, but current `PipelineConfig` also has `allow_cosmetic_remediation` and `cosmetic_remediator`. | `src/superclaude/cli/pipeline/models.py:212-234`. |
| `ClaudeProcess.build_command()` returns `claude --print --verbose ... --max-turns N --output-format text -p "prompt"`. | [CODE-CONTRADICTED] for prompt delivery: current `build_command()` no longer includes `-p`; prompt is written through stdin in `start()`. | Command construction: `src/superclaude/cli/pipeline/process.py:73-95`; stdin prompt delivery: `src/superclaude/cli/pipeline/process.py:114-147`. |
| `docs/generated/cli-portify-release-guide.md` describes a two-layer `/sc:cli-portify` command shim + protocol skill, not the Python `superclaude cli-portify run` runner. | [CODE-VERIFIED] as slash-command docs; [CODE-CONTRADICTED] if used as current Python CLI reference. | Slash command activation exists in `src/superclaude/commands/cli-portify.md:76-91`; current Python CLI runner exists separately in `src/superclaude/cli/cli_portify/commands.py:14-27`, `src/superclaude/cli/main.py:416-418`. |
| Generated release guide says CLI Portify `--dry-run` executes Phases 1-2 only and skips Phases 3-4. | [CODE-CONTRADICTED] for current Python CLI implementation: dry-run eligibility includes PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION phase types; the `commands.py` handler currently returns immediately after printing derived name when `dry_run` is true, before `run_portify`. | Dry-run early return in `src/superclaude/cli/cli_portify/commands.py:191-197`; executor dry-run phase-type constants in `src/superclaude/cli/cli_portify/executor.py:65-99`. |
| v2.24 release guide says module is `cli.py` and 7 steps (`analyze-workflow`, `design-pipeline`, `synthesize-spec`, `brainstorm-gaps`, `panel-review`). | [CODE-CONTRADICTED] by current code: current Click entry is `commands.py`, and `STEP_REGISTRY` includes 8 named registry steps with `protocol-mapping`, `analysis-synthesis`, `step-graph-design`, `models-gates-design`, `prompts-executor-design`, and `pipeline-spec-assembly` rather than the old names. | Current file list has `commands.py` and no `cli.py`; current step registry is `src/superclaude/cli/cli_portify/executor.py:105-183`. |
| v2.24.1 workflow-resolution spec says target resolution should accept command names/paths, skill dirs/names, `SKILL.md`, and `sc:` prefix and discover agents. | [CODE-VERIFIED] as substantially implemented. | `resolve_target()` supports all 6 input forms in `src/superclaude/cli/cli_portify/resolution.py:54-169`; agent extraction patterns exist in `src/superclaude/cli/cli_portify/steps/discover_components.py:56-180`; `PortifyProcess` supports `additional_dirs` in `src/superclaude/cli/cli_portify/process.py:121-177`. |
| v2.23/v2.24 docs say code generation was removed in favor of reviewed release specs feeding roadmap/tasklist/implementation. | [CODE-VERIFIED] for current protocol direction; [CODE-CONTRADICTED] by older SKILL wording that still says “What Gets Generated” as a CLI package. | Evolution spec states the change in `.dev/releases/complete/v2.23-cli-portify-v3/spec-cli-portify-workflow-evolution.md:17-24`, `:51-68`; current executor is artifact/contract pipeline in `src/superclaude/cli/cli_portify/executor.py:1-15`; current skill still says generated files in `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:29-50`. |

Key takeaways:

- Use v2.23+ “spec-driven planning, not direct code generation” as the correct framing for replatform feasibility.
- Avoid using the v2.24 release guide as current API reference without marking it historical; file names and step IDs have drifted.
- CLI Portify’s evolution is valuable precedent for Mastra replatforming: earlier attempts failed where docs/specs drifted from live APIs, and the successful direction was contract-first, gated, resumable, and source-verified.

### C. Sprint CLI Generated Docs

Sources: `docs/generated/sprint-cli/00-overview.md`, `01-entry-points.md`, `03-execution-engine.md`, plus sibling generated sprint docs by directory inventory.

| Doc claim | Status | Code verification / notes |
|---|---|---|
| Sprint CLI is a process orchestrator that launches Claude CLI subprocesses with `/sc:task-unified`/task prompts and monitors NDJSON/stream-json output. | [CODE-VERIFIED] with naming drift: current prompt uses `/sc:task`, not `/sc:task-unified`. | Process wrapper output format: `src/superclaude/cli/sprint/process.py:108-121`; current prompt string: `src/superclaude/cli/sprint/process.py:169-216`; executor monitors output and TUI: `src/superclaude/cli/sprint/executor.py:1308-1457`. |
| Generated docs line refs for `main.py` and sprint commands show only `sprint`, `roadmap`, `cleanup-audit` root workflow groups. | [CODE-CONTRADICTED] by current root registration drift. | Current `main.py` registers `tasklist`, `cli-portify`, `prd`, and `eval` in addition to `sprint`, `roadmap`, `cleanup-audit`: `src/superclaude/cli/main.py:400-426`. |
| Sprint command group has `run`, `attach`, `status`, `logs`, `kill`. | [CODE-VERIFIED] and incomplete: current file also has `verify-checkpoints` after the originally generated range. | `src/superclaude/cli/sprint/commands.py:71-357`, plus `verify-checkpoints` starts at `src/superclaude/cli/sprint/commands.py:360`. |
| `discover_phases()` reads tasklist index, regex-extracts phase filenames, parses optional `Execution Mode`, and falls back to directory scan. | [CODE-VERIFIED] | `src/superclaude/cli/sprint/config.py:52-140`. |
| Sprint task dependencies are parsed but not used for execution ordering; tasks execute in input order. | [CODE-VERIFIED] | Dependencies are parsed in `src/superclaude/cli/sprint/config.py:379-384` and task loop iterates `for i, task in enumerate(tasks)` in `src/superclaude/cli/sprint/executor.py:971-1010`. No dependency scheduler is used in `execute_phase_tasks`. |
| `execution/parallel.py` wave planner is standalone and not directly wired into sprint executor. | [CODE-VERIFIED] within this investigation by absence in the sprint executor paths read; direct `execution/parallel.py` was not re-read here. | Sprint executor per-task and freeform paths are in `src/superclaude/cli/sprint/executor.py:927-1073`, `src/superclaude/cli/sprint/executor.py:1259-1557`; they do not call `ParallelExecutor` in those paths. |
| Sprint process command includes `--output-format stream-json`; base process command includes `--no-session-persistence`, `--tools default`, max turns, permission flag. | [CODE-VERIFIED] | `src/superclaude/cli/pipeline/process.py:73-95`, `src/superclaude/cli/sprint/process.py:108-121`. |

Key takeaways:

- Sprint docs are useful for explaining the current subprocess orchestration pattern and the “process orchestrator, not task executor” framing.
- Treat all generated line numbers as stale unless refreshed against code. The architecture still broadly holds, but command names and registered surfaces have moved.
- For a Mastra/Backlog.md/Beads port, the crucial sprint finding is that dependency semantics in MDTM tasklists do not currently drive task scheduling in sprint execution; Mastra/Beads dependency graph adoption would be new semantics, not just a runtime swap.

### D. Contributor Knowledge Base Generated Docs

Sources: `docs/generated/contributor-knowledge-base/architecture-guide.md`, `cli-api-inventory.md`, plus sibling docs by directory inventory.

| Doc claim | Status | Code verification / notes |
|---|---|---|
| `src/superclaude/` is canonical source for distributable commands/skills/agents and `.claude/` is a repo-local mirror. | [CODE-VERIFIED] through project instructions and current source layout; not independently tested by sync command in this pass. | The architecture guide states this at `docs/generated/contributor-knowledge-base/architecture-guide.md:41-84`; current source files under `src/superclaude/commands`, `src/superclaude/skills`, and current CLI installers in `src/superclaude/cli/main.py:59-81` support the model. |
| Runtime-facing package architecture includes CLI, pytest plugin, pm_agent, execution, commands/skills/agents, core/mcp/modes. | [CODE-VERIFIED] for paths read/listed in current repo; detailed mode/mcp contents not deeply inspected here. | CLI registration and script: `pyproject.toml:65-71`; CLI root: `src/superclaude/cli/main.py:18-26`; generated doc overview at `docs/generated/contributor-knowledge-base/architecture-guide.md:124-142`. |
| CLI API inventory says current root workflow groups are `sprint`, `roadmap`, `cleanup-audit` only. | [CODE-CONTRADICTED] as stale. | Current `main.py` also registers `tasklist`, `cli-portify`, `prd`, and `eval`: `src/superclaude/cli/main.py:400-426`. |
| CLI API inventory says `pipeline/` exports a broad reusable API surface. | [CODE-VERIFIED] | `src/superclaude/cli/pipeline/__init__.py:23-157`. |
| CLI API inventory describes tasklist only as `validate`; this remains accurate for current tasklist CLI. | [CODE-VERIFIED] | `src/superclaude/cli/tasklist/commands.py:15-82`; implementation builds only `tasklist-fidelity` step in `src/superclaude/cli/tasklist/executor.py:191-218`. |
| CLI API inventory says roadmap is an “8-step” pipeline. | [CODE-CONTRADICTED] / stale simplification. | Current roadmap executor docstring says 9-step pipeline and imports additional gates/prompts for anti-instinct, spec-fidelity, wiring, deviation analysis, remediation, and certification at `src/superclaude/cli/roadmap/executor.py:1-10`, `src/superclaude/cli/roadmap/executor.py:24-69`. |

Key takeaways:

- Contributor docs are good for source-of-truth and layer diagrams, but the CLI inventory is dated 2026-03-09 and misses newer CLI surfaces.
- For the feasibility report, cite contributor docs as “report framing” rather than as current command inventory unless paired with code verification.

### E. Skill-vs-CLI Divergence Analysis

Source: `docs/analysis/skill-vs-cli-divergence-roadmap.md`.

| Doc claim | Status | Code verification / notes |
|---|---|---|
| Roadmap CLI is not a 1:1 translation of the `sc-roadmap-protocol` skill; it is an evolved Python subprocess pipeline. | [CODE-VERIFIED] at architecture level. | Roadmap command and executor are current Python CLI code in `src/superclaude/cli/roadmap/commands.py:14-196`, `src/superclaude/cli/roadmap/executor.py:1-69`; skill comparison content itself is a March/April analysis and should not be treated as exhaustive current state. |
| Multi-spec consolidation via `--specs` is not ported; CLI accepts 1-3 positional files routed to spec/TDD/PRD. | [CODE-VERIFIED] | CLI argument is `input_files` with `nargs=-1` capped at 3 in `src/superclaude/cli/roadmap/commands.py:32-35`, `src/superclaude/cli/roadmap/commands.py:207-221`; input routing is `src/superclaude/cli/roadmap/executor.py:214-240`. |
| CLI inlines adversarial generation rather than delegating to `sc:adversarial`. | [CODE-VERIFIED] by roadmap executor imports/prompts and no `Skill` invocation path in the CLI code read. | `src/superclaude/cli/roadmap/executor.py:24-69` imports diff/debate/score/merge prompts/gates; no skill invocation appears in `src/superclaude/cli/roadmap/commands.py:32-260`. |
| Some divergence findings from April may be stale because roadmap has evolved further since the analysis. | [CODE-VERIFIED] for staleness risk. | The doc itself is dated 2026-04-16 and says CLI port was 25 files/~13,166 lines; current code includes newer features like compression/cosmetic remediation flags in `src/superclaude/cli/roadmap/commands.py:142-173` and additional executor imports in `src/superclaude/cli/roadmap/executor.py:24-69`. |

Key takeaways:

- This analysis is highly useful for framing the risk of “porting” as an evolved reimplementation rather than a mechanical translation.
- For the Mastra feasibility report, reuse its pattern categories: missing features, reimagined features, CLI-only additions, scoring/formula mismatches, prompt/template drift.
- Do not assume the specific D-xxx backlog is current without re-verifying each item against current code.

### F. v3.8 RigorFlow Merger Dependency Map

Source: `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/artifacts/dependency-map.md`.

| Doc claim | Status | Code verification / notes |
|---|---|---|
| `/sc:tasklist` skill produces `tasklist-index.md` and `phase-N-tasklist.md` artifacts consumed by `superclaude sprint run`. | [CODE-VERIFIED] at downstream consumer level; tasklist skill generation internals were not re-read in this pass. | Sprint config discovers phase files from `tasklist-index.md` and canonical phase filenames in `src/superclaude/cli/sprint/config.py:52-140`; sprint command takes `index_path` at `src/superclaude/cli/sprint/commands.py:71-78`. |
| `superclaude tasklist validate` imports shared pipeline executor/process/models and roadmap gates/prompts. | [CODE-VERIFIED] with current code: imports shared pipeline executor/models/process and local tasklist gates/prompts; not roadmap gates/prompts. | Current imports are in `src/superclaude/cli/tasklist/executor.py:23-29`; this contradicts the dependency-map rows that mention `cli/roadmap/gates.py` and `cli/roadmap/prompts.py`. |
| `/sc:adversarial` is called by `/sc:roadmap` multi-spec/multi-roadmap modes. | [CODE-CONTRADICTED] for current Python roadmap CLI; [UNVERIFIED] for slash-command skill path. | Current roadmap CLI inlines adversarial prompts/gates and has no `--specs` flag: `src/superclaude/cli/roadmap/commands.py:32-196`, `src/superclaude/cli/roadmap/executor.py:24-69`. The slash-command skill path was not traced here. |
| RF pipeline/team/agent paths are under `.gfdoc`, `~/.claude/teams`, `~/.claude/tasks`, etc. | [UNVERIFIED] in this repo pass. | The dependency map appears to describe RigorFlow external/custom infrastructure; these paths are outside the current SuperClaude CLI source files investigated. Keep as historical context unless an RF-specific codebase is available. |
| SC and RF have no direct integration, with different execution runtimes/artifact schemas. | [UNVERIFIED] as a broad cross-framework claim; [CODE-VERIFIED] only that current SuperClaude sprint/tasklist code consumes MDTM-like tasklist Markdown and does not reference RF in the read paths. | Current sprint/tasklist paths read above do not mention RF; this is negative evidence, not proof across the whole repo. |

Key takeaways:

- The dependency map is useful for report section 9/10 framing around task-of-record and dependency graph semantics, but several SC integration claims are stale against current Python CLI behavior.
- Treat RigorFlow portions as external/historical unless separately verified in its actual source.

## Useful Report Framing for Mastra + Backlog.md + Beads Feasibility

| Report section mapping | Useful framing from investigated docs | Evidence / caveat |
|---|---|---|
| Section 1 — Current-state baseline | SuperClaude CLI orchestration is a Python-controlled subprocess orchestration layer over Claude Code, not a generic agent runtime. | Verified at the `ClaudeProcess` seam and sprint/roadmap/tasklist runners. This is the primary replacement seam for Mastra. |
| Section 2 — Component reuse matrix | Separate portable knowledge artifacts (skills/agents/commands/templates/gates) from runtime-coupled surfaces (Claude CLI subprocess, slash-command dispatch, stream-json monitor, tmux, permission flags, hook events). | Seed brief framing is mostly code-verified, except hook/event specifics were not verified here. |
| Section 4 — Replatform architecture | Treat Mastra as a runtime replacement for Python+ClaudeProcess orchestration only after deciding how to preserve gate semantics, resume contracts, and artifact truth. | CLI Portify evolution shows contract-first/gated approaches reduced drift compared with one-shot code generation. |
| Section 9 — Task-of-record / graph semantics | Current sprint consumes ordered Markdown tasklists; dependencies are parsed but not scheduling drivers. Backlog.md/Beads dependency graph adoption would change semantics. | `execute_phase_tasks()` iterates input order; this matters for Beads-as-dependency-graph claims. |
| Section 10 — Risk register / stale-doc discipline | Existing feasibility and generated docs contain useful architecture history but many API/line/step claims are stale. Code cross-validation must be a formal gate in any port roadmap. | Stale examples: `superclaude pipeline` command claim, CLI Portify `cli.py`/7-step claim, generated CLI inventory missing newer root subcommands, `ClaudeProcess -p` prompt delivery claim. |

## Gaps and Questions

All [UNVERIFIED] and [CODE-CONTRADICTED] claims that should not be treated as current fact:

1. **Stack D external facts are unverified in this pass.** Mastra version/licensing/RBAC, Backlog.md MCP alignment, and Beads v1.0/Dolt/SQLite/server-mode claims come only from the seed brief and require external verification before recommendation.
2. **`superclaude pipeline` as a root command is contradicted.** Current code exposes `pipeline/` as a package API, not a Click command registered in `main.py`.
3. **Hooks as portable/re-homeable runtime events were not code-verified.** Hook claims should be verified against the hook installation and settings code before being used in the port matrix.
4. **Retrospective models were not code-verified.** Roadmap has a `--retrospective` option, but no reusable retrospective “model class” was verified in this doc pass.
5. **Per-task rerun/recoverability details were not code-verified here.** Sprint has rich failure/recovery machinery, but any `rerun-tasks` claims should be separately read from current sprint commands before inclusion.
6. **CLI Portify docs conflict on deliverable type.** Current direction is spec/artifact pipeline; older skill text still describes generated CLI package files. The report should say “spec-driven planning output” unless discussing historical design.
7. **CLI Portify dry-run semantics conflict across docs/code.** Current command handler returns early on dry-run; executor has a broader dry-run phase eligibility model. This needs direct behavioral testing before documenting dry-run output guarantees.
8. **Generated sprint docs cite `/sc:task-unified`; current sprint prompt uses `/sc:task`.** If command naming matters for replatform scope, verify the current slash-command activation path.
9. **Generated contributor CLI inventory is stale.** It omits current root commands `tasklist`, `cli-portify`, `prd`, and `eval`.
10. **RigorFlow dependency-map SC integration claims are mixed.** The `tasklist validate` import chain is stale; `/sc:adversarial` call-by claims are not true for current Python roadmap CLI and were not verified for slash-command skills.
11. **RigorFlow implementation paths are unverified.** `.gfdoc`, RF teams/tasks, and automated QA workflow claims should be verified in the RF source/context before reusing.
12. **Roadmap divergence D-xxx items are historical.** Use them as investigative prompts, not current backlog facts, until each is re-grepped/read.

## Stale Documentation Found

| Document / artifact | Stale or risky claim | Current source-of-truth result |
|---|---|---|
| `.dev/releases/backlog/mastra-beads-port-feasibility/seed-brief.md` | Implies `superclaude pipeline` is a flagship CLI surface. | Current `main.py` does not register a `pipeline` root command; `pipeline/` is a shared library package. |
| `docs/guides/cli-portify-and-pipeline-runner-guide.md` | `ClaudeProcess` docs show prompt passed via `-p`. | Current process sends prompt through stdin after `Popen`, avoiding argv size limits. |
| `docs/guides/cli-portify-and-pipeline-runner-guide.md` | PipelineConfig field list omits current cosmetic remediation fields. | Current `PipelineConfig` includes `allow_cosmetic_remediation` and `cosmetic_remediator`. |
| `docs/generated/cli-portify-release-guide.md` | Documents slash-command `/sc:cli-portify` as the primary command reference, not Python `superclaude cli-portify run`; dry-run and phase claims do not match current Python handler. | Current Python CLI entry is `src/superclaude/cli/cli_portify/commands.py`; slash command remains separate. |
| `.dev/releases/complete/v2.24-cli-portify-cli-v4/release-guide-v2.24-cli-portify-cli.md` | Says module file is `cli.py`, uses 7-step old pipeline. | Current file is `commands.py`; current registry has 8 step IDs and different names. |
| `docs/generated/sprint-cli/00-overview.md` / `01-entry-points.md` | Root registration and command line references are from April and miss newer root subcommands; prompt command name uses `/sc:task-unified`. | Current `main.py` registers more commands; current sprint prompt uses `/sc:task`. |
| `docs/generated/contributor-knowledge-base/cli-api-inventory.md` | Says current root workflow groups are only `sprint`, `roadmap`, `cleanup-audit`; says roadmap is 8-step. | Current root groups include `tasklist`, `cli-portify`, `prd`, `eval`; roadmap executor docs/imports show expanded pipeline. |
| `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/artifacts/dependency-map.md` | Says `superclaude tasklist validate` imports roadmap gates/prompts; says current roadmap calls `/sc:adversarial` in multi-spec modes. | Current tasklist executor uses local tasklist gates/prompts; current roadmap CLI inlines adversarial pipeline and has no `--specs` flag. |
| `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md` | “What Gets Generated” section still describes generated CLI code package as direct output. | Current historical and Python runner direction is reviewed spec/artifact output feeding downstream planning; keep this as protocol-history drift. |

## Summary

The existing docs and release artifacts are useful but must be handled as layered history, not a single current architecture description. The strongest code-verified facts for Mastra + Backlog.md + Beads feasibility are:

1. **The core runtime seam is real and narrow enough to analyze:** `ClaudeProcess` is the subprocess boundary used by sprint/roadmap/tasklist-style orchestration. Replacing it with Mastra is the central replatforming act, but many features hang off that seam: prompt delivery, output parsing, permission flags, cancellation, timeouts, and file-based gates.
2. **Current SuperClaude orchestration is artifact/gate-centric:** Python owns sequencing, retry/halt, state emission, file outputs, and gate checks; Claude subprocesses fill structured content. A Mastra port must preserve runner-authored truth and gate semantics, not merely re-host prompts.
3. **Markdown tasklists are currently ordered execution records, not fully active dependency graphs:** sprint parses dependency annotations but executes tasks in document order. Beads/Backlog.md could add graph semantics, but that is a behavioral change and should be scoped explicitly.
4. **CLI Portify history is the best cautionary precedent:** early code-generation/spec drift caused failures; later spec-driven, contract-first planning became the safer pattern. Use that precedent to frame any Stack D roadmap as strangler/hybrid and source-verified rather than a big-bang rewrite.
5. **Several docs are stale in ways that matter for feasibility:** root CLI command inventory, roadmap step count, CLI Portify file/step names, `ClaudeProcess` prompt delivery, and SC/RF integration claims have all drifted. The final feasibility report should include a “documentation stale claims” risk and require code-verification gates for every porting phase.

Recommended framing: a Mastra + Backlog.md + Beads port is not a direct SuperClaude CLI rewrite. It is a replatforming of a Python-controlled, Claude-Code-subprocess, Markdown-artifact orchestration system into a multi-tenant workflow/task/issue runtime. The safest roadmap is hybrid/strangler: preserve current Markdown knowledge assets and Python gate logic where possible, replace the `ClaudeProcess` runtime seam first in a narrow runner, then decide whether Backlog.md or Beads owns task-of-record semantics after an explicit dependency-graph behavior test.
