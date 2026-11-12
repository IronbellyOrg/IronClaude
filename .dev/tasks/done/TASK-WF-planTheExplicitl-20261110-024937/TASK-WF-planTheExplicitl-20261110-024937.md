---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-planTheExplicitl-20261110-024937
version: "1"
priority: Medium
created_date: "2026-11-10"
---

# Clarify Worktree Ownership

Source: ./source.md
Goal: Remove the ambiguous subordinate-coordinator wording while preserving existing authority boundaries.

## Constraints

- Preserve the person-opened coordinator rule and the prohibition on supervised workers creating worktrees or dispatching workers. Do not implement a subordinate mode or alter the worker contract.
- Do not edit historical research artifacts or treat historical references as current guidance.
- `.dev/tasks/` is always staged; never stage generated `.claude/` mirrors. Commit or push only if separately requested.

## Phase 1: Clarify canonical guidance

## Task 1: Narrow worktree owner guidance

Use `src/superclaude/core/WORKER-CONTRACT.md` rules WC-13 and coordinator eligibility, plus the existing research report sections 7.4, 7.6 and 8, to narrow the current owner wording in `CLAUDE.md`, `src/superclaude/core/CLAUDE.md`, and `src/superclaude/skills/ccsession-tag/README.md`. Describe ownership without suggesting a supervised worker can create a worktree or that a subordinate coordinator is authorized. Keep the appended launch-guidance paragraphs identical in the two distributable files and retain their existing required role language.

Acceptance criteria:
- All three guidance locations clearly preserve person-opened coordinator eligibility and the supervised worker ban without introducing new authority.
- The two distributable launch-guidance paragraphs remain identical; `uv run pytest tests/core/test_orca_session_launch_guidance.py` passes.

## Phase 2: Align emitted guidance and checks

## Task 2: Align hook explanation and regression coverage

Depends on: Task 1

Update the ownership sentence in `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` and its `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh` mirror, and update the exact expected denial text in `tests/hooks/test_require_orca_worktree_agent.py`. Add focused assertions to `tests/core/test_orca_session_launch_guidance.py` where necessary to prevent the misleading wording or a worker exception from returning. Synchronize generated development copies with the existing `make sync-dev` target; do not stage generated mirrors.

Acceptance criteria:
- The emitted explanation agrees with the clarified guidance, changes no guard behavior, and the two distributable hook scripts remain byte-identical.
- `uv run pytest tests/hooks/test_require_orca_worktree_agent.py tests/hooks/test_require_orca_worktree_agent_governed.py tests/core/test_orca_session_launch_guidance.py` and `make verify-sync` pass, or their actual failures are reported.
