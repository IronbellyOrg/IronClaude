# Diff Analysis: `/sc:forensic` design vs `sc:troubleshoot` v2 bundle

## Metadata

- Generated: 2026-05-21
- Artifacts compared: 2 (forensic-breakdown.md; troubleshoot v2 bundle = command + skill + 5 refs + 2 agents)
- Mode: A (compare existing files)
- Focus: differences only (no value judgements)
- Variants treated: Variant A = forensic design (`.dev/eval-workspaces/sc-troubleshoot/forensic-analysis/forensic-breakdown.md`); Variant B = troubleshoot v2 bundle (`src/superclaude/commands/troubleshoot.md` + `src/superclaude/skills/sc-troubleshoot-protocol/**`)
- Total differences found: 31 (S: 5, C: 18, X: 0, U: 6, A: 2)

## Structural Differences

| # | Area | Variant A (forensic) | Variant B (v2 bundle) | Severity |
|---|------|---------------------|------------------------|----------|
| S-001 | Top-level shape | Single 713-line breakdown document organized into 20 sections describing a pipeline-as-spec | Multi-file bundle: 229-line command + 373-line skill + 5 refs + 2 agents | High |
| S-002 | Section count for spec content | 20 sections (Executive Summary → Citations) | 1 command file + 1 skill (Purpose → Wave 6 → Refs) | High |
| S-003 | Refs strategy | All design content inline in `forensic-breakdown.md` plus 29 source files in the backlog; no on-demand load contract | Skill loads `refs/*.md` lazily per wave (rubric in W2, triage-checklist in W1, hypothesis card in W1+W3, report template in W5, remediation handoff in W6) | High |
| S-004 | Authored layering | Pipeline-defined-by-spec; runtime layer is the orchestrator subprocess + sprint/tfep.py CLI module | Command file is a 3-step dispatcher; skill carries the full protocol; agents and refs are addressable units | High |
| S-005 | Document type | Forensic-breakdown is a synthesis/analysis document over a backlog (consumes 12k lines across 29 files) | Bundle is the shipped implementation surface itself | Low |

## Content Differences

| # | Topic | Variant A (forensic) | Variant B (v2 bundle) | Severity |
|---|-------|---------------------|------------------------|----------|
| C-001 | Scope of problems addressed | Generic forensic QA/debug pipeline for any codebase or release; auto-discovers investigation domains across the whole repo (`forensic-spec.md:48-51`); also auto-invoked by `sc:task-unified` TFEP on failing tests | Symptom-driven diagnosis of a single reported issue (bug/build/performance/deployment/security/test); always paired with an issue description or `--scope` | High |
| C-002 | Activation model | Command file calls `sc:forensic-protocol` skill as MANDATORY pre-step; auto-invoked by `task-unified` on TFEP escalation; explicit `--caller` flag in design | Command auto-activates from symptom keywords ("why is X broken", stack traces, "flaky"), explicit `/sc:troubleshoot ...`, or programmatic invocation of the skill; broader keyword-trigger surface than forensic | High |
| C-003 | Tier / phase structure | 8 numbered phases (Phase 0 Recon → Phase 1 RCA → Phase 2 Hypothesis Debate → Phase 3 Fix Proposals → Phase 3b Fix Debate → Phase 4 Implementation → Phase 5 Validation → Phase 6 Final Report) | 3 tiers expressed as 7 waves (Wave 0 Parse → Wave 1 Tier 1 Triage → Wave 2 Confidence Gate → Wave 3 Tier 2 Hypotheses → Wave 4 Tier 2 Adversarial → Wave 5 Synthesis+Report → Wave 6 Tier 3 Remediation) | High |
| C-004 | Execution model | Each phase agent is a separate `claude --print` SUBPROCESS spawned by `ForensicOrchestrator` (no IPC); inter-phase contracts via files on disk | All agents spawned in-session via `Task` tool; in-session skill invocation for `sc:adversarial-protocol`, `task-builder`, `/sc:reflect` | High |
| C-005 | Orchestrator's role | Strict dispatcher — Opus orchestrator NEVER reads source; capped at ≤8,000 tokens total across the whole pipeline (`forensic-spec.md:215-216` NFR-001, `:309-322`); reads only structured JSON / Markdown selection files | Orchestrator (Claude) reads files itself in Waves 0/1/5; runs MCP queries, spawns sub-agents, validates `file:line` (with `evidence-validator` agent or inline fallback); no formal orchestrator-token cap | High |
| C-006 | Agent inventory | Subprocess agents per phase: Phase 0 = 3 Haiku; Phase 1 = N Haiku/Sonnet (risk-tiered); Phase 2/3b = adversarial-protocol's advocate set; Phase 3 = M Sonnet; Phase 4 = specialist Sonnet + quality-engineer Sonnet; Phase 5 = Haiku + 2 Sonnet; Phase 6 = Opus orchestrator. Light tier = 2-4 Sonnet only. Zero new `src/superclaude/agents/` agents | In-session Task agents: `root-cause-analyst`, `confidence-calibrator`, `evidence-validator`, plus 2-4 specialist agents drawn from {`quality-engineer`, `performance-engineer`, `security-engineer`, `devops-architect`, `refactoring-expert`, `system-architect`}, plus `self-review`. Two new dedicated agent files (`evidence-validator.md`, `confidence-calibrator.md`) | High |
| C-007 | Model tiering | Explicit decision matrix: Haiku (recon/lint), Sonnet (deep analysis/fixes/tests), Opus (synthesis/coordination only); light tier collapses to Sonnet-only (`forensic-spec.md:1509-1540`) | All agents default to their per-agent model (sonnet for the two new agents); `--models <tier:model,...>` override; no Haiku tier, no Opus orchestrator pin | High |
| C-008 | MCP usage by phase | Explicit MCP routing table (Serena Phase 0/1/4, Context7 Phase 0/1/4, Sequential Phase 1/2/3); per-server concurrency cap NFR-010 ≤3; prompt-based MCP budgets per agent (3 Serena + 1 Context7 per Phase 1 domain; 5 Serena + 2 Context7 per Phase 4a fix) | Per-tier MCP coverage: auggie + serena every tier for in-repo grounding; context7 + tavily Tier 2 only; sequential Tier 2 synthesis only; tavily rate-cap ≤2 queries/invocation; no per-server concurrency cap | Medium |
| C-009 | Adversarial integration pattern | Forensic *fully delegates* Phase 2 and Phase 3b to `/sc:adversarial`; designates Phase 3b `fix-selection.md` as the PRIMARY decision point; Phase 2 uses `--depth deep`, Phase 3b uses `--depth standard` | v2 invokes `sc:adversarial-protocol` only in Wave 4, and only conditionally (≥2 competing fixes); on consensus, debate is *skipped* to avoid token waste; depth chosen between quick (same-diagnosis variants) and standard | High |
| C-010 | Two-axis vs single-axis mode | Two orthogonal axes: `--tier light\|standard\|deep` (pipeline scope) decoupled from `--depth quick\|standard\|deep` (adversarial debate depth) | Single axis: `--depth quick\|standard\|deep` controls escalation only (Tier 1 cap, default rubric-driven, force Tier 2 respectively); no pipeline-scope flag | High |
| C-011 | Token budget profile | Light tier (~5-8k), standard (~50-60k), deep on top; orchestrator pinned ≤8k; Phase 6 ≤2k; explicit budget-per-phase table | Tier 1 ≤6k Claude (auggie 2-5k offloaded); Tier 2 no-adversarial 15-30k; Tier 2 + adversarial 30-60k; Tier 3 +20-40k; budgets are *targets*, not hard caps | Medium |
| C-012 | Output contract | `final-report.md` (Phase 6) summarising 6 summary artifacts; per-phase manifests; `tfep-report.md` + `tasklist-insertion.md` for light tier; return contract YAML with `status`, `root_cause_path`, `solution_plan_path`, `tasklist_insertion_path`, `recommended_resume_mode`, `recommended_escalation`, `requires_user_review`, `test_is_wrong` | `REPORT.md` always; structured return dict with `status`, `tier_reached`, `report_path`, `audit_log_path`, `confidence`, `escalation_reason`, `hypothesis_cards`, `adversarial_artifacts_dir`, `task_file_path`, `remediation_offered`, `remediation_accepted`; audit log machine-readable header + footer with SC:TROUBLESHOOT:TARGET/SUMMARY HTML-comment blocks | High |
| C-013 | Test strategy | 10 test files (D6.1-D6.13) gated entirely at M6; 6 test types (Smoke per-phase, Integration, Edge case, Schema conformance, Security, Manual review); single 5-file synthetic Python fixture; canned artifacts per phase boundary; 58 success criteria SC-001-SC-058 | Eval workspaces under `.dev/eval-workspaces/sc-troubleshoot/`; no roadmap test-strategy doc; tests run as bundle-shipped pytest suite (project default), not gated by milestone | High |
| C-014 | Failure handling / fallbacks | Three-level adversarial fallback (retry quick → Sonnet scoring agent → emit as-is with `debate_status: "skipped"`); token-overrun via per-phase static rules + `budget_status` field; MCP graceful degradation 4 levels; subprocess SIGTERM→SIGKILL; selective git rollback via `git diff --name-only {baseline}`; resume via `progress.json`; explicit "weakest spot": no fallback when all forensic agents fail | Per-wave error matrix (all MCPs unavail → no-mcp mode; auggie unavail → Grep/Glob; root-cause-analyst fails → degraded Tier 1; all Tier 2 agents fail → downgrade to Tier 1; adversarial fails → highest-confidence proposal; self-review blocker → STOP partial; task-builder unavail → manual; user declines → success; evidence-validator fails → inline fallback + partial; confidence-calibrator fails → inline fallback per card) | High |
| C-015 | CLI / Sprint-runner integration | New `src/superclaude/cli/sprint/tfep.py` module (~450 lines); `ForensicOrchestrator`, `EscalationState`, `perform_rollback`, `inject_remediation_tasks`, `write_incident_report`; modifies `executor.py`, `process.py`, `monitor.py`, `models.py`, `commands.py`, `diagnostics.py`; new flags `--tfep-model`, `--tfep-agents`, `--tfep-budget-multiplier`; new `PhaseStatus.TFEP_HALT`; subprocess parallelism via `ThreadPoolExecutor` | No CLI module changes; no `superclaude sprint` integration; the v2 bundle is exclusively a Claude Code skill+command surface; no `monitor.py`/NDJSON marker scanning; no `claude --print` subprocess pattern | High |
| C-016 | Hallucination contract | Phase 6 reads only 6 summary artifacts, no raw source — architectural constraint enforces hallucination-resistance via dispatcher discipline (`dependency-graph.md:226-232`); 100% evidence coverage required; 100% falsifiability; `file:line` excerpts per hypothesis | Hallucination contract: every claim must cite real `file:line` or real diagnostic command + output; findings that cannot be grounded are DROPPED, not downgraded; `evidence-validator` agent in Wave 5 re-Reads every cited line independently and drops mismatches; if any dropped, REPORT goes `partial` with Grounding Gaps | High |
| C-017 | Remediation chain | Forensic produces `tasklist-insertion.md` for `sc:task-unified --compliance strict` to re-execute the failing phase; remediation tasks use `T{XX}.50+` IDs; resume prompt explicitly skips T01..T{last_completed} and adds git-diff context; selective git rollback before re-launch | Tier 3 remediation chain: task-builder → `/sc:reflect --type task --analyze` → user runs `/task` (never the skill) → `/sc:reflect --type task --validate` as pre-commit gate; no automatic re-launch; no git rollback (changes never applied automatically); diagnosis-first by default | High |
| C-018 | Lifecycle / checkpointing | Every phase writes artifacts; `progress.json` self-describing; stale-codebase detection via `git rev-parse HEAD` on resume; checkpoint/resume borrowed from `sc:cleanup-audit-protocol` pattern; explicit `--resume` mode and `--dry-run` | No formal checkpoint/resume primitive; the output dir under `.dev/troubleshoot/<slug>-<ts>/` holds hypothesis cards, calibrations, adversarial artifacts, REPORT.md, audit.log; re-running invokes a new slug+timestamp dir | High |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|------|----|----|---|

*(None — these are two different designs, not two designs of the same artifact. There are no direct contradictions, only divergences. All differences are captured under Structural / Content / Unique / Shared sections.)*

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | A (forensic) | `--tier × --depth` two-axis mode model decoupling pipeline scope from debate depth | High |
| U-002 | A (forensic) | Sprint-runner CLI module (`sprint/tfep.py`) with `ForensicOrchestrator`, NDJSON marker detection, `PhaseStatus.TFEP_HALT`, selective git rollback, remediation injection, resume prompts | High |
| U-003 | A (forensic) | Orchestrator-as-dispatcher prohibition (Opus never reads source; ≤8k token cap across the whole pipeline) as a *structural* hallucination contract | High |
| U-004 | A (forensic) | Explicit 3-tier escalation gradient (light → standard → halt) with `escalation_count` tracking and budget multiplier (`--tfep-budget-multiplier`) | High |
| U-005 | B (v2) | Dedicated `evidence-validator` agent file (independent re-Read of every cited `file:line`, drops mismatches before report ships) + dedicated `confidence-calibrator` agent file (rubric re-grade stripped of formation context) | High |
| U-006 | B (v2) | Lazy ref loading per wave (rubric W2, triage W1, hypothesis-card W1+W3, report-template W5, remediation-handoff W6); never pre-loaded | Medium |

## Shared Assumptions

| # | Assumption | Source Agreement | Impact | Status |
|---|------------|------------------|--------|--------|
| A-001 | Adversarial debate (`sc:adversarial-protocol`) is the right adjudication primitive for resolving competing hypotheses/fixes | Both designs delegate competing-fix selection to the same skill, with the same 5-step protocol contract | High | UNSTATED in both — neither artifact justifies *why* adversarial debate (vs voting, vs ranking, vs human pick) is the correct merge mechanism for this domain |
| A-002 | A single REPORT.md / final-report.md output is the right user-facing terminal artifact (rather than e.g. a streaming diff, a notebook, or an issue draft) | Both terminate at a single Markdown report consumed by the user/caller | Medium | UNSTATED — both assume a static synthesis is the right unit of user attention |

## Summary

- Total structural differences: 5
- Total content differences: 18
- Total contradictions: 0 (different designs, not different artifacts of the same thing)
- Total unique contributions: 6
- Total shared assumptions surfaced: 2 (both UNSTATED)
- Highest-severity items: S-001, S-002, S-003, S-004, C-001, C-002, C-003, C-004, C-005, C-006, C-007, C-009, C-010, C-012, C-013, C-014, C-015, C-016, C-017, C-018, U-001, U-002, U-003, U-004, U-005, A-001

These differences are dense around five themes: (1) scope (project-wide forensic sweep vs symptom-driven diagnosis), (2) execution model (subprocess pipeline vs in-session waves), (3) orchestrator discipline (strict dispatcher vs participant orchestrator), (4) integration surface (CLI sprint-runner + skill vs Claude Code skill+command only), (5) adversarial coupling (forensic always delegates Phase 2+3b; v2 conditionally delegates Wave 4 only).
