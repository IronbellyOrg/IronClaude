review: 1 of 3
# Merged review 1 (coordinator script; panel of 1 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/offline/replay/k1/a3-r5/round1-t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | AC-0.4, AC-1.1, P0, P1, WC-2, WC-4, WC-9 | t1b-1 |
| L2 | open | yes | single | MAJOR | AC-0.3 | t1b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F-1)

- claim: P1 adds the flag to commands whose gates and outward defaults are still on until later phases.
- anchor: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"
- anchor2: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"

#### L1.t1b-1 (F-2)

- claim: AC-0.4 requires a WC-4 contract for P0 smoke runs that have no command edits.
- anchor: "its report path is the WC-4 contract path"
- anchor2: "step 4 uses the command's existing report file, since the contract arrives in P1"

### L2

#### L2.t1b-1 (F-3)

- claim: The additive-edit check does not detect a deleted bullet.
- anchor: "grep -E '^-[^-]'"

## Other findings

none.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
