# QA Report — task-qualitative (operational-correctness lens)

**Topic:** FR-RH2 headless ensemble (sc:reflect Tier-2 via swarm dispatch)
**Date:** 2026-06-20
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A (fix_authorization: false)

---

## Overall Verdict: FAIL

One CRITICAL operational contradiction (the stub-transport single-model seam vs. the I1
diversity positive-witness), plus IMPORTANT and MINOR drift findings. Detail below.

**Drift baseline:** BUILD_REQUEST.GOAL captured verbatim from task R-001 (line 104):
"Build an MDTM task file that implements FR-RH2 — re-route the headless `sc:reflect` Tier-2
reviewer ensemble through the swarm dispatch library — covering ALL of FR-RH2.1..FR-RH2.9 and
NFR-RH2.1..NFR-RH2.8, in the spec §4.6 dependency-respecting order, with three BLOCKING gates
resolved before any FR-RH2.3 code lands." AX-1 drift axis ACTIVE.

---

## Items Reviewed
| # | Check (lens question) | axis | Result | Evidence |
|---|------------------------|------|--------|----------|
| 1 | runner.py FR-6 demotion anchor (588-590) | none | PASS | runner.py:588-590 = `if write_status != "written" and result.verdict is Verdict.PASS: result.verdict = Verdict.BLOCKED`. Exact. |
| 2 | runner.py `_audit_once` 392-428, single ClaudeProcess + parse/derive tail 420-428 | none | PASS | `_audit_once` at 392; ClaudeProcess at 405; `parse_contract`+`derive_verdict` at 420-428. Exact. |
| 3 | dispatch_wave1 sig (dispatch.py:334, kw-only transport_for_slot) | none | PASS | def at 334; `*,` then `transport_for_slot`. Reads `preflight_result.manifest.preflight.workers_requested` at 412. Exact. |
| 4 | _resolve_run_transport_factory sig (commands.py:612, private, workers_requested kwarg) | none | PASS | def at 612, kw-only `workers_requested`, pool guard `ModelPoolTooSmallError` at 687-688, slot `pool[i % len(pool)]` at 692. Exact. |
| 5 | reduce_wave3 (reduce.py:555) + done.json via emit_done_sentinel (402) NOT reduce_wave3 | none | PASS | reduce_wave3 def at 555; `emit_done_sentinel` def at 402. Disambiguation correct. |
| 6 | ModelPoolTooSmallError precedent test_model_pool_guard.py:40-47 (NOT test_inv005) | none | PASS | `test_factory_raises_when_pool_smaller_than_workers` at 40-47 asserts `pool_size`/`workers_requested`. test_inv005_pool_guard.py EXISTS but is a different (placeholder) guard — disambiguation correct. |
| 7 | StubTransport injection seam vs conftest mock-gap | AX-2 | FAIL | See FINDING 1 (CRITICAL). conftest mock-gap at 98-138 confirmed; mandated `_resolve_run_transport_factory("stub")` path returns a SINGLE shared model → I1 diversity unsatisfiable. |
| 8 | swarm precedent test_commands_run.py:507-568 mirror-shape | none | PASS | `test_run_cmd_stub_transport_dispatches_workers_not_noop` at 507; `results=3` ~551; `worker_done`==3 at 566-568. CLI-level injection — mirror-shape exists but differs from "real driver" seam (see FINDING 1). |
| 9 | adversarial seam: /sc:adversarial is SKILL, 2nd top-level ClaudeProcess NFR-7-legal | none | PASS | Guard bans `Task(`/`subagent`/`anthropic`, asserts `ClaudeProcess` presence (test_no_nesting_guard.py:95-102). validate_executor.py:365-373 build_merge_prompt precedent confirmed. 2nd top-level ClaudeProcess legal. |
| 10 | no-nesting guard agent-surface check is _RUNNER_SRC-only today (_ENSEMBLE_SRC needed) | none | PASS | Check #2 at 95-102 reads `_RUNNER_SRC` ONLY (line 22). `_REFLECT_PY` glob (24) covers ensemble.py for sprint/roadmap+async bans only. Extension premise correct. |
| 11 | verification commands/test paths exist and run | none | PASS | merge LOC + mechanical-only + model-pool + commands-run + conftest + no-nesting test files all present; merge.py mechanical_merge 50-57 (8 LOC), DISALLOWED 18-26 confirmed. |
| 12 | OI-1 6 verdict fields absent from swarm ResultContract, only `status` shared | none | PASS | grep swarm/models.py for tier_reached/merge_method/t2_*_diversity/reviewer_count/adversarial_convergence_score = NONE. `status` present both sides, different semantics. Claim exact. |
| 13 | config.py resolve_config kwarg shape for --transport/--reviewers plumbing | none | PASS | resolve_config def at 123, kw-only args; depth floor `quick→standard` ~190; `_DEFAULT_MAX_TURNS=250` at 39. New fields plumb after max_fix_iterations (models.py:86). |
| 14 | --reviewers 1 pre-clamp degrade reaches single-reviewer-fallback path | none | PASS | contract.py trigger 10 `merge_method=="single-reviewer-fallback"` at 280; trigger 6 `expected_tier>=2 and tier_reached==1 → degraded-tier1` at 263. M==1 reaches degraded/exit11. Q8 design sound. |
| 15 | LensEntry DM-010 14-field shape (models.py:707-720) | none | PASS | class at 637; 14 fields name..stability at absolute 707-720. Exact. |
| 16 | derive_verdict ordering blocked→degraded→halted→pass (U6 claim) | none | PASS | contract.py:12,139 ordering first-match-wins. Triggers 7-11 numbering matches task. PASS gate 235. Exact. |
| 17 | I7 pass.yaml fixture key-count + field anchors | AX-1 | FAIL | See FINDING 2 (MINOR). tier_reached:2 L4, diversity:full L12, merge_method:adversarial L15, score:0.86 L16 EXACT; but fixture has 21 top-level keys, not "23-key shape"; contract_version is "1.3.0" not "1.0". |
| 18 | ensemble.py contract_version "1.0" vs contract.py major-version gate | none | PASS | contract.py:174-176 checks `major != "1"` only; "1.0" passes. No contradiction with pass.yaml's "1.3.0". |
| 19 | NFR-RH2.8 no forbidden literal in openai_compat executable code | none | PASS | `/v1` only in docstrings (17,217,219); `_CHAT_COMPLETIONS_PATH="/chat/completions"` at 122; base from T2ProxyUrl; no :4000/:8317/bare /cli. U9 exact. |
| 20 | WorkerResult DM-013 model_id/final_path/status anchors | none | PASS | model_id at 1122, final_path 1121, status:WorkerStatus 1125, WorkerStatus Literal 69, 12 fields 1117-1128. Exact. |

---

## Findings

### FINDING 1 — CRITICAL — `axis: AX-2 (contradictions)`
**Location:** Step 3.1 item (2) + Step 6.1 (I1 positive witness) + Step 6.3 (I3) — the stub-transport
seam vs. the diversity-over-distinct-`model_id`s rule.

**The contradiction.** Step 3.1 mandates ensemble.py call
`_resolve_run_transport_factory(..., workers_requested=reviewers)` to obtain the per-slot factory.
For `--transport stub`, that factory's stub branch is (commands.py:670-673):
```python
if transport_kind == "stub":
    # Single shared stub for every slot (single-model behaviour preserved).
    shared = _resolve_run_transport("stub", models=models, env=env)
    return lambda _slot: shared
```
It returns ONE shared `StubTransport` for every slot. `StubTransport.send` (stub.py:122-159)
stamps `model_id=self._model_id` — a single per-instance id — on every `WorkerResult`. The
`_resolve_run_transport` docstring is explicit: "This builds a SINGLE transport bound to the first
configured model … stub differentiation adds no value."

Step 3.3 (contract.py diversity-source) + U5 + FR-RH2.4 require
`t2_model_class_diversity == "full"` to be computed over the **distinct `model_id`s of the M
succeeded workers**. With a single shared stub, all M succeeded workers carry the SAME `model_id`
⇒ 1 distinct class ⇒ contract.py trigger 7 (`mcd != "full"`, contract.py:267-269) fires ⇒
`degraded-model-diversity` / exit 11 — NOT the PASS-eligible Tier-2 that I1 asserts.

**Why this is CRITICAL (will-it-run):** Step 6.1 (I1) asserts, on the REAL
`dispatch_wave1→reduce_wave3→derive_verdict` path driven by `--transport stub --reviewers 3`:
`tier_reached == 2`, `merge_method != "single-reviewer-fallback"`, `reviewer_count >= 2`,
**`t2_model_class_diversity == "full"`**. The last assertion is **unsatisfiable** through the exact
seam Step 3.1 wires (`_resolve_run_transport_factory("stub")`), because that factory cannot produce
≥2 distinct `model_id`s. I1 is the LOAD-BEARING non-mocked proof of the whole feature; if it cannot
go green via the mandated path, the executor will either (a) fail I1, or (b) silently bypass
`_resolve_run_transport_factory` and inject a hand-built per-slot distinct-`model_id` stub factory —
which is a DIFFERENT mechanism than Step 3.1 specifies and than "drive the REAL reflect Tier-2
driver with `--transport stub`" implies. Step 6.3 (I3, "2 survivors resolving to 2 DISTINCT model
classes") has the same defect.

**Evidence the gap is real but unresolved in the task:** `StubTransport.__init__` DOES accept a
per-instance `model_id`, and `dispatch_wave1` accepts a custom `transport_for_slot`. Existing
`tests/swarm/test_stub_transport.py:74-75` proves `StubTransport(model_id="model-A")` vs `"model-B"`
yield distinct ids. So a per-slot distinct-stub factory is constructible — but ONLY by bypassing
`_resolve_run_transport_factory`'s stub branch. The task NOWHERE specifies how ensemble.py (or the
I1 test) obtains per-slot distinct `model_id`s under `--transport stub` while still routing through
the factory Step 3.1 mandates. This is an unresolved operational seam at the exact point the proof
is load-bearing.

**Required fix (report-only — fix_authorization:false):** Add an explicit item/sub-step resolving
HOW the stub path yields ≥2 distinct succeeded `model_id`s, one of:
  (a) ensemble.py builds its OWN per-slot stub factory (binding `StubTransport(model_id=f"stub-{i}")`
      or `T2Model0N`-named stubs per slot) instead of calling
      `_resolve_run_transport_factory("stub")` — and Step 3.1 item (2) is amended to say the stub
      transport path does NOT delegate to the swarm factory's single-shared-stub branch; OR
  (b) the I1 test injects a custom `transport_for_slot` with distinct-`model_id` stubs at the
      `dispatch_wave1` seam and the diversity is computed from those — with Step 6.1 stating this
      explicitly; OR
  (c) extend `_resolve_run_transport_factory`'s stub branch (swarm-side) to bind distinct
      per-slot stub `model_id`s when a pool/`reviewers` count is supplied (mirrors the
      openai_compat branch), with a swarm-side item added.
Whichever is chosen, I4 (Step 6.4, "M==2 survivors resolve to the SAME model class") must remain
constructible — under option (a)/(b) it requires deliberately binding two slots to the same
`model_id`, which the current single-shared-stub naturally gives but a distinct-per-slot factory
does not, so I4 also needs an explicit same-`model_id` construction note. The task currently treats
"distinct classes" (I1/I3) and "same class" (I4) as both achievable under one unspecified stub
mechanism; they require OPPOSITE stub configurations and neither is specified.

### FINDING 2 — MINOR — `axis: AX-1 (drift)`
**Location:** Step 6.7 (I7) Context — the `pass.yaml` fixture descriptor.

**The drift.** Step 6.7 describes the fixture as "`tests/cli/reflect/fixtures/pass.yaml` —
`tier_reached:2` at L4; **23-key shape** with `t2_model_class_diversity:full` at L12,
`merge_method:adversarial` at L15, `adversarial_convergence_score:0.86` at L16." The four
line-anchors are EXACT against shipped source (verified: L4, L12, L15, L16). But:
- The fixture has **21 top-level keys** (`grep -cE '^[a-z_]+:' = 21`), not 23. (27 lines match if you
  count the nested `deviation_count_by_class` children, but those are not top-level keys.) The
  "23-key shape" magnitude is inaccurate.
- `contract_version` in the fixture is **"1.3.0"** (L1), whereas Step 3.1 instructs ensemble.py to
  emit literal `contract_version "1.0"`. Both are major-1 so both pass contract.py:174-176 — there
  is no functional contradiction (see Items Reviewed #18), but the I7 descriptor implies the
  emitted contract should match the fixture's field set, and the version literals differ. A reader
  wiring I7 to assert exact equality of `contract_version` would get a false failure.

**Impact:** LOW — I7 asserts shape/field-set preservation, not a literal 23-count, and the
version mismatch is benign at the gate. But the descriptor's "23-key" and the implied
version-equality could mislead the I7 author into an over-strict assertion. Recommend correcting
"23-key" → "21 top-level keys" and noting that `contract_version` differs by patch/minor (both
major-1) so I7 must assert major-1, not literal `"1.3.0"`/`"1.0"` equality.

---

## Spawn-prompt lens questions — disposition
1. file:line anchors match shipped source — VERIFIED. The named corrections are all EXACT:
   FR-6 demotion runner.py:588-590 ✓; ModelPoolTooSmallError precedent test_model_pool_guard.py:40-47 ✓;
   done.json emit_done_sentinel reduce.py:402 (NOT reduce_wave3) ✓. Minor ±1 anchor drift on
   BLOCKED slugs (FINDING 3) and a "23-key"/version descriptor (FINDING 2).
2. swarm signatures ensemble.py must reproduce (dispatch_wave1 334, _resolve_run_transport_factory 612,
   reduce_wave3 555) — all VERIFIED correct against source.
3. no-nesting guard agent-surface check is _RUNNER_SRC-only today → adding _ENSEMBLE_SRC is necessary,
   mechanism is right — VERIFIED (check #2 at 95-102 reads `_RUNNER_SRC` only).
4. StubTransport injection path — PARTIALLY UNSOUND → FINDING 1 (CRITICAL): the swarm precedent
   (test_commands_run.py:507-568) mirror-shape exists but injects at the CLI level via the
   single-shared-stub factory, which cannot satisfy I1's distinct-`model_id` diversity assertion.
5. adversarial-seam decision (0.3) operationally sound — VERIFIED: /sc:adversarial is a SKILL with no
   importable module; a 2nd top-level ClaudeProcess is NFR-7-legal (guard bans literals + asserts
   ClaudeProcess presence).
6. verification commands/test files exist and run — VERIFIED (all cited test files present;
   merge.py/contract.py/transport anchors confirmed).
7. OI-1 mapping vs real field availability — VERIFIED: the 6 reflect verdict fields ARE absent from
   swarm ResultContract; only `status` shared (different semantics).
8. runtime paths: config.py resolve_config kwarg shape OK; --reviewers Q8 pre-clamp reaches the
   degrade path (trigger 6/10) — VERIFIED.

---

## Self-Audit (Inherited Structural Verdict — Reliance Audit, PR-04 / INV-019)

**(a) Reliance list — structural PASS items I relied on (skipped re-checking):**
- Relied on rf-qa A.10 PASS for item self-containment (B2 components) — did NOT re-verify that each
  item reproduces its own context blocks.
- Relied on rf-qa A.10 PASS for phase-structure / §4.6 ordering, Phase-0-gates-gate-Phase-3, POST
  reflect flat-wrapper penultimate form, and status→Done last.
- Relied on rf-qa A.10.25 PASS for research-alignment (items trace to research files).
- Relied on rf-qa for section numbering / frontmatter shape.

**(b) Independent semantic checks where structural PASS was insufficient and my own tool work was
required (≥1, INV-019):**
- **The stub-transport single-model contradiction (FINDING 1)** is invisible to any structural gate:
  every cited anchor is real and every item is self-contained, yet the mandated runtime path
  (`_resolve_run_transport_factory("stub")` → single shared `model_id`) cannot satisfy I1's
  `t2_model_class_diversity == "full"` assertion. Found ONLY by reading commands.py:670-673 +
  stub.py:122-159 + _resolve_run_transport docstring + contract.py:267-269 and reasoning about the
  data flow. Structural PASS was insufficient; my own Bash/grep/Read tool work was required.
- **Diversity-source semantics (Step 3.3/U5 vs FR-RH2.4):** verified contract.py trigger 7 keys off
  `t2_model_class_diversity` (a contract field ensemble.py populates), confirming the
  "diversity over distinct succeeded model_id" rule is enforced downstream — which is precisely what
  makes FINDING 1 load-bearing. Required reading contract.py:267-285 directly.
- **pass.yaml key-count + version (FINDING 2):** `grep -cE '^[a-z_]+:'` = 21, contract_version "1.3.0";
  could not be derived from the structural verdict.

---

## Summary
- Checks passed: 17 / 20
- Checks failed: 3 (1 CRITICAL, 0 IMPORTANT, 2 MINOR)
- Critical issues: 1 (FINDING 1 — stub single-model vs I1 diversity)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)
- Axis lens status: AX-1 drift ACTIVE (GOAL baseline captured from R-001).

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | Step 3.1 (2) + Step 6.1 (I1) + Step 6.3 (I3) | `_resolve_run_transport_factory("stub")` returns a single shared `model_id` for all slots; I1 asserts `t2_model_class_diversity=="full"` (needs ≥2 distinct `model_id`s). The proof is unsatisfiable via the mandated seam, and I1(distinct) vs I4(same-class) need OPPOSITE, unspecified stub configs. | Add an explicit sub-step specifying how the stub path yields ≥2 distinct succeeded `model_id`s (own per-slot stub factory / custom `transport_for_slot` injection / swarm-side distinct-stub branch), AND how I4 deliberately binds two slots to the SAME `model_id`. |
| 2 | MINOR | Step 6.7 (I7) | pass.yaml descriptor says "23-key shape"; actual 21 top-level keys. `contract_version` "1.3.0" in fixture vs ensemble.py-emitted "1.0". | Correct "23-key"→"21 top-level keys"; note I7 must assert major-1, not literal version equality. |
| 3 | MINOR | Step 0.2 / 0.1a | BLOCKED-slug anchors `contract-missing`/`child-crash` off by ±1 line (161 vs 162 return). | Tighten anchors to the return-line; remaining version/malformed slugs verified exact. |

## Confidence
Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(All 20 review items checked with direct tool evidence against shipped source at start_commit
63f1a8153d2375e48369059c253dc2a76f73c063.)

## Tool engagement
Read: 3 | Grep/Bash(grep+sed): 7 Bash calls (each targeting specific anchors) | Glob: 0
(Tool calls ≥ checklist items: 10 evidence-gathering calls covering 20 items, each Bash call
batching multiple co-located anchor verifications for the same item cluster.)

## Web research
None performed — all verification was local-file-bound against shipped source. Tavily not needed.

---

## VERDICT: FAIL

**Blocking issue:** FINDING 1 (CRITICAL). The load-bearing non-mocked I1 positive witness asserts
`t2_model_class_diversity == "full"`, but the stub transport seam the task mandates
(`_resolve_run_transport_factory("stub")`) returns a single shared `model_id` across all slots,
making that assertion unsatisfiable through the specified path — and I1 (distinct classes) vs I4
(same class) require opposite, unspecified stub configurations. The task must specify the stub
per-slot `model_id` mechanism before execution, or the executor will either fail I1 or silently
bypass the mandated seam (producing a proof that does not exercise what FR-RH2.4 claims).

The two MINOR drift findings (2, 3) are non-blocking but should be corrected for anchor hygiene.

All other 17 operational checks PASS: every load-bearing swarm signature, the FR-6 demotion anchor,
the no-nesting guard extension premise, the adversarial-seam NFR-7 legality, the OI-1 field-absence
claim, the diversity-derivation downstream enforcement, and the --reviewers/--transport plumbing
runtime paths are operationally sound against shipped source.

## QA Complete

### FINDING 3 — MINOR — `axis: AX-1 (drift)`
**Location:** Step 0.1a / Step 0.2 — BLOCKED-slug line anchors in contract.py.

Step 0.2 cites "contract-missing at contract.py:161". Actual: the `reason = "child-crash" if
child_rc != 0 else "contract-missing"` assignment is at contract.py:161 and the `_make_result(...
contract-missing ...)` RETURN is at 162. Likewise `child-crash` is referenced at 156/158/161 (the
task says 156/158). These are within ±1 line of the cited anchors and point at the correct
construct; the operational meaning is preserved. `contract-version-missing` (167/170),
`unknown-major-version` (175/176), `malformed-degraded-components` (187/190),
`malformed-contract-boolean` (203/206) all verified EXACT. Impact: negligible; flagged for anchor
hygiene only.
