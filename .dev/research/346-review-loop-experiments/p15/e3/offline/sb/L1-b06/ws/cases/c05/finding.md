**F-3 [BLOCKING] `/sc:load` must name a contract, but its row and its Decisions entry say it writes none.**
- Experts: Wiegers (traceability), Crispin.
- Text: AC-1.1 (`SPEC:195`) requires every command in sections 3.1-3.2 to have a `## Unattended mode` section that names `return-contract.yaml`. `load` is in section 3.2 (`SPEC:112`), with "none (see note)" in the Report column. Its Decisions row (`SPEC:265`) says "a report file would be an unrequested addition." WC-4 (`SPEC:62`) requires the contract "on every outcome".
- Grading sentence: an implementer who follows the `load` row and the Decisions row adds no contract, so AC-1.1 fails for `load`. An implementer who makes AC-1.1 pass adds the report file that `SPEC:265` forbids.
- Recommendation: exclude `load` explicitly from WC-4 and from AC-1.1, in the way section 4 is excluded, or give `load` a contract and remove the Decisions row.
- Priority: High.
