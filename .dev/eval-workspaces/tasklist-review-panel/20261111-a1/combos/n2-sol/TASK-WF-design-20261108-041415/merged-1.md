review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-sol/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-sol/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-sol/t4-2.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-sol/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t2b-1, t4-1, t4-2 |
| L2 | open | no | overlap | MAJOR | - | t2b-1, t4-1 |
| L3 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 12 writes to ./artifacts/, which the Constraints' edit-only list does not allow, so Task 12 cannot be executed without breaking the plan's own scope rule.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.t2b-1 (F2)

- claim: Task 10's acceptance bans the gh api user path that Task 2 preserves and the design document uses for the frozen claim lookup, so the criterion cannot pass without changing claim behaviour.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception, the T3 lookup worker's read-only GET of `orgs/<owner of R>/issue-fields`"

#### L1.t2b-1 (F3)

- claim: Task 1 never states that the read-back returns an option id and must be matched via issue_field_id and single_select_option.name, so an implementer can report a correctly set Complexity field as not set.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t2b-1 (F4)

- claim: Task 3 defines the third block's keys but not its values, so an implementer can emit the wanted type and option instead of the values read back, misreporting what was actually set.
- anchor: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L1.t4-1 (F1)

- claim: A create flow that posts the pushback comment writes a third thing to the created issue, which constraint 23 forbids.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every"

#### L1.t4-1 (F2)

- claim: Several tasks describe a before-state that is already absent at HEAD, so the implementer makes no-op edits.
- anchor: "change `len(blocks) == 2` to 3, keep the first two key lists exactly as they are"
- anchor2: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"

#### L1.t4-1 (F4)

- claim: Keeping the maintainer label lines leaves --repo <owner/repo> on gh label lines, which constraint 21 forbids.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L1.t4-1 (F6)

- claim: The artifact path is ambiguous between the package and the project-root artifacts folder, and it is outside the edit scope.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"

#### L1.t4-1 (F7)

- claim: The stated line numbers differ from HEAD, which the constraint already covers, and the B7 wording in the design doc is still stale.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.t4-2 (F1)

- claim: The create-ref edit names one org path token and its acceptance check names a different token.
- anchor: "states the single `orgs/<owner>/issue-fields` exception"
- anchor2: "orgs/<owner of R>/issue-fields"

#### L1.t4-2 (F2)

- claim: The commanded --mode sentence omits issue type Test, which the type rule requires for a feature in tests.
- anchor: "the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

#### L1.t4-2 (F3)

- claim: Exactly two writes excludes the mode label and the pushback comment that Wave 5 still requires.
- anchor: "writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t4-2 (F4)

- claim: The third block's classification field is not defined to include a mode label that was not applied.
- anchor: "lists every classification it could not set in its final output and in a third return-contract block"
- anchor2: "exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L1.t4-2 (F5)

- claim: Keeping the maintainer label lines leaves `--repo <owner/repo>` instead of `--repo <R>`.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

## Other findings

- L2 (MAJOR, open, overlap): Task 8 does not state that a bare orgs/ token in required prose such as 'no other orgs/ path' is not a path, so a naive scanner regex fails the plan's own mandated text.
- L3 (MAJOR, open, single): The reasons criterion depends on specification 2.4, and source.md is absent from the package, so it cannot be checked.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
