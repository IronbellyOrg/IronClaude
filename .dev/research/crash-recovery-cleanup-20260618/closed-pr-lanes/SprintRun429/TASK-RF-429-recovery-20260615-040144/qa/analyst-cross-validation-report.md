# Cross-Validation Report — Sprint 429 Recovery Research

**Analysis type:** completeness-verification (cross-validation lens)
**Date:** 2026-06-15
**Files analyzed:** 6 (01-file-inventory, 02-patterns-conventions, 03-integration-points, 04-data-flow-tracer, 05-test-verification, 06-template-examples)
**Driving spec:** `.dev/brainstorms/sprint-429-recovery-spec.md`
**Lens:** Cross-validate claims BETWEEN research files; flag contradictions, conflicting line numbers, divergent symbol descriptions.
**Source verification:** Contested overlaps were tie-broken by Reading the actual source (`monitor.py`, `process.py`, `pipeline/process.py`, `executor.py`, `models.py`, `rerun_tasks.py`, `resume/planner.py`).

---

## VERDICT: PASS

All 7 designated overlap points were adjudicated against source. The research set is **cross-consistent on every load-bearing symbol after source tie-break**. The single genuine cross-file divergence (overlap #1, the LAST-result-event parse mirror) is **not an unresolved contradiction** — R1 itself documents the correct underlying mechanic and flags the name discrepancy; R5 explicitly corrects the symbol name with a source citation; the spec's own name (`count_turns_from_stream_json`) matches R2/R4/R5 and the source. The disagreement is over which *symbol to cite as the canonical mirror*, and the source docstring resolves it unambiguously. No conflicting line number survives source verification. No shared dependency is described inconsistently in a way that would mislead the builder.

The two "CORRECTION/FINDING" items that R3 and R4 raise against the **spec** (not against each other) are real, mutually consistent, and converge on the same resolution. They are correctly surfaced as build-time decisions, not silently resolved.

---

## Overlap Adjudication (7 points)

### Overlap #1 — LAST-result-event parse mirror — RESOLVED (source-verified)

**Positions:**
- R1 (01-file-inventory L25, L214): the new detector should mirror `count_turns_from_output` (`monitor.py:223`) and, for per-line `json.loads`, `OutputMonitor._process_chunk` (`monitor.py:389`). R1 *also* explicitly notes (line 214, "Name correction") that the spec/research-notes name `count_turns_from_stream_json` and that the actual monitor.py symbol is `count_turns_from_output`.
- R2 (02-patterns L45, L189), R4 (04-data-flow L39), R5 (05-test L464): the canonical LAST-result-event mirror is `count_turns_from_stream_json` at **`process.py:32-76`** — explicitly "in process.py, NOT monitor". R5 states the spec's `count_turns_from_stream_json` name is correct *for that function* but that `monitor.count_turns_from_output` is a different semantic.

**Source tie-break (verified this pass):**
- `monitor.py:37` `detect_error_max_turns`, `monitor.py:223` `count_turns_from_output`, `monitor.py:253` `class OutputMonitor`.
- `src/superclaude/cli/sprint/process.py:32` `count_turns_from_stream_json` — parses the LAST `{"type":"result"}` event.
- The `count_turns_from_stream_json` **docstring itself** (process.py:42-50) states: *"Two distinct turn-count contracts exist in this package — keep them straight: `count_turns_from_stream_json` (HERE) → the Claude-reported `num_turns` from the terminal result event … `monitor.count_turns_from_output` → counts `"type":"assistant"` lines (a different and less-authoritative semantic)."*

**Resolution:** R2/R4/R5 are correct. The function that "parses the LAST `{"type":"result"}` event" — which is exactly what the spec (§4 Layer 1 L140-141) asks the new detector to mirror — is `count_turns_from_stream_json` (`process.py:32-76`), NOT `count_turns_from_output` (`monitor.py:223`, which counts assistant lines). R1's top-line symbol citation diverges, but R1's *mechanic* guidance is still sound: it correctly says the new core must `json.loads` the LAST result line and cites `_process_chunk:389` as a valid in-class JSON-parse idiom. This is a **citation-quality divergence, not a contradiction that would mislead the builder**, because (a) R1 flags the name issue itself, (b) R5 corrects it with a source citation, (c) the spec name matches the source.

**Builder action:** mirror `count_turns_from_stream_json` (`process.py:32-76`) for the LAST-result-event location; the read/OSError/empty-guard wrapper still mirrors `detect_error_max_turns` (`monitor.py:37-61`) per R2 Pattern A. Do NOT mirror `count_turns_from_output` for the result-event semantic. Consistency rating: **CONSISTENT after source tie-break** (R1's name is the outlier and is self-flagged).

### Overlap #2 — Diagnostic-bundle hazard (executor.py:2103) — RESOLVED, R3 ⇄ R4 AGREE

**Positions:**
- R3 (03-integration IP-3, "CORRECTION"): `:2103` (`if status.is_failure:`) DOES run `DiagnosticCollector` + `FailureClassifier` + writes `phase-N-diagnostic.md`; it is NOT "only halts." BUT the per-task path `continue`s at `:1781` and never reaches `:2103`, so the per-task `FAIL_PROVIDER_EXHAUSTED` does not trip the bundle. Only the single-session `PhaseStatus.is_failure` path does. Recommends option **B1** (add to `is_failure` + one-line guard at `:2103`) or **B2** (don't add to `is_failure`, add explicit halt branch). Both require adding to `is_terminal`.
- R4 (04-data-flow FINDING F-1): identical finding. Spec's "no auto-remediation consumer / only halts" is TRUE for per-task `TaskStatus.is_failure` but FALSE for single-session `PhaseStatus.is_failure` at `:2103-2128`. Resolution: put `PROVIDER_EXHAUSTED` in `is_terminal` not `is_failure`, OR guard the `:2103` block. Requires a test asserting no `phase-N-diagnostic.md` is written.

**Source tie-break (verified this pass):** `executor.py:2103` `if status.is_failure:` → `DiagnosticCollector(config)` → `collector.collect(...)` → `FailureClassifier()` → `reporter.write(bundle, phase-{N}-diagnostic.md)` → `SprintOutcome.HALTED` + `break`. Confirmed verbatim. Confirmed per-task path `continue`s at `:1781` (verified) before reaching `:2103`.

**Resolution:** R3 and R4 are in **full agreement** with each other AND with the source. Both correctly identify the spec's imprecision (the spec §4 Layer 2 L191-196 says "no auto-remediation consumer … only halts"). Both converge on the same two-option resolution (guard the bundle or keep out of `is_failure`; either way add to `is_terminal`). R3 leans B1, R4 lists both equivalently — this is a *recommendation emphasis*, not a contradiction; both options are listed by both researchers. Consistency rating: **FULLY CONSISTENT**. The finding against the spec is correctly surfaced as a P4 build decision, not silently resolved.

### Overlap #3 — cmd/env assembly location — RESOLVED, R3 correct over spec/R1

**Positions:**
- Spec §0 + R1 (implicitly, via spec citations): subprocess cmd `claude --print … [--model M]` and `env_vars` merges into `os.environ.copy()` at `sprint/process.py:129-141`.
- R2 (02-patterns L216, "Verified directly … process.py:32-131") and R3 (03-integration IP-9, "CORRECTION"): the cmd/env assembly is in the **pipeline base** `src/superclaude/cli/pipeline/process.py` (`build_command:121-143`, `build_env:145-160`), NOT `sprint/process.py:129-141`. The sprint subclass `ClaudeProcess.__init__` (`sprint/process.py:137-164`) only passes `model=config.model` (`:162`) up to the base.

**Source tie-break (verified this pass):**
- `sprint/process.py`: NO `os.environ.copy`, NO `--no-session-persistence`, NO `build_command`/`build_env` (grep returned empty). `ClaudeProcess(_PipelineClaudeProcess)` `__init__` passes `model=config.model`.
- `pipeline/process.py:121` `build_command`, `:132` `--no-session-persistence`, `:145` `build_env`, `:155` `os.environ.copy()`. Confirmed.

**Resolution:** R3 (and R2) are correct; the spec/R1 citation `sprint/process.py:129-141` is wrong for the cmd/env assembly — those lines are the subclass `__init__` region, and the actual assembly lives in the pipeline base. R3 explicitly flags this as a correction to spec/research-notes. Because R3 carries the authoritative corrected citation and marks process.py as ZERO-EDIT (read-only consumed), the builder is not misled. Consistency rating: **CONSISTENT** (spec citation corrected by R3 with source evidence; no two research files contradict each other).

### Overlap #4 — `_run_one_task` call sites + lock values — RESOLVED, R2 ⇄ R3 AGREE

**Positions:**
- R2 (02-patterns Pattern E, L161-163): K>1 at `executor.py:1134-1145` passes `lock=lock`; K=1 at `executor.py:1337-1348` passes `lock=None`.
- R3 (03-integration IP-1): K>1 at `:1134-1145`, `lock=lock` (`:1144`); K=1 at `:1337-1348`, `lock=None` (`:1347`).
- R4 (04-data-flow §3 L100): K>1 at `:1144` with the real lock; K=1 at `:1347` with `lock=None`. Same.

**Source tie-break (verified this pass):** K>1 block `:1134-1145` ends `lock=lock,`; K=1 block `:1337-1348` ends `lock=None,`. Both confirmed verbatim.

**Resolution:** R2, R3, R4 are in **exact agreement** with each other and the source — identical line ranges, identical lock values. Consistency rating: **FULLY CONSISTENT**. The builder consequence (thread the new `reset_policy` at BOTH sites) is stated identically by R2 (L163) and R3 (IP-1 EDIT notes).

### Overlap #5 — `TaskResult.from_dict` hard-keyed back-compat — RESOLVED, R1 ⇄ R2 ⇄ R5 AGREE

**Positions:**
- R1 (01-file-inventory FILE 2 L77): result-level fields are HARD-KEYED (`data["status"]` L231 … `data["output_path"]` L239); nested `task` sub-dict uses `.get()`. New fields MUST use `.get(default)`.
- R2 (02-patterns Pattern D): `TaskResult.from_dict` HARD-KEYED (`models.py:231-239`, bare `data[...]`); contrasts with `HandoffRecord.from_dict` (`:337-349`, `.get()` every field). New fields must imitate HandoffRecord.
- R5 (05-test §7 L290, citations L468): `TaskResult.from_dict` hard-keyed today (`models.py:218-240`); new fields need `.get()`; authors both-direction back-compat tests.

**Source tie-break (verified this pass):** `from_dict` (`:218-240`): nested `task` uses `task_data["task_id"]`/`["title"]` (hard) + `.get()` for description/dependencies/command/classifier; result-level `status`/`turns_consumed`/`exit_code`/`started_at`/`finished_at`/`output_bytes`/`gate_outcome`/`reimbursement_amount`/`output_path` are ALL bare `data[...]` subscripts. Confirmed.

**Resolution:** R1, R2, R5 are in **exact agreement** with each other and the source. R2 adds the valuable detail that `HandoffRecord.from_dict` (`:337-349`) is the in-file `.get()` exemplar to copy — complementary, not contradictory. Consistency rating: **FULLY CONSISTENT**.

### Overlap #6 — process.py / resume/planner.py ZERO-EDIT — RESOLVED, R1 ⇄ R3 ⇄ R4 AGREE

**Positions:**
- R3 (03-integration IP-8, IP-9): planner is ZERO-EDIT (`_coerce_task_status` DEF `:339` auto-resolves `TaskStatus(value)`; `rerun_task_ids` `:160-164` filter `not is_success` auto-includes the new status; hard-crash fallback routes through `_classify_transcript`). process.py ZERO-EDIT (`--model` + env inherited, read-only). R3 notes the planner CALL is at `:157`, DEF at `:339` (research-notes cited `:157`).
- R1 (01-file-inventory): scope is monitor/models/recovery_policy/aienv/scripts.ic — does NOT list process.py or planner.py as modify targets (implicit zero-edit; consistent).
- R4 (04-data-flow §6 "Resume routing"): no planner edit needed; `FAIL_PROVIDER_EXHAUSTED` in `is_failure` → `not is_success` True → re-run; `_coerce_task_status → TaskStatus(value)` auto-resolves; hard-crash fallback via `_classify_transcript`. Same conclusion.

**Source tie-break (verified this pass):** `resume/planner.py:160-164` filter `if bt.persisted_status is None or not bt.persisted_status.is_success`; CALL at `:157` `self._coerce_task_status(tr.get("status"))`; DEF `def _coerce_task_status` at `:339`. process.py base `--model` conditional at `pipeline/process.py:140-141` (per R3) and `os.environ.copy()` at `:155`. Confirmed.

**Resolution:** R1, R3, R4 agree (R1 by omission-from-scope, R3/R4 explicitly). R3's `:157` (call) vs `:339` (def) distinction is a *refinement* of the research-notes `:157` citation, not a contradiction with R1/R4 (neither of which cited a competing def line). The filter line range `:160-164` is consistent across R3 and R4. Consistency rating: **CONSISTENT**.

### Overlap #7 — `--max-session-resets` hop chain — RESOLVED, R1 ⇄ R3 ⇄ R5 AGREE

**Positions:**
- R3 (03-integration IP-10): 4-hop chain mirroring `--task-parallelism` — (1) `commands.py` `@click.option` (`:202-209` template), (2) `run()` param (`:234-258`), (3) `load_sprint_config` call (`commands.py:337-354`) + DEF (`config.py:281-298`), (4) `SprintConfig` field (`models.py`, `task_parallelism:int=1` at `:590` template). Default 8.
- R1 (01-file-inventory L220): `SprintConfig.model` (`:537`) and `index_path` (`:531`) consumed by the halt builder/suggester; `max_turns:int=100` (`:536`). R1 does not enumerate the flag chain (out of R1's file scope) but its `SprintConfig` field locations are consistent with R3's `models.py` touch point.
- R5 (05-test §9, citations L473): no existing `max_session_resets` refs (`grep … → 0`, net-new); doc⇆CLI parity must assert the flag in `sprint run --help` + guide. Default `8` stated in the guide. Consistent with R3's registration chain.

**Source tie-break:** Not re-Read line-by-line this pass (R3 marks the chain CONFIRMED; R5 confirms net-new via grep; the chain mirrors the verified `--task-parallelism` precedent). The default value **8** is consistent across spec §4/§8, R3 (IP-10), R4 (§4 budget table), R5 (§6.1 truth table cap=8). No conflicting default value appears anywhere.

**Resolution:** R1, R3, R5 are consistent — R3 owns the flag-chain detail, R1 owns the consumed `SprintConfig` fields, R5 owns the net-new + parity verification. The default `8` is unanimous. Consistency rating: **CONSISTENT**.

---

## Checklist Results

### (a) Cross-file consistency on the same symbols
- `count_turns_from_stream_json` vs `count_turns_from_output`: divergent citation in R1 vs R2/R4/R5; **resolved by source** — distinct functions with distinct semantics, the source docstring itself disambiguates. R1 self-flags the name. Not an unresolved contradiction.
- `_run_one_task` signature + call sites: identical across R2/R3/R4. PASS.
- `TaskResult.from_dict` hard-keying: identical across R1/R2/R5. PASS.
- `TaskStatus`/`PhaseStatus` enums + property tuples: R1/R2 agree; R1 adds the "PhaseStatus has THREE properties (`is_terminal`/`is_success`/`is_failure`)" correction — a *completeness add*, consistent with R2 Pattern C which also lists all three. PASS.
- `executor.py:2103` diagnostic bundle: R3 ⇄ R4 agree, source-confirmed. PASS.

### (b) No contradictory line numbers left unresolved
- `sprint/process.py:129-141` (spec/R1) vs `pipeline/process.py:121-160` (R2/R3): **resolved** — source confirms assembly is in pipeline base; R3 carries the corrected citation. Not left unresolved.
- `_coerce_task_status` `:157` (call, research-notes) vs `:339` (def, R3): **resolved** — both are correct for their respective roles; R3 disambiguates. Not a contradiction.
- `count_turns` line numbers: `monitor.py:223` (R1) vs `process.py:32-76` (R2/R4/R5) — different *files/functions*, both line numbers correct for their respective symbols; resolved by recognizing they are two functions. Not left unresolved.
- All other contested line numbers (call sites `:1134-1145`/`:1337-1348`, from_dict `:218-240`, planner `:160-164`, ladder `:999-1015`/`:1003`/`:1012`) are **identical** across the files that cite them and source-confirmed. PASS.

### (c) Shared dependencies described consistently
- `SessionResetPolicy`/latch threading via the existing `lock` param: R2 (Pattern E), R3 (IP-1), R4 (§3), R5 (§2) describe it identically (checked under lock, spawn unlocked, tripped under lock; storm bound `≤ cap+(K−1)`, `< K×cap`, NOT `≤ cap`). The "NOT `≤ cap`" trap is flagged identically by R2/R3/R4/R5. PASS.
- `_provider_failure_from_text` text-core shared between detector + `_classify_transcript`: R1 (FILE 1 item 5), R2 (Pattern A "text-core split"), R3 (IP-6), R4 (§2 "Offline ladder"), R5 (§4 loaders) describe the same factoring (text-accepting inner, path wrapper delegates, classifier calls inner on existing `text`). PASS.
- `_task_completed_before_overrun` reuse as the trailing-429 completion guard: R4 (§2, edge #1) gives the deepest analysis (`lines[:-1]` mechanics sound when terminal line is a 429); spec §4 Layer 4 + R3 (IP-1 INSERT POINT) agree on placement (below `:1003`, above `:1012`). PASS.
- The 6 fixtures: R5 (§3) authors them from spec §2 verbatim; field names (`api_error_status` for terminal, `error_status` for api_retry) match R4's field-name cross-check (§1) exactly. PASS.

### (d) Integration descriptions match
- Detector ordering ladder (success → error_max_turns/PASS_RECOVERED → provider-failure → transient → terminal): R3 (IP-1), R4 (§2), spec §4 Layer 4 — identical insertion point and ordering. PASS.
- `_classify_transcript` 429 branch placement (above `:582`, after `:580`): R3 (IP-6 EXACT INSERT POINT) and R4 (§2 "Offline ladder") agree; source-confirmed the `:580` `is_error` line and `:582` PASS branch exist. PASS.
- Persistence (`halt_reason`/`exhausted_model` to `_write_phase_result_json`; per-task vs single-session sourcing): R3 (IP-5) and R4 (§6) agree, including the per-task wrinkle (derive from `task_results[*].failure_class` since the per-task path collapses to `PhaseStatus.ERROR`). PASS.
- Recovery nominators `failure_class` exclusion (deferred to P6, `needs_human_decision`-adjacent): R3 (IP-7) corrects research-notes (no `DriftNominator`; only `Nominator`/`ManualNominator`/`ReflectReportNominator`) and marks `context` plumbing UNVERIFIED; R4 (§4) flags the same theme. Consistent. PASS.

---

## Spec-vs-Research Divergences (correctly surfaced, NOT silently resolved)

These are research findings against the **driving spec**, not contradictions between research files. Both relevant researchers agree on each:

1. **`is_failure` "no auto-remediation consumer" / "only halts" (spec §4 Layer 2 L191-196) is imprecise.** R3 (IP-3) + R4 (F-1) both prove `:2103` runs a diagnostic bundle for the single-session `PhaseStatus.is_failure` path. Source-confirmed. Resolution offered as a P4 build decision (guard `:2103` or keep `PROVIDER_EXHAUSTED` out of `is_failure`; add to `is_terminal` regardless). **Correctly surfaced.**
2. **cmd/env at `sprint/process.py:129-141` (spec §0) is the wrong location.** R2 + R3 place it in `pipeline/process.py:121-160`. Source-confirmed. **Correctly surfaced.**
3. **`count_turns_from_stream_json` lives in `process.py`, not `monitor.py`** (the spec §4 L141 says "mirror `count_turns_from_stream_json`" without a file; R1 conflated it with `monitor.count_turns_from_output`). R2/R4/R5 + source docstring resolve it. **Correctly surfaced.**
4. **`aienv.py` design choice** (os.environ reader vs file parser; spec says "parse `~/.aienv`" but no Python in-repo parses the file). R1 (FILE 4) flags as `needs_human_decision`-adjacent with a recommended default + documented fallback. R5 (§8.2) notes the test assumes an injectable `aienv_path`. Consistent treatment. **Correctly surfaced, not auto-resolved** (aligns with `feedback_human_decision_items_must_halt`).
5. **`IC_ALIASES` token is Unverified** (R1 FILE 5; the real mechanism is per-token `export <name>=<model>` + `IC_PRESET_<name>`). R5 (§8.2) echoes the uncertainty and tells the builder to confirm the real format. Consistent.

---

## Minor Notes (non-blocking)

- **R2 status field:** `02-patterns-conventions.md` opens with `**Status:** In Progress` (line 2) but closes with `## Status: Complete` (line 205). The body is complete (full summary, citations, Unverified list). Treat as Complete; the stale header is cosmetic and does not affect cross-validation. (Flagging per completeness-check item 4.)
- **R1 PhaseStatus property count correction** (THREE properties, not the member-add only) is a valuable completeness add over the research-notes; it is consistent with R2 Pattern C and does not conflict with any other file.
- **R3 nominator correction** (no `DriftNominator`) and **R3 `_coerce_task_status` DEF/CALL** distinction are corrections to *research-notes*, not to peer research files; no peer file asserts the contradicted claim, so there is nothing to reconcile.
- Every researcher independently flags the **`≤ cap+(K−1)` / NOT `≤ cap`** storm-bound trap and the **`subtype:"success"` trap** — strong convergence on the two subtlest correctness hazards.

---

## Unresolved Contradictions

**None.** All 7 designated overlaps are consistent after source tie-break. The lone cross-file citation divergence (overlap #1) is self-flagged by R1, corrected by R5 with a source citation, matches the spec name, and is unambiguously resolved by the source docstring that explicitly warns about the two-function confusion. No conflicting line number survives verification. No shared-dependency description would mislead the builder.

---

## Status: COMPLETE
**VERDICT: PASS**
