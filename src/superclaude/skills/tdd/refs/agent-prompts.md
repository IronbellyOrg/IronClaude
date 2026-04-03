## Agent Prompt Templates

These templates are provided to the task builder (in the BUILD_REQUEST) so it can embed them in the task file's self-contained checklist items. The builder should customize each instance with the specific investigation topic, files, and output path.

### Codebase Research Agent Prompt

```
Research this aspect of [component name] and write findings to [output-path]:

Topic: [topic description]
Investigation type: [Architecture Analyst / Code Tracer / Data Model Analyst / API Surface Mapper / Integration Mapper / Doc Analyst]
Files to investigate: [list of files/directories]
Component root: [primary directory]
PRD context: [path to PRD extraction file, if applicable — cross-reference requirements as you research]

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
1. Read the actual source files — understand what each file does, what it exports, what it imports
2. Trace data flow — how does data enter, transform, and exit this part of the system?
3. Document the implementation — key classes, functions, methods with file paths and line numbers
4. Identify architecture patterns suitable for the design — what patterns can inform the TDD?
5. Document data model shapes and relationships — entity types, field definitions, constraints
6. Map API surface and integration contracts — endpoints, request/response schemas, service boundaries
7. Check for edge cases — error handling, fallbacks, configuration-driven behavior
8. Note dependencies — what does this subsystem depend on? What depends on it?
9. Flag gaps — what is missing, broken, undocumented, or unclear? What needs further investigation?
10. Note integration opportunities — where could new functionality hook in? Where are the natural extension points?

CRITICAL — Documentation Staleness Protocol:
Documentation describes intent or historical state. Code describes CURRENT state. These frequently diverge.
When you encounter documentation that describes an architecture, pipeline, service, component, endpoint,
or workflow, you MUST cross-validate EVERY structural claim against actual code before reporting it as current:

1. **Services/components described in docs:** Verify the service directory, entry point file, and key classes actually exist in the repo. Use Glob to check. If a doc says "Service X at path/Y/", verify the path exists. If it doesn't, the doc is STALE — report as historical, not current.

2. **Pipelines/call chains described in docs:** Trace at least the first and last hop in actual source code. If any hop is missing, the pipeline is STALE.

3. **File paths mentioned in docs:** Spot-check that referenced files exist.

4. **API endpoints described in docs:** Verify the endpoint exists in the actual router/app code.

For EVERY doc-sourced architectural claim, mark it with one of:
- **[CODE-VERIFIED]** — confirmed by reading actual source code at [file:line]
- **[CODE-CONTRADICTED]** — code shows different implementation (describe what code actually shows)
- **[UNVERIFIED]** — could not find corresponding code; may be stale, planned, or in a different repo

Claims marked [UNVERIFIED] or [CODE-CONTRADICTED] MUST appear in the Gaps and Questions section.
Do NOT present doc-sourced claims as verified facts without the code verification tag.

Output Format:
- Use descriptive headers for each file or logical group investigated
- Include actual class names, function signatures, data model shapes, and API endpoints (not reproduced code blocks — summaries with key signatures)
- Note any anomalies, tech debt, or surprising behavior
- Flag stale documentation explicitly with **[STALE DOC]** markers
- End each section with a "Key Takeaways" bullet list
- End the file with:
  ## Gaps and Questions
  - [things that need further investigation or are unclear]
  - [all UNVERIFIED and CODE-CONTRADICTED claims from docs]

  ## Stale Documentation Found
  - [list any docs that describe architecture/components that no longer exist in code]

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
Component context: [the overall component being designed]

CRITICAL — Incremental File Writing Protocol:
1. FIRST ACTION: Create your output file with a header including topic, date, and status
2. As you find relevant information, IMMEDIATELY append to the file
3. Never accumulate and one-shot

Research Protocol:
1. Search for official documentation, guides, and API references for relevant technologies
2. Search for architectural patterns and design best practices
3. Search for performance benchmarks and optimization strategies
4. Search for security patterns and threat models for this type of system
5. Search for API design standards and industry conventions
6. Search for SLO/SLI industry benchmarks for similar systems
7. Search for implementation examples and reference architectures
8. For each finding, document:
   - Source URL
   - Key information extracted
   - How it relates to our codebase findings
   - Whether it supports, extends, or contradicts what we found in code
9. Rate source reliability (official docs > well-maintained repos > blog posts > forum answers)

Output Format:
- Use descriptive headers for each research area
- Always include source URLs
- Mark relevance: HIGH / MEDIUM / LOW for each finding
- End with:
  ## Key External Findings
  [Bullet list of the most important discoveries]

  ## Recommendations from External Research
  [How external findings should influence the technical design]

IMPORTANT: Our codebase is the source of truth. External research adds technology context and best practices but does not override verified code behavior. If you find a discrepancy, note it explicitly.
```

**Common web research topics for TDDs:**
- Design pattern references relevant to the component architecture (e.g., repository pattern, saga pattern, circuit breaker)
- Scalability benchmarks for the technology stack and expected load profile
- Security best practices for the component type (e.g., auth patterns, input validation, encryption standards)
- API design standards and industry conventions (e.g., REST best practices, GraphQL schema design, gRPC patterns)
- Infrastructure patterns for the component type (e.g., caching strategies, message queue patterns, database scaling)

### Synthesis Agent Prompt

```
Read the research files listed below and synthesize them into template-aligned sections for a Technical Design Document (TDD).

Research files to read: [list of paths]
Template sections to produce: [section numbers and names]
Output path: [synth file path]
Template reference: src/superclaude/examples/tdd_template.md

Rules:
0. **Read the template first.** Before synthesizing anything, read the TDD template to understand each section's expected content, format, and depth.
1. Follow the template structure exactly — use the same headers, tables, and section format
2. Every fact must come from the research files — do not invent or assume
3. Use tables over prose for multi-item data (requirements, dependencies, metrics, risks)
4. Do not reproduce full interfaces, function bodies, or configuration files — summarize with key signatures and data shapes
5. Architecture sections must include ASCII or Mermaid diagrams where the research supports them
6. Requirements must use ID numbering (FR-001, NFR-001) with priority and acceptance criteria
7. Reference actual file paths, not hypothetical ones
8. Alternatives Considered must include Alternative 0: Do Nothing (mandatory per template)
9. SLOs must include SLI measurements and error budget policies where applicable
10. Documentation-sourced claims require verification status. If a research file reports a finding from documentation, check whether it carries a [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED] tag. Only [CODE-VERIFIED] claims may be presented as current architecture. [CODE-CONTRADICTED] claims must be corrected. [UNVERIFIED] claims must be flagged as uncertain and placed in Open Questions (Section 22) — never in Architecture, Data Models, or API Specifications sections as if they are fact.
11. Never describe architecture from docs alone. When writing Architecture (Section 6), Data Models (Section 7), or API Specifications (Section 8), ONLY use findings that trace back to actual source code reads. If the only evidence is a documentation file, flag as [UNVERIFIED — doc-only] and exclude from architecture diagrams.
12. Every FR in TDD Section 5.1 must trace back to a PRD epic or user story. Cite the epic ID in the FR row's "Source" column. If no PRD epic can be identified for an FR, mark it "[NO PRD TRACE]" and flag it as a gap.
13. TDD Section 4.2 (Business Metrics, if included) must include at least one engineering proxy metric for each business KPI listed in the PRD's Section 4 and Section 19. Format as: Business KPI: [PRD KPI name] — Engineering Proxy: [measurable technical metric].

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
Perform a completeness verification of all research files for [component].

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
4. Apply the 8-item Research Completeness Verification checklist
5. Write your report to [output-path]

CHECKLIST:
1. Coverage audit — every key file/subsystem from scope covered by at least one research file
2. Evidence quality — claims cite specific file paths, line numbers, function names
3. Documentation staleness — all doc-sourced claims tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED]
4. Completeness — every file has Status: Complete, Summary section, Gaps section, Key Takeaways
5. Cross-reference check — cross-cutting concerns covered by multiple agents are cross-referenced
6. Contradiction detection — conflicting findings about the same component surfaced
7. Gap compilation — all gaps unified, deduplicated, and severity-rated (Critical/Important/Minor)
8. Depth assessment — investigation depth matches the stated tier (data models documented, API surfaces mapped, architecture patterns identified)

VERDICTS:
- PASS: All checks pass, no critical gaps
- FAIL: Critical gaps exist (list each with specific remediation action)

Use the full output format from your agent definition (tables for coverage, evidence quality, staleness, completeness).
Be adversarial — your job is to find problems, not confirm things work.
```

### Research QA Agent Prompt (rf-qa — Research Gate)

```
Perform QA verification of research completeness for [component].

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
5. Apply the 10-item Research Gate checklist

IF NO ANALYST REPORT:
Apply the full 10-item Research Gate checklist independently.

10-ITEM CHECKLIST:
1. File inventory — all research files exist with Status: Complete and Summary
2. Evidence density — sample 3-5 claims per file, verify file paths exist
3. Scope coverage — every key file from research-notes EXISTING_FILES examined
4. Documentation cross-validation — all doc-sourced claims tagged, spot-check 2-3 CODE-VERIFIED
5. Contradiction resolution — no unresolved conflicting findings
6. Gap severity — Critical gaps block synthesis, Important reduce quality, Minor are lower priority but must still be fixed
7. Depth appropriateness — matches the tier expectation
8. Integration point coverage — connection points documented
9. Pattern documentation — code patterns and conventions captured
10. Incremental writing compliance — files show iterative structure, not one-shot

VERDICTS:
- PASS: Green light for synthesis
- FAIL: ALL findings must be resolved. Only PASS or FAIL — no conditional pass.

Use the full QA report output format from your agent definition.
Zero tolerance — if you can't verify it, it fails.
```

### Synthesis QA Agent Prompt (rf-qa — Synthesis Gate)

```
Perform QA verification of synthesis files for [component].

QA phase: synthesis-gate
Research directory: [research-dir-path]
Fix authorization: [true/false]
Output path: [output-path]

You are verifying that synthesis files are ready for assembly into the final TDD.
If fix_authorization is true, you can fix issues in-place using Edit.

PROCESS:
1. Use Glob to find ALL synth files (synth-*.md) in the synthesis directory
2. Read EVERY synth file completely
3. Apply the 12-item Synthesis Gate checklist
4. For each issue found:
   a. Document the issue (what, where, severity)
   b. If fix_authorization is true: fix in-place with Edit, verify the fix
   c. If fix_authorization is false: document the required fix
5. Write your QA report to [output-path]

12-ITEM CHECKLIST:
1. Section headers match TDD template (src/superclaude/examples/tdd_template.md)
2. Table column structures correct (FR/NFR numbering, assessment tables, SLO/SLI tables)
3. No fabrication (sample 5 claims per file, trace to research files)
4. Evidence citations use actual file paths
5. Architecture sections include diagrams (ASCII or Mermaid)
6. Requirements use FR-001/NFR-001 ID numbering with priority and acceptance criteria
7. Cross-section consistency (requirements trace to architecture, risks to mitigations)
8. No doc-only claims in Architecture (Section 6), Data Models (Section 7), or API Specs (Section 8)
9. Stale docs surfaced in Open Questions (Section 22)
10. Content rules compliance (tables over prose, no code reproductions)
11. All expected sections have content (no placeholders)
12. No hallucinated file paths (verify parent directories exist)

VERDICTS:
- PASS: All synth files meet quality standards
- FAIL: Issues found (list with specific fixes, note which were fixed in-place)
```

### Report Validation QA Agent Prompt (rf-qa — Report Validation)

```
Perform final QA validation of the assembled TDD for [component].

QA phase: report-validation
Report path: [report-path]
Research directory: [research-dir-path]
Template path: src/superclaude/examples/tdd_template.md
Output path: [output-path]
Fix authorization: true (always authorized for report validation)

This is the final quality check before presenting to the user. You can and should fix issues in-place.

PROCESS:
1. Read the ENTIRE TDD document
2. Apply the 15-item Validation Checklist + 4 Content Quality Checks
3. For each issue: document it, fix it in-place with Edit, verify the fix
4. Write your QA report to [output-path]

15-ITEM VALIDATION CHECKLIST:
1. All template sections present (or explicitly marked as N/A with rationale per tier)
2. Frontmatter has all required fields from the template
3. Total line count within tier budget (Lightweight: 300-600, Standard: 800-1400, Heavyweight: 1400-2200)
4. Document purpose block with tiered usage table present
5. Document Information table has all 7 rows plus Approvers table
6. Numbered Table of Contents present
7. Requirements use FR/NFR ID numbering with priority
8. Architecture section includes at least one diagram (ASCII or Mermaid)
9. Alternative 0: Do Nothing is present in Alternatives Considered
10. SLO/SLI tables present for Standard and Heavyweight tiers
11. No full source code reproductions (interfaces, function bodies, config files)
12. All file paths reference actual files that exist
13. Document History table present
14. Tables use correct column structure from template
15. No doc-sourced architectural claims presented as verified without code cross-validation tags

CONTENT QUALITY CHECKS:
16. Table of Contents accuracy (matches actual section headers)
17. Internal consistency (no contradictions between sections)
18. Readability (scannable — tables, headers, bullets)
19. Web research findings include source URLs for every external claim
20. Actionability (engineer could begin implementation from the Architecture, Data Models, and API Specifications alone)

Fix every issue you find. Report honestly.
```

### Assembly Agent Prompt (rf-assembler — TDD Assembly)

```
Assemble the final Technical Design Document for [component] from synthesis files.

Component files (in order):
[ordered list of synth file paths]

Output path: [tdd-output-path]
Research directory: [research-dir-path]
Template reference: src/superclaude/examples/tdd_template.md

CRITICAL — Incremental File Writing Protocol:
You MUST follow this protocol exactly. Violation results in data loss.

1. FIRST ACTION: Create the output file immediately with the TDD frontmatter and header:
   - Fill in all template frontmatter fields. Set status: "🟡 Draft", populate created_date, parent_doc (link to PRD if applicable), depends_on, tags
   - Write the document purpose block with tiered usage table
   - Write the Document Information table

2. As you assemble each section, IMMEDIATELY write it to the output file using Edit.
   Do NOT accumulate the entire TDD in context and attempt a single write.

3. After each Edit, the file grows. This is correct behavior. Never rewrite from scratch.

Assembly rules:
1. Start with template frontmatter, then document header, then Document Information table
2. Assemble sections in template order — read each synth file and write its content into the correct position
3. Write each section to disk immediately after composing it — do NOT one-shot
4. Sections not assigned a synth file (27. References, 28. Glossary) get written directly during assembly
5. Generate the Table of Contents from actual section headers after all sections are placed
6. Add Appendices — Detailed API Specifications, Database Schema, Wireframes, Performance Test Results as applicable
7. Add Document History — initial entry
8. Add Document Provenance — if created from PRD or by consolidating existing docs, document source materials and creation method
9. Cross-check internal consistency:
   - Requirements in Section 5 trace to architecture in Section 6
   - Risks in Section 20 have mitigations
   - Open Questions in Section 22 aren't answered elsewhere
   - Dependencies in Section 18 are complete
10. Flag any contradictions between sections
11. Ensure no placeholder text remains (search for [, TODO, TBD, PLACEHOLDER)

Content rules (non-negotiable):
- Architecture: ASCII or Mermaid diagrams with component tables, not multi-paragraph prose
- Data models: Entity tables with Field / Type / Required / Description / Constraints
- API specs: Endpoint overview tables plus key endpoint details with request/response examples
- Requirements: FR/NFR split with ID numbering (FR-001, NFR-001)
- Testing: Test pyramid tables by level with coverage targets and tools
- Performance: Budget tables with specific metrics and measurement methods
- Security: Threat model tables plus security controls with verification methods
- Alternatives: Structured Pros/Cons with mandatory "Why Not Chosen" and Do Nothing option
- Dependencies: Tables with Version / Purpose / Risk Level / Fallback
- SLOs: SLO / SLI / Error Budget tables with burn-rate alerts
- Evidence cited inline: file.cpp:123, ClassName::method()

CRITICAL: You are assembling existing content from synthesis files, not creating new findings.
Preserve fidelity to the synthesis files. Add only minimal transitional text for coherence.
Do NOT attempt full content validation — that is the QA agent's job. Focus on assembly
integrity: correct ordering, internal consistency, no placeholders, all components included.

Consolidation protocol (when consolidating existing docs into this TDD):
1. Read each source document listed in the task's "Source Files to Consolidate" section
2. Map each source document's content to the corresponding template section(s)
3. Where source docs overlap, merge by keeping the most specific/recent information and noting conflicts
4. Add an Appendix: Document Provenance subsection listing each source doc with its path, original purpose, and which sections it contributed to
5. Zero content loss — every metadata piece and unique finding from source docs must appear in the final output or be explicitly noted as superseded
6. After assembly, the source docs should be candidates for archival (the TDD replaces them)
```
