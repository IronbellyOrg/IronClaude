# Cluster ccsession-eval-models (review of 2026-11-17)

Base URL for comments: https://github.com/IronbellyOrg/IronClaude/issues/<n>#issuecomment-<id>

| Issue | Title | Verdict | Comment | Evidence |
|---|---|---|---|---|
| 352 | Flaky ccsession shim tests under load | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/352#issuecomment-6941347483 | setup_shim wait still 10 x 0.3 s on master; #453 fixed one cause on 11-08 |
| 435 | Flaky test: parallel thread ids | READY-TO-CLOSE | https://github.com/IronbellyOrg/IronClaude/issues/435#issuecomment-6941348032 | master test uses a Barrier(2); PR #433 merged 2026-11-08 |
| 488 | ccsession tiers 2b / 3 / 4 | READY-TO-CLOSE | https://github.com/IronbellyOrg/IronClaude/issues/488#issuecomment-6941348686 | master JSON has tier2b/3/4; #493, #498, #518 merged; Coder#494 closed |
| 489 | Eval panel tiers and alias map for Tier 2b | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/489#issuecomment-6941349345 | precondition #488 met; no framework code; live probe not run |
| 517 | Proxy: first model always thinks, 400 on medium effort | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/517#issuecomment-6941349941 | no effort handling or switch rule on master; only #516 workaround |
| 523 | Add muse-ember-1.0 to Tier 4 | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/523#issuecomment-6941350430 | Coder#503 closed, shipped; master tier4 still 3 slots, no muse-ember |
| 546 | Model-enforcement pre-event hook | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/546#issuecomment-6941351001 | no hook on master; waits on #551 decisions |
| 551 | Model-policy hook v1 design decisions | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/551#issuecomment-6941351527 | no decisions recorded; no code |
| 487 | Re-useable Spec-Task Eval Framework | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/487#issuecomment-6941352031 | spec only; no lab module on master |
| 560 | eval run coverage failures labelled eval doctor | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/560#issuecomment-6941352695 | commands.py:644 literal still present; Clay backlog hold |
| 561 | eval run leaves directories after invalid selection | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/561#issuecomment-6941353225 | mkdir at lines 1753, 1780 still present; Clay backlog hold |
| 562 | Hook coverage rejecting unrelated eval suites | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/562#issuecomment-6941353718 | Clay parked; no activity |
| 553 | Install TypeSafe Jev plugin by default | NEEDS-OWNER-DECISION | https://github.com/IronbellyOrg/IronClaude/issues/553#issuecomment-6941354230 | not in user_settings_defaults.json on master |

## Close candidates

- 435: origin/master `tests/roadmap/test_parallel.py` uses `threading.Barrier(2, timeout=5)` so both runner threads are alive together; PR #433 merged 2026-11-08 is the last commit on that file. CI history since then not checked.
- 488: tier2b/tier3/tier4 defined in origin/master `ccsession-models.json` (2026-11-11.1); #493, #498 and #518 merged; IronbellyOrg/Coder#494 closed 2026-11-12; proxy log on #517 shows tier 3 answering on GLM-5.3 and Qwen3.8 Max. Remaining per-alias live probe is tracked in #489.

## Owner questions

- 551: For restrictions 1, 2, 3 and 6, keep, narrow or drop each one?
- 553: Install the TypeSafe plugin pinned to a reviewed release (if one exists) or unpinned and watched?
