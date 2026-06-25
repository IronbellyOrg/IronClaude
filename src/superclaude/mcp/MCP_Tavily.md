# Tavily MCP Server

**Purpose**: Web search and real-time information retrieval for research and current events

**Version**: `tavily-mcp@0.2.20` (pinned — see the `install_mcp.py` registry). This file is the
canonical Tavily capability reference; other docs point here rather than restating the surface.

## Triggers

- Web search requirements beyond Claude's knowledge cutoff
- Current events, news, and real-time information needs
- Market research and competitive analysis tasks
- Technical documentation not in training data
- Academic research requiring recent publications
- Fact-checking and verification needs
- Deep research investigations requiring multi-source analysis
- `/sc:research` command activation

## Choose When

- **Over WebSearch**: When you need structured search with advanced filtering
- **Over WebFetch**: When you need multi-source search, not single page extraction
- **For research**: Comprehensive investigations requiring multiple sources
- **For current info**: Events, updates, or changes after knowledge cutoff
- **Not for**: Simple questions answerable from training, code generation, local file operations

## Works Best With

- **Sequential**: Tavily provides raw information → Sequential analyzes and synthesizes
- **Playwright**: Tavily discovers URLs → Playwright extracts complex content
- **Context7**: Tavily searches for updates → Context7 provides stable documentation
- **Serena**: Tavily performs searches → Serena stores research sessions

## Configuration

Requires TAVILY_API_KEY environment variable from <https://app.tavily.com>

## Tool Surface (Tavily MCP 0.2.x)

The 0.2.x server exposes four tools:

| Tool id | Operation | Notes |
|---------|-----------|-------|
| `mcp__tavily__tavily-search` | Web/news search with ranking + filtering | primary search |
| `mcp__tavily__tavily-extract` | Full-text extraction from one or more URLs | page content |
| `mcp__tavily__tavily-map` | Site-structure discovery (URL graph of a domain) | research engine only |
| `mcp__tavily__tavily-crawl` | Deep domain traversal across linked pages | research engine only |

### Parameters

| Param | Values | Applies to |
|-------|--------|-----------|
| `search_depth` | `basic` \| `advanced` | search |
| `extract_depth` | `basic` \| `advanced` | extract |
| `topic` | `general` \| `news` | search |
| `time_range` | `day` \| `week` \| `month` \| `year` | search |
| `days` | integer (with `topic: news`) | search |
| `include_domains` / `exclude_domains` | list of domains | search / map / crawl |
| `max_results` | integer | search |

### DEFAULT_PARAMETERS (server-level baseline)

The server is installed with a server-level `DEFAULT_PARAMETERS` env var carrying the baseline
`{"search_depth":"basic","max_results":10}`, injected at install time (the canonical value lives
in the `install_mcp.py` registry — it is not restated elsewhere). Every Tavily call inherits this
baseline unless a per-call tool argument overrides it.

### Per-call override (X3 exception — M4, intentional)

Per-call tool arguments override the server-level `DEFAULT_PARAMETERS`. This is a deliberate,
mechanically-valid divergence, not a drift to be "corrected":

- The `/sc:troubleshoot` Tier-2 focused query passes `search_depth: advanced` as a per-call
  argument, overriding the server baseline `basic` for that one rate-limited query (≤2 queries) —
  only hard cases reach Tier-2, so the cost is bounded.
- The deep-research engine raises `search_depth` / `extract_depth` to `advanced` at the deep and
  exhaustive Depth Profiles (see RESEARCH_CONFIG.md).

These overrides are the documented exception to the `basic` baseline and MUST NOT be normalized
back to `basic`.

## Search Capabilities

- **Web Search**: General web searches with ranking algorithms
- **News Search**: Time-filtered news and current events
- **Academic Search**: Scholarly articles and research papers
- **Domain Filtering**: Include/exclude specific domains
- **Content Extraction**: Full-text extraction from search results
- **Freshness Control**: Prioritize recent content
- **Multi-Round Searching**: Iterative refinement based on gaps

## Examples

```text
"latest TypeScript features 2024" → Tavily (current technical information)
"OpenAI GPT updates this week" → Tavily (recent news and updates)
"quantum computing breakthroughs 2024" → Tavily (recent research)
"best practices React Server Components" → Tavily (current best practices)
"explain recursion" → Native Claude (general concept explanation)
"write a Python function" → Native Claude (code generation)
```

## Search Patterns

### Basic Search

```text
Query: "search term"
→ Returns: Ranked results with snippets
```

### Domain-Specific Search  

```text
Query: "search term"
Domains: ["arxiv.org", "github.com"]
→ Returns: Results from specified domains only
```

### Time-Filtered Search

```text
Query: "search term"
Recency: "week" | "month" | "year"
→ Returns: Recent results within timeframe
```

### Deep Content Search

```text
Query: "search term"
Extract: true
→ Returns: Full content extraction from top results
```

## Quality Optimization

- **Query Refinement**: Iterate searches based on initial results
- **Source Diversity**: Ensure multiple perspectives in results
- **Credibility Filtering**: Prioritize authoritative sources
- **Deduplication**: Remove redundant information across sources
- **Relevance Scoring**: Focus on most pertinent results

## Integration Flows

### Research Flow

```text
1. Tavily: Initial broad search
2. Sequential: Analyze and identify gaps
3. Tavily: Targeted follow-up searches
4. Sequential: Synthesize findings
5. Serena: Store research session
```

### Fact-Checking Flow

```text
1. Tavily: Search for claim verification
2. Tavily: Find contradicting sources
3. Sequential: Analyze evidence
4. Report: Present balanced findings
```

### Competitive Analysis Flow

```text
1. Tavily: Search competitor information
2. Tavily: Search market trends
3. Sequential: Comparative analysis
4. Context7: Technical comparisons
5. Report: Strategic insights
```

### Deep Research Flow (DR Agent)

```text
1. Planning: Decompose research question
2. Tavily: Execute planned searches
3. Analysis: Assess URL complexity
4. Routing: Simple → Tavily extract | Complex → Playwright
5. Synthesis: Combine all sources
6. Iteration: Refine based on gaps
```

## Advanced Search Strategies

### Multi-Hop Research

```yaml
Initial_Search:
  query: "core topic"
  depth: broad
  
Follow_Up_1:
  query: "entities from initial"
  depth: targeted
  
Follow_Up_2:
  query: "relationships discovered"
  depth: deep
  
Synthesis:
  combine: all_findings
  resolve: contradictions
```

### Adaptive Query Generation

```yaml
Simple_Query:
  - Direct search terms
  - Single concept focus
  
Complex_Query:
  - Multiple search variations
  - Boolean operators
  - Domain restrictions
  - Time filters
  
Iterative_Query:
  - Start broad
  - Refine based on results
  - Target specific gaps
```

### Source Credibility Assessment

```yaml
High_Credibility:
  - Academic institutions
  - Government sources
  - Established media
  - Official documentation
  
Medium_Credibility:
  - Industry publications
  - Expert blogs
  - Community resources
  
Low_Credibility:
  - User forums
  - Social media
  - Unverified sources
```

## Performance Considerations

### Search Optimization

- Batch similar searches together
- Cache search results for reuse
- Prioritize high-value sources
- Limit depth based on confidence

### Rate Limiting

- Maximum searches per minute
- Token usage per search
- Result caching duration
- Parallel search limits

### Cost Management

- Monitor API usage
- Set budget limits
- Optimize query efficiency
- Use caching effectively

## Integration with DR Agent Architecture

### Planning Strategy Support

```yaml
Planning_Only:
  - Direct query execution
  - No refinement needed
  
Intent_Planning:
  - Clarify search intent
  - Generate focused queries
  
Unified:
  - Present search plan
  - Adjust based on feedback
```

### Multi-Hop Execution

```yaml
Hop_Management:
  - Track search genealogy
  - Build on previous results
  - Detect circular references
  - Maintain hop context
```

### Self-Reflection Integration

```yaml
Quality_Check:
  - Assess result relevance
  - Identify coverage gaps
  - Trigger additional searches
  - Calculate confidence scores
```

### Case-Based Learning

```yaml
Pattern_Storage:
  - Successful query formulations
  - Effective search strategies
  - Domain preferences
  - Time filter patterns
```

## Error Handling

### Common Issues

- API key not configured
- Rate limit exceeded
- Network timeout
- No results found
- Invalid query format

### Fallback Strategies

- Use native WebSearch
- Try alternative queries
- Expand search scope
- Use cached results
- Simplify search terms

## Best Practices

### Query Formulation

1. Start with clear, specific terms
2. Use quotes for exact phrases
3. Include relevant keywords
4. Specify time ranges when needed
5. Use domain filters strategically

### Result Processing

1. Verify source credibility
2. Cross-reference multiple sources
3. Check publication dates
4. Identify potential biases
5. Extract key information

### Integration Workflow

1. Plan search strategy
2. Execute initial searches
3. Analyze results
4. Identify gaps
5. Refine and iterate
6. Synthesize findings
7. Store valuable patterns
