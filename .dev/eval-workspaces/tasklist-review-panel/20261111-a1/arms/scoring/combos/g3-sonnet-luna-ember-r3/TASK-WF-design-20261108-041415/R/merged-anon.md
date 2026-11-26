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
| L1 | open | yes | overlap | MAJOR | - | R1, R2 |
| L2 | open | no | single | MAJOR | 2.1 | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: None of the six listed new tests asserts text that only Task 3 adds to SKILL.md, so reverting Task 3 leaves every new test green and the Task 8 criterion fails.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "Sixth, `labels.md` states Feature, Bug, Test and Simple, Medium, Complex."

#### L1.R2 (F1)

- claim: Task 8 POST test wording can be read as requiring the read-only worker to contain a write.
- anchor: "Third, the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`."
- anchor2: "Increased the worker continues. In the Rules section, the \"Read-only GitHub access\" bullet (line 27) keeps \"a path that starts with `repos/<R>/`\" and adds the single exception"

### L3

#### L3.R1 (F3)

- claim: No guard for a gh version without the --type flag, so gh issue create fails as E-CREATE-FAILED and no issue is filed.
- anchor: "`--type` only when the type is listed under `### Repo issue types`"

#### L3.R1 (F4)

- claim: The edit-only-under list excludes the package artifacts folder that Task 12 writes to.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L3.R1 (F6)

- claim: The plan does not say who fills the Issue type row; unchanged T1 and T2 workers write flags.md from the template and could fill it differently from the Wave 5 rule.
- anchor: "`flags.md` gets a derived `Issue type` row by the Q7 rule, and the Complexity row holds the option name."

#### L3.R3 (F1)

- claim: The write limit contradicts the required pushback comment, which is a separate write to the created issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L3.R3 (F2)

- claim: Task 12 requires artifacts outside the only permitted edit roots, so its required deliverables cannot satisfy the stated path constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L3.R3 (F3)

- claim: The plan does not specify matching the read-back to the field ID and selected option name, leaving room to report the wrong field value as applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L3.R2 (F2)

- claim: Maintainer placeholder form is unstated against the use-owner-and-R rule.
- anchor: "No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L3.R2 (F3)

- claim: Check file root is stated two ways (repo-relative path vs package folder).
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): The read-back comparison is not specified, so comparing the response value to the option name can report not applied after create on a successful write.
- L4 (MINOR, open, single): The design doc legitimately contains gh api user, which this literal criterion would reject.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
