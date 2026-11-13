# Merge Log

## Metadata
- Executor: merge-executor
- Merge date: 2026-11-13
- Base: variant-3-original.md (Variant 3)
- Plan: refactor-plan.md (auto-approved, risk Low)
- Output: ../merged-reflect-card.md

## Planned changes
1. APPLIED. F1 = V1 F1 precise resume_decision text, MAJOR, blocking false. [from: V1 F1 / C-001, V3 F2]
2. APPLIED. F2 = base cycle-id finding, re-graded MINOR. [from: V3 F1]
3. APPLIED. F3, F4, F5, F9 = V1 findings (Task 12 grep, autoMergeRequest boolean, _RESOLUTION_SCRIPTS vacuous, Phase strings), MINOR. [from: V1 C-003..C-006]
4. APPLIED. F6 = V2 writer-side event contract, MINOR, narrowed wording as in plan. [from: V2 F1 / C-007]
5. APPLIED. F7, F8 = base Depends on and file:NNN findings, MINOR. [from: V3 F3, F4]
6. APPLIED. F10 INV-003, F11 INV-001, F12 INV-004, F13 INV-005, F14 INV-006, MINOR. [from: invariant-probe.md]
7. APPLIED. F15 = engage-row ordering quirk, MINOR. [from: debate Round 2, all three advocates]
8. APPLIED as notes. INV-002, INV-007, INV-008 appear in the narrative only, not as findings. [from: invariant-probe.md]
9. APPLIED. Findings numbered F1..F15 in plan order; provenance HTML comments attached.

Not made, per plan: V1 "dependencies consistent" and "no missed defects"; V3 "must invent" wording; V3 MAJOR for cycle id; promoting C-001 to blocking. No planned change was skipped.

Note: the plan names only C-001 and C-003..C-006 as a group, so the per-finding C-id for F3, F4, F5, F9 is given as that group.

## Post-merge validation
- Structure: provenance header comments, narrative (10 lines), `## Findings block`, one `findings-v2` fence, then provenance comments. PASS.
- Ids: F1..F15 contiguous, 15 JSON lines. PASS.
- Block identity: plan lines 26-42 compared to the fenced block in the merged file with diff; identical. PASS.
- Added findings: none. Claims, severities, citations unchanged. PASS.
