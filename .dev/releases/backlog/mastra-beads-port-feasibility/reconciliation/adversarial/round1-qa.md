---
topic: "Round 1 QA/ Risk Judge Verdict — Mastra/Beads Port Feasibility Panel"
type: adversarial-panel-judgment
panel_role: "QA / RISK judge — fault-finder lens"
created: 2026-06-03T01:00:00+00:00
reviews:
  - ../merged-requirements.md          # V1 — HYBRID
  - ../review/revised-recommendation.md # V2 — DEFER
  - ./diff-analysis.md                 # Diff between V1 and V2
---

# Round 1 QA / Risk Judge Verdict

## 1. Steelman

### V1 (HYBRID / Conditional Go)

V1's strongest argument: the codebase already has clean injection seams (`StepRunner` Protocol in pipeline, `claude_process_factory` in roadmap), the arithmetic on the Claude-coupled surface (~1.2K of ~73K) is literally correct, and the roadmap is structured so every phase is independently justifiable and reversible. The 5-phase strangler fig keeps the existing CLI alive as benchmark + rollback throughout. The EE licensing unknown is *named* and quarantined to Phase 5, not ignored. If Phase 0 takes <2 weeks and is truly throwaway, the cost of being wrong is bounded. V1 is fundamentally saying: "the unknowns are concentrated and gateable; buy them down while the train keeps moving."

### V2 (DEFER)

V2's strongest argument: V1 bundles three different risk profiles (seam swap, MCP service-ification, multi-tenant RBAC) into one go recommendation, and only the seam swap has strong source support. The telemetry reconstruction (`monitor.py` F2/F4/F6 bindings) is not a peripheral parser -- it is the load-bearing provenance for the entire budget/stall/error signal chain, and neither document has benchmarked whether ACP events can reproduce it. V2 also catches the flagship sequencing error (sprint should be last, not first) and the Phase 5 commercial gate that should be Phase 0. DEFER is not "never" -- it is "buy down the load-bearing unknowns in a time-boxed Phase 0 *before* committing to the multi-phase roadmap." The DEFER posture prevents the classic sunk-cost trap where four phases of engineering momentum force a bad commercial decision.

## 2. Per-Point Verdicts

### X-006: Backlog.md Role

**V1 position:** Sole task-of-record for v1.
**V2 position:** Derived mirror, not task-of-record, until a lossless MDTM round-trip is demonstrated.

**Verdict: V2's "mirror first" is a meaningful safeguard, not just delay.** The dual-source-of-truth drift failure mode is real and well-documented in the Beads section (Dolt instability, reconciliation complexity). Making Backlog.md sole task-of-record *before* demonstrating lossless round-trip creates a write-once, regret-forever scenario: if the MDTM-to-Backlog mapping loses gate/convergence semantics (which it plausibly does -- Backlog.md has no schema for them), you have tasks in the record that are structurally different from what the orchestrator thinks it is executing. V2's mirror-first approach means you write to MDTM (proven) and *also* write to Backlog.md, then diff the round-trip. If lossless, promote. If not, you still have the proven source. The cost is writing an adapter you may throw away if Backlog.md fails the gate. That is the correct asymmetry: the pain of a thrown-away adapter is orders of magnitude smaller than the pain of a corrupted task-of-record.

**V1's defense is weak here.** Its rollback path ("MDTM tasklist-index.md remains the source of truth until the mirror is proven lossless") *is* mirror-first language, contradicting its own "sole task-of-record" headline. V1 already believes V2's position but named it wrong.

### X-009: Per-Tool ACP Parity

**V1 position:** Named gate + risk (Cursor/Gemini/Copilot parity unverified, multi-tool is half the business case).
**V2 position:** De-prioritized. Claude + exactly one second tool is sufficient to prove abstraction value.

**Verdict: V2's de-prioritization is pragmatically sound but hides a business-case risk that needs its own gate.** From a pure risk-of-the-unknown perspective, V2 is correct that proving the *pattern* (ACP can abstract two tools) is sufficient to validate the architectural premise. You do not need three tools to know the abstraction works. However, the *business case* for the port is multi-tool operation, and if the two tools you pick in Phase 0 happen to be the easy ones (Claude + Codex, both named in Mastra docs), you have not proven anything about the hard ones (Cursor's ACP support, Copilot's agent mode). The risk is not technical -- it is commercial. A company investing in multi-tool parity that later discovers Cursor's ACP implementation is incompatible has wasted Phases 1-4. **Mitigation:** the Phase 0 report must explicitly list which tools were tested, which were not, and the *known* ACP support status of Cursor/Gemini/Copilot as a procurement fact (not an architectural one). This is a documentation gate, not a technical one, and V2's de-prioritization is defensible as long as the gap is named.

### Risk Register Quality

**V1 §10** has a 13-row register with likelihood/impact/mitigation columns. It is comprehensive but structurally dishonest in one critical way: it presents all risks as *parallel* when they are actually *hierarchical*. The `@mastra/acp` license risk (row 3) gates the per-tool parity risk (row 7), which gates the sprint rewrite risk (row 5), which gates the Backlog.md risk (row 8). A flat register cannot express this. If the license is EE-gated, rows 5-13 are moot. The register looks thorough but is actually a checklist that gives false comfort -- checking off row 12 (multi-tenant pilot) means nothing if row 3 failed.

**V2 reframes gates** as a prioritized sequence (licensing first, telemetry second, permission third, etc.). This is more honest because it exposes the *dependency chain* -- the gates that actually kill the project are 1-3, and everything below them is downstream. However, V2 loses the quantitative rigor of V1's likelihood/impact scoring. You cannot tell from V2's gate list whether gate 2 (telemetry reconstruction) has a 10% or 80% chance of failing.

**Verdict: V2's gate ordering is more falsifiable, V1's register is more measurable.** The ideal is V2's ordering *annotated with* V1's likelihood/impact per gate. As written, V2 gives the better picture of *what kills the project* (the first three gates) but V1 gives the better picture of *how likely each kill is*. The gap is that V2's gates lack probability estimates, making them binary (pass/fail) without telling you whether you are flipping a coin or a 95/5 shot.

## 3. Shared-Assumption Responses

### A-001: ACP Maturity/Stability

**QUALIFY.**

Neither document verifies ACP's own version stability, governance, or spec churn. They verify Mastra's `@mastra/acp` wrapper version floor (`>=1.34.0`) and Mastra's release velocity (quarterly codemods), but ACP (Agent Client Protocol) is a separate specification with its own governance. If ACP itself is pre-1.0 or under active spec revision, then every parity claim in Phase 0 is a snapshot against a moving target.

**Failure mode if false:** You prove parity against ACP v0.3 in Phase 0, spend Phases 1-3 building on it, and ACP v0.5 changes the event shape for turn boundaries, invalidating your `monitor.py` rewrite. The entire telemetry reconstruction effort -- the single highest-uncertainty technical item -- becomes a moving target you are chasing while the rest of the stack depends on it. This is not hypothetical: the research notes ACP support *requires* Mastra `>=1.34.0` while the latest known is ~1.16, meaning the version that actually supports ACP may not even be released yet. If ACP is a pre-release specification, DEFER is the only defensible position.

### A-002: Python-over-MCP Performance

**REJECT as an assumption -- it must be a measured gate.**

Neither document benchmarks per-call latency. Both *assume* the MCP/HTTP boundary is fast enough for orchestration hot-paths. The convergence 3-cycle loop, gate checks, and checkpoint enforcement are on the critical path. A Python function call taking 0.1ms becoming an MCP round-trip taking 50ms turns a 3-cycle convergence from seconds into minutes. This is not a marginal concern -- it is the difference between a developer tool that feels responsive and one that feels broken.

**Failure mode if false:** The convergence loop, which currently runs in-process and completes in bounded time, now incurs N MCP round-trips per cycle. At 50ms per call and 20 calls per cycle, that is 1 second per cycle minimum, before accounting for network jitter, serialization, or the Python-side MCP server's own GC pauses. The developer experience degrades noticeably, and the "keep Python, don't rewrite" thesis becomes a performance regression that forces a TS rewrite anyway (the exact outcome the hybrid model was designed to avoid). This is a *Phase 0 gate that is missing from both documents*.

### A-003: TS/Node Org Competency

**QUALIFY.**

V2 surfaces this as gate 5 (permanent-polyglot commitment) but neither document verifies the org's actual staffing reality. "Durable TS/Node competency" is not a binary -- it is a distribution. If the org has 2 strong TS engineers among 15 Python engineers, the "permanent polyglot" becomes a bottleneck where every TS-side change requires a hero developer.

**Failure mode if false:** The MCP server, Mastra workflows, and ACP driver all require TS/Node expertise. If this sits with 1-2 people, the hybrid stack becomes a bus-factor risk. Worse, when the Python engineers need to debug a cross-runtime failure (e.g., a gate checker returning wrong results through the MCP boundary), they cannot because the failure is in the TS serialization layer they cannot read. The project does not fail catastrophically -- it fails by attrition, as every cross-runtime bug takes 3x longer to diagnose. This is a slow failure mode that neither document's risk register captures because it is not an event -- it is a tax.

### A-004: 5% Tolerance Acceptance Gate

**REJECT -- the gate is unfalsifiable as written.**

V1 Phase 2 specifies "identical outcomes within 5% tolerance" without defining:
- **What metric?** Final artifacts (tasklist files)? Token totals? Turn counts? Gate pass/fail ratios? Wall-clock duration?
- **5% of what?** 5% absolute difference in token count? 5% of sprints producing identical outputs? 5% of tasks with divergent status?
- **Over what sample?** 2 sprints? 10? Until statistical significance?
- **Which direction?** Is old=baseline and new=variant, or is either direction a failure?

**Failure mode if false (or rather, failure mode of the ambiguity):** You run 2 sprints. Sprint A: old produces 47 tasks, new produces 44 (6.4% difference -- fail). Sprint B: old and new produce identical task lists but new takes 3x the tokens (is that a 0% or 300% difference?). The gate is so underspecified that it can be interpreted to pass or fail any result, making it a post-hoc rationalization tool rather than a decision gate. A gate that cannot reject is not a gate -- it is a rubber stamp. **This must be operationalized before Phase 2 or deleted as decorative safety theater.**

## 4. Sufficiency Challenge: When Is DEFER Wrong?

The panel must not rubber-stamp DEFER. Here is at least one concrete condition under which DEFER is the wrong call:

**If Phase 0 is genuinely <2 weeks, genuinely reversible, and the Phase 0 deliverable is *information that has value regardless of the port decision*, then DEFER and "conditional-go gated on Phase 0" are a distinction without a practical difference -- but the framing matters for organizational momentum.**

Specifically, if the Phase 0 spike produces:
1. A definitive answer on `@mastra/acp` licensing (procurement fact, valuable whether you port or not)
2. A parity report on ACP vs `ClaudeProcess` for `max_turns`/permissions/telemetry (architectural intel, valuable for future planning regardless)
3. A working thin Python ACP client against the existing `StepRunner` interface (engineering asset, immediately usable for adding ACP support to the *current* CLI without any Mastra commitment)

Then Phase 0 is not a "defer" step -- it is a **trivially-justified intelligence-gathering sprint** that would be run regardless. Calling it DEFER frames Phase 0 as a *blocker* to the roadmap, when it is actually *phase 0 of any roadmap*. The distinction between "DEFER, do Phase 0 first" and "HYBRID, conditional on Phase 0" is *semantics* if Phase 0 is throwaway, fast, and universally valuable.

**The real risk is not DEFER vs HYBRID -- it is that the framing changes expectations.** DEFER tells the org "we are not building this." HYBRID tells the org "we are building this, gated." If Phase 0 takes 2 weeks and passes, the DEFER org needs a second decision meeting to restart momentum. The HYBRID org continues. That organizational friction is the *only* substantive difference, and it matters if the org has short institutional memory or competing priorities.

**However**, there is a second condition where DEFER is clearly wrong: **if the cost of *not* exploring ACP parity is higher than the cost of Phase 0**. If the Claude Code CLI is actively losing market position to multi-tool competitors, and ACP is the known standard for multi-tool integration, then every week of DEFER is a week of competitive exposure. The Phase 0 spike is not just architecture research -- it is competitive intelligence.

## 5. Overall Verdict

**V2's corrections to V1 are evidence-backed and must be adopted wholesale:**
- Flagship order reversal (sprint last) -- source-verified
- Commercial gate moved to Phase 0 -- logically necessary
- 1.2K headline reframed to behavioral coupling -- source-verified
- Backlog.md as mirror-first -- structurally safer

**V2's DEFER recommendation is *procedurally* correct but *organizationally* fragile.** DEFER is the right posture *if* Phase 0 is treated as a prerequisite to any commitment. But as the sufficiency challenge demonstrates, Phase 0 has standalone value and is fast/reversible, making the DEFER framing potentially paralyzing for an org that needs momentum to prioritize work.

**The most honest recommendation is: RUN Phase 0 as a standalone, time-boxed (2-week), throwaway intelligence sprint with explicit pass/fail criteria on the six gates from V2 §4. The output is a report, not a port. Based on the report, the go/defer/no-go decision is trivially determined. This is what V2 calls DEFER and V1 calls HYBRID -- they are the same action with different framing.**

**I judge V2's *substance* as superior but its *recommendation label* as organizationally risky. V1's label (HYBRID) is organizationally healthier but its substance (sprint-first, sole-task-of-record, flat risk register) is demonstrably weaker.**

## 6. Recommended Base

**Merge base: V1's structure + V2's corrected judgments.** V1 provides the executable scaffolding (roadmap, component matrix, what-is-lost table) that V2 only revises but never restates. V2 provides the source-verified corrections, the reordered gates, and the risk calibration. The merged document should be V1's 12-section structure with V2's judgments grafted in:

- Sections 1-2: V1 as written, with V2's 1.2K reframing and behavioral coupling correction added as a callout box
- Section 3: V1 as written, with ACP maturity caveat (A-001) added
- Section 4: V1 component matrix, updated with V2's sprint-seam-cleanliness correction
- Section 5: V1 as written, with A-002 (MCP performance) added as a Phase 0 gate
- Section 6: V2's mirror-first position replaces V1's sole-task-of-record
- Section 7: V1 as written
- Section 8: V1 as written
- Section 9: V2's revised phase ordering (pipeline first, sprint last, commercial gate in Phase 0)
- Section 10: V1's 13-row register, re-ordered by V2's gate hierarchy, with A-004 (5% gate) flagged as requiring operationalization
- Sections 11-12: V2's gate ordering replaces V1's open questions; recommendation labeled as "Phase 0 intelligence sprint -- report determines go/defer"

This base honors V2's evidence while preserving V1's structural completeness, and resolves the DEFER-vs-HYBRID framing conflict by naming Phase 0 as a standalone intelligence sprint rather than a blocker.
