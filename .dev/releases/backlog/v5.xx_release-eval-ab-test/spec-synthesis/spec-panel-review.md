# Spec Panel Review: Post-Release Eval & A/B Testing CLI Tool

**Spec**: `.dev/releases/backlog/v5.xx_release-eval-ab-test/release-eval-spec.md`
**Template**: `src/superclaude/examples/release-spec-template.md`
**Decision Record**: `.dev/releases/backlog/v5.xx_release-eval-ab-test/conversation-decisions.md`
**Review Date**: 2026-03-19
**Reviewer**: Multi-expert specification review panel (4 panels)

---

## Summary Table

| # | Finding | Panel | Severity | Section | Description | Remediation |
|---|---------|-------|----------|---------|-------------|-------------|
| 1 | Missing Section 9 | Completeness | MINOR | Spec structure | Template Section 9 (Migration & Rollout) is absent. Template marks it `[CONDITIONAL: refactoring, portification]`, and this is `new_feature`, so omission is acceptable but should be explicitly noted. | Add a one-line note: "Section 9 omitted (not applicable to new_feature spec type)." |
| 2 | Section 4.3 missing | Completeness | INFO | Section 4 | Template Section 4.3 (Removed Files) is conditional on refactoring/portification. Correctly omitted for new_feature. | No action required. |
| 3 | Self-assessed quality scores | Completeness | MINOR | Frontmatter | The spec assigns itself scores (clarity: 9.0, completeness: 9.5, etc.). These are self-awarded, not from a quality gate run. | Either remove self-assessed scores or note they are provisional pending `/sc:spec-panel` review. |
| 4 | Decision record says "Hybrid Skill-First + Parallel Python Library"; spec says "CLI-first" | Completeness | MAJOR | Section 2.1, D-08 | The decision record (Section 2) explicitly chose hybrid skill-first with parallel Python library. The spec overrides this to CLI-first and documents the rationale, but the override is significant enough that it should be more prominently flagged. | Add a "Decision Override" callout box at Section 2.1, row "Build approach", explicitly stating: "Overrides conversation-decisions.md Section 2. Original: skill-first. New: CLI-first. Rationale: 6-prompt workflow invalidated discovery rationale." This is already partially present in the table but buried. |
| 5 | Decision record says "5 runs each" for all tiers; spec says tiered (5/10/5) | Completeness | MINOR | D-01 | The spec correctly overrides the decision record's flat "5 each" with tiered minimums and documents the statistical rationale. Override is well-documented in Section 11. | No action required; well-documented deviation. |
| 6 | Decision record lists D-06 through D-10 as open; spec resolves D-07 through D-10 but D-06 resolution is weak | Completeness | MAJOR | Section 11, D-06 | D-06 asks "Ship scoring library separately or with ab-test?" The spec's resolution says "Ship with slice 3 as first user-testable release" but this is only stated in Section 11's resolution column. Appendix D's delivery plan shows Slices 1-2 as "Internal milestone" and Slice 3 as "v1.0-alpha". The resolution is consistent but should be explicitly stated in the delivery plan section, not just in the open items table. | In Section 4.6 (Implementation Order), add a note: "Slices 1-2 are internal milestones; Slice 3 is the first user-testable release (resolves D-06)." |
| 7 | EvalConfig does not extend PipelineConfig | Architecture | MAJOR | Section 4.5, FR-EVAL.1 | FR-EVAL.1 says `Dependencies: pipeline/models.py (PipelineConfig base class)`. The data model in Section 4.5 shows `EvalConfig` as a standalone dataclass with a comment "Extends PipelineConfig concepts" but does NOT inherit from `PipelineConfig`. `PipelineConfig` has fields `work_dir`, `dry_run`, `max_turns`, `model`, `permission_flag`, `debug`, `grace_period`. `EvalConfig` duplicates `work_dir`, `dry_run`, `max_turns`, `debug` but adds many eval-specific fields and omits `permission_flag`, `grace_period`. The "extends" claim is misleading -- it is composition-by-duplication, not inheritance. | Clarify the relationship. Either: (a) make `EvalConfig` inherit from `PipelineConfig` and override/extend, or (b) change the description to "Mirrors relevant PipelineConfig fields; does not inherit." If (a), document which PipelineConfig fields are unused (permission_flag, grace_period) and why. |
| 8 | GateCriteria pattern mismatch | Architecture | MAJOR | Section 5.2 | The spec maps eval layers to gate tiers (STRICT/STANDARD) but the existing `GateCriteria` dataclass in `pipeline/models.py` has fields: `required_frontmatter_fields`, `min_lines`, `enforcement_tier`, `semantic_checks`. Eval layers do not use `required_frontmatter_fields` or `min_lines`. The spec's "Semantic Checks" column lists functions like `_file_exists()`, `_score_above_threshold()` which are novel, not existing semantic checks. The spec claims to reuse the gate framework but actually needs a different gate model. | Either: (a) define a new `EvalGateCriteria` dataclass specific to eval layers, documenting how it relates to but differs from `GateCriteria`, or (b) extend `GateCriteria` with optional eval-specific fields and document backward compatibility. The current description implies drop-in reuse that will not work. |
| 9 | ClaudeProcess output_format mismatch | Feasibility | MINOR | FR-EVAL.3 | The spec says `run_judge()` invokes ClaudeProcess with `output_format="text"`. The existing ClaudeProcess in `pipeline/process.py` supports `output_format="stream-json"` (default) and `output_format="text"`. This is correct. However, the spec also says `max_turns=15` for judge, while EvalConfig has `max_turns=100`. The judge-specific max_turns should be documented as a separate parameter, not conflated with the config default. | Add `judge_max_turns: int = 15` to EvalConfig, or document that `run_judge()` overrides the config's max_turns. |
| 10 | runner.py depends on isolation.py but dependency graph shows reverse | Architecture | MAJOR | Section 4.4 | The dependency graph in Section 4.4 shows `eval/isolation.py` -> `eval/runner.py` (isolation feeds into runner), which is correct directionally. However, the graph also shows `eval/runner.py` -> `eval/spec_parser.py`, which is incorrect. The runner does not depend on spec_parser; the release_eval executor depends on both runner and spec_parser. The CLI executor modules (`cli/release_eval/executor.py`) should depend on both, not the runner itself. | Fix the dependency graph. runner.py should NOT depend on spec_parser.py. The correct chain is: `eval/spec_parser.py` -> `eval/suite_generator.py` -> `cli/release_eval/executor.py` (which also uses `eval/runner.py`). |
| 11 | release_eval/reporter.py listed in decision record architecture but not in spec | Architecture | MINOR | Section 4.1 | The decision record (Section 5) lists `release_eval/reporter.py` as a separate file. The spec consolidates reporting into `eval/reporter.py` (shared). This is a reasonable simplification. | No action required; shared reporter is better. |
| 12 | No `from_dict` on most dataclasses | Testability | MINOR | Section 4.5 | FR-EVAL.1 AC says "All dataclasses support to_dict/from_dict for JSONL round-trip serialization." But Section 4.5 only shows `to_dict`/`from_dict` on `Score` and `to_dict` on `RunResult`. `TestVerdict`, `EvalReport`, `ABComparison`, `EvalConfig`, `ParsedSpec`, `EvalSuiteTest`, `EvalSuite` all lack serialization methods. | Either: (a) add `to_dict`/`from_dict` stubs to all dataclasses in Section 4.5, or (b) note that serialization will be implemented but is elided from the spec for brevity, referencing FR-EVAL.1 AC-6 as the binding requirement. |
| 13 | NFR-EVAL.14 target may be unachievable | Feasibility | MAJOR | Section 6 | NFR-EVAL.14 states "Full roadmap run < 15 minutes." A single `superclaude roadmap run` invocation involves multiple LLM calls across multiple pipeline steps. With Sonnet, a full roadmap generation for a complex spec can take 10-20 minutes. If the eval runs 5 repetitions, the total wall time is 50-100 minutes for quality layer alone, even with parallelism. The 15-minute target is per-run, but the wording "Eval spec execution time" is ambiguous -- does it mean per-run or total? | Clarify NFR-EVAL.14: "Wall-clock per individual run of the command under test < 15 minutes." Also add a note that total eval wall time scales with runs * models and is not bounded by this NFR. |
| 14 | scipy.stats is optional but p-values are required | Feasibility | MINOR | FR-EVAL.5 | FR-EVAL.5 says `Dependencies: stdlib statistics, optional scipy.stats`. But p-values (Welch's t-test) and Cohen's d are required outputs. Without scipy, these cannot be computed from stdlib alone. The `statistics` module does not include t-test or p-value functions. | Either: (a) make scipy a required dependency (not optional) for the eval package, or (b) implement Welch's t-test manually using only stdlib math (feasible but more work). Document the choice explicitly. |
| 15 | No test for worktree isolation cleanup on SIGINT | Testability | MINOR | Section 8 | Section 8.3 (Manual/E2E) includes "Isolation safety under SIGINT" but there is no automated test for this in Section 8.1 or 8.2. Signal handling is notoriously hard to test automatically, but a basic test that registers the handler and verifies cleanup callback is feasible. | Add an integration test: "Signal handler registration and cleanup callback" that verifies atexit/signal handlers are registered and that the cleanup function restores state when called. |
| 16 | Vanilla prompt library has only 3 commands | Completeness | MINOR | Section 5.4 | The vanilla-prompts.yml schema shows prompts for sc:roadmap, sc:explain, sc:tasklist. The project has 27+ commands. The spec says "vanilla-equivalent prompt library initial set" (Phase 6b) but does not define the minimum set or how new commands must provide vanilla equivalents. | Add an AC to FR-EVAL.11 or FR-EVAL.12: "Vanilla prompt library must include prompts for all commands under test. Commands without vanilla prompts cannot be tested in value/deprecation tiers; CLI prints a clear error." |
| 17 | No cleanup subcommand in CLI surface | Completeness | MINOR | Section 5.1, Section 7 | Risk assessment mentions `superclaude release-eval cleanup` for worktree cleanup, but this subcommand is not listed in the CLI surface (Section 5.1). | Add `cleanup` subcommand to the release-eval CLI surface table, or remove the reference from the risk assessment. |
| 18 | Test plan does not cover AB value/deprecation tiers | Testability | MINOR | Section 8.2 | Integration tests list "End-to-end ab-test regression tier" but there is no integration test for value validation or deprecation audit tiers. These are covered only in Manual/E2E (Section 8.3). | Add integration tests for value validation tier (3-way comparison) and deprecation tier (vanilla vs current). Even if they use small run counts (N=2), they validate the orchestration logic. |
| 19 | `pipeline/state.py` extraction is a refactoring risk | Feasibility | MINOR | Section 4.1, 4.2 | The spec proposes extracting `write_state`/`read_state` from `roadmap/executor.py` to `pipeline/state.py`. The roadmap executor has 16 call sites for these functions. This is a mechanical refactor but touches a critical code path. | Ensure the refactoring is its own slice/PR with dedicated regression tests before any eval code depends on it. The spec's Phase 1a placement is correct. |
| 20 | ab_test CLI `commands.py` vs decision record `main.py` | Architecture | INFO | Section 4.1 | Decision record names the CLI entry point `main.py`; spec names it `commands.py`. The spec's choice is more consistent with the existing `cli/roadmap/commands.py` pattern. | No action required; spec naming is better. |
| 21 | `fcntl` is Linux-only | Feasibility | MINOR | FR-EVAL.6 | The isolation mechanism lists `fcntl` as a dependency for file locking. `fcntl` is not available on Windows. If cross-platform support is ever needed, this will break. | Add a note: "fcntl is Linux/macOS only. Windows support deferred." Or use `filelock` package for cross-platform locking. |
| 22 | No explicit error handling contract | Completeness | MINOR | Section 5 | The spec defines happy-path interfaces but does not specify error return types or error reporting contracts. What does `execute_eval_suite()` return on partial failure? What does `run_judge()` return on timeout? | Add a subsection to Section 5 defining error contracts: return types for failure cases, exception hierarchy (or lack thereof), and how partial results are surfaced to the caller. |
| 23 | Brainstorm gap table schema differs from template | Completeness | MINOR | Section 12 | Template's gap table has columns: Gap ID, Description, Severity, Affected Section, Persona. The spec's gap table has columns: Gap ID, Description, Severity, Affected Section, Resolution. The spec replaces "Persona" with "Resolution" which is more useful for a post-synthesis spec, but diverges from template. | Acceptable divergence. The Resolution column is more valuable than Persona for a finalized spec. Document the deviation or update the template. |
| 24 | No `--output` flag on `release-eval` CLI | Completeness | MINOR | Section 5.1 | The `ab-test` CLI has `--output` to control where results go. The `release-eval` CLI lacks this; NFR-EVAL.6 says results go to `evals/` within the release dir. But what if the release dir is read-only (e.g., on a shared filesystem)? | Add `--output` flag to release-eval CLI surface, defaulting to `<release-dir>/evals/` but overridable. |
| 25 | Template Section 5.3 (Phase Contracts) not addressed | Completeness | INFO | Section 5 | Template marks Section 5.3 as conditional for portification/infrastructure. This spec is new_feature, so omission is correct. | No action required. |

---

## Panel 1: Completeness Review

### Template Coverage

The spec covers all mandatory template sections for a `new_feature` spec type:

- [x] Section 1: Problem Statement (with Evidence + Scope Boundary)
- [x] Section 2: Solution Overview (with Design Decisions + Workflow)
- [x] Section 3: Functional Requirements (15 FRs, all with ACs and dependencies)
- [x] Section 4: Architecture (New Files, Modified Files, Dependency Graph, Data Models, Implementation Order)
- [x] Section 5: Interface Contracts (CLI Surface, Gate Criteria, YAML Schemas)
- [x] Section 6: Non-Functional Requirements (15 NFRs with targets and measurements)
- [x] Section 7: Risk Assessment (10 risks with mitigations)
- [x] Section 8: Test Plan (Unit, Integration, Manual/E2E)
- [ ] Section 9: Migration & Rollout -- omitted (acceptable for new_feature but not noted)
- [x] Section 10: Downstream Inputs
- [x] Section 11: Open Items (all 10 decisions resolved)
- [x] Section 12: Brainstorm Gap Analysis
- [x] Appendix A: Glossary
- [x] Appendix B: Reference Documents
- [x] Appendix C: Scoring Rubric (bonus; not in template)
- [x] Appendix D: Delivery Plan (bonus; not in template)

### Sentinel Check

Zero `{{SC_PLACEHOLDER:*}}` sentinels remain. PASS.

### AC Coverage

All 15 FRs have explicit acceptance criteria with checkboxes. Every AC describes a verifiable condition. PASS.

### Decision Resolution

All 10 open decisions (D-01 through D-10) from the decision record are resolved in the spec with documented rationale. Two decisions were overridden from the original record (D-01 minimum runs, D-08 build approach) with explicit justification. PASS.

### Delivery Plan

The 7-slice plan in Appendix D has clear deliverables, test targets, and release labels. The dependency chain (1->2->3->4 and 1->2->5->6->7) is clearly stated with parallelization opportunity after Slice 2. PASS.

---

## Panel 2: Feasibility Review

### Module Interfaces

Each module has a clear single responsibility and well-defined inputs/outputs. The 10-module eval library plus 2 CLI packages is a reasonable decomposition. The dependency graph is acyclic when the runner->spec_parser error (Finding #10) is corrected.

### NFR Achievability

- **NFR-EVAL.1 (suite generation < 60s)**: Achievable. Suite generation is spec parsing + YAML emission, no LLM calls.
- **NFR-EVAL.3 (CV < 0.15)**: This is a target, not a hard requirement. LLM output variance depends on the model and prompt. Achievable for structural dimensions, may be challenging for subjective dimensions like "actionability."
- **NFR-EVAL.14 (< 15 minutes per run)**: Ambiguous (Finding #13). Per-run is feasible; total eval time is unbounded.

### Isolation Safety

The three-mechanism approach (worktree primary, env-var supplementary, directory rename fallback) is sound. Worktree isolation avoids filesystem mutation of `.claude/`, which is the safest approach. The fallback chain is well-ordered by safety. The `fcntl` platform limitation (Finding #21) is a known constraint.

### Judge Agent Viability

The rubric-anchored scoring approach with anchors at 1, 3, 5, 7, 10 is proven in LLM evaluation literature. The lenient parsing fallback (regex after JSON failure) is pragmatic. The `value=0.0` default for unparseable responses is appropriate since quality layer is advisory, not gating.

### Parallelization

The multi-run engine design is practical. Default sequential execution with opt-in `--parallel` via worktrees avoids resource exhaustion. The file lock prevents the dangerous concurrent case.

---

## Panel 3: Testability Review

### Automated Test Coverage

Every FR has at least one unit test in Section 8.1. The test plan covers:
- Data model serialization round-trips
- Statistical computation correctness with known inputs
- Parser behavior on valid and malformed inputs
- Isolation mechanism setup/teardown
- Report formatting structure

### Measurability

All ACs are binary (PASS/FAIL) or have numeric thresholds. No subjective ACs detected. PASS.

### Layer Coverage

- **Unit tests**: 23 tests across 8 test files. Good coverage of core library.
- **Integration tests**: 11 tests covering cross-module interactions.
- **Manual/E2E tests**: 6 scenarios covering real-world usage.

### 4-Layer Failure Model Testability

- **Structural layer**: Fully testable (file existence checks).
- **Functional layer**: Fully testable (exit code + artifact checks).
- **Quality layer**: Testable via integration test with real judge invocation.
- **Regression layer**: Testable via known score distributions in unit tests; real-world validation via E2E.

### Gaps

The value validation and deprecation tiers lack integration tests (Finding #18). Signal handler cleanup lacks automated tests (Finding #15).

---

## Panel 4: Architecture Consistency

### File Path Accuracy

Verified against the live codebase:
- `src/superclaude/cli/pipeline/models.py` -- EXISTS, contains `PipelineConfig`, `GateCriteria`, `SemanticCheck`, `StepStatus`
- `src/superclaude/cli/pipeline/process.py` -- EXISTS, contains `ClaudeProcess` with `output_format` and `max_turns` parameters
- `src/superclaude/cli/pipeline/gates.py` -- EXISTS, contains `gate_passed()`
- `src/superclaude/cli/roadmap/executor.py` -- EXISTS, contains `write_state`/`read_state` (16 call sites confirmed)
- `src/superclaude/cli/sprint/executor.py` -- EXISTS, contains `IsolationLayers`, `AggregatedPhaseReport.to_markdown()`
- `scripts/eval_runner.py` -- EXISTS
- `scripts/ab_test_workflows.py` -- EXISTS
- `.dev/releases/complete/` -- EXISTS with 37 completed releases (spec says "10+", actual count is 37)
- `src/superclaude/cli/pipeline/state.py` -- DOES NOT EXIST (correctly listed as new file to create)

All file path references in the spec are accurate. PASS.

### Module Layout Consistency

Section 4.1 (New Files) lists 18 new files. Section 4.4 (Dependency Graph) covers all eval modules and CLI packages. The data model in Section 4.5 aligns with the module descriptions. One inconsistency: the dependency graph incorrectly shows `runner.py` depending on `spec_parser.py` (Finding #10).

### CLI-Config Alignment

The CLI surface (Section 5.1) options map correctly to `EvalConfig` fields:
- `--runs` -> `runs_per_test`
- `--models` -> `models`
- `--judge-model` -> `judge_model`
- `--dry-run` -> `dry_run`
- `--parallel` -> `parallel`
- `--debug` -> `debug`
- `--timeout` -> `timeout_per_run`
- `--force` -> `force`
- `--approve` -> `approve`

Missing from EvalConfig: `--layers` (release-eval only), `--regenerate` (release-eval only), `--tier` (ab-test only), `--args`, `--input`. These are CLI-only options not persisted in config, which is acceptable for command-specific arguments. However, `--layers` and `--tier` affect execution behavior and should arguably be part of config or a command-specific config subclass.

### GateCriteria Compatibility

The existing `GateCriteria` pattern (Finding #8) uses `required_frontmatter_fields`, `min_lines`, `enforcement_tier`, `semantic_checks`. The eval layers need different gate semantics (score thresholds, p-value thresholds). The spec implies reuse but the actual gate model needs adaptation.

---

## Overall Verdict

**PASS WITH CAVEATS**

The spec is comprehensive, well-structured, and ready to drive roadmap generation. All template sections are covered, all open decisions are resolved, all FRs have testable ACs, and the architecture references real codebase files accurately. The 4-agent synthesis and adversarial debate process produced a high-quality spec.

**CRITICAL findings: 0** -- Nothing blocks roadmap generation.

**MAJOR findings: 5** -- Should be addressed before or during Phase 1 implementation:

1. **Finding #7 (EvalConfig/PipelineConfig relationship)**: Clarify inheritance vs composition. This affects how implementers structure the config module.
2. **Finding #8 (GateCriteria pattern mismatch)**: The eval gate model diverges from the existing pattern. Needs explicit documentation of how eval gates work alongside pipeline gates.
3. **Finding #10 (Dependency graph error)**: runner.py should not depend on spec_parser.py. Fix the graph before it misleads implementation ordering.
4. **Finding #13 (NFR-EVAL.14 ambiguity)**: "Full roadmap run < 15 minutes" must be clarified as per-run to avoid confusion.
5. **Finding #4 (Decision override prominence)**: The CLI-first override of the decision record's skill-first approach should be more prominently flagged.

These 5 MAJOR findings are addressable with spec edits (no design changes required). The roadmap generator should be able to work from the spec as-is, with these issues noted as constraints for implementation.
