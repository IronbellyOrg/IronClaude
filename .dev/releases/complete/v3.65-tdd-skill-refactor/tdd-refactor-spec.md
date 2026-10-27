# TDD Skill Refactoring — Release Specification

```yaml
---
title: "Decompose monolithic TDD skill into SKILL.md + refs/ architecture"
version: "1.0.0"
status: draft
feature_id: FR-TDD-REFACTOR
parent_feature: null
spec_type: refactoring
complexity_score: 0.53
complexity_class: MEDIUM
target_release: v3.8
authors: [user, claude]
created: 2026-04-02
quality_scores:
  clarity: 9.4
  completeness: 9.5
  testability: 9.3
  consistency: 9.4
  overall: 9.4
---
```

## 1. Problem Statement

The TDD skill at `/config/workspace/IronClaude/.claude/skills/tdd/SKILL.md` is monolithic and currently 1,364 lines in-repo (the master prompt cites 1,387). It mixes behavioral protocol (WHAT/WHEN) with phase-specific implementation detail (HOW): full agent prompt templates, synthesis mapping, assembly instructions, validation checklists, output structure reference, and the full BUILD_REQUEST template.

This causes avoidable token load because content needed only during specific phases is loaded up-front. It also violates the Developer Guide skill decomposition guidance: keep SKILL.md focused on behavioral protocol and move detailed HOW artifacts into refs/ files loaded lazily per wave/phase.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| Monolithic TDD skill file is 1,364 lines | `/config/workspace/IronClaude/src/superclaude/skills/tdd/SKILL.md` (canonical source of truth) | High invocation token cost; poor phase-locality |
| Full agent prompt templates inlined in SKILL.md | TDD SKILL lines 537-959 | Loaded even when only Stage A discovery is active |
| BUILD_REQUEST block inlined in SKILL.md | TDD SKILL lines 341-492 | Large template loaded outside A.7 usage |
| Validation and mapping references inlined | TDD SKILL lines 1084-1245 | No lazy loading; context noise during unrelated phases |
| Developer Guide requires refs/ lazy-loading pattern | `/config/workspace/IronClaude/docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` Sections 5.6, 9.3, 9.7 | Current structure is an identified anti-pattern |
| Reference decomposition pattern exists | `/config/workspace/IronClaude/.claude/skills/sc-adversarial-protocol/refs/` | Proven approach for large protocol skills |

### 1.2 Scope Boundary

**In scope**: Refactoring TDD skill architecture only (file decomposition, per-phase loading declarations, cross-reference updates, fidelity mapping, validation strategy).

**Out of scope**: Any semantic rewrite of prompts/checklists/rules, changes to pipeline behavior, changes to `/task` execution semantics, and any modifications to unrelated skills.

## 2. Solution Overview

Refactor the TDD skill into a behavioral SKILL.md under 500 lines plus refs/ files containing verbatim HOW content. All instructional content is preserved word-for-word; only location and cross-reference paths change.

Because strict fidelity + strict SKILL.md line budget conflict if all behavioral appendices remain inline, the refactor includes one additional refs file (`refs/operational-guidance.md`) to relocate lower-frequency guidance sections without semantic loss.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|-------------------------|-----------|
| Core decomposition | SKILL.md + refs/ | Keep monolith | Aligns to guide and enables lazy loading |
| Required refs files | agent-prompts, validation-checklists, synthesis-mapping, build-request-template | Fewer larger refs | Required by prompt; phase-local loading |
| Extra ref for line budget | Add `refs/operational-guidance.md` | Keep all behavioral appendices in SKILL.md | Ensures `<500` while preserving every line verbatim |
| Fidelity standard | Word-for-word migration | Paraphrased consolidation | Prompt explicitly requires zero semantic drift |
| Cross-references | Replace section-name references with refs paths | Keep prose-only section references | Makes dependencies auditable and phase-safe |

### 2.2 Workflow / Data Flow

```
Invocation
  -> Load SKILL.md (behavioral flow only)
     Stage A.1-A.6 uses SKILL.md only
  -> Stage A.7
     Load refs/build-request-template.md
     Builder subagent loads:
       refs/agent-prompts.md
       refs/synthesis-mapping.md
       refs/validation-checklists.md
       refs/operational-guidance.md (if referenced by build request)
  -> Stage A.8 verify task file
  -> Stage B delegates to /task
     /task executes self-contained checklist items already baked with prompts/rules
```

## 3. Functional Requirements

### FR-TDD-R.1: Decomposed SKILL.md under 500 lines with behavioral protocol only

**Description**: Refactored SKILL.md keeps invocation behavior, Stage A/B control flow, and explicit load directives; removes phase-specific HOW payloads.

**Acceptance Criteria**:
- [ ] `SKILL.md` is `<500` lines.
- [ ] Contains frontmatter, extended metadata comment, Purpose/Input/Tier sections.
- [ ] Contains Stage A protocol and Stage B delegation protocol.
- [ ] Contains Will Do / Will Not Do boundaries.
- [ ] Contains explicit refs loading declarations.

**Dependencies**: FR-TDD-R.2 through FR-TDD-R.6.

### FR-TDD-R.2: refs/agent-prompts.md with all agent templates (word-for-word)

**Description**: Move all agent prompt templates verbatim from source lines 537-959.

**Acceptance Criteria**:
- [ ] File exists at `/config/workspace/IronClaude/src/superclaude/skills/tdd/refs/agent-prompts.md`.
- [ ] After `make sync-dev`, dev copy exists at `/config/workspace/IronClaude/.claude/skills/tdd/refs/agent-prompts.md`.
- [ ] Includes Codebase, Web, Synthesis, Research Analyst, Research QA, Synthesis QA, Report Validation QA, Assembly prompts.
- [ ] Diff against source ranges shows zero textual drift.

**Dependencies**: None.

### FR-TDD-R.3: refs/validation-checklists.md with all checklists (word-for-word)

**Description**: Move synthesis quality checklist, assembly process, validation checklist, and content rules verbatim.

**Acceptance Criteria**:
- [ ] File exists at `/config/workspace/IronClaude/src/superclaude/skills/tdd/refs/validation-checklists.md`.
- [ ] After `make sync-dev`, dev copy exists at `/config/workspace/IronClaude/.claude/skills/tdd/refs/validation-checklists.md`.
- [ ] Contains source lines 1106-1245 content blocks.
- [ ] Numbering and checkbox structure preserved exactly.

**Dependencies**: None.

### FR-TDD-R.4: refs/synthesis-mapping.md with mapping table + output structure (word-for-word)

**Description**: Move output structure and synthesis mapping table verbatim from source lines 962-1105.

**Acceptance Criteria**:
- [ ] File exists at `/config/workspace/IronClaude/src/superclaude/skills/tdd/refs/synthesis-mapping.md`.
- [ ] After `make sync-dev`, dev copy exists at `/config/workspace/IronClaude/.claude/skills/tdd/refs/synthesis-mapping.md`.
- [ ] All section headers/tables preserved.
- [ ] No drift in template section numbering.

**Dependencies**: None.

### FR-TDD-R.5: refs/build-request-template.md with BUILD_REQUEST format (word-for-word)

**Description**: Move Stage A.7 BUILD_REQUEST template from source lines 341-492, with only path-reference updates required for decomposition.

**Acceptance Criteria**:
- [ ] File exists at `/config/workspace/IronClaude/src/superclaude/skills/tdd/refs/build-request-template.md`.
- [ ] After `make sync-dev`, dev copy exists at `/config/workspace/IronClaude/.claude/skills/tdd/refs/build-request-template.md`.
- [ ] BUILD_REQUEST body retained verbatim except path-reference updates in an explicit allowlist.
- [ ] SKILL CONTEXT references updated to refs files.

**Dependencies**: FR-TDD-R.2, FR-TDD-R.3, FR-TDD-R.4.

### FR-TDD-R.6: Explicit per-phase loading declarations in SKILL.md

**Description**: SKILL.md declares exactly which refs files load at each phase and by whom (orchestrator vs builder).

**Acceptance Criteria**:
- [ ] Stage A.7 declaration for build-request-template load is explicit.
- [ ] Builder load dependencies for prompts/mapping/checklists are explicit.
- [ ] No phase loads unnecessary refs.

**Dependencies**: FR-TDD-R.1.

### FR-TDD-R.7: Fidelity verification — zero content loss, zero semantic drift

**Description**: Every instructional block from original TDD skill is mapped to destination and checksum-marked.

**Acceptance Criteria**:
- [ ] Fidelity index covers all source lines 1-1364.
- [ ] Every block has destination + checksum markers (first 10 words, last 10 words).
- [ ] Allowed transformations are explicitly limited to path-reference rewrites listed in Section 12.2 and appendix allowlist.
- [ ] Forbidden transformations: wording edits, header renames, numbering changes, checklist reorder, markdown table schema changes.
- [ ] Normalized diff policy is explicit: line-ending and trailing-whitespace normalization allowed; all other textual diffs fail.
- [ ] No template sentinel placeholders remain in spec outputs.

**Dependencies**: FR-TDD-R.1 through FR-TDD-R.6.

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|--------------|
| `/config/workspace/IronClaude/src/superclaude/skills/tdd/refs/agent-prompts.md` | Canonical verbatim agent prompt templates | Referenced by A.7 builder context |
| `/config/workspace/IronClaude/src/superclaude/skills/tdd/refs/validation-checklists.md` | Canonical verbatim checklists, assembly process, content rules | Referenced by A.7 builder context |
| `/config/workspace/IronClaude/src/superclaude/skills/tdd/refs/synthesis-mapping.md` | Canonical verbatim output structure and synthesis mapping | Referenced by A.7 builder context |
| `/config/workspace/IronClaude/src/superclaude/skills/tdd/refs/build-request-template.md` | Canonical verbatim BUILD_REQUEST format | Loaded at Stage A.7 |
| `/config/workspace/IronClaude/src/superclaude/skills/tdd/refs/operational-guidance.md` | Canonical verbatim critical rules, quality signals, artifact locations, PRD-to-TDD pipeline, update/session guidance | Keeps SKILL.md under 500 lines with full fidelity |
| `/config/workspace/IronClaude/.claude/skills/tdd/refs/*` | Synced dev-copy mirrors for Claude Code runtime | Produced via `make sync-dev`; validated with `make verify-sync` |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `/config/workspace/IronClaude/src/superclaude/skills/tdd/SKILL.md` | Reduce canonical file from monolith to behavioral core, add load declarations, retain Stage A/B flow | Enforce architectural best practices and lazy loading |
| `/config/workspace/IronClaude/.claude/skills/tdd/SKILL.md` | Synced dev-copy of canonical SKILL.md | Runtime parity after `make sync-dev` |

### 4.3 Removed Files

| File/Section | Reason | Migration |
|-------------|--------|-----------|
| None | Refactor is relocation, not deletion | All content remapped to SKILL.md or refs files |

### 4.4 Module Dependency Graph

```
SKILL.md
  ├─(A.7 load)→ refs/build-request-template.md
  ├─(builder loads)→ refs/agent-prompts.md
  ├─(builder loads)→ refs/synthesis-mapping.md
  ├─(builder loads)→ refs/validation-checklists.md
  └─(on-demand reference)→ refs/operational-guidance.md

/task executes from generated task file; does not re-read SKILL.md at run phase.
```

### 4.6 Implementation Order

```
0. Edit/create canonical files under `/config/workspace/IronClaude/src/superclaude/skills/tdd/` only.
1. Create refs/build-request-template.md from source lines 341-492.
2. Create refs/agent-prompts.md from source lines 537-959.
3. Create refs/synthesis-mapping.md from source lines 962-1105.
4. Create refs/validation-checklists.md from source lines 1106-1245.
5. Create refs/operational-guidance.md from source lines 1246-1364.
6. Reduce canonical SKILL.md to behavioral core + load declarations + boundaries.
7. Run fidelity diff checks and placeholder sentinel checks against canonical `src/...` files.
8. Run `make sync-dev` to propagate canonical changes to `.claude/` dev copies.
9. Run `make verify-sync` to enforce src↔dev parity.
```

## 5. Interface Contracts

### 5.3 Phase Contracts

```yaml
phase_contracts:
  invocation:
    loads: [SKILL.md]
    forbidden_loads: [refs/build-request-template.md, refs/agent-prompts.md, refs/synthesis-mapping.md, refs/validation-checklists.md, refs/operational-guidance.md]
    constraints:
      - "Behavioral protocol only"

  stage_a_1_to_a_6:
    loads: [SKILL.md]
    forbidden_loads: [refs/build-request-template.md, refs/agent-prompts.md, refs/synthesis-mapping.md, refs/validation-checklists.md, refs/operational-guidance.md]
    constraints:
      - "No refs pre-load"

  stage_a_7:
    orchestrator_loads:
      - refs/build-request-template.md
    builder_loads:
      - refs/agent-prompts.md
      - refs/synthesis-mapping.md
      - refs/validation-checklists.md
      - refs/operational-guidance.md
    forbidden_loads: []
    ordering:
      - "Build request template loaded before builder spawn"
      - "Builder reads refs before task file generation"
      - "Contract rule: if loaded_ref not in declared loads, phase fails"

  stage_a_8:
    loads: [SKILL.md]
    forbidden_loads: [refs/agent-prompts.md, refs/synthesis-mapping.md, refs/validation-checklists.md, refs/operational-guidance.md]
    constraints:
      - "Task-file structural verification only"

  stage_b:
    loads: [task skill + generated task file]
    forbidden_loads: [refs/build-request-template.md, refs/agent-prompts.md, refs/synthesis-mapping.md, refs/validation-checklists.md, refs/operational-guidance.md]
    constraints:
      - "No direct refs load required during checklist execution"

contract_validation_rule:
  - "declared_loads ∩ forbidden_loads = ∅ for every phase"
  - "runtime_loaded_refs ⊆ declared_loads for every phase"
```

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-TDD-R.1 | Invocation token efficiency | Remove phase-specific payload from baseline invocation | Compare pre/post SKILL.md token footprint |
| NFR-TDD-R.2 | Deterministic fidelity | Zero textual drift in migrated verbatim blocks | Block-wise diff checks against source ranges |
| NFR-TDD-R.3 | Loading discipline | No unnecessary refs outside declared phases | Contract conformance audit |
| NFR-TDD-R.4 | Maintainability | Clear file ownership by concern | Auditable source-to-destination mapping table |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Content loss during decomposition | Medium | High | Word-for-word fidelity index + block-level checksum markers |
| Cross-reference breakage in BUILD_REQUEST | Medium | High | Explicit cross-reference update matrix + grep validation |
| Wrong loading order | Low | Medium | Phase-to-ref contract with explicit load ordering |
| Semantic drift in quality gates | Low | High | Checklist numbering/content diff validation |
| Source length discrepancy (1387 vs 1364) causes mapping ambiguity | Medium | Medium | Anchor mapping to actual in-repo line count 1364 and record discrepancy explicitly |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| Block fidelity diff test | refs files vs original line ranges | Verbatim migration of prompts/checklists/tables; fail on non-allowlisted diffs |
| SKILL budget test | refactored canonical SKILL.md | `<500` line requirement with minimum structural sections present |
| Placeholder sentinel test | both generated spec files | Zero template sentinel placeholders remain |
| Transformation allowlist test | migrated files + exception log | Only Section 12.2 path-reference rewrites are allowed |
| Normalized diff policy test | source vs migrated blocks | Only line-ending/trailing-whitespace normalization permitted |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| Phase loading matrix test | Each phase loads only declared refs and no forbidden refs |
| BUILD_REQUEST reference resolution test | All section-name references replaced with concrete refs paths |
| Sync integrity test | `make sync-dev` creates expected `.claude/skills/tdd/` mirrors |
| Sync verification test | `make verify-sync` passes with no src↔dev drift |
| Functional parity dry run | Stage A/B behavior preserved (no execution semantics changed) with deterministic checklist gate expectations |

### 8.3 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| Fidelity audit | Sample every migrated block using checksum markers | First/last markers and content match source |
| Structural audit | Open SKILL.md + refs directory | Correct decomposition and load declarations present |
| Command-level spec review | Run `/sc:spec-panel` and reflection passes on this release spec | No critical architecture/fidelity gaps found |

## 9. Migration & Rollout

- **Breaking changes**: None; external skill interface remains unchanged.
- **Backwards compatibility**: Preserved; Stage B still delegates to `/task` and task items remain self-contained.
- **Rollback plan**: Revert to monolithic SKILL.md via git.
- **Migration path**: Single refactor commit plus sync/verify pass (`make sync-dev`, `make verify-sync`) after implementation.

## 10. Downstream Inputs

### For sc:roadmap
Provide this spec as a refactor initiative under v3.8 with no behavioral feature delta.

### For sc:tasklist
Generate implementation tasks directly from Section 4.6 order and Section 8 test requirements.

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OI-01 | Resolved: `refs/operational-guidance.md` is mandatory in canonical source and synced dev copy for line-budget/fidelity compliance. | None | 2026-04-03 |
| OI-02 | Resolved: Artifact Locations canonical content lives in `refs/operational-guidance.md`; SKILL.md keeps concise pointer-only summary. | None | 2026-04-03 |

## 12. Brainstorm Gap Analysis

### 12.1 Content Block Inventory Appendix

Complete inventory is in `/config/workspace/IronClaude/.dev/releases/backlog/tdd-skill-refactor/fidelity-index.md` with source ranges and destinations for all blocks B01-B34.

### 12.2 Cross-Reference Map Appendix

Required BUILD_REQUEST path updates (source block B12):

| Legacy Reference in SKILL.md | New Reference |
|-----------------------------|---------------|
| Agent Prompt Templates section | `refs/agent-prompts.md` |
| Synthesis Mapping Table section | `refs/synthesis-mapping.md` |
| Synthesis Quality Review Checklist section | `refs/validation-checklists.md` |
| Assembly Process section | `refs/validation-checklists.md` |
| Validation Checklist section | `refs/validation-checklists.md` |
| Content Rules section | `refs/validation-checklists.md` |
| Tier Selection section | Remains in SKILL.md |

### 12.3 Fidelity Manifest Appendix

Fidelity manifest is the companion index file with:
- source line ranges,
- destination file,
- phase dependency,
- first 10 words + last 10 words checksum markers.

### 12.4 Gap Summary

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|------------------|---------|
| GAP-TDD-01 | Source prompt cites 1,387 lines, repository file is 1,364 lines | Medium | Problem statement, fidelity accounting | analyzer |
| GAP-TDD-02 | `<500` SKILL requirement conflicts with preserving all inline appendices | Medium | Architecture | architect |

Resolved strategy: preserve all content via additional refs file while keeping SKILL behavioral and under budget.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Behavioral protocol | WHAT/WHEN instructions that stay in SKILL.md |
| HOW content | Detailed templates/checklists/prompts moved to refs/ |
| BUILD_REQUEST | Stage A.7 template used to spawn rf-task-builder |
| Fidelity index | Block-by-block preservation manifest with checksum markers |
| Semantic drift | Meaning change introduced by non-verbatim edits |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `/config/workspace/IronClaude/src/superclaude/skills/tdd/SKILL.md` | Canonical source artifact being decomposed |
| `/config/workspace/IronClaude/.claude/skills/tdd/SKILL.md` | Synced dev-copy runtime mirror after `make sync-dev` |
| `/config/workspace/IronClaude/docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Skill architecture rules and anti-pattern guidance |
| `/config/workspace/IronClaude/.claude/skills/sc-adversarial-protocol/SKILL.md` | Structural reference pattern |
| `/config/workspace/IronClaude/.claude/skills/sc-adversarial-protocol/refs/agent-specs.md` | refs decomposition example |
| `/config/workspace/IronClaude/.claude/skills/sc-adversarial-protocol/refs/artifact-templates.md` | refs decomposition example |
| `/config/workspace/IronClaude/.claude/skills/sc-adversarial-protocol/refs/debate-protocol.md` | refs decomposition example |
| `/config/workspace/IronClaude/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` | refs decomposition example |
| `/config/workspace/IronClaude/src/superclaude/examples/release-spec-template.md` | Base release spec template |
| `/config/workspace/IronClaude/.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec.md` | Pattern parity reference |
| `/config/workspace/IronClaude/.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` | Fidelity index style reference |
