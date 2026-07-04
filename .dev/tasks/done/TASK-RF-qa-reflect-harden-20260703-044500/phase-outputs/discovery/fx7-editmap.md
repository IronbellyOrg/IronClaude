# FX7 Edit-Map (Step 3.1)

Worktree HEAD 46a787da. All anchors verified against current source.

## CRITICAL DISCOVERY — two code-contradicted brief premises (resolution below)

The brief (Step 3.2 / Objective 3 / Step 3.4c) asserts that populating `degraded_components` on a
`reviewer_count < reviewers_requested` shortfall makes the shortfall case "honestly degrade WITHOUT a
consumer edit," citing `contract.py:259-260` as "already a trigger." Reading the actual code contradicts
this in TWO ways:

1. **The `degraded_components` trigger is HALT_SET-gated.** `contract.py:259` is
   `if any(token in _DEGRADED_COMPONENTS_HALT_SET for token in degraded_components)`. Only tokens in
   `_DEGRADED_COMPONENTS_HALT_SET = {"serena","auggie","env-aliases","evidence-validator","serena:context-excluded"}`
   (contract.py:31-33) degrade. A bare `"reviewer-shortfall"` token is BENIGN and does NOT degrade —
   proven by `test_benign_degraded_component_does_not_over_halt` (test_verdict_mapping.py:190-201). So
   "populated list degrades without a consumer edit" is FALSE.

2. **Degrading a shortfall REVERSES the deliberate FR-RH2.9 design.** `test_i3_partial_two_of_three_distinct_pass_eligible`
   (test_ensemble_stub_integration.py:199-221) asserts a 2-of-3 reviewer outcome (reviewer_count=2, a genuine
   shortfall vs requested 3) routes **PASS / exit 0** (mn_guard_table: "M>=2 AND >=2 distinct classes →
   pass-eligible"). The M-space is fully partitioned: M>=2 → pass-eligible (FR-RH2.9); M<2 → already degrades
   via `single-reviewer-fallback` (Trigger 10). So "reviewer_count < reviewers_requested → degrade" has NO
   additive room — it necessarily degrades M∈[2, requested-1], which FR-RH2.9 deliberately treats as
   pass-eligible, regressing test_i3. This is NON-ADDITIVE and reverses a tested design — exactly parallel
   to how "degrade-on-any-unverified" reverses R2-F2 (which the brief already routes to needs_human_decision).

### RESOLUTION (code-honest, additive; mirrors the brief's own R2-F2 deferral)
Ship the **visible accounting** additively; **DEFER the verdict-DEGRADE-on-shortfall** to a
`needs_human_decision` PENDING (NOT auto-applied), because it reverses FR-RH2.9/test_i3.
- Populate `degraded_components` with `"reviewer-shortfall"` on genuine shortfall as a VISIBLE/benign token
  (NOT added to `_DEGRADED_COMPONENTS_HALT_SET`) → the shortfall becomes visible in the already-surfaced
  list + `reviewers_verified: false`, WITHOUT flipping any verdict (test_i3 stays PASS; test_benign confirms
  benign tokens don't degrade).
- Add the `*_verified` visibility fields (the primary honest-accounting surface).
- Two PENDING markers (both deferred verdict-flips): `fx7-degrade-on-unverified-DECISION.md` (verification
  degrade, per brief) and `fx7-degrade-on-reviewer-shortfall-DECISION.md` (shortfall degrade, discovered —
  reverses FR-RH2.9).
- Step 3.4c adapted: instead of a "shortfall → DEGRADED" test (which would encode the deferred routing and
  contradict test_i3), author an additive-safety WITNESS test — a populated benign `reviewer-shortfall`
  token does NOT over-degrade a 2-of-3-style contract (stays PASS-eligible, preserving FR-RH2.9), mirroring
  `test_benign_degraded_component_does_not_over_halt`.

## Planned additive edits

> NOTE (Gate-B F-B2 reconciliation): the file:line anchors below are the PRE-EDIT (as-planned) line
> numbers from the ORIGINAL source read at Step 3.1. The edits ADDED lines, so post-edit anchors shifted
> (e.g. builder signature L502→:509, verification block L550-551→:571-572, degraded_components L560→:588).
> The authoritative POST-EDIT anchors are recorded in the Gate-B lens reports (`qa/qa-gateB-*.md`). This is
> a plan doc; the drift is cosmetic and does not affect any code.

### ensemble.py — `build_reflect_contract` (L492-568) + `run_tier2_ensemble` call site (L302)
- Add kwarg `reviewers_requested: int | None = None` (defaulted → additive for direct/test calls).
- Thread from `run_tier2_ensemble`: `reviewers = int(config.reviewers)` (L191) → pass `reviewers_requested=reviewers`
  into the builder call (L302-327).
- `reviewer_count = len(succeeded)` (L517) already computed.
- On `reviewers_requested is not None and reviewer_count < reviewers_requested`: append `"reviewer-shortfall"`
  to the `degraded_components` list (currently `[]` at L560) — VISIBLE/benign (NOT a HALT_SET token).
- Add NEW keys to the emitted dict: `verification_verified: False`, `reviewers_verified: <None-guarded>`
  (`True if reviewers_requested is None else reviewer_count >= reviewers_requested`), `regression_verified: False`.
- KEEP `verification_skip_reason: "tool-unavailable"` (L551) BYTE-UNCHANGED. KEEP `status: "success"` (L538).

### models.py — `ReflectResult` (L117-152)
- Append defaulted: `verification_verified: bool = False`, `reviewers_verified: bool = False`,
  `regression_verified: bool = False` (after `reviewer_grounding_root` L152). Keeps all 5 hand-built sites valid.

### contract.py — `_make_result` (L104-127)
- Defensively populate the 3 new `ReflectResult` fields via `c.get("...", False)`. Additive; no existing mapping changed.
- DO NOT touch `_VERIFICATION_SKIP_EXEMPTIONS` (L36-38) or `_DEGRADED_COMPONENTS_HALT_SET` (L31-33).

### runner.py — `_build_reflect_post_value` (L93-117) + `write_sidecar` (L191-244)
- Append the 3 `*_verified` keys at the END of both mappings (test_writeback asserts keys PRESENT, not exact).
- `--skip-if-pass` / resume gate (`_read_existing_reflect_post` L298; resume short-circuit L585-591):
  Step 3.3c OPTIONAL hardening — evaluate at 3.3c whether requiring `verification_verified is True` breaks a
  resume test; if risk, skip (stay maximally additive).

## Tests (3.4)
- 3.4a fixtures: `degraded_reviewer_shortfall.yaml`, `vacuous_no_verify.yaml` (mirror existing `degraded_*.yaml`).
- 3.4b (test_ensemble_unit.py): shortfall populates `degraded_components` token + `reviewers_verified is False`;
  `*_verified` fields present; clean/full-reviewer (or kwarg-omitted) run → `degraded_components == []` +
  `verification_skip_reason == "tool-unavailable"`. `test_r2f2` + `test_i1` require NO edit.
- 3.4c (test_verdict_mapping.py): ADAPTED additive-safety witness — a benign `reviewer-shortfall` token does
  NOT over-degrade (stays PASS-eligible, FR-RH2.9 preserved); MUST NOT break `test_verification_skip_exemption_not_degraded`.
- 3.4d (test_writeback.py): the 3 `*_verified` keys appear in the written `reflect_post` block.

## DO-NOT (hard prohibitions — verified honored)
- `_VERIFICATION_SKIP_EXEMPTIONS` (contract.py:36-38) — BYTE-UNCHANGED.
- `_DEGRADED_COMPONENTS_HALT_SET` (contract.py:31-33) — BYTE-UNCHANGED (the deferred degrade would edit this; it is NOT shipped).
- `status: "degraded"` — NOT set (misroutes to tier-mismatch HALTED/exit-10).
- `regression:unknown` inside int-typed `deviation_count_by_class.regression` — NOT written; use the separate `regression_verified` bool.
- Clean-run `verification_skip_reason` — NOT flipped (stays exempt `"tool-unavailable"`).
