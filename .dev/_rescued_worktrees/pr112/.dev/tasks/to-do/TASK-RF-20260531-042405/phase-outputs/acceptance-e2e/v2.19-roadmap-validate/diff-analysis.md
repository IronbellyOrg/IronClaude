---
total_diff_points: 14
shared_assumptions_count: 20
---

## Shared Assumptions and Agreements

Both variants converge on the architectural core; divergence is almost entirely about *milestone packaging and schedule*, not *what gets built*.

1. Same spec source, complexity (0.65 MEDIUM), persona (architect), `adversarial: false`.
2. Additive sub-pipeline; zero new pipeline infrastructure (NFR-050.4).
3. Reuse `execute_pipeline`, `ClaudeProcess`, `GateCriteria`, `SemanticCheck`, `gate_passed`, and import `_frontmatter_values_non_empty` from `.gates` (no duplication).
4. One-directional dependency invariant: `validate_*` → `pipeline/*` only; never the reverse (NFR-050.2 / NFR-007).
5. Single shared code path: `_build_validate_steps` returns list-of-1 (single) or list-of-N+merge (NFR-050.5).
6. Subprocess isolation chosen specifically to eliminate confirmation bias.
7. Non-blocking exit contract: warn + `tasklist_ready:false`, never exit non-zero (NFR-IMP-1).
8. Identical 7 validation dimensions with identical severity assignments (5 BLOCKING, 2 WARNING).
9. Same report schema — frontmatter fields + body sections + B/W/I finding IDs (DM-002 / FR-050.6).
10. Adversarial merge categories BOTH_AGREE/ONLY_A/ONLY_B/CONFLICT with conservative escalation.
11. `tasklist_ready` true iff `blocking_issues_count == 0`.
12. `ValidateConfig` extends `PipelineConfig` via dataclass inheritance.
13. Per-step `timeout_seconds=300`, `retry_limit=1`.
14. Identical REFLECT_GATE / ADVERSARIAL_MERGE_GATE field sets, min_lines (20/30), tiers (STANDARD/STRICT).
15. Wall-time budget ≤10% / ≤2 min single-agent (NFR-050.1).
16. Identical open-question set OQ-001..OQ-007.
17. State separation — `.roadmap-state.json` unchanged; output to `<dir>/validate/`.
18. 5 milestones; same critical-path ordering (types → gates/prompts → executor → CLI → tests).
19. Same ~10 named functional tests + import-scan + missing-file + dry-run coverage.
20. Same top-2 risks (circular-dependency regression; validation false positives) flagged High.

## Divergence Points

**1. Total timeline — 6 weeks vs 10 weeks**
Opus: variable per-milestone durations (1+1+2+1+1=6w). Sonnet: uniform 2w × 5 = 10w.
*Impact:* Opus is more aggressive and front-loads risk into a 2-week M3; if executor work slips, the whole chain slips with no slack. Sonnet's uniform allocation buys buffer but may over-budget the lighter milestones (M1 contracts as 2w looks padded).

**2. Dependency graph topology — strict chain vs DAG with cross-edges**
Opus: pure linear M1→M2→M3→M4→M5. Sonnet: adds M1→M3, M2→M4, M3→M5 cross-edges.
*Impact:* Sonnet's DAG documents real parallelism opportunities (CLI scaffolding can begin off M1 before M2 finishes). Opus's linear graph is simpler to reason about and reflects the spec's mandated §4.6 order literally, at the cost of hiding intra-milestone concurrency in prose.

**3. Where report semantics + adversarial merge live**
Opus: folds FR-050.6/FR-050.7 (report schema, merge, agreement table) **into M3 executor**. Sonnet: extracts them into a **dedicated M4** ("Report Semantics, Adversarial Merge, UX Warnings"), moving the executor up to M2.
*Impact:* Sonnet isolates the highest-semantic-risk surface (merge resolution, count recalculation, citation enforcement) into its own milestone with focused review — stronger for correctness. Opus couples merge logic to the executor that produces it, reducing hand-off seams but creating a heavier, higher-risk M3.

**4. Executor milestone placement — M3 (Opus) vs M2 (Sonnet)**
*Impact:* Opus gives the executor a clean dedicated milestone (gates/prompts settle first in M2). Sonnet co-locates executor + gates + prompts in one 18-deliverable M2, accepting a denser milestone to free M3 for CLI and M4 for semantics.

**5. Deliverable granularity — ~48 (Opus) vs ~70 (Sonnet) items**
Sonnet adds explicit resolver/factory components absent from Opus: COMP-009 (agent filename resolver), COMP-010 (model precedence resolver), COMP-011 (artifact resolver), COMP-012/013 (reflect/merge step factories), COMP-017..023, OPS-001/002/003.
*Impact:* Sonnet's decomposition makes implicit sub-tasks first-class and testable, lowering ambiguity for executors. Opus keeps these implicit inside fewer deliverables — leaner to track but relies on the implementer to infer the resolver boundaries.

**6. Open-question resolution timing — distributed vs front-loaded**
Opus: spreads OQ resolution across milestones (OQ-001 by end-M1, OQ-002/003 mid-M2, OQ-005/006/007 in M3, OQ-004 mid-M4). Sonnet: requires **all** OQ-001..007 "resolved or assigned" before M2 exit.
*Impact:* Sonnet locks the public CLI/report contract before implementation — safer against late churn. Opus resolves each OQ just-in-time at its point of need — less up-front analysis, but risks a late OQ (e.g. OQ-005 N≥3 merge) forcing M3 rework.

**7. Import-scan enforcement timing**
Opus: builds the NFR-050.2 import-scan **test in M1**, re-runs in M5 (standing CI gate from day one). Sonnet: design approved M1, **enforcement deferred to M5** (TEST-010).
*Impact:* Opus catches a circular-dependency regression the moment it's introduced. Sonnet risks a violation slipping in mid-build and only surfacing at the release gate.

**8. Gate-failure artifact policy (OQ-007) as deliverable vs mitigation**
Sonnet: dedicated deliverable OPS-003 (partial/missing-report policy). Opus: handled only inside M3 risk mitigation, no standalone deliverable.
*Impact:* Sonnet makes the warn-and-continue artifact contract a tracked, testable unit (paired with TEST-013). Opus leaves it as a risk note — lighter, but the behavior could ship under-specified.

**9. Risk register size — 8 (Opus) vs 10 (Sonnet)**
Sonnet adds R-010 (test coverage misses resume/gate-failure edge paths) and threads resume/dry-run explicitly.
*Impact:* Sonnet's extra entries map to its extra OPS/TEST deliverables — more coverage of edge paths. Opus's tighter register is easier to monitor.

**10. Highest-risk milestone — M3 (Opus) vs M1+M2 (Sonnet)**
Opus rates M3 High (executor + merge concentration). Sonnet rates M1 and M2 High (contract ambiguity + dense construction).
*Impact:* Reflects #3/#6 — Opus's risk peaks at implementation, Sonnet's at design/contract lock. Sonnet's framing favors "decide early," Opus favors "build the hard part carefully."

**11. WARNING-dimension and DM-007 priority — P0 (Opus) vs P1 (Sonnet)**
Opus marks FR-050.5e/5f (interleave/decomposition) and DM-007 (agreement row) as P0. Sonnet downgrades them to P1.
*Impact:* Opus treats the full dimension/merge surface as launch-blocking. Sonnet allows the two WARNING dims and the agreement-row contract to be deferred if schedule tightens — pragmatic descoping lever, but risks shipping without interleave/decomposition coverage.

**12. Decision Summary — plain alternatives vs scored alternatives**
Sonnet embeds numeric scores in the Decision Summary (e.g. "in-session validation (0.35), new validator engine (0.20), subprocess (0.90)"). Opus lists alternatives without scores.
*Impact:* Sonnet's scoring conveys decision confidence and audit trail despite `adversarial:false`. Opus is cleaner but conveys less of *why* the rejected options scored low.

**13. Success-criteria milestone attribution**
Opus distributes validation across the milestone where each criterion is provable (M2/M3/M4/M5/M1). Sonnet attributes nearly **all** success criteria to M5.
*Impact:* Opus enables earlier per-milestone exit verification (e.g. gate criteria provable at M2). Sonnet centralizes proof at the release milestone — simpler gate model, but defers most evidence to the end.

**14. CLI vs Report-semantics split across milestones**
Opus: CLI integration is M4 (one milestone), with semantics already absorbed in M3. Sonnet: CLI is M3, semantics is M4 — i.e. the two variants *swap* the relative order of "wire the CLI" and "perfect the report."
*Impact:* Sonnet wires the CLI before finalizing report internals (end-to-end plumbing demoable earlier, report refined after). Opus stabilizes report+executor first, then wires CLI last (CLI sees a frozen contract).

## Areas Where One Variant Is Clearly Stronger

**Sonnet stronger:**
- **Contract-lock discipline** (#6): front-loading all OQs before M2 is the safer hedge against late public-contract churn — directly mitigates the shared #2-ranked risk.
- **Edge-path coverage** (#5, #8, #9): explicit resolvers, OPS-003 gate-failure policy, and R-010 close real gaps (model precedence, partial reports, resume) that Opus leaves implicit.
- **Semantic-risk isolation** (#3): a dedicated M4 for merge/count-recalculation/citation puts the most error-prone logic under focused review.

**Opus stronger:**
- **Import-invariant enforcement from day one** (#7): a standing CI gate from M1 is unambiguously better than deferring to M5 for the explicitly High-rated circular-dependency risk.
- **Earlier verifiability** (#13): per-milestone success-criteria attribution lets each milestone gate on its own evidence rather than bottlenecking at release.
- **Schedule efficiency** (#1): 6 weeks with effort-sized milestones is more credible than uniform 2w blocks that appear padded for the lighter contract/CLI milestones.
- **Launch completeness** (#11): keeping WARNING dims + agreement-row at P0 avoids shipping with a partial dimension surface.

## Areas Requiring Debate to Resolve

1. **Timeline realism (#1):** Is 6 weeks achievable given a 2-week M3, or is Sonnet's 10 weeks the honest estimate? Resolve by effort-loading M3 deliverables against team velocity — the two estimates differ by 67%.
2. **Report-semantics boundary (#3, #4, #14):** Should adversarial merge live with the executor (Opus) or in a dedicated post-CLI milestone (Sonnet)? This is the single largest structural fork and dictates milestone risk distribution.
3. **OQ timing vs import-gate timing (#6 vs #7):** The variants each front-load *one* safety mechanism and defer the other. The strongest synthesis adopts **both** early — Sonnet's OQ front-load *and* Opus's M1 import-scan gate.
4. **P0/P1 descoping of WARNING dims and DM-007 (#11):** Are interleave/decomposition and the agreement-row contract launch-blocking? Requires a product call on whether advisory WARNING coverage is release-critical.
5. **Granularity vs trackability (#5):** Are Sonnet's ~70 deliverables actionable precision or tracking overhead versus Opus's ~48? Depends on executor autonomy — junior/parallel teams favor Sonnet's explicitness; a senior implementer may prefer Opus's leaner set.
