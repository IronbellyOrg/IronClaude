# QA Report — Discovery Readiness Gate (Phase 2)

**Topic:** TASK-RF-20260604-OQ1-SIGNALB — Signal B PASS_RECOVERED exemption (OQ-1 Opt-2a)
**Date:** 2026-06-04
**Phase:** task-integrity (discovery-readiness pre-edit gate)
**Fix cycle:** N/A (first pass)
**Stance:** Adversarial / zero-trust. Every discovery claim re-verified by independently re-reading the worktree source/test files. No discovery-quoted line number or code snippet was trusted without re-reading the cited worktree file.

---

## Overall Verdict: PASS

The discovery/plan artifacts are complete and accurate enough to begin source edits. Every load-bearing claim (source-site line ranges, code text, test-site ranges, RED→GREEN derivation, no-edit boundary facts, validation/PR discipline) was independently confirmed against the worktree. One MINOR insertion-plan ambiguity (Step 4.2/4.3 overwrite-vs-plan ordering) was found and FIXED in-place in `test-site-inventory.md`.

---

## 1. SOURCE SITE verification (source-site-inventory.md)

| # | Discovery claim | Worktree ground truth | Result |
|---|---|---|---|
| 1 | `_validate_last_completed` spans integrity.py:92–154 | `def _validate_last_completed` at 92; method body ends 154 (`return True, [], lc`), 156 starts `_detect_partial` | PASS |
| 2 | Signal B block at integrity.py:127–131 | 127 comment, 128 `transcript = self._read_transcript(...)`, 129 `derived = _classify_transcript(transcript)`, 130 `lc.derived_status = derived`, 131 `signal_b_pass = derived is TaskStatus.PASS` | PASS — byte-exact |
| 3 | `derived = _classify_transcript(transcript)` at line 129 | confirmed at 129 | PASS |
| 4 | `lc.derived_status = derived` at line 130 | confirmed at 130 | PASS |
| 5 | `signal_b_pass = derived is TaskStatus.PASS` at line 131 | confirmed at 131 (also re-confirmed via `sed -n '131p'`) | PASS |
| 6 | Signal A at 122–125 (`signal_a_pass = lc.persisted_status is not None and lc.persisted_status.is_success`) | 122 comment, 123–125 the assignment | PASS |
| 7 | Artifacts block at 133–148 (unchanged) | 133 comment … 148 `lc.artifacts_present = artifacts_ok` | PASS |
| 8 | Verdict at 150–154, `validated = signal_a_pass and signal_b_pass and artifacts_ok` (unchanged) | 150 `validated = signal_a_pass and signal_b_pass and artifacts_ok`; 151–154 suspect/return | PASS |
| 9 | Opt-2a replacement branches Signal B ONLY on `lc.persisted_status is TaskStatus.PASS_RECOVERED`; leaves artifacts/verdict untouched | Proposed code (source-site §"Intended replacement shape" + research/01 §2) gates exemption on exactly that predicate; `else` keeps `_classify_transcript` + widening; artifacts/verdict lines copied verbatim | PASS |
| 10 | "No source edit applied yet" | Signal B line 131 still the OLD form; branch `fix/sprint-integrity-signalb-pass-recovered` @ base `02949fb3` | PASS |

**Note (non-blocking imprecision, NOT fixed):** research/01 §1 and §Summary describe the base as `origin/master` commit `02949fb3cee8b456df69c9b1e2eac59c3f51c6c6` and frame the recovery semantics around PR "#126". The actual commit at SHA `02949fb3` in the worktree is `fix(ci): hermetic canonical fixtures + brainstorm skill-availability test (#136)`. The **SHA prefix and the file content both verify** (the worktree content matches the researched Signal B block line-for-line), so the inventory's substantive claims are correct. The "#126" reference is a descriptive provenance note, not a load-bearing line/code claim, so it is left as-is. The actual `source-site-inventory.md` says only `02949fb3`, which is correct.

---

## 2. TEST SITE verification (test-site-inventory.md)

| # | Discovery claim | Worktree ground truth | Result |
|---|---|---|---|
| 1 | `PASS_TRANSCRIPT` constant at 33–37 | constant defined 34–37 with comment at 33; content matches (output_tokens 42 + success result) | PASS |
| 2 | `test_resume_pass_recovered_counts_as_completed` at 142–257 | `def` at 142; method's last assert (`assert "T03.01" in drift.explanation`) at 257; 259 starts next method | PASS |
| 3 | T03.01 transcript write (`PASS_TRANSCRIPT`) at 189 | line 189 `(results / "phase-3-task-T03.01-output.txt").write_text(PASS_TRANSCRIPT)` | PASS |
| 4 | deferred comment block at 210–214 | 210–214 the composite-note comment | PASS |
| 5 | weak `assert report is not None` at 215 | line 215 exactly | PASS |
| 6 | `_build_gate_fixture` at 686–725 | `def` at 686; `return index` at 725 | PASS |
| 7 | `class TestInvariants` at 728 | line 728 | PASS |
| 8 | overclaim test at 729–751 | `def test_gate_hard_stops_on_last_completed_overclaim` 729; ends 751 (`assert accepted.passed is True`) | PASS |
| 9 | helper persists T03.01 as `pass` (711), writes `PASS_TRANSCRIPT` (719), `lc_deliverable_exists` gates `lc_deliverable.txt` (693–695) | 711 `"status": "pass"`; 719 write_text(PASS_TRANSCRIPT); 693–695 conditional deliverable write | PASS |
| 10 | positive-test deliverable: `recovered_deliverable.txt` written (161–162) + declared on T03.01 (167) so `artifacts_ok` True | 161–162 write `recovered_deliverable.txt`; 167 `_task_block("T03.01", deliverable=deliv)` | PASS |
| 11 | `RECOVERED_TRANSCRIPT` not yet present | `grep -c RECOVERED_TRANSCRIPT tests/sprint/test_resume.py` → 0 | PASS (consistent with "discovery only") |

### 2a. "PASS_TRANSCRIPT would be vacuous" rationale — VERIFIED CORRECT

`_classify_transcript(PASS_TRANSCRIPT)`: result event present, `is_error=false`, `output_tokens=42 > 0` ⇒ returns `TaskStatus.PASS`. Under pre-Opt-2a `signal_b_pass = derived is TaskStatus.PASS`, that is already `True`, so `assert report.validated_last is True` would pass WITHOUT the source fix (vacuous / always-green). Switching to `RECOVERED_TRANSCRIPT` (derives `FAIL_RECOVERABLE`) makes pre-fix Signal B `False` → genuine RED; the Opt-2a exemption flips it GREEN. **Rationale is correct.**

### 2b. `RECOVERED_TRANSCRIPT` derives `FAIL_RECOVERABLE` — VERIFIED by tracing `_classify_transcript` (rerun_tasks.py:547–593)

Input: assistant msg (output_tokens 42) + `{"type":"result","subtype":"error_during_execution","is_error":true}` + `api_retry`.
Trace: `total_output_tokens=42`; `result_event` present; `subtype="error_during_execution"` ⇒ `subtype.startswith("error")` True ⇒ `is_error=True`. `not is_error and tokens>0` → False (skip PASS). `transient = "api_retry" in text` → True. `if is_error and transient:` ⇒ **returns `FAIL_RECOVERABLE`**. **Correct.**

### 2c. RED→GREEN of the positive test (post-Opt-2a) — VERIFIED

Fixture persists T03.01 `pass_recovered` (→ `PASS_RECOVERED`, `is_success` True ⇒ Signal A True), deliverable present (artifacts_ok True), transcript `RECOVERED_TRANSCRIPT`. Pre-Opt-2a: `signal_b_pass = (FAIL_RECOVERABLE is PASS)` = False → `validated_last False` → RED. Post-Opt-2a: `persisted_status is PASS_RECOVERED` → `signal_b_pass True` → `validated_last True` → GREEN. **Genuine RED→GREEN confirmed.**

### 2d. Step 4.2 / 4.3 insertion plans workable against the helper's real behavior — VERIFIED (with a MINOR fix applied)

- `_build_gate_fixture` RETURNS `index` (line 725); the result.json and transcript live under `tmp_path / "results"`, reachable for overwrite exactly as existing gate tests resolve them (e.g. line 763). The "reuse helper then overwrite result.json/transcript" plan is workable.
- The planner's `_coerce_task_status("pass_recovered")` → `TaskStatus("pass_recovered")` → `TaskStatus.PASS_RECOVERED` (planner.py:339–344; enum value `"pass_recovered"` at models.py:50), so overwriting result.json to `pass_recovered` produces the exact exemption-guard predicate `lc.persisted_status is TaskStatus.PASS_RECOVERED`. Workable.
- Step 4.3 transcript `"partial work, killed mid-task\n"`: no `{`-prefixed line ⇒ `result_event is None` ⇒ `_classify_transcript` returns `INCOMPLETE`; with persisted ordinary `pass` it routes through the Opt-2a `else` branch where `INCOMPLETE.is_success` is False ⇒ `validated_last False`. Workable, GREEN before and after.

**MINOR finding (FIXED in-place):** As originally written, Step 4.2/4.3 listed `_build_gate_fixture → overwrite result.json/transcript → run BoundaryIntegrityGate().run(plan)` but did NOT define `plan` in the step list, nor make explicit that the overwrites must precede `ResumePlanner().plan(index)` (the plan reads result.json + transcript at plan/run time). A literal execution of the original steps risked building the plan before the overwrites (stale `pass`/`PASS_TRANSCRIPT`), silently defeating the test intent. **Fix applied:** inserted an explicit load-bearing ORDERING note into both Step 4.2 and Step 4.3 in `test-site-inventory.md` (sequence: build fixture → overwrite(s) → `plan = ResumePlanner().plan(index)` → `report = BoundaryIntegrityGate().run(plan)`), plus the `_coerce_task_status` mapping note and the "no result.json overwrite needed in 4.3" clarification.

---

## 3. NO-EDIT BOUNDARIES verification (no-edit-boundaries.md)

| # | Discovery claim | Worktree ground truth | Result |
|---|---|---|---|
| 1 | `TaskStatus.is_success` returns membership in `(PASS, PASS_RECOVERED)` | models.py:56–58 `return self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)` | PASS |
| 2 | `TaskStatus.PASS_RECOVERED = "pass_recovered"` | models.py:50 | PASS |
| 3 | `_classify_transcript` never returns `PASS_RECOVERED` | rerun_tasks.py:547–593 — only returns `PASS / FAIL_RECOVERABLE / FAIL_TERMINAL / INCOMPLETE`; no `PASS_RECOVERED` branch exists | PASS |
| 4 | `derived is not None and derived.is_success` ≡ `derived is TaskStatus.PASS` on the non-recovered path | On the `else` branch persisted_status ≠ PASS_RECOVERED by construction; `_classify_transcript` can return only PASS/FAIL_RECOVERABLE/FAIL_TERMINAL/INCOMPLETE; of these only `PASS.is_success` is True ⇒ `derived.is_success` ⟺ `derived is PASS`. Behaviorally identical today. | PASS |
| 5 | `BoundaryTask.derived_status` exists (Signal B), report-visible | resume/models.py:49 `derived_status: TaskStatus | None = None  # Signal B`; surfaced via `_blocking_reasons` `derived={s.derived_status}` at integrity.py:425 (within claimed 421–428) | PASS |
| 6 | `derived_status` interpolation cited at integrity.py:421–428 | `derived={s.derived_status}` at line 425; the `for s in report.suspects` block spans 421–427 | PASS |
| 7 | `discover_failed_tasks_from_transcripts` consumes `_classify_transcript` (rerun_tasks.py:596–625) | `def` at 596; calls `_classify_transcript(text)` at 623 | PASS |
| 8 | Net no-edit rule: modify ONLY `integrity.py` (Signal B) + `tests/sprint/test_resume.py`; leave models.py (both), rerun_tasks.py, executor unmodified | Consistent with the localized Opt-2a design; the exemption branches on `lc.persisted_status` inside integrity.py before/around the `_classify_transcript` call, requiring no shared-surface edits | PASS |

All no-edit boundary facts confirmed. The "Opt-2b rejected because it spills into `discover_failed_tasks_from_transcripts`" rationale is sound — that function does call the shared classifier (line 623), so widening it would change rerun discovery.

---

## 4. VALIDATION / PR READINESS verification (research/03, research/04)

| # | Required element | Where reflected | Result |
|---|---|---|---|
| 1 | UV-only; no `python -m` | research/03 §2.5 + §3.1 explicitly forbid `python -m`; compile uses `uv run python -c "import py_compile; py_compile.compile('<path>', doraise=True)"` | PASS |
| 2 | py_compile checks (python-m-free shape) | research/03 §2.5/§3.1; research/04 R1 carries the genuine-RED requirement | PASS |
| 3 | `uv run pytest tests/sprint/ -q` | research/03 §3.1 | PASS |
| 4 | `uv run ruff check src/ tests/` | research/03 §3.1 + §3.2 (separate gate) | PASS |
| 5 | `uv run ruff format --check src/ tests/` | research/03 §3.1 + §3.2 (separate from `make lint`, per memory) | PASS |
| 6 | Fork PR discipline — push origin only; `gh pr create --repo IronbellyOrg/IronClaude`; verify URL owner | research/03 §2.1–§2.2 (verbatim CLAUDE.md rules + mandatory command shape) | PASS |
| 7 | No `.claude/` staging (except settings.json) | research/03 §2.3 (verbatim prohibition + `-f` siren) | PASS |
| 8 | Baseline-failure attribution to documented node only | research/03 §3.3 (`tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase`) | PASS |
| 9 | Phasing supports discovery→edit→RED/GREEN→validation→rf-qa gate→PR→closeout | research/03 §5 recommended phase plan | PASS |

Validation command set and fork PR discipline are reflected well enough to proceed.

---

## Summary

- Checks passed: 4 / 4 sections (38 / 38 itemized claims verified)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 1 (MINOR — Step 4.2/4.3 overwrite-vs-plan ordering ambiguity in `test-site-inventory.md`)

## Issues Found

| # | Severity | Location | Issue | Resolution |
|---|----------|----------|-------|------------|
| 1 | MINOR | `test-site-inventory.md` Step 4.2 / 4.3 | Step list referenced `plan` without defining it and did not mandate overwrites-before-`ResumePlanner().plan(index)`; literal execution could build the plan over stale `pass`/`PASS_TRANSCRIPT`, defeating the test intent | FIXED in-place: added explicit load-bearing ORDERING note (build fixture → overwrite(s) → build plan → run gate) + `_coerce_task_status` mapping note + "no result.json overwrite needed in 4.3" |
| 2 | INFO (not fixed) | `research/01` §1/§Summary | Base commit framed as PR "#126"; actual commit at SHA `02949fb3` is "#136" | Left as-is: SHA prefix + file content both verify; provenance note is non-load-bearing. `source-site-inventory.md` itself correctly says only `02949fb3` |

## Actions Taken

- Fixed Step 4.2 and Step 4.3 in `test-site-inventory.md` to make the overwrite-before-plan ordering explicit and to document the `pass_recovered` → `TaskStatus.PASS_RECOVERED` coercion path. Verified the edit applied (Edit returned success).

## Recommendations

- Proceed to source edit (Phase 3). The Signal B replacement code in `source-site-inventory.md`/`research/01 §2` is correct and applies cleanly to integrity.py:127–131 with artifacts/verdict untouched.
- When building Step 4.2/4.3 test items, follow the now-explicit ordering note (overwrite result.json/transcript BEFORE `ResumePlanner().plan(index)`).
- Keep the existing `test_gate_hard_stops_on_last_completed_overclaim` unchanged (it remains FR-2.4 coverage).

---

## Confidence Gate

**Confidence:** "Verified: 38/38 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
**Tool engagement:** "Read: 11 | Grep: 0 | Glob: 0 | Bash: 4" (Grep performed via Bash `grep`; no web research required — all claims were local-source-truth, so no Tavily/WebSearch invoked)

Every itemized claim above maps to a specific worktree Read or Bash `grep`/`sed` verification:
- integrity.py Signal B / Signal A / artifacts / verdict / `_read_transcript` / `_blocking_reasons` — Read (offsets 85–164, 415–434) + `sed -n '131p'`
- models.py `TaskStatus` / `is_success` — Read (40–74)
- resume/models.py `BoundaryTask.derived_status` — Read (30–64)
- rerun_tasks.py `_classify_transcript` / `discover_failed_tasks_from_transcripts` — Read (540–629)
- planner.py `_coerce_task_status` / persisted_status — Read (339–363) + grep
- test_resume.py constant / positive test / `_build_gate_fixture` / TestInvariants — Read (30–44, 142–261, 680–779)
- branch / base commit / no-edit-yet state — Bash git/sed/grep

No item was marked VERIFIED on the basis of another report; all were independently re-read from the worktree.

## QA Complete

VERDICT: PASS
