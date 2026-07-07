# QA Report — Task/Research Alignment (LENS: task-research-alignment)

**QA Mode:** task-integrity
**Date:** 2026-07-06
**Task file:** TASK-RF-t2-fallback-ladder-20260706-050832.md
**Design:** .dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/design.md
**Track goal:** Implement the reflect Tier-2 fallback model ladder.
**Stance:** ADVERSARIAL — assume builder dropped or misrepresented findings; target ≥3 alignment gaps.

---

## Scope Read (evidence base)

- design.md (all 13 sections, incl. §9 test surface, §10 change map, decisions F1-F7, §13 open items)
- Task file: 6 phases (P1 pure engine, P2 contract metadata, P3 config/controller, P4 swarm T1 slots, P5 needs_human_decision HALT, P6 docs+final gate) + Source Areas + Key Constraints
- research/06-config-threading-gap-fill.md (config threading + T1 proxy reconciliation + HALT semantics + F4)
- research/07-ensemble-t1-integration-seam.md (GAP-2: env-reading sibling resolver)

---

## Check 1 — Every design §10 change-map file → a task item

| Design §10 file | Expected change | Task item(s) | Status |
|---|---|---|---|
| `reflect/fallback.py` NEW | pure helpers + `run_fallback_ladder` | P1.5-1.10, P2.1, P3.4 | COVERED |
| `reflect/ensemble.py` | seam insert, F4 deadline, `t2_fallback=` kwarg, `resolve_t1_fallback_factory` | P1.4, P2.2, P3.5, P3.6, P4.4 | COVERED |
| `reflect/models.py` | 3 defaulted `ReflectConfig` fields | P3.1 | COVERED |
| `reflect/contract.py` NO-CHANGE | verdict map untouched | P2.6 (git-diff-empty verify) | COVERED |
| `reflect/commands.py` | `--no-tier2-fallback` (4 edits) | P3.3 | COVERED |
| `swarm/config.py` | `T1Model0N` + `_collect_models` | P4.1 | COVERED |
| `swarm/transports/openai_compat.py` | `read_env_for_pool` + thin wrapper (F3) | P4.2 | COVERED |
| `swarm/commands.py` | parameterize `_resolve_run_transport_factory` | P4.3 | COVERED |
| `swarm/models.py` NO-CHANGE | no new `WorkerStatus`/field | P4.7 (git-diff-empty verify) | COVERED |
| `swarm/dispatch.py` read-only (F1 root cause) | no edit | P1.3 anchor read; Source Areas L119 | COVERED |

Extra file added by task (NOT in §10 table): `reflect/_diversity.py` NEW. This is grounded in design §10 "Circular-import guard" preferred option (a) ("move the two diversity helpers into a neutral `reflect/_diversity.py`") and §13 item 4. The task picks option (a) and materializes it (P1.4). Legitimate grounding, not fabrication.

Extra file added by task (NOT in §10 table): `reflect/config.py` `resolve_config` threading (P3.2). NOT in the design §10 change map, but grounded in **research/06** §"Exact edit points". See Observation O1 below — the §10 change map under-counts; the task correctly supplements from research/06.

**Check 1 verdict: PASS** — all 10 §10 rows covered with correct change/no-change disposition; the two files-added beyond the table are both grounded (design §10 option (a) + research/06).

## Check 2 — Every design §9 test-surface row → a test item at the CORRECT path

| Design §9 row | Expected file / path | Task item | Path correct? |
|---|---|---|---|
| Unit: classify | `tests/cli/reflect/test_fallback_classify.py` | P1.11 | YES |
| Unit: plan (F1+F4) | `tests/cli/reflect/test_fallback_plan.py` | P1.12 | YES |
| Unit: select | `tests/cli/reflect/test_fallback_select.py` | P1.13 | YES |
| Unit: slot factory (F1) | `tests/cli/reflect/test_fallback_slot_factory.py` | P1.14 | YES |
| Contract | `tests/cli/reflect/test_contract_fallback_metadata.py` | P2.4 | YES |
| Verdict-unchanged regression (F6) | EXTEND `tests/cli/reflect/test_verdict_mapping.py` (NOT new `test_contract.py`) | P2.5 | YES — explicitly extends, does NOT create test_contract.py |
| Stub integration (F2) | `tests/cli/reflect/test_ensemble_fallback_stub.py` | P3.7 | YES |
| Swarm config | EXTEND `tests/swarm/test_config.py` (NOT `tests/cli/swarm/`) | P4.5 | YES — `tests/swarm/`, extend-in-place |
| Swarm transport (F3) | EXTEND `tests/swarm/test_openai_compat.py` | P4.6 | YES — `tests/swarm/`, extend-in-place |

The two specific traps the lens flags are both AVOIDED:
- Swarm tests land at `tests/swarm/` (P4.5/P4.6), NOT `tests/cli/swarm/` (which design §9 confirms does not exist). Task Source Areas L121 and P6.G2 restate the non-`tests/cli/swarm/` rule.
- The verdict-unchanged row EXTENDS `test_verdict_mapping.py` (P2.5), NOT a new `test_contract.py`. Design §9 explicitly says `test_contract.py` does not exist; task honors this.

**Check 2 verdict: PASS** — all 9 rows present at correct paths; both path traps avoided.

## Check 3 — Design decisions F1-F7 reflected

| Decision | Design intent | Task encoding | Status |
|---|---|---|---|
| F1 slot-name factory + test | `make_fallback_slot_factory` binds slot NAME→pool position; test 2nd attempt = `T1Model02`→pool[1] | P1.10 (factory), P1.14 (binding test), P1.12 (plan returns `slot=="T1Model02"`) | COVERED — correctly SPLIT: plan asserts name, factory asserts pool[1] binding |
| F2 stamp→normalize seam | per-attempt `stamp` BEFORE `normalize`; stable `final_path` | P3.4 (impl stamps before normalize), P3.7 (asserts non-empty `final_path`) | COVERED |
| F3 read_env_for_pool + thin wrapper | pool-parameterized reader; T2-bound thin `read_env()` | P4.2 + P4.6 (thin wrapper still passes T2 body) | COVERED |
| F4 deadline | run-level deadline captured once, clamps each attempt | P3.5 (capture before dispatch), P3.4 (clamp), P1.12 (wall-clock-exhausted test) | COVERED |
| F5 ensemble-not-contract split | `build_reflect_contract` lives in `ensemble.py`; `contract.py` untouched | P2.2 (kwarg on ensemble.py builder), P2.6 (contract.py git-diff-empty) | COVERED |
| F6 first-match degraded-tier1 test | reason is `degraded-tier1` (T6), NOT `single-reviewer-fallback` (T10) as verdict | P2.5 (asserts `degraded-tier1`, MAY assert `merge_method` field but MUST NOT as reason) | COVERED |
| F7 test paths | `tests/cli/reflect/` + `tests/swarm/`; extend not replace | Throughout P1-P4; see Check 2 | COVERED |

**Check 3 verdict: PASS** — all 7 decisions reflected with correct semantics. F1's plan-vs-factory split is more precise than the design §9 conflation.

## Check 4 — GAP-2 (research/07): env-reading sibling, NOT swarm_config-at-seam

research/07 finding: `run_tier2_ensemble` has **no `SwarmConfig`** in scope; the design §2.1 pseudocode `make_fallback_slot_factory(pool=swarm_config.t1_models, ...)` is NOT constructable at the seam. Resolution = a sibling env-reading resolver `resolve_t1_fallback_factory` that reads the T1 pool from `env` INTERNALLY (mirror of `resolve_t2_transport_factory`).

Task encoding:
- P3.5 adds `resolve_t1_fallback_factory(transport, *, ladder, env)` and its item text EXPLICITLY cites GAP-2: "the ensemble has no `SwarmConfig`, only `ReflectConfig`+`env`; resolve the T1 factory from `env` INTERNALLY like the T2 path."
- P4.3 parameterizes `_resolve_run_transport_factory` to call `read_env_for_pool` (research/07 "Builder action" #2).
- P4.4 wraps into slot-NAME factory via `make_fallback_slot_factory` (research/07 #3).
- P5.3 network-free resolver-binding test (research/07 #4).

The task's 4-step encoding is a 1:1 match with research/07's "Builder action" list, and it avoids the design §2.1 `swarm_config` misdirection.

**Check 4 verdict: PASS** — GAP-2 resolved via env-reading sibling; the disproven `swarm_config`-at-seam approach is explicitly rejected in the task text.

## Check 5 — config.py `resolve_config` threading (research/06) + stub-OFF coupling

research/06 §"Exact edit points": (1) add `tier2_fallback_enabled: bool = True` kwonly after `reachability` (config.py:259); (2) forward `tier2_fallback_enabled=resolved_fb_enabled` in `return ReflectConfig(...)` (config.py:380); (3) `resolved_fb_enabled = tier2_fallback_enabled and resolved_transport != "stub"` after transport resolution; ladder/max_attempts NOT threaded (ride dataclass defaults).

Task P3.2 encodes all four points verbatim: signature param after `reachability`, stub-OFF derived line (`tier2_fallback_enabled and resolved_transport != "stub"`), forward after `reachability=reachability`, and explicitly does NOT thread `tier2_fallback_ladder`/`tier2_fallback_max_attempts`. P3.8 tests stub-OFF + explicit-OFF + defaults, matching research/06 §"Verification."

**Check 5 verdict: PASS** — resolve_config threading and stub-OFF coupling both present and faithful to research/06.

## Check 6 — needs_human_decision HALT (T1ProxyUrl/T1ProxyKey binding, NOT T2-reuse)

This is the highest-risk alignment point (memory `feedback_human_decision_items_must_halt`). research/06 §"Reconciliation" + §"HALT semantics" + research-notes G1 establish: the binding is the **dedicated** `T1ProxyUrl`/`T1ProxyKey` arm (NOT the design §7.3 T2-reuse default, which is SUPERSEDED for this environment); confirmation is read-only NAMES-only, no `:4000/v1` probe, PENDING+HALT on unconfirmed, never silently fall back to T2.

Task P5.1 encodes ALL of these:
- Binding = `model_prefix=T1Model0`, `proxy_url_env=T1ProxyUrl`, `proxy_key_env=T1ProxyKey` (NOT T2).
- Read-only, env-var NAMES only (`grep -oE '^(T1ProxyUrl|T1ProxyKey|T1Model01|T1Model02)' ~/.aienv` — lists NAMES, never values), no `:4000/v1` probe.
- IF confirmed → record binding decision + proceed; IF NOT → PENDING to `### Open Questions` + set `status: ⚪ Blocked` + HALT before Step 5.2; "DO NOT silently fall back to the design's T2-reuse default."
- P5.2/P5.3 gate real-dispatch enablement (`_T1_PROXY_BINDING`) and the real-binding test on the P5.1 confirmation; both are deferred under HALT.
- The safe-degrade scaffolding is staged: P3.5 introduces `_T1_PROXY_BINDING = None` sentinel (openai_compat arm raises `TransportEnvError` → `fallback_config_missing`) until confirmed; P4.4 wires structure but NOT active binding; P5.2 flips the sentinel only on confirmation.
- Stub lane (P1-P4 stub work) explicitly does NOT depend on the HALT (research/06 §"Stub-transport work ... proceeds unblocked").

**Check 6 verdict: PASS (strongest alignment point)** — the task encodes the dedicated T1 proxy binding behind a genuine PENDING+HALT, read-only names-only, no proxy probe, and never auto-defaults to T2-reuse.

## Check 7 — Fabrication check

Every file/symbol referenced by a task item traces to design or research:
- `_diversity.py`, `fallback.py` + all helpers → design §4/§10.
- `resolve_t1_fallback_factory` → design §2.1/§7.3 + research/07.
- `build_fallback_metadata`, `TERMINAL_REASONS`, `TIER2_CERTIFICATION_BASES` → design §6.
- `read_env_for_pool` → design §7.3/F3 + research/02.
- `_T1_PROXY_BINDING` sentinel → NOT a literal design symbol, but a legitimate implementation device realizing the design §7.3 "openai_compat arm degrades until confirmed" + research/06 HALT requirement. It is a mechanism for a design-specified behavior, not a fabricated action.
- config.py `resolve_config` threading → research/06 (see O1).

No task item references a file or symbol absent from both design and research.

**Check 7 verdict: PASS** — no fabrication.

---

## Findings (adversarial — genuine discrepancies surfaced)

### MINOR-1: `fallback_attempts_failed` enum token has no emission producer
Design §6 defines `fallback_attempts_failed` = "attempted slots all terminal-failed" AND `fallback_pool_exhausted` = "both slots attempted, still short." The task's `TERMINAL_REASONS` tuple (P2.1) includes `fallback_attempts_failed`, but no task item wires WHEN it is emitted: `plan_next_attempt` (P1.8) enumerates only `fallback_pool_exhausted`/`fallback_config_missing`/`fallback_wall_clock_exhausted`/`no_fallback_eligible_primary_failure`/`diversity_unrepairable`, and the §8 counter-case (P3.7) asserts `fallback_pool_exhausted`. Result: `fallback_attempts_failed` is dead vocabulary with no producer branch. This faithfully inherits the design's own under-disambiguation of these two adjacent tokens. Severity MINOR (matches design; no verdict impact).

### MINOR-2: `run_fallback_ladder` under-specifies derivation of `build_fallback_metadata` semantic args
P3.4 says the controller returns `LadderOutcome(..., metadata=build_fallback_metadata(...))` but does not spell out how it derives `certification_basis`, `terminal_reason`, `original_primary_pool_fully_succeeded`, `contributing_ids`, and `primary_failures` from the attempt results. P2.1 defines the assembler's signature (all as params), but the wiring that computes those values inside the loop is left implicit. An executor could produce a structurally-valid-but-semantically-wrong metadata block. Severity MINOR (within P3.4's stated scope of "building the attempt ledger" but the arg-derivation is thin).

### MINOR-3: per-attempt `vendor` ledger field threading not pinned to `._diversity`
Design §5/§6 ledger entries carry `vendor: <_vendor_from_model_id>`. After P1.4 moves `_vendor_from_model_id` into `_diversity.py`, `build_fallback_metadata` (P2.1) must import it from `._diversity` to populate the ledger `vendor` field, but P2.1 does not name that import. Minor threading omission. Severity MINOR.

---

## IMPORTANT-1 (carried-forward design ambiguity): plan dispatch-vs-escalate ordering
Design §4.2/§8 contain a latent ambiguity the task inherits verbatim: `plan_next_attempt` should "dispatch the NEXT unused ladder slot" (→ `T1Model01` first) but also "escalate to `ladder[1]` when >1 terminal primary failure." The §8 incident has 2 eligible failures yet dispatches `T1Model01` FIRST (not jumping to `T1Model02`). P1.8 reproduces both rules without disambiguating precedence, so an executor could dispatch `T1Model02` first on a ≥2-failure primary set, contradicting §8. This is a faithful reflection of a design ambiguity (good alignment) but is an executor-risk. The P1.12 F1 test (`attempts_made=["T1Model01"]` → returns `T1Model02`) only pins the SECOND-attempt case, not the first-attempt-with-2-failures case, so the ambiguity is not test-closed. Severity IMPORTANT for the executor; NOT a task-vs-research misrepresentation.

---

## Observations (not gaps — alignment strengths / latent design weaknesses)

### O1: design §10 change map under-counts; task correctly supplements from research/06
`reflect/config.py` `resolve_config` threading is NOT a row in the design §10 change map, and the design §2.1 pseudocode/§7.2 do not show it. The threading is purely a research/06 finding (A.8 depth gate flagged it as "flagged-but-not-line-grounded"). The task adds it (P3.2) correctly grounded in research/06. This is a task STRENGTH — it closes a design change-map omission — not a fabrication and not a gap.

### O2: task resolves an internal design contradiction in the correct (safe) direction
Design §7.3 (governing paragraph, "This paragraph governs") resolves the T1 binding to the DEDICATED `T1ProxyUrl`/`T1ProxyKey` contract, superseding the T2-reuse default. But design §13 item 1 STILL says "decided: reuse the T2 proxy endpoint/key." The task follows §7.3 + research/06 (dedicated T1 arm behind HALT), NOT the stale §13 T2-reuse text. Correct resolution.

### O3: design §7.3 environment-grounding claim is guarded, not trusted
Design §7.3 asserts "`T1ProxyUrl`, `T1ProxyKey`, `T1Model01`, `T1Model02` are all present as distinct names." Memory `feedback_aienv_only_proxy_contract` documents only `T2Model01..NN` in `~/.aienv`. If the design's T1-existence claim is optimistic, the task does NOT inherit the risk: P5.1 re-verifies names-only and HALTs (deferring real dispatch) if the names are absent. The task is defensively correct regardless of whether the design's grounding claim holds.

---

## VERDICT: PASS

All 7 alignment checks PASS. Every design §10 change-map file and §9 test-surface row has a corresponding task item at the correct path; all 7 decisions F1-F7 are reflected with correct semantics; GAP-2 (research/07) is resolved via the env-reading sibling resolver (not the disproven `swarm_config`-at-seam); config.py threading + stub-OFF coupling (research/06) are present; the needs_human_decision HALT encodes the dedicated `T1ProxyUrl`/`T1ProxyKey` binding behind a genuine PENDING+HALT with read-only names-only inspection and no `:4000/v1` probe; and no task item fabricates ungrounded actions.

**Severity-rated gaps:**
- IMPORTANT-1 — plan dispatch-vs-escalate ordering ambiguity carried verbatim from design §4.2/§8; not test-closed for the first-attempt-with-≥2-failures case. (Executor risk; faithful to design, so does not fail the alignment gate.)
- MINOR-1 — `fallback_attempts_failed` enum token has no emission producer branch.
- MINOR-2 — `run_fallback_ladder` under-specifies how `build_fallback_metadata`'s semantic args are derived.
- MINOR-3 — per-attempt `vendor` ledger field not explicitly threaded to the `._diversity` `_vendor_from_model_id` import.

None of the four is CRITICAL. All four are refinement notes for `/sc:implement`, not blocking alignment defects. The task is a faithful, well-grounded translation of the design + gap-fill research, and it correctly supplements a design §10 change-map omission (O1) and resolves an internal design contradiction in the safe direction (O2), while defensively guarding a possibly-optimistic design grounding claim (O3).

---
