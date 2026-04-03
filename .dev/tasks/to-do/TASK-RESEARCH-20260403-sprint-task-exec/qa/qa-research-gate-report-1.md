# QA Report — Research Gate (Partition 1 of 2)

**Topic:** Sprint Task Execution Pipeline Investigation
**Date:** 2026-04-03
**Phase:** research-gate
**Fix cycle:** N/A
**Assigned files:** 01, 02, 03, 04

---

## Overall Verdict: FAIL

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 14 | Grep: 7 | Glob: 12 | Bash: 0

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | All 4 assigned files exist with `Status: Complete` and Summary sections. Verified by Read of each file. |
| 2 | Evidence density | PASS (Dense) | Sampled 15+ claims across files. All file paths verified via Glob (12 checks, all found). Line numbers spot-checked: `_parse_phase_tasks` L1095, `execute_sprint` L1112, `_run_task_subprocess` L1053, `build_command` L71, `build_prompt` L123, `_TASK_HEADING_RE` L281, `IsolationLayers` L108, `setup_isolation` L152, hooks at L450/L787, `execute_phase_tasks` L912, `ANTI_INSTINCT_GATE` L1043, `analyze_unwired_callables` L314, `analyze_orphan_modules` L394, `analyze_registries` L554, `run_wiring_analysis` L674 in wiring_gate.py, `build_task_context` L245. All confirmed. >90% of claims have specific file paths and line numbers. Rating: Dense. |
| 3 | Scope coverage | PASS | Files 01-04 cover all key EXISTING_FILES for their assigned topics: sprint/executor.py, sprint/process.py, sprint/config.py, sprint/models.py, pipeline/process.py, pipeline/gates.py, pipeline/models.py, audit/wiring_gate.py, roadmap/gates.py, tasklist-protocol SKILL.md + templates + rules. Remaining EXISTING_FILES (pipeline/executor.py, pm_agent/*, execution/*, release docs, logging, commands) are scoped to files 05-08 (not in this partition). |
| 4 | Documentation cross-validation | FAIL | **No `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` tags found in any of the 4 research files.** Grep for these tags returned zero matches across the entire research directory. File 02 makes doc-sourced claims from SKILL.md Section 4.5 (task ID format mandate), Section 4.4 (task conversion), Section 4.6 (clarification tasks), and the phase template -- all verified against code and actual files but without formal tags. File 03 makes doc-sourced claims about `--bare` and `--print` flag behavior from CLI help text -- no tags. The researchers performed the verification work but failed to apply the required tagging convention. |
| 5 | Contradiction resolution | PASS | No contradictions found between files. File 01 (Path A = minimal prompt) and File 03 (Path B = rich prompt with skill governance) describe different execution paths, not conflicting claims about the same path. File 04's hook analysis is consistent with File 01's gap analysis of Path A. |
| 6 | Gap severity | FAIL | See Issues Found below. Multiple gaps identified across all 4 files, including 2 items requiring severity classification. All gaps must be resolved before synthesis per zero-tolerance policy. |
| 7 | Depth appropriateness (Deep) | PASS | File 01 traces a complete end-to-end data flow: `execute_sprint()` -> `_parse_phase_tasks()` -> `parse_tasklist()` -> Path A/B -> `_run_task_subprocess()` -> `ClaudeProcess.build_command()` -> subprocess launch. File 02 traces generation -> template -> regex -> path selection with empirical verification of 6 actual phase files. Both meet Deep tier requirements. |
| 8 | Integration point coverage | PASS | Key integration points documented: executor <-> config <-> models (File 01), SKILL.md <-> template <-> regex <-> executor (File 02), pipeline/process.py <-> env inheritance <-> CLAUDE.md <-> skills (File 03), executor hooks <-> wiring_gate <-> pipeline/gates <-> roadmap/gates (File 04). Cross-subsystem connections are explicit with file paths and function signatures. |
| 9 | Pattern documentation | PASS | Documented patterns: `__new__` bypass pattern (File 01), Path A/B divergence pattern (File 01), deterministic generation algorithm (File 02), auto-discovery governance inheritance (File 03), GateCriteria/SemanticCheck tiered validation pattern (File 04), hook extension pattern with 3 paths (File 04). Naming conventions (T<PP>.<TT>), architecture patterns, and error handling (vacuous pass, budget exhaustion) all covered. |
| 10 | Incremental writing compliance | PASS | Files show structured progressive investigation (entry point -> deeper traces -> gaps -> summary). While they could potentially be one-shotted, the narrow scope per file (single focused research question) makes this acceptable. Each file builds findings sequentially before summarizing. |

## Summary

- Checks passed: 8 / 10
- Checks failed: 2
- Critical issues: 0
- Important issues: 2
- Minor issues: 0
- Issues fixed in-place: 0 (not fix-authorized)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | All 4 research files | **Missing documentation cross-validation tags.** No `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` tags anywhere in the research files. File 02 makes 4+ doc-sourced claims from SKILL.md (Sections 4.4, 4.5, 4.6) and phase-template.md that were empirically verified against code and actual files but lack formal tags. File 03 makes 2+ doc-sourced claims about `--bare` and `--print` CLI flag behavior from help text that are untagged. The verification work was done but the tagging convention was not applied. | Add `[CODE-VERIFIED]` tags to all doc-sourced claims in Files 02 and 03 that were verified against code. Specifically: (a) File 02, Section 1 SKILL.md claims about T<PP>.<TT> format -> tag as `[CODE-VERIFIED]` citing regex at config.py:281. (b) File 02, Section 2 template claims -> tag as `[CODE-VERIFIED]` citing actual phase files in Section 6. (c) File 03, Section 1 claims about `--print` and `--bare` behavior -> tag as `[UNVERIFIED]` since these are from help text and cannot be code-verified within this codebase (Claude Code CLI is external). |
| 2 | IMPORTANT | Files 01, 03, 04 — Gaps and Questions sections | **Gaps listed but not severity-classified.** File 01 lists 5 "Critical Gaps" and 4 "Design Questions" -- the "Critical" label is applied but inconsistently (some are design questions, not blocking gaps). File 03 lists 6 gaps without severity classification (CRITICAL/IMPORTANT/MINOR). File 04 lists 6 gaps without severity classification. Only File 02's gaps are clearly minor/theoretical. Per research gate protocol, every gap must be classified as CRITICAL (blocks synthesis from producing accurate output), IMPORTANT (reduces quality), or MINOR (lower-priority improvement) so the orchestrator can triage remediation. | Classify every gap in Files 01, 03, and 04 with explicit severity labels: CRITICAL, IMPORTANT, or MINOR. Recommended classifications: **File 01**: Gap 1 (Path A prompt underspecified) = IMPORTANT (documented finding, not a research gap); Gap 2 (dead code) = IMPORTANT; Gap 3 (output file collision) = IMPORTANT; Gap 4 (__new__ bypass) = MINOR; Gap 5 (no lifecycle hooks) = MINOR. **File 03**: Gap 1 (dead isolation code) = IMPORTANT; Gap 2 (CLAUDE.md discovery with CLAUDE_WORK_DIR) = CRITICAL (synthesis cannot accurately describe worker governance without knowing this); Gap 3 (MCP server loading in --print mode) = IMPORTANT; Gap 4 (skill token cost) = MINOR; Gap 5 (model override) = MINOR; Gap 6 (agent teams) = MINOR. **File 04**: Gap 1 (anti-instinct no-op) = IMPORTANT; Gap 2 (wiring gate not task-specific) = IMPORTANT; Gap 3 (no remediation subprocess) = IMPORTANT; Gap 4 (no acceptance_criteria field) = IMPORTANT; Gap 5 (budget dependency) = MINOR; Gap 6 (extension point) = MINOR (this is a finding, not a gap). |

## Actions Taken

None — not authorized to fix.

## Recommendations

1. **Before proceeding to synthesis**: Both issues must be resolved. Issue 1 (missing tags) requires a gap-filling pass on Files 02 and 03 to add proper documentation cross-validation tags. Issue 2 (missing severity classifications) requires updating the Gaps sections of Files 01, 03, and 04 with CRITICAL/IMPORTANT/MINOR labels.

2. **File 03 Gap 2 is the most synthesis-critical finding**: The question of whether Claude Code resolves CLAUDE.md relative to `CLAUDE_WORK_DIR` or traverses upward to the git root fundamentally affects the accuracy of any synthesis about worker governance. This gap should be investigated (potentially via web research on Claude Code behavior) before synthesis begins.

3. [PARTITION NOTE: Cross-file checks limited to assigned subset (files 01-04). Full cross-file verification requires merging all partition reports. Files 05-08 were not examined.]

## QA Complete
