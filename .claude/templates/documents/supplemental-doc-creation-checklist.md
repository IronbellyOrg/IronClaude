# Supplemental Documentation Creation Checklist

Use this checklist when creating any new supplemental documentation file in the GFxAI documentation system.

## Pre-Work (Planning)

**Identify parent/anchor document(s) this supports:**
- [ ] Read file `DOCUMENTATION_CONTENT_SPEC.md` at `Docs_product/DOCUMENTATION_CONTENT_SPEC.md` and log to task notes in ### Planning Phase Findings: Document hierarchy structure and which anchor doc(s) (01-14) this new document will supplement, then mark this item complete

**Define content sections:**
- [ ] Define 5-10 content sections based on topic scope and log to task notes in ### Planning Phase Findings: List of all content sections with brief description of what each section will cover, then mark this item complete

**Gather source materials:**
- [ ] Gather source research/materials (research documents, industry benchmarks, prior art, SME documentation) and log to task notes in ### Planning Phase Findings: List of all source materials collected with paths/URLs, then mark this item complete
- [ ] Identify primary content source document where the agent will find the information to populate the supplemental document (this will be referenced as [content-source-document] throughout this checklist) and log to task notes in ### Planning Phase Findings: Full path to [content-source-document] that contains the information for this supplemental doc, then mark this item complete

**Determine metadata:**
- [ ] Determine priority level (🔥 Highest | 🔼 High | ▶️ Medium | 🔽 Low | 🧊 Lowest) and initial status (⚪ Backlog | 🟡 To Do | 🟠 Doing | 🟢 Done | 🔵 Blocked) and log to task notes in ### Planning Phase Findings: Selected priority and status with rationale, then mark this item complete

**Identify related documents:**
- [ ] Read file `FILE_INVENTORY_STATUS.md` at `Docs_product/FILE_INVENTORY_STATUS.md` and log to task notes in ### Planning Phase Findings: List of related files identified, upstream (input) docs, and downstream (consumer) docs, then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## File Creation

**Create directory structure:**
- [ ] Determine appropriate subdirectory: Product strategy: `product/` | Technical specs: `tech/` | AI/ML details: `ai/` | Operations: `ops/` | UX/Design: `ux/` | GTM/Marketing: `gtm/` | Security: `security/` | Governance: `governance/` and Create subdirectory `[subdirectory-name]/` at `Docs_product/[subdirectory-name]/` if it does not exist and log to task notes in ### File Creation Findings: Directory creation status (created/already exists), then mark this item complete

**Create document file:**
- [ ] Use kebab-case naming: `my-document-name.md` (be descriptive but concise, avoid abbreviations unless widely understood) and Create file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` and log to task notes in ### File Creation Findings: Full file path where document was created, then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Frontmatter (TOML format with +++ delimiters)

### Required Frontmatter Fields Checklist:
- [ ] Read file `[content-source-document]` to understand the topic and extract metadata (title, description, relevant tags), then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` from the beginning through the closing `+++` delimiter (frontmatter section, approximately lines 1-33) to see the exact frontmatter format and fields required, then Add frontmatter to file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the exact format from the template with all required fields: `id` = "GFXAI-[TOPIC-NAME]", `title` = human-readable title from `[content-source-document]`, `description` = one-sentence summary from `[content-source-document]` matching FILE_INVENTORY_STATUS, `status` = initial status determined in planning, `type` = document type (📑 Reference, 📋 Specification, 🎯 Strategy, etc.), `priority` = priority level determined in planning, `created_date` = today's date YYYY-MM-DD, `updated_date` = today's date YYYY-MM-DD, `assigned_to` = owning team, `related_docs` = array of related file paths from planning phase, `tags` = array of relevant topic tags from `[content-source-document]`, and all other fields (autogen, coordinator, parent_task, depends_on, template_schema_doc, etc.) set to appropriate defaults, then mark this item complete
- [ ] Re-read file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` and log to task notes in ### File Creation Findings: Confirmed all required frontmatter fields present with correct TOML syntax (matching +++ delimiters, proper quotes, arrays with square brackets, objects with curly braces), then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Document Header
- [ ] Read file `[content-source-document]` to understand the document title and parent document, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "# [Document Title]" through the WHAT/WHY/HOW TO USE block (approximately lines 35-41) to see the exact format for document title, breadcrumb navigation, and summary, then Add document title and breadcrumb navigation to file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the exact format from the template with proper spacing and new lines, Use relative path from current file location linking to primary parent/anchor document, then mark this item complete
- [ ] Read file `[content-source-document]` to extract what the document contains, why it exists, and who should use it, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section starting with "> **WHAT:**" to see the exact format, then Add WHAT/WHY/HOW TO USE summary block to file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the exact format from template with content from `[content-source-document]`, Keep each line to 1-2 sentences maximum, focus on practical value and usage context, then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Completeness Tracking

**Create Completeness Status section with checklist items matching content sections:**
- [ ] Confirm that you will create one checklist item per major content section defined in planning phase in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md`, Add "All links verified" item, Add "Reviewed by [assigned_to]" as final item, Use consistent format: Checked: `- [x] Item name - **Complete**`, Unchecked: `- [ ] Item name - **Pending**` or `- [ ] Item name - **To Do**`, then mark this item complete
- [ ] Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "## Completeness Status" (approximately lines 43-52) to see the exact format, then Add "## Completeness Status" section to file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the exact format from the template with proper spacing and new lines, Create one checklist item per major content section defined in planning phase, then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Contract Table
- [ ] Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "**Contract Table:**" (approximately lines 54-62) to see the exact format, then Add contract table documenting document relationships to file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the exact format from the template with proper spacing and new lines, then mark this item complete
- [ ] Read file `[content-source-document]` to identify document dependencies and relationships, then Fill out each row accurately in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` for **Dependencies**: Parent docs this file references, **Upstream**: Where information flows FROM, **Downstream**: Where information flows TO, **Change Impact**: Who needs to know about updates, **Review Cadence**: Realistic review frequency, using information from `[content-source-document]`, then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Content Sections
- [ ] Read file `[content-source-document]` to understand the content that needs to be organized, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "## Section 1: [Section Title]" (approximately lines 66-96) to see the exact format and structure for content sections, then Create main content sections (5-10 sections recommended) in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the exact format from the template, Use `##` for top-level sections, Use `###` for subsections, Use `####` for detailed subsections, and log to task notes in ### Content Creation Findings: List of all sections created with their hierarchy level, then mark this item complete
- [ ] Read file `[content-source-document]` to extract the information for each section, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` sections "## Section 2" through "## Section 5" (approximately lines 98-217) to see examples of different content types and patterns, then Populate each section with relevant content in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the patterns from the template and information from `[content-source-document]`, Start with high-level overview then dive into details, Use progressive disclosure (general → specific), and log to task notes in ### Content Creation Findings: Confirmation that all sections populated with appropriate content following template patterns using information from `[content-source-document]`, then mark this item complete
- [ ] Read file `[content-source-document]` for content to format, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` to see formatting examples throughout (tables at lines 85-88, 124-127, code blocks at lines 90-96, etc.), then Use appropriate formatting in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` with **Bold** key metrics, statistics, and important terms, Use bullet lists for clarity and scannability, Use numbered lists for sequential steps or priority order, Use tables for structured data and comparisons, Use code blocks for examples, commands, or technical specs, Use blockquotes (`>`) for callouts, warnings, or important notes, and log to task notes in ### Content Creation Findings: Formatting standards applied throughout document matching template examples, then mark this item complete
- [ ] Read file `[content-source-document]` for examples, use cases, and benchmarks to include, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "## Additional Sections (Optional - Add as Needed)" (approximately lines 221-257) to see optional supporting elements, then Include supporting elements in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` for Tables for structured data, Code blocks with syntax highlighting (```language), ASCII diagrams or flowcharts where helpful, Examples and use cases, Industry benchmarks and research citations from `[content-source-document]`, and log to task notes in ### Content Creation Findings: List of all supporting elements added and their locations, then mark this item complete
- [ ] Read file `[content-source-document]` to understand data and research that needs interpretation, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` to see "**What This Means for GFxAI**" pattern (line 79), then Make data actionable in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` by Don't just present research—interpret it, Provide "What this means for GFxAI" sections, Include specific recommendations and action items, Set targets and benchmarks based on information from `[content-source-document]`, and log to task notes in ### Content Creation Findings: Confirmation that all data includes GFxAI-specific interpretation and actionable recommendations, then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Footer & Navigation
- [ ] Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section starting with "---" horizontal rule (approximately line 219 and 259) to see the exact format, then Add horizontal rule before footer to file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the exact format from the template with proper spacing and new lines, then mark this item complete
- [ ] Read file `[content-source-document]` to identify related documents that should be linked, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "> **See also:**" (approximately lines 261-265) to see the exact format, then Add "See also" section with related documents to file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the exact format from the template with proper spacing and new lines, then mark this item complete
- [ ] Read file `[content-source-document]` to understand relationships between documents, then Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "> **See also:**" to see how links are formatted with descriptions, then Link all related_docs from frontmatter in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` using the exact format from the template, Use relative paths (e.g., `../02_product_overview.md` or `tech/architecture.md`), Add 5-10 word description after each link, Explain what value the related doc provides, Order by relevance (most relevant first), then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Quality Gates
- [ ] Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "> **See also:**" to see how links should be formatted, then Validate all links in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` and log to task notes in ### Quality Gates Findings: Test every internal link (click or verify file exists), Test every external link (opens correctly), Fix any broken or incorrect paths, then mark this item complete
- [ ] Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` to see examples of bold statistics (line 77) and "Industry Context" pattern, then Ensure metrics/data properly sourced in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` and log to task notes in ### Quality Gates Findings: Bold key statistics for visibility, Include "Industry Context" or "Research" labels where applicable, Provide context for numbers (what they mean, why they matter), then mark this item complete
- [ ] Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` to see formatting standards for headers, lists, tables, and code blocks throughout, then Check consistent formatting in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` and log to task notes in ### Quality Gates Findings: Headers follow hierarchy (no skipped levels), Lists are consistently formatted (all bullets or all numbers), Tables have aligned columns, Code blocks have language specified, then mark this item complete
- [ ] Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` frontmatter section (lines 1-33) to verify TOML format, then Validate frontmatter TOML in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` and log to task notes in ### Quality Gates Findings: Check for matching +++ delimiters, Ensure proper quotes around strings, Arrays use square brackets: `["item1", "item2"]`, Objects use curly braces: `{key = "value"}`, then mark this item complete
- [ ] Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` section "## Completeness Status" to see checklist format, then Update completeness checklist in file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` by Mark each section as complete when done, Change status from initial (⚪ Backlog or 🟡 To Do) to 🟢 Done, then mark this item complete
- [ ] Read file `supplemental_doc_template.md` at `.claude/templates/documents/supplemental_doc_template.md` frontmatter to see updated_date field (line 9), then Update updated_date in frontmatter of file `[document-name].md` at `Docs_product/[subdirectory]/[document-name].md` and Set to current date when marking complete, then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## File Inventory Updates
- [ ] Read file `[content-source-document]` to extract summary and description for inventory, then Read file `FILE_INVENTORY_STATUS.md` at `Docs_product/FILE_INVENTORY_STATUS.md` to see the table format and structure, then Add entry to file `FILE_INVENTORY_STATUS.md` at `Docs_product/FILE_INVENTORY_STATUS.md` using the exact format from existing entries, Add row in appropriate layer table, Include: subdirectory, filename, summary from `[content-source-document]`, supports, priority, status, Update summary statistics at top of file, then mark this item complete
- [ ] Read file `[content-source-document]` to understand what the document supports and contains, then Read file `DOCUMENTATION_CONTENT_SPEC.md` at `Docs_product/DOCUMENTATION_CONTENT_SPEC.md` to see the structure overview list format and detailed section format, then Add to file `DOCUMENTATION_CONTENT_SPEC.md` at `Docs_product/DOCUMENTATION_CONTENT_SPEC.md` using the exact format from existing entries, Add to structure overview list in appropriate layer, Add detailed section with Supports/Breadcrumb/Contains information from `[content-source-document]`, then mark this item complete

**REMINDER:** YOU MUST complete the work associated with each checkbox, and mark each checkbox with [x] as you complete it before proceeding to the next item. Work MUST be completed in EXACT sequential order. DO NOT skip ahead.

## Review
- [ ] Read and review `user-activation.md` to see all style, patterns, quality standards, and depth and coverage of document specific content. Then review `[document-name].md` to determine if this new file has the same style, patterns, quality standards, and depth and coverage of document specific content. If `[document-name].md` meets the standard set by `user-activation.md`, then mark this as complete. If If `[document-name].md` does not meet the standard set by `user-activation.md`, then update `[document-name].md` everywhere required in order to bring `[document-name].md` up to the standard set by `user-activation.md`, and then note in the task log Execution log the additions you made, then mark this as complete.
---

## Tips for Success

**Start with the template**: Use `.claude/templates/documents/supplemental_doc_template.md` as your starting point—it has all the boilerplate ready.

**Reference existing docs**: Look at similar supplemental docs (like `user-activation.md`) to see patterns and quality standards.

**Iterate**: Don't try to make it perfect on first pass. Create structure first, then populate content, then polish.

**Use research**: Back up claims with industry data, benchmarks, and research. Bold key statistics.

**Be specific to GFxAI**: Don't just summarize generic best practices—interpret them for our specific product and users.

**Think about consumers**: Who will read this? What do they need to know? How will they use it?

**Maintain consistency**: Follow the same patterns, formatting, and structure as other docs in the system.
