# Adversarial Debate Transcript

- Depth: deep · Rounds: 2 + invariant probe · Convergence: 0.82 · Threshold: 0.75 · Advocates: 3

## Round 1 — Advocate positions (steelmanned)
- **V1 architect:** strongest base — complete architecture, reuse map with anchors, the load-bearing NOT-HomeIsolation boundary, opt-in reversible template flag, integration file-list. Steelman of V2: degradation matters; concedes it only surfaced it as a risk rather than a HALT. Steelman of V3: concrete impl is valuable but mis-places reflect `--output` on the claude argv.
- **V2 analyzer:** the gate's whole value is rejecting a *silently degraded* Tier-2 audit; 18-FM register; fail-closed `degraded` verdict; race-safe write; FM-13 (summarize_changes expected). Steelman of V1: real-env over HomeIsolation is correct. Concedes its own "optionally HomeIsolation" line is weaker than V1's sharp NO.
- **V3 backend:** concrete, implementable — stdin prompt, atomic os.replace + yamllint dumper, exit codes, file layout, --no-promote as hard prompt flag. Concedes: put reflect `--output` only in the prompt (argv bug); concurrency "out of scope" is weaker than V2's race-safe write.

## Round 2 — Rebuttals / convergence
- C-004/X-002 (fail-closed): V1 + V3 concede V2's fail-closed `degraded` verdict is correct for a GATE. RESOLVED → V2.
- C-003 (HomeIsolation): V2 concedes V1's sharp NOT-HomeIsolation. RESOLVED → V1.
- X-001 (--output): V3 concedes prompt-only. RESOLVED → V1/V2.
- C-002/C-001 (home/window): unanimous. RESOLVED.
- C-006 (write-back): V3 mechanism + V2 race-safety are complementary. MERGED.
- C-005 (timeout): 3600 (V1/V3 majority). RESOLVED.
- C-008 (TCS): V1 builder-bakes-depth (single producer). RESOLVED → V1.

## Scoring matrix (per point)
| Point | Winner | Conf | Evidence |
|-------|--------|------|----------|
| C-004 fail-closed | V2 | 92% | gate must reject degraded T2; invariant probe confirms |
| C-003 env | V1 | 88% | HomeIsolation strips MCP/aliases |
| X-001 --output | V1/V2 | 95% | --output is a skill flag not claude flag |
| C-006 write | V3+V2 | 85% | atomic os.replace + compare-before-write |
| C-008 TCS | V1 | 80% | single producer avoids drift |

## Convergence: 0.82 (CONVERGED — all taxonomy levels covered, no HIGH unaddressed invariants after probe)
