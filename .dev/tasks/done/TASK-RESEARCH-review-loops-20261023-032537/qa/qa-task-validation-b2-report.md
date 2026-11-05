<!-- Verbatim agent return transcribed by main; source=/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-atask-structure-b2-b0e48d3057408b2c.jsonl:78; template=agent output format; producer report-write restriction respected. -->
# QA Report: Task Integrity, Self-Containment Lens

**Topic:** Repeated planning and implementation review failures  
**Date:** 2026-10-23  
**Phase:** task-integrity  
**Fix cycle:** N/A  
**Fix authorization:** false

**Task reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md`

**Delivery:** Complete report returned as text because developer instructions prohibit writing report files. Intended transcription destination: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-task-validation-b2-report.md`. That report file was not created by this reviewer.

## Overall Verdict: FAIL

## Items Reviewed

The review covers the seven self-containment checks and the live structural additions. Broader task-integrity checks belong to the separate structure/ordering review.

| # | Check | Applicability | Result | Evidence |
|---|---|---|---|---|
| 1 | All five self-contained prompt components | All 103 items | PASS | Full task read and mechanical enumeration found 103 Context, Action/Output and Verify fields. Every item also has an explicit completion condition. |
| 2 | No reliance on unstated previous-session context | All items | PASS | Inputs are identified through persistent files, task references or explicit source maps. Previously running analysts have named case assignments and output paths. Path defects are recorded separately below. |
| 3 | Concrete embedded agent prompts | All agent-spawning items | PASS | Reviewed producer, partition-reviewer, fixer, verifier and assembler items. They specify actual scope, expected content, output and checks rather than only directing workers to a template. |
| 4 | Specific, correctly resolved file paths | All items | **FAIL** | Multiple input lists omit their directory prefixes despite the package-root path contract. See issue 1. |
| 5 | Measurable verification criteria | All items | PASS | Checks specify counts, classifications, source engagement, artifact existence, binary verdicts and final-state verification rather than generic success assertions. |
| 6 | Individually scoped work, no invisible batch-agent count | Producer and reviewer items | PASS | Research and synthesis each enumerate ten initial reviewer assignments. Cases, hypothesis cards, report lenses and four-way fidelity/omission partitions have separate items. Conditional extra reviewers have explicit thresholds and outputs. |
| 7 | No unsupported findings used to authorize implementation | Research-only task | PASS | Historical unknowns must remain unknown. No production repair or execution of investigated plans is authorized. |
| 8 | Placeholder and title-only scan (TB-Add-1) | All items | PASS | Mechanical scan found no literal `TBD`, `TODO` or `FIXME` tokens in checklist items. All 103 contain substantive bodies. |
| 9 | Blocking-question adjacency (TB-Add-3) | Conditional | PASS | Open Questions document bounded evidence limitations and recovery procedures, not unanswered decisions that currently block execution. Conditional failures must remain unchecked. |
| 10 | Circular dependency detection (TB-Add-4) | Item dependencies | PASS | Read producer-to-consumer ordering through all seven phases. No mutually dependent checklist-item pair was identified. Bounded repair cycles are explicit gate procedures. |
| 11 | Oversized or multi-file work splitting (TB-Add-5) | Conditional | PASS | Multi-input synthesis and assembly produce one coherent artifact per producer item. The long debate item invokes one actual protocol; it does not conceal an unspecified batch of independent research producers. |
| 12 | Verification format consistency (TB-Add-6) | All items | PASS | All 103 items use the same `**Verify:**` prefix. No separate Acceptance Criteria list uses a conflicting format. |
| 13 | Execution Context source-area binding (TB-Add-7) | Degraded form | PASS | `tb-add-7-degraded-tolerated`: the block lacks the catalogue’s literal `**Source areas:**` field. Its differently formatted source-area heading is not treated as a failure. No specific file:line citations appear in the block. |
| 14 | Per-item Context evidence binding (TB-Add-8) | Contexts referencing implementation surfaces | **FAIL** | Items 5.11 and 6.9 reference executable protocol sources without a file:line citation or justified evidence-absence comment. See issue 2. |

**Live catalogue:** Dynamically extracted seven entries from the project agent definition’s bounded Structural Gate Additions section: TB-Add-1, TB-Add-3, TB-Add-4, TB-Add-5, TB-Add-6, TB-Add-7 and TB-Add-8. Observed source hash prefix: `a88d8203`.

## Summary

- Checks passed: **12 / 14**
- Checks failed: **2**
- Critical issues: **0**
- Important issues: **2**
- Minor issues: **0**
- Issues fixed in-place: **0**

**Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

This measures verification coverage, not correctness of the task.

**Tool engagement:** Read: 15 | Grep: 0 | Glob: 0 | Bash: 5

Bash calls performed targeted searches and read-only structural enumeration. No external research was needed. No unchecked or unverifiable checks remain within this assigned lens.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | Items 2.13, 3.1-3.10 and recurring synthesis/fidelity/omission input lists | Input paths lose their directory prefix. For example, item 2.13 names `research/01-session-ac2cd1fd.md` followed by bare `02-session-a9b88895.md` through `06-session-0690ee9f.md`. The task explicitly resolves every relative path from the package root, so those bare names do not designate the assigned files under `research/`. Similar lists omit `research/` from screening files and `synthesis/` from synthesis components. | Prefix every independently quoted input path with its actual package-relative directory. Check all lists, not just the first example. Keep the existing package-root path contract. |
| 2 | IMPORTANT | Items 5.11 and 6.9 | Context evidence binding is missing for protocol implementation surfaces. Item 5.11 names the installed adversarial command and skill; item 6.9 requires current workflow/implementation sources. Neither Context contains a file:line citation or an evidence-absence justification. The live structural rule requires one of those forms. | Add verified source-line citations to each affected Context, or a truthful `<!-- evidence-absence: ... -->` justification where exact lines cannot yet be bound. Do not fabricate future line numbers. |

**Primary task locations**

- Path-list example: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md:187`
- Protocol invocation Context: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md:307`
- Current-protocol review Context: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md:411`
- Governing evidence-binding rule: `/config/workspace/IronClaude/.claude/agents/rf-qa.md:357`

The mechanical scan found 92 Context fields without citation syntax, but that number is **not** reported as 92 violations: many reference only research documents. Issue 2 is confined to confirmed protocol-source contexts.

## Actions Taken

- Read the entire task, adjacent build request and research notes.
- Read the governing self-containment requirements and live structural catalogue.
- Enumerated all 103 items and checked their component fields, completion conditions, placeholders, phase distribution and abbreviated paths.
- Re-read the concrete defect locations before returning this verdict.
- Made no edits, spawned no agents and executed no task steps.

## Recommendations

Correct both issues and repeat the self-containment review. The no-spec PRE skip and disabled post-execution reflection gate are valid for this request; no code-diff audit or implementation work is required.

## QA Complete

VERDICT: FAIL