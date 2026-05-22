# Dimension 7: Tasklist Quality

**Compared artifact:** Tasklist files (phase-*-tasklist.md + tasklist-index.md) across 3 runs
**Sources:** Research files 01, 03 (QA-verified); spot-checks against actual artifacts

---

## Comparison Table

| Metric | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|--------|:----------------:|:----------------:|:----------------:|
| **Tasklist generated** | YES | NO | YES |
| **Total tasks** | 87 | N/A | 44 |
| **Phases** | 5 | N/A | 3 |
| **Phase task breakdown** | 16/17/17/22/15 | N/A | 27/9/8 |
| **Tasklist-index lines** | 66 | N/A | 219 |
| **Component refs (total)** | 73 | N/A | 218 |
| **Persona refs (Alex/Jordan/Sam)** | 0 (0/0/0) | N/A | 40 (20/11/9) |
| **Compliance refs (GDPR+SOC2)** | 0 | N/A | 40 (26/14) |
| **Compliance keyword (generic)** | 3 | N/A | N/A (measured GDPR/SOC2 instead) |
| **Tier distribution** | Not present | N/A | STRICT:24, STANDARD:17, LIGHT:3, EXEMPT:2 |
| **Test ID refs (UT/IT/E2E)** | 0 | N/A | 8 (3/2/3) |

---

## Spot-Check Results

| Check | Research Value | Spot-Check Value | Method | Match |
|-------|:-------------:|:----------------:|--------|:-----:|
| Run A total tasks | 87 | 87 (16+17+17+22+15) | `grep -c '^### T' phase-*-tasklist.md` | YES |
| Run C total tasks | 44 | 44 (27+9+8) | `grep -c '^### T' phase-*-tasklist.md` | YES |
| Run C component refs | 218 (research) | 218 | `grep -oE '...' phase-*-tasklist.md tasklist-index.md \| wc -l` | YES |
| Run A persona refs | 0 | 0 | `grep -ow 'Alex\|Jordan\|Sam' phase-*-tasklist.md tasklist-index.md` | YES |
| Run C persona total | 47 (research) | 40 (Alex=20, Jordan=11, Sam=9) | `grep -ow 'Alex\|Jordan\|Sam' ...` | DISCREPANCY |
| Run C compliance total | 44 (research, 30+14) | 40 (GDPR=26, SOC2=14) | `grep -ow 'GDPR\|SOC2' ...` | DISCREPANCY |

**Discrepancy notes:**
- **Persona count (Run C):** Research file 03 reports 47 total (Alex=20, Jordan=10, Sam=17). Spot-check with `grep -ow` finds 40 (Alex=20, Jordan=11, Sam=9). The research file's per-file breakdown sums to 47 but includes possible double-counting or non-word-boundary matches. The spot-check value of 40 is used in the table.
- **Compliance count (Run C):** Research file 03 reports GDPR=30, SOC2=14 (total 44). Spot-check finds GDPR=26, SOC2=14 (total 40). The discrepancy in GDPR count may reflect research-phase counting that included partial matches. Spot-check value of 40 is used.

---

## Assessment

Run A produces more tasks (87 vs 44) across more phases (5 vs 3) but with zero enrichment -- no personas, no GDPR/SOC2, no test IDs. Run C (TDD+PRD) produces fewer but richer tasks: 3x the component density (218 vs 73 refs across fewer tasks), 40 persona references, 40 compliance references, and test ID traceability. Run C also includes compliance tier classification (STRICT/STANDARD/LIGHT/EXEMPT) which Run A lacks entirely. Run B did not generate a tasklist. The quality-vs-quantity tradeoff is clear: Run A covers more ground with simpler tasks; Run C covers less ground but each task is more precisely specified with explicit persona, compliance, and component traceability.
