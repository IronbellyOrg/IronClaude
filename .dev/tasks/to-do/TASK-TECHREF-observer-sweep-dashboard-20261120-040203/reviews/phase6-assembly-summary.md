# Phase 6 Assembly Summary

Total lines: 1698 (Standard budget 800-1,200; over the ceiling by 498; the Gate 3 template-conformance lens treats more than 1,400 as blocking).

## Section line counts (## headings)
| Section heading | Start line | Lines |
|---|---|---|
| ## Document Information | 78 | 24 |
| ## Completeness Status | 102 | 34 |
| ## Table of Contents | 136 | 25 |
| ## 1. Overview | 161 | 22 |
| ## 2. Architecture | 183 | 86 |
| ## 3. Directory Structure | 269 | 67 |
| ## 4. Data Flow | 336 | 66 |
| ## 5. Subsystem Reference | 402 | 710 |
| ## 6. State Management | 1112 | 25 |
| ## 7. Component Inventory | 1137 | 6 |
| ## 8. API & Integration Points | 1143 | 86 |
| ## 9. Configuration & Environment | 1229 | 41 |
| ## 10. Error Handling & Edge Cases | 1270 | 39 |
| ## 11. Performance Characteristics | 1309 | 45 |
| ## 12. Conventions & Patterns | 1354 | 57 |
| ## 13. Extension Guide | 1411 | 63 |
| ## 14. Known Limitations & Technical Debt | 1474 | 144 |
| ## 15. Verification & Accuracy | 1618 | 21 |
| ## 16. Glossary | 1639 | 24 |
| ## Appendices | 1663 | 29 |
| ## Document History | 1692 | 7 |

## Tags (grep -c lines containing the tag)
- CODE-VERIFIED: 24 lines
- CODE-CONTRADICTED: 20 lines
- UNVERIFIED: 78 lines
- DEFECT-CANDIDATE: 22 lines

## Presence checks
- Section 2.5 matrix: 1 heading(s) found
- Section 14.5 C8 subsection: 1 heading(s) found
- N/A sections: 1112:## 6. State Management 1137:## 7. Component Inventory 
- Largest 5.x subsection:
### 5.1 Observer data contract (what it reads from Orca, what it emits) -> 121 lines
### 5.2 Observer interaction layer, exit codes and release gates -> 125 lines
### 5.3 Sweep Classifier and Joins -> 116 lines
### 5.4 Sweep Read Side, Safety, Publish and the WC-16 Binding -> 124 lines
### 5.5 Agent-work-report pipeline and the living report -> 131 lines
### 5.6 Orca dashboard design package (issue 409) and its relationship to the observer -> 0 (last, see 6 heading)
