# Merge Log

## Metadata

- Base: Variant 3 (opus:refactorer), `variant-3-original.md`, combined score 0.844 (V2 0.725, V1 0.671; base-selection.md)
- Executor: merge-executor
- Changes planned: 23 (B1-B7 base corrections, C1-C16 changes)
- Changes applied: 23
- Status: SUCCESS (merge complete; verdict status BLOCKED_BY_INVARIANTS carries INV-001 and INV-002 as open P1 findings M-03 and M-05)
- Timestamp: 2026-11-07T02:15:00Z
- Output: `merged-verdict.yaml` (31 findings, 1 note, 16 dropped entries, 6 verified_ok entries)
- Path legend: evidence paths are repo-relative to `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2`; `plan:N` is line N of `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md`.

## Changes Applied

### Base corrections

| Change | Status | Source | Target | Before | After | Provenance tag | Validation |
|---|---|---|---|---|---|---|---|
| B1 | Applied | V3 R3-F1, INV-010 | M-01 | Harm worded as "commit/push"; fix without test literal or Task 12 edge | "push" dropped; conditional-commit (WC-9) and `.dev/impact` path (WC-4, WC-11) harms; fix adds 16->12, the UNATTENDED_EXPECT and EXPECTED_NESTING literals, standalone-token rule (INV-010) | base-modified | PASS |
| B2 | Applied | V3 R3-F13 | M-26, dropped | `.dev/reflect` dirty-folder example | Example deleted; finding body replaced by C6 | incorporated (via C6) | PASS |
| B3 | Applied | V3 R3-F6 | M-19 | Both brainstorm handoffs | Tasklist handoff only; task handoff half dropped | base-modified | PASS |
| B4 | Applied | V3 R3-F7 | M-20 | All "Same edits" for improve | Safety Threshold clause only (plan:46) | base-modified | PASS |
| B5 | Applied | V3 R3-F2, V1 R1-F2 | M-02, dropped | Included FR-G5 and `--no-pty` | Those parts removed (settled at plan:248) | incorporated (via C1) | PASS |
| B6 | Applied | V3 R3-F12 | M-25, dropped | Output path plus skill name | Output path only | base-modified | PASS |
| B7 | Applied | V3 verified_ok | `verified_ok` | "Depends on chains correct" and unbounded claims | Six bounded claims; edge list states it is not exhaustive and that M-01 adds 16->12; EXPECTED_NESTING claim says "as written" and points to M-13 | base-modified | PASS |

### Changes C1-C16

| Change | Status | Source | Target | Before | After | Provenance tag | Validation |
|---|---|---|---|---|---|---|---|
| C1 | Applied | V2 R2-F1 (+ V3 R3-F2, V1 R1-F2) | M-02 | Base R3-F2 (P2-level framing) | P1: missing safety-flag block, two separate assertions, subset pending owner | incorporated: V2 per C1 | PASS |
| C2 | Applied | V2 R2-F2, V1 R1-F10 | M-10 | Not in base | Condition-to-outcome phrases per gate; per-gate gaps for Tasks 5, 13, 16 | incorporated: V2 per C2 | PASS |
| C3 | Applied | V1 R1-F3 | M-11 | Not in base | CLI-mode reflect gate; `--fix --promote` stated as not outward | incorporated: V1 per C3 | PASS |
| C4 | Applied | V1 R1-F4 | M-28 | Not in base | spec-panel socratic "not wait" as an unlisted owner decision | incorporated: V1 per C4 | PASS |
| C5 | Applied | V2 R2-F3 | M-09 | R3-F11 (subset of commands) | All 15 P2 commands, real pinned count 2; parametrized test kept | base-modified | PASS |
| C6 | Applied | V2 R2-F4 | M-26 | R3-F13 | Full commit manifest including the `.dev/tasks` package | incorporated: V2 per C6 | PASS |
| C7 | Applied | V1 R1-F1 | M-06 | R3-F3 remedy pinned test 837-844 | refs/return-contract.md added to Task 17 coherence check; test-pin claim removed; fix must reach the line `_artifacts_clause` reads | base-modified | PASS |
| C8 | Applied | V1 R1-F6 | M-29 | Not in base | depth-map.yaml location only (D-P2-13 reading dropped) | incorporated: V1 per C8 | PASS |
| C9 | Applied | V1 R1-F7 | M-30 | Not in base | `reflect-pre` grep AC for Task 16 | incorporated: V1 per C9 | PASS |
| C10 | Applied | V2 R2-F5 | `notes` N-01 | Not in base | Coverage-matrix note, not a finding | incorporated: V2 per C10 | PASS (shape addition, see Deviations) |
| C11 | Applied | V1 R1-F8 | M-22 | Not in base | Collision finding beside M-21 | incorporated: V1 per C11 | PASS |
| C12 | Applied | V1 R1-F5; X-002/C-008 class reassignment | M-31; every finding | Uniform labels per variant | Per-finding class (30 drift, 1 necessary); R1-F5 kept as alternative | incorporated: V1 per C12 | PASS |
| C13 | Applied | R2A3-s3.1, E-1 | M-04 | Not in any variant | Nest-or-refuse owner choice for `--diagnosability-handoff` | incorporated per C13 | PASS |
| C14 | Applied | INV-001 | M-03 | Not in any variant | P1 blocking, linked to M-02 | incorporated per C14 | PASS |
| C15 | Applied | INV-002 | M-05 | Not in any variant | P1 blocking, linked to M-01 | incorporated per C15 | PASS |
| C16 | Applied | INV-003, 004, 009, 011, 016, 017, 018 (findings); INV-005, INV-010 (folded) | M-12 to M-18; M-07, M-08, M-01 | Not in any variant | Seven MEDIUM invariants as P2 findings; INV-005 folded into M-07 and M-08, INV-010 into M-01, each stated in provenance | incorporated per C16 | PASS |

### Executor decisions and deviations (escalation notes)

1. `deviation_class` for the invariant findings (M-03, M-05, M-12 to M-18) and the C13 finding (M-04): the plan gives no class; the executor assigned `drift` (a plan gap against the spec or its own rules). Orchestrator may revise.
2. `owner_decision: true` only where the plan's Review Status lists an owner decision or the source fix names the owner: M-02, M-03, M-04, M-06, M-12, M-17, M-28, M-31.
3. Top-level `notes:` key added for C10 (N-01). It is outside the requested key list; the plan asks for R2-F5 as a coverage-matrix note, not a finding.
4. M-04 wording: the Task 20 `EXPECTED_NESTING` literal changes only under the nest branch; the refuse branch leaves it unchanged. The plan text states the literal edit without that condition; the finding follows the branch-conditional reading (consistent with M-12 and M-13).
5. M-11 cites `tests/skills/test_worker_contract.py:2044-2052` with an `[INFERRED]` note, carried as cited.

## Post-Merge Validation

Validator: one `uv run python` script (stdin, no file written) run from the P2 worktree.

### Structural Integrity

- YAML parses (PyYAML 6.0.3): PASS
- Top-level keys present: merge_method, convergence_score, convergence_status, unaddressed_invariants, findings, dropped, verified_ok: PASS (extra key: `notes`, deliberate per C10)
- 31 findings, ids M-01 to M-31 sequential, no duplicates, ordered P1 then P2 then P3: PASS
- Every finding has all 10 fields non-empty; class in {drift, regression, necessary, authorized}; `owner_decision` boolean; provenance is `base`, `base-modified: ...` or `incorporated: ...`: PASS
- `dropped` entries are `{source_id, reason}` (16); `unaddressed_invariants` entries are `{id, category, assumption, severity}` (2): PASS

### Internal References

- 157 evidence entries (findings and N-01) checked: every path exists and every cited line or range end is within the file length (`plan:N` expanded; comma lists and ranges split; `[INFERRED]` notes stripped): PASS, 0 errors
- Cross-links resolve: M-02<->M-03, M-01<->M-05/M-13/M-14, M-04<->M-12/M-13, M-06<->M-17, M-07<->M-13, M-11<->M-18, M-21<->M-22, `verified_ok`->M-01/M-13: PASS

### Contradiction Re-Scan

- M-11 and dropped R1-F3 agree that `--fix --promote` is not an outward action.
- M-02 (block missing) and dropped X-001 V1 framing agree that the brief may pass the flags.
- M-06 defers the fix form to M-17; neither picks a form.
- `verified_ok` edge list is bounded and points to M-01 for 16->12; EXPECTED_NESTING claim is "as written" and points to M-13.
- M-31 (`necessary`) is the only non-drift finding and is kept as an alternative, matching dropped "R1-F5 as a requirement".
- Result: no new contradictions found.

## Summary

- Planned: 23 (B1-B7, C1-C16)
- Applied: 23
- Failed: 0
- Skipped: 0 (dropped source items listed in `dropped`, 16 entries, all per the plan or its Changes NOT Being Made table)
- Findings: 5 P1, 13 P2, 13 P3 (30 drift, 1 necessary); 1 note; 6 verified_ok
- Structural integrity: PASS
- Internal references: 157 of 157 evidence entries valid
- Contradictions introduced: 0
- Open: INV-001 (M-03) and INV-002 (M-05) remain unaddressed HIGH invariants; convergence_status BLOCKED_BY_INVARIANTS
