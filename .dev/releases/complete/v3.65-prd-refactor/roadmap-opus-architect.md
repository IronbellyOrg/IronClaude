---
spec_source: "prd-refactor-spec.md"
complexity_score: 0.45
primary_persona: architect
generated: "2026-04-03"
generator: "claude-opus-4-6-roadmap-architect"
phases: 4
total_tasks: 18
estimated_effort: "4-6 hours implementation + 1-2 hours verification"
---

# PRD Skill Refactoring — Project Roadmap

## Executive Summary

This roadmap decomposes the monolithic PRD `SKILL.md` (1,373 lines, ~5,000+ tokens on invocation) into a properly architected multi-file skill following the `sc-adversarial-protocol` refs/ pattern. The refactoring produces a 430–500 line `SKILL.md` (behavioral protocol only) plus 4 `refs/` files (HOW content loaded per-phase), achieving ~60% token reduction on invocation with zero behavioral regression.

**Complexity**: MEDIUM (0.45) — high-precision mechanical decomposition with well-defined boundaries and a reference implementation to follow.

**Critical constraint**: Word-for-word content preservation. This is a structural relocation, not a rewrite. Every line of instructional content must appear in exactly one destination file with zero semantic drift.

**Architectural pattern**: Follows the established `sc-adversarial-protocol` refs/ lazy-loading architecture — `SKILL.md` as behavioral spine with `See refs/...` cross-references, refs/ files loaded only when needed per execution phase.

---

## Phase 1: Preparation & Validation (Pre-Implementation)

**Goal**: Confirm all prerequisites exist and the implementation environment is stable.

**Milestone**: Green light to begin content extraction.

### Tasks

1.1. **Verify fidelity index completeness**
   - Confirm `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` exists and covers all 30 content blocks (B01–B30)
   - Validate that every block has: line range, type classification, destination, first/last 10-word markers
   - Cross-check block line ranges against current SKILL.md (1,373 lines) — confirm no gaps or overlaps

1.2. **Freeze SKILL.md baseline**
   - Record current SKILL.md SHA: `git hash-object .claude/skills/prd/SKILL.md`
   - Confirm no pending changes to SKILL.md on current branch
   - This addresses Risk #7 (spec freshness) — implementation must proceed against this exact baseline

1.3. **Create feature branch and refs/ directory**
   - Branch from current HEAD: `git checkout -b refactor/prd-skill-decompose`
   - Create directory: `.claude/skills/prd/refs/`
   - Confirm `src/superclaude/skills/prd/refs/` will be created during sync

1.4. **Verify reference implementation accessibility**
   - Confirm `.claude/skills/sc-adversarial-protocol/refs/` pattern is readable
   - Note the cross-reference syntax used: `See refs/filename.md` inline references

### Exit Criteria
- [ ] Fidelity index verified complete (all blocks mapped, no line gaps)
- [ ] SKILL.md baseline SHA recorded
- [ ] Feature branch created with empty `refs/` directory
- [ ] Reference implementation pattern confirmed

---

## Phase 2: Content Extraction — Create refs/ Files

**Goal**: Extract HOW content from SKILL.md into 4 refs/ files with word-for-word fidelity.

**Milestone**: All 4 refs/ files created, each passing diff verification against original line ranges.

**Sequencing rationale**: refs/ files are created first because FR-PRD-R.5 (build-request-template) depends on knowing the destination file paths from FR-PRD-R.2, FR-PRD-R.3, and FR-PRD-R.4. Extract the dependency-free files first, then the file with cross-reference updates.

### Tasks

2.1. **Create `refs/agent-prompts.md`** (FR-PRD-R.2)
   - Extract blocks B14–B21 (lines 553–967): all 8 agent prompt templates
   - Add header explaining purpose and loading context
   - Include section header + introductory paragraph (lines 553–557)
   - Include "Common web research topics for PRDs" list (lines 679–686)
   - **Verification**: Diff each of 8 templates against original line ranges — zero content changes (whitespace normalization only)
   - **Expected size**: ~415 lines

2.2. **Create `refs/synthesis-mapping.md`** (FR-PRD-R.4)
   - Extract blocks B22–B23 (lines 969–1106): Output Structure + Synthesis Mapping Table
   - Add header explaining purpose and loading context
   - Retain all `> **Note:**` reference documentation markers
   - **Verification**: Diff against original line ranges — zero content changes
   - **Expected size**: ~140 lines (plus header)

2.3. **Create `refs/validation-checklists.md`** (FR-PRD-R.3)
   - Extract blocks B24–B27 (lines 1108–1254): Synthesis Quality Review Checklist, Assembly Process (Steps 8–11), Validation Checklist (18+4 items), Content Rules table
   - Add header explaining purpose and loading context
   - Retain all `> **Note:**` reference documentation markers
   - **Verification**: Diff against original line ranges — zero content changes
   - **Expected size**: ~150 lines (plus header)

2.4. **Create `refs/build-request-template.md`** (FR-PRD-R.5)
   - Extract block B11 (lines 344–508): complete BUILD_REQUEST format
   - Add header explaining purpose and loading context
   - **Update SKILL CONTEXT FILE references** (exactly 6 path changes):
     - `"Agent Prompt Templates" section` → `refs/agent-prompts.md`
     - `"Synthesis Mapping Table" section` → `refs/synthesis-mapping.md`
     - `"Synthesis Quality Review Checklist" section` → `refs/validation-checklists.md`
     - `"Assembly Process" section` → `refs/validation-checklists.md`
     - `"Validation Checklist" section` → `refs/validation-checklists.md`
     - `"Content Rules" section` → `refs/validation-checklists.md`
   - `"Tier Selection" section` remains referencing SKILL.md — no change
   - Update Phase 2 task file references: `from SKILL.md` → `from refs/agent-prompts.md` (and similar)
   - **Verification**: Diff shows ONLY the documented SKILL CONTEXT FILE path changes — zero other content changes
   - **Expected size**: ~165 lines (plus header)

### Integration Points — refs/ File Registry

| Named Artifact | Purpose | Owning Phase | Wired Components | Consuming Phase(s) |
|---|---|---|---|---|
| `refs/agent-prompts.md` | 8 agent prompt templates | Phase 2 (task 2.1) | Codebase Research, Web Research, Synthesis, rf-analyst, rf-qa Research Gate, rf-qa Synthesis Gate, rf-qa Report Validation, rf-assembler | Phase 3 (SKILL.md loading declarations at A.7), Runtime (builder subagent reads) |
| `refs/synthesis-mapping.md` | Output Structure + Synthesis Mapping Table | Phase 2 (task 2.2) | PRD section outline, 9-row mapping table | Phase 3 (SKILL.md loading declarations at A.7), Runtime (builder subagent reads) |
| `refs/validation-checklists.md` | Checklists + Assembly + Content Rules | Phase 2 (task 2.3) | Synthesis QA checklist (9 criteria), Assembly Process (Steps 8-11), Validation Checklist (18+4), Content Rules (10 rows) | Phase 3 (SKILL.md loading declarations at A.7), Runtime (builder subagent reads) |
| `refs/build-request-template.md` | BUILD_REQUEST format with updated paths | Phase 2 (task 2.4) | BUILD_REQUEST block with 6 updated SKILL CONTEXT FILE references | Phase 3 (SKILL.md loading declarations at A.7), Runtime (orchestrator loads at A.7) |

### Cross-Reference Wiring — BUILD_REQUEST Dispatch Table

The BUILD_REQUEST template (refs/build-request-template.md) acts as a **dispatch table** that wires builder subagent phases to specific refs/ files:

| BUILD_REQUEST Reference | Resolved Target | Wired In Phase | Consumed At Runtime |
|---|---|---|---|
| SKILL CONTEXT FILE: `refs/agent-prompts.md` | Agent prompt templates | Phase 2, task 2.4 | Builder subagent Phase 2, 3, 4, 5, 6 |
| SKILL CONTEXT FILE: `refs/synthesis-mapping.md` | Output structure + mapping | Phase 2, task 2.4 | Builder subagent Phase 5, 6 |
| SKILL CONTEXT FILE: `refs/validation-checklists.md` | Checklists + assembly + rules | Phase 2, task 2.4 | Builder subagent Phase 5, 6 |
| SKILL CONTEXT FILE: `SKILL.md` (Tier Selection) | Tier selection section | Unchanged | Builder subagent Phase 1 |

### Exit Criteria
- [ ] 4 files exist in `.claude/skills/prd/refs/`
- [ ] Each file has a purpose header
- [ ] `diff` of agent prompts against original: zero content changes (FR-PRD-R.2)
- [ ] `diff` of synthesis mapping against original: zero content changes (FR-PRD-R.4)
- [ ] `diff` of validation checklists against original: zero content changes (FR-PRD-R.3)
- [ ] `diff` of BUILD_REQUEST shows exactly 6 SKILL CONTEXT FILE path changes (FR-PRD-R.5)
- [ ] Combined refs/ line count: ~870 lines (±30)

---

## Phase 3: SKILL.md Restructuring — Behavioral Spine

**Goal**: Remove extracted content from SKILL.md, add loading declarations, update cross-references. Result: 430–500 line behavioral protocol file.

**Milestone**: SKILL.md passes line count check and contains correct loading declarations.

### Tasks

3.1. **Remove extracted content blocks from SKILL.md**
   - Remove block B11 (lines 344–508): BUILD_REQUEST format → now in `refs/build-request-template.md`
   - Remove blocks B14–B21 (lines 553–967): agent prompt templates → now in `refs/agent-prompts.md`
   - Remove blocks B22–B23 (lines 969–1106): output structure + synthesis mapping → now in `refs/synthesis-mapping.md`
   - Remove blocks B24–B27 (lines 1108–1254): checklists + assembly + content rules → now in `refs/validation-checklists.md`
   - **CRITICAL**: Work from highest line numbers downward to avoid line-shift errors
   - Retain all behavioral blocks (B01–B10, B12–B13, B28–B30) in SKILL.md

3.2. **Add per-phase loading declarations** (FR-PRD-R.6)
   - In the Stage A.7 section, add loading declaration block:
     ```
     **Orchestrator loads**: `refs/build-request-template.md`
     **Builder subagent loads** (referenced within BUILD_REQUEST):
       - `refs/agent-prompts.md`
       - `refs/synthesis-mapping.md`
       - `refs/validation-checklists.md`
     ```
   - Use concrete inline reference format following `sc-adversarial-protocol` `See refs/...` pattern
   - Confirm: no other phase (A.1–A.6, Stage B) loads refs/ files
   - Confirm: orchestrator loads at most 2 refs simultaneously (SKILL.md + build-request-template.md)

3.3. **Update internal cross-references**
   - Replace all former prose section references (e.g., `"Agent Prompt Templates" section in SKILL.md`) with refs/ file paths
   - **Verification**: `grep` for stale section references returns 0 matches
   - Addresses Risk #2 (cross-reference breakage)

3.4. **Handle B05/B30 Artifact Locations table merge** (GAP-01)
   - Append B30's 6 specific QA paths to B05's Artifact Locations table
   - Preserve B05's naming convention
   - Do NOT resolve B30's cosmetic `[NN]-[topic].md` inconsistency (per spec)

3.5. **Line count verification**
   - Count SKILL.md lines: must be 430–500 (hard ceiling at 500)
   - If over 500: identify lowest-priority behavioral content that can be further decomposed
   - If under 430: verify no content was accidentally over-extracted
   - Estimate token count: target ≤ 2,000 tokens (~4.5 tokens/line)

### Integration Points — Loading Declaration Wiring

| Named Artifact | Mechanism | Owning Phase | Wired In Task | Cross-Reference |
|---|---|---|---|---|
| SKILL.md A.7 loading declaration block | Inline markdown reference directives | Phase 3 | Task 3.2 | Consumes refs/ files created in Phase 2 |
| Orchestrator context loading | `See refs/build-request-template.md` | Phase 3 | Task 3.2 | Max 2 refs concurrent (NFR-PRD-R.2) |
| Builder subagent context wiring | BUILD_REQUEST SKILL CONTEXT FILE entries | Phase 2 | Task 2.4 | Builder reads refs/ at runtime per BUILD_REQUEST dispatch |

### Exit Criteria
- [ ] SKILL.md line count: 430–500 (FR-PRD-R.1)
- [ ] Contains: frontmatter, purpose, input, tier selection, output locations, execution overview, Stage A protocol (A.1–A.8), Stage B delegation, critical rules, research quality signals, artifact locations, session management, updating existing PRD
- [ ] Does NOT contain: agent prompt templates, validation checklists, synthesis mapping tables, assembly process steps, content rules tables, BUILD_REQUEST format, output structure reference
- [ ] Loading declarations present at A.7 with correct refs/ paths (FR-PRD-R.6)
- [ ] `grep` for stale prose section references returns 0 matches
- [ ] Token estimate ≤ 2,000

---

## Phase 4: Verification, Sync & Commit

**Goal**: Full fidelity verification, component sync, and atomic commit.

**Milestone**: Single commit on feature branch with all changes passing all success criteria.

### Tasks

4.1. **Fidelity verification — zero content loss** (FR-PRD-R.7)
   - Verify every content block from fidelity index (B01–B30) appears in exactly one destination file
   - Diff each of 8 agent prompt templates against original: zero content changes
   - Diff each checklist/table against original: zero content changes
   - Diff BUILD_REQUEST: only 6 documented path changes
   - Combined line count of SKILL.md + all refs/ files: 1,370–1,400 lines
   - Update fidelity index with verified destinations

4.2. **Success criteria validation sweep**
   - Run all 12 success criteria checks:
     1. SKILL.md line count: 430–500
     2. refs/ file count: exactly 4
     3. Combined line count: 1,370–1,400
     4. Agent prompt fidelity: zero diff
     5. Checklist fidelity: zero diff
     6. BUILD_REQUEST fidelity: only 6 path changes
     7. Zero stale section references: `grep` returns 0
     8. Loading declarations present: `grep 'refs/'` in SKILL.md
     9. Cross-references updated: `grep 'refs/agent-prompts.md'` in build-request-template.md
     10. Token budget: ≤ 2,000 tokens
     11. Max concurrent refs: ≤ 2
     12. Behavioral regression: E2E invocation test

4.3. **Component sync**
   - Run `make sync-dev` to propagate `.claude/skills/prd/` → `src/superclaude/skills/prd/`
   - Run `make verify-sync` to confirm both sides match
   - Verify `src/superclaude/skills/prd/refs/` contains all 4 files

4.4. **Behavioral regression test** (NFR-PRD-R.4)
   - Invoke PRD skill on a test product
   - Verify: Stage A completes, task file created with all prompts baked in
   - Verify: Stage B completes, PRD written to expected output location
   - Verify: Output structure matches pre-refactoring behavior

4.5. **Atomic commit**
   - Single commit containing all changes (per Architectural Constraint #6)
   - Commit message: `refactor: decompose PRD SKILL.md into behavioral spine + 4 refs/ files`
   - Files in commit:
     - Modified: `.claude/skills/prd/SKILL.md`
     - Added: `.claude/skills/prd/refs/agent-prompts.md`
     - Added: `.claude/skills/prd/refs/build-request-template.md`
     - Added: `.claude/skills/prd/refs/synthesis-mapping.md`
     - Added: `.claude/skills/prd/refs/validation-checklists.md`
     - Modified: `src/superclaude/skills/prd/SKILL.md` (via sync)
     - Added: `src/superclaude/skills/prd/refs/*` (via sync)

### Exit Criteria
- [ ] All 12 success criteria pass
- [ ] `make verify-sync` passes
- [ ] E2E behavioral regression test passes
- [ ] Single atomic commit on feature branch
- [ ] Rollback path confirmed: `git revert <commit>` restores monolithic SKILL.md

---

## Risk Assessment & Mitigation

| # | Risk | Severity | Probability | Mitigation | Phase |
|---|------|----------|-------------|------------|-------|
| 1 | Content loss during decomposition | HIGH | Low | Word-for-word diff verification per block using fidelity index first/last 10-word markers | Phase 2, 4 |
| 2 | Cross-reference breakage in BUILD_REQUEST | HIGH | Medium | Explicit cross-reference map (6 documented changes); `grep` for stale section references post-refactoring | Phase 2 (task 2.4), Phase 3 (task 3.3) |
| 3 | Loading order wrong — refs loaded at wrong phase | MEDIUM | Low | Only one phase (A.7) loads refs; loading declaration verified in Phase 3 task 3.2 | Phase 3 |
| 4 | Builder subagent path resolution failure | MEDIUM | Low | Builder spawned from SKILL.md directory; relative paths; test in Phase 4 E2E | Phase 4 |
| 5 | B05/B30 Artifact Locations merge corruption | LOW | Low | Keep B05 intact, append B30's unique QA paths; documented merge strategy | Phase 3 (task 3.4) |
| 6 | refs/ file missing or renamed after deploy | MEDIUM | Low | Builder fails explicitly with file-not-found; single-commit rollback via `git revert` | Phase 4 |
| 7 | SKILL.md modified between spec and implementation | MEDIUM | Low | Freeze baseline SHA in Phase 1; implement immediately; re-verify if changes detected | Phase 1 |

---

## Resource Requirements & Dependencies

### Prerequisites (must exist before Phase 1)
1. Fidelity index at `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` — **confirmed exists**
2. Current SKILL.md at 1,373 lines — **confirmed**
3. `sc-adversarial-protocol` refs/ pattern available as reference — **confirmed** (4 refs/ files)
4. `make sync-dev` and `make verify-sync` tooling operational

### External Dependencies
| Dependency | Type | Risk | Notes |
|---|---|---|---|
| sc-adversarial-protocol skill | Architectural template | None | Read-only reference, not modified |
| SuperClaude Developer Guide | Specification source | None | Defines 500-line ceiling and refs/ pattern |
| rf-task-builder subagent | Runtime consumer | Low | Must resolve relative refs/ paths — verified in Phase 4 E2E |
| `/task` skill | Downstream executor | None | Reads task files not SKILL.md — transparent to decomposition |
| `make sync-dev` / `make verify-sync` | Build tooling | None | Required in Phase 4 for component sync |

### Tooling Required
- `diff` / `git diff` — fidelity verification
- `grep` — cross-reference validation
- `wc -l` — line count verification
- `make sync-dev` / `make verify-sync` — component sync

---

## Success Criteria & Validation Approach

All 12 success criteria from the extraction document are validated in Phase 4, task 4.2. Each criterion maps to a specific, automatable check:

| # | Criterion | Check Method | Pass Condition |
|---|-----------|-------------|----------------|
| 1 | SKILL.md line count | `wc -l SKILL.md` | 430–500 |
| 2 | refs/ file count | `ls refs/ \| wc -l` | 4 |
| 3 | Combined line count | `wc -l SKILL.md refs/*` | 1,370–1,400 |
| 4 | Agent prompt fidelity | `diff` per template vs. original | Zero content diff |
| 5 | Checklist fidelity | `diff` per checklist vs. original | Zero content diff |
| 6 | BUILD_REQUEST fidelity | `diff` vs. original | Only 6 path changes |
| 7 | Zero stale section refs | `grep -c '".*section"' SKILL.md` | 0 |
| 8 | Loading declarations | `grep 'refs/' SKILL.md` | Matches at A.7 |
| 9 | Cross-refs in BUILD_REQUEST | `grep 'refs/agent-prompts.md' refs/build-request-template.md` | Match found |
| 10 | Token budget | Line count × 4.5 | ≤ 2,000 |
| 11 | Max concurrent refs | Manual inspection of loading declarations | ≤ 2 |
| 12 | Behavioral regression | E2E skill invocation | Identical behavior |

---

## Timeline Estimates

| Phase | Estimated Duration | Dependencies | Parallelism |
|-------|-------------------|--------------|-------------|
| Phase 1: Preparation | 30 min | None | Sequential — prerequisite checks |
| Phase 2: Content Extraction | 2–3 hours | Phase 1 complete | Tasks 2.1, 2.2, 2.3 parallelizable; task 2.4 sequential after 2.1–2.3 |
| Phase 3: SKILL.md Restructuring | 1–2 hours | Phase 2 complete | Tasks 3.1–3.4 sequential (all modify same file); task 3.5 after all |
| Phase 4: Verification & Commit | 1–1.5 hours | Phase 3 complete | Tasks 4.1–4.2 parallelizable; 4.3–4.5 sequential |
| **Total** | **4.5–7 hours** | | |

**Critical path**: Phase 1 → Phase 2 (2.1–2.3 parallel, then 2.4) → Phase 3 (sequential) → Phase 4

---

## Open Questions (Carried Forward)

1. **Token ceiling vs. line ceiling precedence** (OQ-1): If 480 lines × 4.5 tokens/line = 2,160 exceeds the 2,000-token target, which constraint takes precedence? **Recommendation**: Treat 500 lines as the hard ceiling; 2,000 tokens as a soft target. If the final SKILL.md is 460 lines (~2,070 tokens), accept it — the ~3.5% overshoot is within estimation error.

2. **Naming convention coexistence** (OQ-2): B30's `[NN]-[topic].md` and B05's `[NN]-[topic-name].md` will coexist in the merged Artifact Locations table per spec instruction. No action required during this refactoring.

3. **Fidelity index creation** (OQ-3): Confirmed — fidelity index already exists at `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md`. Not an implicit prerequisite; it's present.

4. **Whitespace normalization scope** (OQ-4): **Recommendation**: Permit trailing whitespace removal and line-ending normalization (CRLF→LF). Do NOT permit indentation changes or blank line consolidation, as these could alter markdown rendering of code blocks and tables.
