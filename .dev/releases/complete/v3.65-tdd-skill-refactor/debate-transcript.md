---
convergence_score: 0.72
rounds_completed: 1
---

# Structured Adversarial Debate: TDD Skill Refactor Roadmap

## Round 1: Key Divergence Points

---

### Topic 1: BUILD_REQUEST Wiring Timing

**Variant A (Opus):**
Deferring path rewrites to Phase 3 is non-negotiable from a correctness standpoint. You cannot wire references to files that don't exist yet. If extraction of `refs/validation-checklists.md` fails mid-Phase-2 while `build-request-template.md` already has rewritten paths pointing to it, you have a broken artifact with no rollback path. My approach eliminates this entire failure class by construction: Phase 2 extracts verbatim, Phase 3 wires after all targets are confirmed to exist. The cost is one additional pass over `build-request-template.md` — a 15-minute task. The benefit is that Phases 2 and 3 each have clean, independently verifiable gates.

**Variant B (Haiku):**
The risk Opus describes is theoretical. All 5 extractions are mechanical copy operations from verified line ranges. The probability of one extraction succeeding while another fails is near zero — they're the same operation repeated on different ranges. Bundling the 6 path rewrites into Phase 1 (M1.2) alongside extraction means we touch `build-request-template.md` exactly once: extract it, apply the 6 substitutions, done. A second pass is wasted effort and creates its own risk — you now have a phase where the template exists with stale references, and anyone inspecting the repo between Phase 2 and Phase 3 sees an inconsistent state.

**Assessment:** Opus wins on safety principle. Even if the failure probability is low, the cost of separation is trivial (15 minutes) and the failure mode it prevents — partial-state broken references — is exactly the kind of silent defect the spec identifies as highest risk. Haiku's "touch once" efficiency argument is valid but subordinate to correctness guarantees in a fidelity-critical refactor.

---

### Topic 2: When to Define the Phase Loading Contract

**Variant B (Haiku):**
Contract-first is an established architectural principle for good reason. By defining the loading contract in Phase 0 (M0.2, M0.3) — before any content moves — we ensure that extraction is guided by the contract rather than the contract being retrofitted to match whatever extraction produced. If you defer contract design to Phase 4 as Opus does, you risk discovering a contract violation after 3 phases of work are complete. Front-loading costs 0.5 days but eliminates rework risk. The contract is simple (a 4-row matrix); designing it early is cheap.

**Variant A (Opus):**
The contract is indeed simple — which is precisely why it doesn't need a dedicated early phase. The loading matrix is fully specified in the spec (Section 5.3). There's nothing to "design" — it's a transcription of known requirements into SKILL.md. I place it in Phase 4 because that's when SKILL.md is being rewritten, and embedding the declarations is part of the rewrite. Creating a "baseline contract" in Phase 0 that then gets transcribed into SKILL.md in Phase 4 is redundant work. The contract doesn't inform extraction — extraction is driven by block-to-file mapping from the fidelity index, not by loading rules.

**Assessment:** Haiku has the stronger architectural argument but overstates the practical benefit. The contract is already fully defined in the spec — Phase 0 would be ratifying it, not designing it. However, having the contract explicitly documented before migration starts does provide a useful cross-check: after Phase 2, you can verify that the extracted files match the contract's expectations. A lightweight compromise — document the contract in Phase 1 verification without giving it a full phase — captures Haiku's benefit without Haiku's overhead.

---

### Topic 3: Timeline Calibration (3-4 hours vs. 3.5-5 days)

**Variant A (Opus):**
This is a mechanical refactor at complexity 0.53. The operations are: count lines, verify ranges, copy text blocks to new files, apply 6 string replacements, delete moved blocks, add loading directives, run sync. Every task is deterministic. There are no design decisions, no API changes, no behavioral modifications. A single Claude session can execute this in 3-4 hours with parallel extraction in Phase 2. The spec itself characterizes this as MEDIUM complexity. Multi-day estimates belong to feature development, not procedural content relocation.

**Variant B (Haiku):**
Opus's estimate assumes zero surprises — that OQ-1 resolves cleanly, that all line ranges match, that no unmapped content is discovered, that sync tooling handles the new `refs/` directory without issues. The spec identifies 5 risks, 3 at HIGH severity. My estimate includes buffer for: OQ resolution requiring fidelity index rework (half a day), discovery of unmapped lines requiring re-extraction (half a day), and a full day for fidelity certification which Opus allocates only 30-45 minutes. Additionally, my estimate accounts for human review cycles — someone should review each phase's output before proceeding.

**Variant A (Opus):**
Your review-cycle buffer is for a team workflow. The spec doesn't specify team execution. In a single-agent execution context — which is how this will actually be run — review is integrated into verification gates. The OQ resolution buffer is valid but bounded: `wc -l` takes seconds, and re-anchoring ranges is 30 minutes of work even in the worst case. Your "full day for fidelity certification" includes work I've distributed across per-phase gates — I'm not deferring verification, I'm doing it incrementally.

**Assessment:** Both are right for their assumed execution context. For single-agent (Claude session) execution: 3-4 hours is realistic, possibly generous. For team execution with review gates: 3.5-5 days is reasonable. The roadmap should state its assumed execution context explicitly. Given this project's tooling (Claude Code, `make sync-dev`), single-agent execution is the likely context, favoring Opus's estimate.

---

### Topic 4: Line-Count Authority

**Variant A (Opus):**
I commit to 1,387 because the actual file exists and can be measured. Planning around an ambiguous number wastes effort. If I'm wrong, Phase 1's first task (`wc -l`) catches it in seconds and all ranges are re-anchored — but at least the rest of the roadmap has concrete ranges to work from rather than hedged language. Haiku's Phase 4 still references "lines 1–1364" — that's not caution, that's an unresolved inconsistency propagated through the entire plan.

**Variant B (Haiku):**
I treat OQ-1 as open because a roadmap should not assume answers to open questions. The correct approach is to resolve ambiguity in Phase 0, then proceed with the verified answer. If I assumed 1,387 and the fidelity index's 1,364 was correct (perhaps the file was modified between index creation and now), every range in my plan would be wrong. My references to "1–1364" are admittedly inconsistent — they should say "1–N where N is resolved in Phase 0" — but the principle of not baking in assumptions is sound.

**Assessment:** Opus is pragmatically correct. A roadmap with concrete numbers is more actionable than one with variables. The file can be measured in the first task of Phase 1. Haiku's principle is valid but the execution is flawed — referencing "1–1364" throughout while claiming the number is unresolved is worse than either committing to a number or consistently using a variable. Opus's approach with an explicit Phase 1 verification step is the right balance.

---

### Topic 5: Verification Gate Structure

**Variant B (Haiku):**
Named gates (A through D) that group cross-cutting concerns are superior for audit and review. Gate C (Fidelity and semantic immutability) groups criteria 5, 6, 7, 8, 11, 12 — all fidelity concerns — regardless of which phase produced them. This makes it trivial for a reviewer to answer "is fidelity proven?" by checking one gate. Opus's per-phase gates make execution easy but review hard: to answer the same question, a reviewer must check Phase 2, Phase 3, and Phase 5.

**Variant A (Opus):**
Per-phase gates are executable. When I finish Phase 2, I know exactly what to verify before starting Phase 3. Your named gates span phases — Gate C depends on outputs from Phase 1, Phase 3, and Phase 4. When does a reviewer actually run Gate C? After Phase 4? Then you've deferred fidelity verification past the point where fixes are cheap. My approach verifies fidelity incrementally: after extraction (Phase 2 gate), after wiring (Phase 3 gate), and comprehensively (Phase 5 gate). Problems are caught early.

**Assessment:** Both structures are valid for different purposes. The ideal approach combines them: per-phase gates for execution (Opus), with a cross-cutting gate summary table for review (Haiku). This is an additive merge, not a choice. Opus's Phase 5 success criteria table already approximates Haiku's gate groupings.

---

### Topic 6: Precedent Pattern Awareness

**Variant A (Opus):**
Identifying R6 — that this refactor pioneers the refs pattern rather than following an established one — is architecturally significant. Haiku references `sc-adversarial-protocol/refs/` as a "tooling dependency" without verifying it exists. If an implementer follows Haiku's plan and looks for that reference implementation, they'll find nothing, wasting time and creating confusion. My plan names the risk and scopes it correctly (LOW — the pattern is simple).

**Variant B (Haiku):**
I reference the adversarial-protocol refs pattern because the spec cites it as the precedent. If it doesn't exist in the codebase, that's a spec defect, not a roadmap defect. My plan correctly follows the spec's references. However, I concede that Opus's observation is useful — noting the absence of precedent helps implementers set expectations.

**Assessment:** Opus is clearly stronger here. A roadmap should validate its own assumptions rather than propagating potentially incorrect spec references. Noting the absence of precedent is a valuable architectural insight.

---

## Convergence Assessment

### Areas of Agreement (Strong Convergence)

1. **5-phase structure with sequential gating** — both agree on the fundamental approach; differences are in phase boundaries and bundling, not philosophy.
2. **Fidelity as a blocking gate** — zero drift policy, checksum markers, and release-blocking treatment are identical.
3. **Same 5 risks, same severity ratings** — risk identification is fully converged.
4. **Same 14 success criteria** — validation targets are identical.
5. **Same 5 refs files** — decomposition target is identical.
6. **Phase loading contract content** — the matrix itself is agreed; only timing of its documentation differs.
7. **OQ resolution as prerequisite** — both block migration on OQ closure.

### Areas of Partial Convergence (Mergeable)

8. **Verification structure** — per-phase gates (Opus) + cross-cutting gate groupings (Haiku) are complementary, not conflicting. Merge by adding Haiku's Gate A-D summary to Opus's per-phase structure.
9. **Integration point documentation** — Opus's inline placement + Haiku's standalone IP section can coexist. Include both.
10. **Contract timing** — document the contract in Phase 1 (lightweight, as Opus suggests) but verify extraction outputs against it (as Haiku's principle requires). No dedicated Phase 0 contract design.

### Remaining Disputes (Unresolved)

11. **BUILD_REQUEST wiring timing** — Opus's Phase 3 separation is safer; Haiku's Phase 1 bundling is more efficient. **Recommendation: adopt Opus's approach** given the spec's emphasis on fidelity risk.
12. **Timeline** — fundamentally depends on execution context (single-agent vs. team). **Recommendation: state both** with the execution context that determines which applies.
13. **Staffing model** — Opus's single-agent assumption matches likely execution context but Haiku's role definitions are useful documentation. **Recommendation: primary plan assumes single-agent; note team roles as optional scaling model.**

### Synthesis Recommendation

The merged roadmap should use **Opus as the structural base** (phase ordering, task specificity, timeline, BUILD_REQUEST wiring safety, line-count commitment) and incorporate **Haiku's additions** (integration point documentation format, cross-cutting gate summary, requirement traceability matrix, contract-awareness principle in Phase 1). This yields a roadmap that is directly executable (Opus's strength) while remaining auditable and traceable (Haiku's strength).
