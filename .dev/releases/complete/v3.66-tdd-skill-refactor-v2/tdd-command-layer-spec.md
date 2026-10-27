# TDD Skill Command Layer — Release Specification

```yaml
---
title: "Add thin command layer for TDD skill to complete three-tier architecture"
version: "1.0.0"
status: draft
feature_id: FR-TDD-CMD
parent_feature: FR-TDD-REFACTOR
spec_type: refactoring
complexity_score: 0.25
complexity_class: LOW
target_release: v3.65
authors: [user, claude]
created: 2026-04-03
related_specs:
  - ".dev/releases/complete/v3.65-tdd-skill-refactor/tdd-refactor-spec.md (refs/ decomposition — COMPLETE)"
  - ".dev/releases/backlog/prd-skill-refactor/prd-refactor-spec-v2.md (PRD command layer — pattern reference)"
quality_scores:
  clarity: 9.5
  completeness: 9.5
  testability: 9.5
  consistency: 9.5
  overall: 9.5
---
```

## 1. Problem Statement

The TDD skill at `.claude/skills/tdd/SKILL.md` is missing its thin command layer. While the refs/ decomposition is complete (SKILL.md is 438 lines with 5 refs/ files), no command file exists at `commands/sc/tdd.md`. This violates the Developer Guide's three-tier architecture mandate: "Every skill MUST have a command in front of it. The command is the user-facing entry point; the skill is the behavioral engine. A skill without a command is an architectural violation."

Additionally, the SKILL.md contains ~23 lines of interface content (usage examples, tier selection table) that belong in the command layer per Developer Guide Section 9.3, which lists placing "flags, usage examples, or CLI interface concerns in SKILL.md" as a "do not."

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| No command file exists for TDD skill | `ls .claude/commands/sc/tdd*` returns empty | Users invoke skill directly — no standardized entry point with flags, examples, or boundaries |
| Developer Guide mandate: "Every skill MUST have a command in front of it" | Developer Guide, Three-Tier Architecture section | TDD skill violates mandatory architecture |
| Developer Guide anti-pattern: "Skill without command layer" | Developer Guide Section 9.7 | Explicitly listed anti-pattern with solution: "Create a thin command file" |
| Skill-Authoring Checklist item 1: "Thin command layer exists" | Developer Guide Section 5.10 | Mandatory checklist item not satisfied |
| Usage examples in SKILL.md lines 48-63 | `.claude/skills/tdd/SKILL.md` | Interface content in skill file violates separation of concerns |
| Tier selection table in SKILL.md lines 82-88 | `.claude/skills/tdd/SKILL.md` | Flag documentation in skill file instead of command |
| PRD skill had identical gap, resolved in PRD spec v2 | `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec-v2.md` FR-PRD-R.0 | Established pattern for this exact fix |
| Adversarial command demonstrates correct pattern | `.claude/commands/sc/adversarial.md` (167 lines) | Gold-standard thin command layer reference |

### 1.2 Scope Boundary

**In scope**:
- Creating `commands/sc/tdd.md` (~120-150 lines) as the thin command layer
- Migrating interface content (prompt examples, tier table) from SKILL.md to command
- Creating corresponding `src/superclaude/commands/tdd.md` as canonical source
- `make sync-dev` + `make verify-sync` for commands/

**Out of scope**:
- Modifying TDD skill refs/ files (decomposition is complete)
- Modifying TDD skill pipeline logic, phase structure, or execution behavior
- Renaming the skill directory (stays as `tdd/`)
- Changing agent prompt content, validation criteria, or content rules
- Adding new features or capabilities to the TDD skill

## 2. Solution Overview

Create a thin command file at `commands/sc/tdd.md` (~120-150 lines) following the `commands/sc/adversarial.md` gold standard. Migrate ~23 lines of interface content (usage examples, tier selection table) from SKILL.md to the command. This completes the three-tier architecture: Command → Skill → refs/.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Create command file | YES — `commands/sc/tdd.md` | Skip command (current state) | Developer Guide mandates command layer for every skill |
| Command style | Standard (~130 lines) with explicit flags | Minimal (~100, no flags); Heavy (~180+, inline tables) | Standard matches adversarial gold standard and PRD pattern |
| Content migration | Move prompt examples + tier table | Move nothing; Move entire Input section | Examples are usage patterns (command territory). Tier table documents `--tier` flag. Parsing logic and selection rules stay in skill. |
| Directory rename | NO — keep `tdd/` | `sc-tdd-protocol/`, `sc-tdd/` | Dual-purpose utility; `sc-` prefix is for protocol-only skills |
| TDD-specific flags | `--prd`, `--from-prd` in addition to standard flags | Omit PRD flags | PRD-to-TDD translation is a core use case documented in SKILL.md description |

### 2.2 Workflow / Data Flow

```
User invokes /sc:tdd <component> [flags]
  |
  v
commands/sc/tdd.md loaded (~130 lines)
  Parses flags, shows usage/examples/boundaries
  |
  v [Activation: Skill tdd]
skills/tdd/SKILL.md loaded (~415 lines, post-migration)
  Contains: purpose, input parsing, tier selection rules,
            output locations, execution overview, Stage A protocol,
            Stage B delegation, phase loading contract
  |
  v
Stage A: Scope Discovery (A.1 through A.6)
  No refs/ loaded — all behavioral content in SKILL.md
  |
  v
Stage A.7: Build Task File
  Orchestrator loads: refs/build-request-template.md
  Builder loads: refs/agent-prompts.md, refs/synthesis-mapping.md,
                 refs/validation-checklists.md, refs/operational-guidance.md
  |
  v
Stage A.8: Verify task file
  |
  v
Stage B: Delegate to /task skill
  /task executes self-contained checklist items from task file
```

## 3. Functional Requirements

### FR-TDD-CMD.1: Thin Command Layer — `commands/sc/tdd.md`

**Description**: Create a thin command file at `.claude/commands/sc/tdd.md` (~120-150 lines) following the `commands/sc/adversarial.md` pattern. The command provides the user-facing interface and hands off to the skill via the Activation pattern. The command contains zero protocol logic.

**Acceptance Criteria**:
- [ ] File exists at `.claude/commands/sc/tdd.md`
- [ ] Canonical source exists at `src/superclaude/commands/tdd.md`
- [ ] Frontmatter contains: `name: tdd`, `description`, `category: documentation`, `complexity: advanced`, `allowed-tools`, `mcp-servers`, `personas`
- [ ] `## Required Input` section documents the mandatory `<component>` positional argument
- [ ] `## Usage` section shows invocation patterns: `/sc:tdd <component> [options]`
- [ ] `## Arguments` section describes the `<component>` positional argument and optional PRD reference
- [ ] `## Options` table documents these flags:

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<component>` | - | Yes | - | Component, service, or system to design |
| `--tier` | `-t` | No | Auto | `lightweight`, `standard`, `heavyweight` |
| `--prd` | - | No | - | Path to PRD that this TDD implements |
| `--resume` | `-r` | No | `false` | Resume from existing task file |
| `--output` | `-o` | No | Auto | Output path for final TDD |
| `--focus` | `-f` | No | All | Comma-separated directories/subsystems to focus on |
| `--from-prd` | - | No | `false` | Explicit PRD-to-TDD translation mode |

- [ ] `## Behavioral Summary` contains a one-paragraph overview of the two-stage process (scope discovery with task file creation, then task file execution via `/task` delegation) without protocol details
- [ ] `## Examples` section contains 5-6 examples migrated from SKILL.md lines 48-63 plus TDD-specific examples:
  - Strong: all four inputs (component, PRD reference, focus dirs, output path)
  - Strong: PRD-to-TDD translation with explicit PRD path
  - Strong: design from scratch with clear scope
  - Weak (annotated): topic only
  - Resume: `--resume` with existing task folder
  - Tier override: explicit `--tier heavyweight`
- [ ] `## Activation` section contains the mandatory handoff:
  ```
  **MANDATORY**: Before executing any protocol steps, invoke:
  > Skill tdd

  Do NOT proceed with protocol execution using only this command file.
  The full behavioral specification is in the protocol skill.
  ```
- [ ] `## Boundaries` section contains Will/Will Not:
  - **Will**: Create TDDs through systematic codebase investigation and web research; Translate PRDs into engineering specifications; Support three depth tiers; Resume from existing task files; Validate output through multi-agent QA pipeline
  - **Will Not**: Modify source code; Implement the designs described in the TDD; Generate running code; Create PRDs (use `/sc:prd`); Make product decisions
- [ ] `## Related Commands` table references `/sc:prd`, `/sc:design`, `/sc:workflow`, `/sc:brainstorm`
- [ ] Command file line count is between 100 and 170 lines
- [ ] Command contains zero protocol logic — no Stage A/B details, no agent spawning instructions, no phase descriptions, no loading declarations

**Dependencies**: None

### FR-TDD-CMD.2: Content Migration from SKILL.md to Command

**Description**: Specific interface-concern content moves from SKILL.md to the command file. This content is removed from SKILL.md (not duplicated). Migration is optional for line budget (SKILL.md is already under 500) but required for architectural correctness per Developer Guide Section 9.3.

**Acceptance Criteria**:
- [ ] Effective Prompt Examples (SKILL.md lines 48-63, ~16 lines) appear in `commands/sc/tdd.md` Examples section, adapted to command invocation syntax
- [ ] Tier Selection table (SKILL.md lines 82-88, header + 3 data rows, ~7 lines) appears in `commands/sc/tdd.md` Options section as `--tier` reference
- [ ] SKILL.md Input section retains: 4-input description (lines 34-46), "What to Do If Prompt Is Incomplete" template (lines 65-76)
- [ ] SKILL.md Tier Selection section retains: introductory sentence + selection rules (lines 90-94) but not the full table
- [ ] No content appears in BOTH the command file and SKILL.md (except brief cross-references)
- [ ] Post-migration SKILL.md line count is between 400 and 440 lines

**Dependencies**: FR-TDD-CMD.1

### FR-TDD-CMD.3: Fidelity Verification

**Description**: Migrated content appears in the command file verbatim (adapted to command context) and is cleanly removed from SKILL.md with no collateral damage to surrounding content.

**Acceptance Criteria**:
- [ ] All 3 strong prompt examples from SKILL.md lines 48-57 appear in command Examples
- [ ] Both weak prompt examples from SKILL.md lines 59-63 appear in command Examples (annotated)
- [ ] Tier table's 3 data rows (Lightweight, Standard, Heavyweight) with all 5 columns appear in command Options
- [ ] SKILL.md behavioral protocol (Stage A, Stage B, critical rules, session management) is completely unmodified
- [ ] SKILL.md loading declarations and Phase Loading Contract table are completely unmodified
- [ ] All 5 refs/ files are completely unmodified (zero changes)

**Dependencies**: FR-TDD-CMD.1, FR-TDD-CMD.2

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| `src/superclaude/commands/tdd.md` | Canonical thin command layer for TDD skill | None |
| `.claude/commands/sc/tdd.md` | Dev-copy mirror for Claude Code runtime | Produced via `make sync-dev` |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/skills/tdd/SKILL.md` | Remove ~23 lines of interface content (prompt examples lines 48-63, tier table lines 82-88) | Content migrates to command per Developer Guide 9.3 |
| `.claude/skills/tdd/SKILL.md` | Synced dev-copy of canonical SKILL.md | Runtime parity after `make sync-dev` |

### 4.3 Removed Files

| File/Section | Reason | Migration |
|-------------|--------|-----------|
| None | No files removed. Content within SKILL.md is relocated, not deleted. | Prompt examples → command Examples. Tier table → command Options. |

### 4.4 Module Dependency Graph

```
commands/sc/tdd.md (thin command, ~130 lines)
  |
  v [Activation: Skill tdd]
skills/tdd/SKILL.md (behavioral protocol, ~415 lines)
  |
  +-- [Stage A.7 orchestrator] --> refs/build-request-template.md
  |
  +-- [Stage A.7 builder] --> refs/agent-prompts.md
  |                       --> refs/synthesis-mapping.md
  |                       --> refs/validation-checklists.md
  |                       --> refs/operational-guidance.md
  |
  +-- [Stage B] --> /task skill (canonical F1 execution loop)
```

### 4.6 Implementation Order

```
1. Create src/superclaude/commands/tdd.md         -- New command file from adversarial template
   Remove interface content from src/.../SKILL.md  -- [parallel with step 1]
2. Verify SKILL.md structural integrity            -- Depends on 1
3. make sync-dev                                   -- Depends on 1, 2
4. make verify-sync                                -- Depends on 3
5. Run test plan verification                      -- Depends on 4
```

## 5. Interface Contracts

### 5.1 CLI Surface

```
/sc:tdd <component> [--tier lightweight|standard|heavyweight] [--prd <path>]
        [--resume] [--output <path>] [--focus <dirs>] [--from-prd]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<component>` | positional string | (required) | Component, service, or system to design |
| `--tier` | enum | Auto | Depth tier: lightweight, standard, heavyweight |
| `--prd` | path | - | PRD file that this TDD implements |
| `--resume` | boolean | false | Resume from existing MDTM task file |
| `--output` | path | Auto | Output path for final TDD |
| `--focus` | comma-string | All | Directories/subsystems to focus investigation on |
| `--from-prd` | boolean | false | Explicit PRD-to-TDD translation mode |

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-TDD-CMD.1 | Command file size | 100-170 lines | `wc -l commands/sc/tdd.md` |
| NFR-TDD-CMD.2 | Zero protocol leakage | Command contains no Stage A/B, no agent spawning, no phase logic | Grep for prohibited keywords |
| NFR-TDD-CMD.3 | Post-migration SKILL.md size | 400-440 lines | `wc -l skills/tdd/SKILL.md` |
| NFR-TDD-CMD.4 | Activation correctness | Command hands off to `Skill tdd` | Grep for activation pattern |
| NFR-TDD-CMD.5 | Zero behavioral regression | Identical execution behavior before and after | SKILL.md behavioral sections unmodified |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Content loss during migration | Very Low | Low | Only ~23 lines move; contiguous blocks; diff verification |
| Protocol leakage into command | Low | Medium | Review against adversarial gold standard; grep for Stage/Phase/Agent keywords |
| Scope creep to improve TDD content | Low | Medium | Strict spec: only create command + remove migrated content. Zero behavioral changes. |
| Sync failure (command not in src/) | Low | Low | `make verify-sync` catches immediately |
| Prompt examples lose context when adapted to command syntax | Very Low | Low | Examples are self-contained strings. Command provides equivalent framing. |

## 8. Test Plan

### 8.1 Command Layer Tests (Structural)

| Test | Validates |
|------|-----------|
| `test -f .claude/commands/sc/tdd.md` | Command file exists |
| `wc -l .claude/commands/sc/tdd.md` returns 100-170 | Command within line budget |
| `grep '## Activation' .claude/commands/sc/tdd.md` matches | Activation section present |
| `grep 'Skill tdd' .claude/commands/sc/tdd.md` matches | Correct skill invocation |
| `grep '## Boundaries' .claude/commands/sc/tdd.md` matches | Boundaries section present |
| `grep '## Examples' .claude/commands/sc/tdd.md` matches | Examples section present |
| `grep -- '--tier' .claude/commands/sc/tdd.md` matches | Tier flag documented |
| `grep -- '--prd' .claude/commands/sc/tdd.md` matches | PRD flag documented |
| `grep -- '--resume' .claude/commands/sc/tdd.md` matches | Resume flag documented |
| `grep -- '--from-prd' .claude/commands/sc/tdd.md` matches | From-PRD flag documented |
| `grep -c 'Stage A' .claude/commands/sc/tdd.md` returns 0 | Zero protocol leakage |
| `grep -c 'rf-task-builder' .claude/commands/sc/tdd.md` returns 0 | Zero protocol leakage |
| `grep -c 'subagent' .claude/commands/sc/tdd.md` returns 0 | Zero protocol leakage |

### 8.2 Content Migration Tests

| Test | Validates |
|------|-----------|
| `grep 'agent orchestration system' .claude/commands/sc/tdd.md` matches | Strong example migrated to command |
| `grep -c 'agent orchestration system' .claude/skills/tdd/SKILL.md` returns 0 | Example removed from SKILL.md |
| `grep 'canvas roadmap PRD' .claude/commands/sc/tdd.md` matches | PRD-to-TDD example migrated |
| `grep -c '| **Lightweight**' .claude/skills/tdd/SKILL.md` returns 0 | Tier table removed from SKILL.md |
| `grep 'What to Do If the Prompt Is Incomplete' .claude/skills/tdd/SKILL.md` matches | Incomplete prompt template stays |
| `grep 'Default to Standard' .claude/skills/tdd/SKILL.md` matches | Tier selection rules stay |
| `wc -l .claude/skills/tdd/SKILL.md` returns 400-440 | Post-migration line count |

### 8.3 Integration / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|-----------------|
| Command-to-skill handoff | Read `commands/sc/tdd.md`, verify Activation section | Activation pattern matches Developer Guide template |
| Gold-standard comparison | Diff structure against `commands/sc/adversarial.md` | Same sections in same order: frontmatter, required input, usage, arguments, options, behavioral summary, examples, activation, boundaries, related commands |
| Three-tier completeness | Verify all tiers: command at `commands/sc/`, skill at `skills/tdd/`, refs at `skills/tdd/refs/` | All three tiers present |
| Sync verification | `make verify-sync` | Passes with no drift between src/ and .claude/ |
| SKILL.md refs/ loading intact | Grep loading declarations in SKILL.md | All 5 refs/ files still referenced |
| Phase Loading Contract intact | Read Phase Loading Contract table in SKILL.md | Table unmodified |

## 9. Migration & Rollout

- **Breaking changes**: None. This is purely additive (new command file) plus cosmetic cleanup (interface content moves from skill to command).
- **Backwards compatibility**: Preserved. Direct `Skill tdd` invocation continues to work. The command file adds a new, standardized entry point without removing the existing one.
- **Rollback plan**: Delete `commands/sc/tdd.md` and restore ~23 lines to SKILL.md via `git revert <commit>`.
- **Migration steps**:
  1. Create `src/superclaude/commands/tdd.md` (canonical source)
  2. Remove migrated content from `src/superclaude/skills/tdd/SKILL.md`
  3. Run `make sync-dev` to propagate both commands/ and skills/ to `.claude/`
  4. Run `make verify-sync` to confirm parity
  5. Run test plan (Sections 8.1-8.3) to verify command structure and migration fidelity

## 10. Downstream Inputs

### For sc:roadmap
This spec is a minor additive item under the v3.65 TDD refactor release. No behavioral feature delta.

### For sc:tasklist
Single task group with 4 implementation steps from Section 4.6. Estimated effort: ~30-45 minutes. Can be completed in a single session.

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| None | All questions resolved during brainstorm analysis | N/A | N/A |

## 12. Brainstorm Gap Analysis

> Analysis from `.dev/releases/complete/v3.65-tdd-skill-refactor/02-brainstorm-output.md`

| Gap ID | Description | Severity | Affected Section | Resolution |
|--------|-------------|----------|------------------|------------|
| GAP-CMD-01 | Existing TDD refactor spec omits command layer entirely | Critical | Scope, Architecture, Tests | This spec (FR-TDD-CMD) addresses as a companion to the existing refs/ decomposition spec |
| GAP-CMD-02 | SKILL.md contains ~23 lines of interface content (examples, tier table) | Minor | Content migration | FR-TDD-CMD.2 moves this content to command |
| GAP-CMD-03 | Three-tier dependency graph missing from existing spec | Major | Architecture 4.4 | This spec provides the complete three-tier graph |
| GAP-CMD-04 | Migration steps in existing spec don't mention command sync | Minor | Migration 9 | This spec includes command sync steps |
| GAP-CMD-05 | No command-layer tests in existing spec | Major | Test Plan 8 | This spec provides comprehensive command tests (8.1-8.3) |

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Thin command layer | ~80-150 line command file providing flags, usage, examples, boundaries, and Activation handoff to a skill. Contains zero protocol logic. |
| Three-tier architecture | Command → Skill → Agents/refs/ — the mandatory architecture for SuperClaude components |
| Activation pattern | The `## Activation` section in a command that hands off to a skill via `Skill <name>` |
| Interface content | Flags, usage examples, tier tables — content belonging in the command layer per Developer Guide 9.3 |
| Protocol content | Behavioral logic (WHAT/WHEN) — content belonging in the skill layer |
| refs/ | Directory within a skill containing reference material (HOW content) loaded on demand per phase |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `.claude/commands/sc/adversarial.md` | Gold-standard thin command layer (167 lines) — structural template |
| `.dev/releases/backlog/prd-skill-refactor/prd-refactor-spec-v2.md` | PRD spec v2 with FR-PRD-R.0 (command layer) and FR-PRD-R.8 (content migration) — pattern reference |
| `.dev/releases/complete/v3.65-tdd-skill-refactor/02-brainstorm-output.md` | TDD brainstorm output with 5-dimension analysis |
| `.dev/releases/complete/v3.65-tdd-skill-refactor/tdd-refactor-spec.md` | Existing TDD refs/ decomposition spec (COMPLETE — this spec is a companion) |
| `.dev/releases/complete/v3.65-tdd-skill-refactor/fidelity-index.md` | TDD fidelity index |
| `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | Developer Guide: Three-Tier Architecture, Activation Pattern, Sections 5.10, 9.3, 9.7 |
| `src/superclaude/examples/release-spec-template.md` | Template this spec follows |
| `.claude/skills/tdd/SKILL.md` | Current TDD skill (438 lines, post-decomposition) |
