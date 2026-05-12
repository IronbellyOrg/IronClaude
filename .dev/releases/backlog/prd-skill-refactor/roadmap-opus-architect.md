---
spec_source: "prd-refactor-spec-v2.md"
complexity_score: 0.45
primary_persona: architect
generated: "2026-04-03"
generator: "roadmap-agent/opus-4.6/architect"
total_phases: 4
total_milestones: 7
estimated_effort: "2-4 hours implementation + 1 hour verification"
critical_path: "Phase 1 → Phase 2 → Phase 3 → Phase 4 (linear with one parallel step)"
---

# PRD Skill Refactoring — Project Roadmap

## 1. Executive Summary

This roadmap decomposes the monolithic PRD skill (1,369-line SKILL.md) into the mandated three-tier architecture: thin command layer → behavioral SKILL.md → lazy-loaded refs/. The refactoring addresses two Developer Guide violations: the 500-line SKILL.md ceiling (exceeded 2.7x) and the missing command layer.

**Current state**: 3 of 4 refs/ files already exist from a partial v1 implementation. SKILL.md has not been trimmed. No command file exists. Content is duplicated between SKILL.md and existing refs/.

**Target state**: 6 files totaling 1,380-1,520 lines with zero content loss, ~60% token reduction on invocation, and full three-tier compliance.

**Risk profile**: MEDIUM. The primary risk is content fidelity during decomposition — not technical complexity. All verification is mechanical (diff, grep, wc). No runtime behavior changes.

---

## 2. Phased Implementation Plan

### Phase 1: Foundation Verification (Verify Existing Artifacts)

**Objective**: Confirm the 3 existing refs/ files are faithful to the original SKILL.md before building on them.

**Rationale**: The v1 implementation created refs/ files but never trimmed SKILL.md. These files may have drifted during intervening edits. Building on unfaithful refs/ would propagate errors into the final structure. This phase is a prerequisite for all subsequent work.

| Step | Task | Requirements Addressed | Verification |
|------|------|----------------------|--------------|
| 1.1 | Diff `refs/agent-prompts.md` against SKILL.md lines 553-967 | FR-PRD-R.2b, FR-PRD-R.2e | Zero content delta (whitespace normalization permitted) |
| 1.2 | Diff `refs/validation-checklists.md` against SKILL.md lines 1108-1254 | FR-PRD-R.3b-FR-PRD-R.3g | Zero content delta |
| 1.3 | Diff `refs/synthesis-mapping.md` against SKILL.md lines 969-1106 | FR-PRD-R.4b-FR-PRD-R.4e | Zero content delta |
| 1.4 | Verify `refs/agent-prompts.md` contains all 8 named templates | FR-PRD-R.2b | Grep for 8 template headers |
| 1.5 | Verify `refs/agent-prompts.md` includes "Common web research topics" list | FR-PRD-R.2d | Grep for list at original lines 679-686 |
| 1.6 | Verify `refs/validation-checklists.md` includes all 4 subsections | FR-PRD-R.3b-FR-PRD-R.3e | Grep for section headers: Synthesis Quality Review, Assembly Process, Validation Checklist, Content Rules |
| 1.7 | If drift found in any ref: re-extract from current SKILL.md (Risk 5 mitigation) | FR-PRD-R.7 | Re-diff after correction |

**Milestone M1**: All 3 existing refs/ files verified faithful to original SKILL.md.

**Exit criteria**: Each of the 3 diffs shows zero content changes. All structural checks pass.

**Estimated effort**: 30-45 minutes.

---

### Phase 2: Create Missing Artifacts (Command File + Build Request Ref)

**Objective**: Create the two files that don't yet exist: `commands/sc/prd.md` and `refs/build-request-template.md`.

**Dependency**: Phase 1 must complete (refs/ paths must be confirmed before BUILD_REQUEST references can point to them).

**Parallelism**: Steps 2.1 and 2.2 are independent and can execute concurrently.

#### Step 2.1: Create `refs/build-request-template.md`

| Sub-step | Task | Requirements Addressed |
|----------|------|----------------------|
| 2.1.1 | Extract SKILL.md lines 347-508 into `refs/build-request-template.md` | FR-PRD-R.5a, FR-PRD-R.5b |
| 2.1.2 | Add file header explaining purpose and loading context | FR-PRD-R.5a |
| 2.1.3 | Update 6 SKILL CONTEXT FILE references per mapping: | FR-PRD-R.5c |
| | — `"Agent Prompt Templates" section` → `refs/agent-prompts.md` | |
| | — `"Synthesis Mapping Table" section` → `refs/synthesis-mapping.md` | |
| | — `"Synthesis Quality Review Checklist" section` → `refs/validation-checklists.md` | |
| | — `"Assembly Process" section` → `refs/validation-checklists.md (Assembly Process section)` | |
| | — `"Validation Checklist" section` → `refs/validation-checklists.md (Validation Checklist section)` | |
| | — `"Content Rules" section` → `refs/validation-checklists.md (Content Rules section)` | |
| 2.1.4 | Confirm `"Tier Selection" section` reference unchanged | FR-PRD-R.5d |
| 2.1.5 | Diff against original lines 347-508; confirm exactly 6 path changes | FR-PRD-R.5f |

#### Step 2.2: Create `commands/sc/prd.md`

| Sub-step | Task | Requirements Addressed |
|----------|------|----------------------|
| 2.2.1 | Scaffold command file using `adversarial.md` template structure | FR-PRD-R.0 |
| 2.2.2 | Write frontmatter: `name: prd`, `category: documentation`, `complexity: advanced`, etc. | FR-PRD-R.0a |
| 2.2.3 | Write `## Required Input` section documenting `<product>` positional argument | FR-PRD-R.0b |
| 2.2.4 | Write `## Usage` section with invocation patterns | FR-PRD-R.0c |
| 2.2.5 | Write `## Arguments` section for `<product>` | FR-PRD-R.0d |
| 2.2.6 | Write `## Options` table with 7 flags: `<product>`, `--tier`, `--resume`, `--output`, `--scope`, `--focus`, `--purpose` | FR-PRD-R.0e |
| 2.2.7 | Migrate Tier Selection table (B04, SKILL.md lines 79-85) into `--tier` flag documentation | FR-PRD-R.0e, FR-PRD-R.8b |
| 2.2.8 | Write `## Behavioral Summary` (one paragraph, no protocol details) | FR-PRD-R.0f |
| 2.2.9 | Migrate Effective Prompt Examples (B03, SKILL.md lines 46-60) into `## Examples` section; add resume and tier-override examples | FR-PRD-R.0g, FR-PRD-R.8a |
| 2.2.10 | Write `## Activation` section: `Skill prd` invocation + "Do NOT proceed" warning | FR-PRD-R.0h |
| 2.2.11 | Write `## Boundaries` section with Will/Will Not lists | FR-PRD-R.0i |
| 2.2.12 | Write `## Related Commands` table referencing `/tdd`, `/sc:workflow`, `/sc:design`, `/sc:brainstorm` | FR-PRD-R.0j |
| 2.2.13 | Verify line count is 100-170 lines | FR-PRD-R.0k |
| 2.2.14 | Verify command contains zero protocol logic | FR-PRD-R.0l |

**Milestone M2**: `refs/build-request-template.md` created with exactly 6 path changes.
**Milestone M3**: `commands/sc/prd.md` created at 100-170 lines following adversarial.md pattern.

**Exit criteria**: Both files exist, pass line count checks, and contain the correct content per their respective FR requirements.

**Estimated effort**: 1-1.5 hours (parallel execution of 2.1 and 2.2).

---

### Phase 3: SKILL.md Decomposition (Trim + Wire)

**Objective**: Remove content from SKILL.md that now lives in refs/ or the command file. Add per-phase loading declarations. Merge B30 into B05.

**Dependency**: Phase 2 must complete (command file must exist before removing migrated content; all refs/ paths must be finalized before writing loading declarations).

| Step | Task | Requirements Addressed |
|------|------|----------------------|
| 3.1 | Remove agent prompt templates (lines 553-967, ~415 lines) | FR-PRD-R.1c |
| 3.2 | Remove validation checklists + assembly process + content rules (lines 1108-1254, ~147 lines) | FR-PRD-R.1c |
| 3.3 | Remove output structure + synthesis mapping (lines 969-1106, ~137 lines) | FR-PRD-R.1c |
| 3.4 | Remove BUILD_REQUEST template (lines 347-508, ~162 lines) | FR-PRD-R.1c |
| 3.5 | Remove Effective Prompt Examples (lines 46-60, ~15 lines) — now in command | FR-PRD-R.8a, FR-PRD-R.8c |
| 3.6 | Remove Tier Selection table header rows (lines 79-85, ~7 lines) — table now in command; retain selection rules (lines 87-92) | FR-PRD-R.8b, FR-PRD-R.8d |
| 3.7 | Merge B30 (duplicate Artifact Locations) into B05 (Output Locations): append B30's 6 QA paths to B05's table, delete standalone B30 section | FR-PRD-R.1f |
| 3.8 | Add Stage A.7 loading declaration: orchestrator loads `refs/build-request-template.md` | FR-PRD-R.6a |
| 3.9 | Add Stage A.7 loading declaration: builder subagent loads `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` | FR-PRD-R.6b |
| 3.10 | Verify no other phase loads refs/ files (A.1-A.6 use SKILL.md only; Stage B delegates to /task) | FR-PRD-R.6c |
| 3.11 | Verify orchestrator loads at most 2 files simultaneously | FR-PRD-R.6d |
| 3.12 | Update all internal cross-references: section-name references → refs/ file paths | FR-PRD-R.1e |
| 3.13 | Grep for stale "section" references — must find zero (except "Tier Selection" which stays) | Risk 2 mitigation |
| 3.14 | Verify SKILL.md line count is 400-500 lines | FR-PRD-R.1a |
| 3.15 | Verify no content appears in BOTH command file and SKILL.md (except cross-references) | FR-PRD-R.8e |

**Milestone M4**: SKILL.md trimmed to 400-500 lines with loading declarations.
**Milestone M5**: Zero stale cross-references; no content duplication between command and skill.

**Exit criteria**: `wc -l SKILL.md` returns 400-500. Grep for stale section references returns zero matches. FR-PRD-R.1a through FR-PRD-R.1f all pass.

**Estimated effort**: 1-1.5 hours.

#### Integration Points — Dispatch/Wiring Mechanisms

| Named Artifact | Mechanism Type | Wired Components | Owning Phase | Consuming Phase(s) |
|---------------|---------------|------------------|-------------|-------------------|
| **A.7 Orchestrator Loading Declaration** | Explicit file-load directive in SKILL.md | `refs/build-request-template.md` | Phase 3 (Step 3.8) | Runtime: Stage A.7 orchestrator context |
| **A.7 Builder Subagent Loading Declaration** | Explicit file-load directive in SKILL.md | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` | Phase 3 (Step 3.9) | Runtime: rf-task-builder subagent context |
| **BUILD_REQUEST SKILL CONTEXT FILE references** | Cross-reference path table inside `refs/build-request-template.md` | 6 refs/ path entries replacing section-name strings | Phase 2 (Step 2.1.3) | Runtime: builder subagent reads BUILD_REQUEST and follows paths to load refs/ |
| **Command Activation handoff** | `Skill prd` invocation in `## Activation` section | `prd` skill (SKILL.md) | Phase 2 (Step 2.2.10) | Runtime: `/sc:prd` command triggers skill load |
| **Stage B → /task delegation** | Existing delegation in SKILL.md (unchanged) | `/task` skill reads task file | Not modified (pre-existing) | Runtime: Stage B execution |

---

### Phase 4: Fidelity Verification + Sync + Acceptance

**Objective**: Prove zero content loss, sync to src/, and validate end-to-end behavior.

**Dependency**: Phase 3 must complete.

| Step | Task | Requirements Addressed |
|------|------|----------------------|
| 4.1 | Diff each of 8 agent prompt templates (refs/ vs original SKILL.md ranges) | FR-PRD-R.7b |
| 4.2 | Diff each checklist/table (refs/ vs original) | FR-PRD-R.7c |
| 4.3 | Diff output structure + synthesis mapping (refs/ vs original) | FR-PRD-R.7d |
| 4.4 | Diff BUILD_REQUEST: confirm only 6 documented path changes | FR-PRD-R.7e |
| 4.5 | Grep command file for B03 examples; grep SKILL.md to confirm absent | FR-PRD-R.7f |
| 4.6 | Grep command file for B04 tier table; grep SKILL.md to confirm absent | FR-PRD-R.7g |
| 4.7 | Compute combined line count across all 6 files; verify 1,380-1,520 | FR-PRD-R.7h |
| 4.8 | Update fidelity index with B03/B04 command-layer destinations | FR-PRD-R.7a |
| 4.9 | Verify refs/ contains exactly 4 .md files | Success Criterion 4 |
| 4.10 | `make sync-dev` — propagate .claude/ → src/superclaude/ | Success Criterion 11 |
| 4.11 | `make verify-sync` — confirm both sides match | Success Criterion 11 |
| 4.12 | Invoke `/sc:prd` and confirm `Skill prd` triggers correctly | Success Criterion 12 |
| 4.13 | E2E test: invoke skill on a test product; compare output structure to baseline | NFR-PRD-R.4, Success Criterion 10 |

**Milestone M6**: All fidelity diffs pass. Combined line count within range.
**Milestone M7**: `make verify-sync` passes. `/sc:prd` activation confirmed.

**Exit criteria**: All 12 success criteria pass. Zero content loss verified. Sync clean.

**Estimated effort**: 45-60 minutes.

---

## 3. Risk Assessment and Mitigation Strategies

| # | Risk | Severity | Phase Exposed | Mitigation | Contingency |
|---|------|----------|--------------|------------|-------------|
| R1 | Content loss during SKILL.md trimming | HIGH | Phase 3 | Fidelity index with first/last 10-word markers. Phase 4 diffs every block. Never delete without confirming destination exists. | Re-extract from git history (`git show HEAD:path`) |
| R2 | Cross-reference breakage in BUILD_REQUEST | HIGH | Phase 2, Phase 3 | Cross-reference map enumerates all 6 changes. Post-trim grep for stale "section" references. | Grep-based sweep catches any missed reference |
| R3 | Command file incorrect Activation | HIGH | Phase 2 | Use exact pattern from adversarial.md. Phase 4 manual invocation test. | Single-line fix if pattern is wrong |
| R4 | Scope creep — improving content during migration | MEDIUM | Phase 2, Phase 3 | Strict rule: zero content changes except documented migrations. Phase 4 diffs catch violations. | Revert to original and re-extract |
| R5 | Existing refs/ files drifted from SKILL.md | MEDIUM | Phase 1 | Phase 1 exists specifically to catch this. Diff all 3 files before proceeding. | Re-extract from current SKILL.md |
| R6 | Prompt examples lose context when moved | MEDIUM | Phase 2 | Examples are self-contained strings. Command's Examples section provides framing. | Add brief contextual note in command if needed |
| R7 | Tier table/selection rules drift | MEDIUM | Phase 2, Phase 3 | Table is reference (command); rules are behavioral (skill). FR-PRD-R.8e ensures no duplication. | Cross-reference note in both files |
| R8 | Builder subagent can't find refs/ paths | MEDIUM | Phase 3 | Paths are relative to SKILL.md directory. Phase 4 E2E test catches resolution failures. | Adjust paths in BUILD_REQUEST if needed |
| R9 | B30→B05 merge loses QA report paths | LOW | Phase 3 | Append B30's 6 paths to B05's table. Diff verifies all rows present. | Re-extract B30 from git history |

---

## 4. Resource Requirements and Dependencies

### External Dependencies

| Dependency | Type | Required By | Risk if Unavailable |
|-----------|------|------------|-------------------|
| `adversarial.md` (167 lines) | Template | Phase 2 (command scaffolding) | LOW — structure is well-documented in spec; template is convenience |
| Original `SKILL.md` (1,369 lines) | Source content | All phases | CRITICAL — must not be modified until Phase 3 |
| Fidelity index | Verification artifact | Phase 1, Phase 4 | MEDIUM — can reconstruct from SKILL.md but adds effort |
| `make sync-dev` | Build tool | Phase 4 | LOW — manual copy is fallback |
| `make verify-sync` | Build tool | Phase 4 | LOW — manual diff is fallback |
| `rf-task-builder` agent | Runtime dependency | Phase 4 (E2E test) | MEDIUM — E2E test validates builder can resolve refs/ paths |
| `/task` skill | Runtime dependency | Phase 4 (E2E test) | LOW — unchanged by refactoring |

### Tools Required

- Text editor with diff capability
- `wc -l` for line counts
- `grep` for content verification and stale reference detection
- `diff` for fidelity verification
- `make sync-dev` and `make verify-sync` for component sync
- Git for version control and rollback capability

### Prerequisite Knowledge

- SuperClaude three-tier architecture (Command → Skill → refs/)
- PRD skill execution flow (Stage A scope discovery → Stage B task execution)
- `adversarial.md` command structure (gold-standard template)
- Fidelity index block-to-destination mapping

---

## 5. Success Criteria and Validation Approach

### Automated Validation (Phase 4)

| # | Criterion | Threshold | Test Command | Pass/Fail |
|---|-----------|-----------|-------------|-----------|
| SC-1 | SKILL.md line count | 400-500 | `wc -l .claude/skills/prd/SKILL.md` | Lines in range |
| SC-2 | Command file line count | 100-170 | `wc -l .claude/commands/sc/prd.md` | Lines in range |
| SC-3 | SKILL.md token budget | ≤ 2,000 | Line count × ~4.5 | Estimated ≤ 2,025 |
| SC-4 | refs/ file count | Exactly 4 .md | `ls .claude/skills/prd/refs/*.md \| wc -l` | Count = 4 |
| SC-5 | Agent prompt fidelity | Zero changes across 8 templates | Diff refs/agent-prompts.md vs original ranges | No delta |
| SC-6 | BUILD_REQUEST fidelity | Exactly 6 path changes | Diff refs/build-request-template.md vs original | 6 changes only |
| SC-7 | Content migration | B03 in command, absent from SKILL.md | Grep both files | Present/absent confirmed |
| SC-8 | Stale references | Zero (except "Tier Selection") | `grep -n '".*section"' SKILL.md refs/` | No stale matches |
| SC-9 | Combined line count | 1,380-1,520 | Sum of `wc -l` across 6 files | In range |
| SC-10 | Behavioral regression | Identical output structure | E2E invocation comparison | Match |
| SC-11 | Sync verification | Clean | `make verify-sync` | Exit 0 |
| SC-12 | Activation correctness | Skill loads | `/sc:prd test-product` | Skill triggers |

### Validation Approach

**Strategy**: Defense-in-depth with three verification layers.

1. **Per-step verification** (during Phases 1-3): Each step includes its own check (diff, grep, wc). Issues caught immediately, before they compound.

2. **Fidelity sweep** (Phase 4, Steps 4.1-4.8): Systematic diff of every content block against original SKILL.md. Catches any content loss or semantic drift that per-step checks missed.

3. **End-to-end validation** (Phase 4, Steps 4.12-4.13): Invoke the refactored skill and verify identical behavior. Catches integration issues (broken activation, path resolution, loading failures).

**Rollback plan**: Single `git checkout -- .claude/skills/prd/ .claude/commands/sc/prd.md` restores pre-refactoring state. No data migration, no schema changes, no external system state to unwind.

---

## 6. Timeline Estimates Per Phase

| Phase | Description | Est. Effort | Dependencies | Parallelism |
|-------|------------|-------------|-------------|-------------|
| **Phase 1** | Foundation Verification | 30-45 min | None | Steps 1.1-1.3 can run in parallel |
| **Phase 2** | Create Missing Artifacts | 1-1.5 hrs | Phase 1 | Steps 2.1 and 2.2 can run in parallel |
| **Phase 3** | SKILL.md Decomposition | 1-1.5 hrs | Phase 2 | Steps 3.1-3.6 sequential (order matters for line tracking) |
| **Phase 4** | Fidelity + Sync + Acceptance | 45-60 min | Phase 3 | Steps 4.1-4.7 can run in parallel |
| **Total** | | **3.25-4.75 hrs** | | |

### Critical Path

```
Phase 1 (verify refs/) → Phase 2 (create command + build-request ref) → Phase 3 (trim SKILL.md) → Phase 4 (verify + sync)
```

The critical path is strictly linear. Phase 2 has internal parallelism (command file and build-request ref are independent). Phase 4 has internal parallelism (diffs are independent). But each phase gate must pass before the next begins.

### Milestone Summary

| Milestone | Phase | Gate Condition |
|-----------|-------|---------------|
| M1: Existing refs verified | Phase 1 | 3 diffs clean |
| M2: build-request-template.md created | Phase 2 | Exactly 6 path changes |
| M3: prd.md command created | Phase 2 | 100-170 lines, adversarial pattern |
| M4: SKILL.md trimmed | Phase 3 | 400-500 lines |
| M5: Cross-references clean | Phase 3 | Zero stale references |
| M6: Fidelity verified | Phase 4 | All diffs pass, combined lines 1,380-1,520 |
| M7: Sync + activation confirmed | Phase 4 | `make verify-sync` passes, `/sc:prd` triggers |

---

## 7. Implementation Order Summary

```
1. Verify existing refs/ fidelity          [Phase 1 — blocking gate]
   ├── Diff agent-prompts.md               [parallel]
   ├── Diff validation-checklists.md       [parallel]
   └── Diff synthesis-mapping.md           [parallel]

2. Create missing artifacts                [Phase 2 — after Phase 1]
   ├── Create refs/build-request-template.md   [parallel with 2b]
   └── Create commands/sc/prd.md               [parallel with 2a]

3. Trim SKILL.md                           [Phase 3 — after Phase 2]
   ├── Remove 4 content blocks (~860 lines)
   ├── Remove 2 migrated interface blocks (~22 lines)
   ├── Merge B30 into B05
   ├── Add A.7 loading declarations
   └── Update cross-references

4. Verify + Sync + Accept                  [Phase 4 — after Phase 3]
   ├── Fidelity diffs (all blocks)         [parallel]
   ├── Structural checks (line counts)     [parallel]
   ├── make sync-dev + make verify-sync
   └── E2E activation + behavior test
```
