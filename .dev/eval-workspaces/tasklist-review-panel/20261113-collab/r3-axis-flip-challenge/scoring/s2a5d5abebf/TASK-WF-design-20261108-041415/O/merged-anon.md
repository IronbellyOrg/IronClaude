review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R3 |
| L4 | open | yes | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.R1 (f1)

- claim: Task 8 acceptance requires every Task 1 to 5 revert to redden a new test, but no listed new test asserts SKILL.md text, so reverting Task 3 stays green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

### L3

#### L3.R1 (f2)

- claim: Constraint counts only type and field writes, omitting the kept mode-label write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"

#### L3.R1 (f3)

- claim: Artefact path sits outside the stated edit-only trees; needs package-local qualifier.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L3.R3 (f1)

- claim: Running the required sync changes generated files under `.claude/`, violating the candidate's explicit prohibition on editing that directory.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L3.R3 (f4)

- claim: The required owner-check and test-log artifacts are outside the candidate's permitted edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L4

#### L4.R1 (f5)

- claim: Wave 5 text omits the option-not-found branch and the pushback STOP code the source requires.
- anchor: "replace the label step with the sequence of specification 2.1"

#### L4.R1 (f6)

- claim: Task 10 acceptance leaves only the repos form and one orgs read, but the live design doc requires gh api user and Task 2 allows user, so the check cannot pass without breaking the user call.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

## Other findings

- L2 (MAJOR, open, single): Plan names the three keys but never states read-back-or-null values or prefix stripping for classification_missing.
- L5 (MINOR, open, single): Stated line 329 is stale; live file has the phrase at line 333.
- L6 (MINOR, open, single): The candidate does not explicitly require skipping the field write and reporting `option not found` when the mapped Complexity option is absent.

## Reviser brief

Blocking finding ids: L1, L3, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
