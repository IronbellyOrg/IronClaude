# Cluster process-docs, review of 2026-11-17

| Issue | Title | Verdict | Comment | Evidence |
|---|---|---|---|---|
| 201 | Lack of adaptive and historic TDD process to gate relases | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/201#issuecomment-6941365118 | No release-gating PR this week; overlaps #429 |
| 289 | docs(how-we-work): decide the worktree and branch protocol | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/289#issuecomment-6941365498 | Orca-path rule is in HOW-WE-WORK.md:407; naming, cleanup skill, section and tests still missing |
| 290 | docs(how-we-work): decide how team members propose and change skills | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/290#issuecomment-6941365912 | Owner decided all 5 on 10-29; no rules in HOW-WE-WORK.md, no skill issue template or PR template |
| 313 | Tests must not depend on old logs and planning documents under .dev/ | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/313#issuecomment-6941366386 | Reflect, NFR and routing-refresh tests still read .dev on origin/master; no guard test |
| 320 | Compare PR #303 onboarding guidance with recovered SC/BMAD research | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/320#issuecomment-6941366844 | #303 and #319 merged; comparison not started |
| 322 | Design review: fixed worktree write boundary | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/322#issuecomment-6941367282 | No boundary hook on origin/master; design still has Serena rows and no allowlist |
| 326 | Embed more Git and PM related workflows into skills | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/326#issuecomment-6941369051 | git.md untouched since 10-29; scope narrowed in 11-02 comments |
| 354 | v5.0.0 impact runbook | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/354#issuecomment-6941369646 | Ledger 16/27 on 11-17; owner rulings 11-16; many child bugs filed |
| 429 | post-release test suite or pre-release skill | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/429#issuecomment-6941370125 | No post-release command change since 11-07; no design |
| 550 | Record, fold in and re-test proven tasklist experiment designs | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/550#issuecomment-6941370732 | No comments or inventory; waits on #549 plan; tasklist branch still active 11-16 |

## Close candidates

None. No issue in this cluster is done, superseded or a duplicate on the evidence checked. Possible later close: #320 if the owner no longer wants the comparison after the 6.0.0 plan (#571); #201 if folded into #429.

## Owner questions

None marked NEEDS-OWNER-DECISION. Open owner choices are listed in the comments' next steps: #201 (fold into #429?), #290 (modular or monolith first), #322 (proceed or park), #326 (confirm narrowed scope), #429 (extend post-release or separate pipeline).
