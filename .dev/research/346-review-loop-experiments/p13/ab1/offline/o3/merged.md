review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/offline/o3/t1b-1.md, block ok true
- t2-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/offline/o3/t2-1.md, block ok true
- t3-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/offline/o3/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | AC-0.4, AC-1.1, AC-1.2, P0, P1, WC-4 | t1b-1, t2-1, t3-1 |
| L2 | open | yes | single | CRITICAL | AC-2.3, WC-4, WC-6 | t3-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: The P0 check demands a contract the same row says does not exist before P1.
- anchor: "its report path is the WC-4 contract path"
- anchor2: "step 4 uses the command's existing report file, since the contract arrives in P1"

#### L1.t1b-1 (F2)

- claim: The load row says no section and no report, but the P1 checks require both for load.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "use it as a step inside another worker's brief, not as its own Task"

#### L1.t2-1 (F1)

- claim: AC-1.1 and AC-1.2 require a report and a section for load, which the spec says gets neither.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "use it as a step inside another worker's brief, not as its own Task"

#### L1.t2-1 (F2)

- claim: Section 3.1 says ready commands change only by their small fix, but P1 adds the flag and a section to all of them.
- anchor: "The only command changes are the small fixes in the last column"
- anchor2: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"

#### L1.t2-1 (F3)

- claim: AC-0.4 step 3 needs a contract that P0 does not have.
- anchor: "its report path is the WC-4 contract path"
- anchor2: "step 4 uses the command's existing report file, since the contract arrives in P1"

#### L1.t3-1 (REQ-2)

- claim: AC-1.1 requires edits that the rows forbid or schedule for later phases.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"

### L2

#### L2.t3-1 (REQ-1)

- claim: The report-location rule cannot be applied to a dozen commands the spec lists.
- anchor: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"
- anchor2: "not a bare topic; `--output <file>` | the TDD at `--output`"

#### L2.t3-1 (ARCH-1)

- claim: WC-4 and WC-6 contradict on where a retry writes, so the coordinator reads a stale contract.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "the output directory, so the report path is known before dispatch (WC-4)"

## Other findings

none.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
