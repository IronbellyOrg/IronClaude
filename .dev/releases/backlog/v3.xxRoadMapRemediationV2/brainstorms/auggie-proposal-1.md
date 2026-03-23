# Auggie MCP Proposal 1: Codebase-Grounded Requirement Extraction in Phase 0

## Adversarial Review Summary

**Reviewer**: Adversarial self-debate (advocate + critic)
**Date**: 2026-03-23
**Verdict**: Proposal partially accepted. Core insight is valid but original implementation was overengineered and violated skill architecture constraints.

### What Changed and Why

| Original Element | Decision | Rationale |
|-----------------|----------|-----------|
| Problem statement | **Kept** (trimmed) | The core problem -- specs reference code that Phase 0 cannot resolve -- is real and well-articulated. |
| Step 0.2b as new pipeline step | **Kept** (simplified) | Correct location, but scoped down from 5 sub-procedures to 3. |
| `cluster_by_semantic_similarity()` | **Cut** | Pure fiction. No such capability exists in the orchestrator. The orchestrator is Claude using Read/Grep/Glob/Write/Edit/Task/Bash. There is no semantic clustering primitive. |
| Auto-generated derived requirements (`CODEBASE_DERIVED` type) | **Cut** | Dangerous. Machine-generating requirements inflates the requirement universe with items no human authored or reviewed. Dilutes coverage scores. Creates false precision. If a spec says "extend SprintExecutor.run()", the three callers needing updates are implementation details, not spec requirements. The validation should note them as codebase context, not promote them to P1 requirements. |
| New `00-codebase-context.md` artifact | **Cut** | Artifact proliferation. Codebase context belongs inline in `00-requirement-universe.md` as advisory annotations, not in a separate traceability file that no downstream phase reads. |
| 7 skill-level changes (new artifact, new type enum, Phase 2 agent instructions, Phase 4 step, etc.) | **Reduced to 3** | The original was too invasive for an "additive" step. Adding a new Phase 4 sub-step, modifying agent prompt templates, and adding a new requirement type are Phase-0-external changes that belong in separate proposals. |
| "Near-zero marginal token cost" claim | **Corrected** | Misleading. Each enriched requirement adds 200-500 tokens. With 60 code-referencing requirements, that is 12K-30K tokens added to Phase 2 agent prompts. Not zero. Still worthwhile if it prevents false COVEREDs, but the claim was dishonest. |
| Overlap with Read/Grep/Glob | **Acknowledged** | 60-70% of the value can be achieved with existing tools: Grep for backtick identifiers, Glob for file paths, Read for function signatures. Auggie adds semantic retrieval (callers, related tests, architectural context) that grep cannot provide. The proposal now clearly states what Auggie adds beyond existing tools. |
| Adding `codebase-retrieval` to `allowed-tools` | **Flagged as prerequisite** | This is a skill metadata change. It must be a deliberate decision, not buried in implementation notes. |

### Strength Summary (what survived)

1. The problem is real and well-scoped. Specs assume codebase knowledge that Phase 0 ignores today.
2. Phase 0 is the correct injection point -- enrichment before agent dispatch maximizes downstream value.
3. The optional/additive design is architecturally sound. Graceful degradation when Auggie is unavailable.
4. Enriched context genuinely helps Phase 2 agents distinguish COVERED from PARTIAL.

### Weakness Summary (what was cut)

1. Implementation sketch used fictional APIs (`cluster_by_semantic_similarity`).
2. Auto-generating requirements from code analysis crosses the line from "enrichment" to "scope inflation."
3. Seven skill-level changes for one "additive" step is scope creep -- the proposal was writing changes to Phases 2 and 4 while claiming to only modify Phase 0.
4. Token cost was understated; overlap with existing tools was not acknowledged.

---

## Problem Statement

Phase 0 (Document Ingestion & Requirement Extraction) operates entirely on spec and roadmap text. Specs routinely reference existing codebase constructs -- function signatures, class hierarchies, config schemas, API routes, test fixtures -- without fully restating them. The extraction algorithm has no way to resolve these references. Two failure modes result:

1. **Implicit requirements missed**: A spec says "extend `SprintExecutor.run()` to support budget overrides." Phase 0 captures the prose, but the actual contract of `SprintExecutor.run()` -- its parameters, callers, and downstream effects -- remains invisible. Agents later lack context to judge whether a roadmap task truly covers the requirement.

2. **Shallow acceptance criteria**: A spec states "all existing tests must continue to pass." Without knowing how many tests exist and what they cover, this becomes unverifiable. The validator cannot distinguish a roadmap that genuinely addresses backward compatibility from one that waves at it.

Both failures cascade: weak Phase 0 extraction produces weak Phase 2 assessments, inflated Phase 3 scores, and expensive Phase 4 rework.

**What existing tools already provide**: Grep can find backtick-quoted identifiers in source. Glob can verify file paths. Read can retrieve function signatures. These cover simple reference resolution. What they do NOT provide is semantic retrieval: finding callers of a function, related test files, or architectural context that the spec assumes but does not state. Auggie fills this gap.

## Proposed Integration

Add an optional **Step 0.2b -- Codebase Context Enrichment** between the current Steps 0.2 (Extract Requirement Universe) and 0.3 (Parse Roadmap Structure). This step annotates code-referencing requirements with codebase context.

The procedure:

1. **Scan the requirement universe for code references**. Identify requirements that mention specific files, functions, classes, modules, config keys, CLI commands, or test names. Heuristic: any requirement containing backtick-quoted identifiers, file paths matching `src/` or `tests/`, or explicit code keywords (`class`, `def`, `method`).

2. **Query Auggie for each code-referencing requirement** (or small group of closely related requirements). Issue a `codebase-retrieval` call with a query derived from the requirement text. Example: for "extend `SprintExecutor.run()` to support budget overrides," query "SprintExecutor run method signature callers budget." Hard cap: maximum **15 Auggie calls** for the entire step.

3. **Annotate the requirement record**. Append an advisory `codebase_context` note to each enriched requirement in `00-requirement-universe.md`:

```yaml
- id: "REQ-042"
  text: "extend SprintExecutor.run() to support budget overrides"
  source: "spec.md:L145"
  type: FUNCTIONAL
  priority: P0
  domain: "sprint-execution"
  codebase_context: |
    Symbol: SprintExecutor.run (src/superclaude/cli/sprint/executor.py:L87)
    Signature: def run(self, tasklist: Path, mode: str) -> SprintResult
    Callers: execute_sprint (tests/sprint/test_executor.py), pipeline runner
    Related tests: 12 tests in tests/sprint/
    Advisory: Method currently has no budget parameter; callers may need updating.
```

The `codebase_context` field is advisory -- it informs agent judgment but does not generate new requirements, change coverage calculations, or alter the requirement universe count.

**Crucially**, this step is additive. If Auggie is unavailable, the codebase is not indexed, or zero code references are found, Step 0.2b is skipped and the pipeline continues as today.

## Phase(s) Affected

**Primary**: Phase 0 (Ingestion) -- this is where the enrichment happens.

**Downstream benefits propagate naturally** (no Phase 2/4 changes required):
- **Phase 2**: Domain agents already read the full requirement record. A `codebase_context` field gives them concrete facts to assess coverage more precisely. An agent seeing "3 callers may need updating" can judge whether the roadmap addresses caller updates -- producing PARTIAL instead of COVERED when callers are omitted.
- **Phase 4**: The adversarial reviewer reads `00-requirement-universe.md` in Step 4.1. Codebase annotations give the reviewer ammunition to challenge COVERED assessments without needing to independently discover the codebase structure.
- **Phase 5**: Remediation descriptions can reference specific files and functions from the annotations, making patches immediately actionable.

No changes to Phase 2 agent prompt templates, Phase 4 step definitions, or Phase 5 procedures are required. The enrichment is data-level, not protocol-level.

## Expected Value

1. **Higher recall on implicit obligations**: Specs assume codebase knowledge. Annotations surface it. Estimated 10-20% more precise assessments for code-heavy specs.

2. **Sharper COVERED/PARTIAL distinction**: A roadmap task that says "update the executor" gets PARTIAL instead of COVERED when the agent sees untouched callers in the annotation.

3. **Actionable remediation**: Gap descriptions reference specific files and functions rather than vague categories.

4. **Reduced Phase 4 cost**: Stronger Phase 0 means Phase 4 finds fewer new gaps.

5. **Token cost**: Enrichment adds approximately 200-500 tokens per annotated requirement. For a spec with 60 code-referencing requirements, expect 12K-30K additional tokens across all Phase 2 agent prompts. This is a real cost, offset by reduced false COVEREDs and faster adversarial convergence.

## Implementation Sketch

```python
# Pseudocode for Step 0.2b — runs in orchestrator context (Claude + tools)

def enrich_requirements_with_codebase(requirements: list[Requirement]) -> list[Requirement]:
    """Called between Step 0.2 and Step 0.3. Orchestrator executes this logic."""

    code_referencing = [r for r in requirements if has_code_references(r.text)]

    if not code_referencing:
        return requirements  # No enrichment needed

    call_count = 0
    MAX_CALLS = 15

    for req in code_referencing:
        if call_count >= MAX_CALLS:
            break

        query = extract_query_terms(req.text)  # Strip prose, keep identifiers
        context = auggie_codebase_retrieval(query)
        call_count += 1

        if context:
            req.codebase_context = summarize_context(context)
            # Advisory annotation only. No new requirements generated.

    return requirements


def has_code_references(text: str) -> bool:
    """Heuristic: backtick identifiers, file paths, code keywords."""
    patterns = [
        r'`[A-Za-z_]\w+(\.\w+)*`',       # backtick-quoted identifiers
        r'src/\S+',                         # source file paths
        r'tests/\S+',                       # test file paths
        r'\b\w+\.py\b',                     # Python file references
        r'\b(class|def|function|method)\s+', # explicit code references
    ]
    return any(re.search(p, text) for p in patterns)
```

## Skill-Level Changes Required

Three changes to `SKILL.md`:

1. **Add `mcp__auggie-mcp__codebase-retrieval` to `allowed-tools`** in the frontmatter. This is the prerequisite for the step to function.

2. **Insert Step 0.2b** between Steps 0.2 and 0.3 with the procedure above (scan, query, annotate). Include the skip condition and the 15-call cap.

3. **Add `codebase_context` as an optional field** in the requirement record schema (Step 0.2). Mark it as advisory. No new requirement types, no new artifacts, no changes to coverage calculation formulas.

That is the full scope. No Phase 2 agent template changes. No Phase 4 sub-steps. No new artifact files.

## Risks & Tradeoffs

1. **Auggie availability**: If the Auggie MCP server is not running or the codebase is not indexed, Step 0.2b skips entirely. The pipeline never fails due to optional enrichment.

2. **Stale codebase index**: Auggie's index may lag behind the current branch. The `codebase_context` field is labeled advisory and agents treat it as informational, not authoritative.

3. **Token budget increase in Phase 0/2**: Enrichment adds 12K-30K tokens to Phase 2 agent prompts for code-heavy specs. This is a real cost. Mitigation: only requirements with code references get annotated; annotations are concise (200-500 tokens each).

4. **Scope creep risk**: The enrichment step could expand into call-graph tracing, coverage analysis, or dependency mapping. Mitigation: hard cap of 15 Auggie calls total. One query per requirement (or small group). No derived requirements. No new artifacts.

5. **Overlap with existing tools**: Simple reference resolution (does this file exist? what is this function's signature?) can be done with Grep/Glob/Read. Auggie is justified only for semantic queries (callers, related tests, architectural context) that pattern-matching tools cannot answer. If a future skill revision adds Read/Grep-based reference resolution to Step 0.2 directly, Auggie's marginal value decreases.

6. **Domain-specificity**: For pure greenfield specs (no existing code), enrichment adds nothing. Step 0.2b detects this (zero code references or zero Auggie results) and skips cleanly.
