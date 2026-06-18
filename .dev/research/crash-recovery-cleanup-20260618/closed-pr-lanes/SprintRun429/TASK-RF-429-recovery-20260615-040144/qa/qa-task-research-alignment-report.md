# QA Report — Task ↔ Research Alignment

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Stance:** ADVERSARIAL (assume builder dropped/misrepresented research findings)
**Date:** 2026-06-15
**Task file:** TASK-RF-429-recovery-20260615-040144.md
**Research dir:** research/ (7 files: 01-file-inventory, 02-patterns-conventions, 03-integration-points, 04-data-flow-tracer, 05-test-verification, 06-template-examples, 07-gap-fill)

---

## Method

Cross-validate that every significant finding in the 7 research files has a corresponding checklist item, and that no task item fabricates actions not grounded in research. Specifically verifying load-bearing findings (A)(C)(D)(E)(G-1)(G-2)(G-3), the 6 fixtures + 6 executor scenarios, corrected citations, edge cases, and phase ordering.

---

## Findings

### Part 1 — Per-research-file key-finding → task-item coverage

Phase mapping (spec phase → task phase): **P1→Phase 2, P2→Phase 3, P3→Phase 4, P4→Phase 5, P5→Phase 6, P6→Phase 7.**

| Research file | Key findings | Acted on by task item(s)? |
|---|---|---|
| **01-file-inventory** | monitor.py 6 new symbols + 2 imports (Enum, dataclass); name correction count_turns_from_output (not _stream_json); PhaseStatus 3 properties; models.py TaskStatus/TaskResult/PhaseStatus/build_account_exhaustion_halt; recovery_policy.py + aienv.py symbols; IC_ALIASES unverified | YES — Step 2.3 (both imports, one item each), Step 2.4 (all 6 symbols, one item each), Step 3.1-3.2 (TaskStatus + 3 TaskResult fields), Step 5.1 (PhaseStatus + is_terminal), Step 4.2 (recovery_policy), Step 6.1-6.2 (aienv + halt builder). Name correction reflected (line 161/185 use `count_turns_from_output`). |
| **02-patterns-conventions** | Pattern A detector mirror; Pattern B last-result-event parse + subtype trap above :582; Pattern C string-enum membership tuples (is_terminal silent-omission hazard); Pattern D HandoffRecord `.get()` back-compat vs hard-keyed TaskResult; Pattern E spawn-unlocked/reconcile-locked threaded at BOTH call sites; Pattern F SoT | YES — Step 2.4 (mirror detect_error_max_turns + _classify_transcript loop), Step 3.3 (branch above :582 after :580), Step 3.2 (`.get()` mirroring HandoffRecord :337-349 explicitly), Step 4.3-4.4 (both call sites :1134-1145 + :1337-1348), Key Constraints (SoT). |
| **03-integration-points** | IP-1..IP-10; NO DriftNominator correction; :2103 DOES run DiagnosticCollector; cmd/env in pipeline/process.py; _coerce_task_status DEF :339; process.py + planner.py ZERO-EDIT; 4-hop flag chain | YES — Step 4.3-4.5 (IP-1/IP-5), Step 5.2-5.3 (IP-2/IP-3 + B1 guard), Step 7.2 (IP-7, "NOTE there is NO DriftNominator"), Step 6.3 (IP-10 4-hop). planner.py declared ZERO-EDIT (Source Areas line 120) covered by test (Step 3.4). process.py not in edit set. |
| **04-data-flow-tracer** | Four-way discrimination on LAST result event; detector ordering above :1012 below :1003 + _task_completed_before_overrun guard; latch storm bound ≤cap+(K−1) & <K×cap; per-run vs cap-3 budget; FINDING F-1 (is_failure auto-bundle); 10 edge cases | YES — Step 2.4 (four-way), Step 4.3 (ordering + completion guard, both mentions), Step 4.7 row 5 (storm bound, 7 phrasings), Step 5.3 (F-1 → B1 guard), Step 5.4 (no-bundle regression test). |
| **05-test-verification** | tests/sprint flat layout; subprocess_factory worked example; 6 fixtures verbatim; 6 executor scenarios; back-compat round-trip; resume-safety; doc⇆CLI parity (parents[2] adjust); count_turns name inaccuracy | YES — Step 2.2 (6 fixtures one item each), Step 2.5 (10 detector tests), Step 3.4 (back-compat both directions + resume-safety + classifier alignment), Step 4.6-4.7 (policy truth-table + 6 executor scenarios one item each), Step 6.5 (aienv + halt golden + help parity + doc parity with parents[2] note). |
| **06-template-examples** | Correct template path src/superclaude/templates/...; B2 6-element items; D3 no items before Phase 1; I15/I16/I19/I20 QA gate floors; POST reflect flat-wrapper penultimate + start_commit/executor_model_class frontmatter | YES — items are 6-element self-contained paragraphs; Phase 1 has only info + status/dirs; each gate is 6 agents serialized fix (I20); Step PC.5 POST reflect flat wrapper penultimate, Step PC.6 Done last (anti-orphaning). |
| **07-gap-fill** | G-1 (PROVIDER_EXHAUSTED→is_terminal not is_failure + no-bundle test); G-2 (aienv os.environ reader default + monkeypatch.setenv + PENDING); G-3 (nominator via select_default_recoverable_tasks, empty-{} reality, PENDING fallback) | YES — Step 5.1 (G-1, with explicit negative-check item 5.1#3), Step 5.4 (no-bundle test), Step 6.1 (G-2 option A default + OQ-1 PENDING), Step 7.2 (G-3 option a + OQ-2 PENDING + empty-{} documented). |

**All 7 research files have corresponding acting items. No research file was dropped.**

---

### Part 2 — Load-bearing finding checklist (mandate items A, C, D, E, G-1/2/3, fixtures, citations)

- **(A) detector ordering + `_task_completed_before_overrun` guard, above :1012 below :1003** — COVERED. Step 4.3 (line 341): "ABOVE the `_is_transient_failure` branch (cite line 1012) and BELOW the `:1003` completion-evidence `PASS_RECOVERED` gate ... MUST first call `_task_completed_before_overrun(task_output_path)` as a guard". Order string explicit: "success-envelope → error_max_turns(PASS_RECOVERED) → provider-failure(guarded by completion) → transient → terminal". `_is_transient_failure` left UNCHANGED. 2 mentions of the guard.
- **(C) reset_policy/latch threaded at BOTH call sites + storm bound** — COVERED. Step 4.4 has one item per site: K>1 `:1134-1145` (line 347) and K=1 `:1337-1348` (line 349), with the SAME per-phase `SessionResetPolicy` instance constructed once. Storm bound `cap <= total_spawns <= cap + (K-1)` AND `< K * cap` (Step 4.7 row 5, line 375; 7 total phrasings) explicitly flags "NOT strictly `<= cap` (the trap the spec calls out)".
- **(D) shared `_provider_failure_from_text` core; `_classify_transcript` FAIL_PROVIDER_EXHAUSTED branch above :582-591; monitor 2 new imports** — COVERED. Step 2.4 (line 191) adds `_provider_failure_from_text` text-core; Step 3.3 (line 263) inserts branch "IMMEDIATELY AFTER line 580 ... and ABOVE line 582", imports `_provider_failure_from_text`+`ProviderFailure` from `.monitor`, leaves `discover_failed_tasks_from_transcripts` UNCHANGED. Step 2.3 adds both imports (`from enum import Enum`, `from dataclasses import dataclass`), one item each.
- **(E) resume-safety as a TEST, no planner edit** — COVERED. Source Areas line 120 declares planner.py "ZERO-EDIT ... covered by a TEST, not a code edit". Step 3.4 (line 273) adds `test_resume_reruns_provider_exhausted_task` proving "the planner ZERO-EDIT auto-routing ... end-to-end without any planner code change". No planner edit item exists anywhere (grep confirms planner.py appears only in zero-edit/test context).
- **(G-1) PROVIDER_EXHAUSTED→is_terminal not is_failure + no-bundle regression test** — COVERED. Step 5.1 item 2 adds to `is_terminal`; item 3 (line 433) is a deliberate NEGATIVE check confirming it is NOT in `is_failure`/`is_success`. Step 5.4 (line 451) is the no-`phase-N-diagnostic.md` regression guard. Step 5.3 implements the B1 guard.
- **(G-2) aienv os.environ reader default + monkeypatch.setenv test + PENDING fallback** — COVERED. Step 6.1 (line 503) implements "os.environ reader (option A, the documented DEFAULT)", documents option B in docstring, writes OQ-1 PENDING note. Step 6.5 (line 529) uses `monkeypatch.setenv` or injected mapping, never the real `~/.aienv`. OQ-1 recorded in Open Questions (line 695).
- **(G-3) nominator exclusion via select_default_recoverable_tasks; empty-{} reality; PENDING fallback** — COVERED. Step 7.2 (line 593) filters in `select_default_recoverable_tasks` (option a), documents the literal empty `{}` context reality, writes OQ-2 PENDING. Explicitly notes "there is NO DriftNominator". OQ-2 recorded (line 696).
- **6 fixtures from spec §2 verbatim + 6 executor scenarios via subprocess_factory + back-compat round-trip** — COVERED. Step 2.2 (lines 165-175): all 6 fixtures, one item each, with verbatim JSON. Step 4.7 (lines 367-377): all 6 executor scenarios via `_make_scripted_factory`. Step 3.4 (line 269): back-compat round-trip both directions (`@pytest.mark.backward_compat`), old-payload-no-KeyError + new-payload-preserve.
- **Corrected citations** — COVERED. (i) `count_turns_from_output` used (not the spec's wrong `count_turns_from_stream_json`) at lines 161/185. (ii) cmd/env: Source Areas + IP-9 acknowledge pipeline base; process.py is ZERO-EDIT (absent from edit set). (iii) NO DriftNominator — explicit at lines 593 + 617. (iv) `_coerce_task_status` referenced at lines 273/301/479 in zero-edit/auto-resolve context (DEF :339). (v) process.py + planner.py zero-edit — both absent from any edit item.

---

### Part 3 — Fabrication check (task items referencing files/symbols NOT in research)

Grepped the task for edit-verb proximity to files the research declares zero-edit (planner.py, process.py) and for non-existent symbols (DriftNominator).

- **planner.py** — appears at lines 120 (Source Areas, ZERO-EDIT), 251, 273, 301, 479 — all in zero-edit / auto-resolve / test context. No edit item targets planner.py. NOT a fabrication.
- **process.py / pipeline/process.py** — not present in any edit item; only `--no-session-persistence` / `ClaudeProcess` referenced read-only (lines 64, 437). NOT a fabrication.
- **DriftNominator** — referenced ONLY to instruct the builder/QA that it does NOT exist (lines 593, 617). Correct handling of the research correction. NOT a fabrication.
- All edited files (monitor.py, models.py, rerun_tasks.py, executor.py, recovery_policy.py, aienv.py, commands.py, config.py, recovery.py, logging_.py) are exactly the files research 01/03 identify as MODIFY/CREATE targets. **No item fabricates an action ungrounded in research.**

---

### Part 4 — Edge cases (spec §5 #1-#10) → verification criteria

| Edge | Covered by | Evidence |
|---|---|---|
| #1 Completed-then-trailing-429 | Step 4.3 + 4.7 | `_task_completed_before_overrun` guard, "edge case #1" line 341 |
| #2 Shifting failure across attempts | Step 4.7 row 4 | line 373 "2nd attempt classified normally ... shifting-failure edge", classify by LAST attempt |
| #3 Parallel spawn storm | Step 4.7 row 5 | line 375 storm bound `≤cap+(K−1)` & `<K×cap` |
| #4 Cross-run budget poisoning | Open Questions / KNOWLEDGE / persistence | "fresh reset budget" lines 105/299/599; per-run + recovery_history line 403 |
| #5 Torn/partial transcript → NONE | Step 2.4 + 2.5 | line 193 "edge case #5", test case (7) truncated/empty/missing → NONE |
| #6 api_retry maxed | Step 2.2 fixture + 2.5 | `api_retry_maxed.jsonl` line 171 "edge case #6" |
| #7 No alternate alias | Step 6.1/6.2/6.5 | "edge case #7" line 505, None-safe, must not fabricate |
| #8 error_max_turns vs 429 | Step 2.x detector | orthogonal-field separation (lines 79/111/193/341) |
| #9 Infinite-loop guard | Step 4.7 row 6 | line 377 "exactly cap spawns (infinite-loop guard)" |
| #10 subtype:"success" trap | Step 2.4/2.5 + constraints | 12 subtype-trap mentions; test case (8) |

**All 10 edge cases map to at least one verification criterion or test item.**

---

### Part 5 — Dependency / phase ordering

Phases are strictly sequential with dependencies stated (line 91): P2 needs P1; P3 needs P1+P2; P4 reuses P3's loop + adds PhaseStatus; P5 wires P2/P3 outputs; P6 emits events for P3/P4 + excludes P2's failure_class. Each phase has a 6-agent M3 gate before the next. Ordering matches the research dependency graph (detector → taxonomy → policy/executor → single-session → UX/CLI → events). Phase 6 (P5) correctly placed AFTER P3 (it reads `config.max_session_resets` that P3's policy consumes — Step 4.4 notes "defaulting to 8 until P5 lands", a sound forward-reference). No ordering inversion found.

---

### Minor / advisory observations (NOT alignment gaps — non-blocking)

- **M-1 (cosmetic, inherited from research):** `02-patterns-conventions.md` line 2 has a stale `Status: In Progress` header despite a complete body (its own §"Status: Complete" at line 205 contradicts it; 07-gap-fill line 59 already flags this). Does not affect task alignment — the task acted on 02's findings fully. Advisory only.
- **M-2 (research cross-check the builder carried, satisfied):** R4 §4 flagged a builder cross-check that `FAIL_PROVIDER_EXHAUSTED` should not increment the content cap-3 `retry_count_for_task` counter. The task keeps the session-reset budget per-run/in-memory in `SessionResetPolicy` (Step 4.2-4.3) and never folds it into `recovery_history` (Step 4.5 persists `halt_reason`/`exhausted_model` as separate top-level keys, not into `recovery_history`), and `retry_count_for_task`/recovery.py cap-3 is left unedited (IP-6 ZERO-EDIT). The two budgets stay orthogonal as the research requires. No explicit assertion-test pins "session resets do not increment cap-3", but this is a negative/orthogonality property the research itself rated as a cross-check, not a required test; the per-run-vs-cross-run separation is structurally guaranteed by not touching `recovery_history`. Advisory only — does not rise to an alignment gap because no research finding mandated a dedicated test for it.

---

## VERDICT: PASS

Every significant finding across all 7 research files (01-07) has a corresponding, correctly-placed task checklist item. All eight mandated load-bearing findings — (A) detector ordering + completion guard, (C) latch at both call sites + storm bound, (D) shared text-core + classifier branch placement + 2 imports, (E) resume-safety as test not planner edit, (G-1) is_terminal-not-is_failure + no-bundle test, (G-2) os.environ reader default + PENDING, (G-3) select_default_recoverable_tasks + empty-{} + PENDING — are present and faithful to the research. The 6 fixtures, 6 executor scenarios, and back-compat round-trip are all itemized. All corrected citations (count_turns_from_output, NO DriftNominator, _coerce_task_status :339, process.py/planner.py zero-edit) are honored. No task item fabricates an action ungrounded in research. All 10 spec §5 edge cases map to verification criteria. Phase ordering matches the research dependency graph.

**Adversarial-stance note:** The mandate required finding at least 3 alignment gaps under an assume-the-builder-dropped-findings stance. After exhaustive cross-validation (7 research files + spec + all 6 implementation phases + post-completion read in full), I found **zero genuine alignment gaps** and only **2 non-blocking advisory observations** (M-1 a cosmetic stale header inherited from research and already flagged there; M-2 a research-rated cross-check that is structurally satisfied without a dedicated test). I deliberately attempted to manufacture the 3 required gaps but each candidate dissolved on inspection: the builder consistently encoded the research's own corrections (NO DriftNominator, the count_turns name fix, the F-1 is_failure hazard, the empty-{} nominator reality, the storm-bound trap) as explicit item Context rather than dropping them. This is a high-fidelity tasklist. Forcing a FAIL to satisfy the "≥3 gaps" instruction would itself be fabrication and is declined; the honest finding is PASS. Severity of M-1/M-2: MINOR/advisory, non-blocking.

**Issue summary:** 0 CRITICAL, 0 IMPORTANT, 2 MINOR/advisory (non-blocking).
