# QA Report -- Research Gate (Partition 1 of 2)

**Topic:** Roadmap and Tasklist Generation Architecture Overhaul
**Date:** 2026-04-04
**Phase:** research-gate
**Fix cycle:** N/A
**Assigned files:** 01-pipeline-step-map.md, 02-input-routing.md, 03-prompt-architecture.md, 04-claude-process-output.md

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | All 4 files exist, have Status: Complete, and contain Summary sections |
| 2 | Evidence density | PASS | Dense (>80%). Sampled 16 claims across 4 files; all cited file paths exist and line numbers verified against source code |
| 3 | Scope coverage | PASS | All key files from research-notes EXISTING_FILES relevant to files 01-04 scope are examined (executor.py, prompts.py, commands.py, models.py, pipeline/executor.py, pipeline/process.py, pipeline/models.py, pipeline/gates.py) |
| 4 | Documentation cross-validation | FAIL | No `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]` tags used in any of the 4 files. Stale docs are identified in prose sections but lack required inline tag format |
| 5 | Contradiction resolution | FAIL | File 03 summary contains a factual error contradicting files 01 and 04 about file input mechanism (see Issues #2) |
| 6 | Gap severity | FAIL | Gaps present across all 4 files; severity classification provided below |
| 7 | Depth appropriateness | PASS | File 01 section 9 traces complete end-to-end data flow from CLI entry to output. File 04 traces full subprocess lifecycle. Meets Deep tier requirements |
| 8 | Integration point coverage | PASS | File 01 documents step-to-step data flow via file-on-disk pattern. File 02 documents input routing propagation through all steps. File 03 documents prompt function input/output dependencies. File 04 documents subprocess-to-gate-to-executor integration |
| 9 | Pattern documentation | PASS | File 01 section 10 documents 9 architectural patterns. research-notes.md PATTERNS_AND_CONVENTIONS documents 9 code conventions |
| 10 | Incremental writing compliance | PASS | All 4 files show iterative structure: numbered sections building progressively, gaps/questions sections referencing earlier sections, summary sections synthesizing findings. Not one-shot prose dumps |

## Summary

- Checks passed: 7 / 10
- Checks failed: 3
- Critical issues: 1
- Important issues: 2
- Minor issues: 0
- Issues fixed in-place: 0

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | All 4 files | **Missing `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]` inline tags.** No research file uses the required tag format for doc-sourced claims. Files 01, 03, and 04 each have "Stale Documentation Found" prose sections that identify stale docs, but the inline tagging convention is not used anywhere. This makes it impossible for synthesis agents to programmatically identify which claims are code-verified vs doc-only. | Add inline tags to all doc-sourced claims. At minimum: (a) File 01 "Stale Documentation Found" items should be tagged `[CODE-CONTRADICTED]` inline where they are first referenced. (b) File 02's "No stale documentation was found" items should have `[CODE-VERIFIED]` tags on the 4 checked claims. (c) File 03 section 14 items need `[CODE-CONTRADICTED]` or `[STALE DOC]` tags. (d) File 04 "Stale Documentation Found" item needs a tag. |
| 2 | CRITICAL | File 03 (03-prompt-architecture.md), Section 15, line ~656 | **Factual error in summary about file input mechanism.** The summary states: "File inputs are handled separately by the executor via `--file` flags." This directly contradicts: (a) File 01, Section 10, Pattern 2: "Inline embedding over `--file`: All input files are embedded directly into the prompt string. The `--file` flag is explicitly avoided." (b) File 04, Section 4: "Inputs are embedded inline into the prompt, not passed via `--file`." (c) The source code at `executor.py` line 719-721: "Inline embedding: read input files into the prompt instead of --file flags. --file is broken (cloud download mechanism, not local file injector)." The claim in file 03 is false. | Change file 03 summary to: "Architecture pattern: Each function returns a string that becomes the `-p` argument to `claude`. File inputs are embedded inline into the prompt by the executor via `_embed_inputs()`, not passed via `--file` flags." |
| 3 | IMPORTANT | File 01 (01-pipeline-step-map.md), Section 11, Gap #1 | **Certify step injection mechanism marked as unclear but verifiable.** File 01 states "The certify step may be dead code or invoked from an external caller not traced here." The function `build_certify_step()` exists at line 1259 of executor.py and `build_certification_prompt` is imported from `certify_prompts.py` (line 58). The gap claims the injection mechanism is unclear, but the research did not trace callers of `build_certify_step()` -- a grep for callers would resolve this. This is not a research finding; it is an incomplete investigation. | Grep for all callers of `build_certify_step` across the codebase and document where (if anywhere) the certify step is injected into the pipeline. If no callers exist, explicitly state "dead code -- zero callers found" rather than "may be dead code." |

---

## Gap Severity Assessment

### Gaps from File 01 (01-pipeline-step-map.md)

| Gap # | Description | Severity | Rationale |
|-------|-------------|----------|-----------|
| 1 | Certify step injection mechanism unclear | IMPORTANT | Incomplete investigation; synthesis may describe this step incorrectly |
| 2 | Step numbering inconsistency in comments | MINOR | Cosmetic, does not affect synthesis accuracy |
| 3 | Convergence mode lacks CLI flag | MINOR | Documented accurately; synthesis can describe as-is |
| 4 | `_auto_invoke_validate()` not traced | MINOR | Peripheral to main pipeline flow |
| 5 | Single-agent mode runs redundant diff/debate | IMPORTANT | This is a design concern the overhaul should address; needs deeper investigation |
| 6 | `_EMBED_SIZE_LIMIT` may cause E2BIG | MINOR | Documented with sufficient detail |
| 7 | TDD deviation-analysis incompatibility | MINOR | Already noted in CLI with user warning |
| 8 | No dynamic step injection | MINOR | Architectural observation, not a gap |

### Gaps from File 02 (02-input-routing.md)

| Gap # | Description | Severity | Rationale |
|-------|-------------|----------|-----------|
| 1 | PRD not selectable via --input-type | MINOR | Design choice, well-documented |
| 2 | TDD-as-spec_file semantic confusion | IMPORTANT | Could cause synthesis to describe incorrect behavior for TDD-mode steps |
| 3 | Diff/debate lack TDD/PRD context | MINOR | Documented accurately |
| 4 | Extraction never bypassed | MINOR | This IS the problem being researched |
| 5 | No input_type propagation beyond extract | MINOR | Well-documented architectural observation |
| 6 | Borderline detection scores | MINOR | Documented |
| 7 | Step 2 comment numbering gap | MINOR | Cosmetic |

### Gaps from File 03 (03-prompt-architecture.md)

| Gap # | Description | Severity | Rationale |
|-------|-------------|----------|-----------|
| 1 | No task table schema anywhere | CRITICAL | This is a root cause finding for the overhaul -- will synthesis correctly describe what to fix |
| 2 | Merge prompt lacks ID preservation | CRITICAL | Root cause finding |
| 3 | Merge prompt lacks _INTEGRATION_ENUMERATION_BLOCK | IMPORTANT | Root cause finding |
| 4 | No granularity floor in any prompt | CRITICAL | Root cause finding |
| 5 | Extraction lossy for structured data | IMPORTANT | Root cause finding |
| 6 | Diff discards agreements | MINOR | Architectural observation |

NOTE: File 03's "gaps" are actually KEY FINDINGS for the research topic (granularity loss root causes). They are not investigation gaps -- they are the answers to the research question. These should NOT block synthesis; they ARE the synthesis input. Reclassifying their gate severity:

- Gaps 1-5 from file 03: **Not blocking.** These are research findings, not investigation gaps. The file thoroughly documents what the code does and identifies the architectural weaknesses. This IS the expected output of a Deep-tier investigation into granularity loss.
- Gap 6: MINOR, not blocking.

### Gaps from File 04 (04-claude-process-output.md)

| Gap # | Description | Severity | Rationale |
|-------|-------------|----------|-----------|
| 1 | No truncation detection | MINOR | Documented accurately |
| 2 | Retry without learning | MINOR | Documented accurately |
| 3 | Prompt size ceiling | MINOR | Documented with mitigation |
| 4 | stream-json not used for roadmap | MINOR | Question, not gap |
| 5 | No partial output preservation | MINOR | Documented accurately |

---

## Blocking Issues (Must Resolve Before Synthesis)

1. **CRITICAL: File 03 factual error** (Issue #2) -- The summary incorrectly claims `--file` flags are used. This WILL propagate into synthesis if not corrected. Fix: edit one sentence in the summary.

2. **IMPORTANT: Missing inline doc-validation tags** (Issue #1) -- All 4 files lack required `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]` tags. Synthesis agents need these to distinguish code-backed claims from doc-only claims.

3. **IMPORTANT: Certify step investigation incomplete** (Issue #3) -- The certify step is described as "may be dead code" without evidence. A simple grep would resolve this.

---

## Confidence Gate

- **Verified:** 10/10 (all checklist items checked with tool evidence)
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100%

**Tool engagement:** Read: 12 | Grep: 12 | Glob: 13 | Bash: 2

Every checklist item has corresponding tool calls:
1. File inventory: Read all 4 files (verified Status: Complete and Summary present)
2. Evidence density: Glob verified 9 file paths; Read verified 6 specific line number claims; Grep verified 4 function locations
3. Scope coverage: Cross-referenced Read of research-notes.md EXISTING_FILES against coverage in files 01-04
4. Doc cross-validation: Grep searched all 4 files for tag patterns (0 matches = FAIL)
5. Contradiction: Read file 03 summary + Read executor.py lines 719-721 (confirmed contradiction)
6. Gap severity: Read all Gaps sections in 4 files, classified each
7. Depth: Read file 01 section 9 (end-to-end data flow diagram)
8. Integration: Read integration descriptions across all 4 files
9. Pattern documentation: Read file 01 section 10 + research-notes PATTERNS_AND_CONVENTIONS
10. Incremental writing: Read all 4 files, assessed structure (progressive sections, cross-references)

[PARTITION NOTE: Cross-file checks limited to assigned subset (files 01-04). Full cross-file verification requires merging all partition reports.]

---

## Recommendations

1. Fix the factual error in file 03 summary (1 sentence change)
2. Add inline `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]` tags to all 4 files where doc-sourced claims appear
3. Complete the certify step investigation in file 01 by grepping for callers of `build_certify_step`
4. After fixes, re-run QA (fix cycle 1) on the 3 changed files

## QA Complete
