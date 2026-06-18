---
status: success
tier_reached: 2
confidence: 0.88
escalation_reason: forced_by_depth_deep
fix_authorized: true
fix_applied: true
test_is_wrong: false
behavior_is_documented: false
---

# Troubleshoot REPORT — `--reviewers` clobbers caller model identities (Augment PR #178 MEDIUM)

**Target:** `src/superclaude/cli/swarm/commands.py` `--reviewers` override block (PR #178, branch `feat/sc-bare-review-m8m9-migration`, HEAD `590ea2c7`).
**Tier reached:** 2 (forced by `--depth deep`) · **Calibrated confidence:** 0.88 · **Status:** success (fix applied + validated).

## Summary

Augment flagged (severity **medium**) that the `--reviewers` CLI override unconditionally replaced `spec_dict["workers"]["models"]` with placeholder strings (`lens-default-model-{i}`) regardless of input mode. The finding is **real and grounded**: in spec-file / `--stdin` mode the caller supplies their own `workers.models` (often real model identities), and the unconditional resize silently clobbered them. The fix gates the placeholder resize to **lens mode only** (where `workers.models` is placeholder scaffolding by construction); spec-file/stdin callers keep their real model IDs, and the INV-005 warn-with-defaults guard clamps `count` to the real pool size if `--reviewers` exceeds it.

## Diagnosis (root cause)

- `commands.py:1645-1649` (pre-fix) ran `workers_override["models"] = [f"lens-default-model-{i}" for i in range(reviewers)]` with **no gate on `mode`** (`mode` ∈ {`spec-file`,`stdin`,`lens`}, resolved at `commands.py:1581`, in scope at the block).
- **Lens mode**: `_build_spec_from_lens` (`commands.py:728`, models seeded at ~788) already sets `workers.models` to `lens-default-model-{i}` placeholders by construction ("these placeholder strings never reach the wire" — the openai_compat transport reads the `T2Model0N` env contract). The resize merely grows same-kind placeholders to N slots so INV-005 admits `count == 4`. **No data lost.**
- **Spec-file / stdin mode**: the caller's JSON populates `workers.models` with real IDs → the unconditional resize **overwrote** them. **The bug.**
- `workers.models` is consumed in exactly one behaviorally load-bearing place — the INV-005 model-pool guard (`preflight.py:1808-1830`): if `count > len(models)`, the default warn-with-defaults policy clamps `count` down to the pool size with a logged WARNING. The placeholder resize existed solely to inflate the pool length so `--reviewers 4` survived this guard on the lens path.

## Evidence (file:line)

- `src/superclaude/cli/swarm/commands.py:1581` — `mode, spec_dict = _resolve_input_mode(...)` (the in-scope mode var).
- `src/superclaude/cli/swarm/commands.py:1645-1649` (pre-fix) — the unconditional clobber.
- `src/superclaude/cli/swarm/commands.py:728,788` — `_build_spec_from_lens` seeds lens placeholders.
- `src/superclaude/cli/swarm/commands.py:629-633` — openai_compat ignores `workers.models` (wire models from `T2Model0N` env).
- `src/superclaude/cli/swarm/preflight.py:1808-1830` — INV-005 warn-with-defaults clamp (pool = `job.workers.models`).
- `tests/swarm/test_e2e_user_guide.py:276` — `test_reviewers_flag_overrides_worker_count` (the `--reviewers 4` lens-admission invariant the fix must preserve).

## Proposed Fix (APPLIED)

Gate the `models` resize on `mode == "lens"`; always apply the `count` override:

```python
workers_override = spec_dict.setdefault("workers", {})
workers_override["count"] = reviewers
if mode == "lens":
    workers_override["models"] = [f"lens-default-model-{i}" for i in range(reviewers)]
```

Plus an updated comment documenting the rationale and the openai_compat/INV-005 edge.

**Regression tests added** (`tests/swarm/test_e2e_user_guide.py`):
1. `test_reviewers_preserves_real_models_in_spec_file_mode` — captures the spec dict at the `run_preflight` boundary and asserts a spec-file caller's real `workers.models` (`["alpha-model","beta-model","gamma-model"]`) survive `--reviewers 3` (not clobbered to placeholders).
2. `test_reviewers_does_not_inflate_spec_file_pool` — a real 2-model pool + `--reviewers 4` clamps to `workers_requested == 2` (INV-005), the observable proof the real pool was preserved (old code dispatched 4 placeholders).

## Alternative considered

**Placeholder-detection gate** (resize only when existing models all match `lens-default-model-*`). The independent reviewers rated it marginally more robust (auto-handles an openai_compat spec-file caller who happens to under-list placeholder models). Rejected in favor of **mode-gating** because (a) it directly matches Augment's stated preference ("gate the resize on input mode being lens"); (b) it is simpler and keys on the clear architectural fact that only lens mode seeds placeholders; (c) the only divergence is a non-case (spec-file/stdin callers do not write `lens-default-model-*` strings).

## Risk + Rollback

- **Low risk.** Lens-path behavior is unchanged (placeholders still resized → `--reviewers 4` admission preserved; `test_reviewers_flag_overrides_worker_count` green). Only spec-file/stdin `--reviewers` behavior changes — from "silently fabricate placeholders" to "preserve real models; clamp count via INV-005 with a warning if it exceeds the pool".
- **Documented edge (benign):** an openai_compat spec-file caller who under-lists `workers.models` and relies on the `T2Model0N` env pool is now clamped by INV-005 (which reads `workers.models` regardless of transport). This is a pre-existing INV-005/env-pool interaction, not introduced here, and degrades to a logged WARNING — never an error. Captured in the code comment.
- **Rollback:** revert the one-line `if mode == "lens":` gate (+ comment + 2 tests).

## Validation

- `uv run pytest tests/swarm/ -q` → **2214 passed, 27 skipped, 0 failed** (2212 baseline + 2 new tests).
- Targeted `--reviewers`/spec-file tests → 7 passed (incl. the lens `--reviewers 4` admission invariant).
- `uv run ruff check` on both changed files → test file clean; commands.py reports only the **pre-existing** `Logger` F821 (HEAD line 1712, unrelated to this change).

## Out-of-scope pre-existing issues (NOT introduced by this fix)

- `make lint` (`lint-architecture`) fails Check 1: `src/superclaude/commands/recommend.md` has `## Activation` but no `sc-recommend-protocol` skill dir — unrelated to swarm.
- `ruff check .` reports `F821 Undefined name Logger` at `commands.py` (annotation `Optional["Logger"]` vs locally-aliased `_Logger` import) — pre-existing on HEAD.
- Both swarm files (`commands.py`, `test_e2e_user_guide.py`) had pre-existing `ruff format --check` debt on HEAD; this fix matches the file's existing compact idiom rather than whole-file reformatting (to keep the diff minimal/reviewable).

## Next steps

The fix is applied + validated in the worktree. To land it on PR #178 (requires user authorization to commit/push): commit the two files, push to `feat/sc-bare-review-m8m9-migration`, then comment `auggie review` to re-trigger Augment so it can confirm the MEDIUM is resolved. The two LOW findings (#178 `commands.py:1793` spec_dict ordering; #179 `normalize.py:448` stale docstring) are below the user's MEDIUM+ threshold and were not remediated here.
