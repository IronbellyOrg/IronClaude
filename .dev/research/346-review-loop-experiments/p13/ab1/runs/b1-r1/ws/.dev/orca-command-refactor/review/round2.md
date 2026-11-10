review: 2 of 3
# Merged review 2 (coordinator script; panel of 1 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r1/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 580d426a8d5991f96e6cdea92888313791bc19a8611b41a4726d4705e38301b7
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r1/ws/.dev/orca-command-refactor/review/round2-t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | regressed | yes | overlap | CRITICAL | 2.1, 2.3, 3, 3.1, 3.2, 6, 7.2, AC-0.4, AC-1.1, AC-1.2, P0, P1, P2, P4, SA-2, WC-11, WC-4, WC-9 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | regressed | yes | overlap | CRITICAL | 2.3, 3.1, 4, AC-2, AC-2.2, SA-3, WC-2, WC-3, WC-4, WC-5, WC-6 | t1b-1, t2-1, t3-1, t3-2 |
| L3 | open | no | single | MAJOR | AC-4.3, WC-10 | t1b-1 |
| L4 | open | no | overlap | MAJOR | 3.2, AC-4.3, WC-10 | t1b-1, t3-2 |
| L5 | open | no | overlap | MAJOR | 3.2, WC-7 | t1b-1, t3-2 |
| L6 | open | no | single | MINOR | - | t1b-1 |
| L7 | open | no | overlap | MAJOR | 1.4, WC-7 | t1b-1, t3-2 |
| L8 | open | no | single | MINOR | WC-1 | t1b-1 |
| L9 | regressed | yes | overlap | MAJOR | SA-2, WC-8 | t1b-1, t2-1, t3-2 |
| L10 | resolved | yes | single | MAJOR | AC-1.1, WC-4, WC-5 | t2-1 |
| L11 | open | no | overlap | MAJOR | SA-6, WC-9 | t2-1, t3-1 |
| L12 | open | no | overlap | MAJOR | - | t2-1, t3-1 |
| L13 | open | no | single | MAJOR | SA-1 | t3-1 |
| L14 | open | no | single | MINOR | - | t3-1 |
| L15 | open | no | single | MAJOR | 3.2, AC-2.2, AC-2.4, P2, WC-2, WC-9 | t3-2 |
| L16 | open | no | single | MAJOR | 1.3 | t3-2 |
| L17 | open | no | single | MAJOR | 3.1, WC-4 | t1b-1 |
| L18 | open | no | single | MINOR | 2.3, WC-11 | t1b-1 |
| L19 | open | no | single | MINOR | 4 | t1b-1 |
| L20 | open | no | single | MINOR | 3.2, P1 | t1b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (N1)

- claim: AC-1.2 and the P1 scope run the live check with --unattended on load, which gets no flag or contract, so the P1 gate cannot pass.
- anchor: "7.2 live check on each P1 command with `--unattended --output <dir>`"
- anchor2: "so it gets no flag, section or contract and WC-4 and WC-5 never apply to it"

#### L1.t1b-1 (M2)

- claim: spec-panel has a file-valued --output and its own --report-dir contract that WC-4 does not cover.
- anchor: "where the output flag takes a file (tdd, init-lite)"

#### L1.t1b-1 (M3)

- claim: post-release reads blocked and failed for a missing --output.
- anchor: "If the required output path is missing the command writes nothing and the worker ends `failed`."
- anchor2: "require an explicit `--output` and an explicit pre-tag choice, else blocked"

#### L1.t1b-1 (M5)

- claim: Existing contract status values are unchecked and brainstorm has no mapping fix.
- anchor: "the existing value sets were not read: UNVERIFIED"

#### L1.t1b-1 (M8)

- claim: Most blocked rows name no answer flag.
- anchor: "carries the answer as the flag the section 3 row names"

### L2

#### L2.t1b-1 (M4)

- claim: troubleshoot has no brief-named output path for fresh-dir re-runs.
- anchor: "writes into the output path the brief names"

### L9

#### L9.t1b-1 (M10)

- claim: AC-C1 exempts whole files while SA-2 allows only an Orca section.
- anchor: "--exclude=WORKER-CONTRACT.md --exclude=HOW-WE-WORK.md"

## Other findings

- L3 (MAJOR, open, single): A 4 to 5 minute call is allowed by WC-10 and fails AC-4.3.
- L4 (MAJOR, open, overlap): The pr-submit wait reading differs from the inventories and D3(b) names a wait change the row says may be unneeded.
- L5 (MAJOR, open, overlap): The nesting claim for tasklist has no layer count.
- L6 (MINOR, open, single): The re-read and validator claims cannot be reproduced from the workspace.
- L7 (MAJOR, open, overlap): E3 and 1.4(1) use the same evidence for opposite points.
- L8 (MINOR, open, single): WC-1 gives no number, no delivering phase and no check.
- L11 (MAJOR, open, overlap): Unattended reflect may auto-accept remediation that edits code, and the spec does not say the brief must authorize it; the headless trigger also changes from claude --print to a flag.
- L12 (MAJOR, open, overlap): The tasklist nesting claim rests on an UNVERIFIED docs citation and is stated as settled.
- L13 (MAJOR, open, single): The spec never names the safety flags, so an implementer cannot decide whether a given cli-eval brief passes or blocks.
- L14 (MINOR, open, single): The inventory quote of EVIDENCE.md:45 records only the ready state, so the 'answered' claim in E2 is not supported by the quoted evidence.
- L15 (MAJOR, open, single): The safety flags are not defined anywhere in the spec, so the cli-eval run gate cannot be implemented or tested as written.
- L16 (MAJOR, open, single): R1 states as fact that a nested worker-start is refused, but UNVERIFIED item 5 says call-site enforcement was not traced, so the rejection rests on an unchecked claim.
- L17 (MAJOR, open, single): The workflow contract path is stated two ways.
- L18 (MINOR, open, single): The one-worker-at-a-time duty is not in the coordinator brief list.
- L19 (MINOR, open, single): Behavior of --unattended on a coordinator-only command is undefined.
- L20 (MINOR, open, single): P1 text omits the flag refusals its rows schedule.

## Reviser brief

Blocking finding ids: L1, L2, L9.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
