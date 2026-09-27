---
title: "File, Page, and Task Conventions"
description: "Guidelines for file naming, frontmatter for project documentation pages and MDTM task files, content hierarchy, and agent task output conventions."
id: "file-conventions"
sidebar_position: 3
created_date: "2025-08-05"
last_updated: "2025-08-05"
version: 1.0.0
draft: false
content_status: Published
tags:
- "file-conventions"
- frontmatter
- "page-structure"
- "task-structure"
- mdtm
- "agent-output"
- standards
content_type: CoreConcept
target_audience:
- Beginner
- IntermediateUser
- AdvancedUser
- Developer
- ComponentDeveloper
- SystemDesigner
- SystemArchitect
- QAEngineer
- AI
- Machine
owner: "documentation-team"
autogen: false
autogen_method: ""
autogen_source: []
autogen_version: ""
ai_model: ""
model_settings: ""
source_references:
- path: ".roo/all-general-rules-processes-workflows/file_conventions.md"
  type: context_doc
  version_hash: ""
  description: Base document adapted for generic file conventions.
related_links:
- text: IB Agent Core
  link: ~/.claude/rules/core/ib_agent_core.md
- text: Quality Gates
  link: ~/.claude/rules/core/quality_gates.md
related_task_id:
- "TASK-GENERIC-20250805-100200-CreateGenericFileConventions"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: "2026-02-05"
---

# File, Page, and Task Conventions

## Common Frontmatter Fields (Shared Across Documentation & Tasks)

The following fields are used in both documentation pages and MDTM task files with identical conventions. These are defined once here to avoid duplication.

### Tags Field (Shared)

* **`tags`** (Array of Strings, **Mandatory**)
    * **Description:** A list of relevant keywords for discoverability, filtering, and search. Tags should be lowercase and use kebab-case for multiple words.
    * **Example:**
        ```yaml
        tags:
        - core-framework
        - architecture
        - design-philosophy
        - public
        - cpp
        ```
    * **Selection Guidance and Rules:**
        *   **Minimum:** Each page/task MUST have at least 3 tags.
        *   **Maximum:** Aim for 5-10 tags per page/task to maintain relevance and avoid clutter.
        *   **Relevance:** Tags MUST directly relate to the content, topic, or purpose.
        *   **Consistency:** Use existing tags where appropriate. If a new tag is needed, ensure it is generic enough to be reused.
        *   **Format:** All tags MUST be lowercase and use kebab-case for multiple words (e.g., `system-architecture`, `api-reference`).

### AI Model Field (Shared)

* **`ai_model`** (String, **Mandatory - Relevant if autogen: true AND using AI**)
    * **Description:** Name and version of the AI model used for generation.
    * **Example:** `"Claude-3-Opus-20240229"`
    * **Selection Guidance and Rules:**
        *   **Mandatory for AI Generation:** If `autogen` is `true` and the method involves AI, this field MUST be populated with the exact name and version of the AI model used.
        *   **Reproducibility:** Crucial for reproducing AI outputs and understanding model behavior.
        *   **Specificity:** Include the specific model version (e.g., `Claude-3-Opus-20240229`, `gpt-4-turbo-2024-04-09`).

### Model Settings Field (Shared)

* **`model_settings`** (String or Object, Mandatory if autogen: true AND using AI)
    * **Description:** Defines the exact, specific settings used for the AI model during content generation or task execution. This information is crucial for reproducibility, debugging, and fine-tuning generation processes. All relevant and influential settings used MUST be recorded. It MUST be a stringified JSON for comprehensive settings, including all listed key settings below, even if their values are default or empty.
    * **Key Settings to Capture (MUST include all of these as keys in the JSON string):**
        * `temperature` (Float): The sampling temperature. E.g., `0.7`.
        * `max_output_tokens` (Integer): Maximum number of tokens to generate. E.g., `4096`.
        * `top_p` (Float): Nucleus sampling parameter. E.g., `0.95`.
        * `top_k` (Integer): Top-k sampling parameter. E.g., `40`.
        * `prompt_id` (String): A unique identifier, version, or hash of the specific prompt template or user-facing prompt used. E.g., `"component_overview_v1.2_prompt"`, `"sha256:prompt_xyz..."`.
        * `system_prompt_id` (String): A unique identifier, version, or hash of the system prompt or persona instructions provided to the model. E.g., `"technical_writer_persona_v2.1"`, `"default_system_v1"`.
        * `stop_sequences` (Array of Strings): Any specific sequences used to stop generation. E.g., `["</DOCUMENT_END>", "### Next Section:"]`.
        * `frequency_penalty` (Float): Penalty for token frequency. E.g., `0.0`.
        * `presence_penalty` (Float): Penalty for token presence. E.g., `0.0`.
        * *(Add any other model-specific parameters that significantly influence output and are part of your standard generation process, ensuring they are also explicitly listed here).*
    * **Example (stringified JSON - MANDATORY format for comprehensiveness):**
        `"{\"temperature\": 0.6, \"max_output_tokens\": 2048, \"top_p\": 0.9, \"top_k\": 40, \"prompt_id\": \"guide_section_generator_v2.3\", \"system_prompt_id\": \"project_expert_v1.1\", \"stop_sequences\": [], \"frequency_penalty\": 0.0, \"presence_penalty\": 0.0}"`
    * **Selection Guidance and Rules:**
        *   **Reproducibility:** This field is critical for reproducing AI outputs and debugging generation issues.
        *   **Completeness:** This field MUST include all parameters listed above, even if their values are default or empty. Do not omit any of the specified keys.
        *   **Format:** MUST be a stringified JSON.
        *   **Mandatory for AI Generation:** If `autogen` is `true` and using AI, this field is MANDATORY and MUST be fully populated as per the completeness rule.

### Review Info Field (Shared)

* **`review_info`** (Object, **Mandatory**)
    * **Description:** Metadata about the content review status.
    * **Sub-fields:**
        * `last_reviewed_by`: (String or Array of Strings) - The slug(s) of the AI agent(s) or human(s) who last formally reviewed the content.
        * `last_review_date`: (Date `YYYY-MM-DD`) - The date of the most recent formal review.
        * `next_review_date`: (Date `YYYY-MM-DD`, **Mandatory**) - Set a future date for the next scheduled review.
    * **Example:**
        ```yaml
        review_info:
          last_reviewed_by: "qa-reviewer"
          last_review_date: "2025-05-20"
          next_review_date: "2025-11-20"
        ```
    * **Selection Guidance and Rules:**
        *   **`last_reviewed_by`:** Record the slug(s) of the AI agent(s) or human(s) who last formally reviewed the content.
        *   **`last_review_date`:** The date of the most recent formal review. This should be updated with last update date if the review is part of a content update.
        *   **`next_review_date`:** Set a future date for the next scheduled review, typically based on content volatility or a predefined review cadence.
        *   **Optionality:** This entire block is optional, but highly recommended for critical documentation/tasks to ensure content freshness and accuracy.

---

## File and Page Structure Conventions for Documentation

* **File Naming (Documentation Pages):**
    * Use lowercase with hyphens (kebab-case) for filenames (e.g., `getting-started.md`, `user-guide-overview.md`).
* **File Naming (API Reference Pages):**
    * Use naming conventions appropriate to your project (e.g., PascalCase matching the primary element name). 
* **Front-Matter for Documentation Pages:**
    All `.md` documentation files within your documentation root and its subdirectories MUST include a YAML frontmatter block enclosed in `---` delimiters. The following fields are defined:

   **General Rule for All Fields (Mandatory Inclusion):** All frontmatter fields defined in the schema for a given document type MUST be present in the template and in all generated or manually created files. If a field's value is not applicable or is unknown, it MUST be included but left blank or with an appropriate placeholder (e.g., `field_name: ""` for strings, `field_name: []` for arrays, `field_name: {}` for objects, or `field_name: false` for booleans if `false` is the default). Commented-out examples or descriptions within the schema MUST also be preserved. This ensures a consistent and complete schema across all documents.

    #### Core Identification & Discovery:

    * **`title`** (String, **Mandatory**)
        * **Description:** The main H1 page title. Should be human-readable and not include numeric prefixes (those are for directory naming/ordering).
        * **Example:** `"Project Architecture Overview"`

    * **`description`** (String, **Mandatory**)
        * **Description:** A concise summary (ideally 150-250 characters) of the page content. Used for SEO, LLM context, and search result snippets.
        * **Example:** `"A high-level overview of the project's major components, design philosophy, and their interactions."`

    * **`id`** (String, **Mandatory**)
        * **Description:** A unique, stable identifier for this documentation page itself. Useful for persistent linking, tracking, and content management.
        * **Convention:** `kebab-case-semantic-id` (e.g., `system-architecture`, `core-concept-integration`) or a UUID.
        * **Example:** `"core-arch-overview"`
        * **Selection Guidance and Rules:**
            *   **Uniqueness:** The `id` MUST be unique across all documentation pages.
            *   **Stability:** Once assigned, the `id` SHOULD NOT change to ensure persistent links and traceability.
            *   **Semantic Meaning:** The IDs should be semantically meaningful and reflect the page's content or purpose.
            *   **Format:** Use `kebab-case` for readability.
            *   **Mandatory for Cross-Referencing:** While optional, it becomes effectively mandatory if the page is intended to be referenced by other documents or tasks.

    #### Navigation & Presentation:

    * **`sidebar_position`** (Integer, **Mandatory** for most files)
        * **Description:** An integer defining the relative order of this page within its directory/sidebar section. Lower numbers appear first.
        * **Example:** `1`
        * **Selection Guidance and Rules:**
            *   **Ordering:** Lower numbers appear higher in the sidebar navigation.
            *   **Gaps Allowed:** It is acceptable to leave gaps in numbering (e.g., `1, 5, 10`) to allow for future insertions without renumbering all pages.
            *   **Consistency:** Maintain consistent numbering within a given directory.
            *   **`index.md`:** The `index.md` file in a directory should typically have `sidebar_position: 1` or `0` to appear first, or be omitted if the navigation system handles it implicitly.

    #### Status, Lifecycle & Versioning:

    * **`created_date`** (Date, **Mandatory**)
        * **Description:** The date (YYYY-MM-DD) when this documentation file was initially created.
        * **Format:** `YYYY-MM-DD`
        * **Example:** `"2025-01-15"`
        * **Selection Guidance and Rules:**
            *   **Initial Creation:** This date should be set when the file is first created and generally not changed unless the content is completely rewritten in its entirety.
            *   **Accuracy:** Ensure the date accurately reflects the initial creation time.

    * **`last_updated`** (Date, **Mandatory**)
        * **Description:** The date (YYYY-MM-DD) when the content of this page was last significantly modified or reviewed for accuracy.
        * **Format:** `YYYY-MM-DD`
        * **Example:** `"2025-05-24"`
        * **Selection Guidance and Rules:**
            *   **Mandatory Update:** This date MUST be updated every time the content of the page is significantly modified or reviewed for accuracy.
            *   **Automated vs. Manual:** Ideally, this should be automatically updated by the system upon commit or content review, but manual updates are required if automation is not in place.
            *   **Reflects Freshness:** This field indicates the freshness and reliability of the content.

    * **`version`** (String, **Mandatory**)
        * **Description:** A semantic version number (e.g., `1.0.0`, `2.1.3`) for this specific documentation page, useful if the content tracks a versioned component, API, or undergoes major, distinct revisions.
        * **Example:** `"1.1.0"`
        * **Selection Guidance and Rules:**
            *   **Major Revisions:** Update the major version (e.g., `1.x.x` to `2.x.x`) for significant structural changes, complete rewrites, or when the documented component undergoes a major version change.
            *   **Minor Updates:** Update the minor version (e.g., `x.1.x` to `x.2.x`) for substantial content additions, reorganizations, or significant accuracy improvements.
            *   **Patches:** Update the patch version (e.g., `x.x.1` to `x.x.2`) for small corrections, typos, or minor clarifications.
            *   **Alignment:** If the page documents a specific versioned component (e.g., a plugin), its `version` should ideally align with that component's version.
            *   **Omit if N/A:** If versioning is not relevant for the content (e.g., a general style guide), this field can be omitted.

    * **`draft`** (Boolean, **Mandatory**)
        * **Description:** If `true`, the page is considered a draft and might be excluded from production builds or marked accordingly. If `false` or omitted, it's considered ready for publishing.
        * **Options:** `true`, `false`.
        * **Selection Guidance and Rules:**
            *   **Default:** Always set to `true` unless explicitly instructed otherwise or if the content is clearly final and complete
            *   **AI-Generated Content:** For initial AI-generated drafts, set to `true`. Once reviewed and approved by a human or a dedicated review agent, update to `false`.
            *   **Human-Written Content:** Set to `true` only during active writing phases where the content is not yet ready for public consumption.

    * **`content_status`** (String, **Mandatory**)
        * **Description:** The current editorial or review status of the page's content.
        * **Options (Adopt a consistent set):** `"Draft"`, `"InReview"`, `"NeedsUpdate"`, `"TechReviewed"`, `"Published"`, `"Archived"`.
        * **Example:** `"Published"`
        * **Selection Guidance and Rules:**
            *   **`"Draft"`:** For newly created pages (human or AI) that are not yet ready for review.
            *   **`"InReview"`:** When the page has been submitted for human or automated review in the documentation process.
            *   **`"NeedsUpdate"`:** If the content is identified as outdated, inaccurate, or requiring significant additions.
            *   **`"TechReviewed"`:** After a technical expert (human or AI specialist) has verified the accuracy and completeness of the technical content.
            *   **`"Published"`:** For content deemed ready for public consumption. This is the default target status for completed documentation.
            *   **`"Archived"`:** For deprecated or superseded content that should no longer be actively maintained or displayed prominently.

    #### Content Categorization:

    * **`tags`** - See "Common Frontmatter Fields" section above for full field definition.

    * **`content_type`** (String, **Mandatory**)
        * **Description:** A structured category defining the primary purpose or type of the page.
        * **Options (Define your canonical list based on your project structure):** `"Overview"`, `"Introduction"`, `"GettingStarted"`, `"CoreConcept"`, `"ArchitecturalDeepDive"`, `"ComponentReference"`, `"APIReferencePage"`, `"Guide"`, `"Tutorial"`, `"BestPractice"`, `"TroubleshootingFAQ"`, `"GlossaryEntry"`, `"Changelog"`
        * **Example:** `"ArchitecturalDeepDive"`
        * **Selection Guidance and Rules:**
            *   **`"Overview"`:** A high-level summary of a broad topic or section.
            *   **`"Introduction"`:** Initial page for a new concept or section, providing foundational context.
            *   **`"GettingStarted"`:** Step-by-step instructions for initial setup or first-time use.
            *   **`"CoreConcept"`:** Explains fundamental ideas, principles, or systems within the project.
            *   **`"ArchitecturalDeepDive"`:** Detailed explanation of system architecture, design patterns, or complex interactions.
            *   **`"ComponentReference"`:** Overview or detailed information about a specific project component.
            *   **`"APIReferencePage"`:** Auto-generated or manually curated documentation for a specific API element.
            *   **`"Guide"`:** Provides comprehensive instructions or best practices for a specific task or feature.
            *   **`"Tutorial"`:** A step-by-step walkthrough to achieve a specific outcome.
            *   **`"BestPractice"`:** Recommendations for optimal usage, performance, or maintainability.
            *   **`"TroubleshootingFAQ"`:** Solutions to common problems or frequently asked questions.
            *   **`"GlossaryEntry"`:** Defines a specific term or acronym.
            *   **`"Changelog"`:** Records changes and updates to the documentation or project.
            *   **Single Type:** A page should generally have only one `content_type`. Choose the most dominant type.

    * **`target_audience`** (Array of Strings, **Mandatory**)
        * **Description:** Specifies the primary intended audience(s) for this page's content.
        * **Options (Define your canonical list):** `"Beginner"`, `"IntermediateUser"`, `"AdvancedUser"`, `"Developer"`, `"ComponentDeveloper"`, `"SystemDesigner"`, `"SystemArchitect"`, `"QAEngineer"`, `"AI"`, `"Machine"`
        * **Example:**
            ```yaml
            target_audience:
            - SystemArchitect
            - Developer
            - AI
            ```
        * **Selection Guidance and Rules:**
            *   **Default:** If the primary audience is not clearly defined or the content is broadly applicable, select *all* available options from the list.
            *   **Prioritize Specificity:** If a specific audience is clearly intended, choose only the most relevant option(s).
            *   **Multiple Audiences:** A page can target multiple audiences if the content is relevant to all.
            *   **`"AI"` / `"Machine"`:** Include these if the content is specifically structured or intended for consumption by AI agents (e.g., context documents, rule files, API definitions).

    #### Authorship, Ownership & Generation Details:

    * **`owner`** (String or Array of Strings, **Mandatory**)
        * **Description:** The primary individual, team, or AI agent persona responsible for the content's accuracy and maintenance.
        * **Example:** `"CoreArchitectureTeam"`, `"content-author"`
        * **Selection Guidance and Rules:**
            *   **Accountability:** Assign to the individual, team, or AI agent persona that is ultimately responsible for the content's accuracy, completeness, and ongoing maintenance.
            *   **Team vs. Individual:** Prefer team names (e.g., `"CoreTeam"`) for broader ownership, or specific AI agent slugs (e.g., `"content-author"`) if an agent is designated for maintenance.
            *   **Human Fallback:** If an AI agent is the primary owner, ensure there's a human oversight or fallback team implicitly responsible.
            *   **Consistency:** Use consistent naming for teams or agent personas across all documentation.
            *   **Mandatory for Critical Content:** While optional, it is highly recommended to assign an `owner` for all critical or frequently updated documentation pages to ensure clear accountability.

    * **`autogen`** (Boolean, **Mandatory**)
        * **Description:** If `true`, indicates the page content is primarily auto-generated.
        * **Options:** `true`, `false`.
        * **Selection Guidance and Rules:**
            *   **`true`:** Set to `true` if the page content is primarily generated by an automated process (AI, script, data merge). This implies that the content might be regenerated periodically and should not be manually edited directly without considering the automation.
            *   **`false`:** Set to `false` if the page content is primarily human-written or manually curated. Manual edits are expected and encouraged for these pages.
            *   **Hybrid Content:** If a page contains a mix of auto-generated and human-written content, set `autogen` to `true` if the *majority* or *core* of the content is automated, and ensure `autogen_method` and `autogen_source` are specified.

    * **`autogen_method`** (String, **Mandatory - Relevant if `autogen: true`**)
        * **Description:** Specifies the primary method used for automated generation if `autogen` is `true`.
        * **Options (Define your list):** `"AI"`, `"ProgrammaticScript"`, `"DataMerge"`.
        * **Example:** `"AI"`
        * **Selection Guidance and Rules:**
            *   **`"AI"`:** Select if the content was primarily generated by an AI model (e.g., Claude, GPT).
            *   **`"ProgrammaticScript"`:** Select if the content was generated by a custom script or tool that processes data or code (e.g., an API documentation generator).
            *   **`"DataMerge"`:** Select if the content was assembled by merging data from multiple structured sources.
            *   **Prioritize Primary Method:** Choose the single method that contributed most significantly to the content's generation.

    * **`autogen_source`** (String or Array of Strings, **Mandatory - Relevant if `autogen: true`**)
        * **Description:** Path(s) or identifier(s) of the primary source(s) used for auto-generation. Paths typically relative to project root.
        * **Example:** `"src/components/core/Manager.h"`
        * **Selection Guidance and Rules:**
            *   **Specificity:** Provide the most specific path or identifier to the source material.
            *   **Local Files:** For local files, use paths relative to the project root.
            *   **External Sources:** For external sources, use a stable URL.
            *   **Multiple Sources:** If content is derived from multiple primary sources, list all relevant ones.
            *   **Mandatory for `autogen: true`:** This field MUST be populated if `autogen` is `true` to ensure traceability.

    * **`autogen_version`** (String, **Mandatory - Relevant if `autogen: true`**)
        * **Description:** Hash (e.g., MD5, SHA256) or version identifier (e.g., commit SHA) of the `autogen_source` content at the time of generation.
        * **Example:** `"sha256:a1b2c3d4e5f6abcdef1234567890abcdef1234567890abcdef1234567890ab"`
        * **Selection Guidance and Rules:**
            *   **Reproducibility:** This hash is crucial for verifying that the auto-generated content is based on a specific version of the source.
            *   **Automated Generation:** For auto-generated content, this should ideally be captured automatically during the generation process.
            *   **Consistency:** Use a consistent hashing algorithm (e.g., SHA256) across the project.
            *   **Omit if N/A:** If the `autogen_source` is an external URL or a non-versioned resource, this field can be omitted.

    * **`ai_model`** - See "Common Frontmatter Fields" section above for full field definition.

    * **`model_settings`** - See "Common Frontmatter Fields" section above for full field definition.

    #### Relationships & Traceability:

    * **`source_references`** (Array of Objects, **Mandatory if content is derived from specific sources - MUST do**)
        * **Description:** A list of direct source materials used in the creation or significant modification of this page. Crucial for Dependency Impact Review.
        * **Object Fields:**
            * `path`: (String, Required) Relative path from project root or absolute URL.
            * `type`: (String, Required) Type of source (e.g., `source_code`, `context_doc`). Your defined list should be documented elsewhere.
            * `version_hash`: (String, **Mandatory**) Content hash of local file sources.
            * `description`: (String, **Mandatory**) Note on how the source was used.
        * **Example (adapted for generic context):**
            ```yaml
            source_references:
            - path: "docs/internal/context_overview.md" # Example path from project root
              type: context_doc
              version_hash: ""
              description: "Used for architectural decision context."
            - path: "src/core/components/Manager.h" # Example path from project root
              type: source_code
              version_hash: "sha256:abcdef123456"
              description: "Definition of the Manager class."
            ```
        * **Selection Guidance and Rules:**
            *   **Relevance:** Include links to pages that were used as source material in the creation of this page.
            *   **Quantity:** No limit. All file dependencies MUST be included.
            *   **Internal First:** Prioritize internal documentation links over external URLs.
            *   **Project Root Paths:** Use paths relative to the project root for all internal links.
            *   **Descriptive Text:** Ensure the `text` field is descriptive and clearly indicates what the linked page is about.

    * **`related_links`** (Array of Objects, **Mandatory**)
        * **Description:** 3-5 key related documentation pages or external resources.
        * **Object Fields:** `text` (String, Required), `link` (String, Required - relative to project root or absolute URL).
        * **Example (updated to use project root paths):**
            ```yaml
            related_links:
            - text: "Related Concept A"
              link: "docs/concepts/concept-a.md" # Path relative to project root
            ```
        * **Selection Guidance and Rules:**
            *   **Relevance:** Only include links to pages that are highly relevant and provide significant additional context or next steps for the reader.
            *   **Quantity:** Limit to 3-5 links to avoid overwhelming the reader.
            *   **Internal First:** Prioritize internal documentation links over external URLs.
            *   **Project Root Paths:** Use paths relative to the project root for all internal links.
            *   **Descriptive Text:** Ensure the `text` field is descriptive and clearly indicates what the linked page is about.

    * **`related_task_id`** (String or Array of Strings, **Mandatory**)
        * **Description:** The ID(s) of the MDTM task(s) that led to the creation or last significant update of this document.
        * **Example:** `"TASK-WRITER-20250524-100000-UpdateArchOverview"`
        * **Selection Guidance and Rules:**
            *   **Traceability:** Link to the MDTM task(s) that directly initiated or significantly contributed to the creation or update of this documentation page.
            *   **Multiple Tasks:** If multiple tasks are relevant, list all applicable task IDs.
            *   **Format:** Use the exact `TASK-[...]` ID of the MDTM task.
            *   **Mandatory for AI-Driven Content:** If the page was `autogen: true`, this field is effectively mandatory to trace the AI's work back to a specific task.

    #### Review Metadata (**Mandatory**):

    * **`review_info`** - See "Common Frontmatter Fields" section above for full field definition.

    **Comprehensive Documentation Page Frontmatter Example (Illustrative):**
    ```yaml
    ---
    id: "component-dataloader-advanced-config"
    title: "Advanced Configuration for DataLoader Component"
    description: "Detailed guide on advanced configuration options, performance tuning, and custom extension points for the DataLoader component."
    sidebar_position: 3
    created_date: "2025-04-10"
    last_updated: "2025-05-22"
    version: "1.2.1"
    draft: false
    content_status: Published
    tags:
    - dataloader
    - component
    - advanced
    - configuration
    - performance
    - extension
    - public
    content_type: Guide
    target_audience:
    - AdvancedUser
    - Developer
    - SystemArchitect
    - AI
    owner: "ComponentTeamAlpha"
    autogen: false # Primarily human-written, but might incorporate AI-assisted sections
    autogen_method: "" # If parts were AI generated
    autogen_source: [] # "path/to/specific_source_for_ai_section.h"
    autogen_version: ""
    ai_model: "" # "Claude-3-Opus-20240229"
    model_settings: "" # "{ \"temperature\": 0.4 }"
    source_references:
    - path: "src/components/DataLoader/Public/DataLoaderSettings.h"
      type: source_code_h
      version_hash: ""
      description: "Defines available settings."
    - path: "docs/components/DataLoader/internal/DataLoader_Deep_Analysis_Report_20250405.md"
      type: internal_analysis_report
      version_hash: ""
      description: "Used for understanding internal mechanics."
    related_links:
    - text: "DataLoader Component Overview"
      link: "docs/components/DataLoader/index.md" # Path relative to project root
    - text: "Core Data Handling Concepts"
      link: "docs/concepts/core-data-handling.md" # Path relative to project root
    related_task_id:
    - "TASK-WRITER-20250520-AdvancedDataLoaderGuide"
    review_info:
      last_reviewed_by:
      - jane.doe
      - qa-reviewer
      last_review_date: "2025-05-18"
      next_review_date: "2025-11-18"
    ---
    ```

* **Content Hierarchy within Pages:**
    * **H1:** Only one per page, derived from `title` in front-matter. Not explicitly written in Markdown body.
    * **H2 (`##`):** Major sections.
    * **H3 (`###`):** Sub-sections of H2.
    * **H4 (`####`):** Further subdivision if necessary (prefer lists or more H3s for simpler hierarchies).
    * **Logical Flow:** Content must flow logically from overview to specifics. Each paragraph should focus on a single idea. Use clear topic sentences.

---
## MDTM Task File Conventions 

This section details the conventions specifically for Markdown-Driven Task Management (MDTM) files, typically located within the `.dev/tasks/` directory and its subdirectories.

* **File Naming (MDTM Task Files):**
    * **Convention:** `TASK-[AGENT_TYPE_OR_PURPOSE]-[YYYYMMDD]-[HHMMSS]-[OptionalShortIdentifier].md`
    * **Example:** `TASK-RESEARCH-20250524-155500-FrontmatterReview.md`, `TASK-ORCH-ComponentName-20250525-100000.md`

* **Frontmatter for MDTM Task Files (`.dev/tasks/` files):**
    All `.md` MDTM task files MUST include a YAML frontmatter block enclosed in `---` delimiters. The following fields are defined:

   **General Rule for All Fields (Mandatory Inclusion):** All frontmatter fields defined in the schema for a given task type MUST be present in the template and in all generated or manually created task files. If a field's value is not applicable or is unknown, it MUST be included but left blank or with an appropriate placeholder (e.g., `field_name: ""` for strings, `field_name: []` for arrays, `field_name: {}` for objects, or `field_name: false` for booleans if `false` is the default). Commented-out examples or descriptions within the schema MUST also be preserved. This ensures a consistent and complete schema across all tasks.

    #### Mandatory Frontmatter Fields:

    * **`id`** (String)
        * **Description:** A globally unique identifier for the task.
        * **Convention:** `TASK-[AGENT_TYPE_OR_PURPOSE]-[YYYYMMDD]-[HHMMSS]-[OptionalShortIdentifier]`
        * **Selection Guidance and Rules:**
            *   **Uniqueness:** The `id` MUST be unique across all MDTM task files.
            *   **Stability:** Once assigned, the `id` SHOULD NOT change to ensure persistent links and traceability.
            *   **Format:** Adhere strictly to the `TASK-[AGENT_TYPE_OR_PURPOSE]-[YYYYMMDD]-[HHMMSS]-[OptionalShortIdentifier]` format.
            *   **`AGENT_TYPE_OR_PURPOSE`:** Use a concise slug representing the primary agent type (e.g., `RESEARCH`, `WRITER`, `ORCH`) or the task's main purpose.
            *   **`YYYYMMDD` & `HHMMSS`:** Use the creation date and time to ensure uniqueness.
            *   **`OptionalShortIdentifier`:** A brief, kebab-cased identifier for human readability (e.g., `FrontmatterReview`, `ComponentXGuideY`).

    * **`title`** (String)
        * **Description:** A concise, human-readable title summarizing the task's objective.
       * **Selection Guidance and Rules:**
           *   **Clarity:** The title MUST clearly and concisely convey the main purpose of the task.
           *   **Action-Oriented:** Start with an action verb where appropriate (e.g., "Implement X", "Fix Y", "Draft Z").
           *   **Brevity:** Keep the title short, ideally under 10 words, for easy readability and display in task lists.
           *   **Uniqueness (within context):** While not globally unique like `id`, aim for titles that are distinct enough within a given project phase or component.

    * **`description`** (String)
        * **Description:** A brief (1-2 sentences) explanation of the task's purpose, scope, and expected outcome.
       * **Selection Guidance and Rules:**
           *   **Conciseness:** Keep the description brief, ideally 1-2 sentences.
           *   **Purpose & Outcome:** Clearly state *why* the task is being done and *what* the successful completion looks like.
           *   **Scope:** Briefly outline the boundaries of the task.
           *   **Avoid Duplication:** Do not repeat information already present in the `title` or `id`.

    * **`status`** (String)
        * **Description:** The current lifecycle status of the task.
        * **Options:** `"🔵 Backlog"`, `"🟡 To Do"`, `"🟠 Doing"`, `"🔴 Blocked"`, `"🟢 Done"`, `"⚪ Cancelled"`.
        * **Selection Guidance and Rules:**
            *   **`"🔵 Backlog"`:** For tasks identified but not yet prioritized or assigned.
            *   **`"🟡 To Do"`:** For tasks ready to be picked up by an assigned agent.
            *   **`"🟠 Doing"`:** Set by the assigned agent immediately upon starting work on the task.
            *   **`"🔴 Blocked"`:** Set by the assigned agent if an external dependency or issue prevents progress. Requires `blocker_reason`.
            *   **`"🟢 Done"`:** Set by the assigned agent upon successful completion of all acceptance criteria.
            *   **`"⚪ Cancelled"`:** For tasks that are no longer relevant or have been superseded.

    * **`type`** (String)
        * **Description:** Categorizes the nature or domain of the task.
        * **Options (Recommended Base):** `"✨ Feature"`, `"🐛 BugFix"`, `"📚 Documentation"`, `"⚙️ Maintenance"`, `"🔬 Research/Spike"`, `"✅ Verification/QA"`, `"🧩 Integration"`, `"🗣️ Review"`, `"⚙️ Orchestration"`, `"💡 Planning/Strategy"`, `"⚙️ Process Improvement"`, `"🔧 AI Prompt Engineering"`, `"📊 AI Output Analysis"`, `"🛠️ Tooling/Automation"`
        * **Selection Guidance and Rules:**
            *   **Categorize Accurately:** Select the option that best describes the primary nature of the task.
            *   **`"✨ Feature"`:** For tasks implementing new functionalities or significant enhancements.
            *   **`"🐛 BugFix"`:** For tasks addressing defects or unintended behaviors.
            *   **`"📚 Documentation"`:** For tasks directly related to creating, updating, or reviewing documentation content.
            *   **`"⚙️ Maintenance"`:** For tasks involving routine upkeep, refactoring (without changing external behavior), or minor improvements.
            *   **`"🔬 Research/Spike"`:** For exploratory tasks to gather information, evaluate technologies, or test concepts before full implementation.
            *   **`"✅ Verification/QA"`:** For tasks focused on testing, quality assurance, or validating existing features.
            *   **`"🧩 Integration"`:** For tasks involving connecting different systems, modules, or APIs.
            *   **`"🗣️ Review"`:** For tasks requiring a formal review of code, design, or documentation.
            *   **`"⚙️ Orchestration"`:** For tasks managed by orchestrator or coordinator agents that involve delegating and coordinating multiple sub-tasks.
            *   **`"💡 Planning/Strategy"`:** For tasks related to high-level design, roadmap definition, or strategic decision-making.
            *   **`"⚙️ Process Improvement"`:** For tasks aimed at optimizing workflows, tools, or operational procedures.
            *   **`"🔧 AI Prompt Engineering"`:** For tasks focused on designing, testing, or refining prompts and instructions for AI models.
            *   **`"📊 AI Output Analysis"`:** For tasks involving the review, validation, or synthesis of AI-generated content or data.
            *   **`"🛠️ Tooling/Automation"`:** For tasks developing or improving internal tools, scripts, or automation processes.

    * **`priority`** (String)
        * **Description:** The urgency and impact of the task.
        * **Options:** `"🔥 Highest"`, `"🔼 High"`, `"▶️ Medium"`, `"🔽 Low"`, `"🧊 Lowest"`.
        * **Selection Guidance and Rules:**
            *   **`"🔥 Highest"`:** Critical, blocking issues or immediate priorities with significant impact.
            *   **`"🔼 High"`:** Important tasks that should be addressed soon, impacting key features or workflows.
            *   **`"▶️ Medium"`:** Standard priority tasks, part of regular development cycles.
            *   **`"🔽 Low"`:** Minor improvements, non-urgent fixes, or backlog items that can be deferred.
            *   **`"🧊 Lowest"`:** Very low impact, long-term considerations, or tasks that may never be actioned.
            *   **Coordinator Discretion:** The coordinator or delegating lead should assign priority based on project goals and current context.

    * **`created_date`** (Date)
        * **Description:** The date (YYYY-MM-DD) when the task was initially created/logged.
        * **Format:** `YYYY-MM-DD`
       * **Selection Guidance and Rules:**
           *   **Initial Creation:** This date MUST be set when the task file is first created.
           *   **Immutability:** This date should generally not be changed after initial creation, as it marks the task's inception.
           *   **Accuracy:** Ensure the date accurately reflects the actual creation time.

    * **`updated_date`** (Date)
        * **Description:** The date (YYYY-MM-DD) when the task frontmatter or body was last significantly updated.
        * **Format:** `YYYY-MM-DD`
       * **Selection Guidance and Rules:**
           *   **Initial Creation:** This date should be set when the task file is initially created.
           *   **Automated Update:** Ideally, this should be automatically updated by the system when the task status changes or significant edits are made to the file.
           *   **Manual Update:** If automation is not in place, the assigned agent MUST manually update this date whenever they make significant progress or changes to the task file.

    * **`assigned_to`** (String)
        * **Description:** The slug/identifier of the AI agent or human user primarily responsible for executing the task.
        * **Options:** Agent slugs (e.g., `code-analyst`, `content-author`, `orchestrator`), user IDs.
        * **Selection Guidance and Rules:**
            *   **Specific Agent:** Assign to the specific AI agent mode (e.g., `content-author`, `code-analyst`) that is best suited to perform the task.
            *   **Orchestrator:** Assign to `orchestrator` if the task requires high-level coordination, planning, or delegation to multiple sub-tasks.
            *   **Human User:** Assign to a specific human user ID if the task requires manual intervention or human expertise.
            *   **Default:** Always assign to the most appropriate and available agent or human.

    * **`autogen`** (Boolean)
        * **Description:** Indicates if the primary work/output of this task is expected to be automatically generated (by AI/script) versus primarily manual human effort.
        * **Options:** `true`, `false`.
        * **Selection Guidance and Rules:**
            *   **`true`:** Set to `true` if the primary work or output of this task is expected to be generated automatically by an AI model or a script.
            *   **`false`:** Set to `false` if the task primarily requires manual human effort or direct human interaction.
            *   **Hybrid Tasks:** If a task involves significant portions of both automated generation and manual refinement, consider the *dominant* method for the `autogen` flag. If the initial draft or core output is automated, set to `true`.

    * **`method`** (String)
        * **Description:** The primary method used to complete the task.
        * **Options:** `"AI"`, `"Programmatic"`, `"Manual"`, `"Hybrid"`.
        * **Selection Guidance and Rules:**
            *   **`"AI"`:** The task is primarily executed by an AI model.
            *   **`"Programmatic"`:** The task is completed by an automated script or program (non-AI).
            *   **`"Manual"`:** The task requires direct human effort.
            *   **`"Hybrid"`:** The task involves a significant combination of automated (AI or programmatic) and manual steps.
            *   **Consistency with `autogen`:** If `autogen` is `true`, `method` should typically be `"AI"` or `"Programmatic"`. If `autogen` is `false`, `method` should typically be `"Manual"` or `"Hybrid"`.

    * **`coordinator`** (String)
        * **Description:** The AI agent or human user overseeing this task, if different from `assigned_to`.
        * **Options:** Agent slugs, user IDs, `orchestrator`.
        * **Selection Guidance and Rules:**
            *   **Default:** If the task is part of a larger workflow managed by a specific coordinator, set this to the coordinator's slug or ID.
            *   **Self-Coordination:** If an agent is self-coordinating a task, this field can be omitted or set to the agent's own slug.
            *   **Orchestrator:** Set to `orchestrator` if the task was directly delegated by the top-level orchestrator.

    * **`parent_task`** (String)
        * **Description:** The ID or path of a higher-level task, feature, user story, epic, or issue this task contributes to.
        * **Selection Guidance and Rules:**
            *   **Mandatory for Sub-tasks:** If this task is a sub-task of a larger, overarching task (e.g., an orchestrator task), this field MUST be populated with the parent task's ID.
            *   **Feature/Epic Link:** Link to the relevant feature, user story, or epic ID if the task directly contributes to it.
            *   **Format:** Use the `TASK-[...]` format for internal MDTM tasks, or other agreed-upon identifiers for external systems.

    * **`depends_on`** (Array of Strings)
        * **Description:** A list of task IDs that MUST be completed before this task can start.
        * **Example:**
            ```yaml
            depends_on:
            - TASK-ID-001
            - TASK-ID-002
            ```
        * **Selection Guidance and Rules:**
            *   **Identify Pre-requisites:** List all immediate predecessor tasks that must reach a `"🟢 Done"` status before this task can begin.
            *   **Avoid Circular Dependencies:** Ensure that no circular dependencies are introduced.
            *   **Granularity:** Only list direct dependencies; avoid transitive dependencies (i.e., if A depends on B, and B depends on C, only list B as a dependency for A).
            *   **Format:** Use the exact `TASK-[...]` ID of the dependent MDTM task.

    * **`related_docs`** (Array of Strings or Objects)
        * **Description:** List of paths to related plan files, source code, or other artifacts providing context. Paths should be relative to the project root or a known base.
        * **Example:**
            ```yaml
            related_docs:
            - path: ".claude/processes/some_process.md"
              description: "Relevant Process"
            ```
        * **Selection Guidance and Rules:**
            *   **Provide Context:** Include paths to any documents (e.g., requirements, design docs, analysis reports, other MDTM tasks) that are essential for understanding or completing this task.
            *   **Relative Paths:** Prefer paths relative to the project root for consistency.
            *   **Description:** Always provide a brief `description` for each linked document to explain its relevance.

    * **`tags`** - See "Common Frontmatter Fields" section above for full field definition.

    * **`template_schema_doc`** (String)
        * **Description:** Path to a document defining the expected structure for *this task file's body content*, if applicable.
        * **Selection Guidance and Rules:**
            *   **Specify Template:** If the task body is expected to follow a specific Markdown template (e.g., for analysis reports, detailed guides), provide the relative path to that template file (e.g., `.claude/templates/01_mdtm_general.md`).
            *   **Omit if Free-form:** If the task body is free-form or does not adhere to a specific template, this field can be omitted.

    * **`estimation`** (String or Integer)
        * **Description:** An estimate of the effort, size, or complexity.
        * **Recommended System (T-Shirt Sizes - String):** `"XS"`, `"S"`, `"M"`, `"L"`, `"XL"` (Define meanings with examples for your project).
        * **Alternatives:** Story Points (e.g., `1, 2, 3, 5, 8`), Ideal Time (e.g., `"0.5d"`, `"4h"`).
        * **Selection Guidance and Rules:**
            *   **T-Shirt Sizes (Default):** Prefer `"XS"`, `"S"`, `"M"`, `"L"`, `"XL"` for general estimation.
                *   `"XS"`: Very small, quick task (e.g., minor text edit, single line code change).
                *   `"S"`: Small task (e.g., adding a new field, simple bug fix).
                *   `"M"`: Medium task (e.g., implementing a small feature, writing a guide section).
                *   `"L"`: Large task (e.g., implementing a complex feature, major refactoring).
                *   `"XL"`: Very large task, potentially requiring further breakdown.
            *   **Consistency:** Use the chosen system consistently across all tasks.
            *   **Re-estimate if Needed:** If a task's scope changes significantly, update the estimation.

    * **`sprint`** (String or Integer)
        * **Description:** Identifier of the sprint/iteration if using time-boxed cycles.
        * **Format Example:** `"Sprint 2025.12"`, `202507`.
        * **Selection Guidance and Rules:**
            *   **Assign to Current Sprint:** If the task is part of an active sprint, assign the current sprint identifier.
            *   **Future Sprints:** Can be assigned to a future sprint if planned.
            *   **Omit if not using Sprints:** If the project does not use a sprint methodology, this field can be omitted.

    * **`due_date`** (Date)
        * **Description:** Target completion date (YYYY-MM-DD), if there's a specific deadline.
        * **Format:** `YYYY-MM-DD`
        * **Selection Guidance and Rules:**
            *   **Hard Deadlines:** Set if there is a strict, non-negotiable deadline for the task.
            *   **Prioritization:** Can influence task priority.
            *   **Omit if Flexible:** If the task has no specific deadline, this field can be omitted.

    * **`start_date`** (Date)
        * **Description:** Date (YYYY-MM-DD) when active work on the task began.
        * **Format:** `YYYY-MM-DD`
        * **Selection Guidance and Rules:**
            *   **Set on Commencement:** The assigned agent MUST set this date when they begin active work on the task (e.g., when changing `status` to `"🟠 Doing"`).
            *   **Automated Update:** Ideally, this should be automatically updated by the system when the task status changes.

    * **`completion_date`** (Date)
        * **Description:** Date (YYYY-MM-DD) when the task was completed.
        * **Format:** `YYYY-MM-DD`
        * **Selection Guidance and Rules:**
            *   **Set on Completion:** The assigned agent MUST set this date when they complete the task (e.g., when changing `status` to `"🟢 Done"`).
            *   **Automated Update:** Ideally, this should be automatically updated by the system when the task status changes.

    * **`blocker_reason`** (String)
        * **Description:** If `status = "⚪ Blocked"`, a brief explanation of the impediment.
        * **Selection Guidance and Rules:**
            *   **Mandatory for Blocked Status:** If the `status` is set to `"⚪ Blocked"`, this field MUST be populated with a clear, concise explanation of what is impeding progress.
            *   **Actionable Information:** The reason should ideally provide enough information for a coordinator or another agent to help resolve the blocker.

    * **`ai_model`** - See "Common Frontmatter Fields" section above for full field definition.

    * **`model_settings`** - See "Common Frontmatter Fields" section above for full field definition.

    * **`review_info`** - See "Common Frontmatter Fields" section above for full field definition.

    **Example MDTM Task Frontmatter (Illustrative):**
    ```yaml
    ---
    id: "TASK-WRITER-20250615-093000-ComponentXGuideY"
    title: "Draft User Guide for ComponentX Feature Y"
    description: "Create the first draft of the user guide explaining how to configure and use Feature Y in ComponentX, based on analysis outputs."
    status: "🟡 To Do"
    type: "📚 Documentation"
    priority: "🔼 High"
    created_date: "2025-06-15"
    updated_date: "2025-06-15"
    assigned_to: "content-author"
    autogen: true
    method: AI
    coordinator: orchestrator
    parent_task: "TASK-ORCH-ComponentX-20250614-100000" # Orchestrator task for ComponentX
    depends_on:
    - "TASK-REVIEW-ComponentX-Approval"
    related_docs:
    - path: ".claude/processes/content_writing_guide.md"
      description: "Process Guide"
    - path: ".dev/tasks/ORCH-ComponentX/TASK-Analysis.md"
      description: "Analysis Output"
    tags:
    - componentX
    - guide
    - user-documentation
    template_schema_doc: ""
    estimation: M
    sprint: "Sprint 2025.13"
    due_date: ""
    start_date: ""
    completion_date: ""
    blocker_reason: ""
    ai_model: "Claude-3-Opus-20240229"
    model_settings: "{\"temperature\": 0.6, \"max_output_tokens\": 2048, \"top_p\": 0.9, \"top_k\": 40, \"prompt_id\": \"guide_section_generator_v2.3\", \"system_prompt_id\": \"project_expert_v1.1\", \"stop_sequences\": [], \"frequency_penalty\": 0.0, \"presence_penalty\": 0.0}"
    review_info:
      last_reviewed_by: ""
      last_review_date: ""
      next_review_date: ""
    ---

    # Task Body

    ## Goal
    ...
    ```
---

## Agent Task Output Conventions

This section applies if AI agents are configured to produce persistent log files or other output artifacts beyond their primary structured output to the orchestrator.

Persistent agent output files should follow a consistent naming convention, e.g., `TASK-<task_id>-<agent_slug>-<timestamp>-output.log` or `.json`.

The content of these files should also adhere to a structured format where possible, to facilitate parsing and review.

Sensitive information or excessive verbosity should be avoided in these persistent logs; detailed operational traces are typically handled by the orchestrator's internal logging.