review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted> block ok true
- R3: report <redacted> block ok true
- R2: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: docs/designs/sc-issue-command.md:157 holds `gh api user -q .login` (claim lookup, must stay), so the criterion that every gh api path is repos/<R>/... except the orgs read cannot pass.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged"

#### L1.R1 (F3)

- claim: The constraint says two writes besides the issue, but Task 2 also applies the mode label and posts the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F4)

- claim: The source's rule that <owner> is never typed from user input is not carried into Tasks 2 and 5.
- anchor: "(`<owner>` is the part of `<R>` before the slash; no other `orgs/` path;"

#### L1.R1 (F6)

- claim: Task 12 writes under the package artifacts folder, which the edit-only constraint read literally excludes.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F1)

- claim: The plan forbids changes under `.claude/` while requiring `make sync-dev`, which copies source files into `.claude/`.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

#### L1.R3 (F2)

- claim: Task 12 requires an artifact in a directory excluded by the plan’s edit-scope constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: Task 12 requires writing artifacts outside the directories permitted by the scope constraint, so following both requirements is impossible.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): The listed new tests scan folder-wide or only create.md and labels.md, so reverting only SKILL.md (Task 3) turns no new test red.
- L3 (MINOR, open, single): The live line is 333, and the test line numbers in Task 7 and Task 8 are also stale; the constraint to re-read covers it.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
