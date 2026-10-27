---
spec_source: "tdd-refactor-spec.md"
complexity_score: 0.53
primary_persona: architect
generated: "2026-04-03"
generator: "roadmap-opus-architect"
phases: 5
estimated_effort: "3-4 hours hands-on"
critical_path: "Line-range verification → Content migration (parallel) → BUILD_REQUEST wiring → SKILL.md reduction → Fidelity gate"
---

# TDD Skill Refactoring — Project Roadmap

## Executive Summary

This roadmap decomposes the 1,387-line TDD SKILL.md into a <500-line behavioral protocol plus 5 lazily-loaded refs files. The refactoring is procedural — extract, relocate, wire, verify — but carries meaningful fidelity risk because any textual drift silently alters agent behavior.

**Key architect concerns**:
1. The fidelity index claims 1,364 lines while the actual file is 1,387. All line ranges in the extraction and fidelity index must be re-validated before any content migration begins.
2. The adversarial-protocol refs pattern cited as precedent does not yet exist in the codebase. This refactor is pioneering the pattern, not following it.
3. The BUILD_REQUEST cross-reference wiring (FR-TDD-R.5) is the highest-risk integration point — it connects the orchestrator's output to the builder's input, and broken references cause silent Stage A.7 failures.

**Approach**: 5 phases executed sequentially with a hard quality gate between migration (Phases 1-3) and integration (Phase 4-5). No phase may begin until its predecessor's verification step passes.

---

## Phase 1: Baseline Verification & Line-Range Anchoring

**Goal**: Resolve OQ-1 (line count discrepancy) and establish verified source ranges before any content moves.

**Milestone**: Verified fidelity index with correct line ranges anchored to the actual 1,387-line file.

### Tasks

1. **Count actual SKILL.md lines** — `wc -l src/superclaude/skills/tdd/SKILL.md` must yield 1,387.
2. **Re-anchor fidelity index line ranges** — The fidelity index at `.dev/releases/backlog/tdd-skill-refactor/fidelity-index.md` uses a 1,364-line baseline. Every block range (B01–B34) must be verified against the actual 1,387-line file by checking checksum markers (first 10 / last 10 words) at the stated line ranges.
3. **Resolve OQ-5 (lines 493–536 disposition)** — The fidelity index maps B13 as lines 493–510 (behavioral, stays in SKILL.md) and B14 as lines 513–535. Verify lines 511–512 and 536 are blank/separator lines. Confirm no content falls through unmapped.
4. **Resolve OQ-2 (operational guidance range)** — Confirm lines 1246–1364 (fidelity-index basis) or the equivalent range in the 1,387-line file contains the operational guidance content. Verify no gap or overlap with validation-checklists (B25–B28).
5. **Resolve OQ-4 (frontmatter coverage)** — Confirm B01 (lines 1–4) covers the full YAML frontmatter block including the closing `---`.
6. **Produce corrected fidelity index** — Update all block ranges to the verified 1,387-line anchor. This becomes the authoritative mapping for all subsequent phases.

### Verification Gate

- Corrected fidelity index covers lines 1–1387 with zero unmapped content lines (blank/separator lines excluded).
- Every block's checksum markers (first 10 / last 10 words) match the actual file content at the stated ranges.
- OQ-1 through OQ-5 all resolved with documented answers.

### Risk Mitigation

- **Risk 5 (source length discrepancy)**: Directly addressed. No content migration proceeds until ranges are verified.

**Estimated effort**: 30-45 minutes.

---

## Phase 2: Content Migration — Parallel Extraction

**Goal**: Create the 5 refs files with verbatim content from verified source ranges.

**Milestone**: All 5 refs files exist at canonical paths with zero textual drift from source.

**Prerequisites**: Phase 1 verification gate passed.

### Tasks (parallelizable — FR-TDD-R.2, R.3, R.4, R.5, R.8 have no mutual dependencies)

These 5 tasks can execute in parallel since each extracts from non-overlapping line ranges into separate files:

1. **Create `refs/agent-prompts.md`** (FR-TDD-R.2)
   - Source: Blocks B15–B22 (lines per corrected fidelity index, originally ~537–959)
   - Destination: `src/superclaude/skills/tdd/refs/agent-prompts.md`
   - Acceptance: FR-TDD-R.2a through FR-TDD-R.2d
   - Verify: All 8 agent prompts present (Codebase, Web, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly)

2. **Create `refs/validation-checklists.md`** (FR-TDD-R.3)
   - Source: Blocks B25–B28 (lines per corrected fidelity index, originally ~1106–1245)
   - Destination: `src/superclaude/skills/tdd/refs/validation-checklists.md`
   - Acceptance: FR-TDD-R.3a through FR-TDD-R.3d
   - Verify: Checklist numbering and checkbox structure preserved exactly

3. **Create `refs/synthesis-mapping.md`** (FR-TDD-R.4)
   - Source: Blocks B23–B24 (lines per corrected fidelity index, originally ~962–1105)
   - Destination: `src/superclaude/skills/tdd/refs/synthesis-mapping.md`
   - Acceptance: FR-TDD-R.4a through FR-TDD-R.4d
   - Verify: All section headers and tables preserved verbatim

4. **Create `refs/build-request-template.md`** (FR-TDD-R.5) — **verbatim extract only, no path rewrites yet**
   - Source: Block B12 (lines per corrected fidelity index, originally ~341–492)
   - Destination: `src/superclaude/skills/tdd/refs/build-request-template.md`
   - Note: Path-reference updates deferred to Phase 3 (they depend on destination files existing)
   - Acceptance: FR-TDD-R.5a, FR-TDD-R.5b (file existence only at this stage)

5. **Create `refs/operational-guidance.md`** (FR-TDD-R.8)
   - Source: Blocks B29–B34 (lines per corrected fidelity index, originally ~1246–1387)
   - Destination: `src/superclaude/skills/tdd/refs/operational-guidance.md`
   - Acceptance: FR-TDD-R.8a through FR-TDD-R.8d
   - Verify: Zero textual drift from source

### Verification Gate

For each of the 5 files:
- File exists at `src/superclaude/skills/tdd/refs/<filename>`
- Block-wise diff against source line ranges shows zero drift (line-ending/trailing-whitespace normalization only)
- Checksum markers (first 10 / last 10 words per block) match source
- No template sentinel placeholders (`{{`, `<placeholder>`, `TODO`, `FIXME`) present

**Success Criteria addressed**: SC-2 (5/5 files exist), SC-6 (zero drift), SC-8 (no sentinels), SC-11 (8 agent prompts), SC-12 (checklist numbering).

### Risk Mitigation

- **Risk 1 (content loss)**: Block-wise extraction from verified ranges with checksum verification per block.
- **Risk 4 (semantic drift in quality gates)**: Checklist content extracted verbatim with structural diff validation.

**Estimated effort**: 45-60 minutes.

---

## Phase 3: BUILD_REQUEST Cross-Reference Wiring

**Goal**: Apply the 7 allowlisted path-reference updates to `refs/build-request-template.md`.

**Milestone**: All SKILL CONTEXT references in BUILD_REQUEST resolve to existing refs files.

**Prerequisites**: Phase 2 verification gate passed (all destination files must exist for references to resolve).

### Integration Point: BUILD_REQUEST Cross-Reference Dispatch

- **Named Artifact**: SKILL CONTEXT reference block within `refs/build-request-template.md`
- **Wired Components**: 6 path references mapping to 4 refs files:

  | Original Reference | Updated Reference |
  |---|---|
  | "Agent Prompt Templates section" | `refs/agent-prompts.md` |
  | "Synthesis Mapping Table section" | `refs/synthesis-mapping.md` |
  | "Synthesis Quality Review Checklist section" | `refs/validation-checklists.md` |
  | "Assembly Process section" | `refs/validation-checklists.md` |
  | "Validation Checklist section" | `refs/validation-checklists.md` |
  | "Content Rules section" | `refs/validation-checklists.md` |

- **Owning Phase**: Phase 3 (this phase) creates the wiring
- **Cross-Reference**: Phase 4 (SKILL.md reduction) declares load directives that cause `rf-task-builder` to consume these references at Stage A.7 runtime

### Tasks

1. **Apply the 6 path-reference updates** per FR-TDD-R.5c and FR-TDD-R.5d cross-reference map.
   - "Tier Selection section" remains pointing to SKILL.md — no update needed.
   - Each update is a targeted string replacement. No other content may change.

2. **Validate all updated references resolve** — For each of the 6 updated paths, verify the target file exists at the stated path under `src/superclaude/skills/tdd/`.

3. **Diff BUILD_REQUEST against source** — Only the 6 allowlisted path-reference changes should appear. Any other diff is a defect.

### Verification Gate

- `grep` for all 6 updated references in `refs/build-request-template.md` — all match
- `grep` for original section-name references — zero matches (all replaced)
- Full diff against source Block B12 shows exactly 6 changes and nothing else
- FR-TDD-R.5c and FR-TDD-R.5d acceptance criteria met

**Success Criteria addressed**: SC-7 (only allowlisted transformations), SC-10 (BUILD_REQUEST references resolve).

### Risk Mitigation

- **Risk 2 (cross-reference breakage)**: Closed allowlist of exactly 6 path updates. Grep validation confirms both removal of old references and presence of new ones.

**Estimated effort**: 15-20 minutes.

---

## Phase 4: SKILL.md Reduction & Phase Loading Declarations

**Goal**: Reduce SKILL.md to <500 lines by removing migrated HOW content and adding explicit refs-loading declarations.

**Milestone**: SKILL.md contains only behavioral protocol with phase-aware loading directives.

**Prerequisites**: Phases 2 and 3 verification gates passed.

### Integration Point: Phase Loading Contract Matrix

- **Named Artifact**: Per-phase loading declarations within SKILL.md (Section: Refs Loading)
- **Wired Components**:

  | Phase | Actor | Declared Loads | Forbidden Loads |
  |---|---|---|---|
  | Invocation (SKILL.md load) | Claude Code | None (SKILL.md only) | All refs files |
  | Stage A.1–A.6 | Orchestrator | None | All refs files |
  | Stage A.7 | Orchestrator | `refs/build-request-template.md` | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
  | Stage B (builder) | `rf-task-builder` | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` | `refs/build-request-template.md` |

- **Owning Phase**: Phase 4 (this phase) creates the declarations in SKILL.md
- **Cross-Reference**: Phase 3 wired the BUILD_REQUEST references that the builder follows when consuming refs

### Tasks

1. **Remove migrated content blocks from SKILL.md**:
   - Remove Block B12 (BUILD_REQUEST template, ~lines 341–492) — replaced by `Read refs/build-request-template.md` directive
   - Remove Blocks B15–B22 (agent prompts, ~lines 537–959) — replaced by builder loading `refs/agent-prompts.md`
   - Remove Blocks B23–B24 (synthesis mapping, ~lines 962–1105) — replaced by builder loading `refs/synthesis-mapping.md`
   - Remove Blocks B25–B28 (validation checklists, ~lines 1106–1245) — replaced by builder loading `refs/validation-checklists.md`
   - Remove Blocks B29–B34 (operational guidance, ~lines 1246–1387) — replaced by builder loading `refs/operational-guidance.md`

2. **Insert loading declarations in SKILL.md** (FR-TDD-R.6):
   - At Stage A.7: explicit `Read refs/build-request-template.md` directive for orchestrator (FR-TDD-R.6a)
   - At Stage B delegation or BUILD_REQUEST: explicit builder load dependencies for the 4 builder refs files (FR-TDD-R.6b)
   - Phase contract conformance table or equivalent declaring loads and forbidden loads per phase (FR-TDD-R.6c)

3. **Insert load-point replacement markers** — Where each content block was removed, insert a brief directive (e.g., `> **Loaded at runtime from** refs/agent-prompts.md`) so readers understand the delegation.

4. **Preserve all behavioral blocks** — Blocks B01–B11, B13, B14 (frontmatter, purpose, input, tier selection, output locations, execution overview, Stage A steps, Stage B delegation) remain in SKILL.md unchanged.

5. **Validate SKILL.md line count** — `wc -l` must yield strictly < 500 (FR-TDD-R.1a).

6. **Validate retained content** — FR-TDD-R.1b through FR-TDD-R.1e acceptance criteria:
   - Contains frontmatter and extended metadata
   - Contains Purpose/Input/Tier sections
   - Contains Stage A protocol and Stage B delegation protocol
   - Contains Will Do / Will Not Do boundaries
   - Contains explicit refs loading declarations

### Verification Gate

- `wc -l src/superclaude/skills/tdd/SKILL.md` < 500
- All behavioral blocks (B01–B11, B13, B14) present and unchanged
- Loading declarations satisfy FR-TDD-R.6a through FR-TDD-R.6d
- Phase contract validation: `declared_loads ∩ forbidden_loads = ∅` for every phase
- No HOW content remains in SKILL.md (no agent prompts, no checklists, no mapping tables, no BUILD_REQUEST body)

**Success Criteria addressed**: SC-1 (<500 lines), SC-9 (phase contract conformance), SC-13 (Stage A/B behavioral parity), SC-14 (invocation token reduction).

### Risk Mitigation

- **Risk 3 (wrong loading order)**: Phase contract matrix explicitly declares loads and forbidden loads. Validation rules enforced.
- **Risk 1 (content loss)**: Behavioral blocks verified present; removed blocks verified present in refs files (Phase 2 gate).

**Estimated effort**: 45-60 minutes.

---

## Phase 5: Sync, Full Fidelity Gate & Acceptance

**Goal**: Propagate to dev copies, verify full system integrity, and confirm all 14 success criteria pass.

**Milestone**: All success criteria pass. Refactoring complete.

**Prerequisites**: Phase 4 verification gate passed.

### Tasks

1. **Run `make sync-dev`** — Propagates `src/superclaude/skills/tdd/` (SKILL.md + refs/) to `.claude/skills/tdd/`.

2. **Run `make verify-sync`** — Must exit 0 with zero drift (SC-4).

3. **Verify dev copy refs existence** — `ls .claude/skills/tdd/refs/` shows all 5 files (SC-3).

4. **Full fidelity index audit** (FR-TDD-R.7):
   - Fidelity index covers lines 1–1387 with 100% coverage (SC-5, FR-TDD-R.7a)
   - Every block has destination + checksum markers verified (FR-TDD-R.7b)
   - Only allowlisted transformations applied (FR-TDD-R.7c, SC-7)
   - Forbidden transformations confirmed absent (FR-TDD-R.7d)
   - Normalized diff policy confirmed (FR-TDD-R.7e)
   - No sentinel placeholders in any output file (FR-TDD-R.7f, SC-8)

5. **Sentinel grep test** — `grep -rn '{{' src/superclaude/skills/tdd/refs/` and `grep -rn '<placeholder>' src/superclaude/skills/tdd/refs/` both return empty.

6. **BUILD_REQUEST resolution test** — All 6 updated references in `refs/build-request-template.md` point to files that exist under `src/superclaude/skills/tdd/` (SC-10).

7. **Agent prompt count audit** — `refs/agent-prompts.md` contains all 8 named prompts (SC-11).

8. **Token count comparison** — Count tokens in pre-refactor vs post-refactor SKILL.md to confirm reduction (SC-14).

9. **Behavioral parity dry run** — Invoke the TDD skill on a trivial test component and verify Stage A completes through A.7 (BUILD_REQUEST generated with correct refs paths) and Stage B delegation succeeds (SC-13).

### Full Success Criteria Checklist

| # | Criterion | Phase Verified | Method |
|---|-----------|---------------|--------|
| SC-1 | SKILL.md < 500 lines | Phase 4 | `wc -l` |
| SC-2 | 5/5 refs files in canonical location | Phase 2 | `ls` |
| SC-3 | 5/5 refs files synced to dev | Phase 5 | `ls` after `make sync-dev` |
| SC-4 | `make verify-sync` passes | Phase 5 | CI execution |
| SC-5 | Fidelity index 100% coverage | Phase 5 | Fidelity audit |
| SC-6 | Zero textual drift | Phase 2 | Block-wise diff |
| SC-7 | Only allowlisted transforms | Phase 3, 5 | Diff audit |
| SC-8 | No sentinel placeholders | Phase 2, 5 | Grep test |
| SC-9 | Phase contract conformance | Phase 4 | Matrix validation |
| SC-10 | BUILD_REQUEST refs resolve | Phase 3, 5 | Grep + file existence |
| SC-11 | 8 agent prompts present | Phase 2, 5 | Content audit |
| SC-12 | Checklist numbering preserved | Phase 2 | Structural diff |
| SC-13 | Stage A/B behavioral parity | Phase 5 | Dry run |
| SC-14 | Token reduction confirmed | Phase 5 | Token count |

### Verification Gate (Final)

- All 14 success criteria pass
- Updated fidelity index committed alongside the refactored files
- No open questions remain unresolved

**Estimated effort**: 30-45 minutes.

---

## Risk Assessment Summary

| Risk | Severity | Phase Mitigated | Mitigation Strategy |
|------|----------|----------------|---------------------|
| R1: Content loss during decomposition | HIGH | Phase 1 (range verification), Phase 2 (block-wise extraction with checksums) | Corrected fidelity index anchored to actual line count; checksum markers verified per block |
| R2: Cross-reference breakage in BUILD_REQUEST | HIGH | Phase 3 (closed allowlist wiring) | Exactly 6 path updates in closed allowlist; grep validation for old and new references |
| R3: Wrong loading order | MEDIUM | Phase 4 (phase contract matrix) | Explicit declared/forbidden load matrix with set-intersection validation |
| R4: Semantic drift in quality gates | HIGH | Phase 2 (verbatim extraction with structural diff) | Checklist numbering and checkbox structure verified via structural diff |
| R5: Source length discrepancy | MEDIUM | Phase 1 (baseline verification) | Re-anchor all ranges to verified 1,387-line count before any migration |

**Additional architect-identified risk**:

| Risk | Severity | Phase Mitigated | Mitigation Strategy |
|------|----------|----------------|---------------------|
| R6: No established refs pattern precedent | LOW | Phase 2 | The adversarial-protocol refs/ pattern does not yet exist in the repo. This refactor establishes the pattern rather than following it. Risk is low because the pattern is simple (directory of .md files loaded by Read directives), but there is no existing implementation to validate against. Document the pattern for future skill refactors. |

---

## Resource Requirements & Dependencies

### Build Tooling Dependencies

| Dependency | Required By | Validation |
|-----------|------------|------------|
| `make sync-dev` | Phase 5 (and incrementally during dev) | Must propagate new `refs/` directory and contents |
| `make verify-sync` | Phase 5 | Must detect new refs files and include them in parity check |

### Runtime Dependencies (not modified, but must continue working)

| Dependency | Used By | Constraint |
|-----------|---------|-----------|
| `/task` skill | Stage B delegation | Must not require SKILL.md refs at runtime |
| `rf-task-builder` | Stage A.7 | Must be able to Read refs files when directed by BUILD_REQUEST |
| MDTM template system | Task file creation | No changes needed |

### Artifact Dependencies

| Artifact | Location | Status |
|---------|---------|--------|
| Fidelity index | `.dev/releases/backlog/tdd-skill-refactor/fidelity-index.md` | Exists but needs re-anchoring (Phase 1) |
| TDD refactor spec | `.dev/releases/backlog/tdd-skill-refactor/tdd-refactor-spec.md` | Exists, authoritative |
| Canonical SKILL.md | `src/superclaude/skills/tdd/SKILL.md` | 1,387 lines, source of truth |

---

## Timeline Summary

| Phase | Effort | Dependencies | Key Deliverable |
|-------|--------|-------------|----------------|
| Phase 1: Baseline Verification | 30-45 min | None | Corrected fidelity index |
| Phase 2: Content Migration | 45-60 min | Phase 1 gate | 5 refs files with zero drift |
| Phase 3: BUILD_REQUEST Wiring | 15-20 min | Phase 2 gate | 6 cross-references resolved |
| Phase 4: SKILL.md Reduction | 45-60 min | Phases 2+3 gates | <500-line SKILL.md with loading declarations |
| Phase 5: Sync & Fidelity Gate | 30-45 min | Phase 4 gate | All 14 success criteria passing |
| **Total** | **~3-4 hours** | Sequential | Fully decomposed TDD skill |

---

## Open Questions Resolution Plan

| OQ | Resolution Approach | Phase |
|----|-------------------|-------|
| OQ-1 (line count: 1,387 vs 1,364) | Actual file is 1,387 lines. Re-anchor fidelity index to 1,387. | Phase 1 |
| OQ-2 (operational guidance range) | Verify B29–B34 ranges against 1,387-line file. Confirm no gap/overlap with B25–B28. | Phase 1 |
| OQ-3 (missing FR for operational-guidance) | Addressed by extraction as FR-TDD-R.8. No spec change needed. | Resolved |
| OQ-4 (frontmatter coverage) | Verify B01 range covers full YAML frontmatter. | Phase 1 |
| OQ-5 (lines 493–536 disposition) | Fidelity index maps B13 (493–510) and B14 (513–535) as behavioral blocks staying in SKILL.md. Verify gap lines are separators. | Phase 1 |
