review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R5: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3, R4 |
| L2 | open | no | overlap | MAJOR | - | R2, R4 |

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

- claim: The Task 8 tests are the only enforcement of several Task 1-6 rules and no stated gate fails when Task 8 is under-delivered, because Task 12 only requires the test file to pass, which fewer collected tests still do.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red: each new test asserts on the text that task adds."

#### L1.R2 (F2)

- claim: Two allowed spellings of the single orgs/ read appear across tasks; the pinned regex accepts both, so nothing fails today but the looser spelling is a latent divergence.
- anchor: "equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields`"
- anchor2: "the T3 worker also runs `gh api repos/<R>/issue-types` and `gh api orgs/<owner of R>/issue-fields`"

#### L1.R2 (F4)

- claim: verify-sync exits non-zero in a fresh clone until sync-dev runs; the task's own step order already sequences sync-dev first, so this is a sequencing note only.
- anchor: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

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

#### L1.R4 (F1)

- claim: The write limit allows two writes to a created issue, but Task 2 requires a pushback comment on that issue, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R4 (F2)

- claim: Task 12 runs only the protocol test file, so other suites that quote SKILL.md text can break unnoticed.
- anchor: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R4 (F3)

- claim: Several tasks describe a before-state that the checkout already has, so applying their add or replace text literally can duplicate content.
- anchor: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"

#### L1.R4 (F4)

- claim: The orgs scanner is never named or specified, and one already exists in the test file, so the self-check can target the wrong or a duplicate scanner.
- anchor: "Add one self-check test in the style of `test_fork_safety_scan_fails_on_a_ref_without_repo` (line 642) that feeds the `orgs/` scanner"

#### L1.R4 (F6)

- claim: The artifact path is ambiguous between the package folder and the project-root artifacts folder, which the edit limit does not cover.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.R4 (F7)

- claim: The cited line numbers are stale; the tests sit near lines 545 and 586.
- anchor: "`test_skill_will_and_will_not_match_the_command_file`, line 527"

## Other findings

- L2 (MAJOR, open, overlap): The AC's pytest selector is descriptive rather than exact test ids; it currently selects 38 tests including every fork-safety parametrization over the ref files, which covers the intent.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
