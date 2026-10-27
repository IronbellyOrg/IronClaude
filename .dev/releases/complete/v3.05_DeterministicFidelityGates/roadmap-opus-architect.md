---
spec_source: "deterministic-fidelity-gate-requirements.md"
complexity_score: 0.88
primary_persona: architect
---

# Deterministic Fidelity Gates — v3.05 Roadmap

## Executive Summary

v3.05 replaces the monolithic LLM-based fidelity comparison with a **hybrid deterministic/semantic architecture**: five parallel structural checkers produce reproducible findings (~70%), a residual semantic layer handles judgment-dependent checks (~30%), and an adversarial debate protocol validates high-severity semantic findings. A convergence engine (≤3 runs) with TurnLedger budget accounting replaces the single-shot gate.

**Key architectural decisions**:
- Structural checkers are pure functions with zero shared mutable state — enabling safe parallelism and deterministic output (NFR-1, NFR-4)
- Legacy mode (`convergence_enabled=false`) remains byte-identical to commit `f4d9035` — all new behavior is opt-in (NFR-7)
- The deviation registry is the single source of truth for gate pass/fail in convergence mode; `SPEC_FIDELITY_GATE` is excluded
- TurnLedger is consumed from `sprint/models.py` without modification — cross-module import is conditional and convergence-only

**Scope**: 12 functional requirements, 7 non-functional requirements, ~10 files modified/created across 3 module boundaries. ~60% infrastructure pre-built in v3.0.

---

## Phased Implementation Plan

### Phase 1: Foundation — Parser & Data Model (Days 1–4)

**Goal**: Establish the parsing infrastructure and data models that every downstream component depends on. This is the critical path entry point.

**Requirements**: FR-2, FR-5, FR-3 (partial: severity rule table definition), FR-6 (partial: Finding dataclass extension)

#### Milestone 1.1: Spec & Roadmap Parser (FR-2)
- Create `src/superclaude/cli/roadmap/spec_parser.py`
- Implement YAML frontmatter extraction with graceful degradation (`ParseWarning` on malformed input)
- Implement markdown table extraction keyed by heading path
- Implement fenced code block extraction with language annotation
- Implement requirement ID regex extraction: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
- Implement Python function signature extraction from fenced blocks
- Implement `Literal[...]` enum value extraction
- Implement numeric threshold expression extraction (`< 5s`, `>= 90%`, `minimum 20`)
- Implement file path extraction from manifest tables (Sec 4.1, 4.2, 4.3)
- **Validation gate**: Run parser against real spec (`deterministic-fidelity-gate-requirements.md`) — not synthetic fixtures only

#### Milestone 1.2: Sectional Splitting (FR-5)
- Define `SpecSection` dataclass: `heading`, `heading_path`, `level`, `content`, `start_line`, `end_line`
- Implement `split_into_sections(content: str) -> list[SpecSection]` in `spec_parser.py`
- Handle YAML frontmatter as special section (level=0, heading="frontmatter")
- Handle preamble content before first heading (level=0)
- Define dimension-to-section mapping for checker routing

#### Milestone 1.3: Data Model Extensions
- Extend `Finding` dataclass with `rule_id`, `spec_quote`, `roadmap_quote` fields (all defaulted for backward compat)
- Define `SEVERITY_RULES: dict[tuple[str, str], str]` structure and `get_severity()` function (FR-3)
- Define `ParseWarning` type
- Define `RunMetadata` dataclass for registry run tracking

**Exit criteria**:
- Parser produces structured output from real spec with zero crashes
- `ParseWarning` list correctly populated for malformed inputs
- `SpecSection` round-trips: split → reassemble matches original content
- All data model extensions backward-compatible (existing serialized data still loads)

**Risk checkpoint**: FR-2 is the critical path entry. If parser robustness issues surface here, escalate immediately — every downstream phase depends on it (Risk #1).

---

### Phase 2: Structural Checkers & Severity Engine (Days 5–9)

**Goal**: Build the five deterministic checkers and their severity rule tables. After this phase, ~70% of fidelity checks are deterministic.

**Requirements**: FR-1, FR-3 (full)

#### Milestone 2.1: Checker Registry & Interface
- Define checker callable interface: `(spec_path, roadmap_path) → List[Finding]`
- Implement checker registry mapping dimension names to callables
- Ensure checkers receive only relevant `SpecSection` objects per dimension-to-section mapping (consuming FR-5)

#### Milestone 2.2: Five Structural Checkers
1. **Signatures checker** — Compares function signatures extracted from spec code blocks against roadmap
2. **Data Models checker** — Compares dataclass/type definitions between spec and roadmap
3. **Gates checker** — Verifies gate definitions, thresholds, pass/fail criteria
4. **CLI Options checker** — Compares Click options, flags, defaults
5. **NFRs checker** — Verifies numeric thresholds, constraint expressions

Each checker:
- Uses machine keys for `mismatch_type` (e.g., `phantom_id`, `function_missing`)
- Assigns severity via `get_severity()` lookup — never LLM
- Produces findings with: dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location
- Has no shared mutable state with other checkers

#### Milestone 2.3: Severity Rule Tables (FR-3)
- Implement all 19 canonical rules across 5 dimensions
- `KeyError` on unknown `(dimension, mismatch_type)` combinations
- Verify determinism: same inputs → identical output across runs (NFR-1)

**Exit criteria**:
- All 5 checkers pass unit tests with real spec sections
- Checkers execute in parallel without interference (NFR-4)
- Determinism verified: two runs on identical input produce byte-identical findings (SC-1)
- Severity rules cover all 19 canonical mismatch types

---

### Phase 3: Deviation Registry & Convergence Engine (Days 10–15)

**Goal**: Implement the persistent registry and convergence loop with TurnLedger budget accounting. This is the state management core.

**Requirements**: FR-6, FR-7, FR-7.1

#### Milestone 3.1: Deviation Registry Extension (FR-6)
- Extend existing `convergence.py` (lines 50–225) `DeviationRegistry` class
- Add `source_layer` field to findings: `"structural"` or `"semantic"`
- Implement stable ID computation: `(dimension, rule_id, spec_location, mismatch_type)`
- Implement cross-run comparison: match by stable ID, mark FIXED when not reproduced
- Add `first_seen_run` and `last_seen_run` tracking per finding
- Add run metadata: `run_number`, `timestamp`, `spec_hash`, `roadmap_hash`, `structural_high_count`, `semantic_high_count`, `total_high_count`
- Implement spec version change detection → registry reset
- Handle pre-v3.05 registries: default missing `source_layer` to `"structural"`
- Accept `ACTIVE` as valid status alongside `PENDING`

#### Milestone 3.2: Convergence Gate (FR-7)
- Implement `execute_fidelity_with_convergence()` in `convergence.py`
- Pass condition: `active_high_count == 0` (structural + semantic)
- Monotonic progress check on `structural_high_count` only
- Semantic HIGH increases → warnings, not regressions
- Run 2: `structural_high_count <= run_1.structural_high_count` or trigger FR-8
- Run 3: final — pass or halt with full diagnostic report
- Budget exhaustion: halt, diagnostic report, exit non-zero
- Convergence operates within step 8 boundary only

#### Milestone 3.3: TurnLedger Integration
- Import `TurnLedger` from `superclaude.cli.sprint.models` (conditional, convergence-only)
- Pipeline executor constructs `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` when convergence enabled
- Implement budget guards: `can_launch()` before checker runs, `can_remediate()` before remediation
- Implement `reimburse_for_progress()` using `ledger.reimbursement_rate`
- Cost constants module-level in `convergence.py`: CHECKER_COST=10, REMEDIATION_COST=8, REGRESSION_VALIDATION_COST=15, CONVERGENCE_PASS_CREDIT=5
- Early convergence pass credits `CONVERGENCE_PASS_CREDIT`
- Progress credit logging: `"Run {n}: progress credit {credit} turns (structural {prev} -> {curr})"`
- Run metadata includes ledger snapshot in convergence mode

#### Milestone 3.4: Legacy/Convergence Dispatch
- Single dispatch point via `convergence_enabled` boolean
- Legacy mode: `SPEC_FIDELITY_GATE` only, no TurnLedger import or construction
- Convergence mode: `DeviationRegistry` authoritative, `SPEC_FIDELITY_GATE` excluded
- `_check_remediation_budget()` and `_print_terminal_halt()` NOT invoked in convergence mode
- Convergence result mapped to `StepResult` for pipeline compatibility
- `convergence_enabled: bool = False` default preserves legacy behavior (NFR-7)

#### Milestone 3.5: FR-7/FR-8 Interface Contract (FR-7.1)
- Define `handle_regression()` callable signature returning `RegressionResult`
- Define `RegressionResult` dataclass: `validated_findings`, `debate_verdicts`, `agents_succeeded`, `consolidated_report_path`
- Regression validation + remediation = one budget unit
- `ledger.debit(REGRESSION_VALIDATION_COST)` called before `handle_regression()`
- `handle_regression()` performs no ledger operations internally

**Exit criteria**:
- Registry correctly tracks findings across 3 simulated runs
- Stable IDs are collision-free on test corpus (Risk #2 mitigation)
- Legacy mode produces byte-identical output to commit `f4d9035` (SC-5)
- Convergence mode terminates within ≤3 runs on all test cases (SC-2)
- TurnLedger budget never goes negative without halt
- Dual budget mutual exclusion verified by integration test (Risk #5 mitigation)

---

### Phase 4: Semantic Layer & Adversarial Debate (Days 16–21)

**Goal**: Implement the residual semantic layer for judgment-dependent checks and the adversarial debate protocol for HIGH severity validation.

**Requirements**: FR-4, FR-4.1, FR-4.2, FR-10

#### Milestone 4.1: Semantic Layer Extension (FR-4)
- Extend existing `semantic_layer.py` (337 lines)
- Receive only dimensions/aspects not covered by structural checkers
- Use chunked input (per-section, not full-document inline)
- Structural findings passed as context in prompt
- All semantic findings tagged with `source_layer="semantic"`
- Semantic MEDIUM and LOW accepted without debate

#### Milestone 4.2: Prompt Budget Enforcement (FR-4.2)
- Total budget: 30,720 bytes
- Allocation: 60% spec/roadmap, 20% structural context, 15% prior summary, 5% template
- Truncation markers: `[TRUNCATED: N bytes omitted from '<heading>']`
- Template exceeding 5% allocation raises `ValueError`
- Truncation priority: prior summary → structural context → spec/roadmap sections
- Assert before every LLM call (NFR-3, SC-6)

#### Milestone 4.3: Lightweight Debate Protocol (FR-4.1)
- Implement `validate_semantic_high()` in `semantic_layer.py` (protocol steps 1–7)
- Accept `claude_process_factory` parameter for test injection
- Prosecutor and defender execute in parallel (2 LLM calls)
- Deterministic Python judge — same scores always produce same verdict
- 4-criterion rubric: Evidence Quality (30%), Impact Specificity (25%), Logical Coherence (25%), Concession Handling (20%)
- Conservative tiebreak: margin within ±0.15 → CONFIRM_HIGH
- Verdict: CONFIRM_HIGH, DOWNGRADE_TO_MEDIUM, or DOWNGRADE_TO_LOW
- YAML output per finding with rubric scores, margin, verdict
- Registry updated with `debate_verdict` and `debate_transcript` reference
- Token budget: ~3,800 per finding (hard cap: 5,000)
- YAML parse failure: all rubric scores default to 0 for that side

#### Milestone 4.4: Run-to-Run Memory (FR-10)
- Prior findings summary in semantic prompt: ID, severity, status, run_number
- Max 50 prior findings, oldest-first truncation
- Fixed findings from prior runs not re-reported as new
- Registry tracks `first_seen_run` and `last_seen_run` per finding
- Run metadata includes ledger snapshot in convergence mode

**Exit criteria**:
- Semantic layer processes only non-structural dimensions
- No prompt exceeds 30,720 bytes (SC-6) — verified by assertion
- Debate protocol produces consistent verdicts on identical inputs
- ≥70% of findings have severity determined by structural rules (SC-4)
- Prior findings correctly influence semantic layer behavior

---

### Phase 5: Regression Detection & Remediation (Days 22–27)

**Goal**: Implement parallel regression validation and the structured patch remediation system.

**Requirements**: FR-8, FR-9, FR-9.1

#### Milestone 5.1: Regression Detection & Parallel Validation (FR-8)
- Regression trigger: `current_run.structural_high_count > previous_run.structural_high_count`
- Semantic HIGH increases alone do NOT trigger regression
- 3 agents spawned in parallel in isolated temp directories
- Each agent runs full checker suite independently
- Results merged by stable ID; unique findings preserved
- Consolidated report: `fidelity-regression-validation.md`
- Findings sorted by severity (HIGH → MEDIUM → LOW)
- Adversarial debate validates HIGH severity after consolidation
- Debate verdicts update deviation registry
- All 3 agents must succeed; any failure → validation FAILED, run not counted
- Cleanup: try/finally + atexit fallback (Risk #3 mitigation)
- No git worktree calls; no `.git/worktrees/` artifacts

#### Milestone 5.2: Edit-Only Remediation (FR-9)
- Extend existing `remediate_executor.py` (563 lines)
- `RemediationPatch` dataclass: target_file, finding_id, original_code, instruction, update_snippet, rationale
- MorphLLM-compatible JSON output format
- ClaudeProcess primary applicator; `fallback_apply()` for deterministic text replacement (min anchor: 5 lines or 200 chars)
- `check_morphllm_available()` probes MCP runtime (future migration prep)
- Per-patch diff-size guard: reject if `changed_lines / patch_original_lines > 30%` (NFR-5)
- `_check_diff_size()` retired; replaced by per-patch evaluation
- Partial rejection: valid patches applied even when others rejected
- Rejected patches logged with reason; finding status → FAILED
- Valid patches for same file applied sequentially
- Per-file rollback: each file evaluated independently
- Post-execution cross-file coherence check
- Existing snapshot/restore mechanism retained

#### Milestone 5.3: `--allow-regeneration` Flag (FR-9.1)
- Click `is_flag=True` option on `run` command
- `allow_regeneration: bool = False` on `RoadmapConfig`
- Without flag: >30% patches rejected (FAILED)
- With flag: >30% patches applied with WARNING log (includes patch ID, actual ratio, threshold)

**Exit criteria**:
- Regression validation correctly spawns 3 agents and merges results
- Temp directory cleanup verified: no orphaned directories after failure simulation
- Remediation produces valid `RemediationPatch` objects
- Diff-size guard rejects >30% patches correctly
- `--allow-regeneration` overrides guard with warning
- Previously-fixed findings do not re-appear as ACTIVE after remediation (SC-3)

---

### Phase 6: Integration, Cleanup & Verification (Days 28–32)

**Goal**: Wire all components together, delete dead code, verify all success criteria end-to-end.

**Requirements**: NFR-1 through NFR-7, SC-1 through SC-6, architectural constraints

#### Milestone 6.1: Pipeline Integration
- Wire structural checkers → semantic layer → convergence engine → remediation in step 8
- Verify steps 1–7 and step 9 are unaffected
- Convergence result maps to `StepResult` for pipeline compatibility
- `execute_fidelity_with_convergence()` calls `execute_remediation()` between runs

#### Milestone 6.2: Dead Code Removal
- Delete `fidelity.py` (66 lines, zero imports)
- Verify no remaining references

#### Milestone 6.3: End-to-End Verification
- **SC-1**: Run same spec+roadmap twice → byte-identical structural findings
- **SC-2**: Pipeline terminates within ≤3 runs or halts with diagnostic
- **SC-3**: Fixed findings remain FIXED after remediation
- **SC-4**: ≥70% findings from structural rules
- **SC-5**: Legacy mode byte-identical to commit `f4d9035`
- **SC-6**: No semantic prompt exceeds 30,720 bytes
- **NFR-4**: Checkers share no mutable state (parallel execution test)
- **NFR-7**: Integration test confirming steps 1–7 unchanged

#### Milestone 6.4: Open Question Resolution
- Validate rubric threshold (0.15) against real semantic findings corpus (OQ-1)
- Document ParseWarning handling decision: log-and-continue vs. block (OQ-3)
- Document agent failure criteria for regression validation (OQ-5)
- Document cross-file coherence check criteria (OQ-6)

**Exit criteria**:
- All 6 success criteria pass
- All 7 non-functional requirements verified
- Legacy mode regression test passes
- No orphaned temp directories, no git worktree artifacts
- All open questions documented with decisions

---

## Risk Assessment & Mitigation

| # | Risk | Severity | Phase | Mitigation |
|---|------|----------|-------|------------|
| 1 | Spec parser robustness — real specs deviate from template | HIGH | Phase 1 | Graceful degradation with `ParseWarning`; validate against real spec, not synthetics only. Parser is critical path (FR-2 → FR-1 → FR-4 → FR-7). |
| 2 | Stable finding ID collisions — false "new" findings undermine convergence | MEDIUM | Phase 3 | Tuple-based ID `(dimension, rule_id, spec_location, mismatch_type)`; test with real deviation sets. |
| 3 | Temp directory cleanup leaks — orphaned dirs consume disk | MEDIUM | Phase 5 | Dual cleanup: try/finally + atexit handler; prefix-based identification for manual cleanup. |
| 4 | Debate rubric calibration — 0.15 margin threshold is heuristic | MEDIUM | Phase 4 | Conservative tiebreak (CONFIRM_HIGH) limits downside; log all rubric scores; tunable constants. |
| 5 | Dual budget system overlap — double-charging if dispatch fails | HIGH | Phase 3 | Single dispatch via `convergence_enabled`; integration test verifying mutual exclusion. Most critical test in Phase 3. |
| 6 | Cross-module import fragility — TurnLedger moves break import | LOW | Phase 3 | Conditional import (convergence only); one-line fix on migration; documented in handoff notes. |

**Additional architectural risks identified**:

| # | Risk | Severity | Phase | Mitigation |
|---|------|----------|-------|------------|
| 7 | Pre-v3.05 registry migration — defaulting `source_layer` to `"structural"` may misclassify old semantic findings | MEDIUM | Phase 3 | Accept for v3.05 (conservative — treats unknowns as structural for monotonic progress). Document limitation. |
| 8 | Convergence pass credit asymmetry — Run 1 pass costs net 5 turns (10 debit - 5 credit) | LOW | Phase 3 | Intentional partial credit per spec. Document rationale: even a passing run consumed resources. |

---

## Resource Requirements & Dependencies

### External Dependencies (Consumed, Not Modified)
1. **TurnLedger** from `superclaude.cli.sprint.models` — budget accounting. Methods: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`
2. **ClaudeProcess** — LLM subprocess execution for debate agents, validation agents, patch application
3. **Click CLI** — `--allow-regeneration` flag addition
4. **YAML parser** — frontmatter and debate output serialization

### Internal Dependencies (Extended)
5. **DeviationRegistry** (`convergence.py:50-225`) — extended with `source_layer`, split HIGH counts
6. **Finding dataclass** (`models.py`) — extended with `rule_id`, `spec_quote`, `roadmap_quote`
7. **RoadmapConfig** (`models.py`) — `convergence_enabled` and `allow_regeneration` fields (pre-existing)
8. **`remediate_executor.py`** (563 lines) — extended with structured patches and per-patch diff guard

### Future Dependencies (Probed, Not Required)
9. **MorphLLM MCP** — `check_morphllm_available()` probes runtime; not blocking for v3.05

### Files to Create
- `src/superclaude/cli/roadmap/spec_parser.py` — FR-2, FR-5
- `src/superclaude/cli/roadmap/structural_checkers.py` — FR-1, FR-3
- Tests for all new modules

### Files to Modify
- `convergence.py` — FR-6, FR-7, FR-7.1
- `semantic_layer.py` — FR-4, FR-4.1, FR-4.2, FR-10
- `remediate_executor.py` — FR-9, FR-9.1
- `models.py` — Finding extension, RemediationPatch, RunMetadata, RegressionResult
- Pipeline executor — convergence dispatch, TurnLedger construction
- CLI `run` command — `--allow-regeneration` flag

### Files to Delete
- `fidelity.py` (66 lines, zero imports)

---

## Success Criteria & Validation Approach

| Criterion | Validation Method | Phase |
|-----------|------------------|-------|
| SC-1: Deterministic structural findings | Run identical inputs twice, `diff` output — zero differences | Phase 2 (unit), Phase 6 (E2E) |
| SC-2: Convergence within budget | Run convergence loop on test cases; verify ≤3 runs; verify TurnLedger never negative at halt | Phase 3 (unit), Phase 6 (E2E) |
| SC-3: Edit preservation | Run remediation, verify FIXED findings remain FIXED in subsequent run | Phase 5 (unit), Phase 6 (E2E) |
| SC-4: Severity anchoring | Count structural vs. semantic findings; assert ≥70% structural | Phase 4 (integration), Phase 6 (E2E) |
| SC-5: Legacy backward compatibility | Run pipeline with `convergence_enabled=false` on baseline spec; diff output against commit `f4d9035` output | Phase 3 (continuous), Phase 6 (gate) |
| SC-6: Prompt size compliance | Assert `len(prompt) <= 30720` before every LLM call in semantic layer | Phase 4 (unit), Phase 6 (E2E) |

---

## Timeline Summary

| Phase | Days | Focus | Key Deliverables |
|-------|------|-------|-----------------|
| 1 | 1–4 | Foundation | Parser, section splitter, data models |
| 2 | 5–9 | Structural Checkers | 5 checkers, severity engine, registry |
| 3 | 10–15 | Convergence Engine | Deviation registry, convergence gate, TurnLedger integration, legacy dispatch |
| 4 | 16–21 | Semantic Layer | Residual semantic pass, debate protocol, prompt budget, run-to-run memory |
| 5 | 22–27 | Regression & Remediation | Parallel validation, structured patches, diff guard |
| 6 | 28–32 | Integration & Verification | E2E wiring, dead code removal, all SC/NFR verification |

**Total estimated duration**: 32 working days

**Critical path**: FR-2 (parser) → FR-1 (checkers) → FR-4 (semantic layer) → FR-7 (convergence gate) → Integration

**Parallelization opportunities**:
- Phase 2 checkers can be developed in parallel (5 independent units)
- Phase 3 registry and TurnLedger integration are independent until convergence gate wiring
- Phase 4 debate protocol and prompt budget enforcement are independent
- Phase 5 regression detection and remediation extension are semi-independent (shared via FR-7.1 contract)
