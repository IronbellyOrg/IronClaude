# QA Report — research-depth (Adversarial)

**Track goal:** Implement the reflect Tier-2 fallback model ladder per revised design.md
**Lens:** research-depth — is the research deep enough to produce a granular, per-file/per-symbol, immediately-actionable MDTM task file WITHOUT re-reading source?
**Date:** 2026-07-06
**Fix authorization:** false (report only)
**Stance:** Adversarial — assume research is superficial until proven otherwise.

---

## Progress Log

- [ ] Inventory research files
- [ ] Read design.md
- [ ] Read each research file
- [x] Cross-verify claims against actual source (ensemble.py, dispatch.py, openai_compat.py, fallback.py)
- [x] Depth checks 1-5
- [x] Verdict

---

## Verification performed (tool-grounded, not sampled)

I independently re-Read source for ~28 load-bearing claims. Every line-grounded
claim in research 01/02/03 matched source EXACTLY:

| Claim (research) | Source verified | Result |
|---|---|---|
| `run_tier2_ensemble` def @ ensemble.py:171 | sed 171 | EXACT |
| seam between L225 (`normalize_wave2` end) / L226 (`succeeded_final_paths`) | sed 225,226 | EXACT |
| `build_reflect_contract` def @ ensemble.py:553 | sed 553 | EXACT |
| `compute_model_class_diversity` call @615, `compute_vendor_diversity` @616 | sed 615,616 | EXACT |
| diversity helper defs @641/@651 | sed 641,651 | EXACT |
| `_LOAD_BEARING_BOOL_FIELDS` = 7 fields @contract.py:48-58 (no merge/diversity/t2_fallback member) | sed 48-58 | EXACT |
| `_degraded_reason` def @256; T6 `degraded-tier1` (271-272) BEFORE T10 `single-reviewer-fallback` (288-289) | sed 256,271,288 | EXACT (first-match order) |
| swarm T2 constants @51/52/57/63; `t2_models` @95 | sed | EXACT |
| `_collect_t2_models` @178-185 (1-based dense loop) | sed 178-185 | EXACT |
| F1 root: `transport_for_slot(slot_index)` @dispatch.py:454; tasks over `range(workers_requested)` @464-471 | sed | EXACT |
| openai_compat import block @98-103 (4 T2 constants), `read_env` @159 | sed | EXACT |
| `pool[slot_index % len(pool)]` @commands.py:692; `ModelPoolTooSmallError` guard @687-688 | sed | EXACT |
| **research-04 Finding A**: `tests/cli/swarm/` does NOT exist; tests live at `tests/swarm/` | ls | CONFIRMED |
| **research-04 Finding B**: `tests/cli/reflect/test_contract.py` does NOT exist | ls | CONFIRMED |
| greenfield grep (`t2_fallback`/`read_env_for_pool`/`make_fallback_slot_factory`/`t1_models`/`T1Model`) = 0 in src+tests | grep -c | CONFIRMED (0) |
| design §9 lists exactly 9 test files (4 unit + contract + verdict-regression + stub-integ + 2 swarm) | sed 625-645 | CONFIRMED |
| `make_fallback_slot_factory(pool, ladder, *, base_url, api_key) -> Callable[[str], Transport]`, slot-NAME keyed | sed 311-335 | CONFIRMED |
| 5 pure + 1 impure split (`run_fallback_ladder` is the only impure) | design:180,213-257 | CONFIRMED |

Tool engagement: Read 6 (research x5 + notes), Bash/grep/sed/ls 4 (multi-claim
batches covering ~28 distinct assertions). Zero claims taken on trust.

---

## Depth checks 1-5 (assigned focus)

**1. HOW the seams work (control flow, not just line inventory) — PASS.**
Research 01 §1 traces the full primary flow: `dispatch_wave1`(210) → `_stamp_worker_paths`(216)
→ `normalize_wave2`(217-225) → [CONTROLLER SEAM] → `succeeded_final_paths`(226-230)
→ `reduce_wave3`(239) → adversarial gate `len>=2`(259) → `build_reflect_contract`(308).
It explains WHY the seam is between 225/226 (appending to `normalized_workers` flows
through all three downstream consumers unchanged) and that per-attempt flow MUST mirror
the stamp→normalize order (§4.3). Research 02 §3-4 traces the fallback dispatch path
dispatch→`_factory(slot_index)`→`pool[slot_index % len]`. Behavioral, not inventory.

**2. F1 slot-name escalation deep enough to build `make_fallback_slot_factory` + test — PASS.**
Research 02 §4 nails the ROOT CAUSE with a mechanical proof: 1-worker `WorkerSpec(count=1)`
⇒ `workers_requested==1` ⇒ only `index==0` ⇒ factory always called `slot_index==0` ⇒
`pool[0]==T1Model01` every time ⇒ `T1Model02→pool[1]` escalation mechanically unreachable
via the positional map. The design supplies the exact factory signature
(`Callable[[str], Transport]`, ladder[i]→pool[i], raises `fallback_config_missing`).
A builder can write both the function and the "second attempt resolves pool[1] not pool[0]
twice" test without guessing.

**3. Test injection patterns concrete for all 9 test files — PASS.**
Research 04 §3 documents both idioms verbatim from `test_ensemble_stub_integration.py`:
`_distinct_stub(slot)→StubTransport(model_id=stub_model_id(slot))`, hand-rolled
`_FailingTransport` returning `WorkerResult(status="proxy_error")`, the per-slot `factory`
variant, `_run(config, transport_for_slot)` driver, `_const_score` adversarial seam,
`patch.object(...,"ClaudeProcess",_boom)` no-launch proof. For verdict/contract tests it
gives the `_load(name)` + `FIXTURES_DIR` helper and the exact
`derive_verdict(_load(...), expected_tier=2, ...)` call shape + exit-code matrix. For F3 it
gives `httpx.MockTransport(handler)` + `read_env(env_dict)`. Each of the 9 files has a
named reuse source.

**4. pure-vs-impure split of fallback.py understood for per-function items+tests — PASS.**
Design + research agree: 5 pure helpers (`classify_outcomes`, `evaluate_quorum`,
`plan_next_attempt`, `select_contributing_set`, `make_fallback_slot_factory`) + 1 impure
`run_fallback_ladder` (the loop that injects dispatch/normalize). The §9 table maps each
pure helper to its own unit test file.

**5. Per-file items WITHOUT re-reading ensemble.py/dispatch.py/openai_compat.py — PASS
(for the three named files).** Those three are exhaustively line-grounded. See the IMPORTANT
finding for the one adjacent surface (`reflect/config.py`) that is flagged but NOT grounded.

---

## Issues Found

| # | Severity | Location | Issue | Recommended remediation |
|---|----------|----------|-------|------------------------|
| 1 | IMPORTANT | reflect/config.py `resolve_config` (grounding gap across all 5 research files) | The `--tier2-fallback` flag and the 3 new `ReflectConfig` fields do NOTHING unless threaded through `resolve_config` (verified to exist at `config.py:238`, exact sibling pattern `isolate_reviewers=isolate_reviewers`@380 / `reachability=reachability`@382). Research 01 §5+§6 explicitly flags this edit ("must map it to `ReflectConfig.tier2_fallback_enabled`"; "stub-default-coupling logic would live in config.py resolve_config") but marks it "out of scope here" — and NO research file line-grounds `reflect/config.py`. The builder cannot write a per-line-grounded item for this REQUIRED edit surface without an unplanned source read, brushing the "actionable without re-reading source" depth bar. | Add a short grounding pass (or fold into the builder's Phase-1 live-anchor re-verify) covering `reflect/config.py:238-382`: the `resolve_config` signature params, the `ReflectConfig(...)` construction kwargs block (~L378-382), and the `--transport stub` default-coupling branch. This is the ONLY un-grounded required edit surface. |

Notes on non-issues (checked adversarially, found sound):
- G1 (T1 proxy binding) is a *deliberate* `needs_human_decision` HALT the user asked for,
  not a blind gap; env-var NAMES claim consistent (grep of `src/` = 0, values live in
  `~/.aienv` per the proxy contract, not source).
- G2 (circular import) offers two concrete resolutions (extract `_diversity.py` incl. the
  private `_vendor_from_model_id`, or function-local import); design flags option (a).
- G3 (wall-clock) is a *verify* not an edit; design §7.4 covers deadline threading.
- Research 04/05 caught TWO errors in the driving design itself (Finding A swarm path,
  Finding B phantom `test_contract.py`) — adversarial-grade depth, the opposite of a
  surface file-inventory.

---

## Self-Audit

**(a) Reliance list — items where I could have relied on research claims but did not:**
- Did NOT rely on research 01/02 line citations — independently re-Read every cited seam.
- Did NOT rely on research 04 Finding A/B — independently `ls`-confirmed both.
- Did NOT rely on the "greenfield/zero hits" claim — independently ran the grep (0).

**(b) Independent semantic checks (tool-grounded):**
- First-match verdict order (T6 before T10) — verified by reading `contract.py` 256/271/288,
  confirming `degraded-tier1` returns before the `single-reviewer-fallback` branch is reached.
- F1 mechanical unreachability — verified `dispatch.py:454`+`464-471` and `commands.py:692`
  together produce `pool[0]` for a 1-worker dispatch, corroborating the root-cause proof.
- Required-but-ungrounded edit surface — verified `resolve_config` @`config.py:238` with the
  exact threading kwargs (380/382), establishing the IMPORTANT finding is real, not speculative.

---

## Confidence

Verified: 5/5 depth checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
Tool engagement: Read 6 | Grep/Bash 4 (batched, ~28 distinct assertions verified)

---

## VERDICT: PASS (with one IMPORTANT non-blocking grounding recommendation)

The research is genuinely DEEP, not a surface inventory. All five assigned depth checks
PASS: control flow through the seams is traced behaviorally; F1 slot-name escalation is
proven mechanically and the factory signature is fully specified; all 9 test files have
named, concrete injection patterns; the 5-pure/1-impure fallback.py split is per-function
clear; and the three named source files (ensemble/dispatch/openai_compat) are exhaustively
line-grounded. ~28 line claims independently re-verified — every one EXACT — and the
research even caught two errors in its own driving design (adversarial-grade).

The single IMPORTANT finding (reflect/config.py `resolve_config` threading is flagged but
not line-grounded) is a disclosed, bounded handoff — not an undetected superficiality — and
does not sink the depth verdict for the assigned focus. Recommend the builder ground
`reflect/config.py:238-382` before writing the flag/field-threading item.

---
