---
finding_id: F5
status: analyzed
root_cause: "Test-strategy generator only creates validation steps for tasks with testable outputs (code artifacts, test results, config changes); read-only analysis tasks (T2.5) and administrative release tasks (T6.4) fall outside its testability heuristic"
recommended_fix: "Add explicit exclusion annotations for non-testable tasks in the roadmap, and add a documentation-verification step in VM-6 for release administrative tasks"
spec_source: release-spec-ontrag-r0-r1.md
roadmap_source: roadmap.md
test_strategy_source: test-strategy.md
---

# F5: Validation Coverage Gap Analysis — T2.5 and T6.4

## 1. Evidence Summary

### T2.5: Dead Code Import Trace

- **Roadmap definition** (`roadmap.md:84`): `T2.5 | FR-R0.6 | Dead code import trace — read-only analysis, document findings. | Parallel`
- **Extraction** (`extraction.md:82`): `FR-R0.6: Dead code import trace (read-only analysis)` — listed as an implicit sub-requirement under FR-R0.4, with no explicit acceptance criteria.
- **Test strategy VM-2** (`test-strategy.md:49-76`): Gate B lists T-2.1, T-2.2, T-2.3, T-2.4, T-2.6 — **T-2.5 is absent**. No validation step for dead code trace.
- **Test strategy Section 3** (`test-strategy.md:162-218`): Test categories (unit, integration, infrastructure, load, regression) — no test for dead code trace.
- **Test strategy Section 5** (`test-strategy.md:260-300`): Priority 4 (Operational/LOW) includes "Validation scripts (v01, gemini)" at Phase 2 — but dead code trace is not listed.

### T6.4: Tag Release / Changelog / Limitations

- **Roadmap definition** (`roadmap.md:226`): `T6.4 | — | Tag release. Update CHANGELOG.md. Document known limitations for R2 (nullable vector column, no HNSW index, ConversationSummaryBufferMemory left inert). | After T6.3`
- **Requirements column**: Dash (`—`) — no FR/NFR ID assigned.
- **Test strategy VM-6** (`test-strategy.md:145-158`): Release Gate lists T-6.1 (full test suite), T-6.2 (North Star re-run), T-6.3 (15 success criteria checklist) — **T-6.4 is absent**.
- **Test strategy M6 acceptance** (`test-strategy.md:351-355`): Four items — 30/30 tests, North Star, 15 success criteria, release anchors. No CHANGELOG or tag verification.
- **Extraction** (`extraction.md`): No FR/NFR covers release tagging or changelog generation.

### Coverage Gap Confirmation

Both T2.5 and T6.4 appear in the roadmap task tables but have zero matching validation steps anywhere in the test strategy — not in validation milestones, test categories, risk-based priorities, acceptance criteria, or quality gates.

---

## 2. Root Cause Analysis — Three Hypotheses

### RC-1: Test-strategy generator filters on testability, excluding analysis-only and administrative tasks

**Theory**: The test-strategy generator creates validation steps only for tasks that produce testable artifacts (code changes, config modifications, test results, script files). T2.5 produces a document (analysis findings), and T6.4 produces administrative artifacts (git tag, CHANGELOG, limitation notes). Neither produces code that can be verified by automated tests, `grep` checks, or SQL queries. The generator's heuristic for "what needs validation" is implicitly scoped to machine-verifiable outputs.

### RC-2: Test-strategy generator maps from extraction FR/NFR IDs, and tasks without explicit acceptance criteria get dropped

**Theory**: The test-strategy generator uses the extraction document's FR/NFR list as its primary input for building validation milestones. FR-R0.6 exists in the extraction (`extraction.md:82`) but has no acceptance criteria sub-IDs (unlike FR-R0.1/AC1, FR-R0.2/AC2, etc.). T6.4 has no FR/NFR mapping at all (dash in requirements column). The generator only creates validation steps for requirements with explicit AC sub-IDs, so both tasks fall through the mapping.

### RC-3: The merge step added tasks from the Opus variant that the Haiku-derived test strategy did not anticipate

**Theory**: The merged roadmap uses Opus as the base variant (`base-selection.md:2`), which includes Opus's fine-grained task IDs (T0.1-T6.4). The test strategy was generated from the extraction and spec, potentially using the Haiku analyzer's concern-based structure (5 gates A-E mapped to concern clusters, per `diff-analysis.md:71`). The Haiku variant organized validation by requirement clusters, not task IDs. When the merge took Opus's task structure but Haiku's gate structure, tasks that existed only in Opus's breakdown (like T2.5 dead code trace and T6.4 release packaging) had no pre-existing validation home in the Haiku-influenced test strategy.

---

## 3. Root Cause Debate

### RC-1 Debate: Testability Filter Hypothesis

#### Prosecution
T2.5 is described as "read-only analysis, document findings" — its output is a markdown document, not executable code. T6.4's outputs are a git tag, CHANGELOG update, and a limitations document — all administrative. The test strategy's Section 3 (`test-strategy.md:162-218`) categorizes tests as Unit, Integration, Infrastructure, Load, and Regression. None of these categories accommodate "document exists on disk" or "git tag exists" verification. The entire test taxonomy is built around machine-verifiable outputs.

Furthermore, every task that IS covered in the test strategy has a concrete verification method: CLI commands (`python -c "..."`), grep checks, SQL queries, pytest execution, or API calls. T2.5 and T6.4 do not fit any of these verification patterns.

#### Defense
The test strategy DOES include non-automated checks. For example, `test-strategy.md:61-62` lists `T-2.4: validate_v01_data.py exits 1` and `T-2.6: validate_gemini_key.py exists and runs` — these are script-existence checks, not automated tests. If the generator can handle "script exists" verification, it could equally handle "document exists" verification for T2.5's output.

Additionally, T6.3 (`test-strategy.md:150`) says "All 15 success criteria executed as verification checklist with evidence" — this IS a documentation verification step. The generator clearly knows how to create checklist-based validation. It chose not to for T6.4.

#### Rebuttal
The validation scripts (T-2.4, T-2.6) are different because they ARE executable code with defined exit codes. "Script exists and runs" is still a machine-verifiable check. T2.5's output is a prose document with no defined pass/fail criteria. The generator cannot construct a pass condition for "dead code analysis findings are correct" because correctness of a prose analysis is inherently subjective.

For T6.3 vs T6.4: T6.3 maps to the 15 success criteria (SC-1 through SC-15), which are enumerated with specific pass conditions in the extraction. T6.4 has no enumerated pass conditions — "CHANGELOG updated" and "tag created" are process steps, not testable assertions.

#### Verdict: **LIKELY**. The testability filter explains both gaps. The generator's validation taxonomy is oriented around machine-verifiable outputs, and both T2.5 and T6.4 produce artifacts that fall outside that taxonomy.

---

### RC-2 Debate: Missing Acceptance Criteria Hypothesis

#### Prosecution
Every task covered in the test strategy maps to an FR or NFR with explicit acceptance criteria sub-IDs. Examples:
- T-2.1 → FR-R0.3/AC4 (test-strategy.md:58)
- T-2.2 → FR-R0.3a (test-strategy.md:59)
- T-2.4 → FR-R0.5 (extraction.md:81, has implicit AC: "expects exit 1")
- T-6.1 → "All SCs" (roadmap.md:223)

FR-R0.6 (`extraction.md:82`) has no AC sub-IDs. It is listed as `FR-R0.6: Dead code import trace (read-only analysis)` with no acceptance criteria table. T6.4 has no FR mapping at all. The generator appears to iterate over FR/NFR entries with ACs and generate validation steps from those ACs. No ACs = no validation steps.

#### Defense
FR-R0.5 (`validate_v01_data.py`) also has no formal AC sub-ID in the extraction — it appears on the same line as FR-R0.6 as an "implicit sub-requirement." Yet the test strategy covers T-2.4 (the validation script) at `test-strategy.md:61`. This contradicts the hypothesis that missing ACs cause exclusion, because FR-R0.5 is covered despite having the same AC-less format as FR-R0.6.

#### Rebuttal
FR-R0.5 has an implicit but concrete acceptance criterion: "expects exit 1" (`extraction.md:81`). This is a binary pass/fail condition the generator can convert to a test step. FR-R0.6 has no such condition — "read-only analysis" provides no verifiable outcome. The distinction is not "has AC sub-ID" vs "doesn't" but rather "has any machine-verifiable pass condition" vs "doesn't." This collapses RC-2 into RC-1 (testability filter).

#### Verdict: **PARTIALLY TRUE, BUT SUBSUMES INTO RC-1**. The missing acceptance criteria are a symptom of the deeper issue: these tasks have no machine-verifiable outputs. RC-2 is a mechanism (no ACs to map) that produces the same outcome as RC-1 (no testable output).

---

### RC-3 Debate: Merge Mismatch Hypothesis

#### Prosecution
The base-selection document (`base-selection.md:2`) confirms the merged roadmap uses Opus's structure. The diff-analysis (`diff-analysis.md:70-72`) shows Opus has 4 gates while Haiku has 5 concern-based gates (A-E). The final test strategy (`test-strategy.md:2-6`) uses 6 validation milestones with concern-based naming (DEPENDENCY SAFETY, INFRASTRUCTURE READINESS, etc.) — this is closer to Haiku's gate structure than Opus's phase-aligned structure.

This means the merged roadmap took Opus's task breakdown (T0.1-T6.4) but the test strategy adopted Haiku's validation philosophy. If the test strategy was generated from the Haiku-influenced concern-based perspective, it would map validation to requirement concerns, not to individual Opus task IDs. Tasks that Opus added for completeness (T2.5 dead code trace, T6.4 release packaging) but that Haiku didn't surface as separate concern-level items would be invisible to the test-strategy generator.

#### Defense
The test strategy explicitly references task IDs from the roadmap (T-0.1 through T-6.3 at `test-strategy.md:31-150`). It is clearly aware of the Opus task structure — it maps validation steps to T-X.Y identifiers. If it can see T-2.4 and T-2.6 from Opus's Phase 2, it can see T-2.5. The gap is not that the generator is unaware of the tasks; it chose not to create validation for those specific tasks.

Furthermore, both the Opus roadmap (the old version at `.dev/tasks/to-do/v01-hybrid/feature-branch-planning/r0-r1/roadmap.md`) and the new merged roadmap include T2.5 and T6.4. The Opus variant's own test strategy (the old version at `.dev/tasks/to-do/v01-hybrid/feature-branch-planning/r0-r1/test-strategy.md`) also does not cover T2.5 and T6.4 in its milestone sections. This means the gap pre-dates the merge — it existed in Opus's original output too.

#### Rebuttal
The defense's point about the old Opus test strategy is strong. If the gap existed before the merge, the merge process cannot be the root cause. However, I note that the old test strategy DOES mention "dead code trace (FR-019)" in its interleaving map (`test-strategy-old:335`) as a Phase 5 task — it is acknowledged as existing but explicitly placed without a validation step. This suggests the generator acknowledges the task but categorizes it as "work, not test."

#### Verdict: **UNLIKELY**. The evidence shows the gap pre-dates the merge process. The old Opus test strategy also lacks coverage for these tasks. The merge did not introduce the gap.

---

### Most Likely Root Cause

**RC-1 (Testability Filter)** is the most likely root cause, with RC-2 as a contributing mechanism.

The test-strategy generator's validation taxonomy is built around machine-verifiable outputs: CLI commands, grep checks, SQL queries, pytest execution, API responses, and script exit codes. Tasks that produce only prose documents (T2.5 dead code trace) or administrative process artifacts (T6.4 git tag / CHANGELOG) have no natural home in this taxonomy. The generator correctly identifies these tasks exist but has no mechanism to generate validation steps for non-testable outputs.

RC-3 (merge mismatch) is ruled out because the gap exists in the pre-merge Opus test strategy as well.

---

## 4. Solution Brainstorm

### Solution A: Add document-existence verification steps to the test strategy

Add two new validation items:
- **VM-2 addition**: `T-2.5: Dead code import trace document exists at expected path with non-empty content`
- **VM-6 addition**: `T-6.4a: Git tag exists matching release version`, `T-6.4b: CHANGELOG.md updated with R0+R1 section`, `T-6.4c: Known limitations documented (nullable vector, no HNSW, inert ConversationSummaryBufferMemory)`

These are "artifact-on-disk" checks — verifiable by file existence and content inspection, not automated tests.

### Solution B: Annotate non-testable tasks with explicit exclusion in the roadmap

Add a `Validation: N/A (analysis artifact)` or `Validation: N/A (administrative)` annotation to T2.5 and T6.4 in the roadmap. Then add a reconciliation rule to the test strategy frontmatter: "Tasks annotated `Validation: N/A` are excluded from milestone coverage by design." This makes the gap intentional and documented rather than an oversight.

### Solution C: Create a separate "Process Verification Checklist" section in the test strategy

Add a new Section 3.6 to the test strategy: "Process/Administrative Verification" that handles non-code deliverables. This would include:
- Dead code trace document reviewed and committed
- Git tag created and pushed
- CHANGELOG updated
- Limitations document written

This separates process verification from code verification, giving the test strategy a home for tasks that don't fit the automated test taxonomy.

---

## 5. Solution Debate

### Solution A Debate: Document-Existence Verification Steps

#### Advocate
This is the simplest fix. It adds specific, verifiable items to the existing VM-2 and VM-6 sections. "File exists at path X with non-empty content" is a valid verification step that fits the existing test-strategy format. It uses the same pattern as T-2.4 ("validate_v01_data.py exits 1") and T-2.6 ("validate_gemini_key.py exists and runs"). The test strategy already accommodates existence checks — this just extends that pattern to document artifacts.

For T6.4, git tag verification (`git tag -l "v0.1-r0r1"`) and CHANGELOG grep (`grep "R0+R1" CHANGELOG.md`) are machine-verifiable. These fit the existing taxonomy without any structural changes.

#### Critic
This creates false coverage. "Document exists and is non-empty" does not validate the quality or correctness of T2.5's dead code analysis. A file containing "TODO: do the analysis" would pass the existence check. This gives the appearance of validation without substance — exactly the kind of checkbox compliance that masks real gaps.

For T6.4, git tag and CHANGELOG checks are process verification masquerading as test validation. The test strategy's purpose is to validate functional and non-functional requirements. Adding process checks dilutes its focus and sets a precedent for every administrative task needing a validation step.

#### Rebuttal
The critic's point about quality validation is fair for T2.5 — but the same critique applies to many existing items. T-0.3 (`test-strategy.md:33`) says "Async init pattern decision documented with rationale" — this is also a document-quality check that cannot verify correctness mechanically. The test strategy already contains items that verify "artifact exists with expected content" without judging analytical quality.

For T6.4, process verification IS part of release gating. The test strategy already includes `r1-acceptance.md` checklist verification (`test-strategy.md:150`) as a manual review step. Adding CHANGELOG/tag verification is consistent with that precedent.

#### Verdict: **RECOMMENDED**. Simple, consistent with existing patterns, addresses the immediate gap. The false-coverage concern is valid but manageable — these are LOW priority checks, not release-blocking gates.

---

### Solution B Debate: Explicit Exclusion Annotations

#### Advocate
This is the most honest approach. T2.5's dead code trace is genuinely not testable in a meaningful way — it's an expert analysis task whose quality depends on reviewer judgment. T6.4's release packaging is a process step, not a feature. Annotating them as `Validation: N/A` with documented rationale makes the gap intentional and transparent. It also establishes a pattern for future roadmaps where not every task needs a test-strategy entry.

#### Critic
This solves the finding but does not solve the underlying problem. The validation gate requires "all gated tasks to have corresponding validation coverage or explicit exclusion" — Solution B satisfies the gate by adding exclusions, but it means T6.4's CHANGELOG could be forgotten without any safety net. A release without a CHANGELOG or tag is a real operational failure, not a cosmetic one. Exclusion annotations normalize gaps rather than closing them.

Additionally, this puts the burden on the roadmap author to anticipate which tasks need exclusion annotations, which is the same failure mode that created the gap — the roadmap author (or merge step) already failed to anticipate these tasks needed special handling.

#### Rebuttal
The critic correctly identifies that T6.4 (release packaging) is operationally important and should not be excluded. However, T2.5 (dead code trace) is genuinely analysis-only — its value is in informing future R3 decisions, not in gating the current release. A hybrid approach (exclude T2.5, verify T6.4) might be optimal, but Solution B as stated is too broad.

#### Verdict: **ACCEPTABLE for T2.5, REJECTED for T6.4**. Dead code trace is legitimately non-testable analysis. Release packaging is operationally important and should have verification.

---

### Solution C Debate: Separate Process Verification Section

#### Advocate
This is the most architecturally clean approach. It acknowledges that roadmaps contain two types of tasks: (1) implementation tasks with testable outputs, and (2) process/administrative tasks with procedural verification. Creating Section 3.6 gives the test strategy a proper taxonomy for both. Future roadmaps benefit from this structure — every task has a validation home.

The section would use a different verification method (manual checklist) than the automated test sections, which correctly reflects that process tasks require human judgment (was the CHANGELOG complete?) rather than machine verification.

#### Critic
This is over-engineering for two tasks. Adding a new taxonomy section to the test strategy for two items (one of which is genuinely non-gating) creates structural complexity that does not pay for itself. The test strategy is already 459 lines — adding a new section for 4-5 checklist items is a poor complexity-to-value ratio.

Additionally, this sets a precedent that every future roadmap task needs to be classified as "implementation" or "process" and routed to the correct section. This adds cognitive overhead to the roadmap pipeline without clear benefit beyond the current finding.

#### Rebuttal
The complexity concern is valid. However, the critic underestimates the pattern's value: nearly every release has tagging, changelog, and documentation tasks. Creating the section once means future test strategies handle them automatically. The investment is small (one section with a clear template) and the payoff is durable.

That said, the advocate must concede that for the CURRENT finding, this is heavier than needed. Solution A achieves the same coverage with less structural change.

#### Verdict: **ACCEPTABLE but not preferred for this finding**. Architecturally sound, but over-engineered for the immediate gap. Better suited as a pipeline improvement for future releases.

---

### Best Solution

**Solution A (Document-Existence Verification Steps)** is the recommended fix.

**Reasoning**:
1. **Simplest change** — adds 4-5 lines to existing VM-2 and VM-6 sections.
2. **Consistent with existing patterns** — the test strategy already includes artifact-existence checks (T-2.4, T-2.6) and manual checklists (T-6.3).
3. **Addresses both tasks differently**: T2.5 gets a minimal "document exists" check (appropriate for analysis output), T6.4 gets machine-verifiable checks (git tag, CHANGELOG grep) that catch real operational omissions.
4. **No structural changes** — does not add new sections or classification taxonomies.
5. **Solves the validation gate** — all roadmap tasks now have either automated validation, artifact-existence checks, or are covered by the success criteria checklist.

**Specific additions**:

For VM-2 (test-strategy.md, after line 62):
```
- **T-2.5**: Dead code import trace document committed to `.dev/` — file exists with non-empty content
```

For VM-6 (test-strategy.md, after line 150):
```
- **T-6.4a**: Git tag matching release version exists
- **T-6.4b**: `CHANGELOG.md` contains R0+R1 release section
- **T-6.4c**: Known limitations for R2 documented (nullable vector column, no HNSW index, inert ConversationSummaryBufferMemory)
```

For M6 acceptance (test-strategy.md, after line 355):
```
- [ ] CHANGELOG.md updated with R0+R1 section
- [ ] Git tag created
- [ ] Known R2 limitations documented
```
