# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (+ Round 2.5 invariant probe)
- Convergence achieved: 80%
- Convergence threshold: 75%
- Focus areas: All (High items: C-002, X-001, X-002, X-003, S-004, C-005, S-002)
- Advocate count: 3
- Taxonomy coverage: L1 (C-006, S-003), L2 (S-001, S-002, C-001, C-004, X-001, X-004), L3 (C-002, X-002, X-003, A-006, C-003) — all levels covered

## Round 1: Advocate Statements

### Variant 1 Advocate (opus:architect)
Keep V1 loop, MDTM STOP (not auto-invoke), one-fix-then-HALT, AC fallback→cannot-verify. Absorb V2 delete-table and thin V3 halt/ledger tests. A-006 QUALIFY.

### Variant 2 Advocate (sonnet:refactorer)
Two SoT files, item-text-is-AC, MDTM as markdown, fix or Ruling. Steal citations + start-SHA. No 20-cap. A-006 QUALIFY (executor may write ruling).

### Variant 3 Advocate (haiku:qa)
Keep E-*, E-NO-AC before edit, three-field ruling, citation, 20-cap. Concedes unused E-WRONG-TOOL, verb+object as AC, skip FINAL when N=1, copy delete-table. A-006 QUALIFY.

## Round 2: Rebuttals

Full sequential rebuttals captured from advocates (2026-09-24). Locked agreements: `compliant`; extras after QA; no wait-one-turn; V2 delete-table; skip FINAL when N=1; one-fix cap.

Holdouts after R2: MDTM detector (V1) vs execute-as-markdown (V2, V3 R2); executor vs operator Ruling on `extra`; 20-cap; refs count; E-* catalog size.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | V3+V2 hybrid | 75% | V3 AC shape + V2 delete-table; all conceded hybrid |
| S-002 | V3 (2 refs: qa + ledger) | 70% | V2 one-ref lost majority; V1 three-ref cut to two |
| S-003 | V2 | 90% | Personas/MCP identity deleted; all agree |
| S-004 | V3 | 85% | V1 conceded weaker seams; halt-table + ledger regex |
| C-001 | V2 | 72% | Heuristic inline vs subagent; no `--reviewer` flag; V3: don't test identity |
| C-002 | V3 QUALIFY | 78% | Verb+object title is AC; else E-NO-AC before edit; V1 accepted QUALIFY |
| C-003 | V2/V3 | 95% | Extras after spec QA; V1 conceded |
| C-004 | V1/V2 | 90% | Skip whole-list when N=1; V3 conceded |
| C-005 | V1/V2 | 72% | Warn at N≥20; no E-TOO-MANY; V3 holdout |
| C-006 | V2/V3 | 95% | Verdict token `compliant`; V1 conceded |
| X-001 | V2 | 74% | Execute as markdown, no detector, no auto /task; V3 R2 sided V2; V1 holdout |
| X-002 | V1+V3 | 80% | One-fix then HALT; operator-authored ruling to complete non-compliant; V2 extra-ruling rejected by V3 |
| X-003 | V3 QUALIFY | 78% | Same as C-002 |
| X-004 | V2 | 74% | phase-N and MDTM-shaped files: this protocol; ignore ceremony |
| A-006 | QUALIFY (all) | 88% | Unattended = one fix then HALT; no silent complete |

## Convergence Assessment
- Points resolved: 12 of 15 (S+C+X+A)
- Alignment: 80%
- Threshold: 75%
- Status: CONVERGED
- Unresolved: C-005 (warn vs cap — majority warn), X-001 (V1 holdout on MDTM STOP), S-002 (1 vs 2 refs — majority 2)
- Taxonomy: all of L1/L2/L3 addressed
- Invariant probe: see invariant-probe.md; HIGH UNADDRESSED = 0 after merge rules below
