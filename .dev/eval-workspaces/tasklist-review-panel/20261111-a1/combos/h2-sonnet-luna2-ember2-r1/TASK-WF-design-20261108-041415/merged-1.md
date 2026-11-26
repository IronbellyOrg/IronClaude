review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h2-sonnet-luna2-ember2-r1/t1b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h2-sonnet-luna2-ember2-r1/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h2-sonnet-luna2-ember2-r1/t4-2.md, block ok false
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h2-sonnet-luna2-ember2-r1/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/h2-sonnet-luna2-ember2-r1/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t1b-1, t2b-1, t3-1, t4-1, t4-2 |
| L2 | open | no | single | MAJOR | 2.1 | t1b-1 |
| L3 | open | no | single | MAJOR | 2.1 | t1b-1 |
| L4 | open | no | single | MAJOR | - | t1b-1 |
| L5 | open | no | single | MINOR | 2.3 | t1b-1 |
| L6 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: The design doc keeps claim-mode `gh api user -q .login`, which is not a `repos/<R>/` path, and the plan forbids changing claim text, so the Task 10 criterion fails as written.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L1.t1b-1 (F6)

- claim: The pushback comment is a third write that Task 2 keeps, so `exactly two` is imprecise.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t1b-1 (F7)

- claim: Task 12 writes package artifacts outside the four allowed edit locations, and no exemption is stated.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-1 (F1)

- claim: For feature mode with area tests, the plan says both Feature and Test are the issue type.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the issue type rule (mode `bug` gives Bug; mode `feature` with area `tests` gives Test; every other feature gives Feature; Task is never chosen)"

#### L1.t4-1 (F2)

- claim: The required source edits followed by make sync-dev update generated .claude copies, violating the same constraint that forbids editing them.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.t4-1 (F3)

- claim: Task 12 requires artifact files outside the plan's allowed edit paths, so its deliverables cannot be produced while obeying the stated scope.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-1 (F4)

- claim: The plan does not say to compare the single-select option name rather than its ID, leaving the read-back success check underspecified.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t4-2 (F2)

- claim: Running the required sync changes generated files under `.claude/`, contrary to the explicit prohibition on editing that directory.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance forbids the gh api user path that Task 2 keeps legal, so the design-doc edit breaks the claim lookup text.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L1.t2b-1 (F2)

- claim: After the only make sync-dev, a fix in src leaves .claude stale and verify-sync fails without a re-sync.
- anchor: "fix any failure at its source in `src/superclaude/`, never by editing `.claude/`"

#### L1.t2b-1 (F3)

- claim: The artifacts output sits outside the constrained edit dirs and may land in the never-staged repo-root artifacts folder.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.t2b-1 (F4)

- claim: No stated rule matches the read-back row by field id and option name, so the comparison can use the numeric option id.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t3-1 (F1)

- claim: Plan omits how to match a read back option number to the option name.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t3-1 (F2)

- claim: Task 12 artifacts write falls outside the allowed edit set.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t3-1 (F3)

- claim: Plan does not quote the kept maintainer label lines in the required repo form.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block."
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

## Other findings

- L2 (MAJOR, open, single): No rule says how to match the field value in the read-back (single_select_option.name versus numeric value), so a naive compare reports a false `not applied after create`.
- L3 (MAJOR, open, single): The plan never says who fills the `Issue type` row, and the unchanged T1 and T2 workers do not list it, so the row can stay a placeholder.
- L4 (MAJOR, open, single): None of Task 8's new tests asserts text added by Task 3 unless the holder check is an equality check, which the wording does not say.
- L5 (MINOR, open, single): The Task 3 example line has no `--repo <R>`, so copied literally it fails the fork-safety scan.
- L6 (MINOR, open, single): Stale line number: the /sc:issue row is at line 330 in this checkout, though the re-read constraint mitigates it.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
