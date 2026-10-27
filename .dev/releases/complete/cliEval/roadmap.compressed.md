---
spec_source: "design-spec.compressed.md"
complexity_score: 0.72
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "opus"
variant_scores: "opus:82 haiku:74"
convergence_score: 0.78
---

# IronClaude Real-Eval Harness — Project Roadmap

## Executive Summary

The Real-Eval Harness establishes a falsifiable, PTY-driven evaluation system for the IronClaude `claude` binary, replacing simulated/in-process testing with real subprocess execution under strict per-eval isolation. The architecture is a six-milestone rollout that begins with security-critical loader, configuration, and DSL-interface primitives, progresses through isolation, process orchestration, the reporter contract, and full CLI surface, and concludes with eval-body authoring, a falsifiable hook-matcher coverage gate, and release hardening. The harness extends — never replaces — existing `IsolationLayers` (`cli/sprint/executor.py:107-182`), reuses `ClaudeProcess` (`cli/pipeline/process.py:24-150`), and integrates as an additive `superclaude eval` CLI group with zero new external Python dependencies beyond a vendored `pexpect` fork.

**Business Impact:** Eliminates the largest source of false-positive test signals in the IronClaude framework — synthetic SDK stand-ins that drift from real Claude Code behavior. Coverage gate (FR-G5) enforces that every PostToolUse hook matcher pattern in `~/.claude/settings.json` has at least one falsifying eval, making hook regressions provably detectable. Single-command local runnability (FR-G6) makes the harness adoptable without infrastructure investment.

**Complexity:** HIGH (0.72) — subprocess + TTY orchestration (+0.20), concurrency model with up to 15 parallel real subprocesses (+0.10), security-critical path-traversal and HOME-containment surface (+0.15), integration with multiple stable internal APIs (+0.10), strict N′-vs-K reporter contract (+0.07), vendored ptytest ownership (+0.05), and three-tier capability gating (+0.05).

**Critical path:** EvalConfig + SuiteLoader + ExpectDSL interface → HomeIsolation (with path-containment guard) + ptytest vendoring → PtyDriver → EvalRunner → RunOrchestrator → Reporter → Expect primitives + CLI surface → eval bodies (E1–E15) → coverage gate enforcement → ADR/PROVENANCE/NOTICE hardening. Security guards (FR-SCH2, FR-ISO2, NFR-SEC2/3) must land before any code path that writes to a per-eval HOME. Schema and ID validation precede every filesystem write (Validation-Order decision).

**Key architectural decisions:**

- Reuse `ThreadPoolExecutor + as_completed` pattern from `cli/prd/executor.py:774-802` rather than `execution/parallel.py`, matching the blocking-thread-per-eval design (AC6, AC8).
- Vendor `ptytest` under `cli/eval/pty/` rather than depending on PyPI; pin `pexpect>=4.9`, retain LICENSE, document drift in `PROVENANCE.md` (AC10, NFR-MAINT1).
- Per-eval HOME isolation extends rather than replaces `IsolationLayers` to preserve the four existing isolation guarantees (cwd, git ceiling, plugin dir, settings dir) while adding HOME, session_id, and time-offset layers (FR-ISO1).
- Reporter enforces `len(outcomes) == counts.expanded_n_prime` as a contract violation that exits 2 — N′ (post-expansion) is canonical, not K (kept subset) (FR-RPT1).
- DSL interface (COMP-010) lands in M1 so manifest authors can shape `expects:` blocks early; primitives (COMP-010.1–6) land in M4 with backing `EvalContext`.

**Open risks requiring resolution before M1:**

- OQ-1, OQ-2, OQ-7 must be resolved before manifest schema can be frozen — the schema cannot validate evals whose shape (parameterize, `--junit` flag) is undefined. OQ-4 (NOTICE/LICENSE for ptytest) must be resolved before M2 entry (before vendored sources physically land).

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation: Config, Schema, DSL Interface, Security Loader|infrastructure|P0|L|none|22|HIGH|
|M2|Isolation, Process Layer, Vendored ptytest|infrastructure|P0|L|M1|18|HIGH|
|M3|Execution Engine & Reporter|core|P0|XL|M2|19|MEDIUM|
|M4|Expect Primitives & CLI Surface|integration|P0|L|M3|17|MEDIUM|
|M5|Eval Bodies, Coverage Gate, Rollout Plan|validation|P0|XL|M4|22|MEDIUM|
|M6|Docs, ADRs, Hardening, Sync, Platform Roadmap|hardening|P1|M|M5|12|LOW|

## Dependency Graph

```
M1 (Foundation) → M2 (Isolation/Process) → M3 (Execution/Reporter) → M4 (Primitives/CLI) → M5 (Evals/Coverage) → M6 (Hardening)

Within M1:  EvalConfig → SuiteLoader → eval_id regex guard → schema validator → DSL interface (COMP-010) → capability gate outline
Within M2:  OQ-4 closed → ptytest vendored → HomeIsolation (extends IsolationLayers) → path-containment guard → PtyDriver → PtyStream
Within M3:  EvalRunner (lifecycle) → RunOrchestrator (ThreadPoolExecutor) → disk-budget poller → Reporter (markdown/json/junit)
Within M4:  Expect primitives (COMP-010.1–6) → eval_group Click commands (run/list/describe/doctor) → flag wiring → coverage-gate CLI entry
Within M5:  E1 (auggie coverage) → E2.{1,2,3} (matcher parameterize) → E3–E15 bodies → coverage gate enforcement → MIG-002 batch plan
Within M6:  ADR sign-offs (D-5..D-8) → PROVENANCE.md → MIG-003 macOS roadmap → make sync-dev → make verify-sync gate
```

## M1: Foundation — Config, Schema, DSL Interface, Security Loader

**Objective:** Establish the security-critical loader pipeline (eval_id regex guard, manifest schema validation, allowed scratch roots), the configuration data model, and the ExpectDSL public interface before any code path that writes to disk. | **Duration:** 4 days | **Entry:** Open questions OQ-1, OQ-2, OQ-3, OQ-7, OQ-8, OQ-10 resolved or scheduled; ADR sign-offs queued. | **Exit:** `superclaude eval doctor` capability outline runs; schema validates the v1 manifest; eval_id regex rejects malformed IDs with exit 2 before any FS write; DSL interface (COMP-010) is importable and exercised by unit tests against synthetic `EvalContext`.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|COMP-005|EvalConfig dataclass|Create dataclass holding paths, defaults, allowed_scratch_roots|config|-|frozen dataclass; fields paths,defaults,allowed_scratch_roots; default scratch roots include /tmp/eval-runs and repo .dev/eval-runs|S|P0|
|2|DM-011|Suite manifest YAML schema|Define JSON schema for suite manifest structure|loader|COMP-005|fields:name,version,description,defaults,required_binaries,optional_capabilities,evals[]; parameterize accepted; unknown required fields rejected; jsonschema-valid|M|P0|
|3|DM-002|EvalSpec model|Parsed manifest entry data model|loader|DM-011|fields:id,title,category,requires,timeout_sec,isolation,inputs,expects,parameterize|M|P0|
|4|FR-SCH1|Suite manifest schema validation|Load + validate YAML manifests against suite.schema.json using jsonschema|loader|DM-011,COMP-005|jsonschema validation runs in eval doctor and at top of eval run; schema violations exit 2; error names field path|M|P0|
|5|FR-SCH2|Eval ID regex guard (security-critical)|Enforce `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` on every id including parameterize-expanded IDs|loader|FR-SCH1|regex applied pre-FS-write; InvalidEvalId raises exit 2; template tokens inside id rejected; parameterize expansion validated|M|P0|
|6|COMP-002|SuiteLoader|Reads YAML manifests; orchestrates schema + regex + capability gates|loader|FR-SCH2,COMP-010|loads suites/*.yaml; resolves capability gates; enforces eval_id regex; raises typed errors with exit 2|L|P0|
|7|NFR-SEC1|Eval ID path-traversal prevention test set|Negative-case tests proving ID regex blocks traversal patterns|loader|FR-SCH2|tests cover ../home, /etc, .., empty, leading-digit, template-token, parameterized-unsafe cases; all reject with InvalidEvalId|M|P0|
|8|DM-007|Capability dataclass|Capability descriptor with check callable + failure_mode|gates|-|fields:name,check,failure_mode(hard/skip/xfail),skip_flag,description; frozen dataclass|S|P0|
|9|DM-008|CapabilityReport|Per-capability status and blocked-evals listing|gates|DM-007|fields:report[],blocked_evals[],skip_flags[],hard_failures[],soft_skips[],soft_xfails[]; serializable to JSON|S|P0|
|10|COMP-009|CapabilityGates|check_all + which_or_skip + mcp_server_reachable|gates|DM-007,DM-008,OQ-5|claude/jq/make/git checked as HARD; MCP servers as SOFT-SKIP via --no-mcp; emits CapabilityReport|L|P0|
|11|FR-CLI4|`eval doctor` subcommand|Verify harness preconditions and emit capability report|cli|COMP-009,COMP-002|prints green checklist; checks claude PATH+min_version 0.5.0, jq/make/git, ~/.claude exists, ptytest vendored; emits coverage report|M|P0|
|12|COMP-010|ExpectDSL interface|Define the fluent and declarative assertion DSL interface consumed by manifests and runner|dsl|FR-SCH1|file:cli/eval/expect.py; methods:file,jsonl,settings_json,exit_code,stderr,stdout,duration; returns ExpectCallable; YAML mapping supported; primitives deferred to M4|M|P0|
|13|DM-009|ExpectResult record|Assertion outcome returned by ExpectCallable|models|COMP-010|fields:name,passed:bool,message,details,duration_sec,failure:ExpectFailure|None;serializable|S|P0|
|14|DM-005|ExpectFailure detail|Assertion failure detail record|models|COMP-010|fields:eval_id,expect_id,expect_name,expected,actual,message,artifact_ref,traceback; one entry per failing Expect|S|P0|
|15|AC3|Dependency boundary check|CI assertion that no new external Python deps land|deps|-|pyproject.toml unchanged except pexpect transitive via vendored ptytest; jsonschema confirmed as transitive|S|P0|
|16|AC12|Allowed scratch roots enforcement|Codify `/tmp/eval-runs/`, repo `.dev/eval-runs/`, or `--output-dir` allowlist|config|COMP-005|EvalConfig.allowed_scratch_roots is the only source; rejection cases tested; --output-dir resolved against allowlist|M|P0|
|17|AC11|Source-of-truth discipline gate|CI check that all changes live under src/superclaude/|infra|-|make verify-sync passes; pre-commit hook rejects edits to .claude/ without sync-back|S|P0|
|18|FR-CLI2|`eval list` subcommand|Enumerate suites from cli/eval/suites/*.yaml|cli|COMP-002|lists all suite files; honors --json; prints name+version+eval count; handles empty directory; exits 0|S|P1|
|19|FR-CLI3|`eval describe` subcommand|Print manifest content for a suite or single eval|cli|COMP-002,FR-SCH1|--suite required; --eval optional; validates before print; prints resolved (post-parameterize) manifest as YAML/JSON|S|P1|
|20|TEST-001|Schema and ID rejection tests|First-class test deliverable: schema errors, unsafe IDs, parameterized IDs, preflight ordering|tests|FR-SCH1,FR-SCH2|invalid schema exits 2; unsafe id exits 2; no FS writes before rejection; parameterize expansion tested; cross-links NFR-SEC1|M|P0|
|21|OPS-001|Decision record closure|Record decisions for ADR sign-off, PTY flag semantics, JUnit flag, time offset, retry, NOTICE handling in decisions.md|ops|OQ-1,OQ-3,OQ-7,OQ-8,OQ-10|decisions.md updated; D-5..D-8 queued for sign-off; unresolved blockers listed; implementation gates reference decisions|S|P0|
|22|FR-G3|Additive CLI integration registration|Register `superclaude eval` command family without breaking existing commands|cli|COMP-002|entrypoint registered; existing commands unchanged; command help lists eval group; source under src/superclaude|M|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|capability registry|registry|deferred|M1|COMP-009,COMP-002|
|schema file `suites/suite.schema.json`|file resource|wired|M1|FR-SCH1,COMP-002|
|`EvalConfig.allowed_scratch_roots`|allowlist|wired|M1|COMP-006,COMP-003|
|`Expect.*` YAML mapping|strategy table|wired|M1|COMP-010,COMP-004|
|`superclaude eval` Click group|registry|deferred|M1|COMP-001 (M4)|

### Milestone Dependencies — M1

- External: claude binary on PATH (min_version 0.5.0), jq, make, git available on Linux dev host.
- Internal: existing `cli/install_hooks.py` API surface (read-only consumption).
- Process: maintainer (RyanW) available to sign off OPS-001 decision entries.

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-1|Remaining `decisions.md` open-question items (referenced by SC5)|Blocks ADR D-5..D-8 sign-off; blocks M6 exit|RyanW|before M1 exit|
|2|OQ-2|Concrete content of E3–E15 manifest entries|Schema must allow all eval shapes; blocks M1 schema freeze and M5 eval bodies|RyanW|before M1 exit (schema), before M5 entry (bodies)|
|3|OQ-3|Which eval categories are excluded by `--no-pty`|Blocks run-flag semantics in M4|architect|before FR-CLI1 close (M4)|
|4|OQ-7|Whether `--junit` flag is supported in CLI|Schema and CLI surface differ if --junit removed|RyanW|before M1 exit|
|5|OQ-8|How `CLAUDE_FAKE_TIME_OFFSET` is consumed or validated|EvalConfig + HomeIsolation contract|architect|before COMP-005 close|
|6|OQ-10|Exact MCP-specific failure taxonomy permitting retry-once|Capability + retry policy|QA Lead|before M3 exit (empirical resolution acceptable per debate D5)|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R7 — harness misconfigured against real `~/.claude/`|HIGH|LOW|Catastrophic — destroys maintainer env|HomeIsolation refuses HOME outside known scratch dirs; AC12 allowlist enforced in EvalConfig|architect|
|2|Eval ID regex bypass via parameterize expansion|HIGH|MEDIUM|Path traversal; FS write outside scratch|FR-SCH2 re-validates post-expansion IDs; negative test set in NFR-SEC1 and TEST-001|architect|
|3|Schema drift between OQ-2 resolution and v1 freeze|MEDIUM|MEDIUM|Schema rejects valid evals or accepts invalid ones|Defer M1 exit until OQ-1/OQ-2/OQ-7 closed; schema version field in DM-011 for forward evolution|architect|
|4|RR-001 — Unresolved decisions cause contract churn after implementation begins|HIGH|MEDIUM|CLI flags, schema, reports may need rework|Close OQ-1/OQ-3/OQ-7/OQ-8 before M1 exit; OQ-10 may resolve empirically in M3/M5|architect|

## M2: Isolation, Process Layer, Vendored ptytest

**Objective:** Land HomeIsolation with defense-in-depth path containment, the vendored ptytest fork (with attribution complete), PtyDriver, and the ANSI-aware stream layer — every component that touches the per-eval HOME or the real `claude` subprocess. | **Duration:** 5 days | **Entry:** M1 exit; security guards merged; OQ-4 resolved (NOTICE/LICENSE attribution complete before vendored ptytest sources physically land); OQ-5 resolved (MCP reachability contract). | **Exit:** HomeIsolation refuses any HOME outside allowed scratch roots in unit tests; PtyDriver spawns real `claude` against a one-eval suite end-to-end; symlink-attack negative case covered; PROVENANCE.md records vendored ptytest SHA.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|23|NFR-MAINT1|Vendored ptytest fork setup|Fork ptytest under cli/eval/pty/ with LICENSE + PROVENANCE.md|deps|DOC-OQ4|cli/eval/pty/ contains ptytest sources; upstream LICENSE retained; PROVENANCE.md documents fork SHA + changes; pexpect>=4.9 pinned|M|P0|
|24|DOC-OQ4|NOTICE/LICENSE attribution for ptytest|M2 entry blocker (per debate D6 convergence): NOTICE at repo root references ptytest LICENSE|docs|OQ-4|NOTICE exists at repo root referencing ptytest LICENSE; decisions.md records D-? entry; resolved before NFR-MAINT1 lands vendored sources|S|P0|
|25|AC10|ptytest fork SHA pin + drift policy|Document fork SHA freeze; quarterly review cadence|deps|NFR-MAINT1|PROVENANCE.md records SHA + review date; review cadence quarterly; resync procedure documented; CHECKLIST.md in cli/eval/pty/|S|P1|
|26|DM-006|HomeIsolation data record|Frozen dataclass capturing isolation state|isolation|-|fields:eval_id:str;home_root:Path;session_id:str;time_offset_sec:int=0|S|P0|
|27|COMP-012|IsolationLayers integration probe|Verify existing 4-layer isolation API surface remains stable|isolation|-|read-only smoke test pins API of cli/sprint/executor.py:107-182; failing on shape change|S|P0|
|28|FR-ISO1|HomeIsolation extends IsolationLayers|Add HOME override, CLAUDE_SESSION_ID stamp, optional CLAUDE_FAKE_TIME_OFFSET|isolation|COMP-012,DM-006|setup(),env(),teardown(keep),state_path(suffix) methods; per-eval HOMEs are sibling dirs under home_root; preserves 4 existing layers|L|P0|
|29|FR-ISO2|Path containment guard (security-critical)|Re-check eval_id regex; verify home_path.is_relative_to(scratch_root); resolve symlinks|isolation|FR-ISO1,AC12|raises HomeContainmentViolation if any check fails; symlink resolution AFTER creation BEFORE hook deploy; allowed prefix matches /tmp/eval-runs or repo .dev/eval-runs or --output-dir|L|P0|
|30|NFR-SEC2|HOME containment defense-in-depth|Layered guards on eval_id and scratch-root prefix|isolation|FR-ISO2|tests cover scratch-is-symlink-to-HOME attack; scratch-outside-allowlist; eval_id mutation post-construction; loader-bypass still rejected|M|P0|
|31|NFR-SEC3|Hard guard against real `~/.claude/`|HomeIsolation.setup() refuses HOME outside known scratch dirs|isolation|FR-ISO2|tests prove setup() raises if HOME path resolves to real ~/.claude/; integration test attempts attack and confirms refusal|M|P0|
|32|COMP-006|HomeIsolation implementation|Full component with setup/env/teardown/state_path|isolation|FR-ISO1,FR-ISO2|methods setup,env→dict[str,str],teardown(keep),state_path(suffix)→Path; uses install_hooks under the hood|L|P0|
|33|NFR-ISO2|Atomic setup contract|try/except wrap; on exception after mkdtemp partial HOME preserved|isolation|COMP-006|status ERRORED set; keep=True forced; setup_failed artifact tag written; distinguishes harness bugs from eval failures|M|P0|
|34|COMP-014|install_hooks reuse adapter|Adapter calling existing cli/install_hooks.install_hooks|isolation|COMP-006|adapter signature matches install_hooks; targets per-eval HOME path; idempotent; no direct real-HOME writes; errors tagged|S|P0|
|35|NFR-PERF1|HOME setup performance baseline|Measure per-eval HOME setup time and document budget|isolation|COMP-014|p50 ≤2s/eval at 15-eval parallel run; ~1.4s/eval target; benchmark recorded in test report; reuses install_hooks optimizations|S|P1|
|36|COMP-007|PtyDriver wraps pexpect.spawn|expect_prompt_ready, inject_prompt, stdin/stdout, exit capture|process|NFR-MAINT1|methods expect_prompt_ready(timeout=),inject_prompt(text),write_stdin,read_stdout,wait_exit; uses vendored ptytest|L|P0|
|37|COMP-011|PtyStream ANSI/buffer layer|ANSI strip, line buffering, timeout handling|process|COMP-007|strips ANSI escape sequences; line-buffered iterator; raises PtyTimeout on stalled read|M|P0|
|38|COMP-013|ClaudeProcess reuse adapter|Wrap existing cli/pipeline/process.py:24-150 for spawn|process|COMP-007|spawns claude with HomeIsolation.env(); cwd pinned; preserves stdout/stderr separation; no in-process SDK path|M|P0|
|39|R1-mit|Claude version pin in eval doctor|Pin supported claude version range and enforce in doctor|process|FR-CLI4|min_version 0.5.0; max_version recorded; doctor fails closed on out-of-range|S|P0|
|40|TEST-002|Containment unit tests|First-class test deliverable: allowed roots, rejected roots, loader-bypass defense at HomeIsolation|tests|FR-ISO2,NFR-SEC2|repo .dev accepted; /tmp accepted; non-allowlisted root rejected; loader bypass rejected; exit code 2 path covered|M|P0|
|41|TEST-003|Symlink attack tests|First-class test deliverable: symlink resolution catches scratch and HOME escape attempts after creation|tests|FR-ISO2,NFR-SEC3|scratch symlink to real HOME rejected; nested symlink escape rejected; partial HOME preserved; setup_failed tag asserted|M|P0|
|42|TEST-004|Capability gate tests|Validate hard, skip, xfail capability classifications including --no-mcp behavior|tests|COMP-009|missing claude hard fails; --no-mcp soft-skips MCP evals; xfail supported; doctor renders statuses|M|P0|
|43|OPS-002|Scratch root policy enforcement|Document and enforce allowed scratch roots across config, isolation, and CLI output-dir|ops|COMP-005,FR-ISO2|/tmp/eval-runs; repo .dev/eval-runs; resolved --output-dir allowlist; policy appears in doctor failures|S|P0|
|44|R5-mit|Quarterly ptytest drift review checklist|Document review steps and target dates|process|AC10|CHECKLIST.md in cli/eval/pty/; review owner named; cadence quarterly|S|P2|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`HomeIsolation.env()` dict|env injector|wired|M2|COMP-013,COMP-007|
|`install_hooks` adapter|callback wiring|wired|M2|COMP-006|
|Vendored `pexpect.spawn` factory|process factory|wired|M2|COMP-007,COMP-011|
|Scratch-root allowlist|policy registry|wired|M2|COMP-005,COMP-006|

### Milestone Dependencies — M2

- M1 SuiteLoader + EvalConfig + capability gates + DSL interface merged.
- OQ-4 closed: NOTICE/LICENSE attribution complete before vendored ptytest sources physically land (debate D6 convergence).
- Existing `cli/sprint/executor.py:107-182` API unchanged.

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-5|Exact MCP server reachability check semantics|`mcp_server_reachable("auggie")` contract undefined; affects gate behavior|architect|before COMP-009 close (M2)|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R1 — claude TTY behavior change breaks PtyDriver|HIGH|MEDIUM|Suite-wide failure across releases|Pin claude version range in doctor; capture full TTY transcripts as artifacts; isolate parsing in PtyStream|architect|
|2|Symlink attack: scratch dir is symlink to $HOME|HIGH|LOW|Catastrophic — destroys real HOME|FR-ISO2 resolves symlinks AFTER creation BEFORE hook deploy; explicit attack test in NFR-SEC2 and TEST-003|architect|
|3|R8 — IsolationLayers shape changes|MEDIUM|LOW|Compile-time break of HomeIsolation extension|COMP-012 probe test pins API; vendor copy plan documented; pin tested SHA|architect|
|4|R2 — HOME setup slow at 15-eval parallel|MEDIUM|MEDIUM|Suite runtime exceeds adoption target|Reuse install_hooks optimizations; NFR-PERF1 records baseline; ~1.4s/eval budget acceptable|architect|
|5|R5 — Ptytest fork drifts from upstream pexpect|LOW|LOW|Compatibility break over time|Quarterly review of pexpect releases (AC10); resync procedure in PROVENANCE.md; pinned SHA|architect|

## M3: Execution Engine & Reporter

**Objective:** Build the per-eval lifecycle, the parallel orchestrator, and the report writer with strict N′-vs-K contract enforcement. | **Duration:** 6 days | **Entry:** M2 exit; HomeIsolation + PtyDriver land. | **Exit:** RunOrchestrator runs a 3-eval suite in parallel; Reporter emits summary.md/json with `len(outcomes) == counts.expanded_n_prime` invariant enforced; SIGINT cancels in-flight evals and writes partial report; exit-code semantics tests pass.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|45|DM-001|EvalOutcome frozen dataclass|Per-eval outcome record emitted by EvalRunner|models|-|fields:eval_id:str;title:str;status:Literal[PASS,FAIL,ERRORED,TIMEOUT,INTERRUPTED,SKIPPED,XFAIL,XPASS];duration_sec:float;expects:list[ExpectResult];skip_reason:str|None;skip_flag_triggered:str|None;artifacts:dict[str,str];error_class:str|None|M|P0|
|46|DM-003|EvalResult model|Per-eval result record consumed by reporter|models|DM-001|fields:eval_id,outcome:EvalOutcome,start,end,duration_sec,stdout,stderr,artifacts,error:Exception|None; serializable|S|P0|
|47|DM-010|EvalContext runtime record|Runtime context passed to ExpectCallable|models|DM-006|fields:eval_spec,home,home_path,artifacts_dir,run_dir,env,stdout_path,stderr_path,transcript_path,jsonl_paths,exit_code,stdout,stderr,duration_sec,artifacts;immutable view|M|P0|
|48|FR-LC1|EvalRunner lifecycle|build isolation→deploy hooks→spawn→inject→observe→assert→teardown|runner|COMP-006,COMP-013,DM-001|sequence executed per spec; ERRORED status on harness exception; PASS only when all Expects pass; teardown honors keep flag|L|P0|
|49|COMP-004|EvalRunner implementation|Full runner class wrapping FR-LC1|runner|FR-LC1,DM-010|emits EvalOutcome; logs to per-eval JSONL; respects per-eval timeout|L|P0|
|50|NFR-REL1|Signal handling + timeout enforcement|SIGINT/SIGTERM cancel; per-eval timeout kills + reaps|runner|COMP-004|SIGINT marks in-flight as INTERRUPTED;writes partial summary;exits 3;per-eval timeout kills PtyDriver+reaps zombie+marks TIMEOUT|M|P0|
|51|NFR-REL2|Bounded retry policy|Failed evals NOT retried by default; deterministic single-pass|runner|COMP-004|default no-retry; --eval subset re-run path documented; OQ-10 retry semantics gated to MCP-flaky tag only|S|P0|
|52|DM-004|RunSummary aggregate structure|Aggregate run summary data model|models|DM-001|fields:run_id,started_at,finished_at,duration_sec,suite,manifest_version,parallel,counts,totals,evals[],artifacts; serializable|M|P0|
|53|DM-012|summary.json schema|Canonical machine-readable summary contract|reporter|DM-004|fields:run_id,started_at,duration_sec,suite,manifest_version,parallel,counts.{manifest_n,expanded_n_prime,kept_k,skipped_s,kept_plus_skipped_equals_n_prime},totals.{passed,failed,skipped,errored,interrupted,timeout},evals[]|M|P0|
|54|FR-RPT1|Aggregated Run Report|Emit summary.md, summary.json, optional junit.xml|reporter|DM-012,COMP-008|len(evals[])==counts.expanded_n_prime; SKIPPED rows included with skip_reason; mismatch raises ReporterContractViolation exit 2|L|P0|
|55|COMP-008|Reporter / AggregatedRunReport|to_markdown/to_yaml/to_json/to_junit methods|reporter|FR-RPT1,COMP-015|all 4 emitters implemented; assertion guard wired; pattern reference cli/sprint/executor.py:190-335|L|P0|
|56|COMP-015|AggregatedPhaseReport pattern probe|Pin shape reference for AggregatedRunReport|reporter|-|smoke test confirms shape; failing on upstream refactor|S|P1|
|57|COMP-003|RunOrchestrator|ThreadPoolExecutor+as_completed scheduler|orchestrator|COMP-004,DM-001|max_workers=8 default clamped[1,15]; per-eval timeout enforced; emits EvalOutcome per expanded spec; honors AC6 pattern|L|P0|
|58|FR-G2|Parallel execution of 15 evals|Run 15 evals in parallel with concurrency=8 default|orchestrator|COMP-003|integration test runs 15-eval suite at --parallel 8; strict isolation: own HOME, session_id, telemetry namespace; max=15 clamp enforced|L|P0|
|59|NFR-PERF2|Concurrency resource bounds verification|Document RAM ceiling at --parallel 15 with free-RAM precheck|orchestrator|FR-G2|benchmark confirms ≤2.25GB resident at --parallel 15; doctor warns when free RAM <2.25GB before accepting --parallel 15; documented in PROVENANCE/perf-notes|S|P1|
|60|NFR-PERF4|Disk budget enforcement (--max-disk-mb)|Orchestrator polls disk every 5s; halts on breach|orchestrator|COMP-003|default 1024 MB; 0 disables; on breach: in-flight evals complete, no new evals scheduled, exit 2 with disk_budget_exceeded artifact|M|P0|
|61|NFR-ISO1|No shared mutable state at concurrency|Integration test asserting no shared state at max parallel|orchestrator|FR-G2|no shared HOME; no shared file handles (auggie-first.jsonl); no port collisions; test runs N×15 trials|M|P0|
|62|NFR-PERF3|Suite runtime target tracking|Track full-suite duration trend|orchestrator|FR-G2|baseline recorded; budget <10 min documented; --eval subset path documented|S|P2|
|63|TEST-006|PTY lifecycle tests|First-class test deliverable: real PTY spawn, prompt readiness, input injection, timeout handling, transcript capture|tests|FR-LC1,COMP-007|real claude spawned when available; prompt readiness observed; input injected; transcript exists; timeout reaps child|L|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|EvalOutcome emission channel|callback wiring|wired|M3|COMP-008,COMP-003|
|Per-eval JSONL telemetry path|file resource|wired|M3|FR-EXP1,COMP-008|
|Disk-budget poller (5s tick)|background task|wired|M3|NFR-PERF4|
|SIGINT/SIGTERM handler|signal binding|wired|M3|NFR-REL1|
|ThreadPoolExecutor scheduler|concurrency pattern|wired|M3|COMP-003|

### Milestone Dependencies — M3

- M2 HomeIsolation + PtyDriver merged.
- Existing `cli/prd/executor.py:774-802` pattern available as reference.

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|N′-vs-K contract violation goes undetected|HIGH|MEDIUM|Reporter silently drops skipped evals; eval coverage misreported|FR-RPT1 enforces len(evals[])==counts.expanded_n_prime; ReporterContractViolation exits 2; integration test exercises the assertion|architect|
|2|R4 — Concurrent HOMEs exhaust disk|LOW|LOW|Run aborts mid-suite|--keep-home false default; NFR-PERF4 polls every 5s; budget recorded as artifact|architect|
|3|Signal race during teardown|MEDIUM|MEDIUM|Zombie processes; incomplete summary|NFR-REL1 reaps zombies before exit; partial summary always written; exit 3 dedicated to INTERRUPTED|architect|

## M4: Expect Primitives & CLI Surface

**Objective:** Land the assertion DSL primitives (`Expect.*`) against the real `EvalContext`, and complete the `superclaude eval` Click group with all flags wired (including `--junit` per OQ-7 resolution and `--no-pty` exclusion set per OQ-3). | **Duration:** 4 days | **Entry:** M3 exit; RunOrchestrator emits EvalOutcome end-to-end; OQ-3 + OQ-7 resolved (carried from M1). | **Exit:** All seven Expect primitives covered by tests; `superclaude eval run --suite real` parses every documented flag; manifest `expects:` blocks executable in declarative and programmatic forms; coverage-gate CLI entry green for a one-matcher fixture suite.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|64|FR-EXP1|Expect.* assertion DSL primitives|Implement primitives Expect.file/jsonl/settings_json/exit_code/stderr/stdout/duration against real EvalContext|dsl|DM-009,DM-010,COMP-010|each returns callable (EvalContext)->ExpectResult; declarative YAML form and programmatic form both supported; named arguments documented|L|P0|
|65|COMP-010.1|Expect.file primitive|Assert file exists/content matches pattern|dsl|FR-EXP1|args path,exists,contains,regex,equals; ExpectResult includes diff on failure|S|P0|
|66|COMP-010.2|Expect.jsonl primitive|Assert JSONL entries match predicate|dsl|FR-EXP1|args path,line_count,filter,assert_each,assert_any; supports per-eval hook telemetry assertions|M|P0|
|67|COMP-010.3|Expect.settings_json primitive|Assert ~/.claude/settings.json shape|dsl|FR-EXP1|args path,key_path,equals,exists; resolves against HomeIsolation.home_path|S|P0|
|68|COMP-010.4|Expect.exit_code primitive|Assert subprocess exit code|dsl|FR-EXP1|args equals,in_set,not_equals;default equals 0|S|P0|
|69|COMP-010.5|Expect.stderr / stdout primitives|Assert TTY transcripts match patterns|dsl|FR-EXP1|args contains,regex,not_contains; operates on ANSI-stripped buffer from COMP-011|S|P0|
|70|COMP-010.6|Expect.duration primitive|Assert eval duration within bound|dsl|FR-EXP1|args max_sec,min_sec; informational PASS records duration even if outside bound when only one bound set|S|P1|
|71|COMP-001|eval_group Click commands|Top-level Click group exporting subcommands|cli|COMP-002,COMP-009,FR-G3|exports run,list,describe,doctor subcommands; group registered in superclaude entry point|M|P0|
|72|FR-CLI1|`eval run` subcommand|Primary execution entry point with all flags|cli|COMP-001,COMP-003,OQ-7-res|flags --suite,--parallel,--eval,--no-mcp,--no-pty,--output-dir,--keep-home,--timeout-mult,--max-disk-mb,--json,--verbose,--junit all wired and validated|L|P0|
|73|FR-G6|Single-command local runnability|`uv run superclaude eval --suite real` succeeds on clean dev machine|cli|FR-CLI1|smoke test on clean Linux host completes 1-eval suite end-to-end with no manual setup beyond `make dev`|M|P0|
|74|FR-G4|Reproducible artifacts under `.dev/eval-runs/<ISO>/<run-id>/`|Per-run artifact layout|reporter|COMP-008|directory tree contains summary.{md,json}, junit.xml (when enabled), per-eval/{logs.jsonl,tty.transcript,artifacts/}|M|P0|
|75|FR-G5|Falsifiable hook-matcher coverage gate (CLI entry)|`eval doctor --check-coverage` and top-of-run gate|cli|COMP-009,FR-CLI4|gate computes matcher coverage map; FAILS run if any matcher P lacks corresponding eval; v1 coverage mcp__auggie__*,mcp__auggie-mcp__*,mcp__airis-mcp-gateway__*|L|P0|
|76|DOC-OQ7|`--junit` flag wiring decision|Decide and implement --junit flag or remove from §9|cli|OQ-7|either --junit added to FR-CLI1 flag set with junit.xml emission, OR spec §9 corrected to remove conditional language; decision recorded in decisions.md|S|P0|
|77|DOC-OQ3|`--no-pty` exclusion set|Enumerate evals excluded under --no-pty|cli|OQ-3|exclusion set written to suites/real.yaml as no_pty:skip tag per eval; --no-pty implementation honors tag; documented in eval describe output|S|P0|
|78|TEST-007|Reporter contract tests|First-class test deliverable: N′ vs K behavior, skipped inclusion, mismatch failure, JSON schema fidelity|tests|FR-RPT1,DM-012|len(evals)==expanded_n_prime; skipped has status+skip_reason; mismatch exits 2; schema fields complete|M|P0|
|79|TEST-008|Exit-code semantics tests|First-class test deliverable: process exit codes for clean, failing, harness-error, interrupted runs|tests|FR-RPT1,NFR-REL1|0 iff no FAIL/ERRORED/TIMEOUT/XPASS; 1 if any such eval; 2 harness error; 3 interrupted|M|P0|
|80|TEST-009|Artifact reproducibility tests|First-class test deliverable: run directories, transcripts, logs, stack traces, summaries written deterministically|tests|FR-G4|run dir pattern stable; transcript path recorded; logs present; stack trace on error; summary links artifacts|M|P0|
|81|OPS-003|Artifact retention policy|Define default deletion and keep-home behavior for per-eval HOMEs and run artifacts|ops|FR-G4,NFR-PERF4|--keep-home default false; failed setup preserved; run summaries retained; disk budget messages include retention advice|S|P1|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Click `eval_group` registry|registry|wired|M4|superclaude CLI entry|
|Expect callable dispatch|dispatch table|wired|M4|FR-LC1,COMP-004|
|`--no-mcp` skip flag|flag-driven gate|wired|M4|COMP-009|
|Coverage-gate hook matcher map|registry|wired|M4|FR-G5|
|JUnit writer|optional writer strategy|wired|M4|FR-RPT1|

### Milestone Dependencies — M4

- M3 RunOrchestrator + Reporter merged.
- `~/.claude/settings.json` hook matcher patterns frozen for v1 (auggie + auggie-mcp + airis-mcp-gateway).
- OQ-3 and OQ-7 resolutions recorded in decisions.md.

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|Flag drift between spec §4 and implementation|MEDIUM|MEDIUM|User-facing inconsistency; doctor reports wrong status|OQ-7 resolution gates M4 exit; CLI test exercises every documented flag; help text auto-validated|architect|
|2|Coverage gate false negatives (matcher in settings but no eval check)|HIGH|MEDIUM|Gate passes despite missing coverage|FR-G5 enumerates matchers from ~/.claude/settings.json at runtime; failing matcher emits `coverage_missing:<pattern>` artifact|architect|

## M5: Eval Bodies, Coverage Gate, Rollout Plan

**Objective:** Author the 15 eval bodies (E1–E15), validate the coverage gate against a real `~/.claude/settings.json`, prove the suite runs end-to-end at `--parallel 8`, and define the eval-batch rollout plan. | **Duration:** 14 days (per debate D12 — Haiku's 0.93d/eval velocity over 7d Opus original) | **Entry:** M4 exit; DSL + CLI complete; OQ-2 resolved for E3–E15 bodies. | **Exit:** All 15 evals enumerate in `eval list`; coverage gate green for all three v1 matcher families; full suite completes <10 min on dev host; MIG-002 batch plan recorded.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|82|E1|Eval E1 — auggie matcher coverage|Issue real MCP tool call matching mcp__auggie__* pattern and assert hook telemetry|evals|FR-G5,COMP-010|inputs include real auggie tool invocation; expects Expect.jsonl asserts hook fired in per-eval hook log; tagged hook-coverage; skip under --no-mcp|M|P0|
|83|E2.1|Eval E2.1 — auggie-mcp parameterize|Parameterize entry for mcp__auggie-mcp__* matcher|evals|FR-G5,FR-SCH2|parameterize-expanded ID matches eval_id regex; hook telemetry asserted; tagged hook-coverage|M|P0|
|84|E2.2|Eval E2.2 — airis-mcp-gateway parameterize|Parameterize entry for mcp__airis-mcp-gateway__* matcher|evals|FR-G5,FR-SCH2|same as E2.1 for airis-mcp-gateway family; soft-skip under --no-mcp; skip_reason recorded|M|P0|
|85|E2.3|Eval E2.3 — third parameterized matcher entry|Parameterize entry covering remaining v1 hook|evals|FR-G5,FR-SCH2|covers third matcher in v1 set; hook telemetry asserted|M|P0|
|86|E3|Eval E3 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; minimum AC: passes deterministically on clean HOME|M|P0|
|87|E4|Eval E4 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|88|E5|Eval E5 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|89|E6|Eval E6 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|90|E7|Eval E7 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|91|E8|Eval E8 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|92|E9|Eval E9 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|93|E10|Eval E10 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|94|E11|Eval E11 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|95|E12|Eval E12 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|96|E13|Eval E13 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|97|E14|Eval E14 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|98|E15|Eval E15 — body per OQ-2 resolution|Eval body authored per OQ-2 resolution|evals|OQ-2|content frozen post-OQ-2; deterministic AC|M|P0|
|99|SC2|Manifest schema covers all 15 evals|Validate all E1–E15 IDs match regex and load via schema|validation|FR-SCH1,FR-SCH2|all 15 IDs (including parameterize-expanded) pass eval_id regex; suite loads in eval doctor with zero violations|S|P0|
|100|R3-mit|MCP retry-once policy implementation|Per-eval retry-once on MCP-specific failure modes|orchestrator|OQ-10|MCP-flaky tag honored; retry attempted exactly once; failure tagged mcp_server_flaky in outcome.artifacts|M|P1|
|101|TEST-013|Coverage gate tests|First-class test deliverable: doctor and run top-of-run coverage gate against missing and complete matcher sets|tests|FR-G5|missing matcher fails; complete matcher passes; doctor names uncovered patterns; run refuses uncovered suite|M|P0|
|102|TEST-014|No-MCP skip behavior tests|Verify MCP-dependent evals are classified as SKIPPED with reason when `--no-mcp` is used|tests|COMP-009,FR-RPT1|MCP evals skipped; status SKIPPED; skip_reason set; counts kept_plus_skipped_equals_n_prime true|S|P1|
|103|MIG-002|Eval-batch rollout plan|Split broad eval bodies into reviewable batches after harness contract lands (per R9 mitigation)|planning|FR-G5,OQ-2|15 eval IDs tracked; batches of 3–5 defined; harness PR separable; eval PRs reference coverage map|S|P1|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Hook matcher → eval registry|registry|wired|M5|FR-G5|
|Per-eval hook telemetry path `~/.claude/logs/<hook>.jsonl`|file resource|wired|M5|COMP-010.2|
|MCP-flaky retry tag|callback wiring|wired|M5|R3-mit|
|Coverage map|matcher registry|wired|M5|FR-G5,TEST-013|

### Milestone Dependencies — M5

- M4 Expect primitives + CLI merged.
- OQ-2 resolved for E3–E15 bodies.
- Real `~/.claude/settings.json` PostToolUse matchers frozen for v1.

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-10|Exact retry semantics for MCP-flaky failures (empirical resolution per debate D5)|Determines whether R3-mit lands as P0 or remains P1|RyanW|before M5 exit|
|2|OQ-6|Suite filename convention beyond `real.yaml` (e.g., quick subset)|Blocks quick-suite follow-up clarity|architect|before TEST-015 follow-up|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R3 — MCP server flakiness causes E1/E2 false failures|MEDIUM|MEDIUM|Suite is noisy; coverage gate misreports|R3-mit retry-once policy; mcp_server_flaky artifact tag; --no-mcp escape hatch|architect|
|2|R6 — 15-eval suite >10min adoption friction|MEDIUM|MEDIUM|Adoption drops; harness skipped in dev loops|--eval subset documented; follow-up suites/quick.yaml planned per OQ-6; perf budget tracked in M3 NFR-PERF3|architect|
|3|R9 — PR scope creep as evals are added|MEDIUM|HIGH|Review fatigue; merges delayed|MIG-002 batches of 3-5 evals per PR; per-batch DoD recorded; harness merges as PR 1|architect|

## M6: Docs, ADRs, Hardening, Sync, Platform Roadmap

**Objective:** Close decisions, complete documentation (ADRs D-5..D-8, PROVENANCE.md), enforce source-of-truth discipline (`make sync-dev` + `make verify-sync`), record macOS platform follow-up plan (MIG-003), and prove single-command runnability on a clean dev machine. | **Duration:** 2 days | **Entry:** M5 exit; suite green at `--parallel 8`. | **Exit:** RyanW signs off ADRs; `make verify-sync` exits 0; SC1–SC5 satisfied; macOS roadmap entry recorded in decisions.md.

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|104|SC1|ADR sign-offs D-5..D-8|RyanW signs off 4 original + 4 new ADRs in decisions.md|docs|OQ-1|decisions.md contains D-1..D-8 with sign-off date; OQ-1 resolution recorded; ADRs cross-reference roadmap deliverables|S|P0|
|105|DOC-OQ9|macOS support roadmap entry|Record macOS timeline in decisions.md|docs|OQ-9|decisions.md contains macOS follow-up entry with owner + target; AC1 reaffirmed for v1|S|P1|
|106|DOC-OQ8|Time-offset mechanism contract|Document how Claude Code consumes CLAUDE_FAKE_TIME_OFFSET (or remove)|docs|OQ-8|decisions.md records either: (a) confirmation that claude binary honors env var, OR (b) removal of time-offset layer from FR-ISO1|S|P1|
|107|DOC-OQ6|Suite naming convention beyond `real.yaml`|Document suite filename rules; record `quick.yaml` plan|docs|OQ-6|cli/eval/suites/README.md records naming convention; `quick.yaml` plan recorded as follow-up|S|P2|
|108|AC2|CI integration deferral note|Record deferral and follow-up trigger in decisions.md|docs|-|decisions.md entry says local-only for v1; trigger for CI revisit recorded|S|P2|
|109|AC1|Linux-only declaration|Record AC1 in decisions.md and README|docs|-|README documents Linux-only v1; eval doctor refuses non-Linux with friendly error|S|P0|
|110|SC4|Effort estimate acknowledgment|RyanW signs off LOC estimate ~1,340 harness + ~3,000-4,500 eval bodies|docs|SC1|decisions.md records signed-off estimate; ledger updated post-implementation with actual LOC|S|P1|
|111|SC5|Open-question list fully resolved|All 10 OQ-xxx items recorded as resolved in decisions.md|docs|OQ-1,OQ-2,OQ-3,OQ-4,OQ-5,OQ-6,OQ-7,OQ-8,OQ-9,OQ-10|every OQ-xxx has a `resolution:` field in decisions.md; signed-off by RyanW|M|P0|
|112|SC3|Zero-new-deps verification|Verify pyproject.toml has no new external deps beyond pexpect (vendored) + jsonschema (transitive)|docs|AC3|`uv pip list` diff post-implementation shows only ptytest-vendored sources changed; CI assertion enforces|S|P0|
|113|OPS-004|Validation command set|Define the validation command sequence using UV and make targets|ops|MIG-001|uv run pytest targeted eval tests; make verify-sync; eval doctor; single eval run; results linked in artifacts|S|P0|
|114|OPS-005|Release checklist|Assemble release evidence for doctor, sync, tests, artifact contracts, follow-ups|ops|OPS-004|eval doctor green; make verify-sync EXIT=0; targeted tests pass; full-run artifacts linked; follow-ups listed|S|P0|
|115|MIG-001|Source sync migration|Sync eval CLI sources from `src/superclaude/` into `.claude/` dev copies after implementation|sync|OPS-003|make sync-dev run; make verify-sync exits 0; no direct .claude source edits; sync evidence captured|S|P0|
|116|MIG-003|Platform follow-up plan|Record macOS and future CI support as follow-up scope outside v1 Linux-local delivery|planning|DOC-OQ9|macOS non-goal preserved; CI non-goal preserved; follow-up roadmap item created; no v1 blocking work added|S|P2|

### Integration Points — M6

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`decisions.md` ADR ledger|file resource|wired|M6|SC1,SC5|
|`make verify-sync` CI gate|CI binding|wired|M6|AC11,MIG-001|
|`PROVENANCE.md` for vendored ptytest|file resource|wired|M6|NFR-MAINT1|
|Release checklist registry|process|wired|M6|OPS-005|

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
|`concurrent.futures` (stdlib)|M3|HARD|none — Python runtime requirement|
|`shutil` (stdlib)|M2|HARD|none — used for binary lookup and hook deployment|
|`pathlib` (stdlib)|M1,M2|HARD|none — path containment depends on resolved paths|
|`mcp_server.auggie`|M5|SOFT-SKIP|--no-mcp escape hatch; E1 marked SKIPPED|
|`mcp_server.auggie-mcp`|M5|SOFT-SKIP|--no-mcp escape hatch; E2.1 marked SKIPPED|
|`mcp_server.airis-mcp-gateway`|M5|SOFT-SKIP|--no-mcp escape hatch; E2.2 marked SKIPPED|
|`cli/sprint/executor.py:107-182` IsolationLayers|M2|HARD|COMP-012 probe pins shape; vendor copy plan documented|

### Infrastructure Requirements

- Linux dev host with ≥4 GB free RAM (covers `--parallel 15` at ~2.25 GB plus headroom); doctor warns before accepting `--parallel 15` if free RAM <2.25 GB.
- ~2 GB free disk under `/tmp` or repo `.dev/` for per-run scratch (default `--max-disk-mb 1024`).
- Read access to `~/.claude/settings.json` for coverage-gate matcher enumeration (read-only — never written by harness).
- TTY-capable shell (xterm-compatible) for pexpect; CI runners without TTY emulation require `--no-pty` mode.
- `uv` available for `uv run superclaude eval` single-command path.
- Source-of-truth workflow: edit under `src/superclaude/`, run `make sync-dev`, then `make verify-sync`.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R1|Claude Code TTY behavior changes between versions break PtyDriver|M2,M5|MEDIUM|HIGH|Pin claude version range in eval doctor (min 0.5.0); capture full TTY transcripts as artifacts; isolate parsing in PtyStream|architect|
|R2|Per-eval HOME setup slow at 15-eval parallel|M2|MEDIUM|MEDIUM|Reuse `install_hooks.py` optimizations; NFR-PERF1 records baseline; ~1.4s/eval budget acceptable|architect|
|R3|MCP server flakiness causes E1/E2 false failures|M5|MEDIUM|MEDIUM|Per-eval retry-once on MCP-specific failure modes (R3-mit, deliverable 100); mcp_server_flaky artifact tag; --no-mcp escape hatch|architect|
|R4|Concurrent HOMEs/artifacts exhaust disk|M3,M4|LOW|LOW|`--keep-home false` default; NFR-PERF4 polls disk every 5s with default 1024MB budget; exit 2 on breach; partial summaries retained|architect|
|R5|Ptytest fork drifts from upstream pexpect|M2,M6|LOW|LOW|Quarterly review of pexpect releases (AC10); resync procedure in PROVENANCE.md; pinned SHA|architect|
|R6|15-eval suite exceeds 10-min adoption budget|M3,M5|MEDIUM|MEDIUM|`--eval` subset; future `suites/quick.yaml`; per-suite duration recorded as artifact|architect|
|R7|Maintainer runs harness against real `~/.claude/`|M1,M2|LOW|HIGH|Hard guard in HomeIsolation.setup() refusing HOME outside known scratch dirs (NFR-SEC3); AC12 allowlist enforced|architect|
|R8|`IsolationLayers` shape changes breaking extension|M2|LOW|MEDIUM|COMP-012 probe test pins API; vendor copy plan documented; SHA pin recorded|architect|
|R9|PR scope creep as evals are added|M5|HIGH|MEDIUM|Harness lands as PR 1 (M1–M4); evals as PR 2+ via MIG-002 batches of 3-5; per-batch DoD recorded|architect|
|R10|Unresolved decisions cause contract churn after implementation begins|M1|MEDIUM|HIGH|Close OQ-1/OQ-3/OQ-4/OQ-7/OQ-8 before M1 exit (OPS-001); OQ-10 may resolve empirically in M3/M5|architect|
|R11|N′-vs-K reporter contract violation undetected|M3|MEDIUM|HIGH|FR-RPT1 enforces `len(evals[])==counts.expanded_n_prime`; ReporterContractViolation exits 2; TEST-007 covers|architect|
|R12|Signal race during teardown leaves zombies|M3|MEDIUM|MEDIUM|NFR-REL1 reaps zombies before exit; partial summary always written; exit 3 dedicated to INTERRUPTED|architect|
|R13|Coverage gate false negatives (matcher with no eval)|M4,M5|MEDIUM|HIGH|FR-G5 enumerates matchers from ~/.claude/settings.json at runtime; `coverage_missing:<pattern>` artifact; TEST-013 covers|architect|
|R14|Vendored ptytest attribution incomplete|M2|LOW|LOW|OQ-4 resolved before NFR-MAINT1 (M2 entry blocker); NOTICE/LICENSE/PROVENANCE captured|architect|
|R15|Sync drift between `src/superclaude/` and `.claude/`|M6|MEDIUM|LOW|`make verify-sync` runs in CI; pre-commit hook rejects unsynced changes (AC11)|architect|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC1: Maintainer sign-off on ADRs|ADR ledger entries signed|D-1..D-8 all signed|`decisions.md` review checklist; signed-off field per ADR|M6|
|SC2: Manifest schema covers all 15 evals|Schema-valid eval IDs|15/15 IDs pass schema + regex|`eval doctor` zero violations on real.yaml|M5|
|SC3: Zero new external Python deps|pyproject.toml diff|0 new external imports beyond transitive jsonschema|`uv pip list` snapshot compared pre/post|M1,M6|
|SC4: Effort estimate acknowledged|LOC actual vs estimate|±15% of ~1,340 harness + 3,000-4,500 evals|Post-implementation LOC count vs decisions.md estimate|M6|
|SC5: Open-question list resolved|OQ-xxx resolutions|10/10 OQ-xxx have resolution field|`decisions.md` checklist; cross-reference per-milestone OQ tables|M6|
|Doctor health|Preflight status|Green checklist on clean dev machine|`uv run superclaude eval doctor`|M4|
|Real subprocess validation|PTY eval run|E1 single eval runs through real Claude Code subprocess|`uv run superclaude eval run --suite real --eval E1`|M3|
|Exit code semantics|Exit code dispatch|0/1/2/3 per spec|TEST-008 integration test exercises each exit path|M4|
|Reporter contract invariant|`len(outcomes) == counts.expanded_n_prime`|Always equal; mismatch exits 2|TEST-007 `ReporterContractViolation` test|M3|
|Hook matcher coverage|Matchers with eval coverage|3/3 v1 families covered (auggie, auggie-mcp, airis-mcp-gateway)|`eval doctor --check-coverage` green; TEST-013|M5|
|Single-command runnability|`uv run superclaude eval --suite real` success on clean host|Exit 0 on green path|Fresh container/VM smoke test|M5|
|Suite runtime budget|Full suite wall-clock at `--parallel 8`|<10 min|Captured in summary.json `duration_sec`|M5|
|Sync validation|Source/dev copies match|`make verify-sync` exits 0|Run after `make sync-dev`|M6|

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
|Validation order (Haiku D adoption)|Schema + ID validation before any filesystem operation; re-validate inside HomeIsolation as defense-in-depth|Create run dir then validate; runner-level only validation|Prevents path traversal and avoids unsafe side effects from invalid manifests; layered guard catches loader bypass|
|DSL placement|Interface (COMP-010) in M1; primitives (COMP-010.1–6) in M4|All in M1; all in M3|Manifest authors can shape `expects:` blocks early without waiting for backing `EvalContext` to land (debate D3 compromise)|
|Milestone granularity|6 milestones with distinct M6 hardening gate|5 milestones with M5 = evals + release|Separates "harness works at --parallel 8" (M5 exit) from "ADRs signed, NOTICE complete, sync verified" (M6 exit); SC1/SC5 are independently observable|
|Eval-body window|14 days for E1–E15 authoring|7 days; 21 days|Matches observed ~0.93d/eval velocity covering YAML authoring, local run, Expect tuning, artifact capture, telemetry review (debate D12)|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|4 days|Day 1|Day 4|EvalConfig + SuiteLoader + capability gate outline + ExpectDSL interface + eval doctor outline|
|M2|5 days|Day 5|Day 9|OQ-4 closure + ptytest vendor + HomeIsolation + path-containment + PtyDriver + PtyStream|
|M3|6 days|Day 10|Day 15|EvalRunner + RunOrchestrator + Reporter + disk-budget poller + signal handling|
|M4|4 days|Day 16|Day 19|Expect primitives (COMP-010.1–6) + eval_group CLI + all flags + coverage-gate entry|
|M5|14 days|Day 20|Day 33|E1–E15 eval bodies + coverage gate + full-suite green + MIG-002 batch plan|
|M6|2 days|Day 34|Day 35|ADR sign-offs + PROVENANCE.md + NOTICE finalization + MIG-003 macOS roadmap + sync-verify gate|

**Total estimated duration:** 35 working days (~7 calendar weeks at single-engineer pace; harness build ~19 days M1–M4, eval authoring ~14 days M5 per debate D12 convergence, ~2 days hardening M6)
