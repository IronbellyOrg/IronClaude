review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g4-haiku-ember-terra-r3/t4-1.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g4-haiku-ember-terra-r3/t2b-1.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/g4-haiku-ember-terra-r3/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2-1, t2b-1, t4-1 |
| L2 | open | yes | overlap | MAJOR | - | t2b-1, t4-1 |
| L3 | open | no | single | MINOR | - | t4-1 |
| L4 | open | no | single | MAJOR | - | t2-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: Constraint 23 allows exactly two writes besides the issue, but Wave 5 keeps the pushback comment, a third write.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-1 (F3)

- claim: The artifacts folder is unnamed, and the two readings are a never-staged project-root folder or the package folder, neither in constraint 19's allowed trees.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.t4-1 (F4)

- claim: The plan never states that labels_applied and labels_missing now describe the mode label only.
- anchor: "keep the first block key for key and the claim block unchanged"

#### L1.t4-1 (F6)

- claim: Constraint 26 lists three defaults and Task 12 says four.
- anchor: "the four defaults the owner may reverse"
- anchor2: "Decisions taken as defaults (the owner may reverse them later)"

#### L1.t4-1 (F7)

- claim: The live tree already has several texts that Tasks 3 to 6 say to change, so their before-state premises are stale.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"

#### L1.t2b-1 (F1)

- claim: Stale line numbers may mislead placement but the re-read instruction and function names resolve them; minor note only.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.t2b-1 (F2)

- claim: The edit-scope constraint and the artifacts write require the implementer to guess whether ./artifacts is package-relative or repo-root; graded Medium because the sentence needs that guess.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2b-1 (F3)

- claim: Task 10 omits the user path that Task 2 allows, so keeping gh api user needs the implementer to guess an exemption; graded Medium because the sentence needs that guess.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.t2-1 (F1)

- claim: The required package artifacts cannot be written within the permitted edit scope.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2-1 (F2)

- claim: The create flow both forbids and requires a pushback comment as an additional write to the created issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself:"
- anchor2: "field POST and read-back; pushback comment; final output"

#### L1.t2-1 (F3)

- claim: The referenced return contract excludes the missing mode label even though the goal requires every missing classification in the third block.
- anchor: "lists every classification it could not set in its final output and in a third return-contract block"
- anchor2: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

### L2

#### L2.t4-1 (F2)

- claim: The seven listed new tests do not assert Task 4's flags row or wording, or Task 3's error rows, so reverting them leaves all tests green and the acceptance line fails.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "In `flags-decision.md` add an `Issue type` row"

#### L2.t2b-1 (F4)

- claim: A naive substring test for type: would match subagent_type:; the label-token reading avoids it, noted as a minor wording risk only.
- anchor: "labels.md` contains no `type:` label, no `complexity:` label and no `gh label create` line for either."

## Other findings

- L3 (MINOR, open, single): Cited line numbers are stale; the live file has the Will and Will Not test at line 586.
- L4 (MAJOR, open, single): The plan does not require interpreting the field read-back by field ID and option name, so an implementation can falsely report a successfully set value as missing.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
