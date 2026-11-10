# Findings to adjudicate

### X1

- anchor: "make `--remediate` follow the existing headless auto-accept rule"
- anchor2: "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies"
- refs: SA-6, WC-9
- claim: Unattended reflect may auto-accept remediation that edits code, and the spec does not say the brief must authorize it; the headless trigger also changes from claude --print to a flag.

### X2

- anchor: "Any such prompt must fall back on its own well inside the readiness limit (default 60 s)."
- refs: WC-1
- claim: WC-1 gives no number, no delivering phase and no check.

### X3

- anchor: "(worker reached `state: ready, stage: input_accepted` and answered)"
- refs: -
- claim: The inventory quote of EVIDENCE.md:45 records only the ready state, so the 'answered' claim in E2 is not supported by the quoted evidence.

### X4

- anchor: "invocation_method: \"skill-direct\""
- anchor2: "so it proves the nested route, not the direct route this spec requires"
- refs: 1.4, WC-7
- claim: E3 and 1.4(1) use the same evidence for opposite points.

### X5

- anchor: "so the session can already heartbeat between iterations"
- anchor2: "Apply the section 3 row (wait splitting, summary file, HALTs as blocked)"
- refs: 3.2, AC-4.3, WC-10
- claim: The pr-submit wait reading differs from the inventories and D3(b) names a wait change the row says may be unneeded.

### X6

- anchor: "This worker re-read 11 of the load-bearing locations on 2026-11-02"
- refs: -
- claim: The re-read and validator claims cannot be reproduced from the workspace.

### X7

- anchor: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"
- anchor2: "--unattended --output <file>` with a bare topic"
- refs: 2.3, 3.1, 4, AC-2, AC-2.2, SA-3, WC-2, WC-3, WC-4, WC-5, WC-6
- claim: WC-4 puts the contract inside a directory the coordinator passes, but tdd and init-lite take a file-valued --output and adversarial and workflow fix other paths, so the contract location is contradictory.

### X8

- anchor: "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit"
- refs: 3.2, WC-7
- claim: The nesting claim for tasklist has no layer count.

### X9

- anchor: "`run` requires `--suite` and the safety flags in the brief, else blocked"
- refs: SA-1
- claim: The spec never names the safety flags, so an implementer cannot decide whether a given cli-eval brief passes or blocks.

### X10

- anchor: "use it as a step inside another worker"
- anchor2: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming return-contract.yaml"
- refs: AC-1.1, WC-4, WC-5
- claim: AC-1.1 requires a contract for load, the decision table rejects it, and WC-5 then sends a successful load run as failed.

### X11

- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "a report file would be an unrequested addition"
- refs: 2.1, 2.3, 3, 3.1, 3.2, 6, 7.2, AC-0.4, AC-1.1, AC-1.2, P0, P1, P2, P4, SA-2, WC-11, WC-4, WC-9
- claim: AC-1.1 requires /sc:load to carry a return-contract.yaml section while its row and the Decisions table say it gets no report file, so the P1 check cannot pass.

### X12

- anchor: "blocks a single tool call for longer than 5 minutes"
- anchor2: "no single tool call exceeds 240 s"
- refs: AC-4.3, WC-10
- claim: A 4 to 5 minute call is allowed by WC-10 and fails AC-4.3.

### X13

- anchor: "requires `--suite` and the safety flags in the brief, else blocked"
- refs: 3.2, AC-2.2, AC-2.4, P2, WC-2, WC-9
- claim: The safety flags are not defined anywhere in the spec, so the cli-eval run gate cannot be implemented or tested as written.

### X14

- anchor: "its reflect fan-out runs one layer below the worker"
- refs: -
- claim: The tasklist nesting claim rests on an UNVERIFIED docs citation and is stated as settled.

### X15

- anchor: "\\borca(-ide)?[[:space:]]+(orchestration\\|worktree\\|terminal\\|agent)\\b"
- refs: SA-2, WC-8
- claim: In grep -E the escaped pipe is a literal, so AC-C1 never matches an Orca call and always passes, which hides an SA-2 violation.

### X16

- anchor: "would be refused with `nested_worker_depth_exceeded`"
- refs: 1.3
- claim: R1 states as fact that a nested worker-start is refused, but UNVERIFIED item 5 says call-site enforcement was not traced, so the rejection rests on an unchecked claim.
