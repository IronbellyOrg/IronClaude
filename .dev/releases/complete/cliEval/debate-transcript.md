---
convergence_score: 0.78
rounds_completed: 2
---

# Adversarial Debate Transcript

## Round 1 — Initial Positions

### Variant A (Opus) — Opening Statement

**Position on milestone granularity (D1):** A 6-milestone breakdown is essential. Separating Reporter (M3) from CLI surface (M4) lets the reporter's N′-vs-K contract land and be exercised through integration tests before flag wiring obscures whether failures originate in the reporter or the CLI. Folding hardening into the release milestone (Haiku's M5) conflates "harness works" with "harness is documented and signed off" — two distinct gates with different reviewers.

**Position on CLI placement (D2):** CLI must land in M4, *after* reporter and orchestrator. Stub flags written against unknown reporter exit codes and absent disk-budget semantics create churn. `--max-disk-mb` cannot be specified honestly until NFR-PERF4's polling loop exists; `--junit` cannot be wired until DM-012 freezes the JSON schema. Front-loading CLI is theater — the contract isn't real until backing code exists.

**Position on Expect DSL placement (D3):** Same logic — DSL primitives depend on `EvalContext` (DM-010) which depends on `HomeIsolation` (M2) and `EvalRunner` (M3). Authoring manifests against an unstable assertion shape forces rework.

**Position on deliverable enumeration (D4):** 99 deliverables with per-primitive (COMP-010.1–6) and per-eval (E1, E2.1–3, E3–E15) tracking gives reviewers precise per-batch DoD. Haiku's batching under TEST-010/011/012 hides which specific primitive or eval body slipped.

**Position on risk consolidation (D9):** R1–R9 with cross-milestone reuse is the cleaner project surface. Haiku's RR-001..RR-015 double-counts the same disk/RAM concern (RR-008, RR-011) and the same scope-creep concern (RR-002, RR-015), inflating the register without adding signal.

**Position on timeline (D12):** 28 working days is honest about the harness work being ~3.5 days per design-spec §0, plus 7 days for evals. Haiku's 6 calendar weeks pads schedule without naming what the extra week buys.

### Variant B (Haiku) — Opening Statement

**Position on milestone granularity (D1):** 5 milestones map cleanly to calendar weeks and align deliverable boundaries to natural review checkpoints. A standalone M6 for "hardening + ADR sign-off" is bureaucratic overhead — ADRs should be signed at the milestone where the decision crystallizes, not deferred to a final gate.

**Position on CLI placement (D2):** Establishing the CLI contract in M1 is correct because the CLI *is* the public surface. Stakeholders review CLI flags before implementation cost is sunk. Opus's "stub-flag drift" concern is mitigated by treating M1 flags as a contract artifact — they get amended in later milestones if backing components reveal gaps, but the conversation about the contract happens *before* code is written.

**Position on Expect DSL placement (D3):** The DSL *interface* (COMP-010) must land in M1 so manifest authors can begin shaping `expects:` blocks immediately. Implementation of primitives lands in M3 where `EvalContext` is real. Opus conflates interface and implementation.

**Position on license/NOTICE timing (D6):** This is non-negotiable: OQ-4 must gate M1 entry. Vendoring ptytest under M2 without resolved NOTICE/LICENSE attribution creates a release-blocking audit risk. Opus's M6 placement means ptytest sits in the tree for 4 milestones without complete attribution.

**Position on test deliverable surfacing (D10):** TEST-001..TEST-016 as first-class enumerable deliverables creates an auditable QA trail. Opus's "embedded in AC" approach makes test coverage invisible to roadmap-level review — you cannot answer "is this milestone tested?" without reading every AC field.

**Position on eval body window (D12):** 2 weeks for E1–E15 is realistic. OQ-2 leaves E3–E15 bodies undefined; assuming 7 days for authoring undefined evals is optimism, not estimation.

**Position on OQ resolution timing (D5):** Concentrating blocking OQs (OQ-1/3/4/7/8/10) as M1 entry blockers prevents mid-milestone contract churn. Opus's "parallel resolution" risks discovering a contract gap in M4 that invalidates M1–M3 work.

---

## Round 2 — Rebuttals

### Variant A (Opus) — Rebuttal

**Rebutting Haiku on D1 (milestone count):** "Bureaucratic overhead" misframes M6. The distinction is not redundant signing — it's that "harness works at --parallel 8" (M5 exit) and "harness has signed ADRs, NOTICE, PROVENANCE, sync gate, macOS roadmap entry" (M6 exit) are independent observables. Bundling them risks releasing with green tests but unsigned decisions, which is exactly the SC1/SC5 failure mode the spec calls out.

**Rebutting Haiku on D2 (CLI placement):** "Flags as a contract artifact" still requires a stable mental model of what flags exist. OQ-7 (--junit) is unresolved at M1 entry under Haiku's own plan — so Haiku's M1 lands a CLI surface that *omits* a flag the spec conditionally requires, then either back-fills in M4 (drift) or removes from spec (also drift). Opus's M4 placement waits until OQ-7 resolution can be enforced atomically.

**Rebutting Haiku on D6 (NOTICE timing):** Concede the audit-risk framing — but Haiku's "M1 entry blocker" is too rigid. NOTICE/LICENSE can be resolved in parallel with M1 *if* the vendored ptytest does not land until M2. Opus's M6 placement is the wrong end of the spectrum; the correct fix is to add OQ-4 as a *M2 entry blocker* (when vendoring physically happens), not M1. **Partial concession.**

**Rebutting Haiku on D10 (test enumeration):** TEST-001..016 as standalone deliverables creates a parallel ledger that drifts from the AC fields they validate. When a deliverable's AC changes mid-milestone, the corresponding TEST-XXX entry must also be updated — Haiku's structure doubles the maintenance surface. Opus's embedding keeps test definition next to the contract it verifies.

**Rebutting Haiku on D12 (eval window):** OQ-2 resolution is a *prerequisite* to M5 entry under both plans. If OQ-2 is closed before M5, 7 days is sufficient because the eval bodies are then specified. If OQ-2 is *not* closed, neither 7 days nor 14 days suffices — you cannot author undefined evals. Haiku's 14-day allocation is hedging against process failure, not estimation honesty.

**Rebutting Haiku on D5 (OQ concentration):** Hard-blocking M1 entry on 6 OQs assumes maintainer availability to close them synchronously. Real projects close OQs as their concrete impact surfaces — OQ-10 (MCP retry semantics) cannot be meaningfully resolved until E1/E2 evals expose actual MCP flakiness patterns in M5. Haiku's plan forces theoretical resolution of OQ-10 in M1 when empirical resolution in M5 is more honest.

### Variant B (Haiku) — Rebuttal

**Rebutting Opus on D1 (milestone count):** The "two distinct gates" argument is preserved in Haiku's structure — M5 exit criteria explicitly include ADR sign-off (OPS-005 release checklist). Adding M6 doesn't strengthen the gate; it adds a transition cost. The real risk Opus names (SC1/SC5 failure) is mitigated by exit-criteria specification, not milestone proliferation.

**Rebutting Opus on D2 (CLI placement):** Opus's OQ-7 argument is exactly why Haiku gates OQ-7 as an M1 entry blocker. Under Haiku's plan, OQ-7 *cannot* be unresolved at M1 start — the CLI surface lands with --junit either in or out, decided before code. Opus's "wait until M4" approach delays the contract conversation, not avoids it.

**Rebutting Opus on D6 (NOTICE timing):** Accepting Opus's partial concession — M2 entry blocker is acceptable as long as it's *before* vendoring. The dispute reduces to scheduling, not principle. **Convergence.**

**Rebutting Opus on D10 (test enumeration):** "Doubled maintenance surface" is real but worth the cost. When a deliverable's AC changes, the TEST-XXX entry *must* be reconsidered — that's the audit value, not overhead. Opus's embedded model has the opposite failure mode: AC fields drift silently and nobody notices the test coverage hole. The maintenance cost is the feature.

**Rebutting Opus on D12 (eval window):** Opus assumes OQ-2 resolution produces fully-specified eval bodies. In practice, eval body authoring includes: (1) writing the eval YAML, (2) running it locally, (3) tuning Expect primitives until pass/fail is stable, (4) capturing artifacts, (5) reviewing telemetry. 7 days for 15 evals = 0.47 days/eval including all 5 steps — unrealistic. 14 days = 0.93 days/eval is closer to actual eval-authoring velocity in similar harnesses.

**Rebutting Opus on D5 (OQ concentration):** Concede OQ-10 specifically — empirical resolution in M5 is more honest. But OQ-1, OQ-3, OQ-4, OQ-7, OQ-8 are all *contract-shaping*, not empirical. They can and should resolve before contract code lands. **Partial concession.**

---

## Convergence Assessment

### Areas of Agreement (after debate)

1. **D6 (NOTICE/LICENSE timing):** Both variants converge on M2 entry blocker (before ptytest vendoring physically lands), rejecting Opus's M6 placement and Haiku's M1 placement as too late and too early respectively.
2. **D5 (OQ resolution timing):** Both variants agree contract-shaping OQs (OQ-1, OQ-3, OQ-4, OQ-7, OQ-8) should resolve before M1 exit; empirical OQs (OQ-10 MCP retry) can resolve in the milestone where evidence surfaces (M5).
3. **D9 (risk register):** No formal convergence, but Opus's consolidation argument is stronger; recommend consolidating RR-008/RR-011 (disk/RAM) and RR-002/RR-015 (scope creep) regardless of which variant's structure is adopted.
4. **Shared baseline:** 14 shared assumptions remain unchallenged — security-first ordering, ThreadPoolExecutor concurrency, IsolationLayers extension, reporter contract, vendored ptytest, three-tier capability gates, single-pass retry, `.dev/eval-runs/` artifacts, hook-matcher coverage gate.

### Remaining Disputes

1. **D1 (milestone count, 5 vs 6):** Unresolved. Opus argues separate hardening gate prevents SC1/SC5 failure; Haiku argues exit-criteria specification achieves the same outcome without a milestone boundary. **Resolution requires maintainer preference on review-gate granularity.**
2. **D2 (CLI placement, M1 vs M4):** Unresolved. Haiku's argument hinges on OQ-7 being closable in M1; Opus's argument hinges on flag stability requiring backing components. **Resolution depends on maintainer availability for OQ-7 sign-off before M1 start.**
3. **D3 (Expect DSL placement):** Partially converged — Haiku clarified interface vs implementation. Recommend: DSL *interface* in M1 (Haiku) + *primitives* in M3/M4 (compromise).
4. **D4/D10 (deliverable + test enumeration):** Unresolved. Reflects philosophical difference between PR-driven tracking (Opus, embedded AC) and roadmap-driven tracking (Haiku, first-class deliverables). **Resolution depends on whether QA system is roadmap-audited.**
5. **D12 (eval window, 7 vs 14 days):** Unresolved. Opus's argument is theoretically clean; Haiku's argument matches observed eval-authoring velocity. **Resolution should default to Haiku's more conservative estimate given OQ-2 uncertainty.**
6. **D7 (effort sizing semantics):** Unresolved but low-stakes — day-level vs week-level is presentation, not substance.
7. **D11 (SuiteLoader effort L vs M):** Unresolved but low-stakes — single deliverable sizing.

### Convergence Score Rationale

**0.78** reflects:
- Strong agreement on 14 shared assumptions (security architecture, technical primitives, contracts)
- Partial convergence on D3, D5, D6 during debate
- Genuine remaining disputes on D1, D2, D4/D10, D12 that turn on maintainer/process preferences rather than technical correctness
- No variant exposed a fundamental flaw in the other; both are defensible roadmaps with different optimization targets (Opus: implementation sequencing rigor; Haiku: contract-first stakeholder alignment)

### Recommended Merge Posture

The two variants are complementary rather than contradictory. A merged roadmap should:
- Adopt Haiku's M1 CLI-contract framing (D2) **only if** OQ-7 closes before M1 start; otherwise adopt Opus's M4 placement
- Adopt Haiku's first-class TEST-XXX deliverables (D10) for auditability
- Adopt Opus's per-primitive/per-eval enumeration (D4) for tracking granularity
- Adopt the compromise on D3 (interface M1, primitives M3/M4)
- Adopt Haiku's 14-day eval window (D12) given OQ-2 uncertainty
- Adopt Opus's 6-milestone structure (D1) **only if** maintainer wants a distinct release-readiness gate; otherwise Haiku's 5-milestone structure with explicit M5 exit criteria is sufficient
- Adopt the converged M2-entry placement for OQ-4/NOTICE (D6)
- Consolidate the risk register per Opus's structure (D9) regardless of milestone count
