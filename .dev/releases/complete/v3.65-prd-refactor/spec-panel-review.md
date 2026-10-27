# PRD Skill Refactoring Spec -- Panel Review

```yaml
---
spec_reviewed: ".dev/releases/backlog/prd-skill-refactor/prd-refactor-spec.md"
fidelity_index: ".dev/releases/backlog/prd-skill-refactor/fidelity-index.md"
review_date: "2026-04-02"
mode: critique
focus: [correctness, architecture]
expert_panel: [wiegers, adzic, fowler, nygard, whittaker, crispin]
verdict: PASS WITH MINOR REVISIONS
---
```

## Quality Assessment

| Dimension | Score | Notes |
|-----------|-------|-------|
| Clarity | 9.0/10 | Exceptionally clear problem statement, evidence table, and cross-reference maps |
| Completeness | 8.5/10 | All 32 blocks mapped; two minor coverage gaps identified below |
| Testability | 8.5/10 | Strong fidelity diff tests; one gap in structural test coverage |
| Consistency | 8.0/10 | Two internal consistency issues (line count arithmetic, loading model description) |
| **Overall** | **8.5/10** | Production-ready with minor revisions |

---

## Expert Reviews

### Karl Wiegers -- Requirements Quality Assessment

**FR-PRD-R.1: SKILL.md line count target**

MINOR: The acceptance criterion states "430 and 500 lines" but the Solution Overview (Section 2) says "~430-480 lines." These are consistent but the spec self-scores quality at 9.5 completeness, which is slightly generous given the issues below.

RECOMMENDATION: No change needed; the range is a guidance target and the hard ceiling (500) is clearly stated.

**FR-PRD-R.6: Loading declarations**

MAJOR: The acceptance criterion in FR-PRD-R.6 states: "Load refs/agent-prompts.md, refs/build-request-template.md, refs/synthesis-mapping.md, and refs/validation-checklists.md before spawning the builder." However, Section 2.2 (Workflow / Data Flow) clarifies that the orchestrator only loads `refs/build-request-template.md` -- the builder subagent loads the other 3 refs in its own context. The acceptance criterion conflates what the orchestrator loads vs. what the builder loads.

RECOMMENDATION: Revise FR-PRD-R.6 acceptance criteria to distinguish:
- Orchestrator loads: `refs/build-request-template.md` (to construct the builder prompt)
- Builder subagent loads: `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md` (referenced within the BUILD_REQUEST)

This distinction matters because the loading declaration in SKILL.md should only instruct the orchestrator what to load. The builder finds the other refs through the cross-references baked into `refs/build-request-template.md`.

**FR-PRD-R.7: Combined line count criterion**

MINOR: The acceptance criterion says "Combined line count of SKILL.md + all refs/ files approximately equals the original 1,373 lines (accounting for added headers and loading declarations...and removal of duplicate Artifact Locations table B30 which is merged with B05)." The word "approximately" is imprecise. Given that headers are being added to 4 new refs/ files (est. 3-5 lines each = 12-20 lines added) and B30 (20 lines) is being merged (not removed entirely -- some unique rows move to B05), the combined count should be ~1,373 + 12-20 (headers) - 0 (B30 rows are merged, not deleted) = ~1,385-1,393.

RECOMMENDATION: Replace "approximately equals 1,373" with "is between 1,370 and 1,400 lines (original 1,373 plus ref file headers, minus deduplicated B30 rows absorbed into B05)."

---

### Gojko Adzic -- Specification by Example

**Testability of fidelity claims**

The spec provides excellent diff-based verification (Section 8.1). The first/last 10-word markers in the fidelity index enable concrete verification without needing the full diff toolchain.

MINOR: No concrete example is provided showing what a "loading declaration" looks like in the refactored SKILL.md. The spec references the sc-adversarial-protocol pattern (e.g., `Load refs/scoring-protocol.md before executing scoring.`) but the adversarial protocol actually uses `See refs/artifact-templates.md Section 1` -- inline reference, not a `Load` directive.

RECOMMENDATION: Add a concrete example of the loading declaration format to FR-PRD-R.6, e.g.:

```markdown
### A.7: Build the Task File

**Reference files for this phase:**
- Read `refs/build-request-template.md` for the BUILD_REQUEST format
- The BUILD_REQUEST directs the builder to read `refs/agent-prompts.md`,
  `refs/synthesis-mapping.md`, and `refs/validation-checklists.md`
```

This resolves the ambiguity about what "loading declaration" means concretely and aligns with the actual pattern used by sc-adversarial-protocol (`See refs/...`), which is an inline reference rather than a formal `Load` directive.

---

### Martin Fowler -- Architecture & Design

**Decomposition boundaries**

The 4-file decomposition is well-motivated. The decision table (Section 2.1) is thorough. The grouping by usage phase is correct: agent prompts are co-loaded during A.7, validation content is co-loaded during Phase 5-6 (via the builder), and the BUILD_REQUEST is a single self-contained template.

MINOR: The spec names the reference architecture as `sc-adversarial-protocol` but that skill's SKILL.md is actually 2,935 lines -- itself violating the 500-line guidance. This doesn't invalidate the PRD refactoring spec, but citing a 2,935-line SKILL.md as the "gold standard" for decomposition is architecturally ironic. The refs/ pattern from adversarial-protocol is valid; the SKILL.md size is not.

RECOMMENDATION: Clarify that the reference is specifically to the refs/ lazy-loading pattern from sc-adversarial-protocol, not its SKILL.md size compliance. This is documentation accuracy, not a blocking issue.

**Module dependency graph completeness**

The dependency graph in Section 4.4 correctly shows that `refs/build-request-template.md` references the other 3 refs. This is the key architectural insight -- the BUILD_REQUEST is the hub.

No issues found with the dependency structure.

**B30 merge strategy**

The B30 (Artifact Locations) vs B05 (Output Locations) merge is correctly identified as a deduplication. Diff analysis confirms B30 has 6 unique rows (specific QA report paths: analyst-completeness-report, analyst-synthesis-review, qa-research-gate-report, qa-synthesis-gate-report, qa-report-validation, qa-qualitative-review) that do not appear in B05's generalized patterns (`qa/analyst-report-[gate].md`, `qa/qa-report-[gate].md`). B30 also has a different codebase research file naming pattern (`[NN]-[topic].md` vs B05's `[NN]-[topic-name].md`).

MAJOR: The spec says "Merge B30 into B05 during refactoring. Add the analyst/QA report paths from B30 to the B05 table." But this is not a pure "add unique rows" merge -- B30's QA rows are more specific than B05's generalized pattern rows. The implementer needs to decide: keep B05's generalized patterns AND add B30's specific paths (resulting in partial duplication), or replace B05's generalized QA rows with B30's specific ones (cleaner but a content change). The spec does not specify which strategy.

RECOMMENDATION: Add a merge strategy decision to GAP-01 resolution:
- **Option A** (recommended): Keep B05's generalized patterns; append B30's specific QA paths as additional rows. Mark the generalized rows with a note that specific paths are listed below. This preserves all content word-for-word.
- **Option B**: Replace B05's generalized QA rows with B30's specific ones. This is cleaner but constitutes a minor content change that technically violates the "zero content loss" fidelity requirement.

Also note the minor naming discrepancy: B05 uses `[NN]-[topic-name].md` for codebase research while B30 uses `[NN]-[topic].md`. The merge must preserve both or choose one.

---

### Michael Nygard -- Reliability & Failure Modes

**Failure mode: Builder can't resolve refs/ paths**

The spec identifies this risk (Risk table, row 4) with the mitigation "Builder is spawned from the SKILL.md directory. Refs/ paths are relative to the skill directory." This is correct for the current Claude Code execution model where subagents inherit the working directory context.

MINOR: The spec does not specify what error message or fallback behavior occurs if a refs/ file is missing (e.g., deleted or renamed). The current monolithic approach has no such failure mode since all content is inline.

RECOMMENDATION: Add to Risk table: "refs/ file missing or renamed" with mitigation "Builder fails explicitly with file-not-found. Rollback: revert to monolithic SKILL.md from git history." This is low priority since the failure is obvious and self-diagnosing.

**Guard condition: SKILL.md line count ceiling**

The 500-line hard ceiling is a guard condition. The spec handles this well with both a target range (430-480) and a hard ceiling (500), giving 20-70 lines of headroom.

No issues found.

---

### James Whittaker -- Adversarial Analysis

**Attack 1: Sentinel Collision -- "section" string in BUILD_REQUEST**

MAJOR: The cross-reference update map (Section 12.2) lists 13 specific reference updates. The spec says to `grep` for stale section references after refactoring (Test 8.3). However, the grep tests only check SKILL.md for stale references. They do NOT check `refs/build-request-template.md` itself for any remaining "section" references that should have been updated but weren't.

Concrete attack: If the implementer copies the BUILD_REQUEST verbatim to `refs/build-request-template.md` and updates only 12 of the 13 references, the 13th stale reference survives. The cross-reference tests in 8.3 only grep SKILL.md, not the refs/ files. The stale reference would go undetected.

RECOMMENDATION: Add to Section 8.3 (Cross-Reference Tests):
```
grep -c '".*section"' refs/build-request-template.md returns 0
  (or returns only the "Tier Selection" reference which stays as SKILL.md)
```

**Attack 2: Accumulation -- Line count arithmetic**

MINOR: The fidelity index says "Total mapped lines: 1,373 (B01 line 1 through B32 line 1,373 -- full coverage, zero gaps)." Let me verify: B01 ends at line 4, B02 starts at line 6. Lines 5 is unaccounted. Similarly, all the `---` separator lines between sections may or may not be counted. The block inventory shows B32 ending at line 1,373, but the actual file has 1,373 lines (confirmed by `wc -l`), and there is actually a blank line 1,374.

The fidelity index blocks have gaps between them (e.g., B01 lines 1-4, B02 lines 6-30 -- line 5 is the `---` frontmatter delimiter). These inter-block lines (separators, blank lines) total approximately 30-40 lines. They are not explicitly mapped in any block.

RECOMMENDATION: Add a note to the fidelity index: "Inter-block separator lines (---), blank lines, and the frontmatter closing delimiter are structural formatting and are preserved in whichever destination file contains the adjacent blocks. They are not individually catalogued."

**Attack 3: Sequence -- Implementation order parallelism**

The implementation order (Section 4.6) says steps 2a/2b/2c are parallel, then step 3 depends on step 2. This is correct. Step 4 depends on steps 2 and 3. Step 5 depends on step 4.

No issues found -- the dependency chain is well-specified.

**Attack 4: Zero/Empty -- What if the original SKILL.md changes before implementation?**

MINOR: The spec pins all line ranges to the current 1,373-line version of SKILL.md. If any change is made to SKILL.md between spec creation and implementation (e.g., a bug fix to an agent prompt), all line ranges in the fidelity index become stale.

RECOMMENDATION: Add to Section 7 (Risk Assessment): "Spec freshness -- if SKILL.md is modified between spec creation and implementation, all line ranges in the fidelity index must be re-verified. Mitigation: implement this refactoring before any content changes to the PRD skill." Alternatively, pin the spec to a specific git commit hash.

**Attack 5: Divergence -- B13 cross-reference update ambiguity**

The cross-reference map includes one reference in B13 (Stage B, line ~550): `agent prompts, validation criteria, and content rules` becomes `from refs/agent-prompts.md and refs/validation-checklists.md`. But B13 stays in SKILL.md (it is behavioral content). The question is: should SKILL.md's Stage B section reference refs/ file paths when Stage B itself never loads refs/ files? The spec says Stage B "delegates to /task which reads the task file, not SKILL.md." So the refs/ reference in B13 would be informational only.

MINOR: This is not a correctness issue but could confuse implementers. The B13 text is explaining what content is baked into the task file, not instructing the agent to load refs/ at that point.

RECOMMENDATION: In the cross-reference map, annotate the B13 entry: "(informational reference only -- Stage B does not load refs/ files; this text explains what was baked into the task file during A.7)."

---

### Lisa Crispin -- Testing Strategy

**Fidelity test coverage**

Section 8.1 has 8 diff-based tests covering all content categories. This is thorough.

**Structural test gap**

MINOR: Section 8.2 tests check individual file line counts and combined total, but do not verify that SKILL.md no longer contains any agent prompt content. A structural test should verify that `grep -c '### Codebase Research Agent Prompt' SKILL.md` returns 0 -- confirming the prompts were actually removed, not just duplicated into refs/.

RECOMMENDATION: Add to Section 8.2:
```
grep -c 'Agent Prompt' SKILL.md returns 0 or 1 (only the loading declaration reference)
grep -c 'Assembly Process' SKILL.md returns 0
grep -c 'Content Rules' SKILL.md returns 0
```

These tests verify removal from SKILL.md, not just presence in refs/.

**E2E test specificity**

MINOR: Section 8.4 has 3 manual/E2E scenarios but no pass/fail criteria for the first scenario ("Stage A completes, task file created...Stage B executes all phases successfully"). What does "successfully" mean? Does the final PRD need to match a baseline, or just complete without errors?

RECOMMENDATION: Define "successfully" as: "Stage B completes with all task file checklist items checked, and a PRD file is written to the expected output location. Content quality is out of scope for this refactoring test -- the goal is identical execution behavior, not output quality."

---

## Guard Condition Boundary Table

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| SKILL.md line ceiling | FR-PRD-R.1 | At target | 480 lines | pass | Within 430-500 range | OK |
| SKILL.md line ceiling | FR-PRD-R.1 | At maximum | 500 lines | pass | At hard ceiling | OK |
| SKILL.md line ceiling | FR-PRD-R.1 | Over maximum | 501 lines | fail | Spec says "hard ceiling: 500" | OK |
| SKILL.md line ceiling | FR-PRD-R.1 | Below target | 429 lines | pass | Below range but not a failure per spec | GAP |
| refs/ file count | Section 8.2 | Correct | 4 files | pass | Expected count | OK |
| refs/ file count | Section 8.2 | Missing file | 3 files | fail | Unspecified failure behavior | GAP |
| Combined line count | FR-PRD-R.7 | At expected | ~1,373 | pass | "approximately equals" | OK |
| Combined line count | FR-PRD-R.7 | Significantly over | 1,500+ | unclear | "approximately" is vague | GAP |

**Findings from GAP entries:**

MAJOR (row 4): If SKILL.md comes in under 429 lines, the spec's range (430-500) would flag it as out of range, but this is likely acceptable. The spec should clarify: is 430 a soft floor or a hard floor? If removing B30's duplicate content brings SKILL.md below 430, is that acceptable?

MAJOR (row 6): No failure behavior specified when a refs/ file is missing. See Nygard's recommendation above.

MAJOR (row 8): "approximately equals" is not a testable criterion. See Wiegers' recommendation above.

---

## Findings Summary

### By Severity

| Severity | Count | Issues |
|----------|-------|--------|
| CRITICAL | 0 | -- |
| MAJOR | 5 | FR-PRD-R.6 loading model conflation; B30 merge strategy unspecified; stale ref grep coverage gap; SKILL.md floor ambiguity; "approximately" line count |
| MINOR | 7 | Reference architecture irony; loading declaration format example; inter-block separators unmapped; spec freshness risk; B13 cross-ref annotation; structural removal tests; E2E pass criteria |

### By Focus Area

| Focus | Issues | Key Finding |
|-------|--------|-------------|
| Correctness | 4 | Cross-reference grep tests must cover refs/ files, not just SKILL.md |
| Architecture | 3 | B30 merge strategy needs explicit decision; loading model (orchestrator vs builder) needs clarity in FR-PRD-R.6 |
| Completeness | 3 | Missing refs/ file failure behavior; inter-block line mapping; spec freshness |
| Testability | 2 | "approximately equals" is not testable; E2E needs pass criteria |

---

## Consensus Recommendations (Priority-Ranked)

### Must Fix Before Implementation

1. **Revise FR-PRD-R.6** to distinguish orchestrator loading (build-request-template.md only) from builder loading (the other 3 refs). The current wording implies the orchestrator loads all 4 refs, which contradicts Section 2.2.

2. **Add cross-reference grep test for refs/build-request-template.md** (Section 8.3). Without this, a stale "section" reference in the BUILD_REQUEST would escape detection.

3. **Specify B30 merge strategy** explicitly. The implementer needs to know whether to append B30's specific QA paths alongside B05's generalized patterns (recommended) or replace them.

### Should Fix Before Implementation

4. **Replace "approximately equals" in FR-PRD-R.7** with a numeric range (1,370-1,400).

5. **Add a concrete loading declaration example** to FR-PRD-R.6 showing the actual SKILL.md text at A.7.

6. **Add structural removal tests** to Section 8.2 confirming agent prompts, checklists, etc. are absent from the refactored SKILL.md.

### Nice to Have

7. Pin the spec to a git commit hash for SKILL.md to prevent line range drift.

8. Annotate B13 cross-reference as informational.

9. Note inter-block separator handling in fidelity index.

---

## Panel Verdict

**PASS WITH MINOR REVISIONS**

The spec is well-constructed, with thorough content mapping (32 blocks, all accounted for), a clear decomposition rationale, and strong fidelity testing. The 3 "must fix" items are straightforward revisions (clarify wording, add one grep test, specify merge strategy) that do not require architectural changes. An implementer could execute this spec with high confidence after addressing items 1-3.

The fidelity index is the spec's strongest asset -- the first/last 10-word markers and cross-reference map make implementation verification mechanical rather than judgmental.

No blocking architectural concerns. The refs/ pattern is correctly applied and the phase-to-loading mapping is sound.
