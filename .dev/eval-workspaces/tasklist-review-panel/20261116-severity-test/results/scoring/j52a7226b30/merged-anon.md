review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | FO-12 | R1 |
| L3 | open | no | single | MAJOR | ARG-1 | R1 |
| L4 | open | no | single | MAJOR | LA-1, LA-6, LA-7, ST-9 | R1 |
| L5 | open | yes | overlap | MAJOR | - | R1, R3 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | single | MAJOR | FO-11 | R1 |
| L8 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L5

#### L5.t2b-1 (F5)

- claim: Candidate omits source detail that on timeout an agent may have started and detail must say to check Orca before re-running.
- anchor: "a nonzero exit, timeout or `ok` not true removes the launch record, returns `failed` with `W-LAUNCH-FAILED`, the first stderr line and a `hand_command`"

#### L5.t2b-1 (F8)

- claim: Candidate omits source hand_command note that a hand-started agent is not governed by the hook and re-running the claim is preferred.
- anchor: "the first stderr line and a `hand_command` (the same call without the marker)"

#### L5.t2b-1 (F9)

- claim: Candidate omits source rule that the temporary name must not match the nonce pattern, so a half-written record could be visible.
- anchor: "written to a temporary name and renamed to the nonce"

#### L5.t3-1 (F1)

- claim: An implementer who follows the stated text as written builds a failure response that offers an unmarked launch command without warning that it bypasses launch-level enforcement, and that is wrong because the agent can run without the hook enforcing its selected level.
- anchor: "a `hand_command` (the same call without the marker)"

## Other findings

- L1 (MAJOR, open, single): For tracked/.prev files on created/reused, warning cannot both hold only the status code and hold W-WORKTREE-COPY-FAILED; implementer must guess which rule wins.
- L2 (MAJOR, open, single): After-create list already follows a create call, so 'no create call' cannot hold for that case; implementer must guess it applies only to the initial list.
- L3 (MAJOR, open, single): Candidate requires exit 2 only at preflight stage and for --submit with worktree; no acceptance requires ARG-1 for worktree/prompt/launch subcommands.
- L4 (MAJOR, open, single): Candidate LA-1 to LA-6 acceptance omits LA-7 script-level pin; skill-side Wave 8 guard alone does not pin launch subcommand behaviour for a failed record.
- L6 (MINOR, open, single): Source also requires SKILL.md description update; candidate does not name it, so description may stay stale.
- L7 (MAJOR, open, single): Outcome for one new row with non-matching basename, and whether 'two or more' counts total or matching rows, is unspecified; implementer must guess.
- L8 (MAJOR, open, single): The goal implies every pipeline level launches an agent, while later requirements say `none` launches no agent; the detailed tasks clarify the behavior, so this is a non-blocking ambiguity.

## Reviser brief

Blocking finding ids: L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
