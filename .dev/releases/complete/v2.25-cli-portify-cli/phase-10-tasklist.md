# Phase 10 -- CLI Integration

Expose the cli-portify feature through the main CLI entry point; ensure generated module structure complies with the mandated dependency order.

---

### T10.01 -- Implement Click Command Group with All Options in commands.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-062 |
| Why | The Click command group is the user-facing interface; all 7 options must be wired correctly before registration in main.py |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0058 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0058/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/commands.py` Click group `cli_portify_group` with `run` subcommand and all options: `--name`, `--output`, `--max-turns` (default 200), `--model`, `--dry-run`, `--resume`, `--debug` (FR-049)

**Steps:**
1. **[PLANNING]** Review roadmap FR-049: Click group with run subcommand and 7 options
2. **[EXECUTION]** Create `commands.py` with `cli_portify_group = click.Group("cli-portify")`
3. **[EXECUTION]** Implement `@cli_portify_group.command("run")` with all 7 options
4. **[EXECUTION]** `--max-turns` default 200; `--dry-run` is a flag (bool); `--resume` takes a step-id string; `--debug` is a flag
5. **[EXECUTION]** Command body calls `run_portify(config)` from `executor.py`
6. **[EXECUTION]** Handle `PortifyValidationError` → print error message + exit 1; handle `KeyboardInterrupt` → emit return contract + exit 0
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "commands or cli_group" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0058/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "cli_group"` exits 0
- `cli_portify_group` is a `click.Group` instance
- `run` subcommand has all 7 options with correct types and defaults
- `--max-turns` defaults to 200 without explicit flag
- `PortifyValidationError` displays user-friendly message and exits 1

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "commands" -v` passes; option defaults verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0058/spec.md` produced

**Dependencies:** T03.04 (executor run_portify), T09.03 (DiagnosticsCollector for error handling)
**Rollback:** Remove `commands.py`; CLI interface unavailable but library intact

---

### T10.02 -- Implement --dry-run Phase Type Filter

| Field | Value |
|---|---|
| Roadmap Item IDs | R-063 |
| Why | --dry-run must restrict execution to exactly 4 phase types (PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION); any SYNTHESIS, REVIEW, or VERIFICATION step running in dry-run mode wastes tokens and produces unexpected artifacts |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0059 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0059/spec.md`

**Deliverables:**
- `executor.py` `--dry-run` filter: step execution skips all steps whose `phase_type` is NOT in `{PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION}`; no SYNTHESIS/REVIEW/OBSERVABILITY/INTEGRATION/VERIFICATION steps execute (FR-037, SC-012)

**Steps:**
1. **[PLANNING]** Review roadmap FR-037/SC-012: dry-run filter to exactly 4 phase types
2. **[EXECUTION]** Implement `_is_dry_run_eligible(step: PortifyStep) -> bool`: return `step.phase_type in {PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION}`
3. **[EXECUTION]** In `run_pipeline()` dry-run path: skip step if `not _is_dry_run_eligible(step)`; log skipped step to execution log
4. **[EXECUTION]** Update T03.05 dry-run test to use `_is_dry_run_eligible()` function directly
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "dry_run_filter or sc012" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0059/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "dry_run_filter"` exits 0 (SC-012)
- Steps with phase_type SYNTHESIS, REVIEW, OBSERVABILITY, INTEGRATION, VERIFICATION → skipped in dry-run
- Steps with phase_type PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION → executed in dry-run
- Skipped steps logged to execution log with `skipped_dry_run` event

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "sc012" -v` — 4 eligible types and 5 ineligible types tested
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0059/spec.md` produced

**Dependencies:** T03.01 (PortifyPhaseType enum), T03.04 (run_pipeline dry-run path)
**Rollback:** Remove `_is_dry_run_eligible()` check; all steps run regardless of phase type

---

### T10.03 -- Register cli_portify_group in src/superclaude/cli/main.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-064 |
| Why | Without registration in main.py, `superclaude cli-portify run` is not invokable from the CLI; this is the single integration touchpoint with the existing application |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 88% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0060 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0060/evidence.md`

**Deliverables:**
- `src/superclaude/cli/main.py` updated with `from superclaude.cli.cli_portify.commands import cli_portify_group` and `main.add_command(cli_portify_group)` (FR-048, AC-005, Milestone M9)

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/main.py` to confirm no existing cli_portify registration and to match existing registration pattern
2. **[EXECUTION]** Add import: `from superclaude.cli.cli_portify.commands import cli_portify_group`
3. **[EXECUTION]** Add registration: `main.add_command(cli_portify_group)` following existing pattern
4. **[EXECUTION]** Ensure import is placed with other CLI subpackage imports (not at top of file unless convention)
5. **[VERIFICATION]** Run `uv run python -c "from superclaude.cli.main import main; assert any(c.name == 'cli-portify' for c in main.commands.values())"` exits 0
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0060/evidence.md`

**Acceptance Criteria:**
- `uv run python -c "from superclaude.cli.main import main; assert 'cli-portify' in main.commands"` exits 0 (Milestone M9)
- `superclaude cli-portify --help` shows `run` subcommand
- No other command group registration is broken by the addition
- Import follows existing `main.py` pattern

**Validation:**
- Manual check: `uv run python -c "..."` command above exits 0; `superclaude cli-portify --help` displays correctly
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0060/evidence.md` produced

**Dependencies:** T10.01 (commands.py with cli_portify_group)
**Rollback:** Remove import and `main.add_command()` line from `main.py`; revert to prior state

---

### T10.04 -- Implement Prompt Splitting (>300 Lines → portify-prompts.md)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-065 |
| Why | Aggregate prompts exceeding 300 lines hit embedding size limits; splitting to portify-prompts.md keeps the main flow readable while preserving full prompt content |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0061 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0061/spec.md`

**Deliverables:**
- `prompts.py` `maybe_split_prompt(prompt: str, workdir: Path) -> str`: if `len(prompt.splitlines()) > 300`, write full prompt to `workdir/portify-prompts.md` and return summary reference; else return prompt unchanged (FR-050, AC-010)

**Steps:**
1. **[PLANNING]** Review roadmap FR-050/AC-010: >300 lines → split to portify-prompts.md
2. **[EXECUTION]** Implement `maybe_split_prompt(prompt: str, workdir: Path) -> str` in `prompts.py`
3. **[EXECUTION]** Count lines: `len(prompt.splitlines())`
4. **[EXECUTION]** If >300: write to `workdir/portify-prompts.md`; return abbreviated reference string indicating prompt written to file
5. **[EXECUTION]** If ≤300: return prompt unchanged
6. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "prompt_split or portify_prompts" -v`
7. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0061/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "prompt_split"` exits 0
- 301-line prompt → `portify-prompts.md` written to workdir; reference string returned
- 300-line prompt → original prompt returned unchanged; no file written
- `portify-prompts.md` contains full original prompt content

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "portify_prompts" -v` passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0061/spec.md` produced

**Dependencies:** T01.05 (prompt split location confirmed as prompts.py)
**Rollback:** Remove `maybe_split_prompt()` call; prompts passed directly without splitting

---

### T10.05 -- Verify Module Generation Order (NFR-006)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-066 |
| Why | The mandated generation order prevents circular imports in the generated CLI; a test that asserts the order catches any future reordering before it causes import errors |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution 30s |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0062 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0062/evidence.md`

**Deliverables:**
- `tests/cli_portify/` test asserting STEP_REGISTRY order matches NFR-006: models→gates→prompts→config→inventory→monitor→process→executor→tui→logging_→diagnostics→commands→__init__ (NFR-006, AC-012)

**Steps:**
1. **[PLANNING]** Review roadmap NFR-006/AC-012: exact module generation order
2. **[EXECUTION]** Implement `test_step_registry_nfr006_order()` asserting STEP_REGISTRY step names match NFR-006 sequence
3. **[EXECUTION]** Use index comparison: for each consecutive pair (step_i, step_{i+1}), assert step_i appears before step_{i+1} in NFR-006 order
4. **[EXECUTION]** Test is self-documenting: comment lists full NFR-006 order for reference
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "nfr006 or module_order" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0062/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "nfr006"` exits 0
- STEP_REGISTRY contains all 13 module steps
- Order assertion correctly catches any reordering (test is resistant to false passes)
- NFR-006 full order documented in test docstring

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "module_order" -v` passes; swapping two entries causes test to fail
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0062/evidence.md` produced

**Dependencies:** T03.03 (STEP_REGISTRY), T10.01 (commands.py step added)
**Rollback:** Remove test; no production code affected

---

### Checkpoint: End of Phase 10

**Purpose:** Verify `superclaude cli-portify run` is invokable, all CLI options are wired, and module generation order is enforced before final verification phase.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P10-END.md`

**Verification:**
- `uv run python -c "from superclaude.cli.main import main; assert 'cli-portify' in main.commands"` exits 0 (Milestone M9)
- `uv run pytest tests/cli_portify/ -k "cli_group or dry_run_filter or prompt_split or nfr006" -v` exits 0
- `--dry-run` filter verified: SYNTHESIS and REVIEW steps skipped (SC-012)

**Exit Criteria:**
- All 5 Phase 10 tasks complete with D-0058 through D-0062 artifacts
- Milestone M9: `superclaude cli-portify run` is invokable and wired into application
- SC-012 (dry-run phase type filter) verified
