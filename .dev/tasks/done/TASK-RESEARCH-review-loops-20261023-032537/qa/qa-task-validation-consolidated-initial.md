# QA Report: Research Task Structural Validation

**Topic:** Research task file integrity
**Date:** 2026-10-23
**Phase:** task-integrity
**Fix cycle:** 1
**Governing template:** task-builder/SKILL.md A.10; rf-qa.md Output Format

## Overall Verdict: FAIL

Initial independent reports identify two shared Important categories and one template-section issue. No fix or passing verification is claimed yet.

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


## Summary

Two independent structural reports, both FAIL. Three deduplicated issues: two Important, one Minor. The complete Items Reviewed span above is copied verbatim from qa-task-validation-structure-report.md, not independently regraded here. The self-containment reviewer verifies12/14 checks; the broader structure reviewer verifies21/27 pass and6 failing rows mapping to3 issues. No task steps executed, no passing correction review yet.

## Issues Found

| Finding | Severity | Sources | Required correction and boundary |
|---|---|---|---|
|Directory prefixes missing from consumer input paths|IMPORTANT|Both structural reports; task items2.13,3.1-3.10,5.1onward, later fidelity/omission lists|Expand EVERY independent input path to its correct package-relative path. Preserve root-resolution contract, future producer destinations and actual installed refs. Do not merely patch first example.|
|Context evidence bindings missing|IMPORTANT|Both reports, with different breadth interpretation; structure reports92/103 unbound contexts, B2 confirms protocol contexts5.11/6.9|Ensure every applicable Context has verified source citation or truthful evidence-absence justification. For future outputs, explicitly say lines don't yet exist. Do not fabricate citations or change substantive research scope.|
|Required named post-completion section absent|MINOR|Structure report; Phase7 contains actual actions, Template02 named-section requirement|Read actual template and calling-skill anti-orphaning precedence. Add the named section INSIDE final Phase7 at an appropriate nested heading level, preserving all completion items in the final phase. A separate post-completion phase or moving actions outside Phase7 is forbidden by the calling skill. Record this precedence resolution; do not create a new authorization question or weaken completion gates.|

## Actions Taken

Preserved both full independent reports in this qa directory. Consolidated duplicates without dropping findings. Current producer output remains unaccepted pending one serialized task-file fixer and a fresh independent verification. No production source edits authorized.

## Recommendations

One rf-qa fix agent may edit ONLY this research task file and its task-integrity fix log (if its developer instructions permit report writing; otherwise return exact fix-log text). It must re-read real sources before edits, preserve103 items and all review floors, and leave statuses unchecked/ToDo. Then a fresh reviewer verifies the whole resulting task and all three issues. Keep the initial reports and this initial verdict history.

## QA Complete
Pending serialized correction and independent verification.
