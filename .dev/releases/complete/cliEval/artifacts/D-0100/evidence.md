# D-0100 — Evidence index

**Task:** T05.22 — Verify SC2: manifest schema covers all 15 evals
**Deliverable:** D-0100
**Date:** 2026-05-20

## Evidence files

| File | Source command | Proves |
|---|---|---|
| `evidence/T05.22/sc2.log` | `uv run superclaude eval doctor --suite real --check-coverage` | Doctor exits 0 — zero schema/regex violations, all HARD capabilities satisfied, coverage gate 3/3 matchers covered. |
| `evidence/T05.22/doctor.json` | `uv run superclaude eval doctor --suite real --check-coverage --json` | Structured doctor payload — `coverage_gate.result.missing == []`, `passed: true`, `coverage_map` enumerates the auggie-family eval ids (E1, E2.1, E2.2, E2.3) inline. |
| `evidence/T05.22/describe-ids.txt` | `uv run superclaude eval describe --suite real --json \| jq -r '.evals[].id'` | Post-parameterize-expansion roster — 17 expanded ids (E1, E2.1, E2.2, E2.3, E3..E15) load green via `SuiteLoader().load(...)`. |
| `evidence/T05.22/list.json` | `uv run superclaude eval list --json` | Suite-level summary — `real` enumerates with `eval_count: 17` (no parse error). |

## Per-AC mapping

- **AC1 — `sc2.log` records zero schema/regex violations:** `sc2.log` shows exit code 0
  with no `SuiteLoaderError` line in stderr. The doctor exits 2 on any FR-SCH1 or FR-SCH2
  violation (commands.py:793-797), so a 0 exit is the contract for "zero violations".
- **AC2 — All 15 evals appear in the doctor output:** `describe-ids.txt` enumerates all
  17 expanded ids; `doctor.json` `coverage_gate.result.coverage_map` lists the auggie-family
  ids (E1, E2.1, E2.2, E2.3) inline; the remaining ids feed the coverage-gate input via
  the loader return value consumed by `coverage_gate(...)` at commands.py:798-802.
- **AC3 — E2.1, E2.2, E2.3 individually validated:** `describe-ids.txt` lists all three
  as separate entries; the loader's `validate_eval_id` regex runs per row, so the
  post-expansion ids satisfy FR-SCH2 individually.
- **AC4 — `spec.md` documents the verification outcome:** `spec.md` present in this
  artifact directory.

## Reproduction

```bash
# Primary verification (sc2.log content)
uv run superclaude eval doctor --suite real --check-coverage

# Supplementary: structured doctor payload
uv run superclaude eval doctor --suite real --check-coverage --json

# Supplementary: enumerate all 17 expanded eval ids
uv run superclaude eval describe --suite real --json | jq -r '.evals[].id'

# Supplementary: suite-level summary
uv run superclaude eval list --json
```

All four commands exit 0 on the current branch (`feature/sc-auggie-review-protocol`,
commit `2219545` as of 2026-05-20).
