# Cluster issue-watcher, review 2026-11-17

| Issue | Title | Verdict | Comment | Evidence |
|---|---|---|---|---|
| 394 | Hook that enforces the launch level of claim-launched agents | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/394#issuecomment-6941329524 | Guard merged in #432, L2 in #469, approved route removed in #583; only live gates remain (tracked in #442) |
| 442 | Run the live observations OB-H1, OB-H2, OB-H3 and OB-CTX | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/442#issuecomment-6941329850 | origin/master test file still skips all 12 (`test_launch_level_observations.py:84`); OB-H1 fixtures are synthetic; no results recorded; needs a person at a real terminal |
| 450 | Roll out the issue watcher: live test, shadow run, cron | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/450#issuecomment-6941330327 | Doc fixes done (#485, #548); watcher FU-1 not done (no `issue-watcher-live-test.md`); #584 live test is the claim handoff on issue 452, not the watcher |
| 379 | sc:issue --claim can assign a wrong-repository ClickUp task | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/379#issuecomment-6941330614 | `clickup_claim.py` blob unchanged (65b8d643), `title_number` fallback still at lines 157-159 and 208 |

## Close candidates

None. No issue is READY-TO-CLOSE.

## Owner questions

- #394: The hook is built and merged (#432, #469); should this issue close now, with the remaining live gates tracked only in #442, or stay open until OB-H1 item 1, OB-H2 and OB-H3 pass?

Note: #379 could also use an owner call on whether to schedule it, since claims run with "ClickUp: skipped (no_token)"; it was marked STALE-VALID, not NEEDS-OWNER-DECISION.
