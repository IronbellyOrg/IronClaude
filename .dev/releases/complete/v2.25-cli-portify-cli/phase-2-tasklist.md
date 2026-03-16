# Phase 2 -- Prerequisites and Config Foundation

Implement the deterministic setup layer so the pipeline fails early and safely. All path resolution, name derivation, collision detection, component discovery, and workdir creation must complete before any Claude subprocess is invoked.

---

### T02.01 -- Implement Workflow Path Resolution in config.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | The pipeline cannot start without a valid, unambiguous workflow path; failing early here prevents wasted Claude invocations on bad inputs |
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
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0008/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/config.py` updated with `resolve_workflow_path()` implementing AMBIGUOUS_PATH and INVALID_PATH error codes

**Steps:**
1. **[PLANNING]** Load context from `src/superclaude/cli/cli_portify/config.py` (existing Phase 1–2 implementation)
2. **[PLANNING]** Review roadmap FR-001–FR-003: search `src/superclaude/skills/` for workflow, require `SKILL.md`, raise `AMBIGUOUS_PATH` if multiple matches, `INVALID_PATH` if none
3. **[EXECUTION]** Implement `resolve_workflow_path(workflow: str, skills_root: Path) -> Path` in `config.py`
4. **[EXECUTION]** Raise `PortifyValidationError(failure_type=AMBIGUOUS_PATH, candidates=[...])` when multiple matches found
5. **[EXECUTION]** Raise `PortifyValidationError(failure_type=INVALID_PATH)` when no match found or `SKILL.md` absent
6. **[EXECUTION]** Support both exact path and name-only lookup
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "path_resolution or ambiguous or invalid_path" -v`
8. **[COMPLETION]** Document implementation in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0008/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "path_resolution"` exits 0 with tests passing
- `resolve_workflow_path()` raises `AMBIGUOUS_PATH` with candidate list when multiple skills match
- `resolve_workflow_path()` raises `INVALID_PATH` when workflow name not found or `SKILL.md` absent
- Exact path input bypasses search and validates directly

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "path" -v` — confirm AMBIGUOUS_PATH and INVALID_PATH test cases pass
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0008/spec.md` produced

**Dependencies:** T01.03 (OQ-009 failure_type enum defined)
**Rollback:** Revert `config.py` changes; path resolution returns to prior state

---

### T02.02 -- Implement CLI Name Derivation in config.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | Deterministic name derivation from workflow path ensures the generated CLI module has a predictable, well-formed name |
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
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0009/spec.md`

**Deliverables:**
- `config.py` `derive_cli_name()` function: strips `sc-` prefix and `-protocol` suffix, normalizes to kebab-case, supports explicit `--name` override

**Steps:**
1. **[PLANNING]** Review roadmap FR-004–FR-006: strip `sc-` prefix, strip `-protocol` suffix, normalize to kebab-case, explicit `--name` takes precedence
2. **[EXECUTION]** Implement `derive_cli_name(workflow_name: str, explicit_name: str | None = None) -> str` in `config.py`
3. **[EXECUTION]** Apply transformations in order: explicit_name → return as-is; else strip prefixes/suffixes → normalize to kebab-case
4. **[EXECUTION]** Raise `PortifyValidationError(failure_type=DERIVATION_FAILED)` if result is empty after normalization
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "cli_name or derivation" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0009/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "cli_name"` exits 0 with tests passing
- `derive_cli_name("sc-roadmap-protocol")` returns `"roadmap"`
- `derive_cli_name("sc-roadmap-protocol", explicit_name="my-tool")` returns `"my-tool"`
- Empty result after normalization raises `DERIVATION_FAILED`
- `derive_cli_name("sc-my-workflow-protocol")` returns `"my-workflow"` (general kebab-case normalization confirmed beyond prefix/suffix stripping)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "cli_name" -v` shows specific transformation cases passing
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0009/spec.md` produced

**Dependencies:** T01.03 (OQ-009 failure_type enum)
**Rollback:** Revert `config.py` changes

---

### T02.03 -- Implement Collision Detection in config.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | Overwriting a hand-written CLI module would cause irreversible data loss; collision detection must run before any file writes |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0010/spec.md`

**Deliverables:**
- `config.py` `check_collision()` function: scans `src/superclaude/cli/<module_name>/__init__.py` first 10 lines for `Generated by` / `Portified from` marker; raises `NAME_COLLISION` if module exists without marker

**Steps:**
1. **[PLANNING]** Load T01.06 output (D-0006) for exact marker strings and overwrite rule
2. **[PLANNING]** Review roadmap FR-007–FR-008: scan `src/superclaude/cli/`, allow overwrite only for portified modules
3. **[EXECUTION]** Implement `check_collision(output_dir: Path, cli_name: str) -> None` in `config.py`
4. **[EXECUTION]** Target path: `output_dir / cli_name / "__init__.py"`
5. **[EXECUTION]** If path exists: read first 10 lines; if `# Generated by superclaude cli-portify` or `# Portified from` present → allow overwrite; else raise `PortifyValidationError(failure_type=NAME_COLLISION, path=str(target))`
6. **[EXECUTION]** If path does not exist → no collision, proceed
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "collision" -v` — verify both collision and non-collision paths
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0010/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "collision"` exits 0 with all collision test paths passing
- Module with no marker → `NAME_COLLISION` raised before any file is written
- Module with `# Generated by superclaude cli-portify` marker → overwrite allowed, no exception
- Non-existent module → no collision, proceeds normally

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "collision" -v` — confirm NAME_COLLISION test case passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0010/spec.md` produced

**Dependencies:** T01.06 (D-0006 marker strings), T02.02 (cli_name available)
**Rollback:** Revert `config.py` changes; no file writes occur before this check so rollback is safe

---

### T02.04 -- Implement Output Destination Validation in config.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | Writing to a non-writable destination fails silently mid-pipeline; early validation surfaces this as a clean error before any subprocess is invoked |
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
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0011/spec.md`

**Deliverables:**
- `config.py` `validate_output_destination()` function: confirms parent directory exists and is writable; raises `OUTPUT_NOT_WRITABLE`

**Steps:**
1. **[PLANNING]** Review roadmap FR-009: validate output destination before any work begins
2. **[EXECUTION]** Implement `validate_output_destination(output_dir: Path) -> None` in `config.py`
3. **[EXECUTION]** Check `output_dir.parent.exists()` and `os.access(output_dir.parent, os.W_OK)`; raise `PortifyValidationError(failure_type=OUTPUT_NOT_WRITABLE)` if either fails
4. **[EXECUTION]** If `output_dir` itself exists, also check it is writable
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "output_destination or not_writable" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0011/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "output_destination"` exits 0
- Non-existent parent directory raises `OUTPUT_NOT_WRITABLE`
- Non-writable parent directory raises `OUTPUT_NOT_WRITABLE`
- Valid writable destination passes without exception

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "not_writable" -v` passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0011/spec.md` produced

**Dependencies:** T01.03 (OQ-009 failure_type enum)
**Rollback:** Revert `config.py` changes

---

### T02.05 -- Implement Workdir Creation in workdir.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | All pipeline artifacts are written to the workdir; creating it atomically before any Claude step ensures no partial artifact writes to undefined locations |
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
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0012/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/workdir.py` `create_workdir()` function creating `.dev/portify-workdir/<cli_name>/`

**Steps:**
1. **[PLANNING]** Review roadmap FR-010: create workdir at `.dev/portify-workdir/<cli_name>/`
2. **[EXECUTION]** Implement `create_workdir(cli_name: str, project_root: Path) -> Path` in `workdir.py`
3. **[EXECUTION]** Use `Path(project_root / ".dev" / "portify-workdir" / cli_name)` and `workdir.mkdir(parents=True, exist_ok=True)`
4. **[EXECUTION]** Return the created workdir path
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "workdir" -v`
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0012/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "workdir"` exits 0
- `create_workdir("roadmap", Path("/project"))` creates `/project/.dev/portify-workdir/roadmap/`
- Calling with existing workdir is idempotent (`exist_ok=True`)
- Returned path is the created workdir

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "workdir" -v` passes
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0012/spec.md` produced

**Dependencies:** T02.02 (cli_name derived)
**Rollback:** Delete created workdir directory

---

### Checkpoint: Phase 2 / Tasks T02.01-T02.05

**Purpose:** Verify path resolution, name derivation, collision detection, output validation, and workdir creation are implemented and tested before proceeding to YAML emission and component discovery.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P02-T01-T05.md`

**Verification:**
- `uv run pytest tests/cli_portify/ -k "path_resolution or cli_name or collision or output_destination or workdir" -v` exits 0
- All 5 tasks (T02.01–T02.05) have artifacts in their respective `D-0008` through `D-0012` directories
- `NAME_COLLISION` error raised correctly for non-portified module (manual spot-check)

**Exit Criteria:**
- All path/name/collision/destination validation functions implemented and unit-tested
- Workdir creation is idempotent and verified
- Zero open blockers for T02.06 through T02.09

---

### T02.06 -- Emit portify-config.yaml with Resolved Paths

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | `portify-config.yaml` is the single source of truth for all downstream steps; emitting it at Step 0 ensures all phases use consistent resolved paths |
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
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0013/evidence.md`

**Deliverables:**
- `portify-config.yaml` emitted to workdir with resolved `workflow_path`, `cli_name`, `output_dir`, `workdir` fields (SC-001)

**Steps:**
1. **[PLANNING]** Review roadmap FR-011: emit `portify-config.yaml` after all validations pass
2. **[EXECUTION]** Implement `emit_portify_config(config: PortifyConfig, workdir: Path) -> Path` writing YAML to `workdir/portify-config.yaml`
3. **[EXECUTION]** Required G-000 fields: `workflow_path`, `cli_name`, `output_dir`; also emit `workdir` as an additional field (not G-000-required but needed by downstream steps)
4. **[EXECUTION]** Use `pyyaml` (6.0.3 confirmed present) for YAML serialization
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "portify_config" -v`; also validate G-000 gate passes on emitted file
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0013/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "portify_config"` exits 0
- Emitted `portify-config.yaml` contains G-000 required fields: `workflow_path`, `cli_name`, `output_dir`; also contains `workdir` (emitted for downstream use, not a G-000 requirement)
- G-000 gate (`has_valid_yaml_config`) passes on the emitted file (validates workflow_path, cli_name, output_dir only)
- SC-001: Step 0 completes in ≤30s

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "portify_config" -v` confirms G-000 gate pass
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0013/evidence.md` produced

**Dependencies:** T02.01, T02.02, T02.04, T02.05
**Rollback:** Delete emitted `portify-config.yaml` from workdir

---

### T02.07 -- Implement Component Discovery and Inventory in inventory.py

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | The component inventory drives all downstream analysis; missing components here cause silent gaps in the generated CLI specification |
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
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0014/spec.md`

**Deliverables:**
- `src/superclaude/cli/cli_portify/inventory.py` `discover_components()` scanning `SKILL.md`, command `.md` files from both command directories, `refs/`, `rules/`, `templates/`, `scripts/`, `decisions.yaml`

**Steps:**
1. **[PLANNING]** Review roadmap FR-012: scan `SKILL.md`, command `.md` files from both command directories, `refs/`, `rules/`, `templates/`, `scripts/`, `decisions.yaml`
2. **[PLANNING]** Note OQ-007 (agent discovery warnings): emit `warnings.warn()` for missing agent files; do not suppress
3. **[EXECUTION]** Implement `discover_components(workflow_path: Path) -> list[ComponentEntry]` in `inventory.py`
4. **[EXECUTION]** Each `ComponentEntry`: `{path: str, lines: int, purpose: str, type: str}`; type values: `skill_main`, `command`, `reference`, `rule`, `template`, `script`, `decision`
5. **[EXECUTION]** Emit `warnings.warn(f"Agent file not found: {path}")` for missing agent `.md` files (OQ-007)
6. **[EXECUTION]** Enforce 60s timeout (NFR-001) via `concurrent.futures` or signal-based timeout
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "inventory or discover_components" -v`
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0014/spec.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "inventory"` exits 0
- `discover_components()` returns at least one entry with `SKILL.md` as `skill_main` type
- Missing agent files produce `warnings.warn()` call (not suppressed, not raised as exception)
- Discovery completes within 60s timeout enforced by T02.09
- Inventory contains entries for all component types present in test skill: skill_main, command, reference, rule, template, script (type field verified per entry)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "inventory" -v` — G-001 gate passes on discovered inventory
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0014/spec.md` produced

**Dependencies:** T02.01, T01.07 (OQ-007 behavior documented)
**Rollback:** Revert `inventory.py` changes

---

### T02.08 -- Emit component-inventory.yaml to Workdir

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | `component-inventory.yaml` feeds the protocol-mapping and analysis prompts in Phase 5; emitting it now with full content prevents prompt-time gaps |
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
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0015/evidence.md`

**Deliverables:**
- `component-inventory.yaml` emitted to workdir with `{path, lines, purpose, type}` per discovered component (SC-002)

**Steps:**
1. **[PLANNING]** Review roadmap FR-013: emit `component-inventory.yaml` from discovered components
2. **[EXECUTION]** Implement `emit_component_inventory(components: list[ComponentEntry], workdir: Path) -> Path`
3. **[EXECUTION]** Serialize to YAML list; each entry: `path`, `lines`, `purpose`, `type`
4. **[EXECUTION]** Write to `workdir/component-inventory.yaml`
5. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "component_inventory" -v`; validate G-001 gate passes
6. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0015/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "component_inventory"` exits 0
- Emitted YAML contains at least one entry with `SKILL.md`
- G-001 gate (`has_component_inventory`) passes on emitted file
- SC-002: Step 1 completes in ≤60s
- Each entry in `component-inventory.yaml` contains all 4 required fields: `path`, `lines`, `purpose`, `type` (verified on ≥3 entries)

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "component_inventory" -v` confirms G-001 gate pass
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0015/evidence.md` produced

**Dependencies:** T02.07
**Rollback:** Delete emitted `component-inventory.yaml` from workdir

---

### T02.09 -- Enforce 30s and 60s Timeouts on Validation Steps

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Without hard timeouts, a blocked filesystem scan or hung subprocess can cause the pipeline to stall indefinitely before a single Claude call is made |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STRICT |
| Confidence | [█████████░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer 60s |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0016/evidence.md`

**Deliverables:**
- Timeout enforcement in `executor.py` or `config.py`: 30s for input-validation steps (SC-001), 60s for component-discovery step (SC-002); raises `PortifyValidationError(failure_type=TIMEOUT)` on breach

**Steps:**
1. **[PLANNING]** Review roadmap NFR-001: 30s for input-validation, 60s for component-discovery
2. **[PLANNING]** Determine enforcement point: wrap `validate_and_configure()` in 30s timeout; wrap `discover_components()` in 60s timeout
3. **[EXECUTION]** Implement `run_with_timeout(fn, timeout_s, *args, **kwargs)` utility using `concurrent.futures.ThreadPoolExecutor`
4. **[EXECUTION]** Wrap `validate_and_configure()` call with 30s timeout in executor Step 0
5. **[EXECUTION]** Wrap `discover_components()` call with 60s timeout in executor Step 1
6. **[EXECUTION]** On timeout: raise `PortifyValidationError(failure_type=TIMEOUT, step=step_id)`
7. **[VERIFICATION]** Run `uv run pytest tests/cli_portify/ -k "timeout" -v` — mock slow functions to verify timeout fires
8. **[COMPLETION]** Document in `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0016/evidence.md`

**Acceptance Criteria:**
- `uv run pytest tests/cli_portify/ -k "timeout"` exits 0 with timeout test cases passing
- Input-validation step with mocked 31s execution raises `TIMEOUT` exception
- Component-discovery step with mocked 61s execution raises `TIMEOUT` exception
- SC-001 (≤30s) and SC-002 (≤60s) timing constraints enforced

**Validation:**
- Manual check: `uv run pytest tests/cli_portify/ -k "timeout" -v` — both timeout boundaries verified
- Evidence: `.dev/releases/current/v2.25-cli-portify-cli/artifacts/D-0016/evidence.md` produced

**Dependencies:** T02.05, T02.07
**Rollback:** Remove timeout wrappers; validation steps revert to unbounded execution

---

### Checkpoint: End of Phase 2

**Purpose:** Verify the complete deterministic setup layer is implemented, tested, and produces valid `portify-config.yaml` and `component-inventory.yaml` before any executor or model work begins.
**Checkpoint Report Path:** `.dev/releases/current/v2.25-cli-portify-cli/checkpoints/CP-P02-END.md`

**Verification:**
- `uv run pytest tests/cli_portify/ -k "path_resolution or cli_name or collision or output_destination or workdir or portify_config or component_inventory or timeout" -v` exits 0
- SC-001 (Step 0 ≤30s, valid config YAML) and SC-002 (Step 1 ≤60s, inventory ≥1 component) validated
- G-000 and G-001 gates pass on emitted YAML files

**Exit Criteria:**
- All 9 Phase 2 tasks completed with artifacts in D-0008 through D-0016
- `portify-config.yaml` and `component-inventory.yaml` emit correctly on valid input
- `NAME_COLLISION`, `INVALID_PATH`, `AMBIGUOUS_PATH`, `OUTPUT_NOT_WRITABLE`, `TIMEOUT` errors all raise correctly on invalid input
