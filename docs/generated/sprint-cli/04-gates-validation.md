---
title: Sprint CLI - Gates & Validation System
generated: 2026-04-03
scope: cli/pipeline/gates.py, cli/roadmap/gates.py, cli/pipeline/executor.py
---

# Gates & Validation System

## Gate Architecture

Gates are the quality control mechanism that validates pipeline step outputs before allowing progression. The system uses a tiered enforcement model with two execution modes.

### Enforcement Tiers

```
EXEMPT   -> Always pass (no checks)
LIGHT    -> File exists + non-empty
STANDARD -> + min line count + required frontmatter keys
STRICT   -> + semantic check functions
```

### Gate Modes

- **BLOCKING** (`GateMode.BLOCKING`): Failure triggers retry; exhausted retries halt pipeline
- **TRAILING** (`GateMode.TRAILING`): Runs asynchronously; failures logged but don't halt

## Core Gate Function

**`src/superclaude/cli/pipeline/gates.py:20`** — `gate_passed()`

```python
def gate_passed(output_file: Path, criteria: GateCriteria) -> tuple[bool, str | None]:
```

Evaluation flow:
1. EXEMPT tier -> `(True, None)` immediately
2. LIGHT tier -> check file exists and is non-empty
3. STANDARD tier -> + min line count + `_check_frontmatter()` for required keys
4. STRICT tier -> + run all `SemanticCheck.check_fn` functions

### Frontmatter Checker (`_check_frontmatter` — line 85)

- Regex-extracts YAML frontmatter block
- Validates presence of all `required_frontmatter_fields`
- Returns `(True, None)` or `(False, "missing key: <key>")`

## Pipeline Executor Gate Integration

**`src/superclaude/cli/pipeline/executor.py`**

### Single Step Execution (line 174)

```
_execute_single_step(step, config)
  |
  +-> FOR attempt IN range(retry_limit + 1):
  |     +-> Run step (subprocess)
  |     +-> If gate exists:
  |     |     +-> BLOCKING mode:
  |     |     |     gate_passed(output, criteria)?
  |     |     |       YES -> StepStatus.PASS, break
  |     |     |       NO  -> retry (or FAIL if exhausted)
  |     |     +-> TRAILING mode:
  |     |           submit to TrailingGateRunner
  |     |           mark step as PASS immediately
  |     +-> No gate -> PASS on exit_code == 0
```

### Parallel Step Groups (line 297)

```
_run_parallel_steps(steps, config)
  |
  +-> ThreadPoolExecutor with shared cancel event
  +-> Any failure cancels siblings
  +-> All must pass for group success
```

## Roadmap Gate Catalog

**`src/superclaude/cli/roadmap/gates.py`**

### Gate Definitions

| Gate | Line | Tier | Purpose |
|------|------|------|---------|
| `EXTRACT_GATE` | 785 | STRICT | Extraction output validation |
| `EXTRACT_TDD_GATE` | 817 | STRICT | TDD extraction validation |
| `GENERATE_A_GATE` | 857 | STRICT | Agent A roadmap generation |
| `GENERATE_B_GATE` | 875 | STRICT | Agent B roadmap generation |
| `DIFF_GATE` | 893 | STANDARD | Diff analysis output |
| `DEBATE_GATE` | 899 | STRICT | Debate transcript validation |
| `SCORE_GATE` | 912 | STANDARD | Base selection scoring |
| `MERGE_GATE` | 918 | STRICT | Merged roadmap validation |
| `TEST_STRATEGY_GATE` | 941 | STRICT | Test strategy output |
| `SPEC_FIDELITY_GATE` | 984 | STRICT | Spec fidelity analysis (bypassed in convergence mode) |
| `REMEDIATE_GATE` | 1009 | STRICT | Remediation tasklist |
| `CERTIFY_GATE` | 1034 | STRICT | Certification report |
| `ANTI_INSTINCT_GATE` | 1063 | STRICT | Anti-instinct audit |
| `DEVIATION_ANALYSIS_GATE` | 1090 | STRICT | Deviation analysis |
| `ALL_GATES` | 1144 | — | Registry list |

### Semantic Validator Functions

All validators follow signature `content: str -> bool` or `content: str -> bool | str`:

| Function | Line | Validates |
|----------|------|-----------|
| `_no_heading_gaps` | 28 | No heading level skips |
| `_cross_refs_resolve` | 46 | Unresolved cross-refs (warning-only) |
| `_no_duplicate_headings` | 92 | No duplicate H2/H3 headings |
| `_frontmatter_values_non_empty` | 130 | All frontmatter values populated |
| `_has_actionable_content` | 141 | List items exist |
| `_high_severity_count_zero` | 191 | No high-severity findings |
| `_has_per_finding_table` | 218 | Certification report table present |
| `_all_actionable_have_status` | 244 | All remediation entries terminal |
| `_tasklist_ready_consistent` | 268 | Tasklist readiness consistent with counts |
| `_no_undischarged_obligations` | 316 | Zero undischarged obligations |
| `_integration_contracts_covered` | 334 | No uncovered contracts |
| `_fingerprint_coverage_check` | 352 | Coverage >= 0.7 |
| `_convergence_score_valid` | 370 | Score in [0,1] |
| `_no_ambiguous_deviations` | 388 | Zero ambiguous deviations |
| `_certified_is_true` | 414 | `certified: true` in frontmatter |
| `_validation_complete_true` | 432 | `analysis_complete: true` |
| `_routing_ids_valid` | 449 | DEV-\d+ ID format |
| `_slip_count_matches_routing` | 485 | Slip count matches routed IDs |
| `_pre_approved_not_in_fix_roadmap` | 523 | No overlap |
| `_total_analyzed_consistent` | 546 | Total = sum of categories |
| `_complexity_class_valid` | 619 | LOW/MEDIUM/HIGH only |
| `_extraction_mode_valid` | 632 | standard/chunked* |
| `_interleave_ratio_consistent` | 650 | Ratio by complexity class |
| `_milestone_counts_positive` | 678 | Positive integers |
| `_validation_philosophy_correct` | 698 | Exactly `continuous-parallel` |
| `_major_issue_policy_correct` | 714 | Exactly `stop-and-fix` |
| `_deviation_counts_reconciled` | 730 | Routed IDs reconcile with total |

## Step Dependency Graph (Roadmap)

**`src/superclaude/cli/roadmap/executor.py:1299`** — `_build_steps()`

```
extract
  |
  +-> [generate-A, generate-B]  (parallel)
        |
        +-> diff
              |
              +-> debate
                    |
                    +-> score
                          |
                          +-> merge
                                |
                                +-> anti-instinct
                                      |
                                      +-> test-strategy
                                            |
                                            +-> spec-fidelity
                                                  |
                                                  +-> wiring-verification  (TRAILING, non-blocking)
                                                  |
                                                  +-> deviation-analysis
                                                        |
                                                        +-> remediate
                                                              |
                                                              +-> certify  (built dynamically)
```

## Validation Points Across Pipeline

### Pre-Execution
- Binary check: `claude` exists in PATH (executor.py:1123)
- Config validation: file existence, phase gaps (config.py:237-247)
- Input type detection: PRD/TDD/spec (roadmap/executor.py:62)
- Input routing: arity/type/conflict guards (roadmap/executor.py:187)

### Mid-Pipeline
- Output sanitization before gate checks (roadmap executor:355, validate:49, tasklist:63)
- Anti-instinct audit: deterministic scaffold/mock detection (roadmap executor:535)
- Deviation analysis: deterministic spec-vs-roadmap comparison (roadmap executor:1027)
- Wiring verification: trailing mode gate (roadmap executor:1465)

### Post-Execution
- Result file classification: parse agent-written result for status (sprint executor:1555-1590)
- Checkpoint recovery: non-zero exit + PASS checkpoint = PASS_RECOVERED (executor:1592-1603)
- Resume freshness checks: hash-based staleness detection (roadmap executor:1645+)
- Degraded report generation on partial failure (validate executor:318)

## Cross-Module Gate Reuse

- `roadmap/validate_gates.py` reuses `_frontmatter_values_non_empty` from roadmap gates
- `tasklist/gates.py` reuses `_high_severity_count_zero` and `_tasklist_ready_consistent`
- `roadmap` uses `WIRING_GATE` from `audit/wiring_gate.py` as shared strict gate
- `cleanup_audit/gates.py` defines `GATE_G001..GATE_G006` with same pattern
- `cli_portify/gates.py` has large gate registry using same `tuple[bool, str]` convention
