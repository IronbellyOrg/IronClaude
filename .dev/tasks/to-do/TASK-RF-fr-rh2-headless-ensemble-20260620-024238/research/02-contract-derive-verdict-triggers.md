# Research: contract.py derive_verdict + verdict triggers + Q6

- Status: Complete
- Date: 2026-06-20
- Scope: `src/superclaude/cli/reflect/contract.py` (367 lines, verified TODAY)
- Track: 1 of 1 — Integration Points (the reflect verdict layer / OI-1 consumer side + Q6)

All citations are `contract.py:LINE` against shipped source read 2026-06-20.

---

## 0. Q6 GREP RESULT (CRITICAL — read this first)

```
grep -rn "ensemble-empty" src/superclaude/cli/reflect/   -> ZERO matches (no output)
grep -rn "ensemble"       src/superclaude/cli/reflect/contract.py -> ZERO matches (no output)
```

**Confirmed: the slug `ensemble-empty` does NOT exist anywhere in contract.py, and the
substring `ensemble` does NOT appear in contract.py at all.** The TDD claim is correct.
The existing M==0 / empty-input path is handled exclusively by the structural BLOCKED
slugs already in the file (see Section 6 below). No ensemble-specific verdict branch
exists today.

**Q6 implication:** Option A (add a new `ensemble-empty` BLOCKED branch) would be a NET-NEW
edit to `derive_verdict` / `_make_result` reason strings — there is no existing slug to
overload. Option B (map an empty ensemble onto an existing structural slug such as
`contract-missing`, `child-crash`, or `malformed-degraded-components`) preserves
`derive_verdict` byte-for-byte; the new `ensemble.py` mapping layer would synthesize a
contract (or `None`) that lands on one of the existing slugs without touching contract.py.

---

## 1. `derive_verdict` — line range + verbatim ordering

- Signature + body: **contract.py:130-246**.
- Signature (contract.py:130-136):
  ```
  def derive_verdict(
      contract: dict | None,
      *,
      expected_tier: int,
      allow_single_vendor: bool,
      child_rc: int,
  ) -> ReflectResult:
  ```
- Verbatim ordering claim (docstring, contract.py:139):
  > "Ordering: blocked -> degraded -> halted -> pass."
- Also stated in the module docstring (contract.py:11-12):
  > "so the ordering is exact: **blocked -> degraded -> halted -> pass**, first-match-wins."
- Stage markers in the body confirm first-match-wins ordering:
  - `# -- 1. BLOCKED (fail-loud)` — contract.py:147
  - `# -- 2. DEGRADED (chain-critical loss -> audit untrustworthy)` — contract.py:211
  - `# -- 3. HALTED (trustworthy audit FOUND deviations/partial)` — contract.py:227
  - `# -- 4. PASS (only when status success AND expected tier reached)` — contract.py:234

**VERIFIED: spec/TDD ordering claim (blocked → degraded → halted → pass, first-match-wins) matches shipped source.**

---

## 2. `_degraded_reason` — every trigger, line, predicate, returned slug

- Function: **contract.py:249-304**.
- Signature (contract.py:249-256): `_degraded_reason(contract, *, degraded_components, tier_reached, expected_tier, allow_single_vendor) -> str | None`.

Triggers in shipped order (first-match-wins, returns slug):

| Shipped # | Line | Predicate (exact) | Returned slug |
|-----------|------|-------------------|---------------|
| 1-5 | 259-260 | `any(token in _DEGRADED_COMPONENTS_HALT_SET for token in degraded_components)` (exact membership, NOT substring) | `degraded-components` |
| 6 | 263-264 | `expected_tier >= 2 and tier_reached == 1` | `degraded-tier1` |
| 7 | 267-269 | `mcd = contract.get("t2_model_class_diversity"); mcd is not None and mcd != "full"` | `degraded-model-diversity` |
| 8 | 272-273 | `contract.get("t2_vendor_diversity") == "single" and not allow_single_vendor` | `single-vendor` |
| 9 | 276-277 | `contract.get("adversarial_unavailable") is True` | `adversarial-unavailable` |
| 10 | 280-281 | `contract.get("merge_method") == "single-reviewer-fallback"` | `single-reviewer-fallback` |
| 11 | 284-285 | `tier_reached == 2 and contract.get("adversarial_convergence_score") is None` | `null-convergence` |
| 12 | 288-291 | `contract.get("verification_ran") is False` AND `verification_skip_reason not in _VERIFICATION_SKIP_EXEMPTIONS` | `verification-skipped` |
| 13 | 294-298 | `int(contract.get("citations_dropped", 0) or 0) > 0` (TypeError/ValueError swallowed) | `citations-dropped` |
| 14 | 301-302 | `contract.get("input_drift_detected") is True` | `input-drift` |
| — | 304 | fallthrough | `return None` |

`_DEGRADED_COMPONENTS_HALT_SET` (contract.py:31-33): `{"serena", "auggie", "env-aliases", "evidence-validator", "serena:context-excluded"}`.
`_VERIFICATION_SKIP_EXEMPTIONS` (contract.py:36-38): `{"read-only-project", "tool-unavailable", "--no-verify"}`.

**TDD trigger-by-trigger verification:**
- Trigger 7 = `t2_model_class_diversity` set AND `!= "full"` — **VERIFIED** (contract.py:267-269; guards T1-null via `mcd is not None`).
- Trigger 8 = `t2_vendor_diversity == "single"` AND NOT allow_single_vendor — **VERIFIED** (contract.py:272-273).
- Trigger 9 = `adversarial_unavailable is True` — **VERIFIED** (contract.py:276-277).
- Trigger 10 = `merge_method == "single-reviewer-fallback"` — **VERIFIED** (contract.py:280-281).
- Trigger 11 = `tier_reached == 2` AND `adversarial_convergence_score is None` — **VERIFIED** (contract.py:284-285).
- Trigger 12 = verification — **VERIFIED** (contract.py:288-291; note the exemption sub-condition).
- Trigger 13 = citations_dropped — **VERIFIED** (contract.py:294-298).
- Trigger 14 = input_drift — **VERIFIED** (contract.py:301-302; keys on `input_drift_detected`, not `input_drift`).

**Trigger-numbering note:** the TDD numbers triggers 1-14, but the shipped code collapses
1-5 into a single membership test (one slug `degraded-components`, contract.py:259-260).
So there are 10 distinct `if` branches, not 14, but the TDD's 7-14 predicates all map
1:1 to shipped branches as verified above. No predicate drift found.

---

## 3. `_halted_reason` — every trigger + line

- Function: **contract.py:307-328**. Signature: `_halted_reason(contract: dict) -> str | None`.

| Line | Predicate | Returned slug |
|------|-----------|---------------|
| 311-312 | `contract.get("status") == "failed"` | `status-failed` |
| 313 | `contract.get("status") == "partial"` | `status-partial` |
| 315-316 | `contract.get("regression_present") is True` | `regression` |
| 317-318 | `contract.get("unauthorized_deviation_present") is True` | `unauthorized-deviation` |
| 319-320 | `contract.get("needs_human_decision") is True` | `needs-human-decision` |
| 321-322 | `contract.get("user_decision_required") is True` | `user-decision-required` |
| 323-325 | `deviations = _extract_deviations(contract); deviations["regression"] > 0` | `regression` |
| 326-327 | `deviations["drift"] > 0` | `drift` |
| 328 | fallthrough | `return None` |

Note: `_halted_reason` consumes `deviation_count_by_class` via `_extract_deviations`
(contract.py:323) for the regression/drift count triggers. The TDD's
`deviation_count_by_class` trigger is split into two: regression count (line 324) and
drift count (line 326). `needs_human_decision`, `user_decision_required`,
`regression_present`, `unauthorized_deviation_present` all VERIFIED present.

---

## 4. Stage-1 BLOCKED guards — line-by-line

All inside `derive_verdict`, stage 1 (contract.py:147-209). First-match-wins:

| Line | Guard | reason slug |
|------|-------|-------------|
| 148-151 | `child_rc == 124` (timeout) | `timeout` |
| 156-159 | `child_rc != 0` (any other non-zero → child-crash, F0 veto) | `child-crash` |
| 160-164 | `contract is None` (reason ternary: `child-crash` if rc!=0 else `contract-missing`; rc==0 here so effectively `contract-missing`) | `contract-missing` (or `child-crash`) |
| 166-173 | `version = contract.get("contract_version"); version is None or not str(version).strip()` | `contract-version-missing` |
| 174-181 | `major = str(version).strip().split(".")[0].strip(); major != "1"` | `unknown-major-version` |
| 184-193 | `degraded_components` shape guard: None→`[]`; if `not isinstance(degraded_components, list)` → BLOCKED | `malformed-degraded-components` |
| 200-209 | F2 load-bearing-bool guard: for each `_field in _LOAD_BEARING_BOOL_FIELDS`, if present AND `_value is not None and not isinstance(_value, bool)` → BLOCKED | `malformed-contract-boolean` |

- `_LOAD_BEARING_BOOL_FIELDS` (contract.py:47-57): `{regression_present, unauthorized_deviation_present, needs_human_decision, user_decision_required, adversarial_unavailable, input_drift_detected, verification_ran}`.
- `tier_reached = contract.get("tier_reached")` is read at contract.py:195 (between the degraded_components guard and the F2 bool guard).

All four TDD-claimed Stage-1 guard families VERIFIED:
124→timeout (148), other nonzero→child-crash (156), contract-version absent/blank→`contract-version-missing` (167), major≠"1"→`unknown-major-version` (175), degraded_components list-shape→`malformed-degraded-components` (187), non-bool load-bearing field→`malformed-contract-boolean` (203). The "F0 veto" is the `child_rc != 0` branch at 156-159.

---

## 5. parse_contract + _make_result + PASS gate

- `parse_contract(path: Path) -> dict | None` — signature **contract.py:65**, body 65-82.
  Returns `None` on OSError (73-75), `None` on `yaml.YAMLError` (76-79), `None` if
  parsed doc is not a dict (80-81), else the dict (82). Tolerates unknown top-level
  fields (NFR-8 read-and-ignore).
- `_make_result(...)` — line range **contract.py:104-127**. Signature 104-110:
  `_make_result(verdict, *, reason, contract, child_rc) -> ReflectResult`. Reads
  contract fields defensively: `status` (118), `tier_reached` coerced to int-or-None
  (116-117), `report_path` (119), `remediation_task_path` (126), and `deviations` via
  `_extract_deviations` (122). `contract_path` is set to `None` (120) — runner fills it.
- **PASS gate (contract.py:235):** `if contract.get("status") == "success" and tier_reached == expected_tier:` → `Verdict.PASS, reason="pass"` (236-238).
  If NOT satisfied (e.g. status success but tier mismatch) → falls through to
  `Verdict.HALTED, reason="tier-mismatch"` (241-246).

**VERIFIED: PASS requires BOTH `status == "success"` AND `tier_reached == expected_tier`.**

---

## 6. Q6 — the COMPLETE verbatim list of existing BLOCKED reason slugs in contract.py

Every `_make_result(Verdict.BLOCKED, reason="...")` call in the file:

| Slug | Line |
|------|------|
| `timeout` | 150 |
| `child-crash` | 158 (and conditional 161 ternary) |
| `contract-missing` | 161 (ternary, when child_rc == 0) |
| `contract-version-missing` | 170 |
| `unknown-major-version` | 176 |
| `malformed-degraded-components` | 189 |
| `malformed-contract-boolean` | 205 |

That is the FULL set: `{timeout, child-crash, contract-missing, contract-version-missing,
unknown-major-version, malformed-degraded-components, malformed-contract-boolean}`.
**`ensemble-empty` is NOT among them.** All existing BLOCKED slugs are structural
(child process / contract file integrity), confirming the TDD claim.

---

## 7. OI-1 LEFT COLUMN — every contract field `derive_verdict` (+ its helpers) reads

These are the fields the new `ensemble.py` mapping layer must synthesize into the
contract dict it feeds `derive_verdict`. Grouped by stage; each with the line where read.

**Top-level / Stage-1 (in `derive_verdict`):**
- `contract_version` — contract.py:166 (BLOCKED gate; must be present, non-blank, major "1")
- `degraded_components` (list) — contract.py:184 (shape-guarded; feeds trigger 1-5)
- `tier_reached` — contract.py:195 (also coerced in `_make_result` 116; PASS gate 235; degraded triggers 6 & 11)
- all of `_LOAD_BEARING_BOOL_FIELDS` if present must be real bools — contract.py:200-203:
  `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`,
  `user_decision_required`, `adversarial_unavailable`, `input_drift_detected`,
  `verification_ran`
- `status` — contract.py:235 (PASS gate); also `_make_result` 118; `_halted_reason` 311, 313

**DEGRADED stage (`_degraded_reason`):**
- `t2_model_class_diversity` — contract.py:267
- `t2_vendor_diversity` — contract.py:272
- `adversarial_unavailable` — contract.py:276
- `merge_method` — contract.py:280
- `adversarial_convergence_score` — contract.py:284
- `verification_ran` — contract.py:288
- `verification_skip_reason` — contract.py:289
- `citations_dropped` — contract.py:295
- `input_drift_detected` — contract.py:301
- (`degraded_components`, `tier_reached`, `expected_tier`/`allow_single_vendor` passed as kwargs)

**HALTED stage (`_halted_reason`):**
- `status` — contract.py:311, 313
- `regression_present` — contract.py:315
- `unauthorized_deviation_present` — contract.py:317
- `needs_human_decision` — contract.py:319
- `user_decision_required` — contract.py:321
- `deviation_count_by_class` (via `_extract_deviations`) — contract.py:323 (keys: regression 324, drift 326)

**`_make_result` reads (telemetry, every verdict):**
- `status` (118), `tier_reached` (116), `report_path` (119), `remediation_task_path` (126),
  `deviation_count_by_class` via `_extract_deviations` (122).

**`_extract_deviations` (contract.py:90-101):** reads `deviation_count_by_class` (92),
coerces 4 keys `authorized, necessary, drift, regression` (`_DEVIATION_KEYS`, contract.py:40)
to int (absent/malformed → 0).

**Consolidated unique OI-1 field list (what ensemble.py must be able to produce):**
`contract_version`, `status`, `tier_reached`, `degraded_components`,
`deviation_count_by_class`, `report_path`, `remediation_task_path`,
`regression_present`, `unauthorized_deviation_present`, `needs_human_decision`,
`user_decision_required`, `adversarial_unavailable`, `input_drift_detected`,
`verification_ran`, `verification_skip_reason`, `t2_model_class_diversity`,
`t2_vendor_diversity`, `merge_method`, `adversarial_convergence_score`,
`citations_dropped`.

(`classify_fix`, contract.py:331-366, is a separate downstream consumer used by the
runner on a trustworthy HALTED result — not part of `derive_verdict`'s read set, but
it keys on the SAME fields: `regression_present`, `needs_human_decision`,
`user_decision_required`, `unauthorized_deviation_present`, and
`deviation_count_by_class.{regression,drift,necessary}`.)
