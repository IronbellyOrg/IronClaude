---
high_severity_count: 0
medium_severity_count: 6
low_severity_count: 3
total_deviations: 9
validation_complete: true
tasklist_ready: true
---

## Deviation Report

**DEV-001**
- **Severity**: MEDIUM
- **Deviation**: NFR-PRD-R.1 token budget downgraded from stated requirement to "soft target" via roadmap's OQ-1 resolution
- **Source Quote**: `NFR-PRD-R.1 | SKILL.md token budget | <= 2,000 tokens on invocation`
- **Roadmap Quote**: `Token budget | Line count × 4.5 | ≤ 2,000 (soft target)` and `OQ-1 ... 500-line hard ceiling takes precedence; 2,000-token target is soft. Accept up to ~3.5% token overshoot if within line ceiling.`
- **Impact**: The roadmap unilaterally reinterprets a spec NFR as advisory. However, the spec's own measurement column acknowledges the estimate range of ~1,935-2,160 tokens, making this a pragmatic interpretation rather than a contradiction. Risk is low since the line ceiling provides the binding constraint.
- **Recommended Correction**: Add a note in OQ-1 that the spec author should confirm this interpretation, or amend the spec's NFR-PRD-R.1 measurement to acknowledge the soft nature. The roadmap already flags this: "confirm with spec author if challenged during review."

**DEV-002**
- **Severity**: MEDIUM
- **Deviation**: Cross-reference validation tests for `refs/build-request-template.md` from spec Section 8.3 are missing from the roadmap's 12 success criteria
- **Source Quote**: `grep -c '".*section"' refs/build-request-template.md returns 0 (or only "Tier Selection" which stays in SKILL.md)` and `grep -c 'Agent Prompt Templates section' refs/build-request-template.md returns 0`
- **Roadmap Quote**: Success criterion #7: `Zero stale section refs | grep -c '".*section"' SKILL.md | 0` — tests SKILL.md only, not build-request-template.md
- **Impact**: Stale prose section references could survive in the BUILD_REQUEST file without being caught by the success criteria. Task 2.4 describes the updates but doesn't include a negative verification grep against the build-request-template.md file in the formal success criteria table.
- **Recommended Correction**: Add a success criterion #13: `grep -c '".*section"' refs/build-request-template.md` returns 0 or 1 (only "Tier Selection"). Alternatively, expand SC #7 to cover both files.

**DEV-003**
- **Severity**: MEDIUM
- **Deviation**: Spec Section 8.4 functional test scenario 3 (grep task file output for stale "section" references) not included in roadmap verification
- **Source Quote**: `Verify no stale references | Grep task file output for "section" references to SKILL.md | Zero matches — all references should be to refs/ file paths or baked-in content`
- **Roadmap Quote**: Task 4.4 mentions only: `Verify: Stage A completes, task file created with all prompts baked in. Verify: Stage B completes, PRD written to expected output location. Verify: Output structure matches pre-refactoring behavior.`
- **Impact**: The generated task file could contain stale section references without detection. This is the downstream artifact that builder subagents and `/task` consume — stale references there would cause runtime failures.
- **Recommended Correction**: Add to task 4.4: "Grep generated task file for 'section' references to SKILL.md — zero matches expected."

**DEV-004**
- **Severity**: MEDIUM
- **Deviation**: Spec Section 8.2 individual structural grep tests not enumerated as automatable success criteria
- **Source Quote**: `grep -c 'Assembly Process' SKILL.md returns 0`, `grep -c 'Content Rules' SKILL.md returns 0`, `grep -c 'Agent Prompt' SKILL.md returns 0 or 1`, `grep -c 'Validation Checklist' SKILL.md returns 0 or 1`
- **Roadmap Quote**: Phase 3 Exit Criteria prose: `Does NOT contain: agent prompt templates, validation checklists, synthesis mapping tables, assembly process steps, content rules tables, BUILD_REQUEST format, output structure reference`
- **Impact**: The roadmap covers these as exit criteria prose but not as automatable checks in the success criteria table. An implementer running only the 12 numbered success criteria would skip these grep verifications. Risk is mitigated by the exit criteria, but the spec clearly intended these as explicit test commands.
- **Recommended Correction**: Either add these 4 grep checks to the success criteria table, or add a note in task 4.2 that Phase 3 exit criteria greps must also pass as part of the validation sweep.

**DEV-005**
- **Severity**: MEDIUM
- **Deviation**: Spec Section 12.2 B13 informational-only warning not addressed in roadmap
- **Source Quote**: `Note on B13 (Stage B, line ~550): The reference to refs/agent-prompts.md and refs/validation-checklists.md in Stage B is **informational only** — Stage B does not load refs/ files. This text explains what content was baked into the task file during A.7, not an instruction for the agent to load refs/ at that point.`
- **Roadmap Quote**: '[MISSING]'
- **Impact**: Without this warning, an implementer refactoring Stage B text in SKILL.md might add loading declarations there, violating FR-PRD-R.6's requirement that "No other phase in SKILL.md loads refs/ files." The roadmap's Phase 3 task 3.2 says "Confirm: no other phase (A.1–A.6, Stage B) loads refs/ files" which is the correct constraint, but it doesn't explain the B13 nuance that could cause an implementer to mistakenly add refs/ loading at Stage B.
- **Recommended Correction**: Add a note in task 3.2 or 3.3: "B13 (Stage B) may reference refs/ paths informationally — these explain what was baked in during A.7, not loading instructions. Do not add loading declarations at Stage B."

**DEV-006**
- **Severity**: MEDIUM
- **Deviation**: Effort estimate divergence between spec and roadmap
- **Source Quote**: Section 10, For sc:tasklist: `Estimated effort: 1-2 hours. Can be completed in a single session.`
- **Roadmap Quote**: Frontmatter: `estimated_effort: "4-6 hours implementation + 2-3 hours verification (including E2E)"` and Timeline: `Total | 5–8 hours`
- **Impact**: Downstream tasklist generation using spec Section 10 would produce a 1-2 hour estimate, while the roadmap budgets 5-8 hours. The spec's estimate appears to cover only the mechanical extraction work, while the roadmap includes preparation, verification, and E2E testing. This mismatch could affect scheduling if the tasklist consumer uses the spec's estimate.
- **Recommended Correction**: Update spec Section 10 to note that the 1-2 hour estimate covers extraction only, with total effort including verification at 5-8 hours per roadmap analysis. Or clarify the roadmap's scope includes padding the spec didn't intend.

**DEV-007**
- **Severity**: LOW
- **Deviation**: BUILD_REQUEST source line range discrepancy between FR-PRD-R.5 and roadmap
- **Source Quote**: FR-PRD-R.5: `Contains the complete BUILD_REQUEST format block currently embedded in A.7 (original lines 347-508)`
- **Roadmap Quote**: Task 2.4: `Extract block B11 (lines 344–508): complete BUILD_REQUEST format`
- **Impact**: The spec itself is internally inconsistent — FR-PRD-R.5 says 347-508 while Section 12.1 says B11 is 344-508. The roadmap follows the fidelity index (344-508). Lines 344-346 likely contain the section header preceding the BUILD_REQUEST block. No functional impact — the fidelity index is the authoritative source for line ranges.
- **Recommended Correction**: Align FR-PRD-R.5 to say "lines 344-508" to match the fidelity index block definition, or clarify that 347 excludes the section header.

**DEV-008**
- **Severity**: LOW
- **Deviation**: Spec migration step 6 "Merge to integration branch" not included in roadmap
- **Source Quote**: Section 9, Migration steps: `6. Merge to integration branch for testing`
- **Roadmap Quote**: Task 4.5 ends at atomic commit. '[MISSING]' for integration merge.
- **Impact**: Minimal — this is a downstream workflow action, not an implementation step. The roadmap correctly scopes to the feature branch commit. The merge is a post-roadmap activity.
- **Recommended Correction**: Optionally add a "Post-Phase 4" note: "Merge feature branch to integration for testing per spec Section 9."

**DEV-009**
- **Severity**: LOW
- **Deviation**: Roadmap introduces whitespace normalization constraints not in spec
- **Source Quote**: FR-PRD-R.2 acceptance criteria: `Diff of each prompt template against the original SKILL.md shows zero content changes (whitespace normalization permitted)`
- **Roadmap Quote**: OQ-4: `Permit trailing whitespace removal and line-ending normalization (CRLF→LF). Do NOT permit indentation changes or blank line consolidation — these could alter markdown rendering of code blocks and tables.`
- **Impact**: The roadmap is more restrictive than the spec, which is the safer direction. The spec says "whitespace normalization permitted" without scoping it. The roadmap's constraints prevent accidental markdown rendering changes. No risk of incorrect implementation — this is a tightening, not a loosening.
- **Recommended Correction**: No action required. Consider backporting OQ-4's constraints into the spec's acceptance criteria for clarity.

## Summary

**Severity distribution**: 0 HIGH, 6 MEDIUM, 3 LOW (9 total deviations)

The roadmap is a faithful and thorough translation of the spec. No HIGH severity deviations were found — all functional requirements, architectural decisions, data models, and integration wiring from the spec are represented in the roadmap.

The 6 MEDIUM deviations fall into two categories:
1. **Test coverage gaps** (DEV-002, DEV-003, DEV-004): The roadmap consolidates the spec's 31 explicit tests into 12 success criteria, losing some negative-verification greps — particularly for `refs/build-request-template.md` stale references and task file output validation.
2. **Interpretation/alignment issues** (DEV-001, DEV-005, DEV-006): The NFR token budget softening, missing B13 informational warning, and effort estimate divergence are pragmatic but should be explicitly reconciled with the spec author.

The 3 LOW deviations are minor (line range discrepancy matching spec-internal inconsistency, omitted post-implementation merge step, and a safely-restrictive whitespace constraint addition).

**Tasklist readiness**: The roadmap is ready for tasklist generation. The MEDIUM deviations are addressable as additive corrections (additional success criteria, clarifying notes) without structural changes to the roadmap's phasing or task decomposition.
