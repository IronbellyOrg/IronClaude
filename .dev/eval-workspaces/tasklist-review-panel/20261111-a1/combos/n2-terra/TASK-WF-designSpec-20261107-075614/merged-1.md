review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n2-terra/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n2-terra/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n2-terra/t4-2.md, block ok true
- t2-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n2-terra/t2-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2b-1, t4-1, t4-2 |
| L2 | open | yes | overlap | MAJOR | - | t2b-1, t4-1, t4-2 |
| L3 | open | no | overlap | MAJOR | - | t2b-1, t4-1 |
| L4 | open | no | single | MINOR | - | t4-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: resume_decision is given no target_sha, so its re-entry into release_decision must invent one: none holds forever and the live head makes the head check tautological.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"
- anchor2: "`release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)`"

#### L1.t4-1 (F9)

- claim: The base tree already tracks merge_guard.py, refs/merge-guard.md, set-draft-state.sh and the guard tests, and models.py already says 45 members, so the Create and Edit steps and the pre-edit base record do not match this checkout.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py`"

#### L1.t4-2 (F1)

- claim: After a client-failed landing confirmed with no toggle, the next landed request is held as ambiguous, so the release is never recorded.
- anchor: "live state matches the request and observed equals `run_toggles + 1`"
- anchor2: "`settled(draft, confirmed, not changed)` gives `HELD` with `owned_draft` true and no toggle"

#### L1.t4-2 (F2)

- claim: Row 4 cannot both release a landed push and check the head, because the stated signature has no target sha.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"
- anchor2: "it returns `HOLD` for a head different from `target_sha`"

### L2

#### L2.t2b-1 (F2)

- claim: A literal no-L3 test on the Wave 0 bullet can never pass because the bullet is required to contain the at-L3 off sentence.
- anchor: "when it names an L3 or `draft` condition"
- anchor2: "that at L3 with `--merge-guard off` the line \"Remediation is unprotected: --merge-guard off.\" is printed once"

#### L2.t2b-1 (F4)

- claim: Comparing against recorded sentence start text cannot prove byte identity, so a tail edit to a pinned sentence would pass the stated test.
- anchor: "are asserted byte-identical by comparing the live text with string constants (the literal start text recorded in `./artifacts/pre-build-gate.md`, as the existing pins write them)"

#### L2.t4-1 (F1)

- claim: The Wave 0 bullet must state the off line at L3 and that no draft call is made, but the same task's acceptance test fails any bullet that names an L3 or draft condition, so the required text cannot pass.
- anchor: "carries no L3 or `draft` condition"
- anchor2: "when it names an L3 or `draft` condition"

#### L2.t4-1 (F2)

- claim: The Wave 0 bullet and the Resume section run at ordinals 0 to 2, loading the resume ref and applying resume rules on --resume, which is more than the one report line the scope limit allows.
- anchor: "ordinals 0 to 2 change only by one report line"
- anchor2: "applies at every ordinal and in both modes"

#### L2.t4-1 (F3)

- claim: The Engage gate requires a routed Medium-or-higher finding, but the Wave 8 text says a CI-fix cycle engages, and the text does not say whether a failing CI check counts as such a finding.
- anchor: "only when at least one verified finding of Medium severity or higher is routed to a fix"
- anchor2: "engages with kind"

#### L2.t4-1 (F4)

- claim: The single place that mints the guard cycle id is deferred to the Task 1 finding, which may say no id is minted today and name no sentence, so the implementer picks the place.
- anchor: "mints the cycle id"

#### L2.t4-1 (F5)

- claim: The acceptance requires byte identity of two sentences, but the test compares only the literal start text, which cannot prove the whole sentence is unchanged.
- anchor: "asserted byte-identical by comparing the live text with string constants"

#### L2.t4-1 (F6)

- claim: The exit report gives the clear command only for held, so a PR left draft under the unavailable status has no stated clear command or draft report.
- anchor: "values `off`, `released`, `held`, `user_override`, `unavailable`"
- anchor2: "the held-exit list with the clear command"

#### L2.t4-1 (F7)

- claim: The text does not say whether reply, resolve and the S5a re-trigger run after a second failed release.
- anchor: "one retry; `already in target state` counts as confirmed"

#### L2.t4-2 (F3)

- claim: A test that fails on any L3 mention cannot pass on the Wave 0 bullet the same task requires.
- anchor: "when it names an L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line"

#### L2.t4-2 (F4)

- claim: Resume after a landed CI push is not told to skip the review re-trigger, which crash recovery sends to the CI wait.
- anchor: "releases before the re-trigger"
- anchor2: "releases after `push_completed` before the CI re-poll"

## Other findings

- L3 (MAJOR, open, overlap): A literal every-gh-line scan rejects the gh repo view fallback line that the _RESOLUTION_SCRIPTS resolution tests require the script to contain.
- L4 (MINOR, open, single): git status never lists gitignored .claude/ mirrors, so the check's allowance for them is meaningless.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
