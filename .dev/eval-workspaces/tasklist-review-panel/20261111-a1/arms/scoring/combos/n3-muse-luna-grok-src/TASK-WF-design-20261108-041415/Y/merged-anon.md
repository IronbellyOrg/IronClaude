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
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3 |
| L2 | open | no | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Task 10 cannot pass while the design doc keeps the unchanged claim flow's gh api user path, and removing that path makes the design doc misdescribe unchanged claim behaviour.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception, the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.R1 (F4)

- claim: Task 8's orgs test accepts a second spelling of the one allowed path, so it passes text that breaks the exactly-one-path rule stated in the constraints and Tasks 2, 3 and 5.
- anchor: "equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields` and appears only in `create.md`, `SKILL.md` and `issue-worker-t3.md`"
- anchor2: "the T3 worker may read exactly `orgs/<owner of R>/issue-fields`"

#### L1.R1 (F5)

- claim: Task 12 writes under ./artifacts/ without naming the package directory, which read from the repo root falls outside the edit-only trees the constraints allow.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: Task 12 requires a sync that modifies `.claude/` even though the constraints prohibit edits there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

#### L1.R2 (F2)

- claim: Task 12 requires writing an artifact outside the plan's allowed edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F1)

- claim: Task 10's design-doc check fails if the claim lookup's gh api user call stays, and passing the check deletes a call the rest of the plan still requires.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L1.R3 (F2)

- claim: The two-write limit drops the pushback comment, whose failure is still E-POST-FAILED, while Task 2 and source 2.1 require that comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "field POST and read-back; pushback comment; final output"

#### L1.R3 (M2)

- claim: The Task 2 check names a path string that the task body never tells the implementer to write.
- anchor: "create.md states the single `orgs/<owner>/issue-fields` exception"
- anchor2: "read-only GET of `orgs/<owner of R>/issue-fields`"

## Other findings

- L2 (MAJOR, open, overlap): No task states that the single-select read-back value is a numeric option id to be matched via single_select_option.name, so a literal implementation can report a successful Complexity write as not set.
- L3 (MAJOR, open, single): Task 6 adds only the creation ban to the command Will Not, so the command file can omit the never-write-a-field-other-than-Complexity boundary the skill states and the lists-agree acceptance requires.
- L4 (MINOR, open, single): Line 329 is the index-repo row in this tree, not the issue row, so a blind line edit would change the wrong command.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
