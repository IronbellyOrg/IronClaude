# Close list, open-issue review 2026-11-17

Nothing was closed. Each issue has a status comment posted on IronbellyOrg/IronClaude. Source reports sit beside this file.

## Tier 1: agents judged these done (owner to confirm)

| Issue | Why | Caveat |
|---|---|---|
| #488 | Tier 2b, 3 and 4 are defined in origin/master ccsession-models.json (2026-11-11.1); PRs #493, #498, #518 merged; live proxy log on #517 shows tier 3 answering. | The per-alias live probe is tracked in #489. |
| #435 | tests/roadmap/test_parallel.py on origin/master uses threading.Barrier(2, timeout=5); fix landed with #433 (2026-11-08). | CI history since then was not checked. |
| #381 | The stated cause does not hold on origin/master: `_completion_time` in src/superclaude/pr_submit/classifier.py:319 already covers a comment stamped 1 second late; #499 replayed real PR 377 data. | Read from code, tests not run. |

## Tier 2: close only if the owner answers yes

| Issue | Condition |
|---|---|
| #394 | Hook is built and merged (#432, #469). Close now and track the live gates only in #442? |
| #346 | Close as delivered (text and prompt fixes plus #582), with spec-panel retirement and a convergence re-test tracked separately? |
| #363, #364 | Does any private repo need a Windows x64 or Linux arm64 self-hosted runner? If not, close as not planned. |
| #431 | Close as "rules merged in #434, monitor work under #423"? |
| #29, #143, #401, #476, #496, #535, #554 | Close as not planned if the owner confirms the #571 removal PRs 2, 4 and 11 (cleanup_audit, cli_portify, sprint). Precedent: #495, #558, #559 closed as not planned on 2026-11-17. |
| #332 | Superseded if #571 PR 6 retires /sc:load. |
| #556 | Becomes closable when #563 to #565 are resolved. |
| #525 to #530 | Close as superseded if the 50-pair hand check is no longer wanted after the merged shadow runs. |
| #201 | Fold into #429? |
| #320 | Close if the comparison is no longer wanted after the 6.0.0 plan (#571). |
| #536, #510 | Closable after their small, owner-decided follow-up fixes merge. |

## Owner decisions raised (not closures)

- #534: raise or page the sweep's 50-read cap, or keep as a stated limit?
- #551: keep, narrow or drop restrictions 1, 2, 3 and 6?
- #553: pin the TypeSafe plugin to a reviewed release, or install unpinned and watch it?
- #571: start Part A wave 1 (PRs 1, 2 and 5) into `integration` now?
- #387: fix the two parser gaps, or switch the hook to a simpler block rule?
