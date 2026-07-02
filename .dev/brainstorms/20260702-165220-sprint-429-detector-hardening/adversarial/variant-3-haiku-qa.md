# Variant 3 (QA / Test-Engineer lens) — sprint 429 detector hardening

**Scope:** REQUIREMENTS / DESIGN SPEC for the **verification surface** of the 429
detector hardening. Not an implementation. Every claim is grounded in source read
this session (2026-07-02): `src/superclaude/cli/sprint/monitor.py:291-345`,
`rerun_tasks.py:552-618`, the 6 fixtures under `tests/sprint/fixtures/exhaustion/`,
`tests/sprint/test_monitor.py`, `tests/sprint/test_recovery_policy.py`, and the
verbatim Shape-2 transcript in the task brief.

**Thesis:** the bug is *a fixture-fabricated contract*. The detector's tests
assert the assumed contract over fixtures that **encode the assumption**, so they
pass while reality drifts. The fix's verification must therefore be **contract-
table-driven**, not anecdotal-fixture-driven: a parametrized matrix that
enumerates the dimensions on which the proxy transcript can vary, with one row per
real/canonical shape, one FP row, and one row per distinct non-target class. The
matrix is the regression boundary — any future proxy-shape drift must change
exactly one matrix row, not silently slip past a hand-picked fixture.

---

## 1. SIZING VERDICT (test-risk view)

**Verdict: SMALL in lines-of-test, MEDIUM in contract surface. Do NOT size by
the production diff (it is ~6 lines of predicate + one regex). Size by the
detector's *false-confidence surface*: the gap between "tests green" and
"recovery fires in production" is exactly the surface we must close.**

Risk drivers, ranked:

1. **R1 — Fixture-fabrication recurrence (load-bearing).** The 6 existing fixtures
   all share Shape 1 (`api_error_status:429` present, `via provider` present). They
   were authored by the same hand that authored the predicate, so they encode the
   predicate's assumptions. **A test suite where the fixtures are the only negative
   authority cannot detect a contract drift in the fixture itself.** This is the
   bug class that just recurred. Mitigation: the contract-table test (§3) is
   generated from a dimension list, not hand-picked; and at least one fixture (the
   Shape-2 all-account) is a **verbatim paste from a production incident log**,
   never synthesized.
2. **R2 — Live/offline divergence.** Two call sites share `_provider_failure_from_text`:
   live `detect_provider_failure` (`monitor.py:348`) and offline
   `_classify_transcript` (`rerun_tasks.py:552`, calls the inner at `:592`).
   Hardening fixes both only because the inner is shared. **But the test suite
   currently asserts `detect_provider_failure` only — it does not assert that
   `_classify_transcript` maps the same transcript to `FAIL_PROVIDER_EXHAUSTED`.**
   Mitigation: §4 mandates a parity assertion over the same fixture set.
3. **R3 — Model-capture regression (silent).** `resolved_model` feeds
   `resume_command` → `suggest_alternate_model`. If the new regex captures the
   wrong substring (e.g. `gpt-5.5 are cooling down` instead of `gpt-5.5`) the
   classifier still returns `ALL_ACCOUNT_COOLDOWN`, so a `kind`-only assertion
   passes and the resume hint is silently broken. Mitigation: §3 row table asserts
   `resolved_model` per row.
4. **R4 — FP over-trigger (low-probability, high-blast-radius).** Loosening the
   gate to `'rate_limit_error' in body` opens a new FP surface: a *successful* task
   whose output literally discusses rate limits. Mitigation: §3 FP row + the
   `is_error:true` conjunct (C1) keeps the gate closed on benign output.
5. **R5 — Timeout exact-match brittleness (C3 follow-up, NOT in scope).** Documented
   out of scope per OQ5; the contract table covers it as a regression row only.

**Conclusion:** this is correctly a **C-class (medium) verification effort**: ~4 new
fixtures, one parametrized contract-table class, two parity tests, and an FP guard.
It is **deliberately not** a property/fuzz suite (§8) and **deliberately more than**
"add one Shape-2 fixture" (§9).

---

## 2. NEW FIXTURES TO AUTHOR

All under `tests/sprint/fixtures/exhaustion/`. Naming follows the existing
`<shape>_<variant>.jsonl` convention. **Verbatim fixtures must be a byte-for-byte
copy of the production line** (then legal-escape if needed for JSON embedding —
see OQ1), not a re-typing.

### 2.1 `all_account_cooldown_shape2.jsonl` — **the incident reproducer** (SC1/SC4)

- **Shape:** Shape 2 ("API Error: 429", July incident).
- **Class:** `ALL_ACCOUNT_COOLDOWN`, `resolved_model == "gpt-5.5"`.
- **Source:** the verbatim Shape-2 result line from the task brief. **Do not
  paraphrase.** This fixture is the regression boundary for the incident.
- **Required content (three lines, mirroring real transcript structure):**
  1. A leading `system/init`-style line (harmless preamble; proves the detector
     keys on the LAST `{"type":"result"}` line, not the first).
  2. A synthetic `assistant` line carrying the same rate-limit text (proves the
     detector does NOT fire on a non-result event — guards C5).
  3. The verbatim result line:
     `{"type":"result","subtype":"success","is_error":true,"duration_ms":181906,"num_turns":1,"result":"API Error: 429 {\"error\":{\"message\":\"b'{\\\"type\\\":\\\"error\\\",\\\"error\\\":{\\\"type\\\":\\\"rate_limit_error\\\",\\\"message\\\":\\\"All credentials for model gpt-5.5 are cooling down\\\"}}'\",\"type\":\"None\",\"param\":\"None\",\"code\":\"429\"}}","session_id":"0a06b2fc-...","total_cost_usd":0}`
- **Asserts:** `detect_provider_failure(path).kind is ALL_ACCOUNT_COOLDOWN` AND
  `.resolved_model == "gpt-5.5"`.

### 2.2 `single_account_429_shape2.jsonl` — **the assumption fixture** (OQ2)

- **Shape:** Shape 2 surface (`api_error_status` ABSENT) + **single-account** body.
- **Class:** `SINGLE_ACCOUNT_LIMIT`, `resolved_model is None`.
- **Source:** SYNTHESIZED — we have no verbatim Shape-2 single-account transcript.
  This is the explicit-handling-of-uncertainty fixture: it encodes the design's
  **stated assumption** (mirrors Shape 1's `would exceed your account's rate limit`
  phrasing) so that if a future real Shape-2 single-account transcript contradicts
  the assumption, **this fixture fails loudly** rather than the assumption drifting
  silently. The fixture's docstring/comment must mark it `# SYNTHESIZED — OQ2
  assumption; replace with verbatim on first capture`.
- **Asserts:** kind is `SINGLE_ACCOUNT_LIMIT` (verifying the conservative default
  holds under the new gate) AND the FP/trap properties below.

### 2.3 `fp_benign_ratelimit_text.jsonl` — **the false-positive guard** (SC5)

- **Shape:** a genuinely **successful** task whose `result` body literally contains
  the strings `"429"` and `"rate limit"`.
- **Class:** `NONE`.
- **Required content:** `{"type":"result","subtype":"success","is_error":false,
  "result":"Wrote tests for issue #429 (rate limit handling). All acceptance criteria met."}`.
  The `is_error:false` is the load-bearing field; the body carries both trigger
  tokens to prove the body-match alone does NOT fire (C1 conjunct).
- **Asserts:** `detect_provider_failure(path).kind is NONE`. Also asserts that a
  transcript-wide scan (C5 violation) WOULD have mis-fired — see §3 FP row note.

### 2.4 `single_account_429_no_via_provider.jsonl` — **the matrix-completeness fixture** (SC4)

- **Shape:** Shape 1 surface (`api_error_status:429` PRESENT) + single-account body
  **but without** the Shape-1 `via provider`-style suffix. This already exists in
  spirit (`single_account_429.jsonl`) but the matrix (§3) needs the row explicit.
  **Decision:** do NOT add a duplicate fixture if `single_account_429.jsonl` already
  covers the row — instead, the contract-table test references the existing fixture
  for that row (§3 row S1). Author a NEW fixture ONLY for rows not already covered.
  This avoids fixture sprawl and respects the "verbatim first, synthesize last" rule.

> **Net new fixtures: 3** (§2.1, §2.2, §2.3). §2.4 reuses the existing
> `single_account_429.jsonl`. This is the minimum set that makes the matrix (§3)
> exhaustive without redundancy.

---

## 3. THE DETECTION-CONTRACT TABLE TEST (centerpiece)

**Design.** One parametrized test method, `test_detection_contract_table`, in a new
class `TestProviderFailureContractTable` in `tests/sprint/test_monitor.py`. Each
parametrize row is a tuple `(row_id, transcript_text_or_fixture, expected_kind,
expected_model, rationale)`. The method calls `_provider_failure_from_text(text)`
directly (not the path wrapper) so the matrix runs in-memory and fast, then a
second pass calls `detect_provider_failure(path)` for fixture-backed rows to prove
the wrapper agrees (already asserted in `test_text_core_matches_path_wrapper`, but
the contract table restates it per fixture-backed row for locality).

**Why a parametrized table, not separate `def test_*` methods?** Because the bug
was *dimensional*: the proxy can vary along `api_error_status present/absent`,
`via provider present/absent`, and `prefix variant`, and the original suite varied
only the first. A table forces every cell of the cross-product to be acknowledged;
an empty cell must be explicitly `xfail` or skipped with a reason, never silently
absent. This is the structural fix for the fixture-fabrication class.

### 3.1 The matrix rows

Legend — `aes` = `api_error_status`; `vp` = `via provider` token; `kind` is the
expected `ProviderFailure`; `model` is the expected `resolved_model`.

| Row ID | aes     | vp    | prefix / body                                              | expected kind              | expected model      | source / rationale |
|--------|---------|-------|------------------------------------------------------------|----------------------------|---------------------|--------------------|
| **A1** | `429`   | yes   | Shape-1 all-account (`claude-opus-4-8`)                    | `ALL_ACCOUNT_COOLDOWN`     | `claude-opus-4-8`   | existing fixture `all_account_cooldown.jsonl` — **regression anchor (C2 fast-path)** |
| **A2** | absent  | no    | Shape-2 all-account (`gpt-5.5`)                            | `ALL_ACCOUNT_COOLDOWN`     | `gpt-5.5`           | NEW fixture §2.1 — **the incident** |
| **S1** | `429`   | n/a   | Shape-1 single-account (`would exceed your account's…`)    | `SINGLE_ACCOUNT_LIMIT`     | `None`              | existing fixture `single_account_429.jsonl` — regression anchor |
| **S2** | absent  | n/a   | Shape-2 single-account (SYNTHESIZED, OQ2 assumption)       | `SINGLE_ACCOUNT_LIMIT`     | `None`              | NEW fixture §2.2 — assumption guard |
| **S3** | `429`   | no    | 429 with **neither** recognizable body (bare prefix)      | `SINGLE_ACCOUNT_LIMIT`     | `None`              | conservative default — already tested at `test_monitor.py:322-332`; restated in-table for dimensional completeness |
| **T1** | `null`  | n/a   | `API Error: The operation timed out.` exact body          | `OPERATION_TIMEOUT`        | `None`              | existing fixture `operation_timeout.jsonl` — distinct-class regression row (OQ5) |
| **N1** | `null`  | n/a   | clean pass (`is_error:false`, no trigger tokens)          | `NONE`                     | `None`              | existing fixture `clean_pass.jsonl` |
| **N2** | absent  | n/a   | real task failure (`is_error:true`, no 429 tokens)        | `NONE`                     | `None`              | existing fixture `task_failure_real.jsonl` — proves non-429 failures fall through to `NONE` (downstream `FAIL_TERMINAL` is the classifier's job, not the detector's) |
| **F1** | absent  | n/a   | **FP**: `is_error:false`, body contains `"429"` + `"rate limit"` | `NONE`                | `None`              | NEW fixture §2.3 — **FP guard (C1 + C5)** |
| **F2** | absent  | n/a   | result event ABSENT (only `assistant` lines)              | `NONE`                     | `None`              | synthesized; proves the detector does NOT fire on a non-`result` event carrying the rate-limit text (C5 — terminal-event scoping) |
| **X1** | `429`   | yes   | Shape-1 all-account with **prefix variant** `API Error: 429` (not `Request rejected`) | `ALL_ACCOUNT_COOLDOWN` | `claude-opus-4-8` | synthesized; proves the prefix is NOT load-bearing — only `is_error` + body tokens are (decouples detector from the SDK's prefix wording) |

**Notes on the matrix:**
- Rows A1, S1, T1, N1, N2 are **fixture-backed** (read the `.jsonl`, pass text to the
  inner). Rows A2, S2, F1 are **fixture-backed via the NEW §2 fixtures**. Rows S3,
  F2, X1 are **inline transcripts** in the parametrize list (they exercise
  dimensional cells that don't warrant a standalone fixture).
- Row S3 duplicates `test_429_with_neither_body_conservative_default` deliberately:
  in a contract table, dimensional cells must be in-table even if also covered
  elsewhere, so the table is a self-contained specification.
- Row X1 is the **anti-brittleness** row: it pins that the prefix wording is not
  load-bearing. If a future implementation starts keying on `Request rejected`, X1
  fails. (This is the structural counterpart to the bug we just fixed.)

### 3.2 Per-row assertions (the "assert-model-per-row" guarantee — OQ4)

Every row asserts **both** `kind` AND `resolved_model`:

```python
sig = _provider_failure_from_text(text)
assert sig.kind is expected_kind, f"{row_id}: kind {sig.kind} != {expected_kind}"
assert sig.resolved_model == expected_model, f"{row_id}: model {sig.resolved_model!r} != {expected_model!r}"
```

**Why assert the model on EVERY row, including `None` rows?** Because
`resolved_model` is the silent-regression vector (R3). A `kind`-only assertion
cannot detect a regex that captures `gpt-5.5 are cooling down` instead of
`gpt-5.5`, or — worse — a regex that *over-captures* on rows that should return
`None` (e.g. a greedy `.+` that leaks into a single-account body). Asserting
`resolved_model == None` on every non-cooldown row pins the negative space.

### 3.3 Dimensional completeness check (the anti-recurrence argument)

The matrix covers the cross-product of the two load-bearing dimensions:

|                  | `vp` present        | `vp` absent            |
|------------------|---------------------|------------------------|
| `aes == 429`     | A1 (all-account)    | X1 (prefix-var) + S1 (single, n/a) + S3 (neither) |
| `aes` absent     | (implausible¹)      | **A2 (incident)** + S2 (single-assumption) |

¹ The `vp`-present/`aes`-absent cell is implausible (`via provider` only appears in
the all-account body, which carries `rate_limit_error` and opens the gate via the
body-token disjunct regardless) — but the table marks it `xfail`/skip-with-reason
rather than omitting it, so a future drift that populates the cell is surfaced.

**This is the structural guarantee that a third proxy-shape drift cannot silently
recur: any new shape maps to exactly one cell, and an empty cell is a visible
`xfail`, not an invisible omission.**

---

## 4. LIVE / OFFLINE PARITY ASSERTIONS (SC2 + the untested seam)

The shared-inner architecture means hardening fixes both paths — **but only if the
test suite actually exercises both**. Today, `test_monitor.py` asserts
`detect_provider_failure`; it does NOT assert that `_classify_transcript` maps the
same transcript to `FAIL_PROVIDER_EXHAUSTED`. That is an untested seam.

**New test class `TestProviderFailureLiveOfflineParity` in `test_monitor.py`** (or a
sibling `test_classify_transcript.py` if imports stay clean — prefer colocation with
`test_monitor.py` to keep the detector's contract in one file):

1. **`test_classify_transcript_maps_all_account_to_provider_exhausted`** — feed the
   §2.1 Shape-2 fixture text to `_classify_transcript` (imported from
   `superclaude.cli.sprint.rerun_tasks`), assert the return is
   `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (SC2). This is the load-bearing live/offline
   parity test: it proves the hardening reaches the offline rerun path.
2. **`test_classify_transcript_pass_recovered_intercept`** — feed a transcript that
   has BOTH a trailing Shape-2 all-account result AND a structured success envelope
   *before* it; assert `PASS_RECOVERED` (the edge-1 intercept at
   `rerun_tasks.py:603-604` must still fire on Shape 2). This guards the
   completed-before-overrun gate against the new gate predicate.
3. **`test_classify_transcript_clean_pass_still_pass`** — regression: the §N1 clean
   transcript maps to `TaskStatus.PASS` (not accidentally to
   `FAIL_PROVIDER_EXHAUSTED` via an over-loose body match).
4. **`test_live_offline_agree_on_full_fixture_set`** — for each of the 6 existing +
   3 new fixtures, assert `(detect_provider_failure(path).kind in {NONE, SINGLE_,
   ALL_, TIMEOUT})` is **consistent** with `_classify_transcript(text) in {PASS,
   PASS_RECOVERED, FAIL_PROVIDER_EXHAUSTED, FAIL_TERMINAL, ...}` per the documented
   mapping. This is the seam-closer: any future divergence between the two paths on
   the same transcript fails this test.

> **Mapping table the parity test encodes** (derived from `rerun_tasks.py:593-605`):
> detector `ALL_ACCOUNT_COOLDOWN` or `SINGLE_ACCOUNT_LIMIT` → classifier
> `FAIL_PROVIDER_EXHAUSTED` (or `PASS_RECOVERED` if completion-evidence fires);
> detector `OPERATION_TIMEOUT` or `NONE` → classifier unchanged (falls through to
> the is_error/transient ladder).

---

## 5. REGRESSION GUARD — the 6 existing fixtures (SC3)

**`test_monitor.py`'s existing `TestDetectProviderFailure` must pass UNCHANGED.**
This is the C2 fast-path preservation guarantee. Concretely:

- `test_single_account_429` → `SINGLE_ACCOUNT_LIMIT` (fixture `single_account_429.jsonl`).
- `test_all_account_cooldown_captures_model` → `ALL_ACCOUNT_COOLDOWN` + model `claude-opus-4-8`.
- `test_operation_timeout` → `OPERATION_TIMEOUT`.
- `test_task_failure_real_is_none` → `NONE`.
- `test_clean_pass_is_none` → `NONE`.
- `test_api_retry_maxed_still_single_account` → `SINGLE_ACCOUNT_LIMIT` (the
  "attempt==max_retries is only corroborating" edge — proves the LAST result event
  wins; the contract table's row-selection logic must preserve this).

Plus the tolerance edges (`test_truncated_ndjson_is_none`,
`test_empty_output_is_none`, `test_missing_file_is_none`), the subtype-trap
(`test_subtype_trap_keys_on_is_error_not_subtype`), the conservative default
(`test_429_with_neither_body_conservative_default`), and the shared-core
equivalence (`test_text_core_matches_path_wrapper`). **None of these test bodies
should change.** The acceptance gate is: `uv run pytest tests/sprint/test_monitor.py
tests/sprint/test_recovery_policy.py` is green before AND after the hardening, with
the SAME set of `PASSED` test names (only ADDITIONS allowed).

**`test_recovery_policy.py`'s 7-row truth table (`decide()`) must also pass
unchanged** — it consumes the `ProviderFailure` enum, which C4 preserves. The
contract table does NOT re-test `decide()`; that is the policy's contract, not the
detector's. Scope discipline (C3) applies to tests too.

---

## 6. ACCEPTANCE CRITERIA mapped to SC1–SC6

| SC | Test artifact (this spec) | Pass condition |
|----|---------------------------|----------------|
| **SC1** Shape-2 → ALL_ACCOUNT_COOLDOWN + `gpt-5.5` | §2.1 fixture + matrix row **A2** | row A2 green |
| **SC2** offline `_classify_transcript` → FAIL_PROVIDER_EXHAUSTED | §4 test #1 | green |
| **SC3** 6 existing fixtures + recovery policy unchanged | §5 regression guard | same PASSED set, only additions |
| **SC4** Shape-2 fixture + contract-table matrix | §2.1 + §3 full table (11 rows) | all rows green (or documented `xfail`) |
| **SC5** FP guard (`is_error:false` + literal `429`/`rate limit` → NONE) | §2.3 fixture + matrix row **F1** | row F1 green |
| **SC6** scope + lint/format/sync clean | §10 final gate | `make lint`, `ruff format --check src/ tests/`, `make verify-sync` clean; diff confined to `monitor.py:41-43,323-333` + `tests/sprint/` + 3 new fixtures |

---

## 7. OPEN QUESTIONS — answers from a testability view

- **OQ1 (nested escaping — raw substring vs nested-JSON unescape).** **Answer: raw
  substring/regex on the once-`json.loads`-decoded `result` string is sufficient and
  correct; nested unescaping is over-engineering.** Testability grounds:
  (a) the verbatim Shape-2 fixture (§2.1), when `json.loads`-parsed at the line
  level, yields a `result` field whose Python-str value **contains** the literal
  substring `rate_limit_error` and `All credentials for model gpt-5.5 are cooling
  down` — both the body-token disjunct (C1) and the new `_RE_ALL_ACCOUNT` (C8) match
  on that decoded value without any second-pass unescape; (b) the matrix row A2
  asserts both `kind` and `model` off that single decode, proving sufficiency; (c)
  adding a second unescape pass would EXPAND the FP surface (a doubly-escaped benign
  payload could become a trigger) and is therefore testability-negative. The
  contract table is the evidence: if raw-substring were insufficient, A2 would fail.

- **OQ2 (single-account Shape-2 unknown).** **Answer: assume it mirrors Shape 1's
  `would exceed your account's rate limit` phrasing; pin that assumption with the
  §2.2 SYNTHESIZED fixture and a leading comment marking it
  `# SYNTHESIZED — replace with verbatim on first capture`.** Testability move: the
  assumption is encoded as an executable test (matrix row S2), so the day a real
  Shape-2 single-account transcript arrives and contradicts it, **S2 fails loudly**
  rather than the assumption drifting silently. This is the disciplined way to test
  an unknown: make the assumption a breakpoint. The conservative
  `SINGLE_ACCOUNT_LIMIT` default for the `429-with-neither-body` cell (row S3) is
  preserved — *do not* loosen it on speculation; if Shape-2 single-account proves to
  need a different body match, that's a follow-up with a verbatim fixture.

- **OQ3 (cascade short-circuit).** **Out of scope for the detector's tests.**
  Whether the executor short-circuits the phase after the first
  `ALL_ACCOUNT_COOLDOWN` is a policy/executor concern; the detector's contract ends
  at returning `ALL_ACCOUNT_COOLDOWN` for each transcript independently. The matrix
  (§3) deliberately tests ONE transcript per row. A separate executor-level test
  (not in this spec) would cover cascade behavior. Mentioning it here prevents scope
  creep into the detector suite.

- **OQ4 (matrix shape + model-per-row).** **Answer: yes, assert `resolved_model`
  per row.** See §3.2. The matrix is 11 rows × 4 fields (id, input, expected kind,
  expected model). Asserting the model on every row — including `None` on the 8
  non-cooldown rows — is the only way to pin the `resolved_model` regression vector
  (R3). A `kind`-only table would leave the resume-hint capture untested.

- **OQ5 (timeout exact-match brittleness).** **Out of scope per C3; covered as a
  regression row only.** Matrix row T1 pins the CURRENT behavior (`body == "API
  Error: The operation timed out."` exact equality → `OPERATION_TIMEOUT`) so a
  future hardening of the timeout branch has a breakpoint. A follow-up task (not
  this spec) should consider `body.startswith("API Error: The operation timed out")`
  or a timeout-specific signal. Documenting it here as a row — not fixing it — is
  the disciplined boundary.

---

## 8. ANTI-OVER-ENGINEERING — why NOT a property/fuzz suite

A full property-based (Hypothesis) or fuzz suite over transcript strings is
**warranted-NO** here:

1. **The input domain is not arbitrary text — it is stream-json from one CLI
   proxy.** A fuzzer would generate millions of malformed JSON strings that the
   detector correctly rejects via the `json.JSONDecodeError` guard at
   `monitor.py:309`; these add zero coverage of the *contract* and slow the suite.
2. **The bug was not a missing edge — it was a missing *dimension*.** Property tests
   are good at finding edges within a dimension; they are poor at *naming* the
   dimensions. The contract table (§3) names the dimensions explicitly, which is
   what makes future drift visible.
3. **The detector is a pure function over a single transcript string — no I/O, no
   state, no concurrency.** The parametrized table covers the equivalence classes
   exhaustively (§3.3). Adding Hypothesis would multiply runtime for no information
   gain.
4. **CI cost / flake discipline.** The project values fast, deterministic unit
   tests (`@pytest.mark.unit`). A fuzz suite introduces nondeterminism and runtime
   pressure that is disproportionate to a ~6-line predicate fix.

The right size is the **contract table + 3 fixtures + parity tests**. Bigger is
theatre; smaller (§9) is the bug recurring.

---

## 9. ANTI-UNDER-ENGINEERING — why a single Shape-2 fixture is insufficient

The temptation, given the production diff is tiny, is to ship "add one Shape-2
fixture, assert `ALL_ACCOUNT_COOLDOWN`." **That is precisely the failure mode that
caused the incident.** Reasons a single fixture is insufficient:

1. **It re-creates the fabrication problem.** A lone Shape-2 fixture asserts ONE
   cell of the matrix. The next drift (a Shape 3) hits an untested cell and silently
   misroutes — exactly the recurrence we are bound to prevent.
2. **It leaves the FP surface unguarded.** Loosening the gate to
   `'rate_limit_error' in body` (C1) is a behavior change with a NEW FP surface.
   Without row F1, we have no evidence the gate stays closed on benign output.
3. **It leaves `resolved_model` untested.** A single `kind`-only assertion cannot
   detect the model-capture regression (R3), which silently breaks the resume hint —
   the user-visible recovery affordance.
4. **It leaves the live/offline seam untested.** A single `detect_provider_failure`
   assertion does not reach `_classify_transcript` (SC2). The offline rerun path —
   the user's `sprint rerun-tasks` recovery verb — would remain unverified.
5. **It leaves the dimensional boundary implicit.** Without the matrix, there is no
   artifact that says "these are the dimensions on which a transcript can vary." The
   next contributor has no map.

The contract table is the **minimum** verification object that (a) reproduces the
incident, (b) guards the new FP surface, (c) pins the model capture, (d) closes the
live/offline seam, and (e) makes the dimensional boundary explicit so a third
proxy-shape drift is a visible row failure, not an invisible omission. Anything
less is a bet that the next drift will look like this one — which is the bet we just
lost.

---

## 10. FINAL VERIFICATION GATE (acceptance, in order)

1. `uv run pytest tests/sprint/test_monitor.py -v` — all 39 existing + new
   contract-table rows + parity tests green.
2. `uv run pytest tests/sprint/test_recovery_policy.py -v` — 7 rows unchanged.
3. `uv run pytest tests/sprint/ -v` — full sprint suite green (no wider regression).
4. `make lint` — `ruff check` clean on touched files.
5. `uv run ruff format --check src/ tests/` — CI format gate (per project memory:
   `make lint` does NOT run the format check).
6. `make verify-sync` — `src/` ↔ `.claude/` sync intact (this fix touches only
   `src/` + `tests/`, but the gate is mandatory before commit).
7. **Scope audit:** `git diff --stat master...HEAD --name-only` shows changes ONLY
   in `src/superclaude/cli/sprint/monitor.py` (the predicate + regex),
   `tests/sprint/test_monitor.py` (+ sibling if added), and the 3 new fixtures. Any
   other path = scope violation (C3/C6).

---

## 11. TRACEABILITY SUMMARY (one line per artifact)

- §2.1 `all_account_cooldown_shape2.jsonl` → SC1, SC4 (matrix row A2).
- §2.2 `single_account_429_shape2.jsonl` → OQ2 assumption guard (matrix row S2).
- §2.3 `fp_benign_ratelimit_text.jsonl` → SC5 (matrix row F1).
- §3 contract table (11 rows) → SC4, R1, R3 (anti-recurrence structural fix).
- §4 parity tests (4) → SC2, R2 (the untested live/offline seam).
- §5 regression guard → SC3 (6 fixtures + recovery policy unchanged).
- §6 acceptance map → SC1–SC6 coverage matrix.
- §7 OQ answers → OQ1 (raw substring suffices), OQ2 (synth + breakpoint), OQ3
  (out of scope), OQ4 (model-per-row yes), OQ5 (regression row only).
- §8/§9 → sizing discipline (not property suite, not single fixture).
- §10 final gate → SC6 (scope + lint/format/sync).

**The contract table is the deliverable. Everything else supports it.**
