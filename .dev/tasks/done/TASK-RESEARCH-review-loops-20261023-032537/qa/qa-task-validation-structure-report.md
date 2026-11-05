<!-- Verbatim agent return transcribed by main; source=/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-atask-structure-order-5cd0920e592d6e4f.jsonl:96; template=agent output format; producer report-write restriction respected. -->
# QA Report: Task Integrity, Phase Structure

**Topic:** Repeated planning and implementation review failures  
**Date:** 2026-10-23  
**Phase:** task-integrity  
**Fix cycle:** N/A  
**Fix authorization:** false  
**Overall Verdict:** FAIL

**Reviewed task:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md`

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | Task items 2.13, 3.1-3.10, 5.1 onward and later verification items; concrete example at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md:315` | Input filenames omit their directory prefixes, contradicting the explicit package-root resolution contract. Item 5.13 reads `synth-02-target-gaps.md` and `synth-03-external-findings.md`, but their producers create them under `synthesis/`. Case references similarly omit `research/`. Filesystem checks confirmed that the package-root case paths do not exist while the corresponding `research/` paths do. Following the task literally therefore breaks producer-to-consumer dependencies. | Give every input its complete package-relative or absolute path. Check all case, screening, synthesis, hypothesis, installed-reference and gate-decision references, not just these examples. Preserve the package-root resolution contract rather than relying on inferred directory inheritance. |
| 2 | IMPORTANT | Context fields throughout the task; examples at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md:127`, `:131`, `:315` | **92 of 103 Context fields** reference specific files but contain neither a file:line citation nor an evidence-absence justification. The live per-item evidence-binding rule explicitly includes specific files, so research-only scope does not exempt these references. | Add a verified source citation to each affected Context field, or a truthful `<!-- evidence-absence: ... -->` explanation when the referenced output does not yet exist. Do not invent future line numbers. The 11 currently citation-bearing items are 2.2-2.12. |
| 3 | MINOR | Completion items beginning at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md:545` | The mandatory `## Post-Completion Actions` section is absent. Phase 7 contains inventory, summary and final-status actions, but Template 02 explicitly requires the named section. The actions exist; the required structural section does not. | Add `## Post-Completion Actions` around the finalization sequence without changing its dependency order or weakening the final-state gate requirements. |

## Items Reviewed

“Verified” means the check was performed, not that the task passed it.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Actual frontmatter schema | PASS | YAML parsed successfully. Compared with actual Template 02 fields, including `created_date` and `template_schema_doc`; did not invent requirements for legacy aliases such as `created`, `template` or `tracks`. |
| 2 | Checkbox format | PASS | Mechanical scan found 103 valid flat `- [ ]` items and no malformed checkbox variants. |
| 3 | Single-paragraph, self-contained item structure | PASS | All 103 items have Context, Action/Output and Verify fields in one paragraph. Completion and blocker handling are embedded. Evidence-binding defects are recorded separately below. |
| 4 | No nested checkboxes | PASS | Full-file checkbox scan found no indented or parent-child checkbox structures. |
| 5 | Agent assignments and embedded operational instructions | PASS | Producer and reviewer items specify roles, inputs, outputs, focused work, verification and failure handling. No instruction to execute investigated historical plans was found. |
| 6 | Independent parallel work | PASS | Research and synthesis reviewer batches explicitly require same-message spawning. Hypothesis cards with dependencies remain sequential. Compared with Template 02’s independent-subagent exception. |
| 7 | Required phase and section structure | FAIL | Phases 1-7 are ordered, but the mandatory Post-Completion Actions section is absent. Issue 3. |
| 8 | Output paths | PASS | Producers specify persistent package-local output paths. Incorrect consumer paths are a separate dependency defect, Issue 1. |
| 9 | No standalone context-only items | PASS | Every checkbox produces an artifact, a review, an actual protocol invocation, a presentation or a task-state update. |
| 10 | Atomicity | PASS | Producer outputs and reviewer assignments have individual items. Consolidated correction workers are explicitly justified by the required single-writer correction protocol. |
| 11 | Within-phase producer-before-consumer ordering | FAIL | Intended order is sound, but shortened consumer paths do not resolve to their producers’ outputs. Issue 1. |
| 12 | Duplicate operations | PASS | No identical item bodies. Repeated verification has intervening production/correction or a distinct gate/lens purpose. |
| 13 | Durable verification | PASS | Research-only verification produces persistent Markdown reports, correction logs, source maps and decisions. Code tests are correctly N/A; no production code delivery is required. |
| 14 | Honest completion criteria | PASS | Final status depends on real outputs and final-state PASS reports. Historical uncertainty may remain explicitly bounded; missing mandatory artifacts cannot be called complete. |
| 15 | Phase and item dependency correctness | FAIL | Logical sequence is forward, but Issue 1 disconnects several literal file dependencies. |
| 16 | Execution-order simulation | FAIL | A literal executor reaches incorrect package-root input paths despite earlier creation of the correct directory-qualified outputs. Issue 1. No source-signature change is required by this research task. |
| 17 | Referenced implementation symbols | PASS | No production function/class implementation or signature migration is required. The explicit skill invocation is a harness operation, not a claimed repository function. |
| 18 | Phase counts and numbering | PASS | Mechanical counts: Phase 1: 2; Phase 2: 13; Phase 3: 15; Phase 4: 1; Phase 5: 27; Phase 6: 42; Phase 7: 3. Total: 103. Step numbering is contiguous. |
| 19 | Quantitative structural claims | PASS | Ten research reviewers, ten synthesis reviewers, 11 baseline final-report lenses with 13/15 size expansions, four fidelity reviewers plus contradiction reviewer, and four anti-omission reviewers are encoded. |
| 20 | Actual template cross-reference compliance | FAIL | Read actual Template 02, including completion, parallelism, reviewer floors, serialized corrections and source fidelity. Completion-section omission remains, Issue 3. Calling-skill two-cycle fidelity limit is correctly distinguished from the generic template limit. |
| 21 | Placeholder and title-only scan (TB-Add-1) | PASS | No checklist item contains literal `TBD`, `TODO` or `FIXME`. No title-only checklist item was found. Instructions to preserve unfinished historical originals are intentional evidence handling, not unfinished task prompts. |
| 22 | Open-question adjacency (TB-Add-3) | PASS | Open questions describe bounded historical uncertainty and documented recovery paths, not an unresolved user decision blocking execution. Missing complete worker output must remain blocked. No currently blocked checkbox requiring an unresolved decision was established. |
| 23 | Circular dependencies (TB-Add-4) | PASS | Traced preparation, cases, deck, research gate, external applicability, synthesis/cards, debate, ranking, synthesis gate, assembly, report gate, fidelity, anti-omission and completion. No circular prerequisite was found. Correction cycles are explicitly bounded control loops. |
| 24 | Oversized-item handling (TB-Add-5) | PASS | Individual producers/reviewers are separated. Cross-file correction workers are constrained by the explicit single-fixer rule rather than unbounded parallel editing. |
| 25 | Verification formatting (TB-Add-6) | PASS | All 103 items consistently use `**Verify:**`. No conflicting Acceptance Criteria list format appears. |
| 26 | Execution Context source areas (TB-Add-7) | PASS | The literal `**Source areas:**` line is absent: `tb-add-7-degraded-tolerated`. Additionally checked the actual Source Areas subsection: all four named areas reappear in item Context text. No prohibited file:line citation was found in the header block. |
| 27 | Context evidence binding (TB-Add-8) | FAIL | Mechanical Context-only scan found 92 fields without a citation or justified-absence comment. Independently checked representative failures against the live catalogue. Issue 2. |

## Gate Ordering and Authorization Findings

| Area | Verified result |
|---|---|
| Full-intensity research and synthesis review floors | Correct roles and two partitions per lens are encoded. |
| Serialized corrections | Reviews precede consolidation, one authorized fixer, two independent verifiers and a decision. Clean paths record no-fix-needed rather than inventing corrections. |
| Report review before source fidelity | Correct. The report decision precedes source mapping and fidelity review. |
| Fidelity before exhaustive anti-omission | Correct. Fidelity must actually PASS before anti-omission mapping and review. |
| Late corrections | Affected earlier PASS results must be invalidated and rerun; stale acceptance is expressly prohibited. |
| Additional `/task` phase gates | Calling-skill Stage B expressly provides these automatically in addition to skill-specific gates. Their appearance in task prose is not evidence of a fabricated run. |
| PRE and POST reflection | No-spec PRE skip and disabled POST are consistent with the BUILD request. No reflection run was fabricated. |
| Forbidden actions and preservation | Production changes, historical plan execution, commits, pushes, publication, archive/movement and intermediate deletion are prohibited. Final completion remains in place. |

## Summary

- Checks passed: **21 / 27**
- Checks failed: **6**, representing **3 distinct issues**
- Critical issues: **0**
- Important issues: **2**
- Minor issues: **1**
- Issues fixed in-place: **0**
- Report file written: **None**, following the report-write prohibition.

**Confidence:** Verified: 27/27 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 19 | Grep: 0 | Glob: 0 | Bash: 8

**Tool-engagement caveat:** Dedicated Read/Grep/Glob calls total 19, below the 27-check advisory minimum. This review therefore carries the required “tool-engagement minimum not met” flag. Bash calls performed targeted searches, filesystem checks, YAML parsing and item scans; they are not relabeled as dedicated Grep/Glob calls.

**Review-process limitation:** The initial template Read exceeded the requested focused-line budget. This did not authorize or cause task execution, source changes or report writes.

## Actions Taken

Read-only inspection only. Both Python inspections and YAML validation used UV. No agents were spawned, no coordination tools were used, and no historical task or adversarial debate was run.

## Recommended Action

Revise the reviewed task to resolve all three issues, then rerun structural validation before execution. The intended gate sequence is sound, but its literal input paths and mandatory evidence bindings are not execution-ready.

VERDICT: FAIL