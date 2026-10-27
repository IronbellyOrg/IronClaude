

---
spec_source: sprint-preflight-executor-spec.md
generated: "2026-03-16T00:00:00Z"
generator: claude-opus-4-6-requirements-extractor
functional_requirements: 8
nonfunctional_requirements: 5
total_requirements: 13
complexity_score: 0.55
complexity_class: moderate
domains_detected: 4
risks_identified: 5
dependencies_identified: 6
success_criteria_count: 8
extraction_mode: full
---

## Functional Requirements

**FR-001** (FR-PREFLIGHT.1): **Execution Mode Annotation Parsing** — The sprint runner MUST read an `Execution Mode` column from the Phase Files table in `tasklist-index.md` and store the value on each `Phase` object. The `Phase` dataclass gains an `execution_mode: str` field defaulting to `"claude"`. Recognized values: `claude`, `python`, `skip` (case-insensitive). Unrecognized values MUST raise `click.ClickException`. Missing column defaults all phases to `"claude"`.

**FR-002** (FR-PREFLIGHT.2): **Pre-Sprint Preflight Executor** — A new `execute_preflight_phases()` function MUST execute all `python`-mode phases before the main Claude loop using `subprocess.run()`. It iterates `config.active_phases` where `execution_mode == "python"`, parses tasks via `parse_tasklist()`, extracts shell commands from `**Command:**` fields, executes via `subprocess.run(shell=False, capture_output=True, timeout=120)`, captures stdout/stderr/exit_code/duration, builds `TaskResult` per task, and returns `list[PhaseResult]`.

**FR-003** (FR-PREFLIGHT.3): **Command Field Extraction** — `parse_tasklist()` MUST be extended to extract a `**Command:**` field from task blocks into a new `command` attribute on `TaskEntry`. Backtick delimiters are stripped. Tasks without the field have `command == ""`. Commands with pipes, redirects, and quoted arguments MUST be preserved verbatim.

**FR-004** (FR-PREFLIGHT.4): **Classifier Registry** — A new module `src/superclaude/cli/sprint/classifiers.py` MUST provide a `CLASSIFIERS` dict of named Python callables with signature `(exit_code: int, stdout: str, stderr: str) -> str`. `parse_tasklist()` extracts `| Classifier |` metadata into `TaskEntry.classifier`. Missing classifier lookup MUST raise `KeyError`. At least one built-in classifier (`empirical_gate_v1`) MUST be provided.

**FR-005** (FR-PREFLIGHT.5): **Evidence Artifact Writing** — The preflight executor MUST write structured evidence files for each task to `artifacts/D-NNNN/evidence.md` (or `artifacts/<task_id>/evidence.md`). Evidence includes: command executed, exit code, stdout (truncated to 10KB), stderr (truncated to 2KB), wall-clock duration, and classification label. Directories created with `mkdir(parents=True, exist_ok=True)`.

**FR-006** (FR-PREFLIGHT.6): **Result File Generation** — The preflight executor MUST write a `phase-N-result.md` file compatible with `_determine_phase_status()` using `AggregatedPhaseReport.to_markdown()`. YAML frontmatter includes `source: preflight`. Contains `EXIT_RECOMMENDATION: CONTINUE` (all pass) or `EXIT_RECOMMENDATION: HALT` (any fail). Existing parser MUST parse it without modification.

**FR-007** (FR-PREFLIGHT.7): **Main Loop Phase Skipping** — The main `execute_sprint()` phase loop MUST skip phases already handled by preflight (`execution_mode == "python"`) and phases annotated `skip` (with `PhaseStatus.SKIPPED`). Sprint outcome MUST correctly reflect preflight + main loop results combined.

**FR-008** (FR-PREFLIGHT.8): **PhaseStatus.PREFLIGHT_PASS Enum Value** — Add `PhaseStatus.PREFLIGHT_PASS = "preflight_pass"` to the enum. `is_success` MUST return `True`, `is_failure` MUST return `False`. Logger and TUI MUST handle the new status without errors.

## Non-Functional Requirements

**NFR-001** (NFR-PREFLIGHT.1): **Preflight Execution Speed** — Preflight phase execution MUST complete in < 30 seconds for 5 EXEMPT-tier tasks. Measured by wall-clock timing in execution log.

**NFR-002** (NFR-PREFLIGHT.2): **Zero API Token Consumption** — Python-mode phases MUST consume zero Claude API tokens. No `ClaudeProcess` is instantiated for python-mode phases.

**NFR-003** (NFR-PREFLIGHT.3): **Result File Compatibility** — `_determine_phase_status()` MUST parse preflight-generated result files identically to Claude-generated ones. Validated by unit test exercising both sources.

**NFR-004** (NFR-PREFLIGHT.4): **Single-Line Rollback** — Removing the `execute_preflight_phases()` call MUST revert behavior to all-Claude execution with no other changes required.

**NFR-005** (NFR-PREFLIGHT.5): **Command Timeout** — Per-command timeout of 120 seconds, configurable via `subprocess.run(timeout=...)`.

## Complexity Assessment

**Score: 0.55 / 1.0 — Moderate**

**Rationale:**
- **Domain breadth (moderate):** Touches 4 domains — subprocess management, markdown parsing, classification logic, and sprint orchestration — but all within a single Python package.
- **Integration surface (moderate):** Modifies 3 existing files and adds 3 new files. Integrates with existing `discover_phases()`, `parse_tasklist()`, `execute_sprint()`, `AggregatedPhaseReport`, and `_determine_phase_status()`.
- **New abstractions (low-moderate):** Introduces classifier registry pattern and preflight executor hook, but both are straightforward.
- **Risk profile (low-moderate):** Primary risk is result file format compatibility; mitigated by reusing existing `AggregatedPhaseReport.to_markdown()`.
- **Estimated LOC:** ~400 new code + ~200 tests = ~600 total, well within moderate range.
- **No external service dependencies:** All execution is local subprocess calls.

## Architectural Constraints

1. **UV-only Python execution** — All Python operations must use `uv run`; no bare `python` or `pip`.
2. **subprocess.run with shell=False** — Commands MUST be executed with `shell=False` for security; command strings split via `shlex.split()`.
3. **Pre-sprint hook placement** — Preflight execution MUST occur before the main phase loop in `execute_sprint()`, not inline.
4. **Phase-level annotation only** — Execution mode is phase-level, not per-task. Mixed python/claude within a single phase is out of scope.
5. **Existing parser compatibility** — `_determine_phase_status()` MUST NOT be modified; preflight result files must conform to its expected format.
6. **Source-of-truth in src/superclaude/** — All new modules go under `src/superclaude/cli/sprint/`. Dev copies synced via `make sync-dev`.
7. **Annotation values restricted to three** — `claude`, `python`, `skip`. No other values permitted.
8. **No changes to Claude-mode execution path** — The existing `ClaudeProcess` subprocess logic remains untouched.

## Risk Inventory

**RISK-001** (Severity: High) — **Result file format drift.** Preflight-generated result files could diverge from Claude-generated format, causing `_determine_phase_status()` parse failures and sprint halts.
*Mitigation:* Shared unit test validates both `AggregatedPhaseReport.to_markdown()` output and `_determine_phase_status()` parsing against the same fixture.

**RISK-002** (Severity: Medium) — **Environment mismatch.** Shell commands may require environment variables, paths, or tools not available in the preflight execution context.
*Mitigation:* Evidence files capture full stderr; preflight logs command and environment details for diagnosis.

**RISK-003** (Severity: Medium) — **Command quoting/escaping issues.** The `**Command:**` field may contain pipes, redirects, or special characters that break `shlex.split()`.
*Mitigation:* Parse as single string, split via `shlex.split()`, comprehensive tests with pipes and quoted arguments.

**RISK-004** (Severity: Low) — **Classifier bugs.** A bug in a classifier function could misclassify output, causing downstream phases to make wrong decisions.
*Mitigation:* Unit tests per classifier with known inputs/outputs; classifier exceptions caught, logged, and treated as task failure.

**RISK-005** (Severity: Low) — **Future mixed-mode phases.** Future phases may need mixed python/claude tasks within a single phase, which is unsupported by phase-level annotation.
*Mitigation:* Phase-level annotation is sufficient for known patterns; migration path to per-task annotation is non-breaking and deferred.

## Dependency Inventory

1. **subprocess (stdlib)** — `subprocess.run()` for command execution with `capture_output=True`, `timeout`, and `shell=False`.
2. **shlex (stdlib)** — `shlex.split()` for safe command string tokenization.
3. **click** — `click.ClickException` for invalid execution mode errors. Already a project dependency.
4. **AggregatedPhaseReport** — Existing internal class in sprint executor for generating result file markdown. Must be compatible with preflight outputs.
5. **_determine_phase_status()** — Existing internal function that parses result files. Preflight result files must conform to its expectations.
6. **parse_tasklist() / discover_phases()** — Existing internal parsers in `config.py` that are extended (not replaced) by this feature.

## Success Criteria

1. **SC-001:** Phase 1 of a sprint with `execution_mode: python` completes in < 30 seconds with zero Claude API token consumption (vs. 857s timeout previously).
2. **SC-002:** Nested `claude --print -p "hello"` command executes successfully via `subprocess.run()` without deadlock.
3. **SC-003:** `_determine_phase_status()` parses preflight-generated result files without modification, returning correct pass/fail status.
4. **SC-004:** All 14 unit tests in the test plan pass (models, config parsing, classifiers).
5. **SC-005:** All 8 integration tests in the test plan pass (preflight execution, result compatibility, timeout, combined results).
6. **SC-006:** `execution_mode: skip` phases produce `PhaseStatus.SKIPPED` with no subprocess launched.
7. **SC-007:** Removing the single `execute_preflight_phases()` call from `execute_sprint()` reverts to full all-Claude behavior with no other code changes.
8. **SC-008:** Evidence artifacts written for each preflight task contain command, exit code, stdout, stderr, duration, and classification label.

## Open Questions

1. **OQ-001 (GAP-01, Low):** How should multi-line commands in `**Command:**` fields be handled? Spec notes `\` continuation as a possibility but defers. Needs clarification if any known tasks use multi-line commands.

2. **OQ-002 (GAP-02, Low):** How should `--dry-run` flag interact with preflight phases? Spec suggests listing python-mode phases with `[preflight]` annotation in `_print_dry_run()` but does not formalize this as a requirement.

3. **OQ-003 (GAP-03, Low):** What happens when a classifier function itself raises an exception (not a classification result)? Spec suggests catching, logging, and treating as `TaskStatus.FAIL`, but this is not a formal FR acceptance criterion.

4. **OQ-004:** Should preflight execution respect the `--phases` CLI filter (e.g., `superclaude sprint run --phases 2,3` skipping preflight Phase 1)? The spec does not address selective phase execution interaction.

5. **OQ-005:** Is there a maximum number of python-mode phases expected per sprint, or any ordering constraint (e.g., must python phases precede claude phases)?
