# Variant 2 — Refactorer Lens: 429 Detector Hardening (Minimal-Diff Spec)

**Artifact type:** Requirements / design spec (NOT code).
**Lens:** Refactorer — smallest correct diff, ruthless anti-over-engineering, technical-debt awareness, zero-regression back-compat.
**Target:** `_provider_failure_from_text` + `_RE_ALL_ACCOUNT` in `src/superclaude/cli/sprint/monitor.py`.
**Grounded against source, 2026-07-02:** gate at `monitor.py:323`, all-account regex at `monitor.py:41-43`, timeout branch at `monitor.py:335-338`, shared-inner delegation confirmed (`rerun_tasks.py:552→:592`).

---

## 1. SIZING VERDICT — this is a two-line predicate edit + one regex loosening

**Verdict: NARROW.** This is a detection-predicate hardening, not a feature. The true diff surface is *three source hunks in one file*, all inside the detection layer:

| # | Hunk | Location | Change | LOC delta |
|---|---|---|---|---|
| H1 | All-account regex | `monitor.py:41-43` | Drop `via provider` suffix (C8) | ~1 line edited |
| H2 | Entry gate predicate | `monitor.py:323` | `api_error_status == 429` → `(api_error_status == 429 OR 'rate_limit_error' in body)` (C1) | ~2 lines |
| H3 | Timeout-branch guard | `monitor.py:337` | Neutralize the now-invalidated `api_error_status is None` assumption (see §2.4) | ~1 line |

**Source-code diff surface: ≈4 changed lines in ONE file.** Everything else is test/fixture additions. No new function, no new module, no new import, no new type, no new enum kind, no signature change. `body` is already computed at `monitor.py:321` — the new disjunct reuses an existing local. `ProviderFailureSignal`, `ProviderFailure`, and the `resolved_model` capture at `:328` are untouched.

**Why one function fixes both paths:** the offline `_classify_transcript` (`rerun_tasks.py:552`) delegates to the same shared inner (`:592`). Editing `_provider_failure_from_text` once repairs live + offline (SC1 + SC2) with no second edit site. This is the single strongest argument that the change is narrow: there is exactly one behavioral choke point.

**Cost-of-change asymmetry:** the incident (whole phase → `FAIL_TERMINAL`, PR #183's entire recovery subsystem dark) is catastrophic; the fix is ~4 lines. The ROI of *right-sizing* here is not "do less to save effort" — it is "the smallest change that closes both gaps has the smallest regression surface against 6 green fixtures." Every line added beyond these is a line that can regress Shape 1.

---

## 2. THE PRECISE MINIMAL CHANGE (requirements + pseudocode, NOT code)

### 2.1 H1 — Loosen the all-account regex (C8, closes gap 2)

**Requirement R1:** `_RE_ALL_ACCOUNT` MUST match both `...cooling down via provider claude` (Shape 1) and `...cooling down` (Shape 2, no suffix), while still capturing the model non-greedily.

Pseudocode (pattern only):
```
_RE_ALL_ACCOUNT  ==  /All credentials for model (?P<model>.+?) are cooling down/
```
Rationale for the boundary: anchor the capture on the fixed prefix `All credentials for model ` and terminate the non-greedy group at ` are cooling down`. Dropping `via provider` is *strictly widening* — every string Shape 1 matched still matches (the suffix was optional context, not a disambiguator). The `.+?` still stops at the first ` are cooling down`, so `resolved_model` capture is unchanged for Shape 1 (`claude-opus-4-8`) and correct for Shape 2 (`gpt-5.5`). No new group, no new regex object.

### 2.2 H2 — Widen the entry gate to C1 (closes gap 1, load-bearing)

**Requirement R2:** the entry predicate MUST fire when `is_error` is true AND *either* the structured `api_error_status == 429` *or* the literal substring `rate_limit_error` is present in the terminal result body.

Current (`monitor.py:323`):
```
if is_error and api_error_status == 429:
```
Target predicate:
```
rate_limited = (api_error_status == 429) or ("rate_limit_error" in body)
if is_error and rate_limited:
    <existing body-discrimination block, UNCHANGED>
```

**Design decision — INLINE, no helper (anti-over-engineering).** A named `_is_rate_limited(...)` helper would be a one-caller abstraction: pure ceremony for a two-term boolean. The disjunct is self-documenting at the call site and `body` is already in scope. Requirement: express C1 as an inline local boolean; do NOT extract a helper, a predicate registry, or a "signal-source" strategy object.

**C2 fast-path is preserved by construction.** `api_error_status == 429` is the *first* disjunct — it short-circuits before the substring scan. For all 6 Shape-1 fixtures the structured field is present, so evaluation reaches the identical body-discrimination block via the identical branch. Zero behavioral change for Shape 1 (SC3).

**Body-discrimination block is UNCHANGED.** Once the gate opens, the existing `_RE_ALL_ACCOUNT` → `_RE_SINGLE_ACCOUNT` → conservative-default ladder (`:324-333`) runs verbatim. With H1 applied, Shape 2's all-account body now matches at the first rung and returns `ALL_ACCOUNT_COOLDOWN` with `resolved_model="gpt-5.5"` (SC1). Both gaps close through the *same* opened gate — this is why H1 and H2 must ship together (see §7 anti-under-fixing).

### 2.3 FP-guard is inherited, not added (C5, C6)

The `rate_limit_error` scan runs ONLY against `body`, which is `str(result_event.get("result", ""))` from the *last* `{"type":"result"}` event (`:302-321`). The predicate is *already* scoped to the terminal result event body and gated behind `is_error` — the existing parse loop supplies C5 and C6 for free. **Requirement R3:** the new disjunct MUST read only the existing `body` local; it MUST NOT introduce a transcript-wide scan, a second parse, or a pre-`is_error` check. No new code is needed to satisfy C5/C6 — the guard is structural.

### 2.4 H3 — Repair the timeout branch's stale assumption (necessary, not scope creep)

The timeout branch at `monitor.py:335-338` reads:
```
if is_error and api_error_status is None and body == "API Error: The operation timed out.":
```
This is downstream of the 429 gate and is *not* about 429s. But note: the 429 gate at `:323` currently returns before reaching it whenever `api_error_status == 429`. Under C1, a Shape-2 429 has `api_error_status is None` — but it ALSO now matches the widened 429 gate (via `rate_limit_error in body`) and returns at `:333` at the latest, *before* the timeout branch. So the timeout branch is not reached by any 429.

**Therefore H3 is a no-op-for-429 correctness note, not a required edit** — UNLESS the implementer discovers the widened gate could theoretically fall through. It cannot: every `is_error` 429 (both shapes) now returns inside the 429 block. **Requirement R4 (conditional):** the timeout branch MUST remain byte-for-byte unchanged; the spec asserts (and a test SHOULD prove) that no Shape-1/Shape-2 429 transcript ever reaches `:335`. If the implementer is tempted to touch `:337`, that temptation is the over-fix siren — the H3 row in §1 is a *watch item*, not a mandated hunk. **Net mandated source edits: H1 + H2 only (~3 lines).**

---

## 3. CHANGES WE ARE NOT MAKING (the anti-over-engineering artifact)

This is the load-bearing section of this variant. Each rejected addition is a real temptation a well-meaning implementer or reviewer will raise; each is rejected with a reason grounded in the locked constraints and the actual transcript facts.

| Tempting addition | Why it's tempting | Why REJECTED |
|---|---|---|
| **Nested-JSON / bytestring unescaping** of the `b'{...rate_limit_error...}'` envelope | "Parse it properly instead of substring-matching escaped text." | Ground truth (§OQ1) confirms `rate_limit_error` and `All credentials...cooling down` appear **literally** in the once-`json.loads`-decoded `result` string; nested escaping does NOT hide them. A recursive unescaper adds a parse path, new failure modes (malformed nested repr → exception), and buys nothing. Raw substring on the already-decoded body is sufficient AND safest (C6: torn input → NONE, not a crash). **See §4.** |
| **Generic error-taxonomy / pluggable matcher registry** | "Future providers will have new bodies; make it extensible." | C7 forbids new subsystems. There are exactly two known shapes and one detector. A registry is speculative generality (YAGNI) — it trades a 2-term boolean for a framework. Add the next matcher when the next real transcript arrives, not before. |
| **Config knob** (e.g. `--rate-limit-signal-tokens`) | "Let operators tune the token list." | C7 forbids new flags/config. The token `rate_limit_error` is a CLIProxyAPI protocol constant, not an operator preference. A knob invites drift between config and reality and adds a whole config-plumbing surface for a hardcoded protocol string. |
| **Refactor sibling detectors** (`detect_error_max_turns`, `detect_prompt_too_long`) to share the same structured-field decoupling | "They have the same `api_error_status` coupling; fix them all." | C3 scopes strictly to the 429 detector. Those siblings have **no drift evidence** — no incident, no failing transcript. Refactoring them now is a change without a triggering failure: pure risk, zero proven benefit. Document as a **follow-up** (§8). |
| **New `ProviderFailure` enum kind** (e.g. `ALL_ACCOUNT_COOLDOWN_UNSTRUCTURED`) | "Shape 2 is a different signal; give it its own kind." | C4 preserves the taxonomy exactly. Shape 2 is the *same* provider condition (all accounts cooling down) reached by a *different transcript encoding*. The consumer (`SessionResetPolicy.decide`) acts on the condition, not the encoding. A new kind would force a consumer change — scope explosion, and a back-compat break in serialization. |
| **Change `ProviderFailureSignal` shape** to carry the match source / raw body | "Useful for debugging which disjunct fired." | C4 preserves serialization/field defaults. The `resolved_model` field already carries the one downstream-relevant datum. Debug provenance belongs in a log line, not the serialized signal. |
| **Fix the timeout branch's `==` exact-match brittleness** (OQ5, `:338`) | "It's brittle; while we're here..." | Out of scope per C3. It is a *sibling* detector concern with no 429 relevance and no incident. Note as follow-up (§8). "While we're here" is the canonical scope-creep vector. |
| **Broaden the single-account default** or add a Shape-2 single-account matcher (OQ2) | "Symmetry — handle Shape-2 single-account too." | We have **no verbatim Shape-2 single-account transcript** (OQ2). Speculating its body would be inventing a fixture from imagination — a violation of evidence-based development. Keep the conservative `429-with-neither-body → SINGLE_ACCOUNT_LIMIT` default (`:332-333`) exactly; it already degrades safely (rotate, don't halt) for any un-modeled 429 body. **See §6 OQ2.** |
| **Add phase-cascade short-circuit** in the executor (OQ3) | "5 tasks each re-hit the 429; stop after the first." | Out of the detection layer. Detection alone reclassifies every task correctly; whether the phase halts on the first `ALL_ACCOUNT_COOLDOWN` is a policy/executor concern (`recovery_policy.py`/`executor.py`), and per the seed brief the downstream is already correct. Not this spec's surface. |

**Rule of thumb enforced by this section:** every proposed line must map to closing gap 1 or gap 2 against a *verbatim-verified* transcript. If a change is justified only by a hypothetical future transcript, it is rejected here.

---

## 4. FP-GUARD REASONING — why `rate_limit_error` beats a bare `429` scan

**Requirement R5:** the text disjunct MUST use the token `rate_limit_error`, NOT a bare `429` / `"rate limit"` scan.

1. **Specificity.** `429` appears in benign successful task output constantly (HTTP examples, test fixtures, docs a task might generate, this very spec). A bare `429 in body` disjunct would fire on any task that *mentions* 429 — a false-positive engine. `rate_limit_error` is the CLIProxyAPI error-type constant; it does not occur in ordinary successful output.
2. **Both real shapes carry it.** Verified: `rate_limit_error` appears literally in Shape 1's `b'{..."type":"rate_limit_error"...}'` and in Shape 2's nested envelope. It is the single token common to both shapes and absent from success bodies — the lowest-false-positive basis available.
3. **Double-gated.** The disjunct is only evaluated when `is_error` is already true (`:319`, `:323`). A successful task (`is_error:false`) whose output literally contains `rate_limit_error` or `429` classifies as NONE — never reaches the disjunct. This directly satisfies SC5. (A phrase like "rate limit" in prose is also NOT `rate_limit_error`, so even an errored task discussing rate limits in prose won't trip it.)
4. **No regex needed for the token.** A plain `"rate_limit_error" in body` substring test is faster and less error-prone than a regex, and immune to escaping (§OQ1). Requirement: use `in`, not `re.search`, for the token check.

**Contrast with under-specified alternatives:** a `"429" in body` scan fails specificity (2); an `api_error_status`-only fix (status quo) fails Shape 2 entirely (gap 1 stays open); a full JSON-path extract of `error.type == "rate_limit_error"` fails simplicity and adds a parse failure mode for zero specificity gain over the substring.

---

## 5. BACK-COMPAT PROOF (C2, C4, SC3)

**Claim:** all 6 existing Shape-1 fixtures and `test_monitor.py` / `test_recovery_policy.py` assertions pass unchanged.

- **H2 short-circuit:** for every Shape-1 fixture, `api_error_status == 429` is true, so the first disjunct is true and the second is never evaluated. The branch taken is identical to the pre-change branch; the body-discrimination ladder runs identically. ⇒ identical return values for all 6.
- **H1 widening is a superset:** the new regex matches a strict superset of the old (removing a required suffix cannot un-match a previously-matching string). Shape-1 all-account bodies (`...cooling down via provider claude`) still match; `.+?` still terminates the model capture at ` are cooling down`, preserving `claude-opus-4-8`. ⇒ identical `resolved_model` for Shape 1.
- **Taxonomy/serialization (C4):** no enum member added/removed/reordered; `ProviderFailureSignal(kind, resolved_model)` shape unchanged; `TaskResult` field defaults untouched. ⇒ serialization byte-compatible.
- **Timeout branch (H3):** unchanged; proven unreachable by any 429 (§2.4). ⇒ no timeout-classification change.

**Regression surface = 0 for Shape 1.** This is the whole point of keeping the structured field as the leading fast-path (C2) rather than replacing it.

---

## 6. ANSWERS TO OPEN QUESTIONS

- **OQ1 (raw substring sufficient?):** **YES — raw substring on the once-decoded `result` string is sufficient and safest; nested unescaping is over-engineering.** Ground truth confirms both marker strings survive literally into the decoded body. Recursive unescaping adds a parse path and a crash mode (malformed nested repr) that C6 explicitly wants to avoid (torn → NONE, never raise). Use `"rate_limit_error" in body`.
- **OQ2 (Shape-2 single-account):** **Do NOT model it.** No verbatim transcript exists; inventing its body violates evidence-based development. Keep the conservative `429-with-neither-body → SINGLE_ACCOUNT_LIMIT` default exactly — it already degrades safely (rotate, not halt) for any un-modeled 429 body, including a future Shape-2 single-account. Add a real matcher only when a real transcript lands (follow-up §8).
- **OQ3 (phase-cascade short-circuit):** **Out of scope.** Detection correctly reclassifies each task; the halt-on-first behavior is a policy/executor concern and the seed brief states downstream is already correct. Not a detection-layer change.
- **OQ4 (contract-test shape):** matrix = `api_error_status ∈ {429, absent} × via-provider-suffix ∈ {present, absent} × prefix ∈ {"Request rejected (429)", "429 {…}"}`. **Assert `resolved_model` per all-account row** — this guards the model-capture regression that feeds `suggest_alternate_model` (the resume hint). At minimum assert the four "must-fire" cells (the two real shapes + the two cross-permutations) return `ALL_ACCOUNT_COOLDOWN` with the expected model, and one "must-not-fire" cell (`is_error:false`) returns NONE. See §7.
- **OQ5 (timeout `==` brittleness):** **Out of scope per C3** — sibling brittleness, no 429 relevance, no incident. Document as follow-up (§8).

---

## 7. TEST / FIXTURE PLAN (minimal, matched to the diff)

**Anti-over-testing principle:** one new verbatim fixture + one parametrized contract table + one FP guard test. Do NOT add a fixture per permutation (the table synthesizes permutations from the two real anchors); do NOT re-test unchanged downstream policy (already covered).

1. **F1 — Verbatim Shape-2 fixture** under `tests/sprint/fixtures/exhaustion/` (all-account, `gpt-5.5`, no `via provider`, `api_error_status` absent), copied verbatim from the July incident raw log. Proves SC1 + SC2 against real bytes, not a synthesized string.
2. **F2 — Detection-contract table test** (parametrized) asserting `_provider_failure_from_text` fires across the OQ4 matrix, asserting BOTH `kind == ALL_ACCOUNT_COOLDOWN` AND `resolved_model == expected` per all-account row. Include exactly one `is_error:false` row asserting `NONE` (SC5).
3. **F3 — Offline-path assertion:** `_classify_transcript` on F1 → `FAIL_PROVIDER_EXHAUSTED`, not `FAIL_TERMINAL` (SC2). One test; shared inner means this is a thin wrapper check.
4. **F4 — Regression guard (SC3):** the existing 6 Shape-1 fixtures + `test_monitor.py`/`test_recovery_policy.py` run unchanged and green. No edits to existing tests.
5. **F5 — Unreachability assertion (§2.4):** one test that a Shape-2 429 transcript does NOT return `OPERATION_TIMEOUT` (guards the timeout branch's continued no-touch).

Gates: `make lint` + `uv run ruff format --check src/ tests/` + `make verify-sync` clean (SC6).

### Anti-UNDER-fixing (explicit)

- **A lone regex tweak (H1 only)** leaves gap 1 OPEN: Shape 2 has `api_error_status` absent, so even a `via provider`-free regex never runs — the gate at `:323` still fails the conjunct and returns NONE. H1 without H2 = incident recurs. **Both hunks are mandatory.**
- **A single-shape fixture** (only F1, no contract table) fails to prove the cross-permutations (e.g. `api_error_status:429` + no-`via-provider`, which the widened regex must also handle). The table (F2) is required to prove the *predicate matrix*, not just one incident replay.

---

## 8. FOLLOW-UPS (documented, deliberately deferred — C3, C7)

1. Sibling detectors `detect_error_max_turns` / `detect_prompt_too_long` share the structured-field coupling but have **no drift evidence** — revisit only if a real transcript fails them.
2. Timeout branch `==` exact-match brittleness (OQ5, `:338`) — loosen to substring only when a real timeout-body variant appears.
3. Shape-2 single-account body (OQ2) — add a matcher when a verbatim single-account Shape-2 transcript is captured.

These are recorded so the deferral is a *decision*, not an omission — and so a future reader sees they were considered and consciously rejected for now.

---

## 9. ACCEPTANCE CRITERIA

- **AC1:** `detect_provider_failure` returns `ALL_ACCOUNT_COOLDOWN`, `resolved_model="gpt-5.5"` on the verbatim Shape-2 fixture (SC1).
- **AC2:** `_classify_transcript` maps the Shape-2 fixture to `FAIL_PROVIDER_EXHAUSTED` (SC2).
- **AC3:** all 6 Shape-1 fixtures + existing monitor/recovery tests pass unchanged (SC3, C2).
- **AC4:** contract table (F2) green across the OQ4 matrix, with per-row `resolved_model` assertions (SC4, OQ4).
- **AC5:** an `is_error:false` body containing literal `429`/`rate_limit_error` → NONE (SC5).
- **AC6:** source diff touches ONLY `monitor.py` lines 41-43 (regex) and ~323 (predicate); no enum, signature, config, flag, or sibling-detector change (SC6, C3/C4/C7).
- **AC7:** `make lint` + `ruff format --check` + `make verify-sync` clean (SC6).
- **AC8:** timeout branch (`:335-338`) byte-unchanged and proven unreachable by any 429 (F5).

**Definition of done:** ~3 mandated source lines changed in one file; 4-5 focused tests added; zero downstream edits; both verified gaps closed; six green fixtures still green.
