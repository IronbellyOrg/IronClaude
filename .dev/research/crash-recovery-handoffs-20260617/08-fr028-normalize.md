# FR-028 handoff

## Current state

- Lane worktree: `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028`.
- Branch: `fix/swarm-normalize-perworker-status-fr028`.
- HEAD: `d2ad3cbd556f93f2ff9aeef208b9c6d6a9f496d6` (`fix(swarm): thread per-worker status into recipe normalize (FR-028)`).
- Git state: clean and tracking `origin/fix/swarm-normalize-perworker-status-fr028`.
- PR: `https://github.com/IronbellyOrg/IronClaude/pull/179`, open, non-draft, base `feat/sc-bare-review-m8m9-migration`, merge state `CLEAN`, no status checks reported by GitHub, Augment summary comment present.
- M8/M9 corrective task file in this worktree is marked `status: "🟢 Done"` at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/TASK-RF-bare-review-migration-20260616-045915.md`.
- OPS-004 tabletop rehearsal sign-off remains intentionally pending as a human-decision HALT, tracked at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/plans/ops004-rehearsal-pending.md`.

## Evidence

- `git -C /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 status --short --branch --untracked-files=all` returned only the branch/tracking line, with no modified or untracked files listed.
- `git -C /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 rev-parse HEAD` returned `d2ad3cbd556f93f2ff9aeef208b9c6d6a9f496d6`.
- `gh pr view 179 --repo IronbellyOrg/IronClaude --json ...` showed PR #179 open at the same head SHA, base `feat/sc-bare-review-m8m9-migration`, merge state `CLEAN`, and no check rollup entries.
- The FR-028 code change is localized to `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py`: `_normalize_one` now copies shared `recipe_args` and injects only `status=worker.status` before calling `recipe.normalize`, so a shared args dict cannot cause every worker to look like `success`.
- The FR-028 regression tests are in `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/tests/swarm/test_recipe_bare_review.py`: new coverage deliberately omits `status` from shared `recipe_args`, verifies a recoverable `parse_error` promotes to `success`, verifies an unrecoverable `parse_error` stays failed, and verifies a mixed-status batch behaves per worker while leaving the shared args dict unmutated.
- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/tests/swarm/test_normalize.py` was updated so the generic recipe-args forwarding test expects the injected `status` while documenting that caller-provided args are otherwise preserved.
- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/tests/swarm/test_parse_error_salvage.py` remains the direct §7.4 salvage contract suite: it covers promoted salvage, non-salvage rejection reasons, meta sidecar `salvage_reason`, hard-failure omission, recipe exception handling, and no input mutation.
- The M8/M9 task closeout artifacts report final validation green: `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/test-results/final-regression-summary.md` records `uv run pytest tests/swarm/ -q` as `2212 passed, 27 skipped, 0 failed`, `make verify-sync` as exit 0, and the bare-review parity/recipe gates as `27 passed, 0 skipped`.
- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/reports/post-reflect-summary.md` records the final post-reflect as benign degraded-model-diversity, content-clean, and says the remaining grounding/user-decision issue is the single OPS-004 tabletop rehearsal HALT.
- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/reports/final-deliverable-verification.md` records all deliverables present/compliant and explicitly treats OPS-004 sign-off as the only open human follow-up, not a missing deliverable.

## What remains if anything

- Code work for FR-028 appears complete and already pushed to the fork branch.
- PR #179 remains open. Next owner should review/merge it against `feat/sc-bare-review-m8m9-migration` when satisfied.
- No cleanup should be performed in the lane before PR disposition.
- The OPS-004 tabletop rehearsal sign-off is still pending human action. This is not an FR-028 code blocker, but it must not be auto-stamped or fabricated.

## Validation/QA/test plan

Recommended fresh validation before merge, all single-line commands:

- `/usr/bin/env bash -lc 'cd /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 && uv run pytest tests/swarm/test_normalize.py tests/swarm/test_recipe_bare_review.py tests/swarm/test_parse_error_salvage.py -q'`
- `/usr/bin/env bash -lc 'cd /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 && uv run pytest tests/swarm/ -q'`
- `/usr/bin/env bash -lc 'cd /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 && make verify-sync'`
- `/usr/bin/env bash -lc 'cd /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 && uv run ruff check src/superclaude/cli/swarm/normalize.py tests/swarm/test_normalize.py tests/swarm/test_recipe_bare_review.py tests/swarm/test_parse_error_salvage.py'`
- `/usr/bin/env bash -lc 'cd /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 && git status --short --branch --untracked-files=all'`

Recorded validation evidence already available in artifacts:

- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/test-results/final-regression-summary.md`
- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/reports/post-reflect-summary.md`
- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/reports/final-deliverable-verification.md`

## Cleanup/archive plan

- Do not delete or archive `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028` until PR #179 is merged or deliberately closed.
- After merge/close, archive only if no follow-up debugging is needed: keep the PR URL, head SHA, and this handoff path in the recovery index, then remove the worktree with normal git worktree cleanup from the parent repo.
- Preserve `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/plans/ops004-rehearsal-pending.md` until a human completes and records the OPS-004 tabletop rehearsal sign-off.
- Never stage `.claude/` generated mirrors during any cleanup or follow-up. This lane's code changes are in `src/`, `tests/`, docs, scripts, and `.dev` task artifacts.

## Risks

- The behavioral bug is subtle: `normalize_wave2` receives one shared `recipe_args` dict, so without the per-worker copy and `status` injection a `parse_error` worker can be normalized as if it were `success`, preventing §7.4 salvage promotion and causing aggregate undercounts/partial outcomes.
- The fix intentionally injects only `status`. Injecting per-worker timing or other dynamic fields could break frozen golden byte equality in parity gates.
- PR #179 currently has no status checks reported by GitHub, so merge confidence depends on local validation unless CI is triggered later.
- OPS-004 is still pending by design. Any attempt to auto-fill the rollback rehearsal sign-off would violate the human-decision HALT discipline.
- The PR base is `feat/sc-bare-review-m8m9-migration`, not `master`; do not retarget without understanding the stacked branch context.

## New-session prompt

Continue FR-028 from `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028` on branch `fix/swarm-normalize-perworker-status-fr028` at clean HEAD `d2ad3cbd556f93f2ff9aeef208b9c6d6a9f496d6`. Inspect PR #179 (`https://github.com/IronbellyOrg/IronClaude/pull/179`) against base `feat/sc-bare-review-m8m9-migration`; do not modify or clean up unless asked. Validate with `/usr/bin/env bash -lc 'cd /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 && uv run pytest tests/swarm/test_normalize.py tests/swarm/test_recipe_bare_review.py tests/swarm/test_parse_error_salvage.py -q'`, `/usr/bin/env bash -lc 'cd /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 && uv run pytest tests/swarm/ -q'`, and `/usr/bin/env bash -lc 'cd /config/workspace/IronClaude/.claude/worktrees/fr028-fr028 && make verify-sync'`. Remember OPS-004 tabletop sign-off remains a human HALT at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/plans/ops004-rehearsal-pending.md`; do not auto-stamp it.
