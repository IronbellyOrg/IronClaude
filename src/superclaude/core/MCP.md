# MCP.md - SuperClaude MCP Server Reference

MCP (Model Context Protocol) server integration and orchestration system for Claude Code SuperClaude framework.

## Server Selection Algorithm

**Priority Matrix**:

1. Task-Server Affinity: Match tasks to optimal servers based on capability matrix
2. Performance Metrics: Server response time, success rate, resource utilization
3. Context Awareness: Current persona, command depth, session state
4. Load Distribution: Prevent server overload through intelligent queuing
5. Fallback Readiness: Maintain backup servers for critical operations

**Selection Process**: Task Analysis → Server Capability Match → Performance Check → Load Assessment → Final Selection

## Context7 Integration (Documentation & Research)

**Purpose**: Official library documentation, code examples, best practices, localization standards

**Activation Patterns**:

- Automatic: External library imports detected, framework-specific questions, scribe persona active
- Manual: `--c7`, `--context7` flags
- Smart: Commands detect need for official documentation patterns

**Workflow Process**:

1. Library Detection: Scan imports, dependencies, package.json for library references
2. ID Resolution: Use `resolve-library-id` to find Context7-compatible library ID
3. Documentation Retrieval: Call `get-library-docs` with specific topic focus
4. Pattern Extraction: Extract relevant code patterns and implementation examples
5. Implementation: Apply patterns with proper attribution and version compatibility
6. Validation: Verify implementation against official documentation
7. Caching: Store successful patterns for session reuse

**Integration Commands**: `/build`, `/analyze`, `/improve`, `/design`, `/document`, `/explain`, `/git`

**Error Recovery**:

- Library not found → WebSearch for alternatives → Manual implementation
- Documentation timeout → Use cached knowledge → Note limitations
- Invalid library ID → Retry with broader search terms → Fallback to WebSearch
- Version mismatch → Find compatible version → Suggest upgrade path
- Server unavailable → Activate backup Context7 instances → Graceful degradation

## Playwright Integration (Browser Automation & Testing)

**Purpose**: Cross-browser E2E testing, performance monitoring, automation, visual testing

**Activation Patterns**:

- Automatic: Testing workflows, performance monitoring requests, E2E test generation
- Manual: `--play`, `--playwright` flags
- Smart: QA persona active, browser interaction needed

**Workflow Process**:

1. Browser Connection: Connect to Chrome, Firefox, Safari, or Edge instances
2. Environment Setup: Configure viewport, user agent, network conditions, device emulation
3. Navigation: Navigate to target URLs with proper waiting and error handling
4. Server Coordination: Sync with Context7 for documentation, Serena for code insight
5. Interaction: Perform user actions (clicks, form fills, navigation) across browsers
6. Data Collection: Capture screenshots, videos, performance metrics, console logs
7. Validation: Verify expected behaviors, visual states, and performance thresholds
8. Multi-Server Analysis: Coordinate with other servers for comprehensive test analysis
9. Reporting: Generate test reports with evidence, metrics, and actionable insights
10. Cleanup: Properly close browser connections and clean up resources

**Capabilities**:

- Multi-Browser Support: Chrome, Firefox, Safari, Edge with consistent API
- Visual Testing: Screenshot capture, visual regression detection, responsive testing
- Performance Metrics: Load times, rendering performance, resource usage, Core Web Vitals
- User Simulation: Real user interaction patterns, accessibility testing, form workflows
- Data Extraction: DOM content, API responses, console logs, network monitoring
- Mobile Testing: Device emulation, touch gestures, mobile-specific validation
- Parallel Execution: Run tests across multiple browsers simultaneously

**Integration Patterns**:

- Test Generation: Create E2E tests based on user workflows and critical paths
- Performance Monitoring: Continuous performance measurement with threshold alerting
- Visual Validation: Screenshot-based testing and regression detection
- Cross-Browser Testing: Validate functionality across all major browsers
- User Experience Testing: Accessibility validation, usability testing, conversion optimization

## Auggie MCP Integration (Codebase Intelligence)

**Purpose**: Semantic codebase retrieval, project structure understanding, code-aware context loading

**Activation Patterns**:

- Automatic: Code-related brainstorm topics, task execution (STRICT/STANDARD tiers), implementation planning
- Manual: `--auggie` flag
- Smart: Commands detect need for codebase awareness before code-related operations

**Workflow Process**:

1. Topic Analysis: Determine if codebase context would be valuable for the current operation
2. Query Formulation: Create natural language queries from task/topic context
3. Retrieval: Call `codebase-retrieval` with project `directory_path` (current working directory)
4. Context Synthesis: Extract relevant findings into structured briefing (~500-800 tokens)
5. Integration: Feed context into downstream reasoning, dialogue, or implementation

**Query Patterns**:

- Topic-Specific: `"{topic} - find relevant code, existing implementations, related components"`
- Architecture Scan: `"Project architecture, structure, patterns related to {domain_area}"`
- Pre-Edit Context: `"All symbols, classes, and methods involved in {change_description}"`

**Integration Commands**: `/brainstorm`, `/task`, `/implement`, `/analyze`, `/troubleshoot`

**Error Recovery**:

- Server unavailable → Fallback to Serena symbol search (`get_symbols_overview`) + Grep/Glob for basic codebase awareness
- No relevant results → Proceed without codebase context, note limitation to user
- Timeout → Use partial results if available, otherwise skip with warning
- Authentication expired → Note limitation, suggest `auggie login`, use fallback tools
- Working directory invalid → Prompt user for correct project path

## MCP Server Use Cases by Command Category

**Development Commands**:

- Context7: Framework patterns, library documentation
- Auggie: Pre-implementation codebase context

**Analysis Commands**:

- Context7: Best practices, patterns
- Playwright: Issue reproduction, visual testing
- Auggie: Codebase context and pattern discovery

**Quality Commands**:

- Context7: Security patterns, improvement patterns

**Testing Commands**:

- Playwright: E2E test execution, visual regression

**Documentation Commands**:

- Context7: Documentation patterns, style guides, localization standards
- Scribe Persona: Professional writing with cultural adaptation and language-specific conventions

**Planning Commands**:

- Context7: Benchmarks and patterns
- Auggie: Existing implementation awareness

**Deployment Commands**:

- Playwright: Deployment validation

**Meta Commands**:

- All MCP: Comprehensive analysis and orchestration
- Loop Command: Iterative workflows with Context7 (patterns)

## Server Orchestration Patterns

**Multi-Server Coordination**:

- Task Distribution: Intelligent task splitting across servers based on capabilities
- Dependency Management: Handle inter-server dependencies and data flow
- Synchronization: Coordinate server responses for unified solutions
- Load Balancing: Distribute workload based on server performance and capacity
- Failover Management: Automatic failover to backup servers during outages

**Caching Strategies**:

- Context7 Cache: Documentation lookups with version-aware caching
- Playwright Cache: Test results and screenshots with environment-specific caching
- Auggie Cache: Codebase retrieval results with working-directory-scoped caching
- Cross-Server Cache: Shared cache for multi-server operations
- Loop Optimization: Cache iterative analysis results, reuse improvement patterns

## Error Handling & Circuit Breaker Configuration

**Recovery Strategies**: Exponential backoff with jitter, circuit breaker pattern, graceful degradation, alternative routing, partial result handling.

**Circuit States**: CLOSED (normal) → OPEN (unavailable, fallback used) → HALF_OPEN (testing recovery)

**State Transitions**: failures ≥ threshold → OPEN | timeout elapsed → HALF_OPEN | test succeeds → CLOSED | test fails → OPEN (extend timeout)

### Per-Server Settings & Fallbacks

| Server | Threshold | Timeout | Fallback | Impact |
|--------|-----------|---------|----------|--------|
| Context7 | 5 failures | 60s | WebSearch for docs | Less curated results |
| Serena | 4 failures | 45s | Basic file operations | No semantic understanding |
| Playwright | 2 failures | 120s | Skip E2E, use unit tests | Reduced test coverage |
| Auggie | 3 failures | 45s | Serena + Grep/Glob | Reduced codebase awareness |

### Task Command Circuit Integration

| Compliance Tier | Required Servers | Fallback Allowed | Behavior |
|-----------------|-----------------|------------------|----------|
| STRICT | Serena | No | Block if unavailable |
| STANDARD | — (prefer Context7) | Yes | Use fallbacks, note limits |
| LIGHT | — | Yes | Native tools only |
| EXEMPT | — | Yes | No MCP dependency |

**Integration Patterns**:

- Minimal Start: Start with minimal MCP usage and expand based on needs
- Progressive Enhancement: Progressively enhance with additional servers
- Result Combination: Combine MCP results for comprehensive solutions
- Graceful Fallback: Fallback gracefully when servers unavailable
- Loop Integration: Context7 for improvement patterns
- Dependency Orchestration: Manage inter-server dependencies and data flow
