review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | yes | overlap | CRITICAL | - | R1, R2 |
| L3 | open | no | single | MAJOR | 2.1, 3.4 | R1 |
| L4 | open | no | single | MINOR | 2.2 | R1 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L2

#### L2.R1 (F2)

- claim: Copied literally, the Task 3 span has no --repo and the existing gh_lines_missing_repo scan would fail on SKILL.md.
- anchor: "add the field POST and `gh issue create ... --type <name>` to the orchestrator's write list"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L2.R1 (F3)

- claim: The command Will Not line misses the skill's 'no field other than Complexity' item, so the Task 6 criterion that the two lists agree is not met as written.
- anchor: "and the Will Not line (line 93) to also say it creates no issue types or issue fields"
- anchor2: "add that the skill never creates an issue type or an issue field and never writes a field other than Complexity"

#### L2.R1 (F5)

- claim: The constraint says two writes, while Task 2 also applies the mode label and posts the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L2.R1 (F6)

- claim: The design doc keeps `gh api user -q .login` (line 157) and a prohibition naming the brace placeholder (line 334), so both statements are over-literal.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "No file may contain a brace placeholder for owner and repo"

#### L2.R1 (F8)

- claim: Task 12 writes package artifacts outside the listed edit paths, and its .claude status check is vacuous because that folder is gitignored.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

#### L2.R2 (F1)

- claim: Task 10 acceptance criterion omits the user path, so it cannot pass while the gh api user login lookup is kept.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception, the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields`"

#### L2.R2 (F2)

- claim: Edit-scope rule and Task 12 artifacts path point in different directions.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L1 (MAJOR, open, single): Read as an upper bound, the listed tests stay green if Task 3 (SKILL.md) is reverted, so the Task 8 criterion needs an extra SKILL.md assertion the plan does not state.
- L3 (MAJOR, open, single): The plan never says how to match the read-back row to the written option, so a naive value comparison could print a false 'not applied after create' after a successful write.
- L4 (MINOR, open, single): The goal says every unset classification goes in the third block, but a missing mode label is reported only in labels_missing in the first block.
- L5 (MINOR, open, single): Read-only ban wording drops the --method form from the stated check.
- L6 (MINOR, open, single): Read-back comparison against option names is never stated.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
