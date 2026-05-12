# Dimension 1: Extraction Quality

**Compared artifact:** `extraction.md` across 3 runs
**Sources:** Research files 01, 02, 03 (QA-verified); spot-checks against actual artifacts

---

## Comparison Table

| Metric | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|--------|:----------------:|:----------------:|:----------------:|
| **Lines** | 302 | 247 | 660 |
| **Section count (## headers)** | 8 | 8 | 14 |
| **Functional requirements** | 5 | 5 | 5 |
| **Non-functional requirements** | 3 | 6 | 8 |
| **Total requirements** | 8 | 11 | 13 |
| **Risks identified** | 3 | 7 | 7 |
| **Dependencies identified** | 7 | 7 | 10 |
| **Success criteria** | 9 | 7 | 10 |
| **Domains detected** | 2 | 4 | 5 |
| **YAML frontmatter fields** | 14 | 14 | 21 |
| **Complexity score** | 0.6 | 0.6 | 0.55 |
| **Persona refs (Alex/Jordan/Sam)** | 0 | 10 (5/2/3) | 4 (1/2/1) |
| **Compliance refs (GDPR/SOC2)** | 0 | 12 (6/6) | 11 (3/5+3 NIST) |
| **Component name refs (total)** | 12 | 16 | 134 |
| **Extra TDD sections** | 0 | 0 | 6 (Data Models, API Specs, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness) |

---

## Spot-Check Results

| Check | Research Value | Spot-Check Value | Method | Match |
|-------|:-------------:|:----------------:|--------|:-----:|
| Run A extraction lines | 302 | 302 | `wc -l extraction.md` | YES |
| Run C extraction lines | 660 | 660 | `wc -l extraction.md` | YES |
| Run B persona Alex (word-boundary) | 5 | 5 | `grep -ow 'Alex' extraction.md` | YES |
| Run B GDPR count | 6 | 6 | `grep -ow 'GDPR' extraction.md` | YES |
| Run A component total | 6 (research, distinct names) | 12 (total occurrences) | `grep -oE 'AuthService\|...' extraction.md` | NOTE |
| Run C section headers | 14 | 14 | `grep -c '^## ' extraction.md` | YES |

**Note on Run A components:** Research file 01 reported "6 matches" meaning 6 distinct component names found. The actual file contains 12 total occurrences (AuthService=1, JwtService=2, PasswordHasher=4, TokenManager=5). The research phrasing was ambiguous. Corrected value used in table above is 12 total occurrences.

---

## Assessment

Run C (TDD+PRD) produces the most comprehensive extraction: 2.2x more lines than Run A, 14 sections vs 8, 21 YAML fields vs 14, and 6 additional TDD-specific sections (Data Models, API Specifications, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness). Run B (Spec+PRD) adds PRD-derived content (personas, compliance, more NFRs) but keeps the same 8-section structure as Run A. The TDD input drives the largest structural expansion, while the PRD input drives enrichment within existing sections. Component name density is an order of magnitude higher in Run C (134 vs 12-16) reflecting the TDD's implementation-level detail.
