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
| L1 | open | yes | overlap | CRITICAL | - | R3, R1, R2 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MINOR | - | R3 |
| L5 | open | no | single | MINOR | - | R3 |
| L6 | open | yes | single | MAJOR | - | R1 |
| L7 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The printed Orca create command has no --agent, so the installed hook blocks it and the required master-comparison evidence cannot be produced as written.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

#### L1.t3-1 (F1)

- claim: The command omits the required --agent flag, so the project hook blocks creation and Task 14 cannot complete as written.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

#### L1.t4-1 (F1)

- claim: If a test must be shown to fail on master, the specified Orca command omits required --agent and cannot create the comparison worktree.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

### L6

#### L6.t3-1 (F2)

- claim: The specified outputs are saved under project-root ./artifacts/, so git add .dev/tasks does not stage them and the staging criterion cannot pass.
- anchor: "git add .dev/tasks` has been run so this package and its `artifacts/` are staged; nothing is committed or pushed."

## Other findings

- L2 (MAJOR, open, single): Checking only the source copies lets a flag missing from the installed copy pass the test while the shipped primitive breaks.
- L3 (MAJOR, open, single): The plan can complete with five of the nine section 20 acceptance criteria still pending, so the feature is not fully proven against the source.
- L4 (MINOR, open, single): The Wave 4 worker writes more than one file but returns only one path; harmless because the paths are deterministic, flagged as wording only.
- L5 (MINOR, open, single): The test pins whatever behavior the implementer documented, so a script that crashes on a bad page-cap value cannot be caught by it.
- L7 (MAJOR, open, single): The plan does not clearly require or test the source-supported behavior that --create accepts @path as a description file.

## Reviser brief

Blocking finding ids: L1, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
