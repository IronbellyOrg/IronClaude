# Deep Comparative Analysis: TheAuditor vs SuperClaude Audit Pipeline

**Date**: 2026-03-23
**Scope**: Architecture, analysis methodology, capabilities, and strategic lessons

---

## Executive Summary

TheAuditor and SuperClaude represent two fundamentally different philosophies for code auditing with AI agents:

- **TheAuditor**: A database-first, polyglot security analysis platform that indexes codebases into SQLite, then serves deterministic query results to AI agents. It prioritizes correctness and ground truth via structured data.
- **SuperClaude Audit**: An evidence-gated, multi-pass classification pipeline that uses grep proof and tiered dependency graphs to make DELETE/KEEP/INVESTIGATE decisions. It prioritizes safe classifications with confidence tiers.

TheAuditor is broader in scope (security, taint, ML predictions, architecture visualization) while SuperClaude is deeper in its specific domain (cleanup classification with evidence guarantees). TheAuditor is now archived (Jan 2026); future work moved closed-source.

---

## 1. Architecture Comparison

### 1.1 Data Layer

| Dimension | TheAuditor | SuperClaude |
|-----------|-----------|-------------|
| **Storage** | SQLite databases (`.pf/repo_index.db`, `.pf/graphs.db`) | In-memory dataclasses with JSON checkpoint persistence |
| **Schema** | 70+ tables across 10 schema modules | Flat dataclass models (`FileAnalysis`, `ClassificationResult`, `DependencyEdge`) |
| **Persistence** | Full database with WAL mode, foreign keys, transactional integrity | `progress.json` checkpoints, batch-level atomic writes |
| **Query model** | SQL with recursive CTEs, ad-hoc queries via `aud query` | Python method calls on in-memory graph objects |
| **Incrementality** | SHA256-keyed AST cache, incremental re-indexing | Content-hash cache in `ResultCache` (SHA-256), session-scoped |
| **Size overhead** | 50-500MB+ for `repo_index.db`, 30-300MB+ for `graphs.db` | Negligible (in-memory, JSON artifacts) |

**Analysis**: TheAuditor's database-first approach enables arbitrary post-hoc queries that were never anticipated at analysis time. SuperClaude's in-memory approach is lighter but cannot support ad-hoc interrogation. The database is the critical differentiator -- it turns analysis from a one-shot pipeline into a persistent knowledge base.

### 1.2 Pipeline Architecture

| Dimension | TheAuditor | SuperClaude |
|-----------|-----------|-------------|
| **Pipeline model** | 24-phase indexing pipeline with async orchestration | 3-pass sequential pipeline (surface -> structural -> cross-cutting) |
| **Parallelism** | Subprocess execution with timeout, async architecture | Parallel sub-agent execution with batching (Haiku for surface, Sonnet for structural) |
| **Error handling** | Zero Fallback principle (parser failures surface, never silently degrade) | Batch retry with escalation; checkpoint-based resume |
| **Monorepo** | Early monorepo detection to avoid irrelevant scanning | Monorepo-aware batch decomposition with segment isolation |
| **Languages** | Python, JS/TS, Go, Rust, Bash, Terraform/HCL (7+) | Python, JS/TS (primary), polyglot pattern matching |

### 1.3 Parsing Strategy

| Dimension | TheAuditor | SuperClaude |
|-----------|-----------|-------------|
| **Python** | Built-in `ast` module, 27 specialized extractors, 47 data categories | Line-based pattern matching + regex for imports/exports |
| **JS/TS** | TypeScript Compiler API (full semantic), 10MB compiled bundle | Regex-based import/export detection |
| **Go/Rust** | Tree-sitter structural parsing | N/A (pattern matching only) |
| **Fidelity** | Manifest/receipt pairing to verify storage integrity | Evidence gate checks (string matching in evidence lists) |

**Analysis**: TheAuditor invests heavily in deep AST parsing per language, producing rich semantic facts. SuperClaude uses a lighter-weight approach -- `_default_analyzer` in `tool_orchestrator.py` is line-based pattern matching, with the expectation that AI sub-agents provide deeper analysis. This is a fundamental trade-off: deterministic extraction vs. AI-augmented interpretation.

---

## 2. Analysis Vectors Comparison

### 2.1 TheAuditor: Four-Vector Convergence Engine (FCE)

The FCE identifies high-risk code by finding where multiple independent analysis vectors converge:

| Vector | Source | Signal |
|--------|--------|--------|
| **STATIC** | Linters (ESLint, Ruff, Clippy, Bandit) | Code quality, security patterns |
| **STRUCTURAL** | CFG complexity analysis | Cyclomatic complexity, nesting depth |
| **PROCESS** | Git history (churn analysis) | File volatility, change patterns |
| **FLOW** | Taint propagation engine | Source-to-sink data flow vulnerabilities |

**Key design rule**: Multiple tools within the SAME vector do NOT increase density. Five linters flagging the same issue equals one STATIC vector signal, not five.

**Convergence scoring**: `density = len(vectors_present) / 4` -- pure math, no subjective weighting.

**Threshold**: When 3+ vectors converge on a file, confidence is claimed to be exponentially higher than any single tool.

### 2.2 SuperClaude: 3-Pass Multi-Agent Pipeline

| Pass | Agent | Function |
|------|-------|----------|
| **Pass 1** (Surface) | Haiku (fast, cheap) | DELETE/REVIEW/KEEP triage per file |
| **Pass 2** (Structural) | Sonnet (deeper analysis) | 8-field profiles: imports, exports, size, complexity, age, churn, coupling, test_coverage |
| **Pass 3** (Cross-cutting) | Consolidation | Duplication matrices, dead code detection, dependency graph analysis |

**Classification system**: Two-tier (actionable vs. informational) with 7 fine-grained actions (DELETE, KEEP, INVESTIGATE, REORGANIZE, MODIFY, ARCHIVE, FLAG), mapped back to 4 v1 categories.

**Evidence gate**: Every DELETE requires zero-reference proof; every KEEP requires reference evidence. No classification passes without evidence.

### 2.3 Head-to-Head: Analysis Methodology

| Aspect | TheAuditor | SuperClaude |
|--------|-----------|-------------|
| **Philosophy** | Evidence convergence across orthogonal vectors | Evidence-gated classification with confidence tiers |
| **Convergence** | 4 independent vectors, mathematical density scoring | 3-tier dependency graph (AST/grep/inference) with confidence labels |
| **Determinism** | Database queries produce identical results | Same inputs produce same classification (deterministic `classify_finding`) |
| **Confidence model** | Vector density (0-4 scale, threshold at 3) | Float confidence per classification (0.35-0.95 range per tier) |
| **Linter integration** | Wraps ESLint, Ruff, Clippy, Bandit with unified JSON | No direct linter integration; relies on AI sub-agents |
| **Git integration** | Git churn as PROCESS vector (deeply integrated) | Git log for age/churn in 8-field profiles |

---

## 3. Dead Code Detection

### 3.1 TheAuditor

Three detection methods:
1. **Isolated modules**: Files with no import edges in the module graph
2. **Dead symbols**: Functions/classes with zero callers in the call graph
3. **Ghost imports**: Imported symbols that are never referenced after import

Confidence levels: HIGH, MEDIUM, LOW. Notes that manual review is needed for entry points, tests, magic methods, and type-hint-related cases.

**Strength**: Symbol-level granularity via full call graph analysis. Can identify dead functions within otherwise-alive files.

### 3.2 SuperClaude

Detection via `dead_code.py` using the 3-tier dependency graph:
1. Files with exports that have **zero Tier-A importers** AND **zero Tier-B references**
2. Exclusions for entry points (16 patterns: `__main__`, `app.py`, `manage.py`, etc.)
3. Exclusions for framework hooks (12 patterns: `pytest_`, `middleware`, `celery`, etc.)

**Strength**: Conservative approach prevents false positives. Dynamic import detection (`dynamic_imports.py`) overrides DELETE to KEEP:monitor for dynamically-loaded files.

### 3.3 Comparison

| Aspect | TheAuditor | SuperClaude |
|--------|-----------|-------------|
| **Granularity** | Symbol-level (functions, classes) | File-level |
| **Graph source** | Full call graph from AST | 3-tier dependency graph (AST + grep + inference) |
| **Dynamic imports** | Not explicitly addressed in visible docs | Explicit detection and KEEP:monitor policy |
| **Entry point handling** | Noted as manual review needed | 16 built-in entry point patterns + custom list |
| **Framework hooks** | Noted as caveat | 12 built-in hook patterns with active exclusion |

**Verdict**: TheAuditor has finer granularity (symbol-level). SuperClaude has better safety nets (dynamic import protection, framework hook exclusion).

---

## 4. Taint Analysis

### 4.1 TheAuditor (Has It)

Full taint analysis engine with:
- **Algorithm**: IFDS backward worklist with predecessor resolution (dual direction)
- **Field sensitivity**: Access path tracking
- **Vulnerability classes**: 18+ including SQL injection, command injection, XSS, path traversal
- **Sanitizer detection**: Identifies sanitization functions in data flow paths
- **Source/sink registry**: Configurable source and sink definitions
- **Boundary analysis**: Security boundary quality scoring (CLEAR, ACCEPTABLE, FUZZY, MISSING)
- **Severity levels**: Critical, High, Medium, Low (filterable via `--severity`)
- **Framework awareness**: Pluggable DFG strategies for Django ORM, Express middleware, Go HTTP handlers, Rust traits, Bash pipes

### 4.2 SuperClaude (Does Not Have It)

SuperClaude has no taint analysis capability. The closest analogs are:
- **Credential scanner** (`credential_scanner.py`): Pattern-based detection of hardcoded secrets (10 patterns: AWS keys, GitHub tokens, Slack tokens, Stripe keys, private keys, generic passwords/tokens)
- **Placeholder exclusion**: Distinguishes real secrets from `${VAR}`, `<YOUR_KEY>`, `os.environ.get()` patterns

This is secret detection, not data flow taint analysis. It cannot track how untrusted data propagates through function calls.

### 4.3 Gap Analysis

SuperClaude lacks:
- Source-to-sink data flow tracking
- Interprocedural taint propagation
- Sanitizer detection
- Security boundary analysis
- Vulnerability class identification (SQLi, XSS, command injection, etc.)
- Field-sensitive access paths

This is the single largest capability gap between the two systems.

---

## 5. ML-Based Predictions vs Multi-Agent Consensus

### 5.1 TheAuditor: ML Pipeline

- **Feature engineering**: 109-dimensional feature vectors including:
  - File metadata, graph topology, execution history
  - AST proofs, git churn, semantic imports
  - AST complexity, security patterns, vulnerability flow
  - Type coverage, control flow, impact coupling
  - Agent behavior, session execution, text features
- **Three-model ensemble**:
  - Root Cause Classifier
  - Next Edit Predictor
  - Risk Regression
- **Training**: `aud learn --enable-git --session-dir` trains on your codebase history
- **Prediction**: `aud suggest --topk 10` predicts root causes and next files to edit
- **Session analysis**: `aud session` analyzes AI agent interactions for quality insights
- **Persistence**: `model.joblib` + `session_history.db`

### 5.2 SuperClaude: Multi-Agent Consensus

- **Agent tiering**: Haiku for surface scan (cheap, fast), Sonnet for structural analysis (deeper)
- **Confidence model**: Float confidence per classification, evidence-gated
- **PM Agent integration**: ConfidenceChecker (pre-execution), SelfCheckProtocol (post-implementation), ReflexionPattern (error learning)
- **No ML training**: No codebase-specific model training
- **Consensus**: Multi-pass agreement -- Pass 1 triage must be confirmed by Pass 2 structural analysis

### 5.3 Comparison

| Aspect | TheAuditor | SuperClaude |
|--------|-----------|-------------|
| **Approach** | Classical ML on extracted features | Multi-agent LLM consensus |
| **Training** | Codebase-specific model training | No training; relies on pre-trained LLM capabilities |
| **Cold start** | Handled explicitly; needs initial training | Works immediately (LLM has general knowledge) |
| **Improvement** | Model retraining on accumulated data | ReflexionPattern for error learning (cross-session) |
| **Prediction types** | Root cause, next edit, risk scoring | Classification confidence only |
| **Explainability** | Feature importance from ML models | Evidence lists attached to every classification |

---

## 6. AI Agent Integration

### 6.1 TheAuditor

Designed explicitly as a tool for AI agents:
- **Slash commands**: `/onboard`, `/theauditor:planning`, `/theauditor:security`, `/theauditor:impact`
- **Deterministic queries**: `aud query --symbol authenticate --show-callers` returns exact database results
- **Token efficiency**: Targeted queries instead of broad file reading
- **Context bundles**: `AIContextBundle` packages relevant facts for LLM consumption
- **Impact analysis**: `aud impact --symbol AuthService --planning-context` for pre-change analysis

### 6.2 SuperClaude

Built as part of an AI agent framework:
- **CLI pipeline**: `superclaude audit` orchestrates the full pipeline
- **Sub-agent dispatch**: Haiku and Sonnet agents dispatched per batch
- **Slash commands**: Part of the broader SuperClaude command system
- **Artifact output**: Reports to `.claude-audit/` directory
- **Incremental checkpointing**: Resume interrupted audit runs

### 6.3 Comparison

| Aspect | TheAuditor | SuperClaude |
|--------|-----------|-------------|
| **Integration model** | Tool FOR AI agents (provides facts) | Tool that IS an AI agent (orchestrates agents) |
| **Query interface** | SQL-backed CLI commands | Python API + CLI pipeline |
| **Token efficiency** | Targeted database queries (minimal tokens) | Batch processing with budget awareness |
| **Context packaging** | `AIContextBundle` with structured facts | JSON artifacts in `.claude-audit/` |
| **Real-time queries** | Ad-hoc queries at any time | Pipeline-based (run audit, then read results) |

---

## 7. Report Format and Structure

### 7.1 TheAuditor

- **Output directory**: `.pf/` with structured subdirectories
- **Raw exports**: JSON files (`fce.json`, `lint.json`, `taint.json`)
- **Audit journals**: NDJSON in `.pf/history/{run_type}/{timestamp}/journal.ndjson`
- **ML artifacts**: `.pf/ml/model.joblib` + `session_history.db`
- **AST cache**: `.pf/.cache/` keyed by SHA256
- **Format**: Structured JSON optimized for LLM consumption
- **Chunking**: Findings chunked into 65KB segments for AI context windows

### 7.2 SuperClaude

- **Output directory**: `.claude-audit/`
- **Checkpoint**: `progress.json` with batch-level status
- **Classifications**: `ClassificationResult` dataclass with evidence lists
- **Profiles**: 8-field `FullFileProfile` per file
- **Dependency graph**: Adjacency list with edge attributes
- **Duplication matrix**: Pair-wise similarity with recommendations
- **Dead code report**: Candidates with evidence + exclusions with reasons

### 7.3 Comparison

TheAuditor produces richer, more varied output formats (NDJSON journals, ML models, AST caches). SuperClaude produces more focused output oriented toward classification decisions.

---

## 8. Determinism: Database Queries vs Grep Evidence

| Dimension | TheAuditor | SuperClaude |
|-----------|-----------|-------------|
| **Ground truth** | SQLite database with indexed facts | Grep output + AST-resolved imports |
| **Reproducibility** | Same database = same query results | Same inputs = same classification |
| **Evidence chain** | Database records with transaction IDs | String evidence lists on `ClassificationResult` |
| **Verification** | Manifest/receipt pairing (storage integrity) | Evidence gate checks (string matching) |
| **Ad-hoc verification** | `aud query` for any question at any time | Must re-run analysis or read artifacts |

**Analysis**: TheAuditor's database provides stronger determinism guarantees. SuperClaude's evidence lists are more flexible but harder to verify independently. The manifest/receipt pattern in TheAuditor (count extracted items, verify stored count matches) is more rigorous than SuperClaude's string-based evidence checking.

---

## 9. Pros and Cons

### 9.1 TheAuditor

**Pros**:
1. **Database-first architecture** enables arbitrary post-hoc queries; analysis facts persist beyond the current session
2. **Four-vector convergence** provides mathematically grounded risk scoring with no subjective weighting
3. **Full taint analysis** with IFDS algorithm, 18+ vulnerability classes, sanitizer detection
4. **Deep AST parsing** per language (Python `ast`, TypeScript Compiler API, Tree-sitter) produces rich semantic facts
5. **ML pipeline** with 109-dimensional features enables codebase-specific predictions
6. **Framework-aware analysis** with pluggable DFG strategies (Django, Express, Go HTTP, etc.)
7. **Token efficiency** for AI agents via targeted database queries vs. broad file reading
8. **Polyglot support** at full semantic fidelity for Python and JS/TS, structural for Go/Rust/Bash
9. **Zero Fallback principle** surfaces parser failures instead of silently degrading
10. **Impact analysis** with blast radius calculation before changes

**Cons**:
1. **Heavy setup overhead**: Initial `aud full` takes 1-10 minutes; not suited for quick one-off scans
2. **Large database sizes**: 50-500MB+ for `repo_index.db` alone
3. **Python 3.14+ requirement** limits adoption (PEP 649 dependency for taint annotations)
4. **No IDE integration**: CLI-first workflow only
5. **Archived/closed-source**: Public repo archived Jan 2026; no community contribution path
6. **Complexity budget**: 12 engines, 70+ tables, 24 pipeline phases = high maintenance burden
7. **Limited language depth**: Go and Rust have structural analysis only (no type resolution)
8. **Cold start for ML**: Models need training data before predictions are useful
9. **No C++ support**
10. **Single-developer project origins** (described as vibe-coded in HN discussion)

### 9.2 SuperClaude Audit Pipeline

**Pros**:
1. **Evidence-gated classifications** prevent false positives; every DELETE requires zero-reference proof
2. **Multi-agent architecture** leverages LLM capabilities (Haiku for speed, Sonnet for depth) without custom ML training
3. **Dynamic import safety** explicitly protects dynamically-loaded files from false DELETE
4. **Incremental checkpointing** enables resume of interrupted audits
5. **Monorepo-aware batching** with segment isolation
6. **Lightweight footprint**: In-memory analysis, no large database overhead
7. **Framework hook awareness**: 12 built-in patterns prevent false positives on pytest fixtures, middleware, etc.
8. **Credential scanning** with placeholder exclusion (distinguishes real secrets from templates)
9. **Two-tier classification** with backward compatibility to v1 categories
10. **Plugin architecture** on `ToolOrchestrator` for extensible analysis
11. **3-tier dependency graph** with explicit confidence labels (A=AST, B=grep, C=inference)
12. **Budget-aware execution** with token cost management

**Cons**:
1. **No taint analysis**: Cannot track untrusted data flow through function calls
2. **File-level granularity only**: Dead code detection operates on files, not symbols
3. **Shallow parsing**: Default analyzer is line-based pattern matching, not AST-based
4. **No persistent knowledge base**: Analysis results are session-scoped; no database for post-hoc queries
5. **No linter integration**: Does not wrap ESLint, Ruff, Bandit, etc.
6. **No CFG analysis**: No cyclomatic complexity from control flow graphs (uses branch-counting heuristic)
7. **No ML predictions**: No codebase-specific model training or risk regression
8. **Limited language support**: Strong for Python/JS, minimal for other languages
9. **No impact analysis**: Cannot calculate blast radius before changes
10. **No architecture visualization**: No equivalent to `aud blueprint`
11. **Evidence checking is string-based**: `"zero" in e.lower() and "ref" in e.lower()` is fragile
12. **LLM dependency**: Classification quality depends on model capabilities (non-deterministic element)

---

## 10. What SuperClaude Can Learn from TheAuditor

### 10.1 HIGH PRIORITY: Database-First Architecture

**What TheAuditor does**: Every analysis result is stored in SQLite tables. Post-analysis, any question can be answered with a SQL query without re-scanning.

**What SuperClaude should adopt**:
- Replace or supplement in-memory dataclasses with a lightweight SQLite layer
- Store `FileAnalysis`, `ClassificationResult`, `DependencyEdge`, `DeadCodeCandidate` in tables
- Enable ad-hoc queries: "show me all files classified DELETE with confidence < 0.80"
- Persist across sessions: incremental re-audit only touches changed files
- Use recursive CTEs for transitive dependency queries instead of Python graph traversal

**Implementation sketch**: Add a `storage.py` module with:
```python
class AuditDatabase:
    """SQLite-backed persistent storage for audit results."""
    def __init__(self, db_path: str = ".claude-audit/audit.db"):
        ...
    def store_classification(self, result: ClassificationResult) -> None:
        ...
    def query_classifications(self, **filters) -> list[ClassificationResult]:
        ...
    def store_dependency_edge(self, edge: DependencyEdge) -> None:
        ...
    def transitive_dependents(self, file_path: str, depth: int = 3) -> list[str]:
        """Recursive CTE query for transitive dependents."""
        ...
```

**ROI**: High. Enables audit result persistence, incremental re-auditing, and ad-hoc querying with minimal implementation cost.

### 10.2 HIGH PRIORITY: Taint Analysis (New Capability)

**What TheAuditor does**: IFDS backward worklist algorithm tracking untrusted data from sources (user input, HTTP params) to sinks (SQL queries, shell commands, file writes) with sanitizer detection.

**What SuperClaude should adopt**:
- Start with a simplified version: regex-based source/sink detection per file
- Phase 2: Interprocedural taint tracking using the existing dependency graph
- Phase 3: Framework-aware strategies (Django ORM, Flask routes, Express middleware)
- Integrate with existing credential scanner as the "secret source" detection layer

**Minimum viable taint**:
1. Define source patterns (request params, user input, file reads)
2. Define sink patterns (SQL execution, subprocess calls, file writes)
3. Flag files containing both sources and sinks as TAINT:investigate
4. Use dependency graph to find files where source-file imports flow to sink-files

### 10.3 MEDIUM PRIORITY: Four-Vector Convergence Concept

**What TheAuditor does**: Combines STATIC + STRUCTURAL + PROCESS + FLOW vectors, scoring density as `vectors_present / 4`.

**What SuperClaude can adapt**:
- SuperClaude already has elements of 3 vectors:
  - STATIC: credential scanning, pattern matching
  - STRUCTURAL: 8-field profiles (complexity, coupling)
  - PROCESS: git age/churn in profiles
- Missing: FLOW (taint analysis)
- Add a convergence scoring step after Pass 3 that counts how many independent signals agree on a file being high-risk

### 10.4 MEDIUM PRIORITY: Symbol-Level Dead Code Detection

**Current state**: SuperClaude detects dead code at file level only.

**What to adopt**: Extend dead code detection to identify dead functions/classes within otherwise-alive files. This requires deeper AST parsing (at minimum for Python using `ast` module) to extract function/class definitions and track their callers.

### 10.5 MEDIUM PRIORITY: Linter Integration

**What TheAuditor does**: Wraps ESLint, Ruff, Clippy, Bandit with parallel orchestration and batching. Outputs unified JSON.

**What SuperClaude should adopt**: Integrate Ruff (already in the project's dev dependencies) as a STATIC analysis vector. Run as subprocess, parse JSON output, feed findings into the classification pipeline.

### 10.6 LOWER PRIORITY: Manifest/Receipt Verification

**What TheAuditor does**: Every storage operation produces a manifest (expected count, transaction ID) and receipt (actual stored count). Reconciliation detects data loss.

**What SuperClaude can adopt**: The existing evidence gate is a lighter version of this concept. Could strengthen by adding counters: "analyzed N files, stored N classifications, produced N dependency edges" with reconciliation at pipeline completion.

### 10.7 LOWER PRIORITY: Impact Analysis

**What TheAuditor does**: Bidirectional BFS for blast radius, coupling scores, direct upstream/downstream identification.

**What SuperClaude can build on**: The 3-tier dependency graph already has the data structures. Add bidirectional traversal methods and a coupling score metric.

---

## 11. Strategic Recommendations

### Short-term (Next Release)
1. Add SQLite persistence layer for audit results
2. Integrate Ruff as a static analysis vector
3. Add convergence scoring across existing analysis dimensions

### Medium-term (2-3 Releases)
4. Implement basic taint analysis (source/sink pattern matching)
5. Extend dead code detection to symbol level for Python
6. Add manifest/receipt verification for pipeline integrity

### Long-term (Future)
7. Interprocedural taint analysis with framework strategies
8. Impact analysis with blast radius calculation
9. ML feature extraction from accumulated audit data

---

## 12. Source List

| Source | Type | URL |
|--------|------|-----|
| TheAuditor GitHub README | Primary | https://github.com/TheAuditorTool/Auditor |
| TheAuditor Architecture.md | Primary | https://github.com/TheAuditorTool/Auditor/blob/main/Architecture.md |
| HN Discussion | Secondary | https://news.ycombinator.com/item?id=45165897 |
| SuperClaude `cli/audit/` source | Primary | Local codebase: `src/superclaude/cli/audit/` (43 modules) |
| SuperClaude `classification.py` | Primary | Local: evidence-gated two-tier classification |
| SuperClaude `dependency_graph.py` | Primary | Local: 3-tier dependency graph |
| SuperClaude `dead_code.py` | Primary | Local: cross-boundary dead code detection |
| SuperClaude `tool_orchestrator.py` | Primary | Local: static-tool orchestration with caching |
| SuperClaude `credential_scanner.py` | Primary | Local: credential scanning with redaction |
| SuperClaude `duplication.py` | Primary | Local: structural similarity matrix |
| SuperClaude `dynamic_imports.py` | Primary | Local: dynamic import safety |
| SuperClaude `profile_generator.py` | Primary | Local: 8-field profile generation |
| SuperClaude `batch_decomposer.py` | Primary | Local: monorepo-aware batching |
| SuperClaude `checkpoint.py` | Primary | Local: incremental checkpointing |

**Confidence level**: HIGH for architectural comparison; MEDIUM for TheAuditor internals (Architecture.md was truncated in extraction -- taint engine, FCE, ML, and rules engine body text were not fully visible).

**Note**: TheAuditor's public repository was archived January 2026. The analysis is based on the last publicly available state.
