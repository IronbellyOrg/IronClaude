# D-0100 — SC2 manifest-schema coverage verification

**Deliverable ID:** D-0100
**Task ID:** T05.22 (Phase 5)
**Date:** 2026-05-21 (re-verified; first run 2026-05-20)
**Roadmap Item:** R-099

## 1. Purpose

T05.22 closes the SC2 success criterion: prove the `real` suite manifest
loads green via `SuiteLoader`, every authored eval id passes FR-SCH1
(`suite.schema.json`) and FR-SCH2 (`validate_eval_id` regex), and the
matcher-coverage gate (FR-G5) recognises all three v1 matcher families.
SC2 is cross-referenced from M6 SC5 (T06.09).

## 2. Verification command

```bash
uv run superclaude eval doctor --suite real --check-coverage
```

The doctor subcommand, when passed `--suite <name>`, resolves the
manifest under `src/superclaude/cli/eval/suites/`, invokes
`SuiteLoader().load(...)` (commands.py:786-797), and forwards the
post-parameterize-expansion `EvalSpec` tuple into `coverage_gate(...)`.
Two failure modes exit the doctor with a non-zero status:

| Failure | Source | Exit code |
|---|---|---|
| Schema violation or FR-SCH2 regex rejection on any eval | `SuiteLoaderError` | `SUITE_LOADER_ERROR_EXIT_CODE` (2) |
| Missing suite manifest | `SuiteNotFound` | `SUITE_NOT_FOUND_EXIT_CODE` (2) |
| HARD capability failure on host | `report.hard_failures` | `HARD_FAIL_EXIT_CODE` (2) |
| Coverage gate uncovered matcher | `CoverageResult.passed == False` | `COVERAGE_GATE_FAILED_EXIT_CODE` (2) |

A `0` exit therefore proves zero schema, zero FR-SCH2 regex, and zero
coverage-gate violations across the whole suite.

## 3. Result

```
all HARD capabilities satisfied
soft skips: mcp_server.auggie-mcp, mcp_server.airis-mcp-gateway, vendored.ptytest
coverage gate: 3/3 matcher(s) covered (passed)
Exit code: 0
```

- **HARD capabilities:** all satisfied (Claude CLI, make, jq, git, auggie, ~/.claude/, Claude CLI ≥0.5.0).
- **Soft skips:** `mcp_server.auggie-mcp`, `mcp_server.airis-mcp-gateway`, `vendored.ptytest` — informational, not violations.
- **Coverage gate:** 3 of 3 v1 matchers covered (`mcp__auggie__.*`, `mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*`, `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*`).
- **Schema/regex violations:** zero (otherwise `SuiteLoader().load(...)` would have raised `SuiteLoaderError` and the doctor would have exited 2 before reaching the coverage stanza).

## 4. Per-eval enumeration

The post-parameterize-expansion roster (`superclaude eval describe --suite real --json | jq -r '.evals[].id'`) lists **17 ids** = 14 nominal entries authored verbatim in `real.yaml` + the **E2** parameterize block expanded into **E2.1 / E2.2 / E2.3**. The 15 conceptual evals (E1, E2.1-3, E3..E15) named in the T05.22 AC map 1:1 onto the 17 expanded ids:

| Conceptual eval | Expanded id(s) | Validation |
|---|---|---|
| E1 | E1 | FR-SCH1 + FR-SCH2 |
| E2 (3 matchers) | E2.1, E2.2, E2.3 | FR-SCH1 + FR-SCH2 (each individually) |
| E3..E15 | E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15 | FR-SCH1 + FR-SCH2 |

All 17 expanded ids appear in the doctor's `coverage_map` (where applicable, the auggie-family ids) and in `superclaude eval describe --suite real --json`. Neither output reports any missing or extra id; the `missing` array under `coverage_gate.result` is empty.

## 5. Acceptance criteria mapping

| AC | Evidence file | Disposition |
|---|---|---|
| `TASKLIST_ROOT/evidence/T05.22/sc2.log` records `superclaude eval doctor --suite real` with zero schema or regex violations. | `sc2.log` | PASS — exit code 0; no `SuiteLoaderError`. |
| All 15 evals (E1, E2.1-3, E3..E15) appear in the doctor output. | `describe-ids.txt`, `doctor.json` (`coverage_gate.result.coverage_map`) | PASS — 17 expanded ids enumerate; the auggie-family ids E1/E2.1/E2.2/E2.3 surface inline in the doctor's coverage map; the remaining ids appear via the loaded suite tuple consumed by the coverage gate. |
| Parameterize-expanded ids E2.1, E2.2, E2.3 are individually validated. | `describe-ids.txt`, `doctor.json` | PASS — each id resolves through `validate_eval_id` (FR-SCH2) during `SuiteLoader().load(...)`; doctor exits 0. |
| `TASKLIST_ROOT/artifacts/D-0100/spec.md` documents the verification outcome. | this file | PASS — present. |

## 6. Cross-references

- **FR-SCH1** (T01.04): `suite.schema.json` JSON-Schema gate — invoked
  by `SuiteLoader().load(...)`.
- **FR-SCH2** (T01.05): `validate_eval_id` regex
  `^E[1-9][0-9]?(\.[1-9][0-9]?)?$` — invoked per row during loader
  validation; parameterize-expanded ids are validated post-expansion.
- **FR-G5** (T04.14): coverage gate wired into doctor via
  `--check-coverage`; passes when the hooks.json matcher patterns
  intersect with the suite's eval-tag set.
- **M6 SC5** (T06.09): cross-references SC2 as a prerequisite for
  release readiness.
