---
spec_source: "tdd-command-layer-spec.md"
complexity_score: 0.25
primary_persona: architect
---

# Roadmap: TDD Command Layer Refactor

## 1. Executive Summary

This roadmap covers the creation of a thin command layer for the TDD skill (`commands/sc/tdd.md`) and the migration of ~23 lines of interface-concern content from `SKILL.md` to the new command file. The work resolves an architectural violation documented in the Developer Guide Section 9.3: every skill must have a command in front of it.

**Scope**: 2 new files (canonical + dev copy), 2 modified files (SKILL.md canonical + dev copy), ~130 new lines, ~23 lines relocated. Zero behavioral changes. Complexity: LOW (0.25).

**Gold-standard pattern**: `commands/sc/adversarial.md` (167 lines) defines the structural template. The TDD command follows this pattern exactly.

---

## 2. Phased Implementation Plan

### Phase 1: Preparation & Template Study

**Objective**: Read all reference materials; confirm current state matches extraction assumptions.

**Tasks**:
1. Read `commands/sc/adversarial.md` — internalize section ordering, frontmatter fields, activation pattern, boundaries format
2. Read `skills/tdd/SKILL.md` — confirm current line count (expected: 438), locate migration blocks:
   - Lines 48-63: Effective Prompt Examples (~16 lines)
   - Lines 82-88: Tier Selection table (header + 3 data rows, ~7 lines)
3. Read Developer Guide Section 9.3 (separation of concerns) and Section 5.10 (checklist)
4. Snapshot pre-migration state: `wc -l` on SKILL.md, `git diff --stat` baseline

**Milestone**: All reference material read. Migration blocks confirmed at expected line ranges. Baseline measurements recorded.

**Duration**: ~15 minutes

---

### Phase 2: Command File Creation (FR-TDD-CMD.1)

**Objective**: Create `src/superclaude/commands/tdd.md` following the adversarial gold-standard structure.

**Tasks**:
1. Create `src/superclaude/commands/tdd.md` with the following sections in order:
   - **Frontmatter** (FR-TDD-CMD.1b): `name: tdd`, `description`, `category: documentation`, `complexity: advanced`, `allowed-tools`, `mcp-servers`, `personas`
   - **Required Input** (FR-TDD-CMD.1c): Document `<component>` positional argument
   - **Usage** (FR-TDD-CMD.1d): `/sc:tdd <component> [options]` invocation patterns
   - **Arguments** (FR-TDD-CMD.1e): `<component>` description + optional PRD reference
   - **Options Table** (FR-TDD-CMD.1f): All 7 flags (`<component>`, `--tier`, `--prd`, `--resume`, `--output`, `--focus`, `--from-prd`)
   - **Behavioral Summary** (FR-TDD-CMD.1g): One paragraph on two-stage process — zero protocol details
   - **Examples** (FR-TDD-CMD.1h): 5-6 examples (3 strong, 2 weak annotated, 1 resume/tier override)
   - **Activation** (FR-TDD-CMD.1i): `> Skill tdd` with "Do NOT proceed" guard
   - **Boundaries** (FR-TDD-CMD.1j): Will/Will Not list
   - **Related Commands** (FR-TDD-CMD.1k): `/sc:prd`, `/sc:design`, `/sc:workflow`, `/sc:brainstorm`

2. Verify line count: 100-170 lines (NFR-TDD-CMD.1, FR-TDD-CMD.1l)
3. Verify zero protocol leakage (NFR-TDD-CMD.2, FR-TDD-CMD.1m): grep for `Stage A`, `Stage B`, `rf-task-builder`, `subagent` returns 0 matches

**Named Artifacts / Integration Points**:
- **Activation handoff**: The `## Activation` section wires the command to the skill via `> Skill tdd`. Created in this phase, consumed by Claude Code's skill dispatch at runtime.
- **Options table**: Documents the 7 flags that the skill's Input section interprets. Created here, cross-referenced by Phase 3 (tier table migration populates the `--tier` row).

**Milestone**: `src/superclaude/commands/tdd.md` exists, passes line budget (100-170), passes zero-leakage grep.

**Duration**: ~30 minutes

---

### Phase 3: Content Migration (FR-TDD-CMD.2)

**Objective**: Migrate ~23 lines of interface-concern content from SKILL.md to the command file, then remove from SKILL.md.

**Tasks**:
1. **Migrate prompt examples** (FR-TDD-CMD.2a): Copy SKILL.md lines 48-63 (3 strong + 2 weak examples) into command Examples section. Adapt to command invocation syntax (e.g., prefix with `/sc:tdd`).
2. **Migrate tier table** (FR-TDD-CMD.2b): Copy SKILL.md lines 82-88 (header + 3 data rows) into command Options section as `--tier` reference material.
3. **Remove migrated content from SKILL.md**:
   - Remove Effective Prompt Examples block (lines 48-63) — FR-TDD-CMD.2e
   - Remove tier table rows (lines 82-88), retain introductory sentence + selection rules (lines 90-94) — FR-TDD-CMD.2d
   - Retain 4-input description (lines 34-46) and "What to Do If Prompt Is Incomplete" template (lines 65-76) — FR-TDD-CMD.2c
4. Verify SKILL.md post-migration line count: 400-440 lines (NFR-TDD-CMD.3, FR-TDD-CMD.2f)
5. Verify no duplication — grep for distinctive example strings in both files; each should appear in exactly one (FR-TDD-CMD.2e)

**Named Artifacts / Integration Points**:
- **SKILL.md Input section**: Retains the 4-input structure and incomplete-prompt template. Command's Examples section now owns the concrete examples. The skill reads inputs; the command documents them for users.
- **SKILL.md Tier Selection section**: Retains selection rules (lines 90-94). Command's Options table now owns the tier comparison table. The skill applies rules; the command presents the reference.

**Milestone**: Content migrated. SKILL.md within 400-440 lines. No duplication across files.

**Duration**: ~20 minutes

---

### Phase 4: Fidelity Verification (FR-TDD-CMD.3)

**Objective**: Verify migration correctness with zero collateral damage.

**Tasks**:
1. **Migrated content presence in command** (FR-TDD-CMD.3a, FR-TDD-CMD.3b, FR-TDD-CMD.3c):
   - Grep command file for 3 strong example distinctive strings
   - Grep command file for 2 weak example distinctive strings
   - Grep command file for `Lightweight`, `Standard`, `Heavyweight` tier rows with all 5 columns
2. **Behavioral protocol untouched** (FR-TDD-CMD.3d, NFR-TDD-CMD.5):
   - Diff SKILL.md Stage A section pre/post — zero changes
   - Diff SKILL.md Stage B section pre/post — zero changes
   - Diff SKILL.md critical rules section pre/post — zero changes
   - Diff SKILL.md session management section pre/post — zero changes
3. **Loading declarations untouched** (FR-TDD-CMD.3e):
   - Diff SKILL.md Phase Loading Contract table pre/post — zero changes
4. **Refs files untouched** (FR-TDD-CMD.3f):
   - `git diff` on all 5 refs/ files returns empty:
     - `refs/build-request-template.md`
     - `refs/agent-prompts.md`
     - `refs/synthesis-mapping.md`
     - `refs/validation-checklists.md`
     - `refs/operational-guidance.md`
5. **Activation correctness** (NFR-TDD-CMD.4): Grep command file for `Skill tdd`

**Milestone**: All 26 verification checks pass. Zero collateral damage confirmed.

**Duration**: ~10 minutes

---

### Phase 5: Sync & Commit

**Objective**: Propagate changes through the component sync pipeline and commit.

**Tasks**:
1. Run `make sync-dev` — propagates `src/superclaude/commands/tdd.md` to `.claude/commands/sc/tdd.md` and SKILL.md changes to `.claude/skills/tdd/SKILL.md`
2. Run `make verify-sync` — confirm exit code 0 (SC-12)
3. Verify both file locations exist (SC-1):
   - `src/superclaude/commands/tdd.md`
   - `.claude/commands/sc/tdd.md`
4. Final validation pass on dev copies (repeat key checks from Phase 4 on `.claude/` copies)
5. Commit with conventional commit message: `refactor(tdd): create command layer and migrate interface content from SKILL.md`

**Named Artifacts / Integration Points**:
- **`make sync-dev` pipeline**: Reads from `src/superclaude/commands/` and `src/superclaude/skills/`, writes to `.claude/commands/sc/` and `.claude/skills/`. This phase triggers the pipeline; all prior phases edit only canonical sources.
- **`make verify-sync` check**: Validates parity between `src/` and `.claude/`. Must pass before commit.

**Milestone**: Both canonical and dev-copy locations populated. `make verify-sync` passes. Changes committed.

**Duration**: ~10 minutes

---

## 3. Risk Assessment and Mitigation

| Risk ID | Risk | Severity | Probability | Mitigation | Phase |
|---------|------|----------|-------------|------------|-------|
| RISK-01 | Content loss during migration — ~23 lines partially lost or corrupted | Low | Very Low | Migration blocks are contiguous (lines 48-63, 82-88); diff verification in Phase 4 confirms completeness | Phase 3, 4 |
| RISK-02 | Protocol leakage into command — Stage A/B details or agent spawning in command file | Medium | Low | Author against adversarial gold standard; automated grep for prohibited keywords (`Stage A`, `Stage B`, `rf-task-builder`, `subagent`) in Phase 2, 4 | Phase 2, 4 |
| RISK-03 | Scope creep — temptation to improve TDD content while refactoring | Medium | Low | Strict boundary: only create command + relocate content. Zero behavioral changes. FR-TDD-CMD.3d-f verification gates | Phase 2, 3, 4 |
| RISK-04 | Sync failure — command created in `.claude/` but not `src/` | Low | Low | Always edit `src/superclaude/` first. `make verify-sync` catches drift immediately in Phase 5 | Phase 5 |
| RISK-05 | Prompt examples lose context when adapted to command syntax | Low | Very Low | Examples are self-contained strings; command provides equivalent framing. Visual review in Phase 4 | Phase 3, 4 |

**Architect's note**: The dominant risk is RISK-03 (scope creep). The mitigation is procedural: Phase 4 includes explicit diff checks on every SKILL.md section that must remain untouched. If a behavioral section shows any diff, the implementation is wrong — full stop.

---

## 4. Resource Requirements and Dependencies

### Internal Dependencies

| Dependency | Type | Required By | Notes |
|------------|------|-------------|-------|
| `commands/sc/adversarial.md` | Template | Phase 1, 2 | Gold-standard structural pattern (167 lines). Read-only reference. |
| `skills/tdd/SKILL.md` | Source + Target | Phase 1, 3, 4 | Current 438 lines. Source of migrated content. Modified in Phase 3. |
| `make sync-dev` | Build tool | Phase 5 | Propagates `src/` → `.claude/`. Must succeed before commit. |
| `make verify-sync` | Build tool | Phase 5 | Validates parity. Must exit 0. |
| Developer Guide | Reference | Phase 1 | Sections 9.3, 9.7, 5.10. Authoritative architectural rules. |

### External Dependencies

None. Pure Markdown refactoring — no libraries, services, APIs, or runtime dependencies.

### Tooling

- Text editor (Read, Edit, Write tools)
- Shell (`wc -l`, `grep`, `diff`, `make`)
- Git (commit, diff)

---

## 5. Success Criteria and Validation Approach

All 12 success criteria from the extraction are validated in Phases 4 and 5:

| SC | Criterion | Phase | Method |
|----|-----------|-------|--------|
| SC-1 | Command file exists at both locations | 5 | `test -f` on `src/superclaude/commands/tdd.md` and `.claude/commands/sc/tdd.md` |
| SC-2 | Command file 100-170 lines | 2 | `wc -l` |
| SC-3 | All 7 flags in Options table | 2 | Grep for each flag name |
| SC-4 | Activation section contains `Skill tdd` | 2 | Grep |
| SC-5 | Zero protocol leakage | 2, 4 | Grep for prohibited keywords returns 0 |
| SC-6 | All prompt examples in command | 4 | Grep for distinctive strings from 3 strong + 2 weak examples |
| SC-7 | Tier table in command | 4 | Grep for `Lightweight`, `Standard`, `Heavyweight` rows |
| SC-8 | Migrated content removed from SKILL.md | 4 | Grep for migrated strings in SKILL.md returns 0 |
| SC-9 | SKILL.md 400-440 lines post-migration | 3 | `wc -l` |
| SC-10 | Behavioral protocol unmodified | 4 | Section-level diff pre/post |
| SC-11 | All 5 refs/ files unmodified | 4 | `git diff` on refs/ directory |
| SC-12 | `make verify-sync` passes | 5 | Exit code 0 |

**Validation approach**: Verification is integrated into each phase (not deferred to the end). Phase 2 checks structural correctness. Phase 3 checks migration completeness. Phase 4 is the full fidelity gate. Phase 5 confirms sync pipeline integrity.

---

## 6. Timeline Estimates

| Phase | Description | Estimated Duration | Cumulative |
|-------|-------------|-------------------|------------|
| 1 | Preparation & Template Study | ~15 min | ~15 min |
| 2 | Command File Creation | ~30 min | ~45 min |
| 3 | Content Migration | ~20 min | ~65 min |
| 4 | Fidelity Verification | ~10 min | ~75 min |
| 5 | Sync & Commit | ~10 min | ~85 min |

**Total estimated duration**: ~85 minutes for a single implementer.

**Critical path**: Phase 2 (command creation) is the longest phase and the foundation for Phase 3. Phases 4 and 5 are lightweight verification and pipeline steps.

**Parallelization opportunity**: None meaningful — each phase depends on the prior phase's output. However, within Phase 4, the 26 verification checks can be batched into parallel grep/diff/wc invocations.

---

## 7. Integration Points Summary

| Mechanism | Type | Owning Phase | Wired Components | Consuming Phase(s) |
|-----------|------|-------------|------------------|---------------------|
| `## Activation` section with `> Skill tdd` | Skill dispatch handoff | Phase 2 | Command → TDD skill | Runtime (Claude Code session) |
| Options table `--tier` row | Flag documentation + tier table | Phase 2 (skeleton), Phase 3 (tier table migration) | Command Options ↔ SKILL.md Tier Selection rules | Runtime (user reads command, skill applies rules) |
| SKILL.md Input section | Input contract | Phase 3 (migration preserves) | Skill Input section ↔ Command Examples | Runtime (skill reads inputs, command documents them) |
| `make sync-dev` pipeline | File sync | Phase 5 | `src/superclaude/commands/tdd.md` → `.claude/commands/sc/tdd.md`; `src/superclaude/skills/tdd/SKILL.md` → `.claude/skills/tdd/SKILL.md` | Phase 5 (verify-sync) |

---

## 8. Architect Recommendations

1. **Follow the template exactly**. The adversarial.md gold standard exists precisely so that new commands are structurally identical. Resist any urge to innovate on section ordering or naming.

2. **Edit canonical sources only**. Every change goes to `src/superclaude/` first. The `.claude/` copies are derived artifacts — treat them as read-only until `make sync-dev`.

3. **Snapshot before migration**. Before touching SKILL.md in Phase 3, record `wc -l` and save a copy of the migration blocks. This makes Phase 4 verification trivial.

4. **Treat Phase 4 as a hard gate**. If any verification check fails, do not proceed to Phase 5. Fix the issue and re-verify. The 26 checks are cheap; the cost of committing a broken migration is not.

5. **Single commit**. This is an atomic refactoring — command creation and content migration are logically one change. Ship as one commit, not separate ones. This ensures `git revert` restores everything cleanly (RISK-01 mitigation).
