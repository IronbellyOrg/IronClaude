# Defect catalog (defect-catalog/1, built by pn3)

doc sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`

| cid | theme | confirmed | sources | label | anchor span |
|---|---|---|---|---|---|
| D1 | T2 | yes | 18 | WC-4 contract location cannot be resolved for file-valued, nested, generated or absent output flags | [61, 62] |
| D2 | T2 | yes | 4 | WC-6 fresh directory on retry contradicts a fixed, known-before-dispatch output location | [63, 64] |
| D3 | T1 | yes | 13 | P1 ships --unattended on every command before the gates it must disable are converted in P2-P4 | [158, 159] |
| D4 | T3 | yes | 3 | AC-C1 scans core/, where P0 itself adds Orca text, so the check cannot pass | [171, 172] |
| D5 | T2 | no | 1 | Fixed status vocabulary was not checked against the contracts that already exist | [61, 62] |
| D6 | T1 | no | 1 | WC-3 ask protocol is incomplete for commands with several gates | [60, 61] |
| D7 | other | yes | 2 | WC-10 leaves a hole between 4 and 5 minutes and cannot split Monitor-driven or fan-out waits | [67, 68] |
| D8 | other | yes | 2 | WC-9 names no mechanism by which outward actions are authorized and checked | [66, 67] |
| D9 | other | no | 1 | Fan-in of workers is specified for the success case only | [38, 39] |
| D10 | T2 | yes | 2 | A stale contract from an earlier attempt can be read as the current result | [61, 62] |
| D11 | T2 | yes | 2 | The --unattended switch has no token rule, so quoted text can switch gates off | [227, 228] |
| D12 | T1 | yes | 14 | AC-1.1/AC-1.2 demand a contract section for /sc:load, which the spec exempts | [194, 195] |
| D13 | T3 | no | 1 | The spec never says how the worker starts the command, and AC-0.4 does not check the skill loaded | [64, 65] |
| D14 | T1 | no | 1 | No version or capability check before dispatch for older installs or section-4 commands | [75, 76] |
| D15 | other | no | 1 | No rule that --unattended is passed to nested skills and commands | [59, 60] |
| D16 | other | yes | 3 | AC-C5/AC-0.3 grep cannot detect a deleted markdown bullet, so 'additive' is not proved | [175, 176] |
| D17 | T2 | no | 1 | WC-5 treats only a missing report as failure; empty, unparseable or out-of-set contracts are unspecified | [62, 63] |
| D18 | other | no | 1 | WC-2 lists default, flag and blocked with no precedence, and one blocked_question for several gates | [59, 60] |
| D19 | T3 | yes | 7 | AC-0.4 requires a contract that Phase 0 cannot yet produce | [193, 194] |
| D20 | T1 | yes | 5 | Ready commands with no small fix get no section or contract yet P1/AC-1.1/WC-4 expect one | [78, 79] |
| D21 | other | no | 1 | cli-portify can only end blocked under --unattended, yet AC-2.3 requires a succeeded happy path | [104, 105] |
| D22 | other | no | 1 | AC-2.2 requires status blocked for P2 commands whose gates resolve by default or flag | [199, 200] |

## Members

### D1 WC-4 contract location cannot be resolved for file-valued, nested, generated or absent output flags
anchor: `where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)`  (members name tdd/init-lite file-valued --output, adversarial/workflow paths or missing output flags)
a1-r1/R1:F-01, a1-r1/R1:F-02, a1-r2/R1:F4, a1-r3/R1:4, a1-r3/R1:11, a2-r2/R1:B2, a2-r5/R1:B-1, a3-r2/R1:R1-B2, a3-r6/R1:REQ-1, a2-r1/AUD:F-2, a2-r2/AUD:F-01, a2-r3/AUD:ARCH-1, a2-r4/AUD:F-2, a3-r1/AUD:B2, a3-r3/AUD:F-2, a3-r4/AUD:A-02, a3-r1/AUD2:F1, a3-r3/AUD2:B2, a3-r5/AUD2:B-1, a3-r6/AUD2:B1

### D2 WC-6 fresh directory on retry contradicts a fixed, known-before-dispatch output location
anchor: `writes each run into a fresh output directory so a re-run starts clean`  (members name the retry writing into or away from the first attempt's WC-4 directory)
a1-r1/R1:F-02, a1-r3/R1:3, a3-r6/R1:ARCH-1, a1-r1/AUD:B-01

### D3 P1 ships --unattended on every command before the gates it must disable are converted in P2-P4
anchor: `the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)`  (members name the P1 scope/AC-1.1 counts against the later-phase gate conversion and the P4 wait on D2-D4)
a1-r1/R1:F-03, a1-r2/R1:F2, a1-r3/R1:1, a1-r3/R1:2, a3-r2/R1:R1-B1, a3-r4/R1:F-01, a3-r5/R1:F-1, a2-r1/AUD:F-1, a2-r3/AUD:REQ-2, a2-r4/AUD:F-1, a3-r1/AUD:B1, a3-r3/AUD:F-1, a3-r1/AUD2:F2, a3-r3/AUD2:B1

### D4 AC-C1 scans core/, where P0 itself adds Orca text, so the check cannot pass
anchor: `src/superclaude/agents src/superclaude/core`  (members say AC-C1 greps src/superclaude/core while P0 adds WORKER-CONTRACT.md and an Orca section there)
a1-r1/R1:F-04, a1-r2/R1:F3, a1-r3/R1:9

### D5 Fixed status vocabulary was not checked against the contracts that already exist
anchor: `keep their fields and add the missing ones`  (single member)
a1-r1/R1:F-05

### D6 WC-3 ask protocol is incomplete for commands with several gates
anchor: `ask the coordinator once with the preamble's `ask` command`  (single member)
a1-r1/R1:F-06

### D7 WC-10 leaves a hole between 4 and 5 minutes and cannot split Monitor-driven or fan-out waits
anchor: `must be split into waits of at most 4 minutes`  (members name the 4-5 minute gap and unsplittable waits)
a1-r1/R1:F-07, a1-r3/R1:10

### D8 WC-9 names no mechanism by which outward actions are authorized and checked
anchor: `any default that pushes, opens a PR, posts to GitHub`  (members name missing authorization mechanism or precedence for outward flags)
a1-r1/R1:F-08, a1-r3/R1:13

### D9 Fan-in of workers is specified for the success case only
anchor: `Orca keeps those records only for workers the coordinator starts`  (single member)
a1-r2/R1:F1

### D10 A stale contract from an earlier attempt can be read as the current result
anchor: `Orca does not check the file, so the coordinator opens it.`  (single member)
a1-r2/R1:F5, a1-r3/R1:3

### D11 The --unattended switch has no token rule, so quoted text can switch gates off
anchor: `cannot misfire on a person`  (members name the flag inside quoted or pasted text)
a1-r2/R1:F6, a1-r3/R1:11

### D12 AC-1.1/AC-1.2 demand a contract section for /sc:load, which the spec exempts
anchor: `every command in sections 3.1-3.2 has a `## Unattended mode` section`  (all members name /sc:load as exempt by its row and Decision but required by the universal acceptance check)
a1-r2/R1:F7, a1-r3/R1:1, a2-r1/R1:B-2, a2-r2/R1:B1, a2-r4/R1:B-1, a2-r6/R1:F-01, a3-r1/R1:F2, a3-r3/R1:F1, a3-r4/R1:F-01, a3-r6/R1:REQ-2, a2-r3/AUD:REQ-1, a2-r5/AUD:F-1, a3-r2/AUD:F-02, a3-r2/AUD2:B-1

### D13 The spec never says how the worker starts the command, and AC-0.4 does not check the skill loaded
anchor: `The worker runs the command directly in its own session`  (single member)
a1-r3/R1:5

### D14 No version or capability check before dispatch for older installs or section-4 commands
anchor: `split into 10 ready today, 27 needing a change and 6 coordinator-only`  (single member)
a1-r3/R1:6

### D15 No rule that --unattended is passed to nested skills and commands
anchor: `the command never calls `AskUserQuestion``  (single member)
a1-r3/R1:7

### D16 AC-C5/AC-0.3 grep cannot detect a deleted markdown bullet, so 'additive' is not proved
anchor: `prints nothing: edits are additive`  (members name the '^-[^-]' pattern failing on '-- ' lines)
a1-r3/R1:8, a3-r5/R1:F-3, a3-r4/AUD2:B-01

### D17 WC-5 treats only a missing report as failure; empty, unparseable or out-of-set contracts are unspecified
anchor: ``--outcome failed` when the report says `failed` or `blocked`, or no report exists`  (single member)
a1-r3/R1:12

### D18 WC-2 lists default, flag and blocked with no precedence, and one blocked_question for several gates
anchor: `Each gate resolves one of three ways`  (single member)
a1-r3/R1:14

### D19 AC-0.4 requires a contract that Phase 0 cannot yet produce
anchor: `step 4 uses the command's existing report file, since the contract arrives in P1`  (all members say step 3 of the live check needs the WC-4 contract while P0 makes no command edits)
a2-r1/R1:B-1, a2-r5/R1:B-2, a3-r1/R1:F1, a3-r3/R1:F3, a3-r5/R1:F-2, a2-r2/AUD:F-02, a3-r2/AUD:F-01

### D20 Ready commands with no small fix get no section or contract yet P1/AC-1.1/WC-4 expect one
anchor: `The only command changes are the small fixes in the last column.`  (members name brainstorm, init-lite, cleanup-audit, index-repo or adversarial: ready rows that gain nothing but are counted by the universal check)
a3-r3/R1:F2, a3-r4/R1:F-01, a3-r6/R1:REQ-2, a2-r5/AUD:F-1, a3-r2/AUD2:B-1

### D21 cli-portify can only end blocked under --unattended, yet AC-2.3 requires a succeeded happy path
anchor: `each of the three approval gates resolves as blocked with the artifact to review named in the contract`  (single member: no default or approval flag exists for the cli-portify gates)
a2-r4/AUD:F-3

### D22 AC-2.2 requires status blocked for P2 commands whose gates resolve by default or flag
anchor: `contract `status: blocked` with a non-empty `blocked_question``  (single member: AC-2.2 asserts blocked for each P2 command)
a3-r4/AUD:A-01

## Revision-introduced

- a3-r6/AUD F-01: `the contract is the sibling `<file>.return-contract.yaml``
- a3-r6/AUD2 B2: `gain none (REQ-2)`
