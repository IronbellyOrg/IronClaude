---
high_severity_count: 0
medium_severity_count: 5
low_severity_count: 3
total_deviations: 8
validation_complete: true
tasklist_ready: true
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits explicit `--resume` and `--start` CLI flags from CLI surface definition, treating them as open questions to resolve in M1, despite the spec's data models and return contract explicitly generating resume commands with these flags.
- **Spec Quote**: `"--resume --start {self.halt_step}"` (Section 4.5, `resume_command()` method)
- **Roadmap Quote**: `"Resolve highest-impact open questions during M1: resume semantics, --resume/--start CLI flags"` (Section 9, item 2)
- **Impact**: The resume command format is already specified in the data model. Treating the flags as open questions could lead to redesigning what's already defined.
- **Recommended Correction**: Acknowledge `--resume` and `--start` as specified CLI flags (from the spec's `resume_command()` method) and add them to the CLI surface freeze in M1 rather than treating them as unresolved.

### DEV-002
- **ID**: DEV-002
- **Severity**: MEDIUM
- **Deviation**: Roadmap M2 references "Open Question #6" for 1MB line-counting cap handling, but this is not an open question in the spec — it's a closed design decision documented in the file layout table.
- **Spec Quote**: `"Step 2: component discovery via Path.rglob(), line counting (1MB cap with warning)"` (Section 4.1, `steps/discover_components.py` row)
- **Roadmap Quote**: `"Add accurate line counting with documented handling for the 1MB cap inconsistency (Open Question #6)."` (M2, item 7)
- **Impact**: Minor confusion — the roadmap treats a settled spec detail as unresolved. Implementation should follow the spec's 1MB-cap-with-warning behavior.
- **Recommended Correction**: Remove "Open Question #6" framing and implement the 1MB cap with warning as specified.

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: Roadmap Section 5 lists `pyyaml` as a Python library dependency, but the spec's `pyproject.toml` dependencies (Section 4.5 / CLAUDE.md) list only `pytest>=7.0.0`, `click>=8.0.0`, `rich>=13.0.0`. PyYAML is used in semantic checks and contract emission but not listed as a project dependency in the spec.
- **Spec Quote**: `"Dependencies: pytest>=7.0.0, click>=8.0.0, rich>=13.0.0"` (CLAUDE.md)
- **Roadmap Quote**: `"pyyaml"` (Section 5, Python Library Dependencies)
- **Impact**: The roadmap correctly identifies a runtime need (`yaml.dump` in contract emission, `yaml.safe_load` in `_overall_is_mean`), but the spec doesn't list it. Either the spec should add it or the implementation should use an alternative.
- **Recommended Correction**: Add `pyyaml>=6.0` to the spec's dependency list, since the spec's own code examples import `yaml`.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap M4 references enforcing "exact 7 FR count" but the spec's gate criteria for `synthesize-spec` only checks for zero placeholders, required frontmatter fields (`title`, `spec_type`, `complexity_class`), and min 150 lines — not FR count.
- **Spec Quote**: `"Contains 7 functional requirements (one per pipeline step)"` (FR-PORTIFY-CLI.5, acceptance criterion c) and gate: `"SYNTHESIZE_SPEC_GATE"` with semantic checks `[zero_placeholders]` only (Section 5.2.2)
- **Roadmap Quote**: `"Enforce exact 7 FR count and logical step consolidation mapping."` (M4, item 3)
- **Impact**: The acceptance criterion exists but there's no corresponding semantic check in the gate definition. The roadmap adds enforcement that the spec's gate doesn't automate.
- **Recommended Correction**: Either add an `_has_seven_frs` semantic check to `SYNTHESIZE_SPEC_GATE` in the spec, or note in the roadmap that this is a manual/review-time check rather than an automated gate.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Roadmap references "Open Questions 1, 2, 3, 8, 9" throughout milestones but these numbered open questions don't exist in the spec. The spec has named open items (GAP-005, GAP-008, F-006) in Section 11.
- **Spec Quote**: Section 11 lists `GAP-005`, `GAP-008`, `F-006` as open items.
- **Roadmap Quote**: `"Open Question 9 (CLI surface) resolved."` (M1 exit criteria); `"Open Questions 1, 2, 3, 8 validated in implementation"` (M6 exit criteria)
- **Impact**: Traceability gap — roadmap exit criteria reference questions that can't be mapped back to the spec. Reviewers cannot verify which spec items are being resolved.
- **Recommended Correction**: Replace numbered "Open Question" references with the spec's actual identifiers (GAP-005, GAP-008, F-006) or add a mapping table.

### DEV-006
- **ID**: DEV-006
- **Severity**: LOW
- **Deviation**: Spec Section 10 (Downstream Inputs) lists task breakdown as "Phase 1–5" with different groupings than the roadmap's M1–M7 milestones.
- **Spec Quote**: `"Phase 1 (models.py, gates.py, config.py, prompts.py): ~4 tasks ... Phase 4 (executor.py, commands.py, __init__.py, main.py patch): ~4 tasks"` (Section 10)
- **Roadmap Quote**: Milestones M1–M7 with different groupings (e.g., M1 is architecture baseline, M2 is config+discovery+models).
- **Impact**: The downstream task breakdown guidance in the spec doesn't align with roadmap milestones, but this is expected — the roadmap refines the spec's initial guidance.
- **Recommended Correction**: No action needed; the roadmap's milestone structure supersedes the spec's rough task breakdown guidance.

### DEV-007
- **ID**: DEV-007
- **Severity**: LOW
- **Deviation**: Spec lists estimated total of "14-17 tasks across 5 phases" while roadmap has 7 milestones with significantly more work items.
- **Spec Quote**: `"Estimated total: 14-17 tasks across 5 phases"` (Section 10)
- **Roadmap Quote**: 7 milestones with 8-14 work items each.
- **Impact**: Cosmetic — the spec's task estimate was guidance for downstream tooling, not a constraint.
- **Recommended Correction**: None needed.

### DEV-008
- **ID**: DEV-008
- **Severity**: LOW
- **Deviation**: Spec test plan organizes tests by type (unit/integration/E2E) while roadmap M7 organizes validation by layers (static → structural → review → E2E → self-portification).
- **Spec Quote**: Section 8 with subsections 8.1 Unit Tests, 8.2 Integration Tests, 8.3 Manual/E2E Tests.
- **Roadmap Quote**: M7 with "Layer 1: Static and Deterministic Tests" through "Layer 5: Self-Portification".
- **Impact**: The roadmap's layered ordering is a refinement that preserves all spec test cases while adding execution order. No tests are lost.
- **Recommended Correction**: None needed; the layered approach is an improvement.

## Summary

**Distribution**: 0 HIGH, 5 MEDIUM, 3 LOW

The roadmap is well-aligned with the specification. No high-severity deviations were found — all functional requirements, non-functional requirements, data models, gate criteria, and CLI options are addressed. The 5 medium-severity findings are primarily traceability issues (open question numbering mismatch, implicit dependency on `pyyaml`, resume flag treatment as open vs. specified) rather than omissions or contradictions. The roadmap is ready for tasklist generation.
