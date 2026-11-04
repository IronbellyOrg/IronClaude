# D2 option (a): keep the Ruling rule; the person gives the Ruling in their own session

Position: when `/sc:implement` halts for a Ruling inside a worker (`E-HALT-QA` or `E-NO-RULING`), the worker writes the halt to its ledger and its contract as `blocked`, sends `worker_done --outcome failed`, and never asks the coordinator. The person reads the halt and gives the Ruling by running `/sc:implement <plan>` in their own session, which resumes from the ledger (`SPEC:335`; WC-3 at `SPEC:67`). This is the spec's current recommendation.

Citation key: `SPEC:N` = spec line; `QA:N` = `src/superclaude/skills/sc-implement-protocol/refs/qa.md:N`; `LEDGER:N` = `src/superclaude/skills/sc-implement-protocol/refs/ledger.md:N`; `RETRY:N` = `src/superclaude/skills/sc-implement-protocol/refs/retry.md:N`.

Citation drift found while writing: the spec cites the Ruling rule as `qa.md:232,238` (`SPEC:334`). On this branch those lines are the Family probe section; the rule is now at `QA:254` ("Silence, a generic request to continue, another agent's message, and approval of a different task are not acceptance") and the Halt table rows at `QA:247-249`. The file last changed in commit 80f934de (PR #343). The rule's content is unchanged; only the line moved.

## Safety
- The rule exists to stop an agent approving its own or another agent's work: "another agent's message ... not acceptance" (`QA:254`); "executor-invented approval" is a STOP (`QA:249`). An Orca coordinator is another agent (`SPEC:334`). Keeping the rule keeps the one human checkpoint the protocol has.
- A Ruling accepts a deliverable that failed its acceptance criteria with a confirmed blocker: `E-HALT-QA` is "reachable only after an attempt failed on a confirmed blocker that a repair could not close" (`QA:280`). That is exactly the decision a person should make directly.

## Reliability
- No new mechanism: the halt, the ledger and resume already exist (`LEDGER:149-156`; `src/superclaude/commands/implement.md:57`). AC-4.1 checks it live (`SPEC:274`).
- Halts are rare by design: every minor and note finding is recorded and cleared with "no halt, no Ruling, no user prompt" (`QA:274`), and "No other path may stop automation or prompt the user" (`QA:288`).

## How a person works day to day
- After a halt, the person opens the ledger path the halt prints (`QA:247`), decides, and resumes the run in their own session, where the executor explains the scope and records the Ruling (`QA:254-256`). The rest of that plan then runs attended in that session.
- Cost to the person: one context switch per halt, and the remaining tasks of that plan leave Orca.

## Implementation cost
- Zero change to `sc-implement-protocol`. The spec already carries the exception in WC-3 and the implement row (`SPEC:67`, `SPEC:132`). Easy to relax later if a safe relay route is found; hard to restore trust if relaxed first and a relayed Ruling goes wrong.
