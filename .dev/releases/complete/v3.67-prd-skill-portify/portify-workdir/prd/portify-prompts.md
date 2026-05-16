---
pipeline_name: prd
companion_to: portify-spec.md
status: completed
---

# PRD Pipeline Prompt Builders

> Companion to `portify-spec.md` Section 7. Each function returns a `str` prompt for a Claude subprocess.

---

## 1. build_parse_request_prompt

Step 2: Parse the raw user request into structured fields.

```python
def build_parse_request_prompt(config: PrdConfig) -> str:
    return f"""Parse the following product request into structured JSON.

User request:
---
{config.user_message}
---

Extract these fields and return valid JSON:

{{
  "GOAL": "<one-sentence description of the PRD's purpose>",
  "PRODUCT_NAME": "<human-readable product name>",
  "PRODUCT_SLUG": "<kebab-case identifier>",
  "PRD_SCOPE": "<product|feature>",
  "SCENARIO": "<A|B>",
  "WHERE": [<list of source directories to focus on>],
  "WHY": "<purpose of the PRD>",
  "TIER_RECOMMENDATION": "<lightweight|standard|heavyweight>"
}}

Scenario Classification:
- Scenario A (explicit): User provides specific product name, source directories, and clear scope
- Scenario B (vague): User provides broad description, requires codebase exploration to scope

Tier Recommendation:
- Lightweight: Single feature, narrow scope, 2-3 research agents
- Standard: Multi-feature or product area, 4-6 research agents
- Heavyweight: Full product/platform, 6-10+ research agents

If the user request is vague (Scenario B), set SCENARIO to "B" and leave WHERE as empty list.
If the request mentions specific directories or files, extract them into WHERE.

Return ONLY the JSON object, no markdown fencing, no explanation.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 2. build_scope_discovery_prompt

Step 3: Explore the codebase to understand the product scope.

```python
def build_scope_discovery_prompt(config: PrdConfig) -> str:
    parsed = _load_json(config.task_dir / "parsed-request.json")
    where_clause = ""
    if parsed.get("WHERE"):
        where_clause = f"""\nFocus on these directories:
{chr(10).join('- ' + d for d in parsed['WHERE'])}"""
    else:
        where_clause = """\nNo specific directories provided. Explore the codebase starting from the repo root.
Use Glob and Read to understand the project structure, key source directories, and product areas."""

    return f"""Perform scope discovery for a PRD about: {parsed['GOAL']}

Product: {parsed.get('PRODUCT_NAME', 'Unknown')}
Scope: {parsed.get('PRD_SCOPE', 'feature')}
Scenario: {parsed.get('SCENARIO', 'B')}
{where_clause}

Your task is to explore the codebase and produce a comprehensive scope discovery document.

PROCESS:
1. Map the project structure — identify key source directories, configuration files, and documentation
2. Identify product areas — what distinct functional areas exist?
3. Trace user-facing features — what does the product actually do for users?
4. Document technical architecture — key technology choices, patterns, frameworks
5. Find existing documentation — READMEs, docs/, wiki references, inline comments
6. Identify integration points — APIs, external services, plugin systems
7. Assess complexity — how many distinct areas need dedicated research agents?

OUTPUT FORMAT:

Write a markdown document with these sections:

## Project Overview
[Brief description of what this project is]

## Directory Structure
[Key directories with their purposes]

## Product Areas
[Each distinct product area with description and key files]

## Technology Stack
[Languages, frameworks, key dependencies]

## Existing Documentation
[Path to each doc file found, with brief description]

## Integration Points
[External APIs, services, databases, third-party tools]

## Complexity Assessment
- Estimated research agents needed: [N]
- Key areas requiring dedicated investigation: [list]
- Cross-cutting concerns: [list]

## Recommended Research Assignments
For each recommended research agent:
- **Topic**: [specific investigation topic]
- **Type**: [Feature Analyst / Doc Analyst / Integration Mapper / UX Investigator / Architecture Analyst]
- **Files**: [specific files/directories to investigate]
- **Rationale**: [why this agent is needed]

Be thorough. Read actual files, don't guess from directory names alone.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 3. build_research_notes_prompt

Step 4: Produce structured research notes from scope discovery.

```python
def build_research_notes_prompt(config: PrdConfig) -> str:
    scope_content = _read_file(config.task_dir / "scope-discovery-raw.md")
    parsed = _load_json(config.task_dir / "parsed-request.json")

    return f"""Create structured research notes for the PRD pipeline.

Product: {parsed.get('PRODUCT_NAME', 'Unknown')}
Scope: {parsed.get('PRD_SCOPE', 'feature')}
Scenario: {parsed.get('SCENARIO', 'B')}
Tier: {config.tier}

Scope Discovery Results:
---
{scope_content}
---

Produce a research-notes.md file with EXACTLY these 7 sections (all required):

---
Date: {_today()}
Scenario: {parsed.get('SCENARIO', 'B')}
Tier: {config.tier}
---

# Research Notes: {parsed.get('PRODUCT_NAME', 'Unknown')}

## EXISTING_FILES
List every relevant source file discovered, grouped by product area.
Format: `path/to/file.ext` — brief description

## PATTERNS_AND_CONVENTIONS
Code patterns, naming conventions, architecture decisions observed.

## FEATURE_ANALYSIS
User-facing features identified, with evidence from source code.

## RECOMMENDED_OUTPUTS
List the output artifacts this PRD pipeline should produce.

## SUGGESTED_PHASES
For each research agent to spawn, provide ALL of:
- **Topic**: specific investigation area
- **Agent type**: Feature Analyst / Doc Analyst / Integration Mapper / UX Investigator / Architecture Analyst
- **Files**: specific files and directories to investigate
- **Output path**: research/NN-slug.md

Agent count guidance for tier '{config.tier}':
- Lightweight: 2-3 codebase agents, 0-1 web agents
- Standard: 4-6 codebase agents, 1-2 web agents
- Heavyweight: 6-10+ codebase agents, 2-4 web agents

## TEMPLATE_NOTES
Notes on which PRD template sections need special attention.

## AMBIGUITIES_FOR_USER
Questions that would benefit from user clarification (but don't block execution).

Every entry must have specific evidence — no generic placeholders.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 4. build_sufficiency_review_prompt

Step 5: Review research notes for completeness before proceeding.

```python
def build_sufficiency_review_prompt(config: PrdConfig) -> str:
    notes_content = _read_file(config.task_dir / "research-notes.md")

    return f"""Review the research notes for sufficiency.

Research Notes:
---
{notes_content}
---

Tier: {config.tier}

Evaluate whether these research notes provide sufficient foundation for the PRD pipeline:

1. **Coverage**: Does EXISTING_FILES cover the major source directories?
2. **Agent assignments**: Does SUGGESTED_PHASES have the right number of agents for the tier?
3. **Specificity**: Does each agent assignment have specific files, not just directories?
4. **Balance**: Are there gaps — areas mentioned in EXISTING_FILES but not assigned to any agent?
5. **Web research**: Are there topics requiring external market/competitive research?

Return JSON:
{{
  "verdict": "PASS" or "FAIL",
  "coverage_score": 0-100,
  "gaps": [
    {{
      "area": "<product area>",
      "issue": "<what's missing>",
      "severity": "critical|important|minor"
    }}
  ],
  "recommendations": ["<specific actions to fix gaps>"]
}}

A PASS requires coverage_score >= 80 and no critical gaps.
A FAIL means the research notes need augmentation before spawning agents.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 5. build_task_file_prompt

Step 7: Build the MDTM task file from research notes + refs.

```python
def build_task_file_prompt(config: PrdConfig) -> str:
    notes = _read_file(config.task_dir / "research-notes.md")
    build_template = _read_file(config.skill_refs_dir / "build-request-template.md")
    agent_prompts = _read_file(config.skill_refs_dir / "agent-prompts.md")
    synth_mapping = _read_file(config.skill_refs_dir / "synthesis-mapping.md")
    validation = _read_file(config.skill_refs_dir / "validation-checklists.md")
    operational = _read_file(config.skill_refs_dir / "operational-guidance.md")

    return f"""Build an MDTM task file for the PRD pipeline.

You are the task builder. Your job is to create a self-contained task file that
encodes the complete PRD creation workflow as a checklist.

Research Notes:
---
{notes}
---

Build Request Template:
---
{build_template}
---

Agent Prompt Templates:
---
{agent_prompts}
---

Synthesis Mapping:
---
{synth_mapping}
---

Validation Checklists:
---
{validation}
---

Operational Guidance:
---
{operational}
---

INSTRUCTIONS:
1. Follow the BUILD_REQUEST template exactly
2. Use Template 02 (complex task pattern)
3. Customize agent prompts with specific product areas, files, and output paths from the research notes
4. Each checklist item must be SELF-CONTAINED — no "see above" references
5. Encode parallel spawning instructions in Phases 2, 3, 4, and 5
6. Encode all 7 PRD skill phases into the task file structure
7. Include the synthesis mapping for Phase 4 (which synth file covers which sections)
8. Include validation checklists for Phase 5 and Phase 6

Write the task file to: {config.task_dir / 'TASK-PRD-' + config.product_slug + '.md'}

The task file frontmatter must include:
- id: TASK-PRD-{config.product_slug}
- title: Create PRD for {config.product_name}
- status: to-do
- complexity: L (large)
- created_date: {_today()}
- type: prd-creation
- tier: {config.tier}

CRITICAL: Use incremental file writing. Create the file with frontmatter first,
then append each phase section using Edit. Never one-shot the entire file.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 6. build_verify_task_file_prompt

Step 8: Verify the task file meets quality standards.

```python
def build_verify_task_file_prompt(config: PrdConfig) -> str:
    task_files = list(config.task_dir.glob("TASK-PRD-*.md"))
    task_path = task_files[0] if task_files else config.task_dir / "task-file.md"
    task_content = _read_file(task_path)

    return f"""Verify the MDTM task file for completeness and quality.

Task file:
---
{task_content}
---

Tier: {config.tier}

Verification checklist:
1. Frontmatter has all required fields (id, title, status, complexity, created_date, type, tier)
2. All 7 phases are present as section headers
3. Each phase has checklist items (- [ ] format)
4. No checklist item references "see above" or "as described above" (B2 self-containment)
5. Phases 2, 3, 4, 5 include parallel spawning instructions
6. Agent prompts in Phase 2 have specific file paths (not generic)
7. Synthesis mapping in Phase 4 maps synth files to PRD sections
8. Validation checklists in Phases 5 and 6 are present
9. Line count meets tier minimum: lightweight=200, standard=400, heavyweight=600
10. No placeholder text (TODO, TBD, PLACEHOLDER)

Return JSON:
{{
  "verdict": "PASS" or "FAIL",
  "line_count": <int>,
  "checklist_items": <count of - [ ] items>,
  "issues": [
    {{
      "check": "<check number>",
      "issue": "<description>",
      "severity": "critical|major|minor",
      "location": "<line number or section>"
    }}
  ]
}}

A PASS requires no critical issues and no more than 2 major issues.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 7. build_preparation_prompt

Step 9: Create task directories and prepare for Stage B execution.

```python
def build_preparation_prompt(config: PrdConfig) -> str:
    notes = _read_file(config.task_dir / "research-notes.md")
    task_files = list(config.task_dir.glob("TASK-PRD-*.md"))
    task_path = task_files[0] if task_files else config.task_dir / "task-file.md"

    return f"""Prepare for Stage B execution of the PRD pipeline.

Task file: {task_path}
Research directory: {config.research_dir}
Synthesis directory: {config.synthesis_dir}
QA directory: {config.qa_dir}

PREPARATION STEPS:
1. Verify all required directories exist (research/, synthesis/, qa/)
2. Create a .preparation-complete marker file
3. Verify the task file is readable and has the expected structure
4. Extract the list of research agent assignments from research-notes.md
5. Verify each assigned output path's parent directory exists

Write a brief status report to .preparation-complete:

```
Preparation Status: READY
Task file: [path]
Research agents: [count]
Web research topics: [count]
Synthesis files planned: [count]
Directories verified: research/, synthesis/, qa/
```

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 8. build_investigation_prompt

Step 10 (dynamic): Per-agent research prompt. Adapts the Codebase Research Agent template.

```python
def build_investigation_prompt(
    topic: str,
    agent_type: str,
    files: list[str],
    product_root: str,
    output_path: Path,
) -> str:
    files_list = chr(10).join(f"- {f}" for f in files)

    return f"""Research this aspect of the product and write findings to {output_path}:

Topic: {topic}
Investigation type: {agent_type}
Files to investigate:
{files_list}
Product root: {product_root}

CRITICAL -- Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create your output file immediately with this header:
   ```markdown
   # Research: {topic}

   **Investigation type:** {agent_type}
   **Scope:** [files/directories assigned]
   **Status:** In Progress
   **Date:** [today]

   ---
   ```

2. As you investigate each file, component, or logical unit, IMMEDIATELY append
   your findings to the output file using Edit. Do NOT accumulate findings in
   your context window.

3. After each append, your output file grows. This is correct behavior.
   Never rewrite the file from scratch.

4. When finished, update the Status line from "In Progress" to "Complete"
   and append a summary section.

Research Protocol:
1. Read the actual source files -- understand what each file does, what capabilities
   it provides, what user value it delivers
2. Trace user flows -- how does the user interact with this part of the product?
3. Document the product interface -- features, settings, capabilities, touchpoints
4. Identify patterns -- product conventions, design decisions, UX patterns
5. Check for edge cases -- error states, missing features, config-driven behavior
6. Note dependencies -- what does this area depend on? What depends on it?
7. Flag gaps -- what is missing, broken, undocumented, or unclear?
8. Note integration opportunities -- extension points, APIs, plugin systems

CRITICAL -- Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state.
When you encounter documentation that describes a product capability:
- **[CODE-VERIFIED]** -- confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** -- code shows different implementation
- **[UNVERIFIED]** -- could not find corresponding code; may be stale

Output Format:
- Use descriptive headers for each file or logical group
- Include actual feature capabilities, user flows, technology choices
- Note anomalies, tech debt, or surprising behavior
- End each section with "Key Takeaways" bullets
- End the file with:
  ## Gaps and Questions
  ## Stale Documentation Found
  ## Summary

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 9. build_web_research_prompt

Step 12 (dynamic): Per-topic web research prompt.

```python
def build_web_research_prompt(
    topic: str,
    context: str,
    product: str,
    output_path: Path,
) -> str:
    return f"""Research this topic externally and write findings to {output_path}.

Topic: {topic}
What we already know from codebase: {context}
Product context: {product}

CRITICAL -- Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for market data, industry reports, and competitive landscape
2. Search for comparable products and their feature sets
3. Search for industry best practices and standards
4. Search for technology trends affecting this product category
5. For each finding, document:
   - Source URL
   - Key information extracted
   - How it relates to our product's current capabilities
   - Whether it supports, extends, or contradicts codebase findings
6. Rate source reliability (official reports > industry publications > repos > blog posts > forums)

Output Format:
- Descriptive headers for each research area
- Always include source URLs
- Mark relevance: HIGH / MEDIUM / LOW
- End with:
  ## Key External Findings
  ## Recommendations from External Research

IMPORTANT: Our codebase is the source of truth for current capabilities.
External research adds market context and competitive intelligence but does
not override verified product behavior.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 10. build_analyst_completeness_prompt

Step 11 (analyst agent): Research completeness verification.

```python
def build_analyst_completeness_prompt(config: PrdConfig) -> str:
    return f"""Perform a completeness verification of all research files for the PRD.

Analysis type: completeness-verification
Research directory: {config.research_dir}
Research notes file: {config.task_dir / 'research-notes.md'}
Tier: {config.tier}
Output path: {config.qa_dir / 'analyst-completeness-report.md'}

Your job is to independently verify that research agents produced thorough,
evidence-based findings before downstream synthesis begins.

PROCESS:
1. Read the research-notes.md to understand planned scope (EXISTING_FILES, SUGGESTED_PHASES)
2. Use Glob to find ALL research files in {config.research_dir} (files matching [NN]-*.md)
3. Read EVERY research file -- do not skip any
4. Apply the 8-item checklist below
5. Write your report to the output path

CHECKLIST:
1. Coverage audit -- every key product area from scope covered by at least one file
2. Evidence quality -- claims cite specific file paths, feature names, capabilities
3. Documentation staleness -- all doc-sourced claims tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED]
4. Completeness -- every file has Status: Complete, Summary section, Gaps section
5. Cross-reference check -- cross-cutting concerns covered by multiple agents are cross-referenced
6. Contradiction detection -- conflicting findings about the same feature surfaced
7. Gap compilation -- all gaps unified, deduplicated, severity-rated (Critical/Important/Minor)
8. Depth assessment -- investigation depth matches tier '{config.tier}'

VERDICTS:
- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action)

Be adversarial -- your job is to find problems, not confirm things work.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 11. build_qa_research_gate_prompt

Step 11 (QA agent): Research gate verification.

```python
def build_qa_research_gate_prompt(config: PrdConfig) -> str:
    analyst_report = config.qa_dir / "analyst-completeness-report.md"
    has_analyst = analyst_report.exists()

    return f"""Perform QA verification of research completeness for the PRD.

QA phase: research-gate
Research directory: {config.research_dir}
Analyst report: {analyst_report} ({'exists' if has_analyst else 'not found'})
Research notes file: {config.task_dir / 'research-notes.md'}
Tier: {config.tier}
Output path: {config.qa_dir / 'qa-research-gate-report.md'}

You are the last line of defense before synthesis begins.
Assume everything is wrong until you verify it.

{'IF ANALYST REPORT EXISTS:' if has_analyst else 'NO ANALYST REPORT -- apply full checklist independently.'}
{'1. Read the analyst completeness report' if has_analyst else ''}
{'2. Spot-check 3-5 of their coverage audit claims' if has_analyst else ''}
{'3. Validate gap severity classifications' if has_analyst else ''}
{'4. Check their verdict against your own independent assessment' if has_analyst else ''}

11-ITEM CHECKLIST:
1. File inventory -- all research files exist with Status: Complete and Summary
2. Evidence density -- sample 3-5 claims per file, verify file paths exist
3. Scope coverage -- every key product area from research-notes examined
4. Documentation cross-validation -- doc-sourced claims tagged, spot-check 2-3 CODE-VERIFIED
5. Contradiction resolution -- no unresolved conflicting findings
6. Gap severity -- Critical gaps block synthesis, Important reduce quality, Minor are low priority
7. Depth appropriateness -- matches tier '{config.tier}'
8. User flow coverage -- key user interactions documented
9. Integration point coverage -- external dependencies documented
10. Pattern documentation -- code patterns captured for product design
11. Incremental writing compliance -- files show iterative structure

VERDICTS:
- PASS: Green light for synthesis
- FAIL: ALL findings must be resolved. Only PASS or FAIL -- no conditional pass.

Zero tolerance -- if you can't verify it, it fails.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 12. build_synthesis_prompt

Step 13a (dynamic): Per-synth-file synthesis prompt.

```python
def build_synthesis_prompt(
    research_files: list[Path],
    template_sections: list[str],
    output_path: Path,
    template_path: Path,
) -> str:
    files_list = chr(10).join(f"- {f}" for f in research_files)
    sections_list = chr(10).join(f"- {s}" for s in template_sections)

    return f"""Read the research files and synthesize them into PRD template sections.

Research files to read:
{files_list}

Template sections to produce:
{sections_list}

Output path: {output_path}
Template reference: {template_path}

Rules:
0. Read the template first. Understand each section's expected content, format, and depth.
1. Follow the template structure exactly -- same headers, tables, section format
2. Every fact must come from the research files -- do not invent or assume
3. Use tables over prose for multi-item data (feature lists, comparisons, KPI tables)
4. Do not reproduce full source code -- summarize with key capabilities
5. User stories: "As a [persona], I want [goal] so that [benefit]"
6. Acceptance criteria must be specific and testable
7. Reference actual file paths and feature names, not hypothetical ones
8. Use RICE scoring or MoSCoW prioritization where the template requires it
9. Include competitive analysis with feature comparison matrices where applicable
10. Only [CODE-VERIFIED] claims may be presented as current product capability
11. Never describe product capabilities from docs alone

CRITICAL -- Incremental File Writing:
Write to your output file incrementally as you synthesize each section.
Do NOT read all research files and attempt a single large write.
1. Create the output file with header and first section
2. After each subsequent section, append immediately using Edit
3. Never rewrite the entire file from memory

Write sections in the exact format they should appear in the final PRD.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 13. build_analyst_synthesis_prompt

Step 13b (analyst agent): Synthesis quality review.

```python
def build_analyst_synthesis_prompt(config: PrdConfig) -> str:
    return f"""Review synthesis files for quality and completeness.

Analysis type: synthesis-review
Synthesis directory: {config.synthesis_dir}
Research directory: {config.research_dir}
Output path: {config.qa_dir / 'analyst-synthesis-review.md'}

PROCESS:
1. Read ALL synth files in {config.synthesis_dir}
2. Cross-reference claims against research files in {config.research_dir}
3. Check template section alignment
4. Report findings

CHECKLIST:
1. Each synth file covers its mapped template sections (per synthesis-mapping.md)
2. Table structures match template expectations
3. No fabricated claims -- sample 5 per file, trace to research
4. Evidence citations use actual file paths
5. User stories follow format with acceptance criteria
6. Cross-section consistency (personas in S7 match user stories in S21.1)
7. No doc-only claims in capability sections
8. Content rules compliance (tables over prose, no code reproductions)

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found with specific fixes listed

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 14. build_qa_synthesis_gate_prompt

Step 13b (QA agent): Synthesis gate verification.

```python
def build_qa_synthesis_gate_prompt(config: PrdConfig) -> str:
    return f"""Perform QA verification of synthesis files for the PRD.

QA phase: synthesis-gate
Synthesis directory: {config.synthesis_dir}
Research directory: {config.research_dir}
Fix authorization: true
Output path: {config.qa_dir / 'qa-synthesis-gate-report.md'}

You are verifying that synthesis files are ready for assembly.
You CAN fix issues in-place using Edit.

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in {config.synthesis_dir}
2. Read EVERY synth file completely
3. Apply the 12-item checklist
4. For each issue: document it, fix in-place with Edit, verify the fix
5. Write your QA report

12-ITEM CHECKLIST:
1. Section headers match PRD template structure
2. Table column structures correct
3. No fabrication (sample 5 claims per file, trace to research)
4. Evidence citations use actual file paths
5. User stories follow As a / I want / So that format
6. Requirements use RICE or MoSCoW prioritization
7. Cross-section consistency
8. No doc-only claims in feature inventories
9. Stale docs surfaced in Open Questions or Assumptions
10. Content rules compliance
11. All expected sections have content (no placeholders)
12. No hallucinated file paths

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with fixes, note which were fixed in-place)

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 15. build_assembly_prompt

Step 14a: Assemble final PRD from synthesis files.

```python
def build_assembly_prompt(config: PrdConfig) -> str:
    synth_files = discover_synth_files(config.task_dir)
    files_list = chr(10).join(f"- {f}" for f in synth_files)

    return f"""Assemble the final Product Requirements Document from synthesis files.

Component files (in order):
{files_list}

Output path: {config.output_path}
Research directory: {config.research_dir}
Template reference: {config.template_path}

CRITICAL -- Incremental File Writing Protocol:
1. FIRST ACTION: Create the output file with PRD frontmatter
   Set status: "Draft", populate created_date, tags, etc.
2. As you assemble each section, IMMEDIATELY write it using Edit
3. Never rewrite from scratch

Assembly procedure:
1. Write frontmatter and HOW TO USE blockquote
2. Write Document Information table (9 rows)
3. Assemble sections in template order from synth files
4. Write Table of Contents from actual section headers
5. Add Appendices (Glossary, Acronyms, etc.)
6. Add Document History (initial entry)
7. Add Document Provenance

Assembly rules:
1. Write header first, then sections in order, then ToC
2. Write each section to disk immediately
3. Cross-check internal consistency:
   - Personas in S7 appear in user stories in S21.1
   - Requirements in S21.2 have acceptance criteria
   - Competitive features in S9 map to requirements in S21.2
   - Open Questions in S13 aren't answered elsewhere
   - Success Metrics in S19 have measurement methods
   - Risk mitigations in S20 address identified risks
4. Flag contradictions: [CONTRADICTION: Section X claims A, Section Y claims B]
5. No placeholder text remains
6. Tables over prose for multi-item data
7. No full source code reproductions

Content rules (non-negotiable):
- Tables over prose whenever presenting multi-item data
- Product vision: concise statement + 1-2 paragraph expansion
- User personas: structured attribute tables
- User stories: As a / I want / So that + acceptance criteria
- Competitive analysis: feature comparison matrices with status icons
- Requirements: prioritized tables with RICE/MoSCoW
- KPIs: Category / KPI / Target / Measurement Method table
- Risk analysis: probability/impact matrices with mitigations

You are assembling existing content, not creating new findings.
Preserve fidelity to synthesis files. Minimal transitional text only.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 16. build_structural_qa_prompt

Step 14b: Structural QA of assembled PRD.

```python
def build_structural_qa_prompt(config: PrdConfig) -> str:
    return f"""Perform final QA validation of the assembled PRD.

QA phase: report-validation
Report path: {config.output_path}
Research directory: {config.research_dir}
Template path: {config.template_path}
Output path: {config.qa_dir / 'qa-report-validation.md'}
Fix authorization: true

This is the final structural check. You can and should fix issues in-place.

18-ITEM VALIDATION CHECKLIST:
1. All template sections present (or marked N/A with rationale)
2. Frontmatter has all required fields
3. Line count within tier budget (Lightweight: 400-800, Standard: 800-1500, Heavyweight: 1500-2500)
4. HOW TO USE blockquote present
5. Document Information table has all 9 rows
6. Numbered Table of Contents present
7. User stories follow format
8. Acceptance criteria are specific and testable
9. Feature prioritization uses RICE or MoSCoW
10. Competitive analysis includes feature comparison matrix
11. KPI tables have measurement methods
12. No full source code reproductions
13. All file paths reference actual files
14. Document History table present
15. Tables use correct column structure from template
16. No doc-sourced claims presented as verified without tags
17. Product capability claims cite actual file paths
18. Web research findings include source URLs

CONTENT QUALITY CHECKS:
19. Table of Contents accuracy
20. Internal consistency (no contradictions)
21. Readability (scannable -- tables, headers, bullets)
22. Actionability (team could begin planning from this PRD alone)

Fix every issue you find. Report honestly.

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 17. build_qualitative_qa_prompt

Step 14c: Qualitative review of assembled PRD.

```python
def build_qualitative_qa_prompt(config: PrdConfig) -> str:
    return f"""Perform qualitative review of the assembled PRD.

QA phase: qualitative-review
Report path: {config.output_path}
Output path: {config.qa_dir / 'qa-qualitative-review.md'}
Fix authorization: true

You are reviewing whether the PRD makes sense as a product document.
This is NOT structural validation -- that was done in the prior step.

QUALITATIVE CHECKLIST:
1. Does the executive summary accurately capture the product's value proposition?
2. Are the user personas realistic and based on observed product behavior?
3. Do the user stories represent actual user needs (not developer conveniences)?
4. Is the competitive analysis fair and evidence-based?
5. Are success metrics measurable and aligned with business objectives?
6. Is the implementation plan realistic given the technical requirements?
7. Are risks properly assessed with actionable mitigations?
8. Does the scope definition clearly separate in-scope from out-of-scope?
9. Are dependencies identified with owners and resolution plans?
10. Is the document coherent end-to-end (no contradictions between sections)?

SCOPE CHECKS:
- Feature-scope PRD doesn't accidentally describe the entire platform
- Product-scope PRD doesn't accidentally narrow to a single feature
- Technical requirements match the scope (not over/under-specified)

For each issue found:
1. Describe the problem
2. Assess severity (critical / major / minor)
3. Fix in-place if possible
4. Document what you fixed and what remains

VERDICT: PASS or FAIL

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 18. build_completion_prompt

Step 15: Generate completion summary.

```python
def build_completion_prompt(config: PrdConfig) -> str:
    return f"""Generate a completion summary for the PRD pipeline.

Final PRD: {config.output_path}
Task directory: {config.task_dir}
Tier: {config.tier}

Produce a brief markdown summary:

# PRD Pipeline Complete

## Output
- **PRD path**: [path]
- **Line count**: [count]
- **Sections**: [count]

## Pipeline Statistics
- Research agents: [count]
- Web research agents: [count]
- Synthesis agents: [count]
- QA fix cycles: [count]

## Quality
- Structural QA: [PASS/FAIL]
- Qualitative QA: [PASS/FAIL]

## Next Steps
- Review the PRD at [path]
- Share with stakeholders
- Create implementation tasks from Section 21

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## 19. build_gap_filling_prompt

Fix cycle: Spawn targeted agents to address specific QA failures.

```python
def build_gap_filling_prompt(
    failure: dict,
    config: PrdConfig,
    cycle: int,
    phase: str,  # "research" or "synthesis"
) -> str:
    return f"""Address this specific QA failure from fix cycle {cycle}.

Phase: {phase}
Failure:
  Area: {failure['area']}
  Issue: {failure['issue']}
  Severity: {failure['severity']}
  Remediation: {failure.get('remediation', 'Not specified')}

Task directory: {config.task_dir}
Research directory: {config.research_dir}

Your ONLY job is to fix this specific gap. Do not re-do work that already passed QA.

If phase is 'research':
- Read the relevant research file(s)
- Investigate the specific gap area in the codebase
- Append missing findings to the appropriate research file
- Update the file's summary and gaps sections

If phase is 'synthesis':
- Read the relevant synth file(s)
- Cross-reference against research files
- Fix the specific issue in the synth file using Edit
- Verify the fix addresses the QA finding

Write a brief report of what you fixed to:
{config.qa_dir / f'gap-fix-{cycle:02d}-{failure["area"][:20]}.md'}

EXIT_RECOMMENDATION: CONTINUE
"""
```

---

## Helper Functions

```python
import json
from datetime import date
from pathlib import Path

def _load_json(path: Path) -> dict:
    """Load and parse a JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))

def _read_file(path: Path) -> str:
    """Read a file, truncating if >50KB for prompt embedding."""
    content = path.read_text(encoding="utf-8")
    if len(content) > 50_000:
        return content[:50_000] + "\n\n[TRUNCATED -- file exceeds 50KB inline limit]"
    return content

def _today() -> str:
    """Return today's date in ISO format."""
    return date.today().isoformat()
```
