---
title: "Sprint 429 Detector Hardening — Merged Requirements Spec"
domain: code
strategy: systematic
depth: deep
status: ready-for-design
created: 2026-07-02
source: /sc:brainstorm --codebase --depth deep --interactive --blind --handoff design
adversarial_convergence: 0.90
base_variant: variant-1 (architect); harvested refactorer + qa
ground_truth: .dev/troubleshoot/429-signature-ground-truth.md
provenance: merged by /sc:adversarial from 3 blind variants (architect/refactorer/qa)
---

# Sprint 429 Detector Hardening — Merged Requirements Spec

<!-- Provenance: produced by /sc:adversarial; Base = Variant 1 (architect); merged 2026-07-02 -->

## 1. Problem statement

A `superclaude sprint run` phase halted with **every task failing `FAIL_TERMINAL`** during an
all-account 429 cooldown, even though PR #183 shipped a complete 429/account-exhaustion recovery
subsystem. Recovery **never engaged** (`session_resets=0`, empty `recovery_history`, empty
`exhausted_model`). The defect is confined to the **detection layer**: the provider-failure
classifier's entry predicate is coupled to a structured `api_error_status == 429` field that the
real CLIProxyAPI transcript does not always carry, and its all-account regex requires a `via
provider` suffix the real body omits. The taxonomy, policy, status, resume machinery, and offline
mirror are all correct — they simply never receive a non-`NONE` signal.

<!-- Source: Base (original) -->

## 2. Complexity sizing verdict (two-axis)

**Production surface: NARROW.** The mandated source change is **two hunks in one file**
(`src/superclaude/cli/sprint/monitor.py`): widen the entry predicate (~1 expression at `:323`) and
loosen `_RE_ALL_ACCOUNT` (`:41-43`). One function edit fixes **both** the live and offline paths,
because `_classify_transcript` (`rerun_tasks.py:592`) already delegates to the same inner. No new
enum kind, no new field, no config knob, no new module. Size is set by **blast radius, not line
count**: the fix sits upstream of every stable contract, all of which stay byte-unchanged.

**Verification surface: MEDIUM.** The incident's real cost was the gap between "tests green" and
"recovery fires" — the fixtures fabricated the shape the detector expected. Closing that gap is a
C-class effort: 3 new fixtures + an ~12-row parametrized detection-contract table + 4 live/offline
parity assertions. This is deliberately larger than the production diff and is the point of the
work.

**Sizing → solution shape.** A hardened detector predicate + one relaxed regex + a shape-variant
contract test. Explicitly NOT a new subsystem, taxonomy, or config surface (§5), and explicitly NOT
a single-regex patch or single fixture (§10). The two axes are why: the fix is small; the *contract
it must honor going forward* is what earns the test investment.

<!-- Source: Variant 2 (refactorer) + Variant 3 (qa), merged per Change #1, #6 -->

## 3. Grounding evidence (verified against current source, 2026-07-02)

**The two real transcript shapes** (both verbatim-verified; Shape 1 in
`.dev/troubleshoot/429-signature-ground-truth.md`, Shape 2 in the July incident raw logs):

| Field | Shape 1 — "Request rejected" (June; = all 6 fixtures) | Shape 2 — "API Error: 429" (July incident; unhandled) |
|---|---|---|
| `is_error` | `true` | `true` (**both shapes share this**) |
| `api_error_status` | `429` present | **absent** |
| result prefix | `API Error: Request rejected (429) · ` | `API Error: 429 {…}` |
| all-account body | `All credentials for model claude-opus-4-8 are cooling down **via provider** claude` | `All credentials for model gpt-5.5 are cooling down` (no "via provider") |
| nested envelope | `b'{…"type":"rate_limit_error"…}'` | `{"error":{"message":"b'{…rate_limit_error…}'","code":"429"}}` |
| model | `claude-opus-4-8` | `gpt-5.5` |
| **shape-robust tokens** | `is_error:true` + `rate_limit_error` ∈ body | `is_error:true` + `rate_limit_error` ∈ body |

**Choke point & consumer chain** (all line numbers current):
- Detector inner: `_provider_failure_from_text` (`monitor.py:291-345`); entry predicate `:323`;
  all-account regex `:41-43`; `429-with-neither-body → SINGLE_ACCOUNT_LIMIT` default `:332-333`.
- Live wrapper `detect_provider_failure` (`monitor.py:348`) → consumed `executor.py:1085` (K>1) and
  `:2283` (K=1) **before** the normal status ladder.
- Policy `SessionResetPolicy.decide` (`recovery_policy.py:76-96`): `ALL_ACCOUNT_COOLDOWN →
  HALT_MODEL_SWITCH` (any attempt); `SINGLE_ACCOUNT_LIMIT → RETRY_NEW_SESSION` under budget.
- Status `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (`models.py:53`, in `is_failure` `:66`).
- Resume `SprintResult.resume_command` (`models.py:880`) → `suggest_alternate_model(exhausted_model)`
  (`aienv.py:81`) — needs only the detector to capture the resolved model string.
- **Shared inner**: offline `_classify_transcript` (`rerun_tasks.py:552`, calls inner `:592`) →
  hardening the one function fixes both paths.

**Two confirmed gaps:** (G1, load-bearing) `api_error_status` absent in Shape 2 → conjunct fails →
`NONE` → `decide` returns `CONTINUE` → phase cascades to `FAIL_TERMINAL`. (`is_error` is genuinely
`true`; the absent structured field is the breaker.) (G2, secondary) `_RE_ALL_ACCOUNT` requires `via
provider`; Shape 2 omits it → even with the gate open, it hits the SINGLE_ACCOUNT_LIMIT default →
wrong `RETRY_NEW_SESSION` + no captured model for the resume hint.

<!-- Source: Base (original), enriched with Variant 2/3 line citations -->

## 4. Requirements

### R1 — Entry-predicate hardening (C1) [load-bearing]
Widen the 429 branch gate from `is_error and api_error_status == 429` to:

```
enter_429_branch  IF  is_error == true
                  AND ( api_error_status == 429           # structured fast-path (C2)
                        OR  "rate_limit_error" in body )   # text primary/fallback
```

`body = str(result_event.get("result", ""))` (already in scope at `:321`). The `rate_limit_error`
disjunct is **inlined** — no `_is_rate_limited()` helper (one-caller ceremony for a 2-term boolean).
Membership test is a plain `"rate_limit_error" in body`, NOT a regex, NOT a JSON-path extraction.

### R2 — All-account regex loosening (C8) [secondary gap]
`_RE_ALL_ACCOUNT` becomes `r"All credentials for model (?P<model>.+?) are cooling down"` (drop `via
provider`), still non-greedily capturing the resolved model. Matches BOTH shapes; `_RE_SINGLE_ACCOUNT`
(`would exceed your account's rate limit`) is unchanged.

### R3 — Structured field stays as fast-path; back-compat by construction (C2)
`api_error_status == 429` is evaluated FIRST in the disjunction. The new match set is a **superset**
of the old (`old_match ⊆ new_match`): any transcript the old predicate caught, the new one still
catches via the same fast-path. This is the formal guarantee that all 6 Shape-1 fixtures and every
`test_monitor.py`/`test_recovery_policy.py` assertion pass unchanged.

### R4 — False-positive guard (C5) + documented residual
The text scan is scoped to the LAST `{"type":"result"}` event's `result` field only — never a
transcript-wide scan. This is **load-bearing** (invariant-probe INV-004): it prevents a task whose
prose mentions rate-limiting (but whose terminal result is a timeout or success) from tripping the
gate. **Documented residual (INV-001):** a task that itself fails (`is_error:true`) with an
incidental `rate_limit_error` substring in its own result body and no provider body → one spurious
`RETRY_NEW_SESSION` via the neither-body default. Bounded (one re-spawn; then success or budget halt),
improbable (`rate_limit_error` is an underscored error-TYPE token, not natural prose), and accepted —
NOT hardened into a co-required-429 gate (the user chose the `OR` form).

### R5 — Scope discipline (C3)
Change ONLY `_provider_failure_from_text` + `_RE_ALL_ACCOUNT` (+ tests/fixtures). Sibling detectors
`detect_error_max_turns` and `detect_prompt_too_long` share the same structured-field coupling but
have **no drift evidence** — recorded as a debt-ledger follow-up (§7), NOT touched now.

### R6 — Single source of truth (both paths)
The change lives in the shared inner so live (`detect_provider_failure`) and offline
(`_classify_transcript`) agree. Tests MUST assert both (§6.3).

### R7 — Model capture feeds resume
The captured `resolved_model` (Shape 2 → `gpt-5.5`) must flow to `ProviderFailureSignal.resolved_model`
so `resume_command` can suggest an alternate alias. Tests assert the model per row (§6.2).

<!-- Source: Base (architect) R1/R3/R5/R6; Variant 2 (refactorer) inline/substring in R1, R4 residual; invariant-probe INV-001/INV-004 -->

## 5. Changes we are NOT making (anti-over-engineering ledger)

Each rejected against a locked constraint or verified fact:

1. **No nested-JSON / bytestring unescaping** (OQ1). `rate_limit_error` and `All credentials…cooling
   down` survive literally into the once-`json.loads`-decoded `result` string; a recursive unescaper
   only adds a raise path that violates C6 (torn → NONE, never crash).
2. **No new `ProviderFailure` kind / no `TaskStatus` addition.** The 4-kind taxonomy already covers
   the incident; Shape 2 is the same ALL_ACCOUNT_COOLDOWN semantics, not a new class (C4).
3. **No config knob / flag** for wording variants (C7). The contract table absorbs new shapes as data.
4. **No `_is_rate_limited()` helper / strategy object / matcher registry** — one-caller ceremony (C7).
5. **No sibling-detector refactor** (C3) — no drift evidence for `error_max_turns`/`prompt_too_long`.
6. **No generic "provider error taxonomy"** — speculative; the evidence is exactly two 429 shapes.
7. **No phase-cascade short-circuit / policy change** (OQ3). `decide` already HALTs on the first
   all-account; the K>1 storm bound (`cap + (K-1)`) is existing correct policy behavior, out of scope.
8. **No timeout-branch edit** (OQ5). Proved unreachable for 429s (§7) — left byte-unchanged; only a
   guard test is added.
9. **No property/fuzz suite.** The bug was a missing *dimension*, not a missing edge (§10).

<!-- Source: Variant 2 (refactorer), Section "Changes We Are Not Making"; item 9 from Variant 3 (qa) -->

## 6. Test & fixture plan

### 6.1 New fixtures (`tests/sprint/fixtures/exhaustion/`)
- `all_account_cooldown_apierror429.jsonl` — **verbatim Shape 2** all-account (`gpt-5.5`, no
  `api_error_status`, no "via provider", nested LiteLLM envelope). The load-bearing regression fixture.
- `provider_429_incidental_ratelimit_text.jsonl` — FP guard: `is_error:false`, result body contains
  literal `429`/`rate limit` prose → expected `NONE`.
- `single_account_apierror429_SYNTHESIZED.jsonl` — Shape-2 single-account **assumption breakpoint**
  (no verbatim capture exists; OQ2). Clearly named `_SYNTHESIZED`; documents the assumed
  `would exceed your account's rate limit` phrasing; flips to a loud failure if a real capture later
  contradicts it.

### 6.2 Detection-contract table test (the centerpiece)
A parametrized test over the matrix `api_error_status {429 | absent | null} × via-provider {present |
absent} × prefix {Request-rejected | API-Error-429}`. Every row asserts `(kind, resolved_model)`.
Empty/impossible cells are explicit `xfail`/skip with a reason — never silent omissions, so a THIRD
drift maps to exactly one visible failing row.

| # | is_error | api_error_status | body signature | Expected kind | Expected model | Source |
|---|---|---|---|---|---|---|
| 1 | true | 429 | Shape1 all-account (via provider) | ALL_ACCOUNT_COOLDOWN | claude-opus-4-8 | existing fixture |
| 2 | true | 429 | Shape1 single-account | SINGLE_ACCOUNT_LIMIT | None | existing |
| 3 | true | 429 | Shape1 api_retry_maxed (single) | SINGLE_ACCOUNT_LIMIT | None | existing |
| 4 | true | **absent** | **Shape2 all-account (no via provider)** | ALL_ACCOUNT_COOLDOWN | **gpt-5.5** | **NEW (load-bearing)** |
| 5 | true | 429 | all-account **without** "via provider" | ALL_ACCOUNT_COOLDOWN | X | synthetic (C8 ⟂ aes) |
| 6 | true | **absent** | Shape1 all-account **with** "via provider" | ALL_ACCOUNT_COOLDOWN | claude-opus-4-8 | synthetic (C1 text gate) |
| 7 | true | absent | Shape2 single-account (rate_limit_error + "would exceed…") | SINGLE_ACCOUNT_LIMIT | None | NEW synthesized (OQ2) |
| 8 | true | absent | rate_limit_error present, neither all/single body | SINGLE_ACCOUNT_LIMIT | None | default (`:332-333`); INV-001 residual |
| 9 | **false** | null/absent | "429"/"rate limit" incidental prose | **NONE** | None | NEW FP fixture |
| 10 | true | null | "API Error: The operation timed out." | OPERATION_TIMEOUT | None | existing (timeout T1) |
| 11 | true | absent | `error_during_execution` "pytest exited 1" (no rate_limit_error) | NONE | None | existing (real task fail ≠ provider) |
| 12 | false | null | "Task complete." | NONE | None | existing clean_pass |

### 6.3 Live/offline parity (4 assertions)
1. `detect_provider_failure(path)` == `_provider_failure_from_text(path.read_text())` on the Shape-2
   fixture (extends existing `test_monitor.py:339-343`).
2. `_classify_transcript(shape2_text)` → `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (SC2) — the currently
   **untested seam**.
3. `_classify_transcript` on the FP fixture → NOT `FAIL_PROVIDER_EXHAUSTED`.
4. Completion-evidence intercept: a Shape-2 transcript with prior `success` envelope then trailing
   429 → `PASS_RECOVERED` (unchanged), proving R-gate ordering survives the new shape.

### 6.4 Regression & guard tests
- All 6 existing fixtures + `test_recovery_policy.py` truth table pass unchanged (R3).
- **Timeout unreachability test (F5):** assert a 429 body never reaches the timeout branch — every
  `is_error` 429 returns inside the 429 block before `:335`.
- **Scope-discipline note:** the `decide()` 7-row truth table is the *policy's* contract
  (`test_recovery_policy.py`) and must NOT be duplicated in the detector suite (C3 applies to tests).

<!-- Source: Variant 3 (qa), Sections 2-5; matrix rows reconciled with invariant-probe INV-001 (row 8) -->

## 7. Risk analysis & debt ledger

- **FP residual (INV-001)** — MEDIUM likelihood-weighted-LOW: bounded to one re-spawn; mitigated by
  C5 scoping + FP fixture; accepted, not engineered away.
- **C5 is load-bearing (INV-004)** — result-body scoping is what prevents timeout/incidental-text
  bleed; it gets an explicit interaction test, not just a comment.
- **Sufficiency proven (INV-005)** — post-fix branch-trace shows detection is the ONLY closed gate;
  the consumer chain is already correct and wired, so the fix ALONE makes recovery engage.
- **Debt ledger (do NOT fix now, record):** (a) sibling detectors `detect_error_max_turns` /
  `detect_prompt_too_long` share the structured-field coupling (C3 follow-up); (b) timeout branch
  exact-match `body == "API Error: The operation timed out."` (`:335-338`) is the same brittleness
  class (OQ5) — pinned as contract-table row T1 so a future hardening has a breakpoint.

<!-- Source: invariant-probe.md; Variant 1 (architect) §4.3 debt-ledger; Variant 3 (qa) OQ5 pin -->

## 8. Open questions — resolved

- **OQ1 (nested escaping):** raw substring on the once-decoded `result` string is sufficient and
  safest; reject nested unescaping (adds a C6-violating crash mode).
- **OQ2 (Shape-2 single-account uncaptured):** synthesize a clearly-named breakpoint fixture asserting
  the assumed `would exceed…` phrasing; it fails loudly if a real capture contradicts.
- **OQ3 (fast-path cascade):** out of scope — `decide` already HALTs on first all-account; K>1 bound
  is existing policy.
- **OQ4 (contract-test shape):** assert `resolved_model` per row (incl. `None` on non-cooldown rows) to
  guard the greedy-regex regression that feeds the resume hint.
- **OQ5 (timeout exact-match):** out of scope per C3; pinned as row T1 for a future pass.

## 9. Acceptance criteria (mapped to seed-brief SC1-SC6)

- **AC1 (SC1):** `detect_provider_failure` returns `ALL_ACCOUNT_COOLDOWN`, `resolved_model="gpt-5.5"`
  on the verbatim Shape-2 fixture.
- **AC2 (SC2):** `_classify_transcript` maps the same transcript to `FAIL_PROVIDER_EXHAUSTED`.
- **AC3 (SC3):** all 6 Shape-1 fixtures + existing assertions pass unchanged.
- **AC4 (SC4):** Shape-2 fixture + the ~12-row contract table land; empty cells are explicit xfail.
- **AC5 (SC5):** the `is_error:false` incidental-429 fixture classifies as `NONE`.
- **AC6 (SC6):** no change outside the detection layer + tests/fixtures; `make lint`,
  `uv run ruff format --check src/ tests/`, and `make verify-sync` clean.

## 10. Anti-over / anti-under-engineering (explicit)

- **Against over-engineering:** the 9-item ledger (§5). The temptations are a generic taxonomy, a
  config knob, a helper/registry, nested parsing, and a sibling refactor — every one exceeds the
  two-shape evidence. No line ships unless it maps to a verbatim-verified transcript.
- **Against under-engineering:** a lone `via provider` regex tweak leaves G1 open (absent
  `api_error_status` → gate never opens → incident recurs); a single Shape-2 fixture re-creates the
  fabrication that caused the incident. Both hunks + the contract table are mandatory.

## 11. Handoff

Ready for `/sc:design @merged-requirements.md` to formalize the detector-contract architecture (the
predicate, the regex, the contract-table test harness) and the fixture set before implementation.
Recommended implementer scope: the two `monitor.py` hunks, 3 fixtures, the contract-table test,
4 parity assertions, and the F5 unreachability test — one focused PR on `DetectionContractBranch`.
