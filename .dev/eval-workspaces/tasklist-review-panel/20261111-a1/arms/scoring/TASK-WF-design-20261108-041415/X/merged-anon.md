review: 1 of 3
# Merged review 1 (coordinator script; panel of 1 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Task 10's acceptance line forbids every gh api path except repos/<R>/... and the one orgs/ read, but the design doc keeps the unchanged claim lookup `gh api user -q .login` (line 157), so the check cannot pass without falsifying the doc; Task 2 states the correct rule (user or repos/<R>/...).
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.R1 (F2)

- claim: tests/skills/test_worker_contract.py classifies every gh api/gh pr line by file and exact text, so the plan's edits to those lines in SKILL.md, create.md, labels.md and the T3 worker leave stale and unclassified entries; no task updates it and Task 12 runs only test_issue_protocol.py.
- anchor: "`make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source"
- anchor2: "Search the file for any other assertion on the old label wording"

#### L1.R1 (F3)

- claim: The candidate gives only key names for the third block, so it is unclear whether label-missing lines belong in classification_missing.
- anchor: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"
- anchor2: "lists every classification it could not set in its final output and in a third return-contract block."

#### L1.R1 (F4)

- claim: The constraint says two writes besides the issue, but Wave 5 also posts a pushback comment and the create call carries a mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F5)

- claim: Read literally, the edit allow-list excludes the package artifacts folder that Task 12 must write to.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F6)

- claim: Task 3 adds the Complexity-only write limit to the skill's Will Not list, but Task 6's command wording omits it, so the stated agreement does not hold.
- anchor: "The Will and Will Not lists agree with the skill's Will and Will Not lists on the new create behaviour."
- anchor2: "never writes a field other than Complexity"

#### L1.R1 (F7)

- claim: The unverified list omits the issueType and field-values read-backs and any minimum gh version; a gh without --type would fail the create with E-CREATE-FAILED instead of a non-fatal not-set line.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4 (POST body, `--type` flag, silent drop without push access)"
- anchor2: "read-back with `gh issue view <N> --repo <R> --json issueType --jq .issueType.name`"

## Other findings

none.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
