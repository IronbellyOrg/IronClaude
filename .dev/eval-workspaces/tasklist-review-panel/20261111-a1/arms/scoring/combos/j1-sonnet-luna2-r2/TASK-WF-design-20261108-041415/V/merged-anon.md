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
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | overlap | MAJOR | - | R1, R2, R3 |
| L5 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The plan rewrites at least nine `gh api` lines but never updates or runs tests/skills/test_worker_contract.py, whose exact-line table then fails as unclassified and stale.
- anchor: "`make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`"
- anchor2: "add the single `orgs/<owner of R>/issue-fields` read exception for the T3 worker"

#### L1.R1 (F3)

- claim: The command's Will Not lacks the no-other-field clause the skill gets, so the criterion that the two lists agree fails on a strict reading.
- anchor: "and the Will Not line (line 93) to also say it creates no issue types or issue fields."
- anchor2: "add that the skill never creates an issue type or an issue field and never writes a field other than Complexity"

#### L1.R1 (F8)

- claim: Wave 5 also applies a mode label and may post the pushback comment, so the count of two writes is inaccurate.
- anchor: "It writes exactly two things to a created issue besides the issue itself"

#### L1.R3 (F1)

- claim: The plan forbids edits under `.claude/` while requiring `make sync-dev`, which writes generated copies there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R2 (F1)

- claim: The plan requires a mode-label write while also saying the issue type and field are the only two writes besides issue creation.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R2 (F2)

- claim: The plan requires make sync-dev, which writes generated copies under .claude, while prohibiting edits there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

## Other findings

- L2 (MAJOR, open, single): The design doc keeps `gh api user -q .login` in its claim section, so a strict check of this criterion fails.
- L3 (MAJOR, open, single): Presence-only tests pass on a swapped depth mapping or a dropped reason, and no new test necessarily fails if Task 3 is reverted.
- L4 (MAJOR, open, overlap): The read-back never says to compare single_select_option.name for the field id, so comparing the value could report every successful Complexity write as not applied.
- L5 (MINOR, open, single): The plan does not say who writes the Issue type row or from which flags, so a worker's differing mode could set the wrong issue type.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
