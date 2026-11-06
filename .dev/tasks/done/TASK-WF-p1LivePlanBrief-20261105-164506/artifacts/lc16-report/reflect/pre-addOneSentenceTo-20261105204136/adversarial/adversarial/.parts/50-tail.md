
## Round 2.5: Invariant Probe

See `invariant-probe.md`. 13 findings: 7 ADDRESSED, 6 UNADDRESSED (HIGH 2: INV-003, INV-012; MEDIUM 2: INV-001, INV-010; LOW 2: INV-007, INV-008). HIGH + UNADDRESSED items block convergence.

## Scoring Matrix

Winner per point after Round 2 (each advocate's final position; confidence is the mean of the three stated values, rounded):

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|------------------|
| S-001 | L1 | tie | 63% | All three label non-findings `minor`; no card is better structured on this point |
| C-001 | L2 | V1 | 70% | Seed-file counterexample is code-verified (install_hooks.py:89-95; main.py:52); V3 reaches the same wording fix from docs only |
| C-002 | L3 | V1 | 78% | Plain `git diff --stat` misses staged and untracked changes (V1 raised it; V2 and V3 conceded); V1's staged-files rationale was wrong and conceded |
| C-003 | L2 | V1 | 93% | main.py:178-236 and install_core.py:69 trace `force` to every installer; V3 relied on docs |
| X-001 | L3 | V1 | 75% | V2's "falsifiable" holds only trivially; V2 conceded in Round 2 |
| X-002 | L2 | tie | 78% | Both "left alone" claims fail: install_skill.py:47-48, installation.md:593 |
| A-001 | L3 | QUALIFY (3 of 3) | n/a | Check must see staged and untracked changes; V2's Round 1 REJECT moved to QUALIFY |
| A-002 | L2 | QUALIFY (3 of 3) | n/a | Only README-reading test checks links (tests/docs/test_retired_docs_absent.py:37-49); no test catches a wrong sentence; V3 moved from ACCEPT |

Positions moved in Round 2: V2 conceded it never tested the sentence's truth and that criterion 2 is insufficient; V3 conceded the false "leaves user-created files alone" claim; V1 conceded the staged-files argument and the "never touched" phrasing.

Not-converging flags: none on diff points. Oscillation: none.

## Convergence Assessment

- Points resolved: 8 of 8 (6 with a winner or a stated tie, 2 shared assumptions resolved to QUALIFY)
- Alignment: 100% (unanimous after Round 2)
- Threshold: 80%
- Taxonomy coverage: L1 = S-001; L2 = C-001, C-003, X-002, A-002; L3 = C-002, X-001, A-001. All levels covered.
- Invariant probe gate: **2 HIGH-severity UNADDRESSED invariants (INV-003, INV-012)**
- Status: **BLOCKED_BY_INVARIANTS**. Standard depth has no Round 3, so convergence is not declared. The refactor plan addresses INV-003 and INV-012 by construction, but no debate round tested that fix.
- Unresolved points: INV-003, INV-012 (HIGH); INV-001, INV-010 (MEDIUM, warning only)
