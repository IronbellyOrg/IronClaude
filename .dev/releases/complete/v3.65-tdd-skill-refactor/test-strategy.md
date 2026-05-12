---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 5
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
spec_source: tdd-refactor-spec.md
generated: "2026-04-03T05:57:16.666422+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy: TDD Skill Refactoring

## 1. Validation Milestones Mapped to Roadmap Phases

The 1:2 interleave ratio (MEDIUM complexity) produces 3 validation milestones across 5 work phases:

| Validation Milestone | After Phases | Scope |
|---------------------|-------------|-------|
| **VM-1: Baseline & Extraction Gate** | Phase 1 + Phase 2 | Fidelity index verified, all 5 refs files exist with zero drift |
| **VM-2: Wiring & Reduction Gate** | Phase 3 + Phase 4 | Cross-references resolve, SKILL.md <500 lines, phase contracts valid |
| **VM-3: Acceptance Gate** | Phase 5 | All 14 SC criteria pass, behavioral parity confirmed |

### Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | stop-and-fix immediately | Blocks current phase |
| MAJOR | stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

**Classification examples for this refactor**:
- CRITICAL: Content loss in extracted block, fidelity index range mismatch with actual file
- MAJOR: BUILD_REQUEST reference points to nonexistent file, phase contract violation (`declared_loads ∩ forbidden_loads ≠ ∅`)
- MINOR: Trailing whitespace inconsistency beyond normalization policy
- COSMETIC: Load-point replacement marker wording preference

---

## 2. Test Categories

### 2.1 Unit Tests (per-file, per-block validation)

| ID | Test | Phase | Method | Severity if Fails |
|----|------|-------|--------|--------------------|
| U-01 | `wc -l` on canonical SKILL.md = 1,387 before migration | 1 | Shell command | CRITICAL |
| U-02 | Each block B01–B34 checksum markers (first 10 / last 10 words) match actual file at stated ranges | 1 | Script: extract range, compare boundary words | CRITICAL |
| U-03 | Fidelity index covers lines 1–1387 with zero unmapped content lines | 1 | Coverage audit script | CRITICAL |
| U-04 | Each refs file exists at `src/superclaude/skills/tdd/refs/<name>` | 2 | `ls` / `test -f` | CRITICAL |
| U-05 | Block-wise diff per refs file against source ranges = empty (after normalization) | 2 | `diff` with whitespace normalization | CRITICAL |
| U-06 | `refs/agent-prompts.md` contains exactly 8 named prompts | 2 | `grep -c` for prompt headers | MAJOR |
| U-07 | `refs/validation-checklists.md` numbering matches source | 2 | Structural diff on numbered lines | MAJOR |
| U-08 | Sentinel grep: `{{`, `<placeholder>`, `TODO`, `FIXME` = 0 matches across all refs | 2 | `grep -rn` | MAJOR |
| U-09 | Exactly 6 path-reference changes in `refs/build-request-template.md` vs source B12 | 3 | `diff` line count | CRITICAL |
| U-10 | All 6 updated references match expected target paths | 3 | `grep` for each expected path | CRITICAL |
| U-11 | Zero original section-name references remain in build-request-template | 3 | `grep` for old reference strings | MAJOR |
| U-12 | `wc -l` on refactored SKILL.md < 500 | 4 | Shell command | CRITICAL |
| U-13 | Behavioral blocks B01–B11, B13, B14 present and unchanged in refactored SKILL.md | 4 | Checksum marker verification | CRITICAL |
| U-14 | Loading declarations present for Stage A.7 and Stage B | 4 | `grep` for `refs/build-request-template.md` directive and builder load declarations | MAJOR |
| U-15 | No HOW content remains in SKILL.md (no agent prompts, checklists, mapping tables, BUILD_REQUEST body) | 4 | `grep` for content block signatures | MAJOR |

### 2.2 Integration Tests (cross-file, cross-system)

| ID | Test | Phase | Method | Severity if Fails |
|----|------|-------|--------|--------------------|
| I-01 | All 6 BUILD_REQUEST path references resolve to existing files under `src/superclaude/skills/tdd/` | 3 | Script: extract paths, `test -f` each | CRITICAL |
| I-02 | Phase contract validation: `declared_loads ∩ forbidden_loads = ∅` for every phase | 4 | Parse contract matrix, compute set intersection | CRITICAL |
| I-03 | `make sync-dev` completes without error | 5 | Shell execution | CRITICAL |
| I-04 | `make verify-sync` exits 0 | 5 | Shell execution | CRITICAL |
| I-05 | All 5 refs files exist at `.claude/skills/tdd/refs/` after sync | 5 | `ls` | CRITICAL |
| I-06 | Dev copy refs content matches canonical refs content | 5 | `diff -r` | MAJOR |
| I-07 | Extracted file set matches phase loading contract documented in Phase 1 (no extra, no missing refs files) | 2 | Set comparison | MAJOR |

### 2.3 End-to-End Tests (behavioral parity)

| ID | Test | Phase | Method | Severity if Fails |
|----|------|-------|--------|--------------------|
| E-01 | TDD skill invocation on trivial component: Stage A completes through A.7 | 5 | Dry run execution | CRITICAL |
| E-02 | BUILD_REQUEST generated at A.7 contains correct refs paths (not old section references) | 5 | Inspect generated BUILD_REQUEST output | CRITICAL |
| E-03 | Stage B delegation succeeds (rf-task-builder receives and can read all 4 builder refs) | 5 | Dry run execution | CRITICAL |
| E-04 | Token count comparison: post-refactor SKILL.md tokens < pre-refactor | 5 | Token counting tool/script | MAJOR |

### 2.4 Acceptance Tests (success criteria matrix)

The 14 success criteria (SC-1 through SC-14) serve as the acceptance test suite. Each maps to specific unit/integration/E2E tests above:

| SC | Acceptance Test | Maps To |
|----|----------------|---------|
| SC-1 | SKILL.md < 500 lines | U-12 |
| SC-2 | 5/5 refs files in canonical location | U-04 |
| SC-3 | 5/5 refs files synced to dev | I-05 |
| SC-4 | `make verify-sync` passes | I-04 |
| SC-5 | Fidelity index 100% coverage | U-03 |
| SC-6 | Zero textual drift | U-05 |
| SC-7 | Only allowlisted transforms | U-09 |
| SC-8 | No sentinel placeholders | U-08 |
| SC-9 | Phase contract conformance | I-02 |
| SC-10 | BUILD_REQUEST refs resolve | I-01 |
| SC-11 | 8 agent prompts present | U-06 |
| SC-12 | Checklist numbering preserved | U-07 |
| SC-13 | Stage A/B behavioral parity | E-01, E-02, E-03 |
| SC-14 | Token reduction confirmed | E-04 |

---

## 3. Test-Implementation Interleaving Strategy

### Ratio Justification

**1:2 (MEDIUM)** is appropriate because:
- Complexity score 0.53 places this firmly in MEDIUM territory
- The task is procedural (extract, relocate, verify) but carries HIGH fidelity risk (3 of 5 identified risks are HIGH severity)
- Each phase has hard quality gates already built into the roadmap — the 1:2 ratio adds validation milestones that aggregate phase gates into cross-cutting checks
- Going to 1:1 would add overhead without proportional risk reduction given the procedural nature; going to 1:3 would leave too large a gap between the extraction (Phase 2) and wiring (Phase 3) where cross-reference breakage could compound

### Interleaving Schedule

```
Phase 1 (Baseline)     → Execute → Phase Gate
Phase 2 (Extraction)   → Execute → Phase Gate
                        ════════════════════════
                        VM-1: Baseline & Extraction Gate
                        - Run: U-01 through U-08, I-07
                        - Cross-cutting gates: A (structural), C (fidelity) partial
                        - STOP if any CRITICAL/MAJOR failures
                        ════════════════════════
Phase 3 (Wiring)       → Execute → Phase Gate
Phase 4 (Reduction)    → Execute → Phase Gate
                        ════════════════════════
                        VM-2: Wiring & Reduction Gate
                        - Run: U-09 through U-15, I-01, I-02
                        - Cross-cutting gates: B (contract), C (fidelity) complete
                        - STOP if any CRITICAL/MAJOR failures
                        ════════════════════════
Phase 5 (Sync & Accept)→ Execute → Phase Gate
                        ════════════════════════
                        VM-3: Acceptance Gate
                        - Run: I-03 through I-06, E-01 through E-04
                        - Cross-cutting gates: A+B+C+D all finalized
                        - All 14 SC criteria must pass
                        ════════════════════════
```

### Parallel Test Execution Within Milestones

At each VM, independent tests run in parallel where possible:

- **VM-1**: U-04 through U-08 can run in parallel (one per refs file) after U-01 through U-03 complete sequentially
- **VM-2**: U-09 through U-11 (wiring tests) parallel with U-12 through U-15 (reduction tests) since they target different files. I-01 and I-02 run after both groups complete
- **VM-3**: I-03 must precede I-04 through I-06. E-01 through E-04 run sequentially (each stage depends on prior)

---

## 4. Risk-Based Test Prioritization

Tests are ordered by risk severity and detection value:

### Priority 1 — CRITICAL Risk Mitigation (run first at each VM)

| Risk | Tests | Rationale |
|------|-------|-----------|
| R1: Content loss (HIGH) | U-02, U-03, U-05 | Silent behavioral alteration. Fidelity index range verification and block-wise diff are the primary defense |
| R2: Cross-reference breakage (HIGH) | U-09, U-10, I-01 | Stage A.7 silent failure. Must catch before behavioral parity testing |
| R4: Semantic drift in quality gates (HIGH) | U-07, U-08 | Altered checklists produce different validation outcomes |

### Priority 2 — Structural Completeness (run second)

| Risk | Tests | Rationale |
|------|-------|-----------|
| R5: Source length discrepancy (MEDIUM) | U-01, U-02 | Foundation for all subsequent work; if wrong, everything shifts |
| R3: Wrong loading order (MEDIUM) | I-02, U-14 | Builder spawned without context; caught by contract validation |

### Priority 3 — Integration & Behavioral (run after structural is clean)

| Tests | Rationale |
|-------|-----------|
| I-03, I-04, I-05, I-06 | Sync pipeline — depends on all canonical files being correct first |
| E-01, E-02, E-03 | Behavioral parity — most expensive tests, only meaningful after all content verified |

### Priority 4 — Measurement (run last)

| Tests | Rationale |
|-------|-----------|
| E-04, U-12 | Token reduction and line count are outcome metrics, not risk gates |

---

## 5. Acceptance Criteria Per Milestone

### VM-1: Baseline & Extraction Gate

**Entry**: Phase 1 + Phase 2 complete with phase-level verification gates passing.

| Criterion | Threshold | Test IDs |
|-----------|-----------|----------|
| Fidelity index anchored to 1,387 lines | 100% block coverage, zero unmapped lines | U-01, U-02, U-03 |
| OQ-1 through OQ-5 resolved | All 5 documented with answers | Manual review |
| 5 refs files exist at canonical paths | 5/5 | U-04 |
| Zero textual drift in all extractions | Block-wise diff empty after normalization | U-05 |
| 8 agent prompts in agent-prompts.md | 8/8 | U-06 |
| Checklist structure preserved | Numbering match | U-07 |
| No sentinel placeholders | 0 grep matches | U-08 |
| File set matches loading contract | No extra, no missing | I-07 |

**Exit**: All CRITICAL and MAJOR tests pass. MINOR issues logged but do not block.

### VM-2: Wiring & Reduction Gate

**Entry**: VM-1 passed. Phase 3 + Phase 4 complete.

| Criterion | Threshold | Test IDs |
|-----------|-----------|----------|
| Exactly 6 path-reference changes | Diff shows 6 and only 6 changes | U-09 |
| All updated refs match target paths | 6/6 grep matches | U-10 |
| No old section-name references remain | 0 grep matches | U-11 |
| All refs resolve to existing files | 6/6 file existence | I-01 |
| SKILL.md < 500 lines | Strictly less | U-12 |
| Behavioral blocks unchanged | B01–B11, B13, B14 checksum match | U-13 |
| Loading declarations present | Stage A.7 + Stage B directives found | U-14 |
| No HOW content in SKILL.md | 0 matches for content block signatures | U-15 |
| Phase contract valid | `declared_loads ∩ forbidden_loads = ∅` | I-02 |

**Exit**: All CRITICAL and MAJOR tests pass. Zero open CRITICAL issues from VM-1.

### VM-3: Acceptance Gate

**Entry**: VM-2 passed. Phase 5 complete.

| Criterion | Threshold | Test IDs |
|-----------|-----------|----------|
| `make sync-dev` succeeds | Exit 0 | I-03 |
| `make verify-sync` passes | Exit 0, zero drift | I-04 |
| Dev copy refs complete | 5/5 files | I-05 |
| Dev-canonical parity | `diff -r` empty | I-06 |
| Stage A completes through A.7 | BUILD_REQUEST generated | E-01 |
| BUILD_REQUEST has correct refs paths | New paths present, old absent | E-02 |
| Stage B delegation succeeds | Builder reads all 4 refs | E-03 |
| Token reduction confirmed | Post < Pre | E-04 |
| All 14 SC criteria | 14/14 pass | Full SC matrix |

**Exit**: All 14 success criteria pass. All 4 cross-cutting gates (A–D) satisfied. Zero open CRITICAL or MAJOR issues.

---

## 6. Quality Gates Between Phases

### Gate Structure

Each phase boundary has a **phase gate** (defined in the roadmap). Validation milestones add **cross-cutting gates** that verify properties spanning multiple phases.

```
┌─────────┐   Phase    ┌─────────┐   Phase    ┌─────────────┐
│ Phase 1  │──Gate 1──▶│ Phase 2  │──Gate 2──▶│   VM-1      │
└─────────┘           └─────────┘           │ Cross-cut   │
                                             │ validation  │
                                             └──────┬──────┘
                                                    │
┌─────────┐   Phase    ┌─────────┐   Phase    ┌─────────────┐
│ Phase 3  │──Gate 3──▶│ Phase 4  │──Gate 4──▶│   VM-2      │
└─────────┘           └─────────┘           │ Cross-cut   │
                                             │ validation  │
                                             └──────┬──────┘
                                                    │
                      ┌─────────┐   Phase    ┌─────────────┐
                      │ Phase 5  │──Gate 5──▶│   VM-3      │
                      └─────────┘           │ Acceptance  │
                                             └─────────────┘
```

### Phase Gate Definitions

**Gate 1 (Phase 1 → Phase 2)**: Baseline locked
- Corrected fidelity index with verified ranges for all 34 blocks
- OQ-1 through OQ-5 resolved
- Phase loading contract matrix documented
- **Blocker if fails**: No content migration may begin with unverified ranges

**Gate 2 (Phase 2 → VM-1)**: Extraction complete
- All 5 refs files exist with zero drift
- Phase 2 verification gate criteria met
- **Blocker if fails**: Cannot wire references to nonexistent files

**Gate 3 (Phase 3 → Phase 4)**: References wired
- 6 path-reference updates applied and validated
- All references resolve to existing files
- **Blocker if fails**: Removing content from SKILL.md before references are wired creates broken state

**Gate 4 (Phase 4 → VM-2)**: Reduction complete
- SKILL.md < 500 lines with behavioral protocol intact
- Phase contracts encoded and valid
- **Blocker if fails**: Sync would propagate an incomplete SKILL.md

**Gate 5 (Phase 5 → VM-3)**: Sync & final verification
- All sync operations succeed
- Full fidelity audit complete
- Behavioral parity dry run passed
- **Blocker if fails**: Refactoring not accepted

### Cross-Cutting Gate Matrix

| Gate | Concern | Tests Required | Pass Threshold |
|------|---------|---------------|----------------|
| **Gate A**: Structural completeness | SC-1, SC-2, SC-3 | U-04, U-12, I-05 | All 3 SC pass |
| **Gate B**: Sync & contract integrity | SC-4, SC-9, SC-10 | I-04, I-02, I-01 | All 3 SC pass |
| **Gate C**: Fidelity & semantic immutability | SC-5, SC-6, SC-7, SC-8, SC-11, SC-12 | U-03, U-05, U-09, U-08, U-06, U-07 | All 6 SC pass |
| **Gate D**: Runtime behavioral parity | SC-13, SC-14 | E-01–E-04 | All 2 SC pass |

### Regression Protocol

When a CRITICAL or MAJOR issue is found at any gate:

1. **CRITICAL**: Halt immediately. Diagnose root cause. Fix in the phase that owns the defect. Re-run all tests from that phase forward (not just the failing test).
2. **MAJOR**: Complete current phase gate. Fix before entering next phase. Re-run the cross-cutting gate that covers the affected SC criteria.
3. After any fix, re-verify that the fix did not introduce drift in previously-passing tests (run the full VM test suite for the current milestone, not just the targeted fix test).
