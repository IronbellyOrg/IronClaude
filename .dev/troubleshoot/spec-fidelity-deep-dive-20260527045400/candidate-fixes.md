# Candidate Fixes Index (Wave 3 step 4)

5 distinct fix proposals emerged from Tier 1 + 4 Tier 2 specialists. All five share the mechanical observation (`D01 != D1` at `structural_checkers.py:380`) but frame the structural root cause differently and locate the fix in different modules.

| # | Source | Where the fix lives | One-line claim | Verdict |
|---|---|---|---|---|
| 1 | Tier 1 RCA | `structural_checkers.py` (~15 LOC) | Comparator-canonicalization gap + missing severity-demotion for drift class. Smallest scope. | **competing** |
| 2 | Tier 2 RCA | `structural_checkers.py` (~48 LOC) | Missing fixability invariant at finding-emission boundary; canonicalizer is one concrete user of a generalizable classifier. | **competing** |
| 3 | Tier 2 refactoring-expert | `spec_parser.py` (~12 LOC) | Primitive obsession on raw ID strings; move canonicalization UPSTREAM into extraction so checker is correct as-written. | **competing** |
| 4 | Tier 2 system-architect | `structural_checkers.py` + `commands.py` + models (~57 LOC, 3 files) | Binary pass condition on open-world finding stream; introduce new `ADVISORY` severity tier + CLI lane mirroring `--allow-cosmetic-remediation`. | **competing** |
| 5 | Tier 2 quality-engineer | `structural_checkers.py` code (mirrors #1) + 4 new test files (~150 LOC) | Test-design defect lets the code defect ship undetected each release; pair code fix with property-based generators + flatline-halt regression. | **competing** |

**Consensus dimension**: all 5 endorse SOME form of canonicalization-aware comparator behavior and reject S6 (MANUAL_TRIAGE halt) as standalone primary fix. None propose touching `convergence.py:539` directly.

**Divergence dimensions**:
1. **Locus**: extractor (#3) vs comparator (#1, #2, #5) vs orchestration vocabulary (#4)
2. **Generalization**: surgical (#1, #3) vs scaffolded (#2 fixability infra, #4 advisory tier)
3. **Empirical validation surface**: code-only (#1, #2, #3, #4) vs code+property-tests (#5)

Wave 4 (sc:adversarial-protocol `--compare`) will debate all 5. Materializing each as a standalone fix proposal now.
