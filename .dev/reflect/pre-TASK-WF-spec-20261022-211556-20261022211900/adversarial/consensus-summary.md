# Emerging consensus after Round 2 (17/17 points agreed)

Verdict: not_ready. Meaning: scope, phase order and coverage of Fix 1-4 are sound; acceptance bullets in Tasks 5, 6 and 8 violate source.md:38 ("every acceptance bullet must fail on a wrong edit") and must be rewritten before execution.

Must-fix (medium):
- R1-1 Task 5: header-comment check (tasklist:88) and ::warning check (tasklist:90) pass a wrong reword; require advisory wording and forbid 'requiring this check' / 'before merge' on text-anchored blocks.
- R1-5 Task 6: compare unchanged run-body lines (pull-sync-framework.yml:89-108 incl. git add -f docs/.framework-sync-commit), step if/working-directory/name, and assert --base master --head sync/framework.
- R2-4 Task 8: badge must name actions/workflows/test.yml; boundary paragraph must state it cannot block; sync paragraph must state it does not push to master.
- R1-4/R2-2 Task 6 stub: git stub delegates every non-push subcommand to real git; gh stub logs and prints scripted count; set GITHUB_REPOSITORY; run with bash -eo pipefail; third run with index == HEAD.

Low:
- Backslash-before-backtick check written as a fenced command (tasklist:94).
- Replace line-number slices (tasklist:88, :91) with text anchors.
- Define <t1-head> (./artifacts/t1-head.txt) and <decided file input> (Task 2 Decision line); fail if angle brackets survive.
- Depends on: Task 7 -> Task 2 is the real predecessor; Task 3/4 do not depend on 2/3 (chain is safe but misstated).
- Task 4: git init -b master and a local commit identity.
- Task 5 render: pin BASE_SHA as an ancestor of HEAD_SHA (e.g. a commit touching merge.py and its parent).
- Task 1/9 scope tooling: parse porcelain -z, handle deleted/renamed paths; .dev/reflect/ is untracked and not ignored, so any write there after Task 1 fails Task 9.
- INF-045: the 300 vs 3,000 path-filter question has no home; put a docs quote in Task 3's artifact and a 'Question for user' in t9-leftovers.md (no new task).
- Task 9: read scripts/README.md neighbours before editing.

Rejected: a user question before Task 9 (R2-3; source.md:35,:44 already decided); R2-9/R2-10 are reflect coverage-matrix corrections, not tasklist edits.

Shared assumptions: A-001 holds (gh authenticated, can_approve_pull_request_reviews=true); A-002 holds (pyproject.toml:38); A-003 UNVERIFIED (boundary-guard pytest on base not run); A-004 qualified (no high, but must-fix list is mandatory).
