review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r5/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r5/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-design-20261108-041415-r5/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | 2.2 | t2b-1 |
| L2 | open | no | single | MAJOR | 2.1, 2.5 | t2b-1 |
| L3 | open | no | single | MINOR | 3.4 | t2b-1 |
| L4 | open | no | single | MAJOR | 3.1 | t2b-1 |
| L5 | open | yes | overlap | MAJOR | - | t3-1, t4-1 |
| L6 | open | yes | single | MAJOR | - | t4-1 |
| L7 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

### L5

#### L5.t3-1 (F1)

- claim: An implementer who follows the stated text as written cannot write the required owner-check file or checks log without violating the file-scope constraint, so the required artifact acceptance criterion cannot pass.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.t3-1 (F2)

- claim: An implementer who follows the stated text as written must run `make sync-dev` but cannot allow its copies into `.claude/`, so the instructions contradict each other; the target copies source files there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L5.t3-1 (F3)

- claim: The owner-check notes omit the source's organization-membership visibility condition and API-version 404 caveat, leaving operators without those documented explanations for failed field lookup or writes.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4 (POST body, `--type` flag, silent drop without push access)"

#### L5.t4-1 (B1)

- claim: The exact-two-writes constraint conflicts with applying the required mode label, so following both requirements cannot produce the specified create behavior.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

### L6

#### L6.t4-1 (B2)

- claim: The planned `--mode` wording says feature mode selects Feature, contradicting the required Test type when the feature area is `tests`.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "mode `feature` with area `tests` gives Test"

## Other findings

- L1 (MAJOR, open, single): Task 3 omits the source value format for classification_missing and the redefinition of labels_applied/labels_missing as mode-label only.
- L2 (MAJOR, open, single): No task requires the field body file to live under the renamed .dev/issues/<N>/ directory, losing the no-path-lost failure case.
- L3 (MINOR, open, single): Task 12 counts four reversible defaults where the source names three owner decisions (Q4, Q5, Q6).
- L4 (MAJOR, open, single): Task 11 conditions the CLAUDE.md level-table copy on a phrase search instead of re-running it as the source requires.
- L7 (MAJOR, open, single): The plan does not carry forward the source's organization-membership visibility case or require documenting and checking that an inaccessible Complexity field produces a non-fatal `not set` result.

## Reviser brief

Blocking finding ids: L5, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
