# Variant 1 — Systems-Architect Lens: The 429 Detection Contract

**Task:** Harden `superclaude sprint`'s provider-failure detector so PR #183's 429/account-exhaustion recovery ALWAYS engages, by inverting a brittle structured-field dependency into a resilient text-primary detection **contract** with the structured field retained as a corroborating fast-path.

**Deliverable:** requirements/design spec (not code). Scope locked by C1–C8; ground truth verified against source 2026-07-02.

---

## 1. Objective Complexity Sizing Verdict

**Verdict: SMALL — one-function surgical change + one regex literal + fixture/contract-test expansion. ~2500-token / "complex-single-unit" budget, NOT a feature.**

Justification through the architect lens — sizing is a function of *blast radius*, not line count:

- **One choke point, two consumers, zero new surface.** The entire behavioral change lives in `_provider_failure_from_text` (`monitor.py:291-345`) plus one module-level regex literal (`_RE_ALL_ACCOUNT`, `monitor.py:41-43`). Both the live path (`detect_provider_failure` → `executor.py:1085`/`:2283`) and the offline path (`_classify_transcript` → `rerun_tasks.py:592`) delegate to this single inner. **Confirmed at source:** `rerun_tasks.py:592` calls `_provider_failure_from_text(text)` and gates on `{SINGLE_ACCOUNT_LIMIT, ALL_ACCOUNT_COOLDOWN}` at `:593-596`. This is textbook single-source-of-truth: the fix cost is O(1) in consumers.
- **No taxonomy, policy, status, or serialization change.** `ProviderFailure` (4 kinds), `ProviderFailureSignal(kind, resolved_model)`, `SessionResetPolicy.decide`, `TaskStatus.FAIL_PROVIDER_EXHAUSTED`, and the `resume_command` chain all stay byte-identical. The change is *upstream of* every stable contract; it only widens what reaches an already-correct machine.
- **The risk is not "will it work" — it is "will it regress the 6 passing Shape-1 fixtures."** That risk is fully controllable by keeping the structured predicate as a disjunct fast-path (C2). So the *engineering* is small; the *diligence* (contract table, false-positive proof) is where the effort concentrates — which is exactly the right place for a detector that silently failed once already.

**Why not larger:** treating this as a "detection subsystem redesign" (pluggable matchers, a signal registry, a config-driven pattern table) would be over-engineering a two-shape problem (§6). **Why not smaller:** a one-line predicate patch with no contract table would re-earn the same silent-drift failure the moment CLIProxyAPI emits Shape 3 — under-engineering (§6).

---

## 2. The Detection-Layer Change — Requirements + Literals + Predicate Pseudocode

### 2.1 The architectural reframe: brittle structured dependency → resilient text-primary contract

The defect is a **coupling defect**, not a regex defect. Today the detector's entry gate (`monitor.py:323`, `if is_error and api_error_status == 429:`) treats a *structured, provider-emitted, optional* field as a *load-bearing precondition*. That inverts the reliability hierarchy: the detector's job is to survive whatever the proxy emits, but it delegated its own liveness to a field the proxy is free to omit — and did omit in Shape 2. The all-account regex compounds it by hard-coding a `via provider` suffix that is a *presentation* detail of one proxy build, not a *semantic* invariant.

The corrected architecture states the semantic invariant first and treats structured fields as *accelerators*, never *gatekeepers*:

> **Semantic invariant (the contract's meaning):** "A terminal result event that errored AND whose body carries the provider's rate-limit signature is a provider 429." The rate-limit signature is the durable token `rate_limit_error`, present verbatim in BOTH real shapes (`ground-truth.md`; July raw logs). The structured `api_error_status==429` is one *corroboration* of that invariant, not its definition.

### 2.2 Requirements (normative)

- **R1 (gate inversion, load-bearing).** The entry gate MUST fire when `is_error==true AND (api_error_status==429 OR 'rate_limit_error' in body)`. This is a disjunction: the structured field is now ONE of two independent sufficient conditions, neither necessary. Satisfies C1.
- **R2 (fast-path preservation).** When `api_error_status==429` is present (Shape 1), the classifier MUST produce byte-identical output to today's code. The structured branch is retained as the FIRST-evaluated corroborator so the 6 Shape-1 fixtures see zero behavioral delta. Satisfies C2. This is the anti-regression keystone.
- **R3 (all-account regex de-brittling).** `_RE_ALL_ACCOUNT` MUST drop the `via provider` requirement while still capturing the resolved model non-greedily:
  `r"All credentials for model (?P<model>.+?) are cooling down"`.
  Non-greedy `.+?` bounded by the literal ` are cooling down` suffix captures `gpt-5.5` / `claude-opus-4-8` in both shapes without swallowing trailing text. Satisfies C8.
- **R4 (locus scoping — false-positive containment).** The `rate_limit_error` body match MUST be evaluated ONLY against the `result` field of the LAST `{"type":"result"}` event (the existing `result_event` parse at `monitor.py:302-321`), NEVER a transcript-wide scan. A task whose *successful* output prints the string `rate_limit_error` (e.g. a task editing this very file) MUST classify as `NONE` because `is_error` is false on its result event. Satisfies C5.
- **R5 (torn-transcript tolerance).** `result_event is None` (no terminal event / truncated stdout) MUST continue to return `NONE`. Preserve the existing OSError/empty tolerance in the `detect_provider_failure` wrapper (`monitor.py:348+`) and the `startswith("{")` + `json.loads` try/except line filter. Satisfies C6.
- **R6 (model capture is contractual output).** On `ALL_ACCOUNT_COOLDOWN`, `resolved_model` MUST be populated from the regex `model` group — it feeds `suggest_alternate_model(exhausted_model)` (`aienv.py:81`) for the resume hint. A match that fires but captures `None` is a silent regression and MUST be caught by the contract table (§5, R-per-row assertion).
- **R7 (no taxonomy/serialization drift).** No changes to `ProviderFailure`, `ProviderFailureSignal`, or any downstream. Satisfies C3/C4/C7.

### 2.3 Predicate pseudocode (design intent — NOT an implementation)

```
result_event = last event where type == "result"   # unchanged parse, C5/C6
if result_event is None: return NONE                # torn transcript, R5

is_error         = bool(result_event.is_error)
api_error_status = result_event.api_error_status    # may be absent → None
body             = str(result_event.result or "")

# R1: the gate is now a disjunction. Structured field OR durable text token.
rate_limited = (api_error_status == 429) or ("rate_limit_error" in body)

if is_error and rate_limited:
    # R3/C8: model-bearing all-account match, `via provider` dropped
    m = RE_ALL_ACCOUNT.search(body)          # (?P<model>.+?) are cooling down
    if m: return ALL_ACCOUNT_COOLDOWN(resolved_model = m.group("model"))   # R6
    if RE_SINGLE_ACCOUNT.search(body): return SINGLE_ACCOUNT_LIMIT
    return SINGLE_ACCOUNT_LIMIT              # neither-body default, OQ2 — unchanged, conservative

# operation-timeout branch — UNCHANGED, out of scope (C3, OQ5)
if is_error and api_error_status is None and body == "API Error: The operation timed out.":
    return OPERATION_TIMEOUT

return NONE
```

The evaluation order — all-account (model-bearing) → single-account → conservative default — is preserved exactly. Only the **gate** changed (conjunct → disjunct) and the **all-account regex** relaxed. Everything inside the `if` block is structurally identical to `monitor.py:324-333`.

---

## 3. The Detection Contract as a First-Class Boundary

This is the variant's central architectural contribution: name the contract, so the next drift is caught by a *test that already exists* rather than a *production incident*.

### 3.1 What the contract IS

**The detection contract is the mapping from `(is_error, api_error_status, body-tokens)` → `ProviderFailureSignal`.** It is defined by the disjunctive gate (R1), the two body regexes (R3 + `_RE_SINGLE_ACCOUNT`), and the conservative default. It is *provider-shape-agnostic by construction*: it keys on the durable semantic token (`rate_limit_error`) and the durable phrase stem (`are cooling down`), not on any one proxy build's punctuation, envelope nesting, or optional structured fields.

### 3.2 Who the TWO consumers are

1. **Live path** — `detect_provider_failure` (`monitor.py:348`), consumed at `executor.py:1085` (K>1 attempts) and `:2283` (K=1). Feeds `SessionResetPolicy.decide` → `HALT_MODEL_SWITCH` / `RETRY_NEW_SESSION`.
2. **Offline path** — `_classify_transcript` (`rerun_tasks.py:552`), which calls the shared inner at `:592` and gates on the two account-exhaustion kinds at `:593-596` to map to `FAIL_PROVIDER_EXHAUSTED` for `sprint rerun-tasks`.

**Architectural property being protected:** both consumers delegate to the SAME inner (`_provider_failure_from_text`). This single-source-of-truth is *why* the fix is small and *why* it must stay a single function. A future maintainer tempted to "specialize" the offline classifier with its own copy of the predicate would fork the contract and re-open exactly the live/offline divergence this design forbids. **The contract test (§5) MUST assert both consumers agree on the same transcript** so any fork is caught mechanically.

### 3.3 How it resists the NEXT drift

The 2026-06→07 incident was drift #1 (Shape 1 → Shape 2). The design must assume drift #2. Resistance is layered:

- **Semantic-token keying (R1):** keying on `rate_limit_error` (an error-taxonomy token the proxy is unlikely to rename) rather than `api_error_status` (an optional transport field) means a Shape 3 that again drops the structured field but keeps the standard rate-limit envelope is caught with **zero code change**.
- **Phrase-stem regex (R3):** matching `are cooling down` rather than `are cooling down via provider <name>` survives suffix/provider-label churn.
- **The contract table (§5) is the drift tripwire:** its permutation matrix (`api_error_status` present/absent × `via provider` present/absent × prefix variant) is the *executable specification* of the contract. When drift #2 arrives, the operator adds one verbatim fixture row; if the classifier already handles it, the row is green and the contract self-documents its own robustness; if red, the failure is a unit-test failure at PR time, not a `FAIL_TERMINAL` cascade in production. This converts "silent detector rot" (the original failure mode) into "loud test failure" — the single most valuable architectural move available here.
- **Explicit follow-up ledger (§4.3):** the sibling detectors that share the coupling are named as debt, so the drift-resistance reasoning is not lost when this PR merges.

---

## 4. Back-Compat Guarantees

### 4.1 Behavioral back-compat (Shape 1, the 6 fixtures)

**Guarantee: zero delta.** Because `api_error_status==429` remains the first disjunct (R2), any transcript that satisfied the old conjunct satisfies the new disjunct identically, and reaches the identical body-discrimination block. The relaxed `_RE_ALL_ACCOUNT` (R3) is a strict superset of the old pattern — every string the old regex matched, the new one matches with the same `model` capture (the dropped ` via provider` was a trailing anchor, not part of the capture group). Formally: old-match ⊆ new-match, and on the intersection the `model` group is byte-identical. Therefore SC3 holds by construction, not by luck.

### 4.2 Structural back-compat (serialization + taxonomy)

`ProviderFailureSignal(kind, resolved_model)`, the 4-member `ProviderFailure` enum, `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (`models.py:53`, in the `is_failure` set `:66`), and `TaskResult` field defaults are untouched (R7). No new enum member, no field, no flag (C4/C7). Any persisted `.roadmap-state`/sprint artifact deserializes unchanged.

### 4.3 Explicit non-changes (the debt ledger)

Per C3, these SHARE the structured-field coupling but have NO drift evidence and are **deliberately not touched**, recorded here so the reasoning survives:

- `detect_error_max_turns` (`monitor.py:47`) — keys on `"subtype":"error_max_turns"`; no 429 coupling, no evidence.
- `detect_prompt_too_long` (`monitor.py:74`) — keys on `"Prompt is too long"`; no evidence.
- Operation-timeout branch (`monitor.py:335-338`) — `body == "API Error: The operation timed out."` exact-equality is a sibling brittleness (OQ5). **Follow-up, not this PR** — touching it now would violate C3 and inflate blast radius with no incident backing it.

---

## 5. Test / Fixture Plan — The Shape-Variant Contract Table

The test plan is the deliverable's spine, because the failure mode was *untested drift*, not *wrong code*.

### 5.1 Verbatim regression fixture (SC1/SC2)

Add `tests/sprint/fixtures/exhaustion/shape2-all-account-gpt55-output.txt` — the verbatim July incident transcript (all-account, `gpt-5.5`, `api_error_status` absent, no `via provider`, `rate_limit_error` inside the nested escaped bytestring-repr). Two assertions bind both consumers:
- **SC1:** `detect_provider_failure(fixture)` → `ALL_ACCOUNT_COOLDOWN`, `resolved_model == "gpt-5.5"`.
- **SC2:** `_classify_transcript(fixture_text)` → `FAIL_PROVIDER_EXHAUSTED`.

### 5.2 The detection-contract table test (SC4 — the drift tripwire)

A single parametrized test enumerating the permutation matrix. Each row is a minimal synthetic terminal `{"type":"result"}` event; the assertion binds BOTH the resulting kind AND (where applicable) `resolved_model` (OQ4 — per-row model assertion guards the R6 model-capture regression that feeds the resume hint).

| # | is_error | api_error_status | all-account body | via provider | prefix | Expected kind | Expected model |
|---|---|---|---|---|---|---|---|
| 1 | true | 429 | yes | yes | Request rejected | ALL_ACCOUNT_COOLDOWN | claude-opus-4-8 | (Shape 1, fast-path) |
| 2 | true | absent | yes | no | API Error: 429 | ALL_ACCOUNT_COOLDOWN | gpt-5.5 | (Shape 2, text-path) |
| 3 | true | 429 | yes | no | Request rejected | ALL_ACCOUNT_COOLDOWN | (any model) | (cross: struct field + relaxed regex) |
| 4 | true | absent | yes | yes | API Error: 429 | ALL_ACCOUNT_COOLDOWN | (any model) | (cross: text-path + old suffix) |
| 5 | true | 429 | no (single-account body) | — | Request rejected | SINGLE_ACCOUNT_LIMIT | None |
| 6 | true | absent | no (single-account body) | — | API Error: 429 | SINGLE_ACCOUNT_LIMIT | None | (OQ2 — text-path single-account) |
| 7 | true | 429 | neither body | — | Request rejected | SINGLE_ACCOUNT_LIMIT | None | (conservative default, unchanged) |
| 8 | true | absent | neither body but rate_limit_error present | — | API Error: 429 | SINGLE_ACCOUNT_LIMIT | None | (text-gate opens, default fires) |
| 9 | **false** | absent | body literally contains `rate_limit_error` + `429` | — | task output | **NONE** | — | (SC5 false-positive guard) |
| 10 | true | absent | body has no rate token at all | — | generic error | **NONE** | — | (non-429 error stays NONE) |
| 11 | (no terminal result event) | — | — | — | truncated | **NONE** | — | (SC6 torn transcript, R5) |

Rows 1 + 5 + 7 pin the fast-path invariant (SC3). Row 9 is the false-positive keystone (C5/SC5): it proves the `is_error` guard, not the body token, is load-bearing for containment. Rows 3/4 are the *cross-product* rows that a naive "just OR the two conditions" patch might not have reasoned about — they belong in the contract precisely because they document that the two sufficient conditions compose cleanly.

### 5.3 Existing-suite preservation (SC3)

`test_monitor.py` and `test_recovery_policy.py` run unchanged and green. `SessionResetPolicy.decide` is not exercised by new tests beyond confirming the existing `ALL_ACCOUNT_COOLDOWN → HALT_MODEL_SWITCH` assertion still holds when driven by a Shape-2-derived signal (one added assertion, no policy change).

### 5.4 Gate hygiene (SC6)

`make lint` + `uv run ruff format --check src/ tests/` + `make verify-sync` clean. No `.claude/` staging. Fixture is data, not code — no format concern.

---

## 6. Anti-Over-Engineering AND Anti-Under-Engineering

Tied explicitly to the SMALL sizing verdict (§1).

**Against OVER-engineering (the sizing floor):**
- **No matcher registry / pluggable-pattern subsystem.** Two shapes and one incident do not justify a pattern-plugin architecture. A registry would add a config surface (violates C7), a lookup indirection, and a second place for the contract to drift — net-negative reliability for a problem a disjunction solves. YAGNI: build the second abstraction when the third shape genuinely needs a *different kind* of match, not a different literal.
- **No nested-JSON unescaping (OQ1).** The `rate_limit_error` token and the `are cooling down` phrase survive verbatim through the `b'{…}'` bytestring-repr nesting — a raw substring/regex over the once-`json.loads`-decoded `result` string matches both. Adding a recursive unescape-and-reparse layer buys nothing measurable and adds a failure mode (double-decode on malformed nesting → exception → potential mis-degrade). Raw substring is *both* sufficient AND safer. Confirmed over-engineering — reject.
- **No config flags, no new enum kinds, no telemetry counters.** C7 forbids surface growth; none is warranted.

**Against UNDER-engineering (the sizing ceiling):**
- **A one-line predicate patch is insufficient.** Flipping `and` to a disjunct without the contract table (§5) would fix Shape 2 and re-arm the exact silent-drift failure for Shape 3. The incident's root cause was *absence of a shape-variant test*, so the fix MUST ship the tripwire, not just the patch.
- **Relaxing the regex without the per-row model assertion is insufficient.** A regex that matches but captures `None` silently breaks the resume hint (`suggest_alternate_model`) — a *second* silent failure downstream. R6 + the per-row `resolved_model` assertion (OQ4) is non-negotiable.
- **Fixing the gate without binding BOTH consumers in test is insufficient.** The live/offline single-source-of-truth is an invariant that a future refactor can break; the contract test must assert both paths agree (§3.2) or the SoT guarantee is aspirational, not enforced.

The SMALL verdict is precisely the band where a disjunction + relaxed literal + an 11-row contract table sits: large enough to be drift-resistant, small enough to touch one function.

---

## 7. Answers to Open Questions

- **OQ1 (body-match locus & escaping):** Raw substring/regex on the once-decoded `result` string is sufficient AND safest. The durable tokens survive the nested bytestring-repr verbatim (verified in the July raw body). Nested unescaping is over-engineering (§6) and introduces a double-decode failure mode. **Do not unescape.**
- **OQ2 (single-account Shape 2 uncaptured):** Keep the `429-with-neither-body → SINGLE_ACCOUNT_LIMIT` conservative default unchanged. A single-account limit rotating a session (RETRY_NEW_SESSION) is the *safe* wrong-guess (retry, recoverable); an all-account cooldown mis-classified as single-account would burn attempts — but the all-account regex now fires on the durable `are cooling down` stem across both shapes, so the dangerous mis-classification is closed. Contract row 6 asserts the *text-path* single-account body (`would exceed your account's rate limit`, assumed shared with Shape 1 per OQ2) still maps correctly. If a Shape-2 single-account body is later captured verbatim, add it as a row — the contract absorbs it without code change.
- **OQ3 (fast-path cascade):** Out of scope here — it is a policy/executor concern. Detection alone correctly classifies each of the 5 cascading tasks; whether the phase short-circuits after the first `ALL_ACCOUNT_COOLDOWN` is `SessionResetPolicy`/executor behavior (`executor.py:1085`/`:2283`), which is correct today and untouched (C3). Note it as a downstream observation, do not act.
- **OQ4 (contract-test shape):** Matrix dimensions = `is_error` × `api_error_status`(present/absent) × body-family(all-account / single-account / neither / non-429 / false-positive / torn) × `via provider`(present/absent, all-account rows only). Per-row `resolved_model` assertion is MANDATORY on all-account rows (guards R6). 11 rows as tabulated in §5.2.
- **OQ5 (operation-timeout exact-match brittleness):** Explicitly OUT of scope per C3 — recorded in the §4.3 debt ledger as a sibling follow-up. It has no drift evidence and no incident; touching it now inflates blast radius against the SMALL sizing. Named, not fixed.

---

## 8. Acceptance Criteria

- **AC1 (SC1):** `detect_provider_failure` on the verbatim Shape-2 fixture → `ALL_ACCOUNT_COOLDOWN`, `resolved_model == "gpt-5.5"`.
- **AC2 (SC2):** `_classify_transcript` on the same fixture → `FAIL_PROVIDER_EXHAUSTED`.
- **AC3 (SC3, back-compat):** all 6 Shape-1 exhaustion fixtures + `test_monitor.py` + `test_recovery_policy.py` pass unchanged; fast-path output byte-identical.
- **AC4 (SC4):** the 11-row detection-contract table test passes, asserting kind AND `resolved_model` per applicable row, and asserting both consumers (`detect_provider_failure`, `_classify_transcript`) agree on the shared fixture.
- **AC5 (SC5):** row 9 — `is_error:false` body containing literal `rate_limit_error`/`429` → `NONE`.
- **AC6 (SC6/scope):** diff touches ONLY `monitor.py` (`_provider_failure_from_text` gate + `_RE_ALL_ACCOUNT` literal), plus `tests/sprint/` fixtures/tests. `make lint` + `ruff format --check` + `make verify-sync` clean. No `.claude/` staging, no downstream file changed.
- **AC7 (contract integrity):** `_provider_failure_from_text` remains the SOLE classifier inner for both consumers — no forked predicate in `rerun_tasks.py`.

---

*Grounded against source 2026-07-02: `monitor.py:41-43` (`_RE_ALL_ACCOUNT` with `via provider`), `monitor.py:323` (conjunctive gate), `monitor.py:324-333` (body discrimination + neither-body default), `monitor.py:335-338` (operation-timeout exact-match), `rerun_tasks.py:592-596` (offline delegation + account-exhaustion gate). Two shapes per `.dev/troubleshoot/429-signature-ground-truth.md` + July raw logs.*
