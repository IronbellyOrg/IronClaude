# TDD Skill Refactoring — Fidelity Index

> Purpose: Full content preservation map for `/config/workspace/IronClaude/.claude/skills/tdd/SKILL.md`.
>
> Source baseline used for this index: **1,364 lines** (actual repository file on 2026-04-02).
> Master prompt cites 1,387 lines; this discrepancy is tracked as GAP-TDD-01.
>
> Verification marker format per block: first 10 words + last 10 words.

---

## Legend

| Column | Meaning |
|--------|---------|
| Block ID | Sequential block identifier |
| Lines | Inclusive source range in original SKILL.md |
| Type | `behavioral` (WHAT/WHEN) or `reference` (HOW) |
| Phase Need | Stage/phase where block is needed |
| Destination | Target file in decomposed architecture |
| Checksum Marker | First 10 words / Last 10 words |

---

## Content Block Inventory

| Block ID | Lines | Type | Phase Need | Destination |
|----------|-------|------|------------|-------------|
| B01 | 1-4 | behavioral | Invocation | SKILL.md frontmatter |
| B02 | 6-30 | behavioral | Invocation | SKILL.md purpose/overview |
| B03 | 33-77 | behavioral | Invocation, Stage A | SKILL.md Input section |
| B04 | 80-95 | behavioral | Stage A | SKILL.md Tier Selection |
| B05 | 98-130 | behavioral | Stage A | SKILL.md Output Locations |
| B06 | 133-161 | behavioral | Stage A/B | SKILL.md Execution Overview |
| B07 | 164-202 | behavioral | Stage A | SKILL.md A.1-A.2 |
| B08 | 203-252 | behavioral | Stage A | SKILL.md A.3 |
| B09 | 253-297 | behavioral | Stage A | SKILL.md A.4 |
| B10 | 298-322 | behavioral | Stage A | SKILL.md A.5 |
| B11 | 323-340 | behavioral | Stage A | SKILL.md A.6 |
| B12 | 341-492 | reference | Stage A.7 | refs/build-request-template.md |
| B13 | 493-510 | behavioral | Stage A.7-A.8 | SKILL.md A.7 spawn + A.8 verify |
| B14 | 513-535 | behavioral | Stage B | SKILL.md Stage B delegation |
| B15 | 537-627 | reference | Phase 2/3/6 prompt embed | refs/agent-prompts.md |
| B16 | 628-677 | reference | Phase 4 prompt embed | refs/agent-prompts.md |
| B17 | 678-712 | reference | Phase 5 prompt embed | refs/agent-prompts.md |
| B18 | 713-751 | reference | Phase 3 prompt embed | refs/agent-prompts.md |
| B19 | 752-797 | reference | Phase 3 prompt embed | refs/agent-prompts.md |
| B20 | 798-841 | reference | Phase 5 prompt embed | refs/agent-prompts.md |
| B21 | 842-890 | reference | Phase 6 prompt embed | refs/agent-prompts.md |
| B22 | 891-959 | reference | Phase 6 prompt embed | refs/agent-prompts.md |
| B23 | 962-1083 | reference | Phase 5/6 | refs/synthesis-mapping.md |
| B24 | 1084-1105 | reference | Phase 5 | refs/synthesis-mapping.md |
| B25 | 1106-1127 | reference | Phase 5 QA | refs/validation-checklists.md |
| B26 | 1128-1173 | reference | Phase 6 assembly | refs/validation-checklists.md |
| B27 | 1174-1217 | reference | Phase 6 validation | refs/validation-checklists.md |
| B28 | 1218-1245 | reference | Phase 5/6 writing standards | refs/validation-checklists.md |
| B29 | 1246-1283 | behavioral | All phases | refs/operational-guidance.md |
| B30 | 1284-1313 | behavioral | Stage A/2/3 quality triage | refs/operational-guidance.md |
| B31 | 1314-1334 | behavioral | All phases | refs/operational-guidance.md |
| B32 | 1335-1348 | behavioral | PRD-fed flow | refs/operational-guidance.md |
| B33 | 1349-1361 | behavioral | Update mode | refs/operational-guidance.md |
| B34 | 1362-1364 | behavioral | Session resume | refs/operational-guidance.md |

---

## Checksum-Style Verification Markers

| Block ID | First 10 words | Last 10 words |
|----------|----------------|---------------|
| B01 | --- name: tdd description: "Create or populate a Technical Design | this feature', or 'turn this PRD into a TDD'." --- |
| B02 | # TDD Creator Creates comprehensive Technical Design Documents (TDDs) for | be re-verified later, and feed directly into the assembled TDD. |
| B03 | ## Input The skill needs four pieces of information to | #1 answered clearly. Items #2-4 improve quality but aren't blockers. |
| B04 | ## Tier Selection Match the tier to component scope. **Default | multiple services, architectural layers, or integration boundaries — always Heavyweight |
| B05 | ## Output Locations All persistent artifacts go into the task | the same component, read it first and build on it. |
| B06 | ## Execution Overview The skill operates in two stages: **Stage | and invoke `/task` to resume from the first unchecked item. |
| B07 | ## Stage A: Scope Discovery & Task File Creation ### | the Input section only when the request truly cannot proceed. |
| B08 | ### A.3: Perform Scope Discovery Use Glob, Grep, and codebase-retrieval | file. You then use those notes as input for A.4. |
| B09 | ### A.4: Write Research Notes File (MANDATORY) Write the scope | intent is clear from the request and codebase context."] ``` |
| B10 | ### A.5: Review Research Sufficiency (MANDATORY GATE) **You MUST review | the codebase effectively — it relies on what you provide. |
| B11 | ### A.6: Template Triage Determine which MDTM template the task | 4), synthesis (Phase 5), and assembly with validation (Phase 6). |
| B12 | ### A.7: Build the Task File Spawn the `rf-task-builder` subagent. | PART 2 structure 7. Return the task file path ``` |
| B13 | **Spawning the builder:** Use the Agent tool with `subagent_type: "rf-task-builder"` | the builder with specific corrections. Otherwise, proceed to Stage B. |
| B14 | ## Stage B: Task File Execution Stage B delegates execution | code snippets unless the TDD documents existing implementation patterns. --- |
| B15 | ## Agent Prompt Templates These templates are provided to the | the actual source code of X verifies X exists. ``` |
| B16 | ### Web Research Agent Prompt ``` Research this topic externally | component type (e.g., caching strategies, message queue patterns, database scaling) |
| B17 | ### Synthesis Agent Prompt ``` Read the research files listed | including all table structures and headers from the template. ``` |
| B18 | ### Research Analyst Agent Prompt (rf-analyst — Completeness Verification) ``` | job is to find problems, not confirm things work. ``` |
| B19 | ### Research QA Agent Prompt (rf-qa — Research Gate) ``` | tolerance — if you can't verify it, it fails. ``` |
| B20 | ### Synthesis QA Agent Prompt (rf-qa — Synthesis Gate) ``` | (list with specific fixes, note which were fixed in-place) ``` |
| B21 | ### Report Validation QA Agent Prompt (rf-qa — Report Validation) | Specifications alone) Fix every issue you find. Report honestly. ``` |
| B22 | ### Assembly Agent Prompt (rf-assembler — TDD Assembly) ``` Assemble | should be candidates for archival (the TDD replaces them) ``` |
| B23 | ## Output Structure > **Note:** This section is reference documentation. | Database Schema, C: Wireframes, D: Performance Test Results. ``` --- |
| B24 | ## Synthesis Mapping Table > **Note:** This section is reference | Small components can combine more sections per synth file. --- |
| B25 | ## Synthesis Quality Review Checklist > **Note:** This section is | issues remaining unfixed trigger re-synthesis of the affected files. --- |
| B26 | ## Assembly Process > **Note:** This section is reference documentation. | items in the stub's consolidation checklist if one exists --- |
| B27 | ## Validation Checklist > **Note:** This section is reference documentation. | structure with tables, headers, bullets; no walls of prose --- |
| B28 | ## Content Rules (From Template — Non-Negotiable) These rules come | Prefer ASCII/Mermaid diagrams for visual relationships over paragraph descriptions --- |
| B29 | ## Critical Rules (Non-Negotiable) These are SKILL-SPECIFIC content rules that | invisible to the F1 executor and will be skipped. --- |
| B30 | ## Research Quality Signals ### Strong Investigation Signals - Findings | - Web research reveals patterns that need codebase verification --- |
| B31 | ## Artifact Locations | Artifact | Location | |----------|----------| | | and can be re-used when the document needs updating. --- |
| B32 | ## PRD-to-TDD Pipeline When a PRD is provided as input, | into engineering specifications without information loss or scope drift. --- |
| B33 | ## Updating an Existing TDD When the user wants to | Updated date 6. Update Document History with what changed --- |
| B34 | ## Session Management Session management is provided by the `/task` | file, reads it, and resumes from the first unchecked item. |

---

## Cross-Reference Map (Required Path Updates)

These source references (inside BUILD_REQUEST and phase guidance) must be updated to concrete refs paths in the decomposed architecture.

| Source Reference Phrase | Destination Reference |
|-------------------------|-----------------------|
| "Agent Prompt Templates section" | `refs/agent-prompts.md` |
| "Synthesis Mapping Table section" | `refs/synthesis-mapping.md` |
| "Synthesis Quality Review Checklist section" | `refs/validation-checklists.md` |
| "Assembly Process section" | `refs/validation-checklists.md` |
| "Validation Checklist section" | `refs/validation-checklists.md` |
| "Content Rules section" | `refs/validation-checklists.md` |
| "Tier Selection section" | stays in SKILL.md |

Additional phrase updates needed in Stage A.7 body:
- "full codebase research agent prompt from SKILL.md" -> `refs/agent-prompts.md`
- "synthesis agent prompt from SKILL.md" -> `refs/agent-prompts.md`
- "Assembly Process steps from SKILL.md" -> `refs/validation-checklists.md`
- "Content Rules from SKILL.md" -> `refs/validation-checklists.md`

---

## Destination Summary and Coverage

| Destination File | Source Blocks |
|------------------|---------------|
| SKILL.md | B01-B11, B13-B14 |
| refs/build-request-template.md | B12 |
| refs/agent-prompts.md | B15-B22 |
| refs/synthesis-mapping.md | B23-B24 |
| refs/validation-checklists.md | B25-B28 |
| refs/operational-guidance.md | B29-B34 |

Coverage statement: All source lines **1-1364** are mapped to a destination file. No unmapped source blocks.

---

## Verification Protocol

1. For each block, extract destination text and compare with source line range.
2. Confirm first-10 and last-10 markers match this index.
3. Validate that only expected cross-reference path changes exist in BUILD_REQUEST content.
4. Confirm no behavioral semantics changed.
5. Confirm no placeholder sentinels remain in release-spec outputs.
