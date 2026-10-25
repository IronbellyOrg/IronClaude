<!-- Qualitative scoring PASS 1 (order A, B). Independent native Task worker (general-purpose), model slot: opus. agentId a87b40df47627a2a6. Persisted by the top-level pipeline driver (tables verbatim; prose condensed). PROCESS DEVIATION self-reported by scorer: one read-only Bash `cat`/`ls` call despite Read/Grep/Glob-only instruction; nothing written. -->
Result: A 20/30 (qual 0.667), B 24/30 (qual 0.800). Floor: A 3/5, B 2/5 (both eligible).
Decisive factual check: Variant A risks bullet 2 cites interaction-effects.yaml:14-21; file has 13 lines -> lines do not exist. All other citations in A and B resolved.

| Dimension / criterion | A | B |
|---|---|---|
| Completeness 1 explicit reqs | MET | MET |
| Completeness 2 edge/failure | MET | MET |
| Completeness 3 deps/prereqs | MET | MET |
| Completeness 4 success criteria | MET | MET |
| Completeness 5 out of scope | NOT MET (no evidence) | MET (coverage_audit spec.md:1-3 non-normative; message not required) |
| Correctness 1 no factual errors | NOT MET (interaction-effects.yaml:14-21 nonexistent) | MET |
| Correctness 2 feasible | MET | MET |
| Correctness 3 terminology | MET | MET |
| Correctness 4 no contradictions | MET (hedge, not contradiction) | MET |
| Correctness 5 claims supported | MET | MET |
| Structure 1 ordering | MET | MET |
| Structure 2 hierarchy | MET | MET |
| Structure 3 separation | MET | MET |
| Structure 4 navigation/xrefs | MET | MET |
| Structure 5 artifact conventions | NOT MET (decision_needed_by_user prose; deviation-taxonomy.md:146 requires true/false) | MET (booleans; hunk_ref: none lenient, matches t1-card G-1 practice) |
| Clarity 1 unambiguous | NOT MET ("Drift (LOW) or no-deviation") | MET |
| Clarity 2 concrete | MET | MET |
| Clarity 3 section purpose | MET | MET |
| Clarity 4 terms defined | NOT MET | NOT MET |
| Clarity 5 next steps | MET | MET |
| Risk 1 >=3 risks w/ probability+impact | NOT MET | NOT MET |
| Risk 2 mitigation per risk | NOT MET | NOT MET |
| Risk 3 failure modes + recovery | NOT MET (detection only) | MET (conftest/pythonpath) |
| Risk 4 external deps | MET | MET |
| Risk 5 validation mechanism | MET | MET |
| Inv 1 boundaries | MET | MET |
| Inv 2 state across boundaries | NOT MET | NOT MET |
| Inv 3 guard gaps | MET (`if not name` too broad for R-002) | MET (whitespace; non-string) |
| Inv 4 count divergence | NOT MET | NOT MET |
| Inv 5 interaction effects | MET (shared-function coupling) | NOT MET (evidence-status statement, not effect) |
Subtotals A: 4/4/4/3/2/3 = 20. B: 5/5/5/4/3/2 = 24.
Close calls flagged by scorer: B Structure 5; B Inv 5; both Inv 2.
