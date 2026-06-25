# Research 03 — Integration Points: contract.py Consumer & FR-RH2.7 Invariant

**Status:** Complete
**Date:** 2026-06-21
**Topic:** The exact contract keys, types, and truth conditions that `build_reflect_contract`
must produce so REAL adversarial findings flow into `derive_verdict` — WITHOUT changing
`derive_verdict` itself (FR-RH2.7 invariant).
**Scope:** `src/superclaude/cli/reflect/contract.py` + spec FR-RH2.7 acceptance bullet.

---

## 0. Headline Finding (the seam defect)

`build_reflect_contract` (`src/superclaude/cli/reflect/ensemble.py:360-407`) **hardcodes every
deviation / regression signal to a clean value**, so a REAL adversarial finding can NEVER reach
`derive_verdict`. The contract it emits always contains:

- `deviation_count_by_class: {authorized:0, necessary:0, drift:0, regression:0}` (ensemble.py:385-390)
- `regression_present: False` (ensemble.py:401)
- `unauthorized_deviation_present: False` (ensemble.py:402)
- `needs_human_decision: False` (ensemble.py:403)
- `user_decision_required: False` (ensemble.py:404)
- `status: "success"` (ensemble.py:379) — unconditional

`derive_verdict` is correct and must NOT change (FR-RH2.7); the fix is **ensemble-side mapping ONLY** —
`build_reflect_contract` must read the adversarial merge result and populate these fields from it. With
the current hardcoding, a faithful Tier-2 run that finds a regression still routes **PASS** (status
success + tier_reached==expected), exactly the silent-pass leak `contract.py`'s header warns about
(contract.py:10-12). The `report_path` IS sourced live (`_select_report_path`, ensemble.py:375/383) —
but it is the only live deviation/finding-bearing field; the verdict-driving signals are inert constants.

---

## 1. `derive_verdict` — the full first-match-wins ladder

`derive_verdict(contract, *, expected_tier, allow_single_vendor, child_rc)` at
`contract.py:130-246`. Ordering (header contract.py:12, docstring contract.py:139):
**blocked → degraded → halted → pass**, first-match-wins. The fields read, in order:

### Stage 1 — BLOCKED (fail-loud), contract.py:147-209
| Condition (in evaluation order) | Line | Verdict / reason |
|---|---|---|
| `child_rc == 124` | 148 | BLOCKED / `timeout` |
| `child_rc != 0` (any other non-zero) | 156 | BLOCKED / `child-crash` |
| `contract is None` | 160 | BLOCKED / `contract-missing` (or `child-crash`) |
| `contract_version` None/blank | 166-167 | BLOCKED / `contract-version-missing` |
| major version `!= "1"` | 174-175 | BLOCKED / `unknown-major-version` |
| `degraded_components` present but not a list | 184-187 | BLOCKED / `malformed-degraded-components` |
| any `_LOAD_BEARING_BOOL_FIELDS` member present, non-None, not `bool` | 200-203 | BLOCKED / `malformed-contract-boolean` |

### Stage 2 — DEGRADED, contract.py:211-225 (delegates to `_degraded_reason`, contract.py:249-304)
First matching FR-11 trigger returns a slug → DEGRADED:
- chain-critical `degraded_components` membership in `_DEGRADED_COMPONENTS_HALT_SET` (259) → `degraded-components`
- `expected_tier >= 2 and tier_reached == 1` (263) → `degraded-tier1`
- `t2_model_class_diversity` set and `!= "full"` (267-268) → `degraded-model-diversity`
- `t2_vendor_diversity == "single"` and not `allow_single_vendor` (272) → `single-vendor`
- `adversarial_unavailable is True` (276) → `adversarial-unavailable`
- `merge_method == "single-reviewer-fallback"` (280) → `single-reviewer-fallback`
- `tier_reached == 2 and adversarial_convergence_score is None` (284) → `null-convergence`
- `verification_ran is False` and skip-reason not exempt (288-290) → `verification-skipped`
- `citations_dropped > 0` (294-295) → `citations-dropped`
- `input_drift_detected is True` (301) → `input-drift`

### Stage 3 — HALTED, contract.py:227-232 (delegates to `_halted_reason`, contract.py:307-328)
**THIS is the stage REAL adversarial findings must trip.** First match returns a slug → HALTED (exit 10):
| Condition | Line | reason slug |
|---|---|---|
| `status == "failed"` | 311 | `status-failed` |
| `status == "partial"` | 313 | `status-partial` |
| `regression_present is True` | 315 | `regression` |
| `unauthorized_deviation_present is True` | 317 | `unauthorized-deviation` |
| `needs_human_decision is True` | 319 | `needs-human-decision` |
| `user_decision_required is True` | 321 | `user-decision-required` |
| `deviation_count_by_class.regression > 0` | 324 | `regression` |
| `deviation_count_by_class.drift > 0` | 326 | `drift` |

Note the strict-identity checks: `is True` (315, 317, 319, 321) — a non-bool truthy value would NOT
trigger here, but Stage 1's `_LOAD_BEARING_BOOL_FIELDS` guard (200-203) routes such malformed values to
BLOCKED first, so they never silently leak. The count-based fallbacks (324, 326) go through
`_extract_deviations` which coerces to int (see §2).

### Stage 4 — PASS, contract.py:234-246
- `contract.get("status") == "success" and tier_reached == expected_tier` (235) → PASS / `pass` (the **only** exit-0 path)
- otherwise (e.g. status success but tier mismatch) → HALTED / `tier-mismatch` (241-245)

**Consequence for the mapping target:** to make `derive_verdict` NON-pass when the seam reports a
regression, `build_reflect_contract` only needs to flip ONE of the Stage-3 signals to its truthy form
(`regression_present: True`, or `deviation_count_by_class.regression >= 1`, etc.). No change to
`derive_verdict` is required or permitted.

---

## 2. `_extract_deviations` — expected shape of `deviation_count_by_class`

`_extract_deviations(contract)` at `contract.py:90-101`; key set `_DEVIATION_KEYS = ("authorized",
"necessary", "drift", "regression")` at `contract.py:40`.

- Reads `contract["deviation_count_by_class"]` (contract.py:92).
- If the value is absent/None/falsey → `{}`; if not a dict → `{}` (contract.py:92-94).
- For each of the 4 keys: `int(raw.get(key, 0) or 0)`, with `TypeError`/`ValueError` → `0` (contract.py:96-100).
- **Output is always a 4-key dict of ints; any absent/malformed key coerces to 0.**

So the mapping target for counts is exactly: `deviation_count_by_class` = a dict with int values under
keys `authorized` / `necessary` / `drift` / `regression`. Only `regression > 0` (contract.py:324) and
`drift > 0` (contract.py:326) drive a HALT; `authorized`/`necessary` are inert for the verdict (they
matter only to `classify_fix`, contract.py:364). Same extractor is reused inside `_halted_reason`
(contract.py:323) and `classify_fix` (contract.py:361-364) — one source, no second parse.

---

## 3. `_LOAD_BEARING_BOOL_FIELDS` — full set + malformed-boolean path

`_LOAD_BEARING_BOOL_FIELDS` (frozenset) at `contract.py:47-57`:
```
regression_present
unauthorized_deviation_present
needs_human_decision
user_decision_required
adversarial_unavailable
input_drift_detected
verification_ran
```

Validation (the F2 fail-closed guard) at `contract.py:200-209`: for each field, `if _field in contract`
and `_value is not None and not isinstance(_value, bool)` → BLOCKED / `malformed-contract-boolean`.

- **Absent or `None` → flows normally** (no block); only a PRESENT non-None non-bool blocks.
- A string `"true"` or int `1` is NOT `is True`, so without this guard the Stage-3 `is True` checks
  would silently miss and leak to PASS — the guard converts that into a hard BLOCK (rationale at
  contract.py:42-46). **Implication for the mapping: `build_reflect_contract` MUST emit genuine Python
  `bool` (or omit/None), never `"True"`/`1`,** or it self-inflicts a BLOCKED verdict.
- `parse_contract` (contract.py:65-82) does NOT validate booleans — it only guarantees a dict (returns
  `None` on missing file / YAML error / non-mapping doc). All bool validation lives in `derive_verdict`'s
  Stage-1 loop, not in parse. `_make_result` (contract.py:104-127) reads fields defensively (`.get`,
  isinstance guards) and does NOT re-validate booleans.

---

## 4. Verdict → exit-code map (location)

Lives on the `Verdict` enum, NOT in contract.py: `Verdict.exit_code` property at
`src/superclaude/cli/reflect/models.py:38-49`:
```
PASS → 0    (the ONLY exit-0 path; models.py:15-16, is_promotable models.py:51-54)
HALTED → 10
DEGRADED → 11
BLOCKED → 2
```
Module docstring restates it at models.py:14-17. `derive_verdict` returns a `ReflectResult` carrying the
`Verdict`; the command keys process exit off `verdict.exit_code` (ReflectResult docstring models.py:108).

---

## 5. FR-RH2.7 acceptance bullet (quoted) — fix MUST be ensemble-side only

From `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md`:

**FR-RH2.7: Downstream return-contract consumers are unaffected** (spec.md:295). Description
(spec.md:297-299):
> "The reflect `return-contract.yaml` shape and the derived `reflect_post:` write-back +
> `wrapper-result.yaml` sidecar MUST remain compatible: existing fields keep their names/semantics; the
> verdict map and exit codes (`contract.py`, `models.py`) are unchanged."

Acceptance criteria (spec.md:301-305):
> - [ ] `derive_verdict` and the `Verdict` exit-code map (`pass→0`, `halted→10`, `degraded→11`,
>   `blocked→2`) are unchanged.
> - [ ] `write_reflect_post` produces the same `reflect_post:` field set/order; the sidecar keeps its fields.
> - [ ] Existing reflect contract/verdict tests pass without modification.

Corroborating "UNCHANGED" markers: the dataflow diagram tags step (4) as
`reflect derive_verdict (contract.py, UNCHANGED)` (spec.md:171); the architecture tree marks
`cli/reflect/contract.derive_verdict (UNCHANGED verdict map)` (spec.md:368); risk register notes the
verdict map + diversity/merge_method/single-reviewer degrade triggers are "preserved" (spec.md:647);
the open issue OI-1 (spec.md:597) frames the work as a swarm-`ResultContract`-field → reflect-contract
mapping table — i.e. the mapping lives in `ensemble.py`, not in `derive_verdict`.

**Conclusion: the fix is ensemble-side mapping ONLY.** `derive_verdict`, `_halted_reason`,
`_degraded_reason`, `_extract_deviations`, `_LOAD_BEARING_BOOL_FIELDS`, `_make_result`, `parse_contract`,
and `Verdict.exit_code` are all frozen. The only file that may change to wire real findings is
`ensemble.py` (`build_reflect_contract`).

---

## 6. Mapping-target table — contract key → type → NON-pass truth condition → adversarial-child source

The columns: what `build_reflect_contract` must emit, the type `derive_verdict` requires, the exact value
that makes `derive_verdict` NON-pass, and which adversarial merge field should source it. (The
adversarial-child emission shape is R2's scope; here we pin only the *consumer-side* requirement the seam
must satisfy.)

| Contract key | Required type | Value that makes `derive_verdict` NON-pass | derive_verdict line | Should source from |
|---|---|---|---|---|
| `regression_present` | `bool` (genuine) | `True` → HALTED `regression` | contract.py:315 | adversarial merge: any finding classified **Regression** |
| `deviation_count_by_class.regression` | `int` | `>= 1` → HALTED `regression` | contract.py:324 | count of Regression-class findings |
| `deviation_count_by_class.drift` | `int` | `>= 1` → HALTED `drift` | contract.py:326 | count of Drift-class findings |
| `unauthorized_deviation_present` | `bool` | `True` → HALTED `unauthorized-deviation` | contract.py:317 | any unauthorized-expansion finding |
| `needs_human_decision` | `bool` | `True` → HALTED `needs-human-decision` | contract.py:319 | grounding-gaps non-empty (per SKILL.md invariant cited in classify_fix, contract.py:346-351) |
| `user_decision_required` | `bool` | `True` → HALTED `user-decision-required` | contract.py:321 | any user-decision finding |
| `status` | `str` | `"failed"` → HALTED `status-failed`; `"partial"` → HALTED `status-partial`; anything `!= "success"` → not-PASS | contract.py:311/313/235 | overall merge outcome (currently hardcoded `"success"`, ensemble.py:379) |
| `report_path` | `str \| None` | (not a verdict driver) | — | adversarial merged-report path — ALREADY live via `_select_report_path` (ensemble.py:375/383) |
| `adversarial_convergence_score` | `float \| None` | at `tier_reached==2`, `None` → DEGRADED `null-convergence` | contract.py:284 | adversarial merge convergence score (param already threaded, ensemble.py:364/395) |

**Minimal correct fix for the TRACK GOAL test:** when the adversarial seam reports a regression,
`build_reflect_contract` must set `regression_present=True` (a genuine `bool`) and/or
`deviation_count_by_class["regression"] >= 1` (an `int`). Either alone trips Stage-3 HALTED at
contract.py:315 or :324 → `Verdict.HALTED` → exit 10. The assertion is therefore:
`derive_verdict(...).verdict is not Verdict.PASS` (specifically `is Verdict.HALTED`,
`reason == "regression"`).

**Type-trap to avoid (self-BLOCK):** emitting `regression_present="true"` (str) or `1` (int) would hit
the F2 guard (contract.py:200-203) and route **BLOCKED / malformed-contract-boolean** (exit 2) instead
of HALTED — a different non-PASS, but the wrong one and a contract bug. The mapping MUST emit a genuine
Python `bool`. Counts under `deviation_count_by_class` ARE expected to be ints (contract.py:96-100).

---

## 7. Notes for the test author (R4)

- A seam-reports-regression test can call `derive_verdict` directly over a `build_reflect_contract`
  output (or over a contract dict with `regression_present=True`) with `child_rc=0`,
  `expected_tier=2`, `tier_reached=2`, and assert `result.verdict is Verdict.HALTED` and
  `result.reason == "regression"` (NOT PASS). This pins the seam without touching `derive_verdict`.
- Existing unit `tests/cli/reflect/test_ensemble_unit.py:170` already calls
  `build_reflect_contract(workers, adversarial_convergence_score=0.86)` — the new test should extend the
  builder's signature/inputs to carry adversarial findings (R1/R2 scope) and assert the contract it emits
  flips the Stage-3 signal; then feed that contract through `derive_verdict` and assert non-PASS.
- Backward-compat guard (NFR-RH2.6, spec.md:475): `uv run pytest tests/cli/reflect -q` must stay green;
  the clean-path builder output (no findings) must still yield all-zero deviation counts and
  `regression_present=False` so a genuinely clean Tier-2 run still PASSes.

---

## Summary

- **The defect is in `build_reflect_contract` (ensemble.py:360-407), not `derive_verdict`.** All
  verdict-driving deviation/regression signals are hardcoded clean (`deviation_count_by_class` all-0
  ensemble.py:385-390; `regression_present/unauthorized_deviation_present/needs_human_decision/
  user_decision_required` all `False` ensemble.py:401-404; `status:"success"` ensemble.py:379), so real
  adversarial findings can never reach the consumer → a regression-finding Tier-2 run silently PASSes.
- **`derive_verdict` (contract.py:130-246) is correct and frozen by FR-RH2.7** (spec.md:295-305, plus
  UNCHANGED markers spec.md:171/368/647). Ladder = blocked→degraded→halted→pass, first-match-wins.
  Stage-3 HALTED (`_halted_reason`, contract.py:307-328) is where findings must land.
- **Minimal correct fix (ensemble-side ONLY):** map real findings onto `regression_present=True`
  (genuine `bool`) and/or `deviation_count_by_class["regression"] >= 1` (`int`). Either trips
  contract.py:315 / :324 → `Verdict.HALTED` → exit 10.
- **Type trap:** the F2 guard (contract.py:200-209, `_LOAD_BEARING_BOOL_FIELDS` contract.py:47-57) routes
  any present non-bool load-bearing field to BLOCKED/`malformed-contract-boolean`. Emit genuine Python
  `bool`s, never `"true"`/`1`. Counts under `deviation_count_by_class` are ints (contract.py:96-100).
- **Exit-code map** lives on `Verdict.exit_code` (models.py:38-49): pass→0, halted→10, degraded→11,
  blocked→2. Also frozen by FR-RH2.7.
- **Test seam:** feed a contract with a regression signal through `derive_verdict` (child_rc=0,
  expected_tier=2, tier_reached=2) and assert `verdict is Verdict.HALTED` / `reason == "regression"`
  (NOT PASS). Keep `tests/cli/reflect -q` green (NFR-RH2.6, spec.md:475) — clean path must still PASS.
