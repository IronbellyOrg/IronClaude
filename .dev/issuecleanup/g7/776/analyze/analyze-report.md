# /sc:analyze report: src/superclaude/cli/issue_pipeline (architecture, quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:46:41Z; degraded: none

Target: `src/superclaude/cli/issue_pipeline/` at commit a7ae3dd30 (worktree HEAD; origin/master is 3 unrelated commits ahead, none touching this area).

## Layout
cli.py (command group: plan-hash, check-approval, init, adopt-create, adopt-mark, record-create, record-show, record-mark, release-worker, complete, stage-status), approval_line.py, approval_record.py, brief.py, complete.py, plan_hash.py, reads.py, release.py, stage_predicates.py, templates/worker-brief.txt.

## Findings
1. MEDIUM (architecture): the approval predicates are plan-only. `stage_predicates.py:45` `STAGE = "plan"`; `evaluate` (:247) builds its key as `(issue, STAGE, marker.plan_hash)` (:294). Used by cli.py, reads.py and tests/issue_pipeline/test_stage_predicates.py. No stage parameter exists.
2. MEDIUM (architecture, contract mismatch): `templates/worker-brief.txt:12` puts `Plan approval: ... follow rule WC-17 ...` in the shared `[head]`, so every stage row (research, spec, plan, debug; `brief.py:19` STAGES) carries it. Only the plan row writes a plan. What research, spec and debug workers do at WC-17 step 1 is not defined in the brief, the contract or the design note. UNVERIFIED at runtime.
3. LOW: `cli.py` has no `approve` verb; approval is recorded through `record-create` / `check-approval` only. No code in `issue_pipeline/` sets the claim approval (the `Approved` field is read by `issue_watch`).
4. INFO: no approval skill exists under `src/superclaude/skills/` on HEAD or origin/master.

## Recommendations
Owners decide stage-aware approval versus a Plan-row-only line; then change brief template, contract, design note and tests together.
