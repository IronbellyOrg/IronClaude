review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R2 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | ARG-1, LA-6, LA-7 | R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MINOR | ST-8 | R2 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MINOR | - | R2 |
| L8 | open | no | single | MAJOR | - | R2 |
| L9 | open | yes | single | MAJOR | FO-18 | R3 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: No task copies the brainstorm folder that Task 8 acceptance requires to exist with five contents; on disk it does not exist.
- anchor: "already copied into this repository and part of the change"

#### L1.t2b-1 (F9)

- claim: The file is absent from this checkout, so section-number lookups depend on source.md rather than the named path; no acceptance checks the file itself.
- anchor: "Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it)."

### L9

#### L9.t3-1 (F1)

- claim: The prescribed worktree-create call omits required --agent, so the repository hook blocks real worktree creation even though the fake-orca test can pass.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

## Other findings

- L2 (MAJOR, open, single): Rule puts W-ORIGIN-BASE-STALE and W-WORKTREE-COPY-FAILED in detail on created/reused, but source requires them in worktree_warning.
- L3 (MAJOR, open, single): Task 6 acceptance drops test ids LA-7 and ARG-1 (bad arguments of every subcommand exit 2), so a plan-faithful build can ship them untested.
- L4 (MAJOR, open, single): Source requires the temporary name to not match the 32-hex nonce pattern; the candidate omits that guard, so a half-written record could be visible to the hook.
- L5 (MINOR, open, single): ST-8 wording says only submit contains the tokens and only worktree also contains them; both cannot be literal, read worktree as the permitted prohibition exception.
- L6 (MINOR, open, single): Rendered full with --submit does contain the tokens via the submit block; the pin only holds for the no-submit render, which the text never says.
- L7 (MINOR, open, single): The no-create-call clause is stated for the after-create list too, where a create call already ran; read it as no further create.
- L8 (MAJOR, open, single): Field list is carried but the not_requested-for-none/failed and null-on-STOP mapping never reaches the SKILL.md task text.

## Reviser brief

Blocking finding ids: L1, L9.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
