---
spec_source: design-spec.compressed.md
generated: 2026-05-18T19:15:30Z
generator: requirements-extractor-agent
functional_requirements: 17
nonfunctional_requirements: 12
total_requirements: 29
complexity_score: 0.72
complexity_class: HIGH
domains_detected: [backend, cli, testing, security, devops, isolation, concurrency]
risks_identified: 9
dependencies_identified: 11
success_criteria_count: 5
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 115.0, started_at: "2026-05-18T19:15:27.461426+00:00", finished_at: "2026-05-18T19:17:22.475767+00:00"}
---

## Functional Requirements

### FR-G1: Real Claude Code Subprocess via PTY
Drive a real Claude Code subprocess through a PTY for each eval. No mocks, synthetic stubs, or in-process SDK clients.
- Source: §1 Goal 1
- Endpoint: subprocess invocation of `claude` binary
- Acceptance: PtyDriver spawns real `claude` binary; no in-process SDK shortcuts.

### FR-G2: Parallel Execution of 15 Evals
Run all 15 evals in parallel with default concurrency=8, max=15. Strict isolation: each eval owns its own HOME, session_id, and state/telemetry namespace.
- Source: §1 Goal 2, §12
- Acceptance: ThreadPoolExecutor with `max_workers=8`; clamped `[1,15]`.

### FR-G3: CLI Integration (Additive)
Plug cleanly into existing IronClaude CLI as `superclaude eval --suite real`. No breaking changes; ~60% scaffolding reused from `cli/sprint`, `cli/prd`, `cli/pipeline`.
- Source: §1 Goal 3, §10
- Endpoint: `superclaude eval [OPTIONS] COMMAND [ARGS]...`

### FR-G4: Reproducible Artifacts
Produce reproducible artifacts under `.dev/eval-runs/<ISO>/<run-id>/` — structured per-eval logs, aggregate report (Markdown + JSON), failure stack traces, captured TTY transcripts.
- Source: §1 Goal 4, §3, §9
- Path: `.dev/eval-runs/2026-05-18T18-30-12_run-abc123/`

### FR-G5: Falsifiable Hook-Matcher Coverage Gate
For every PostToolUse hook H with matcher pattern P in `~/.claude/settings.json`, an eval must exist that (a) issues a real MCP tool call matching P, (b) reads the per-eval `~/.claude/logs/<hook>.jsonl` telemetry, and (c) asserts H fired. The harness FAILS the run if any matcher P lacks a corresponding eval.
- Source: §1 Goal 5
- Endpoint: `eval doctor --check-coverage` and `eval run` top-of-run gate
- v1 coverage: `mcp__auggie__*`, `mcp__auggie-mcp__*`, `mcp__airis-mcp-gateway__*` via E1, E2.{1,2,3}

### FR-G6: Single-Command Local Runnability
Runnable locally with a single command: `uv run superclaude eval --suite real`.
- Source: §1 Goal 6

### FR-CLI1: `eval run` Subcommand
Primary execution entry point with flags: `--suite`, `--parallel`, `--eval`, `--no-mcp`, `--no-pty`, `--output-dir`, `--keep-home`, `--timeout-mult`, `--max-disk-mb`, `--json`, `--verbose`.
- Source: §4 Subcommands + Flags
- Endpoint: `superclaude eval run --suite SUITE`

### FR-CLI2: `eval list` Subcommand
Enumerate available suites from `cli/eval/suites/*.yaml`.
- Endpoint: `superclaude eval list`

### FR-CLI3: `eval describe` Subcommand
Print the manifest content for a suite or single eval.
- Endpoint: `superclaude eval describe --suite SUITE [--eval ID]`

### FR-CLI4: `eval doctor` Subcommand
Verify harness preconditions: claude binary on PATH, jq/make/git available, `~/.claude` exists, ptytest vendored, capability gate report, coverage check.
- Endpoint: `superclaude eval doctor`

### FR-SCH1: Suite Manifest Schema Validation
Load and validate YAML manifests (`suites/*.yaml`) using `jsonschema` against `suites/suite.schema.json`. Validation runs in `eval doctor` and at top of `eval run`.
- Source: §5

### FR-SCH2: Eval Identifier Validation (Security-Critical)
Every `id:` field — including parameterize-expanded IDs — MUST match regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. Loader REJECTS non-matching with `InvalidEvalId` and exits 2 BEFORE any filesystem operations. Template tokens inside `id:` rejected.
- Source: §5 Identifier validation

### FR-LC1: Per-Eval Lifecycle Sequence
EvalRunner executes per-eval lifecycle: build HomeIsolation → deploy hooks → spawn ClaudeProcess via PtyDriver → inject inputs → observe JSONL + state side-effects → apply Expect.* assertions → teardown HOME.
- Source: §6

### FR-ISO1: HomeIsolation Extension
HomeIsolation extends/composes `IsolationLayers` (sprint/executor.py:107-182) adding: HOME override, CLAUDE_SESSION_ID stamp, optional CLAUDE_FAKE_TIME_OFFSET. Per-eval HOMEs are sibling directories under `home_root`.
- Source: §7

### FR-ISO2: Path Containment Guard (Security-Critical)
Before any filesystem write, `HomeIsolation.setup()` MUST: (a) re-check eval_id regex, (b) compute resolved `home_path` and `scratch_root`, (c) verify `home_path.is_relative_to(scratch_root)`, (d) verify `scratch_root` matches allowed prefixes (`/tmp/eval-runs/`, `<repo_root>/.dev/eval-runs/`, or `--output-dir` resolved against `EvalConfig.allowed_scratch_roots`), (e) resolve symlinks under `home_path` after creation BEFORE deploying hooks. Raises `HomeContainmentViolation` on failure.
- Source: §7 invariant 5

### FR-EXP1: Expect.* Assertion DSL
Implement assertion DSL with primitives: `Expect.file`, `Expect.jsonl`, `Expect.settings_json`, `Expect.exit_code`, `Expect.stderr`, `Expect.stdout`, `Expect.duration`. Each returns a callable `(EvalContext) -> ExpectResult`. Support both declarative (YAML) and programmatic forms.
- Source: §8

### FR-RPT1: Aggregated Run Report
Produce `summary.md` (human), `summary.json` (machine), optional `junit.xml`. JSON `evals[]` length MUST equal N' (post-expansion, post-parameterize), NOT K (kept subset). Skipped evals included with `status: SKIPPED` + `skip_reason`. Reporter asserts `len(outcomes) == counts.expanded_n_prime`; mismatch raises `ReporterContractViolation` and run exits 2.
- Source: §9

## Non-Functional Requirements

### NFR-PERF1: Per-Eval HOME Setup Performance
Per-eval HOME setup (~135 file ops for 15 evals) acceptable at ~10ms per `cp`, totaling ~1.4s per eval. Reuse `install_hooks.py` optimizations.
- Source: §14 R2

### NFR-PERF2: Concurrency Resource Bounds
At `--parallel 8`, max 8 `claude` subprocesses (~150MB resident each). At `--parallel 15`, ~2.25GB free RAM required.
- Source: §12

### NFR-PERF3: Suite Runtime Target
Full suite duration target <10 min to avoid adoption friction. Provide `--eval <subset>` and follow-up `suites/quick.yaml`.
- Source: §14 R6

### NFR-PERF4: Disk Budget Enforcement
`--max-disk-mb` (default 1024) polled every 5s by orchestrator. On breach: in-flight evals complete, no new evals scheduled, exit 2 with `disk_budget_exceeded`. `0` disables.
- Source: §4, §14 R4

### NFR-SEC1: Eval ID Path-Traversal Prevention
ID regex validation prevents path traversal via interpolated `home_root / eval_id / home`. (See FR-SCH2.)
- Source: §5

### NFR-SEC2: HOME Containment Defense-in-Depth
HomeIsolation re-validates eval_id and enforces containment against allowed scratch roots. Symlink resolution after creation prevents `scratch dir is symlink to $HOME` attack.
- Source: §7 invariant 5, §14 R7

### NFR-SEC3: Hard Guard Against Real `~/.claude/` Use
`HomeIsolation.setup()` MUST refuse if HOME points outside a known eval-runs scratch dir.
- Source: §14 R7

### NFR-ISO1: No Shared Mutable State at Concurrency
At max concurrency: no shared HOME, no shared file handles (`auggie-first.jsonl`), no port collisions.
- Source: §12

### NFR-ISO2: Atomic Setup Contract
`HomeIsolation.setup()` wrapped in try/except; on exception after `mkdtemp` succeeds, partial HOME preserved (status ERRORED, `keep=True` forced), `setup_failed` artifact tag written. Distinguishes harness bugs from eval failures.
- Source: §7 invariant 6

### NFR-REL1: Signal Handling
SIGINT/SIGTERM cancels running evals, marks in-flight as INTERRUPTED, writes partial summary, exits 3. Per-eval timeout kills PtyDriver subprocess + reaps zombie; marks TIMEOUT.
- Source: §12

### NFR-REL2: Bounded Retry (No Infinite Retry)
Failed evals NOT retried by default. Deterministic single-pass. User re-runs subset with `--eval <failed-ids>`.
- Source: §12

### NFR-MAINT1: Vendored Dependency Discipline
Fork ptytest under `cli/eval/pty/`. Pin `pexpect>=4.9`. Retain upstream LICENSE; document changes in `PROVENANCE.md`. Quarterly upstream review.
- Source: §13, §14 R5

## Complexity Assessment

**complexity_score: 0.72 (HIGH)**

Scoring rationale:
- **Subprocess + TTY orchestration (+0.20):** Real PTY-driven Claude Code subprocesses with pexpect — platform-sensitive, fragile to upstream TTY changes (R1).
- **Concurrency model (+0.10):** ThreadPoolExecutor with up to 15 parallel real subprocesses; bounded resource (RAM, disk) management.
- **Security surface (+0.15):** Path-traversal guard (FR-SCH2, FR-ISO2), HOME containment (NFR-SEC2/3), symlink resolution — security-critical correctness paths.
- **Integration surface (+0.10):** Extends existing `IsolationLayers`, reuses `ClaudeProcess`, `install_hooks.py`, `AggregatedPhaseReport`. Multiple stable APIs depended upon.
- **Reporting contract (+0.07):** N' vs K dimensional invariant; status taxonomy (8 states); reporter contract violation as exit 2.
- **Vendored fork ownership (+0.05):** Fork-and-own ptytest; bus-factor risk mitigation.
- **Capability gating (+0.05):** Three-tier (HARD/SOFT-SKIP/SOFT-XFAIL) with MCP-server reachability checks.

LOC estimate: ~1,340 harness + ~3,000–4,500 eval bodies. Multi-phase rollout (5 phases) over 3.5 days harness + 1–2 weeks evals.

## Architectural Constraints

- **AC1:** Linux-only for v1 (TTY behavior platform-specific; macOS/Windows are follow-ups).
- **AC2:** No CI integration (deferred; local-only via `uv run superclaude eval`).
- **AC3:** No new external Python deps beyond `pexpect` (vendored) and `jsonschema` (transitive).
- **AC4:** Reuse `ClaudeProcess` from `cli/pipeline/process.py:24-150` for subprocess scaffolding.
- **AC5:** Extend (not replace) `IsolationLayers` at `cli/sprint/executor.py:107-182`.
- **AC6:** Use `ThreadPoolExecutor + as_completed` pattern from `cli/prd/executor.py:774-802` (NOT `execution/parallel.py`).
- **AC7:** Single-host only; no distributed mode.
- **AC8:** No async/await — blocking-thread-per-eval model.
- **AC9:** TTY-driven by design; observability via JSONL hook telemetry, not SDK interception.
- **AC10:** Vendored ptytest frozen at fork SHA; `PROVENANCE.md` documents resync procedure.
- **AC11:** Source-of-truth discipline: edits under `src/superclaude/`; `make sync-dev` before `make verify-sync`.
- **AC12:** Allowed scratch roots: `/tmp/eval-runs/`, `<repo_root>/.dev/eval-runs/`, or `--output-dir` allowlisted via `EvalConfig.allowed_scratch_roots`.

## Component Inventory

### Services / Modules / Classes

- **COMP-001 `eval_group`** (`cli/eval/commands.py`) — Click group exporting `run`, `list`, `describe`, `doctor` subcommands. Depends on: COMP-002, COMP-003, COMP-004, COMP-009. Source: §3, §4.
- **COMP-002 SuiteLoader** (`cli/eval/loader.py`) — Reads YAML manifests, validates schema via `jsonschema`, resolves capability gates, enforces eval_id regex. Depends on: COMP-005, COMP-010. Source: §3, §5.
- **COMP-003 RunOrchestrator** (`cli/eval/orchestrator.py`) — `ThreadPoolExecutor` + `as_completed` scheduler; per-eval timeout; disk-budget poller (5s); emits `EvalOutcome` per expanded spec. Depends on: COMP-004, COMP-008, DM-001. Source: §3, §12.
- **COMP-004 EvalRunner** (`cli/eval/runner.py`) — Per-eval lifecycle: build HomeIsolation → deploy hooks → spawn → inject inputs → observe → assert → teardown. Depends on: COMP-006, COMP-007, COMP-011. Source: §3, §6.
- **COMP-005 EvalConfig** (`cli/eval/config.py`) — Dataclass for paths, defaults, `allowed_scratch_roots`. Source: §3, §7.
- **COMP-006 HomeIsolation** (`cli/eval/isolation.py`) — Extends `IsolationLayers`; adds HOME override, session_id stamp, time offset, path containment guard. Methods: `setup()`, `env() -> dict[str,str]`, `teardown(keep)`, `state_path(suffix) -> Path`. Source: §3, §7.
- **COMP-007 PtyDriver** (`cli/eval/pty/driver.py`) — Wraps `pexpect.spawn`; methods include `expect_prompt_ready(timeout=)`, `inject_prompt(text)`, stdin write, stdout read, exit capture. Source: §3, §13.
- **COMP-008 Reporter / AggregatedRunReport** (`cli/eval/reporter.py`) — `to_markdown()`, `to_yaml()`, `to_json()`, `to_junit()`; asserts `len(outcomes) == counts.expanded_n_prime`. Source: §3, §9.
- **COMP-009 CapabilityGates** (`cli/eval/capability_gates.py`) — `check_all(skip_flags) -> CapabilityReport`; `which_or_skip`, `mcp_server_reachable`. Source: §3, §11.
- **COMP-010 ExpectDSL** (`cli/eval/expect.py`) — Fluent assertion DSL static methods returning typed Expect classes. Source: §3, §8.
- **COMP-011 PtyStream** (`cli/eval/pty/stream.py`) — ANSI strip, line buffering, timeout handling. Source: §3, §13.
- **COMP-012 IsolationLayers (reused)** (`cli/sprint/executor.py:107-182`) — Existing 4-layer isolation (cwd, git ceiling, plugin dir, settings dir). Source: §7, §10.
- **COMP-013 ClaudeProcess (reused)** (`cli/pipeline/process.py:24-150`) — Subprocess scaffolding for spawn+capture. Source: §10.
- **COMP-014 install_hooks (reused)** (`cli/install_hooks.py:install_hooks`) — Populates per-eval HOMEs with hooks. Source: §10.
- **COMP-015 AggregatedPhaseReport (pattern reference)** (`cli/sprint/executor.py:190-335`) — Shape reference for AggregatedRunReport. Source: §10.

### Data Models / DTOs

- **DM-001 EvalOutcome** (frozen dataclass) — fields: `eval_id: str`, `title: str`, `status: Literal["PASS","FAIL","ERRORED","TIMEOUT","INTERRUPTED","SKIPPED","XFAIL","XPASS"]`, `duration_sec: float`, `expects: list[ExpectResult]`, `skip_reason: str|None`, `skip_flag_triggered: str|None`, `artifacts: dict[str,str]`, `error_class: str|None`. Source: §9.
- **DM-002 EvalSpec** (`cli/eval/models.py`) — parsed manifest entry; includes id, title, category, requires, timeout_sec, isolation, inputs, expects, parameterize. Source: §3, §5.
- **DM-003 EvalResult** (`cli/eval/models.py`) — per-eval result emitted by runner. Source: §3.
- **DM-004 RunSummary** (`cli/eval/models.py`) — aggregate summary structure. Source: §3.
- **DM-005 ExpectFailure** (`cli/eval/models.py`) — assertion failure detail. Source: §3.
- **DM-006 HomeIsolation (frozen dataclass)** — fields: `eval_id: str`, `home_root: Path`, `session_id: str`, `time_offset_sec: int = 0`. Source: §7.
- **DM-007 Capability** (dataclass) — fields: `name: str`, `check: Callable[[],bool]`, `failure_mode: Literal["hard","skip","xfail"]`, `skip_flag: Optional[str]`, `description: str`. Source: §11.
- **DM-008 CapabilityReport** — per-capability status + blocked-evals listing. Source: §11.
- **DM-009 ExpectResult** — assertion outcome record returned by ExpectCallable. Source: §8, §9.
- **DM-010 EvalContext** — runtime context passed to ExpectCallable. Source: §8.
- **DM-011 Suite manifest YAML** — fields: `name`, `version`, `description`, `defaults`, `required_binaries`, `optional_capabilities`, `evals[]`. Source: §5.
- **DM-012 summary.json schema** — fields: `run_id`, `started_at`, `duration_sec`, `suite`, `manifest_version`, `parallel`, `counts.{manifest_n, expanded_n_prime, kept_k, skipped_s, kept_plus_skipped_equals_n_prime}`, `totals.{passed,failed,skipped,errored,interrupted,timeout}`, `evals[]`. Source: §9.

## Risk Inventory

1. **R1 (HIGH/MEDIUM)** — Claude Code TTY behavior changes between versions breaks PtyDriver. Mitigation: pin `claude` version range in `eval doctor`; full TTY transcripts.
2. **R2 (MEDIUM/HIGH)** — Per-eval HOME setup slow (135 file ops). Mitigation: reuse optimized `install_hooks.py`; ~1.4s/eval acceptable.
3. **R3 (MEDIUM/MEDIUM)** — MCP server flakiness causes E1/E2 false failures. Mitigation: per-eval retry-once on MCP-specific failure modes; "MCP-server-flaky" tag.
4. **R4 (LOW/LOW)** — Concurrent HOMEs exhaust disk. Mitigation: `--keep-home false` default; `--max-disk-mb 1024` poller every 5s.
5. **R5 (LOW/LOW)** — Ptytest fork drift from upstream. Mitigation: quarterly review of `pexpect` releases.
6. **R6 (MEDIUM/MEDIUM)** — 15-eval suite >10min adoption friction. Mitigation: `--eval <subset>`; future `suites/quick.yaml`.
7. **R7 (HIGH/LOW)** — Maintainer runs harness against real `~/.claude/`. Mitigation: hard guard in `HomeIsolation.setup()` refusing HOMEs outside known scratch dirs.
8. **R8 (MEDIUM/LOW)** — `IsolationLayers` shape changes breaking extension. Mitigation: vendor copy if refactor risk grows; pin to tested SHA for now.
9. **R9 (MEDIUM/HIGH)** — PR scope creep as evals get added. Mitigation: ship harness as PR 1; evals as PR 2 in batches of 3-5.

## Dependency Inventory

### Python Libraries
1. **pexpect (>=4.9)** — TTY subprocess control; pinned via vendored ptytest fork.
2. **jsonschema** — manifest validation (transitive dependency, no new install).
3. **click (>=8.0.0)** — CLI framework (existing).
4. **concurrent.futures (stdlib)** — `ThreadPoolExecutor`, `as_completed`.
5. **shutil (stdlib)** — `which()`, hook file deployment.
6. **pathlib (stdlib)** — Path manipulation, `is_relative_to`.

### Vendored Dependencies
7. **ptytest fork** (`brandon-fryslie/ptytest`, MIT, Python 3.8+) — vendored under `cli/eval/pty/`; LICENSE retained.

### External Binaries (Capability-Gated)
8. **claude binary** (min_version: 0.5.0) — HARD requirement.
9. **make** — HARD requirement.
10. **jq** — HARD requirement.
11. **git** — HARD requirement.

### MCP Servers (SOFT-SKIP via `--no-mcp`)
- `mcp_server.auggie`
- `mcp_server.auggie-mcp`
- `mcp_server.airis-mcp-gateway`

### Internal Module Dependencies
- `cli/sprint/executor.py:107-182` (`IsolationLayers`)
- `cli/sprint/executor.py:190-335` (`AggregatedPhaseReport` shape)
- `cli/pipeline/process.py:24-150` (`ClaudeProcess`)
- `cli/prd/executor.py:774-802` (orchestrator pattern)
- `cli/install_hooks.py` (`install_hooks`)
- `src/superclaude/hooks/scripts/*.sh` (deployed into HOMEs)
- `src/superclaude/hooks/hooks.json` (settings source)

## Success Criteria

1. **SC1: Maintainer sign-off on ADRs** — RyanW signs off on 4 original decisions + 4 new ADRs (D-5..D-8) in `decisions.md`.
2. **SC2: Manifest schema covers all 15 evals** — All 15 eval IDs (E1-E15) from `/sc:brainstorm` addressable by manifest schema (§5) AND match eval_id regex.
3. **SC3: Zero new external deps** — No new external Python deps required beyond `pexpect` (vendored) and `jsonschema` (transitive).
4. **SC4: Effort estimate acknowledged** — ~1,340 LOC harness + 15 eval bodies (+150 LOC for R2 path-guard, status taxonomy, disk-budget poller, EvalOutcome contract) acknowledged.
5. **SC5: Open-question list resolved** — Open-question list in `decisions.md` fully resolved before `/sc:roadmap`.

### Additional measurable acceptance signals
- `superclaude eval doctor` prints green checklist on clean dev machine (Phase 1 validation).
- Phase 3 validates real Claude Code subprocess spawn end-to-end with stub 1-eval suite (E1 only).
- `make verify-sync` post-changes must EXIT=0 (Phase 4 validation).
- Exit code semantics: 0 ⇔ no eval in {FAIL,ERRORED,TIMEOUT,XPASS}; 1 ⇔ at least one; 2 ⇔ harness error; 3 ⇔ INTERRUPTED.
- Reporter contract: `len(outcomes) == counts.expanded_n_prime` (mismatch → `ReporterContractViolation`, exit 2).

## Open Questions

1. **OQ-1:** Resolution of remaining items in `decisions.md` open-question list (referenced in SC5 but content not in spec).
2. **OQ-2:** Concrete content of E3–E15 manifest entries (only E1 and E2 parameterize are shown in §5; spec defers full eval-body design).
3. **OQ-3:** Behavior of `--no-pty` flag — exact subset of evals excluded ("most A/D categories") is not enumerated.
4. **OQ-4:** Whether IronClaude has a top-level NOTICE file for ptytest license attribution; §13 says "add one" if absent — decision pending.
5. **OQ-5:** Exact MCP server reachability check semantics (`mcp_server_reachable("auggie")` is interface only — implementation contract undefined).
6. **OQ-6:** Suite file naming convention beyond `real.yaml` — `quick.yaml` mentioned as follow-up but not specified.
7. **OQ-7:** Whether `--junit` flag exists (§9 says "generated only when `--junit` is passed" but §4 flag table does not list `--junit`).
8. **OQ-8:** Time-offset mechanism details — `CLAUDE_FAKE_TIME_OFFSET` env var is mentioned but how Claude Code consumes it is not defined.
9. **OQ-9:** macOS support roadmap — §1 non-goals list it as follow-up but no timeline.
10. **OQ-10:** Exact retry semantics for R3 ("per-eval retry-once on MCP-specific failure modes") — failure-mode taxonomy and idempotency guarantees not specified.
