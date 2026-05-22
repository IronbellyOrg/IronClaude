# TASKLIST INDEX -- IronClaude Real-Eval Harness

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | IronClaude Real-Eval Harness |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-05-18 |
| TASKLIST_ROOT | `.dev/releases/current/cliEval/` |
| Total Phases | 6 |
| Total Tasks | 143 (117 regular + 1 clarification embedded in regular count + 26 checkpoints) |
| Total Deliverables | 143 (117 regular D-#### + 26 checkpoint D-CP##) |
| Complexity Class | HIGH |
| Primary Persona | architect |
| Consulting Personas | security, backend, qa, devops |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `TASKLIST_ROOT/tasklist-index.md` |
| Phase 1 Tasklist | `TASKLIST_ROOT/phase-1-tasklist.md` |
| Phase 2 Tasklist | `TASKLIST_ROOT/phase-2-tasklist.md` |
| Phase 3 Tasklist | `TASKLIST_ROOT/phase-3-tasklist.md` |
| Phase 4 Tasklist | `TASKLIST_ROOT/phase-4-tasklist.md` |
| Phase 5 Tasklist | `TASKLIST_ROOT/phase-5-tasklist.md` |
| Phase 6 Tasklist | `TASKLIST_ROOT/phase-6-tasklist.md` |
| Execution Log | `TASKLIST_ROOT/execution-log.md` |
| Checkpoint Reports | `TASKLIST_ROOT/checkpoints/` |
| Evidence Directory | `TASKLIST_ROOT/evidence/` |
| Artifacts Directory | `TASKLIST_ROOT/artifacts/` |
| Validation Reports | `TASKLIST_ROOT/validation/` |
| Feedback Log | `TASKLIST_ROOT/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Foundation Config Schema DSL Security | T01.01-T01.27 | STRICT: 7, STANDARD: 13, EXEMPT: 2, LIGHT: 5 |
| 2 | phase-2-tasklist.md | Isolation Process Vendored Ptytest | T02.01-T02.27 | STRICT: 9, STANDARD: 10, EXEMPT: 3, LIGHT: 5 |
| 3 | phase-3-tasklist.md | Execution Engine and Reporter | T03.01-T03.23 | STRICT: 0, STANDARD: 19, EXEMPT: 0, LIGHT: 4 |
| 4 | phase-4-tasklist.md | Expect Primitives and CLI Surface | T04.01-T04.22 | STRICT: 0, STANDARD: 16, EXEMPT: 2, LIGHT: 4 |
| 5 | phase-5-tasklist.md | Eval Bodies Coverage Gate Rollout | T05.01-T05.28 | STRICT: 1, STANDARD: 21, EXEMPT: 1, LIGHT: 5 |
| 6 | phase-6-tasklist.md | Docs ADRs Hardening Sync Platform | T06.01-T06.16 | STRICT: 1, STANDARD: 2, EXEMPT: 10, LIGHT: 3 |

## Source Snapshot

- Roadmap defines 6 sequential milestones (M1 Foundation, M2 Isolation, M3 Execution, M4 Primitives/CLI, M5 Evals/Coverage, M6 Hardening) with strict dependency chain M1 -> M2 -> M3 -> M4 -> M5 -> M6.
- Complexity HIGH (0.72) driven by PTY/subprocess orchestration, security-critical path-containment, vendored ptytest ownership, strict N'-vs-K reporter contract, and three-tier capability gating.
- 10 open questions (OQ-1 .. OQ-10) gate milestone exits; OQ-1/OQ-2/OQ-7/OQ-8 must close before M1 exit, OQ-4/OQ-5 before M2 entry/exit, OQ-10 may resolve empirically in M3/M5, OQ-9 in M6.
- 15 risks registered (R1-R15) with R1 (claude TTY drift), R7 (real-HOME write), R11 (N'-vs-K reporter), R13 (coverage gate false negatives), R9 (PR scope creep) marked HIGH impact.
- Security-critical components (FR-SCH2 eval_id regex, FR-ISO2 path containment, NFR-SEC2/3 defense-in-depth, AC12 scratch-root allowlist) must land before any filesystem write path.
- 12 architectural decisions recorded including subprocess driving (real claude via PTY), parallelism (ThreadPoolExecutor + as_completed), isolation strategy (extend IsolationLayers), reporter contract (len(outcomes)==counts.expanded_n_prime mismatch exits 2), validation order (schema+ID before any FS op).

## Deterministic Rules Applied

- Phase bucketing from explicit `## M<n>` milestone headings in roadmap; renumbered to Phase 1-6 with no gaps.
- Roadmap items R-001 .. R-116 assigned in appearance order from numbered milestone tables.
- Task IDs `T<PP>.<TT>` zero-padded two digits; tasks emitted in roadmap appearance order within each phase.
- Mid-phase checkpoint after every 5 regular tasks (numbered task form per Section 4.8); end-of-phase checkpoint as last task in each phase.
- Checkpoint deliverable IDs use `D-CP<PP>` (end) and `D-CP<PP>-MID-T<start>-T<end>` (range) to avoid collision with regular `D-####` sequence.
- Effort and Risk computed per Section 5.2 keyword/length mappings; Tier per Section 5.3 priority `STRICT > EXEMPT > LIGHT > STANDARD`.
- Critical Path Override applied to tasks touching `auth/`, `security/`, `crypto/`, `models/`, `migrations/` per Section 4.11.
- Verification routing per tier: STRICT = quality-engineer sub-agent, STANDARD = direct test, LIGHT = sanity check, EXEMPT = skip.
- Clarification task inserted as T05.01 for OQ-2 (E3-E15 eval body content) per Section 4.6.
- MCP requirements per tier (Section 5.5); STRICT requires Sequential+Serena, STANDARD prefers Sequential+Context7.
- Multi-file output: `tasklist-index.md` + 6 phase files; phase files contain only tasks; index holds registries, traceability, and templates.
- Deliverable registry assigns D-#### in global task order, one deliverable per task default with concrete intended artifact paths under `TASKLIST_ROOT/artifacts/D-####/`.

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | 1 | COMP-005 EvalConfig dataclass: create dataclass holding paths, defaults, allowed_scratch_roots |
| R-002 | 1 | DM-011 Suite manifest YAML schema: define JSON schema for suite manifest structure |
| R-003 | 1 | DM-002 EvalSpec model: parsed manifest entry data model |
| R-004 | 1 | FR-SCH1 Suite manifest schema validation: load and validate YAML manifests against suite.schema.json |
| R-005 | 1 | FR-SCH2 Eval ID regex guard (security-critical): enforce regex on every id including parameterize-expanded IDs |
| R-006 | 1 | COMP-002 SuiteLoader: reads YAML manifests; orchestrates schema + regex + capability gates |
| R-007 | 1 | NFR-SEC1 Eval ID path-traversal prevention test set: negative-case tests proving ID regex blocks traversal |
| R-008 | 1 | DM-007 Capability dataclass: capability descriptor with check callable and failure_mode |
| R-009 | 1 | DM-008 CapabilityReport: per-capability status and blocked-evals listing |
| R-010 | 1 | COMP-009 CapabilityGates: check_all + which_or_skip + mcp_server_reachable |
| R-011 | 1 | FR-CLI4 eval doctor subcommand: verify harness preconditions and emit capability report |
| R-012 | 1 | COMP-010 ExpectDSL interface: define fluent and declarative assertion DSL interface consumed by manifests and runner |
| R-013 | 1 | DM-009 ExpectResult record: assertion outcome returned by ExpectCallable |
| R-014 | 1 | DM-005 ExpectFailure detail: assertion failure detail record |
| R-015 | 1 | AC3 Dependency boundary check: CI assertion that no new external Python deps land |
| R-016 | 1 | AC12 Allowed scratch roots enforcement: codify /tmp/eval-runs/, repo .dev/eval-runs/, or --output-dir allowlist |
| R-017 | 1 | AC11 Source-of-truth discipline gate: CI check that all changes live under src/superclaude/ |
| R-018 | 1 | FR-CLI2 eval list subcommand: enumerate suites from cli/eval/suites/*.yaml |
| R-019 | 1 | FR-CLI3 eval describe subcommand: print manifest content for a suite or single eval |
| R-020 | 1 | TEST-001 Schema and ID rejection tests: first-class test deliverable for schema errors and unsafe IDs |
| R-021 | 1 | OPS-001 Decision record closure: record decisions for ADR sign-off, PTY flag, JUnit, time offset, retry |
| R-022 | 1 | FR-G3 Additive CLI integration registration: register superclaude eval command family without breaking existing commands |
| R-023 | 2 | NFR-MAINT1 Vendored ptytest fork setup: fork ptytest under cli/eval/pty/ with LICENSE and PROVENANCE |
| R-024 | 2 | DOC-OQ4 NOTICE/LICENSE attribution for ptytest: M2 entry blocker per debate convergence |
| R-025 | 2 | AC10 ptytest fork SHA pin + drift policy: document fork SHA freeze with quarterly review cadence |
| R-026 | 2 | DM-006 HomeIsolation data record: frozen dataclass capturing isolation state |
| R-027 | 2 | COMP-012 IsolationLayers integration probe: verify existing 4-layer isolation API surface remains stable |
| R-028 | 2 | FR-ISO1 HomeIsolation extends IsolationLayers: add HOME override, CLAUDE_SESSION_ID stamp, optional time-offset |
| R-029 | 2 | FR-ISO2 Path containment guard (security-critical): re-check regex; verify is_relative_to; resolve symlinks |
| R-030 | 2 | NFR-SEC2 HOME containment defense-in-depth: layered guards on eval_id and scratch-root prefix |
| R-031 | 2 | NFR-SEC3 Hard guard against real ~/.claude/: setup() refuses HOME outside known scratch dirs |
| R-032 | 2 | COMP-006 HomeIsolation implementation: full component with setup/env/teardown/state_path |
| R-033 | 2 | NFR-ISO2 Atomic setup contract: try/except wrap; on exception after mkdtemp partial HOME preserved |
| R-034 | 2 | COMP-014 install_hooks reuse adapter: adapter calling existing install_hooks and deploying hooks.json |
| R-035 | 2 | NFR-PERF1 HOME setup performance baseline: measure per-eval HOME setup time and document budget |
| R-036 | 2 | COMP-007 PtyDriver wraps pexpect.spawn: expect_prompt_ready, inject_prompt, stdin/stdout, exit capture |
| R-037 | 2 | COMP-011 PtyStream ANSI/buffer layer: ANSI strip, line buffering, timeout handling |
| R-038 | 2 | COMP-013 ClaudeProcess reuse adapter: wrap existing process.py for spawn with no in-process SDK path |
| R-039 | 2 | R1-mit Claude version pin in eval doctor: pin supported claude version range and enforce in doctor |
| R-040 | 2 | TEST-002 Containment unit tests: allowed roots, rejected roots, loader-bypass defense at HomeIsolation |
| R-041 | 2 | TEST-003 Symlink attack tests: symlink resolution catches scratch and HOME escape attempts |
| R-042 | 2 | TEST-004 Capability gate tests: validate hard, skip, xfail classifications including --no-mcp behavior |
| R-043 | 2 | OPS-002 Scratch root policy enforcement: document and enforce allowed scratch roots across config and CLI |
| R-044 | 2 | R5-mit Quarterly ptytest drift review checklist: document review steps and target dates |
| R-045 | 3 | DM-001 EvalOutcome frozen dataclass: per-eval outcome record emitted by EvalRunner |
| R-046 | 3 | DM-003 EvalResult model: per-eval result record consumed by reporter |
| R-047 | 3 | DM-010 EvalContext runtime record: runtime context passed to ExpectCallable |
| R-048 | 3 | FR-LC1 EvalRunner lifecycle: build isolation deploy hooks spawn inject observe assert teardown |
| R-049 | 3 | COMP-004 EvalRunner implementation: full runner class wrapping FR-LC1 |
| R-050 | 3 | NFR-REL1 Signal handling + timeout enforcement: SIGINT/SIGTERM cancel; per-eval timeout kills and reaps |
| R-051 | 3 | NFR-REL2 Bounded retry policy: failed evals NOT retried by default; deterministic single-pass |
| R-052 | 3 | DM-004 RunSummary aggregate structure: aggregate run summary data model |
| R-053 | 3 | DM-012 summary.json schema: canonical machine-readable summary contract |
| R-054 | 3 | FR-RPT1 Aggregated Run Report: emit summary.md, summary.json, optional junit.xml |
| R-055 | 3 | COMP-008 Reporter / AggregatedRunReport: to_markdown/to_yaml/to_json/to_junit methods |
| R-056 | 3 | COMP-015 AggregatedPhaseReport pattern probe: pin shape reference for AggregatedRunReport |
| R-057 | 3 | COMP-003 RunOrchestrator: ThreadPoolExecutor + as_completed scheduler |
| R-058 | 3 | FR-G2 Parallel execution of 15 evals: run 15 evals in parallel with concurrency=8 default |
| R-059 | 3 | NFR-PERF2 Concurrency resource bounds verification: document RAM ceiling at --parallel 15 with free-RAM precheck |
| R-060 | 3 | NFR-PERF4 Disk budget enforcement (--max-disk-mb): orchestrator polls disk every 5s; halts on breach |
| R-061 | 3 | NFR-ISO1 No shared mutable state at concurrency: integration test asserting no shared state at max parallel |
| R-062 | 3 | NFR-PERF3 Suite runtime target tracking: track full-suite duration trend |
| R-063 | 3 | TEST-006 PTY lifecycle tests: real PTY spawn, prompt readiness, input injection, timeout handling, transcript |
| R-064 | 4 | FR-EXP1 Expect.* assertion DSL primitives: implement primitives Expect.file/jsonl/settings_json/exit_code/stderr/stdout/duration |
| R-065 | 4 | COMP-010.1 Expect.file primitive: assert file exists/content matches pattern |
| R-066 | 4 | COMP-010.2 Expect.jsonl primitive: assert JSONL entries match predicate |
| R-067 | 4 | COMP-010.3 Expect.settings_json primitive: assert ~/.claude/settings.json shape |
| R-068 | 4 | COMP-010.4 Expect.exit_code primitive: assert subprocess exit code |
| R-069 | 4 | COMP-010.5 Expect.stderr / stdout primitives: assert TTY transcripts match patterns |
| R-070 | 4 | COMP-010.6 Expect.duration primitive: assert eval duration within bound |
| R-071 | 4 | COMP-001 eval_group Click commands: top-level Click group exporting subcommands run/list/describe/doctor |
| R-072 | 4 | FR-CLI1 eval run subcommand: primary execution entry point with all flags wired and validated |
| R-073 | 4 | FR-G6 Single-command local runnability: uv run superclaude eval succeeds on clean dev machine |
| R-074 | 4 | FR-G4 Reproducible artifacts under .dev/eval-runs/<ISO>/<run-id>/: per-run artifact layout |
| R-075 | 4 | FR-G5 Falsifiable hook-matcher coverage gate (CLI entry): eval doctor --check-coverage and top-of-run gate |
| R-076 | 4 | DOC-OQ7 --junit flag wiring decision: decide and implement --junit flag or remove from spec |
| R-077 | 4 | DOC-OQ3 --no-pty exclusion set: enumerate evals excluded under --no-pty |
| R-078 | 4 | TEST-007 Reporter contract tests: N' vs K behavior, skipped inclusion, mismatch failure, JSON schema fidelity |
| R-079 | 4 | TEST-008 Exit-code semantics tests: process exit codes for clean, failing, harness-error, interrupted runs |
| R-080 | 4 | TEST-009 Artifact reproducibility tests: run directories, transcripts, logs, summaries written deterministically |
| R-081 | 4 | OPS-003 Artifact retention policy: define default deletion and keep-home behavior |
| R-082 | 5 | E1 Eval E1 -- auggie-first sticky lifecycle: sticky-lifecycle eval per design-spec section 5 |
| R-083 | 5 | E2.1 Eval -- matcher coverage mcp__auggie__: parameterize entry for mcp__auggie__* matcher via codebase-retrieval |
| R-084 | 5 | E2.2 Eval -- matcher coverage mcp__auggie-mcp__: parameterize entry for mcp__auggie-mcp__* via ask_question |
| R-085 | 5 | E2.3 Eval -- matcher coverage mcp__airis-mcp-gateway__: parameterize entry via auggie_search tool call |
| R-086 | 5 | E3 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-087 | 5 | E4 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-088 | 5 | E5 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-089 | 5 | E6 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-090 | 5 | E7 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-091 | 5 | E8 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-092 | 5 | E9 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-093 | 5 | E10 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-094 | 5 | E11 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-095 | 5 | E12 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-096 | 5 | E13 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-097 | 5 | E14 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-098 | 5 | E15 Eval body per OQ-2 resolution: content frozen post-OQ-2; deterministic AC |
| R-099 | 5 | SC2 Manifest schema covers all 15 evals: validate all E1-E15 IDs match regex and load via schema |
| R-100 | 5 | R3-mit MCP retry-once policy implementation: per-eval retry-once on MCP-specific failure modes |
| R-101 | 5 | TEST-013 Coverage gate tests: doctor and run top-of-run coverage gate against missing and complete matchers |
| R-102 | 5 | TEST-014 No-MCP skip behavior tests: verify MCP-dependent evals are SKIPPED with reason when --no-mcp is used |
| R-103 | 5 | MIG-002 Eval-batch rollout plan: split broad eval bodies into reviewable batches after harness contract lands |
| R-104 | 6 | SC1 ADR sign-offs D-5..D-8: RyanW signs off 4 original + 4 new ADRs in decisions.md |
| R-105 | 6 | DOC-OQ9 macOS support roadmap entry: record macOS timeline in decisions.md |
| R-106 | 6 | DOC-OQ8 Time-offset mechanism contract: document how Claude Code consumes CLAUDE_FAKE_TIME_OFFSET (or remove) |
| R-107 | 6 | DOC-OQ6 Suite naming convention beyond real.yaml: document suite filename rules; record quick.yaml plan |
| R-108 | 6 | AC2 CI integration deferral note: record deferral and follow-up trigger in decisions.md |
| R-109 | 6 | AC1 Linux-only declaration: record AC1 in decisions.md and README |
| R-110 | 6 | SC4 Effort estimate acknowledgment: RyanW signs off LOC estimate ~1,340 harness + ~3,000-4,500 eval bodies |
| R-111 | 6 | SC5 Open-question list fully resolved: all 10 OQ-xxx items recorded as resolved in decisions.md |
| R-112 | 6 | SC3 Zero-new-deps verification: verify pyproject.toml has no new external deps beyond pexpect vendored |
| R-113 | 6 | OPS-004 Validation command set: define the validation command sequence using UV and make targets |
| R-114 | 6 | OPS-005 Release checklist: assemble release evidence for doctor, sync, tests, artifact contracts |
| R-115 | 6 | MIG-001 Source sync migration: sync eval CLI sources from src/superclaude/ into .claude/ dev copies |
| R-116 | 6 | MIG-003 Platform follow-up plan: record macOS and future CI support as follow-up scope outside v1 |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | EvalConfig frozen dataclass module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0001/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0002 | T01.02 | R-002 | suite.schema.json JSON schema file | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0002/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0003 | T01.03 | R-003 | EvalSpec dataclass model | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0003/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0004 | T01.04 | R-004 | jsonschema-driven manifest validator | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0004/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0005 | T01.05 | R-005 | Eval ID regex guard module (InvalidEvalId) | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0005/spec.md`,`notes.md`,`evidence.md` | M | High |
| D-CP01-MID-T01-T05 | T01.06 | R-001..R-005 | Phase 1 mid-checkpoint report (T01-T05) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md` | XS | Low |
| D-0006 | T01.07 | R-006 | SuiteLoader implementation module | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0006/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0007 | T01.08 | R-007 | Path-traversal negative test suite | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0007/spec.md`,`notes.md`,`evidence.md` | M | High |
| D-0008 | T01.09 | R-008 | Capability frozen dataclass | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0008/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0009 | T01.10 | R-009 | CapabilityReport dataclass | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0009/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0010 | T01.11 | R-010 | CapabilityGates implementation | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0010/spec.md`,`notes.md`,`evidence.md` | L | Low |
| D-CP01-MID-T07-T11 | T01.12 | R-006..R-010 | Phase 1 mid-checkpoint report (T07-T11) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P01-T07-T11.md` | XS | Low |
| D-0011 | T01.13 | R-011 | eval doctor subcommand module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0011/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0012 | T01.14 | R-012 | cli/eval/expect.py DSL interface module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0012/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0013 | T01.15 | R-013 | ExpectResult record dataclass | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0013/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0014 | T01.16 | R-014 | ExpectFailure record dataclass | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0014/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0015 | T01.17 | R-015 | CI dependency-boundary assertion | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0015/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP01-MID-T13-T17 | T01.18 | R-011..R-015 | Phase 1 mid-checkpoint report (T13-T17) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P01-T13-T17.md` | XS | Low |
| D-0016 | T01.19 | R-016 | EvalConfig.allowed_scratch_roots allowlist | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0016/spec.md`,`notes.md`,`evidence.md` | M | High |
| D-0017 | T01.20 | R-017 | make verify-sync gate + pre-commit hook | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0017/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0018 | T01.21 | R-018 | eval list subcommand | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0018/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0019 | T01.22 | R-019 | eval describe subcommand | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0019/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0020 | T01.23 | R-020 | schema/ID rejection pytest module | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0020/spec.md`,`notes.md`,`evidence.md` | M | High |
| D-CP01-MID-T19-T23 | T01.24 | R-016..R-020 | Phase 1 mid-checkpoint report (T19-T23) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P01-T19-T23.md` | XS | Low |
| D-0021 | T01.25 | R-021 | decisions.md ADR sign-off updates | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0021/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0022 | T01.26 | R-022 | superclaude eval Click group registration | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0022/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-CP01 | T01.27 | R-001..R-022 | Phase 1 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P01-END.md` | XS | Low |
| D-0023 | T02.01 | R-023 | Vendored ptytest sources under cli/eval/pty/ | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0023/spec.md`,`notes.md`,`evidence.md` | M | Medium |
| D-0024 | T02.02 | R-024 | NOTICE file at repo root for ptytest LICENSE | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0024/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0025 | T02.03 | R-025 | PROVENANCE.md fork SHA + drift policy entry | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0025/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0026 | T02.04 | R-026 | HomeIsolation frozen dataclass | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0026/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0027 | T02.05 | R-027 | IsolationLayers integration probe test | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0027/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP02-MID-T01-T05 | T02.06 | R-023..R-027 | Phase 2 mid-checkpoint report (T01-T05) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md` | XS | Low |
| D-0028 | T02.07 | R-028 | HomeIsolation.setup/env/teardown extension methods | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0028/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0029 | T02.08 | R-029 | Path containment guard module (HomeContainmentViolation) | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0029/spec.md`,`notes.md`,`evidence.md` | L | High |
| D-0030 | T02.09 | R-030 | Defense-in-depth containment tests | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0030/spec.md`,`notes.md`,`evidence.md` | M | High |
| D-0031 | T02.10 | R-031 | Hard-guard real ~/.claude/ rejection tests | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0031/spec.md`,`notes.md`,`evidence.md` | M | High |
| D-0032 | T02.11 | R-032 | COMP-006 HomeIsolation implementation module | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0032/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-CP02-MID-T07-T11 | T02.12 | R-028..R-032 | Phase 2 mid-checkpoint report (T07-T11) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P02-T07-T11.md` | XS | Low |
| D-0033 | T02.13 | R-033 | Atomic setup try/except wrapper | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0033/spec.md`,`notes.md`,`evidence.md` | M | Medium |
| D-0034 | T02.14 | R-034 | install_hooks reuse adapter module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0034/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0035 | T02.15 | R-035 | NFR-PERF1 HOME setup benchmark report | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0035/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0036 | T02.16 | R-036 | PtyDriver implementation wrapping pexpect.spawn | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0036/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0037 | T02.17 | R-037 | PtyStream ANSI/buffer layer | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0037/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-CP02-MID-T13-T17 | T02.18 | R-033..R-037 | Phase 2 mid-checkpoint report (T13-T17) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P02-T13-T17.md` | XS | Low |
| D-0038 | T02.19 | R-038 | ClaudeProcess reuse adapter (no in-process SDK) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0038/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0039 | T02.20 | R-039 | Claude version pin in eval doctor | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0039/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0040 | T02.21 | R-040 | TEST-002 containment unit tests | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0040/spec.md`,`notes.md`,`evidence.md` | M | High |
| D-0041 | T02.22 | R-041 | TEST-003 symlink attack tests | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0041/spec.md`,`notes.md`,`evidence.md` | M | High |
| D-0042 | T02.23 | R-042 | TEST-004 capability gate tests | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0042/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-CP02-MID-T19-T23 | T02.24 | R-038..R-042 | Phase 2 mid-checkpoint report (T19-T23) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P02-T19-T23.md` | XS | Low |
| D-0043 | T02.25 | R-043 | Scratch root policy enforcement doc + code | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0043/spec.md`,`notes.md`,`evidence.md` | S | Medium |
| D-0044 | T02.26 | R-044 | Quarterly ptytest drift CHECKLIST.md | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0044/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP02 | T02.27 | R-023..R-044 | Phase 2 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P02-END.md` | XS | Low |
| D-0045 | T03.01 | R-045 | EvalOutcome frozen dataclass | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0045/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0046 | T03.02 | R-046 | EvalResult dataclass | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0046/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0047 | T03.03 | R-047 | EvalContext runtime record | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0047/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0048 | T03.04 | R-048 | FR-LC1 EvalRunner lifecycle spec + impl | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0048/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0049 | T03.05 | R-049 | COMP-004 EvalRunner class | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0049/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-CP03-MID-T01-T05 | T03.06 | R-045..R-049 | Phase 3 mid-checkpoint report (T01-T05) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P03-T01-T05.md` | XS | Low |
| D-0050 | T03.07 | R-050 | Signal handling + timeout enforcement module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0050/spec.md`,`notes.md`,`evidence.md` | M | Medium |
| D-0051 | T03.08 | R-051 | Bounded retry policy decision + impl | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0051/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0052 | T03.09 | R-052 | RunSummary aggregate dataclass | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0052/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0053 | T03.10 | R-053 | summary.json schema definition | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0053/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0054 | T03.11 | R-054 | FR-RPT1 aggregated run report writer | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0054/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-CP03-MID-T07-T11 | T03.12 | R-050..R-054 | Phase 3 mid-checkpoint report (T07-T11) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P03-T07-T11.md` | XS | Low |
| D-0055 | T03.13 | R-055 | COMP-008 Reporter to_* emitter methods | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0055/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0056 | T03.14 | R-056 | AggregatedPhaseReport shape probe test | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0056/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0057 | T03.15 | R-057 | RunOrchestrator ThreadPoolExecutor module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0057/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0058 | T03.16 | R-058 | FR-G2 parallel-15 integration test | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0058/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0059 | T03.17 | R-059 | NFR-PERF2 resource bounds benchmark | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0059/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP03-MID-T13-T17 | T03.18 | R-055..R-059 | Phase 3 mid-checkpoint report (T13-T17) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P03-T13-T17.md` | XS | Low |
| D-0060 | T03.19 | R-060 | NFR-PERF4 disk budget poller (--max-disk-mb) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0060/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0061 | T03.20 | R-061 | NFR-ISO1 shared-state integration test | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0061/spec.md`,`notes.md`,`evidence.md` | M | Medium |
| D-0062 | T03.21 | R-062 | Suite runtime tracking artifact | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0062/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0063 | T03.22 | R-063 | TEST-006 PTY lifecycle integration test | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0063/spec.md`,`notes.md`,`evidence.md` | L | Low |
| D-CP03 | T03.23 | R-045..R-063 | Phase 3 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P03-END.md` | XS | Low |
| D-0064 | T04.01 | R-064 | FR-EXP1 Expect.* primitive package | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0064/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0065 | T04.02 | R-065 | Expect.file primitive impl + tests | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0065/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0066 | T04.03 | R-066 | Expect.jsonl primitive impl + tests | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0066/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0067 | T04.04 | R-067 | Expect.settings_json primitive | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0067/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0068 | T04.05 | R-068 | Expect.exit_code primitive | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0068/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP04-MID-T01-T05 | T04.06 | R-064..R-068 | Phase 4 mid-checkpoint report (T01-T05) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md` | XS | Low |
| D-0069 | T04.07 | R-069 | Expect.stderr / Expect.stdout primitives | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0069/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0070 | T04.08 | R-070 | Expect.duration primitive | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0070/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0071 | T04.09 | R-071 | eval_group Click commands top-level | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0071/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0072 | T04.10 | R-072 | eval run subcommand with all flags wired | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0072/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0073 | T04.11 | R-073 | Single-command runnability smoke test | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0073/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-CP04-MID-T07-T11 | T04.12 | R-069..R-073 | Phase 4 mid-checkpoint report (T07-T11) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P04-T07-T11.md` | XS | Low |
| D-0074 | T04.13 | R-074 | .dev/eval-runs/<ISO>/<run-id>/ layout writer | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0074/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0075 | T04.14 | R-075 | FR-G5 coverage gate CLI entry | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0075/spec.md`,`notes.md`,`evidence.md` | L | Medium |
| D-0076 | T04.15 | R-076 | DOC-OQ7 --junit decision recorded in decisions.md | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0076/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0077 | T04.16 | R-077 | DOC-OQ3 --no-pty exclusion set in real.yaml | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0077/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0078 | T04.17 | R-078 | TEST-007 reporter contract pytest module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0078/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-CP04-MID-T13-T17 | T04.18 | R-074..R-078 | Phase 4 mid-checkpoint report (T13-T17) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P04-T13-T17.md` | XS | Low |
| D-0079 | T04.19 | R-079 | TEST-008 exit-code semantics pytest module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0079/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0080 | T04.20 | R-080 | TEST-009 artifact reproducibility tests | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0080/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0081 | T04.21 | R-081 | OPS-003 artifact retention policy doc | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0081/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP04 | T04.22 | R-064..R-081 | Phase 4 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P04-END.md` | XS | Low |
| D-0082 | T05.01 | R-086..R-098 | OQ-2 resolution decision artifact for E3-E15 bodies | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0082/spec.md`,`notes.md`,`evidence.md` | XS | Low |
| D-0083 | T05.02 | R-082 | E1 auggie-first sticky lifecycle eval YAML + body | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0083/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0084 | T05.03 | R-083 | E2.1 mcp__auggie__ matcher coverage eval | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0084/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0085 | T05.04 | R-084 | E2.2 mcp__auggie-mcp__ matcher coverage eval | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0085/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0086 | T05.05 | R-085 | E2.3 mcp__airis-mcp-gateway__ matcher coverage eval | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0086/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-CP05-MID-T01-T05 | T05.06 | R-082..R-085 | Phase 5 mid-checkpoint report (T01-T05) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P05-T01-T05.md` | XS | Low |
| D-0087 | T05.07 | R-086 | E3 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0087/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0088 | T05.08 | R-087 | E4 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0088/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0089 | T05.09 | R-088 | E5 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0089/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0090 | T05.10 | R-089 | E6 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0090/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0091 | T05.11 | R-090 | E7 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0091/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-CP05-MID-T07-T11 | T05.12 | R-086..R-090 | Phase 5 mid-checkpoint report (T07-T11) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P05-T07-T11.md` | XS | Low |
| D-0092 | T05.13 | R-091 | E8 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0092/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0093 | T05.14 | R-092 | E9 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0093/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0094 | T05.15 | R-093 | E10 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0094/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0095 | T05.16 | R-094 | E11 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0095/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0096 | T05.17 | R-095 | E12 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0096/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-CP05-MID-T13-T17 | T05.18 | R-091..R-095 | Phase 5 mid-checkpoint report (T13-T17) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P05-T13-T17.md` | XS | Low |
| D-0097 | T05.19 | R-096 | E13 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0097/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0098 | T05.20 | R-097 | E14 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0098/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0099 | T05.21 | R-098 | E15 eval body YAML + body (post-OQ-2) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0099/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0100 | T05.22 | R-099 | SC2 schema-covers-15-evals verification artifact | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0100/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0101 | T05.23 | R-100 | R3-mit MCP retry-once policy module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0101/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-CP05-MID-T19-T23 | T05.24 | R-096..R-100 | Phase 5 mid-checkpoint report (T19-T23) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P05-T19-T23.md` | XS | Low |
| D-0102 | T05.25 | R-101 | TEST-013 coverage gate pytest module | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0102/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0103 | T05.26 | R-102 | TEST-014 no-MCP skip behavior tests | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0103/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0104 | T05.27 | R-103 | MIG-002 eval-batch rollout plan doc | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0104/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP05 | T05.28 | R-082..R-103 | Phase 5 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P05-END.md` | XS | Low |
| D-0105 | T06.01 | R-104 | SC1 ADR sign-offs in decisions.md | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0105/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0106 | T06.02 | R-105 | DOC-OQ9 macOS roadmap entry | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0106/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0107 | T06.03 | R-106 | DOC-OQ8 time-offset contract decision | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0107/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0108 | T06.04 | R-107 | DOC-OQ6 suites/README.md naming convention | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0108/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0109 | T06.05 | R-108 | AC2 CI deferral note in decisions.md | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0109/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP06-MID-T01-T05 | T06.06 | R-104..R-108 | Phase 6 mid-checkpoint report (T01-T05) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P06-T01-T05.md` | XS | Low |
| D-0110 | T06.07 | R-109 | AC1 Linux-only declaration in README + decisions | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0110/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0111 | T06.08 | R-110 | SC4 effort estimate sign-off entry | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0111/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0112 | T06.09 | R-111 | SC5 OQ-1..OQ-10 resolution ledger | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0112/spec.md`,`notes.md`,`evidence.md` | M | Low |
| D-0113 | T06.10 | R-112 | SC3 zero-new-deps verification artifact | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0113/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0114 | T06.11 | R-113 | OPS-004 validation command sequence doc | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0114/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP06-MID-T07-T11 | T06.12 | R-109..R-113 | Phase 6 mid-checkpoint report (T07-T11) | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P06-T07-T11.md` | XS | Low |
| D-0115 | T06.13 | R-114 | OPS-005 release checklist artifact | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0115/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-0116 | T06.14 | R-115 | MIG-001 src/.claude sync evidence | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0116/spec.md`,`notes.md`,`evidence.md` | S | Medium |
| D-0117 | T06.15 | R-116 | MIG-003 platform follow-up plan entry | EXEMPT | Skip verification | `TASKLIST_ROOT/artifacts/D-0117/spec.md`,`notes.md`,`evidence.md` | S | Low |
| D-CP06 | T06.16 | R-104..R-116 | Phase 6 end-of-phase checkpoint report | LIGHT | Quick sanity check | `TASKLIST_ROOT/checkpoints/CP-P06-END.md` | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0001/` |
| R-002 | T01.02 | D-0002 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0002/` |
| R-003 | T01.03 | D-0003 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0003/` |
| R-004 | T01.04 | D-0004 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0004/` |
| R-005 | T01.05 | D-0005 | STRICT | 95% | `TASKLIST_ROOT/artifacts/D-0005/` |
| R-006 | T01.07 | D-0006 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0006/` |
| R-007 | T01.08 | D-0007 | STRICT | 95% | `TASKLIST_ROOT/artifacts/D-0007/` |
| R-008 | T01.09 | D-0008 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0008/` |
| R-009 | T01.10 | D-0009 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0009/` |
| R-010 | T01.11 | D-0010 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0010/` |
| R-011 | T01.13 | D-0011 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0011/` |
| R-012 | T01.14 | D-0012 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0012/` |
| R-013 | T01.15 | D-0013 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0013/` |
| R-014 | T01.16 | D-0014 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0014/` |
| R-015 | T01.17 | D-0015 | EXEMPT | 90% | `TASKLIST_ROOT/artifacts/D-0015/` |
| R-016 | T01.19 | D-0016 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0016/` |
| R-017 | T01.20 | D-0017 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0017/` |
| R-018 | T01.21 | D-0018 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0018/` |
| R-019 | T01.22 | D-0019 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0019/` |
| R-020 | T01.23 | D-0020 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0020/` |
| R-021 | T01.25 | D-0021 | EXEMPT | 90% | `TASKLIST_ROOT/artifacts/D-0021/` |
| R-022 | T01.26 | D-0022 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0022/` |
| R-023 | T02.01 | D-0023 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0023/` |
| R-024 | T02.02 | D-0024 | EXEMPT | 90% | `TASKLIST_ROOT/artifacts/D-0024/` |
| R-025 | T02.03 | D-0025 | EXEMPT | 90% | `TASKLIST_ROOT/artifacts/D-0025/` |
| R-026 | T02.04 | D-0026 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0026/` |
| R-027 | T02.05 | D-0027 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0027/` |
| R-028 | T02.07 | D-0028 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0028/` |
| R-029 | T02.08 | D-0029 | STRICT | 95% | `TASKLIST_ROOT/artifacts/D-0029/` |
| R-030 | T02.09 | D-0030 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0030/` |
| R-031 | T02.10 | D-0031 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0031/` |
| R-032 | T02.11 | D-0032 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0032/` |
| R-033 | T02.13 | D-0033 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0033/` |
| R-034 | T02.14 | D-0034 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0034/` |
| R-035 | T02.15 | D-0035 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0035/` |
| R-036 | T02.16 | D-0036 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0036/` |
| R-037 | T02.17 | D-0037 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0037/` |
| R-038 | T02.19 | D-0038 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0038/` |
| R-039 | T02.20 | D-0039 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0039/` |
| R-040 | T02.21 | D-0040 | STRICT | 95% | `TASKLIST_ROOT/artifacts/D-0040/` |
| R-041 | T02.22 | D-0041 | STRICT | 95% | `TASKLIST_ROOT/artifacts/D-0041/` |
| R-042 | T02.23 | D-0042 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0042/` |
| R-043 | T02.25 | D-0043 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0043/` |
| R-044 | T02.26 | D-0044 | EXEMPT | 90% | `TASKLIST_ROOT/artifacts/D-0044/` |
| R-045 | T03.01 | D-0045 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0045/` |
| R-046 | T03.02 | D-0046 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0046/` |
| R-047 | T03.03 | D-0047 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0047/` |
| R-048 | T03.04 | D-0048 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0048/` |
| R-049 | T03.05 | D-0049 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0049/` |
| R-050 | T03.07 | D-0050 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0050/` |
| R-051 | T03.08 | D-0051 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0051/` |
| R-052 | T03.09 | D-0052 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0052/` |
| R-053 | T03.10 | D-0053 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0053/` |
| R-054 | T03.11 | D-0054 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0054/` |
| R-055 | T03.13 | D-0055 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0055/` |
| R-056 | T03.14 | D-0056 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0056/` |
| R-057 | T03.15 | D-0057 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0057/` |
| R-058 | T03.16 | D-0058 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0058/` |
| R-059 | T03.17 | D-0059 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0059/` |
| R-060 | T03.19 | D-0060 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0060/` |
| R-061 | T03.20 | D-0061 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0061/` |
| R-062 | T03.21 | D-0062 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0062/` |
| R-063 | T03.22 | D-0063 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0063/` |
| R-064 | T04.01 | D-0064 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0064/` |
| R-065 | T04.02 | D-0065 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0065/` |
| R-066 | T04.03 | D-0066 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0066/` |
| R-067 | T04.04 | D-0067 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0067/` |
| R-068 | T04.05 | D-0068 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0068/` |
| R-069 | T04.07 | D-0069 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0069/` |
| R-070 | T04.08 | D-0070 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0070/` |
| R-071 | T04.09 | D-0071 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0071/` |
| R-072 | T04.10 | D-0072 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0072/` |
| R-073 | T04.11 | D-0073 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0073/` |
| R-074 | T04.13 | D-0074 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0074/` |
| R-075 | T04.14 | D-0075 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0075/` |
| R-076 | T04.15 | D-0076 | EXEMPT | 90% | `TASKLIST_ROOT/artifacts/D-0076/` |
| R-077 | T04.16 | D-0077 | EXEMPT | 90% | `TASKLIST_ROOT/artifacts/D-0077/` |
| R-078 | T04.17 | D-0078 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0078/` |
| R-079 | T04.19 | D-0079 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0079/` |
| R-080 | T04.20 | D-0080 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0080/` |
| R-081 | T04.21 | D-0081 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0081/` |
| R-082 | T05.02 | D-0083 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0083/` |
| R-083 | T05.03 | D-0084 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0084/` |
| R-084 | T05.04 | D-0085 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0085/` |
| R-085 | T05.05 | D-0086 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0086/` |
| R-086 | T05.07 | D-0087 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0087/` |
| R-087 | T05.08 | D-0088 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0088/` |
| R-088 | T05.09 | D-0089 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0089/` |
| R-089 | T05.10 | D-0090 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0090/` |
| R-090 | T05.11 | D-0091 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0091/` |
| R-091 | T05.13 | D-0092 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0092/` |
| R-092 | T05.14 | D-0093 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0093/` |
| R-093 | T05.15 | D-0094 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0094/` |
| R-094 | T05.16 | D-0095 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0095/` |
| R-095 | T05.17 | D-0096 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0096/` |
| R-096 | T05.19 | D-0097 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0097/` |
| R-097 | T05.20 | D-0098 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0098/` |
| R-098 | T05.21 | D-0099 | STANDARD | 75% | `TASKLIST_ROOT/artifacts/D-0099/` |
| R-099 | T05.22 | D-0100 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0100/` |
| R-100 | T05.23 | D-0101 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0101/` |
| R-101 | T05.25 | D-0102 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0102/` |
| R-102 | T05.26 | D-0103 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0103/` |
| R-103 | T05.27 | D-0104 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0104/` |
| R-104 | T06.01 | D-0105 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0105/` |
| R-105 | T06.02 | D-0106 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0106/` |
| R-106 | T06.03 | D-0107 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0107/` |
| R-107 | T06.04 | D-0108 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0108/` |
| R-108 | T06.05 | D-0109 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0109/` |
| R-109 | T06.07 | D-0110 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0110/` |
| R-110 | T06.08 | D-0111 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0111/` |
| R-111 | T06.09 | D-0112 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0112/` |
| R-112 | T06.10 | D-0113 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0113/` |
| R-113 | T06.11 | D-0114 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0114/` |
| R-114 | T06.13 | D-0115 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0115/` |
| R-115 | T06.14 | D-0116 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0116/` |
| R-116 | T06.15 | D-0117 | EXEMPT | 95% | `TASKLIST_ROOT/artifacts/D-0117/` |
| (OQ-2 clarification) | T05.01 | D-0082 | EXEMPT | 90% | `TASKLIST_ROOT/artifacts/D-0082/` |

## Execution Log Template

**Intended Path:** `TASKLIST_ROOT/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| 2026-MM-DDTHH:MM:SSZ | T01.01 | STANDARD | D-0001 | Implemented EvalConfig dataclass | uv run pytest tests/cli/eval/test_config.py | TBD | `TASKLIST_ROOT/evidence/T01.01/` |

## Checkpoint Report Template

For each checkpoint task, execution must produce one report using this template.

**Template:**
- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status`
  - `Overall: Pass | Fail | TBD`
- `## Verification Results` (exactly 3 bullets; align to checkpoint Verification bullets)
- `## Exit Criteria Assessment` (exactly 3 bullets; align to checkpoint Exit Criteria bullets)
- `## Issues & Follow-ups`
  - List blocking issues; reference `T<PP>.<TT>` and `D-####`
- `## Evidence`
  - Bullet list of intended evidence paths under `TASKLIST_ROOT/evidence/`

## Feedback Collection Template

**Intended Path:** `TASKLIST_ROOT/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
| T01.05 | STRICT | | | | | |

## Generation Notes

- TASKLIST_ROOT auto-derived from path substring `.dev/releases/current/cliEval/` in the roadmap file path (Section 3.1, step 1).
- Phase buckets derived from explicit `## M<n>:` milestone headings in roadmap (Section 4.2).
- One Clarification Task (T05.01) inserted before E3-E15 tasks per Section 4.6 (OQ-2 unresolved).
- All E3-E15 tasks tagged Confidence 75% (just above threshold) because the roadmap explicitly schedules OQ-2 resolution before M5 entry; T05.01 carries the clarification artifact.
- Tier classifications applied priority order STRICT > EXEMPT > LIGHT > STANDARD with critical-path override for tasks touching auth/, security/, crypto/, models/, migrations/ paths.
- Checkpoint deliverable IDs use D-CP<PP>(-MID-T<start>-T<end>) convention to avoid collision with D-#### sequence (Section 5.1, v3.7 Wave 4).
