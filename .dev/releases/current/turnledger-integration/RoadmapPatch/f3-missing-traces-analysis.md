---
finding_id: F3
status: analyzed
root_cause: "Extraction.md treats Open Questions as a separate category from FR/NFR requirements; the roadmap generators correctly mapped tasks to their governing Open Questions but the merge step did not back-trace Open Questions to their parent FR/NFR IDs"
recommended_fix: "Add explicit parent-FR cross-references to Open Question citations in T0.2 and T0.3; mark T6.4 as non-requirement release-admin work with an explicit 'N/A — release administration' annotation"
---

# F3: Missing FR/NFR Requirement Traces — Root Cause Analysis

## 1. Evidence Summary

### Tasks Under Investigation

**T0.2** (merged roadmap, line 39):
- Requirements column: `Open Question 1 (F6)`
- Description: F6 API verification spike — verify AsyncPostgresSaver import path, `from_conn_string()` signature, `max_size` kwarg, `.setup()` requirement.
- The Opus variant (roadmap-opus-architect.md, line 108) lists this same task as `T4.0` with Requirements = `Open Question 1`.
- The Haiku variant (roadmap-haiku-analyzer.md, lines 41-52) addresses this in Phase 0, Milestone 0.1, item 2, citing `Open Question 1 (F6)`.

**T0.3** (merged roadmap, line 40):
- Requirements column: `Open Question 8`
- Description: Async initialization pattern decision — choose between factory classmethod, FastAPI startup hook, or `asyncio.run()` in init.
- The Opus variant has this as `T4.1` with Requirements = `Open Question 8`.
- The Haiku variant addresses it in Phase 0, Milestone 0.1, item 3.

**T6.4** (merged roadmap, line 226):
- Requirements column: `—`
- Description: Tag release. Update CHANGELOG.md. Document known limitations for R2.
- Both Opus (line 167) and Haiku (Milestone 4.3) have equivalent release-admin tasks with no formal requirement citation.

### Open Question to FR/NFR Mapping

From extraction.md (lines 314-325), the Open Questions table:

| OQ | Question | Parent Requirement |
|----|----------|-------------------|
| OQ-1 | AsyncPostgresSaver API (F6) — import path, `from_conn_string()`, `.setup()` | Maps to **FR-R1.2** (checkpoint persistence) — the API surface being verified IS the FR-R1.2 implementation mechanism |
| OQ-8 | AsyncPostgresSaver async initialization — `.setup()` lifecycle pattern | Maps to **FR-R1.2** and **Risk 4** — the initialization pattern is a prerequisite for FR-R1.2 implementation |
| OQ-9 | langchain coordinated upgrade | Maps to **FR-R0.1** — dependency resolution |

From extraction.md (lines 316-317): OQ-1 states "HIGH — blocks Tasks 16/17" and cites "tech-spec:237, adversarial F6". From extraction.md (line 323): OQ-8 states "HIGH — architectural decision" and cites "tech-spec:237".

Both OQ-1 and OQ-8 are implementation-risk questions about **how** to deliver FR-R1.2. They are not independent requirements; they are pre-conditions for implementing an existing FR.

**T6.4** has no parent requirement because release tagging, changelog updates, and limitation documentation are process/administrative activities, not functional or non-functional requirements specified in the release spec.

---

## 2. Root Cause Debate

### Root Cause 1: Extraction.md treats Open Questions as a structurally separate category from FR/NFR, and the roadmap generators faithfully reproduced this separation without back-tracing to parent requirements.

#### Prosecution

The extraction.md file (lines 17-18) explicitly separates its output into three categories: "Functional Requirements" (8), "Non-Functional Requirements" (6), and "Open Questions" (10). Open Questions appear in their own section (lines 312-325) with columns `#`, `Question`, `Impact`, `Resolution Target`, `Source` — but crucially, **no "Parent Requirement" column**. This structural omission means any downstream consumer (Opus generator, Haiku generator) that reads extraction.md cannot mechanically map an Open Question back to its governing FR/NFR without semantic reasoning.

Evidence: extraction.md line 316 — OQ-1's Source is "tech-spec:237, adversarial F6", not "FR-R1.2". The extractor cited the *source document* of the question, not the *requirement it serves*. Similarly, OQ-8 (line 323) cites "tech-spec:237" — again, a source reference, not a requirement reference.

The Opus roadmap generator, when creating T4.0 and T4.1 (later merged to T0.2 and T0.3), correctly identified these as Open Question resolution tasks and cited the OQ IDs. It did not perform the additional inference step of tracing OQ-1 back through its content ("AsyncPostgresSaver API") to FR-R1.2 ("Replace MemorySaver with AsyncPostgresSaver"). The generator followed the extraction's structure faithfully.

#### Defense

The generators are not purely mechanical — they are LLM-based and capable of semantic reasoning. The Opus roadmap (line 108) correctly places T4.0 as a "pre-implementation gate" for Phase 4, which IS the FR-R1.2 phase. This means Opus understood the dependency relationship even though it did not formalize it in the Requirements column. The structural separation in extraction.md is descriptive, not prescriptive — a competent generator should have inferred the connection.

Additionally, the Haiku variant (lines 41-52) explicitly groups OQ-1 resolution under "Deliverables" with "Implementation note resolving Open Questions 1, 8, and 9" alongside "Exact dependency lock decision for FR-R0.1" — showing that Haiku did understand the FR-to-OQ relationship, just didn't formalize it either.

#### Rebuttal

Understanding a relationship implicitly (via task ordering and phase placement) is not the same as formalizing it in the Requirements column. Both generators demonstrated implicit understanding but neither produced explicit traceability. This is exactly the failure the validation gate caught. The extraction's lack of a "Parent Requirement" column on Open Questions made explicit tracing a reasoning-optional step rather than a structurally-enforced one.

#### Verdict: **LIKELY**. The extraction's structural separation is the proximate cause. Both generators understood the relationship but neither formalized it because the extraction did not make the mapping explicit.

---

### Root Cause 2: The merge step (base-selection + diff-analysis + debate-transcript) incorporated Haiku's F6 timing change (moving T4.0/T4.1 to Phase 0) without updating the Requirements column to include the parent FR/NFR IDs.

#### Prosecution

The merge process is documented in base-selection.md and diff-analysis.md. The key merge decision was D2/D3 (diff-analysis.md lines 32-48): Haiku's Phase 0 F6 timing was adopted over Opus's Phase 4 timing. This meant T4.0 and T4.1 from the Opus base were physically relocated to Phase 0 and renumbered as T0.2 and T0.3.

During this relocation, the merge step preserved the Opus task descriptions and Requirements column values. The Opus originals had `Open Question 1` and `Open Question 8` in the Requirements column. The merge step kept these citations. At no point during the merge did the process add `FR-R1.2` as a co-citation, even though the merge was motivated precisely by the concern that F6 unresolved could block FR-R1.2.

The debate-transcript.md (line 137-140) describes what the merge would adopt from each variant — but the merge instructions focus on structural elements (Opus) and governance elements (Haiku). There is no instruction to "reconcile Requirements column citations across variants" or "ensure all tasks trace to formal FR/NFR IDs."

#### Defense

The merge step's job is to combine the best structural and governance elements of both variants. Requirements traceability validation is not part of the merge step — it is the job of the downstream validation gate (which is precisely what caught this issue). The merge step correctly relocated the tasks, preserved their content, and maintained the logical dependency structure. Adding FR/NFR back-traces would be a validation-driven correction, not a merge operation.

#### Rebuttal

The defense argument is functionally correct — the merge step's scope is structural combination, not traceability validation. However, this means the pipeline has a known gap: the merge step can produce a roadmap that satisfies structural quality criteria but fails traceability criteria. The validation gate is working as designed by catching this. The root cause is still partly attributable to the merge step because it had the opportunity to add the traces (both variants implicitly understood the FR-R1.2 connection) and did not.

#### Verdict: **LIKELY but secondary**. The merge step is a contributing cause, not the primary cause. It faithfully reproduced the extraction's structural gap.

---

### Root Cause 3: T6.4 is genuinely non-requirement administrative work that the pipeline has no mechanism to classify, resulting in a bare "—" that the validation gate treats as a deficiency.

#### Prosecution

T6.4's description is: "Tag release. Update CHANGELOG.md. Document known limitations for R2 (nullable vector column, no HNSW index, ConversationSummaryBufferMemory left inert)."

None of these activities correspond to any FR or NFR in extraction.md:
- Release tagging is a process artifact, not a functional requirement.
- CHANGELOG.md updates are documentation hygiene, not a specified deliverable.
- Documenting R2 limitations is forward-planning, not an R1 requirement.

Both the Opus variant (line 167) and the Haiku variant (Milestone 4.3, lines 346-352) have equivalent release-admin tasks. Neither cites any FR/NFR. This is consistent across both generators — it is not a gap in one generator that the other caught.

The extraction.md contains no requirement for "release tagging" or "changelog maintenance." The spec (release-spec-ontrag-r0-r1.md) Section 1.2 (Scope Boundary) does not list release admin activities. These are standard engineering practices that exist outside the formal requirement set.

#### Defense

One could argue that T6.4 implicitly serves all requirements — a release gate ensures all SCs are met. T6.3 already verifies all 15 success criteria, so T6.4 could cite "All SCs" as its requirement (matching T6.1). Alternatively, the validation gate could be configured to accept "—" for explicitly-marked administrative tasks rather than treating all "—" entries as deficiencies.

Additionally, the CHANGELOG documentation of known R2 limitations could be traced to the R2 handoff contracts (Architectural Constraints 5, 6 in extraction.md lines 242-244), which derive from spec Section 2.1 Decisions 5 and 11.

#### Rebuttal

Tracing T6.4 to "All SCs" would be false traceability — T6.4 does not *implement* or *verify* any SC; it packages them. Similarly, tracing CHANGELOG entries to Architectural Constraints is a stretch — the constraints govern implementation behavior, not documentation activities. The honest answer is that T6.4 is non-requirement work, and the pipeline should acknowledge this category explicitly rather than forcing a false trace or flagging it as a gap.

#### Verdict: **LIKELY**. T6.4 is genuinely non-requirement work. The pipeline lacks a "release administration" task category that would make "—" an intentional annotation rather than a gap.

---

### Most Likely Root Cause Declaration

**Root Cause 1 is the primary cause** for T0.2 and T0.3. The extraction.md structurally separates Open Questions from FR/NFR requirements without providing a parent-requirement cross-reference column. Both roadmap generators faithfully reproduced this separation, and the merge step preserved it. The validation gate correctly identified the resulting traceability gap.

**Root Cause 3 is the primary cause** for T6.4. This is a categorically different issue — T6.4 is genuine non-requirement work that has no formal FR/NFR to trace to. The pipeline lacks a mechanism to classify administrative tasks.

Root Cause 2 is a contributing factor but not the primary driver.

---

## 3. Solution Debate

### Solution 1: Patch the merged roadmap — add `FR-R1.2` as a co-citation to T0.2 and T0.3; annotate T6.4 with `N/A — release administration`.

#### Advocate

This is the simplest, most direct fix. It addresses the immediate finding with minimal disruption:

- T0.2's Requirements column changes from `Open Question 1 (F6)` to `FR-R1.2, OQ-1 (F6)` — making explicit what both generators implicitly understood.
- T0.3's Requirements column changes from `Open Question 8` to `FR-R1.2, OQ-8` — same logic.
- T6.4's Requirements column changes from `—` to `N/A — release administration` — explicitly marking it as intentionally non-requirement work.

This fix takes <5 minutes, is verifiable by re-running the validation gate, and does not require changes to the extraction pipeline, the generator prompts, or the merge process. It addresses the symptom at the point where the validation gate found it.

The traceability is not false — OQ-1 and OQ-8 genuinely serve FR-R1.2. The fix makes a true relationship explicit.

#### Critic

This is symptom patching. The extraction pipeline will produce the same gap on the next release spec. The next roadmap generation will require the same manual fix. If the goal is audit completeness, fixing three cells in one roadmap does not achieve systemic improvement.

Additionally, adding `FR-R1.2` to T0.2 could be misleading — T0.2 does not implement FR-R1.2; it verifies a precondition. A reader might interpret `FR-R1.2` in the Requirements column as "this task delivers FR-R1.2" rather than "this task de-risks FR-R1.2."

#### Rebuttal

The critic's systemic concern is valid but premature. This is a V0.1 pipeline running its first validation pass. Systemic fixes should be informed by a pattern of failures, not a single finding. If F3 recurs in subsequent releases, then pipeline changes are warranted.

On the misleading interpretation: the Requirements column in this roadmap already mixes "implements" and "verifies" relationships (e.g., T0.4 cites `FR-R0.1/AC5, NFR-R1.6` — it verifies them, it does not implement them). Adding `FR-R1.2` to T0.2 is consistent with existing column semantics.

#### Verdict: **RECOMMENDED**. Correct, minimal, consistent with existing conventions, and immediately actionable.

---

### Solution 2: Add a "Parent Requirement" column to the extraction.md Open Questions table, and re-run the roadmap generators.

#### Advocate

This addresses Root Cause 1 at its source. By adding a `Parent Requirement` column to the Open Questions table in extraction.md, every downstream consumer (Opus generator, Haiku generator, merge step) has explicit traceability information. Future roadmaps generated from this extraction will automatically produce correct traces.

The mapping is straightforward:
- OQ-1 → FR-R1.2
- OQ-2 → FR-R1.4
- OQ-3 → FR-R0.3
- OQ-4 → Deferred (R2)
- OQ-5 → Deferred (R2)
- OQ-6 → Deferred (R2)
- OQ-7 → Deferred (R3)
- OQ-8 → FR-R1.2
- OQ-9 → FR-R0.1
- OQ-10 → FR-R1.4

This is a one-time enrichment that pays forward.

#### Critic

Re-running the roadmap generators is expensive and risky. The current merged roadmap is the product of a multi-step adversarial pipeline (two generators, debate, base selection, diff analysis, merge). Re-running this to fix three cells is disproportionate. There is also a risk that re-generation produces different results — the generators are non-deterministic, and any roadmap drift would require a new validation cycle.

Additionally, the extraction.md schema is a pipeline artifact. Changing its schema requires updating the extraction prompt, which affects all future releases. This is a pipeline evolution decision that should be made deliberately, not reactively in response to a single validation finding.

#### Rebuttal

The critic correctly identifies the cost-benefit imbalance. However, the enrichment of extraction.md itself (adding the Parent Requirement column) is valuable even without re-running the generators. It can be done as a standalone improvement to the extraction artifact, and the roadmap can be patched per Solution 1. The two actions are complementary, not alternatives.

#### Verdict: **ACCEPTABLE with modification**. Enrich extraction.md with the Parent Requirement column as a forward-looking improvement, but DO NOT re-run the generators. Patch the roadmap per Solution 1 for the immediate fix.

---

### Solution 3: Introduce a `task_category` field in the roadmap task schema that distinguishes "implementation", "verification", "decision", and "administration" tasks — each with different traceability requirements.

#### Advocate

This addresses Root Cause 3 systemically and also clarifies Root Cause 1. By categorizing tasks:

- **Implementation** tasks (T1.3, T3.1, T4.2, T5.3, etc.) MUST trace to FR/NFR IDs.
- **Verification** tasks (T0.4, T4.5, T6.1, T6.3) MUST trace to SC IDs.
- **Decision** tasks (T0.2, T0.3, T4.0) MUST trace to OQ IDs AND their parent FR/NFR.
- **Administration** tasks (T6.4) are explicitly exempt from FR/NFR tracing.

This schema change would make the validation gate smarter — it can enforce different rules per category rather than a blanket "all tasks must have FR/NFR traces."

#### Critic

This is over-engineering for a V0.1 pipeline. The roadmap currently has 28 tasks across 7 phases. Adding a task_category schema, updating the generator prompts, updating the merge process, and updating the validation gate is a multi-day effort to prevent a 3-cell patching operation. The ROI is negative unless the pipeline will be used for dozens of future releases.

Furthermore, the category boundaries are fuzzy. Is T0.1 (clean virtualenv spike) an "implementation" task or a "verification" task? Is T2.5 (dead code import trace) a "decision" task or a "verification" task? Category assignment itself becomes a source of debate and potential error.

#### Rebuttal

The critic's cost concern is decisive for the current release. However, the category concept is worth noting for future pipeline evolution. The fuzzy boundary concern is real but manageable — most tasks have obvious categories, and edge cases can default to "implementation" (strictest traceability).

#### Verdict: **REJECTED for current scope**. Good concept for future pipeline evolution but disproportionate for this finding.

---

### Recommended Solution Declaration

**Solution 1 (direct roadmap patch)** is the recommended fix for F3.

Specific changes:
1. **T0.2** (roadmap.md line 39): Change Requirements from `Open Question 1 (F6)` to `FR-R1.2, OQ-1 (F6)`
2. **T0.3** (roadmap.md line 40): Change Requirements from `Open Question 8` to `FR-R1.2, OQ-8`
3. **T6.4** (roadmap.md line 226): Change Requirements from `—` to `N/A — release administration`

Optional forward-looking improvement (Solution 2, partial): Add a `Parent Requirement` column to extraction.md's Open Questions table for future pipeline runs. This is not required to close F3 but improves the extraction artifact for subsequent releases.

