# Patch Checklist
Generated: 2026-03-16
Total edits: 23 across 8 files

---

## File-by-file edit checklist

- **roadmap.md**
  - [ ] Fix stale "template >50KB" in Phase 10 Key Actions item 3 (from L13)

- **phase-1-tasklist.md**
  - [ ] T01.03: Remove CONTENT_TOO_LARGE from OQ-009 resolution; add note it's added in Phase 7 (from M1)
  - [ ] T01.04: Change T03.08/Phase 3 references to note renumbering: "T03.08 (output Phase 3 = roadmap Phase 2)" (from M2)
  - [ ] T01.02: Add AC bullet documenting API interface contract, not just import paths (from L1)
  - [ ] T01.05: Reframe split-location decision as evaluation step, not foregone conclusion (from L2)
  - [ ] T01.07: Add note that OQ-014 phase assignment is output Phase 9 = roadmap Phase 8 observability (from L4)

- **phase-2-tasklist.md**
  - [ ] T02.06: Remove workdir from G-000 field list in Steps and AC; clarify workdir is emitted but not G-000-required (from M3)
  - [ ] T02.02: Add AC bullet verifying general kebab-case normalization beyond prefix/suffix (from L5)
  - [ ] T02.07: Add AC bullet verifying all discovered component types present in inventory (from L6)
  - [ ] T02.08: Add AC bullet verifying full {path, lines, purpose, type} schema on ≥3 entries (from L7)

- **phase-3-tasklist.md**
  - [ ] T03.04: Change resume AC to status-based skip semantics, not step-ID skip (from L8)
  - [ ] T03.06: Change INVALID_PATH to unspecified/appropriate error type; add NFR-017 minimum version doc step (from L9)
  - [ ] T03.11: Add PARTIAL to outcomes list in AC; add dry-run path to return-contract AC (from L10)

- **phase-4-tasklist.md**
  - [ ] T04.03: Change "Phase 9" reference to "Phase 9 (output) / Phase 8 (roadmap)" (from L11)

- **phase-6-tasklist.md**
  - [ ] T06.05: Rename task title; narrow deliverable to per-gate enforcement wording matching G-006 as return-type-pattern (from M5)

- **phase-7-tasklist.md**
  - [ ] T07.04: Fix dependency line from T03.01 to T01.03 for CONTENT_TOO_LARGE (from L12)

- **phase-8-tasklist.md**
  - [ ] T08.02: Remove overall>=7.0 from convergence scoring function; convergence = zero CRITICALs only (from M4)

- **phase-9-tasklist.md**
  - [ ] T09.01: Update Step 5 wiring to update_step() during subprocess execution, not only on completion; add intermediate-update AC (from L14)

- **phase-11-tasklist.md**
  - [ ] T11.04: Expand AC to enumerate all 14 SC criteria individually with pass conditions from roadmap SC-to-Phase matrix (from M6)

---

## Cross-file consistency sweep
- [ ] Verify all "Phase 3/T03.x" references for roadmap Phase 2 content are annotated with renumbering note
- [ ] Verify CONTENT_TOO_LARGE only appears as a failure_type in T07.04 scope and not in Phase 1 OQ-009 resolution
- [ ] Verify G-006 description consistently says "return type pattern check" (not EXIT_RECOMMENDATION) wherever referenced

---

## Precise diff plan

### 1) roadmap.md

#### Section: Phase 10 Key Actions item 3
**A. Fix stale template size reference**
Current issue: "template >50KB" is stale; amendment changed to >120KB
Change: Replace "template >50KB" with "template >120KB raises CONTENT_TOO_LARGE"
Diff intent: `Edge case tests: ... template >50KB` → `Edge case tests: ... template >120KB raises CONTENT_TOO_LARGE`

---

### 2) phase-1-tasklist.md

#### T01.03 — OQ-009 resolution
**A. Remove CONTENT_TOO_LARGE from enum**
Current issue: 6 values listed; roadmap specifies 5 for Phase 1
Change: Remove `CONTENT_TOO_LARGE` from Step 9 enum definition; add note "CONTENT_TOO_LARGE added in Phase 7 (T07.04) as Phase 6 amendment"
Diff intent: `NAME_COLLISION | ... | DERIVATION_FAILED | CONTENT_TOO_LARGE` → `NAME_COLLISION | ... | DERIVATION_FAILED`

#### T01.04 — Phase reference
**B. Annotate Phase 3 references with renumbering**
Current issue: Says "T03.08" and "Phase 3 executor" but roadmap calls it Phase 2
Change: Append note "(output Phase 3 = roadmap Phase 2)" after each Phase 3/T03 reference
Diff intent: `"T03.08 (_determine_status())"` → `"T03.08 (_determine_status(), output Phase 3 = roadmap Phase 2)"`

#### T01.02 — AC addition
**C. Add API stability AC**
Current issue: Only import success verified; roadmap requires stability documentation
Change: Add bullet: "Current API interface contract for all 6 base types documented in D-0002 (field names, key signatures, inheritance hierarchy)"
Diff intent: Add after last AC bullet in T01.02

---

### 3) phase-2-tasklist.md

#### T02.06 — G-000 fields
**A. Remove workdir from G-000 claim**
Current issue: Steps and AC say G-000 requires workdir; roadmap G-000 only has 3 fields
Change: In Steps: "Required fields: workflow_path, cli_name, output_dir (per G-000 gate check); workdir (additional emitted field)"
In AC: "Emitted portify-config.yaml contains workflow_path, cli_name, output_dir (G-000 required) and workdir (emitted for downstream use)"
Diff intent: Remove parenthetical "per G-000 gate check" from workdir reference

#### T02.02 — Kebab-case AC
**B. Add general normalization test case**
Current issue: Only prefix/suffix stripping tested
Change: Add AC: "derive_cli_name('SC My Workflow') returns 'my-workflow' (space→hyphen, lowercase normalization confirmed)"
Diff intent: New AC bullet after existing explicit examples

#### T02.07 — Component category AC
**C. Add component-type coverage check**
Current issue: AC only requires one SKILL.md entry
Change: Add AC: "Inventory contains entries for all component types present in test skill: skill_main, command, reference, rule, template, script (type field verified per entry)"
Diff intent: New AC bullet after existing G-001 reference

#### T02.08 — Schema completeness AC
**D. Add full schema verification**
Current issue: AC only checks G-001 gate; doesn't verify all 4 fields
Change: Add AC: "Each inventory entry in component-inventory.yaml contains all 4 fields: path, lines, purpose, type (verified on ≥3 entries)"
Diff intent: New AC bullet after existing G-001 gate pass reference

---

### 4) phase-3-tasklist.md

#### T03.04 — Resume semantics
**A. Fix resume AC to status-based**
Current issue: "--resume step-5 skips steps 1-4" implies sequential skip by ID
Change: "--resume resumes from first step with status not in {PASS, PASS_NO_REPORT}; completed steps are not re-executed"
Diff intent: Replace existing resume AC bullet

#### T03.06 — Binary detection error type
**B. Remove INVALID_PATH mapping for missing binary**
Current issue: Roadmap doesn't specify INVALID_PATH for this failure
Change: Step 3: raise PortifyValidationError with appropriate message; remove INVALID_PATH specificity from AC; add step for NFR-017 minimum version documentation
Diff intent: Remove `failure_type=INVALID_PATH` from step 3 and AC

#### T03.11 — Return contract outcomes
**C. Add PARTIAL and dry-run to AC**
Current issue: PARTIAL missing; dry-run path missing
Change: In AC listing outcomes: add PARTIAL. Add new AC bullet: "return-contract.yaml emitted on dry-run pipeline completion"
Diff intent: "SUCCESS, FAILURE, INTERRUPTED, HALTED" → "SUCCESS, PARTIAL, FAILURE, INTERRUPTED, HALTED"; new AC bullet for dry-run

---

### 5) phase-4-tasklist.md

#### T04.03 — Phase reference
**A. Annotate diagnostics phase**
Current issue: "diagnostics.py (Phase 9)" but roadmap Phase 8
Change: "diagnostics.py (output Phase 9 = roadmap Phase 8)"
Diff intent: Append renumbering note to phase reference in Step 1

---

### 6) phase-6-tasklist.md

#### T06.05 — Title and deliverable
**A. Fix title and deliverable wording**
Current issue: Claims EXIT_RECOMMENDATION on all 4 steps; G-006 is return-type check
Change: Title → "Verify 600s Timeout and Per-Gate Enforcement on All Phase 2 Claude Steps"
Deliverable → "Audit confirming all 4 Phase 2 steps have timeout_s=600; EXIT_RECOMMENDATION verified on G-005/G-007/G-008 steps; G-006 enforces return-type pattern"
Diff intent: Replace title and one-sentence deliverable

---

### 7) phase-7-tasklist.md

#### T07.04 — Dependency line
**A. Fix wrong dependency citation**
Current issue: "T03.01 (CONTENT_TOO_LARGE in failure_type enum per OQ-009 resolution, T01.03)" — T03.01 is models.py, not OQ-009 resolution
Change: "T01.03 (CONTENT_TOO_LARGE in failure_type enum, OQ-009 resolution)"
Diff intent: Replace "T03.01" with "T01.03" in dependency line; remove duplicate T01.03 parenthetical

---

### 8) phase-8-tasklist.md

#### T08.02 — Convergence condition
**A. Separate convergence from downstream_ready**
Current issue: "zero unaddressed CRITICALs and overall ≥ 7.0 → converged" conflates FR-032 and FR-034
Change: Step 5: "compute_convergence_score() returns True when zero unaddressed CRITICALs (FR-032); overall>=7.0 scoring handled by T08.05 downstream_ready gate"
AC: Remove "overall >= 7.0" from convergence condition; convergence = zero CRITICALs only
Diff intent: Remove `and overall ≥ 7.0` from Step 5 and corresponding AC bullet

---

### 9) phase-9-tasklist.md

#### T09.01 — TUI real-time wiring
**A. Fix post-completion-only wiring**
Current issue: Step 5 wires update_step() after step completes; not real-time
Change: Step 5: "Wire OutputMonitor.update() callback to call PortifyTUI.update_step() on each output chunk during subprocess execution (not only on completion)"
AC: Add "Progress bar shows at least one intermediate update during a mocked 5s subprocess run"
Diff intent: Replace Step 5 wording; add AC bullet

---

### 10) phase-11-tasklist.md

#### T11.04 — SC criteria enumeration
**A. Expand AC to enumerate all 14 SC criteria**
Current issue: Only references "SC-001–SC-014" as range; no per-criterion pass conditions
Change: Add 14-row SC validation checklist to AC, derived verbatim from roadmap SC-to-Phase Validation Matrix:
- SC-001: Step 0 ≤30s, portify-config.yaml valid (workflow_path, cli_name, output_dir)
- SC-002: Step 1 ≤60s, component-inventory.yaml with ≥1 component
- SC-003: G-002 passes on protocol-map.md
- SC-004: G-003 passes on portify-analysis-report.md
- SC-005: G-008 passes on portify-spec.md (step_mapping consistent)
- SC-006: Review gates write phase approval YAML with status:pending
- SC-007: Resume skips steps already in PASS/PASS_NO_REPORT status
- SC-008: G-010 passes on portify-release-spec.md (zero placeholders, Section 12)
- SC-009: Convergence CONVERGED within 3 iterations with zero unaddressed CRITICALs
- SC-010: Quality score overall>=7.0 → downstream_ready=true
- SC-011: return-contract.yaml emitted on success, failure, dry-run, interrupted paths
- SC-012: --dry-run limits execution to PREREQUISITES, ANALYSIS, USER_REVIEW, SPECIFICATION
- SC-013: Exit codes correct (0=success, 1=failure, 0=interrupted)
- SC-014: Exit code 124 → PortifyStatus.TIMEOUT classification
Diff intent: Replace "All 14 SC criteria (SC-001–SC-014) have status PASS in validation table" with full 14-row checklist

---

## Suggested execution order
1. roadmap.md (L13 — fix stale reference before T11.03 spot-check)
2. phase-1-tasklist.md (M1, M2 — foundational; affects all downstream phase references)
3. phase-2-tasklist.md (M3 — G-000 gate spec affects tests in phase-4)
4. phase-8-tasklist.md (M4 — convergence condition; high semantic impact)
5. phase-6-tasklist.md (M5 — title/deliverable clarity)
6. phase-11-tasklist.md (M6 — SC enumeration; impacts final verification)
7. phase-3-tasklist.md (L8, L9, L10 — implementation detail corrections)
8. phase-4-tasklist.md (L11 — minor phase annotation)
9. phase-7-tasklist.md (L12 — dependency correction)
10. phase-9-tasklist.md (L14 — TUI wiring clarification)
