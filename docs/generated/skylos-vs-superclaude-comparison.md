# Skylos vs SuperClaude Audit Pipeline: Deep Comparative Analysis

**Date**: 2026-03-23
**Scope**: Architecture, detection, security, CI/CD, MCP, auto-fix, multi-pass

---

## 1. Executive Summary

Skylos and SuperClaude's audit pipeline solve overlapping problems -- dead code detection, security scanning, and code quality analysis -- but from fundamentally different architectural positions. Skylos is a **standalone SAST tool** with an MCP server bolt-on, designed for individual developers and CI pipelines. SuperClaude is a **multi-agent orchestration framework** with audit as one pipeline, designed for AI-assisted development workflows within Claude Code.

**Key insight**: These tools are not direct competitors. Skylos operates at the *tool* layer (like ruff, vulture, or bandit). SuperClaude operates at the *orchestration* layer (like a CI pipeline manager that delegates to tools). The most productive framing is: could SuperClaude orchestrate Skylos as one of its evidence sources?

---

## 2. Architecture Comparison

### 2.1 Skylos Architecture

```
                     CLI / MCP Server / GitHub Action / VS Code Extension
                                         |
                     +-------------------+-------------------+
                     |                   |                   |
              Dead Code Engine    Security Engine     Quality Engine
              (AST + Tree-sitter) (Taint analysis)   (Complexity/lint)
                     |                   |                   |
              +------+------+    +-------+-------+          |
              | Python AST  |    | Pattern match |    Rule engine
              | TS/Go       |    | Taint flows   |    (SKY-L/P/UC/E)
              | Tree-sitter |    | Secret regex  |          |
              +------+------+    +-------+-------+          |
                     |                   |                   |
              Confidence scoring    Severity rating     Score/threshold
                     |                   |                   |
              +------+---------+---------+------------------+
              |           Result Layer                       |
              |  JSON / SARIF / LLM-optimized / Tree / TUI  |
              +------+---------+---------+------------------+
                     |                   |
              LLM Verification    Auto-Remediation
              (optional)          (LibCST / agent)
```

**Single-pass, multi-engine**: Skylos runs all enabled engines in a single invocation. Each engine (dead code, security, quality, secrets) operates independently on the same file set. Results are merged into a unified output.

**Parser strategy**: Python uses stdlib `ast`. TypeScript/Go use Tree-sitter. This is a pragmatic choice -- `ast` is fast and reliable for Python, Tree-sitter provides cross-language support without language-specific compilers.

**Confidence scoring**: Each finding carries a 0-100 confidence score. The default threshold is 60. Framework-aware patterns (Flask routes, pytest fixtures, Django admin) boost or suppress confidence.

### 2.2 SuperClaude Audit Architecture

```
               /sc:cleanup-audit Skill (Orchestrator)
                          |
            +-------------+-------------+
            |             |             |
         Pass 1        Pass 2        Pass 3
         Surface       Structural    Cross-cutting
         (Haiku)       (Sonnet)      (Sonnet)
            |             |             |
      +---------+   +---------+   +---------+
      | Wave 1  |   | Wave 1  |   | Wave 1  |
      | 7-8     |   | 7-8     |   | 7-8     |
      | agents  |   | agents  |   | agents  |
      +---------+   +---------+   +---------+
            |             |             |
      Evidence Gate  Evidence Gate  Duplication
      (grep proof)   (dep graph)   Matrix
            |             |             |
      Classification  Classification  Cross-cut
      (DELETE/KEEP/   (8-field       Comparison
       INVESTIGATE)    profiles)
            |             |             |
            +-------------+-------------+
                          |
                   Consolidation
                   (ultrathink)
                          |
                   Final Report
```

**3-pass, multi-agent**: SuperClaude uses a progressive refinement architecture. Pass 1 (Haiku) does cheap surface scanning. Pass 2 (Sonnet) does deep structural analysis on flagged files. Pass 3 (Sonnet) does cross-cutting comparison for duplication and systemic patterns.

**Evidence-gated**: Every classification must carry proof. DELETE requires zero-reference evidence (grep proof). KEEP requires reference evidence. This is the core philosophical difference -- SuperClaude treats the audit as a legal proceeding where every verdict needs evidence.

**42-module Python package**: The audit pipeline is implemented as a modular Python package under `src/superclaude/cli/audit/` with specialized modules for:
- `dead_code.py` -- cross-boundary dead code detection via 3-tier dependency graph
- `dependency_graph.py` -- Tier-A (AST), Tier-B (grep), Tier-C (inference) edges
- `credential_scanner.py` -- secret detection with placeholder exclusion
- `dynamic_imports.py` -- KEEP:monitor policy for dynamically loaded code
- `duplication.py` -- structural similarity via shared import/export overlap
- `evidence_gate.py` -- blocks unproven DELETE or unproven KEEP
- `classification.py` -- two-tier (actionable/informational) with v1/v2 mapping
- `wiring_gate.py` -- unwired callables, orphan modules, broken registries
- `tool_orchestrator.py` -- content-hash cached static analysis dispatch
- Plus 32 more modules for checkpointing, batch decomposition, profiling, etc.

---

## 3. Dead Code Detection

| Dimension | Skylos | SuperClaude |
|-----------|--------|-------------|
| **Approach** | AST/Tree-sitter single-pass scan | 3-tier dependency graph + evidence gate |
| **Recall claim** | 98.1% (benchmarked against 9 OSS repos) | No recall benchmark; designed for precision over recall |
| **False positive strategy** | Framework-aware patterns, confidence scoring | Evidence-gated: DELETE blocked without grep proof |
| **Confidence model** | 0-100 numeric score per finding | Tier-based: A (0.90), B (0.65), C (0.35) per edge |
| **Framework awareness** | Flask, Django, FastAPI, pytest, React, Next.js | Entry point patterns, framework hook patterns (general) |
| **Dynamic import handling** | Not explicitly documented | Dedicated `dynamic_imports.py`: KEEP:monitor policy for `__import__`, `importlib`, dynamic `require()` |
| **Runtime integration** | `.skylos-trace` runtime data correlation | No runtime integration |
| **Granularity** | Function, class, import, variable, parameter, file | File-level with export location tracking |
| **LLM verification** | Optional second pass with GPT-4.1/any model | Multi-agent verification via Sonnet in Pass 2 |
| **Safe removal** | LibCST-based syntax-safe pruning | Audit only; no auto-removal |

### Analysis

Skylos has the edge on **granularity and benchmarked accuracy**. It operates at the symbol level (individual functions, variables, imports) and has published benchmarks against real-world repos showing 98.1% recall with 3x fewer false positives than Vulture.

SuperClaude has the edge on **evidentiary rigor and safety**. The 3-tier dependency graph (AST import > grep reference > naming inference) with the policy that Tier-C edges never promote to DELETE is more conservative by design. The evidence gate literally blocks classifications that lack proof. The dynamic import detection with automatic KEEP:monitor override prevents a class of false positives that static-only tools struggle with.

**Gap for SuperClaude**: No published recall benchmarks. The file-level granularity (rather than symbol-level) means it cannot identify individual unused functions within an otherwise-used file.

**Gap for Skylos**: The confidence scoring is less transparent than SuperClaude's tiered evidence model. A score of "60" is harder to reason about than "zero Tier-A importers and zero Tier-B references."

---

## 4. Security Scanning

| Dimension | Skylos | SuperClaude |
|-----------|--------|-------------|
| **Taint analysis** | Yes -- flow tracking for SQL injection, XSS | No taint analysis |
| **Secret detection** | AWS, Stripe, OpenAI, private keys, high-entropy | AWS, GitHub, Slack, Stripe, generic API keys, passwords, private keys |
| **Placeholder exclusion** | Not explicitly documented | Yes -- `${VAR}`, `<YOUR_KEY>`, `changeme`, `os.environ`, `process.env` |
| **Prompt injection** | Full scanner: Unicode normalization, base64 decode, homoglyph detection | Not present |
| **AI defense** | 13 checks: dangerous sinks, input-to-prompt, tool scope, PII filter, model pinning | Not present |
| **OWASP mapping** | LLM01-LLM06 + Ops categories | Not present |
| **Supply chain** | Hallucinated dependency detection, undeclared dependency | Not present |
| **MCP security** | Tool description poisoning, unauthenticated transport, permissive URIs, network exposure | Not present |
| **Dangerous patterns** | `eval()`, `pickle`, weak crypto, `yaml.load()`, `marshal.loads()` | Not primary focus (wiring gate catches some structural issues) |
| **Redaction** | Not documented | Yes -- `[REDACTED]` marker in all output for real secrets |

### Analysis

Skylos dominates the security scanning dimension. Its taint analysis, prompt injection detection, AI defense scoring, supply chain scanning, and MCP-specific security checks represent a comprehensive SAST offering. The AI defense checks (13 rules covering OWASP LLM categories) are particularly relevant for 2026 codebases that increasingly integrate LLM APIs.

SuperClaude's credential scanner is competent but narrow -- regex-based pattern matching with intelligent placeholder exclusion. The redaction feature (replacing detected secrets with `[REDACTED]` in output) is a thoughtful safety mechanism that Skylos does not explicitly document.

**Gap for SuperClaude**: No taint analysis, no prompt injection scanning, no AI-specific defense checks, no supply chain analysis. These are significant omissions for a tool used in AI-assisted development.

**Gap for Skylos**: No explicit output redaction of detected secrets. No placeholder exclusion is documented (though the whitelist system may cover this implicitly).

---

## 5. Language Support

| Language | Skylos | SuperClaude |
|----------|--------|-------------|
| Python | AST parser, full feature set | Import/export pattern matching, grep-based |
| TypeScript/TSX | Tree-sitter parser, dead code + security + quality | JS/TS import resolution in dependency graph |
| Go | Supported (details sparse) | Not explicitly supported |
| Java | Appears in partial table | Not supported |
| Framework detection | Flask, Django, FastAPI, pytest, React, Next.js, Express | Entry point patterns, framework hooks (general) |

### Analysis

Skylos has broader and deeper language support. Its use of Tree-sitter for TypeScript/Go means it performs real parsing, not pattern matching. SuperClaude's language handling is regex-based -- it recognizes Python `import`/`from` and JS/TS `import`/`export` patterns but does not parse ASTs.

SuperClaude's approach is deliberately language-agnostic at the orchestration level. The dependency graph and evidence gates work the same regardless of language. But the tradeoff is shallower analysis per language.

---

## 6. MCP Server Approach

This is one of the most architecturally interesting comparison points.

### 6.1 Skylos: Tool as MCP Server

Skylos exposes itself as an MCP server with **13 tools**:

| Tool | Purpose |
|------|---------|
| `analyze` | Dead code analysis |
| `security_scan` | Security/danger scanning |
| `quality_check` | Quality analysis |
| `secrets_scan` | Secret detection |
| `remediate` | LLM-driven auto-fix |
| `verify_dead_code` | LLM verification of findings |
| `provenance_scan` | Git provenance analysis |
| `generate_fix` | Patch generation for dead code |
| `learn_triage` | Feed triage decisions back |
| `get_triage_suggestions` | Retrieve triage suggestions |
| `validate_code_change` | Diff-based pre-merge security validation |
| `get_security_context` | Project framework/security posture discovery |
| `city_topology` | Code-city visualization topology |

Plus **3 MCP resources** for result persistence and retrieval by run ID.

Architecture: `FastMCP` with auth gating, credit deduction, stdio/SSE/streamable-HTTP transport. Each tool is independently callable. Results are persisted and retrievable.

### 6.2 SuperClaude: Orchestrator of MCP Servers

SuperClaude does not expose itself as an MCP server. Instead, it **consumes** MCP servers:

- **Sequential MCP**: Multi-step reasoning for cross-cutting synthesis
- **Serena MCP**: Import chain tracing, symbol-level understanding
- **Context7 MCP**: Framework documentation validation
- **Auggie MCP**: Codebase search for broader context

The audit pipeline orchestrates these servers as evidence sources within its multi-pass architecture. MCP tools are only available to the orchestrator, not to spawned subagents.

### 6.3 Comparison

| Dimension | Skylos | SuperClaude |
|-----------|--------|-------------|
| **MCP role** | Producer (exposes tools) | Consumer (orchestrates tools) |
| **Integration point** | Claude Desktop, any MCP client | Claude Code internal orchestration |
| **Tool count** | 13 exposed tools | 0 exposed tools (consumes 4+ servers) |
| **Auth model** | Built-in auth + credit gating | Relies on MCP client-side auth |
| **Transport** | stdio / SSE / streamable-HTTP | Inherited from consumed servers |
| **Result persistence** | Built-in run storage + retrieval | File-based checkpointing |

**Key insight**: These are complementary approaches. Skylos as MCP server could be consumed by SuperClaude as an evidence source, similar to how SuperClaude already consumes Serena for symbol navigation or Context7 for documentation.

---

## 7. CI/CD Integration

| Dimension | Skylos | SuperClaude |
|-----------|--------|-------------|
| **GitHub Action** | Yes -- `action.yml`, `skylos cicd init` generates workflow | No GitHub Action |
| **PR annotations** | Yes -- inline comments on changed files | No PR integration |
| **Diff-aware** | `--diff origin/main` for changed-lines-only | No diff-aware mode |
| **Gating** | `skylos --gate` and `skylos cicd gate --input results.json` | Evidence gate is internal classification logic only |
| **Baseline** | Supports baseline for existing debt management | No baseline tracking for CI |
| **SARIF output** | Yes -- for GitHub/IDE integration | No SARIF output |
| **Threshold config** | `pyproject.toml` thresholds + `skylos-defend.yaml` | Configuration via skill arguments |

### Analysis

Skylos has a complete CI/CD story. The `skylos cicd init` command generates a ready-to-commit GitHub Actions workflow. PR annotations with inline comments, diff-aware scanning, baseline management, and SARIF output are table stakes for modern SAST tools, and Skylos delivers all of them.

SuperClaude has no CI/CD integration. The audit pipeline is designed as a developer-facing tool run interactively within Claude Code. There is no GitHub Action, no SARIF output, no PR annotation capability. The evidence gate is an internal classification mechanism, not a CI gate.

**This is the largest capability gap for SuperClaude.**

---

## 8. Auto-Fix and Remediation

| Dimension | Skylos | SuperClaude |
|-----------|--------|-------------|
| **Dead code removal** | LibCST-based safe pruning (imports, functions, decorators, async) | No auto-removal |
| **LLM remediation** | `skylos agent remediate . --auto-pr` with test-then-commit | No auto-fix |
| **Interactive mode** | CLI for verifying and selectively removing findings | No interactive removal |
| **Fix generation** | `generate_fix` MCP tool with patch validation and optional apply | No patch generation |
| **Dry run** | `--dry-run` for preview | N/A |
| **Quality cleanup** | `--standards` for LLM-guided quality improvements | Audit produces recommendations only |

### Analysis

Skylos provides a complete remediation pipeline: detect -> verify -> fix -> test -> commit -> PR. The LibCST-based removal ensures syntax-safe code changes. The MCP `remediate` tool allows AI agents to orchestrate the full cycle.

SuperClaude explicitly separates audit from fix. The audit pipeline is read-only by design. This is a deliberate philosophical choice -- the audit produces evidence-backed recommendations for human review, not automated changes. The argument is that false positives in automated deletion are catastrophic, so keeping a human in the loop is safer.

Both approaches have merit. Skylos mitigates the auto-fix risk with dry-run mode, confidence thresholds, and optional test execution. SuperClaude mitigates by not automating at all.

---

## 9. Multi-Pass vs Single-Pass Architecture

| Dimension | Skylos | SuperClaude |
|-----------|--------|-------------|
| **Pass count** | 1 (+ optional LLM verification) | 3 (surface + structural + cross-cutting) |
| **Agent model** | Single process, optional LLM call | Multi-agent waves (7-8 concurrent) |
| **Cost model** | Fixed per scan; LLM optional | Haiku for Pass 1 (cheap), Sonnet for Pass 2-3 (deeper) |
| **Progressive refinement** | No -- all findings in one pass | Yes -- Pass 1 triages, Pass 2 deepens flagged items |
| **Cross-file comparison** | Not a primary feature | Dedicated Pass 3 with duplication matrices |
| **Checkpointing** | Not documented | Every 5-10 files; resume from checkpoint |

### Analysis

SuperClaude's 3-pass architecture is more sophisticated for large codebases. The Haiku-first cost optimization means Pass 1 scans everything cheaply, and only flagged files get expensive Sonnet analysis in Pass 2. For a 10,000-file monorepo, this can mean 70% cost reduction compared to running Sonnet on everything.

The cross-cutting Pass 3 with duplication matrices and systemic pattern detection has no equivalent in Skylos. This pass identifies things like "these 5 config files share 80% content and should be consolidated" -- a finding that requires comparing files against each other rather than analyzing them individually.

Skylos's single-pass approach is simpler and faster. For most projects, one pass is sufficient. The optional LLM verification adds a second logical pass but only for dead code findings.

---

## 10. Detailed Pros and Cons

### 10.1 Skylos

**Pros**:
- Benchmarked 98.1% recall with 3x fewer false positives than Vulture
- Comprehensive security: taint analysis, prompt injection, AI defense, supply chain, MCP security
- Full CI/CD pipeline: GitHub Action, PR annotations, SARIF, diff-aware, baselines
- MCP server with 13 tools -- any AI agent can invoke Skylos analysis
- Auto-fix with LibCST safety, test execution, and auto-PR
- Multi-language: Python AST, TypeScript/Go Tree-sitter
- Framework-aware for 6+ frameworks
- Runtime trace integration for reducing false positives
- VS Code extension for in-editor findings
- Granular finding types: function, class, import, variable, parameter, file level
- Inline suppression (`# skylos: ignore`, `# noqa: skylos`)
- Active community (346+ stars, Real Python featured)

**Cons**:
- Single-pass architecture may miss cross-file systemic patterns
- No evidence-chain transparency (confidence score is a number, not a proof)
- No multi-agent orchestration for large codebases
- No checkpointing/resume for large scans
- LLM features require external API keys and incur cost
- Auto-fix carries inherent risk despite safety measures
- No output redaction for detected secrets (documented)
- AI defense checks are Python-only
- No built-in duplication/consolidation analysis
- Confidence scoring semantics are opaque (what makes something 60 vs 80?)

### 10.2 SuperClaude Audit Pipeline

**Pros**:
- Evidence-gated classification: every verdict requires proof
- 3-tier dependency graph with transparent confidence semantics
- Multi-pass progressive refinement: cheap surface -> expensive deep analysis
- Haiku-first cost optimization (50-70% reduction on Pass 1)
- Cross-cutting comparison with duplication matrices
- Dynamic import detection with automatic KEEP:monitor policy
- Checkpoint/resume for long-running audits
- Multi-agent parallelism (7-8 concurrent agents per wave)
- Conservative by design: uncertain -> INVESTIGATE, never DELETE
- Credential scanner with intelligent placeholder exclusion and output redaction
- Deep integration with Claude Code ecosystem (skills, personas, MCP consumption)
- Read-only audit eliminates auto-fix risk
- 42-module modular architecture allows selective use
- Wiring gate catches structural integrity issues (orphan modules, broken registries)

**Cons**:
- No CI/CD integration (no GitHub Action, no SARIF, no PR annotations)
- No benchmarked recall/precision metrics
- No taint analysis or flow-based security scanning
- No prompt injection or AI defense checks
- No supply chain analysis
- No auto-fix or remediation capability
- File-level granularity only (cannot find unused functions within used files)
- No MCP server exposure (cannot be called by external AI agents)
- Regex-based parsing instead of AST/Tree-sitter
- No VS Code extension
- No runtime trace integration
- Requires Claude Code environment (not standalone)
- Language support is shallow (pattern matching, not parsing)
- No diff-aware mode for incremental scanning

---

## 11. What SuperClaude Can Learn from Skylos

### 11.1 HIGH PRIORITY: MCP Server Exposure

**Current state**: SuperClaude consumes MCP servers but does not expose one.

**Opportunity**: Expose the audit pipeline as an MCP server with tools like:
- `audit_scan` -- run surface pass on a path
- `evidence_check` -- verify a specific file's classification evidence
- `dependency_graph` -- return the 3-tier graph for a path
- `credential_scan` -- run secret detection
- `wiring_check` -- run structural integrity analysis

**Impact**: Any AI agent (Claude Desktop, Cursor, Copilot) could invoke SuperClaude's audit capabilities. This transforms SuperClaude from a Claude-Code-only tool into a platform.

**Implementation path**: The `skylos_mcp/server.py` pattern is straightforward -- `FastMCP` with tool definitions wrapping existing analysis functions. SuperClaude's modular `src/superclaude/cli/audit/` package is already well-factored for this.

### 11.2 HIGH PRIORITY: CI/CD Integration

**Current state**: No CI/CD story at all.

**Opportunity**:
1. SARIF output from the classification/evidence gate results
2. GitHub Action that runs the audit pipeline in a container
3. PR annotations from evidence-gated findings
4. Diff-aware mode: only audit changed files against baseline
5. `pyproject.toml` configuration for thresholds and gates

**Impact**: Without CI/CD, the audit pipeline is a developer tool only. With CI/CD, it becomes an enforcement mechanism.

### 11.3 MEDIUM PRIORITY: Symbol-Level Granularity

**Current state**: Dead code detection operates at file level.

**Opportunity**: Detect unused functions, classes, and variables within otherwise-used files. Skylos does this with AST walking. SuperClaude could do it by extending `FileAnalysis` to track symbol-level exports and cross-referencing at the symbol level rather than file level.

**Impact**: File-level granularity misses the most common dead code pattern: individual unused functions in active files.

### 11.4 MEDIUM PRIORITY: Security Scanning Depth

**Current state**: Credential scanning only. No taint analysis, no prompt injection, no AI defense.

**Opportunity**: Add prompt injection detection (following Skylos's canonicalization + pattern matching approach), AI defense scoring (OWASP LLM mapping), and supply chain checks (hallucinated dependency detection).

**Impact**: As AI-generated code proliferates, detecting AI-specific security issues (phantom calls, disabled security controls, prompt injection payloads) becomes critical.

### 11.5 MEDIUM PRIORITY: Skylos as Evidence Source

**Current state**: SuperClaude consumes Serena, Context7, Sequential, and Auggie as MCP servers.

**Opportunity**: Add Skylos as an additional MCP evidence source. The orchestrator could:
1. Call Skylos `analyze` for dead code findings
2. Call Skylos `security_scan` for taint analysis results
3. Feed Skylos findings into SuperClaude's evidence gate as Tier-A evidence
4. Use SuperClaude's multi-pass architecture to cross-reference Skylos findings against its own dependency graph

**Impact**: This combines Skylos's benchmarked recall with SuperClaude's evidentiary rigor. Skylos finds the candidates; SuperClaude verifies the evidence.

### 11.6 LOW PRIORITY: Runtime Trace Integration

**Current state**: No runtime data integration.

**Opportunity**: Accept coverage data or runtime traces (similar to Skylos's `.skylos-trace`) to promote or demote dead code candidates.

**Impact**: Runtime data is the strongest possible evidence for or against dead code. A function that was called in production is definitively not dead.

### 11.7 LOW PRIORITY: Auto-Fix Pipeline

**Current state**: Deliberately read-only.

**Opportunity**: Add optional `--fix` mode with LibCST-based safe removal, gated behind evidence requirements and dry-run preview. The existing evidence gate could serve as the safety mechanism: only findings that pass the full evidence gate with high confidence are eligible for auto-fix.

**Impact**: Cautious auto-fix with evidence gating could be safer than Skylos's approach because the evidence requirements are stricter.

---

## 12. What Skylos Can Learn from SuperClaude

For completeness, areas where Skylos could benefit from SuperClaude's approach:

1. **Evidence transparency**: SuperClaude's requirement that every classification carries verifiable evidence (grep proof, import chain, reference citation) is more auditable than a confidence score
2. **Multi-pass cost optimization**: Haiku-first scanning could dramatically reduce Skylos's LLM costs when verification is enabled
3. **Cross-cutting analysis**: Duplication matrices and systemic pattern detection across files
4. **Dynamic import safety**: The KEEP:monitor policy for dynamically loaded code is a principled approach to a common false positive source
5. **Checkpoint/resume**: For large codebase scans, the ability to resume from the last checkpoint after interruption

---

## 13. Conclusion

Skylos is the more **complete standalone tool** -- broader security scanning, better language support, CI/CD integration, auto-fix, MCP server exposure, and benchmarked accuracy. It is ready for production use today across Python/TypeScript/Go codebases.

SuperClaude has the more **sophisticated analysis architecture** -- 3-tier dependency graphs, evidence-gated classification, multi-pass progressive refinement, multi-agent parallelism, and principled handling of dynamic imports. It excels at large-scale codebase audits where evidentiary rigor matters more than speed.

The highest-impact actions for SuperClaude are:
1. **Expose an MCP server** to make the audit pipeline accessible to any AI agent
2. **Add CI/CD integration** to make the audit pipeline enforceable
3. **Integrate Skylos as an MCP evidence source** to combine benchmarked recall with evidentiary rigor

---

## Sources

- Skylos GitHub repository: https://github.com/duriantaco/skylos
- Skylos MCP server source: `skylos_mcp/server.py` (13 tools, 3 resources)
- Skylos benchmark blog: https://dev.to/duriantaco/python-dead-code-i-scanned-flask-fastapi-and-7-other-popular-repos-heres-what-i-found-5c1c
- Skylos Flask case study: https://skylos.dev/blog/flask-dead-code-case-study
- Hacker News discussion: https://news.ycombinator.com/item?id=46866141
- SuperClaude audit modules: `src/superclaude/cli/audit/` (42 modules)
- SuperClaude audit skill: `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`
