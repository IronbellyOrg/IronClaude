# Validation Report
Generated: 2026-03-16
Roadmap: .dev/releases/current/v2.25-cli-portify-cli/roadmap.md
Phases validated: 11
Agents spawned: 10
Total findings: 20 (High: 0, Medium: 6, Low: 14)

---

## Findings

### Medium Severity

#### M1. T01.03 — CONTENT_TOO_LARGE injected into Phase 0 OQ-009 enum
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.03
- **Problem**: Task resolves OQ-009 `failure_type` enum with 6 values including `CONTENT_TOO_LARGE`, but the roadmap specifies exactly 5 Phase 1 error codes. `CONTENT_TOO_LARGE` is a Phase 6/7 concern and is not part of the Phase 1 spec module plan.
- **Roadmap evidence**: "models.py foundations (including all 5 error code definitions: NAME_COLLISION, OUTPUT_NOT_WRITABLE, AMBIGUOUS_PATH, INVALID_PATH, DERIVATION_FAILED — no separate failures.py)"
- **Tasklist evidence**: T01.03 Step 9: "define failure_type enum as NAME_COLLISION | OUTPUT_NOT_WRITABLE | AMBIGUOUS_PATH | INVALID_PATH | DERIVATION_FAILED | CONTENT_TOO_LARGE"
- **Exact fix**: Remove CONTENT_TOO_LARGE from T01.03 OQ-009 resolution. Add a note that CONTENT_TOO_LARGE is added in Phase 7 (T07.04) as a Phase 6 amendment concern. Update T07.04 dependency note accordingly.

#### M2. T01.04 — Phase cross-reference mismatch (Phase 3 vs Phase 2)
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.04
- **Problem**: Task references T03.x (Phase 3) for OQ-002/OQ-013 implementation, but roadmap places these decisions in Phase 2 (process.py, executor logic). This causes incorrect dependency tracking.
- **Roadmap evidence**: "OQ-002: Kill signal mechanism — affects process.py Phase 2"; "OQ-013: PASS_NO_SIGNAL retry — affects executor logic Phase 2"
- **Tasklist evidence**: "Classify OQ-013 as NON-BLOCKING: T03.08 implements it"; "Phase 3 executor implementation notes updated"
- **Exact fix**: Change T01.04 references from "T03.08" and "Phase 3" to "T03.08/Phase 3 (output Phase 3 = roadmap Phase 2)". Add a clarifying note: "Note: output Phase 3 corresponds to roadmap Phase 2 per phase renumbering."

#### M3. T02.06 — G-000 gate fields misstated (workdir not required by roadmap)
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.06
- **Problem**: Task states G-000 requires workdir field, but roadmap G-000 only requires workflow_path, cli_name, output_dir. Adding workdir to G-000 acceptance criteria contradicts the gate spec.
- **Roadmap evidence**: "G-000 | has_valid_yaml_config (config YAML valid with required fields: workflow_path, cli_name, output_dir)"
- **Tasklist evidence**: T02.06 AC: "Emitted portify-config.yaml contains workflow_path, cli_name, output_dir, workdir"; T02.06 Steps: "Required fields: workflow_path, cli_name, output_dir, workdir (per G-000 gate check)"
- **Exact fix**: Remove workdir from the G-000 field requirement. Keep workdir as an emitted field (it's reasonable), but remove the G-000 parenthetical claim. Change AC to: "Emitted portify-config.yaml contains workflow_path, cli_name, output_dir (G-000 required) and workdir (additional emitted field)."

#### M4. T08.02 — CONVERGED condition incorrectly folds overall>=7.0 into convergence check
- **Severity**: Medium
- **Affects**: phase-8-tasklist.md / T08.02
- **Problem**: Task Step 5 and AC combine zero unaddressed CRITICALs AND overall>=7.0 as the convergence condition, but roadmap separates these: FR-032 defines CONVERGED as zero CRITICALs; FR-034 defines downstream_ready as overall>=7.0. These are distinct conditions handled by different tasks (T08.03 and T08.05).
- **Roadmap evidence**: "FR-032 / Phase 7 action 3: Implement CONVERGED condition: zero unaddressed CRITICALs → status: success"; "FR-034 / Phase 7 action 5: Set downstream_ready = true only when overall >= 7.0"
- **Tasklist evidence**: T08.02 Step 5: "if zero unaddressed CRITICALs and overall ≥ 7.0 → converged"; AC: same compound condition
- **Exact fix**: Remove overall>=7.0 from T08.02 convergence scoring function. convergence_score() should return True only on zero unaddressed CRITICALs. downstream_ready scoring (overall>=7.0) is handled exclusively in T08.05. Update Step 5 and AC accordingly.

#### M5. T06.05 — Title/deliverable overclaims EXIT_RECOMMENDATION on G-006
- **Severity**: Medium
- **Affects**: phase-6-tasklist.md / T06.05
- **Problem**: Task title "Enforce EXIT_RECOMMENDATION and 600s Timeout on All Phase 2 Claude Steps" and deliverable wording claim all 4 steps enforce EXIT_RECOMMENDATION, but G-006 performs a return-type-pattern check, not EXIT_RECOMMENDATION. The task body partially acknowledges this inconsistency, making it internally contradictory.
- **Roadmap evidence**: "G-005 | EXIT_RECOMMENDATION marker present"; "G-006 | Return type pattern check"; "G-007 | EXIT_RECOMMENDATION marker present"; "G-008 | EXIT_RECOMMENDATION marker present; step-count consistency"
- **Tasklist evidence**: Title claims all 4; step 4 says "Confirm each gate checks EXIT_RECOMMENDATION marker (G-005, G-007, G-008 do; G-006 checks return type pattern)"
- **Exact fix**: Rename task title to "Verify 600s Timeout and Per-Gate Enforcement on All Phase 2 Claude Steps." Update deliverable to: "Audit confirming all 4 Phase 2 steps have timeout_s=600 in STEP_REGISTRY; EXIT_RECOMMENDATION enforced on G-005/G-007/G-008; G-006 enforces return-type pattern."

#### M6. T11.04 — All 14 SC criteria referenced only as a range, not individually enumerated
- **Severity**: Medium
- **Affects**: phase-11-tasklist.md / T11.04
- **Problem**: Task references SC-001 through SC-014 as a range in acceptance criteria but does not enumerate each criterion's specific validation requirement from the roadmap's SC-to-Phase matrix. A validation table with just "PASS" is weaker than the matrix which specifies concrete evidence per criterion.
- **Roadmap evidence**: SC-to-Phase Validation Matrix with 14 rows, each with specific validation method (e.g., "SC-001: Step 0 ≤30s, valid config YAML — Unit test: run Step 0, assert timing + YAML parse + required fields")
- **Tasklist evidence**: T11.04 AC: "All 14 SC criteria (SC-001–SC-014) have status PASS in validation table" — no per-criterion definitions
- **Exact fix**: Add a roadmap-derived SC validation checklist to T11.04 acceptance criteria explicitly naming each criterion's pass condition, matching the roadmap's SC-to-Phase Validation Matrix exactly. The table must have 14 rows, not just a range reference.

---

### Low Severity

#### L1. T01.02 — Acceptance only verifies imports, not API stability contract
- **Severity**: Low
- **Affects**: phase-1-tasklist.md / T01.02
- **Problem**: Roadmap requires confirming "stable locations" implying documenting the interface contract, not just successful imports.
- **Exact fix**: Add one AC bullet: "Current API interface contract for all 6 base types documented in D-0002 (field names, signatures, inheritance hierarchy)."

#### L2. T01.05 — Prompt-split location resolved without roadmap basis
- **Severity**: Low
- **Affects**: phase-1-tasklist.md / T01.05
- **Problem**: Task resolves split location to prompts.py as a hard decision; roadmap only asks to confirm the location. This is acceptable invented scope but should be framed as a decision to record, not a foregone conclusion.
- **Exact fix**: Change Step 2 from "Determine location: prompts.py..." to "Evaluate and decide: executor or prompt builder; document rationale."

#### L3. T01.06 — Marker strings and 10-line scan limit not in roadmap
- **Severity**: Low
- **Affects**: phase-1-tasklist.md / T01.06
- **Problem**: Exact marker strings and "first 10 lines" scan are implementation specifics not prescribed by roadmap.
- **Exact fix**: Note these as implementation choices. No AC change required — implementation detail at this level is acceptable.

#### L4. T01.07 — OQ-014 phased to Phase 9; roadmap ties to Phase 8 observability
- **Severity**: Low
- **Affects**: phase-1-tasklist.md / T01.07
- **Problem**: Task assigns OQ-014 to "Phase 9" but roadmap ties workdir cleanup documentation to Phase 8 observability completion (Phase 8 action 4/Risk 12).
- **Exact fix**: Change OQ-014 phase assignment to Phase 9 (output Phase 9 = roadmap Phase 8 observability). Already correct by renumbering — note that output Phase 9 corresponds to roadmap Phase 8.

#### L5. T02.02 — kebab-case normalization not verified in AC
- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.02
- **Problem**: Acceptance only tests prefix/suffix stripping with one example; doesn't verify general kebab-case normalization.
- **Exact fix**: Add AC bullet: "derive_cli_name('SC My Workflow') returns 'my-workflow' (general kebab-case normalization verified beyond prefix/suffix stripping)."

#### L6. T02.07 — Acceptance omits verification of discovered component categories
- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.07
- **Problem**: Roadmap requires discovery across 7 component types; AC only requires SKILL.md entry and warning behavior.
- **Exact fix**: Add AC bullet: "Inventory contains entries for all discovered component types: skill_main, command, reference, rule, template, script, decision (if present in test workflow)."

#### L7. T02.08 — AC doesn't verify full {path, lines, purpose, type} schema
- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.08
- **Problem**: Roadmap requires all 4 fields per component; AC only verifies G-001 pass.
- **Exact fix**: Add AC bullet: "Each entry in component-inventory.yaml contains all 4 required fields: path, lines, purpose, type (verified on at least 3 entries)."

#### L8. T03.04 — Resume described as step-ID skip vs status-based skip
- **Severity**: Low
- **Affects**: phase-3-tasklist.md / T03.04
- **Problem**: AC describes resume as "--resume step-5 skips steps 1-4" but roadmap resume is status-based (skip PASS/PASS_NO_REPORT steps).
- **Exact fix**: Change AC bullet to: "--resume resumes from first step not yet in PASS or PASS_NO_REPORT status; steps before resume point are not re-executed."

#### L9. T03.06 — Missing binary mapped to INVALID_PATH (not in roadmap); NFR-017 doc omitted
- **Severity**: Low
- **Affects**: phase-3-tasklist.md / T03.06
- **Problem**: Roadmap doesn't specify INVALID_PATH for missing binary; also NFR-017 requires documenting minimum version.
- **Exact fix**: Change error type to a distinct error or leave type unspecified in AC. Add step: "Note minimum claude CLI version required (from NFR-017) in D-0022/evidence.md."

#### L10. T03.11 — PARTIAL outcome missing from return-contract AC; dry-run path missing
- **Severity**: Low
- **Affects**: phase-3-tasklist.md / T03.11
- **Problem**: AC lists SUCCESS/FAILURE/INTERRUPTED/HALTED but omits PARTIAL. SC-011 validation matrix also requires dry-run path.
- **Exact fix**: Add PARTIAL to AC bullet listing outcomes. Add AC bullet: "return-contract.yaml emitted on dry-run completion path."

#### L11. T04.03 — Diagnostics phase reference says Phase 9, roadmap Phase 8
- **Severity**: Low
- **Affects**: phase-4-tasklist.md / T04.03
- **Problem**: Step 1 references "diagnostics.py (Phase 9)" but roadmap places diagnostics in Phase 8.
- **Exact fix**: Change "Phase 9" to "Phase 9 (output phase = roadmap Phase 8)" to be explicit about renumbering.

#### L12. T07.04 — Dependency cites T03.01 for CONTENT_TOO_LARGE but source is T01.03
- **Severity**: Low
- **Affects**: phase-7-tasklist.md / T07.04
- **Problem**: Dependencies line says "T03.01 (CONTENT_TOO_LARGE in failure_type enum per OQ-009 resolution, T01.03)" — T03.01 is models.py, not the OQ-009 resolution. T01.03 is the actual source.
- **Exact fix**: Change dependency to: "T01.03 (CONTENT_TOO_LARGE in failure_type enum, OQ-009 resolution)"

#### L13. Roadmap stale reference — Phase 10 still says "template >50KB"
- **Severity**: Low
- **Affects**: roadmap.md / Phase 10 Key Actions item 3
- **Problem**: Phase 10 roadmap still contains "template >50KB" as an edge case, but the amendment changed the limit to >120KB and replaced --file with PortifyValidationError. T11.03 correctly implements >120KB. The roadmap is internally inconsistent.
- **Exact fix**: Update roadmap.md Phase 10, Key Actions item 3: change "template >50KB" to "template >120KB raises CONTENT_TOO_LARGE" to match the Phase 6 amendment.

#### L14. T09.01 — TUI update wired post-step-completion; not real-time during execution
- **Severity**: Low
- **Affects**: phase-9-tasklist.md / T09.01
- **Problem**: Step 5 wires update_step() after step completes. For 600-1200s Claude steps, this doesn't satisfy "real-time progress." Acceptance only checks method is callable, not that progress is visible during execution.
- **Exact fix**: Update Step 5 to wire update_step() to OutputMonitor.update() callback during subprocess execution, not only on completion. Add AC bullet: "Progress bar updates visible during a 5s mocked subprocess run (at least one intermediate update before completion)."

---

---

## Verification Results
Verified: 2026-03-16
Findings resolved: 20/20

| Finding | Status | Notes |
|---------|--------|-------|
| M1 | RESOLVED | CONTENT_TOO_LARGE removed from T01.03 OQ-009 enum; note added pointing to T07.04 |
| M2 | RESOLVED | Phase 3 references in T01.04 annotated with "(output Phase 3 = roadmap Phase 2)" |
| M3 | RESOLVED | T02.06 G-000 field list corrected; workdir marked as emitted-but-not-G-000-required |
| M4 | RESOLVED | T08.02 convergence condition updated to zero CRITICALs only; overall>=7.0 delegated to T08.05 |
| M5 | RESOLVED | T06.05 title renamed to "Verify 600s Timeout and Per-Gate Enforcement"; G-006 return-type distinction explicit |
| M6 | RESOLVED | T11.04 AC expanded with 14-row SC checklist matching roadmap SC-to-Phase matrix exactly |
| L1 | RESOLVED | T01.02 AC added API interface contract documentation bullet |
| L2 | RESOLVED | T01.04 phase reference annotated |
| L3 | ADVISORY | Marker strings and 10-line scan are implementation choices; no AC change required |
| L4 | RESOLVED | T01.07 OQ-014 phase assignment annotated with renumbering note |
| L5 | RESOLVED | T02.02 AC added general kebab-case normalization test case |
| L6 | RESOLVED | T02.07 AC added component-type coverage check |
| L7 | RESOLVED | T02.08 AC added full {path, lines, purpose, type} schema verification |
| L8 | RESOLVED | T03.04 resume AC changed to status-based semantics |
| L9 | RESOLVED | T03.06 error type note added; NFR-017 version doc step added |
| L10 | RESOLVED | T03.11 PARTIAL added to outcomes; dry-run return-contract bullet added |
| L11 | RESOLVED | T04.03 diagnostics phase annotated with renumbering |
| L12 | RESOLVED | T07.04 dependency corrected from T03.01 to T01.03 |
| L13 | RESOLVED | roadmap.md Phase 10 item 3 updated from ">50KB" to ">120KB raises CONTENT_TOO_LARGE" |
| L14 | RESOLVED | T09.01 Step 5 wiring updated to real-time chunk callback; intermediate-update AC added |

---

## Additional Roadmap Patch Required

The following roadmap inconsistency was identified and must be patched (independent of tasklist fixes):

- **roadmap.md Phase 10 Key Actions item 3**: "template >50KB" — stale, must be updated to ">120KB raises CONTENT_TOO_LARGE" (see L13)
