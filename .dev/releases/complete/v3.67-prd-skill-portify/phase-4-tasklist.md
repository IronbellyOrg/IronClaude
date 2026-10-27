# Phase 4 -- CLI Integration

**Goal**: Wire the PRD pipeline executor into the SuperClaude CLI as `superclaude prd run` and `superclaude prd resume` subcommands. Register with the main CLI entry point.

**Files**: `commands.py`, `__init__.py`, modified `main.py`

**Dependencies**: Phase 3 (executor, config), Click framework

---

## T04.01: Implement commands.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: Preferred: Context7
**Sub-Agent Delegation**: None

**Deliverable**: D-0021 u2014 `src/superclaude/cli/prd/commands.py`
**Roadmap Items**: R-028, R-052

**Steps**:
1. **[PLANNING]** Review sprint module's commands.py for Click CLI group pattern
2. **[PLANNING]** Review Section 5.1 (CLI Surface) for all options and flags
3. **[EXECUTION]** Implement `prd_group` Click group with help text
4. **[EXECUTION]** Implement `prd run` command with options: REQUEST (positional), --product/-p, --where/-w (multiple), --output/-o, --tier (choice: lightweight/standard/heavyweight), --max-turns, --model, --dry-run, --debug
5. **[EXECUTION]** Implement `prd resume` command with STEP_ID (positional) + --max-turns, --model, --debug
6. **[EXECUTION]** Wire options to `resolve_config()` then `PrdExecutor.run()` or `.resume()`
7. **[VERIFICATION]** Verify `superclaude prd --help` shows both subcommands with correct options
8. **[COMPLETION]** Record CLI surface in evidence

**Acceptance Criteria**:
- [ ] Click group `prd` with two subcommands: `run` and `resume`
- [ ] All Section 5.1 options correctly mapped to Click parameters with defaults
- [ ] `--tier` validates against choice set (lightweight, standard, heavyweight)
- [ ] `--dry-run` flag propagated to config for validation-only mode

**Validation**:
- `uv run python -c "from superclaude.cli.prd.commands import prd_group; print(prd_group.name)"`
- Evidence: prd_group is a Click Group with 2 commands

**Risk Drivers**: None

---

## T04.02: Implement __init__.py

**Effort**: XS | **Risk**: Low | **Tier**: LIGHT | **Confidence**: [####------] 40%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Quick sanity check | Token Budget: ~100 | Timeout: 10s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0022 u2014 `src/superclaude/cli/prd/__init__.py`
**Roadmap Items**: R-029

**Steps**:
1. **[PLANNING]** Review existing `__init__.py` files in `src/superclaude/cli/` for export conventions
2. **[EXECUTION]** Create `__init__.py` with package-level exports: `prd_group` from commands, `PrdConfig` from models, `PrdExecutor` from executor
3. **[EXECUTION]** Add `__all__` list for explicit public API
4. **[VERIFICATION]** Verify `from superclaude.cli.prd import prd_group` works
5. **[COMPLETION]** Record exports in evidence

**Acceptance Criteria**:
- [ ] Package is importable: `import superclaude.cli.prd`
- [ ] Public API exports: prd_group, PrdConfig, PrdExecutor
- [ ] `__all__` list defined
- [ ] No import side effects on package load

**Validation**:
- `uv run python -c "from superclaude.cli.prd import prd_group, PrdConfig"`
- Evidence: 3 exports importable without error

**Risk Drivers**: None

---

## T04.03: Register PRD subcommand in main.py

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Critical Path Override**: No
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0023 u2014 Modified `src/superclaude/cli/main.py`
**Roadmap Items**: R-030

**Steps**:
1. **[PLANNING]** Read `src/superclaude/cli/main.py` to identify where other subcommands are registered
2. **[PLANNING]** Identify the Click app object and registration pattern
3. **[EXECUTION]** Add import: `from superclaude.cli.prd.commands import prd_group`
4. **[EXECUTION]** Add registration: `app.add_command(prd_group)` following existing pattern
5. **[VERIFICATION]** Verify `superclaude --help` lists `prd` as a subcommand
6. **[VERIFICATION]** Verify `superclaude prd --help` displays the prd group help
7. **[COMPLETION]** Record diff in evidence

**Acceptance Criteria**:
- [ ] `superclaude prd` is registered as a CLI subcommand
- [ ] `superclaude --help` lists `prd` alongside existing commands (sprint, roadmap, etc.)
- [ ] Import follows existing convention (lazy or eager import matching other modules)
- [ ] No other changes to main.py beyond the import and registration lines

**Validation**:
- `uv run superclaude --help | grep prd`
- Evidence: `prd` appears in superclaude --help output

**Risk Drivers**: None

---

## T04.04: CLI integration smoke test

**Effort**: XS | **Risk**: Low | **Tier**: STANDARD | **Confidence**: [####------] 35%
**Requires Confirmation**: Yes (covered by T01.01)
**Verification Method**: Direct test execution | Token Budget: 300-500 | Timeout: 30s
**MCP Tools**: None required
**Sub-Agent Delegation**: None

**Deliverable**: D-0024 u2014 CLI dry-run integration test
**Roadmap Items**: R-050 (partial)

**Steps**:
1. **[PLANNING]** Review test_prd_pipeline_dry_run from integration test plan
2. **[EXECUTION]** Implement CLI-level smoke test: invoke `superclaude prd run "test" --dry-run` via Click test runner
3. **[EXECUTION]** Verify exit code 0 for valid inputs with --dry-run
4. **[EXECUTION]** Verify exit code non-zero for invalid tier value
5. **[VERIFICATION]** Run the smoke test and confirm expected behavior
6. **[COMPLETION]** Record test result in evidence

**Acceptance Criteria**:
- [ ] `superclaude prd run "test" --dry-run` exits with code 0
- [ ] `superclaude prd run "test" --tier invalid` exits with non-zero code
- [ ] Dry-run mode validates config without launching any subprocesses
- [ ] Test uses Click CliRunner for isolated CLI testing

**Validation**:
- `uv run pytest tests/cli/prd/test_cli_smoke.py -v --tb=short`
- Evidence: CLI smoke test passes

**Risk Drivers**: None

---

### Checkpoint: End of Phase 4

**Purpose**: Verify the PRD CLI subcommand is fully registered and functional in dry-run mode.

**Verification**:
- [ ] `superclaude prd --help` displays help text with `run` and `resume` subcommands
- [ ] `superclaude prd run "test" --dry-run` exits cleanly
- [ ] CLI smoke test passes

**Exit Criteria**:
- [ ] PRD subcommand registered in main CLI entry point
- [ ] Dry-run validates config without subprocess launches
- [ ] 39/39 cumulative tests passing (Phase 1-3: 38 + Phase 4: 1)
