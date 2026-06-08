# QA Report — Research Gate (rf-qa)

**Topic:** PASS_RECOVERED rerun/handoff predicate research
**Date:** 2026-06-04
**Phase:** research-gate | fix_authorization: false

> The rf-qa agent declined to write this file (perceived no-write harness instruction) and returned its
> report inline; the orchestrator persisted it here, then resolved the findings (see
> `research/04-gate-resolutions.md`).

## Initial Verdict: FAIL → Resolved to PASS (post gap-fill)

All 6 required zero-trust checks PASSED (independently verified by reading source):
1. `_rerun_targets_passed` reads raw JSON strings (`rerun_tasks.py:1168/:1176/:1177`) → fix must coerce.
2. Caller `rerun_succeeded` → `if rerun_succeeded and merge_back:` (:1370-1374, skip at :1431-1444). ✓
3. `handoff.py:34` compares string `.value`; consumed at executor.py:1103/:1277. ✓
4. Direct test import viable; RED pre-fix / GREEN post-fix (runtime-probed: unfixed returns False;
   `TaskStatus("pass_recovered").is_success` True). ✓
5. `models.py:49-58` is_success PASS-family; `:207/:231` status string round-trip. ✓
6. `resume/planner._coerce_task_status` NOT on origin/master — builder must not import it. ✓

## Findings (and resolutions — see research/04-gate-resolutions.md)

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | CRITICAL | research 03 recommended `uv run python -m py_compile` but CLAUDE.md:7 forbids `python -m` | RESOLVED — builder instructed to use `uv run python -c "import py_compile; py_compile.compile('<file>', doraise=True)"` (or rely on pytest, which catches syntax errors). |
| 2 | IMPORTANT | research 02 missed `tests/sprint/test_resume_contract.py:8,55-70` which already imports/tests `is_validated_success` | RESOLVED — builder instructed to extend `test_is_validated_success_only_for_pass_plus_gate_success` with a `PASS_RECOVERED + GateOutcome.PASS → True` case (primary handoff test surface), in addition to / instead of test_handoff_record.py. |
| 3 | IMPORTANT | research 03 doc claims not tagged [CODE-VERIFIED]/[UNVERIFIED] | ACKNOWLEDGED — doc-hygiene only; claims are about stable template/CLAUDE.md text the analyst + this gate independently re-verified. Does not change built-task correctness. |
| 4 | IMPORTANT | research 03 cites `.claude/templates/...` not canonical `src/superclaude/templates/...` | ACKNOWLEDGED — SoT nitpick; `.claude/` is the synced mirror (verified current). Builder reads template content either way; built task is unaffected. |
| 5 | MINOR | no research-notes.md in research/ | NON-ISSUE — research-notes.md lives at TASK_DIR root per skill convention. |
| 6 | MINOR | no incremental-writing markers | NON-ISSUE — researchers wrote header-first then Edit-appended; polished end state is expected. |

VERDICT (post-resolution): PASS — substantive findings (#1, #2) folded into the BUILD_REQUEST; doc-hygiene findings acknowledged and non-blocking.
