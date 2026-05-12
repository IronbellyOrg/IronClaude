# Web Research 02: Incremental Generation Patterns for LLM Pipelines

**Date**: 2026-04-04
**Topic**: Patterns for LLM-based incremental file writing, template-driven generation, multi-turn output pipelines, and structured output enforcement
**Status**: Complete

---

## Research Areas

1. Large structured document generation via LLM pipelines
2. Template-driven generation (section-by-section fill)
3. Multi-turn / tool-use patterns for incremental file writing
4. Output format enforcement techniques

---

## Area 1: Large Structured Document Generation via LLM Pipelines

### Finding 1.1: Break Work Into Small Iterative Chunks (Addy Osmani's LLM Workflow)

**Source**: https://addyosmani.com/blog/ai-coding-workflow/
**Relevance**: HIGH -- directly addresses our problem of monolithic one-shot output

Key pattern: "Avoid asking the AI for large, monolithic outputs. Instead, break the project into iterative steps or tickets and tackle them one by one." The author generates a structured "prompt plan" file containing a sequence of prompts for each task, so tools can execute them one by one.

Core principles:
- LLMs do best with focused prompts: one function, one bug, one feature at a time
- Each chunk is small enough that the AI can handle it within context
- Finish task, run tests, commit -- each chunk ends up as its own commit
- Planning first forces human and AI onto the same page, prevents wasted cycles
- A robust spec/plan is the cornerstone of the workflow

**Relationship to our codebase**: This validates our proposed shift from one-shot `claude --print` to multi-step tool-use generation. The "prompt plan" concept maps directly to our template-driven approach where each section gets its own prompt.

### Finding 1.2: Hierarchical / Structure-Based Chunking Strategies

**Source**: https://weaviate.io/blog/chunking-strategies-for-rag
**Source**: https://www.firecrawl.dev/blog/best-chunking-strategies-rag
**Relevance**: MEDIUM -- applies to how we structure output documents for downstream consumption

Key insight: Document-based chunking where Markdown files are split by headers/subheaders preserves logical structure. "Agentic chunking" takes this further -- an AI agent dynamically decides how to split documents based on structure, density, and content.

For our generation pipeline, the reverse applies: we should GENERATE documents in the same hierarchical structure we'd want to chunk them into. Each section should be a self-contained unit.

### Finding 1.3: LLM-Suggested Chunk Boundaries

**Source**: https://www.firecrawl.dev/blog/best-chunking-strategies-rag
**Relevance**: MEDIUM -- pattern for LLM-aware document structure

Pattern: Send the first N characters of a document to GPT-4 with a system prompt instructing it to analyze document structure and suggest chunk boundaries. The LLM returns section titles with character positions.

**Relationship to our codebase**: We could use a similar pre-pass where the model analyzes the template and plans which sections need the most detail, allowing dynamic allocation of output tokens per section.

---

## Area 2: Template-Driven Generation (Section-by-Section Fill)

### Finding 2.1: Hybrid Template-LLM Generation (iEcoreGen Pattern)

**Source**: https://www.emergentmind.com/topics/template-driven-generators
**Relevance**: HIGH -- directly describes the pattern we want to implement

Key pattern: "Hybridization of template-driven code generation with LLM completion" where correctness-guaranteed template skeletons are paired with docstring specifications, allowing LLMs to fill implementation gaps. This yields higher pass@k rates than LLM-only baselines while retaining full compilation correctness.

Formal taxonomy of template-driven generation:
- Templates are "partially specified output artifacts with static scaffolding and dynamic slots"
- Static scaffolding = the fixed structure (headers, required sections, format)
- Dynamic slots = content the LLM fills in based on context
- Templates intermingle fixed output text with expressions, loops, and conditions

**Relationship to our codebase**: This is precisely our target architecture. The roadmap/tasklist templates define the static scaffolding (section headers, required fields, formatting), and the LLM fills each dynamic slot. The template guarantees structural correctness while the LLM provides content.

### Finding 2.2: Template Pattern for Content Generation

**Source**: https://www.prompthub.us/blog/prompt-engineering-for-content-creation
**Relevance**: HIGH -- practical prompt-level technique

The "Template Pattern": Send a specific template format that you want the LLM to follow when it produces output. Example: provide section headers (Introduction, Key Benefits, Real-World Example, Call to Action) and the model fills each one.

Related pattern -- "Skeleton of Thought Prompting": Creates an outline first, then fills it in, ensuring a continuous information stream. This is a two-pass approach:
1. Pass 1: Generate the skeleton/outline
2. Pass 2: Fill each section in parallel or sequentially

**Relationship to our codebase**: The Skeleton-of-Thought approach maps to a two-phase pipeline: (1) generate outline/plan from spec, (2) fill each section via separate tool-use calls. This naturally solves the token limit problem since each section fill is a bounded output.

### Finding 2.3: Prompt Chaining for Document Generation

**Source**: https://www.taskade.com/blog/what-is-prompt-chaining
**Relevance**: HIGH -- architectural pattern for multi-step generation

Prompt chaining decomposes a large task into sequential subtasks where each prompt builds on the previous output. Key implementation steps:
1. Define the overall objective
2. Decompose into subtasks (the LLM can help with this)
3. Craft prompts for each subtask
4. Each consecutive prompt "recycles" the result from the previous generation
5. Each prompt specifies the expected output format

Critical insight: "If you try to throw all that at the LLM at once, it will hallucinate or lose context. But if you break the task down into compounding steps, the AI will approach the task gradually and build on its own output."

**Relationship to our codebase**: This validates the multi-step pipeline approach. Each roadmap step (extraction, base-selection, debate, etc.) is already a chain. The next level is making each step internally chained -- e.g., the roadmap step generates section by section.

### Finding 2.4: Prefill / Anchor the Output (Skeleton Priming)

**Source**: https://www.lakera.ai/blog/prompt-engineering-guide
**Relevance**: HIGH -- directly applicable technique for Claude

"Prefill or Anchor the Output": Give the model the beginning of the desired output -- a partial structure -- to steer how it completes the rest. LLMs are autocomplete engines; when you control how the answer starts, you reduce randomness, hallucinations, and drift.

Model-specific insight for Claude: "Claude responds reliably to sentence stems (e.g., 'The key finding is...'), but prefers declarative phrasing over open-ended fragments."

**Relationship to our codebase**: For each section fill, we can prefill the assistant message with the section header and any structural prefix. This is directly supported by the Anthropic API's `assistant` prefill feature. For `claude` CLI, we can achieve this by including the template structure in the prompt and instructing the model to continue from a specific point.

### Finding 2.5: Enterprise Prompt Templates as Infrastructure

**Source**: https://www.refontelearning.com/blog/from-templates-to-toolchains-prompt-engineering-trends-2025-explained
**Relevance**: MEDIUM -- validates template-as-code approach

Modern prompt templates in 2025 are:
- Modular: Split into instruction blocks, task logic, formatting, and guardrails
- Dynamic: Integrated with API calls, context retrieval, and user metadata
- Versioned: Managed in Git-like repositories for traceability and rollback
- Multilingual: Designed to handle locale and translation via token substitution

Tools: LangChain PromptTemplates, PromptLayer, Azure OpenAI prompt flows, custom YAML/JSON schemas.

**Relationship to our codebase**: Our template files in `src/superclaude/skills/` already follow this pattern. The key insight is that templates should be first-class versioned artifacts, not just prompt strings.

---

## Area 3: Multi-Turn / Tool-Use Patterns for Incremental File Writing

### Finding 3.1: Claude Code's Agentic Write Pattern

**Source**: https://www.anthropic.com/product/claude-code
**Source**: https://github.com/anthropics/claude-code
**Relevance**: HIGH -- this is the exact tool we use; understanding its internals is critical

Claude Code is an agentic coding system that reads the full codebase, plans an approach across multiple files, executes changes, runs tests, and iterates on failures. The key architectural pattern:
1. Read files to understand context
2. Plan the approach
3. Write/modify code across multiple files simultaneously
4. Run tests and iterate

The Agent Teams feature enables multiple Claude Code instances to work on different parts simultaneously, coordinated by a lead agent.

**Relationship to our codebase**: Our Sprint pipeline already uses this pattern -- `claude` in agentic mode with `--tools default` and `--dangerously-skip-permissions` writes files via tool use. The roadmap pipeline currently does NOT use this pattern (it uses `--print` one-shot mode). The fix is to switch roadmap steps to agentic mode with tool-use file writing.

### Finding 3.2: Advanced Tool Use -- Tool Search, Programmatic Tool Calling

**Source**: https://www.anthropic.com/engineering/advanced-tool-use
**Relevance**: MEDIUM -- shows direction of Anthropic's tool-use capabilities

Three advanced features:
1. **Tool Search Tool**: Claude can search thousands of tools without consuming context window
2. **Programmatic Tool Calling**: Claude invokes tools in a code execution environment, reducing context impact
3. **Tool Use Examples**: Universal standard for demonstrating tool usage

**Relationship to our codebase**: Programmatic tool calling could be relevant for our pipeline -- instead of the model making individual write_file tool calls, it could execute a script that handles the file writing pattern programmatically.

### Finding 3.3: AnythingLLM Write File Block Pattern

**Source**: https://docs.anythingllm.com/agent-flows/blocks/write-file
**Relevance**: MEDIUM -- shows how other agentic frameworks implement file writing

The Write File block allows writing content to a file on the local file system, useful for exporting results, logging, or passing data to other applications. The pattern separates data collection (pre-processing stage with API calls, database queries, CLI tools) from agent reasoning (reading collected files with read_file tool).

**Relationship to our codebase**: This two-stage pattern (collect data -> agent reads and processes) is already used in our pipeline. The missing piece is the second stage: agent writes output incrementally via tool calls rather than one-shot print.

### Finding 3.4: Claude CLI Token Limits and Truncation Behavior

**Source**: https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
**Source**: https://github.com/anthropics/claude-code/issues/14888
**Relevance**: HIGH -- directly explains our truncation problem

Key findings:
- Non-streaming fallback token cap: increased from 21k to 64k, timeout from 120s to 300s
- `--print` mode uses non-streaming fallback which has lower token limits
- Files loaded via @ syntax are silently truncated at 2000 lines
- Environment variable `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK` can help
- Full command output enters the context window

**Relationship to our codebase**: This confirms that `--print` mode has inherent output size limitations. The 64k token cap on non-streaming fallback is the likely cause of our 800+ line truncation. Switching to agentic mode with tool-use file writing completely bypasses this limit since the model writes to files directly rather than outputting to stdout.

### Finding 3.5: Agentic Workflow Patterns (Weaviate)

**Source**: https://weaviate.io/blog/what-are-agentic-workflows
**Relevance**: MEDIUM -- general agentic pattern reference

Agentic workflows decompose complex tasks into subtasks executed by specialized agents. The architecture supports modular tool-based design where the agent binds to a tool schema and forces a single precise tool call per step.

**Relationship to our codebase**: Our pipeline steps are already modular. The key architectural change is making each step internally agentic (tool-use mode) rather than one-shot (print mode).

---

## Area 4: Output Format Enforcement Techniques

### Finding 4.1: Anthropic Structured Outputs (JSON Schema Enforcement)

**Source**: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
**Source**: https://towardsdatascience.com/hands-on-with-anthropics-new-structured-output-capabilities/
**Relevance**: HIGH -- native Anthropic solution for output format enforcement

Anthropic now offers structured outputs via `output_config` parameter with JSON schema:
- Compiles JSON schema into a grammar
- Actively restricts token generation during inference -- the model literally cannot produce tokens that would violate the schema
- Schema is cached for 24 hours
- Guaranteed compliance on the first try -- no retries, no validation loops
- Available for Claude Sonnet 4.5, Opus 4.5, Haiku 4.5

Implementation options:
1. **Pydantic (Python)**: Define schema as Pydantic model, auto-generates JSON Schema
2. **Zod (TypeScript)**: Same pattern for TypeScript
3. **Direct JSON Schema**: Raw schema definition

**Relationship to our codebase**: For structured intermediate outputs (extraction results, base-selection decisions), we could use structured outputs to guarantee valid JSON. However, for large markdown documents (the roadmap itself), structured outputs are less appropriate -- markdown content within JSON fields would still hit token limits.

### Finding 4.2: Constrained Decoding / Grammar-Based Generation

**Source**: https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output
**Source**: https://www.letsdatascience.com/blog/structured-outputs-making-llms-return-reliable-json
**Source**: https://www.aidancooper.co.uk/constrained-decoding/
**Relevance**: MEDIUM -- explains the underlying mechanism

Constrained decoding ensures 100% compliance by masking incompatible tokens during generation. Key frameworks:
- **Outlines**: Open-source, grammar-based constrained decoding
- **Guidance (llguidance)**: Microsoft's library for super-fast structured outputs
- **XGrammar**: CFG-level expressiveness with FSM-level performance, up to 100x speedup over traditional methods
- **vLLM**: Production inference server with built-in structured output support

**Relationship to our codebase**: These are primarily relevant if we self-host models. Since we use the Claude API/CLI, Anthropic's native structured outputs (Finding 4.1) are the appropriate enforcement mechanism. However, understanding constrained decoding helps us reason about what's possible and what the overhead is.

### Finding 4.3: Function Calling as Format Enforcement

**Source**: https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms
**Source**: https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/extracting_structured_json.ipynb
**Relevance**: HIGH -- practical pattern we can use today

Tool/function calling can be used as a format enforcement mechanism: define a tool with a specific schema, and the model's output is constrained to that schema. Anthropic's cookbook shows using tool_use to extract structured JSON from unstructured text.

Pattern for our use case:
1. Define a `write_section` tool with parameters: `section_id`, `section_title`, `content`, `metadata`
2. The model must call this tool for each section, guaranteeing structured output
3. Our code receives structured tool calls and assembles the final document
4. Each tool call is individually bounded (no single call can be too large)

**Relationship to our codebase**: This is the most promising approach for our pipeline. Instead of asking the model to output a complete markdown document, we define tools like `write_section(section_id, content)` and `append_to_section(section_id, content)`. The model calls these tools to build the document incrementally. This naturally:
- Prevents truncation (each tool call is bounded)
- Enforces structure (section_ids must match template)
- Enables progress tracking (each tool call is observable)
- Allows validation (we can reject malformed tool calls)

### Finding 4.4: Prefill/Anchor Technique for Format Enforcement

**Source**: https://www.lakera.ai/blog/prompt-engineering-guide (also cited in Area 2)
**Relevance**: HIGH -- complementary technique for within-section format enforcement

For content within each section, the prefill/anchor technique steers the model. Claude's API supports assistant message prefill -- providing the start of the assistant's response. Combined with tool-use, this means:
1. Tool call constrains the section structure
2. Prefill within the prompt constrains the content format within each section
3. System prompt constrains overall style and quality

This layered enforcement (structural + content + style) provides comprehensive format control.

---

## Supplementary: Long Document Generation Benchmarks

### Finding S.1: ICLR 2025 Long-Form Generation Benchmarks

**Source**: https://proceedings.iclr.cc/paper_files/paper/2025/file/141304a37d59ec7f116f3535f1b74bde-Paper-Conference.pdf
**Relevance**: MEDIUM -- academic validation of the chunked-generation approach

Academic research from ICLR 2025 confirms that even large-context LLMs struggle with long-form generation quality. The solution across all high-performing systems is staged/iterative generation rather than single-pass output.

### Finding S.2: Iterative Summarization Pattern (MetroStar)

**Source**: https://blog.metrostar.com/iteratively-summarize-long-documents-llm
**Relevance**: MEDIUM -- demonstrates iterative processing of long documents

Pattern: Break documents into fixed-size chunks, process each chunk, combine outputs, repeat until final output meets quality/length thresholds. Each stage reuses outputs from the previous one, making the pipeline modular, traceable, and cost-efficient.

**Relationship to our codebase**: Our pipeline already follows this general pattern across steps (extraction -> base-selection -> debate -> roadmap). The needed improvement is applying the same iterative pattern WITHIN each step.

---

## Key External Findings

### F1: The One-Shot Output Problem Is Well-Understood
The industry consensus (Addy Osmani, multiple framework authors, ICLR 2025 research) is that large monolithic LLM outputs fail. The universal solution is decomposition into smaller, bounded generation tasks. Our truncation problem with `claude --print` is a known limitation of non-streaming/one-shot modes.

### F2: Template-Driven Hybrid Generation Is a Proven Pattern
The iEcoreGen model (template skeleton + LLM fill) is formally validated in software engineering research. Templates provide correctness-guaranteed structure; LLMs provide content. This hybrid produces higher quality than LLM-only generation.

### F3: Tool-Use File Writing Is the Standard Agentic Pattern
Claude Code, AnythingLLM, LangChain agents, and other frameworks all use tool-based file writing as their core output mechanism. The model calls `write_file` / `edit_file` tools rather than printing to stdout. This naturally handles arbitrarily long outputs.

### F4: Anthropic's Structured Outputs Can Enforce Intermediate Formats
For structured intermediate data (JSON extraction results, decision records), Anthropic's `output_config` with JSON schema provides grammar-level enforcement. For large markdown content, tool-use with defined schemas is more appropriate.

### F5: Layered Enforcement Is Most Effective
Best results combine multiple enforcement layers:
1. **Structural**: Tool schemas constrain section structure
2. **Content**: Prefill/anchor constrains within-section format
3. **Semantic**: System prompts constrain quality and style
4. **Validation**: Post-generation checks catch remaining issues

### F6: The `--print` Mode Token Cap Is the Root Cause
Non-streaming fallback in Claude CLI caps at 64k tokens with a 300s timeout. This directly explains our truncation at 800+ lines. Switching to agentic mode with tool-use bypasses this entirely.

---

## Recommendations for Our Architecture

### R1: Switch Pipeline Steps from `--print` to Agentic Tool-Use Mode
**Priority**: CRITICAL
**Effort**: Medium

Replace `claude --print` invocations with `claude` in agentic mode (already used by Sprint). Each pipeline step should write its output via tool-use file operations rather than stdout capture. This immediately solves the truncation problem.

### R2: Implement Template-Driven Section-by-Section Generation
**Priority**: HIGH
**Effort**: Medium-High

For each pipeline step that produces structured output (roadmap, tasklist, extraction):
1. Define a markdown template with section headers and required fields
2. Prompt the model to fill each section via `write_section` tool calls
3. Assemble the final document from the ordered section outputs
4. Validate each section meets minimum content requirements

### R3: Use Structured Outputs for Intermediate JSON Artifacts
**Priority**: MEDIUM
**Effort**: Low

For pipeline steps that produce structured data (extraction.json, base-selection.json, wiring-verification.json), use Anthropic's `output_config` with JSON schema to guarantee valid structured output without retry loops.

### R4: Implement Two-Phase Generation (Plan Then Fill)
**Priority**: MEDIUM
**Effort**: Medium

Adopt the Skeleton-of-Thought pattern:
- Phase 1: Model generates an outline/plan for the document (bounded output)
- Phase 2: Model fills each planned section (bounded per-section output)

This provides an observable checkpoint between planning and execution, allows human review of the plan, and distributes token budget across sections.

### R5: Add Post-Generation Validation Layer
**Priority**: LOW (can be added incrementally)
**Effort**: Low

After document assembly, run a validation pass:
- Check all required sections are present
- Verify minimum content lengths per section
- Validate cross-references and internal consistency
- Flag sections that appear truncated or incomplete

---

## Source Index

| # | URL | Area | Relevance |
|---|-----|------|-----------|
| 1 | https://addyosmani.com/blog/ai-coding-workflow/ | 1 | HIGH |
| 2 | https://weaviate.io/blog/chunking-strategies-for-rag | 1 | MEDIUM |
| 3 | https://www.firecrawl.dev/blog/best-chunking-strategies-rag | 1 | MEDIUM |
| 4 | https://www.emergentmind.com/topics/template-driven-generators | 2 | HIGH |
| 5 | https://www.prompthub.us/blog/prompt-engineering-for-content-creation | 2 | HIGH |
| 6 | https://www.taskade.com/blog/what-is-prompt-chaining | 2 | HIGH |
| 7 | https://www.lakera.ai/blog/prompt-engineering-guide | 2,4 | HIGH |
| 8 | https://www.refontelearning.com/blog/from-templates-to-toolchains-prompt-engineering-trends-2025-explained | 2 | MEDIUM |
| 9 | https://www.anthropic.com/product/claude-code | 3 | HIGH |
| 10 | https://github.com/anthropics/claude-code | 3 | HIGH |
| 11 | https://www.anthropic.com/engineering/advanced-tool-use | 3 | MEDIUM |
| 12 | https://docs.anythingllm.com/agent-flows/blocks/write-file | 3 | MEDIUM |
| 13 | https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work | 3 | HIGH |
| 14 | https://weaviate.io/blog/what-are-agentic-workflows | 3 | MEDIUM |
| 15 | https://platform.claude.com/docs/en/build-with-claude/structured-outputs | 4 | HIGH |
| 16 | https://towardsdatascience.com/hands-on-with-anthropics-new-structured-output-capabilities/ | 4 | HIGH |
| 17 | https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output | 4 | MEDIUM |
| 18 | https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms | 4 | HIGH |
| 19 | https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/extracting_structured_json.ipynb | 4 | HIGH |
| 20 | https://proceedings.iclr.cc/paper_files/paper/2025/file/141304a37d59ec7f116f3535f1b74bde-Paper-Conference.pdf | S | MEDIUM |
| 21 | https://blog.metrostar.com/iteratively-summarize-long-documents-llm | S | MEDIUM |
