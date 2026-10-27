---
high_severity_count: 2
medium_severity_count: 5
low_severity_count: 3
total_deviations: 10
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **Severity**: HIGH
- **Deviation**: Spec defines 7 implementation phases; roadmap consolidates into 5 phases with different groupings
- **Spec Quote**: "### Downstream Inputs ... Milestones: 7 implementation phases (data models -> resolution -> discovery -> scoping -> CLI -> validation -> tests)" and "### 4.6 Implementation Order: 1. models.py ... 2. resolution.py ... 3. discover_components.py ... 4. process.py / validate_config.py ... 5. cli.py + config.py ... 6. Tests + fixtures"
- **Roadmap Quote**: "Phase 1: Data Model, Resolution Core & Algorithm ... Phase 2: Component Tree Discovery & Agent Extraction ... Phase 3: CLI Integration & Artifact Enrichment ... Phase 4: Subprocess Scoping & Directory Consolidation ... Phase 5: Integration Testing & Final Validation"
- **Impact**: Phase 1 merges models + resolution + validation config work. Phase 3 merges CLI + config + artifact enrichment. Phase 5 is testing-only. The spec's `validate_config.py` modifications (checks 5-6, error codes, `to_dict()`) are split across Phases 1, 3, and 5 without clear ownership. The spec explicitly states models and resolution can be parallel ("Phases 1-2 can run in parallel") but the roadmap merges them into a single serial phase, eliminating that parallelization opportunity.
- **Recommended Correction**: Either align to the spec's 7-phase structure or explicitly map each spec phase to the roadmap phase that covers it, with a traceability table. Ensure `validate_config.py` work (new error codes, checks 5-6, `to_dict()` update) has a single owning phase.

### DEV-002
- **Severity**: HIGH
- **Deviation**: Roadmap omits `config.py` modifications entirely
- **Spec Quote**: "### 4.2 Modified Files ... | `config.py` | Update `load_portify_config()` to accept and pass through new parameters (+15-25 lines) | Propagate new CLI options to config |"
- **Roadmap Quote**: Phase 3 tasks mention "Wire resolution and discovery into the CLI" but `config.py` is not listed in any phase's task breakdown. Phase 3 title mentions "CLI Integration" and tasks reference `cli.py` but not `config.py`.
- **Impact**: Without `config.py` updates, new CLI options (`--commands-dir`, `--skills-dir`, `--agents-dir`, `--include-agent`, `--save-manifest`) cannot propagate through `load_portify_config()` to `PortifyConfig`. This is a functional gap that would cause new CLI options to be silently ignored.
- **Recommended Correction**: Add explicit `config.py` task to Phase 3: "Update `load_portify_config()` to accept and pass through `commands_dir`, `skills_dir`, `agents_dir`, `include_agents`, `save_manifest_path` parameters."

### DEV-003
- **Severity**: MEDIUM
- **Deviation**: Roadmap introduces 12 "Success Criteria" (SC-1 through SC-12) not defined in the spec
- **Spec Quote**: The spec defines acceptance criteria per FR (FR-PORTIFY-WORKFLOW.1, .2, .3) with checkbox items and NFRs (NFR-WORKFLOW.1 through .5). No "SC-NNN" identifiers exist.
- **Roadmap Quote**: "SC-1 | Dry-run enriched inventory ... SC-2 | Skill-dir backward compat ... SC-3 | 6 input forms resolve <1s ... SC-12 | Dir consolidation at >10"
- **Impact**: The SC criteria are reasonable derivations from spec requirements but introduce a new numbering scheme without explicit mapping to spec FRs/NFRs. SC-11 ("to_dict() new fields") maps to spec's `ValidateConfigResult.to_dict()` requirement but this mapping is implicit. Traceability between spec acceptance criteria and roadmap success criteria is unclear.
- **Recommended Correction**: Add a traceability table mapping each SC to its source FR/NFR acceptance criterion. Example: SC-3 → NFR-WORKFLOW.1, SC-9 → NFR-WORKFLOW.2.

### DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap introduces 7 "Open Questions" (OQ-1 through OQ-7) where spec has only 4 "Open Items" (OI-1 through OI-4)
- **Spec Quote**: "## 11. Open Items: OI-1 (recursive agent refs), OI-2 (manifest loading), OI-3 (--exclude-component), OI-4 (quality scores — RESOLVED)"
- **Roadmap Quote**: "OQ-1 (recursive agent resolution), OQ-2 (manifest load), OQ-3 (--exclude-component), OQ-4 (multi-skill commands), OQ-5 (agent regex completeness), OQ-6 (naming convention deviations), OQ-7 (to_dict() downstream consumers)"
- **Impact**: OQ-4 through OQ-7 are additions not in the spec. While they are reasonable concerns extracted from spec risk assessment and edge cases, they should be explicitly noted as roadmap-originated rather than spec-required deferrals. OI-4 (quality scores, resolved) is dropped without acknowledgment.
- **Recommended Correction**: Note OQ-4 through OQ-7 as "roadmap-identified" open questions. Acknowledge OI-4 as resolved per spec.

### DEV-005
- **Severity**: MEDIUM
- **Deviation**: Spec's `TargetInputType` enum has 5 values but spec section 4.5 describes 6 input forms
- **Spec Quote**: Enum: "COMMAND_NAME, COMMAND_PATH, SKILL_DIR, SKILL_NAME, SKILL_FILE" (5 values). Input Acceptance Matrix: "Bare command name, Command name with prefix, Command file path, Skill directory path, Skill directory name, SKILL.md path" (6 forms).
- **Roadmap Quote**: "accept 6 input forms (bare command name, prefixed name, command path, skill directory, skill name, SKILL.md path)"
- **Impact**: The roadmap correctly references 6 input forms but doesn't address that the "Command name with prefix" form (e.g., `sc:roadmap`) maps to the same `COMMAND_NAME` enum value after prefix stripping. This is a spec-internal inconsistency the roadmap inherits without clarifying.
- **Recommended Correction**: Roadmap should note that 6 input forms map to 5 `TargetInputType` enum values, with `sc:` prefix stripping as a pre-classification normalization step.

### DEV-006
- **Severity**: MEDIUM
- **Deviation**: `derive_cli_name()` enhancement placed in Phase 2 but spec associates it with `models.py` (Phase 1 territory)
- **Spec Quote**: "### 4.5 Data Models ... #### PortifyConfig Extensions (models.py) ... The `derive_cli_name()` method is augmented to prefer the command name when available"
- **Roadmap Quote**: "Phase 2 ... FR-PORTIFY-WORKFLOW.2i — `derive_cli_name()` enhancement: prefer `command_path.stem` when available"
- **Impact**: Minor sequencing inconsistency. The method lives in `models.py` which is modified in Phase 1, but the enhancement is deferred to Phase 2 where it depends on resolved `command_path`. Functionally correct since Phase 2 depends on Phase 1, but the FR numbering (2i) suggests it's a discovery concern when it's really a model concern enabled by resolution.
- **Recommended Correction**: Either move to Phase 1 (since it modifies `models.py`) or explicitly note it's deferred to Phase 2 because it depends on `command_path` being populated by resolution.

### DEV-007
- **Severity**: MEDIUM
- **Deviation**: Roadmap test count breakdown doesn't match spec's test plan
- **Spec Quote**: "### 8.1 Unit Tests" lists 25 unit tests. "### 8.2 Integration Tests" lists 3. "Total estimated new tests: ~37"
- **Roadmap Quote**: "Tests (~15)" in Phase 1, "Tests (~12)" in Phase 2, "Tests (~5)" in Phase 3, "Tests (~5)" in Phase 4 = ~37 total
- **Impact**: The per-phase allocation is reasonable but the spec's detailed test table assigns tests to specific files (`test_resolution.py`, `test_models.py`, `test_validate_config.py`, `test_process.py`). The roadmap doesn't map its per-phase test counts to these file assignments, making it unclear which specific tests from the spec's test plan land in which phase.
- **Recommended Correction**: Add test file mapping per phase, e.g., Phase 1: `test_resolution.py` (input forms), `test_models.py` (dataclasses); Phase 2: `test_resolution.py` (agent extraction), `test_models.py` (tree methods).

### DEV-008
- **Severity**: LOW
- **Deviation**: Spec defines effort in hours; roadmap uses days
- **Spec Quote**: "Phase 1: 2-3 hours ... Phase 7: 5-7 hours ... Total: 19-28 hours ... Estimated sessions: 2-3 focused implementation sessions"
- **Roadmap Quote**: "Phase 1: 2-3 days ... Total: 7-9 working days for a single developer"
- **Impact**: The roadmap's day-based estimates are significantly larger than the spec's hour-based estimates (7-9 days vs ~3-4 days at 8hr/day). This may reflect different assumptions about session productivity but the mismatch could cause planning confusion.
- **Recommended Correction**: Reconcile units. If roadmap days assume partial-day focus, note the assumption explicitly.

### DEV-009
- **Severity**: LOW
- **Deviation**: Roadmap relabels spec's "Tier 2" terminology
- **Spec Quote**: "Tier 2 | Refs, rules, templates, scripts — step-specific detail loaded on-demand"
- **Roadmap Quote**: "## Tier 2: Agents" in manifest output description; refs/rules/templates/scripts listed separately without tier label
- **Impact**: The spec uses "Tier 2" for refs/rules/templates/scripts and treats agents as a separate category. The roadmap's `to_manifest_markdown()` labels agents as "Tier 2" which contradicts the spec's glossary. However, this is inherited from the spec's own `to_manifest_markdown()` code which also uses "## Tier 2: Agents", so this is a spec-internal inconsistency the roadmap faithfully reproduces.
- **Recommended Correction**: No roadmap change needed; note the spec-internal inconsistency for future cleanup.

### DEV-010
- **Severity**: LOW
- **Deviation**: Roadmap's resource requirements section adds "Architect/reviewer" role not in spec
- **Spec Quote**: No resource roles defined in spec beyond effort estimates in Appendix C.
- **Roadmap Quote**: "3. Architect/reviewer — Verifies boundary discipline, compatibility posture, and downstream contract safety."
- **Impact**: Additive information. Does not contradict spec but introduces a resource requirement the spec doesn't mandate.
- **Recommended Correction**: None required; this is reasonable roadmap-level planning detail.

## Summary

**Distribution**: 2 HIGH, 5 MEDIUM, 3 LOW

The two HIGH-severity deviations are:
1. **Phase structure mismatch** — The spec defines 7 phases; the roadmap consolidates to 5 with different groupings, losing the spec's parallelization guidance and fragmenting `validate_config.py` ownership across multiple phases.
2. **Missing `config.py` coverage** — A required modified file is absent from all roadmap phase task lists, which would leave new CLI options unable to propagate to configuration.

The MEDIUM deviations are primarily traceability gaps (unmapped success criteria, test assignments, open question provenance) and minor sequencing inconsistencies. The LOW deviations are unit/terminology differences that don't affect correctness.

**Recommendation**: Resolve the two HIGH deviations before generating a tasklist. Add explicit `config.py` tasks and either align phase structure or provide a clear spec-phase-to-roadmap-phase mapping table.
