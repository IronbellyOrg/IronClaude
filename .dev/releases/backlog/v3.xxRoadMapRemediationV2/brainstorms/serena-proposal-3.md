## Adversarial Review Summary

Three proposals were reviewed against the sc-validate-roadmap-protocol SKILL.md (v2.0.0). Each was evaluated for strengths, weaknesses, feasibility within the skill's architecture, overlap with simpler approaches, and compliance with execution rules R1-R16.

**Key changes across all three proposals:**

1. **Proposal G (Evolutionary Domain Taxonomy)** — Substantially cut. The core idea of taxonomy persistence has merit but the original overengineered it with difficulty signals, adaptive agent allocation, and cross-validation learning loops. These create non-determinism that conflicts with R3 (Evidence-Based Claims) and R1 (Artifact-Based Workflow). Refactored to a simpler "taxonomy seed" that is written as an artifact file (not Serena memory), making it inspectable, diffable, and not dependent on MCP state. Serena memory adds coupling for minimal gain over a plain file.

2. **Proposal H (Symbol-Graph-Driven Requirement Extraction)** — Heavily cut. The strongest idea here — enriching vague code-referencing requirements with structural data — is genuinely valuable. But the proposal overreaches by injecting Serena calls into Phase 0.2, Phase 2, AND Phase 4, violating the skill's clean phase separation. The derived sub-requirements mechanism risks massive false-positive inflation (R6 violation) and the 150+ MCP round-trips make it impractical at standard depth. Refactored to a single optional enrichment pass gated behind `deep` depth only, producing an informational supplement rather than injecting derived requirements into the scoring pipeline.

3. **Proposal I (Pattern-Validated Spec Claims)** — Most promising of the three but still overscoped. The core insight — specs can be wrong about the codebase — is the most impactful problem statement. However, the original tries to verify quantitative claims ("168 eval tests") and structural inheritance relationships, which requires fragile heuristic parsing and produces unreliable results. Refactored to focus narrowly on file existence verification (high-confidence, low-cost) and drop the speculative pattern/count/structure verification. Also: this does NOT require Serena. `Glob` and `Grep` (already in the skill's allowed-tools) handle file existence checks. Serena is unnecessary overhead.

**Cross-cutting verdict:** All three proposals share a pattern of reaching for Serena MCP as a solution when simpler tools already in the skill's vocabulary would suffice. The skill explicitly binds verbs to tools in Section 4 (Execution Vocabulary). Adding Serena as a dependency creates fragility (MCP server must be running), non-determinism (memory state varies), and violates the skill's design as a document-to-document audit (Section 8 Boundaries: "Will Not: Validate code execution or test results — only document-level coverage"). The refactored versions preserve the valuable insights while respecting these constraints.

---

# Proposal G (Refactored): Taxonomy Seed File for Cross-Run Stability

## Problem Statement

Phase 0.4 (Build Domain Taxonomy) reinvents the domain decomposition from scratch on every validation run. When the same project runs validate-roadmap across multiple releases, domain names change, boundaries shift, and cross-cutting classifications become inconsistent. This makes cross-run coverage comparison impossible.

## Proposed Integration

After Phase 0.4 completes, write the final taxonomy as a structured artifact file alongside the other Phase 0 outputs. On subsequent runs, if a prior taxonomy file is provided via a new `--prior-taxonomy` flag, Phase 0.4 uses it as a seed for clustering rather than starting cold.

**No Serena required.** The taxonomy is a markdown artifact written by `Write` and read by `Read` — tools already in the skill's vocabulary (Section 4). The user controls when to reuse a prior taxonomy by explicitly passing the flag, eliminating non-determinism.

### Mechanism

**On first run (or without `--prior-taxonomy`)**: Phase 0.4 runs the existing cold-start algorithm unchanged. At completion, the taxonomy is already written to `{OUTPUT_DIR}/00-domain-taxonomy.md` per the current spec — no new artifact needed.

**On subsequent runs (with `--prior-taxonomy <path>`)**: Phase 0.4 reads the prior taxonomy file, extracts domain names and boundary descriptions, and uses them as initial cluster centers. New requirements are assigned to existing domains by affinity. Genuinely new domains are created. Dead domains (zero requirements) are pruned. A delta section is appended to the new taxonomy artifact showing what changed.

### What was cut and why

1. **Serena memory integration** — Cut. A plain file is inspectable, diffable, version-controlled, and does not depend on MCP server state. The user can diff two taxonomy files with standard tools. Serena memory is opaque.

2. **Difficulty signals and adaptive agent allocation** — Cut. This creates a feedback loop where validation quality depends on prior run outcomes, violating the principle that each validation should be independently reproducible. A bad prior run would poison future agent allocation. The skill's agent allocation logic (Phase 1.1) should remain deterministic based on requirement count and domain boundaries.

3. **Cross-validation learning** — Cut. Phase 3.9 writing signals back to memory creates a circular dependency between the assessment and the assessment infrastructure. The validator is a read-only audit (Section 8 Boundaries). It should not modify its own configuration based on results.

4. **Parallel cold-start comparison** — Cut from original risks section. Running two algorithms in parallel at `deep` depth and comparing divergence is expensive and unnecessary. If the user suspects taxonomy drift, they can run without `--prior-taxonomy` and diff the results manually.

## Phase(s) Affected

- **Phase 0.4** (Domain Taxonomy) — sole change. Reads optional prior taxonomy, seeds clustering, writes delta to artifact.

## New Flag

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `--prior-taxonomy` | | No | - | Path to a prior `00-domain-taxonomy.md` to seed domain clustering |

## Expected Value

1. **Taxonomy stability**: Domain names remain consistent across runs when seed is provided, enabling cross-run trend analysis.
2. **User control**: The `--prior-taxonomy` flag makes reuse explicit. No hidden state.
3. **Zero new dependencies**: Uses only `Read` and `Write`, already in the execution vocabulary.

## Risks

- **Stale seed**: A taxonomy from v2.0 may be a poor seed for v4.0 if the architecture changed radically. Mitigation: the user decides whether to pass the flag.
- **Format coupling**: The taxonomy artifact must be parseable as input. This constrains the format of `00-domain-taxonomy.md`. Mitigation: define a stable header format for the domain list section.

## Rule Compliance

- R1 (Artifact-Based): Taxonomy is a file artifact, not memory state.
- R3 (Evidence-Based): Seeded domains still require evidence-based assignment of requirements.
- R11 (Phase Sequencing): Only Phase 0.4 is affected; no cross-phase feedback loops.
- R16 (Preserve Artifacts): Prior taxonomy is read-only; new taxonomy is a new file.

---

# Proposal H (Refactored): Codebase Symbol Supplement for Deep Validation

## Problem Statement

Phase 0.2 (Requirement Extraction) relies entirely on natural-language parsing of spec documents. When specs reference code symbols ("extend `SprintExecutor.run()` to support budget-aware mode"), the full scope of the requirement is hidden in the codebase's call graph. Without structural knowledge, the validator cannot assess whether the roadmap's coverage of code-referencing requirements is complete or superficial.

## Proposed Integration

At `deep` depth only, add an **optional post-Phase-0 enrichment step** (Step 0.5) that uses Serena's symbol navigation to produce a **supplemental artifact** documenting the structural context of code-referenced requirements. This artifact is informational — it does NOT modify requirement records, inject derived sub-requirements, or alter coverage scoring.

### What was cut and why

1. **Derived sub-requirements injected into scoring** — Cut. The original proposed generating sub-requirements like "REQ-042a: Update 3 callers" and feeding them into the coverage pipeline. This inflates the requirement count with machine-generated items, violates R4 (Spec is Source of Truth — the spec did not say "update callers"), and produces false negatives (R6 violation) when a backward-compatible change doesn't require caller updates.

2. **Phase 2 agent enrichment** — Cut. Giving agents symbol context alongside requirements changes the agent protocol (Section Phase 2 Domain Agent Instructions). Agents validate spec requirements against roadmap text. Adding codebase structure to agent inputs crosses the boundary stated in Section 8: "Will Not: Validate code execution or test results — only document-level coverage."

3. **Phase 4 adversarial ripple-effect checking** — Cut. The adversarial pass (Phase 4) re-reads specs and roadmap with fresh eyes. Injecting automated dependency-graph checks changes its nature from human-judgment review to automated code analysis. The adversarial pass's value comes from reading the documents like a skeptic, not from running graph algorithms.

4. **Performance at standard depth** — Cut. The original acknowledged 150+ MCP round-trips. At `standard` depth, this is unacceptable. Restricting to `deep` depth (which already expects higher cost) and capping symbol lookups makes it viable.

### Mechanism

**New Step 0.5 — Symbol Context Supplement** (deep depth only):

1. Scan the requirement universe for identifiers matching code symbol patterns (PascalCase, dotted paths, backtick-quoted names).
2. For each unique symbol (capped at 30 lookups), use `serena.find_symbol()` to locate its definition.
3. For symbols found, use `serena.get_symbols_overview()` on the containing file.
4. Write results to `{OUTPUT_DIR}/00-symbol-context-supplement.md`.

The supplement is referenced by the adversarial pass (Phase 4) as background reading — a human reviewer can use it to make better judgments about whether code-referencing requirements are truly covered. It is NOT consumed programmatically by agents or scoring.

## Phase(s) Affected

- **Phase 0** — new Step 0.5, `deep` depth only. Produces informational artifact.

## Expected Value

1. **Informed adversarial review**: The Phase 4 reviewer has structural context when evaluating code-referencing requirements, catching shallow "mentions the class name" coverage.
2. **No scoring distortion**: Because the supplement is informational only, it cannot inflate requirement counts or produce false findings.
3. **Bounded cost**: 30-symbol cap means at most ~60 Serena calls (find + overview), acceptable at `deep` depth.

## Risks

- **Codebase required**: Only works when a codebase exists alongside specs. Greenfield specs get no benefit. Mitigation: skip Step 0.5 if no symbols are found or Serena is unavailable.
- **MCP dependency**: Serena must be running. Mitigation: Step 0.5 failure is non-blocking. Log a note and continue.
- **Symbol noise**: Not every backtick-quoted term is a real symbol. Mitigation: only include symbols that `find_symbol` successfully resolves.

## Rule Compliance

- R1 (Artifact-Based): Output is a file artifact, not injected into context.
- R4 (Spec is Source of Truth): No derived requirements are generated. The spec's requirements are unchanged.
- R6 (No False Positives): The supplement is informational; it cannot produce findings.
- R10 (Parallel Agents Independent): Agents never see the supplement. Only the orchestrator's adversarial pass uses it.
- R11 (Phase Sequencing): Step 0.5 runs after Step 0.4, before Phase 1. Clean sequencing.

---

# Proposal I (Refactored): Spec File Reference Verification

## Problem Statement

Specs frequently reference files and paths in the codebase: "the existing `trailing_gate.py` handles budget enforcement," "config keys are defined in `settings.yaml`." Phase 0.2 takes these claims at face value. When referenced files have been renamed, moved, or deleted, requirements built on them are invalid and the entire validation is corrupted downstream.

## Proposed Integration

Add a lightweight **Step 0.1.5 — File Reference Check** that verifies whether file paths mentioned in specs actually exist. This uses `Glob` (already in the execution vocabulary) — no Serena required.

### What was cut and why

1. **Serena dependency** — Cut entirely. File existence checking is a `Glob` operation. `Glob` is already in the skill's allowed-tools and execution vocabulary (Section 4: "Find files → Glob"). Adding an MCP dependency for something a built-in tool handles is unjustified complexity.

2. **Quantitative claim verification** — Cut. Counting "168 eval tests" by searching for test patterns is fragile. What counts as a "test"? A function starting with `test_`? A `@pytest.mark` decorated function? A class? The spec author and the search pattern will disagree, producing false STALE flags that erode trust in the report. The cost-to-reliability ratio is poor.

3. **Structural claim verification** — Cut. Verifying "class A inherits from B" requires parsing code structure. This crosses into code analysis territory, which the skill explicitly excludes (Section 8: "Will Not: Validate code execution or test results"). Checking inheritance relationships is code validation, not document validation.

4. **Pattern existence claims** — Cut. "Defines function Y" is ambiguous. Does a function named `y` in a different module count? Does a renamed function that does the same thing count? Too many edge cases for reliable automated verification.

5. **Confidence reduction on stale-sourced requirements** — Simplified. The original proposed complex adjudication rules (Step 3.4 modifications, Step 4.6 modifications). The refactored version simply flags stale file references in an informational section of the requirement universe artifact. The human decides how to weight this.

### Mechanism

**New Step 0.1.5 — File Reference Check**:

1. After reading all documents (Step 0.1), scan spec text for file path patterns: anything matching common extensions (`.py`, `.ts`, `.md`, `.yaml`, `.json`, `.toml`) in backtick-quoted or inline-code context.
2. For each unique path found, use `Glob` to check if the file exists in the project. Try the exact path first, then basename-only search.
3. Write a "File Reference Status" section at the top of `{OUTPUT_DIR}/00-requirement-universe.md` listing:
   - FOUND: `path/to/file.py` (resolved to `full/path/to/file.py`)
   - NOT FOUND: `old/path/to/thing.py` (referenced in spec.md, section 4.2)
4. Requirements whose source sections contain NOT FOUND references get an annotation: `file_ref_stale: true`.

That is the full scope. No new artifact files, no scoring changes, no adjudication rule modifications.

## Phase(s) Affected

- **Phase 0** — new Step 0.1.5 between document reading and requirement extraction. Adds a section to the existing requirement universe artifact.

## Expected Value

1. **Catches renamed/deleted files early**: The most common and highest-impact form of spec staleness is referencing files that no longer exist. This catches it before Phase 0.2 builds requirements on phantom files.
2. **Zero new dependencies**: Uses `Glob`, already in the execution vocabulary.
3. **Minimal performance cost**: One `Glob` call per unique file path. Typical specs reference 10-30 files. Negligible overhead.
4. **Non-invasive**: Adds information to an existing artifact. Does not change scoring, agent behavior, or verdict logic.

## Risks

- **Path resolution ambiguity**: A spec might say `settings.yaml` without a full path. Basename search may find multiple matches or the wrong file. Mitigation: report all matches; let the human judge.
- **Relative vs absolute paths**: Specs use inconsistent path conventions. Mitigation: try both project-relative and basename-only. Report confidence level for each resolution.
- **False NOT FOUND**: File exists but under a different path than the spec claims. This is still useful information — it means the spec's path is wrong even if the file exists somewhere.

## Rule Compliance

- R1 (Artifact-Based): Results written to artifact file section, not held in memory.
- R3 (Evidence-Based): Each FOUND/NOT FOUND claim is backed by a Glob result.
- R4 (Spec is Source of Truth): We verify the spec's claims are grounded, not that they are correct.
- R6 (No False Positives): NOT FOUND is informational, not a finding. It does not generate gaps.
- R11 (Phase Sequencing): Step 0.1.5 completes before Step 0.2 begins.
- Section 8 Boundary: File existence checking via Glob is document-adjacent, not code validation. The skill already uses Glob and Bash for file checks (Section 4).
