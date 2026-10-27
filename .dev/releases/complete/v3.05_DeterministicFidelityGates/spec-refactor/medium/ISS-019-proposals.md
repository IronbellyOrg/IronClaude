# ISS-019 Refactoring Proposals

> **Issue**: No "existing baseline from v3.0" section in spec. The spec assumes greenfield when 19 requirements are already fully satisfied and 3 modules already exist.
>
> **Source**: Compatibility Report Section 8, Priority 2
>
> **Overlap Analysis**: ISS-001/002/003 (CRITICAL) reclassify individual FRs from CREATE to MODIFY. Their per-FR proposals (baseline subsections, description rewording) address the _symptoms_ within each FR but do NOT address the _root cause_: the spec has no single place that inventories what v3.0 already provides. An implementer who reads only FR-2 (spec_parser.py, genuinely new) has no way to know that the adjacent FR-4 module already exists. ISS-019 requires a **global baseline section** that ISS-001/002/003 per-FR fixes cannot replace.
>
> **Verdict**: ISS-001/002/003 resolutions are necessary but NOT sufficient. ISS-019 requires its own resolution: a dedicated spec section.

---

## Proposal #1: Insert Section 1.3 "v3.0 Baseline" into Problem Statement (RECOMMENDED)

**Strategy**: Add a new subsection within the existing Problem Statement (Section 1) that documents the v3.0 baseline. This is the natural home because the Problem Statement already contextualizes v3.05 as a response to v3.0 failures. Placing the baseline here ensures every reader encounters it before reaching any FR.

### Exact Spec Text to Add

**File**: `deterministic-fidelity-gate-requirements.md`

**Location**: Insert after line 58 (end of Section 1.2 Scope Boundary), before the `---` separator at line 60.

**New text**:

```markdown

### 1.3 v3.0 Baseline

This spec was originally drafted before v3.0 shipped. During v3.0 implementation,
~60% of the v3.05 infrastructure was pre-built. The spec MUST be read as
"extend existing code," not "build from scratch." The following inventory is
verified against commit `f4d9035`.

#### Pre-Existing Modules (MODIFY, not CREATE)

| Module | Lines | Key Capabilities | v3.05 FRs That Extend |
|--------|-------|------------------|-----------------------|
| `convergence.py` | 323 | DeviationRegistry lifecycle, compute_stable_id(), ConvergenceResult, _check_regression() (structural-only), temp dir isolation + atexit, get_prior_findings_summary() | FR-6, FR-7, FR-8, FR-10 |
| `semantic_layer.py` | 337 | Prompt budget constants + enforcement (FR-4.2), build_semantic_prompt(), debate scoring (RubricScores, score_argument, judge_verdict), wire_debate_verdict(), prosecutor/defender templates | FR-4, FR-4.1, FR-4.2, FR-5 |
| `remediate_executor.py` | 563 | Snapshot create/restore/cleanup, enforce_allowlist(), parallel ClaudeProcess agents, _check_diff_size() at 50% per-file, all-or-nothing rollback | FR-9 |

#### Pre-Existing Config & Pipeline Wiring (no work needed)

| Component | Location | Spec Requirement |
|-----------|----------|------------------|
| `ACTIVE` in `VALID_FINDING_STATUSES` | models.py:16 | FR-6/BF-1 |
| `Finding.source_layer` field | models.py:44 | FR-6/BF-3 |
| `RoadmapConfig.convergence_enabled` | models.py:107 | FR-7 |
| `RoadmapConfig.allow_regeneration` | models.py:108 | FR-9.1 |
| `--allow-regeneration` CLI flag | commands.py:89-94 | FR-9.1 |
| `WIRING_GATE` registered in `ALL_GATES` | gates.py:944 | NFR-7 |
| `SPEC_FIDELITY_GATE` conditional bypass | executor.py:521 | FR-7 |
| `first_seen_run` / `last_seen_run` tracking | convergence.py:104-130 | FR-10 |
| Prior findings in semantic prompt | semantic_layer.py:140,215-221 | FR-10 |

#### Genuinely New Modules (CREATE)

| Module | Spec Ref | Description |
|--------|----------|-------------|
| `spec_parser.py` | FR-2 | Spec & roadmap structural data extraction |
| `structural_checkers.py` | FR-1 | 5 deterministic dimension checkers |

#### Dead Code (DELETE)

| Module | Evidence |
|--------|----------|
| `fidelity.py` (66 lines) | Zero imports across codebase; superseded by Finding + DeviationRegistry |

**Reading convention**: In all subsequent FR sections, acceptance criteria marked
`[x]` with a source reference are v3.0 baseline items (verify, do not rebuild).
Unchecked `[ ]` items require implementation.
```

### Why This Location

The Problem Statement already says "After 4 failed runs on the v3.0 release..." — the baseline section extends this by documenting what v3.0 actually delivered. A reader flows naturally from "here's the problem" (1.1) to "here's what's in/out of scope" (1.2) to "here's what already exists" (1.3) before encountering any FR.

### Interaction with ISS-001/002/003

This proposal is **complementary** to the per-FR baseline fixes in ISS-001/002/003. The global section provides the inventory; the per-FR changes provide the implementation-level detail (function lists, delta specs). Neither replaces the other:

- Without ISS-019: Per-FR baselines exist but no single overview. Implementers must read all FRs to understand the full landscape.
- Without ISS-001/002/003: Global baseline exists but individual FRs still say "create" instead of "extend."
- With both: Complete picture at both macro and micro levels.

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` | Insert Section 1.3 (~45 lines) after line 58 |

### Risk: **LOW**

- Purely additive — no existing text is modified or removed.
- Section numbering is preserved (1.3 fits naturally after 1.2).
- No FR cross-references break since no FR text changes.
- The `[x]`/`[ ]` reading convention note sets up downstream per-FR changes (ISS-001/002/003) without requiring them to already be applied.

### Requires Code Changes: **No**

Pure spec addition. All referenced code already exists.

---

## Proposal #2: Insert Section 2.5 "v3.0 Baseline" Between Goals and FRs

**Strategy**: Place the baseline section between "Clarified User Goals" (Section 2) and "Functional Requirements" (Section 3) as a bridge. This follows the pattern proposed in ISS-002 Proposal #2.

### Exact Spec Text to Add

**File**: `deterministic-fidelity-gate-requirements.md`

**Location**: Insert after line 83 (end of Section 2 / the `---` separator), before line 85 (`## 3. Functional Requirements`).

**New text**:

```markdown

## 2.5 v3.0 Baseline — Pre-Existing Implementation

> **Critical context**: This spec was drafted before v3.0 shipped. v3.0
> pre-implemented ~60% of v3.05 infrastructure. All FR sections that reference
> existing modules describe MODIFY operations, not CREATE operations.
> Verified against commit `f4d9035`.

### Pre-Existing Modules

| Module | Lines | Already Implements | v3.05 Adds |
|--------|-------|--------------------|------------|
| `convergence.py` | 323 | DeviationRegistry lifecycle, compute_stable_id(), ConvergenceResult, _check_regression(), temp dir isolation, run-to-run memory | execute_fidelity_with_convergence(), handle_regression() |
| `semantic_layer.py` | 337 | Prompt budget constants + enforcement, build_semantic_prompt(), debate scoring + verdicts, wire_debate_verdict() | validate_semantic_high(), run_semantic_layer(), TRUNCATION_MARKER heading fix |
| `remediate_executor.py` | 563 | Snapshots, allowlist, parallel ClaudeProcess agents, diff-size guard (50%), all-or-nothing rollback | MorphLLM patch format, threshold 50->30%, per-patch granularity, per-file rollback |

### Pre-Satisfied Requirements (19 items — verify only)

| Requirement | Location | FR |
|-------------|----------|----|
| ACTIVE in VALID_FINDING_STATUSES | models.py:16 | FR-6 |
| Finding.source_layer field | models.py:44 | FR-6 |
| RoadmapConfig.convergence_enabled | models.py:107 | FR-7 |
| RoadmapConfig.allow_regeneration | models.py:108 | FR-9.1 |
| --allow-regeneration CLI flag | commands.py:89-94 | FR-9.1 |
| WIRING_GATE in ALL_GATES | gates.py:944 | NFR-7 |
| SPEC_FIDELITY_GATE conditional bypass | executor.py:521 | FR-7 |
| DeviationRegistry full lifecycle | convergence.py:50-225 | FR-6 |
| compute_stable_id() | convergence.py:24-32 | FR-6 |
| ConvergenceResult dataclass | convergence.py:228-237 | FR-7 |
| _check_regression() structural-only | convergence.py:240-272 | FR-7 |
| Temp dir isolation + atexit cleanup | convergence.py:278-323 | FR-8 |
| All prompt budget constants | semantic_layer.py constants | FR-4.2 |
| build_semantic_prompt() with enforcement | semantic_layer.py | FR-4.2 |
| Debate scoring (RubricScores, score_argument, judge_verdict) | semantic_layer.py | FR-4.1 |
| Snapshot create/restore/cleanup | remediate_executor.py:53-101 | FR-9 |
| Run-to-run memory: prior findings summary | convergence.py:179-188 | FR-10 |
| Prior findings in semantic prompt | semantic_layer.py:140,215-221 | FR-10 |
| first_seen_run / last_seen_run tracking | convergence.py:104-130 | FR-10 |

### Genuinely New Code

| Component | FR | Notes |
|-----------|----|-------|
| spec_parser.py | FR-2 | New module — CREATE |
| structural_checkers.py | FR-1 | New module — CREATE |
| Severity rule tables | FR-3 | New infrastructure — no existing code |
| Section splitter | FR-5 | New logic (truncation exists, splitting does not) |
| validate_semantic_high() | FR-4.1 | New orchestrator in existing module |
| run_semantic_layer() | FR-4 | New entry point in existing module |
| execute_fidelity_with_convergence() | FR-7 | New orchestrator in existing module |
| handle_regression() | FR-8 | New flow in existing module |
| RemediationPatch dataclass | FR-9 | New dataclass in existing module |
| apply_patches() / fallback_apply() | FR-9 | New functions in existing module |

---
```

### Differences from Proposal #1

| Aspect | Proposal #1 (Section 1.3) | Proposal #2 (Section 2.5) |
|--------|--------------------------|--------------------------|
| Location | Inside Problem Statement | Between Goals and FRs |
| Framing | "Here's context about what exists" | "Here's the implementation starting point" |
| Section number | 1.3 (fits naturally) | 2.5 (non-standard half-number) |
| Includes "v3.05 Adds" column | No (defers to per-FR deltas) | Yes (preview of work per module) |
| Reading flow | Problem -> Evidence -> Scope -> Baseline -> Goals -> FRs | Problem -> Goals -> Baseline -> FRs |

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` | Insert Section 2.5 (~55 lines) after line 83 |

### Risk: **LOW-MEDIUM**

- Additive — no existing text modified.
- Section 2.5 is a non-standard number. If additional sections are later inserted between Goals and FRs, numbering may get confusing. Could use "Section 2a" or rename to "Section 3" and renumber existing FRs section to "Section 4," but that would break many cross-references.
- The "v3.05 Adds" column in the modules table duplicates information from per-FR delta sections (ISS-001/002/003), creating a minor dual-source-of-truth risk.

### Requires Code Changes: **No**

Pure spec addition.

---

## Proposal #3: Add `module_disposition` to YAML Frontmatter + Minimal Body Section

**Strategy**: Machine-parseable baseline in the frontmatter (for tooling like `/sc:roadmap` and `/sc:tasklist`) combined with a short human-readable section. Two-layer approach: tools read frontmatter, humans read the body section.

### Exact Spec Text Changes

**Change 1 — YAML Frontmatter** (after line 23, end of `relates_to` list)

INSERT:

```yaml
baseline_commit: f4d9035
module_disposition:
  - file: src/superclaude/cli/roadmap/convergence.py
    action: MODIFY
    lines: 323
    extends_frs: [FR-6, FR-7, FR-8, FR-10]
  - file: src/superclaude/cli/roadmap/semantic_layer.py
    action: MODIFY
    lines: 337
    extends_frs: [FR-4, FR-4.1, FR-4.2, FR-5]
  - file: src/superclaude/cli/roadmap/remediate_executor.py
    action: MODIFY
    lines: 563
    extends_frs: [FR-9]
  - file: src/superclaude/cli/roadmap/spec_parser.py
    action: CREATE
    extends_frs: [FR-2]
  - file: src/superclaude/cli/roadmap/structural_checkers.py
    action: CREATE
    extends_frs: [FR-1]
  - file: src/superclaude/cli/roadmap/fidelity.py
    action: DELETE
    note: "Dead code — zero imports"
pre_satisfied_count: 19
```

**Change 2 — Body section** (insert after Section 1.2, before the `---` separator)

INSERT:

```markdown

### 1.3 Implementation Baseline

This spec targets an existing codebase, not a greenfield build. See the
`module_disposition` table in the YAML frontmatter for the machine-readable
module inventory. Of the spec's requirements, 19 are already fully satisfied
by v3.0 code (commit `f4d9035`). Only modules with `action: CREATE` are
genuinely new; all others are `MODIFY` operations on existing code.

Implementers and pipeline tooling MUST consult `module_disposition` before
generating tasks. Any tool that interprets FR descriptions as CREATE
instructions for MODIFY-disposition modules is producing incorrect output.
```

### Files Affected

| File | Change |
|------|--------|
| `deterministic-fidelity-gate-requirements.md` | Add ~20 lines to YAML frontmatter + ~10 lines body section |

### Risk: **MEDIUM**

- YAML frontmatter addition is safe and additive. Non-aware parsers ignore unknown keys.
- The body section is deliberately minimal — it defers detail to the frontmatter. This means a human reader must understand YAML to get the full picture, which is a readability tradeoff.
- If `/sc:roadmap` or `/sc:tasklist` are updated to consume `module_disposition`, this becomes the most powerful option. If not, it's just metadata that sits unused.
- Does NOT include the detailed "pre-satisfied requirements" table. That detail is deferred to the per-FR `[x]` marks from ISS-001/002/003.

### Requires Code Changes: **No** (spec only)

However, for full value, the roadmap/tasklist generators should be updated to parse `module_disposition`. That is a separate enhancement, not a blocker for this spec change.

---

## Overlap Matrix: ISS-019 Proposals vs ISS-001/002/003 Proposals

| ISS-019 Proposal | Works standalone? | Best paired with ISS-001/002/003 Proposal | Redundancy risk |
|-------------------|-------------------|-------------------------------------------|-----------------|
| #1 (Section 1.3 inventory) | Yes | Per-FR minimal rewords (#1 from each) | Low — global overview + per-FR detail serve different purposes |
| #2 (Section 2.5 bridge) | Yes | Per-FR minimal rewords (#1 from each) | Medium — "v3.05 Adds" column overlaps per-FR delta lists |
| #3 (Frontmatter + minimal body) | Partial — needs per-FR detail from ISS-001/002/003 | Per-FR baseline subsections (#2 from each) | Low — machine vs human layers are complementary |

---

## Ranking Summary

| Rank | Proposal | Disruption | Self-Contained | Tooling Value | Recommendation |
|------|----------|-----------|----------------|---------------|----------------|
| 1 | **#1: Section 1.3 inventory** | Low | High | None (human-readable only) | **Best standalone fix for ISS-019** |
| 2 | **#3: Frontmatter + body** | Medium | Partial | High (machine-parseable) | Best if tooling will consume disposition data |
| 3 | **#2: Section 2.5 bridge** | Low-Medium | High | None | Good but non-standard numbering and slight redundancy with per-FR deltas |

**Recommended approach**: Proposal #1. It is purely additive, sits in the natural location (Problem Statement), is fully self-contained, and complements the per-FR fixes from ISS-001/002/003 without duplicating them. Apply ISS-001/002/003 per-FR rewords (their respective Proposal #1s) alongside ISS-019 Proposal #1 for complete coverage at both macro and micro levels.
