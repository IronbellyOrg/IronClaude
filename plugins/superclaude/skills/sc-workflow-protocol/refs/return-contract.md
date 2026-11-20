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
handoff_action: none | design | implement
handoff_output_path: ./progress.md | null
reflect_status: success | partial | failed | skipped   # Wave 4 `/sc:reflect --mode pre`; advisory only
reflect_report_path: <abs path to reflect REPORT.md> | null
unresolved: []
# additive remediation fields (Wave 4R, `refs/remediation.md`); each is absent until the step below writes it
remediation_route: surgical | regenerate      # written by `place` (surgical) or `mark` (regenerate), on the new package
supersedes: <old-id>                          # written by `place` or `mark`, on the new package
superseded_by: <new-id> | none                # written by `archive` (and `mark`), on the archived package
finding_counts: {blocking: <n>, label_high: <n>, medium: <n>, note: <n>}   # the counts the route was chosen from; written with `remediation_route`
fix_cycles: <n>                               # fix cycles run (0 to 2); written by `mark`
review_verdict: FAIL                          # written by `mark` only when blockers stay open after the last cycle; absent otherwise
open_blockers: [<finding id>, ...]            # written by `mark` together with `review_verdict: FAIL`
```

On the regenerate route `mark` runs before Wave 5, so when the new package has no contract yet `mark` creates a minimal one (`contract_version: "1.1"`, `status: partial`, `slug`, then the keys it marks); Wave 5 merges into it, sets the final `status` over that `partial` and keeps the mark lines.

The seven remediation fields are additive: `contract_version` stays `"1.1"` and `/sc:implement` keeps accepting only `"1.1"`. Only `remediate.py` writes them (by appending or replacing one line, never by re-writing the YAML), and Wave 5 keeps every line of them.

`reflect_*` are additive and advisory: they never change `status`. A generation `failed` contract (reflect never ran) uses `reflect_status: skipped`, `reflect_report_path: null`. For a package that replaced another, `reflect_status` records the re-review verdict and its scope ("changed lines plus prior blockers"), not a full review of the plan.

## Status

| Situation | status | plan_path |
|-----------|--------|-----------|
| Plan gated; handoff `none`/`design` text emitted, or `implement` accepted | `success` | `./<id>.md` |
| Plan gated but the `--handoff implement` invocation failed (skill missing, implement STOP) | `partial` | `./<id>.md` — the plan stays valid and executable; list the reason in `unresolved` |
| Package exists but generation failed (`E-NO-PHASES`, `E-GATE`, write error) | `failed` | `null` (`source_path` `./source.md` if the snapshot was written, else `null`) |

## Handoff relocation rule

Write the contract (`status: success`, `handoff_action: implement`, `handoff_output_path: ./progress.md`) **before** invoking `implement`. `implement` may archive the package into `.dev/tasks/done/<id>/`, including when it errors after the move. Afterwards resolve the package by id; a contract rewrite (to `partial`, or any other) is allowed only while the package is still at `.dev/tasks/to-do/<id>/`, and every rewrite merges into the existing file: it changes only the keys it owns (`status`, `reflect_*`, `handoff_*`, `unresolved`, and any stable 1.1 field still missing) and keeps every other line, including those `place` and `mark` wrote (`supersedes`, `remediation_route`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`). If only `done/<id>` exists, never write, recreate a directory, or "fix" the contract: the archived contract stays as written, the outcome goes to chat with the actual path. If both locations exist, mutate neither and report the conflict. Contract links stay package-relative `./` and the status of a valid plan stays non-failed.

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
artifacts: [<package return-contract.yaml>, <package source.md if written>, <each file reflect wrote in its <report-dir>/nested/reflect-<n>/ run directory, whatever reflect_status is>, <docs/memory/reflect/deviation-patterns-<slug>.md if reflect wrote it>]   # [] before a package exists; gitignored .dev/reflect/runs.jsonl and .superclaude/memory/ are left out (WC-4 in ~/.claude/WORKER-CONTRACT.md)
                                                                    # artifacts also lists the nested reflect contract <report-dir>/nested/reflect-<n>/return-contract.yaml, also when the call failed
reason: <the STOP code or the failure>                              # only when failed
```

Status mapping: package `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`. A pre-creation STOP → `failed` with the STOP code in `reason` and `report_path: null`. A skipped `--handoff implement` makes the package contract `partial` with one `unresolved` line.
