# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** Reflect Tier-2 fallback model ladder
**Date:** 2026-07-06
**Phase:** research-gate
**Lens:** gap-detection (areas the design requires but no research covers)
**Fix cycle:** N/A
**Fix authorization:** false (report only)

---

## Scope & Method

Verified all 5 `research/*.md` + `research-notes.md` against the design's work breakdown
(design §2, §4.3.1, §5, §6, §7.1–7.4, §9, §10, §12, §13). Lens: find work the design
REQUIRES that no research file grounds. Every design claim spot-checked below was
re-verified against the live worktree tree (not trusted from the research text).

**Independent verifications performed (tool-cited):**
- `runner.py:508-523` read directly — confirmed in-process ensemble path `run_tier2_ensemble(config); rc = 0` has NO outer timeout; `timeout_seconds` only on the ELSE Tier-1 `ClaudeProcess` branch (L522).
- `reflect/config.py:238-383` read — `resolve_config` construction tail (L358-383) ends `reachability=reachability`; 3 new `tier2_fallback_*` fields NOT threaded; no stub-coupling clause.
- `reflect/ensemble.py:140-209` read + grep — `run_tier2_ensemble` receives only `ReflectConfig`; imports `_resolve_run_transport_factory` but NOT `SwarmConfig`; zero `t1_models`/`swarm_config` references.
- `~/.aienv` name-only grep — `T1ProxyUrl`, `T1ProxyKey`, `T1Model01`, `T1Model02` ALL present as distinct env-var names (values not read, per proxy-contract memory).
- `commands.py:459-492` read — `_build_inner_command` tmux forwarding of `--promote`/`--no-reachability`/`--allow-single-vendor`/`--isolate-reviewers`/`--resume` confirmed.

---

## Gaps Found

### GAP-1 (IMPORTANT) — reflect `config.py::resolve_config` seam entirely un-grounded
The design requires (§7.2, §10 commands.py row) that the 3 new `ReflectConfig` fields
(`tier2_fallback_enabled/_ladder/_max_attempts`), a new `tier2_fallback` signature
param, AND the `--transport stub → default fallback OFF` coupling all land in
`resolve_config`. **No research file covers `config.py`.** Research 01 §5/§6 explicitly
punts it: "resolve_config … out of this file's scope; flagged for the config researcher /
task builder" — but there IS no config-researcher file in the 5-file set. Verified live:
`resolve_config` is at `config.py:238`, its `ReflectConfig(...)` build is `config.py:358-383`
and currently ends at `reachability=reachability` with none of the fallback fields. The
§7.2 `stub → fallback OFF` default has **no grounded home** anywhere in the research.
→ Builder must invent these edits with no file:line anchor, risking a dropped field-thread
or a mis-placed/omitted stub-coupling (a silently non-functional flag).
**Remediation:** ground `resolve_config` signature (`config.py:238-262`) + construction
tail (`config.py:358-383`) + the exact insertion point for the `stub→fallback OFF` clause,
before build.

### GAP-2 (IMPORTANT) — ensemble→swarm T1 pool + proxy-cred acquisition seam un-grounded (integration point)
This is the design's central hand-wave. `run_tier2_ensemble` (`ensemble.py:171`) receives
ONLY `ReflectConfig`; the runner calls it as `run_tier2_ensemble(config)` (`runner.py:512`,
verified) with no `transport_for_slot`, no `env`, no `SwarmConfig`. The existing
`resolve_t2_transport_factory` (`ensemble.py:140`) → `_resolve_run_transport_factory`
binds the proxy **internally** and returns a `Callable[[int], Transport]` — it never
surfaces `base_url`/`api_key`. YET design §2.1 pseudocode builds
`make_fallback_slot_factory(pool=swarm_config.t1_models, base_url=..., api_key=...)` from a
`swarm_config` that **does not exist at the seam** (verified: ensemble.py has zero
`SwarmConfig`/`t1_models` refs). No research file traces the concrete path from `config`/
`env` to a T1 `read_env_for_pool(model_prefix="T1Model0", ...)` `TransportConfig`
(base_url/api_key/models) inside the ensemble. The single most load-bearing integration
point is exactly the one left un-grounded.
**Remediation:** research/builder item must ground how the ensemble obtains the T1 pool +
proxy creds (e.g. `SwarmConfig.from_env(env)` for `t1_models`, or a direct
`read_env_for_pool` call returning `TransportConfig`), and how `deadline`+`fallback_metadata`
thread through the `run_tier2_ensemble(config)`-only runner call.

### GAP-3 (IMPORTANT, premise confirmed TRUE) — F4 "no outer timeout" premise never grounded in research
Design §7.4's whole wall-clock decision rests on `runner.py:508-513` having no outer
`ClaudeProcess` timeout around the ensemble. Research-notes G3 flags "verify runner.py in-
process path has no outer timeout" — but **no research file reads runner.py** (01 is scoped
to ensemble/contract/models/commands; 02 swarm; 03 patterns; 04 tests; 05 template). I read
it myself: `runner.py:508-513` = `if expected_tier == 2 and ClaudeProcess is _ProductionClaudeProcess: run_tier2_ensemble(config); rc = 0` — no timeout wrapper; `timeout_seconds=config.timeout_seconds` is on the ELSE Tier-1 branch (`runner.py:522`). Premise CONFIRMED TRUE, so the design decision is sound — but the research gate shipped with its load-bearing premise unverified.
**Remediation:** capture the `runner.py:508-523` grounding in the research set so the
builder can cite it; low substantive risk (confirmed).

### GAP-4 (MINOR, but flips a design default) — `.aienv` T1 proxy contract grounded only in research-notes, not a research file
research-notes G1 claims `T1ProxyUrl`/`T1ProxyKey`/`T1Model01`/`T1Model02` exist as env
names and that a **dedicated T1 proxy contract** exists, superseding design §7.3/§13-item-1
("reuse the T2 proxy"). I confirmed against `~/.aienv` (name-only grep): all four T1 names
ARE present. So G1 is factually correct and the recommended binding
`read_env_for_pool(model_prefix="T1Model0", proxy_url_env="T1ProxyUrl", proxy_key_env="T1ProxyKey")`
is right. Two residual gaps: (a) **no research FILE** carries this env-name evidence — it
lives only in the notes without a capture command; (b) the design BODY (§7.3) still defaults
to the wrong T2-reuse binding, so a builder grounding from §7.3 alone would wire
`T2ProxyUrl`/`T2ProxyKey` for the T1 pool. Design §13-item-1's "if `~/.aienv` proves a
distinct T1 contract" condition is already SATISFIED — it should be stated as decided, not
deferred. Note this affects only the real-dispatch lane (rollout step 5); stub-lane work
(steps 1–4) is unaffected.
**Remediation:** surface the T1 proxy-contract finding into a research file; the
needs_human_decision HALT item (gap #7) should present the recommended answer
(`T1ProxyUrl`/`T1ProxyKey`) explicitly rather than "confirm later."

### GAP-5 (MINOR) — LadderOutcome / attempt-ledger metadata (§5/§6) source citations unverified
The metadata schema (`reviewer_attempts`, `contributing_reviewer_attempt_ids`,
`primary_failures_preserved`, `tier2_certification_basis`, `terminal_reason` enum) is
greenfield (research 04: zero existing refs) and rides over `WorkerResult` fields that ARE
grounded (`index`/`model_id`/`status`/`final_path` — research 01 §3, 02 §5). Code side is
ADEQUATE. However the design cites `merged-requirements.md:185-216/:350/:364` as the source
for specific field choices (`tier2_certification_basis`, the *omitted* `model_slot`/
`retry_count`, the *excluded* `aborted_or_cancelled` enum) and **no research file verifies
those source-doc line citations** (no research file reads merged-requirements.md).
**Remediation:** treat §5/§6 schema as authoritative-by-design; do not let the builder rely
on merged-requirements line numbers as anchors. Low substantive risk (additive telemetry).

### GAP-6 (MINOR / hygiene) — research 05 carries contradictory Status markers
`05-template-and-examples.md:3` says `**Status: In Progress**` while `:199` says
`**Status: Complete**`. Checklist item 1 (file inventory) requires a single unambiguous
`Status: Complete`. Consistent with incremental writing (a stale top marker), but a
reviewer/builder scanning the header would read "In Progress."
**Remediation:** fix the line-3 marker to `Complete`.

---

## Design defects the research CAUGHT (not research gaps — noted for builder)
These are the research doing its job; the builder MUST follow the research correction over
the design text:
- **Design §9 swarm test path is wrong** (`tests/cli/swarm/` does not exist) — research 04
  Finding A corrects to `tests/swarm/`. Verified: no `tests/cli/swarm/` dir.
- **Design §9 labels `test_contract.py` "existing"** — research 04 Finding B: it does not
  exist; create new OR fold into `test_verdict_mapping.py`.
- **Design §2.1 line drift** — `build_reflect_contract` def is `ensemble.py:553` not `:552`;
  `_degraded_reason` def is `:256` not `:265`; `ReflectConfig` body starts `:58` — research
  01 §0 reconciled all (±1). Non-blocking.

## Well-covered areas (verified, no gap)
- **gap #1 (G2 circular import):** SUFFICIENT. Research 01 §3 grounds the 3 helpers
  (`compute_model_class_diversity` L641, `compute_vendor_diversity` L651, `_vendor_from_model_id`
  L672) and explicitly notes `_vendor_from_model_id` must move WITH the two public helpers for
  option (a) — matching design §10 "move `_vendor_from_model_id` too."
- **gap #4 (--no-tier2-fallback 4-edit surface):** SUFFICIENT. Research 01 §6 grounds all 4
  edits incl. tmux `_build_inner_command` forwarding (verified `commands.py:459-492`).
- **F1 slot-name escalation:** SUFFICIENT. Research 02 §3/§4 grounds the `slot_index==0` root
  cause (`dispatch.py:454/471`, `commands.py:692 pool[slot_index % len(pool)]`) exactly.
- **F3 read_env_for_pool:** SUFFICIENT. Research 02 §2 + 04 §1 ground the T2-hardcoded
  `read_env` (`openai_compat.py:98-103/159-202`) and the thin-wrapper regression harness.
- **Additive-kwarg / dataclass-ordering / collector-generalization patterns:** SUFFICIENT
  (research 03 §1-4).

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory / Status:Complete | PASS* | 5 research files + notes present; 01-04 marked Complete; **05 has BOTH In Progress (L3) + Complete (L199)** → GAP-6 |
| 2 | Evidence density | PASS | Spot-checked file:line claims independently (runner.py, config.py, ensemble.py, commands.py tmux, .aienv) — all held; research is Dense where it covers |
| 3 | Scope coverage vs design work breakdown | FAIL | config.py resolve_config (GAP-1), runner.py deadline premise (GAP-3), ensemble→T1 acquisition (GAP-2) required by design, covered by NO research file |
| 4 | Doc cross-validation | FAIL | merged-requirements.md §5/§6 source citations unverified by any file (GAP-5); code-side claims are code-grounded (fine) |
| 5 | Contradiction resolution | PASS | design §7.3 (reuse T2 proxy) vs research-notes G1 (distinct T1) surfaced; confirmed G1 correct vs .aienv; research 04 vs design §9 test paths resolved in research's favor |
| 6 | Gap severity rating | PASS | each gap rated; ALL gaps → overall FAIL per gate rule |
| 7 | Depth (Deep: end-to-end flow) | PARTIAL | primary/fallback dispatch seam traced end-to-end (01+02); ensemble→T1-pool flow un-traced (GAP-2) |
| 8 | Integration point coverage | FAIL | reflect-ensemble↔swarm-T1-transport integration under-grounded (GAP-2); config threading (GAP-1) |
| 9 | Pattern documentation | PASS | research 03 documents additive-kwarg, dataclass ordering, collector generalization, first-match chain, test seams thoroughly |
| 10 | Incremental writing compliance | PASS* | files show growing structure; 05 stale top marker (GAP-6) is a symptom of incremental writing |

---

## Summary
- Checks passed: 6 / 10 (2 FAIL, 2 PARTIAL/asterisk)
- Gaps: 6 total — IMPORTANT: 3 (GAP-1, GAP-2, GAP-3), MINOR: 3 (GAP-4, GAP-5, GAP-6)
- Critical issues: 0 (none will directly cause synthesis/build hallucination of a WRONG fact; GAP-1/GAP-2 cause OMISSION or invented anchors)
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Confidence Gate
- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 6 (via Bash) | Glob: 0 | Bash: 5 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
  (No external lookup required — all verification is source-truth-local. Tool calls (~13) ≥ 10 checklist items.)
- Every checklist item verified with a cited tool call; every gap independently re-checked against the live tree (runner.py, config.py, ensemble.py, commands.py, ~/.aienv). No item taken on the research's word alone.

## Recommendations (before task-build proceeds)
1. **Close GAP-1 + GAP-2** (IMPORTANT) — add a short research pass (or explicit pre-grounded
   builder items) covering `reflect/config.py::resolve_config` and the ensemble→swarm T1
   pool/proxy-cred acquisition path. These are the two seams where the builder currently has
   no file:line anchor and would either omit an edit or hallucinate one.
2. **Close GAP-3** — capture the `runner.py:508-523` "no outer timeout" grounding (premise
   already confirmed TRUE here; just needs to live in the research set).
3. **Close GAP-4** — record the `~/.aienv` T1 proxy-contract finding in a research file and
   have the needs_human_decision HALT item state the recommended `T1ProxyUrl`/`T1ProxyKey`
   binding explicitly (the §13-item-1 condition is already satisfied). Stub-lane work is not
   blocked by this.
4. **GAP-5 / GAP-6** — minor: note §5/§6 schema is design-authoritative (don't anchor on
   merged-requirements line numbers); fix research 05 line-3 status marker.
5. Builder MUST honor research 04 Findings A & B (swarm tests → `tests/swarm/`;
   `test_contract.py` does not exist) over design §9.

---

## Overall Verdict: FAIL

Per the research-gate rule "ALL gaps regardless of severity = FAIL," and given 3 IMPORTANT
coverage gaps (config.py resolve_config seam, ensemble→swarm T1 acquisition integration
point, and the un-grounded F4 timeout premise), this research set is NOT yet green for an
unattended task-build. The gaps are remediable and mostly narrow (two un-covered files +
one un-captured-but-true premise); none indicate fabricated content. The research that IS
present (01–04 especially) is dense, well-grounded, and independently verified. Re-gate after
GAP-1/GAP-2/GAP-3 are closed.

## QA Complete

---
