---
spec_source: "design-spec.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: null
---
# Real Claude Code Eval Harness — Project Roadmap

## Executive Summary

Build a local-only `superclaude eval --suite real` harness that runs 15 real Claude Code evaluations through PTY subprocesses, isolates every eval in its own HOME/session/state namespace, verifies hook matcher coverage against real MCP tool calls, and emits reproducible per-run artifacts under `.dev/eval-runs/<ISO>/<run-id>/`. The architecture should land as a security-first CLI subsystem: loader and schema validation before filesystem writes, HomeIsolation containment before hook deployment, PTY lifecycle before parallel orchestration, and reporter invariants before broad eval authoring.

**Business Impact:** Maintainers get falsifiable, reproducible local confidence that hook matchers and real Claude Code behavior still work, reducing regressions that unit tests cannot observe because they bypass PTY, HOME, and MCP telemetry boundaries.

**Complexity:** HIGH (0.72) — Real TTY orchestration, parallel subprocess management, HOME containment, hook deployment, capability gating, and N' reporting invariants create multiple failure domains that must be sequenced behind strict validation and containment gates.

**Critical path:** Resolve blocking decisions → define manifest/models/security guards → implement isolated PTY runner → add bounded parallel orchestration and disk/signal controls → emit contract-checked reports → author 15 real evals and hook coverage gate.

**Key architectural decisions:**

- Keep v1 Linux-only and local-only to reduce PTY and CI variance while proving the harness contract.
- Validate eval IDs and suite manifests before any filesystem operation; revalidate inside HomeIsolation as defense-in-depth.
- Use blocking `ThreadPoolExecutor + as_completed` orchestration with one PTY subprocess per worker rather than async coordination.

**Open risks requiring resolution before M1:**

- OQ-1, OQ-2, OQ-3, OQ-4, OQ-5, OQ-7, OQ-8, and OQ-10 block exact schema, CLI flag, licensing, capability, retry, and time-offset contracts needed before implementation can close its first milestone.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Decisions, Schema, and CLI Contract|Foundation|P0|L|OQ-1,OQ-3,OQ-4,OQ-7,OQ-8,OQ-10|21|HIGH|
|M2|Isolation, Capability Gates, and Security Guards|Security|P0|XL|M1,OQ-5|18|HIGH|
|M3|PTY Runner and Parallel Orchestration|Backend|P0|XL|M2|17|HIGH|
|M4|Reporting, Artifacts, and Sync Validation|Reporting|P1|L|M3|13|MEDIUM|
|M5|Real Suite Coverage and Release Validation|Validation|P1|XL|M4,OQ-2,OQ-6,OQ-9|11|MEDIUM|

## Dependency Graph

OQ-1/OQ-3/OQ-4/OQ-7/OQ-8/OQ-10 → M1 → M2 → M3 → M4 → M5
OQ-5 → M2
OQ-2/OQ-6/OQ-9 → M5
FR-SCH2 → FR-ISO2 → NFR-SEC2 → NFR-SEC3
COMP-005 → COMP-002 → COMP-001
COMP-012 + COMP-014 → COMP-006 → COMP-004
COMP-013 + COMP-007 + COMP-011 → COMP-004 → COMP-003
COMP-010 + DM-009 + DM-010 → COMP-004
COMP-003 + DM-001 + COMP-008 → FR-RPT1
FR-G5 + COMP-009 + TEST-013 → M5 exit

## M1: Decisions, Schema, and CLI Contract

**Objective:** Lock decision inputs and create the public CLI/manifest contract before filesystem writes or subprocess work begins | **Duration:** Week 1 (1 week) | **Entry:** extraction accepted; maintainer available for OQ closure | **Exit:** CLI commands, schema, eval ID validation, DTO contracts, and blocking ADR decisions are review-ready

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|FR-G3|Additive CLI integration|Add `superclaude eval` as an additive command family using existing CLI conventions without breaking current commands.|CLI|OQ-1|entrypoint registered; existing commands unchanged; command help lists eval group; source under src/superclaude|M|P0|
|2|FR-G6|Single-command local run|Expose the local invocation path for `uv run superclaude eval --suite real` with defaults resolving to the real suite.|CLI|FR-G3|command resolves suite=real; UV invocation documented in help; exits through eval run path|S|P1|
|3|FR-CLI1|Run subcommand|Implement `eval run` with suite, parallel, eval subset, MCP, PTY, output, HOME retention, timeout, disk, JSON, and verbosity flags.|CLI|FR-G3,OQ-3,OQ-7|--suite; --parallel; --eval; --no-mcp; --no-pty; --output-dir; --keep-home; --timeout-mult; --max-disk-mb; --json; --verbose|M|P0|
|4|FR-CLI2|List subcommand|Implement `eval list` to enumerate suite manifests from `cli/eval/suites/*.yaml`.|CLI|FR-G3|reads suite dir; prints suite names; handles empty directory; exits 0 on success|S|P1|
|5|FR-CLI3|Describe subcommand|Implement `eval describe` to print suite or single-eval manifest content.|CLI|FR-G3,FR-SCH1|--suite required; optional --eval ID; validates before print; preserves manifest fields|S|P1|
|6|FR-CLI4|Doctor subcommand|Implement `eval doctor` as the preflight surface for binaries, HOME, ptytest, capability gates, and coverage checks.|CLI|FR-G3,OQ-5|checks claude; checks jq/make/git; checks ~/.claude exists; reports ptytest; reports capability gates; supports coverage check|M|P0|
|7|FR-SCH1|Suite schema validation|Validate YAML suite manifests with `jsonschema` in doctor and run before eval expansion proceeds.|Loader|FR-CLI1,FR-CLI4|schema file loaded; invalid manifest exits 2; doctor and run both validate; errors name field path|M|P0|
|8|FR-SCH2|Eval identifier validation|Reject unsafe eval IDs and template-token IDs before any filesystem operation.|Loader|FR-SCH1|regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`; expanded IDs checked; template tokens rejected; InvalidEvalId; exit 2 before paths|M|P0|
|9|NFR-SEC1|ID traversal prevention|Use the eval ID regex contract to prevent traversal via interpolated HOME paths.|Security|FR-SCH2|slash rejected; dot-dot rejected; absolute path rejected; parameterized unsafe ID rejected before filesystem work|S|P0|
|10|COMP-001|eval_group command group|Click group exporting eval run/list/describe/doctor and delegating to loader, orchestrator, runner, and capability checks.|CLI|FR-G3|file:cli/eval/commands.py; exports:run,list,describe,doctor; deps:COMP-002,COMP-003,COMP-004,COMP-009; registered in main CLI|M|P0|
|11|COMP-002|SuiteLoader|Manifest loader for YAML, jsonschema validation, capability resolution, and eval ID enforcement.|Loader|FR-SCH1,FR-SCH2|file:cli/eval/loader.py; reads YAML; validates schema; expands parameterize; enforces regex; deps:COMP-005,COMP-010|M|P0|
|12|COMP-005|EvalConfig|Configuration dataclass carrying default paths, output roots, and allowed scratch root policy.|Config|FR-CLI1|file:cli/eval/config.py; fields:paths,defaults,allowed_scratch_roots; output_dir resolved; scratch roots normalized|M|P0|
|13|COMP-010|ExpectDSL interface|Define the fluent and declarative assertion DSL interface consumed by manifests and runner.|Expect|FR-SCH1|file:cli/eval/expect.py; methods:file,jsonl,settings_json,exit_code,stderr,stdout,duration; returns ExpectCallable; YAML mapping supported|M|P0|
|14|DM-002|EvalSpec model|Parsed manifest entry model for one eval definition before execution.|Models|FR-SCH1|id:str; title:str; category:str; requires:list; timeout_sec:int; isolation:dict; inputs:list; expects:list; parameterize:list|M|P0|
|15|DM-005|ExpectFailure model|Assertion failure detail used by ExpectResult and reports.|Models|COMP-010|eval_id:str; expect_id:str; message:str; actual:any; expected:any; artifact_ref:str|S|P1|
|16|DM-007|Capability model|Capability check declaration for binary and MCP preconditions.|Models|FR-CLI4|name:str; check:Callable[[],bool]; failure_mode:Literal[hard,skip,xfail]; skip_flag:Optional[str]; description:str|S|P0|
|17|DM-009|ExpectResult model|Assertion outcome record returned by every Expect callable.|Models|COMP-010|name:str; passed:bool; message:str; details:dict; duration_sec:float; failure:ExpectFailure|S|P0|
|18|DM-010|EvalContext model|Runtime context passed to assertion callables.|Models|COMP-010|eval_id:str; home_path:Path; run_dir:Path; env:dict; stdout_path:Path; stderr_path:Path; transcript_path:Path; artifacts:dict|S|P0|
|19|DM-011|Suite manifest YAML schema|Top-level YAML suite contract for suite metadata, defaults, capabilities, and eval list.|Schema|FR-SCH1|name; version; description; defaults; required_binaries; optional_capabilities; evals[]; parameterize accepted; unknown required fields rejected|M|P0|
|20|TEST-001|Schema and ID rejection tests|Add validation coverage for schema errors, unsafe IDs, parameterized IDs, and command preflight ordering.|Tests|FR-SCH1,FR-SCH2|invalid schema exits 2; unsafe id exits 2; no filesystem writes before rejection; parameterize expansion tested|M|P0|
|21|OPS-001|Decision record closure|Record decisions for ADR sign-off, PTY flag semantics, JUnit flag, time offset, retry, and NOTICE handling.|Ops|OQ-1,OQ-3,OQ-4,OQ-7,OQ-8,OQ-10|decisions.md updated; D-5..D-8 signed off; unresolved blockers listed; implementation gates reference decisions|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`superclaude eval`|Click command registry|Yes|M1|COMP-001|
|`cli/eval/suites/suite.schema.json`|Schema registry|Yes|M1|COMP-002,FR-SCH1|
|`Expect.*` YAML mapping|Strategy table|Yes|M1|COMP-010,COMP-004|
|Capability failure modes|Dispatch table|Yes|M1|COMP-009,FR-CLI4|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Unresolved decisions cause contract churn after implementation begins|HIGH|MEDIUM|CLI flags, schema, and reports may need rework|Close OQ-1/OQ-3/OQ-4/OQ-7/OQ-8/OQ-10 before M1 exit|Architect|
|2|PR scope expands before harness contract is stable|MEDIUM|HIGH|Review burden increases and eval bodies obscure core contract defects|Ship harness foundation first; defer broad eval bodies to M5 batches|Tech Lead|

### Milestone Dependencies — M1

- Requires maintainer sign-off on decisions.md items before command and schema contracts are treated as closed.
- Requires source-of-truth discipline: edits under `src/superclaude/` and later sync into `.claude/`.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-1|What exact remaining `decisions.md` items must be resolved for SC5?|Blocks ADR sign-off and M1 exit|RyanW|Before M1 exit|
|2|OQ-3|Which eval categories are excluded by `--no-pty`?|Blocks run flag semantics|Architect|Before FR-CLI1 close|
|3|OQ-4|Does the repo require a top-level NOTICE file for ptytest attribution?|Blocks vendored dependency packaging|Maintainer|Before NFR-MAINT1 close|
|4|OQ-7|Should `--junit` be added to the run flag set?|Blocks report CLI contract|Architect|Before FR-CLI1 close|
|5|OQ-8|How should `CLAUDE_FAKE_TIME_OFFSET` be consumed or validated?|Blocks EvalConfig and HomeIsolation contract|Architect|Before COMP-005 close|
|6|OQ-10|What exact MCP-specific failure taxonomy permits retry-once?|Blocks capability and retry policy|QA Lead|Before M3 exit|

## M2: Isolation, Capability Gates, and Security Guards

**Objective:** Implement the containment boundary, capability preflight layer, and hook deployment path so every later PTY run executes inside a known eval scratch root | **Duration:** Week 2 (1 week) | **Entry:** M1 schema/CLI contracts accepted | **Exit:** HOME isolation refuses unsafe paths, capability checks classify blockers, and hook deployment into per-eval HOMEs is tested

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|FR-ISO1|HomeIsolation extension|Extend/combine IsolationLayers with per-eval HOME override, session stamp, optional time offset, and sibling HOME layout.|Isolation|COMP-005,COMP-012|HOME override set; CLAUDE_SESSION_ID set; CLAUDE_FAKE_TIME_OFFSET optional; homes under home_root; IsolationLayers behavior retained|L|P0|
|2|FR-ISO2|Path containment guard|Enforce path and symlink containment before deploying hooks or writing state.|Isolation|FR-SCH2,FR-ISO1|eval_id rechecked; home_path resolved; scratch_root resolved; home_path relative to scratch_root; scratch root allowlisted; symlinks resolved after creation; HomeContainmentViolation raised|XL|P0|
|3|NFR-SEC2|HOME containment defense|Apply containment as a second validation layer independent of manifest loader success.|Security|FR-ISO2|loader bypass still rejected; symlink-to-real-HOME rejected; only allowlisted roots accepted; failure exits as harness error|M|P0|
|4|NFR-SEC3|Real HOME guard|Refuse execution when HOME would point outside known eval-runs scratch directories.|Security|NFR-SEC2|real ~/.claude path refused; repo .dev/eval-runs accepted; /tmp/eval-runs accepted; allowlisted output-dir accepted|M|P0|
|5|NFR-ISO2|Atomic setup contract|Preserve partial HOME artifacts on setup errors and tag setup failures distinctly from eval failures.|Isolation|FR-ISO1|try/except wraps setup; post-mkdtemp failure keeps HOME; status ERRORED; setup_failed tag written; keep forced true|M|P0|
|6|NFR-PERF1|HOME setup performance|Keep per-eval HOME creation acceptable by reusing optimized hook installation behavior.|Isolation|COMP-014|~135 file ops accepted; ~1.4s/eval target; install_hooks optimizations reused; setup timing recorded|S|P1|
|7|NFR-MAINT1|Vendored PTY dependency discipline|Establish ptytest vendoring, pexpect pinning, license retention, provenance, and review cadence before driver work.|PTY|OQ-4|ptytest under cli/eval/pty; pexpect>=4.9 pinned; LICENSE retained; PROVENANCE.md records fork SHA; quarterly review task recorded|M|P1|
|8|COMP-006|HomeIsolation|Isolation class with setup, env, teardown, state path, and containment behavior.|Isolation|FR-ISO1,FR-ISO2|file:cli/eval/isolation.py; methods:setup,env,teardown,state_path; fields:eval_id,home_root,session_id,time_offset_sec; deps:COMP-012,COMP-014|XL|P0|
|9|COMP-009|CapabilityGates|Capability checker for required binaries, optional MCP reachability, skip flags, and doctor output.|Capability|DM-007,OQ-5|file:cli/eval/capability_gates.py; check_all(skip_flags); which_or_skip; mcp_server_reachable; returns CapabilityReport|M|P0|
|10|COMP-012|IsolationLayers reuse|Integrate the existing isolation layers as the base boundary for cwd, git ceiling, plugin dir, and settings dir.|Isolation|FR-ISO1|existing cwd layer used; git ceiling preserved; plugin dir isolated; settings dir isolated; no replacement of current behavior|M|P0|
|11|COMP-014|install_hooks reuse|Deploy hook sources into per-eval HOMEs through the existing optimized hook installer.|Hooks|FR-ISO1,NFR-PERF1|file:cli/install_hooks.py; populates per-eval HOME; uses src hook source; no direct real-HOME writes; errors tagged|M|P0|
|12|DM-006|HomeIsolation dataclass|Frozen dataclass representing per-eval isolation configuration.|Models|COMP-006|eval_id:str; home_root:Path; session_id:str; time_offset_sec:int=0|S|P0|
|13|DM-008|CapabilityReport model|Report structure for capability statuses and blocked eval listings.|Models|COMP-009|capabilities:list; statuses:dict; blocked_evals:list; skip_flags:list; hard_failures:list; soft_skips:list; soft_xfails:list|S|P0|
|14|TEST-002|Containment unit tests|Validate allowed roots, rejected roots, and loader-bypass defense at the HomeIsolation boundary.|Tests|FR-ISO2,NFR-SEC2|repo .dev accepted; /tmp accepted; non-allowlisted root rejected; loader bypass rejected; exit code 2 path covered|M|P0|
|15|TEST-003|Symlink attack tests|Verify symlink resolution catches scratch and HOME escape attempts after directory creation.|Tests|FR-ISO2,NFR-SEC3|scratch symlink to real HOME rejected; nested symlink escape rejected; partial HOME preserved; setup_failed tag asserted|M|P0|
|16|TEST-004|Capability gate tests|Validate hard, skip, and xfail capability classifications including MCP disabled behavior.|Tests|COMP-009,OQ-5|missing claude hard fails; --no-mcp soft-skips MCP evals; xfail supported; doctor renders statuses|M|P0|
|17|TEST-005|Hook deployment performance test|Measure hook installation path and capture setup timing without requiring live Claude execution.|Tests|NFR-PERF1,COMP-014|setup timing captured; hook files present; no real ~/.claude writes; performance regression threshold documented|S|P1|
|18|OPS-002|Scratch root policy|Document and enforce allowed scratch roots across config, isolation, and CLI output-dir handling.|Ops|COMP-005,FR-ISO2|/tmp/eval-runs; repo .dev/eval-runs; resolved --output-dir allowlist; policy appears in doctor failures|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|HomeIsolation setup pipeline|Lifecycle chain|Yes|M2|COMP-004|
|Allowed scratch roots|Policy registry|Yes|M2|COMP-005,COMP-006|
|Capability checks|Dispatch table|Yes|M2|COMP-001,COMP-003|
|Hook deployment|Installer wiring|Yes|M2|COMP-006,COMP-004|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Maintainer accidentally targets real `~/.claude/`|HIGH|LOW|Real user configuration or telemetry could be modified|Hard guard refuses HOMEs outside known eval scratch roots|Security Lead|
|2|Home setup is too slow for parallel runs|MEDIUM|HIGH|Suite runtime exceeds adoption target|Reuse optimized install_hooks path and record timing in outcomes|Backend Lead|
|3|IsolationLayers changes break HomeIsolation extension|MEDIUM|LOW|Eval setup could silently lose isolation guarantees|Contract tests around reused layers; vendor copy only if refactor risk materializes|Architect|
|4|Vendored ptytest attribution is incomplete|LOW|LOW|Release cannot satisfy license expectations|Resolve OQ-4 and record LICENSE/PROVENANCE before PTY driver merge|Maintainer|

### Milestone Dependencies — M2

- Requires M1 DTO and config contracts to stabilize path, skip, and capability schemas.
- Requires OQ-5 resolution before MCP reachability checks can be considered complete.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-5|What exact contract defines MCP server reachability for `mcp_server_reachable("auggie")`?|Blocks capability gates and hook coverage preflight|Architect|Before COMP-009 close|

## M3: PTY Runner and Parallel Orchestration

**Objective:** Run real Claude Code subprocesses through PTYs inside isolated HOMEs and coordinate bounded parallel execution with deterministic lifecycle, disk, signal, and retry semantics | **Duration:** Week 3 (1 week) | **Entry:** M2 isolation and capability gates pass | **Exit:** Single and parallel real PTY evals execute with lifecycle assertions, bounded resources, and correct interruption handling

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|FR-G1|Real PTY Claude subprocess|Drive the real `claude` binary through a PTY for every eval without in-process SDK shortcuts.|PTY|COMP-007,COMP-013|pexpect spawn used; real claude binary invoked; no SDK client path; transcript captured; exit captured|XL|P0|
|2|FR-G2|Parallel 15-eval execution|Run expanded evals in parallel with default 8 workers and max 15 while preserving per-eval state isolation.|Orchestrator|COMP-003,NFR-ISO1|ThreadPoolExecutor max_workers=8 default; --parallel clamped 1..15; 15 evals schedulable; unique HOME/session/state per eval|XL|P0|
|3|FR-LC1|Per-eval lifecycle sequence|Execute the ordered lifecycle from isolation setup through hook deployment, PTY spawn, input injection, observation, assertion, and teardown.|Runner|COMP-004,COMP-006,COMP-007|build HomeIsolation; deploy hooks; spawn ClaudeProcess via PtyDriver; inject inputs; observe JSONL/state; apply Expect; teardown HOME|XL|P0|
|4|FR-EXP1|Expectation assertion DSL|Implement Expect primitives as callable assertions for declarative YAML and programmatic usage.|Expect|COMP-010,DM-009,DM-010|Expect.file; Expect.jsonl; Expect.settings_json; Expect.exit_code; Expect.stderr; Expect.stdout; Expect.duration; returns callable EvalContext->ExpectResult|L|P0|
|5|NFR-PERF2|Concurrency resource bounds|Bound subprocess concurrency and document RAM expectations for 8 and 15 workers.|Orchestrator|FR-G2|8 workers default; 15 max; ~150MB/process noted; 2.25GB free RAM check/warning for 15; no oversubscription beyond clamp|M|P1|
|6|NFR-PERF4|Disk budget enforcement|Poll run disk usage and stop scheduling new evals when budget is breached.|Orchestrator|COMP-003|--max-disk-mb default 1024; poll every 5s; breach lets in-flight finish; no new scheduling; exit 2; disk_budget_exceeded recorded; 0 disables|L|P0|
|7|NFR-ISO1|No shared mutable state|Ensure max-concurrency runs do not share HOME, state files, log handles, or ports.|Isolation|FR-G2,FR-ISO1|unique HOME; unique CLAUDE_SESSION_ID; unique telemetry namespace; no shared auggie-first.jsonl handle; no port collisions|M|P0|
|8|NFR-REL1|Signal and timeout handling|Cancel and summarize cleanly on SIGINT/SIGTERM and kill timed-out PTY subprocesses.|Orchestrator|COMP-003,COMP-007|SIGINT/SIGTERM mark in-flight INTERRUPTED; partial summary written; exit 3; timeout kills subprocess; zombie reaped; TIMEOUT status|L|P0|
|9|NFR-REL2|Single-pass retry policy|Keep failed eval execution deterministic with no default retry and subset rerun support.|Orchestrator|FR-CLI1,OQ-10|no default retry; failed IDs emitted; --eval failed-id reruns subset; MCP retry-once only if OQ-10 contract permits|S|P1|
|10|COMP-003|RunOrchestrator|Scheduler coordinating expanded specs, worker pool, per-eval timeouts, disk polling, and EvalOutcome emission.|Orchestrator|COMP-004,COMP-008,DM-001|file:cli/eval/orchestrator.py; ThreadPoolExecutor; as_completed; timeout control; disk poller; emits EvalOutcome; deps:COMP-004,COMP-008,DM-001|XL|P0|
|11|COMP-004|EvalRunner|Per-eval executor that wires isolation, hooks, PTY process, input injection, observations, expectations, and teardown.|Runner|COMP-006,COMP-007,COMP-011|file:cli/eval/runner.py; build isolation; deploy hooks; spawn; inject; observe; assert; teardown; deps:COMP-006,COMP-007,COMP-011|XL|P0|
|12|COMP-007|PtyDriver|PTY adapter around pexpect for prompt readiness, input injection, stdout/stderr capture, and exit status.|PTY|NFR-MAINT1,COMP-011|file:cli/eval/pty/driver.py; pexpect.spawn; expect_prompt_ready; inject_prompt; stdin write; stdout read; exit capture|L|P0|
|13|COMP-011|PtyStream|Stream processor for ANSI stripping, line buffering, and timeout-aware read loops.|PTY|COMP-007|file:cli/eval/pty/stream.py; ansi strip; line buffering; timeout handling; transcript-safe output|M|P1|
|14|COMP-013|ClaudeProcess reuse|Reuse existing subprocess process structure for spawn and capture semantics under the PTY adapter.|PTY|FR-G1|file:cli/pipeline/process.py; spawn/capture pattern reused; wrapped by PtyDriver; no in-process SDK path|M|P0|
|15|DM-001|EvalOutcome model|Frozen per-expanded-eval outcome contract consumed by reporter and exit-code logic.|Models|COMP-003|eval_id:str; title:str; status:Literal[PASS,FAIL,ERRORED,TIMEOUT,INTERRUPTED,SKIPPED,XFAIL,XPASS]; duration_sec:float; expects:list[ExpectResult]; skip_reason:str or None; skip_flag_triggered:str or None; artifacts:dict[str,str]; error_class:str or None|M|P0|
|16|DM-003|EvalResult model|Runner-level per-eval result before orchestration-level normalization.|Models|COMP-004|eval_id:str; status:str; started_at:str; finished_at:str; duration_sec:float; stdout:str; stderr:str; artifacts:dict; error:Exception or None|S|P0|
|17|TEST-006|PTY lifecycle tests|Validate real PTY spawn, prompt readiness, input injection, timeout handling, and transcript capture with a safe single eval.|Tests|FR-G1,FR-LC1|real claude spawned when available; prompt readiness observed; input injected; transcript exists; timeout reaps child|L|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|ThreadPoolExecutor scheduler|Concurrency pattern|Yes|M3|COMP-003|
|PtyDriver to ClaudeProcess|Adapter wiring|Yes|M3|COMP-004,COMP-013|
|Expect callable registry|Strategy pattern|Yes|M3|COMP-004,FR-EXP1|
|Signal handlers|Callback wiring|Yes|M3|COMP-003,NFR-REL1|
|Disk budget poller|Scheduler guard|Yes|M3|COMP-003,NFR-PERF4|

### Milestone Dependencies — M3

- Requires M2 containment tests to pass before spawning real subprocesses.
- Requires OQ-10 resolution for any MCP retry-once behavior; otherwise deterministic no-retry remains the v1 policy.

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Claude Code TTY behavior changes break prompt detection|HIGH|MEDIUM|Real evals fail despite harness correctness|Pin supported Claude version in doctor and preserve full TTY transcripts|Backend Lead|
|2|Concurrent subprocesses exhaust RAM or disk|MEDIUM|MEDIUM|Run instability and incomplete artifacts|Clamp workers, document RAM, poll disk every 5s, stop scheduling on budget breach|DevOps|
|3|Signal handling loses partial results|MEDIUM|LOW|Interrupted runs become non-diagnostic|Centralize cancellation and write partial summary before exit 3|QA Lead|

## M4: Reporting, Artifacts, and Sync Validation

**Objective:** Convert runner outcomes into reproducible artifacts, enforce reporter dimensional contracts, and validate source/dev-copy synchronization before real-suite expansion | **Duration:** Week 4 (1 week) | **Entry:** M3 real PTY and parallel execution pass | **Exit:** summary.md, summary.json, optional junit.xml, exit-code semantics, artifact layout, and sync verification are contract-tested

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|FR-G4|Reproducible artifacts|Produce per-run and per-eval artifacts under `.dev/eval-runs/<ISO>/<run-id>/`.|Reporter|COMP-008|run dir includes ISO/run-id; per-eval logs; aggregate Markdown; aggregate JSON; failure stack traces; TTY transcripts|L|P0|
|2|FR-RPT1|Aggregated run report|Emit human, machine, and optional JUnit reports while enforcing N' outcome cardinality.|Reporter|COMP-008,DM-012|summary.md; summary.json; optional junit.xml; evals length equals expanded_n_prime; skipped included; mismatch raises ReporterContractViolation; exit 2|XL|P0|
|3|NFR-PERF3|Suite runtime target|Keep the full real suite under the target runtime and provide subset execution for iteration.|Reporter|FR-CLI1,FR-G2|full suite target <10min; --eval subset available; quick suite follow-up tracked; duration recorded in summary|M|P1|
|4|COMP-008|Reporter AggregatedRunReport|Report builder for Markdown, YAML, JSON, JUnit, and outcome-count contract checks.|Reporter|DM-001,DM-012|file:cli/eval/reporter.py; to_markdown; to_yaml; to_json; to_junit; asserts len(outcomes)==counts.expanded_n_prime|L|P0|
|5|COMP-015|AggregatedPhaseReport reference|Reuse the existing aggregate-report shape as a design reference for eval reporting without coupling output contracts.|Reporter|COMP-008|file:cli/sprint/executor.py reference; summary sections mapped; status counts mapped; no dependency on sprint runtime|S|P2|
|6|DM-004|RunSummary model|Aggregate in-memory summary for a run before serialization.|Models|COMP-008|run_id:str; started_at:str; finished_at:str; duration_sec:float; suite:str; counts:dict; totals:dict; evals:list[EvalOutcome]; artifacts:dict|M|P0|
|7|DM-012|summary.json schema|Machine-readable report contract for run metadata, counts, totals, and eval outcomes.|Schema|FR-RPT1|run_id; started_at; duration_sec; suite; manifest_version; parallel; counts.manifest_n; counts.expanded_n_prime; counts.kept_k; counts.skipped_s; counts.kept_plus_skipped_equals_n_prime; totals.passed; totals.failed; totals.skipped; totals.errored; totals.interrupted; totals.timeout; evals[]|M|P0|
|8|TEST-007|Reporter contract tests|Validate N' versus K behavior, skipped inclusion, mismatch failure, and JSON schema fidelity.|Tests|FR-RPT1,DM-012|len(evals)==expanded_n_prime; skipped has status+skip_reason; mismatch exits 2; schema fields complete|M|P0|
|9|TEST-008|Exit-code semantics tests|Assert process exit codes for clean, failing, harness-error, and interrupted runs.|Tests|FR-RPT1,NFR-REL1|0 iff no FAIL/ERRORED/TIMEOUT/XPASS; 1 if any such eval; 2 harness error; 3 interrupted|M|P0|
|10|TEST-009|Artifact reproducibility tests|Verify run directories, transcripts, logs, stack traces, and summaries are written deterministically.|Tests|FR-G4|run dir pattern stable; transcript path recorded; logs present; stack trace on error; summary links artifacts|M|P0|
|11|OPS-003|Artifact retention policy|Define default deletion and keep-home behavior for per-eval HOMEs and run artifacts.|Ops|FR-G4,NFR-PERF4|--keep-home default false; failed setup preserved; run summaries retained; disk budget messages include retention advice|S|P1|
|12|MIG-001|Source sync migration|Sync eval CLI sources from `src/superclaude/` into `.claude/` dev copies after implementation.|Sync|OPS-003|make sync-dev run; make verify-sync exits 0; no direct .claude source edits; sync evidence captured|S|P0|
|13|OPS-004|Validation command set|Define the validation command sequence for roadmap completion using UV and make targets.|Ops|MIG-001|uv run pytest targeted eval tests; make verify-sync; eval doctor; single eval run; results linked in artifacts|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Outcome to reporter serialization|DTO mapping|Yes|M4|COMP-008,DM-012|
|JUnit writer|Optional writer strategy|Yes|M4|FR-RPT1|
|Exit-code resolver|Status dispatch table|Yes|M4|COMP-001,COMP-008|
|Artifact path registry|Report link map|Yes|M4|FR-G4,DM-004|
|Sync validation|Build target wiring|Yes|M4|MIG-001,OPS-004|

### Milestone Dependencies — M4

- Requires M3 to emit EvalOutcome consistently for PASS, FAIL, ERRORED, TIMEOUT, INTERRUPTED, SKIPPED, XFAIL, and XPASS.
- Requires source-of-truth edits to remain under `src/superclaude/` before sync validation.

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Reporter drops skipped evals and hides coverage gaps|HIGH|LOW|Summary becomes non-falsifiable for expanded suite size|Assert `len(outcomes)==expanded_n_prime` and include skipped outcomes|QA Lead|
|2|Concurrent artifacts exhaust disk|LOW|LOW|Run terminates before useful diagnostics are written|Default --keep-home false, poll disk, keep partial summaries|DevOps|
|3|Full suite exceeds 10 minutes|MEDIUM|MEDIUM|Maintainers avoid local run|Track duration, support --eval subset, plan quick suite follow-up|Product Owner|

## M5: Real Suite Coverage and Release Validation

**Objective:** Author the real eval suite, enforce falsifiable hook matcher coverage, validate local runnability, and prepare follow-up rollout items without expanding v1 beyond local Linux execution | **Duration:** Weeks 5-6 (2 weeks) | **Entry:** M4 reporter and artifact contracts pass | **Exit:** all 15 evals are addressable, coverage gate fails missing matchers, full run artifacts are reproducible, and release validation evidence is complete

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|
|1|FR-G5|Hook matcher coverage gate|Require a real eval for each PostToolUse hook matcher pattern and fail the run when coverage is missing.|Coverage|COMP-009,FR-RPT1,OQ-2|real MCP call matches P; per-eval hook JSONL read; hook fired asserted; doctor --check-coverage; run top gate; missing matcher fails|XL|P0|
|2|TEST-010|E1 auggie matcher eval|Author the E1 real eval covering `mcp__auggie__*` hook matcher behavior.|Eval Suite|FR-G5|real MCP tool call issued; per-eval telemetry read; hook fired asserted; skip under --no-mcp|M|P0|
|3|TEST-011|E2 auggie-mcp matcher evals|Author parameterized E2 eval coverage for `mcp__auggie-mcp__*` matcher behavior.|Eval Suite|FR-G5|parameterized IDs valid; real call issued; telemetry read; hook fired asserted; reports include expanded rows|M|P0|
|4|TEST-012|Airis gateway matcher eval|Author coverage for `mcp__airis-mcp-gateway__*` matcher behavior.|Eval Suite|FR-G5|gateway call issued when reachable; soft-skip under --no-mcp; telemetry assertion present; skip_reason recorded|M|P0|
|5|TEST-013|Coverage gate tests|Validate the doctor and run top-of-run coverage gate against missing and complete matcher sets.|Coverage|FR-G5|missing matcher fails; complete matcher passes; doctor names uncovered patterns; run refuses uncovered suite|M|P0|
|6|TEST-014|No-MCP skip behavior tests|Verify MCP-dependent evals are classified as SKIPPED with reason when `--no-mcp` is used.|Eval Suite|COMP-009,FR-RPT1|MCP evals skipped; status SKIPPED; skip_reason set; counts kept_plus_skipped_equals_n_prime true|S|P1|
|7|TEST-015|Quick subset follow-up|Define a quick suite or subset strategy for iteration without changing the v1 full-suite contract.|Eval Suite|OQ-6,NFR-PERF3|quick.yaml decision recorded; --eval subset examples pass; full real.yaml remains authoritative; runtime target tracked|S|P2|
|8|TEST-016|Full local run validation|Run the full real suite locally and capture summary, transcripts, coverage, and timing evidence.|Validation|FR-G6,FR-G5|uv run superclaude eval --suite real succeeds or reports eval failures; summary.md present; summary.json present; coverage gate passed; duration captured|L|P0|
|9|OPS-005|Release checklist|Assemble release evidence for doctor, sync, tests, artifact contracts, and known follow-ups.|Ops|OPS-004,TEST-016|eval doctor green; make verify-sync EXIT=0; targeted tests pass; full-run artifacts linked; follow-ups listed|S|P0|
|10|MIG-002|Eval-batch rollout|Split broad eval bodies into reviewable batches after the harness contract lands.|Planning|FR-G5,OQ-2|15 eval IDs tracked; batches of 3-5 defined; harness PR separable; eval PRs reference coverage map|S|P1|
|11|MIG-003|Platform follow-up plan|Record macOS and future CI support as follow-up scope outside v1 Linux-local delivery.|Planning|OQ-9|macOS non-goal preserved; CI non-goal preserved; follow-up roadmap item created; no v1 blocking work added|S|P2|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Coverage map|Matcher registry|Yes|M5|FR-G5,TEST-013|
|Real suite manifest|Suite registry|Yes|M5|COMP-002,TEST-016|
|MCP eval gating|Capability wiring|Yes|M5|COMP-009,TEST-014|
|Eval batch map|Release planning|Yes|M5|MIG-002|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|MCP server flakiness creates false failures|MEDIUM|MEDIUM|Hook coverage appears broken when external server is unstable|Use capability gates, telemetry tags, and retry-once only under resolved OQ-10 semantics|QA Lead|
|2|Full real suite takes longer than 10 minutes|MEDIUM|MEDIUM|Maintainers avoid routine local validation|Provide --eval subset and define quick-suite follow-up without weakening real suite coverage|Product Owner|
|3|Eval body authoring expands PR scope|MEDIUM|HIGH|Review slows and harness defects are harder to isolate|Ship harness first, then eval batches of 3-5 with coverage map|Tech Lead|

### Milestone Dependencies — M5

- Requires M4 reports to preserve skipped outcomes so coverage and MCP-gated evals remain auditable.
- Requires OQ-2 to define E3-E15 content before all 15 evals can be declared complete.
- Requires OQ-6 and OQ-9 to be recorded as follow-up decisions rather than hidden v1 requirements.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-2|What are the concrete E3-E15 manifest entries and eval bodies?|Blocks full 15-eval suite completion|QA Lead|Before TEST-016|
|2|OQ-6|What suite file naming convention applies beyond `real.yaml`?|Blocks quick-suite follow-up clarity|Architect|Before TEST-015|
|3|OQ-9|When should macOS support be planned after Linux v1?|Blocks platform follow-up planning|Maintainer|Before MIG-003|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|pexpect>=4.9|M2,M3|Required vendored path|Block PTY driver until vendored fork is approved|
|jsonschema|M1|Transitive existing dependency|Fail doctor/run if unavailable|
|click>=8.0.0|M1|Existing dependency|Reuse existing CLI dependency only|
|concurrent.futures|M3|stdlib|No fallback; Python runtime requirement|
|shutil|M2|stdlib|No fallback; used for binary lookup and hook deployment|
|pathlib|M1,M2|stdlib|No fallback; path containment depends on resolved paths|
|ptytest fork|M2,M3|Vendored dependency|Hold NFR-MAINT1 until license/provenance complete|
|claude binary >=0.5.0|M3,M5|Hard capability|Doctor hard-fails and run exits 2|
|make|M4,M5|Hard capability|Doctor hard-fails validation path|
|jq|M1,M4,M5|Hard capability|Doctor hard-fails report-inspection path|
|git|M4,M5|Hard capability|Doctor hard-fails sync/release validation|
|mcp_server.auggie|M5|Soft-skip with --no-mcp|Skip dependent evals with skip_reason|
|mcp_server.auggie-mcp|M5|Soft-skip with --no-mcp|Skip dependent evals with skip_reason|
|mcp_server.airis-mcp-gateway|M5|Soft-skip with --no-mcp|Skip dependent evals with skip_reason|

### Infrastructure Requirements

- Linux host for v1; macOS and Windows stay follow-up scope.
- Local machine with enough RAM for 8 default Claude subprocesses and approximately 2.25GB free RAM when `--parallel 15` is requested.
- Writable scratch root under `/tmp/eval-runs/`, repo `.dev/eval-runs/`, or allowlisted `--output-dir`.
- Real Claude Code binary on PATH and reachable MCP servers for non-skipped hook matcher evals.
- Source-of-truth workflow: edit under `src/superclaude/`, run `make sync-dev`, then `make verify-sync`.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|RR-001|Unresolved decisions cause contract churn after implementation begins|M1|MEDIUM|HIGH|Close OQ-1/OQ-3/OQ-4/OQ-7/OQ-8/OQ-10 before M1 exit|Architect|
|RR-002|PR scope expands before harness contract is stable|M1,M5|HIGH|MEDIUM|Ship harness foundation first; defer broad eval bodies to M5 batches|Tech Lead|
|RR-003|Maintainer accidentally targets real `~/.claude/`|M2|LOW|HIGH|Hard guard refuses HOMEs outside known eval scratch roots|Security Lead|
|RR-004|Home setup is too slow for parallel runs|M2|HIGH|MEDIUM|Reuse optimized install_hooks path and record timing in outcomes|Backend Lead|
|RR-005|IsolationLayers changes break HomeIsolation extension|M2|LOW|MEDIUM|Contract tests around reused layers; vendor copy only if refactor risk materializes|Architect|
|RR-006|Vendored ptytest attribution is incomplete|M2|LOW|LOW|Resolve OQ-4 and record LICENSE/PROVENANCE before PTY driver merge|Maintainer|
|RR-007|Claude Code TTY behavior changes break prompt detection|M3|MEDIUM|HIGH|Pin supported Claude version in doctor and preserve full TTY transcripts|Backend Lead|
|RR-008|Concurrent subprocesses exhaust RAM or disk|M3,M4|MEDIUM|MEDIUM|Clamp workers, document RAM, poll disk every 5s, stop scheduling on budget breach|DevOps|
|RR-009|Signal handling loses partial results|M3|LOW|MEDIUM|Centralize cancellation and write partial summary before exit 3|QA Lead|
|RR-010|Reporter drops skipped evals and hides coverage gaps|M4|LOW|HIGH|Assert `len(outcomes)==expanded_n_prime` and include skipped outcomes|QA Lead|
|RR-011|Concurrent artifacts exhaust disk|M4|LOW|LOW|Default --keep-home false, poll disk, keep partial summaries|DevOps|
|RR-012|Full suite exceeds 10 minutes|M4,M5|MEDIUM|MEDIUM|Track duration, support --eval subset, plan quick suite follow-up|Product Owner|
|RR-013|MCP server flakiness creates false failures|M5|MEDIUM|MEDIUM|Use capability gates, telemetry tags, and retry-once only under resolved OQ-10 semantics|QA Lead|
|RR-014|Full real suite takes longer than 10 minutes|M5|MEDIUM|MEDIUM|Provide --eval subset and define quick-suite follow-up without weakening real suite coverage|Product Owner|
|RR-015|Eval body authoring expands PR scope|M5|HIGH|MEDIUM|Ship harness first, then eval batches of 3-5 with coverage map|Tech Lead|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC1 maintainer ADR sign-off|Signed decisions|4 original + D-5..D-8 signed|Review `decisions.md` and release checklist|M1|
|SC2 manifest covers all evals|Addressable eval IDs|E1-E15 valid and regex-compliant|Run schema validation and `eval describe --suite real`|M5|
|SC3 dependency discipline|New external deps|0 beyond vendored pexpect and transitive jsonschema|Review lock/dependency diff and PROVENANCE|M2|
|SC4 effort acknowledged|Estimate captured|~1,340 LOC harness + 15 eval bodies +150 LOC controls|Decision record and milestone summary review|M1|
|SC5 open questions resolved|Blocking OQs|All OQs resolved or explicitly moved to follow-up|Check per-milestone OQ tables before exit|M5|
|Doctor health|Preflight status|Green checklist on clean dev machine|`uv run superclaude eval doctor`|M4|
|Real subprocess validation|PTY eval run|E1 single eval runs through real Claude Code subprocess|`uv run superclaude eval run --suite real --eval E1`|M3|
|Sync validation|Source/dev copies|`make verify-sync` exits 0|Run after `make sync-dev`|M4|
|Exit semantics|Process codes|0/1/2/3 match status taxonomy|Automated exit-code tests|M4|
|Reporter invariant|Outcome count|`len(outcomes)==counts.expanded_n_prime`|Reporter contract tests|M4|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Execution model|Real Claude Code subprocess through PTY|In-process SDK client; command wrapper without PTY|PTY path is the only path that observes real terminal behavior and hook side effects|
|Concurrency model|ThreadPoolExecutor with default 8 and max 15|async/await; serial execution; distributed workers|Matches existing PRD executor pattern and bounds resource use on a single host|
|Isolation model|Per-eval HOME/session/state namespace under allowlisted scratch roots|Shared HOME; shared telemetry; repo-local only scratch|Security-critical prevention of user HOME mutation and concurrency state collisions|
|Validation order|Schema and ID validation before filesystem operations|Create run dir then validate; runner-level only validation|Prevents path traversal and avoids unsafe side effects from invalid manifests|
|Reporter contract|Report expanded N' including skipped outcomes|Report kept K only; omit skipped|Makes coverage and skip behavior falsifiable and prevents silent suite shrinkage|
|Scope boundary|Linux-local v1 with no CI integration|Cross-platform v1; CI-first run mode|Reduces PTY variance while proving harness semantics before platform expansion|
|MCP behavior|Soft-skip with --no-mcp plus explicit reachability checks|Hard-fail all MCP evals; silently skip|Keeps local run usable while preserving auditable skip reasons|
|Dependency policy|Vendored ptytest and existing/transitive libraries only|Add new test harness dependencies; use provider SDK|Controls supply-chain surface and keeps project dependency discipline intact|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|1 week|Week 1|Week 1|Decisions closed; CLI group; schema and ID validation|
|M2|1 week|Week 2|Week 2|HomeIsolation; capability gates; hook deployment; containment tests|
|M3|1 week|Week 3|Week 3|Real PTY runner; parallel orchestrator; disk/signal controls|
|M4|1 week|Week 4|Week 4|Reports; artifacts; exit semantics; sync validation|
|M5|2 weeks|Week 5|Week 6|15-eval suite; coverage gate; full local run; release evidence|

**Total estimated duration:** 6 weeks
