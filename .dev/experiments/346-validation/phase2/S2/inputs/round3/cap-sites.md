# Review-loop cap sites: classification

**Date**: 2026-11-02 · **Branch**: `fix/review-severity-rule` · **Input**: `.dev/review-severity-rule/capscan-raw.txt` (160 hits), inventory section 3, merged verdict B-02, B-03, B-07..B-11.
**Rule applied**: a review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalates to the user with the open blocking findings. Caps of 2 stay; caps of 3 or more drop to 2. `sc-implement-protocol` excluded.
**Canonical at-cap text**: "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings".
**Legend**: IN = must change; OUT = keep (reason given). "missed" = not in the raw scan, found by the extra greps. Every hit was opened at its line. Severity wording on the same lines ("ALL findings regardless of severity", "Open Questions" at-cap rules) belongs to inventory sections 2 and 3.1 and is not repeated here.

## 1. Agents (`src/superclaude/agents/`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `rf-analyst.md:74` | IN | "(max-3-cycles HALT-and-ask-user contract)"; "sha256 frozen at `51725c0f…`" | "(max-2-cycles HALT-and-ask-user contract)"; re-pin the sha256 to the new `rf-team-lead.md:462` line. Keep the closed vocabulary `gap-fill-round-3` (identifier, not a cap). | `tests/audit/test_dnsp_all_agents_fail_bypass.py` (sha + token) |
| `rf-qa-qualitative.md:83` | IN | same DNSP clause as rf-analyst:74 | same as rf-analyst:74 | same |
| `rf-qa-qualitative.md:797` | IN | "Maximum 3 fix cycles. After 3 cycles, if issues remain, HALT execution and ask the user for guidance." | "Maximum 2 fix cycles. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." (rest of line kept) | none |
| `rf-qa-qualitative.md:827` | IN | "**Fix cycle:** [1 / 2 / 3 / N/A]" | "**Fix cycle:** [1 / 2 / N/A]" | none |
| `rf-qa-qualitative.md:940` | OUT | "Maximum 3 additional rounds." | confidence-raising rounds inside one review | — |
| `rf-qa-qualitative.md:941` | OUT | "After 3 rounds still below 95%" | confidence-raising rounds inside one review | — |
| `rf-qa-qualitative.md:982` | IN | "10. **Maximum 3 fix cycles** — After 3 rounds of fixes without resolution, HALT and escalate to the user." | "10. **Maximum 2 fix cycles** — After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | `tests/audit/test_severity_floor_unweakened.py` BASELINE_BLOCK_SHA (hashes the Critical Rules block incl. rule 10; re-pin) |
| `rf-qa.md:82` | IN | same DNSP clause as rf-analyst:74 | same as rf-analyst:74 | `test_dnsp_all_agents_fail_bypass.py` |
| `rf-qa.md:390` | IN | "Maximum 3 fix cycles. After 3 cycles, if issues remain, HALT execution and ask the user for guidance." | as rf-qa-qualitative:797 | none |
| `rf-qa.md:393` | IN | "strengthens this 3-fix-cycle" | "strengthens this 2-fix-cycle" | none |
| `rf-qa.md:395` (1st) | IN | "the existing 3-fix-cycle above" | "the existing 2-fix-cycle above" | none |
| `rf-qa.md:395` (2nd) | IN | "BEFORE the existing 3-cycle cap fires" | "BEFORE the existing 2-cycle cap fires" | none |
| `rf-qa.md:403` | IN | "slow convergence (e.g., `\|F\|=5,4`) continues to the 3-cycle cap" | "... continues to the 2-cycle cap" (the 5,4 example is still two cycles) | none |
| `rf-qa.md:406` | IN | "The existing 3-cycle hard cap at `rf-team-lead's Fix Cycles rule`" | "The existing 2-cycle hard cap ..." | none |
| `rf-qa.md:418` | IN | "[1 / 2 / 3 / N/A]" | "[1 / 2 / N/A]" | none |
| `rf-qa.md:498` | OUT | "Maximum 3 additional rounds." | confidence-raising rounds inside one review | — |
| `rf-qa.md:499` | OUT | "After 3 rounds still below 95%" | confidence-raising rounds inside one review | — |
| `rf-qa.md:537` | IN | "10. **Maximum 3 fix cycles** — After 3 rounds of fixes without resolution, HALT and escalate to the user." | as rf-qa-qualitative:982 | `tests/skills/test_task_builder_merge.py:435` (comment "3-fix-cycle" only) |
| `rf-team-lead.md:462` | IN | "(max 3 cycles per phase). If max cycles exhausted, HALT and ask user" | "(max 2 cycles per phase). ..." (rest kept; B-11 FIX-trigger wording is a separate severity edit on the same line) | `tests/audit/test_dnsp_all_agents_fail_bypass.py:14,32,77,395-399,640`; fixture `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt`; sha `51725c0f…` also in rf-qa:82, rf-qa-qualitative:83, rf-analyst:74, `task-builder/SKILL.md:901` |
| `rf-task-builder.md:383` (missed) | IN | "\| research-gate \| 3 \| HALT and escalate \|" | "\| research-gate \| 2 \| ..." | none |
| `rf-task-builder.md:385` (missed) | IN | "\| report-validation \| 3 \| ..." | "\| report-validation \| 2 \| ..." | none |
| `rf-task-builder.md:387` (missed) | IN | "\| Any qualitative gate \| 3 \| ..." | "\| Any qualitative gate \| 2 \| ..." | none |

## 2. Python CLI (`src/superclaude/cli/`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `cli_portify/convergence.py:70` | OUT | `return total / 4.0` | mean of 4 scores | — |
| `cli_portify/convergence.py:128` | OUT | `return total / 4.0` | mean of 4 scores | — |
| `cli_portify/convergence.py:149` | IN | docstring `ConvergenceEngine(max_iterations=3)` / `for i in range(1, 4):` | `max_iterations=2` / `range(1, 3)` | none |
| `cli_portify/convergence.py:165` (missed) | IN | `max_iterations: int = 3,` | `max_iterations: int = 2,`. Count: one iteration = one submitted review result after an incorporation pass (ESCALATED at `iteration >= max`), matching the protocol's REVIEWING→INCORPORATING→SCORING; 2 gives at most 2 fix passes. | `tests/cli_portify/test_convergence.py:78-86` `test_default_max_iterations_is_3` (pins the default; rewrite for 2). Explicit-value tests unaffected: `test_convergence.py:29,52,110,115,121,127,135`, `integration/test_orchestration.py:327,337,360` |
| `cli_portify/steps/panel_review.py:95` | OUT | `return total / 4.0` | mean of 4 scores | — |
| `cli_portify/steps/panel_review.py:352` | IN | `engine = ConvergenceEngine(max_iterations=3)` | `max_iterations=2` (latent today: only iteration=1 is submitted, merged verdict M-01) | none pins it |
| `cli_portify/commands.py:100-101` (missed) | IN | `default=3,` / help "Maximum convergence iterations for panel-review (default: 3)" | `default=2,` / "(default: 2)". User may still raise it (same as pr-submit `--max-rounds`). | none pins the default |
| `cli_portify/config.py:53` (missed) | IN | `max_convergence: int = 3,` | `= 2` | none (tests pass explicit 3: `integration/test_orchestration.py:84,442`) |
| `cli_portify/models.py:583` (missed) | IN | `max_convergence: int = 3` | `= 2` | none |
| `cli_portify/prompts.py:68` (missed) | IN | `max_convergence: int = 3` | `= 2` | none (`test_prompts.py:32` explicit) |
| `cli_portify/resume.py:136` (missed) | IN | `suggest_budget(..., max_convergence: int = 3)` | `= 2` | none (`test_resume.py:139,147` explicit). `failures.py:240` "+2" resume suggestion is a user-raise path: keep. |
| `prd/models.py:203` | IN | `max_research_fix_cycles: int = 3` | `= 2`. Count: `executor.py:1157` runs `range(max_cycles + 1)` = initial QA + N fix cycles, so 2 → 3 QA runs. | none pins the default; `tests/cli/prd/test_integration.py:263` passes explicit `max_cycles=3` (unaffected; may lower for consistency) |
| `audit/batch_decomposer.py:141` | OUT | `// 4` | token estimate | — |
| `audit/escalation.py:134` | OUT | `// 4` | token estimate | — |
| `roadmap/semantic_layer.py:68` | OUT | `raw / 3.0` | score normalization | — |
| `init_lite.py:12` | OUT | `ceil(bytes / 4)` | token estimate | — |
| `init_lite.py:47` | OUT | `ceil(size_bytes / 4)` | token estimate | — |
| `init_lite.py:50` | OUT | `(size_bytes + 3) // 4` | token estimate | — |
| `eval/suites/adversarial_merge_consistency.yaml:94` | OUT | "5 login attempts / 5 minutes" | eval-suite fixture text | — |
| `roadmap/convergence.py:440`, `roadmap/executor.py:1725` (checked) | OUT | `max_runs: int = 3` / `max_runs=3` | counts checker runs (reviews); remediation runs only between runs (`run_idx < max_runs - 1`), so 3 runs = 2 fix cycles, already at the cap; halts `passed=False` | — |
| `sprint/recovery.py:412` (checked) | OUT | `max_attempts = 3` | reclaimer livelock bound, not a review loop | — |
| `reflect/config.py:260` (checked) | OUT | `max_fix_iterations: int = 2` | already 2 | — |

## 3. Installed rule doc (`src/superclaude/rules/core/`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `ib_agent_core.md:633` | IN | "Maximum 5 correction attempts per batch" | "Maximum 2 correction attempts per batch" (QA-fail → correction → re-QA loop, B-10) | none |
| `ib_agent_core.md:913` | IN | "Manual intervention needed after 3 attempts" | "... after 2 attempts" (today contradicts line 633's 5) | none |
| `ib_agent_core.md:933` (missed) | IN | "`MAX_CORRECTION_ATTEMPTS` (default: 5)" | "(default: 2)". Note: documents `automated_qa_workflow.sh`, which is not in this repo, so the edit changes the doc only. | none |

## 4. Skill: operational-guide (`src/superclaude/skills/operational-guide/SKILL.md`)

No tests pin these lines (markdown).

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `:427` | IN | "Verification round (2 agents). Max 3 fix cycles." | "... Max 2 fix cycles." | none |
| `:439` | IN | "= 5 agents. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:447` | IN | "= 11 agents. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:514` | IN | "run serialized fix cycle (max 3 cycles)" | "(max 2 cycles)"; "max 2 gap-fill rounds" stays | none |
| `:571` | IN | "repeat Step 6.4 (max 3 cycles total). After 3 cycles, HALT: log remaining issues in Task Log, present to user." | "repeat Step 6.4 (max 2 cycles total). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log remaining issues in Task Log." | none |
| `:1349` | IN | "Max fix cycles: 3 for research, 2 for synthesis, 3 for final document, 2 for source-document fidelity. After max fix cycles, HALT and ask user for guidance." | "Max fix cycles: 2 for research, 2 for synthesis, 2 for final document, 2 for source-document fidelity. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." (B-02) | none |
| `:1371` | IN | "phase-gate QA failing 3 fix cycles" | "phase-gate QA failing 2 fix cycles" (B-07) | none |

## 5. Skill: readme (`src/superclaude/skills/readme/SKILL.md`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `:188` | IN | "apply fixes via serialized protocol (max 3 cycles)" | "(max 2 cycles)"; gap-fill 2 stays | none |
| `:191` | IN | "(max 3 fix cycles per gate)" | "(max 2 fix cycles per gate)" | none |
| `:451` | IN | "= 5 agents. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:460` | IN | "= 11 agents. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:464` | IN | "2 rf-qa fidelity agents. HALT if unresolved after 3 cycles." | "2 rf-qa fidelity agents. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `:546` | IN | "Maximum 3 fix cycles for Sub-flow A." | "Maximum 2 fix cycles for Sub-flow A." | none |
| `:553` | IN | "Sub-flow A (max 3 fix cycles)" | "Sub-flow A (max 2 fix cycles)" | none |
| `:602` | IN | "(max 3 cycles). If unresolved after 3 cycles, HALT and present findings to user." | "(max 2 cycles). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `:607` | IN | "2 verification agents, max 3 cycles)" | "max 2 cycles)" | none |
| `:608` | IN | "If unresolved after 3 cycles, HALT and present findings to user." | "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `:1690` (1st) | IN | "Maximum 3 fix cycles for the fidelity gate." | "Maximum 2 fix cycles for the fidelity gate." | none |
| `:1690` (2nd) | IN | "After 3 cycles, HALT and escalate to user." | "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `:1715` (1st) | IN | same as :1690 (1st) | same | none |
| `:1715` (2nd) | IN | same as :1690 (2nd) | same | none |
| `:2034` | IN | "Max fix cycles: 3 for research gate, 2 for synthesis gate, 3 for final document gate, 3 for fidelity gate. After max fix cycles, HALT and ask user for guidance." | "Max fix cycles: 2 for research gate, 2 for synthesis gate, 2 for final document gate, 2 for fidelity gate. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." (B-02) | none |
| `:2058` | IN | "phase-gate QA failing 3 fix cycles" | "failing 2 fix cycles" (B-07) | none |

## 6. Skill: roadmap (`src/superclaude/skills/roadmap/SKILL.md`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `:435` | IN | "= 17-19 agents. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:440` | IN | "detail-preservation rf-qa-qualitative). Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:554` | IN (judgment) | "Sentinel gate — ... Any found = FAIL. Fix cycle (max 3): identify unpopulated sections, re-populate, re-scan." | "Fix cycle (max 2): ...". Mechanical placeholder scan, but it is a FAIL gate with a fix/re-scan loop inside the QA stage. | none |
| `:563` | IN | "repeat fix-verify cycle (max 3 total cycles). HALT if unresolved after 3 cycles." | "(max 2 total cycles). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `:577` | IN | "... to its originating coverage agent). Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:2073` (1st) | IN | "Stage 1 lens QA: max 3 fix cycles." | "Stage 1 lens QA: max 2 fix cycles." | none |
| `:2073` (2nd) | IN | "Stage 2 coverage: max 3 fix cycles." | "Stage 2 coverage: max 2 fix cycles." (fidelity/Stage 3/Stage 4 already 2) | none |
| `:2587` | IN | "phase-gate QA failing 3 fix cycles" | "failing 2 fix cycles" (B-07) | none |

## 7. Skill: task-builder (`src/superclaude/skills/task-builder/SKILL.md`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `:204` | IN | "with gap-fill cycle if needed (max 3 rounds) (A.8)" | "(max 2 rounds)". A.8 re-runs analyst + QA after each gap-fill (`:871`), so it is a review loop, not a bare researcher retry. | none |
| `:872` | IN | "4. **Maximum 3 gap-fill rounds**" | "4. **Maximum 2 gap-fill rounds**" | none |
| `:873` | IN | "5. After 3 rounds, proceed with remaining gaps as Open Questions in the task file" | "5. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" (also inventory 3.1) | none |
| `:1147` | IN | "6. Max 3 fix-verify cycles." | "6. Max 2 fix-verify cycles." | none |
| `:1275` (1st, "A.10 / A.10.5") | OUT | "the A.10 / A.10.5 fix cycles" | section names, no number | — |
| `:1275` (2nd) | IN | "rf-qa's 3-fix-cycle in rf-qa.md" | "rf-qa's 2-fix-cycle in rf-qa.md" | `tests/skills/test_task_builder_merge.py` checks only "Retry Monotonicity Protocol" here |
| `:1275` (3rd) | IN | "the existing 3-cycle hard cap at `rf-team-lead's Fix Cycles rule`" | "the existing 2-cycle hard cap ..." | none |
| `:1282` | OUT | "research-gate gap-fill, A.10 fix cycle, A.10.5 fix cycle, and any per-gate cycles" | independent-counter prose, no number | — |
| `:1310` | IN | "(research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3 -- ... with the global 3-cycle backstop" | "(research-gate=2, synthesis-gate=2, report-validation=2, task-integrity=2, qualitative=2 -- ... with the global 2-cycle backstop" | none |
| `:1412` | IN | "Max 3 fix-verify cycles." | "Max 2 fix-verify cycles." | none |
| `:1419` | IN | "**FAIL with unfixable issues after 3 fix-verify cycles**" | "**FAIL with unfixable issues after 2 fix-verify cycles (3 reviews)**" | none |
| `:1420` | IN | "counts against the A.10 fix-cycle budget, max 3 cycles" | "max 2 cycles" (its "Open Question" at-cap rule is inventory 3.1) | none |
| `:1471` | IN | "(independent of A.10's 3-cycle budget)" | "(independent of A.10's 2-cycle budget)"; A.10.25's own cap of 1 stays | none |
| `:2369` | IN | "phase-gate QA failing 3 fix cycles" | "failing 2 fix cycles" (B-07) | none |
| `:901` (dependent, not a cap) | — | "sha256 frozen at `51725c0f…`" | re-pin to the new sha of `rf-team-lead.md:462` | — |

## 8. Skill: task (`src/superclaude/skills/task/SKILL.md`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `:120` | IN | "(2) a phase-gate QA has failed 3 fix cycles" | "(2) a phase-gate QA has failed 2 fix cycles" (B-07) | none |
| `:254` (1st) | IN | "Maximum 3 fix cycles total (per I16 (MDTM template rule: maximum 3 fix-verify cycles per gate)6)." | "Maximum 2 fix cycles total (per I16 (MDTM template rule: maximum 2 fix-verify cycles per gate))." (drops the stray "6") | none |
| `:254` (2nd) | IN | "After 3 failed cycles: HALT execution — log all remaining issues ..." | "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings — log all remaining issues ..." (B-08) | none |
| `:271` | OUT | "Sections 1-7 / 8-14 / 15-21 / 22-28" | section ranges | — |
| `:336` | IN | "then a verification round. Maximum 3 fix cycles." | "Maximum 2 fix cycles." | none |
| `:366` | IN | "Maximum 3 fix cycles total per gate." | "Maximum 2 fix cycles total per gate." | none |
| `:368` | IN | "6. **Escalation:** After 3 failed cycles, HALT — log all remaining issues in the Task Log, present findings to the user, and ask for guidance." | "6. **Escalation:** After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log all remaining issues in the Task Log." (B-08) | none |
| `:405` | IN | "Maximum 3 fix cycles (per I16), then HALT and escalate to user." | "Maximum 2 fix cycles (per I16). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `:477` | IN | "[1 / 2 / 3 / N/A]" | "[1 / 2 / N/A]" | none |
| `:616` | IN | "phase-gate QA failing 3 fix cycles" | "failing 2 fix cycles" (B-07) | none |

## 9. Skill: tech-reference (`src/superclaude/skills/tech-reference/SKILL.md`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `:177` (missed) | IN | "gap-fill cycles if needed (max 3)" (Phase 3 QA gate) | "(max 2)" | none |
| `:412` | IN | "2-agent verification round ... Max 3 cycles." | "Max 2 cycles." | none |
| `:415` | IN | "then 2-agent verification round (max 3 cycles)" | "(max 2 cycles)" | none |
| `:424` | IN | "= 5 agents. Max 3 gap-fill cycles." (Gate 1 full; same loop as `:512`) | "Max 2 gap-fill cycles." | none |
| `:428` | IN | "= 5 agents. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:432` | IN | "= 11-15 agents. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:436` | IN | "8 at >2000. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:512` | IN | "Maximum 3 cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed." | "Maximum 2 cycles — after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log all remaining issues in Task Log." (B-08) | none |
| `:529` | IN | "Maximum 3 fix cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present findings to user, ask for guidance." | "Maximum 2 fix cycles — after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log all remaining issues in Task Log." (B-08) | none |
| `:534` | IN | "(max 3 total cycles). After 3 cycles, HALT: log remaining issues, present to user, ask for guidance." | "(max 2 total cycles). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `:535` | IN | "(max 3 fix cycles). HALT after max cycles exceeded." | "(max 2 fix cycles). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `:1307` | IN | "Maximum 3 fix cycles per gate — after 3 failed cycles, HALT execution and ask the user for guidance." | "Maximum 2 fix cycles per gate — after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." (B-08) | none |
| `:1327` | IN | "phase-gate QA failing 3 fix cycles" | "failing 2 fix cycles" (B-07) | none |

## 10. Skill: tech-research (`src/superclaude/skills/tech-research/SKILL.md`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `:398` | IN | "= 5 agents. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:406` | IN | "= 9-13 agents. Max 3 fix cycles." | "Max 2 fix cycles." | none |
| `:486` | IN | "repeat Step 3.2 (max 3 cycles total), then HALT — log issues in Task Log, present to user" | "repeat Step 3.2 (max 2 cycles total). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log issues in Task Log" | none |
| `:551` | IN | "repeat Steps 6.5-6.6 (max 3 cycles), then HALT if unresolved." | "repeat Steps 6.5-6.6 (max 2 cycles). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `:1643` | IN | "phase-gate QA failing 3 fix cycles" | "failing 2 fix cycles" (B-07) | none |

## 11. Skills: prd / tdd build-request templates

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `skills/prd/refs/build-request-template.md:130` | IN | "Maximum 3 fix cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present findings to user." | "Maximum 2 fix cycles — after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log all remaining issues in Task Log." (B-08; `:149` already 2) | none |
| `skills/tdd/refs/build-request-template.md:125` | IN | "Maximum 3 fix cycles — after 3 failed cycles, HALT execution: log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance on how to proceed." | "Maximum 2 fix cycles — after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log all remaining issues in Task Log." (rest kept; `:144` already 2) | none |

## 12. Skill: sc-cli-portify-protocol

Count note: each iteration is REVIEWING → INCORPORATING (fix) → SCORING, so N iterations = N fix passes; 2 gives at most 2 fix cycles. The ESCALATED state already escalates the open CRITICALs to the user.

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `SKILL.md:336` | OUT | "`(clarity + completeness + testability + consistency) / 4`" | score mean | — |
| `SKILL.md:355` (missed) | IN | "`ESCALATED` — Terminal state: 3 iterations exhausted" | "2 iterations exhausted" | none |
| `SKILL.md:363` (missed) | IN | "SCORING → REVIEWING (unaddressed CRITICALs remain, iteration < 3)" | "iteration < 2" | none |
| `SKILL.md:364` (missed) | IN | "SCORING → ESCALATED (unaddressed CRITICALs remain, iteration >= 3)" | "iteration >= 2" | none |
| `SKILL.md:367` | IN | "Hard cap: `max_iterations = 3` (SC-008)." | "Hard cap: `max_iterations = 2` (SC-008)." | none |
| `SKILL.md:374` (missed) | IN | "**ESCALATED**: `status: partial` — 3 iterations exhausted with unaddressed CRITICALs remaining." | "2 iterations exhausted ..." | none |
| `SKILL.md:534` (missed) | IN | "`convergence_exhausted` \| Maximum convergence iterations (3) reached" | "Maximum convergence iterations (2) reached" | none |
| `decisions.yaml:121` | IN | "Max 3 iterations." | "Max 2 iterations." | none |
| `decisions.yaml:123` (missed) | IN | "ESCALATED = 3 iterations exhausted" | "ESCALATED = 2 iterations exhausted" | none |

## 13. Templates: documents (`src/superclaude/templates/documents/`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `agent_template_qa.md:184` | IN | "Maximum 3 fix cycles. After 3 cycles, if issues remain, HALT execution and ask the user for guidance." | "Maximum 2 fix cycles. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." (rest kept) | none |
| `agent_template_qa.md:210` | IN | "[1 / 2 / 3 / N/A]" | "[1 / 2 / N/A]" | none |
| `agent_template_qa.md:292` | OUT | "Maximum 3 additional rounds." | confidence-raising rounds inside one review | — |
| `agent_template_qa.md:293` | OUT | "After 3 rounds still below 95%" | confidence-raising rounds inside one review | — |
| `agent_template_qa.md:320` | IN | "template position N+3 = rf-qa.md rule 10 (max 3 fix cycles)" | "(max 2 fix cycles)" | none |
| `agent_template_qa.md:335` | IN | "N+3. **Maximum 3 fix cycles** — After 3 rounds of fixes without resolution, HALT and escalate to the user." | "N+3. **Maximum 2 fix cycles** — After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `skill_template.md:427` | IN | "Gate 1 ... in parallel, max 3 fix cycles, partitioning >6 files." | "max 2 fix cycles" (`:428` already 2) | none |

## 14. Templates: modularization-template-review (`src/superclaude/templates/modularization-template-review/`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `qa-consolidated-findings_template.md:102` | IN | "**Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}} / 3" | "/ 2" | none |
| `qa-cross-source-contradictions_template.md:101` | IN | same | "/ 2" | none |
| `qa-fix-summary_template.md:96` | IN | "Fix cycle: {{RF_PLACEHOLDER:FIX_CYCLE}} / 3" | "/ 2" | none |
| `qa-fix-summary_template.md:105` (1st) | IN | "Feeds the max-3-cycle escalation" | "max-2-cycle escalation" | none |
| `qa-fix-summary_template.md:105` (2nd) | IN | "unfixed at Fix cycle 3/3" | "unfixed at Fix cycle 2/2" | none |
| `qa-research-depth_report_template.md:105` | IN | "/ 3" | "/ 2" | none |
| `qa-research-evidence_report_template.md:100` | IN | "/ 3" | "/ 2" | none |
| `qa-research-gap_report_template.md:103` | IN | "/ 3" | "/ 2" | none |
| `qa-source-fidelity_template.md:95` | IN | "/ 3" | "/ 2" | none |
| `qa-task-validation-b2_report_template.md:101` | IN | "/ 3" | "/ 2" | none |
| `qa-task-validation-structure_report_template.md:104` | IN | "/ 3" | "/ 2" | none |

## 15. Templates: MDTM workflow (`src/superclaude/templates/workflow/`)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `01_mdtm_template_generic_task.md:649` (missed) | IN | "\| research-gate \| 3 \| HALT and escalate to user \|" | "\| research-gate \| 2 \| ..." (B-02 cell form) | none |
| `01_mdtm_template_generic_task.md:651` (missed) | IN | "\| report-validation \| 3 \| ..." | "\| 2 \|" | none |
| `01_mdtm_template_generic_task.md:653` (missed) | IN | "\| Any qualitative gate \| 3 \| ..." | "\| 2 \|" | none |
| `01_mdtm_template_generic_task.md:787` | IN | "Per I16 (2-3 per gate)" | "Per I16 (2 per gate)" (B-09) | none |
| `02_mdtm_template_complex_task.md:662` (missed) | IN | "\| research-gate \| 3 \| ..." | "\| 2 \|" | none |
| `02_mdtm_template_complex_task.md:664` (missed) | IN | "\| report-validation \| 3 \| ..." | "\| 2 \|" | none |
| `02_mdtm_template_complex_task.md:666` (missed) | IN | "\| Any qualitative gate \| 3 \| ..." | "\| 2 \|" | none |
| `02_mdtm_template_complex_task.md:667` (missed) | IN | "\| source-fidelity \| 3 \| ..." | "\| 2 \|" | none |
| `02_mdtm_template_complex_task.md:753` | IN | "Maximum cycles per I16 gate-type table (3 for most gates, 2 for synthesis-gate and task-integrity). If issues remain after 3 cycles, HALT and escalate to user." | "Maximum cycles per I16 gate-type table (2 for every gate). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `02_mdtm_template_complex_task.md:804` | IN | "Per I16 (2-3 per gate)" | "Per I16 (2 per gate)" (B-09) | none |
| `02_mdtm_template_complex_task.md:1090` | IN | "(3 for most gates, 2 for synthesis-gate and task-integrity) (per I16). If issues remain after 3 cycles, HALT and escalate to user." | "(2 for every gate) (per I16). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings." | none |
| `02_mdtm_template_complex_task.md:1119` | IN | "Same cycle control as M3 Step 8 (max 3 cycles, then HALT)." | "Same cycle control as M3 Step 8 (max 2 cycles; after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings)." | none |

Not changed: 01:803/812/938 and 02 lite/standard rows (caps 1 and 2); 02:1043 "up to the max cycles defined in I16" (no number); 02:708-711, 735-737 (agent counts).

## 16. Other raw hits (all OUT)

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `plugins/superclaude/commands/reflect.md:157` | OUT | "UC-2 §6.1 step 5 / 5.5" | section reference | — |
| `plugins/superclaude/skills/confidence-check/confidence.ts:180` | OUT | "// 3. Verify no helper modules ..." | numbered comment | — |
| `plugins/superclaude/skills/confidence-check/confidence.ts:198` | OUT | "// 3. Check not reinventing ..." | numbered comment | — |
| `plugins/superclaude/skills/confidence-check/confidence.ts:216` | OUT | "// 3. Verify approach matches ..." | numbered comment | — |
| `plugins/superclaude/skills/confidence-check/confidence.ts:234` | OUT | "// 3. Confirm fix aligns ..." | numbered comment | — |
| `src/superclaude/commands/init-lite.md:40` | OUT | "`ceil(bytes / 4)`" | token estimate | — |
| `src/superclaude/commands/init-lite.md:86` | OUT | "`ceil(bytes / 4)`" | token estimate | — |
| `src/superclaude/commands/reflect.md:166` | OUT | "§6.1 step 5 / 5.5" | section reference | — |
| `src/superclaude/hooks/scripts/freshness-session-start.sh:27` | OUT | "23.8k lines / 5.4 MB" | file-size note | — |
| `skills/sc-auggie-review-protocol/refs/severity-rubric.md:3` | OUT | "After Wave 3 grounding completes" | wave name | — |
| `skills/sc-init-lite-protocol/SKILL.md:50` | OUT | "`ceil(bytes / 4)`" | token estimate | — |
| `skills/sc-pr-submit-protocol/refs/state-machine.md:165` | OUT | "`round_counter < max_rounds`" | `/sc:pr-submit --max-rounds` (default 2, user may raise) | — |
| `skills/sc-reflect-protocol/SKILL.md:188` | OUT | "§6.1 step 5 / 5.5" | section reference | — |
| `skills/sc-reflect-protocol/refs/coverage-mapping.md:186` | OUT | "§6.1 step 5 / 5.5" | section reference | — |
| `skills/sc-reflect-protocol/refs/deviation-taxonomy.md:102` | OUT | "§6.1 step 5 / 5.5" | section reference | — |
| `skills/sc-reflect-protocol/refs/ops-integration.md:126` | OUT | "§6.1 step 5 / 5.5" | section reference | — |
| `skills/sc-reflect-protocol/refs/reflection-rubric.md:127` | OUT | "§6.1 step 5 / 5.5" | section reference | — |
| `skills/sc-roadmap-protocol/refs/scoring.md:79` | OUT | "`min(depth / 8, 1.0)`" | scoring rubric | — |
| `skills/sc-roadmap-protocol/refs/scoring.md:80` | OUT | "`min(domains / 5, 1.0)`" | scoring rubric | — |
| `skills/sc-roadmap-protocol/refs/scoring.md:135` | OUT | "`min(depth / 8, 1.0)`" | scoring rubric | — |
| `skills/sc-roadmap-protocol/refs/scoring.md:136` | OUT | "`min(domains / 7, 1.0)`" | scoring rubric | — |
| `skills/sc-tasklist-protocol/SKILL.md:1660` | OUT | "`ceil(n_tasks / 5)`" | size scoring | — |
| `skills/sc-tasklist-protocol/SKILL.md:1661` | OUT | "`ceil(n_R / 5)`" | size scoring | — |
| `skills/sc-troubleshoot-protocol/SKILL.md:86` | OUT | "S1.6.4 precedence / 3-round cap / A8" | diagnosability instrumentation-round cap (`:322`), not a review/fix loop | — |
| `skills/sc-troubleshoot-protocol/refs/primitive-differential.md:28` | OUT | "38 core attempts plus 3 optional attempts" | probe-pack row counts | — |
| `skills/sc-validate-roadmap-protocol/SKILL.md:52` | OUT | "Phase 0 / 6" | phase names | — |

## 17. Extra greps: checked and kept (not in the raw scan)

Greps run over `src/superclaude` and `plugins/superclaude` (sc-implement-protocol excluded): "failing 3", "failed 3", "3 rounds", "three cycles", "three rounds", "3 attempts", "5 attempts", plus "3-cycle", "max-3", "3 iterations", "Max fix cycles: 3", "\| 3 \|" cells, `FIX_CYCLE}} / 3`, Python `max_*… = 3+`, and "repeat until / until PASS". All 8 B-07 "failing/failed 3 fix cycles" sites and all 6 B-08 "after 3 failed cycles" sites were already in the raw scan (rows above). No twins of any IN file exist under `plugins/superclaude/`.

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `skills/sc-cli-eval-protocol/SKILL.md:204`, `refs/create-pipeline.md:50` | OUT (flag) | "Max 3 fix loops, then report blocked" | schema-loader (`eval describe`) fix loop, a mechanical validator in the eval pipeline, not a review. Ask the user if they want it at 2 too. | — |
| `skills/sc-roadmap-protocol/SKILL.md:372` | OUT | "`--depth deep` → 3 rounds" | adversarial debate rounds | — |
| `skills/sc-troubleshoot-protocol/SKILL.md:322, 678`, `refs/report-template.md:214`, `refs/diagnosability-audit.md:345` | OUT | "3-round diagnosability cap" | instrumentation rounds, not review/fix | — |
| `plugins/superclaude/core/RESEARCH_CONFIG.md:226` | OUT | "iterations: 3" (deep research) | research iterations | — |
| `cli/eval/suites/frontier_vs_cheap_combo.yaml:71`, `adversarial_merge_consistency.yaml:136` | OUT | "3 attempts" / "5 attempts" | eval-suite fixture text | — |
| `pr_submit/fsm.py:33`, `pr_submit/loop_guard.py:20` | OUT | `HARD_CAP_MAX_ROUNDS = 5` | user-raised `--max-rounds` ceiling (kept by decision) | — |
| `agents/rf-qa.md:82`, `rf-qa-qualitative.md:83`, `rf-analyst.md:74`, `task-builder/SKILL.md` (3 hits), `sc-tasklist-protocol/SKILL.md` (1 hit) | OUT | closed vocabulary `gap-fill-round-3` | identifier; becomes unreachable once A.8 is 2 rounds but stays valid | — |

## Totals

- Raw hits: **160** = **114 IN** + **46 OUT**.
- Missed IN sites found by extra greps: **24** (`rf-task-builder.md` 383/385/387; `01_mdtm` 649/651/653; `02_mdtm` 662/664/666/667; `cli_portify/convergence.py:165`; `cli_portify` `max_convergence` defaults in `commands.py:100-101`, `config.py:53`, `models.py:583`, `prompts.py:68`, `resume.py:136`; `sc-cli-portify-protocol/SKILL.md` 355/363/364/374/534; `decisions.yaml:123`; `ib_agent_core.md:933`; `tech-reference/SKILL.md:177`).
- Dependent edit (not a cap site): `task-builder/SKILL.md:901` sha re-pin (same sha also inside rf-qa:82, rf-qa-qualitative:83, rf-analyst:74).
- **Total IN sites: 138.**
- Tests that change: `tests/cli_portify/test_convergence.py:78-86` (default 3 → 2), `tests/audit/test_dnsp_all_agents_fail_bypass.py` + `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt` (rf-team-lead line, sha, "max-3-cycles" token), `tests/audit/test_severity_floor_unweakened.py` BASELINE_BLOCK_SHA (rf-qa-qualitative rule 10), `tests/skills/test_task_builder_merge.py:435` (comment). No test pins `max_research_fix_cycles` or the `max_convergence` default.

## 18. CAP_PATTERN hits not in the raw scan (all OUT; added 2026-11-02 by the orchestrator)

The plan's CAP_PATTERN (Constraints of package `TASK-WF-removeTheAnyIssu-20261102-042031`) matches 163 lines in the 38 IN files (`.dev/review-severity-rule/cap-pattern-hits.txt`). 132 of them are rows above; the other 31 (`.dev/review-severity-rule/unclassified-hits.txt`) are table cells that count agents, lines or phases, not fix cycles. All OUT; the Task 18 allowlist and the per-task scans treat them as OUT by quoted text.

| file:line | IN/OUT | current excerpt | replacement or reason | pinned tests |
|---|---|---|---|---|
| `skills/sc-cli-portify-protocol/SKILL.md:183, 184, 189, 190, 191` | OUT | "\| 3 \| Functional Requirements \|", "\| 4 \| Architecture \|", "\| 6 \| NFRs \|", "\| 7 \| Risk Assessment \|", "\| 8 \| Test Plan \|" | spec section numbers | — |
| `skills/task-builder/SKILL.md:136` | OUT | "\| **Quick** \| Small scope ... \| 3 \| 0 \|" | researcher/agent counts per tier | — |
| `skills/task-builder/SKILL.md:1036, 1037, 1166, 1167` | OUT | "\| Research gate \| 5 \| 2 rf-analyst ...", "\| Synthesis gate \| 5 \| ..." | agent counts per gate | — |
| `skills/task/SKILL.md:194-197` | OUT | "\| <500 lines \| 3 \| 3 \| 6 \|" .. "\| >3000 lines \| 6 \| 6 \| 12 \|" | lens-agent counts by document size | — |
| `skills/task/SKILL.md:207, 208, 209` | OUT | "\| Research gate (Phase 3) \| 5 \| ...", "\| Synthesis gate (Phase 5) \| 5 \| ...", "\| Task-integrity gate \| 5 \| ..." | agent counts per gate | — |
| `templates/workflow/01_mdtm_template_generic_task.md:691-694` | OUT | "\| <500 lines \| 3 \| 3 \| 6 \|" .. | lens-agent counts by document size | — |
| `templates/workflow/01_mdtm_template_generic_task.md:718, 719, 720` | OUT | "\| Research gate (Phase 3) \| 5 \| ..." | agent counts per gate | — |
| `templates/workflow/02_mdtm_template_complex_task.md:708-711` | OUT | "\| <500 lines \| 3 \| 3 \| 6 \|" .. | lens-agent counts by document size | — |
| `templates/workflow/02_mdtm_template_complex_task.md:735, 736, 737` | OUT | "\| Research gate (Phase 3) \| 5 \| ...", "\| task-integrity (Phase 5.5) \| 5 \| ..." | agent counts per gate | — |

## Files with at least one IN site (38)

- `src/superclaude/agents/rf-analyst.md`
- `src/superclaude/agents/rf-qa.md`
- `src/superclaude/agents/rf-qa-qualitative.md`
- `src/superclaude/agents/rf-team-lead.md`
- `src/superclaude/agents/rf-task-builder.md`
- `src/superclaude/cli/cli_portify/convergence.py`
- `src/superclaude/cli/cli_portify/steps/panel_review.py`
- `src/superclaude/cli/cli_portify/commands.py`
- `src/superclaude/cli/cli_portify/config.py`
- `src/superclaude/cli/cli_portify/models.py`
- `src/superclaude/cli/cli_portify/prompts.py`
- `src/superclaude/cli/cli_portify/resume.py`
- `src/superclaude/cli/prd/models.py`
- `src/superclaude/rules/core/ib_agent_core.md`
- `src/superclaude/skills/operational-guide/SKILL.md`
- `src/superclaude/skills/readme/SKILL.md`
- `src/superclaude/skills/roadmap/SKILL.md`
- `src/superclaude/skills/task-builder/SKILL.md`
- `src/superclaude/skills/task/SKILL.md`
- `src/superclaude/skills/tech-reference/SKILL.md`
- `src/superclaude/skills/tech-research/SKILL.md`
- `src/superclaude/skills/prd/refs/build-request-template.md`
- `src/superclaude/skills/tdd/refs/build-request-template.md`
- `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md`
- `src/superclaude/skills/sc-cli-portify-protocol/decisions.yaml`
- `src/superclaude/templates/documents/agent_template_qa.md`
- `src/superclaude/templates/documents/skill_template.md`
- `src/superclaude/templates/modularization-template-review/qa-consolidated-findings_template.md`
- `src/superclaude/templates/modularization-template-review/qa-cross-source-contradictions_template.md`
- `src/superclaude/templates/modularization-template-review/qa-fix-summary_template.md`
- `src/superclaude/templates/modularization-template-review/qa-research-depth_report_template.md`
- `src/superclaude/templates/modularization-template-review/qa-research-evidence_report_template.md`
- `src/superclaude/templates/modularization-template-review/qa-research-gap_report_template.md`
- `src/superclaude/templates/modularization-template-review/qa-source-fidelity_template.md`
- `src/superclaude/templates/modularization-template-review/qa-task-validation-b2_report_template.md`
- `src/superclaude/templates/modularization-template-review/qa-task-validation-structure_report_template.md`
- `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`
- `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`

