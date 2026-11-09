# Final-check re-test of the L2 limits (#441, Task 11)

Plan package: TASK-WF-designSpec-20261108-165559 (source §8.1 row 22). Limits: spec §6 (`merged-requirements.md:267-286`), source §9.1 (`source.md:612-633`), design table `docs/designs/sc-issue-launch-level-hook.md:536-557`. Acceptance: AC-11 (`source.md:735`).

## Re-test table

Status values: **tested** means a test in this branch pins the stated behaviour; **documented, accepted** means the limit stands as written in the design table and no dedicated test exists. Test paths are relative to the repository root.

| ID | Limit | Status | Evidence |
|---|---|---|---|
| LIM-1 | Monitor tool commands report `ordinary` | pinned as unselected (tested) | `tests/hooks/test_launch_job_identity.py:707` (tool list incl. `Monitor`), `:1151` (Monitor payload) |
| LIM-2 | `setsid` child escapes the supervisor session | pinned as unselected (tested) | `tests/hooks/test_launch_job_identity.py:480`, `:1437` |
| LIM-3 | Killed supervisor makes a live child `unknown` (`orphaned`) | fails closed (tested) | `tests/hooks/test_launch_level_pre_push.py:630`, `tests/hooks/test_launch_job_identity.py:318` |
| LIM-4 | `--no-verify`, `-c core.hooksPath`, `--config-env`, `GIT_CONFIG_*` | pinned leak (tested, FR-101); L1 TAMPER token (tested) | `tests/hooks/test_launch_level_pre_push.py:1062-1065`; `tests/hooks/test_launch_level_guard_l2_tokens.py:107`, `:111`, `:116`, `:121` |
| LIM-5 | Machine drift: uv moves or HOME changes | fails closed, detected at next claim (tested) | `tests/hooks/test_launch_level_pre_push.py:768` (`uv-dir-wrong`: identity check failed); `tests/skills/test_issue_l2_install.py:289` (data file differs: conflict) |
| LIM-6 | Per-worktree `core.hooksPath` set after install | pinned leak (tested, FR-101); detected at next claim (tested) | `tests/hooks/test_launch_level_pre_push.py:1069`; `tests/skills/test_issue_l2_install.py:312` |
| LIM-7 | `git send-pack`, raw receive-pack, libgit2, dulwich | pinned leak for `send-pack` (tested, FR-101); L1 token for `send-pack` (tested); library pushes documented, accepted | `tests/hooks/test_launch_level_pre_push.py:1070`; `tests/hooks/test_launch_level_guard_l2_tokens.py:126` |
| LIM-8 | `gh api` ref writes, REST writes, `orca terminal send` | L1 coverage only (tested in the #440 suite) | `tests/hooks/test_launch_level_guard.py:783`, `:814` (GHWRITE), `:61`, `:786` (ESCAPE); that file is read only for #441 |
| LIM-9 | Missing or non-executable hook | detected at next claim (tested) | `tests/skills/test_issue_l2_install.py:219-221` (`not-executable` case), `:235` |
| LIM-10 | Same-user change to any link of the selector chain | documented, accepted (no dedicated test) | design table row `docs/designs/sc-issue-launch-level-hook.md:547` |
| LIM-11 | HOME redirection | pinned HOME tested; an agent recorded under another HOME documented, accepted | `tests/hooks/test_launch_level_pre_push.py:985` (`test_t22_pusher_home_elsewhere`) |
| LIM-12 | git 2.54+ `hook.<name>.command` / `hook.pre-push.enabled` | L1 token (tested) | `tests/hooks/test_launch_level_guard_l2_tokens.py:60-61` |
| LIM-13 | Wrong remote (L2 checks the ref name, not the repository) | documented, accepted (no dedicated test) | design table row `docs/designs/sc-issue-launch-level-hook.md:550` |
| LIM-14 | Stale job record | fails closed (tested) | `tests/hooks/test_launch_level_pre_push.py:621`, `:707`, `:896`, `:911` |
| LIM-15 | Human with another uid pushes from the clone | fails closed (tested); the real second-uid test skips unless root and `setpriv` | `tests/hooks/test_launch_level_pre_push.py:661`, `:672-675` |
| LIM-16 | L1 over-block | accepted over-blocks pinned (tested) | `tests/hooks/test_launch_level_guard_l2_tokens.py:65` |
| LIM-17 | Template byte change makes hooks read `stale` | detected at next claim (tested) | `tests/skills/test_issue_l2_install.py:200-211` (`marker-only`, `edited-body`, `old-version` read `stale`), `:235` |
| LIM-18 | Case-folding remote (`Main`, `MAIN`) | case-sensitive match pinned (tested); remote behaviour UNVERIFIED | `tests/hooks/test_launch_level_pre_push.py:507` (`refs/heads/Main` in EDGES); see U-9 below |
| LIM-19 | No hook-wide time bound beyond the selector timeout | selector timeout fails closed (tested); no hook-wide bound, documented, accepted | `tests/hooks/test_launch_level_pre_push.py:769` (`selector-timeout`) |
| LIM-20 | Orphaned installer probe directory | documented, accepted (no dedicated test) | design table row `docs/designs/sc-issue-launch-level-hook.md:557` |

## Pending for the owner (not done)

- **OB-H3 (#442 observation): PENDING.** Not run in #441. It is one of the FR-065 preconditions for switching the IR-7 refusal on (`source.md:600`), and AC-11 requires it to be listed as pending (`source.md:735`). The IR-7 refusal path stays off (`IR7_REFUSE = False`) until the owner records a PASS.
- **U-10: PENDING.** Wait for #442 (`source.md:753`); this table lists OB-H3 as pending, as U-10 asks.

## Open, not fixed

- **U-5 (LIM-5): OPEN.** Whether the `uv` directory recorded at claim time is the `uv` a human pusher has on PATH is not observed (`source.md:748`). The tests cover only a wrong recorded uv directory (fails closed, `tests/hooks/test_launch_level_pre_push.py:768`). Needs one observation on the owner's machine.
- **U-9 (LIM-18): OPEN.** Whether any remote folds `refs/heads/Main` or `refs/heads/MAIN` to `main` is not observed (`source.md:752`). The test at `tests/hooks/test_launch_level_pre_push.py:507` pins only the hook's case-sensitive match. Out of scope to fix; the observation is to be recorded when one is made.
