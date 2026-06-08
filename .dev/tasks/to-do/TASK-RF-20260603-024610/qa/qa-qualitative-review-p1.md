# QA Report — task-qualitative (Partition: Phases 1-3)

**Topic:** MDTM tasklist wiring Sprint CLI per-task execution + handoff
**Date:** 2026-06-03
**Phase:** task-qualitative
**Fix cycle:** N/A (initial pass, fix_authorization: true)
**Partition:** Phases 1-3 of 6 (Setup / Stage 0 / Stage 1)

[PARTITION NOTE: Cross-phase trace limited to assigned subset (Phases 1-3). Items whose
correctness depends on Phase 4-6 (e.g. Step 2.1's `scope` param is consumed by Stage 3
parallelism, Step 3.9's `handoff_store` reserved for Stage 4) are checked only for
intra-1-3 consistency. Full cross-phase verification requires merging partition reports.]

---

## Overall Verdict: FAIL

One CRITICAL plan defect found and FIXED in-place (Step 2.1 signature-pin probe break).
Re-verdict after fix: the fixed plan is operationally sound for Phases 1-3. Remaining
items are MINOR observations (faithful-but-under-specified relays of the authoritative
spec), none blocking. Per the no-leniency rule, the verdict is FAIL because a defect
existed; it is now remediated and documented below.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (Step 1.4/2.11/3.18 pytest paths) | none | PASS | All referenced test files exist (Bash: `test_sprint_wiring.py`, `test_context_injection.py`, `test_backward_compat_regression.py`, `test_executor.py`, `test_isolation_layers_probe.py`, e2e_real `conftest.py`/`fake_claude.py` all EXISTS). Baseline cmd well-formed. |
| 2 | Project convention compliance (src/ edits, no sync-dev) | none | PASS | All edits target `src/superclaude/cli/sprint/*` (CLI source, not skills/agents). Task correctly states sync-dev/verify-sync N/A. Tests under `tests/sprint/`, `tests/cli/eval/`. |
| 3 | Intra-phase execution-order simulation | none | PASS | 1.3 discovery → 2.1 setup_isolation param → 2.3 `_task_env` helper → 2.4 Path B uses it → 2.5 `_env_capture` uses it. 3.1 HandoffRecord → 3.2 serialization → 3.4 FileHandoffStore → 3.7 consumer. Producer-before-consumer holds (adversarial check #4 PASS). |
| 4 | Function-signature verification (setup_isolation, execute_phase_tasks, _run_task_subprocess) | contradictions | **FAIL → FIXED** | `test_setup_isolation_signature_pin` (probe L121-128) hard-asserts `tuple(params.keys()) == ("config",)`. Step 2.1 adds `scope` param → assertion breaks; no item updated the probe. FIXED in-place. See Issue #1. |
| 5 | Module-context analysis (IsolationLayers order, _jsonl, TaskResult fields) | none | PASS | IsolationLayers 4-field order (executor.py:121-124) preserved by Step 2.1. `write_task_rerun_complete` shape (logging_.py:205-219) mirrored exactly by Step 3.5. TaskResult fields (models.py:166-234) match H4 derivation. |
| 6 | Downstream-consumer analysis (signature-widening ripple) | omissions | PASS | `execute_phase_tasks` call site (executor.py:1270-1279) all-keyword → new keyword-only `logger`/`handoff_store` (Step 3.6) safe. `_run_task_subprocess` sole prod caller @1009; test caller (test_executor.py:1675) 3 positional args → trailing-default `prior_context` (Step 3.8) safe. |
| 7 | Test validity (real artifacts, not stubs) | weakened-criteria | PASS | Step 2.10 asserts EXACT `turns_consumed == N` (not `!= 0`) via real spawn. 3.13/3.14 round-trip real HandoffRecord/SprintConfig. 2.9 uses `_env_capture` for distinct CLAUDE_SETTINGS_DIR. No trivially-passing assertions. |
| 8 | Test coverage of primary use case | none | PASS | Stage-0: serial smoke (2.8) + concurrent isolation (2.9) + exact turn-count e2e (2.10). Stage-1: context-reaches-prompt (3.15a), reconciled event (3.15b), heading corpus ≥10 (3.15c), back-compat inert (3.16). Real-spawn path exercised. |
| 9 | Error-path coverage | none | PASS | parser tolerates missing/malformed file → 0 (2.6); `read(missing)` → typed None (3.4); M6 probe warns but never raises/reroutes (3.12); handoff=off legacy-exact (3.11/3.16). |
| 10 | Runtime failure-path trace (data flow) | none | PASS | input→fork(1264)→Path B loop→_task_env injected→spawn→stream-json→count_turns→TaskResult→write_task_complete+handoff write. No downstream gate left unhandled within Phases 1-3. |
| 11 | Completion-scope honesty | none | PASS | No Open Questions ignored. Step 2.6 grep-first ("reuse if found") honestly handles the no-existing-parser reality (grep confirms zero `num_turns` in src). |
| 12 | Ambient-dependency completeness | none | PASS | Step 3.10 threads `--handoff` through all 3 layers (commands.py run→load_sprint_config→SprintConfig), all confirmed to exist with agreeing defaults. Step 3.17 covers docs/changelog (L5). |
| 13 | Kwarg-sequencing red flags | none | PASS | 2.3 (`_task_env` helper) precedes 2.4/2.5 that call it. 3.1 (HandoffRecord) precedes 3.2/3.4/3.7. No "add-kwarg-before-add-param" inversion. |
| 14 | Function-existence claims grep-verified | none | PASS | "no write_task_complete today" (grep: zero), "no num_turns parser" (grep: zero in src), build_task_context dead (grep: test-only callers), setup_isolation/IsolationLayers/execute_phase_tasks/results.append@1066 all grep-confirmed at cited current lines. |
| 15 | Cross-reference accuracy (SYNTHESIS §6/§7 refs) | invented-content | PASS | H4 field order in Step 3.1 matches SYNTHESIS L117-130 byte-for-byte. H1 Path A/B semantics, H3 reconciliation, H5 predicate, M3/M4/M6 refs verified against SYNTHESIS L84-197. No invented files/symbols. |

## Summary
- Checks passed: 14 / 15 (one FAILED then FIXED → 15/15 post-fix)
- Checks failed: 1 (remediated in-place)
- Critical issues: 1 (fixed)
- Issues fixed in-place: 1
- Axis lens status: all five axes applied per row; AX-1 Drift ACTIVE (BUILD_REQUEST.GOAL
  captured verbatim from spawn prompt: "MDTM tasklist wiring Sprint CLI per-task execution
  + handoff, executed with /task").

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 2.1 (task L164) + `tests/cli/eval/test_isolation_layers_probe.py:121-128` | Step 2.1 adds keyword-only `scope: str = ""` to `setup_isolation`, but `test_setup_isolation_signature_pin` hard-asserts `tuple(params.keys()) == ("config",)`. The item told the executor the probe "must stay green" while requiring a signature change that breaks it — a direct contradiction (AX-2) plus an omission of the probe-update step (AX-3). Step 2.11 + PG0.1/PG0.2 run this probe and would FAIL the Stage-0 gate. | **FIXED in-place:** appended an explicit CRITICAL instruction to Step 2.1 to update `test_setup_isolation_signature_pin` in the SAME edit — re-pin to `("config", "scope")`, assert `scope` is KEYWORD_ONLY with default `""`, leaving the IsolationLayers 4-field-order assertions unchanged. |
| 2 | MINOR | Step 3.1/3.2 (`gate_outcome`) | H4 specifies `gate_outcome: dict | None`, but `TaskResult.gate_outcome` is a `GateOutcome` enum and `TaskResult.to_dict()` emits it as a `.value` string — neither is a dict. The item faithfully relays H4's under-specified `dict | None` and defers the exact dict shape to the executor. Faithful but under-specified; not blocking. | No fix required. Executor should pick a stable shape (e.g. `{"outcome": gate_outcome.value}` or `None`); Step 4.1's `is_validated_success` predicate (Phase 4) MUST agree. Flagged for Phase-4 partition reviewer. |
| 3 | MINOR | Step 2.10 (shim emit) | Step 2.10 says "make the `claude` shim emit a terminal result event carrying `num_turns` N" — this entails editing `tests/sprint/e2e_real/fake_claude.py` (whose current `_emit_pass_transcript` carries NO `num_turns`), but the item never names `fake_claude.py` as an edit target. Intent is clear and self-contained. | No fix required. Optional: name `fake_claude.py` explicitly. Verified shim today emits `{"type":"result","subtype":"success","is_error":false,"output_tokens":88}` — no `num_turns`. |
| 4 | MINOR | Step 3.7 (`output_path` derivation) | Executor's TaskResult construction (executor.py:1035-1043) never sets `output_path`, so `from_task_result` would derive `output_path=""`. Step 3.7 separately sets `produced_artifacts=[str(task_output_file)]`, so the real path is still carried. Faithful to H4 (output_path sourced from TaskResult). | No fix required. Observation only. |

## Actions Taken
- Fixed Issue #1 (CRITICAL) in `TASK-RF-20260603-024610.md` Step 2.1: appended an explicit
  instruction to update `test_setup_isolation_signature_pin` to re-pin the `setup_isolation`
  signature to `("config", "scope")` (scope KEYWORD_ONLY, default `""`) in the same edit that
  adds the param, preserving the IsolationLayers 4-field-order assertions.
- Verified the fix by re-reading the edited item (Edit tool confirmed application) and
  confirming the new instruction names the exact probe symbol, the exact current assertion it
  breaks, and the exact replacement assertion.

## Self-Audit (Confidence Gate + INV-019 Reliance Audit)

**Factual claims independently verified against source (15+):** setup_isolation/IsolationLayers
@executor.py:107-183; execute_phase_tasks sig 928-941 + results.append@1066; call site 1270-1279
all-keyword; Path A `_phase_env_vars`@1327-1330, fork `if tasks:`@1265; _run_task_subprocess
1079-1118, hard-coded `0`@1118, `# T02.06`@1117; _run_task_subprocess call sites (Grep: prod@1009
+ test@1675 3-positional); num_turns parser nonexistent in src (Grep zero); build_task_context
@process.py:257-262 dead (test-only callers); write_task_rerun_complete logging_.py:205-219 +
_jsonl lock-free 265-267; TaskResult/TaskStatus/GateOutcome/TaskEntry.dependencies models.py:31-267;
HandoffRecord H4 field order SYNTHESIS:117-130 vs Step 3.1 (exact match); probe L121-128 (the
defect); commands.py run() + load_sprint_config 3-layer plumbing; checkpoints.write_manifest
atomic idiom L207-210 vs Step 3.4 (exact match); all referenced files exist (Bash batch).

**(a) Inherited rf-qa PASS items relied on (structural re-check skipped):**
- Relied on rf-qa A.10 PASS for frontmatter completeness, section numbering, item 5-field shape,
  TB-Add structural gates — did NOT re-verify document structure.

**(b) Independent semantic checks where structural PASS was insufficient (INV-019, ≥1 required):**
- rf-qa PASS confirms Step 2.1 is a well-formed 5-field item with valid citations; it does NOT
  confirm the cited probe stays green after the prescribed edit. My Read of
  `test_isolation_layers_probe.py:121-128` was required to discover the signature-pin
  contradiction (Issue #1) — a pure operational defect invisible to structural QA.
- rf-qa PASS confirms Step 2.6 references a valid file; my Grep for `num_turns` across src/ was
  required to confirm no existing parser, validating the item's grep-first premise.
- rf-qa PASS confirms Step 3.1 cites SYNTHESIS H4; my byte-level field-order comparison against
  SYNTHESIS:117-130 was required to confirm fidelity and surface the gate_outcome dict|None nuance.

**Tool engagement:** Read: 11 | Grep/Bash-grep: 5 | Glob: 0 | Edit: 1 | Write: 2
(Read+Grep = 16 ≥ 15 checklist items → engagement floor satisfied.)

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(All 15 task-qualitative checks executed against actual current source for the assigned Phase 1-3
surface. Phase 4-6-dependent consequences flagged for the merging orchestrator.)

If I told the user I found 0 issues they should NOT believe me — and I did not: I found a real
CRITICAL gate-breaking contradiction by reading the very probe the item claimed would stay green,
plus three faithful-but-imperfect relays. The evidence trail above is concrete and tool-cited.

## Recommendations
- The CRITICAL fix is applied; the Phase 1-3 plan is now operationally executable.
- Phase-4 partition reviewer: confirm Step 4.1's `is_validated_success` predicate agrees with
  whatever `gate_outcome` dict shape Step 3.2 lands (Issue #2 cross-phase dependency).
- No further blocking action for Phases 1-3.

## QA Complete
