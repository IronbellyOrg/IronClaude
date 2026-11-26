# HX-2 notes

Report used: `.dev/reflect/pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416/REPORT.md` plus its `adversarial/merged-verdict.yaml`. Its input-snapshot plan sha256 (4db97227...) equals the plan file, and its source sha256 (fbc456a1...) equals source.md.

## Kept (6)
- D-M13 (blocking in the report): GT1, `blocking_in_implement` true. The plan folder's `artifacts/pre/` holds the five pre-edit snapshots, so the implementer applied the remediation.
- D-M03, D-M09, D-M11, D-M12, D-M15: minor in the report, `blocking_in_implement` false.
- D-M09, D-M11 and D-M15 were re-checked against `artifacts/pre/issue-worker-t1.md:17`, `issue-worker-t2.md:17` and `refs/claim.md` Wave 4 and Wave 1 (read with `git show` at commit 6542ca72). The claims hold.

## Dropped (5)
- D-M01: the coordinator message was not stored in the package. The package now has `artifacts/coordinator-message.md`; this is a missing artifact, not wrong plan text.
- D-M02: Task 3 edits SKILL.md outside the spec's Files list. The plan discloses it as the author's judgement; the report calls it authorised scope, not a defect.
- D-M06: nested backticks make the exact-text boundaries ambiguous. Wording and format only.
- D-M07: `make verify-sync` might fail for unrelated files. Hypothetical, and the implementation log shows it passed.
- D-M14: the tests prove text only; a live re-claim is out of this plan's scope.
- The implementation-time records for this plan hold no `review-*.md` files, so no implementation-time blocking finding exists.

## Base commit (limitation, read this)
- The `start sha=` lines are tree objects, not commits. Tree f8b6a1bb equals commit 119622e3 plus the uncommitted output of the earlier /sc:issue plan (HX-3), including the five files this plan edits.
- That uncommitted state was never a commit: the five target files first appear in squash commit 6542ca72, already carrying both plans' work. No commit contains the repository exactly as this plan was written against.
- Base is therefore 119622e3, the commit both plans started from. At that commit the agent files, `sc-issue-protocol/` and `tests/skills/test_issue_worker_agents.py` do not exist (checked with `git ls-tree`). A reviewer in the sandbox cannot see the files the plan edits; the plan's own Constraints and `source.md` describe them.
- `masked_paths` is `[]`: the implementation creates no file, and the files it edits are absent at base.
