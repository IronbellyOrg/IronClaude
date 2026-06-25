# Phase 2 Research Corpus Inventory

**Date:** 2026-06-21
**Glob:** `.dev/tasks/to-do/TASK-TDD-20260621-124414/research/*.md`
**Expected:** 7 codebase research files (00–06). **Found:** 7. **Missing:** none.

| File | Status | Lines | Has Gaps § | Has Summary § | Topic |
|------|--------|-------|-----------|---------------|-------|
| 00-prd-extraction.md | Complete | 139 | yes | yes | FR-DRS requirements (goal, evidence, approach, AC-1..AC-6, scope, OQ-DRS.1/.2/.3) |
| 01-runtime-surface-algorithm.md | Complete | 281 | yes | yes | The 7-step sweep algorithm + ledger schema/TypedDict/reduction precedence/count invariant (mostly [UNVERIFIED — spec-only]; greenfield) |
| 02-product-path-integration.md | Complete | 458 | yes | yes | reflect CLI producer/consumer surfaces; contract READ at runner.py:445; invocation-site tradeoffs (OQ-DRS.2) |
| 03-consumer-surfaces.md | Complete | 292 | yes | yes | The 6 canonical `runtime_surface_*` field names; §5.3 pre-filter; §9.3 advisory map; sprint-executor criterion UNMET |
| 04-eval-path-integration.md | Complete | 180 | yes | yes | grader.py `check_yaml_list_len_eq`; 5 uc2 cases (ids 37–41); grader-to-module integration options |
| 05-reuse-and-boundaries.md | Complete | 326 | yes | yes | 6 reuse verdicts re-confirmed; reflect→audit import boundary (3 options, rec Option C reflect-local copy) |
| 06-skill-prose-demotion.md | Complete | 151 | yes | yes | §6.1 4b/4b′ demote-vs-preserve boundary; no contract_version bump (OQ-DRS.3) |

**Total:** 1,827 lines across 7 files. All Status: Complete; all carry Gaps + Summary sections (confirmed via agent completion reports + line counts).

**No files missing or In Progress.** Corpus is ready for the research-gate QA (Steps 3.2–3.6).

**Cross-file notable findings flagged during Phase 2 (for QA attention):**
- The six contract fields: only 5 carry the `runtime_surface_` prefix; the 6th (`unreached_surfaces`) is a list — a `startswith` filter would silently drop it.
- `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` (ensemble.py:59) is stale vs SKILL.md's declared `"1.6.0"` — harmless today (consumer gates on `major == "1"`) but an inconsistency to reconcile.
- Acceptance criterion "sprint executor reads the deterministic scalars" is currently UNMET — `cli/sprint/executor.py` reads no reflect contract today.
- Strongest CLI invocation site `_audit_once` (runner.py:394-453) does NOT cover bare `claude -p /sc:reflect` — OQ-DRS.2 must resolve the bare-skill path.
