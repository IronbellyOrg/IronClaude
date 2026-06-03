# Research: 04 - Adjacent Orchestration Tools
**Investigation type:** Pattern Investigator / Integration Mapper
**Scope:** `src/superclaude/cli/cli_portify/`, `src/superclaude/cli/prd/`, `src/superclaude/cli/cleanup_audit/`, `src/superclaude/cli/eval/`, `src/superclaude/cli/audit/`
**Status:** Complete
**Date:** 2026-06-02

---

## Investigation Inventory

Target directories contain a large CLI orchestration surface: `cli_portify/` (87 files), `prd/` (44 files), `cleanup_audit/` (37 files), `eval/` (65 files), and `audit/` (127 files). The source tree is the current source of truth; documentation claims are treated as stale unless cross-validated against source.

Key top-level files observed include:

- `src/superclaude/cli/cli_portify/{commands.py,executor.py,gates.py,convergence.py,resume.py,review.py,process.py,monitor.py,tui.py,prompts.py,models.py,config.py}`
- `src/superclaude/cli/prd/{commands.py,executor.py,gates.py,inventory.py,filtering.py,process.py,monitor.py,tui.py,prompts.py,models.py,config.py}`
- `src/superclaude/cli/cleanup_audit/{commands.py,executor.py,gates.py,process.py,monitor.py,tui.py,prompts.py,models.py,config.py}`
- `src/superclaude/cli/eval/{commands.py,orchestrator.py,runner.py,isolation.py,claude_process.py,pty_driver.py,retry.py,reporter.py,artifact_layout.py,models.py,config.py}`
- `src/superclaude/cli/audit/{tool_orchestrator.py,validation.py,validation_output.py,coverage.py,spot_check.py,report_depth.py,report_completeness.py,resume.py,checkpoint.py,batch_retry.py,artifact_emitter.py,...}`

Key Takeaways:

- All five target areas are CLI-adjacent orchestration systems rather than simple one-off commands.
- The research focus should prioritize pipeline entry points, gates, retry/resume, artifact layouts, prompt/process/monitor/TUI patterns, and audit/evaluation scoring surfaces over exhaustive low-level helper enumeration.

## `cli_portify/` Orchestration Pattern

### Entry point and deterministic pipeline

- `src/superclaude/cli/cli_portify/commands.py:14-27` defines the `superclaude cli-portify` Click group. The docstring describes conversion of slash commands, skills, and agents into deterministic Python-controlled pipeline runners.
- `src/superclaude/cli/cli_portify/commands.py:30-131` defines the `run` subcommand and its options: target workflow, `--cli-name/--name`, `--output`, `--commands-dir`, `--skills-dir`, `--agents-dir`, repeated `--include-agent`, `--save-manifest`, `--max-turns`, `--model`, `--dry-run`, `--resume/--start`, `--max-convergence`, `--debug`, and `--gate-mode {shadow,soft,full}`.
- `src/superclaude/cli/cli_portify/commands.py:152-183` loads config, applies path/agent/manifest/resume/gate-mode overrides, then validates config at `commands.py:184-189` before either printing dry-run metadata at `commands.py:191-197` or invoking `run_portify(config)` at `commands.py:199`.
- `src/superclaude/cli/cli_portify/executor.py:65-73` defines the dry-run phase whitelist: `PREREQUISITES`, `ANALYSIS`, `USER_REVIEW`, and `SPECIFICATION`.
- `src/superclaude/cli/cli_portify/executor.py:105-183` defines `STEP_REGISTRY` with ordered step IDs, phase types, timeouts, and retry limits: `validate-config` (30s, no retry), `discover-components` (60s, no retry), `protocol-mapping` (600s, retry 1), `analysis-synthesis` (600s, retry 1), `user-review-p1`, `step-graph-design` (600s, retry 1), `models-gates-design` (600s, retry 1), `prompts-executor-design` (600s, retry 1), `pipeline-spec-assembly` (600s, retry 1), `user-review-p2`, `release-spec-synthesis` (900s, retry 1), and `panel-review` (1200s, no outer retry).
- `src/superclaude/cli/cli_portify/executor.py:767-840` is the top-level execution builder. It creates a workdir, emits config YAML, validates resume prerequisites, creates `results/`, assigns known artifact names, constructs `PortifyStep` objects, converts gate mode to `PortifyGateMode`, and runs `PortifyExecutor`.

### Gate handling and return contracts

- `src/superclaude/cli/cli_portify/models.py:123-132` defines `PortifyPhaseType`; `models.py:139-153` defines step statuses including `PASS_NO_SIGNAL`, `PASS_NO_REPORT`, `HALT`, `TIMEOUT`, and `SKIPPED`; `models.py:160-165` defines ordered gate modes `SHADOW`, `SOFT`, and `FULL`.
- `src/superclaude/cli/cli_portify/gates.py:6-24` maps named gate IDs `G-000` through `G-011` to portify steps and required semantics. `gates.py:67-82` maps failing semantic checks to remediation hints; `gates.py:87-110` formats a gate failure diagnostic.
- Gate semantic checks are plain source-level functions returning `tuple[bool, str]`: valid YAML config (`gates.py:119-142`), component inventory (`gates.py:145-155`), required analysis sections (`gates.py:158-175`), approval status (`gates.py:178-182`), `EXIT_RECOMMENDATION` marker (`gates.py:185-189`), zero placeholders (`gates.py:192-197`), brainstorm/gaps section (`gates.py:200-209`), quality scores (`gates.py:212-227`), criticals addressed (`gates.py:230-247`), return type pattern (`gates.py:250-256`), and step-count consistency (`gates.py:259+`).
- `src/superclaude/cli/cli_portify/executor.py:380-440` implements `PortifyGatePolicy`: global mode plus per-gate promotion, `gate_passed()` from `superclaude.cli.pipeline.gates`, and blocking only when the effective mode is `FULL`.
- `src/superclaude/cli/cli_portify/executor.py:590-607` applies gate enforcement after a production step. Failed gates warn in `SOFT`; failed gates record diagnostics and return `HALT` in `FULL`; `SHADOW` only logs.
- `src/superclaude/cli/cli_portify/executor.py:283-372` emits `return-contract.yaml` on all outcome paths, using success/dry-run/partial/failed contract builders plus backward-compatible fields: `outcome`, `completed_steps`, `remaining_steps`, `suggested_resume_budget`, and optionally `resume_command`.

### Resume, retry, convergence, and failure semantics

- `src/superclaude/cli/cli_portify/executor.py:224-257` classifies process output deterministically: timeout or exit 124 becomes `TIMEOUT`; nonzero exit becomes `ERROR`; exit zero plus `EXIT_RECOMMENDATION` plus artifact becomes `PASS`; artifact without marker becomes `PASS_NO_SIGNAL`; no artifact/result becomes `PASS_NO_REPORT`.
- `src/superclaude/cli/cli_portify/executor.py:554-575` retries injected/test step runners once when status is `PASS_NO_SIGNAL` and the step has retry capacity; production retry behavior is mediated through step dispatch/result status rather than a generic loop.
- `src/superclaude/cli/cli_portify/executor.py:656-743` is a sequential execution loop with signal handling, resume skipping, dry-run skipping, turn-budget checks, outcome mapping, diagnostics emission on failure/timeout/halt, execution-log flush, TUI shutdown, and return-contract emission.
- `src/superclaude/cli/cli_portify/resume.py:45-95` contains a legacy resumability matrix for seven conceptual steps. It treats `validate-config`, `discover-components`, `analyze-workflow`, and `design-pipeline` as not resumable; `synthesize-spec`, `brainstorm-gaps`, and `panel-review` as resumable with required artifacts. This is partially out of sync with current executor step IDs such as `protocol-mapping`, `analysis-synthesis`, and the Phase 6 specification steps.
- `src/superclaude/cli/cli_portify/resume.py:168-198` validates resume by checking required artifacts in a workdir, but uses the matrix names above. `executor.py:795-802` calls this before resume. **[CODE-CONTRADICTED]** current executor supports `--resume` values from `STEP_REGISTRY`, but resume validation only recognizes legacy conceptual step names.
- `src/superclaude/cli/cli_portify/convergence.py:144-255` implements a standalone convergence state machine. `ConvergenceEngine.submit()` converges on zero unaddressed criticals (`convergence.py:215-218`), escalates on max iterations (`convergence.py:220-224`), and has explicit budget/user escalation methods (`convergence.py:229-243`).

### Prompt/process/monitor/TUI patterns

- `src/superclaude/cli/cli_portify/process.py:28-41` detects the `claude` binary via `shutil.which()` and raises installation guidance when unavailable.
- `src/superclaude/cli/cli_portify/process.py:71-113` deduplicates/resolves additional directories and caps them at `MAX_ADDITIONAL_DIRS = 10`.
- `src/superclaude/cli/cli_portify/process.py:121-215` extends shared `ClaudeProcess`: it adds `--add-dir` entries for both workdir and workflow path, inserts prior-artifact references using `@path` prompt lines, supports extra directories, and emits a structured `ProcessResult` via `run()` at `process.py:217-240`.
- `src/superclaude/cli/cli_portify/prompts.py:59-72` defines `PromptContext`; `prompts.py:79-141` defines `BasePromptBuilder` with standardized input artifact references, required frontmatter, output contract, and body composition. `prompts.py:143-163` adds retry prompt construction with failure reason and unresolved placeholder sentinels.
- `src/superclaude/cli/cli_portify/prompts.py:171-201` and `prompts.py:209-234` show concrete prompt builders that require prior artifacts, explicit frontmatter, and `EXIT_RECOMMENDATION` output contracts.
- `src/superclaude/cli/cli_portify/review.py:32-38` marks `design-pipeline` and `panel-review` as review gates; `review.py:56-86` prompts for accept/reject; `review.py:94-116` returns `(should_continue, decision)`. Like `resume.py`, this names legacy conceptual steps and does not align exactly with the current `STEP_REGISTRY`.

### Reusable migration methodology for Mastra + Backlog.md + Beads

- **Reusable as-is conceptually:** explicit step registry with phase classification, timeouts, retry limits, and named artifacts (`executor.py:105-183`, `executor.py:751-764`). Mastra workflows can map each registry entry to a workflow node; Beads can preserve these step IDs as execution graph nodes; Backlog.md can record step status/artifact fields.
- **Reusable with adaptation:** two-layer gate enforcement (`executor.py:380-440`) maps well to Mastra middleware/gates and Beads dependency blocking, but enforcement state must be persisted outside transient Python objects.
- **Reusable with adaptation:** return contracts (`executor.py:283-372`) are a strong bridge to Backlog.md records and Beads memory. The current contract is YAML in a workdir; a port should produce both a machine record and a durable markdown summary.
- **Rebuild needed:** resume validation (`resume.py:45-95`) currently contradicts the live step registry. A Mastra/Beads port should generate resume requirements from the authoritative graph, not maintain a parallel matrix.
- **Reusable with adaptation:** prompt builders (`prompts.py:79-163`) encode an artifact-first migration method: every agent prompt declares input artifacts, required frontmatter, and output contract. This can become a typed Mastra prompt/node contract and Backlog.md checklist schema.

Key Takeaways:

- `cli_portify` is the richest local pattern for deterministic migration orchestration: explicit graph, gates, contracts, TUI/logging, workdir artifacts, and convergence.
- The most important portability lesson is to avoid duplicate truth sources: the current `STEP_REGISTRY`, resume matrix, and review-gate names show drift risk.
- For Sections 2/4/6/8 mapping, `cli_portify` supports a proposed architecture of graph-first workflow definition, artifact-backed node contracts, policy-based gates, and resumable execution records.

## `prd/` Multi-Agent PRD Orchestration Pattern

### Entry point and pipeline shape

- `src/superclaude/cli/prd/commands.py:14-29` defines the `superclaude prd` group. Its docstring states a 15-step pipeline, tiered execution, and resume support.
- `src/superclaude/cli/prd/commands.py:32-89` defines `prd run` with request, product, focused source dirs, output, tier (`lightweight|standard|heavyweight`), max turns, model, dry-run, and debug options.
- `src/superclaude/cli/prd/commands.py:100-128` resolves config and either prints dry-run config (`commands.py:119-125`) or executes `PrdExecutor(config).run()`.
- `src/superclaude/cli/prd/commands.py:135-221` defines `prd resume STEP_ID`, reconstructing config with `resume_from=step_id` (`commands.py:201-211`) and running the same executor.
- `src/superclaude/cli/prd/executor.py:372-388` defines Stage A as nine ordered steps: `check-existing`, `parse-request`, `scope-discovery`, `research-notes`, `sufficiency-review`, `template-triage`, `build-task-file`, `verify-task-file`, and `preparation`.
- `src/superclaude/cli/prd/executor.py:416-506` executes the full pipeline: dry-run short-circuit, signal handler install, task directory creation, TUI registration, sequential Stage A, dynamic Stage B, final `present-complete`, and signal/TUI cleanup.

### Dynamic fan-out, QA loops, and resume behavior

- Stage B is dynamic rather than statically enumerated. `src/superclaude/cli/prd/executor.py:721-860` executes investigations, research QA/fix cycle, web research, synthesis, synthesis QA/fix cycle, assembly, structural QA, and qualitative QA.
- `src/superclaude/cli/prd/executor.py:862-887` generates investigation agents by tier: lightweight 3, standard 5, heavyweight 8.
- `src/superclaude/cli/prd/executor.py:888-905` generates web research agents by tier: lightweight 1, standard 2, heavyweight 3.
- `src/superclaude/cli/prd/executor.py:907-917` generates synthesis steps from the synthesis mapping table loaded by `load_synthesis_mapping()`.
- `src/superclaude/cli/prd/executor.py:923-958` runs parallel groups via `ThreadPoolExecutor` with `max_workers = min(len(steps), 10)`. It catches per-future exceptions and records an `ERROR` step result rather than crashing the whole thread pool.
- `src/superclaude/cli/prd/executor.py:963-1047` implements a QA -> fix -> re-QA loop. It runs initial QA plus up to `max_cycles`, halts on budget exhaustion (`executor.py:982-993`), records cycle outcomes (`executor.py:1004-1006`), exits on QA pass (`executor.py:1008-1014`), halts strict QA failures that do not trigger fixes (`executor.py:1016-1024`), and runs a gap-fill step before the next QA pass (`executor.py:1033-1046`).
- `src/superclaude/cli/prd/executor.py:443-457` implements Stage A resume by skipping prior steps when `resume_from` is a Stage A ID and skipping all Stage A when the resume target is a Stage B ID.
- `src/superclaude/cli/prd/executor.py:728-744` implements Stage B resume by comparing `resume_from` against ordered substages (`investigation`, `research-qa`, `web-research`, `synthesis`, `synthesis-qa`, `assembly`, `structural-qa`, `qualitative-qa`). It also skips already-existing investigation/web/synthesis outputs at `executor.py:746-756`.

### Artifact resolution, sentinel detection, and gate handling

- `src/superclaude/cli/prd/executor.py:72-97` detects `EXIT_RECOMMENDATION: CONTINUE|HALT` using an anchored multiline regex after stripping fenced code blocks. This avoids false positives inside code samples.
- `src/superclaude/cli/prd/executor.py:105-136` extracts assistant text from Claude stream-json/NDJSON output.
- `src/superclaude/cli/prd/executor.py:247-263` maps step IDs to canonical artifact filenames, with QA artifacts under `qa/`.
- `src/superclaude/cli/prd/executor.py:266-365` resolves the best gate content by preferring disk files written by subprocesses over NDJSON commentary. It includes special cases for dynamic `TASK-PRD-*.md` task files (`executor.py:293-303`) and dynamic final PRD assembly outputs (`executor.py:309-337`).
- `src/superclaude/cli/prd/executor.py:560-643` runs subprocess steps with a turn-budget guard, prompt construction, `PrdClaudeProcess`, stream-json extraction, disk artifact resolution, status determination, gate evaluation, artifact persistence, and result construction.
- `src/superclaude/cli/prd/executor.py:645-676` classifies timeout, crash, `HALT`, `CONTINUE`, QA verdict strings, and missing sentinel (`PASS_NO_SIGNAL`).
- `src/superclaude/cli/prd/executor.py:678-715` evaluates gates using minimum line counts plus semantic checks; failures are recorded through diagnostics and logger.
- `src/superclaude/cli/prd/gates.py:36-83` defines reusable verdict/no-placeholder checks. `gates.py:91-249` defines PRD-specific checks for parsed request fields, research note sections, suggested phase detail, task phase presence, self-contained checklist items, parallel instructions, PRD critical sections, and QA verdicts.
- `src/superclaude/cli/prd/gates.py:257-280` wraps every semantic check so exceptions become error strings. This is a useful robustness pattern for untrusted scorer functions.
- `src/superclaude/cli/prd/gates.py:303-514` defines `GATE_CRITERIA` for all 15 conceptual steps. Strict gates include parsed request, research notes, sufficiency review, build task file, verify task file, research/synthesis QA, assembly, structural QA, and qualitative QA; investigation/web/synthesis are standard; check-existing and template-triage are exempt; preparation and present-complete are light.

### Inventory, existing-work detection, and filtering

- `src/superclaude/cli/prd/inventory.py:26-67` detects existing work under `.dev/tasks/to-do/TASK-PRD-*` and returns `NO_EXISTING`, `RESUME_STAGE_A`, `RESUME_STAGE_B`, or `ALREADY_COMPLETE` based on matching task dirs, final PRD artifacts, and completed research files.
- `src/superclaude/cli/prd/inventory.py:69-130` avoids false positives for short product names by requiring `product_name` frontmatter match for names shorter than three characters; longer names use bounded content substring matching.
- `src/superclaude/cli/prd/inventory.py:138-160` discovers completed research files, excluding empty files and files containing `[INCOMPLETE]`.
- `src/superclaude/cli/prd/inventory.py:176-185` selects template variant 2 for product scope and 1 otherwise.
- `src/superclaude/cli/prd/inventory.py:193-199` creates required task subdirectories: `research/`, `synthesis/`, `qa/`, `reviews/`, and `results/`.
- `src/superclaude/cli/prd/filtering.py:20-48` partitions file lists for parallel work by threshold.
- `src/superclaude/cli/prd/filtering.py:56-87` compiles and deduplicates gaps from research files; `filtering.py:133-175` merges QA partition reports pessimistically (`FAIL` if any partition fails).

### Reusable migration methodology for Mastra + Backlog.md + Beads

- **Reusable as-is conceptually:** staged orchestration: sequential preparation, dynamic parallel fan-out, QA/fix cycles, assembly, final QA (`executor.py:416-506`, `executor.py:721-860`). This maps naturally to Mastra workflows with dynamic child nodes and Beads execution graph edges.
- **Reusable with adaptation:** task directory layout and artifact state (`inventory.py:193-199`) can become Backlog.md sections plus per-artifact paths. Existing-work detection (`inventory.py:26-67`) can seed resume state in Beads memory.
- **Reusable with adaptation:** bounded parallelism (`executor.py:923-958`) maps to Mastra concurrency controls; Beads can model each investigation/synthesis agent as a child bead with pessimistic aggregate status.
- **Reusable with adaptation:** QA/fix loop (`executor.py:963-1047`) is directly relevant to migration methodology: run independent QA, record verdict, run targeted fix/gap-fill, re-run QA until pass/cycle limit/budget exhaustion.
- **Rebuild needed:** PRD uses ad hoc artifact discovery for LLM-written files (`executor.py:266-365`). A Mastra/Backlog/Beads port should prefer explicit output declarations and tool-mediated artifact writes to avoid search heuristics.

Key Takeaways:

- `prd` contributes the strongest pattern for multi-agent dynamic fan-out and QA/fix convergence.
- Its safest reusable design is not the text of PRD prompts but the pipeline skeleton: prepare, parallel investigate, QA/fix, parallel synthesize, QA/fix, assemble, structural/qualitative QA.
- For a migration port, Backlog.md should track both conceptual stages and dynamically generated child records, while Beads should own dependency state and resumption boundaries.

## `cleanup_audit/` Read-Only Audit Orchestration Pattern

### Entry point and supervised sequential audit

- `src/superclaude/cli/cleanup_audit/commands.py:18-21` defines the `superclaude cleanup-audit` command group for read-only cleanup recommendations.
- `src/superclaude/cli/cleanup_audit/commands.py:24-71` defines `cleanup-audit run TARGET` with pass selection (`surface|structural|cross-cutting|all`), batch size, focus area, output directory, max turns, model, dry-run, and debug.
- `src/superclaude/cli/cleanup_audit/commands.py:73-90` loads config, prints a dry-run table when requested, or runs `execute_cleanup_audit(config)` and exits nonzero unless outcome is success.
- `src/superclaude/cli/cleanup_audit/commands.py:93-120` dry-run prints a Rich table with step ID, pass type, output, gate tier, timeout, and agent type using `_build_steps(config)`.
- `src/superclaude/cli/cleanup_audit/executor.py:52-184` is a sprint-style supervised execution loop: preflight `claude` binary check, signal handler install, logger/TUI/monitor setup, per-step process launch, polling supervision, stall watchdog, gate check, diagnostics on failure, summary, and cleanup.
- Although `executor.py:11-13` says `ThreadPoolExecutor` is used for parallel batch dispatch, the actual code read in `executor.py:72-159` executes `_build_steps(config)` sequentially and no `ThreadPoolExecutor` import appears in the read source. **[CODE-CONTRADICTED]** this module docstring overstates current parallel behavior.

### Step graph, gates, and status classification

- `src/superclaude/cli/cleanup_audit/executor.py:187-287` builds six audit steps: `G-001` surface scan, `G-002` structural analysis, `G-003` per-file profiles, `G-004` cross-cutting analysis, `G-005` consolidation/summary, and `G-006` validation. Each step stores a prompt, output file, gate, timeout, inputs, blocking gate mode, pass type, and agent type.
- `src/superclaude/cli/cleanup_audit/executor.py:191-203` configures surface scanning as `audit-scanner`, light gate, 600s timeout.
- `src/superclaude/cli/cleanup_audit/executor.py:205-237` configures structural analysis and per-file profiles as two separate structural steps using the surface scan output.
- `src/superclaude/cli/cleanup_audit/executor.py:239-285` configures cross-cutting analysis, consolidation, and validation as downstream steps.
- `src/superclaude/cli/cleanup_audit/executor.py:290-321` classifies outcomes: exit 124 => `TIMEOUT`; nonzero exit => `ERROR`; `G-ID-result.md` content with `EXIT_RECOMMENDATION: HALT` => `HALT`; `EXIT_RECOMMENDATION: CONTINUE` or `status: PASS` => `PASS`; `status: FAIL` => `HALT`; otherwise result file => `PASS_NO_SIGNAL`; output file plus max-turns error => `INCOMPLETE`; output file only => `PASS_NO_REPORT`; no artifacts => `ERROR`.
- `src/superclaude/cli/cleanup_audit/gates.py:20-54` defines simple regex semantic checks for classification tables, per-file profiles, cross-cutting findings, consolidation opportunities, deduplication evidence, exit recommendation, and validation verdicts.
- `src/superclaude/cli/cleanup_audit/gates.py:59-154` defines `ALL_GATES`: `G-001` light; `G-002`/`G-003` standard with frontmatter/min-line checks; `G-004` strict cross-cutting/consolidation checks; `G-005` strict deduplication and exit marker checks; `G-006` standard validation verdict checks.

### Process/monitor/TUI pattern

- `src/superclaude/cli/cleanup_audit/process.py:22-42` extends shared pipeline `ClaudeProcess`, writes stream-json output to `<step.id>-output.jsonl`, error logs to `<step.id>-error.log`, and passes max turns/model/permission flag/timeout through config and step.
- `src/superclaude/cli/cleanup_audit/process.py:49-72` implements signal handling with shutdown flag and restoration of SIGINT/SIGTERM handlers.
- `src/superclaude/cli/cleanup_audit/executor.py:88-115` polls the process at 0.5s intervals, stops on signal, hard deadline, or stall timeout when `stall_action == "kill"`, and updates the TUI with monitor state.
- `src/superclaude/cli/cleanup_audit/executor.py:133-141` only gates passing steps and converts gate failure into `HALT` plus a stored `gate_failure_reason`.
- `src/superclaude/cli/cleanup_audit/executor.py:143-159` builds diagnostics with collector/classifier/report generator and halts after any non-pass status.

### Prompt pattern

- `src/superclaude/cli/cleanup_audit/prompts.py:18-36` builds a surface scan prompt requiring classification table and grep evidence, ending with `EXIT_RECOMMENDATION`.
- `src/superclaude/cli/cleanup_audit/prompts.py:39-59` builds structural analysis prompt with YAML frontmatter and mandatory 8-field per-file profiles.
- `src/superclaude/cli/cleanup_audit/prompts.py:62-82` builds cross-cutting prompt for duplication/sprawl/consolidation/import-chain analysis.
- `src/superclaude/cli/cleanup_audit/prompts.py:85-106` builds consolidation prompt requiring executive summary, deduplicated findings, severity distribution, recommended actions, and estimated impact.
- `src/superclaude/cli/cleanup_audit/prompts.py:109-128` builds validation prompt requiring spot-checks, independent verification, verdicts, and validation rate.

### Reusable migration methodology for Mastra + Backlog.md + Beads

- **Reusable as-is conceptually:** staged audit passes with named gates (`G-001`..`G-006`) and explicit output files (`executor.py:187-287`) can map to Beads nodes and Backlog.md audit records.
- **Reusable with adaptation:** read-only prompt contracts are valuable for migration audits: classify, profile, cross-cut, consolidate, validate. Mastra can run them as deterministic workflow stages with stricter typed artifact declarations.
- **Reusable with adaptation:** process supervision loop (`executor.py:88-115`) provides a practical model for external agent execution: monitor output, deadline, stall timeout, signal handling, and TUI progress.
- **Rebuild needed:** configured pass selection and batch size are accepted by the CLI (`commands.py:24-40`) but `_build_steps(config)` does not visibly filter by pass or batch files in the code read (`executor.py:187-287`). A port should either implement these as graph filters or remove the options.
- **Rebuild needed:** docs/comments mention parallel batch dispatch, but current source executes sequentially. Do not carry this claim into Mastra/Beads architecture without implementing it.

Key Takeaways:

- `cleanup_audit` is the clearest example of read-only evidence-backed audit orchestration with validation as a first-class stage.
- Its current implementation is simpler than its comments imply: sequential six-step execution, not dynamic batch parallelism.
- For Mastra/Backlog/Beads, it supplies useful audit stage taxonomy and monitor/TUI supervision patterns, but pass filtering/batching/parallelism need rebuilding from source-verified behavior.

## `eval/` Real-Eval Harness and Isolation Pattern

### CLI entry points, capability gates, and run setup

- `src/superclaude/cli/eval/commands.py:763-821` defines the `eval` group and `doctor` command area; the command module also contains `list`, `describe`, and `run` subcommands.
- `src/superclaude/cli/eval/commands.py:119-192` implements a hard Claude-version capability check using `claude --version`, parsing a semantic version and comparing against `EvalConfig.min_claude_version`.
- `src/superclaude/cli/eval/commands.py:195-205` hard-checks that `~/.claude/` exists.
- `src/superclaude/cli/eval/commands.py:1553-1668` defines `eval run` options: required suite, parallel worker count, repeated eval filters, `--no-mcp`, `--no-pty`, output dir, keep-home, timeout multiplier, max disk MB, JSON output, verbose, and JUnit.
- `src/superclaude/cli/eval/commands.py:1689-1711` validates/clamps runtime flags: parallel below 1 clamps to 1, above 15 clamps to 15; timeout multiplier must be positive; max disk MB must be nonnegative.
- `src/superclaude/cli/eval/commands.py:1713-1780` builds the output/run directory with scratch-root allowlist validation, composes run IDs and run dirs, extends runtime `EvalConfig.allowed_scratch_roots`, and creates `home_root` only after allowlist extension.
- `src/superclaude/cli/eval/commands.py:1782-1812` resolves and loads the suite manifest, then filters post-expansion specs by requested eval IDs, failing with a harness-level exit code if requested IDs are missing.
- `src/superclaude/cli/eval/commands.py:1813-1830` runs the hook matcher coverage gate before any per-eval HOME is allocated.
- `src/superclaude/cli/eval/commands.py:1846-1853` wires `DiskBudgetPoller`; `commands.py:1853` creates the shared cancellation token.
- `src/superclaude/cli/eval/commands.py:1926-1939` instantiates `RunOrchestrator` with `run_one`, cancellation token, and disk-budget poller; it wraps the run in `SignalHandlerInstaller` when safe.
- `src/superclaude/cli/eval/commands.py:1953-1974` computes run stats, builds a `RunSummary`, and writes reports through `Reporter`. `commands.py:1989-2004` maps cancellation, disk budget breach, failures/timeouts, and clean runs to exit codes.

### Parallel scheduling and cancellation

- `src/superclaude/cli/eval/orchestrator.py:113-145` defines `RunOrchestrator` with default parallelism 8, min 1, max 15.
- `src/superclaude/cli/eval/orchestrator.py:164-299` schedules per-spec workers with `ThreadPoolExecutor` and `as_completed`, preserving original spec order by preallocating outcome slots.
- `src/superclaude/cli/eval/orchestrator.py:197-204` rejects invalid non-int/bool parallel values and parallel below 1, and clamps parallel above max.
- `src/superclaude/cli/eval/orchestrator.py:226-278` starts/stops the optional disk budget poller around the submission/drain loop.
- `src/superclaude/cli/eval/orchestrator.py:235-254` stops submitting new work when cancellation or disk-budget breach is observed. `orchestrator.py:280-291` backfills never-submitted specs as `INTERRUPTED` or disk-budget `SKIPPED` outcomes.
- `src/superclaude/cli/eval/orchestrator.py:263-275` drains futures with `as_completed`, folds worker exceptions into `ERRORED`, and never drops an eval outcome.
- `src/superclaude/cli/eval/orchestrator.py:323-344` constructs disk-budget skipped outcomes with stable skip reason and flag metadata; `orchestrator.py:347-360` constructs interrupted outcomes.

### Per-eval lifecycle, retry, and forensic logging

- `src/superclaude/cli/eval/runner.py:179-357` implements `run_eval()`, a seven-step lifecycle: setup HOME, deploy hooks, spawn, inject, observe, assert expectations, teardown.
- `src/superclaude/cli/eval/runner.py:400-423` classifies lifecycle state: any harness exception => `ERRORED` with fully-qualified exception class; all expectations pass => `PASS`; otherwise `FAIL`.
- `src/superclaude/cli/eval/runner.py:425-473` finalizes by preserving failed/errored HOME directories (`keep=True`) and removing PASS homes unless `keep_home_on_pass` is set.
- `src/superclaude/cli/eval/runner.py:537-588` implements a thread-safe JSONL event buffer/writer; `runner.py:591-673` wraps HOME and executor operations to log setup, teardown, spawn, inject, observe, and errors.
- `src/superclaude/cli/eval/runner.py:712-878` defines `EvalRunner`, adding per-eval JSONL logging, timeout enforcement, cooperative cancellation, and optional retry-once policy.
- `src/superclaude/cli/eval/runner.py:764-828` shows constructor dependencies: `HomeIsolation`, `EvalConfig`, lifecycle executor, run/artifact/stdout/stderr/transcript paths, expectation callables, hook deployer, keep-home flag, default timeout, cancellation token, retry policy, and optional HOME factory.
- `src/superclaude/cli/eval/runner.py:833-878` runs one lifecycle, then if `RetryOncePolicy` is wired and the first outcome qualifies, optionally creates a fresh HOME and retries exactly once, annotating the final outcome.
- `src/superclaude/cli/eval/runner.py:880-1005` executes exactly once in a worker thread, wraps expect callables for logging, handles pre-cancel interruption, joins by timeout, converts wired cancellation interrupts into `INTERRUPTED`, emits terminal outcome events, and flushes logs.
- `src/superclaude/cli/eval/runner.py:1026-1101` handles timeout by emitting timeout events, best-effort cancelling the executor, preserving HOME, returning `TIMEOUT`, and flushing the JSONL log.
- `src/superclaude/cli/eval/retry.py:41-57` defines retry-once constants: `MCP-flaky` tag, `mcp_server_flaky` artifact, and flaky statuses `FAIL`, `ERRORED`, `TIMEOUT`.
- `src/superclaude/cli/eval/retry.py:92-165` defines immutable `RetryOncePolicy`, allowing one retry when a spec carries `MCP-flaky` and first outcome is flaky; it annotates final outcomes idempotently.

### HOME isolation and artifact layout implications

- `src/superclaude/cli/eval/isolation.py:224-260` defines a three-check `containment_guard`: eval ID regex, scratch-root allowlist, and post-mkdtemp path containment.
- `src/superclaude/cli/eval/isolation.py:456-642` creates a per-eval HOME under `home_root` with pre-mkdir allowlist validation, `mkdtemp`, post-mkdtemp containment guard, setup-failed tagging for non-containment errors, and no writes under refused containment paths.
- `src/superclaude/cli/eval/isolation.py:644-671` returns environment variables containing `HOME`, `CLAUDE_SESSION_ID`, and optional `CLAUDE_FAKE_TIME_OFFSET`.
- `src/superclaude/cli/eval/isolation.py:673-706` tears down HOME by removing it unless `keep=True`, then clears the private home path slot.
- `src/superclaude/cli/eval/isolation.py:708-747` provides guarded `state_path()` for relative paths that must not escape HOME.

### Reusable migration methodology for Mastra + Backlog.md + Beads

- **Reusable as-is conceptually:** orchestrator separation (`RunOrchestrator` owns scheduling only; worker closure owns isolation/runner setup) is ideal for Mastra/Beads. Beads can represent one outcome per input spec and preserve original ordering; Mastra can supply the worker closure.
- **Reusable with adaptation:** capability/coverage gates before dispatch (`commands.py:1813-1830`) should become preflight nodes in a migration workflow so failures occur before side effects.
- **Reusable with adaptation:** per-execution HOME isolation and strict scratch-root allowlists (`isolation.py:456-642`) are directly relevant to evaluating migration agents safely.
- **Reusable with adaptation:** forensic JSONL logs and preserved failed HOME directories (`runner.py:537-588`, `runner.py:425-473`) can become Backlog.md links and Beads memory artifacts.
- **Reusable with adaptation:** retry-once policy should be policy-tag driven (`retry.py:92-165`) rather than blanket retries. This is a strong pattern for flaky MCP/tool-backed migration tasks.
- **Rebuild needed:** eval is optimized for test/eval manifests, not general workflow orchestration. A Mastra port should reuse its isolation, scheduling, reporting, and retry patterns, not its suite schema wholesale.

Key Takeaways:

- `eval` is the strongest local pattern for safe parallel execution isolation, deterministic outcome accounting, and forensic artifact preservation.
- It complements `prd` and `cli_portify`: those define workflow/gate structures, while `eval` defines how to execute many agent processes safely and report every result.
- For Sections 2/4/6/8, this supports a feasibility claim that Mastra can orchestrate workflow nodes while Backlog.md/Beads persist status, artifacts, retries, and forensic state.

## `audit/` Shared Audit Infrastructure and Scorers

### Static evidence, classification, and consolidation

- `src/superclaude/cli/audit/tool_orchestrator.py:15-34` defines `FileAnalysis` with file path, content hash, imports, exports, references, and metadata.
- `src/superclaude/cli/audit/tool_orchestrator.py:61-96` implements a content-hash keyed `ResultCache` with hit/miss stats; `tool_orchestrator.py:99-101` computes SHA-256 hashes.
- `src/superclaude/cli/audit/tool_orchestrator.py:108-143` provides a default line-based analyzer for import/export patterns and file metadata.
- `src/superclaude/cli/audit/tool_orchestrator.py:146-224` implements `ToolOrchestrator`: analyzer injection, plugin registration, per-file cached analysis, batch analysis, and cache stats.
- `src/superclaude/cli/audit/classification.py:19-45` defines legacy v1 categories, v2 tiers, and v2 actions.
- `src/superclaude/cli/audit/classification.py:47-57` defines deterministic `(tier, action) -> v1 category` mapping. `classification.py:96-105` raises on unmapped combinations.
- `src/superclaude/cli/audit/classification.py:108-166` classifies a finding deterministically from `has_references`, `is_test_or_config`, `is_temporal_artifact`, evidence, and qualifiers.
- `src/superclaude/cli/audit/consolidation.py:93-180` consolidates phase findings by file path, merges evidence without loss, records source phases, and resolves conflicting tier/action classifications by highest confidence.

### Coverage, validation, and calibrated QA language

- `src/superclaude/cli/audit/coverage.py:56-95` accumulates classification results with per-tier metrics, deduplicates by file path, and emits total scanned/classified plus tier percentages.
- `src/superclaude/cli/audit/validation.py:42-86` performs stratified sampling of classification results with at least one sample per populated tier and reproducible random seed.
- `src/superclaude/cli/audit/validation.py:89-151` re-classifies sampled results, compares tier/action, and reports total, sample size, consistency counts, consistency rate, tier sample counts, and inconsistencies.
- `src/superclaude/cli/audit/spot_check.py:47-76` stratifies consolidated findings by tier with a default 10% sample.
- `src/superclaude/cli/audit/spot_check.py:79-155` independently re-classifies sampled consolidated findings and reports overall/per-tier consistency rates and inconsistencies.
- `src/superclaude/cli/audit/validation_output.py:14-27` explicitly defines calibration notes and limitations stating that consistency rate is self-agreement, not ground-truth correctness.
- `src/superclaude/cli/audit/validation_output.py:30-64` formats structured validation reports with consistency-rate language; `validation_output.py:67-116` renders human-readable text and avoids the term accuracy.

### Batching, checkpoints, retry, and budget degradation

- `src/superclaude/cli/audit/batch_decomposer.py:91-135` detects monorepo segments from workspace marker files and common root directories, assigning unsegmented files to `__root__`.
- `src/superclaude/cli/audit/batch_decomposer.py:145-187` decomposes files into segment-isolated batches that never mix monorepo segments and respect `max_batch_size`, producing batch IDs and token estimates.
- `src/superclaude/cli/audit/checkpoint.py:19-55` models batch status and checkpoint state for `progress.json`.
- `src/superclaude/cli/audit/checkpoint.py:58-88` atomically writes checkpoint state via temp file plus rename; `checkpoint.py:91-110` reads checkpoint state and derives completed batch IDs.
- `src/superclaude/cli/audit/batch_retry.py:60-135` retries each batch up to `DEFAULT_MAX_RETRIES = 2`, updates checkpoint state after success/final failure, and records retry history.
- `src/superclaude/cli/audit/batch_retry.py:137-187` executes all batches sequentially, detects cascading failure when all executed batches fail, and emits a minimum viable report with failed batch summaries.
- `src/superclaude/cli/audit/budget.py:26-43` defines enforcement actions and degradation levels: warn, degrade, halt; skip duplication matrix, reduce validation sample, skip Tier-C graph edges, reduce profile fields, minimum viable report.
- `src/superclaude/cli/audit/budget.py:69-92` validates budget config and threshold order. `budget.py:159-234` tracks per-phase consumption and triggers warn/degrade/halt. `budget.py:236-320` manages ordered degradation with protected-capability overrides.

### Report rendering, completeness, and docs-audit support

- `src/superclaude/cli/audit/report_depth.py:22-39` defines `summary`, `standard`, and `detailed` report depths.
- `src/superclaude/cli/audit/report_depth.py:42-88` summary output includes tier/action counts and top 10 findings. `report_depth.py:91-134` standard output groups findings by action with evidence and conflicts. `report_depth.py:137-170` detailed output includes per-file profiles and all conflicts. `report_depth.py:173-193` dispatches by selected depth.
- `src/superclaude/cli/audit/report_completeness.py:12-20` mandates final report sections: `executive_summary`, `findings_by_tier`, `action_items`, `coverage_metrics`, `validation_results`, and `dependency_graph_summary`.
- `src/superclaude/cli/audit/report_completeness.py:43-59` checks present/missing sections; `report_completeness.py:62-82` checks large-directory assessment coverage; `report_completeness.py:85-115` returns a structured completeness result.
- `src/superclaude/cli/audit/docs_audit.py:80-98` extracts relative markdown links. `docs_audit.py:101-132` checks broken internal links against known files. `docs_audit.py:135-171` flags docs stale after a default 365-day threshold. `docs_audit.py:174-211` runs the minimal docs audit.

### Reusable migration methodology for Mastra + Backlog.md + Beads

- **Reusable as-is conceptually:** static evidence cache (`tool_orchestrator.py:61-96`) and deterministic classification (`classification.py:108-166`) are strong candidates for Beads memory enrichment and Backlog.md evidence fields.
- **Reusable with adaptation:** consolidation by file path plus highest-confidence conflict resolution (`consolidation.py:93-180`) maps to migration issue deduplication across multiple agents.
- **Reusable with adaptation:** consistency validation must preserve calibration language (`validation_output.py:14-27`): report self-consistency, not truth. This matters for QA claims in feasibility reports.
- **Reusable with adaptation:** checkpoint and retry primitives (`checkpoint.py:58-110`, `batch_retry.py:60-187`) should be lifted into a shared orchestration library rather than reimplemented per workflow.
- **Reusable with adaptation:** budget degradation (`budget.py:26-43`, `budget.py:159-320`) offers a method to keep long Mastra workflows from failing late: degrade non-critical outputs before halting.
- **Rebuild needed:** these audit modules are mostly pure primitives, not one coherent CLI runner in the files read. A port needs an explicit integration layer that wires these primitives into Mastra nodes and Beads records.

Key Takeaways:

- `audit/` contains reusable primitives for evidence, deterministic classification, deduplication, validation, checkpointing, retry, degradation, and report scoring.
- The most portable asset is the audit vocabulary and scoring discipline, not a single end-to-end command.
- For a Mastra + Backlog.md + Beads port, these modules should become shared utility nodes/policies used by workflows such as PRD generation, cleanup audit, and migration execution.

## Mapping to Requested Report Sections

### Section 2 Mapping: Current orchestration assets

- `cli_portify` provides the graph-first migration pipeline: static `STEP_REGISTRY`, phase types, timeouts, retry limits, artifact names, gate policy, return contracts, and convergence (`src/superclaude/cli/cli_portify/executor.py:105-183`, `executor.py:380-440`, `executor.py:767-840`).
- `prd` provides dynamic multi-agent orchestration: sequential Stage A, tier-sized investigation/web fan-outs, synthesis mapping fan-out, and QA/fix loops (`src/superclaude/cli/prd/executor.py:372-388`, `executor.py:721-860`, `executor.py:963-1047`).
- `cleanup_audit` provides read-only audit passes with monitor/TUI supervision and blocking gates (`src/superclaude/cli/cleanup_audit/executor.py:52-184`, `executor.py:187-287`).
- `eval` provides safe parallel execution infrastructure: capability preflight, scratch-root allowlist, per-eval HOME isolation, ordered outcome accounting, JSONL forensic logs, cancellation, disk-budget skips, and retry-once policy (`src/superclaude/cli/eval/commands.py:1713-1780`, `orchestrator.py:164-299`, `runner.py:833-878`, `isolation.py:456-642`).
- `audit` provides shared utility primitives: static evidence cache, deterministic classification, consolidation, coverage, consistency validation, checkpointing, retry, report depth, and completeness scoring (`src/superclaude/cli/audit/tool_orchestrator.py:146-224`, `classification.py:108-166`, `consolidation.py:93-180`, `validation.py:89-151`).

### Section 4 Mapping: Reusable orchestration methodology

- Define workflow nodes in one authoritative registry/graph. Avoid parallel truth sources; current `cli_portify` shows drift between `STEP_REGISTRY` and legacy resume/review step names.
- Attach explicit node contracts: input artifacts, output artifacts, required frontmatter, semantic gates, timeout, retry policy, and phase type. `cli_portify.prompts.BasePromptBuilder` is the clearest source pattern (`src/superclaude/cli/cli_portify/prompts.py:79-163`).
- Preflight before side effects. `eval run` validates output roots, suite manifests, hook coverage, and capability flags before per-eval HOME allocation (`src/superclaude/cli/eval/commands.py:1713-1830`).
- Execute with observable supervision: monitor output, deadlines, stall timeouts, TUI/logging, and signal-aware graceful shutdown (`src/superclaude/cli/cleanup_audit/executor.py:88-115`, `src/superclaude/cli/prd/executor.py:430-440`, `src/superclaude/cli/eval/runner.py:880-1005`).
- Gate after every artifact-producing step and persist diagnostics. Strict gates halt; standard/soft gates can allow downstream progress depending on workflow policy (`src/superclaude/cli/prd/executor.py:620-638`, `src/superclaude/cli/cli_portify/executor.py:590-607`).
- Use QA/fix convergence loops for artifact quality rather than assuming first-pass LLM success (`src/superclaude/cli/prd/executor.py:963-1047`, `src/superclaude/cli/cli_portify/convergence.py:144-255`).

### Section 6 Mapping: Mastra + Backlog.md + Beads integration implications

- **Mastra workflows:** best fit for graph execution, dynamic fan-out, per-node middleware/gates, retries, and preflight/finalization nodes. Use `cli_portify`/`prd` as the workflow-shape sources and `eval` as the execution safety source.
- **Backlog.md records:** best fit for human-readable durable work records: node status, gate verdicts, artifact links, QA/fix cycle summaries, retry attempts, and final return contracts. Existing `return-contract.yaml` and PRD task directories show what should be preserved in markdown form (`src/superclaude/cli/cli_portify/executor.py:283-372`, `src/superclaude/cli/prd/inventory.py:193-199`).
- **Beads execution graph/memory:** best fit for dependency state, node IDs, resumption, deduped evidence, checkpoint state, and persistent per-node memory. Audit checkpoint and consolidation modules are directly applicable (`src/superclaude/cli/audit/checkpoint.py:58-110`, `src/superclaude/cli/audit/consolidation.py:93-180`).
- **Migration methodology:** use a typed graph as source of truth; generate Backlog.md from graph state; let Beads own dependency/resume memory; run Mastra nodes with SuperClaude-style gates and eval-style isolation.

### Section 8 Mapping: Rebuild/adaptation priorities

1. **Graph source of truth:** rebuild first. Generate resume requirements, Backlog.md records, and Beads dependencies from the same graph definition.
2. **Artifact contract layer:** adapt `BasePromptBuilder` and PRD artifact persistence into typed node input/output declarations.
3. **Gate policy layer:** adapt `cli_portify` two-layer gate policy and PRD safe semantic checks. Preserve strict vs standard/light/exempt semantics.
4. **Execution safety layer:** adapt `eval` HOME isolation, ordered outcomes, cancellation token, disk-budget skips, and JSONL logs for Mastra workers.
5. **QA/convergence layer:** adapt PRD QA/fix loops and portify convergence state into reusable node-loop policies.
6. **Audit scoring layer:** adapt audit classification, consolidation, coverage, validation, and completeness scorers as reusable quality nodes.
7. **Retire duplicated matrices:** do not port `cli_portify.resume.RESUMABILITY_MATRIX` or review-gate names as-is because source verification found drift.

## Gaps and Questions

- `src/superclaude/cli/cli_portify/resume.py:45-95` uses legacy conceptual step names (`analyze-workflow`, `design-pipeline`, `synthesize-spec`) while `src/superclaude/cli/cli_portify/executor.py:105-183` uses current registry step names (`protocol-mapping`, `analysis-synthesis`, `step-graph-design`, etc.). **[CODE-CONTRADICTED]** Question: should resume be generated from `STEP_REGISTRY` before any port, or is the legacy resume surface intentionally retained for older workdirs?
- `src/superclaude/cli/cli_portify/review.py:32-38` marks `design-pipeline` and `panel-review` as review gates, but the current registry does not include `design-pipeline`. **[CODE-CONTRADICTED]** Question: should review gates be attached to `user-review-p1`, `user-review-p2`, and/or specific specification steps instead?
- `src/superclaude/cli/cleanup_audit/commands.py:24-40` accepts `--pass` and `--batch-size`, but `src/superclaude/cli/cleanup_audit/executor.py:187-287` builds the same six steps without visible pass filtering or batch decomposition. **[CODE-CONTRADICTED]** Question: are these flags planned, implemented elsewhere, or currently non-functional?
- `src/superclaude/cli/cleanup_audit/executor.py:11-13` states `ThreadPoolExecutor` is used for parallel batch dispatch, but the source read executes steps sequentially and does not import `ThreadPoolExecutor`. **[CODE-CONTRADICTED]** Question: should cleanup-audit be treated as sequential in the feasibility report unless parallelism is rebuilt?
- `src/superclaude/cli/eval/runner.py:731-740` comments say retry is default zero and future R3-mit will extend MCP-flaky retry, while `src/superclaude/cli/eval/retry.py:1-23` and `runner.py:851-876` show retry-once policy is now implemented when wired. **[CODE-CONTRADICTED]** Question: update comments/docs before using retry behavior as a cited current capability.
- No source file in this investigation directly implements Mastra, Backlog.md, or Beads integration. All integration mapping above is feasibility inference from verified SuperClaude behavior, not current implementation. **[UNVERIFIED]**

## Stale Documentation Found

- **[STALE DOC]** `src/superclaude/cli/cleanup_audit/executor.py:11-13` says the executor uses `ThreadPoolExecutor` for parallel batch dispatch; source in the same file shows sequential execution of `_build_steps(config)` at `executor.py:72-159`.
- **[STALE DOC]** `src/superclaude/cli/cli_portify/resume.py:5-13` says there are all 7 steps and steps 5-7 are resumable; current `STEP_REGISTRY` has 12 registered steps in `src/superclaude/cli/cli_portify/executor.py:105-183`.
- **[STALE DOC]** `src/superclaude/cli/cli_portify/prompts.py:7-11` lists legacy prompt builders `AnalyzeWorkflowPrompt`, `DesignPipelinePrompt`, `SynthesizeSpecPrompt`, `BrainstormGapsPrompt`, and `PanelReviewPrompt`; current executor registry and artifact map include newer steps such as `protocol-mapping`, `analysis-synthesis`, `step-graph-design`, `models-gates-design`, `prompts-executor-design`, and `pipeline-spec-assembly` (`src/superclaude/cli/cli_portify/executor.py:105-183`, `executor.py:751-764`).
- **[STALE DOC]** `src/superclaude/cli/eval/runner.py:731-740` says MCP-flaky retry-once is future work; `src/superclaude/cli/eval/retry.py:92-165` and `src/superclaude/cli/eval/runner.py:851-876` show a wired retry-once policy now exists.

## Summary

This investigation found five reusable orchestration surfaces:

1. `cli_portify/` is the primary deterministic migration pipeline pattern: explicit step registry, phase filtering, gates, return contracts, artifact names, and convergence.
2. `prd/` is the primary dynamic multi-agent workflow pattern: sequential setup, tier-based fan-out, parallel execution, QA/fix loops, artifact discovery, and final QA.
3. `cleanup_audit/` is the primary read-only audit-pipeline pattern: monitored subprocesses, blocking gates, audit pass taxonomy, validation, and diagnostics; however, batching/parallel claims are stale in the code read.
4. `eval/` is the primary execution-safety pattern: capability gates, scratch-root allowlists, per-eval HOME isolation, ordered parallel outcomes, JSONL forensic logs, cancellation, disk budget handling, and policy-tag retry.
5. `audit/` is the primary reusable scoring primitive library: evidence cache, deterministic classification, consolidation, checkpoint/retry, coverage, consistency validation, report depth, and completeness checks.

For Mastra + Backlog.md + Beads feasibility, the verified migration method is: define a single typed graph, attach explicit artifact/gate contracts to nodes, preflight before side effects, run nodes with isolation and supervision, persist graph/checkpoint/artifact state durably, apply QA/fix or convergence loops, and report calibrated validation results without overstating correctness.
