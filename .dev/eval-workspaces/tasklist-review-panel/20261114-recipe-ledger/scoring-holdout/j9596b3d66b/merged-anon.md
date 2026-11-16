review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 e54e890380e234377e77d17b785d8ad7940fdadc69528f488b0c06b0ff5964f4
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | yes | single | MAJOR | - | R2 |
| L8 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 14 creates the master worktree without --agent, which the project hook blocks, so the master comparison cannot run as written.
- anchor: "(`orca worktree create --name issue302-master-check --base-branch origin/master`; never a raw `git worktree add`)"

#### L1.t3-1 (F2)

- claim: The prescribed Orca worktree command omits the required `--agent` flag and is blocked, preventing the required master comparison when a test failure needs validation.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

#### L1.t4-1 (ORCA-AGENT)

- claim: When a failure must be checked against master, the prescribed Orca command is blocked because it omits the required --agent option.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

### L7

#### L7.t3-1 (F1)

- claim: The plan both requires every gh api path to be repository-qualified and requires the worker to call the unqualified `gh api user` endpoint, so the requirements cannot both be met.
- anchor: "every `gh api` path spells `repos/<owner>/<repo>/...`"
- anchor2: "runs `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login`"

## Other findings

- L2 (MAJOR, open, single): Candidate lets live checks end pending as a valid result, weakening source section 20 acceptance criteria 5, 7 and 9.
- L3 (MAJOR, open, single): Default D22 (summary on every claim; analysis only when out of date) appears nowhere in the candidate.
- L4 (MAJOR, open, single): Candidate drops B5 (templates start from GFxAI ISSUE_TEMPLATE files) and only cites the heading list.
- L5 (MINOR, open, single): Acceptance allows edits in section 4.2, wider than the source sections 4.1 and 4.3.
- L6 (MINOR, open, single): First-page test is self-referential: it checks the request against the docstring, not the API value.
- L8 (MAJOR, open, single): This instruction can leave the no-write closed-issue check and next-step-content check pending even though neither requires approval for a GitHub write.

## Reviser brief

Blocking finding ids: L1, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
