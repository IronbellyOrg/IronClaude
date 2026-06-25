# Phase 3 Fix-Verification — Content/Semantics (proxy-honesty + idiom)

**VERDICT: PASS**

Report-only re-verification (fix_authorization: false; no files modified). The two FAIL
lenses — "run_report idiom conformance" and "proxy honesty" — and their associated findings
(P3-2, P3-4, P3-5) are genuinely fixed: the wire text now matches the code's actual
guarantees, no oversell remains, and no new vacuity was introduced. All 24 backtest tests pass.

## Evidence per verification checkpoint

### 1. P3-2 — wire text MATCHES code (producer-asserted bookkeeping, not executed-gate) — PASS

- `_PROXY_NOTE` (`catch_rate_report.py:35-42`): states the model "enforces card_path
  NON-NULLNESS only (it is NOT an executed gate and does not stat the path)", that "All three
  is_fully_caught conjuncts (CATCH / negative_witness / card_path) are producer-asserted", and
  that "Card EXISTENCE (the impl ref having landed) is enforced UPSTREAM by the Phase 4
  requires_impl_ref skip-guard and the aggregation (which sets card_path only from a
  verified-existing ref)". Matches code exactly.
- Model module docstring (`catch_rate.py:19-27`) — "PRODUCER-ASSERTED bookkeeping contract
  (NOT executed-gate observations)"; explicitly "The data invariant this model enforces on
  card_path is NON-NULLNESS only; it does NOT stat the filesystem."
- `EscapeResult.card_path` docstring (`catch_rate.py:84-89`) — "The model's data invariant is
  NON-NULLNESS only ... the model does NOT stat the path. Card EXISTENCE is enforced upstream".
- Writer module docstring (`catch_rate_report.py:10-16`) — same producer-asserted framing.
- Code confirms the description: `is_fully_caught` (`catch_rate.py:107-113`) tests
  `card_path is not None` (non-nullness), no `.exists()`. `__post_init__` (`catch_rate.py:158-201`)
  performs only pure string/count/derivation checks — zero filesystem IO.
- No remaining "complete only reachable once impl refs land" overclaim attributed to the
  model's card_path check. Grep for `complete only reachable / only reachable once / impl refs
  land / once impl refs` in source modules: none.
- Residual "impl refs land" mentions are NOT the P3-2 overclaim:
  - `catch_rate.schema.json:116` — "null until impl refs land. A null card_path blocks complete
    (anti-vacuity)." Honest: describes producer behavior + the actual non-null invariant.
  - `fixtures/.../valid_full.json:17` — "this complete report presumes the impl refs landed."
    The hedge "presumes" explicitly states the report assumes (does not verify) landing — model-honest.
  - `fixtures/.../valid_minimal.json:11` — a producer-asserted `proxy_limitation` caveat string,
    not a claim about the model's card_path check enforcing existence.

### 2. P3-4 — markdown headline carries proxy qualifier inline; note directly under headline — PASS

- Headline (`catch_rate_report.py:107-110`): `## Catch rate (documentation-presence proxy):
  {caught}/{total} ({status})` — qualifier is INLINE in the headline, not just trailing.
- Proxy-limitation note appears DIRECTLY under the headline (`catch_rate_report.py:111-112`,
  `> Proxy limitation: ...`) AND at the tail (`:128`). A skimmer cannot read the bare number as
  executed-gate coverage.
- JSON `catch_rate` interpretation stays bound by the serialized `proxy_limitation` model field
  (a required, non-empty `__post_init__`-guarded field, `catch_rate.py:156,162-166`).

### 3. P3-2 helper `unresolved_card_paths` — genuine testable existence gate, NOT IO-in-model — PASS

- `unresolved_card_paths` (`catch_rate.py:262-284`) is a pure module-level helper; performs the
  on-disk check `(root / e.card_path).exists()` OUTSIDE the frozen model. Null card_paths are
  skipped (`:280-281`); non-existent paths returned (`:282-283`).
- `__post_init__` does NO filesystem IO (confirmed `catch_rate.py:158-201`), so the existence
  gate is correctly model-external.
- Test `test_backtest_unresolved_card_paths_existing_vs_fabricated`
  (`test_catch_rate_schema.py:269-307`): real existing files → `()` (`:288`); a fabricated path
  with no file on disk → `(fabricated,)` (`:307`). Real behavioral assertion, not a stub.

### 4. P3-5 — `_check` / `CatchRateContractViolation` docstrings precise (bypass/duck-typed) — PASS

- `_check` docstring (`catch_rate_report.py:68-74`): "for inputs that BYPASS the frozen model …
  Guards duck-typed / mutated reports whose `__post_init__` never ran (the fidelity test passes a
  `types.SimpleNamespace` directly into the renderer). For a constructible `CatchRateReport` this
  is intentionally redundant".
- `CatchRateContractViolation` docstring (`catch_rate_report.py:52-58`): "this guard protects
  inputs that BYPASS the frozen model … the fidelity test exercises exactly this via a
  `types.SimpleNamespace` … intentionally REDUNDANT … not as a claim that constructible reports
  can trip it."
- Overclaimed "defense in depth" language is GONE (grep for `defense in depth / defense-in-depth
  / defence in depth` in backtest dir: exit 1, no match).
- The described bypass path is real: `test_backtest_contract_violation_when_counts_unbalanced`
  (`test_catch_rate_schema.py:148-161`) feeds a `types.SimpleNamespace` (3+1 != 5) straight into
  `render_catch_rate_json`, which raises `CatchRateContractViolation`. Docstring matches the test.

### 5. No new vacuity; tests still assert real behavior — PASS

- `uv run pytest tests/troubleshoot/backtest/ -q` → 24 passed, 0 failed, 0 errored.
- proxy_limitation honesty is double-enforced (no empty caveat can ship): schema `minLength: 1`
  (`catch_rate.schema.json:64-67`) + model `__post_init__` non-empty/non-whitespace guard
  (`catch_rate.py:162-166`).
- Anti-vacuity derivation preserved: a CATCH count alone never earns `complete` — requires
  CATCH AND negative_witness AND non-null card_path for all escapes (`catch_rate.py:119-130`,
  `:189-201`); exercised by `test_backtest_anti_vacuity_*` and
  `test_backtest_complete_claim_with_null_card_raises` (`test_catch_rate_schema.py:200-252`).
- Idiom conformance (P3-1, cross-check): `write_catch_rate_report` guards FIRST
  (`catch_rate_report.py:149` `_check(report)` before `Path(output_dir)`/`mkdir` at `:156-157`),
  and renders both payloads to local strings before writing either (`:153-154`) — mirrors
  `write_aggregated_report` (`run_report.py:438` `_check_invariant(summary)` before the
  artifact-set write).

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**

- Relied on the prior Phase 3 structural lenses (status-derivation PASS, schema-fidelity PASS)
  for section/field-shape correctness; did not re-run the JSON Schema `required[]` pin check.

**(b) Independent semantic checks (≥1 required, INV-019):**

- Independently grep-verified the residual "impl refs land" occurrences (schema:116,
  valid_minimal:11, valid_full:17) and read each in context to confirm they describe
  producer/upstream behavior with honest hedges ("presumes", "blocks complete"), NOT the P3-2
  model-card_path existence overclaim — a semantic judgment rf-qa structural checks do not make.
- Independently read `run_report.py:420-439` to confirm the guard-before-mkdir idiom the writer
  claims to mirror is real (`_check_invariant` precedes dir creation), not just asserted.
- Independently ran the 24-test suite to confirm the SimpleNamespace bypass test actually
  exercises the `_check` path the P3-5 docstring now describes.

## Confidence

- Verified: 5/5 checkpoints | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- Tool engagement: Read: 6 | Grep: 2 | Bash(pytest): 1
