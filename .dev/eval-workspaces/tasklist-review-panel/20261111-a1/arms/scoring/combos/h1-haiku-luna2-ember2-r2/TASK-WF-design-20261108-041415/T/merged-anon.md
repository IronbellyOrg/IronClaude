review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R5: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R3 |
| L2 | open | yes | overlap | CRITICAL | - | R1, R2, R3, R4, R5 |
| L3 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Reverting Task 3 turns none of the seven new tests red, so the Task 8 acceptance line cannot pass for Task 3.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "and appears only in `create.md`, `SKILL.md` and `issue-worker-t3.md`"

#### L1.R3 (F4)

- claim: The new scanner test accepts a second orgs/ spelling that Tasks 2, 3 and 5 do not prescribe, weakening the pinned exception.
- anchor: "equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields`"

### L2

#### L2.R1 (F2)

- claim: The Wave 5 sequence posts a pushback comment, a third write, which the constraint forbids.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L2.R1 (F3)

- claim: The read-back match rule is unstated, so a naive comparison prints a false not-applied line on every success.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L2.R1 (F4)

- claim: Much of the change already exists at HEAD 8c93e1d, so following Task 8 duplicates tests with no stated baseline.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

#### L2.R1 (F5)

- claim: Keeping the maintainer lines as they are leaves a gh label line with --repo <owner/repo>, not the --repo <R> the constraint requires.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L2.R1 (F6)

- claim: The artifact folder is undefined, and the two candidate locations have opposite staging rules.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R1 (F7)

- claim: The constraint lists three defaults and Task 12 names four.
- anchor: "Decisions taken as defaults (the owner may reverse them later)"
- anchor2: "the four defaults the owner may reverse"

#### L2.R4 (F1)

- claim: The plan requires a sync that edits `.claude/` while forbidding edits there.
- anchor: "run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"

#### L2.R4 (F2)

- claim: Task 12 requires writing deliverables outside the plan's allowed edit scope.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R5 (F1)

- claim: The plan both requires applying a mode label and limits issue writes to exactly two classifications, excluding that label.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L2.R5 (F2)

- claim: The plan does not specify how to interpret the field read-back, although the current protocol requires matching the field ID and comparing the single-select option name.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L2.R2 (F1)

- claim: Task 10 criterion 3 cannot pass while the unchanged claim lookup uses gh api user and Task 2 allows user paths.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L2.R2 (F2)

- claim: Task 12 artifacts path sits outside the stated edit allow-list, leaving its base directory ambiguous.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R2 (F3)

- claim: Goal wording suggests the missing mode label belongs in the third block, whose definition in source 2.2 holds only not set lines.
- anchor: "lists every classification it could not set in its final output and in a third return-contract block"
- anchor2: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L2.R2 (F4)

- claim: Maintainer label lines kept verbatim use --repo <owner/repo>, conflicting with the universal --repo <R> rule.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L2.R2 (F5)

- claim: Candidate never specifies comparing single_select_option.name rather than the numeric value on field read-back.
- anchor: "the POST with `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>` and body"

#### L2.R3 (F1)

- claim: The exact not-set reason tokens are left in source.md, so an implementer can omit or abbreviate a token and still pass the plan's own wording.
- anchor: "and the three exact output line formats of specification 2.4."

#### L2.R3 (F2)

- claim: Field id type and the complexity-field.json path are unspecified, so the POST can be built at the wrong path or with a wrongly typed id.
- anchor: "{\"issue_field_values\":[{\"field_id\":<id>,\"value\":\"<option name>\"}]}"

#### L2.R3 (F3)

- claim: The artifact root is ambiguous, so the manual check can land in the never-staged repo-root artifacts/ instead of the package artifacts/.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L2.R3 (F5)

- claim: Task line numbers drift after the base commit, so execution depends on the re-read instruction rather than on current numbers.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

## Other findings

- L3 (MINOR, open, single): Task 8 wording reads as banning all gh label create lines, conflicting with kept maintainer lines.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
