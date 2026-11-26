review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3, R4 |
| L2 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: The exactly-two-writes constraint forbids the mode label application and pushback comment that the Goal and Wave 5 require, so one stated behaviour must be dropped.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`), no longer asks for `type:` or `complexity:` labels"

#### L1.R2 (F2)

- claim: The design doc's unchanged claim lookup uses gh api user, which is neither repos/<R>/ nor the allowed orgs read, so Task 10's criterion cannot pass without breaking the claim-unchanged rule.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L1.R2 (F3)

- claim: Task 12 writes to ./artifacts/ without stating whether that is the package folder or the repo root, and the repo-root reading breaches the edit-only scope.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F4)

- claim: Keeping the maintainer gh label create lines verbatim leaves --repo <owner/repo> in place, breaching the --repo <R> rule, and the task does not direct the fix.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L1.R2 (F5)

- claim: The candidate defers reason lists and UNVERIFIED points to ./source.md, which is absent from the candidate package, so those acceptance criteria cannot be checked from the plan alone.
- anchor: "with every reason listed in specification 2.4"
- anchor2: "Source: ./source.md"

#### L1.R2 (F6)

- claim: For create.md the named formats are prefixes only, so a full-line equality test would fail against a create.md that follows Task 2.
- anchor: "`create.md` and `labels.md` carry the three exact line formats `not applied: label missing in repo:`, `not set: issue type` and `not set: field Complexity`"

#### L1.R3 (F1)

- claim: The distributive reading of this sentence produces a test asserting every skill and agent file contains the POST line, which fails against the plan's own correct output because workers and claim-side refs must not carry a field-write command.
- anchor: "Third, the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`."

#### L1.R3 (F2)

- claim: The constraint restricts placeholder forms to `<owner>` and `<R>` while Task 1 keeps maintainer lines using a third form `<owner/repo>`; no pinned test distinguishes them, so the tension is cosmetic.
- anchor: "use `<owner>` and `<R>`"
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R3 (F4)

- claim: Task 7's premise is stale in this checkout (the test already asserts 3 blocks at line 545) and several named line anchors shifted, but the plan's own re-read constraint makes every edit land correctly and the acceptance criteria still pass.
- anchor: "change `len(blocks) == 2` to 3"
- anchor2: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.R4 (F1)

- claim: The plan simultaneously forbids edits outside its listed directories and requires writing the owner-check artifact under an unlisted package artifacts directory.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F1)

- claim: No task updates tests/skills/test_worker_contract.py, which pins exact worker, SKILL.md and create.md write lines, so the planned edits leave it red while every stated check passes.
- anchor: "`make verify-sync` and `make lint` exit 0 and the whole `tests/skills/test_issue_protocol.py` file passes"
- anchor2: "Edit `tests/skills/test_issue_protocol.py`. Source section: 3.2"

#### L1.R1 (F2)

- claim: The constraint says exactly two writes besides the issue, but Task 2 also posts a pushback comment and applies the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F3)

- claim: The constraints list three reversible defaults while Task 12 asks the owner note to record four.
- anchor: "Decisions taken as defaults (the owner may reverse them later)"
- anchor2: "the four defaults the owner may reverse"

#### L1.R1 (F4)

- claim: A scanner that must accept a path with spaces and must not flag the bare prose mention of orgs/ is not specified, so a naive regex fails on the text Task 2 requires.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals `orgs/<owner of R>/issue-fields`"
- anchor2: "no other `orgs/` path"

## Other findings

- L2 (MINOR, open, single): The prescribed `--mode` row says the mode yields Feature or Bug, which is imprecise for `--mode feature --type tests` (Test); the adjacent `--type` row states the exception, so no user-visible behavior is wrong.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
