# Return contract 1.1

Write `.dev/tasks/to-do/<id>/return-contract.yaml`. Paths inside the package are package-relative (`./…`) so the file stays valid after the package moves to `done/`:

```yaml
contract_version: "1.1"
status: success | partial | failed
slug: <id>
plan_path: ./<id>.md | null
source_path: ./source.md | null
source_origin: <original path or "inline">   # informational only; never used for lookup
strategy: systematic | agile | enterprise
depth: quick | standard | deep
handoff_action: none | design | implement | tasklist
handoff_output_path: ./progress.md | null
reflect_status: success | partial | failed | skipped   # Wave 4 `/sc:reflect --mode pre`; advisory only
reflect_report_path: <abs path to reflect REPORT.md> | null
unresolved: []
```

`reflect_*` are additive and advisory: they never change `status`. A generation `failed` contract (reflect never ran) uses `reflect_status: skipped`, `reflect_report_path: null`.

## Status

| Situation | status | plan_path |
|-----------|--------|-----------|
| Plan gated; handoff `none`/`design`/`tasklist` text emitted, or `implement` accepted | `success` | `./<id>.md` |
| Plan gated but the `--handoff implement` invocation failed (skill missing, implement STOP) | `partial` | `./<id>.md` — the plan stays valid and executable; list the reason in `unresolved` |
| Package exists but generation failed (`E-NO-PHASES`, `E-GATE`, write error) | `failed` | `null` (`source_path` `./source.md` if the snapshot was written, else `null`) |

## Handoff relocation rule

Write the contract (`status: success`, `handoff_action: implement`, `handoff_output_path: ./progress.md`) **before** invoking `implement`. `implement` may archive the package into `.dev/tasks/done/<id>/`, including when it errors after the move. Afterwards resolve the package by id; a contract rewrite (to `partial`) is allowed only while the package is still at `.dev/tasks/to-do/<id>/`. If only `done/<id>` exists, never write, recreate a directory, or "fix" the contract: the archived contract stays as written, the outcome goes to chat with the actual path. If both locations exist, mutate neither and report the conflict. Contract links stay package-relative `./` and the status of a valid plan stays non-failed.

A failed *generation* (no valid plan) and a failed *execution handoff* (valid plan) are different states: never mark a valid gated plan `failed`, never mark a failed generation `success`/`partial`.

## When no contract is written

STOPs before the package exists (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-LEGACY` including retired `--output`, `E-BAD-FLAG`, `E-PACKAGE-COLLISION`): chat only — **no package directory, no yaml**.

After the package exists: any STOP → write the `failed` contract; delete a draft `<id>.md` that failed the gate.

## Worker contract (`--unattended`)

Written to `<report-dir>/return-contract.yaml` (the one directory passed with `--report-dir`, never the package) on every outcome. The package contract above is unchanged.

```yaml
worker_contract_version: "1"
worker_status: succeeded | partial | failed
command: <the exact command line>
report_path: <repo path of the plan <id>.md, in to-do/ or, after an archive, done/> | null
artifacts: [<package return-contract.yaml>, <package source.md>]   # [] before a package exists
reason: <the STOP code or the failure>                              # only when failed
```

Status mapping: package `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`. A pre-creation STOP → `failed` with the STOP code in `reason` and `report_path: null`. A skipped `--handoff implement` makes the package contract `partial` with one `unresolved` line.
