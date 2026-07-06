# Research: Detector Change Surface

**Status:** Complete
**Topic:** File Inventory / exact change-surface + read-only consumer confirmation
**Scope:** `src/superclaude/cli/sprint/monitor.py` + read-only consumer chain
**Verified against source:** 2026-07-02 (every claim below cites a line I actually Read this turn)

---

## 1. Entry predicate + surrounding block — `_provider_failure_from_text` (monitor.py)

Function spans `monitor.py:291-345`. The two mandated hunks (C1 predicate, C8 regex) are the ONLY
edits inside this file; everything below is quoted verbatim as it exists NOW.

### 1a. The C1 target — entry-predicate line (spec said "~:323", CONFIRMED at :323)

```python
323	    if is_error and api_error_status == 429:
```

This is the EXACT current expression the C1 hunk widens to
`is_error and (api_error_status == 429 or "rate_limit_error" in body)`.

### 1b. The full 429 branch body through the neither-body default (`:324-333`)

```python
324	        cooldown = _RE_ALL_ACCOUNT.search(body)
325	        if cooldown:
326	            return ProviderFailureSignal(
327	                ProviderFailure.ALL_ACCOUNT_COOLDOWN,
328	                resolved_model=cooldown.group("model"),
329	            )
330	        if _RE_SINGLE_ACCOUNT.search(body):
331	            return ProviderFailureSignal(ProviderFailure.SINGLE_ACCOUNT_LIMIT)
332	        # 429 with neither body — conservative default: rotate (don't halt).
333	        return ProviderFailureSignal(ProviderFailure.SINGLE_ACCOUNT_LIMIT)
```

Spec's "`429-with-neither-body → SINGLE_ACCOUNT_LIMIT` default (~:332-333)" is CONFIRMED verbatim
at `:332` (comment) + `:333` (return). This is the INV-001 residual path (contract row 8).

### 1c. The operation-timeout branch (spec said "~:335-338", CONFIRMED at :335-343)

```python
335	    if (
336	        is_error
337	        and api_error_status is None
338	        and body == "API Error: The operation timed out."
339	    ):
340	        # Spec §2 conjunctive predicate: OPERATION_TIMEOUT requires is_error too —
341	        # a non-error result carrying this exact body (implausible, but the spec
342	        # predicate is conjunctive) must not be mis-classified as a timeout.
343	        return ProviderFailureSignal(ProviderFailure.OPERATION_TIMEOUT)
344	
345	    return ProviderFailureSignal(ProviderFailure.NONE)
```

The timeout branch predicate begins at `:335` and closes with the `OPERATION_TIMEOUT` return at
`:343`; the terminal `NONE` fall-through is `:345`. NOTE: the spec's "~:335-338" refers to the
predicate lines; the branch's actual return is `:343` (spec §5 item 8 / §7 debt-ledger pins this
`body == "API Error: The operation timed out."` exact-match at `:335-338` as byte-unchanged / row T1).
This branch STAYS UNTOUCHED — only a guard test (F5 unreachability) is added.

---

## 2. Regex definitions — `_RE_ALL_ACCOUNT` + `_RE_SINGLE_ACCOUNT` (monitor.py)

Spec said "`_RE_ALL_ACCOUNT` at :41-43". CONFIRMED at `:41-43`:

```python
41	_RE_ALL_ACCOUNT = re.compile(
42	    r"All credentials for model (?P<model>.+?) are cooling down via provider"
43	)
44	_RE_SINGLE_ACCOUNT = re.compile(r"would exceed your account's rate limit")
```

- `_RE_ALL_ACCOUNT` (`:41-43`) CURRENTLY requires the `... are cooling down via provider` suffix —
  this is the C8 target. R2 drops `via provider` →
  `r"All credentials for model (?P<model>.+?) are cooling down"`, keeping the non-greedy
  `(?P<model>.+?)` capture group.
- `_RE_SINGLE_ACCOUNT` (`:44`) is `r"would exceed your account's rate limit"` — spec R2 says this is
  UNCHANGED. Confirmed single-line, no capture group.

Supporting docstring context for these regexes is at `:38-40` (comment block naming the `model`
group as the P5 alias-suggester feed).

---

## 3. In-scope locals at the predicate site (C1/C8 are surgical inline edits — no new helper)

All three locals are established at `:319-321`, immediately BEFORE the `:323` predicate:

```python
319	    is_error = bool(result_event.get("is_error"))
320	    api_error_status = result_event.get("api_error_status")
321	    body = str(result_event.get("result", ""))
```

- `body = str(result_event.get("result", ""))` — CONFIRMED in scope at `:321` (spec R1 said "already
  in scope at :321"; exact). So the C1 disjunct `"rate_limit_error" in body` needs NO new extraction
  and NO helper — it references an existing local. The membership test is a plain `in` on the decoded
  result string (spec R1: NOT a regex, NOT JSON-path).
- `is_error` and `api_error_status` locals BOTH exist at the predicate site (`:319`, `:320`). Both C1
  and C8 are therefore single-expression inline edits with zero new symbols.

---

## 4. Read-only consumer chain — MUST STAY UNTOUCHED (each confirmed at file:line)

| # | Consumer | Location | Confirmed behavior | Status |
|---|---|---|---|---|
| a | offline `_classify_transcript` | `rerun_tasks.py:552` | parses terminal result event; delegates | **confirmed at rerun_tasks.py:552 — untouched** |
| b | inner-detector call from offline | `rerun_tasks.py:592` (`_sig = _provider_failure_from_text(text)`) | on `SINGLE_ACCOUNT_LIMIT` OR `ALL_ACCOUNT_COOLDOWN` (`:593-596`) → returns `TaskStatus.FAIL_PROVIDER_EXHAUSTED` at `:605` (or `PASS_RECOVERED` at `:604` if completed-before-overrun) | **confirmed at rerun_tasks.py:592/605 — untouched; returns FAIL_PROVIDER_EXHAUSTED on a 429 signal** |
| c | policy `SessionResetPolicy.decide` | `recovery_policy.py:53` | `ALL_ACCOUNT_COOLDOWN → HALT_MODEL_SWITCH` on ANY attempt (`:69-70`); `SINGLE_ACCOUNT_LIMIT → RETRY_NEW_SESSION` under budget else `HALT_MODEL_SWITCH` (`:71-74`) | **confirmed at recovery_policy.py:69-70 — untouched** |
| d | live call site (K>1) | `executor.py:1085` (`signal = detect_provider_failure(task_output_path)`) | consumes signal before status ladder; sets `FAIL_PROVIDER_EXHAUSTED` at `:1063`/`:1124` | **confirmed at executor.py:1085 — untouched** |
| e | live call site (K=1) | `executor.py:2283` (`signal = detect_provider_failure(config.output_file(phase))`) | K=1 phase path | **confirmed at executor.py:2283 — untouched** |
| f | status enum | `models.py:53` (`FAIL_PROVIDER_EXHAUSTED = "fail_provider_exhausted"`) | member of `is_failure` set at `models.py:66` | **confirmed at models.py:53/66 — untouched** |
| g | resume hint | `models.py:880` (`def resume_command`) | feeds `suggest_alternate_model(exhausted_model)` | **confirmed at models.py:880 — untouched** |
| h | alias suggester | `aienv.py:81` (`def suggest_alternate_model(`) | consumes captured `resolved_model` | **confirmed at aienv.py:81 — untouched** |

**Offline mirror confirmation (spec R6 single-source-of-truth):** `_classify_transcript`
(`rerun_tasks.py:552`) calls the SAME inner `_provider_failure_from_text` at `:592` that the live
wrapper `detect_provider_failure` (`monitor.py:348-364`, calls inner at `:364`) calls. Editing the one
inner function fixes BOTH paths — CONFIRMED. The offline classifier's own parse loop (`:560-579`) is
a parallel/independent loop for `output_tokens`+`is_error`; it does NOT re-implement the 429
discrimination (it defers entirely to `_provider_failure_from_text`), so it stays byte-unchanged.

---

## 5. Precision notes for the builder's verification criteria

- **`is_error` is truthy-guarded via `bool(...)`**: `monitor.py:319` is
  `is_error = bool(result_event.get("is_error"))`. So `is_error` is always a real `bool` (missing key →
  `False`), never a truthy-string surprise. The C1 predicate's `is_error and (...)` short-circuits on a
  genuine boolean.
- **`api_error_status` uses `.get` (absent → `None`)**: `monitor.py:320` is
  `api_error_status = result_event.get("api_error_status")` — NO default arg, so an ABSENT field
  yields `None`. This is exactly the Shape-2 breaker (spec G1): `None == 429` is `False`, so the old
  conjunct fails and the branch never opens. The C1 `or "rate_limit_error" in body` disjunct is what
  reopens it. (The offline classifier does NOT read `api_error_status` at all — it delegates — so no
  parallel edit is needed there.)
- **Superset/back-compat (R3) is structural**: because `api_error_status == 429` remains the FIRST
  disjunct at the (widened) `:323` predicate, every transcript the old gate caught still enters via the
  fast-path. `old_match ⊆ new_match` holds by construction.
- **No new imports needed in monitor.py**: `re` (`:12`) and `json` (`:10`) are already imported; the
  C1/C8 edits add no symbol, no helper, no import.

---

## Summary

The two mandated hunks are pinned to exact current lines: **C1** widens the entry predicate at
`monitor.py:323` (`if is_error and api_error_status == 429:`), and **C8** loosens `_RE_ALL_ACCOUNT` at
`monitor.py:41-43` (drop `via provider`). Both are surgical inline edits — `body`, `is_error`, and
`api_error_status` locals already exist at `:319-321`, so no helper/import is added. `is_error` is
`bool(...)`-guarded (`:319`); `api_error_status` uses bare `.get` so an absent field is `None` (`:320`)
— the exact Shape-2 breaker. The entire consumer chain is confirmed untouched: offline
`_classify_transcript` (`rerun_tasks.py:552`) delegates to the same inner at `:592` and returns
`FAIL_PROVIDER_EXHAUSTED` (`:605`); `decide` maps `ALL_ACCOUNT_COOLDOWN→HALT_MODEL_SWITCH`
(`recovery_policy.py:69-70`); executor call sites (`:1085`, `:2283`), `models.py` enum (`:53`) +
`resume_command` (`:880`), and `aienv.suggest_alternate_model` (`:81`) all stay byte-unchanged. The
single-inner-function edit fixes both live and offline paths (R6).
