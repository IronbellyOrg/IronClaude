# Research: Data Flow Tracer

**Status:** Complete
**Date:** 2026-06-15
**Researcher:** R4 (Data Flow Tracer)
**Scope:** Runtime path of a 429 signal end-to-end: subprocess stdout → detector → policy → status → persistence → resume → halt UX. Both the per-task path and the single-session phase path. Four-way discrimination + detector ordering + global latch + reset budget + 10 edge cases.

---

## 0. End-to-end pipeline (one-line map, per path)

**Per-task path (K=1 sequential + K>1 parallel, both via `_run_one_task`):**

```
subprocess stdout stream-json file (config.task_output_file(phase,task))
  → [Design] detect_provider_failure(output_path) reads LAST {"type":"result"} event
  → [Design] SessionResetPolicy.decide(signal, attempt) → Action
  → Action RETRY_NEW_SESSION: re-spawn loop in _run_one_task (executor.py:986-993)
    | Action HALT_MODEL_SWITCH / cap-exhausted: TaskStatus.FAIL_PROVIDER_EXHAUSTED
    | Action CONTINUE: fall through to existing :1003/:1012/:1014 ladder
  → TaskResult(status, session_resets, failure_class, exhausted_model)  [Design fields]
  → result.status.is_failure (models.py:61) ⇒ resume re-runs it (planner.py:160-164)
  → halt UX: build_account_exhaustion_halt (Design, models.py)
```

**Single-session phase path (one `ClaudeProcess` per phase, NO `_run_one_task`):**

```
ClaudeProcess(config, phase, env_vars=…).start()  (executor.py:1815)
  → [Design] wrap in re-spawn loop BEFORE _determine_phase_status (executor.py:1993)
  → detect_provider_failure on config.output_file(phase) + SessionResetPolicy.decide
  → ALL_ACCOUNT_COOLDOWN / cap-exhausted ⇒ PhaseStatus.PROVIDER_EXHAUSTED [Design]
  → status.is_failure (models.py:437) gate at executor.py:2103
       ⚠ CONTRADICTION with spec — see Finding F-1 below
  → _write_phase_result_json adds halt_reason/exhausted_model (executor.py:2657) [Design]
  → SprintOutcome.HALTED + break (executor.py:2130-2132)
```

Evidence anchors verified this session: `_run_one_task` signature + spawn + ladder (executor.py:963-1015); K>1 call site lock-threaded (executor.py:1134-1145); K=1 call site lock=None (executor.py:1337-1348); single-session spawn (executor.py:1815) → `_determine_phase_status` (executor.py:1993) → `is_failure` diagnostic gate (executor.py:2103-2132); `_is_transient_failure` (executor.py:2267-2289); `_task_completed_before_overrun` (executor.py:2321-2387); `_classify_transcript` (rerun_tasks.py:547-593); `count_turns_from_stream_json` LAST-result-event parse (process.py:32-76 — **NOT monitor.py**); `detect_error_max_turns` last-line-only scan (monitor.py:37-61); TaskStatus/PhaseStatus enums + properties (models.py:46-66, 385-443).

---

## 1. The four-way discrimination table (decision crux)

All four are decided on the **LAST `{"type":"result"}` event** (spec §2 pinned predicates, line 86). The detector must mirror the `count_turns_from_stream_json` parse (process.py:59-69): iterate every line, `json.loads`, keep the last `event.get("type")=="result"`. It must **NOT** key on `subtype` (spec §2 line 70-72, edge #10) — `subtype=="success"` even when `is_error` is true.

| # | Category | Pinned predicate (spec §2:86-91, §4 table:277-282) | `ProviderFailure` (Design, monitor.py) | Policy `Action` (Design, recovery_policy.py) | Resulting status | Re-spawn? |
|---|---|---|---|---|---|---|
| 1 | **All-account cooldown** | `type=="result" && is_error==true && api_error_status==429` AND `result` matches `/All credentials for model (?P<model>.+?) are cooling down via provider/` | `ALL_ACCOUNT_COOLDOWN` (+ captures resolved model) | `HALT_MODEL_SWITCH` on **ANY** attempt incl. first (fast path) | per-task `FAIL_PROVIDER_EXHAUSTED` / phase `PROVIDER_EXHAUSTED` | **No** — 0 extra spawns |
| 2 | **Single-account limit** | `type=="result" && is_error==true && api_error_status==429` AND `result` contains `would exceed your account's rate limit` | `SINGLE_ACCOUNT_LIMIT` | `RETRY_NEW_SESSION` if `attempt < cap`, else `HALT_MODEL_SWITCH` | re-spawn; on cap → `FAIL_PROVIDER_EXHAUSTED` | **Yes**, bounded by cap |
| 2b | **429, body matches neither** | `is_error==true && api_error_status==429` AND neither regex | `SINGLE_ACCOUNT_LIMIT` (conservative default, spec §4:159) | `RETRY_NEW_SESSION` bounded by cap | re-spawn → cap → exhausted | **Yes**, bounded |
| 3 | **Operation timeout** | `is_error==true && api_error_status==null && result=="API Error: The operation timed out."` (spec §2:91) | `OPERATION_TIMEOUT` | `CONTINUE` (detector returns this kind, executor treats as non-exhaustion) | existing timeout path — **unchanged** | No (existing) |
| 4 | **Genuine task failure** | `is_error==true`, substantive tokens, **no** 429 body, `api_error_status` not 429 | `NONE` | `CONTINUE` | existing `FAIL_TERMINAL` (tokens>0) / `FAIL_RECOVERABLE` (tokens==0 / transient markers) at executor.py:1012-1015 | No (existing) |

**Field-name cross-check (spec §2 pinned predicates — these exact names matter):**
- Load-bearing terminal event field is **`api_error_status`** (spec §2:69-72), NOT `subtype`. Verified: `_classify_transcript` currently reads `result_event.get("subtype")` and `result_event.get("is_error")` (rerun_tasks.py:579-580) — it does **not** yet read `api_error_status`, so today a 429 is invisible to it and falls to FAIL_TERMINAL/FAIL_RECOVERABLE (spec §0:34, confirmed at rerun_tasks.py:582-591).
- The CLI's own in-session retry event uses a **different** field name: **`error_status`** (spec §2:63-64) on `{"type":"system","subtype":"api_retry"}`, with `attempt` and `max_retries:10`. Do NOT confuse `error_status` (api_retry) with `api_error_status` (terminal result). Edge #6 keys on `attempt==max_retries==10` from this event.
- Operation timeout is `api_error_status==null` (spec §2:83, §2:91), the discriminator separating class 3 from classes 1/2.

**Why "conservative default → SINGLE_ACCOUNT_LIMIT" (case 2b) is safe:** a 429 with an unrecognized body still routes to bounded retry, not halt. Worst case it burns `cap` re-spawns then halts — never an infinite loop (edge #9), never a false PASS. The fast-path (case 1) is only taken on the *positive* cooldown-regex match, so an ambiguous 429 cannot wrongly skip the retry budget.

---

## 2. Detector-ordering rule (per-task status ladder)

**Current ladder (verified, executor.py:999-1015):**

```
exit_code==0                                              → PASS                (:999-1000)
exit_code==124                                            → INCOMPLETE          (:1001-1002)
detect_error_max_turns(p) AND _task_completed_before_overrun(p)
                                                          → PASS_RECOVERED      (:1003-1011)
_is_transient_failure(p)                                  → FAIL_RECOVERABLE    (:1012-1013)
else                                                      → FAIL_TERMINAL       (:1014-1015)
```

**Design target ladder (spec §4 Layer-4:242-251):** insert the provider-failure branch **ABOVE `_is_transient_failure` (:1012)** and **BELOW the `:1003` completion-evidence gate**:

```
success-envelope (exit 0)            → PASS
error_max_turns + completed          → PASS_RECOVERED       (the :1003 gate — outranks everything below)
provider-failure (429) + NOT completed  → drive SessionResetPolicy  ← NEW BRANCH, inserted here
transient                            → FAIL_RECOVERABLE
terminal                             → FAIL_TERMINAL
```

**The reused completion guard (spec §4:248-251, §5 edge #1):** because `detect_provider_failure` keys on the LAST result event, a transcript that finished its work and *then* emitted a trailing 429 must NOT be re-spawned. Two sub-cases, both guarded by `_task_completed_before_overrun(output_path)` (executor.py:2321):

- **Overrun-then-429:** `detect_error_max_turns` True AND completed → the existing `:1003` branch already returns `PASS_RECOVERED` *before* the new branch is reached. Ordering alone handles it.
- **Clean-success-then-trailing-429:** `detect_error_max_turns` is **False** (terminal line is the 429 result, not error_max_turns), so the `:1003` branch is skipped and control reaches the NEW provider-failure branch. Here the new branch must **itself** call `_task_completed_before_overrun(output_path)` first: if completion evidence is present → classify `PASS_RECOVERED`, do NOT re-spawn (spec §4:248-251).

**Guard-reuse correctness note (verified against the helper's contract):** `_task_completed_before_overrun` scans `lines[:-1]` — strictly *before* the terminal line (executor.py:2367-2387). Its docstring says it is "only meaningful when called for a stream whose terminal line is the `error_max_turns` envelope" (executor.py:2349-2352). When reused in the provider-failure branch the terminal line is the **429 result** instead, but the helper's mechanics are unaffected: it excludes the last line (the 429) and looks for a success envelope (Class 1, `_TASK_SUCCESS_ENVELOPE_PATTERN`) or a tail completion verdict (Class 2) in the preceding lines. So a genuine clean-success-then-429 (which has a real success envelope before the 429) returns True → PASS_RECOVERED; a task that 429'd mid-work has no such envelope → returns False → proceeds to SessionResetPolicy. The guard is sound for this reuse. **(Builder note for R5: add a test asserting the success-envelope-then-trailing-429 fixture classifies PASS_RECOVERED with 0 re-spawns — this is the precise behavior the guard protects, edge #1.)**

**Offline ladder (rerun_tasks._classify_transcript, spec §4:168-177):** the same discrimination must be mirrored. Current order (rerun_tasks.py:582-591): `not is_error && tokens>0 → PASS`; `is_error && transient → FAIL_RECOVERABLE`; `is_error → FAIL_TERMINAL`. The Design inserts a `FAIL_PROVIDER_EXHAUSTED` branch **above** the `is_error`/transient branching (spec §4:176-177) keyed off the shared `_provider_failure_from_text(text)` inner. Signature reconciliation (spec §4:168-175): factor a text-accepting core `_provider_failure_from_text(text)`; the path wrapper `detect_provider_failure(output_path)` reads the file then delegates; `_classify_transcript` calls the inner on its existing `text` (it already has `text`, never re-reads).

---

## 3. Global-latch K>1 flow (parallel spawn-storm bound)

**Threading (spec §4 Layer-3:220-232, verified concurrency model):** the `SessionResetPolicy` instance (carrying `_latch_tripped`) is passed into `_run_one_task` as a **new shared param** alongside `ledger`/`shadow_metrics`/`remediation_log` (existing signature at executor.py:963-975; both call sites pass `lock=` — K>1 at executor.py:1144 with the real lock, K=1 at executor.py:1347 with `lock=None`).

**Verified lock discipline (executor.py:976-985 docstring + :1017-1018 guard):** the SPAWN runs **UNLOCKED** (the concurrency win). The budget reconcile + post-task hooks run under `guard = lock if lock is not None else contextlib.nullcontext()`. The new latch follows this exact pattern:

```
[under lock]   check policy._latch_tripped  → if tripped, skip spawn, return FAIL_PROVIDER_EXHAUSTED
[UNLOCKED]     spawn subprocess (the slow part)
[detect]       detect_provider_failure(output_path)
[policy]       SessionResetPolicy.decide(signal, attempt)
[under lock]   if Action==HALT_MODEL_SWITCH: set policy._latch_tripped = True
```

**Storm bound (spec §4:230-232, §5 edge #3, §6 test:332) — the load-bearing arithmetic:**
- The latch is checked under `lock` immediately before each spawn and tripped under `lock` after a worker classifies HALT_MODEL_SWITCH.
- BUT the spawn is unlocked, so up to **K−1** workers may already be mid-spawn (past their latch check) when the latch trips.
- Therefore: **total spawns ≤ cap + (K−1)** and strictly **< K × cap** (no storm), but **NOT** strictly `≤ cap` under genuine parallelism.
- The spec is explicit that the test must assert `total spawns < K × cap AND ≤ cap + (K−1)` (spec §6:332), **not** `≤ cap`. A builder/reviewer who writes `assert spawns <= cap` for the K>1 case is encoding the wrong (over-strict) bound — this is the subtle trap the spec calls out.

**Why the latch matters:** without it, K parallel workers each independently burn the full `cap` reset budget against a dead pool → `K × cap` spawn storm. The latch makes the first HALT_MODEL_SWITCH sprint-wide, so the others short-circuit. The `cap + (K−1)` slack is the price of keeping the spawn unlocked (the deliberate concurrency tradeoff, spec §4:227-232).

---

## 4. Reset budget: per-run/in-memory vs cross-run cap-3

Two **independent** budgets — must not be conflated (spec §4 Q4:299, §8 Q4:376):

| Budget | Scope | Storage | Value | Purpose |
|---|---|---|---|---|
| **Session-reset budget** (NEW) | per-run, in-memory | `SessionResetPolicy._exhaustion_attempts` / `attempt` counter (Design, recovery_policy.py) | `max_session_resets` default **8** ≈ pool size (spec §4 Q5:213, §8 Q5:378) | bound single-account re-route loop within ONE sprint run |
| **Content-rerun cap-3** (EXISTING) | cross-run, persisted | `retry_count_for_task(...) >= 3` (rerun_tasks.py:1482; recovery.py:356) | 3 | bound how many times `rerun-tasks`/recovery re-runs a task for *content* failures across runs |

**Key flow consequence (spec §3 contract #7:127-129, §5 edge #4):** the session-reset budget is **NOT folded into the cumulative `recovery_history`** (verified: `recovery_history` is persisted in `_write_phase_result_json` at executor.py:2692 and is the cross-run content surface). So:
- A 429-halted task that resumes in a *next* run gets a **FRESH** reset budget of `max_session_resets` (spec §3:129 "the resume gets a fresh reset budget").
- An account freed by the time the next run starts is not penalized by exhaustion attempts burned in the prior run (edge #4: "cross-run budget poisoning" is avoided).
- Conversely, the content cap-3 still applies to genuine content reruns — a 429-exhausted task is `FAIL_PROVIDER_EXHAUSTED` (infra), not a content failure, so it should NOT increment the content retry counter. (Builder/R3 cross-check: confirm `FAIL_PROVIDER_EXHAUSTED` is excluded from `retry_count_for_task` accounting; spec §4 (G):195-196 + research-notes (G) flags the parallel concern that recovery.py *nominators* should exclude `failure_class=="provider_exhaustion"` — same theme, deferred to P6.)

---

## FINDING F-1 (material discrepancy — single-session diagnostic gate)

**Spec claim (§4 Layer-2:191-196):** *"`is_failure` has **no auto-remediation consumer** in the live executor — `executor.py:2103` (`if status.is_failure:`) only halts the phase (desired). Diagnostic-bundle nomination is operator-invoked via `sprint rerun-tasks`."*

**Verified reality (executor.py:2103-2128, this session):** the `if status.is_failure:` block in the **single-session phase path** does NOT merely halt. It runs, inline and automatically:

```python
if status.is_failure:                               # executor.py:2103  (PhaseStatus.is_failure)
    collector = DiagnosticCollector(config)         # :2106
    bundle = collector.collect(phase, phase_result, monitor.state)  # :2107
    classifier = FailureClassifier()                # :2108
    bundle.category = classifier.classify(bundle)   # :2109
    reporter.write(bundle, phase-N-diagnostic.md)   # :2111-2114
    ...
    sprint_result.outcome = SprintOutcome.HALTED    # :2130
    break
```

So the spec's "no auto-remediation consumer" statement is **true for the per-task `TaskStatus.is_failure` path** (executor.py:1012-1015 has no inline collector) but **FALSE for the single-session `PhaseStatus.is_failure` path** (executor.py:2103 runs DiagnosticCollector + FailureClassifier + writes a `phase-N-diagnostic.md` product-bug bundle automatically).

**Impact on UX contract #4 (spec §3:117-119 "never trips remediation/diagnostic-bundle machinery"):** if `PhaseStatus.PROVIDER_EXHAUSTED` is added to `PhaseStatus.is_failure` (models.py:437-443), a single-session 429 halt WILL auto-write a spurious product-bug diagnostic bundle — exactly what contract #4 forbids.

**Recommended resolution (for the builder — encode, do not silently pick):**
- Add `PhaseStatus.PROVIDER_EXHAUSTED` to **`is_terminal`** (models.py:410-423) so the phase halts and resume treats it correctly, but **NOT** to `is_failure` (models.py:437) — OR
- Amend the executor.py:2103 guard to `if status.is_failure and status is not PhaseStatus.PROVIDER_EXHAUSTED:` (skip diagnostics) while separately driving the HALTED outcome for the exhaustion case.
- Either way the phase must still set `SprintOutcome.HALTED` (executor.py:2130) and break. This is a P4 concern (single-session path) and should be an explicit task item with a test asserting **no `phase-N-diagnostic.md` is written** for a single-session 429 halt.

This finding is the runtime-flow counterpart to research-notes line 31 ("`status.is_failure` consumer at `:2103-2132` = phase halt") which under-described the diagnostic side-effect; R3 (static wiring) should corroborate. It does NOT change the per-task path (TaskStatus.is_failure has no such consumer).

---

## 5. The 10 edge cases (spec §5) — expected classification + flow

Each row: trigger → detector output → policy/ladder outcome → why. All Design unless an existing-code anchor is cited.

| # | Edge case | Detector (`ProviderFailure`) | Policy `Action` / status | Expected end-state | Evidence / mechanism |
|---|---|---|---|---|---|
| 1 | **Completed-then-trailing-429** | Inner sees 429 on LAST result event → would say SINGLE/ALL, BUT the executor branch is **gated** by `_task_completed_before_overrun` first | guard True → `PASS_RECOVERED`, branch skipped | **PASS_RECOVERED, 0 re-spawns** | spec §5:288-292; guard reuse §2 above; executor.py:2321 + :1003 ordering. The completion gate outranks the 429 because the detector keys on the LAST event. |
| 2 | **Shifting failure across attempts** (single-429 → cooldown → real bug) | classify by the **last** attempt's transcript | cooldown fast-path halts immediately; or single→single hits cap; or final real-bug → `NONE`→CONTINUE→FAIL_TERMINAL | last-attempt classification wins; loop stops at cooldown or cap | spec §5:293. Each re-spawn re-runs the detector on the new transcript; no state carried except the attempt counter + latch. |
| 3 | **Parallel spawn storm** | each worker detects independently | first HALT_MODEL_SWITCH trips latch under lock | **total spawns ≤ cap+(K−1) AND < K×cap** (NOT ≤ cap) | spec §5:294-298, §3 above. Unlocked spawn admits K−1 in-flight overshoots. |
| 4 | **Cross-run budget poisoning** | n/a (detector stateless) | reset budget per-run/in-memory, NOT in `recovery_history` | next run gets FRESH budget; freed account not penalized | spec §5:299; §4 above; `recovery_history` persisted at executor.py:2692, separate from reset counter. |
| 5 | **Torn/partial transcript** (killed subprocess) | read/parse error or no result event → **NONE** | CONTINUE → existing ladder (likely INCOMPLETE via exit 124, or FAIL via transient) | no false re-spawn | spec §5:300. Mirrors OSError tolerance: `detect_error_max_turns` returns False on OSError (monitor.py:48-49); `count_turns` returns 0 on OSError (process.py:56-57); `_classify_transcript` returns INCOMPLETE when `result_event is None` (rerun_tasks.py:576-577). New detector must degrade to NONE. |
| 6 | **`api_retry` already at `max_retries==10`** | terminal result is still 429 → SINGLE/ALL as normal; the `api_retry` `attempt==max_retries==10` (field **`error_status`**, spec §2:63) only confirms in-session retries are burned | RETRY_NEW_SESSION (new session, not in-session) or fast-path halt | go straight to new session / model switch; no sprint-level in-session retry | spec §5:301, §2:90. The detector keys on `api_error_status` (terminal), the `error_status==429 + attempt==10` is corroborating context that in-session retry is pointless. |
| 7 | **No alternate alias in `~/.aienv`** | n/a (detection unaffected) | halt proceeds; `suggest_alternate_model` returns None-safe | message shows exhausted model + generic guidance (wait/add accounts/switch if available), **must not fabricate** an alias | spec §5:302; §3 contract #6; aienv.py Design (P5). |
| 8 | **`error_max_turns` vs 429** | detector **excludes** budget exhaustion; `error_max_turns` is `subtype` on result with `api_error_status` absent/not-429 | distinct path → PASS_RECOVERED (if completed) or its own handling, never provider-failure | no conflation | spec §5:303. `ERROR_MAX_TURNS_PATTERN` keys on `subtype:"error_max_turns"` (monitor.py:33); the 429 detector keys on `api_error_status==429` — orthogonal fields. |
| 9 | **Infinite-loop guard** (always-429 single-account factory) | every attempt → SINGLE_ACCOUNT_LIMIT | RETRY_NEW_SESSION until `attempt >= cap` → HALT_MODEL_SWITCH | terminates in **exactly `cap` spawns** (test-asserted) | spec §5:304, §6:334. cap + latch are the two terminators; a single-account loop that never escalates to cooldown is bounded by cap. |
| 10 | **`subtype:"success"` trap** | MUST key on `is_error` + `api_error_status`, NEVER `subtype` | correct 429 detection despite `subtype=="success"` | no false PASS on a 429 | spec §5:305, §2:70-72. Today `_classify_transcript` reads `subtype` (rerun_tasks.py:579) — the new shared core must read `is_error`+`api_error_status` so the offline path stops mis-reading a 429's `subtype:"success"` as non-error. |

---

## 6. Persistence → resume → halt-UX trace (terminal-state movement)

**Persistence (per-task, Design — spec §4 Layer-2:198-201 + Layer-4:255-257):**
- `TaskResult` gains `failure_class: str=""`, `session_resets: int=0`, `exhausted_model: str=""`. `to_dict` serializes them flat; `from_dict` MUST use `.get(default)` (currently hard-keyed at models.py:218-240 per research-notes — old `phase-N-result.json` would KeyError without defaults).
- Single-session phase: `_write_phase_result_json` (executor.py:2657-2701) gains top-level `halt_reason: "provider_exhaustion"` + `exhausted_model`. Current payload (verified executor.py:2685-2696) has `phase/status/exit_code/started_at/finished_at/task_results/recovery_history/tasklist_sha256/tasklist_sha256_ws` — the two new top-level keys append cleanly.
- `execution-log.jsonl`: emit `session_reset` / `account_exhaustion_halt` events (P6).

**Resume routing (verified, no planner edit needed — spec §4:184-188):**
- `FAIL_PROVIDER_EXHAUSTED` is in `TaskStatus.is_failure` (Design add to models.py:61-66) → `not persisted_status.is_success` is True → `ResumePlanner` re-runs it (planner.py:160-164, per research-notes).
- Per-task resume coerces via `_coerce_task_status → TaskStatus(value)` (planner.py:157) — auto-resolves the new enum member, no edit.
- Hard-crash fallback `discover_failed_tasks_from_transcripts` (rerun_tasks.py:596+) routes through `_classify_transcript`, so the P2 shared-detector alignment makes a transcript-derived 429 re-run too.
- Phase must NOT be classed COMPLETE (spec §6 resume-safety:336-337) — `FAIL_PROVIDER_EXHAUSTED` / `PROVIDER_EXHAUSTED` is non-success.

**Halt UX (Design — spec §4 Layer-5:259-273, §3 contract #6):**
- `models.build_account_exhaustion_halt(config, halt_task_id, exhausted_model, suggested_model, remaining_tasks, ledger)` → **single-line** `superclaude sprint run <index> --resume <task-id> --model <suggested>` + CLIProxyAPI rationale. Single-line is mandatory (terminal can't paste multi-line — spec §3:122, and per global memory `feedback_no_multiline_paste`).
- Wired into halt output when `halt_reason == provider_exhaustion`; else fall through to existing `build_resume_output` (models.py:1017-1071).
- The cooldown body embeds the **resolved** model (`All credentials for model claude-opus-4-8 …`), so `_RE_ALL_ACCOUNT`'s `(?P<model>.+?)` capture (spec §4:150) gives the suggester the resolved model even when `config.model` was an alias — `suggest_alternate_model` returns the next distinct alias (opus→sonnet; `T0Model01`→`T0Model02`).

---

## Summary

Traced the full runtime path of a 429 signal end-to-end for both the per-task path (`_run_one_task`, K=1 + K>1) and the single-session phase path, grounded in verified code sites.

**Decision-flow deliverables for the builder:**
1. **Four-way discrimination table** (§1) — all decided on the LAST `{"type":"result"}` event via `api_error_status` (NOT `subtype`); all-account cooldown → HALT_MODEL_SWITCH fast-path on ANY attempt; single-account (and unrecognized-body 429, conservative default) → RETRY_NEW_SESSION bounded by cap; operation_timeout (`api_error_status==null`) → existing path; genuine failure → existing FAIL_TERMINAL/RECOVERABLE.
2. **Detector ordering** (§2) — provider-failure branch inserted ABOVE `_is_transient_failure` (executor.py:1012) and BELOW the `:1003` completion gate; `_task_completed_before_overrun` reused as the guard for clean-success-then-trailing-429; verified the guard's `lines[:-1]` mechanics stay sound when the terminal line is a 429 instead of error_max_turns.
3. **Global-latch K>1 flow** (§3) — checked/tripped under lock, spawn unlocked; storm bound **≤ cap+(K−1) AND < K×cap**, explicitly NOT `≤ cap` (the over-strict-assertion trap).
4. **Reset budget** (§4) — per-run/in-memory `max_session_resets`=8, independent of cross-run content cap-3; resume gets a fresh budget.
5. **10 edge cases** (§5) — each with detector output + policy/ladder outcome + evidence anchor.

**Field-name cross-check (spec §2):** terminal event field is `api_error_status` (load-bearing); api_retry event field is the different `error_status`; operation-timeout discriminator is `api_error_status==null`. Confirmed `_classify_transcript` today reads `subtype`+`is_error` only (rerun_tasks.py:579-580), so a 429 is currently invisible to the offline classifier.

**MATERIAL FINDING F-1:** The spec's claim that `is_failure` has "no auto-remediation consumer in the live executor" is **true for the per-task `TaskStatus.is_failure` path but FALSE for the single-session `PhaseStatus.is_failure` path** — executor.py:2103-2128 runs `DiagnosticCollector` + `FailureClassifier` and writes a `phase-N-diagnostic.md` product-bug bundle automatically before halting. Adding `PROVIDER_EXHAUSTED` to `PhaseStatus.is_failure` (models.py:437) would trip exactly the diagnostic machinery UX contract #4 forbids. Resolution: put `PROVIDER_EXHAUSTED` in `is_terminal` (not `is_failure`), or guard the executor.py:2103 block to skip diagnostics for it — encode as an explicit P4 item with a test asserting no diagnostic bundle is written on a single-session 429 halt. (R3 to corroborate the static-wiring side.)
