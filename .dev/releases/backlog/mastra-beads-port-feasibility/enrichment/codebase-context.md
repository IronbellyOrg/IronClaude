# Codebase Port-Surface Map

## Subsystem inventory

| Subsystem | Role | LOC band | Port difficulty |
|---|---|---|---|
| pipeline/executor.py | Generic step sequencer with retry, parallel dispatch, trailing-gate sync, cosmetic-remediation injection. Composition-via-callable design: consumers inject their own StepRunner. | ~470 LOC | `medium` |
| pipeline/process.py (ClaudeProcess) | THE SINGLE RUNTIME SEAM. Spawns ['claude','--print','--verbose',permission_flag,'--no-session-persistence','--tools','default','--max-turns',N,'--output-format','stream-json'\|'text','--model',M] via subprocess.Popen, pipes prompt via stdin (avoids MAX_ARG_STRLEN), sets os.setpgrp for kill-tree. Accepts lifecycle hooks (on_spawn/on_signal/on_exit). | ~245 LOC | `very-high` |
| pipeline/gates.py (gate_passed) | Pure Python gate validator. EXEMPT/LIGHT/STANDARD/STRICT tier enforcement: file-exists, non-empty, min-lines, YAML frontmatter keys, semantic check functions. No subprocess, no LLM. | ~145 LOC | `low` |
| pipeline/models.py | Shared data types: StepStatus, GateMode, SemanticCheck, GateCriteria, Step, StepResult, Deliverable, PipelineConfig, CosmeticRemediator Protocol. Zero sprint/roadmap imports. | ~235 LOC | `low` |
| pipeline/trailing_gate.py | TrailingGateRunner: async gate submission/thread pool for TRAILING-mode steps with grace-period enforcement, DeferredRemediationLog, TrailingGateResult. Protocol+callback-based. | ~650 LOC | `low` |
| pipeline/fmea_classifier.py | Dual-signal FMEA failure mode classifier: invariant cross-reference (Signal 1) + no-error-path detection (Signal 2). Pure Python regex heuristics on deliverable descriptions. | ~370 LOC | `low` |
| pipeline/fmea_domains.py | Input domain taxonomy (DomainCategory enum, InputDomain dataclass) for FMEA degenerate-input testing. | ~170 LOC | `low` |
| pipeline/fmea_promotion.py | Promotes failure modes through detection/severity matrices into risk register entries. | ~235 LOC | `low` |
| pipeline/invariants.py | Invariant predicate registry (InvariantEntry dataclass) for FMEA Signal 1 cross-references. | ~205 LOC | `low` |
| pipeline/invariant_pass.py | Applies invariant predicates to deliverable descriptions. | ~175 LOC | `low` |
| pipeline/dataflow_graph.py | Builds directed dataflow dependency graphs from deliverable metadata. | ~380 LOC | `low` |
| pipeline/dataflow_pass.py | Dataflow analysis pass: identifies upstream/downstream dependencies, cycle detection. | ~315 LOC | `low` |
| pipeline/guard_analyzer.py | Guard clause analysis: identifies missing/weak guards in deliverable descriptions. | ~495 LOC | `low` |
| pipeline/guard_pass.py | Applies guard analysis to deliverable inventory. | ~210 LOC | `low` |
| pipeline/guard_resolution.py | Resolves guard conflicts across deliverables. | ~250 LOC | `low` |
| pipeline/conflict_detector.py | Cross-deliverable conflict detection: identifies contradictory requirements, overlapping responsibilities. | ~350 LOC | `low` |
| pipeline/conflict_review.py | Conflict review reporting and summarization. | ~110 LOC | `low` |
| pipeline/contract_extractor.py | Extracts interface contracts from deliverable descriptions. | ~340 LOC | `low` |
| pipeline/deliverables.py | Deliverable decomposition and kind classification. | ~195 LOC | `low` |
| pipeline/diagnostic_chain.py | Chains diagnostic passes (FMEA + invariant + guard + conflict) into unified analysis. | ~250 LOC | `low` |
| pipeline/state_detector.py | Detects state mutation patterns in deliverable descriptions. | ~280 LOC | `low` |
| pipeline/mutation_inventory.py | Inventory of state mutations across deliverables. | ~150 LOC | `low` |
| pipeline/verification_emitter.py | Emits verification artifacts from analysis results. | ~125 LOC | `low` |
| pipeline/combined_m2_pass.py | Combined M2 (metadata) analytical pass over deliverables. | ~205 LOC | `low` |
| sprint/executor.py | THE FLAGSHIP. ~2150 LOC main orchestration loop: per-phase Claude subprocess spawning, TUI dashboard, output monitor thread, stall watchdog (startup-stall + mid-stall), TurnLedger budget accounting, wiring-gate hooks, anti-instinct hooks, checkpoint enforcement, crash recovery, KPI report, retrospective generation, summary worker fanout, tmux IPC via .sprint-exitcode sentinel. | ~2150 LOC | `very-high` |
| sprint/process.py (Sprint ClaudeProcess) | Extends pipeline.process.ClaudeProcess with sprint-specific build_prompt() (/sc:task injection, sprint context header, execution rules, checkpoint instructions, EXIT_RECOMMENDATION sentinel). Hook factories for debug logging. | ~385 LOC | `very-high` |
| sprint/models.py | Rich domain types: TaskEntry, TaskStatus, GateOutcome, GateDisplayState (with transition FSM), TaskResult, PhaseStatus (13 states), SprintOutcome, Phase, CheckpointEntry, SprintConfig (extends PipelineConfig with 20+ fields + migration shims), SprintStep, PhaseResult, SprintResult, MonitorState (stream-json telemetry), TurnLedger (economic budget model), ShadowGateMetrics. Pure data. | ~885 LOC | `low` |
| sprint/checkpoints.py | Checkpoint path extraction from markdown tasklists (regex-based), manifest build/write/recovery, evidence artifact discovery, auto-recovered checkpoint report rendering. Pure Python + file I/O. | ~410 LOC | `low` |
| sprint/commands.py | Click CLI group: sprint run/attach/status/logs/kill/verify-checkpoints. Fidelity block preflight, tmux decision logic, config loading delegation. | ~465 LOC | `medium` |
| sprint/config.py | SprintConfig loader: discovers phases from tasklist index, parses markdown phase files, resolves release directories. | ~510 LOC | `low` |
| sprint/monitor.py | OutputMonitor: background thread parsing stream-json (NDJSON) output from claude subprocess. Extracts turns, tokens, tool calls, errors, activity log, stall detection. Core stream-json parser. | ~570 LOC | `high` |
| sprint/tmux.py | Tmux session management: create/attach/kill sprint sessions, split-pane TUI dashboard, tail-pane live updates, summary-pane notifications, .sprint-exitcode IPC, self-relaunch with --no-tmux. | ~325 LOC | `high` |
| sprint/tui.py | SprintTUI: Rich-based terminal dashboard with phase table, activity stream, error panel, agent context line, dual progress bar. Poll-based updates. | ~630 LOC | `medium` |
| sprint/summarizer.py | PhaseSummarizer + SummaryWorker: daemon thread pool that re-parses stream-json output, asks Haiku for narrative summaries, writes phase-N-summary.md. Exception-isolated fanout to tmux/TUI. | ~645 LOC | `medium` |
| sprint/retrospective.py | RetrospectiveGenerator: generates release retrospective from sprint results + phase summaries. | ~365 LOC | `low` |
| sprint/kpi.py | Builds KPI report from accumulated gate results, remediation log, and TurnLedger. | ~220 LOC | `low` |
| sprint/logging_.py | SprintLogger: writes execution-log.jsonl and execution-log.md with phase results, checkpoint verification events. | ~235 LOC | `low` |
| sprint/diagnostics.py | DiagnosticCollector, FailureClassifier, ReportGenerator: collects phase failure diagnostics, classifies category, writes report. | ~290 LOC | `low` |
| sprint/preflight.py | Executes python-mode and skip-mode phases before the main Claude loop. Pure Python steps (no subprocess). | ~245 LOC | `low` |
| sprint/notify.py | Desktop/system notifications for phase/sprint completion. | ~60 LOC | `low` |
| sprint/debug_logger.py | Debug logging setup for sprint execution. | ~140 LOC | `low` |
| roadmap/executor.py | THE LARGEST. ~3700 LOC 8-step pipeline: extract, generate-A, generate-B, diff, debate (multi-agent), score, merge, anti-instinct audit, test-strategy, spec-fidelity (convergence loop), deviation-analysis, remediate, certify. Reuses execute_pipeline + ClaudeProcess with StepRunner adapter. Has its own _ClaudeRunner inner class for prompt->string interface. Direct (non-subprocess) execution for anti-instinct, deviation-analysis, remediate, wiring-verification steps. | ~3700 LOC | `very-high` |
| roadmap/convergence.py | Convergence engine: DeviationRegistry (file-backed JSON, spec-hash reset, stable finding IDs), execute_fidelity_with_convergence (up to 3 checker/remediation cycles with TurnLedger budget accounting, regression detection, progress credit), handle_regression (3-agent parallel validation with temp dir isolation, adversarial merge). | ~780 LOC | `medium` |
| roadmap/gates.py | 14 GateCriteria constants (EXTRACT through CERTIFY) with 30+ semantic check functions (pure Python: frontmatter validation, heading structure, cross-ref resolution, table schema checks, template sentinel detection, deviation routing consistency). ALL_GATES list in pipeline order. | ~1440 LOC | `low` |
| roadmap/fidelity_checker.py | FidelityChecker: exact name matching of spec FR function/class names against codebase AST scan. Fail-open on ambiguity (R-3). Produces Finding objects compatible with convergence registry. | ~420 LOC | `low` |
| roadmap/commands.py | Click CLI: roadmap run/validate/accept-spec-change. Routes input files (spec/TDD/PRD), builds RoadmapConfig, delegates to execute_roadmap. | ~400 LOC | `low` |
| roadmap/models.py | RoadmapConfig, AgentSpec, Finding, ValidateConfig dataclasses. Pure data. | ~145 LOC | `low` |
| roadmap/cosmetic_remediator.py | Deterministic auto-fix of pure-cosmetic gate failures (heading shape, dash variants, whitespace, smart-quotes, table padding). Classifies failures, applies regex transforms, re-checks. No LLM. | ~1100 LOC | `low` |
| roadmap/obligation_scanner.py | Scans roadmap for undischarged obligations (scaffolding without discharge in later milestones), integration contract gaps. | ~825 LOC | `low` |
| roadmap/integration_contracts.py | Integration contract analysis: identifies wiring tasks required for roadmap contracts. | ~475 LOC | `low` |
| roadmap/structural_checkers.py | Structural deviation checkers: heading hierarchy, cross-references, duplicate detection, table schema validation. | ~1070 LOC | `low` |
| roadmap/semantic_layer.py | Semantic deviation checker: LLM-based semantic gap detection between spec and roadmap. | ~690 LOC | `medium` |
| roadmap/spec_parser.py | Parses spec markdown into structured FR/NFR model with requirement IDs. | ~640 LOC | `low` |
| roadmap/fingerprint.py | Code fingerprint generation: extracts code-level identifiers from spec for coverage checking. | ~225 LOC | `low` |
| roadmap/prompts.py | All LLM prompts for the 8-step roadmap pipeline (extract, generate, diff, debate, score, merge, test-strategy, certify). | ~1370 LOC | `low` |
| roadmap/remediate.py | Remediation orchestration: patches roadmap to fix deviation findings. | ~435 LOC | `low` |
| roadmap/remediate_executor.py | Remediation step executor: runs patch generation via Claude subprocess, applies fixes. | ~860 LOC | `medium` |
| roadmap/spec_patch.py | Spec hash update after accepted deviations. | ~305 LOC | `low` |
| roadmap/validate_executor.py | Validation pipeline executor for roadmap outputs. | ~520 LOC | `low` |
| roadmap/certify_prompts.py | Certification step prompts. | ~340 LOC | `low` |
| roadmap/templates.py | Roadmap template constants. | ~70 LOC | `low` |
| roadmap/validate_prompts.py | Validation prompts. | ~200 LOC | `low` |
| roadmap/validate_gates.py | Validation gate criteria. | ~70 LOC | `low` |
| roadmap/remediate_parser.py | Parses remediation output. | ~390 LOC | `low` |
| roadmap/remediate_prompts.py | Remediation prompts. | ~135 LOC | `low` |
| roadmap/spec_structural_audit.py | Structural audit of spec files. | ~110 LOC | `low` |
| tasklist/executor.py | Tasklist validation: reuses execute_pipeline + ClaudeProcess for fidelity checking. | ~275 LOC | `low` |
| tasklist/models.py | TasklistValidateConfig dataclass. | ~30 LOC | `low` |
| tasklist/gates.py | TASKLIST_FIDELITY_GATE criteria. | ~45 LOC | `low` |
| tasklist/prompts.py | Tasklist fidelity prompt templates. | ~235 LOC | `low` |
| tasklist/commands.py | Click CLI for tasklist validation. | ~185 LOC | `low` |
| prd/executor.py | PRD pipeline executor. | ~1200 LOC | `medium` |
| prd/prompts.py | PRD-specific LLM prompts. | ~1455 LOC | `low` |
| audit/* (entire module) | Static analysis suite: wiring_gate (~1120 LOC), wiring_analyzer, wiring_config, dependency_graph, reachability, dead_code, credential_scanner, duplication, dynamic_imports, profiling, and more. Pure Python, no subprocess. | ~6700 LOC total | `low` |
| skills/* (24 SKILL.md files) | Portable markdown skill definitions installed to ~/.claude/commands/sc/. Define /sc:* command behavior. Runtime-agnostic. | ~varies, 24 files | `low` |
| agents/* (39 .md files) | Agent persona definitions in markdown (pm-agent, system-architect, rf-team, etc.). Installed as Claude Code agent prompts. Runtime-agnostic. | ~8000 LOC total | `low` |
| cli_portify/* | Self-referential porting tool: discovers components, synthesizes spec, designs pipeline, validates config. ~6000 LOC across 30+ files. | ~6000 LOC | `medium` |
| eval/* | Evaluation/test harness: ~8500 LOC across 30+ files. PTY driver, isolation, capabilities testing, runner orchestration. | ~8500 LOC | `high` |

## Runtime coupling points (Claude Code CLI seam)

- pipeline/process.py:79-95 — build_command() constructs ['claude','--print','--verbose',permission_flag,'--no-session-persistence','--tools','default','--max-turns',N,'--output-format','stream-json'|'text'] + optional ['--model',M]. This is THE single runtime seam.
- pipeline/process.py:114-146 — start(): subprocess.Popen with stdin=PIPE for prompt delivery (bypasses Linux MAX_ARG_STRLEN=128KB), preexec_fn=os.setpgrp for kill-tree, CLAUDECODE/CLAUDE_CODE_ENTRYPOINT env var removal to prevent nested-session detection.
- pipeline/process.py:159-171 — wait(): subprocess.wait(timeout=timeout_seconds) with TimeoutExpired -> terminate() -> exit code 124.
- pipeline/process.py:173-214 — terminate(): SIGTERM then SIGKILL after 10s via os.killpg(pgid, ...) or process.kill().
- sprint/process.py:108-121 — Sprint ClaudeProcess.__init__: wires hooks, sets output_format='stream-json', timeout_seconds=max_turns*120+300.
- sprint/process.py:123-216 — build_prompt(): constructs /sc:task prompt with sprint context header, execution rules, checkpoint instructions, EXIT_RECOMMENDATION sentinel.
- sprint/executor.py:1147-1151 — Pre-flight check: shutil.which('claude') raises SystemExit if binary not found.
- sprint/executor.py:1324 — ClaudeProcess(config, phase, env_vars=_phase_env_vars): launches per-phase subprocess.
- sprint/executor.py:1340-1457 — Poll loop: proc_manager._process.poll() with TUI updates, stall watchdog (config.startup_stall_timeout, config.stall_timeout), monotonic deadline enforcement.
- sprint/monitor.py:254-423 — OutputMonitor thread: tail-f on stream-json output file, parses NDJSON lines for turn counting, token accumulation, tool-call extraction, error detection, stall timing.
- sprint/tmux.py:68-323 — subprocess.run(['tmux',...]) for session management: new-session, split-window, send-keys, select-pane, kill-session, attach-session. Self-relaunch via ['superclaude','sprint','run',..., '--no-tmux','--tmux-session-name',name].
- sprint/commands.py:110-114 — Click choices for --permission-flag: '--dangerously-skip-permissions' or '--allow-hierarchical-permissions'.
- sprint/commands.py:287-290 — tmux decision: is_tmux_available() + not no_tmux -> launch_in_tmux(config) else execute_sprint(config).
- roadmap/executor.py:1107-1115 — ClaudeProcess instantiation for roadmap steps with output_format='text'.
- roadmap/executor.py:1271-1279 — _ClaudeRunner inner class: ClaudeProcess wrapper with run(prompt)->str interface for convergence remediation steps.
- install_hooks.py:43-76 — _FRESHNESS_SCRIPTS: installs shell scripts to ~/.claude/hooks/ (freshness-session-start.sh, freshness-user-prompt.sh, freshness-pre-edit.sh, etc.).
- install_hooks.py:88-100 — install_hooks(): merges hook registrations into ~/.claude/settings.json via atomic write + additive merge.
- install_commands.py:12-90 — install_commands(): copies .md command files to ~/.claude/commands/sc/ for /sc:* namespace.
- install_mcp.py:17-100 — MCP server installation: registers MCP servers (sequential-thinking, context7, magic, playwright, serena, tavily, auggie) into Claude Code config.
- install_agents.py — Installs agent persona .md files into Claude Code agent configuration.

## Portable IP (runtime-agnostic)

- pipeline/models.py — Step, StepResult, StepStatus, GateCriteria, SemanticCheck, GateMode, PipelineConfig, Deliverable, DeliverableKind. Pure dataclasses, zero runtime coupling.
- pipeline/gates.py — gate_passed(): pure Python validation logic (file-exists, frontmatter, semantic checks). No subprocess, no LLM. Directly portable.
- pipeline/trailing_gate.py — TrailingGateRunner, DeferredRemediationLog, TrailingGateResult. Thread-based async gate evaluation with Protocol-based interface.
- pipeline/fmea_classifier.py + fmea_domains.py + invariants.py + invariant_pass.py + fmea_promotion.py — FMEA failure mode classification suite. Pure regex/text analysis.
- pipeline/dataflow_graph.py + dataflow_pass.py — Dependency graph construction and analysis. Pure Python.
- pipeline/guard_analyzer.py + guard_pass.py + guard_resolution.py — Guard clause analysis. Pure Python.
- pipeline/conflict_detector.py + conflict_review.py — Conflict detection and review. Pure Python.
- pipeline/state_detector.py + mutation_inventory.py — State mutation pattern detection. Pure Python.
- pipeline/diagnostic_chain.py — Diagnostic chaining. Pure Python.
- pipeline/contract_extractor.py — Contract extraction. Pure Python.
- pipeline/deliverables.py — Deliverable decomposition. Pure Python.
- pipeline/verification_emitter.py — Verification artifact emission. Pure Python.
- pipeline/combined_m2_pass.py — M2 metadata analysis pass. Pure Python.
- sprint/models.py — TaskEntry, TaskStatus, GateOutcome, GateDisplayState (with FSM transitions), TaskResult, PhaseStatus, SprintOutcome, Phase, CheckpointEntry, SprintConfig, PhaseResult, SprintResult, MonitorState, TurnLedger (economic budget model), ShadowGateMetrics. All pure data.
- sprint/checkpoints.py — Checkpoint path extraction from markdown, manifest build/write/recovery, evidence discovery. Pure Python + file I/O.
- sprint/config.py — Phase discovery from tasklist index, config loading. Pure markdown parsing.
- sprint/diagnostics.py — DiagnosticCollector, FailureClassifier, ReportGenerator. Pure Python.
- sprint/kpi.py — KPI report generation from gate results + TurnLedger. Pure Python.
- sprint/retrospective.py — Retrospective generation. Pure Python.
- sprint/logging_.py — Execution-log.jsonl/md writer. Pure Python.
- roadmap/gates.py — 14 GateCriteria constants + 30+ semantic check functions (pure Python: frontmatter, heading structure, cross-refs, table schema, sentinels, routing consistency).
- roadmap/convergence.py — DeviationRegistry (file-backed JSON with stable IDs), convergence loop logic, regression detection. Core algorithm is portable.
- roadmap/fidelity_checker.py — FR-to-implementation exact name matching via AST scan. Pure Python.
- roadmap/cosmetic_remediator.py — Deterministic auto-fix of cosmetic gate failures. Pure regex transforms.
- roadmap/obligation_scanner.py — Obligation scanning. Pure Python text analysis.
- roadmap/integration_contracts.py — Integration contract analysis. Pure Python.
- roadmap/structural_checkers.py — Structural deviation checkers. Pure Python.
- roadmap/spec_parser.py — Spec markdown parser. Pure Python.
- roadmap/fingerprint.py — Code fingerprint generation. Pure Python.
- roadmap/validate_gates.py — Validation gate criteria. Pure Python.
- tasklist/gates.py, models.py — Pure data.
- audit/* (entire module, ~6700 LOC) — Static analysis suite: wiring analysis, dependency graphs, dead code, credential scanning, duplication detection, profiling. All pure Python, no subprocess.
- skills/* (24 SKILL.md files) — Portable markdown skill definitions. Runtime-agnostic prompt engineering.
- agents/* (39 .md files, ~8000 LOC) — Agent persona definitions in markdown. Runtime-agnostic.

## Claude-Code-specific (lost on exit)

- pipeline/process.py (ClaudeProcess) — Directly invokes 'claude' CLI with --print --verbose --no-session-persistence --output-format stream-json --max-turns --model flags. Tight coupling to Claude Code's CLI surface. On exit, this entire class must be replaced with a Mastra-compatible agent invocation adapter.
- pipeline/process.py:107-112 — Removes CLAUDECODE and CLAUDE_CODE_ENTRYPOINT env vars to prevent nested-session detection. This is Claude Code-specific internal knowledge.
- sprint/process.py:169-216 — build_prompt() emits '/sc:task Execute all tasks...' which is a Claude Code slash command. The prompt assumes Claude Code's command parsing and tool ecosystem.
- sprint/tmux.py — Creates tmux sessions named 'sc-sprint-*' with specific pane layout (TUI pane + tail pane + summary pane). The self-relaunch re-invokes 'superclaude sprint run ... --no-tmux'. Tmux is a deployment choice, not a Claude Code dependency, but the pane protocol is custom.
- install_hooks.py — Installs shell scripts to ~/.claude/hooks/ and merges into ~/.claude/settings.json. Claude Code's hook system (PreToolUse, PostToolUse, FileChanged, SessionInit, SubagentStart, SubagentStop) is irreducibly Claude-Code-specific.
- install_commands.py — Copies command .md files to ~/.claude/commands/sc/. The /sc:* slash command namespace exists only in Claude Code.
- install_agents.py — Installs agent personas into Claude Code's agent configuration system.
- install_mcp.py — Registers MCP servers into Claude Code's MCP configuration. MCP is a standard but the installation target is Claude Code-specific.
- sprint/monitor.py — Parses the NDJSON stream-json output format specific to 'claude --output-format stream-json'. The event shape (assistant message, tool use, turn markers, token counts) is Anthropic's Claude Code wire format.
- sprint/executor.py:1196-1200 — TurnLedger initial_budget = config.max_turns * len(config.active_phases). The 'max_turns' concept is specific to Claude Code's --max-turns flag.
- sprint/executor.py:1324 — ClaudeProcess config/phase instantiation with env_vars including CLAUDE_WORK_DIR isolation. CLAUDE_WORK_DIR is a Claude Code environment variable.
- sprint/commands.py:110-114 — --permission-flag choices are Claude Code CLI flags: --dangerously-skip-permissions and --allow-hierarchical-permissions.
- roadmap/executor.py:1254-1280 — _ClaudeRunner inner class wraps ClaudeProcess for convergence remediation steps with output_format='text'.
- Freshness hooks (freshness-*.sh) — Shell scripts that respond to Claude Code lifecycle events (session start, user prompt, pre-edit, post-read, subagent start/stop). Tied to Claude Code's hook event model.
- settings.json merge — The atomic merge of hook registrations into ~/.claude/settings.json assumes Claude Code's settings schema.

## Reuse assessment

"REUSE ASSESSMENT: The SuperClaude codebase is a ~73K-LOC Python orchestration layer with three distinct strata. Stratum 1 (portable IP, ~50K LOC): pipeline base types (models.py, gates.py, executor.py, trailing_gate.py), FMEA analysis suite (classifier, domains, invariants, dataflow, guards, conflicts), static audit suite (audit/*, ~6.7K LOC), sprint/roadmap models, checkpoint system, convergence engine (DeviationRegistry, convergence loop algorithm), semantic check functions, cosmetic remediation, all SKILL.md and agent .md files. These are pure Python or markdown with zero Claude Code runtime coupling. Stratum 2 (adaptable patterns, ~12K LOC): sprint executor orchestration loop (phase sequencing, budget tracking, stall detection, TUI, KPI, retrospective) and roadmap executor pipeline (8-step sequencing, parallel dispatch, convergence integration). These contain ClaudeProcess coupling but the orchestration logic itself (turn ledger, gate enforcement, convergence control, parallel step dispatch with cancellation) is pattern-portable. Stratum 3 (irreplaceable, ~11K LOC): ClaudeProcess (245 LOC + sprint subclass 385 LOC), monitor.py stream-json parser (570 LOC), tmux.py session management (325 LOC), install_hooks/commands/agents/mcp (1400+ LOC), and all prompt files (roadmap/prompts.py 1370 LOC, prd/prompts.py 1455 LOC). The strategic assessment: replacing the single ClaudeProcess/stream-json seam (Stratum 3, ~1200 LOC) with a Mastra agent adapter would unlock ~62K LOC of portable IP for multi-tenant reuse. The gate logic, convergence engine, FMEA suite, audit tools, checkpoint system, and markdown harness (skills/agents) are all runtime-agnostic. The TUI, tmux, and install pipelines would need replacement but represent well-understood patterns. 'Do not port' remains viable because the Claude Code dependency is a single, well-isolated subprocess layer, but the 50K+ LOC of portable gate/convergence/FMEA/audit/harness IP represents significant competitive advantage that would be lost without a replatforming vehicle."
