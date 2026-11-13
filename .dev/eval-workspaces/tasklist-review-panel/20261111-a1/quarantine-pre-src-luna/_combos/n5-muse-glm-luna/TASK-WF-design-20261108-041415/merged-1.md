review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-muse-glm-luna/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-muse-glm-luna/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n5-muse-glm-luna/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | t2b-1 |
| L2 | open | yes | overlap | MAJOR | - | t2b-1, t3-1, t4-1 |
| L3 | open | no | single | MAJOR | - | t2b-1 |
| L4 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance rejects the gh api user path that the claim lookup and Task 2 rule require, so it cannot pass without breaking claim mode.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`, with one stated exception"

### L2

#### L2.t2b-1 (F2)

- claim: No task states that the field read-back must match issue_field_id and compare single_select_option.name, so a numeric comparison would report every successful POST as not applied.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L2.t2b-1 (F3)

- claim: The third block is pinned by keys only, so wanted values could be reported instead of read-back values and classification_missing content is undefined.
- anchor: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L2.t3-1 (F1)

- claim: Tasks 1, 2, 7 and 12 rest on normative content in ./source.md, which is not part of the package under review, so those clauses cannot be executed or audited from the candidate alone.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4 (POST body, `--type` flag, silent drop without push access)"
- anchor2: "and the three exact output line formats of specification 2.4."

#### L2.t3-1 (F2)

- claim: The stated provenance commit does not exist in this clone, so the plan's pre-state line numbers are unverifiable; harmless because the same sentence mandates re-reading live lines.
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L2.t3-1 (F3)

- claim: ./artifacts/ reads as the never-staged repo-root folder rather than the always-staged package artifacts directory, so on the worse reading the owner-manual-check record never reaches the commit.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "the outputs are saved to `./artifacts/t12-checks.log`"

#### L2.t3-1 (F4)

- claim: The constraint's literal reading conflicts with the maintainer lines Task 1 keeps (they carry `--repo <owner/repo>`), and rewriting them to `<R>` would break the maintainer instruction for arbitrary target repos.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`. No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L2.t3-1 (F5)

- claim: The Goal wording covers the missing mode label, which the specified third block excludes; safe because the first block's labels_missing carries it.
- anchor: "lists every classification it could not set in its final output and in a third return-contract block"
- anchor2: "add a third YAML block with exactly the keys `issue_type`, `complexity_field`, `classification_missing`"

#### L2.t4-1 (F1)

- claim: An implementer who follows the stated text as written runs `make sync-dev` while being forbidden to edit under `.claude/`, and that is wrong because the Makefile copies source files into `.claude/`, so both instructions cannot be followed.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L2.t4-1 (F2)

- claim: An implementer who follows the stated text as written must create the manual-check and test-log artifacts outside the allowed edit locations, and that is wrong because the constraints prohibit edits there, making the required deliverables impossible within scope.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L3 (MAJOR, open, single): The exact not-set reasons are only in the absent source.md, so the plan alone cannot satisfy or verify that acceptance line.
- L4 (MINOR, open, single): Task 8 test allows a second orgs spelling that the exact-path rule elsewhere forbids, weakening the scan.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
