---
topic: "Make superclaude sprint 429/account-exhaustion recovery ALWAYS engage: harden the monitor.py provider-failure detector against real CLIProxyAPI transcript shapes (429-as-text with subtype 'success', missing api_error_status field, 'cooling down' body without 'via provider') so the existing PR #183 re-route/model-switch machinery fires instead of silently failing the phase."
domain: code
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: design
created: 2026-07-02T16:52:20Z
ground_truth: .dev/troubleshoot/429-signature-ground-truth.md
---

# Seed Brief: sprint 429 detector hardening

## Problem Statement

A `superclaude sprint run` phase halted with every task failing `FAIL_TERMINAL` during
an all-account 429 cooldown, even though PR #183 shipped a full 429/account-exhaustion
recovery subsystem (re-route on single-account limit; halt-with-model-switch on
all-account cooldown). The recovery **never engaged** (`session_resets=0`, empty
`exhausted_model`). Root cause is in the **detection layer only**: the provider-failure
classifier's entry predicate is coupled to a structured `api_error_status == 429` field
that the real CLIProxyAPI transcript does not carry, and its all-account regex requires a
`via provider` suffix the real body omits. The downstream taxonomy, policy, status, and
resume machinery are correct — they simply never receive a non-`NONE` signal.

## Known Context (verified against current source, 2026-07-02)

- **Single detection choke point:** `_provider_failure_from_text` (`monitor.py:291-345`).
  Entry predicate at `monitor.py:323` is `is_error and api_error_status == 429`.
- **Shared by both paths (single source of truth):** live `detect_provider_failure`
  (`monitor.py:348`) and offline `_classify_transcript` (`rerun_tasks.py:552`, calls the
  shared inner at `:592`) both delegate to `_provider_failure_from_text`. Hardening that one
  function fixes live + offline together.
- **Consumer chain is correct:** `SessionResetPolicy.decide` (`recovery_policy.py:76-96`):
  `ALL_ACCOUNT_COOLDOWN → HALT_MODEL_SWITCH` (any attempt); `SINGLE_ACCOUNT_LIMIT →
  RETRY_NEW_SESSION` under budget. Wired at `executor.py:1085` (K>1) and `:2283` (K=1).
- **Resume machinery is correct:** `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (`models.py:53`, in
  `is_failure` set `:66`); `SprintResult.resume_command` (`models.py:880`) →
  `suggest_alternate_model(exhausted_model)` (`aienv.py:81`). It only needs the detector to
  capture the resolved model string.

## The two REAL transcript shapes (both verified verbatim)

| Field | Shape 1 — "Request rejected" (June, ground-truth.md L18-31; = all 6 fixtures) | Shape 2 — "API Error: 429" (July incident raw logs) |
|---|---|---|
| `is_error` | `true` | `true` (both shapes share this) |
| `api_error_status` | `429` present | **absent** |
| result prefix | `API Error: Request rejected (429) · ` | `API Error: 429 {…}` |
| all-account body | `All credentials for model claude-opus-4-8 are cooling down **via provider** claude` | `All credentials for model gpt-5.5 are cooling down` (no "via provider") |
| nested envelope | `b'{…"type":"rate_limit_error"…}'` | `{"error":{"message":"b'{…rate_limit_error…}'","code":"429"}}` |
| model | `claude-opus-4-8` | `gpt-5.5` |
| Shared robust tokens | `is_error:true` + `rate_limit_error` in body | `is_error:true` + `rate_limit_error` in body |

**Two confirmed gaps:**
1. **(load-bearing)** `api_error_status` is absent in Shape 2 → conjunct `is_error and
   api_error_status == 429` fails → returns `NONE` → `decide()` returns `CONTINUE` → phase
   cascades to `FAIL_TERMINAL`. (`is_error` is genuinely `true`; the preamble's guess that it
   was false is wrong — the absent structured field is the real breaker.)
2. **(secondary)** `_RE_ALL_ACCOUNT` requires `via provider` (`monitor.py:41-43`); Shape 2
   omits it → even if the gate opened, it would hit the `429-with-neither-body →
   SINGLE_ACCOUNT_LIMIT` default (`:332-333`) → wrong `RETRY_NEW_SESSION` instead of
   `HALT_MODEL_SWITCH`, plus no model captured for the resume hint.

## Constraints (locked by user decisions + source facts)

- **C1 — Gate signal:** harden to `is_error==true AND (api_error_status==429 OR
  'rate_limit_error' in result body)`. `rate_limit_error` appears verbatim in both real
  shapes and is unlikely in benign task output (lowest false-positive basis).
- **C2 — Keep structured field as a corroborating fast-path**, not a replacement — zero
  regression to the 6 currently-passing Shape-1 fixtures.
- **C3 — Scope strictly to the 429 provider detector** (`_provider_failure_from_text` +
  `_RE_ALL_ACCOUNT`/`_RE_SINGLE_ACCOUNT` + fixtures/tests). Sibling detectors
  (`detect_error_max_turns`, `detect_prompt_too_long`) share the coupling but have no
  drift evidence — document as a follow-up, do NOT touch now.
- **C4 — Preserve the taxonomy + back-compat serialization** exactly (4 `ProviderFailure`
  kinds; `ProviderFailureSignal(kind, resolved_model)`; `TaskResult` field defaults).
- **C5 — False-positive guard:** the text signal must be scoped to the terminal
  `{"type":"result"}` event body (the existing last-result-event parse), never an
  arbitrary transcript-wide scan.
- **C6 — Detect on stdout only** (stderr is 0 bytes for 429s); torn/partial transcript
  degrades to `NONE` (no false re-spawn) — preserve current OSError/empty tolerance.
- **C7 — No new flags, config surface, or subsystems.** Reliability/correctness fix only.
- **C8 — All-account regex must drop the `via provider` requirement** while still
  capturing the resolved model non-greedily (`All credentials for model (?P<model>.+?)
  are cooling down`), matching BOTH shapes.

## Success Criteria (observable)

- **SC1:** `detect_provider_failure` returns `ALL_ACCOUNT_COOLDOWN` with
  `resolved_model="gpt-5.5"` on the verbatim Shape 2 incident transcript.
- **SC2:** offline `_classify_transcript` maps the same Shape 2 transcript to
  `FAIL_PROVIDER_EXHAUSTED` (not `FAIL_TERMINAL`).
- **SC3:** all 6 existing Shape-1 fixtures + `test_monitor.py`/`test_recovery_policy.py`
  assertions still pass unchanged (fast-path preserved).
- **SC4:** a verbatim Shape 2 fixture (all-account gpt-5.5) is added under
  `tests/sprint/fixtures/exhaustion/`, plus a shape-variant **detection-contract table
  test** asserting the classifier fires across the permutation matrix
  (`api_error_status` present/absent × `via provider` present/absent × prefix variant).
- **SC5:** false-positive guard proven — a task whose own successful output contains the
  literal `429`/`rate limit` (but `is_error:false`) classifies as `NONE`.
- **SC6:** no changes outside the detection layer + tests/fixtures; `make lint` +
  `ruff format --check` + `make verify-sync` clean.

## Open Questions (adversarial debate seeds)

- **OQ1 — Body-match locus & escaping:** the Shape 2 `rate_limit_error` / model phrase sits
  inside a nested, escaped Python-bytestring-repr (`b'{\"…\"}'`). Is a raw-substring/regex
  match on the once-`json.loads`-decoded `result` string sufficient and safest, or is any
  nested-JSON unescaping warranted? (Hypothesis: raw substring is sufficient and
  over-parsing is over-engineering — pressure-test.)
- **OQ2 — Single-account Shape 2 variant is uncaptured.** We have Shape 2 all-account
  verbatim but not a Shape 2 single-account body. Should the design assume it mirrors
  Shape 1's `would exceed your account's rate limit` phrasing, and how conservative should
  the `429-with-neither-body` default remain (currently `SINGLE_ACCOUNT_LIMIT`)?
- **OQ3 — Fast-path cascade:** the raw logs show 5 tasks each independently hitting the
  same all-account 429 and cascading. Detection alone fixes each task's classification —
  does the phase-level halt already short-circuit the cascade once the first task returns
  `ALL_ACCOUNT_COOLDOWN`, or is that purely a policy/executor concern out of scope here?
- **OQ4 — Contract-test shape:** exact matrix dimensions + whether to assert the captured
  `resolved_model` per row (guards the model-capture regression that feeds the resume hint).
- **OQ5 — Operation-timeout exact-match brittleness:** the timeout branch (`monitor.py:338`)
  uses `body == "API Error: The operation timed out."` exact equality — in scope to note as
  a sibling brittleness follow-up, or explicitly out of scope per C3?

## Enrichment Context

Codebase enrichment: **primary** (Auggie/grep/Read over `monitor.py`, `recovery_policy.py`,
`rerun_tasks.py`, `executor.py`, `models.py`, `aienv.py`, the 6 exhaustion fixtures,
`test_monitor.py`, `test_recovery_policy.py`, and both ground-truth artifacts). Research
enrichment: **skipped** (self-contained internal detector; no external framework docs
needed). Full grounding table lives in this brief's Known Context + the two-shape table;
verbatim shapes in `.dev/troubleshoot/429-signature-ground-truth.md` and the July raw logs.
