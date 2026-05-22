# D-0104 — Evidence

## Files produced

| File | Purpose |
|---|---|
| `docs/eval/mig-002-batch-plan.md` | Primary deliverable — the batch plan. |
| `.dev/releases/current/cliEval/artifacts/D-0104/spec.md` | Per-AC summary. |
| `.dev/releases/current/cliEval/artifacts/D-0104/notes.md` | Design notes and counting reconciliation. |
| `.dev/releases/current/cliEval/artifacts/D-0104/evidence.md` | This file. |
| `.dev/releases/current/cliEval/evidence/T05.27/README.md` | Per-task evidence stub linking back here. |

## AC verification trace

| T05.27 AC bullet | Verification |
|---|---|
| File `docs/eval/mig-002-batch-plan.md` exists and partitions all 15 evals into 3-5 batches. | File created with 5 batches (A-E); §3 lists every eval id; §4 reverse-lookup table covers all 17 enumerated entries (published count: 15). |
| Each batch entry lists DoD and the matchers it covers. | §2 specifies common DoD (6 bullets); each batch §3 subsection adds batch-specific DoD bullets; each batch's "coverage map" subsection enumerates matcher family + suite source line range. |
| Harness PR named explicitly as PR 1 with eval PRs as PR 2+; each batch entry includes a `coverage-map: <link>` field that the corresponding eval PR description cites verbatim. | §1 PR ordering table names PR 1 = Harness, PR 2-6 = Batches A-E. Each batch §3 section contains an explicit `coverage-map:` line. §4 reverse-lookup gives the paste-ready field per eval. |
| `TASKLIST_ROOT/artifacts/D-0104/spec.md` records the batch plan summary. | `spec.md` created (this artifact set). |

## Sources cross-checked

- `src/superclaude/cli/eval/coverage.py` lines 103-107 (`_DEFAULT_MCP_TOOL_PREFIXES`) — confirms the three v1 matcher prefixes.
- `src/superclaude/cli/eval/coverage.py` lines 188-198 (`default_matcher_filter`) — confirms `Edit|Write|mcp__serena__*` matchers are excluded from v1 gate (informs Batch C's "FR-G5 matcher families cleared: none in v1" claim).
- `src/superclaude/cli/eval/suites/real.yaml` — eval id rows confirmed at lines 43 (E1), 79 (E2.1), 111 (E2.2), 142 (E2.3), 179 (E3), 228 (E4), 292 (E5), 370 (E6), 465 (E7), 565 (E8), 690 (E9), 785 (E10), 884 (E11), 1014 (E12), 1132 (E13), 1292 (E14), 1435 (E15).
- `.dev/releases/current/cliEval/roadmap.md` — R-103 / MIG-002 AC verbatim: `15 eval IDs tracked; batches of 3-5 defined; harness PR separable; eval PRs reference coverage map`. R9 row verbatim: `Harness lands as PR 1 (M1-M4); evals as PR 2+ via MIG-002 batches of 3-5; per-batch DoD recorded`.
- `.dev/releases/current/cliEval/validation/ValidationReport.md` M10 — the AC bullet that added the `coverage-map: <link>` per-batch field requirement (RESOLVED).
