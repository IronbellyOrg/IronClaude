---
spec_source: "design-spec.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# IronClaude Real-Eval Harness — Project Roadmap

## Executive Summary

The Real-Eval Harness establishes a falsifiable, PTY-driven evaluation system for the IronClaude `claude` binary, replacing simulated/in-process testing with real subprocess execution under strict per-eval isolation. The architecture is a six-milestone rollout that begins with security-critical loader and isolation primitives, progresses through process orchestration and the assertion DSL, and concludes with eval-body authoring and a falsifiable hook-matcher coverage gate. The harness extends — never replaces — existing `IsolationLayers` (`cli/sprint/executor.py:107-182`), reuses `ClaudeProcess` (`cli/pipeline/process.py:24-150`), and integrates as an additive `superclaude eval` CLI group with zero new external Python dependencies beyond a vendored `pexpect` fork.

**Business Impact:** Eliminates the largest source of false-positive test signals in the IronClaude framework — synthetic SDK stand-ins that drift from real Claude Code behavior. Coverage gate (FR-G5) enforces that every PostToolUse hook matcher pattern in `~/.claude/settings.json` has at least one falsifying eval, making hook regressions provably detectable in CI. Single-command local runnability (FR-G6) makes the harness adoptable without infrastructure investment.

**Complexity:** HIGH (0.72) — subprocess + TTY orchestration (+0.20), concurrency model with up to 15 parallel real subprocesses (+0.10), security-critical path-traversal and HOME-containment surface (+0.15), integration with multiple stable internal APIs (+0.10), strict N′-vs-K reporter contract (+0.07), vendored ptytest ownership (+0.05), and three-tier capability gating (+0.05).

**Critical path:** EvalConfig + SuiteLoader → HomeIsolation (with path-containment guard) → PtyDriver → EvalRunner → RunOrchestrator → Reporter → ExpectDSL → CLI surface → eval bodies (E1–E15) → coverage gate enforcement. Security guards (FR-SCH2, FR-ISO2, NFR-SEC2/3) must land before any code path that writes to a per-eval HOME.

**Key architectural decisions:**

- Reuse `ThreadPoolExecutor + as_completed` pattern from `cli/prd/executor.py:774-802` rather than `execution/parallel.py`, matching the blocking-thread-per-eval design (AC6, AC8).
- Vendor `ptytest` under `cli/eval/pty/` rather than depending on PyPI; pin `pexpect>=4.9`, retain LICENSE, document drift in `PROVENANCE.md` (AC10, NFR-MAINT1).
- Per-eval HOME isolation extends rather than replaces `IsolationLayers` to preserve the four existing isolation guarantees (cwd, git ceiling, plugin dir, settings dir) while adding HOME, session_id, and time-offset layers (FR-ISO1).
- Reporter enforces `len(outcomes) == counts.expanded_n_prime` as a contract violation that exits 2 — N′ (post-expansion) is canonical, not K (kept subset) (FR-RPT1).

**Open risks requiring resolution before M1:**

- OQ-1, OQ-2, OQ-7 must be resolved before manifest schema can be frozen — the schema cannot validate evals whose shape (parameterize, `--junit` flag) is undefined.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation: Config, Schema, Security Loader|infrastructure|P0|L|none|18|HIGH|
|M2|Isolation & Process Layer|infrastructure|P0|L|M1|16|HIGH|
|M3|Execution Engine & Reporter|core|P0|XL|M2|17|MEDIUM|
|M4|Expect DSL & CLI Surface|integration|P0|L|M3|16|MEDIUM|
|M5|Eval Bodies & Coverage Gate|validation|P0|XL|M4|18|MEDIUM|
|M6|Docs, ADRs, Hardening, Sync|hardening|P1|M|M5|10|LOW|

## Dependency Graph

```
M1 (Foundation) → M2 (Isolation/Process) → M3 (Execution/Reporter) → M4 (DSL/CLI) → M5 (Evals/Coverage) → M6 (Hardening)

Within M1:  EvalConfig → SuiteLoader → eval_id regex guard → schema validator → capability gate scaffolding
Within M2:  HomeIsolation (extends IsolationLayers) → path-containment guard → PtyDriver (uses vendored ptytest) → PtyStream
Within M3:  EvalRunner (lifecycle) → RunOrchestrator (ThreadPoolExecutor) → disk-budget poller → Reporter (markdown/json/junit)
Within M4:  ExpectDSL primitives → eval_group Click commands (run/list/describe/doctor) → flag wiring
Within M5:  E1 (auggie coverage) → E2.{1,2,3} (matcher parameterize) → E3–E15 bodies → coverage gate enforcement
Within M6:  ADR sign-offs (D-5..D-8) → PROVENANCE.md → make sync-dev → make verify-sync gate
```

## M1: Foundation — Config, Schema, Security Loader

**Objective:** Establish the security-critical loader pipeline (eval_id regex guard, manifest schema validation, allowed scratch roots) and the configuration data model before any code path that writes to disk. | **Duration:** 4 days | **Entry:** Open questions OQ-1, OQ-2, OQ-7 resolved; ADR sign-offs scheduled. | **Exit:** `superclaude eval doctor` capability outline runs; schema validates the v1 manifest; eval_id regex rejects malformed IDs with exit 2 before any FS write.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-005|EvalConfig dataclass|Create dataclass holding paths, defaults, allowed_scratch_roots|config|-|frozen dataclass; fields paths,defaults,allowed_scratch_roots; default scratch roots include /tmp/eval-runs and repo .dev/eval-runs|S|P0|
|2|DM-011|Suite manifest YAML schema|Define JSON schema for suite manifest structure|loader|COMP-005|fields:name,version,description,defaults,required_binaries,optional_capabilities,evals[]; jsonschema-valid|M|P0|
|3|DM-002|EvalSpec model|Parsed manifest entry data model|loader|DM-011|fields:id,title,category,requires,timeout_sec,isolation,inputs,expects,parameterize|M|P0|
|4|FR-SCH1|Suite manifest schema validation|Load + validate YAML manifests against suite.schema.json using jsonschema|loader|DM-011,COMP-005|jsonschema validation runs in eval doctor and at top of eval run; schema violations exit 2|M|P0|
|5|FR-SCH2|Eval ID regex guard (security-critical)|Enforce `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` on every id including parameterize-expanded IDs|loader|FR-SCH1|regex applied pre-FS-write; InvalidEvalId raises exit 2; template tokens inside id rejected; parameterize expansion validated|M|P0|
|6|COMP-002|SuiteLoader|Reads YAML manifests; orchestrates schema + regex + capability gates|loader|FR-SCH2,COMP-010|loads suites/*.yaml; resolves capability gates; enforces eval_id regex; raises typed errors with exit 2|L|P0|
|7|NFR-SEC1|Eval ID path-traversal prevention test set|Negative-case tests proving ID regex blocks traversal patterns|loader|FR-SCH2|tests cover ../home, /etc, .., empty, leading-digit, template-token cases; all reject with InvalidEvalId|M|P0|
|8|DM-007|Capability dataclass|Capability descriptor with check callable + failure_mode|gates|-|fields:name,check,failure_mode(hard/skip/xfail),skip_flag,description; frozen dataclass|S|P0|
|9|DM-008|CapabilityReport|Per-capability status and blocked-evals listing|gates|DM-007|fields:report[],blocked_evals[];serializable to JSON|S|P0|
|10|COMP-009|CapabilityGates|check_all + which_or_skip + mcp_server_reachable|gates|DM-007,DM-008,OQ-5|claude/jq/make/git checked as HARD; MCP servers as SOFT-SKIP via --no-mcp; emits CapabilityReport|L|P0|
|11|FR-CLI4|`eval doctor` subcommand|Verify harness preconditions and emit capability report|cli|COMP-009,COMP-002|prints green checklist; checks claude PATH+min_version 0.5.0, jq/make/git, ~/.claude exists, ptytest vendored; emits coverage report|M|P0|
|12|NFR-MAINT1|Vendored ptytest fork setup|Fork ptytest under cli/eval/pty/ with LICENSE + PROVENANCE.md|deps|-|cli/eval/pty/ contains ptytest sources, upstream LICENSE retained, PROVENANCE.md documents fork SHA + changes; pexpect>=4.9 pinned|M|P0|
|13|AC3|Dependency boundary check|CI assertion that no new external Python deps land|deps|NFR-MAINT1|pyproject.toml unchanged except pexpect transitive via vendored ptytest; jsonschema confirmed as transitive|S|P0|
|14|AC10|ptytest fork SHA pin + drift policy|Document fork SHA freeze; quarterly review cadence|deps|NFR-MAINT1|PROVENANCE.md records SHA + review date; review cadence quarterly; resync procedure documented|S|P1|
|15|AC12|Allowed scratch roots enforcement|Codify `/tmp/eval-runs/`, repo `.dev/eval-runs/`, or `--output-dir` allowlist|config|COMP-005|EvalConfig.allowed_scratch_roots is the only source; rejection cases tested; --output-dir resolved against allowlist|M|P0|
|16|AC11|Source-of-truth discipline gate|CI check that all changes live under src/superclaude/|infra|-|make verify-sync passes; pre-commit hook rejects edits to .claude/ without sync-back|S|P0|
|17|FR-CLI2|`eval list` subcommand|Enumerate suites from cli/eval/suites/*.yaml|cli|COMP-002|lists all suite files; honors --json; prints name+version+eval count|S|P1|
|18|FR-CLI3|`eval describe` subcommand|Print manifest content for a suite or single eval|cli|COMP-002|--suite required; --eval optional; prints resolved (post-parameterize) manifest as YAML/JSON|S|P1|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|capability registry|registry|deferred|M1|COMP-009,COMP-002|
|schema file `suites/suite.schema.json`|file resource|wired|M1|FR-SCH1,COMP-002|
|`EvalConfig.allowed_scratch_roots`|allowlist|wired|M1|COMP-006,COMP-003|

### Milestone Dependencies — M1

- External: claude binary on PATH (min_version 0.5.0), jq, make, git available on Linux dev host.
- Internal: existing `cli/install_hooks.py` API surface (read-only consumption).

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-1|Remaining `decisions.md` open-question items (referenced by SC5)|Blocks ADR D-5..D-8 sign-off; blocks M6 exit|RyanW|before M1 exit|
|2|OQ-2|Concrete content of E3–E15 manifest entries|Schema must allow all eval shapes; blocks M1 schema freeze|RyanW|before M1 exit|
|3|OQ-7|Whether `--junit` flag is supported in CLI|Schema and CLI surface differ if --junit removed|RyanW|before M1 exit|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R7 — harness misconfigured against real `~/.claude/`|HIGH|LOW|Catastrophic — destroys maintainer env|HomeIsolation refuses HOME outside known scratch dirs; AC12 allowlist enforced in EvalConfig|architect|
|2|Eval ID regex bypass via parameterize expansion|HIGH|MEDIUM|Path traversal; FS write outside scratch|FR-SCH2 re-validates post-expansion IDs; negative test set in NFR-SEC1|architect|
|3|Schema drift between OQ-2 resolution and v1 freeze|MEDIUM|MEDIUM|Schema rejects valid evals or accepts invalid ones|Defer M1 exit until OQ-1/OQ-2/OQ-7 closed; schema version field in DM-011 for forward evolution|architect|

## M2: Isolation & Process Layer

**Objective:** Land HomeIsolation with defense-in-depth path containment, PtyDriver around the vendored ptytest, and the ANSI-aware stream layer — every component that touches the per-eval HOME or the real `claude` subprocess. | **Duration:** 5 days | **Entry:** M1 exit; security guards merged; ptytest vendored. | **Exit:** HomeIsolation refuses any HOME outside allowed scratch roots in unit tests; PtyDriver spawns real `claude` against a one-eval suite end-to-end; symlink-attack negative case covered.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|19|DM-006|HomeIsolation data record|Frozen dataclass capturing isolation state|isolation|-|fields:eval_id:str;home_root:Path;session_id:str;time_offset_sec:int=0|S|P0|
|20|COMP-012|IsolationLayers integration probe|Verify existing 4-layer isolation API surface remains stable|isolation|-|read-only smoke test pins API of cli/sprint/executor.py:107-182; failing on shape change|S|P0|
|21|FR-ISO1|HomeIsolation extends IsolationLayers|Add HOME override, CLAUDE_SESSION_ID stamp, optional CLAUDE_FAKE_TIME_OFFSET|isolation|COMP-012,DM-006|setup(),env(),teardown(keep),state_path(suffix) methods; per-eval HOMEs are sibling dirs under home_root; preserves 4 existing layers|L|P0|
|22|FR-ISO2|Path containment guard (security-critical)|Re-check eval_id regex; verify home_path.is_relative_to(scratch_root); resolve symlinks|isolation|FR-ISO1,AC12|raises HomeContainmentViolation if any check fails; symlink resolution AFTER creation BEFORE hook deploy; allowed prefix matches /tmp/eval-runs or repo .dev/eval-runs or --output-dir|L|P0|
|23|NFR-SEC2|HOME containment defense-in-depth|Layered guards on eval_id and scratch-root prefix|isolation|FR-ISO2|tests cover scratch-is-symlink-to-HOME attack; scratch-outside-allowlist; eval_id mutation post-construction|M|P0|
|24|NFR-SEC3|Hard guard against real `~/.claude/`|HomeIsolation.setup() refuses HOME outside known scratch dirs|isolation|FR-ISO2|tests prove setup() raises if HOME path resolves to real ~/.claude/; integration test attempts attack and confirms refusal|M|P0|
|25|COMP-006|HomeIsolation implementation|Full component with setup/env/teardown/state_path|isolation|FR-ISO1,FR-ISO2|methods setup,env→dict[str,str],teardown(keep),state_path(suffix)→Path; uses install_hooks under the hood|L|P0|
|26|NFR-ISO2|Atomic setup contract|try/except wrap; on exception after mkdtemp partial HOME preserved|isolation|COMP-006|status ERRORED set; keep=True forced; setup_failed artifact tag written; distinguishes harness bugs from eval failures|M|P0|
|27|COMP-014|install_hooks reuse adapter|Adapter calling existing cli/install_hooks.install_hooks|isolation|COMP-006|adapter signature matches install_hooks; targets per-eval HOME path; idempotent|S|P0|
|28|NFR-PERF1|HOME setup performance baseline|Measure per-eval HOME setup time and document budget|isolation|COMP-014|p50 ≤2s/eval at 15-eval parallel run; benchmark recorded in test report; reuses install_hooks optimizations|S|P1|
|29|COMP-007|PtyDriver wraps pexpect.spawn|expect_prompt_ready, inject_prompt, stdin/stdout, exit capture|process|NFR-MAINT1|methods expect_prompt_ready(timeout=),inject_prompt(text),write_stdin,read_stdout,wait_exit; uses vendored ptytest|L|P0|
|30|COMP-011|PtyStream ANSI/buffer layer|ANSI strip, line buffering, timeout handling|process|COMP-007|strips ANSI escape sequences; line-buffered iterator; raises PtyTimeout on stalled read|M|P0|
|31|COMP-013|ClaudeProcess reuse adapter|Wrap existing cli/pipeline/process.py:24-150 for spawn|process|COMP-007|spawns claude with HomeIsolation.env(); cwd pinned; preserves stdout/stderr separation|M|P0|
|32|FR-G1|Real Claude Code subprocess via PTY|End-to-end test driving real claude via PtyDriver|process|COMP-007,COMP-013|integration test spawns real claude binary; no in-process SDK shortcuts; full TTY transcript captured to artifact|L|P0|
|33|R1-mit|Claude version pin in eval doctor|Pin supported claude version range and enforce in doctor|process|FR-CLI4|min_version 0.5.0; max_version recorded; doctor fails closed on out-of-range|S|P0|
|34|R5-mit|Quarterly ptytest drift review checklist|Document review steps and target dates|process|AC10|CHECKLIST.md in cli/eval/pty/; review owner named; cadence quarterly|S|P2|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`HomeIsolation.env()` dict|env injector|wired|M2|COMP-013,COMP-007|
|`install_hooks` adapter|callback wiring|wired|M2|COMP-006|
|Vendored `pexpect.spawn` factory|process factory|wired|M2|COMP-007,COMP-011|

### Milestone Dependencies — M2

- M1 SuiteLoader + EvalConfig + capability gates merged.
- Existing `cli/sprint/executor.py:107-182` API unchanged.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-3|`--no-pty` flag exact eval exclusion set|Determines which evals are skipped under no-pty; affects PtyDriver bypass path|RyanW|before M2 exit|
|2|OQ-8|How Claude Code consumes `CLAUDE_FAKE_TIME_OFFSET`|If unsupported, time-offset layer becomes pass-through and is removed|RyanW|before M2 exit|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R1 — claude TTY behavior change breaks PtyDriver|HIGH|MEDIUM|Suite-wide failure across releases|Pin claude version range in doctor; capture full TTY transcripts as artifacts; isolate parsing in PtyStream|architect|
|2|Symlink attack: scratch dir is symlink to $HOME|HIGH|LOW|Catastrophic — destroys real HOME|FR-ISO2 resolves symlinks AFTER creation BEFORE hook deploy; explicit attack test in NFR-SEC2|architect|
|3|R8 — IsolationLayers shape changes|MEDIUM|LOW|Compile-time break of HomeIsolation extension|COMP-012 probe test pins API; vendor copy plan documented; pin tested SHA|architect|

## M3: Execution Engine & Reporter

**Objective:** Build the per-eval lifecycle, the parallel orchestrator, and the report writer with strict N′-vs-K contract enforcement. | **Duration:** 6 days | **Entry:** M2 exit; HomeIsolation + PtyDriver land. | **Exit:** RunOrchestrator runs a 3-eval suite in parallel; Reporter emits summary.md/json with `len(outcomes) == counts.expanded_n_prime` invariant enforced; SIGINT cancels in-flight evals and writes partial report.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|35|DM-001|EvalOutcome frozen dataclass|Per-eval outcome record emitted by EvalRunner|models|-|fields:eval_id:str;title:str;status:Literal[PASS,FAIL,ERRORED,TIMEOUT,INTERRUPTED,SKIPPED,XFAIL,XPASS];duration_sec:float;expects:list[ExpectResult];skip_reason:str|None;skip_flag_triggered:str|None;artifacts:dict[str,str];error_class:str|None|M|P0|
|36|DM-003|EvalResult model|Per-eval result record consumed by reporter|models|DM-001|fields:eval_id,outcome:EvalOutcome,start,end,duration_sec; serializable|S|P0|
|37|DM-005|ExpectFailure detail|Assertion failure detail record|models|-|fields:expect_name,expected,actual,message,traceback; one entry per failing Expect|S|P0|
|38|DM-009|ExpectResult record|Assertion outcome returned by ExpectCallable|models|-|fields:name,passed:bool,detail:ExpectFailure|None,duration_sec;serializable|S|P0|
|39|DM-010|EvalContext runtime record|Runtime context passed to ExpectCallable|models|DM-006|fields:eval_spec,home,artifacts_dir,jsonl_paths,exit_code,stdout,stderr,duration_sec;immutable view|M|P0|
|40|FR-LC1|EvalRunner lifecycle|build isolation→deploy hooks→spawn→inject→observe→assert→teardown|runner|COMP-006,COMP-013,DM-001|sequence executed per spec; ERRORED status on harness exception; PASS only when all Expects pass; teardown honors keep flag|L|P0|
|41|COMP-004|EvalRunner implementation|Full runner class wrapping FR-LC1|runner|FR-LC1,DM-010|emits EvalOutcome; logs to per-eval JSONL; respects per-eval timeout|L|P0|
|42|NFR-REL1|Signal handling + timeout enforcement|SIGINT/SIGTERM cancel; per-eval timeout kills + reaps|runner|COMP-004|SIGINT marks in-flight as INTERRUPTED;writes partial summary;exits 3;per-eval timeout kills PtyDriver+reaps zombie+marks TIMEOUT|M|P0|
|43|NFR-REL2|Bounded retry policy|Failed evals NOT retried by default; deterministic single-pass|runner|COMP-004|default no-retry; --eval subset re-run path documented; OQ-10 retry semantics gated to MCP-flaky tag only|S|P0|
|44|DM-004|RunSummary aggregate structure|Aggregate run summary data model|models|DM-001|fields:run_id,started_at,duration_sec,suite,manifest_version,parallel,counts,totals,evals[]; serializable|M|P0|
|45|DM-012|summary.json schema|Canonical machine-readable summary contract|reporter|DM-004|fields:run_id,started_at,duration_sec,suite,manifest_version,parallel,counts.{manifest_n,expanded_n_prime,kept_k,skipped_s,kept_plus_skipped_equals_n_prime},totals.{passed,failed,skipped,errored,interrupted,timeout},evals[]|M|P0|
|46|FR-RPT1|Aggregated Run Report|Emit summary.md, summary.json, optional junit.xml|reporter|DM-012,COMP-008|len(evals[])==counts.expanded_n_prime; SKIPPED rows included with skip_reason; mismatch raises ReporterContractViolation exit 2|L|P0|
|47|COMP-008|Reporter / AggregatedRunReport|to_markdown/to_yaml/to_json/to_junit methods|reporter|FR-RPT1,COMP-015|all 4 emitters implemented; assertion guard wired; pattern reference cli/sprint/executor.py:190-335|L|P0|
|48|COMP-015|AggregatedPhaseReport pattern probe|Pin shape reference for AggregatedRunReport|reporter|-|smoke test confirms shape; failing on upstream refactor|S|P1|
|49|COMP-003|RunOrchestrator|ThreadPoolExecutor+as_completed scheduler|orchestrator|COMP-004,DM-001|max_workers=8 default clamped[1,15]; per-eval timeout enforced; emits EvalOutcome per expanded spec; honors AC6 pattern|L|P0|
|50|FR-G2|Parallel execution of 15 evals|Run 15 evals in parallel with concurrency=8 default|orchestrator|COMP-003|integration test runs 15-eval suite at --parallel 8; strict isolation: own HOME, session_id, telemetry namespace; max=15 clamp enforced|L|P0|
|51|NFR-PERF2|Concurrency resource bounds verification|Document RAM ceiling at --parallel 15|orchestrator|FR-G2|benchmark confirms ≤2.25GB resident at --parallel 15;documented in PROVENANCE/perf-notes|S|P1|
|52|NFR-PERF4|Disk budget enforcement (--max-disk-mb)|Orchestrator polls disk every 5s; halts on breach|orchestrator|COMP-003|default 1024 MB; 0 disables; on breach: in-flight evals complete, no new evals scheduled, exit 2 with disk_budget_exceeded artifact|M|P0|
|53|NFR-ISO1|No shared mutable state at concurrency|Integration test asserting no shared state at max parallel|orchestrator|FR-G2|no shared HOME; no shared file handles (auggie-first.jsonl); no port collisions; test runs N×15 trials|M|P0|
|54|NFR-PERF3|Suite runtime target tracking|Track full-suite duration trend|orchestrator|FR-G2|baseline recorded; budget <10 min documented; --eval subset path documented|S|P2|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|EvalOutcome emission channel|callback wiring|wired|M3|COMP-008,COMP-003|
|Per-eval JSONL telemetry path|file resource|wired|M3|FR-EXP1,COMP-008|
|Disk-budget poller (5s tick)|background task|wired|M3|NFR-PERF4|
|SIGINT/SIGTERM handler|signal binding|wired|M3|NFR-REL1|

### Milestone Dependencies — M3

- M2 HomeIsolation + PtyDriver merged.
- Existing `cli/prd/executor.py:774-802` pattern available as reference.

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|N′-vs-K contract violation goes undetected|HIGH|MEDIUM|Reporter silently drops skipped evals; eval coverage misreported|FR-RPT1 enforces len(evals[])==counts.expanded_n_prime; ReporterContractViolation exits 2; integration test exercises the assertion|architect|
|2|R4 — Concurrent HOMEs exhaust disk|LOW|LOW|Run aborts mid-suite|--keep-home false default; NFR-PERF4 polls every 5s; budget recorded as artifact|architect|
|3|Signal race during teardown|MEDIUM|MEDIUM|Zombie processes; incomplete summary|NFR-REL1 reaps zombies before exit; partial summary always written; exit 3 dedicated to INTERRUPTED|architect|

## M4: Expect DSL & CLI Surface

**Objective:** Land the assertion DSL primitives (`Expect.*`) and complete the `superclaude eval` Click group with all flags wired. | **Duration:** 4 days | **Entry:** M3 exit; RunOrchestrator emits EvalOutcome end-to-end. | **Exit:** All seven Expect primitives covered by tests; `superclaude eval run --suite real` parses every documented flag; manifest `expects:` blocks executable in declarative and programmatic forms.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|55|FR-EXP1|Expect.* assertion DSL|Implement primitives Expect.file/jsonl/settings_json/exit_code/stderr/stdout/duration|dsl|DM-009,DM-010|each returns callable (EvalContext)->ExpectResult; declarative YAML form and programmatic form both supported; named arguments documented|L|P0|
|56|COMP-010|ExpectDSL static class|Fluent assertion DSL static methods returning typed Expect classes|dsl|FR-EXP1|class methods Expect.file,Expect.jsonl,Expect.settings_json,Expect.exit_code,Expect.stderr,Expect.stdout,Expect.duration; typed return classes; unit tests cover each|L|P0|
|57|COMP-010.1|Expect.file primitive|Assert file exists/content matches pattern|dsl|COMP-010|args path,exists,contains,regex,equals; ExpectResult includes diff on failure|S|P0|
|58|COMP-010.2|Expect.jsonl primitive|Assert JSONL entries match predicate|dsl|COMP-010|args path,line_count,filter,assert_each,assert_any; supports per-eval hook telemetry assertions|M|P0|
|59|COMP-010.3|Expect.settings_json primitive|Assert ~/.claude/settings.json shape|dsl|COMP-010|args path,key_path,equals,exists; resolves against HomeIsolation.home_path|S|P0|
|60|COMP-010.4|Expect.exit_code primitive|Assert subprocess exit code|dsl|COMP-010|args equals,in_set,not_equals;default equals 0|S|P0|
|61|COMP-010.5|Expect.stderr / stdout primitives|Assert TTY transcripts match patterns|dsl|COMP-010|args contains,regex,not_contains; operates on ANSI-stripped buffer from COMP-011|S|P0|
|62|COMP-010.6|Expect.duration primitive|Assert eval duration within bound|dsl|COMP-010|args max_sec,min_sec; informational PASS records duration even if outside bound when only one bound set|S|P1|
|63|COMP-001|eval_group Click commands|Top-level Click group exporting subcommands|cli|COMP-002,COMP-009|exports run,list,describe,doctor subcommands; group registered in superclaude entry point|M|P0|
|64|FR-G3|CLI integration (additive)|Plug into existing IronClaude CLI as `superclaude eval`|cli|COMP-001|no breaking changes to existing CLI; ~60% scaffolding reuse from cli/sprint, cli/prd, cli/pipeline documented; entry point registered|M|P0|
|65|FR-CLI1|`eval run` subcommand|Primary execution entry point with all flags|cli|COMP-001,COMP-003|flags --suite,--parallel,--eval,--no-mcp,--no-pty,--output-dir,--keep-home,--timeout-mult,--max-disk-mb,--json,--verbose all wired and validated|L|P0|
|66|FR-G6|Single-command local runnability|`uv run superclaude eval --suite real` succeeds on clean dev machine|cli|FR-CLI1|smoke test on clean Linux host completes 1-eval suite end-to-end with no manual setup beyond `make dev`|M|P0|
|67|FR-G4|Reproducible artifacts under `.dev/eval-runs/<ISO>/<run-id>/`|Per-run artifact layout|reporter|COMP-008|directory tree contains summary.{md,json}, junit.xml (when enabled), per-eval/{logs.jsonl,tty.transcript,artifacts/}|M|P0|
|68|FR-G5|Falsifiable hook-matcher coverage gate (CLI entry)|`eval doctor --check-coverage` and top-of-run gate|cli|COMP-009,FR-CLI4|gate computes matcher coverage map; FAILS run if any matcher P lacks corresponding eval; v1 coverage mcp__auggie__*,mcp__auggie-mcp__*,mcp__airis-mcp-gateway__*|L|P0|
|69|OQ-7-res|`--junit` flag wiring decision|Decide and implement --junit flag or remove from §9|cli|OQ-7|either --junit added to FR-CLI1 flag set with junit.xml emission, OR spec §9 corrected to remove conditional language; decision recorded in decisions.md|S|P0|
|70|OQ-3-res|`--no-pty` exclusion set|Enumerate evals excluded under --no-pty|cli|OQ-3|exclusion set written to suites/real.yaml as no_pty:skip tag per eval; --no-pty implementation honors tag; documented in eval describe output|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Click `eval_group` registry|registry|wired|M4|superclaude CLI entry|
|Expect callable dispatch|dispatch table|wired|M4|FR-LC1,COMP-004|
|`--no-mcp` skip flag|flag-driven gate|wired|M4|COMP-009|
|Coverage-gate hook matcher map|registry|wired|M4|FR-G5|

### Milestone Dependencies — M4

- M3 RunOrchestrator + Reporter merged.
- `~/.claude/settings.json` hook matcher patterns frozen for v1 (auggie + auggie-mcp + airis-mcp-gateway).

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-5|Exact MCP server reachability check semantics|`mcp_server_reachable("auggie")` contract undefined; affects gate behavior|RyanW|before M4 exit|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Flag drift between spec §4 and implementation|MEDIUM|MEDIUM|User-facing inconsistency; doctor reports wrong status|OQ-7 resolution gates M4 exit; CLI test exercises every documented flag; help text auto-validated|architect|
|2|Coverage gate false negatives (matcher in settings but no eval check)|HIGH|MEDIUM|Gate passes despite missing coverage|FR-G5 enumerates matchers from ~/.claude/settings.json at runtime; failing matcher emits `coverage_missing:<pattern>` artifact|architect|

## M5: Eval Bodies & Coverage Gate Enforcement

**Objective:** Author the 15 eval bodies (E1–E15), validate the coverage gate against a real `~/.claude/settings.json`, and prove the suite runs end-to-end at `--parallel 8`. | **Duration:** 7 days | **Entry:** M4 exit; DSL + CLI complete. | **Exit:** All 15 evals enumerate in `eval list`; coverage gate green for all three v1 matcher families; full suite completes <10 min on dev host.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|71|E1|Eval E1 — auggie matcher coverage|Issue real MCP tool call matching mcp__auggie__* pattern and assert hook telemetry|evals|FR-G5,COMP-010|inputs include real auggie tool invocation; expects Expect.jsonl asserts hook fired in per-eval hook log; tagged hook-coverage|M|P0|
|72|E2.1|Eval E2.1 — auggie-mcp parameterize|Parameterize entry for mcp__auggie-mcp__* matcher|evals|FR-G5,FR-SCH2|parameterize-expanded ID matches eval_id regex; hook telemetry asserted; tagged hook-coverage|M|P0|
|73|E2.2|Eval E2.2 — airis-mcp-gateway parameterize|Parameterize entry for mcp__airis-mcp-gateway__* matcher|evals|FR-G5,FR-SCH2|same as E2.1 for airis-mcp-gateway family|M|P0|
|74|E2.3|Eval E2.3 — third parameterized matcher entry|Parameterize entry covering remaining v1 hook|evals|FR-G5,FR-SCH2|covers third matcher in v1 set; hook telemetry asserted|M|P0|
|75|E3|Eval E3 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; minimum AC: passes deterministically on clean HOME|M|P0|
|76|E4|Eval E4 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|77|E5|Eval E5 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|78|E6|Eval E6 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|79|E7|Eval E7 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|80|E8|Eval E8 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|81|E9|Eval E9 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|82|E10|Eval E10 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|83|E11|Eval E11 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|84|E12|Eval E12 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|85|E13|Eval E13 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|86|E14|Eval E14 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|87|E15|Eval E15 — body TBD|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|88|SC2|Manifest schema covers all 15 evals|Validate all E1–E15 IDs match regex and load via schema|validation|FR-SCH1,FR-SCH2|all 15 IDs (including parameterize-expanded) pass eval_id regex; suite loads in eval doctor with zero violations|S|P0|
|89|R3-mit|MCP retry-once policy implementation|Per-eval retry-once on MCP-specific failure modes|orchestrator|OQ-10|MCP-flaky tag honored; retry attempted exactly once; failure tagged mcp_server_flaky in outcome.artifacts|M|P1|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Hook matcher → eval registry|registry|wired|M5|FR-G5|
|Per-eval hook telemetry path `~/.claude/logs/<hook>.jsonl`|file resource|wired|M5|COMP-010.2|
|MCP-flaky retry tag|callback wiring|wired|M5|R3-mit|

### Milestone Dependencies — M5

- M4 ExpectDSL + CLI merged.
- OQ-2 resolved for E3–E15 bodies.
- Real `~/.claude/settings.json` PostToolUse matchers frozen for v1.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-10|Exact retry semantics for MCP-flaky failures|Determines whether R3-mit lands as P0 or remains P1|RyanW|before M5 exit|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R3 — MCP server flakiness causes E1/E2 false failures|MEDIUM|MEDIUM|Suite is noisy; coverage gate misreports|R3-mit retry-once policy; mcp_server_flaky artifact tag; --no-mcp escape hatch|architect|
|2|R6 — 15-eval suite >10min adoption friction|MEDIUM|MEDIUM|Adoption drops; harness skipped in dev loops|--eval subset documented; follow-up suites/quick.yaml planned; perf budget tracked in M3 NFR-PERF3|architect|
|3|R9 — PR scope creep as evals are added|MEDIUM|HIGH|Review fatigue; merges delayed|Harness lands as PR 1 (M1–M4); evals as PR 2 in batches of 3-5; per-batch DoD recorded|architect|

## M6: Docs, ADRs, Hardening, Sync

**Objective:** Close decisions, complete documentation (ADRs D-5..D-8, PROVENANCE.md, NOTICE handling), enforce source-of-truth discipline (`make sync-dev` + `make verify-sync`), and prove single-command runnability on a clean dev machine. | **Duration:** 2 days | **Entry:** M5 exit; suite green at `--parallel 8`. | **Exit:** RyanW signs off ADRs; `make verify-sync` exits 0; SC1–SC5 satisfied; macOS roadmap entry recorded in decisions.md.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|90|SC1|ADR sign-offs D-5..D-8|RyanW signs off 4 original + 4 new ADRs in decisions.md|docs|OQ-1|decisions.md contains D-1..D-8 with sign-off date; OQ-1 resolution recorded; ADRs cross-reference roadmap deliverables|S|P0|
|91|OQ-4-res|NOTICE file for ptytest license attribution|Add top-level NOTICE if missing; reference ptytest|docs|NFR-MAINT1|NOTICE exists at repo root referencing ptytest LICENSE; decisions.md records D-? entry|S|P0|
|92|OQ-9-res|macOS support roadmap entry|Record macOS timeline in decisions.md|docs|-|decisions.md contains macOS follow-up entry with owner + target; AC1 reaffirmed for v1|S|P1|
|93|OQ-8-res|Time-offset mechanism contract|Document how Claude Code consumes CLAUDE_FAKE_TIME_OFFSET (or remove)|docs|OQ-8|decisions.md records either: (a) confirmation that claude binary honors env var, OR (b) removal of time-offset layer from FR-ISO1|S|P1|
|94|OQ-6-res|Suite naming convention beyond `real.yaml`|Document suite filename rules; record `quick.yaml` plan|docs|-|cli/eval/suites/README.md records naming convention; `quick.yaml` plan recorded as follow-up|S|P2|
|95|AC2|CI integration deferral note|Record deferral and follow-up trigger in decisions.md|docs|-|decisions.md entry says local-only for v1; trigger for CI revisit recorded|S|P2|
|96|AC1|Linux-only declaration|Record AC1 in decisions.md and README|docs|-|README documents Linux-only v1; eval doctor refuses non-Linux with friendly error|S|P0|
|97|SC4|Effort estimate acknowledgment|RyanW signs off LOC estimate ~1,340 harness + ~3,000-4,500 eval bodies|docs|SC1|decisions.md records signed-off estimate; ledger updated post-implementation with actual LOC|S|P1|
|98|SC5|Open-question list fully resolved|All 10 OQ-xxx items recorded as resolved in decisions.md|docs|OQ-1,OQ-2,OQ-3,OQ-4,OQ-5,OQ-6,OQ-7,OQ-8,OQ-9,OQ-10|every OQ-xxx has a `resolution:` field in decisions.md; signed-off by RyanW|M|P0|
|99|SC3|Zero-new-deps verification|Verify pyproject.toml has no new external deps beyond pexpect (vendored) + jsonschema (transitive)|docs|AC3|`uv pip list` diff post-implementation shows only ptytest-vendored sources changed; CI assertion enforces|S|P0|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`decisions.md` ADR ledger|file resource|wired|M6|SC1,SC5|
|`make verify-sync` CI gate|CI binding|wired|M6|AC11|
|`PROVENANCE.md` for vendored ptytest|file resource|wired|M6|NFR-MAINT1|

### Milestone Dependencies — M6

- M5 exit; eval suite green.
- All OQ-xxx items have resolution candidates from M1–M5.

### Risk Assessment and Mitigation — M6

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|ADR sign-off delay blocks release|MEDIUM|MEDIUM|M6 exit slips; harness ships without recorded decisions|SC1 owner named (RyanW); OQ resolutions tracked per-milestone, not deferred to M6|architect|
|2|Sync drift between `src/superclaude/` and `.claude/`|LOW|MEDIUM|Skill/agent edits land in `.claude/` only and are lost|`make verify-sync` runs in CI; pre-commit hook rejects unsynced changes (AC11)|architect|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|`claude` binary (min 0.5.0)|M2,M5|HARD|eval doctor fails closed with explicit error|
|`make` binary|M1,M6|HARD|eval doctor fails closed|
|`jq` binary|M1,M5|HARD|eval doctor fails closed|
|`git` binary|M1|HARD|eval doctor fails closed|
|`pexpect>=4.9` (via vendored ptytest)|M2|HARD|none — vendored fork is the source|
|`jsonschema` (transitive)|M1|HARD|none — already transitive|
|`click>=8.0.0`|M4|HARD|none — existing dep|
|`mcp_server.auggie`|M5|SOFT-SKIP|--no-mcp escape hatch; E1 marked SKIPPED|
|`mcp_server.auggie-mcp`|M5|SOFT-SKIP|--no-mcp escape hatch; E2.1 marked SKIPPED|
|`mcp_server.airis-mcp-gateway`|M5|SOFT-SKIP|--no-mcp escape hatch; E2.2 marked SKIPPED|
|`cli/sprint/executor.py:107-182` IsolationLayers|M2|HARD|COMP-012 probe pins shape; vendor copy plan documented|

### Infrastructure Requirements

- Linux dev host with min 4 GB free RAM (covers `--parallel 15` at ~2.25 GB plus headroom).
- ~2 GB free disk under `/tmp` or repo `.dev/` for per-run scratch (default `--max-disk-mb 1024`).
- Read access to `~/.claude/settings.json` for coverage-gate matcher enumeration (read-only — never written by harness).
- TTY-capable shell (xterm-compatible) for pexpect; CI runners without TTY emulation require `--no-pty` mode.
- `uv` available for `uv run superclaude eval` single-command path.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R1|Claude Code TTY behavior changes between versions breaks PtyDriver|M2,M5|MEDIUM|HIGH|Pin claude version range in eval doctor (min 0.5.0); capture full TTY transcripts as artifacts; isolate parsing in PtyStream|architect|
|R2|Per-eval HOME setup slow at 15-eval parallel|M2|MEDIUM|MEDIUM|Reuse `install_hooks.py` optimizations; NFR-PERF1 records baseline; ~1.4s/eval budget acceptable|architect|
|R3|MCP server flakiness causes E1/E2 false failures|M5|MEDIUM|MEDIUM|Per-eval retry-once on MCP-specific failure modes (R3-mit, deliverable 89); mcp_server_flaky artifact tag; --no-mcp escape hatch|architect|
|R4|Concurrent HOMEs exhaust disk|M3|LOW|LOW|`--keep-home false` default; NFR-PERF4 polls disk every 5s with default 1024MB budget; exit 2 on breach|architect|
|R5|Ptytest fork drifts from upstream pexpect|M2,M6|LOW|LOW|Quarterly review of pexpect releases (AC10); resync procedure in PROVENANCE.md; pinned SHA|architect|
|R6|15-eval suite exceeds 10-min adoption budget|M3,M5|MEDIUM|MEDIUM|`--eval` subset; future `suites/quick.yaml`; per-suite duration recorded as artifact|architect|
|R7|Maintainer runs harness against real `~/.claude/`|M1,M2|LOW|HIGH|Hard guard in HomeIsolation.setup() refusing HOME outside known scratch dirs (NFR-SEC3); AC12 allowlist enforced|architect|
|R8|`IsolationLayers` shape changes breaking extension|M2|LOW|MEDIUM|COMP-012 probe test pins API; vendor copy plan documented; SHA pin recorded|architect|
|R9|PR scope creep as evals are added|M5|HIGH|MEDIUM|Harness lands as PR 1 (M1–M4); evals as PR 2 in batches of 3-5; per-batch DoD recorded|architect|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC1: Maintainer sign-off on ADRs|ADR ledger entries signed|D-1..D-8 all signed|`decisions.md` review checklist; signed-off field per ADR|M6|
|SC2: Manifest schema covers all 15 evals|Schema-valid eval IDs|15/15 IDs pass schema + regex|`eval doctor` zero violations on real.yaml|M5|
|SC3: Zero new external Python deps|pyproject.toml diff|0 new external imports beyond transitive jsonschema|`uv pip list` snapshot compared pre/post|M1,M6|
|SC4: Effort estimate acknowledged|LOC actual vs estimate|±15% of ~1,340 harness + 3,000-4,500 evals|Post-implementation LOC count vs decisions.md estimate|M6|
|SC5: Open-question list resolved|OQ-xxx resolutions|10/10 OQ-xxx have resolution field|`decisions.md` checklist; cross-reference per-milestone OQ tables|M6|
|Exit code semantics|Exit code dispatch|0/1/2/3 per spec|Integration test exercises each exit path|M3|
|Reporter contract invariant|`len(outcomes) == counts.expanded_n_prime`|Always equal; mismatch exits 2|`ReporterContractViolation` test|M3|
|Hook matcher coverage|Matchers with eval coverage|3/3 v1 families covered (auggie, auggie-mcp, airis-mcp-gateway)|`eval doctor --check-coverage` green|M5|
|Single-command runnability|`uv run superclaude eval --suite real` success on clean host|Exit 0 on green path|Fresh container/VM smoke test|M5|
|Suite runtime budget|Full suite wall-clock at `--parallel 8`|<10 min|Captured in summary.json `duration_sec`|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|Subprocess driving model|Real `claude` via PTY (pexpect)|in-process SDK client; CLI invocation without TTY|Goal 1 requires falsifiable end-to-end behavior; SDK shortcuts drift from real binary; TTY semantics necessary for prompt-ready detection|
|Parallelism primitive|`ThreadPoolExecutor + as_completed` (AC6)|`execution/parallel.py`; asyncio; multiprocessing|Blocking-thread-per-eval matches per-eval PTY model (AC8); reuses proven pattern from `cli/prd/executor.py:774-802`; no async/await complexity|
|Isolation strategy|Extend existing `IsolationLayers`|Replace; reimplement from scratch|Preserves 4 existing isolation guarantees; lower regression risk vs replacement; aligns with AC5|
|ptytest dependency model|Vendored fork under `cli/eval/pty/`|PyPI dep; pexpect direct usage|Bus-factor mitigation; fork SHA pinning; AC3 forbids new external deps|
|Reporter contract|`len(outcomes) == counts.expanded_n_prime`; mismatch exits 2|Soft warning; tolerate drift|N′ vs K dimensional invariant is the only way to detect silent eval drops; exit 2 forces investigation|
|Capability gating tiers|HARD / SOFT-SKIP / SOFT-XFAIL|Binary present/absent|Three tiers express the policy difference between missing toolchain (HARD) and missing optional MCP server (SOFT)|
|Retry policy|No retry by default; MCP-flaky retry-once|Unlimited retry; configurable retry|Determinism > tolerance; MCP exception scoped to R3 mitigation only|
|Output sink|`.dev/eval-runs/<ISO>/<run-id>/`|`docs/generated/`; `~/.claude/eval-runs/`|`.dev/` is the conventional scratch root; aligns with CLAUDE.md AC12 allowlist; never under `.claude/` (override rule)|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|4 days|Day 1|Day 4|Loader + EvalConfig + capability gate skeleton + eval doctor outline|
|M2|5 days|Day 5|Day 9|HomeIsolation + path-containment + PtyDriver + PtyStream|
|M3|6 days|Day 10|Day 15|EvalRunner + RunOrchestrator + Reporter + disk-budget poller|
|M4|4 days|Day 16|Day 19|Expect DSL primitives + eval_group CLI + all flags wired|
|M5|7 days|Day 20|Day 26|E1–E15 eval bodies + coverage gate + full-suite green|
|M6|2 days|Day 27|Day 28|ADR sign-offs + PROVENANCE.md + NOTICE + sync-verify gate|

**Total estimated duration:** 28 working days (~5.5 calendar weeks at single-engineer pace; ~3.5 days harness work as design-spec §0 budgets + ~1–2 weeks evals + ~0.5 week docs)
