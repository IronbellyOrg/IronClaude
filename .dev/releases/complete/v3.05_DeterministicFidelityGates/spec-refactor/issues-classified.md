# v3.05 Spec Issues — Classified from Compatibility Report

> Source: `CompatibilityReport-Merged.md` (commit `f4d9035`)
> Extracted: 2026-03-20

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH     | 7 |
| MEDIUM   | 9 |
| LOW      | 5 |
| **Total** | **24** |

---

## CRITICAL — Spec claims create for existing code; implementing as-is would overwrite

| ID | Source § | Specific Claim / Gap | Affected Spec | Spec Says | Reality | Proposed Resolution |
|----|---------|----------------------|---------------|-----------|---------|---------------------|
| ISS-001 | §1 | convergence.py listed as CREATE new module | FR-7 | "Create convergence engine" | Already exists (v3.0), 323 lines, added in commit f4d9035 | Reclassify → MODIFY. Spec must say "extend existing convergence.py with `execute_fidelity_with_convergence()` and `handle_regression()`" |
| ISS-002 | §1 | semantic_layer.py listed as CREATE new module | FR-4 | "Build semantic layer module" | Already exists (v3.0), 336 lines, with prompt budget constants, `build_semantic_prompt()`, debate scoring | Reclassify → MODIFY. Spec must say "complete existing semantic_layer.py with `validate_semantic_high()` and `run_semantic_layer()` orchestrators" |
| ISS-003 | §1 | remediate_executor.py listed as CREATE new module | FR-9 | "Create remediation executor" | Already exists (v3.0), 563 lines, with snapshot create/restore/cleanup | Reclassify → MODIFY. Split FR-9 into already-implemented / conflicting / missing subsections |

---

## HIGH — Spec and code materially conflict on behavior

| ID | Source § | Specific Claim / Gap | Affected Spec | Spec Says | Reality | Proposed Resolution |
|----|---------|----------------------|---------------|-----------|---------|---------------------|
| ISS-004 | §3 | Diff-size threshold mismatch | FR-9 | 30% threshold | Code uses `_DIFF_SIZE_THRESHOLD_PCT = 50` at remediate_executor.py:45 | Change code to 30% — spec's value was deliberate (adversarial-reviewed BF-5) |
| ISS-005 | §3 | Diff-size granularity mismatch | FR-9 | Per-patch granularity | Code implements per-file granularity | Modify remediate_executor.py to check per-patch, not per-file |
| ISS-006 | §3 | Rollback scope mismatch | FR-9 | Per-file rollback | Code implements all-or-nothing rollback | Add per-file rollback logic to remediate_executor.py |
| ISS-007 | §7c | MorphLLM vs ClaudeProcess remediation model design gap | FR-9 | Describes "MorphLLM-compatible lazy edit snippets" as remediation model | All remediation uses ClaudeProcess; MorphLLM exists as MCP but is not integrated | Use ClaudeProcess with MorphLLM-compatible patch format (JSON schema) for future swap compatibility |
| ISS-008 | §1 | deviation_registry.py listed as new file but class exists inside convergence.py | FR-6 | "Create deviation_registry.py" | DeviationRegistry class already exists inside convergence.py:50-225 | Either extract to own file or update spec to accept current location |
| ISS-009 | §7e | FR-3 severity rule tables are foundational but entirely new — no code exists | FR-3, FR-1, FR-6, FR-7, FR-8 | Severity rules anchor all 5 structural checkers | Zero rule table infrastructure exists; `compute_stable_id()` uses `mismatch_type` but no rules | Build and validate severity rule tables early — cascading dependency across FR-1→FR-6→FR-7→FR-8 |
| ISS-010 | §7b | Remediation ownership conflict: post-pipeline vs within convergence loop | FR-7, FR-9 | Remediation within convergence loop (between runs) | Current remediation is post-pipeline; `_check_remediation_budget()` and `_print_terminal_halt()` assume external remediation | Redesign remediation to run within convergence loop, not after pipeline |

---

## MEDIUM — Spec omits something that exists and matters

| ID | Source § | Specific Claim / Gap | Affected Spec | Spec Says | Reality | Proposed Resolution |
|----|---------|----------------------|---------------|-----------|---------|---------------------|
| ISS-011 | §6 | spec_patch.py not mentioned in v3.05 spec at all | (omitted) | No mention | spec_patch.py is active: imported in commands.py:210 and executor.py:1397 for accepted-deviation workflow | Explicitly scope spec_patch.py as preserved legacy or coexisting with v3.05 |
| ISS-012 | §7a | Convergence loop vs linear pipeline tension undocumented | FR-7 | Adds convergence as new phase | Pipeline is single-pass; convergence needs up to 3 runs within step 8 | FR-7 should describe convergence as altering step-8 authority/behavior, not adding new phase |
| ISS-013 | §7d | SPEC_FIDELITY_GATE + wiring step ordering semantics undocumented | FR-7 | (implicit) | When convergence_enabled=true, spec-fidelity gate is None; wiring step still works but ordering semantics unclear | Document step ordering when convergence mode replaces spec-fidelity gate |
| ISS-014 | §4 | validate_semantic_high() referenced in docstring but never defined | FR-4.1 | Function should exist | Docstring reference at semantic_layer.py:321 but no function definition | Implement validate_semantic_high() in semantic_layer.py |
| ISS-015 | §7f | spec_parser.py critical path risk not surfaced in spec | FR-2 | Lists spec_parser.py as new module | FR-1 depends on FR-2; FR-4 depends on FR-1; parser robustness against real-world specs is unaddressed | Add parser robustness requirements and note critical path dependency chain |
| ISS-016 | §7g | FR-7/FR-8 circular interface not designed | FR-7, FR-8 | FR-7 triggers FR-8; FR-8 feeds back into FR-7 | Circular dependency requires careful interface design; regression validation must count as one "run" toward budget of 3 | Specify interface contract between FR-7 and FR-8, including budget accounting |
| ISS-017 | §3 | TRUNCATION_MARKER missing heading name | FR-5 | Include `<heading>` in truncation marker | Current implementation omits heading name | Add heading name to TRUNCATION_MARKER in semantic_layer.py |
| ISS-018 | §4 | Section splitter for chunked comparison does not exist | FR-5 | Split spec/roadmap by headings for per-section checker input | `_truncate_to_budget()` exists but no section-splitting logic | Build section splitter — needed for per-section fidelity checking |
| ISS-019 | §8 P2 | No "existing baseline from v3.0" section in spec | (whole spec) | Spec assumes greenfield | 19 requirements already fully satisfied; 3 modules already exist | Add explicit baseline section documenting pre-existing modules, fields, and pipeline wiring |

---

## LOW — Spec wording is stale but intent is clear

| ID | Source § | Specific Claim / Gap | Affected Spec | Spec Says | Reality | Proposed Resolution |
|----|---------|----------------------|---------------|-----------|---------|---------------------|
| ISS-020 | §5 | fidelity.py is dead code (66 lines) | (none) | Not referenced | Zero imports across entire codebase; superseded by Finding + DeviationRegistry | Delete fidelity.py |
| ISS-021 | §5 | RunMetadata dataclass is dead within convergence.py | (none) | Defined at line 36 | Never instantiated; `begin_run()` uses raw dicts | Remove RunMetadata or wire it into begin_run() |
| ISS-022 | §8 P1 | Spec language uses "create" for modules that need "extend" | FR-4, FR-7, FR-8, FR-9 | "Create new", "build module" | Should say "extend existing", "complete module" | Reword all FR sections to acknowledge existing code |
| ISS-023 | §6 | prompts.py:build_spec_fidelity_prompt() role undocumented in v3.05 context | (none) | Not mentioned | Used in legacy mode (convergence_enabled=false); still generates report in convergence mode | Document role of legacy prompt builder in v3.05 context |
| ISS-024 | §4 | Finding dataclass missing v3.05 fields | FR-6 | Requires rule_id, spec_quote, roadmap_quote, stable_id | Fields not yet on Finding dataclass in models.py | Extend Finding dataclass with new fields — low risk, additive change |
