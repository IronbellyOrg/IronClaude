---
total_diff_points: 14
shared_assumptions_count: 18
---

# Cross-Framework Deep Analysis — Roadmap Variant Diff (Opus-Architect vs Sonnet-Architect)

Both variants decompose the identical 8-phase analytical sprint spec (complexity 0.85 HIGH, architect persona, non-adversarial base). They agree on nearly all *content* and diverge almost entirely on *milestone packaging, sequencing of verification, and registry granularity*. The Opus variant is a 1:1 phase-to-milestone mapping (8 milestones, 13 weeks); the Sonnet variant consolidates into 5 coarser milestones (12 weeks).

## 1. Shared Assumptions and Agreements

|#|Shared assumption|
|---|---|
|1|Complexity 0.85 / HIGH; architect persona; `adversarial: false`; no base variant or convergence score|
|2|Strict-sequential phase-gate orchestration via the superclaude sprint CLI is the control plane|
|3|llm-workflows is a **frozen reference** — path-verify only, no implementation changes|
|4|Auggie MCP is the mandated primary code-reader; Serena `get_symbols_overview` + Grep/Glob is the annotated fallback|
|5|"Adopt patterns not mass" R-RULE — adopt control/validation patterns, exclude bash/shell machinery|
|6|Anti-sycophancy: every strength must carry a paired weakness/cost (100% target)|
|7|Scope is exactly 19 components — 8 IronClaude (COMP-001..008) + 11 llm-workflows (COMP-009..019)|
|8|The **same 8 enumerated comparison pairs** (4a–4h) with identical pairings|
|9|`improvement-backlog.md` → `/sc:roadmap`; `final-improve-plan.md` → `/sc:tasklist` (downstream consumers, not milestones)|
|10|DM-001 backlog item schema — **field-for-field identical** (id/component/title/priority/effort/pattern_source/rationale/file_targets/acceptance_criteria/risk/patterns_not_mass_verified)|
|11|DM-002 phase-gate contract + DM-003 gate-criteria row contract, same field definitions|
|12|Artifact-root ambiguity (`.dev/releases/current/...` vs bare `artifacts/...`) is the dominant pre-M1 risk|
|13|Phase 2 and Phase 3 are parallelizable *within* the strategy milestone but both must gate the comparison milestone|
|14|"No clear winner" and "discard both" are explicitly valid verdicts (documented as "no adoption; why")|
|15|Five 100%-coverage NFR verification targets (Auggie-primary, anti-sycophancy pairing, citation verifiability, patterns-not-mass, restartability)|
|16|Zero production-code change; trivial rollback (delete artifacts directory)|
|17|Deterministic §5.2 per-phase minima govern gate enforcement; "35+ artifacts" is informational only|
|18|Both repos must be readable; `/sc:adversarial` is the required comparison engine; reference inputs (`prompt.md`, merged spec, spec template) available|

## 2. Divergence Points

**1. Milestone granularity (8 vs 5)**
- Opus: M0–M7, one milestone per spec phase plus a dedicated foundation milestone.
- Sonnet: M1–M5, consolidating adjacent phases into composite milestones.
- Impact: Opus gives finer gate-by-gate traceability and per-phase risk isolation at the cost of more milestone overhead; Sonnet is leaner to manage but couples two spec phases per milestone, blurring per-phase checkpoint accountability.

**2. Foundation milestone: standalone (Opus M0) vs folded (Sonnet M1)**
- Opus carves gate-contract authoring + artifact-root fix + restartability proof into its own M0 before any inventory work.
- Sonnet folds contracts (DM-002/DM-003) and artifact-root resolution into M1 alongside the inventory.
- Impact: Opus enforces "infrastructure before artifacts" as a hard gate (cannot inventory until gate machinery is proven); Sonnet risks interleaving contract authoring with inventory work, but saves a milestone boundary.

**3. Synthesis vs improvement-plan separation**
- Opus splits into M4 (merged synthesis) and M5 (prioritized improvement plan) — two gates.
- Sonnet combines both into M4 (Synthesis and Improvement Planning) — one gate.
- Impact: Opus gates the "rigor without bloat" synthesis independently before plan authoring begins, catching synthesis defects earlier; Sonnet's combined milestone is 3 weeks and defers any synthesis/plan split-check to a single exit gate.

**4. Validation vs assembly separation**
- Opus splits into M6 (adversarial validation, typed **Quality**, P0) and M7 (artifact assembly, **Integration**, P1).
- Sonnet combines into M5 (Validation, Assembly, and Downstream Readiness).
- Impact: Opus elevates adversarial validation to a discrete quality gate that must pass before assembly; Sonnet treats validation as the first step inside an assembly milestone, lowering the visibility of validation as an independent pass/fail boundary.

**5. Restartability (NFR-5) verification timing**
- Opus verifies `--start` resume on a no-op gate in **M0** (earliest possible).
- Sonnet defers NFR-XFDA.5 verification to **M5** (final milestone).
- Impact: This is the most consequential sequencing difference. Opus proves crash-resilience before 12 weeks of artifacts exist; Sonnet discovers any resume defect only at the end, when a non-resumable sprint is most expensive to remediate.

**6. Artifact-root resolution deadline**
- Opus: resolve OQ-ROOT "Before M1 (M0 exit)".
- Sonnet: resolve OI-4 "Before M1 **start**".
- Impact: Functionally close, but Sonnet treats it as a hard precondition to launching M1 at all, whereas Opus allows M0 work to begin and resolves root within M0 — Opus's framing permits some M0 contract drafting before the root is fixed.

**7. Open-question ID scheme**
- Opus: mixed namespace — OI-1/2/3, OQ-ROOT, OQ-PAIRSET, OQ-COUNTS, GAP-1/2/3.
- Sonnet: unified OI-1 through OI-6 (OI-4 = root, OI-5 = pair set, OI-6 = count authority).
- Impact: Sonnet's flat scheme is cleaner to track; Opus's semantic IDs (OQ-ROOT, OQ-PAIRSET) are more self-documenting but cross-reference less uniformly. Pure traceability/bookkeeping difference, no behavioral effect.

**8. Component priority differentiation**
- Opus: every COMP row is **P0**.
- Sonnet: tiers components P0/P1/P2 (e.g., COMP-002 P1, COMP-014/015/016 P2).
- Impact: Sonnet encodes adoption-likelihood/centrality into priorities, useful if the sprint must triage under time pressure; Opus treats all 19 inventories as equally mandatory, which is defensible since the gate requires all 19 regardless — Sonnet's tiers have no effect if every component is still gate-required.

**9. Risk-register granularity (10 vs 17)**
- Opus: R1–R10.
- Sonnet: R-001–R-017, splitting strategy-bias, citation-quality, shell-overfit, and field-completeness into distinct rows.
- Impact: Sonnet surfaces more failure modes explicitly (better for a risk-averse reviewer); Opus is more compact and folds related risks. No contradiction — Sonnet is a superset.

**10. Explicit parent-FR closure item**
- Sonnet adds a discrete M5 item `FR-XFDA-001` (Feature acceptance closure: 8 child FRs traced, 6 NFRs validated, 19 components, 3 contracts).
- Opus has no standalone parent-FR closure row; it relies on M7 traceability + NFR-6 backlog interoperability.
- Impact: Sonnet gives an auditable single "feature done" assertion; Opus's end-to-end traceability is distributed across the M7 artifact-index check, which is functionally equivalent but lacks one consolidated acceptance row.

**11. Total duration (13 vs 12 weeks)**
- Opus 13 weeks (M0 adds a week); Sonnet 12 weeks.
- Impact: The entire delta is M0. Same per-phase effort otherwise; Opus "spends" one week buying an explicit foundation gate.

**12. Comparison-pair "≥8" resolution path**
- Opus: fixes the set in M0 via OQ-PAIRSET; M3 gate min_artifacts derived there.
- Sonnet: resolves via OI-5 "before M3 exit", gating extra pairs as "approved only if explicitly accepted".
- Impact: Opus locks scope earliest (no ad-hoc pair surprises downstream); Sonnet leaves the door open to bounded expansion until M3, trading early certainty for late flexibility.

**13. Deliverable-count semantics**
- Opus milestone table lists granular deliverable counts (M1=22, reflecting the 19 COMP rows + 3 inventory artifacts as discrete items).
- Sonnet lists consolidated counts (M1=23 including DM rows) and rolls COMP rows differently.
- Impact: Cosmetic/bookkeeping; both cover the same 19 components + contracts, counted under different rollup conventions.

**14. Adversarial validation typing/emphasis**
- Opus types M6 as a **Quality** milestone (P0) — adversarial validation is a first-class phase.
- Sonnet models validation as `FR-XFDA-001.7` inside a **Validation** pipeline milestone with assembly.
- Impact: Opus signals validation as an independent quality stage with its own owner/gate; Sonnet integrates it into the closing pipeline, which can compress the schedule but reduces the structural prominence of the adversarial check.

## 3. Areas Where One Variant Is Clearly Stronger

|Area|Stronger variant|Why|
|---|---|---|
|Crash-resilience assurance|**Opus**|Proves `--start` resume in M0 before any artifacts exist; Sonnet discovers resume defects only at M5 when remediation is costliest (Divergence 5)|
|Early scope-locking|**Opus**|Pair set (OQ-PAIRSET) and artifact root both fixed in M0, eliminating downstream path/scope drift before inventory begins (Divergences 6, 12)|
|Independent quality gating|**Opus**|Synthesis, plan, validation, and assembly are four separate gates (M4–M7), catching defects at the earliest stage they can appear (Divergences 3, 4, 14)|
|Risk visibility|**Sonnet**|17 enumerated risks expose more discrete failure modes (strategy bias, citation variance, shell overfit, field completeness) for a risk-averse reviewer (Divergence 9)|
|Operational leanness|**Sonnet**|5 milestones / 12 weeks reduce milestone-boundary overhead with one fewer week and fewer gate transitions (Divergences 1, 11)|
|Explicit feature acceptance|**Sonnet**|Dedicated FR-XFDA-001 closure row gives one auditable "all child FRs/NFRs/components/contracts traced" assertion (Divergence 10)|
|Priority triage signal|**Sonnet**|P0/P1/P2 component tiers aid time-pressured triage (though weakened by all-components-gate-required) (Divergence 8)|

## 4. Areas Requiring Debate to Resolve

|#|Question for debate|Why it needs resolution|
|---|---|---|
|1|Should restartability be proven up front (Opus M0) or at sprint close (Sonnet M5)?|Highest-leverage divergence — determines whether a non-resumable sprint is caught on day 1 or week 12. Strong argument for Opus's early proof; the only cost is sequencing the no-op gate test before real work.|
|2|8 fine-grained milestones vs 5 composite milestones?|Trades per-phase gate accountability (Opus) against management overhead (Sonnet). Must pick the milestone model before either roadmap can proceed.|
|3|Standalone M0 foundation (+1 week) vs folded into inventory?|The entire duration delta. Debate whether the explicit "infrastructure before artifacts" gate justifies the extra week.|
|4|Separate validation/assembly gates (Opus M6/M7) vs combined (Sonnet M5)?|Determines whether adversarial validation is an independent pass/fail boundary or an embedded pipeline step — affects how scope-creep/citation failures are caught and corrected.|
|5|Component priority: uniform P0 (Opus) vs tiered P0–P2 (Sonnet)?|Tiers only matter if the gate ever permits partial completion; if all 19 are mandatory, tiers are inert. Resolve whether triage flexibility is real or cosmetic.|
|6|Unify the open-question ID scheme (OI-* vs OQ-/GAP-/OI- mix)?|Low-stakes but should be standardized before merge to keep cross-references uniform across artifacts.|
|7|Add an explicit parent-FR closure item (Sonnet) to the Opus structure?|Opus's distributed M7 traceability is equivalent but lacks one consolidated acceptance assertion — debate whether to graft Sonnet's closure row in.|
