review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R3 |
| L2 | open | yes | single | CRITICAL | - | R3 |
| L3 | open | yes | overlap | MAJOR | - | R3, R1 |
| L4 | open | no | single | MAJOR | ARG-1, LA-1, LA-7 | R3 |
| L5 | open | no | overlap | MAJOR | - | R3, R1, R2 |
| L6 | open | no | single | MINOR | ST-8 | R3 |
| L7 | open | no | single | MAJOR | - | R3 |
| L8 | open | yes | single | MAJOR | - | R1 |
| L9 | open | yes | single | MAJOR | FO-18 | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: No task copies the brainstorm folder, it is absent on disk, so the Task 8 folder-exists acceptance criterion cannot pass as written.
- anchor: "already copied into this repository and part of the change"

### L2

#### L2.t2b-1 (F2)

- claim: Task 3 states every claim launches one agent, contradicting source §1 and Task 9, which state --pipeline none launches no agent.
- anchor: "Rewrite the claim bullet and the Will list so a claim now also creates or reuses the worktree and launches one agent at the chosen level and never merges."
- anchor2: "`none` creates the worktree and launches no agent"

#### L2.t2b-1 (F3)

- claim: Task 3 states every claim produces launch-prompt.md, contradicting source §10 and Task 7, which produce it only when the pipeline is not none.
- anchor: "the Outputs table (claim also produces `launch-prompt.md` and `worktree.json`)"

### L3

#### L3.t2b-1 (F4)

- claim: The no-create-call rule is stated for the after-create list too, but the create call has already happened by then.
- anchor: "otherwise `failed` with `W-ORCA-LIST-FAILED` and no create call"
- anchor2: "including the after-create list"

#### L3.t2b-1 (F7)

- claim: The command list reads as execution order with fetch and verification before the list, while source §8.3 makes them no-hit-path steps after lookup.
- anchor: "`git fetch origin`; `git rev-parse --verify origin/<B>`; `orca worktree list"

#### L3.t3-1 (F2)

- claim: The required create command omits --agent, but project instructions say a hook blocks Orca worktree creation without that flag, so the planned worktree creation fails.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

### L8

#### L8.t3-1 (F1)

- claim: The source-only constraint contradicts Tasks 8 and 9, which require edits outside src/superclaude, so the plan cannot satisfy both its constraint and its acceptance criteria.
- anchor: "Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`."
- anchor2: "Edit `docs/designs/sc-issue-command.md`."

### L9

#### L9.t4-1 (F1)

- claim: The required create call omits --agent, but the repository's hook blocks orca worktree create without --agent, so the call cannot create the worktree.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

## Other findings

- L4 (MAJOR, open, single): Source test IDs LA-7 (no launch for a failed worktree) and ARG-1 (bad arguments of every subcommand exit 2) have no task or acceptance criterion.
- L5 (MAJOR, open, overlap): Task 6 omits the source hand-command note (a hand-started agent is not governed) and the timeout check-Orca detail.
- L6 (MINOR, open, single): ST-8 wording says only the submit block contains the tokens and also that the worktree block contains them.
- L7 (MAJOR, open, single): Task 7 never states the contract value rules: launch_status not_requested for none and failed worktree, and null fields on STOP.

## Reviser brief

Blocking finding ids: L1, L2, L3, L8, L9.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
