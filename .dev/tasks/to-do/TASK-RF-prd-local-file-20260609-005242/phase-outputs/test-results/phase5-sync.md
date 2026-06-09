# Phase 5.3 SoT sync drift guard

`make sync-dev && make verify-sync` -> verify-sync exit 2 (**DRIFT**), disposition per Step 5.3(a) = **log + PROCEED**.

**Drift source:** `.claude/skills/{sc-persona-research-protocol, sc-recommend-protocol}` MISSING in `src/superclaude/skills/` (a `.claude/`-only skill with no `src/` counterpart). This is a PRE-EXISTING condition on the skills surface, present on `origin/master` independent of this task.

**Classification (Step 5.3):** the drift names a SYNCED surface (skills/) this task did NOT touch; it names NONE of this task's edited files (`cli/prd/process.py`, `cli/prd/prompts.py`, `tests/cli/prd/test_spec_flag.py`). `cli/` is never synced (research 03 §3), and git shows ZERO tracked `.claude/` changes from this work. Therefore disposition (a) applies: unrelated synced-surface drift = log + proceed (do NOT reconcile unrelated pre-existing drift in this cli-only task). Disposition (b) (reconcile) does NOT apply since no edited file is a synced surface.
