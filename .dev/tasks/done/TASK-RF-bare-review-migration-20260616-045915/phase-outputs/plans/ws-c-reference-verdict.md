# WS-C Reference-Scan Verdict (Step 5.8)

**Status: Complete**
**Verdict: PASS — zero class-(iii) live invocations; deletion is safe.**
**Date:** 2026-06-16

Scan: `grep -rn 't2_preflight|t2_dispatch|t2_normalize'` over `src/ tests/ scripts/ Makefile .pre-commit-config.yaml .github` (raw: `phase-outputs/test-results/ws-c-reference-scan.txt`). Every remaining match is classified below. NONE is a live invocation of a deleted script.

## Class (i) — docstring / comment / historical-note (ACCEPTABLE)
- `src/superclaude/cli/swarm/recipes/__init__.py:9` — comment ("ports t2_normalize.py").
- `src/superclaude/cli/swarm/recipes/bare_review_v1.py:4,89,105,217` — docstrings/comments ("mirror t2_normalize.py verbatim" — the recipe is the byte-faithful PORT; these document provenance).
- `src/superclaude/cli/swarm/commands.py:1392,1405,1417,1429,1628,1652,1665,1674,1847` — `--reviewers`/`--target-line-cap`/`--timeout-sec`/`--label` help-text + comments citing the legacy `t2_preflight.sh`/`t2_normalize.py` semantics as historical context. No invocation.
- `src/superclaude/skills/sc-bare-review/refs/templates/bare-review-output.md:121` — doc prose (this is the KEPT ref `refs/templates/bare-review-output.md`, NOT a deleted file).
- `tests/swarm/test_recipe_bare_review.py:4,18,52` — docstring/comment (post-rework provenance note).
- `tests/swarm/test_e2e_user_guide.py:155,163,293` — comments ("legacy ... parity").
- `tests/swarm/test_bare_review_parity.py:13,15,19,46` — docstring (explains the gate no longer needs the script).
- `tests/swarm/fixtures/bare_review_v1/golden/README.md:5,8,28,75` — doc prose.

## Class (ii) — frozen-golden regen helper (LEGITIMATE conditional reference)
- `tests/swarm/test_bare_review_golden_regen.py:4,12,18,64,152,154,264,278` — the env-gated (`SWARM_REGEN_GOLDEN=1`) regen helper references the legacy machinery. **Post-deletion behavior is safe + graceful:** the module `skipif`-skips in all normal/CI runs (env unset), so its `LEGACY_SCRIPT` path never executes; only an explicit `SWARM_REGEN_GOLDEN=1` invocation runs it, and it then `assert LEGACY_SCRIPT.exists()` fails with an actionable message ("legacy t2_normalize.py missing ... Post-deletion, re-blessing must drive the CLI"). Documented in `golden/README.md`. NOT a live dependency of any gate.

## Class (iii) — LIVE invocation requiring a fix
**NONE.** No CI workflow (`.github/`), Makefile target, pre-commit hook (`.pre-commit-config.yaml`), `scripts/` file, or production source path invokes `t2_preflight.sh` / `t2_dispatch.sh` / `t2_normalize.py`. The deletion strands no live consumer.

## Conclusion
The legacy script deletion (Steps 5.3-5.7) is safe. Proceed to sync (5.9) + disk-verify (5.10) + post-deletion gate (5.11).
