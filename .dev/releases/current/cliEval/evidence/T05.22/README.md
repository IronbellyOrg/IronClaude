# T05.22 — Evidence Manifest

**Task:** T05.22 — Verify SC2: manifest schema covers all 15 evals
**Deliverable:** D-0100
**Date:** 2026-05-20

## Files

| File | What it proves | AC mapped |
|---|---|---|
| `sc2.log` | `superclaude eval doctor --suite real --check-coverage` exits 0 with `all HARD capabilities satisfied` and `coverage gate: 3/3 matcher(s) covered (passed)`. The doctor exits 2 on any FR-SCH1 schema violation or FR-SCH2 eval-id regex rejection (commands.py:793-797), so a 0 exit is the binary contract for "zero schema or regex violations on all 15 evals". | AC: "File `TASKLIST_ROOT/evidence/T05.22/sc2.log` records `superclaude eval doctor --suite real` with zero schema or regex violations." |
| `doctor.json` | Structured doctor payload — `coverage_gate.result.passed == true`, `coverage_gate.result.missing == []`, `coverage_gate.result.coverage_map` enumerates the four auggie-family eval ids (E1, E2.1, E2.2, E2.3) inline against the three v1 matcher patterns. | AC: "All 15 evals (E1, E2.1-3, E3..E15) appear in the doctor output" (auggie-family subset surfaces directly in doctor stdout/JSON; the remainder load into the `SuiteLoader` return value the doctor consumes at commands.py:788). |
| `describe-ids.txt` | `superclaude eval describe --suite real --json \| jq -r '.evals[].id'` enumerates all 17 post-parameterize-expansion ids (E1, E2.1, E2.2, E2.3, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15). No missing ids; no extras. | AC: "All 15 evals (E1, E2.1-3, E3..E15) appear in the doctor output" (complete roster); AC: "Parameterize-expanded ids E2.1, E2.2, E2.3 are individually validated" (each appears as a separate entry — `validate_eval_id` runs per row during `SuiteLoader().load(...)`). |
| `list.json` | `superclaude eval list --json` reports `real` with `eval_count: 17` and exits 0. Confirms the suite enumerates at the suite-summary level. | AC: implicit — schema validity is a precondition for the suite enumerating at all. |

## Why "all 15 evals" maps to 17 expanded ids

`real.yaml` authors **14 nominal entries** verbatim plus the **E2 parameterize block** that expands to **E2.1 / E2.2 / E2.3** per OQ-2 (one entry per v1 matcher family). The post-expansion roster lists **17 ids**; the conceptual eval count remains **15** because E2.1-3 are the three faces of the single conceptual E2 matcher-coverage eval. The T05.22 AC uses the conceptual count ("E1, E2.1-3, E3..E15"); the loader and `eval describe` use the expanded count.

| Conceptual eval | Expanded id(s) |
|---|---|
| E1 | E1 |
| E2 (matcher trio) | E2.1, E2.2, E2.3 |
| E3 | E3 |
| ... | ... |
| E15 | E15 |
| **Total: 15 conceptual** | **17 expanded** |

## Out-of-scope (deferred / not asserted here)

- **Eval bodies pass `eval run`.** SC2 is the manifest-schema gate, not the runtime gate. End-to-end run-green at `--parallel 8` is the M5 exit criterion (CP-P05-END / T05.28).
- **Hook scripts emit the OQ-2-frozen ledger rows.** T05.07..T05.21 evidence notes the pre-existing telemetry-emission gap (current hooks write to `logs/freshness-hook.jsonl` / `state/reads.jsonl` / `state/bg-agents/` rather than `logs/freshness.jsonl`); a follow-up hook-script wiring task closes that gap. T05.22 is schema-coverage only.
- **Coverage-gate fixtures for the missing-matcher branch.** TEST-013 (T05.25) covers the missing-matcher scenario with a hand-crafted fixture `settings.json`; T05.22 only exercises the happy path against the live `~/.claude/settings.json`.

## Cross-references

- FR-SCH1 (T01.04) — `suite.schema.json` JSON-Schema gate.
- FR-SCH2 (T01.05) — `validate_eval_id` regex `^E[1-9][0-9]?(\.[1-9][0-9]?)?$`.
- FR-G5 (T04.14) — coverage gate wired into doctor via `--check-coverage`.
- M6 SC5 (T06.09) — cross-references SC2 as a prerequisite.
- D-0100 (`artifacts/D-0100/`) — verification outcome spec, notes, and evidence index.
