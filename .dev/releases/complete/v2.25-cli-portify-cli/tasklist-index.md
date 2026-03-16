# TASKLIST INDEX -- CLI Portify Pipeline

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | CLI Portify Pipeline |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-03-16 |
| TASKLIST_ROOT | `.dev/releases/current/v2.25-cli-portify-cli/` |
| Total Phases | 11 |
| Total Tasks | 68 |
| Total Deliverables | 82 |
| Complexity Class | HIGH |
| Primary Persona | backend |
| Consulting Personas | architect, qa, analyzer |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `.dev/releases/current/v2.25-cli-portify-cli/tasklist-index.md` |
| Phase 1 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-1-tasklist.md` |
| Phase 2 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-2-tasklist.md` |
| Phase 3 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-3-tasklist.md` |
| Phase 4 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-4-tasklist.md` |
| Phase 5 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-5-tasklist.md` |
| Phase 6 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-6-tasklist.md` |
| Phase 7 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-7-tasklist.md` |
| Phase 8 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-8-tasklist.md` |
| Phase 9 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-9-tasklist.md` |
| Phase 10 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-10-tasklist.md` |
| Phase 11 Tasklist | `.dev/releases/current/v2.25-cli-portify-cli/phase-11-tasklist.md` |
| Execution Log | `.dev/releases/current/v2.25-cli-portify-cli/execution-log.md` |
| Checkpoint Reports | `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/` |
| Evidence Directory | `.dev/releases/current/v2.25-cli-portify-cli/evidence/` |
| Artifacts Directory | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/` |
| Validation Reports | `.dev/releases/current/v2.25-cli-portify-cli/validation/` |
| Feedback Log | `.dev/releases/current/v2.25-cli-portify-cli/feedback-log.md` |

---

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Architecture Confirmation | T01.01-T01.07 | EXEMPT: 3, STANDARD: 4 |
| 2 | phase-2-tasklist.md | Prerequisites and Config | T02.01-T02.09 | STANDARD: 7, STRICT: 2 |
| 3 | phase-3-tasklist.md | Executor Skeleton and Observability | T03.01-T03.13 | STRICT: 5, STANDARD: 8 |
| 4 | phase-4-tasklist.md | Gate System | T04.01-T04.03 | STRICT: 2, STANDARD: 1 |
| 5 | phase-5-tasklist.md | Analysis Pipeline | T05.01-T05.05 | STRICT: 2, STANDARD: 3 |
| 6 | phase-6-tasklist.md | Specification Pipeline | T06.01-T06.06 | STRICT: 2, STANDARD: 4 |
| 7 | phase-7-tasklist.md | Release Spec Synthesis | T07.01-T07.04 | STRICT: 2, STANDARD: 2 |
| 8 | phase-8-tasklist.md | Panel Review Loop | T08.01-T08.06 | STRICT: 3, STANDARD: 3 |
| 9 | phase-9-tasklist.md | Observability Completion | T09.01-T09.04 | STANDARD: 3, STRICT: 1 |
| 10 | phase-10-tasklist.md | CLI Integration | T10.01-T10.05 | STRICT: 2, STANDARD: 3 |
| 11 | phase-11-tasklist.md | Verification and Release Readiness | T11.01-T11.06 | STRICT: 3, STANDARD: 3 |

---

## Source Snapshot

- Enterprise-grade pipeline (complexity 0.92) converting SuperClaude skill workflows into deterministic CLI runners via 12-step sequentially-gated execution
- 65 requirements (47 functional, 18 non-functional) across 8 technical domains; delivers `src/superclaude/cli/cli_portify/` registered in `src/superclaude/cli/main.py`
- Sequential-only pipeline with 12-gate enforcement (STANDARD/STRICT tiers), convergence loop capped at 3 iterations, full resume/checkpoint support
- Phase 6 amended: `--file` passthrough removed (confirmed broken v2.24.5); inline `-p` embedding only; content >120KB raises `PortifyValidationError`
- Success requires all 14 SC criteria (SC-001–SC-014) validated by automated tests

---

## Deterministic Rules Applied

- Phase renumbering: Roadmap Phase 0–10 → output Phase 1–11 (sequential, no gaps, Section 4.3)
- Task ID scheme: `T<PP>.<TT>` zero-padded 2-digit phase and task numbers (Section 4.5)
- R-020 split into two tasks (T03.04 executor + T03.05 dry-run unit test) per Section 4.4 (feature AND test strategy)
- Checkpoint cadence: after every 5 tasks within a phase + end-of-phase checkpoint (Section 4.8)
- Deliverable registry: D-0001 through D-0082 in global task/deliverable appearance order (Section 5.1)
- Effort scoring: EFFORT_SCORE formula applied; scores map XS/S/M/L/XL per Section 5.2.1
- Risk scoring: RISK_SCORE formula applied; scores map Low/Medium/High per Section 5.2.2
- Tier classification: STRICT(1) > EXEMPT(2) > LIGHT(3) > STANDARD(4) priority; compound phrases checked first (Section 5.3)
- Verification routing: STRICT→sub-agent quality-engineer 60s; STANDARD→direct test 30s; EXEMPT→skip (Section 4.10)
- MCP requirements: STRICT requires Sequential+Serena; STANDARD preferred Sequential+Context7 (Section 5.5)
- Traceability: every R-### maps to at least one T<PP>.<TT> and D-#### below

---

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (≤20 words) |
|---|---|---|
| R-001 | Phase 1 | Validate target architecture against existing SuperClaude CLI framework |
| R-002 | Phase 1 | Confirm imports and stable locations for PipelineConfig, Step, StepResult, GateCriteria, GateMode, SemanticCheck |
| R-003 | Phase 1 | Assess all 14 open questions; resolve 5 blocking OQs: OQ-001, OQ-003, OQ-004, OQ-009, OQ-011 |
| R-004 | Phase 1 | Assess OQ-002 kill signal, OQ-013 PASS_NO_SIGNAL retry as potential blockers |
| R-005 | Phase 1 | Confirm prompt splitting threshold location (executor vs. prompt builder) |
| R-006 | Phase 1 | Confirm overwrite rules for generated modules using Generated by / Portified from markers |
| R-007 | Phase 1 | Confirm OQ-007 and OQ-014 are non-blocking; document for respective phases |
| R-008 | Phase 2 | Implement workflow path resolution under src/superclaude/skills/; require SKILL.md |
| R-009 | Phase 2 | Implement CLI name derivation: strip sc- prefix and -protocol suffix, normalize to kebab-case |
| R-010 | Phase 2 | Implement collision detection: scan src/superclaude/cli/, allow overwrite only for portified modules |
| R-011 | Phase 2 | Validate output destination: parent exists and is writable |
| R-012 | Phase 2 | Create workdir at .dev/portify-workdir/<cli_name>/ |
| R-013 | Phase 2 | Emit portify-config.yaml with resolved paths |
| R-014 | Phase 2 | Implement component discovery and inventory: scan SKILL.md, command .md, refs/, rules/, templates/, scripts/, decisions.yaml |
| R-015 | Phase 2 | Emit component-inventory.yaml with {path, lines, purpose, type} per component |
| R-016 | Phase 2 | Enforce timeouts: 30s input-validation, 60s component-discovery |
| R-017 | Phase 3 | Implement core domain models: PortifyPhaseType, ConvergenceState, PortifyConfig, PortifyStep, PortifyStepResult, PortifyOutcome, PortifyStatus, MonitorState, TurnLedger |
| R-018 | Phase 3 | Implement __init__.py with Generated by / Portified from marker |
| R-019 | Phase 3 | Implement step registration in mandated module generation order |
| R-020 | Phase 3 | Implement executor: sequential execution, --dry-run, --resume, signal handling |
| R-021 | Phase 3 | Implement claude binary detection via shutil.which("claude") |
| R-022 | Phase 3 | Implement timeout classification: exit code 124 → TIMEOUT, other non-zero → ERROR |
| R-023 | Phase 3 | Implement _determine_status() classification based on exit code + EXIT_RECOMMENDATION + artifact presence |
| R-024 | Phase 3 | Implement retry mechanism with retry_limit=1 for Claude-assisted steps |
| R-025 | Phase 3 | Implement TurnLedger: can_launch() check, budget exhaustion → HALTED outcome |
| R-026 | Phase 3 | Implement signal handlers: SIGINT/SIGTERM → complete current step result → INTERRUPTED outcome |
| R-027 | Phase 3 | Implement mandatory return-contract.yaml emission on all outcomes |
| R-028 | Phase 3 | Implement resume_command() with exact CLI command |
| R-029 | Phase 3 | Implement suggested_resume_budget: remaining * 25 where remaining = PENDING or INCOMPLETE steps |
| R-030 | Phase 3 | Implement OutputMonitor tracking: bytes, growth rate, stall seconds, events, line count, convergence iteration, findings count, placeholder count |
| R-031 | Phase 3 | Implement execution-log.jsonl (machine-readable) and execution-log.md (human-readable) skeleton |
| R-032 | Phase 3 | Implement stall detection with kill action via OutputMonitor.growth_rate_bps |
| R-033 | Phase 3 | Implement basic PortifyTUI start/stop lifecycle |
| R-034 | Phase 4 | Implement all 12 gates G-000 through G-011 with frontmatter checks, min line counts, tier, GateMode.BLOCKING |
| R-035 | Phase 4 | Implement semantic check functions returning tuple[bool, str] |
| R-036 | Phase 4 | Implement gate diagnostics formatting |
| R-037 | Phase 5 | Implement protocol-mapping prompt builder; generate protocol-map.md with YAML frontmatter; enforce EXIT_RECOMMENDATION |
| R-038 | Phase 5 | Implement analysis-synthesis prompt builder; generate portify-analysis-report.md; enforce EXIT_RECOMMENDATION |
| R-039 | Phase 5 | Enforce 600s timeout for protocol-mapping and analysis-synthesis steps |
| R-040 | Phase 5 | Implement user-review-p1: write phase1-approval.yaml status:pending, print resume instructions, exit cleanly |
| R-041 | Phase 5 | Implement --resume logic: require status:approved in approval YAML with YAML parse + schema validation |
| R-042 | Phase 6 | Implement step-graph-design prompt builder → step-graph-spec.md |
| R-043 | Phase 6 | Implement models-gates-design prompt builder → models-gates-spec.md |
| R-044 | Phase 6 | Implement prompts-executor-design prompt builder → prompts-executor-spec.md |
| R-045 | Phase 6 | Implement pipeline-spec-assembly: programmatic pre-assembly + Claude synthesis → portify-spec.md |
| R-046 | Phase 6 | Enforce EXIT_RECOMMENDATION on all Phase 2 Claude steps; 600s timeout per step |
| R-047 | Phase 6 | Implement user-review-p2: status:completed, blocking gates passed, step_mapping entries; phase2-approval.yaml YAML validation |
| R-048 | Phase 7 | Load release-spec-template.md from src/superclaude/examples/; create working copy |
| R-049 | Phase 7 | Implement 4-substep synthesis (3a–3d): working copy, populate 13 sections, 3-persona brainstorm, incorporate findings |
| R-050 | Phase 7 | Validate zero {{SC_PLACEHOLDER:*}} sentinels; validate Section 12 exists; emit portify-release-spec.md |
| R-051 | Phase 7 | AMENDED: inline embedding only; raise PortifyValidationError if >120KB; 900s timeout |
| R-052 | Phase 8 | Implement convergence state machine: NOT_STARTED→REVIEWING→INCORPORATING→SCORING→CONVERGED\|ESCALATED |
| R-053 | Phase 8 | Implement per-iteration logic 4a–4d: expert focus pass, finding incorporation, panel critique scoring, convergence scoring |
| R-054 | Phase 8 | Implement CONVERGED: zero unaddressed CRITICALs → status:success |
| R-055 | Phase 8 | Implement ESCALATED: 3 iterations exhausted → status:partial |
| R-056 | Phase 8 | Gate downstream_ready=true only when overall>=7.0; emit panel-report.md on both terminal conditions |
| R-057 | Phase 8 | Use internal convergence loop NOT outer retry; enforce 1200s timeout |
| R-058 | Phase 9 | Complete PortifyTUI: full real-time progress display via rich |
| R-059 | Phase 9 | Complete OutputMonitor: convergence iteration, findings count, placeholder count tracking |
| R-060 | Phase 9 | Implement failure diagnostics: gate failure reason, exit code, missing artifacts, resume guidance |
| R-061 | Phase 9 | Finalize execution-log.jsonl and execution-log.md with complete event coverage |
| R-062 | Phase 10 | Implement Click command group with run subcommand; wire --name, --output, --max-turns, --model, --dry-run, --resume, --debug |
| R-063 | Phase 10 | Implement --dry-run: limit to PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION phase types |
| R-064 | Phase 10 | Register cli_portify_group in src/superclaude/cli/main.py via main.add_command() |
| R-065 | Phase 10 | Implement prompt splitting: if aggregate prompt >300 lines, split to portify-prompts.md |
| R-066 | Phase 10 | Verify module generation order: models→gates→prompts→config→inventory→monitor→process→executor→tui→logging_→diagnostics→commands→__init__ |
| R-067 | Phase 11 | Unit tests: all 5 validation error paths, all 12 gates, _determine_status() exhaustively, TurnLedger budget, exit codes |
| R-068 | Phase 11 | Integration tests: dry-run, resume across both review boundaries, signal handling, gate failure + retry |
| R-069 | Phase 11 | Edge case tests: ambiguous skill name, name collision, budget exhaustion, ESCALATED path, template >120KB |
| R-070 | Phase 11 | Run uv run pytest; validate all 14 success criteria SC-001–SC-014 |
| R-071 | Phase 11 | Perform sample runs: valid workflow, ambiguous, insufficient budget, interrupted, escalation |
| R-072 | Phase 11 | Confirm logs and workdir behavior; produce release readiness checklist |

---

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | Architecture decision notes | EXEMPT | Skip | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0001/spec.md` | S | Low |
| D-0002 | T01.02 | R-002 | Import verification report | EXEMPT | Skip | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0002/evidence.md` | S | Low |
| D-0003 | T01.03 | R-003 | OQ resolution list (blocking/non-blocking) | EXEMPT | Skip | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0003/spec.md` | M | Low |
| D-0004 | T01.04 | R-004 | OQ-002/OQ-013 blocker assessment | EXEMPT | Skip | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0004/spec.md` | S | Low |
| D-0005 | T01.05 | R-005 | Prompt split threshold decision | EXEMPT | Skip | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0005/spec.md` | XS | Low |
| D-0006 | T01.06 | R-006 | Overwrite rules documentation | EXEMPT | Skip | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0006/spec.md` | XS | Low |
| D-0007 | T01.07 | R-007 | Non-blocking OQ documentation (OQ-007, OQ-014) | EXEMPT | Skip | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0007/spec.md` | XS | Low |
| D-0008 | T02.01 | R-008 | `config.py` workflow path resolution | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0008/spec.md` | M | Low |
| D-0009 | T02.02 | R-009 | `config.py` CLI name derivation logic | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0009/spec.md` | S | Low |
| D-0010 | T02.03 | R-010 | `config.py` collision detection | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0010/spec.md` | M | Low |
| D-0011 | T02.04 | R-011 | `config.py` output destination validation | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0011/spec.md` | S | Low |
| D-0012 | T02.05 | R-012 | `workdir.py` workdir creation | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0012/spec.md` | S | Low |
| D-0013 | T02.06 | R-013 | `portify-config.yaml` emission | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0013/evidence.md` | S | Low |
| D-0014 | T02.07 | R-014 | `inventory.py` component scanner | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0014/spec.md` | M | Low |
| D-0015 | T02.08 | R-015 | `component-inventory.yaml` emission | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0015/evidence.md` | S | Low |
| D-0016 | T02.09 | R-016 | Timeout enforcement (30s/60s) | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0016/evidence.md` | S | Low |
| D-0017 | T03.01 | R-017 | `models.py` with all 9 domain types | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0017/spec.md` | L | Low |
| D-0018 | T03.02 | R-018 | `__init__.py` with marker | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0018/spec.md` | XS | Low |
| D-0019 | T03.03 | R-019 | Step registration order enforcement | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0019/spec.md` | S | Low |
| D-0020 | T03.04 | R-020 | `executor.py` sequential + resume + signal | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0020/spec.md` | XL | Low |
| D-0021 | T03.05 | R-020 | Dry-run unit test (SC-012 early) | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0021/evidence.md` | S | Low |
| D-0022 | T03.06 | R-021 | `claude` binary detection in `executor.py` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0022/evidence.md` | XS | Low |
| D-0023 | T03.07 | R-022 | Timeout classification (exit 124→TIMEOUT) | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0023/evidence.md` | S | Low |
| D-0024 | T03.08 | R-023 | `_determine_status()` in `executor.py` | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0024/spec.md` | M | Low |
| D-0025 | T03.09 | R-024 | Retry mechanism (retry_limit=1) in `executor.py` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0025/spec.md` | S | Low |
| D-0026 | T03.10 | R-025 | `TurnLedger.can_launch()` + HALTED outcome | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0026/spec.md` | M | Low |
| D-0027 | T03.11 | R-026, R-027 | Signal handlers + `return-contract.yaml` emission | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0027/spec.md` | M | Low |
| D-0028 | T03.12 | R-028, R-029 | `resume_command()` + `suggested_resume_budget` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0028/spec.md` | S | Low |
| D-0029 | T03.13 | R-030, R-031, R-032, R-033 | `monitor.py`, `logging_.py` skeleton, `tui.py` lifecycle | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0029/spec.md` | L | Low |
| D-0030 | T04.01 | R-034 | `gates.py` G-000–G-011 implementations | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0030/spec.md` | XL | Low |
| D-0031 | T04.02 | R-035 | Semantic check helpers in `gates.py` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0031/spec.md` | M | Low |
| D-0032 | T04.03 | R-036 | Gate diagnostics formatter in `gates.py` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0032/spec.md` | S | Low |
| D-0033 | T05.01 | R-037 | `prompts.py` protocol-mapping builder + `protocol-map.md` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0033/spec.md` | M | Low |
| D-0034 | T05.02 | R-038 | `prompts.py` analysis-synthesis builder + `portify-analysis-report.md` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0034/spec.md` | M | Low |
| D-0035 | T05.03 | R-039 | 600s timeout enforcement on analysis steps | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0035/evidence.md` | S | Low |
| D-0036 | T05.04 | R-040 | `user-review-p1` gate + `phase1-approval.yaml` (status:pending) | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0036/spec.md` | M | Low |
| D-0037 | T05.05 | R-041 | Resume logic with YAML parse + schema validation for `phase1-approval.yaml` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0037/spec.md` | M | Low |
| D-0038 | T06.01 | R-042 | `prompts.py` step-graph-design builder + `step-graph-spec.md` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0038/spec.md` | M | Low |
| D-0039 | T06.02 | R-043 | `prompts.py` models-gates-design builder + `models-gates-spec.md` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0039/spec.md` | M | Low |
| D-0040 | T06.03 | R-044 | `prompts.py` prompts-executor-design builder + `prompts-executor-spec.md` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0040/spec.md` | M | Low |
| D-0041 | T06.04 | R-045 | Pipeline-spec-assembly logic + `portify-spec.md` | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0041/spec.md` | L | Low |
| D-0042 | T06.05 | R-046 | EXIT_RECOMMENDATION + 600s enforcement on Phase 2 steps | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0042/evidence.md` | S | Low |
| D-0043 | T06.06 | R-047 | `user-review-p2` gate + `phase2-approval.yaml` YAML validation | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0043/spec.md` | M | Low |
| D-0044 | T07.01 | R-048 | Template loader + working copy creator in `prompts.py` | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0044/spec.md` | S | Low |
| D-0045 | T07.02 | R-049 | 4-substep synthesis (3a–3d) in release spec step | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0045/spec.md` | XL | Low |
| D-0046 | T07.03 | R-050 | Placeholder validator + `portify-release-spec.md` emission | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0046/spec.md` | M | Low |
| D-0047 | T07.04 | R-051 | Inline embed guard (>120KB → PortifyValidationError) + 900s timeout | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0047/spec.md` | M | Low |
| D-0048 | T08.01 | R-052 | Convergence state machine in `review.py` | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0048/spec.md` | L | Low |
| D-0049 | T08.02 | R-053 | Per-iteration logic 4a–4d in `review.py` | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0049/spec.md` | XL | Low |
| D-0050 | T08.03 | R-054 | CONVERGED terminal condition (status:success) | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0050/spec.md` | M | Low |
| D-0051 | T08.04 | R-055 | ESCALATED terminal condition (status:partial) | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0051/spec.md` | M | Low |
| D-0052 | T08.05 | R-056 | `downstream_ready` gate (overall>=7.0) + `panel-report.md` on both paths | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0052/spec.md` | M | Low |
| D-0053 | T08.06 | R-057 | Internal convergence loop + 1200s timeout | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0053/spec.md` | S | Low |
| D-0054 | T09.01 | R-058 | `tui.py` complete with rich real-time display | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0054/spec.md` | M | Low |
| D-0055 | T09.02 | R-059 | `monitor.py` complete with convergence/findings/placeholder tracking | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0055/spec.md` | M | Low |
| D-0056 | T09.03 | R-060 | `diagnostics.py` failure diagnostics collection | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0056/spec.md` | M | Low |
| D-0057 | T09.04 | R-061 | `logging_.py` complete with full event coverage | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0057/spec.md` | M | Low |
| D-0058 | T10.01 | R-062 | `commands.py` Click group + all CLI options | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0058/spec.md` | M | Low |
| D-0059 | T10.02 | R-063 | `--dry-run` phase-type filter in `commands.py`/`executor.py` | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0059/spec.md` | S | Low |
| D-0060 | T10.03 | R-064 | `main.py` integration via `main.add_command(cli_portify_group)` | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0060/evidence.md` | S | Low |
| D-0061 | T10.04 | R-065 | Prompt splitter (>300 lines → `portify-prompts.md`) | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0061/spec.md` | S | Low |
| D-0062 | T10.05 | R-066 | Module generation order verification | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0062/evidence.md` | S | Low |
| D-0063 | T11.01 | R-067 | Unit test suite: 5 error paths + 12 gates + status + TurnLedger + exit codes | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0063/evidence.md` | XL | Low |
| D-0064 | T11.02 | R-068 | Integration test suite: dry-run + resume + signal + gate retry | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0064/evidence.md` | XL | Low |
| D-0065 | T11.03 | R-069 | Edge case test suite: ambiguous + collision + budget + escalated + >120KB | STRICT | Sub-agent quality-engineer 60s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0065/evidence.md` | L | Low |
| D-0066 | T11.04 | R-070 | `uv run pytest` passing; SC-001–SC-014 validation report | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0066/evidence.md` | M | Low |
| D-0067 | T11.05 | R-071 | 5 sample run results (valid/ambiguous/budget/interrupted/escalation) | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0067/evidence.md` | M | Low |
| D-0068 | T11.06 | R-072 | Release readiness checklist | STANDARD | Direct test 30s | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0068/spec.md` | S | Low |

---

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | EXEMPT | 85% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0001/spec.md` |
| R-002 | T01.02 | D-0002 | EXEMPT | 85% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0002/evidence.md` |
| R-003 | T01.03 | D-0003 | EXEMPT | 85% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0003/spec.md` |
| R-004 | T01.04 | D-0004 | EXEMPT | 85% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0004/spec.md` |
| R-005 | T01.05 | D-0005 | EXEMPT | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0005/spec.md` |
| R-006 | T01.06 | D-0006 | EXEMPT | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0006/spec.md` |
| R-007 | T01.07 | D-0007 | EXEMPT | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0007/spec.md` |
| R-008 | T02.01 | D-0008 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0008/spec.md` |
| R-009 | T02.02 | D-0009 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0009/spec.md` |
| R-010 | T02.03 | D-0010 | STRICT | 85% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0010/spec.md` |
| R-011 | T02.04 | D-0011 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0011/spec.md` |
| R-012 | T02.05 | D-0012 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0012/spec.md` |
| R-013 | T02.06 | D-0013 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0013/evidence.md` |
| R-014 | T02.07 | D-0014 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0014/spec.md` |
| R-015 | T02.08 | D-0015 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0015/evidence.md` |
| R-016 | T02.09 | D-0016 | STRICT | 85% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0016/evidence.md` |
| R-017 | T03.01 | D-0017 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0017/spec.md` |
| R-018 | T03.02 | D-0018 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0018/spec.md` |
| R-019 | T03.03 | D-0019 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0019/spec.md` |
| R-020 | T03.04, T03.05 | D-0020, D-0021 | STRICT, STANDARD | 88%, 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0020/spec.md`, `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0021/evidence.md` |
| R-021 | T03.06 | D-0022 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0022/evidence.md` |
| R-022 | T03.07 | D-0023 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0023/evidence.md` |
| R-023 | T03.08 | D-0024 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0024/spec.md` |
| R-024 | T03.09 | D-0025 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0025/spec.md` |
| R-025 | T03.10 | D-0026 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0026/spec.md` |
| R-026 | T03.11 | D-0027 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0027/spec.md` |
| R-027 | T03.11 | D-0027 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0027/spec.md` |
| R-028 | T03.12 | D-0028 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0028/spec.md` |
| R-029 | T03.12 | D-0028 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0028/spec.md` |
| R-030 | T03.13 | D-0029 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0029/spec.md` |
| R-031 | T03.13 | D-0029 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0029/spec.md` |
| R-032 | T03.13 | D-0029 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0029/spec.md` |
| R-033 | T03.13 | D-0029 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0029/spec.md` |
| R-034 | T04.01 | D-0030 | STRICT | 90% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0030/spec.md` |
| R-035 | T04.02 | D-0031 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0031/spec.md` |
| R-036 | T04.03 | D-0032 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0032/spec.md` |
| R-037 | T05.01 | D-0033 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0033/spec.md` |
| R-038 | T05.02 | D-0034 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0034/spec.md` |
| R-039 | T05.03 | D-0035 | STRICT | 85% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0035/evidence.md` |
| R-040 | T05.04 | D-0036 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0036/spec.md` |
| R-041 | T05.05 | D-0037 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0037/spec.md` |
| R-042 | T06.01 | D-0038 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0038/spec.md` |
| R-043 | T06.02 | D-0039 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0039/spec.md` |
| R-044 | T06.03 | D-0040 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0040/spec.md` |
| R-045 | T06.04 | D-0041 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0041/spec.md` |
| R-046 | T06.05 | D-0042 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0042/evidence.md` |
| R-047 | T06.06 | D-0043 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0043/spec.md` |
| R-048 | T07.01 | D-0044 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0044/spec.md` |
| R-049 | T07.02 | D-0045 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0045/spec.md` |
| R-050 | T07.03 | D-0046 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0046/spec.md` |
| R-051 | T07.04 | D-0047 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0047/spec.md` |
| R-052 | T08.01 | D-0048 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0048/spec.md` |
| R-053 | T08.02 | D-0049 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0049/spec.md` |
| R-054 | T08.03 | D-0050 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0050/spec.md` |
| R-055 | T08.04 | D-0051 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0051/spec.md` |
| R-056 | T08.05 | D-0052 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0052/spec.md` |
| R-057 | T08.06 | D-0053 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0053/spec.md` |
| R-058 | T09.01 | D-0054 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0054/spec.md` |
| R-059 | T09.02 | D-0055 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0055/spec.md` |
| R-060 | T09.03 | D-0056 | STRICT | 85% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0056/spec.md` |
| R-061 | T09.04 | D-0057 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0057/spec.md` |
| R-062 | T10.01 | D-0058 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0058/spec.md` |
| R-063 | T10.02 | D-0059 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0059/spec.md` |
| R-064 | T10.03 | D-0060 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0060/evidence.md` |
| R-065 | T10.04 | D-0061 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0061/spec.md` |
| R-066 | T10.05 | D-0062 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0062/evidence.md` |
| R-067 | T11.01 | D-0063 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0063/evidence.md` |
| R-068 | T11.02 | D-0064 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0064/evidence.md` |
| R-069 | T11.03 | D-0065 | STRICT | 88% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0065/evidence.md` |
| R-070 | T11.04 | D-0066 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0066/evidence.md` |
| R-071 | T11.05 | D-0067 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0067/evidence.md` |
| R-072 | T11.06 | D-0068 | STANDARD | 80% | `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0068/spec.md` |

---

## Execution Log Template

**Intended Path:** `.dev/releases/current/v2.25-cli-portify-cli/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (≤12 words) | Validation Run | Result | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| (fill during execution) | T01.01 | EXEMPT | D-0001 | Validated architecture against framework | Manual | TBD | `.dev/releases/current/v2.25-cli-portify-cli/evidence/` |

---

## Checkpoint Report Template

For each checkpoint, produce one report at `TASKLIST_ROOT/checkpoints/<name>.md`:

- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** .dev/releases/current/v2.25-cli-portify-cli/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status` — `Overall: Pass | Fail | TBD`
- `## Verification Results` (3 bullets)
- `## Exit Criteria Assessment` (3 bullets)
- `## Issues & Follow-ups`
- `## Evidence`

---

## Feedback Collection Template

**Intended Path:** `.dev/releases/current/v2.25-cli-portify-cli/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (≤15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
| (fill during execution) | | | | | | |

---

## Generation Notes

- R-020 split per Section 4.4: roadmap item contained both executor feature (T03.04) and a named test strategy (T03.05 dry-run unit test for SC-012)
- Phase 0 bucket mapped to output Phase 1 per Section 4.3 sequential renumbering
- All Phase 1 tasks classified EXEMPT: architecture confirmation and OQ resolution are read-only planning operations
- T02.03 (collision detection) and T02.09 (timeout enforcement) escalated to STRICT due to safety-critical behavior (incorrect collision detection could overwrite user modules; incorrect timeout could cause unbounded subprocess hang)
- Risk 11 (template >50KB / --file) marked RESOLVED in source roadmap; T07.04 implements the amendment
- Edge case test R-069 updated from ">50KB" to ">120KB" to match the roadmap amendment
