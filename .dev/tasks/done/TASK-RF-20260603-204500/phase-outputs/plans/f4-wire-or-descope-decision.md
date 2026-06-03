# F4 Decision — Wire vs. De-scope the plugin eval gate

**Decision:** **Option 1a — WIRE** (the safe, spec-aligned default)
**Date:** 2026-06-03
**Decided by:** default (1a) — confirmed by the operator's choice of "Build full remediation task" in the `/sc:reflect --remediate` offer (which selected wiring over deferral).

## Rationale

The `/sc:reflect` UC-2 audit found `plugin_eval.py` (`run_preconditions` / `evaluate_adoption` /
`patch_plugin_row`) is fully orphaned — zero callers, no `--plugin --eval` path, no test imports it.
Spec Implementation Order step 8 (`merged-requirements.md:424-428`) requires the plugin eval gate to
be **wired**, and the operator opted for the full remediation. Option 1a (wire) closes the gap as the
spec intends; Option 1b (de-scope) would only paper over it. The deterministic helper functions are
already correct in isolation — wiring them is low-risk (a thin CLI subcommand + skill prose + tests),
and the test coverage 1a adds (a `tests/recommend/test_plugin_eval.py`) also retires the "untested"
half of the finding.

## Which Step 2.x items apply (1a path)

All of Steps 2.2–2.6 apply:

- **2.2** — discovery of the `plugin_eval.py` surface + the `commands.py` Click-group pattern.
- **2.3** — add the `recommend eval plugin` CLI subcommand (real caller of all three helpers; HARD-BLOCK propagates; `sys.exit(1)`).
- **2.4** — wire the 4-phase `--plugin --eval` lifecycle into `SKILL.md` `## Phase 3 — --plugin Mode`.
- **2.5** — add `tests/recommend/test_plugin_eval.py` (HARD-BLOCK raise, warn/skip, 3 adoption verdicts, patch round-trip; tmp_path only).
- **2.6** — `make sync-dev` + run the new tests + grep-confirm a real caller exists.

(1b de-scope path is NOT taken; its alternate item bodies are not executed.)
