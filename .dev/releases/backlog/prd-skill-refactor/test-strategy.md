---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 4
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
spec_source: prd-refactor-spec-v2.md
generated: "2026-04-04T03:04:51.582394+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — PRD Skill Refactoring

## 1. Validation Milestones Mapped to Roadmap Phases

| Validation Milestone | Roadmap Phase | Roadmap Milestones Covered | Gate Type |
|---------------------|---------------|---------------------------|-----------|
| **VM-1: Baseline Fidelity Gate** | Phase 1 (Foundation Verification) | M1 | Entry gate — blocks all subsequent phases |
| **VM-2: Artifact Completeness Gate** | After Phase 2 + Phase 3 | M2, M3, M4, M5 | Mid-point gate — validates both creation and decomposition before final verification |
| **VM-3: Final Acceptance Gate** | Phase 4 (Fidelity + Sync + Acceptance) | M6, M7 | Exit gate — blocks merge to integration |

**Interleave rationale (1:2)**: MEDIUM complexity means one validation milestone per two work milestones. Phase 2 produces two work milestones (M2, M3) validated together at VM-2. Phase 3 produces two work milestones (M4, M5) also validated at VM-2. This batching is safe because Phase 2 and Phase 3 outputs are independently diffable — if VM-2 fails, the failing phase is identifiable from diff output without ambiguity.

---

## 2. Issue Classification

| Severity | Definition | Action | Gate Impact |
|----------|-----------|--------|-------------|
| **CRITICAL** | Content loss detected in any diff; activation pattern broken; file missing entirely | stop-and-fix immediately | Blocks current phase |
| **MAJOR** | Stale cross-reference found; line count outside range; BUILD_REQUEST has wrong path count; content duplicated between command and SKILL.md | stop-and-fix before next phase | Blocks next phase |
| **MINOR** | Whitespace inconsistency beyond normalization; header formatting drift; `.gitkeep` presence/absence | Track and fix in next sprint | No gate impact |
| **COSMETIC** | Comment wording preferences; markdown style variations (e.g., `---` vs `***` for horizontal rules) | Backlog | No gate impact |

---

## 3. Test Categories

### 3.1 Structural Tests (Unit-equivalent)

Mechanical checks on individual files. No cross-file dependencies.

| Test ID | Target | Command | Pass Condition |
|---------|--------|---------|----------------|
| ST-01 | SKILL.md line count | `wc -l .claude/skills/prd/SKILL.md` | 400–500 |
| ST-02 | Command file line count | `wc -l .claude/commands/sc/prd.md` | 100–170 |
| ST-03 | refs/ file count | `ls .claude/skills/prd/refs/*.md \| wc -l` | 4 |
| ST-04 | Token budget estimate | ST-01 result × 4.5 | ≤ 2,025 |
| ST-05 | Combined line count | Sum `wc -l` across all 6 files | 1,380–1,520 |
| ST-06 | Command frontmatter fields | Grep for `name: prd`, `category: documentation`, `complexity: advanced` | All present |
| ST-07 | Command sections exist | Grep for `## Required Input`, `## Usage`, `## Arguments`, `## Options`, `## Behavioral Summary`, `## Examples`, `## Activation`, `## Boundaries`, `## Related Commands` | All 9 present |
| ST-08 | Activation pattern | Grep command file for `Skill prd` | Present |
| ST-09 | No protocol logic in command | Grep command file for `Stage A`, `Stage B`, `A\.1`, `A\.2`, `subagent`, `rf-task` | Zero matches |
| ST-10 | Loading declarations exist | Grep SKILL.md for `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` | All 4 present in A.7 section |

### 3.2 Fidelity Tests (Integration-equivalent)

Cross-file comparisons verifying content preservation between original and refactored artifacts.

| Test ID | Source (Original SKILL.md) | Destination | Method | Pass Condition |
|---------|---------------------------|-------------|--------|----------------|
| FT-01 | Lines 553–967 (agent prompts) | `refs/agent-prompts.md` | Diff (whitespace-normalized) | Zero content delta |
| FT-02 | Lines 1108–1254 (validation checklists) | `refs/validation-checklists.md` | Diff (whitespace-normalized) | Zero content delta |
| FT-03 | Lines 969–1106 (synthesis mapping) | `refs/synthesis-mapping.md` | Diff (whitespace-normalized) | Zero content delta |
| FT-04 | Lines 347–508 (BUILD_REQUEST) | `refs/build-request-template.md` | Diff | Exactly 6 path changes |
| FT-05 | Lines 46–60 (prompt examples) | `commands/sc/prd.md` Examples section | Grep for key example phrases | Content present in command |
| FT-06 | Lines 46–60 (prompt examples) | Refactored SKILL.md | Grep for key example phrases | Content absent from SKILL.md |
| FT-07 | Lines 79–85 (tier table) | `commands/sc/prd.md` Options section | Grep for tier names | Content present in command |
| FT-08 | Lines 79–85 (tier table) | Refactored SKILL.md | Grep for tier table headers | Content absent from SKILL.md |
| FT-09 | 8 named templates | `refs/agent-prompts.md` | Grep for 8 template headers | All 8 found |
| FT-10 | Lines 679–686 (web research topics) | `refs/agent-prompts.md` | Grep for "Common web research topics" | Present |
| FT-11 | 4 validation subsections | `refs/validation-checklists.md` | Grep for section headers | All 4 found |
| FT-12 | B30 QA paths | B05 in refactored SKILL.md | Grep for 6 QA path entries | All 6 present in B05 |
| FT-13 | Standalone B30 section | Refactored SKILL.md | Grep for B30 section header | Absent (merged into B05) |

### 3.3 Cross-Reference Integrity Tests (Integration-equivalent)

| Test ID | Scope | Method | Pass Condition |
|---------|-------|--------|----------------|
| XR-01 | SKILL.md + refs/ | `grep -n '".*section"'` across all files | Zero stale section-name references (except "Tier Selection") |
| XR-02 | `refs/build-request-template.md` | Grep for 6 specific refs/ paths | All 6 present |
| XR-03 | `refs/build-request-template.md` | Grep for `"Tier Selection" section` | Present (unchanged) |
| XR-04 | SKILL.md A.7 section | Verify orchestrator loads ≤ 2 files | Count file references in A.7 orchestrator context |
| XR-05 | SKILL.md A.1–A.6 | Grep for `refs/` in non-A.7 stages | Zero matches |
| XR-06 | Command vs SKILL.md | Grep for identical content blocks in both | Zero duplication (except cross-references) |

### 3.4 End-to-End Tests (Acceptance-equivalent)

| Test ID | Scenario | Method | Pass Condition |
|---------|----------|--------|----------------|
| E2E-01 | Activation | Invoke `/sc:prd test-product` | Skill prd loads; no error |
| E2E-02 | Behavioral regression | Compare output structure of refactored skill vs baseline | Identical structure |
| E2E-03 | Sync integrity | `make sync-dev && make verify-sync` | Exit code 0 |
| E2E-04 | Builder subagent path resolution | Spawn builder subagent from SKILL.md directory; verify it can read all 4 refs/ files | All files accessible |

---

## 4. Test-Implementation Interleaving Strategy

```
Phase 1: Foundation Verification
  ├── WORK: Diff 3 existing refs/ files (Steps 1.1–1.6)
  ├── WORK: Re-extract if drift found (Step 1.7)
  └── VM-1 GATE ─────────────────────────────────────
       Tests: FT-01, FT-02, FT-03, FT-09, FT-10, FT-11
       Pass condition: All 3 refs verified faithful
       Failure policy: CRITICAL — stop-and-fix (re-extract from SKILL.md)

Phase 2: Create Missing Artifacts
  ├── WORK: Create refs/build-request-template.md (Step 2.1)  ─┐
  └── WORK: Create commands/sc/prd.md (Step 2.2)               ─┤ parallel
       Inline checks: ST-02, ST-06, ST-07, ST-08, ST-09        │
                                                                 │
Phase 3: SKILL.md Decomposition                                  │
  ├── WORK: Remove 4 content blocks (Steps 3.1–3.4)             │
  ├── WORK: Remove migrated interface blocks (Steps 3.5–3.6)    │
  ├── WORK: Merge B30→B05 (Step 3.7)                            │
  ├── WORK: Add loading declarations (Steps 3.8–3.11)           │
  └── WORK: Update cross-references (Steps 3.12–3.13)           │
                                                                 │
  └── VM-2 GATE ─────────────────────────────────────────────────┘
       Tests: ST-01, ST-02, ST-03, ST-04, ST-05, ST-10,
              FT-04, FT-05, FT-06, FT-07, FT-08, FT-12, FT-13,
              XR-01, XR-02, XR-03, XR-04, XR-05, XR-06
       Pass condition: All structural + fidelity + cross-reference tests pass
       Failure policy:
         Line count outside range → MAJOR (stop-and-fix before Phase 4)
         Content loss in any diff → CRITICAL (stop-and-fix immediately)
         Stale reference found → MAJOR (stop-and-fix before Phase 4)

Phase 4: Fidelity Verification + Sync + Acceptance
  ├── WORK: Full fidelity diffs (Steps 4.1–4.8)     ─┐ parallel
  ├── WORK: Structural checks (Steps 4.7, 4.9)       ─┤
  ├── WORK: Sync (Steps 4.10–4.11)                    │
  └── WORK: E2E tests (Steps 4.12–4.13)               │
                                                       │
  └── VM-3 GATE ───────────────────────────────────────┘
       Tests: ALL (ST-01–ST-10, FT-01–FT-13, XR-01–XR-06, E2E-01–E2E-04)
       Pass condition: All 12 success criteria pass
       Failure policy:
         Any fidelity diff failure → CRITICAL (blocks merge)
         Sync failure → MAJOR (re-run make sync-dev)
         Activation failure → CRITICAL (fix activation pattern)
```

**Ratio justification**: The 1:2 interleave ratio means VM-2 validates both Phase 2 and Phase 3 together. This is appropriate because:
1. Phase 2 artifacts (command file, build-request ref) are inputs to Phase 3 (SKILL.md trimming references them)
2. Testing Phase 2 in isolation would require stub SKILL.md state that doesn't yet exist
3. Combined validation at VM-2 tests the actual integrated state after both phases complete
4. Phase 1 (VM-1) remains a standalone gate because all subsequent work depends on verified refs/

---

## 5. Risk-Based Test Prioritization

Tests ordered by risk severity and likelihood of catching regressions:

| Priority | Tests | Risk Addressed | Rationale |
|----------|-------|---------------|-----------|
| **P0 — Run first** | FT-01, FT-02, FT-03 | R1 (content loss), R5 (refs drift) | Content fidelity is the primary project risk. If refs/ have drifted, all downstream work is compromised. |
| **P1 — Run at every gate** | XR-01, FT-04, FT-06, FT-08 | R2 (cross-reference breakage), R4 (scope creep) | Stale references and content duplication are the most likely implementation errors. |
| **P2 — Run at VM-2, VM-3** | ST-01, ST-02, ST-05, ST-09, ST-10 | R1, NFR-PRD-R.1, NFR-PRD-R.5 | Structural checks validate governance compliance (500-line ceiling, thin command). |
| **P3 — Run at VM-3 only** | E2E-01, E2E-02, E2E-03, E2E-04 | R3 (activation), R8 (path resolution), NFR-PRD-R.4 | E2E tests are expensive and only meaningful after all artifacts are in final state. |
| **P4 — Run at VM-3** | FT-05, FT-07, FT-09, FT-10, FT-11, FT-12, FT-13 | R6, R7, R9 | Secondary fidelity checks for migrated content and merged sections. |

---

## 6. Acceptance Criteria per Milestone

### M1: Existing refs verified (VM-1 Gate)

| Criterion | Test(s) | Severity if Failed |
|-----------|---------|-------------------|
| `refs/agent-prompts.md` matches SKILL.md lines 553–967 | FT-01 | CRITICAL |
| `refs/validation-checklists.md` matches SKILL.md lines 1108–1254 | FT-02 | CRITICAL |
| `refs/synthesis-mapping.md` matches SKILL.md lines 969–1106 | FT-03 | CRITICAL |
| All 8 named templates present | FT-09 | CRITICAL |
| Web research topics list present | FT-10 | MAJOR |
| All 4 validation subsections present | FT-11 | MAJOR |

### M2: build-request-template.md created

| Criterion | Test(s) | Severity if Failed |
|-----------|---------|-------------------|
| File exists at correct path | ST-03 (partial) | CRITICAL |
| Exactly 6 path changes from original | FT-04 | CRITICAL |
| "Tier Selection" reference unchanged | XR-03 | MAJOR |
| All 6 refs/ paths correct | XR-02 | CRITICAL |

### M3: prd.md command created

| Criterion | Test(s) | Severity if Failed |
|-----------|---------|-------------------|
| Line count 100–170 | ST-02 | MAJOR |
| All 9 required sections present | ST-07 | CRITICAL |
| Correct frontmatter | ST-06 | MAJOR |
| `Skill prd` activation pattern | ST-08 | CRITICAL |
| Zero protocol logic | ST-09 | CRITICAL |
| B03 examples present | FT-05 | MAJOR |
| B04 tier table present | FT-07 | MAJOR |

### M4: SKILL.md trimmed to 400–500 lines

| Criterion | Test(s) | Severity if Failed |
|-----------|---------|-------------------|
| Line count 400–500 | ST-01 | CRITICAL (if >500), MAJOR (if <400) |
| Token budget ≤ 2,025 | ST-04 | MAJOR |
| Loading declarations present in A.7 | ST-10 | CRITICAL |
| B03 absent from SKILL.md | FT-06 | MAJOR |
| B04 table absent from SKILL.md | FT-08 | MAJOR |
| B30 merged into B05 | FT-12, FT-13 | MAJOR |

### M5: Cross-references clean

| Criterion | Test(s) | Severity if Failed |
|-----------|---------|-------------------|
| Zero stale section references | XR-01 | MAJOR |
| No refs/ loading outside A.7 | XR-05 | MAJOR |
| Orchestrator loads ≤ 2 files | XR-04 | MAJOR |
| No content duplication command↔SKILL.md | XR-06 | MAJOR |

### M6: Fidelity verified

| Criterion | Test(s) | Severity if Failed |
|-----------|---------|-------------------|
| All 8 template diffs clean | FT-01, FT-09 | CRITICAL |
| All checklist diffs clean | FT-02, FT-11 | CRITICAL |
| Synthesis mapping diff clean | FT-03 | CRITICAL |
| BUILD_REQUEST diff shows only 6 changes | FT-04 | CRITICAL |
| Combined line count 1,380–1,520 | ST-05 | MAJOR |
| refs/ contains exactly 4 .md files | ST-03 | MAJOR |

### M7: Sync + activation confirmed

| Criterion | Test(s) | Severity if Failed |
|-----------|---------|-------------------|
| `make verify-sync` exits 0 | E2E-03 | CRITICAL |
| `/sc:prd` triggers skill load | E2E-01 | CRITICAL |
| Output structure matches baseline | E2E-02 | CRITICAL |
| Builder subagent resolves refs/ paths | E2E-04 | MAJOR |

---

## 7. Quality Gates Between Phases

### Gate G1: Phase 1 → Phase 2

**Gatekeeper**: VM-1
**Blocking tests**: FT-01, FT-02, FT-03 (all CRITICAL)
**Decision matrix**:

| Outcome | Action |
|---------|--------|
| All 3 diffs clean | Proceed to Phase 2 |
| 1+ diffs show content delta | CRITICAL: Re-extract affected refs/ from current SKILL.md, re-run VM-1 |
| Structural checks fail (missing templates/sections) | CRITICAL: Investigate and fix before proceeding |

### Gate G2: Phase 2 + Phase 3 → Phase 4

**Gatekeeper**: VM-2
**Blocking tests**: ST-01, ST-02, FT-04, XR-01, XR-02 (CRITICAL and MAJOR)
**Decision matrix**:

| Outcome | Action |
|---------|--------|
| All tests pass | Proceed to Phase 4 |
| SKILL.md > 500 lines | CRITICAL: Identify untrimmed content, remove to correct destination |
| SKILL.md < 400 lines | MAJOR: Verify no content was dropped (not just moved) |
| Stale references found | MAJOR: Update references before Phase 4 |
| BUILD_REQUEST has ≠ 6 path changes | CRITICAL: Review cross-reference map, correct paths |
| Content found in both command and SKILL.md | MAJOR: Remove from SKILL.md (command is canonical for interface content) |

### Gate G3: Phase 4 → Merge

**Gatekeeper**: VM-3
**Blocking tests**: All 33 tests (ST-01–10, FT-01–13, XR-01–06, E2E-01–04)
**Decision matrix**:

| Outcome | Action |
|---------|--------|
| All 12 success criteria pass | Approve merge to integration branch |
| Any fidelity diff failure | CRITICAL: Content loss — restore from `git show HEAD~1:path` and re-apply changes |
| `make verify-sync` fails | MAJOR: Re-run `make sync-dev`, investigate desync |
| Activation failure | CRITICAL: Fix activation pattern in command file, re-test |
| E2E behavioral regression | CRITICAL: Compare output diff, identify structural change, revert and re-apply |

**Rollback trigger**: 2+ CRITICAL failures at VM-3 → rollback entire refactoring via `git checkout -- .claude/skills/prd/ .claude/commands/sc/prd.md` and restart from Phase 1.

---

## 8. Test Execution Checklist

```
VM-1 (after Phase 1):
  □ P0: FT-01, FT-02, FT-03 — refs/ fidelity diffs
  □ P1: FT-09, FT-10, FT-11 — structural completeness
  GATE G1: All pass → proceed

VM-2 (after Phase 2 + Phase 3):
  □ P1: XR-01, FT-04, FT-06, FT-08 — cross-refs + migration
  □ P2: ST-01, ST-02, ST-03, ST-05, ST-09, ST-10 — structural
  □ P2: XR-02, XR-03, XR-04, XR-05, XR-06 — reference integrity
  □ P4: FT-05, FT-07, FT-12, FT-13 — secondary fidelity
  □ P2: ST-04, ST-06, ST-07, ST-08 — command structure
  GATE G2: All pass → proceed

VM-3 (after Phase 4):
  □ P0: FT-01, FT-02, FT-03 — re-run refs/ diffs (final state)
  □ P1–P4: All remaining tests — full sweep
  □ P3: E2E-01, E2E-02, E2E-03, E2E-04 — end-to-end
  GATE G3: All 12 success criteria pass → approve merge
```
