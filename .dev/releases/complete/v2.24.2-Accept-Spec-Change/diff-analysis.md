---
total_diff_points: 12
shared_assumptions_count: 14
---

## 1. Shared Assumptions and Agreements

Both roadmaps agree on the following foundational elements:

1. **Complexity score**: 0.65 (MEDIUM)
2. **Primary persona**: architect
3. **Spec source**: `release-spec-accept-spec-change.md`
4. **New leaf module**: `spec_patch.py` with zero internal imports, no subprocess usage
5. **Dependency direction**: `commands.py → spec_patch.py`, `executor.py → spec_patch.py`, no reverse
6. **Atomic write mechanism**: `.tmp` file + `os.replace()`
7. **Single-cycle recursion guard**: local `_spec_patch_cycle_count` variable, max 1 cycle
8. **Disk-reread invariant**: no in-memory state reuse after spec-hash update
9. **6-step disk-reread sequence**: re-read → recompute → atomic write → re-read → rebuild steps → `_apply_resume()`
10. **PyYAML ≥6.0** as new dependency for YAML frontmatter parsing
11. **3-condition detection** for auto-resume trigger (cycle count, deviation mtime, hash divergence)
12. **`auto_accept` parameter**: internal-only, no CLI flag, `bool = False` default
13. **All 15 success criteria** (SC-1 through SC-15) must pass before release
14. **Total timeline**: ~4.5–6 days engineering effort

---

## 2. Divergence Points

### D1: Phase Structure — Architecture Lock Phase

- **Haiku**: Includes explicit **Phase 0** ("Architecture lock and implementation readiness") as a separate phase before any code is written
- **Opus**: No Phase 0; jumps directly to Phase 1 (Foundation) with implementation
- **Impact**: Haiku's approach reduces risk of mid-implementation design changes but adds ~0.5 day overhead. Opus assumes design decisions can be made inline during Phase 1.

### D2: Phase Count and Granularity

- **Haiku**: 6 phases (0–5), with Phase 5 dedicated to release hardening and operator documentation
- **Opus**: 4 phases (1–4), folding documentation into Phase 4 and omitting a standalone hardening phase
- **Impact**: Haiku's separation makes documentation a first-class deliverable. Opus treats it as a subtask of integration testing, risking NFR-5 being deprioritized.

### D3: Parallelism Acknowledgment

- **Haiku**: Presents phases purely sequentially with no explicit parallelism callout
- **Opus**: Explicitly identifies that Phases 2 and 3 can run in parallel after Phase 1, with a dependency diagram
- **Impact**: Opus enables faster delivery (~4.5 days vs Haiku's 4.5–6 days) by surfacing the obvious parallelism opportunity.

### D4: Requirement Coverage Presentation

- **Haiku**: Includes a dedicated **Section 7** ("Requirement coverage map") listing all FRs and NFRs grouped by path
- **Opus**: Distributes requirement references inline within phase tasks and uses a **Success Criteria Validation Matrix** instead
- **Impact**: Haiku's approach makes audit/traceability easier. Opus's matrix ties criteria to validation phases more directly. Different audiences benefit from each.

### D5: Risk Assessment Format

- **Haiku**: Narrative risk descriptions with detailed mitigation paragraphs, split into "high-priority architectural" and "secondary delivery" categories
- **Opus**: Tabular risk summary (Severity × Probability × Phase × Mitigation)
- **Impact**: Opus's table is faster to scan and prioritize. Haiku's narrative provides deeper context on failure modes.

### D6: `DeviationRecord` Dataclass

- **Haiku**: Mentions confirming data model expectations for `DeviationRecord`, especially absent `id` handling, as a Phase 0 decision
- **Opus**: Explicitly calls out creating a frozen dataclass with 7 fields and strict type invariants as a Phase 1 task
- **Impact**: Opus is more prescriptive and implementation-ready. Haiku defers the decision, which could cause Phase 1 delays.

### D7: Non-Interactive Detection Method

- **Haiku**: Describes non-interactive behavior but doesn't specify detection mechanism
- **Opus**: Explicitly specifies `sys.stdin.isatty()` as the detection method
- **Impact**: Opus eliminates an implementation ambiguity that Haiku leaves open.

### D8: Test File Organization

- **Haiku**: Calls for "2 focused test files minimum" (CLI/spec-patch behavior + executor resume-cycle behavior)
- **Opus**: Does not prescribe test file organization, instead listing test scenarios by phase
- **Impact**: Haiku provides clearer guidance for test structure. Opus leaves it to implementer judgment.

### D9: Phase 0 Parser Behavior Decisions

- **Haiku**: Explicitly flags that absent `id` handling and `>=` vs `>` for mtime comparison must be decided before implementation begins
- **Opus**: Addresses mtime `>=` as a documented limitation in Phase 3 risks; absent `id` not called out as a pre-decision
- **Impact**: Haiku front-loads ambiguity resolution. Opus risks discovering these edge cases mid-implementation.

### D10: Architect Recommendations Style

- **Haiku**: Includes per-phase "Architect recommendation" callouts with specific warnings (e.g., "Do not begin executor changes until module isolation is agreed")
- **Opus**: No per-phase recommendations; architectural guidance is embedded in risk mitigations
- **Impact**: Haiku's callouts serve as implementation guardrails that are harder to miss during execution.

### D11: Final Invariant Statement

- **Haiku**: Ends with an explicit **Section 8** listing 4 invariants that must hold, with a "pause for redesign" directive if any weaken
- **Opus**: No equivalent section; safety properties are distributed across phase validations
- **Impact**: Haiku's invariant list serves as a release gate checklist. Opus relies on the SC matrix for the same purpose but lacks the "stop and redesign" escalation.

### D12: Timeline Confidence

- **Haiku**: Provides ranges per phase (e.g., "1.0–1.5 days"), total 4.5–6.0 days
- **Opus**: Provides point estimates per phase (e.g., "~2 days"), total ~4.5 days with parallelism
- **Impact**: Haiku's ranges are more honest about uncertainty. Opus's point estimates assume ideal conditions and explicit parallelism.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Parallelism planning**: Explicit dependency graph and parallelism callout between Phases 2 and 3
- **Implementation specificity**: `DeviationRecord` dataclass definition, `sys.stdin.isatty()` detection, tabular risk/SC matrices
- **Scannability**: Consistent use of tables and compact formatting makes it faster to consume as a working document

### Haiku is stronger in:
- **Risk front-loading**: Phase 0 forces design decisions before code, reducing mid-implementation surprises
- **Architectural guardrails**: Per-phase architect recommendations act as embedded review criteria
- **Release safety**: Explicit invariant list with "pause for redesign" escalation policy
- **Traceability**: Dedicated requirement coverage map (Section 7) for audit purposes
- **Documentation as deliverable**: Standalone Phase 5 ensures NFR-5 doesn't get deprioritized

---

## 4. Areas Requiring Debate to Resolve

1. **Phase 0 value vs overhead**: Is a formal architecture-lock phase worth 0.5 days, or can design decisions be made inline during Phase 1? Depends on team familiarity with the codebase.

2. **Documentation phase**: Should operator documentation (NFR-5) be a standalone phase (Haiku) or folded into integration testing (Opus)? Given the spec's emphasis on NFR-5 as a safety control, a standalone phase may be warranted.

3. **Test organization**: Should the roadmap prescribe test file structure (Haiku's 2-file minimum) or leave it to implementer judgment (Opus)? Prescriptive guidance reduces review friction.

4. **Timeline representation**: Ranges (Haiku) vs point estimates with parallelism (Opus). The answer depends on whether the audience is planning capacity or tracking progress.

5. **Absent `id` handling**: Must be resolved regardless — Haiku flags it as a pre-decision, Opus doesn't address it. This needs a definitive answer before implementation.
