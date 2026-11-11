| step | id | theme | verifier reason |
|---|---|---|---|
| VF1 | M1 | T1 | D3(a) rules out only Phase 4 pr-submit changes, so AC-1.1 requiring a section on pr-submit in P1 does not fail on the recommended choice; the spec has no text saying a gated command is dispatched with `--unattended` before its gate phase lands, so the stall needs an added assumption. |
| VF1 | M8 | other | The spec is silent on whether `--resume` passes a gate, and 3.2 lists no per-command required brief flags, so that no happy path can reach `succeeded` is an inference not stated in the candidate. |
