# Dimension 2: Roadmap Quality

**Compared artifact:** `roadmap.md` (merged) across 3 runs
**Sources:** Research files 01, 02, 03 (QA-verified); spot-checks against actual artifacts

---

## Comparison Table

| Metric | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|--------|:----------------:|:----------------:|:----------------:|
| **Lines** | 380 | 558 | 746 |
| **## section headers** | 7 (Phase-related) | 9 | 10 |
| **Phases** | 5 | 4 | 3 |
| **Milestones** | 0 (word absent) | 4 | 1 |
| **Persona refs (Alex/Jordan/Sam)** | 0 | 20 (10/4/6) | 11 (2/6/3) |
| **Compliance refs (GDPR/SOC2)** | 0 | 22 | 25 (14/11) |
| **Business metrics (revenue/conversion)** | 0 | 7 (1 revenue, 6 conversion) | 7 (1 revenue, 6 conversion) |
| **Component name refs** | 41 | N/A (not measured with same set) | 111 |
| **Base variant selected** | Opus A (81 vs 73) | Opus A (81 vs 76) | Haiku B (79 vs 71) |
| **Convergence score** | 0.62 | 0.62 | 0.72 |
| **Timeline** | Weeks 1-6 | Weeks 1-10 | 6 weeks |
| **prd_source in frontmatter** | No | Yes | Yes |

---

## Spot-Check Results

| Check | Research Value | Spot-Check Value | Method | Match |
|-------|:-------------:|:----------------:|--------|:-----:|
| Run A roadmap lines | 380 | 380 | `wc -l roadmap.md` | YES |
| Run C roadmap lines | 746 | 746 | `wc -l roadmap.md` | YES |
| Run A component refs | 41 | 41 | `grep -oE 'AuthService\|TokenManager\|...' roadmap.md` | YES |
| Run B persona total | 17 (research) | 20 (spot-check) | `grep -ow 'Alex\|Jordan\|Sam' roadmap.md` | DISCREPANCY |
| Run C GDPR count | 14 | 14 | `grep -ow 'GDPR' roadmap.md` | YES |
| Run C SOC2 count | 11 | 11 | `grep -ow 'SOC2' roadmap.md` | YES |

**Discrepancy note:** Research file 02 reported 17 total persona refs in Run B roadmap. Spot-check with `grep -ow` found 20 (Alex=10, Jordan=4, Sam=6). The research file breakdown was Alex in 5 contexts, Jordan in 4 contexts (529/543/557 = 3 entries), Sam in 3 contexts. The discrepancy arises because some contexts contain the persona name multiple times. Spot-check value of 20 is used in the table above.

---

## Assessment

Roadmap size scales with input richness: Run C is nearly 2x Run A. PRD-enriched runs (B and C) both gain persona references, compliance frameworks, and business metrics that are entirely absent in Run A. Run C produces a more compact phase structure (3 phases vs 5 in Run A and 4 in Run B) but denser content per phase. Component name density is highest in Run C (111 refs) reflecting TDD input propagation through the roadmap. The adversarial process converged better in Run C (0.72 vs 0.62), suggesting the richer input set produced less architectural disagreement between variants.
