# R3 Research — Consumer Wiring: contract.py + SKILL §5.3 Pre-filter (FR-DRS)

**Status:** Complete
**Date:** 2026-06-22
**Researcher:** R3 (of 8)
**Topic:** Consumer-side additions for FR-DRS (deterministic runtime-surface sweep) — the EXACT, reuse-not-rebuild wiring in `contract.py` + the SKILL §5.3 pre-filter derivation transform.

> Core constraint (from TDD I7 / §14.3): UNREACHED is **NOT a 5th deviation class**. All consumer wiring REUSES existing slugs (`"degraded-components"`, `"regression"`). NO new deviation class, NO new verdict reason for the halt path.

## 0. Verification preamble (re-anchored 2026-06-22)

All line numbers below RE-VERIFIED against the current worktree tree this turn:
- `src/superclaude/cli/reflect/contract.py` — read IN FULL (367 lines). [CODE-VERIFIED]
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — §5.3 region re-grepped + Read. [CODE-VERIFIED]
- TDD: `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md` (FR-006 line 286, §12.5 @883, §14.3/I7 @991, §15.4a @1070-1090, §19.3 Phase 2 @1363-1370). [CODE-VERIFIED]
- `src/superclaude/cli/reflect/runner.py` — `_audit_once` @394, `parse_contract(config.contract_path)` @445. [CODE-VERIFIED]

**KEY GROUND-TRUTH FINDING — contract.py is currently UNWIRED for runtime-surface.**
`grep -n "runtime_surface\|runtime-surface\|surface_unreached\|backend_unavailable" src/superclaude/cli/reflect/contract.py` → **NONE**. [CODE-VERIFIED]
The SKILL.md `surface_unreached` pre-filter (§5.3) already exists (added by the prior FR-RSR rollout); the contract.py consumer triggers and the `surface_unreached` derivation do NOT yet exist. **FR-DRS Phase 2 is the net-new contract.py wiring.** This is exactly why the TDD frames Phase 2 (lines 1363-1370) as the consumer-wiring step.

---

## 1. `_degraded_reason` wiring — REUSE `"degraded-components"` slug

### What exists today (the predicate that already fires) [CODE-VERIFIED]

`contract.py:31-33` — the frozenset (quote, verbatim current contents):

```python
_DEGRADED_COMPONENTS_HALT_SET = frozenset(
    {"serena", "auggie", "env-aliases", "evidence-validator", "serena:context-excluded"}
)
```

`contract.py:258-260` — Trigger-1 inside `_degraded_reason` (def @249):

```python
    # Triggers 1-5: chain-critical degraded_components (exact membership).
    if any(token in _DEGRADED_COMPONENTS_HALT_SET for token in degraded_components):
        return "degraded-components"
```

### The required change (RECOMMENDED path) [CODE-VERIFIED against TDD:1369]

Add the token `"runtime-surface:backend_unavailable"` to `_DEGRADED_COMPONENTS_HALT_SET` (contract.py:31). The sweep appends that exact token to the contract's `degraded_components` list on a degraded edge (FR-010, TDD:291/867/774; SKILL.md:489). Once the token is a member, the EXISTING `any(...)` membership test at `contract.py:259` fires and returns the EXISTING `"degraded-components"` slug. **No new predicate, no new slug, no new trigger.**

Resulting frozenset after the edit (for the builder to write):

```python
_DEGRADED_COMPONENTS_HALT_SET = frozenset(
    {
        "serena",
        "auggie",
        "env-aliases",
        "evidence-validator",
        "serena:context-excluded",
        "runtime-surface:backend_unavailable",
    }
)
```

> Note the membership is EXACT (not substring) by design — see the comment at contract.py:27-30 ("EXACT membership (NOT substring) so benign fail-open tokens ... do NOT over-HALT"). The runtime-surface token must therefore be added literally and exactly.

### Optional alternative (NOT recommended) [CODE-VERIFIED against TDD:1369]

The TDD records an alternative: an independent trigger keyed off the boolean field rather than the token —

```python
    if contract.get("runtime_surface_degraded") is True:
        return "runtime-surface-degraded"
```

The TDD explicitly marks **token-membership reuse as RECOMMENDED** and this independent trigger as the fallback "if `runtime_surface_degraded: true` must surface independently of `degraded_components`." The recommended path "keep[s] it a §10.6 Grounding Gap, not a new degraded class." **Builder: write the token-membership change; record the independent-trigger as a noted alternative only, not an item.**

---

## 2. `_halted_reason` wiring — REUSE `"regression"` slug, NO new branch

### What exists today (the branch that already halts UNREACHED) [CODE-VERIFIED]

`contract.py:307` — `def _halted_reason(contract: dict) -> str | None:`
`contract.py:323-325` — the existing deviation-count branch:

```python
    deviations = _extract_deviations(contract)
    if deviations["regression"] > 0:
        return "regression"
```

(There is also an earlier `regression_present is True → "regression"` at contract.py:315-316; both return the SAME `"regression"` slug.)

### The required change — NONE in `_halted_reason` [CODE-VERIFIED against TDD:1370, §14.3/I7]

Per TDD §14.3 (line 991) and I7: **"UNREACHED is not a 5th deviation class. ... its blocking signal flows through the existing `deviation_count_by_class.regression` / `.drift` counters."** SKILL.md:1063 confirms: "There is no 5th runtime-surface deviation class and no `deviation_count_by_class.runtime_surface` ... counter."

So a confirmed UNREACHED symbol is wired by the SWEEP populating `deviation_count_by_class.regression` from the UNREACHED set (producer-side). The existing `if deviations["regression"] > 0: return "regression"` (contract.py:324-325) then already halts it. **`_halted_reason`'s predicate and slug are UNCHANGED.** The TDD is emphatic (line 1370): "the Phase-2 'consumer trigger' is a producer-side population of an existing counter, not a net-new reason slug."

**Builder item shape:** assert/confirm that `_halted_reason` is NOT modified for UNREACHED; the only "wiring" on the halt path is the producer (sweep/runner) writing `deviation_count_by_class.regression` — which is R1/R2's product-seam territory, NOT a contract.py edit. The contract.py side of the halt path is a NO-OP-by-design that must be PROVEN (a test confirming `deviations["regression"] > 0 → "regression"` still fires for an UNREACHED-sourced count).

---

## 3. Count-invariant malformed-contract guard — mirror the `_LOAD_BEARING_BOOL_FIELDS` fail-closed block

### The pattern to mirror (the fail-closed block) [CODE-VERIFIED]

`contract.py:47-57` — `_LOAD_BEARING_BOOL_FIELDS` frozenset.
`contract.py:200-209` — the fail-closed block inside `derive_verdict` (this is the model to copy):

```python
    # F2 (fail-closed): a PRESENT load-bearing boolean that is not an actual bool
    # is malformed -> BLOCKED before any degraded/halted/pass decision. Absent or
    # None fields flow normally; only present non-bool values block.
    for _field in _LOAD_BEARING_BOOL_FIELDS:
        if _field in contract:
            _value = contract[_field]
            if _value is not None and not isinstance(_value, bool):
                return _make_result(
                    Verdict.BLOCKED,
                    reason="malformed-contract-boolean",
                    contract=contract,
                    child_rc=child_rc,
                )
```

There is a precedent for a SHAPE guard too — the `degraded_components` list-shape check at `contract.py:184-193` returns `malformed-degraded-components`. That is the closer analogue for a malformed-LIST guard.

### The count-invariant guard the builder should mirror [CODE-VERIFIED against §7.4/§12.5; TDD Phase-2 "count-invariant guard" @1342]

The §7.4 / §12.5 invariant is `len(unreached_surfaces) == runtime_surface_unreached`. The producer guarantees it BY CONSTRUCTION; the consumer guard is a defense against a malformed contract where they diverge. Mirror the fail-closed block so a divergent contract routes BLOCKED rather than leaking. Suggested shape (builder to place it alongside the existing F2 block, BEFORE the degraded/halted/pass decision, mirroring `malformed-degraded-components`):

```python
    # F-count (fail-closed): when the sweep ran, the count invariant
    # len(unreached_surfaces) == runtime_surface_unreached MUST hold. A divergent
    # PRESENT pair is a malformed contract -> BLOCKED (mirror of the F2 / the
    # malformed-degraded-components guards). Absent fields flow normally.
    if contract.get("runtime_surface_sweep_ran") is True:
        _unreached = contract.get("unreached_surfaces")
        _count = contract.get("runtime_surface_unreached")
        if (
            isinstance(_unreached, list)
            and isinstance(_count, int)
            and not isinstance(_count, bool)
            and len(_unreached) != _count
        ):
            return _make_result(
                Verdict.BLOCKED,
                reason="malformed-runtime-surface-count",
                contract=contract,
                child_rc=child_rc,
            )
```

> Builder caveat: the new reason slug `"malformed-runtime-surface-count"` is a BLOCKED-class telemetry reason (parallel to `malformed-degraded-components`/`malformed-contract-boolean`), NOT a deviation class — it does not violate I7. It is a malformed-input guard, not a verdict for a well-formed audit. Confirm with R1/R7 whether the guard is desired at the consumer layer at all, since the producer already guarantees the invariant by construction (§7.4); the TDD lists a "count-invariant guard" under Phase 2 (line 1342) which supports adding it. Mark as RECOMMENDED-mirror, defer exact slug naming to builder consensus.

---

## 4. The `surface_unreached` derivation transform (FR-006)

### The transform [CODE-VERIFIED against TDD:286 (FR-006), §15.4a:1070-1090]

The §5.3 pre-filter gates on a DERIVED STRING field `surface_unreached`, **not** on the integer `runtime_surface_unreached` directly. Derivation rule:

- integer `runtime_surface_unreached ≥ 1` from a **successful** sweep → set string `surface_unreached = "runtime_surface_unreached"` (the literal string value, SKILL.md:412).
- integer `0` (fully-REACHED) → `surface_unreached = null`.
- degrade-only run (`runtime_surface_degraded == true`, `unreached == 0`) → `surface_unreached = null` (the degrade path is independent; its Grounding Gap prevents a clean PASS separately).

### Owner [CODE-VERIFIED against TDD:286, §6.3:444, §15.4a:1073]

**RECOMMENDED owner:** the deterministic sweep / reflect CLI wrapper writes `surface_unreached` into `tier_decision`/contract state alongside the six scalars at **`runner._audit_once`** (contract.py:445 is where `parse_contract` reads; the merge-overwrite happens just before, at the FR-005 merge point — the SAME merge point as the six scalars). [CODE-VERIFIED: runner._audit_once @394, parse_contract @445]
**FALLBACK owner:** `derive_verdict` (contract.py:130) is the fallback if the field is consumed there. Per TDD:286 "`derive_verdict` is the fallback owner if the field is consumed there."

Because the §5.3 pre-filter is SKILL-side (LLM-read tier-decision), the practical owner is the runner/sweep wrapper writing `surface_unreached` into the contract/tier_decision state. The contract.py role here is the FALLBACK derivation only. **Builder: the derivation lives at the runner._audit_once merge point (R2's seam); contract.py carries the fallback derivation if `surface_unreached` is consumed in `derive_verdict`.** This item straddles R2/R3 — R3 owns the contract.py fallback half + the §5.3 gate transform; R2 owns the runner merge-point write. Cross-reference R2.

### §15.4a truth table (verbatim) [CODE-VERIFIED, TDD:1075-1080]

| Given (integer scalar from sweep) | Sweep status | Expected `surface_unreached` | Expected §5.3 effect |
|-----------------------------------|--------------|------------------------------|----------------------|
| `runtime_surface_unreached == 0` | successful (REACHED) | `null` | no force; STOP rows may fire |
| `runtime_surface_unreached == 1` | successful (UNREACHED) | `"runtime_surface_unreached"` | force Tier 2 + `status: partial` |
| `runtime_surface_unreached == 2` | successful | `"runtime_surface_unreached"` | force Tier 2 + `status: partial` |
| `runtime_surface_degraded == true`, `unreached == 0` | degrade-only | `null` | NOT forced via this pre-filter (degrade path is independent) |

The §15.4a test asserts (a) the derivation transform in isolation (integer → derived string), then (b) the §5.3 pre-filter reads the derived string — proving producer→derivation→consumer is wired to the deterministic value, never an LLM-typed one (closes the C1 gap).

---

## 5. EXACT current SKILL.md line numbers — §5.3 pre-filter + `surface_unreached`

All re-anchored this turn via grep + Read. [CODE-VERIFIED]
File: `src/superclaude/skills/sc-reflect-protocol/SKILL.md`

| Line | Content (current) |
|------|-------------------|
| **386** | `### 5.3 Decision logic (applied in order; first match wins)` |
| **388-389** | decision table header (`| # | Condition | Decision |`) |
| **390** | Row 1 STOP — conjunct `... AND NOT coverage_degraded AND NOT surface_unreached` |
| **391** | Row 2 STOP — conjunct `... AND NOT coverage_degraded AND NOT surface_unreached` |
| **398** | Row 8 `Default | STOP at T1` |
| **402** | **Pre-filter precedence (D13)** paragraph — table-wide `surface_unreached` pre-filter: "when ... `surface_unreached` is set from a SUCCESSFUL runtime-surface sweep with `runtime_surface_unreached ≥ 1`, NO STOP row ... may fire and the run routes to Tier 2"; pinned-run forces `status: partial`; degrade-only (`runtime_surface_unreached == 0`) does NOT force T2 |
| **412** | `surface_unreached: <string> | null` in the `tier_decision.yaml` block — literal value `"runtime_surface_unreached"` documented |

Cross-check (NOT R3's to edit, but co-located): the six `runtime_surface_*` contract fields are documented at SKILL.md:721-735; mandatory-emission rule SKILL.md:491; sweep step 4b SKILL.md:489; §9.3 UC-2 advisory consumer rows SKILL.md:890; count invariant SKILL.md:730; "no 5th deviation class" SKILL.md:1063.

> The TDD's FR-006 citation "SKILL.md:390-391 ... 402 ... 412" MATCHES the current tree exactly — no drift. The §5.3 pre-filter is ALREADY in SKILL.md. R3's SKILL responsibility (§5.3) is therefore **verify-and-leave** (the transform feeding it is the new work), NOT an edit to §5.3 text. (§6.1/§9.1 demotion edits belong to R6.)

---

## 6. Summary for the builder (reuse-not-rebuild manifest)

| # | Surface | File:line | Change | Slug | New class? |
|---|---------|-----------|--------|------|-----------|
| 1 | `_DEGRADED_COMPONENTS_HALT_SET` | contract.py:31-33 | ADD token `"runtime-surface:backend_unavailable"` | REUSE `"degraded-components"` (fires @259-260) | NO |
| 2 | `_halted_reason` UNREACHED | contract.py:307/324-325 | **NO EDIT** — producer populates `deviation_count_by_class.regression`; existing branch halts | REUSE `"regression"` | NO (I7) |
| 3 | count-invariant guard | contract.py (new block ~after 209) | MIRROR F2 fail-closed block for `len(unreached_surfaces)==runtime_surface_unreached` | new BLOCKED telemetry reason e.g. `"malformed-runtime-surface-count"` (malformed-input, not a verdict class) | NO |
| 4 | `surface_unreached` derivation | runner._audit_once @394/merge-before-445 (RECOMMENDED); `derive_verdict` @130 (FALLBACK) | integer `≥1` from successful sweep → `"runtime_surface_unreached"`; else null | new DERIVED field, not a deviation class | NO |
| 5 | §5.3 pre-filter | SKILL.md:390-391/402/412 | **verify-and-leave** (already present) | n/a | NO |

**The I7 invariant holds across all five:** no `deviation_count_by_class.runtime_surface` key, no 5th deviation class, no new HALT reason slug. The two consumer triggers REUSE `"degraded-components"` and `"regression"`. The only genuinely-new strings are (a) the membership token (data, not a class), (b) an optional malformed-input BLOCKED reason, and (c) the derived `surface_unreached` string field the §5.3 pre-filter already expects.

**Boundary notes for the builder (avoid R-overlap):**
- Producer-side population of `deviation_count_by_class.regression` from the UNREACHED set = R1 (module) / R2 (runner merge). R3 owns only the contract.py CONSUMER assertion that the existing branch still fires.
- The runner._audit_once merge-overwrite of the six scalars + the recommended-owner `surface_unreached` write = R2's seam. R3 owns the contract.py FALLBACK derivation + the §5.3 gate transform semantics.
- §6.1/§9.1 demotion = R6 (NOT R3). R3's SKILL scope is §5.3 only, which is verify-and-leave.

## Status: Complete

Delivered the exact, reuse-not-rebuild consumer wiring: (1) add `"runtime-surface:backend_unavailable"` to `_DEGRADED_COMPONENTS_HALT_SET` (contract.py:31) reusing the existing `"degraded-components"` slug via the @259-260 membership test; (2) `_halted_reason` UNREACHED is NO-EDIT — producer populates `deviation_count_by_class.regression`, the existing @324-325 branch reuses `"regression"` (I7: no 5th class); (3) mirror the @200-209 fail-closed block for the `len(unreached_surfaces)==runtime_surface_unreached` count invariant; (4) `surface_unreached` derivation (integer ≥1 → `"runtime_surface_unreached"`, owner = runner._audit_once merge point, fallback = derive_verdict) with the §15.4a truth table; (5) §5.3 SKILL.md lines re-anchored (390-391/402/412 — present, verify-and-leave). KEY: contract.py currently has ZERO runtime-surface wiring (grep-confirmed), so Phase 2 is net-new but slug-reusing.
