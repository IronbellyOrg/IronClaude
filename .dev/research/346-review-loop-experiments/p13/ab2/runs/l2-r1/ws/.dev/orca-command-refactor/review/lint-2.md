lint: superclaude review lint, review-lint/1, sha256 746b5ffc5ac4b78a7e2053e0e341cc67756a46ac8a09ff6161b886dedded7fa2

Checks: REF. Findings: 2.

### LINT-REF-1

- check: REF (fact)
- lines: 62
- quote: | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the c...
- message: REQ-1 is referenced but never defined (4 references).

### LINT-REF-2

- check: REF (fact)
- lines: 159
- quote: | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag and `## Unattended mode` section on each command whose own row is P1, plus the ready...
- message: REQ-2 is referenced but never defined (2 references).
