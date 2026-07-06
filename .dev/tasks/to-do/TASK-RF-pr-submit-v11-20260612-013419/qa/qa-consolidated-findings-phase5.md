# Phase 5 — Consolidated QA Findings (M3 lens gate — HIGHEST-RISK)

8 lens agents ran (3 structural + 3 content + 2 domain), all report-only.

| Lens | Report | Verdict |
|---|---|---|
| dual-surface lock-step | qa-structural-dualsurface-phase5.md | FAIL (drift findings) |
| internal-consistency | qa-structural-consistency-phase5.md | PASS (2 latent notes) |
| evidence/anchor-freshness | qa-structural-evidence-phase5.md | PASS |
| actionability/test-correctness | qa-content-actionability-phase5.md | PASS (2 test-quality notes) |
| domain-accuracy | qa-content-domain-accuracy-phase5.md | PASS |
| crossref-chain | qa-content-crossref-phase5.md | PASS |
| **INV-fidelity (CRITICAL lens)** | qa-domain-inv-fidelity-phase5.md | **PASS** (INV-001 verbatim + R1/R2/R3 traced) |
| core-purity NFR-6 | qa-domain-core-purity-phase5.md | PASS |

## TOP-LINE VERDICT: FAIL → targeted fixes (NO INV-001 issue — the load-bearing lens PASSED)

**Critically: the INV-fidelity lens (the highest-priority lens for this phase) PASSED** — INV-001
edge byte-identical, exactly one `round_counter += 1` (fsm.py:988), N=2 worked trace confirms
`max_rounds=N ⇒ N pushes`, INV-R1/R2/R3 all traced with worked examples (push_count≤max_rounds+1
holds at equality N+1). The FAIL is driven by the dual-surface lens's drift/maintainability
findings + 2 test-quality gaps — NOT a correctness regression.

## Deduplicated findings + disposition

| # | Finding (lens) | Severity | Disposition |
|---|---|---|---|
| F1 | **Forked fallback pipeline (DRIFT-4).** `_run_fallback` hand-copies verify→fix→validate→push inline rather than re-entering S2_CLASSIFY; transition() Edge 5 models it as S2 re-entry. | IMPORTANT (maintainability, NOT correctness) | **DOCUMENT as by-design + mitigate via test.** run_skill is the EXISTING V1.0 architecture: an imperative run-to-terminal driver that does NOT call transition() (task explicitly: "run_skill() does NOT call transition()"). The fallback mirroring this inline pattern is consistent, not a new fork. Refactoring to share the pipeline is a HIGH-RISK change in the highest-risk phase (could regress INV-001) and out of scope ("build exactly what's asked"). The task's OWN prescribed mitigation is "the dual-surface lens gate verifies the two surfaces match" → addressed by **F4** (a transition()-driving test) + a code comment. |
| F2 | **S5A/S5B states never materialized** in run_skill's result.state (DRIFT-1/3); run_skill jumps straight to S5_AWAITING_REREVIEW / terminal. | MINOR | **FIX** — set `result.state = S5A_RETRIGGER_REVIEW` at the re-trigger step and `result.state = S5B_AUGGIE_FALLBACK` at `_run_fallback` entry, so the imperative surface visibly enters the new states (overwritten by the terminal, but self-documenting + faithful to topology). |
| F3 | **Namespace drift:** transition() event `"rereview_attributed"` vs run_skill outcome token `"attributed"`; no shared constant binds them (internal-consistency). | MINOR | **FIX (comment)** — add a comment documenting the mapping (the outcome token `"attributed"` is what emits the FSM `"rereview_attributed"` edge). They are deliberately different vocabularies (outcome token vs edge event); a comment prevents a maintainer conflating/renaming them. |
| F4 | **Dead transition() edges** (S5A/retriggered, S5B/fallback_findings, S5B/fallback_skip) unreachable from run_skill (internal-consistency MINOR) — and DRIFT-5 (S5b exit fan-out partially modeled). | MINOR | **FIX (test)** — add `test_transition_v11_edges` exercising transition()'s 6 new edges directly (covers the dead edges, pins both surfaces, catches future transition()-side drift). This is the task's prescribed dual-surface mitigation. |
| F5 | **`test_t_auggie_at_most_once` mislabel:** enters `_run_fallback` only ONCE, so it does not exercise the CROSS-ENTRY strict-once guard (actionability). | IMPORTANT (test quality) | **FIX** — strengthen the test to call `_run_fallback` TWICE on the same SkillResult and assert the invoke recorder fires exactly once (genuinely exercises the `if not result.auggie_review_invoked` guard). The durable cross-resume strict-once is separately covered by test_idempotency T-1124. |
| F6 | **Fence-post matrix doesn't discriminate the `>=`→`>` gate mutation** (defense-in-depth masks it); the `>=` regression is caught by `test_gate_uses_ge_not_gt` + `test_t626`'s `summary_posted` assert (actionability). | LOW | **NO-FIX (documented)** — the `>=` gate IS directly guarded by `test_gate_uses_ge_not_gt` (unit) and `test_fallback_round_counter_cap_one`. The matrix remains a valuable integration check. Not weakening or removing it. |
| F7 | recovery.py described as "UNCHANGED" but is a net-new staged file `A` (evidence lens MINOR). | INFO | **NO-FIX** — semantics correct (Branch-A target unperturbed); "unchanged" means "not modified by THIS task". Note accepted. |

## ACTIONABLE FIXES (executor as single I20 writer, Step 5.G6) — INV-001 MUST NOT be touched
- F2: materialize S5A/S5B states in fsm.py (transient, terminal-overwritten).
- F3: add the "attributed"→"rereview_attributed" mapping comment.
- F4: add `test_transition_v11_edges` (dual-surface coverage of the 6 new edges).
- F5: strengthen the auggie strict-once test to exercise cross-entry double-invoke guard.
