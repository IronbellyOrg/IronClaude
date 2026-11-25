# Phase 1 Template Checklist (technical_reference_template.md, 16 sections)

| Section | Required or conditional | Planned status | Synthesis file |
|---|---|---|---|
| 1. Overview | Required | Populate (include the four-subject scope, key numbers once, the purpose for the owner) | synth-01-overview-architecture.md |
| 2. Architecture (2.1 high-level, 2.2 subsystem map, 2.3 design decisions as built, 2.4 technology stack) | Required | Populate; add the cross-subject comparison matrix (data sources x outputs x live/designed x consumers x overlaps) and the WC-16 relationship diagram (protected from cuts) | synth-01 |
| 3. Directory Structure | Required | Populate (file trees of the four subjects) | synth-02-directory-dataflow.md |
| 4. Data Flow (4.1 primary, 4.2 sources, 4.3 transformations) | Required | Populate (one flow per subject) | synth-02 |
| 5. Subsystem Reference | Required | Populate 5.1 observer data contract, 5.2 observer interaction, 5.3 sweep classifier, 5.4 sweep read side and WC-16, 5.5 work report and living report, 5.6 dashboard design package | synth-03 (5.1, 5.2), synth-04 (5.3, 5.4), synth-05 (5.5, 5.6) |
| 6. State Management | Conditional (frontend) | N/A unless research finds a clear state model (observer session/view state may be summarised); rationale to be stated | synth-06-integration-config-perf.md |
| 7. Component Inventory | Conditional (frontend) | N/A with rationale (no component inventory beyond subsystem tables) | synth-06 |
| 8. API & Integration Points | Conditional | Populate: Orca verb inventory per tool (bare orca vs orca-ide vs discovered binary), schemas and formats each writes, who reads what | synth-06 |
| 9. Configuration & Environment | Conditional | Populate: flags, env vars, config.json, paths, state dirs | synth-06 |
| 10. Error Handling & Edge Cases | Required | Populate (exit codes, unscanned/UNKNOWN handling, failure modes) | synth-06 |
| 11. Performance Characteristics | Required | Populate (caps, budgets, intervals) | synth-06 |
| 12. Conventions & Patterns | Required | Populate | synth-07-conventions-extension-debt.md |
| 13. Extension Guide | Required | Populate with concrete file paths; plus a factual list of unification touch points (not recommendations) | synth-07 |
| 14. Known Limitations & Technical Debt | Required | Populate: contradictions, stale docs, UNVERIFIED items, C8 DEFECT-CANDIDATE analysis | synth-07 |
| 15. Verification & Accuracy | Mandatory | Populate (snapshot commit 61ac2c2e6, date, spot-check protocol) | synth-07 |
| 16. Glossary | Conditional | Populate (define S1-S11, R1-R11, C1-C5 labels or avoid them) | synth-07 |

Appendices: Document Provenance (scope + research file list). Document History: initial entry.

## Content rules (copied from the template CONTENT RULES and SUBSYSTEM DEPTH LIMITS comments)
| Rule | Do | Don't |
|---|---|---|
| Source code | Summarize behavior in tables and prose | Reproduce TypeScript interfaces, function bodies, or CSS values |
| Statistics | State key numbers once in Section 1 Overview | Embed file counts, line counts, or component counts throughout |
| Architecture | Use tables and ASCII diagrams | Write multi-paragraph prose for what could be a table row |
| Configuration | List key settings with purpose and default | Reproduce entire config files |
| State shape | Table with Slice / Key Fields / Notable Behavior | Full TypeScript interface definitions per slice |
| Single source of truth | Describe each concept in exactly one section | Repeat the same info in Architecture, Subsystem Ref, and State Mgmt |
| Conventions | List rules with brief rationale | Lengthy explanations of why each convention exists |

| Subsystem Complexity | Line Target |
|---|---|
| Simple | 40-80 lines |
| Standard | 80-120 lines |
| Complex | 120-200 lines (more than 200 = candidate for its own reference) |
Section 6 stays under 150 lines. LINE BUDGET Standard tier: 800-1,200 lines.
