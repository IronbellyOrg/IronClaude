# Serena MCP Proposals — Adversarial Review

## Adversarial Review Summary

All three proposals were evaluated against the `sc-validate-roadmap-protocol` SKILL.md for strengths, weaknesses, feasibility, overlap, and implementability. Key findings:

### Cross-Cutting Issue: Serena Is Not in the Allowed-Tools List

The skill's frontmatter declares `allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`. Serena tools (`write_memory`, `read_memory`, `find_symbol`, `search_for_pattern`, etc.) are **not permitted**. Any proposal using Serena requires amending the skill's allowed-tools declaration and Execution Vocabulary (Section 4). This is not a blocker, but it is a prerequisite that none of the original proposals acknowledged.

### What Changed and Why

**Proposal A (Cross-Session Caching)**: Substantially narrowed. The original proposed skipping Phase 0 and Phase 1 entirely on cache hit. This violates R1 (Artifact-Based Workflow) and R16 (Preserve All Artifacts) — artifacts must be written every run regardless. The core value (avoiding redundant extraction) is real, but the mechanism was over-scoped. Refactored to cache the extraction *work* but still write all artifacts, and to use a simpler file-based cache with Serena only for hash-to-path metadata rather than storing entire requirement universes in Serena's memory (which has payload limits).

**Proposal B (Symbol-Aware Tracing)**: Rejected as core integration, preserved as an opt-in extension. The original violated Section 8 Boundaries: "Will Not: Validate code execution or test results — only document-level coverage." Adding a Phase 2.5 that queries the codebase symbol graph fundamentally changes the skill's identity from document-level auditor to code-aware auditor. The value proposition (catching blast-radius gaps) is genuine but belongs in a separate skill or as a post-validation step, not embedded in the validate-roadmap pipeline. Refactored to a standalone companion skill invoked after validation, not a new phase within it.

**Proposal C (Pattern-Based Adversarial Scanning)**: Moderately trimmed. The regex patterns proposed are achievable with Grep (already an allowed tool) and do not require Serena's `search_for_pattern`. The cross-session memory component (storing pattern effectiveness) adds real value but is the only part that genuinely needs Serena. Refactored to use Grep for pattern scanning (no new tool dependency for the core work) and Serena only for the optional cross-session learning component.

---

# Proposal A: Cross-Session Requirement Universe Caching (Refactored)

## Problem Statement

Phase 0 (Document Ingestion & Requirement Extraction) is the most expensive phase. Every invocation re-reads all specs, re-extracts all requirements, re-builds the domain taxonomy from scratch. When iterating on a roadmap (the common NO_GO -> fix -> revalidate cycle), the specs have not changed — only the roadmap has. Yet the entire requirement universe is rebuilt every time.

## Adversarial Debate

### Strengths
1. **Real pain point**: The NO_GO -> fix -> revalidate loop is the primary usage pattern. Re-extracting unchanged specs is genuinely wasteful.
2. **Content-hash keying is sound**: SHA-256 of concatenated spec contents provides reliable cache invalidation without timestamp fragility.
3. **Stable requirement IDs**: Cached extraction produces identical REQ-IDs across runs, making it possible to track which gaps were fixed. Today, re-extraction can shuffle IDs.

### Weaknesses
1. **Payload limits**: The original proposed storing entire requirement universes (potentially hundreds of YAML entries) in Serena's `write_memory`. Serena's memory is designed for lightweight metadata, not bulk data storage. A 500-requirement universe serialized to YAML could be 50-100KB.
2. **R1 violation**: The original proposed "skip Phase 0 Steps 0.2-0.4 and Phase 1 entirely." But R1 says "Every agent writes findings to its output file." R16 says "Do not delete intermediate files. Agent reports serve as the evidence trail." Even on cache hit, `00-requirement-universe.md`, `00-domain-taxonomy.md`, and `00-decomposition-plan.md` must be written. The original acknowledged this in Risks but the implementation sketch skipped artifact writing.
3. **Conceptual staleness**: The original's own Risks section admits "If a user edits a spec and then undoes the edit (same hash, but mental model changed), the cache would serve stale conceptual context." This is actually broader: if the *roadmap* changes significantly (different structure, new phases), the Phase 1 decomposition may no longer be optimal even though specs haven't changed. Decomposition depends on BOTH specs AND roadmap structure.
4. **40% savings claim is overstated**: Phase 0 and Phase 1 are orchestrator-only phases that read files and produce structured output. The expensive phases are Phase 2 (parallel agent spawning and full document reads by each agent) and Phase 4 (adversarial re-read). Phase 0/1 are closer to 15-20% of total pipeline cost.

### Feasibility Check
- Requires adding Serena tools to allowed-tools in frontmatter and Section 4.
- Phase 1 decomposition depends on roadmap structure (Step 0.3), not just specs. Caching Phase 1 output across roadmap changes is incorrect — only Phase 0's requirement extraction is safely cacheable.
- Does not violate R3-R16 if artifacts are still written.

### Overlap Check
- File-based caching (write cached extraction to `{OUTPUT_DIR}/.cache/`) achieves the same result without Serena. The orchestrator could check for `{OUTPUT_DIR}/.cache/{spec_hash}/requirement-universe.yaml` before extracting.
- Serena adds value only for cross-directory cache discovery (finding cached results from a previous output directory). If the user always uses the same `--output` directory, file-based caching suffices.

## Refactored Proposal

**Scope**: Cache Phase 0 requirement extraction only (not Phase 1 decomposition, which depends on roadmap structure).

**Mechanism**:
1. On Phase 0 completion, write cached extraction to `{OUTPUT_DIR}/.cache/{spec_hash}.yaml` containing the requirement universe and domain taxonomy.
2. On subsequent runs, check for cache file. If found and `--no-cache` not set, load cached extraction. Still write `00-requirement-universe.md` and `00-domain-taxonomy.md` from cached data (satisfying R1 and R16).
3. Always run Phase 1 fresh — decomposition depends on roadmap structure which may have changed.
4. Optionally use Serena's `write_memory` to store `vrp:cache:{spec_hash}:path` pointing to the cache file location, enabling cache discovery across different output directories.

**What was cut**:
- Phase 1 caching (decomposition depends on roadmap, not just specs)
- Storing bulk data in Serena memory (use file-based cache instead)
- The 40% savings claim (realistic savings: 10-15% on revalidation runs)
- Skipping artifact writing on cache hit

**Required skill changes**:
- Add `--no-cache` flag to Section 3 flags table
- If Serena cross-directory discovery is used: add Serena tools to allowed-tools
- Add cache-check logic to Phase 0 Step 0.2 preamble

---

# Proposal B: Symbol-Aware Requirement Tracing (Refactored)

## Problem Statement

Many spec requirements reference concrete code artifacts — function signatures, class names, config keys. The pipeline validates document-to-document coverage but cannot cross-reference claims against the actual codebase symbol graph. This creates phantom coverage (roadmap says "implement X" but X already exists with a different interface) and missed blast radius (modifying Y requires updating its 12 consumers, none mentioned in the roadmap).

## Adversarial Debate

### Strengths
1. **Genuine blind spot**: Document-level validation cannot catch "the roadmap says to change X but doesn't account for Y, Z, W that depend on X." This is a real class of planning failures.
2. **Quantifiable blast radius**: Instead of "modify UserSession model," the validation could report "UserSession is referenced in 14 files across 3 modules — roadmap covers 2." This is actionable intelligence.
3. **find_referencing_symbols is unique**: No other available tool provides call-site / dependency graph analysis. This is the one Serena capability with no overlap.

### Weaknesses
1. **Section 8 boundary violation**: The skill explicitly states "Will Not: Validate code execution or test results — only document-level coverage." Adding code symbol queries changes the skill's fundamental identity. This is not a minor enhancement; it redefines what the skill does.
2. **Phase 2.5 violates R11**: R11 says "Complete each phase before starting the next. Phase N depends on Phase N-1 outputs." Inserting Phase 2.5 between Phase 2 and Phase 3 breaks the numbered phase contract. All downstream phases would need renumbering, and the consolidated report format (Section 3.10) assumes a specific phase structure.
3. **False positive storm**: `find_symbol("Config")` matches dozens of unrelated symbols. PascalCase/snake_case extraction from natural-language spec text is error-prone. "The system will manage user sessions" would extract "user" and "sessions" as potential symbols, producing noise.
4. **Greenfield projects produce only noise**: For new codebases, every symbol is NEW. The entire phase produces zero value and maximum noise.
5. **Serena project activation overhead**: Requires `activate_project` and possibly `onboarding` before any queries work. If the project index is not built, the phase either fails or adds significant startup cost.
6. **Scope creep precedent**: Once the validator reads code, the boundary between "planning validation" and "implementation validation" dissolves. Next proposal will want to run tests. The boundary exists for a reason.

### Feasibility Check
- Violates Section 8 Boundaries (document-level only).
- Violates R11 (phase sequencing contract) by inserting Phase 2.5.
- Requires Serena tools not in allowed-tools.
- `find_symbol` and `find_referencing_symbols` require an indexed project, adding a precondition.
- GAP-S{N} ID scheme conflicts with the existing GAP-{SEVERITY_PREFIX}{N} scheme in Phase 3.

### Overlap Check
- Grep + Glob can find file references and basic symbol names without Serena.
- The unique value (dependency graph / reference counting) genuinely requires Serena — no overlap there.
- But that unique value belongs in a different skill, not embedded here.

## Refactored Proposal

**Recommendation**: Do not integrate into `sc-validate-roadmap-protocol`. Instead, create a companion skill: `sc-validate-roadmap-symbols` (or add as a post-validation step in the pipeline).

**Design for the companion skill**:
1. Takes as input the validation output directory (reads `00-requirement-universe.md` and `02-consolidated-report.md`).
2. Runs symbol validation as a standalone pass.
3. Produces `06-symbol-validation.md` in the same output directory.
4. Updates the consolidated report's verdict only if critical symbol conflicts are found.
5. Invoked separately: `/sc:validate-roadmap-symbols {output-dir}` or automatically when `--depth deep` is passed to the main validation.

**What was cut**:
- Embedding as Phase 2.5 within the existing skill (boundary violation)
- GAP-S{N} ID scheme (use existing GAP-{SEVERITY_PREFIX}{N} with `[SYM]` prefix instead)
- Automatic activation for all depth levels (companion skill, not default behavior)

**What was preserved**:
- The core value proposition: blast-radius analysis via `find_referencing_symbols`
- Symbol existence verification for code-referencing requirements
- The opt-in nature (`--verify-symbols` flag, now on the companion skill)

---

# Proposal C: Pattern-Based Adversarial Scanning (Refactored)

## Problem Statement

Phase 4 (Adversarial Pass) re-reads with the same tools (Read, Grep) and is likely to miss what the agents missed. Steps 4.3 (Orphan Requirements), 4.6 (Silent Assumptions), and 4.7 (Test Coverage Mapping) are weak because they rely on the same cognitive approach as the original extraction.

## Adversarial Debate

### Strengths
1. **Correct diagnosis**: The adversarial pass using the same tools and approach as the original extraction is a genuine weakness. Orthogonal verification methods catch blind spots.
2. **Pattern catalog is well-designed**: The modal verb patterns (`shall|must|will`), negation patterns (`must not|shall not|never`), and quantitative patterns (`at least|at most|within \d+`) are well-established requirements engineering heuristics. They would genuinely catch orphan requirements.
3. **Negation requirements are the highest-miss category**: "Must NOT" requirements are empirically the most commonly missed requirement type. A dedicated negation scan addresses this systematically.
4. **Cross-session learning is novel**: Storing which patterns produced valid findings and ranking them for future runs is genuine learning-loop value that no current mechanism provides.

### Weaknesses
1. **Serena's `search_for_pattern` vs Grep**: The proposal's own Risks section admits: "If Serena's pattern search is just regex under the hood, this adds no value over Grep." Serena's `search_for_pattern` IS regex under the hood for markdown files (it is symbol/AST-aware for code files, but specs and roadmaps are markdown). For document scanning, Grep already does everything `search_for_pattern` does, and Grep is already an allowed tool.
2. **False positive rate from modal verbs**: "The system will be built using Python" matches `will [^.]*` but is not a requirement. "Users must have a valid email to register" in an overview section is a statement of fact, not a requirement to extract. The proposal acknowledges this but the mitigation ("filter by context — require patterns to appear outside of introductory/overview sections") is vaguely specified and would itself need implementation.
3. **Pattern effectiveness memory assumes cross-project transfer**: Patterns that catch orphan requirements in a security spec may be useless for a data pipeline spec. Domain-specific vocabulary makes cross-project pattern transfer unreliable without project-type metadata (acknowledged in Risks but not addressed in the implementation).
4. **Test cross-reference (Enhancement 4.7a)** is under-specified: The pattern `[Tt]est[- _]?\d+` catches test IDs but not descriptions or scope. Building a "structured mapping" from regex matches is fragile. The current approach (re-reading both documents) is actually more reliable for semantic matching.

### Feasibility Check
- The regex pattern scanning is fully achievable with Grep (allowed tool). No Serena dependency needed for the core functionality.
- Cross-session memory (pattern effectiveness tracking) genuinely requires Serena's `write_memory`/`read_memory`. This is the only Serena-dependent component.
- Does not violate R1-R16. Enhances Phase 4 steps without restructuring the phase architecture.
- Does not violate Section 8 Boundaries (still document-level, still read-only).
- Pattern scanning integrates naturally into Steps 4.3, 4.6, 4.7 without new phases.

### Overlap Check
- Core pattern scanning: fully achievable with Grep. Serena adds zero value here.
- Cross-session learning: genuinely requires Serena. No current mechanism provides this.
- Structured test cross-reference: marginally better with Serena for code test files, but spec/roadmap test matching is a document operation where Grep suffices.

## Refactored Proposal

**Scope**: Enhance Phase 4 Steps 4.3, 4.6, and 4.7 with systematic regex pattern scanning using Grep. Optionally use Serena for cross-session pattern effectiveness tracking.

**Enhancement 4.3a — Systematic Orphan Requirement Detection (Grep-based)**

Add to Step 4.3 a structured pattern scan before the free-form orphan search:

```
For each spec file, run Grep with these patterns:
1. Modal requirements: (shall|must|required to|needs to) [^.]{10,80}
2. Negation requirements: (must not|shall not|never|prohibited|forbidden) [^.]{10,80}
3. Quantitative NFRs: (at least|at most|within|maximum|minimum) \d+
4. Conditional requirements: (if|when|unless) .{5,40} (must|shall|should)

For each match: check against the requirement universe.
If not already captured: create ADV finding of type ORPHAN_REQUIREMENT.
Filter: skip matches in document preamble/overview sections (first 20 lines of each file).
Filter: skip matches that are pure narrative (no concrete noun or measurable target).
```

**Enhancement 4.6a — Assumption Detection (Grep-based)**

Add to Step 4.6 a structured pattern scan:

```
Scan roadmap for assumption indicators:
1. Explicit: (assumes|assuming|given that|prerequisite|depends on)
2. Implicit state references: (existing|current|already|previously) .{5,40} (service|system|API|database|table|endpoint)

For each match: verify the assumed capability appears in the spec.
If not specified in spec: create ADV finding of type SILENT_ASSUMPTION.
```

**Enhancement 4.7a — No change**. The current re-read approach for test matching is more reliable than regex extraction for semantic matching of test descriptions and scope. The pattern `[Tt]est[- _]?\d+` catches IDs but misses the substance. Dropped from proposal.

**Cross-Session Learning (Serena-dependent, optional)**

If Serena is available (`--serena` flag or detected):
1. After Phase 4, compute effectiveness stats for each pattern: hit count, false positive rate, average finding severity.
2. Store via `write_memory` with key `vrp:adversarial-patterns:{project-type}`.
3. On future runs, `read_memory` retrieves ranked patterns. Insert top-performing historical patterns into the scan list before the default patterns.
4. Retention policy: keep top 20 patterns per project type. Expire entries older than 90 days.

**What was cut**:
- Serena `search_for_pattern` for document scanning (Grep does this already)
- Enhancement 4.7a test cross-reference (current approach is more reliable)
- Assumption that cross-project pattern transfer works without project-type segmentation

**What was preserved**:
- Systematic pattern catalog for orphan and assumption detection
- Negation requirement scanning (highest-value single pattern)
- Cross-session learning loop (the genuinely novel Serena contribution)

**Required skill changes**:
- Add pattern scanning steps to Phase 4 Steps 4.3 and 4.6
- If cross-session learning is used: add Serena read_memory/write_memory to allowed-tools; add `--serena` flag to Section 3
- Add pattern effectiveness reporting to Phase 6 summary
