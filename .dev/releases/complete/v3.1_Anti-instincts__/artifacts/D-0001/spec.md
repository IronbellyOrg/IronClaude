# Architecture Decision Record — v3.1 Anti-Instinct Gate Day-1 Decisions

**Sprint**: v3.1_Anti-instincts__
**Task**: T01.01
**Source**: Roadmap Section 1.0 Recommended Resolutions

---

## OQ-003: `# obligation-exempt` Syntax Scope

**Decision**: Per-line scope on the scaffold term's line.

**Resolution**: The `# obligation-exempt` comment applies only to the line on which it appears. If a scaffold term (e.g., "mocked") appears on a line ending with `# obligation-exempt`, that specific obligation is excluded from the undischarged count. Multi-line exemptions require the comment on each line.

**API Impact on `obligation_scanner.py`**:
- `scan_obligations()` must check each line containing a scaffold match for a trailing `# obligation-exempt` comment.
- Exempt obligations are still recorded in the `Obligation` dataclass but with an `exempt=True` field (or equivalent filtering).
- `ObligationReport.undischarged_count` excludes exempt obligations.

---

## OQ-004: MEDIUM Severity vs STRICT Gate Blocking

**Decision**: Separate `medium_severity_obligations` frontmatter field, excluded from gate blocking.

**Resolution**: Scaffold terms found inside code blocks (backtick-fenced) are demoted to MEDIUM severity. MEDIUM severity obligations are stored in a separate frontmatter field (`medium_severity_obligations`) and are NOT counted toward the `undischarged_obligations` field that the ANTI_INSTINCT_GATE checks. The gate blocks only on HIGH severity (non-code-block) undischarged obligations.

**API Impact on `obligation_scanner.py`**:
- `Obligation` dataclass includes a `severity` field: `"HIGH"` (default) or `"MEDIUM"` (code-block context).
- `ObligationReport` exposes `undischarged_count` property that returns count where `discharged=False AND severity != "MEDIUM"`.
- Code-block detection: scaffold terms within ``` fenced blocks are tagged MEDIUM.

---

## OQ-005: D-03/D-04 Coexistence (Defense-in-Depth)

**Decision**: Both gates evaluate independently per NFR-010.

**Resolution**: The existing `WIRING_GATE` (D-03) and the new `ANTI_INSTINCT_GATE` (D-04) operate as independent pipeline gates. Both evaluate on every run. Neither short-circuits the other. If either fails, the pipeline halts. This is defense-in-depth: the wiring gate checks structural artifact presence while the anti-instinct gate checks semantic content quality.

**API Impact**:
- `ANTI_INSTINCT_GATE` is inserted into `ALL_GATES` between `merge` and `test-strategy` (Phase 2 work).
- No modifications to `WIRING_GATE` behavior or evaluation order.
- Both gates remain in `ALL_GATES` list and both are evaluated by the pipeline runner.

---

## OQ-009: Global vs Contract-Specific Pattern Matching

**Decision**: Phase 1 uses global pattern matching; contract-specific matching deferred to future iteration.

**Resolution**: In Phase 1, the integration contract extractor uses global pattern matching across the entire spec text. It does not attempt to associate specific dispatch patterns with specific contract scopes (e.g., "this RUNNERS dict belongs to the executor module"). Contract-specific matching (associating contracts with their owning modules) is deferred to a future iteration after shadow-mode metrics establish baseline accuracy.

**API Impact on `integration_contracts.py`**:
- `extract_integration_contracts()` scans entire `spec_text` without scope partitioning.
- `check_roadmap_coverage()` checks entire `roadmap_text` for each contract.
- No per-module or per-section scoping logic in Phase 1.

---

## OQ-010: `## Integration Wiring Tasks` Heading Validation

**Decision**: Add heading presence check as structural audit indicator.

**Resolution**: The presence of an `## Integration Wiring Tasks` heading in the roadmap is added as a structural indicator in the spec structural audit module. This is a warning-only check (consistent with FR-MOD4.3). The heading presence is not enforced by the anti-instinct gate directly but contributes to the structural richness ratio.

**API Impact on `spec_structural_audit.py`**:
- The 7 structural indicators already include registry patterns and similar constructs. The heading presence check can be added as an additional signal in Phase 2 when the structural audit is wired into the executor. For Phase 1, the 7 indicators defined in the spec are sufficient.
