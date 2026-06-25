# Final QA Gate — Consolidated (Step 7.2)

**Date:** 2026-06-23
**Lenses:** 6 (3 rf-qa structural + 3 rf-qa-qualitative content), adversarial stance, report-only.

## Verdicts

| Lens | Agent | Verdict | Report |
|------|-------|---------|--------|
| (a) version-pin-consistency | rf-qa | **PASS** | `qa/final-version-pin-consistency.md` |
| (b) invariant-conformance (X1–X7) | rf-qa | **PASS** | `qa/final-invariant-conformance.md` |
| (c) test-assertion-strength | rf-qa | **FAIL** | `qa/final-test-assertion-strength.md` |
| (d) docs-point-not-duplicate (X6) | rf-qa-qualitative | **PASS** | `qa/final-docs-point-not-duplicate.md` |
| (e) advanced-override documented (M4) | rf-qa-qualitative | **PASS** | `qa/final-advanced-override-m4.md` |
| (f) sync-discipline | rf-qa-qualitative | **PASS** | `qa/final-sync-discipline.md` |

## Findings to resolve

### CRITICAL — C1 (lens c): `tests/docs/test_tavily_doc_alignment.py` is vacuously green
- **Defect:** `_iter_text_files` excludes a path if ANY component of the **absolute** path is in `_EXCLUDE_DIRS` (`any(part in _EXCLUDE_DIRS for part in p.parts)`). Because this worktree lives at `…/.dev/worktrees/TavilyUpgrade`, the `.dev` ancestor matches the exclusion → **0 files are ever scanned** → all 4 assertions pass trivially.
- **Proof (mutation):** lens (c) reverted a pin to `tavily-mcp@0.1.2` and the test still PASSED from the worktree path; the same mutation FAILED when run from a path without `.dev`. So the drift guard guards nothing in this worktree.
- **Fix:** exclude only directories UNDER each root, i.e. test `p.relative_to(root).parts` against `_EXCLUDE_DIRS`, not the absolute `p.parts`. Then re-run and confirm (i) it now scans a non-zero number of files and (ii) a reverted `@0.1.2`/stale-token mutation would now FAIL.
- **Owner:** executor (Step 7.3).

## Non-blocking / out-of-scope notes (no action)
- Lens (b): pre-existing `mcp.tavily` placeholder strings in two UNTOUCHED test fixtures (`tests/cli/eval/test_mcp_retry_once.py`, `test_eval_outcome.py`) — outside X4's grep scope and the guard's `_ROOTS`; not an X4 violation.
- Lens (f): a tracked `.dev/releases/.../perf.json` mod — unrelated to this task; not a sync-discipline concern.
- The 8 pre-existing environmental eval-test failures (ruff-not-a-venv-module ×2; missing `.dev/releases/current/cliEval/{artifacts/D-0072,evidence/T06.11}` ×6) and the broad-tree ruff swarm/** noise remain out of scope (documented in phase4/phase7 summaries).

## Gate outcome
1 CRITICAL must be fixed in Step 7.3, then the affected validation (the doc-alignment test) re-run to confirm green AND non-vacuous.

---

## Step 7.3 — Resolution (2026-06-23)

**C1 (CRITICAL) — RESOLVED.** Fixed `_iter_text_files` in `tests/docs/test_tavily_doc_alignment.py` to exclude on `p.relative_to(root).parts` (dirs UNDER the root) instead of the absolute `p.parts` (which matched the `.dev` ancestor of the worktree). Verified by 3 checks:
1. File count now scanned = **911** (was 0 — no longer vacuous).
2. Clean tree: 4 passed.
3. **Mutation proof:** a temp `docs/__mutation_probe__.md` containing `tavily-mcp@0.1.2` made `test_tavily_version_single_pin` FAIL (guard now effective); probe removed → back to 4 passed.

Fix STRENGTHENS the test (weakens no assertion). ruff check + format clean. Full Tavily suite re-run: **45 passed, 1 skipped** (1 fix→verify cycle, under the 3-cycle cap).

Audit: only the doc-alignment test used absolute-path exclusion; `test_tavily_tool_parity.py` globs `agents/`+`skills/` directly with no dir-exclusion, so it was unaffected.

**Gate status: GREEN** — all 6 lenses resolved (5 original PASS + 1 CRITICAL fixed-and-verified).
