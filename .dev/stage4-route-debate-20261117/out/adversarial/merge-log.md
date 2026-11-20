# Merge Log

## Metadata
- Base: variant 2 (Route B)
- Executor: orchestrator (no separate merge-executor agent was spawned; the merge is one short document)
- Changes applied: 5 of 5
- Status: success
- Timestamp: 2026-11-17

## Changes Applied
1. Precondition inserted (owner decides the gate first). Provenance tag in merged-output.md "Precondition".
2. Route step 2 replaced: edit request and `source.md` together, verify with `cmp`.
3. Route step 3 replaced and step 4 added: slug equal in folder, file name and plan; contract 1.1; run and read `/sc:reflect --mode pre`.
4. Risks: ledger-rule departure recorded as an owner-approved exception.
5. New section "Switch to Route A when" with three triggers.

## Post-Merge Validation
- Structure: headings H1, then H2 only; no level gaps. Pass.
- Internal references: README.md:9, README.md:3 and managed-workspace.md:9-12 re-checked against disk (README read earlier this session; detection lines grep-confirmed in this run). Resolved: 3 of 3. Broken: 0.
- Contradiction re-scan: no new contradiction. One tension left on purpose: the merged route departs from README.md:3, and says so.

## Summary
Planned 5, applied 5, failed 0, skipped 0.
