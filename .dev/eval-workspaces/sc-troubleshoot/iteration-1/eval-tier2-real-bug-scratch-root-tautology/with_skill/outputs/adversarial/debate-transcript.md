# Adversarial Debate Transcript

**Mode**: compare
**Inputs**: fix-1.md, fix-2.md, fix-3.md
**Depth**: standard
**Focus**: correctness, risk, test-coverage
**Date**: 2026-05-21

## Round 1 — Opening positions

**Pro-Fix-1 (security-engineer)**: Minimal surface. The bug is one call site; fix the call site. The `output_dir=` kwarg has a legitimate use in `containment_guard` — touching the helper risks collateral damage.

**Pro-Fix-2 (root-cause-analyst)**: One-line call-site fixes are how this bug shipped in the first place. The API allows the tautology silently. A defensive guard at the helper closes the class, not just the instance.

**Pro-Fix-3 (quality-engineer)**: The coverage gap is the real story. `test_scratch_root_policy.py` pins the doctor and the helper but NOT the `eval_run` boundary. Without a regression test at the eval_run CLI boundary, this bug can be reintroduced by accident next quarter.

## Round 2 — Cross-examination

**Re: Fix-2 (defensive helper guard)**:

- Pro-Fix-1 counter: `containment_guard` (`isolation.py:307-318`) calls `resolve_scratch_root(scratch_root, config=config)` with no `output_dir=` kwarg, so the proposed guard does not break the current `containment_guard` path. So that risk is hypothetical, not actual.
- Pro-Fix-3 counter: even so, the helper guard does not address the missing regression test — and the missing test is the systemic problem, not the API ergonomics.
- Pro-Fix-2 concedes: the guard is a "belt" without a "suspenders" — useful but insufficient on its own.

**Re: Fix-3 (CLI-boundary regression test)**:

- Pro-Fix-1: accepts that the test is the right shape; can be incorporated into Fix-1 trivially.
- Pro-Fix-2: accepts, but argues the test alone does not stop a refactor that re-introduces the tautology somewhere else (e.g. `eval_gather`, `eval_replay`).

**Re: Fix-1 (call-site only)**:

- Pro-Fix-2: insufficient — only closes the instance.
- Pro-Fix-3: insufficient without the test — the bug can come back silently.

## Round 3 — Synthesis

Consensus emerges:

- The **call-site change is non-negotiable** (Fix-1's mechanism).
- The **regression test is non-negotiable** (Fix-3's mechanism) because the absence of that test is what let the bug ship.
- The **defensive helper guard** (Fix-2) is a *good-to-have* but introduces API ergonomics complexity (the `containment_guard` opt-in). Moving it to a **follow-up task** keeps the immediate fix minimal and unblocks the security gate quickly.

## Decision

**Merged fix = Fix-1 mechanism + Fix-3 test plan**, with Fix-2's defensive helper guard split into a follow-up task.

Rationale: addresses both the bug (instance) and the systemic gap (missing CLI-boundary test) with the smallest possible diff. The follow-up guard can be debated on its own merits in a separate PR without blocking the security fix.
