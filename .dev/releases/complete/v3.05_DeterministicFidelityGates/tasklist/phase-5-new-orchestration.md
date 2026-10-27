---
phase: 5
title: "New Orchestration Functions"
tasks: 8
depends_on: [3, 4]
parallelizable: partial
---

# Phase 5: New Orchestration Functions

These build the orchestration layer on top of the foundation modules. Dependency order:

```
T17 (run_semantic_layer) ──→ T18 (validate_semantic_high) ──→ T22 (execute_fidelity_with_convergence)
                                                                        ↑
T19 (RemediationPatch) ──→ T20 (apply_patches) ──→ T21 (fallback) ──→ │
                                                                        ↑
                                                T23 (handle_regression) ┘

T24 (check_morphllm) — independent
```

---

### T17: Create run_semantic_layer() entrypoint (FR-4)

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/semantic_layer.py
**FR**: FR-4
**Depends on**: T10 (checkers produce structural findings as context), T11 (section splitter)

**Action**: Add the top-level semantic layer entry point. This function:

1. Receives structural findings from checkers (FR-1) as context
2. Identifies dimensions/aspects NOT covered by structural rule tables (FR-3)
3. Uses chunked input per section (FR-5), not full-document inline
4. Calls `build_semantic_prompt()` with structural findings context
5. Tags all findings with `source_layer="semantic"`
6. Returns `list[Finding]`

**Interface**:
```python
def run_semantic_layer(
    spec_path: Path,
    roadmap_path: Path,
    structural_findings: list[Finding],
    registry: DeviationRegistry,
    config: RoadmapConfig,
) -> list[Finding]:
```

**Acceptance criteria**:
- [ ] Semantic layer receives only uncovered dimensions (FR-4 AC #1)
- [ ] Uses chunked input (FR-4 AC #2, FR-5)
- [ ] Includes structural findings as context (FR-4 AC #7)
- [ ] All findings tagged source_layer="semantic" (FR-4 AC #8)
- [ ] Prior findings summary from registry included in prompt (FR-10)

---

### T18: Create validate_semantic_high() (FR-4.1)

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/semantic_layer.py
**FR**: FR-4.1 — Lightweight Debate Protocol
**Depends on**: T17
**Decision**: Lives in semantic_layer.py; uses ClaudeProcess (established pattern)

**Action**: Implement the prosecutor/defender debate protocol for semantic HIGH findings:

1. Build prosecutor prompt (argues HIGH) and defender prompt (argues downgrade)
2. Execute both via `ClaudeProcess` in **parallel** (2 LLM calls) — pattern: executor.py:281, remediate_executor.py:198
3. Parse YAML responses from each
4. Score both against 4-criterion rubric (deterministic Python, no LLM):
   - Evidence Quality (30%): 0-3 points
   - Impact Specificity (25%): 0-3 points
   - Logical Coherence (25%): 0-3 points
   - Concession Handling (20%): 0-3 points
5. Compute margin = prosecutor_weighted - defender_weighted
6. Verdict: margin > 0.15 → CONFIRM_HIGH; margin < -0.15 → DOWNGRADE; else → CONFIRM_HIGH (conservative tiebreak)
7. Write debate output YAML to `output_dir/debates/{finding.stable_id}/debate.yaml`
8. Update registry with `debate_verdict` and `debate_transcript` reference

**Token budget**: ~3,800 per finding (hard cap: 5,000)
**YAML parse failure**: Side fails to produce valid YAML → all rubric scores default to 0 for that side

**Interface**:
```python
def validate_semantic_high(
    finding: Finding,
    spec_section: str,
    roadmap_section: str,
    output_dir: Path,
    registry: DeviationRegistry,
) -> str:  # Returns "CONFIRM_HIGH" | "DOWNGRADE_TO_MEDIUM" | "DOWNGRADE_TO_LOW"
```

**Acceptance criteria**:
- [ ] All 5 FR-4.1 acceptance criteria met
- [ ] Prosecutor and defender execute in parallel
- [ ] Judge is deterministic Python
- [ ] Conservative tiebreak (±0.15 margin → CONFIRM_HIGH)
- [ ] Debate YAML written per finding
- [ ] Registry updated with verdict

---

### T19: Create RemediationPatch dataclass (FR-9)

**Tier**: simple
**File**: src/superclaude/cli/roadmap/remediate_executor.py
**FR**: FR-9
**Decision**: MorphLLM-compatible format, ClaudeProcess execution

**Action**: Add the patch dataclass matching FR-9's JSON schema:

```python
@dataclass
class RemediationPatch:
    target_file: str
    finding_id: str
    original_code: str       # Anchor for matching (min 5 lines or 200 chars)
    instruction: str         # Human-readable edit instruction
    update_snippet: str      # New content with "// ... existing code ..." markers
    rationale: str           # Why this change is needed (links to finding)
```

**Acceptance criteria**:
- [ ] All 6 fields from FR-9 spec present
- [ ] Supports to_dict/from_dict for serialization
- [ ] Compatible with MorphLLM lazy edit format (context markers)

---

### T20: Create apply_patches() (FR-9)

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/remediate_executor.py
**FR**: FR-9
**Depends on**: T19 (RemediationPatch), T13 (per-patch diff guard)

**Action**: Implement sequential per-file, per-patch application:

1. Group patches by target_file
2. For each file: create snapshot (existing mechanism)
3. Apply patches sequentially within each file
4. Per-patch diff-size guard (T13): reject if `changed_lines / total_file_lines > 30%`
5. Rejected patches: log reason, set finding status to FAILED in registry
6. On patch failure: per-file rollback (T14), continue with next file
7. When `--allow-regeneration` and patch exceeds threshold: log WARNING, proceed

**Interface**:
```python
def apply_patches(
    patches: list[RemediationPatch],
    registry: DeviationRegistry,
    config: RoadmapConfig,
) -> dict[str, str]:  # {finding_id: "FIXED" | "FAILED"}
```

**Acceptance criteria**:
- [ ] Patches applied sequentially per file
- [ ] Per-patch diff guard enforced at 30%
- [ ] --allow-regeneration overrides threshold with WARNING
- [ ] Per-file rollback on failure
- [ ] Registry updated per finding

---

### T21: Create fallback_apply() (FR-9)

**Tier**: moderate
**File**: src/superclaude/cli/roadmap/remediate_executor.py
**FR**: FR-9
**Depends on**: T19

**Action**: Deterministic text replacement when MorphLLM is unavailable:

1. Use `RemediationPatch.original_code` as anchor
2. Find anchor in target file (minimum match: 5 lines or 200 chars per FR-9 AC #4)
3. Replace with `update_snippet` content
4. If anchor not found: mark patch as FAILED

**Interface**:
```python
def fallback_apply(patch: RemediationPatch, file_content: str) -> tuple[str, bool]:
    # Returns (new_content, success)
```

**Acceptance criteria**:
- [ ] Anchor matching with 5-line/200-char minimum
- [ ] Deterministic (same input → same output)
- [ ] Returns failure if anchor not found (no silent corruption)

---

### T22: Create execute_fidelity_with_convergence() (FR-7)

**Tier**: complex
**File**: src/superclaude/cli/roadmap/convergence.py
**FR**: FR-7 — Convergence Gate
**Depends on**: T10 (checkers), T17 (semantic layer), T20 (apply_patches)
**Risk**: §7a (convergence loop vs linear pipeline), §7b (remediation ownership)

**Action**: Implement the 3-run convergence loop orchestrator:

```
Run 1 (catch):
  → structural_checkers (parallel) → semantic_layer → register findings
  → if 0 active HIGHs: PASS
  → else: remediate → Run 2

Run 2 (verify):
  → structural_checkers → semantic_layer → register findings
  → monotonic check: structural_high_count must be ≤ Run 1 (else → handle_regression via FR-8)
  → semantic HIGH fluctuations: log warning only
  → if 0 active HIGHs: PASS
  → else: remediate → Run 3

Run 3 (backup — final):
  → structural_checkers → semantic_layer → register findings
  → if 0 active HIGHs: PASS
  → else: HALT with diagnostic report, exit non-zero
```

**Key constraints**:
- Self-contained within step 8 — does NOT re-run the full pipeline (§7a)
- Remediation runs WITHIN the loop, not post-pipeline (§7b)
- In convergence mode, SPEC_FIDELITY_GATE is never invoked (gate authority model)
- Progress logged with split counts: `structural: {n} → {n+1}, semantic: {n} → {n+1}`

**Interface**:
```python
def execute_fidelity_with_convergence(
    spec_path: Path,
    roadmap_path: Path,
    output_dir: Path,
    config: RoadmapConfig,
) -> ConvergenceResult:
```

**Acceptance criteria**:
- [ ] All 11 FR-7 acceptance criteria met
- [ ] Maximum 3 runs enforced
- [ ] Monotonic check on structural_high_count only
- [ ] Registry is sole authority (not SPEC_FIDELITY_GATE)
- [ ] Diagnostic report on budget exhaustion

---

### T23: Create handle_regression() (FR-8)

**Tier**: complex
**File**: src/superclaude/cli/roadmap/convergence.py
**FR**: FR-8 — Regression Detection & Parallel Validation
**Depends on**: T10 (checkers), T18 (debate protocol), T22 (budget tracking)
**Risk**: §7g (circular interface with FR-7)

**Action**: When structural HIGHs increase between runs:

1. Spawn 3 parallel validation agents in isolated temp directories
   - Use existing `_create_validation_dirs()` / `_cleanup_validation_dirs()` / `_atexit_cleanup()` (convergence.py:278-323)
   - Each dir contains independent copies of spec, roadmap, registry snapshot
2. Each agent runs full checker suite (structural + semantic) independently
3. Collect results, merge by stable_id, deduplicate
4. Write consolidated `fidelity-regression-validation.md`
5. Sort findings by severity (HIGH → MEDIUM → LOW)
6. For each HIGH: run adversarial debate (validate_semantic_high, T18)
7. Update registry with debate verdicts
8. This entire flow counts as ONE run toward budget of 3

**Cleanup guarantee**: try/finally + atexit fallback. No git worktrees. No `.git/worktrees/` artifacts.

**Interface**:
```python
def handle_regression(
    spec_path: Path,
    roadmap_path: Path,
    registry: DeviationRegistry,
    output_dir: Path,
    config: RoadmapConfig,
) -> list[Finding]:  # Consolidated, deduplicated findings
```

**Acceptance criteria**:
- [ ] All 16 FR-8 acceptance criteria met
- [ ] 3 agents in isolated temp dirs (not worktrees)
- [ ] Semantic HIGH increases alone do NOT trigger regression
- [ ] Cleanup guaranteed via try/finally + atexit
- [ ] Counts as one run toward budget

---

### T24: Create check_morphllm_available() (FR-9)

**Tier**: simple
**File**: src/superclaude/cli/roadmap/remediate_executor.py
**FR**: FR-9

**Action**: MCP runtime probe to check if MorphLLM is available:

1. Check if `morphllm-fast-apply` MCP server is configured
2. If available: `apply_patches()` can use MorphLLM for semantic merging
3. If not available: use `fallback_apply()` (deterministic text replacement)

**Interface**:
```python
def check_morphllm_available() -> bool:
```

**Acceptance criteria**:
- [ ] Returns True if MorphLLM MCP server is accessible
- [ ] Returns False gracefully (no exception) if unavailable
- [ ] Called once at start of remediation, not per-patch
