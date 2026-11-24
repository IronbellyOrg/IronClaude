# Issue 540 fix: start here

This is the completed implementation package for the missing swarm completion marker. Foreground, resume and detached-child behavior were repaired; the user separately authorized the detached launcher handoff. The original investigation and all failed intermediate checks are retained as history.

## Current locations

| What to revisit | File |
|---|---|
| Original investigation and its limitations | [Investigation guide](../../../troubleshoot/bug-issue540-completion-marker-20261123191058/README.md) |
| Approved implementation plan | [Plan](TASK-WF-createACheckedFi-20261123-195635.md) |
| Append-only implementation and archive record | [Progress ledger](progress.md) |
| Final independent acceptance review | [Final review](artifacts/final-review.md) |
| Original planning-stage contract, not current execution status | [Planning contract](return-contract.yaml) |
| Foreground positive command-line witness | [Capture](artifacts/foreground-cli-check.txt), [saved marker](artifacts/foreground-cli/done.json), [result contract](artifacts/foreground-cli/return-contract.yaml) |
| Resume positive command-line witness | [Capture](artifacts/resume-cli-check.txt), [saved marker](artifacts/resume-cli/done.json), [result contract](artifacts/resume-cli/return-contract.yaml) |
| Detached negative and positive witnesses | [Appended capture records](artifacts/detached-check.txt), [successful child marker](artifacts/detached-cli/verified/out/done.json), [result contract](artifacts/detached-cli/verified/out/return-contract.yaml) |
| Combined affected-test results | [Runtime checks](artifacts/final-runtime-check.txt) |
| Completion documentation and local-link checks | [Reference checks](artifacts/reference-doc-check.txt), [monitoring checks](artifacts/monitoring-doc-check.txt) |
| Retry history and reviewer notes | [Detached review](artifacts/retries/T3/operator-review-2.md), [reference review](artifacts/retries/T4/review-2.md), [monitoring review](artifacts/retries/T5/review-1.md) |
| Transferred-evidence validation | [Path audit](../../../research/issue540-transfer-path-audit-20261124.json) |
| Exact portable file locations | [File-location index](../../../research/issue540-current-file-locations.json) |

## Historical paths are not live links

This package originally lived at `.dev/tasks/to-do/TASK-WF-createACheckedFi-20261123-195635/`. The managed archive helper moved it to `.dev/tasks/done/TASK-WF-createACheckedFi-20261123-195635/` after the final review. For a captured path beginning with the old package location, keep the suffix and use this folder instead. The file-location index records that mapping for every saved file.

Absolute paths embedded in saved commands, marker `contract_path` values, contracts, logs and reviewer inputs describe the location **at capture time**. Their corresponding files are linked above and indexed at their current repository-relative locations. Original captures have not been rewritten to pretend they were produced after the move. Do not recreate the old `to-do` directory or run historical helper scripts as current reproduction instructions.

The planning contract preserves the failed advisory planning review and its then-pending implementation authorization. Current execution completion is in the progress ledger and final review, not in that planning-stage prose. Earlier failed checks are likewise historical, not replacements for the later passing outcomes.

## Later formatting cleanup

After archiving, the user requested the remaining test import-spacing cleanup. A blank line was added in `tests/swarm/test_commands_run.py`, and lint passed for all five changed Python files; the whitespace check also passed. The earlier failed lint log remains preserved as the actual earlier result. That cleanup did not change runtime behavior or rerun the whole final acceptance review.

## Revisit checks

- Original transferred files: verify hashes using the investigation's transfer receipt. The added navigation guide is not one of those original 61 files.
- Code citations from the original diagnosis: use recorded revision `db57e231863078dbbb8e4e5fb37a61371c89806c`, not present-day source line numbers.
- Package-local evidence: start from the links in this guide or the portable index, not absolute paths copied from historical logs.
- No commit, push, pull request or merge is implied by completion or by this navigation update.
