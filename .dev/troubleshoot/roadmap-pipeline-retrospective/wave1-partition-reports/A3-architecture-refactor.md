# A3 — Pipeline Architecture Refactor Retrospective

**Partition:** A3 — Pipeline Architecture Refactor
**Directories mined:**
1. `.dev/releases/complete/v2.01-Architecture-Refactor/` — command/skill decoupling refactor
2. `.dev/releases/complete/v2.13-CLIRunner-PipelineUnification/` — sprint/pipeline/roadmap executor boundaries
3. `.dev/releases/complete/v3.2_fidelity-refactor___/` — spec-fidelity, wiring-verification, and execute_sprint integration

**Focus:** Each architectural refactor and what new failure classes it eliminated vs. introduced.

**Auggie cross-reference target:** `/config/workspace/IronClaude/.claude/worktrees/BareReview/src/superclaude/cli/roadmap` (and adjacent `sprint/`, `cli_portify/`, `audit/`, `pipeline/`).

---

## Findings

### F-A3-01: Monolithic command files exceed agent attention budget (RC-1)
- **Type:** FAILURE
- **Pipeline step:** OTHER (skill/command load layer that the roadmap pipeline depends on for activation)
- **Symptom:** `task-unified.md` ran to 567 lines and other commands hit 1005L (`recommend.md`), 913L (`review-translation.md`), 592L (`pm.md`); auto-loaded into context every invocation, agents silently dropped the behavioral protocol mid-execution and "guessed or hallucinated protocol steps."
- **Root cause (claimed):** Auto-loaded monolithic command files mix interface metadata with behavioral spec; attention degrades across the document so the protocol competes with examples and flag tables for weight. (RC-1, RC-2 in `extract-root-cause-analysis.md`.)
- **Remediation applied:** v2.01 3-tier loading model — Tier 0 command stub ≤150 lines, Tier 1 protocol skill on-demand via `Skill sc:<name>-protocol`, Tier 2 refs via `claude -p`. Thin-dispatcher template enforced.
- **Outcome:** Removed the "agent ignores protocol because it never reached it" failure class. Did not solve scope-control or context-compaction resilience (explicitly flagged as open in Section 6 of the RCA).
- **Still possible today (Auggie check):** NO for sc:roadmap — protocol lives in `sc-roadmap-protocol` skill and command files are short stubs. The roadmap CLI pipeline itself sidesteps the issue entirely because it runs in subprocesses with discrete prompts, not auto-loaded chat-context skills.
- **Source artifacts:** `v2.01-Architecture-Refactor/spec-planning/extract-root-cause-analysis.md` Sections 2 (RC-1), 5 (Solution 1), 7; `workflow_sc-roadmap-refactor.md` lines 22-52.

### F-A3-02: Naming collision blocked skill re-entry, so adversarial debate never ran (RC-4)
- **Type:** FAILURE
- **Pipeline step:** debate
- **Symptom:** Command `adversarial` invoking skill `sc:adversarial` was silently rejected by the Skill tool's re-entry block; `sc:roadmap` could not chain into adversarial generation.
- **Root cause (claimed):** Skill tool blocks re-invocation when an active skill shares the command name, so any command/skill pair with identical names cannot compose. (RC-4 in `extract-root-cause-analysis.md`; "Why Separate Names?" in Command-Skill Policy.)
- **Remediation applied:** v2.01 introduced the `-protocol` suffix convention: skill directories renamed to `sc-<name>-protocol/`, frontmatter `name: sc:<name>-protocol`. Bidirectional CI lint added in `make lint-architecture`.
- **Outcome:** Eliminated the silent skill-skip pattern at the chat-context layer; cross-skill invocations (roadmap → adversarial → tasklist) became possible.
- **Still possible today (Auggie check):** NO at the chat layer (rename completed; lint enforces). The CLI pipeline's adversarial integration is now a deterministic Python step (`adversarial_runner.py`/roadmap executor) rather than a chat-skill chain, so the re-entry block is irrelevant there.
- **Source artifacts:** `extract-root-cause-analysis.md` RC-4 (lines 56-62); `workflow_sc-roadmap-refactor.md` Problem Statement bullets 1-4 (BUG-001/005/006/T02.03).

### F-A3-03: Missing `Skill` in `allowed-tools` blocked skill invocation in 4 of 5 commands (RC-5, BUG-001)
- **Type:** FAILURE
- **Pipeline step:** OTHER (activation layer)
- **Symptom:** 4 commands added mandatory `Skill` invocations in `## Activation` but never added `Skill` to `allowed-tools` frontmatter. The agent was instructed to use a non-permitted tool, resulting in silent failure or hard error — protocol skill never loaded.
- **Root cause (claimed):** Frontmatter contract was treated as optional metadata, not enforced; no validation between activation directive and tool whitelist.
- **Remediation applied:** v2.01 Phase 2 fixed BUG-001 across `adversarial.md`, `cleanup-audit.md`, `task-unified.md`, `validate-tests.md`; CI check #8 ("Skill frontmatter complete: name, description, allowed-tools") added to `make lint-architecture`.
- **Outcome:** Closed the "instruction-without-permission" silent-skip failure class. RC-5 marked as resolved in `extract-root-cause-analysis.md` Section 5 (Solution 5).
- **Still possible today (Auggie check):** NO for the CLI roadmap pipeline (it does not use the Skill tool to chain steps — `executor.py` dispatches Python `StepRunner` callables directly). Still possible for unmaintained chat-layer commands unless `make lint-architecture` runs in CI.
- **Source artifacts:** `extract-root-cause-analysis.md` RC-5 (lines 64-72); `workflow_sc-roadmap-refactor.md` Phase 2 Task 2.1.

### F-A3-04: Rollback Incident — 4-file plan executed 68 file changes after context compaction
- **Type:** FAILURE
- **Pipeline step:** OTHER (scope-control gap upstream of the roadmap pipeline)
- **Symptom:** An agent given a 4-file plan executed 68 file changes; context compaction caused it to "go rogue" mid-execution and required a full rollback.
- **Root cause (claimed):** No runtime scope-control mechanism, no plan-validation gate, no atomic-change-group enforcement, and context compaction summarized away the boundary directives mixed into monolithic command files. (Section 4 of `extract-root-cause-analysis.md`.)
- **Remediation applied:** Partial — 3-tier loading raises compaction resilience (skills load "fresher" in context), but Section 5 Solution 6 explicitly notes "Scope Control Mechanism (Not Yet Designed)." Section 7 lists "no scope control" as the fifth and unsolved root cause.
- **Outcome:** PARTIAL. The architectural refactor mitigated the priming layer (RC-1 / RC-6) but the rollback class itself is still possible by design. Section 6 gap analysis explicitly marks runtime scope control as CRITICAL/not-designed.
- **Still possible today (Auggie check):** YES at the chat-layer. The CLI roadmap pipeline is structurally immune because each step runs as a subprocess with a single declared output file (validated by `executor.py:1043` and gate enforcement in `gates.py`), so "agent edits arbitrary files" cannot happen inside a pipeline step. The vulnerability persists wherever an interactive agent drives multi-file editing.
- **Source artifacts:** `extract-root-cause-analysis.md` Section 4 (lines 138-165), Section 6 (lines 269-280), Section 7 Item 5 (lines 285-295).

### F-A3-05: SUCCESS — `make lint-architecture` makes architecture policy machine-enforced
- **Type:** SUCCESS
- **Pipeline step:** OTHER (build-system / CI gate for the chat-skill layer the roadmap pipeline activates from)
- **Symptom:** Six of ten architecture checks now run in CI (bidirectional command↔skill linkage, size warnings/errors at 200/500 lines, activation section presence, skill frontmatter completeness, naming consistency, sync integrity).
- **Root cause (claimed):** N/A (this is the remediation).
- **Remediation applied:** v2.01 Phase 3 Task T03.02; `Makefile` `lint-architecture` target added with .PHONY and help registration.
- **Outcome:** Drift detection moved from "discovered after a rollback" to "caught at PR time." 4/10 checks still unimplemented (BUG-006).
- **Still possible today (Auggie check):** N/A — this is a positive outcome; the gap is the 4 unimplemented checks (BUG-006) which leave residual drift surface.
- **Source artifacts:** `extract-root-cause-analysis.md` Section 5 Solution 4 (lines 213-234); `workflow_sc-roadmap-refactor.md` Scope Map (Makefile rows).

### F-A3-06: `make sync-dev` skip heuristic never blocked roadmap-skill sync but was scheduled for cleanup
- **Type:** REMEDIATION (preventive)
- **Pipeline step:** OTHER (build system)
- **Symptom:** The `sync-dev` / `verify-sync` Makefile heuristic strips `sc-` prefix to derive a command name and skips syncing skills whose matching command file exists. For `-protocol` skills this *would not* trigger today (stripping `sc-` from `sc-roadmap-protocol` yields `roadmap-protocol`, which has no command match), but the heuristic is "conceptually incompatible with v2.01 architecture."
- **Root cause (claimed):** The empty `.claude/skills/sc-roadmap-protocol/` was actually caused by `make sync-dev` never being run after the rogue-agent rename, not by the heuristic — but the heuristic remained a latent failure surface.
- **Remediation applied:** T03.01 in `workflow_sc-roadmap-refactor.md` — remove 3-line skip heuristic from `sync-dev` (lines 114-117) and `verify-sync` (lines 153-157).
- **Outcome:** Latent failure class neutralized. Preventive, not curative.
- **Still possible today (Auggie check):** UNKNOWN — would require reading current Makefile. The pre-existing failure pattern documented in `Phase 1 Task 1.3` ("EMPTY — confirms skip heuristic is active") shows the original confusion between heuristic and unrun-sync.
- **Source artifacts:** `workflow_sc-roadmap-refactor.md` Phase 1 Task 1.3 (lines 129-141), Scope Map Makefile rows.

### F-A3-07: SUCCESS — Pipeline was correctly extracted from sprint; type-level dependencies inverted
- **Type:** SUCCESS
- **Pipeline step:** OTHER (architecture boundary that all roadmap steps rely on)
- **Symptom:** `pipeline/process.py:3` documents "Extracted from sprint/process.py"; commit `6548f17` atomically created `pipeline/` and `roadmap/`, reparenting sprint's models and process classes. Both `SprintConfig→PipelineConfig` and `Sprint ClaudeProcess→pipeline ClaudeProcess` extractions work. NFR-007 ("No imports from superclaude.cli.sprint or superclaude.cli.roadmap") is preserved across every pipeline module.
- **Root cause (claimed):** N/A (positive baseline established by v2.13 evidence).
- **Remediation applied:** Pre-v2.13 work; v2.13 validated the boundary holds and confirmed roadmap consumes `execute_pipeline()` cleanly (`roadmap/executor.py` delegates to `execute_pipeline()` with `roadmap_run_step` as StepRunner).
- **Outcome:** Roadmap pipeline gets generic infrastructure (gates, retry, parallel dispatch, stateless callbacks) without coupling to sprint internals.
- **Still possible today (Auggie check):** N/A — Auggie confirms `pipeline/` still has no upward imports; `roadmap/executor.py` still uses `_embed_inputs` (line 531) and the file-passing fix from F-A3-10.
- **Source artifacts:** `v2.13-CLIRunner-PipelineUnification/merged-pipeline-decision.md` lines 25-42; `release-spec.md` Section 2.

### F-A3-08: Premature unification of sprint executor into pipeline was rejected via adversarial debate
- **Type:** SUCCESS (adversarial-protocol functioned as designed)
- **Pipeline step:** debate
- **Symptom:** Pro-unification proposal claimed sprint should adopt `execute_pipeline()`; debate (convergence 0.72) established that (a) sprint's poll loop would relocate into a 100-150 line `sprint_run_step` callback rather than disappear, (b) sprint phases cannot be retried (filesystem side effects) or parallelized (sequential mutation), (c) net code reduction ≈ 0, (d) effort Large, regression risk High against zero executor tests.
- **Root cause (claimed):** Initial unification proposal undercounted divergence in orchestration semantics (7 interleaved subsystems in sprint — subprocess lifecycle, NDJSON monitor threads, monotonic timeouts, watchdog stall detection, tmux, diagnostic collection, structured logs).
- **Remediation applied:** Rejected Option 1 (full unification); deferred Option 2 (partial unification) pending semantic-overlap trigger conditions; adopted Option 3 (targeted fixes — logging hooks, dead-code removal, file-passing fix, characterization tests).
- **Outcome:** Avoided a large refactor with high regression risk and ≈ zero net benefit. Debate transcript preserves the trigger conditions for re-evaluation (gate-based validation in sprint, retry-with-rollback, third executor consumer).
- **Still possible today (Auggie check):** N/A — this is the absence of an unnecessary refactor.
- **Source artifacts:** `merged-pipeline-decision.md` Sections 3-5, "Summary" table (lines 222-230), Recommendation (lines 232-249).

### F-A3-09: Process method overrides duplicated ~90 lines between sprint and pipeline ClaudeProcess
- **Type:** FAILURE → REMEDIATION
- **Pipeline step:** OTHER (subprocess layer shared with roadmap)
- **Symptom:** `sprint/process.py` overrode `start()`, `wait()`, `terminate()` from pipeline's `ClaudeProcess` with ~90 lines whose only functional difference was `debug_log()` calls vs `_log.debug()` calls.
- **Root cause (claimed):** Sprint needed structured debug logging; instead of designing a hook, the implementation copy-pasted entire method bodies.
- **Remediation applied:** v2.13 D1 — added `on_spawn`, `on_exit`, `on_signal` callback hooks to pipeline base; sprint subclass provides hooks instead of overriding methods. AC-3 explicitly requires base behavior identical when hooks are None (so roadmap is unaffected).
- **Outcome:** Phase 4 acceptance showed `sprint/process.py` went from 201 → 183 lines (net -18, target was -58); the *duplication* was eliminated but new `super().__init__()` plumbing offset the raw line count. Verdict: EXEMPT FAIL on numeric target, PASS on architectural goal.
- **Still possible today (Auggie check):** UNKNOWN — would require reading `sprint/process.py` and `pipeline/process.py`. The phase-4 result file documents the hooks landed and tests pass.
- **Source artifacts:** `release-spec.md` D1 (lines 56-103); `tasklist/results/phase-4-result.md` (T04.03 FAIL with rationale).

### F-A3-10: Roadmap `--file` flag produced 0-byte outputs from bare terminal — replaced with inline embedding
- **Type:** FAILURE → REMEDIATION → SUCCESS
- **Pipeline step:** extract / generate-opus-architect / generate-sonnet-architect (every step that reads upstream inputs)
- **Symptom:** Roadmap executor passed input files via `--file` flags through `extra_args`; produced 0-byte output files when run from a bare terminal. Sprint's `@file` mechanism didn't have the same failure because it relied on the LLM agent actively reading files via the `Read` tool after launch (not content injection at prompt time).
- **Root cause (claimed):** Adversarial benchmark (`CLIRunner-benchmark/adversarial-output/merged-analysis.md`) determined the load-bearing claim ("`--file` only accepts remote `file_id:relative_path`") was empirically unverified; alternative hypotheses (timeout, prompt complexity, gate strictness) remained open. But the correct architectural answer was a *third* approach: Python-side file reading + inline prompt embedding, deterministic regardless of `--file` semantics.
- **Remediation applied:** v2.13 D3 / Phase 3 — `_embed_inputs()` helper added in `roadmap/executor.py:56` (now at line 531 per Auggie), `roadmap_run_step()` uses inline embedding for inputs under 100KB. 4 unit tests + 3 integration tests, 137 roadmap tests pass with 0 regressions.
- **Outcome:** Failure class "roadmap step succeeds with empty output" eliminated for inputs under 100KB. The 100KB guard preserves a fallback path for oversized inputs (not exhaustively tested).
- **Still possible today (Auggie check):** NO for sub-100KB inputs — Auggie confirms `_embed_inputs` exists at `roadmap/executor.py:531` and is invoked at line 1072 in the main step runner.
- **Source artifacts:** `merged-analysis.md` Sections 1-4; `release-spec.md` D3 (lines 123-142); `tasklist/results/phase-3-result.md`.

### F-A3-11: `_build_subprocess_argv` mis-classified as dead code; live in 7+ test sites
- **Type:** FAILURE (false positive from a planning analyst) → REMEDIATION (verdict overturned by ground-truth evidence)
- **Pipeline step:** OTHER (planning/scope analysis)
- **Symptom:** Variant A (pro-unification proposal) and the v2.13 release spec D2 both claimed `roadmap/executor.py:53-76 _build_subprocess_argv()` was dead code. Ground-truth grep showed it imported and called in `tests/roadmap/test_executor.py` (lines 21, 171) and `tests/roadmap/test_cli_contract.py` (6 call sites). Phase 4 verification (T04.04) confirmed FAIL: "Dead code premise incorrect. `_FORBIDDEN_FLAGS` and `_build_subprocess_argv` are actively referenced by 7+ test call sites across `test_executor.py` and `test_cli_contract.py`. These are production code, not dead code. The roadmap item's premise was incorrect."
- **Root cause (claimed):** Both architect variants asserted dead-code status without grepping the test tree. The "validate the contract independent of `ClaudeProcess` implementation" purpose was missed.
- **Remediation applied:** Removed from deletion scope; documented as test-contract infrastructure in adversarial merge document. Deviation surfaced explicitly in Phase 4 result.
- **Outcome:** Avoided removing live test infrastructure. Surfaced a real brittleness: planners can mark code dead without checking tests.
- **Still possible today (Auggie check):** NO for this specific symbol — Auggie shows `_build_subprocess_argv` no longer appears in current `roadmap/executor.py` (the function set is now `_embed_inputs` at line 531 and downstream callers). Whether the test references were also refactored is unconfirmed from this partition's artifacts.
- **Source artifacts:** `CLIRunner-benchmark/adversarial-output/merged-analysis.md` Section 4 (lines 125-147); `tasklist/results/phase-4-result.md` T04.04 (lines 18, 38-39).

### F-A3-12: v3.2 — CRITICAL — `execute_sprint()` never threaded TurnLedger; all per-task wiring hooks unreachable
- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint executor integration that consumes roadmap-pipeline output)
- **Symptom:** The v3.2 wiring gate was designed for `execute_phase_tasks()` (task-granularity). Production entry point `execute_sprint()` ran phases as monolithic Claude subprocesses and never instantiated a TurnLedger, never called `execute_phase_tasks()`. All per-task hooks (wiring, anti-instinct) were dead code in production.
- **Root cause (claimed):** RCA-1 ("Two execution models, one integration point"): codebase had a phase-level production path and a task-level test path; the wiring gate integrated with the test path only. The roadmap pipeline's spec-fidelity gate validated roadmap-vs-spec but had no mechanism to check whether the production sprint entry point could reach the hooks the spec mandated.
- **Remediation applied:** v3.2 remediation tasklist T01/T02: created `run_post_phase_wiring_hook()` and wired it into `execute_sprint()` main loop after `phase_results.append()`. QA reflection (`execution-qa-reflection.md` T02) initially flagged this as PARTIAL — function defined at executor.py:735 but never called — requiring a one-line fix.
- **Outcome:** Eventually closed. Auggie confirms `run_post_phase_wiring_hook` is invoked at `sprint/executor.py:1289` and `:1568` in current code; `_resolve_wiring_mode` is called at line 483; `DeferredRemediationLog` is constructed at line 1206-1209. The full lifecycle now exists.
- **Still possible today (Auggie check):** NO for the original wiring-gate-bypass symptom. The deeper class — "spec-fidelity gate doesn't compare spec vs production entry point" — is still possible because spec-fidelity is roadmap-vs-spec, not implementation-vs-spec (see F-A3-15).
- **Source artifacts:** `v3.2/roadmap-gap-analysis-merged.md` D2/RCA-1 (lines 44-47, 139-141); `v3.2/pipeline-weakness-analysis.md` Weakness 2 (lines 35-53); `v3.2/execution-qa-reflection.md` T02 (lines 46-54).

### F-A3-13: v3.2 — CRITICAL — `_resolve_wiring_mode()` written but never called (dead code on the production path)
- **Type:** FAILURE → REMEDIATION
- **Pipeline step:** wiring-verification
- **Symptom:** `_resolve_wiring_mode()` defined at `executor.py:420-446` (original line range; now lines 421-447 per A4 amendment), would pass any artifact-based gate, but `run_post_task_wiring_hook()` at line 473 read `config.wiring_gate_mode` directly. Goal-5d (scope-based mode resolution) never executed.
- **Root cause (claimed):** RCA-2 ("Spec evolution not propagated to call sites"): classic "wrote the function, forgot to wire it" pattern. Spec evolved from string-switch to scope-based resolution; bridge function written; call site never updated.
- **Remediation applied:** v3.2 T03 — one-line fix at executor.py:475: `mode = _resolve_wiring_mode(config)` replaces direct field access.
- **Outcome:** Confirmed by QA reflection (T03 YES, scope-based resolution works, fallback works). Auggie cross-check: `_resolve_wiring_mode(config)` now lives at `sprint/executor.py:483`.
- **Still possible today (Auggie check):** NO for this specific symbol. The general class ("dead code that produces no output artifact and therefore cannot be detected by any artifact-based gate") is the brittleness driver behind Pipeline Weakness 1 (no call-site wiring verification in pipeline gates) — still systemically possible.
- **Source artifacts:** `v3.2/roadmap-gap-analysis-merged.md` D1/RCA-2 (lines 35-40, 142-143); `v3.2/pipeline-weakness-analysis.md` Weakness 1 (lines 15-32); `v3.2/execution-qa-reflection.md` T03 (lines 24-32).

### F-A3-14: v3.2 — CRITICAL — Shadow mode broke evidence chain (no DeferredRemediationLog writes)
- **Type:** FAILURE → REMEDIATION
- **Pipeline step:** wiring-verification (shadow / TRAILING mode branch)
- **Symptom:** Shadow branch in `run_post_task_wiring_hook()` only called `_wiring_logger.info()`; never constructed `TrailingGateResult`, never appended to `DeferredRemediationLog`. The roadmap executor's wiring-verification step (`executor.py:424-439`) called `run_wiring_analysis()` + `emit_report()` directly and returned PASS without touching the trailing-gate infrastructure that already existed in `pipeline/trailing_gate.py`. Shadow findings emitted to a report file but never entered the deferred-remediation pipeline. Breaks Gamma IE-4 (spec-mandated adapter feeding findings into trailing gate pipeline).
- **Root cause (claimed):** RCA-5: Shadow mode implemented as a logging-only path; the spec's explicit adapter was overlooked. Structurally: pipeline executor created `TrailingGateRunner` when `grace_period > 0`, but the roadmap executor's *direct* execution of the wiring step short-circuited this path entirely (Pipeline Weakness 5).
- **Remediation applied:** v3.2 T04/T05 — `_log_shadow_findings_to_remediation_log()` added at executor.py:619-645 (Amendment A1 corrected `TrailingGateResult` constructor to `step_id`, `passed`, `evaluation_ms`, `failure_reason`); shadow branch in `run_post_task_wiring_hook()` now invokes it; `remediation_log` parameter threaded through `execute_phase_tasks()` and `run_post_phase_wiring_hook()`.
- **Outcome:** Evidence chain restored. Auggie confirms `DeferredRemediationLog` constructed at `sprint/executor.py:1206-1209` and threaded into wiring hooks.
- **Still possible today (Auggie check):** NO for this specific path. The underlying brittleness (gates validate report-file frontmatter, not evidence-chain participation) remains a structural property of the gate model.
- **Source artifacts:** `v3.2/roadmap-gap-analysis-merged.md` Gap #3 / RCA-5 (lines 109, 151-152); `v3.2/pipeline-weakness-analysis.md` Weakness 5 (lines 98-115).

### F-A3-15: v3.2 — HIGH — Spec-fidelity gate compares roadmap vs spec, never implementation vs spec
- **Type:** FAILURE (still possible)
- **Pipeline step:** spec-fidelity
- **Symptom:** SPEC_FIDELITY_GATE catches roadmap deviation from spec (e.g., DEV-001 through DEV-011 in `spec-fidelity.md`). But once the roadmap is approved, no pipeline gate verifies that the implementation matches the spec's naming contracts, field definitions, or interface signatures. Result in v3.2: KPI field names diverged (`wiring_net_cost`, `wiring_analyses_run`, `wiring_remediations_attempted` missing); TurnLedger fields used `wiring_turns_used` vs spec's `wiring_gate_cost`; SprintConfig scope-based fields not adopted. Naming drift accumulated unchecked.
- **Root cause (claimed):** Pipeline's fidelity loop ends at roadmap approval; implementation happens after the pipeline exits. There is no "implementation-fidelity" gate that compares actual Python field names, class signatures, and interface contracts against the spec via AST inspection.
- **Remediation applied:** Partial — v3.2 T09/T10/T11 closed specific naming gaps after the fact (post-hoc remediation tasklist). No pipeline-level fix; the spec-fidelity gate's scope was not expanded.
- **Outcome:** Naming gaps for v3.2 closed manually. The *structural weakness* persists: any future spec→implementation handoff has the same blind spot.
- **Still possible today (Auggie check):** YES. Auggie shows `_cross_refs_resolve` (gates.py line 48) and `_deviation_counts_reconciled` (line 770) — both operate on report markdown content. Neither parses spec text to extract field-name contracts and check them against AST of generated code. The brittleness driver — "fidelity loop terminates at roadmap, not at implementation" — is structurally unchanged.
- **Source artifacts:** `v3.2/roadmap-gap-analysis-merged.md` Gaps #6/#7/#8/RCA-4 (lines 112-114, 148-149); `v3.2/pipeline-weakness-analysis.md` Weakness 3 (lines 55-73); `spec-fidelity.md` DEV-001/002/003 HIGH cluster (lines 14-37).

### F-A3-16: v3.2 — Roadmap fabricates traceability IDs (Goal-1a, NFR-001) the spec never defines
- **Type:** FAILURE (still possible)
- **Pipeline step:** generate-opus-architect / generate-sonnet-architect
- **Symptom:** Roadmap uses `FR: Goal-1a, Goal-1b` and `NFR-001 ... NFR-008` requirement references. Spec defines numbered Goals 1-5 with no sub-letter granularity, and never defines numbered NFR identifiers. Traceability chain broken: implementers cannot look up "NFR-006" in the spec because it does not exist there.
- **Root cause (claimed):** LLM generator (Opus/Sonnet architect step) invented requirement IDs for tabular formatting convenience; SPEC_FIDELITY_GATE classified as LOW (DEV-009, DEV-010); no programmatic cross-reference check parsing IDs from spec and verifying each appears in roadmap.
- **Remediation applied:** Roadmap-level: marked LOW severity, recommended corrections (add IDs to spec or use real identifiers). Pipeline-level: none — no programmatic ID extraction was added.
- **Outcome:** v3.2 shipped with fabricated IDs. The cli-portify forensic report (`PlanningArtifacts/cli-portify-executor-noop-forensic-report.md`) Section 10 Mitigation 1 explicitly recommends "parse all `FR-NNN`, `NFR-NNN`, `SC-NNN` identifiers from the spec extraction; verify each appears in the roadmap body text; flag missing identifiers as HIGH severity regardless of LLM classification." Auggie shows `_cross_refs_resolve` exists in `roadmap/gates.py:48` — partial; full bidirectional parse-and-verify is not present.
- **Still possible today (Auggie check):** YES. `_cross_refs_resolve` validates that referenced IDs resolve to something, but does not detect fabricated IDs that don't exist in the source spec. Bidirectional spec→roadmap ID coverage check is not present.
- **Source artifacts:** `spec-fidelity.md` DEV-009/010 (lines 87-101); `cli-portify-executor-noop-forensic-report.md` Section 10 Mitigation 1 (lines 416-422).

### F-A3-17: cli-portify no-op executor — spec dispatched, roadmap dropped, code never wired
- **Type:** FAILURE (canonical exemplar of every fidelity weakness in this partition)
- **Pipeline step:** spec-fidelity (Link 1: spec → roadmap)
- **Symptom:** `superclaude cli-portify run` raced through 12 steps in milliseconds, wrote `return-contract.yaml: outcome: SUCCESS`, performed no real work. `_execute_step()` had a no-op default; `run_portify()` never passed `step_runner`; 8 real step modules in `cli_portify/steps/` were orphaned. Validation function existed at `config.py:125` but `commands.py:run()` never called it. Pipeline silently "succeeded" against nonexistent inputs.
- **Root cause (claimed):** Spec-to-roadmap fidelity failure (Primary): v2.24/v2.24.1/v2.25 specs specified three-way dispatch (`_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step`) with `PROGRAMMATIC_RUNNERS` dictionary and `test_programmatic_step_routing` integration test. Roadmap Phase 2 Key Action 4 reduced this to "Implement executor: sequential execution only" and Milestone M2 explicitly said "Sequential pipeline runs end-to-end with **mocked steps**." SPEC_FIDELITY_GATE (LLM-dependent semantic comparison) did not catch or did not escalate this as HIGH severity. Roadmap→Tasklist link passed vacuously because tasklist faithfully reproduced the already-incomplete roadmap description. Link 3 (Tasklist→Code fidelity gate) **does not exist** — the entire fidelity chain has no terminal verification step.
- **Remediation applied:** Bug-level fix: `STEP_DISPATCH` dictionary added in `cli_portify/steps/__init__.py` (Auggie confirms current state); `run_portify()` updated; validation call added to `commands.py`. Pipeline-level: forensic report enumerated five mitigation classes (programmatic cross-refs at Links 1-2, Link 3 implementation, wiring-verification gate category, smoke-test gate at release tier).
- **Outcome:** Bug fixed; structural mitigations partially applied. The forensic report's scoring puts unified-audit-gating v1.2.1 (as currently specified) at 4/10 for catching this bug class; 8/10 with Link 3; 9/10 with full chain plus deterministic ID cross-refs.
- **Still possible today (Auggie check):** YES at the structural level. Auggie shows `STEP_DISPATCH` exists in `cli_portify/steps/__init__.py` (this instance fixed), but the forensic report's findings about gate-validates-document-not-code-wiring remain. The pipeline's wiring-verification step now exists (`audit/wiring_gate.py`, `wiring_analyzer.py`) and was the v3.2 deliverable, but as F-A3-12/F-A3-15 show, it has its own integration gaps.
- **Source artifacts:** `PlanningArtifacts/cli-portify-executor-noop-forensic-report.md` Sections 1-10 (the entire 535-line document is one finding).

### F-A3-18: v3.2 — HIGH — Remediation lifecycle was stubbed (debit-only, no actual remediation execution)
- **Type:** FAILURE → REMEDIATION (with deferral)
- **Pipeline step:** remediate
- **Symptom:** BLOCKING wiring mode debited TurnLedger budget for remediation but performed no actual remediation: `_format_wiring_failure()`, `_recheck_wiring()`, `SprintGatePolicy.build_remediation_step()` all absent. `attempt_remediation()` from `trailing_gate.py` not called. Pipeline-level test-strategy step generated test cases for artifact structure, never tested whether remediation functions were importable callables.
- **Root cause (claimed):** RCA-3: BLOCKING path implemented the economic model (debit budget) without the behavioral model (spawn remediation subprocess, recheck, credit on success). Given 24-minute sprint execution constraint, implementer prioritized analysis engine + shadow integration over full remediation. Pipeline Weakness 4: pipeline treats remediation as artifact-generation problem (`produce remediation-tasklist.md that passes REMEDIATE_GATE`), never validates remediation execution mechanics.
- **Remediation applied:** v3.2 T06/T07/T08 — `_format_wiring_failure()` at executor.py:653-696, `_recheck_wiring()` at executor.py:704-727, full inline lifecycle at executor.py:563-604. Amendment A2 Option B: `attempt_remediation()` deferred to v3.3 in favor of inline approach (debit → format → recheck → credit-on-success / persist-FAIL).
- **Outcome:** Functional remediation lifecycle now exists. Auggie confirms `_format_wiring_failure` at `sprint/executor.py:666` and `_recheck_wiring` at `:717`. Full `attempt_remediation()` integration explicitly deferred.
- **Still possible today (Auggie check):** NO for the specific debit-without-remediation pattern (line 580 `prompt = _format_wiring_failure(...)`; line 590 `_recheck_wiring(...)` invocation confirmed). YES for the structural class — pipeline still does not include a "remediation smoke test" gate verifying that spec-declared remediation functions are importable with correct signatures.
- **Source artifacts:** `v3.2/roadmap-gap-analysis-merged.md` Gap #4/RCA-3 (lines 110, 145-146); `v3.2/pipeline-weakness-analysis.md` Weakness 4 (lines 77-94); `v3.2/execution-qa-reflection.md` T06/T07/T08 (lines 64-108).

### F-A3-19: v3.2 — Six verification tasks (T17–T22) skipped — no automated proof of P0 correctness
- **Type:** FAILURE (process)
- **Pipeline step:** test-strategy / certify
- **Symptom:** QA reflection found T17 (integration test: TurnLedger threading), T18 (unit test: `_resolve_wiring_mode` activation), T19 (KPI/contract verification), T20 (E2E shadow-mode pipeline), T21 (full regression suite run with captured evidence), T22 (gap closure audit) all SKIPPED. Plus T13 (budget scenarios 5-8) and T15 (performance benchmark) skipped. Overall verdict FAIL: "no automated verification that the wiring, remediation lifecycle, and KPI changes work correctly as an integrated system."
- **Root cause (claimed):** Implementation tasks (T01-T16) executed; verification wave deprioritized. Without dedicated tests covering the new functions, regressions become invisible until production failure.
- **Remediation applied:** Documented in `execution-qa-reflection.md` Remaining Issues. No evidence in this partition that verification tasks were subsequently completed.
- **Outcome:** Scorecard: 14/22 executed, 13/14 correct, 8/22 skipped, all 8 skipped are verification tasks. Overall FAIL verdict.
- **Still possible today (Auggie check):** UNKNOWN — would require checking current `tests/audit/` and `tests/sprint/` directories for the listed test functions. The structural class ("verification tier of a remediation tasklist can be skipped without halting the release") is still possible because verification tasks are not pipeline-gated.
- **Source artifacts:** `v3.2/execution-qa-reflection.md` Verification Wave sections (lines 110-200), Summary Scorecard (lines 256-269), Overall Verdict (lines 271-280).

### F-A3-20: SUCCESS — Adversarial debate (Opus vs Haiku) settled phase-structure / spec-closure / rollout-phase disputes
- **Type:** SUCCESS
- **Pipeline step:** debate / merge
- **Symptom:** Convergence score 0.72 over 2 rounds. Strong agreement areas: core technical architecture (AST-only, 3 analyzers, whitelist-first, phased enforcement), NFR-006 immutability, R6 (provider_dir_names mismatch) as highest risk, retrospective validation T11 requirement, floor-to-zero credit semantics, Anti-Instincts merge-conflict coordination. Remaining disputes: rollout-as-roadmap-phase vs operational concern; 4 vs 7 phase granularity; timeline-estimate governance.
- **Root cause (claimed):** N/A (this is functional protocol behavior).
- **Remediation applied:** Merged roadmap balanced the two positions; explicit prerequisites added for blocking items (budget constants, SprintGatePolicy validation); rollout treated as separate runbook concern.
- **Outcome:** Debate transcript preserved for future reference; areas of agreement (provider_dir_names risk, retrospective validation requirement) became hard requirements in subsequent tasklists.
- **Still possible today (Auggie check):** N/A — positive outcome demonstrating adversarial protocol functioning.
- **Source artifacts:** `v3.2_fidelity-refactor___/debate-transcript.md` Round 1-2 (lines 1-67), Convergence Assessment (lines 70-88).

### F-A3-21: v3.2 spec-fidelity gate flagged 3 HIGH-severity unilateral scope decisions correctly
- **Type:** SUCCESS (with caveat)
- **Pipeline step:** spec-fidelity
- **Symptom:** DEV-001 (`files_skipped` frontmatter field not in spec's 11-field contract), DEV-002 (whitelist scope expanded from `unwired_callables` to all three finding types), DEV-003 (provider directory heuristic removed from v1.0) all caught and escalated to HIGH severity. Gate fired correctly: `tasklist_ready: false` set; pipeline blocked until reconciliation.
- **Root cause (claimed):** Roadmap made scope decisions unilaterally (OQ-3, OQ-8, OQ-9 in roadmap) that conflicted with spec contract. Gate is supposed to surface exactly these.
- **Remediation applied:** Recommended corrections in fidelity report; subsequent reconciliation either updated spec or revised roadmap.
- **Outcome:** Demonstrates spec-fidelity gate working as intended for scope-level deviations. Caveat: gate is LLM-driven semantic comparison — false-negative risk persists (see F-A3-17 cli-portify case where the gate missed the executor dispatch reduction entirely).
- **Still possible today (Auggie check):** N/A — positive outcome. The gate's structural blind spot (LLM-only, no deterministic ID cross-ref) is documented in F-A3-15 and F-A3-16.
- **Source artifacts:** `spec-fidelity.md` DEV-001/002/003 (lines 12-37), Summary (lines 113-128).

---

## Cross-cutting patterns within this partition

- **"Written but not wired" recurs across all three releases.** v2.01 BUG-001 (`Skill` in activation but not in `allowed-tools`), v2.13 dead-code mis-classification (the `_build_subprocess_argv` test-infrastructure case showed how planners miss wiring), v3.2 `_resolve_wiring_mode` (function written, call site never updated), v3.2 `run_post_phase_wiring_hook` (defined at executor.py:735 but unwired into `execute_sprint` until QA caught it), and cli-portify no-op (`step_runner` parameter exists but never provided in production) — see F-A3-03, F-A3-11, F-A3-13, F-A3-17.

- **Gates validate artifact structure, not behavioral correctness.** Every gate in this partition (`SPEC_FIDELITY_GATE`, `TASKLIST_FIDELITY_GATE`, `WIRING_GATE` frontmatter checks, `REMEDIATE_GATE` tasklist structure checks) follows `(content: str) -> bool` or `(file: Path, criteria) -> tuple[bool, str|None]` signature. They check frontmatter fields, heading structure, minimum line counts — never that code components are reachable from their declared call sites — see F-A3-12, F-A3-13, F-A3-14, F-A3-15, F-A3-17, F-A3-18 and Pipeline Weakness 1.

- **Fidelity loop terminates at roadmap approval; no Link 3 to code.** Spec→Roadmap (SPEC_FIDELITY_GATE) and Roadmap→Tasklist (TASKLIST_FIDELITY_GATE) gates exist, but no gate verifies code satisfies tasklist acceptance criteria. Naming divergence in v3.2 (Gaps #6/#7/#8) and the entire cli-portify no-op class flow directly from this missing terminal link — see F-A3-15, F-A3-17.

- **LLM-only fidelity comparison has a false-negative blind spot.** SPEC_FIDELITY_GATE caught DEV-001/002/003 (F-A3-21) but missed cli-portify's executor-dispatch reduction entirely (F-A3-17). The pattern: gate catches obvious surface-level scope additions but misses semantic *reductions* where the roadmap silently drops a spec requirement. Deterministic ID cross-references (F-A3-16) would close part of this.

- **Adversarial debate works as a safety valve when both sides commit to convergence.** v2.13 (debate-convergence 0.72 rejected premature unification) and v3.2 (debate-convergence 0.72 settled phase-structure and spec-closure disputes) both demonstrate the protocol functioning correctly — see F-A3-08, F-A3-20. The success requires both variants to engage in good faith; a one-sided debate (variant doubling down) would not produce the same convergence.

- **Verification tier is silently skippable.** v3.2 shipped with 6 of 6 verification tasks (T17–T22) marked SKIPPED in the QA reflection, no pipeline gate halted the release on that basis — see F-A3-19. The verification wave is task-list discipline, not pipeline enforcement.

- **Pipeline-extraction boundaries hold when they reflect genuine semantic overlap.** Pipeline/sprint extraction succeeded at `PipelineConfig`/`ClaudeProcess` boundary (real shared semantics) but adversarial debate rejected extending it to `execute_sprint()` (overlap is a for-loop, divergence is 7 interleaved subsystems) — see F-A3-07, F-A3-08. The pattern: don't extract until semantic overlap forces the abstraction.

## Brittleness drivers identified

- **Artifact-centric gate model.** Every pipeline gate has the signature "produce file → validate file passes structural criteria." Dead code, unwired functions, and missing call edges produce no output artifact and are therefore *categorically undetectable* by this gate model. The cli-portify no-op shipped a pipeline that returned `outcome: SUCCESS` with all 12 steps "completed" because the no-op default emitted a structurally valid `return-contract.yaml`. (Drives F-A3-13, F-A3-14, F-A3-17, F-A3-18; Pipeline Weakness 1, 4, 5.)

- **Fidelity chain has no terminal verification link.** Spec→Roadmap and Roadmap→Tasklist gates exist as deterministic Python checks layered atop LLM-generated reports, but Tasklist→Code does not exist. The transitive trust model assumes every link is trustworthy; v3.2 naming divergence and cli-portify executor reduction both exploited this missing link. (Drives F-A3-12, F-A3-15, F-A3-17.)

- **LLM-only semantic comparison lacks deterministic invariants.** SPEC_FIDELITY_GATE relies on Claude to identify deviations and classify severity; Python only enforces `high_severity_count == 0` in the LLM-produced frontmatter. No programmatic check parses `FR-NNN`/`NFR-NNN`/`SC-NNN` identifiers from the spec and verifies bidirectional coverage in roadmap. The gate cannot distinguish "no deviations found" from "deviations not detected by the LLM." (Drives F-A3-16, F-A3-17.)

- **Spec contracts are not machine-verified against generated artifacts.** Roadmaps fabricate traceability IDs (Goal-1a, NFR-001) that the spec never defines. Field-name divergence between spec and TurnLedger/KPI/SprintConfig accumulates because no AST-level check parses spec field contracts and verifies the implementation honors them. (Drives F-A3-15, F-A3-16.)

- **Two execution models, one integration point.** The codebase has a phase-level production path (`execute_sprint`) and a task-level test path (`execute_phase_tasks`). New hooks (anti-instinct, wiring) integrate with the test path only; the spec-fidelity gate compares roadmap vs spec and has no mechanism to verify the *production entry point* reaches the integration hooks the spec mandates. This is a *structural* brittleness because it makes "feature works in tests but is dead code in production" the default, not the exception. (Drives F-A3-12.)

- **Adversarial planner findings can mis-classify live code as dead.** Both architect variants in v2.13 marked `_build_subprocess_argv` as dead code without grepping the test tree; the function was live in 7+ test call sites. The brittleness: planner agents reason about production call graphs and forget that test-infrastructure call sites are also valid call sites. Phase 4 verification caught this — but only because the EXEMPT-tier check ran post-implementation. (Drives F-A3-11.)

- **Remediation lifecycle is artifact-generation, not behavior-validation.** Pipeline's REMEDIATE_GATE checks `remediation-tasklist.md` structure; never verifies the spec-declared remediation functions (`_format_wiring_failure`, `_recheck_wiring`, `build_remediation_step`) exist as importable callables with the right signatures. The v3.2 BLOCKING path debited budget for non-existent remediation work for an unknown duration before detection. (Drives F-A3-18; Pipeline Weakness 4.)

- **Verification wave is task-list discipline, not pipeline gate.** When implementation tasks complete but verification tasks (T17–T22) get skipped, no pipeline check halts the release. The remediation tasklist is treated as an MDTM checklist where verification tier compliance is honor-system. (Drives F-A3-19.)
