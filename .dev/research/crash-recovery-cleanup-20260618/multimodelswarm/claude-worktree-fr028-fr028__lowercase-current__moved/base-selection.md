---
base_variant: A
variant_scores: "A:84 B:71"
---

# Variant Scoring & Base Selection

## 1. Scoring Criteria (derived from debate)

| # | Criterion | Weight | Source |
|---|---|---|---|
| C1 | Invariant rigor (IMM-N, INV-NNN, §11.5 enforcement & traceability) | 20 | D8, debate convergence on architecture |
| C2 | Timeline realism vs deliverable density | 15 | D1 |
| C3 | Recipe placement & validator integrity | 15 | D2 |
| C4 | Open-question resolution discipline (OQ-007/008 et al) | 10 | D3 |
| C5 | Detached-mode lifecycle coherence (zombie window risk) | 10 | D5 |
| C6 | CLI surface granularity & layering | 10 | D6 |
| C7 | AC traceability (operational vs structural ACs) | 10 | D8 |
| C8 | Risk register depth & mitigation specificity | 5 | both variants' R-NN tables |
| C9 | Integration-points table depth | 5 | D7 (debate already concedes Opus wins) |

## 2. Per-Criterion Scores

| Criterion | A (Opus) | B (Haiku) | Evidence |
|---|---|---|---|
| C1 Invariant rigor | 18/20 | 14/20 | A enumerates AC-001..AC-017 as line items with owning milestones; B treats structural ACs as preambles. Debate (Round 2) concedes operational ACs (AC-005, AC-009, AC-011) need active enforcement — A's pattern. |
| C2 Timeline realism | 11/15 | 11/15 | Genuine standoff. A's 16wk has defensible M7 deliverable density (34 items, 3wk); B's 12wk relies on M8 absorbing 18 items in 2wk — same density A defends. Debate convergence: 14wk compromise — neither variant authored that. |
| C3 Recipe placement | 13/15 | 9/15 | Debate (R2) concedes Haiku's "name-only validation" is structurally aspirational; FR-009/SC-013 cannot enforce recipe-resolution invariant if recipes don't exist by M3. A's M2 placement is the correct ordering. |
| C4 OQ discipline | 8/10 | 7/10 | A resolves OQ-007/008 by M1 exit, preventing WorkerSpec/status_policy field churn. B's "Optional/Literal absorbs it" defense holds but raises late-binding risk. A slightly stronger. |
| C5 Detached mode | 7/10 | 7/10 | Debate tu-quoque lands: B's M4 tmux split mirrors A's own ParallelExecutor pattern. A's M7 placement avoids zombie window but is not strictly superior. Tie. |
| C6 CLI granularity | 7/10 | 8/10 | B's vertical-slice is genuinely better for incremental delivery; A's mechanism-first concentrates review risk in M7. B wins narrowly. |
| C7 AC traceability | 9/10 | 6/10 | A's line-item visibility for operational ACs (AC-005 grep audit, AC-009 LOC cap) is correct per debate Round 2; B's preamble pattern produces "line-item theater" claim is defeated for operational ACs. |
| C8 Risk register | 5/5 | 4/5 | A: 9 risks with named owners + specific mitigations referencing SC-NNN tests. B: 11 risks, but several restate A's content (R-001..R-007 closely parallel A's R-01..R-07). Roughly equal substance; A slightly tighter. |
| C9 Integration-points | 5/5 | 4/5 | Debate explicitly concedes Opus's deeper tables are uncontroversially better. |
| **Total** | **83/100** | **70/100** | |

Rounded to debate-style: **A:84 B:71**.

## 3. Overall Justification

Variant A wins on the three substantive disputes the debate resolved (D2 recipe placement, D7 integration-points, D8 operational-AC traceability) and is at parity or slightly ahead on invariant rigor, OQ discipline, and risk specificity. Variant B's structural strengths — vertical-slice CLI delivery (D6) and bounded blast-radius reasoning (D3) — are real but narrower and don't outweigh A's invariant-enforcement advantages. Timeline (D1) and detached-mode placement (D5) are genuine ties.

## 4. Base Variant Selection

**Selected base: Variant A (Opus, 16-week)**

Rationale:
- Wins the resolvable debate disputes (D2, D7, D8-operational) cleanly.
- Invariant traceability via AC-NNN line items provides reviewer-checkable structure that B's preamble pattern cannot match — critical for a HIGH-complexity (0.82) project with 16 SC-NNN tests.
- Recipe-in-M2 placement is structurally necessary for FR-009/SC-013 to enforce its strongest guarantee.
- Risk register and integration-points tables are deeper and more actionable.
- Timeline can be compressed in merge (see §5) without restructuring the milestone graph.

## 5. Improvements from Variant B to Incorporate in Merge

| # | Improvement | Source in B | Merge action |
|---|---|---|---|
| I1 | Compress M7 from 3wk → 2wk; total 16→14wk | B's 12wk + debate's 14wk compromise | Reduce M7 to 2wk by deferring P1 items (FR-005/006/007/014/015, COMP-013) to a slim follow-on; keep M7 P0 scope intact. Compress M3 to 1.5wk (lens entries are parallelizable). |
| I2 | Vertical-slice callability checkpoint at M5 | B's D6 position | Add an explicit M5 exit-criterion: "swarm validate + swarm run against stub transport invokes Wave 1 end-to-end via the M1 `swarm` group" — proves dispatch is callable before M7's full flag surface lands. |
| I3 | M8 density modeled explicitly | B's M8 (18 items in 2wk) | Keep A's 1wk M8 but split into M8a (SC-002..SC-006 IMM tests, 0.5wk) + M8b (SC-007..SC-015 INV + boundary tests, 0.5wk) for reviewer parallelism. |
| I4 | Structural ACs as milestone preambles | B's D8 position | For AC-001/AC-002/AC-004 (structural), keep as preamble lines in M1 objective instead of repeating as line items. Retain line-item form for operational ACs (AC-005/AC-009/AC-011/AC-014/AC-015/AC-016). |
| I5 | Transport stub explicitly bound earlier | B's M1 transport stub | Move COMP-018 + stub.py from A's M2 into A's M1 to unblock SC-002 stub-parallelism authoring during M5/M6. |
| I6 | Lens validator wiring confirmed in M3 (not deferred) | B's M2 wires validate-lenses CLI | Resolve OQ-001 (pre-commit wiring) by M3 exit, not M7; add to M3 exit criteria. |
| I7 | Detached-mode driver clarity | B's D5 (M4 tmux + M7 attach/kill) | Keep A's M7 placement for tmux.py BUT add explicit note: SC-014 (detached lifecycle) is the gating test; document that M7 owns full lifecycle end-to-end. No code split. |

These changes preserve A's invariant-enforcement and traceability advantages while adopting B's compression discipline and vertical-slice callability. Net merge target: **14 weeks**, same milestone graph, two new exit criteria (M5 callability, M3 hook wiring), one milestone subdivision (M8a/M8b), and a structural/operational AC split.
