# Research Completeness Verification — Gap-Fill Re-Gate (Round 2)

**Topic:** Reflect T2 fallback ladder — research gap closure
**Date:** 2026-07-06
**Analysis type:** completeness-verification (gap-fill re-gate)
**Lens:** completeness + cross-validation (source-grounded)

Focus files:
- research/06-config-threading-gap-fill.md
- research/07-ensemble-t1-integration-seam.md
- research/04-test-surface.md (edits)
- design.md §2.1, §4.3.1

Prior gaps under re-verification: GAP-1/G-1, GAP-2, G-2/C-1, G-3, G-6/GAP-3.

---

## Verdict: PASS — all 5 prior gaps CLOSED with source-accurate structural grounding. 3 MINOR residuals (non-blocking, itemized below).

Each gap was re-verified by re-Reading the actual source (config.py, ensemble.py, swarm/commands.py, runner.py) and the corrected design sections — not by trusting the research prose.

---

## GAP-1 / G-1 (was Critical) — config.py resolve_config threading — CLOSED

Verified against `src/superclaude/cli/reflect/config.py` (re-Read 2026-07-06):

- `resolve_config` def keyword is at **line 238** (research/06 says "237-382"; 237 is the blank line above — 1-line drift).
- Last keyword-only param IS `reachability: bool = True` at **line 260** (research says 259 — 1-line drift). Research/06's insertion precedent ("add the new param after reachability, mirroring it") is STRUCTURALLY EXACT.
- The `return ReflectConfig(...)` construct runs **lines 358–383**; the final forwarded field IS `reachability=reachability,` at **line 382**, immediately before the closing `)` at 383 (research says "355–381 / reachability at 380" — ~2-line drift). The forward-append precedent is EXACT.
- Transport IS resolved in-body before the return: `resolved_transport ... not in {"openai_compat","stub"}` at **lines 322–326** (research says 326–330 — ~4-line drift). The stub-OFF derived line (`tier2_fallback_enabled and resolved_transport != "stub"`) is implementable exactly as described — `resolved_transport` is in scope from line 322, well before the return.

**Structural grounding is correct on every anchor** (reachability is both the last kwarg AND the last forwarded field; transport set-check exists in-body; flat kwarg return). Only line numbers drift ~1–4 lines low. Anchors are named and greppable, so the builder is not misled. `tier2_fallback_ladder`/`tier2_fallback_max_attempts` correctly ride dataclass defaults (no signature edit) — all existing call sites stay valid.

**Residual R1 (MINOR):** research/06 line numbers run ~1–4 lines low throughout (def 238 not 237; reachability param 260 not 259; return 358–383 not 355–381; transport check 322–326 not 326–330). Non-blocking — every cited symbol/anchor is correct and greppable.

## GAP-2 (was Important) — ensemble→swarm T1 pool/creds acquisition seam — CLOSED

Verified against `ensemble.py` and `swarm/commands.py` (re-Read 2026-07-06). All three sub-claims TRUE:

- **(a) run_tier2_ensemble gets only ReflectConfig + env (no swarm_config):** CONFIRMED. Signature `run_tier2_ensemble(config, *, prompt, transport_for_slot, adversarial_..., env)` at **ensemble.py:171–180**. No `SwarmConfig`, no `t1_models`, no `base_url`/`api_key` in scope. The call to `resolve_t2_transport_factory(config.transport, reviewers=reviewers, env=env)` is at **ensemble.py:201–205** (research cite EXACT).
- **(b) _resolve_run_transport_factory reads creds via read_env internally:** CONFIRMED. `config = read_env(env)` at **swarm/commands.py:680** (research cite EXACT); `OpenAICompatTransport(base_url=config.base_url, api_key=config.api_key, model=...)` built per-slot and cached at **691–701**. base_url/api_key never leave the closure. Function spans **612–707** (research cite EXACT).
- **(c) resolution is a sibling resolve_t1_fallback_factory reading env internally:** the proposed new function correctly mirrors `resolve_t2_transport_factory` (**ensemble.py:140–168**; research says "139–167", 1-line drift). Structurally sound — env is already threaded to `run_tier2_ensemble(..., env=env)` and forwards internally, so no SwarmConfig plumbing is introduced.

**design §2.1 misdirection REMOVED:** CONFIRMED. `grep swarm_config .../design.md` returns only the GAP-2 *correction note* at lines 89–96 ("there is NO `swarm_config` at this seam — run_tier2_ensemble receives only ReflectConfig + env... Resolve the T1 factory from `env` INTERNALLY"). The old `make_fallback_slot_factory(pool=swarm_config.t1_models, ...)` construct is gone from §2.1, replaced by `resolve_t1_fallback_factory(config.transport, ladder=..., env=env)` at lines 97–101. §4.3.1 (lines 313–318) carries the matching correction and cross-references the §2.1 GAP-2 note. Both sections are now consistent with research/07.

**Residual R2 (MINOR):** `resolve_t2_transport_factory` is at ensemble.py:**140–168**, not the "139–167" cited (1-line drift). All other GAP-2 cites (201–205, 612–707, 680) are byte-exact.

## G-2 / C-1 — T1 proxy binding supersedes the T2-reuse default behind a HALT — CLOSED (with consistency residual)

research/06 (lines 51–73) correctly states the design §7.3 T2-reuse default (`proxy_url_env=T2_PROXY_URL_ENV`) is **SUPERSEDED** and prescribes the `T1ProxyUrl`/`T1ProxyKey` + `model_prefix="T1Model0"` arm via `read_env_for_pool`, gated behind the needs_human_decision HALT. The `read_env_for_pool` shape parameterizes the proxy-env names — CONFIRMED structurally: current `read_env` hardcodes the T2 names (`read_env(env)` at openai_compat.py:159; T2 constants at 179–204 per research/04 §F3), and F3 introduces the parameterized `read_env_for_pool(model_prefix, max_slots, proxy_url_env, proxy_key_env)`. So swapping proxy-env names is a call-site argument choice, not a structural fork. This closes G-2/C-1.

**Residual R3 (MINOR — design/research consistency):** design **§7.3 (lines 550–559)** was NOT harmonized with research/06. §7.3 still frames **T2-proxy-reuse as the DEFAULT** ("Fallback slots reuse the same proxy endpoint/key as T2... the `.aienv`-only-proxy-contract-safe default") with `T1ProxyUrl`/`T1ProxyKey` as a *conditional* swap ("if `~/.aienv` proves a separate T1 proxy contract exists"). research/06 inverts this to "MUST use the T1Proxy* arm, NOT the T2-reuse default." §2.1 and §4.3.1 were corrected for GAP-2 but §7.3 retains the older framing. This is NON-BLOCKING because BOTH arms route through the identical needs_human_decision HALT (rollout step 5): step 1 confirms `~/.aienv` exposes the required names WITHOUT reading values, and if unconfirmed → PENDING-write + halt. Neither arm can ship an unverified binding. **Recommendation:** the builder should treat research/06 as governing §7.3 (or §7.3 should be updated to match §2.1/§4.3.1), so the task item encodes the T1Proxy* arm as primary.

**Note (handled, not a gap):** research/06's factual claim that `~/.aienv` exposes distinct `T1ProxyUrl`/`T1ProxyKey`/`T1Model01` names is not independently verifiable from within this analysis — the `.aienv`-only-proxy contract forbids probing, and the known contract convention centers on `T2Model01..NN`. This uncertainty is correctly ABSORBED by the HALT (confirm-names-without-values, else PENDING+halt), so it does not undermine closure.

## G-3 — needs_human_decision PENDING-write + halt — CLOSED

research/06 (lines 75–96) grounds the HALT semantics per the `feedback_human_decision_items_must_halt` project convention: the item preceding real fallback dispatch (rollout step 5) MUST (1) confirm `~/.aienv` exposes `T1ProxyUrl`/`T1ProxyKey`/`T1Model01` names-only without reading values or probing `:4000/v1`, (2) proceed + log the binding if confirmed, (3) else write a PENDING entry to `### Open Questions` (append, don't delete) and HALT before wiring — never silently fall back to the T2-reuse default. Stub-transport rollout steps 1–4 correctly proceed unblocked (stub certifies without a real proxy). This is grounded in the real project convention and is internally consistent. CLOSED.

## G-6 / GAP-3 (F4 premise) — runner.py no-outer-timeout — CLOSED

Verified against `src/superclaude/cli/reflect/runner.py` (re-Read 2026-07-06) — BYTE-EXACT:

- `expected_tier = 2 if config.depth in {"standard", "deep"} else 1` at **line 506**.
- `if expected_tier == 2 and ClaudeProcess is _ProductionClaudeProcess:` at **line 508**.
- `run_tier2_ensemble(config)` called **directly with no timeout argument and no wrapping timeout construct** at **line 512**; `rc = 0` at **line 513**.
- Contrast confirmed: the Tier-1 `else` branch (line 517+) DOES pass `timeout_seconds=config.timeout_seconds` to `ClaudeProcess` (line 522) — proving the ensemble path has no equivalent outer bound.

F4's premise is correct: no caller-level timeout wraps `run_tier2_ensemble`, so the shared run deadline must be captured INSIDE the ensemble (design §7.4: `deadline = _monotonic() + config.timeout_seconds`). research/06 cites "runner.py:505–513" and design §7.4 cites "runner.py:508–513"; both correctly bracket the real 506–513 range. `config.timeout_seconds` is the single budget source (`timeout or _DEFAULT_TIMEOUT_SECONDS`, config.py:367). CLOSED.

## research/04 edits — verified clean

The two path groundings are correctly reframed from "BLOCKING design errors" to CONFIRMATIONS of the revised design: (A) swarm tests live at `tests/swarm/` not `tests/cli/swarm/` (design §9 agrees); (B) `tests/cli/reflect/test_contract.py` does not exist — create-new or fold into `test_verdict_mapping.py` (design §9 agrees). The WorkerResult line-cite self-correction (models.py:1123–1129, corrected from an earlier "1010–1012", deferring to research 02 as authoritative) is a healthy cross-file reconciliation. Status: Complete. No residual gap.

---

## Compiled Residuals (all MINOR — none block the build)

| # | Severity | Location | Issue | Recommendation |
|---|----------|----------|-------|----------------|
| R1 | Minor | research/06 §config.py | Line numbers ~1–4 lines low (def 238 not 237; reachability param 260 not 259; return 358–383 not 355–381; transport 322–326 not 326–330) | Builder greps `reachability` / the return tail — anchors are correct. Optional: refresh line numbers. |
| R2 | Minor | research/07 | `resolve_t2_transport_factory` at ensemble.py:140–168 (cited "139–167"), 1-line drift | Optional line-number refresh; all other cites exact. |
| R3 | Minor (consistency) | design §7.3 (550–559) vs research/06 | §7.3 still frames T2-proxy-reuse as DEFAULT; research/06 supersedes to T1Proxy* arm. §2.1/§4.3.1 were corrected but §7.3 was not | Treat research/06 as governing §7.3, OR update §7.3 to match §2.1/§4.3.1. Non-blocking: the needs_human_decision HALT protects both arms. |

## Depth Assessment

Both gap-fill files (06, 07) provide line-grounded, symbol-named evidence at the depth required for a builder to write per-line threading + a new resolver function. GAP-2's three sub-claims are all source-true; F4/G-6 grounding is byte-exact; the design §2.1/§4.3.1 corrections landed cleanly. The only shortfall is cosmetic line drift (R1/R2) and one un-harmonized design section (R3), all absorbed by named anchors and the HALT. Sufficient for the standard/deep depth tier.

## Verdict Restated: PASS

All 5 prior gaps (GAP-1/G-1, GAP-2, G-2/C-1, G-3, G-6/GAP-3) are CLOSED with source-accurate structural grounding, re-verified against live source. Residuals R1–R3 are MINOR and non-blocking; R3 warrants a one-line builder instruction (research/06 governs design §7.3).
