# infra-release cluster review, 2026-11-17

| Issue | Title | Verdict | Comment | Evidence |
|---|---|---|---|---|
| 362 | Fall back to a hosted runner when no self-hosted runner is online | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/362#issuecomment-6941376595 | Parked backlog; IronClaude workflows all `ubuntu-latest`; #402 changed no runners |
| 363 | Windows x64 self-hosted runner on Proxmox | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/363#issuecomment-6941377023 | 2026-11-04 decision keeps public repos hosted; no private consumer named |
| 364 | Linux arm64 self-hosted runner | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/364#issuecomment-6941377434 | Same decision; also no arm64 hardware named |
| 393 | sc:implement retry ladder picks advisers it cannot start | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/393#issuecomment-6941377904 | `refs/retry.md:183` "GPT spawn path: none verified"; #518 added GPT rung 0 `T2bModel01` |
| 421 | pr-submit reports Codex clean while security review runs | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/421#issuecomment-6941378302 | `detection-contract.md:130` still "`security_review` is ignored" |
| 381 | Finished Augment review never classified (1 s late comment) | READY-TO-CLOSE | https://github.com/IronbellyOrg/IronClaude/issues/381#issuecomment-6941378766 | `_completion_time` (`classifier.py:319`) since #337; #499 evidence "not reproducible" plus tests with PR 377 times |
| 571 | Release 6.0.0 removal plan | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6941379301 | No removal PR yet; `integration` exists, 11 behind master; 4 decisions open |
| 572 | Evaluate rf-* and other agents | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/572#issuecomment-6941379757 | Waits on #571 removals and Part B map; #582 and #511 edited agents this week |
| 573 | Documentation skill retirement findings | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/573#issuecomment-6941380253 | Optional input; cited skills unchanged since 2026-11-12 (not re-read line by line) |

Counts: READY-TO-CLOSE 1, NEEDS-OWNER-DECISION 3, STALE-VALID 4, BLOCKED 1. Comments posted 9, skipped 0.

## Close candidates

- #381: the stated cause (`created > completed_at` rejecting a 1 second late comment) does not hold on origin/master because `_completion_time` (`src/superclaude/pr_submit/classifier.py:319`, from #337, commit `d4ac8a3d9`, 2026-10-31, already present at the issue's commit `e2a79d95`) extends completion to the same review's own comments. #499 (merged 2026-11-11) replayed real PR 377 data (result: findings) and added `tests/pr_submit/test_late_inline_comment.py` with the exact times; its evidence record `.dev/issues/381-382-456/evidence.md` says "not reproducible on current master". Tests were not run by this review. The original stall's real cause is UNVERIFIED (possibly an older installed copy).

## Owner questions

- #363: Does any private repo have a job that needs a Windows x64 self-hosted runner? If not, close as not planned.
- #364: Does any private repo have a job that needs a Linux arm64 self-hosted runner, and is there arm64 hardware? If not, close as not planned.
- #571: Do you approve starting Part A wave 1 (PRs 1, 2 and 5) into `integration` now, with decisions 6.1, 6.3, 6.6, the `/sc:review-translation` destination and the snapshot fork address to follow?

## Cross-issue notes

- 571, 572 and 573 overlap on the task and documentation bundle. 572 waits on 571 Part A and Part B; 573 is optional input to Part B and Part C. 573 counts `roadmap` as a documentation skill while 571 removes it in Part A PR 11.
- 393 touches `implement-retry-adviser`, which 572 lists for evaluation; settle 393 first.
- 421 and 381 are the same pr-submit monitor family as the closed #382 and #456 (fixed by #499).
