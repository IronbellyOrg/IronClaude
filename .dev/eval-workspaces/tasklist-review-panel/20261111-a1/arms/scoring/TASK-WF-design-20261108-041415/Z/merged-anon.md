review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MINOR | - | R2 |

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

#### L1.R2 (F1)

- claim: The design doc the plan yields keeps the claim-mode `gh api user -q .login` lookup (line 157, untouched by every task), so this acceptance criterion can never pass: `user` is a gh api path that spells neither `repos/<R>/...` nor the one allowed orgs read.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "at the places listed by grep for \"label\" (around lines 18, 76, 77, 197, 207, 224, 225, 283 to 293, 354, 366, 370, 449, 479 and 492)"

#### L1.R2 (F2)

- claim: The constraint counts two writes to the created issue while the Goal and Tasks 1, 2, 4 and 6 also apply the mode label via `--label`, a third write; only the charitable reading (two new classification writes) keeps the document consistent.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R2 (F3)

- claim: No reason value is defined for a failed repo-label lookup: the label output line's only reason is `label missing in repo`, so a failed `gh label list` is misreported as a missing label instead of an unknown state.
- anchor: "`labels.md` contains the three exact line formats `not applied: label missing in repo: <name>`, `not set: issue type <name>: <reason>` and `not set: field Complexity <value>: <reason>`"
- anchor2: "a failed lookup is recorded as `lookup failed: <reason>` and never stops the run"

#### L1.R2 (F4)

- claim: Commit `1aa2e5c3` does not exist in this repository's history, so the cited analysis base is unverifiable; the re-read rule keeps it advisory.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.R3 (F1)

- claim: Task 10's third acceptance criterion cannot pass because the design doc's untouched claim-mode line `gh api user -q .login` is a gh api path that spells neither repos/<R>/... nor the one allowed orgs/ read, and no task permits editing it.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L1.R3 (F2)

- claim: The plan never states that the field read-back's value is a numeric option id compared via single_select_option.name, a rule the shipped labels.md section and its test pin, so an implementer without source.md may compare the numeric value and misreport the field as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R3 (F3)

- claim: The kept maintainer-block lines carry --repo <owner/repo>, not --repo <R> as the constraint demands; harmless because the fork-safety scanner accepts an explicit repo placeholder.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R3 (F4)

- claim: Task 12 writes artifacts under the package's artifacts directory, which the edit-scope constraint's four trees do not name; resolved only by the phrase 'in this package'.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MINOR, open, single): The kept depth-rule text stays lowercase (simple, medium, complex) beside the capitalized option values; harmless because option matching is case-insensitive.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
