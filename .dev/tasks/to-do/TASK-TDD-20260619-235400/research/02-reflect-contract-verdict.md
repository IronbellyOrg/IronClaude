# 02 — Reflect Contract Verdict Derivation (Reflect-Side OI-1 Half)

- **Topic:** `derive_verdict` field-correspondence — every `return-contract.yaml` field the reflect wrapper reads, its type/semantics, the verdict branch that consumes it, and absent/malformed behavior.
- **Investigation type:** Data Model Analyst
- **Scope:** `src/superclaude/cli/reflect/contract.py` (verdict derivation, degraded routing) + `src/superclaude/cli/reflect/models.py` (`Verdict` enum, exit-code map, `ReflectResult` dataclass). This is the REFLECT-SIDE half of the load-bearing OI-1 contract field-correspondence table.
- **Status:** Complete
- **Date:** 2026-06-20
- **Source of truth:** the actual code in the worktree (line numbers re-verified against the files read this turn).

---

## 1. The 4-State Verdict Enum + Exit-Code Map `[CODE-VERIFIED]`

Source: `models.py` `Verdict` enum (L26–54).

| Verdict | enum value | `exit_code` | `is_promotable` | Semantics |
|---|---|---|---|---|
| `PASS` | `"pass"` | `0` | `True` | The **only** exit-0 path. Clean, full, non-degraded, expected-tier-reached audit. |
| `HALTED` | `"halted"` | `10` | `False` | Trustworthy audit that **found** real problems (deviations / partial / failed / tier-mismatch). |
| `DEGRADED` | `"degraded"` | `11` | `False` | Chain-critical capability loss → audit is **untrustworthy** (cannot be trusted to have found problems). |
| `BLOCKED` | `"blocked"` | `2` | `False` | Fail-loud: contract missing / unparseable / wrong major version / malformed load-bearing field / child crash/timeout. |

Exit-code map is hard-coded in `Verdict.exit_code` (L44–49): `{PASS:0, HALTED:10, DEGRADED:11, BLOCKED:2}`. `is_promotable` (L51–54) returns `True` IFF `self is Verdict.PASS`.

### Load-bearing ordering (first-match-wins) `[CODE-VERIFIED]`

`derive_verdict` (contract.py L130–246) evaluates branches in a **fixed order**, returning on the first match:

```
1. BLOCKED  (fail-loud pre-checks)   ← evaluated FIRST
2. DEGRADED (chain-critical loss)
3. HALTED   (audit found problems)
4. PASS     (success + expected tier) ← evaluated LAST
```

Module docstring (L10–12) states the rationale explicitly: a wrong verdict map "silently leaks a degraded audit as a pass," so the ordering is exact `blocked -> degraded -> halted -> pass`, first-match-wins.

**The load-bearing M==0 ordering:** the BLOCKED checks (child-crash, contract-missing, version, and the malformed-field guards) are ordered structurally **AHEAD** of any degraded/halted/pass decision. Specifically, when the contract is absent / unparseable / has the wrong major version / has a malformed `degraded_components` (non-list) or a malformed load-bearing boolean, the function returns `BLOCKED` (exit 2) **before** `_degraded_reason` or `_halted_reason` is ever consulted. This is the M==0 → blocked/exit-2 guarantee: zero trustworthy signal must route to BLOCKED, never be evaluated as a candidate for degraded/halted/pass. A non-bool truthy field (e.g. the string `"true"`) would otherwise fail the `is True` identity checks downstream and silently leak to PASS — the F2 guard (L200–209) blocks it first.

---

## 2. Field-Correspondence Table — BLOCKED Branch (Stage 1) `[CODE-VERIFIED]`

These fields are consumed by `derive_verdict` itself (L147–209), BEFORE delegation to `_degraded_reason` / `_halted_reason`. Non-contract inputs (`child_rc`, `expected_tier`, `allow_single_vendor`) are call-args, not contract fields, but listed for completeness since they gate the BLOCKED stage.

| Field (contract key) | Type | Semantics | Verdict branch consuming it | Absent / malformed behavior |
|---|---|---|---|---|
| *(call-arg)* `child_rc` | `int` | Child `claude` process exit code. `124` == timeout. | BLOCKED stage 1 (L148–159) | `124` → BLOCKED `reason="timeout"`. Any other non-zero → BLOCKED `reason="child-crash"` (F0 fail-closed veto, L156–159). `0` → proceed. |
| *(whole contract)* | `dict \| None` | Parsed `return-contract.yaml` mapping. | BLOCKED (L160–164) | `None` (missing file / YAML-unparseable / non-mapping per `parse_contract` L65–82) → BLOCKED `reason="contract-missing"` (or `child-crash` if rc≠0). |
| `contract_version` | `str` (e.g. `"1.x"`) | Schema version; only major `1` accepted. | BLOCKED (L166–181) | Absent / `None` / blank-after-strip → BLOCKED `reason="contract-version-missing"`. Major part (`split(".")[0]`) ≠ `"1"` → BLOCKED `reason="unknown-major-version"`. |
| `degraded_components` | `list[str]` | Telemetry list of degraded capability tokens (FR-11 chain-critical subset). | BLOCKED guard here (L184–193); consumed for degraded in stage 2. | Absent → `[]`. `None` → `[]`. Present but **not a list** → BLOCKED `reason="malformed-degraded-components"`. |
| `tier_reached` | `int` (1 or 2) | Highest reflection tier actually reached by the audit. | Read at L195; consumed in degraded (T1 trigger, null-convergence) + pass (tier match). | Read raw via `.get` (no block here); in `_make_result` (L116–117) coerced to `None` if not `int`. |
| `regression_present` | `bool` | (load-bearing bool) Audit detected a regression. | F2 guard here (L200–209); consumed in HALTED + `classify_fix`. | Absent / `None` → flows normally. Present but **not a bool** → BLOCKED `reason="malformed-contract-boolean"`. |
| `unauthorized_deviation_present` | `bool` | (load-bearing bool) Unauthorized deviation found. | F2 guard (L200–209); HALTED + `classify_fix`. | Same F2 rule: present non-bool → BLOCKED. |
| `needs_human_decision` | `bool` | (load-bearing bool) Grounding-gaps non-empty → human required. | F2 guard (L200–209); HALTED + `classify_fix`. | Same F2 rule: present non-bool → BLOCKED. |
| `user_decision_required` | `bool` | (load-bearing bool) Explicit user decision gate. | F2 guard (L200–209); HALTED + `classify_fix`. | Same F2 rule: present non-bool → BLOCKED. |
| `adversarial_unavailable` | `bool` | (load-bearing bool) Adversarial merge could not run. | F2 guard (L200–209); DEGRADED trigger 9. | Same F2 rule: present non-bool → BLOCKED. |
| `input_drift_detected` | `bool` | (load-bearing bool) Spec/input drifted from audited state. | F2 guard (L200–209); DEGRADED trigger 14. | Same F2 rule: present non-bool → BLOCKED. |
| `verification_ran` | `bool` | (load-bearing bool) Whether verification actually executed. | F2 guard (L200–209); DEGRADED trigger 12 (uses `is False`). | Same F2 rule: present non-bool → BLOCKED. |

The `_LOAD_BEARING_BOOL_FIELDS` frozenset (L47–57) enumerates the seven F2-guarded booleans. The guard loop (L200–209) only blocks a field that is **present, non-None, and not an actual `bool`** — absent or `None` values flow through. This is the fail-closed defense (F2): a malformed-but-truthy `"true"`/`1` is not `is True`, so without the guard the downstream identity checks would silently not fire and leak to PASS.

---

## 3. Field-Correspondence Table — DEGRADED Branch (Stage 2) `[CODE-VERIFIED]`

Consumed by `_degraded_reason` (contract.py L249–304). Triggers evaluated in order, first-match-wins; each returns a reason slug; all map to `Verdict.DEGRADED` → exit 11. Two inputs (`degraded_components`, `tier_reached`) are passed from `derive_verdict`; the rest are read inside `_degraded_reason` via `contract.get`.

| Field (contract key) | Type | Semantics | Trigger / reason slug | Absent / malformed behavior |
|---|---|---|---|---|
| `degraded_components` | `list[str]` | Chain-critical capability-loss tokens. | Trigger 1–5 (L259–260): any token ∈ `_DEGRADED_COMPONENTS_HALT_SET` → `"degraded-components"`. | Already normalized to `[]` in stage 1; empty → no trigger. **Exact membership** (not substring) so benign fail-open tokens don't over-degrade. |
| `tier_reached` *(+ `expected_tier` arg)* | `int` | Reached tier vs expected. | Trigger 6 (L263–264): `expected_tier >= 2 and tier_reached == 1` → `"degraded-tier1"`. | If `tier_reached` not `1`, no trigger here. |
| `t2_model_class_diversity` | `str` (e.g. `"full"`) | Diversity of model classes across T2 reviewers. | Trigger 7 (L267–269): set AND `!= "full"` → `"degraded-model-diversity"`. | T1-null guard: `None` → skipped (no trigger). Only a present non-`"full"` value triggers. |
| `t2_vendor_diversity` | `str` (e.g. `"single"`) | Vendor diversity across T2 reviewers. | Trigger 8 (L272–273): `== "single"` AND NOT `allow_single_vendor` → `"single-vendor"`. | Absent / other value → no trigger. Suppressed by `--allow-single-vendor` (call-arg `allow_single_vendor`). |
| `adversarial_unavailable` | `bool` | Adversarial merge could not run. | Trigger 9 (L276–277): `is True` → `"adversarial-unavailable"`. | Strict `is True`. (F2-guarded upstream so present non-bool already BLOCKED.) |
| `merge_method` | `str` | How reviewer outputs were merged. | Trigger 10 (L280–281): `== "single-reviewer-fallback"` → `"single-reviewer-fallback"`. | Absent / any other value → no trigger. |
| `adversarial_convergence_score` | numeric \| `None` | Adversarial convergence at T2. | Trigger 11 (L284–285): `tier_reached == 2` AND value `is None` → `"null-convergence"`. | Guard: only checked when `tier_reached == 2`. At T1 it is ignored even if `None`. |
| `verification_ran` | `bool` | Whether verification executed. | Trigger 12 (L288–291): `is False` AND `verification_skip_reason` ∉ exemptions → `"verification-skipped"`. | `is False` only (not falsy). Absent/`True` → no trigger. |
| `verification_skip_reason` | `str` | Why verification was skipped. | Read inside trigger 12 (L289). | If ∈ `_VERIFICATION_SKIP_EXEMPTIONS` (`read-only-project`, `tool-unavailable`, `--no-verify`) → exempt (no degrade). Any other value (incl. absent → `None`) → degrade. |
| `citations_dropped` | `int` | Count of citations dropped (sample-count, NOT extrapolated). | Trigger 13 (L294–298): `int(...) > 0` → `"citations-dropped"`. | Absent → `0`. `None`/non-int → coerced; `TypeError`/`ValueError` caught → no trigger. |
| `input_drift_detected` | `bool` | Spec/input drifted. | Trigger 14 (L301–302): `is True` → `"input-drift"`. | Strict `is True`. Absent → no trigger. |

`_DEGRADED_COMPONENTS_HALT_SET` (L31–33) = `{"serena", "auggie", "env-aliases", "evidence-validator", "serena:context-excluded"}`. Membership is exact (the comment at L27–30 names the benign fail-open tokens deliberately excluded). `_VERIFICATION_SKIP_EXEMPTIONS` (L36–38) = `{"read-only-project", "tool-unavailable", "--no-verify"}`.

---

## 4. Field-Correspondence Table — HALTED Branch (Stage 3) `[CODE-VERIFIED]`

Consumed by `_halted_reason` (contract.py L307–328). Reached only when stages 1–2 produced no match (contract is well-formed AND not degraded → trustworthy audit). First-match-wins; all map to `Verdict.HALTED` → exit 10.

| Field (contract key) | Type | Semantics | Trigger / reason slug | Absent / malformed behavior |
|---|---|---|---|---|
| `status` | `str` | Audit completion status. | L311–314: `== "failed"` → `"status-failed"`; `== "partial"` → `"status-partial"`. | Absent / `"success"` / other → no halt here (deferred to PASS/tier-mismatch in `derive_verdict`). |
| `regression_present` | `bool` | Regression detected. | L315–316: `is True` → `"regression"`. | Strict `is True`. (F2-guarded upstream.) |
| `unauthorized_deviation_present` | `bool` | Unauthorized deviation found. | L317–318: `is True` → `"unauthorized-deviation"`. | Strict `is True`. |
| `needs_human_decision` | `bool` | Human decision required (grounding-gaps non-empty). | L319–320: `is True` → `"needs-human-decision"`. | Strict `is True`. |
| `user_decision_required` | `bool` | User decision gate. | L321–322: `is True` → `"user-decision-required"`. | Strict `is True`. |
| `deviation_count_by_class` | `dict[str,int]` | Per-class deviation counts (keys: authorized/necessary/drift/regression). | L323–327 via `_extract_deviations`: `regression > 0` → `"regression"`; `drift > 0` → `"drift"`. | Absent / non-dict / non-int values → each key coerced to `0` (`_extract_deviations` L90–101, try/except). |

`_extract_deviations` (L90–101) pulls `deviation_count_by_class` into a fixed 4-key int dict (`_DEVIATION_KEYS = ("authorized","necessary","drift","regression")`, L40). Non-dict raw → `{}`; any non-coercible value → `0`. This same dict is also stored on `ReflectResult.deviations` (via `_make_result` L121).

---

## 5. Field-Correspondence Table — PASS / fall-through (Stage 4) `[CODE-VERIFIED]`

Consumed by `derive_verdict` directly (L234–246), only when stages 1–3 produced no match.

| Field (contract key) | Type | Semantics | Branch | Absent / malformed behavior |
|---|---|---|---|---|
| `status` | `str` | Audit completion status. | PASS gate (L235): `status == "success"` AND `tier_reached == expected_tier` → `Verdict.PASS` reason `"pass"`. | Not `"success"` → falls through to `tier-mismatch` HALTED (L241–246). |
| `tier_reached` | `int` | Reached tier. | PASS gate (L235) requires `== expected_tier`. | Mismatch (e.g. success but wrong tier) → `Verdict.HALTED` reason `"tier-mismatch"` (L241–246). |

**Fall-through:** if a well-formed, non-degraded, non-halted contract is `status == "success"` but `tier_reached != expected_tier`, it is HALTED (`"tier-mismatch"`), NOT pass. PASS is the only path returning exit 0 and requires BOTH conditions.

---

## 6. `ReflectResult` Construction (`_make_result`, L104–127) `[CODE-VERIFIED]`

Every verdict branch builds its result via `_make_result`, which reads contract fields defensively (`c = contract or {}`):

| `ReflectResult` field | Source | Notes |
|---|---|---|
| `verdict` | branch arg | the derived `Verdict`. |
| `status` | `contract["status"]` | raw `.get`, may be `None`. |
| `tier_reached` | `contract["tier_reached"]` | coerced to `None` if not `int` (L116–117). |
| `reason` | branch arg | reason slug. |
| `report_path` | `contract["report_path"]` | may be `None`. |
| `contract_path` | hard `None` | runner fills the pinned path it parsed (L122). |
| `deviations` | `_extract_deviations(contract)` | the 4-key int dict. |
| `child_exit_code` | `child_rc` arg | passthrough. |
| `write_status` | `""` | runner finalizes after write-back. |
| `remediation_task_path` | `contract["remediation_task_path"]` | FR-8: wrapper only READS reflect's emitted path; default `None`. |

`ReflectResult` dataclass (models.py L94–121) additionally defaults `fix_iterations=0`, `fix_converged=False` (auto-fix loop bookkeeping, set by runner — not by `_make_result`). `ReflectResult.outcome` (L118–121) returns `"success"` IFF `verdict is Verdict.PASS`, else `"failed"`.

---

## 7. `classify_fix` field reads (L331–366) `[CODE-VERIFIED]`

Not part of `derive_verdict` ordering, but reads the same contract fields. Pure carve-out consulted ONLY on a trustworthy HALTED result. Returns `"human-required"` / `"auto-fixable"` / `"none"`.

- **HUMAN-REQUIRED** on ANY: `regression_present is True`, `needs_human_decision is True`, `user_decision_required is True`, `unauthorized_deviation_present is True`, OR `deviations["regression"] > 0` (L356–363).
- **AUTO-FIXABLE** only with NO hard signal AND `deviations["drift"] > 0 or deviations["necessary"] > 0` (L364–365).
- Otherwise **"none"** (clean) (L366).

Load-bearing invariant (docstring L346–354): the grounding-gaps → HUMAN-REQUIRED carve-out rests entirely on reflect's guarantee that `needs_human_decision is True` IFF `grounding-gaps.yaml` is non-empty. The wrapper does NOT re-parse grounding-gaps.

---

## Key Takeaways

1. **Ordering is the safety property.** `derive_verdict` is `blocked → degraded → halted → pass`, first-match-wins (contract.py L130–246; docstring L10–12; enum docstring models.py L29–30). The whole design exists to stop a degraded/untrustworthy audit leaking to PASS.
2. **M==0 → BLOCKED is structural, not derived.** Missing/unparseable/non-mapping contract, missing/blank `contract_version`, major≠1, non-list `degraded_components`, and any present-but-non-bool load-bearing boolean ALL return `BLOCKED` (exit 2) at stage 1 BEFORE `_degraded_reason`/`_halted_reason` run (L147–209). Zero trustworthy signal never reaches a degrade/halt/pass evaluation.
3. **Exit-code map is the contract:** `pass→0` (only exit-0 path), `halted→10`, `degraded→11`, `blocked→2` (models.py L44–49). Hard-coded; `is_promotable` ⇔ `PASS`.
4. **Three fail-closed defenses (F0/F2 + malformed-list guard):** F0 = any non-zero `child_rc` vetoes a present contract → BLOCKED (L156–159). F2 = present non-bool load-bearing field → BLOCKED (L200–209). Malformed `degraded_components` (non-list) → BLOCKED (L187–193). Each prevents a silent leak past the strict `is True`/`is False` identity checks.
5. **Strict identity, not truthiness.** All boolean triggers use `is True` (or `is False` for `verification_ran`) — never bare truthiness. This is WHY the F2 malformed-bool guard is required.
6. **Guarded degrade triggers:** `t2_model_class_diversity` (only when set), `adversarial_convergence_score` (only at `tier_reached==2`), `verification_ran is False` (exempted by 3 skip reasons), `single-vendor` (suppressible by `--allow-single-vendor`). These guards prevent T1-null false degrades.
7. **`single-reviewer-fallback`** is a degraded trigger via `merge_method == "single-reviewer-fallback"` (L280–281) → reason `"single-reviewer-fallback"` → exit 11. This matches the known benign exit-11 "degraded (single-reviewer-fallback)" behavior.
8. **PASS requires two conjuncts:** `status == "success"` AND `tier_reached == expected_tier`. Success-but-tier-mismatch falls through to HALTED `"tier-mismatch"` (L235–246).

## Gaps and Questions

- **OI-1 producer side not in scope here.** This document covers only the REFLECT-WRAPPER CONSUMER half (`contract.py`/`models.py`). The PRODUCER side — where/how `/sc:reflect` (the skill / `reflect_post`) actually emits each field into `return-contract.yaml`, and whether the emitted types match the consumer's expectations — is `[UNVERIFIED]` from this investigation and must be cross-checked against the skill's contract-writing code (e.g. `src/superclaude/skills/sc-reflect/**`, SKILL.md contract section) to complete the field-correspondence table. The docstring at L346–354 cites `SKILL.md:754` for the `needs_human_decision` IFF grounding-gaps guarantee, which should be verified against the actual SKILL.md.
- **`t2_model_class_diversity` / `t2_vendor_diversity` enum domains** `[UNVERIFIED]`: code only checks `!= "full"` and `== "single"` respectively. The full set of valid values (e.g. `"full"`/`"partial"`/`None` and `"single"`/`"multi"`) is not enumerated in `contract.py` — confirm against producer.
- **`adversarial_convergence_score` numeric type** `[UNVERIFIED]`: code only tests `is None`; the numeric type (float 0–1 vs int) is not asserted by the consumer.
- **Task brief line-number drift (now corrected):** the brief's approximate citations (`_degraded_reason ~L249`, model-diversity `~L267-269`, single-reviewer `~L280-281`) are CORRECT as re-verified. `derive_verdict` is at L130 (brief said ~L130 ✓); ordering constant referenced as ~L12/~L139 maps to the docstring L10–12 and the `derive_verdict` docstring L139 ✓.

## Summary

`derive_verdict` (contract.py L130–246) maps a parsed `return-contract.yaml` to one of four verdicts via a fixed first-match-wins ordering `blocked → degraded → halted → pass`, each carrying a hard-coded exit code (`2/11/10/0`, models.py L44–49). Stage 1 (BLOCKED) reads `child_rc`, the whole contract, `contract_version`, `degraded_components` (list-shape guard), and the seven `_LOAD_BEARING_BOOL_FIELDS` (F2 non-bool guard) — these structurally precede any trust-dependent decision, enforcing M==0 → exit 2. Stage 2 (`_degraded_reason`, L249–304) reads `degraded_components`, `tier_reached`, `t2_model_class_diversity`, `t2_vendor_diversity`, `adversarial_unavailable`, `merge_method`, `adversarial_convergence_score`, `verification_ran` + `verification_skip_reason`, `citations_dropped`, and `input_drift_detected` across 14 ordered triggers. Stage 3 (`_halted_reason`, L307–328) reads `status`, four load-bearing booleans, and `deviation_count_by_class`. Stage 4 (PASS) requires `status == "success"` AND `tier_reached == expected_tier`, else falls through to HALTED `"tier-mismatch"`. All boolean checks use strict `is True`/`is False`; the F0/F2/list-shape fail-closed guards exist specifically to keep a malformed-but-truthy field from leaking past those identity checks into PASS. This is the reflect-side half of the OI-1 field-correspondence contract; the producer-side emission is the outstanding cross-check.

---

*Status: Complete*
