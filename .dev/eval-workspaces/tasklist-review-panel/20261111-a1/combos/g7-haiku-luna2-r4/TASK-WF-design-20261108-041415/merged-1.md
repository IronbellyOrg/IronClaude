review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g7-haiku-luna2-r4/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g7-haiku-luna2-r4/t3-1.md, block ok false
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g7-haiku-luna2-r4/t4-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t3-1, t4-1, t4-2 |
| L2 | open | no | single | MAJOR | - | t4-1 |
| L3 | open | no | single | MINOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The constraint allows exactly two writes to a created issue, but the Wave 5 sequence the plan also requires posts a pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-1 (F2)

- claim: The plan never says to check whether each change already exists; at HEAD 8c93e1d the labels, worker, command, mirror and 119 passing tests already carry the new text, so running the tasks as written makes no-op edits or duplicate tests.
- anchor: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"
- anchor2: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

#### L1.t4-1 (F4)

- claim: The artifact path is outside the four folders the first Constraints bullet allows, and './artifacts' could mean the project-root folder (never staged) or the package folder (always staged), so the implementer must guess.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.t4-1 (F6)

- claim: The same bullet forbids editing under .claude/ and tells the implementer to run make sync-dev, which writes there, so the implementer must guess which rule wins.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"
- anchor2: "run `make sync-dev` after the `src/superclaude/` edits"

#### L1.t3-1 (F1)

- claim: The plan both prohibits edits under `.claude/` and requires a sync command that copies source files there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`;"

#### L1.t3-1 (F2)

- claim: The required artifact files are outside the candidate's permitted edit locations, so the scope constraint and Task 12 cannot both be satisfied.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t3-1 (F3)

- claim: The required mode label is a third issue write, contradicting the constraint that only two things besides the issue itself are written.
- anchor: "`/sc:issue --create` sets the issue type (Feature, Bug or Test) and the org's Complexity issue field on the new issue, applies only the mode label (`bug` or `enhancement`)"
- anchor2: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."

#### L1.t4-2 (F1)

- claim: The plan requires sync-dev while forbidding its writes to .claude, so both instructions cannot be followed.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

#### L1.t4-2 (F2)

- claim: Task 12 requires artifact writes outside the only permitted edit paths, making the plan's scope rule and acceptance criteria incompatible.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-2 (F3)

- claim: The instructions omit how to compare single-select read-back values, allowing a successful field write to be reported as missing when its numeric value is compared with the option name.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

## Other findings

- L2 (MAJOR, open, single): The plan does not quote the Will Not sentences, and the existing test test_command_and_skill_agree_on_the_new_create_boundaries asserts exact phrases that the plan wording does not contain.
- L3 (MINOR, open, single): The cited line numbers are stale in the live file: the Will test is at line 586, the return-contract test at 545, and the fork-safety test at 701.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
