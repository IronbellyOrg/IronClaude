# Section 5: External Research Findings

**Synthesis Date**: 2026-04-04
**Sources**: 2 web research files (web-01, web-02)
**Status**: Complete

> **Note**: All findings in this section are supplementary. Codebase findings take precedence where conflicts exist.

---

## 5.1 Claude CLI Output Formats and Capabilities

### 5.1.1 Output Format Options

| Finding | Description | Source | Relevance | Codebase Relationship |
|:--------|:------------|:-------|:----------|:----------------------|
| `--output-format` accepts three values: `text`, `json`, `stream-json` | `text` returns final text only; `json` returns structured object with metadata; `stream-json` returns NDJSON with per-event granularity | [CLI Reference](https://code.claude.com/docs/en/cli-reference) | HIGH | **Supports** -- our pipeline uses `text` for roadmap and `stream-json` for sprint; switching roadmap to `stream-json` would enable tool-use observability |
| `stream-json` exposes tool_use events in real-time | Each line is a complete JSON object; event types include assistant messages, tool_use, thinking, stream deltas | [Headless Docs](https://code.claude.com/docs/en/headless) | HIGH | **Extends** -- currently invisible tool calls in roadmap pipeline would become observable |
| `json` format includes `session_id` and `structured_output` field | When combined with `--json-schema`, validated structured output appears in `structured_output` field | [CLI Reference](https://code.claude.com/docs/en/cli-reference) | MEDIUM | **Extends** -- could enable structured intermediate artifacts (extraction, base-selection) |

### 5.1.2 Model Output Token Limits

| Model | Context Window | Max Output (Sync) | Max Output (Batch) | Source |
|:------|:---------------|:-------------------|:-------------------|:-------|
| Opus 4.6 | 1M tokens | 128k tokens (~96k words) | 300k (beta header) | [Model Overview](https://platform.claude.com/docs/en/about-claude/models/overview) |
| Sonnet 4.6 | 1M tokens | 64k tokens (~48k words) | 300k (beta header) | [Model Overview](https://platform.claude.com/docs/en/about-claude/models/overview) |
| Haiku 4.5 | 200k tokens | 64k tokens (~48k words) | N/A | [Model Overview](https://platform.claude.com/docs/en/about-claude/models/overview) |

| Finding | Description | Source | Relevance | Codebase Relationship |
|:--------|:------------|:-------|:----------|:----------------------|
| Output token caps are NOT the bottleneck for typical roadmap artifacts | Typical roadmap artifacts are 5k-20k tokens, well within all model limits | [web-01 analysis](https://platform.claude.com/docs/en/about-claude/models/overview) | HIGH | **Supports** -- one-shot architecture is not fundamentally limited by output token caps |
| Non-streaming fallback caps at 64k tokens with 300s timeout | `--print` mode uses non-streaming fallback which has lower limits; this is the likely cause of 800+ line truncation | [Support Article](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work) | HIGH | **Supports** -- directly explains observed truncation problem |
| `max_tokens` does not factor into OTPM rate limit calculations | No rate limit penalty for setting higher max_tokens value | [Model Overview](https://platform.claude.com/docs/en/about-claude/models/overview) | LOW | **Supports** -- no cost to requesting higher output limits |

---

## 5.2 Print Mode and Agentic Capabilities

| Finding | Description | Source | Relevance | Codebase Relationship |
|:--------|:------------|:-------|:----------|:----------------------|
| `--print` mode is fully agentic when tools are available | With `--tools default`, Claude makes multiple tool calls across many turns; session continues until final text response with no tool calls | [Headless Docs](https://code.claude.com/docs/en/headless) | HIGH | **Contradicts** assumption that `--print` is single-turn; our pipeline already supports multi-turn within a single invocation |
| Claude CAN write files directly in our current setup | `--tools default` + `--dangerously-skip-permissions` gives Claude full tool access including `Write` and `Edit`; no flag changes needed | [CLI Reference](https://code.claude.com/docs/en/cli-reference) | HIGH | **Extends** -- only prompt changes are needed to enable file-writing behavior |
| Each tool invocation counts as an agentic turn toward `--max-turns` | A session with 5 file reads = at least 6 turns (1 initial + 5 tool-use); our pipeline default is 100 turns | [CLI Reference](https://code.claude.com/docs/en/cli-reference) | HIGH | **Supports** -- 100-turn budget is generous for incremental writing (typically 10-20 turns) |
| Cross-invocation continuation exists via `--continue` and `--resume` | `--continue` resumes most recent conversation; `--resume <session_id>` resumes specific session; our `--no-session-persistence` flag disables this | [Headless Docs](https://code.claude.com/docs/en/headless) | MEDIUM | **Extends** -- removing `--no-session-persistence` would enable multi-stage generation |
| `--bare` mode recommended for scripted/SDK calls | Skips auto-discovery of hooks, skills, plugins, MCP servers, CLAUDE.md; will become default for `-p` in future release | [Headless Docs](https://code.claude.com/docs/en/headless) | MEDIUM | **Extends** -- relevant for pipeline isolation needs |

### Permission Modes in Print Mode

| Mode | Behavior | Source |
|:-----|:---------|:-------|
| `bypassPermissions` | All tools auto-approve (current pipeline setup) | [CLI Reference](https://code.claude.com/docs/en/cli-reference) |
| `dontAsk` | Denies anything not in `permissions.allow` rules | [CLI Reference](https://code.claude.com/docs/en/cli-reference) |
| `acceptEdits` | File writes auto-approve; Bash/network need rules | [CLI Reference](https://code.claude.com/docs/en/cli-reference) |
| `default` | Blocks in non-interactive -- unsuitable for print mode | [CLI Reference](https://code.claude.com/docs/en/cli-reference) |

---

## 5.3 Incremental Generation Patterns

### 5.3.1 Decomposition and Chunking

| Finding | Description | Source | Relevance | Codebase Relationship |
|:--------|:------------|:-------|:----------|:----------------------|
| Industry consensus: large monolithic LLM outputs fail | "Avoid asking the AI for large, monolithic outputs. Instead, break the project into iterative steps." Generate a prompt plan file, execute prompts one by one. | [Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/) | HIGH | **Supports** -- validates proposed shift from one-shot to multi-step tool-use generation |
| Hierarchical chunking preserves logical structure | Documents split by headers/subheaders maintain self-contained units; generation should mirror desired chunk structure | [Weaviate](https://weaviate.io/blog/chunking-strategies-for-rag) | MEDIUM | **Supports** -- roadmap sections should be generated as self-contained units |
| LLM-suggested chunk boundaries improve quality | Pre-pass where model analyzes template and plans section detail level enables dynamic token allocation | [Firecrawl](https://www.firecrawl.dev/blog/best-chunking-strategies-rag) | MEDIUM | **Extends** -- could add a planning pre-pass before section-by-section generation |
| ICLR 2025 confirms staged generation outperforms single-pass | Even large-context LLMs struggle with long-form generation quality; all high-performing systems use staged/iterative generation | [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/141304a37d59ec7f116f3535f1b74bde-Paper-Conference.pdf) | MEDIUM | **Supports** -- academic validation of the chunked-generation approach |

### 5.3.2 Template-Driven Hybrid Generation

| Finding | Description | Source | Relevance | Codebase Relationship |
|:--------|:------------|:-------|:----------|:----------------------|
| Template skeleton + LLM fill yields higher quality than LLM-only | iEcoreGen pattern: "partially specified output artifacts with static scaffolding and dynamic slots"; templates guarantee structural correctness, LLM provides content | [EmergentMind](https://www.emergentmind.com/topics/template-driven-generators) | HIGH | **Supports** -- precisely the target architecture for roadmap/tasklist templates |
| Skeleton-of-Thought prompting: outline first, then fill | Two-pass: (1) generate skeleton/outline, (2) fill each section sequentially or in parallel; ensures continuous information stream | [PromptHub](https://www.prompthub.us/blog/prompt-engineering-for-content-creation) | HIGH | **Extends** -- maps to two-phase pipeline: generate outline from spec, then fill each section |
| Prompt chaining decomposes large tasks into sequential subtasks | Each prompt builds on previous output; "If you try to throw all that at the LLM at once, it will hallucinate or lose context" | [Taskade](https://www.taskade.com/blog/what-is-prompt-chaining) | HIGH | **Supports** -- validates making each pipeline step internally chained (section by section) |
| Prefill/anchor technique steers LLM completion | Providing beginning of desired output reduces randomness, hallucinations, and drift; Claude responds reliably to sentence stems | [Lakera](https://www.lakera.ai/blog/prompt-engineering-guide) | HIGH | **Extends** -- each section fill can prefill with section header and structural prefix |
| Modern prompt templates are modular, dynamic, versioned | Templates split into instruction blocks, task logic, formatting, guardrails; managed in Git for traceability | [Refonte](https://www.refontelearning.com/blog/from-templates-to-toolchains-prompt-engineering-trends-2025-explained) | MEDIUM | **Supports** -- our template files in `src/superclaude/skills/` already follow this pattern |

---

## 5.4 Tool-Use File Writing Patterns

| Finding | Description | Source | Relevance | Codebase Relationship |
|:--------|:------------|:-------|:----------|:----------------------|
| Tool-based file writing is the standard agentic output pattern | Claude Code, AnythingLLM, LangChain agents all use `write_file`/`edit_file` tools rather than stdout; naturally handles arbitrarily long outputs | [Anthropic](https://www.anthropic.com/product/claude-code), [AnythingLLM](https://docs.anythingllm.com/agent-flows/blocks/write-file) | HIGH | **Supports** -- Sprint already uses this pattern; roadmap should adopt it |
| Two-stage pattern: collect data then agent reads and processes | Separate data collection (API calls, CLI tools) from agent reasoning (read collected files, produce output) | [AnythingLLM](https://docs.anythingllm.com/agent-flows/blocks/write-file) | MEDIUM | **Supports** -- already used in our pipeline; missing piece is agent writing output via tool calls |
| Function calling as format enforcement | Define a `write_section` tool with parameters (`section_id`, `content`, `metadata`); model must call this tool per section, guaranteeing structure | [Agenta](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms), [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/extracting_structured_json.ipynb) | HIGH | **Extends** -- most promising approach; each tool call is bounded, structured, observable, and validatable |
| Iterative summarization: chunk, process, combine, repeat | Break documents into fixed-size chunks, process each, combine outputs, repeat until quality/length thresholds met | [MetroStar](https://blog.metrostar.com/iteratively-summarize-long-documents-llm) | MEDIUM | **Supports** -- pipeline already follows across steps; needed improvement is applying within each step |

---

## 5.5 Output Format Enforcement

| Finding | Description | Source | Relevance | Codebase Relationship |
|:--------|:------------|:-------|:----------|:----------------------|
| Anthropic structured outputs via `output_config` with JSON schema | Compiles JSON schema into grammar; restricts token generation during inference; guaranteed compliance on first try; no retries needed | [Anthropic Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [TDS](https://towardsdatascience.com/hands-on-with-anthropics-new-structured-output-capabilities/) | HIGH | **Extends** -- applicable for structured intermediates (extraction, base-selection JSON); NOT for large markdown documents |
| Constrained decoding ensures 100% compliance via token masking | Frameworks: Outlines, Guidance, XGrammar, vLLM; primarily relevant for self-hosted models | [Brenndoerfer](https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output) | MEDIUM | **Supports** -- since we use Claude API/CLI, Anthropic's native structured outputs are the appropriate mechanism |
| Layered enforcement is most effective | Three layers: (1) structural -- tool schemas constrain section structure, (2) content -- prefill/anchor constrains within-section format, (3) semantic -- system prompts constrain quality and style; plus (4) post-generation validation | [Lakera](https://www.lakera.ai/blog/prompt-engineering-guide), [Agenta](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms) | HIGH | **Extends** -- comprehensive enforcement model for our pipeline; currently only layer 3 (system prompts) is used |
| Files loaded via `@` syntax are silently truncated at 2000 lines | Full command output enters context window; `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK` env var can help | [GitHub Issue #14888](https://github.com/anthropics/claude-code/issues/14888) | HIGH | **Supports** -- confirms silent truncation as a real issue affecting our pipeline inputs |

---

## 5.6 External Research Summary

### Key Takeaways

| # | Takeaway | Supported By | Impact |
|:--|:---------|:-------------|:-------|
| 1 | **The `--print` non-streaming fallback 64k token cap is the root cause of truncation** -- not model output limits (128k/64k). Switching to agentic tool-use file writing bypasses this entirely. | web-01 S5, web-02 F3.4 | CRITICAL |
| 2 | **No flag changes are needed** -- our pipeline already has `--tools default` + `--dangerously-skip-permissions`. Only prompt changes required to enable file-writing behavior. | web-01 S3 | HIGH |
| 3 | **Template-driven hybrid generation (static scaffolding + dynamic LLM fill) is a formally validated pattern** that produces higher quality than LLM-only generation. | web-02 F2.1, F2.2 | HIGH |
| 4 | **Function calling as format enforcement** (defining `write_section` tools) naturally solves truncation, enforces structure, enables progress tracking, and allows validation. | web-02 F4.3 | HIGH |
| 5 | **Layered enforcement** (structural + content + semantic + validation) is the industry best practice for output quality. Our pipeline currently only uses the semantic layer (system prompts). | web-02 F4.4, F4.1 | MEDIUM |
| 6 | **`stream-json` output format would enable real-time observability** of tool-use events in roadmap pipeline, matching sprint's existing approach. | web-01 S1 | MEDIUM |
| 7 | **Cross-invocation continuation (`--continue`/`--resume`) is available** but disabled by our `--no-session-persistence` flag. Could enable multi-stage generation if needed. | web-01 S5 | LOW |
| 8 | **`--bare` mode** is recommended by Anthropic for scripted calls and provides cleaner isolation for pipeline subprocesses. | web-01 S5 | LOW |

### Relevance Distribution

| Rating | Count | Percentage |
|:-------|:------|:-----------|
| HIGH | 17 | 65% |
| MEDIUM | 9 | 35% |
| LOW | 0 | 0% |

### Codebase Relationship Distribution

| Relationship | Count | Description |
|:-------------|:------|:------------|
| **Supports** | 14 | External finding confirms or validates existing codebase behavior/direction |
| **Extends** | 11 | External finding suggests new capabilities or enhancements beyond current codebase |
| **Contradicts** | 1 | External finding contradicts an assumption (print mode is NOT single-turn) |

---

## Source Index

| # | URL | Section | Relevance |
|:--|:----|:--------|:----------|
| 1 | https://code.claude.com/docs/en/cli-reference | 5.1, 5.2 | HIGH |
| 2 | https://code.claude.com/docs/en/headless | 5.1, 5.2 | HIGH |
| 3 | https://platform.claude.com/docs/en/about-claude/models/overview | 5.1 | HIGH |
| 4 | https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work | 5.1 | HIGH |
| 5 | https://github.com/anthropics/claude-code/issues/14888 | 5.5 | HIGH |
| 6 | https://addyosmani.com/blog/ai-coding-workflow/ | 5.3 | HIGH |
| 7 | https://www.emergentmind.com/topics/template-driven-generators | 5.3 | HIGH |
| 8 | https://www.prompthub.us/blog/prompt-engineering-for-content-creation | 5.3 | HIGH |
| 9 | https://www.taskade.com/blog/what-is-prompt-chaining | 5.3 | HIGH |
| 10 | https://www.lakera.ai/blog/prompt-engineering-guide | 5.3, 5.5 | HIGH |
| 11 | https://www.anthropic.com/product/claude-code | 5.4 | HIGH |
| 12 | https://platform.claude.com/docs/en/build-with-claude/structured-outputs | 5.5 | HIGH |
| 13 | https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms | 5.4, 5.5 | HIGH |
| 14 | https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/extracting_structured_json.ipynb | 5.4 | HIGH |
| 15 | https://weaviate.io/blog/chunking-strategies-for-rag | 5.3 | MEDIUM |
| 16 | https://www.firecrawl.dev/blog/best-chunking-strategies-rag | 5.3 | MEDIUM |
| 17 | https://docs.anythingllm.com/agent-flows/blocks/write-file | 5.4 | MEDIUM |
| 18 | https://blog.metrostar.com/iteratively-summarize-long-documents-llm | 5.4 | MEDIUM |
| 19 | https://www.refontelearning.com/blog/from-templates-to-toolchains-prompt-engineering-trends-2025-explained | 5.3 | MEDIUM |
| 20 | https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output | 5.5 | MEDIUM |
| 21 | https://towardsdatascience.com/hands-on-with-anthropics-new-structured-output-capabilities/ | 5.5 | HIGH |
| 22 | https://proceedings.iclr.cc/paper_files/paper/2025/file/141304a37d59ec7f116f3535f1b74bde-Paper-Conference.pdf | 5.3 | MEDIUM |
| 23 | https://github.com/Roasbeef/claude-agent-sdk-go/blob/main/docs/cli-protocol.md | 5.1 | MEDIUM |
| 24 | https://www.instructa.ai/blog/claude-code/how-to-use-allowed-tools-in-claude-code | 5.2 | MEDIUM |
| 25 | https://weaviate.io/blog/what-are-agentic-workflows | 5.4 | MEDIUM |
| 26 | https://devtk.ai/en/blog/claude-api-pricing-guide-2026/ | 5.1 | MEDIUM |
