# Phase 1 -- Foundation Config Schema DSL Security

**Phase Goal:** Establish the security-critical loader pipeline (eval_id regex guard, manifest schema validation, allowed scratch roots), the configuration data model, and the ExpectDSL public interface before any code path that writes to disk. `superclaude eval doctor` outline runs, schema validates v1 manifests, and the DSL interface is importable.

### T01.01 -- Implement EvalConfig dataclass with allowed_scratch_roots

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | Roadmap COMP-005 requires a frozen dataclass holding paths, defaults, and allowed_scratch_roots so other components can resolve config without duplicating defaults. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0001/spec.md`
- `TASKLIST_ROOT/artifacts/D-0001/notes.md`
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Deliverables:**
- Frozen `EvalConfig` dataclass module with fields `paths`, `defaults`, `allowed_scratch_roots` defaulting to `/tmp/eval-runs` and repo `.dev/eval-runs`.

**Steps:**
1. **[PLANNING]** Load context and identify scope from roadmap COMP-005 entry.
2. **[PLANNING]** Check dependencies and blockers (no upstream deps for this task).
3. **[PLANNING]** Confirm OQ-8 resolution status (DOC-OQ8 T06.03) or record deferral in `TASKLIST_ROOT/artifacts/D-0001/spec.md`.
4. **[EXECUTION]** Add `EvalConfig` frozen dataclass module under `src/superclaude/cli/eval/config.py`.
5. **[EXECUTION]** Populate `allowed_scratch_roots` default list with `/tmp/eval-runs` and `.dev/eval-runs`.
6. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_config.py -v` and confirm fields present and frozen.
7. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.01/` and update execution log.

**Acceptance Criteria:**
- Module `src/superclaude/cli/eval/config.py` exists and exports a frozen `EvalConfig` dataclass with fields `paths`, `defaults`, `allowed_scratch_roots`.
- `EvalConfig` instances reject mutation (frozen dataclass) and the default `allowed_scratch_roots` contains `/tmp/eval-runs` and `.dev/eval-runs`.
- Construction with the same inputs produces equal instances (deterministic equality).
- `TASKLIST_ROOT/artifacts/D-0001/spec.md` records the field schema and default list.

**Validation:**
- Manual check: confirm frozen dataclass behavior with attempted mutation.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Default scratch roots align with AC12 allowlist landing in T01.19. OQ-8 (`CLAUDE_FAKE_TIME_OFFSET` consumption) must resolve before COMP-005 close or be deferred via T06.03 decision.

### T01.02 -- Define suite.schema.json YAML manifest schema

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | DM-011 requires a JSON schema covering suite name, version, description, defaults, required_binaries, optional_capabilities, and evals[] entries with parameterize. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0002/notes.md`
- `TASKLIST_ROOT/artifacts/D-0002/evidence.md`

**Deliverables:**
- `suite.schema.json` file under `src/superclaude/cli/eval/suites/` defining manifest fields and `parameterize` acceptance.

**Steps:**
1. **[PLANNING]** Load context: read DM-011 roadmap entry and dependent COMP-005 fields.
2. **[PLANNING]** Confirm EvalConfig (T01.01) deliverable is available.
3. **[EXECUTION]** Author `suites/suite.schema.json` declaring required fields and rejecting unknown required keys.
4. **[EXECUTION]** Accept `parameterize` block under evals[] with template token validation.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_schema_load.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.02/`.

**Acceptance Criteria:**
- File `src/superclaude/cli/eval/suites/suite.schema.json` exists and is jsonschema-valid against a documented JSON Schema dialect (decision recorded in `TASKLIST_ROOT/artifacts/D-0002/spec.md`).
- Schema declares required fields `name,version,description,defaults,required_binaries,optional_capabilities,evals` and forbids unknown required keys.
- A reference fixture manifest validates green; a fixture with a missing required field is rejected by jsonschema.
- `TASKLIST_ROOT/artifacts/D-0002/spec.md` documents schema field rules and `parameterize` shape.

**Validation:**
- Manual check: load schema via `python -c "import json; json.load(open(...))"` and run jsonschema validator on fixture manifests.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Schema version field supports forward evolution per M1 Risk-3.

### T01.03 -- Add EvalSpec parsed-manifest data model

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | DM-002 requires a parsed manifest entry model carrying id, title, category, requires, timeout_sec, isolation, inputs, expects, parameterize. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0003/spec.md`
- `TASKLIST_ROOT/artifacts/D-0003/notes.md`
- `TASKLIST_ROOT/artifacts/D-0003/evidence.md`

**Deliverables:**
- `EvalSpec` dataclass module under `src/superclaude/cli/eval/models.py` matching DM-011 schema shape.

**Steps:**
1. **[PLANNING]** Confirm schema fields from T01.02 are stable.
2. **[PLANNING]** Inventory existing model patterns in `src/superclaude/cli/pipeline/models.py` for consistency.
3. **[EXECUTION]** Add `EvalSpec` dataclass with the 9 fields named in DM-002.
4. **[EXECUTION]** Implement `from_dict()` factory aligned with `suite.schema.json` field names.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_models.py::test_evalspec -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.03/`.

**Acceptance Criteria:**
- Class `EvalSpec` is importable from `src/superclaude/cli/eval/models.py` and exposes fields `id,title,category,requires,timeout_sec,isolation,inputs,expects,parameterize`.
- `EvalSpec.from_dict()` accepts a schema-valid mapping and returns an instance whose fields match the input.
- Two `EvalSpec` instances built from the same dict compare equal.
- `TASKLIST_ROOT/artifacts/D-0003/spec.md` documents the 9-field contract.

**Validation:**
- Manual check: build an `EvalSpec` from a fixture manifest entry and assert field equality.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.02
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Field names match schema for round-trip determinism.

### T01.04 -- Wire FR-SCH1 manifest schema validation entry point

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | FR-SCH1 requires manifest validation via jsonschema both inside `eval doctor` and at the top of `eval run` so schema violations exit 2 before any FS write. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0004/spec.md`
- `TASKLIST_ROOT/artifacts/D-0004/notes.md`
- `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Deliverables:**
- Validator function `validate_manifest(path)` returning `EvalSpec` list or raising a typed `SchemaError` mapped to exit code 2.

**Steps:**
1. **[PLANNING]** Confirm `suite.schema.json` (T01.02) and `EvalSpec` (T01.03) are stable.
2. **[PLANNING]** Identify exit-code mapping for `SchemaError` (exit 2 per FR-SCH1).
3. **[EXECUTION]** Implement `validate_manifest(path)` in `src/superclaude/cli/eval/loader.py` calling jsonschema.
4. **[EXECUTION]** On violation, raise `SchemaError` with field-path message and surface exit-2 mapping.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_schema_validate.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.04/`.

**Acceptance Criteria:**
- Function `validate_manifest(path)` in `src/superclaude/cli/eval/loader.py` raises `SchemaError` for a fixture manifest missing a required field; the error message names the offending JSON path.
- Valid fixture manifest returns a list of `EvalSpec` instances matching the schema's `evals[]` length.
- No filesystem writes occur before validation succeeds (verified by a pytest fixture that snapshots `/tmp/eval-runs` before and after a rejection).
- `TASKLIST_ROOT/artifacts/D-0004/spec.md` records error->exit-code mapping.

**Validation:**
- Manual check: run `superclaude eval doctor --suite <fixture>` and confirm exit 2 on invalid manifest.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.02, T01.03
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Validation runs before any path resolution to guarantee no FS write on bad manifest.

### T01.05 -- Implement FR-SCH2 Eval ID regex guard (security-critical)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | FR-SCH2 is security-critical: every eval id (including parameterize-expanded IDs) must match `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` before any FS write to prevent path traversal. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, scope (eval id is system-wide gate) |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0005/spec.md`
- `TASKLIST_ROOT/artifacts/D-0005/notes.md`
- `TASKLIST_ROOT/artifacts/D-0005/evidence.md`

**Deliverables:**
- `validate_eval_id(eval_id: str)` function raising `InvalidEvalId` (exit code 2) for any malformed or traversal-pattern id, applied pre-FS-write and post-parameterize-expansion.

**Steps:**
1. **[PLANNING]** Load FR-SCH2 specification and identify caller sites (SuiteLoader, HomeIsolation).
2. **[PLANNING]** Enumerate negative cases from NFR-SEC1 (T01.08) checklist.
3. **[EXECUTION]** Implement `validate_eval_id` in `src/superclaude/cli/eval/loader.py` with compiled regex.
4. **[EXECUTION]** Apply guard at the top of `SuiteLoader` and again after parameterize expansion.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_eval_id_regex.py -v` covering traversal cases.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.05/` and record sub-agent verification.

**Acceptance Criteria:**
- Function `validate_eval_id()` in `src/superclaude/cli/eval/loader.py` raises `InvalidEvalId` for inputs `../home`, `/etc`, `..`, empty string, leading-digit IDs, and template tokens inside id.
- Guard is applied at SuiteLoader entry AND after parameterize expansion (verified by integration test that simulates expansion producing an unsafe id).
- `InvalidEvalId` propagates to process exit code 2 via the loader error mapping.
- `TASKLIST_ROOT/artifacts/D-0005/spec.md` documents the regex and all negative cases.

**Validation:**
- Manual check: invoke `validate_eval_id("../home")` and confirm `InvalidEvalId` raised before any FS access.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.04
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Critical-path override applied per Section 4.11 (security keyword in roadmap text + pre-FS-write guard).

### T01.06 -- Checkpoint: Phase 1 / Tasks T01.01-T01.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001,R-002,R-003,R-004,R-005 |
| Why | Gate: verify EvalConfig, schema, EvalSpec, schema validation, and eval_id guard are landed before SuiteLoader builds on them. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md`

**Purpose:** Verify foundational config, schema, model, validator, and eval_id guard before SuiteLoader composes them.

**Verification:**
- `src/superclaude/cli/eval/config.py` exports a frozen `EvalConfig` with `allowed_scratch_roots` populated.
- `src/superclaude/cli/eval/suites/suite.schema.json` validates the v1 reference manifest.
- `validate_eval_id` rejects all traversal patterns; jsonschema rejects the invalid-field fixture; both raise exit-2 mapped errors.

**Exit Criteria:**
- All five upstream tests (T01.01..T01.05) pass on `uv run pytest`.
- No filesystem writes occur in any rejection path covered above.
- Checkpoint report `CP-P01-T01-T05.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T01.01-T01.05).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01..T01.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T01.07 -- Implement COMP-002 SuiteLoader orchestrating schema + regex + gates

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | COMP-002 SuiteLoader reads YAML manifests and orchestrates schema validation, eval_id regex, and capability gates; raises typed errors with exit 2. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | scope (security gate orchestrator) |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0006/spec.md`
- `TASKLIST_ROOT/artifacts/D-0006/notes.md`
- `TASKLIST_ROOT/artifacts/D-0006/evidence.md`

**Deliverables:**
- `SuiteLoader` class in `src/superclaude/cli/eval/loader.py` exposing `load(path)` that returns parsed suites and raises typed errors mapped to exit 2.

**Steps:**
1. **[PLANNING]** Confirm `validate_manifest` (T01.04), `validate_eval_id` (T01.05), and capability gate interface availability.
2. **[PLANNING]** Define call sequence: read YAML -> schema -> id regex -> capability resolution -> parameterize expansion -> id regex re-check.
3. **[EXECUTION]** Implement `SuiteLoader.load` chaining the gates above.
4. **[EXECUTION]** Map every typed error to exit code 2 with a stable error-class name.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_suite_loader.py -v` covering positive + negative cases.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.07/`.

**Acceptance Criteria:**
- Class `SuiteLoader` in `src/superclaude/cli/eval/loader.py` loads `suites/*.yaml`, applies schema validation, eval_id regex, capability resolution, and parameterize expansion in that order.
- Each typed error (`SchemaError`,`InvalidEvalId`,`UnresolvedCapability`) maps to process exit code 2 with the error class name in stderr.
- A reference fixture suite loads without error; a fixture with an unsafe id is rejected before any capability resolution call (verified by mock).
- `TASKLIST_ROOT/artifacts/D-0006/spec.md` documents the gate ordering and exit-code map.

**Validation:**
- Manual check: load the reference suite from the CLI and verify exit 0 on pass, exit 2 on each error class.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.04, T01.05, T01.14
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Capability gates resolved here come from T01.11 (COMP-009). COMP-010 (T01.14) dependency follows roadmap COMP-002 deps `FR-SCH2, COMP-010` so the loader can wire the DSL interface at construction time.

### T01.08 -- Author NFR-SEC1 path-traversal prevention test set

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | NFR-SEC1 requires negative-case tests proving the eval_id regex blocks traversal patterns; cross-links FR-SCH2 and TEST-001 for traceability. |
| Effort | M |
| Risk | High |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0007/spec.md`
- `TASKLIST_ROOT/artifacts/D-0007/notes.md`
- `TASKLIST_ROOT/artifacts/D-0007/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_path_traversal.py` covering `../home`, `/etc`, `..`, empty, leading-digit, template-token, and parameterized-unsafe cases; all asserting `InvalidEvalId`.

**Steps:**
1. **[PLANNING]** Enumerate all rejection cases listed in NFR-SEC1.
2. **[PLANNING]** Confirm `validate_eval_id` (T01.05) is importable for direct unit assertions.
3. **[EXECUTION]** Author `tests/cli/eval/test_path_traversal.py` with one test per negative case.
4. **[EXECUTION]** Add a parameterized expansion test that simulates an unsafe expanded id and asserts rejection.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_path_traversal.py -v` and confirm 7+ passing assertions.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.08/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_path_traversal.py` exists and contains tests for `../home`, `/etc`, `..`, empty, leading-digit, template-token, and parameterized-unsafe ids; each asserts `InvalidEvalId`.
- `uv run pytest tests/cli/eval/test_path_traversal.py -v` exits 0 with at least 7 passing tests.
- Cross-link to FR-SCH2 (T01.05) and TEST-001 (T01.23) is recorded in the test docstring header.
- `TASKLIST_ROOT/artifacts/D-0007/spec.md` documents the negative-case checklist.

**Validation:**
- Manual check: run the targeted pytest command above and confirm all assertions pass.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.05
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Sub-agent delegation Required because tier=STRICT and Risk=High (Section 5.6).

### T01.09 -- Add DM-007 Capability frozen dataclass

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | DM-007 requires a capability descriptor carrying name, check callable, failure_mode (hard/skip/xfail), skip_flag, and description as a frozen dataclass. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/notes.md`
- `TASKLIST_ROOT/artifacts/D-0008/evidence.md`

**Deliverables:**
- Frozen `Capability` dataclass in `src/superclaude/cli/eval/capabilities.py` with the 5 fields from DM-007.

**Steps:**
1. **[PLANNING]** Read DM-007 fields and confirm `failure_mode` literal set (`hard`,`skip`,`xfail`).
2. **[PLANNING]** Identify caller site (COMP-009 CapabilityGates at T01.11).
3. **[EXECUTION]** Add `Capability` dataclass with `frozen=True` and a `Literal["hard","skip","xfail"]` for `failure_mode`.
4. **[EXECUTION]** Provide `__post_init__` validating `failure_mode` membership.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_capability_dataclass.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.09/`.

**Acceptance Criteria:**
- Class `Capability` in `src/superclaude/cli/eval/capabilities.py` is a frozen dataclass exposing `name,check,failure_mode,skip_flag,description`.
- Instantiation with an invalid `failure_mode` raises `ValueError`.
- Two instances built from the same arguments compare equal.
- `TASKLIST_ROOT/artifacts/D-0008/spec.md` records the 5-field contract.

**Validation:**
- Manual check: build a Capability with `failure_mode="invalid"` and assert `ValueError`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Consumed by COMP-009 (T01.11) and CapabilityReport (T01.10).

### T01.10 -- Add DM-008 CapabilityReport aggregate dataclass

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | DM-008 requires a per-capability status and blocked-evals listing serializable to JSON for doctor output. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0009/spec.md`
- `TASKLIST_ROOT/artifacts/D-0009/notes.md`
- `TASKLIST_ROOT/artifacts/D-0009/evidence.md`

**Deliverables:**
- `CapabilityReport` dataclass in `src/superclaude/cli/eval/capabilities.py` with `report[],blocked_evals[],skip_flags[],hard_failures[],soft_skips[],soft_xfails[]` and `to_json()` method.

**Steps:**
1. **[PLANNING]** Confirm `Capability` (T01.09) is available for typing.
2. **[PLANNING]** Identify JSON output requirements for FR-CLI4 doctor (T01.13).
3. **[EXECUTION]** Add `CapabilityReport` dataclass with the 6 list fields from DM-008.
4. **[EXECUTION]** Implement `to_json()` producing a stable, deterministic JSON ordering.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_capability_report.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.10/`.

**Acceptance Criteria:**
- Class `CapabilityReport` exposes the 6 list fields named in DM-008 and a `to_json()` method.
- `to_json()` produces a JSON-serializable mapping per DM-008 "serializable to JSON" requirement.
- Empty report serializes to a stable canonical form documented in spec.md.
- `TASKLIST_ROOT/artifacts/D-0009/spec.md` records the JSON shape.

**Validation:**
- Manual check: build empty + populated reports and diff serialized JSON.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.09
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Determinism is a derived requirement for doctor snapshot tests, not in DM-008. If snapshot stability is desired by downstream, `to_json()` should sort keys.

### T01.11 -- Implement COMP-009 CapabilityGates with check_all + which_or_skip + mcp_server_reachable

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | COMP-009 implements claude/jq/make/git as HARD checks; MCP servers as SOFT-SKIP via `--no-mcp`; emits CapabilityReport for doctor and run pre-flight. |
| Effort | L |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0010/spec.md`
- `TASKLIST_ROOT/artifacts/D-0010/notes.md`
- `TASKLIST_ROOT/artifacts/D-0010/evidence.md`

**Deliverables:**
- `CapabilityGates` class with methods `check_all()`,`which_or_skip(name)`,`mcp_server_reachable(name)` producing a `CapabilityReport`.

**Steps:**
1. **[PLANNING]** Confirm `Capability` and `CapabilityReport` (T01.09, T01.10) interfaces.
2. **[PLANNING]** Inventory binary names: claude, jq, make, git (HARD) + auggie/auggie-mcp/airis-mcp-gateway (SOFT-SKIP).
3. **[EXECUTION]** Implement `which_or_skip` using `shutil.which()` with HARD failure when not found and binary marked HARD.
4. **[EXECUTION]** Implement `mcp_server_reachable` per OQ-5 resolution semantics with SOFT-SKIP fallback under `--no-mcp`.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_capability_gates.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.11/`.

**Acceptance Criteria:**
- Class `CapabilityGates` exposes `check_all()`, `which_or_skip()`, `mcp_server_reachable()` and returns a populated `CapabilityReport`.
- Missing `claude` on PATH classifies HARD; missing MCP server classifies SOFT-SKIP under `--no-mcp`.
- `check_all()` is idempotent (calling twice returns equal CapabilityReport objects).
- `TASKLIST_ROOT/artifacts/D-0010/spec.md` documents the binary roster and HARD/SOFT semantics.

**Validation:**
- Manual check: invoke `superclaude eval doctor` with PATH manipulated to exclude jq and confirm HARD classification.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.09, T01.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** OQ-5 (mcp_server_reachable semantics) must be resolved before COMP-009 close (M2 target) per roadmap Open Questions table.

### T01.12 -- Checkpoint: Phase 1 / Tasks T01.07-T01.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006,R-007,R-008,R-009,R-010 |
| Why | Gate: verify SuiteLoader and capability subsystem are landed before the eval doctor CLI consumes them. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-T07-T11.md`

**Purpose:** Confirm SuiteLoader orchestration and capability subsystem before eval doctor depends on them.

**Verification:**
- `SuiteLoader` integration test exercises the full gate chain (schema -> id regex -> capability -> expansion -> id re-check).
- `CapabilityGates.check_all()` returns a populated `CapabilityReport` with idempotent results.
- Path-traversal test set (T01.08) is green at the targeted pytest path.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_suite_loader.py tests/cli/eval/test_capability_gates.py tests/cli/eval/test_path_traversal.py -v` exits 0.
- `CapabilityReport.to_json()` produces deterministic output across two invocations.
- Checkpoint report `CP-P01-T07-T11.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P01-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T01.07-T01.11).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.07..T01.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T01.13 -- Implement FR-CLI4 `eval doctor` subcommand

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | FR-CLI4 prints a green checklist verifying claude PATH+min_version 0.5.0, jq/make/git, ~/.claude exists, ptytest vendored, and emits a coverage report. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0011/spec.md`
- `TASKLIST_ROOT/artifacts/D-0011/notes.md`
- `TASKLIST_ROOT/artifacts/D-0011/evidence.md`

**Deliverables:**
- Click command `eval doctor` in `src/superclaude/cli/eval/commands.py` invoking CapabilityGates and emitting human-readable + JSON output.

**Steps:**
1. **[PLANNING]** Confirm CapabilityGates (T01.11) and CapabilityReport (T01.10) interfaces.
2. **[PLANNING]** Identify required preconditions (claude min_version 0.5.0, ptytest vendored under cli/eval/pty/).
3. **[EXECUTION]** Add `eval_doctor` Click command emitting a green-checklist text and `--json` option.
4. **[EXECUTION]** Wire `--check-coverage` flag for FR-G5 coverage gate (lands in M4 T04.14).
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_doctor.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.13/`.

**Acceptance Criteria:**
- Command `superclaude eval doctor` exits 0 on a clean dev machine with claude>=0.5.0, jq, make, git present and `~/.claude/` extant.
- `superclaude eval doctor --json` emits a deterministic JSON payload matching the CapabilityReport contract.
- Doctor fails closed (exit 2) when any HARD capability is missing; emits a HARD-failure artifact identifying the missing capability.
- `TASKLIST_ROOT/artifacts/D-0011/spec.md` documents the green-checklist format and JSON schema.

**Validation:**
- Manual check: run `superclaude eval doctor` and `superclaude eval doctor --json` on a clean dev machine; compare against expected output.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.07, T01.11
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Coverage gate wiring is partial here; full FR-G5 lands in M4 T04.14.

### T01.14 -- Implement COMP-010 ExpectDSL interface

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | COMP-010 lands the ExpectDSL public interface in M1 so manifest authors can shape `expects:` blocks early; primitives (COMP-010.1-6) land in M4. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0012/spec.md`
- `TASKLIST_ROOT/artifacts/D-0012/notes.md`
- `TASKLIST_ROOT/artifacts/D-0012/evidence.md`

**Deliverables:**
- File `src/superclaude/cli/eval/expect.py` declaring `Expect` class with method stubs and predicate helpers, plus the YAML mapping table.

**Steps:**
1. **[PLANNING]** Read COMP-010 interface contract from roadmap (methods + predicate helpers).
2. **[PLANNING]** Confirm FR-SCH1 (T01.04) validation can route DSL block fields.
3. **[EXECUTION]** Declare `Expect` class with methods `file/jsonl/settings_json/exit_code/stderr/stdout/duration` returning `ExpectCallable` stubs.
4. **[EXECUTION]** Add predicate helpers `contains_event,does_not_contain,event_count,greater_than,less_than,has_content_matching,has_mode,has_registration,hooks_count,is_valid_jsonl,matches_line`.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_interface.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.14/`.

**Acceptance Criteria:**
- File `src/superclaude/cli/eval/expect.py` exports `Expect` with the 7 methods named in COMP-010 and the 11 predicate helpers.
- Each method returns an `ExpectCallable` stub raising `NotImplementedError("M4")` so manifests can be shaped without runtime execution.
- Unit tests instantiate `Expect` and exercise each method against a synthetic `EvalContext` fixture, asserting the stub `NotImplementedError("M4")` is raised consistently (per M1 exit criterion).
- YAML mapping table maps DSL keys to `Expect` methods deterministically.
- `TASKLIST_ROOT/artifacts/D-0012/spec.md` documents the interface contract and M4 deferral.

**Validation:**
- Manual check: import `Expect` and verify each method exists and returns a stub.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.04
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Primitives deferred to M4 (Phase 4) per debate compromise.

### T01.15 -- Add DM-009 ExpectResult record

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | DM-009 carries the assertion outcome returned by every ExpectCallable: name, passed, message, details, duration, optional ExpectFailure. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0013/spec.md`
- `TASKLIST_ROOT/artifacts/D-0013/notes.md`
- `TASKLIST_ROOT/artifacts/D-0013/evidence.md`

**Deliverables:**
- `ExpectResult` frozen dataclass module entry under `src/superclaude/cli/eval/models.py` with the 6 fields from DM-009.

**Steps:**
1. **[PLANNING]** Confirm `ExpectFailure` (T01.16) field requirements.
2. **[PLANNING]** Choose serialization strategy (dataclasses.asdict).
3. **[EXECUTION]** Add `ExpectResult` frozen dataclass with `name,passed,message,details,duration_sec,failure:Optional[ExpectFailure]`.
4. **[EXECUTION]** Implement `to_dict()` for JSON serialization in reporter.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_result.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.15/`.

**Acceptance Criteria:**
- Class `ExpectResult` is frozen and exposes the 6 fields named in DM-009.
- `ExpectResult` is JSON-serializable via `dataclasses.asdict()` per DM-009 "serializable" requirement.
- Construction with valid field types succeeds; `failure` is Optional per DM-009 (no required-when-failed coupling).
- `TASKLIST_ROOT/artifacts/D-0013/spec.md` documents the field contract.

**Validation:**
- Manual check: build a passing + failing ExpectResult, serialize both, compare to expected JSON.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.16
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Consumed by COMP-008 Reporter (T03.13).

### T01.16 -- Add DM-005 ExpectFailure detail record

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | DM-005 carries assertion failure detail (eval_id, expect_id, expect_name, expected, actual, message, artifact_ref, traceback) so reporter can render per-Expect failures. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0014/spec.md`
- `TASKLIST_ROOT/artifacts/D-0014/notes.md`
- `TASKLIST_ROOT/artifacts/D-0014/evidence.md`

**Deliverables:**
- `ExpectFailure` frozen dataclass in `src/superclaude/cli/eval/models.py` with the 8 fields from DM-005.

**Steps:**
1. **[PLANNING]** Read DM-005 fields and confirm one entry per failing Expect.
2. **[PLANNING]** Identify reporter consumer site (COMP-008 T03.13).
3. **[EXECUTION]** Add `ExpectFailure` frozen dataclass with all 8 fields.
4. **[EXECUTION]** Provide `to_dict()` returning a stable ordered mapping.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_failure.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.16/`.

**Acceptance Criteria:**
- Class `ExpectFailure` is frozen and exposes the 8 fields named in DM-005.
- `to_dict()` output is JSON-serializable per DM-005 implicit serialization requirement.
- Reporter produces exactly one ExpectFailure entry per failing Expect (verified by integration test in which 2 failing Expects in a single eval produce 2 ExpectFailure entries).
- `TASKLIST_ROOT/artifacts/D-0014/spec.md` documents the 8-field contract.

**Validation:**
- Manual check: build a reference ExpectFailure and diff `to_dict()` outputs.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** One ExpectFailure per failing Expect; aggregated in EvalOutcome (T03.01).

### T01.17 -- Add AC3 CI dependency-boundary assertion

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | AC3 requires that no new external Python deps land beyond pexpect (transitive via vendored ptytest) and jsonschema (already transitive). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0015/spec.md`
- `TASKLIST_ROOT/artifacts/D-0015/notes.md`
- `TASKLIST_ROOT/artifacts/D-0015/evidence.md`

**Deliverables:**
- CI check (e.g., `make verify-deps` target) comparing `uv pip list` snapshots before/after eval CLI lands.

**Steps:**
1. **[PLANNING]** Read AC3 roadmap entry and identify allowed deps (pexpect, jsonschema).
2. **[PLANNING]** Identify CI insertion point (existing GitHub Actions or Makefile target).
3. **[EXECUTION]** Add `make verify-deps` target running `uv pip list` snapshot diff.
4. **[EXECUTION]** Wire CI to fail on any new top-level dep beyond the allow-list.
5. **[VERIFICATION]** Run `make verify-deps` locally and confirm exit 0 on clean tree.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.17/`.

**Acceptance Criteria:**
- File `Makefile` contains a `verify-deps` target running the `uv pip list` snapshot comparison.
- CI configuration runs `make verify-deps` and fails on new top-level deps outside the allow-list `{pexpect,jsonschema}`.
- `make verify-deps` exits 0 on the current dependency tree (pre-eval-CLI).
- `TASKLIST_ROOT/artifacts/D-0015/spec.md` records the allow-list and CI wiring.

**Validation:**
- Manual check: run `make verify-deps` on a tree with a synthetic added dep and confirm exit non-zero.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** EXEMPT tier per Section 5.3 (CI process check, no runtime code change).

### T01.18 -- Checkpoint: Phase 1 / Tasks T01.13-T01.17

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011,R-012,R-013,R-014,R-015 |
| Why | Gate: verify doctor command, ExpectDSL interface, ExpectResult/Failure models, and dep-boundary CI before scratch-root allowlist gates them. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01-MID-T13-T17 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-T13-T17.md`

**Purpose:** Verify doctor command + ExpectDSL interface + Expect{Result,Failure} + AC3 before downstream consumers.

**Verification:**
- `superclaude eval doctor` exits 0 on a clean dev machine and `--json` returns a valid CapabilityReport.
- `src/superclaude/cli/eval/expect.py` exports `Expect` with the 7 methods + 11 predicate helpers; primitives stubbed to `NotImplementedError("M4")`.
- `make verify-deps` exits 0 on the current dependency tree.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_doctor.py tests/cli/eval/test_expect_interface.py tests/cli/eval/test_expect_result.py tests/cli/eval/test_expect_failure.py -v` exits 0.
- `make verify-deps` exits 0.
- Checkpoint report `CP-P01-T13-T17.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P01-T13-T17.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T01.13-T01.17).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.13..T01.17
**Rollback:** N/A (checkpoints are read-only verifications)

### T01.19 -- Enforce AC12 Allowed scratch roots in EvalConfig

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | AC12 codifies the only safe scratch root locations: `/tmp/eval-runs/`, repo `.dev/eval-runs/`, or `--output-dir` resolved against the allowlist; rejection enforced in EvalConfig. |
| Effort | M |
| Risk | High |
| Risk Drivers | security (containment allowlist) |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0016/spec.md`
- `TASKLIST_ROOT/artifacts/D-0016/notes.md`
- `TASKLIST_ROOT/artifacts/D-0016/evidence.md`

**Deliverables:**
- `resolve_scratch_root(path)` helper raising `ScratchRootViolation` when path is not under `/tmp/eval-runs`, repo `.dev/eval-runs`, or `--output-dir`.

**Steps:**
1. **[PLANNING]** Confirm EvalConfig.allowed_scratch_roots (T01.01) is the single source.
2. **[PLANNING]** Identify caller sites (SuiteLoader, HomeIsolation, CLI run command).
3. **[EXECUTION]** Implement `resolve_scratch_root` using `Path.resolve()` and `is_relative_to()` against allowlist.
4. **[EXECUTION]** Add `--output-dir` resolution path with explicit allowlist enforcement.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_scratch_root_allowlist.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.19/`.

**Acceptance Criteria:**
- Function `resolve_scratch_root(path)` raises `ScratchRootViolation` for `/home/user/foo`, `/var/lib/eval-runs`, and any non-allowlisted prefix.
- Resolved paths under `/tmp/eval-runs/`, repo `.dev/eval-runs/`, or a CLI-supplied `--output-dir` pass.
- Allowlist source is `EvalConfig.allowed_scratch_roots`; no other module embeds a hard-coded copy.
- `TASKLIST_ROOT/artifacts/D-0016/spec.md` documents the allowlist policy.

**Validation:**
- Manual check: invoke `resolve_scratch_root("/etc/passwd")` and confirm `ScratchRootViolation`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Defense-in-depth layered with FR-ISO2 (T02.08) and NFR-SEC2 (T02.09).

### T01.20 -- Wire AC11 Source-of-truth discipline gate

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017 |
| Why | AC11 requires `make verify-sync` to pass and a pre-commit hook to reject edits to `.claude/` without sync-back from `src/superclaude/`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0017/spec.md`
- `TASKLIST_ROOT/artifacts/D-0017/notes.md`
- `TASKLIST_ROOT/artifacts/D-0017/evidence.md`

**Deliverables:**
- `make verify-sync` target + pre-commit hook ensuring `src/superclaude/` and `.claude/` parity for skills/agents/commands.

**Steps:**
1. **[PLANNING]** Confirm `make sync-dev` and `make verify-sync` Makefile targets exist.
2. **[PLANNING]** Identify pre-commit framework (existing `.pre-commit-config.yaml` or new hook).
3. **[EXECUTION]** Extend `make verify-sync` to cover any new `src/superclaude/cli/eval/` sources mirrored into `.claude/`.
4. **[EXECUTION]** Wire a pre-commit hook that fails on edits to `.claude/` without a corresponding sync-back commit.
5. **[VERIFICATION]** Run `make verify-sync` locally and confirm exit 0.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.20/`.

**Acceptance Criteria:**
- Target `make verify-sync` exists in `Makefile` and exits 0 on a synced tree.
- Pre-commit hook rejects a synthetic commit that edits a `.claude/` file without touching the matching `src/superclaude/` source.
- Pre-commit hook test fixture confirms a benign synced edit is allowed (positive case).
- `TASKLIST_ROOT/artifacts/D-0017/spec.md` records the gate wiring.

**Validation:**
- Manual check: edit a `.claude/` file directly and attempt commit; confirm pre-commit failure.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Source-of-truth discipline carried into MIG-001 (T06.14).

### T01.21 -- Implement FR-CLI2 `eval list` subcommand

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018 |
| Why | FR-CLI2 enumerates suites from `cli/eval/suites/*.yaml` with `--json` option; handles empty directory; exits 0. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0018/spec.md`
- `TASKLIST_ROOT/artifacts/D-0018/notes.md`
- `TASKLIST_ROOT/artifacts/D-0018/evidence.md`

**Deliverables:**
- Click command `eval list` in `src/superclaude/cli/eval/commands.py` printing suite name+version+eval count.

**Steps:**
1. **[PLANNING]** Confirm SuiteLoader (T01.07) is available for enumeration.
2. **[PLANNING]** Define empty-directory behavior (exit 0 with empty list message).
3. **[EXECUTION]** Add `eval_list` Click command iterating `suites/*.yaml`.
4. **[EXECUTION]** Wire `--json` option emitting a list of `{name, version, eval_count}` dicts.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_list.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.21/`.

**Acceptance Criteria:**
- Command `superclaude eval list` exits 0 with at least one suite present and zero suites present (empty-directory case).
- `--json` flag emits a JSON array with `{name,version,eval_count}` entries.
- Output is deterministic for a given suite directory (sorted by filename).
- `TASKLIST_ROOT/artifacts/D-0018/spec.md` records the output schema.

**Validation:**
- Manual check: run `superclaude eval list` and `superclaude eval list --json` against fixture suite directory.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.07
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Empty-directory handling required by FR-CLI2 AC.

### T01.22 -- Implement FR-CLI3 `eval describe` subcommand

| Field | Value |
|---|---|
| Roadmap Item IDs | R-019 |
| Why | FR-CLI3 prints manifest content for a suite or single eval; `--suite` required; `--eval` optional; validates before print; prints resolved (post-parameterize) manifest. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0019 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0019/spec.md`
- `TASKLIST_ROOT/artifacts/D-0019/notes.md`
- `TASKLIST_ROOT/artifacts/D-0019/evidence.md`

**Deliverables:**
- Click command `eval describe` printing the post-parameterize-expansion manifest content as YAML or JSON.

**Steps:**
1. **[PLANNING]** Confirm SuiteLoader (T01.07) + FR-SCH1 (T01.04) for validation.
2. **[PLANNING]** Define output format precedence (YAML default; `--json` opt-in).
3. **[EXECUTION]** Add `eval_describe` Click command requiring `--suite` and optional `--eval`.
4. **[EXECUTION]** Validate manifest before print; emit resolved (post-parameterize) content.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_describe.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.22/`.

**Acceptance Criteria:**
- Command `superclaude eval describe --suite <name>` prints validated post-parameterize manifest content for the suite.
- `--eval <id>` filters to a single eval; missing id exits 2 with `EvalNotFound`.
- Validation runs before any print operation; invalid manifest exits 2.
- `TASKLIST_ROOT/artifacts/D-0019/spec.md` records flag semantics.

**Validation:**
- Manual check: run `superclaude eval describe --suite real --eval E1` and inspect output.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.04, T01.07
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Output mirrors validated manifest exactly; no editorial transformation.

### T01.23 -- Author TEST-001 schema and ID rejection pytest module

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | TEST-001 is a first-class test deliverable covering schema errors, unsafe IDs, parameterized IDs, and preflight ordering; cross-links NFR-SEC1. |
| Effort | M |
| Risk | High |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0020 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0020/spec.md`
- `TASKLIST_ROOT/artifacts/D-0020/notes.md`
- `TASKLIST_ROOT/artifacts/D-0020/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_schema_id_rejection.py` covering schema errors, unsafe IDs, parameterized IDs, and pre-flight ordering (no FS writes before rejection).

**Steps:**
1. **[PLANNING]** Confirm `validate_manifest` (T01.04) and `validate_eval_id` (T01.05) plus NFR-SEC1 cases (T01.08).
2. **[PLANNING]** Enumerate test cases: invalid schema field, unsafe id, parameterized-unsafe, ordering check.
3. **[EXECUTION]** Author `tests/cli/eval/test_schema_id_rejection.py` with one test per case.
4. **[EXECUTION]** Add a snapshot-fixture test verifying no FS writes occur before rejection.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_schema_id_rejection.py -v` and confirm all assertions.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.23/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_schema_id_rejection.py` exists and contains tests for schema-violation rejection, unsafe id rejection, parameterize expansion validated post-expansion (both safe and unsafe expansion cases), and pre-flight ordering (no FS writes before rejection).
- `uv run pytest tests/cli/eval/test_schema_id_rejection.py -v` exits 0 with at least 4 passing tests.
- Tests assert process exit code 2 on schema-violation and unsafe-id rejection paths (per FR-SCH1 + FR-SCH2 AC).
- Test docstrings cross-link FR-SCH1, FR-SCH2, and NFR-SEC1 by ID; `TASKLIST_ROOT/artifacts/D-0020/spec.md` documents the test matrix.

**Validation:**
- Manual check: run the targeted pytest command above and confirm all assertions pass.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.04, T01.05, T01.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Snapshot-fixture verification proves preflight ordering claim.

### T01.24 -- Checkpoint: Phase 1 / Tasks T01.19-T01.23

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016,R-017,R-018,R-019,R-020 |
| Why | Gate: verify scratch-root allowlist, source-of-truth CI, eval list/describe, and schema/ID rejection tests before OPS-001 + CLI registration close M1. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01-MID-T19-T23 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-T19-T23.md`

**Purpose:** Verify scratch-root enforcement + source-of-truth gate + list/describe + schema/ID rejection tests before closing M1.

**Verification:**
- `resolve_scratch_root` rejects non-allowlisted prefixes and accepts the three allowed roots.
- `make verify-sync` exits 0 and the pre-commit hook rejects untracked `.claude/` edits.
- `tests/cli/eval/test_schema_id_rejection.py` passes with all 4+ assertions.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_scratch_root_allowlist.py tests/cli/eval/test_list.py tests/cli/eval/test_describe.py tests/cli/eval/test_schema_id_rejection.py -v` exits 0.
- `make verify-sync` exits 0.
- Checkpoint report `CP-P01-T19-T23.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P01-T19-T23.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T01.19-T01.23).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.19..T01.23
**Rollback:** N/A (checkpoints are read-only verifications)

### T01.25 -- Record OPS-001 decision artifacts in decisions.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021 |
| Why | OPS-001 closes ADR sign-off, PTY flag semantics, JUnit flag, time offset, retry policy, and NOTICE handling per OQ-1/3/7/8/10 resolutions. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0021 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0021/spec.md`
- `TASKLIST_ROOT/artifacts/D-0021/notes.md`
- `TASKLIST_ROOT/artifacts/D-0021/evidence.md`

**Deliverables:**
- Updated `.dev/releases/current/cliEval/decisions.md` recording D-5..D-8 queue, OQ-1/3/7/8/10 resolution status, and implementation gates referencing decisions.

**Steps:**
1. **[PLANNING]** Identify decisions.md location and current state.
2. **[PLANNING]** Inventory OQ-1, OQ-3, OQ-7, OQ-8, OQ-10 with current resolutions or owners.
3. **[EXECUTION]** Append D-5..D-8 entries with sign-off-pending status.
4. **[EXECUTION]** Cross-reference implementation gate sites (M1 schema freeze, M2 vendoring, etc.).
5. **[VERIFICATION]** Manual review by maintainer.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.25/`.

**Acceptance Criteria:**
- File `.dev/releases/current/cliEval/decisions.md` contains entries D-5..D-8 with status `queued for sign-off`.
- Each OQ-1, OQ-3, OQ-7, OQ-8, OQ-10 has a resolution-status field or owner pointer.
- Implementation gates reference decisions by ADR ID.
- `TASKLIST_ROOT/artifacts/D-0021/spec.md` records the update summary.

**Validation:**
- Manual check: maintainer reviews decisions.md and confirms entries exist.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** EXEMPT tier per Section 5.3 (documentation/ADR closure).

### T01.26 -- Register `superclaude eval` Click group without breaking existing commands (FR-G3)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-022 |
| Why | FR-G3 requires additive CLI integration: register `eval` group via entrypoint with no impact on existing commands; help text lists eval group. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0022 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0022/spec.md`
- `TASKLIST_ROOT/artifacts/D-0022/notes.md`
- `TASKLIST_ROOT/artifacts/D-0022/evidence.md`

**Deliverables:**
- Registered `superclaude eval` Click group in `src/superclaude/cli/__init__.py` (or matching entry point), with help text exposing the group.

**Steps:**
1. **[PLANNING]** Identify existing CLI entry point (typically `src/superclaude/cli/main.py`).
2. **[PLANNING]** Confirm subcommands list/describe/doctor are imported from `src/superclaude/cli/eval/commands.py`.
3. **[EXECUTION]** Register the `eval` Click group at the existing entry point.
4. **[EXECUTION]** Run regression smoke against pre-existing commands to confirm unchanged behavior.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/test_cli_registration.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T01.26/`.

**Acceptance Criteria:**
- `superclaude --help` lists `eval` as a subcommand group.
- `superclaude eval --help` lists the M1 subcommands (`list`, `describe`, `doctor`); additional subcommands land per their milestones (`run` per FR-CLI1 in M4).
- Existing `superclaude` subcommands behave identically (regression test snapshot).
- `TASKLIST_ROOT/artifacts/D-0022/spec.md` records entry-point wiring.

**Validation:**
- Manual check: run `superclaude --help` and `superclaude eval --help` after install.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.13, T01.21, T01.22
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Group registration is additive only; no existing command path changes.

### T01.27 -- Checkpoint: End of Phase 1

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001..R-022 |
| Why | M1 exit gate: confirm doctor outline runs, schema validates v1 manifest, eval_id regex rejects unsafe ids with exit 2 before any FS write, DSL interface exercises against synthetic EvalContext, and CLI group is registered. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`

**Purpose:** M1 exit gate: foundation, schema, regex guard, DSL interface, capability gates, doctor outline, and CLI group registration verified.

**Verification:**
- `superclaude eval doctor` capability outline runs and exits 0 on clean dev machine.
- `validate_manifest()` accepts the v1 reference manifest and rejects invalid fixtures.
- `validate_eval_id()` rejects all NFR-SEC1 traversal cases before any FS write.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/ -v` passes on M1 modules.
- `superclaude eval --help` lists `list`,`describe`,`doctor` subcommands.
- Checkpoint report `CP-P01-END.md` records pass/fail per task in Phase 1.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P01-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T01.01-T01.26).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01..T01.26
**Rollback:** N/A (checkpoints are read-only verifications)
