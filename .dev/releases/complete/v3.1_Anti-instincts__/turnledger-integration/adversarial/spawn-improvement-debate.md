# Adversarial Debate: sc:spawn Prompt Construction Rules

**Subject**: Proposed Rules 1-4 in `src/superclaude/commands/spawn.md` (Prompt Construction Rules section, lines 37-56)
**Date**: 2026-03-20
**Format**: 3-round structured debate (Opening, Rebuttal, Closing + Verdict)

## Background

An A/B test comparing manual orchestration (Doc A) vs `sc:spawn` delegation (Doc B) across 3 releases produced the following results:

| Criterion | Winner | Margin |
|-----------|--------|--------|
| S1: Gap Detection | Doc B (spawn) | Consistent across all 3 releases |
| S2: Actionability | Doc B (spawn) | Consistent across all 3 releases |
| S3: Evidence Rigor | Doc A (manual) | Consistent across all 3 releases |
| Low-impact completeness | Doc A (manual) | Caught criterion counts, stale refs, subsection ordering |

Four rules were proposed to close the S3 gap while preserving S1/S2 strengths:

- **Rule 1**: Resolve file paths before delegation (lines 41-42)
- **Rule 2**: Inject evidence requirements into every analytical prompt (lines 44-49)
- **Rule 3**: Inject output structure when user omits it (lines 51-53)
- **Rule 4**: Inject cross-reference counts (lines 55-56)

---

## Round 1: Opening Arguments

### PRO — Each Rule Addresses a Specific, Observed Deficit

**On Rule 1 (Resolve File Paths Before Delegation):**

The A/B test showed Doc B's sub-agents sometimes referenced files by name without confirming paths, leading to accuracy gaps under S3. When spawn passes a bare goal like "review this release," the delegated agent must independently discover which files matter. This path-discovery step is nondeterministic -- the agent may Glob differently each time, miss nested directories, or waste tokens traversing irrelevant paths. Rule 1 eliminates this variance by doing the work once at the orchestrator level and handing each agent an explicit, verified file manifest.

This is not speculative. The current spawn.md Behavioral Flow (line 24) already lists "Analyze: Parse complex operation requirements and assess scope across domains" as Step 1. Rule 1 simply requires that this analysis resolve to concrete file paths rather than abstract scope descriptions. The orchestrator already reads the user's input -- extracting file paths from that read is marginal additional cost.

**On Rule 2 (Inject Evidence Requirements):**

This rule directly targets the S3 deficit. Doc A won on Evidence Rigor for a single, clear reason: its prompt explicitly stated "cite line numbers, task IDs, quotes." Doc B's delegated commands had no such instruction. The delegated commands' own protocols (which drove S1 and S2 wins) do not include evidence citation standards -- they focus on analytical structure and gap coverage.

Rule 2 is a 3-line text injection. The token cost is approximately 30-40 tokens per delegated prompt. The return is that every analytical output cites verifiable evidence rather than making unsupported assertions. This is the highest-ROI rule in the set: minimal cost, directly closes the measured gap, and does not alter the delegated command's analytical approach at all -- it only adds an evidence citation layer on top.

**On Rule 3 (Inject Output Structure When User Omits It):**

The A/B test revealed that when Doc B's delegated commands chose their own output structure, the structure was optimized for the command's internal protocol but not for downstream consumption. For example, a `sc:reflect` output might organize findings by reflection phase rather than by the sections the user will need to act on. The orchestrator has more context about the full pipeline -- it knows which other commands will consume this output and what structure they expect.

Rule 3 does not override the delegated command's structure in all cases. It activates only "when the user omits" a structure specification. This is a fallback, not an override. When the user specifies sections, Rule 3 is inert. When no one specifies sections, someone must -- and the orchestrator has strictly more context than the delegated command about the end-to-end workflow.

**On Rule 4 (Inject Cross-Reference Counts):**

Doc A caught low-impact items that Doc B missed -- specifically, criterion counts, stale Appendix references, and subsection ordering. These are completeness checks that require knowing the expected count before verification. Without a count, an agent can verify that "tasks are covered" without actually counting whether all N tasks are present.

Rule 4 turns a qualitative verification ("check coverage") into a quantitative one ("the plan contains 20 edits -- verify all 20"). This is the difference between an agent declaring "100% coverage" after spotting 15 of 20 items and an agent that knows it must account for exactly 20.

### CON — Each Rule Risks Damaging Spawn's Existing Strengths or Violating Its Design

**On Rule 1 (Resolve File Paths Before Delegation):**

The current spawn.md defines itself as a meta-orchestrator that "produces a TASK HIERARCHY ONLY" (line 113) and "delegates execution to other commands" (line 113). Rule 1 fundamentally changes spawn's role: it must now pre-read the filesystem to resolve paths before producing its task hierarchy. This is execution work, not decomposition work.

The "CRITICAL BOUNDARIES" section (lines 109-127) explicitly states spawn "Will NOT: Execute implementation tasks directly." Resolving file paths by running Glob/Read operations is an implementation task -- it produces runtime artifacts (a resolved path list) that the delegated command needs. Spawn currently operates at a higher abstraction level: it tells the agent what to analyze, not which bytes to read.

Furthermore, pre-resolving paths creates a brittleness problem. If spawn resolves paths at decomposition time but the delegated agent runs minutes or hours later (in a multi-step pipeline), files may have been created, moved, or deleted in the interim. Spawn would be providing stale path data. The delegated agent, running at execution time, would discover the current filesystem state.

**On Rule 2 (Inject Evidence Requirements):**

While the 30-40 token cost per prompt seems small, the real cost is the behavioral constraint it places on the delegated command. The injected text says "Unsupported assertions must be flagged as LOW CONFIDENCE." This creates a perverse incentive: the agent may avoid making high-value inferential observations (the kind that drove Doc B's S1 gap-detection superiority) because they cannot be directly quoted from a source line.

Doc B beat Doc A on gap detection precisely because the delegated commands' protocols encourage open-ended discovery -- finding what is missing, not just what is present. Gap detection is inherently about absence, which cannot be cited with a line number. Rule 2 risks shifting agents toward a conservative, citation-heavy style that confirms what exists rather than discovering what is absent.

The A/B test showed this tradeoff clearly: Doc A had better evidence rigor (S3) but worse gap detection (S1). These may be inversely correlated. If so, Rule 2 does not "close the S3 gap while preserving S1" -- it trades S1 for S3.

**On Rule 3 (Inject Output Structure When User Omits It):**

Rule 3's justification claims "the orchestrator has more context about what downstream consumers need." This is stated as fact in the rule text (line 53) but is actually the central contested claim. Does the orchestrator have more context, or less?

The delegated command has domain-specific protocol knowledge. `sc:reflect` knows what a good reflection looks like. `sc:adversarial` knows what a good debate structure looks like. These commands have been refined through usage -- their output structures are not arbitrary defaults but evolved protocol designs. The orchestrator, by contrast, has breadth (it knows the full pipeline) but not depth (it does not know what makes a good reflection).

More critically, Rule 3 says "Do not rely on the delegated command to choose its own structure." This is an anti-pattern in delegation architecture. If the orchestrator overrides the delegated command's structure, it is micromanaging -- and micromanagement in multi-agent systems produces the same pathology it produces in human organizations: the delegate follows the imposed structure even when it is suboptimal for the task, because it was told to.

The A/B test already proved this: Doc B (which let delegated commands choose their own structure) won on S1 and S2. The structure the commands chose was better for gap detection and actionability than anything the orchestrator could have imposed.

**On Rule 4 (Inject Cross-Reference Counts):**

Rule 4 requires spawn to pre-read source documents to extract counts before delegation. This is a significant expansion of spawn's responsibilities. Currently, spawn decomposes and delegates -- it does not analyze source content. Rule 4 turns spawn into a content-aware preprocessor.

The "Explicitly Will NOT: Execute implementation tasks directly" boundary (line 115) is directly violated. Counting items in a document, parsing its structure to determine how many edits/tasks/criteria exist -- this is analytical work that belongs to the delegated command, not the orchestrator.

There is also a correctness risk. If spawn counts "20 edits" but miscounts (perhaps because the document has nested or conditional edits), the delegated agent will either: (a) trust the count and stop at 20 even if 22 exist, or (b) find a discrepancy and waste tokens reconciling whether the orchestrator's count or its own count is correct. The orchestrator's count becomes an authoritative-but-potentially-wrong constraint.

Finally, the observation that "Doc A caught low-impact items Doc B missed" must be weighed against the word "low-impact." The items missed (criterion counts, stale Appendix refs, subsection ordering) were classified as low-impact in the A/B evaluation itself. Building a rule to catch low-impact items at the cost of increased orchestrator complexity is questionable ROI.

---

## Round 2: Rebuttals

### PRO Responds to CON's Strongest Point

CON's strongest argument is the inverse correlation claim on Rule 2: that evidence rigor (S3) and gap detection (S1) are inherently in tension, and improving one necessarily degrades the other. This is the most dangerous objection because, if true, it means the proposal's core motivation is flawed.

However, the inverse correlation is asserted, not demonstrated. The A/B test compared two entirely different prompting strategies (manual vs delegated), not two versions of the same strategy with and without evidence requirements. Doc A's weaker gap detection was not caused by its evidence requirements -- it was caused by its lack of the delegated commands' analytical protocols. Doc B's weaker evidence rigor was not caused by its superior gap detection -- it was caused by the absence of any evidence citation instruction.

These are independent deficits with independent causes. Rule 2 injects evidence requirements into prompts that already have the delegated commands' gap-detection protocols. It does not replace those protocols. The agent receives both: "use your reflective analysis protocol" (from the delegated command) AND "cite line numbers for your findings" (from Rule 2). There is no mechanism by which adding a citation instruction would suppress the analytical protocol that drives gap detection.

The "LOW CONFIDENCE" flag for unsupported assertions is specifically designed to handle the gap-detection case. When an agent detects a gap (something absent from the document), it cannot cite a line number -- there is no line to cite. Under Rule 2, it flags this as LOW CONFIDENCE, which is accurate: a finding about absence is inherently lower confidence than a finding about presence. The flag does not prevent the observation -- it calibrates trust appropriately.

### CON Responds to PRO's Strongest Point

PRO's strongest argument is on Rule 2: that the 30-40 token injection directly targets the measured S3 deficit at minimal cost and without altering the delegated command's analytical approach. This is compelling because it appears to be a purely additive intervention.

However, "purely additive" is naive about how LLM agents respond to instructions. When you inject "cite specific line numbers, task IDs, section references, or direct quotes for every finding," you are not adding a passive annotation layer -- you are reshaping the agent's attention allocation. The agent will spend tokens locating citable evidence rather than exploring the problem space. This is not a logical necessity but an empirical pattern: LLM agents given citation requirements produce more citations and fewer novel observations.

The "LOW CONFIDENCE" flag mechanism does not solve this. It creates a two-tier system where cited findings are implicitly HIGH CONFIDENCE and uncited findings are explicitly LOW CONFIDENCE. In any report with mixed-tier findings, the reader (or downstream agent) will naturally prioritize the HIGH CONFIDENCE items. Gap-detection findings -- which are systematically uncitable -- will be systematically deprioritized. The flag does not prevent the observation, but it does devalue it.

A better approach: inject evidence requirements only for verification tasks (where completeness checking matters) and not for discovery tasks (where open-ended exploration matters). Rule 2 as written applies to "every delegated prompt that produces analytical output" -- this is too broad. It should distinguish between verification-mode and discovery-mode delegations.

### PRO Responds to CON on Rule 3

CON argues that delegated commands have evolved protocols that produce superior structure (evidenced by S1/S2 wins). This is partially true but mischaracterizes Rule 3's scope. Rule 3 activates only "when the user omits" structure. In practice, most spawn invocations include user intent that implies structure -- "review this release," "audit this implementation." Rule 3 handles the edge case where intent is ambiguous.

CON's "micromanagement" analogy also overstates the intervention. Rule 3 says to "infer appropriate sections from the delegated command's protocol." The orchestrator is not imposing a foreign structure -- it is making the delegated command's own protocol structure explicit in the prompt. This is closer to writing a meeting agenda based on the facilitator's known process than to micromanaging the facilitator's decisions.

### CON Responds to PRO on Rule 1

PRO argues that resolving paths is a marginal extension of spawn's existing Step 1 ("Analyze: Parse complex operation requirements"). This undersells the change. "Parsing requirements" is a cognitive task -- understanding what the user wants. "Resolving file paths" is a filesystem task -- running Glob, reading directories, verifying file existence. These are categorically different operations.

The brittleness argument stands unrebutted. If spawn operates asynchronously (decomposes now, delegates later), resolved paths may be stale. PRO has not addressed this because there is no good answer: either paths are resolved at decomposition time (potentially stale) or at delegation time (which means the delegated agent resolves them, making Rule 1 moot).

That said, if spawn operates synchronously (decomposes and delegates in the same session), the staleness risk is negligible. The applicability of Rule 1 depends on spawn's execution model, which the proposal does not specify.

---

## Round 3: Closing Arguments + Verdict

### PRO Closing

The A/B test identified a clear, reproducible deficit: Doc B (spawn-delegated) produces structurally superior analysis with better gap detection but lacks evidence discipline. Rules 1-4 are a targeted intervention to close this gap.

The most defensible rules are Rule 1 (path resolution) and Rule 2 (evidence injection), which address concrete, observed failure modes with minimal architectural disruption. Rule 4 (count injection) addresses a real but lower-priority issue. Rule 3 (structure injection) has the weakest justification given that Doc B's self-chosen structures already outperform.

I concede that CON's point about Rule 2's scope is well-taken: evidence requirements should distinguish verification tasks from discovery tasks. I concede that Rule 3's claim about orchestrator context superiority is not supported by the A/B evidence -- the data shows delegated commands choose better structures. I maintain that Rule 1 and Rule 4 are sound engineering: give agents the data they need rather than making them discover it.

### CON Closing

The proposal's motivation is sound -- the S3 deficit is real and should be addressed. But the implementation is overbroad. Rules 1-4 collectively transform spawn from a thin orchestrator into a content-aware preprocessor that resolves paths, injects behavioral constraints, overrides structure, and pre-counts items. This violates the separation of concerns that made spawn effective in the first place.

The A/B test's most important finding is not the S3 deficit -- it is that Doc B won on S1 and S2 without these rules. The delegated commands' protocols are the source of spawn's quality advantage. Rules that constrain, override, or preempt those protocols risk degrading the very mechanism that produces superior results.

I concede that Rule 2 (evidence injection) has merit in a narrowed form. I concede that Rule 1 (path resolution) reduces nondeterminism at acceptable cost if spawn operates synchronously. I maintain that Rule 3 should be dropped entirely and Rule 4 should be optional rather than mandatory.

---

## Verdict

### Per-Rule Assessment

| Rule | Verdict | Rationale |
|------|---------|-----------|
| Rule 1: Resolve File Paths | **KEEP with modification** | Sound engineering -- reduces nondeterminism and wasted tokens. Modify to scope it to synchronous execution only: "When spawning agents within the same session, resolve file paths. When producing async task hierarchies for later execution, include path hints but do not assert resolution." |
| Rule 2: Inject Evidence Requirements | **KEEP with modification** | Highest-ROI rule, directly targets the measured S3 deficit. Modify to narrow scope: apply to verification/audit/completeness-check delegations. For discovery/reflection/brainstorm delegations, inject a softer version: "Provide supporting evidence where available; flag findings without direct evidence as inferential." This preserves gap-detection capability while improving citation discipline where it matters most. |
| Rule 3: Inject Output Structure | **DROP** | The A/B evidence argues against this rule. Doc B won S1 and S2 with delegated-command-chosen structures. The claim that "the orchestrator has more context" is not supported by the data -- if anything, the data shows the opposite. The rule's text ("Do not rely on the delegated command to choose its own structure") contradicts the principle of delegation. Remove Rule 3 entirely. |
| Rule 4: Inject Cross-Reference Counts | **MODIFY to optional** | The underlying observation is valid (agents declare coverage without counting), but mandatory pre-reading violates spawn's boundary as a decomposition-only tool. Modify to: "When source documents are already read as part of Rule 1 path resolution, extract and inject relevant counts. Do not pre-read documents solely to extract counts." This makes Rule 4 opportunistic rather than mandatory, and dependent on Rule 1 execution. |

### Scoring Summary

| Criterion | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|-----------|--------|--------|--------|--------|
| Addresses measured deficit | 7/10 | 9/10 | 3/10 | 6/10 |
| Risk to existing strengths (S1/S2) | Low | Medium (mitigated by scope narrowing) | High | Low |
| Architectural consistency with spawn's boundaries | Medium (requires scoping) | High | Low (contradicts delegation) | Medium (requires scoping) |
| Implementation cost (tokens + complexity) | Low | Low | Medium | Medium |
| **Net recommendation** | Keep (modified) | Keep (modified) | Drop | Modify to optional |

### Recommended Revised Text for spawn.md

The Prompt Construction Rules section should be rewritten as follows:

**Rule 1 (revised)**: "Before spawning agents within the same session, resolve all input file paths using Glob/Read. Each agent prompt MUST include absolute paths to every file the agent needs. When producing task hierarchies for asynchronous execution, include path hints (directory names, glob patterns) but do not assert resolved paths."

**Rule 2 (revised)**: "For delegated prompts performing verification, audit, or completeness checking, inject: 'Evidence standard: cite specific line numbers, task IDs, section references, or direct quotes for every finding. Unsupported assertions must be flagged as LOW CONFIDENCE.' For delegated prompts performing discovery, reflection, or brainstorming, inject: 'Provide supporting evidence where available. Flag findings without direct evidence as inferential rather than confirmed.'"

**Rule 3**: Remove entirely. Delegated commands' own protocol structures produced superior results on S1 (Gap Detection) and S2 (Actionability) in A/B testing. The orchestrator should not override or preempt these structures.

**Rule 4 (revised)**: "When source documents have been read as part of path resolution (Rule 1), extract and include relevant counts in the delegated prompt (e.g., 'The plan contains 20 edits -- verify all 20'). Do not pre-read documents solely to extract counts."

### Unresolved Tensions

1. **Empirical validation needed**: The modified rules are evidence-informed recommendations, not evidence-proven improvements. The only way to confirm they close the S3 gap without degrading S1/S2 is to run a follow-up A/B test with the modified spawn.md against the original.

2. **Verification vs. discovery boundary**: Rule 2's revised form depends on spawn correctly classifying delegations as "verification" vs. "discovery." This classification is itself nontrivial and may need its own heuristic or user hint (e.g., `--mode verify` vs `--mode discover`).

3. **Rule 4 dependency on Rule 1**: The revised Rule 4 is opportunistic -- it fires only when Rule 1 has already read documents. This means Rule 4 has no effect in async task-hierarchy mode. Whether this limitation is acceptable depends on how often spawn operates synchronously vs. asynchronously.

---

**Convergence score**: 72% -- Both sides agreed on Rule 2's merit (with scope narrowing) and Rule 3's weakness. Disagreement persists on the degree to which Rules 1 and 4 expand spawn's responsibilities beyond its design boundaries.
