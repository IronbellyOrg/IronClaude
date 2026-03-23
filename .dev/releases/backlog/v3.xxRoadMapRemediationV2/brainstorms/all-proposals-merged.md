# MCP Integration Proposals for sc-validate-roadmap-protocol (Post-Adversarial)

> All proposals have undergone structured adversarial review. Each file contains
> an Adversarial Review Summary documenting what was kept, cut, and refactored.

---

## AUGGIE MCP PROPOSALS

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


---

# Auggie MCP Proposal 2: Ground-Truth Symbol Resolution for File Change Coverage

## Adversarial Review Summary

**Reviewer verdict: CONDITIONAL ACCEPT — significant scoping required.**

### What survived the review

The core insight is sound: File Change Coverage checks (one of the 10 Specific Validation Checks in Phase 2) currently rely on string matching, which produces both false positives (roadmap references phantom paths, agent marks COVERED) and false negatives (spec references a pre-refactor path, agent marks MISSING). Auggie's `codebase-retrieval` can ground file-path references against the real codebase. This is a genuine gap with a proportional fix.

### What was cut and why

1. **Symbol-level resolution removed.** The proposal's Stages B and C expanded from file-path validation into class/method/function resolution and "wiring relationship" detection. This crosses the skill's explicit boundary: "Will Not: Validate code execution or test results — only document-level coverage" (Section 8). Verifying whether `GateRunner.validate()` exists is code-level validation, not document-level. The skill validates that the *roadmap* covers what the *spec* says — it does not verify that the *codebase* already implements what the roadmap plans to implement. A roadmap task saying "add `validate()` to `GateRunner`" is describing *future work*; the method's absence from the codebase is expected, not a finding.

2. **Coverage adjustment logic removed.** The proposal's Stage C introduced automatic downgrade/upgrade rules (COVERED->PARTIAL, MISSING->re-evaluate). This violates R3 (Evidence-Based Claims) by substituting Auggie output for agent evidence, and violates R4 (Spec is Source of Truth) by making the codebase's current state an authority over spec requirements. The spec may intentionally reference files that do not yet exist (new files to create). Downgrading coverage because a target file is absent would produce false findings.

3. **Phase 4 integration removed.** Giving the adversarial reviewer access to a Symbol Resolution Table is over-engineering. The adversarial reviewer already re-reads source documents (Step 4.1) and can use Read/Glob/Grep to verify file paths if suspicious. No new artifact needed.

4. **Phase 5 integration removed.** Embedding "correct file paths from Auggie" into remediation entries assumes the spec's paths are wrong and the codebase's paths are right. The spec is source of truth (R4). If the spec says "modify file X" and file X does not exist, the remediation is "clarify spec" — not "substitute Auggie's guess."

5. **`deep` depth symbol/relationship queries removed.** These would turn the validator into a code audit tool, which it explicitly is not.

### What was refactored

The pass is narrowed to a **File Path Existence Check** — a lightweight verification that file paths referenced in agent reports and the requirement universe actually exist on disk. Non-existent paths are flagged as annotations for human review, not automatic coverage adjustments. This can be done with `Glob` and `Bash` (both already in `allowed-tools`) without requiring Auggie at all, which eliminates an external dependency for a check that basic filesystem tools handle better.

### Key risk addressed

The original proposal's biggest risk was scope creep into code validation (acknowledged in its own risk table). The refactored version enforces the boundary by limiting the check to file existence only, using tools already available to the skill, and framing results as informational annotations rather than coverage overrides.

---

## Problem Statement

Phase 2 agents perform "File Change Coverage" checks (per the Specific Validation Checks list): when a spec says "modify file X" or a roadmap task targets `src/foo/bar.py`, agents currently treat these as opaque strings. They can only do text matching — confirming that the roadmap mentions the same filename the spec mentions. They cannot verify whether:

1. The file actually exists in the codebase.
2. Two tasks targeting "different" files actually resolve to the same module (aliased paths, moved files).

This means the validator can mark a requirement as COVERED when the roadmap references a file path that does not exist, or mark it MISSING when the roadmap uses a different but valid path to the same file. Both are coverage-accuracy errors — false negatives and false positives — that propagate into incorrect verdicts.

## Proposed Integration

Add a **File Path Verification Pass** as a sub-step within Phase 3 (Consolidation), between Step 3.1 (Collect Agent Reports) and Step 3.2 (Build Unified Coverage Matrix). This pass uses `Glob` and `Bash` (already in the skill's `allowed-tools`) to verify that file paths referenced in agent reports and the requirement universe actually exist on disk.

The pass works in two stages:

### Stage A: Extract File Path References

Scan all agent reports (`01-agent-*.md`) and the requirement universe (`00-requirement-universe.md`) for file path references using pattern matching: anything matching `src/`, `.py`, `.ts`, `.md`, or other recognizable path patterns. Build a deduplicated list of all referenced paths.

### Stage B: Filesystem Verification

For each unique file path, check whether it exists using `Glob` or `Bash` (`test -f`):

- **EXISTS**: File found at the referenced path.
- **NOT_FOUND**: No file at the referenced path. Use `Glob` with the filename (ignoring directory) to search for possible relocated files.
- **POSSIBLY_MOVED**: File not found at the referenced path, but a file with the same name exists elsewhere in the codebase.

Build a **File Path Verification Table** and write it as an annotation block at the top of the coverage matrix:

```markdown
## File Path Verification (Step 3.1b)

| Referenced Path | Source | Status | Notes |
|----------------|--------|--------|-------|
| `src/superclaude/cli/sprint/executor.py` | REQ-042 | EXISTS | — |
| `src/pipeline/hooks.py` | REQ-061 | POSSIBLY_MOVED | Candidate: `src/superclaude/cli/pipeline/trailing_gate.py` |
| `src/gates/runner.py` | Roadmap Phase 3 | NOT_FOUND | No match in codebase |

**Note**: This table verifies path existence only. NOT_FOUND paths may reference files to be created by the roadmap. POSSIBLY_MOVED paths require human review to determine if the spec or roadmap uses a stale path.
```

This table is **informational**. It does NOT automatically change any coverage status. Agents' assessments stand as-is. The table provides the orchestrator and adversarial reviewer with ground-truth context for interpreting path-based coverage claims.

## Phase(s) Affected

- **Phase 3 (Consolidation)**: New sub-step 3.1b "File Path Verification" inserted between Steps 3.1 and 3.2. Produces an annotation block in the coverage matrix.

No other phases are structurally changed. The adversarial reviewer in Phase 4 can reference the verification table if they choose, but no new artifact or instructions are added to Phase 4.

## Expected Value

**Accuracy improvement on File Change Coverage checks**: Provides ground-truth context for the single weakest validation category — the one that relies on string matching against paths that may be stale, aliased, or invented.

**Concrete impact scenarios**:

1. **Spec written before refactor**: Spec references `src/pipeline/hooks.py` which was renamed to `src/superclaude/cli/pipeline/trailing_gate.py`. Without verification, agent marks MISSING. With verification, orchestrator or adversarial reviewer sees the POSSIBLY_MOVED annotation and can re-evaluate during Step 4.2, preventing a false-negative finding.

2. **Roadmap invents plausible path**: Roadmap says "add task targeting `src/gates/runner.py`" — file does not exist. Without verification, agent marks COVERED (path looks reasonable). With verification, the NOT_FOUND annotation alerts the adversarial reviewer that the coverage claim targets a phantom path.

**Estimated false-positive/false-negative reduction**: 10-20% on requirements that reference specific file paths (typically 20-40% of a codebase-centric spec's requirements).

## Implementation Sketch

### 1. Reference Extractor (addition to Phase 3 orchestrator instructions)

Parse agent reports and requirement universe for file path references using pattern matching:

- File paths: anything matching `src/`, `.py`, `.ts`, `.md`, or other path-like patterns
- Deduplicate across agents (same path referenced by 5 agents needs one check)

### 2. Filesystem Check (using existing tools)

```
Step 3.1b — File Path Verification

After collecting agent reports (Step 3.1), verify all file path references:

1. Extract all unique file paths from agent reports and requirement universe.
2. For each path, check existence:
   - Use Bash: test -f "{path}" for exact match.
   - If not found, use Glob: **/{filename} for relocated files.
3. Build File Path Verification Table with status:
   EXISTS | NOT_FOUND | POSSIBLY_MOVED.
4. Write table as annotation block at top of coverage matrix
   (Step 3.2 output).

This table is INFORMATIONAL ONLY. Do not auto-adjust coverage statuses.
Agents' assessments stand. The adversarial reviewer may use this table
as evidence when challenging coverage claims in Phase 4.
```

### 3. Depth-Gating

- `quick`: Skip file path verification entirely (speed priority).
- `standard`: Verify file paths (exact match only, no relocation search).
- `deep`: Verify file paths with relocation search via Glob.

## Risks & Tradeoffs

| Risk | Severity | Mitigation |
|------|----------|------------|
| **False confidence from existence checks**: A file existing does not mean the roadmap task correctly targets it | LOW | Table is explicitly informational. Clear disclaimer: "EXISTS = file found on disk, not validated for correctness." No automatic coverage changes. |
| **Spec references files to be created**: NOT_FOUND is expected for new-file requirements | MEDIUM | Disclaimer in table: "NOT_FOUND paths may reference files to be created by the roadmap." Human reviewer interprets. |
| **Stale filesystem state**: Files may have been added/removed since last sync | LOW | Validator already runs in the working directory. Filesystem is as current as the checkout. |
| **Minimal wall-clock cost**: File existence checks are fast | NONE | `test -f` and `Glob` are near-instantaneous. No MCP round-trips. Batch all checks. |
| **Scope creep into code validation**: Temptation to expand from "does this path exist?" to "does this class/method exist?" or "is the implementation correct?" | MEDIUM | Enforce strict boundary: this pass checks file path existence only. It does not read file contents, parse symbols, or evaluate implementations. The skill remains a document-level audit per its Section 8 Boundaries. |


---

# Auggie MCP Proposal 3: Codebase-Grounded Remediation Plans

## Adversarial Review Summary

**Reviewed**: 2026-03-23 | **Verdict**: CONDITIONALLY ACCEPTED with scope reduction

### What Changed and Why

1. **Removed "evidence-backed effort" replacing heuristic effort levels.** The original proposal claimed Auggie file counts could replace the existing TRIVIAL/SMALL/MEDIUM/LARGE heuristic. This is false confidence. Auggie returns files that *match keywords*, not files that *must change*. A semantic search for "JWT rotation" might return 8 files that reference tokens but only 2 that need modification. The file-count-to-effort mapping (e.g., "7+ files = LARGE") is itself a heuristic — just a different, less transparent one. **Kept**: Auggie results as *advisory context* alongside the existing heuristic. **Cut**: The replacement claim and the rigid file-count thresholds.

2. **Removed the secondary Phase 3.9 impact.** The original proposal suggested Auggie-grounded effort estimates could flow backward into Step 3.9 aggregate metrics. This violates Phase Sequencing (R11) in spirit — Phase 5 enrichment should not retroactively alter Phase 3 outputs. The consolidated report metrics should reflect document-level analysis; codebase context belongs in the remediation artifact only.

3. **Added NFR/abstract-requirement exclusion as a hard rule, not just a mitigation.** The original risks table acknowledged that Auggie returns noise for abstract requirements ("system shall be horizontally scalable") but only listed it as a MEDIUM risk with a mitigation. In practice, this is the dominant failure mode. Queries for abstract NFRs will pollute the remediation plan with irrelevant file listings. The refactored version makes this an explicit skip condition in the algorithm.

4. **Capped query count and added a bail-out.** The original mentioned "max 15 queries" in the risks table but not in the implementation sketch. The refactored version embeds the cap in the algorithm and adds a bail-out: if the first 3 queries return <50% relevant results (orchestrator judgment), skip remaining queries and fall back to heuristic. This prevents wasting the entire Phase 5 on bad Auggie responses.

5. **Removed `mcp__auggie-mcp__codebase-retrieval` from `allowed-tools`.** The skill's `allowed-tools` line controls what the skill's *agents* can use. Auggie queries happen in the orchestrator during Phase 5, not in spawned agents. Adding it to `allowed-tools` would permit agents in Phase 2 to call Auggie, which is out of scope and risks uncontrolled token spend. The orchestrator already has access to MCP tools; no metadata change is needed for `allowed-tools`.

6. **Narrowed the "Codebase impact" block format.** The original example included verification commands (`uv run pytest tests/auth/`) and specific code change descriptions ("TokenManager.refresh() needs rotation logic"). This crosses the "Will Not" boundary — the skill does not prescribe implementation. The refactored format lists affected files and packages but does not suggest *what* to change in those files. That is the tasklist generator's job.

7. **Acknowledged the overlap-with-existing-tools weakness.** For many gaps, `Grep` and `Glob` can find relevant files without Auggie. The refactored proposal clarifies when Auggie adds genuine value over basic search: semantic/architectural queries where keyword matching fails. For keyword-obvious gaps, the orchestrator should prefer `Grep`/`Glob` and reserve Auggie for ambiguous cases.

### Strengths Preserved

- The core insight is sound: remediation plans that reference real code structure are more actionable than abstract checklists.
- Graceful degradation (Auggie unavailable = no change) is well-designed and preserved.
- Scoping to Phase 5 only keeps Phases 0-4 clean as document-level analysis.
- Limiting queries to CRITICAL+HIGH gaps is correct token discipline.

---

## Problem Statement

Phase 5 (Remediation Plan) currently generates patch checklists in a vacuum. When the validator identifies a gap — say, "REQ-042: JWT rotation policy is MISSING from the roadmap" — the remediation entry says something like:

```
- Action: ADD
- Change: "Add task for JWT token rotation policy implementation"
- File: roadmap.md:~line 180
```

This tells the roadmap author *what* to add but not *where the work actually lands in the codebase* or *which modules are involved*. The author must then manually investigate the codebase to write a meaningful roadmap task. This creates two failure modes:

1. **Vague remediation items** that produce equally vague roadmap tasks, which then produce vague tasklist items — the gap propagates downstream.
2. **Effort misestimation** — a "SMALL" remediation might actually require touching many files across multiple packages, but the heuristic has no signal to detect this.

The remediation plan is the skill's most actionable output, yet it is the least grounded in implementation reality.

## Proposed Integration

Add an **optional** Auggie-powered enrichment step between Step 5.1 (ordering) and Step 5.2 (patch checklist generation). When Auggie MCP is available, the orchestrator queries it for qualifying gaps to retrieve codebase context about the components that would be affected.

For each qualifying gap, the orchestrator:

1. **Extracts implementation keywords** from the gap's spec requirement text and domain tag (e.g., "JWT rotation", "token refresh", "auth middleware").
2. **Evaluates whether keywords are concrete enough** to produce useful results. Abstract/architectural requirements (NFRs, constraints without file-level specificity) are skipped.
3. **Queries Auggie** with a semantic codebase retrieval for those keywords, requesting file paths and architectural context.
4. **Attaches a codebase context block** listing affected files and packages as advisory information alongside the existing heuristic effort level.

The enriched remediation entry becomes:

```markdown
- [ ] **GAP-C01** (CRITICAL, MEDIUM): Add JWT token rotation policy task
  - File: roadmap.md:180-195
  - Action: ADD
  - Change: "Add task for JWT token rotation implementation"
  - Codebase context: (auggie-grounded, advisory)
    - src/auth/token_manager.py — token lifecycle management
    - src/auth/middleware.py — token validation
    - src/config/auth_settings.py — auth configuration
    - Affected scope: 3 existing files, 2 packages
  - Verification: re-read roadmap.md:180-195 after edit to confirm requirement addressed
  - Dependencies: [GAP-H03]
```

This provides codebase orientation to the roadmap author without prescribing implementation details.

## Phase(s) Affected

**Primary**: Phase 5 (Remediation Plan) — new sub-step 5.1b "Codebase Context Lookup" between ordering and patch checklist generation.

No changes to Phases 0-4. No changes to Phase 3 metrics. The codebase context is scoped strictly to the remediation artifact.

## Expected Value

1. **Oriented remediation**: Roadmap authors can see which codebase areas a gap touches, helping them write specific, file-aware tasks instead of vague "add support for X" entries.

2. **Effort calibration signal**: When a gap's codebase context reveals many affected files across multiple packages, it signals that the heuristic effort level may underestimate. The author can adjust accordingly.

3. **Reduced fix-and-revalidate cycles**: When remediation items reference real code structure, the roadmap author gets the fix right on the first pass instead of writing another vague task that fails re-validation.

4. **Graceful degradation**: When Auggie is unavailable (no MCP server configured, pre-code project, spec-only validation), the skill falls back to current behavior with zero impact. The enrichment is additive.

## Implementation Sketch

### New sub-step in Phase 5

```
Step 5.1b — Codebase Context Lookup (optional, requires auggie-mcp)

IF auggie-mcp is available AND project has existing codebase:

  query_count = 0
  relevance_misses = 0
  MAX_QUERIES = 10

  FOR each gap WHERE severity IN (CRITICAL, HIGH):
    IF gap.type IN (NFR, CONSTRAINT) AND gap.spec_text lacks file/module references:
      SKIP — abstract requirements produce noise, not signal.

    IF query_count >= MAX_QUERIES:
      BREAK — token budget cap reached.

    1. Extract search terms from gap.spec_text + gap.domain
    2. IF search terms are concrete keywords (function names, file paths, module names):
       PREFER Grep/Glob over Auggie — cheaper and more precise.
       ELSE:
       Call mcp__auggie-mcp__codebase-retrieval with:
         - query: "{requirement description} implementation"
         - context: "{domain} {related file paths from spec if any}"
    3. query_count += 1
    4. Evaluate response relevance (orchestrator judgment).
       IF response is irrelevant or empty:
         relevance_misses += 1
         IF relevance_misses >= 3 out of first 3 queries:
           BAIL OUT — Auggie context not useful for this codebase/spec pair.
           Add note: "Codebase context lookup abandoned — low relevance."
           BREAK
       ELSE:
         From response, extract:
           - affected_files: [path, brief description of role]
           - affected_packages: [unique parent dirs]
         Attach codebase_context block to gap record.

  FOR gaps WHERE severity IN (MEDIUM, LOW):
    Use current heuristic effort estimation only (no codebase lookup).

ELSE:
  Proceed to Step 5.2 with current heuristic effort levels.
  Add note to report: "Codebase context lookup skipped — auggie-mcp not available."
```

### Artifact changes

`04-remediation-plan.md` gains a new optional section per qualifying gap:

```markdown
  - Codebase context: (auggie-grounded, advisory)
    - {file_path} — {brief role description}
    - ...
    - Affected scope: {N} files, {N} packages
```

The existing `effort` field (TRIVIAL/SMALL/MEDIUM/LARGE) remains heuristic-based. The codebase context is supplementary information, not a replacement.

### Skill metadata update

```yaml
mcp-servers: [sequential, auggie]  # auggie added as optional
```

No change to `allowed-tools` — the orchestrator calls Auggie directly during Phase 5. Spawned agents in Phase 2 do not use Auggie.

## Risks & Tradeoffs

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Auggie returns irrelevant results** for abstract/architectural requirements | HIGH | Hard skip: NFR/CONSTRAINT-type gaps without file-level specificity are excluded from queries. Bail-out after 3 consecutive irrelevant results. |
| **Over-specificity** — grounding in current code could bias toward incremental changes when redesign is warranted | MEDIUM | Codebase context is labeled "advisory" and does not replace the gap's remediation action (ADD/EDIT/MOVE/SPLIT). The format deliberately avoids prescribing code changes. |
| **Overlap with Grep/Glob** — many gaps can be located with basic keyword search | MEDIUM | Algorithm prefers Grep/Glob for concrete keywords. Auggie reserved for semantic/architectural queries where keyword matching is insufficient. |
| **Stale codebase index** — Auggie's index may not reflect recent changes | LOW | Auggie indexes on-demand. Add freshness note: "Codebase context based on index at {timestamp}." |
| **Pre-code projects have no codebase** — greenfield specs validated before any code exists | LOW | Graceful degradation: if Auggie returns no results, fall back to heuristic. Note "no existing codebase context available." |
| **Coupling between validation and implementation** — the skill is designed as a document-level audit; adding code awareness blurs the boundary | LOW | Scoped strictly to Phase 5 output enrichment. Phases 0-4 remain document-only. Codebase context is advisory annotation, not validation input. The "Will Not" boundary is preserved. |


---

## SERENA MCP PROPOSALS

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


---

# Serena MCP Proposals D, E, F — Adversarial Review & Refactored Versions

## Adversarial Review Summary

### What Changed and Why

**Proposal D (Cross-Session Validation Ledger)**: Substantially reduced in scope. The core value — delta reporting between runs — survives, but adversarial calibration (using historical false-positive rates to tune Phase 4 intensity) was cut. The adversarial pass is a *fresh-eyes* review by design; injecting historical bias contradicts its purpose and violates the spirit of R3 (evidence-based claims from *this* run's evidence). The ledger write was moved from Phase 6 to a post-completion hook to avoid polluting the phase architecture with MCP side-effects. Serena availability must be gracefully optional throughout, not just as a footnote.

**Proposal E (Symbol-Graph Integration Verification)**: Rejected in its current form and replaced with a much narrower variant. The original proposal directly violates Section 8 Boundaries: "Will Not: Validate code execution or test results — only document-level coverage." Symbol graph traversal IS code-level validation. Additionally, Serena's `find_symbol` / `find_referencing_symbols` are NOT in the skill's `allowed-tools` list (`Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`). Adding Serena as a tool dependency changes the skill's contract. The refactored version uses existing allowed tools (Grep, Glob) to do lightweight symbol-existence checks, which captures 80% of the value without violating boundaries or adding tool dependencies.

**Proposal F (Progressive Domain Knowledge Accumulation)**: Cut by roughly 60%. Taxonomy persistence and correction memory were removed entirely. Taxonomy persistence creates a *consistency trap*: stable domains sound good but actually prevent the validator from adapting to genuinely changed architectures. Correction memory is dangerous — it lets past human errors suppress future valid findings, creating a silent accuracy degradation path. What survives is terminology persistence (genuinely useful, low-risk) and pattern recording (informational only, no behavioral changes). Both are scoped as strictly optional enrichments.

### Cross-Cutting Concerns

1. **allowed-tools violation**: None of these proposals can use Serena tools unless the skill's frontmatter `allowed-tools` is updated. This is a prerequisite, not an afterthought, and must be weighed against keeping the skill's tool surface small.
2. **Graceful degradation is non-negotiable**: Every Serena integration must be wrapped in try/fail-open logic. The validator must produce identical core output with or without Serena.
3. **Phase architecture purity**: The 7-phase pipeline (0-6) is well-defined with clear inputs/outputs. MCP side-effects (memory reads/writes) should be pre-phase and post-phase hooks, not injected into phase step logic.

---

# Serena MCP Proposal D (Refactored): Cross-Session Validation Ledger

## Problem Statement

The `sc-validate-roadmap-protocol` treats every invocation as stateless. When a user runs the validator, applies fixes, and reruns, the second run has no awareness of the first. This causes two concrete problems:

1. **Regression blindness**: A fix for GAP-C01 might break coverage for REQ-042, but the second run cannot flag this as a *regression* because it has no baseline.
2. **Remediation churn tracking is manual**: The user must visually diff two reports to determine which gaps closed, persisted, or are new. On a 200-requirement spec this is error-prone.

## Proposed Integration

Use Serena's `write_memory` / `read_memory` to maintain a **Validation Ledger** that persists across sessions. The integration is structured as **pre-phase and post-phase hooks** — not modifications to phase step logic.

**Pre-Phase 0 Hook — Load Baseline (optional, fail-open):**

1. Attempt `read_memory("validation-ledger/{roadmap-slug}/latest")`.
2. If found, parse into a baseline summary (verdict, coverage scores, gap ID list, requirement count).
3. If Serena unavailable or memory missing, proceed without baseline. No degradation to core validation.

**Post-Phase 6 Hook — Write Ledger Entry (optional, fail-open):**

1. After the Phase 6 summary artifact is written and the core validation is complete, write a ledger entry to `validation-ledger/{roadmap-slug}/{timestamp}`.
2. Write `validation-ledger/{roadmap-slug}/latest` pointing to the same entry.
3. If Serena unavailable, skip silently. The validation report is already on disk.

**Phase 3 Addition — Delta Section in Consolidated Report:**

During Step 3.10 (Write Consolidated Report), if a baseline was loaded, append a delta section:

- Gaps present in both runs: **PERSISTENT** (with run count if available).
- Gaps in previous but absent now: **RESOLVED**.
- Gaps absent in previous but present now: **NEW**.
- Requirements COVERED in previous but now PARTIAL/MISSING: **REGRESSION** (auto-escalate severity by one level).

This delta section is *informational* — it enriches the report but does not change how findings are adjudicated in Step 3.4.

## What Was Cut and Why

**Adversarial calibration was removed.** The original proposal used historical false-positive rates to tune Phase 4 challenge intensity. This contradicts the adversarial pass's fundamental design: it is a *fresh-eyes* review (Step 4.1 explicitly says "Do NOT rely on agent reports for this pass"). Injecting historical bias makes it less adversarial, not more effective. If past runs had low false-positive rates, that tells you the agents are good — it does NOT mean the adversarial pass should be more aggressive on this run's different content.

## Phase(s) Affected

- **Pre-Phase 0**: Load baseline (new hook, outside phase logic).
- **Phase 3, Step 3.10**: Append delta section to consolidated report (additive only).
- **Post-Phase 6**: Write ledger entry (new hook, outside phase logic).

## Implementation Sketch

```python
# Pre-Phase 0 hook — BEFORE document ingestion
baseline = None
try:
    raw = serena.read_memory(f"validation-ledger/{roadmap_slug}/latest")
    baseline = json.loads(raw.content) if raw else None
except Exception:
    baseline = None  # fail-open: proceed without baseline

# Phase 3, Step 3.10 — append to consolidated report (only if baseline exists)
if baseline:
    delta = compute_gap_delta(
        previous_gaps=baseline["gap_ids"],
        current_gaps=current_gap_registry,
    )
    append_delta_section(consolidated_report, delta)
    # Regressions get severity += 1 in the delta display,
    # but this does NOT retroactively change Step 3.4 adjudication.

# Post-Phase 6 hook — AFTER all artifacts are written
ledger_entry = {
    "timestamp": now_iso(),
    "verdict": verdict,
    "weighted_coverage": score,
    "gap_ids": {g.id: g.severity for g in gaps},
    "req_count": total_reqs,
    "spec_content_hash": hash_spec_files(spec_paths),
}
try:
    serena.write_memory(
        f"validation-ledger/{roadmap_slug}/{timestamp}",
        json.dumps(ledger_entry),
    )
    serena.write_memory(
        f"validation-ledger/{roadmap_slug}/latest",
        json.dumps(ledger_entry),
    )
except Exception:
    pass  # fail-open: validation is already complete
```

## Risks & Mitigations

- **Memory bloat**: Each entry is ~2-5 KB. Mitigation: prune entries older than 30 days or keep only last 10.
- **Slug collisions**: Mitigation: use full relative path as slug, normalized to filesystem-safe characters.
- **Stale baselines after spec changes**: Include `spec_content_hash` in ledger entry. If hash differs between runs, warn that delta is approximate due to spec changes.
- **Serena unavailable**: All ledger operations are fail-open. Core validation is identical with or without Serena.

---

# Serena MCP Proposal E (Refactored): Lightweight Symbol-Existence Checks

## Problem Statement

Phase 3, Step 3.7 (Integration Wiring Audit) validates integration points by matching prose descriptions. When a spec references specific code symbols (e.g., `PaymentProcessor.on_complete()`), the validator cannot check whether those symbols exist or have been renamed. This is a real gap — but the solution must stay within the skill's document-level boundaries.

## What Was Cut and Why

**The original proposal was rejected because it violates two hard constraints:**

1. **Section 8 Boundary Violation**: The skill explicitly declares "Will Not: Validate code execution or test results — only document-level coverage." Traversing a symbol graph via `find_symbol` and `find_referencing_symbols` is code-level analysis.

2. **allowed-tools Violation**: The skill's frontmatter lists `Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill`. Serena tools (`find_symbol`, `get_symbols_overview`, `find_referencing_symbols`) are not in this list. Using them would be an execution rule violation.

3. **Scope creep**: The original proposal introduced fuzzy matching, reference graph traversal, and blast-radius analysis. Each of these is a feature-sized addition that moves the validator from "document audit" toward "code analysis tool."

## Refactored Proposal: Grep-Based Symbol Spot-Check

Use the skill's existing allowed tools (`Grep`, `Glob`) to perform lightweight symbol-existence checks. This captures the highest-value scenario (spec references a symbol that doesn't exist in the codebase) without crossing the document-level boundary.

**New optional sub-step in Phase 3, Step 3.7 — Symbol Spot-Check (--depth deep only):**

For each integration point where the spec text contains backtick-wrapped identifiers (the most reliable signal of a code symbol reference):

1. Extract backtick-wrapped identifiers from the spec requirement text.
2. Use `Grep` to search the codebase for each identifier.
3. If a symbol appears in zero files: flag as `symbol_not_found: true` on the integration entry. This upgrades an otherwise-COVERED integration to PARTIAL with a LOW finding: "Spec references symbol `X` which was not found in the codebase — verify it exists or has not been renamed."
4. If a symbol appears in files: note `symbol_found: true` with file paths. No further analysis.

This is a spot-check, not a graph analysis. It adds one `Grep` call per backtick-wrapped symbol, bounded by the number of integration points (typically 5-30).

## Phase(s) Affected

- **Phase 3, Step 3.7**: Optional enrichment of integration entries with `symbol_found` / `symbol_not_found` flags. Only for `--depth deep`.

## Implementation Sketch

```python
# Phase 3, Step 3.7 — only for --depth deep
if depth == "deep":
    for integration in integration_points:
        backtick_symbols = re.findall(r'`([A-Za-z_]\w*(?:\.\w+)*)`', integration.spec_text)
        for sym in backtick_symbols:
            # Use Grep (allowed tool) to search codebase
            results = grep(pattern=sym, path=project_root, type="py")
            if not results:
                integration.symbol_evidence.append({
                    "symbol": sym,
                    "status": "NOT_FOUND_IN_CODEBASE",
                })
                # Downgrade to PARTIAL if was COVERED
                if integration.verdict == "FULLY_WIRED":
                    integration.verdict = "PARTIALLY_WIRED"
                    add_finding(
                        severity="LOW",
                        description=f"Spec references `{sym}` but symbol not found in codebase",
                    )
```

## Risks & Mitigations

- **False positives from grep**: A symbol name like `run` will match everywhere. Mitigation: only check backtick-wrapped identifiers with dot-notation or PascalCase/snake_case patterns longer than 6 characters.
- **Language limitations**: Grep is language-agnostic but imprecise. Mitigation: this is a spot-check, not a guarantee. Findings are LOW severity and informational.
- **Performance**: One grep per symbol. For 30 integration points averaging 2 symbols each, that is 60 grep calls. Acceptable for `--depth deep`.

---

# Serena MCP Proposal F (Refactored): Terminology Persistence

## Problem Statement

The validator builds domain context from scratch on every run. For teams that validate related roadmaps repeatedly, two things are wastefully re-derived:

1. **Project-specific terminology**: Terms like "TurnLedger" or "fidelity gate" have project-specific meanings that the validator must re-derive from context each time.
2. **Recurring patterns**: Certain requirement types are consistently PARTIAL across runs, suggesting systematic under-specification — but this insight evaporates between sessions.

## What Was Cut and Why

**Taxonomy persistence was removed.** The original proposal persisted domain boundaries across runs for "consistency." This creates a *consistency trap*: if a project's architecture changes between v1.0 and v3.0, stale domain boundaries actively harm extraction accuracy. The validator's cold-start domain clustering (Step 0.4) is designed to adapt to the *current* spec — seeding it with stale domains biases it toward the past. Cross-run domain comparison can be done post-hoc by the user reading reports side-by-side; it does not need to be enforced by the tool.

**Correction memory was removed.** This is the highest-risk item in the original proposal. It allows a user's past disagreements with findings to automatically suppress future findings. If a user incorrectly rejects a valid finding, the correction memory silently degrades future accuracy. The expiration mechanism (5 runs / 60 days) does not help — the damage occurs within those 5 runs. Additionally, automated severity adjustment based on past corrections violates R3 (evidence-based claims) and R4 (spec is source of truth) — findings should be adjudicated based on current evidence, not historical user preferences.

**Agent assignment optimization was removed.** "Optimal agent configurations" from past runs presuppose that the same domains and requirement distributions apply to the next run. This is rarely true for evolving projects.

## Refactored Proposal: Terminology Map + Pattern Log

Two lightweight, low-risk Serena memory integrations:

### Terminology Map (Pre-Phase 0 load, Post-Phase 6 write)

**Load**: At startup, attempt `read_memory("project-terms/{project-slug}")`. If found, make the term map available during Phase 0, Step 0.2 requirement extraction. Terms are used as context hints, not as overrides — the validator still extracts from the current spec text.

**Write**: After Phase 6, if new glossary terms were discovered during extraction (from spec glossary sections, defined terms, or `NEEDS-SPEC-DECISION` resolutions), merge them into the term map and persist.

**Content**: A simple dictionary mapping project-specific terms to plain-language definitions. Maximum 200 entries. Example: `{"TurnLedger": "audit log system", "fidelity gate": "quality checkpoint"}`.

**Behavioral constraint**: The terminology map is *advisory*. It helps the extractor resolve ambiguous text but does not change coverage assessments, finding severity, or verdicts. If the map says "fidelity gate = quality checkpoint" but the current spec defines it differently, the current spec wins (R4).

### Pattern Log (Post-Phase 6 write only)

**Write only** — this is a log, not a feedback loop. After Phase 6, record:

- Requirement types that are consistently PARTIAL (suggests systematic under-specification in roadmap format).
- Domains with consistently high gap rates.
- Total requirement count and coverage score for trend tracking.

**No behavioral impact**: The pattern log does NOT change how any phase operates. It is written to `project-patterns/{project-slug}` for human review during retrospectives. A user can read it via `read_memory` in a separate session to understand trends, but the validator never loads it during execution.

This is the key distinction from the original proposal: patterns are recorded for human consumption, not consumed by the validator to change its behavior.

## Phase(s) Affected

- **Pre-Phase 0**: Load terminology map (fail-open).
- **Phase 0, Step 0.2**: Use terminology map as extraction context hints.
- **Post-Phase 6**: Write updated terminology map and pattern log entry.

## Implementation Sketch

```python
# Pre-Phase 0 hook
term_map = {}
try:
    raw = serena.read_memory(f"project-terms/{project_slug}")
    term_map = json.loads(raw.content) if raw else {}
except Exception:
    term_map = {}  # fail-open

# Phase 0, Step 0.2 — terminology as context hints during extraction
# term_map is passed to the requirement extractor as advisory context
# e.g., when spec says "TurnLedger", extractor knows it means "audit log system"
# This helps with domain classification, NOT with coverage assessment

# Post-Phase 6 hook — persist terminology
new_terms = extract_glossary_terms(spec_files)
if new_terms:
    merged = {**term_map, **new_terms}
    # Cap at 200 entries, keep most recent
    if len(merged) > 200:
        merged = dict(list(merged.items())[-200:])
    try:
        serena.write_memory(
            f"project-terms/{project_slug}",
            json.dumps(merged),
        )
    except Exception:
        pass  # fail-open

# Post-Phase 6 hook — write pattern log (append-only, never read by validator)
pattern_entry = {
    "timestamp": now_iso(),
    "roadmap": roadmap_path,
    "req_count": total_reqs,
    "weighted_coverage": score,
    "verdict": verdict,
    "consistently_partial_types": [
        t for t, rate in type_partial_rates.items() if rate > 0.5
    ],
    "high_gap_domains": [
        d for d, rate in domain_gap_rates.items() if rate > 0.3
    ],
}
try:
    existing = serena.read_memory(f"project-patterns/{project_slug}")
    patterns = json.loads(existing.content) if existing else []
    patterns.append(pattern_entry)
    patterns = patterns[-20:]  # keep last 20
    serena.write_memory(
        f"project-patterns/{project_slug}",
        json.dumps(patterns),
    )
except Exception:
    pass  # fail-open
```

## Risks & Mitigations

- **Stale terminology**: A term definition from v1.0 may mislead on v3.0. Mitigation: current spec definitions always override the map (R4). Include `last_updated` timestamp; terms older than 90 days are treated as lower-confidence hints.
- **Serena unavailable**: All operations are fail-open. Validator behavior is identical without Serena — slightly less context during extraction, no pattern log written.
- **Cross-project contamination**: Derive project slug from git remote URL or user-specified `--project` flag, not directory name alone.
- **Pattern log size**: Capped at 20 entries. Each entry is ~500 bytes.


---

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

