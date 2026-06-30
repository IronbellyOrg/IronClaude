# Research Notes: OQ-1 Opt-2a — integrity Signal B recovered-tail exemption

**Date:** 2026-06-04
**Scenario:** A (explicit — fix shape + guardrails pinned by base-selection.md adversarial recommendation)
**Depth Tier:** Quick
**Track Count:** 1

> **MATERIAL UPDATE:** PR #124 MERGED to origin/master at 2026-06-04 10:57 UTC (`5d660ca9`). The
> `resume/` package — including `integrity.py` with Signal A fixed and `signal_b_pass = derived is
> TaskStatus.PASS` (line 131, the PENDING state) — is NOW ON master. So this Opt-2a fix lands on a
> fresh branch off `origin/master` (request is feasible exactly as stated; no dependency on #124).

---

## EXISTING_FILES (all now on origin/master post-#124-merge)

- `src/superclaude/cli/sprint/resume/integrity.py` — `_validate_last_completed` (~line 100-154). Signal A (122-125, already None-safe PASS-family). **Signal B target (127-131):** `derived = _classify_transcript(transcript); lc.derived_status = derived; signal_b_pass = derived is TaskStatus.PASS`. Verdict `validated = signal_a_pass and signal_b_pass and artifacts_ok` (~150).
- `src/superclaude/cli/sprint/models.py` — `TaskStatus.PASS_RECOVERED` + `is_success` (PASS-family); reference only.
- `src/superclaude/cli/sprint/executor.py` — assigns PASS_RECOVERED via `detect_error_max_turns` + `_task_completed_before_overrun` (~997-1011 / 2321-2330) — the recovery determination Opt-2a trusts for Signal B.
- `src/superclaude/cli/sprint/rerun_tasks.py` — `_classify_transcript` (SHARED; never emits PASS_RECOVERED). **MUST NOT be touched (Opt-2b is rejected).**
- `tests/sprint/test_resume.py` — `test_resume_pass_recovered_counts_as_completed` (line 142) already exists (from #124); lines 210-213 carry the DEFERRED `validated_last` note ("OQ-1/Opt-2-dependent — NOT a guard"). `_build_gate_fixture` + `TestInvariants.test_gate_hard_stops...` are the integrity-gate negative-case patterns.
- Design spec: `.dev/tasks/to-do/TASK-RF-20260604-035221/phase-outputs/oq1-adversarial/adversarial/base-selection.md` — the adversarial recommendation + 4 guardrails.

## PATTERNS_AND_CONVENTIONS

- The Opt-2a edit (per base-selection.md guardrails): guard the exemption to PASS_RECOVERED ONLY (`if lc.persisted_status is TaskStatus.PASS_RECOVERED: signal_b_pass = True`); ordinary PASS still transcript-rechecked. Keep Opt-1's `derived is not None and derived.is_success` widening for the non-recovered path. Set `lc.derived_status` for transparency so the report shows the recovered basis (e.g. `lc.derived_status = TaskStatus.PASS_RECOVERED` for the exempted case).
- DO NOT touch shared `_classify_transcript` (Opt-2b — blast radius into rerun failed-task discovery).
- Validation: UV only; `python -m` FORBIDDEN (CLAUDE.md:7 — use `uv run python -c "import py_compile; ..."` or rely on pytest); `uv run pytest tests/sprint/ -q`; BOTH `uv run ruff check src/ tests/` AND `uv run ruff format --check src/ tests/`.

## GAPS_AND_QUESTIONS

- Exact post-Opt-2a test shape: (a) extend `test_resume_pass_recovered_counts_as_completed` to ASSERT `report.validated_last is True` for the recovered last_completed (un-defer the commented note), since Signal B now passes via the exemption; (b) add a NEGATIVE case — a recovered last_completed with MISSING artifacts still STOPs (validated_last False) so the exemption doesn't over-trust; (c) confirm ordinary non-PASS still fails Signal B. Researcher 2 to pin exact assertions + whether to edit the existing test vs add a new one.
- Confirm `lc.derived_status` field exists on BoundaryTask and how the report surfaces it (researcher 1).
- Exact line numbers on master (post-merge) for the Signal B block (researcher 1 — re-locate by text).

## RECOMMENDED_OUTPUTS

- `research/01-integrity-signalb-edit.md` — File Inventory + Data Flow: exact Signal B block on master (re-located by text), the precise Opt-2a edit (guarded exemption + derived.is_success widening + lc.derived_status transparency), `lc.derived_status`/BoundaryTask field confirmation, executor recovery-determination evidence, confirmation `_classify_transcript` is untouched.
- `research/02-test-surface.md` — Test & Verification: the existing `test_resume_pass_recovered_counts_as_completed` + `_build_gate_fixture`/`test_gate_hard_stops` patterns; exact RED→GREEN assertions for Opt-2a (validated_last True post-fix; negative missing-artifacts case; ordinary-PASS unaffected).
- `research/03-template-pr-discipline.md` — Template 02 + fork-PR discipline + validation command set (python -m-free).

## SUGGESTED_PHASES

- Researcher 1 (File Inventory + Data Flow): integrity.py Signal B + executor recovery + models + confirm _classify_transcript untouched. Output 01.
- Researcher 2 (Test & Verification): test_resume.py integrity-gate test surface; the RED→GREEN Opt-2a assertions. Output 02. (No source-edit detail — researcher 1 owns that.)
- Researcher 3 (Template & Examples): MDTM template 02 + fork-PR + validation discipline. Output 03.

## TEMPLATE_NOTES

- Template **02** (discovery→fix→test→validate→QA gate→commit/push/fork-PR). Tier **Quick** (3 researchers, 0 web). QA_GATE_REQUIREMENTS: PER_PHASE. VALIDATION: pytest + both ruff gates + python-m-free compile. TESTING: UNIT (RED→GREEN; the load-bearing assertion is `validated_last is True` for a recovered last_completed, which is RED pre-Opt-2a / GREEN post).

## AMBIGUITIES_FOR_USER

- None blocking. The branch target is now unambiguous (fresh branch off origin/master — integrity.py is on master post-#124-merge). The fix shape + guardrails are pinned by base-selection.md.
