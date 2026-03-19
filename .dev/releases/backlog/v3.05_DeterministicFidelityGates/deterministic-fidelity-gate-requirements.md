---
title: "Deterministic Spec-Fidelity Gate — Requirements Specification"
version: "1.0.0"
status: draft
created: 2026-03-19
source: "/sc:brainstorm systematic deep codebase"
parent_feature: v3.0_unified-audit-gating
relates_to:
  - src/superclaude/cli/roadmap/executor.py
  - src/superclaude/cli/roadmap/prompts.py
  - src/superclaude/cli/roadmap/gates.py
  - src/superclaude/cli/roadmap/remediate.py
  - src/superclaude/cli/roadmap/remediate_executor.py
  - src/superclaude/cli/roadmap/fidelity.py
---

# Deterministic Spec-Fidelity Gate — Requirements Specification

## 1. Problem Statement

The current roadmap CLI pipeline has a spec-fidelity gate that uses an LLM to
compare a spec against a generated roadmap and report deviations. This gate is
non-deterministic and gets stuck in infinite remediation loops.

After 4 failed runs on the v3.0 release, five failure modes were identified:

1. **Severity drift** — MEDIUM→HIGH across runs with no anchoring
2. **Full document regeneration** — destroying prior fixes
3. **Attention degradation** — on large inline-embedded documents
4. **No convergence mechanism** — no memory of prior findings
5. **Goalpost movement** — severity criteria re-interpreted each run

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| Runs 1→3 showed gradual convergence (3→1 HIGH), then Run 4 regressed catastrophically | `fidelity-remediation-log.md` | All prior fixes lost |
| Severity classifications drift between runs on identical content | Run logs, vote files | Non-deterministic gate behavior |
| Full roadmap regenerated from scratch on Run 4 | `fidelity-remediation-log.md` | Phase structure, numbering, paths all changed |
| Phantom requirement IDs (FR-009..FR-038) fabricated by LLM | `vote-2.md`, `vote-4.md` | False deviations inflate severity counts |
| Gate only checks `high_severity_count == 0` in frontmatter | `gates.py` | No validation of report quality or classification accuracy |

### 1.2 Scope Boundary

**In scope**: Refactoring the fidelity comparison, severity classification,
deviation tracking, remediation editing, and convergence control subsystems.

**Out of scope**: Upstream pipeline steps (extract, generate, diff, debate,
score, merge). Test strategy generation. Certification step.

---

## 2. Clarified User Goals

G1. **Determinism**: Same spec + same roadmap → same findings and severity
    classifications, every time.

G2. **Convergence**: The pipeline MUST terminate. 3 runs max (catch → verify →
    backup). If it can't converge in 3, halt and report — don't loop.

G3. **Edit preservation**: Remediation never destroys prior fixes. No full
    document regeneration without explicit user consent.

G4. **Anchored severity**: Severity is determined by structural rules where
    possible (~70% of deviations). When LLM assigns HIGH, adversarial debate
    validates it before the pipeline acts on it.

G5. **Scalability**: Large specs and roadmaps handled via chunked/sectional
    comparison, not full-inline embedding.

G6. **Auditability**: Every finding, every severity assignment, every
    remediation edit is traceable to a rule or debate verdict.

---

## 3. Functional Requirements

### FR-1: Decomposed Structural Checkers (5 Dimensions)

**Description**: Replace the monolithic LLM fidelity comparison with 5
independent, statically-typed checkers — one per dimension. Each checker
extracts structured data from spec and roadmap, compares deterministically,
and produces typed findings with predetermined severity rules.

**Checkers**:

| # | Checker | Extracts From Spec | Extracts From Roadmap | Structural % |
|---|---------|--------------------|-----------------------|-------------|
| 1 | **Signatures** | Function sigs from fenced Python, FR/NFR/SC ID sets | Referenced IDs, function names/params in task descriptions | 80% |
| 2 | **Data Models** | File manifest tables (Sec 4.1/4.2), dataclass fields, enum literals | File paths in tasks, field references, mode coverage | 85% |
| 3 | **Gates** | `GateCriteria` fields, `Step(...)` params, semantic check names, step ordering | Gate implementation tasks, parameter coverage | 65% |
| 4 | **CLI Options** | CLI table (Sec 5.1), config fields, `Literal[...]` modes, defaults | Config/option coverage in tasks | 75% |
| 5 | **NFRs** | Numeric thresholds, security primitives, dependency rules (Sec 6) | Corresponding targets/validations in roadmap | 55% |

**Acceptance Criteria**:
- [ ] Each checker is an independent callable that takes (spec_path, roadmap_path) → List[Finding]
- [ ] Each checker produces findings with severity assigned by structural rules, not LLM prose
- [ ] Checkers can run in parallel (no shared state)
- [ ] Each finding includes: dimension, rule_id, severity, spec_quote, roadmap_quote_or_MISSING, location
- [ ] A checker registry maps dimension names to checker callables

**Dependencies**: FR-2 (spec parser), FR-3 (severity rules)

---

### FR-2: Spec & Roadmap Parser

**Description**: A parser that extracts structured data from the spec template
format (YAML frontmatter, markdown tables, fenced code blocks, heading
hierarchy, requirement ID patterns) and from roadmap markdown.

**Acceptance Criteria**:
- [ ] Parses YAML frontmatter from both spec and roadmap
- [ ] Extracts markdown tables by section (keyed by heading path)
- [ ] Extracts fenced code blocks with language annotation
- [ ] Extracts requirement ID families via regex: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
- [ ] Extracts Python function signatures from fenced blocks: `def name(params) -> return_type`
- [ ] Extracts file paths from manifest tables (Sec 4.1, 4.2, 4.3)
- [ ] Extracts `Literal[...]` enum values from code blocks
- [ ] Extracts numeric threshold expressions: `< 5s`, `>= 90%`, `minimum 20`
- [ ] Returns structured objects, not raw text

**Dependencies**: None

---

### FR-3: Anchored Severity Rules

**Description**: Each structural checker has a severity rule table that maps
specific structural mismatch types to fixed severity levels. Severity is NOT
LLM-judged for structural findings.

**Rule Examples**:

| Dimension | Mismatch Type | Severity |
|-----------|--------------|----------|
| Signatures | Roadmap references ID not in spec | HIGH |
| Signatures | Function missing from roadmap | HIGH |
| Signatures | Parameter arity mismatch | MEDIUM |
| Data Models | Required spec file missing from roadmap | HIGH |
| Data Models | File path prefix mismatch | HIGH |
| Data Models | Enum literal not covered | MEDIUM |
| Gates | Required frontmatter field not covered | HIGH |
| Gates | Step parameter missing | MEDIUM |
| Gates | Ordering constraint violated | MEDIUM |
| CLI | Config mode not covered | MEDIUM |
| CLI | Default value mismatch | MEDIUM |
| NFRs | Numeric threshold contradicted | HIGH |
| NFRs | Security primitive missing | HIGH |
| NFRs | Dependency direction violated | HIGH |
| NFRs | Coverage threshold mismatch | MEDIUM |

**Acceptance Criteria**:
- [ ] Every structural checker has an explicit rule table
- [ ] Rules are defined in code (not prompt text), keyed by `(dimension, mismatch_type) → severity`
- [ ] Same inputs always produce the same severity — no randomness, no LLM interpretation
- [ ] Rule table is extensible (new rules can be added without changing checker logic)

**Dependencies**: FR-1

---

### FR-4: Residual Semantic Layer with Adversarial Validation

**Description**: After structural checkers complete, a residual LLM pass
handles the ~30% of checks that require semantic judgment (prose sufficiency,
spec contradiction resolution, additive-but-benign assessment). When the
semantic layer assigns HIGH severity, it does NOT auto-accept. Instead, it
triggers an adversarial debate (`/sc:adversarial`) to validate the rating.

**Acceptance Criteria**:
- [ ] Semantic layer receives only dimensions/aspects not covered by structural checkers
- [ ] Semantic layer uses chunked input (per-section, not full-document inline)
- [ ] When semantic layer assigns HIGH: pipeline pauses, spawns adversarial debate
- [ ] Adversarial debate produces a verdict: CONFIRM_HIGH, DOWNGRADE_TO_MEDIUM, or DOWNGRADE_TO_LOW
- [ ] Verdict is recorded in the deviation registry with debate transcript reference
- [ ] Semantic MEDIUM and LOW findings are accepted without debate
- [ ] Semantic layer prompt includes the structural findings as context (to avoid re-checking what's already checked)

**Dependencies**: FR-1 (structural findings as input), FR-6 (deviation registry)

---

### FR-5: Sectional/Chunked Comparison

**Description**: Replace full-document inline embedding with sectional
comparison. Both spec and roadmap are split by top-level sections. Each
checker operates on relevant sections only.

**Acceptance Criteria**:
- [ ] Spec is split by `## N. Section Name` headings into named chunks
- [ ] Roadmap is split by phase/task headings into named chunks
- [ ] Each checker receives only the sections relevant to its dimension
- [ ] No single prompt contains both full documents inline
- [ ] Prompt size per checker call is bounded (configurable, default ~30KB)
- [ ] Section mapping is deterministic: dimension → spec sections → roadmap sections

**Dependencies**: FR-2 (parser)

---

### FR-6: Deviation Registry

**Description**: A persistent, file-backed registry of all findings across
runs within a release. Each run appends new findings, updates status of
existing ones. The gate evaluates registry state, not fresh-scan results.

**Registry Lifecycle**: Resets when spec version changes (new spec = new registry).

**Statuses**: FIXED, SKIPPED, FAILED (matching current system).

**Acceptance Criteria**:
- [ ] Registry is a structured file (JSON or YAML) in the release output directory
- [ ] Each finding has a stable ID derived from (dimension, rule_id, spec_location, mismatch_type)
- [ ] New runs compare current findings against registry: new findings are appended, existing findings are matched by stable ID
- [ ] Fixed findings are marked FIXED (finding no longer reproduced on current inputs)
- [ ] Registry includes run metadata: run_number, timestamp, spec_hash, roadmap_hash
- [ ] Gate reads registry to determine pass/fail — not the raw fidelity report
- [ ] Registry resets when `spec_hash` changes (new spec version)

**Dependencies**: FR-1 (findings to register)

---

### FR-7: Convergence Gate

**Description**: The fidelity gate evaluates convergence based on registry
state with these criteria:
- **Pass**: Zero HIGH findings in registry (all FIXED or SKIPPED)
- **Monotonic progress**: Each run must have ≤ HIGHs than previous run
- **Hard budget**: Maximum 3 runs (catch → verify → backup)
- **Regression detection**: If run N+1 has MORE HIGHs than run N, trigger
  parallel validation (see FR-8)

**Acceptance Criteria**:
- [ ] Gate reads deviation registry, not raw fidelity output
- [ ] Pass requires: `active_high_count == 0`
- [ ] Run 2 must have `high_count <= run_1.high_count` or trigger FR-8
- [ ] Run 3 is final: pass or halt with full report
- [ ] If budget exhausted without convergence: halt, write diagnostic report, exit non-zero
- [ ] Progress proof is logged: `{run_n_highs} → {run_n+1_highs}` per run

**Dependencies**: FR-6 (registry), FR-8 (regression handling)

---

### FR-8: Regression Detection & Parallel Validation

**Description**: When run N+1 has MORE HIGHs than run N (regression detected),
the system spawns 3 parallel validation agents in isolated worktrees. Each
independently re-runs the fidelity check. Their findings are collected, merged
by stable ID, deduplicated, sorted by severity, and written to a consolidated
report. After the 4th total evaluation, an adversarial debate validates the
severity of each finding in the consolidated report.

**Acceptance Criteria**:
- [ ] Regression detected when `current_run.high_count > previous_run.high_count`
- [ ] 3 agents spawned in parallel, each in its own `git worktree`
- [ ] Each agent runs the full checker suite (structural + semantic) independently
- [ ] Results are merged: findings matched by stable ID across all 3 agents
- [ ] Unique findings (those appearing in any agent's results) are preserved
- [ ] Consolidated report written to `fidelity-regression-validation.md`
- [ ] Findings sorted by severity (HIGH → MEDIUM → LOW)
- [ ] After consolidation: adversarial debate (`/sc:adversarial`) validates severity of each HIGH
- [ ] Debate verdicts update the deviation registry
- [ ] This entire flow counts as one "run" toward the budget of 3

**Dependencies**: FR-1 (checkers), FR-4 (adversarial), FR-6 (registry), FR-7 (budget)

---

### FR-9: Edit-Only Remediation with Diff-Size Guard

**Description**: Remediation produces structured patches as MorphLLM-compatible
lazy edit snippets instead of freeform file rewrites. A per-patch diff-size
guard rejects any individual edit that modifies more than a configurable
percentage of the target file. Full document regeneration requires explicit
user consent.

**Patch Format (MorphLLM Lazy Snippets)**:
Patches use MorphLLM's semantic merging format, NOT unified diffs:
```
{
  "target_file": "roadmap.md",
  "finding_id": "SIG-001",
  "original_code": "<relevant section from current file>",
  "instruction": "Replace phantom FR-009 reference with correct G-001 ID",
  "update_snippet": "// ... existing code ...\n<changed lines>\n// ... existing code ...",
  "rationale": "Roadmap references FR-009 which does not exist in spec ID set"
}
```
Context markers (`// ... existing code ...`) indicate unchanged regions.
MorphLLM applies edits via semantic understanding, tolerating minor
line-number or formatting discrepancies.

**Acceptance Criteria**:
- [ ] Remediation agents output MorphLLM-compatible lazy edit snippets per finding
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] MorphLLM (when available) applies patches via semantic merging
- [ ] Fallback applicator (when MorphLLM unavailable): deterministic Python text replacement using original_code as anchor
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file (not all-or-nothing)
- [ ] Existing snapshot/restore mechanism retained for per-file rollback

**Dependencies**: FR-6 (finding IDs link patches to registry)

---

### FR-10: Run-to-Run Memory

**Description**: Each fidelity run has access to prior run findings and their
outcomes. The deviation registry (FR-6) is the primary memory mechanism. The
fidelity prompt (for the semantic layer) includes a summary of prior findings
to prevent re-discovery of already-fixed issues and to anchor severity
classification.

**Acceptance Criteria**:
- [ ] Semantic layer prompt includes: prior findings summary (ID, severity, status, run_number)
- [ ] Structural checkers implicitly have memory via registry diff (new vs known findings)
- [ ] Registry tracks `first_seen_run` and `last_seen_run` per finding
- [ ] Fixed findings from prior runs are not re-reported as new
- [ ] Summary is bounded: max 50 prior findings in prompt, oldest first truncated

**Dependencies**: FR-4 (semantic layer), FR-6 (registry)

---

## 4. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | Determinism | Same inputs → identical structural findings | Run twice on same inputs, diff output |
| NFR-2 | Convergence | ≤3 runs to pass or halt | Run counter in registry |
| NFR-3 | Prompt size | No single prompt exceeds 30KB | Measured before LLM call |
| NFR-4 | Checker independence | Checkers share no mutable state | Code review; parallel execution test |
| NFR-5 | Edit safety | No file changes >30% without user consent | Diff-size guard metric |
| NFR-6 | Traceability | Every finding traceable to rule_id or debate verdict | Audit log review |
| NFR-7 | Backward compat | Existing pipeline steps (1-7) unchanged | Integration test |

---

## 5. User Stories / Acceptance Criteria

### US-1: Pipeline operator runs fidelity gate on v3.0 spec
**Given** a spec and merged roadmap
**When** the fidelity gate runs
**Then** structural checkers produce deterministic findings, semantic layer handles residual checks, and the gate evaluates the deviation registry — producing a PASS (0 active HIGHs) or FAIL with a clear report.

### US-2: LLM assigns HIGH severity to a semantic finding
**Given** a semantic finding classified as HIGH
**When** the pipeline reaches that classification
**Then** an adversarial debate is spawned, produces a verdict (CONFIRM/DOWNGRADE), and the verdict is recorded in the registry before the gate evaluates.

### US-3: Run 2 regresses (more HIGHs than Run 1)
**Given** Run 2 produces more HIGHs than Run 1
**When** regression is detected
**Then** 3 parallel worktree agents independently validate, results are merged/deduped into `fidelity-regression-validation.md`, adversarial debate validates each HIGH, and updated findings are written to the registry.

### US-4: Remediation edits a roadmap section
**Given** a HIGH finding with a recommended correction
**When** remediation runs
**Then** a structured patch is generated, validated against the diff-size guard (≤30% changed lines), applied to the target file, and the finding is marked FIXED in the registry. If the patch exceeds the threshold, it is rejected and the finding is marked FAILED.

### US-5: Budget exhausted without convergence
**Given** 3 runs completed without reaching 0 active HIGHs
**When** the budget check triggers
**Then** the pipeline halts, writes a diagnostic report listing all active findings with run history, and exits non-zero.

### US-6: New spec version cuts
**Given** the spec hash changes (new version)
**When** the pipeline starts
**Then** the deviation registry is reset (fresh start for new spec), and all prior findings are archived.

---

## 6. Resolved Questions

| # | Question | Resolution |
|---|----------|------------|
| 1 | Should structural checkers produce confidence scores alongside severity? | **No.** Fixed severity is sufficient. Structural checkers are deterministic — their findings are definitionally certain. |
| 2 | Should FR-8 adversarial debate use full `/sc:adversarial` or lighter variant? | **Lighter-weight variant.** Full adversarial protocol is reserved for FR-4 (semantic HIGH validation). Regression validation uses a streamlined debate focused solely on severity confirmation, reducing token budget and latency. |
| 3 | What is the patch schema for MorphLLM integration? | **Lazy edit snippets with semantic merging.** MorphLLM does NOT use unified diffs or git diff format. It accepts: (1) original code, (2) editing instruction, (3) update snippet with `// ... existing code ...` context markers. Morph uses semantic understanding to merge, tolerating minor line-number or formatting errors. FR-9 patch model should produce MorphLLM-compatible lazy snippets, not unified diff hunks. |
| 4 | Should diff-size guard be per-file or per-patch? | **Per-patch.** Each individual patch is evaluated against the 30% threshold independently. This prevents a single large edit from hiding behind many small ones, and allows fine-grained rejection of oversized patches while accepting valid small ones for the same file. |
| 5 | How should cross-section references be handled in sectional comparison? | **Reference graph with bidirectional linking.** When the parser extracts structured data, it also extracts cross-references (e.g., FR-1.2 in Sec 3 referencing a signature in Sec 4). Checkers receive their primary sections plus any referenced sections as supplementary context. This keeps prompts bounded while preserving semantic completeness. The section→dimension mapping includes a "supplementary sections" field populated by reference extraction. |

---

## 7. Handoff

**Next steps**:
- `/sc:design` — Architecture design for the 5-checker framework, parser, registry, and patch applicator
- `/sc:adversarial` — Validate this requirements spec itself before implementation begins
- `/sc:workflow` — Implementation planning with task breakdown

**Key implementation risks**:
1. Spec parser robustness — real specs may deviate from template
2. Stable finding IDs — hash collisions or overly-specific IDs causing false "new" findings
3. Worktree isolation — 3 parallel agents need clean worktree management
4. Adversarial debate integration — new pipeline primitive (mid-step sub-orchestration)

---

## Appendix A: Current vs Proposed Architecture

### Current (as-is)
```
Spec + Roadmap (full inline) → Single LLM call → Fidelity report (YAML frontmatter)
  → Gate checks high_severity_count == 0
  → If fail: LLM agents edit files in-place (full file context)
  → Retry once → Pass or halt
```

### Proposed (to-be)
```
Spec + Roadmap → Parser extracts structured data per section
  → 5 Structural Checkers (parallel) → Typed findings with rule-based severity
  → Residual Semantic Layer (chunked) → Semantic findings
    → If any semantic HIGH: adversarial debate → verdict
  → All findings → Deviation Registry (append/update)
  → Convergence Gate reads registry
    → Pass: 0 active HIGHs
    → Regression detected: 3 parallel worktree agents → merge → adversarial debate
    → Fail + budget remaining: structured patch remediation (diff-size guarded)
    → Fail + budget exhausted: halt with diagnostic report
```

### Proposed Remediation Flow
```
Active findings → Group by target file
  → Per file: generate structured patches (line range, old/new text)
  → Validate: diff-size guard (≤30% changed lines per file)
  → Apply: deterministic patch applicator
  → Rollback: per-file snapshot/restore on failure
  → Update registry: FIXED / FAILED per finding
```

## Appendix B: Structural Checkability Evidence

Based on analysis of real deviations from 4 failed runs on v3.0:

| Deviation | Dimension | Could Be Structural? | Rule |
|-----------|-----------|---------------------|------|
| Phantom FR-009..FR-038 IDs | Signatures | Yes | Roadmap IDs ⊆ spec-defined IDs |
| Phantom NFR IDs | Signatures | Yes | Same |
| Missing `wiring_config.py` | Data Models | Yes | Spec manifest files ⊆ roadmap files |
| Wrong path prefix (`audit/` vs `cli/audit/`) | Data Models | Yes | Path prefix exact match |
| Missing test infrastructure files | Data Models | Yes | Manifest coverage |
| `ast_analyze_file()` dual placement | Signatures | Partial | Duplicate function detection |
| `audit_artifacts_used` omission | Gates | Partial | Field set comparison (but spec contradiction complicates) |
| `<2s` vs `<5s` threshold | NFRs | Yes | Numeric threshold extraction + comparison |
| Missing `yaml.safe_dump()` | NFRs | Yes | Security primitive presence check |
| Missing `_get_all_step_ids()` update | Gates | Mostly | Explicit MUST item → task mapping |
| Wrong `gate_passed()` signature | Signatures | Yes | Function signature matching |
| Missing step parameters | Gates | Yes | `Step(...)` parameter set comparison |
| "Implicitly covers" a requirement | Cross-cutting | No | Requires semantic judgment |
| Stricter phasing than spec | Gates | Partial | Dependency graph comparison (structural); intent judgment (semantic) |
| Additive risk R9 | Cross-cutting | No | Requires judgment on additive content |
