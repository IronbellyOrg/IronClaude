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
| L1 | open | no | overlap | MAJOR | - | R3, R2 |
| L2 | open | no | overlap | MAJOR | - | R3, R2 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | yes | overlap | MAJOR | - | R3, R1, R2 |
| L5 | open | no | single | MINOR | ARG-1, LA-1 | R3 |
| L6 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L4

#### L4.t2b-1 (F4)

- claim: Worse reading applies record-reuse after create, contradicting set-difference and no-create-call text.
- anchor: "including the after-create list: a `worktree.json` record in the source directory"

#### L4.t3-1 (F1)

- claim: The specified create call omits the required --agent flag, so the repository’s Orca enforcement rejects worktree creation.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

#### L4.t4-1 (F1)

- claim: The plan requires an exact worktree-create call without `--agent`, but the repository Orca guard rejects create calls without that flag, so the planned worktree step cannot run.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent"
- anchor2: "`--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call."

## Other findings

- L1 (MAJOR, open, overlap): Template built from candidate lacks required started-by statement, weakening launched-agent context.
- L2 (MAJOR, open, overlap): Launch-failure detail omits check-Orca warning and hand-command governance note from design.
- L3 (MAJOR, open, single): Contract list omits not_requested for none/failed and null-on-STOP semantics.
- L5 (MINOR, open, single): ARG-1 not explicitly pinned for worktree, prompt and launch subcommands.
- L6 (MAJOR, open, single): The plan does not carry the driving document’s owner follow-up to run the observed post-merge checks on test issues.

## Reviser brief

Blocking finding ids: L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
