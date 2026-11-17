# Codegraph grounding

## Run state

- index_state: not checked (documents-only change; Grep, Glob and Read used as the floor)
- token: graph:skipped-docs-only

## Resolved symbols

- src/superclaude/core/WORKER-CONTRACT.md:57 (sentence containing "decision D2, amended 2026-11-17 by the owner: no approval is ever required to be written into a file by the person")
- docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:722 (table row for `WORKER-CONTRACT.md:57`, containing "D2, amended 2026-11-17: the person never has to write a file")

## Dependents

- Grep over tracked files outside .dev/ and .claude/ for the old phrases: only the two lines above match. No plugins/ mirror of either file.
- tests/skills/test_worker_contract.py and tests/issue_pipeline/test_brief.py mention WORKER-CONTRACT; neither pins the phrases "never has to write" or "required to be written" (Grep over tests found no match).
- Report-only: docs/designs/issue-pipeline-fu1.md:106 ("the owner never has to write a file"), about the live test's go and written acceptance.

## Pre-check

Both files and both lines exist as named. No unnamed dependents.
