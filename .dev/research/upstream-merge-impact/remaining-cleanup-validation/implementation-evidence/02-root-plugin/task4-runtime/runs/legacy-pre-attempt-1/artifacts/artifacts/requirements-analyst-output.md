# sc:sc-requirements-analyst returned findings (Wave 1B, model slot: sonnet, agentId aaef57c3617a61817)

Persisted by the orchestrator, verbatim in substance.

## Pass1 verification
- R-001 spec.md:5 `## R-001 Greeting` -> proposed.md:3 `## T-101 R-001` (exact)
- R-002 spec.md:8 `## R-002 Empty input` -> proposed.md:6 `## T-102 R-002` (exact)
- R-003 spec.md:11 `## R-003 Evidence` -> proposed.md:9 `## T-103 R-003` (exact)
- No other ID tokens. Spans: R-001 spec.md:5-7, R-002 spec.md:8-10, R-003 spec.md:11-12.
- parsed_total 3, matched 3, coverage_pct 1.0000, unmapped_requirements [].

## Pass2 rows
None kept. inferred_count 0; coverage_pct_union 1.0000; unmapped_requirements_union []; parse-density guard does not fire.

## Pass2 dropped candidates
- spec.md:6 "The greet function MUST return the exact string Hello, Ada! for Ada." - overlaps R-001 span
- spec.md:9 "The greet function MUST reject an empty name with ValueError." - overlaps R-002 span
- spec.md:12 "Tests MUST exercise the ordinary greeting and empty-input rejection." - overlaps R-003 span
- spec.md:3 "This fixture is synthetic audit input, not shipped product code." - informational, not requirement-shaped
- spec.md:1 "# Synthetic greeting contract" - document title

## Semantic coverage per requirement
- R-001 PARTIAL: spec.md:6 vs proposed.md:4 "Implement greet(name) returning the required greeting." - exact string `Hello, Ada!` not restated; no Ada->output mapping; no per-task verification. [INFERRED] general format beyond Ada not required.
- R-002 COVERED: spec.md:9 vs proposed.md:7 "Reject an empty name using ValueError." - faithful. [INFERRED] whitespace-only, None/non-string, message content unspecified.
- R-003 COVERED LOOSELY: spec.md:12 vs proposed.md:10 "Add ordinary and empty-name test cases." - assertions not specified (exact string, ValueError); no run/pass instruction. [INFERRED] framework/location unspecified.

## Plan gaps/risks
- No dependency/ordering fields (proposed.md:3,6,9). (Grounded)
- No per-task acceptance criteria / done definition (proposed.md:4,7,10). (Grounded)
- No file paths/module names (proposed.md:4,10). (Grounded)
- Token-only traceability: 1.0 coverage overstates semantic fidelity (R-001).
- [INFERRED] whitespace-only / None handling open.
- [INFERRED] no end-to-end test-run exit step.

## Best-practice grade suggestion: 3/5
