---
spec_source: "tdd-command-layer-spec.md"
complexity_score: 0.25
adversarial: true
---

# Final Merged Roadmap: TDD Command Layer Refactor

## 1. Executive Summary

This roadmap covers the creation of a thin command layer for the TDD skill (`commands/sc/tdd.md`) and the migration of ~23 lines of interface-concern content from `SKILL.md` to the new command file. The work resolves an architectural violation documented in Developer Guide Section 9.3: every skill must have a command in front of it.

**Scope**: 2 new files (canonical + sync-derived dev copy), 2 modified files (SKILL.md canonical + dev copy), ~130 new lines, ~23 lines relocated. Zero behavioral changes. Complexity: LOW (0.25).

**Gold-standard pattern**: `commands/sc/adversarial.md` (167 lines) defines the structural template. The TDD command follows this pattern exactly.

**Architectural priorities**:
1. Enforce strict layer boundaries — command owns interface concerns, skill owns protocol (FR-TDD-CMD.1m, NFR-TDD-CMD.2).
2. Preserve behavior exactly — zero changes to Stage A/B, critical rules, session management, loading declarations, or refs/ files (FR-TDD-CMD.3d–3f, NFR-TDD-CMD.5).
3. Maintain source-of-truth and sync guarantees — canonical edits in `src/superclaude/` only; dev copies produced exclusively via `make sync-dev` (Architectural Constraints #2, #7; SC-12).

**Estimated work-time**: ~85 minutes for a single implementer or Claude session. Calendar time may vary with review cycles.

---

## 2. Phased Implementation Plan

### Phase 1: Preparation & Template Study

**Objective**: Read all reference materials, confirm current state matches extraction assumptions, and freeze baseline for verification.

**Tasks**:
1. Read `commands/sc/adversarial.md` — internalize section ordering, frontmatter fields, activation pattern, boundaries format
2. Read `skills/tdd/SKILL.md` — confirm current line count (expected: 438), locate migration blocks:
   - Lines 48–63: Effective Prompt Examples (~16 lines)
   - Lines 82–88: Tier Selection table (header + 3 data rows, ~7 lines)
3. Read Developer Guide Section 9.3 (separation of concerns) and Section 5.10 (checklist)
4. **MANDATORY: Snapshot pre-migration state before any edits** — record `wc -l` on SKILL.md, `git diff --stat` baseline, and save copies of migration blocks for Phase 4 diffing

**Milestone**: All reference material read. Migration blocks confirmed at expected line ranges. Baseline measurements recorded and reviewable.

**Requirement coverage**: FR-TDD-CMD.3d, FR-TDD-CMD.3e, FR-TDD-CMD.3f, NFR-TDD-CMD.5

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
   - **Examples** (FR-TDD-CMD.1h): 5–6 examples (3 strong, 2 weak annotated, 1 resume/tier override)
   - **Activation** (FR-TDD-CMD.1i): `> Skill tdd` with "Do NOT proceed" guard
   - **Boundaries** (FR-TDD-CMD.1j): Will/Will Not list
   - **Related Commands** (FR-TDD-CMD.1k): `/sc:prd`, `/sc:design`, `/sc:workflow`, `/sc:brainstorm`
2. Verify line count: 100–170 lines (NFR-TDD-CMD.1, FR-TDD-CMD.1l)
3. Verify zero protocol leakage (NFR-TDD-CMD.2, FR-TDD-CMD.1m): grep for `Stage A`, `Stage B`, `rf-task-builder`, `subagent` returns 0 matches

**Named Artifacts / Integration Points**:
- **Activation handoff**: The `## Activation` section wires the command to the skill via `> Skill tdd`. Created in this phase, consumed by Claude Code's skill dispatch at runtime.
- **Options table**: Documents the 7 flags that the skill's Input section interprets. Created here, cross-referenced by Phase 3 (tier table migration populates the `--tier` row).

**Milestone**: `src/superclaude/commands/tdd.md` exists, passes line budget (100–170), passes zero-leakage grep.

**Requirement coverage**: FR-TDD-CMD.1a–1m, NFR-TDD-CMD.1, NFR-TDD-CMD.2, NFR-TDD-CMD.4

**Duration**: ~30 minutes

---

### Phase 3: Content Migration (FR-TDD-CMD.2)

**Objective**: Migrate ~23 lines of interface-concern content from SKILL.md to the command file, then remove from SKILL.md.

**Tasks**:
1. **Migrate prompt examples** (FR-TDD-CMD.2a): Copy SKILL.md lines 48–63 (3 strong + 2 weak examples) into command Examples section. Adapt to command invocation syntax (e.g., prefix with `/sc:tdd`).
2. **Migrate tier table** (FR-TDD-CMD.2b): Copy SKILL.md lines 82–88 (header + 3 data rows) into command Options section as `--tier` reference material.
3. **Remove migrated content from SKILL.md**:
   - Remove Effective Prompt Examples block (lines 48–63) — FR-TDD-CMD.2e
   - Remove tier table rows (lines 82–88), retain introductory sentence + selection rules (lines 90–94) — FR-TDD-CMD.2d
   - Retain 4-input description (lines 34–46) and "What to Do If Prompt Is Incomplete" template (lines 65–76) — FR-TDD-CMD.2c
4. Verify SKILL.md post-migration line count: 400–440 lines (NFR-TDD-CMD.3, FR-TDD-CMD.2f)
5. Verify no duplication — grep for distinctive example strings in both files; each should appear in exactly one (FR-TDD-CMD.2e)

**Named Artifacts / Integration Points**:
- **SKILL.md Input section**: Retains the 4-input structure and incomplete-prompt template. Command's Examples section now owns the concrete examples. The skill reads inputs; the command documents them for users.
- **SKILL.md Tier Selection section**: Retains selection rules (lines 90–94). Command's Options table now owns the tier comparison table. The skill applies rules; the command presents the reference.

**Milestone**: Content migrated. SKILL.md within 400–440 lines. No duplication across files.

**Requirement coverage**: FR-TDD-CMD.2a–2f, NFR-TDD-CMD.3

**Duration**: ~20 minutes

---

### Phase 4: Fidelity Verification (FR-TDD-CMD.3)

**Objective**: Verify migration correctness with zero collateral damage. This phase is a **hard gate** — if any check fails, do not proceed to Phase 5.

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
6. **Migrated content removed from SKILL.md** (SC-8): Grep SKILL.md for distinctive migrated strings — 0 matches

**Parallelization note**: The 26 verification checks above are independent and can be batched into parallel grep/diff/wc invocations for efficiency.

**Milestone**: All 26 verification checks pass. Zero collateral damage confirmed.

**Requirement coverage**: FR-TDD-CMD.3a–3f, NFR-TDD-CMD.2, NFR-TDD-CMD.4, NFR-TDD-CMD.5

**Duration**: ~10 minutes

---

### Phase 5: Sync, Evidence & Commit

**Objective**: Propagate changes through the component sync pipeline, optionally produce evidence report, and commit.

**Tasks**:
1. Run `make sync-dev` — propagates `src/superclaude/commands/tdd.md` to `.claude/commands/sc/tdd.md` and SKILL.md changes to `.claude/skills/tdd/SKILL.md`
2. Run `make verify-sync` — confirm exit code 0 (SC-12)
3. Verify both file locations exist (SC-1):
   - `src/superclaude/commands/tdd.md`
   - `.claude/commands/sc/tdd.md`
4. Final validation pass on dev copies (repeat key checks from Phase 4 on `.claude/` copies)
5. **Conditional evidence report**: If this refactor pattern will repeat for other skills (PRD, design, etc.), produce a short evidence report mapping each SC and FR/NFR to its verification result. This takes ~15 minutes and serves as a reusable template for subsequent skill refactors.
6. Commit as a **single atomic commit**: `refactor(tdd): create command layer and migrate interface content from SKILL.md`

**Named Artifacts / Integration Points**:
- **`make sync-dev` pipeline**: Reads from `src/superclaude/commands/` and `src/superclaude/skills/`, writes to `.claude/commands/sc/` and `.claude/skills/`. This phase triggers the pipeline; all prior phases edit only canonical sources.
- **`make verify-sync` check**: Validates parity between `src/` and `.claude/`. Must pass before commit.

**Milestone**: Both canonical and dev-copy locations populated. `make verify-sync` passes. Changes committed as single atomic unit.

**Requirement coverage**: SC-1, SC-12

**Duration**: ~10 minutes (+ ~15 minutes if evidence report is produced)

---

## 3. Risk Assessment and Mitigation

| Risk ID | Risk | Severity | Probability | Mitigation | Gate |
|---------|------|----------|-------------|------------|------|
| RISK-01 | Content loss during migration — ~23 lines partially lost or corrupted | Low | Very Low | Migration blocks are contiguous (lines 48–63, 82–88); Phase 1 snapshot enables precise diff verification in Phase 4 | FR-TDD-CMD.3a/3b/3c, SC-6/SC-7/SC-8 |
| RISK-02 | Protocol leakage into command — Stage A/B details or agent spawning in command file | Medium | Low | Author against adversarial gold standard; automated grep for prohibited keywords in Phase 2 and Phase 4 | FR-TDD-CMD.1m, NFR-TDD-CMD.2, SC-5 |
| RISK-03 | Scope creep — temptation to improve TDD content while refactoring | Medium | Low | Strict boundary: only create command + relocate content. Zero behavioral changes. Phase 4 verification gates enforce this. **Any newly discovered ambiguity must be logged as a change request, not solved by in-scope expansion** — this protects FR-TDD-CMD.3d–f and NFR-TDD-CMD.5. | FR-TDD-CMD.3d/3e/3f, NFR-TDD-CMD.5, SC-10/SC-11 |
| RISK-04 | Sync failure — command created in `.claude/` instead of `src/` | Low | Low | Always edit `src/superclaude/` first. Dev copies are produced exclusively via `make sync-dev`. `make verify-sync` catches drift in Phase 5. | FR-TDD-CMD.1a, SC-1, SC-12 |
| RISK-05 | Prompt examples lose context when adapted to command syntax | Low | Very Low | Examples are self-contained strings; command provides equivalent framing. Visual review in Phase 4. | FR-TDD-CMD.3a/3b, SC-6 |

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

All 12 success criteria from the extraction are validated across Phases 2–5:

| SC | Criterion | Phase | Method |
|----|-----------|-------|--------|
| SC-1 | Command file exists at both locations | 5 | `test -f` on `src/superclaude/commands/tdd.md` and `.claude/commands/sc/tdd.md` |
| SC-2 | Command file 100–170 lines | 2 | `wc -l` |
| SC-3 | All 7 flags in Options table | 2 | Grep for each flag name |
| SC-4 | Activation section contains `Skill tdd` | 2 | Grep |
| SC-5 | Zero protocol leakage | 2, 4 | Grep for prohibited keywords returns 0 |
| SC-6 | All prompt examples in command | 4 | Grep for distinctive strings from 3 strong + 2 weak examples |
| SC-7 | Tier table in command | 4 | Grep for `Lightweight`, `Standard`, `Heavyweight` rows |
| SC-8 | Migrated content removed from SKILL.md | 4 | Grep for migrated strings in SKILL.md returns 0 |
| SC-9 | SKILL.md 400–440 lines post-migration | 3 | `wc -l` |
| SC-10 | Behavioral protocol unmodified | 4 | Section-level diff pre/post against Phase 1 snapshot |
| SC-11 | All 5 refs/ files unmodified | 4 | `git diff` on refs/ directory |
| SC-12 | `make verify-sync` passes | 5 | Exit code 0 |

### Traceability Rule

Every phase closes with explicit FR/NFR/SC requirement coverage before progressing. Coverage IDs are listed at the end of each phase above.

### Validation Approach

Verification is integrated into each phase, not deferred to the end. Phase 2 checks structural correctness. Phase 3 checks migration completeness. Phase 4 is the full fidelity gate (hard stop on failure). Phase 5 confirms sync pipeline integrity.

---

## 6. Timeline Estimates

| Phase | Description | Estimated Duration | Cumulative |
|-------|-------------|-------------------|------------|
| 1 | Preparation & Template Study | ~15 min | ~15 min |
| 2 | Command File Creation | ~30 min | ~45 min |
| 3 | Content Migration | ~20 min | ~65 min |
| 4 | Fidelity Verification | ~10 min | ~75 min |
| 5 | Sync, Evidence & Commit | ~10 min | ~85 min |

**Total estimated work-time**: ~85 minutes for a single implementer or Claude session. If an evidence report is produced (recommended when pattern will repeat), add ~15 minutes.

**Calendar-time note**: For team execution with review cycles, allow up to half a working day. The 85-minute figure represents unbroken execution time, not calendar allocation.

**Critical path**: Phase 2 (command creation) is the longest phase and the foundation for Phase 3. Phases 4 and 5 are lightweight verification and pipeline steps.

**Parallelization**: Within Phase 4, the 26 verification checks are independent and can be batched into parallel grep/diff/wc invocations.

---

## 7. Architect Recommendations

1. **Follow the template exactly.** The adversarial.md gold standard exists precisely so that new commands are structurally identical. Resist any urge to innovate on section ordering or naming.

2. **Edit canonical sources only.** Every change goes to `src/superclaude/` first. The `.claude/` copies are derived artifacts produced exclusively by `make sync-dev` — never create or edit them manually.

3. **Snapshot before migration.** Before touching SKILL.md in Phase 3, record `wc -l` and save a copy of the migration blocks. This makes Phase 4 verification trivial.

4. **Treat Phase 4 as a hard gate.** If any verification check fails, do not proceed to Phase 5. Fix the issue and re-verify. The 26 checks are cheap; the cost of committing a broken migration is not.

5. **Single atomic commit.** This is an atomic refactoring — command creation and content migration are logically one change. Ship as one commit, not separate ones. This ensures `git bisect` never hits a broken intermediate state and `git revert` restores everything cleanly.

6. **Formal traceability.** Every phase must close with explicit FR/NFR/SC mapping before the implementer progresses. The requirement coverage lines at the end of each phase section are not decorative — they are the verification that the phase delivered its contracted requirements.

7. **Scope discipline on ambiguity.** Any newly discovered ambiguity during implementation must be logged as a change request, not solved by in-scope expansion. This protects the zero-behavioral-change guarantee (FR-TDD-CMD.3d–f, NFR-TDD-CMD.5) from well-intentioned but scope-violating "fixes."
