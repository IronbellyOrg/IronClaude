review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/candidate.md sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sonnet-ember/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sonnet-ember/t4-1.md, block ok false
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-design-20261108-041415/reviews/combos/n4-sonnet-ember/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1 |
| L2 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L3 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance forbids the claim-mode gh api user path that Task 2 allows and the claim-unchanged constraint requires.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.t2b-1 (M1)

- claim: Maintainer gh label create lines kept as-is carry --repo <owner/repo>, not --repo <R>, violating the stated --repo <R> rule.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block."

#### L1.t2b-1 (M2)

- claim: Plan never defines how the read-back value is compared, so a numeric-value comparison would falsely report not applied after create.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.t2b-1 (N1)

- claim: Artifacts path is ambiguous between package and repo root and sits outside the stated edit roots.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t1b-1 (F1)

- claim: The design doc still documents the claim-mode call `gh api user -q .login` (line 157), which must stay, so this criterion cannot pass as written.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

#### L1.t1b-1 (F3)

- claim: The worker-agent and command test files that pin text edited in Tasks 5 and 6 are never run by the plan.
- anchor: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"
- anchor2: "In the Rules section, the \"Read-only GitHub access\" bullet (line 27) keeps"

#### L1.t1b-1 (F4)

- claim: The 'exactly two writes' constraint ignores the pushback comment and mode label that Wave 5 still writes.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.t1b-1 (F5)

- claim: Task 12 writes package artifact files that the edit-only constraint does not list.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t1b-1 (F6)

- claim: As written, 'no file' conflicts with existing files that quote the placeholder as a ban; it should be limited to the skill, refs and agent files.
- anchor: "No file may contain a brace placeholder for owner and repo; use `<owner>` and `<R>`."

## Other findings

- L2 (MAJOR, open, overlap): As described the orgs scanner flags the bare orgs/ prose token that Tasks 2, 3 and 5 require, with no prose exemption stated.
- L3 (MINOR, open, single): The /sc:issue row sits outside the level-table markers, so the level-table copy instruction is a no-op for this change and is misdescribed.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
