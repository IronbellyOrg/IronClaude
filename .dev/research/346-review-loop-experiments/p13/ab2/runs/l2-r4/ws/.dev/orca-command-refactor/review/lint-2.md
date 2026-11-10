lint: superclaude review lint, review-lint/1, sha256 64ace65d5ab1437b097ef30b7325e413a6e90e0ea575952d431a0fa4c73ce23e

Checks: REF. Findings: 2.

### LINT-REF-1

- check: REF (fact)
- lines: 147
- quote: | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an exam...
- message: F-2 is referenced but never defined (2 references).

### LINT-REF-2

- check: REF (fact)
- lines: 159
- quote: | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by each command listed in this row except load (a no-op where a command has...
- message: F-1 is referenced but never defined.
