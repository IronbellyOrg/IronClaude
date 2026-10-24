# QA Report - Specification Review - Routing and Design

**Topic:** sc:recommend routing refresh  
**Date:** 2026-10-24  
**Phase:** Independent specification review  
**Lens:** routing-and-design  
**Fix cycle:** 1  
**fix_authorization:** false

**Reviewed specification:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/SPEC-sc-recommend-refresh.md`

## Overall Verdict: FAIL

The specification establishes the right ordinary implementation policy and avoids unnecessary architecture. Two gaps remain: the full-spec entry point lacks an explicit ordinary-work alternative to its indirect MDTM pipeline, and several specialized routing changes have no corresponding behavioral acceptance case despite being assigned test IDs.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Ordinary planned implementation defaults to workflow/implement | PASS | FR-01 expressly removes file/session/spec-based MDTM escalation. |
| 2 | Every governing guide entry point applies the new MDTM threshold | FAIL | Finding R01: full-spec and `/roadmap` remain insufficiently specified. |
| 3 | Explicit commands and existing executor identity survive | PASS | FR-02 preserves managed workflow packages, existing MDTM execution and explicit implement semantics. |
| 4 | Direct-change limits and contained cleanup exception remain bounded | PASS | FR-02 preserves the existing five-edit/one-source-file rule and checkpoint/diff requirements. |
| 5 | Whole requested outcomes outrank generic phrases | PASS | FR-03/04 distinguish specialized reporting, documentation, testing and lifecycle outcomes. |
| 6 | Options and activation dependencies require actual interface evidence | PASS | FR-05 recognizes Usage syntax and self-contained commands while rejecting unsupported options. |
| 7 | Cached answers cannot retain another request's inputs or authority | PASS | FR-07 requires current-source verification and handoff reconstruction. |
| 8 | Native, cold and missing-guide behavior receive the same policy | PASS | FR-01/07/10 require consistent fallbacks without introducing classifier keys. |
| 9 | Installed/plugin availability is distinguished from checkout authority | PASS | FR-06/10 preserve actual-copy verification, missing-dependency limitations and custom-command exceptions. |
| 10 | Design avoids a duplicate registry or dependency framework | PASS | Sections 2 and 4 reuse the guide, cache schema and existing tests. |
| 11 | PR defaults, explicit lower ceilings and publication boundaries are preserved | PASS | FR-09 retains monitor 3 while requiring mutually exclusive lower-ceiling branches, origin/head safeguards and no recommendation execution. |
| 12 | Proposed regressions cover the newly specified routes | FAIL | Finding R02: several Appendix C assignments do not correspond to cases in Section 8. |

## Summary

- Checks passed: **10/12**
- Checks failed: **2**
- Critical issues: **0**
- Issues fixed in-place: **N/A**
- No command implementations, proposed tests, model evaluations or GitHub operations were executed.
- Read-only `git diff HEAD --name-only -- src plugins tests` returned no changed implementation files.

## Issues Found

### R01 - IMPORTANT - Explicitly gate full-spec's indirect MDTM planning route

**Specification location:** FR-01, especially lines 150-165.

**Supporting live sources:**

- `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:309`
- `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/roadmap/SKILL.md:8-10`

**Issue:** FR-01 explicitly changes level 4 and enumerates several follow-on routes, but its level-6 criterion only prevents automatic MDTM execution. It does not explicitly require replacing or conditioning the current full-spec route's automatic `/roadmap` planning step.

That distinction matters. The current full-spec row matches a **new component**, not just an exceptionally complex, long-running program, and asks for a full roadmap. The roadmap skill creates an MDTM task for roadmap generation and, on its full path, invokes task-builder for downstream phase tasks. Removing the final product-execution step does not remove that indirect escalation.

**Failure scenario:** A bounded new component needs reviewed PRD/TDD documents followed by ordinary implementation planning. An implementation can update level 4 and stop unauthorized execution while retaining full-spec's automatic full-roadmap/task-builder pipeline. The main user policy is then bypassed through a different guide entry point.

**Required fix:** Specify the level-6/full-spec branch explicitly:

1. Requested documents remain terminal deliverables when appropriate.
2. Ordinary subsequent implementation planning uses workflow/implement.
3. The existing MDTM roadmap pipeline remains available for explicit selection or qualifying exceptional workload needs.
4. Internal machinery owned by expressly requested document/artifact skills is not being redesigned.

Add a negative regression for an ordinary new component that needs reviewed documents but does not justify MDTM planning.

### R02 - IMPORTANT - Replace nominal test mappings with route-specific acceptance cases

**Specification locations:** Section 8.1, lines 670-686; Appendix C, including lines 867 and 886.

**Issue:** FR-04 introduces separate `cli-eval-create`, `cli-eval-run` and `release-boundary` routes, but Section 8 does not specify positive behavioral cases for those selections. Appendix C maps cli-eval to T20/T21 and release-split to T20/T22, while the corresponding T19-T22 group describes build packaging, tasklist ambiguity and explicit-mode preservation.

These are not tests of cliEval create versus run, or release-boundary assessment versus implementation planning. Similar broad mappings cannot demonstrate that specialized capabilities remain reachable.

**Failure scenario:** Recommendation continues routing cliEval suite authoring to generic planning or routes existing-suite supervision to ordinary application testing. Every explicitly described Section 8 case can still pass.

**Required fix:** Give each new route a concrete positive request, expected command/mode, stopping point and relevant negative competitor. Assign unambiguous case IDs and repair Appendix C mappings. At minimum, distinguish cliEval create/run and neutral release-split assessment. Separate deterministic text checks from recommendation-generation evaluations, without executing recommended commands.

## Actions Taken

No fixes authorized this round; findings reported only. No specification, analysis or source files were edited.

## Recommendations

Resolve R01 and R02 before approval, then repeat this lens against the revised requirements and acceptance mappings. No new routing engine, classifier vocabulary or specialized-command implementation changes are needed.

## Self-Audit

**(a) Reliance list**

None. No other reviewer's PASS verdict was inherited. Analyst reports were treated as research leads, not independent proof.

**(b) Independent semantic checks**

- Tried to falsify workflow-first consistency by tracing a route outside level 4. The full-spec to roadmap dependency exposed R01.
- Tried to falsify behavioral coverage by comparing new route requirements with their assigned test descriptions. CliEval and release-split mappings exposed R02.
- Challenged whether cache safety required new infrastructure. Mandatory consumer re-verification supports the narrower proposed design.
- Challenged whether requested deep review necessarily requires MDTM. The specification correctly distinguishes current coupled remediation behavior from separate ordinary planning.
- Challenged whether PR recommendations silently increase authority. The proposed conditional ceilings and conflict disclosure preserve that boundary.

## Confidence Gate

- **Confidence:** Verified: **12/12** | Unverifiable: **0** | Unchecked: **0** | Confidence: **100%**
- **Calculation:** `12 / (12 - 0) × 100`
- **Meaning:** Evidence coverage of the twelve review checks, not specification correctness or measured runtime reliability.
- **Tool engagement:** Read: **30** | Grep: **0** | Glob: **0** | Bash: **1**
- **Unchecked items:** None within the stated twelve-check lens.
- **Unverifiable items:** None required for these contract-level findings. Actual recommendation behavior and executor capacity were not tested or claimed.

## QA Complete

VERDICT: FAIL