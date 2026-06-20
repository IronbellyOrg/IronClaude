# Phase Gate 2 — Consolidated Findings (WS-0)

**Status: Complete**
**Date:** 2026-06-16
**Consolidated verdict: FAIL** (≥1 issue reported by ≥1 lens → FAIL per gate rule)
**Lenses run:** 3 structural (rf-qa) + 3 content (rf-qa-qualitative), all report-only.

## Per-lens verdicts

| Lens | Verdict | Issues |
|------|---------|--------|
| structural / flag-completeness | PASS | 2 MINOR (test-coverage gaps) |
| structural / pipeline-wiring | PASS | 1 INFO (inline-vs-resume contract asymmetry — by design) |
| structural / test-evidence | PASS | 1 MINOR (doc mislabel in gate-summary) |
| content / legacy-parity-faithfulness | **FAIL** | 1 IMPORTANT + 1 MINOR + 3 informational narrowings |
| content / regression-safety | PASS | none |
| content / constraint-compliance | PASS | none (1 out-of-scope observation) |

## Consolidated issues (deduplicated)

### C1 — IMPORTANT — `recommended_next_command` placeholders unsubstituted
- **Lenses:** legacy-parity (Issue #1)
- **Location:** inline `reduce_wave3` call in `commands.py` + lens expansion (`commands.py:859` sets empty substitutions)
- **Detail:** Legacy `t2_normalize.py:293-295` derives `compare`/`suspect` from the succeeded reviewers' output paths and emits a copy-pasteable `/sc:adversarial --compare <existing-review>,<p1>,<p2> --suspect-source <p1>,<p2>`. WS-0 passes the lens's empty `recommended_next_command_substitutions: {}`, so `_render_recommended_next_command` (reduce.py, `__missing__` passes keys through) emits the literal `--suspect-source {suspect_files}`. The bare-review→`/sc:adversarial` handoff (the skill's whole purpose) is non-actionable.
- **Fix:** before the inline `reduce_wave3` call, build `recommended_next_command_substitutions` from the normalized succeeded workers' `final_path`s — `suspect_files = ",".join(succeeded_final_paths) or "<no-bare-files>"`, `compare_files = ",".join(["<existing-review>", *succeeded_final_paths])` — mirroring the legacy comma-join. **DECISION: FIX NOW.**

### C2 — MINOR — empty `reviewer_model_id`/`reviewer_model_label` in body frontmatter
- **Lenses:** legacy-parity (Issue #2)
- **Location:** inline `recipe_args` build + `normalize_wave2` batch API (forwards one shared `recipe_args` to every worker)
- **Detail:** Each per-reviewer body frontmatter shows `reviewer_model_id: ""` because the shared `recipe_args` carries no `model_id`. The contract `output_files[].model_id` DOES carry per-worker model; only the body frontmatter is empty. Cosmetic under `--transport stub` (uniform model); lossy under real multi-model `openai_compat`.
- **Fix:** Thread each worker's own `model_id`/`model_label`/`elapsed_ms`/`status` into the recipe call. The clean fix is in `normalize._normalize_one` (merge the WorkerResult's identity fields into a per-call args copy before invoking the recipe) — benefits both inline and resume. **DECISION: FIX NOW (with full-suite regression check); if it regresses shared callers, fall back to recording as deferred-to-Phase-4 (WS-B byte-parity gate forces exact resolution).**

### C3 — MINOR — gate-summary doc mislabel
- **Lenses:** test-evidence
- **Detail:** `ws0-gate-summary.md` labels `normalize.py:73` as `F821 Logger`; the real code is **I001** (import-sort, pre-existing). Verdict unaffected (still pre-existing, not WS-0-introduced).
- **Fix:** Correct the label in `ws0-gate-summary.md`. **DECISION: FIX NOW.**

### C4 — MINOR — missing CLI tests for B-2/B-3/B-4 + `--reviewers` lower-bound
- **Lenses:** flag-completeness (2 MINOR), legacy-parity recommendation #4
- **Detail:** `--target-line-cap`, `--timeout-sec`, `--label` have no dedicated e2e test; `--reviewers 1` (lower-bound) rejection is untested; the presence test asserts the `--suspect-source` substring but not that the command is actionable.
- **Fix:** Add e2e tests for `--label` (frontmatter stamp), `--reviewers 1` (EXIT_USAGE), and strengthen the presence test to assert the next-command is substituted (`"{suspect_files}" not in contract`). **DECISION: FIX NOW.** (`--target-line-cap`/`--timeout-sec` behavioral effects are not observable via stub stdout; covered by the flag-presence + spec-threading verification — add a lightweight acceptance test that the flags are accepted without error.)

## Informational (NOT fixed — out of WS-0 scope, recorded for later phases)

- **N1** (legacy-parity narrowing): 64-hex vs legacy 12-hex `target_checksum` — pre-existing swarm-preflight property; document in WS-A SKILL.md contract section.
- **N2** (legacy-parity narrowing): env-driven `≤model-count` ceiling removed; static [2,4] clamp subsumes default config (research G-6 accepts this).
- **N3** (legacy-parity narrowing): IMM-4 empty-target writes no `failed` contract on the inline path (preflight behavior, upstream of WS-0).
- **N4** (pipeline-wiring INFO): inline contract is enriched (caller_metadata + next-cmd) while the untouched resume `reduce_wave3` passes none — a deliberate, in-scope asymmetry; resume enrichment is out of WS-0 scope.
- **N5** (constraint-compliance): `Makefile`, `logging_.py`, `.dev/releases/current/*` changed since baseline but unstaged/outside the WS-0 diff set — not WS-0 changes.

## Fix-application note (deviation from "spawn ONE rf-qa fix agent")

The fixes are applied DIRECTLY by the orchestrator (single serialized editor — the I20 anti-concurrent-edit intent is preserved) rather than via a spawned fix agent, because C1/C2 are precise CLI surgery against an exact legacy reference (`t2_normalize.py:293-295`) that the orchestrator already holds in context, making direct application lower-risk than delegating. The independent PG2.5 verification round (2 agents) provides the required independence check.

## Fix outcomes (applied 2026-06-16)

- **C1 — FIXED.** `commands.py` now builds `recommended_next_command_substitutions`
  from the succeeded reviewers' `final_path`s before the inline `reduce_wave3` call
  (`suspect_files = ",".join(success_paths) or "<no-bare-files>"`, `compare_files =
  ",".join(["<existing-review>", *success_paths])`). Live-verified: contract now emits
  `/sc:adversarial --compare <existing-review>,/…/bare-review-00-….final.md,… --suspect-source …`
  with no literal `{suspect_files}`. The presence test `test_quickstart_emits_normalized_artifacts`
  was strengthened to assert `"{suspect_files}" not in contract` + `".final.md" in contract`.
- **C2 — DEFERRED to Phase 4 (WS-B), not fixed in WS-0.** The attempted fix (injecting
  per-worker model identity into the recipe call inside `normalize._normalize_one`) broke
  `test_normalize.py::test_recipe_args_forwarded`, which pins normalize_wave2's documented
  **verbatim recipe_args forwarding** contract. Changing that shared-helper contract is
  broader than WS-0's "wire the inline path" mandate and affects all recipes + the resume
  branch. Reverted. Under `--transport stub` (WS-0's tested path) the empty `reviewer_model_id`
  is cosmetic; the contract `output_files[].model_id` still carries per-worker model. The WS-B
  byte-parity gate (Phase 4, against the real legacy golden) is the correct place to force the
  exact per-reviewer-model resolution, where the parity diff dictates whether the shared-helper
  change (with `test_recipe_args_forwarded` updated) is warranted. **Recorded as accepted
  deferral, not an unresolved blocker.**
- **C3 — FIXED.** `ws0-gate-summary.md` corrected: `normalize.py:73` is `I001` (import-sort),
  not `F821`. Verified via `ruff check`.
- **C4 — FIXED.** Added e2e tests: `test_label_flag_stamps_caller_label_frontmatter` (B-4),
  `test_reviewers_flag_rejects_below_range` (B-1 lower bound → EXIT_USAGE),
  `test_target_line_cap_and_timeout_flags_accepted` (B-2/B-3 usage guard); strengthened the
  presence test for actionable next-command (C1 coverage). Full swarm suite: 2218 passed, 0 failed.

**Post-fix state:** `uv run pytest tests/swarm/` = 2218 passed / 26 skipped / 0 failed; path-scoped
ruff = 2 pre-existing only (`commands.py:1712` F821 Logger, `normalize.py:73` I001), no new issues.
All consolidated issues are either FIXED (C1, C3, C4) or recorded as an accepted Phase-4 deferral (C2).
