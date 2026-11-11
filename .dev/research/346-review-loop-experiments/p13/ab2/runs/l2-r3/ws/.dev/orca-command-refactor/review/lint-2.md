lint: superclaude review lint, review-lint/1, sha256 032a73216d9fa2a2e58b2be6fa0c2ed6374df75cb60076a9b7d7f4bd03d07a67

Checks: REF. Findings: 2.

### LINT-REF-1

- check: REF (fact)
- lines: 62
- quote: | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the c...
- message: F-1 is referenced but never defined (7 references).

### LINT-REF-2

- check: REF (fact)
- lines: 159
- quote: | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `/sc:load` (F-2) (a no-op w...
- message: F-2 is referenced but never defined (2 references).
