---
spec_source: "deterministic-fidelity-gate-requirements.md"
generated: "2026-03-20T00:00:00Z"
generator: "claude-opus-4-6-requirements-extractor"
functional_requirements: 12
nonfunctional_requirements: 7
total_requirements: 19
complexity_score: 0.88
complexity_class: HIGH
domains_detected: [backend, cli, testing, pipeline-orchestration, nlp-integration]
risks_identified: 6
dependencies_identified: 8
success_criteria_count: 6
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 162.0, started_at: "2026-03-20T13:40:48.373809+00:00", finished_at: "2026-03-20T13:43:30.398744+00:00"}
---

## Functional Requirements

### FR-1: Decomposed Structural Checkers (5 Dimensions)

**Description**: Replace monolithic LLM fidelity comparison with 5 independent, statically-typed checkers (Signatures, Data Models, Gates, CLI Options, NFRs). Each extracts structured data from spec and roadmap, compares deterministically, and produces typed findings with predetermined severity rules.

**Acceptance Criteria**:
- Each checker is an independent callable: `(spec_path, roadmap_path) → List[Finding]`
- Severity assigned by structural rules, not LLM prose
- Checkers run in parallel (no shared state)
- Each finding includes: dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location
- A checker registry maps dimension names to checker callables

**Dependencies**: FR-2, FR-3

---

### FR-2: Spec & Roadmap Parser

**Description**: Parser extracting structured data from spec template format (YAML frontmatter, markdown tables, fenced code blocks, heading hierarchy, requirement ID patterns) and roadmap markdown. New module: `spec_parser.py`.

**Acceptance Criteria**:
- Parses YAML frontmatter from both spec and roadmap
- Extracts markdown tables by section (keyed by heading path)
- Extracts fenced code blocks with language annotation
- Extracts requirement ID families via regex: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
- Extracts Python function signatures from fenced blocks
- Extracts file paths from manifest tables (Sec 4.1, 4.2, 4.3)
- Extracts `Literal[...]` enum values from code blocks
- Extracts numeric threshold expressions: `< 5s`, `>= 90%`, `minimum 20`
- Returns structured objects, not raw text
- Graceful degradation on malformed YAML frontmatter: partial parse + `ParseWarning`
- Graceful degradation on irregular markdown tables: best-effort + `ParseWarning`
- Graceful degradation on missing/wrong language tags: raw text + `ParseWarning`
- `ParseWarning` list collected per parse call, surfaced to caller
- Validated against real spec (`deterministic-fidelity-gate-requirements.md`)

**Critical Path Note**: FR-2 → FR-1 → FR-4 → FR-7. Parser failure cascades to all downstream FRs.

**Dependencies**: None (entry point for structural checker pipeline)

---

### FR-3: Anchored Severity Rules

**Description**: Each structural checker has a severity rule table mapping specific structural mismatch types to fixed severity levels. Severity is NOT LLM-judged for structural findings. 19 canonical rules across 5 dimensions.

**Acceptance Criteria**:
- Every structural checker has an explicit rule table
- Rules defined in code as `SEVERITY_RULES: dict[tuple[str, str], str]` keyed by `(dimension, mismatch_type) → severity`
- Machine keys used in code (e.g., `phantom_id`, `function_missing`)
- Same inputs always produce same severity — no randomness, no LLM
- Rule table extensible without changing checker logic
- Unknown `(dimension, mismatch_type)` combinations raise `KeyError`
- `SEVERITY_RULES` dict and `get_severity()` function are the canonical API
- Finding objects use machine keys in `mismatch_type` field

**Dependencies**: FR-1

---

### FR-4: Residual Semantic Layer with Adversarial Validation

**Description**: After structural checkers, a residual LLM pass handles ~30% of checks requiring semantic judgment. When semantic layer assigns HIGH, triggers lightweight adversarial debate. Extends existing `semantic_layer.py` (337 lines).

**Acceptance Criteria**:
- Semantic layer receives only dimensions/aspects not covered by structural checkers
- Uses chunked input (per-section, not full-document inline)
- When semantic HIGH: pipeline pauses, spawns adversarial debate
- Debate produces verdict: CONFIRM_HIGH, DOWNGRADE_TO_MEDIUM, or DOWNGRADE_TO_LOW
- Verdict recorded in deviation registry with debate transcript reference
- Semantic MEDIUM and LOW accepted without debate
- Prompt includes structural findings as context
- All semantic findings tagged with `source_layer="semantic"`

**Dependencies**: FR-1, FR-2, FR-5, FR-6

#### FR-4.1: Lightweight Debate Protocol

**Description**: Single-round prosecutor/defender model with deterministic automated judge for semantic HIGH validation.

**Acceptance Criteria**:
- `validate_semantic_high()` exists in `semantic_layer.py` implementing protocol steps 1-7
- Accepts `claude_process_factory` parameter for test injection
- Prosecutor and defender execute in parallel (2 LLM calls)
- Judge is deterministic Python — same scores always produce same verdict
- Conservative tiebreak: margin within ±0.15 → CONFIRM_HIGH
- 4-criterion rubric: Evidence Quality (30%), Impact Specificity (25%), Logical Coherence (25%), Concession Handling (20%)
- Debate output YAML written per finding with rubric scores, margin, verdict
- Registry updated with `debate_verdict` and `debate_transcript` reference
- Token budget: ~3,800 per finding (hard cap: 5,000)
- YAML parse failure: all rubric scores default to 0 for that side

**Dependencies**: FR-6 (registry)

#### FR-4.2: Prompt Budget Enforcement (NFR-3)

**Description**: Semantic layer enforces 30KB prompt limit via proportional budget allocation with tail-truncation.

**Acceptance Criteria**:
- Total budget: 30,720 bytes (60% spec/roadmap, 20% structural context, 15% prior summary, 5% template)
- Truncation markers include section heading: `[TRUNCATED: N bytes omitted from '<heading>']`
- Template exceeding 5% allocation raises `ValueError`
- Truncation priority: prior summary → structural context → spec/roadmap sections

**Dependencies**: FR-1, FR-6

---

### FR-5: Sectional/Chunked Comparison

**Description**: Replace full-document inline embedding with sectional comparison. Both spec and roadmap split by top-level sections. Each checker operates on relevant sections only.

**Acceptance Criteria**:
- `SpecSection` dataclass with fields: heading, heading_path, level, content, start_line, end_line
- `split_into_sections(content: str) -> list[SpecSection]` in `spec_parser.py`
- Split on `^#{1,6} ` heading lines; nested sections are children
- YAML frontmatter as special section (level=0, heading="frontmatter")
- Content before first heading as preamble section (level=0)
- Each checker receives only relevant sections per dimension-to-section mapping
- Supplementary sections included when reference graph detects cross-references
- No single prompt contains both full documents inline
- Prompt size per checker call bounded (default ~30KB)
- Section mapping deterministic: dimension → spec sections → roadmap sections
- `SpecSection.heading` propagated to truncation markers

**Dependencies**: FR-2

---

### FR-6: Deviation Registry

**Description**: Persistent, file-backed JSON registry of all findings across runs within a release. Located in `convergence.py` (existing class, lines 50-225). Resets on spec version change.

**Acceptance Criteria**:
- Registry is JSON file in release output directory
- Each finding has stable ID from (dimension, rule_id, spec_location, mismatch_type)
- Each finding has `source_layer` field: `"structural"` or `"semantic"`
- New runs compare current findings against registry; existing matched by stable ID
- Fixed findings marked FIXED when no longer reproduced
- Run metadata includes: run_number, timestamp, spec_hash, roadmap_hash, structural_high_count, semantic_high_count, total_high_count
- Gate reads registry for pass/fail — not raw fidelity report
- Registry resets when `spec_hash` changes
- `ACTIVE` accepted as valid status alongside `PENDING`
- Pre-v3.05 registries default missing `source_layer` to `"structural"`
- Run metadata uses typed `RunMetadata` dataclass
- Finding dataclass extended with `rule_id`, `spec_quote`, `roadmap_quote` fields (all defaulted for backward compat)

**Dependencies**: FR-1

---

### FR-7: Convergence Gate

**Description**: Extends existing `convergence.py` with `execute_fidelity_with_convergence()` and `handle_regression()`. Evaluates convergence via registry state with TurnLedger-backed budget accounting.

**Acceptance Criteria**:
- Gate reads deviation registry, not raw fidelity output
- Pass requires: `active_high_count == 0` (structural + semantic)
- Monotonic progress check uses `structural_high_count` only
- Semantic HIGH increases logged as warnings, not regressions
- Run 2 must have `structural_high_count <= run_1.structural_high_count` or trigger FR-8
- Run 3 is final: pass or halt with full report
- Budget exhaustion without convergence: halt, diagnostic report, exit non-zero
- In convergence mode, `SPEC_FIDELITY_GATE` never invoked
- In legacy mode, behavior byte-identical to pre-v3.05
- `convergence_enabled: bool = False` default preserves legacy behavior
- Convergence loop executes within step 8 boundary
- Steps 1-7 and step 9 unaffected
- `execute_fidelity_with_convergence()` calls `execute_remediation()` between runs
- `_check_remediation_budget()` and `_print_terminal_halt()` NOT invoked in convergence mode
- Legacy and convergence budgets never overlap
- `ledger: TurnLedger` is required positional parameter — engine does not construct its own
- `run_checkers`, `run_remediation`, `handle_regression_fn` are keyword-only optional callable overrides
- Pipeline executor constructs `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` when convergence enabled
- Legacy mode never constructs a TurnLedger
- `CHECKER_COST` debited before each checker suite run
- `REMEDIATION_COST` debited before each remediation cycle
- `can_launch()` and `can_remediate()` guards checked before operations
- Early convergence pass credits `CONVERGENCE_PASS_CREDIT`
- Forward progress credits via `reimburse_for_progress()` using `ledger.reimbursement_rate`
- Cost constants module-level in `convergence.py` and overridable
- TurnLedger imported from `superclaude.cli.sprint.models`
- Pipeline executor dispatch constructs TurnLedger only when `convergence_enabled=true`
- Legacy branch does not import or reference TurnLedger
- Convergence result mapped to `StepResult` for pipeline compatibility

**Budget Constants**: CHECKER_COST=10, REMEDIATION_COST=8, REGRESSION_VALIDATION_COST=15, CONVERGENCE_PASS_CREDIT=5. MIN_CONVERGENCE_BUDGET=28, STD_CONVERGENCE_BUDGET=46, MAX_CONVERGENCE_BUDGET=61.

**Reimbursement**:
- `reimburse_for_progress()` uses `ledger.reimbursement_rate`, never hardcoded
- Returns 0 when `curr_structural_highs >= prev_structural_highs`
- Calls `ledger.credit()` only when credit > 0
- Progress credit events logged with format: `"Run {n}: progress credit {credit} turns (structural {prev} -> {curr})"`

**Dependencies**: FR-6, FR-7.1, FR-8

#### FR-7.1: FR-7/FR-8 Interface Contract

**Description**: Calling convention between convergence gate (FR-7) and regression detection (FR-8).

**Acceptance Criteria**:
- `handle_regression()` callable with documented signature returning `RegressionResult`
- `RegressionResult` dataclass with: validated_findings, debate_verdicts, agents_succeeded, consolidated_report_path
- Regression validation + remediation counts as one budget unit
- FR-7 does not spawn agents directly (delegated to FR-8)
- FR-8 does not evaluate convergence (delegated to FR-7)
- `ledger.debit(REGRESSION_VALIDATION_COST)` called before `handle_regression()`
- `handle_regression()` does not perform any ledger operations internally
- No separate `REMEDIATION_COST` debit for post-regression remediation (subsumed)

**Dependencies**: FR-7, FR-8, FR-6

---

### FR-8: Regression Detection & Parallel Validation

**Description**: When structural HIGHs regress, spawn 3 parallel validation agents in isolated temp directories. Each independently re-runs fidelity check. Findings merged, deduplicated, severity validated via adversarial debate.

**Acceptance Criteria**:
- Regression detected when `current_run.structural_high_count > previous_run.structural_high_count`
- Semantic HIGH increases alone do NOT trigger regression
- 3 agents spawned in parallel in isolated temp directories with independent file copies
- Each agent runs full checker suite independently
- Results merged by stable ID across all 3 agents
- Unique findings preserved; consolidated report written to `fidelity-regression-validation.md`
- Findings sorted by severity (HIGH → MEDIUM → LOW)
- Adversarial debate validates severity of each HIGH after consolidation
- Debate verdicts update deviation registry
- Entire flow counts as one "run" toward budget
- All 3 agents must succeed; any failure → entire validation marked FAILED, run not counted
- Cleanup guaranteed via try/finally; atexit fallback registered
- No git worktree calls; no `.git/worktrees/` artifacts

**Dependencies**: FR-1, FR-4, FR-6, FR-7

---

### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Extends existing `remediate_executor.py` (563 lines) to produce structured patches in MorphLLM-compatible JSON format. Engine-agnostic: ClaudeProcess primary, deterministic fallback, future MorphLLM swap.

**Acceptance Criteria**:
- Remediation agents output structured lazy edit snippets (MorphLLM-compatible JSON)
- Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- `RemediationPatch` dataclass defined with typed fields
- ClaudeProcess primary applicator; `fallback_apply()` for deterministic text replacement (min anchor: 5 lines or 200 chars)
- `check_morphllm_available()` probes MCP runtime for future migration
- Per-patch diff-size guard: reject if `changed_lines / patch_original_lines > 30%`
- `_check_diff_size()` retired; replaced by per-patch evaluation
- Partial rejection: valid patches applied even when others for same file rejected
- Rejected patches logged with reason; finding status set to FAILED
- Valid patches for same file applied sequentially
- Full regeneration only with `--allow-regeneration` flag
- Per-file rollback: each file evaluated independently
- Post-execution coherence check across cross-file findings
- Existing snapshot/restore mechanism retained
- `_DIFF_SIZE_THRESHOLD_PCT` changed from 50 to 30

**Dependencies**: FR-6

#### FR-9.1: `--allow-regeneration` Flag

**Acceptance Criteria**:
- `--allow-regeneration` is Click `is_flag=True` option on `run` command
- `allow_regeneration: bool = False` on `RoadmapConfig`
- Without flag: patches exceeding 30% rejected (FAILED)
- With flag: patches exceeding 30% applied with WARNING log
- WARNING log includes patch ID, actual ratio, threshold
- Existing behavior preserved when flag not passed

---

### FR-10: Run-to-Run Memory

**Description**: Each fidelity run has access to prior run findings and outcomes via the deviation registry. Semantic layer prompt includes prior findings summary.

**Acceptance Criteria**:
- Semantic layer prompt includes prior findings summary (ID, severity, status, run_number)
- Structural checkers have implicit memory via registry diff
- Registry tracks `first_seen_run` and `last_seen_run` per finding
- Fixed findings from prior runs not re-reported as new
- Summary bounded: max 50 prior findings in prompt, oldest-first truncated
- Run metadata includes ledger snapshot (`budget_consumed`, `budget_reimbursed`, `budget_available`) in convergence mode
- Progress proof logging includes budget state
- Progress credit events logged with specified format

**Dependencies**: FR-4, FR-6

---

## Non-Functional Requirements

### NFR-1: Determinism
Same inputs → identical structural findings. Verified by running twice on same inputs and diffing output.

### NFR-2: Convergence
≤3 runs to pass or halt. Measured by run counter in registry.

### NFR-3: Prompt Size
No single prompt exceeds 30KB. Enforced by proportional budget allocation in `build_semantic_prompt`, tail-truncation with `[TRUNCATED]` markers, `assert` before LLM call (see FR-4.2).

### NFR-4: Checker Independence
Checkers share no mutable state. Verified by code review and parallel execution test.

### NFR-5: Edit Safety
No file changes >30% without user consent (`--allow-regeneration`). Measured by diff-size guard metric.

### NFR-6: Traceability
Every finding traceable to rule_id or debate verdict. Verified by audit log review.

### NFR-7: Backward Compatibility
Existing pipeline steps (1-7) unchanged. Verified by integration test. Legacy mode behavior byte-identical to pre-v3.05.

---

## Complexity Assessment

**Score**: 0.88 / 1.0
**Class**: HIGH

**Rationale**:
- **Architectural breadth** (0.9): 10+ files modified/created across 3 module boundaries (roadmap, sprint, pipeline). Cross-module import with migration plan.
- **Concurrency** (0.85): Parallel structural checkers, parallel debate agents (prosecutor/defender), 3 parallel regression validation agents with temp dir isolation.
- **State management** (0.9): Persistent deviation registry with cross-run memory, TurnLedger budget accounting with reimbursement, dual budget system (legacy/convergence) with mutual exclusion.
- **Integration surface** (0.85): Must preserve byte-identical legacy behavior, coexist with spec_patch.py, interface with pipeline executor step ordering, and maintain backward compatibility for serialized registries.
- **Domain complexity** (0.85): Deterministic/semantic hybrid with adversarial validation, convergence loop with monotonic progress enforcement, structured patch generation with multi-engine applicator strategy.
- **Pre-existing code interaction** (0.9): ~60% infrastructure pre-built in v3.0; must extend without breaking. 19 pre-satisfied acceptance criteria that need verification, not reimplementation.

---

## Architectural Constraints

1. **UV-only Python environment**: All execution via `uv run`. No bare `python -m` or `pip`.
2. **Source of truth**: `src/superclaude/` is canonical; `.claude/` is dev copy synced via `make sync-dev`.
3. **Module disposition**: Specific files designated CREATE, MODIFY, DELETE, or CONSUME per frontmatter `module_disposition`.
4. **Cross-module import boundary**: `convergence.py` imports `TurnLedger` from `sprint/models.py` conditionally (convergence mode only). Migration to `pipeline/models.py` is future scope.
5. **Mutual exclusion**: Convergence mode and legacy mode are dispatched by single `convergence_enabled` boolean. Both budget systems must never run simultaneously.
6. **Pipeline step boundary**: Convergence engine operates within step 8 only. Steps 1-7 and step 9 are unaffected.
7. **Gate authority**: In convergence mode, only `DeviationRegistry` is authoritative. `SPEC_FIDELITY_GATE` is excluded. In legacy mode, only `SPEC_FIDELITY_GATE` is used.
8. **Baseline commit**: `f4d9035` — all pre-existing code references verified against this commit.
9. **No TurnLedger modifications**: Consumed as-is from `sprint/models.py`.
10. **Feature branch workflow**: Never commit directly to master/main.
11. **Backward compatibility default**: `convergence_enabled: bool = False` — all new behavior gated behind opt-in flag.
12. **Dead code removal**: `fidelity.py` (66 lines, zero imports) must be deleted.

---

## Risk Inventory

1. **Spec parser robustness** — Severity: HIGH — Real specs may deviate from template format. FR-2 is critical path entry point; parser failure cascades to all downstream FRs. *Mitigation*: Graceful degradation with `ParseWarning`, validation against real spec, not just synthetic fixtures.

2. **Stable finding ID collisions** — Severity: MEDIUM — Hash collisions or overly-specific IDs could cause false "new" findings, undermining convergence memory. *Mitigation*: `compute_stable_id()` uses (dimension, rule_id, spec_location, mismatch_type) tuple; test with real-world deviation sets.

3. **Temp directory cleanup leaks** — Severity: MEDIUM — Failed cleanup could leave orphaned directories consuming disk. *Mitigation*: Dual cleanup (try/finally + atexit handler); prefix-based identification for manual cleanup.

4. **Debate rubric calibration** — Severity: MEDIUM — Heuristic scoring thresholds (0.15 margin) may need tuning on real findings. Conservative tiebreak (CONFIRM_HIGH) limits downside. *Mitigation*: Conservative defaults; constants are tunable; log all rubric scores for post-hoc analysis.

5. **Dual budget system overlap** — Severity: HIGH — If `convergence_enabled` dispatch fails, both TurnLedger and legacy budget could run simultaneously, causing double-charging. *Mitigation*: Single dispatch point via `convergence_enabled`; integration test verifying mutual exclusion.

6. **Cross-module import fragility** — Severity: LOW — `convergence.py` → `sprint/models.py` import could break if TurnLedger moves. *Mitigation*: Conditional import (convergence mode only); one-line fix on migration; tracked in handoff notes.

---

## Dependency Inventory

1. **TurnLedger** (`superclaude.cli.sprint.models`) — Pure data class for budget accounting. Consumed as-is; not modified. Methods used: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`.

2. **DeviationRegistry** (`convergence.py:50-225`) — Pre-existing v3.0 class. Extended with source_layer tracking and split HIGH counts.

3. **ClaudeProcess** — Established pipeline execution engine for LLM subprocess calls. Used by FR-4.1 (debate agents), FR-8 (parallel validation agents), FR-9 (patch application).

4. **RoadmapConfig** (`models.py`) — Pre-existing config with `convergence_enabled` and `allow_regeneration` fields already present.

5. **Finding dataclass** (`models.py`) — Extended with `rule_id`, `spec_quote`, `roadmap_quote` fields.

6. **MorphLLM MCP** (`morphllm-fast-apply`) — Future dependency. `check_morphllm_available()` probes runtime; not required for v3.05.

7. **Click CLI framework** — `--allow-regeneration` flag added to `run` command.

8. **YAML parser** — For frontmatter extraction in spec_parser.py and debate output serialization.

---

## Success Criteria

1. **SC-1: Deterministic structural findings** — Run the same spec+roadmap pair through the fidelity gate twice; structural findings must be byte-identical. Zero diff on output.

2. **SC-2: Convergence within budget** — Pipeline terminates within ≤3 runs or halts with diagnostic report. No infinite loops. TurnLedger budget never goes negative without a halt.

3. **SC-3: Edit preservation** — After remediation, no previously-fixed finding re-appears as ACTIVE. Registry `FIXED` findings remain FIXED unless spec changes.

4. **SC-4: Severity anchoring** — ≥70% of findings have severity determined by structural rules (machine keys from FR-3 table). Semantic HIGHs validated by debate before pipeline acts.

5. **SC-5: Legacy backward compatibility** — With `convergence_enabled=false`, pipeline behavior is byte-identical to pre-v3.05 (commit `f4d9035`). No regressions in steps 1-7 or step 9.

6. **SC-6: Prompt size compliance** — No semantic layer prompt exceeds 30,720 bytes. Assert fires before any LLM call if exceeded.

---

## Open Questions

1. **Rubric threshold calibration**: The 0.15 margin threshold for debate verdicts is a heuristic. Should this be validated against a corpus of real semantic findings before shipping, or is the conservative tiebreak (CONFIRM_HIGH) sufficient as a safety net?

2. **TurnLedger cost constant values**: CHECKER_COST=10, REMEDIATION_COST=8, etc. are "recommended defaults" per spec. What is the calibration strategy? Are these based on empirical measurement or estimates? The spec notes they "may need recalibration based on real-world convergence behavior."

3. **ParseWarning severity**: FR-2 specifies graceful degradation with `ParseWarning`, but does not define whether parse warnings should block the pipeline, be logged-and-continued, or have their own severity classification.

4. **Pre-v3.05 registry migration**: When a pre-v3.05 registry (without `source_layer`) is loaded, all findings default to `"structural"`. If some were actually semantic, this could cause incorrect monotonic progress tracking. Is this acceptable for the migration path?

5. **Agent failure in regression validation**: FR-8 states "All 3 agents must succeed" — but what constitutes agent "failure"? Timeout? Parse error? Non-zero exit? The failure criteria are not specified.

6. **Cross-file coherence check scope**: FR-9 mentions post-execution coherence check for cross-file findings, but does not specify the coherence evaluation criteria or whether it requires an LLM call.

7. **Convergence pass credit timing**: When convergence passes on Run 1, the spec credits `CONVERGENCE_PASS_CREDIT=5`. But the budget was debited `CHECKER_COST=10` for Run 1. Is the 5-turn credit intentionally partial (net cost of 5 for a passing run), or should a Run-1 pass receive a larger credit?
