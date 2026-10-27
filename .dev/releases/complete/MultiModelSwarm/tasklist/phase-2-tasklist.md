# Phase 2 -- Preflight, Schema, Lens Registry & Injection Guard (Wave 0)

**Goal:** Build Wave 0 — JSON Schema validation with cross-field rules, lens resolution and materialization, the 8-entry lens registry plus PR-grade validator, the §11.5 prompt-injection guard enforced identically across all three prompt-input paths (lens / JSON-Schema / custom-prompt-dir), and the INV-005 / INV-007 worker-pool guards. Exit when `swarm validate` and `swarm validate-lenses` both pass on the bundled registry, the injection guard is enforced on every path, the empty-target guard STOPs before dispatch, the worker-vs-pool guard and empty-pool failure semantics are operational, and OQ-007 / OQ-008 / OQ-010 are resolved.

### T02.01 -- Build schema module with cross-field validators

| Field | Value |
|---|---|
| Roadmap | R-030 (COMP-005) |
| Deliverables | D-0026 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, auggie, context7 (jsonschema) |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `src/superclaude/cli/swarm/schema.py` with JSON Schema + cross-field validators.

**Steps:**
1. [PLANNING] Enumerate DM-001 sub-fields from JobSpec.
2. [EXECUTION] Implement JSON Schema covering all DM-001 leaves.
3. [EXECUTION] Add cross-field rules + §11.5 required-substring on `prompt.system`.
4. [VERIFICATION] Pass valid + reject invalid specs (fixture-based).
5. [COMPLETION] `make verify-sync`.

**Acceptance Criteria:**
- `cli/swarm/schema.py` exists and validates all DM-001 subfields.
- §11.5 required-substring rule enforced on `prompt.system`.
- Invalid specs rejected pre-dispatch with structured diagnostics.
- Schema version pinned via `spec_version`.

**Validation:**
- `uv run pytest tests/swarm/test_schema.py -v` passes.
- Fixture: spec missing §11.5 substring → rejected.

**Dependencies:** T01.13. **Rollback:** revert schema module.
**Notes:** STRICT — security-critical (§11.5 enforcement).

### T02.02 -- Implement preflight (Wave 0) module

| Field | Value |
|---|---|
| Roadmap | R-031 (COMP-006) |
| Deliverables | D-0027 |
| Effort | L |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `cli/swarm/preflight.py` running lens resolution → materialization → manifest emit → state init.

**Steps:**
1. [PLANNING] Map Wave 0 phases against roadmap COMP-006 description.
2. [EXECUTION] Implement `run_preflight(job_spec) -> Manifest`.
3. [EXECUTION] Wire schema validation + injection-guard enforcement + IMM-4 empty-target guard call sites.
4. [VERIFICATION] End-to-end Wave 0 pass on stub fixture.
5. [COMPLETION] `make verify-sync`.

**Acceptance Criteria:**
- `cli/swarm/preflight.py::run_preflight` resolves lens, materializes prompts, writes manifest, sets `state=preflight_ok`.
- Calls schema validator, §11.5 guard, IMM-4 guard, INV-005/007 guards.
- Returns Manifest object (or raises with structured failure contract).
- Wave 0 entry test green.

**Validation:**
- `uv run pytest tests/swarm/test_preflight.py -v` passes.
- Stub spec yields valid Manifest.

**Dependencies:** T01.27, T02.01, T02.14. **Rollback:** revert preflight module.

### T02.03 -- Enforce FR-019 job-spec schema validation with §11.5 substring rule

| Field | Value |
|---|---|
| Roadmap | R-032 (FR-019) |
| Deliverables | D-0028 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. Cross-field validator + §11.5 substring assertion in schema module.

**Steps:**
1. [EXECUTION] Add §11.5 substring rule on `prompt.system`.
2. [EXECUTION] Add cross-field rules (e.g., custom_prompt_dir requires lens=='custom').
3. [VERIFICATION] Negative-test fixtures.

**Acceptance Criteria:**
- `tests/swarm/test_schema_injection_substring.py` exists and passes.
- Invalid specs rejected pre-dispatch with structured diagnostics naming failing rule.
- §11.5 substring rule enforced on `prompt.system`.
- Cross-field rules cover custom_prompt_dir+lens interaction.

**Validation:**
- `uv run pytest tests/swarm/test_schema_injection_substring.py -v` passes.
- Fixture without substring is rejected.

**Dependencies:** T02.01.
**Notes:** STRICT — security-critical injection-guard binding.

### T02.04 -- Implement FR-020 lens-driven defaults expansion at preflight

| Field | Value |
|---|---|
| Roadmap | R-033 (FR-020) |
| Deliverables | D-0029 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:** 1. `preflight.py::expand_lens_defaults(spec, registry) -> ResolvedLensEntry`.

**Steps:**
1. [PLANNING] Enumerate the 10 fields expanded from LENSES[lens].
2. [EXECUTION] Implement default-expansion function.
3. [VERIFICATION] Test expansion produces every listed default.

**Acceptance Criteria:**
- `preflight.py::expand_lens_defaults` populates system/user_template/recipe/template_path/workers.count/line_cap/filename_template/lens_name/next_command_template/suspect/tier from LENSES[lens].
- Unknown lens → structured failure.
- ResolvedLensEntry returned matches LENSES entry verbatim on all 10 fields.
- Test fixture for bare-review lens passes.

**Validation:**
- `uv run pytest tests/swarm/test_lens_defaults.py -v` passes.
- bare-review spec expansion produces expected fields.

**Dependencies:** T02.14, T02.02.

### T02.05 -- Implement FR-021 custom-prompt-dir escape hatch

| Field | Value |
|---|---|
| Roadmap | R-034 (FR-021) |
| Deliverables | D-0030 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `preflight.py::read_custom_prompt_dir(path) -> (system, user, meta)`.

**Steps:**
1. [PLANNING] Confirm INV-003 substring rule applies here too.
2. [EXECUTION] Implement directory reader for system.txt / user.txt / meta.yaml.
3. [EXECUTION] Wire §11.5 substring check on `system.txt` contents.
4. [VERIFICATION] Missing-file + missing-substring negative tests.

**Acceptance Criteria:**
- `preflight.py::read_custom_prompt_dir` reads `<dir>/system.txt`, `user.txt`, `meta.yaml`.
- Missing file → structured failed contract.
- §11.5 substring enforced on `system.txt` contents identically to lens path.
- 3 files round-trip into Manifest snapshot.

**Validation:**
- `uv run pytest tests/swarm/test_custom_prompt_dir.py -v` passes.
- Missing system.txt produces failed contract.

**Dependencies:** T02.04, T02.07.
**Notes:** STRICT — security-critical escape hatch.

### T02.06 -- Checkpoint: Phase 2 mid-phase (schema + preflight foundations)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP2-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- T02.01..T02.05 done.
- `phase-2-cp1.md` checkpoint report exists.
- Schema, preflight, lens-defaults expansion, custom-prompt-dir reader all green.
- §11.5 substring rule enforced in schema.

**Validation:** Checkpoint file exists; `grep -c "status: done" execution-log.yaml` ≥ 32.
**Dependencies:** T02.01..T02.05.

### T02.07 -- Enforce §11.5 prompt-injection guard across all 3 prompt-input paths

| Field | Value |
|---|---|
| Roadmap | R-035 (§11.5) |
| Deliverables | D-0031 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `preflight.py::enforce_injection_guard` wrapping target in delimiters + asserting substring on lens/schema/custom-prompt-dir paths.

**Steps:**
1. [PLANNING] Map the 3 prompt-input paths.
2. [EXECUTION] Implement central guard function called from each path.
3. [VERIFICATION] Parametrized test covers all 3 paths.

**Acceptance Criteria:**
- `tests/swarm/test_injection_guard_all_paths.py` exists and passes.
- Delimiters `<<<TARGET>>>` / `<<<END TARGET>>>` applied; required-substring present on lens, JSON-Schema, and custom-prompt-dir paths.
- Bypass attempts (target containing end-marker) neutralized.
- All 3 paths share single enforcement code path.

**Validation:**
- `uv run pytest tests/swarm/test_injection_guard_all_paths.py -v` passes.
- Mutation: dropping one path's enforcement fails the parametrized test.

**Dependencies:** T02.02, T02.03.

### T02.08 -- Add INV-003 custom-prompt-dir identical-guard test

| Field | Value |
|---|---|
| Roadmap | R-036 (INV-003) |
| Deliverables | D-0032 |
| Effort | S |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests + verify-sync |

**Deliverables:** 1. `tests/swarm/test_custom_prompt_dir_injection_guard.py`.

**Steps:** [PLANNING] confirm guard helper available. [EXECUTION] write parity test. [VERIFICATION] run.

**Acceptance Criteria:**
- `tests/swarm/test_custom_prompt_dir_injection_guard.py` exists.
- Asserts `--custom-prompt-dir` preflight rejects missing substring.
- Same fixture used for lens path produces identical rejection.
- Failure message identifies failing rule.

**Validation:**
- `uv run pytest tests/swarm/test_custom_prompt_dir_injection_guard.py -v` passes.
- Mutation: bypassing guard on custom-prompt-dir path fails test.

**Dependencies:** T02.07.

### T02.09 -- Add INV-014 escape-hatch isomorphism test

| Field | Value |
|---|---|
| Roadmap | R-037 (INV-014) |
| Deliverables | D-0033 |
| Effort | S |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests + verify-sync |

**Deliverables:** 1. `tests/swarm/test_escape_hatch_guard_parity.py`.

**Steps:** [EXECUTION] parametrize a guard violation across both paths; assert identical rejection.

**Acceptance Criteria:**
- `tests/swarm/test_escape_hatch_guard_parity.py` exists.
- Parity test: lens path and `--custom-prompt-dir` path both reject the same guard violation.
- Failure messages structurally similar.
- Test catches asymmetric guard regression.

**Validation:**
- `uv run pytest tests/swarm/test_escape_hatch_guard_parity.py -v` passes.
- Mutation: removing one path's guard fails the parity assertion.

**Dependencies:** T02.08.

### T02.10 -- Implement INV-005 worker-count vs model-pool guard

| Field | Value |
|---|---|
| Roadmap | R-038 (INV-005) |
| Deliverables | D-0034 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `preflight.py::check_pool_size(workers, pool)`.

**Steps:**
1. [PLANNING] Read OQ-007 resolution from M1 exit notes.
2. [EXECUTION] Implement guard with both warn-with-defaults vs STOP branches.
3. [VERIFICATION] Parametrized test covers both OQ-007 branches.

**Acceptance Criteria:**
- `preflight.py::check_pool_size` detects workers_exceed_pool.
- Behavior matches OQ-007 resolution (warn-with-defaults vs STOP).
- Test covers both branches.
- Resolution recorded in `docs/swarm/oq-resolutions.md`.

**Validation:**
- `uv run pytest tests/swarm/test_inv005_pool_guard.py -v` passes.
- OQ-007 resolution captured.

**Dependencies:** T01.14.
**Notes:** Requires OQ-007 resolution from M1 exit. Clarification task T02.10a flagged below if unresolved.

### T02.11 -- Implement INV-007 empty-pool failure contract

| Field | Value |
|---|---|
| Roadmap | R-039 (INV-007) |
| Deliverables | D-0035 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `preflight.py::emit_env_missing_contract`.

**Steps:**
1. [PLANNING] Confirm OQ-008 resolved (via INV-007 itself per roadmap).
2. [EXECUTION] Detect empty pool pre-dispatch; emit structured `failed`/`env-missing` contract when output dir creatable; bare abort otherwise.
3. [VERIFICATION] Two-branch test (output dir creatable vs not).

**Acceptance Criteria:**
- `preflight.py::emit_env_missing_contract` writes `failed`/`env-missing` contract when output dir creatable.
- Pre-output abort when output dir not creatable.
- Reason field populated (`reason: env-missing`).
- Both branches tested.

**Validation:**
- `uv run pytest tests/swarm/test_inv007_empty_pool.py -v` passes.
- OQ-008 resolution recorded.

**Dependencies:** T02.10.

### T02.12 -- Checkpoint: Phase 2 mid-phase (injection guard + pool guards verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP2-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- T02.07..T02.11 done.
- `phase-2-cp2.md` checkpoint report exists.
- §11.5 enforced on all 3 paths; INV-005/007 guards green.
- OQ-007, OQ-008 resolutions recorded.

**Validation:** Checkpoint file exists; `grep -c "status: done"` ≥ 38.
**Dependencies:** T02.07..T02.11.

### T02.13 -- Implement IMM-4 empty-target guard

| Field | Value |
|---|---|
| Roadmap | R-040 (IMM-4) |
| Deliverables | D-0036 |
| Effort | S |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests + verify-sync |

**Deliverables:** 1. `preflight.py::guard_empty_target`.

**Steps:**
1. [EXECUTION] Implement <50 non-whitespace-byte check after truncation.
2. [VERIFICATION] 49-byte fixture produces failed contract; no dispatch occurs.

**Acceptance Criteria:**
- `preflight.py::guard_empty_target` rejects targets with <50 non-whitespace bytes.
- Failed contract reason: `target-too-small`.
- STOP before any dispatch.
- 49-byte fixture test green.

**Validation:**
- `uv run pytest tests/swarm/test_imm4_empty_target.py -v` passes.
- Dispatch never reached for 49-byte target (mock dispatcher records 0 calls).

**Dependencies:** T02.02.

### T02.14 -- Implement LENSES dict + helpers

| Field | Value |
|---|---|
| Roadmap | R-041 (COMP-022) |
| Deliverables | D-0037 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `cli/swarm/lenses/__init__.py` exporting `LENSES` dict + helper accessors.

**Steps:**
1. [EXECUTION] Create LENSES dict mapping 8 names → LensEntry.
2. [EXECUTION] Add helper `get_lens(name) -> LensEntry`.
3. [VERIFICATION] Registry import test loads 8 entries.

**Acceptance Criteria:**
- `cli/swarm/lenses/__init__.py` exports `LENSES: dict[str, LensEntry]`.
- Registry loads 8 entries (bare_review, refactor_find, edge_case_hunt, spec_completeness, feasibility_probe, troubleshoot_hypothesis, doc_completeness, custom).
- `get_lens(name)` resolves; unknown raises KeyError.
- Round-trip from registry → manifest snapshot intact.

**Validation:**
- `uv run pytest tests/swarm/test_lenses_registry.py -v` passes.
- `len(LENSES) == 8`.

**Dependencies:** T01.23, T02.23.

### T02.15 -- Implement _validate (lens validator) module

| Field | Value |
|---|---|
| Roadmap | R-042 (COMP-023) |
| Deliverables | D-0038 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `cli/swarm/lenses/_validate.py` with 5-assertion validator.

**Steps:** [EXECUTION] implement file-refs / recipe-registered / suspect-coupling / name-uniqueness / §11.5-substring assertions. [VERIFICATION] fixtures.

**Acceptance Criteria:**
- `_validate.py` enforces 5 assertions: file refs resolve, recipe registered, suspect↔suspect_files coupling, name uniqueness, §11.5 substring in `system_prompt_fragment`.
- Non-conforming entry fails with clear diagnostic.
- Each assertion has dedicated test.
- Fails fast on first violation.

**Validation:**
- `uv run pytest tests/swarm/test_lens_validator.py -v` passes.
- Mutation: dropping §11.5 substring fails validation.

**Dependencies:** T02.14.

### T02.16 -- Implement U-008 swarm validate-lenses logic

| Field | Value |
|---|---|
| Roadmap | R-043 (U-008) |
| Deliverables | D-0039 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests + verify-sync |

**Deliverables:** 1. `_validate.py::validate_all(registry)`.

**Steps:** [EXECUTION] iterate LENSES; run all 5 assertions per entry. [VERIFICATION] fixture bundle passes.

**Acceptance Criteria:**
- `validate_all` iterates LENSES and runs all 5 assertions per entry.
- Asserts: file refs resolve, recipe_name registered, suspect:true entries include `{suspect_files}` in next-cmd template, name uniqueness, §11.5 substring in system_prompt_fragment.
- 7 non-custom entries pass against bundled registry.
- Failure surfaces first failing assertion + entry name.

**Validation:**
- `uv run pytest tests/swarm/test_validate_all_lenses.py -v` passes.
- 7 of 8 bundled entries pass (`custom` is escape hatch).

**Dependencies:** T02.15.

### T02.17 -- Bundle 8-entry lens registry (FR-009)

| Field | Value |
|---|---|
| Roadmap | R-044 (FR-009) |
| Deliverables | D-0040 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests + verify-sync |

**Deliverables:** 1. LENSES dict populated with 8 entries.

**Steps:** [EXECUTION] populate registry from individual lens files (see T02.23). [VERIFICATION] count + validator gate.

**Acceptance Criteria:**
- LENSES dict contains 8 entries: bare-review, refactor-find, edge-case-hunt, spec-completeness, feasibility-probe, troubleshoot-hypothesis, doc-completeness, custom.
- 7 non-custom entries pass U-008 validator.
- `custom` entry intentionally bypasses validation (escape hatch).
- Entry order documented.

**Validation:**
- `uv run pytest tests/swarm/test_lens_registry_count.py -v` passes.
- `validate-lenses` exits 0 on bundled set.

**Dependencies:** T02.16, T02.23.

### T02.18 -- Checkpoint: Phase 2 mid-phase (lens registry + validator green)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP2-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- T02.13..T02.17 done.
- `phase-2-cp3.md` checkpoint report exists.
- IMM-4 guard green; 8-lens registry + validator green.

**Validation:** Checkpoint file exists; `grep -c "status: done"` ≥ 43.
**Dependencies:** T02.13..T02.17.

### T02.19 -- Implement FR-007 swarm validate subcommand

| Field | Value |
|---|---|
| Roadmap | R-045 (FR-007) |
| Deliverables | D-0041 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:** 1. `commands.py::validate_cmd`.

**Steps:** [EXECUTION] wire subcommand to schema validator. [VERIFICATION] valid + invalid fixtures.

**Acceptance Criteria:**
- `commands.py::validate_cmd` registered with `swarm_group`.
- Exits 0 on valid spec.
- Exits non-zero with structured diagnostics on invalid spec.
- Supports `--strict` flag (future-proofing).

**Validation:**
- `uv run pytest tests/swarm/test_validate_cmd.py -v` passes.
- `superclaude swarm validate <good.json>` exits 0.

**Dependencies:** T02.01.

### T02.20 -- Implement FR-008 swarm validate-lenses subcommand

| Field | Value |
|---|---|
| Roadmap | R-046 (FR-008) |
| Deliverables | D-0042 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:** 1. `commands.py::validate_lenses_cmd`.

**Steps:** [EXECUTION] wire subcommand to U-008 validator. [VERIFICATION] resolved OQ-010 failure semantics.

**Acceptance Criteria:**
- `commands.py::validate_lenses_cmd` registered.
- Exits 0 when registry passes; reports first failure with entry name otherwise.
- Failure semantics per OQ-010 resolution (exit code + blocking/warning policy).
- Supports `--warning-mode` flag if OQ-010 resolves to warning-mode.

**Validation:**
- `uv run pytest tests/swarm/test_validate_lenses_cmd.py -v` passes.
- `superclaude swarm validate-lenses` exits 0 on bundled set.

**Dependencies:** T02.16.

### T02.21 -- Implement FR-LENSREG.NS normalizer_strategy field

| Field | Value |
|---|---|
| Roadmap | R-047 (FR-LENSREG.NS) |
| Deliverables | D-0043 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:** 1. `LENSES` entry schema updated with `normalizer_strategy` field; validator asserts match.

**Steps:** [EXECUTION] add field to LensEntry. [EXECUTION] extend validator. [VERIFICATION] negative-case test.

**Acceptance Criteria:**
- `LENSES` entries declare `normalizer_strategy` matching the prompt's expected output shape.
- Validator asserts a registered Recipe matches the strategy.
- `validate-lenses` fails when `normalizer_strategy` is missing or unmatched.
- Documented in lens-contribution-policy.

**Validation:**
- `uv run pytest tests/swarm/test_normalizer_strategy.py -v` passes.
- Missing field test fails validation.

**Dependencies:** T02.20.

### T02.22 -- Implement FR-024 --auto-inject-guard flag

| Field | Value |
|---|---|
| Roadmap | R-048 (FR-024) |
| Deliverables | D-0044 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests + verify-sync |

**Deliverables:** 1. `preflight.py::auto_inject_guard` helper + Click flag.

**Steps:** [EXECUTION] add `--auto-inject-guard` flag; when set, prepend canonical §11.5 sentence to `system.txt` reads. [VERIFICATION] flag + no-flag paths.

**Acceptance Criteria:**
- `--auto-inject-guard` flag prepends canonical §11.5 sentence on custom-prompt-dir path.
- Absent flag preserves §11.5 required-substring enforcement (no silent bypass).
- Migration path documented for legacy users.
- Test covers both modes.

**Validation:**
- `uv run pytest tests/swarm/test_auto_inject_guard.py -v` passes.
- Without flag + missing substring → rejected.

**Dependencies:** T02.05, T02.07.

### T02.23 -- Bundle 7 non-custom lens entry files (COMP-024..030 merged)

| Field | Value |
|---|---|
| Roadmap | R-049..R-055 (COMP-024..COMP-030 merged) |
| Deliverables | D-0045 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `cli/swarm/lenses/{bare_review, refactor_find, edge_case_hunt, spec_completeness, feasibility_probe, troubleshoot_hypothesis, doc_completeness}.py`.

**Steps:**
1. [PLANNING] Map each roadmap row to its LensEntry field values.
2. [EXECUTION] Write 7 lens files; each exports a `LENS` constant.
3. [EXECUTION] Aggregate into `LENSES` dict via `lenses/__init__.py`.
4. [VERIFICATION] All 7 pass U-008 validator.

**Acceptance Criteria:**
- 7 lens files exist under `cli/swarm/lenses/`.
- Each declares `LensEntry(name=..., system_prompt_fragment=..., user_template=..., recipe_name=..., default_workers=..., suspect=..., tier=..., recommended_next_command_template=..., stability=...)`.
- bare_review.suspect=True, tier=T2, workers=3; edge_case_hunt.workers=4; troubleshoot_hypothesis.workers=4.
- All 7 pass `validate-lenses`.

**Validation:**
- `uv run pytest tests/swarm/test_bundled_lenses.py -v` passes.
- `validate-lenses` exit 0.

**Dependencies:** T02.16.
**Notes:** 7 small lens files merged into one task — each is ~30 LOC dataclass instantiation, mechanically identical.

### T02.24 -- Checkpoint: Phase 2 mid-phase (subcommands + bundled lenses green)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP2-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- T02.19..T02.23 done.
- `phase-2-cp4.md` checkpoint report exists.
- `validate` + `validate-lenses` subcommands functional; 7 non-custom lenses pass validator.

**Validation:** Checkpoint exists; `grep -c "status: done"` ≥ 48.
**Dependencies:** T02.19..T02.23.

### T02.25 -- Implement DM-020 CallerMetadata at preflight

| Field | Value |
|---|---|
| Roadmap | R-056 (DM-020) |
| Deliverables | D-0046 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:** 1. `models.py::CallerMetadata` + preflight resolution.

**Steps:** [PLANNING] confirm OQ-009 precedence resolution. [EXECUTION] dataclass + resolution logic. [VERIFICATION] precedence test.

**Acceptance Criteria:**
- `models.py::CallerMetadata` exports suspect:bool, tier:str.
- Resolution precedence matches OQ-009 (lens-only vs caller-overridable).
- Manifest captures resolved CallerMetadata.
- Test fixture verifies precedence.

**Validation:**
- `uv run pytest tests/swarm/test_caller_metadata.py -v` passes.
- OQ-009 resolution recorded in docs.

**Dependencies:** T01.23, T02.04.

### T02.26 -- Add NFR-003 prompt-injection enforcement neutralization test

| Field | Value |
|---|---|
| Roadmap | R-057 (NFR-003) |
| Deliverables | D-0047 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | rf-qa (advisory) |
| Verification | tests + verify-sync |

**Deliverables:** 1. `tests/swarm/test_prompt_injection_neutralization.py`.

**Steps:** [EXECUTION] craft target containing end-marker `<<<END TARGET>>>` and assert it is neutralized (delimiters + substring guard prevent injection). [VERIFICATION] run.

**Acceptance Criteria:**
- Test fixture target contains `<<<END TARGET>>>` literal.
- Preflight neutralizes it (either escape or reject) — does NOT pass instruction-like content to dispatch.
- All 3 prompt paths exercised.
- Mutation: removing escape/reject logic fails the test.

**Validation:**
- `uv run pytest tests/swarm/test_prompt_injection_neutralization.py -v` passes.
- Dispatch mock confirms zero "instruction" data leakage.

**Dependencies:** T02.07.

### T02.27 -- Document NFR-012 lens-registry PR review discipline

| Field | Value |
|---|---|
| Roadmap | R-058 (NFR-012) |
| Deliverables | D-0048 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke (manual review) |

**Deliverables:** 1. `docs/dev/lens-contribution-policy.md`.

**Steps:** [EXECUTION] document 5 review criteria. [VERIFICATION] checklist render.

**Acceptance Criteria:**
- `docs/dev/lens-contribution-policy.md` exists.
- Covers real caller, §11.5 substring, normalizer-output-shape alignment, real downstream command, extra scrutiny for `suspect:true`.
- OQ-001 (pre-commit hook decision) recorded.
- Owners listed.

**Validation:**
- `grep -c "§11.5" docs/dev/lens-contribution-policy.md` ≥ 1.
- Doc review by `architect` + `security` recorded.

**Dependencies:** T02.16.

### T02.28 -- Add AC-013 no-Claude-Code-isms grep audit CI gate

| Field | Value |
|---|---|
| Roadmap | R-059 (AC-013) |
| Deliverables | D-0049 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests |

**Deliverables:** 1. `tests/swarm/test_no_claude_isms.py`.

**Steps:** [EXECUTION] grep forbidden tokens (`Task`, `WebFetch`, etc.) across job-spec/contract/CLI/monitoring surfaces. [VERIFICATION] CI green; mutation fails.

**Acceptance Criteria:**
- `tests/swarm/test_no_claude_isms.py` exists.
- Grep audit covers job spec, result contract, CLI surface, monitoring contract files.
- Zero Claude tool names found.
- Test fails on injection of a Claude-tool reference.

**Validation:**
- `uv run pytest tests/swarm/test_no_claude_isms.py -v` passes.
- Mutation: adding `WebFetch` to schema.py fails the test.

**Dependencies:** T02.01.

### T02.29 -- Checkpoint: Phase 2 end-of-phase (M2 exit gate)

| Field | Value |
|---|---|
| Type | CHECKPOINT (end-of-phase, mandatory) |
| Deliverables | D-CP2-1 |
| Tier | STRICT |

**Acceptance Criteria:**
- `phase-2-cp5.md` end-of-phase report with sign-off.
- `swarm validate` + `swarm validate-lenses` green on bundled registry.
- §11.5 enforced on all 3 paths; IMM-4 + INV-005/007 green.
- OQ-007 / OQ-008 / OQ-010 resolutions recorded.
- `make verify-sync` passes.

**Validation:**
- `grep -c "status: done"` ≥ 54.
- `superclaude swarm validate-lenses` exits 0.
- OQ resolutions logged in `docs/swarm/oq-resolutions.md`.

**Dependencies:** all prior Phase 2 tasks.
