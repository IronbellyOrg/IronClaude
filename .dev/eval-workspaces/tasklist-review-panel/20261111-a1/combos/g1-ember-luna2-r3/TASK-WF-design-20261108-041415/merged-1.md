review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g1-ember-luna2-r3/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g1-ember-luna2-r3/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g1-ember-luna2-r3/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | t2b-1 |
| L2 | open | no | overlap | MAJOR | - | t2b-1, t4-1 |
| L3 | open | yes | overlap | MAJOR | - | t2b-1, t3-1, t4-1 |
| L4 | open | no | single | MINOR | - | t2b-1 |
| L5 | open | no | single | MINOR | - | t2b-1 |
| L6 | open | no | single | MINOR | - | t2b-1 |
| L7 | open | no | single | MAJOR | - | t3-1 |

## Blocking findings

### L3

#### L3.t2b-1 (F3)

- claim: Task 12 artifacts lie outside the stated edit-only directory list, requiring an unstated outputs-vs-edits reading.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package"

#### L3.t4-1 (F1)

- claim: An implementer who follows the stated text as written runs `make sync-dev`, and that is wrong because the same plan forbids editing `.claude/`, where the sync writes generated copies.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v;"

#### L3.t4-1 (F2)

- claim: An implementer who follows the stated text as written writes `./artifacts/owner-manual-check.md` in the candidate package, and that is wrong because the constraints permit edits only under four other directory trees.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L3.t3-1 (F1)

- claim: The required sync writes source files under `.claude/`, despite the explicit prohibition on editing anything there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L3.t3-1 (F2)

- claim: Task 12 requires creating an artifact outside the plan's permitted edit locations.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

## Other findings

- L1 (MAJOR, open, single): Third-block value semantics (read-back names or null; classification_missing without prefix) are never stated, so a wrong value shape passes all candidate acceptance criteria.
- L2 (MAJOR, open, overlap): Field read-back shape (option id vs single_select_option.name, case-insensitive name match) is unspecified, so a correct POST can be misread as not applied.
- L4 (MINOR, open, single): New orgs-path test allows two spellings while the prescribing tasks use one, weakening the pin.
- L5 (MINOR, open, single): Cited line numbers have drifted in the live files; only tasks that repeat the re-read instruction are explicit about it.
- L6 (MINOR, open, single): Which history wording is false is left to implementer judgment.
- L7 (MAJOR, open, single): If either read-back command fails or returns unparseable data, the plan does not require a missing-classification line, so the final output may omit a classification the run could not verify.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
