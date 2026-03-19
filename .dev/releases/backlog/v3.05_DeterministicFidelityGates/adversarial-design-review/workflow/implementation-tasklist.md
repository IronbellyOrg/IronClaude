# Deterministic Fidelity Gate -- Implementation Tasklist

## Metadata
- **Source**: 7 adversarially-validated blocking finding resolutions (bf1-final.md through bf7-final.md)
- **Total tasks**: 24
- **Groups**: 6
- **Generated**: 2026-03-19

---

## Group 1: Foundation -- models.py (No Dependencies)

### Task 1.1: Add ACTIVE to VALID_FINDING_STATUSES
- **Source**: BF-1
- **File**: `src/superclaude/cli/roadmap/models.py`
- **Change**: Line 16 -- add `"ACTIVE"` to the `VALID_FINDING_STATUSES` frozenset so it becomes `frozenset({"PENDING", "ACTIVE", "FIXED", "FAILED", "SKIPPED"})`
- **Acceptance**: `Finding(... status="ACTIVE")` succeeds; `Finding(... status="INVALID")` still raises `ValueError`

### Task 1.2: Update Finding docstring lifecycle
- **Source**: BF-1
- **File**: `src/superclaude/cli/roadmap/models.py`
- **Change**: Line 27 -- update lifecycle comment from `PENDING -> FIXED | FAILED | SKIPPED` to `PENDING/ACTIVE -> FIXED | FAILED | SKIPPED`
- **Acceptance**: Docstring accurately reflects both valid initial statuses

### Task 1.3: Add source_layer field to Finding dataclass
- **Source**: BF-3
- **File**: `src/superclaude/cli/roadmap/models.py`
- **Change**: Add `source_layer: str = "structural"` field to `Finding`. Valid values: `"structural"`, `"semantic"`. Default `"structural"` for backward compatibility with pre-v3.05 registries
- **Acceptance**: `Finding(... source_layer="semantic")` succeeds; default is `"structural"`

### Task 1.4: Add convergence_enabled field to RoadmapConfig
- **Source**: BF-2
- **File**: `src/superclaude/cli/roadmap/models.py`
- **Change**: Add `convergence_enabled: bool = False` to `RoadmapConfig` dataclass
- **Acceptance**: `RoadmapConfig(... convergence_enabled=True)` succeeds; default is `False`

### Task 1.5: Add allow_regeneration field to RoadmapConfig
- **Source**: BF-5
- **File**: `src/superclaude/cli/roadmap/models.py`
- **Change**: Add `allow_regeneration: bool = False` to `RoadmapConfig` dataclass with comment `# FR-9: override diff-size guard`
- **Acceptance**: `RoadmapConfig(... allow_regeneration=True)` succeeds; default is `False`

---

## Group 2: Architecture Design Doc (No Code Dependencies)

### Task 2.1: Update Section 4.4 -- ACTIVE status clarification
- **Source**: BF-1
- **File**: `architecture-design.md` (Section 4.4, ~line 582)
- **Change**: Add clarifying note that both `ACTIVE` and `PENDING` are valid initial statuses. `ACTIVE` is used in the deviation registry; `PENDING` is the legacy pipeline default. Both represent "not yet resolved"
- **Acceptance**: Section 4.4 documents both statuses with rationale for the distinction

### Task 2.2: Update Section 5.1 -- Conditional step 8 construction
- **Source**: BF-2
- **File**: `architecture-design.md` (Section 5.1)
- **Change**: Replace step 8 code block with mode-dependent construction: convergence mode sets `gate=None` and `prompt=None`; legacy mode retains `SPEC_FIDELITY_GATE`
- **Acceptance**: Section 5.1 shows `if config.convergence_enabled` branching for step 8

### Task 2.3: Replace Section 5.3 -- Gate Authority Model
- **Source**: BF-2
- **File**: `architecture-design.md` (Section 5.3)
- **Change**: Replace entirely with Gate Authority Model text documenting mutual exclusion: convergence mode uses only DeviationRegistry; legacy mode uses only SPEC_FIDELITY_GATE. Include Design Principle #3 compliance statement
- **Acceptance**: Section 5.3 explicitly states the two authorities never coexist

### Task 2.4: Amend Design Principle #3
- **Source**: BF-2
- **File**: `architecture-design.md` (Section 1)
- **Change**: Append to Principle #3: "SPEC_FIDELITY_GATE is excluded from convergence mode to prevent dual-authority conflicts (see Sec 5.3)"
- **Acceptance**: Principle #3 references the exclusion and cross-references Section 5.3

### Task 2.5: Update Section 4.5 -- Split structural/semantic tracking
- **Source**: BF-3
- **File**: `architecture-design.md` (Section 4.5)
- **Change**: Update step 6 of convergence algorithm: monotonic progress check applies only to `structural_high_count`. Semantic increases logged as warnings, not regressions. Gate evaluation (step 5) still uses total active HIGHs
- **Acceptance**: Section 4.5 step 6 references `structural_high_count` for regression, total for gate

### Task 2.6: Update FR-7 and FR-8 acceptance criteria
- **Source**: BF-3
- **File**: `architecture-design.md` (FR-7, FR-8 sections)
- **Change**: FR-7: amend to `structural_high_count <= run_1.structural_high_count`. FR-8: amend regression trigger to `structural_high_count` only
- **Acceptance**: Both FRs reference structural counts explicitly

### Task 2.7: Replace Section 4.5.1 -- Temp directory isolation
- **Source**: BF-4
- **File**: `architecture-design.md` (Section 4.5.1)
- **Change**: Replace worktree management with temp directory management. Update FR-8 text from "git worktree" to "isolated temporary directory containing independent copies of all input files"
- **Acceptance**: No references to `git worktree` in convergence/regression sections

### Task 2.8: Update Section 4.6.2 -- allow_regeneration parameter
- **Source**: BF-5
- **File**: `architecture-design.md` (Section 4.6.2)
- **Change**: Add `allow_regeneration: bool = False` parameter to `apply_patches()` documentation. Update algorithm step 2.b.ii with conditional behavior based on flag
- **Acceptance**: Section 4.6.2 documents the flag and its effect on diff-threshold enforcement

### Task 2.9: Update Section 4.3 -- Debate protocol specification
- **Source**: BF-6
- **File**: `architecture-design.md` (Section 4.3)
- **Change**: Replace `validate_semantic_high()` docstring with full protocol specification: single-round prosecutor/defender, automated deterministic judge, rubric weights, verdict thresholds. Add constants: `PROSECUTOR_TEMPLATE`, `DEFENDER_TEMPLATE`, `RUBRIC_WEIGHTS`, `VERDICT_MARGIN_THRESHOLD`, `DEBATE_TOKEN_CAP`
- **Acceptance**: Section 4.3 contains complete debate protocol implementable without external references

### Task 2.10: Add Section 4.3.1 -- Prompt budget enforcement
- **Source**: BF-7
- **File**: `architecture-design.md` (new Section 4.3.1)
- **Change**: Add subsection documenting proportional budget allocation (60/20/15/5 split), truncation priority order, configurability, and section ordering within budget. Update NFR-3 row in Section 10 compliance matrix
- **Acceptance**: Section 4.3.1 exists with budget ratios, truncation rules, and markers

---

## Group 3: Convergence Engine (Depends on Group 1)

### Task 3.1: Add split structural/semantic HIGH tracking to registry
- **Source**: BF-3
- **File**: `src/superclaude/cli/roadmap/convergence.py` (new module per architecture Sec 4.5)
- **Change**: `DeviationRegistry.merge_findings()` tags each finding with `source_layer` based on origin (structural_checkers vs semantic_layer). Run metadata includes `structural_high_count`, `semantic_high_count`, and `total_high_count`
- **Acceptance**: Registry JSON contains `source_layer` on each finding and split counts per run

### Task 3.2: Implement structural-only monotonic enforcement
- **Source**: BF-3
- **File**: `src/superclaude/cli/roadmap/convergence.py`
- **Change**: In `execute_fidelity_with_convergence()` step 6: regression check uses `structural_high_count` only. Semantic increases emit warning log `"Semantic HIGH fluctuation: {prev} -> {curr} (delta: +{delta}). Not a regression."` but do not trigger FR-8 parallel validation
- **Acceptance**: Semantic count increase alone does not trigger `handle_regression()`; structural increase does

### Task 3.3: Replace worktree isolation with temp directories
- **Source**: BF-4
- **File**: `src/superclaude/cli/roadmap/convergence.py`
- **Change**: Implement `_create_validation_dirs(spec_path, roadmap_path, registry_path, count=3)` using `tempfile.mkdtemp` + `shutil.copy2`. Implement `_cleanup_validation_dirs(dirs)` with try/except per dir. Update `handle_regression()` to use temp dirs with try/finally cleanup. Register `atexit` fallback
- **Acceptance**: No git worktree calls; temp dirs created under system temp; cleanup guaranteed via finally block

### Task 3.4: Implement registry-only gate evaluation in convergence mode
- **Source**: BF-2
- **File**: `src/superclaude/cli/roadmap/executor.py`
- **Change**: In `_build_steps()`, replace unconditional step 8 construction with conditional: when `config.convergence_enabled`, set `gate=None` and `prompt=None`; otherwise use `SPEC_FIDELITY_GATE`. In step runner, when `step.prompt is None` and `step.gate is None`, delegate to convergence engine
- **Acceptance**: With `convergence_enabled=True`, SPEC_FIDELITY_GATE is never invoked; with `False`, behavior is byte-identical to pre-v3.05

---

## Group 4: Semantic Layer / Debate (Depends on Group 3)

### Task 4.1: Implement lightweight debate protocol
- **Source**: BF-6
- **File**: `src/superclaude/cli/roadmap/semantic_layer.py` (new module per architecture Sec 4.3)
- **Change**: Implement `validate_semantic_high()` with: (1) prosecutor/defender prompt construction from templates, (2) parallel ClaudeProcess execution, (3) YAML response parsing, (4) `score_argument()` deterministic rubric scoring, (5) `judge_verdict()` with 0.15 margin threshold and conservative tiebreak, (6) debate output YAML writing. Add `RubricScores` dataclass with weighted property. Handle YAML parse failures (score 0 for that side)
- **Acceptance**: Known-HIGH finding returns CONFIRM_HIGH; rubric scores are deterministic for fixed inputs; tiebreak always favors CONFIRM_HIGH

### Task 4.2: Implement prompt budget enforcement
- **Source**: BF-7
- **File**: `src/superclaude/cli/roadmap/semantic_layer.py`
- **Change**: Implement `build_semantic_prompt()` with proportional budget allocation (60% spec/roadmap, 20% structural context, 15% prior summary, 5% template). Tail-truncation on line boundaries with `[TRUNCATED: N bytes omitted]` markers. `MAX_PROMPT_BYTES = 30_720` as module constant. Assert final prompt <= budget before return. ValueError if template exceeds 5% allocation
- **Acceptance**: Prompt with 25KB section is truncated to <= 30,720 bytes; truncation marker is present; empty sections produce valid prompt

### Task 4.3: Wire debate verdicts into registry
- **Source**: BF-6
- **File**: `src/superclaude/cli/roadmap/semantic_layer.py`
- **Change**: In `run_semantic_layer()`, after `validate_semantic_high()` returns, call `registry.record_debate_verdict(finding.stable_id, verdict, transcript_path)`. If verdict starts with `DOWNGRADE_TO_`, update `finding.severity` to the new level
- **Acceptance**: After debate, registry finding has `debate_verdict` and `debate_transcript` fields populated; downgraded findings have updated severity

---

## Group 5: Remediation Changes (Depends on Group 1)

### Task 5.1: Add --allow-regeneration CLI flag
- **Source**: BF-5
- **File**: `src/superclaude/cli/roadmap/commands.py`
- **Change**: Add `@click.option("--allow-regeneration", is_flag=True, help="Allow patches that exceed the diff-size threshold...")` to the `run` command. Add `allow_regeneration: bool` parameter to `run()` function. Pass through to `config_kwargs`
- **Acceptance**: `superclaude roadmap run spec.md --allow-regeneration` parses; config has `allow_regeneration=True`

### Task 5.2: Implement diff-size guard with override logic
- **Source**: BF-5
- **File**: `src/superclaude/cli/roadmap/remediate_executor.py`
- **Change**: In `apply_patches()`, add `allow_regeneration: bool = False` parameter. When `ratio > diff_threshold`: if `allow_regeneration=True`, log WARNING and proceed; if `False` (default), reject patch and mark finding FAILED in registry. Caller in convergence.py passes `config.allow_regeneration`
- **Acceptance**: Without flag, patches >30% are rejected (FAILED); with flag, patches >30% are applied with WARNING log

---

## Group 6: Integration Tests (Depends on All Above)

### Task 6.1: BF-1 validation -- ACTIVE status tests
- **Source**: BF-1
- **File**: `tests/roadmap/test_models.py`
- **Change**: Add `test_finding_active_status_valid()` confirming `Finding(... status="ACTIVE")` succeeds. Verify PENDING still works. Verify INVALID still raises ValueError
- **Acceptance**: All three assertions pass

### Task 6.2: BF-2 validation -- Dual authority elimination tests
- **Source**: BF-2
- **File**: `tests/roadmap/test_convergence.py` (new)
- **Change**: V1: convergence mode constructs step 8 with `gate=None`. V2: legacy mode uses `SPEC_FIDELITY_GATE`. V3: registry with 0 active HIGHs passes in convergence mode. V4: grep convergence.py for SPEC_FIDELITY_GATE references (expect 0). V5: legacy mode output matches pre-v3.05 baseline
- **Acceptance**: All 5 validation scenarios pass

### Task 6.3: BF-3 validation -- Split tracking and regression tests
- **Source**: BF-3
- **File**: `tests/roadmap/test_convergence.py`
- **Change**: (1) Structural regression triggers `handle_regression()`. (2) Semantic fluctuation does NOT trigger regression, emits warning. (3) Gate requires 0 total HIGHs (semantic HIGHs block gate). (4) Integration: identical inputs with semantic variation, no regression triggered. (5) Property: all structural findings have `source_layer="structural"`, all semantic have `"semantic"`
- **Acceptance**: All 5 test scenarios pass

### Task 6.4: BF-4 validation -- Temp directory isolation tests
- **Source**: BF-4
- **File**: `tests/roadmap/test_convergence.py`
- **Change**: (1) File independence: mutate file in dir-0, dirs 1-2 unaffected. (2) Cleanup removes all dirs. (3) Parallel execution: 3 checkers produce identical findings. (4) No worktree artifacts after `handle_regression()`
- **Acceptance**: All 4 test scenarios pass

### Task 6.5: BF-5 validation -- Allow-regeneration tests
- **Source**: BF-5
- **File**: `tests/roadmap/test_remediation.py` (new)
- **Change**: (1) Default rejects patches >30% threshold. (2) Flag allows override with WARNING log. (3) CLI wiring: `--allow-regeneration` sets config correctly. (4) Safety: existing tests pass without flag
- **Acceptance**: All 4 test scenarios pass

### Task 6.6: BF-6 validation -- Debate protocol tests
- **Source**: BF-6
- **File**: `tests/roadmap/test_semantic_layer.py` (new)
- **Change**: Unit: rubric scoring determinism, verdict threshold boundaries (0.14/0.15/0.16 margins), YAML parse failure handling, token budget enforcement. Integration: known-HIGH returns CONFIRM_HIGH, known-MEDIUM downgrades, registry updated after debate, parallel debates no corruption. Property: tiebreak always CONFIRM_HIGH, weighted score in [0.0, 1.0], verdict determinism
- **Acceptance**: All unit, integration, and property tests pass

### Task 6.7: BF-7 validation -- Prompt budget tests
- **Source**: BF-7
- **File**: `tests/roadmap/test_semantic_layer.py`
- **Change**: (1) Normal case: all components fit. (2) Oversized section truncated with marker. (3) Truncation on line boundary. (4) Empty sections produce valid prompt. (5) Bloated template raises ValueError. (6) Structural findings truncated at finding boundary. (7) Integration: no prompt exceeds 30KB in full semantic layer run
- **Acceptance**: All 7 test scenarios pass

---

## Dependency Graph

```
Group 1: models.py
  |
  +---> Group 3: convergence.py + executor.py
  |       |
  |       +---> Group 4: semantic_layer.py (debate + budget)
  |
  +---> Group 5: remediate_executor.py + commands.py
  |
  v
Group 2: architecture-design.md (parallel with Groups 1, 3-5)
  |
  v
Group 6: Integration tests (depends on ALL above)

Execution order:
  [Group 1] --+--> [Group 3] --> [Group 4]
              |
              +--> [Group 5]
              |
  [Group 2] --+  (can run in parallel with any code group)
              |
              +--> [Group 6] (after all code groups complete)
```

---

## Implementation Notes

### Cross-cutting concerns

1. **Registry schema evolution**: BF-1 (ACTIVE status), BF-3 (source_layer field, split counts), and BF-6 (debate_verdict, debate_transcript) all modify the registry JSON schema. These changes are additive and non-conflicting, but the `DeviationRegistry` class must handle all three in a single coherent implementation.

2. **convergence.py is new**: Tasks 3.1-3.4 reference `convergence.py` which does not yet exist. It should be created as `src/superclaude/cli/roadmap/convergence.py` per architecture Section 4.5. All convergence-related logic (registry management, regression detection, gate evaluation) lives here.

3. **semantic_layer.py is new**: Tasks 4.1-4.3 reference `semantic_layer.py` which does not yet exist. It should be created as `src/superclaude/cli/roadmap/semantic_layer.py` per architecture Section 4.3.

4. **Backward compatibility**: All changes default to off (`convergence_enabled=False`, `allow_regeneration=False`, `source_layer="structural"`). Existing pipeline behavior is preserved byte-identical when new flags are not set.

5. **No changes to gates.py**: `SPEC_FIDELITY_GATE` remains defined in `gates.py` for legacy mode. It is never deleted, only conditionally bypassed.

### Ordering constraints

- Task 1.3 (source_layer field) MUST complete before Task 3.1 (merge_findings tagging), since the registry expects the field to exist on Finding objects.
- Task 1.4 (convergence_enabled) MUST complete before Task 3.4 (conditional step 8), since the executor reads this config field.
- Task 3.1/3.2 (split tracking) SHOULD complete before Task 4.1 (debate protocol), since the debate protocol writes `source_layer="semantic"` findings.
- Task 5.1 (CLI flag) and Task 5.2 (guard logic) can be done in either order but both are needed for the feature to work end-to-end.

### Warnings

- **Do not remove PENDING**: BF-1 resolution explicitly keeps PENDING as valid. Removing it would break all existing pipeline tests and serialized state.
- **Do not invoke SPEC_FIDELITY_GATE in convergence.py**: BF-2 resolution requires zero references to SPEC_FIDELITY_GATE in the convergence module. Grep verification is part of Task 6.2.
- **Temperature=0 is NOT the solution for BF-3**: The resolution explicitly rejected temperature pinning. Do not add temperature configuration to address semantic fluctuation.
