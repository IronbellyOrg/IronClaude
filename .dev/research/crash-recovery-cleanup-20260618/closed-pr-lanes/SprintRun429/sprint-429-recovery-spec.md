---
title: "Sprint Run 429 / Account-Exhaustion Recovery — Implementation Spec"
status: ready-for-mdtm
domain: code
strategy: systematic
depth: deep
created: 2026-06-15
source: /sc:brainstorm --depth deep --strategy systematic
ground_truth: /config/workspace/Octodive/.dev/troubleshoot/build-superclaude-sprint-run-stalled-20260613121456/429-signature-ground-truth.md
---

# Sprint Run 429 / Account-Exhaustion Recovery — Implementation Spec

> **Infra ground truth (do not re-litigate):** Claude CLI traffic →
> LiteLLM `:4000/cli` → CLIProxyAPI → ~8 Anthropic accounts. A 429 means a
> *routed account* hit its 5h/7d window, not that the model is globally down.
> Because sprint always spawns subprocesses with `--no-session-persistence`
> (`process.py:132`), **a new subprocess == a new session == a new CLIProxyAPI
> routing decision == a chance at a different account.** Recovery is *re-routing*,
> not *waiting*.

---

## 0. Grounding evidence (verified against source, 2026-06-14/15)

| Fact | Evidence |
|---|---|
| Subprocess cmd: `claude --print --verbose --no-session-persistence … --output-format stream-json [--model M]` | `process.py:129-141` |
| `config.model` → `--model`; `env_vars` merges into `os.environ.copy()` (inherits `ANTHROPIC_DEFAULT_*` + proxy base URL) | `process.py:141`; `executor.py:1808-1815` |
| **No 429/cooldown/rate-limit handling exists** | grep: 0 hits in `cli/sprint/` |
| **No in-process retry/backoff exists**; failed phase → `SprintOutcome.HALTED` + `break` | `executor.py:2103-2132` |
| Per-task status ladder (exit0→PASS; 124→INCOMPLETE; max_turns+done→PASS_RECOVERED; `_is_transient_failure`→FAIL_RECOVERABLE; else FAIL_TERMINAL) | `executor.py:999-1015` |
| `_is_transient_failure`: only `api_retry` / `ConnectionRefused` / (`is_error`+0 tokens) | `executor.py:2267-2289` |
| Offline `_classify_transcript`: a 429 today → FAIL_TERMINAL (tokens>0) or FAIL_RECOVERABLE (tokens==0); never recognized as routing problem | `rerun_tasks.py:547-593` |
| Retry-cap-3 precedent for content reruns: `retry_count_for_task(...) >= 3` | `rerun_tasks.py:1482`; `recovery.py:356` |
| Resume re-runs any task whose persisted status is not success | `resume/planner.py:160-164` |
| Halt UX emits `--resume … --max-turns` / `--start/--end`; **neither carries `--model`** | `models.py:1017-1071`; `models.py:821-828` |
| `detect_*` helper family (template for the new detector) | `monitor.py:37,64` |
| Test seam: `_run_one_task(subprocess_factory=…)`, `_execute_phase_tasks_parallel(_subprocess_factory=…)` | `executor.py:986-993,1054` |

---

## 1. Diagnosis of the incorrect prior assumption

The previous troubleshooting pass treated a 429 as a **provider-wide temporal
cooldown** ("wait 5h/7d"). Wrong on two counts:

1. **Wrong layer** — a 429 is one routed account hitting its window; ~7 other
   accounts remain usable behind CLIProxyAPI.
2. **Wrong lever** — `--no-session-persistence` already makes every subprocess a
   fresh upstream connection, so the corrective action is **re-routing** (new
   subprocess, or a model-alias switch that draws from a different pool), never
   *time*. Waiting pins the same exhausted account.

---

## 2. 429 signature — PINNED from real transcripts (Q1)

**Surfaces entirely in stdout stream-json. The `*-errors.txt` stderr sidecars are
0 bytes for every 429 — do NOT read stderr.** Three event types per transcript:

```jsonc
// 1. CLI's own retry loop (note: field is "error_status", up to max_retries:10)
{"type":"system","subtype":"api_retry","error_status":429,"error":"rate_limit","attempt":N,"max_retries":10}

// 2. harness-injected terminal assistant (note literal "model":"<synthetic>")
{"type":"assistant","message":{"model":"<synthetic>", ...},"error":"rate_limit"}

// 3. THE LOAD-BEARING LINE (note: field is "api_error_status";
//    subtype is "success" EVEN THOUGH is_error is true — do NOT key on subtype)
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,
 "result":"API Error: Request rejected (429) · ..."}
```

**Two distinct upstream bodies in event #3's `result` string = two distinct signals:**

| Signal | `result` body (observed) | Count | Meaning | Action |
|---|---|---|---|---|
| **All-account cooldown** | `All credentials for model <resolved-model> are cooling down via provider claude` | 27× | CLIProxyAPI already rotated through every account | **Model-switch halt — FAST PATH** |
| **Single-account limit** | `This request would exceed your account's rate limit. Please try again later.` | 14× | Raw Anthropic 429 for one routed account | **New-session retry (rotate)** |

**Separate class — do NOT fold in:** operation timeout =
`is_error==true && api_error_status==null && result=="API Error: The operation timed out."`
(observed at T03.05). This is the existing timeout path, not account exhaustion.

**Pinned predicates** (evaluate on the LAST `{"type":"result"}` event):
- provider rate-limit terminal failure: `type=="result" && is_error==true && api_error_status==429`
- → **all-account** (model switch): `result` matches `/All credentials for model .+ are cooling down via provider/`
- → **single-account** (new-session retry): `result` contains `This request would exceed your account's rate limit`
- in-session retry already burned: `api_retry` event with `attempt==max_retries==10` ⇒ sprint-level in-session retry is pointless; only a new session or model switch helps
- timeout (distinct): `is_error==true && api_error_status==null && result=="API Error: The operation timed out."`

**Design implication (efficiency):** the all-account body lets us **skip the blind
N-attempt heuristic for the common case** — if the *first* failure already says
"All credentials … cooling down via provider", every account is down, so go
**straight to the model-switch halt** instead of burning more session reopens.

**Fixture sources (on Octodive; NOT reachable from the IronClaude dev worktree —
author fixtures from the verbatim JSON in the ground-truth doc):**
- Single-account, 17-line minimal: `results/phase-3-task-T03.14-output.txt`
- All-account cooldown after real work (num_turns=25): `results/phase-3-task-T03.13-output.txt`
- Timeout (distinct class): `results/phase-3-task-T03.05-output.txt`
- Full verbatim doc: `/config/workspace/Octodive/.dev/troubleshoot/build-superclaude-sprint-run-stalled-20260613121456/429-signature-ground-truth.md`

---

## 3. Product / UX contract

1. **Re-route, don't wait.** On a single-account 429, close the subprocess and
   re-spawn the same task/phase (new session → CLIProxyAPI re-routes). No long
   sleep; optional ~0–2 s jitter only.
2. **Fast-path halt.** On an all-account-cooldown body (on *any* attempt, incl. the
   first), halt immediately with the model-switch message — no further re-spawns.
3. **Bounded backstop.** Single-account retries are capped by `--max-session-resets`
   (**default scales toward pool size ≈ 8**, Q5). Per-run / in-memory budget (Q4).
4. **Distinguish, don't conflate.** Re-route attempts are **not** semantic task
   failures. The terminal infra status is a **new** `FAIL_PROVIDER_EXHAUSTED`
   (Q3), never `FAIL_TERMINAL`, so it never trips remediation/diagnostic-bundle
   machinery meant for product bugs.
5. **Clean halt.** Halt preserves all prior successful task state; never re-runs
   validated-successful tasks.
6. **Actionable, single-line resume command** (terminal cannot paste multi-line):
   names the exhausted model, prints a paste-ready resume with a **different**
   model, and a one-line rationale.
   - `superclaude sprint run <index> --resume <task-id> --model sonnet`
   - or proxy-alias form: `… --resume <task-id> --model T0Model02` (failed on `T0Model01`)
7. **Safe resume boundary.** Re-running re-attempts only the exhausted task and
   everything after it (existing handoff-skip path); the resume gets a **fresh**
   reset budget.
8. **No regressions** to `fail_recoverable`, `rerun-tasks`, `--resume/--start/--end`,
   `PASS_RECOVERED`, TurnLedger for non-429 paths.

---

## 4. Technical design — module-level changes

### Layer 1 — Detection (pure, shared) → `monitor.py`

New sibling to `detect_error_max_turns`/`detect_prompt_too_long`. Parses the LAST
`{"type":"result"}` event (mirror `count_turns_from_stream_json`), keys on
**structured fields**, then discriminates the body:

```python
class ProviderFailure(Enum):
    NONE = "none"
    SINGLE_ACCOUNT_LIMIT = "single_account_limit"   # → new-session retry
    ALL_ACCOUNT_COOLDOWN = "all_account_cooldown"   # → model-switch halt (fast path)
    OPERATION_TIMEOUT = "operation_timeout"         # → existing timeout path (NOT exhaustion)

_RE_ALL_ACCOUNT = re.compile(r"All credentials for model (?P<model>.+?) are cooling down via provider")
_RE_SINGLE_ACCOUNT = re.compile(r"would exceed your account's rate limit")

def detect_provider_failure(output_path) -> ProviderFailureSignal:
    """Returns (kind, resolved_model|None). OSError/parse-tolerant → NONE.
    Reads stdout transcript only (stderr is 0 bytes for 429s)."""
    # find last {"type":"result"}; read is_error, api_error_status, result text
    # 429 + all-account regex   -> ALL_ACCOUNT_COOLDOWN (+capture resolved model)
    # 429 + single-account regex-> SINGLE_ACCOUNT_LIMIT
    # 429 + neither             -> SINGLE_ACCOUNT_LIMIT  (conservative default for api_error_status==429)
    # api_error_status==null + timeout body -> OPERATION_TIMEOUT
    # else                      -> NONE
```

**Single source of truth** consumed by both the live executor AND offline
`_classify_transcript` — prevents the doc/code-at-the-seams drift that bit PR #160.
**Do NOT key on `subtype`** (it is `"success"` even when `is_error` is true).

**Signature reconciliation (sharing mechanics):** `detect_provider_failure(output_path)`
reads the path (mirroring `detect_error_max_turns`), but `_classify_transcript`
(`rerun_tasks.py:547`) already operates on an in-memory `text: str`. To share one
core without double-reading, factor the discrimination into a text-accepting inner
(`_provider_failure_from_text(text) -> ProviderFailureSignal`); the path-based
wrapper reads the file then delegates, and `_classify_transcript` calls the inner
on its existing `text`. `_classify_transcript` then gains a **new branch that
returns `FAIL_PROVIDER_EXHAUSTED` when the inner reports a 429 signal**, placed
**above** the existing `is_error`/transient branching (`rerun_tasks.py:582-591`),
so an offline 429 maps to the infra status instead of `FAIL_TERMINAL`.

### Layer 2 — Taxonomy + status → `models.py`

- New `TaskStatus.FAIL_PROVIDER_EXHAUSTED = "fail_provider_exhausted"`; add to the
  `is_failure` set (`models.py:61-66`). It is a *failure* (so resume re-runs it via
  `planner.py:160-164`) but *flagged infra* (skips remediation).
  - **Both resume paths covered by P2:** the per-task path (`planner.py:157`)
    coerces via `_coerce_task_status` → `TaskStatus(value)`, which resolves the new
    member automatically; the hard-crash fallback `discover_failed_tasks_from_transcripts`
    (`planner.py:166-171`) routes through `_classify_transcript`, so the shared-detector
    alignment makes a transcript-derived 429 re-run too. No separate planner edit needed.
  - **Remediation-skip is NOT automatic (verified blast radius):** `is_failure` has
    **no auto-remediation consumer** in the live executor — `executor.py:2103`
    (`if status.is_failure:`) only halts the phase (desired). Diagnostic-bundle
    nomination is **operator-invoked** via `sprint rerun-tasks` (`recovery.py` nominators),
    so adding the status is safe. To *fully* honor UX contract #4, the `rerun-tasks`
    nominators SHOULD exclude `failure_class == "provider_exhaustion"` (else a re-routed
    infra failure gets a spurious product-bug bundle) — deferred to P6, or scope UX
    contract #4 to the live auto-path.
- New `PhaseStatus.PROVIDER_EXHAUSTED` for the single-session path → routes to halt.
- `TaskResult`: add `failure_class: str = ""`, `session_resets: int = 0`,
  `exhausted_model: str = ""`. Serialize in `to_dict`; read with **`.get(...)`
  defaults** in `from_dict` (current `from_dict` uses hard keys — new fields MUST
  default so old `phase-N-result.json` stays readable) (`models.py:190-240`).

### Layer 3 — Policy (control flow) → new `recovery_policy.py`

```python
class Action(Enum): RETRY_NEW_SESSION; HALT_MODEL_SWITCH; FAIL_TASK; CONTINUE

@dataclass
class SessionResetPolicy:
    max_session_resets: int = 8     # Q5: ≈ pool size; cooldown body is primary terminator
    _exhaustion_attempts: int = 0
    _latch_tripped: bool = False    # shared across K>1 workers, lock-guarded

    def decide(self, signal: ProviderFailure, attempt: int) -> Action:
        if signal is ProviderFailure.ALL_ACCOUNT_COOLDOWN: return HALT_MODEL_SWITCH  # fast path
        if signal is ProviderFailure.SINGLE_ACCOUNT_LIMIT:
            return RETRY_NEW_SESSION if attempt < self.max_session_resets else HALT_MODEL_SWITCH
        return CONTINUE   # NONE / OPERATION_TIMEOUT → existing paths
```

**Global latch** (shared like `ledger`/`shadow_metrics`, guarded by the existing
`lock` param in `_run_one_task`): the first worker to conclude
HALT_MODEL_SWITCH trips a sprint-wide halt so K>1 parallel workers don't each burn
the full reset budget against a dead pool (no `K × max` spawn storm).
**Threading:** `SessionResetPolicy` (carrying `_latch_tripped`) is passed into
`_run_one_task` as a **new shared param** alongside `ledger`/`shadow_metrics`
(signature add at `executor.py:963-975`). The latch is **checked under `lock`
immediately before each spawn** and **tripped under `lock`** after a worker
classifies HALT_MODEL_SWITCH; the spawn itself stays **unlocked** (the
concurrency win). Because the spawn is unlocked, up to `K−1` workers may already
be mid-spawn when the latch trips — so the storm bound is `≤ cap + (K−1)` and
strictly `< K × cap`, **not** strictly `≤ cap` (see edge case #3).

### Layer 4 — Executor wiring → `executor.py`

- **Per-task path:** wrap the spawn in `_run_one_task` (`executor.py:986-993`) in a
  bounded re-spawn loop driven by `detect_provider_failure` + `SessionResetPolicy`.
  Insert a new status branch **above** `_is_transient_failure` (`:1012`) and
  **below** the `:1003` completion-evidence gate.
  **Detector ordering** (completion evidence outranks all, mirroring
  `_task_completed_before_overrun` at `:1003`):
  `success-envelope → error_max_turns (PASS_RECOVERED) → provider-failure → transient → terminal`.
  The provider-failure branch sits **below** the `:1003` gate, so a transcript
  that hit max-turns after substantive work (even with a trailing 429) stays
  `PASS_RECOVERED`, never re-spawned. **`detect_provider_failure` keys on the
  LAST `{"type":"result"}` event**, so to also cover a *clean-success*-then-
  trailing-429 (where `detect_error_max_turns` is False and the `:1003` branch is
  skipped), gate the provider-failure branch behind an explicit completion-
  evidence check — reuse `_task_completed_before_overrun(output_path)`: if
  substantive completion is present, classify `PASS_RECOVERED` and do NOT
  re-spawn.
- **Single-session path:** same loop around `ClaudeProcess(config, phase, env_vars=…)`
  (`executor.py:1815`) before `_determine_phase_status` (`:1993`);
  ALL_ACCOUNT_COOLDOWN / cap-exhausted → `PhaseStatus.PROVIDER_EXHAUSTED`.
- **Persistence:** add top-level `halt_reason: "provider_exhaustion"` + `exhausted_model`
  to `phase-N-result.json` (`_write_phase_result_json`, `executor.py:2657-2701`);
  emit `session_reset` / `account_exhaustion_halt` events to `execution-log.jsonl`.

### Layer 5 — `~/.aienv` alias suggester + halt UX (Q2 = Enhanced) → new `aienv.py` + `models.py`

- New `aienv.py`: parse `~/.aienv` for `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL`
  and `T*Model0N` / `IC_ALIASES` exports (reuse the resolution convention from
  `src/superclaude/scripts/ic`). `suggest_alternate_model(failed_model_or_alias)`
  returns the next distinct alias (opus→sonnet; `T0Model01`→`T0Model02`).
  The cooldown body embeds the **resolved** failed model
  (`All credentials for model claude-opus-4-8 …`), so the suggester can match the
  resolved model even when `config.model` was an alias.
  > Caveat surfaced in the message: alias→account-pool mapping is operator
  > knowledge; the suggester assumes "next slot routes to a different pool."
- New `models.build_account_exhaustion_halt(config, halt_task_id, exhausted_model,
  suggested_model, remaining_tasks, ledger)` → single-line `--resume … --model <suggested>`
  + CLIProxyAPI rationale. Wire into halt output when `halt_reason ==
  provider_exhaustion`; else fall through to existing `build_resume_output`.

### Four-way discrimination (the crux)

| Category | Signature | Action |
|---|---|---|
| All-account cooldown | result 429 + `/All credentials … cooling down via provider/` | **Halt + model switch (fast path, any attempt)** |
| Single-account limit | result 429 + `would exceed your account's rate limit` | Re-spawn (rotate), bounded by cap → then halt |
| Operation timeout | `is_error` + `api_error_status==null` + timeout body | Existing timeout path (unchanged) |
| Genuine task failure | `is_error`, substantive tokens, **no** 429 body | Existing FAIL_TERMINAL/FAIL_RECOVERABLE; **no re-spawn** |

---

## 5. Edge cases & failure modes

1. **Completed-then-trailing-429** — the `:1003` completion-evidence gate
   (`_task_completed_before_overrun`, reused in the provider-failure branch per §4
   Layer 4) wins → `PASS_RECOVERED`, no re-spawn (ordering rule). Since
   `detect_provider_failure` keys on the LAST result event, this guard is what
   prevents re-spawning a task that finished before the trailing 429.
2. **Shifting failure across attempts** (single-429 → cooldown → real bug) — classify by the *last* attempt; cooldown fast-path or cap stops the loop.
3. **Parallel spawn storm** — global latch halts once. The spawn runs UNLOCKED, so
   the latch is checked under `lock` immediately before each spawn and tripped under
   `lock` after a HALT_MODEL_SWITCH; up to `K−1` workers may be mid-spawn when it
   trips. Realistic bound: **total spawns ≤ cap + (K−1)** and strictly **< K × cap**
   (no storm) — NOT strictly `≤ cap` under genuine parallelism.
4. **Cross-run budget poisoning** — reset budget is per-run/in-memory; NOT folded into cumulative `recovery_history` (Q4), so an account freed by next run gets a fresh budget.
5. **Torn/partial transcript** on a killed subprocess — detector degrades to NONE (no false re-spawn); mirror existing OSError tolerance.
6. **`api_retry` already at `max_retries==10`** — CLI burned its in-session retries; go straight to new session/model switch (no sprint-level in-session retry).
7. **No alternate alias in `~/.aienv`** — message must not fabricate one; show exhausted model + generic guidance (wait for window, add accounts, or switch alias if available).
8. **`error_max_turns` vs 429** — distinct; detector excludes budget exhaustion.
9. **Infinite-loop guard** — cap + latch; an always-429 single-account factory terminates in exactly `cap` spawns (test-asserted).
10. **`subtype:"success"` trap** — never key on `subtype` for error detection; use `is_error` + `api_error_status`.

---

## 6. Test plan (synthetic + real-derived fixtures)

**Fixtures** (`tests/.../fixtures/exhaustion/`, authored from the verbatim
ground-truth JSON; on Octodive copy the real transcripts as-is):
- `single_account_429.jsonl` (← T03.14 minimal) — result 429 + "would exceed your account's rate limit"
- `all_account_cooldown.jsonl` (← T03.13, num_turns=25) — result 429 + "All credentials … cooling down via provider claude" (+ real prior tokens)
- `operation_timeout.jsonl` (← T03.05) — `api_error_status==null` + timeout body
- `api_retry_maxed.jsonl` — `api_retry` events up to `attempt==max_retries==10`
- `task_failure_real.jsonl` — `is_error:true`, substantive tokens, real error, **no** 429 body
- `clean_pass.jsonl` — success envelope

**Unit** — `detect_provider_failure` returns the right `ProviderFailure` + resolved
model per fixture; tolerant of truncated/empty; confirms it ignores `subtype`.

**Policy** — `SessionResetPolicy.decide` truth table over (signal × attempt),
incl. cooldown-on-first-attempt → immediate HALT_MODEL_SWITCH.

**Executor (via `subprocess_factory` seam)** — scripted factory writes a per-attempt
transcript:
- single-429 → clean ⇒ PASS, `session_resets==1` persisted
- cooldown on attempt 1 ⇒ halt with `FAIL_PROVIDER_EXHAUSTED`, **0 extra spawns**
- single-429 × cap ⇒ halt; `halt_reason==provider_exhaustion`
- single-429 → real-failure ⇒ second attempt classified normally (no further re-spawn)
- K>1 all-429 ⇒ single latch halt; **assert total spawns < K × cap AND ≤ cap + (K−1)**
  (no storm; the unlocked spawn admits up to K−1 in-flight overshoots)
- always-429 single ⇒ exactly `cap` spawns (no infinite loop)

**Resume-safety** — `phase-N-result.json` fixture with `FAIL_PROVIDER_EXHAUSTED` ⇒
`ResumePlanner.rerun_task_ids` includes it; phase NOT classed `COMPLETE`.

**UX golden-string** — `build_account_exhaustion_halt` output is single-line for the
resume command, names the exhausted model, suggests a distinct alias, includes the
CLIProxyAPI rationale; **doc⇆CLI parity test** asserting the suggested flags exist
in `sprint run --help`.

**`aienv.py`** — parse a fixture `~/.aienv`; `suggest_alternate_model` returns the
next distinct alias for opus and for `T0Model01`; returns None-safe when no alt.

**Back-compat** — old `phase-N-result.json` (no new fields) round-trips through
`TaskResult.from_dict`.

---

## 7. Phased implementation plan (MDTM-ready)

| Phase | Scope | Risk | Gate |
|---|---|---|---|
| **P1** | `detect_provider_failure` + `ProviderFailure` enum + 6 fixtures + unit tests. **Zero behavior change.** | Low | Detector unit tests green (incl. subtype-trap + timeout-separation) |
| **P2** | `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (+is_failure, to_dict/from_dict back-compat) + `PhaseStatus.PROVIDER_EXHAUSTED` + align `_classify_transcript` to shared detector + resume-safety tests | Low-Med | Resume re-runs exhausted task; back-compat round-trip |
| **P3** | `recovery_policy.SessionResetPolicy` (cap default 8, fast-path) + re-spawn loop in `_run_one_task` + global latch for K>1 + persist `session_resets`/`failure_class`/`exhausted_model`/`halt_reason` | **High** (live control flow + concurrency) | Factory scenarios incl. no-storm / no-loop / cooldown-fast-path |
| **P4** | Single-session phase path: re-spawn loop + `PROVIDER_EXHAUSTED` in `_determine_phase_status` | Med | Single-session cooldown → halt; single-429×cap → halt |
| **P5** | `aienv.py` alias suggester + `build_account_exhaustion_halt` + wire into halt + `--max-session-resets` flag (default 8) + CLI doc + doc⇆CLI parity | Med | Golden-string + parity + aienv unit tests |
| **P6** | `execution-log.jsonl` events, KNOWLEDGE.md note, telemetry | Low | Events emitted |

**SoT discipline:** all edits in `src/superclaude/cli/sprint/` → `make sync-dev` →
`make verify-sync`; `uv run ruff format --check src/ tests/` before push; feature
branch only; PR to `IronbellyOrg/IronClaude` with `--repo`.

---

## 8. Resolved decisions (Q1–Q5)

- **Q1** — Signature pinned from real transcripts (§2): structured-field detection +
  two-body discrimination + cooldown fast-path; stdout-only; ignore `subtype`.
- **Q2** — **Enhanced**: `~/.aienv` reader enumerates aliases and suggests the next
  slot; assumes next slot routes to a different pool (caveat surfaced in message).
- **Q3** — **New status** `FAIL_PROVIDER_EXHAUSTED` (+ `PhaseStatus.PROVIDER_EXHAUSTED`).
- **Q4** — Reset budget is **per-run / in-memory**, independent of cross-run
  `recovery_history` cap-3.
- **Q5** — Reset cap **scales toward pool size** (default 8); the all-account-cooldown
  body is the primary terminator, the cap is the backstop for pathological
  single-account loops that never escalate to cooldown.
