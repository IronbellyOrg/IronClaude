review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted> block ok true
- R3: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R2 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L6 | open | no | single | MAJOR | - | R2 |
| L7 | open | no | single | MINOR | - | R2 |
| L8 | open | no | single | MINOR | - | R2 |
| L9 | open | no | single | MINOR | - | R2 |
| L10 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: Reverting Task 3 (SKILL.md) leaves all seven listed new tests green, so the acceptance line cannot pass for Task 3, and Task 2's Wave 1 text is also uncovered.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.R2 (F4)

- claim: The orgs/ scanner is never defined, so the self-check test has no named function to call.
- anchor: "feeds the `orgs/` scanner a text with `orgs/other/issue-fields` and expects it to be reported"

#### L1.R2 (F5)

- claim: Read per agent, the test requires T1 to T3 to contain a POST, which contradicts their read-only rule.
- anchor: "the skill folder and the agents contain `-X POST` together with `issue-field-values`"

#### L1.R2 (F11)

- claim: Test 6 only checks that the names appear, so a wrong mode-to-type mapping passes.
- anchor: "Sixth, `labels.md` states Feature, Bug, Test and Simple, Medium, Complex."

### L5

#### L5.R2 (F8)

- claim: The constraint says exactly two writes, but the mode label and the pushback comment are also written to the created issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself"

#### L5.R2 (F10)

- claim: The write location is ambiguous between the project-root artifacts folder, which is never staged, and the package artifacts folder.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.R3 (F1)

- claim: The plan simultaneously forbids edits under `.claude/` and requires a sync operation that updates generated `.claude/` copies.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

#### L5.R3 (F2)

- claim: The plan requires writing artifacts outside its stated set of permitted edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.R1 (F1)

- claim: Running the required sync writes generated files under `.claude/`, violating the stated prohibition on edits there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L5.R1 (F3)

- claim: The plan does not identify an artifact location that is clearly permitted by its edit-scope constraint.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): When the field exists but lacks the wanted option, no POST and no not-set line are specified, so the classification is dropped silently.
- L3 (MAJOR, open, single): The bare orgs/ token required by Task 2 can trip the orgs/ scan of test 2 depending on an unspecified regex.
- L4 (MAJOR, open, single): The command Will Not does not add the non-Complexity clause that Task 3 adds to SKILL.md, and no finite check enforces agreement.
- L6 (MAJOR, open, single): A 404 from orgs/ issue-fields on a user-owned repo is recorded as lookup failed, not field not found in org as spec 2.5 requires.
- L7 (MINOR, open, single): The cited line numbers drift from the live file (Will test at 580, claim test at 545, fork-safety test at 695).
- L8 (MINOR, open, single): The elided gh issue create text has no --repo, which the constraint requires.
- L9 (MINOR, open, single): The phrase sits at line 333 in both live copies, not line 329.
- L10 (MAJOR, open, single): The plan leaves the non-fatal outcome and final-output reason undefined when the field read-back command itself fails.

## Reviser brief

Blocking finding ids: L1, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
