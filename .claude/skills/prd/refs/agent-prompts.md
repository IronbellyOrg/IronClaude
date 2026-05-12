# Agent Prompt Templates

> **Purpose:** Agent prompt templates for the PRD pipeline, loaded during Stage A.7 by the builder subagent.
> Extracted from SKILL.md lines 553-967 with zero content changes.

---


## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder should customize each instance with the specific product area, files, and output path.

### Codebase Research Agent Prompt

```
Research this aspect of [product name] and write findings to [output-path]:

Topic: [topic description]
Investigation type: [Feature Analyst / Doc Analyst / Integration Mapper / UX Investigator / Architecture Analyst]
Files to investigate: [list of files/directories]
Product root: [primary directory]

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create your output file immediately with this header:
   ```markdown
   # Research: [Your Topic]

   **Investigation type:** [type]
   **Scope:** [files/directories assigned]
   **Status:** In Progress
   **Date:** [today]

   ---
   ```

2. As you investigate each file, component, or logical unit, IMMEDIATELY append your findings to the output file using Edit. Do NOT accumulate findings in your context window.

3. After each append, your output file grows. This is correct behavior. Never rewrite the file from scratch.

4. When finished, update the Status line from "In Progress" to "Complete" and append a summary section.

Research Protocol:
1. Read the actual source files — understand what each file does, what capabilities it provides, what user value it delivers
2. Trace user flows — how does the user interact with this part of the product? What is the experience?
3. Document the product interface — what features, settings, capabilities, and user touchpoints exist?
4. Identify patterns — what product conventions, design decisions, or UX patterns are evident?
5. Check for edge cases — error states, missing features, configuration-driven behavior, accessibility gaps
6. Note dependencies — what does this product area depend on? What depends on it?
7. Flag gaps — what is missing, broken, undocumented, or unclear? What needs further investigation?
8. Note integration opportunities — where could new features or product capabilities hook in? What extension points exist? What APIs, events, or plugin systems could be leveraged?

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state. These frequently diverge.
When you encounter documentation that describes a product capability, feature, service, or workflow, you MUST cross-validate structural claims against actual code before reporting them as current:

1. **Features/capabilities described in docs:** Verify the feature's implementation files actually exist in the repo. Use Glob to check. If a doc says "real-time collaboration at frontend/app/collab/", verify the path exists. If it doesn't, the doc is STALE — report as historical, not current.

2. **User flows described in docs:** Trace at least the entry and exit points in actual source code. If a doc describes a user flow but the referenced components don't exist, the flow is STALE.

3. **File paths mentioned in docs:** Spot-check that referenced files exist.

4. **API endpoints described in docs:** Verify route definitions exist in the actual codebase. If a doc describes an endpoint at `/api/v1/sessions` but the route handler doesn't exist, the endpoint is STALE.

For EVERY doc-sourced claim, mark it with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code actually shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale, planned, or in a different repo

Claims marked [UNVERIFIED] or [CODE-CONTRADICTED] MUST appear in the Gaps and Questions section.

Output Format:
- Use descriptive headers for each file or logical group
- Include actual feature capabilities, user flows, configuration options, and technology choices (not reproduced code blocks — summaries with key capabilities)
- Note any anomalies, tech debt, or surprising behavior
- End each section with a "Key Takeaways" bullet list
- End the file with:
  ## Gaps and Questions
  - [things that need further investigation or are unclear]
  - [all UNVERIFIED and CODE-CONTRADICTED claims from docs]

  ## Stale Documentation Found
  - [list any docs that describe features/capabilities that no longer exist in code]

  ## Summary
  [3-5 sentence summary of what you found]

Be thorough. Be specific. Only document what you verified in the source. Do not guess or infer.
Documentation is NOT verification — reading a doc that says "X exists" does not verify X exists.
Only reading the actual source code of X verifies X exists.
```

### Web Research Agent Prompt

```
Research this topic externally and write findings to [output-path].

Topic: [specific external research topic]
What we already know from codebase: [brief summary of relevant codebase findings]
Product context: [the overall product being documented]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for market data, industry reports, and competitive landscape information
2. Search for comparable products and their feature sets
3. Search for industry best practices and standards relevant to this product area
4. Search for technology trends affecting this product category
5. For each finding, document:
   - Source URL
   - Key information extracted
   - How it relates to our product's current capabilities
   - Whether it supports, extends, or contradicts what we found in code
6. Rate source reliability (official reports > industry publications > well-maintained repos > blog posts > forum answers)

Output Format:
- Use descriptive headers for each research area
- Always include source URLs
- Mark relevance: HIGH / MEDIUM / LOW for each finding
- End with:
  ## Key External Findings
  [Bullet list of the most important discoveries]

  ## Recommendations from External Research
  [How external findings should influence the PRD — market positioning, feature gaps, competitive threats]

IMPORTANT: Our codebase is the source of truth for current capabilities. External research adds market context and competitive intelligence but does not override verified product behavior. If you find a discrepancy, note it explicitly.
```

Common web research topics for PRDs:
- Competitive landscape and feature comparison matrices
- Market sizing (TAM/SAM/SOM) data and industry reports
- Industry standards and compliance requirements
- Technology trends and emerging capabilities
- User research findings and market validation
- Pricing models and monetization patterns in the space

### Synthesis Agent Prompt

```
Read the research files listed below and synthesize them into template-aligned sections for a Product Requirements Document (PRD).

Research files to read: [list of paths]
Template sections to produce: [section numbers and names]
Output path: [synth file path]
Template reference: src/superclaude/examples/prd_template.md

Rules:
0. **Read the template first.** Before synthesizing anything, read the PRD template to understand each section's expected content, format, and depth.
1. Follow the template structure exactly — use the same headers, tables, and section format
2. Every fact must come from the research files — do not invent or assume
3. Use tables over prose for multi-item data (feature lists, competitive comparisons, KPI tables, requirements)
4. Do not reproduce full source code or configuration files — summarize with key capabilities and technology choices
5. User stories must follow the standard format: "As a [persona], I want [goal] so that [benefit]"
6. Acceptance criteria must be specific and testable
7. Reference actual file paths and feature names, not hypothetical ones
8. Use RICE scoring or MoSCoW prioritization where the template requires it
9. Include competitive analysis with feature comparison matrices where applicable
10. Documentation-sourced claims require verification status. If a research file reports a finding from documentation, check whether it carries a [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED] tag. Only [CODE-VERIFIED] claims may be presented as current product capability. [CODE-CONTRADICTED] claims must be corrected. [UNVERIFIED] claims must be flagged as uncertain.
11. Never describe product capabilities from docs alone. When writing sections about current product state, ONLY use findings that trace back to actual source code reads. If the only evidence is a documentation file, flag as [UNVERIFIED — doc-only] and exclude from feature inventories.

CRITICAL — Incremental File Writing:
You MUST write to your output file incrementally as you synthesize each section. Do NOT read all research files into context and attempt a single large write at the end. The process is:
1. Create the output file with a header and your first synthesized section
2. After completing each subsequent section, append it to the output file immediately using Edit
3. Never rewrite the entire file from memory — always append or do targeted edits

This prevents data loss from context limits and ensures partial results survive if the agent is interrupted.

Write the sections in the exact format they should appear in the final document, including all table structures and headers from the template.
```

### Research Analyst Agent Prompt (rf-analyst — Completeness Verification)

```
Perform a completeness verification of all research files for [product name] PRD.

Analysis type: completeness-verification
Research directory: [research-dir-path]
Research notes file: [research-notes-path]
Tier: [Lightweight/Standard/Heavyweight]
Output path: [output-path]

Your job is to independently verify that research agents produced thorough, evidence-based findings
before downstream synthesis begins. You are the analytical quality gate — be rigorous.

PROCESS:
1. Read the research-notes.md file to understand the planned scope (EXISTING_FILES, SUGGESTED_PHASES)
2. Use Glob to find ALL research files in the research directory (files matching [NN]-*.md)
3. Read EVERY research file — do not skip any
4. Apply the 8-item Research Completeness Verification checklist from your agent definition
5. Write your report to [output-path]

CHECKLIST:
1. Coverage audit — every key product area from scope covered by at least one research file
2. Evidence quality — claims cite specific file paths, feature names, capability descriptions
3. Documentation staleness — all doc-sourced claims tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED]
4. Completeness — every file has Status: Complete, Summary section, Gaps section, Key Takeaways
5. Cross-reference check — cross-cutting concerns covered by multiple agents are cross-referenced
6. Contradiction detection — conflicting findings about the same feature surfaced
7. Gap compilation — all gaps unified, deduplicated, and severity-rated (Critical/Important/Minor)
8. Depth assessment — investigation depth matches the stated tier (stakeholder segments identified, user journeys documented, feature scope mapped, competitive landscape analyzed)

VERDICTS:
- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action)

Use the full output format from your agent definition (tables for coverage, evidence quality, staleness, completeness).
Be adversarial — your job is to find problems, not confirm things work.
```

### Research QA Agent Prompt (rf-qa — Research Gate)

```
Perform QA verification of research completeness for [product name] PRD.

QA phase: research-gate
Research directory: [research-dir-path]
Analyst report: [analyst-report-path] (if exists, verify the analyst's work; if not, perform full verification)
Research notes file: [research-notes-path]
Tier: [Lightweight/Standard/Heavyweight]
Output path: [output-path]

You are the last line of defense before synthesis begins. Assume everything is wrong until you verify it.

IF ANALYST REPORT EXISTS:
1. Read the analyst's completeness report
2. Spot-check 3-5 of their coverage audit claims (verify the scope items are actually covered)
3. Validate gap severity classifications (are "Critical" really critical? Are "Minor" really minor?)
4. Check their verdict against your own independent assessment
5. Apply the 10-item Research Gate checklist from your agent definition

IF NO ANALYST REPORT:
Apply the full 10-item Research Gate checklist from your agent definition independently.

11-ITEM CHECKLIST:
1. File inventory — all research files exist with Status: Complete and Summary
2. Evidence density — sample 3-5 claims per file, verify file paths exist
3. Scope coverage — every key product area from research-notes EXISTING_FILES examined
4. Documentation cross-validation — all doc-sourced claims tagged, spot-check 2-3 CODE-VERIFIED
5. Contradiction resolution — no unresolved conflicting findings
6. Gap severity — Critical gaps block synthesis, Important reduce quality, Minor are lower priority but must still be fixed
7. Depth appropriateness — matches the tier expectation
8. User flow coverage — key user interactions documented with entry and exit points
9. Integration point coverage — external dependencies and connection points documented
10. Pattern documentation — code patterns and conventions captured that inform product design
11. Incremental writing compliance — files show iterative structure, not one-shot

VERDICTS:
- PASS: Green light for synthesis
- FAIL: ALL findings must be resolved. Only PASS or FAIL — no conditional pass.

Use the full QA report output format from your agent definition.
Zero tolerance — if you can't verify it, it fails.
```

### Synthesis QA Agent Prompt (rf-qa — Synthesis Gate)

```
Perform QA verification of synthesis files for [product name] PRD.

QA phase: synthesis-gate
Research directory: [research-dir-path]
Fix authorization: [true/false]
Output path: [output-path]

You are verifying that synthesis files are ready for assembly into the final PRD.
If fix_authorization is true, you can fix issues in-place using Edit.

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in the synthesis directory
2. Read EVERY synth file completely
3. Apply the 12-item Synthesis Gate checklist from your agent definition
4. For each issue found:
   a. Document the issue (what, where, severity)
   b. If fix_authorization is true: fix in-place with Edit, verify the fix
   c. If fix_authorization is false: document the required fix
5. Write your QA report to [output-path]

12-ITEM CHECKLIST:
1. Section headers match PRD template structure (src/superclaude/examples/prd_template.md)
2. Table column structures correct (competitive matrix, requirements table, KPI table, etc.)
3. No fabrication (sample 5 claims per file, trace to research files)
4. Evidence citations use actual file paths and feature names
5. User stories follow As a / I want / So that format with acceptance criteria
6. Requirements use RICE or MoSCoW prioritization framework
7. Cross-section consistency (personas in S7 referenced in user stories S21.1, etc.)
8. No doc-only claims in product capability or feature inventory sections
9. Stale docs surfaced in Open Questions (S13) or Assumptions & Constraints (S10)
10. Content rules compliance (tables over prose, no code reproductions)
11. All expected sections have content (no placeholders)
12. No hallucinated file paths (verify parent directories exist)

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with specific fixes, note which were fixed in-place)
```

### Report Validation QA Agent Prompt (rf-qa — Report Validation)

```
Perform final QA validation of the assembled PRD for [product name].

QA phase: report-validation
Report path: [report-path]
Research directory: [research-dir-path]
Template path: src/superclaude/examples/prd_template.md
Output path: [output-path]
Fix authorization: true (always authorized for report validation)

This is the final quality check before presenting to the user. You can and should fix issues in-place.

PROCESS:
1. Read the ENTIRE PRD
2. Apply the 18-item Validation Checklist + 4 Content Quality Checks
3. For each issue: document it, fix it in-place with Edit, verify the fix
4. Write your QA report to [output-path]

18-ITEM VALIDATION CHECKLIST:
1. All template sections present (or explicitly marked as N/A with rationale)
2. Frontmatter has all required fields from the template
3. Total line count within tier budget (Lightweight: 400-800, Standard: 800-1500, Heavyweight: 1500-2500)
4. HOW TO USE blockquote present
5. Document Information table has all 9 rows
6. Numbered Table of Contents present
7. User stories follow As a / I want / So that format
8. Acceptance criteria are specific and testable for each story
9. Feature prioritization uses RICE or MoSCoW framework
10. Competitive analysis includes feature comparison matrix
11. KPI tables have measurement methods defined
12. No full source code reproductions
13. All file paths reference actual files that exist
14. Document History table present
15. Tables use correct column structure from template
16. No doc-sourced claims presented as verified without code cross-validation tags
17. Product capability and feature claims cite actual file paths (not just prose assertions)
18. Web research findings include source URLs for every external claim

CONTENT QUALITY CHECKS:
19. Table of Contents accuracy
20. Internal consistency (no contradictions between sections)
21. Readability (scannable — tables, headers, bullets)
22. Actionability (product team could begin planning from this PRD alone)

Fix every issue you find. Report honestly.
```

### Assembly Agent Prompt (rf-assembler — PRD Assembly)

```
Assemble the final Product Requirements Document (PRD) for [product name] from synthesis files.

Component files (in order):
[ordered list of synth file paths]

Output path: [PRD-output-path]
Research directory: [research-dir-path]
Template reference: src/superclaude/examples/prd_template.md

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create the output file immediately with the PRD frontmatter:
   Fill in all frontmatter fields from the template. Set status: "🟡 Draft",
   populate created_date, depends_on, tags, etc.

2. As you assemble each section, IMMEDIATELY write it to the output file using Edit.
   Do NOT accumulate the entire PRD in context and attempt a single write.

3. After each Edit, the file grows. This is correct behavior. Never rewrite from scratch.

Assembly procedure:
1. Write the frontmatter and HOW TO USE blockquote
2. Write the Document Information table (Product Name, Product Owner, Engineering Lead, Design Lead, Stakeholders, Status, Target Release, Last Updated, Review Cadence)
3. Assemble sections in template order — read each synth file and write its content into the correct position. Sections not covered by synth files get written directly during assembly from patterns observed in the synth files.
4. Write the Table of Contents — generate from actual section headers after all sections are placed
5. Add Appendices — Glossary, Acronyms, Technical Architecture Diagrams, User Research Data, Financial Projections as applicable
6. Add Document History — initial entry
7. Add Document Provenance — if the PRD was created by consolidating existing docs, document the source materials and creation method. Zero content loss: every piece of metadata from source documents must appear somewhere in the normalized PRD.

Assembly rules:
1. Write the header first, then sections in template order, then ToC
2. Write each section to disk immediately after composing it — do NOT one-shot
3. Cross-check internal consistency:
   - Personas in Section 7 appear in user stories in Section 21.1
   - Requirements in Section 21.2 have acceptance criteria
   - Competitive features in Section 9 map to product requirements in Section 21.2
   - Open Questions in Section 13 aren't answered elsewhere in the document
   - Success Metrics in Section 19 have measurement methods
   - Risk mitigations in Section 20 address identified risks
4. Flag any contradictions between sections using: [CONTRADICTION: Section X claims A, Section Y claims B]
5. Ensure no placeholder text remains (search for [, TODO, TBD, PLACEHOLDER)
6. Tables over prose whenever presenting multi-item data
7. No full source code reproductions — summarize with key capabilities and technology choices

Content rules (non-negotiable):
- Tables over prose whenever presenting multi-item data
- Product vision: concise statement with 1-2 paragraph expansion
- User personas: structured attribute tables with representative quotes
- User stories: As a / I want / So that format with acceptance criteria
- Competitive analysis: feature comparison matrices with status icons
- Requirements: prioritized tables with RICE/MoSCoW
- KPIs: table with Category / KPI / Target / Measurement Method
- Risk analysis: probability/impact matrices with mitigations

CRITICAL: You are assembling existing content, not creating new findings. Preserve fidelity
to the synthesis files. Add only minimal transitional text where needed for coherence.
Do NOT attempt full content validation — that is the QA agent's job. Focus on assembly
integrity: correct ordering, internal consistency, no placeholders, all components included.

Consolidation protocol (when consolidating existing docs into this PRD):
1. Read each source document listed in the task's "Source Files to Consolidate" section
2. Map each source document's content to the corresponding template section(s)
3. Where source docs overlap, merge by keeping the most specific/recent information and noting conflicts
4. Add an Appendix: Document Provenance subsection listing each source doc with its path, original purpose, and which sections it contributed to
5. Zero content loss — every metadata piece and unique finding from source docs must appear in the final output or be explicitly noted as superseded
6. After assembly, the source docs should be candidates for archival (the PRD replaces them)
```
