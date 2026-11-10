RESTART: REMOVE THE "ANY ISSUE OF ANY SEVERITY FAILS" RULE AND CAP REVIEW LOOPS AT 2 FIX CYCLES (5.0.0 RELEASE BLOCKER)

You replace an earlier worker on this task. It stopped at 2026-11-01 00:01 UTC on Claude API connection errors, with a context of about 484k tokens, and never resumed. Nothing it did was committed. Its on-disk work is yours to reuse; do not message or wait for it.

READ FIRST, IN THIS ORDER
1. The original task spec: /tmp/t11-severity-rule-spec.md. It still governs (WHY, TARGET, CHANGE, CONSTRAINTS, OBSERVABLE ACCEPTANCE) except where the FINAL DECISIONS below change it.
2. The previous worker's inventory (step 1 of the original spec, already done; reuse and update it, do not redo it from scratch): /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule/.dev/review-severity-rule/inventory.md
3. Its plan pre-review report (advisory): /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule/.dev/reflect/pre-removeTheAnyIssu-20261031235716/REPORT.md. Fold in its findings C1-C4 and partial rows INF-003, INF-005, INF-007, INF-009, INF-017, INF-019, INF-023.

STATE OF THE WORKTREE
- Worktree /home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule, branch fix/review-severity-rule at f90877be (= origin/master, checked 2026-11-01 22:46 UTC), no upstream set. No tracked changes. Untracked: .dev/review-severity-rule/, .dev/reflect/pre-removeTheAnyIssu-20261031235716/, .dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261031-235404/.
- The package TASK-WF-removeTheAnyIssu-20261031-235404 is SUPERSEDED (its return-contract.yaml says so). Do not execute it. Leave it on disk; do not delete it.

FINAL DECISIONS (from the user; nothing is pending, do not ask again)
- B1 rule: when a review fails only on minor findings, note them and proceed: no recheck, no FAIL. Remove every "any severity" rule. At the cap with blocking findings still open, stop and escalate to the user; never pass them silently.
- B2 cap: "limit review loops to 2" means 2 FIX CYCLES = at most 3 reviews (review, fix, re-review, fix, re-review), then escalate the open blocking findings to the user. Existing "Max 2 fix cycles" stay; "Max 3" and uncapped loops drop to 2. Canonical text, reused everywhere: "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings".
- B3 /sc:implement: option A. Remove the second A2 in-place repair (A1 review, fix, A2 re-review, one repair, re-review = 2 fix cycles). Keep the retry-adviser attempts A3-A5, the halt contract, the saved reviewer prompt and FINAL unchanged. Update refs/retry.md (valid j values, A2 timing, the "Worst case: 9 reviews" line), the ledger Resume rows and their twins, and the implement tests. Re-read refs/retry.md and refs/qa.md before editing; line numbers may have moved.
- Add the 3 sites the pre-review found: rf-analyst.md:74, task-builder/SKILL.md:895, synthetic-dnsp-finding.contract:52 (re-verify each line). Put the S5 sentence in the output style (pragmatic.md) so later tasks can read it there.
- P1: do not change update.sh.

DO
1. Update inventory.md for the decisions above.
2. Regenerate the plan: /sc:workflow "<this task, citing /tmp/t11-severity-rule-spec.md, this file, FINDINGS.md at /home/coder/workspaces/IronClaude/.dev/worktrees/qa-loop-investigation/.dev/qa-loop-investigation/FINDINGS.md and the inventory, with labelled requirement ids>" --depth standard --handoff none
3. /sc:implement <printed plan path>
4. Tests, verify-sync, lint, commit, push, CHANGELOG Unreleased entry and /sc:pr-submit --monitor 3 exactly as in original spec steps 5 and 6.
5. Apply the new rule to your own run: minor findings from your plan's reviewers are noted, not fixed in extra rounds.

IF YOU GET STUCK
- On an API or connection error, retry. If you cannot continue, or your context gets too full to finish reliably, send an escalation saying exactly where you stopped (last finished plan task, files changed, what is uncommitted) instead of improvising.

OBSERVABLE ACCEPTANCE: as in the original spec, plus the cap text and option A changes above are present and tested. worker_done gives the PR URL, final head SHA, inventory path, canonical rule text with file:line, every file changed, and checks run with results.
