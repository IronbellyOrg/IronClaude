review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 e54e890380e234377e77d17b785d8ad7940fdadc69528f488b0c06b0ff5964f4
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R3, R1 |
| L2 | open | yes | overlap | CRITICAL | - | R1, R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Overbroad --repo scope conflicts with source gh api user and auth commands that take no --repo; shipped refs must keep those lines without --repo.
- anchor: "every `gh` command passes `--repo IronbellyOrg/IronClaude`"
- anchor2: "the gh commands exactly as written there (each with `--repo <R>`)"

#### L1.t3-1 (F1)

- claim: The skill cannot run the required `gh auth status` preflight with `--repo`, because that command does not accept the flag.
- anchor: "every `gh` command passes `--repo IronbellyOrg/IronClaude`"
- anchor2: "the orchestrator is the only place that writes to GitHub or ClickUp, and every `gh` call carries `--repo <R>`"

### L2

#### L2.t3-1 (F2)

- claim: Orca blocks the prescribed temporary-worktree command because it omits the required `--agent` flag, preventing the master comparison task from completing.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

#### L2.t4-1 (F1)

- claim: Task 14's worktree creation command omits the required --agent option, so the project hook blocks the master comparison needed to classify pre-existing test failures.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

## Other findings

none.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
