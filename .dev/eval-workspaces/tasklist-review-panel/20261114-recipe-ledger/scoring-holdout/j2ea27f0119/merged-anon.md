review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R1 |
| L2 | open | yes | overlap | CRITICAL | - | R1, R2 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | yes | single | CRITICAL | FO-18 | R3 |
| L7 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The STOP order contradicts itself: the listed order puts the claim-only check first while the final sentence requires the create-only check to win.
- anchor: "Add three STOP rules after the existing ones and before Activation, in this order:"
- anchor2: "`E-CREATE-ONLY-FLAG` for `--depth`, `--mode`, `--type` with `--claim` stays the first rule."

#### L1.t2b-1 (F3)

- claim: The frontmatter description still says the claim stops and no task rewrites it, so it stays false after the change.
- anchor: "Rewrite the claim bullet and the Will list so a claim now also creates or reuses the worktree"

### L2

#### L2.t2b-1 (F2)

- claim: Banning the agent flags in every recorded call contradicts the launch call, which must carry them, so the wider scope cannot pass once the launch exists.
- anchor: "`--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--setup`, `--branch`, `--activate`, `--run-hooks`) appears in any recorded `orca` call."
- anchor2: "`orca agent launch --agent claude --worktree path:<wt> --surface terminal"

#### L2.t2b-1 (F5)

- claim: The grep checks for literal strings, not for executed commands, so it cannot prove the claim it is meant to enforce.
- anchor: "finds no executed command."

#### L2.t4-1 (F1)

- claim: An implementer following this failure text can remove the level record and retry after a timeout without checking whether an agent started; that can leave a running agent without its hook record or start a duplicate, contrary to the required timeout check.
- anchor: "a nonzero exit, timeout or `ok` not true removes the launch record, returns `failed` with `W-LAUNCH-FAILED`, the first stderr line and a `hand_command`"

### L6

#### L6.t3-1 (F1)

- claim: An implementer who follows the stated text as written builds an Orca create call without `--agent`, which the repository's required hook blocks; the exact-argv acceptance check also forbids changing that call.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

## Other findings

- L3 (MINOR, open, single): The older design acceptance text still says the command stops and Task 8 does not update it.
- L4 (MINOR, open, single): The grep returns many pre-existing hits, so by itself it cannot show which hit, if any, this change introduced.
- L5 (MINOR, open, single): The tree tracks a second file under `.claude/`, so the parenthetical statement about what is tracked is false.
- L7 (MAJOR, open, single): The plan lists the return fields but omits the specified values for skipped launches and fields that do not apply after a STOP, leaving the contract under-specified.

## Reviser brief

Blocking finding ids: L1, L2, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
