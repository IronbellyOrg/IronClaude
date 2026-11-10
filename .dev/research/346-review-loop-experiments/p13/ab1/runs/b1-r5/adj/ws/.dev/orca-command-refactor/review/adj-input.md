# Findings to adjudicate

### X1

- anchor: "runs one layer below the worker, inside Claude Code's nesting limit"
- refs: 3.2, WC-7
- claim: The tasklist row keeps reflect fan-out in subagents against INV-B's needs-change verdict, and its depth is not counted against the three-layer limit.

### X2

- anchor: "A command step that blocks a single tool call for longer than 5 minutes"
- anchor2: "4 minutes leaves a margin under the 5-minute heartbeat cadence"
- refs: WC-10
- claim: The split trigger is 5 minutes while the rationale wants 4 minutes of margin, so a 4:30 or 5:00 call is left unsplit.

### X3

- anchor: "grep -E '^-[^-]'"
- refs: SA-4
- claim: The diff filter misses removed blank lines and removed lines beginning with two dashes, so non-additive edits pass.

### X4

- anchor: "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"
- anchor2: "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed"
- refs: 2.1, 2.3, 3.1, 7.2, AC-0.1, AC-0.4, AC-1.1, AC-1.4, AC-2.2, P0, P1, P2, P4, SA-3, SA-4, WC-12, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9
- claim: The adversarial row puts the contract one directory below the path WC-4 tells the coordinator to read, so the report path handed to worker_done does not exist.

### X5

- anchor: "are not counted by Orca's nesting limit"
- refs: -
- claim: E4 presents as evidence a point the inventory marks UNVERIFIED.

### X6

- anchor: "What changes in the commands is limited to the worker contract in section 2"
- anchor2: "reconcile the flag surface the command calls unsupported with the flags the skill still defines"
- refs: 1.1, 2.1, SA-4
- claim: The scope statement says only the contract changes commands, but §3.2 requires other changes such as the roadmap flag reconciliation.

### X7

- anchor: "make `--remediate` follow the existing headless auto-accept rule"
- refs: P2
- claim: Reflect is labelled ready today, but its row requires a P2 change.

### X8

- anchor: "The only end-to-end proof is the PR #329 run"
- anchor2: "invocation_method: \"skill-direct\""
- refs: 1.4
- claim: Section 1.4 says PR #329 is the only end-to-end proof and no direct-route run was observed, while E3 cites a skill-direct worker contract.

### X9

- anchor: "inside Claude Code's nesting limit"
- anchor2: "its reflect fan-out runs one layer below the worker"
- refs: -
- claim: The tasklist nesting claim is not counted: at the depth limit the reflect Agent tool is withheld and the fan-out fails silently, and the inventory's required change is dropped without a recorded decision.

### X10

- anchor: "prints nothing (SA-2, WC-8)"
- refs: P0, SA-2, SA-5, WC-8
- claim: The grep over core may fail on the Orca text P0 adds to core files, depending on a wording the spec does not fix.

### X11

- anchor: "stays a worker candidate only if the user accepts open decision D3"
- anchor2: "**Coordinator or person only (recommended).**"
- refs: 3.2
- claim: The 27-command count and the pr-submit row assume D3 option (b), while the spec recommends option (a), so the classification is not stable.

### X12

- anchor: "no `--remediate`; `--no-promote` when the coordinator owns folder moves"
- refs: WC-11, WC-9
- claim: Reflect's default tracked-file write and folder move are not covered by any unattended rule.

### X13

- anchor: "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies"
- refs: WC-2
- claim: The tasklist HALT on needs_human_decision items has no resolution, so a tasklist worker can stop without worker_done.

### X14

- anchor: "must fall back on its own well inside the readiness limit"
- refs: WC-1
- claim: The fallback has no numeric bound, so an implementer cannot tell whether a 50 s fallback is compliant.

### X15

- anchor: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4."
- refs: -
- claim: Phase gating by user decision is stated two ways and D1 and D4 touch earlier phases.

### X16

- anchor: "This worker re-read 11 of the load-bearing locations on 2026-11-02"
- refs: -
- claim: Many citations point to files outside the workspace, so this review could not check them.
