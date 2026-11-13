review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sonnet/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sonnet/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sonnet/t4-1.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sonnet/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t3-1, t4-1 |
| L2 | open | no | overlap | MAJOR | - | t1b-1, t2b-1, t4-1 |
| L3 | open | no | single | MINOR | - | t3-1 |
| L4 | open | no | single | MINOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10's check cannot pass while the unchanged claim flow keeps its gh api user login lookup that Task 2 expressly allows.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L1.t2b-1 (F2)

- claim: The third block's value semantics are never stated, so a contract with wrong values passes every stated test.
- anchor: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L1.t2b-1 (F4)

- claim: Task 2 can be satisfied by referencing labels.md for the formats, leaving Task 8's create.md test red with no edit scope to fix it.
- anchor: "`create.md` and `labels.md` carry the three exact line formats `not applied: label missing in repo:`, `not set: issue type` and `not set: field Complexity`"
- anchor2: "final output with every `not applied` and `not set` line"

#### L1.t2b-1 (F6)

- claim: The artifacts location is relative to an unnamed package directory and, read from the repo root, falls outside the plan's own edit-only list.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.t3-1 (F2)

- claim: A pre-existing tracked cache file under .claude/ makes the literal reading of this criterion unpassable, though the plan introduces no such change.
- anchor: "`git status --short` shows no path under `.claude/` other than `.claude/settings.json` in the set of staged or tracked changes"

#### L1.t3-1 (F3)

- claim: The pinned commit is absent from this checkout, so the line-number evidence and Task 12 artifacts are not reproducible here; the plan's own re-read rule prevents a wrong outcome.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.t4-1 (F1)

- claim: The constraint allows exactly two writes besides the issue, but Wave 5 keeps the pushback comment, which is a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every"

#### L1.t4-1 (F2)

- claim: The seven listed new tests stay green when Task 3 is reverted, so this acceptance criterion cannot pass as written.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.t4-1 (F3)

- claim: The reason texts exist only in spec 2.4, which is not in the candidate folder, so the implementer cannot write them from the candidate.
- anchor: "with every reason listed in specification 2.4"

#### L1.t4-1 (F4)

- claim: The constraint limits edits to four folders, but Task 12 writes artifacts outside them, and the text does not say whether writing counts as editing.
- anchor: "Edit only under `src/superclaude/`"
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.t4-1 (F5)

- claim: Gh label lines must carry --repo <R>, but Task 1 never asks to fix the live owner-slash-repo label lines, and its acceptance checks only gh issue lines.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries"
- anchor2: "Every `gh issue` line in the file carries `--repo <R>`"

#### L1.t4-1 (F7)

- claim: The scanner regex is unspecified, so the bare orgs token that Task 2 requires in create.md and the spaced owner form can fail the equality check.
- anchor: "Second, every `orgs/` path found by regex in the skill folder files"
- anchor2: "no other `orgs/` path; T1 and T2 keep the old rule"

#### L1.t4-1 (F9)

- claim: The live create.md Wave 5 runs to line 74, so the stated range is stale.
- anchor: "Fourth, Wave 5 (lines 61 to 69)"

#### L1.t1b-1 (F1)

- claim: The 'exactly two writes' constraint conflicts with the mode label and the pushback comment that Wave 5 also writes, so a literal SKILL.md line would be false.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t1b-1 (F2)

- claim: Copying the quoted write-list string without --repo <R> would fail the fork-safety scan that Task 8 requires to pass.
- anchor: "`gh issue create ... --type <name>` to the orchestrator's write list"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L1.t1b-1 (F3)

- claim: The scanner is not told to ignore the bare prose token 'orgs/' that Tasks 2, 3 and 5 require, so a naive regex fails on mandated text.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"

#### L1.t1b-1 (F5)

- claim: Task 12 writes package artifacts outside the four paths the first constraint allows for edits.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.t1b-1 (F6)

- claim: Constraints list three defaults, Task 12 records four.
- anchor: "the four defaults the owner may reverse (the `orgs/` read exception, keeping the `--type` flag, keeping the mode labels, area `tests` giving Test)"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

## Other findings

- L2 (MAJOR, open, overlap): No task states which read-back field is compared with the option name, so a successful Complexity write can be reported as not set.
- L3 (MINOR, open, single): The design doc's own ban wording contains the literal brace placeholder, which a future placeholder scanner over docs would false-positive on.
- L4 (MINOR, open, single): The named test checks only skill tokens, never compares the command file, and sits at line 586 rather than 527, so the agree requirement has no test.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
