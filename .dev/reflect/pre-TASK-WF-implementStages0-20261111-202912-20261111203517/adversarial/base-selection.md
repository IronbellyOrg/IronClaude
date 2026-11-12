# Base selection

Scoring done by the orchestrator, not by a separate pass; this is a documented simplification of the 30-criterion rubric, because the three variants are findings lists on one plan and not competing prose artifacts.

| Variant | Findings | Upheld as graded | Upheld lower | Refuted | Unique upheld findings |
|---|---|---|---|---|---|
| V1 (sonnet analyzer) | 12 | 6 | 5 (F4 minor, F9, F10, F12 minor; F8 medium) | 0 | C-003, C-004, C-006, C-008 |
| V2 (haiku-pinned qa) | 10 | 6 | 3 (F2, F8, F9 medium) | 0 (F4 reduced to a clarification) | C-013, C-015 |
| V3 (opus refactorer) | 14 | 9 | 3 | 2 (F12 / C-026 refuted, F7 / C-022 minor) | C-021, C-023, C-024, C-025, INV sources |

Base variant: V3 (broadest verified coverage of cross-task coupling; two blocking findings independently matched by V2). Strengths incorporated from V1: C-003, C-004, C-006, C-008 (code-level). From V2: C-013, C-015 (spec staging). Edge-case floor: all variants scored at least 1/5 on invariant and edge-case coverage through the Round 2.5 probe items, none ineligible.
Tiebreaker not applied.
