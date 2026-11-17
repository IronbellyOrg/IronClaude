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
| L1 | open | no | single | MAJOR | FO-18 | R2 |
| L2 | open | no | single | MAJOR | LA-6, LA-7 | R2 |
| L3 | open | no | single | MINOR | ARG-1 | R2 |
| L4 | open | no | overlap | MAJOR | - | R2, R1 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | yes | overlap | MAJOR | PR-1, PR-4 | R3, R1 |
| L7 | open | no | single | MAJOR | - | R3 |
| L8 | open | yes | single | MAJOR | - | R1 |

## Blocking findings

### L6

#### L6.t3-1 (F1)

- claim: The prompt-rendering instruction requires common plus the selected level block, but its acceptance criterion says to keep only the level block, so the specified test and renderer cannot both meet the plan.
- anchor: "`worktree` and `full` keep only their own block"
- anchor2: "keeps `common` plus the level block"

#### L6.t4-1 (F3)

- claim: The prompt implementation requires the common block, but the acceptance criterion can be read as requiring only the selected level block.
- anchor: "`prompt --template <path> --level worktree|full [--submit] --number <N> --out <file>` keeps `common` plus the level block"
- anchor2: "`uv run pytest tests/skills/test_issue_orca_worktree.py -k prompt` passes with PR-1 to PR-4 (levels keep only their own block,"

### L8

#### L8.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a worktree step that Orca blocks because the command omits the required --agent flag.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

## Other findings

- L1 (MAJOR, open, single): Task2 says no forbidden flag appears in any recorded orca call while Task6 requires --agent/--prompt/--surface in launch; implementer must guess the list/create scope.
- L2 (MAJOR, open, single): No acceptance requires LA-7 test: no launch call for a failed worktree record and no pending record for none.
- L3 (MINOR, open, single): Bad-argument exit 2 is only pinned for preflight; no acceptance pins ARG-1 for worktree, prompt and launch.
- L4 (MAJOR, open, overlap): Design requires hand-command note that hand-started agent is not governed and timeout detail to check Orca; candidate omits both texts.
- L5 (MINOR, open, single): Candidate omits the six default chains result for <K> (features, bug chains step 1); rule itself is carried so impact is illustrative only.
- L7 (MAJOR, open, single): The plan does not require a test that invalid flag combinations cause no GitHub or Orca calls, as required by the driving design.

## Reviser brief

Blocking finding ids: L6, L8.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
