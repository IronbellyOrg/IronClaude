review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-sonnet-src/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-sonnet-src/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-sonnet-src/t4-2.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n2-sonnet-src/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t4-1, t4-2 |
| L2 | open | no | overlap | MAJOR | - | t2b-1, t4-1 |
| L3 | open | yes | overlap | MAJOR | - | t1b-1, t2b-1, t4-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The design doc must keep the claim lookup's gh api user path, which this check forbids, so the check cannot pass without breaking unchanged claim behaviour.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L1.t2b-1 (F2)

- claim: No stated text says the read-back value is an option id to be matched via issue_field_id and single_select_option.name, so a direct name comparison reports every successful Complexity write as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t2b-1 (F3)

- claim: The kept maintainer lines use --repo <owner/repo> for a human maintainer, so keeping them breaks the stated --repo <R> rule and rewriting them changes their audience.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block."
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

#### L1.t2b-1 (F5)

- claim: Read per file this test is unpassable without putting a POST into templates and the read-only T3 worker; only the unstated across-the-set reading passes.
- anchor: "the skill folder and the agents contain `-X POST` together with `issue-field-values` and no `-X PUT`"
- anchor2: "still forbids every write and every `-X` other than `GET`."

#### L1.t4-1 (F2)

- claim: The Constraints allow only the issue type and the Complexity value as writes to the created issue, but Tasks 1 and 2 keep a pushback comment and a mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output with every"

#### L1.t4-1 (F4)

- claim: The plan gives no key or value rule for the Complexity read-back, so an implementer may compare the wrong key or value shape and misreport the field.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t4-1 (F5)

- claim: The plan never says what to do when a named change is already in the live tree, and most of its changes already are, so tasks become no-ops or duplicate tests.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3`"
- anchor2: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"

#### L1.t4-1 (F7)

- claim: The type lookup uses a route the GitHub docs do not list, and the plan does not mark it UNVERIFIED although it works on the fork today.
- anchor: "the T3 worker also runs `gh api repos/<R>/issue-types`"

#### L1.t4-2 (F1)

- claim: Task 10's acceptance check cannot pass while the design document still documents claim mode's gh api user call.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

#### L1.t4-2 (F2)

- claim: The read-back never says to compare single_select_option.name, so a check of the returned value property treats a successful Complexity write as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t1b-1 (F1)

- claim: Test 2 is worded as a subset check and no new test pins SKILL.md text, so reverting Task 3 leaves every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"
- anchor2: "appears only in create.md, SKILL.md and issue-worker-t3.md"

#### L1.t1b-1 (F2)

- claim: The plan does not say who derives the Issue type row, and the unchanged T1/T2 workers fill the shared template without the rule.
- anchor: "`flags.md` gets a derived `Issue type` row by the Q7 rule, and the Complexity row holds the option name"

#### L1.t1b-1 (F3)

- claim: How the read-back is compared is unspecified, and a compare of value against the option name can print a false 'not applied after create'.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t1b-1 (F5)

- claim: The scanner is not told to ignore the bare `orgs/` token that Task 2 requires as prose, so a naive regex fails on required text.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"
- anchor2: "that no other `orgs/` path is allowed"

#### L1.t1b-1 (F6)

- claim: The 'exactly two things' sentence omits the mode label and pushback comment still written, and the edit-only list omits the artifacts Task 12 writes.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.t1b-1 (F7)

- claim: The lookup response carries is_enabled and the plan does not filter on it, so a disabled but listed type could fail gh issue create and stop the run (UNVERIFIED).
- anchor: "`--type` only when the type is listed under `### Repo issue types`"

### L3

#### L3.t2b-1 (F6)

- claim: Keys and one sentence are pinned but the read-back-or-null values from specification 2.2 are not, so wanted-but-unapplied values would pass every stated acceptance check.
- anchor: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L3.t4-1 (F3)

- claim: Task 6 as written gives the command a Will Not list without the Complexity-only clause, so its acceptance that both lists agree cannot pass.
- anchor: "add that the skill never creates an issue type or an issue field and never writes a field other than Complexity"
- anchor2: "and the Will Not line (line 93) to also say it creates no issue types or issue fields"

#### L3.t1b-1 (F4)

- claim: Task 3 adds two Will Not items and Task 6 gives the command only one, and the skill's Will list has no create bullet to agree with.
- anchor: "The Will and Will Not lists agree with the skill's Will and Will Not lists on the new create behaviour."
- anchor2: "and the Will Not line (line 93) to also say it creates no issue types or issue fields"

## Other findings

- L2 (MAJOR, open, overlap): ./artifacts at the repo root is never staged while a package's artifacts live under .dev/tasks/<pkg>/artifacts, so the file's destination and staging depend on the reader's working directory.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
