# QA Report — task-qualitative (consolidated-fix lens)

**Topic:** FR-RH2 headless ensemble (sc:reflect Tier-2 via swarm dispatch)
**Date:** 2026-06-20
**Phase:** task-qualitative
**Lens:** consolidated-fix (single serialized fix agent, MDTM I20)
**Fix cycle:** 1
**fix_authorization:** true
**Task file:** `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`
**Source verification commit:** HEAD `63f1a81` (matches task `start_commit` `63f1a8153d...`)

---

## Overall Verdict: PASS

All three findings from the operational report (1 CRITICAL, 2 MINOR) are remediated in-place.
The sufficiency report PASSED and contributed no fixes. Every fix mechanism was verified
constructible against shipped source before application.

---

## Findings dispatched (from qa-qualitative-operational-report.md)

| # | Severity | Axis | Location | Status |
|---|----------|------|----------|--------|
| 1 | CRITICAL | AX-2 (contradictions) | Step 3.1 + Step 6.1 (I1) + Step 6.3 (I3) + Step 6.4 (I4) | FIXED |
| 2 | MINOR | AX-1 (drift) | Step 6.7 (I7) — pass.yaml descriptor | FIXED |
| 3 | MINOR | AX-1 (anchor drift) | Step 0.2 — BLOCKED-slug anchors | FIXED |

---

## Source verification performed BEFORE applying fixes (zero-trust)

| Claim | Tool evidence | Result |
|-------|---------------|--------|
| `_resolve_run_transport_factory("stub")` returns ONE shared stub for all slots | `commands.py:670-673` = `if transport_kind == "stub": # Single shared stub for every slot … return lambda _slot: shared` | CONFIRMED |
| `openai_compat` path is per-slot distinct (`pool[i % len(pool)]`) | `commands.py:674-700` factory builds per-model transports from env pool | CONFIRMED |
| `StubTransport(model_id=...)` takes a per-instance model_id (default present) | `stub.py:93-99` `__init__(self, model_id: str = _DEFAULT_MODEL_ID, *, …)`; `self._model_id = model_id`; non-empty guard | CONFIRMED |
| Distinct `model_id` → distinct per-slot identity/output | `tests/swarm/test_stub_transport.py:72-75` `test_default_mode_distinct_models_yield_distinct_bodies` asserts `body_a != body_b` for model-A vs model-B | CONFIRMED |
| Trigger 7 fires `degraded-model-diversity` when mcd != "full" | `contract.py:267-269` `mcd = contract.get("t2_model_class_diversity"); if mcd is not None and mcd != "full": return "degraded-model-diversity"` | CONFIRMED |
| pass.yaml top-level key count | `grep -cE '^[a-z_]+:' tests/cli/reflect/fixtures/pass.yaml` = **21** (NOT 23) | CONFIRMED — descriptor was wrong |
| pass.yaml `contract_version` value | `pass.yaml:1` = `contract_version: "1.3.0"` (major-1) | CONFIRMED |
| ensemble.py emits major-1 contract_version | Step 3.1 instructs literal `"1.0"` (major-1); `contract.py:174-176` checks only `major != "1"` | CONFIRMED — both major-1, exact-string match would false-fail |
| BLOCKED-slug return anchors | `contract.py:161` = `reason = "child-crash" if child_rc != 0 else "contract-missing"`; `contract.py:162` = `return _make_result(Verdict.BLOCKED, reason=reason, …)` | CONFIRMED — slug return resolves at the 156-162 span, not a single line |

---

## FIXES APPLIED

### FIX 1 — CRITICAL (AX-2: the stub-diversity contradiction) — 4 edits

The CRITICAL contradiction was that the I1/I3 positive-diversity witnesses assert
`t2_model_class_diversity == "full"` (needs ≥2 distinct succeeded `model_id`s), but the swarm
factory's stub branch (`commands.py:670-673`) returns ONE shared `StubTransport` for every slot,
collapsing all slots to one `model_id` ⇒ 1 distinct class ⇒ trigger 7 always fires
`degraded-model-diversity`. I1 was therefore UNSATISFIABLE through the mandated seam, and
I1 (distinct) vs I4 (same-class) required OPPOSITE, unspecified stub configurations.

**(a) Step 3.1** — Added a **STUB-PATH DESIGN NOTE** mandating that under `--transport stub`,
`ensemble.py` builds its OWN per-slot transport binding yielding DISTINCT `model_id`s
(`transport_for_slot = lambda i: StubTransport(model_id=f"stub-model-{i:02d}")`), and MUST NOT route
through the factory's single-shared-stub branch (`commands.py:670-673`). The `openai_compat` path
still uses the swarm factory (per-slot distinct `T2Model0N`). Cites `commands.py:670-673`
(branch to bypass) + `stub.py:93-99` (per-instance model_id) + `test_stub_transport.py:72-75`
(precedent). Explicitly states this is the mechanism that makes I1/I3 satisfiable and I4
constructible (opposite config).

**(b) Step 6.1 (I1)** — Specified the test injects a per-slot DISTINCT-model stub binding
(≥2 distinct `model_id`s) so the real `dispatch_wave1→reduce_wave3→derive_verdict` path yields
≥2 distinct classes and `t2_model_class_diversity == "full"` is GENUINELY satisfiable — NOT via the
shared-stub factory branch. All 4 canonical assertions retained.

**(c) Step 6.3 (I3)** — Specified the 2 M==2 survivors are bound to 2 DISTINCT `model_id`s
(same per-slot distinct-model binding), so the PASS-eligible `t2_model_class_diversity == "full"`
assertion holds.

**(d) Step 6.4 (I4)** — Specified the 2 M==2 survivors share the SAME `model_id`
(`StubTransport(model_id="stub-model-dup")`) — explicitly called out as the DELIBERATE OPPOSITE stub
configuration from I1/I3 — so `t2_model_class_diversity != "full"` and the run routes
`degraded-model-diversity` / exit 11.

I1↔I4 now use explicitly opposite stub `model_id` configurations, both stated with no executor
ambiguity.

### FIX 2 — MINOR (AX-1 drift) — Step 6.7 (I7)

- Corrected the descriptor `23-key shape` → `21-key (21 top-level keys) shape` (verified
  `grep -cE '^[a-z_]+:' = 21`).
- Softened the `contract_version` assertion: I7 now asserts **MAJOR version == 1** (MAJOR-1
  compatibility — fixture emits `"1.3.0"`, ensemble.py emits a major-1 value such as `"1.0"`; both
  pass `contract.py:174-176`), explicitly NOT an exact-string match of `"1.3.0"`/`"1.0"`. This
  prevents a false-failure if the I7 author wired an exact equality.

### FIX 3 — MINOR (AX-1 anchor drift) — Step 0.2

- Adjusted the BLOCKED-slug anchors that pointed at single non-return lines to span form:
  `contract-missing at contract.py:161` → `contract.py:156-162` (the check at 161 + return at 162);
  `child-crash at 156/158` → `156-162` (check/return span). The remaining slug anchors
  (contract-version-missing 167/170, unknown-major-version 175/176, malformed-degraded-components
  187/190, malformed-contract-boolean 203/206) were verified EXACT and left unchanged.

---

## Verification of applied fixes

| Check | Method | Result |
|-------|--------|--------|
| Frontmatter still parses | `yaml.safe_load` of frontmatter block → 35 keys, id intact | PASS |
| No `23-key` remains | `grep -c "23-key"` = 0 | PASS |
| `21-key (21 top-level keys)` present | `grep -c` = 1 | PASS |
| STUB-PATH DESIGN NOTE in Step 3.1 + referenced by I1/I3 | `grep -c "STUB-PATH DESIGN NOTE"` = 3 (1 def + 2 back-refs) | PASS |
| I1 per-slot DISTINCT-model binding | `grep -c "per-slot DISTINCT-model stub binding"` = 1 | PASS |
| I4 same-model (`stub-model-dup`) | `grep -c "stub-model-dup"` = 1 | PASS |
| I4 explicitly opposite I1/I3 | `grep -c "DELIBERATE OPPOSITE stub configuration from I1/I3"` = 1 | PASS |
| I7 major-1 assertion | `grep -c "assert MAJOR version == 1"` = 1 | PASS |
| Item count unchanged | `grep -cE '^- \[ \]'` = 52 (no items added/removed) | PASS |
| No broken cross-references | back-refs point to "Step 3.1 STUB-PATH DESIGN NOTE" which exists | PASS |

---

## Self-Audit (Inherited Structural Verdict — Reliance Audit, PR-04 / INV-019)

**(a) Reliance list — structural/operational PASS items relied on (not re-checked):**
- Relied on the operational report's 17 PASS items (swarm signatures, FR-6 demotion anchor,
  no-nesting guard extension premise, adversarial-seam NFR-7 legality, OI-1 field-absence,
  diversity-derivation downstream enforcement, --reviewers/--transport plumbing) — these were
  machine-verified by the operational QA pass and were not re-litigated.
- Relied on the sufficiency report PASS — no sufficiency-class fixes applied.

**(b) Independent semantic checks where my own tool work was required (≥1, INV-019):**
- **Re-verified the FIX 1 mechanism is constructible** by independently reading `stub.py:93-99`
  (per-instance `model_id` constructor) + `test_stub_transport.py:72-75` (distinct-model precedent)
  + `commands.py:670-700` (shared-stub branch vs openai_compat per-slot branch) + `contract.py:267-269`
  (trigger 7) — confirming the design note I wrote names a real, buildable seam (not an invented one)
  before mandating it. A fix that prescribed an unconstructible mechanism would itself be a defect.
- **Re-verified the FIX 2 numbers** by `grep -cE '^[a-z_]+:' pass.yaml` = 21 and reading
  `pass.yaml:1` = `"1.3.0"` and `contract.py:174-176` (major-only check) — confirming "21-key" is
  correct and the major-1 softening is the right call (exact-string would false-fail).
- **Re-verified the FIX 3 span** by reading `contract.py:156-162` directly — confirming the slug
  return resolves at 162 with the check at 161, so the span form is accurate.

---

## Summary
- Findings dispatched: 3 (1 CRITICAL, 2 MINOR)
- Issues fixed in-place: 3 / 3
- Issues remaining: 0
- New issues introduced by fixes: 0 (item count unchanged; frontmatter parses; no broken refs)
- Axis lens status: AX-1 drift ACTIVE (GOAL baseline R-001 present in task file); AX-2 fired on FIX 1.

## Confidence
Verified: 3/3 findings remediated and re-verified | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 2 (operational report, task file body) | Grep/Bash: 4 (source verification + post-fix
verification) | Edit: 6 (FIX1 ×4, FIX2 ×1, FIX3 ×1) | Glob: 0
(All source claims verified against shipped source at `63f1a81` before fixing; all fixes verified
post-application.)

## Web research
None performed — all verification was local-file-bound against shipped source. Tavily not needed.

---

## VERDICT: PASS

All three operational-report findings are remediated in-place and re-verified. The load-bearing
CRITICAL contradiction (FIX 1) is resolved: the stub path now has an explicit per-slot
distinct-`model_id` mechanism (Step 3.1 design note) that makes the I1/I3 positive-diversity
witnesses satisfiable, with I4 carrying the deliberate opposite same-`model_id` config — no executor
ambiguity remains. The two MINOR drift findings (I7 "21-key" + major-1 contract_version; Step 0.2
span anchors) are corrected. Frontmatter parses, item count is unchanged (52), and no
cross-references were broken.

## QA Complete
