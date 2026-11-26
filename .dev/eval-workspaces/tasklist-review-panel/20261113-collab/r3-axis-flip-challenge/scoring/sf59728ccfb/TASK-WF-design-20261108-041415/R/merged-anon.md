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
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L2

#### L2.R1 (f1)

- claim: Task 7 and Task 8 cite test line numbers 492, 527 and 642, but the named tests are at live lines 545, 580 and 695, so line-number navigation lands on unrelated tests.
- anchor: "In `test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` (around lines 492 to 520)"
- anchor2: "Add one self-check test in the style of `test_fork_safety_scan_fails_on_a_ref_without_repo` (line 642)"

#### L2.R1 (f2)

- claim: The plan leaves the POST body file as generic <file> and never states it is written under the renamed .dev/issues/<N>/ directory, so the path-dependency in source 2.5 is unspecified.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>` and body `{\"issue_field_values\":[{\"field_id\":<id>,\"value\":\"<option name>\"}]}`"

#### L2.R1 (f3)

- claim: Task 12 writes ./artifacts/owner-manual-check.md, a path outside the edit-only scope the Constraints state, so the two stated texts conflict on whether artifacts output is allowed.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L2.R1 (f4)

- claim: Commit 1aa2e5c3 does not exist in this checkout, so line-number provenance cannot be verified, mitigated by the re-read rule.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L2.R1 (f5)

- claim: Task 8 allows two orgs/ spellings while the Constraints say exactly one, so the test is more permissive than the stated exact-read rule.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields`"
- anchor2: "the T3 worker may read exactly `orgs/<owner of R>/issue-fields`"

#### L2.R1 (f6)

- claim: The kept maintainer gh label create lines currently carry --repo <owner/repo>, and the plan never says whether to rewrite them to --repo <R>, while the fork-safety test only requires any --repo.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block."
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

#### L2.R3 (f7)

- claim: The create flow must post a pushback comment while the stated two-write limit forbids that additional issue write.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment as today"

#### L2.R3 (f1)

- claim: The plan requires artifact files outside its permitted edit paths, so it cannot meet both the scope constraint and Task 12.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R3 (f8)

- claim: Running the required sync edits generated files under `.claude/`, which the plan explicitly forbids.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint`"

#### L2.R2 (f7)

- claim: The allowed edit locations exclude the package artifact that Task 12 requires the implementer to create.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L1 (MAJOR, open, single): Task 11 names line 329 for the /sc:issue row, but live line 329 is the /sc:graph row and the /sc:issue row is line 333, so a literal edit corrupts the wrong row and leaves the phrase in place.
- L3 (MAJOR, open, overlap): The plan names the third block keys but never defines classification_missing contents, dropping source 2.2's rule that it holds each not set line without the prefix.
- L4 (MAJOR, open, single): The acceptance criteria state literal <reason> formats while source 2.4 lists enumerated reasons, so labels.md content is ambiguous between a placeholder and the enumerated set.
- L5 (MAJOR, open, single): A failed issue-type or field-value read-back has no specified output handling, so the required classification report <redacted> be incomplete.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
