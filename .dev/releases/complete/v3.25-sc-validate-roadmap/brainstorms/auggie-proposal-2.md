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
