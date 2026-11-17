review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 e54e890380e234377e77d17b785d8ad7940fdadc69528f488b0c06b0ff5964f4
reviewers:
- R2: report <path>, block ok true
- R1: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MINOR | - | R2 |
| L2 | open | no | single | MINOR | - | R2 |
| L3 | open | no | single | MINOR | - | R2 |
| L4 | open | yes | overlap | MAJOR | - | R1, R3 |
| L5 | open | yes | single | MAJOR | - | R1 |
| L6 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L4

#### L4.t3-1 (F1)

- claim: An implementer who follows the stated text as written builds a baseline-comparison step that invokes Orca worktree creation without --agent, and that step is wrong because repository instructions block worktree creation unless --agent is supplied.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

#### L4.t4-1 (F1)

- claim: The prescribed worktree creation omits required --agent, so Orca blocks the master comparison when Task 14 needs it.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

### L5

#### L5.t3-1 (F2)

- claim: An implementer who follows the stated text as written builds incompatible requirements: all gh api paths must start with repos/<owner>/<repo>/, but the required `gh api user` lookup does not use a repository path, so the mandated prefix breaks the user lookup.
- anchor: "every `gh api` path spells `repos/<owner>/<repo>/...`"
- anchor2: "the gh commands exactly as written there"

## Other findings

- L1 (MINOR, open, single): Test checks source copies only rather than source section 16's installed-or-source wording; weaker drift check, product unaffected.
- L2 (MINOR, open, single): Plan leaves invalid page-cap behaviour to implementer choice; tests pin documented choice, so any choice passes.
- L3 (MINOR, open, single): Goal wording implies full passing while Task 14 permits recorded pre-existing failures; shorthand tension, operative acceptance is Task 14.
- L6 (MAJOR, open, single): The plan does not instruct the implementer to use the source document's named feature branch before editing and staging changes.

## Reviser brief

Blocking finding ids: L4, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
